"""Hai công tắc buổi tối của lịch "Lên kế hoạch" (23/11/2026) — phần code, 0 USD, bảng điểm thật (riêng tư) qua `flags_from`.

`toi_nhe`: đoàn có trẻ nhỏ / người lớn tuổi được MỘT hoạt động tối nhẹ mỗi tối không phải ngày đi xa, chỉ trong danh sách `toi_nhe` của bảng, không lặp.
`bo_toi_de_trong`: lệnh bỏ một hoạt động buổi tối ⇒ tối đó để trống (cả ở các lần sửa sau), buổi tối ngày khác và điểm ban ngày giữ nguyên.
Phép đếm mọi tổ hợp biểu mẫu (960) là script riêng tư ngoài git; ở đây là các ca giữ hành vi. Test không ghi tên điểm nào của bảng (bảng riêng tư).
"""
import itertools

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_cong_dot_1 import flags_from

TAT = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True)
BAT = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, sua_lich_v2=True, toi_nhe=True, bo_toi_de_trong=True)
B0, B1 = TAT.bang_lich_v2, BAT.bang_lich_v2
DOAN = [dict(tre_em=1), dict(lon_tuoi=True), dict(tre_em=2, lon_tuoi=True)]


def _toi(khung):
    return [ng["buoi"]["toi"] for ng in khung["ngay"]]


def _ban_ngay(khung):
    return [[ng["buoi"][b] for b in v2.BUOI_NGAY] for ng in khung["ngay"]]


def test_both_switches_default_off_and_off_keeps_the_old_rule():
    assert (AssistantFlags().toi_nhe, AssistantFlags().bo_toi_de_trong) == (False, False)
    assert B0.toi_nhe == () and len(B1.toi_nhe) >= 2  # tắt ⇒ bộ xếp không thấy danh sách của bảng
    for doan, n in itertools.product(DOAN, (1, 3, 5)):
        k = v2.xep_v2(B0, v2.ThamSoV2(n, kieu_di="can_bang", **doan))
        assert _toi(k) == [[]] * n and "han_che" in k["gia_dinh"] and "toi_trong" not in k["tham_so"]


def test_restricted_groups_get_one_light_evening_activity_without_repeats():
    for doan, n, kieu in itertools.product(DOAN, (1, 2, 3, 4, 5), ("nhe_nhang", "can_bang", "kham_pha")):
        ts = v2.ThamSoV2(n, kieu_di=kieu, **doan)
        k, cu = v2.xep_v2(B1, ts), v2.xep_v2(B0, ts)
        assert v2.kiem_khung_v2(B1, k) == [] and _ban_ngay(k) == _ban_ngay(cu)  # buổi tối thêm vào KHÔNG làm đổi lịch ban ngày
        chon = [j for t in _toi(k) for j in t]
        assert all(len(t) <= 1 for t in _toi(k)) and set(chon) <= set(B1.toi_nhe) and len(chon) == len(set(chon))
        for ng in k["ngay"]:
            xa = any(B1.theo_id[j]["cum"] == v2.CUM_XA for b in v2.BUOI_NGAY for j in ng["buoi"][b])
            if not ng["buoi"]["toi"]:  # tối trống luôn có lý do đúng: ngày đi xa, hoặc danh sách nhẹ đã dùng hết
                assert k["toi_nghi"][ng["ngay"]] == ("xa" if xa else "het_nhe")
            else:
                assert not xa
        assert "han_che_toi" in k["gia_dinh"] and "han_che" not in k["gia_dinh"]
    k = v2.xep_v2(B1, v2.ThamSoV2(2, kieu_di="nhe_nhang", tre_em=1))
    assert chon_duoc(k), "lịch 2 ngày nhẹ nhàng của đoàn có trẻ nhỏ phải có ít nhất một hoạt động tối"
    lich = v2.dung_lich(B1, k, {})
    muc_toi = [m for ng in lich["ngay"] for m in ng["muc"] if m["loai"] == "hoat_dong_toi"]
    assert muc_toi and all(m["ghi_chu"].endswith(v2.GHI_CHU_TOI_NHE) for m in muc_toi)  # thẻ nói thật vì sao là hoạt động này


def chon_duoc(khung) -> bool:
    return any(_toi(khung))


def test_groups_without_restriction_are_untouched_by_the_light_evening_switch():
    for n, kieu, st in itertools.product((1, 3, 5), ("nhe_nhang", "kham_pha"), ((), ("am_thuc",))):
        ts = v2.ThamSoV2(n, kieu_di=kieu, so_thich=st)
        assert v2.xep_v2(B1, ts) == v2.xep_v2(B0, ts)
    lich = v2.dung_lich(B1, v2.xep_v2(B1, v2.ThamSoV2(2, kieu_di="can_bang")), {})
    assert not any((m.get("ghi_chu") or "").endswith(v2.GHI_CHU_TOI_NHE) for ng in lich["ngay"] for m in ng["muc"])


