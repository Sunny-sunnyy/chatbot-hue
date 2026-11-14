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
    return ltl.o_dau(BANG_LT, [BANG_V2.theo_id[j]["cum"] for j in v2.diem_ban_ngay(khung)], len(khung["ngay"]), bool(ts["tre_em"] or ts["lon_tuoi"]))


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
        mong = ltl.KHU_BIEN if dem[ltl.KHU_BIEN] >= 0.6 * n else ltl.KHU_TAY if dem[ltl.KHU_TAY] > 0.5 * n and not han_che else ltl.KHU_LOI
        assert o["khu"] == mong or (mong == ltl.KHU_BIEN and o["ly_do"].startswith("Khu trung tâm — ven biển")), key
        if o["khu"] == ltl.KHU_BIEN:  # cơ sở cùng phía với cụm ven biển nhiều điểm nhất (không gợi ý Lăng Cô cho lịch Thuận An)
            cum = Counter(c for c in (BANG_V2.theo_id[j]["cum"] for j in v2.diem_ban_ngay(khung)) if c in ltl.PHIA_BIEN).most_common(1)[0][0]
            assert all(any(t in (c["dia_chi"] or "") for t in ltl.PHIA_BIEN[cum]) for c in o["co_so"]), key
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
            [{"ten": f"{k}-{h}-{i}", "xep_hang": h, "khu": k, "nguon": "danh mục thử", "cum_gan": None}
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


def test_rule_spread_by_rank_and_near_cluster_first():
    co_so = [{"ten": t, "xep_hang": h, "khu": ltl.KHU_LOI, "nguon": "n", "cum_gan": g} for t, h, g in
             [("B5", "5 sao", None), ("A4", "4 sao", None), ("C5", "5 sao", "bo_nam"), ("D3", "3 sao", None), ("E2", "2 sao", None),
              ("F2", "2 sao", None), ("G1", "1 sao", None), ("H", "Đạt chuẩn phục vụ khách du lịch", "bo_nam")]]
    ten = [c["ten"] for c in ltl.chon_co_so(_bang(co_so=co_so), ltl.KHU_LOI, "bo_nam")]
    assert ten == ["C5", "A4", "D3", "E2", "H"]


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
