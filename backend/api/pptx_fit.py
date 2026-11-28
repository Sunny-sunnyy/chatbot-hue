"""Đo tràn chữ hình học tiếng Việt có dấu (3 tầng) & cắt ảnh trung tâm không méo cho `.pptx` v2 (`Đợt 5 — Phần A`)."""
import io
import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

from api.pptx_catalog import LAYOUT_SPECS

MARGIN_H_IN = 0.08
MARGIN_V_IN = 0.08
LINE_SPACING = 1.22
VI_SAFETY = 1.08  # hệ số dự phòng cho chữ hoa + dấu tiếng Việt


@dataclass(frozen=True)
class OverflowErrorItem:
    slide_index: int
    slot_id: str
    excess_chars: int
    max_chars_approx: int
    estimated_lines: int
    max_lines: int

    def to_dict(self) -> dict:
        return {
            "slide_index": self.slide_index,
            "slot_id": self.slot_id,
            "excess_chars": self.excess_chars,
            "max_chars_approx": self.max_chars_approx,
            "estimated_lines": self.estimated_lines,
            "max_lines": self.max_lines,
        }


def _chars_per_line(width_in: float, font_pt: float) -> int:
    usable_w = max(0.25, width_in - MARGIN_H_IN)
    avg_char_w_in = (font_pt * 0.54 / 72.0) * VI_SAFETY
    return max(4, int(usable_w // avg_char_w_in))


def _max_lines(height_in: float, font_pt: float, line_spacing: float = LINE_SPACING) -> int:
    usable_h = max(0.15, height_in - MARGIN_V_IN)
    line_h_in = (font_pt * line_spacing) / 72.0
    return max(1, int(usable_h // line_h_in))


def wrap_lines(text: str, width_in: float, font_pt: float) -> list[str]:
    """Mô phỏng xuống dòng theo từ trên độ rộng thực của hộp chữ."""
    chu = str(text or "").strip()
    if not chu:
        return []
    cap = _chars_per_line(width_in, font_pt)
    dong_ra: list[str] = []
    for doan in chu.splitlines():
        doan = " ".join(doan.split())
        if not doan:
            dong_ra.append("")
            continue
        cur = ""
        for tu in doan.split(" "):
            if not cur:
                if len(tu) <= cap:
                    cur = tu
                else:
                    for i in range(0, len(tu), cap):
                        dong_ra.append(tu[i:i + cap])
                    cur = ""
            elif len(cur) + 1 + len(tu) <= cap:
                cur = f"{cur} {tu}"
            else:
                dong_ra.append(cur)
                if len(tu) <= cap:
                    cur = tu
                else:
                    for i in range(0, len(tu), cap):
                        part = tu[i:i + cap]
                        if i + cap < len(tu):
                            dong_ra.append(part)
                        else:
                            cur = part
        if cur:
            dong_ra.append(cur)
    return dong_ra


def tinh_so_dong(text: str, width_in: float, font_pt: float) -> int:
    return len(wrap_lines(text, width_in, font_pt))


def co_chu_vua_khung(
    text: str,
    width_in: float,
    height_in: float,
    base_pt: float,
    min_pt: float,
    *,
    line_spacing: float = LINE_SPACING,
) -> tuple[float, bool, int, int]:
    """Tầng 1: co cỡ chữ từng bước `0.5pt` từ `base_pt` xuống `min_pt` tới khi vừa hộp."""
    pt = float(base_pt)
    min_p = float(min_pt)
    while pt >= min_p - 1e-6:
        cur_pt = round(max(pt, min_p), 1)
        est = tinh_so_dong(text, width_in, cur_pt)
        cap_lines = _max_lines(height_in, cur_pt, line_spacing=line_spacing)
        if est <= cap_lines:
            return cur_pt, True, est, cap_lines
        if cur_pt <= min_p:
            return cur_pt, False, est, cap_lines
        pt -= 0.5
    cur_pt = round(min_p, 1)
    est = tinh_so_dong(text, width_in, cur_pt)
    cap_lines = _max_lines(height_in, cur_pt, line_spacing=line_spacing)
    return cur_pt, est <= cap_lines, est, cap_lines


def cat_sach_ranh_gioi(
    text: str,
    width_in: float,
    height_in: float,
    font_pt: float,
    *,
    line_spacing: float = LINE_SPACING,
) -> str:
    """Tầng 3: cắt sạch ở ranh giới câu / từ cuối vừa khít hộp và nối `…`."""
    chu = " ".join(str(text or "").split())
    if not chu:
        return ""
    cap_lines = _max_lines(height_in, font_pt, line_spacing=line_spacing)
    lines = wrap_lines(chu, width_in, font_pt)
    if len(lines) <= cap_lines:
        return chu
    cap_chars = max(12, _chars_per_line(width_in, font_pt) * cap_lines - 2)
    cat = chu[:cap_chars].rsplit(" ", 1)[0].rstrip(",;:—- ")
    if not cat:
        cat = chu[:cap_chars].rstrip()
    while cat and tinh_so_dong(cat + "…", width_in, font_pt) > cap_lines:
        if " " not in cat:
            cat = cat[:-1]
        else:
            cat = cat.rsplit(" ", 1)[0].rstrip(",;:—- ")
    return (cat + "…") if cat else chu[:max(4, cap_chars - 1)] + "…"


def kiem_tra_slot(
    slide_index: int,
    layout_id: str,
    slot_id: str,
    text: str | None,
    *,
    width_in: float | None = None,
    height_in: float | None = None,
    base_pt: float | None = None,
    min_pt: float | None = None,
) -> tuple[float, OverflowErrorItem | None]:
    """Kiểm tra một slot theo `LAYOUT_SPECS` (hoặc kích thước truyền trực tiếp). Trả `(font_pt, error_or_None)`."""
    spec = LAYOUT_SPECS.get(layout_id, {}).get(slot_id)
    if spec is None and (width_in is None or height_in is None or base_pt is None or min_pt is None):
        return 11.0, None
    w = width_in if width_in is not None else spec[0]
    h = height_in if height_in is not None else spec[1]
    b_pt = base_pt if base_pt is not None else spec[2]
    m_pt = min_pt if min_pt is not None else spec[3]
    chu = str(text or "").strip()
    if not chu:
        return b_pt, None
    pt, fits, est, cap = co_chu_vua_khung(chu, w, h, b_pt, m_pt)
    if fits:
        return pt, None
    approx = max(10, _chars_per_line(w, m_pt) * cap)
    excess = max(1, len(chu) - approx)
    return pt, OverflowErrorItem(
        slide_index=slide_index,
        slot_id=slot_id,
        excess_chars=excess,
        max_chars_approx=approx,
        estimated_lines=est,
        max_lines=cap,
    )


def kiem_tra_tran_chu(slides: list[dict]) -> list[dict]:
    """Tầng 2: quét toàn bộ chuỗi trang (dạng đã chuẩn hoá hoặc bán chuẩn hoá), trả danh sách `overflow_errors`."""
    errors: list[dict] = []
    for idx, sl in enumerate(slides, start=1):
        lay = sl.get("layout_id") or ""
        kieu = sl.get("kieu")
        if kieu == "bia":
            for slot, val in (
                ("title", sl.get("tieu_de")),
                ("subtitle", sl.get("tom_tat")),
                ("highlights", "\n".join(sl.get("diem_chinh") or [])),
                ("an_toan", sl.get("an_toan")),
            ):
                _, err = kiem_tra_slot(idx, lay, slot, val)
                if err:
                    errors.append(err.to_dict())
        elif kieu == "ngay":
            for slot, val in (("day_header", sl.get("ngay_tieu_de")), ("route_summary", sl.get("chang"))):
                _, err = kiem_tra_slot(idx, lay, slot, val)
                if err:
                    errors.append(err.to_dict())
            for m in sl.get("muc") or []:
                _, err_t = kiem_tra_slot(idx, lay, "item_title", m.get("ten"))
                if err_t:
                    errors.append({**err_t.to_dict(), "id_muc": m.get("id_muc")})
                copy_text = "\n".join(x for x in (m.get("cau"), m.get("ghi_chu")) if x)
                _, err_c = kiem_tra_slot(idx, lay, "item_copy", copy_text)
                if err_c:
                    errors.append({**err_c.to_dict(), "id_muc": m.get("id_muc")})
        elif kieu == "luu_y":
            _, err_at = kiem_tra_slot(idx, lay, "an_toan", sl.get("an_toan_cau"))
            if err_at:
                errors.append(err_at.to_dict())
            body = "\n".join("•  " + d for d in (sl.get("dong") or []) if d != sl.get("an_toan_cau"))
            _, err_b = kiem_tra_slot(idx, lay, "notes_body", body)
            if err_b:
                errors.append(err_b.to_dict())
    return errors


def crop_anh_giua(image_path: Path, target_w_in: float, target_h_in: float) -> io.BytesIO | None:
    """Mở ảnh bằng Pillow, cắt chính giữa đúng tỷ lệ khung `(target_w_in / target_h_in)` để tránh méo > 5% trên mọi trình chiếu."""
    if not image_path or not image_path.is_file() or target_w_in <= 0 or target_h_in <= 0:
        return None
    with Image.open(image_path) as raw:
        img = ImageOps.exif_transpose(raw)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        w, h = img.size
        if w <= 0 or h <= 0:
            return None
        target_ratio = target_w_in / target_h_in
        cur_ratio = w / h
        if cur_ratio > target_ratio:
            new_w = max(1, int(round(h * target_ratio)))
            left = max(0, (w - new_w) // 2)
            box = (left, 0, min(w, left + new_w), h)
        elif cur_ratio < target_ratio:
            new_h = max(1, int(round(w / target_ratio)))
            top = max(0, (h - new_h) // 2)
            box = (0, top, w, min(h, top + new_h))
        else:
            box = (0, 0, w, h)
        cropped = img.crop(box)
        buf = io.BytesIO()
        fmt = "PNG" if cropped.mode == "RGBA" else "JPEG"
        if fmt == "JPEG":
            cropped.save(buf, format="JPEG", quality=90)
        else:
            cropped.save(buf, format="PNG")
        buf.seek(0)
        return buf
