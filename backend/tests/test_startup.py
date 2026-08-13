"""Live tests for profile-scoped startup, snapshot and staleness detection.

Stacks are built by the real startup code against real Qdrant collections.
The healthy path uses the ingested test collection (real pipeline output);
corrupt-state guards reproduce real Qdrant states on marked per-test
collections holding the real vectors scrolled back from the ingested
collection. Mutations that restore the shared test collection do so in
finally blocks.
"""

import pytest
from qdrant_client import models

from core.schema import (
    ComponentNotReadyError,
    RetrievalConfigurationError,
)
from core.startup import (
    CANONICAL_CHUNK_COUNT,
    build_retrieval_stack,
    verify_snapshot,
)
from reranking.models.cross_encoder import CrossEncoderReranker
from retrieval.service import build_service
from vectorstore.qdrant import expected_schema

from conftest import (
    TEST_COLLECTION,
    cleanup_collection,
    make_test_settings,
)

MODEL_ID = "intfloat/multilingual-e5-small"
MINILM_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"
DIMENSION = 384


def make_settings(profile, **overrides):
    return make_test_settings(TEST_COLLECTION, **{"active_profile": profile, **overrides})


def create_with_points(client, name, structs, profile="hybrid_no_rerank"):
    """Create a marked test collection and upsert real point structs."""
    settings = make_test_settings(name, **{"active_profile": profile})
    client.create_collection(
        name,
        vectors_config={"dense": expected_schema(settings)["dense"]},
        sparse_vectors_config={"sparse": expected_schema(settings)["sparse"]},
    )
    if structs:
        client.upsert(name, points=structs, wait=True)
    return settings


def to_struct(record):
    """Convert a scrolled record into a re-upsertable PointStruct."""
    return models.PointStruct(id=record.id, vector=record.vector, payload=record.payload)


def build_stack(profile, client, embedder):
    return build_retrieval_stack(
        make_settings(profile), client=client, embedder=embedder
    )


# --- Healthy startup paths on the real ingested corpus ---

def test_dense_only_builds_only_dense_retriever(
    ingested_collection, real_client, real_embedder
):
    stack = build_stack("dense_only", real_client, real_embedder)
    assert stack.dense_retriever is not None
    assert stack.hybrid_retriever is None
    assert stack.reranker is None
    assert stack.snapshot.bm25_ready is False
    assert stack.snapshot.reranker_ready is False
    assert stack.snapshot.point_count == CANONICAL_CHUNK_COUNT
    assert stack.snapshot.corpus_fingerprint is None
    assert stack.snapshot.embedding_model == MODEL_ID
    assert stack.snapshot.embedding_dimension == DIMENSION


def test_hybrid_no_rerank_scrolls_real_corpus(
    ingested_collection, real_client, real_embedder
):
    stack = build_stack("hybrid_no_rerank", real_client, real_embedder)
    assert stack.hybrid_retriever is not None
    assert stack.reranker is None
    assert stack.snapshot.bm25_ready is True
    fingerprint = stack.snapshot.corpus_fingerprint
    assert isinstance(fingerprint, str)
    assert len(fingerprint) == 64
    assert all(c in "0123456789abcdef" for c in fingerprint)


def test_hybrid_rerank_loads_real_cached_minilm(
    ingested_collection, real_client, real_embedder
):
    stack = build_stack("hybrid_rerank", real_client, real_embedder)
    assert stack.hybrid_retriever is not None
    assert isinstance(stack.reranker, CrossEncoderReranker)
    assert stack.reranker.model_id == MINILM_ID
    assert stack.snapshot.reranker_ready is True


def test_fingerprint_is_deterministic_and_sensitive_to_corpus(
    ingested_collection, real_client, real_embedder, ingested_point_structs
):
    first = build_stack("hybrid_no_rerank", real_client, real_embedder)
    second = build_stack("hybrid_no_rerank", real_client, real_embedder)
    assert first.snapshot.corpus_fingerprint == second.snapshot.corpus_fingerprint

    original = to_struct(ingested_point_structs[0])
    changed = models.PointStruct(
        id=original.id,
        vector=original.vector,
        payload={**original.payload, "text": "nội dung bị thay đổi hoàn toàn"},
    )
    try:
        real_client.upsert(TEST_COLLECTION, points=[changed], wait=True)
        third = build_stack("hybrid_no_rerank", real_client, real_embedder)
        assert third.snapshot.corpus_fingerprint != first.snapshot.corpus_fingerprint
    finally:
        real_client.upsert(TEST_COLLECTION, points=[original], wait=True)
        assert real_client.count(TEST_COLLECTION, exact=True).count == CANONICAL_CHUNK_COUNT


