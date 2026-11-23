"""Quán ăn gợi ý trong lịch bản 2 (plan `2026-11-14-quan-trong-lich-plan.md`, cờ `quan_lich`) — logic thuần, 0 USD.
Sàn trên 3.840 khung thật (bảng điểm v8 + bảng quán C + toạ độ điểm) + nạp bảng / cờ + Q1: khối `an` không vào tin nhắn gửi model;
cờ tắt ⇒ chữ `ghep_chu` như bản trước."""
import copy
import itertools
import json
from pathlib import Path

import pytest

from llm import lich_trinh as lt
from llm import lich_trinh_v2 as v2
from llm import quan_lich as ql
from test_cong_dot_1 import SETTINGS, flags_from

BACKEND = Path(__file__).resolve().parents[1]
A = SETTINGS["assistant"]
BANG_V2 = v2.nap_bang_v2(BACKEND / A["lich_trinh_bang_v2"])
QUAN = ql.nap_bang_quan(BACKEND / A["lich_trinh_bang_quan"], BANG_V2.cum)
TOA = lt.nap_toa_do(BACKEND / A["lich_trinh_toa_do"], BANG_V2)
ST_16 = [()] + [(s,) for s in v2.LOAI_DIEM_THU_TU] + list(itertools.combinations(v2.LOAI_DIEM_THU_TU, 2))
NGAY = (None, v2.dt.date(2027, 4, 7), v2.dt.date(2026, 11, 21), v2.dt.date(2026, 11, 13))
KEO = {(q["ten"], tuple(q["toa"])): (c, q) for c, ds in QUAN.items() for q in ds}


def _toa_tu_link(url: str) -> tuple:
    return tuple(map(float, url.split("query=")[1].replace("%2C", ",").split(",")))


def test_simulation_floor():
    """Mọi quán có trong bảng, cùng cụm với điểm, ≤ 2 km, không lặp trong chuyến; quán ăn trước cà phê, trong cùng loại quán kho trước; ≤ 2 quán / bữa; bữa có dòng ≥ 75 %."""
    bua = co = 0
    for key in itertools.product(range(1, 6), (0, 1), (False, True), ("nhe_nhang", "can_bang", "kham_pha"), ST_16, NGAY):
        k = v2.xep_v2(BANG_V2, v2.ThamSoV2(*key[:4], so_thich=key[4]), ngay_bat_dau=key[5])
        an = ql.an_uong(QUAN, BANG_V2, k, TOA)
        bua += sum(bool(n["buoi"].get("sang") or n["buoi"].get("chieu")) + bool(n["buoi"].get("chieu") or [j for j in n["buoi"].get("toi", []) if j in BANG_V2.theo_id]) for n in k["ngay"])
        thay = set()
        for a in an:
            if "ghi_chu" in a:  # điểm kho nói không có quán ⇒ chỉ ghi chú, không quán (test_meal_note_…)
                assert a["quan"] == [] and (next(j for j, d in BANG_V2.theo_id.items() if d["ten"] == a["gan"]), a["bua"]) in ql.GHI_CHU_AN
                continue
            co += 1
            diem = next(d for d in BANG_V2.theo_id.values() if d["ten"] == a["gan"])
            assert 1 <= len(a["quan"]) <= ql.SO_QUAN
            nguon = []
            for q in a["quan"]:
                cum, goc = KEO[(q["ten"], _toa_tu_link(q["map_url"]))]
                assert cum == diem["cum"] and ql._km(TOA[diem["id"]], goc["toa"]) <= ql.KM_TOI_DA
                assert (q["ten"], q["map_url"]) not in thay
                thay.add((q["ten"], q["map_url"]))
                assert (q["nhan"] is None) == (goc["nguon"] == "kho") and (q["bai_id"] is not None) == (goc["nguon"] == "kho")
                nguon.append((goc["loai"] != "quan_an", ql.NGUON.index(goc["nguon"])))
            assert nguon == sorted(nguon)  # trong cùng loại quán kho trước
            assert len({l for l, _ in nguon}) == 1  # bữa có quán ăn ⇒ không kèm cà phê (cà phê chỉ khi không có quán ăn nào)
    assert co / bua >= 0.75


