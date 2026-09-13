"""Qdrant client factory, collection schema validation and guarded create."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from qdrant_client import QdrantClient, models

DENSE_VECTOR_NAME = "dense"
SPARSE_VECTOR_NAME = "sparse"
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


def expected_full_corpus_schema(
    dimension: int,
) -> tuple[dict[str, models.VectorParams], dict[str, models.SparseVectorParams]]:
    if dimension not in {384, 768, 1024}:
        raise ValueError(f"Unsupported full-corpus dense dimension: {dimension}")
    return (
        {DENSE_VECTOR_NAME: models.VectorParams(size=dimension, distance=DISTANCE)},
        {SPARSE_VECTOR_NAME: models.SparseVectorParams()},
    )


def validate_full_corpus_collection_params(params: Any, dimension: int) -> None:
    expected_dense, expected_sparse = expected_full_corpus_schema(dimension)
    dense = params.vectors
    if not isinstance(dense, dict) or set(dense) != {DENSE_VECTOR_NAME}:
        names = sorted(dense) if isinstance(dense, dict) else ["unnamed"]
        raise QdrantSchemaError(f"dense vector names {names} != ['dense']")
    dense_params = dense[DENSE_VECTOR_NAME]
    if dense_params.size != dimension:
        raise QdrantSchemaError(
            f"dense dimension {dense_params.size} != {dimension}"
        )
    if dense_params.distance != DISTANCE:
        raise QdrantSchemaError("dense distance is not cosine")
    if getattr(dense_params, "on_disk", None) is True:
        raise QdrantSchemaError("dense vector on_disk is not allowed")
    if getattr(dense_params, "hnsw_config", None) is not None:
        raise QdrantSchemaError("dense vector custom hnsw_config is not allowed")
    if getattr(dense_params, "quantization_config", None) is not None:
        raise QdrantSchemaError("dense vector custom quantization_config is not allowed")
    if dense_params != expected_dense[DENSE_VECTOR_NAME]:
        raise QdrantSchemaError(f"dense params deviate from expected default: {dense_params}")

    sparse = params.sparse_vectors or {}
    if set(sparse) != {SPARSE_VECTOR_NAME}:
        raise QdrantSchemaError(f"sparse vector names {sorted(sparse)} != ['sparse']")
    sparse_params = sparse[SPARSE_VECTOR_NAME]
    if sparse_params.modifier is not None:
        raise QdrantSchemaError("sparse modifier must be none/default")
    index_params = getattr(sparse_params, "index", None)
    if index_params is not None:
        if getattr(index_params, "on_disk", None) is True:
            raise QdrantSchemaError("sparse index on_disk is not allowed")
        raise QdrantSchemaError("sparse index custom parameters are not allowed")
    if sparse_params != expected_sparse[SPARSE_VECTOR_NAME]:
        raise QdrantSchemaError(f"sparse params deviate from expected default: {sparse_params}")


def validate_full_corpus_collection_info(info: Any, dimension: int) -> None:
    validate_full_corpus_collection_params(info.config.params, dimension)
    if info.payload_schema:
        raise QdrantSchemaError(
            f"full-corpus collection has payload indexes: {sorted(info.payload_schema)}"
        )


@dataclass(frozen=True)
class FullCorpusTargetObservation:
    state: Literal["absent", "empty", "non_empty"]
    point_count: int
    build_record_exists: bool
    blockers: tuple[str, ...]


def classify_full_corpus_target(
    *, exists: bool, point_count: int, schema_error: str | None,
    build_record_exists: bool,
) -> FullCorpusTargetObservation:
    if not exists and point_count != 0:
        raise ValueError("Absent target cannot have points")
    state: Literal["absent", "empty", "non_empty"]
    state = "absent" if not exists else ("empty" if point_count == 0 else "non_empty")
    blockers: list[str] = []
    if schema_error is not None:
        blockers.append(f"schema mismatch: {schema_error}")
    if state == "non_empty":
        blockers.append(f"target is non-empty: {point_count} points")
    if build_record_exists:
        blockers.append("final build record already exists")
    return FullCorpusTargetObservation(
        state=state, point_count=point_count,
        build_record_exists=build_record_exists, blockers=tuple(blockers),
    )


def inspect_full_corpus_target(
    client: QdrantClient, collection_name: str, dimension: int,
    build_record_path: Path, timeout: int,
) -> FullCorpusTargetObservation:
    exists = client.collection_exists(collection_name)
    if not exists:
        return classify_full_corpus_target(
            exists=False, point_count=0, schema_error=None,
            build_record_exists=build_record_path.exists(),
        )
    info = client.get_collection(collection_name)
    try:
        validate_full_corpus_collection_info(info, dimension)
        schema_error = None
    except QdrantSchemaError as error:
        schema_error = str(error)
    count = client.count(collection_name, exact=True, timeout=timeout).count
    return classify_full_corpus_target(
        exists=True, point_count=count, schema_error=schema_error,
        build_record_exists=build_record_path.exists(),
    )


def require_fresh_full_corpus_target(
    observation: FullCorpusTargetObservation,
) -> Literal["absent", "empty"]:
    if observation.blockers:
        raise QdrantSchemaError("; ".join(observation.blockers))
    if observation.state not in {"absent", "empty"}:
        raise QdrantSchemaError(f"target state is not fresh: {observation.state}")
    return observation.state


def create_full_corpus_collection(
    client: QdrantClient, collection_name: str, dimension: int, timeout: int
) -> None:
    dense, sparse = expected_full_corpus_schema(dimension)
    client.create_collection(
        collection_name,
        vectors_config=dense,
        sparse_vectors_config=sparse,
        timeout=timeout,
    )
