"""Công cụ `tinh_ve_va_gio_tham_quan` — Đợt 6 (6.3a, mặc định tắt).

Tính chính xác bằng code thuần (không gọi model, không mạng):
- Giá vé lẻ 12 điểm Quần thể Di tích Cố đô Huế (NQ 55/2025/NQ-HĐND, hiệu lực 04/01/2026) & phương án tối ưu (vé lẻ vs tuyến 2/3/4/12 điểm, kèm cảnh báo tuyến 530k chỉ gồm 4 điểm).
- Tách riêng Hải Vân Quan (NQ 05/2026/NQ-HĐND: 70.000đ người lớn, <13 tuổi miễn phí).
- Các điểm/trải nghiệm có vé khác (Bạch Mã, Bạch Mã Village, Alba Thanh Tân, Không gian lưu niệm Lê Bá Đảng, Sốnglab, Duyệt Thị Đường, Ca Huế sông Hương, Xe buýt 2 tầng).
- Quy định trẻ em, giảm 50% công dân VN từ đủ 60 tuổi trở lên, 5 ngày lễ miễn phí công dân VN (dùng lịch âm sẵn có ở `ngay_lich`).
- Kiểm tra ngày nghỉ định kỳ, suất diễn và kịp giờ đóng cửa từ `diem_v16` / `the_noi`.
"""
from __future__ import annotations

import datetime as dt
import re
import unicodedata
from dataclasses import dataclass
from typing import Sequence

from llm import ngay_lich as nl

NGUON_QUAN_THE = "travel/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md"
NGUON_HAI_VAN = "travel/tickets/Vé tham quan Hải Vân Quan.md"
NGUON_DIEM_KHAC = "travel/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md"
NGUON_NGHE_THUAT = "travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md"
NGUON_HUONG_DAN = "travel/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md"

TEN_NGUON = {
    NGUON_QUAN_THE: "Vé tham quan Quần thể Di tích Cố đô Huế",
    NGUON_HAI_VAN: "Vé tham quan Hải Vân Quan",
    NGUON_DIEM_KHAC: "Vé các điểm tham quan và trải nghiệm khác ở Huế",
    NGUON_NGHE_THUAT: "Vé biểu diễn nghệ thuật và trải nghiệm sông Hương",
    NGUON_HUONG_DAN: "Hướng dẫn mua và sử dụng vé du lịch Huế",
}

DIEU_KIEN_CAO_TUOI_VN = (
    "Công dân Việt Nam từ đủ 60 tuổi trở lên theo Luật Người cao tuổi "
    "(xuất trình thẻ người cao tuổi, CCCD hoặc tài khoản VNeID)."
)

CANH_BAO_530K = (
    "Lưu ý tuyến 4 điểm (530.000đ người lớn / 100.000đ trẻ 7–12 tuổi, tối đa 02 ngày): "
    "chỉ gồm 4 điểm (Đại Nội Huế, Lăng Minh Mạng, Lăng Tự Đức, Lăng Khải Định), "
    "KHÔNG phải vé toàn bộ 12 điểm Quần thể Di tích (tuyến Tất cả các điểm là 600.000đ, tối đa 05 ngày)."
)

# 12 điểm thuộc Quần thể Di tích Cố đô Huế (NQ 55/2025/NQ-HĐND, hiệu lực 04/01/2026)
QUAN_THE_DIEM: dict[str, dict] = {
    "dai_noi": {"ten": "Đại Nội Huế", "nguoi_lon": 200_000, "tre_7_12": 40_000, "phut": 150, "gio_mo": (("07:00", "17:00"),)},
    "lang_minh_mang": {"ten": "Lăng Minh Mạng", "nguoi_lon": 150_000, "tre_7_12": 30_000, "phut": 150, "gio_mo": (("07:00", "17:00"),)},
    "lang_tu_duc": {"ten": "Lăng Tự Đức", "nguoi_lon": 150_000, "tre_7_12": 30_000, "phut": 150, "gio_mo": (("07:00", "17:00"),)},
    "lang_khai_dinh": {"ten": "Lăng Khải Định", "nguoi_lon": 150_000, "tre_7_12": 30_000, "phut": 150, "gio_mo": (("07:00", "17:00"),)},
    "lang_gia_long": {"ten": "Lăng Gia Long", "nguoi_lon": 150_000, "tre_7_12": 0, "phut": 150, "gio_mo": (("07:00", "17:00"),)},
    "lang_dong_khanh": {"ten": "Lăng Đồng Khánh", "nguoi_lon": 100_000, "tre_7_12": 0, "phut": 75, "gio_mo": (("07:00", "17:00"),)},
    "lang_thieu_tri": {"ten": "Lăng Thiệu Trị", "nguoi_lon": 50_000, "tre_7_12": 0, "phut": 75, "gio_mo": (("07:00", "17:00"),)},
    "bao_tang_co_vat": {"ten": "Bảo tàng Cổ vật Cung đình Huế", "nguoi_lon": 50_000, "tre_7_12": 0, "phut": 150, "gio_mo": (("07:00", "17:00"),)},
    "dien_hon_chen": {"ten": "Điện Hòn Chén", "nguoi_lon": 50_000, "tre_7_12": 0, "phut": 75, "gio_mo": (("07:00", "17:00"),)},
    "cung_an_dinh": {"ten": "Cung An Định", "nguoi_lon": 50_000, "tre_7_12": 0, "phut": 75, "gio_mo": (("07:00", "17:00"),)},
    "dan_nam_giao": {"ten": "Đàn Nam Giao", "nguoi_lon": 50_000, "tre_7_12": 0, "phut": 75, "gio_mo": (("07:00", "17:00"),)},
    "lang_duc_duc": {"ten": "Lăng Dục Đức", "nguoi_lon": 50_000, "tre_7_12": 0, "phut": 75, "gio_mo": (("07:00", "17:00"),)},
}


