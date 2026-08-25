"""Live tests for the real dense-only ingestion pipeline, upsert and reset guards.

Every mutation happens on real Qdrant with marked isolated test collections;
the real curated corpus and the real E5 embedder are used.
The active collection is never touched.
"""

import uuid

import pytest
from qdrant_client import models

from conftest import (
    TEST_COLLECTION,
    cleanup_collection,
    make_test_settings,
)
from ingestion.pipeline import CANONICAL_CHUNK_COUNT, run_ingestion
from vectorstore.points import build_points, point_id_for
from vectorstore.qdrant import (
    ensure_collection,
    expected_schema,
)
from vectorstore.reset import reset_collection
from vectorstore.upsert import (
    upsert_points,
    verify_point_count,
)

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384


def _real_points_for_chunks(chunks, embedder, model_id=MODEL_ID, dimension=DIMENSION):
    """Build real dense-only points from chunks."""
    texts = [chunk["text"] for chunk in chunks]
    dense = embedder.embed_documents(texts)
    return build_points(chunks, dense, model_id, dimension)


def _create_marked_collection(client, name):
    """Create a real marked test collection with the dense-only 384-d schema."""
    settings = make_test_settings(name)
    client.create_collection(
        name,
        vectors_config=expected_schema(settings),
    )
    return settings


# --- Point and Schema Contracts ---

def test_dense_point_contract_uses_uuid5_and_model_identity(real_chunks, real_embedder):
    chunk = real_chunks[0]
    dense = real_embedder.embed_documents([chunk["text"]])
    point = build_points([chunk], dense, MODEL_ID, DIMENSION)[0]
    assert point.id == point_id_for(chunk["metadata"]["chunk_id"])
    assert set(point.vector) == {"dense"}
    assert len(point.vector["dense"]) == 384
    assert point.payload["embedding_model"] == MODEL_ID
    assert "embedding_dimension" not in point.payload


def test_live_dense_schema_has_no_sparse_vectors(real_client):
    name = "hue_rag_live_test_dense_schema"
    settings = make_test_settings(name)
    try:
        assert ensure_collection(real_client, settings) == "created"
        info = real_client.get_collection(name)
        assert set(info.config.params.vectors) == {"dense"}
        assert not info.config.params.sparse_vectors
    finally:
        cleanup_collection(real_client, name)


# --- Real Pipeline over the Curated Corpus ---

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
    assert not info.config.params.sparse_vectors


def test_ingestion_idempotent_rerun_on_real_dense_collection(
    ingested_collection, real_client, real_embedder
):
    first_count = real_client.count(TEST_COLLECTION, exact=True).count
    summary = run_ingestion(
        make_test_settings(TEST_COLLECTION),
        embedder=real_embedder,
        client=real_client,
    )
    assert first_count == summary["point_count"] == CANONICAL_CHUNK_COUNT
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


def test_ingestion_rejects_foreign_existing_points_before_upsert(
    real_client, real_embedder, real_chunks
):
    """A foreign point in the target collection blocks the real pipeline run."""
    name = "hue_rag_live_test_ingestion_foreign"
    settings = _create_marked_collection(real_client, name)
    foreign_vector = real_embedder.embed_documents([real_chunks[0]["text"]])[0]
    foreign = models.PointStruct(
        id=uuid.uuid4(),
        vector={"dense": foreign_vector},
        payload={
            "chunk_id": "x",
            "source": "foods/test.md",
            "title": "Test",
            "section": "Intro",
            "category": "foods",
            "subcategory": "test",
            "chunk_type": "section",
            "embedding_model": MODEL_ID,
        },
    )
    real_client.upsert(name, points=[foreign], wait=True)
    try:
        with pytest.raises(ValueError, match="foreign"):
            run_ingestion(
                settings,
                embedder=real_embedder,
                client=real_client,
            )
        assert real_client.count(name, exact=True).count == 1
    finally:
        cleanup_collection(real_client, name)


def test_ingestion_rejects_existing_model_mismatch_before_mutation(
    real_client, real_embedder, real_chunks
):
    name = "hue_rag_live_test_model_mismatch"
    settings = make_test_settings(name)
    ensure_collection(real_client, settings)
    point = build_points(
        real_chunks[:1],
        real_embedder.embed_documents([real_chunks[0]["text"]]),
        MODEL_ID,
        DIMENSION,
    )[0]
    point.payload["embedding_model"] = "other/model"
    real_client.upsert(name, points=[point], wait=True)
    try:
        with pytest.raises(ValueError, match="embedding_model"):
            run_ingestion(settings, embedder=real_embedder, client=real_client)
        assert real_client.count(name, exact=True).count == 1
    finally:
        cleanup_collection(real_client, name)


# --- Upsert and Count Gates with Real Points ---

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


# --- Reset Command on Real Collections ---

def test_reset_deletes_only_exact_guarded_target_and_reports_count(real_client):
    name = "hue_rag_live_test_reset_exact"
    settings = make_test_settings(name)
    ensure_collection(real_client, settings)
    deleted_name, count = reset_collection(
        real_client,
        settings,
        collection_name=name,
        confirmation=f"DELETE {name}",
    )
    assert (deleted_name, count) == (name, 0)
    assert not real_client.collection_exists(name)


def test_reset_rejects_confirmation_mismatch_without_deleting(real_client):
    name = "hue_rag_live_test_reset_confirmation"
    settings = make_test_settings(name)
    ensure_collection(real_client, settings)
    try:
        with pytest.raises(ValueError, match="confirmation"):
            reset_collection(
                real_client,
                settings,
                collection_name=name,
                confirmation=f"DELETE {name} extra",
            )
        assert real_client.collection_exists(name)
    finally:
        cleanup_collection(real_client, name)


def test_reset_refuses_missing_collection(real_client):
    name = "hue_rag_live_test_reset_missing"
    settings = make_test_settings(name)
    with pytest.raises(ValueError, match="does not exist"):
        reset_collection(
            real_client,
            settings,
            collection_name=name,
            confirmation=f"DELETE {name}",
        )
    assert not real_client.collection_exists(name)
