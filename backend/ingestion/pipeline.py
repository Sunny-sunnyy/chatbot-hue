"""Ingestion orchestration connecting chunking, embedding and Qdrant index."""
import logging

from core.logging_setup import setup_logging
from core.settings_loader import load_settings
from embedding.batch_embed import embed_in_batches
from embedding.embedder import SentenceTransformerEmbedder
from embedding.sparse_embedder import SparseEmbedder
from ingestion.chunking.markdown_chunker import chunk_foods_markdown
from vectorstore.hybrid_index import build_points, validate_chunks
from vectorstore.qdrant import (
    client_from_settings,
    ensure_collection,
    validate_collection_info,
)
from vectorstore.upsert import (
    upsert_points,
    validate_existing_points,
    verify_point_count,
)

logger = logging.getLogger(__name__)

# Canonical Phase 2 corpus size; changing it requires a user-approved
# contract change, never a silent pipeline adjustment.
CANONICAL_CHUNK_COUNT = 572


def _reject_reset(settings):
    """Fail closed when config requests reset; reset is a separate command."""
    db = settings["vector_database"]
    if db["reset_collection"]:
        raise ValueError(
            "vector_database.reset_collection must be false; run "
            "`uv run python -m vectorstore.reset` with user approval "
            "to delete the collection"
        )


def _build_embedder(settings):
    """Build the local dense embedder from settings."""
    embedding = settings["embedding"]
    return SentenceTransformerEmbedder(
        model_id=embedding["model"],
        dimension=embedding["vector_size"],
        device=embedding["device"],
        batch_size=embedding["batch_size"],
    )


def run_ingestion(settings=None, *, chunker=None, embedder=None, client=None):
    """Run the full Phase 2-4 ingestion and return a non-sensitive summary.

    Validation is pre-mutation: chunk IDs and the canonical count are checked
    before any embedding work, and build_points validates every dense/sparse
    vector and payload before the Qdrant client is created or the collection
    is touched. chunker/embedder/client are injectable for offline tests.
    """
    settings = load_settings() if settings is None else settings
    _reject_reset(settings)
    embedding = settings["embedding"]
    db = settings["vector_database"]
    chunks = chunk_foods_markdown() if chunker is None else chunker()
    chunk_ids = validate_chunks(chunks)
    if len(chunk_ids) != CANONICAL_CHUNK_COUNT:
        raise ValueError(
            f"chunk count {len(chunk_ids)} != canonical {CANONICAL_CHUNK_COUNT}; "
            "report the corpus/chunking input diff instead of reindexing"
        )
    texts = [chunk["text"] for chunk in chunks]
    sparse_embedder = SparseEmbedder().fit(texts)
    dense = embed_in_batches(
        embedder if embedder is not None else _build_embedder(settings),
        texts,
        embedding["batch_size"],
    )
    sparse = [sparse_embedder.encode(text) for text in texts]
    points = build_points(chunks, dense, sparse, embedding["model"], db["vector_size"])
    client = client_from_settings(settings) if client is None else client
    ensure_collection(client, settings)
    validate_existing_points(client, settings, points, embedding["model"])
    upsert_points(client, settings, points)
    validate_collection_info(client.get_collection(db["collection_name"]), settings)
    actual_count = verify_point_count(client, settings, CANONICAL_CHUNK_COUNT)
    summary = {
        "collection_name": db["collection_name"],
        "embedding_model": embedding["model"],
        "embedding_dimension": db["vector_size"],
        "chunk_count": CANONICAL_CHUNK_COUNT,
        "point_count": actual_count,
    }
    logger.info("ingestion summary: %s", summary)
    return summary


def main():
    """Run ingestion with settings from disk and print the summary."""
    setup_logging()
    print(run_ingestion())


if __name__ == "__main__":
    main()
