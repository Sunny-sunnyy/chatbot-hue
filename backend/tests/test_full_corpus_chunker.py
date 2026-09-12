"""Comprehensive technical tests for Full-Corpus RAG Wave 1.

Tests cover:
- Deterministic corpus discovery (5 domains, 7 P7 partitions, 205 files, inventory/part exclusions, sorted order).
- CRLF/CR normalization, zero-based Unicode code-point offsets, and repeated text locator.
- Markdown block extraction (H1 title, intro before H2, blockquotes, nested lists, tables, image-only exclusion, section exclusions).
- Condition attachment outside corpus (schema validation fail-closed, exact selector matching, missing/duplicate selector detection).
- Tokenizer checker settings responsiveness (different settings across calls in same process without blind singleton reuse).
- Splitting logic: sentence boundary split for oversized paragraphs, table row split retaining headers and conditions, nested-list split retaining parent labels.
- Detailed assertions on the named acceptance sample files (Mệ Kéo address/hours/price/dish, Gia Lạc historical vs contemporary space and non-commercial nature, Đại Nội Ngọ Môn 5 entrances, Lịch trình 3N2Đ day structure, Ca Huế performing art instruments, Ca Huế tickets conditions, Chi phí du lịch Huế daily budgets).
- Synthetic isolated oversized minimal group fail-closed blocking.
- Generic condition/parser error preview blocking isolated from oversized groups.
- Canonical full-corpus preview PASS (zero errors, zero oversized, domain and P7 breakdowns).
- Deterministic reproducibility across full corpus: deep-equal chunks/IDs/UUID5, 100% exact evidence slicing, and byte-identical preview outputs.
"""
from __future__ import annotations

import json
from pathlib import Path
import uuid
import pytest
from pyvi import ViTokenizer
from transformers import AutoTokenizer

from core.schema import EvidencePart, FullCorpusChunk, point_id_for_chunk_id
from core.settings_loader import BACKEND_DIR, get_full_corpus_settings, load_settings
from ingestion.chunking.full_corpus_chunker import (
    ConditionManager,
    build_representation_a_search_text,
    chunk_document,
    chunk_full_corpus,
    extract_sentence_spans,
    get_default_tokenizer_checker,
    match_block_selector,
)
from ingestion.chunking.markdown_blocks import (
    TableRowInfo,
    TableInfo,
    build_line_offsets,
    get_block_span,
    parse_markdown_blocks,
)
from ingestion.preview import (
    count_tokens_for_chunk,
    generate_preview,
    load_tokenizers,
    partition_for_source,
)
from ingestion.source_state import (
    compute_corpus_state,
    compute_file_hash,
    compute_source_hash,
    discover_full_corpus_files,
    normalize_lf,
    read_source_lf,
    verify_build_record_freshness,
)


# --- 1. Discovery and Inventory Exclusions ---

def test_full_corpus_discovery_and_inventory_exclusions():
    """Verify discovery finds exactly 205 files across 5 domains and 7 P7 partitions in deterministic order."""
    root, files = discover_full_corpus_files()
    assert root.is_dir()
    assert len(files) == 205

    # Check 5 domain counts
    domains = [f.split("/")[0] for f in files]
    assert domains.count("festivals") == 27
    assert domains.count("foods") == 91
    assert domains.count("heritages") == 29
    assert domains.count("performing_arts") == 13
    assert domains.count("travel") == 45

    # Check 7 P7 partition counts
    p7_partitions = [partition_for_source(f) for f in files]
    assert p7_partitions.count("foods") == 91
    assert p7_partitions.count("heritages") == 29
    assert p7_partitions.count("festivals") == 27
    assert p7_partitions.count("performing_arts") == 13
    assert p7_partitions.count("travel_places") == 36
    assert p7_partitions.count("travel_services") == 4
    assert p7_partitions.count("travel_tickets") == 5
    assert sum(p7_partitions.count(p) for p in set(p7_partitions)) == 205

    # Check deterministic sorted order
    assert files == sorted(files)

    # Check exact inventory exclusions
    assert "travel/services/services-research-and-entities-inventory.md" not in files
    assert "travel/tickets/tickets-research-and-entities-inventory.md" not in files

    # Check exclude_parts
    for f in files:
        parts = Path(f).parts
        assert "evaluation" not in parts
        assert "_source-dumps" not in parts
        assert "meta" not in parts


# --- 2. Normalization and Unicode Code-Point Offsets ---

def test_lf_normalization_and_hash():
    """Verify CRLF and CR are normalized to LF before hashing and locator."""
    raw_crlf = "Dòng 1\r\nDòng 2\r\nDòng 3\r\n"
    raw_cr = "Dòng 1\rDòng 2\rDòng 3\r"
    expected_lf = "Dòng 1\nDòng 2\nDòng 3\n"

    assert normalize_lf(raw_crlf) == expected_lf
    assert normalize_lf(raw_cr) == expected_lf
    assert compute_source_hash(expected_lf) == compute_source_hash(normalize_lf(raw_crlf))


def test_unicode_code_point_offsets_and_repeated_text_locator():
    """Verify offsets are zero-based Unicode code points and repeated substrings locate correctly."""
    repeated_phrase = "Cố đô Huế"
    text = (
        f"# Tiêu đề về {repeated_phrase}\n\n"
        f"Đoạn một ca ngợi vẻ đẹp của {repeated_phrase} bên bờ sông Hương.\n\n"
        f"Đoạn hai khẳng định {repeated_phrase} là di sản vô giá của Việt Nam."
    )
    doc = parse_markdown_blocks("repeated.md", text)
    assert len(doc.blocks) == 2

    b0 = doc.blocks[0]
    b1 = doc.blocks[1]
    assert b0.text == f"Đoạn một ca ngợi vẻ đẹp của {repeated_phrase} bên bờ sông Hương."
    assert b1.text == f"Đoạn hai khẳng định {repeated_phrase} là di sản vô giá của Việt Nam."

    # Both blocks contain the exact repeated phrase, but at strictly different non-overlapping offsets
    assert repeated_phrase in b0.text
    assert repeated_phrase in b1.text
    assert doc.lf_text[b0.start:b0.end] == b0.text
    assert doc.lf_text[b1.start:b1.end] == b1.text
    assert b0.end <= b1.start


