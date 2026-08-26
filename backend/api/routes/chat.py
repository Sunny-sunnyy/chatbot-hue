"""Single-turn retrieval, context building and grounded answer generation."""
import asyncio
import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from core.schema import (
    ComponentNotReadyError,
    GenerationError,
    RetrievalDependencyError,
)
from llm.prompt import INSUFFICIENT_ANSWER

logger = logging.getLogger("chat")
router = APIRouter()

INVALID_REQUEST = "Yêu cầu không hợp lệ."
SERVICE_UNAVAILABLE = (
    "Hệ thống tạm thời không khả dụng. Vui lòng thử lại sau."
)


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)


class ChatResponse(BaseModel):
    answer: str


@router.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, request: Request):
    query = body.query.strip()
    if not query:
        logger.warning("Received an empty question")
        raise HTTPException(status_code=422, detail=INVALID_REQUEST)

    logger.info(f"Received question: {query}")
    state = request.app.state
    if not state.retrieval_ready:
        logger.warning("Retrieval service is not ready")
        raise HTTPException(status_code=503, detail=SERVICE_UNAVAILABLE)

    logger.info("Running retrieval")
    try:
        documents = await asyncio.to_thread(
            state.retrieval_service.search,
            query,
        )
    except (ComponentNotReadyError, RetrievalDependencyError) as error:
        logger.error(f"Retrieval failed: {error}")
        raise HTTPException(
            status_code=503,
            detail=SERVICE_UNAVAILABLE,
        ) from error
    logger.info(f"Retrieved {len(documents)} documents")

    context = state.context_builder.build(documents)
    if not context:
        logger.warning("No relevant context found")
        return ChatResponse(answer=INSUFFICIENT_ANSWER)

    if not state.generator_configured:
        logger.error("Answer generator is not configured")
        raise HTTPException(status_code=503, detail=SERVICE_UNAVAILABLE)

    try:
        answer = await state.generator.generate_answer(query, context)
    except GenerationError as error:
        logger.error(f"Answer generation failed: {error}")
        raise HTTPException(
            status_code=503,
            detail=SERVICE_UNAVAILABLE,
        ) from error

    logger.info("Chat request completed successfully")
    return ChatResponse(answer=answer)
