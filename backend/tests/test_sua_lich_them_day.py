"""Cờ `sua_lich_them_day` (23/11/2026) — 0 USD, không gọi model. Vì sao: trên lịch vừa xếp, lệnh "thêm X" không bao giờ làm được (liệt kê 108 lịch mẫu:
0 / 14.725) vì lịch đã đầy quỹ nhịp đi; chủ dự án chọn "cho ngày dày thêm" — người dùng XIN thêm thì lịch nhận, vượt nhịp đi đã chọn, kèm dòng báo. Cờ
bật: lệnh thêm chỉ vướng NHỊP ĐI (số điểm một buổi, quỹ phút) được áp; ngày đó dài ra (buổi chiều lùi theo buổi sáng, bữa trưa 60 phút, sáng kết ≤ 13:30,
chiều kết ≤ 18:00); mọi luật khác giữ nguyên; đoàn có trẻ nhỏ / người lớn tuổi không đổi gì. File kiểm phần code trên bảng điểm thật và bộ áp thật; con số
toàn lưới (108 lịch) và năm lệnh đã ghi của người dùng mô phỏng nằm ở report của nhánh."""
import copy

import pytest

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_sua_lich_v2 import B, _lich

T = B.theo_id
NGAY_DIEM = [i for i, d in T.items() if set(d["buoi"]) & set(v2.BUOI_NGAY)]
NHIP = {"qua_day_buoi", "vuot_quy"}


def _them(luu, i, ngay=None, buoi=None, **kw):
    return s.ap(B, luu, [s.HanhDong(loai="them_diem", ten=T[i]["ten"], ngay=ngay, buoi=buoi)], them_khong_the=True, **kw)


def _lenh(k):
    """Mọi lệnh "thêm X" + "thêm X vào <buổi> ngày <n>" trên một lịch."""
    trong = set(s._vi_tri(k)) | {j for ng in k["ngay"] for j in ng["buoi"]["toi"]}
    for i in NGAY_DIEM:
        if i in trong:
            continue
        yield i, None, None
        for ng in k["ngay"]:
            for b in v2.BUOI_NGAY:
                if b in T[i]["buoi"]:
                    yield i, ng["ngay"], b


def _phut(khung, j):
    return tuple(v2.ra_phut(x.strip()) for x in khung["gio"][j].split("–"))


def _gio_di_duoc(khung, ngay):
    """Kiểm ĐỘC LẬP với `kiem_khung_v2`: giờ của ngày đã dày đọc từ `khung["gio"]` phải đi được thật."""
    ng = next(x for x in khung["ngay"] if x["ngay"] == ngay)
    ket_sang = None
    for b in v2.BUOI_NGAY:
        truoc = None
        for j in ng["buoi"][b]:
            bd, kt = _phut(khung, j)
            assert kt - bd == v2.PHUT[T[j]["thoi_luong"]]
            assert not T[j].get("gio_mo") or any(v2.ra_phut(o) <= bd and kt <= v2.ra_phut(c) for o, c in T[j]["gio_mo"]), (j, khung["gio"][j])
            if truoc is not None:
                assert bd >= truoc[1] + v2._phut_di(T[truoc[0]], T[j])  # nối giờ + phút đi; khu không kề trong một buổi ⇒ None ⇒ lỗi ngay
            elif b == "chieu" and ket_sang is not None:
                assert bd >= ket_sang + v2.NGHI_TRUA  # bữa trưa còn đủ
            truoc = (j, kt)
        assert len(ng["buoi"][b]) <= v2.TOI_DA_BUOI + 1
        if b == "sang" and truoc:
            ket_sang = truoc[1]
            assert ket_sang <= v2.GIO_KET_SANG_DAY
        if b == "chieu" and truoc:
            assert truoc[1] <= v2.GIO_KET_CHIEU_DAY


def test_flag_defaults_off_and_needs_the_no_replace_flag():
    assert AssistantFlags().sua_lich_them_day is False
    with pytest.raises(ValueError, match="sua_lich_them_day needs"):
        AssistantFlags(sua_lich_them_day=True)


