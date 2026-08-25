import math
import uuid

from qdrant_client import models

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
