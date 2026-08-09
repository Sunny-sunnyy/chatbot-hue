"""Tests for foods Markdown parsing and chunking."""
import re
from pathlib import Path

from ingestion.chunking.markdown_chunker import (
    EXCLUDED_SECTIONS,
    _chunk_file,
    _clean_body,
    _context_label,
    chunk_foods_markdown,
)
from ingestion.helpers.make_metadata import make_metadata
from ingestion.helpers.markdown_parser import parse_document
from ingestion.helpers.split_text import _LIST_ITEM, split_text

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


def _content_of(chunk):
    """Return the chunk content without the leading label line."""
    return chunk["text"].split("\n", 1)[1]


def _contains_table(content):
    """True when content includes a Markdown table separator row."""
    lines = content.splitlines()
    return any(
        "|" in lines[i - 1] and "-" in line and TABLE_SEPARATOR.match(line)
        for i, line in enumerate(lines[1:], start=1)
    )


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


def test_split_text_keeps_unbreakable_block_whole():
    # No sentence end and no space: the block cannot be cut without splitting
    # words, so it stays whole even when longer than the limit.
    block = "x" * 2000
    assert split_text(block, max_chars=500) == [block]


def test_split_text_prefers_sentence_boundary():
    text = "Đây là câu một. " * 40
    chunks = split_text(text, max_chars=200)
    assert all(len(c) <= 200 for c in chunks)
    assert len(chunks) > 1
    # No character is lost or duplicated: cuts only remove whitespace.
    assert "".join(chunks).replace(" ", "") == text.replace(" ", "")


def test_split_text_splits_long_sentence_at_space():
    text = "từ " * 120
    chunks = split_text(text, max_chars=100)
    assert all(len(c) <= 100 for c in chunks)
    assert len(chunks) >= 3
    assert "".join(chunks).replace(" ", "") == text.replace(" ", "")


def test_split_text_keeps_table_whole():
    rows = "| Món | Giá |\n|---|---:|\n" + "".join(
        f"| Món {i} | 50.000 VNĐ |\n" for i in range(40)
    )
    assert len(rows) > 400
    assert split_text(rows, max_chars=400) == [rows.strip()]


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
    # Tái hiện foods/local_specialties/banh canh nam pho.md, mục
    # "Thành phần và đặc điểm": dòng xuống hàng thụt lề thuộc mục trước.
    text = (
        "- **Sợi bánh:** Bột gạo được pha với bột lọc theo tỷ lệ gia truyền, thường được\n"
        "  mô tả khoảng 3 phần bột gạo và 1 phần bột lọc. Sợi bánh có màu trắng trong.\n"
        "- **Nhân tôm cua:** Tôm tươi và thịt ba chỉ được giã hoặc xay nhuyễn, vo viên\n"
        "  nhỏ hoặc dàn mỏng rồi nấu chín. Phần nhân có màu đỏ gạch tự nhiên và hòa\n"
        "  quyện trong nước dùng thay vì chỉ đặt riêng bên trên.\n"
        "- **Nước dùng:** Nước được ninh từ xương cùng nước luộc tôm, cua.\n"
    )
    chunks = split_text(text, max_chars=400)
    # "Phần nhân..." không được tách khỏi mục "Nhân tôm cua" khi cả mục < 400.
    target = next(c for c in chunks if "**Nhân tôm cua:**" in c)
    assert "Phần nhân có màu đỏ gạch" in target
    assert len(target) <= 400
    # Điểm chia chỉ nằm giữa các mục, không bao giờ giữa một mục.
    for chunk in chunks:
        for line in chunk.splitlines()[1:]:
            assert _LIST_ITEM.match(line) or line.startswith("  ")


def test_wrapped_list_items_stay_together_in_corpus():
    chunks = chunk_foods_markdown()
    target = next(
        c for c in chunks
        if c["metadata"]["source"] == "foods/local_specialties/banh canh nam pho.md"
        and c["metadata"]["section"] == "Thành phần và đặc điểm"
        and "**Nhân tôm cua:**" in c["text"]
    )
    assert "Phần nhân có màu đỏ gạch" in target["text"]


