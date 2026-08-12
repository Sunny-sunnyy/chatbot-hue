"""Tests for deterministic point building and validation in hybrid_index."""
import math
import uuid

import pytest

from vectorstore.hybrid_index import (
    build_points,
    point_id_for,
    validate_chunks,
    validate_vectors,
)

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384


def _chunk(chunk_id="foods/restaurants/example.md|Tóm tắt|0", text="Nội dung mẫu"):
    return {
        "text": text,
        "metadata": {
            "chunk_id": chunk_id,
            "source": "foods/restaurants/example.md",
            "title": "Example",
            "section": "Tóm tắt",
            "category": "foods",
            "subcategory": "restaurants",
            "chunk_type": "section",
        },
    }


def _dense(count=1, dimension=DIMENSION):
    return [[1.0 / math.sqrt(dimension)] * dimension for _ in range(count)]


def _sparse(count=1):
    return [{"indices": [1, 7], "values": [1.3, 2.1]} for _ in range(count)]


def test_point_id_is_deterministic_uuid5():
    chunk_id = "foods/restaurants/example.md|Tóm tắt|0"
    expected = uuid.uuid5(uuid.NAMESPACE_URL, f"hue-rag:{chunk_id}")
    assert point_id_for(chunk_id) == expected
    assert point_id_for(chunk_id) == expected
    assert point_id_for(chunk_id) != point_id_for("foods/cafes/other.md|Tóm tắt|0")


def test_validate_chunks_returns_ids_in_order():
    chunks = [_chunk("a|S|0"), _chunk("b|S|0")]
    assert validate_chunks(chunks) == ["a|S|0", "b|S|0"]


def test_validate_chunks_rejects_missing_or_empty_id():
    with pytest.raises(ValueError, match="chunk_id"):
        validate_chunks([_chunk(chunk_id=None)])
    with pytest.raises(ValueError, match="chunk_id"):
        validate_chunks([_chunk(chunk_id="")])
    with pytest.raises(ValueError, match="chunk_id"):
        validate_chunks([{"text": "x", "metadata": {}}])


def test_validate_chunks_rejects_duplicate_ids():
    with pytest.raises(ValueError, match="duplicate"):
        validate_chunks([_chunk("a|S|0"), _chunk("a|S|0")])


def test_validate_chunks_rejects_empty_corpus():
    with pytest.raises(ValueError, match="no chunks"):
        validate_chunks([])


def test_validate_vectors_rejects_count_mismatch():
    chunks = [_chunk("a|S|0"), _chunk("b|S|0")]
    with pytest.raises(ValueError, match="dense vector count"):
        validate_vectors(_dense(1), _sparse(2), 2, DIMENSION)
    with pytest.raises(ValueError, match="sparse vector count"):
        validate_vectors(_dense(2), _sparse(1), 2, DIMENSION)


def test_validate_vectors_rejects_dimension_mismatch():
    with pytest.raises(ValueError, match="dimension"):
        validate_vectors(_dense(1, dimension=8), _sparse(1), 1, DIMENSION)


def test_validate_vectors_rejects_non_finite_dense():
    with pytest.raises(ValueError, match="non-finite"):
        validate_vectors([[float("nan")] * DIMENSION], _sparse(1), 1, DIMENSION)
    with pytest.raises(ValueError, match="non-finite"):
        validate_vectors([[float("inf")] * DIMENSION], _sparse(1), 1, DIMENSION)


def test_validate_vectors_rejects_sparse_shape_mismatch():
    with pytest.raises(ValueError, match="indices"):
        validate_vectors(_dense(1), [{"indices": [1, 7], "values": [1.3]}], 1, DIMENSION)
    with pytest.raises(ValueError, match="indices"):
        validate_vectors(_dense(1), [{"indices": [1.5], "values": [1.3]}], 1, DIMENSION)
    with pytest.raises(ValueError, match="indices"):
        validate_vectors(_dense(1), [{"indices": [-1], "values": [1.3]}], 1, DIMENSION)
    with pytest.raises(ValueError, match="indices and values"):
        validate_vectors(_dense(1), [{"values": [1.3]}], 1, DIMENSION)


def test_validate_vectors_rejects_non_finite_sparse():
    with pytest.raises(ValueError, match="non-finite"):
        validate_vectors(_dense(1), [{"indices": [1], "values": [float("nan")]}], 1, DIMENSION)


def test_build_points_exact_payload_fields():
    chunk = _chunk()
    point = build_points([chunk], _dense(1), _sparse(1), MODEL_ID, DIMENSION)[0]
    assert point["id"] == point_id_for(chunk["metadata"]["chunk_id"])
    assert set(point["vector"]) == {"dense", "sparse"}
    assert point["vector"]["sparse"] == {"indices": [1, 7], "values": [1.3, 2.1]}
    assert point["payload"] == {
        "text": "Nội dung mẫu",
        "chunk_id": "foods/restaurants/example.md|Tóm tắt|0",
        "source": "foods/restaurants/example.md",
        "title": "Example",
        "section": "Tóm tắt",
        "category": "foods",
        "subcategory": "restaurants",
        "chunk_type": "section",
        "embedding_model": MODEL_ID,
        "embedding_dimension": DIMENSION,
    }


def test_build_points_keeps_order_and_validates_lengths_first():
    chunks = [_chunk("a|S|0"), _chunk("b|S|0")]
    points = build_points(chunks, _dense(2), _sparse(2), MODEL_ID, DIMENSION)
    assert [p["payload"]["chunk_id"] for p in points] == ["a|S|0", "b|S|0"]
    # Short dense list must fail before any zip-based truncation.
    with pytest.raises(ValueError, match="dense vector count"):
        build_points(chunks, _dense(1), _sparse(2), MODEL_ID, DIMENSION)
