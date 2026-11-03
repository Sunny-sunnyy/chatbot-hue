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

from core.schema import (ContextBudgetError, CitationIntegrityError, GenerationError, GeneratorNotReadyError, RetrievalDependencyError,
                         RetrievedDocument)
from llm.answer_stream import AnswerTextStream
from llm.citations import select_cited_sources
from llm.emergency import EMERGENCY_ANSWER, is_emergency
from llm.full_corpus_prompt import (INSUFFICIENT_ANSWER, MAY_HAVE_CHANGED_NOTICE, OUT_OF_SCOPE_ANSWER, TOOL_LIMIT_TEXT, TOOL_NO_NEW_TEXT,
                                   build_assistant_input, today_line)
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
MODEL_SEARCH_LIMIT = 2  # B2 D5: số lần MODEL gọi `tim_kho` được tìm thật (lần tìm đầu của code không tính); lần 3 ⇒ TOOL_LIMIT_TEXT
SEARCH_VARIANTS = ("v0", "v1", "v2", "v3")  # B2a: lần tìm đầu (plan D1)
STREAM_DRAIN_SECONDS = 0.5  # ngắt giữa chừng: sau `result.cancel()` đọc nốt tối đa chừng này giây (spec streaming §4.5 bước 3)


@dataclass(frozen=True)
class AssistantFlags:
    """Cờ từng phần B1 (plan D9, `settings.yaml` khối `assistant:`); tắt cả 4 ⇒ chuỗi gửi model như B0.
    B2 (plan B2 D1): `lan_tim_dau` — v0 câu gốc · v1 / v3 câu tìm do định tuyến viết (cần `router`) · v2 trợ lý tự gọi `tim_kho`;
    `tim_them` — sau lần tìm đầu của code, trợ lý được gọi `tim_kho` thêm (B2b). `v0` + `tim_them` tắt ⇒ chuỗi gửi model như B1."""
    emergency_rule: bool = False
    router: bool = False
    today_line: bool = False
    may_have_changed_notice: bool = False
    lan_tim_dau: str = "v0"
    tim_them: bool = False
    # B3 (plan B3 D7): nhớ hội thoại trong một cuộc trò chuyện — tắt tới khi giao diện nhiều lượt xong (D8); chỉ nhớ câu hỏi khi `nho_cau_tra_loi` tắt
    nho_hoi_thoai: bool = False
    nho_cau_tra_loi: bool = True

    def __post_init__(self) -> None:
        if self.lan_tim_dau not in SEARCH_VARIANTS:
            raise ValueError(f"assistant.lan_tim_dau must be one of {SEARCH_VARIANTS}")
        if self.lan_tim_dau in ("v1", "v3") and not self.router:
            raise ValueError("assistant.lan_tim_dau v1 / v3 needs assistant.router: true (search text is written by the router)")

    @classmethod
    def from_settings(cls, settings: dict) -> "AssistantFlags":
        config = settings.get("assistant") or {}
        values = {name: bool(config.get(name, cls.__dataclass_fields__[name].default)) for name in cls.__dataclass_fields__ if name != "lan_tim_dau"}
        return cls(**values, lan_tim_dau=str(config.get("lan_tim_dau", "v0")))

    @property
    def uses_tools(self) -> bool:
        """Tuyến `tro_ly_hue` đi vòng công cụ (trợ lý có `tim_kho`) thay vì sinh một lần."""
        return self.lan_tim_dau == "v2" or self.tim_them


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
    # B2: câu tìm định tuyến viết (V1 / V3) — chỉ trong RAM, KHÔNG log (chữ người dùng); số câu + cờ rỗng thì log được
    cau_tim: list[str] | None = None
    cau_tim_rong: bool = False
    model_searches: int = 0  # số lần model gọi `tim_kho` (D5 trần)
    model_queries: list[str] = field(default_factory=list)  # câu tìm model viết khi gọi `tim_kho` — KHÔNG log
    context_parts: list[str] = field(default_factory=list)  # chữ ngữ cảnh mỗi lần tìm — đếm ngân sách chung (D5)
    seen_ids: list[str] = field(default_factory=list)  # chunk_id đã vào ngữ cảnh — lần tìm sau bỏ trùng (D5)
    tool_error: Exception | None = None  # lỗi tìm / ngữ cảnh trong công cụ: SDK có thể bọc lại ⇒ lõi ném lại đúng lỗi gốc
    # B3: lịch sử cuộc trò chuyện của lượt này ((câu hỏi, câu trả lời đã cắt), …) — route đọc từ kho; rỗng = không nhớ (B2). KHÔNG log.
    history: tuple[tuple[str, str], ...] = ()


