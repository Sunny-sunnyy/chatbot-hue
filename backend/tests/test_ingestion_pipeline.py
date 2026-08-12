"""Tests for batch upsert, ingestion orchestration and reset guards."""
import math
import uuid
from types import SimpleNamespace

import httpx
import pytest
from qdrant_client import models
from qdrant_client.http.exceptions import UnexpectedResponse

from ingestion.pipeline import run_ingestion
from vectorstore.hybrid_index import build_points
from vectorstore.reset import reset_collection
from vectorstore.upsert import to_point_struct, upsert_points, validate_existing_points, verify_point_count

COLLECTION = "hue_foods_e5_small_384"
MODEL_ID = "intfloat/multilingual-e5-small"
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
        "embedding": {"model": MODEL_ID, "vector_size": DIMENSION, "device": "cpu", "batch_size": 64},
    }
    for key, value in overrides.items():
        section, field = key.split(".", 1)
        settings[section][field] = value
    return settings


def make_info():
    dense = SimpleNamespace(size=DIMENSION, distance=models.Distance.COSINE)
    sparse = {"sparse": SimpleNamespace(index=object())}
    return SimpleNamespace(
        config=SimpleNamespace(params=SimpleNamespace(vectors={"dense": dense}, sparse_vectors=sparse))
    )


def _chunk(index=0):
    return {
        "text": f"Nội dung mẫu {index}",
        "metadata": {
            "chunk_id": f"foods/restaurants/example.md|Tóm tắt|{index}",
            "source": "foods/restaurants/example.md",
            "title": "Example",
            "section": "Tóm tắt",
            "category": "foods",
            "subcategory": "restaurants",
            "chunk_type": "section",
        },
    }


def build_fake_points(count):
    """Build count deterministic points with fake vectors."""
    chunks = [_chunk(index) for index in range(count)]
    norm = 1.0 / math.sqrt(DIMENSION)
    dense = [[norm] * DIMENSION for _ in range(count)]
    sparse = [{"indices": [i % 5], "values": [1.0]} for i in range(count)]
    return build_points(chunks, dense, sparse, MODEL_ID, DIMENSION)


class FakeQdrantClient:
    """In-memory Qdrant client honoring failure hooks for retry/count tests."""

    def __init__(self, existing_points=None, exists=False, info=None):
        self.exists = exists
        self.info = info
        self.info_after_upsert = None
        self.points = {}
        self.created = False
        self.create_kwargs = None
        self.upsert_batches = []
        self.delete_calls = 0
        self.count_override = None
        self.upsert_error = None
        self.transient_remaining = 0
        self.fail_upsert_on_batch = None
        self.deleted_stays = False
        for point in existing_points or []:
            self.points[str(point.id)] = point

    def collection_exists(self, name):
        return self.exists

    def get_collection(self, name):
        if self.upsert_batches and self.info_after_upsert is not None:
            return self.info_after_upsert
        return self.info if self.info is not None else make_info()

    def create_collection(self, name, **kwargs):
        self.created = True
        self.create_kwargs = kwargs
        self.exists = True

    def upsert(self, collection_name, points, wait=True, timeout=None):
        self.upsert_batches.append(len(points))
        if self.upsert_error is not None:
            raise self.upsert_error
        if self.transient_remaining > 0:
            self.transient_remaining -= 1
            raise httpx.ConnectError("connection refused")
        if self.fail_upsert_on_batch is not None and len(self.upsert_batches) == self.fail_upsert_on_batch:
            raise UnexpectedResponse(500, "boom", b"", {})
        for point in points:
            self.points[str(point.id)] = point

    def count(self, collection_name, exact=True):
        if self.count_override is not None:
            return SimpleNamespace(count=self.count_override)
        return SimpleNamespace(count=len(self.points))

    def scroll(self, collection_name, limit=10, with_payload=True, with_vectors=False, timeout=None):
        records = [SimpleNamespace(id=point.id, payload=point.payload) for point in self.points.values()]
        return records, None

    def delete_collection(self, name, timeout=None):
        self.delete_calls += 1
        if self.deleted_stays:
            return
        self.exists = False
        self.points = {}


