"""Rào đổi số ngày sau lần hiểu ý sửa lịch (`sua_lich_v2.so_ngay_co_trong_cau`): số trong một ngày tháng không thành số ngày (C 15/11)."""
import pytest

from llm import sua_lich_v2 as sl


@pytest.mark.parametrize("cau, so_ngay, hien_tai, duoc", [
    ("Mình đi từ ngày 20/12 nhé", 1, 3, False),        # lỗi thật 15/11: 20/12 ⇒ "1 ngày"
    ("Đi từ 20/12 nhé", 2, 3, False),
    ("Mình đi từ ngày 20/12 nhé", None, 3, False),     # đổi số ngày không kèm số
    ("Đổi sang ngày 1/1 và cho khách sạn 5 sao", 1, 3, False),
    ("Bỏ đồi Vọng Cảnh, thêm Hổ Quyền, với lại rút xuống 2 ngày thôi.", 2, 3, True),  # Q3 đã thấy S03
    ("Giờ rút xuống còn 2 ngày giúp mình.", 2, 3, True),
    ("Cho mình đi hai ngày thôi", 2, 3, True),
    ("Lịch 4N3Đ nhé", 4, 3, True),
    ("Thêm một ngày nữa", 4, 3, True),                 # tương đối
    ("Thêm một ngày nữa", 1, 3, False),                # "một ngày" sau "thêm" không phải tổng
    ("Bớt 1 ngày", 2, 3, True),
    ("Chiều ngày 2 đổi Đại Nội sang Bảo tàng", 2, 3, False),  # "ngày 2" là ngày thứ mấy, không phải số ngày
    ("Đi từ thứ hai ngày 20/12", 2, 3, False),          # review E m-2: "thứ hai" không phải "hai ngày"
    ("Mình đi thứ ba ngày 18/11", 3, 4, False),
    ("Đi 2 hôm thôi", 2, 3, True),                      # review E m-3
    ("Bỏ ngày cuối đi", 2, 3, True),
    ("Bỏ ngày 3 nhé", 2, 3, True),
    ("Bỏ ngày 2 nhé", 2, 3, False),                     # bỏ ngày giữa không phải bớt ngày cuối
])
def test_day_count_needs_a_number_of_days_in_the_text(cau, so_ngay, hien_tai, duoc):
    assert sl.so_ngay_co_trong_cau(cau, so_ngay, hien_tai) is duoc


def test_filter_keeps_other_actions():
    luu = {"khung": {"tham_so": {"so_ngay": 3}}}
    hd = [sl.HanhDong(loai="doi_so_ngay", so_ngay=1), sl.HanhDong(loai="bo_diem", ten="Đại Nội")]
    giu, bi_chan = sl.loc_hanh_dong(hd, "Bỏ Đại Nội, mình đi từ ngày 20/12", luu)
    assert [h.loai for h in giu] == ["bo_diem"] and bi_chan == 1


def test_blocked_day_count_stays_an_edit_turn_with_not_done_line(monkeypatch):
    """Review E M-1: rào bỏ hết hành động ⇒ vẫn là lượt sửa (lịch không đổi) + dòng "Chưa làm: đổi số ngày", không rơi về đường trả lời thường."""
    import asyncio
    from test_len_ke_hoach_v2 import V2
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    k = v2.xep_v2(V2.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",)))
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(k, None, None); tr.sua_chon = None

    class Gen:
        async def hieu_sua(self, prompt, call_log):
            return [sl.HanhDong(loai="doi_so_ngay", so_ngay=1)]
    kq = asyncio.run(lkh.hieu_va_ap("Mình đi từ ngày 20/12 nhé", Gen(), tr, V2))
    assert kq is not None and kq["khung"]["tham_so"]["so_ngay"] == 3
    assert [d["cau"] for d in sl.thay_doi(V2.bang_lich_v2, kq)] == ["Chưa làm: đổi số ngày — bạn nhắn tiếp nhé."]


# ---------- (C 17/11) ý đổi chỗ ngày khi model ĐÃ nhận câu là câu sửa (tự thử 16/11: "Chưa làm: đổi số ngày" sai việc) ----------

@pytest.mark.parametrize("cau, la", [
    ("Đổi chỗ ngày 1 với ngày 2", True),                     # tự thử 16/11 (A, C, E)
    ("Hoán đổi ngày 2 và ngày 3 giúp mình", True),
    ("Đảo thứ tự hai ngày nhé", True),
    ("Ngày 1 và ngày 3 đổi chỗ cho nhau", True),
    ("Gộp ngày 2 với ngày 3", True),
    ("Đổi chỗ ở sang khách sạn khác ngày 2 và ngày 3", False),  # "chỗ ở" = lưu trú
    ("Đổi ngày đi sang 20/12", False),                       # hành động có sẵn (đổi ngày đi)
    ("Dời Đại Nội từ ngày 1 sang ngày 2", False),            # dời buổi — làm được
    ("Ngày 2 nên ăn gì ở đâu?", False),
])
def test_day_reorder_requests_are_recognised(cau, la):
    assert sl.la_viec_ngay_chua_lam(cau) is la


def _hieu(cau, ra):
    import asyncio
    from test_len_ke_hoach_v2 import V2
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    k = v2.xep_v2(V2.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",)))
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(k, None, None); tr.sua_chon = None

    class Gen:
        async def hieu_sua(self, prompt, call_log):
            return list(ra)
    return k, asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, V2))


def test_blocked_day_count_on_a_swap_request_says_the_right_thing():
    k, kq = _hieu("Đổi chỗ ngày 1 với ngày 2", [sl.HanhDong(loai="doi_so_ngay")])  # model đoán "đổi số ngày" ⇒ rào chặn
    from test_len_ke_hoach_v2 import V2
    assert kq["khung"] == k and [d["cau"] for d in sl.thay_doi(V2.bang_lich_v2, kq)] == [sl.CAU_VIEC_KHAC]


def test_swap_next_to_a_doable_action_is_reported_not_dropped():
    from test_len_ke_hoach_v2 import V2
    k, kq = _hieu("Đổi chỗ ngày 1 với ngày 2, và đổi sang kiểu đi nhẹ nhàng", [sl.HanhDong(loai="doi_tham_so", kieu_di="nhe_nhang")])
    cau = [d["cau"] for d in sl.thay_doi(V2.bang_lich_v2, kq)]
    assert cau[-1] == sl.CAU_VIEC_KHAC and any(c.startswith("Đã đổi") for c in cau)


def test_model_empty_stays_normal_path():  # lưới ở đường "model trả rỗng" đã thử và bỏ (bộ kề bên E 10 / 20) ⇒ việc của `chua_ho_tro`
    _, kq = _hieu("Đổi chỗ ngày 1 với ngày 2", [])
    assert kq is None