@dataclass(frozen=True)
class TuyenQuanThe:
    id: str
    ten: str
    diem: frozenset[str]
    nguoi_lon: int
    tre_7_12: int
    han: str


QUAN_THE_TUYEN: tuple[TuyenQuanThe, ...] = (
    TuyenQuanThe("tuyen_minh_mang_gia_long", "Tuyến 2 điểm Minh Mạng – Gia Long", frozenset({"lang_minh_mang", "lang_gia_long"}), 240_000, 30_000, "trong ngày"),
    TuyenQuanThe("tuyen_tu_duc_dong_khanh", "Tuyến 2 điểm Tự Đức – Đồng Khánh", frozenset({"lang_tu_duc", "lang_dong_khanh"}), 200_000, 30_000, "trong ngày"),
    TuyenQuanThe("tuyen_co_vat_an_dinh", "Tuyến 2 điểm Bảo tàng Cổ vật – Cung An Định", frozenset({"bao_tang_co_vat", "cung_an_dinh"}), 80_000, 0, "trong ngày"),
    TuyenQuanThe("tuyen_3_dai_noi_mm_kd", "Tuyến 3 điểm (Đại Nội – Minh Mạng – Khải Định)", frozenset({"dai_noi", "lang_minh_mang", "lang_khai_dinh"}), 420_000, 80_000, "trong ngày"),
    TuyenQuanThe("tuyen_3_dai_noi_mm_td", "Tuyến 3 điểm (Đại Nội – Minh Mạng – Tự Đức)", frozenset({"dai_noi", "lang_minh_mang", "lang_tu_duc"}), 420_000, 80_000, "trong ngày"),
    TuyenQuanThe("tuyen_3_dai_noi_td_kd", "Tuyến 3 điểm (Đại Nội – Tự Đức – Khải Định)", frozenset({"dai_noi", "lang_tu_duc", "lang_khai_dinh"}), 420_000, 80_000, "trong ngày"),
    TuyenQuanThe("tuyen_4_diem", "Tuyến 4 điểm (Đại Nội – Minh Mạng – Tự Đức – Khải Định)", frozenset({"dai_noi", "lang_minh_mang", "lang_tu_duc", "lang_khai_dinh"}), 530_000, 100_000, "tối đa 02 ngày"),
    TuyenQuanThe("tuyen_tat_ca_12", "Tuyến Tất cả các điểm (12 điểm Quần thể)", frozenset(QUAN_THE_DIEM), 600_000, 120_000, "tối đa 05 ngày"),
)

