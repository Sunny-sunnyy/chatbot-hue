"""Live tests for the FastAPI app: lifespan, health, chat contract, errors.

The app runs with its real lifespan against the real ingested test
collection, the real E5 embedder, the real MiniLM reranker (when the
profile uses it) and the real gpt-5.4-nano generator. Success tests print
the full question, full answer, model, latency, token usage and estimated
cost. Failure paths are reproduced with real conditions: dead Qdrant URLs,
a collection deleted mid-run, a missing key and a dead OpenAI base URL.
"""

import importlib
import logging
import time
import uuid

import pytest
from fastapi.testclient import TestClient
from qdrant_client import models

from api.app import create_app
from llm.prompt import SYSTEM_INSTRUCTIONS
from vectorstore.qdrant import expected_schema

from conftest import (
    TEST_COLLECTION,
    cleanup_collection,
    make_test_settings,
)

MODEL = "gpt-5.4-nano"
PRICING_INPUT_PER_1M = 0.20
PRICING_OUTPUT_PER_1M = 1.25


def make_app(profile="dense_only", collection=TEST_COLLECTION, **overrides):
    """Real app with real settings pointed at a marked test collection."""
    settings = make_test_settings(
        collection, **{"active_profile": profile, **overrides}
    )
    return create_app(settings=settings)


def create_with_points(client, name, structs):
    """Create a marked test collection and upsert real point structs."""
    settings = make_test_settings(name)
    client.create_collection(
        name,
        vectors_config={"dense": expected_schema(settings)["dense"]},
        sparse_vectors_config={"sparse": expected_schema(settings)["sparse"]},
    )
    if structs:
        client.upsert(name, points=structs, wait=True)
    return settings


def log_cost_summary(caplog):
    """Print the token summary and estimated cost from the generator log."""
    for record in caplog.records:
        if "tokens=" in record.getMessage():
            print(f"LIVE_LOG generator: {record.getMessage()}")
            token_part = record.getMessage().split("tokens=")[-1]
            if "/" in token_part and token_part != "unknown":
                tokens_in, tokens_out = token_part.split("/")
                cost = int(tokens_in) / 1e6 * PRICING_INPUT_PER_1M + (
                    int(tokens_out) / 1e6 * PRICING_OUTPUT_PER_1M
                )
                print(
                    f"LIVE_LOG estimated_cost_usd={cost:.8f} "
                    f"(input {tokens_in}, output {tokens_out})"
                )
            else:
                print("LIVE_LOG estimated_cost_usd=unknown (provider usage absent)")
            return


class TestImportAndHealth:
    def test_import_has_no_external_side_effect(self):
        module = importlib.import_module("api.app")
        assert module.app.state.retrieval_ready is False
        assert module.app.state.generator_configured is False

    def test_health_degraded_before_lifespan(self):
        from api.app import app

        response = TestClient(app).get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "degraded"
        assert body["components"]["app"] == "alive"
        assert body["components"]["qdrant"] == "not_ready"
        assert body["components"]["generator"] == "not_configured"

    def test_health_ok_after_real_lifespan(
        self, require_openai_key, ingested_collection
    ):
        app = make_app()
        with TestClient(app) as client:
            response = client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["components"]["qdrant"] == "ready"
        assert body["components"]["retrieval"] == "ready"
        assert body["components"]["generator"] == "configured"

    def test_health_degraded_when_qdrant_is_down(self, require_openai_key):
        """A dead Qdrant URL reproduces degraded startup for real."""
        app = make_app(
            collection="hue_rag_live_test_api_dead_qdrant",
            **{"vector_database.url": "http://localhost:6399", "vector_database.timeout": 3},
        )
        with TestClient(app) as client:
            health = client.get("/health")
            chat = client.post("/api/chat", json={"query": "Ăn gì ở Huế?"})
        assert health.status_code == 200
        assert health.json()["status"] == "degraded"
        assert chat.status_code == 503
        assert chat.json()["detail"]["code"] == "retrieval_not_ready"

    def test_health_never_exposes_secrets(
        self, require_openai_key, ingested_collection
    ):
        app = make_app()
        with TestClient(app) as client:
            response = client.get("/health")
        assert "OPENAI_API_KEY" not in response.text
        assert "sk-" not in response.text


