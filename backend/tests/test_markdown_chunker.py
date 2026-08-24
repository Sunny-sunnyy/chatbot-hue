"""Tests for foods Markdown chunking and text splitting."""
import re
import pytest

from ingestion.chunking import markdown_chunker
from ingestion.chunking.markdown_chunker import chunk_foods_markdown
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

TABLE_SEPARATOR = re.compile(r"^\s*\|?[\s|:.-]*\|\s*$")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")


def _contains_table(content):
    """True when content includes a Markdown table separator row."""
    lines = content.splitlines()
    return any(
        "|" in lines[i - 1] and "-" in line and TABLE_SEPARATOR.match(line)
        for i, line in enumerate(lines[1:], start=1)
    )


# --- Splitter tests ---


def test_split_text_keeps_short_text_whole():
    assert split_text("Một đoạn ngắn.") == ["Một đoạn ngắn."]


def test_split_text_packs_paragraphs_within_max():
    text = "a" * 100 + "\n\n" + "b" * 100 + "\n\n" + "c" * 100
    assert split_text(text, max_chars=250) == ["a" * 100 + "\n" + "b" * 100, "c" * 100]


def test_split_text_prefers_sentence_boundary():
    text = "Đây là câu một. " * 40
    chunks = split_text(text, max_chars=200)
    assert all(len(c) <= 200 for c in chunks)
    assert len(chunks) > 1
    assert "".join(chunks).replace(" ", "") == text.replace(" ", "")


def test_split_text_splits_long_sentence_at_space():
    text = "từ " * 120
    chunks = split_text(text, max_chars=100)
    assert all(len(c) <= 100 for c in chunks)
    assert len(chunks) >= 3
    assert "".join(chunks).replace(" ", "") == text.replace(" ", "")


def test_split_text_keeps_unbreakable_block_whole():
    block = "x" * 2000
    assert split_text(block, max_chars=500) == [block]


def test_split_text_breaks_list_between_lines():
    lines = [f"- Món {i}: " + "mô tả" * 25 for i in range(4)]
    text = "\n".join(lines)
    chunks = split_text(text, max_chars=300)
    assert all(len(c) <= 300 for c in chunks)
    original = set(lines)
    for chunk in chunks:
        for line in chunk.splitlines():
            assert line in original, "list line must never be cut"


def test_split_text_keeps_wrapped_list_item_whole():
    text = (
        "- **Sợi bánh:** Bột gạo được pha với bột lọc theo tỷ lệ gia truyền, thường được\n"
        "  mô tả khoảng 3 phần bột gạo và 1 phần bột lọc. Sợi bánh có màu trắng trong.\n"
        "- **Nhân tôm cua:** Tôm tươi và thịt ba chỉ được giã hoặc xay nhuyễn, vo viên\n"
        "  nhỏ hoặc dàn mỏng rồi nấu chín. Phần nhân có màu đỏ gạch tự nhiên và hòa\n"
        "  quyện trong nước dùng thay vị chỉ đặt riêng bên trên.\n"
        "- **Nước dùng:** Nước được ninh từ xương cùng nước luộc tôm, cua.\n"
    )
    chunks = split_text(text, max_chars=400)
    target = next(c for c in chunks if "**Nhân tôm cua:**" in c)
    assert "Phần nhân có màu đỏ gạch" in target
    assert len(target) <= 400
    for chunk in chunks:
        for line in chunk.splitlines()[1:]:
            assert LIST_ITEM_RE.match(line) or line.startswith("  ")


def test_split_text_keeps_table_whole():
    rows = "| Món | Giá |\n|---|---:|\n" + "".join(
        f"| Món {i} | 50.000 VNĐ |\n" for i in range(40)
    )
    assert len(rows) > 400
    assert split_text(rows, max_chars=400) == [rows.strip()]


# --- Chunker unit tests with discovery seam ---


def test_chunk_file_h1_title_h2_sections_and_h3_retained(tmp_path, monkeypatch):
    file_path = tmp_path / "foods" / "restaurants" / "quan_x.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        "# Quán X tại Huế\n\n"
        "## Tóm tắt\n\n"
        "Giới thiệu quán X.\n\n"
        "### Không gian\n\n"
        "Không gian rộng rãi.\n\n"
        "## Thông tin\n\n"
        "- Địa chỉ: 123 Đường Y, Huế\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        markdown_chunker, "_discover_markdown_files", lambda: (tmp_path, [file_path])
    )
    chunks = chunk_foods_markdown()
    assert len(chunks) == 2

    # First chunk (Tóm tắt + H3 retained in body)
    c0 = chunks[0]
    assert c0["metadata"]["title"] == "Quán X tại Huế"
    assert c0["metadata"]["section"] == "Tóm tắt"
    assert c0["metadata"]["subcategory"] == "restaurants"
    assert c0["metadata"]["category"] == "foods"
    assert c0["metadata"]["chunk_type"] == "section"
    assert c0["metadata"]["source"] == "foods/restaurants/quan_x.md"
    assert c0["metadata"]["chunk_id"] == "foods/restaurants/quan_x.md|Tóm tắt|0"
    assert c0["text"].startswith("Quán X tại Huế — giới thiệu\n")
    assert "### Không gian" in c0["text"]

    # Second chunk (Thông tin with single topic)
    c1 = chunks[1]
    assert c1["metadata"]["section"] == "Thông tin"
    assert c1["metadata"]["chunk_id"] == "foods/restaurants/quan_x.md|Thông tin|1"
    assert c1["text"].startswith("Quán X tại Huế — địa chỉ\n")


