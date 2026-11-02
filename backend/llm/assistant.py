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

import json
import logging

import anyio

from core.schema import CitationIntegrityError, GenerationError, GeneratorNotReadyError, RetrievedDocument
from llm.answer_stream import AnswerTextStream
from llm.citations import select_cited_sources
from llm.emergency import EMERGENCY_ANSWER, is_emergency
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, MAY_HAVE_CHANGED_NOTICE, OUT_OF_SCOPE_ANSWER, today_line
from llm.generator_openai_full_corpus import CallLog, GeneratedText
from retrieval.full_corpus_context import PackedContext, PackedSource

logger = logging.getLogger("chat")  # cùng logger với route: dòng `chat_stream_drain` giữ tên + khuôn như trước B1

# Tuyến (spec Phase 9 §3). B0: mọi câu `tro_ly_hue` = đường RAG 1–8. B1: luật khẩn cấp + định tuyến chọn một trong 4.
ROUTE_TRO_LY_HUE = "tro_ly_hue"
ROUTE_TRO_CHUYEN = "tro_chuyen"
ROUTE_NGOAI_PHAM_VI = "ngoai_pham_vi"
ROUTE_KHAN_CAP = "khan_cap"
# H4c (B1 D8): nguồn trích thuộc vé / điểm đến / lễ hội ⇒ dòng "có thể đã thay đổi".
NOTICE_SOURCE_PREFIXES = ("travel/tickets/", "travel/places/", "festivals/")
STREAM_DRAIN_SECONDS = 0.5  # ngắt giữa chừng: sau `result.cancel()` đọc nốt tối đa chừng này giây (spec streaming §4.5 bước 3)


@dataclass(frozen=True)
class AssistantFlags:
    """Cờ từng phần B1 (plan D9, `settings.yaml` khối `assistant:`); tắt cả 4 ⇒ chuỗi gửi model như B0."""
    emergency_rule: bool = False
    router: bool = False
    today_line: bool = False
    may_have_changed_notice: bool = False

    @classmethod
    def from_settings(cls, settings: dict) -> "AssistantFlags":
        config = settings.get("assistant") or {}
        return cls(**{name: bool(config.get(name, False)) for name in cls.__dataclass_fields__})


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
    llm_calls: list[dict] = field(default_factory=list)  # mỗi lần gọi model (generator `CallLog`) + `route` của lần gọi
    # B1: câu trả lời cố định (không qua kiểm citation) ⇒ outcome riêng: "emergency" / "out_of_scope" / "refusal_no_sources"
    fixed_outcome: str | None = None
    emergency_by: str | None = None  # "rule" (luật code) | "router" (định tuyến chọn khan_cap)
    route_error: str | None = None  # định tuyến lỗi ⇒ đi `tro_ly_hue`
    routing_ms: float | None = None
    today: str | None = None  # dòng ngày đã gửi model (D7) — log chỉ ghi phần ngày
    notice: str | None = None  # dòng H4c (D8)


async def tim_kho(cau_tim: str, *, retrieval_service, context_builder, trace: AnswerTrace, today: str | None = None) -> None:
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
        trace.packed = context_builder.build(cau_tim, result.documents, today=today)  # dòng ngày tính vào ngân sách token (D7)
        trace.context_ms = elapsed_ms(started)
        trace.so_nguon.extend(trace.packed.sources)
    finally:
        trace.tools.append({"name": "tim_kho", "ms": elapsed_ms(tool_started)})


# Mọi công cụ của trợ lý, một chỗ (test ranh giới khoá tên + tham số; B2 bọc `function_tool` từ đây).
TOOLS = {"tim_kho": tim_kho}


def record_llm_calls(trace: AnswerTrace, calls, call_route: str | None = None) -> None:
    """Nối các lần gọi model đã xong vào `trace.llm_calls`, mỗi mục gắn tuyến của **lần gọi** (`router` / `tro_chuyen` / `tro_ly_hue`)."""
    trace.llm_calls.extend({"route": call_route or trace.route, **call} for call in calls)


def turn_usd(trace: AnswerTrace) -> float | None:
    """USD của cả lượt = cộng từng lần gọi. Không gọi model (câu cố định, từ chối trước model, lỗi trước bước sinh) ⇒ 0; đã gọi mà không có
    mục nào (ngắt / lỗi giữa chừng — không có usage) ⇒ None, không đoán."""
    if trace.llm_calls:
        return sum(call["usd"] for call in trace.llm_calls)
    return 0.0 if trace.generation_ms is None and trace.routing_ms is None else None


