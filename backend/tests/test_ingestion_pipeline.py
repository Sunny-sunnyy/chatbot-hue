"""Live tests for the real ingestion pipeline, upsert and reset guards.

Every mutation happens on real Qdrant with marked isolated test
collections; the real curated corpus, the real E5 embedder and the real
sparse embedder are used. The active collection is never touched.
"""

import uuid

import httpx
import pytest
from qdrant_client import models
from qdrant_client.http.exceptions import ResponseHandlingException, UnexpectedResponse

from embedding.sparse_embedder import SparseEmbedder
from ingestion.pipeline import CANONICAL_CHUNK_COUNT, run_ingestion
from vectorstore.hybrid_index import build_points, point_id_for
from vectorstore.qdrant import expected_schema
from vectorstore.reset import reset_collection
from vectorstore.upsert import (
    to_point_struct,
    upsert_points,
    validate_existing_points,
    verify_point_count,
)

from conftest import (
    TEST_COLLECTION,
    cleanup_collection,
    make_test_settings,
)

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384


def _real_points_for_chunks(chunks, embedder, model_id=MODEL_ID, dimension=DIMENSION):
    """Build real points: real E5 dense vectors and real fitted sparse vectors."""
    texts = [chunk["text"] for chunk in chunks]
    sparse = SparseEmbedder().fit(texts)
    dense = embedder.embed_documents(texts)
    return build_points(
        chunks, dense, [sparse.encode(text) for text in texts], model_id, dimension
    )


def _create_marked_collection(client, name):
    """Create a real marked test collection with the expected 384-d schema."""
    settings = make_test_settings(name)
    client.create_collection(
        name,
        vectors_config={"dense": expected_schema(settings)["dense"]},
        sparse_vectors_config={"sparse": expected_schema(settings)["sparse"]},
    )
    return settings


# --- Real pipeline over the curated corpus ---

def test_live_ingestion_summary_and_collection_state(
    ingested_collection, real_client, live_settings
):
    """The real pipeline ingested the real corpus into the test collection."""
    assert ingested_collection == {
        "collection_name": TEST_COLLECTION,
        "embedding_model": MODEL_ID,
        "embedding_dimension": DIMENSION,
        "chunk_count": CANONICAL_CHUNK_COUNT,
        "point_count": CANONICAL_CHUNK_COUNT,
    }
    assert real_client.collection_exists(TEST_COLLECTION)
    assert real_client.count(TEST_COLLECTION, exact=True).count == CANONICAL_CHUNK_COUNT
    info = real_client.get_collection(TEST_COLLECTION)
    dense = info.config.params.vectors
    assert set(dense) == {"dense"}
    assert dense["dense"].size == DIMENSION
    assert dense["dense"].distance == models.Distance.COSINE
    sparse = info.config.params.sparse_vectors
    assert set(sparse) == {"sparse"}
    assert sparse["sparse"].index is not None


def test_ingestion_idempotent_rerun_on_existing_collection(
    real_client, real_embedder
):
    """Rerunning the real pipeline over the same collection stays idempotent."""
    from ingestion.chunking.markdown_chunker import chunk_foods_markdown

    settings = make_test_settings(TEST_COLLECTION)
    summary = run_ingestion(
        settings,
        chunker=chunk_foods_markdown,
        embedder=real_embedder,
        client=real_client,
    )
    assert summary["point_count"] == CANONICAL_CHUNK_COUNT
    assert real_client.count(TEST_COLLECTION, exact=True).count == CANONICAL_CHUNK_COUNT


def test_ingestion_rejects_non_canonical_chunk_count(real_client, real_embedder, real_chunks):
    """571 real chunks are rejected before any embedding or collection creation."""
    name = "hue_rag_live_test_ingestion_571"
    settings = make_test_settings(name)

    def chunker():
        return real_chunks[:-1]

    with pytest.raises(ValueError, match="canonical"):
        run_ingestion(settings, chunker=chunker, embedder=real_embedder, client=real_client)
    assert not real_client.collection_exists(name)


def test_ingestion_rejects_reset_collection_true(real_client, real_embedder, real_chunks):
    """reset_collection=true fails closed before touching anything."""
    name = "hue_rag_live_test_ingestion_reset_true"
    settings = make_test_settings(name, **{"vector_database.reset_collection": True})
    with pytest.raises(ValueError, match="reset_collection"):
        run_ingestion(
            settings,
            chunker=lambda: real_chunks,
            embedder=real_embedder,
            client=real_client,
        )
    assert not real_client.collection_exists(name)