def test_chunk_file_excludes_source_section_and_image_lines(tmp_path, monkeypatch):
    file_path = tmp_path / "foods" / "cafes" / "cafe_y.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        "# Cà Phê Y\n\n"
        "## Giới thiệu\n\n"
        "Quán cà phê view đẹp.\n"
        "![Hình ảnh quán](https://example.com/photo.jpg)\n"
        "Đồ uống ngon.\n\n"
        "## Nguồn dữ liệu\n\n"
        "- https://example.com/source\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        markdown_chunker, "_discover_markdown_files", lambda: (tmp_path, [file_path])
    )
    chunks = chunk_foods_markdown()
    assert len(chunks) == 1
    assert chunks[0]["metadata"]["section"] == "Giới thiệu"
    assert "![" not in chunks[0]["text"]
    assert "Quán cà phê view đẹp.\nĐồ uống ngon." in chunks[0]["text"]


def test_chunk_file_fails_fast_on_missing_h1(tmp_path, monkeypatch):
    file_path = tmp_path / "foods" / "restaurants" / "no_h1.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        "## Tóm tắt\n\nNội dung không có H1.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        markdown_chunker, "_discover_markdown_files", lambda: (tmp_path, [file_path])
    )
    with pytest.raises(ValueError, match="H1"):
        chunk_foods_markdown()


def test_chunk_file_fails_fast_on_missing_answer_h2(tmp_path, monkeypatch):
    file_path = tmp_path / "foods" / "restaurants" / "only_source.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        "# Quán Chỉ Có Nguồn\n\n## Nguồn dữ liệu\n\n- https://example.com\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        markdown_chunker, "_discover_markdown_files", lambda: (tmp_path, [file_path])
    )
    with pytest.raises(ValueError, match="H2"):
        chunk_foods_markdown()


def test_chunk_file_fails_fast_on_image_only_answer_h2(tmp_path, monkeypatch):
    file_path = tmp_path / "foods" / "restaurants" / "only_image.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        "# Quán Chỉ Có Ảnh\n\n"
        "## Giới thiệu\n\n"
        "![Hình ảnh](https://example.com/pic.jpg)\n\n"
        "## Nguồn dữ liệu\n\n"
        "- https://example.com\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        markdown_chunker, "_discover_markdown_files", lambda: (tmp_path, [file_path])
    )
    with pytest.raises(ValueError, match="H2"):
        chunk_foods_markdown()


# --- Full real corpus tests ---


def test_chunk_foods_markdown_real_corpus_invariants():
    chunks = chunk_foods_markdown()
    assert chunks

    sources = set()
    chunk_ids = []
    for chunk in chunks:
        # Non-empty text and label line
        text = chunk["text"]
        assert text.strip()
        lines = text.split("\n", 1)
        assert len(lines) == 2, "chunk must have a label line and body"
        label_line, body = lines[0], lines[1]
        assert label_line.startswith(chunk["metadata"]["title"] + " — ")
        assert "![" not in text
        assert chunk["metadata"]["section"] != "Nguồn dữ liệu"

        # Exact 7 metadata fields
        meta = chunk["metadata"]
        assert set(meta.keys()) == REQUIRED_METADATA

        # Source is KB-relative
        src = meta["source"]
        assert not src.startswith("/")
        assert src.startswith("foods/")
        parts = src.split("/")
        assert "evaluation" not in parts
        assert "_source-dumps" not in parts
        assert "meta" not in parts
        sources.add(src)

        # ID uniqueness and format
        cid = meta["chunk_id"]
        assert cid == f"{src}|{meta['section']}|{cid.rsplit('|', 1)[-1]}"
        chunk_ids.append(cid)

        # Length limit (normal chunks <= 400 chars, table exception allowed)
        if not _contains_table(body):
            assert len(body) <= 400

    assert sources
    assert len(chunk_ids) == len(set(chunk_ids)), "chunk_id must be unique across corpus"


def test_chunk_foods_markdown_deterministic_output():
    run1 = chunk_foods_markdown()
    run2 = chunk_foods_markdown()
    assert run1 == run2
