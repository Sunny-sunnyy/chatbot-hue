"""Behavioral tests for the deterministic TF-IDF sparse representation."""
import math

import pytest

from embedding.sparse_embedder import SparseEmbedder, tokenize


def test_tokenize_vietnamese_text():
    assert tokenize("Bún bò Huế, cà-phê (muối)!") == [
        "bún", "bò", "huế", "cà", "phê", "muối"
    ]


def test_known_tfidf_values_and_document_frequency():
    embedder = SparseEmbedder().fit(["a b a c", "b c"])
    result = embedder.encode("a a b")
    expected_a = 2 * (math.log(3 / 2) + 1)
    assert embedder.vocabulary_size == 3
    assert result["indices"] == [0, 1]
    assert result["values"] == pytest.approx([expected_a, 1.0])


def test_same_ordered_corpus_reproduces_vectors():
    corpus = ["bún bò huế", "cơm hến", "bánh ép mè xửng"]
    first = SparseEmbedder().fit(corpus)
    second = SparseEmbedder().fit(corpus)
    assert [first.encode(text) for text in corpus] == [
        second.encode(text) for text in corpus
    ]


def test_fit_again_resets_previous_state():
    embedder = SparseEmbedder().fit(["bún bò huế"])
    embedder.fit(["cơm hến"])
    assert embedder.vocabulary_size == 2
    assert embedder.num_documents == 1
    assert embedder.encode("bún") == {"indices": [], "values": []}


def test_empty_and_unknown_text_return_empty_vectors():
    embedder = SparseEmbedder().fit(["bún bò huế"])
    expected = {"indices": [], "values": []}
    assert embedder.encode("") == expected
    assert embedder.encode("phở gà") == expected


def test_encode_before_fit_is_rejected():
    with pytest.raises(ValueError, match="fit"):
        SparseEmbedder().encode("bún bò huế")
