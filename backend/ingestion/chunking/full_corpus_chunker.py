"""Full-corpus Markdown chunker and Representation A builder for Wave 1.

Implements semantic grouping/splitting, condition attachment outside corpus,
source locator verification, representation A text construction, sentence-boundary
splitting for oversized blocks, and deterministic chunk ID / UUID5 generation.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Callable

try:
    from backend.core.schema import EvidencePart, FullCorpusChunk, point_id_for_chunk_id
    from backend.core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings
    from backend.ingestion.chunking.markdown_blocks import (
        MarkdownBlock,
        ParsedDocument,
        TableInfo,
        TableRowInfo,
        parse_markdown_blocks,
    )
    from backend.ingestion.source_state import (
        discover_full_corpus_files,
        read_source_lf,
    )
except ModuleNotFoundError:
    from core.schema import EvidencePart, FullCorpusChunk, point_id_for_chunk_id
    from core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings
    from ingestion.chunking.markdown_blocks import (
        MarkdownBlock,
        ParsedDocument,
        TableInfo,
        TableRowInfo,
        parse_markdown_blocks,
    )
    from ingestion.source_state import (
        discover_full_corpus_files,
        read_source_lf,
    )


def extract_sentence_spans(text: str, base_offset: int = 0) -> list[tuple[int, int, str]]:
    """Extract zero-based sentence spans [start, end) and text from string.

    Splits at sentence ends (. ! ?) followed by whitespace or end of string.
    Preserves exact source offsets and ensures text == source_lf[start:end].
    """
    pattern = re.compile(r'([.!?]["\'\)\]]*)(?:\s+|$)')
    sentences = []
    curr = 0
    while curr < len(text):
        while curr < len(text) and text[curr].isspace():
            curr += 1
        if curr >= len(text):
            break
        m = pattern.search(text, curr)
        if m:
            sent_end = m.end(1)
            sent_text = text[curr:sent_end]
            sentences.append((base_offset + curr, base_offset + sent_end, sent_text))
            curr = m.end()
        else:
            sent_text = text[curr:].rstrip()
            sentences.append((base_offset + curr, base_offset + curr + len(sent_text), sent_text))
            break
    return sentences


def build_representation_a_search_text(
    title: str,
    heading_path: list[str],
    evidence_parts: list[EvidencePart],
) -> str:
    """Construct Representation A search_text from title, heading path, and evidence parts.

    Formatted as:
    title
    [ancestor > path]
    [condition / header / body parts]
    """
    lines = [title]
    if heading_path:
        lines.append(" > ".join(heading_path))

    parts_out: list[str] = []
    for i, part in enumerate(evidence_parts):
        if part.role == "header":
            parts_out.append(part.text)
        elif part.role == "body" and i > 0 and evidence_parts[i - 1].role == "header":
            # Direct table row, sub-item, or sentence body following header/label: connect with single newline
            prev = parts_out.pop()
            parts_out.append(f"{prev}\n{part.text}")
        else:
            parts_out.append(part.text)

    body_text = "\n\n".join(parts_out)
    return "\n".join(lines) + "\n" + body_text


def match_block_selector(block: MarkdownBlock, selector: dict[str, Any]) -> bool:
    """Exact matcher for block selector {heading_path, block_type, exact_text}.

    Strict exact matching only: no wildcards, no aliases, no fallbacks.
    """
    return (
        block.heading_path == selector["heading_path"]
        and block.block_type == selector["block_type"]
        and block.text == selector["exact_text"]
    )


def _validate_selector_schema(sel: Any, context: str) -> None:
    """Validate selector dictionary schema fail-closed."""
    if not isinstance(sel, dict):
        raise ValueError(f"{context} must be a dictionary")
    for field in ("heading_path", "block_type", "exact_text"):
        if field not in sel:
            raise ValueError(f"{context} missing required field '{field}'")
    heading_path = sel["heading_path"]
    if not isinstance(heading_path, list) or not all(isinstance(p, str) for p in heading_path):
        raise ValueError(f"{context} 'heading_path' must be a list of strings")
    block_type = sel["block_type"]
    if not isinstance(block_type, str) or not block_type.strip():
        raise ValueError(f"{context} 'block_type' must be a non-empty string")
    exact_text = sel["exact_text"]
    if not isinstance(exact_text, str) or not exact_text.strip():
        raise ValueError(f"{context} 'exact_text' must be a non-empty string")


class ConditionManager:
    """Manages declarative condition attachments outside corpus."""

    def __init__(
        self,
        conditions_path: Path | str | None = None,
        settings: dict[str, Any] | None = None,
    ) -> None:
        if conditions_path is None:
            fc = get_full_corpus_settings(settings)
            rel_cond = fc.get("conditions_file", "config/full_corpus_conditions.json")
            conditions_path = (BACKEND_DIR / rel_cond).resolve()

        self.path = Path(conditions_path)
        if not self.path.is_file():
            raise FileNotFoundError(f"Conditions file not found: {self.path}")

        with self.path.open("r", encoding="utf-8") as f:
            self.rules: list[dict[str, Any]] = json.load(f)

        self._validate_rules_schema()

    def _validate_rules_schema(self) -> None:
        """Validate declarative conditions JSON schema fail-closed."""
        if not isinstance(self.rules, list):
            raise ValueError("Conditions configuration must be a list of rule dictionaries")
        for r_idx, rule in enumerate(self.rules):
            if not isinstance(rule, dict):
                raise ValueError(f"Rule {r_idx} must be a dictionary")
            source = rule.get("source")
            if not source or not isinstance(source, str):
                raise ValueError(f"Rule {r_idx} missing valid 'source' string")
            _validate_selector_schema(rule.get("condition"), f"Rule {r_idx} 'condition'")
            targets = rule.get("targets")
            if not isinstance(targets, list) or not targets:
                raise ValueError(f"Rule {r_idx} missing non-empty 'targets' list")
            for t_idx, tgt in enumerate(targets):
                _validate_selector_schema(tgt, f"Rule {r_idx} target {t_idx}")

    def validate_corpus_rules(
        self,
        discovered_files: list[str],
        docs_by_source: dict[str, ParsedDocument],
    ) -> list[str]:
        """Validate all condition rules across the discovered corpus files.

        Fails closed with blocking errors if any rule's source is missing, or if any
        condition or target selector fails to match exactly one block.
        """
        errors: list[str] = []
        discovered_set = set(discovered_files)

        for r_idx, rule in enumerate(self.rules):
            source = rule["source"]
            if source not in discovered_set:
                errors.append(
                    f"Condition rule {r_idx}: source {source!r} is not in discovered files."
                )
                continue

            doc = docs_by_source.get(source)
            if doc is None:
                errors.append(f"Condition rule {r_idx}: parsed document not found for {source!r}.")
                continue

            # Validate condition selector exact-one match
            cond_sel = rule["condition"]
            matched_cond = [b for b in doc.blocks if match_block_selector(b, cond_sel)]
            if len(matched_cond) == 0:
                errors.append(
                    f"Condition rule {r_idx} in {source}: Condition selector missing. "
                    f"Expected path={cond_sel['heading_path']!r}, type={cond_sel['block_type']!r}, text={cond_sel['exact_text'][:40]!r}"
                )
            elif len(matched_cond) > 1:
                errors.append(
                    f"Condition rule {r_idx} in {source}: Duplicate condition selector matches ({len(matched_cond)})."
                )

            # Validate target selectors exact-one match
            for t_idx, tgt_sel in enumerate(rule.get("targets", [])):
                matched_tgt = [b for b in doc.blocks if match_block_selector(b, tgt_sel)]
                if len(matched_tgt) == 0:
                    errors.append(
                        f"Condition rule {r_idx} target {t_idx} in {source}: Target selector missing. "
                        f"Expected path={tgt_sel['heading_path']!r}, type={tgt_sel['block_type']!r}"
                    )
                elif len(matched_tgt) > 1:
                    errors.append(
                        f"Condition rule {r_idx} target {t_idx} in {source}: Duplicate target selector matches ({len(matched_tgt)})."
                    )

        return errors

    def validate_and_resolve_for_doc(
        self,
        doc: ParsedDocument,
    ) -> tuple[dict[int, list[EvidencePart]], set[int], list[str]]:
        """Resolve condition rules for a specific document.

        Returns:
            - target_attachments: map of target_block_index -> list of condition EvidenceParts
            - condition_block_indices: set of block indices that act as condition sources
            - errors: list of selector mismatch / missing / duplicate errors
        """
        target_attachments: dict[int, list[EvidencePart]] = {}
        condition_block_indices: set[int] = set()
        errors: list[str] = []

        file_rules = [r for r in self.rules if r.get("source") == doc.source]
        if not file_rules:
            return target_attachments, condition_block_indices, errors

        for r_idx, rule in enumerate(file_rules):
            cond_sel = rule.get("condition", {})
            matched_cond_indices = [
                b_idx for b_idx, b in enumerate(doc.blocks)
                if match_block_selector(b, cond_sel)
            ]

            if len(matched_cond_indices) == 0:
                errors.append(
                    f"Condition rule {r_idx} in {doc.source}: Condition selector missing. "
                    f"Expected path={cond_sel.get('heading_path')!r}, type={cond_sel.get('block_type')!r}, text={str(cond_sel.get('exact_text'))[:40]!r}"
                )
                continue
            if len(matched_cond_indices) > 1:
                errors.append(
                    f"Condition rule {r_idx} in {doc.source}: Duplicate condition selector matches ({len(matched_cond_indices)})."
                )
                continue

            c_idx = matched_cond_indices[0]
            condition_block_indices.add(c_idx)
            cond_block = doc.blocks[c_idx]
            cond_part = EvidencePart(
                role="condition",
                start=cond_block.start,
                end=cond_block.end,
                text=cond_block.text,
            )

            for t_idx, tgt_sel in enumerate(rule.get("targets", [])):
                matched_tgt_indices = [
                    b_idx for b_idx, b in enumerate(doc.blocks)
                    if match_block_selector(b, tgt_sel)
                ]

                if len(matched_tgt_indices) == 0:
                    errors.append(
                        f"Condition rule {r_idx} target {t_idx} in {doc.source}: Target selector missing. "
                        f"Expected path={tgt_sel.get('heading_path')!r}, type={tgt_sel.get('block_type')!r}"
                    )
                    continue
                if len(matched_tgt_indices) > 1:
                    errors.append(
                        f"Condition rule {r_idx} target {t_idx} in {doc.source}: Duplicate target selector matches ({len(matched_tgt_indices)})."
                    )
                    continue

                tgt_b_idx = matched_tgt_indices[0]
                if tgt_b_idx not in target_attachments:
                    target_attachments[tgt_b_idx] = []
                target_attachments[tgt_b_idx].append(cond_part)

        return target_attachments, condition_block_indices, errors


_CHECKER_CACHE: dict[tuple[Any, ...], Callable[[str], bool]] = {}


def get_default_tokenizer_checker(settings: dict[str, Any] | None = None) -> Callable[[str], bool]:
    """Return cached default 3-model offline tokenizer limit checker keyed by exact settings.

    Fails closed if any required tokenizer cannot be loaded offline.
    """
    try:
        from backend.ingestion.preview import load_tokenizers, count_tokens_for_chunk
    except ModuleNotFoundError:
        from ingestion.preview import load_tokenizers, count_tokens_for_chunk

    fc_settings = get_full_corpus_settings(settings)
    models_cfg = fc_settings.get("embedding_models", [])
    cache_key = tuple(
        (
            spec.get("id"),
            spec.get("max_tokens"),
            spec.get("prefix", ""),
            spec.get("word_segment", False),
        )
        for spec in models_cfg
    )

    if cache_key in _CHECKER_CACHE:
        return _CHECKER_CACHE[cache_key]

    tokenizers, errors = load_tokenizers(settings)
    if errors:
        raise RuntimeError(
            f"Failed to load required offline tokenizers (fail-closed): {errors}"
        )

    def checker(search_text: str) -> bool:
        counts = count_tokens_for_chunk(search_text, tokenizers, models_cfg)
        for spec in models_cfg:
            if counts.get(spec["id"], 0) > spec["max_tokens"]:
                return False
        return True

    _CHECKER_CACHE[cache_key] = checker
    return checker


def chunk_document(
    doc: ParsedDocument,
    condition_manager: ConditionManager | None = None,
    is_fits_tokenizer_fn: Callable[[str], bool] | None = None,
) -> tuple[list[FullCorpusChunk], list[str]]:
    """Chunk a parsed document into canonical FullCorpusChunks.

    Adheres to the approved Written Spec and Plan:
    - Tables: kept whole when fitting, split row-by-row with header and conditions when oversized.
    - Nested lists: kept whole when fitting, split across sub-items with exact parent label when oversized.
    - Single paragraphs and list items: kept whole when fitting, split at source sentence boundaries when oversized.
    - Preserves exact source slices [start, end) without blind budget-fill merging.
    """
    errors: list[str] = []
    if condition_manager is None:
        condition_manager = ConditionManager()
    if is_fits_tokenizer_fn is None:
        is_fits_tokenizer_fn = get_default_tokenizer_checker()

    target_attachments, condition_block_indices, cond_errors = (
        condition_manager.validate_and_resolve_for_doc(doc)
    )
    errors.extend(cond_errors)

    chunks: list[FullCorpusChunk] = []
    chunk_ordinal = 0

    idx = 0
    while idx < len(doc.blocks):
        block = doc.blocks[idx]

        # Skip blocks that serve purely as attached conditions
        if idx in condition_block_indices:
            idx += 1
            continue

        attached_conds = target_attachments.get(idx, [])
        lead_conds = [c for c in attached_conds if c.start < block.start]
        trailing_conds = [c for c in attached_conds if c.start > block.start]

        # Case 1: Table
        if block.block_type == "table":
            table_info = block.table_info
            table_part = EvidencePart(
                role="body",
                start=block.start,
                end=block.end,
                text=block.text,
            )
            whole_parts = lead_conds + [table_part] + trailing_conds
            whole_search_text = build_representation_a_search_text(
                doc.title, block.heading_path, whole_parts
            )

            fits_whole = True
            if is_fits_tokenizer_fn is not None:
                fits_whole = is_fits_tokenizer_fn(whole_search_text)

            if fits_whole or not table_info or not table_info.rows:
                chunk_id = f"{doc.source}#{chunk_ordinal}"
                chunk_ordinal += 1
                chunks.append(
                    FullCorpusChunk(
                        chunk_id=chunk_id,
                        source=doc.source,
                        title=doc.title,
                        heading_path=list(block.heading_path),
                        evidence_parts=whole_parts,
                        search_text=whole_search_text,
                    )
                )
            else:
                # Split table row by row
                header_part = EvidencePart(
                    role="header",
                    start=table_info.header_start,
                    end=table_info.header_end,
                    text=table_info.header_text,
                )
                for row in table_info.rows:
                    row_part = EvidencePart(
                        role="body",
                        start=row.start,
                        end=row.end,
                        text=row.text,
                    )
                    row_parts = lead_conds + [header_part, row_part] + trailing_conds
                    row_search_text = build_representation_a_search_text(
                        doc.title, block.heading_path, row_parts
                    )
                    chunk_id = f"{doc.source}#{chunk_ordinal}"
                    chunk_ordinal += 1
                    chunks.append(
                        FullCorpusChunk(
                            chunk_id=chunk_id,
                            source=doc.source,
                            title=doc.title,
                            heading_path=list(block.heading_path),
                            evidence_parts=row_parts,
                            search_text=row_search_text,
                        )
                    )
            idx += 1
            continue

        # Case 2: List item with nested sub-items
        if block.block_type == "list_item" and block.list_item_info and block.list_item_info.sub_items:
            single_part = EvidencePart(
                role="body",
                start=block.start,
                end=block.end,
                text=block.text,
            )
            whole_parts = lead_conds + [single_part] + trailing_conds
            whole_search_text = build_representation_a_search_text(
                doc.title, block.heading_path, whole_parts
            )

            fits_whole = True
            if is_fits_tokenizer_fn is not None:
                fits_whole = is_fits_tokenizer_fn(whole_search_text)

            if fits_whole:
                chunk_id = f"{doc.source}#{chunk_ordinal}"
                chunk_ordinal += 1
                chunks.append(
                    FullCorpusChunk(
                        chunk_id=chunk_id,
                        source=doc.source,
                        title=doc.title,
                        heading_path=list(block.heading_path),
                        evidence_parts=whole_parts,
                        search_text=whole_search_text,
                    )
                )
            else:
                # Split nested sub-items, retaining parent label
                first_sub = block.list_item_info.sub_items[0]
                parent_text = doc.lf_text[block.start:first_sub.start].rstrip("\n ")
                parent_end = block.start + len(parent_text)
                parent_part = EvidencePart(
                    role="header",
                    start=block.start,
                    end=parent_end,
                    text=parent_text,
                )
                for sub in block.list_item_info.sub_items:
                    sub_part = EvidencePart(
                        role="body",
                        start=sub.start,
                        end=sub.end,
                        text=sub.text,
                    )
                    sub_parts = lead_conds + [parent_part, sub_part] + trailing_conds
                    sub_search_text = build_representation_a_search_text(
                        doc.title, block.heading_path, sub_parts
                    )
                    chunk_id = f"{doc.source}#{chunk_ordinal}"
                    chunk_ordinal += 1
                    chunks.append(
                        FullCorpusChunk(
                            chunk_id=chunk_id,
                            source=doc.source,
                            title=doc.title,
                            heading_path=list(block.heading_path),
                            evidence_parts=sub_parts,
                            search_text=sub_search_text,
                        )
                    )
            idx += 1
            continue

        # Case 3: Single paragraph, list item without sub-items, or blockquote
        single_part = EvidencePart(
            role="body",
            start=block.start,
            end=block.end,
            text=block.text,
        )
        whole_parts = lead_conds + [single_part] + trailing_conds
        whole_search_text = build_representation_a_search_text(
            doc.title, block.heading_path, whole_parts
        )

        fits_whole = True
        if is_fits_tokenizer_fn is not None:
            fits_whole = is_fits_tokenizer_fn(whole_search_text)

        if fits_whole:
            chunk_id = f"{doc.source}#{chunk_ordinal}"
            chunk_ordinal += 1
            chunks.append(
                FullCorpusChunk(
                    chunk_id=chunk_id,
                    source=doc.source,
                    title=doc.title,
                    heading_path=list(block.heading_path),
                    evidence_parts=whole_parts,
                    search_text=whole_search_text,
                )
            )
        else:
            # Oversized block: split at source sentence boundaries
            label_m = None
            if block.block_type == "list_item":
                label_m = re.match(r'^(\s*[-*+]\s+(?:\*\*.+?\*\*|__.+?__|[^\n:]+):?)\s*', block.text)

            if label_m:
                label_text = label_m.group(1)
                label_part = EvidencePart(
                    role="header",
                    start=block.start,
                    end=block.start + label_m.end(1),
                    text=label_text,
                )
                body_start = block.start + label_m.end()
                body_text = block.text[label_m.end():]
                sents = extract_sentence_spans(body_text, body_start)
                prefix_parts = lead_conds + [label_part]
            else:
                prefix_parts = lead_conds
                sents = extract_sentence_spans(block.text, block.start)

            if not sents:
                # Unbreakable unit: emit whole chunk so preview can detect it
                chunk_id = f"{doc.source}#{chunk_ordinal}"
                chunk_ordinal += 1
                chunks.append(
                    FullCorpusChunk(
                        chunk_id=chunk_id,
                        source=doc.source,
                        title=doc.title,
                        heading_path=list(block.heading_path),
                        evidence_parts=whole_parts,
                        search_text=whole_search_text,
                    )
                )
            else:
                # Group sentences greedily into chunks that fit all tokenizers
                s_idx = 0
                while s_idx < len(sents):
                    curr_group = [sents[s_idx]]
                    next_s = s_idx + 1
                    while next_s < len(sents):
                        cand_sents = curr_group + [sents[next_s]]
                        cand_text = doc.lf_text[cand_sents[0][0] : cand_sents[-1][1]]
                        cand_part = EvidencePart(
                            role="body",
                            start=cand_sents[0][0],
                            end=cand_sents[-1][1],
                            text=cand_text,
                        )
                        cand_parts = prefix_parts + [cand_part] + trailing_conds
                        cand_st = build_representation_a_search_text(
                            doc.title, block.heading_path, cand_parts
                        )
                        if is_fits_tokenizer_fn is not None and not is_fits_tokenizer_fn(cand_st):
                            break
                        curr_group.append(sents[next_s])
                        next_s += 1

                    group_text = doc.lf_text[curr_group[0][0] : curr_group[-1][1]]
                    group_part = EvidencePart(
                        role="body",
                        start=curr_group[0][0],
                        end=curr_group[-1][1],
                        text=group_text,
                    )
                    parts = prefix_parts + [group_part] + trailing_conds
                    st = build_representation_a_search_text(doc.title, block.heading_path, parts)
                    chunk_id = f"{doc.source}#{chunk_ordinal}"
                    chunk_ordinal += 1
                    chunks.append(
                        FullCorpusChunk(
                            chunk_id=chunk_id,
                            source=doc.source,
                            title=doc.title,
                            heading_path=list(block.heading_path),
                            evidence_parts=parts,
                            search_text=st,
                        )
                    )
                    s_idx = next_s

        idx += 1

    # Verify each chunk
    for ch in chunks:
        if not ch.search_text.strip():
            errors.append(f"Empty search_text in chunk {ch.chunk_id}")
        for part in ch.evidence_parts:
            if doc.lf_text[part.start:part.end] != part.text:
                errors.append(
                    f"Evidence part slice mismatch in chunk {ch.chunk_id} [{part.start}:{part.end}]: "
                    f"expected {part.text!r}, got {doc.lf_text[part.start:part.end]!r}"
                )

    return chunks, errors


def chunk_full_corpus(
    settings: dict[str, Any] | None = None,
    is_fits_tokenizer_fn: Callable[[str], bool] | None = None,
    condition_manager: ConditionManager | None = None,
) -> tuple[list[FullCorpusChunk], list[str]]:
    """Discover, parse and chunk the complete full corpus (all 205 files).

    Validates condition rules across the entire corpus fail-closed.
    Returns:
        (chunks, all_blocking_errors)
    """
    root, files = discover_full_corpus_files(settings)
    if condition_manager is None:
        condition_manager = ConditionManager(settings=settings)
    if is_fits_tokenizer_fn is None:
        is_fits_tokenizer_fn = get_default_tokenizer_checker(settings)

    all_chunks: list[FullCorpusChunk] = []
    all_errors: list[str] = []
    docs_by_source: dict[str, ParsedDocument] = {}

    # 1. Parse all files first
    for rel in files:
        full_path = root / rel
        lf_text = read_source_lf(full_path)
        try:
            doc = parse_markdown_blocks(rel, lf_text)
            docs_by_source[rel] = doc
        except Exception as e:
            all_errors.append(f"Parsing failed for {rel}: {e}")

    # 2. Validate condition rules across all discovered files
    corpus_rule_errors = condition_manager.validate_corpus_rules(files, docs_by_source)
    all_errors.extend(corpus_rule_errors)

    # 3. Chunk documents
    seen_chunk_ids: set[str] = set()
    seen_point_ids: set[str] = set()

    for rel in files:
        doc = docs_by_source.get(rel)
        if doc is None:
            continue

        doc_chunks, doc_errors = chunk_document(
            doc,
            condition_manager=condition_manager,
            is_fits_tokenizer_fn=is_fits_tokenizer_fn,
        )
        all_errors.extend(doc_errors)

        for chunk in doc_chunks:
            if chunk.chunk_id in seen_chunk_ids:
                all_errors.append(f"Duplicate chunk_id: {chunk.chunk_id}")
            seen_chunk_ids.add(chunk.chunk_id)

            if chunk.point_id in seen_point_ids:
                all_errors.append(f"Duplicate point_id (UUID5 collision): {chunk.point_id}")
            seen_point_ids.add(chunk.point_id)

            all_chunks.append(chunk)

    return all_chunks, all_errors
