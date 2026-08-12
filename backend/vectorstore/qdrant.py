"""Qdrant client factory, collection schema validation and guarded create."""
from functools import lru_cache

from qdrant_client import QdrantClient, models

DENSE_VECTOR_NAME = "dense"
SPARSE_VECTOR_NAME = "sparse"
DISTANCE = models.Distance.COSINE


class QdrantSchemaError(ValueError):
    """Raised when an existing collection deviates from the expected schema."""


@lru_cache(maxsize=4)
def get_client(url, timeout):
    """Return one cached QdrantClient per (url, timeout) pair."""
    return QdrantClient(url=url, timeout=timeout)


def client_from_settings(settings=None):
    """Build a cached client from the vector_database settings group."""
    if settings is None:
        from core.settings_loader import load_settings

        settings = load_settings()
    db = settings["vector_database"]
    return get_client(db["url"], db["timeout"])


def expected_schema(settings):
    """Return the expected named-vector schema for the current settings."""
    dimension = settings["vector_database"]["vector_size"]
    return {
        DENSE_VECTOR_NAME: models.VectorParams(size=dimension, distance=DISTANCE),
        SPARSE_VECTOR_NAME: models.SparseVectorParams(index=models.SparseIndexParams()),
    }


def validate_collection_info(info, settings):
    """Raise QdrantSchemaError when an existing collection deviates from expectations."""
    params = info.config.params
    expected_dimension = settings["vector_database"]["vector_size"]
    dense = params.vectors
    if not isinstance(dense, dict) or set(dense) != {DENSE_VECTOR_NAME}:
        names = sorted(dense) if isinstance(dense, dict) else "single (non-named) vector config"
        raise QdrantSchemaError(f"collection vectors {names} != expected ['dense']")
    dense_params = dense[DENSE_VECTOR_NAME]
    if dense_params.size != expected_dimension:
        raise QdrantSchemaError(
            f"dense dimension {dense_params.size} != expected {expected_dimension}"
        )
    if dense_params.distance != DISTANCE:
        raise QdrantSchemaError(f"dense distance {dense_params.distance!r} != cosine")
    sparse = params.sparse_vectors or {}
    if not isinstance(sparse, dict) or set(sparse) != {SPARSE_VECTOR_NAME}:
        names = sorted(sparse) if isinstance(sparse, dict) else "missing"
        raise QdrantSchemaError(f"sparse vectors {names} != expected ['sparse']")
    if sparse[SPARSE_VECTOR_NAME].index is None:
        raise QdrantSchemaError("sparse vector has no index enabled")


def ensure_collection(client, settings):
    """Create the collection only when absent; validate schema when it exists."""
    db = settings["vector_database"]
    name = db["collection_name"]
    if client.collection_exists(name):
        validate_collection_info(client.get_collection(name), settings)
        return "existing"
    schema = expected_schema(settings)
    client.create_collection(
        name,
        vectors_config={DENSE_VECTOR_NAME: schema[DENSE_VECTOR_NAME]},
        sparse_vectors_config={SPARSE_VECTOR_NAME: schema[SPARSE_VECTOR_NAME]},
        timeout=db["timeout"],
    )
    return "created"
