"""Công cụ `goi_y_phuong_an_mua_nang` — gợi ý điểm trong nhà / có mái che phù hợp thời tiết (Đợt 2, cờ `goi_y_mua_nang`).

Chia việc code ↔ model:
- Code: chặn tuyệt đối khi là lượt bão/lũ (`thoi_tiet.la_luot_bao_lu` hoặc mưa cực đoan >= 100 mm/ngày), gọi chung `du_bao` (cache 30 phút Open-Meteo),
  lọc `diem_v16` theo `trong_nha in ("trong_nha", "ca_hai")`, `buoi`, `mua_luu_y` (`Thác Nhị Hồ` tháng 9–2) và `ngay_hoat_dong`, xếp ưu tiên cùng `cum`
  rồi cụm gần nhất theo `khoang_cach_v1`, trả tối đa 5 điểm thành một nguồn `[n]`.
- Model: ánh xạ ý người dùng sang enum (`tinh_huong`, `diem_goc`, `buoi`, `ngay`) và viết lời khuyên bám nguồn `[n]`.

Module thuần (không SDK, không gọi mạng trực tiếp); `assistant.py` bọc thành công cụ của một lượt.
"""
from __future__ import annotations

import datetime as dt
import re
import unicodedata

from llm import khoang_cach as kc
from llm import lich_trinh as lt
from llm import lich_trinh_v2 as lt2
from llm import thoi_tiet as tt

NGUON_SOURCE = "he-thong-mua-nang"
MUC_NGUON = "Gợi ý điểm đến phù hợp thời tiết"
TIEU_DE_NGUON = "Điểm trong nhà / có mái che phù hợp"
KHONG_RO = "khong_ro"
TINH_HUONG = ("mua", "nang_nong")
BUOI_LUA_CHON = ("sang", "chieu", "toi", "ca_ngay")
SO_TOI_DA = 5
SO_LAN_MOI_LUOT = 2
NGUONG_MUA_NGUY_HIEM = 100.0  # mm/ngày: mưa cực đoan cảnh báo ngập lụt -> chặn gợi ý đi chơi

CAU_CHAN_BAO_LU = (
    "Cảnh báo an toàn: đang có tình huống bão, lũ hoặc mưa ngập nguy hiểm — tuyệt đối không gợi ý lịch trình hay điểm đi chơi. "
    f"{tt.CAU_BAO_LU}"
)
CAU_KHONG_CO_DIEM = "Trong bảng điểm hiện tại chưa có điểm trong nhà hoặc có mái che phù hợp với buổi và điều kiện đã chọn."

_NHAN_TRONG_NHA = {
    "trong_nha": "trong nhà hoàn toàn",
    "ca_hai": "có cả khu trong nhà và ngoài trời",
}
_NHAN_THOI_LUONG = {
    "ngan": "ngắn (~1–1,5 giờ)",
    "nua_buoi": "nửa buổi (~2–2,5 giờ)",
}
_NHAN_TINH_HUONG = {
    "mua": "trời mưa",
    "nang_nong": "trời nắng nóng",
}

_Y_DINH_DI_CHOI = re.compile(
    r"(?<!\w)(?:đi\s+đâu|nên\s+đi|chơi\s+gì|chơi\s+đâu|có\s+gì\s+chơi|ghé\s+đâu|thay\s+(?:cho|bằng|điểm)|đổi\s+(?:điểm|lịch|chỗ)|"
    r"trong\s+nhà|mái\s+che|tránh\s+(?:mưa|nắng)|nắng\s+nóng|gợi\s+ý|tham\s+quan|chỗ\s+nào|điểm\s+nào)(?!\w)",
    re.IGNORECASE,
)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def co_tu_khoa_luot(query: str, history) -> bool:
    """Cổng từ khoá đưa công cụ: có từ khoá thời tiết VÀ ý định tìm/thay điểm đi chơi, KHÔNG phải lượt bão/lũ."""
    if tt.la_luot_bao_lu(query, history):
        return False
    if not tt.co_tu_khoa_luot_rong(query, history):
        return False
    return bool(_Y_DINH_DI_CHOI.search(_nfc(query))) or bool(history and _Y_DINH_DI_CHOI.search(_nfc(history[-1][0])))


