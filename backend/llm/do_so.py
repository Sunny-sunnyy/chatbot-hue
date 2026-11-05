"""Dò số trong câu người dùng bằng luật code (Phase 9 B5, plan `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` bản 7 D12 (b), D15).

Một chỗ dò số dùng chung: B5 dò **số ngày**; B5c (plan `2026-11-05-phase-9-b5c-plan.md` D6) thêm số người vào đây. Không gọi model.
"""
import re
import unicodedata
from dataclasses import dataclass

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


# ---- B5c (plan `2026-11-05-phase-9-b5c-plan.md` D6): số người + kiểm "X ngày Y đêm" cho dự toán ----
MAX_NGUOI = 20  # D7: `TruongInput.so_nguoi` 1–20; dò được > 20 ⇒ ngoài phạm vi
_NGAY_DEM = re.compile(r"(?<![\w])" + _SO + r"\s+ngày\s+" + _SO + r"\s+đêm(?![\w])")
_NUA_NGAY = re.compile(r"(?<![\w])nửa\s+ngày(?![\w])")
_NGUOI_LON = re.compile(r"(?<![\w])" + _SO + r"\s+người\s+lớn(?![\w])")
_TRE = re.compile(r"(?<![\w])" + _SO + r"\s+(?:trẻ\s+em|trẻ\s+nhỏ|trẻ|em\s+bé|bé|cháu|con|đứa\s+nhỏ|đứa\s+trẻ)(?![\w])")
_TU_TRE = re.compile(r"(?<![\w])(?:trẻ\s+em|trẻ\s+nhỏ|em\s+bé|con\s+nhỏ|đứa\s+nhỏ|đứa\s+trẻ|bé|cháu)(?![\w])")  # có nhắc trẻ (kể cả không số)
_CAP = re.compile(r"(?<![\w])(?:vợ\s+chồng|cặp\s+đôi)(?![\w])")
_MOT_MINH = re.compile(r"(?<![\w])(?:một\s+mình|mình\s+tôi)(?![\w])")
_NGUOI = re.compile(r"(?<![\w])" + _SO + r"\s+(?:người|khách|thành\s+viên|(?:đứa\s+)?bạn|đứa)(?![\w])")


@dataclass(frozen=True)
class SoNguoi:
    """Kết quả dò số người. `tong` cho dự toán (D3: người lớn + trẻ em); `nguoi_lon` / `tre_em` cho vé (D2b). None = không dò được / mơ hồ.
    `tre_em` = 0 khi câu nêu số người lớn mà không nhắc trẻ; None khi có nhắc trẻ mà không có số (D2b: không tính tổng vé trẻ)."""
    tong: int | None = None
    nguoi_lon: int | None = None
    tre_em: int | None = None

    @property
    def qua_gioi_han(self) -> bool:
        return self.tong is not None and self.tong > MAX_NGUOI


def _mot_gia_tri(values: set[int]) -> int | None:
    return values.pop() if len(values) == 1 else None


def do_so_nguoi(text: str) -> SoNguoi:
    """Số người người dùng nêu trong `text` (D6). Nhiều giá trị khác nhau cho cùng trường ⇒ None (không đoán). "cả nhà", "nhóm mình" ⇒ None."""
    t = unicodedata.normalize("NFC", text).casefold()
    lon = {_so(m.group(1)) for m in _NGUOI_LON.finditer(t)} | ({2} if _CAP.search(t) else set()) | ({1} if _MOT_MINH.search(t) else set())
    tre_khop = list(_TRE.finditer(t))
    tre = {_so(m.group(1)) for m in tre_khop}
    # đếm chung ("4 người", "5 đứa bạn") sau khi che phần đã đọc là người lớn / trẻ em
    che = _TRE.sub(" ", _NGUOI_LON.sub(" ", t))
    chung = {_so(m.group(1)) for m in _NGUOI.finditer(che)}
    n_lon, n_tre = _mot_gia_tri(lon), _mot_gia_tri(tre)
    if len(lon) > 1 or len(tre) > 1:
        return SoNguoi()
    co_tre_khong_so = len(_TU_TRE.findall(che)) > 0
    if n_lon is None and n_tre is None:
        return SoNguoi(tong=_mot_gia_tri(chung))
    if n_lon is None:  # chỉ có số trẻ ("vé cho 2 bé"): không biết người lớn
        return SoNguoi(tong=None, nguoi_lon=None, tre_em=n_tre)
    if n_tre is None and co_tre_khong_so:
        return SoNguoi(tong=None, nguoi_lon=n_lon, tre_em=None)
    tong = n_lon + (n_tre or 0)
    if chung and chung != {tong}:  # "nhóm 5 người, 2 người lớn" — mâu thuẫn ⇒ không đoán
        return SoNguoi()
    return SoNguoi(tong=tong, nguoi_lon=n_lon, tre_em=n_tre or 0)


def do_ngay_du_toan(text: str) -> tuple[str | None, str | None]:
    """Số ngày cho dự toán (D2, D6) ⇒ (giá trị `so_ngay` hoặc None, mã ngoài phạm vi hoặc None). "nửa ngày" ⇒ `nua_ngay`; "X ngày Y đêm" /
    "XnYđ" có Y ≠ X − 1 ⇒ `dem_lech` (kho chỉ có 1 ngày / 2N1Đ / 3N2Đ). Số ngày lấy như `do_so_ngay` (B5)."""
    t = unicodedata.normalize("NFC", text).casefold()
    if _NUA_NGAY.search(t):
        return None, "nua_ngay"
    cap = [(_so(m.group(1)), _so(m.group(2))) for m in _NGAY_DEM.finditer(t)]
    cap += [(int(m.group(1)), int(m.group(2))) for m in _NGAY_DEM_TAT.finditer(t)]
    if any(dem != ngay - 1 for ngay, dem in cap):
        return None, "dem_lech"
    return do_so_ngay(text), None
