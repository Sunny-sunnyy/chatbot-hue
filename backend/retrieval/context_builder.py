"""Whole-chunk bounded context assembly with source mapping."""
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class ContextResult:
    """Context text plus per-document source mapping in rank order."""

    context: str
    sources: list[dict]


class ContextBuilder:
    """Build a bounded context from whole chunks; never truncates content.

    The context is a JSON array of evidence objects serialized with the
    standard library, so untrusted document text can never forge a
    structural field of its own: every block maps 1:1 to its chunk_id. The
    character budget includes the serialized array and its brackets. Empty
    documents are skipped, rank order is preserved and input documents are
    never mutated.
    """

    def __init__(self, max_documents=5, max_characters=3000):
        self._max_documents = max_documents
        self._max_characters = max_characters

    def build(self, documents):
        """Return context and sources; stop before the first chunk that does not fit."""
        blocks = []
        sources = []
        length = 0  # length of "[" + ",".join(serialized blocks) + "]"
        for rank, document in enumerate(documents, start=1):
            text = document.text
            if not text.strip():
                continue
            metadata = document.metadata
            block = {
                "chunk_id": metadata.get("chunk_id"),
                "source": metadata.get("source"),
                "section": metadata.get("section"),
                "title": metadata.get("title"),
                "text": text,
            }
            serialized = json.dumps(block, ensure_ascii=False, sort_keys=True)
            # Opening/closing brackets for the first item, ", " for the rest.
            overhead = 2
            if (
                len(blocks) >= self._max_documents
                or length + overhead + len(serialized) > self._max_characters
            ):
                break
            blocks.append(block)
            length += overhead + len(serialized)
            sources.append(
                {
                    "chunk_id": metadata.get("chunk_id"),
                    "source": metadata.get("source"),
                    "title": metadata.get("title"),
                    "section": metadata.get("section"),
                    "rank": rank,
                }
            )
        context = json.dumps(blocks, ensure_ascii=False, sort_keys=True)
        return ContextResult(context=context, sources=sources)
