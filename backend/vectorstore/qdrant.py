"""Qdrant client factory, collection schema validation and guarded create."""
from qdrant_client import QdrantClient, models

DENSE_VECTOR_NAME = "dense"
DISTANCE = models.Distance.COSINE


class QdrantSchemaError(ValueError):
    """Raised when an existing collection deviates from the expected schema."""


def client_from_settings(settings=None):
    """Build an uncached client from the vector_database settings group."""
    if settings is None:
        from core.settings_loader import load_settings

        settings = load_settings()
    db = settings["vector_database"]
    return QdrantClient(url=db["url"], timeout=db["timeout"])


def expected_schema(settings):
    """Return the expected dense named-vector schema for the current settings."""
    dimension = settings["vector_database"]["vector_size"]
    return {DENSE_VECTOR_NAME: models.VectorParams(size=dimension, distance=DISTANCE)}


def validate_collection_info(info, settings, *, strict_dense_only=True):
    """Raise QdrantSchemaError when an existing collection deviates from expectations.

    Checks that the named 'dense' vector exists with the configured size and cosine distance.
    When strict_dense_only=True (default, used for ingestion and candidate validation),
    rejects any unexpected sparse vectors or non-dense vector names.
    When strict_dense_only=False (used by retrieval startup before cutover),
    accepts legacy collections that contain the required dense vector and ignores unused sparse fields.
    """
    params = info.config.params
    expected_dimension = settings["vector_database"]["vector_size"]
    dense = params.vectors
    if not isinstance(dense, dict) or DENSE_VECTOR_NAME not in dense:
        names = sorted(dense) if isinstance(dense, dict) else "single (non-named) vector config"
        raise QdrantSchemaError(f"collection vectors {names} missing expected 'dense'")
    if strict_dense_only and set(dense) != {DENSE_VECTOR_NAME}:
        raise QdrantSchemaError(f"collection vectors {sorted(dense)} != expected ['dense']")
    dense_params = dense[DENSE_VECTOR_NAME]
    if dense_params.size != expected_dimension:
        raise QdrantSchemaError(
            f"dense dimension {dense_params.size} != expected {expected_dimension}"
        )
    if dense_params.distance != DISTANCE:
        raise QdrantSchemaError(f"dense distance {dense_params.distance!r} != cosine")
    sparse = params.sparse_vectors or {}
    if strict_dense_only and sparse:
        raise QdrantSchemaError(f"collection has unexpected sparse vectors: {sorted(sparse)}")


def ensure_collection(client, settings):
    """Create the collection only when absent; validate strict schema when it exists."""
    db = settings["vector_database"]
    name = db["collection_name"]
    if client.collection_exists(name):
        validate_collection_info(client.get_collection(name), settings, strict_dense_only=True)
        return "existing"
    client.create_collection(
        name,
        vectors_config=expected_schema(settings),
        timeout=db["timeout"],
    )
    return "created"
