"""T3 hướng (a) — "phương án B" của spec Phase 9 §12.2 (User chọn 09/11/2026 sau khi vòng 3 âm ở sàn Q3).

Bảng vé + giờ User duyệt (`bang_v1.json`, private — chỉ nạp khi cờ bật) **không** đưa cho model (không công cụ, không tra trước, không khối điều kiện):
chỉ dùng **sau** khi model viết — code kiểm số tiền + giờ trong chữ model ⊂ {số trong dòng bảng của điểm nêu trong câu} ∪ {số trong đoạn kho đã đưa
model} ∪ {câu hỏi}; lệch ⇒ lõi nối một câu cố định (`CAU_CO_THE_KHAC`). Không cộng / nhân. Trường `ghi_chu` của bảng không dùng.
"""
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from llm.lich_trinh import chuan_ten
from llm.so_tien import tim_so_tien

# Câu cố định nối sau chữ model khi kiểm số lệch (spec §12.2 phương án B: "giá / giờ có thể khác — xem nguồn").
CAU_CO_THE_KHAC = ("Lưu ý: giá vé / giờ mở cửa nêu trên có chỗ chưa khớp bảng vé và nguồn dữ liệu, có thể khác thực tế — "
                   "hãy xem phần Nguồn hoặc hỏi nơi đến trước khi đi.")

# Cổng kiểm (khuôn cổng công cụ cũ, plan m-2): ranh giới từ như `thoi_tiet._TU_KHOA`; "bây giờ / bao giờ / đánh giá / miễn là" không khớp.
_TU_KHOA = re.compile(
    r"\bvé\b|\bgiá\s+vé\b|\bbao\s+nhiêu\s+tiền\b|\bmất\s+tiền\b|\bphí\b|\bmở\s+cửa\b|\bđóng\s+cửa\b|\bmấy\s+giờ\b"
    r"|\bgiờ\s+(?:mở|đóng|tham\s+quan|hoạt\s+động)\b|\bmiễn\s+(?:giảm|phí|vé)\b|\bgiảm\s+(?:giá|vé|\d+\s*%)|\bưu\s+đãi\b",
    re.IGNORECASE)
# Giờ trong ngày (n-3): "7:30" · "7h30" · "7h" · "7 giờ 30" · "lúc / từ / đến … 7 giờ"; "mất 2 giờ" (thời lượng) **không** tính.
# Ranh giới số (S05 09/11: "17:20, 18:00" — dấu phẩy + khoảng trắng là liệt kê, không phải số thập phân ⇒ bản cũ `(?![\d,]|\.\d)` bỏ mọi giờ đứng trước dấu
# phẩy): trước không là chữ số / "chữ số + . ,"; sau không là chữ số / ". ," + chữ số.
_TRUOC, _SAU = r"(?<!\d)(?<!\d[.,])", r"(?!\d|[.,]\d)"
_GIO = re.compile(_TRUOC + r"(\d{1,2})\s*(?::|h(?=\s*\d|\b)|giờ\s+(?=\d))\s*(\d{2})?" + _SAU, re.IGNORECASE)
_GIO_SAU_TU = re.compile(r"\b(?:lúc|từ|đến|tới|mở\s+cửa|đóng\s+cửa|trước|sau)\s+(\d{1,2})\s*giờ\b(?!\s*\d)", re.IGNORECASE)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _sach(text: str) -> str:
    """Chuỗi kho ⇒ chữ phẳng để tìm số: bỏ dấu in đậm / nghiêng Markdown, `<br>` ⇒ " / ", gộp khoảng trắng (không đổi chữ)."""
    return re.sub(r"\s+", " ", _nfc(text).replace("*", "").replace("<br>", " / ")).strip()


@dataclass(frozen=True)
class BangVeGio:
    diem: tuple[dict, ...]
    khoa: dict[str, int]  # tên / bí danh đã chuẩn hoá ⇒ vị trí điểm


