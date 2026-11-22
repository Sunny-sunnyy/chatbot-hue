"""Rào "bỏ / thay phải có chỗ neo" (22/11/2026) — 0 USD. Vì sao: trong cuộc đã có lịch, sau lượt "Kể các quán chè ở Huế", tin "Bỏ quán đầu đi rồi viết
lại danh sách" bị lần hiểu ý sửa lịch gán "quán đầu" cho điểm đầu của lịch và lịch bị đổi thật ("Đã bỏ Đại Nội Huế, thêm…" — 5 / 6 lượt thật). Lần hiểu
ý chỉ thấy lịch + đúng câu đó, nên code chỉ nhận hành động bỏ / thay khi câu người dùng có TÊN điểm bị chạm hoặc MỐC của lịch. File này kiểm phần code
(bảng điểm thật, lịch 3 ngày thật, bộ áp thật); model chỉ là đồ giả để DỰNG điều kiện "model đã trả hành động bỏ / thay"."""
import asyncio
import copy

import pytest

from llm import len_ke_hoach as lkh
from llm import sua_lich_v2 as s
from llm.assistant import AnswerTrace
from test_cong_dot_1 import flags_from
from test_sua_lich_v2 import B, _lich

K, _ = _lich()
DAU = sorted(s._vi_tri(K))[0]                 # một điểm đang nằm trong lịch
TEN = B.theo_id[DAU]["ten"]
NGOAI = next(d["ten"] for d in B.diem if d["id"] not in s._vi_tri(K))  # một điểm của bảng chưa có trong lịch


def _bo(ten=TEN):
    return s.HanhDong(loai="bo_diem", ten=ten)


@pytest.mark.parametrize("cau", [
    "Bỏ quán đầu đi rồi viết lại danh sách",           # ca lỗi thật
    "bỏ cái thứ hai đi",
    "Xoá câu vừa rồi đi",
    "Bỏ quán đầu đi, mình đi du lịch tự túc mà",        # "du lịch" không phải mốc của lịch
    "Bỏ cái đó đi rồi kể lịch sử quán thứ hai",          # "lịch sử" cũng không
    "Bỏ món đầu, tra giúp âm lịch hôm nay",
])
def test_remove_without_place_name_or_plan_anchor_is_dropped(cau):
    assert s.loc_bo_thay(B, [_bo()], cau) == ([], [_bo()])
    thay = s.HanhDong(loai="thay_diem", ten=TEN, ten_moi=NGOAI)
    assert s.loc_bo_thay(B, [thay], cau.replace("Bỏ", "Thay").replace("bỏ", "thay")) == ([], [thay])


@pytest.mark.parametrize("cau", [
    f"Bỏ {TEN} đi",
    f"bỏ {TEN.lower()} giúp mình nhé",
    "Bỏ điểm đầu tiên của ngày 2",
    "Bỏ điểm đầu tiên đi",
    "Bỏ cái buổi chiều hôm đầu",
    "Ngày 2 nặng quá, bớt một chỗ đi giúp mình",
    "Bỏ điểm đầu tiên khỏi lịch vì đang có bão",
    "Chuyến đi này bỏ bớt một chỗ cho nhẹ",
])
def test_real_edit_with_a_name_or_a_plan_anchor_is_kept(cau):
    assert s.loc_bo_thay(B, [_bo()], cau) == ([_bo()], [])


def test_a_distinctive_part_of_the_name_counts_as_the_name():
    tu_duc, thien_mu = s.khop_ten(B, "Lăng Tự Đức"), s.khop_ten(B, "Chùa Thiên Mụ")
    assert tu_duc and thien_mu
    assert s._ten_trong_cau(B, tu_duc, "Lăng Tự Đức", "bỏ tự đức đi") and s._ten_trong_cau(B, thien_mu, "Chùa Thiên Mụ", "Thay Thiên Mụ bằng chỗ khác")
    assert not s._ten_trong_cau(B, tu_duc, "Lăng Tự Đức", "bỏ cái lăng đầu đi")  # chữ loại ("lăng") không đủ: danh sách vừa kể cũng có thể toàn lăng
    le_ba_dang = s.khop_ten(B, "Trung tâm Nghệ thuật Lê Bá Đảng")
    assert le_ba_dang and not s._ten_trong_cau(B, le_ba_dang, "Trung tâm Nghệ thuật Lê Bá Đảng", "bỏ quán đầu đi, quán ở trung tâm ấy")  # khúc chung, không tên riêng


