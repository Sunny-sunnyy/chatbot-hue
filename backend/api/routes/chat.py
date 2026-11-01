"""Single-turn full-corpus retrieval, context building, grounded answer generation and citations."""
import json
import logging
import time

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from core.schema import (
    ContextBudgetError,
    GenerationError,
    GeneratorNotReadyError,
    RetrievalDependencyError,
)
from llm.citations import normalize_citations
from llm.evidence_recorder import get_current_recorder
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.grounded_answer import AnswerTrace, answer_query, elapsed_ms

logger = logging.getLogger("chat")
router = APIRouter()

# Một dòng `chat_metrics` mỗi lần gọi (plan C59): chỉ số đếm, mã cố định và thời gian — KHÔNG ghi câu hỏi, câu trả lời, nội dung nguồn,
# chunk_id, response_id hay thông điệp lỗi. Test khóa đúng tập trường này (thêm trường phải sửa danh sách có chủ đích).
METRIC_FIELDS = (
    "outcome", "status_code", "refusal", "model", "input_tokens", "output_tokens", "reasoning_tokens",
    "n_context_sources", "n_cited_sources", "search_ms", "dense_ms", "context_ms", "generation_ms", "citation_ms", "total_ms",
)


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
        metrics["total_ms"] = elapsed_ms(started)
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

    trace = AnswerTrace()
    generator = state.generator if getattr(state, "generator_ready", False) else None
    try:
        await answer_query(query, state.retrieval_service, state.context_builder, generator, trace, recorder)
    except RetrievalDependencyError:
        logger.error("Retrieval dependency error")
        if recorder:
            recorder.record_error("retrieval_unavailable")
        return error_response(
            503,
            "retrieval_unavailable",
            "Hệ thống tra cứu tạm thời không khả dụng.",
        )
    except ContextBudgetError:
        if recorder:
            recorder.record_error("context_budget_error")
        return error_response(
            500,
            "context_budget_error",
            "Không thể đóng gói ngữ cảnh trong giới hạn cho phép.",
        )
    except GeneratorNotReadyError:
        if recorder:
            recorder.record_error("generation_unavailable")
        return error_response(
            502,
            "generation_unavailable",
            "Không thể tạo câu trả lời vào lúc này.",
        )
    except GenerationError:
        metrics["outcome"] = "generation_failed"  # cùng mã 502 với "chưa sẵn sàng", nhưng đã gọi model rồi lỗi
        logger.error("Answer generation failed")
        if recorder:
            recorder.record_error("generation_failed")
        return error_response(
            502,
            "generation_unavailable",
            "Không thể tạo câu trả lời vào lúc này.",
        )
    finally:
        _copy_trace_metrics(trace, metrics)  # cả khi lỗi: bước nào đã chạy thì có số đo của bước đó

    if trace.generated is None:
        metrics["outcome"] = "refusal_no_sources"  # từ chối trước khi gọi model
        return ChatResponse(answer=INSUFFICIENT_ANSWER, sources=[])

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

    answer = normalize_citations(trace.answer)
    sources = [
        SourceResponse(
            id=source.id,
            title=source.title,
            heading_path=list(source.heading_path),
            excerpts=list(source.excerpts),
        )
        for source in trace.cited
    ]
    return ChatResponse(answer=answer, sources=sources)


def _copy_trace_metrics(trace: AnswerTrace, metrics: dict) -> None:
    metrics.update(
        search_ms=trace.search_ms, dense_ms=trace.dense_ms, context_ms=trace.context_ms,
        n_context_sources=None if trace.packed is None else len(trace.packed.sources),
        generation_ms=trace.generation_ms, citation_ms=trace.citation_ms,
        n_cited_sources=None if trace.cited is None else len(trace.cited),
    )
    if trace.generated is not None:
        # getattr như EvidenceRecorder: route chỉ đòi `generated.text`; thiếu trường usage thì log None, không đổi phản hồi (B68 m-4)
        metrics.update({field: getattr(trace.generated, field, None) for field in ("model", "input_tokens", "output_tokens", "reasoning_tokens")})
