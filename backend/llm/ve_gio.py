"""T3 — bảng vé + giờ mở cửa có cấu trúc (plan `docs/superpowers/plans/2026-11-08-phase-9-t3-bang-plan.md` bản 2; spec Phase 9 bản 13 §12.5).

Phần code tất định (lõi `assistant.py` gọi): nạp bảng User duyệt (`bang_v1.json`, private — chỉ nạp khi cờ bật), khớp tên điểm, dựng **chữ gửi model**
(dòng giá là số + giờ + ngày nguồn), dựng **khối điều kiện** do code nối nguyên văn (dòng miễn phí / 0, điều kiện miễn giảm, quy định chung — **không**
vào model: bài học B5c), kiểm cuối số tiền + giờ trong chữ model. Không cộng / nhân. Mọi chuỗi hiển thị là chuỗi kho đã kiểm (`tools/kiem_nhap.py`);
trường `ghi_chu` của bảng là ghi chú của người dựng bảng — **không** hiện ra ngoài.
"""
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from llm.lich_trinh import chuan_ten
from llm.so_tien import tim_so_tien

MAX_DIEM = 5
THU_MUC_VE = "travel/tickets/"  # bảng ghi tên file vé không kèm thư mục
TIEU_DE_NGUON = "Bảng vé và giờ mở cửa"
CAU_NGOAI_BANG = "Bảng vé và giờ của hệ thống chưa có điểm này."  # không thấy ≠ không tồn tại
CAU_CO_DIEU_KIEN = "Có điều kiện miễn / giảm vé — hiện bên dưới câu trả lời (không nêu lại điều kiện)."
CAU_DAN_TU_CHOI = "Theo bảng vé và giờ trong nguồn dữ liệu:"  # có dòng bảng mà model từ chối (M-4) — khuôn thời tiết `CAU_DAN_DU_BAO`
CAU_MAU_THUAN = "Lưu ý: nguồn dữ liệu ghi khác nhau ở một số mục của {ten} — các dòng chép nguyên văn từng nguồn."
NHAN_GIO = {"gio_mo_cua": "giờ mở cửa", "gio_hoat_dong_kho_mo_ta": "giờ hoạt động (kho mô tả)"}

# Cổng đưa công cụ (plan m-2): ranh giới từ như `thoi_tiet._TU_KHOA`; "bây giờ / bao giờ / đánh giá / miễn là" không khớp.
_TU_KHOA = re.compile(
    r"\bvé\b|\bgiá\s+vé\b|\bbao\s+nhiêu\s+tiền\b|\bmất\s+tiền\b|\bphí\b|\bmở\s+cửa\b|\bđóng\s+cửa\b|\bmấy\s+giờ\b"
    r"|\bgiờ\s+(?:mở|đóng|tham\s+quan|hoạt\s+động)\b|\bmiễn\s+(?:giảm|phí|vé)\b|\bgiảm\s+(?:giá|vé|\d+\s*%)|\bưu\s+đãi\b",
    re.IGNORECASE)
# Câu hỏi về đối tượng ⇒ khối điều kiện đầy đủ; câu khác ⇒ một dòng "có điều kiện" (khối đủ của Quần thể dài ~40 dòng).
_HOI_DIEU_KIEN = re.compile(
    r"\bmiễn\b|\bgiảm\b|\bưu\s+đãi\b|\btrẻ\b|\bbé\b|\bcon\s+nhỏ\b|\btuổi\b|\bhọc\s+sinh\b|\bsinh\s+viên\b|\bcao\s+tuổi\b|\bngười\s+già\b"
    r"|\bkhuyết\s+tật\b|\bthương\s+binh\b|\bngười\s+có\s+công\b|\bhộ\s+nghèo\b|\bgiấy\s+tờ\b",
    re.IGNORECASE)