async def search_into_trace(queries: list[str], *, cau_hoi: str, retrieval_service, context_builder, trace: AnswerTrace,
                            today: str | None = None, instructions: str | None = None, by: str = "code") -> PackedContext:
    """Một lần tìm của lượt: tìm `queries` (1 câu ⇒ `search`; nhiều ⇒ `search_many`, B2 V3) → dựng ngữ cảnh → nối sổ nguồn.
    Ngân sách token đếm bằng `cau_hoi` (câu thật gửi model — B2 D3) + ngữ cảnh các lần trước (`trace.context_parts`) + `instructions` của
    đường trợ lý (B2 D5); lần sau đánh số tiếp, bỏ đoạn đã có. Lần đầu điền `trace.documents` / `trace.packed` (như B1); thời gian cộng dồn.
    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `ContextBudgetError` (ngữ cảnh)."""
    tool_started = time.perf_counter()
    first = trace.packed is None
    packed = None
    try:
        started = time.perf_counter()
        if len(queries) == 1:
            result = await asyncio.to_thread(retrieval_service.search, queries[0])
        else:
            result = await asyncio.to_thread(retrieval_service.search_many, queries)
        search_ms = elapsed_ms(started)
        dense_ms = result.trace.timings_ms.get("dense_ms")  # trace giữ 3 chữ số; làm tròn 1 chữ số như các trường *_ms khác
        dense_ms = None if dense_ms is None else round(dense_ms, 1)
        if first:  # ghi ngay (như B1): ngữ cảnh lỗi sau đó thì nơi gọi vẫn đọc được số đo + kết quả tìm
            trace.documents, trace.search_ms, trace.dense_ms = result.documents, search_ms, dense_ms
        else:
            trace.search_ms = round((trace.search_ms or 0) + search_ms, 1)
            trace.dense_ms = None if dense_ms is None else round((trace.dense_ms or 0) + dense_ms, 1)

        started = time.perf_counter()
        packed = context_builder.build(cau_hoi, result.documents, today=today, first_id=len(trace.so_nguon) + 1,
                                       prior_context="\n\n".join(trace.context_parts), skip_ids=frozenset(trace.seen_ids),
                                       instructions=instructions, history=trace.history,
                                       n_tool_items=2 * trace.model_searches if by == "model" else 0)
        context_ms = elapsed_ms(started)
        if first:
            trace.packed, trace.context_ms = packed, context_ms
        else:
            trace.context_ms = round((trace.context_ms or 0) + context_ms, 1)
        trace.so_nguon.extend(packed.sources)
        trace.context_parts.append(packed.text)
        trace.seen_ids.extend(packed.document_ids)
        return packed
    finally:
        entry = {"name": "tim_kho", "ms": elapsed_ms(tool_started)}
        if not first or by == "model" or len(queries) > 1:  # B2: thêm số đo cho lần tìm thêm / do model / nhiều câu; lần tìm đầu một câu giữ như B1
            entry.update(by=by, n_queries=len(queries), n_new=None if packed is None else len(packed.sources))
        trace.tools.append(entry)


