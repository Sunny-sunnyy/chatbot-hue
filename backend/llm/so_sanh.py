"""Công cụ `so_sanh_diem_den` — so sánh đa tiêu chí 2–3 điểm đến từ dữ liệu cấu trúc sẵn có (Đợt 2, cờ `so_sanh_diem_den`).

Chia việc code ↔ model:
- Code: nhận 2–3 mã điểm enum từ `diem_v16`, kiểm tra tối thiểu 2 mã khác nhau (trả actionable feedback nếu thiếu), dựng bảng so sánh gồm
  `cum`, `thoi_luong`, `trong_nha`, `bac_thang`, giờ mở cửa & giá vé lẻ lấy nguyên văn từ `the_noi_bang` (tuyệt đối KHÔNG đọc ghi chú nội bộ
  `gio_mo_cua` trong `diem_v16`), và khoảng cách đường đi từ `khoang_cach_bang`, đăng thành 1 nguồn `[n]`.
- Model: ánh xạ câu hỏi so sánh thực dụng sang 2–3 mã điểm và tổng hợp câu trả lời bám đúng `[n]`; dùng thêm `tim_kho` nếu câu hỏi cần chiều sâu
  văn hoá/kiến trúc không có trong bảng.

Module thuần (không SDK, không gọi mạng); `assistant.py` bọc thành công cụ của một lượt.
"""
from __future__ import annotations

from collections.abc import Sequence
import re
import unicodedata

from llm import khoang_cach as kc
from llm import lich_trinh_v2 as lt2
from llm import the_noi as thn

NGUON_SOURCE = "he-thong-so-sanh"
MUC_NGUON = "So sánh thuộc tính thực dụng từ dữ liệu hệ thống"
TIEU_DE_NGUON = "Bảng đối chiếu các điểm đến"
KHONG_CO = "khong_co"
SO_LAN_MOI_LUOT = 2

CAU_THIEU_DIEM = (
    "Trạng thái: cần ít nhất 2 điểm khác nhau trong danh sách để so sánh. "
    "Nếu một điểm nằm ngoài danh sách hoặc người dùng hỏi so sánh lịch sử, kiến trúc chuyên sâu, hãy dùng công cụ tim_kho."
)

THOI_LUONG_NHAN = {
    "ngan": "ngắn (~1–1,5 giờ)",
    "nua_buoi": "nửa buổi (~2–2,5 giờ)",
}
TRONG_NHA_NHAN = {
    "trong_nha": "trong nhà",
    "ngoai_troi": "ngoài trời",
    "ca_hai": "kết hợp trong nhà và ngoài trời",
}

_TU_KHOA = re.compile(
    r"(?<!\w)(?:so\s+sánh|khác\s+gì|khác\s+nhau|hợp\s+hơn|tiện\s+hơn|dễ\s+đi\s+hơn|ít\s+bậc|nhiều\s+bậc|"
    r"bậc\s+thang|người\s+(?:già|lớn\s+tuổi|cao\s+tuổi)|trẻ\s+(?:nhỏ|em)|xe\s+lăn)(?!\w)"
    r"|\bnên\s+(?:đi|chọn)\b[^.?!\n]{1,60}\bhay\b"
    r"|\bgiữa\b[^.?!\n]{1,60}\bvới\b",
    re.IGNORECASE,
)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def co_tu_khoa_luot(query: str, history) -> bool:
    """Cổng từ khoá đưa công cụ: câu cuối hoặc câu hỏi liền trước có dấu hiệu so sánh / tiêu chí đi lại."""
    return bool(_TU_KHOA.search(_nfc(query))) or bool(history and _TU_KHOA.search(_nfc(history[-1][0])))


def chuan_danh_sach_ma(bang: lt2.BangV2, raw_ids: Sequence[str | None]) -> tuple[str, ...]:
    """Lọc mã hợp lệ có trong `bang.theo_id`, bỏ `khong_co`/`None` và bỏ trùng theo thứ tự xuất hiện."""
    out: list[str] = []
    for raw in raw_ids:
        if not raw or raw == KHONG_CO or raw not in bang.theo_id:
            continue
        if raw not in out:
            out.append(raw)
    return tuple(out)


