"""Ngày + âm lịch Việt Nam cho trợ lý (Phase 9 T1, plan `docs/superpowers/plans/2026-11-08-phase-9-t1-ngay-plan.md`).

**Code** tính ngày và đổi dương ↔ âm; model chỉ gửi số + loại lịch, không tự đổi (luật AI FDE: phép tính ⇒ code). Lịch âm Việt Nam (múi UTC+7) bằng
`lunar-vn` 1.4.0 (bản Python của thuật toán Hồ Ngọc Đức, MIT, 0 phụ thuộc — E đọc hết mã 08/11). Không dùng thư viện lịch Trung Quốc (UTC+8 lệch:
Tết 1985 VN 21/01 ↔ TQ 20/02, Tết 2007 VN 17/02 ↔ TQ 18/02).

Chỉ nhận năm **1976–2100**: E so ngày Tết `lunar-vn` với bảng tính sẵn của Hồ Ngọc Đức 1901–2099 (`data/phase_9/t1/tools/so_tet.py`) — khớp mọi năm từ 1966; lệch
1 ngày ở 4 năm trước đó (lịch Việt Nam xưa theo UTC+8 / dựng lại lịch sử). Trước 1976 hai miền dùng lịch khác nhau (Tết Mậu Thân 1968: miền Bắc 29/01, miền
Nam — có Huế — 30/01) ⇒ câu cố định, không đoán. Mọi chữ trả về do code dựng.
"""
import datetime as dt
from typing import Literal

from lunar_vn import LunarDate, can_chi, lunar_to_solar, solar_to_lunar

from llm.full_corpus_prompt import VIETNAM_TZ

NAM_MIN, NAM_MAX = 1976, 2100
THU = ("Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ nhật")
TEN_THANG_AM = {1: "Giêng", 12: "Chạp"}
CAU_NGOAI_KHOANG = f"Mình chỉ đổi được ngày từ năm {NAM_MIN} đến {NAM_MAX} (trước {NAM_MIN} lịch âm hai miền khác nhau)."
CAU_NGAY_SAI = "Ngày này không có trong lịch."


def hom_nay(now: dt.datetime | None = None) -> dt.date:
    """Ngày hôm nay theo giờ Việt Nam (không theo giờ máy chủ)."""
    return (now or dt.datetime.now(VIETNAM_TZ)).astimezone(VIETNAM_TZ).date()


def _thang_am(am: LunarDate) -> str:
    ten = TEN_THANG_AM.get(am.month, str(am.month))
    return f"tháng {ten}" + (" (nhuận)" if am.leap else "")


def mo_ta(ngay: dt.date) -> str:
    """Một ngày dương ⇒ một dòng chữ do code dựng: thứ, ngày dương, ngày âm, năm can chi (theo năm âm)."""
    am = solar_to_lunar(ngay)
    return (f"{THU[ngay.weekday()]}, {ngay:%d/%m/%Y} dương lịch — ngày {am.day} {_thang_am(am)} âm lịch, "
            f"năm {can_chi.get_year_can_chi(am.year)}")


def doi(ngay: int, thang: int, nam: int, loai: Literal["duong", "am"], nhuan: bool = False) -> str:
    """Đổi một ngày người dùng nêu (dương ⇒ âm hoặc âm ⇒ dương) ⇒ dòng chữ của `mo_ta`, hoặc câu cố định khi ngoài khoảng / không có ngày đó."""
    if not NAM_MIN <= nam <= NAM_MAX:
        return CAU_NGOAI_KHOANG
    try:
        if loai == "duong":
            if nhuan:
                return CAU_NGAY_SAI
            return mo_ta(dt.date(nam, thang, ngay))
        am = LunarDate(ngay, thang, nam, nhuan)
        duong = lunar_to_solar(am)
    except ValueError:  # ngày dương không có (31/4…), tháng âm sai, cờ nhuận không khớp năm
        return CAU_NGAY_SAI
    # `lunar_to_solar` không kiểm số ngày của tháng âm (30 ở tháng 29 ngày ⇒ lặng lẽ ra ngày đầu tháng sau) ⇒ đổi ngược để chắc ngày có thật
    if solar_to_lunar(duong) != am:
        return CAU_NGAY_SAI
    if not NAM_MIN <= duong.year <= NAM_MAX:
        return CAU_NGOAI_KHOANG
    return mo_ta(duong)
