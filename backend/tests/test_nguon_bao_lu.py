"""Nguồn "Tin bão / lũ chính thức" gửi cho giao diện (soát khác hãng 22/11/2026) — 0 USD, không gọi model, không Qdrant.
Vì sao: khi model gọi công cụ thời tiết loại bão / lũ, code đăng một nguồn mà đoạn trích là CHỮ DẶN CHO MODEL (`tt.KET_QUA_BAO_LU`: "…không viết là có
hay không có bão, lũ; không trấn an; chỉ trả lời phần khác của câu hỏi"). Model trích nguồn đó ⇒ người dùng bấm mở nguồn là đọc thấy lời dặn nội bộ
(sổ vết 17–22/11: 9 / 21 lượt bão / lũ thật có trích). Sửa: đoạn trích gửi giao diện của nguồn đó là câu bản tin chính thức + 112 (`tt.CAU_BAO_LU`, câu
đang dùng); chữ model nhận không đổi. Một hàm (`_source_responses`) cho cả đường stream lẫn không stream."""
from api.routes.chat import _source_responses
from llm import thoi_tiet as tt
from retrieval.full_corpus_context import PackedSource

BAO_LU = PackedSource(3, tt.TIEU_DE_NGUON_BAO_LU, (), (tt.KET_QUA_BAO_LU,), tt.NGUON_SOURCE)
KHO = PackedSource(1, "Bài kho", ("Mục",), ("Chùa mở cửa buổi sáng.",), "diem-den/bai.md")
DU_BAO = PackedSource(2, "Dự báo thời tiết Huế", (), ("Ngày mai 23–27 °C, khả năng mưa 80 %.",), tt.NGUON_SOURCE)


def test_storm_source_shows_the_official_bulletin_sentence_not_the_model_instruction():
    ra = _source_responses((KHO, DU_BAO, BAO_LU))
    assert ra[2].title == tt.TIEU_DE_NGUON_BAO_LU and ra[2].excerpts == [tt.CAU_BAO_LU] and "112" in ra[2].excerpts[0]
    assert all("không trấn an" not in doan for nguon in ra for doan in nguon.excerpts)  # chữ dặn nội bộ không tới giao diện
    # đối chứng: bài kho và nguồn dự báo thường (cùng `source` open-meteo, tiêu đề khác) giữ nguyên đoạn trích
    assert ra[0].excerpts == list(KHO.excerpts) and ra[1].excerpts == list(DU_BAO.excerpts)
    assert BAO_LU.excerpts == (tt.KET_QUA_BAO_LU,)  # nguồn model đã nhận không bị sửa tại chỗ
