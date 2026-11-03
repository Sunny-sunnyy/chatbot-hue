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
from fastapi import APIRouter, Request
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
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream, elapsed_ms, turn_usd

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


class SourceResponse(BaseModel):
    id: int
    title: str
    heading_path: list[str]
    excerpts: list[str]


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    notice: str | None = None  # B1 H4c: dòng "có thể đã thay đổi" (D8)


def error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


@router.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, request: Request):
    """Điểm ghi số đo duy nhất: mọi nhánh của `_answer`, kể cả exception đi tới handler 500 chung (`api/app.py`), đều có đúng một dòng log.
    Phần suy `outcome` chỉ đọc giá trị kiểu thường; log không được đổi phản hồi."""
    started = time.perf_counter()
    metrics = dict.fromkeys(METRIC_FIELDS)
    try:
        response = await _answer(body, request, metrics)
        _set_outcome(response, metrics)
        return response
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
    query = body.query.strip()
    if not query:
        return error_response(422, "invalid_request", "Yêu cầu không hợp lệ.")

    state = request.app.state
    recorder = get_current_recorder()
    not_ready = _retrieval_not_ready(state, recorder)
    if not_ready is not None:
        return not_ready

    trace = AnswerTrace()
    try:
        await answer_turn(query, state.retrieval_service, state.context_builder, _ready_generator(state), trace, _flags(state), recorder)
    except (RetrievalDependencyError, ContextBudgetError, GeneratorNotReadyError, GenerationError) as exc:
        return _error_response_for(exc, recorder, metrics)
    finally:
        _copy_trace_metrics(trace, metrics)  # cả khi lỗi: bước nào đã chạy thì có số đo của bước đó

    if trace.fixed_outcome is not None:
        metrics["outcome"] = trace.fixed_outcome  # câu cố định / từ chối trước model: không qua kiểm citation
        return ChatResponse(answer=trace.answer, sources=[])

    if trace.citation_error is not None:
        logger.error("Citation integrity failed")
        if recorder:
            recorder.record_error("citation_integrity_failed")
        return error_response(
            500,
            "citation_integrity_error",
            "Câu trả lời không đáp ứng yêu cầu trích dẫn.",
        )

    if recorder:
        recorder.mark_success()

    return ChatResponse(answer=normalize_citations(trace.answer), sources=_source_responses(trace.cited), notice=trace.notice)


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
        route_error=trace.route_error, emergency_by=trace.emergency_by,
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
        turn = answer_turn_stream(query, state.retrieval_service, state.context_builder, generator, trace, _flags(state), recorder)
        response = StreamingResponse(
            _answer_events(turn, trace, metrics, started),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
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

    def __init__(self, metrics: dict, started: float) -> None:
        self.metrics = metrics
        self.started = started
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

    def done(self) -> bytes:
        return sse_event("done", {"outcome": self.metrics["outcome"]})

    def fixed(self, trace: AnswerTrace) -> list[bytes]:
        """Câu cố định (khẩn cấp, ngoài phạm vi, từ chối khi ngữ cảnh không có nguồn) — chữ đã ra một `delta`; không kiểm citation."""
        self.metrics["outcome"] = trace.fixed_outcome
        self.metrics["refusal"] = trace.answer.strip() in REFUSAL_ANSWERS
        self.metrics["delta_matches_final"] = "".join(self.shown).strip() == trace.answer.strip()
        return [sse_event("sources", []), self.done()]

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
        return events + [self.done()]

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


async def _answer_events(turn, trace: AnswerTrace, metrics: dict, started: float):
    """Chuỗi sự kiện SSE của một lượt: đổi sự kiện của lõi (`answer_turn_stream`) ra `status … delta … sources | error [notice] … done`
    (spec streaming §4.1, §4.4). Tự bắt mọi `Exception` rồi phát `error` + `done`. Người dùng ngắt ⇒ không gửi gì thêm, raise lại.
    `finally`: đóng lõi **trong vùng che** (lõi ghi `llm_calls`, tự huỷ + đọc nốt có hạn giờ) rồi mới ghi dòng log — chỉ có `await` được che
    trước dòng log, nên ý spec streaming §4.5 (anyio không huỷ mất dòng log) giữ nguyên (C132 m-1)."""
    metrics["status_code"] = 200
    stream = StreamEvents(metrics, started)
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
