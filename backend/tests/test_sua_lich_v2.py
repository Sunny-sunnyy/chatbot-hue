"""Sửa lịch bằng lời trên lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-sua-lich-v2-plan.md`) — phần code (0 USD): bộ xếp giữ chỗ / loại điểm,
áp hành động, khối "Đã đổi / Không đổi được", từ dò câu sửa, trạng thái lưu. Phép thử mọi tổ hợp ở `data/len_ke_hoach_v2_2026-11-13/tools/do_sua_lich_v2.py`."""
import datetime as dt

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_cong_dot_1 import flags_from

V2 = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True)
B = V2.bang_lich_v2


def _lich(n=3, kieu="can_bang", so_thich=("di_tich",), ngay=None):
    k = v2.xep_v2(B, v2.ThamSoV2(n, kieu_di=kieu, so_thich=so_thich), ngay_bat_dau=ngay)
    return k, s.luu_tu_lich(k, None if ngay is None else ngay.isoformat(), None)


def test_default_scheduler_unchanged_and_keep_exclude_work():
    k, _ = _lich()
    assert v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)), giu=None, loai=frozenset()) == k
    vt = s._vi_tri(k)
    x = sorted(vt)[0]
    k2 = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",)), giu={j: v for j, v in vt.items() if j != x}, loai=frozenset({x}))
    tat = {j for ng in k2["ngay"] for b in v2.BUOI for j in ng["buoi"][b]}
    assert x not in tat and all(s._vi_tri(k2)[j] == v for j, v in vt.items() if j != x) and v2.kiem_khung_v2(B, k2) == []


def test_remove_replace_move_and_card():
    k, luu = _lich()
    vt = s._vi_tri(k)
    x = sorted(vt)[0]
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=B.theo_id[x]["ten"])])
    assert kq["da_ap"] == [{"loai": "bo_diem", "diem": x}] and x in kq["luu"]["loai"] and v2.kiem_khung_v2(B, kq["khung"]) == []
    assert s.thay_doi(B, kq)[0] == {"cau": f"Đã bỏ {B.theo_id[x]['ten']}.", "duoc": True}
    the = s.ap(B, luu, [s.HanhDong(loai="thay_diem", ten=x)])  # không nói thay bằng gì ⇒ thẻ, khung không đổi
    assert the["the"]["cu"] == x and the["khung"] == k and the["the"]["lua_chon"][-1]["gia_tri"] == "bo"
    moi = the["the"]["lua_chon"][0]["gia_tri"]
    bam = s.ap(B, luu, [], sua_chon={"cu": x, "moi": moi})  # bấm nút ⇒ đúng điểm đã chọn vào đúng chỗ cũ
    assert s._vi_tri(bam["khung"])[moi] == vt[x] and x in bam["luu"]["loai"]
    dich = "chieu" if vt[x][1] == "sang" else "sang"
    dd = s.ap(B, luu, [s.HanhDong(loai="doi_buoi", ten=x, buoi=dich)])
    assert (dd["da_ap"] and s._vi_tri(dd["khung"])[x][1] == dich) or dd["khong_doi"]


def test_unknown_names_and_limits_are_reported_not_guessed():
    k, luu = _lich()
    kq = s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten="Tháp Eiffel"), s.HanhDong(loai="them_diem", ten="x"), s.HanhDong(loai="doi_so_ngay", so_ngay=2)])
    assert kq["khong_doi"][0]["ma_luat"] == "ngoai_bang" and kq["chua_lam"] == ["doi_so_ngay"] and kq["khung"] == k
    dong = s.thay_doi(B, kq)
    assert all(not d["duoc"] for d in dong) and dong[-1]["cau"].startswith("Chưa làm")


def test_change_days_keeps_points_that_still_fit():
    k, luu = _lich(n=3)
    kq = s.ap(B, luu, [s.HanhDong(loai="doi_so_ngay", so_ngay=2)])
    assert len(kq["khung"]["ngay"]) == 2 and kq["doi_truong"] == [("so_ngay", 3, 2)]
    giu = {j: v for j, v in s._vi_tri(k).items() if v[0] <= 2}
    assert all(s._vi_tri(kq["khung"]).get(j) == v for j, v in giu.items()) or v2.kiem_khung_v2(B, kq["khung"]) == []


def test_edit_words_gate_and_intent_message():
    assert s.co_tu_sua("Bỏ lăng Tự Đức đi") and s.co_tu_sua("Ngày 2 cho Bao Vinh sang buổi chiều") and s.co_tu_sua("Mình không muốn đi chùa nữa")
    assert not s.co_tu_sua("Lăng Tự Đức mở cửa mấy giờ?") and not s.co_tu_sua("Cảm ơn nhé") and not s.co_tu_sua("Bị cướp điện thoại thì làm sao")
    k, luu = _lich(n=1)
    tin = s.tin_nhan_hieu(B, luu, "  bỏ điểm đầu  ")
    assert tin.endswith("Câu người dùng: bỏ điểm đầu") and "Ngày 1" in tin
    assert s.khop_ten(B, "Đại Nội Huế") == "dai_noi" and s.khop_ten(B, "đại nội") == "dai_noi" and s.khop_ten(B, "Đại") is None


def test_flag_needs_v2():
    import pytest
    with pytest.raises(ValueError):
        AssistantFlags(sua_lich_v2=True)