# --- 3. Markdown Block Parsing, Structure, Blockquotes and Exclusions ---

def test_markdown_blocks_h1_intro_and_exclusions():
    """Verify H1 is title, intro before H2 has empty heading_path, and exclusions are honored."""
    test_md = (
        "# Tiêu Đề Bài Viết\n\n"
        "Đoạn dẫn nhập trước mọi H2.\n\n"
        "## Mục Một\n\n"
        "Nội dung mục một.\n\n"
        "![Ảnh minh họa](https://example.com/pic.jpg)\n\n"
        "---\n\n"
        "## Nguồn dữ liệu\n\n"
        "- https://example.com/source\n"
    )
    doc = parse_markdown_blocks("test.md", test_md)
    assert doc.title == "Tiêu Đề Bài Viết"
    assert len(doc.blocks) == 2

    # Block 0: intro before H2
    b0 = doc.blocks[0]
    assert b0.block_type == "paragraph"
    assert b0.heading_path == []
    assert b0.text == "Đoạn dẫn nhập trước mọi H2."
    assert doc.lf_text[b0.start:b0.end] == b0.text

    # Block 1: under Mục Một (image and separator excluded, Nguồn dữ liệu excluded)
    b1 = doc.blocks[1]
    assert b1.block_type == "paragraph"
    assert b1.heading_path == ["Mục Một"]
    assert b1.text == "Nội dung mục một."
    assert doc.lf_text[b1.start:b1.end] == b1.text


def test_markdown_blocks_blockquote_and_exclusions():
    """Verify blockquotes under headings, exact slicing, and image/separator exclusions."""
    md = (
        "# Bài Viết Trích Dẫn\n\n"
        "## Mục Nhận Định\n\n"
        "> Đây là lời trích dẫn nguyên văn rất quan trọng của học giả về văn hóa Huế.\n\n"
        "![Ảnh chân dung](https://example.com/scholar.jpg)\n\n"
        "---\n\n"
        "> Lời trích dẫn thứ hai mang tính đúc kết lịch sử.\n"
    )
    doc = parse_markdown_blocks("quote.md", md)
    assert len(doc.blocks) == 2
    b0 = doc.blocks[0]
    b1 = doc.blocks[1]

    assert b0.block_type == "blockquote"
    assert b0.heading_path == ["Mục Nhận Định"]
    assert b0.text == "> Đây là lời trích dẫn nguyên văn rất quan trọng của học giả về văn hóa Huế."
    assert doc.lf_text[b0.start:b0.end] == b0.text

    assert b1.block_type == "blockquote"
    assert b1.heading_path == ["Mục Nhận Định"]
    assert b1.text == "> Lời trích dẫn thứ hai mang tính đúc kết lịch sử."
    assert doc.lf_text[b1.start:b1.end] == b1.text
    assert b0.end <= b1.start


def test_markdown_blocks_table_and_nested_list_extraction():
    """Verify table header and rows, and nested list parent label and sub-items are extracted accurately."""
    content = (
        "# Cấu Trúc Kiểm Thử\n\n"
        "## Danh Sách Lồng\n\n"
        "- **Nhãn cha:** Phần dẫn của danh sách cha.\n"
        "  - Mục con thứ nhất\n"
        "  - Mục con thứ hai\n\n"
        "## Bảng Dữ Liệu\n\n"
        "| Cột A | Cột B |\n"
        "|---|---:|\n"
        "| Giá trị 1 | 100 |\n"
        "| Giá trị 2 | 200 |\n"
    )
    doc = parse_markdown_blocks("nested_and_table.md", content)
    assert len(doc.blocks) == 2

    # Block 0: nested list item
    b_list = doc.blocks[0]
    assert b_list.block_type == "list_item"
    assert b_list.list_item_info is not None
    info = b_list.list_item_info
    assert len(info.sub_items) == 2
    assert content[info.parent_start:info.parent_end] == info.parent_text
    assert info.parent_text == "- **Nhãn cha:** Phần dẫn của danh sách cha."
    assert content[info.sub_items[0].start:info.sub_items[0].end] == "  - Mục con thứ nhất"
    assert content[info.sub_items[1].start:info.sub_items[1].end] == "  - Mục con thứ hai"

    # Block 1: table
    b_tbl = doc.blocks[1]
    assert b_tbl.block_type == "table"
    assert b_tbl.table_info is not None
    tinfo = b_tbl.table_info
    assert content[tinfo.header_start:tinfo.header_end] == tinfo.header_text
    assert tinfo.header_text == "| Cột A | Cột B |\n|---|---:|"
    assert len(tinfo.rows) == 2
    assert content[tinfo.rows[0].start:tinfo.rows[0].end] == "| Giá trị 1 | 100 |"
    assert content[tinfo.rows[1].start:tinfo.rows[1].end] == "| Giá trị 2 | 200 |"


# --- 4. Condition Attachment (Schema Validation & Exact Matching) ---

def test_condition_manager_schema_validation(tmp_path):
    """Verify ConditionManager validates schema fail-closed on missing or malformed selector fields."""
    def write_and_load(rules_data):
        p = tmp_path / f"cond_{len(list(tmp_path.iterdir()))}.json"
        p.write_text(json.dumps(rules_data), encoding="utf-8")
        return ConditionManager(conditions_path=p)

    # 1. Missing source
    with pytest.raises(ValueError, match="missing valid 'source'"):
        write_and_load([{"condition": {}, "targets": []}])

    # 2. Missing heading_path
    with pytest.raises(ValueError, match="missing required field 'heading_path'"):
        write_and_load([{
            "source": "s.md",
            "condition": {"block_type": "paragraph", "exact_text": "text"},
            "targets": [{"heading_path": [], "block_type": "paragraph", "exact_text": "t"}],
        }])

    # 3. heading_path not list of strings
    with pytest.raises(ValueError, match="'heading_path' must be a list of strings"):
        write_and_load([{
            "source": "s.md",
            "condition": {"heading_path": "invalid_string", "block_type": "paragraph", "exact_text": "text"},
            "targets": [{"heading_path": [], "block_type": "paragraph", "exact_text": "t"}],
        }])

    # 4. Missing block_type
    with pytest.raises(ValueError, match="missing required field 'block_type'"):
        write_and_load([{
            "source": "s.md",
            "condition": {"heading_path": [], "exact_text": "text"},
            "targets": [{"heading_path": [], "block_type": "paragraph", "exact_text": "t"}],
        }])

    # 5. Missing exact_text
    with pytest.raises(ValueError, match="missing required field 'exact_text'"):
        write_and_load([{
            "source": "s.md",
            "condition": {"heading_path": [], "block_type": "paragraph"},
            "targets": [{"heading_path": [], "block_type": "paragraph", "exact_text": "t"}],
        }])

    # 6. Targets empty list
    with pytest.raises(ValueError, match="missing non-empty 'targets' list"):
        write_and_load([{
            "source": "s.md",
            "condition": {"heading_path": [], "block_type": "paragraph", "exact_text": "text"},
            "targets": [],
        }])

    # 7. Target missing required field
    with pytest.raises(ValueError, match="missing required field 'exact_text'"):
        write_and_load([{
            "source": "s.md",
            "condition": {"heading_path": [], "block_type": "paragraph", "exact_text": "text"},
            "targets": [{"heading_path": [], "block_type": "paragraph"}],
        }])


