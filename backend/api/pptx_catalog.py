"""Danh mục bảng màu (3 theme) và bố cục (9 layout) cho `.pptx` v2 (Đợt 5 — Phần A).

Không chứa ghi công tác giả / giấy phép ảnh (quyết định chủ dự án 14/11 & 19/11).
Mọi toạ độ khung chữ được khai báo tập trung tại `LAYOUT_SPECS` để `pptx_fit.py` và `lich_pptx.py` dùng chung.
"""

RONG = 13.333  # inch (16:9)
CAO = 7.5      # inch (16:9)
PHONG_TD = "Georgia"
PHONG = "Arial"

# 3 bảng màu chuẩn hoá
THEMES: dict[str, dict[str, str]] = {
    "di_san_tram": {
        "ten": "Di sản trầm",
        "nen": "FAF6EE",
        "chinh": "5B2333",
        "phu": "8C4A32",
        "nhan": "B8860B",
        "nhat": "EFE8D8",
        "hoa_tiet": "D8CEBC",
        "chu": "231F20",
        "chu_phu": "5C5346",
        "sang": "B8860B",
        "chieu": "A75B43",
        "toi": "34495E",
        "trang": "FFFFFF",
    },
    "song_huong_xanh": {
        "ten": "Sông Hương xanh",
        "nen": "F7F9F8",
        "chinh": "1E4D4B",
        "phu": "2B7A78",
        "nhan": "D4A359",
        "nhat": "E4EFEA",
        "hoa_tiet": "CBE0DA",
        "chu": "1D2A29",
        "chu_phu": "4A6360",
        "sang": "C88A2E",
        "chieu": "2B7A78",
        "toi": "243B53",
        "trang": "FFFFFF",
    },
    "co_do_hien_dai": {
        "ten": "Cố đô hiện đại",
        "nen": "FCFBF9",
        "chinh": "2B2D42",
        "phu": "C85A32",
        "nhan": "E09F3E",
        "nhat": "F2ECE4",
        "hoa_tiet": "E2D7CA",
        "chu": "222228",
        "chu_phu": "5E5C64",
        "sang": "C85A32",
        "chieu": "8D5B4C",
        "toi": "3D405B",
        "trang": "FFFFFF",
    },
}

ALLOWED_THEMES = frozenset(THEMES)

ALLOWED_LAYOUTS_BY_KIND: dict[str, tuple[str, ...]] = {
    "cover": ("cover_hero", "cover_split"),
    "overview": ("overview_route",),
    "day": ("day_timeline", "day_cards_2col", "day_photo_feature", "day_compact_grid"),
    "lodging": ("lodging_dining",),
    "notes": ("notes_map",),
}

ALL_LAYOUTS = frozenset(lay for lays in ALLOWED_LAYOUTS_BY_KIND.values() for lay in lays)

# Đặc tả hình học (width_in, height_in, base_pt, min_pt, max_chars_hint) cho từng slot của 9 layout.
LAYOUT_SPECS: dict[str, dict[str, tuple[float, float, float, float, int]]] = {
    "cover_hero": {
        "title": (4.3, 1.9, 36.0, 24.0, 56),
        "subtitle": (4.3, 0.9, 15.0, 11.5, 95),
        "highlights": (4.3, 1.4, 13.0, 10.5, 110),
        "an_toan": (7.3, 0.78, 10.5, 8.5, 220),
    },
    "cover_split": {
        "title": (4.2, 2.0, 38.0, 24.0, 52),
        "subtitle": (4.2, 0.9, 16.0, 11.5, 90),
        "highlights": (4.2, 1.4, 13.5, 10.5, 110),
        "an_toan": (6.85, 0.84, 10.5, 8.5, 220),
    },
    "overview_route": {
        "header": (11.8, 0.7, 26.0, 18.0, 60),
        "day_title": (2.2, 0.48, 14.0, 11.0, 32),
        "day_route": (9.2, 0.52, 13.0, 10.0, 130),
    },
    "day_timeline": {
        "day_header": (2.0, 1.2, 28.0, 20.0, 28),
        "route_summary": (2.0, 2.2, 12.5, 10.0, 90),
        "item_title": (4.7, 0.38, 15.5, 12.0, 52),
        "item_copy": (4.7, 0.75, 11.5, 9.5, 135),
        "dining_note": (7.4, 0.85, 11.5, 9.5, 160),
    },
    "day_cards_2col": {
        "day_header": (12.0, 0.55, 24.0, 18.0, 55),
        "route_summary": (12.0, 0.35, 12.5, 10.0, 95),
        "item_title": (3.7, 0.42, 14.5, 11.5, 48),
        "item_copy": (3.7, 1.15, 11.5, 9.5, 140),
        "dining_note": (11.8, 0.55, 11.5, 9.5, 180),
    },
    "day_photo_feature": {
        "day_header": (6.2, 0.65, 26.0, 19.0, 48),
        "route_summary": (6.2, 0.42, 13.0, 10.5, 80),
        "item_title": (6.0, 0.45, 17.0, 13.0, 52),
        "item_copy": (6.0, 1.35, 13.0, 10.0, 175),
        "dining_note": (6.0, 0.85, 12.0, 9.5, 160),
    },
    "day_compact_grid": {
        "day_header": (12.0, 0.5, 23.0, 17.0, 55),
        "route_summary": (12.0, 0.32, 12.0, 10.0, 95),
        "item_title": (4.1, 0.34, 13.0, 10.5, 46),
        "item_copy": (4.1, 0.72, 10.5, 8.8, 115),
        "dining_note": (11.8, 0.52, 11.0, 9.0, 180),
    },
    "lodging_dining": {
        "header": (12.0, 0.65, 26.0, 18.0, 60),
        "lodging_meta": (3.55, 1.1, 11.5, 9.5, 110),
        "dining_summary": (11.8, 1.25, 11.5, 9.5, 220),
        "disclaimer": (11.8, 0.42, 11.0, 9.0, 140),
    },
    "notes_map": {
        "header": (10.5, 0.7, 26.0, 18.0, 50),
        "an_toan": (11.6, 0.72, 11.5, 9.5, 240),
        "notes_body": (7.2, 3.85, 12.5, 9.5, 520),
    },
}


def chon_theme_mac_dinh(tham_so: dict | None) -> str:
    """Chọn theme mặc định theo sở thích / kiểu đi trong `tham_so`."""
    ts = tham_so or {}
    so_thich = set(ts.get("so_thich") or [])
    kieu = ts.get("kieu_di")
    if so_thich & {"am_thuc", "chup_anh"} or kieu == "kham_pha":
        return "co_do_hien_dai"
    if "thien_nhien" in so_thich or kieu == "nhe_nhang" or ts.get("tre_em") or ts.get("lon_tuoi"):
        return "song_huong_xanh"
    return "di_san_tram"


def chon_layout_ngay(ngay_dict: dict, *, co_anh: bool) -> str:
    """Bộ chọn layout theo đặc trưng ngày (dùng cho chế độ thuần code và fallback)."""
    muc = [m for m in (ngay_dict.get("muc") or []) if m.get("loai") != "nghi"]
    n = len(muc)
    if n <= 2 and co_anh:
        return "day_photo_feature"
    if n in (2, 4) and co_anh:
        return "day_cards_2col"
    if n >= 5:
        return "day_compact_grid"
    return "day_timeline"