def test_far_or_unknown_point_gets_no_row():
    """Cụm rộng: điểm cách mọi quán cùng cụm > 2 km ⇒ không dòng; điểm không có toạ độ ⇒ không dòng (không đoán)."""
    xa = next(j for j, d in BANG_V2.theo_id.items() if j in TOA and QUAN.get(d["cum"])
              and min(ql._km(TOA[j], q["toa"]) for q in QUAN[d["cum"]]) > ql.KM_TOI_DA)
    khung = {"ngay": [{"ngay": 1, "buoi": {"sang": [xa], "chieu": [xa]}}]}
    assert ql.an_uong(QUAN, BANG_V2, khung, TOA) == []
    co_quan = next(j for j, d in BANG_V2.theo_id.items() if j in TOA and len(QUAN.get(d["cum"], [])) > 10)
    assert ql.an_uong(QUAN, BANG_V2, {"ngay": [{"ngay": 1, "buoi": {"sang": [co_quan]}}]}, {}) == []


def test_meal_note_for_points_without_restaurants():
    """Bạch Mã / Nhị Hồ: không quán trong 2 km ⇒ bữa có ghi chú theo kho (không bịa quán), vào cả chữ chép / tải."""
    for diem, _ in ql.GHI_CHU_AN:
        assert diem in BANG_V2.theo_id and not any(ql._km(TOA[diem], q["toa"]) <= ql.KM_TOI_DA for q in QUAN.get(BANG_V2.theo_id[diem]["cum"], []))
    khung = {"ngay": [{"ngay": 1, "buoi": {"sang": ["bach_ma"], "chieu": ["thac_nhi_ho"]}}]}
    an = ql.an_uong(QUAN, BANG_V2, khung, TOA)
    assert [(a["bua"], a["quan"], a["ghi_chu"]) for a in an] == [("trua", [], ql.GHI_CHU_AN[("bach_ma", "trua")]),
                                                                  ("toi", [], ql.GHI_CHU_AN[("thac_nhi_ho", "toi")])]
    assert ql.GHI_CHU_AN[("bach_ma", "trua")] in "\n".join(ql.dong_chu(an))
    khung = {"ngay": [{"ngay": 1, "buoi": {"sang": ["lang_non_tay_ho"], "chieu": ["deo_hai_van"]}}]}  # 15/11 tối: hai bữa từng trống
    assert [(a["bua"], a["quan"], a["ghi_chu"]) for a in ql.an_uong(QUAN, BANG_V2, khung, TOA)] == [
        ("trua", [], ql.GHI_CHU_AN[("lang_non_tay_ho", "trua")]), ("toi", [], ql.GHI_CHU_AN[("deo_hai_van", "toi")])]


def test_lunch_falls_back_to_other_points_of_the_day():
    """Tự thử 16/11: điểm cuối buổi sáng cách mọi quán > 2 km (Điện Hòn Chén) ⇒ trước đây cả ngày không bữa trưa; nay xét điểm sáng còn lại
    rồi điểm đầu buổi chiều. Điểm kho có ghi chú ăn (Bạch Mã) vẫn giữ ghi chú, không nhảy sang điểm khác."""
    khung = {"ngay": [{"ngay": 1, "buoi": {"sang": ["chua_thien_mu", "dien_hon_chen"], "chieu": ["doi_vong_canh"]}}]}
    trua = [a for a in ql.an_uong(QUAN, BANG_V2, khung, TOA) if a["bua"] == "trua"]
    assert len(trua) == 1 and trua[0]["gan"] == BANG_V2.theo_id["chua_thien_mu"]["ten"] and trua[0]["quan"]
    khung = {"ngay": [{"ngay": 1, "buoi": {"sang": ["chua_thien_mu", "bach_ma"], "chieu": []}}]}
    assert [a.get("ghi_chu") for a in ql.an_uong(QUAN, BANG_V2, khung, TOA) if a["bua"] == "trua"] == [ql.GHI_CHU_AN[("bach_ma", "trua")]]


