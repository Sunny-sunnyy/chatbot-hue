"""Tests for corpus-scoped BM25, min-max normalization and weight validation."""
import math

import pytest

from scoring.bm25 import BM25, min_max_normalize, validate_weights

CORPUS = ["a b c", "a b", "b"]


def reference_bm25(term, document, corpus, k1=1.5, b=0.75):
    """Reference BM25 formula used to anchor the implementation exactly."""
    documents = [doc.split() for doc in corpus]
    num_documents = len(documents)
    average_length = sum(len(doc) for doc in documents) / num_documents
    document_frequency = sum(1 for doc in documents if term in doc)
    idf = math.log((num_documents - document_frequency + 0.5) / (document_frequency + 0.5) + 1.0)
    term_frequency = document.split().count(term)
    length = len(document.split())
    denominator = term_frequency + k1 * (1.0 - b + b * length / average_length)
    return idf * (term_frequency * (k1 + 1.0)) / denominator


def test_bm25_fit_statistics():
    bm25 = BM25().fit(CORPUS)
    assert bm25.num_documents == 3
    assert bm25.average_document_length == pytest.approx(2.0)


def test_bm25_average_length_counts_non_empty_documents_only():
    bm25 = BM25().fit(["a b c", "a b", "b", "", "   "])
    assert bm25.num_documents == 3
    assert bm25.average_document_length == pytest.approx(2.0)


def test_bm25_score_matches_reference_formula():
    bm25 = BM25().fit(CORPUS)
    assert bm25.score("a", "a b c") == pytest.approx(
        reference_bm25("a", "a b c", CORPUS)
    )
    assert bm25.score("b", "a b") == pytest.approx(
        reference_bm25("b", "a b", CORPUS)
    )


def test_bm25_known_corpus_ranking():
    bm25 = BM25().fit(CORPUS)
    assert bm25.score("a b", "a b") > bm25.score("a b", "a b c") > bm25.score("a b", "b")
    assert bm25.score("a", "b") == pytest.approx(0.0)


def test_bm25_query_terms_are_deduplicated():
    bm25 = BM25().fit(CORPUS)
    assert bm25.score("a a b", "a b c") == bm25.score("a b", "a b c")


def test_bm25_out_of_vocabulary_term_contributes_zero():
    bm25 = BM25().fit(CORPUS)
    assert bm25.score("a zzz", "a b c") == bm25.score("a", "a b c")


def test_bm25_empty_document_scores_zero():
    bm25 = BM25().fit(CORPUS)
    assert bm25.score("a b", "") == pytest.approx(0.0)


def test_bm25_score_before_fit_raises():
    with pytest.raises(ValueError, match="fit"):
        BM25().score("a", "a b c")


def test_bm25_fit_all_empty_corpus_raises():
    with pytest.raises(ValueError, match="non-empty"):
        BM25().fit(["", "  "])


def test_bm25_refit_resets_state():
    bm25 = BM25().fit(CORPUS)
    first = bm25.score("a", "a b c")
    bm25.fit(["x y z"])
    assert bm25.num_documents == 1
    assert bm25.average_document_length == pytest.approx(3.0)
    assert bm25.score("a", "a b c") != first


def test_bm25_score_is_finite():
    bm25 = BM25().fit(CORPUS)
    assert math.isfinite(bm25.score("a b", "a b c"))


def test_min_max_normalize_normal_case():
    assert min_max_normalize([3, 1, 2]) == [1.0, 0.0, 0.5]


def test_min_max_normalize_constant_signal_maps_to_zero():
    assert min_max_normalize([5, 5, 5]) == [0.0, 0.0, 0.0]


def test_min_max_normalize_empty_input():
    assert min_max_normalize([]) == []


def test_min_max_normalize_rejects_non_finite():
    with pytest.raises(ValueError, match="non-finite"):
        min_max_normalize([1.0, float("nan")])


def test_validate_weights_accepts_baseline():
    assert validate_weights(0.6, 0.4) == (0.6, 0.4)
    assert validate_weights(0.5, 0.5) == (0.5, 0.5)


def test_validate_weights_rejects_negative():
    with pytest.raises(ValueError, match="non-negative"):
        validate_weights(-0.1, 1.1)


def test_validate_weights_rejects_wrong_sum():
    with pytest.raises(ValueError, match="sum"):
        validate_weights(0.8, 0.3)


def test_validate_weights_rejects_non_finite():
    with pytest.raises(ValueError, match="finite"):
        validate_weights(float("nan"), 1.0)
    with pytest.raises(ValueError, match="finite"):
        validate_weights(1.0, float("inf"))
