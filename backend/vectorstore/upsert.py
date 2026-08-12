"""Bounded batch upsert, transient-only retry and point-count verification."""
import logging

import httpx

from qdrant_client import models

logger = logging.getLogger(__name__)

TRANSIENT_ERRORS = (httpx.TransportError,)
SCROLL_LIMIT = 1000


def to_point_struct(point):
    """Convert a built point dict into a qdrant PointStruct."""
    return models.PointStruct(
        id=point["id"],
        vector={
            "dense": point["vector"]["dense"],
            "sparse": models.SparseVector(**point["vector"]["sparse"]),
        },
        payload=point["payload"],
    )


def upsert_batch(client, collection_name, point_structs, timeout, max_retries):
    """Upsert one batch, retrying transient connection/timeout errors only."""
    attempt = 0
    while True:
        try:
            client.upsert(
                collection_name, points=point_structs, wait=True, timeout=timeout
            )
            return
        except TRANSIENT_ERRORS:
            attempt += 1
            if attempt > max_retries:
                raise


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
    max_retries = db["upsert_max_retries"]
    completed = 0
    total = len(points)
    for start in range(0, total, batch_size):
        batch = points[start : start + batch_size]
        try:
            upsert_batch(
                client,
                name,
                [to_point_struct(point) for point in batch],
                timeout,
                max_retries,
            )
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
    dimension = db["vector_size"]
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
    by_id = {str(point["id"]): point for point in expected_points}
    for record in records:
        point = by_id.get(str(record.id))
        if point is None:
            raise ValueError(
                f"foreign point {record.id} is not part of the expected corpus"
            )
        payload = record.payload or {}
        if payload.get("chunk_id") != point["payload"]["chunk_id"]:
            raise ValueError(f"payload chunk_id mismatch for point {record.id}")
        if payload.get("embedding_model") != model_id:
            raise ValueError(f"payload embedding_model mismatch for point {record.id}")
        if payload.get("embedding_dimension") != dimension:
            raise ValueError(f"payload embedding_dimension mismatch for point {record.id}")


def verify_point_count(client, settings, expected_count):
    """Raise unless the collection holds exactly expected_count points."""
    name = settings["vector_database"]["collection_name"]
    actual = client.count(name, exact=True).count
    if actual != expected_count:
        raise ValueError(
            f"collection {name} point count {actual} != expected {expected_count}"
        )
    return actual