# Điểm ngoài Quần thể (tách riêng Hải Vân Quan + 8 điểm/trải nghiệm khác)
DIEM_NGOAI: dict[str, dict] = {
    "hai_van_quan": {
        "ten": "Hải Vân Quan",
        "nguon": NGUON_HAI_VAN,
        "diem_v16_id": "deo_hai_van",
        "gio_mo": (("07:00", "17:30"),),
        "phut": 75,
        "ngay_nghi": (),
        "giam_cao_tuoi_vn": True,
        "ghi_chu": (
            "Tách biệt hoàn toàn với Quần thể Di tích Cố đô Huế (NQ 05/2026/NQ-HĐND): "
            "người lớn (>=13 tuổi) 70.000đ; trẻ em <13 tuổi hoặc <1,3 m miễn phí; không nằm trong vé gộp Quần thể."
        ),
    },
    "bach_ma": {
        "ten": "Vườn quốc gia Bạch Mã",
        "nguon": NGUON_DIEM_KHAC,
        "diem_v16_id": "bach_ma",
        "gio_mo": (("07:30", "17:00"),),
        "phut": 150,
        "ngay_nghi": (),
        "giam_cao_tuoi_vn": True,
        "ghi_chu": (
            "Vé vào cổng người lớn 60.000–65.000đ; trẻ em (<1,3 m hoặc <16 tuổi) / HSSV 20.000–25.000đ; trẻ <6 tuổi miễn phí; "
            "công dân VN >=60 tuổi giảm 50%. Xe trung chuyển/vận chuyển lên đỉnh tính riêng; kiểm tra tình trạng sạt lở đường Km12 trước khi đi."
        ),
    },
    "bach_ma_village": {
        "ten": "Bạch Mã Village",
        "nguon": NGUON_DIEM_KHAC,
        "diem_v16_id": None,
        "gio_mo": (),
        "phut": 150,
        "ngay_nghi": (),
        "giam_cao_tuoi_vn": False,
        "ghi_chu": "Tính theo chiều cao: >=1,3 m là 100.000–120.000đ; 1,0–<1,3 m là 60.000–70.000đ; dưới 1,0 m miễn phí.",
    },
    "alba_thanh_tan": {
        "ten": "Suối khoáng nóng Alba Thanh Tân",
        "nguon": NGUON_DIEM_KHAC,
        "diem_v16_id": None,
        "gio_mo": (("07:00", "24:00"),),
        "phut": 180,
        "ngay_nghi": (),
        "giam_cao_tuoi_vn": False,
        "ghi_chu": "Vé cổng tắm khoáng / công viên nước: >1,4 m là 230.000đ; 1,2–1,4 m là 115.000đ; <1,2 m miễn phí (trò chơi zipline/highwire tính gói riêng).",
    },
    "kg_le_ba_dang": {
        "ten": "Không gian lưu niệm Lê Bá Đảng",
        "nguon": NGUON_DIEM_KHAC,
        "diem_v16_id": "kg_le_ba_dang",
        "gio_mo": (("08:00", "12:00"), ("14:00", "18:00")),
        "phut": 75,
        "ngay_nghi": (0,),  # Thứ Hai đóng cửa
        "giam_cao_tuoi_vn": False,
        "ghi_chu": (
            "Tiêu chuẩn 200.000đ/lượt; cư dân Huế 120.000đ; đoàn >=30 khách 150.000đ; trẻ <6 tuổi & <1,3 m miễn phí. "
            "Mở Thứ Ba–Chủ Nhật (08:00–12:00, 14:00–18:00), ĐÓNG CỬA Thứ Hai. Phân biệt với Bảo tàng Nghệ thuật Lê Bá Đảng tại 17 Lê Lợi."
        ),
    },
    "songlab": {
        "ten": "Sốnglab Huế",
        "nguon": NGUON_DIEM_KHAC,
        "diem_v16_id": None,
        "gio_mo": (("09:00", "21:00"),),
        "phut": 90,
        "ngay_nghi": (0, 1, 2, 3),  # Chỉ mở Thứ Sáu – Chủ Nhật
        "giam_cao_tuoi_vn": False,
        "ghi_chu": (
            "Chỉ mở Thứ Sáu – Chủ Nhật (09:00–21:00), đóng cửa Thứ Hai–Thứ Năm. "
            "Ngoài Huế: 150.000–180.000đ (trẻ 0,8–1,4 m: 100.000–110.000đ); cư dân Huế: 100.000đ (trẻ 70.000đ); dưới 0,8 m miễn phí."
        ),
    },
    "duyet_thi_duong": {
        "ten": "Nhà hát Duyệt Thị Đường",
        "nguon": NGUON_NGHE_THUAT,
        "diem_v16_id": "duyet_thi_duong",
        "gio_mo": (("10:00", "10:40"), ("15:00", "15:40")),
        "phut": 40,
        "ngay_nghi": (),
        "giam_cao_tuoi_vn": False,
        "ghi_chu": (
            "300.000đ/khách/suất (2 suất/ngày: 10:00–10:40 và 15:00–15:40). "
            "Bắt buộc mua thêm vé vào Đại Nội Huế (200.000đ người lớn / 40.000đ trẻ 7–12 tuổi) nếu chưa có."
        ),
    },
    "ca_hue_song_huong": {
        "ten": "Ca Huế trên sông Hương",
        "nguon": NGUON_NGHE_THUAT,
        "diem_v16_id": "ca_hue_song_huong",
        "gio_mo": (("19:00", "22:00"),),
        "phut": 60,
        "ngay_nghi": (),
        "giam_cao_tuoi_vn": False,
        "ghi_chu": "Suất tối 19:00 / 20:00 / 21:00 (tối thiểu 50 phút): ghép thuyền khách VN 100.000–130.000đ, khách quốc tế 150.000đ.",
    },
    "xe_buyt_2_tang": {
        "ten": "Xe buýt 2 tầng City Sightseeing Huế",
        "nguon": NGUON_DIEM_KHAC,
        "diem_v16_id": None,
        "gio_mo": (),
        "phut": 60,
        "ngay_nghi": (),
        "giam_cao_tuoi_vn": False,
        "ghi_chu": (
            "Tour Đêm 130.000đ (trẻ 6–11 tuổi 95.000đ); vé 4h khách VN 150.000đ / quốc tế 299.000đ; 24h 429.000đ; 48h 599.000đ; "
            "trẻ <6 tuổi ngồi cùng người lớn miễn phí. Chỉ gồm vé xe, không gồm vé vào cửa các điểm di tích."
        ),
    },
}

DIEM_IDS: tuple[str, ...] = tuple(QUAN_THE_DIEM) + tuple(DIEM_NGOAI)

