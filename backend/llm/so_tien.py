"""Bộ nhận số tiền trong chữ (Phase 9 B5, plan B5 bản 7 D8 (3), ý #1 nghiên cứu 04/11) — code chạy dùng chung (B5 kiểm cuối; B5c dùng lại).

Bắt mọi dạng hay gặp: "50.000đ", "50.000 đ", "1,5 triệu", "200k", "200.000 VNĐ", "300 nghìn". Không bắt: "3N2Đ" (chữ "Đ" hoa, theo sau số
ngày), "nghìn năm" / "nghìn người" / "nghìn lượt" / "nghìn bậc" (số đếm, không phải tiền). Chỉ phát hiện; chưa chuẩn hoá giá trị (B5c thêm khi cần).
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
