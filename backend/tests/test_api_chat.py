"""Real FastAPI lifecycle and strict full-corpus chat contract tests."""
import importlib
import json
import logging
import subprocess
from pathlib import Path
from contextlib import contextmanager
from types import SimpleNamespace

from fastapi.testclient import TestClient

from api.app import create_app
from api.routes.chat import METRIC_FIELDS
from core.logging_setup import LOG_FILE_NAME, LOGS_DIR
from core.settings_loader import load_settings


@contextmanager
def chat_log_records(caplog):
    """Gắn thẳng handler của caplog vào logger `chat`: sau `setup_logging()` (lifespan) logger này có `propagate: no` nên caplog ở root không thấy."""
    chat_logger = logging.getLogger("chat")
    chat_logger.addHandler(caplog.handler)
    try:
        yield caplog.records
    finally:
        chat_logger.removeHandler(caplog.handler)


def metric_lines(records) -> list[dict]:
    return [json.loads(r.getMessage().removeprefix("chat_metrics ")) for r in records
            if r.name == "chat" and r.getMessage().startswith("chat_metrics ")]


def test_import_has_no_external_side_effect():
    module = importlib.import_module("api.app")
    assert module.app.state.retrieval_ready is False
    assert getattr(module.app.state, "generator_ready", False) is False


def test_invalid_requests_use_typed_vietnamese_envelope():
    app = create_app(load_settings())
    for body in (
        {"query": "   "},
        {"query": "x" * 501},
        {"query": []},
        {"query": "Huế", "extra": True},
    ):
        response = TestClient(app).post("/api/chat", json=body)
        assert response.status_code == 422
        assert response.json() == {
            "error": {"code": "invalid_request", "message": "Yêu cầu không hợp lệ."}
        }


def test_health_is_cached_and_ready_after_real_lifespan(require_openai_key):
    app = create_app(load_settings())
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["components"] == {
        "app": "alive",
        "qdrant": "ready",
        "retrieval": "ready",
        "tokenizer": "ready",
        "generator": "ready",
    }


def test_real_first_chunk_budget_error_has_no_partial_answer(caplog):
    settings = load_settings()
    settings["full_corpus_generation"] = dict(settings["full_corpus_generation"])
    settings["full_corpus_generation"]["context_limit"] = 2561
    app = create_app(settings)
    query = "Giá vé Đại Nội?"
    log_file = LOGS_DIR / LOG_FILE_NAME
    with TestClient(app) as client, chat_log_records(caplog) as records:
        moc = len(log_file.read_text(encoding="utf-8", errors="replace").splitlines())  # sau lifespan: file log đã có
        response = client.post("/api/chat", json={"query": query})
        chat_messages = [r.getMessage() for r in records if r.name == "chat"]
        lines = metric_lines(records)
    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "context_budget_error",
            "message": "Không thể đóng gói ngữ cảnh trong giới hạn cho phép.",
        }
    }
    assert "answer" not in response.text
    assert "sources" not in response.text
    # Câu hỏi đã đi qua tìm kiếm + dựng context: log số đo có đúng một dòng, đúng danh sách trắng, không lọt câu hỏi (plan C59 §4).
    assert len(lines) == 1
    assert set(lines[0]) == set(METRIC_FIELDS)
    assert lines[0]["outcome"] == "context_budget_error" and lines[0]["status_code"] == 500
    assert isinstance(lines[0]["search_ms"], float) and isinstance(lines[0]["dense_ms"], float)
    assert lines[0]["dense_ms"] == round(lines[0]["dense_ms"], 1)  # làm tròn 1 chữ số như các trường *_ms (B70 m-2)
    assert lines[0]["input_tokens"] is None and lines[0]["output_tokens"] is None
    assert not any(query in message for message in chat_messages)
    # Dòng thật trong file log (thứ script đếm đọc) mang mã commit của đúng thư mục code đang chạy.
    moi = [line for line in log_file.read_text(encoding="utf-8", errors="replace").splitlines()[moc:] if "chat_metrics " in line]
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=Path(__file__).parent, capture_output=True, text=True).stdout.strip()
    assert len(moi) == 1 and sha
    assert json.loads(moi[0].split("chat_metrics ", 1)[1])["git_sha"] == sha == lines[0]["git_sha"]


def test_git_sha_khong_co_git_thi_khong_chet(monkeypatch):
    from api.routes import chat

    def khong_git(*args, **kwargs):
        raise FileNotFoundError("git")

    monkeypatch.delenv("HUE_GIT_SHA", raising=False)
    monkeypatch.setattr(chat.subprocess, "run", khong_git)
    assert chat._doc_git_sha() == "khong_ro"
    # Ảnh Docker (không git): mã do người build truyền qua biến môi trường; biến rỗng / toàn dấu cách coi như không đặt.
    monkeypatch.setenv("HUE_GIT_SHA", " abc1234\n")
    assert chat._doc_git_sha() == "abc1234"
    monkeypatch.setenv("HUE_GIT_SHA", "  ")
    assert chat._doc_git_sha() == "khong_ro"


