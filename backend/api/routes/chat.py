"""Single-turn full-corpus retrieval, context building, grounded answer generation and citations.

Hai route cùng một lõi (`llm.assistant`): `POST /api/chat` trả cả câu một lần (JSON); `POST /api/chat/stream` hiện chữ dần
bằng sự kiện SSE (spec streaming `docs/superpowers/specs/2026-10-31-streaming-design.md` §4). Lỗi **trước** model của hai route đi
cùng một đoạn code (`_retrieval_not_ready`, `_error_response_for`) nên mã HTTP + thân giống nhau.
"""
import asyncio
import json
import logging
import time

import anyio
from agents.exceptions import AgentsException
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.sse import format_sse_event
from openai import OpenAIError
from pydantic import BaseModel, ConfigDict, Field

from core.schema import (
    ContextBudgetError,
    GenerationError,
    GeneratorNotReadyError,
    RetrievalDependencyError,
)
from llm.citations import normalize_citations
from llm.evidence_recorder import get_current_recorder
from llm.full_corpus_prompt import REFUSAL_ANSWERS
from llm.hoi_lai import TruongInput, ghep_cau
from api.conversations import TTL_SECONDS
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream, elapsed_ms, lich_cho_giao_dien, turn_usd

logger = logging.getLogger("chat")
router = APIRouter()

# Một dòng `chat_metrics` mỗi lần gọi vào handler (plan C59): chỉ số đếm, mã cố định và thời gian — KHÔNG ghi câu hỏi, câu trả lời,
# nội dung nguồn, chunk_id, response_id hay thông điệp lỗi. Test khóa đúng tập trường này (thêm trường phải sửa danh sách có chủ đích).
# Phase 9 B0 (spec §3 "Log + vết"): tuyến, USD cả câu, số lần + từng lần gọi model (tuyến, loại đầu ra, ms, USD, token), công cụ đã chạy (tên, ms).
METRIC_FIELDS = (
    "outcome", "status_code", "refusal", "model", "input_tokens", "output_tokens", "reasoning_tokens", "cache_write_tokens", "cached_tokens",
    "n_context_sources", "n_cited_sources", "search_ms", "dense_ms", "context_ms", "generation_ms", "citation_ms", "total_ms",
    "route", "usd", "n_llm_calls", "llm_calls", "tools",
    # B1: định tuyến lỗi ⇒ đường cũ; câu khẩn cấp do luật / định tuyến bắt; ngày đã đưa model (chỉ ngày, không giờ)
    "route_error", "emergency_by", "today",
    # B2 D9: ms của lần gọi định tuyến (đã có trong `llm_calls`, tách riêng để theo dõi tốc độ theo tuyến)
    "routing_ms",
    # B3 D4: chỉ số đếm của lịch sử đưa vào lượt này (không chữ, không mã cuộc)
    "n_history_turns", "history_tokens",
    # B4 D9: lượt hỏi lại ({loai, n} — không giá trị) · lượt ghép: số trường người dùng chọn (không giá trị)
    "hoi_lai", "co_truong",
    # B5 (plan B5 bản 7 §3, D14 (d)): có lịch + qua kiểm cuối · số điểm đã xếp · mã vi phạm kiểm cuối (D8) · mã các bước tiến độ đã phát
    "lich_trinh_ok", "lich_trinh_so_diem", "lich_trinh_kiem", "lich_trinh_buoc",
)
# Route stream thêm: ms từ lúc nhận request tới lúc gửi sự kiện đầu / mảnh chữ đầu (spec §4.6); chữ ghép từ các `delta` có trùng chữ cuối
# đã chuẩn hóa không (spec §4.3 bước 4, §6 C5 — chỉ là cờ đúng / sai, không ghi chữ).
STREAM_METRIC_FIELDS = METRIC_FIELDS + ("first_event_ms", "first_text_ms", "delta_matches_final")

GENERATION_FAILURE_MESSAGE = "Không thể tạo câu trả lời vào lúc này."
INTERNAL_ERROR_MESSAGE = "Đã xảy ra lỗi trong hệ thống. Vui lòng thử lại sau."  # giống handler 500 chung (`api/app.py`)
RETRIEVAL_UNAVAILABLE_MESSAGE = "Hệ thống tra cứu tạm thời không khả dụng."
CONTEXT_BUDGET_MESSAGE = "Không thể đóng gói ngữ cảnh trong giới hạn cho phép."


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    query: str = Field(min_length=1, max_length=500)
    truong: TruongInput | None = None  # B4 D4: giá trị chọn ở nút hỏi lại; `{}` = "Trả lời luôn"


