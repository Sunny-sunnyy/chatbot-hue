"""Công cụ `goi_y_luu_tru` — Đợt 6 (6.3b, mặc định tắt).

Tái sử dụng trực tiếp `llm.luu_tru_lich` (bảng 136 cơ sở lưu trú, deep link 3 sàn Booking/Agoda/Traveloka,
danh sách tên miền cho phép `ALLOWED_OTA_HOSTS`).
Bất biến cứng:
- Luôn kèm đúng `ltl.NHAN`: "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống."
- Tuyệt đối không bịa giá phòng, tình trạng còn phòng hay email.
"""
from __future__ import annotations

import datetime as dt

from llm import luu_tru_lich as ltl
from llm import lich_trinh_v2 as lt2

TIEU_DE_NGUON = "Gợi ý cơ sở lưu trú Huế (theo vị trí và hạng)"
MUC_NGUON = "Danh sách gợi ý lưu trú (kèm link Booking / Agoda / Traveloka)"
NGUON_SOURCE = "he_thong://goi_y_luu_tru"
NHAN = ltl.NHAN

KHU_LUA_CHON = ("trung_tam", "phia_tay", "ven_bien_bac", "ven_bien_nam", "bat_ky")
HANG_LUA_CHON = ("cao", "vua", "binh_dan", "tat_ca")

_KHU_LOC = {
    "trung_tam": (ltl.KHU_LOI, None),
    "phia_tay": (ltl.KHU_TAY, None),
    "ven_bien_bac": (ltl.KHU_BIEN, "bac"),
    "ven_bien_nam": (ltl.KHU_BIEN, "nam"),
    "bat_ky": (None, None),
}
_TEN_KHU_LUA_CHON = {
    "trung_tam": ltl.TEN_KHU[ltl.KHU_LOI],
    "phia_tay": ltl.TEN_KHU[ltl.KHU_TAY],
    "ven_bien_bac": f"{ltl.TEN_KHU[ltl.KHU_BIEN]} (bờ Bắc: Thuận An, Tam Giang)",
    "ven_bien_nam": f"{ltl.TEN_KHU[ltl.KHU_BIEN]} (bờ Nam: Lăng Cô, Phú Lộc)",
    "bat_ky": "Toàn thành phố Huế",
}
_HANG_RANK = {"5 sao": 5, "4 sao": 4, "3 sao": 3, "2 sao": 2, "1 sao": 1, "Đạt chuẩn phục vụ khách du lịch": 0}
_HANG_TAP = {
    "cao": frozenset({"5 sao", "4 sao"}),
    "vua": frozenset({"3 sao", "2 sao"}),
    "binh_dan": frozenset({"1 sao", "Đạt chuẩn phục vụ khách du lịch"}),
    "tat_ca": None,
}
_DIEM_VEN_BIEN_NAM = frozenset({"dam_lap_an", "bach_ma", "thac_nhi_ho", "deo_hai_van"})
_DIEM_VEN_BIEN_BAC = frozenset({"bien_thuan_an", "pha_tam_giang", "dam_chuon"})


def _chuan_khu_theo_diem(khu: str, gan_diem: str) -> str:
    khu_chuan = khu if khu in _KHU_LOC else "bat_ky"
    if gan_diem in _DIEM_VEN_BIEN_NAM:
        return "ven_bien_nam"
    if gan_diem in _DIEM_VEN_BIEN_BAC:
        return "ven_bien_bac"
    return khu_chuan


def _km_den(c: dict, cum_id: str | None) -> float:
    km_map = c.get("km_toi_cum")
    if isinstance(km_map, dict):
        key = cum_id or c.get("cum_gan")
        if key and key in km_map:
            return float(km_map[key])
        if km_map:
            return float(min(km_map.values()))
    elif isinstance(km_map, (int, float)):
        return float(km_map)
    return 999.0


def _parse_date(s: str) -> dt.date | None:
    raw = (s or "").strip()
    if not raw:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(raw, fmt).date()
        except ValueError:
            pass
    return None


def _loc_co_so_chi_tiet(
    bang_luu_tru: dict,
    bang_v2: lt2.BangV2 | None,
    khu: str = "bat_ky",
    gan_diem: str = "",
    hang_sao: str = "tat_ca",
    toi_da: int = 5,
) -> tuple[list[dict], str, bool]:
    khu_chuan = _chuan_khu_theo_diem(khu, gan_diem)
    hang_chuan = hang_sao if hang_sao in _HANG_TAP else "tat_ca"
    khu_gia_tri, phia = _KHU_LOC[khu_chuan]
    allowed_stars = _HANG_TAP[hang_chuan]

    cum_muc_tieu = None
    ten_diem = None
    if gan_diem and gan_diem != "khong" and bang_v2 is not None and gan_diem in bang_v2.theo_id:
        cum_muc_tieu = bang_v2.theo_id[gan_diem]["cum"]
        ten_diem = bang_v2.theo_id[gan_diem]["ten"]

    pool = list(bang_luu_tru["co_so"])
    if khu_gia_tri is not None:
        pool = [c for c in pool if c.get("khu") == khu_gia_tri and (phia is None or c.get("phia_bien") == phia)]
    da_noi_hang = False
    if allowed_stars is not None:
        pool_hang = [c for c in pool if c.get("xep_hang") in allowed_stars]
        if pool_hang:
            pool = pool_hang
        elif pool:
            da_noi_hang = True

    if cum_muc_tieu:
        pool.sort(key=lambda c: (_km_den(c, cum_muc_tieu), -_HANG_RANK.get(c.get("xep_hang", ""), 0), c["ten"]))
        chon = pool[:toi_da]
    else:
        pool.sort(key=lambda c: (-_HANG_RANK.get(c.get("xep_hang", ""), 0), _km_den(c, None), c["ten"]))
        chon = pool[:toi_da]

    bo_loc = _TEN_KHU_LUA_CHON[khu_chuan]
    if ten_diem:
        bo_loc += f" · gần {ten_diem}"
    return chon, bo_loc, da_noi_hang


