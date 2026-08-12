"""Tests for profile-scoped startup, bounded scroll, snapshot and staleness."""
import hashlib
from types import SimpleNamespace

import pytest
from qdrant_client import models

from core.schema import (
    ComponentNotReadyError,
    RetrievalConfigurationError,
)
from core.startup import (
    CANONICAL_CHUNK_COUNT,
    SCROLL_PAYLOAD_FIELDS,
    build_retrieval_stack,
    verify_snapshot,
)
from reranking.models import cross_encoder
from reranking.reranker import ScorerReranker
from retrieval.service import build_service

COLLECTION = "hue_foods_e5_small_384"
MODEL = "fake-e5"
DIMENSION = 4


class FakeEmbedder:
    """Deterministic embedder injected to keep startup fully offline."""

    def __init__(self, dimension=DIMENSION, model_id=MODEL):
        self._dimension = dimension
        self._model_id = model_id

    @property
    def model_id(self):
        return self._model_id

    @property
    def dimension(self):
        return self._dimension

    def embed_query(self, query):
        return [0.1] * self._dimension

    def embed_documents(self, texts):
        return [[0.1] * self._dimension for _ in texts]


def make_info(dense_size=DIMENSION):
    vectors = {"dense": SimpleNamespace(size=dense_size, distance=models.Distance.COSINE)}
    sparse = {"sparse": SimpleNamespace(index=object())}
    return SimpleNamespace(
        config=SimpleNamespace(params=SimpleNamespace(vectors=vectors, sparse_vectors=sparse))
    )


def make_payloads(count=CANONICAL_CHUNK_COUNT, model=MODEL, dimension=DIMENSION):
    return [
        {
            "chunk_id": f"foods/restaurants/doc{i:03d}.md|Tóm tắt|0",
            "text": f"nội dung quán {i}",
            "source": f"foods/restaurants/doc{i:03d}.md",
            "title": "Tiêu đề",
            "section": "Tóm tắt",
            "category": "foods",
            "subcategory": "restaurants",
            "chunk_type": "section",
            "embedding_model": model,
            "embedding_dimension": dimension,
        }
        for i in range(count)
    ]


class FakeClient:
    """In-memory Qdrant fake: schema, count, bounded scroll and dense query."""

    def __init__(self, payloads, count=None, info=None):
        self._payloads = payloads
        self._count = count if count is not None else len(payloads)
        self._info = info if info is not None else make_info()
        self.scroll_calls = []
        self.count_calls = 0
        self._exists = True

    def collection_exists(self, name):
        return self._exists

    def set_missing(self):
        self._exists = False

    def get_collection(self, name):
        return self._info

    def set_info(self, info):
        self._info = info

    def count(self, name, exact=True):
        self.count_calls += 1
        return SimpleNamespace(count=self._count)

    def set_count(self, count):
        self._count = count

    def scroll(self, name, limit, offset=None, with_payload=True, with_vectors=False, timeout=None):
        self.scroll_calls.append(
            {"limit": limit, "with_payload": with_payload, "with_vectors": with_vectors}
        )
        start = 0 if offset is None else offset
        batch = self._payloads[start : start + limit]
        next_offset = start + len(batch) if start + len(batch) < len(self._payloads) else None
        return [SimpleNamespace(payload=payload) for payload in batch], next_offset

    def query_points(self, collection_name, query, using=None, limit=None, **kwargs):
        points = [
            SimpleNamespace(id=payload["chunk_id"], score=1.0 - i * 0.001, payload=payload)
            for i, payload in enumerate(self._payloads)
        ]
        return SimpleNamespace(points=points[:limit])


def make_settings(profile="dense_only", **overrides):
    settings = {
        "active_profile": profile,
        "profiles": {
            "dense_only": {"retrieval_mode": "dense", "use_bm25": False, "use_reranker": False},
            "hybrid_no_rerank": {
                "retrieval_mode": "hybrid",
                "use_bm25": True,
                "use_reranker": False,
            },
            "hybrid_rerank": {
                "retrieval_mode": "hybrid",
                "use_bm25": True,
                "use_reranker": True,
            },
        },
        "embedding": {"model": MODEL, "vector_size": DIMENSION, "device": "cpu", "batch_size": 64},
        "vector_database": {
            "url": "http://localhost:6333",
            "collection_name": COLLECTION,
            "vector_size": DIMENSION,
            "timeout": 30,
            "scroll_batch_size": 128,
        },
        "retrieval": {
            "top_k": 10,
            "candidate_multiplier": 3,
            "score_threshold": 0.0,
            "dense_weight": 0.6,
            "bm25_weight": 0.4,
        },
        "reranking": {"model": "cross-encoder/ms-marco-MiniLM-L-6-v2", "device": "cpu", "top_k": 5},
    }
    for key, value in overrides.items():
        section, field = key.split(".", 1)
        settings[section][field] = value
    return settings


