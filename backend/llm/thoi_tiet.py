"""Thời tiết Huế (Phase 9 B5b, plan `docs/superpowers/plans/2026-11-05-phase-9-b5b-plan.md` bản 2 `cc09fda9f634`).

Module **duy nhất** gọi Open-Meteo (test ranh giới cho phép `httpx` ở đây). Mọi số thời tiết người dùng thấy do **code** in (D5) — model chỉ hiểu
"mai / cuối tuần" ⇒ số ngày (D3) và viết lời quanh khối. Yêu cầu ra ngoài chỉ có toạ độ cố định + tham số do code dựng (D2) — không chữ người dùng.
- `co_tu_khoa` (D4): công cụ chỉ được đưa khi câu cuối hoặc câu hỏi liền trước có từ khoá thời tiết (so cả từ).
- `lay_du_bao` (D7): một lần gọi, hết giờ 3 s, không thử lại; lỗi / sai schema / số ngoài miền ⇒ "loi" (không bao giờ đưa số); cache RAM 30 phút.
- `khoi_du_bao` (D5): câu số liệu cố định + ghi công Open-Meteo + "số liệu lúc HH:MM"; `so_cho_phep` = đúng các chuỗi số code đã in.
- `so_thoi_tiet` / `kiem_so` (D8): số dạng thời tiết trong chữ model phải ∈ số code đưa ∪ số trong đoạn kho được trích.
- Câu cố định bão / lũ (D6), ngoài 7 ngày (D3), "theo cả ngày" (D5), lỗi API (D7) — do code nối.
"""
import re
import time
import unicodedata
from dataclasses import dataclass, field
from datetime import date

import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
HUE_LAT, HUE_LON = 16.4637, 107.5909  # D2: một điểm trung tâm TP Huế, cố định trong code
TIMEOUT_S = 3.0
CACHE_S = 30 * 60
SO_NGAY = 7  # dự báo hôm nay + 6 ngày tới (tham số công cụ 0–6)
NGUONG_MUA = 60  # D9: khả năng mưa ≥ 60 % ⇒ dòng "Nếu mưa"
MIEN = {"tmax": (-10, 50), "tmin": (-10, 50), "xs": (0, 100), "mua": (0, 1000)}  # D7: số ngoài miền ⇒ lỗi

GHI_CONG = "Dữ liệu thời tiết: Open-Meteo.com (CC BY 4.0)"
NCHMF_URL = "https://nchmf.gov.vn"
LU_QUET_URL = "https://luquetsatlo.nchmf.gov.vn"
TIEU_DE = "**Dự báo thời tiết Huế**"
# E17 (A chọn): kết quả công cụ là một nguồn trong sổ nguồn — model trích [k]; khung nguồn của giao diện hiện nguồn này
TIEU_DE_NGUON = "Dự báo thời tiết Huế (Open-Meteo)"
TIEU_DE_NGUON_LOI = "Dự báo thời tiết Huế — chưa lấy được"
MUC_NGUON = "Dự báo 7 ngày tới"
NGUON_SOURCE = "open-meteo"  # `source` của nguồn — không thuộc tiền tố H4c (vé / điểm đến / lễ hội)
CAU_LOI = f"Mình chưa lấy được dự báo thời tiết lúc này — bạn xem bản tin của Trung tâm Dự báo khí tượng thủy văn quốc gia: {NCHMF_URL}"
CAU_BAO_LU = (f"Với bão, lũ, ngập: hãy theo dõi bản tin chính thức của Trung tâm Dự báo khí tượng thủy văn quốc gia ({NCHMF_URL}) và cổng cảnh "
              f"báo lũ quét, sạt lở ({LU_QUET_URL}); khi gặp nguy hiểm gọi 112.")
CAU_NGOAI_7_NGAY = "Mình chỉ có dự báo 7 ngày tới."
CAU_THEO_CA_NGAY = "Đây là dự báo theo cả ngày, không riêng buổi bạn hỏi."
CAU_CO_THE_DOI = "Dự báo có thể thay đổi."
THU = ("Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ nhật")

_TU_KHOA = re.compile(r"\b(?:thời\s+tiết|mưa|nắng|nhiệt\s+độ|bão|lũ|trời|nóng|lạnh|độ\s+ẩm|gió)\b", re.IGNORECASE)
_BAO_LU = re.compile(r"\b(?:bão|lũ|ngập)\b", re.IGNORECASE)
_CANH_BAO = re.compile(r"\bcảnh\s+báo\b", re.IGNORECASE)
_BUOI = re.compile(r"\b(?:sáng|trưa|chiều|tối|đêm)\s+(?:nay|mai)\b|\bbuổi\s+(?:sáng|trưa|chiều|tối)\b", re.IGNORECASE)
_XA = re.compile(r"\b(?:tuần\s+sau|tháng\s+sau|tháng\s+tới|năm\s+sau|năm\s+tới)\b", re.IGNORECASE)
_NGAY_THANG = re.compile(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?![\d/])")


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def co_tu_khoa(text: str) -> bool:
    return bool(_TU_KHOA.search(_nfc(text)))


