"""Gợi ý nơi ở trong lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-luu-tru-trong-lich-plan.md`, cờ `luu_tru_lich`).

Mọi thứ do code: chọn MỘT khu cho cả chuyến theo cụm của các điểm ban ngày, chọn ≤ 5 cơ sở trải theo hạng trong khu đó, viết lý do,
dựng link tìm phòng. Model không chọn, không viết tên cơ sở; khối này không vào tin nhắn gửi model. Không giá, không "còn phòng".
Bảng: `bang_luu_tru_lich_v2.json` = bảng E (danh mục công khai, có nguồn + ngày; khu theo `cum_ve_khu` của C) + toạ độ Places + ảnh đã duyệt (B 14/11).
"""
import datetime as dt
import itertools
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, quote, quote_plus, unquote, urlencode, urlparse, urlunparse

from llm.lich_trinh import MAP_BASE

KHU_LOI = "loi_do_thi_hai_bo_song_huong"
KHU_TAY = "phia_tay_yen_tinh"
KHU_BIEN = "ven_bien_dam_pha_lang_co"
TEN_KHU = {KHU_LOI: "trung tâm, hai bờ sông Hương", KHU_TAY: "phía tây yên tĩnh (Kim Long, Thủy Xuân)", KHU_BIEN: "ven biển, đầm phá"}
NGUONG_TAY = 0.5   # phía tây chỉ khi > 50 % điểm ban ngày ở phía tây VÀ không có trẻ em / người lớn tuổi
NGUONG_BIEN = 0.6  # ven biển chỉ khi ≥ 60 % điểm ban ngày ở ven biển (ngày ra biển thường là đi trong ngày)
# Trải theo hạng để khách tự chọn: tối đa 2 cơ sở 4–5 sao · 2 cơ sở 2–3 sao · 1 cơ sở 1 sao / đạt chuẩn
MUC_HANG = {"5 sao": 0, "4 sao": 0, "3 sao": 1, "2 sao": 1, "1 sao": 2, "Đạt chuẩn phục vụ khách du lịch": 2}
SO_THEO_MUC = (2, 2, 1)
# Người dùng chọn mức chỗ ở (biểu mẫu, nhãn kèm hạng sao — hạng ≠ giá) ⇒ ≤ 5 cơ sở của riêng mức đó; khu không có mức đó ⇒ im lặng về SO_THEO_MUC
MUC_NGAN_SACH = {"cao": 0, "vua": 1, "binh_dan": 2}
# Khu ven biển gộp hai phía cách nhau ~40 km (Thuận An / Tam Giang ↔ Lăng Cô) ⇒ chỉ gợi ý cơ sở cùng phía (`phia_bien` của bảng v3, cùng trường trang
# "Chỗ ở" dùng) với cụm có nhiều điểm nhất. Trước 15/11 tách theo chữ trong địa chỉ — cơ sở có địa chỉ không ghi tên huyện bị bỏ sót.
CUM_DI_TRONG_NGAY = {"nam_xa"}
PHIA_CUM = {"dong_bien": "bac", "nam_xa": "nam"}
LINK_TIM = "https://www.booking.com/searchresults.html?ss="  # link tìm (không đặt chỗ), chỉ mở khi người dùng bấm
ALLOWED_OTA_HOSTS = frozenset({"www.booking.com", "www.agoda.com", "www.traveloka.com"})
_CTRL_CHARS = re.compile(r"[\x00-\x1f\x7f]+")
ANH_GOC = "/anh/khach_san/"  # ảnh tự host (1 agent con chọn + B nhìn lại 14/11); bảng ghi đường khác gốc này ⇒ không khởi động
NHAN = "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống."


def sach_chuoi_tham_so(chuoi: str | None) -> str:
    """Làm sạch ký tự điều khiển (`\\r\\n\\0`), chuẩn hoá NFC, loại `..` và gộp khoảng trắng thừa trước khi đưa vào URL/template."""
    sach = _CTRL_CHARS.sub(" ", unicodedata.normalize("NFC", str(chuoi or "")))
    while ".." in sach:
        sach = sach.replace("..", " ")
    return " ".join(sach.split()).strip()


