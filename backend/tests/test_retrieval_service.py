"""Tests for profile routing, score metadata and typed error propagation."""
import copy
from types import SimpleNamespace

import pytest

from core.schema import (
    ComponentNotReadyError,
    InvalidQueryError,
    RetrievedDocument,
    RetrievalConfigurationError,
    RetrievalDependencyError,
)
from core.startup import RetrievalSnapshot, RetrievalStack
from embedding.base import EmbeddingError
from reranking.reranker import ScorerReranker
from retrieval.dense_retriever import DenseRetriever, QUERY_PAYLOAD_FIELDS
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.service import RetrievalService
from scoring.bm25 import BM25

MODEL_ID = "fake-e5"


class FakeEmbedder:
    """Deterministic embedder; model_id mirrors the real contract."""

    model_id = MODEL_ID

    def __init__(self, vector=None):
        self._vector = vector or [0.1, 0.2, 0.3, 0.4]

    def embed_query(self, query):
        return list(self._vector)

    def embed_documents(self, texts):
        return [list(self._vector) for _ in texts]


class FailingEmbedder:
    """Embedder that fails like a broken model backend."""

    model_id = MODEL_ID

    def embed_query(self, query):
        raise EmbeddingError("fake model failure")

    def embed_documents(self, texts):
        raise EmbeddingError("fake model failure")


class FailingClient:
    """Client whose dense query fails like a broken Qdrant backend."""

    def query_points(self, *args, **kwargs):
        raise RuntimeError("fake transport failure")


class FakeClient:
    """In-memory dense query fake recording every call."""

    def __init__(self, scored_points):
        self._scored_points = scored_points
        self.calls = []

    def query_points(self, collection_name, query, using=None, limit=None, with_payload=True, **kwargs):
        self.calls.append(
            {
                "collection_name": collection_name,
                "using": using,
                "limit": limit,
                "with_payload": with_payload,
            }
        )
        return SimpleNamespace(points=self._scored_points[:limit])


def make_point(chunk_id, score, text=None):
    payload = {
        "chunk_id": chunk_id,
        "text": text or f"text {chunk_id}",
        "source": "foods/restaurants/doc.md",
        "title": "Doc",
        "section": "Tóm tắt",
        "category": "foods",
        "subcategory": "restaurants",
        "chunk_type": "section",
    }
    return SimpleNamespace(id=chunk_id, score=score, payload=payload)


def make_snapshot(profile, **overrides):
    fields = {
        "collection_name": "hue_foods_e5_small_384",
        "point_count": 572,
        "embedding_model": MODEL_ID,
        "embedding_dimension": 4,
        "corpus_fingerprint": "abc123",
        "active_profile": profile,
        "bm25_ready": profile != "dense_only",
        "reranker_ready": profile == "hybrid_rerank",
    }
    fields.update(overrides)
    return RetrievalSnapshot(**fields)


def make_dense(embedder=None, client=None, top_k=10):
    return DenseRetriever(
        client=client if client is not None else FakeClient([]),
        embedder=embedder if embedder is not None else FakeEmbedder(),
        collection_name="hue_foods_e5_small_384",
        top_k=top_k,
    )


def make_hybrid(corpus_texts, dense_client=None, top_k=10, candidate_depth=30):
    dense = make_dense(client=dense_client, top_k=top_k)
    bm25 = BM25().fit(corpus_texts)
    return HybridRetriever(
        dense_retriever=dense,
        bm25=bm25,
        candidate_depth=candidate_depth,
        top_k=top_k,
    )


def make_service(profile, stack=None, **kwargs):
    if stack is None:
        stack = RetrievalStack(snapshot=make_snapshot(profile))
    return RetrievalService(stack, **kwargs)


def test_dense_only_returns_raw_cosine_scores_with_stage_metadata():
    client = FakeClient([make_point("b", 0.7), make_point("a", 0.9)])
    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"), dense_retriever=make_dense(client=client)
        ),
    )
    documents = service.search("bún bò huế")
    assert [doc.id for doc in documents] == ["a", "b"]
    assert documents[0].score == pytest.approx(0.9)
    assert documents[0].metadata["dense_score"] == pytest.approx(0.9)
    assert documents[0].metadata["embedding_model"] == MODEL_ID
    assert documents[0].metadata["retrieval_profile"] == "dense_only"
    assert documents[0].metadata["retrieval_rank"] == 1
    assert documents[1].metadata["retrieval_rank"] == 2
    for doc in documents:
        for absent in (
            "bm25_score",
            "normalized_dense_score",
            "normalized_bm25_score",
            "hybrid_score",
            "rerank_score",
            "reranker_model",
        ):
            assert absent not in doc.metadata


