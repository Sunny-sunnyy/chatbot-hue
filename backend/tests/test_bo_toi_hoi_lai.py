"""Công tắc `bo_toi_hoi_lai` (23/11/2026; chủ dự án: bỏ hoạt động tối thì "nên hỏi lại người dùng đổi hoạt động hay là để trống") — phần code, 0 USD,
bảng điểm thật (riêng tư) qua `flags_from`.

Lệnh bỏ một hoạt động BUỔI TỐI: chưa nói cách ⇒ lịch giữ nguyên + dòng hỏi lại hai lựa chọn (và hai câu đó được nhớ cho lượt kế); "đổi" ⇒ thay ĐÚNG tối
đó, tối khác và ban ngày giữ nguyên, không lặp; "để trống" ⇒ tối đó trống. Model chỉ ghi lại cách người dùng nói (`cach_toi` của khuôn).
"""
import itertools

import pytest
from pydantic import ValidationError

from llm import lich_trinh_v2 as v2
from llm import sua_lich_v2 as s
from llm.assistant import AssistantFlags
from llm.full_corpus_prompt import SUA_LICH_LOI_DAN_TOI_HOI, SUA_LICH_LOI_DAN_TOI_HOI_BO
from test_cong_dot_1 import flags_from

B = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True).bang_lich_v2
LOAI = ("di_tich", "am_thuc", "thien_nhien", "le_hoi_nghe_thuat", "chup_anh")
SO_THICH = [()] + [(a,) for a in LOAI] + list(itertools.combinations(LOAI, 2))


def _toi(khung):
    return [ng["buoi"]["toi"] for ng in khung["ngay"]]


def _ban_ngay(khung):
    return [[ng["buoi"][b] for b in v2.BUOI_NGAY] for ng in khung["ngay"]]


def _bo(luu, id_, ngay, cach=None):
    lenh = [s.HanhDongToiHoiBo(loai="bo_diem", ten=B.theo_id[id_]["ten"], ngay=ngay, **({"cach_toi": cach} if cach else {}))]
    return s.ap(B, luu, lenh, them_khong_the=True, bo_toi_hoi_lai=True)


def test_switch_is_off_by_default_needs_the_edit_switches_and_adds_one_rule_and_one_field():
    assert AssistantFlags().bo_toi_hoi_lai is False
    with pytest.raises(ValueError):
        AssistantFlags(bo_toi_hoi_lai=True)  # thiếu các công tắc sửa lịch mà nó dựa vào
    assert SUA_LICH_LOI_DAN_TOI_HOI_BO.startswith(SUA_LICH_LOI_DAN_TOI_HOI) and "cach_toi" not in SUA_LICH_LOI_DAN_TOI_HOI
    assert s.HanhDongToiHoiBo(loai="bo_diem", ten="x", cach_toi="doi").cach_toi == "doi"
    with pytest.raises(ValidationError):
        s.HanhDongToiHoi(loai="bo_diem", ten="x", cach_toi="doi")  # khuôn cũ không có trường này


def test_removing_an_evening_activity_without_saying_how_keeps_the_schedule_and_asks():
    k = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang"))
    luu = s.luu_tu_lich(k, None, None)
    x = _toi(k)[1][0]
    kq = _bo(luu, x, 2)
    assert not kq["da_ap"] and kq["khung"] == k and [d["ma_luat"] for d in kq["khong_doi"]] == ["bo_toi_hoi"]
    cau = s.thay_doi(B, kq)[0]["cau"]
    ten = B.theo_id[x]["ten"]
    # dòng hỏi lại là một CÂU HỎI (không mở đầu "Chưa làm", mang `hoi` để giao diện không tô đỏ), nêu tên mục một lần, mời gõ ngắn
    dong = s.thay_doi(B, kq)[0]
    assert dong["hoi"] is True and dong["duoc"] is False
    assert cau == f"Bạn muốn đổi {ten} (tối ngày 2) sang một hoạt động tối khác, hay để trống tối đó? Nhắn «đổi đi» hoặc «để trống» — lịch chưa đổi gì."
    goi_y = s.cau_goi_y(B, kq)
    assert len(goi_y) == 2 and all(ten in c and "ngày 2" in c for c in goi_y)  # hai câu ĐỦ TÊN vẫn được nhớ cho lần hiểu ý của lượt kế
    # công tắc tắt (không truyền `bo_toi_hoi_lai`) ⇒ đường cũ: bỏ là áp ngay
    assert s.ap(B, luu, [s.HanhDong(loai="bo_diem", ten=ten)])["da_ap"]