_MIEN_PHI = re.compile(r"^\s*(?:miễn\s+phí|0)\b", re.IGNORECASE)
_MUC_DIEU_KIEN_CHUNG = {"miễn phí", "giảm 50%", "trẻ em", "giảm (kích cầu)", "giấy tờ"}  # bỏ "hiệu lực" / "hoàn hủy" / "nguyên tắc" khỏi khối
# Giờ trong ngày (n-3): "7:30" · "7h30" · "7h" · "7 giờ 30" · "lúc / từ / đến … 7 giờ"; "mất 2 giờ" (thời lượng) **không** tính.
_GIO = re.compile(r"(?<![\d.,])(\d{1,2})\s*(?::|h(?=\s*\d|\b)|giờ\s+(?=\d))\s*(\d{2})?(?![\d,]|\.\d)", re.IGNORECASE)
_GIO_SAU_TU = re.compile(r"\b(?:lúc|từ|đến|tới|mở\s+cửa|đóng\s+cửa|trước|sau)\s+(\d{1,2})\s*giờ\b(?!\s*\d)", re.IGNORECASE)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _sach(text: str) -> str:
    """Chuỗi kho đã kiểm ⇒ chữ hiển thị: bỏ dấu in đậm / nghiêng Markdown, `<br>` ⇒ " / ", gộp khoảng trắng (không đổi chữ)."""
    return re.sub(r"\s+", " ", _nfc(text).replace("*", "").replace("<br>", " / ")).strip()


def _file_kho(file: str) -> str:
    return file if "/" in file else THU_MUC_VE + file


@dataclass(frozen=True)
class BangVeGio:
    diem: tuple[dict, ...]
    khoa: dict[str, int]  # tên / bí danh đã chuẩn hoá ⇒ vị trí điểm
    quy_dinh_chung: tuple[dict, ...]
    ap_dung_chung: frozenset[str]


