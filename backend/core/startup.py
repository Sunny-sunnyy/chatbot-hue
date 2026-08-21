"""Profile-scoped retrieval startup: verification, bounded scroll and snapshot."""
import hashlib
import json
import logging
from dataclasses import dataclass
from typing import Optional

from core.schema import (
    ComponentNotReadyError,
    RetrievalConfigurationError,
    RetrievalDependencyError,
)
from core.settings_loader import load_settings
from embedding.embedder import SentenceTransformerEmbedder
from reranking.base import BaseReranker
from reranking.models.cross_encoder import CrossEncoderReranker
from retrieval.dense_retriever import DenseRetriever
from retrieval.hybrid_retriever import HybridRetriever
from scoring.bm25 import BM25
from vectorstore.qdrant import (
    QdrantSchemaError,
    client_from_settings,
    validate_collection_info,
)

logger = logging.getLogger(__name__)

# Canonical Phase 2 corpus size; changing it requires a user-approved
# contract change, never a silent pipeline adjustment.
CANONICAL_CHUNK_COUNT = 572

PROFILE_RERANK = "hybrid_rerank"

# Internal warm-up texts: never user queries, never sent to a provider and
# never logged. They only verify the real local models during startup.
E5_WARMUP_QUERY = "món ăn Huế"

SCROLL_PAYLOAD_FIELDS = [
    "chunk_id",
    "text",
    "embedding_model",
    "embedding_dimension",
]


@dataclass(frozen=True)
class RetrievalSnapshot:
    """Immutable verified state of the retrieval stack at startup."""

    collection_name: str
    point_count: int
    embedding_model: str
    embedding_dimension: int
    corpus_fingerprint: Optional[str]
    active_profile: str
    bm25_ready: bool
    reranker_ready: bool
    config_fingerprint: Optional[str] = None


@dataclass(frozen=True)
class RetrievalStack:
    """Built components plus the snapshot; only profile-relevant components exist."""

    snapshot: RetrievalSnapshot
    dense_retriever: Optional[DenseRetriever] = None
    hybrid_retriever: Optional[HybridRetriever] = None
    reranker: Optional[BaseReranker] = None


def _query_embedder(settings):
    """Build the local query embedder from settings; model loads lazily."""
    embedding = settings["embedding"]
    return SentenceTransformerEmbedder(
        model_id=embedding["model"],
        dimension=embedding["vector_size"],
        device=embedding["device"],
        batch_size=embedding["batch_size"],
    )


def _warm_embedder(embedder):
    """Load the real embedding model and verify one warm-up vector.

    embed_query() applies the shared BaseEmbedder validation: dimension,
    finiteness, non-zero norm and L2 normalization. The warm-up text is an
    internal constant: never a user query and never logged.
    """
    try:
        embedder.embed_query(E5_WARMUP_QUERY)
    except Exception as exc:  # model load/encode or validation failures
        raise ComponentNotReadyError(
            "embedder warm-up failed; the local model is unusable"
        ) from exc


def _scroll_all_payloads(client, collection_name, batch_size, timeout):
    """Scroll every payload in bounded batches, requesting only safe fields."""
    records = []
    offset = None
    while True:
        batch, offset = client.scroll(
            collection_name,
            limit=batch_size,
            offset=offset,
            with_payload=SCROLL_PAYLOAD_FIELDS,
            with_vectors=False,
            timeout=timeout,
        )
        records.extend(batch)
        if offset is None:
            break
    return records


