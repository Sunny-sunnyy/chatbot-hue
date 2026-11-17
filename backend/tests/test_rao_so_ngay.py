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


# ---------- (C 17/11) lưới sau hiểu ý: câu sửa mà model trả rỗng (tự thử 16/11: lịch chữ giả, "Chưa làm: đổi số ngày" sai việc) ----------

@pytest.mark.parametrize("cau, la", [
    ("Đổi chỗ ngày 1 với ngày 2", True),                     # tự thử 16/11 (A, C, E)
    ("Hoán đổi ngày 2 và ngày 3 giúp mình", True),
    ("Đảo thứ tự hai ngày nhé", True),
    ("Ngày 1 và ngày 3 đổi chỗ cho nhau", True),
    ("Gộp ngày 2 với ngày 3", True),
    ("Đổi chỗ ở sang khách sạn khác ngày 2 và ngày 3", False),  # "chỗ ở" = lưu trú
    ("Đổi ngày đi sang 20/12", False),                       # hành động có sẵn (đổi ngày đi)
    ("Đảo Cồn Hến có gì ăn?", False),
    ("Ngày 2 nên ăn gì ở đâu?", False),                      # câu xen giữa
    ("Ngày 1 và ngày 2 trời có mưa không?", False),
    ("Để ngày 2 sang trước, ngày 1 đi sau", True),           # dạng rộng: hai mốc ngày + từ chỉ thứ tự
    ("Lùi cả lịch muộn lại một chút", True),                 # dời giờ cả lịch
    ("Cho nghỉ ngơi buổi trưa lâu hơn ở các ngày", True),    # dời / thêm giờ nghỉ cả lịch ⇒ chưa làm được
])
def test_day_reorder_requests_are_recognised(cau, la):
    assert sl.la_viec_ngay_chua_lam(cau) is la


def test_loose_forms_only_when_model_found_nothing():
    # câu sửa làm được ("dời … từ ngày 1 sang ngày 2" = dời buổi) không bị thêm dòng "Chưa làm" khi model đã ra hành động (dạng chặt)
    assert sl.la_viec_ngay_chua_lam("Dời Đại Nội từ ngày 1 sang ngày 2", rong=False) is False
    assert sl.la_viec_ngay_chua_lam("Đổi chỗ ngày 1 với ngày 2, và bỏ điểm cuối ngày 3", rong=False) is True


@pytest.mark.parametrize("cau, hien_tai, la", [
    ("đổi thành 2 ngày", 2, True),                           # tự thử 16/11 (C: 5 ngày, E: 2 ngày)
    ("Làm lại lịch 5 ngày giúp mình", 5, True),
    ("đổi thành 3 ngày", 2, False),                          # số khác ⇒ việc của model + rào số ngày
    ("Còn 2 ngày nữa là mình đi rồi", 2, False),             # không có động từ sửa
    ("Đi 2 ngày có đủ không?", 2, False),
    ("Mình đi 3 ngày thôi nhé", 3, True),                    # câu dặn ngắn
    ("Trong 3 ngày đó mình muốn ăn bún bò", 3, False),      # không phải câu dặn
])
def test_same_day_count_request(cau, hien_tai, la):
    assert sl.so_ngay_dang_dung(cau, hien_tai) is la


@pytest.mark.parametrize("cau, ra, cau_dong", [
    ("Đổi chỗ ngày 1 với ngày 2", [], [sl.CAU_VIEC_KHAC]),                                        # model rỗng ⇒ vẫn lượt sửa
    ("Đổi chỗ ngày 1 với ngày 2", [sl.HanhDong(loai="doi_so_ngay")], [sl.CAU_VIEC_KHAC]),         # model đoán "đổi số ngày" ⇒ câu đúng việc
    ("đổi thành 3 ngày", [], ["Lịch đang đúng như vậy rồi (số ngày: 3 ngày)."]),
])
def test_net_keeps_edit_turn_and_lich_unchanged(cau, ra, cau_dong):
    import asyncio
    from test_len_ke_hoach_v2 import V2
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    k = v2.xep_v2(V2.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",)))
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(k, None, None); tr.sua_chon = None

    class Gen:
        async def hieu_sua(self, prompt, call_log):
            return list(ra)
    kq = asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, V2))
    assert kq is not None and kq["khung"] == k and kq["da_ap"] == []
    assert [d["cau"] for d in sl.thay_doi(V2.bang_lich_v2, kq)] == cau_dong


def test_plain_question_in_a_planned_conversation_stays_normal():
    import asyncio
    from test_len_ke_hoach_v2 import V2
    from llm import len_ke_hoach as lkh, lich_trinh_v2 as v2
    from llm.assistant import AnswerTrace
    k = v2.xep_v2(V2.bang_lich_v2, v2.ThamSoV2(3, so_thich=("di_tich",)))
    tr = AnswerTrace(); tr.lich_luu = sl.luu_tu_lich(k, None, None); tr.sua_chon = None

    class Gen:
        async def hieu_sua(self, prompt, call_log):
            return []
    assert asyncio.run(lkh.hieu_va_ap("Ngày 2 nên ăn gì ở đâu?", Gen(), tr, V2)) is None
