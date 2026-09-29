"""Shared runtime data models and typed retrieval errors."""
from dataclasses import dataclass, field
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


FULL_CORPUS_DOMAINS = frozenset(
    {"foods", "heritages", "festivals", "performing_arts", "travel"}
)


def domain_for_source(source: str) -> str:
    """Derive canonical product domain from the first POSIX path component."""
    if not isinstance(source, str) or not source or source.startswith("/"):
        raise ValueError("source must be a non-empty relative POSIX path")
    if "\\" in source:
        raise ValueError("source must use POSIX separators")
    parts = source.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("source contains a non-canonical path component")
    domain = parts[0]
    if domain not in FULL_CORPUS_DOMAINS:
        raise ValueError(f"unsupported full-corpus domain: {domain}")
    return domain


def validate_chunk_id(source: str, chunk_id: str) -> int:
    """Validate that chunk_id serializes source#ordinal and return non-negative ordinal."""
    prefix = f"{source}#"
    if not isinstance(chunk_id, str) or not chunk_id.startswith(prefix):
        raise ValueError("chunk_id must serialize source#ordinal")
    ordinal_text = chunk_id[len(prefix):]
    if not ordinal_text.isdecimal():
        raise ValueError("chunk ordinal must be a non-negative decimal integer")
    ordinal = int(ordinal_text)
    if str(ordinal) != ordinal_text:
        raise ValueError("chunk ordinal must use canonical decimal form")
    return ordinal


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
    domain: str = field(init=False)

    def __post_init__(self) -> None:
        self.domain = domain_for_source(self.source)

    @property
    def point_id(self) -> str:
        """Deterministic Qdrant UUID5 point ID."""
        return point_id_for_chunk_id(self.chunk_id)

    def to_qdrant_payload(self) -> dict[str, Any]:
        """Qdrant payload containing exactly the seven required fields from Written Spec."""
        return {
            "search_text": self.search_text,
            "source": self.source,
            "title": self.title,
            "heading_path": list(self.heading_path),
            "evidence_parts": [part.to_dict() for part in self.evidence_parts],
            "chunk_id": self.chunk_id,
            "domain": self.domain,
        }
