"""Whole-chunk bounded context assembly with source mapping."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ContextResult:
    """Context text plus per-document source mapping in rank order."""

    context: str
    sources: list[dict]


class ContextBuilder:
    """Build a bounded context from whole chunks; never truncates content.

    The character budget includes the source label and separators. Empty
    documents are skipped, rank order is preserved and input documents are
    never mutated.
    """

    def __init__(self, max_documents=5, max_characters=3000):
        self._max_documents = max_documents
        self._max_characters = max_characters

    def build(self, documents):
        """Return context and sources; stop before the first chunk that does not fit."""
        parts = []
        sources = []
        length = 0
        for rank, document in enumerate(documents, start=1):
            text = document.text
            if not text.strip():
                continue
            metadata = document.metadata
            label = f"[{metadata.get('source', '')} | {metadata.get('section', '')}]"
            block = f"{label}\n{text}"
            separator = "\n\n" if parts else ""
            if (
                len(parts) >= self._max_documents
                or length + len(separator) + len(block) > self._max_characters
            ):
                break
            parts.append(block)
            length += len(separator) + len(block)
            sources.append(
                {
                    "chunk_id": metadata.get("chunk_id"),
                    "source": metadata.get("source"),
                    "title": metadata.get("title"),
                    "section": metadata.get("section"),
                    "rank": rank,
                }
            )
        return ContextResult(context="\n\n".join(parts), sources=sources)
