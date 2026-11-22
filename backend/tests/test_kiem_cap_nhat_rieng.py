"""Phép kiểm "cập nhật riêng giống dựng lại toàn bộ" phải BẮT được từng kiểu lệch — một phép kiểm không bao giờ đỏ thì không kiểm gì.
Điểm dựng tay, không Qdrant, không model; lượt trên collection thật ghi ở report."""
import json

import numpy as np

from ingestion.kiem_cap_nhat_rieng import Diem, so_file, so_voi_dung_lai, so_voi_truoc


def _diem(bai: str, chu: str, nghia=(0.6, 0.8), tu_khoa=((1, 4), (0.5, 0.25))) -> Diem:
    return Diem(payload={"source": bai, "search_text": chu}, nghia=np.asarray(nghia, dtype=np.float32), tu_khoa=tu_khoa)


TRUOC = {"a0": _diem("bai_a.md", "vé 150.000"), "a1": _diem("bai_a.md", "giờ mở cửa"), "b0": _diem("bai_b.md", "bún bò")}
# bài A sửa giá: đoạn a0 đổi chữ và được tính lại; bảng từ vựng đổi ⇒ vector từ khoá của mọi điểm đổi
SAU = {"a0": _diem("bai_a.md", "vé 200.000", nghia=(0.8, 0.6), tu_khoa=((1, 5), (0.4, 0.3))),
       "a1": _diem("bai_a.md", "giờ mở cửa", tu_khoa=((1, 5), (0.5, 0.2))), "b0": _diem("bai_b.md", "bún bò", tu_khoa=((2, 5), (0.5, 0.2)))}


def _lech_nhe(diem: Diem, muc: float) -> Diem:
    return Diem(diem.payload, diem.nghia + np.float32(muc), diem.tu_khoa)


def test_correct_update_passes_both_comparisons_with_batch_level_noise():
    dung_lai = {ma: _lech_nhe(d, 1e-7) for ma, d in SAU.items()}  # dựng lại: lô khác thành phần ⇒ lệch cỡ 1e-7
    loi, so = so_voi_dung_lai(SAU, dung_lai)
    assert loi == [] and so["so_diem_chung"] == 3 and so["vector_nghia_giong_tung_byte"] == 0
    loi, so = so_voi_truoc(TRUOC, SAU, {"bai_a.md"})
    assert loi == [] and so["diem_doi_chu"] == 1 and so["diem_giu_chu"] == 2 and so["diem_giu_chu_ma_vector_tu_khoa_doi"] == 2


def test_leftover_tail_point_and_missing_point_are_reported():
    loi, _ = so_voi_dung_lai({**SAU, "a2": _diem("bai_a.md", "đoạn đuôi cũ")}, SAU)
    assert len(loi) == 1 and "thừa" in loi[0]
    loi, _ = so_voi_dung_lai({ma: d for ma, d in SAU.items() if ma != "b0"}, SAU)
    assert len(loi) == 1 and "thiếu" in loi[0]


def test_payload_keyword_vector_and_meaning_vector_drift_are_each_reported():
    khac_chu = {**SAU, "a0": _diem("bai_a.md", "vé 150.000", nghia=(0.8, 0.6), tu_khoa=((1, 5), (0.4, 0.3)))}
    tu_khoa_cu = {**SAU, "b0": _diem("bai_b.md", "bún bò")}  # quên ghi lại vector từ khoá của bài không sửa
    lech_xa = {**SAU, "a0": _lech_nhe(SAU["a0"], 1e-3)}
    assert ["payload" in so_voi_dung_lai(khac_chu, SAU)[0][0], "từ khoá" in so_voi_dung_lai(tu_khoa_cu, SAU)[0][0],
            "vector nghĩa" in so_voi_dung_lai(lech_xa, SAU)[0][0]] == [True, True, True]


def test_untouched_text_must_keep_its_meaning_vector_byte_for_byte():
    loi, _ = so_voi_truoc(TRUOC, {**SAU, "b0": _lech_nhe(SAU["b0"], 1e-7)}, {"bai_a.md"})
    assert len(loi) == 1 and "không đổi chữ" in loi[0]


def test_changes_outside_the_declared_articles_and_declared_articles_without_changes_are_reported():
    loi, _ = so_voi_truoc(TRUOC, SAU, set())
    assert len(loi) == 1 and "không khai" in loi[0]
    loi, _ = so_voi_truoc(TRUOC, {ma: d for ma, d in SAU.items() if ma != "b0"}, {"bai_a.md"})  # điểm của bài B bị xoá oan
    assert len(loi) == 1 and "không khai" in loi[0]
    loi, _ = so_voi_truoc(TRUOC, SAU, {"bai_a.md", "bai_c.md"})
    assert len(loi) == 1 and "không điểm nào" in loi[0]


def test_files_only_the_collection_name_may_differ(tmp_path):
    def ghi(ten: str, noi_dung) -> object:
        path = tmp_path / ten
        path.write_text(noi_dung if isinstance(noi_dung, str) else json.dumps(noi_dung), encoding="utf-8")
        return path
    tk = ghi("tk.json", "{}")
    ban_ghi = {"collection_name": "thu_sau", "corpus": {"chunk_count": 3}}
    a, b = ghi("a.json", ban_ghi), ghi("b.json", {**ban_ghi, "collection_name": "thu_dung_lai"})
    assert so_file(tk, ghi("tk2.json", "{}"), a, b) == []
    loi = so_file(tk, ghi("tk3.json", '{"idf": [1]}'), a, ghi("c.json", {**ban_ghi, "corpus": {"chunk_count": 4}}))
    assert len(loi) == 2 and "thống kê" in loi[0] and "corpus" in loi[1]
