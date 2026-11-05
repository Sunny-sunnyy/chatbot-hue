"""Dò số trong câu người dùng bằng luật code (Phase 9 B5, plan `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` bản 7 D12 (b), D15).

Một chỗ dò số dùng chung: B5 dò **số ngày**; B5c (plan `2026-11-05-phase-9-b5c-plan.md` D6) thêm số người vào đây. Không gọi model.
"""
import re
import unicodedata

CHU_SO = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6, "bảy": 7, "tám": 8, "chín": 9, "mười": 10}
_SO = r"(\d+|" + "|".join(CHU_SO) + r")"
# "3 ngày", "ba ngày", "3 ngày 2 đêm" (lấy số ngày) · "3N2Đ" / "3n2đ" (sau khi hạ chữ thường)
_NGAY = re.compile(r"(?<![\w])" + _SO + r"\s+ngày(?![\w])")
_NGAY_DEM_TAT = re.compile(r"(?<![\w])(\d+)\s*n\s*(\d+)\s*đ(?![\w])")


def _so(text: str) -> int:
    return int(text) if text.isdigit() else CHU_SO[text]


def gia_tri_so_ngay(n: int) -> str:
    """Số ngày ⇒ giá trị trường `so_ngay` của B4 ({1, 2, 3, 4+})."""
    return "4+" if n >= 4 else str(n)


def do_so_ngay(text: str) -> str | None:
    """Số ngày người dùng nêu trong `text` ⇒ "1" / "2" / "3" / "4+"; không thấy, hoặc thấy **nhiều giá trị khác nhau** ⇒ None (không đoán).
    "ngày thứ 2", "mỗi ngày" không phải số ngày (số phải đứng ngay trước chữ "ngày")."""
    t = unicodedata.normalize("NFC", text).casefold()
    so = {_so(m.group(1)) for m in _NGAY.finditer(t)} | {int(m.group(1)) for m in _NGAY_DEM_TAT.finditer(t)}
    so.discard(0)
    gia_tri = {gia_tri_so_ngay(n) for n in so}
    return gia_tri.pop() if len(gia_tri) == 1 else None


# Phase 9 B5b D9 (plan `2026-11-05-phase-9-b5b-plan.md` bản 2): ngày đi của lịch ⇒ số ngày tính từ hôm nay (0–6), cho dòng dự báo trong ghi chú.
_THU_SO = {"hai": 0, "ba": 1, "tư": 2, "năm": 3, "sáu": 4, "bảy": 5}
_MAI = re.compile(r"(?<![\w])(?:ngày\s+)?mai(?![\w])")
_NGAY_KIA = re.compile(r"(?<![\w])ngày\s+(?:kia|mốt)(?![\w])")
_THU = re.compile(r"(?<![\w])(?<!ngày )(?:thứ\s+(hai|ba|tư|năm|sáu|bảy)|(chủ\s+nhật))(?![\w])")  # "ngày thứ ba" = ngày 3 của chuyến, không phải thứ Ba
_CUOI_TUAN = re.compile(r"(?<![\w])cuối\s+tuần(?:\s+này)?(?![\w])")
_DD_MM = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?![\d/])")


def do_ngay_di(text: str, hom_nay) -> int | None:
    """Số ngày từ `hom_nay` (date, giờ Việt Nam) tới ngày đi người dùng nêu: "mai" 1 · "ngày kia / mốt" 2 · "thứ X" / "chủ nhật" lần tới gần nhất
    (hôm nay đúng thứ đó ⇒ 0) · "cuối tuần (này)" thứ Bảy gần nhất · "dd/mm" ⇒ đúng ngày. Ngoài 0–6, không thấy, hoặc thấy **nhiều giá trị khác
    nhau** ⇒ None (không đoán; lịch như B5)."""
    import datetime as _dt
    t = unicodedata.normalize("NFC", text).casefold()
    found = set()
    if _MAI.search(t):
        found.add(1)
    if _NGAY_KIA.search(t):
        found.add(2)
    for m in _THU.finditer(t):
        thu = 6 if m.group(2) else _THU_SO[m.group(1)]
        found.add((thu - hom_nay.weekday()) % 7)
    if _CUOI_TUAN.search(t):
        found.add((5 - hom_nay.weekday()) % 7)
    for d, mo in _DD_MM.findall(t):
        try:
            ngay = _dt.date(hom_nay.year, int(mo), int(d))
        except ValueError:
            continue
        found.add((ngay - hom_nay).days)
    if len(found) != 1:
        return None
    n = found.pop()
    return n if 0 <= n <= 6 else None