class SourceResponse(BaseModel):
    id: int
    title: str
    heading_path: list[str]
    excerpts: list[str]


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    notice: str | None = None  # B1 H4c: dòng "có thể đã thay đổi" (D8)
    turn_id: str | None = None  # B142: mã lượt cho 👍 / 👎 (`api/feedback.py`)
    clarify: dict | None = None  # B4 D8: thẻ hỏi lại (trường + lựa chọn do code dựng)
    lich_trinh: dict | None = None  # B5 D11 / D12: link bản đồ từng điểm + thẻ "Sửa" chọn sẵn (dữ liệu code, không chữ model)


def error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


# B3 D1: cookie mã cuộc trò chuyện — HttpOnly (JS không đọc), SameSite=Strict, chỉ gửi cho /api. `Secure` tắt vì chạy http://127.0.0.1
# (bật trước khi deploy — spec §7).
CONVERSATION_COOKIE = "conversation_id"
REMEMBERED_OUTCOMES = {"success", "out_of_scope", "emergency", "refusal_no_sources", "max_turns", "hoi_lai"}


def _start_conversation(request: Request, trace: AnswerTrace, metrics: dict) -> str | None:
    """Nhớ bật ⇒ mã cuộc của lượt này (giữ cookie còn hạn, không thì cuộc mới) + đưa lịch sử vào `trace`. Nhớ tắt ⇒ None."""
    store = getattr(request.app.state, "conversations", None)
    if store is None:
        return None
    conversation_id = store.ensure(request.cookies.get(CONVERSATION_COOKIE))
    trace.history = store.history(conversation_id)
    metrics["n_history_turns"], metrics["history_tokens"] = len(trace.history), store.history_tokens(conversation_id)
    return conversation_id


def _remember(request: Request, conversation_id: str | None, query: str, trace: AnswerTrace, outcome: str | None) -> None:
    """Ghi lượt đã xong vào cuộc (D2): chỉ lượt có câu trả lời cuối — lỗi / ngắt / rút lại không ghi."""
    # B4 D5: lượt hỏi lại không có chữ trả lời nhưng vẫn lưu câu hỏi ⇒ người dùng gõ giá trị bằng chữ ở lượt sau vẫn có câu gốc
    if conversation_id is not None and outcome in REMEMBERED_OUTCOMES and (trace.answer or outcome == "hoi_lai"):
        request.app.state.conversations.append(conversation_id, query, trace.answer)


def _model_query(body: "ChatRequest", query: str, trace: AnswerTrace, metrics: dict) -> str:
    """B4 D4: có giá trị trường ⇒ câu ghép đủ ý gửi model (không hỏi lại lần hai); lần tìm đầu vẫn bằng câu gốc (m-3). Không ⇒ câu gốc."""
    if body.truong is None:
        return query
    trace.truong, trace.search_query = body.truong.model_dump(exclude_none=True), query
    metrics["co_truong"] = len(body.truong.model_dump(exclude_none=True))
    return ghep_cau(query, body.truong)


def _new_turn_id(request: Request, trace: AnswerTrace, outcome: str | None) -> str | None:
    """B142: mã lượt ngẫu nhiên cho lượt có câu trả lời cuối (đánh giá 👍 / 👎) — không liên quan mã cuộc trò chuyện."""
    turns = getattr(request.app.state, "feedback_turns", None)
    return None if turns is None else turns.add(trace.route, outcome, 0 if trace.cited is None else len(trace.cited))


def _set_cookie(response, conversation_id: str | None) -> None:
    if conversation_id is not None:
        response.set_cookie(CONVERSATION_COOKIE, conversation_id, max_age=TTL_SECONDS, path="/api", httponly=True, samesite="strict",
                            secure=False)


@router.post("/api/conversation/new")
async def new_conversation(request: Request):
    """"Cuộc trò chuyện mới" (D1): xoá cuộc hiện tại khỏi RAM, đặt mã mới. Nhớ tắt ⇒ không làm gì."""
    store = getattr(request.app.state, "conversations", None)
    response = JSONResponse({"nho_hoi_thoai": store is not None})
    if store is not None:
        _set_cookie(response, store.reset(request.cookies.get(CONVERSATION_COOKIE)))
    return response