def test_git_sha_bien_moi_truong_thang_git(monkeypatch):
    from api.routes import chat

    monkeypatch.setenv("HUE_GIT_SHA", "abc1234")
    assert chat._doc_git_sha() == "abc1234"  # có biến ⇒ không hỏi git (thư mục này có git, mã thật khác "abc1234")
    monkeypatch.delenv("HUE_GIT_SHA")
    assert chat._doc_git_sha() not in ("abc1234", "khong_ro")  # không biến ⇒ đường git như cũ


def test_chat_metrics_logged_when_retrieval_not_ready(caplog):
    app = create_app(load_settings())  # không chạy lifespan ⇒ retrieval chưa sẵn sàng ⇒ 503, không gọi Qdrant / model
    with chat_log_records(caplog) as records:
        response = TestClient(app).post("/api/chat", json={"query": "Huế có gì?"})
        lines = metric_lines(records)
    assert response.status_code == 503
    assert len(lines) == 1
    assert lines[0]["outcome"] == "retrieval_unavailable" and lines[0]["status_code"] == 503


def test_git_sha_co_o_ca_hai_route(caplog):
    from api.routes.chat import GIT_SHA

    app = create_app(load_settings())  # không lifespan ⇒ 503 trước model ở cả hai route, 0 USD
    with chat_log_records(caplog) as records:
        for path in ("/api/chat", "/api/chat/stream"):
            assert TestClient(app).post(path, json={"query": "Huế có gì?"}).status_code == 503
        lines = metric_lines(records)
    assert [line["git_sha"] for line in lines] == [GIT_SHA, GIT_SHA] and GIT_SHA != "khong_ro"


def test_clean_subprocess_import_production_command():
    import subprocess
    import sys
    from pathlib import Path

    backend_dir = Path(__file__).resolve().parents[1]
    cmd = [
        sys.executable,
        "-c",
        "import api.app; print('CLEAN_IMPORT_OK')",
    ]
    # Run with empty PYTHONPATH and cwd=backend_dir
    res = subprocess.run(
        cmd,
        cwd=backend_dir,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "PYTHONPATH": ""},
    )
    assert res.returncode == 0, f"Import failed: {res.stderr}"
    assert "CLEAN_IMPORT_OK" in res.stdout


def test_production_app_state_has_no_last_chat_trace_after_chat():
    settings = load_settings()
    settings["full_corpus_generation"] = dict(settings["full_corpus_generation"])
    settings["full_corpus_generation"]["context_limit"] = 2561
    app = create_app(settings)
    with TestClient(app) as client:
        client.post("/api/chat", json={"query": "Giá vé Đại Nội?"})
    assert not hasattr(app.state, "last_chat_trace")


def test_chat_returns_bracket_citations_when_model_writes_nguon_label():
    """Model viết "[Nguồn 1]" ⇒ 200, answer gửi UI chỉ còn "[1]" (C-09). Retrieval, context thật (Qdrant chỉ đọc);
    generator thay bằng text cố định để kiểm logic của route — không gọi OpenAI, không cần key."""

    class FixedAnswerGenerator:
        async def route(self, query, call_log):  # B1: cờ `router` bật mặc định ⇒ lõi hỏi tuyến trước
            return "tro_ly_hue"

        async def generate_answer(self, query, context_text, **kwargs):  # B1: lõi truyền thêm `call_log` (+ `today`)
            return SimpleNamespace(text="Thông tin giá vé có trong tài liệu [Nguồn 1].")

        assistant_instructions = ""  # B2: `tim_them` bật mặc định ⇒ lõi đi đường trợ lý có công cụ (đếm ngân sách bằng lời dặn này)

        async def generate_with_tools(self, prompt, tool_fn, call_log, **_cong_cu):  # nhận công cụ theo cờ (con_luot_fn…)
            return SimpleNamespace(text="Thông tin giá vé có trong tài liệu [Nguồn 1].")

    app = create_app(load_settings())
    with TestClient(app) as client:
        original = app.state.generator, app.state.generator_ready
        app.state.generator, app.state.generator_ready = FixedAnswerGenerator(), True
        response = client.post("/api/chat", json={"query": "Giá vé Đại Nội?"})
        app.state.generator, app.state.generator_ready = original
    assert response.status_code == 200
    assert response.json()["answer"] == "Thông tin giá vé có trong tài liệu [1]."
    assert [source["id"] for source in response.json()["sources"]] == [1]


