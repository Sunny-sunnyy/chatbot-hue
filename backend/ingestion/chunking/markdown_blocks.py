"""Markdown block parsing with exact Unicode code-point source spans.

Uses markdown-it-py with tables enabled to parse curated Markdown into structured
blocks (paragraphs, tables, list items, blockquotes) with heading paths and
zero-based code-point offsets [start, end) on LF source text.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

import markdown_it

IMAGE_ONLY_RE = re.compile(r"^\s*!\[.*?\]\(.*?\)\s*$")
EXCLUDED_SECTIONS = {"Nguồn dữ liệu"}


def build_line_offsets(text: str) -> list[int]:
    """Calculate the zero-based character start offset for each line in LF text."""
    offsets = []
    curr = 0
    for line in text.split("\n"):
        offsets.append(curr)
        curr += len(line) + 1  # +1 for newline character '\n'
    return offsets


def get_block_span(
    start_line: int,
    end_line: int,
    lines: list[str],
    offsets: list[int],
    trim_trailing_blank: bool = True,
) -> tuple[int, int]:
    """Convert line indices [start_line, end_line] to character offset range [start, end)."""
    if start_line >= len(lines):
        return 0, 0
    start_char = offsets[start_line]
    last_line_idx = end_line - 1
    if trim_trailing_blank:
        while last_line_idx > start_line and lines[last_line_idx].strip() == "":
            last_line_idx -= 1
    end_char = offsets[last_line_idx] + len(lines[last_line_idx])
    return start_char, end_char


@dataclass(frozen=True)
class TableRowInfo:
    """Exact span and text of a single table row."""

    start: int
    end: int
    text: str


@dataclass
class TableInfo:
    """Detailed structural information for a markdown table."""

    header_start: int
    header_end: int
    header_text: str
    rows: list[TableRowInfo]


@dataclass(frozen=True)
class ListItemSubItem:
    """Sub-item inside a nested list item."""

    start: int
    end: int
    text: str


@dataclass
class ListItemInfo:
    """Detailed structural information for a list item."""

    start: int
    end: int
    text: str
    parent_start: int = 0
    parent_end: int = 0
    parent_text: str = ""
    sub_items: list[ListItemSubItem] = field(default_factory=list)


@dataclass
class MarkdownBlock:
    """A semantic block extracted from markdown source."""

    block_type: str  # "paragraph" | "table" | "list_item" | "blockquote"
    heading_path: list[str]
    start: int
    end: int
    text: str
    table_info: TableInfo | None = None
    list_item_info: ListItemInfo | None = None


@dataclass
class ParsedDocument:
    """Document parsed into semantic blocks with verified source spans."""

    source: str
    title: str
    blocks: list[MarkdownBlock]
    lf_text: str
    lines: list[str]
    offsets: list[int]


def parse_markdown_blocks(source: str, lf_text: str) -> ParsedDocument:
    """Parse normalized LF markdown text into blocks with verified offsets."""
    lines = lf_text.split("\n")
    offsets = build_line_offsets(lf_text)
    md = markdown_it.MarkdownIt().enable("table")
    tokens = md.parse(lf_text)

    title = ""
    h_stack: list[tuple[int, str]] = []
    blocks: list[MarkdownBlock] = []

    list_depth = 0
    in_table = False
    in_blockquote = False

    # First pass: find title (H1)
    for i, t in enumerate(tokens):
        if t.type == "heading_open" and t.tag == "h1":
            title = tokens[i + 1].content.strip()
            break

    if not title:
        # Fallback check for first line starting with #
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

    if not title:
        raise ValueError(f"File {source} missing H1 title")

    idx = 0
    while idx < len(tokens):
        t = tokens[idx]

        # Heading handling
        if t.type == "heading_open":
            lvl = int(t.tag[1])
            htitle = tokens[idx + 1].content.strip()
            if lvl > 1:
                while h_stack and h_stack[-1][0] >= lvl:
                    h_stack.pop()
                h_stack.append((lvl, htitle))
            idx += 1
            continue

        cur_path = [h[1] for h in h_stack]

        # Skip excluded source tracking sections
        if any(part in EXCLUDED_SECTIONS for part in cur_path):
            idx += 1
            continue

        # Lists tracking
        if t.type in ("bullet_list_open", "ordered_list_open"):
            list_depth += 1
            idx += 1
            continue
        if t.type in ("bullet_list_close", "ordered_list_close"):
            list_depth -= 1
            idx += 1
            continue

        # Table handling
        if t.type == "table_open":
            in_table = True
            table_map = t.map
            idx += 1
            # Find thead and rows inside this table
            header_map = None
            row_maps: list[tuple[int, int]] = []
            in_tbody = False
            while idx < len(tokens) and tokens[idx].type != "table_close":
                cur_t = tokens[idx]
                if cur_t.type == "tbody_open":
                    in_tbody = True
                    if table_map and cur_t.map:
                        header_map = (table_map[0], cur_t.map[0])
                elif cur_t.type == "tbody_close":
                    in_tbody = False
                elif cur_t.type == "tr_open" and in_tbody and cur_t.map:
                    row_maps.append(cur_t.map)
                idx += 1

            in_table = False
            if table_map:
                s, e = get_block_span(table_map[0], table_map[1], lines, offsets)
                tbl_text = lf_text[s:e]

                # Extract header info
                tbl_info: TableInfo | None = None
                if header_map:
                    hs, he = get_block_span(header_map[0], header_map[1], lines, offsets)
                    hdr_text = lf_text[hs:he]
                    parsed_rows: list[TableRowInfo] = []
                    for r_map in row_maps:
                        rs, re_ = get_block_span(r_map[0], r_map[1], lines, offsets)
                        parsed_rows.append(TableRowInfo(start=rs, end=re_, text=lf_text[rs:re_]))
                    tbl_info = TableInfo(
                        header_start=hs,
                        header_end=he,
                        header_text=hdr_text,
                        rows=parsed_rows,
                    )

                blocks.append(
                    MarkdownBlock(
                        block_type="table",
                        heading_path=list(cur_path),
                        start=s,
                        end=e,
                        text=tbl_text,
                        table_info=tbl_info,
                    )
                )
            idx += 1
            continue

        # Blockquote handling
        if t.type == "blockquote_open":
            in_blockquote = True
            bq_map = t.map
            while idx < len(tokens) and tokens[idx].type != "blockquote_close":
                idx += 1
            in_blockquote = False
            if bq_map:
                s, e = get_block_span(bq_map[0], bq_map[1], lines, offsets)
                blocks.append(
                    MarkdownBlock(
                        block_type="blockquote",
                        heading_path=list(cur_path),
                        start=s,
                        end=e,
                        text=lf_text[s:e],
                    )
                )
            idx += 1
            continue

        # List item handling at top-level of list (list_depth == 1)
        if list_depth == 1 and t.type == "list_item_open" and t.map:
            item_map = t.map
            # Collect any sub-items within this list item
            sub_item_maps: list[tuple[int, int]] = []
            nest_open = 1
            item_idx = idx + 1
            while item_idx < len(tokens) and nest_open > 0:
                sub_t = tokens[item_idx]
                if sub_t.type in ("bullet_list_open", "ordered_list_open"):
                    pass
                elif sub_t.type == "list_item_open":
                    nest_open += 1
                    if nest_open > 1 and sub_t.map:
                        sub_item_maps.append(sub_t.map)
                elif sub_t.type == "list_item_close":
                    nest_open -= 1
                item_idx += 1

            s, e = get_block_span(item_map[0], item_map[1], lines, offsets)
            item_text = lf_text[s:e]

            # Construct ListItemInfo
            parsed_sub_items: list[ListItemSubItem] = []
            for sm in sub_item_maps:
                ss, se = get_block_span(sm[0], sm[1], lines, offsets)
                parsed_sub_items.append(
                    ListItemSubItem(start=ss, end=se, text=lf_text[ss:se])
                )

            parent_start = s
            parent_end = s
            parent_text = ""
            if sub_item_maps:
                ps, pe = get_block_span(item_map[0], sub_item_maps[0][0], lines, offsets)
                parent_start = ps
                parent_end = pe
                parent_text = lf_text[ps:pe]

            item_info = ListItemInfo(
                start=s,
                end=e,
                text=item_text,
                parent_start=parent_start,
                parent_end=parent_end,
                parent_text=parent_text,
                sub_items=parsed_sub_items,
            )

            blocks.append(
                MarkdownBlock(
                    block_type="list_item",
                    heading_path=list(cur_path),
                    start=s,
                    end=e,
                    text=item_text,
                    list_item_info=item_info,
                )
            )
            idx += 1
            continue

        # Standalone paragraph handling
        if list_depth == 0 and not in_table and not in_blockquote:
            if t.type == "paragraph_open" and t.map:
                s, e = get_block_span(t.map[0], t.map[1], lines, offsets)
                p_text = lf_text[s:e]
                if not IMAGE_ONLY_RE.match(p_text.strip()):
                    blocks.append(
                        MarkdownBlock(
                            block_type="paragraph",
                            heading_path=list(cur_path),
                            start=s,
                            end=e,
                            text=p_text,
                        )
                    )
                idx += 1
                continue

        idx += 1

    # Verify every block matches source slice exactly
    for b in blocks:
        if lf_text[b.start:b.end] != b.text:
            raise ValueError(
                f"Block span mismatch in {source} [{b.start}:{b.end}]: "
                f"got {lf_text[b.start:b.end]!r} != {b.text!r}"
            )
        if b.table_info:
            if lf_text[b.table_info.header_start:b.table_info.header_end] != b.table_info.header_text:
                raise ValueError(f"Table header span mismatch in {source}")
            for row in b.table_info.rows:
                if lf_text[row.start:row.end] != row.text:
                    raise ValueError(f"Table row span mismatch in {source}")
        if b.list_item_info and b.list_item_info.sub_items:
            if lf_text[b.list_item_info.parent_start:b.list_item_info.parent_end] != b.list_item_info.parent_text:
                raise ValueError(f"List item parent span mismatch in {source}")
            for sub in b.list_item_info.sub_items:
                if lf_text[sub.start:sub.end] != sub.text:
                    raise ValueError(f"List item sub-item span mismatch in {source}")

    return ParsedDocument(
        source=source,
        title=title,
        blocks=blocks,
        lf_text=lf_text,
        lines=lines,
        offsets=offsets,
    )