def kiem_tra_ota_url(url: str | None) -> str | None:
    """Xác thực URL OTA: phải là `https`, host thuộc `ALLOWED_OTA_HOSTS`, không chứa ký tự điều khiển, `javascript:` hay `..` (kể cả đã percent-encode)."""
    if not isinstance(url, str):
        return None
    raw = url.strip()
    if not raw or _CTRL_CHARS.search(raw) or raw.lower().startswith("javascript:"):
        return None
    parsed = urlparse(raw)
    if parsed.scheme != "https" or parsed.netloc.lower() not in ALLOWED_OTA_HOSTS:
        return None
    raw_decoded = unquote(raw)
    if ".." in raw or ".." in raw_decoded or "%2e%2e" in raw.lower():
        return None
    return raw


link_phong_hop_le = kiem_tra_ota_url


def _booking_url(ten: str, checkin: str | None, checkout: str | None, adults: int, children: int, rooms: int) -> str:
    params: dict[str, str | int] = {"ss": f"{ten}, Huế", "lang": "vi"}
    if checkin and checkout:
        params["checkin"] = checkin
        params["checkout"] = checkout
    params["group_adults"] = adults
    params["group_children"] = children
    params["no_rooms"] = rooms
    url = f"https://www.booking.com/searchresults.html?{urlencode(params, quote_via=quote_plus)}"
    return kiem_tra_ota_url(url) or (LINK_TIM + quote(f"{ten}, Huế"))


def _agoda_url(ten: str, checkin: str | None, checkout: str | None, so_ngay: int, adults: int, children: int, rooms: int,
               anh_trang: str | None = None) -> str:
    params: list[tuple[str, str | int]] = []
    co_ngay = bool(checkin and checkout)
    base_hop_le = kiem_tra_ota_url(anh_trang)
    if base_hop_le and urlparse(base_hop_le).netloc.lower() == "www.agoda.com":
        p = urlparse(base_hop_le)
        params.extend(parse_qsl(p.query, keep_blank_values=True))
        if co_ngay:
            params.extend([("checkIn", checkin), ("los", max(1, so_ngay))])
        params.extend([("adults", adults), ("children", children), ("rooms", rooms)])
        url = urlunparse((p.scheme, p.netloc, p.path, p.params, urlencode(params, quote_via=quote_plus), ""))
    else:
        params.append(("textToSearch", f"{ten} Huế"))
        if co_ngay:
            params.extend([("checkIn", checkin), ("los", max(1, so_ngay))])
        params.extend([("adults", adults), ("children", children), ("rooms", rooms)])
        url = f"https://www.agoda.com/search?{urlencode(params, quote_via=quote_plus)}"
    return kiem_tra_ota_url(url) or f"https://www.agoda.com/search?{urlencode({'textToSearch': f'{ten} Huế'}, quote_via=quote_plus)}"


def _traveloka_url(ten: str, checkin: str | None, checkout: str | None, adults: int, children: int, rooms: int) -> str:
    params: dict[str, str | int] = {"q": f"{ten} Huế"}
    if checkin and checkout:
        params["checkin"] = checkin
        params["checkout"] = checkout
    params["adults"] = adults
    params["children"] = children
    params["rooms"] = rooms
    url = f"https://www.traveloka.com/vi-vn/hotel/search?{urlencode(params, quote_via=quote_plus)}"
    return kiem_tra_ota_url(url) or f"https://www.traveloka.com/vi-vn/hotel/search?{urlencode({'q': f'{ten} Huế'}, quote_via=quote_plus)}"


def tao_deep_links_co_so(
    ten: str,
    *,
    ngay_di: str | None = None,
    so_ngay: int = 2,
    nguoi_lon: int = 2,
    tre_em: int = 0,
    anh_trang: str | None = None,
) -> dict[str, str]:
    """Sinh bộ 3 Deep Link OTA (`booking`, `agoda`, `traveloka`) xác định (`0 USD`), đã làm sạch và kiểm allowlist host."""
    ten_sach = sach_chuoi_tham_so(ten) or "Huế"
    so_dem = max(1, int(so_ngay or 2) - 1) if int(so_ngay or 2) >= 2 else 1
    adults = max(1, int(nguoi_lon or 2))
    children = max(0, int(tre_em or 0))
    rooms = max(1, math.ceil(adults / 2))
    checkin = checkout = None
    if ngay_di:
        try:
            d_in = dt.date.fromisoformat(str(ngay_di))
            d_out = d_in + dt.timedelta(days=so_dem)
            checkin, checkout = d_in.isoformat(), d_out.isoformat()
        except ValueError:
            checkin = checkout = None
    return {
        "booking": _booking_url(ten_sach, checkin, checkout, adults, children, rooms),
        "agoda": _agoda_url(ten_sach, checkin, checkout, so_dem, adults, children, rooms, anh_trang=anh_trang),
        "traveloka": _traveloka_url(ten_sach, checkin, checkout, adults, children, rooms),
    }


