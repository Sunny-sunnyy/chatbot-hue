"""Đếm đoạn đúng (Phase 8.1 G1, gold v2 trở đi): trích dẫn là dòng tiêu đề Markdown thì trúng chunk mang tiêu đề đó trong heading_path;
một fact được phủ khi một trích dẫn bất kỳ của nó trúng (gold v3 câu 138 dựa vào luật này). Chuỗi tự viết."""
from experiments.phase_8_1.g1_retrieval import gold_coverage, quote_is_chunk_heading

PAYLOAD = {"source": "domain/vi_du.md", "heading_path": ["Mục A", "Mục B (phần một)"],
           "evidence_parts": [{"start": 500, "end": 900}]}


def test_heading_line_hits_chunk_carrying_that_heading():
    assert quote_is_chunk_heading(PAYLOAD, "### Mục B (phần một)")
    assert quote_is_chunk_heading(PAYLOAD, "## Mục A")


def test_body_text_or_other_heading_does_not_count_as_heading_hit():
    assert not quote_is_chunk_heading(PAYLOAD, "Mục B (phần một)")  # cùng chữ nhưng không phải dòng tiêu đề
    assert not quote_is_chunk_heading(PAYLOAD, "### Mục C")


def test_fact_is_covered_by_any_one_of_its_quotes_and_all_needs_every_fact():
    # chunk giao khoảng [500, 900) của file ví dụ ⇒ trích dẫn [600, 650) trúng; trích dẫn ở file khác không trúng (không đọc file)
    hit, miss = ("domain/vi_du.md", 600, 650), ("domain/khac.md", 600, 650)
    assert gold_coverage([[miss, hit]], [PAYLOAD]) == {"all": 1.0, "frac": 1.0}
    assert gold_coverage([[hit], [miss]], [PAYLOAD]) == {"all": 0.0, "frac": 0.5}