def test_dense_only_requests_exact_top_k_depth():
    client = FakeClient([make_point(f"d{i:02d}", 0.9 - i * 0.01) for i in range(30)])
    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"), dense_retriever=make_dense(client=client)
        ),
    )
    documents = service.search("bún bò huế")
    assert len(documents) == 10
    assert client.calls[0]["limit"] == 10
    assert client.calls[0]["using"] == "dense"
    assert client.calls[0]["with_payload"] == QUERY_PAYLOAD_FIELDS


def test_dense_only_never_calls_hybrid_or_reranker():
    client = FakeClient([make_point("a", 0.5)])
    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"), dense_retriever=make_dense(client=client)
        ),
    )
    service.search("bún bò huế")
    assert len(client.calls) == 1
    assert client.calls[0]["using"] == "dense"


def test_dense_only_ties_break_by_chunk_id():
    client = FakeClient([make_point("b", 0.8), make_point("a", 0.8)])
    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"), dense_retriever=make_dense(client=client)
        ),
    )
    assert [doc.id for doc in service.search("bún bò huế")] == ["a", "b"]


def test_hybrid_no_rerank_fusion_math_on_known_corpus():
    client = FakeClient(
        [
            make_point("d0", 0.8, text="a b"),
            make_point("d1", 0.6, text="b"),
            make_point("d2", 0.4, text="c"),
        ]
    )
    hybrid = make_hybrid(["a b", "b", "c"], dense_client=client)
    service = make_service(
        "hybrid_no_rerank",
        stack=RetrievalStack(
            snapshot=make_snapshot("hybrid_no_rerank"), hybrid_retriever=hybrid
        ),
    )
    documents = service.search("a")
    assert [doc.id for doc in documents] == ["d0", "d1", "d2"]
    # normalized dense = [1.0, 0.5, 0.0]; BM25("a") = [0.9808..., 0, 0]
    # -> normalized BM25 = [1.0, 0.0, 0.0]; hybrid = 0.6*dense + 0.4*bm25
    assert documents[0].score == pytest.approx(1.0)
    assert documents[1].score == pytest.approx(0.3)
    assert documents[2].score == pytest.approx(0.0)
    assert documents[0].metadata["normalized_dense_score"] == pytest.approx(1.0)
    assert documents[0].metadata["normalized_bm25_score"] == pytest.approx(1.0)
    assert documents[0].metadata["hybrid_score"] == pytest.approx(1.0)
    assert documents[0].metadata["bm25_score"] == pytest.approx(
        BM25().fit(["a b", "b", "c"]).score("a", "a b")
    )
    assert documents[0].score == documents[0].metadata["hybrid_score"]
    assert documents[0].metadata["retrieval_profile"] == "hybrid_no_rerank"
    assert "rerank_score" not in documents[0].metadata
    assert "reranker_model" not in documents[0].metadata


def test_hybrid_no_rerank_requests_candidate_depth():
    client = FakeClient([make_point(f"d{i:02d}", 0.9 - i * 0.01) for i in range(30)])
    hybrid = make_hybrid([f"text {i}" for i in range(30)], dense_client=client)
    service = make_service(
        "hybrid_no_rerank",
        stack=RetrievalStack(
            snapshot=make_snapshot("hybrid_no_rerank"), hybrid_retriever=hybrid
        ),
    )
    documents = service.search("bún bò huế")
    assert len(documents) == 10
    assert client.calls[0]["limit"] == 30


def test_hybrid_constant_bm25_signal_does_not_affect_ranking():
    client = FakeClient(
        [
            make_point("d0", 0.8, text="x y"),
            make_point("d1", 0.6, text="z w"),
            make_point("d2", 0.4, text="q r"),
        ]
    )
    hybrid = make_hybrid(["x y", "z w", "q r"], dense_client=client)
    service = make_service(
        "hybrid_no_rerank",
        stack=RetrievalStack(
            snapshot=make_snapshot("hybrid_no_rerank"), hybrid_retriever=hybrid
        ),
    )
    documents = service.search("bún bò huế")
    assert [doc.id for doc in documents] == ["d0", "d1", "d2"]
    assert documents[0].score == pytest.approx(0.6)
    assert documents[1].score == pytest.approx(0.3)
    assert documents[2].score == pytest.approx(0.0)
    assert documents[0].metadata["normalized_bm25_score"] == pytest.approx(0.0)