def test_model_chon_loai_bao_lu_roi_loi_thi_loi_bao_cua_route_co_cau_112():
    """Soát tích hợp đợt 2 (18/11), đi qua ROUTE thật `/api/chat`: câu gõ không khớp lưới bão / lũ, model gọi công cụ `thoi_tiet(loai="bao_lu")` rồi lỗi
    ⇒ lời báo 502 phải kèm câu bản tin chính thức + 112 (route truyền `trace.thoi_tiet_ctx` cho `loi_bao_luoi_cuoi`). Tìm kho + ngữ cảnh thật (Qdrant chỉ
    đọc); model và dự báo là đồ thay thế — không mạng, không cần khoá. Đối chứng: cùng câu, model lỗi mà CHƯA gọi công cụ ⇒ lời báo nguyên."""
    from dataclasses import replace

    from api.routes.chat import GENERATION_FAILURE_MESSAGE
    from core.schema import GenerationError
    from llm import thoi_tiet as tt

    cau = "Mai đi biển Thuận An thời tiết có nguy hiểm gì không?"
    assert not tt.la_luot_bao_lu(cau, ())

    class ModelLoi:
        assistant_instructions = ""
        goi_bao_lu = True

        async def route(self, query, call_log):
            return "tro_ly_hue"

        async def generate_with_tools(self, prompt, tool_fn, call_log, **cong_cu):
            if self.goi_bao_lu:
                await cong_cu["thoi_tiet_fn"]("bao_lu", 1, 1)
            raise GenerationError("x")

    async def du_bao_loi():
        return tt.DuBao(trang_thai="loi", loi="test")

    app = create_app(load_settings())
    with TestClient(app) as client:
        goc = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        assert goc[2].thoi_tiet and goc[2].bao_lu_cong_cu  # cấu hình đang chạy: hai cờ này bật
        app.state.generator, app.state.generator_ready = ModelLoi(), True
        app.state.assistant_flags = replace(goc[2], du_bao=du_bao_loi)
        co_goi = client.post("/api/chat", json={"query": cau})
        ModelLoi.goi_bao_lu = False
        khong_goi = client.post("/api/chat", json={"query": cau})
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = goc
    assert co_goi.status_code == khong_goi.status_code == 502
    assert co_goi.json()["error"]["message"] == f"{GENERATION_FAILURE_MESSAGE}\n\n{tt.CAU_BAO_LU}"
    assert khong_goi.json()["error"]["message"] == GENERATION_FAILURE_MESSAGE


def test_stream_model_chon_loai_bao_lu_roi_loi_thi_su_kien_error_co_cau_112():
    """Cùng ca với test `/api/chat` ở trên nhưng đi qua ROUTE thật `/api/chat/stream` — chỗ hai cơ chế gặp nhau: ở đường stream có cờ
    `song_song_tra_loi`, phần trả lời chạy trên trace PHỤ; lỗi của nó phải được gộp về trace chính TRƯỚC khi route dựng sự kiện `error`
    (`sua_loi` đọc `trace.thoi_tiet_ctx`). Câu gõ không khớp lưới bão / lũ; model (SDK thật + client kịch bản) gọi `thoi_tiet(loai="bao_lu")`
    rồi lần gọi kế lỗi ⇒ sự kiện `error` phải mang câu bản tin chính thức + 112. Kiểm cả hai nhánh cờ song song. Đối chứng: model lỗi khi
    CHƯA gọi công cụ ⇒ lời báo nguyên. Tìm kho + ngữ cảnh thật (Qdrant chỉ đọc); model và dự báo là đồ thay thế — không mạng, không cần khoá."""
    from dataclasses import replace

    from openai import OpenAIError

    from api.routes.chat import GENERATION_FAILURE_MESSAGE
    from llm import thoi_tiet as tt
    from test_b2_tool_loop import generator
    from test_b5b_thoi_tiet import bao_call
    from test_chat_stream import parse_sse

    cau = "Mai đi biển Thuận An thời tiết có nguy hiểm gì không?"
    assert not tt.la_luot_bao_lu(cau, ())

    def kich_ban(goi_bao_lu: bool):
        lan_tro_ly = []

        def script(n, kw):
            instructions = kw.get("instructions") or ""
            if "tro_ly_hue" in instructions and "ngoai_pham_vi" in instructions:  # lời dặn định tuyến
                return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                         "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
            lan_tro_ly.append(n)
            if goi_bao_lu and len(lan_tro_ly) == 1:
                return [bao_call()]
            raise OpenAIError("x")
        return script

    async def du_bao_loi():
        return tt.DuBao(trang_thai="loi", loi="test")

    def loi_bao(client, app, flags, goi_bao_lu: bool) -> dict:
        app.state.generator, app.state.assistant_flags = generator(kich_ban(goi_bao_lu)), flags
        client.cookies.clear()  # mỗi lượt một cuộc mới: lượt trước không thành "câu liền trước" của lưới
        r = client.post("/api/chat/stream", json={"query": cau})
        assert r.status_code == 200
        events = parse_sse([block.encode() + b"\n\n" for block in r.text.split("\n\n") if block.strip()])
        assert events[-1][0] == "done" and [name for name, _ in events].count("error") == 1
        return dict(events)["error"]

    app = create_app(load_settings())
    with TestClient(app) as client:
        goc = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        app.state.generator_ready = True
        ket_qua = {}
        for song_song in (True, False):  # cờ đặt trong test (không dựa vào settings.yaml): hai nhánh của đường stream
            flags = replace(goc[2], router=True, tim_them=True, lan_tim_dau="v0", thoi_tiet=True, bao_lu_cong_cu=True,
                            song_song_tra_loi=song_song, du_bao=du_bao_loi)
            ket_qua[song_song] = loi_bao(client, app, flags, True), loi_bao(client, app, flags, False)
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = goc
    for song_song, (co_goi, khong_goi) in ket_qua.items():
        assert co_goi["code"] == khong_goi["code"] == "generation_unavailable", song_song
        assert co_goi["message"] == f"{GENERATION_FAILURE_MESSAGE}\n\n{tt.CAU_BAO_LU}", song_song
        assert khong_goi["message"] == GENERATION_FAILURE_MESSAGE, song_song