async def prepare_answer(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None,
                         today: str | None = None) -> None:
    """Phần trước model của tuyến `tro_ly_hue`: `tim_kho` bằng câu gốc → ngữ cảnh.
    Ngữ cảnh không có nguồn ⇒ `trace.answer` = câu từ chối chuẩn (không gọi model). Còn lại cần model: `generator=None` nghĩa là
    chưa sẵn sàng ⇒ `GeneratorNotReadyError`. `recorder` chỉ route truyền (spec §4.8 khác biệt 4).

    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `ContextBudgetError` (ngữ cảnh), `GeneratorNotReadyError`."""
    await tim_kho(query, retrieval_service=retrieval_service, context_builder=context_builder, trace=trace, today=today)
    if recorder:
        recorder.record_packed_context(trace.packed)

    if not trace.packed.sources:
        if recorder:
            recorder.record_fallback()
        trace.answer = INSUFFICIENT_ANSWER  # từ chối trước khi gọi model
        trace.fixed_outcome = "refusal_no_sources"
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


def set_notice(trace: AnswerTrace, flags: AssistantFlags) -> None:
    """H4c (D8): câu trả lời kho có nguồn được trích thuộc vé / điểm đến / lễ hội ⇒ dòng cố định. Chữ câu trả lời không đổi."""
    if flags.may_have_changed_notice and trace.cited and any(src.source.startswith(NOTICE_SOURCE_PREFIXES) for src in trace.cited):
        trace.notice = MAY_HAVE_CHANGED_NOTICE


async def answer_query(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None,
                       today: str | None = None) -> None:
    """Tuyến `tro_ly_hue` không stream: `prepare_answer` → sinh → `check_citations`, điền `trace`.
    Lỗi đi ra nguyên kiểu như `prepare_answer`, thêm `GenerationError` (sinh)."""
    await prepare_answer(query, retrieval_service, context_builder, generator, trace, recorder, today)
    if not trace.packed.sources:
        return

    started = time.perf_counter()
    call_log = CallLog()
    try:
        # `today` chỉ truyền khi có: generator thay thế trong test route chỉ nhận (query, context)
        kwargs = {"call_log": call_log} if today is None else {"call_log": call_log, "today": today}
        trace.generated = await generator.generate_answer(query, trace.packed.text, **kwargs)
    finally:
        trace.generation_ms = elapsed_ms(started)  # có cả khi model lỗi (route log `generation_failed` kèm thời gian)
        record_llm_calls(trace, call_log.calls, ROUTE_TRO_LY_HUE)  # cả khi lượt lỗi sau phản hồi (review C128 m-1)
    if recorder:
        recorder.record_generation_result(trace.generated)
    trace.answer = trace.generated.text
    check_citations(trace)


# ---------- Một lượt có định tuyến (Phase 9 B1, plan D1, D6) ----------

def _set_fixed(trace: AnswerTrace, text: str, outcome: str) -> None:
    trace.answer, trace.cited, trace.fixed_outcome = text, (), outcome


async def _pick_route(query: str, generator, trace: AnswerTrace, flags: AssistantFlags) -> None:
    """Luật khẩn cấp (code) ⇒ định tuyến (model) ⇒ câu cố định cho `khan_cap` / `ngoai_pham_vi`. Còn lại để `trace.route` cho bước sau."""
    if flags.emergency_rule and is_emergency(query):
        trace.route, trace.emergency_by = ROUTE_KHAN_CAP, "rule"
        _set_fixed(trace, EMERGENCY_ANSWER, "emergency")
        return
    if flags.router and generator is not None:
        started = time.perf_counter()
        call_log = CallLog()
        try:
            trace.route = await generator.route(query, call_log)
        except GenerationError:
            trace.route, trace.route_error = ROUTE_TRO_LY_HUE, "router_failed"  # lỗi ⇒ đường cũ (D3)
        finally:
            trace.routing_ms = elapsed_ms(started)
            record_llm_calls(trace, call_log.calls, "router")
    if trace.route == ROUTE_KHAN_CAP:
        trace.emergency_by = "router"
        _set_fixed(trace, EMERGENCY_ANSWER, "emergency")
    elif trace.route == ROUTE_NGOAI_PHAM_VI:
        _set_fixed(trace, OUT_OF_SCOPE_ANSWER, "out_of_scope")


