"""Tests for lexical tokenization and BM25 scoring."""
import math

import pytest

from scoring.bm25 import BM25, tokenize


def test_tokenize_keeps_vietnamese_words_and_removes_punctuation():
    assert tokenize("Bún bò Huế, ngon! Giá 35.000đ.") == [
        "bún", "bò", "huế", "ngon", "giá", "35", "000đ"
    ]


def test_bm25_known_hue_corpus_ranking_and_fit():
    corpus = ["bún bò huế đặc biệt", "cơm hến huế", "chè cung đình"]
    bm25 = BM25().fit(corpus)
    assert bm25.num_documents == 3
    assert bm25.average_document_length > 0
    scores = [bm25.score("bún bò", text) for text in corpus]
    assert all(math.isfinite(score) for score in scores)
    assert scores[0] > scores[1] == scores[2] == 0.0
    assert bm25.score("bún bò", "") == 0.0
    with pytest.raises(ValueError, match="fit"):
        BM25().score("bún bò", "bún bò huế")