def _khoang_cach_cum(bang: lt2.BangV2, bang_kc: kc.BangKhoangCach | None, cum_goc: str, cum_dich: str) -> float:
    if cum_dich == cum_goc:
        return 0.0
    if bang_kc is not None:
        cac_km = [
            bang_kc.cap[f"{a['id']}|{b['id']}"]["km"]
            for a in bang.diem
            for b in bang.diem
            if a["cum"] == cum_goc and b["cum"] == cum_dich and f"{a['id']}|{b['id']}" in bang_kc.cap
        ]
        if cac_km:
            return min(cac_km)
    return 10.0 if cum_dich in lt.CUM_KE.get(cum_goc, ()) else 999.0


def _khoang_cach_diem(bang: lt2.BangV2, bang_kc: kc.BangKhoangCach | None, diem_goc: str, diem_dich: dict) -> float:
    if bang_kc is not None:
        v = bang_kc.cap.get(f"{diem_goc}|{diem_dich['id']}") or bang_kc.cap.get(f"{diem_dich['id']}|{diem_goc}")
        if v is not None:
            return float(v["km"])
    return _khoang_cach_cum(bang, bang_kc, bang.theo_id[diem_goc]["cum"], diem_dich["cum"])


def _hop_mua_va_ngay(d: dict, ngay_muc_tieu: dt.date) -> bool:
    mua = d.get("mua_luu_y") or {}
    if mua.get("bo_khoi_lich") and ngay_muc_tieu.month in (mua.get("thang") or ()):
        return False
    ngay_hd = d.get("ngay_hoat_dong") or ()
    if ngay_hd and ngay_muc_tieu.weekday() not in ngay_hd:
        return False
    return True


def _hop_buoi(d: dict, buoi: str) -> bool:
    buois = set(d.get("buoi") or ())
    if buoi == "ca_ngay":
        return bool(buois & {"sang", "chieu"})
    return buoi in buois


def loc_diem(
    bang: lt2.BangV2,
    bang_kc: kc.BangKhoangCach | None,
    tinh_huong: str,
    diem_goc: str,
    buoi: str,
    ngay_muc_tieu: dt.date,
) -> list[dict]:
    """Lọc điểm `trong_nha`/`ca_hai` hợp buổi, hợp mùa (`mua_luu_y`), ưu tiên cùng cụm rồi cụm gần nhất."""
    del tinh_huong  # cả mưa và nắng nóng đều ưu tiên `trong_nha` trước `ca_hai`
    ung_vien = [
        d for d in bang.diem
        if d["id"] != diem_goc
        and d["trong_nha"] in ("trong_nha", "ca_hai")
        and _hop_buoi(d, buoi)
        and _hop_mua_va_ngay(d, ngay_muc_tieu)
    ]
    if diem_goc != KHONG_RO and diem_goc in bang.theo_id:
        goc_cum = bang.theo_id[diem_goc]["cum"]
        ung_vien.sort(key=lambda d: (
            0 if d["cum"] == goc_cum else 1,
            _khoang_cach_cum(bang, bang_kc, goc_cum, d["cum"]),
            _khoang_cach_diem(bang, bang_kc, diem_goc, d),
            0 if d["trong_nha"] == "trong_nha" else 1,
            (d.get("uu_tien") or {}).get("chung", 99),
            d["ten"],
        ))
    else:
        uu_cum = {"kinh_thanh": 0, "bo_nam": 0, "an_cuu": 1, "kim_long": 2, "thuy_xuan": 2}
        ung_vien.sort(key=lambda d: (
            0 if d["trong_nha"] == "trong_nha" else 1,
            (d.get("uu_tien") or {}).get("chung", 99),
            uu_cum.get(d["cum"], 3),
            d["ten"],
        ))
    return ung_vien[:SO_TOI_DA]


def _tom_tat_ngay_du_bao(kq: tt.DuBao, ngay: int) -> tuple[str | None, bool]:
    """Trả `(dòng tóm tắt dự báo ngày, có mức cảnh báo mưa cực đoan không)`."""
    if kq.trang_thai != "ok" or not (0 <= ngay < len(kq.ngay)):
        return None, False
    d = kq.ngay[ngay]
    co_canh_bao = d.get("mua") is not None and float(d["mua"]) >= NGUONG_MUA_NGUY_HIEM
    return f"Dự báo ngày {d['ngay']:%d/%m/%Y}: {tt.dong_ngay(d)} ({tt.GHI_CONG}).", co_canh_bao