def _corpus_pairs(records, expected_model, expected_dimension):
    """Return (chunk_id, text) pairs from records, verifying the payload contract."""
    pairs = []
    for record in records:
        payload = record.payload or {}
        chunk_id = payload.get("chunk_id")
        text = payload.get("text")
        if not isinstance(chunk_id, str) or not chunk_id:
            raise ComponentNotReadyError("collection payload has an invalid chunk_id")
        if not isinstance(text, str) or not text.strip():
            raise ComponentNotReadyError("collection payload has empty text")
        if payload.get("embedding_model") != expected_model:
            raise ComponentNotReadyError("collection payload embedding model mismatch")
        if payload.get("embedding_dimension") != expected_dimension:
            raise ComponentNotReadyError("collection payload embedding dimension mismatch")
        pairs.append((chunk_id, text))
    return pairs


def _corpus_fingerprint(pairs):
    """SHA-256 over sorted chunk_id + text pairs; deterministic per corpus."""
    lines = [f"{chunk_id}\x00{text}" for chunk_id, text in sorted(pairs)]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def _verify_collection(client, settings):
    """Verify collection existence, schema and canonical point count."""
    db = settings["vector_database"]
    collection_name = db["collection_name"]
    try:
        collection_exists = client.collection_exists(collection_name)
    except Exception as exc:  # client transport/protocol failures
        raise RetrievalDependencyError("Qdrant collection check failed") from exc
    if not collection_exists:
        raise RetrievalConfigurationError(
            f"collection {collection_name} does not exist"
        )
    try:
        collection_info = client.get_collection(collection_name)
    except Exception as exc:  # client transport/protocol failures
        raise RetrievalDependencyError("Qdrant collection info failed") from exc
    try:
        validate_collection_info(collection_info, settings)
    except QdrantSchemaError as exc:
        raise RetrievalConfigurationError(
            f"collection {collection_name} schema mismatch: {exc}"
        ) from exc
    try:
        actual_count = client.count(collection_name, exact=True).count
    except Exception as exc:  # client transport/protocol failures
        raise RetrievalDependencyError("Qdrant point count failed") from exc
    if actual_count != CANONICAL_CHUNK_COUNT:
        raise ComponentNotReadyError(
            f"collection {collection_name} has {actual_count} points, "
            f"expected {CANONICAL_CHUNK_COUNT}"
        )
    return actual_count


def _verify_config_consistency(settings, embedder):
    """Fail fast when embedding/database/injected-embedder identity disagrees."""
    db = settings["vector_database"]
    embedding = settings["embedding"]
    if embedding["vector_size"] != db["vector_size"]:
        raise RetrievalConfigurationError(
            f"embedding.vector_size {embedding['vector_size']} != "
            f"vector_database.vector_size {db['vector_size']}"
        )
    if getattr(embedder, "dimension", None) != db["vector_size"]:
        raise RetrievalConfigurationError(
            f"embedder dimension {getattr(embedder, 'dimension', None)} != "
            f"configured {db['vector_size']}"
        )
    if getattr(embedder, "model_id", None) != embedding["model"]:
        raise RetrievalConfigurationError(
            f"embedder model_id {getattr(embedder, 'model_id', None)!r} != "
            f"configured {embedding['model']!r}"
        )


def _semantic_config(settings):
    """Deterministic subset of settings that decides retrieval behavior.

    Reranking keys are included only when the active profile uses the
    reranker; the active profile itself is verified separately.
    """
    retrieval = settings["retrieval"]
    config = {
        "top_k": retrieval["top_k"],
        "candidate_multiplier": retrieval["candidate_multiplier"],
        "dense_weight": retrieval["dense_weight"],
        "bm25_weight": retrieval["bm25_weight"],
    }
    if settings["active_profile"] == PROFILE_RERANK:
        reranking = settings["reranking"]
        config["reranking_model"] = reranking["model"]
        config["reranking_device"] = reranking["device"]
        config["reranking_top_k"] = reranking["top_k"]
    return config


def _config_fingerprint(settings):
    """SHA-256 over the deterministic semantic config; stable per config."""
    return hashlib.sha256(
        json.dumps(_semantic_config(settings), sort_keys=True).encode("utf-8")
    ).hexdigest()


