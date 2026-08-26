"""FastAPI application factory with cached component readiness."""
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

logger = logging.getLogger("api")


def create_app(settings=None):
    if settings is None:
        settings = load_settings()

    @asynccontextmanager
    async def lifespan(app):
        setup_logging()
        logger.info("Starting Hue Foods RAG API")

        retrieval_service = None
        retrieval_ready = False
        try:
            retrieval_service = build_retrieval_service(settings)
            retrieval_ready = True
            logger.info("Retrieval service started successfully")
        except Exception as error:
            logger.error(f"Retrieval startup failed: {error}")

        llm = settings["llm"]
        generator = OpenAIAnswerGenerator(
            model=llm["answer_model"],
            temperature=llm["temperature"],
            max_output_tokens=llm["max_output_tokens"],
            timeout_seconds=llm["timeout"],
        )
        context_builder = ContextBuilder(
            max_documents=settings["retrieval"]["max_context_documents"],
            max_characters=settings["retrieval"]["max_context_characters"],
        )

        app.state.retrieval_ready = retrieval_ready
        app.state.generator_configured = generator.configured
        app.state.retrieval_service = retrieval_service
        app.state.context_builder = context_builder
        app.state.generator = generator
        logger.info(
            f"Answer generator configured: {generator.configured}; "
            f"model={generator.model}"
        )
        yield
        logger.info("Stopping Hue Foods RAG API")

    app = FastAPI(title="Hue Foods RAG API", lifespan=lifespan)
    app.state.retrieval_ready = False
    app.state.generator_configured = False
    app.state.retrieval_service = None
    app.state.context_builder = None
    app.state.generator = None
    app.include_router(health_router)
    app.include_router(chat_router)

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, error: RequestValidationError):
        logger.warning(f"Invalid API request: {request.url.path}")
        return JSONResponse(
            status_code=422,
            content={"detail": "Yêu cầu không hợp lệ."},
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, error: Exception):
        logger.exception(
            f"Unexpected request failure on {request.url.path}: {error}"
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Đã xảy ra lỗi trong hệ thống. Vui lòng thử lại sau."
            },
        )

    return app


app = create_app()
