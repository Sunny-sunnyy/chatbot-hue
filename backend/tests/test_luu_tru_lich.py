"""Gợi ý nơi ở trong lịch bản 2 (plan `2026-11-14-luu-tru-trong-lich-plan.md`, cờ `luu_tru_lich`) — logic thuần, 0 USD.
Tiêu chí "Luôn" trên 3.840 khung thật (bảng điểm v8 + bảng lưu trú của E) + luật chọn khu trên dữ liệu nhỏ tự đặt + nạp bảng / cờ +
Q1: khối `o_dau` không vào tin nhắn gửi model; cờ tắt ⇒ chữ `ghep_chu` như bản trước."""
import copy
import itertools
import json
from collections import Counter
from pathlib import Path

import pytest

from llm import lich_trinh_v2 as v2
from llm import luu_tru_lich as ltl
from test_cong_dot_1 import SETTINGS, flags_from

BACKEND = Path(__file__).resolve().parents[1]
BANG_V2 = v2.nap_bang_v2(BACKEND / SETTINGS["assistant"]["lich_trinh_bang_v2"])
BANG_LT = ltl.nap_bang_luu_tru(BACKEND / SETTINGS["assistant"]["lich_trinh_bang_luu_tru"], BANG_V2.cum)
ST_16 = [()] + [(s,) for s in v2.LOAI_DIEM_THU_TU] + list(itertools.combinations(v2.LOAI_DIEM_THU_TU, 2))
KIEU = ("nhe_nhang", "can_bang", "kham_pha")
NGAY = (None, v2.dt.date(2027, 4, 7), v2.dt.date(2026, 11, 21), v2.dt.date(2026, 11, 13))  # như mô phỏng 3.840 của bản 2


def _o_dau(khung):
    ts = khung["tham_so"]
    co_toi = (lambda toi: bool(toi) and all(BANG_LT["cum_ve_khu"][BANG_V2.theo_id[j]["cum"]] == ltl.KHU_LOI for j in toi))(
        [j for ng in khung["ngay"] for j in ng["buoi"]["toi"] if j in BANG_V2.theo_id])
    return ltl.o_dau(BANG_LT, [BANG_V2.theo_id[j]["cum"] for j in v2.diem_ban_ngay(khung)], len(khung["ngay"]),
                     bool(ts["tre_em"] or ts["lon_tuoi"]), co_toi)


@pytest.fixture(scope="module")
def mo_phong():
    kq = {}
    for key in itertools.product(range(1, 6), (0, 1), (False, True), KIEU, ST_16, NGAY):
        kq[key] = v2.xep_v2(BANG_V2, v2.ThamSoV2(*key[:4], so_thich=key[4]), ngay_bat_dau=key[5])
    assert len(kq) == 3840
    return kq


def test_simulation_always_rules(mo_phong):
    theo_ten = {c["ten"]: c for c in BANG_LT["co_so"]}
    khu_dem = Counter()
    for key, khung in mo_phong.items():
        o = _o_dau(khung)
        if key[0] == 1:
            assert o is None, key
            continue
        assert o is not None, key
        khu_dem[o["khu"]] += 1
        # khu đúng luật (1): đếm lại độc lập theo cụm
        khu = [None if BANG_V2.theo_id[j]["cum"] in ltl.CUM_DI_TRONG_NGAY else BANG_LT["cum_ve_khu"][BANG_V2.theo_id[j]["cum"]]
               for j in v2.diem_ban_ngay(khung)]
        n, dem, han_che = len(khu), Counter(khu), bool(key[1] or key[2])
        co_toi = (lambda toi: bool(toi) and all(BANG_LT["cum_ve_khu"][BANG_V2.theo_id[j]["cum"]] == ltl.KHU_LOI for j in toi))(
        [j for ng in khung["ngay"] for j in ng["buoi"]["toi"] if j in BANG_V2.theo_id])
        mong = ltl.KHU_LOI if co_toi else ltl.KHU_BIEN if dem[ltl.KHU_BIEN] >= 0.6 * n else ltl.KHU_TAY if dem[ltl.KHU_TAY] > 0.5 * n and not han_che \
            else ltl.KHU_LOI
        assert o["khu"] == mong or (mong == ltl.KHU_BIEN and o["ly_do"].startswith("Khu trung tâm — ven biển")), key
        if o["khu"] == ltl.KHU_BIEN:  # cơ sở cùng phía với cụm ven biển nhiều điểm nhất (không gợi ý Lăng Cô cho lịch Thuận An)
            phia = {"dong_bien": "bac", "nam_xa": "nam"}  # viết lại độc lập với `ltl.PHIA_CUM`
            cum = Counter(c for c in (BANG_V2.theo_id[j]["cum"] for j in v2.diem_ban_ngay(khung)) if c in phia).most_common(1)[0][0]
            assert all(theo_ten[c["ten"]]["phia_bien"] == phia[cum] for c in o["co_so"]), key
        assert 1 <= len(o["co_so"]) <= 5 and o["nhan"].startswith("Gợi ý theo vị trí và hạng — chưa kiểm giá")
        for c in o["co_so"]:
            assert c["ten"] in theo_ten and theo_ten[c["ten"]]["khu"] == o["khu"] and c["xep_hang"] == theo_ten[c["ten"]]["xep_hang"]
            assert c["link"].startswith(ltl.LINK_TIM) and "\n" not in c["link"]
        assert len({c["ten"] for c in o["co_so"]}) == len(o["co_so"])
        assert " 0 / " not in o["ly_do"]
        if o["ly_do"].startswith("Cùng khu với"):  # tỉ lệ chỉ nêu khi ≥ một nửa (người xem 14/11: "2 / 9" nghe như khu không hợp)
            a_, b_ = (int(x) for x in o["ly_do"].split("với ")[1].split(" điểm")[0].split(" / "))
            assert a_ * 2 >= b_, (key, o["ly_do"])
    print("khu theo lịch >= 2 ngày:", dict(khu_dem))


