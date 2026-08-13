"""Live tests for the real local E5 embedder and the OpenRouter adapter.

The local embedder runs the real intfloat/multilingual-e5-small model from
cache. OpenRouter adapter tests are limited to behavior verifiable without
a live OpenRouter call: constructor validation, missing-key failure and
the empty-batch skip (no network is ever reached).
"""

import math

import pytest

from embedding.batch_embed import embed_in_batches
from embedding.embedder import (
    DOCUMENT_PREFIX,
    QUERY_PREFIX,
    SentenceTransformerEmbedder,
)
from embedding.openrouter_embedder import OpenRouterEmbedder
from embedding.base import EmbeddingError

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384


def test_empty_documents_skip_model(real_embedder):
    """Embedding nothing must not load or run the real model."""
    from embedding import embedder as module

    before = module._get_model.cache_info().currsize
    assert real_embedder.embed_documents([]) == []
    assert module._get_model.cache_info().currsize == before


def test_embed_documents_returns_one_vector_per_text_in_order(real_embedder):
    """Three real texts produce three real vectors matching solo embeds."""
    vectors = real_embedder.embed_documents(
        ["Bún bò Huế", "Cơm hến", "Bánh ép mè xửng"]
    )
    assert len(vectors) == 3
    for vector in vectors:
        assert len(vector) == DIMENSION
        assert all(math.isfinite(value) for value in vector)
    first_solo = real_embedder.embed_documents(["Bún bò Huế"])[0]
    third_solo = real_embedder.embed_documents(["Bánh ép mè xửng"])[0]
    assert vectors[0] == pytest.approx(first_solo, abs=1e-5)
    assert vectors[2] == pytest.approx(third_solo, abs=1e-5)


def test_vectors_are_l2_normalized(real_embedder):
    vector = real_embedder.embed_query("Bún bò Huế")
    norm = math.sqrt(sum(value * value for value in vector))
    assert norm == pytest.approx(1.0, abs=1e-4)


def test_dimension_mismatch_fails_fast(real_embedder):
    embedder = SentenceTransformerEmbedder(MODEL_ID, dimension=3)
    with pytest.raises(EmbeddingError, match="dimension"):
        embedder.embed_query("Bún bò Huế")


def test_custom_prefixes_change_the_real_embeddings(real_embedder):
    """Different E5 prefixes feed different real model inputs."""
    default = real_embedder.embed_documents(["Bún bò Huế"])[0]
    custom = SentenceTransformerEmbedder(
        MODEL_ID, DIMENSION, document_prefix="doc: ", query_prefix="q: "
    )
    changed = custom.embed_documents(["Bún bò Huế"])[0]
    assert changed != pytest.approx(default, abs=1e-6)
    assert DOCUMENT_PREFIX == "passage: "
    assert QUERY_PREFIX == "query: "


def test_empty_and_whitespace_query_rejected(real_embedder):
    with pytest.raises(EmbeddingError):
        real_embedder.embed_query("")
    with pytest.raises(EmbeddingError):
        real_embedder.embed_query("   ")


def test_model_cached_once_per_process(real_embedder):
    """Two embedder instances share one real model in the process cache."""
    from embedding import embedder as module

    other = SentenceTransformerEmbedder(MODEL_ID, DIMENSION)
    real_embedder.embed_documents(["x"])
    other.embed_documents(["y"])
    assert module._get_model.cache_info().currsize == 1


def test_model_id_and_dimension_exposed(real_embedder):
    assert real_embedder.model_id == MODEL_ID
    assert real_embedder.dimension == DIMENSION


def test_embed_in_batches_with_real_embedder(real_embedder):
    """Batched real embedding returns one normalized vector per text.

    Batch boundaries introduce small float noise from the real BLAS
    kernels, so equivalence with a single batch is checked at 1e-3.
    """
    texts = ["Bún bò Huế", "Cơm hến", "Bánh ép", "Mè xửng", "Chè heo quay"]
    vectors = embed_in_batches(real_embedder, texts, batch_size=2)
    assert len(vectors) == 5
    for vector in vectors:
        assert len(vector) == DIMENSION
        assert all(math.isfinite(value) for value in vector)
        norm = math.sqrt(sum(value * value for value in vector))
        assert norm == pytest.approx(1.0, abs=1e-3)
    solo = real_embedder.embed_documents(texts)
    for got, want in zip(vectors, solo):
        assert got == pytest.approx(want, abs=1e-3)


def test_embed_in_batches_empty_input(real_embedder):
    assert embed_in_batches(real_embedder, [], batch_size=2) == []


def test_embed_in_batches_rejects_invalid_batch_size(real_embedder):
    with pytest.raises(ValueError):
        embed_in_batches(real_embedder, ["t0"], batch_size=0)


# --- OpenRouter adapter: behavior verifiable without a live provider call ---

def test_openrouter_constructor_validation():
    with pytest.raises(EmbeddingError, match="batch_size"):
        OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION, batch_size=0)
    with pytest.raises(EmbeddingError, match="batch_size"):
        OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION, batch_size=-3)
    with pytest.raises(EmbeddingError, match="timeout"):
        OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION, timeout=0)
    with pytest.raises(EmbeddingError, match="max_retries"):
        OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION, max_retries=-1)


def test_openrouter_empty_batch_skips_network():
    embedder = OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION)
    assert embedder.embed_documents([]) == []


def test_openrouter_missing_api_key_fails_before_request(monkeypatch):
    """Without OPENROUTER_API_KEY the adapter fails before any POST."""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    embedder = OpenRouterEmbedder("qwen/qwen3-embedding-0.6b", DIMENSION)
    with pytest.raises(EmbeddingError, match="OPENROUTER_API_KEY"):
        embedder.embed_documents(["a"])