def tao_deep_links(ten: str, tham_so: dict | None = None, *, anh_trang: str | None = None) -> dict[str, str]:
    """Wrapper tương thích hợp đồng nhận `(ten, tham_so)` và trả dict 3 sàn OTA (`booking`, `agoda`, `traveloka`)."""
    ts = tham_so or {}
    return tao_deep_links_co_so(
        ten,
        ngay_di=ts.get("ngay_di"),
        so_ngay=int(ts.get("so_ngay") or 2),
        nguoi_lon=int(ts.get("nguoi_lon") or 2),
        tre_em=int(ts.get("tre_em") or 0),
        anh_trang=anh_trang,
    )


def tao_mau_hoi_phong(
    ten: str,
    *,
    dia_chi: str | None = None,
    ngay_di: str | None = None,
    so_ngay: int = 2,
    nguoi_lon: int = 2,
    tre_em: int = 0,
    lon_tuoi: bool = False,
) -> str:
    """Sinh mẫu tin nhắn hỏi phòng tiếng Việt xác định (`0 USD`) đủ 6 trường, không bịa giá hay email."""
    ten_sach = sach_chuoi_tham_so(ten) or "Cơ sở lưu trú"
    dc_sach = sach_chuoi_tham_so(dia_chi)
    so_dem = max(1, int(so_ngay or 2) - 1) if int(so_ngay or 2) >= 2 else 1
    adults = max(1, int(nguoi_lon or 2))
    children = max(0, int(tre_em or 0))

    if ngay_di:
        try:
            d_in = dt.date.fromisoformat(str(ngay_di))
            d_out = d_in + dt.timedelta(days=so_dem)
            nhan_tra = f"Nhận phòng: {d_in:%d/%m/%Y} · Trả phòng: {d_out:%d/%m/%Y} ({so_dem} đêm)"
        except ValueError:
            nhan_tra = f"Nhận/trả phòng: [chọn ngày đi] ({so_dem} đêm)"
    else:
        nhan_tra = f"Nhận phòng: [chọn ngày] · Trả phòng: [sau {so_dem} đêm] ({so_dem} đêm)"

    doan_parts = [f"{adults} người lớn"]
    if children > 0:
        doan_parts.append(f"{children} trẻ em")
    if lon_tuoi:
        doan_parts.append("có người lớn tuổi")
    doan = ", ".join(doan_parts)

    yeu_cau = []
    if lon_tuoi:
        yeu_cau.append("ưu tiên phòng tầng thấp hoặc gần thang máy, yên tĩnh cho người lớn tuổi")
    if children > 0:
        yeu_cau.append("hỏi thêm chính sách phụ thu trẻ em / giường phụ")
    dong_yeu_cau = f"- Yêu cầu đặc biệt: {'; '.join(yeu_cau)}." if yeu_cau else "- Yêu cầu đặc biệt: phòng sạch sẽ, yên tĩnh."

    dong = [
        f"Xin chào {ten_sach}" + (f" ({dc_sach})" if dc_sach else "") + ",",
        f"- Thời gian lưu trú: {nhan_tra}.",
        f"- Cơ cấu đoàn: {doan}.",
        dong_yeu_cau,
        "- Nhờ cơ sở xác nhận giúp: tình trạng phòng trống cho các ngày trên, tổng giá đã bao gồm thuế/phí, giờ nhận/trả phòng tiêu chuẩn, chính sách bữa sáng và điều kiện huỷ phòng.",
        "Xin cảm ơn!",
    ]
    return "\n".join(dong)