_BIET_DANH: dict[str, str] = {
    "hoang thanh": "dai_noi",
    "tu cam thanh": "dai_noi",
    "dai noi": "dai_noi",
    "dai noi hue": "dai_noi",
    "minh mang": "lang_minh_mang",
    "hieu lang": "lang_minh_mang",
    "tu duc": "lang_tu_duc",
    "khiem lang": "lang_tu_duc",
    "khai dinh": "lang_khai_dinh",
    "ung lang": "lang_khai_dinh",
    "gia long": "lang_gia_long",
    "thien tho lang": "lang_gia_long",
    "dong khanh": "lang_dong_khanh",
    "tu lang": "lang_dong_khanh",
    "thieu tri": "lang_thieu_tri",
    "xuong lang": "lang_thieu_tri",
    "bao tang co vat": "bao_tang_co_vat",
    "dien long an": "bao_tang_co_vat",
    "hon chen": "dien_hon_chen",
    "dien hue nam": "dien_hon_chen",
    "cung an dinh": "cung_an_dinh",
    "an dinh": "cung_an_dinh",
    "dan nam giao": "dan_nam_giao",
    "nam giao": "dan_nam_giao",
    "duc duc": "lang_duc_duc",
    "an lang": "lang_duc_duc",
    "deo hai van": "hai_van_quan",
    "deo_hai_van": "hai_van_quan",
    "hai van quan": "hai_van_quan",
    "vuon quoc gia bach ma": "bach_ma",
    "vqg bach ma": "bach_ma",
    "bach ma": "bach_ma",
    "bach ma village": "bach_ma_village",
    "alba": "alba_thanh_tan",
    "alba thanh tan": "alba_thanh_tan",
    "le_ba_dang": "kg_le_ba_dang",
    "le ba dang": "kg_le_ba_dang",
    "khong gian luu niem le ba dang": "kg_le_ba_dang",
    "songlab": "songlab",
    "song lab": "songlab",
    "duyet thi duong": "duyet_thi_duong",
    "ca hue": "ca_hue_song_huong",
    "ca hue song huong": "ca_hue_song_huong",
    "xe buyt 2 tang": "xe_buyt_2_tang",
    "city sightseeing": "xe_buyt_2_tang",
}

_LE_VN_DUONG = {
    (26, 3): "Ngày Giải phóng thành phố Huế (26/3)",
    (19, 8): "Ngày Cách mạng Tháng Tám (19/8)",
    (2, 9): "Ngày Quốc khánh (02/9)",
    (23, 11): "Ngày Di sản Văn hóa Việt Nam (23/11)",
}
_THU_VIET = ("Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật")


def _bo_dau(text: str) -> str:
    s = unicodedata.normalize("NFD", (text or "").replace("đ", "d").replace("Đ", "D"))
    return " ".join("".join(ch for ch in s if unicodedata.category(ch) != "Mn").lower().split())


def chuan_diem(ma_hoac_ten: str) -> str | None:
    s = (ma_hoac_ten or "").strip()
    if s in QUAN_THE_DIEM or s in DIEM_NGOAI:
        return s
    k = _bo_dau(s.replace("_", " "))
    if k.replace(" ", "_") in QUAN_THE_DIEM or k.replace(" ", "_") in DIEM_NGOAI:
        return k.replace(" ", "_")
    return _BIET_DANH.get(k)


def _dinh_dang_tien(amount: int) -> str:
    return f"{amount:,}".replace(",", ".") + "đ"


def parse_ngay(ngay: str, hom_nay: dt.date | None = None) -> dt.date | None:
    s = (ngay or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    m = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})", s)
    if m:
        ref = hom_nay or nl.hom_nay()
        try:
            return dt.date(ref.year, int(m.group(2)), int(m.group(1)))
        except ValueError:
            return None
    return None


def parse_gio_phut(gio: str) -> int | None:
    s = (gio or "").strip().lower()
    if not s:
        return None
    m = re.fullmatch(r"(\d{1,2})\s*[:hg]\s*(\d{1,2})?", s)
    if not m:
        return None
    hh, mm = int(m.group(1)), int(m.group(2) or 0)
    if 0 <= hh <= 23 and 0 <= mm <= 59:
        return hh * 60 + mm
    return None


def _phut_sang_chuoi(phut: int) -> str:
    return f"{phut // 60:02d}:{phut % 60:02d}"


def kiem_tra_ngay_le_vn(ngay_d: dt.date) -> tuple[bool, bool, str | None]:
    """Trả `(mien_quan_the, mien_hai_van_quan, ten_le)` cho ngày dương lịch `ngay_d`."""
    am = nl.solar_to_lunar(ngay_d)
    if not am.leap and am.day == 1 and am.month == 1:
        return True, True, "Mùng 1 Tết Nguyên Đán (âm lịch)"
    le = _LE_VN_DUONG.get((ngay_d.day, ngay_d.month))
    if le:
        return True, True, le
    if (ngay_d.day, ngay_d.month) == (29, 3):
        return False, True, "Ngày Giải phóng thành phố Đà Nẵng (29/3 — chỉ áp dụng miễn phí tại Hải Vân Quan)"
    return False, False, None


