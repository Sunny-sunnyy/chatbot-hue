from collections.abc import Mapping, Sequence
import math
import uuid

import numpy as np
from qdrant_client import models

try:
    from backend.core.schema import (
        FullCorpusChunk,
        point_id_for_chunk_id,
        validate_chunk_id,
    )
    from backend.embedding.full_corpus import validate_vector_matrix
    from backend.embedding.sparse import SparseState, SparseVector, encode_sparse_document
except ModuleNotFoundError:
    from core.schema import (
        FullCorpusChunk,
        point_id_for_chunk_id,
        validate_chunk_id,
    )
    from embedding.full_corpus import validate_vector_matrix
    from embedding.sparse import SparseState, SparseVector, encode_sparse_document

POINT_ID_NAMESPACE = uuid.NAMESPACE_URL


def point_id_for(chunk_id: str):
    return uuid.uuid5(POINT_ID_NAMESPACE, f"hue-rag:{chunk_id}")


def validate_chunks(chunks):
    if not chunks:
        raise ValueError("no chunks to index")
    chunk_ids = []
    seen = set()
    for chunk in chunks:
        chunk_id = (chunk.get("metadata") or {}).get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            raise ValueError("chunk missing a non-empty metadata.chunk_id")
        if chunk_id in seen:
            raise ValueError(f"duplicate chunk_id: {chunk_id}")
        seen.add(chunk_id)
        chunk_ids.append(chunk_id)
    return chunk_ids


def build_points(chunks, dense, model_id, dimension):
    chunk_ids = validate_chunks(chunks)
    if len(dense) != len(chunk_ids):
        raise ValueError(f"dense vector count {len(dense)} != chunk count {len(chunk_ids)}")
    points = []
    for chunk, chunk_id, vector in zip(chunks, chunk_ids, dense):
        if len(vector) != dimension:
            raise ValueError(f"dense dimension {len(vector)} != expected {dimension}")
        if not all(math.isfinite(float(value)) for value in vector):
            raise ValueError("dense vector contains non-finite values")
        metadata = chunk["metadata"]
        points.append(models.PointStruct(
            id=point_id_for(chunk_id),
            vector={"dense": vector},
            payload={
                "text": chunk["text"],
                "chunk_id": chunk_id,
                "source": metadata["source"],
                "title": metadata["title"],
                "section": metadata["section"],
                "category": metadata["category"],
                "subcategory": metadata["subcategory"],
                "chunk_type": metadata["chunk_type"],
                "embedding_model": model_id,
            },
        ))
    return points


FULL_CORPUS_BATCH_SIZE = 64


def _validate_sparse_vector(chunk_id: str, sparse: SparseVector) -> None:
    if len(sparse.indices) != len(sparse.values):
        raise ValueError(f"Sparse indices/values mismatch for {chunk_id}")
    if tuple(sorted(set(sparse.indices))) != sparse.indices:
        raise ValueError(f"Sparse indices are not unique/sorted for {chunk_id}")
    if not all(math.isfinite(value) for value in sparse.values):
        raise ValueError(f"Sparse vector contains non-finite value for {chunk_id}")


def validate_full_corpus_point_inputs(
    chunks: Sequence[FullCorpusChunk],
    dense_matrix: np.ndarray,
    dimension: int,
    sparse_state: SparseState,
    vocabulary_index: Mapping[str, int],
) -> None:
    if not chunks:
        raise ValueError("Full-corpus chunks must not be empty")
    validate_vector_matrix(dense_matrix, len(chunks), dimension)
    chunk_ids = [chunk.chunk_id for chunk in chunks]
    point_ids = [chunk.point_id for chunk in chunks]
    if len(set(chunk_ids)) != len(chunk_ids):
        raise ValueError("Duplicate chunk_id in full corpus")
    if len(set(point_ids)) != len(point_ids):
        raise ValueError("Duplicate point ID in full corpus")
    required_payload = {
        "search_text", "source", "title", "heading_path", "evidence_parts",
        "chunk_id", "domain",
    }
    for chunk in chunks:
        validate_chunk_id(chunk.source, chunk.chunk_id)
        if chunk.point_id != point_id_for_chunk_id(chunk.chunk_id):
            raise ValueError(f"Point ID mismatch for chunk: {chunk.chunk_id}")
        if set(chunk.to_qdrant_payload()) != required_payload:
            raise ValueError(f"Payload fields mismatch for {chunk.chunk_id}")
        sparse = encode_sparse_document(
            chunk.search_text, sparse_state, vocabulary_index
        )
        _validate_sparse_vector(chunk.chunk_id, sparse)


def build_full_corpus_point_batch(
    chunks: Sequence[FullCorpusChunk],
    dense_rows: np.ndarray,
    dimension: int,
    sparse_state: SparseState,
    vocabulary_index: Mapping[str, int],
) -> list[models.PointStruct]:
    if not chunks:
        raise ValueError("Full-corpus point batch must not be empty")
    if len(chunks) > FULL_CORPUS_BATCH_SIZE:
        raise ValueError(f"Full-corpus point batch exceeds {FULL_CORPUS_BATCH_SIZE}")
    validate_vector_matrix(dense_rows, len(chunks), dimension)
    if len({chunk.chunk_id for chunk in chunks}) != len(chunks):
        raise ValueError("Duplicate chunk_id in full-corpus point batch")
    points: list[models.PointStruct] = []
    for chunk, dense_row in zip(chunks, dense_rows, strict=True):
        validate_chunk_id(chunk.source, chunk.chunk_id)
        if chunk.point_id != point_id_for_chunk_id(chunk.chunk_id):
            raise ValueError(f"Point ID mismatch for chunk: {chunk.chunk_id}")
        sparse = encode_sparse_document(
            chunk.search_text, sparse_state, vocabulary_index
        )
        _validate_sparse_vector(chunk.chunk_id, sparse)
        payload = chunk.to_qdrant_payload()
        if set(payload) != {
            "search_text", "source", "title", "heading_path", "evidence_parts",
            "chunk_id", "domain",
        }:
            raise ValueError(f"Payload fields mismatch for {chunk.chunk_id}")
        points.append(models.PointStruct(
            id=chunk.point_id,
            vector={
                "dense": dense_row.tolist(),
                "sparse": models.SparseVector(
                    indices=list(sparse.indices), values=list(sparse.values)
                ),
            },
            payload=payload,
        ))
    return points