def nap_bang(path: Path) -> BangVeGio:
    """Bảng User duyệt. Kiểm schema tối thiểu; tên / bí danh trùng giữa hai điểm ⇒ lỗi khởi động (khớp phải ra đúng một điểm)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    diem, khoa = tuple(data["diem"]), {}
    for i, d in enumerate(diem):
        for k in ("ten", "nhom", "ve", "gio", "mien_giam", "loai_gio"):
            if k not in d:
                raise ValueError(f"bảng vé / giờ: điểm {i} thiếu trường {k}")
        if d["loai_gio"] not in NHAN_GIO:
            raise ValueError(f"bảng vé / giờ: loai_gio lạ ở điểm {d['ten']}")
        for ten in (d["ten"], *d.get("bi_danh", ())):
            k = chuan_ten(ten)
            if khoa.get(k, i) != i:
                raise ValueError(f"bảng vé / giờ: tên «{ten}» trỏ hai điểm")
            khoa[k] = i
    chung = data.get("quy_dinh_chung_mien_giam") or {}
    return BangVeGio(diem=diem, khoa=khoa, quy_dinh_chung=tuple(chung.get("muc", ())), ap_dung_chung=frozenset(chung.get("ap_dung_nhom", ())))


def khop(bang: BangVeGio, ten: str) -> dict | None:
    i = bang.khoa.get(chuan_ten(ten))
    return None if i is None else bang.diem[i]


def co_tu_khoa(text: str) -> bool:
    return bool(_TU_KHOA.search(_nfc(text)))


def co_tu_khoa_luot(query: str, history) -> bool:
    """Câu cuối hoặc câu hỏi liền trước (khuôn `thoi_tiet.co_tu_khoa_luot`)."""
    return co_tu_khoa(query) or bool(history and co_tu_khoa(history[-1][0]))


def hoi_dieu_kien(query: str) -> bool:
    return bool(_HOI_DIEU_KIEN.search(_nfc(query)))


def _la_mien_phi(v: dict) -> bool:
    return bool(_MIEN_PHI.match(_sach(v.get("gia") or "")))


def dong_gui_model(d: dict) -> list[tuple[str, str]]:
    """(file kho, dòng chữ) gửi model cho một điểm — chỉ dòng giá là số + giờ + ngày nguồn (plan bản 2 bảng "trường nào đi đâu")."""
    out = []
    for v in d["ve"]:
        if v.get("gia") and not _la_mien_phi(v):
            nhan = " · ".join(_sach(x) for x in (v.get("loai"), v.get("doi_tuong")) if x)
            out.append((_file_kho(v["file"]), f"{d['ten']} — vé {nhan}: {_sach(v['gia'])}" + (f" {_sach(v['don_vi'])}" if v.get("don_vi") else "")))
    for g in d["gio"]:
        khi = " · ".join(_sach(x) for x in (g.get("muc"), g.get("mua_hoac_ngay")) if x)
        mo_dong = " – ".join(_sach(x) for x in (g.get("mo"), g.get("dong")) if x)
        if mo_dong:
            chung = " (giờ chung của Quần thể Di tích Cố đô Huế)" if g.get("gio_chung_quan_the") else ""
            out.append((_file_kho(g.get("file") or ""), f"{d['ten']} — {NHAN_GIO[d['loai_gio']]}{chung}" + (f" {khi}" if khi else "") + f": {mo_dong}"))
    for k in ("ngay_nguon_ve", "ngay_nguon_gio"):
        ng = d.get(k)
        if ng and out:
            out.append((_file_kho(ng.get("file") or ""), f"{d['ten']} — ngày nguồn: {_sach(ng['nguyen_van'])}"))
    return [(f, chu) for f, chu in out if f]


def co_dieu_kien(bang: BangVeGio, d: dict) -> bool:
    return bool(d["mien_giam"] or any(_la_mien_phi(v) for v in d["ve"]) or (d["nhom"] in bang.ap_dung_chung and bang.quy_dinh_chung))


def khoi_dieu_kien(bang: BangVeGio, diems: list[dict], day_du: bool) -> str | None:
    """Khối code nối dưới câu trả lời. `day_du` (câu hỏi về đối tượng) ⇒ điều kiện nguyên văn; không ⇒ một dòng chỉ có tên điểm. Thêm dòng
    "nguồn ghi khác nhau" khi điểm có mâu thuẫn (User 08/11 câu 1 (a))."""
    co = [d for d in diems if co_dieu_kien(bang, d)]
    mau = [d["ten"] for d in diems if d.get("mau_thuan")]
    if not co and not mau:
        return None
    dong: list[str] = []
    if co and day_du:
        dong.append("**Điều kiện miễn / giảm vé** (chép nguyên văn từ nguồn dữ liệu):")
        da: set[str] = set()

        def them(chu: str) -> None:
            chu = _sach(chu)
            if chu and chu not in da:
                da.add(chu)
                dong.append(f"- {chu}")

        for d in co:
            for v in d["ve"]:
                if _la_mien_phi(v):
                    them(f"{d['ten']} — {_sach(v.get('doi_tuong') or '')}: {_sach(v['gia'])}")
            for m in d["mien_giam"]:
                them(m["nguyen_van"])
        if any(d["nhom"] in bang.ap_dung_chung for d in co):
            for m in bang.quy_dinh_chung:
                if m.get("muc") in _MUC_DIEU_KIEN_CHUNG:
                    them(m["nguyen_van"])
    elif co:
        dong.append(f"Có điều kiện miễn / giảm vé cho một số đối tượng ở: {', '.join(d['ten'] for d in co)} — hỏi \"miễn giảm vé\" để xem nguyên văn.")
    dong += [CAU_MAU_THUAN.format(ten=t) for t in mau]
    return "\n".join(dong)


def _so_gio(text: str) -> set[tuple[int, int]]:
    text = _nfc(text)
    cap = {(int(h), int(m or 0)) for h, m in _GIO.findall(text)} | {(int(h), 0) for h in _GIO_SAU_TU.findall(text)}
    return {c for c in cap if c[0] <= 24 and c[1] < 60}


def _so_tien(text: str) -> set[str]:
    return {re.sub(r"\D", "", t) for t in tim_so_tien(text)}


def kiem_so(chu_model: str, cho_phep: str) -> list[str]:
    """Kiểm cuối (plan M-1, n-3): số tiền + giờ (so theo cặp giờ / phút đã chuẩn hoá: "7h30" ↔ "7:30") trong chữ model ⊂ số trong `cho_phep`
    (dòng đã gửi model + đoạn kho được trích + câu hỏi). Trả mã lỗi; rỗng = đạt."""
    loi = []
    if _so_tien(chu_model) - _so_tien(cho_phep):
        loi.append("tien_ngoai_bang")
    if _so_gio(chu_model) - _so_gio(cho_phep):
        loi.append("gio_ngoai_bang")
    return loi
