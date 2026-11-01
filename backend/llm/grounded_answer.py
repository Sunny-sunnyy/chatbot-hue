"""Lõi chung của một lượt hỏi: tìm → dựng ngữ cảnh → sinh → kiểm citation.

`POST /api/chat` (`api/routes/chat.py`) và bộ đánh giá (`evaluation/full_corpus_eval.py` `answer_case`) cùng gọi
`answer_query`, nên hai nơi đi đúng một đường (spec streaming `2026-10-31-streaming-design.md` §3, §4.8).

Lõi chỉ làm các bước và ném lỗi có kiểu; nó **không** quyết phản hồi. Mỗi nơi gọi tự giữ cách của mình (spec §4.8):
route đổi lỗi ra mã HTTP, chuẩn hóa `[Nguồn n]` → `[n]`, trả 500 khi citation hỏng, ghi `EvidenceRecorder`; bộ đánh giá
giữ chữ gốc, giữ chữ khi citation hỏng, đổi mọi lỗi thành `row["error"]`.
"""
import asyncio
import time
from dataclasses import dataclass

from core.schema import CitationIntegrityError, GeneratorNotReadyError, RetrievedDocument
from llm.citations import select_cited_sources
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.generator_openai_full_corpus import GeneratedText
from retrieval.full_corpus_context import PackedContext, PackedSource


def elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 1)


@dataclass
class AnswerTrace:
    """Một lượt đã đi tới đâu. Lõi điền dần từng bước, nên khi một bước ném lỗi nơi gọi vẫn đọc được các bước trước
    (route: số đo `chat_metrics` của lần lỗi; bộ đánh giá: `top_chunk_ids`, `context_sources`, token của dòng lỗi)."""

    documents: list[RetrievedDocument] | None = None  # toàn bộ kết quả tìm, đúng thứ tự
    search_ms: float | None = None
    dense_ms: float | None = None
    packed: PackedContext | None = None
    context_ms: float | None = None
    generated: GeneratedText | None = None  # None khi ngữ cảnh không có nguồn ⇒ từ chối, không gọi model
    generation_ms: float | None = None
    answer: str | None = None  # chữ gốc của model (chưa chuẩn hóa citation) hoặc câu từ chối chuẩn
    cited: tuple[PackedSource, ...] | None = None  # nguồn được trích; chỉ có khi citation hợp lệ
    citation_ms: float | None = None
    citation_error: CitationIntegrityError | None = None  # citation hỏng: không ném, để mỗi nơi tự xử (spec §4.8 khác biệt 2)


async def answer_query(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None) -> None:
    """Chạy một lượt, điền `trace`. `generator=None` nghĩa là chưa sẵn sàng: chỉ ném `GeneratorNotReadyError` khi thật sự cần
    gọi model (ngữ cảnh rỗng vẫn từ chối được). `recorder` chỉ route truyền (spec §4.8 khác biệt 4).

    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `ContextBudgetError` (ngữ cảnh), `GeneratorNotReadyError`,
    `GenerationError` (sinh)."""
    started = time.perf_counter()
    result = await asyncio.to_thread(retrieval_service.search, query)
    trace.search_ms = elapsed_ms(started)
    dense_ms = result.trace.timings_ms.get("dense_ms")  # trace giữ 3 chữ số; làm tròn 1 chữ số như các trường *_ms khác
    trace.dense_ms = None if dense_ms is None else round(dense_ms, 1)
    trace.documents = result.documents

    started = time.perf_counter()
    trace.packed = context_builder.build(query, result.documents)
    trace.context_ms = elapsed_ms(started)
    if recorder:
        recorder.record_packed_context(trace.packed)

    if not trace.packed.sources:
        if recorder:
            recorder.record_fallback()
        trace.answer = INSUFFICIENT_ANSWER  # từ chối trước khi gọi model
        return

    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")

    started = time.perf_counter()
    try:
        trace.generated = await generator.generate_answer(query, trace.packed.text)
    finally:
        trace.generation_ms = elapsed_ms(started)  # có cả khi model lỗi (route log `generation_failed` kèm thời gian)
    if recorder:
        recorder.record_generation_result(trace.generated)
    trace.answer = trace.generated.text

    # Kiểm trên chữ gốc: regex citation nhận cả `[n]` lẫn `[Nguồn n]` nên kết quả giống hệt kiểm sau chuẩn hóa.
    started = time.perf_counter()
    try:
        trace.cited = select_cited_sources(trace.answer, trace.packed.sources)
        trace.citation_ms = elapsed_ms(started)
    except CitationIntegrityError as exc:
        trace.citation_error = exc