class FakeEmbedder:
    """Deterministic embedder used instead of the local E5 model."""

    model_id = MODEL_ID
    dimension = DIMENSION

    def embed_documents(self, texts):
        return [[0.1] * DIMENSION for _ in texts]


class RecordingEmbedder(FakeEmbedder):
    """FakeEmbedder that records how many times embedding was invoked."""

    def __init__(self):
        self.embed_calls = 0

    def embed_documents(self, texts):
        self.embed_calls += 1
        return super().embed_documents(texts)


class BadDimensionEmbedder(FakeEmbedder):
    """Embedder returning vectors of the wrong dimension."""

    dimension = 8

    def embed_documents(self, texts):
        return [[0.1] * 8 for _ in texts]


def fake_chunker(chunks):
    """Wrap a static chunk list into the chunker callable signature."""
    return lambda: chunks


# --- Upsert: batch boundaries, retry allowlist, count gate ---

def test_upsert_points_batches_64_with_tail_60():
    client = FakeQdrantClient(exists=True)
    points = build_fake_points(572)
    completed = upsert_points(client, make_settings(), points)
    assert completed == 572
    assert client.upsert_batches == [64] * 8 + [60]


def test_upsert_retries_transient_error_once_then_succeeds():
    client = FakeQdrantClient(exists=True)
    client.transient_remaining = 1
    upsert_points(client, make_settings(), build_fake_points(64))
    # One failed attempt plus one retry for the same batch.
    assert client.upsert_batches == [64, 64]
    assert len(client.points) == 64


def test_upsert_transient_retry_exhausted_raises():
    client = FakeQdrantClient(exists=True)
    client.transient_remaining = 2
    with pytest.raises(httpx.TransportError):
        upsert_points(client, make_settings(), build_fake_points(64))
    assert client.upsert_batches == [64, 64]


def test_upsert_does_not_retry_non_transient_errors():
    client = FakeQdrantClient(exists=True)
    client.upsert_error = UnexpectedResponse(400, "bad request", b"", {})
    with pytest.raises(UnexpectedResponse):
        upsert_points(client, make_settings(), build_fake_points(64))
    assert client.upsert_batches == [64]


def test_upsert_partial_failure_stops_without_reporting_success(caplog):
    client = FakeQdrantClient(exists=True)
    client.fail_upsert_on_batch = 3  # third batch raises a non-retryable error
    with pytest.raises(UnexpectedResponse):
        upsert_points(client, make_settings(), build_fake_points(572))
    assert len(client.points) == 128  # first two batches are in, rest stopped
    assert client.upsert_batches == [64, 64, 64]
    # Safe progress evidence: completed count surfaced, no success claimed.
    assert "128/572" in caplog.text
    assert "completed" in caplog.text


def test_verify_point_count_is_exact_gate():
    client = FakeQdrantClient(exists=True)
    upsert_points(client, make_settings(), build_fake_points(572))
    assert verify_point_count(client, make_settings(), 572) == 572
    client.count_override = 571
    with pytest.raises(ValueError, match="point count"):
        verify_point_count(client, make_settings(), 572)


def test_existing_valid_subset_is_accepted():
    points = build_fake_points(64)
    client = FakeQdrantClient(existing_points=[to_point_struct(p) for p in points], exists=True)
    validate_existing_points(client, make_settings(), points, MODEL_ID)


def test_foreign_point_id_is_rejected():
    points = build_fake_points(64)
    foreign = models.PointStruct(
        id=uuid.uuid4(), vector={"dense": [0.1] * DIMENSION}, payload={"chunk_id": "x", "embedding_model": MODEL_ID, "embedding_dimension": DIMENSION}
    )
    client = FakeQdrantClient(existing_points=[foreign], exists=True)
    with pytest.raises(ValueError, match="foreign"):
        validate_existing_points(client, make_settings(), points, MODEL_ID)