@pytest.mark.parametrize("sua, loi", [
    ({"ten": "Quán <b>x</b>"}, "không hợp lệ"), ({"ten": "x" * 81}, "không hợp lệ"), ({"ten": "Ăn ở https://a.vn"}, "không hợp lệ"),
    ({"ten": "a\u0007b"}, "không hợp lệ"), ({"ten": "Qu\u202eán"}, "không hợp lệ"), ({"ten": "Quán\u200bA"}, "không hợp lệ"),
    ({"khong_bua": ["sang"]}, "không hợp lệ"), ({"khong_bua": []}, "không hợp lệ"), ({"khong_bua": "trua"}, "không hợp lệ"),
    ({"gio_kho": ""}, "không hợp lệ"), ({"gio_kho": "x" * 161}, "không hợp lệ"), ({"gio_kho": "xem https://a.vn"}, "không hợp lệ"), ({"gio_kho": 18}, "không hợp lệ"),
    ({"ten": "[Quán](x)"}, "không hợp lệ"), ({"ten": "Quán //x"}, "không hợp lệ"), ({"cum": "khong_co"}, "không hợp lệ"), ({"link": "https://evil.example/x"}, "không hợp lệ"),
])
def test_table_load_rejects_bad_rows(tmp_path, sua, loi):
    p = tmp_path / "q.json"
    dong = {"ten": "Quán A", "loai": "quan_an", "cum": "kinh_thanh", "toa": [16.47, 107.58], "nguon": "osm",
            "link": "https://www.openstreetmap.org/node/1", **sua}
    p.write_text(json.dumps({"quan": [dong]}), encoding="utf-8")
    with pytest.raises(ValueError, match=loi):
        ql.nap_bang_quan(p, BANG_V2.cum)


def test_restaurant_closed_at_a_meal_is_not_suggested_for_it():
    """23/11/2026: quán mà kho ghi giờ hoạt động không phủ một bữa (`khong_bua` của bảng) không được gợi ý cho bữa đó — Bún bò Bà Nga (18h–23h) từng ra
    ở bữa trưa của lịch mặc định và ở 756 / 960 tổ hợp biểu mẫu. Sàn trên mọi khung không ngày đi: 0 quán nằm ở bữa nó đóng."""
    q = {"ten": "Quán tối", "loai": "quan_an", "cum": "kinh_thanh", "toa": [16.47, 107.58], "nguon": "kho", "bai_id": "x.md", "khong_bua": ["trua"]}
    assert ql._chon([q], (16.47, 107.58), set(), "trua") == [] and ql._chon([q], (16.47, 107.58), set(), "toi") == [q]
    mac_dinh = ql.an_uong(QUAN, BANG_V2, v2.xep_v2(BANG_V2, v2.ThamSoV2(2)), TOA)
    assert mac_dinh and all(x["ten"] != "Bún bò Bà Nga" for a in mac_dinh if a["bua"] == "trua" for x in a["quan"])
    cam = {(x["ten"], b) for ds in QUAN.values() for x in ds for b in x.get("khong_bua", ())}
    assert ("Bún bò Bà Nga", "trua") in cam  # bảng đang chạy phải mang trường này, không thì sàn dưới không kiểm gì
    for key in itertools.product(range(1, 6), (0, 1), (False, True), ("nhe_nhang", "can_bang", "kham_pha"), ST_16):
        for a in ql.an_uong(QUAN, BANG_V2, v2.xep_v2(BANG_V2, v2.ThamSoV2(*key[:4], so_thich=key[4])), TOA):
            assert not [x["ten"] for x in a["quan"] if (x["ten"], a["bua"]) in cam]


def test_flag_needs_v2_and_table():
    with pytest.raises(ValueError, match="quan_lich needs"):
        flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=False, anh_lich=False, quan_lich=True)
    on = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, anh_lich=False, quan_lich=True)
    assert on.quan_bang is not None and on.quan_toa_do
    assert flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, anh_lich=False).quan_bang is None