def toi_uu_quan_the(diem_ids: Sequence[str], tre_em: bool = False) -> tuple[int, tuple[tuple[str, str, int], ...]]:
    """Bitmask DP tìm gói vé Quần thể rẻ nhất phủ đủ `diem_ids` (`1 <= len <= 12`).

    Trả `(tong_toi_uu, ((ten_goi, han_dung, gia), ...))`.
    Khi chi phí bằng nhau, ưu tiên ít vé hơn; nếu vẫn bằng nhau ưu tiên mua lẻ.
    """
    pts = [d for d in dict.fromkeys(diem_ids) if d in QUAN_THE_DIEM]
    if not pts:
        return 0, ()
    idx = {d: i for i, d in enumerate(pts)}
    full = (1 << len(pts)) - 1
    field = "tre_7_12" if tre_em else "nguoi_lon"

    options: list[tuple[int, int, str, str]] = []
    for d in pts:
        options.append((1 << idx[d], QUAN_THE_DIEM[d][field], f"Vé lẻ {QUAN_THE_DIEM[d]['ten']}", "trong ngày"))
    for t in QUAN_THE_TUYEN:
        mask = 0
        for d in t.diem:
            if d in idx:
                mask |= 1 << idx[d]
        if mask:
            options.append((mask, getattr(t, field), t.ten, t.han))

    inf = (10**12, 10**6)
    dp: list[tuple[int, int]] = [inf] * (full + 1)
    choice: list[tuple[int, tuple[int, str, str, int]] | None] = [None] * (full + 1)
    dp[0] = (0, 0)

    for mask in range(full):
        cost_m, cnt_m = dp[mask]
        if cost_m >= 10**12:
            continue
        for opt_mask, price, ten, han in options:
            nxt = mask | opt_mask
            if nxt == mask:
                continue
            cand = (cost_m + price, cnt_m + 1)
            if cand < dp[nxt]:
                dp[nxt] = cand
                choice[nxt] = (mask, (price, ten, han, opt_mask))

    picked: list[tuple[str, str, int]] = []
    cur = full
    while cur:
        step = choice[cur]
        assert step is not None
        prev, (price, ten, han, _) = step
        picked.append((ten, han, price))
        cur = prev
    picked.reverse()
    return dp[full][0], tuple(picked)


def _gio_va_thoi_luong(diem_id: str, bang_v2) -> tuple[tuple[tuple[str, str], ...], int, str]:
    info = QUAN_THE_DIEM.get(diem_id) or DIEM_NGOAI[diem_id]
    v16_id = diem_id if diem_id in QUAN_THE_DIEM else info.get("diem_v16_id")
    gio_mo = info["gio_mo"]
    phut = info["phut"]
    gio_text = ""
    if bang_v2 is not None and v16_id and v16_id in bang_v2.theo_id:
        row = bang_v2.theo_id[v16_id]
        if row.get("gio_mo"):
            gio_mo = tuple((a, b) for a, b in row["gio_mo"])
        if row.get("thoi_luong") == "ngan":
            phut = 75
        elif row.get("thoi_luong") == "nua_buoi":
            phut = 150
        if row.get("gio_mo_cua"):
            gio_text = str(row["gio_mo_cua"])
    return gio_mo, phut, gio_text


def _the_noi_dong(diem_id: str, the_noi_bang) -> str:
    if the_noi_bang is None:
        return ""
    ten = (QUAN_THE_DIEM.get(diem_id) or DIEM_NGOAI[diem_id])["ten"]
    for noi in getattr(the_noi_bang, "noi", ()):
        if noi.ten == ten or noi.ten.startswith(ten):
            return " · ".join(noi.dong)
    return ""


def _gia_ngoai(diem_id: str, nguoi_lon: int, cao_tuoi_vn: int, tre_7_12: int, la_vn: bool, cu_tru_hue: bool) -> tuple[str, int | None]:
    """Trả `(tổng chi phí đọc dễ hiểu, số tiền ước tính nếu xác định chính xác một mức | None)`."""
    if diem_id == "hai_van_quan":
        # <13t miễn phí (trẻ 7–12t vào Hải Vân Quan miễn phí)
        tien_nl = 70_000 * nguoi_lon
        tien_ct = (35_000 if la_vn else 70_000) * cao_tuoi_vn
        tong = tien_nl + tien_ct
        chi_tiet = f"Hải Vân Quan (tách riêng, KHÔNG thuộc vé gộp Quần thể): {_dinh_dang_tien(tong)}"
        chi_tiet += f" (người lớn >=13t: 70.000đ × {nguoi_lon}"
        if cao_tuoi_vn:
            chi_tiet += f"; công dân VN >=60t: 35.000đ × {cao_tuoi_vn}" if la_vn else f"; khách nước ngoài >=60t: 70.000đ × {cao_tuoi_vn}"
        if tre_7_12:
            chi_tiet += f"; trẻ 7–12t (<13t): 0đ × {tre_7_12}"
        return chi_tiet + ").", tong
    if diem_id == "duyet_thi_duong":
        tong_show = 300_000 * (nguoi_lon + cao_tuoi_vn + tre_7_12)
        return (
            f"Nhà hát Duyệt Thị Đường: 300.000đ/suất × {nguoi_lon + cao_tuoi_vn + tre_7_12} = {_dinh_dang_tien(tong_show)} "
            "(cần mua thêm vé vào Đại Nội nếu chưa có).",
            tong_show,
        )
    if diem_id == "kg_le_ba_dang":
        don_gia = 120_000 if cu_tru_hue else 200_000
        tong = don_gia * (nguoi_lon + cao_tuoi_vn + tre_7_12)
        nhan = "cư dân Huế 120.000đ" if cu_tru_hue else "tiêu chuẩn 200.000đ"
        return f"Không gian lưu niệm Lê Bá Đảng ({nhan}): {_dinh_dang_tien(tong)}.", tong
    if diem_id == "alba_thanh_tan":
        tong = 230_000 * (nguoi_lon + cao_tuoi_vn) + 115_000 * tre_7_12
        return (
            f"Alba Thanh Tân (tạm tính theo chiều cao >1,4 m cho người lớn và 1,2–1,4 m cho trẻ 7–12t; <1,2 m miễn phí): {_dinh_dang_tien(tong)}.",
            tong,
        )
    return f"{DIEM_NGOAI[diem_id]['ten']}: {DIEM_NGOAI[diem_id]['ghi_chu']}", None


