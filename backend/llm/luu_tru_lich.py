"""Gợi ý nơi ở trong lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-luu-tru-trong-lich-plan.md`, cờ `luu_tru_lich`).

Mọi thứ do code: chọn MỘT khu cho cả chuyến theo cụm của các điểm ban ngày, chọn ≤ 5 cơ sở trải theo hạng trong khu đó, viết lý do,
dựng link tìm phòng. Model không chọn, không viết tên cơ sở; khối này không vào tin nhắn gửi model. Không giá, không "còn phòng".
Bảng: `bang_luu_tru_lich.json` của E (danh mục công khai, có nguồn + ngày; khu theo `cum_ve_khu` của C).
"""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote

KHU_LOI = "loi_do_thi_hai_bo_song_huong"
KHU_TAY = "phia_tay_yen_tinh"
KHU_BIEN = "ven_bien_dam_pha_lang_co"
TEN_KHU = {KHU_LOI: "trung tâm, hai bờ sông Hương", KHU_TAY: "phía tây yên tĩnh (Kim Long, Thủy Xuân)", KHU_BIEN: "ven biển, đầm phá"}
NGUONG_TAY = 0.5   # phía tây chỉ khi > 50 % điểm ban ngày ở phía tây VÀ không có trẻ em / người lớn tuổi
NGUONG_BIEN = 0.6  # ven biển chỉ khi ≥ 60 % điểm ban ngày ở ven biển (ngày ra biển thường là đi trong ngày)
# Trải theo hạng để khách tự chọn: tối đa 2 cơ sở 4–5 sao · 2 cơ sở 2–3 sao · 1 cơ sở 1 sao / đạt chuẩn
MUC_HANG = {"5 sao": 0, "4 sao": 0, "3 sao": 1, "2 sao": 1, "1 sao": 2, "Đạt chuẩn phục vụ khách du lịch": 2}
SO_THEO_MUC = (2, 2, 1)
# Khu ven biển gộp hai phía cách nhau ~40 km (Thuận An / Tam Giang ↔ Lăng Cô); bảng không có cụm gần cho phần lớn cơ sở ven biển ⇒ tách theo
# chữ trong địa chỉ, chỉ gợi ý cơ sở cùng phía với cụm có nhiều điểm nhất (địa chỉ không khớp phía nào ⇒ không gợi ý — không đoán).
CUM_DI_TRONG_NGAY = {"nam_xa"}
PHIA_BIEN = {"dong_bien": ("Phú Vang", "Thuận An"), "nam_xa": ("Phú Lộc", "Lăng Cô")}
LINK_TIM = "https://www.booking.com/searchresults.html?ss="  # link tìm (không đặt chỗ), chỉ mở khi người dùng bấm
NHAN = "Gợi ý theo vị trí và hạng — chưa kiểm giá, phòng trống."


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


def chon_co_so(bang_luu_tru: dict, khu: str, cum_dau: str | None) -> list[dict]:
    """≤ 5 cơ sở trong khu, trải theo mức hạng (SO_THEO_MUC); trong một mức: gần cụm có nhiều điểm nhất trước, rồi theo tên (tất định)."""
    out = []
    for muc, so in enumerate(SO_THEO_MUC):
        ds = [c for c in bang_luu_tru["co_so"] if c["khu"] == khu and MUC_HANG[c["xep_hang"]] == muc
              and (khu != KHU_BIEN or any(t in (c.get("dia_chi") or "") for t in PHIA_BIEN.get(cum_dau, ())))]
        ds.sort(key=lambda c: (c.get("cum_gan") != cum_dau, c["ten"]))
        out += ds[:so]
    return [{"ten": c["ten"], "xep_hang": c["xep_hang"], "dia_chi": c.get("dia_chi"), "link": LINK_TIM + quote(f"{c['ten']}, Huế"),
             "nguon": c["nguon"]} for c in out]


def o_dau(bang_luu_tru: dict, cum_cac_diem: list[str], so_ngay: int, han_che: bool) -> dict | None:
    """Khối `lich["o_dau"]`; lịch 1 ngày ⇒ None (không có đêm nào)."""
    if so_ngay < 2 or not cum_cac_diem:
        return None
    khu, ly_do = chon_khu(bang_luu_tru, cum_cac_diem, han_che)
    cum_trong_khu = [c for c in cum_cac_diem if bang_luu_tru["cum_ve_khu"][c] == khu]
    cum_dau = Counter(cum_trong_khu).most_common(1)[0][0] if cum_trong_khu else None
    co_so = chon_co_so(bang_luu_tru, khu, cum_dau)
    if not co_so:  # (ven biển không có cơ sở cùng phía) ⇒ về khu trung tâm, nói thẳng lý do
        khu, ly_do = KHU_LOI, "Khu trung tâm — ven biển phía này chưa có cơ sở trong danh mục."
        cum_dau = None
        co_so = chon_co_so(bang_luu_tru, khu, None)
    if not co_so:
        return None
    return {"khu": khu, "ten_khu": TEN_KHU[khu], "ly_do": ly_do,
            "co_so": [{k: c[k] for k in ("ten", "xep_hang", "dia_chi", "link")} for c in co_so],
            "nhan": NHAN, "nguon": " · ".join(dict.fromkeys(c["nguon"] for c in co_so))}


def dong_chu(o: dict) -> list[str]:
    """Khối chữ thuần cho `ghep_chu` (nút chép / tải, lịch sử chat)."""
    return ["", f"**Nơi ở gợi ý: khu {o['ten_khu']}** — {o['ly_do']}",
            *(f"- {c['ten']} ({c['xep_hang']})" + (f", {c['dia_chi']}" if c.get("dia_chi") else "") for c in o["co_so"]),
            f"{o['nhan']} Nguồn: {o['nguon']}."]
