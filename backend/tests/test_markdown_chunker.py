"""Tests for foods Markdown parsing and chunking."""
from pathlib import Path

from ingestion.chunking.markdown_chunker import (
    EXCLUDED_SECTIONS,
    _chunk_file,
    _clean_body,
    chunk_foods_markdown,
)
from ingestion.helpers.make_metadata import make_metadata
from ingestion.helpers.markdown_parser import parse_document
from ingestion.helpers.split_text import split_text

REQUIRED_METADATA = {
    "chunk_id",
    "source",
    "title",
    "section",
    "category",
    "subcategory",
    "chunk_type",
}


def test_parse_document_splits_sections():
    text = (
        "# Quán X\n\n"
        "## Tóm tắt\n\n"
        "Nội dung.\n\n"
        "### Chi tiết\n\n"
        "- điểm\n\n"
        "## Thông tin\n\n"
        "- Địa chỉ: A\n"
    )
    title, sections = parse_document(text)
    assert title == "Quán X"
    assert [s["heading"] for s in sections] == ["Tóm tắt", "Thông tin"]
    assert "### Chi tiết" in sections[0]["body"]


def test_parse_document_captures_intro_content():
    text = "# Quán X\n\nGiới thiệu ngắn.\n\n## Thông tin\n\n- Địa chỉ: A\n"
    title, sections = parse_document(text)
    assert title == "Quán X"
    assert sections[0]["heading"] == ""
    assert "Giới thiệu ngắn." in sections[0]["body"]


def test_split_text_keeps_short_text_whole():
    assert split_text("Một đoạn ngắn.") == ["Một đoạn ngắn."]


def test_split_text_packs_paragraphs_within_max():
    text = "a" * 100 + "\n\n" + "b" * 100 + "\n\n" + "c" * 100
    assert split_text(text, max_chars=250) == ["a" * 100 + "\n" + "b" * 100, "c" * 100]


def test_split_text_keeps_oversized_block_whole():
    block = "x" * 2000
    assert split_text(block, max_chars=500) == [block]


def test_make_metadata_fields():
    metadata = make_metadata(
        "foods/restaurants/quan x.md", "Quán X", "Thông tin", "restaurants", 3
    )
    assert metadata["chunk_id"] == "foods/restaurants/quan x.md|Thông tin|3"
    assert metadata["category"] == "foods"
    assert metadata["chunk_type"] == "section"


def test_clean_body_drops_image_lines():
    lines = ["Đoạn văn.", "![Ảnh](https://example.com/x.jpg?w=100)", "- Món ngon"]
    assert _clean_body(lines) == "Đoạn văn.\n- Món ngon"


def test_chunk_file_skips_source_sections(tmp_path):
    path = tmp_path / "mon x.md"
    path.write_text(
        "# Món X\n\n## Thông tin\n\n- Địa chỉ: A\n\n## Nguồn dữ liệu\n\n- src\n",
        encoding="utf-8",
    )
    chunks = _chunk_file(path, tmp_path)
    assert len(chunks) == 1
    assert chunks[0]["metadata"]["section"] == "Thông tin"
    assert chunks[0]["metadata"]["subcategory"] == "guide"


def test_chunk_file_splits_long_sections(tmp_path):
    body = "\n\n".join("Đoạn %d " % i + "nội dung " * 90 for i in range(3))
    path = tmp_path / "mon y.md"
    path.write_text(f"# Món Y\n\n## Thông tin\n\n{body}\n", encoding="utf-8")
    chunks = _chunk_file(path, tmp_path)
    assert len(chunks) == 3
    assert all(chunk["metadata"]["section"] == "Thông tin" for chunk in chunks)
    ids = [chunk["metadata"]["chunk_id"] for chunk in chunks]
    assert len(ids) == len(set(ids))


def test_chunk_foods_markdown_gate():
    chunks = chunk_foods_markdown()
    assert chunks
    for chunk in chunks:
        assert chunk["text"].strip()
        assert REQUIRED_METADATA <= chunk["metadata"].keys()


def test_chunk_sources_are_kb_relative():
    sources = {c["metadata"]["source"] for c in chunk_foods_markdown()}
    assert sources
    assert all(source.startswith("foods/") for source in sources)
    assert "foods/food-guides.md" in sources


def test_no_excluded_folders_indexed():
    for chunk in chunk_foods_markdown():
        parts = chunk["metadata"]["source"].split("/")
        assert "evaluation" not in parts
        assert "_source-dumps" not in parts
        assert "meta" not in parts


def test_no_absolute_paths_in_metadata():
    for chunk in chunk_foods_markdown():
        for value in chunk["metadata"].values():
            assert not str(value).startswith("/")


def test_chunk_ids_unique():
    chunks = chunk_foods_markdown()
    ids = [c["metadata"]["chunk_id"] for c in chunks]
    assert len(ids) == len(set(ids))


def test_chunk_ids_stable_across_runs():
    first = [c["metadata"]["chunk_id"] for c in chunk_foods_markdown()]
    second = [c["metadata"]["chunk_id"] for c in chunk_foods_markdown()]
    assert first == second


def test_source_sections_excluded_from_corpus():
    sections = {c["metadata"]["section"] for c in chunk_foods_markdown()}
    assert EXCLUDED_SECTIONS.isdisjoint(sections)


def test_no_image_markdown_in_chunk_text():
    for chunk in chunk_foods_markdown():
        assert "![" not in chunk["text"]
