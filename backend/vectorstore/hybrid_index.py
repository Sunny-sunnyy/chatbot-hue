"""Deterministic Qdrant point building and validation for Hue Foods chunks."""
import math
import uuid

POINT_ID_NAMESPACE = uuid.NAMESPACE_URL


def point_id_for(chunk_id):
    """Return the deterministic UUID5 point ID for a chunk_id."""
    return uuid.uuid5(POINT_ID_NAMESPACE, f"hue-rag:{chunk_id}")


def validate_chunks(chunks):
    """Validate chunk dicts and return chunk_ids in input order."""
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


def validate_vectors(dense, sparse, expected_count, dimension):
    """Validate dense/sparse representations against chunks before building points."""
    if len(dense) != expected_count:
        raise ValueError(
            f"dense vector count {len(dense)} != chunk count {expected_count}"
        )
    if len(sparse) != expected_count:
        raise ValueError(
            f"sparse vector count {len(sparse)} != chunk count {expected_count}"
        )
    for vector in dense:
        if len(vector) != dimension:
            raise ValueError(f"dense dimension {len(vector)} != expected {dimension}")
        if not all(math.isfinite(float(value)) for value in vector):
            raise ValueError("dense vector contains non-finite values")
    for sparse_vector in sparse:
        if not isinstance(sparse_vector, dict):
            raise ValueError("sparse vector must be a dict")
        indices = sparse_vector.get("indices")
        values = sparse_vector.get("values")
        if not isinstance(indices, list) or not isinstance(values, list):
            raise ValueError("sparse vector needs indices and values lists")
        if len(indices) != len(values):
            raise ValueError("sparse indices/values length mismatch")
        if any(not isinstance(i, int) or i < 0 for i in indices):
            raise ValueError("sparse indices must be non-negative integers")
        if any(not math.isfinite(float(value)) for value in values):
            raise ValueError("sparse vector contains non-finite values")


def build_points(chunks, dense, sparse, model_id, dimension):
    """Build deterministic point dicts from chunks and aligned vectors.

    Lengths are validated before the zip below, so a mismatch can never be
    silently truncated. Returns plain dicts; the Qdrant layer converts them.
    """
    chunk_ids = validate_chunks(chunks)
    validate_vectors(dense, sparse, len(chunk_ids), dimension)
    points = []
    for chunk, chunk_id, dense_vector, sparse_vector in zip(
        chunks, chunk_ids, dense, sparse
    ):
        points.append(
            {
                "id": point_id_for(chunk_id),
                "vector": {"dense": dense_vector, "sparse": sparse_vector},
                "payload": {
                    "text": chunk["text"],
                    "chunk_id": chunk_id,
                    "source": chunk["metadata"]["source"],
                    "title": chunk["metadata"]["title"],
                    "section": chunk["metadata"]["section"],
                    "category": chunk["metadata"]["category"],
                    "subcategory": chunk["metadata"]["subcategory"],
                    "chunk_type": chunk["metadata"]["chunk_type"],
                    "embedding_model": model_id,
                    "embedding_dimension": dimension,
                },
            }
        )
    return points