def test_condition_manager_corpus_validation_and_attachment(tmp_path):
    """Verify ConditionManager validates rules against corpus and handles missing/duplicate/mismatch."""
    cond_mgr = ConditionManager()
    root, files = discover_full_corpus_files()
    docs_by_source = {}
    for rel in files:
        lf = read_source_lf(root / rel)
        docs_by_source[rel] = parse_markdown_blocks(rel, lf)

    # 1. Whole-corpus condition validation of canonical rules must produce zero errors
    corpus_errors = cond_mgr.validate_corpus_rules(files, docs_by_source)
    assert len(corpus_errors) == 0

    # 2. Synthetic document for error paths
    test_doc = parse_markdown_blocks(
        "test.md",
        "# Test\n\n## Mục\n\nCâu lặp lại.\n\nCâu lặp lại.\n\nCâu duy nhất.\n"
    )
    docs = {"test.md": test_doc}

    # Missing source file
    cfg_src = tmp_path / "cond_bad_src.json"
    cfg_src.write_text(json.dumps([{
        "source": "nonexistent.md",
        "condition": {"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu duy nhất."},
        "targets": [{"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu duy nhất."}],
    }]), encoding="utf-8")
    assert any("not in discovered files" in e for e in ConditionManager(conditions_path=cfg_src).validate_corpus_rules(["test.md"], docs))

    # Missing condition selector
    cfg_mc = tmp_path / "cond_missing_c.json"
    cfg_mc.write_text(json.dumps([{
        "source": "test.md",
        "condition": {"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Không tồn tại"},
        "targets": [{"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu duy nhất."}],
    }]), encoding="utf-8")
    assert any("Condition selector missing" in e for e in ConditionManager(conditions_path=cfg_mc).validate_corpus_rules(["test.md"], docs))

    # Duplicate condition selector
    cfg_dc = tmp_path / "cond_dup_c.json"
    cfg_dc.write_text(json.dumps([{
        "source": "test.md",
        "condition": {"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu lặp lại."},
        "targets": [{"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu duy nhất."}],
    }]), encoding="utf-8")
    assert any("Duplicate condition selector" in e for e in ConditionManager(conditions_path=cfg_dc).validate_corpus_rules(["test.md"], docs))

    # Missing target selector
    cfg_mt = tmp_path / "cond_missing_t.json"
    cfg_mt.write_text(json.dumps([{
        "source": "test.md",
        "condition": {"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu duy nhất."},
        "targets": [{"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Không tồn tại"}],
    }]), encoding="utf-8")
    assert any("Target selector missing" in e for e in ConditionManager(conditions_path=cfg_mt).validate_corpus_rules(["test.md"], docs))

    # Duplicate target selector
    cfg_dt = tmp_path / "cond_dup_t.json"
    cfg_dt.write_text(json.dumps([{
        "source": "test.md",
        "condition": {"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu duy nhất."},
        "targets": [{"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu lặp lại."}],
    }]), encoding="utf-8")
    assert any("Duplicate target selector" in e for e in ConditionManager(conditions_path=cfg_dt).validate_corpus_rules(["test.md"], docs))

    # Exact matcher rejection: wrong block_type (no alias or wildcard)
    cfg_alias = tmp_path / "cond_alias.json"
    cfg_alias.write_text(json.dumps([{
        "source": "test.md",
        "condition": {"heading_path": ["Mục"], "block_type": "bullet_list_item", "exact_text": "Câu duy nhất."},
        "targets": [{"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Câu duy nhất."}],
    }]), encoding="utf-8")
    assert any("Condition selector missing" in e for e in ConditionManager(conditions_path=cfg_alias).validate_corpus_rules(["test.md"], docs))


# --- 5. Tokenizer Checker Settings Responsiveness ---

def test_tokenizer_checker_settings_switch():
    """Verify get_default_tokenizer_checker respects settings across calls without config-blind singleton reuse."""
    default_checker = get_default_tokenizer_checker()
    sample_text = "Thành phố Huế là trung tâm văn hóa, giáo dục và du lịch lớn của miền Trung Việt Nam."
    # With default settings (~15-20 tokens, limits are 256 and 512), this should return True
    assert default_checker(sample_text) is True

    # Custom settings with very low max_tokens (e.g. 5 tokens) for one model
    custom_settings = load_settings()
    custom_settings["full_corpus"]["embedding_models"] = [
        {
            "id": "intfloat/multilingual-e5-small",
            "max_tokens": 5,
            "prefix": "passage: ",
            "word_segment": False,
        }
    ]
    custom_checker = get_default_tokenizer_checker(custom_settings)
    # With max_tokens=5, sample_text exceeds limit -> must return False
    assert custom_checker(sample_text) is False

    # Calling again with default settings returns True (cache keyed properly by settings)
    assert get_default_tokenizer_checker()(sample_text) is True


# --- 6. Splitting Logic Preserving Exact Evidence ---

