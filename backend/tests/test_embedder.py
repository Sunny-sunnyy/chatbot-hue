"""Real behavioral tests for the local multilingual E5 embedder."""
import math

import pytest

from embedding.embedder import E5Embedder

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384


def test_empty_documents_and_invalid_queries(real_embedder):
    assert real_embedder.embed_documents([]) == []
    for query in ("", "   ", None):
        with pytest.raises(ValueError, match="query"):
            real_embedder.embed_query(query)


def test_real_document_vectors_keep_order_shape_and_norm(real_embedder):
    texts = ["Bún bò Huế", "Cơm hến", "Bánh ép mè xửng"]
    vectors = real_embedder.embed_documents(texts)
    assert real_embedder.model_id == MODEL_ID
    assert real_embedder.dimension == DIMENSION
    assert len(vectors) == len(texts)
    assert all(len(vector) == DIMENSION for vector in vectors)
    assert all(math.isfinite(value) for vector in vectors for value in vector)
    assert all(
        math.sqrt(sum(value * value for value in vector))
        == pytest.approx(1.0, abs=1e-4)
        for vector in vectors
    )
    first_alone = real_embedder.embed_documents([texts[0]])[0]
    last_alone = real_embedder.embed_documents([texts[-1]])[0]
    assert vectors[0] == pytest.approx(first_alone, abs=1e-5)
    assert vectors[-1] == pytest.approx(last_alone, abs=1e-5)


def test_query_and_document_use_distinct_real_e5_roles(real_embedder):
    text = "Bún bò Huế"
    query_vector = real_embedder.embed_query(text)
    document_vector = real_embedder.embed_documents([text])[0]
    assert len(query_vector) == DIMENSION
    assert query_vector != pytest.approx(document_vector, abs=1e-6)


def test_real_model_rejects_wrong_configured_dimension():
    embedder = E5Embedder(MODEL_ID, dimension=3, device="cpu", batch_size=64)
    with pytest.raises(ValueError, match="dimension"):
        embedder.embed_query("Bún bò Huế")
