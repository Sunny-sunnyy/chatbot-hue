"""Chat endpoint: deterministic retrieval -> context -> grounded generation."""
import asyncio
import logging
import uuid

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from core.schema import (
    ComponentNotReadyError,
    GeneratorNotConfiguredError,
    GeneratorTimeoutError,
    GeneratorUnavailableError,
    InvalidGeneratorOutputError,
    RetrievalDependencyError,
)

logger = logging.getLogger("chat")
router = APIRouter()

MAX_QUERY_CHARS = 500
MAX_SESSION_ID_CHARS = 128

INSUFFICIENT_ANSWER = (
    "Tôi chưa đủ thông tin từ nguồn dữ liệu hiện có để trả lời câu hỏi này."
)


class ChatRequest(BaseModel):
    """MVP chat request; session_id is an opaque client value."""

    query: str
    session_id: str | None = None


def _fail(status_code, code, message):
    raise HTTPException(
        status_code=status_code, detail={"code": code, "message": message}
    )


def _validate(body):
    """Normalize and validate the request; raises HTTP 422 on violation."""
    query = body.query.strip()
    if not query or len(query) > MAX_QUERY_CHARS:
        _fail(
            422,
            "invalid_query",
            "Câu hỏi không hợp lệ: phải có từ 1 đến 500 ký tự.",
        )
    session_id = body.session_id
    if session_id is None:
        session_id = str(uuid.uuid4())
    else:
        session_id = session_id.strip()
        if not session_id or len(session_id) > MAX_SESSION_ID_CHARS:
            _fail(422, "invalid_session_id", "session_id không hợp lệ.")
    return query, session_id


def _success(answer, sources, session_id, debug):
    return {
        "answer": answer,
        "sources": sources,
        "session_id": session_id,
        "retrieval_debug": debug,
    }


def _retrieval_debug(state, documents, sources):
    """Safe debug fields from the immutable startup snapshot."""
    runtime = state.runtime
    debug = {
        "profile": runtime["profile"],
        "embedding_model": runtime["embedding_model"],
        "retrieved_count": len(documents),
        "context_source_count": len(sources),
    }
    if runtime["reranker_model"] is not None:
        debug["reranker_model"] = runtime["reranker_model"]
    return debug


def _source_items(sources, used_ids, documents):
    """Project sources in context order, deduplicated, with their scores."""
    scores = {document.id: document.score for document in documents}
    used = set(used_ids)
    items = []
    for source in sources:
        chunk_id = source["chunk_id"]
        if chunk_id not in used:
            continue
        items.append(
            {
                "chunk_id": chunk_id,
                "source": source["source"],
                "title": source["title"],
                "section": source["section"],
                "score": scores.get(chunk_id),
            }
        )
    return items


def _dedup_in_order(context_ids, used_ids):
    """Keep only used IDs, in context evidence order, without duplicates."""
    seen = set()
    ordered = []
    for sid in context_ids:
        if sid in used_ids and sid not in seen:
            seen.add(sid)
            ordered.append(sid)
    return ordered


@router.post("/api/chat")
async def chat(body: ChatRequest, request: Request):
    """Answer one query; never stores session history."""
    state = request.app.state
    query, session_id = _validate(body)
    if not state.retrieval_ready:
        _fail(503, "retrieval_not_ready", "Hệ thống truy xuất chưa sẵn sàng.")
    try:
        # Retrieval is sync and blocking; keep it off the event loop.
        documents = await asyncio.to_thread(state.retrieval_service.search, query)
    except ComponentNotReadyError:
        _fail(503, "retrieval_not_ready", "Hệ thống truy xuất chưa sẵn sàng.")
    except RetrievalDependencyError:
        _fail(
            503,
            "retrieval_unavailable",
            "Hệ thống truy xuất tạm thời không khả dụng.",
        )
    context_result = state.context_builder.build(documents)
    debug = _retrieval_debug(state, documents, context_result.sources)
    if not context_result.sources:
        # No evidence: skip the model entirely and answer safe.
        return _success(INSUFFICIENT_ANSWER, [], session_id, debug)
    if not state.generator_configured:
        _fail(
            503,
            "generator_not_configured",
            "Bộ sinh câu trả lời chưa được cấu hình.",
        )
    available_ids = [source["chunk_id"] for source in context_result.sources]
    try:
        generated = await state.generator.generate_answer(
            query, context_result.context, available_ids
        )
    except GeneratorNotConfiguredError:
        _fail(
            503,
            "generator_not_configured",
            "Bộ sinh câu trả lời chưa được cấu hình.",
        )
    except GeneratorTimeoutError:
        _fail(504, "generator_timeout", "Bộ sinh câu trả lời hết thời gian.")
    except InvalidGeneratorOutputError:
        _fail(
            502,
            "invalid_generator_output",
            "Đầu ra của bộ sinh câu trả lời không hợp lệ.",
        )
    except GeneratorUnavailableError:
        _fail(
            502,
            "generator_unavailable",
            "Bộ sinh câu trả lời tạm thời không khả dụng.",
        )
    except Exception:  # unexpected generator failure
        logger.exception("unexpected generator failure")
        _fail(500, "internal_error", "Lỗi nội bộ không mong đợi.")
    if not generated.used_source_ids:
        # Model cited nothing: discard its answer and return a safe refusal.
        return _success(INSUFFICIENT_ANSWER, [], session_id, debug)
    used_ids = _dedup_in_order(available_ids, set(generated.used_source_ids))
    sources = _source_items(context_result.sources, used_ids, documents)
    return _success(generated.answer, sources, session_id, debug)