def test_flag_off_is_the_old_behaviour_and_unmarked_schedules_are_untouched():
    """Cờ tắt ⇒ gói trả về y như lời gọi không có tham số mới; khung không có dấu ⇒ `_xep` trả đúng khung của `xep_v2`, không khoá `day_them`."""
    k, luu = _lich(2)
    for i, ng, b in _lenh(k):
        assert _them(luu, i, ng, b) == _them(luu, i, ng, b, them_day=False)
    vt = s._vi_tri(k)
    k2 = s._xep(B, luu, s._ts(k["tham_so"]), vt, [])
    assert "day_them" not in k2 and k2 == v2.xep_v2(B, v2.ThamSoV2(2, kieu_di="can_bang", so_thich=("di_tich",)), giu=vt, loai=frozenset())


@pytest.mark.parametrize("n,kieu", [(1, "nhe_nhang"), (2, "can_bang"), (2, "kham_pha")])
def test_add_beyond_pace_is_applied_marked_reported_and_still_walkable(n, kieu):
    """Quét mọi lệnh thêm trên một lịch vừa xếp. Cờ bật: có lệnh làm được (trước: 0); mỗi lệnh làm được ⇒ không mất điểm nào, ngày được ghi dấu, khung đúng
    luật theo `kiem_khung_v2`, BỎ dấu đi thì chỉ còn đúng hai mã nhịp đi, giờ đi được thật (phép kiểm độc lập), dòng báo nói ngày dày hơn nhịp đã chọn.
    Lệnh không làm được ⇒ lịch giữ nguyên; cách "thêm thẳng" được gợi ý nào cũng làm được khi nhắn đúng câu đó."""
    k, luu = _lich(n, kieu)
    truoc = set(s._vi_tri(k))
    n_duoc = n_goi_y = 0
    for i, ng, b in _lenh(k):
        assert not _them(luu, i, ng, b)["da_ap"]  # lịch vừa xếp: không lệnh thêm nào làm được khi cờ tắt
        kq = _them(luu, i, ng, b, them_day=True)
        if not kq["da_ap"]:
            assert kq["khung"] == k and "day_them" not in kq["luu"]
            for g in kq["khong_doi"][0].get("cach") or ():
                if g["thay"] is None:  # gợi ý "thêm vào buổi khác, không mất điểm nào"
                    n_goi_y += 1
                    assert g.get("day") and _them(luu, i, g["ngay"], g["buoi"], them_day=True)["da_ap"]
                    assert "(ngày đó sẽ dày hơn nhịp bạn chọn)" in s.thay_doi(B, kq)[0]["cau"]
            continue
        n_duoc += 1
        a, moi = kq["da_ap"][0], kq["khung"]
        assert set(s._vi_tri(moi)) == truoc | {i} and a["the_cho"] is None  # thêm thẳng, không điểm nào bị thế
        assert (ng is None or a["ngay"] == ng) and (b is None or a["buoi"] == b)
        assert moi["day_them"] == kq["luu"]["day_them"] == [a["ngay"]] and v2.kiem_khung_v2(B, moi) == []
        khong_dau = {x: v for x, v in moi.items() if x != "day_them"}
        assert set(v2.kiem_khung_v2(B, khong_dau)) and set(v2.kiem_khung_v2(B, khong_dau)) <= NHIP  # chỉ nhịp đi bị vượt
        _gio_di_duoc(moi, a["ngay"])
        cau = s.thay_doi(B, kq)[0]
        assert cau["duoc"] and f"Ngày {a['ngay']} nay dày hơn nhịp {v2.NHAN_KIEU_DI[kieu]} bạn chọn" in cau["cau"]
    assert n_duoc > 0 and (n == 1 or n_goi_y > 0)


