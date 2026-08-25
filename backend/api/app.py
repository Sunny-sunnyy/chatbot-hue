"""FastAPI application factory; importing this module has no side effects.

Lifespan builds the real runtime once (retrieval stack, context builder and
generator) and stores components plus cached readiness in app.state. A
missing Qdrant/retrieval/generator keeps the app alive in a degraded state.
There is no component injection: every app uses the real dependencies.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.health import router as health_router
from api.routes.chat import router as chat_router
from core.logging_setup import setup_logging
from core.settings_loader import load_settings
from core.startup import build_retrieval_service
from llm.generator_openai import OpenAIAnswerGenerator
from retrieval.context_builder import ContextBuilder

logger = logging.getLogger(__name__)


def _runtime_info(retrieval_service, settings):
    """Immutable startup status fields exposed through retrieval_debug."""
    status = (
        retrieval_service.status if retrieval_service is not None else None
    )
    return {
        "profile": status.active_profile if status else None,
        "embedding_model": status.embedding_model if status else None,
        "reranker_model": (
            settings["reranking"]["model"]
            if status is not None and status.reranker_ready
            else None
        ),
    }


def create_app(settings=None):
    """Create the FastAPI app; the lifespan always builds real components."""
    if settings is None:
        settings = load_settings()

    @asynccontextmanager
    async def lifespan(app):
        setup_logging()
        retrieval_service = None
        retrieval_ready = False
        try:
            retrieval_service = build_retrieval_service(settings)
            retrieval_ready = True
        except Exception as exc:  # any retrieval dependency/config failure
            logger.warning(
                "retrieval stack unavailable at startup: %s",
                type(exc).__name__,
            )
        llm_cfg = settings["llm"]
        gen = OpenAIAnswerGenerator(
            model=llm_cfg["answer_model"],
            temperature=llm_cfg["temperature"],
            max_output_tokens=llm_cfg["max_output_tokens"],
            timeout_seconds=llm_cfg["timeout"],
        )
        builder = ContextBuilder(
            max_documents=settings["retrieval"]["max_context_documents"],
            max_characters=settings["retrieval"]["max_context_characters"],
        )
        app.state.retrieval_ready = retrieval_ready
        app.state.generator_configured = gen.configured
        app.state.retrieval_service = retrieval_service
        app.state.context_builder = builder
        app.state.generator = gen
        app.state.runtime = _runtime_info(retrieval_service, settings)
        yield

    app = FastAPI(title="Hue Foods RAG API", lifespan=lifespan)
    app.state.retrieval_ready = False
    app.state.generator_configured = False
    app.state.retrieval_service = None
    app.state.context_builder = None
    app.state.generator = None
    app.state.runtime = {
        "profile": None,
        "embedding_model": None,
        "reranker_model": None,
    }
    app.include_router(health_router)
    app.include_router(chat_router)

    @app.exception_handler(RequestValidationError)
    async def _validation_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "detail": {
                    "code": "invalid_request",
                    "message": "Yêu cầu không hợp lệ.",
                }
            },
        )

    @app.exception_handler(Exception)
    async def _unhandled_handler(request: Request, exc: Exception):
        logger.exception("unhandled request failure")
        return JSONResponse(
            status_code=500,
            content={
                "detail": {
                    "code": "internal_error",
                    "message": "Lỗi nội bộ không mong đợi.",
                }
            },
        )

    return app


app = create_app()
