"""Bounded batch upsert and point-count verification."""
import logging

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