def test_groups_with_children_or_elderly_are_not_changed():
    """Luật của đoàn có trẻ nhỏ / người lớn tuổi (một điểm một buổi, hai điểm một ngày) không phải nhịp đi ⇒ cờ bật không đổi gì cho đoàn đó."""
    for them in ({"tre_em": 1}, {"lon_tuoi": True}):
        k = v2.xep_v2(B, v2.ThamSoV2(2, kieu_di="can_bang", so_thich=("di_tich",), **them))
        luu = s.luu_tu_lich(k, None, None)
        for i, ng, b in _lenh(k):
            assert _them(luu, i, ng, b, them_day=True) == _them(luu, i, ng, b)
        vt = s._vi_tri(k)
        co_dau = s._xep(B, {**luu, "day_them": [1]}, s._ts(k["tham_so"]), vt, [])
        assert "day_them" not in co_dau  # dấu không có tác dụng với đoàn này


def test_later_edits_work_on_a_denser_schedule():
    """Lịch đã dày: bỏ từng điểm ban ngày đều làm được và khung vẫn đúng luật (kể cả khi buổi vừa trống không còn điểm lấp nào hợp giờ đã lùi); thêm lần
    nữa vào chính ngày đó không vượt trần ba điểm một buổi; đổi chỗ hai ngày thì dấu đi theo nội dung của ngày."""
    k, luu = _lich(2, "can_bang")
    dau = next(kq for i, ng, b in _lenh(k) if ng is None and (kq := _them(luu, i, them_day=True))["da_ap"])
    ngay = dau["da_ap"][0]["ngay"]
    for j in s._vi_tri(dau["khung"]):
        kq = s.ap(B, dau["luu"], [s.HanhDong(loai="bo_diem", ten=T[j]["ten"])], them_khong_the=True, them_day=True)
        assert kq["da_ap"] and v2.kiem_khung_v2(B, kq["khung"]) == []
        _gio_di_duoc(kq["khung"], ngay)
    for i, ng, b in _lenh(dau["khung"]):
        kq = _them(dau["luu"], i, ng, b, them_day=True)
        assert v2.kiem_khung_v2(B, kq["khung"]) == []
        assert all(len(x["buoi"][bb]) <= v2.TOI_DA_BUOI + 1 for x in kq["khung"]["ngay"] for bb in v2.BUOI_NGAY)
        cach = (kq["khong_doi"][0].get("cach") or ()) if kq["khong_doi"] else ()
        assert all(g["thay"] is not None or g.get("day") for g in cach)  # lịch này buổi nào cũng đầy ⇒ mọi cách "thêm thẳng" đều làm ngày dày hơn
        assert len(cach) <= 1 or all(g["thay"] is not None for g in cach)  # có cách không mất điểm ⇒ chỉ nêu MỘT cách đó (không ghép "… hoặc thay …")
    # thêm LẦN NỮA vào ngày đang dày (lịch nhẹ nhàng một ngày: sáng 2 rồi chiều 2): qua được ở lần thử thường, vẫn phải có dòng báo + dòng ghi chú của lịch
    k1, luu1 = _lich(1, "nhe_nhang")
    n_lan_hai = 0
    for kq1 in (kq for i, ng, b in _lenh(k1) if ng is None and (kq := _them(luu1, i, them_day=True))["da_ap"]):
        for i, ng, b in _lenh(kq1["khung"]):
            kq2 = _them(kq1["luu"], i, ng, b, them_day=True)
            if kq2["da_ap"]:
                n_lan_hai += 1
                assert kq2["da_ap"][0].get("day") and "Ngày 1 nay dày hơn nhịp" in s.thay_doi(B, kq2)[0]["cau"]
                assert kq2["khung"]["day_them"] == [1] and v2.kiem_khung_v2(B, kq2["khung"]) == []
                _gio_di_duoc(kq2["khung"], 1)
        if n_lan_hai:
            break
    assert n_lan_hai > 0
    # dòng báo đi theo LỊCH: khối ghi chú của thẻ lịch (và file tải về) có đúng một dòng cho ngày đã dày; lịch gốc không có
    ghi = [g for g in v2.dung_lich(B, dau["khung"], {})["ghi_chu"] if g["ma"] == "day_them"]
    assert len(ghi) == 1 and ghi[0]["cau"].startswith(f"Ngày {ngay} dày hơn nhịp cân bằng bạn chọn vì bạn đã xin thêm điểm: buổi ")
    assert not [g for g in v2.dung_lich(B, k, {})["ghi_chu"] if g["ma"] == "day_them"]
    # bỏ chính điểm vừa thêm ⇒ ngày hết vượt nhịp ⇒ dấu tự gỡ, giờ về như lịch gốc
    bo = s.ap(B, dau["luu"], [s.HanhDong(loai="bo_diem", ten=T[dau["da_ap"][0]["diem"]]["ten"])], them_khong_the=True, them_day=True)
    assert bo["da_ap"] and "day_them" not in bo["khung"] and bo["khung"]["gio"] == k["gio"]
    # đổi chỗ hai ngày ⇒ dấu đi theo NỘI DUNG: đúng một ngày có dấu, là ngày kia
    n_doi = 0
    for i, ng, b in _lenh(k):
        kq = _them(luu, i, ng, b, them_day=True)
        if not kq["da_ap"]:
            continue
        doi = s.doi_cho_ngay(B, kq["luu"], 1, 2)
        if doi["da_ap"]:
            n_doi += 1
            assert doi["khung"]["day_them"] == [3 - kq["da_ap"][0]["ngay"]] and v2.kiem_khung_v2(B, doi["khung"]) == []
        else:
            assert doi["khung"] == kq["khung"]
    assert n_doi > 0