def ket_qua(
    diem: Sequence[str],
    ngay: str = "",
    gio_bat_dau: str = "",
    so_nguoi_lon: int = 1,
    so_tre_7_12: int = 0,
    so_tre_duoi_7: int = 0,
    so_nguoi_cao_tuoi_vn: int = 0,
    la_cong_dan_vn: bool = True,
    cu_tru_hue: bool = False,
    bang_v2=None,
    the_noi_bang=None,
) -> tuple[str, tuple[str, ...]]:
    """Tính vé + kiểm tra giờ mở cửa/ngày lễ; trả `(văn_bản_kết_quả, tuple_đường_dẫn_bài_kho)`."""
    hop_le: list[str] = []
    bo_qua: list[str] = []
    for raw in diem or ():
        cid = chuan_diem(raw)
        if cid:
            if cid not in hop_le:
                hop_le.append(cid)
        elif str(raw).strip():
            bo_qua.append(str(raw).strip())

    # Duyệt Thị Đường nằm trong Đại Nội Huế: luôn nhắc vé Đại Nội nếu chưa có
    nhac_dai_noi_cho_duyet = "duyet_thi_duong" in hop_le and "dai_noi" not in hop_le

    nguoi_lon = max(int(so_nguoi_lon or 0), 0)
    tre_7_12 = max(int(so_tre_7_12 or 0), 0)
    tre_duoi_7 = max(int(so_tre_duoi_7 or 0), 0)
    cao_tuoi = max(int(so_nguoi_cao_tuoi_vn or 0), 0)
    if nguoi_lon + tre_7_12 + tre_duoi_7 + cao_tuoi == 0:
        nguoi_lon = 1

    quan_the = [d for d in hop_le if d in QUAN_THE_DIEM]
    ngoai = [d for d in hop_le if d in DIEM_NGOAI]

    ngay_d = parse_ngay(ngay)
    start_min = parse_gio_phut(gio_bat_dau)

    dong: list[str] = []
    if not hop_le:
        dong.append("Chưa nhận diện được điểm tham quan hợp lệ nào trong yêu cầu; hãy truyền mã điểm hợp lệ hoặc tra kho.")
        return "\n".join(dong), (NGUON_QUAN_THE,)

    sources: list[str] = []
    if quan_the:
        sources.append(NGUON_QUAN_THE)
    for d in ngoai:
        src = DIEM_NGOAI[d]["nguon"]
        if src not in sources:
            sources.append(src)
    if not sources:
        sources.append(NGUON_QUAN_THE)

    dong.append(
        f"Thông số tính: {len(hop_le)} điểm | Người lớn (13–59t / ngoài diện ưu đãi): {nguoi_lon}, "
        f"Công dân VN >=60t: {cao_tuoi}, Trẻ 7–12t: {tre_7_12}, Trẻ <7t (hoặc <1,2 m): {tre_duoi_7} | "
        f"Quốc tịch VN: {'có' if la_cong_dan_vn else 'không'}."
    )
    if bo_qua:
        dong.append(f"Điểm ngoài bảng tính (chưa áp bảng giá cố định): {', '.join(bo_qua)}.")

    mien_qt = mien_hvq = False
    ten_le: str | None = None
    if ngay_d is not None:
        mien_qt, mien_hvq, ten_le = kiem_tra_ngay_le_vn(ngay_d)
        dong.append(f"Ngày dự kiến: {ngay_d.strftime('%d/%m/%Y')} ({_THU_VIET[ngay_d.weekday()]}).")
        if ten_le:
            if la_cong_dan_vn:
                dong.append(
                    f"NGÀY LỄ MIỄN PHÍ CHO CÔNG DÂN VIỆT NAM — {ten_le}: "
                    "miễn phí 100% vé vào cửa cho công dân VN (07:00–17:30, xuất trình CCCD hoặc VNeID mức độ 2)."
                )
            else:
                dong.append(
                    f"Lưu ý ngày {ngay_d.strftime('%d/%m/%Y')} là {ten_le}: "
                    "chính sách miễn phí ngày lễ chỉ áp dụng cho công dân Việt Nam, khách quốc tế vẫn mua vé bình thường."
                )
    elif ngay.strip():
        dong.append(f"Chưa đọc được định dạng ngày '{ngay}' (nên dùng YYYY-MM-DD hoặc DD/MM/YYYY).")

    tong_uoc_tinh = 0

    # 1. Tính phần Quần thể Di tích Cố đô Huế
    if quan_the:
        dong.append("\n[Quần thể Di tích Cố đô Huế — NQ 55/2025/NQ-HĐND, hiệu lực 04/01/2026]")
        le_nl = sum(QUAN_THE_DIEM[d]["nguoi_lon"] for d in quan_the)
        le_te = sum(QUAN_THE_DIEM[d]["tre_7_12"] for d in quan_the)
        for d in quan_the:
            info = QUAN_THE_DIEM[d]
            dong.append(
                f"- {info['ten']}: vé lẻ người lớn {_dinh_dang_tien(info['nguoi_lon'])}, "
                f"trẻ 7–12t {_dinh_dang_tien(info['tre_7_12']) if info['tre_7_12'] else 'Miễn phí'}"
            )

        opt_nl, goi_nl = toi_uu_quan_the(quan_the, tre_em=False)
        opt_te, goi_te = toi_uu_quan_the(quan_the, tre_em=True)
        dong.append(
            f"- So sánh 1 người lớn: mua vé lẻ = {_dinh_dang_tien(le_nl)} | "
            f"phương án tối ưu = {_dinh_dang_tien(opt_nl)} ({' + '.join(f'{ten} [{han}: {_dinh_dang_tien(gia)}]' for ten, han, gia in goi_nl)})."
        )
        if tre_7_12 > 0:
            dong.append(
                f"- So sánh 1 trẻ em 7–12 tuổi: mua vé lẻ = {_dinh_dang_tien(le_te)} | "
                f"phương án tối ưu = {_dinh_dang_tien(opt_te)} ({' + '.join(f'{ten} [{han}: {_dinh_dang_tien(gia)}]' for ten, han, gia in goi_te)})."
            )
        if tre_duoi_7 > 0:
            dong.append(f"- Trẻ em <7 tuổi (hoặc <1,2 m) ({tre_duoi_7} bé): Miễn phí 0đ tại mọi điểm Quần thể.")

        if mien_qt and la_cong_dan_vn:
            tien_qt = 0
            dong.append("=> Tổng vé Quần thể ngày lễ (công dân VN): 0đ.")
        else:
            don_cao_tuoi = opt_nl // 2 if la_cong_dan_vn else opt_nl
            tien_qt = nguoi_lon * opt_nl + cao_tuoi * don_cao_tuoi + tre_7_12 * opt_te
            parts = []
            if nguoi_lon:
                parts.append(f"{nguoi_lon} người lớn × {_dinh_dang_tien(opt_nl)}")
            if cao_tuoi:
                if la_cong_dan_vn:
                    parts.append(f"{cao_tuoi} người cao tuổi VN (giảm 50%) × {_dinh_dang_tien(don_cao_tuoi)}")
                else:
                    parts.append(f"{cao_tuoi} khách >=60t nước ngoài (không giảm) × {_dinh_dang_tien(don_cao_tuoi)}")
            if tre_7_12:
                parts.append(f"{tre_7_12} trẻ 7–12t × {_dinh_dang_tien(opt_te)}")
            dong.append(f"=> Tổng vé Quần thể ước tính theo phương án tối ưu: {_dinh_dang_tien(tien_qt)} ({' + '.join(parts)}).")
        tong_uoc_tinh += tien_qt

        # Cảnh báo 530k khi có >= 2 trong 4 điểm trọng điểm hoặc hỏi nhiều điểm
        diem_4 = {"dai_noi", "lang_minh_mang", "lang_tu_duc", "lang_khai_dinh"}
        if len(set(quan_the) & diem_4) >= 2 or len(quan_the) >= 4:
            dong.append(CANH_BAO_530K)

    if cao_tuoi > 0:
        if la_cong_dan_vn:
            dong.append(f"Điều kiện giảm 50% người cao tuổi: {DIEU_KIEN_CAO_TUOI_VN}")
        else:
            dong.append(f"Lưu ý người cao tuổi: chính sách giảm 50% chỉ áp dụng cho {DIEU_KIEN_CAO_TUOI_VN}")

    # 2. Tính phần điểm ngoài Quần thể
    if ngoai:
        dong.append("\n[Điểm tham quan / trải nghiệm tách riêng ngoài vé Quần thể]")
        for d in ngoai:
            if d == "hai_van_quan" and mien_hvq and la_cong_dan_vn:
                dong.append("- Hải Vân Quan (tách riêng, KHÔNG thuộc vé gộp Quần thể): 0đ (miễn phí ngày lễ cho công dân VN, xuất trình CCCD/VNeID mức 2).")
                continue
            dong_gia, so_tien = _gia_ngoai(d, nguoi_lon, cao_tuoi, tre_7_12, la_cong_dan_vn, cu_tru_hue)
            dong.append(f"- {dong_gia}")
            if so_tien is not None:
                tong_uoc_tinh += so_tien

    if nhac_dai_noi_cho_duyet:
        dong.append("Lưu ý Duyệt Thị Đường: cần thêm vé vào cửa Đại Nội Huế (200.000đ người lớn, 40.000đ trẻ 7–12 tuổi).")

    if quan_the or ngoai:
        dong.append(f"\nTổng vé ước tính các mục xác định được giá: {_dinh_dang_tien(tong_uoc_tinh)}.")

    # 3. Kiểm tra giờ mở cửa, ngày nghỉ định kỳ & thời lượng
    dong.append("\n[Giờ mở cửa & kiểm tra kịp giờ]")
    cur_min = start_min
    for d in hop_le:
        ten = (QUAN_THE_DIEM.get(d) or DIEM_NGOAI[d])["ten"]
        gio_mo, phut, gio_text = _gio_va_thoi_luong(d, bang_v2)
        the_noi = _the_noi_dong(d, the_noi_bang)
        mo_str = ", ".join(f"{a}–{b}" for a, b in gio_mo) if gio_mo else "xem theo suất/khung hoạt động"
        dong_gio = f"- {ten}: giờ mở {mo_str} (thời lượng tham quan gợi ý ~{phut} phút)"
        if gio_text:
            dong_gio += f" · {gio_text}"
        elif the_noi:
            dong_gio += f" · {the_noi}"
        dong.append(dong_gio)

        if ngay_d is not None and d in DIEM_NGOAI and ngay_d.weekday() in DIEM_NGOAI[d]["ngay_nghi"]:
            dong.append(f"  -> CẢNH BÁO NGÀY NGHỈ: {ten} ĐÓNG CỬA vào {_THU_VIET[ngay_d.weekday()]} ({ngay_d.strftime('%d/%m/%Y')})!")

        if cur_min is not None and gio_mo:
            if d == "duyet_thi_duong":
                suat_bat_dau = [parse_gio_phut(a) for a, _ in gio_mo]
                hop = [s for s in suat_bat_dau if s is not None and cur_min <= s]
                if not hop:
                    dong.append(f"  -> CẢNH BÁO GIỜ SUẤT DIỄN: xuất phát lúc {_phut_sang_chuoi(cur_min)} đã qua 2 suất cố định 10:00 và 15:00.")
                continue
            if d == "ca_hue_song_huong":
                continue
            khop_cua = False
            dong_muon = max((parse_gio_phut(b) or 0) for _, b in gio_mo)
            for a, b in gio_mo:
                m_a, m_b = parse_gio_phut(a), parse_gio_phut(b)
                if m_a is not None and m_b is not None and cur_min < m_b:
                    bat_dau = max(cur_min, m_a)
                    ket_thuc = bat_dau + phut
                    if ket_thuc <= m_b:
                        khop_cua = True
                        cur_min = ket_thuc + 15  # 15p di chuyển tối thiểu giữa hai điểm
                        break
            if not khop_cua:
                if cur_min >= dong_muon:
                    dong.append(f"  -> CẢNH BÁO ĐÓNG CỬA: lúc {_phut_sang_chuoi(cur_min)} điểm {ten} đã đóng cửa ({mo_str}).")
                else:
                    dong.append(
                        f"  -> CẢNH BÁO KHÔNG KỊP THỜI LƯỢNG: bắt đầu từ {_phut_sang_chuoi(cur_min)} cần ~{phut} phút, "
                        f"sẽ vượt quá giờ đóng cửa {_phut_sang_chuoi(dong_muon)}."
                    )

    dong.append("Nguồn kho: " + ", ".join(TEN_NGUON[s] for s in sources) + ".")
    return "\n".join(dong), tuple(sources)