def test_ingestion_rejects_foreign_existing_points_before_upsert(
    real_client, real_embedder, real_chunks
):
    """A foreign point in the target collection blocks the real pipeline run."""
    from ingestion.chunking.markdown_chunker import chunk_foods_markdown

    name = "hue_rag_live_test_ingestion_foreign"
    settings = _create_marked_collection(real_client, name)
    foreign_vector = real_embedder.embed_documents([real_chunks[0]["text"]])[0]
    sparse = SparseEmbedder().fit([real_chunks[0]["text"]])
    foreign = models.PointStruct(
        id=uuid.uuid4(),
        vector={
            "dense": foreign_vector,
            "sparse": models.SparseVector(**sparse.encode(real_chunks[0]["text"])),
        },
        payload={
            "chunk_id": "x",
            "embedding_model": MODEL_ID,
            "embedding_dimension": DIMENSION,
        },
    )
    real_client.upsert(name, points=[foreign], wait=True)
    try:
        with pytest.raises(ValueError, match="foreign"):
            run_ingestion(
                settings,
                chunker=chunk_foods_markdown,
                embedder=real_embedder,
                client=real_client,
            )
        # The pipeline never upserted corpus points over the foreign one.
        assert real_client.count(name, exact=True).count == 1
    finally:
        cleanup_collection(real_client, name)


# --- Upsert and count gates with real points ---

def test_upsert_points_and_count_gate_on_real_batch(
    real_client, real_embedder, real_chunks
):
    """Real points upsert in batches and the exact count gate sees real counts."""
    name = "hue_rag_live_test_upsert_batch"
    settings = _create_marked_collection(real_client, name)
    subset = real_chunks[:124]
    points = _real_points_for_chunks(subset, real_embedder)
    try:
        completed = upsert_points(real_client, settings, points)
        assert completed == 124
        assert verify_point_count(real_client, settings, 124) == 124
        with pytest.raises(ValueError, match="point count"):
            verify_point_count(real_client, settings, 123)
    finally:
        cleanup_collection(real_client, name)


def test_upsert_network_failure_is_real_failure(real_embedder, real_chunks):
    """A dead Qdrant URL raises the real transport error; no fake fallback."""
    dead_settings = make_test_settings(
        "hue_rag_live_test_upsert_dead",
        **{"vector_database.url": "http://localhost:6399", "vector_database.timeout": 3},
    )
    from vectorstore.qdrant import get_client

    dead_client = get_client(
        dead_settings["vector_database"]["url"],
        dead_settings["vector_database"]["timeout"],
    )
    points = _real_points_for_chunks(real_chunks[:1], real_embedder)
    with pytest.raises((httpx.TransportError, ResponseHandlingException)):
        upsert_points(dead_client, dead_settings, points)


def test_upsert_bad_request_is_real_failure(real_client, real_chunks):
    """Qdrant rejects a wrong-dimension dense vector with a real HTTP 400."""
    name = "hue_rag_live_test_upsert_400"
    settings = _create_marked_collection(real_client, name)
    chunk = real_chunks[0]
    bad_point = {
        "id": point_id_for(chunk["metadata"]["chunk_id"]),
        "vector": {"dense": [0.1] * 8, "sparse": {"indices": [1], "values": [1.0]}},
        "payload": {
            "chunk_id": chunk["metadata"]["chunk_id"],
            "embedding_model": MODEL_ID,
            "embedding_dimension": DIMENSION,
        },
    }
    try:
        with pytest.raises(UnexpectedResponse):
            upsert_points(real_client, settings, [bad_point])
        assert real_client.count(name, exact=True).count == 0
    finally:
        cleanup_collection(real_client, name)


# --- Existing-point validation with real points ---

def test_validate_existing_points_accepts_real_subset(
    real_client, real_embedder, real_chunks
):
    """Already-ingested real points pass validation on rerun."""
    name = "hue_rag_live_test_validate_ok"
    settings = _create_marked_collection(real_client, name)
    points = _real_points_for_chunks(real_chunks[:3], real_embedder)
    real_client.upsert(name, points=[to_point_struct(p) for p in points], wait=True)
    try:
        validate_existing_points(real_client, settings, points, MODEL_ID)
    finally:
        cleanup_collection(real_client, name)


def test_validate_existing_points_rejects_foreign_point(
    real_client, real_embedder, real_chunks
):
    """A foreign point id in the collection is rejected."""
    name = "hue_rag_live_test_validate_foreign"
    settings = _create_marked_collection(real_client, name)
    points = _real_points_for_chunks(real_chunks[:3], real_embedder)
    foreign = models.PointStruct(
        id=uuid.uuid4(),
        vector=to_point_struct(points[0]).vector,
        payload={"chunk_id": "x", "embedding_model": MODEL_ID, "embedding_dimension": DIMENSION},
    )
    real_client.upsert(name, points=[foreign], wait=True)
    try:
        with pytest.raises(ValueError, match="foreign"):
            validate_existing_points(real_client, settings, points, MODEL_ID)
    finally:
        cleanup_collection(real_client, name)


