"""Deterministic Representation B assembly and length checks for Phase 6."""
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class RepresentationBResult:
    search_text: str
    used_representation_b: bool
    reason: str


def build_representation_b_search_text(
    representation_a: str,
    search_context: str,
    *,
    fits_all_embedding_tokenizers: Callable[[str], bool],
) -> RepresentationBResult:
    base = representation_a.strip()
    addition = search_context.strip()
    if not base or not addition:
        raise ValueError("Representation A and generated search context must be non-empty")
    combined = f"{base}\n\n[Ngữ cảnh tìm kiếm bổ sung]\n{addition}"
    if not fits_all_embedding_tokenizers(combined):
        return RepresentationBResult(
            search_text=base,
            used_representation_b=False,
            reason="combined_text_exceeds_embedding_limit",
        )
    return RepresentationBResult(
        search_text=combined,
        used_representation_b=True,
        reason="representation_b_used",
    )