def test_hybrid_rerank_runs_reranker_on_exactly_pre_rerank_top_10():
    client = FakeClient([make_point(f"d{i:02d}", 0.9 - i * 0.01) for i in range(30)])
    hybrid = make_hybrid([f"text {i}" for i in range(30)], dense_client=client)
    scored = []

    def scorer(query, documents):
        scored.append(len(documents))
        return [float(len(documents) - i) for i in range(len(documents))]

    reranker = ScorerReranker(scorer=scorer, model_id="fake-reranker")
    service = make_service(
        "hybrid_rerank",
        stack=RetrievalStack(
            snapshot=make_snapshot("hybrid_rerank"),
            hybrid_retriever=hybrid,
            reranker=reranker,
        ),
    )
    documents = service.search("bún bò huế")
    assert client.calls[0]["limit"] == 30
    assert scored == [10]
    assert len(documents) == 5
    assert documents[0].metadata["reranker_model"] == "fake-reranker"
    assert documents[0].metadata["rerank_score"] == documents[0].score
    assert documents[0].metadata["retrieval_profile"] == "hybrid_rerank"
    assert documents[0].metadata["retrieval_rank"] == 1
    assert documents[-1].metadata["retrieval_rank"] == 5


def test_hybrid_rerank_score_is_rerank_score_not_hybrid_score():
    client = FakeClient(
        [make_point("d0", 0.9, text="a b"), make_point("d1", 0.1, text="b")]
    )
    hybrid = make_hybrid(["a b", "b"], dense_client=client)

    def scorer(query, documents):
        return [0.5, 0.9]

    reranker = ScorerReranker(scorer=scorer, model_id="fake-reranker")
    service = make_service(
        "hybrid_rerank",
        stack=RetrievalStack(
            snapshot=make_snapshot("hybrid_rerank"),
            hybrid_retriever=hybrid,
            reranker=reranker,
        ),
    )
    documents = service.search("a")
    assert [doc.id for doc in documents] == ["d1", "d0"]
    assert documents[0].score == pytest.approx(0.9)
    assert documents[0].metadata["rerank_score"] == pytest.approx(0.9)
    assert documents[0].metadata["hybrid_score"] != documents[0].score


def test_empty_query_raises_invalid_query_error():
    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"),
            dense_retriever=make_dense(client=FakeClient([make_point("a", 0.5)])),
        ),
    )
    for query in ("", "   ", "\n", 123, None):
        with pytest.raises(InvalidQueryError):
            service.search(query)


def test_unknown_profile_raises_configuration_error():
    snapshot = make_snapshot("dense_only", active_profile="bogus_profile")
    with pytest.raises(RetrievalConfigurationError):
        RetrievalService(RetrievalStack(snapshot=snapshot))


def test_missing_required_component_raises_not_ready_error():
    with pytest.raises(ComponentNotReadyError, match="hybrid_retriever"):
        make_service(
            "hybrid_no_rerank",
            stack=RetrievalStack(snapshot=make_snapshot("hybrid_no_rerank")),
        )
    with pytest.raises(ComponentNotReadyError, match="reranker"):
        make_service(
            "hybrid_rerank",
            stack=RetrievalStack(
                snapshot=make_snapshot("hybrid_rerank"),
                hybrid_retriever=make_hybrid(["x"]),
            ),
        )


def test_embedder_failure_propagates_as_dependency_error():
    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"),
            dense_retriever=make_dense(embedder=FailingEmbedder()),
        ),
    )
    with pytest.raises(RetrievalDependencyError):
        service.search("bún bò huế")


def test_embedder_runtime_error_wraps_as_dependency_error():
    class CrashEmbedder:
        model_id = MODEL_ID

        def embed_query(self, query):
            raise RuntimeError("model backend crashed")

        def embed_documents(self, texts):
            raise RuntimeError("model backend crashed")

    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"),
            dense_retriever=make_dense(embedder=CrashEmbedder()),
        ),
    )
    with pytest.raises(RetrievalDependencyError, match="embedding failed"):
        service.search("bún bò huế")


def test_qdrant_failure_propagates_as_dependency_error():
    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"),
            dense_retriever=make_dense(client=FailingClient()),
        ),
    )
    with pytest.raises(RetrievalDependencyError):
        service.search("bún bò huế")