def test_dense_only_builds_only_dense_retriever():
    client = FakeClient(make_payloads())
    stack = build_retrieval_stack(
        make_settings("dense_only"), client=client, embedder=FakeEmbedder()
    )
    assert stack.dense_retriever is not None
    assert stack.hybrid_retriever is None
    assert stack.reranker is None
    assert stack.snapshot.bm25_ready is False
    assert stack.snapshot.reranker_ready is False
    assert stack.snapshot.point_count == CANONICAL_CHUNK_COUNT
    assert stack.snapshot.corpus_fingerprint is None
    assert client.scroll_calls == []
    assert client.count_calls == 1


def test_hybrid_no_rerank_scrolls_bounded_batches_with_safe_projection():
    client = FakeClient(make_payloads())
    stack = build_retrieval_stack(
        make_settings("hybrid_no_rerank"), client=client, embedder=FakeEmbedder()
    )
    assert stack.hybrid_retriever is not None
    assert stack.reranker is None
    assert stack.snapshot.bm25_ready is True
    assert stack.snapshot.corpus_fingerprint is not None
    limits = [call["limit"] for call in client.scroll_calls]
    assert limits == [128, 128, 128, 128, 128]
    assert all(call["with_vectors"] is False for call in client.scroll_calls)
    assert all(call["with_payload"] == SCROLL_PAYLOAD_FIELDS for call in client.scroll_calls)
    assert client.count_calls == 1


def test_hybrid_rerank_loads_cached_reranker_once(monkeypatch):
    calls = []

    def fake_load(model_id, device):
        calls.append((model_id, device))
        return object()

    monkeypatch.setattr(cross_encoder, "_get_cross_encoder", fake_load)
    client = FakeClient(make_payloads())
    stack = build_retrieval_stack(
        make_settings("hybrid_rerank"), client=client, embedder=FakeEmbedder()
    )
    assert stack.hybrid_retriever is not None
    assert stack.reranker is not None
    assert calls == [("cross-encoder/ms-marco-MiniLM-L-6-v2", "cpu")]
    assert stack.snapshot.reranker_ready is True


def test_hybrid_rerank_missing_cache_fails_not_ready(monkeypatch):
    def fail_load(model_id, device):
        raise OSError("cache missing")

    monkeypatch.setattr(cross_encoder, "_get_cross_encoder", fail_load)
    client = FakeClient(make_payloads())
    with pytest.raises(ComponentNotReadyError, match="cache"):
        build_retrieval_stack(
            make_settings("hybrid_rerank"), client=client, embedder=FakeEmbedder()
        )


def test_hybrid_rerank_injected_reranker_is_used_without_load(monkeypatch):
    calls = []

    def fail_if_called(model_id, device):
        calls.append(model_id)
        return object()

    monkeypatch.setattr(cross_encoder, "_get_cross_encoder", fail_if_called)
    reranker = ScorerReranker(scorer=lambda query, docs: [0.5] * len(docs), model_id="fake")
    client = FakeClient(make_payloads())
    stack = build_retrieval_stack(
        make_settings("hybrid_rerank"),
        client=client,
        embedder=FakeEmbedder(),
        reranker=reranker,
    )
    assert stack.reranker is reranker
    assert calls == []


def test_fingerprint_is_deterministic_and_sensitive_to_corpus():
    first = build_retrieval_stack(
        make_settings("hybrid_no_rerank"), client=FakeClient(make_payloads()), embedder=FakeEmbedder()
    )
    second = build_retrieval_stack(
        make_settings("hybrid_no_rerank"), client=FakeClient(make_payloads()), embedder=FakeEmbedder()
    )
    assert first.snapshot.corpus_fingerprint == second.snapshot.corpus_fingerprint
    assert len(first.snapshot.corpus_fingerprint) == 64
    changed = make_payloads()
    changed[0]["text"] = "nội dung khác hẳn"
    third = build_retrieval_stack(
        make_settings("hybrid_no_rerank"), client=FakeClient(changed), embedder=FakeEmbedder()
    )
    assert third.snapshot.corpus_fingerprint != first.snapshot.corpus_fingerprint


