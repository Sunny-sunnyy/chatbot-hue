"""Tests for reranker invariants: counts, finiteness, purity and ties."""
import copy

import pytest

from core.schema import ComponentNotReadyError, RetrievedDocument, RetrievalDependencyError
from reranking.models import cross_encoder
from reranking.models.cross_encoder import CrossEncoderReranker
from reranking.reranker import ScorerReranker

MODEL_ID = "fake-reranker"


def make_docs(*chunk_ids):
    return [
        RetrievedDocument(
            id=chunk_id,
            score=0.0,
            text=f"text {chunk_id}",
            metadata={
                "chunk_id": chunk_id,
                "source": "foods/restaurants/doc.md",
                "title": "Doc",
                "section": "Tóm tắt",
            },
        )
        for chunk_id in chunk_ids
    ]


def make_reranker(scores):
    calls = []

    def scorer(query, documents):
        calls.append(query)
        return scores

    return ScorerReranker(scorer=scorer, model_id=MODEL_ID), calls


def test_empty_documents_return_empty_without_calling_scorer():
    def scorer(query, documents):
        raise AssertionError("scorer must not run for empty input")

    reranker = ScorerReranker(scorer=scorer, model_id=MODEL_ID)
    assert reranker.rerank("bún bò huế", [], top_k=5) == []


def test_score_count_mismatch_raises_dependency_error():
    reranker, _ = make_reranker([1.0])
    with pytest.raises(RetrievalDependencyError, match="for 3 documents"):
        reranker.rerank("bún bò huế", make_docs("a", "b", "c"), top_k=5)


def test_non_finite_score_raises_dependency_error():
    reranker, _ = make_reranker([1.0, float("nan")])
    with pytest.raises(RetrievalDependencyError, match="non-finite"):
        reranker.rerank("bún bò huế", make_docs("a", "b"), top_k=5)


def test_non_numeric_scores_raise_dependency_error():
    for bad_scores in ([1.0, "malformed"], [1.0, None], [1.0, object()]):
        reranker, _ = make_reranker(bad_scores)
        with pytest.raises(RetrievalDependencyError, match="non-numeric"):
            reranker.rerank("bún bò huế", make_docs("a", "b"), top_k=5)


def test_numeric_string_scores_are_converted():
    reranker, _ = make_reranker(["0.9", "0.5"])
    result = reranker.rerank("bún bò huế", make_docs("a", "b"), top_k=5)
    assert result[0].score == pytest.approx(0.9)
    assert result[1].score == pytest.approx(0.5)


def test_scorer_runtime_failure_wraps_as_dependency_error():
    def scorer(query, documents):
        raise RuntimeError("model backend crashed")

    reranker = ScorerReranker(scorer=scorer, model_id=MODEL_ID)
    with pytest.raises(RetrievalDependencyError, match="scoring failed"):
        reranker.rerank("bún bò huế", make_docs("a", "b"), top_k=5)


def test_output_only_contains_input_documents_without_duplicates():
    reranker, _ = make_reranker([0.5, 0.9, 0.1, 0.7, 0.3, 0.8, 0.2, 0.6, 0.4, 0.0])
    input_ids = [f"d{i:02d}" for i in range(10)]
    result = reranker.rerank("bún bò huế", make_docs(*input_ids), top_k=5)
    result_ids = [doc.id for doc in result]
    assert len(result_ids) == len(set(result_ids)) == 5
    assert set(result_ids) <= set(input_ids)


def test_duplicate_input_chunk_ids_are_rejected_before_scorer():
    def scorer(query, documents):
        raise AssertionError("scorer must not run for duplicate input")

    reranker = ScorerReranker(scorer=scorer, model_id=MODEL_ID)
    with pytest.raises(RetrievalDependencyError, match="duplicate chunk_id"):
        reranker.rerank("bún bò huế", make_docs("a", "a", "b"), top_k=5)


def test_input_missing_chunk_id_is_rejected():
    reranker, _ = make_reranker([0.5, 0.9])
    documents = make_docs("a", "b")
    del documents[1].metadata["chunk_id"]
    with pytest.raises(RetrievalDependencyError, match="chunk_id"):
        reranker.rerank("bún bò huế", documents, top_k=5)


def test_rerank_does_not_mutate_input_list_or_metadata():
    reranker, _ = make_reranker([0.5, 0.9])
    documents = make_docs("a", "b")
    snapshot = copy.deepcopy(
        [(doc.score, doc.text, dict(doc.metadata)) for doc in documents]
    )
    reranker.rerank("bún bò huế", documents, top_k=5)
    after = [(doc.score, doc.text, dict(doc.metadata)) for doc in documents]
    assert after == snapshot


def test_ties_break_by_chunk_id_ascending():
    reranker, _ = make_reranker([1.0, 1.0, 0.5])
    result = reranker.rerank("bún bò huế", make_docs("b", "a", "c"), top_k=5)
    assert [doc.id for doc in result] == ["a", "b", "c"]


def test_top_k_truncates_output():
    reranker, _ = make_reranker([float(10 - i) for i in range(10)])
    result = reranker.rerank("bún bò huế", make_docs(*[f"d{i}" for i in range(10)]), top_k=5)
    assert len(result) == 5
    assert result[0].score == pytest.approx(10.0)


def test_top_k_larger_than_input_returns_all():
    reranker, _ = make_reranker([0.5, 0.9])
    result = reranker.rerank("bún bò huế", make_docs("a", "b"), top_k=10)
    assert len(result) == 2


def test_non_positive_top_k_raises():
    reranker, _ = make_reranker([0.5, 0.9])
    for top_k in (0, -1):
        with pytest.raises(ValueError, match="positive"):
            reranker.rerank("bún bò huế", make_docs("a", "b"), top_k=top_k)


def test_output_metadata_carries_reranker_model_and_score():
    reranker, _ = make_reranker([0.9, 0.5])
    result = reranker.rerank("bún bò huế", make_docs("a", "b"), top_k=5)
    assert result[0].metadata["reranker_model"] == MODEL_ID
    assert result[0].metadata["rerank_score"] == pytest.approx(0.9)
    assert result[0].score == pytest.approx(0.9)
    assert "dense_score" not in result[0].metadata


def test_cross_encoder_reranker_reports_local_model_id():
    reranker = CrossEncoderReranker()
    assert reranker.model_id == "cross-encoder/ms-marco-MiniLM-L-6-v2"


def test_cross_encoder_load_verifies_cache_and_fails_typed(monkeypatch):
    def fail_load(model_id, device):
        raise OSError("cache missing")

    monkeypatch.setattr(cross_encoder, "_get_cross_encoder", fail_load)
    reranker = CrossEncoderReranker()
    with pytest.raises(ComponentNotReadyError, match="cache"):
        reranker.load()


def test_cross_encoder_load_caches_once_and_forces_local_files_only(monkeypatch):
    calls = []

    class FakeCrossEncoder:
        def __init__(self, model_id, device, local_files_only=False):
            calls.append((model_id, device, local_files_only))

        def predict(self, pairs, **kwargs):
            return [1.0] * len(pairs)

    monkeypatch.setattr("sentence_transformers.CrossEncoder", FakeCrossEncoder)
    cross_encoder._get_cross_encoder.cache_clear()
    try:
        reranker = CrossEncoderReranker()
        reranker.load()
        reranker.load()
        assert calls == [("cross-encoder/ms-marco-MiniLM-L-6-v2", "cpu", True)]
    finally:
        cross_encoder._get_cross_encoder.cache_clear()
