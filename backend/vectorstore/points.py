from collections.abc import Mapping, Sequence
import math

import numpy as np
from qdrant_client import models

from core.schema import (
    FullCorpusChunk,
    point_id_for_chunk_id,
    validate_chunk_id,
)
from embedding.full_corpus import validate_vector_matrix
from embedding.sparse import SparseState, SparseVector, encode_sparse_document

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
