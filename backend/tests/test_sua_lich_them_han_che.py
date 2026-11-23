"""Công tắc `sua_lich_them_han_che` (23/11/2026) — 0 USD, không gọi model. Vì sao: đoàn có trẻ nhỏ / người lớn tuổi được xếp nhẹ (một điểm một buổi,
hai điểm một ngày) và lệnh "thêm <điểm>" của họ không bao giờ làm được (0 / 2.376 lệnh trên 72 lịch của đoàn). Chủ dự án chọn: chính họ xin thì "cho
thêm, có dòng báo". Công tắc bật: ngày họ xin thêm được tới ba điểm một ngày, hai điểm một buổi, buổi sáng kết ≤ 13:00, buổi chiều kết ≤ 17:00, giữ bữa
trưa 60 phút; luật khu không nới; lịch xếp ban đầu của đoàn không đổi; đoàn thường không đổi gì. Con số toàn lưới nằm ở runbook 10.2."""
import pytest

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_sua_lich_them_day import NGAY_DIEM, _lenh, _them
from test_sua_lich_v2 import B

T = B.theo_id
TEN = {d["ten"]: i for i, d in T.items()}
DOAN = ({"tre_em": 1}, {"lon_tuoi": True})


def _lich(n, kieu="can_bang", so_thich=(), **doan):
    k = v2.xep_v2(B, v2.ThamSoV2(n, kieu_di=kieu, so_thich=so_thich, **doan))
    return k, s.luu_tu_lich(k, None, None)


def test_flag_defaults_off_and_needs_the_denser_day_switch():
    assert AssistantFlags().sua_lich_them_han_che is False
    with pytest.raises(ValueError, match="sua_lich_them_han_che needs"):
        AssistantFlags(sua_lich_them_han_che=True)


@pytest.mark.parametrize("doan", DOAN)
def test_off_changes_nothing_and_on_changes_nothing_for_regular_groups(doan):
    k, luu = _lich(2, **doan)
    for i, ng, b in _lenh(k):
        assert _them(luu, i, ng, b, them_day=True) == _them(luu, i, ng, b)  # công tắc tắt: đoàn này y như trước
    k, luu = _lich(2)
    for i, ng, b in _lenh(k):
        assert _them(luu, i, ng, b, them_day=True, them_han_che=True) == _them(luu, i, ng, b, them_day=True)  # đoàn thường: công tắc không làm gì


@pytest.mark.parametrize("n,kieu,doan", [(2, "can_bang", DOAN[0]), (3, "kham_pha", DOAN[1]), (1, "nhe_nhang", DOAN[0])])
def test_their_own_add_is_accepted_within_the_group_ceilings_and_reported(n, kieu, doan):
    k, luu = _lich(n, kieu, **doan)
    assert v2.kiem_khung_v2(B, k) == [] and "day_them" not in k  # lịch xếp ban đầu của đoàn không đổi: không ngày nào quá hai điểm
    duoc = 0
    for i, ng, b in _lenh(k):
        kq = _them(luu, i, ng, b, them_day=True, them_han_che=True)
        assert v2.kiem_khung_v2(B, kq["khung"]) == []
        if not kq["da_ap"]:
            assert kq["khung"] == k
            continue
        duoc += 1
        ngay = kq["da_ap"][0]["ngay"]
        d = next(x for x in kq["khung"]["ngay"] if x["ngay"] == ngay)
        sang, chieu = d["buoi"]["sang"], d["buoi"]["chieu"]
        gio = lambda j: tuple(v2.ra_phut(x.strip()) for x in kq["khung"]["gio"][j].split("–"))  # noqa: E731
        assert len(sang) + len(chieu) == v2.HAN_CHE_NGAY_DAY and max(len(sang), len(chieu)) <= v2.HAN_CHE_BUOI_DAY
        assert not sang or gio(sang[-1])[1] <= v2.HAN_CHE_KET_SANG
        assert not chieu or gio(chieu[-1])[1] <= v2.HAN_CHE_KET_CHIEU
        assert not (sang and chieu) or gio(chieu[0])[0] >= gio(sang[-1])[1] + v2.NGHI_TRUA  # bữa trưa còn đủ 60 phút
        assert kq["khung"]["day_them"] == [ngay] and "khu_them" not in kq["khung"]  # luật khu không nới cho đoàn này
        cau = s.thay_doi(B, kq)[0]["cau"]
        assert f"Ngày {ngay} nay dày hơn {v2.MUC_HAN_CHE}: " in cau and "bạn chọn" not in cau
        ghi = [g["cau"] for g in v2.dung_lich(B, kq["khung"], {})["ghi_chu"] if g["ma"] == "day_them"]
        assert len(ghi) == 1 and v2.MUC_HAN_CHE in ghi[0]
        # các ngày khác của lịch giữ mức nhẹ; bỏ chính điểm vừa thêm thì lịch về lại không dấu
        assert all(sum(len(x["buoi"][bb]) for bb in v2.BUOI_NGAY) <= 2 for x in kq["khung"]["ngay"] if x["ngay"] != ngay)
        bo = s.ap(B, kq["luu"], [s.HanhDong(loai="bo_diem", ten=T[i]["ten"])], them_khong_the=True, them_day=True, them_han_che=True)
        assert bo["da_ap"] and "day_them" not in bo["khung"] and v2.kiem_khung_v2(B, bo["khung"]) == []
    assert duoc > 0