def co_tu_khoa_luot(query: str, history) -> bool:
    """D4 (+ m-2): câu cuối **hoặc câu hỏi liền trước** trong lịch sử của cuộc có từ khoá."""
    return co_tu_khoa(query) or bool(history and co_tu_khoa(history[-1][0]))


def la_cau_bao_lu(text: str) -> bool:
    """D6 (+ m-3): bão / lũ / ngập; hoặc "cảnh báo" **cùng** một từ thời tiết khác ("cảnh báo bậc thang" ⇒ không)."""
    t = _nfc(text)
    return bool(_BAO_LU.search(t) or (_CANH_BAO.search(t) and co_tu_khoa(_CANH_BAO.sub(" ", t))))


def co_buoi(text: str) -> bool:
    return bool(_BUOI.search(_nfc(text)))


def ngoai_7_ngay(text: str, hom_nay: date | None) -> bool:
    """D3: "tuần sau / tháng sau…" hoặc ngày dd/mm cách hôm nay ≥ 7 ngày (hoặc đã qua) ⇒ câu cố định "chỉ có dự báo 7 ngày"."""
    t = _nfc(text)
    if _XA.search(t):
        return True
    if hom_nay is None:
        return False
    for d, m in _NGAY_THANG.findall(t):
        try:
            ngay = date(hom_nay.year, int(m), int(d))
        except ValueError:
            continue
        if ngay < hom_nay:  # dd/mm đã qua trong năm ⇒ hiểu là năm sau
            ngay = ngay.replace(year=hom_nay.year + 1)
        if (ngay - hom_nay).days >= SO_NGAY:
            return True
    return False


@dataclass
class DuBao:
    """Kết quả một lần lấy: `trang_thai` "ok" / "loi" (`loi` = mã ngắn); `ngay` = 7 ngày (đã làm tròn); `cap_nhat` = "HH:MM dd/mm" API trả."""
    trang_thai: str
    ngay: list[dict] = field(default_factory=list)
    cap_nhat: str | None = None
    loi: str | None = None
    ms: float = 0.0
    tu_cache: bool = False


_CACHE: dict = {}


def _so(x, ten: str) -> float:
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise ValueError(ten)
    lo, hi = MIEN[ten]
    if not lo <= x <= hi:
        raise ValueError(ten)
    return float(x)


