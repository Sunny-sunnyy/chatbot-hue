"""Shared runtime data models and typed retrieval errors."""
from dataclasses import dataclass
from typing import Any


class InvalidQueryError(ValueError):
    """Raised when a retrieval query is empty or whitespace-only."""


class RetrievalConfigurationError(ValueError):
    """Raised when the active profile or retrieval configuration is invalid."""


class ComponentNotReadyError(RuntimeError):
    """Raised when a required component is missing or the snapshot is stale."""


class RetrievalDependencyError(RuntimeError):
    """Raised when an embedder, Qdrant or reranker call fails."""


@dataclass
class RetrievedDocument:
    """Document returned by retrieval for prompt context building."""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]