class TestChatValidation:
    def test_empty_query_422(self):
        app = make_app()
        with TestClient(app) as client:
            response = client.post("/api/chat", json={"query": "   "})
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "invalid_query"

    def test_oversized_query_422(self):
        app = make_app()
        with TestClient(app) as client:
            response = client.post("/api/chat", json={"query": "x" * 501})
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "invalid_query"

    def test_whitespace_session_id_422(self):
        app = make_app()
        with TestClient(app) as client:
            response = client.post(
                "/api/chat", json={"query": "Ăn gì ở Huế?", "session_id": "   "}
            )
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "invalid_session_id"

    def test_oversized_session_id_422(self):
        app = make_app()
        with TestClient(app) as client:
            response = client.post(
                "/api/chat", json={"query": "Ăn gì ở Huế?", "session_id": "s" * 129}
            )
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "invalid_session_id"

    def test_missing_body_422_invalid_request(self):
        app = make_app()
        with TestClient(app) as client:
            response = client.post("/api/chat")
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "invalid_request"

    def test_malformed_body_422_invalid_request(self):
        app = make_app()
        with TestClient(app) as client:
            response = client.post(
                "/api/chat", json={"query": 123, "session_id": []}
            )
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "invalid_request"


class TestChatSuccess:
    def test_chat_success_with_explicit_session_id(
        self, require_openai_key, ingested_collection, caplog
    ):
        """One real end-to-end call: retrieval, context, generation, sources."""
        caplog.set_level(logging.INFO, logger="llm")
        app = make_app()
        question = "Ăn gì ở Huế?"
        with TestClient(app) as client:
            started = time.monotonic()
            response = client.post(
                "/api/chat", json={"query": question, "session_id": "live-api-echo"}
            )
            latency_ms = round((time.monotonic() - started) * 1000)
        assert response.status_code == 200
        body = response.json()
        assert body["answer"].strip()
        assert body["session_id"] == "live-api-echo"
        assert body["sources"], "real retrieval produced no sources"
        for source in body["sources"]:
            assert set(source) == {"chunk_id", "source", "title", "section", "score"}
            assert isinstance(source["score"], float)
        debug = body["retrieval_debug"]
        assert debug["profile"] == "dense_only"
        assert debug["embedding_model"] == "intfloat/multilingual-e5-small"
        assert "reranker_model" not in debug
        assert debug["retrieved_count"] >= debug["context_source_count"] >= 1
        print(
            f"LIVE_LOG question={question}\n"
            f"LIVE_LOG answer={body['answer']}\n"
            f"LIVE_LOG model={MODEL} latency_ms={latency_ms} "
            f"sources={[s['chunk_id'] for s in body['sources']]}"
        )
        log_cost_summary(caplog)

    def test_chat_generates_session_id_when_missing(
        self, require_openai_key, ingested_collection, caplog
    ):
        """The real server generates a UUID when the client sends none."""
        caplog.set_level(logging.INFO, logger="llm")
        app = make_app()
        question = "Ăn gì ở Huế?"
        with TestClient(app) as client:
            started = time.monotonic()
            response = client.post("/api/chat", json={"query": question})
            latency_ms = round((time.monotonic() - started) * 1000)
        assert response.status_code == 200
        body = response.json()
        session_id = body["session_id"]
        uuid.UUID(session_id)
        assert session_id != ""
        print(
            f"LIVE_LOG question={question}\n"
            f"LIVE_LOG answer={body['answer']}\n"
            f"LIVE_LOG model={MODEL} latency_ms={latency_ms} "
            f"session_id_generated={session_id}"
        )
        log_cost_summary(caplog)

    def test_hybrid_rerank_exposes_real_minilm_in_debug(
        self, require_openai_key, ingested_collection, caplog
    ):
        """The real MiniLM reranker appears in debug when it actually ran."""
        caplog.set_level(logging.INFO, logger="llm")
        app = make_app(profile="hybrid_rerank")
        question = "Ăn gì ở Huế?"
        with TestClient(app) as client:
            started = time.monotonic()
            response = client.post("/api/chat", json={"query": question})
            latency_ms = round((time.monotonic() - started) * 1000)
        assert response.status_code == 200
        body = response.json()
        debug = body["retrieval_debug"]
        assert debug["profile"] == "hybrid_rerank"
        assert debug["reranker_model"] == "cross-encoder/ms-marco-MiniLM-L-6-v2"
        print(
            f"LIVE_LOG question={question}\n"
            f"LIVE_LOG answer={body['answer']}\n"
            f"LIVE_LOG model={MODEL} latency_ms={latency_ms} profile=hybrid_rerank"
        )
        log_cost_summary(caplog)