def doc_phan_hoi(data) -> DuBao:
    """Phản hồi Open-Meteo ⇒ `DuBao`; sai schema / độ dài / số ngoài miền ⇒ `ValueError`. Làm tròn **ở đây** (D8 m-1): nhiệt độ, xác suất nguyên;
    lượng mưa 1 chữ số thập phân."""
    daily, current = data["daily"], data["current"]
    cot = [daily[k] for k in ("time", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max", "precipitation_sum")]
    if any(not isinstance(c, list) or len(c) != SO_NGAY for c in cot):
        raise ValueError("do_dai")
    ngay = []
    for t, tmax, tmin, xs, mua in zip(*cot):
        ngay.append({"ngay": date.fromisoformat(t), "tmax": round(_so(tmax, "tmax")), "tmin": round(_so(tmin, "tmin")),
                     "xs": None if xs is None else round(_so(xs, "xs")), "mua": round(_so(mua, "mua"), 1)})
    gio = current["time"]  # "YYYY-MM-DDTHH:MM" theo `timezone`
    ngay_cn = date.fromisoformat(gio[:10])
    return DuBao("ok", ngay, f"{gio[11:16]} {ngay_cn:%d/%m}")


async def lay_du_bao(*, timeout: float = TIMEOUT_S, transport: httpx.AsyncBaseTransport | None = None) -> DuBao:
    """D7: một lần gọi (không thử lại); cache RAM 30 phút (chỉ kết quả "ok"). `transport`: chỉ test truyền (phản hồi ghi sẵn, không mạng)."""
    cu = _CACHE.get("kq")
    if cu is not None and time.monotonic() - _CACHE["t"] < CACHE_S and transport is None:
        return DuBao(cu.trang_thai, cu.ngay, cu.cap_nhat, None, 0.0, True)
    started = time.perf_counter()
    params = {"latitude": HUE_LAT, "longitude": HUE_LON, "timezone": "Asia/Ho_Chi_Minh", "forecast_days": SO_NGAY, "current": "temperature_2m",
              "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum"}

    def xong(**kw) -> DuBao:
        return DuBao(ms=round((time.perf_counter() - started) * 1000, 1), **kw)

    try:
        async with httpx.AsyncClient(timeout=timeout, transport=transport) as client:
            response = await client.get(OPEN_METEO_URL, params=params)
    except httpx.TimeoutException:
        return xong(trang_thai="loi", loi="het_gio")
    except httpx.HTTPError:
        return xong(trang_thai="loi", loi="mang")
    if response.status_code != 200:
        return xong(trang_thai="loi", loi=f"http_{response.status_code}")
    try:
        kq = doc_phan_hoi(response.json())
    except (ValueError, KeyError, TypeError):
        return xong(trang_thai="loi", loi="schema")
    kq.ms = round((time.perf_counter() - started) * 1000, 1)
    if transport is None:
        _CACHE.update(kq=kq, t=time.monotonic())
    return kq


def _so_chu(x: float) -> str:
    return f"{x:.1f}".replace(".", ",")


def dong_ngay(d: dict) -> str:
    """D5: một ngày ⇒ một dòng cố định (số đã làm tròn)."""
    phan = [f"{d['tmin']}–{d['tmax']} °C"]
    if d["xs"] is not None:
        phan.append(f"khả năng mưa {d['xs']} %")
    phan.append(f"lượng mưa {_so_chu(d['mua'])} mm")
    return f"{THU[d['ngay'].weekday()]} {d['ngay']:%d/%m}: " + ", ".join(phan)


def dong_nguon(du_bao: DuBao) -> str:
    return f"{GHI_CONG} — số liệu lúc {du_bao.cap_nhat}. {CAU_CO_THE_DOI}"


def khoi_du_bao(du_bao: DuBao, tu: int, den: int, buoi: bool = False) -> str:
    """D5: khối số liệu cho ngày `tu`…`den` (0 = hôm nay theo giờ Việt Nam của API); luôn có dòng nguồn + giờ."""
    tu, den = sorted((max(0, min(tu, SO_NGAY - 1)), max(0, min(den, SO_NGAY - 1))))
    dong = [f"- {dong_ngay(d)}" for d in du_bao.ngay[tu:den + 1]]
    if buoi:
        dong.append(f"- {CAU_THEO_CA_NGAY}")
    return "\n".join([TIEU_DE, *dong, dong_nguon(du_bao)])


# D8: số dạng thời tiết — °C / ° / độ (C) / % hay "phần trăm" cạnh mưa / ẩm / khả năng / mm / mi-li-mét / "li" cạnh mưa; khoảng "24–30", "từ 24 đến 30"
_SO = r"\d+(?:[.,]\d+)?"
_KHOANG = rf"({_SO})(?:\s*(?:–|-|—|đến|tới)\s*({_SO}))?\s*"
_DON_VI_LUON = re.compile(_KHOANG + r"(?:°\s*c|°|độ\s*c|độ|mm|mi-li-mét|milimét)(?![\w])", re.IGNORECASE)
_DON_VI_CANH_MUA = re.compile(_KHOANG + r"(?:%|phần\s+trăm|li)(?![\w])", re.IGNORECASE)
_CANH_MUA = re.compile(r"mưa|ẩm|khả\s+năng|xác\s+suất", re.IGNORECASE)
_MOI_SO = re.compile(_SO)


def chuan_so(s: str) -> str:
    return s.replace(".", ",")


def so_thoi_tiet(text: str) -> list[str]:
    """Mọi chuỗi số dạng thời tiết trong `text` (đã chuẩn `.` ⇒ `,`), theo thứ tự xuất hiện."""
    t = _nfc(text)
    out = []
    for m in _DON_VI_LUON.finditer(t):
        out += [chuan_so(g) for g in m.groups() if g]
    for m in _DON_VI_CANH_MUA.finditer(t):
        if _CANH_MUA.search(t[max(0, m.start() - 30):m.start()]):
            out += [chuan_so(g) for g in m.groups() if g]
    return out


def tap_so(text: str) -> set[str]:
    """Mọi chuỗi số trong `text` (đoạn kho được trích / khối code in) — tập cho phép của D8."""
    return {chuan_so(s) for s in _MOI_SO.findall(_nfc(text))}


def kiem_so(text: str, cho_phep: set[str]) -> list[str]:
    """D8: số thời tiết trong chữ model nằm ngoài tập cho phép (rỗng = đạt)."""
    return [s for s in so_thoi_tiet(text) if s not in cho_phep]
