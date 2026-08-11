"""Base embedder interface and shared vector validation."""
from abc import ABC, abstractmethod

import numpy as np


class EmbeddingError(ValueError):
    """Raised for invalid embedder input or output."""


ZERO_NORM_EPSILON = 1e-12


class BaseEmbedder(ABC):
    """Minimal embedder contract consumed by ingestion and retrieval."""

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Actual provider/model ID for logging and benchmark metadata."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Expected dense vector dimension."""

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed texts into normalized vectors, preserving input order."""

    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        """Embed a single query into one normalized vector."""

    def _validate_query(self, query):
        """Reject empty or whitespace-only queries."""
        if not isinstance(query, str) or not query.strip():
            raise EmbeddingError("query must be a non-empty string")

    def _process_vectors(self, raw_vectors):
        """Validate shape/finiteness, L2-normalize and return list[list[float]].

        Dimension mismatch and zero-norm vectors fail fast: vectors are never
        padded, truncated or silently re-routed to another model, and a zero
        vector (norm ~ 0) cannot be a normalized dense vector.
        """
        array = np.asarray(raw_vectors, dtype=float)
        if array.ndim != 2 or array.shape[1] != self.dimension:
            raise EmbeddingError(
                f"model produced shape {array.shape}; dimension mismatch with "
                f"configured {self.dimension}"
            )
        if not np.isfinite(array).all():
            raise EmbeddingError("embedder produced non-finite vector values")
        norms = np.linalg.norm(array, axis=1)
        if np.any(norms < ZERO_NORM_EPSILON):
            raise EmbeddingError("embedder produced a zero-norm vector")
        return (array / norms[:, None]).tolist()
