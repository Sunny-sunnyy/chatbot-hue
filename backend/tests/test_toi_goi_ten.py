"""Công tắc `toi_goi_ten` (23/11/2026) — người dùng GỌI TÊN hoạt động tối muốn có; phần code, 0 USD, bảng điểm thật (riêng tư) qua `flags_from`.

Hai cách model vốn ghi câu này: `thay_diem(ten=<mục tối đang có>, ten_moi=<tên>)` và `them_diem(ten=<tên>, ngay=N, buoi="toi")`. Công tắc mở ⇒ code
đặt đúng mục đó vào tối đó (ghim), tối khác + ban ngày giữ nguyên; mục đang ở tối khác ⇒ hai tối đổi chỗ; không làm được ⇒ câu nói thật lý do.
"""
import collections
import itertools

import pytest

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from test_cong_dot_1 import flags_from

B = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True).bang_lich_v2
B_NHE = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, toi_nhe=True).bang_lich_v2
TOI = [d["id"] for d in B.diem if "toi" in d["buoi"]]
LOAI = ("di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh")
SO_THICH = [()] + [(a,) for a in LOAI] + list(itertools.combinations(LOAI, 2))
BAT = dict(them_khong_the=True, bo_toi_hoi_lai=True, toi_goi_ten=True)


def _toi(khung):
    return {ng["ngay"]: ng["buoi"]["toi"][0] for ng in khung["ngay"] if ng["buoi"]["toi"]}


def _ban_ngay(khung):
    return [[ng["buoi"][b] for b in v2.BUOI_NGAY] for ng in khung["ngay"]]


def _ten(i, bang=B):
    return bang.theo_id[i]["ten"]


def test_switch_is_off_by_default_and_needs_the_ask_first_switch():
    assert AssistantFlags().toi_goi_ten is False
    with pytest.raises(ValueError):
        AssistantFlags(toi_goi_ten=True)
    k = v2.xep_v2(B, v2.ThamSoV2(2, kieu_di="can_bang"))
    luu, toi = s.luu_tu_lich(k, None, None), _toi(k)
    khac = next(j for j in TOI if j not in toi.values() and not B.theo_id[j].get("ngay_hoat_dong") and j not in s._vi_tri(k))
    kq = s.ap(B, luu, [s.HanhDongToiHoiBo(loai="thay_diem", ten=_ten(toi[1]), ten_moi=_ten(khac))], them_khong_the=True, bo_toi_hoi_lai=True)
    assert not kq["da_ap"] and kq["khung"] == k  # công tắc tắt ⇒ như cũ: câu từ chối, lịch không đổi


def test_every_named_replacement_on_the_form_grid_lands_on_that_evening_only_or_says_why():
    """Mọi lệnh "thay <mục tối đang có> bằng <mục tối khác của bảng>" trên lưới biểu mẫu của đoàn thường (lịch không có ngày đi)."""
    dem = collections.Counter()
    for n, kieu, st in itertools.product((1, 2, 3, 4, 5), ("nhe_nhang", "can_bang", "kham_pha"), SO_THICH):
        k = v2.xep_v2(B, v2.ThamSoV2(n, kieu_di=kieu, so_thich=st))
        luu, toi, vt = s.luu_tu_lich(k, None, None), _toi(k), s._vi_tri(k)
        for d, x in toi.items():
            for y in TOI:
                if y == x:
                    continue
                kq = s.ap(B, luu, [s.HanhDongToiHoiBo(loai="thay_diem", ten=_ten(x), ten_moi=_ten(y), ngay=d)], **BAT)
                sau = _toi(kq["khung"])
                if not kq["da_ap"]:  # không đặt được ⇒ lịch đứng yên + đúng lý do
                    assert kq["khung"] == k and len(kq["khong_doi"]) == 1
                    ma = kq["khong_doi"][0]["ma_luat"]
                    assert ma == ("toi_ten_ban_ngay" if y in vt else "toi_ten_theo_thu"), (ma, y)
                    cau = s.thay_doi(B, kq)[0]["cau"]
                    assert _ten(y) in cau
                    if ma == "toi_ten_theo_thu":  # câu nói rõ nơi đó mở tối nào và cách để đặt được
                        assert all(s.THU[t] in cau for t in B.theo_id[y]["ngay_hoat_dong"]) and "chọn ngày đi ở biểu mẫu" in cau
                    dem[ma] += 1
                    continue
                assert v2.kiem_khung_v2(B, kq["khung"]) == [] and _ban_ngay(kq["khung"]) == _ban_ngay(k) and sau[d] == y
                cau = s.thay_doi(B, kq)[0]["cau"]
                assert cau.startswith(f"Đã thay {_ten(x)} bằng {_ten(y)} ở buổi tối ngày {d}.")
                if y in toi.values():  # mục được gọi tên đang ở tối khác ⇒ hai tối đổi chỗ, dòng báo nói mục kia đi đâu
                    d2 = next(a for a, b in toi.items() if b == y)
                    assert sau == {**toi, d: y, d2: x} and f"{_ten(x)} chuyển sang buổi tối ngày {d2}." in cau
                    dem["doi_cho"] += 1
                else:
                    assert sau == {**toi, d: y} and "Buổi tối xếp lại" not in cau
                    dem["thay"] += 1
    tong = sum(dem.values())
    assert tong > 5000 and (dem["thay"] + dem["doi_cho"]) / tong > 0.85, dem  # đếm 23/11/2026: 56,9 % + 28,8 % làm được