def test_api_catches_the_same_error_classes_that_retrieval_raises():
    """Gói 1b (B-01 / C-01): lệnh production `uvicorn api.app:app` chạy từ backend/ — mỗi module chỉ nạp một lần và lớp lỗi API bắt
    là đúng đối tượng lớp mà module ném ra (trước đây `core.schema` và `backend.core.schema` cùng nạp ⇒ bắt hụt)."""
    import json
    import subprocess
    import sys
    from pathlib import Path

    probe = """
import json, sys
import api.app, api.routes.chat
import llm.citations, llm.generator_openai_full_corpus, llm.assistant, reranking.cross_encoder, retrieval.full_corpus, retrieval.full_corpus_context
pairs = [
    ("api.app", name, raiser) for name in ("ComponentNotReadyError", "RetrievalConfigurationError", "RetrievalDependencyError")
    for raiser in ("retrieval.full_corpus", "reranking.cross_encoder")
] + [
    ("api.routes.chat", "RetrievalDependencyError", "retrieval.full_corpus"),
    ("api.routes.chat", "RetrievalDependencyError", "reranking.cross_encoder"),
    ("api.routes.chat", "ContextBudgetError", "retrieval.full_corpus_context"),
    ("api.routes.chat", "GenerationError", "llm.generator_openai_full_corpus"),
    ("api.routes.chat", "GeneratorNotReadyError", "llm.assistant"),
    # từ S1 streaming lõi chung bắt lỗi citation thay route (route đọc `trace.citation_error`)
    ("llm.assistant", "CitationIntegrityError", "llm.citations"),
]
mismatched = [f"{c}.{n} vs {r}" for c, n, r in pairs
              if hasattr(sys.modules[r], n) and getattr(sys.modules[c], n) is not getattr(sys.modules[r], n)]
missing = [f"{c}.{n}" for c, n, r in pairs if not hasattr(sys.modules[c], n)]
twice = sorted(m[8:] for m in sys.modules if m.startswith("backend.") and m[8:] in sys.modules)
print(json.dumps({"twice": twice, "mismatched": mismatched, "missing": missing}))
"""
    res = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "PYTHONPATH": "", "HF_HUB_OFFLINE": "1"},
    )
    assert res.returncode == 0, res.stderr
    result = json.loads(res.stdout.strip().splitlines()[-1])
    assert result == {"twice": [], "mismatched": [], "missing": []}


def test_stale_corpus_at_startup_returns_409():
    """Kho lệch build record lúc khởi động ⇒ 409 corpus_reingest_required (B-01 / C-01). Dựng "kho đổi" chỉ trong bộ nhớ: bỏ một domain
    khỏi discovery — không sửa kho, file hay Qdrant; route trả lỗi retrieval trước bước sinh nên không gọi OpenAI."""
    settings = load_settings()
    knowledge_base = settings["full_corpus"]["knowledge_base"]
    knowledge_base["exclude_parts"] = [*knowledge_base["exclude_parts"], "foods"]
    app = create_app(settings)
    with TestClient(app) as client:
        response = client.post("/api/chat", json={"query": "Giá vé Đại Nội?"})
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "corpus_reingest_required"
