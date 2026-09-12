"""Shared runtime data models and typed retrieval errors."""
from dataclasses import dataclass
from typing import Any
import uuid


class InvalidQueryError(ValueError):
    """Raised when a retrieval query is empty or whitespace-only."""


class RetrievalConfigurationError(ValueError):
    """Raised when the active profile or retrieval configuration is invalid."""


class ComponentNotReadyError(RuntimeError):
    """Raised when a required component is missing or the snapshot is stale."""


class RetrievalDependencyError(RuntimeError):
    """Raised when an embedder, Qdrant or reranker call fails."""


class GenerationError(RuntimeError):
    """Raised when answer generation cannot return a valid answer."""


@dataclass
class RetrievedDocument:
    """Document returned by retrieval for prompt context building."""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]


# UUID5 namespace for deterministic Qdrant point IDs
POINT_ID_NAMESPACE = uuid.NAMESPACE_URL


def point_id_for_chunk_id(chunk_id: str) -> str:
    """Generate deterministic UUID5 string from chunk_id."""
    return str(uuid.uuid5(POINT_ID_NAMESPACE, f"hue-rag:{chunk_id}"))


@dataclass(frozen=True)
class EvidencePart:
    """Exact sliced evidence part from normalized LF source text."""

    role: str  # "body" | "header" | "condition"
    start: int  # Zero-based Unicode code-point offset start [start, end)
    end: int    # Zero-based Unicode code-point offset end (exclusive)
    text: str   # Exact sliced substring: source_text[start:end] == text

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "start": self.start,
            "end": self.end,
            "text": self.text,
        }


@dataclass
class FullCorpusChunk:
    """Canonical Full-Corpus Chunk for Wave 1 and representation contract."""

    chunk_id: str  # Serialized pair: (source, chunk_ordinal), e.g. "path/to/file.md#0"
    source: str    # Relative POSIX path to knowledge-base-hue/
    title: str     # H1 title of the document
    heading_path: list[str]  # Ancestor headings excluding H1, e.g. ["H2", "H3"]
    evidence_parts: list[EvidencePart]
    search_text: str  # Representation A search text

    @property
    def point_id(self) -> str:
        """Deterministic Qdrant UUID5 point ID."""
        return point_id_for_chunk_id(self.chunk_id)

    def to_qdrant_payload(self) -> dict[str, Any]:
        """Qdrant payload containing exactly the five required fields from Written Spec."""
        return {
            "search_text": self.search_text,
            "source": self.source,
            "title": self.title,
            "heading_path": list(self.heading_path),
            "evidence_parts": [part.to_dict() for part in self.evidence_parts],
        }
