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
    source: str = ""  # đường dẫn file của đoạn (payload `source`) — chỉ code dùng (H4c, Phase 9 B1 D8); không vào chữ ngữ cảnh


@dataclass(frozen=True)
class PackedContext:
    text: str
    sources: tuple[PackedSource, ...]
    input_tokens: int
    document_ids: tuple[str, ...] = ()  # chunk_id của các đoạn đã vào ngữ cảnh — để lần tìm sau bỏ trùng (Phase 9 B2 D5)


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

    def _token_count(self, query: str, context: str, today: str | None = None, instructions: str | None = None) -> int:
        messages = build_answer_messages(query, context, today)
        if instructions is not None:  # B2 D5: đường trợ lý có lời dặn riêng (dài hơn) — đếm bằng chính lời dặn gửi đi
            messages[0]["content"] = instructions
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
            source=str(metadata.get("source") or ""),
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
        self, query: str, documents: Sequence[RetrievedDocument], today: str | None = None, *,
        first_id: int = 1, prior_context: str = "", skip_ids: frozenset[str] = frozenset(), instructions: str | None = None,
    ) -> PackedContext:
        """`today`: dòng ngày sẽ đứng đầu tin nhắn gửi model (B1 D7) — đếm cùng một chuỗi với chuỗi gửi đi.
        Lần tìm thêm trong một lượt (Phase 9 B2 D5): đánh số từ `first_id`, bỏ đoạn `skip_ids` đã có, và đếm ngân sách **chung** —
        `prior_context` (ngữ cảnh các lần trước) + khối mới, bằng `instructions` của trợ lý. Hết ngân sách ở lần tìm thêm ⇒ ít / 0 đoạn,
        không lỗi (chỉ lần đầu mới `ContextBudgetError`). Mặc định = một lần tìm như B1 (giống byte)."""
        blocks: list[str] = []
        sources: list[PackedSource] = []
        ids: list[str] = []

        def counted(new_text: str) -> int:
            context = "\n\n".join(part for part in (prior_context, new_text) if part)
            return self._token_count(query, context, today, instructions)

        input_tokens = counted("")
        for document in documents:
            if len(sources) >= self._max_documents:
                break
            if document.id in skip_ids:
                continue
            source = self._source(document, first_id + len(sources))
            if source is None:
                continue
            candidate_text = "\n\n".join([*blocks, self._block(source)])
            candidate_tokens = counted(candidate_text)
            fits = candidate_tokens + self._reserved + self._margin <= self._context_limit
            if not fits:
                if not sources and not prior_context:
                    raise ContextBudgetError("Highest-ranked evidence block exceeds budget")
                break
            blocks.append(self._block(source))
            sources.append(source)
            ids.append(document.id)
            input_tokens = candidate_tokens
        return PackedContext("\n\n".join(blocks), tuple(sources), input_tokens, tuple(ids))