class TestChatFailures:
    def test_retrieval_unavailable_when_collection_vanishes_mid_run(
        self, require_openai_key, ingested_point_structs, real_client
    ):
        """Deleting the collection after startup reproduces 503 for real."""
        name = "hue_rag_live_test_api_vanish"
        structs = [
            models.PointStruct(id=r.id, vector=r.vector, payload=r.payload)
            for r in ingested_point_structs
        ]
        settings = create_with_points(real_client, name, structs)
        app = make_app(collection=name)
        with TestClient(app) as client:
            health = client.get("/health")
            assert health.json()["status"] == "ok"
            cleanup_collection(real_client, name)
            response = client.post("/api/chat", json={"query": "Ăn gì ở Huế?"})
        assert response.status_code == 503
        assert response.json()["detail"]["code"] == "retrieval_unavailable"

    def test_generator_not_configured_503(
        self, monkeypatch, ingested_collection
    ):
        """A missing OpenAI key reproduces the typed 503 for real."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        app = make_app()
        with TestClient(app) as client:
            response = client.post("/api/chat", json={"query": "Ăn gì ở Huế?"})
        assert response.status_code == 503
        assert response.json()["detail"]["code"] == "generator_not_configured"

    def test_generator_unavailable_502(
        self, require_openai_key, ingested_collection, monkeypatch
    ):
        """A dead OpenAI base URL reproduces the provider failure for real."""
        monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:9/v1")
        app = make_app()
        with TestClient(app) as client:
            response = client.post("/api/chat", json={"query": "Ăn gì ở Huế?"})
        assert response.status_code == 502
        assert response.json()["detail"]["code"] == "generator_unavailable"

    def test_no_sensitive_payload_in_responses(
        self, require_openai_key, ingested_collection, caplog
    ):
        caplog.set_level(logging.INFO, logger="llm")
        app = make_app()
        question = "Ăn gì ở Huế?"
        with TestClient(app) as client:
            started = time.monotonic()
            success = client.post("/api/chat", json={"query": question})
            latency_ms = round((time.monotonic() - started) * 1000)
            failure = client.post("/api/chat", json={"query": ""})
        for response in (success, failure):
            assert SYSTEM_INSTRUCTIONS not in response.text
            assert "OPENAI_API_KEY" not in response.text
            assert "sk-" not in response.text
        print(
            f"LIVE_LOG question={question}\n"
            f"LIVE_LOG answer={success.json()['answer']}\n"
            f"LIVE_LOG model={MODEL} latency_ms={latency_ms} "
            f"status={success.status_code}"
        )
        log_cost_summary(caplog)


class TestLifecycleWarmup:
    """Milestone 6.1: real component warm-up happens inside the lifespan."""

    def test_lifespan_warms_e5_and_minilm_before_ready(self, ingested_collection):
        """hybrid_rerank lifespan loads E5 AND MiniLM before /health is ready."""
        from reranking.models import cross_encoder as rerank_module

        rerank_module._get_cross_encoder.cache_clear()
        app = make_app(profile="hybrid_rerank")
        with TestClient(app) as client:
            health = client.get("/health")
        assert health.status_code == 200
        components = health.json()["components"]
        assert components["qdrant"] == "ready"
        assert components["retrieval"] == "ready"
        assert (
            app.state.retrieval_service._stack.dense_retriever._embedder._model
            is not None
        ), "E5 must load during startup"
        assert (
            rerank_module._get_cross_encoder.cache_info().misses >= 1
        ), "MiniLM must load during startup"

    def test_dense_only_lifespan_loads_e5_but_never_minilm(self, ingested_collection):
        """Profile scoping at app level: dense_only warms E5, skips MiniLM."""
        from reranking.models import cross_encoder as rerank_module

        rerank_module._get_cross_encoder.cache_clear()
        app = make_app(profile="dense_only")
        with TestClient(app) as client:
            health = client.get("/health")
        assert health.json()["components"]["qdrant"] == "ready"
        assert (
            app.state.retrieval_service._stack.dense_retriever._embedder._model
            is not None
        ), "E5 must load during startup"
        assert (
            rerank_module._get_cross_encoder.cache_info().misses == 0
        ), "dense_only must not load MiniLM"
