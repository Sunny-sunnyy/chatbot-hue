"""Bộ nhận số tiền trong chữ (Phase 9 B5, plan B5 bản 7 D8 (3), ý #1 nghiên cứu 04/11) — code chạy dùng chung (B5 kiểm cuối; B5c dùng lại).

Bắt mọi dạng hay gặp: "50.000đ", "50.000 đ", "1,5 triệu", "200k", "200.000 VNĐ", "300 nghìn". Không bắt: "3N2Đ" (chữ "Đ" hoa, theo sau số
ngày), "nghìn năm" / "nghìn người" / "nghìn lượt" / "nghìn bậc" (số đếm, không phải tiền). B5c (plan B5c D9): `tim_gia_tri` chuẩn hoá về số đồng ("1,5 triệu" = "1.500.000 đ"), kể cả cận thấp của khoảng "150.000–300.000 đồng".
"""
import re
import unicodedata

# số: 50.000 · 1,5 · 200 ; đơn vị: đồng / VNĐ / vnd / triệu / nghìn / ngàn (không phân biệt hoa thường) hoặc "đ" / "k" chữ thường đứng riêng
_SO_TIEN = re.compile(
    r"(?<![\w.,])\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s*"
    r"(?:(?i:đồng|vnđ|vnd|triệu)(?![\w])|(?i:nghìn|ngàn)(?!\s+(?:năm|người|lượt|bậc))(?![\w])|(?:đ|k)(?![\w]))"
)


def tim_so_tien(text: str) -> list[str]:
    """Mọi chuỗi số tiền trong `text`, theo thứ tự xuất hiện (rỗng = không có)."""
    return [m.group(0) for m in _SO_TIEN.finditer(unicodedata.normalize("NFC", text))]


# ---- B5c D9: giá trị số đồng ----
_SO_DAU = re.compile(r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?")
# cận thấp của khoảng: số không đơn vị đứng ngay trước "–" / "-" / "—" / "đến" / "tới" rồi một số tiền ("150.000–300.000 đồng", "1–1,5 triệu")
_CAN_THAP = re.compile(r"(?<![\w.,])(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)\s*(?:[-–—]|đến|tới)\s*$")


def _so_thuc(chuoi: str) -> float:
    """"150.000" / "1,500,000" ⇒ phân cách nghìn; "1,5" / "2.5" ⇒ phần thập phân (nhóm sau dấu không đủ 3 chữ số)."""
    phan = re.split(r"[.,]", chuoi)
    if len(phan) > 1 and all(len(x) == 3 for x in phan[1:]):
        return float("".join(phan))
    if len(phan) == 1:
        return float(phan[0])
    return float("".join(phan[:-1]) + "." + phan[-1])


def _he_so(chuoi_tien: str) -> int:
    t = chuoi_tien.strip().casefold()
    if "triệu" in t:
        return 1_000_000
    if "nghìn" in t or "ngàn" in t or t.endswith("k"):
        return 1_000
    return 1


def gia_tri_dong(chuoi_tien: str) -> int:
    """Một chuỗi `tim_so_tien` trả ⇒ số đồng."""
    return round(_so_thuc(_SO_DAU.match(chuoi_tien.strip()).group(0)) * _he_so(chuoi_tien))


def tim_gia_tri(text: str) -> list[int]:
    """Mọi số tiền trong `text` theo số đồng (thứ tự xuất hiện), gồm cận thấp không ghi đơn vị của khoảng (dùng đơn vị của cận cao)."""
    t = unicodedata.normalize("NFC", text)
    out: list[int] = []
    for m in _SO_TIEN.finditer(t):
        thap = _CAN_THAP.search(t[:m.start()])
        if thap:
            out.append(round(_so_thuc(thap.group(1)) * _he_so(m.group(0))))
        out.append(gia_tri_dong(m.group(0)))
    return out