@router.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, request: Request, response: Response):
    """Điểm ghi số đo duy nhất: mọi nhánh của `_answer`, kể cả exception đi tới handler 500 chung (`api/app.py`), đều có đúng một dòng log.
    Phần suy `outcome` chỉ đọc giá trị kiểu thường; log không được đổi phản hồi."""
    started = time.perf_counter()
    metrics = dict.fromkeys(METRIC_FIELDS)
    try:
        result, conversation_id = await _answer(body, request, metrics)
        _set_outcome(result, metrics)
        # cookie đi theo cả phản hồi lỗi (review C145 m-2): lượt đầu lỗi không để lại cuộc mồ côi, đồng nhất với đường stream
        _set_cookie(result if isinstance(result, JSONResponse) else response, conversation_id)
        return result
    except Exception:
        metrics["outcome"], metrics["status_code"] = "internal_error", 500
        raise
    finally:
        metrics["total_ms"] = elapsed_ms(started)
        logger.info("chat_metrics %s", json.dumps(metrics))


def _set_outcome(response, metrics: dict) -> None:
    if isinstance(response, JSONResponse):  # mọi lỗi của route đều qua error_response(...)
        metrics["status_code"] = response.status_code
        if metrics["outcome"] is None:
            metrics["outcome"] = json.loads(response.body)["error"]["code"]
    else:
        metrics["status_code"] = 200
        metrics["refusal"] = response.answer.strip() in REFUSAL_ANSWERS
        if metrics["outcome"] is None:
            metrics["outcome"] = "success"


async def _answer(body: ChatRequest, request: Request, metrics: dict):
    """Trả (phản hồi, mã cuộc trò chuyện hoặc None). Lỗi trước khi vào cuộc ⇒ không mã."""
    query = body.query.strip()
    if not query:
        return error_response(422, "invalid_request", "Yêu cầu không hợp lệ."), None

    state = request.app.state
    recorder = get_current_recorder()
    not_ready = _retrieval_not_ready(state, recorder)
    if not_ready is not None:
        return not_ready, None

    trace = AnswerTrace()
    conversation_id = _start_conversation(request, trace, metrics)
    query = _model_query(body, query, trace, metrics)
    try:
        await answer_turn(query, state.retrieval_service, state.context_builder, _ready_generator(state), trace, _flags(state), recorder)
    except (RetrievalDependencyError, ContextBudgetError, GeneratorNotReadyError, GenerationError) as exc:
        return _error_response_for(exc, recorder, metrics), conversation_id
    finally:
        _copy_trace_metrics(trace, metrics)  # cả khi lỗi: bước nào đã chạy thì có số đo của bước đó

    if trace.fixed_outcome is not None:
        metrics["outcome"] = trace.fixed_outcome  # câu cố định / từ chối trước model: không qua kiểm citation
        _remember(request, conversation_id, query, trace, trace.fixed_outcome)
        if trace.clarify is not None:  # B4: lượt hỏi lại — không chữ, không mã đánh giá
            return ChatResponse(answer="", sources=[], clarify=trace.clarify), conversation_id
        return ChatResponse(answer=trace.answer, sources=[], turn_id=_new_turn_id(request, trace, trace.fixed_outcome)), conversation_id

    if trace.citation_error is not None:
        logger.error("Citation integrity failed")
        if recorder:
            recorder.record_error("citation_integrity_failed")
        return error_response(
            500,
            "citation_integrity_error",
            "Câu trả lời không đáp ứng yêu cầu trích dẫn.",
        ), conversation_id

    if recorder:
        recorder.mark_success()

    _remember(request, conversation_id, query, trace, "success")
    return ChatResponse(answer=normalize_citations(trace.answer), sources=_source_responses(trace.cited), notice=trace.notice,
                        turn_id=_new_turn_id(request, trace, "success"),
                        lich_trinh=lich_cho_giao_dien(trace, _flags(state), trace.search_query or query)), conversation_id


# ---------- Phần trước model, chung cho hai route ----------

def _ready_generator(state):
    return state.generator if getattr(state, "generator_ready", False) else None


def _flags(state) -> AssistantFlags:
    return getattr(state, "assistant_flags", None) or AssistantFlags()


def _retrieval_not_ready(state, recorder) -> JSONResponse | None:
    if getattr(state, "retrieval_ready", False):
        return None
    if recorder:
        recorder.record_error("retrieval_unavailable")
    return error_response(
        getattr(state, "retrieval_error_status", 503),
        getattr(state, "retrieval_error_code", "retrieval_unavailable"),
        getattr(
            state,
            "retrieval_error_message",
            "Hệ thống tra cứu tạm thời không khả dụng.",
        ),
    )