def test_oversized_paragraph_sentence_boundary_split():
    """Verify long paragraph splits cleanly at sentence boundaries without cutting mid-sentence."""
    text = (
        "# Văn Bản Thử Nghiệm\n\n"
        "## Mục Đoạn Văn\n\n"
        "Câu thứ nhất miêu tả lịch sử lâu đời của ngôi cổ tự nghìn năm tuổi. "
        "Câu thứ hai trình bày chi tiết về kiến trúc các gian điện và tượng Phật thờ phụng bên trong. "
        "Câu thứ ba kết luận về giá trị tâm linh sâu sắc đối với Phật tử bốn phương về chiêm bái."
    )
    doc = parse_markdown_blocks("para.md", text)
    assert len(doc.blocks) == 1

    # Budget function forcing splitting across sentences
    chunks, errors = chunk_document(doc, is_fits_tokenizer_fn=lambda t: len(t) < 180)
    assert len(errors) == 0
    assert len(chunks) >= 2

    # Each chunk must have sentence spans as evidence parts
    for ch in chunks:
        assert len(ch.evidence_parts) >= 1
        for p in ch.evidence_parts:
            assert p.role == "body"
            assert doc.lf_text[p.start:p.end] == p.text
            assert p.text.endswith(".")


def test_oversized_table_row_split_preserves_header_and_condition(tmp_path):
    """Verify table row split retains table header and attached condition on every row chunk."""
    text = (
        "# Bảng Giá\n\n"
        "Đoạn dẫn điều kiện giá vé.\n\n"
        "## Bảng Dịch Vụ\n\n"
        "| Loại vé | Giá vé |\n"
        "|---|---:|\n"
        "| Vé người lớn | 100.000đ |\n"
        "| Vé trẻ em | 50.000đ |\n"
        "| Vé sinh viên | 70.000đ |\n"
    )
    doc = parse_markdown_blocks("table.md", text)
    assert len(doc.blocks) == 2

    cond_file = tmp_path / "cond.json"
    cond_file.write_text(json.dumps([{
        "source": "table.md",
        "condition": {"heading_path": [], "block_type": "paragraph", "exact_text": "Đoạn dẫn điều kiện giá vé."},
        "targets": [{"heading_path": ["Bảng Dịch Vụ"], "block_type": "table", "exact_text": "| Loại vé | Giá vé |\n|---|---:|\n| Vé người lớn | 100.000đ |\n| Vé trẻ em | 50.000đ |\n| Vé sinh viên | 70.000đ |"}],
    }]), encoding="utf-8")
    mgr = ConditionManager(conditions_path=cond_file)

    # Force splitting so each row is its own chunk
    chunks, errors = chunk_document(doc, condition_manager=mgr, is_fits_tokenizer_fn=lambda t: len(t) < 160)
    assert len(errors) == 0
    assert len(chunks) == 3

    for ch in chunks:
        roles = [p.role for p in ch.evidence_parts]
        assert "condition" in roles
        assert "header" in roles
        assert "body" in roles
        cond_part = [p for p in ch.evidence_parts if p.role == "condition"][0]
        header_part = [p for p in ch.evidence_parts if p.role == "header"][0]
        body_part = [p for p in ch.evidence_parts if p.role == "body"][0]

        assert cond_part.text == "Đoạn dẫn điều kiện giá vé."
        assert header_part.text == "| Loại vé | Giá vé |\n|---|---:|"
        assert body_part.text.startswith("| Vé ")
        for p in ch.evidence_parts:
            assert doc.lf_text[p.start:p.end] == p.text


def test_oversized_nested_list_split_preserves_parent_and_sub_items():
    """Verify nested list splitting retains parent label part alongside assigned sub-items."""
    text = (
        "# Danh Sách\n\n"
        "## Mục\n\n"
        "- **Quy định quan trọng:** Các điều khoản bắt buộc gồm có:\n"
        "  - Điều một: Phải tuân thủ thời gian tham quan quy định.\n"
        "  - Điều hai: Giữ gìn vệ sinh và không xả rác bừa bãi.\n"
        "  - Điều ba: Không tự ý chạm vào hiện vật trưng bày.\n"
    )
    doc = parse_markdown_blocks("list.md", text)
    assert len(doc.blocks) == 1

    # Budget function forcing each sub-item into separate chunk
    chunks, errors = chunk_document(doc, is_fits_tokenizer_fn=lambda t: len(t) < 150)
    assert len(errors) == 0
    assert len(chunks) >= 2

    for ch in chunks:
        roles = [p.role for p in ch.evidence_parts]
        assert "header" in roles
        assert "body" in roles
        header_part = [p for p in ch.evidence_parts if p.role == "header"][0]
        assert header_part.text == "- **Quy định quan trọng:** Các điều khoản bắt buộc gồm có:"
        for p in ch.evidence_parts:
            assert doc.lf_text[p.start:p.end] == p.text


def test_sentence_boundary_splitting_preserves_label_and_exact_spans():
    """Verify sentence boundary extraction and chunking of oversized items preserves label and exact source slices."""
    raw_md = (
        "# Di Tích Thử Nghiệm\n\n"
        "## Lịch Sử\n\n"
        "- **Giai đoạn phát triển:** Câu thứ nhất về nguồn gốc di tích. "
        "Câu thứ hai miêu tả sự hưng thịnh của đền thờ. "
        "Câu thứ ba kể lại biến cố chiến tranh tàn phá nặng nề. "
        "Câu thứ tư khẳng định công cuộc trùng tu lớn lao. "
        "Câu thứ năm mở đầu cho thời kỳ phục hưng đương đại."
    )
    doc = parse_markdown_blocks("test_split.md", raw_md)
    assert len(doc.blocks) == 1
    block = doc.blocks[0]
    assert block.block_type == "list_item"

    # Custom budget function forcing max length ~140 chars to trigger split
    def strict_fits(text: str) -> bool:
        return len(text) <= 150

    chunks, errors = chunk_document(doc, is_fits_tokenizer_fn=strict_fits)
    assert len(errors) == 0
    assert len(chunks) >= 2

    # Every chunk must have the leading bold label as header part, followed by sentence parts
    for ch in chunks:
        assert len(ch.evidence_parts) >= 2
        label_part = ch.evidence_parts[0]
        body_part = ch.evidence_parts[1]

        assert label_part.role == "header"
        assert label_part.text == "- **Giai đoạn phát triển:**"
        assert doc.lf_text[label_part.start:label_part.end] == label_part.text
        assert body_part.role == "body"
        assert doc.lf_text[body_part.start:body_part.end] == body_part.text


