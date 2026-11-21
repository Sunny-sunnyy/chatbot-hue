"""Cờ `sua_lich_doi_cho_ngay` (20/11) — "đổi chỗ ngày 1 với ngày 2": hàm đọc câu (danh sách cho phép) + hàm hoán đổi hai ngày qua đường xếp-rồi-kiểm.
Hàm thuần trên bảng lịch thật (private, như `test_sua_lich_v2`); không model, không mạng. KHÔNG phải bằng chứng trên lượt thật qua giao diện."""
import copy

import pytest

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from test_cong_dot_1 import flags_from

B = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True).bang_lich_v2
K3 = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)))
LUU3 = s.luu_tu_lich(K3, None, None)


@pytest.mark.parametrize("cau, so_ngay, mong", [
    ("đổi chỗ ngày 1 với ngày 2", 3, (1, 2)),
    ("Đổi chỗ ngày 3 và ngày 1 giúp mình nhé", 3, (1, 3)),
    ("hoán đổi ngày đầu với ngày cuối", 4, (1, 4)),
    ("đảo ngày 2 với ngày thứ ba cho mình", 3, (2, 3)),
    ("đổi chỗ hai ngày cho nhau", 2, (1, 2)),
    ("đổi chỗ ngày 1 với ngày 2 được không", 3, (1, 2)),   # "được không" cuối câu là lời nhờ, không phải phủ định
])
def test_reads_a_plain_request_to_swap_two_days(cau, so_ngay, mong):
    assert s.cap_ngay_doi_cho(cau, so_ngay) == mong


@pytest.mark.parametrize("cau, so_ngay", [
    ("đổi chỗ Đại Nội ngày 1 với lăng Tự Đức ngày 2", 3),     # đổi chỗ hai ĐIỂM
    ("đổi chỗ ngày 1 với ngày 2 và bỏ chùa Thiên Mụ", 3),      # kèm ý khác
    ("gộp ngày 1 với ngày 2", 3),                              # gộp, không phải đổi chỗ
    ("đổi chỗ buổi sáng ngày 1 với buổi chiều ngày 2", 3),     # đổi BUỔI
    ("đổi chỗ ngày 1 với ngày 4", 3),                          # ngày ngoài lịch
    ("đổi chỗ ngày 2 với ngày 2", 3),
    ("đổi chỗ hai ngày cho nhau", 3),                          # lịch 3 ngày: không biết hai ngày nào
    ("đổi ngày đi sang ngày 2 tháng 12", 3),
    ("đổi chỗ ở ngày 1 sang gần sông", 3),
    ("ngày 1 với ngày 2 ngày nào đi nhiều hơn", 3),
    ("không đổi chỗ ngày 1 với ngày 2", 3),                    # review E 20/11: câu PHỦ ĐỊNH không phải lệnh đổi
    ("đừng đổi chỗ ngày 1 với ngày 2 nhé", 3),
    ("", 3),
])
def test_anything_else_is_left_to_the_fixed_not_done_line(cau, so_ngay):
    assert s.cap_ngay_doi_cho(cau, so_ngay) is None


def test_swap_puts_each_daytime_stop_on_the_other_day_same_slot_and_twice_restores():
    kq = s.doi_cho_ngay(B, LUU3, 1, 3)
    assert [a["loai"] for a in kq["da_ap"]] == ["doi_cho_ngay"] and not kq["khong_doi"] and not v2.kiem_khung_v2(B, kq["khung"])
    cu, moi = s._vi_tri(K3), s._vi_tri(kq["khung"])
    doi = {1: 3, 3: 1}
    assert moi == {j: (doi.get(n, n), b) for j, (n, b) in cu.items()}
    assert s._vi_tri(LUU3["khung"]) == cu  # bản lưu truyền vào không bị sửa tại chỗ
    lai = s.doi_cho_ngay(B, kq["luu"], 1, 3)
    assert s._vi_tri(lai["khung"]) == cu
    dong = s.thay_doi(B, kq)
    assert dong == [{"cau": "Đã đổi chỗ các điểm buổi sáng và chiều của ngày 1 với ngày 3; hoạt động buổi tối giữ theo từng ngày.", "duoc": True}]
    toi = lambda k: {ng["ngay"]: ng["buoi"]["toi"] for ng in k["ngay"]}  # noqa: E731
    assert toi(kq["khung"]) == toi(K3)  # buổi tối không đi theo phần đổi chỗ ⇒ không có dòng "xếp lại thêm"


