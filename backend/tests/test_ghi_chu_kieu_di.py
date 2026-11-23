"""Ghi chú "chưa chọn kiểu đi nên xếp mức cân bằng" không được hiện cho đoàn có trẻ nhỏ / người lớn tuổi (23/11/2026) — 0 USD, bảng điểm thật qua `flags_from`.

Lỗi đã thấy trên trình duyệt: đoàn hạn chế để trống kiểu đi (mặc định của biểu mẫu) ⇒ hai dòng ghi chú liền nhau nói ngược nhau — "xếp mức cân bằng" rồi
"xếp nhẹ nhàng". Với đoàn hạn chế kiểu đi không vào bộ xếp (luôn nhẹ nhàng) nên câu đầu là sai.
"""
from llm import lich_trinh_v2 as v2
from test_cong_dot_1 import flags_from

B = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True).bang_lich_v2


def _ma_ghi_chu(**ts):
    khung = v2.xep_v2(B, v2.ThamSoV2(2, **ts))
    return khung["gia_dinh"], [g["cau"] for g in v2.dung_lich(B, khung, {})["ghi_chu"]]


def test_restricted_group_without_a_chosen_pace_gets_only_the_gentle_note():
    for doan in (dict(tre_em=1), dict(lon_tuoi=True)):
        gia_dinh, cau = _ma_ghi_chu(**doan)
        assert "han_che" in gia_dinh and "kieu_di" not in gia_dinh
        assert v2.CAU_GHI_CHU["han_che"] in cau and v2.CAU_GHI_CHU["kieu_di"] not in cau


def test_other_groups_keep_the_default_pace_note_and_a_chosen_pace_has_none():
    gia_dinh, cau = _ma_ghi_chu()
    assert "kieu_di" in gia_dinh and v2.CAU_GHI_CHU["kieu_di"] in cau
    assert "kieu_di" not in _ma_ghi_chu(kieu_di="kham_pha")[0]


def test_card_header_states_the_gentle_pace_for_restricted_groups_whatever_was_chosen():
    """Đầu thẻ ("Mình hiểu…", ô "Thời gian") ghi mức lịch THẬT SỰ dùng; tham số lưu trong khung giữ nguyên lựa chọn của người dùng."""
    for chon in (None, "can_bang", "kham_pha"):
        khung = v2.xep_v2(B, v2.ThamSoV2(2, tre_em=1, kieu_di=chon))
        lich = v2.dung_lich(B, khung, {})
        assert "đi nhẹ nhàng" in lich["minh_hieu"] and lich["tham_so"]["kieu_di"] == "nhe_nhang"
        assert khung["tham_so"]["kieu_di"] == (chon or v2.KIEU_DI_MAC_DINH)
    lich = v2.dung_lich(B, v2.xep_v2(B, v2.ThamSoV2(2)), {})  # đoàn thường: như cũ
    assert "đi cân bằng" in lich["minh_hieu"] and lich["tham_so"]["kieu_di"] == "can_bang"
