"""Lõi chung của trợ lý (Phase 9; đổi tên + thêm `tim_kho` / sổ nguồn / log ở B0): tìm kho (`tim_kho`) → dựng ngữ cảnh → sinh → kiểm citation.

`POST /api/chat` (`api/routes/chat.py`) và bộ đánh giá (`evaluation/full_corpus_eval.py` `answer_case`) cùng gọi `answer_query`;
`POST /api/chat/stream` gọi chung `prepare_answer` (phần trước model) và `check_citations`, chỉ phần sinh là stream
(spec streaming `2026-10-31-streaming-design.md` §3, §4.8). Phase 9 B0 (plan `docs/superpowers/plans/2026-11-02-phase-9-b0-plan.md`):
đường trả lời giữ y RAG 1–8 — code gọi `tim_kho` bằng câu gốc, sinh một lần; định tuyến (B1) và vòng công cụ do model gọi (B2) chưa có.

Ranh giới (plan B0 D3, test `tests/test_assistant_boundary.py`): module này **không** import SDK / client mạng; mọi lần gọi OpenAI nằm ở
`llm/generator_openai_full_corpus.py`. Lõi giữ chính sách (tuyến, công cụ, sổ nguồn, tiền mỗi lượt) bằng hàm Python thường.

Lõi chỉ làm các bước và ném lỗi có kiểu; nó **không** quyết phản hồi. Mỗi nơi gọi tự giữ cách của mình (spec streaming §4.8):
route đổi lỗi ra mã HTTP, chuẩn hóa `[Nguồn n]` → `[n]`, trả 500 khi citation hỏng, ghi `EvidenceRecorder`; bộ đánh giá
giữ chữ gốc, giữ chữ khi citation hỏng, đổi mọi lỗi thành `row["error"]`.
"""
import asyncio
import time
from dataclasses import dataclass, field

from core.schema import CitationIntegrityError, GeneratorNotReadyError, RetrievedDocument
from llm.citations import select_cited_sources
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.generator_openai_full_corpus import GeneratedText
from retrieval.full_corpus_context import PackedContext, PackedSource

# B0 chưa định tuyến: mọi câu đi đường RAG 1–8, đúng tuyến `tro_ly_hue` của spec Phase 9 §5 B1.
ROUTE_TRO_LY_HUE = "tro_ly_hue"


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
    route: str = ROUTE_TRO_LY_HUE
    # Sổ nguồn của cả lượt: mọi kiểm citation đọc từ đây. B0 một lần tìm ⇒ sổ = nguồn của ngữ cảnh, giữ nguyên số [n];
    # đánh số nối khi tìm nhiều lần (B2b) và phần web [w n] (B6) để plan bậc đó (plan B0 D4).
    so_nguon: list[PackedSource] = field(default_factory=list)
    tools: list[dict] = field(default_factory=list)  # mỗi lần chạy công cụ: {"name", "ms"}
    llm_calls: list[dict] = field(default_factory=list)  # mỗi lần gọi model (generator `CallLog`) + `route` của lượt


async def tim_kho(cau_tim: str, *, retrieval_service, context_builder, trace: AnswerTrace) -> None:
    """Công cụ tìm kho: tìm `cau_tim` → dựng ngữ cảnh, ghi vào `trace` + sổ nguồn. Tham số vị trí là phần model sẽ thấy khi B2 cho model gọi
    (chỉ `cau_tim`); top-k, collection, pool, giới hạn token nằm trong `retrieval_service` / `context_builder` do code dựng (plan B0 D2).
    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `ContextBudgetError` (ngữ cảnh)."""
    tool_started = time.perf_counter()
    try:
        started = time.perf_counter()
        result = await asyncio.to_thread(retrieval_service.search, cau_tim)
        trace.search_ms = elapsed_ms(started)
        dense_ms = result.trace.timings_ms.get("dense_ms")  # trace giữ 3 chữ số; làm tròn 1 chữ số như các trường *_ms khác
        trace.dense_ms = None if dense_ms is None else round(dense_ms, 1)
        trace.documents = result.documents

        started = time.perf_counter()
        trace.packed = context_builder.build(cau_tim, result.documents)
        trace.context_ms = elapsed_ms(started)
        trace.so_nguon.extend(trace.packed.sources)
    finally:
        trace.tools.append({"name": "tim_kho", "ms": elapsed_ms(tool_started)})


