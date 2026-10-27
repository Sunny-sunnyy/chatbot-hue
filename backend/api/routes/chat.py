"""Single-turn full-corpus retrieval, context building, grounded answer generation and citations."""
import asyncio
import json
import logging
import time

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from core.schema import (
    CitationIntegrityError,
    ContextBudgetError,
    GenerationError,
    RetrievalDependencyError,
)
from llm.citations import normalize_citations, select_cited_sources
from llm.evidence_recorder import get_current_recorder
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER

logger = logging.getLogger("chat")
router = APIRouter()

# Một dòng `chat_metrics` mỗi lần gọi (plan C59): chỉ số đếm, mã cố định và thời gian — KHÔNG ghi câu hỏi, câu trả lời, nội dung nguồn,
# chunk_id, response_id hay thông điệp lỗi. Test khóa đúng tập trường này (thêm trường phải sửa danh sách có chủ đích).
METRIC_FIELDS = (
    "outcome", "status_code", "refusal", "model", "input_tokens", "output_tokens", "reasoning_tokens",
    "n_context_sources", "n_cited_sources", "search_ms", "dense_ms", "context_ms", "generation_ms", "citation_ms", "total_ms",
)


def _elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 1)


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
        if isinstance(response, JSONResponse):  # mọi lỗi của route đều qua error_response(...)
            metrics["status_code"] = response.status_code
            if metrics["outcome"] is None:
                metrics["outcome"] = json.loads(response.body)["error"]["code"]
        else:
            metrics["status_code"] = 200
            metrics["refusal"] = response.answer.strip() == INSUFFICIENT_ANSWER
            if metrics["outcome"] is None:
                metrics["outcome"] = "success"
        return response
    except Exception:
        metrics["outcome"], metrics["status_code"] = "internal_error", 500
        raise
    finally:
        metrics["total_ms"] = _elapsed_ms(started)
        logger.info("chat_metrics %s", json.dumps(metrics))


async def _answer(body: ChatRequest, request: Request, metrics: dict):
    query = body.query.strip()
    if not query:
        return error_response(422, "invalid_request", "Yêu cầu không hợp lệ.")

    state = request.app.state
    recorder = get_current_recorder()

    if not getattr(state, "retrieval_ready", False):
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

    try:
        started = time.perf_counter()
        result = await asyncio.to_thread(state.retrieval_service.search, query)
        metrics["search_ms"] = _elapsed_ms(started)
        metrics["dense_ms"] = result.trace.timings_ms.get("dense_ms")
    except (RetrievalDependencyError,):
        logger.error("Retrieval dependency error")
        if recorder:
            recorder.record_error("retrieval_unavailable")
        return error_response(
            503,
            "retrieval_unavailable",
            "Hệ thống tra cứu tạm thời không khả dụng.",
        )

    try:
        started = time.perf_counter()
        packed = state.context_builder.build(query, result.documents)
        metrics["context_ms"] = _elapsed_ms(started)
        metrics["n_context_sources"] = len(packed.sources)
    except ContextBudgetError:
        if recorder:
            recorder.record_error("context_budget_error")
        return error_response(
            500,
            "context_budget_error",
            "Không thể đóng gói ngữ cảnh trong giới hạn cho phép.",
        )

    if recorder:
        recorder.record_packed_context(packed)

    if not packed.sources:
        if recorder:
            recorder.record_fallback()
        metrics["outcome"] = "refusal_no_sources"  # từ chối trước khi gọi model
        return ChatResponse(answer=INSUFFICIENT_ANSWER, sources=[])

    if not getattr(state, "generator_ready", False):
        if recorder:
            recorder.record_error("generation_unavailable")
        return error_response(
            502,
            "generation_unavailable",
            "Không thể tạo câu trả lời vào lúc này.",
        )

    started = time.perf_counter()
    try:
        generated = await state.generator.generate_answer(query, packed.text)
    except GenerationError:
        metrics["generation_ms"] = _elapsed_ms(started)
        metrics["outcome"] = "generation_failed"  # cùng mã 502 với "chưa sẵn sàng", nhưng đã gọi model rồi lỗi
        logger.error("Answer generation failed")
        if recorder:
            recorder.record_error("generation_failed")
        return error_response(
            502,
            "generation_unavailable",
            "Không thể tạo câu trả lời vào lúc này.",
        )

    metrics["generation_ms"] = _elapsed_ms(started)
    # getattr như EvidenceRecorder: route chỉ đòi `generated.text`; thiếu trường usage thì log None, không đổi phản hồi (B68 m-4)
    metrics.update({field: getattr(generated, field, None) for field in ("model", "input_tokens", "output_tokens", "reasoning_tokens")})
    if recorder:
        recorder.record_generation_result(generated)

    started = time.perf_counter()
    answer = normalize_citations(generated.text)
    try:
        cited = select_cited_sources(answer, packed.sources)
        metrics["citation_ms"] = _elapsed_ms(started)
        metrics["n_cited_sources"] = len(cited)
    except CitationIntegrityError:
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

    sources = [
        SourceResponse(
            id=source.id,
            title=source.title,
            heading_path=list(source.heading_path),
            excerpts=list(source.excerpts),
        )
        for source in cited
    ]
    return ChatResponse(answer=answer, sources=sources)