def test_corpus_fingerprint_matches_reference_digest():
    payloads = make_payloads()
    pairs = sorted((payload["chunk_id"], payload["text"]) for payload in payloads)
    lines = [f"{chunk_id}\x00{text}" for chunk_id, text in pairs]
    expected = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    stack = build_retrieval_stack(
        make_settings("hybrid_no_rerank"), client=FakeClient(payloads), embedder=FakeEmbedder()
    )
    assert stack.snapshot.corpus_fingerprint == expected


def test_scroll_batch_size_can_be_overridden():
    client = FakeClient(make_payloads())
    build_retrieval_stack(
        make_settings("hybrid_no_rerank"),
        client=client,
        embedder=FakeEmbedder(),
        scroll_batch_size=64,
    )
    assert all(call["limit"] == 64 for call in client.scroll_calls)


def test_count_mismatch_raises_not_ready_for_dense_only():
    client = FakeClient(make_payloads(572), count=571)
    with pytest.raises(ComponentNotReadyError, match="571"):
        build_retrieval_stack(make_settings("dense_only"), client=client, embedder=FakeEmbedder())


def test_scroll_payload_count_mismatch_raises():
    # count() says 572 but the scroll only reaches 571 payloads
    client = FakeClient(make_payloads(571), count=572)
    with pytest.raises(ComponentNotReadyError, match="571 payloads"):
        build_retrieval_stack(
            make_settings("hybrid_no_rerank"), client=client, embedder=FakeEmbedder()
        )


def test_duplicate_chunk_ids_raise_not_ready():
    payloads = make_payloads()
    payloads[1]["chunk_id"] = payloads[0]["chunk_id"]
    with pytest.raises(ComponentNotReadyError, match="duplicate"):
        build_retrieval_stack(
            make_settings("hybrid_no_rerank"), client=FakeClient(payloads), embedder=FakeEmbedder()
        )


def test_empty_text_raises_not_ready():
    payloads = make_payloads()
    payloads[0]["text"] = "   "
    with pytest.raises(ComponentNotReadyError, match="empty text"):
        build_retrieval_stack(
            make_settings("hybrid_no_rerank"), client=FakeClient(payloads), embedder=FakeEmbedder()
        )


def test_payload_embedding_model_mismatch_raises():
    payloads = make_payloads(model="other-model")
    with pytest.raises(ComponentNotReadyError, match="embedding model"):
        build_retrieval_stack(
            make_settings("hybrid_no_rerank"), client=FakeClient(payloads), embedder=FakeEmbedder()
        )


def test_missing_collection_raises_configuration_error():
    client = FakeClient(make_payloads())
    client.set_missing()
    with pytest.raises(RetrievalConfigurationError, match="does not exist"):
        build_retrieval_stack(make_settings("dense_only"), client=client, embedder=FakeEmbedder())


def test_schema_mismatch_raises_configuration_error():
    client = FakeClient(make_payloads(), info=make_info(dense_size=512))
    with pytest.raises(RetrievalConfigurationError, match="schema"):
        build_retrieval_stack(make_settings("dense_only"), client=client, embedder=FakeEmbedder())


def test_unknown_profile_raises_configuration_error():
    with pytest.raises(RetrievalConfigurationError, match="active_profile"):
        build_retrieval_stack(
            make_settings("bogus"),
            client=FakeClient(make_payloads()),
            embedder=FakeEmbedder(),
        )


def test_embedding_db_dimension_mismatch_raises():
    settings = make_settings("dense_only", **{"embedding.vector_size": 5})
    with pytest.raises(RetrievalConfigurationError, match="vector_size"):
        build_retrieval_stack(
            settings, client=FakeClient(make_payloads()), embedder=FakeEmbedder()
        )


def test_injected_embedder_dimension_mismatch_raises():
    settings = make_settings("dense_only")
    with pytest.raises(RetrievalConfigurationError, match="embedder dimension"):
        build_retrieval_stack(
            settings,
            client=FakeClient(make_payloads()),
            embedder=FakeEmbedder(dimension=5),
        )