def gan_xuat_nang_cao_o_dau(o: dict | None, tham_so: dict | None = None, *, bang_luu_tru: dict | None = None) -> dict | None:
    """Bổ sung `deep_links` (3 sàn OTA) và `mau_hoi_phong` cho từng cơ sở trong `o_dau` khi cờ `xuat_nang_cao` bật."""
    if not isinstance(o, dict):
        return o
    ts = tham_so or {}
    anh_trang_theo_ten = {c["ten"]: c.get("anh_trang") for c in (bang_luu_tru or {}).get("co_so", []) if c.get("ten")}
    ngay_di = ts.get("ngay_di")
    so_ngay = int(ts.get("so_ngay") or 2)
    nguoi_lon = int(ts.get("nguoi_lon") or 2)
    tre_em = int(ts.get("tre_em") or 0)
    lon_tuoi = bool(ts.get("lon_tuoi", False))
    for c in o.get("co_so") or []:
        c["deep_links"] = tao_deep_links_co_so(
            c["ten"],
            ngay_di=ngay_di,
            so_ngay=so_ngay,
            nguoi_lon=nguoi_lon,
            tre_em=tre_em,
            anh_trang=anh_trang_theo_ten.get(c["ten"]),
        )
        c["mau_hoi_phong"] = tao_mau_hoi_phong(
            c["ten"],
            dia_chi=c.get("dia_chi"),
            ngay_di=ngay_di,
            so_ngay=so_ngay,
            nguoi_lon=nguoi_lon,
            tre_em=tre_em,
            lon_tuoi=lon_tuoi,
        )
    return o


def nap_bang_luu_tru(path: str | Path, cum_diem) -> dict:
    """Lúc khởi động (cờ `luu_tru_lich`): mọi cụm của bảng điểm có khu; khu ∈ 3 khu đã biết; cơ sở đủ tên + hạng đã biết + nguồn.
    Sai ⇒ `ValueError` (server không khởi động). `cum_diem` = các mã cụm của bảng điểm v2."""
    bang = json.loads(Path(path).read_text(encoding="utf-8"))
    thieu = sorted(set(cum_diem) - set(bang["cum_ve_khu"]))
    if thieu:
        raise ValueError(f"bảng lưu trú: cụm của bảng điểm không có khu: {thieu}")
    if not set(bang["cum_ve_khu"].values()) <= set(TEN_KHU):
        raise ValueError("bảng lưu trú: cum_ve_khu có khu lạ")
    for c in bang["co_so"]:
        if not (c.get("ten") and c.get("xep_hang") in MUC_HANG and c.get("nguon") and c.get("khu")):
            raise ValueError(f"bảng lưu trú: cơ sở thiếu tên / hạng / nguồn / khu: {c.get('ten')!r}")
        if c.get("phia_bien") not in (None, "bac", "nam") or (c["khu"] == KHU_BIEN) != (c.get("phia_bien") is not None):
            raise ValueError(f"bảng lưu trú: phia_bien sai (chỉ bac / nam, đúng cho cơ sở ven biển): {c.get('ten')!r}")
        if c.get("anh") and not (c["anh"].startswith(ANH_GOC) and c["anh"].endswith(".jpg")):
            raise ValueError(f"bảng lưu trú: ảnh ngoài {ANH_GOC}: {c.get('ten')!r}")
    return bang


def chon_khu(bang_luu_tru: dict, cum_cac_diem: list[str], han_che: bool) -> tuple[str, str]:
    """(khu, lý do). `cum_cac_diem` = cụm của từng điểm ban ngày (có lặp, theo thứ tự lịch); `han_che` = có trẻ em / người lớn tuổi."""
    # cụm đi trong ngày (Bạch Mã, Nhị Hồ… — `nam_xa`) thuộc khu ven biển trong bảng nhưng không phải lý do ở biển ⇒ không đếm cho khu nào
    khu = [None if c in CUM_DI_TRONG_NGAY else bang_luu_tru["cum_ve_khu"][c] for c in cum_cac_diem]
    dem, n = Counter(khu), len(khu)
    if dem[KHU_BIEN] >= NGUONG_BIEN * n:
        chon = KHU_BIEN
    elif dem[KHU_TAY] > NGUONG_TAY * n:
        if han_che:
            return KHU_LOI, "Khu trung tâm — đi cùng trẻ em hoặc người lớn tuổi nên ở gần dịch vụ, đường đi ngắn."
        chon = KHU_TAY
    else:
        chon = KHU_LOI
    if chon == KHU_LOI and dem[chon] * 2 < n:  # trung tâm được chọn vì điểm rải nhiều hướng — không nêu tỉ lệ thấp như thể khu không hợp
        return chon, "Khu trung tâm — các điểm của lịch rải nhiều hướng, từ đây đi hướng nào cũng gần."
    return chon, f"Cùng khu với {dem[chon]} / {n} điểm tham quan ban ngày của lịch."


