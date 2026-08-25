"""Live tests for profile routing, score metadata and startup service composition.

The retrieval service is built by the real startup code against the ingested
test collection with the real E5 embedder and the real MiniLM reranker.
"""
import copy
import math

import pytest

from conftest import TEST_COLLECTION, make_test_settings
from core.schema import (
    InvalidQueryError,
    RetrievalConfigurationError,
    RetrievalDependencyError,
)
from core.startup import build_retrieval_service
from reranking.cross_encoder import CrossEncoderReranker

MODEL_ID = "intfloat/multilingual-e5-small"
MINILM_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def make_live_service(profile, real_client, real_embedder):
    settings = make_test_settings(TEST_COLLECTION, **{"active_profile": profile})
    return build_retrieval_service(
        settings, client=real_client, embedder=real_embedder
    )


def test_cross_encoder_rerank_contract_and_non_mutation(real_retrieved_docs):
    reranker = CrossEncoderReranker()
    documents = real_retrieved_docs[:5]
    before = copy.deepcopy([(d.id, d.score, d.text, d.metadata) for d in documents])
    result = reranker.rerank("bún bò Huế", documents, top_k=3)
    assert len(result) == 3
    assert all(math.isfinite(doc.score) for doc in result)
    assert [doc.score for doc in result] == sorted((doc.score for doc in result), reverse=True)
    assert all(doc.metadata["reranker_model"] == MINILM_ID for doc in result)
    assert [(d.id, d.score, d.text, d.metadata) for d in documents] == before


def test_dense_only_builds_only_required_runtime(
    ingested_collection, real_client, real_embedder
):
    service = make_live_service("dense_only", real_client, real_embedder)
    assert service.status.active_profile == "dense_only"
    assert service.status.bm25_ready is False
    assert service.status.reranker_ready is False
    assert service.status.point_count == 572
    assert service.status.embedding_model == MODEL_ID
    assert service.status.embedding_dimension == 384
    documents = service.search("bún bò Huế")
    assert documents
    assert all("bm25_score" not in doc.metadata for doc in documents)


def test_dense_only_search_returns_dense_scores_only(
    ingested_collection, real_client, real_embedder
):
    """Real dense search: sorted scores and no fabricated stage metadata."""
    service = make_live_service("dense_only", real_client, real_embedder)
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


def test_hybrid_no_rerank_runs_dense_then_python_bm25(
    ingested_collection, real_client, real_embedder
):
    service = make_live_service("hybrid_no_rerank", real_client, real_embedder)
    assert service.status.bm25_ready is True
    assert service.status.reranker_ready is False
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


def test_hybrid_rerank_runs_dense_bm25_then_real_minilm(
    ingested_collection, real_client, real_embedder
):
    """The real MiniLM reranks real hybrid candidates."""
    service = make_live_service("hybrid_rerank", real_client, real_embedder)
    assert service.status.bm25_ready is True
    assert service.status.reranker_ready is True
    documents = service.search("bún bò Huế")
    assert documents
    assert 1 <= len(documents) <= 5  # rerank top_k from settings
    scores = [doc.score for doc in documents]
    assert scores == sorted(scores, reverse=True)
    for doc in documents:
        assert doc.metadata["reranker_model"] == MINILM_ID
        assert doc.metadata["rerank_score"] == doc.score
        assert doc.metadata["retrieval_profile"] == "hybrid_rerank"
        assert "hybrid_score" in doc.metadata  # hybrid stage ran first


def test_empty_query_raises_invalid_query_error(
    ingested_collection, real_client, real_embedder
):
    service = make_live_service("dense_only", real_client, real_embedder)
    for query in ("", "   ", "\n", 123, None):
        with pytest.raises(InvalidQueryError):
            service.search(query)


def test_unknown_profile_raises_configuration_error(
    ingested_collection, real_client, real_embedder
):
    with pytest.raises(RetrievalConfigurationError):
        make_live_service("bogus_profile", real_client, real_embedder)


def test_repeated_real_search_is_deterministic(
    ingested_collection, real_client, real_embedder
):
    """Two real searches over the same corpus give identical results."""
    service = make_live_service("dense_only", real_client, real_embedder)
    first = service.search("bún bò Huế")
    second = service.search("bún bò Huế")
    assert [(doc.id, doc.score) for doc in first] == [
        (doc.id, doc.score) for doc in second
    ]
