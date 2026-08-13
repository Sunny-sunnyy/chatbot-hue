"""Live tests for point building and validation on real pipeline artifacts.

Dense vectors come from the real E5 embedder and sparse vectors from the
real TF-IDF-style SparseEmbedder fitted on the curated corpus. Invalid-input
guard tests corrupt real artifacts to exercise the validation contracts.
"""

import math
import uuid

import pytest

from embedding.sparse_embedder import SparseEmbedder
from vectorstore.hybrid_index import (
    build_points,
    point_id_for,
    validate_chunks,
    validate_vectors,
)

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384


def real_vectors(chunks, embedder):
    """Real dense + sparse vectors for the given curated chunks."""
    texts = [chunk["text"] for chunk in chunks]
    sparse = SparseEmbedder().fit(texts)
    dense = embedder.embed_documents(texts)
    return dense, [sparse.encode(text) for text in texts]


def test_point_id_is_deterministic_uuid5(real_chunks):
    chunk_id = real_chunks[0]["metadata"]["chunk_id"]
    expected = uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}")
    assert point_id_for(chunk_id) == expected
    assert point_id_for(chunk_id) == point_id_for(chunk_id)
    assert point_id_for(chunk_id) != point_id_for(real_chunks[1]["metadata"]["chunk_id"])


def test_validate_chunks_returns_ids_in_order(real_chunks):
    first, second = real_chunks[:2]
    assert validate_chunks([first, second]) == [
        first["metadata"]["chunk_id"],
        second["metadata"]["chunk_id"],
    ]


def test_validate_chunks_rejects_missing_or_empty_id(real_chunks):
    chunk = dict(real_chunks[0])
    chunk["metadata"] = {**chunk["metadata"], "chunk_id": None}
    with pytest.raises(ValueError, match="chunk_id"):
        validate_chunks([chunk])
    chunk["metadata"] = {**chunk["metadata"], "chunk_id": ""}
    with pytest.raises(ValueError, match="chunk_id"):
        validate_chunks([chunk])
    chunk["metadata"] = {}
    with pytest.raises(ValueError, match="chunk_id"):
        validate_chunks([chunk])


def test_validate_chunks_rejects_duplicate_ids(real_chunks):
    chunk = real_chunks[0]
    with pytest.raises(ValueError, match="duplicate"):
        validate_chunks([chunk, chunk])


def test_validate_chunks_rejects_empty_corpus():
    with pytest.raises(ValueError, match="no chunks"):
        validate_chunks([])


def test_validate_vectors_rejects_count_mismatch(real_chunks, real_embedder):
    chunks = real_chunks[:2]
    dense, sparse = real_vectors(chunks, real_embedder)
    with pytest.raises(ValueError, match="dense vector count"):
        validate_vectors(dense[:1], sparse, 2, DIMENSION)
    with pytest.raises(ValueError, match="sparse vector count"):
        validate_vectors(dense, sparse[:1], 2, DIMENSION)


def test_validate_vectors_rejects_dimension_mismatch(real_chunks, real_embedder):
    dense, sparse = real_vectors(real_chunks[:1], real_embedder)
    with pytest.raises(ValueError, match="dimension"):
        validate_vectors(dense, sparse, 1, 8)


def test_validate_vectors_rejects_non_finite_dense(real_chunks, real_embedder):
    """A corrupted real vector must be rejected by the finite guard."""
    dense, sparse = real_vectors(real_chunks[:1], real_embedder)
    corrupted = [list(dense[0])]
    corrupted[0][0] = float("nan")
    with pytest.raises(ValueError, match="non-finite"):
        validate_vectors(corrupted, sparse, 1, DIMENSION)
    corrupted[0][0] = float("inf")
    with pytest.raises(ValueError, match="non-finite"):
        validate_vectors(corrupted, sparse, 1, DIMENSION)


def test_validate_vectors_rejects_corrupt_sparse(real_chunks, real_embedder):
    """Corrupted sparse shapes are rejected by the shape guards."""
    dense, sparse = real_vectors(real_chunks[:1], real_embedder)
    with pytest.raises(ValueError, match="indices"):
        validate_vectors(dense, [{"indices": [1, 7], "values": [1.3]}], 1, DIMENSION)
    with pytest.raises(ValueError, match="indices"):
        validate_vectors(dense, [{"indices": [1.5], "values": [1.3]}], 1, DIMENSION)
    with pytest.raises(ValueError, match="indices"):
        validate_vectors(dense, [{"indices": [-1], "values": [1.3]}], 1, DIMENSION)
    with pytest.raises(ValueError, match="indices and values"):
        validate_vectors(dense, [{"values": [1.3]}], 1, DIMENSION)


def test_validate_vectors_rejects_non_finite_sparse(real_chunks, real_embedder):
    dense, sparse = real_vectors(real_chunks[:1], real_embedder)
    with pytest.raises(ValueError, match="non-finite"):
        validate_vectors(dense, [{"indices": [1], "values": [float("nan")]}], 1, DIMENSION)


def test_build_points_exact_payload_fields(real_chunks, real_embedder):
    """Real E5 + real sparse vectors produce the exact live payload contract."""
    chunk = real_chunks[0]
    dense, sparse = real_vectors([chunk], real_embedder)
    point = build_points([chunk], dense, sparse, MODEL_ID, DIMENSION)[0]
    assert point["id"] == point_id_for(chunk["metadata"]["chunk_id"])
    assert set(point["vector"]) == {"dense", "sparse"}
    assert point["vector"]["sparse"] == sparse[0]
    assert len(point["vector"]["dense"]) == DIMENSION
    assert all(math.isfinite(value) for value in point["vector"]["dense"])
    assert point["payload"] == {
        "text": chunk["text"],
        "chunk_id": chunk["metadata"]["chunk_id"],
        "source": chunk["metadata"]["source"],
        "title": chunk["metadata"]["title"],
        "section": chunk["metadata"]["section"],
        "category": chunk["metadata"]["category"],
        "subcategory": chunk["metadata"]["subcategory"],
        "chunk_type": chunk["metadata"]["chunk_type"],
        "embedding_model": MODEL_ID,
        "embedding_dimension": DIMENSION,
    }


def test_build_points_keeps_order_and_validates_lengths_first(
    real_chunks, real_embedder
):
    chunks = real_chunks[:2]
    dense, sparse = real_vectors(chunks, real_embedder)
    points = build_points(chunks, dense, sparse, MODEL_ID, DIMENSION)
    assert [p["payload"]["chunk_id"] for p in points] == [
        chunks[0]["metadata"]["chunk_id"],
        chunks[1]["metadata"]["chunk_id"],
    ]
    # Short dense list must fail before any zip-based truncation.
    with pytest.raises(ValueError, match="dense vector count"):
        build_points(chunks, dense[:1], sparse, MODEL_ID, DIMENSION)


def test_real_vectors_are_valid_by_the_runtime_contract(real_chunks, real_embedder):
    """The real E5/sparse outputs pass validate_vectors unchanged."""
    dense, sparse = real_vectors(real_chunks[:5], real_embedder)
    validate_vectors(dense, sparse, 5, DIMENSION)
