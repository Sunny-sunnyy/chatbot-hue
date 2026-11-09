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


def ngay_duong(ngay: int, thang: int, nam: int, loai: Literal["duong", "am"], nhuan: bool = False) -> dt.date | str:
    """Ngày người dùng nêu (dương hoặc âm) ⇒ ngày dương, hoặc câu cố định khi ngoài khoảng / không có ngày đó."""
    if not NAM_MIN <= nam <= NAM_MAX:
        return CAU_NGOAI_KHOANG
    if not (1 <= ngay <= 31 and 1 <= thang <= 12):  # review nhánh m-1: số vô lý ⇒ câu cố định (trước: OverflowError làm hỏng cả lượt)
        return CAU_NGAY_SAI
    try:
        if loai == "duong":
            return CAU_NGAY_SAI if nhuan else dt.date(nam, thang, ngay)
        am = LunarDate(ngay, thang, nam, nhuan)
        duong = lunar_to_solar(am)
    except ValueError:  # ngày dương không có (31/4…), tháng âm sai, cờ nhuận không khớp năm
        return CAU_NGAY_SAI
    # `lunar_to_solar` không kiểm số ngày của tháng âm (30 ở tháng 29 ngày ⇒ lặng lẽ ra ngày đầu tháng sau) ⇒ đổi ngược để chắc ngày có thật
    if solar_to_lunar(duong) != am:
        return CAU_NGAY_SAI
    return duong if NAM_MIN <= duong.year <= NAM_MAX else CAU_NGOAI_KHOANG


def doi(ngay: int, thang: int, nam: int, loai: Literal["duong", "am"], nhuan: bool = False) -> str:
    """Đổi một ngày người dùng nêu ⇒ dòng chữ của `mo_ta`, hoặc câu cố định."""
    d = ngay_duong(ngay, thang, nam, loai, nhuan)
    return d if isinstance(d, str) else mo_ta(d)


def so_voi_hom_nay(ngay: dt.date, hom: dt.date) -> str:
    """A chọn (b) 08/11 sau lượt đo (A2: model tự so ngày lễ với hôm nay rồi kết luận ngược): phép so trước / sau do **code** làm."""
    n = (ngay - hom).days
    return "là hôm nay" if n == 0 else (f"còn {n} ngày nữa" if n > 0 else f"đã qua {-n} ngày")


