"""Gợi ý nơi ở trong lịch bản 2 (plan `docs/superpowers/plans/2026-11-14-luu-tru-trong-lich-plan.md`, cờ `luu_tru_lich`).

Mọi thứ do code: chọn MỘT khu cho cả chuyến theo cụm của các điểm ban ngày, chọn ≤ 5 cơ sở trải theo hạng trong khu đó, viết lý do,
dựng link tìm phòng. Model không chọn, không viết tên cơ sở; khối này không vào tin nhắn gửi model. Không giá, không "còn phòng".
Bảng: `bang_luu_tru_lich_v2.json` = bảng E (danh mục công khai, có nguồn + ngày; khu theo `cum_ve_khu` của C) + toạ độ Places + ảnh đã duyệt (B 14/11).
"""
import itertools
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote

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
# Khu ven biển gộp hai phía cách nhau ~40 km (Thuận An / Tam Giang ↔ Lăng Cô); bảng không có cụm gần cho phần lớn cơ sở ven biển ⇒ tách theo
# chữ trong địa chỉ, chỉ gợi ý cơ sở cùng phía với cụm có nhiều điểm nhất (địa chỉ không khớp phía nào ⇒ không gợi ý — không đoán).
CUM_DI_TRONG_NGAY = {"nam_xa"}
PHIA_BIEN = {"dong_bien": ("Phú Vang", "Thuận An"), "nam_xa": ("Phú Lộc", "Lăng Cô")}
LINK_TIM = "https://www.booking.com/searchresults.html?ss="  # link tìm (không đặt chỗ), chỉ mở khi người dùng bấm
ANH_GOC = "/anh/khach_san/"  # ảnh tự host (1 agent con chọn + B nhìn lại 14/11); bảng ghi đường khác gốc này ⇒ không khởi động
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
                  and (khu != KHU_BIEN or any(t in (c.get("dia_chi") or "") for t in PHIA_BIEN.get(cum_dau, ())))]
            nhom[hang] = sorted(ds, key=lambda c: (c.get("cum_gan") != cum_dau, not c.get("anh"), c["ten"]))
        lay = [c for vong in itertools.zip_longest(*nhom.values()) for c in vong if c]  # vòng 1: đầu mỗi hạng; vòng 2: thứ hai…
        out += lay[:so]
    return [{"ten": c["ten"], "xep_hang": c["xep_hang"], "dia_chi": c.get("dia_chi"), "link": LINK_TIM + quote(f"{c['ten']}, Huế"),
             "map_url": MAP_BASE + quote(", ".join(x for x in (c["ten"], c.get("dia_chi"), "Huế") if x)),
             "anh": c.get("anh"), "nguon": c["nguon"]} for c in out]  # `anh` chỉ có khi ảnh chắc (ảnh kc không vào bảng — dễ tưởng là đúng nơi)


def o_dau(bang_luu_tru: dict, cum_cac_diem: list[str], so_ngay: int, han_che: bool, co_toi: bool = False,
          ngan_sach: str | None = None) -> dict | None:
    """Khối `lich["o_dau"]`; lịch 1 ngày ⇒ None (không có đêm nào). `co_toi`: lịch có hoạt động buổi tối — bộ xếp chỉ đặt buổi tối ở trung tâm, nên
    khách về trung tâm mỗi tối ⇒ ở trung tâm (người xem 14/11: "3 / 5 điểm ngày ở phía tây + mọi tối ở trung tâm" mà gợi ý phía tây là sai)."""
    if so_ngay < 2 or not cum_cac_diem:
        return None
    khu, ly_do = (KHU_LOI, "Khu trung tâm — các buổi tối của lịch đều ở trung tâm, về chỗ ở gần.") if co_toi \
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
    return {"khu": khu, "ten_khu": TEN_KHU[khu], "ly_do": ly_do,
            "co_so": [{k: c[k] for k in ("ten", "xep_hang", "dia_chi", "link", "map_url", "anh")} for c in co_so],
            "nhan": NHAN, "nguon": " · ".join(dict.fromkeys(c["nguon"] for c in co_so))}


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


def trang_cho_o(bang_luu_tru: dict) -> dict:
    """`{nhom: [{khu, ten, muc: [{ten, co_so: [...]}]}], nhan, nguon}`. Trong mức: có ảnh trước ⇒ hạng cao ⇒ tên (review E: ảnh trước như lịch)."""
    nhom = []
    for khu, phia, ten in NHOM_TRANG:
        ds = [c for c in bang_luu_tru["co_so"] if c["khu"] == khu and c.get("phia_bien") == phia]
        muc = [{"ten": TEN_MUC[m], "co_so": [
            {"ten": c["ten"], "xep_hang": c["xep_hang"], "dia_chi": c.get("dia_chi"), "anh": c.get("anh"),
             "map_url": MAP_BASE + quote(", ".join(x for x in (c["ten"], c.get("dia_chi"), "Huế") if x)), "link": LINK_TIM + quote(f"{c['ten']}, Huế")}
            for c in sorted((c for c in ds if MUC_HANG[c["xep_hang"]] == m), key=lambda c: (not c.get("anh"), HANG.index(c["xep_hang"]), c["ten"]))]}
            for m in range(3)]
        nhom.append({"khu": f"{khu}:{phia}" if phia else khu, "ten": ten, "muc": [x for x in muc if x["co_so"]]})
    return {"nhom": nhom, "nhan": NHAN, "nguon": " · ".join(dict.fromkeys(c["nguon"] for c in bang_luu_tru["co_so"]))}
