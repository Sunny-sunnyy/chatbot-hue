"""Profile-scoped retrieval startup: verification, bounded scroll and direct service composition."""
import logging
from dataclasses import dataclass

from core.schema import (
    ComponentNotReadyError,
    RetrievalConfigurationError,
    RetrievalDependencyError,
)
from core.settings_loader import load_settings
from embedding.embedder import E5Embedder
from reranking.cross_encoder import CrossEncoderReranker
from retrieval.dense_retriever import DenseRetriever
from retrieval.hybrid_retriever import HybridRetriever
from scoring.bm25 import BM25
from vectorstore.qdrant import (
    QdrantSchemaError,
    client_from_settings,
    validate_collection_info,
)

logger = logging.getLogger(__name__)

CANONICAL_CHUNK_COUNT = 572
PROFILE_RERANK = "hybrid_rerank"
E5_WARMUP_QUERY = "món ăn Huế"
SCROLL_LIMIT = 128
SCROLL_PAYLOAD_FIELDS = [
    "chunk_id",
    "text",
    "embedding_model",
]


@dataclass(frozen=True)
class RetrievalStatus:
    """Immutable verified state of the retrieval service at startup."""

    collection_name: str
    point_count: int
    embedding_model: str
    embedding_dimension: int
    active_profile: str
    bm25_ready: bool
    reranker_ready: bool


def _query_embedder(settings):
    """Build the local query embedder from settings; model loads lazily."""
    embedding = settings["embedding"]
    return E5Embedder(
        model_id=embedding["model"],
        dimension=embedding["vector_size"],
        device=embedding["device"],
        batch_size=embedding["batch_size"],
    )


def _warm_embedder(embedder):
    """Load the real embedding model and verify one warm-up vector."""
    try:
        embedder.embed_query(E5_WARMUP_QUERY)
    except Exception as exc:
        raise ComponentNotReadyError(
            "embedder warm-up failed; the local model is unusable"
        ) from exc


def _scroll_all_payloads(client, collection_name, timeout):
    """Scroll every payload in bounded batches of 128, requesting only safe fields."""
    records = []
    offset = None
    while True:
        batch, offset = client.scroll(
            collection_name,
            limit=SCROLL_LIMIT,
            offset=offset,
            with_payload=SCROLL_PAYLOAD_FIELDS,
            with_vectors=False,
            timeout=timeout,
        )
        records.extend(batch)
        if offset is None:
            break
    return records


def _corpus_pairs(records, expected_model):
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
        pairs.append((chunk_id, text))
    return pairs


def _verify_collection(client, settings):
    """Verify collection existence, dense schema and canonical point count."""
    db = settings["vector_database"]
    collection_name = db["collection_name"]
    try:
        collection_exists = client.collection_exists(collection_name)
    except Exception as exc:
        raise RetrievalDependencyError("Qdrant collection check failed") from exc
    if not collection_exists:
        raise RetrievalConfigurationError(
            f"collection {collection_name} does not exist"
        )
    try:
        collection_info = client.get_collection(collection_name)
    except Exception as exc:
        raise RetrievalDependencyError("Qdrant collection info failed") from exc
    try:
        validate_collection_info(collection_info, settings, strict_dense_only=False)
    except QdrantSchemaError as exc:
        raise RetrievalConfigurationError(
            f"collection {collection_name} schema mismatch: {exc}"
        ) from exc
    try:
        actual_count = client.count(collection_name, exact=True).count
    except Exception as exc:
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


def build_retrieval_service(
    settings=None,
    *,
    client=None,
    embedder=None,
):
    """Verify collection and build RetrievalService directly with small runtime status."""
    from retrieval.service import RetrievalService

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
    except Exception as exc:
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

    hybrid_retriever = None
    if bm25_ready:
        try:
            records = _scroll_all_payloads(client, collection_name, db["timeout"])
        except Exception as exc:
            raise RetrievalDependencyError("Qdrant payload scroll failed") from exc
        corpus_pairs = _corpus_pairs(records, expected_model)
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
        except Exception as exc:
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
        reranker_instance = CrossEncoderReranker(
            model_id=reranking["model"], device=reranking["device"]
        )
        reranker_instance.load()
        reranker_instance.warm_up()

    status = RetrievalStatus(
        collection_name=collection_name,
        point_count=actual_count,
        embedding_model=expected_model,
        embedding_dimension=dimension,
        active_profile=profile,
        bm25_ready=bm25_ready,
        reranker_ready=reranker_ready,
    )

    logger.info(
        "retrieval service ready: profile=%s collection=%s points=%d bm25=%s reranker=%s",
        profile,
        collection_name,
        actual_count,
        bm25_ready,
        reranker_ready,
    )

    return RetrievalService(
        status=status,
        dense_retriever=dense_retriever,
        hybrid_retriever=hybrid_retriever,
        reranker=reranker_instance,
        rerank_top_k=reranking["top_k"],
    )