def _bang(cum_ve_khu=None, co_so=None):
    return {"cum_ve_khu": cum_ve_khu or {"kinh_thanh": ltl.KHU_LOI, "kim_long": ltl.KHU_TAY, "dong_bien": ltl.KHU_BIEN},
            "co_so": co_so if co_so is not None else
            [{"ten": f"{k}-{h}-{i}", "xep_hang": h, "khu": k, "nguon": "danh mục thử", "cum_gan": None, **({"phia_bien": "bac"} if k == ltl.KHU_BIEN else {})}
             for k in (ltl.KHU_LOI, ltl.KHU_TAY, ltl.KHU_BIEN) for h in ("5 sao", "3 sao", "1 sao") for i in range(3)]}


def test_rule_zone_choice():
    b = _bang()
    assert ltl.chon_khu(b, ["kim_long"] * 3 + ["kinh_thanh"] * 2, False)[0] == ltl.KHU_TAY
    assert ltl.chon_khu(b, ["kim_long"] * 3 + ["kinh_thanh"] * 2, True) == (ltl.KHU_LOI, ltl.chon_khu(b, ["kim_long"] * 3, True)[1])
    assert "trẻ em" in ltl.chon_khu(b, ["kim_long"] * 3, True)[1]
    assert ltl.chon_khu(b, ["kim_long"] * 2 + ["kinh_thanh"] * 2, False)[0] == ltl.KHU_LOI  # đúng 50 % ⇒ không sang phía tây
    assert ltl.chon_khu(b, ["dong_bien"] * 3 + ["kinh_thanh"] * 2, True)[0] == ltl.KHU_BIEN  # 60 % ven biển
    assert ltl.chon_khu(b, ["dong_bien"] * 2 + ["kinh_thanh"] * 2, False) == (ltl.KHU_LOI, "Cùng khu với 2 / 4 điểm tham quan ban ngày của lịch.")
    assert ltl.chon_khu(b, ["dong_bien"] * 1 + ["kim_long"] * 1, False)[1].startswith("Khu trung tâm — các điểm của lịch rải")
    b["cum_ve_khu"]["nam_xa"] = ltl.KHU_BIEN  # Bạch Mã / Nhị Hồ: đi trong ngày, không kéo khu ở ra biển
    assert ltl.chon_khu(b, ["dong_bien"] * 2 + ["nam_xa"] * 2 + ["kinh_thanh"] * 2, False)[0] == ltl.KHU_LOI


def test_evening_activity_means_central_stay():
    """Người xem 14/11 (bản 3): lịch có buổi tối (luôn ở trung tâm) mà gợi ý phía tây ⇒ khách đi về mỗi tối ⇒ có buổi tối thì ở trung tâm."""
    b = _bang()
    cum = ["kim_long", "kim_long", "kim_long", "kinh_thanh"]
    assert ltl.o_dau(b, cum, 2, False)["khu"] == ltl.KHU_TAY
    o = ltl.o_dau(b, cum, 2, False, co_toi=True)
    assert o["khu"] == ltl.KHU_LOI and "buổi tối" in o["ly_do"]
    assert "buổi tối" not in ltl.o_dau(b, ["dong_bien"] * 3, 2, False)["ly_do"]  # không có buổi tối ⇒ lý do không nhắc buổi tối


