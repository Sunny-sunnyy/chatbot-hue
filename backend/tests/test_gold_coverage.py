"""Đếm đoạn đúng (Phase 8.1 G1, gold v2): trích dẫn là dòng tiêu đề Markdown thì trúng chunk mang tiêu đề đó trong heading_path. Chuỗi tự viết."""
from experiments.phase_8_1.g1_retrieval import quote_is_chunk_heading

PAYLOAD = {"source": "domain/vi_du.md", "heading_path": ["Mục A", "Mục B (phần một)"],
           "evidence_parts": [{"start": 500, "end": 900}]}


def test_heading_line_hits_chunk_carrying_that_heading():
    assert quote_is_chunk_heading(PAYLOAD, "### Mục B (phần một)")
    assert quote_is_chunk_heading(PAYLOAD, "## Mục A")


def test_body_text_or_other_heading_does_not_count_as_heading_hit():
    assert not quote_is_chunk_heading(PAYLOAD, "Mục B (phần một)")  # cùng chữ nhưng không phải dòng tiêu đề
    assert not quote_is_chunk_heading(PAYLOAD, "### Mục C")