# --- 7. Six Named Acceptance Sample Assertions ---

def test_acceptance_sample_me_keo():
    """Verify Bún bò Mệ Kéo is chunked with exact address, opening hours, price, and dish description."""
    root, _ = discover_full_corpus_files()
    rel = "foods/restaurants/quan bun bo me keo.md"
    doc = parse_markdown_blocks(rel, read_source_lf(root / rel))
    chunks, errors = chunk_document(doc)
    assert len(errors) == 0
    assert len(chunks) > 0

    # 1. Address chunk under Thông tin
    addr_chunks = [ch for ch in chunks if ch.heading_path == ["Thông tin"] and "Số 20 đường Bạch Đằng" in ch.search_text]
    assert len(addr_chunks) == 1
    ch_addr = addr_chunks[0]
    assert any("Số 20 đường Bạch Đằng, phường Phú Cát" in p.text for p in ch_addr.evidence_parts)
    for p in ch_addr.evidence_parts:
        assert doc.lf_text[p.start:p.end] == p.text

    # 2. Price chunk under Thông tin
    price_chunks = [ch for ch in chunks if ch.heading_path == ["Thông tin"] and "Mức giá" in ch.search_text]
    assert len(price_chunks) == 1
    ch_price = price_chunks[0]
    assert any("25.000 VNĐ – 50.000 VNĐ/tô" in p.text for p in ch_price.evidence_parts)
    for p in ch_price.evidence_parts:
        assert doc.lf_text[p.start:p.end] == p.text

    # 3. Hours chunk under Thông tin
    hours_chunks = [ch for ch in chunks if ch.heading_path == ["Thông tin"] and "Giờ hoạt động" in ch.search_text]
    assert len(hours_chunks) == 1
    ch_hours = hours_chunks[0]
    assert any("6:00 sáng – 10:00 sáng" in p.text for p in ch_hours.evidence_parts)
    for p in ch_hours.evidence_parts:
        assert doc.lf_text[p.start:p.end] == p.text

    # 4. Exact chunk for dish characteristic without beef
    no_beef_chunks = [
        ch for ch in chunks
        if ch.heading_path == ["Món ăn / trải nghiệm"]
        and any("không có thịt bò" in p.text for p in ch.evidence_parts)
    ]
    assert len(no_beef_chunks) == 1
    ch_no_beef = no_beef_chunks[0]
    assert "Bún Mệ Kéo, được mô tả là tô bún bò Huế đặc biệt không có thịt bò" in ch_no_beef.search_text
    assert len(ch_no_beef.evidence_parts) == 1
    p_no_beef = ch_no_beef.evidence_parts[0]
    assert p_no_beef.text == "- Bún Mệ Kéo, được mô tả là tô bún bò Huế đặc biệt không có thịt bò."
    assert doc.lf_text[p_no_beef.start:p_no_beef.end] == p_no_beef.text

    # 5. Exact chunk for dish ingredients
    ingr_chunks = [
        ch for ch in chunks
        if ch.heading_path == ["Món ăn / trải nghiệm"]
        and any("thịt ba chỉ, chả cua, huyết heo" in p.text for p in ch.evidence_parts)
    ]
    assert len(ingr_chunks) == 1
    ch_ingr = ingr_chunks[0]
    assert "thịt ba chỉ, chả cua, huyết heo" in ch_ingr.search_text
    assert len(ch_ingr.evidence_parts) == 1
    p_ingr = ch_ingr.evidence_parts[0]
    assert p_ingr.text == "- Thành phần được nhắc trong mô tả gốc gồm thịt ba chỉ, chả cua, huyết heo, nước dùng thơm mùi ruốc sả và rau sống."
    assert doc.lf_text[p_ingr.start:p_ingr.end] == p_ingr.text

    # Assert no-beef and ingredients are strictly separate chunks
    assert ch_no_beef.chunk_id != ch_ingr.chunk_id


def test_acceptance_sample_gia_lac():
    """Verify Hội xuân Gia Lạc preserves distinct historical vs contemporary revival spaces and non-commercial nature."""
    root, _ = discover_full_corpus_files()
    rel = "festivals/festival/Hội xuân Gia Lạc.md"
    doc = parse_markdown_blocks(rel, read_source_lf(root / rel))
    chunks, errors = chunk_document(doc)
    assert len(errors) == 0
    assert len(chunks) > 0

    # 1. Exact historical space chunk under Không gian tổ chức
    hist_chunks = [
        ch for ch in chunks
        if ch.heading_path == ["Không gian tổ chức"]
        and any("Không gian lịch sử" in p.text and "ngã ba làng Nam Phổ" in p.text for p in ch.evidence_parts)
    ]
    assert len(hist_chunks) == 1
    ch_hist = hist_chunks[0]
    assert "ngã ba làng Nam Phổ" in ch_hist.search_text
    assert len(ch_hist.evidence_parts) == 1
    p_hist = ch_hist.evidence_parts[0]
    assert doc.lf_text[p_hist.start:p_hist.end] == p_hist.text

    # 2. Exact contemporary revival space chunk under Không gian tổ chức
    contemp_chunks = [
        ch for ch in chunks
        if ch.heading_path == ["Không gian tổ chức"]
        and any("Không gian tái hiện đương đại" in p.text for p in ch.evidence_parts)
    ]
    assert len(contemp_chunks) == 1
    ch_contemp = contemp_chunks[0]
    assert "ngã ba Chợ Mai" in ch_contemp.search_text
    assert "Nguyễn Đình Tứ" in ch_contemp.search_text
    assert len(ch_contemp.evidence_parts) == 1
    p_contemp = ch_contemp.evidence_parts[0]
    assert doc.lf_text[p_contemp.start:p_contemp.end] == p_contemp.text

    # Assert historical and contemporary revival are strictly two distinct chunks
    assert ch_hist.chunk_id != ch_contemp.chunk_id

    # 3. Exact non-commercial nature chunk under Thông tin chung
    non_comm_chunks = [
        ch for ch in chunks
        if ch.heading_path == ["Thông tin chung"]
        and any("không mang tính thương mại đơn thuần" in p.text and "cầu may" in p.text for p in ch.evidence_parts)
    ]
    assert len(non_comm_chunks) == 1
    ch_non_comm = non_comm_chunks[0]
    assert "không mang tính thương mại đơn thuần" in ch_non_comm.search_text
    assert "cầu may" in ch_non_comm.search_text
    assert len(ch_non_comm.evidence_parts) == 1
    p_non_comm = ch_non_comm.evidence_parts[0]
    assert doc.lf_text[p_non_comm.start:p_non_comm.end] == p_non_comm.text