def _loc_co_so(
    bang_luu_tru: dict,
    bang_v2: lt2.BangV2 | None,
    khu: str = "bat_ky",
    gan_diem: str = "",
    hang_sao: str = "tat_ca",
    toi_da: int = 5,
) -> tuple[list[dict], str]:
    chon, bo_loc, _ = _loc_co_so_chi_tiet(bang_luu_tru, bang_v2, khu=khu, gan_diem=gan_diem, hang_sao=hang_sao, toi_da=toi_da)
    return chon, bo_loc


def ket_qua_co_kieu(
    bang_luu_tru: dict,
    bang_v2: lt2.BangV2 | None,
    khu: str = "bat_ky",
    gan_diem: str = "",
    hang_sao: str = "tat_ca",
    ngay_nhan: str = "",
    ngay_tra: str = "",
    so_khach: int = 2,
    toi_da: int = 5,
) -> tuple[str, dict]:
    """Trả `(văn_bản_gợi_ý, dữ_liệu_có_kiểu)` có link Booking/Agoda/Traveloka an toàn, cờ `da_noi_hang` và đúng `NHAN`."""
    from urllib.parse import quote

    d_nhan = _parse_date(ngay_nhan)
    d_tra = _parse_date(ngay_tra)
    if d_nhan is not None and d_tra is not None and d_tra <= d_nhan:
        d_tra = None
    so_nguoi = max(int(so_khach or 2), 1)
    hang_chuan = hang_sao if hang_sao in _HANG_TAP else "tat_ca"
    chon, mo_ta_loc, da_noi_hang = _loc_co_so_chi_tiet(
        bang_luu_tru, bang_v2, khu=khu, gan_diem=gan_diem, hang_sao=hang_chuan, toi_da=toi_da
    )
    cum_muc_tieu = (
        bang_v2.theo_id[gan_diem]["cum"]
        if (gan_diem and gan_diem != "khong" and bang_v2 is not None and gan_diem in bang_v2.theo_id)
        else None
    )

    ghi_chu_noi_hang = f"Đã nới hạng vì khu vực chưa có hạng {hang_chuan}." if da_noi_hang else None
    hang_mo_ta = (
        f"Đã nới hạng vì khu vực chưa có hạng {hang_chuan} (hiển thị hạng hiện có)"
        if da_noi_hang
        else f"Hạng: {hang_chuan}"
    )
    dong = [
        NHAN,
        f"Phạm vi lọc: {mo_ta_loc} | {hang_mo_ta} | Số khách tìm phòng: {so_nguoi}"
        + (f" | Nhận {d_nhan.strftime('%d/%m/%Y')}" if d_nhan else "")
        + (f" – Trả {d_tra.strftime('%d/%m/%Y')}" if d_tra else "")
        + ".",
    ]
    du_lieu = {
        "nhan": NHAN,
        "pham_vi": mo_ta_loc,
        "hang_sao": hang_chuan,
        "da_noi_hang": da_noi_hang,
        "ghi_chu_noi_hang": ghi_chu_noi_hang,
        "co_so": [],
    }
    if not chon:
        dong.append("Chưa có cơ sở lưu trú phù hợp bộ lọc này trong bảng 136 cơ sở.")
        return "\n".join(dong), du_lieu

    so_dem = (d_tra - d_nhan).days if (d_nhan is not None and d_tra is not None) else 1
    for idx, c in enumerate(chon, 1):
        links = ltl.tao_deep_links_co_so(
            c["ten"],
            ngay_di=d_nhan.isoformat() if d_nhan else None,
            so_ngay=so_dem + 1,
            nguoi_lon=so_nguoi,
            anh_trang=c.get("anh_trang"),
        )
        cum_ref = cum_muc_tieu or c.get("cum_gan")
        cum_entry = bang_v2.cum.get(cum_ref) if (bang_v2 is not None and cum_ref) else cum_ref
        ten_cum = cum_entry.get("ten") if isinstance(cum_entry, dict) else (cum_entry or cum_ref)
        km_val = _km_den(c, cum_ref)
        vi_tri_ngan = f"cách cụm {ten_cum} khoảng {km_val:.1f} km" if (ten_cum and km_val < 999.0) else ""
        vi_tri = f" · {vi_tri_ngan}" if vi_tri_ngan else ""
        links_md = " · ".join(f"[{san}]({url})" for san, url in links.items())
        dong.append(
            f"{idx}. **{c['ten']}** ({c.get('xep_hang', '')}) — {c.get('dia_chi', '')}{vi_tri} "
            f"[nguồn: {c.get('nguon', '')}] · Tìm phòng: {links_md}"
        )
        map_url = ltl.MAP_BASE + quote(", ".join(x for x in (c["ten"], c.get("dia_chi"), "Huế") if x))
        du_lieu["co_so"].append({
            "ten": c["ten"],
            "xep_hang": c.get("xep_hang", ""),
            "dia_chi": c.get("dia_chi", ""),
            "vi_tri": vi_tri_ngan,
            "anh": c.get("anh"),
            "map_url": map_url,
            "links": links,
            "nguon": c.get("nguon", ""),
        })
    dong.append("Không có thông tin giá phòng hay tình trạng còn phòng trực tiếp; hãy kiểm tra trên link đặt phòng.")
    return "\n".join(dong), du_lieu