def chon_co_so(bang_luu_tru: dict, khu: str, cum_dau: str | None, ngan_sach: str | None = None) -> list[dict]:
    """≤ 5 cơ sở trong khu, trải theo mức hạng (SO_THEO_MUC). Trong một mức lấy lần lượt từng hạng, hạng cao trước (vd 1 × 5 sao + 1 × 4 sao) —
    xếp theo tên trong cả mức từng làm 5 sao không bao giờ hiện (mô phỏng 3.840 khung 14/11: 0 / 6.108). Cùng hạng: gần cụm có nhiều điểm
    nhất trước ⇒ có ảnh trước ⇒ theo tên (tất định). `ngan_sach` ⇒ chỉ mức đó, tối đa 5 (trống ⇒ như không chọn)."""
    if ngan_sach is not None:
        so_muc = tuple(sum(SO_THEO_MUC) if m == MUC_NGAN_SACH[ngan_sach] else 0 for m in range(len(SO_THEO_MUC)))
        return _chon(bang_luu_tru, khu, cum_dau, so_muc) or _chon(bang_luu_tru, khu, cum_dau, SO_THEO_MUC)
    return _chon(bang_luu_tru, khu, cum_dau, SO_THEO_MUC)


def _chon(bang_luu_tru: dict, khu: str, cum_dau: str | None, so_muc: tuple[int, ...]) -> list[dict]:
    out = []
    for muc, so in enumerate(so_muc):
        nhom = {}  # hạng ⇒ cơ sở, theo thứ tự hạng của MUC_HANG (cao trước)
        for hang in (h for h, m in MUC_HANG.items() if m == muc):
            ds = [c for c in bang_luu_tru["co_so"] if c["khu"] == khu and c["xep_hang"] == hang
                  and (khu != KHU_BIEN or c.get("phia_bien") == PHIA_CUM.get(cum_dau))]
            nhom[hang] = sorted(ds, key=lambda c: (c.get("cum_gan") != cum_dau, not c.get("anh"), c["ten"]))
        lay = [c for vong in itertools.zip_longest(*nhom.values()) for c in vong if c]  # vòng 1: đầu mỗi hạng; vòng 2: thứ hai…
        out += lay[:so]
    return [{"ten": c["ten"], "xep_hang": c["xep_hang"], "dia_chi": c.get("dia_chi"), "link": LINK_TIM + quote(f"{c['ten']}, Huế"),
             "map_url": MAP_BASE + quote(", ".join(x for x in (c["ten"], c.get("dia_chi"), "Huế") if x)),
             "anh": c.get("anh"), "nguon": c["nguon"]} for c in out]  # `anh` chỉ có khi ảnh chắc (ảnh kc không vào bảng — dễ tưởng là đúng nơi)


def o_dau(bang_luu_tru: dict, cum_cac_diem: list[str], so_ngay: int, han_che: bool, co_toi: bool = False,
          ngan_sach: str | None = None, *, tham_so: dict | None = None, ngay_di: str | None = None,
          xuat_nang_cao: bool = False) -> dict | None:
    """Khối `lich["o_dau"]`; lịch 1 ngày ⇒ None (không có đêm nào). `co_toi`: lịch có hoạt động buổi tối — bộ xếp chỉ đặt buổi tối ở trung tâm, nên
    khách về trung tâm mỗi tối ⇒ ở trung tâm (người xem 14/11: "3 / 5 điểm ngày ở phía tây + mọi tối ở trung tâm" mà gợi ý phía tây là sai)."""
    if so_ngay < 2 or not cum_cac_diem:
        return None
    # "các hoạt động buổi tối", không phải "các buổi tối": lịch có thể có tối trống (ngày đi xa; đoàn có trẻ nhỏ / người lớn tuổi; tối người dùng đã bỏ)
    khu, ly_do = (KHU_LOI, "Khu trung tâm — các hoạt động buổi tối của lịch đều ở trung tâm, về chỗ ở gần.") if co_toi \
        else chon_khu(bang_luu_tru, cum_cac_diem, han_che)
    cum_trong_khu = [c for c in cum_cac_diem if bang_luu_tru["cum_ve_khu"][c] == khu]
    cum_dau = Counter(cum_trong_khu).most_common(1)[0][0] if cum_trong_khu else None
    co_so = chon_co_so(bang_luu_tru, khu, cum_dau, ngan_sach)
    if not co_so:  # (ven biển không có cơ sở cùng phía) ⇒ về khu trung tâm, nói thẳng lý do
        khu, ly_do = KHU_LOI, "Khu trung tâm — ven biển phía này chưa có cơ sở trong danh mục."
        cum_dau = None
        co_so = chon_co_so(bang_luu_tru, khu, None, ngan_sach)
    if not co_so:
        return None
    kq = {"khu": khu, "ten_khu": TEN_KHU[khu], "ly_do": ly_do,
          "co_so": [{k: c[k] for k in ("ten", "xep_hang", "dia_chi", "link", "map_url", "anh")} for c in co_so],
          "nhan": NHAN, "nguon": " · ".join(dict.fromkeys(c["nguon"] for c in co_so))}
    if xuat_nang_cao or tham_so is not None or ngay_di is not None:
        ts = dict(tham_so or {})
        ts.setdefault("so_ngay", so_ngay)
        if ngay_di is not None:
            ts.setdefault("ngay_di", ngay_di)
        gan_xuat_nang_cao_o_dau(kq, ts, bang_luu_tru=bang_luu_tru)
    return kq