_EXAMPLE = (
    'Ví dụ: diem=["dai_noi", "lang_minh_mang", "lang_tu_duc", "lang_khai_dinh"], '
    'ngay="2026-09-02", gio_bat_dau="08:00", so_nguoi_lon=2, so_tre_7_12=1, so_nguoi_cao_tuoi_vn=1.'
)


def mo_ta_cong_cu(toi_uu: bool = False) -> str:
    """Mô tả công cụ gửi model (giữ gọn để ổn định prompt cache prefix)."""
    ds_qt = ", ".join(QUAN_THE_DIEM)
    ds_ng = ", ".join(DIEM_NGOAI)
    than = (
        "Tính chính xác giá vé tham quan Huế (vé lẻ 12 điểm Quần thể vs tuyến gộp tối ưu 2/3/4/12 điểm, tách riêng Hải Vân Quan và 8 điểm khác), "
        "ưu đãi trẻ em, giảm 50% công dân VN >=60 tuổi, 5 ngày lễ miễn phí công dân VN và kiểm tra ngày đóng cửa / kịp giờ đóng cửa."
        if toi_uu
        else (
            "Tính giá vé tham quan Huế, chọn vé lẻ hay tuyến gộp rẻ nhất (12 điểm Quần thể, tách riêng Hải Vân Quan), "
            "kiểm tra ngày lễ miễn phí, ngày đóng cửa và kịp giờ đóng cửa."
        )
    )
    return f"{than}\nMã điểm Quần thể: {ds_qt}.\nMã điểm/trải nghiệm khác: {ds_ng}.\n{_EXAMPLE}"