def build_retrieval_stack(
    settings=None,
    *,
    client=None,
    embedder=None,
    reranker=None,
    scroll_batch_size=None,
):
    """Verify the active collection and build only the profile's components.

    Verification is fail-explicit: config consistency, collection schema,
    dimension, canonical point count, unique chunk_ids, non-empty texts and
    embedding model identity must all match before any component is usable.
    For hybrid_rerank the MiniLM model is loaded once from the local cache
    (downloads disabled) and runs one warm-up prediction; a missing cache or
    an invalid warm-up score fails startup. The snapshot records what was
    verified; see verify_snapshot() for detecting stale state later.
    """
    settings = load_settings() if settings is None else settings
    profile = settings["active_profile"]
    profiles = settings.get("profiles", {})
    if profile not in profiles:
        raise RetrievalConfigurationError(
            f"Unknown active_profile: {profile!r}. Valid profiles: {sorted(profiles)}"
        )
    db = settings["vector_database"]
    retrieval = settings["retrieval"]
    embedding = settings["embedding"]
    reranking = settings["reranking"]
    collection_name = db["collection_name"]
    dimension = db["vector_size"]
    expected_model = embedding["model"]
    try:
        client = client_from_settings(settings) if client is None else client
    except Exception as exc:  # client construction/config failures
        raise RetrievalDependencyError("Qdrant client creation failed") from exc
    actual_count = _verify_collection(client, settings)
    bm25_ready = profile != "dense_only"
    reranker_ready = profile == PROFILE_RERANK
    embedder = _query_embedder(settings) if embedder is None else embedder
    _verify_config_consistency(settings, embedder)
    _warm_embedder(embedder)
    dense_retriever = DenseRetriever(
        client=client,
        embedder=embedder,
        collection_name=collection_name,
        top_k=retrieval["top_k"],
    )
    corpus_pairs = None
    hybrid_retriever = None
    if bm25_ready:
        batch_size = (
            db["scroll_batch_size"] if scroll_batch_size is None else scroll_batch_size
        )
        try:
            records = _scroll_all_payloads(
                client, collection_name, batch_size, db["timeout"]
            )
        except Exception as exc:  # client transport/protocol failures
            raise RetrievalDependencyError("Qdrant payload scroll failed") from exc
        corpus_pairs = _corpus_pairs(records, expected_model, dimension)
        if len(corpus_pairs) != CANONICAL_CHUNK_COUNT:
            raise ComponentNotReadyError(
                f"scroll returned {len(corpus_pairs)} payloads, "
                f"expected {CANONICAL_CHUNK_COUNT}"
            )
        chunk_ids = [chunk_id for chunk_id, _ in corpus_pairs]
        if len(chunk_ids) != len(set(chunk_ids)):
            raise ComponentNotReadyError("collection has duplicate chunk_id values")
        try:
            bm25 = BM25().fit([text for _, text in corpus_pairs])
        except Exception as exc:  # corpus-scoped fit failures
            raise ComponentNotReadyError("BM25 fit failed at startup") from exc
        hybrid_retriever = HybridRetriever(
            dense_retriever=dense_retriever,
            bm25=bm25,
            candidate_depth=retrieval["top_k"] * retrieval["candidate_multiplier"],
            top_k=retrieval["top_k"],
            dense_weight=retrieval["dense_weight"],
            bm25_weight=retrieval["bm25_weight"],
        )
    reranker_instance = None
    if reranker_ready:
        if reranker is None:
            reranker_instance = CrossEncoderReranker(
                model_id=reranking["model"], device=reranking["device"]
            )
            reranker_instance.load()
        else:
            reranker_instance = reranker
        reranker_instance.warm_up()
    snapshot = RetrievalSnapshot(
        collection_name=collection_name,
        point_count=actual_count,
        embedding_model=expected_model,
        embedding_dimension=dimension,
        corpus_fingerprint=(
            _corpus_fingerprint(corpus_pairs) if corpus_pairs is not None else None
        ),
        active_profile=profile,
        bm25_ready=bm25_ready,
        reranker_ready=reranker_ready,
        config_fingerprint=_config_fingerprint(settings),
    )
    logger.info(
        "retrieval stack ready: profile=%s collection=%s points=%d bm25=%s reranker=%s",
        profile,
        collection_name,
        actual_count,
        bm25_ready,
        reranker_ready,
    )
    return RetrievalStack(
        snapshot=snapshot,
        dense_retriever=dense_retriever,
        hybrid_retriever=hybrid_retriever,
        reranker=reranker_instance,
    )


