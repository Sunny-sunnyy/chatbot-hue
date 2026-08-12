"""Tests for Qdrant client factory, schema validation and guarded create."""
from types import SimpleNamespace

import pytest
from qdrant_client import models

from vectorstore import qdrant

COLLECTION = "hue_foods_e5_small_384"
DIMENSION = 384


def make_settings(**overrides):
    settings = {
        "vector_database": {
            "url": "http://localhost:6333",
            "collection_name": COLLECTION,
            "reset_collection": False,
            "vector_size": DIMENSION,
            "distance": "cosine",
            "timeout": 30,
            "upsert_batch_size": 64,
            "upsert_max_retries": 1,
        },
        "embedding": {"model": "intfloat/multilingual-e5-small", "vector_size": DIMENSION},
    }
    for key, value in overrides.items():
        section, field = key.split(".", 1)
        settings[section][field] = value
    return settings


def make_info(dense_size=DIMENSION, distance=models.Distance.COSINE, sparse_present=True, has_sparse_index=True):
    """Build a duck-typed CollectionInfo-like object for schema checks."""
    vectors = {"dense": SimpleNamespace(size=dense_size, distance=distance)}
    index = object() if has_sparse_index else None
    sparse = {"sparse": SimpleNamespace(index=index)} if sparse_present else None
    return SimpleNamespace(
        config=SimpleNamespace(
            params=SimpleNamespace(vectors=vectors, sparse_vectors=sparse)
        )
    )


class FakeClient:
    """In-memory fake recording collection lifecycle calls."""

    def __init__(self, info=None):
        self.collections = {COLLECTION: info} if info is not None else {}
        self.created = []

    def collection_exists(self, name):
        return name in self.collections

    def get_collection(self, name):
        return self.collections[name]

    def create_collection(self, name, **kwargs):
        self.created.append((name, kwargs))


def test_get_client_caches_per_url_and_timeout(monkeypatch):
    """Cache identity is proven with a fake constructor; no real QdrantClient
    is ever created, so no localhost connection or version probe happens."""
    calls = []

    def fake_constructor(url, timeout):
        calls.append((url, timeout))
        return object()

    monkeypatch.setattr(qdrant, "QdrantClient", fake_constructor)
    qdrant.get_client.cache_clear()
    try:
        first = qdrant.get_client("http://localhost:6333", 30)
        assert qdrant.get_client("http://localhost:6333", 30) is first
        assert calls == [("http://localhost:6333", 30)]
        second = qdrant.get_client("http://localhost:6333", 45)
        assert second is not first
        assert calls == [
            ("http://localhost:6333", 30),
            ("http://localhost:6333", 45),
        ]
    finally:
        qdrant.get_client.cache_clear()


def test_client_from_settings_uses_configured_url_and_timeout(monkeypatch):
    captured = {}

    def fake_get_client(url, timeout):
        captured["url"] = url
        captured["timeout"] = timeout
        return "client"

    monkeypatch.setattr(qdrant, "get_client", fake_get_client)
    assert qdrant.client_from_settings(make_settings()) == "client"
    assert captured == {"url": "http://localhost:6333", "timeout": 30}


def test_ensure_collection_creates_exact_schema_when_absent():
    client = FakeClient()
    assert qdrant.ensure_collection(client, make_settings()) == "created"
    (name, kwargs), = client.created
    assert name == COLLECTION
    dense = kwargs["vectors_config"]["dense"]
    assert dense.size == DIMENSION
    assert dense.distance == models.Distance.COSINE
    assert set(kwargs["vectors_config"]) == {"dense"}
    assert set(kwargs["sparse_vectors_config"]) == {"sparse"}
    assert kwargs["sparse_vectors_config"]["sparse"].index is not None


def test_ensure_collection_accepts_matching_schema_without_recreate():
    client = FakeClient(info=make_info())
    assert qdrant.ensure_collection(client, make_settings()) == "existing"
    assert client.created == []


def test_ensure_collection_rejects_dimension_mismatch():
    client = FakeClient(info=make_info(dense_size=512))
    with pytest.raises(qdrant.QdrantSchemaError, match="dimension"):
        qdrant.ensure_collection(client, make_settings())
    assert client.created == []


def test_ensure_collection_rejects_distance_mismatch():
    client = FakeClient(info=make_info(distance=models.Distance.DOT))
    with pytest.raises(qdrant.QdrantSchemaError, match="distance"):
        qdrant.ensure_collection(client, make_settings())


def test_ensure_collection_rejects_extra_or_missing_vector_names():
    wrong_names = SimpleNamespace(
        config=SimpleNamespace(
            params=SimpleNamespace(
                vectors={"dense": SimpleNamespace(size=DIMENSION, distance=models.Distance.COSINE), "other": None},
                sparse_vectors={"sparse": SimpleNamespace(index=object())},
            )
        )
    )
    with pytest.raises(qdrant.QdrantSchemaError, match="vectors"):
        qdrant.ensure_collection(FakeClient(info=wrong_names), make_settings())


def test_ensure_collection_rejects_missing_sparse_vector():
    info = make_info(sparse_present=False)
    with pytest.raises(qdrant.QdrantSchemaError, match="sparse"):
        qdrant.ensure_collection(FakeClient(info=info), make_settings())


def test_ensure_collection_rejects_sparse_without_index():
    info = make_info(has_sparse_index=False)
    with pytest.raises(qdrant.QdrantSchemaError, match="index"):
        qdrant.ensure_collection(FakeClient(info=info), make_settings())