def test_validator_keeps_the_ceilings_of_a_marked_day():
    """`kiem_khung_v2` với ngày có dấu: bốn điểm một buổi vẫn là `qua_day_buoi`; buổi sáng kết sau 13:30, buổi chiều kết sau 18:00, bữa trưa dưới 60 phút
    ⇒ `day_qua_gio`; dấu ở ngày khác không che được ngày này."""
    k, luu = _lich(2, "can_bang")
    dau = next(kq for i, ng, b in _lenh(k) if ng is None and (kq := _them(luu, i, them_day=True))["da_ap"])
    khung, ngay = dau["khung"], dau["da_ap"][0]["ngay"]
    ng = next(x for x in khung["ngay"] if x["ngay"] == ngay)
    assert v2.kiem_khung_v2(B, khung) == []

    def voi_gio(j, bd, kt):
        moi = copy.deepcopy(khung)
        moi["gio"][j] = v2.in_gio(bd, kt)
        return set(v2.kiem_khung_v2(B, moi))

    sang, chieu = ng["buoi"]["sang"], ng["buoi"]["chieu"]
    if sang:
        dai = v2.PHUT[T[sang[-1]]["thoi_luong"]]
        assert "day_qua_gio" in voi_gio(sang[-1], v2.GIO_KET_SANG_DAY + 15 - dai, v2.GIO_KET_SANG_DAY + 15)
    if chieu:
        dai = v2.PHUT[T[chieu[-1]]["thoi_luong"]]
        assert "day_qua_gio" in voi_gio(chieu[-1], v2.GIO_KET_CHIEU_DAY + 15 - dai, v2.GIO_KET_CHIEU_DAY + 15)
    if sang and chieu:
        bd, kt = _phut(khung, chieu[0])
        ket_sang = _phut(khung, sang[-1])[1]
        assert "day_qua_gio" in voi_gio(chieu[0], ket_sang + v2.NGHI_TRUA - 15, ket_sang + v2.NGHI_TRUA - 15 + kt - bd)
    dong = copy.deepcopy(khung)
    buoi_day = max(v2.BUOI_NGAY, key=lambda b: len(ng["buoi"][b]))
    them = [j for j in NGAY_DIEM if j not in s._vi_tri(khung)][: v2.TOI_DA_BUOI + 2 - len(ng["buoi"][buoi_day])]
    next(x for x in dong["ngay"] if x["ngay"] == ngay)["buoi"][buoi_day] += them
    dong["gio"].update({j: "8:00 – 9:15" for j in them})
    assert "qua_day_buoi" in v2.kiem_khung_v2(B, dong)
    lech = {**copy.deepcopy(khung), "day_them": [3 - ngay]}
    assert set(v2.kiem_khung_v2(B, lech)) & NHIP
