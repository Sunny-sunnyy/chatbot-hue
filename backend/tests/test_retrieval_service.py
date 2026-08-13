"""Live tests for profile routing and score metadata on the real stack.

The retrieval stack is built by the real startup code against the ingested
test collection with the real E5 embedder and the real MiniLM reranker.
"""

import pytest

from core.schema import (
    ComponentNotReadyError,
    InvalidQueryError,
    RetrievalConfigurationError,
    RetrievalDependencyError,
)
from core.startup import RetrievalStack, build_retrieval_stack
from reranking.models.cross_encoder import CrossEncoderReranker
from retrieval.dense_retriever import DenseRetriever
from retrieval.service import RetrievalService

from conftest import TEST_COLLECTION, make_test_settings

MODEL_ID = "intfloat/multilingual-e5-small"
MINILM_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def make_live_stack(profile, real_client, real_embedder):
    settings = make_test_settings(TEST_COLLECTION, **{"active_profile": profile})
    return build_retrieval_stack(
        settings, client=real_client, embedder=real_embedder
    )


def test_dense_only_builds_only_dense_retriever(ingested_collection, real_client, real_embedder):
    stack = make_live_stack("dense_only", real_client, real_embedder)
    assert stack.dense_retriever is not None
    assert stack.hybrid_retriever is None
    assert stack.reranker is None
    assert stack.snapshot.bm25_ready is False
    assert stack.snapshot.reranker_ready is False
    assert stack.snapshot.point_count == 572
    assert stack.snapshot.embedding_model == MODEL_ID
    assert stack.snapshot.embedding_dimension == 384


def test_dense_only_search_returns_dense_scores_only(ingested_collection, real_client, real_embedder):
    """Real dense search: sorted scores and no fabricated stage metadata."""
    stack = make_live_stack("dense_only", real_client, real_embedder)
    service = RetrievalService(stack)
    documents = service.search("bún bò Huế")
    assert documents
    assert len(documents) <= 10
    scores = [doc.score for doc in documents]
    assert scores == sorted(scores, reverse=True)
    for doc in documents:
        assert doc.metadata["dense_score"] == doc.score
        assert doc.metadata["embedding_model"] == MODEL_ID
        assert doc.metadata["retrieval_profile"] == "dense_only"
        for absent in (
            "bm25_score",
            "normalized_dense_score",
            "normalized_bm25_score",
            "hybrid_score",
            "rerank_score",
            "reranker_model",
        ):
            assert absent not in doc.metadata
    assert [doc.metadata["retrieval_rank"] for doc in documents] == list(
        range(1, len(documents) + 1)
    )


def test_hybrid_no_rerank_builds_hybrid_and_fuses_real_scores(
    ingested_collection, real_client, real_embedder
):
    stack = make_live_stack("hybrid_no_rerank", real_client, real_embedder)
    assert stack.hybrid_retriever is not None
    assert stack.reranker is None
    assert stack.snapshot.bm25_ready is True
    assert len(stack.snapshot.corpus_fingerprint) == 64
    service = RetrievalService(stack)
    documents = service.search("bún bò Huế")
    assert documents
    for doc in documents:
        assert doc.metadata["hybrid_score"] == doc.score
        assert "bm25_score" in doc.metadata
        assert "normalized_dense_score" in doc.metadata
        assert "normalized_bm25_score" in doc.metadata
        assert 0.0 <= doc.metadata["normalized_dense_score"] <= 1.0
        assert 0.0 <= doc.metadata["normalized_bm25_score"] <= 1.0
        assert doc.metadata["retrieval_profile"] == "hybrid_no_rerank"
        assert "rerank_score" not in doc.metadata
        assert "reranker_model" not in doc.metadata


def test_hybrid_rerank_runs_real_minilm(ingested_collection, real_client, real_embedder):
    """The real MiniLM reranks real hybrid candidates."""
    stack = make_live_stack("hybrid_rerank", real_client, real_embedder)
    assert isinstance(stack.reranker, CrossEncoderReranker)
    assert stack.reranker.model_id == MINILM_ID
    assert stack.snapshot.reranker_ready is True
    service = RetrievalService(stack)
    documents = service.search("bún bò Huế")
    assert documents
    assert len(documents) <= 5  # rerank top_k from settings
    scores = [doc.score for doc in documents]
    assert scores == sorted(scores, reverse=True)
    for doc in documents:
        assert doc.metadata["reranker_model"] == MINILM_ID
        assert doc.metadata["rerank_score"] == doc.score
        assert doc.metadata["retrieval_profile"] == "hybrid_rerank"
        assert "hybrid_score" in doc.metadata  # hybrid stage ran first


def test_empty_query_raises_invalid_query_error(ingested_collection, real_client, real_embedder):
    service = RetrievalService(make_live_stack("dense_only", real_client, real_embedder))
    for query in ("", "   ", "\n", 123, None):
        with pytest.raises(InvalidQueryError):
            service.search(query)


def test_unknown_profile_raises_configuration_error(
    ingested_collection, real_client, real_embedder
):
    with pytest.raises(RetrievalConfigurationError):
        make_live_stack("bogus_profile", real_client, real_embedder)


def test_missing_required_component_raises_not_ready_error(
    ingested_collection, real_client, real_embedder
):
    snapshot = make_live_stack("hybrid_no_rerank", real_client, real_embedder).snapshot
    with pytest.raises(ComponentNotReadyError, match="hybrid_retriever"):
        RetrievalService(RetrievalStack(snapshot=snapshot))
    rerank_snapshot = make_live_stack("hybrid_rerank", real_client, real_embedder).snapshot
    with pytest.raises(ComponentNotReadyError, match="reranker"):
        RetrievalService(RetrievalStack(snapshot=rerank_snapshot, hybrid_retriever="x"))


def test_qdrant_network_failure_propagates_as_dependency_error(real_embedder):
    """A dead Qdrant URL reproduces the transport failure for real."""
    from vectorstore.qdrant import get_client

    dead_client = get_client("http://localhost:6399", 3)
    retriever = DenseRetriever(
        client=dead_client,
        embedder=real_embedder,
        collection_name=TEST_COLLECTION,
        top_k=10,
    )
    # The snapshot truthfully describes the wired stack.
    from core.startup import RetrievalSnapshot

    snapshot = RetrievalSnapshot(
        collection_name=TEST_COLLECTION,
        point_count=572,
        embedding_model=MODEL_ID,
        embedding_dimension=384,
        corpus_fingerprint=None,
        active_profile="dense_only",
        bm25_ready=False,
        reranker_ready=False,
        config_fingerprint="dead-url-test",
    )
    service = RetrievalService(RetrievalStack(snapshot=snapshot, dense_retriever=retriever))
    with pytest.raises(RetrievalDependencyError):
        service.search("bún bò Huế")


def test_repeated_search_is_deterministic(ingested_collection, real_client, real_embedder):
    """Two real searches over the same corpus give identical results."""
    service = RetrievalService(make_live_stack("dense_only", real_client, real_embedder))
    first = service.search("bún bò Huế")
    second = service.search("bún bò Huế")
    assert [(doc.id, doc.score) for doc in first] == [
        (doc.id, doc.score) for doc in second
    ]