# Mọi công cụ của trợ lý, một chỗ (test ranh giới khoá tên + tham số; B2 bọc `function_tool` từ đây).
TOOLS = {"tim_kho": tim_kho}


def record_llm_calls(trace: AnswerTrace, calls) -> None:
    """Gắn tuyến của lượt vào từng lần gọi model (generator chỉ biết token / ms / USD, không biết chính sách)."""
    trace.llm_calls = [{"route": trace.route, **call} for call in calls]


def turn_usd(trace: AnswerTrace) -> float | None:
    """USD của cả lượt = cộng từng lần gọi. Không gọi model (từ chối trước model, lỗi trước bước sinh) ⇒ 0; đã gọi mà không có mục nào
    (ngắt / lỗi giữa chừng — không có usage) ⇒ None, không đoán."""
    if trace.llm_calls:
        return sum(call["usd"] for call in trace.llm_calls)
    return 0.0 if trace.generation_ms is None else None


async def prepare_answer(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None) -> None:
    """Phần trước model, chung cho `POST /api/chat`, `POST /api/chat/stream` và bộ đánh giá: `tim_kho` bằng câu gốc → ngữ cảnh.
    Ngữ cảnh không có nguồn ⇒ `trace.answer` = câu từ chối chuẩn (không gọi model). Còn lại cần model: `generator=None` nghĩa là
    chưa sẵn sàng ⇒ `GeneratorNotReadyError`. `recorder` chỉ route truyền (spec §4.8 khác biệt 4).

    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `ContextBudgetError` (ngữ cảnh), `GeneratorNotReadyError`."""
    await tim_kho(query, retrieval_service=retrieval_service, context_builder=context_builder, trace=trace)
    if recorder:
        recorder.record_packed_context(trace.packed)

    if not trace.packed.sources:
        if recorder:
            recorder.record_fallback()
        trace.answer = INSUFFICIENT_ANSWER  # từ chối trước khi gọi model
        return

    if generator is None:
        raise GeneratorNotReadyError("generator is not ready")


def check_citations(trace: AnswerTrace) -> None:
    """Kiểm citation của `trace.answer` (chữ gốc model) với sổ nguồn. Kiểm trên chữ gốc: regex citation nhận cả `[n]` lẫn
    `[Nguồn n]` nên kết quả giống hệt kiểm sau chuẩn hóa. Hỏng ⇒ ghi `trace.citation_error`, không ném."""
    started = time.perf_counter()
    try:
        trace.cited = select_cited_sources(trace.answer, trace.so_nguon)
        trace.citation_ms = elapsed_ms(started)
    except CitationIntegrityError as exc:
        trace.citation_error = exc


async def answer_query(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None) -> None:
    """Một lượt không stream (`POST /api/chat`, `answer_case`): `prepare_answer` → sinh → `check_citations`, điền `trace`.
    Lỗi đi ra nguyên kiểu như `prepare_answer`, thêm `GenerationError` (sinh)."""
    await prepare_answer(query, retrieval_service, context_builder, generator, trace, recorder)
    if not trace.packed.sources:
        return

    started = time.perf_counter()
    try:
        trace.generated = await generator.generate_answer(query, trace.packed.text)
    finally:
        trace.generation_ms = elapsed_ms(started)  # có cả khi model lỗi (route log `generation_failed` kèm thời gian)
    # getattr: generator thay thế trong test route chỉ trả `text` (như `_copy_trace_metrics` đọc usage)
    record_llm_calls(trace, getattr(trace.generated, "llm_calls", ()))
    if recorder:
        recorder.record_generation_result(trace.generated)
    trace.answer = trace.generated.text
    check_citations(trace)
