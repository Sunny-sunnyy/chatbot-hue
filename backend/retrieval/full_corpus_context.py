"""Evidence-only token packing for Phase 6 full-corpus generation."""
from dataclasses import dataclass
from typing import Any, Sequence

from core.schema import ContextBudgetError, RetrievedDocument
from llm.full_corpus_prompt import build_answer_messages


@dataclass(frozen=True)
class PackedSource:
    id: int
    title: str
    heading_path: tuple[str, ...]
    excerpts: tuple[str, ...]


@dataclass(frozen=True)
class PackedContext:
    text: str
    sources: tuple[PackedSource, ...]
    input_tokens: int


class FullCorpusContextBuilder:
    def __init__(
        self,
        tokenizer: Any,
        *,
        context_limit: int = 16384,
        reserved_output_tokens: int = 2048,
        safety_margin: int = 512,
        max_documents: int = 5,
    ) -> None:
        self._tokenizer = tokenizer
        self._context_limit = context_limit
        self._reserved = reserved_output_tokens
        self._margin = safety_margin
        self._max_documents = max_documents

    def _token_count(self, query: str, context: str) -> int:
        if hasattr(self._tokenizer, "apply_chat_template"):
            token_ids = self._tokenizer.apply_chat_template(
                build_answer_messages(query, context),
                tokenize=True,
                add_generation_prompt=True,
            )
            return len(token_ids)
        messages = build_answer_messages(query, context)
        num_tokens = 3
        for message in messages:
            num_tokens += 3
            for key, value in message.items():
                num_tokens += len(self._tokenizer.encode(value))
        return num_tokens

    @staticmethod
    def _source(document: RetrievedDocument, number: int) -> PackedSource | None:
        metadata = document.metadata
        raw_parts = metadata.get("evidence_parts") or []
        excerpts = tuple(
            part["text"].strip()
            for part in raw_parts
            if isinstance(part, dict)
            and isinstance(part.get("text"), str)
            and part["text"].strip()
        )
        if not excerpts:
            return None
        heading = metadata.get("heading_path") or []
        return PackedSource(
            id=number,
            title=str(metadata.get("title") or ""),
            heading_path=tuple(str(item) for item in heading),
            excerpts=excerpts,
        )

    @staticmethod
    def _block(source: PackedSource) -> str:
        section = " > ".join(source.heading_path)
        evidence = "\n".join(f"- {text}" for text in source.excerpts)
        return (
            f"[Nguồn {source.id}]\n"
            f"Tiêu đề: {source.title}\n"
            f"Mục: {section}\n"
            f"Bằng chứng:\n{evidence}"
        )

    def build(
        self, query: str, documents: Sequence[RetrievedDocument]
    ) -> PackedContext:
        blocks: list[str] = []
        sources: list[PackedSource] = []
        input_tokens = self._token_count(query, "")
        for document in documents:
            if len(sources) >= self._max_documents:
                break
            source = self._source(document, len(sources) + 1)
            if source is None:
                continue
            candidate_text = "\n\n".join([*blocks, self._block(source)])
            candidate_tokens = self._token_count(query, candidate_text)
            fits = candidate_tokens + self._reserved + self._margin <= self._context_limit
            if not fits:
                if not sources:
                    raise ContextBudgetError("Highest-ranked evidence block exceeds budget")
                break
            blocks.append(self._block(source))
            sources.append(source)
            input_tokens = candidate_tokens
        return PackedContext("\n\n".join(blocks), tuple(sources), input_tokens)