def ket_qua(
    bang: lt2.BangV2,
    bang_kc: kc.BangKhoangCach | None,
    tinh_huong: str,
    diem_goc: str,
    buoi: str,
    ngay: int | None,
    kq_du_bao: tt.DuBao | None = None,
    hom_nay: dt.date | None = None,
) -> tuple[tuple[str, ...], list[dict], bool]:
    """Dựng `(các dòng nguồn, danh sách điểm chọn, bị chặn vì cảnh báo cực đoan)`."""
    hom = hom_nay or tt.hom_nay_vn()
    ngay_muc_tieu = hom + dt.timedelta(days=int(ngay)) if ngay is not None else hom

    dong_du_bao = None
    if ngay is not None and kq_du_bao is not None:
        dong_du_bao, nguy_hiem = _tom_tat_ngay_du_bao(kq_du_bao, int(ngay))
        if nguy_hiem:
            return (), [], True

    chon = loc_diem(bang, bang_kc, tinh_huong, diem_goc, buoi, ngay_muc_tieu)
    if not chon:
        return (CAU_KHONG_CO_DIEM,), [], False

    nhan_buoi = lt.NHAN_BUOI.get(buoi, "cả ngày").lower()
    moc_goc = f" (ưu tiên gần {bang.theo_id[diem_goc]['ten']})" if diem_goc in bang.theo_id else ""
    dong: list[str] = []
    if dong_du_bao:
        dong.append(dong_du_bao)
    dong.append(f"Gợi ý điểm tránh {_NHAN_TINH_HUONG.get(tinh_huong, tinh_huong)} cho buổi {nhan_buoi}{moc_goc}:")
    for d in chon:
        ten_cum = bang.cum.get(d["cum"], d["cum"])
        loai_tn = _NHAN_TRONG_NHA.get(d["trong_nha"], d["trong_nha"])
        tl = _NHAN_THOI_LUONG.get(d["thoi_luong"], d["thoi_luong"])
        kc_txt = ""
        if bang_kc is not None and diem_goc in bang.theo_id:
            v = bang_kc.cap.get(f"{diem_goc}|{d['id']}") or bang_kc.cap.get(f"{d['id']}|{diem_goc}")
            if v is not None:
                phut = int(v["phut"] * kc.HE_SO_OSRM + 0.5) + kc.PHUT_CONG
                kc_txt = f"; cách điểm gốc {kc._km(v['km'])}, {kc._phut(phut)}"
        luu_y = f" (lưu ý: {d['luu_y']})" if d.get("luu_y") else ""
        dong.append(f"- {d['ten']}: {loai_tn}; khu vực {ten_cum}; thời lượng {tl}{kc_txt}{luu_y}.")
    if diem_goc in bang.theo_id and any("cách điểm gốc" in line for line in dong):
        dong.append(kc.CAU_GHI_CHU)
    return tuple(dong), chon, False


def mo_ta_cong_cu(bang: lt2.BangV2) -> str:
    """Mô tả công cụ ngắn gọn kèm danh sách mã điểm hợp lệ."""
    ds = "; ".join(f"{d['id']}={d['ten']}" for d in bang.diem)
    return (
        "Gợi ý điểm tham quan trong nhà hoặc có mái che ở Huế khi trời mưa hoặc nắng nóng, lọc theo buổi và ưu tiên gần điểm gốc. "
        "KHÔNG dùng khi người dùng hỏi bão, lũ, ngập lụt hoặc thời tiết nguy hiểm (giữ cảnh báo an toàn 112). "
        f"tinh_huong = mua | nang_nong; buoi = sang | chieu | toi | ca_ngay; ngay = 0..6 (0=hôm nay) hoặc null; "
        f"diem_goc = mã điểm gốc nếu có hoặc \"{KHONG_RO}\". "
        "Kết quả là một nguồn [n]: chỉ gợi ý các điểm có trong nguồn này và trích mã [n]; cần giờ mở cửa hay chi tiết bài thì gọi thêm tim_kho.\n"
        f"Mã điểm: {ds}."
    )