async def tim_kho(cau_tim: str, *, retrieval_service, context_builder, trace: AnswerTrace, today: str | None = None,
                  cau_hoi: str | None = None) -> None:
    """Công cụ tìm kho: tìm `cau_tim` → dựng ngữ cảnh, ghi vào `trace` + sổ nguồn. Tham số vị trí là phần model thấy (chỉ `cau_tim`);
    top-k, collection, pool, giới hạn token nằm trong `retrieval_service` / `context_builder` do code dựng (plan B0 D2). `cau_hoi` (B2 D3):
    câu thật gửi model để đếm ngân sách — None ⇒ chính `cau_tim` (B0 / B1)."""
    await search_into_trace([cau_tim], cau_hoi=cau_tim if cau_hoi is None else cau_hoi, retrieval_service=retrieval_service,
                            context_builder=context_builder, trace=trace, today=today)


def tool_for_turn(query: str, retrieval_service, context_builder, trace: AnswerTrace, today: str | None, instructions: str):
    """Hàm `tim_kho` của **một lượt** cho trợ lý có công cụ (B2 D5): generator bọc thành công cụ SDK (lõi không import SDK — T-3).
    Model chỉ thấy `cau_tim`; trần `MODEL_SEARCH_LIMIT` đếm ở đây; lần vượt ⇒ chữ "đã hết lượt", không tìm. Lỗi tìm / ngữ cảnh: ghi
    `trace.tool_error` rồi ném (lõi ném lại đúng lỗi gốc ⇒ route ra câu lỗi như B1, không đưa lỗi cho model)."""

    async def tim_kho(cau_tim: str) -> str:
        """Tìm thêm Bằng chứng trong kho tri thức Huế bằng một câu tìm đứng một mình; trả các nguồn mới, đánh số tiếp theo.

        Args:
            cau_tim: câu tìm đứng một mình cho phần thông tin còn thiếu.
        """
        trace.model_searches += 1
        trace.model_queries.append(cau_tim)  # chỉ RAM / file private của harness — không log (chữ do model viết từ câu người dùng)
        if trace.model_searches > MODEL_SEARCH_LIMIT:
            trace.tools.append({"name": "tim_kho", "ms": 0.0, "by": "model", "n_queries": 0, "n_new": 0, "het_luot": True})
            return TOOL_LIMIT_TEXT
        try:
            packed = await search_into_trace([cau_tim], cau_hoi=query, retrieval_service=retrieval_service, context_builder=context_builder,
                                             trace=trace, today=today, instructions=instructions, by="model")
        except (RetrievalDependencyError, ContextBudgetError) as exc:
            trace.tool_error = exc
            raise
        return packed.text or TOOL_NO_NEW_TEXT

    return tim_kho


# Mọi công cụ của trợ lý, một chỗ (test ranh giới khoá tên + tham số; B2 bọc `function_tool` từ đây).
TOOLS = {"tim_kho": tim_kho}


def _history_kwargs(trace: AnswerTrace) -> dict:
    """`history=` chỉ truyền khi có lịch sử: lượt không lịch sử gọi generator y như B2 (generator thay thế trong test không cần tham số này)."""
    return {"history": trace.history} if trace.history else {}


def _assistant_instructions(generator, trace: AnswerTrace) -> str:
    """Lời dặn trợ lý thật sự gửi ở lượt này (có câu dặn lịch sử khi có lịch sử — B3 D3) — để đếm ngân sách đúng chuỗi gửi (D5)."""
    return generator.assistant_instructions_for(trace.history) if trace.history else generator.assistant_instructions


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
                         today: str | None = None, instructions: str | None = None) -> None:
    """Phần trước model của tuyến `tro_ly_hue`: lần tìm đầu của code → ngữ cảnh. Câu tìm = câu gốc (V0) hoặc câu định tuyến viết
    (`trace.cau_tim`, B2 V1 / V3); ngân sách luôn đếm bằng câu gốc (B2 D3). `instructions`: lời dặn trợ lý khi lượt đi vòng công cụ (B2b).
    Ngữ cảnh không có nguồn ⇒ `trace.answer` = câu từ chối chuẩn (không gọi model). Còn lại cần model: `generator=None` nghĩa là
    chưa sẵn sàng ⇒ `GeneratorNotReadyError`. `recorder` chỉ route truyền (spec §4.8 khác biệt 4).

    Lỗi đi ra nguyên kiểu: `RetrievalDependencyError` (tìm), `ContextBudgetError` (ngữ cảnh), `GeneratorNotReadyError`."""
    await search_into_trace(trace.cau_tim or [query], cau_hoi=query, retrieval_service=retrieval_service, context_builder=context_builder,
                            trace=trace, today=today, instructions=instructions)
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