def test_acceptance_sample_dai_noi():
    """Verify Đại Nội Huế preserves Ngọ Môn structure, 5 entrances relationship, and exact evidence parts."""
    root, _ = discover_full_corpus_files()
    rel = "heritages/heritage/Đại Nội Huế.md"
    doc = parse_markdown_blocks(rel, read_source_lf(root / rel))
    chunks, errors = chunk_document(doc)
    assert len(errors) == 0
    assert len(chunks) > 0

    # Locate Ngọ Môn 5-entrance nested list chunk
    entrance_chunks = [
        ch for ch in chunks
        if "Ngọ Môn" in ch.heading_path
        and any("Cấu trúc phần đài nền" in p.text for p in ch.evidence_parts)
    ]
    assert len(entrance_chunks) == 1
    ch = entrance_chunks[0]

    # Verify all 5 entrance relationships are in this chunk's evidence parts
    assert any("Lối giữa" in p.text and "hoàng đế" in p.text for p in ch.evidence_parts)
    assert any("Tả Giáp môn" in p.text and "Hữu Giáp môn" in p.text and "quan văn" in p.text for p in ch.evidence_parts)
    assert any("Tả Dịch môn" in p.text and "Hữu Dịch môn" in p.text and "binh lính" in p.text for p in ch.evidence_parts)

    for p in ch.evidence_parts:
        assert doc.lf_text[p.start:p.end] == p.text


def test_acceptance_sample_lich_trinh_3n2d():
    """Verify Lịch trình du lịch Huế 3 ngày 2 đêm retains distinct day structures and timeline activities."""
    root, _ = discover_full_corpus_files()
    rel = "travel/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md"
    doc = parse_markdown_blocks(rel, read_source_lf(root / rel))
    chunks, errors = chunk_document(doc)
    assert len(errors) == 0
    assert len(chunks) > 0

    # Day 1 morning chunks: Đại Nội
    d1_morning = [
        ch for ch in chunks
        if ch.heading_path == ["Ngày 1: Phú Xuân–Thuận Hóa và hai bờ sông Hương", "Buổi đầu: Đại Nội hoặc cụm bảo tàng"]
    ]
    assert len(d1_morning) == 2
    assert any("Đại Nội" in ch.search_text for ch in d1_morning)

    # Day 1 evening chunk: Ca Huế vs Nhã nhạc distinction
    d1_evening = [
        ch for ch in chunks
        if ch.heading_path == ["Ngày 1: Phú Xuân–Thuận Hóa và hai bờ sông Hương", "Buổi tối: Hoạt động linh hoạt"]
    ]
    assert len(d1_evening) == 1
    assert "Ca Huế" in d1_evening[0].search_text
    assert "nhạc cung đình là loại hình khác" in d1_evening[0].search_text

    # Day 2 morning chunk: Kim Long & Chùa Thiên Mụ
    d2_morning = [
        ch for ch in chunks
        if ch.heading_path == ["Ngày 2: Kim Long–Thủy Xuân", "Buổi đầu: Kim Long"]
    ]
    assert len(d2_morning) == 1
    assert "Chùa Thiên Mụ" in d2_morning[0].search_text

    # Day 3 departure chunk: Thanh Thủy
    d3_morning = [
        ch for ch in chunks
        if ch.heading_path == ["Ngày 3: Một nhánh nhẹ và rời Huế", "Phương án mặc định: Thanh Thủy"]
    ]
    assert len(d3_morning) == 1
    assert "Thanh Thủy" in d3_morning[0].search_text

    for ch in chunks:
        for p in ch.evidence_parts:
            assert doc.lf_text[p.start:p.end] == p.text


def test_acceptance_sample_ca_hue_performing_art():
    """Verify Ca Huế trên sông Hương (performing art) preserves classical instruments and ensemble structure."""
    root, _ = discover_full_corpus_files()
    rel = "performing_arts/arts/Ca Huế trên sông Hương.md"
    doc = parse_markdown_blocks(rel, read_source_lf(root / rel))
    chunks, errors = chunk_document(doc)
    assert len(errors) == 0
    assert len(chunks) > 0
    assert doc.title == "Ca Huế trên sông Hương"

    # Locate classical orchestra instruments chunk
    orch_chunks = [
        ch for ch in chunks
        if ch.heading_path == ["Dàn nhạc, nhạc cụ và hệ thống bài bản tiêu biểu", "Cơ cấu dàn nhạc dân tộc"]
        and any("Dàn ngũ tuyệt cổ điển" in p.text for p in ch.evidence_parts)
    ]
    assert len(orch_chunks) == 1
    ch_orch = orch_chunks[0]

    # Verify all classical instruments
    assert any("đàn nguyệt" in p.text for p in ch_orch.evidence_parts)
    assert any("đàn tỳ bà" in p.text for p in ch_orch.evidence_parts)
    assert any("đàn nhị" in p.text for p in ch_orch.evidence_parts)
    assert any("đàn tranh" in p.text for p in ch_orch.evidence_parts)
    assert any("đàn tam" in p.text for p in ch_orch.evidence_parts)
    assert any("đàn bầu" in p.text for p in ch_orch.evidence_parts)

    # Locate percussion instruments chunk
    perc_chunks = [
        ch for ch in chunks
        if ch.heading_path == ["Dàn nhạc, nhạc cụ và hệ thống bài bản tiêu biểu", "Cơ cấu dàn nhạc dân tộc"]
        and any("Nhạc cụ điểm nhịp" in p.text for p in ch.evidence_parts)
    ]
    assert len(perc_chunks) == 1
    ch_perc = perc_chunks[0]
    assert any("Song loan" in p.text and "sênh sứa" in p.text for p in ch_perc.evidence_parts)

    for p in ch_orch.evidence_parts:
        assert doc.lf_text[p.start:p.end] == p.text
    for p in ch_perc.evidence_parts:
        assert doc.lf_text[p.start:p.end] == p.text