def test_swap_changes_only_that_evening_never_repeats_and_survives_later_edits():
    """Mọi lệnh "đổi hoạt động tối" trên lưới biểu mẫu của đoàn thường (mỗi tối có hoạt động của mỗi lịch): tối khác 0 đổi, ban ngày 0 đổi, 0 lặp."""
    n_lenh = het = 0
    for n, kieu, st in itertools.product((1, 2, 3, 4, 5), ("nhe_nhang", "can_bang", "kham_pha"), SO_THICH):
        k = v2.xep_v2(B, v2.ThamSoV2(n, kieu_di=kieu, so_thich=st))
        luu = s.luu_tu_lich(k, None, None)
        for d, t in enumerate(_toi(k), start=1):
            if not t:
                continue
            n_lenh += 1
            kq = _bo(luu, t[0], d, "doi")
            sau = _toi(kq["khung"])
            assert [a["loai"] for a in kq["da_ap"]] == ["bo_diem"] and "toi_xep_lai" not in kq["da_ap"][0]
            assert _ban_ngay(kq["khung"]) == _ban_ngay(k) and v2.kiem_khung_v2(B, kq["khung"]) == []
            assert all(sau[i] == _toi(k)[i] for i in range(n) if i != d - 1)  # tối của ngày khác giữ nguyên
            assert sau[d - 1] != t and t[0] not in [j for x in sau for j in x]
            chon = [j for x in sau for j in x]
            assert len(chon) == len(set(chon))
            cau = s.thay_doi(B, kq)[0]["cau"]
            if sau[d - 1]:
                assert cau == f"Đã bỏ {B.theo_id[t[0]]['ten']}; buổi tối ngày {d} đổi sang {B.theo_id[sau[d - 1][0]]['ten']}."
            else:  # hết hoạt động tối chưa dùng ⇒ nói thật là để trống
                het += 1
                assert f"buổi tối ngày {d} để trống vì lịch không còn hoạt động tối nào khác chưa dùng" in cau
            if (n, kieu) == (3, "can_bang") and sau[d - 1]:  # lần sửa SAU (bỏ một điểm ban ngày) không làm buổi tối dồn hàng lại
                y = next(j for ng in _ban_ngay(kq["khung"]) for b in ng for j in b)
                kq2 = s.ap(B, kq["luu"], [s.HanhDong(loai="bo_diem", ten=B.theo_id[y]["ten"])], them_khong_the=True, bo_toi_hoi_lai=True)
                if kq2["da_ap"] and not any(j in _ban_ngay(kq2["khung"])[i][b] for i in range(n) for b in (0, 1) for x in sau for j in x):
                    assert _toi(kq2["khung"]) == sau
    assert n_lenh > 600 and het < n_lenh // 10  # lưới thật phải có đủ lệnh, và "hết mục" là ca hiếm


def test_leave_empty_empties_that_evening_only_and_names_it():
    k = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang"))
    luu = s.luu_tu_lich(k, None, None)
    x = _toi(k)[0][0]
    kq = _bo(luu, x, 1, "de_trong")
    assert _toi(kq["khung"]) == [[]] + _toi(k)[1:] and _ban_ngay(kq["khung"]) == _ban_ngay(k)
    assert s.thay_doi(B, kq)[0]["cau"] == f"Đã bỏ {B.theo_id[x]['ten']}; buổi tối ngày 1 để trống."
    # sửa tiếp: tối đã bỏ vẫn trống, và "đổi" tối khác không lấp lại nó
    y = _toi(kq["khung"])[2][0]
    kq2 = _bo(kq["luu"], y, 3, "doi")
    assert _toi(kq2["khung"])[0] == [] and _toi(kq2["khung"])[1] == _toi(k)[1] and _toi(kq2["khung"])[2] not in ([], [y])


def test_a_pin_left_from_a_day_no_longer_in_the_schedule_does_not_block_the_remaining_evenings():
    """Lịch từng 3 ngày có ghim ở tối ngày 3, rồi rút còn 2 ngày: mục ghim của ngày đã mất phải dùng lại được — buổi tối của lịch 2 ngày giống hệt lịch
    không có ghim nào (trước khi lọc: mục đó bị loại khỏi lựa chọn của mọi tối còn lại)."""
    sach = v2.xep_v2(B, v2.ThamSoV2(2, kieu_di="can_bang"))
    con_ghim = v2.xep_v2(B, v2.ThamSoV2(2, kieu_di="can_bang", toi_chon=((3, _toi(sach)[0][0]),)))
    assert _toi(con_ghim) == _toi(sach)


def test_old_refusals_no_longer_advise_removing_when_removing_now_asks():
    """Công tắc mở: "bỏ" một hoạt động tối là hỏi lại, không tự chọn mục khác ⇒ câu từ chối của "thay / thêm vào buổi tối" không được khuyên "bỏ …, lịch sẽ
    tự chọn"; dòng thường (không phải câu hỏi lại) không mang `hoi`."""
    k = v2.xep_v2(B, v2.ThamSoV2(3, kieu_di="can_bang"))
    luu = s.luu_tu_lich(k, None, None)
    x = _toi(k)[0][0]
    khac = next(d["id"] for d in B.diem if set(d["buoi"]) == {"toi"} and not d.get("ngay_hoat_dong") and d["id"] not in [j for t in _toi(k) for j in t])
    for lenh in ([s.HanhDongToiHoiBo(loai="thay_diem", ten=B.theo_id[x]["ten"], ten_moi=B.theo_id[khac]["ten"])],
                 [s.HanhDongToiHoiBo(loai="them_diem", ten=B.theo_id[khac]["ten"])]):
        dong = s.thay_doi(B, s.ap(B, luu, lenh, them_khong_the=True, bo_toi_hoi_lai=True))
        assert dong and "tự chọn một" not in dong[0]["cau"] and "đổi" in dong[0]["cau"] and "hoi" not in dong[0]