def test_q1_restaurants_not_in_model_message_and_off_text_unchanged():
    khung = v2.xep_v2(BANG_V2, v2.ThamSoV2(3, 0, False, "can_bang", so_thich=()))
    lich = v2.dung_lich(BANG_V2, khung, {j: i for i, j in enumerate(v2.diem_v2(khung), start=1)})
    co = copy.deepcopy(lich)
    co["an"] = ql.an_uong(QUAN, BANG_V2, khung, TOA)
    assert co["an"]
    assert v2.tin_nhan_model(co, "TL") == v2.tin_nhan_model(lich, "TL")
    cau = {m["id_muc"]: "Câu." for m in v2.moi_muc(lich)}
    tat, bat = v2.ghep_chu(lich, cau), v2.ghep_chu(co, cau)
    assert bat.startswith(tat) and "Ăn uống gợi ý" in bat[len(tat):] and "Ăn uống" not in tat


def test_restaurant_photo_field_is_checked_at_load_and_every_photo_file_exists(tmp_path):
    # (C 14/11 tối) ảnh quán ngoài kho: chỉ tên file dưới anh/quan/; quán kho không mang trường ảnh (giao diện dùng ảnh Khám phá theo mã bài)
    co_anh = [q for ds in QUAN.values() for q in ds if q.get("anh")]
    assert co_anh and all(q["nguon"] != "kho" for q in co_anh)
    for q in co_anh:  # bảng nhắc tới ảnh nào thì file đó phải có trong frontend/public (thiếu ⇒ thẻ bữa hiện ảnh vỡ)
        assert (BACKEND.parent / "frontend/public/anh" / f"{q['anh']}.jpg").is_file(), q["anh"]
    mau = next(q for q in co_anh)
    for xau in ("../x", "quan/a.jpg", "https://x/y", "kp/k1"):
        p = tmp_path / "b.json"; p.write_text(json.dumps({"quan": [{**mau, "anh": xau}]}), encoding="utf-8")
        with pytest.raises(ValueError):
            ql.nap_bang_quan(p, BANG_V2.cum)
    kho = next(q for ds in QUAN.values() for q in ds if q["nguon"] == "kho")
    p = tmp_path / "k.json"; p.write_text(json.dumps({"quan": [{**kho, "anh": "quan/x"}]}), encoding="utf-8")
    with pytest.raises(ValueError):
        ql.nap_bang_quan(p, BANG_V2.cum)
    assert ql._hien(mau)["anh"] == mau["anh"] and ql._hien(kho)["anh"] is None


KHO = BACKEND.parent / "knowledge-base-hue"


@pytest.mark.skipif(not KHO.is_dir(), reason="bản chép không có kho")
def test_no_kb_place_in_the_table_is_marked_closed_in_its_own_article():
    """21/11/2026: bảng bản 1 còn một quán mà chính bài kho của nó ghi trạng thái đã đóng cửa ⇒ mục ăn uống của thẻ lịch có thể gợi ý nó. Mọi quán nguồn
    kho trong bảng: bài phải còn trong kho và dòng "Trạng thái" của bài (nếu có) không nói đóng cửa / ngừng hoạt động. Kho đổi ⇒ test này báo để dựng lại bảng."""
    kho = [q for ds in QUAN.values() for q in ds if q["nguon"] == "kho"]
    assert len(kho) >= 40
    da_dong = []
    for q in kho:
        bai = KHO / q["bai_id"]
        assert bai.is_file(), q["bai_id"]
        trang_thai = [d for d in bai.read_text(encoding="utf-8").splitlines() if d.lstrip("-* ").lower().startswith("trạng thái")]
        if any(tu in d.lower() for d in trang_thai for tu in ("đóng cửa", "ngừng hoạt động", "ngưng hoạt động")):
            da_dong.append(q["bai_id"])
    assert da_dong == []