def test_acceptance_sample_ca_hue_tickets_and_conditions():
    """Verify Ca Huế tickets attaches lead and exclusions conditions correctly to Table A and Table B."""
    root, _ = discover_full_corpus_files()
    rel = "travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md"
    doc = parse_markdown_blocks(rel, read_source_lf(root / rel))
    chunks, errors = chunk_document(doc)
    assert len(errors) == 0

    # Look for Table A row chunks
    table_a_chunks = [
        ch for ch in chunks
        if "A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)" in ch.heading_path
        and any(p.role == "header" for p in ch.evidence_parts)
    ]
    assert len(table_a_chunks) == 4  # 4 rows in Table A

    # Each Table A chunk must have lead condition and exclusions condition
    for ch in table_a_chunks:
        cond_roles = [p for p in ch.evidence_parts if p.role == "condition"]
        assert len(cond_roles) == 2
        assert "Dưới đây là mức giá khảo sát" in cond_roles[0].text
        assert "Không bao gồm:" in cond_roles[1].text
        for p in ch.evidence_parts:
            assert doc.lf_text[p.start:p.end] == p.text

    # Look for Table B chunks (charter boat) - should only have lead condition, NOT exclusions condition
    table_b_chunks = [
        ch for ch in chunks
        if "B. Thuê trọn gói nguyên thuyền rồng biểu diễn Ca Huế riêng (Bao chuyến)" in ch.heading_path
        and any(p.role == "header" for p in ch.evidence_parts)
    ]
    assert len(table_b_chunks) >= 1
    for ch in table_b_chunks:
        cond_roles = [p for p in ch.evidence_parts if p.role == "condition"]
        assert len(cond_roles) == 1
        assert "Dưới đây là mức giá khảo sát" in cond_roles[0].text
        assert not any("Không bao gồm:" in p.text for p in cond_roles)


def test_acceptance_sample_chi_phi_du_lich():
    """Verify Chi phí du lịch Huế attaches intro condition to the 3 daily budget tables."""
    root, _ = discover_full_corpus_files()
    rel = "travel/services/Chi phí du lịch Huế.md"
    doc = parse_markdown_blocks(rel, read_source_lf(root / rel))
    chunks, errors = chunk_document(doc)
    assert len(errors) == 0

    target_sections = [
        "Dự toán một ngày tại Huế",
        "Dự toán hai ngày một đêm tại Huế",
        "Dự toán ba ngày hai đêm tại Huế",
    ]
    for sec in target_sections:
        sec_chunks = [ch for ch in chunks if sec in ch.heading_path]
        assert len(sec_chunks) > 0
        table_chunks = [ch for ch in sec_chunks if any(p.role in ("body", "header") and "|" in p.text for p in ch.evidence_parts)]
        assert len(table_chunks) > 0
        for ch in table_chunks:
            conds = [p for p in ch.evidence_parts if p.role == "condition"]
            assert len(conds) >= 1
            assert "Ngân sách du lịch Huế phụ thuộc" in conds[0].text
            for p in ch.evidence_parts:
                assert doc.lf_text[p.start:p.end] == p.text


# --- 8. Synthetic Isolated Error and Oversized Fail-Closed Blocking ---

def test_synthetic_oversized_group_blocking(tmp_path):
    """Verify pure oversized minimal unit triggers fail-closed blocking in preview without mixing condition errors."""
    kb_fake = tmp_path / "fake_kb"
    test_file = kb_fake / "foods" / "huge.md"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    # A single sentence with 2000 characters (cannot be sentence-split)
    massive_sentence = "Một_từ_siêu_dài_" * 150 + ".\n"
    test_file.write_text("# Tài Liệu Lớn\n\n## Mục\n\n" + massive_sentence, encoding="utf-8")

    # Empty conditions file to isolate oversized behavior completely
    empty_cond = tmp_path / "empty_cond.json"
    empty_cond.write_text("[]", encoding="utf-8")

    fake_settings = {
        "active_profile": "dense_only",
        "profiles": {"dense_only": {}},
        "full_corpus": {
            "knowledge_base": {
                "root_dir": str(kb_fake),
                "include_globs": ["foods/**/*.md"],
                "exclude_parts": ["evaluation"],
                "exclude_files": [],
            },
            "conditions_file": str(empty_cond),
            "embedding_models": [
                {
                    "id": "CODE4LIFEOFFICIAL/huydang-dek21-embedding",
                    "max_tokens": 256,
                    "prefix": "",
                    "word_segment": True,
                }
            ],
        },
    }

    out_json = tmp_path / "synthetic_blocked_preview.json"
    artifact, exit_code = generate_preview(out_json, settings=fake_settings)

    assert exit_code == 1
    assert artifact["status"] == "BLOCKED_OVERSIZED_GROUP"
    assert artifact["summary"]["oversized_groups_count"] >= 1
    assert len(artifact["oversized_groups"]) >= 1
    # Pure oversized: no non-oversized errors
    non_oversized = [e for e in artifact["errors"] if not e.startswith("Oversized group:")]
    assert len(non_oversized) == 0


