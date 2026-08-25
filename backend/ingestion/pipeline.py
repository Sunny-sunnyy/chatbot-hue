"""Ingestion orchestration connecting chunking, embedding and Qdrant index."""
import copy
import logging

from core.logging_setup import setup_logging
from core.settings_loader import load_settings
from embedding.embedder import E5Embedder
from ingestion.chunking.markdown_chunker import chunk_foods_markdown
from vectorstore.points import build_points, validate_chunks
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

CANONICAL_CHUNK_COUNT = 572


def _build_embedder(settings):
    """Build the local dense embedder from settings."""
    embedding = settings["embedding"]
    return E5Embedder(
        model_id=embedding["model"],
        dimension=embedding["vector_size"],
        device=embedding["device"],
        batch_size=embedding["batch_size"],
    )


def run_ingestion(
    settings=None,
    *,
    collection_name=None,
    chunker=None,
    embedder=None,
    client=None,
):
    """Run the full Phase 2-4 ingestion and return a non-sensitive summary.

    Validation is pre-mutation: chunk IDs and the canonical count are checked
    before any embedding work, and build_points validates every dense vector and
    payload before the Qdrant client is created or the collection is touched.
    chunker/embedder/client are injectable for offline tests.
    """
    settings = copy.deepcopy(load_settings() if settings is None else settings)
    if collection_name is not None:
        if not isinstance(collection_name, str) or not collection_name.strip():
            raise ValueError("collection_name must be a non-empty exact name")
        settings["vector_database"]["collection_name"] = collection_name
    chunks = chunk_foods_markdown() if chunker is None else chunker()
    chunk_ids = validate_chunks(chunks)
    if len(chunk_ids) != CANONICAL_CHUNK_COUNT:
        raise ValueError(
            f"chunk count {len(chunk_ids)} != canonical {CANONICAL_CHUNK_COUNT}; "
            "report the corpus/chunking input diff instead of reindexing"
        )
    texts = [chunk["text"] for chunk in chunks]
    dense_embedder = embedder if embedder is not None else _build_embedder(settings)
    dense = dense_embedder.embed_documents(texts)
    points = build_points(
        chunks,
        dense,
        settings["embedding"]["model"],
        settings["vector_database"]["vector_size"],
    )
    client = client_from_settings(settings) if client is None else client
    ensure_collection(client, settings)
    validate_existing_points(client, settings, points, settings["embedding"]["model"])
    upsert_points(client, settings, points)
    validate_collection_info(
        client.get_collection(settings["vector_database"]["collection_name"]),
        settings,
    )
    actual_count = verify_point_count(client, settings, CANONICAL_CHUNK_COUNT)
    summary = {
        "collection_name": settings["vector_database"]["collection_name"],
        "embedding_model": settings["embedding"]["model"],
        "embedding_dimension": settings["vector_database"]["vector_size"],
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