def test_naming_an_activity_for_an_evening_places_it_and_survives_a_later_edit():
    k = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang"))
    luu, toi = s.luu_tu_lich(k, None, None), _toi(k)
    moi = next(j for j in TOI if j not in toi.values() and not B.theo_id[j].get("ngay_hoat_dong") and j not in s._vi_tri(k))
    kq = s.ap(B, luu, [s.HanhDongToiHoiBo(loai="them_diem", ten=_ten(moi), ngay=1, buoi="toi")], **BAT)
    assert _toi(kq["khung"]) == {**toi, 1: moi} and _ban_ngay(kq["khung"]) == _ban_ngay(k)
    assert s.thay_doi(B, kq)[0]["cau"] == f"Đã thêm {_ten(moi)} (ngày 1, buổi tối, thế chỗ {_ten(toi[1])})."
    # lần sửa sau (bỏ một điểm ban ngày) không làm buổi tối dồn hàng lại
    y = _ban_ngay(kq["khung"])[1][0][0]
    kq2 = s.ap(B, kq["luu"], [s.HanhDong(loai="bo_diem", ten=_ten(y))], **BAT)
    assert kq2["da_ap"] and _toi(kq2["khung"]) == {**toi, 1: moi}
    # không nói ngày ⇒ hỏi ngày, lịch không đổi; mục đang ở đúng tối được xin ⇒ câu "đang ở … rồi"
    kq3 = s.ap(B, luu, [s.HanhDongToiHoiBo(loai="them_diem", ten=_ten(moi))], **BAT)
    assert not kq3["da_ap"] and [d["ma_luat"] for d in kq3["khong_doi"]] == ["toi_ten_thieu_ngay"] and "ngày nào" in s.thay_doi(B, kq3)[0]["cau"]
    kq4 = s.ap(B, luu, [s.HanhDongToiHoiBo(loai="them_diem", ten=_ten(toi[3]), ngay=3, buoi="toi")], **BAT)
    assert [d["ma_luat"] for d in kq4["khong_doi"]] == ["toi_dang_o"]
    # tối người dùng đã để trống rồi gọi tên một mục cho tối đó ⇒ hết trống
    trong = s.ap(B, luu, [s.HanhDongToiHoiBo(loai="bo_diem", ten=_ten(toi[3]), ngay=3, cach_toi="de_trong")], **BAT)
    assert 3 not in _toi(trong["khung"])
    kq5 = s.ap(B, trong["luu"], [s.HanhDongToiHoiBo(loai="them_diem", ten=_ten(moi), ngay=3, buoi="toi")], **BAT)
    assert _toi(kq5["khung"]) == {1: toi[1], 2: toi[2], 3: moi}


def test_groups_with_children_or_elderly_only_get_light_activities_by_name_and_far_days_stay_free():
    nhe, ngoai = B_NHE.toi_nhe, [j for j in TOI if j not in B_NHE.toi_nhe and not B_NHE.theo_id[j].get("ngay_hoat_dong")]
    k = v2.xep_v2(B_NHE, v2.ThamSoV2(3, tre_em=1))
    luu, toi = s.luu_tu_lich(k, None, None), _toi(k)
    moi = next(j for j in nhe if j not in toi.values() and j not in s._vi_tri(k))
    kq = s.ap(B_NHE, luu, [s.HanhDongToiHoiBo(loai="them_diem", ten=_ten(moi, B_NHE), ngay=1, buoi="toi")], **BAT)
    assert _toi(kq["khung"])[1] == moi and v2.kiem_khung_v2(B_NHE, kq["khung"]) == []
    kq = s.ap(B_NHE, luu, [s.HanhDongToiHoiBo(loai="them_diem", ten=_ten(ngoai[0], B_NHE), ngay=1, buoi="toi")], **BAT)
    assert not kq["da_ap"] and [d["ma_luat"] for d in kq["khong_doi"]] == ["toi_ten_khong_nhe"] and kq["khung"] == k
    # công tắc `toi_nhe` TẮT: đoàn này không có buổi tối nào ⇒ câu nói đúng điều đó, không nói "chỉ nhận hoạt động nhẹ" (B đọc code 23/11/2026)
    k0 = v2.xep_v2(B, v2.ThamSoV2(3, tre_em=1))
    kq = s.ap(B, s.luu_tu_lich(k0, None, None), [s.HanhDongToiHoiBo(loai="them_diem", ten=_ten(nhe[0]), ngay=1, buoi="toi")], **BAT)
    assert not kq["da_ap"] and [d["ma_luat"] for d in kq["khong_doi"]] == ["toi_ten_han_che"] and "không xếp hoạt động buổi tối" in s.thay_doi(B, kq)[0]["cau"]
    # ngày đi xa: tối để nghỉ, gọi tên cũng không đặt
    for n, kieu, st in itertools.product((3, 4, 5), ("can_bang", "kham_pha"), SO_THICH):
        k = v2.xep_v2(B, v2.ThamSoV2(n, kieu_di=kieu, so_thich=st))
        xa = [ng["ngay"] for ng in k["ngay"] if k["toi_nghi"].get(ng["ngay"]) == "xa"]
        if xa:
            moi = next(j for j in TOI if j not in _toi(k).values() and not B.theo_id[j].get("ngay_hoat_dong") and j not in s._vi_tri(k))
            kq = s.ap(B, s.luu_tu_lich(k, None, None), [s.HanhDongToiHoiBo(loai="them_diem", ten=_ten(moi), ngay=xa[0], buoi="toi")], **BAT)
            assert not kq["da_ap"] and [d["ma_luat"] for d in kq["khong_doi"]] == ["toi_ten_ngay_xa"]
            assert f"Ngày {xa[0]} đi xa" in s.thay_doi(B, kq)[0]["cau"]
            break
    else:
        raise AssertionError("lưới phải có một lịch có ngày đi xa")