def test_validate_existing_points_rejects_payload_mismatch(
    real_client, real_embedder, real_chunks
):
    """Payload identity mismatches (model and chunk_id) are rejected."""
    name = "hue_rag_live_test_validate_payload"
    settings = _create_marked_collection(real_client, name)
    points = _real_points_for_chunks(real_chunks[:3], real_embedder)
    real_client.upsert(name, points=[to_point_struct(p) for p in points], wait=True)
    try:
        bad_model = to_point_struct(points[0])
        bad_model.payload = {**points[0]["payload"], "embedding_model": "other/model"}
        real_client.upsert(name, points=[bad_model], wait=True)
        with pytest.raises(ValueError, match="embedding_model"):
            validate_existing_points(real_client, settings, points, MODEL_ID)

        bad_chunk = to_point_struct(points[0])
        bad_chunk.payload = {**points[0]["payload"], "chunk_id": "other.md|S|0"}
        real_client.upsert(name, points=[bad_chunk], wait=True)
        with pytest.raises(ValueError, match="chunk_id"):
            validate_existing_points(real_client, settings, points, MODEL_ID)
    finally:
        cleanup_collection(real_client, name)


# --- Reset command guards on real collections ---

def test_reset_requires_exact_confirmation(ingested_collection, real_client):
    settings = make_test_settings(TEST_COLLECTION)
    with pytest.raises(ValueError, match="confirmation"):
        reset_collection(
            real_client, settings, expected_count=CANONICAL_CHUNK_COUNT,
            confirmation=f"DELETE {TEST_COLLECTION} extra",
        )
    assert real_client.collection_exists(TEST_COLLECTION)


def test_reset_refuses_missing_collection(real_client):
    name = "hue_rag_live_test_reset_missing"
    settings = make_test_settings(name)
    with pytest.raises(ValueError, match="does not exist"):
        reset_collection(
            real_client, settings, expected_count=0, confirmation=f"DELETE {name}"
        )
    assert not real_client.collection_exists(name)


def test_reset_refuses_wrong_schema(real_client):
    name = "hue_rag_live_test_reset_dim512"
    real_client.create_collection(
        name,
        vectors_config={"dense": models.VectorParams(size=512, distance=models.Distance.COSINE)},
        sparse_vectors_config={"sparse": models.SparseVectorParams(index=models.SparseIndexParams())},
    )
    settings = make_test_settings(name)
    try:
        with pytest.raises(ValueError, match="dimension"):
            reset_collection(
                real_client, settings, expected_count=0, confirmation=f"DELETE {name}"
            )
        assert real_client.collection_exists(name)  # guard never deletes
    finally:
        cleanup_collection(real_client, name)


def test_reset_refuses_count_mismatch(real_client, real_embedder, real_chunks):
    name = "hue_rag_live_test_reset_count"
    settings = _create_marked_collection(real_client, name)
    points = _real_points_for_chunks(real_chunks[:3], real_embedder)
    real_client.upsert(name, points=[to_point_struct(p) for p in points], wait=True)
    try:
        with pytest.raises(ValueError, match="count"):
            reset_collection(
                real_client, settings, expected_count=CANONICAL_CHUNK_COUNT,
                confirmation=f"DELETE {name}",
            )
        assert real_client.collection_exists(name)
    finally:
        cleanup_collection(real_client, name)


def test_reset_refuses_payload_model_mismatch(real_client, real_embedder, real_chunks):
    name = "hue_rag_live_test_reset_payload"
    settings = _create_marked_collection(real_client, name)
    points = _real_points_for_chunks(real_chunks[:1], real_embedder)
    bad = to_point_struct(points[0])
    bad.payload = {**points[0]["payload"], "embedding_model": "other/model"}
    real_client.upsert(name, points=[bad], wait=True)
    try:
        with pytest.raises(ValueError, match="embedding_model"):
            reset_collection(
                real_client, settings, expected_count=1, confirmation=f"DELETE {name}"
            )
        assert real_client.collection_exists(name)
    finally:
        cleanup_collection(real_client, name)


def test_reset_deletes_exact_target_only_when_all_guards_pass(
    real_client, real_embedder, real_chunks
):
    """With valid real state the reset deletes exactly the confirmed target."""
    name = "hue_rag_live_test_reset_ok"
    settings = _create_marked_collection(real_client, name)
    points = _real_points_for_chunks(real_chunks[:3], real_embedder)
    real_client.upsert(name, points=[to_point_struct(p) for p in points], wait=True)
    deleted = reset_collection(
        real_client, settings, expected_count=3, confirmation=f"DELETE {name}"
    )
    assert deleted == name
    assert not real_client.collection_exists(name)
