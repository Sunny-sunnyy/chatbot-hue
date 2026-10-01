"""Single-turn full-corpus retrieval, context building, grounded answer generation and citations."""
import asyncio
import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from core.schema import (
    CitationIntegrityError,
    ComponentNotReadyError,
    ContextBudgetError,
    GenerationError,
    RetrievalDependencyError,
)
from llm.citations import select_cited_sources
from llm.evidence_recorder import get_current_recorder
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER

logger = logging.getLogger("chat")
router = APIRouter()


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
        result = await asyncio.to_thread(state.retrieval_service.search, query)
    except (ComponentNotReadyError,):
        logger.error("Corpus reingest required")
        if recorder:
            recorder.record_error("corpus_reingest_required")
        return error_response(
            409,
            "corpus_reingest_required",
            "Dữ liệu tra cứu cần được lập chỉ mục lại.",
        )
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
        packed = state.context_builder.build(query, result.documents)
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
        return ChatResponse(answer=INSUFFICIENT_ANSWER, sources=[])

    if not getattr(state, "generator_ready", False):
        if recorder:
            recorder.record_error("generation_unavailable")
        return error_response(
            502,
            "generation_unavailable",
            "Không thể tạo câu trả lời vào lúc này.",
        )

    try:
        generated = await state.generator.generate_answer(query, packed.text)
    except GenerationError:
        logger.error("Answer generation failed")
        if recorder:
            recorder.record_error("generation_failed")
        return error_response(
            502,
            "generation_unavailable",
            "Không thể tạo câu trả lời vào lúc này.",
        )

    if recorder:
        recorder.record_generation_result(generated)

    try:
        cited = select_cited_sources(generated.text, packed.sources)
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
    return ChatResponse(answer=generated.text, sources=sources)
