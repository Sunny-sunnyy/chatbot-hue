"""Thước R4 (Phase 8.2 §10): số trong câu trả lời phải có trong câu hỏi hoặc nguồn được trích. Chuỗi thử tự viết, không lấy từ kho."""
from experiments.phase_8_2.r4_numbers import normalize_number, number_tokens, unsupported_numbers
from retrieval.full_corpus_context import PackedSource


def source(number: int, *excerpts: str) -> PackedSource:
    return PackedSource(id=number, title="Quán thử", heading_path=("Giá",), excerpts=excerpts)


def test_normalize_number_formats():
    assert normalize_number("95.000") == normalize_number("95,000") == normalize_number("95000") == "95000"
    assert normalize_number("1.200.000") == "1200000"
    assert normalize_number("2,5") == "2.5"
    assert normalize_number("08:00") == "8:00"


def test_number_tokens_split_ranges_and_skip_citation_labels():
    assert number_tokens("mở 3–5 ngày, giá 100.000-700.000 đồng [1] [Nguồn 2]") == {"3", "5", "100000", "700000"}


def test_supported_numbers_pass():
    sources = (source(1, "Lễ kéo dài từ 3 đến 5 ngày; vé 95,000 đồng."),)
    assert unsupported_numbers("Lễ kéo dài 3–5 ngày, vé 95.000 đồng. [1]", "Lễ kéo dài mấy ngày?", sources) == []


def test_number_only_in_uncited_source_is_flagged():
    sources = (source(1, "Vé 50.000 đồng."), source(2, "Mở cửa từ năm 1999."))
    assert unsupported_numbers("Vé 50.000 đồng, mở từ năm 1999. [1]", "Vé bao nhiêu?", sources) == ["1999"]


def test_numbers_from_question_are_not_flagged():
    sources = (source(1, "Mùa mưa từ tháng 10."),)
    assert unsupported_numbers("Tháng 11 thuộc mùa mưa từ tháng 10. [1]", "Tháng 11 có mưa không?", sources) == []


def test_answer_without_citation_is_not_checked():
    assert unsupported_numbers("Tôi không tìm thấy 2 nguồn.", "Hỏi gì?", (source(1, "x"),)) == []