def verify_snapshot(stack, settings=None, client=None, scroll_batch_size=None):
    """Fail explicitly when a built stack's snapshot no longer matches reality.

    Bounded staleness check for lifecycle use, never per-request: it compares
    the current config, collection schema, exact point count and (for hybrid
    stacks) the corpus fingerprint against the stored snapshot. The corpus is
    never refit. Any mismatch raises ComponentNotReadyError.
    """
    snapshot = stack.snapshot
    settings = load_settings() if settings is None else settings
    db = settings["vector_database"]
    embedding = settings["embedding"]
    if settings["active_profile"] != snapshot.active_profile:
        raise ComponentNotReadyError("active_profile changed since snapshot")
    if db["collection_name"] != snapshot.collection_name:
        raise ComponentNotReadyError("collection name changed since snapshot")
    if embedding["model"] != snapshot.embedding_model:
        raise ComponentNotReadyError("embedding model changed since snapshot")
    if embedding["vector_size"] != snapshot.embedding_dimension:
        raise ComponentNotReadyError("embedding dimension changed since snapshot")
    if snapshot.config_fingerprint is not None:
        if _config_fingerprint(settings) != snapshot.config_fingerprint:
            raise ComponentNotReadyError("retrieval config changed since snapshot")
    collection_name = db["collection_name"]
    try:
        client = client_from_settings(settings) if client is None else client
    except Exception as exc:  # client construction/config failures
        raise RetrievalDependencyError("Qdrant client creation failed") from exc
    try:
        collection_exists = client.collection_exists(collection_name)
    except Exception as exc:  # client transport/protocol failures
        raise RetrievalDependencyError("Qdrant collection check failed") from exc
    if not collection_exists:
        raise ComponentNotReadyError("collection missing since snapshot")
    try:
        collection_info = client.get_collection(collection_name)
    except Exception as exc:  # client transport/protocol failures
        raise RetrievalDependencyError("Qdrant collection info failed") from exc
    try:
        validate_collection_info(collection_info, settings)
    except QdrantSchemaError as exc:
        raise ComponentNotReadyError(
            f"collection schema changed since snapshot: {exc}"
        ) from exc
    try:
        actual_count = client.count(collection_name, exact=True).count
    except Exception as exc:  # client transport/protocol failures
        raise RetrievalDependencyError("Qdrant point count failed") from exc
    if actual_count != snapshot.point_count:
        raise ComponentNotReadyError(
            f"collection point count changed since snapshot: {actual_count} != "
            f"{snapshot.point_count}"
        )
    if snapshot.corpus_fingerprint is not None:
        batch_size = (
            db["scroll_batch_size"] if scroll_batch_size is None else scroll_batch_size
        )
        try:
            records = _scroll_all_payloads(
                client, db["collection_name"], batch_size, db["timeout"]
            )
        except Exception as exc:  # client transport/protocol failures
            raise RetrievalDependencyError("Qdrant payload scroll failed") from exc
        pairs = _corpus_pairs(records, snapshot.embedding_model, snapshot.embedding_dimension)
        fingerprint = _corpus_fingerprint(pairs)
        if fingerprint != snapshot.corpus_fingerprint:
            raise ComponentNotReadyError("corpus fingerprint changed since snapshot")
    return None
