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