def test_injected_embedder_model_id_mismatch_raises():
    settings = make_settings("dense_only")
    with pytest.raises(RetrievalConfigurationError, match="embedder model_id"):
        build_retrieval_stack(
            settings,
            client=FakeClient(make_payloads()),
            embedder=FakeEmbedder(model_id="wrong-model"),
        )


def test_injected_embedder_matching_model_id_builds():
    settings = make_settings("dense_only")
    stack = build_retrieval_stack(
        settings,
        client=FakeClient(make_payloads()),
        embedder=FakeEmbedder(model_id=MODEL),
    )
    assert stack.snapshot.embedding_model == MODEL


def test_components_are_immutable_after_startup():
    payloads = make_payloads()
    client = FakeClient(payloads)
    stack = build_retrieval_stack(
        make_settings("hybrid_no_rerank"), client=client, embedder=FakeEmbedder()
    )
    before = [doc.metadata["bm25_score"] for doc in stack.hybrid_retriever.search("nội dung quán")]
    payloads[0]["text"] = "thay đổi hoàn toàn nội dung"
    after = [doc.metadata["bm25_score"] for doc in stack.hybrid_retriever.search("nội dung quán")]
    assert after == before


def test_build_service_factory_routes_active_profile():
    service = build_service(
        make_settings("dense_only"), client=FakeClient(make_payloads()), embedder=FakeEmbedder()
    )
    assert service.active_profile == "dense_only"
    assert service.snapshot.point_count == CANONICAL_CHUNK_COUNT


def test_verify_snapshot_passes_when_unchanged():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    assert verify_snapshot(stack, settings=settings, client=client) is None


def test_verify_snapshot_passes_for_dense_only_without_scroll():
    client = FakeClient(make_payloads())
    settings = make_settings("dense_only")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    assert verify_snapshot(stack, settings=settings, client=client) is None
    assert client.scroll_calls == []


def test_verify_snapshot_detects_point_count_change():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    client.set_count(571)
    with pytest.raises(ComponentNotReadyError, match="point count"):
        verify_snapshot(stack, settings=settings, client=client)


def test_verify_snapshot_detects_corpus_fingerprint_change():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    client._payloads[0]["text"] = "nội dung bị thay đổi"
    with pytest.raises(ComponentNotReadyError, match="fingerprint"):
        verify_snapshot(stack, settings=settings, client=client)


def test_verify_snapshot_detects_missing_collection():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    client.set_missing()
    with pytest.raises(ComponentNotReadyError, match="missing"):
        verify_snapshot(stack, settings=settings, client=client)


def test_verify_snapshot_detects_schema_change():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    client.set_info(make_info(dense_size=512))
    with pytest.raises(ComponentNotReadyError, match="schema"):
        verify_snapshot(stack, settings=settings, client=client)


def test_verify_snapshot_detects_config_change():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    changed = make_settings("dense_only")
    with pytest.raises(ComponentNotReadyError, match="active_profile"):
        verify_snapshot(stack, settings=changed, client=client)


def test_verify_snapshot_detects_fusion_weight_change():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    changed = make_settings(
        "hybrid_no_rerank",
        **{"retrieval.dense_weight": 0.7, "retrieval.bm25_weight": 0.3},
    )
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(stack, settings=changed, client=client)


def test_verify_snapshot_detects_candidate_depth_change():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    changed = make_settings("hybrid_no_rerank", **{"retrieval.top_k": 5})
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(stack, settings=changed, client=client)
    changed = make_settings("hybrid_no_rerank", **{"retrieval.candidate_multiplier": 4})
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(stack, settings=changed, client=client)


def test_verify_snapshot_detects_rerank_config_change_for_hybrid_rerank(monkeypatch):
    def fake_load(model_id, device):
        return object()

    monkeypatch.setattr(cross_encoder, "_get_cross_encoder", fake_load)
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    changed_model = make_settings("hybrid_rerank", **{"reranking.model": "other-model"})
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(stack, settings=changed_model, client=client)
    changed_top_k = make_settings("hybrid_rerank", **{"reranking.top_k": 3})
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(stack, settings=changed_top_k, client=client)


def test_verify_snapshot_ignores_rerank_config_for_non_rerank_profile():
    client = FakeClient(make_payloads())
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=client, embedder=FakeEmbedder())
    changed = make_settings("hybrid_no_rerank", **{"reranking.top_k": 3})
    assert verify_snapshot(stack, settings=changed, client=client) is None
