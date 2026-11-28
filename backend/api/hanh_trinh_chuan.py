"""Chuẩn hoá dữ liệu lịch trình thành `CanonicalItinerary` bất biến (Đợt 5 — Phần A).

Ranh giới dùng chung cho `.ics` v2 và `Slide Designer Agent` / `.pptx` v2:
- Trích xuất cấu trúc lịch sạch từ `lich` (hoặc `lich_tu_luu(luu, flags)`), không gọi model, không đọc OAuth/chat.
- Chuẩn hoá câu tả (gỡ mã `[n]`), kiểm tra `map_url` theo `MAP_PREFIX`, kiểm tra ảnh tự host `/anh/lich/` và `/anh/khach_san/` (cấm `..`, cấm thư mục con, không mang trường ghi công/tác giả/giấy phép).
- Sinh `itinerary_hash` SHA-256 ổn định để làm `UID` `.ics` và khoá cache `(itinerary_hash, theme_id)` cho Slide Designer.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

MAP_PREFIX = "https://www.google.com/maps/search/"
ANH_LICH_PREFIX = "/anh/lich/"
ANH_KS_PREFIX = "/anh/khach_san/"
_MA_NGUON = re.compile(r"\s*\[(?:Nguồn\s*)?\d+\]")


def sach_cau_ta(cau: str | None) -> str | None:
    """Bỏ mã trích dẫn `[n]` / `[Nguồn n]` khỏi câu mô tả đã kiểm."""
    chu = _MA_NGUON.sub("", cau or "").strip()
    return chu or None


def hop_le_anh_lich(anh: dict | str | None, thu_muc_anh: Path | None = None) -> str | None:
    """Chỉ nhận ảnh tự host ngay dưới `/anh/lich/` (không `..`, không thư mục con, không ghi công)."""
    src = str((anh.get("src") if isinstance(anh, dict) else anh) or "").strip()
    if not src.startswith(ANH_LICH_PREFIX) or ".." in src or "\r" in src or "\n" in src or "\0" in src:
        return None
    ten_file = src[len(ANH_LICH_PREFIX):]
    if not ten_file or "/" in ten_file or "\\" in ten_file:
        return None
    if thu_muc_anh is not None and not (thu_muc_anh / src.lstrip("/")).is_file():
        return None
    return src


def hop_le_anh_ks(src: str | None, thu_muc_anh: Path | None = None) -> str | None:
    """Chỉ nhận ảnh khách sạn tự host ngay dưới `/anh/khach_san/*.jpg` (không `..`, không thư mục con)."""
    duong = str(src or "").strip()
    if not duong.startswith(ANH_KS_PREFIX) or not duong.endswith(".jpg") or ".." in duong or "\r" in duong or "\n" in duong or "\0" in duong:
        return None
    ten_file = duong[len(ANH_KS_PREFIX):]
    if not ten_file or "/" in ten_file or "\\" in ten_file:
        return None
    if thu_muc_anh is not None and not (thu_muc_anh / duong.lstrip("/")).is_file():
        return None
    return duong


def _map_url_hop_le(url: str | None) -> str | None:
    s = str(url or "").strip()
    if s.startswith(MAP_PREFIX) and "\r" not in s and "\n" not in s and "\0" not in s:
        return s
    return None


def chuan_hoa_lich(
    lich: dict,
    cau: dict[str, str] | None = None,
    *,
    an_toan: str | None = None,
    thu_muc_anh: Path | None = None,
) -> dict:
    """Chuyển `lich` (+ `cau` theo `id_muc`, `an_toan` nếu có) thành `CanonicalItinerary` thuần JSON + `itinerary_hash` ổn định."""
    cau = cau or {}
    ts = copy.deepcopy(lich.get("tham_so") or {})
    minh_hieu = str(lich.get("minh_hieu") or "")
    ngay_chuan = []
    manifest_diem: dict[str, str] = {}
    manifest_ks: dict[str, str] = {}

    for ng in lich.get("ngay") or []:
        muc_chuan = []
        for m in ng.get("muc") or []:
            id_muc = str(m.get("id_muc") or "")
            anh_src = hop_le_anh_lich(m.get("anh"), thu_muc_anh=thu_muc_anh)
            if anh_src and m.get("id_diem"):
                manifest_diem[str(m["id_diem"])] = anh_src
            elif anh_src and id_muc:
                manifest_diem[id_muc] = anh_src
            muc_chuan.append({
                "id_muc": id_muc,
                "buoi": m.get("buoi"),
                "loai": m.get("loai"),
                "id_diem": m.get("id_diem"),
                "ten": str(m.get("ten") or ""),
                "gio": m.get("gio"),
                "cau": sach_cau_ta(cau.get(id_muc) if id_muc in cau else m.get("cau")),
                "ghi_chu": m.get("ghi_chu"),
                "nhan": list(m.get("nhan") or []),
                "loai_diem": list(m.get("loai_diem") or []),
                "phut_di": m.get("phut_di"),
                "map_url": _map_url_hop_le(m.get("map_url")),
                "anh": {"src": anh_src} if anh_src else None,
            })
        ngay_chuan.append({
            "ngay": ng.get("ngay"),
            "ngay_thang": ng.get("ngay_thang"),
            "thu": ng.get("thu"),
            "chang": list(ng.get("chang") or []),
            "muc": muc_chuan,
        })

    an_chuan = []
    for a in lich.get("an") or []:
        an_chuan.append({
            "ngay": a.get("ngay"),
            "bua": a.get("bua"),
            "gan": a.get("gan"),
            "ghi_chu": a.get("ghi_chu"),
            "quan": [
                {
                    "ten": q.get("ten"),
                    "loai": q.get("loai"),
                    "nhan": q.get("nhan"),
                    "bai_id": q.get("bai_id"),
                    "map_url": _map_url_hop_le(q.get("map_url")),
                }
                for q in (a.get("quan") or [])
            ],
        })

    o_dau_raw = lich.get("o_dau")
    o_dau_chuan = None
    if isinstance(o_dau_raw, dict):
        co_so_chuan = []
        for c in o_dau_raw.get("co_so") or []:
            anh_ks = hop_le_anh_ks(c.get("anh"), thu_muc_anh=thu_muc_anh)
            if anh_ks and c.get("ten"):
                manifest_ks[str(c["ten"])] = anh_ks
            muc_ks = {
                "ten": c.get("ten"),
                "xep_hang": c.get("xep_hang"),
                "dia_chi": c.get("dia_chi"),
                "map_url": _map_url_hop_le(c.get("map_url")),
                "link": c.get("link"),
                "anh": anh_ks,
            }
            if isinstance(c.get("deep_links"), dict):
                muc_ks["deep_links"] = dict(c["deep_links"])
            if c.get("mau_hoi_phong"):
                muc_ks["mau_hoi_phong"] = c["mau_hoi_phong"]
            co_so_chuan.append(muc_ks)
        o_dau_chuan = {
            "khu": o_dau_raw.get("khu"),
            "ten_khu": o_dau_raw.get("ten_khu"),
            "ly_do": o_dau_raw.get("ly_do"),
            "co_so": co_so_chuan,
            "nhan": o_dau_raw.get("nhan"),
            "nguon": o_dau_raw.get("nguon"),
        }

    ghi_chu_chuan = [
        {"ma": g.get("ma"), "cau": g.get("cau"), **({"ngay": g["ngay"]} if "ngay" in g else {})}
        for g in (lich.get("ghi_chu") or [])
        if g.get("ma") != "du_bao"
    ]
    an_toan_sach = str(an_toan).strip() if an_toan and str(an_toan).strip() else None

    cot_loi = {
        "tham_so": ts,
        "ngay": ngay_chuan,
        "an": an_chuan,
        "o_dau": o_dau_chuan,
        "ghi_chu": ghi_chu_chuan,
        "an_toan": an_toan_sach,
    }
    itinerary_hash = hashlib.sha256(json.dumps(cot_loi, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    lich_id = str(lich.get("lich_id") or "").strip() or None

    return {
        "schema_version": "1.0",
        "itinerary_hash": itinerary_hash,
        **({"lich_id": lich_id} if lich_id else {}),
        "minh_hieu": minh_hieu,
        **cot_loi,
        "anh_manifest": {
            "diem": manifest_diem,
            "khach_san": manifest_ks,
        },
    }


def tu_luu_chuan(luu: dict, flags, *, thu_muc_anh: Path | None = None) -> dict:
    """Dựng `CanonicalItinerary` trực tiếp từ bản lưu `luu` trong `ConversationStore` qua `lich_tu_luu(luu, flags)`."""
    from api.routes.xuat import lich_tu_luu

    lich, cau = lich_tu_luu(luu, flags)
    return chuan_hoa_lich(lich, cau, an_toan=luu.get("an_toan"), thu_muc_anh=thu_muc_anh)