def _today(flags: AssistantFlags, trace: AnswerTrace) -> str | None:
    trace.today = today_line() if flags.today_line else None
    return trace.today


async def answer_turn(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                      recorder=None) -> None:
    """Một lượt không stream (`POST /api/chat`, `answer_case`): luật khẩn cấp ⇒ định tuyến ⇒ trả lời theo tuyến. Lỗi như `answer_query`."""
    await _pick_route(query, generator, trace, flags)
    if trace.fixed_outcome is not None:
        return
    if trace.route == ROUTE_TRO_CHUYEN:
        started = time.perf_counter()
        call_log = CallLog()
        try:
            trace.generated = await generator.generate_chat(query, call_log)
        finally:
            trace.generation_ms = elapsed_ms(started)
            record_llm_calls(trace, call_log.calls, ROUTE_TRO_CHUYEN)
        trace.answer, trace.cited = trace.generated.text, ()  # trò chuyện không có sổ nguồn, không kiểm citation (D4)
        return
    await answer_query(query, retrieval_service, context_builder, generator, trace, recorder, _today(flags, trace))
    set_notice(trace, flags)


async def answer_turn_stream(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                             recorder=None):
    """Cùng thứ tự `answer_turn` nhưng phát sự kiện: `("status", dict)` / `("delta", str)`. Kết thúc ⇒ `trace` đủ để route dựng `sources` /
    `error` / `notice` / `done`. Hạn giờ model bọc cả vòng đọc (spec streaming §4.3); tự dừng đọc (hết giờ / ngắt) ⇒ `cancel()` + đọc nốt
    trong vùng che (spec §4.5). Lỗi đi ra nguyên kiểu (route đổi thành sự kiện `error`)."""
    result = call_log = None
    call_route = None
    stopped_early = False
    try:
        if flags.router and generator is not None and not (flags.emergency_rule and is_emergency(query)):
            yield "status", {"stage": "routing"}
        await _pick_route(query, generator, trace, flags)
        if trace.fixed_outcome is not None:
            yield "delta", trace.answer
            return
        if trace.route == ROUTE_TRO_CHUYEN:
            yield "status", {"stage": "generating"}
            call_route = ROUTE_TRO_CHUYEN
            result, call_log = generator.start_chat_stream(query)
        else:
            await prepare_answer(query, retrieval_service, context_builder, generator, trace, recorder, _today(flags, trace))
            yield "status", {"stage": "searched", "n_sources": len(trace.packed.sources)}
            if trace.fixed_outcome is not None:  # ngữ cảnh không có nguồn ⇒ từ chối, không gọi model
                yield "delta", trace.answer
                return
            yield "status", {"stage": "generating"}
            call_route = ROUTE_TRO_LY_HUE
            result, call_log = generator.start_answer_stream(query, trace.packed.text, trace.today)

        started, generator_started = time.perf_counter(), time.monotonic()
        extractor = AnswerTextStream()
        events = result.stream_events()
        deadline = asyncio.get_running_loop().time() + generator.timeout
        try:
            while True:
                try:
                    async with asyncio.timeout_at(deadline):
                        event = await anext(events)
                except StopAsyncIteration:
                    break
                if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
                    text = extractor.feed(event.data.delta)
                    if text:
                        yield "delta", text
        finally:
            trace.generation_ms = elapsed_ms(started)

        trace.generated = generator.finish_answer_stream(result, call_log, generator_started)
        trace.answer = trace.generated.text
        if call_route == ROUTE_TRO_CHUYEN:
            trace.cited = ()
        else:
            check_citations(trace)
            set_notice(trace, flags)
    except (asyncio.CancelledError, GeneratorExit, TimeoutError):
        stopped_early = True
        raise
    finally:
        if call_log is not None:
            record_llm_calls(trace, call_log.calls, call_route)
        if result is not None and stopped_early:
            # dừng lần gọi model rồi đọc nốt bằng iterator mới, trong vùng che có hạn giờ (spec streaming §4.5). Không dựa `result.is_complete`.
            result.cancel()
            drain_started = time.perf_counter()
            with anyio.CancelScope(shield=True):
                with anyio.move_on_after(STREAM_DRAIN_SECONDS) as drain_scope:
                    async for _ in result.stream_events():
                        pass
            logger.info("chat_stream_drain %s", json.dumps({"finished": not drain_scope.cancelled_caught,
                                                             "ms": elapsed_ms(drain_started)}))
