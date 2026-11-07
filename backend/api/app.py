"""FastAPI application factory for Phase 6 Full-Corpus RAG API."""
from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

from api.conversations import ConversationStore
from api.feedback import FeedbackTurns
from api.feedback import router as feedback_router
from api.health import router as health_router
from api.routes.anh import router as anh_router
from api.routes.chat import router as chat_router
from api.routes.cong import nap_kham_pha
from api.routes.cong import router as cong_router
from core.logging_setup import setup_logging
from core.schema import (
    ComponentNotReadyError,
    RetrievalConfigurationError,
    RetrievalDependencyError,
)
from core.settings_loader import BACKEND_DIR, load_settings
from ingestion.source_state import discover_full_corpus_files
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from llm.assistant import AssistantFlags
from llm.nhan_anh import nap_danh_sach, tao_agent
from llm.tra_web import SERPER_API_KEY_ENV, tim_web
from llm.openai_tokenizer import load_openai_tokenizer
from retrieval.full_corpus import build_full_corpus_retrieval_service
from retrieval.full_corpus_context import FullCorpusContextBuilder

logger = logging.getLogger("api")
REPO_ROOT = Path(__file__).resolve().parents[2]

# Bản build của giao diện React (`cd frontend && npm ci && npm run build`); không commit. Thiếu ⇒ API vẫn chạy, chỉ không có trang web.
FRONTEND_DIR = REPO_ROOT / "frontend" / "dist"


# Trang chỉ nạp script / CSS từ chính server (`/static/…`, không script nội dòng, bản build không dùng `eval`) ⇒ chặn mọi tải từ máy khác,
# kể cả khi chữ Markdown do model viết lọt qua DOMPurify (rà bảo mật C106 R2, S3 streaming).
# Phase 10 (spec A7, User duyệt 05/11): `img-src` thêm `blob:` — chỉ để xem trước ảnh người dùng vừa chọn (URL do chính trang tạo, không mở mạng).
FRONTEND_CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' blob:; connect-src 'self'; "
                "object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")


class FrontendStaticFiles(StaticFiles):
    """`/static/…` như `StaticFiles`, nhưng trang HTML (vd `/static/index.html` — cùng app chạy được ở đó) cũng mang CSP như `/` (review C107 M-1).
    Không dùng middleware HTTP chung: middleware kiểu `BaseHTTPMiddleware` bọc cả luồng SSE của `/api/chat/stream`."""

    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        if response.media_type == "text/html":
            response.headers["Content-Security-Policy"] = FRONTEND_CSP
        return response


def _tim_web_server(settings: dict):
    """B6: hàm tra web của server. Khoá đọc **trong** hàm mỗi lần tra (review E13 m-1: `functools.partial(api_key=…)` để lộ khoá trong `repr`)."""
    timeout = float((settings.get("assistant") or {}).get("tra_web_timeout_seconds", 5))

    async def tim(cau: str):
        return await tim_web(cau, api_key=os.getenv(SERPER_API_KEY_ENV, "").strip() or None, timeout=timeout)

    return tim


def create_app(settings=None):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        nonlocal settings
        if settings is None:
            settings = load_settings(validate_private_paths=False)

        setup_logging()
        logger.info("Starting Hue Full-Corpus RAG API")
        app.state.assistant_flags = AssistantFlags.from_settings(settings)  # Phase 9 B1 D9
        # B6 D3: hàm tra web của server — khoá Serper chỉ ở server; thiếu khoá ⇒ mỗi lần tra ra "loi", không mở mạng. Cờ tắt ⇒ None.
        app.state.tim_web = _tim_web_server(settings) if app.state.assistant_flags.tra_web else None

        app.state.retrieval_ready = False
        app.state.retrieval_service = None
        app.state.kham_pha = None
        app.state.retrieval_error_status = 503
        app.state.retrieval_error_code = "retrieval_unavailable"
        app.state.retrieval_error_message = "Hệ thống tra cứu tạm thời không khả dụng."

        app.state.tokenizer_ready = False
        app.state.tokenizer = None
        app.state.context_builder = None
        app.state.conversations = None

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

        # 1b. Cổng đợt 1 D6: bài kho cho trang Khám phá — chỉ khi bước 1 đã kiểm danh sách + hash file khớp build record; lỗi ⇒ route 503
        if app.state.retrieval_ready:
            try:
                app.state.kham_pha = nap_kham_pha(*discover_full_corpus_files(settings))
            except Exception:
                logger.error("Explore list startup failed")

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
            flags = app.state.assistant_flags
            # B3 D1: kho cuộc trò chuyện trong RAM — chỉ khi cờ nhớ bật (tắt ⇒ không cookie, không kho)
            app.state.conversations = ConversationStore(lambda text: len(tokenizer.encode(text)), keep_answers=flags.nho_cau_tra_loi) \
                if flags.nho_hoi_thoai else None
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

        # 4. Hỏi bằng ảnh (Phase 10 A1 D2): cờ tắt / thiếu generator / danh sách lỗi ⇒ `app.state.anh = None` ⇒ route trả 404
        anh = settings.get("anh") or {}
        if anh.get("bat") and app.state.generator is not None:
            try:
                Image.MAX_IMAGE_PIXELS = anh["max_pixels"]  # lớp sau của rào bom giải nén (`nhan_anh.chuan_bi_anh`)
                danh_sach = nap_danh_sach((BACKEND_DIR / anh["danh_sach"]).resolve())
                app.state.anh = {"danh_sach": danh_sach, "agent": tao_agent(app.state.generator, danh_sach), "max_bytes": anh["max_bytes"],
                                 "max_pixels": anh["max_pixels"], "canh_dai": anh["canh_dai"], "timeout": anh["timeout"]}
                logger.info("Image route enabled (%d names)", len(danh_sach))
            except Exception:
                logger.error("Image route startup failed")

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
    app.state.anh = None
    app.state.kham_pha = None

    app.include_router(health_router)
    app.include_router(chat_router)
    app.include_router(anh_router)  # luôn đăng ký: `settings` chỉ có trong lifespan (Phase 10 A1 D2, review C m-1); cờ tắt ⇒ 404
    app.include_router(feedback_router)
    app.include_router(cong_router)  # cổng đợt 1 D6: 4 route chỉ đọc
    app.state.feedback_turns = FeedbackTurns()  # B142: mã lượt cho 👍 / 👎 (RAM, không cần lifespan)

    if not FRONTEND_DIR.is_dir():
        logger.warning("Frontend build not found at frontend/dist — run `npm ci && npm run build` in frontend/")
    else:
        app.mount("/static", FrontendStaticFiles(directory=FRONTEND_DIR), name="static")

        @app.get("/", include_in_schema=False)
        async def frontend_index():
            return FileResponse(FRONTEND_DIR / "index.html", headers={"Content-Security-Policy": FRONTEND_CSP})

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
