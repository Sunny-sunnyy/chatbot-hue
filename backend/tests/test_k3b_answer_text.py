"""Đếm câu không citation (theo dõi W2, plan phụ lục K3b-m): `[n]` đứng sau dấu chấm vẫn thuộc câu trước (B58 m-1). Chuỗi tự viết."""
from experiments.phase_8_2.k3b_answer import uncited_sentences


def test_citation_after_period_belongs_to_previous_sentence():
    assert uncited_sentences("Giá vé 50.000 đồng.[1] Nguồn không nêu giờ mở cửa.") == 1
    assert uncited_sentences("Câu một.[1] Câu hai [Nguồn 2].") == 0


def test_numbers_with_dots_are_not_sentence_breaks():
    assert uncited_sentences("Giá 1.100.000–1.200.000 đồng [1].") == 0
    assert uncited_sentences("Không có trích dẫn nào.") == 1


def test_citation_after_space_or_lowercase_label():
    assert uncited_sentences("Quán mở cửa từ 6 giờ. [1]") == 0
    assert uncited_sentences("Câu một. [1] Câu hai. [nguồn 2]") == 0
    assert uncited_sentences("Câu một. [1] Nguồn không nêu giá.") == 1