def test_payload_identity_mismatch_is_rejected():
    points = build_fake_points(64)
    bad = models.PointStruct(
        id=points[0]["id"], vector={"dense": [0.1] * DIMENSION},
        payload={**points[0]["payload"], "embedding_model": "other/model"},
    )
    client = FakeQdrantClient(existing_points=[bad], exists=True)
    with pytest.raises(ValueError, match="embedding_model"):
        validate_existing_points(client, make_settings(), points, MODEL_ID)

    bad_chunk = models.PointStruct(
        id=points[0]["id"], vector={"dense": [0.1] * DIMENSION},
        payload={**points[0]["payload"], "chunk_id": "other.md|S|0"},
    )
    client = FakeQdrantClient(existing_points=[bad_chunk], exists=True)
    with pytest.raises(ValueError, match="chunk_id"):
        validate_existing_points(client, make_settings(), points, MODEL_ID)


# --- Ingestion pipeline orchestration ---

def test_ingestion_creates_collection_and_upserts_all_points():
    points = build_fake_points(572)
    client = FakeQdrantClient()
    summary = run_ingestion(
        make_settings(),
        chunker=fake_chunker([_chunk(i) for i in range(572)]),
        embedder=FakeEmbedder(),
        client=client,
    )
    assert client.created is True
    assert client.upsert_batches == [64] * 8 + [60]
    assert summary == {
        "collection_name": COLLECTION,
        "embedding_model": MODEL_ID,
        "embedding_dimension": DIMENSION,
        "chunk_count": 572,
        "point_count": 572,
    }
    assert len(client.points) == 572


def test_ingestion_rejects_non_canonical_chunk_count():
    for count in (571, 573):
        embedder = RecordingEmbedder()
        client = FakeQdrantClient()
        with pytest.raises(ValueError, match="canonical"):
            run_ingestion(
                make_settings(),
                chunker=fake_chunker([_chunk(i) for i in range(count)]),
                embedder=embedder,
                client=client,
            )
        # Rejected before embedding, client creation or collection mutation.
        assert embedder.embed_calls == 0
        assert client.created is False
        assert client.upsert_batches == []


def test_invalid_vectors_fail_before_collection_creation():
    client = FakeQdrantClient()
    with pytest.raises(ValueError, match="dimension"):
        run_ingestion(
            make_settings(),
            chunker=fake_chunker([_chunk(i) for i in range(572)]),
            embedder=BadDimensionEmbedder(),
            client=client,
        )
    assert client.created is False
    assert client.upsert_batches == []


def test_final_schema_revalidated_after_upsert():
    bad_info = SimpleNamespace(
        config=SimpleNamespace(
            params=SimpleNamespace(
                vectors={"dense": SimpleNamespace(size=512, distance=models.Distance.COSINE)},
                sparse_vectors={"sparse": SimpleNamespace(index=object())},
            )
        )
    )
    client = FakeQdrantClient()
    client.info_after_upsert = bad_info  # schema changes after the upsert
    with pytest.raises(ValueError, match="dimension"):
        run_ingestion(
            make_settings(),
            chunker=fake_chunker([_chunk(i) for i in range(572)]),
            embedder=FakeEmbedder(),
            client=client,
        )
    # Upsert ran, but success was never reported.
    assert client.upsert_batches == [64] * 8 + [60]


def test_ingestion_rejects_reset_collection_true():
    with pytest.raises(ValueError, match="reset_collection"):
        run_ingestion(
            make_settings(**{"vector_database.reset_collection": True}),
            chunker=fake_chunker([_chunk(0)]),
            embedder=FakeEmbedder(),
            client=FakeQdrantClient(),
        )