def test_a_name_outside_the_table_is_kept_only_when_it_is_a_real_name_in_the_message():
    """Tên model điền không phải điểm của bảng: tên riêng có trong câu ⇒ giữ (bộ áp nói thật "không có trong lịch"); chỉ là chữ trỏ ⇒ bỏ."""
    assert s.khop_ten(B, "Vincom Plaza") is None and s.khop_ten(B, "quán đầu") is None
    assert s.loc_bo_thay(B, [_bo("Vincom Plaza")], "Bỏ Vincom Plaza đi")[1] == []
    assert s.loc_bo_thay(B, [_bo("quán đầu")], "Bỏ quán đầu đi rồi viết lại danh sách")[0] == []
    assert s.loc_bo_thay(B, [_bo(None)], "bỏ đi")[0] == []


def test_other_action_kinds_are_not_touched():
    them = s.HanhDong(loai="them_diem", ten=NGOAI)
    assert s.loc_bo_thay(B, [them, _bo()], "thêm cái đó vào, bỏ cái kia") == ([them], [_bo()])


def _chay(ra, cau, flags=None, goi_y=()):
    flags = flags or flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True)
    k, luu = _lich()

    class Gen:
        async def hieu_sua(self, prompt, call_log, **kw):
            return list(ra)

    tr = AnswerTrace(history=(("Kể các quán chè ở Huế", ""),))
    tr.lich_luu, tr.sua_chon, tr.goi_y_sua = luu, None, goi_y
    truoc = copy.deepcopy(luu)
    return asyncio.run(lkh.hieu_va_ap(cau, Gen(), tr, flags)), tr, luu == truoc


def test_message_about_the_list_just_given_leaves_the_plan_alone_and_goes_the_ordinary_way():
    kq, tr, nguyen = _chay([_bo()], "Bỏ quán đầu đi rồi viết lại danh sách")
    assert kq is None and tr.sua == {"n_hanh_dong": 0} and nguyen          # None ⇒ lõi đi đường hỏi đáp thường; lịch đã lưu không đổi
    assert tr.vet["sua"]["khong_neo"] == 1 and tr.vet["sua"]["hanh_dong"] == [] and tr.vet["sua"]["model_ra"][0]["loai"] == "bo_diem"


def test_same_action_with_the_place_named_is_still_applied():
    kq, tr, _ = _chay([_bo()], f"Bỏ {TEN} đi")
    assert kq is not None and [x["loai"] for x in kq["da_ap"]] == ["bo_diem"] and "khong_neo" not in tr.vet["sua"]


def test_dropped_action_is_said_out_loud_when_the_turn_has_another_edit():
    kq, tr, _ = _chay([_bo(), s.HanhDong(loai="them_diem", ten=NGOAI)], f"Bỏ quán đầu đi, thêm {NGOAI} vào")
    assert kq is not None and "bo_diem" in kq["chua_lam"] and all(x["loai"] != "bo_diem" for x in kq["da_ap"])
    assert any(d["cau"].startswith("Chưa làm: bỏ điểm") for d in s.thay_doi(B, kq))


def test_agreeing_to_the_suggestion_of_the_previous_turn_is_not_guarded():
    """"ok thay đi" sau một câu code gợi ý: tên điểm nằm trong câu gợi ý, không trong câu người dùng ⇒ rào không áp cho lượt này."""
    co = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, sua_lich_them_khong_the=True)
    thay = s.HanhDong(loai="thay_diem", ten=TEN, ten_moi=NGOAI)
    kq, tr, _ = _chay([thay], "ok thay đi", co, goi_y=(f"thay {TEN} bằng {NGOAI}",))
    assert kq is not None and "khong_neo" not in tr.vet["sua"] and "thay_diem" not in kq["chua_lam"]
    kq, tr, _ = _chay([thay], "ok thay đi", co)                              # không có câu gợi ý nào ⇒ rào áp như thường
    assert kq is None and tr.vet["sua"]["khong_neo"] == 1