def test_a_fourth_stop_on_that_day_is_refused_with_the_group_reason_and_the_browser_case_works():
    """Lượt trình duyệt 23/11/2026: đoàn có trẻ nhỏ "thêm Hổ Quyền" từng ra "lịch đang kín…" trong khi sáng ngày 2 trống từ 9:15."""
    k, luu = _lich(2, tre_em=1)
    kw = dict(them_khong_the=True, them_day=True, them_han_che=True)
    kq = s.ap(B, luu, [s.HanhDong(loai="them_diem", ten="Hổ Quyền")], **kw)
    assert kq["da_ap"] and s.thay_doi(B, kq)[0]["cau"].startswith("Đã thêm Hổ Quyền (ngày ")
    ngay = kq["da_ap"][0]["ngay"]
    lan_hai = [j for j in NGAY_DIEM if j not in s._vi_tri(kq["khung"])]
    tu_choi = 0
    for j in lan_hai:
        k2 = s.ap(B, kq["luu"], [s.HanhDong(loai="them_diem", ten=T[j]["ten"], ngay=ngay)], **kw)
        assert v2.kiem_khung_v2(B, k2["khung"]) == []
        assert not k2["da_ap"] and sum(len(x) for x in next(d for d in k2["khung"]["ngay"] if d["ngay"] == ngay)["buoi"].values()) <= v2.HAN_CHE_NGAY_DAY + 1
        cau = s.thay_doi(B, k2)[0]["cau"]
        assert "đang kín" not in cau and "phạm luật xếp" not in cau
        tu_choi += s.CAU_LY_DO["doan_nhe"] in cau
    assert tu_choi > 0


def test_a_dense_regular_schedule_goes_back_to_the_light_pattern_when_the_group_changes():
    """Dấu "ngày dày" sinh ra lúc lịch còn là của đoàn thường KHÔNG được dùng cho đoàn có trẻ nhỏ: đổi sang "có trẻ nhỏ" thì lịch về mức hai điểm một
    ngày như trước nay, không giữ ngày ba bốn điểm cho đoàn không xin."""
    k, luu = _lich(2)
    kw = dict(them_khong_the=True, them_day=True, them_han_che=True)
    dau = next(kq for i, ng, b in _lenh(k) if ng is None and (kq := _them(luu, i, them_day=True, them_han_che=True))["da_ap"])
    assert dau["khung"].get("day_them")
    kq = s.ap(B, dau["luu"], [s.HanhDong(loai="doi_tham_so", tre_em=1)], **kw)
    assert kq["da_ap"] and v2.kiem_khung_v2(B, kq["khung"]) == [] and "day_them" not in kq["khung"]
    assert all(sum(len(x["buoi"][b]) for b in v2.BUOI_NGAY) <= 2 for x in kq["khung"]["ngay"])