def nap_bang(path: Path) -> BangVeGio:
    """Bảng User duyệt. Kiểm schema tối thiểu; tên / bí danh trùng giữa hai điểm ⇒ lỗi khởi động (khớp phải ra đúng một điểm)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    diem, khoa = tuple(data["diem"]), {}
    for i, d in enumerate(diem):
        for k in ("ten", "ve", "gio", "mien_giam"):
            if k not in d:
                raise ValueError(f"bảng vé / giờ: điểm {i} thiếu trường {k}")
        for ten in (d["ten"], *d.get("bi_danh", ())):
            k = chuan_ten(ten)
            if khoa.get(k, i) != i:
                raise ValueError(f"bảng vé / giờ: tên «{ten}» trỏ hai điểm")
            khoa[k] = i
    return BangVeGio(diem=diem, khoa=khoa)


def do_diem(bang: BangVeGio, text: str) -> list[dict]:
    """Tên / bí danh điểm của bảng **có trong chữ** người dùng (so sau chuẩn hoá như `chuan_ten`, ranh giới từ, khoá dài trước — khoá ngắn nằm trong
    khoá dài đã khớp thì bỏ; khoá < 4 ký tự bỏ). Trả điểm theo thứ tự xuất hiện."""
    t = " ".join(re.sub(r"[^\w]+", " ", _nfc(text).casefold()).split())
    da_che, gap = [False] * len(t), []
    for khoa_ten in sorted(bang.khoa, key=len, reverse=True):
        k = " ".join(re.sub(r"[^\w]+", " ", khoa_ten).split())
        if len(k) < 4:
            continue
        for m in re.finditer(rf"(?<!\w){re.escape(k)}(?!\w)", t):
            if not any(da_che[m.start():m.end()]):
                da_che[m.start():m.end()] = [True] * (m.end() - m.start())
                gap.append((m.start(), bang.khoa[khoa_ten]))
    out = []
    for _, i in sorted(gap):
        if bang.diem[i] not in out:
            out.append(bang.diem[i])
    return out


def co_tu_khoa(text: str) -> bool:
    return bool(_TU_KHOA.search(_nfc(text)))


def co_tu_khoa_luot(query: str, history) -> bool:
    """Câu cuối hoặc câu hỏi liền trước (khuôn `thoi_tiet.co_tu_khoa_luot`): "còn lăng Khải Định?" sau câu hỏi vé vẫn được kiểm."""
    return co_tu_khoa(query) or bool(history and co_tu_khoa(history[-1][0]))


def chu_cua_diem(d: dict) -> str:
    """Mọi chuỗi kho của một điểm trong bảng (giá, đơn vị, giờ, điều kiện miễn giảm, ngày nguồn) — tập số **được phép** khi kiểm chữ model."""
    phan = [str(v.get(k) or "") for v in d["ve"] for k in ("loai", "doi_tuong", "gia", "don_vi")]
    phan += [str(g.get(k) or "") for g in d["gio"] for k in ("muc", "mua_hoac_ngay", "mo", "dong")]
    phan += [m.get("nguyen_van") or "" for m in d["mien_giam"]]
    phan += [(d.get(k) or {}).get("nguyen_van") or "" for k in ("ngay_nguon_ve", "ngay_nguon_gio")]
    return " ".join(_sach(x) for x in phan if x)


def _so_gio(text: str) -> set[tuple[int, int]]:
    text = _nfc(text)
    cap = {(int(h), int(m or 0)) for h, m in _GIO.findall(text)} | {(int(h), 0) for h in _GIO_SAU_TU.findall(text)}
    return {c for c in cap if c[0] <= 24 and c[1] < 60}


def _so_tien(text: str) -> set[str]:
    return {re.sub(r"\D", "", t) for t in tim_so_tien(text)}


_NHOM_NGHIN = re.compile(_TRUOC + r"\d{1,3}(?:\.\d{3})+" + _SAU)  # "420.000" trần — ô bảng giá của kho thường không kèm "đồng"


def kiem_so(chu_model: str, cho_phep: str) -> list[str]:
    """Kiểm cuối (plan M-1, n-3): số tiền + giờ (so theo cặp giờ / phút đã chuẩn hoá: "7h30" ↔ "7:30") trong chữ model ⊂ số trong `cho_phep`
    (dòng bảng của điểm nêu trong câu + đoạn kho đã đưa model + câu hỏi). Phía cho phép nhận cả số nhóm nghìn **trần** (vòng 3, User duyệt 08/11: ô bảng giá trong kho
    ghi "420.000" không kèm "đồng" ⇒ `tim_so_tien` không nhận ⇒ rút lại oan một câu đúng — như thời tiết dùng `tap_so` cho mọi số). Trả mã lỗi."""
    loi = []
    cho_tien = _so_tien(cho_phep) | {re.sub(r"\D", "", x) for x in _NHOM_NGHIN.findall(_nfc(cho_phep))}
    if _so_tien(chu_model) - cho_tien:
        loi.append("tien_ngoai_bang")
    if _so_gio(chu_model) - _so_gio(cho_phep):
        loi.append("gio_ngoai_bang")
    return loi
