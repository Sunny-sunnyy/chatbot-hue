"""Real FastAPI lifecycle and strict full-corpus chat contract tests."""
import importlib
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