def ket_qua(
    bang_luu_tru: dict,
    bang_v2: lt2.BangV2 | None,
    khu: str = "bat_ky",
    gan_diem: str = "",
    hang_sao: str = "tat_ca",
    ngay_nhan: str = "",
    ngay_tra: str = "",
    so_khach: int = 2,
    toi_da: int = 5,
) -> tuple[str, int]:
    """Trả `(văn_bản_gợi_ý, số_cơ_sở)` có link Booking/Agoda/Traveloka an toàn và đúng `NHAN`."""
    text_out, du_lieu = ket_qua_co_kieu(
        bang_luu_tru,
        bang_v2,
        khu=khu,
        gan_diem=gan_diem,
        hang_sao=hang_sao,
        ngay_nhan=ngay_nhan,
        ngay_tra=ngay_tra,
        so_khach=so_khach,
        toi_da=toi_da,
    )
    return text_out, len(du_lieu["co_so"])


def _bang_diem(bang_v2: lt2.BangV2 | None) -> str:
    if bang_v2 is None:
        return ""
    return ", ".join(f"{d['id']} ({d['ten']})" for d in bang_v2.diem)


_MO_TA_CACH_DUNG = (
    "Khi khách hỏi gợi ý khách sạn, nhà nghỉ, homestay, resort hoặc chỗ ở ở Huế theo khu vực, hạng sao hoặc gần điểm tham quan "
    "(như trung tâm / hai bờ sông Hương, gần Đại Nội, phía tây Kim Long/Thủy Xuân, Thuận An, Lăng Cô), HÃY GỌI công cụ này "
    "thay vì chỉ tự liệt kê từ bài kho để trả đủ danh sách từ bảng 136 cơ sở, 3 link Booking/Agoda/Traveloka và nhãn chuẩn "
    "(không gọi cho câu ngoài Huế như Đà Nẵng, hoặc câu chỉ hỏi giá/phòng trống của 1 khách sạn cụ thể).\n"
    "- khu: trung_tam (hai bờ sông Hương, Bờ Nam, Kinh thành, gần Đại Nội/Đông Ba), phia_tay (Kim Long, Thủy Xuân, yên tĩnh), "
    "ven_bien_bac (Thuận An, Phá Tam Giang, Đầm Chuồn), ven_bien_nam (Lăng Cô, Chân Mây, Đầm Lập An, Phú Lộc), bat_ky.\n"
    "- hang_sao: cao (4–5★), vua (2–3★), binh_dan (1★/nhà nghỉ/Đạt chuẩn), tat_ca.\n"
    "- gan_diem: mã điểm trong bảng hệ thống (nếu hỏi gần một điểm cụ thể) hoặc `khong`.\n"
    "- ngay_nhan, ngay_tra (YYYY-MM-DD nếu có), so_khach (mặc định 2); luôn giữ nhãn chưa kiểm giá/phòng trống và không bịa giá.\n"
    'Ví dụ: khu="ven_bien_nam", hang_sao="tat_ca", so_khach=4 | khu="trung_tam", hang_sao="binh_dan", so_khach=2.'
)


def mo_ta_cong_cu(bang_v2: lt2.BangV2 | None, *, toi_uu: bool = False) -> str:
    """Mô tả công cụ khi không hoặc có `gan_diem`."""
    if bang_v2 is None:
        return _MO_TA_CACH_DUNG
    return f"{_MO_TA_CACH_DUNG}\nMã điểm tham khảo cho `gan_diem` (hoặc `khong`): {_bang_diem(bang_v2)}."


def mo_ta_ngan(bang_v2: lt2.BangV2 | None, *, toi_uu: bool = False) -> str:
    """Mô tả gọn dưới `cong_cong_cu: linh_hoat` (bảng điểm đã nằm ở khối đầu của lời dặn)."""
    return _MO_TA_CACH_DUNG
