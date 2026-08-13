"""Live tests for the Qdrant client factory, schema validation and guarded create.

All collection mutations happen on real Qdrant with marked isolated test
collections that are deleted at the end of each test. The active collection
is never touched.
"""

import pytest
from qdrant_client import models

from vectorstore import qdrant
from vectorstore.qdrant import DENSE_VECTOR_NAME, SPARSE_VECTOR_NAME, get_client

from conftest import cleanup_collection, make_test_settings

DIMENSION = 384


def _make_settings(**overrides):
    return make_test_settings("hue_rag_live_test_qdrant_schema", **overrides)


def create_real_collection(client, name, **kwargs):
    """Create a real collection with explicit schema for schema guard tests."""
    client.create_collection(name, **kwargs)
    return client.get_collection(name)


def test_get_client_caches_per_url_and_timeout():
    """Real QdrantClient objects are cached per (url, timeout) pair.

    Distinct timeouts and URL strings are used so the shared session cache
    stays intact for other tests; the cache is production behavior and is
    never cleared here.
    """
    first = get_client("http://localhost:6333", 31)
    assert get_client("http://localhost:6333", 31) is first
    second = get_client("http://localhost:6333", 45)
    assert second is not first
    # A different URL string for the same server is a distinct cache key.
    third = get_client("http://127.0.0.1:6333", 31)
    assert third is not first


def test_client_from_settings_returns_working_cached_client(real_client):
    """The settings-built client is cached and talks to the configured server.

    Identity across separate cache lookups is guaranteed; identity with a
    fixture created earlier is not, because the production lru_cache holds
    only four (url, timeout) entries and later tests legitimately add new
    keys that evict older ones.
    """
    settings = make_test_settings()
    from vectorstore.qdrant import client_from_settings

    built = client_from_settings(settings)
    assert built is client_from_settings(settings)
    # Real round trip against the configured server proves the URL resolves.
    assert isinstance(built.get_collections().collections, list)
    assert isinstance(real_client.get_collections().collections, list)


def test_ensure_collection_creates_exact_schema_when_absent(real_client):
    name = "hue_rag_live_test_qdrant_created"
    settings = make_test_settings("hue_rag_live_test_qdrant_created")
    try:
        assert qdrant.ensure_collection(real_client, settings) == "created"
        info = real_client.get_collection(name)
        dense = info.config.params.vectors
        assert set(dense) == {DENSE_VECTOR_NAME}
        assert dense[DENSE_VECTOR_NAME].size == DIMENSION
        assert dense[DENSE_VECTOR_NAME].distance == models.Distance.COSINE
        sparse = info.config.params.sparse_vectors
        assert set(sparse) == {SPARSE_VECTOR_NAME}
        assert sparse[SPARSE_VECTOR_NAME].index is not None
    finally:
        cleanup_collection(real_client, name)


def test_ensure_collection_accepts_matching_schema_without_recreate(real_client):
    name = "hue_rag_live_test_qdrant_existing"
    settings = make_test_settings("hue_rag_live_test_qdrant_existing")
    try:
        assert qdrant.ensure_collection(real_client, settings) == "created"
        assert qdrant.ensure_collection(real_client, settings) == "existing"
        assert real_client.collection_exists(name)
        assert real_client.count(name, exact=True).count == 0
    finally:
        cleanup_collection(real_client, name)


def test_ensure_collection_rejects_dimension_mismatch(real_client):
    name = "hue_rag_live_test_qdrant_dim512"
    settings = make_test_settings("hue_rag_live_test_qdrant_dim512")
    try:
        create_real_collection(
            real_client,
            name,
            vectors_config={
                "dense": models.VectorParams(
                    size=512, distance=models.Distance.COSINE
                )
            },
            sparse_vectors_config={
                "sparse": models.SparseVectorParams(index=models.SparseIndexParams())
            },
        )
        with pytest.raises(qdrant.QdrantSchemaError, match="dimension"):
            qdrant.ensure_collection(real_client, settings)
        assert real_client.collection_exists(name)  # guard never deletes
    finally:
        cleanup_collection(real_client, name)


def test_ensure_collection_rejects_distance_mismatch(real_client):
    name = "hue_rag_live_test_qdrant_dot"
    settings = make_test_settings("hue_rag_live_test_qdrant_dot")
    try:
        create_real_collection(
            real_client,
            name,
            vectors_config={
                "dense": models.VectorParams(size=DIMENSION, distance=models.Distance.DOT)
            },
            sparse_vectors_config={
                "sparse": models.SparseVectorParams(index=models.SparseIndexParams())
            },
        )
        with pytest.raises(qdrant.QdrantSchemaError, match="distance"):
            qdrant.ensure_collection(real_client, settings)
    finally:
        cleanup_collection(real_client, name)


def test_ensure_collection_rejects_extra_vector_names(real_client):
    name = "hue_rag_live_test_qdrant_extra"
    settings = make_test_settings("hue_rag_live_test_qdrant_extra")
    try:
        create_real_collection(
            real_client,
            name,
            vectors_config={
                "dense": models.VectorParams(size=DIMENSION, distance=models.Distance.COSINE),
                "other": models.VectorParams(size=DIMENSION, distance=models.Distance.COSINE),
            },
            sparse_vectors_config={
                "sparse": models.SparseVectorParams(index=models.SparseIndexParams())
            },
        )
        with pytest.raises(qdrant.QdrantSchemaError, match="vectors"):
            qdrant.ensure_collection(real_client, settings)
    finally:
        cleanup_collection(real_client, name)


def test_ensure_collection_rejects_missing_sparse_vector(real_client):
    name = "hue_rag_live_test_qdrant_no_sparse"
    settings = make_test_settings("hue_rag_live_test_qdrant_no_sparse")
    try:
        create_real_collection(
            real_client,
            name,
            vectors_config={
                "dense": models.VectorParams(size=DIMENSION, distance=models.Distance.COSINE)
            },
        )
        with pytest.raises(qdrant.QdrantSchemaError, match="sparse"):
            qdrant.ensure_collection(real_client, settings)
    finally:
        cleanup_collection(real_client, name)


def test_ensure_collection_rejects_sparse_without_index(real_client):
    name = "hue_rag_live_test_qdrant_sparse_no_index"
    settings = make_test_settings("hue_rag_live_test_qdrant_sparse_no_index")
    try:
        create_real_collection(
            real_client,
            name,
            vectors_config={
                "dense": models.VectorParams(size=DIMENSION, distance=models.Distance.COSINE)
            },
            sparse_vectors_config={"sparse": models.SparseVectorParams()},
        )
        with pytest.raises(qdrant.QdrantSchemaError, match="index"):
            qdrant.ensure_collection(real_client, settings)
    finally:
        cleanup_collection(real_client, name)