def test_no_chunk_starts_with_wrapped_list_line():
    for chunk in chunk_foods_markdown():
        first = chunk["text"].split("\n", 1)[1].splitlines()[0]
        assert _LIST_ITEM.match(first) or not first.startswith("  "), (
            "chunk must not start with a wrapped line cut off its item"
        )


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


def test_context_label_direct_mapping():
    assert _context_label("restaurants", "Tóm tắt", "Nội dung.") == "giới thiệu"
    assert _context_label("cafes", "Menu và giá tham khảo", "Bảng.") == "menu"
    assert _context_label("cafes", "Món ăn / trải nghiệm", "Nội dung.") == "trải nghiệm"
    assert _context_label("local_specialties", "Cách làm tóm tắt", "Nội dung.") == "cách làm"
    assert _context_label("local_specialties", "Nguồn gốc và bối cảnh", "Nội dung.") == "nguồn gốc"
    assert _context_label("guide", "Gợi ý ăn sáng", "Nội dung.") == "ăn sáng"
    assert _context_label("guide", "Food tour 1 ngày", "Nội dung.") == "tour 1 ngày"


def test_context_label_thong_tin_single_topic():
    assert _context_label("restaurants", "Thông tin", "- Địa chỉ: 52 Tôn Thất Thiệp.") == "địa chỉ"
    assert _context_label("cafes", "Thông tin", "- Giờ hoạt động: 07:30 – 21:30.") == "giờ hoạt động"
    assert _context_label("restaurants", "Thông tin", "- Mức giá: 25.000 VNĐ.") == "mức giá"


def test_context_label_thong_tin_multi_or_no_topic():
    multi = "- Địa chỉ: A.\n- Giờ hoạt động: B.\n- Mức giá: C."
    assert _context_label("restaurants", "Thông tin", multi) == "thông tin quán"
    assert _context_label("cafes", "Thông tin", "- Điện thoại: 0123.") == "thông tin quán"


def test_context_label_fallback_is_short_heading():
    assert _context_label("restaurants", "Ưu đãi tham khảo", "Nội dung.") == "ưu đãi"
    assert _context_label("restaurants", "Mục chưa biết", "Nội dung.") == "mục chưa biết"


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


def test_chunk_file_text_has_context_label(tmp_path):
    path = tmp_path / "quan x.md"
    path.write_text("# Quán X\n\n## Tóm tắt\n\nNội dung ngắn.\n", encoding="utf-8")
    chunks = _chunk_file(path, tmp_path)
    assert len(chunks) == 1
    assert chunks[0]["text"].startswith("Quán X — giới thiệu\n")
    assert chunks[0]["text"].endswith("Nội dung ngắn.")


def test_chunk_file_splits_long_sections(tmp_path):
    body = "\n\n".join("Câu một. " * 50 for _ in range(3))
    path = tmp_path / "mon y.md"
    path.write_text(f"# Món Y\n\n## Thông tin\n\n{body}\n", encoding="utf-8")
    chunks = _chunk_file(path, tmp_path)
    assert len(chunks) == 6
    assert all(chunk["metadata"]["section"] == "Thông tin" for chunk in chunks)
    assert all(len(_content_of(chunk)) <= 400 for chunk in chunks)
    ids = [chunk["metadata"]["chunk_id"] for chunk in chunks]
    assert len(ids) == len(set(ids))


def test_chunk_foods_markdown_gate():
    chunks = chunk_foods_markdown()
    assert chunks
    for chunk in chunks:
        assert chunk["text"].strip()
        assert REQUIRED_METADATA <= chunk["metadata"].keys()
        assert chunk["text"].count("\n") >= 1


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


def test_no_normal_chunk_over_400():
    for chunk in chunk_foods_markdown():
        content = _content_of(chunk)
        if not _contains_table(content):
            assert len(content) <= 400


def test_corpus_covers_91_files():
    sources = {c["metadata"]["source"] for c in chunk_foods_markdown()}
    assert len(sources) == 91