def _error_response_for(exc: Exception, recorder, metrics: dict) -> JSONResponse:
    """Lỗi có kiểu của lõi ⇒ phản hồi JSON (route stream chỉ gặp 3 lớp đầu: lỗi sinh của nó xảy ra sau khi luồng đã mở)."""
    if isinstance(exc, RetrievalDependencyError):
        logger.error("Retrieval dependency error")
        if recorder:
            recorder.record_error("retrieval_unavailable")
        return error_response(503, "retrieval_unavailable", RETRIEVAL_UNAVAILABLE_MESSAGE)
    if isinstance(exc, ContextBudgetError):
        if recorder:
            recorder.record_error("context_budget_error")
        return error_response(500, "context_budget_error", CONTEXT_BUDGET_MESSAGE)
    if isinstance(exc, GeneratorNotReadyError):
        if recorder:
            recorder.record_error("generation_unavailable")
        return error_response(502, "generation_unavailable", GENERATION_FAILURE_MESSAGE)
    metrics["outcome"] = "generation_failed"  # GenerationError: cùng mã 502 với "chưa sẵn sàng", nhưng đã gọi model rồi lỗi
    logger.error("Answer generation failed")
    if recorder:
        recorder.record_error("generation_failed")
    return error_response(502, "generation_unavailable", GENERATION_FAILURE_MESSAGE)


def _source_responses(cited) -> list[SourceResponse]:
    return [
        SourceResponse(
            id=source.id,
            title=source.title,
            heading_path=list(source.heading_path),
            excerpts=list(source.excerpts),
        )
        for source in cited
    ]


def _copy_trace_metrics(trace: AnswerTrace, metrics: dict) -> None:
    metrics.update(
        search_ms=trace.search_ms, dense_ms=trace.dense_ms, context_ms=trace.context_ms,
        n_context_sources=None if trace.packed is None else len(trace.packed.sources),
        generation_ms=trace.generation_ms, citation_ms=trace.citation_ms,
        n_cited_sources=None if trace.cited is None else len(trace.cited),
        route=trace.route, usd=turn_usd(trace), n_llm_calls=len(trace.llm_calls), llm_calls=trace.llm_calls, tools=trace.tools,
        route_error=trace.route_error, emergency_by=trace.emergency_by, routing_ms=trace.routing_ms, n_history_turns=len(trace.history),
        hoi_lai=None if trace.clarify is None else {"loai": trace.clarify["loai"], "n": len(trace.clarify["truong"])},
        lich_trinh_ok=None if trace.lich is None else not trace.lich_kiem and trace.citation_error is None,
        lich_trinh_so_diem=None if trace.lich is None else len(trace.lich["nguon"]),
        lich_trinh_kiem=trace.lich_kiem, lich_trinh_buoc=[b["buoc"] for b in trace.buoc_lich] or None,
        today=None if trace.today is None else trace.today.split(", ")[-1].split(" ")[0],  # chỉ "dd/mm/yyyy"
    )
    if trace.generated is not None:
        # getattr như EvidenceRecorder: route chỉ đòi `generated.text`; thiếu trường usage thì log None, không đổi phản hồi (B68 m-4)
        metrics.update({field: getattr(trace.generated, field, None)
                        for field in ("model", "input_tokens", "output_tokens", "reasoning_tokens", "cache_write_tokens", "cached_tokens")})


# ---------- Route stream ----------