def test_scroll_batch_size_can_be_overridden(
    ingested_collection, real_client, real_embedder
):
    stack = build_retrieval_stack(
        make_settings("hybrid_no_rerank"),
        client=real_client,
        embedder=real_embedder,
        scroll_batch_size=64,
    )
    assert stack.snapshot.bm25_ready is True
    assert len(stack.snapshot.corpus_fingerprint) == 64


# --- Corrupt real Qdrant states reproduced on marked test collections ---

def test_count_mismatch_raises_not_ready(
    ingested_point_structs, real_client, real_embedder
):
    name = "hue_rag_live_test_startup_count571"
    settings = create_with_points(real_client, name, [to_struct(r) for r in ingested_point_structs[:571]])
    try:
        with pytest.raises(ComponentNotReadyError, match="571"):
            build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    finally:
        cleanup_collection(real_client, name)


def test_duplicate_chunk_ids_raise_not_ready(
    ingested_point_structs, real_client, real_embedder
):
    name = "hue_rag_live_test_startup_dup"
    structs = [to_struct(r) for r in ingested_point_structs]
    structs[1] = models.PointStruct(
        id=structs[1].id,
        vector=structs[1].vector,
        payload={**structs[1].payload, "chunk_id": structs[0].payload["chunk_id"]},
    )
    settings = create_with_points(real_client, name, structs)
    try:
        with pytest.raises(ComponentNotReadyError, match="duplicate"):
            build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    finally:
        cleanup_collection(real_client, name)


def test_empty_text_raises_not_ready(
    ingested_point_structs, real_client, real_embedder
):
    name = "hue_rag_live_test_startup_empty_text"
    structs = [to_struct(r) for r in ingested_point_structs]
    structs[0] = models.PointStruct(
        id=structs[0].id,
        vector=structs[0].vector,
        payload={**structs[0].payload, "text": "   "},
    )
    settings = create_with_points(real_client, name, structs)
    try:
        with pytest.raises(ComponentNotReadyError, match="empty text"):
            build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    finally:
        cleanup_collection(real_client, name)


def test_payload_embedding_model_mismatch_raises(
    ingested_point_structs, real_client, real_embedder
):
    name = "hue_rag_live_test_startup_model"
    structs = [to_struct(r) for r in ingested_point_structs]
    structs[0] = models.PointStruct(
        id=structs[0].id,
        vector=structs[0].vector,
        payload={**structs[0].payload, "embedding_model": "other-model"},
    )
    settings = create_with_points(real_client, name, structs)
    try:
        with pytest.raises(ComponentNotReadyError, match="embedding model"):
            build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    finally:
        cleanup_collection(real_client, name)


def test_missing_collection_raises_configuration_error(real_client, real_embedder):
    name = "hue_rag_live_test_startup_missing"
    with pytest.raises(RetrievalConfigurationError, match="does not exist"):
        build_retrieval_stack(
            make_test_settings(name), client=real_client, embedder=real_embedder
        )


def test_schema_mismatch_raises_configuration_error(real_client, real_embedder):
    name = "hue_rag_live_test_startup_dim512"
    real_client.create_collection(
        name,
        vectors_config={"dense": models.VectorParams(size=512, distance=models.Distance.COSINE)},
        sparse_vectors_config={"sparse": models.SparseVectorParams(index=models.SparseIndexParams())},
    )
    try:
        with pytest.raises(RetrievalConfigurationError, match="schema"):
            build_retrieval_stack(
                make_test_settings(name), client=real_client, embedder=real_embedder
            )
    finally:
        cleanup_collection(real_client, name)


def test_unknown_profile_raises_configuration_error(
    ingested_collection, real_client, real_embedder
):
    with pytest.raises(RetrievalConfigurationError, match="active_profile"):
        build_stack("bogus", real_client, real_embedder)


def test_embedding_db_dimension_mismatch_raises(
    ingested_collection, real_client, real_embedder
):
    settings = make_settings("dense_only", **{"embedding.vector_size": 512})
    with pytest.raises(RetrievalConfigurationError, match="vector_size"):
        build_retrieval_stack(settings, client=real_client, embedder=real_embedder)


# --- verify_snapshot against real state changes ---

def test_verify_snapshot_passes_when_unchanged(
    ingested_collection, real_client, real_embedder
):
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    assert verify_snapshot(stack, settings=settings, client=real_client) is None


def test_verify_snapshot_passes_for_dense_only_without_scroll(
    ingested_collection, real_client, real_embedder
):
    settings = make_settings("dense_only")
    stack = build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    assert verify_snapshot(stack, settings=settings, client=real_client) is None