def test_generic_condition_or_parser_error_blocks_preview(tmp_path):
    """Verify generic condition error triggers non-PASS exit 1 status without oversized groups."""
    kb_fake = tmp_path / "fake_kb"
    test_file = kb_fake / "foods" / "normal.md"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("# Tài Liệu Nhỏ\n\n## Mục\n\nĐoạn văn ngắn gọn phù hợp trần token.\n", encoding="utf-8")

    # Condition file referencing non-existent selector to cause condition error
    bad_cond = tmp_path / "bad_cond.json"
    bad_cond.write_text(json.dumps([{
        "source": "foods/normal.md",
        "condition": {"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Không tồn tại"},
        "targets": [{"heading_path": ["Mục"], "block_type": "paragraph", "exact_text": "Đoạn văn ngắn gọn phù hợp trần token."}],
    }]), encoding="utf-8")

    fake_settings = {
        "active_profile": "dense_only",
        "profiles": {"dense_only": {}},
        "full_corpus": {
            "knowledge_base": {
                "root_dir": str(kb_fake),
                "include_globs": ["foods/**/*.md"],
                "exclude_parts": ["evaluation"],
                "exclude_files": [],
            },
            "conditions_file": str(bad_cond),
            "embedding_models": [
                {
                    "id": "CODE4LIFEOFFICIAL/huydang-dek21-embedding",
                    "max_tokens": 256,
                    "prefix": "",
                    "word_segment": True,
                }
            ],
        },
    }

    out_json = tmp_path / "generic_error_preview.json"
    artifact, exit_code = generate_preview(out_json, settings=fake_settings)

    assert exit_code == 1
    assert artifact["status"] == "BLOCKED_ERRORS"
    assert artifact["summary"]["blocking_errors_count"] >= 1
    assert len(artifact["errors"]) >= 1
    assert artifact["summary"]["oversized_groups_count"] == 0
    assert len(artifact["oversized_groups"]) == 0


# --- 9. Canonical Preview Invariants & PASS ---

def test_canonical_preview_pass():
    """Verify canonical full-corpus preview passes with zero blocking errors, zero oversized groups, and self-consistent breakdowns."""
    canonical_path = BACKEND_DIR.parent / "reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json"
    with canonical_path.open("r", encoding="utf-8") as f:
        artifact = json.load(f)

    assert artifact["status"] == "PASS"
    total_files = artifact["summary"]["total_files"]
    total_chunks = artifact["summary"]["total_chunks"]
    assert total_files == 205
    assert artifact["summary"]["condition_rules_count"] == 3
    assert artifact["summary"]["blocking_errors_count"] == 0
    assert artifact["summary"]["oversized_groups_count"] == 0

    # Domain breakdown (5 domains)
    assert len(artifact["domain_breakdown"]) == 5
    assert sum(d["file_count"] for d in artifact["domain_breakdown"].values()) == total_files
    assert sum(d["chunk_count"] for d in artifact["domain_breakdown"].values()) == total_chunks

    # P7 breakdown (7 partitions)
    assert len(artifact["p7_breakdown"]) == 7
    assert sum(p["file_count"] for p in artifact["p7_breakdown"].values()) == total_files
    assert sum(p["chunk_count"] for p in artifact["p7_breakdown"].values()) == total_chunks

    # Tokenizer limits: all models <= max_tokens
    for mid, tinfo in artifact["tokenizer_limits"].items():
        assert tinfo["max_observed_tokens"] <= tinfo["max_tokens"], (
            f"Model {mid} exceeded limit: {tinfo['max_observed_tokens']} > {tinfo['max_tokens']}"
        )


# --- 10. Full-Corpus Determinism, Exact Evidence Slicing, and Preview Byte Equality ---

def test_full_corpus_determinism_and_preview_byte_equality(tmp_path):
    """Verify repeated preview runs produce byte-identical JSON and chunks match canonical totals."""
    canonical_path = BACKEND_DIR.parent / "reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json"
    with canonical_path.open("r", encoding="utf-8") as f:
        canonical = json.load(f)
    expected_chunks = canonical["summary"]["total_chunks"]
    expected_files = canonical["summary"]["total_files"]

    root, files = discover_full_corpus_files()
    assert len(files) == expected_files

    # Run chunk_full_corpus twice for deep equality verification
    chunks_run1, errors1 = chunk_full_corpus()
    assert len(errors1) == 0
    assert len(chunks_run1) == expected_chunks

    chunks_run2, errors2 = chunk_full_corpus()
    assert len(errors2) == 0
    assert len(chunks_run2) == expected_chunks

    # Deep equality across all chunks between both runs
    seen_chunk_ids = set()
    seen_point_ids = set()
    for c1, c2 in zip(chunks_run1, chunks_run2):
        assert c1.chunk_id == c2.chunk_id
        assert c1.point_id == c2.point_id
        assert c1.source == c2.source
        assert c1.title == c2.title
        assert c1.heading_path == c2.heading_path
        assert c1.search_text == c2.search_text
        assert c1.evidence_parts == c2.evidence_parts

        # Assert point_id invariants: deterministic helper, uniqueness, UUID5 version
        expected_point_id = point_id_for_chunk_id(c1.chunk_id)
        assert c1.point_id == expected_point_id
        assert c1.chunk_id not in seen_chunk_ids
        assert c1.point_id not in seen_point_ids
        seen_chunk_ids.add(c1.chunk_id)
        seen_point_ids.add(c1.point_id)

        parsed_uuid = uuid.UUID(c1.point_id)
        assert parsed_uuid.version == 5

    assert len(seen_chunk_ids) == expected_chunks
    assert len(seen_point_ids) == expected_chunks

    # Verify 100% exact evidence slicing across all chunks in run 1
    for ch in chunks_run1:
        full_path = root / ch.source
        lf_text = read_source_lf(full_path)
        for part in ch.evidence_parts:
            assert lf_text[part.start:part.end] == part.text, (
                f"Slice mismatch in chunk {ch.chunk_id}: {part.text!r} != {lf_text[part.start:part.end]!r}"
            )

    # Generate preview to two distinct paths and verify byte-identical equality
    p1 = tmp_path / "preview_run1.json"
    p2 = tmp_path / "preview_run2.json"
    generate_preview(p1)
    generate_preview(p2)
    assert p1.read_bytes() == p2.read_bytes()

    # Verify generated preview totals match canonical artifact totals
    preview_data = json.loads(p1.read_text(encoding="utf-8"))
    assert preview_data["summary"]["total_files"] == expected_files
    assert preview_data["summary"]["total_chunks"] == expected_chunks
    assert sum(d["chunk_count"] for d in preview_data["domain_breakdown"].values()) == expected_chunks
    assert sum(p["chunk_count"] for p in preview_data["p7_breakdown"].values()) == expected_chunks
    assert sum(d["file_count"] for d in preview_data["domain_breakdown"].values()) == expected_files
    assert sum(p["file_count"] for p in preview_data["p7_breakdown"].values()) == expected_files