async def _before_model(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder, today: str | None,
                        flags: AssistantFlags) -> str | None:
    """Phần trước lần gọi model của tuyến `tro_ly_hue`. Trả tin nhắn user cho trợ lý có công cụ (None = đường sinh một lần như B1).
    V2: không tìm trước (chỉ cần generator). Còn lại: `prepare_answer` (có thể đặt câu từ chối khi ngữ cảnh rỗng ⇒ `fixed_outcome`)."""
    if flags.lan_tim_dau == "v2":
        if generator is None:
            raise GeneratorNotReadyError("generator is not ready")
        return build_assistant_input(query, None, today)
    instructions = _assistant_instructions(generator, trace) if (flags.tim_them and generator is not None) else None
    await prepare_answer(query, retrieval_service, context_builder, generator, trace, recorder, today, instructions)
    return build_assistant_input(query, trace.packed.text, today) if flags.tim_them else None


def _finish_generated(trace: AnswerTrace) -> None:
    """Sau lần sinh: chạm `max_turns` (cờ generator, B2 D5) ⇒ câu từ chối cố định `max_turns`; còn lại ⇒ kiểm citation trên sổ nguồn."""
    if getattr(trace.generated, "hit_max_turns", False):  # getattr: generator thay thế trong test chỉ có `text` (như route, B68 m-4)
        _set_fixed(trace, INSUFFICIENT_ANSWER, "max_turns")
        return
    trace.answer = trace.generated.text
    check_citations(trace)


async def answer_query(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, recorder=None,
                       today: str | None = None, flags: AssistantFlags | None = None) -> None:
    """Tuyến `tro_ly_hue` không stream: lần tìm đầu (theo `flags.lan_tim_dau`) → sinh một lần, hoặc trợ lý có công cụ (`flags.uses_tools`)
    → `check_citations`, điền `trace`. Lỗi đi ra nguyên kiểu như `prepare_answer`, thêm `GenerationError` (sinh); lỗi tìm trong công cụ
    ra đúng lỗi gốc."""
    flags = flags or AssistantFlags()
    tool_prompt = await _before_model(query, retrieval_service, context_builder, generator, trace, recorder, today, flags)
    if trace.fixed_outcome is not None:
        return

    started = time.perf_counter()
    call_log = CallLog()
    try:
        if flags.uses_tools:
            tool_fn = tool_for_turn(query, retrieval_service, context_builder, trace, today, _assistant_instructions(generator, trace))
            try:
                trace.generated = await generator.generate_with_tools(tool_prompt, tool_fn, call_log, **_history_kwargs(trace))
            except GenerationError:
                if trace.tool_error is not None:
                    raise trace.tool_error from None
                raise
        else:
            # `today` chỉ truyền khi có: generator thay thế trong test route chỉ nhận (query, context)
            kwargs = {"call_log": call_log} if today is None else {"call_log": call_log, "today": today}
            trace.generated = await generator.generate_answer(query, trace.packed.text, **kwargs, **_history_kwargs(trace))
    finally:
        trace.generation_ms = elapsed_ms(started)  # có cả khi model lỗi (route log `generation_failed` kèm thời gian)
        record_llm_calls(trace, call_log.calls, ROUTE_TRO_LY_HUE)  # cả khi lượt lỗi sau phản hồi (review C128 m-1)
    if recorder:
        recorder.record_generation_result(trace.generated)
    _finish_generated(trace)


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
            if flags.lan_tim_dau in ("v1", "v3"):  # B2 D2: định tuyến viết luôn câu tìm (cùng một lần gọi)
                trace.route, queries = await generator.route_search(query, call_log, flags.lan_tim_dau)
                trace.cau_tim = [q.strip() for q in queries if q.strip()] or None
                trace.cau_tim_rong = trace.cau_tim is None  # rỗng ⇒ tìm bằng câu gốc, đếm được
            else:
                trace.route = await generator.route(query, call_log, **_history_kwargs(trace))
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
            trace.generated = await generator.generate_chat(query, call_log, **_history_kwargs(trace))
        finally:
            trace.generation_ms = elapsed_ms(started)
            record_llm_calls(trace, call_log.calls, ROUTE_TRO_CHUYEN)
        trace.answer, trace.cited = trace.generated.text, ()  # trò chuyện không có sổ nguồn, không kiểm citation (D4)
        return
    await answer_query(query, retrieval_service, context_builder, generator, trace, recorder, _today(flags, trace), flags)
    set_notice(trace, flags)


