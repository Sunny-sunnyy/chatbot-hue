"""Bounded batching helpers for embedder consumers."""
from embedding.base import BaseEmbedder


def batches(texts, batch_size):
    """Yield consecutive slices of texts of at most batch_size items."""
    for start in range(0, len(texts), batch_size):
        yield texts[start : start + batch_size]


def embed_in_batches(embedder: BaseEmbedder, texts, batch_size):
    """Embed all texts in bounded batches, preserving input order."""
    if batch_size <= 0:
        raise ValueError(f"batch_size must be positive, got {batch_size}")
    if not texts:
        return []
    vectors = []
    for batch in batches(texts, batch_size):
        vectors.extend(embedder.embed_documents(batch))
    return vectors
