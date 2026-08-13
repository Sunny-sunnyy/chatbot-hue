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


class GeneratorNotConfiguredError(RuntimeError):
    """Raised when the OpenAI key or generator configuration is missing."""


class GeneratorTimeoutError(RuntimeError):
    """Raised when answer generation exceeds the provider timeout."""


class GeneratorUnavailableError(RuntimeError):
    """Raised when the OpenAI provider call fails (connection/API error)."""


class InvalidGeneratorOutputError(RuntimeError):
    """Raised when the model output is blank, out of schema or references
    unknown source IDs."""


@dataclass
class RetrievedDocument:
    """Document returned by retrieval for prompt context building."""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]