async def answer_turn_stream(query: str, retrieval_service, context_builder, generator, trace: AnswerTrace, flags: AssistantFlags,
                             recorder=None):
    """Cùng thứ tự `answer_turn` nhưng phát sự kiện: `("status", dict)` / `("delta", str)`. Kết thúc ⇒ `trace` đủ để route dựng `sources` /
    `error` / `notice` / `done`. Hạn giờ model bọc cả vòng đọc (spec streaming §4.3); tự dừng đọc (hết giờ / ngắt) ⇒ `cancel()` + đọc nốt
    trong vùng che (spec §4.5). Lỗi đi ra nguyên kiểu (route đổi thành sự kiện `error`)."""
    result = call_log = tool_state = None
    pending_generating = False
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
            result, call_log = generator.start_chat_stream(query, **_history_kwargs(trace))
        else:
            today = _today(flags, trace)
            tool_prompt = await _before_model(query, retrieval_service, context_builder, generator, trace, recorder, today, flags)
            if trace.packed is not None:  # V2 không tìm trước (B2 D5): `searching` / `searched` đến từ lần gọi công cụ
                yield "status", {"stage": "searched", "n_sources": len(trace.packed.sources)}
            if trace.fixed_outcome is not None:  # ngữ cảnh không có nguồn ⇒ từ chối, không gọi model
                yield "delta", trace.answer
                return
            call_route = ROUTE_TRO_LY_HUE
            if flags.uses_tools:
                # B3 D9 (b): vòng công cụ ⇒ "đang viết" phát ngay trước chữ đầu (không trước các lượt `tim_kho`)
                pending_generating = True
                tool_fn = tool_for_turn(query, retrieval_service, context_builder, trace, today, _assistant_instructions(generator, trace))
                result, call_log, tool_state = generator.start_tools_stream(tool_prompt, tool_fn, **_history_kwargs(trace))
            else:
                yield "status", {"stage": "generating"}
                result, call_log = generator.start_answer_stream(query, trace.packed.text, trace.today, **_history_kwargs(trace))

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
                        if pending_generating:
                            pending_generating = False
                            yield "status", {"stage": "generating"}
                        yield "delta", text
                elif event.type == "run_item_stream_event" and event.name == "tool_called":  # thẻ công cụ (B2 D7): lượt gọi không có chữ
                    yield "status", {"stage": "searching"}
                elif event.type == "run_item_stream_event" and event.name == "tool_output":
                    yield "status", {"stage": "searched", "n_sources": len(trace.so_nguon)}
        except Exception:
            if trace.tool_error is not None:  # lỗi tìm trong công cụ: SDK có thể bọc lại ⇒ ném đúng lỗi gốc (route ra câu lỗi như B1)
                raise trace.tool_error from None
            raise
        finally:
            trace.generation_ms = elapsed_ms(started)

        trace.generated = generator.finish_answer_stream(result, call_log, generator_started, tool_state)
        if call_route == ROUTE_TRO_CHUYEN:
            trace.answer, trace.cited = trace.generated.text, ()
        else:
            _finish_generated(trace)
            if trace.fixed_outcome is not None:  # chạm `max_turns`: không có chữ model nào ⇒ câu từ chối thành một `delta` (B2 D5)
                yield "delta", trace.answer
                return
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