def test_rule_spread_by_rank_and_near_cluster_first():
    co_so = [{"ten": t, "xep_hang": h, "khu": ltl.KHU_LOI, "nguon": "n", "cum_gan": g} for t, h, g in
             [("B5", "5 sao", None), ("A4", "4 sao", None), ("C5", "5 sao", "bo_nam"), ("D3", "3 sao", None), ("E2", "2 sao", None),
              ("F2", "2 sao", None), ("G1", "1 sao", None), ("H", "Đạt chuẩn phục vụ khách du lịch", "bo_nam")]]
    ten = [c["ten"] for c in ltl.chon_co_so(_bang(co_so=co_so), ltl.KHU_LOI, "bo_nam")]
    assert ten == ["C5", "A4", "D3", "E2", "G1"]  # mỗi mức: lần lượt từng hạng, hạng cao trước; cùng hạng: gần cụm trước
    # lỗi 14/11: xếp theo tên trong cả mức ⇒ hai 4 sao tên "A…" đẩy mọi 5 sao ra ngoài; cùng hạng + cùng cụm: có ảnh trước
    co_so = [{"ten": t, "xep_hang": h, "khu": ltl.KHU_LOI, "nguon": "n", "cum_gan": None, **({"anh": "x.jpg"} if a else {})}
             for t, h, a in [("A4", "4 sao", False), ("A4b", "4 sao", False), ("Z5", "5 sao", False), ("Y5", "5 sao", True)]]
    assert [c["ten"] for c in ltl.chon_co_so(_bang(co_so=co_so), ltl.KHU_LOI, None)] == ["Y5", "A4"]


def test_table_load_checks(tmp_path):
    p = tmp_path / "lt.json"
    p.write_text(json.dumps(_bang()), encoding="utf-8")
    with pytest.raises(ValueError, match="không có khu"):
        ltl.nap_bang_luu_tru(p, ["kinh_thanh", "an_cuu"])
    hong = _bang()
    hong["co_so"][0]["xep_hang"] = "6 sao"
    p.write_text(json.dumps(hong), encoding="utf-8")
    with pytest.raises(ValueError, match="thiếu tên / hạng"):
        ltl.nap_bang_luu_tru(p, ["kinh_thanh"])


def test_flag_needs_v2_and_table():
    with pytest.raises(ValueError, match="luu_tru_lich needs"):
        flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=False, anh_lich=False, luu_tru_lich=True)
    on = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, anh_lich=False, luu_tru_lich=True)
    assert on.luu_tru_bang is not None and len(on.luu_tru_bang["co_so"]) == len(BANG_LT["co_so"])
    assert flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, anh_lich=False, luu_tru_lich=False).luu_tru_bang is None


def test_q1_lodging_not_in_model_message_and_off_text_unchanged(mo_phong):
    khung = mo_phong[(3, 0, False, "can_bang", (), None)]
    lich = v2.dung_lich(BANG_V2, khung, {j: i for i, j in enumerate(v2.diem_v2(khung), start=1)})
    co = copy.deepcopy(lich)
    co["o_dau"] = _o_dau(khung)
    assert co["o_dau"] is not None
    assert v2.tin_nhan_model(co, "TL") == v2.tin_nhan_model(lich, "TL")
    cau = {m["id_muc"]: "Câu." for m in v2.moi_muc(lich)}
    tat, bat = v2.ghep_chu(lich, cau), v2.ghep_chu(co, cau)
    assert bat.startswith(tat) and "Nơi ở gợi ý" in bat[len(tat):] and "Nơi ở" not in tat


def test_evening_outside_center_falls_back_to_day_rule(mo_phong):
    """Review E m-1: luật "có buổi tối ⇒ trung tâm" chỉ áp khi MỌI điểm tối thuộc khu trung tâm (code kiểm bằng bảng khu, không giả định)."""
    from llm import len_ke_hoach as lkh
    flags = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, anh_lich=False, luu_tru_lich=True)
    khung = copy.deepcopy(next(k for key, k in mo_phong.items() if key[0] >= 2 and any(ng["buoi"]["toi"] for ng in k["ngay"])))
    lich = {}
    lkh.gan_o_an(lich, BANG_V2, khung, flags)
    assert "buổi tối" in lich["o_dau"]["ly_do"]  # mọi điểm tối ở trung tâm ⇒ luật buổi tối
    tay = next(j for j, d in BANG_V2.theo_id.items() if BANG_LT["cum_ve_khu"][d["cum"]] != ltl.KHU_LOI)  # dữ liệu giả: một điểm tối ngoài trung tâm
    next(ng for ng in khung["ngay"] if ng["buoi"]["toi"])["buoi"]["toi"][0] = tay
    lich = {}
    lkh.gan_o_an(lich, BANG_V2, khung, flags)
    assert "buổi tối" not in lich["o_dau"]["ly_do"]  # ⇒ về luật cũ theo điểm ngày