# Dò từ chỉ ngày (code — chỉ khi có mới đưa công cụ cho model; bài học B5c: công cụ có mặt mọi lượt đổi cách model tìm). Viết hẹp: "mai" đứng một mình
# không tính (hoa mai, mai mốt), "tết" tính (hỏi ngày Tết), số dạng "15/1" tính. Không tính "khi nào / bao giờ / ngày nào" (câu lịch sử "xây khi nào"
# sẽ nhận công cụ không cần — tốn tiền, rủi ro S4). "sang năm" tính (09/11, lượt xác nhận bắt sót), trừ khi theo sau là số ("sang năm 1945").
_TU_NGAY = re.compile(
    r"(?<!\w)(?:hôm nay|bữa nay|hôm qua|(?:sáng|trưa|chiều|tối|đêm) nay|bây giờ|lúc này|hiện giờ|sắp tới|ngày mai|sáng mai|trưa mai|chiều mai|tối mai|ngày kia|tuần (?:này|sau|tới|trước)|cuối tuần|"
    r"tháng (?:này|sau|tới|trước)|năm (?:nay|sau|tới|ngoái)|sang năm(?!\s*\d)|chủ nhật|rằm|mùng|mồng|âm lịch|dương lịch|"
    r"lịch âm|lịch dương|tết)(?!\w)"
    # review nhánh m-2: "dd/mm" chỉ khi đứng sau từ chỉ thời điểm hoặc có năm ("1/2", "24/7" đứng một mình không phải ngày)
    r"|(?<!\w)(?:ngày|hôm|sáng|trưa|chiều|tối|đêm|từ|đến|tới|vào|dịp|qua)\s+\d{1,2}/\d{1,2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    re.IGNORECASE)
# review nhánh m-2: "thứ hai / thứ 3…" là ngày trong tuần TRỪ KHI đứng sau danh từ chỉ thứ tự ("vua thứ ba", "lần thứ hai", "mùa thứ hai")
_THU = re.compile(r"(?:(\w+)\s+)?thứ (?:hai|ba|tư|năm|sáu|bảy|[2-7])(?!\w)", re.IGNORECASE)
_THU_TU = {"vua", "đời", "lần", "mùa", "người", "con", "bậc", "tầng", "hạng", "giải", "lớp", "phần", "chương", "tập", "vị", "đợt", "kỳ", "khóa",
           "khoá", "cấp", "hàng", "số", "ngôi", "đứng", "xếp", "thế", "hệ", "chúa", "hoàng", "chiếc", "cái", "điều", "bước", "vòng", "trận"}


def co_tu_ngay(text: str) -> bool:
    text = unicodedata.normalize("NFC", text)
    if _TU_NGAY.search(text):
        return True
    return any((m.group(1) or "").lower() not in _THU_TU for m in _THU.finditer(text))


def co_tu_ngay_luot(query: str, history) -> bool:
    """Câu cuối **hoặc câu hỏi liền trước** có từ chỉ ngày (như `thoi_tiet.co_tu_khoa_luot`: "còn tuần sau thì sao?")."""
    return co_tu_ngay(query) or bool(history and co_tu_ngay(history[-1][0]))


def _ngan(d: dt.date) -> str:
    am = solar_to_lunar(d)
    return f"{THU[d.weekday()]}, {d:%d/%m/%Y} (ngày {am.day} {_thang_am(am)} âm)"


_KHOANG = re.compile(r"(?<!\w)(tuần này|tuần sau|tuần tới|tháng này)(?!\w)", re.IGNORECASE)


def khoang_ngay(cau: str, hom: dt.date) -> list[str]:
    """A chọn (i) 08/11 sau lượt 2 (R7: model tự suy "tuần này là giữa tháng 9 âm" ⇒ sai): câu có "tuần này / tuần sau / tuần tới / tháng này" ⇒ code
    ghi ngày đầu / cuối của khoảng đó (dương + âm). Tuần tính từ thứ Hai. "Tháng này" ⇒ cả tháng dương và tháng âm hiện tại."""
    cum = {m.lower() for m in _KHOANG.findall(unicodedata.normalize("NFC", cau))}
    dong = []
    dau_tuan = hom - dt.timedelta(days=hom.weekday())
    if "tuần này" in cum:
        dong.append(f"Tuần này: từ {_ngan(dau_tuan)} đến {_ngan(dau_tuan + dt.timedelta(days=6))}.")
    if cum & {"tuần sau", "tuần tới"}:
        dong.append(f"Tuần sau: từ {_ngan(dau_tuan + dt.timedelta(days=7))} đến {_ngan(dau_tuan + dt.timedelta(days=13))}.")
    if "tháng này" in cum:
        dau = hom.replace(day=1)
        cuoi = (dau + dt.timedelta(days=32)).replace(day=1) - dt.timedelta(days=1)
        dong.append(f"Tháng này (dương lịch): từ {_ngan(dau)} đến {_ngan(cuoi)}.")
        am = solar_to_lunar(hom)
        dau_am = lunar_to_solar(LunarDate(1, am.month, am.year, am.leap))
        cuoi_am = dau_am + dt.timedelta(days=28)
        while solar_to_lunar(cuoi_am + dt.timedelta(days=1)).day != 1:
            cuoi_am += dt.timedelta(days=1)
        dong.append(f"Tháng âm hiện tại ({_thang_am(am)}): từ {_ngan(dau_am)} đến {_ngan(cuoi_am)}.")
    return dong


def ket_qua(loai: Literal["hom_nay", "duong", "am"], ngay: int, thang: int, nam: int, thang_nhuan: bool, now: dt.datetime | None = None,
            cau: str = "") -> str:
    """Chữ trả cho model (do code dựng): luôn có dòng hôm nay; `loai` khác `hom_nay` ⇒ thêm dòng ngày được đổi. `nam` = 0 (không nêu năm) ⇒ cả lần gần nhất đã qua và lần sắp tới."""
    hom = hom_nay(now)
    dong = [f"Hôm nay (giờ Việt Nam): {mo_ta(hom)}.", *khoang_ngay(cau, hom)]
    lich = "âm" if loai == "am" else "dương"
    nhuan = ", tháng nhuận" if thang_nhuan else ""
    if loai != "hom_nay" and nam:
        d = ngay_duong(ngay, thang, nam, loai, thang_nhuan)
        chu = d if isinstance(d, str) else f"{mo_ta(d)} — {so_voi_hom_nay(d, hom)} (so với hôm nay)"
        dong.append(f"Ngày được hỏi ({lich} lịch {ngay}/{thang}/{nam}{nhuan}): {chu}")
    elif loai != "hom_nay":
        # review nhánh M-1 (A chọn 08/11): không nêu năm ⇒ KHÔNG đoán "năm nay" (từ 1/1 tới Tết năm âm ≠ năm dương: "Tết năm nay" sẽ thành Tết đã qua) ⇒ code
        # trả cả lần gần nhất đã qua (hoặc hôm nay) và lần sắp tới
        goc = solar_to_lunar(hom).year if loai == "am" else hom.year
        ngays = sorted({d for y in (goc - 1, goc, goc + 1) if isinstance(d := ngay_duong(ngay, thang, y, loai, thang_nhuan), dt.date)})
        qua = [d for d in ngays if d <= hom]
        toi = [d for d in ngays if d > hom]
        if not qua and not toi:
            dong.append(f"Ngày được hỏi ({lich} lịch {ngay}/{thang}{nhuan}): {ngay_duong(ngay, thang, goc, loai, thang_nhuan)}")
        if qua:
            dong.append(f"Ngày được hỏi ({lich} lịch {ngay}/{thang}{nhuan}) — lần gần nhất: {mo_ta(qua[-1])} — {so_voi_hom_nay(qua[-1], hom)} (so với hôm nay)")
        if toi:
            dong.append(f"Ngày được hỏi ({lich} lịch {ngay}/{thang}{nhuan}) — lần sắp tới: {mo_ta(toi[0])} — {so_voi_hom_nay(toi[0], hom)} (so với hôm nay)")
    return "\n".join(dong)


# Nguồn trong sổ nguồn (review plan M-2): câu trả lời chỉ có ngày (không đoạn kho) vẫn phải có [n] để qua bộ kiểm citation — như nguồn thời tiết
TIEU_DE_NGUON = "Lịch hệ thống — tính theo giờ Việt Nam"
MUC_NGUON = "Ngày và âm lịch Việt Nam"
NGUON_SOURCE = "he-thong-lich"  # `source` của nguồn — không thuộc tiền tố H4c, không phải bài kho (không `bai_id`)
