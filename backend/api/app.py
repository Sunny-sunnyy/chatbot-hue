"""FastAPI application factory for Phase 6 Full-Corpus RAG API."""
from contextlib import asynccontextmanager
import logging
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = Path(__file__).resolve().parents[1]
for _p in (str(REPO_ROOT), str(BACKEND_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from api.health import router as health_router
from api.routes.chat import router as chat_router
from core.logging_setup import setup_logging
from core.schema import (
    ComponentNotReadyError,
    RetrievalConfigurationError,
    RetrievalDependencyError,
)
from core.settings_loader import load_settings
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from llm.openai_tokenizer import load_openai_tokenizer
from retrieval.full_corpus import build_full_corpus_retrieval_service
from retrieval.full_corpus_context import FullCorpusContextBuilder

logger = logging.getLogger("api")
FRONTEND_DIR = REPO_ROOT / "frontend"


def create_app(settings=None):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        nonlocal settings
        if settings is None:
            settings = load_settings(validate_private_paths=False)

        setup_logging()
        logger.info("Starting Hue Full-Corpus RAG API")

        app.state.retrieval_ready = False
        app.state.retrieval_service = None
        app.state.retrieval_error_status = 503
        app.state.retrieval_error_code = "retrieval_unavailable"
        app.state.retrieval_error_message = "Hệ thống tra cứu tạm thời không khả dụng."

        app.state.tokenizer_ready = False
        app.state.tokenizer = None
        app.state.context_builder = None

        app.state.generator_ready = False
        app.state.generator = None

        # 1. Full-corpus retrieval service
        try:
            runtime = settings["full_corpus_runtime"]
            app.state.retrieval_service = build_full_corpus_retrieval_service(
                candidate_id=runtime["candidate_id"],
                retrieval_treatment=runtime["retrieval_treatment"],
                reranker=runtime["reranker"],
                settings=settings,
            )
            app.state.retrieval_ready = True
            logger.info("Full-corpus retrieval service started successfully")
        except (ComponentNotReadyError, RetrievalConfigurationError):
            logger.error("Retrieval configuration or snapshot error during startup")
            app.state.retrieval_error_status = 409
            app.state.retrieval_error_code = "corpus_reingest_required"
            app.state.retrieval_error_message = (
                "Dữ liệu tra cứu cần được lập chỉ mục lại."
            )
        except RetrievalDependencyError:
            logger.error("Retrieval dependency error during startup")
            app.state.retrieval_error_status = 503
            app.state.retrieval_error_code = "retrieval_unavailable"
            app.state.retrieval_error_message = (
                "Hệ thống tra cứu tạm thời không khả dụng."
            )
        except Exception:
            logger.error("Unexpected retrieval startup failure")
            app.state.retrieval_error_status = 503
            app.state.retrieval_error_code = "retrieval_unavailable"
            app.state.retrieval_error_message = (
                "Hệ thống tra cứu tạm thời không khả dụng."
            )

        # 2. Tokenizer and Context Builder
        try:
            tokenizer = load_openai_tokenizer()
            generation = settings["full_corpus_generation"]
            context_builder = FullCorpusContextBuilder(
                tokenizer,
                context_limit=generation["context_limit"],
                reserved_output_tokens=generation["reserved_output_tokens"],
                safety_margin=generation["safety_margin"],
                max_documents=generation["max_context_documents"],
            )
            app.state.tokenizer = tokenizer
            app.state.context_builder = context_builder
            app.state.tokenizer_ready = True
            logger.info("OpenAI tokenizer and context builder initialized successfully")
        except Exception:
            logger.error("Tokenizer or context builder startup failed")

        # 3. Generator
        try:
            generator = OpenAIFullCorpusGenerator.from_environment(settings)
            app.state.generator = generator
            app.state.generator_ready = True
            logger.info("OpenAI full-corpus generator initialized successfully")
        except Exception:
            logger.error("Generator startup failed")

        try:
            yield
        finally:
            logger.info("Stopping Hue Full-Corpus RAG API")
            if getattr(app.state, "retrieval_service", None) is not None:
                try:
                    app.state.retrieval_service.close()
                except Exception:
                    logger.warning("Error closing retrieval service during shutdown")
            if getattr(app.state, "generator", None) is not None:
                try:
                    await app.state.generator.aclose()
                except Exception:
                    logger.warning("Error closing generator during shutdown")

    app = FastAPI(title="Hue Full-Corpus RAG API", lifespan=lifespan)
    app.state.retrieval_ready = False
    app.state.retrieval_service = None
    app.state.tokenizer_ready = False
    app.state.tokenizer = None
    app.state.context_builder = None
    app.state.generator_ready = False
    app.state.generator = None

    app.include_router(health_router)
    app.include_router(chat_router)

    if FRONTEND_DIR.is_dir():
        app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

        @app.get("/", include_in_schema=False)
        async def frontend_index():
            return FileResponse(FRONTEND_DIR / "index.html")

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, error: RequestValidationError):
        logger.warning(f"Invalid API request: {request.url.path}")
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "invalid_request",
                    "message": "Yêu cầu không hợp lệ.",
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, error: Exception):
        logger.error(f"Unexpected request failure on {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "Đã xảy ra lỗi trong hệ thống. Vui lòng thử lại sau.",
                }
            },
        )

    return app


app = create_app()
