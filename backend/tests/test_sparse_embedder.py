"""Tests for the deterministic TF-IDF-style SparseEmbedder."""
import math

import pytest

from embedding.sparse_embedder import SparseEmbedder, tokenize


def test_tokenize_lowercases_and_drops_punctuation():
    assert tokenize("Bún bò Huế, Cơm hến!") == ["bún", "bò", "huế", "cơm", "hến"]


def test_tokenize_splits_on_non_word_chars():
    assert tokenize("cà-phê (muối)") == ["cà", "phê", "muối"]
    assert tokenize("mè xửng") == ["mè", "xửng"]


def test_fit_builds_deterministic_vocabulary():
    corpus = ["Bún bò Huế", "Cơm hến bún bò"]
    first = SparseEmbedder().fit(corpus)
    second = SparseEmbedder().fit(corpus)
    assert first.vocabulary_size == 5
    assert first.encode("bún")["indices"] == second.encode("bún")["indices"]


def test_tfidf_values_on_small_known_corpus():
    corpus = ["a b a c", "b c"]
    embedder = SparseEmbedder().fit(corpus)
    result = embedder.encode("a a b")
    # df(a)=1, df(b)=2, num_documents=2
    idf_a = math.log((2 + 1) / (1 + 1)) + 1
    assert result["indices"] == [0, 1]
    assert result["values"] == pytest.approx([2 * idf_a, 1.0])
    assert result["values"][0] > result["values"][1]


def test_document_frequency_counts_once_per_document():
    embedder = SparseEmbedder().fit(["a a", "b"])
    # Even though "a" appears twice in one document, df(a) is 1.
    result = embedder.encode("a a")
    assert result["values"] == pytest.approx([2 * (math.log(3 / 2) + 1)])
    assert result["indices"] == [0]


def test_unknown_tokens_are_ignored():
    embedder = SparseEmbedder().fit(["bún bò huế"])
    result = embedder.encode("phở gà")
    assert result == {"indices": [], "values": []}


def test_empty_text_returns_empty_lists():
    embedder = SparseEmbedder().fit(["bún bò huế"])
    assert embedder.encode("") == {"indices": [], "values": []}
    assert embedder.encode("   ") == {"indices": [], "values": []}


def test_encode_before_fit_rejected():
    with pytest.raises(ValueError, match="fit"):
        SparseEmbedder().encode("bún bò huế")


def test_fit_twice_resets_state():
    corpus_a = ["bún bò huế"]
    corpus_b = ["cơm hến"]
    embedder = SparseEmbedder().fit(corpus_a)
    assert embedder.encode("bún")["indices"] == [0]
    embedder.fit(corpus_b)
    # Vocabulary was reset: "bún" is unknown and its old index is gone.
    assert embedder.encode("bún") == {"indices": [], "values": []}
    assert embedder.vocabulary_size == 2
    assert embedder.num_documents == 1


def test_output_invariants():
    corpus = ["bún bò huế mè xửng", "cơm hến bánh ép", "chè heo quay"]
    embedder = SparseEmbedder().fit(corpus)
    result = embedder.encode("bún bò bò huế")
    indices, values = result["indices"], result["values"]
    assert len(indices) == len(values)
    assert len(indices) == len(set(indices))
    assert all(isinstance(i, int) for i in indices)
    assert all(math.isfinite(v) and v > 0 for v in values)


def test_num_documents_tracks_corpus_size():
    embedder = SparseEmbedder().fit(["a", "b", "c"])
    assert embedder.num_documents == 3


def test_same_corpus_reproduces_same_vectors():
    corpus = ["bún bò huế", "cơm hến", "bánh ép mè xửng"]
    first = SparseEmbedder().fit(corpus)
    second = SparseEmbedder().fit(corpus)
    for text in corpus + ["bún", "cơm hến bánh ép"]:
        assert first.encode(text) == second.encode(text)
