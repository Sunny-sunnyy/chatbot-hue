"""Citation validation and cited-source mapping for Phase 6."""
import re
from collections.abc import Sequence

from core.schema import CitationIntegrityError
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from retrieval.full_corpus_context import PackedSource

# Context gắn nhãn mỗi nguồn là "[Nguồn n]" nên model đôi khi trích đúng dạng đó thay vì "[n]";
# hai dạng cùng nghĩa (C-09, rà code 25/10).
CITATION_PATTERN = re.compile(r"\[\s*(?:nguồn\s*)?(\d+)\s*\]", re.IGNORECASE)


def normalize_citations(answer: str) -> str:
    """Đưa mọi citation về dạng "[n]" — dạng UI tách thành link."""
    return CITATION_PATTERN.sub(r"[\1]", answer)


def select_cited_sources(
    answer: str, sources: Sequence[PackedSource]
) -> tuple[PackedSource, ...]:
    markers = [int(value) for value in CITATION_PATTERN.findall(answer)]
    if INSUFFICIENT_ANSWER in answer:
        if markers:
            raise CitationIntegrityError("Fallback answer must not contain citations")
        if answer.strip() == INSUFFICIENT_ANSWER:
            return ()
    if not markers:
        raise CitationIntegrityError("Grounded answer has no citation")
    by_id = {source.id: source for source in sources}
    unknown = sorted(set(markers) - set(by_id))
    if unknown:
        raise CitationIntegrityError(f"Unknown citation IDs: {unknown}")
    return tuple(by_id[source_id] for source_id in sorted(set(markers)))