@router.post("/api/chat/stream")
async def chat_stream(body: ChatRequest, request: Request):
    """Lỗi trước luồng: chỉ còn "chưa sẵn sàng" (tìm kho / generator) ⇒ JSON mã + thân như `/api/chat`, dòng log ghi ở đây. Qua hết ⇒ mở
    luồng SSE; định tuyến + tìm kho chạy **trong** luồng (Phase 9 B1 D6 — đổi cố ý: lỗi Qdrant giữa lượt ⇒ sự kiện `error` mang đúng câu 503 cũ).
    `_answer_events` tự ghi dòng log ở `finally` của nó ⇒ vẫn đúng một dòng mỗi lần gọi."""
    started = time.perf_counter()
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream_opened = False
    try:
        query = body.query.strip()
        if not query:
            response = error_response(422, "invalid_request", "Yêu cầu không hợp lệ.")
            _set_outcome(response, metrics)
            return response
        state = request.app.state
        recorder = get_current_recorder()
        response = _retrieval_not_ready(state, recorder)
        if response is not None:
            _set_outcome(response, metrics)
            return response

        generator = _ready_generator(state)
        if generator is None:
            response = _error_response_for(GeneratorNotReadyError("generator is not ready"), recorder, metrics)
            _set_outcome(response, metrics)
            return response

        trace = AnswerTrace()
        conversation_id = _start_conversation(request, trace, metrics)
        query = _model_query(body, query, trace, metrics)
        turn = answer_turn_stream(query, state.retrieval_service, state.context_builder, generator, trace, _flags(state), recorder)
        cau_goc = trace.search_query or query

        def remember() -> None:  # gọi ở `finally` của luồng, sau khi outcome đã có
            _remember(request, conversation_id, query, trace, metrics["outcome"])

        response = StreamingResponse(
            _answer_events(turn, trace, metrics, started, remember, lambda: _new_turn_id(request, trace, metrics["outcome"]),
                           lambda: lich_cho_giao_dien(trace, _flags(state), cau_goc)),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
        _set_cookie(response, conversation_id)
        stream_opened = True
        return response
    except Exception:
        metrics["outcome"], metrics["status_code"] = "internal_error", 500
        raise
    finally:
        if not stream_opened:
            metrics["total_ms"] = elapsed_ms(started)
            logger.info("chat_metrics %s", json.dumps(metrics))


def sse_event(event: str, data: dict | list) -> bytes:
    return format_sse_event(event=event, data_str=json.dumps(data, ensure_ascii=False))


class StreamEvents:
    """Dựng sự kiện SSE của một lượt stream và điền `outcome` / mốc thời gian vào `metrics` (spec §4.4, §4.6). Không gọi model ⇒ test
    được bằng chữ có sẵn; `_answer_events` chỉ nối nó với luồng model."""

    def __init__(self, metrics: dict, started: float, new_turn_id=None, lich=None) -> None:
        self.metrics = metrics
        self.started = started
        self.new_turn_id = new_turn_id  # B142: cấp mã lượt (đánh giá 👍 / 👎) ở `done` của lượt có câu trả lời cuối; None ⇒ `done` như cũ
        self.lich = lich  # B5: dựng dữ liệu sự kiện `lich_trinh` (link bản đồ + thẻ Sửa) khi lượt có lịch qua kiểm; None ⇒ không có sự kiện
        self.seq = 0
        self.shown: list[str] = []  # các mảnh chữ đã gửi

    def status(self, data: dict) -> bytes:
        if self.metrics["first_event_ms"] is None:
            self.metrics["first_event_ms"] = elapsed_ms(self.started)
        return sse_event("status", data)

    def delta(self, text: str) -> bytes:
        if self.metrics["first_text_ms"] is None:
            self.metrics["first_text_ms"] = elapsed_ms(self.started)
        self.shown.append(text)
        self.seq += 1
        return sse_event("delta", {"seq": self.seq, "text": text})

    def done(self, answered: bool = False) -> bytes:
        data = {"outcome": self.metrics["outcome"]}
        if answered and self.new_turn_id is not None:
            data["turn_id"] = self.new_turn_id()
        return sse_event("done", data)

    def fixed(self, trace: AnswerTrace) -> list[bytes]:
        """Câu cố định (khẩn cấp, ngoài phạm vi, từ chối khi ngữ cảnh không có nguồn) — chữ đã ra một `delta`; không kiểm citation."""
        self.metrics["outcome"] = trace.fixed_outcome
        self.metrics["refusal"] = trace.answer.strip() in REFUSAL_ANSWERS
        self.metrics["delta_matches_final"] = "".join(self.shown).strip() == trace.answer.strip()
        if trace.clarify is not None:  # B4 D8: lượt hỏi lại ⇒ thẻ nút, không chữ, không mã đánh giá
            return [sse_event("clarify", trace.clarify), self.done()]
        return [sse_event("sources", []), self.done(answered=True)]

    def finish(self, trace: AnswerTrace) -> list[bytes]:
        """Sau kiểm citation: qua ⇒ `sources` (chỉ nguồn được trích) [+ `notice` H4c]; hỏng ⇒ `error` để giao diện rút lại chữ (D3 (a))."""
        final = normalize_citations(trace.answer)
        self.metrics["refusal"] = final.strip() in REFUSAL_ANSWERS
        self.metrics["delta_matches_final"] = "".join(self.shown).strip() == final
        if trace.citation_error is not None:
            logger.error("Citation integrity failed")
            self.metrics["outcome"] = "retracted"
            events = [sse_event("error", {"code": "citation_integrity_error",
                                          "message": "Câu trả lời không đáp ứng yêu cầu trích dẫn.", "after_text": bool(self.shown)})]
        else:
            self.metrics["outcome"] = "success"
            events = [sse_event("sources", [source.model_dump() for source in _source_responses(trace.cited)])]
            if trace.notice is not None:
                events.append(sse_event("notice", {"text": trace.notice}))
            lich = None if self.lich is None else self.lich()
            if lich is not None:  # B5 D11 / D12: dữ liệu có cấu trúc, sau `sources` (chỉ khi lịch qua kiểm)
                events.append(sse_event("lich_trinh", lich))
        return events + [self.done(answered=trace.citation_error is None)]

    def failure(self, exc: Exception) -> list[bytes]:
        """Lỗi sau khi luồng đã mở ⇒ `error` + `done`; đã hiện chữ thì giao diện xóa hết (D3 (b)). Lỗi tìm kho / ngữ cảnh giữa lượt (B1 D6)
        mang đúng mã + câu như JSON trước luồng hôm nay (`_error_response_for`)."""
        logger.error("Answer stream failed: %s", type(exc).__name__)  # chỉ tên lớp lỗi, không thông điệp (có thể chứa nội dung)
        if isinstance(exc, RetrievalDependencyError):
            code, message = "retrieval_unavailable", RETRIEVAL_UNAVAILABLE_MESSAGE
        elif isinstance(exc, ContextBudgetError):
            code, message = "context_budget_error", CONTEXT_BUDGET_MESSAGE
        elif isinstance(exc, (TimeoutError, AgentsException, OpenAIError, GenerationError, GeneratorNotReadyError)):
            code, message = "generation_unavailable", GENERATION_FAILURE_MESSAGE
        else:
            code, message = "internal_error", INTERNAL_ERROR_MESSAGE
        if self.shown:
            self.metrics["outcome"] = "stream_error_after_text"
        else:
            self.metrics["outcome"] = {"generation_unavailable": "generation_failed"}.get(code, code)
        return [sse_event("error", {"code": code, "message": message, "after_text": bool(self.shown)}), self.done()]


async def _answer_events(turn, trace: AnswerTrace, metrics: dict, started: float, remember=None, new_turn_id=None, lich=None):
    """Chuỗi sự kiện SSE của một lượt: đổi sự kiện của lõi (`answer_turn_stream`) ra `status … delta … sources | error [notice] … done`
    (spec streaming §4.1, §4.4). Tự bắt mọi `Exception` rồi phát `error` + `done`. Người dùng ngắt ⇒ không gửi gì thêm, raise lại.
    `finally`: đóng lõi **trong vùng che** (lõi ghi `llm_calls`, tự huỷ + đọc nốt có hạn giờ) rồi mới ghi dòng log — chỉ có `await` được che
    trước dòng log, nên ý spec streaming §4.5 (anyio không huỷ mất dòng log) giữ nguyên (C132 m-1)."""
    metrics["status_code"] = 200
    stream = StreamEvents(metrics, started, new_turn_id, lich)
    try:
        async for kind, data in turn:
            yield stream.status(data) if kind == "status" else stream.delta(data)
        for event in (stream.fixed(trace) if trace.fixed_outcome is not None else stream.finish(trace)):
            yield event
    except (asyncio.CancelledError, GeneratorExit):
        # Ngắt khi đang chờ model ⇒ CancelledError; ngắt đúng lúc đang đứng ở `yield` ⇒ Starlette bỏ dở, generator bị đóng ⇒ GeneratorExit.
        metrics["outcome"] = "client_disconnected"  # token để None: lần hủy không có usage (spec §4.5)
        raise
    except Exception as exc:
        for event in stream.failure(exc):
            yield event
    finally:
        metrics["total_ms"] = elapsed_ms(started)  # như B0: thời gian người dùng thấy, chưa tính đọc nốt
        try:
            with anyio.CancelScope(shield=True):  # vùng che: anyio không huỷ lại lần chờ này khi người dùng ngắt (B105)
                await turn.aclose()  # lõi dừng ở `yield` (ngắt lúc gửi) ⇒ `finally` của lõi ghi `llm_calls`, huỷ lần gọi model + đọc nốt
        finally:
            _copy_trace_metrics(trace, metrics)  # sau `aclose` để có `llm_calls` lõi vừa ghi (C132 m-1)
            logger.info("chat_metrics %s", json.dumps(metrics))
            if remember is not None:  # B3: ghi lượt vào cuộc trò chuyện (chỉ outcome đã xong — `_remember` lọc)
                remember()