def test_ingestion_idempotent_rerun_after_partial_failure():
    first_client = FakeQdrantClient()
    first_client.fail_upsert_on_batch = 3
    with pytest.raises(UnexpectedResponse):
        run_ingestion(
            make_settings(),
            chunker=fake_chunker([_chunk(i) for i in range(572)]),
            embedder=FakeEmbedder(),
            client=first_client,
        )
    # Rerun on a client that already holds the completed batches.
    rerun_client = FakeQdrantClient(
        existing_points=list(first_client.points.values()), exists=True
    )
    summary = run_ingestion(
        make_settings(),
        chunker=fake_chunker([_chunk(i) for i in range(572)]),
        embedder=FakeEmbedder(),
        client=rerun_client,
    )
    assert summary["point_count"] == 572
    assert rerun_client.upsert_batches == [64] * 8 + [60]


def test_ingestion_rejects_foreign_existing_points_before_upsert():
    foreign = models.PointStruct(
        id=uuid.uuid4(), vector={"dense": [0.1] * DIMENSION},
        payload={"chunk_id": "x", "embedding_model": MODEL_ID, "embedding_dimension": DIMENSION},
    )
    client = FakeQdrantClient(existing_points=[foreign], exists=True)
    with pytest.raises(ValueError, match="foreign"):
        run_ingestion(
            make_settings(),
            chunker=fake_chunker([_chunk(i) for i in range(572)]),
            embedder=FakeEmbedder(),
            client=client,
        )
    assert client.upsert_batches == []


# --- Reset command guards ---

def test_reset_requires_exact_confirmation():
    client = FakeQdrantClient(exists=True)
    with pytest.raises(ValueError, match="confirmation"):
        reset_collection(client, make_settings(), expected_count=572, confirmation="DELETE other_collection")


def test_reset_refuses_missing_collection():
    client = FakeQdrantClient()
    with pytest.raises(ValueError, match="does not exist"):
        reset_collection(client, make_settings(), expected_count=572, confirmation=f"DELETE {COLLECTION}")
    assert client.delete_calls == 0


def test_reset_refuses_wrong_schema():
    bad_info = SimpleNamespace(
        config=SimpleNamespace(
            params=SimpleNamespace(
                vectors={"dense": SimpleNamespace(size=512, distance=models.Distance.COSINE)},
                sparse_vectors={"sparse": SimpleNamespace(index=object())},
            )
        )
    )
    client = FakeQdrantClient(exists=True, info=bad_info)
    with pytest.raises(ValueError, match="dimension"):
        reset_collection(client, make_settings(), expected_count=572, confirmation=f"DELETE {COLLECTION}")
    assert client.delete_calls == 0


def test_reset_refuses_count_mismatch():
    client = FakeQdrantClient(exists=True)
    client.count_override = 571
    with pytest.raises(ValueError, match="count"):
        reset_collection(client, make_settings(), expected_count=572, confirmation=f"DELETE {COLLECTION}")
    assert client.delete_calls == 0


def test_reset_refuses_payload_model_mismatch():
    point = build_fake_points(1)[0]
    wrong = models.PointStruct(
        id=point["id"], vector={"dense": [0.1] * DIMENSION},
        payload={**point["payload"], "embedding_model": "other/model"},
    )
    client = FakeQdrantClient(existing_points=[wrong], exists=True)
    with pytest.raises(ValueError, match="embedding_model"):
        reset_collection(client, make_settings(), expected_count=572, confirmation=f"DELETE {COLLECTION}")
    assert client.delete_calls == 0


def test_reset_deletes_exact_target_only_when_all_guards_pass():
    points = build_fake_points(572)
    client = FakeQdrantClient(existing_points=[to_point_struct(p) for p in points], exists=True)
    name = reset_collection(client, make_settings(), expected_count=572, confirmation=f"DELETE {COLLECTION}")
    assert name == COLLECTION
    assert client.delete_calls == 1
    assert client.exists is False


def test_reset_detects_delete_failure():
    points = build_fake_points(572)
    client = FakeQdrantClient(existing_points=[to_point_struct(p) for p in points], exists=True)
    client.deleted_stays = True
    with pytest.raises(RuntimeError, match="still exists"):
        reset_collection(client, make_settings(), expected_count=572, confirmation=f"DELETE {COLLECTION}")