def test_verify_snapshot_detects_point_count_change(
    ingested_collection, real_client, real_embedder, ingested_point_structs
):
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    victim = to_struct(ingested_point_structs[0])
    try:
        real_client.delete(
            TEST_COLLECTION,
            points_selector=models.PointIdsList(points=[victim.id]),
            wait=True,
        )
        with pytest.raises(ComponentNotReadyError, match="point count"):
            verify_snapshot(stack, settings=settings, client=real_client)
    finally:
        real_client.upsert(TEST_COLLECTION, points=[victim], wait=True)
        assert real_client.count(TEST_COLLECTION, exact=True).count == CANONICAL_CHUNK_COUNT


def test_verify_snapshot_detects_corpus_fingerprint_change(
    ingested_collection, real_client, real_embedder, ingested_point_structs
):
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    original = to_struct(ingested_point_structs[0])
    changed = models.PointStruct(
        id=original.id,
        vector=original.vector,
        payload={**original.payload, "text": "nội dung bị thay đổi"},
    )
    try:
        real_client.upsert(TEST_COLLECTION, points=[changed], wait=True)
        with pytest.raises(ComponentNotReadyError, match="fingerprint"):
            verify_snapshot(stack, settings=settings, client=real_client)
    finally:
        real_client.upsert(TEST_COLLECTION, points=[original], wait=True)


def test_verify_snapshot_detects_missing_collection(
    ingested_point_structs, real_client, real_embedder
):
    name = "hue_rag_live_test_startup_verify_missing"
    settings = create_with_points(real_client, name, [to_struct(r) for r in ingested_point_structs])
    stack = build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    cleanup_collection(real_client, name)
    with pytest.raises(ComponentNotReadyError, match="missing"):
        verify_snapshot(stack, settings=settings, client=real_client)


def test_verify_snapshot_detects_schema_change(
    ingested_point_structs, real_client, real_embedder
):
    name = "hue_rag_live_test_startup_verify_schema"
    settings = create_with_points(real_client, name, [to_struct(r) for r in ingested_point_structs])
    stack = build_retrieval_stack(settings, client=real_client, embedder=real_embedder)
    cleanup_collection(real_client, name)
    real_client.create_collection(
        name,
        vectors_config={"dense": models.VectorParams(size=512, distance=models.Distance.COSINE)},
        sparse_vectors_config={"sparse": models.SparseVectorParams(index=models.SparseIndexParams())},
    )
    try:
        with pytest.raises(ComponentNotReadyError, match="schema"):
            verify_snapshot(stack, settings=settings, client=real_client)
    finally:
        cleanup_collection(real_client, name)


def test_verify_snapshot_detects_config_change(
    ingested_collection, real_client, real_embedder
):
    settings = make_settings("hybrid_no_rerank")
    stack = build_retrieval_stack(settings, client=real_client, embedder=real_embedder)

    changed_profile = make_settings("dense_only")
    with pytest.raises(ComponentNotReadyError, match="active_profile"):
        verify_snapshot(stack, settings=changed_profile, client=real_client)

    changed_weights = make_settings(
        "hybrid_no_rerank",
        **{"retrieval.dense_weight": 0.7, "retrieval.bm25_weight": 0.3},
    )
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(stack, settings=changed_weights, client=real_client)

    changed_top_k = make_settings("hybrid_no_rerank", **{"retrieval.top_k": 5})
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(stack, settings=changed_top_k, client=real_client)

    changed_depth = make_settings("hybrid_no_rerank", **{"retrieval.candidate_multiplier": 4})
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(stack, settings=changed_depth, client=real_client)


def test_verify_snapshot_rerank_config_scope(
    ingested_collection, real_client, real_embedder
):
    rerank_settings = make_settings("hybrid_rerank")
    rerank_stack = build_retrieval_stack(
        rerank_settings, client=real_client, embedder=real_embedder
    )
    changed_model = make_settings("hybrid_rerank", **{"reranking.model": "other-model"})
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(rerank_stack, settings=changed_model, client=real_client)
    changed_top_k = make_settings("hybrid_rerank", **{"reranking.top_k": 3})
    with pytest.raises(ComponentNotReadyError, match="config changed"):
        verify_snapshot(rerank_stack, settings=changed_top_k, client=real_client)

    # Non-rerank profiles ignore reranking config in the semantic fingerprint.
    no_rerank_settings = make_settings("hybrid_no_rerank")
    no_rerank_stack = build_retrieval_stack(
        no_rerank_settings, client=real_client, embedder=real_embedder
    )
    ignored = make_settings("hybrid_no_rerank", **{"reranking.top_k": 3})
    assert verify_snapshot(no_rerank_stack, settings=ignored, client=real_client) is None


def test_build_service_factory_routes_active_profile(
    ingested_collection, real_client, real_embedder
):
    service = build_service(
        make_settings("dense_only"), client=real_client, embedder=real_embedder
    )
    assert service.active_profile == "dense_only"
    assert service.snapshot.point_count == CANONICAL_CHUNK_COUNT
