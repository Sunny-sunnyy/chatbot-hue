"""Live tests for the real local MiniLM reranker on real retrieval results.

Input documents are real dense retrieval results from the ingested test
collection. The reranker model is the real cross-encoder/ms-marco-MiniLM
loaded from cache; a missing cache is reproduced with a nonexistent model
id so the failure path stays real.
"""

import copy

import pytest

from core.schema import ComponentNotReadyError, RetrievedDocument, RetrievalDependencyError
from reranking.models.cross_encoder import CrossEncoderReranker

MODEL_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def test_reranker_reports_local_model_id():
    assert CrossEncoderReranker().model_id == MODEL_ID


def test_load_uses_real_cached_model():
    """The cached MiniLM loads and loads once per process."""
    from reranking.models import cross_encoder as module

    reranker = CrossEncoderReranker()
    reranker.load()
    entries = module._get_cross_encoder.cache_info().currsize
    reranker.load()
    assert module._get_cross_encoder.cache_info().currsize == entries


def test_load_missing_cache_fails_typed():
    """A nonexistent model id reproduces the missing-cache failure for real."""
    reranker = CrossEncoderReranker(model_id="cross-encoder/nonexistent-model-xyz")
    with pytest.raises(ComponentNotReadyError, match="cache"):
        reranker.load()


def test_empty_documents_return_empty_without_model(real_retrieved_docs):
    reranker = CrossEncoderReranker()
    assert reranker.rerank("bún bò Huế", [], top_k=5) == []


def test_real_rerank_ranks_and_truncates(real_retrieved_docs):
    """Real MiniLM scores real retrieved documents and truncates to top_k."""
    reranker = CrossEncoderReranker()
    reranker.load()
    documents = real_retrieved_docs[:5]
    result = reranker.rerank("bún bò Huế", documents, top_k=3)
    assert len(result) == 3
    ids = [doc.id for doc in result]
    assert len(ids) == len(set(ids))
    assert set(ids) <= {doc.id for doc in documents}
    scores = [doc.score for doc in result]
    assert scores == sorted(scores, reverse=True)
    for document in result:
        assert document.metadata["reranker_model"] == MODEL_ID
        assert document.metadata["rerank_score"] == document.score
        assert "dense_score" in document.metadata  # hybrid stage ran first


def test_top_k_larger_than_input_returns_all(real_retrieved_docs):
    reranker = CrossEncoderReranker()
    reranker.load()
    result = reranker.rerank("bún bò Huế", real_retrieved_docs[:2], top_k=10)
    assert len(result) == 2


def test_non_positive_top_k_raises(real_retrieved_docs):
    reranker = CrossEncoderReranker()
    for top_k in (0, -1):
        with pytest.raises(ValueError, match="positive"):
            reranker.rerank("bún bò Huế", real_retrieved_docs[:2], top_k=top_k)


def test_duplicate_input_chunk_ids_rejected_before_model(real_retrieved_docs):
    """Duplicates fail validation before the real model scores anything."""
    reranker = CrossEncoderReranker()
    documents = [real_retrieved_docs[0], real_retrieved_docs[0]]
    with pytest.raises(RetrievalDependencyError, match="duplicate chunk_id"):
        reranker.rerank("bún bò Huế", documents, top_k=5)


def test_input_missing_chunk_id_rejected(real_retrieved_docs):
    reranker = CrossEncoderReranker()
    documents = copy.deepcopy(real_retrieved_docs[:2])
    del documents[1].metadata["chunk_id"]
    with pytest.raises(RetrievalDependencyError, match="chunk_id"):
        reranker.rerank("bún bò Huế", documents, top_k=5)


def test_rerank_does_not_mutate_input(real_retrieved_docs):
    """Real reranking creates fresh outputs and leaves inputs untouched."""
    reranker = CrossEncoderReranker()
    reranker.load()
    documents = real_retrieved_docs[:5]
    snapshot = copy.deepcopy(
        [(doc.score, doc.text, dict(doc.metadata)) for doc in documents]
    )
    result = reranker.rerank("bún bò Huế", documents, top_k=3)
    after = [(doc.score, doc.text, dict(doc.metadata)) for doc in documents]
    assert after == snapshot
    assert all(output is not input_ for output, input_ in zip(result, documents))