def _khoang_cach_cap(bang_kc: kc.BangKhoangCach | None, a: str, b: str) -> tuple[float, int] | None:
    if bang_kc is None:
        return None
    v = bang_kc.cap.get(f"{a}|{b}") or bang_kc.cap.get(f"{b}|{a}")
    if v is None:
        return None
    phut = int(v["phut"] * kc.HE_SO_OSRM + 0.5) + kc.PHUT_CONG
    return float(v["km"]), phut


def ket_qua(
    bang: lt2.BangV2,
    bang_kc: kc.BangKhoangCach | None,
    the_noi_bang: thn.Bang | None,
    raw_ids: Sequence[str | None],
) -> tuple[tuple[str, ...], tuple[dict, ...]]:
    """Trả `(các dòng nguồn, danh sách điểm hợp lệ)` — dưới 2 điểm trả `((), ())` để tool trả `CAU_THIEU_DIEM`."""
    ids = chuan_danh_sach_ma(bang, raw_ids)
    if len(ids) < 2:
        return (), ()

    noi_theo_rel = {n.rel: n for n in the_noi_bang.noi} if the_noi_bang is not None else {}
    chon = tuple(bang.theo_id[i] for i in ids)
    dong: list[str] = [f"So sánh {' và '.join(d['ten'] for d in chon)}:"]
    co_ve = False

    for d in chon:
        cum = bang.cum.get(d["cum"], d["cum"])
        tl = THOI_LUONG_NHAN.get(d["thoi_luong"], d["thoi_luong"])
        tn = TRONG_NHA_NHAN.get(d["trong_nha"], d["trong_nha"])
        bac = "nhiều bậc thang (cân nhắc khi đi cùng người lớn tuổi / trẻ nhỏ)" if d.get("bac_thang") == "nhieu" else "không thuộc nhóm nhiều bậc thang"
        chi_tiet = [f"khu vực {cum}", f"thời lượng {tl}", f"không gian {tn}", f"bậc thang: {bac}"]

        noi = noi_theo_rel.get(d["nguon"])
        if noi is not None and noi.dong:
            chi_tiet.extend(noi.dong)
        if noi is not None and noi.ve:
            co_ve = True
            chi_tiet.append(f"vé lẻ tham khảo: {noi.ve}")
        if noi is None or (not noi.dong and not noi.ve):
            chi_tiet.append("giờ mở cửa/vé: chưa có trong thẻ tóm tắt (dùng tim_kho nếu cần)")
        dong.append(f"- {d['ten']}: {'; '.join(chi_tiet)}.")

    if co_ve and the_noi_bang is not None and the_noi_bang.ve_dau:
        dong.append(f"Cột bảng vé lẻ ({the_noi_bang.ve_tieu_de}): {the_noi_bang.ve_dau}")

    kc_dong: list[str] = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            cap = _khoang_cach_cap(bang_kc, a, b)
            if cap is not None:
                km, phut = cap
                kc_dong.append(f"- Đường đi {bang.theo_id[a]['ten']} ↔ {bang.theo_id[b]['ten']}: {kc._km(km)}, khoảng {kc._phut(phut)}.")
    if kc_dong:
        dong.extend(kc_dong)
        dong.append(kc.CAU_GHI_CHU)

    return tuple(dong), chon


def mo_ta_cong_cu(bang: lt2.BangV2) -> str:
    """Mô tả công cụ ngắn gọn kèm danh sách mã điểm hợp lệ."""
    ds = "; ".join(f"{d['id']}={d['ten']}" for d in bang.diem)
    return (
        "So sánh 2 đến 3 điểm đến ở Huế theo tiêu chí thực dụng (khu vực, thời lượng, trong nhà/ngoài trời, nhiều bậc thang, giờ/vé tóm tắt từ kho, khoảng cách). "
        "KHÔNG dùng cho so sánh thuần lịch sử/kiến trúc hoặc điểm ngoài danh sách (dùng tim_kho). "
        f"Truyền diem_1, diem_2 và diem_3 (\"{KHONG_CO}\" hoặc null nếu chỉ so sánh 2 điểm). "
        "Kết quả là một nguồn [n]: bám đúng thuộc tính và trích mã [n]; cần chiều sâu văn hoá/lịch sử thì gọi thêm tim_kho.\n"
        f"Mã điểm: {ds}."
    )