def test_blocked_swap_keeps_the_saved_plan_and_says_why(monkeypatch):
    monkeypatch.setattr(v2, "kiem_khung_v2", lambda bang, khung: ["cum_xa"])  # dựng điều kiện: bộ kiểm báo điểm khu xa rơi vào ngày 1
    kq = s.doi_cho_ngay(B, LUU3, 1, 2)
    assert not kq["da_ap"] and kq["khung"] == LUU3["khung"] and kq["luu"]["khung"] == LUU3["khung"]
    assert s.thay_doi(B, kq) == [{"cau": "Chưa đổi chỗ ngày 1 với ngày 2 được vì ngày 1 sẽ có điểm ở khu xa trung tâm, mà lịch không xếp khu xa vào ngày đầu "
                                         "— lịch giữ nguyên.", "duoc": False}]


def test_real_blocked_case_far_cluster_on_day_one():
    """Ca thật (không dựng): lịch 3 ngày mà đổi ngày 1 với ngày có điểm khu xa ⇒ bị chặn, lịch giữ nguyên."""
    for kieu, st in (("kham_pha", ()), ("can_bang", ()), ("kham_pha", ("thien_nhien",)), ("can_bang", ("thien_nhien",))):
        k = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di=kieu, so_thich=st))
        luu = s.luu_tu_lich(k, None, None)
        for b in (2, 3):
            kq = s.doi_cho_ngay(B, luu, 1, b)
            if not kq["da_ap"]:
                assert kq["khong_doi"][0]["ly_do"] == "xa_ngay_dau" and kq["khung"] == luu["khung"]
                return
    pytest.skip("bảng lịch hiện tại không còn ca khu xa bị chặn trong bốn kiểu lịch thử")


def test_extra_rearrangement_by_the_scheduler_is_reported():
    kq = s.doi_cho_ngay(B, LUU3, 1, 2)
    kq["da_ap"][0]["xep_them"] = {"doi_cho": [], "ra": [], "vao": [next(iter(s._vi_tri(K3)))]}
    assert any(d["cau"].startswith("Ngoài phần đổi chỗ, lịch xếp lại thêm: thêm ") for d in s.thay_doi(B, kq))


# ---------- Nối vào luồng sửa lịch (`len_ke_hoach.hieu_va_ap`): model giả chỉ để DỰNG điều kiện "model đã nhận là câu sửa" ----------
def _luot_sua(cau, ra, **co):
    import asyncio

    from llm import len_ke_hoach as lkh
    from llm.assistant import AnswerTrace
    f = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_chua_ho_tro=True, **co)
    k = v2.xep_v2(f.bang_lich_v2, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)))
    tr = AnswerTrace()
    tr.lich_luu, tr.sua_chon = s.luu_tu_lich(k, None, None), None

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            return list(ra)
    return f, k, asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, f))


CHT = [s.HanhDongCHT(loai="chua_ho_tro")]


def test_flag_on_swaps_for_a_plain_request_and_flag_off_keeps_the_not_done_line():
    f, k, kq = _luot_sua("Đổi chỗ ngày 1 với ngày 3", CHT, sua_lich_doi_cho_ngay=True)
    cau = [d["cau"] for d in s.thay_doi(f.bang_lich_v2, kq)]
    assert cau[0].startswith("Đã đổi chỗ các điểm buổi sáng và chiều của ngày 1 với ngày 3") and s.CAU_VIEC_KHAC not in cau
    assert s._vi_tri(kq["khung"]) != s._vi_tri(k) and not v2.kiem_khung_v2(f.bang_lich_v2, kq["khung"])
    f, k, kq = _luot_sua("Đổi chỗ ngày 1 với ngày 3", CHT)  # cờ tắt ⇒ đúng như hôm nay
    assert kq["khung"] == k and [d["cau"] for d in s.thay_doi(f.bang_lich_v2, kq)] == [s.CAU_VIEC_KHAC]


@pytest.mark.parametrize("cau, ra", [
    ("Gộp ngày 1 với ngày 2", CHT),                                                                       # không phải đổi chỗ ⇒ "Chưa làm"
    ("Đổi chỗ ngày 1 với ngày 2, và đổi sang kiểu đi nhẹ nhàng", [s.HanhDong(loai="doi_tham_so", kieu_di="nhe_nhang")]),  # lượt có ý khác đã áp
])
def test_flag_on_leaves_other_day_requests_and_mixed_turns_as_before(cau, ra):
    f, k, kq = _luot_sua(cau, ra, sua_lich_doi_cho_ngay=True)
    cau_bao = [d["cau"] for d in s.thay_doi(f.bang_lich_v2, kq)]
    assert s.CAU_VIEC_KHAC in cau_bao and not any(c.startswith("Đã đổi chỗ các điểm") for c in cau_bao)
