"""Real FastAPI lifecycle and answer-only chat contract tests."""
import importlib
import logging

from fastapi.testclient import TestClient

from api.app import create_app

from conftest import TEST_COLLECTION, make_test_settings

SERVICE_UNAVAILABLE = (
    "Hệ thống tạm thời không khả dụng. Vui lòng thử lại sau."
)


def make_app(profile="dense_only", collection=TEST_COLLECTION, **overrides):
    settings = make_test_settings(
        collection,
        **{"active_profile": profile, **overrides},
    )
    return create_app(settings=settings)


class TestImportAndHealth:
    def test_import_has_no_external_side_effect(self):
        module = importlib.import_module("api.app")
        assert module.app.state.retrieval_ready is False
        assert module.app.state.generator_configured is False

    def test_health_degraded_before_lifespan(self):
        from api.app import app

        response = TestClient(app).get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "degraded",
            "components": {
                "app": "alive",
                "qdrant": "not_ready",
                "retrieval": "not_ready",
                "generator": "not_configured",
            },
        }

    def test_health_ok_after_real_lifespan(
        self,
        require_openai_key,
        ingested_collection,
    ):
        with TestClient(make_app()) as client:
            response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["components"]["retrieval"] == "ready"
        assert response.json()["components"]["generator"] == "configured"


class TestChatValidation:
    def test_empty_query_returns_simple_422(self):
        response = TestClient(make_app()).post(
            "/api/chat",
            json={"query": "   "},
        )
        assert response.status_code == 422
        assert response.json() == {"detail": "Yêu cầu không hợp lệ."}

    def test_oversized_query_returns_simple_422(self):
        response = TestClient(make_app()).post(
            "/api/chat",
            json={"query": "x" * 501},
        )
        assert response.status_code == 422
        assert response.json() == {"detail": "Yêu cầu không hợp lệ."}

    def test_malformed_body_returns_simple_422(self):
        response = TestClient(make_app()).post(
            "/api/chat",
            json={"query": []},
        )
        assert response.status_code == 422
        assert response.json() == {"detail": "Yêu cầu không hợp lệ."}


class TestChatBehavior:
    def test_chat_before_lifespan_returns_simple_503(self):
        app = create_app(settings=make_test_settings())
        response = TestClient(app).post(
            "/api/chat",
            json={"query": "Ăn gì ở Huế?"},
        )
        assert response.status_code == 503
        assert response.json() == {"detail": SERVICE_UNAVAILABLE}

    def test_no_context_returns_exact_fallback_without_generation(
        self,
        ingested_collection,
    ):
        app = make_app(**{"retrieval.max_context_characters": 1})
        with TestClient(app) as client:
            response = client.post(
                "/api/chat",
                json={"query": "Ăn gì ở Huế?"},
            )
        assert response.status_code == 200
        assert response.json() == {
            "answer": "Mình không tìm thấy thông tin phù hợp trong dữ liệu hiện tại."
        }

    def test_real_chat_returns_only_answer_and_writes_backend_logs(
        self,
        require_openai_key,
        ingested_collection,
        caplog,
    ):
        caplog.set_level(logging.INFO)
        question = "Bún bò Huế có đặc điểm gì nổi bật?"
        with TestClient(make_app()) as client:
            logging.getLogger("chat").addHandler(caplog.handler)
            logging.getLogger("llm").addHandler(caplog.handler)
            response = client.post("/api/chat", json={"query": question})
        assert response.status_code == 200
        assert set(response.json()) == {"answer"}
        assert response.json()["answer"].strip()
        messages = [record.getMessage() for record in caplog.records]
        assert any(f"Received question: {question}" in item for item in messages)
        assert any("Retrieved" in item and "documents" in item for item in messages)
        assert any("Generated answer successfully" in item for item in messages)
        assert "sources" not in response.text
        assert "retrieval_debug" not in response.text
        assert "session_id" not in response.text
        assert "Generated answer successfully" not in response.text


class TestLifecycleWarmup:
    """Milestone 6.1: real component warm-up happens inside the lifespan."""

    def test_lifespan_warms_e5_and_minilm_before_ready(self, ingested_collection):
        """hybrid_rerank lifespan loads E5 AND MiniLM before /health is ready."""
        app = make_app(profile="hybrid_rerank")
        with TestClient(app) as client:
            health = client.get("/health")
        assert health.status_code == 200
        components = health.json()["components"]
        assert components["qdrant"] == "ready"
        assert components["retrieval"] == "ready"
        assert (
            app.state.retrieval_service._dense._embedder._model
            is not None
        ), "E5 must load during startup"
        assert (
            app.state.retrieval_service._reranker._model
            is not None
        ), "MiniLM must load during startup"

    def test_dense_only_lifespan_loads_e5_but_never_minilm(self, ingested_collection):
        """Profile scoping at app level: dense_only warms E5, skips MiniLM."""
        app = make_app(profile="dense_only")
        with TestClient(app) as client:
            health = client.get("/health")
        assert health.json()["components"]["qdrant"] == "ready"
        assert (
            app.state.retrieval_service._dense._embedder._model
            is not None
        ), "E5 must load during startup"
        assert (
            app.state.retrieval_service._reranker is None
        ), "dense_only must not load MiniLM"
