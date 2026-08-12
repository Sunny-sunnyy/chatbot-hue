"""Reranker interface contract."""
from abc import ABC, abstractmethod


class BaseReranker(ABC):
    """Minimal reranker contract consumed by the retrieval service."""

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Actual provider/model ID for logging and benchmark metadata."""

    @abstractmethod
    def rerank(self, query, documents, top_k):
        """Score query-document pairs and return the top-k reordered documents."""
