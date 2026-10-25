"""Real FastAPI lifecycle and strict full-corpus chat contract tests."""
import importlib
from types import SimpleNamespace

from fastapi.testclient import TestClient

from api.app import create_app
from core.settings_loader import load_settings


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


def test_real_first_chunk_budget_error_has_no_partial_answer(require_openai_key):
    settings = load_settings()
    settings["full_corpus_generation"] = dict(settings["full_corpus_generation"])
    settings["full_corpus_generation"]["context_limit"] = 2561
    app = create_app(settings)
    with TestClient(app) as client:
        response = client.post("/api/chat", json={"query": "Giá vé Đại Nội?"})
    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "context_budget_error",
            "message": "Không thể đóng gói ngữ cảnh trong giới hạn cho phép.",
        }
    }
    assert "answer" not in response.text
    assert "sources" not in response.text


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


def test_production_app_state_has_no_last_chat_trace_after_chat(require_openai_key):
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
        async def generate_answer(self, query, context_text):
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
import llm.citations, llm.generator_openai_full_corpus, reranking.cross_encoder, retrieval.full_corpus, retrieval.full_corpus_context
pairs = [
    ("api.app", name, raiser) for name in ("ComponentNotReadyError", "RetrievalConfigurationError", "RetrievalDependencyError")
    for raiser in ("retrieval.full_corpus", "reranking.cross_encoder")
] + [
    ("api.routes.chat", "RetrievalDependencyError", "retrieval.full_corpus"),
    ("api.routes.chat", "RetrievalDependencyError", "reranking.cross_encoder"),
    ("api.routes.chat", "ContextBudgetError", "retrieval.full_corpus_context"),
    ("api.routes.chat", "GenerationError", "llm.generator_openai_full_corpus"),
    ("api.routes.chat", "CitationIntegrityError", "llm.citations"),
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