def test_every_lodging_photo_path_has_a_file():
    """14/11 (C review m-1): bảng `data/` sửa trước merge ⇒ main trỏ ảnh chưa có file. Mọi `anh` của bảng đang cấu hình phải có file dưới
    `frontend/public` (bảng và ảnh vào cùng lượt merge)."""
    public = BACKEND.parent / "frontend" / "public"
    thieu = [c["ten"] for c in BANG_LT["co_so"] if c.get("anh") and not (public / c["anh"].lstrip("/")).is_file()]
    assert not thieu, thieu


# ---------- ngân sách chỗ ở (plan `2026-11-15-khach-san-trang-va-ngan-sach.md` bản 2 §2, T1–T4, T7) ----------

def test_budget_off_same_khung_and_on_only_that_tier(mo_phong):
    """T1: không chọn ⇒ khung không có khoá mới (trạng thái lưu / ô Nơi ở như cũ). T2: chọn mức ⇒ mọi cơ sở đúng mức, ≤ 5, cùng khu như không chọn."""
    for key, khung in mo_phong.items():
        assert "ngan_sach" not in khung["tham_so"], key
        goc = _o_dau(khung)
        if goc is None:
            continue
        cum = [BANG_V2.theo_id[j]["cum"] for j in v2.diem_ban_ngay(khung)]
        han_che = bool(key[1] or key[2])
        co_toi = (lambda toi: bool(toi) and all(BANG_LT["cum_ve_khu"][BANG_V2.theo_id[j]["cum"]] == ltl.KHU_LOI for j in toi))(
            [j for ng in khung["ngay"] for j in ng["buoi"]["toi"] if j in BANG_V2.theo_id])
        for ns, muc in ltl.MUC_NGAN_SACH.items():
            o = ltl.o_dau(BANG_LT, cum, len(khung["ngay"]), han_che, co_toi, ns)
            assert o["khu"] == goc["khu"] and 1 <= len(o["co_so"]) <= 5, (key, ns)
            assert all(ltl.MUC_HANG[c["xep_hang"]] == muc for c in o["co_so"]), (key, ns)  # bảng hiện tại: 0 khu trống mức


def test_budget_empty_tier_falls_back_silently():
    co_so = [{"ten": t, "xep_hang": h, "khu": ltl.KHU_LOI, "nguon": "n"} for t, h in [("A5", "5 sao"), ("B3", "3 sao")]]
    b = _bang(co_so=co_so)
    assert [c["ten"] for c in ltl.chon_co_so(b, ltl.KHU_LOI, None, "binh_dan")] == [c["ten"] for c in ltl.chon_co_so(b, ltl.KHU_LOI, None)]
    assert [c["ten"] for c in ltl.chon_co_so(b, ltl.KHU_LOI, None, "cao")] == ["A5"]


def test_budget_kept_through_text_edit_and_not_in_model_messages():
    """T4: sửa lịch bằng lời xếp lại qua `sua_lich_v2._xep` ⇒ mức còn trong khung ⇒ `gan_o_an` chỉ ra mức đó. T3: chuỗi gửi model như không chọn."""
    from llm import hoi_lai
    from llm import sua_lich_v2 as sl
    from llm.len_ke_hoach import gan_o_an
    flags = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, anh_lich=False, luu_tru_lich=True)
    truong = {"so_ngay": "3", "nguoi_lon": 2, "kieu_di": "can_bang", "so_thich": ["di_tich"]}
    k0 = v2.xep_v2(BANG_V2, v2.tu_truong(truong))
    k = v2.xep_v2(BANG_V2, v2.tu_truong({**truong, "ngan_sach": "cao"}))
    assert k["tham_so"].pop("ngan_sach") == "cao" and k == k0  # ngân sách không vào bộ xếp
    k["tham_so"]["ngan_sach"] = "cao"
    kq = sl.ap(BANG_V2, sl.luu_tu_lich(k, None, None), [sl.HanhDong(loai="doi_so_ngay", so_ngay=2)])
    assert len(kq["khung"]["ngay"]) == 2 and kq["khung"]["tham_so"]["ngan_sach"] == "cao"
    lich = v2.dung_lich(BANG_V2, kq["khung"], {j: i for i, j in enumerate(v2.diem_v2(kq["khung"]), start=1)})
    gan_o_an(lich, BANG_V2, kq["khung"], flags)
    assert lich["o_dau"]["co_so"] and all(c["xep_hang"] in ("4 sao", "5 sao") for c in lich["o_dau"]["co_so"])
    # T3: tin nhắn viết câu, tin nhắn hiểu ý sửa, câu người dùng vào lịch sử — giống byte có / không ngân sách
    l0 = v2.dung_lich(BANG_V2, k0, {j: i for i, j in enumerate(v2.diem_v2(k0), start=1)})
    l1 = v2.dung_lich(BANG_V2, k, {j: i for i, j in enumerate(v2.diem_v2(k), start=1)})
    assert v2.tin_nhan_model(l1, "TL") == v2.tin_nhan_model(l0, "TL") and l1["minh_hieu"] == l0["minh_hieu"]
    assert sl.tin_nhan_hieu(BANG_V2, sl.luu_tu_lich(k, None, None), "bỏ một điểm") == sl.tin_nhan_hieu(BANG_V2, sl.luu_tu_lich(k0, None, None), "bỏ một điểm")
    assert hoi_lai.ghep_cau_v2("Lên kế hoạch", {**truong, "ngan_sach": "cao"}) == hoi_lai.ghep_cau_v2("Lên kế hoạch", truong)