def dong_chu(o: dict) -> list[str]:
    """Khối chữ thuần cho `ghep_chu` (nút chép / tải, lịch sử chat)."""
    return ["", f"**Nơi ở gợi ý: khu {o['ten_khu']}** — {o['ly_do']}",
            *(f"- {c['ten']} ({c['xep_hang']})" + (f", {c['dia_chi']}" if c.get("dia_chi") else "") for c in o["co_so"]),
            f"{o['nhan']} Nguồn: {o['nguon']}."]


# Trang "Chỗ ở" (plan `2026-11-15-khach-san-trang-va-ngan-sach.md` §1, sha b5d8bc184090): mọi cơ sở của bảng theo khu ⇒ mức hạng; chỉ mở từ ô "Nơi ở".
# Ven biển tách hai phía theo `phia_bien` (bảng v3) — hai phía cách nhau ~40 km. Không giá, không điện thoại, không toạ độ (link Bản đồ do code dựng).
NHOM_TRANG = ((KHU_LOI, None, "Trung tâm, hai bờ sông Hương"), (KHU_TAY, None, "Phía tây yên tĩnh (Kim Long, Thủy Xuân)"),
              (KHU_BIEN, "bac", "Ven biển phía bắc (Thuận An, Phú Vang)"), (KHU_BIEN, "nam", "Phía nam (Phú Lộc – Lăng Cô)"))
TEN_MUC = ("4–5 sao", "2–3 sao", "1 sao, đạt chuẩn")
HANG = list(MUC_HANG)


def trang_cho_o(bang_luu_tru: dict, *, xuat_nang_cao: bool = False) -> dict:
    """`{nhom: [{khu, ten, muc: [{ten, co_so: [...]}]}], nhan, nguon}`. Trong mức: có ảnh trước ⇒ hạng cao ⇒ tên (review E: ảnh trước như lịch)."""
    nhom = []
    for khu, phia, ten in NHOM_TRANG:
        ds = [c for c in bang_luu_tru["co_so"] if c["khu"] == khu and c.get("phia_bien") == phia]
        muc_items = []
        for m in range(3):
            ds_m = []
            for c in sorted((c for c in ds if MUC_HANG[c["xep_hang"]] == m), key=lambda c: (not c.get("anh"), HANG.index(c["xep_hang"]), c["ten"])):
                item = {
                    "ten": c["ten"], "xep_hang": c["xep_hang"], "dia_chi": c.get("dia_chi"), "anh": c.get("anh"),
                    "map_url": MAP_BASE + quote(", ".join(x for x in (c["ten"], c.get("dia_chi"), "Huế") if x)),
                    "link": LINK_TIM + quote(f"{c['ten']}, Huế"),
                }
                if xuat_nang_cao:
                    item["deep_links"] = tao_deep_links_co_so(c["ten"], anh_trang=c.get("anh_trang"))
                    item["mau_hoi_phong"] = tao_mau_hoi_phong(c["ten"], dia_chi=c.get("dia_chi"))
                ds_m.append(item)
            muc_items.append({"ten": TEN_MUC[m], "co_so": ds_m})
        nhom.append({"khu": f"{khu}:{phia}" if phia else khu, "ten": ten, "muc": [x for x in muc_items if x["co_so"]]})
    return {"nhom": nhom, "nhan": NHAN, "nguon": " · ".join(dict.fromkeys(c["nguon"] for c in bang_luu_tru["co_so"]))}