def test_non_finite_dense_score_rejected_as_dependency_error():
    for bad_score in (float("nan"), float("inf")):
        client = FakeClient([make_point("a", bad_score)])
        service = make_service(
            "dense_only",
            stack=RetrievalStack(
                snapshot=make_snapshot("dense_only"),
                dense_retriever=make_dense(client=client),
            ),
        )
        with pytest.raises(RetrievalDependencyError, match="non-finite"):
            service.search("bún bò huế")


def test_non_numeric_dense_score_rejected_as_dependency_error():
    for bad_score in ("malformed", None, object()):
        client = FakeClient([make_point("a", bad_score)])
        service = make_service(
            "dense_only",
            stack=RetrievalStack(
                snapshot=make_snapshot("dense_only"),
                dense_retriever=make_dense(client=client),
            ),
        )
        with pytest.raises(RetrievalDependencyError, match="non-numeric"):
            service.search("bún bò huế")


class StubDense:
    """Dense retriever stub returning the exact same captured list/objects."""

    def __init__(self, documents):
        self._documents = documents
        self.calls = 0

    def search(self, query, limit=None):
        self.calls += 1
        return self._documents


class StubHybrid:
    """Hybrid retriever stub returning the exact same captured list/objects."""

    def __init__(self, documents):
        self._documents = documents
        self.calls = 0

    def search(self, query):
        self.calls += 1
        return self._documents


def make_candidate(chunk_id, score=0.5):
    return RetrievedDocument(
        id=chunk_id,
        score=score,
        text=f"text {chunk_id}",
        metadata={
            "chunk_id": chunk_id,
            "source": "foods/restaurants/doc.md",
            "title": "Doc",
            "section": "Tóm tắt",
            "dense_score": 0.5,
        },
    )


def test_hybrid_does_not_mutate_the_same_captured_objects():
    candidates = [make_candidate("d0", 0.8), make_candidate("d1", 0.6)]
    stub = StubDense(candidates)
    hybrid = HybridRetriever(
        dense_retriever=stub,
        bm25=BM25().fit(["a b", "b"]),
        candidate_depth=30,
        top_k=10,
    )
    captured = candidates
    snapshot = [
        (doc.score, doc.text, copy.deepcopy(doc.metadata)) for doc in captured
    ]
    output = hybrid.search("a")
    after = [(doc.score, doc.text, dict(doc.metadata)) for doc in captured]
    assert after == snapshot
    assert all("hybrid_score" not in doc.metadata for doc in captured)
    # Output must be fresh result objects, not the captured instances.
    assert all(output_doc is not captured_doc for output_doc, captured_doc in zip(output, captured))
    assert [doc.id for doc in output] == ["d0", "d1"]


def test_service_does_not_mutate_the_same_captured_objects():
    documents = [make_candidate("d0"), make_candidate("d1")]
    stub = StubHybrid(documents)
    service = make_service(
        "hybrid_no_rerank",
        stack=RetrievalStack(
            snapshot=make_snapshot("hybrid_no_rerank"), hybrid_retriever=stub
        ),
    )
    captured = documents
    snapshot = [
        (doc.score, doc.text, copy.deepcopy(doc.metadata)) for doc in captured
    ]
    output = service.search("a")
    after = [(doc.score, doc.text, dict(doc.metadata)) for doc in captured]
    assert after == snapshot
    assert all("retrieval_profile" not in doc.metadata for doc in captured)
    # Output must be fresh result objects, not the captured instances.
    assert all(output_doc is not captured_doc for output_doc, captured_doc in zip(output, captured))
    assert [doc.id for doc in output] == ["d0", "d1"]
    assert all(doc.metadata["retrieval_profile"] == "hybrid_no_rerank" for doc in output)


def test_no_candidates_returns_empty_list():
    service = make_service(
        "dense_only",
        stack=RetrievalStack(
            snapshot=make_snapshot("dense_only"),
            dense_retriever=make_dense(client=FakeClient([])),
        ),
    )
    assert service.search("bún bò huế") == []


def test_hybrid_no_candidates_returns_empty_list():
    hybrid = make_hybrid(["x"], dense_client=FakeClient([]))
    service = make_service(
        "hybrid_no_rerank",
        stack=RetrievalStack(
            snapshot=make_snapshot("hybrid_no_rerank"), hybrid_retriever=hybrid
        ),
    )
    assert service.search("bún bò huế") == []