def test_schedule_check_rejects_an_evening_activity_outside_the_light_list_for_restricted_groups():
    k = v2.xep_v2(B1, v2.ThamSoV2(1, kieu_di="nhe_nhang", tre_em=1))
    ban_ngay = {j for row in _ban_ngay(k) for buoi in row for j in buoi}
    ngoai = next(d["id"] for d in B1.diem if "toi" in d["buoi"] and d["cum"] in v2.CUM_TOI and d["id"] not in B1.toi_nhe and d["id"] not in ban_ngay)
    k["ngay"][0]["buoi"]["toi"] = [ngoai]
    k["toi_nghi"] = {}
    assert "toi_qua_day" in v2.kiem_khung_v2(B1, k)
    assert "toi_qua_day" in v2.kiem_khung_v2(B0, k)  # luật cũ (công tắc tắt): đoàn hạn chế không có buổi tối nào


def test_removing_an_evening_activity_leaves_that_evening_empty_and_touches_nothing_else():
    ts = v2.ThamSoV2(3, kieu_di="can_bang", so_thich=("di_tich",))
    k = v2.xep_v2(B1, ts)
    assert all(_toi(k)), "ca mẫu cần ba tối đều có hoạt động"
    luu = s.luu_tu_lich(k, None, None)
    bo = k["ngay"][1]["buoi"]["toi"][0]
    lenh = [s.HanhDong(loai="bo_diem", ten=B1.theo_id[bo]["ten"])]

    kq = s.ap(B1, luu, lenh, bo_toi_de_trong=True)
    m = kq["khung"]
    assert [(a["loai"], a["diem"], a["toi_trong"]) for a in kq["da_ap"]] == [("bo_diem", bo, [2])]
    assert _toi(m) == [_toi(k)[0], [], _toi(k)[2]] and _ban_ngay(m) == _ban_ngay(k) and v2.kiem_khung_v2(B1, m) == []
    assert m["tham_so"]["toi_trong"] == [2] and m["toi_nghi"][2] == "da_bo" and bo in kq["luu"]["loai"]
    cau = s.thay_doi(B1, kq)[0]["cau"]
    assert cau == f"Đã bỏ {B1.theo_id[bo]['ten']}; buổi tối ngày 2 để trống."

    # sửa tiếp (bỏ một điểm ban ngày): bộ xếp chạy lại nhưng tối đã bỏ vẫn trống, hoạt động đã bỏ không quay lại ở tối nào
    x = next(j for row in _ban_ngay(m) for buoi in row for j in buoi)
    kq2 = s.ap(B1, kq["luu"], [s.HanhDong(loai="bo_diem", ten=B1.theo_id[x]["ten"])], bo_toi_de_trong=True)
    assert kq2["da_ap"] and _toi(kq2["khung"])[1] == [] and bo not in [j for t in _toi(kq2["khung"]) for j in t]

    # công tắc tắt (mặc định): cùng lệnh ⇒ như cũ — bộ xếp chọn hoạt động tối khác cho tối đó, không có khoá `toi_trong`
    cu = s.ap(B0, s.luu_tu_lich(v2.xep_v2(B0, ts), None, None), lenh)
    assert _toi(cu["khung"])[1] and "toi_trong" not in cu["khung"]["tham_so"] and "toi_trong" not in cu["da_ap"][0]


def test_removing_a_repeated_evening_activity_on_one_named_day_keeps_its_other_evening():
    lap = None
    for kieu, st in itertools.product(("nhe_nhang", "can_bang", "kham_pha"), ((), ("am_thuc",), ("di_tich",), ("thien_nhien",), ("chup_anh",))):
        k = v2.xep_v2(B1, v2.ThamSoV2(5, kieu_di=kieu, so_thich=st))
        phang = [j for t in _toi(k) for j in t]
        if len(phang) != len(set(phang)):
            lap = k
            break
    if lap is None:  # bảng đổi tới mức không lịch nào còn lặp hoạt động tối ⇒ ca này không còn gì để giữ
        return
    i = next(j for j in phang if phang.count(j) > 1)
    ngay = [ng["ngay"] for ng in lap["ngay"] if i in ng["buoi"]["toi"]]
    kq = s.ap(B1, s.luu_tu_lich(lap, None, None), [s.HanhDong(loai="bo_diem", ten=B1.theo_id[i]["ten"], ngay=ngay[-1])], bo_toi_de_trong=True)
    m = kq["khung"]
    assert kq["da_ap"][0]["toi_trong"] == [ngay[-1]] and i not in kq["luu"]["loai"]
    assert _toi(m)[ngay[-1] - 1] == [] and _toi(m)[ngay[0] - 1] == [i] and v2.kiem_khung_v2(B1, m) == []
