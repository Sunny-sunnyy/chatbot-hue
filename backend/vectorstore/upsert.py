"""Bounded batch upsert and point-count verification."""
from collections.abc import Mapping, Sequence
import logging
import math
from typing import Any

import numpy as np
from qdrant_client import QdrantClient, models

try:
    from backend.core.schema import FullCorpusChunk
    from backend.embedding.full_corpus import validate_vector_matrix
    from backend.vectorstore.qdrant import validate_full_corpus_collection_info
except ModuleNotFoundError:
    from core.schema import FullCorpusChunk
    from embedding.full_corpus import validate_vector_matrix
    from vectorstore.qdrant import validate_full_corpus_collection_info

logger = logging.getLogger(__name__)

SCROLL_LIMIT = 1000


def upsert_points(client, settings, points):
    """Upsert all points in bounded batches; return completed point count.

    A partial failure logs safe progress (completed/total, never point
    content) and re-raises the original exception unchanged; no rollback.
    Rerunning is idempotent because point IDs are deterministic.
    """
    db = settings["vector_database"]
    name = db["collection_name"]
    batch_size = db["upsert_batch_size"]
    timeout = db["timeout"]
    completed = 0
    total = len(points)
    for start in range(0, total, batch_size):
        batch = points[start : start + batch_size]
        try:
            client.upsert(name, points=batch, wait=True, timeout=timeout)
        except Exception:
            logger.exception(
                "upsert failed after %d/%d points completed; rerun is idempotent",
                completed,
                total,
            )
            raise
        completed += len(batch)
    return completed


def validate_existing_points(client, settings, expected_points, model_id):
    """Fail closed when existing points are not a valid subset of the corpus."""
    db = settings["vector_database"]
    name = db["collection_name"]
    records, _ = client.scroll(
        name,
        limit=SCROLL_LIMIT,
        with_payload=True,
        with_vectors=False,
        timeout=db["timeout"],
    )
    if len(records) > len(expected_points):
        raise ValueError(
            f"collection has {len(records)} existing points, "
            f"more than expected {len(expected_points)}"
        )
    by_id = {str(point.id): point for point in expected_points}
    for record in records:
        point = by_id.get(str(record.id))
        if point is None:
            raise ValueError(
                f"foreign point {record.id} is not part of the expected corpus"
            )
        payload = record.payload or {}
        if payload.get("chunk_id") != point.payload["chunk_id"]:
            raise ValueError(f"payload chunk_id mismatch for point {record.id}")
        if payload.get("embedding_model") != model_id:
            raise ValueError(f"payload embedding_model mismatch for point {record.id}")


def verify_point_count(client, settings, expected_count):
    """Raise unless the collection holds exactly expected_count points."""
    name = settings["vector_database"]["collection_name"]
    actual = client.count(name, exact=True).count
    if actual != expected_count:
        raise ValueError(
            f"collection {name} point count {actual} != expected {expected_count}"
        )
    return actual


FULL_CORPUS_SCROLL_LIMIT = 1000
FULL_CORPUS_BATCH_SIZE = 64


def upsert_full_corpus_batch(
    client: QdrantClient,
    collection_name: str,
    points: Sequence[models.PointStruct],
    timeout: int,
) -> int:
    if not 1 <= len(points) <= FULL_CORPUS_BATCH_SIZE:
        raise ValueError("Full-corpus upsert batch size must be between 1 and 64")
    client.upsert(
        collection_name, points=points, wait=True, timeout=timeout
    )
    return len(points)


def compare_full_corpus_records(
    records: Sequence[models.Record],
    expected_payloads: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    seen: set[str] = set()
    for record in records:
        point_id = str(record.id)
        if point_id in seen:
            raise ValueError(f"Duplicate point returned by Qdrant: {point_id}")
        expected = expected_payloads.get(point_id)
        if expected is None:
            raise ValueError(f"Foreign point returned by Qdrant: {point_id}")
        if record.payload != expected:
            raise ValueError(f"Full-corpus payload mismatch for point {point_id}")
        seen.add(point_id)
    return seen


def validate_sample_vectors(
    records: Sequence[models.Record],
    expected_dimension: int,
    expected_ids: set[str],
) -> None:
    if {str(record.id) for record in records} != expected_ids:
        raise ValueError("Sample vector IDs do not match the exact expected set")
    for record in records:
        vectors = record.vector
        if not isinstance(vectors, dict) or set(vectors) != {"dense", "sparse"}:
            raise ValueError(f"Sample vector names mismatch for point {record.id}")
        dense = np.asarray(vectors["dense"], dtype=np.float32).reshape(1, -1)
        validate_vector_matrix(dense, 1, expected_dimension)
        sparse = vectors["sparse"]
        if not isinstance(sparse, models.SparseVector):
            raise ValueError(f"Sparse sample has wrong type for point {record.id}")
        if len(sparse.indices) != len(sparse.values):
            raise ValueError(f"Sparse sample length mismatch for point {record.id}")
        if sorted(set(sparse.indices)) != sparse.indices:
            raise ValueError(f"Sparse sample indices invalid for point {record.id}")
        if not all(math.isfinite(value) for value in sparse.values):
            raise ValueError(f"Sparse sample values invalid for point {record.id}")


def verify_full_corpus_collection(
    client: QdrantClient,
    collection_name: str,
    dimension: int,
    chunks: Sequence[FullCorpusChunk],
    sample_chunk_ids: Sequence[str],
    timeout: int,
) -> dict[str, int]:
    validate_full_corpus_collection_info(
        client.get_collection(collection_name), dimension
    )
    actual_count = client.count(collection_name, exact=True, timeout=timeout).count
    if actual_count != len(chunks):
        raise ValueError(
            f"Collection {collection_name} point count {actual_count} != {len(chunks)}"
        )
    expected_payloads = {
        chunk.point_id: chunk.to_qdrant_payload() for chunk in chunks
    }
    seen: set[str] = set()
    offset = None
    while True:
        records, next_offset = client.scroll(
            collection_name,
            limit=FULL_CORPUS_SCROLL_LIMIT,
            offset=offset,
            with_payload=True,
            with_vectors=False,
            timeout=timeout,
        )
        page_ids = compare_full_corpus_records(records, expected_payloads)
        duplicate = seen & page_ids
        if duplicate:
            raise ValueError(f"Duplicate point across scroll pages: {sorted(duplicate)}")
        seen.update(page_ids)
        if next_offset is None:
            break
        offset = next_offset
    if seen != set(expected_payloads):
        missing = sorted(set(expected_payloads) - seen)
        raise ValueError(f"Full-corpus point ID set mismatch; missing={missing[:10]}")
    chunk_by_id = {chunk.chunk_id: chunk for chunk in chunks}
    if any(chunk_id not in chunk_by_id for chunk_id in sample_chunk_ids):
        raise ValueError("Phase 3 sample chunk ID is absent from fresh corpus")
    sample_point_ids = {chunk_by_id[chunk_id].point_id for chunk_id in sample_chunk_ids}
    sample_records = client.retrieve(
        collection_name,
        ids=sorted(sample_point_ids),
        with_payload=False,
        with_vectors=["dense", "sparse"],
        timeout=timeout,
    )
    validate_sample_vectors(sample_records, dimension, sample_point_ids)
    return {
        "point_count": actual_count,
        "payloads_verified": len(seen),
        "sample_vectors_verified": len(sample_records),
    }