def test_budget_value_from_browser_is_checked():
    """T7: chỉ đúng ba giá trị; lạ ⇒ lỗi khuôn (route trả 422)."""
    from pydantic import ValidationError
    from llm.hoi_lai import TruongInput, co_gia_tri_moi
    assert co_gia_tri_moi(TruongInput(so_ngay="2", ngan_sach="vua"))  # giá trị mới ⇒ chỉ nhận ở lượt biểu mẫu bản 2
    with pytest.raises(ValidationError):
        TruongInput(so_ngay="2", ngan_sach="re")


def test_lodging_page_lists_every_listing_once_with_safe_fields():
    """Trang "Chỗ ở" (plan 2026-11-15 §1, T5): mọi cơ sở của bảng đúng một lần, đúng nhóm khu / mức; chỉ các trường đã duyệt (không giá, điện
    thoại, toạ độ); 0 dòng trùng tên + địa chỉ; ảnh chỉ gốc tự host; link chỉ 2 gốc; trong mức có ảnh trước."""
    t = ltl.trang_cho_o(BANG_LT)
    ds = [(n, m, c) for n in t["nhom"] for m in n["muc"] for c in m["co_so"]]
    assert len(ds) == len(BANG_LT["co_so"]) and len({(c["ten"], c["dia_chi"]) for *_, c in ds}) == len(ds)
    goc = {(c["ten"], c.get("dia_chi")): c for c in BANG_LT["co_so"]}
    for n, m, c in ds:
        assert set(c) == {"ten", "xep_hang", "dia_chi", "anh", "map_url", "link"}
        g = goc[(c["ten"], c["dia_chi"])]
        assert n["khu"].split(":")[0] == g["khu"] and m["ten"] == ltl.TEN_MUC[ltl.MUC_HANG[g["xep_hang"]]]
        assert c["anh"] is None or (c["anh"].startswith(ltl.ANH_GOC) and c["anh"].endswith(".jpg"))
        assert c["map_url"].startswith(ltl.MAP_BASE) and c["link"].startswith(ltl.LINK_TIM)
    for n in t["nhom"]:
        for m in n["muc"]:
            co_anh = [bool(c["anh"]) for c in m["co_so"]]
            assert co_anh == sorted(co_anh, reverse=True)
    assert [n["khu"] for n in t["nhom"]] == [ltl.KHU_LOI, ltl.KHU_TAY, f"{ltl.KHU_BIEN}:bac", f"{ltl.KHU_BIEN}:nam"]


def test_table_load_checks_coast_side(tmp_path):
    p = tmp_path / "lt.json"
    p.write_text(json.dumps(_bang()), encoding="utf-8")
    assert ltl.nap_bang_luu_tru(p, ["kinh_thanh"])  # bảng mẫu (ven biển có phía) nạp được ⇒ các ca dưới hỏng đúng vì phần sửa
    for sua in ({"khu": ltl.KHU_BIEN}, {"phia_bien": "dong"}, {"phia_bien": "bac"}):  # ven biển thiếu phía · phía lạ · phía ở cơ sở không ven biển
        hong = _bang()
        hong["co_so"][0].update(sua)
        p.write_text(json.dumps(hong), encoding="utf-8")
        with pytest.raises(ValueError, match="phia_bien"):
            ltl.nap_bang_luu_tru(p, ["kinh_thanh"])
