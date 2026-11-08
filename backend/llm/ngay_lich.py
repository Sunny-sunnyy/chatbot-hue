"""Ngày + âm lịch Việt Nam cho trợ lý (Phase 9 T1, plan `docs/superpowers/plans/2026-11-08-phase-9-t1-ngay-plan.md`).

**Code** tính ngày và đổi dương ↔ âm; model chỉ gửi số + loại lịch, không tự đổi (luật AI FDE: phép tính ⇒ code). Lịch âm Việt Nam (múi UTC+7) bằng
`lunar-vn` 1.4.0 (bản Python của thuật toán Hồ Ngọc Đức, MIT, 0 phụ thuộc — E đọc hết mã 08/11). Không dùng thư viện lịch Trung Quốc (UTC+8 lệch:
Tết 1985 VN 21/01 ↔ TQ 20/02, Tết 2007 VN 17/02 ↔ TQ 18/02).

Chỉ nhận năm **1976–2100**: E so ngày Tết `lunar-vn` với bảng tính sẵn của Hồ Ngọc Đức 1901–2099 (`data/phase_9/t1/tools/so_tet.py`) — khớp mọi năm từ 1966; lệch
1 ngày ở 4 năm trước đó (lịch Việt Nam xưa theo UTC+8 / dựng lại lịch sử). Trước 1976 hai miền dùng lịch khác nhau (Tết Mậu Thân 1968: miền Bắc 29/01, miền
Nam — có Huế — 30/01) ⇒ câu cố định, không đoán. Mọi chữ trả về do code dựng.
"""
import datetime as dt
import re
import unicodedata
from typing import Literal

from lunar_vn import LunarDate, can_chi, lunar_to_solar, solar_to_lunar

from llm.full_corpus_prompt import _WEEKDAYS as THU, VIETNAM_TZ  # review plan m-2: dùng lại bảng tên thứ của `today_line`

NAM_MIN, NAM_MAX = 1976, 2100
TEN_THANG_AM = {1: "Giêng", 12: "Chạp"}
CAU_NGOAI_KHOANG = f"Mình chỉ đổi được ngày từ năm {NAM_MIN} đến {NAM_MAX} (trước {NAM_MIN} lịch âm hai miền khác nhau)."
CAU_NGAY_SAI = "Ngày này không có trong lịch."


def hom_nay(now: dt.datetime | None = None) -> dt.date:
    """Ngày hôm nay theo giờ Việt Nam (không theo giờ máy chủ). Như `thoi_tiet.hom_nay_vn` nhưng nhận `now` để test được ca qua nửa đêm."""
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


# Dò từ chỉ ngày (code — chỉ khi có mới đưa công cụ cho model; bài học B5c: công cụ có mặt mọi lượt đổi cách model tìm). Viết hẹp: "mai" đứng một mình
# không tính (hoa mai, mai mốt), "tết" tính (hỏi ngày Tết), số dạng "15/1" tính. Không tính "khi nào / bao giờ / ngày nào" (câu lịch sử "xây khi nào"
# sẽ nhận công cụ không cần — tốn tiền, rủi ro S4).
_TU_NGAY = re.compile(
    r"(?<!\w)(?:hôm nay|bữa nay|hôm qua|(?:sáng|trưa|chiều|tối|đêm) nay|bây giờ|lúc này|hiện giờ|sắp tới|ngày mai|sáng mai|trưa mai|chiều mai|tối mai|ngày kia|tuần (?:này|sau|tới|trước)|cuối tuần|"
    r"tháng (?:này|sau|tới|trước)|năm (?:nay|sau|tới|ngoái)|thứ (?:hai|ba|tư|năm|sáu|bảy|[2-7])|chủ nhật|rằm|mùng|mồng|âm lịch|dương lịch|"
    r"lịch âm|lịch dương|tết)(?!\w)|\b\d{1,2}/\d{1,2}\b",
    re.IGNORECASE)


def co_tu_ngay(text: str) -> bool:
    return bool(_TU_NGAY.search(unicodedata.normalize("NFC", text)))


def co_tu_ngay_luot(query: str, history) -> bool:
    """Câu cuối **hoặc câu hỏi liền trước** có từ chỉ ngày (như `thoi_tiet.co_tu_khoa_luot`: "còn tuần sau thì sao?")."""
    return co_tu_ngay(query) or bool(history and co_tu_ngay(history[-1][0]))


def ket_qua(loai: Literal["hom_nay", "duong", "am"], ngay: int, thang: int, nam: int, thang_nhuan: bool, now: dt.datetime | None = None) -> str:
    """Chữ trả cho model (do code dựng): luôn có dòng hôm nay; `loai` khác `hom_nay` ⇒ thêm dòng ngày được đổi. `nam` = 0 ⇒ năm nay (năm âm hiện tại khi
    `loai` = "am")."""
    hom = hom_nay(now)
    dong = [f"Hôm nay (giờ Việt Nam): {mo_ta(hom)}."]
    if loai != "hom_nay":
        nam = nam or (solar_to_lunar(hom).year if loai == "am" else hom.year)
        dong.append(f"Ngày được hỏi ({'âm' if loai == 'am' else 'dương'} lịch {ngay}/{thang}/{nam}"
                    + (", tháng nhuận" if thang_nhuan else "") + f"): {doi(ngay, thang, nam, loai, thang_nhuan)}")
    return "\n".join(dong)


# Nguồn trong sổ nguồn (review plan M-2): câu trả lời chỉ có ngày (không đoạn kho) vẫn phải có [n] để qua bộ kiểm citation — như nguồn thời tiết
TIEU_DE_NGUON = "Lịch hệ thống — tính theo giờ Việt Nam"
MUC_NGUON = "Ngày và âm lịch Việt Nam"
NGUON_SOURCE = "he-thong-lich"  # `source` của nguồn — không thuộc tiền tố H4c, không phải bài kho (không `bai_id`)
