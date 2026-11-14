"""“Lên kế hoạch” đợt 1 — bước (a): hợp đồng `truong` mới + biểu mẫu bốn nhóm, bộ xếp cũ (plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md`
§3 (a), spec bản 3.3 §5) — 0 USD.

Kiểm: bảng giá trị hợp lệ / không hợp lệ từng trường · đổi giá trị cũ ⇒ mới ⇒ cũ · cờ tắt ⇒ giá trị mới bị 422 như thân sai khuôn hôm nay và
`/api/tinh_nang` không có khoá mới · cờ bật ⇒ giá trị mới ra đúng chuỗi gửi model như giá trị cũ tương ứng (bộ xếp cũ). Đường biểu mẫu: SDK thật +
client giả có kịch bản (không mạng) + Qdrant thật (đọc) + bảng điểm thật (private) — như `test_cong_dot_1.py`. “Cờ tắt giống byte” của chuỗi gửi
model đo thêm bằng Q1 (`capture_all.py`, report).
"""
import asyncio
import copy
import dataclasses
import json
import datetime as dt
import itertools
from pathlib import Path

import pytest
from pydantic import ValidationError

from llm import ngay_lich as nl
from llm.assistant import AnswerTrace, AssistantFlags
from llm.hoi_lai import GIA_TRI, NGAY_DI_TOI_DA, TruongInput, co_gia_tri_moi, doi_sang_cu, doi_sang_moi, loi_v2
from test_api_chat import chat_log_records, metric_lines
from test_b2_tool_loop import answer, deps, generator  # noqa: F401  (fixture `deps` dùng chung)
from test_cong_dot_1 import SETTINGS, FORM, OFF, _restore, _with, app_client, chu_gui, flags_from, viet_theo_khung  # noqa: F401  (fixture `app_client`)

V2 = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, anh_lich=False)  # cờ ảnh tự đặt (settings.yaml bật từ 14/11)
V2_BANG_PATH = Path(__file__).resolve().parents[1] / SETTINGS["assistant"]["lich_trinh_bang_v2"]
HOM_NAY = dt.date(2026, 11, 13)


# ---------- bảng giá trị của từng trường (khuôn) ----------

HOP_LE = [
    {"so_ngay": "5"}, {"so_ngay": "4+"}, {"so_ngay": "1", "nguoi_lon": 1}, {"so_ngay": "2", "nguoi_lon": 10, "tre_em": 6},
    {"so_ngay": "2", "tre_em": 0}, {"so_ngay": "2", "lon_tuoi": False}, {"so_ngay": "3", "kieu_di": "can_bang"},
    {"so_ngay": "3", "so_thich": ["di_tich", "am_thuc"]}, {"so_ngay": "3", "so_thich": "di_tich"}, {"so_ngay": "1", "ngay_di": "2026-12-20"},
    {"so_ngay": "2", "so_thich": []},  # bộ đo của E gửi [] cho "không chọn sở thích" (lỗi bắt ở lượt nghiệm thu 13/11)
    {"so_ngay": "2", "di_cung": "cap_doi", "kieu_di": "thong_tha"},
]
KHONG_HOP_LE = [
    {"so_ngay": "6"}, {"so_ngay": "0"}, {"so_ngay": 2}, {"nguoi_lon": 0}, {"nguoi_lon": 11}, {"nguoi_lon": "2"}, {"nguoi_lon": True},
    {"nguoi_lon": 2.0}, {"tre_em": -1}, {"tre_em": 7}, {"lon_tuoi": "co"}, {"lon_tuoi": 1}, {"kieu_di": "vua"},
    {"so_thich": ["di_tich", "am_thuc", "chup_anh"]}, {"so_thich": ["di_tich", "di_tich"]}, {"so_thich": ["mua_sam"]},
    {"ngay_di": "20/12/2026"}, {"ngay_di": 20261220}, {"ngay_di": "2026-02-30"},
    {"di_cung": "cap_doi", "nguoi_lon": 2}, {"di_cung": "nhom_ban", "tre_em": 0}, {"ten": "Lan"},
]


@pytest.mark.parametrize("truong", HOP_LE)
def test_truong_accepts_valid_values(truong):
    TruongInput.model_validate_json(json.dumps(truong))


@pytest.mark.parametrize("truong", KHONG_HOP_LE)
def test_truong_rejects_invalid_values(truong):
    with pytest.raises(ValidationError):
        TruongInput.model_validate_json(json.dumps(truong))


def test_old_values_are_not_new_and_new_values_are():
    for combo in itertools.product(GIA_TRI["so_ngay"], [None, *GIA_TRI["di_cung"]], [None, *GIA_TRI["kieu_di"]], [None, *GIA_TRI["so_thich"]]):
        cu = {k: v for k, v in zip(("so_ngay", "di_cung", "kieu_di", "so_thich"), combo) if v}
        assert not co_gia_tri_moi(TruongInput(**cu)), cu
    for moi in ({"so_ngay": "4"}, {"so_ngay": "5"}, {"kieu_di": "can_bang"}, {"kieu_di": "nhe_nhang"}, {"so_thich": ["di_tich"]},
                {"nguoi_lon": 2}, {"tre_em": 0}, {"lon_tuoi": False}, {"ngay_di": HOM_NAY}):
        assert co_gia_tri_moi(TruongInput(**moi)), moi


def test_v2_limits_by_vietnam_day_and_shown_interests():
    def loi(**t):
        return loi_v2(TruongInput(**t), HOM_NAY)
    assert loi(ngay_di=HOM_NAY) is None and loi(ngay_di=HOM_NAY + dt.timedelta(days=NGAY_DI_TOI_DA)) is None
    assert loi(ngay_di=HOM_NAY - dt.timedelta(days=1)) == "ngay_di"
    assert loi(ngay_di=HOM_NAY + dt.timedelta(days=NGAY_DI_TOI_DA + 1)) == "ngay_di"
    assert loi(so_ngay="5") is None and loi(so_thich=["di_tich", "am_thuc"]) is None  # bộ xếp mới (từ bước (c)) nhận đủ khuôn trường
    assert loi_v2(TruongInput(so_thich=["chup_anh"]), HOM_NAY, ("di_tich",)) == "so_thich_an"
    assert loi_v2(TruongInput(so_thich="chup_anh"), HOM_NAY, ("di_tich",)) is None  # giá trị cũ (chuỗi) không qua kiểm bản 2


# ---------- đổi giá trị cũ ⇔ mới ----------

def test_old_values_round_trip_through_new_shape():
    """Mọi tổ hợp giá trị cũ: cũ ⇒ mới ⇒ cũ ra đúng như cũ (bộ xếp cũ nhận lại đúng tham số). "4+" ⇒ "4" ⇒ "4+"."""
    for combo in itertools.product(GIA_TRI["so_ngay"], [None, *GIA_TRI["di_cung"]], [None, *GIA_TRI["kieu_di"]], [None, *GIA_TRI["so_thich"]]):
        cu = {k: v for k, v in zip(("so_ngay", "di_cung", "kieu_di", "so_thich"), combo) if v}
        moi = doi_sang_moi(cu)
        assert "di_cung" not in moi and not isinstance(moi.get("so_thich", []), str)
        TruongInput(**moi)  # khuôn mới hợp lệ
        assert doi_sang_cu(moi) == cu, cu


def test_old_to_new_values():
    assert doi_sang_moi({"so_ngay": "4+", "kieu_di": "thong_tha", "so_thich": "am_thuc", "di_cung": "gia_dinh_tre_em"}) == {
        "so_ngay": "4", "kieu_di": "nhe_nhang", "so_thich": ["am_thuc"], "nguoi_lon": 2, "tre_em": 1}
    assert doi_sang_moi({"so_ngay": "2", "kieu_di": "day_lich", "di_cung": "nguoi_lon_tuoi"}) == {
        "so_ngay": "2", "kieu_di": "kham_pha", "nguoi_lon": 2, "lon_tuoi": True}
    assert doi_sang_moi({"so_ngay": "1", "di_cung": "nhom_ban"}) == {"so_ngay": "1", "nguoi_lon": 4}


def test_new_to_old_values():
    assert doi_sang_cu({"so_ngay": "3", "nguoi_lon": 3, "tre_em": 2, "lon_tuoi": True}) == {"so_ngay": "3", "di_cung": "gia_dinh_tre_em"}  # trẻ em thắng
    assert doi_sang_cu({"so_ngay": "3", "nguoi_lon": 5, "tre_em": 0, "lon_tuoi": True}) == {"so_ngay": "3", "di_cung": "nguoi_lon_tuoi"}
    assert [doi_sang_cu({"so_ngay": "1", "nguoi_lon": n, "tre_em": 0, "lon_tuoi": False})["di_cung"] for n in (1, 2, 3, 10)] == [
        "mot_minh", "cap_doi", "nhom_ban", "nhom_ban"]
    assert doi_sang_cu({"so_ngay": "4", "kieu_di": "can_bang", "so_thich": ["thien_nhien"], "ngay_di": HOM_NAY}) == {
        "so_ngay": "4+", "so_thich": "thien_nhien"}  # mức giữa ⇒ không kiểu đi; ngày đi chưa dùng ở bộ xếp cũ
    assert doi_sang_cu({"so_ngay": "2"}) == {"so_ngay": "2"}


# ---------- cờ ----------

def test_flag_needs_form_flag_and_known_cells():
    with pytest.raises(ValueError, match="len_ke_hoach_v2 needs"):
        flags_from(lich_trinh_bieu_mau=False, len_ke_hoach_v2=True)
    with pytest.raises(ValueError, match="len_ke_hoach_o_hien"):
        dataclasses.replace(V2, len_ke_hoach_o_hien=("so_ngay", "ngan_sach"))
    assert V2.len_ke_hoach_v2 and V2.len_ke_hoach_o_hien and set(V2.len_ke_hoach_o_hien) <= {
        "so_ngay", "nguoi_lon", "tre_em", "lon_tuoi", "kieu_di", "so_thich", "ngay_di"}
    assert not FORM.len_ke_hoach_v2 and AssistantFlags().len_ke_hoach_o_hien == ()


# ---------- route ----------

NEW_FORM = {"so_ngay": "2", "nguoi_lon": 2, "tre_em": 1, "lon_tuoi": False, "so_thich": ["di_tich"]}
OLD_SAME = {"so_ngay": "2", "di_cung": "gia_dinh_tre_em", "so_thich": "di_tich"}


def _post(client, path, truong, bieu_mau=True):
    return client.post(path, json={"query": "x", "bieu_mau": bieu_mau, "truong": truong})


@pytest.mark.parametrize("path", ["/api/chat", "/api/chat/stream"])
def test_new_values_rejected_like_bad_body_when_flag_off(app_client, caplog, path):
    """Cờ tắt: giá trị mới ⇒ đúng 422 của handler thân sai khuôn, không dòng `chat_metrics`, không gọi model (= hôm nay, khi khuôn chưa có
    trường mới). Cờ bật: lượt không phải biểu mẫu (thẻ hỏi lại) vẫn không nhận giá trị mới."""
    app, client = app_client
    gen = generator(lambda n, kw: [answer("x")])
    bad_shape = None
    try:
        original = _with(app, FORM, gen)
        with chat_log_records(caplog) as records:
            bad_shape = _post(client, path, {"so_ngay": "9"})  # thân sai khuôn: mốc của hôm nay
            off = [_post(client, path, t) for t in ({"so_ngay": "4"}, {"so_ngay": "2", "nguoi_lon": 2}, NEW_FORM,
                                                    {"so_ngay": "2", "kieu_di": "can_bang"}, {"so_ngay": "2", "so_thich": ["di_tich"]})]
            _with(app, V2)
            not_form = _post(client, path, {"so_ngay": "2", "nguoi_lon": 2}, bieu_mau=False)
    finally:
        _restore(app, original)
    assert bad_shape.status_code == 422
    assert all((r.status_code, r.json()) == (422, bad_shape.json()) for r in [*off, not_form])
    assert metric_lines(records) == [] and gen.client.responses.calls == []


@pytest.mark.parametrize("path", ["/api/chat", "/api/chat/stream"])
def test_flag_on_date_limits_rejected(app_client, path):
    app, client = app_client
    hom = nl.hom_nay()
    original = _with(app, V2, generator(lambda n, kw: [answer("x")]))
    try:
        rs = [_post(client, path, t) for t in (
            {"so_ngay": "2", "ngay_di": (hom - dt.timedelta(days=1)).isoformat()},
            {"so_ngay": "2", "ngay_di": (hom + dt.timedelta(days=NGAY_DI_TOI_DA + 1)).isoformat()},
            {"so_ngay": "2", "so_thich": ["di_tich", "am_thuc", "chup_anh"]})]
    finally:
        _restore(app, original)
    assert [r.status_code for r in rs] == [422] * 3


def test_feature_flags_key_only_when_flag_on(app_client):
    app, client = app_client
    anh_goc, app.state.anh = app.state.anh, None
    try:
        original = _with(app, FORM)
        off = client.get("/api/tinh_nang").json()
        _with(app, V2)
        on = client.get("/api/tinh_nang").json()
    finally:
        _restore(app, original)
        app.state.anh = anh_goc
    co_cu = {"lich_trinh_bieu_mau": True, "thoi_tiet": FORM.thoi_tiet, "anh": False, "tra_web": FORM.tra_web, "ban_do_lich": FORM.ban_do_lich}
    assert off == co_cu  # cờ tắt: khoá mới vắng hẳn (không null, không rỗng)
    assert on == {**co_cu, "len_ke_hoach_v2": {"o_hien": list(V2.len_ke_hoach_o_hien), "so_ngay_toi_da": 5, "so_thich_toi_da": 2,
                                               "so_thich_hien": list(V2.so_thich_hien)}}
    assert set(V2.so_thich_hien) == set(V2.bang_lich_v2.loai_hien) - set(V2.len_ke_hoach_so_thich_an)


# =====================================================================================================================================
# Bước (b): bảng v8 + bộ xếp mới `xep_v2` + mô phỏng toàn tổ hợp (plan §3 (b), spec 5b / 5c.1 / 5c.3 / 5c.4) — 0 USD, không model
# =====================================================================================================================================

from llm import lich_trinh_v2 as v2  # noqa: E402

def _diem(id_, cum, loai=("di_tich",), thoi_luong="ngan", bac_thang=None, buoi=("sang", "chieu")):
    return {"id": id_, "ten": id_, "cum": cum, "loai": list(loai), "thoi_luong": thoi_luong, "gio_mo_cua": None, "nguon": f"x/{id_}.md",
            "buoi": list(buoi), "quan_the": False, "luu_y": None, "ten_khac": [], "trong_nha": "ngoai_troi", "bac_thang": bac_thang, "uu_tien": {}}


def _bang(tmp_path, diem, uu_tien=None, ten="b.json"):
    cum = {c: c for c in ("kinh_thanh", "bo_nam", "an_cuu", "thuy_xuan", "kim_long", "lang_xa", "dong_bien", "nam_xa")}
    p = tmp_path / ten
    p.write_text(json.dumps({"cum": cum, "diem": diem, "uu_tien_theo_so_thich": uu_tien or {"chung": [diem[0]["id"]]}}), encoding="utf-8")
    return v2.nap_bang_v2(p)


def test_v2_table_load_checks(tmp_path):
    ok = [_diem("a", "kinh_thanh"), _diem("b", "bo_nam", loai=("thien_nhien",))]
    assert _bang(tmp_path, ok).loai_hien == ()  # < 4 điểm mỗi loại ⇒ không loại nào hiện
    for sai, uu in ((dict(ok[0], thoi_luong=None), None), ({k: v for k, v in ok[0].items() if k != "trong_nha"}, None),
                    (dict(ok[0], bac_thang="it"), None), (ok[0], {"chung": ["khong_co"]}), (ok[0], {"thien_nhien": ["a"], "chung": ["a"]}),
                    (ok[0], {"di_tich": ["a"]})):
        with pytest.raises(ValueError):
            _bang(tmp_path, [sai, ok[1]], uu)
    bon = [_diem(f"t{i}", "bo_nam", loai=("thien_nhien",)) for i in range(4)]
    assert _bang(tmp_path, [ok[0], *bon]).loai_hien == ("thien_nhien",)


def test_v2_flag_needs_table_and_fails_loudly(tmp_path):
    with pytest.raises(ValueError, match="lich_trinh_bang_v2"):
        dataclasses.replace(V2, bang_lich_v2=None)
    with pytest.raises(FileNotFoundError):
        flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, lich_trinh_bang_v2=str(tmp_path / "khong_co.json"))
    assert V2.bang_lich_v2 is not None and FORM.bang_lich_v2 is None  # cờ tắt ⇒ không nạp (clone không có data/ vẫn chạy)


def ts(n, **kw):
    return v2.ThamSoV2(n, **kw)


def test_rule_minutes_per_session(tmp_path):
    """5c.3: 2 ngắn cùng cụm = 165 phút ⇒ vừa cân bằng; nửa buổi + ngắn = 240 ⇒ chỉ khám phá nhiều; nhẹ nhàng / nhóm hạn chế luôn 1 điểm / buổi."""
    b = _bang(tmp_path, [_diem("n1", "kinh_thanh"), _diem("n2", "kinh_thanh"), _diem("n3", "kinh_thanh"), _diem("n4", "kinh_thanh")])
    # điểm đầu của sáng rồi chiều chọn trước, điểm thêm sau (5b: kiểu đi là bậc thấp nhất)
    assert v2.xep_v2(b, ts(1, kieu_di="can_bang"))["ngay"][0]["buoi"] == {"sang": ["n1", "n3"], "chieu": ["n2", "n4"], "toi": []}
    assert v2.xep_v2(b, ts(1, kieu_di="nhe_nhang"))["ngay"][0]["buoi"] == {"sang": ["n1"], "chieu": ["n2"], "toi": []}
    assert v2.xep_v2(b, ts(1, kieu_di="kham_pha", tre_em=1))["ngay"][0]["buoi"] == {"sang": ["n1"], "chieu": ["n2"], "toi": []}
    b = _bang(tmp_path, [_diem("h", "kinh_thanh", thoi_luong="nua_buoi"), _diem("n", "kinh_thanh"), _diem("n2", "kinh_thanh")])
    assert v2.xep_v2(b, ts(1, kieu_di="can_bang"))["ngay"][0]["buoi"]["sang"] == ["h"]  # 150 + 15 + 75 = 240 > 210
    assert v2.xep_v2(b, ts(1, kieu_di="kham_pha"))["ngay"][0]["buoi"]["sang"] == ["h", "n2"]  # = 240 ⇒ vừa
    b = _bang(tmp_path, [_diem("a", "kinh_thanh"), _diem("b", "an_cuu")])  # khác cụm, không kề ⇒ không ghép trong một buổi
    assert v2.xep_v2(b, ts(1, kieu_di="kham_pha"))["ngay"][0]["buoi"]["sang"] == ["a"]


def test_rule_far_cluster_only_from_day_2_of_3(tmp_path):
    b = _bang(tmp_path, [_diem("xa", "nam_xa", loai=("thien_nhien",)), _diem("xa2", "nam_xa", loai=("thien_nhien",)),
                         *[_diem(f"d{i}", "kinh_thanh") for i in range(8)]], {"chung": ["d0"], "thien_nhien": ["xa"]})
    for n in (1, 2):
        assert "xa" not in v2.diem_v2(v2.xep_v2(b, ts(n, so_thich=("thien_nhien",))))
    k = v2.xep_v2(b, ts(3, so_thich=("thien_nhien",)))
    assert "xa" not in v2.diem_v2({"ngay": k["ngay"][:1]}) and "xa" in k["ngay"][1]["buoi"]["sang"] + k["ngay"][1]["buoi"]["chieu"]
    assert v2.kiem_khung_v2(b, k) == []


def test_rule_priority_first_and_two_interests_interleave(tmp_path):
    b = _bang(tmp_path, [_diem("a1", "kinh_thanh"), _diem("a2", "kinh_thanh"), _diem("b1", "bo_nam", loai=("am_thuc",)),
                         _diem("b2", "bo_nam", loai=("am_thuc",)), _diem("a3", "kinh_thanh")],
              {"chung": ["a1"], "di_tich": ["a3", "a1"], "am_thuc": ["b2"]})
    pool, _, uu = v2.thu_tu_xet(b, ("di_tich", "am_thuc"))
    assert pool[:3] == ["a3", "b2", "a1"] and uu == {"a3", "b2", "a1"}  # A1, B1, A2 rồi điểm hợp sở thích theo bảng
    k = v2.xep_v2(b, ts(1, kieu_di="nhe_nhang", so_thich=("di_tich", "am_thuc")))
    assert k["ngay"][0]["buoi"] == {"sang": ["a3"], "chieu": ["b2"], "toi": []}


def test_pair_unusable_priority_does_not_take_the_other_interest_turn(tmp_path):
    """Lỗi bắt được ở mô phỏng: ưu tiên cụm xa (bị loại khi < 3 ngày) vẫn giữ chỗ khi xen kẽ ⇒ lượt của sở thích đó rơi sang điểm sở thích kia."""
    b = _bang(tmp_path, [_diem("a1", "kinh_thanh"), _diem("a2", "kinh_thanh"), _diem("xa", "nam_xa", loai=("thien_nhien",)),
                         _diem("t2", "dong_bien", loai=("thien_nhien",))], {"chung": ["a1"], "di_tich": ["a1", "a2"], "thien_nhien": ["xa", "t2"]})
    k = v2.xep_v2(b, ts(1, kieu_di="nhe_nhang", so_thich=("di_tich", "thien_nhien")))
    assert v2.diem_v2(k) == ["a1", "t2"] and k["thieu_uu_tien"] == []


def test_pair_extra_point_does_not_block_priority_of_afternoon(tmp_path):
    """Lỗi bắt được ở mô phỏng (thứ tự 5b: ưu tiên bậc 4 > kiểu đi bậc 7): điểm thêm của buổi sáng không được chiếm suất cụm thứ hai của ngày
    khi điểm ưu tiên buổi chiều cần nó."""
    b = _bang(tmp_path, [_diem("l1", "kinh_thanh", loai=("le_hoi_nghe_thuat",)), _diem("l2", "kim_long", loai=("le_hoi_nghe_thuat",)),
                         _diem("c1", "dong_bien", loai=("chup_anh",), thoi_luong="nua_buoi")],
              {"chung": ["l1"], "le_hoi_nghe_thuat": ["l1", "l2"], "chup_anh": ["c1"]})
    k = v2.xep_v2(b, ts(1, kieu_di="kham_pha", so_thich=("le_hoi_nghe_thuat", "chup_anh")))
    assert "c1" in v2.diem_v2(k) and v2.kiem_khung_v2(b, k) == []


def test_pair_stairs_vs_priority_and_cluster(tmp_path):
    """Bậc 1 (nhóm hạn chế tránh bậc thang) thắng bậc 4 (ưu tiên): điểm ưu tiên nhiều bậc thang bị thay bằng điểm cùng cụm ⇒ ghi chú do code.
    Điểm thay phải cùng cụm (không kéo ngày sang cụm khác); không có điểm thay cùng cụm ⇒ giữ điểm ưu tiên."""
    b = _bang(tmp_path, [_diem("p", "kinh_thanh", bac_thang="nhieu"), _diem("q", "kinh_thanh"), _diem("q2", "kinh_thanh"), _diem("r", "bo_nam"),
                         _diem("s", "an_cuu", bac_thang="nhieu")], {"chung": ["p", "s"], "di_tich": ["p", "s"]})
    k = v2.xep_v2(b, ts(1, lon_tuoi=True, so_thich=("di_tich",)))
    assert v2.diem_v2(k) == ["q", "q2"] and k["thay_bac_thang"] == [{"diem": "p", "thay": "q"}]
    b2 = _bang(tmp_path, [_diem("p", "kinh_thanh", bac_thang="nhieu"), _diem("q", "kinh_thanh")], {"chung": ["p"], "di_tich": ["p"]})
    k = v2.xep_v2(b2, ts(1, lon_tuoi=True, so_thich=("di_tich",)))  # hết điểm thay cùng cụm ở buổi chiều ⇒ giữ điểm ưu tiên, không ghi chú
    assert v2.diem_v2(k) == ["q", "p"] and k["thay_bac_thang"] == []
    k0 = v2.xep_v2(b, ts(1, so_thich=("di_tich",)))
    assert "p" in v2.diem_v2(k0) and k0["thay_bac_thang"] == []
    b = _bang(tmp_path, [_diem("p", "kinh_thanh", bac_thang="nhieu"), _diem("r", "bo_nam")], {"chung": ["p"], "di_tich": ["p"]})
    assert v2.diem_v2(v2.xep_v2(b, ts(1, tre_em=2, so_thich=("di_tich",))))[0] == "p"


def test_kiem_khung_v2_catches_violations(tmp_path):
    b = _bang(tmp_path, [_diem("a", "kinh_thanh"), _diem("b", "kinh_thanh", thoi_luong="nua_buoi"), _diem("c", "an_cuu"),
                         _diem("x", "nam_xa"), _diem("t", "bo_nam", loai=("thien_nhien",))])
    good = v2.xep_v2(b, ts(1, kieu_di="can_bang"))
    assert v2.kiem_khung_v2(b, good) == []

    def sai(sang, chieu=(), **tham):
        k = copy.deepcopy(good)
        k["ngay"][0]["buoi"].update(sang=list(sang), chieu=list(chieu))
        k["tham_so"].update(tham)
        k["ngoai_so_thich"] = [i for i in (*sang, *chieu) if k["tham_so"]["so_thich"] and b.theo_id[i]["loai"] == ["di_tich"]]
        return v2.kiem_khung_v2(b, k)
    assert "vuot_quy" in sai(["a", "b"])  # 75 + 15 + 150 > 210
    assert "ghep_khong_ke" in sai(["a", "c"], kieu_di="kham_pha")
    assert "cum_xa" in sai(["x"])
    assert "qua_day_buoi" in sai(["a", "t"], tre_em=1)
    assert "trung_diem" in sai(["a"], ["a"])
    assert "ngay_rong" in sai([])
    chong = copy.deepcopy(good)  # review 14/11 M-1: sáng kết thúc sau giờ đầu buổi chiều
    chong["ngay"][0]["buoi"].update(sang=["a"], chieu=["c"])
    chong["gio"] = {"a": "11:45 – 13:00", "c": "13:00 – 14:15"}
    assert "sang_chong_chieu" not in v2.kiem_khung_v2(b, chong)
    chong["gio"]["a"] = "11:50 – 13:05"
    assert "sang_chong_chieu" in v2.kiem_khung_v2(b, chong)
    assert "lap_khong_nhan" in v2.kiem_khung_v2(b, dict(good, tham_so=dict(good["tham_so"], so_thich=["thien_nhien"])))


# ---------- mô phỏng toàn tổ hợp trên bảng v8 thật (private) ----------

ST_16 = [()] + [(s,) for s in v2.LOAI_DIEM_THU_TU] + list(itertools.combinations(v2.LOAI_DIEM_THU_TU, 2))
KIEU = ("nhe_nhang", "can_bang", "kham_pha")


@pytest.fixture(scope="module")
def mo_phong():
    b = V2.bang_lich_v2
    kq = {key: v2.xep_v2(b, v2.ThamSoV2(*key[:4], so_thich=key[4]))
          for key in itertools.product(range(1, 6), (0, 1), (False, True), KIEU, ST_16)}
    assert len(kq) == 960
    return b, kq


def test_simulation_always_rules(mo_phong):
    b, kq = mo_phong
    T = b.theo_id
    loi = {key: v2.kiem_khung_v2(b, k) for key, k in kq.items() if v2.kiem_khung_v2(b, k)}
    assert loi == {}  # 0 lỗi khung · 0 điểm lặp · 0 ngày rỗng · ≤ 2 cụm kề · đúng n ngày
    for (n, te, lt_, kieu, st), k in kq.items():
        ids = v2.diem_v2(k)
        for s in st or ("chung",):  # điểm ưu tiên số 1 có mặt (trừ cụm xa khi < 3 ngày)
            dau = next(i for i in b.uu_tien[s] if T[i]["cum"] != v2.CUM_XA or n >= 3)
            assert dau in ids, (n, te, lt_, kieu, st, s)
        assert not any(T[i]["cum"] == v2.CUM_XA for b_ in v2.BUOI_NGAY for i in k["ngay"][0]["buoi"][b_])
        if n >= 3:
            for s in st:
                for u in b.uu_tien[s]:
                    if T[u]["cum"] == v2.CUM_XA:
                        assert sum(u in v2.diem_v2({"ngay": [ng]}) for ng in k["ngay"][1:]) == 1
            assert len(v2.diem_v2(v2.xep_v2(b, v2.ThamSoV2(n, te, lt_, kieu, st), ngay_1_khong_xa=False))) <= len(ids)
        if te or lt_:
            assert all(len(v2.diem_v2({"ngay": [ng]})) <= 2 and not ng["buoi"]["toi"] for ng in k["ngay"])
        if len(st) == 2 and n >= 2:
            assert all(any(s in T[i]["loai"] for i in ids) for s in st)
    for n, te, lt_, st in itertools.product(range(1, 6), (0, 1), (False, True), ST_16):
        so = [len(v2.diem_v2(kq[(n, te, lt_, k, st)])) for k in KIEU]
        assert so[0] <= so[1] <= so[2]
        if te or lt_:  # nhóm hạn chế: ba mức cho cùng một khung
            assert kq[(n, te, lt_, "nhe_nhang", st)]["ngay"] == kq[(n, te, lt_, "kham_pha", st)]["ngay"]
    assert {json.dumps(v2.xep_v2(b, v2.ThamSoV2(3, so_thich=("di_tich",), nguoi_lon=a))["ngay"]) for a in range(1, 11)} == {
        json.dumps(kq[(3, 0, False, "can_bang", ("di_tich",))]["ngay"])}  # đổi số người lớn ⇒ khung giống hệt (kiểu đi mặc định = cân bằng)


def test_simulation_floors(mo_phong):
    """Sàn ghi trước (plan §3 (b)); số đo 13/11 (bảng v8 `6335b21eb243`): kiểu đi 65 / 80 = 81 % · bậc thang giảm 420 / 720 = 58 % · không bao giờ
    xếp 1 · sở thích thấp nhất: chụp ảnh / lễ hội 50 % (lễ hội 43 % trước khi gắn nhãn Cung An Định — A quyết)."""
    b, kq = mo_phong
    T = b.theo_id
    nhom = list(itertools.product(range(1, 6), ST_16))
    khac3 = sum(len({json.dumps(kq[(n, 0, False, k, st)]["ngay"]) for k in KIEU}) == 3 for n, st in nhom)
    assert khac3 / len(nhom) >= 0.70
    bt = lambda k: sum(T[i]["bac_thang"] == "nhieu" for i in v2.diem_ban_ngay(k))  # noqa: E731
    cap = [(k, kq[(n, 0, False, kieu, st)]) for (n, te, lt_, kieu, st), k in kq.items() if te or lt_]
    assert sum(bt(a) < bt(c) for a, c in cap) / len(cap) >= 0.50 and not any(bt(a) > bt(c) for a, c in cap)
    ban_ngay = {d["id"] for d in b.diem if set(d["buoi"]) & set(v2.BUOI_NGAY)}
    assert len(ban_ngay - {i for k in kq.values() for i in v2.diem_v2(k)}) <= 3
    # mỗi sở thích ≥ 50 % suất sáng / chiều của TỪNG lịch 2 ngày (A quyết 13/11: đọc theo từng tổ hợp) — dưới sàn ⇒ ô ẩn bằng cấu hình
    duoi = {s for s in v2.LOAI_DIEM_THU_TU for te, lt_, kieu in itertools.product((0, 1), (False, True), KIEU)
            if (lambda ids: sum(s in T[i]["loai"] for i in ids) / len(ids))(v2.diem_ban_ngay(kq[(2, te, lt_, kieu, (s,))])) < 0.50}
    assert duoi == set(V2.len_ke_hoach_so_thich_an)


# =====================================================================================================================================
# Bước (c): khuôn `lich` bản 2 + model trả mảng {id_muc, cau} + kiểm từng câu + sự kiện lich_khung / lich_cau / lich_xong — model giả, 0 USD
# =====================================================================================================================================

import re as _re  # noqa: E402

from llm.full_corpus_prompt import LICH_V2_LOI_DAN  # noqa: E402

_MUC = _re.compile(r"^- (n\d+-\w+-\d+): .+ \(tài liệu \[(\d+)\]\)$", _re.M)


def cau_json(items) -> dict:
    """Mục đầu ra của model giả cho lần gọi viết câu: đúng khuôn `{cau: [...]}`."""
    return {"type": "message", "id": f"msg_v2_{id(items)}", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": json.dumps({"cau": items}, ensure_ascii=False), "annotations": []}]}


def viet_dung(kw, sua=None):
    """Model giả "đúng luật": một câu cho mỗi id_muc trong tin nhắn, mã nguồn đúng. `sua(items)` để làm hỏng có chủ đích."""
    items = [{"id_muc": i, "cau": f"Ở đây có nhiều thứ đáng xem [{n}]."} for i, n in _MUC.findall(chu_gui(kw))]
    return [cau_json(sua(items) if sua else items)]


def _sse(r):
    from test_chat_stream import parse_sse
    return parse_sse([f"{block}\n\n".encode() for block in r.text.strip("\n").split("\n\n")])


V2_FORM = {"so_ngay": "3", "nguoi_lon": 2, "kieu_di": "kham_pha", "so_thich": ["di_tich", "thien_nhien"]}


@pytest.mark.parametrize("path", ["/api/chat", "/api/chat/stream"])
def test_v2_turn_frame_first_then_sentences(app_client, caplog, path):
    app, client = app_client
    gen = generator(lambda n, kw: viet_dung(kw))
    original = _with(app, V2, gen)
    client.cookies.clear()
    typed = "chữ tự do lạ không được tới model"
    try:
        with chat_log_records(caplog) as records:
            r = client.post(path, json={"query": typed, "bieu_mau": True, "truong": V2_FORM})
    finally:
        _restore(app, original)
    (call,) = gen.client.responses.calls
    assert call["instructions"] == LICH_V2_LOI_DAN and not call.get("tools") and getattr(call.get("reasoning"), "effort", None) == "low"
    assert typed not in chu_gui(call)
    if path == "/api/chat":
        body = r.json()
        v2_ = body["lich_trinh"]
        answer_text = body["answer"]
    else:
        events = _sse(r)
        kinds = [k for k, _ in events]
        khung = next(d for k, d in events if k == "lich_khung")
        cau = [d for k, d in events if k == "lich_cau"]
        assert kinds.index("lich_khung") < kinds.index("lich_cau") and kinds.index("lich_xong") > max(i for i, k in enumerate(kinds) if k == "lich_cau")
        assert kinds.index("lich_xong") < kinds.index("delta") < kinds.index("sources") < kinds.index("lich_trinh") < kinds.index("done")
        assert [c["id_muc"] for c in cau] == [m["id_muc"] for m in v2.moi_muc(khung)]
        v2_ = next(d for k, d in events if k == "lich_trinh")
        assert v2_["lich"] == khung
        answer_text = "".join(d["text"] for k, d in events if k == "delta")
    lich = v2_["lich"]
    ids = [m["id_muc"] for m in v2.moi_muc(lich)]
    assert r.status_code == 200 and v2_["phien_ban"] == 2 and v2_["so_cau_du_phong"] == 0 and set(v2_["cau"]) == set(ids)
    assert len(lich["ngay"]) == 3 and lich["tham_so"]["kieu_di"] == "kham_pha" and lich["tham_so"]["so_thich"] == ["di_tich", "thien_nhien"]
    assert answer_text.startswith("Mình hiểu: 3 ngày · 2 người lớn · đi khám phá nhiều") and all(m["ten"] in answer_text for m in v2.moi_muc(lich))
    line = metric_lines(records)[-1]
    assert line["outcome"] == "success" and line["lich_trinh_ok"] is True and line["lich_v2"]["so_cau_du_phong"] == 0
    assert typed not in json.dumps(line, ensure_ascii=False)
    if path == "/api/chat/stream":
        assert line["lich_khung_ms"] <= line["lich_xong_ms"]


def test_v2_sentence_checks(app_client):
    """5c.6: thiếu ⇒ dự phòng · lặp ⇒ phần tử đầu · id lạ ⇒ bỏ · giờ / thời lượng / tiền / link / tên điểm khác / mã ngoài nguồn / không mã ⇒
    dự phòng riêng mục đó; câu đúng giữ nguyên."""
    b = V2.bang_lich_v2
    k = v2.xep_v2(b, v2.ThamSoV2(2, kieu_di="nhe_nhang", so_thich=("di_tich",)))
    lich = v2.dung_lich(b, k, {i: n for n, i in enumerate(v2.diem_v2(k), start=1)})
    m = [x for x in v2.moi_muc(lich) if x["loai"] == "tham_quan"]
    assert len(m) == 4
    khac = next(d["ten"] for d in b.diem if d["id"] not in v2.diem_v2(k) and not any(
        v2.chuan_ten(d["ten"]) in v2.chuan_ten(t) for x in v2.diem_v2(k) for t in v2.ten_cua(b.theo_id[x])))
    hong = {m[0]["id_muc"]: f"Mở cửa lúc 8:00 [{m[0]['nguon']}].", m[1]["id_muc"]: f"Vé 50.000 đồng [{m[1]['nguon']}].",
            m[2]["id_muc"]: f"Gần {khac} [{m[2]['nguon']}]."}
    for sai, ma in ((f"Nên ở đây 2 tiếng [{m[0]['nguon']}].", "gio"), (f"Xem tại https://x.vn [{m[0]['nguon']}].", "link"),
                    (f"Đẹp [{m[0]['nguon'] + 1}].", "ma_ngoai_nguon"), ("Đẹp lắm.", "khong_ma"), ("  ", "rong"),
                    (f"Tài liệu không cung cấp thông tin về điểm này; nội dung chỉ mô tả nơi khác. [{m[0]['nguon']}]", "noi_ve_tai_lieu")):
        assert v2.kiem_cau(b, m[0], sai) == ma
    for tot in ("Trưng bày nhiều tài liệu, hiện vật quý", "Xem văn bản cổ và châu bản"):  # m-3: câu tả bảo tàng không bị chặn nhầm
        assert v2.kiem_cau(b, m[0], f"{tot} [{m[0]['nguon']}].") != "noi_ve_tai_lieu"
    tu_model = [{"id_muc": i, "cau": c} for i, c in hong.items()] + [{"id_muc": m[0]["id_muc"], "cau": f"Câu sau bị bỏ [{m[0]['nguon']}]."},
                                                                     {"id_muc": "n9-sang-1", "cau": "id lạ [1]."}]
    cau, loi = v2.chon_cau(b, lich, tu_model)
    toi = [x["id_muc"] for x in v2.moi_muc(lich) if x["loai"] == "hoat_dong_toi"]
    assert loi == {m[0]["id_muc"]: "gio", m[1]["id_muc"]: "tien", m[2]["id_muc"]: "ten_khac", m[3]["id_muc"]: "thieu", **dict.fromkeys(toi, "thieu")}
    assert all(cau[x["id_muc"]] == v2.cau_du_phong(b, x) for x in m) and "n9-sang-1" not in cau
    tot = f"Ở đây có kiến trúc đẹp [{m[3]['nguon']}]."
    assert v2.chon_cau(b, lich, [{"id_muc": m[3]["id_muc"], "cau": tot}])[0][m[3]["id_muc"]] == tot


def test_v2_sub_name_inside_own_name_is_not_another_place(tmp_path):
    """Tên một điểm khác nằm trong chính tên điểm này (tên con trong điểm lớn) ⇒ không thay câu — ca plan (c) dặn đếm."""
    b = _bang(tmp_path, [_diem("lon", "kinh_thanh"), _diem("con", "kinh_thanh"), _diem("xa", "bo_nam")])
    b.theo_id["lon"]["ten"], b.theo_id["con"]["ten"], b.theo_id["xa"]["ten"] = "Kinh thành Huế (Ngọ Môn)", "Ngọ Môn", "Chợ Đông Ba"
    muc = {"id_diem": "lon", "nguon": 1, "ten": "Kinh thành Huế (Ngọ Môn)"}
    assert v2.kiem_cau(b, muc, "Đứng trước Ngọ Môn ngắm cổng [1].") is None
    assert v2.kiem_cau(b, muc, "Rồi ghé Chợ Đông Ba [1].") == "ten_khac"


@pytest.mark.parametrize("hong", ["sai_khuon", "loi_model"])
def test_v2_model_failure_keeps_full_frame(app_client, hong):
    """Model lỗi / sai khuôn ⇒ lịch vẫn đủ khung, mọi mục câu dự phòng, không rút cả lịch (5c.6), log ghi loại lỗi (không chữ)."""
    app, client = app_client

    def script(n, kw):
        if hong == "loi_model":
            import httpx
            from openai import APIConnectionError
            raise APIConnectionError(request=httpx.Request("POST", "https://api.openai.com/v1/responses"))  # lỗi nhà cung cấp như thật
        return [{"type": "message", "id": "msg_x", "role": "assistant", "status": "completed",
                 "content": [{"type": "output_text", "text": '{"answer": "không đúng khuôn"}', "annotations": []}]}]
    original = _with(app, V2, generator(script))
    client.cookies.clear()
    try:
        r = client.post("/api/chat/stream", json={"query": "x", "bieu_mau": True, "truong": {"so_ngay": "2"}})
    finally:
        _restore(app, original)
    events = _sse(r)
    khung = next(d for k, d in events if k == "lich_khung")
    n = len(v2.moi_muc(khung))
    assert n >= 2 and next(d for k, d in events if k == "lich_xong") == {"so_cau_du_phong": n}
    assert len([1 for k, _ in events if k == "lich_cau"]) == n and "error" not in [k for k, _ in events]
    assert next(d for k, d in events if k == "done")["outcome"] == "success"


def test_v2_old_values_and_long_limits(app_client):
    """Giá trị cũ (giao diện cũ trong bộ đệm) vẫn chạy ở bản 2; 5 ngày + 2 sở thích nhận được (bộ xếp mới)."""
    app, client = app_client
    out = []
    for truong in (OLD_SAME, {"so_ngay": "5", "so_thich": ["am_thuc", "chup_anh"], "kieu_di": "nhe_nhang"},
                   {"so_ngay": "1", "nguoi_lon": 4, "lon_tuoi": True, "kieu_di": "can_bang", "so_thich": []}):
        gen = generator(lambda n, kw: viet_dung(kw))
        original = _with(app, V2, gen)
        client.cookies.clear()
        try:
            out.append(client.post("/api/chat", json={"query": "x", "bieu_mau": True, "truong": truong}).json()["lich_trinh"]["lich"])
        finally:
            _restore(app, original)
    assert out[0]["tham_so"] | {"ngay_di": None} == {"so_ngay": 2, "nguoi_lon": 2, "tre_em": 1, "lon_tuoi": False, "kieu_di": "can_bang",
                                                    "so_thich": ["di_tich"], "ngay_di": None}
    assert len(out[1]["ngay"]) == 5 and out[1]["tham_so"]["so_thich"] == ["am_thuc", "chup_anh"]
    assert out[2]["tham_so"]["so_thich"] == [] and "so_thich" in [g["ma"] for g in out[2]["ghi_chu"]]  # [] = không chọn


def test_v2_plain_answer_is_built_from_frame():
    lich = {"minh_hieu": "Mình hiểu: x", "ngay": [{"ngay": 1, "muc": [{"id_muc": "n1-sang-1", "buoi": "sang", "loai": "tham_quan", "ten": "A", "gio": None},
                                                                      {"id_muc": "n1-chieu-1", "buoi": "chieu", "loai": "tham_quan", "ten": "B",
                                                                       "gio": "13:30 – 14:45"},
                                                                      {"id_muc": "n1-toi-1", "buoi": "toi", "loai": "nghi", "ten": "Tối nghỉ.", "gio": None}]}],
            "ghi_chu": [{"ma": "kieu_di", "cau": "Chưa chọn kiểu đi."}]}
    assert v2.ghep_chu(lich, {"n1-sang-1": "câu a [1].", "n1-chieu-1": "câu b [2]."}) == (
        "Mình hiểu: x\n\n**Ngày 1**\n- Sáng: A — câu a [1].\n- Chiều (13:30 – 14:45): B — câu b [2].\n- Tối: Tối nghỉ.\n\n**Ghi chú của lịch**\n- Chưa chọn kiểu đi.")


def test_cau_stream_emits_each_closed_item():
    s = v2.CauStream()
    raw = json.dumps({"cau": [{"id_muc": "n1-sang-1", "cau": "a {b} \"c\" [1]."}, {"id_muc": "n1-chieu-1", "cau": "d [2]."}]}, ensure_ascii=False)
    out = [x for i in range(0, len(raw), 5) for x in s.feed(raw[i:i + 5])]
    assert out == json.loads(raw)["cau"]


# =====================================================================================================================================
# Bước (d): ngày đi — thứ, mùa, dự báo (plan §3 (d), spec 5c.2) — ngày cố định, dự báo ghi sẵn, 0 USD, không mạng
# =====================================================================================================================================

from llm import len_ke_hoach as lkh  # noqa: E402
from llm import thoi_tiet as tt  # noqa: E402

D = dt.date


def _mua_luu_y(thang):
    return {"thang": list(thang), "cau": "x", "bo_khoi_lich": True}


def test_rule_season_closure_beats_priority_by_day(tmp_path):
    """5c.2 (i): điểm tạm dừng theo mùa không xếp đúng NGÀY rơi vào tháng dừng, kể cả điểm ưu tiên ⇒ ghi chú; lịch vắt hai tháng xét từng ngày."""
    b = _bang(tmp_path, [dict(_diem("thac", "bo_nam", loai=("thien_nhien",)), mua_luu_y=_mua_luu_y((9, 10, 11, 12, 1, 2))),
                         *[_diem(f"t{i}", "bo_nam", loai=("thien_nhien",)) for i in range(6)]], {"chung": ["t0"], "thien_nhien": ["thac", "t0"]})
    s = ("thien_nhien",)
    dong = v2.xep_v2(b, ts(1, kieu_di="nhe_nhang", so_thich=s), ngay_bat_dau=D(2026, 12, 20))
    assert "thac" not in v2.diem_v2(dong) and dong["tam_dung_mua"] == ["thac"] and v2.kiem_khung_v2(b, dong) == []
    mo = v2.xep_v2(b, ts(1, kieu_di="nhe_nhang", so_thich=s), ngay_bat_dau=D(2027, 3, 1))
    assert v2.diem_v2(mo)[0] == "thac" and mo["tam_dung_mua"] == []
    vat = v2.xep_v2(b, ts(3, kieu_di="nhe_nhang", so_thich=s), ngay_bat_dau=D(2027, 2, 27))  # 27/2, 28/2 dừng · 1/3 mở
    assert [("thac" in v2.diem_v2({"ngay": [ng]})) for ng in vat["ngay"]] == [False, False, True] and v2.kiem_khung_v2(b, vat) == []
    assert v2.diem_v2(v2.xep_v2(b, ts(1, kieu_di="nhe_nhang", so_thich=s)))[0] == "thac"  # không ngày đi ⇒ luật mùa không áp (không đoán tháng)
    assert "tam_dung_mua" in v2.kiem_khung_v2(b, dict(dong, ngay=[{"ngay": 1, "buoi": {"sang": ["thac"], "chieu": [], "toi": []}}]))


def test_rule_weekday_only_points(tmp_path):
    b = _bang(tmp_path, [dict(_diem("thu7", "kinh_thanh"), ngay_hoat_dong=[5]), _diem("a", "kinh_thanh"), _diem("c", "kinh_thanh")],
              {"chung": ["thu7", "a"], "di_tich": ["thu7", "a"]})
    sat, sun = D(2026, 11, 21), D(2026, 11, 22)
    assert sat.weekday() == 5 and "thu7" in v2.diem_v2(v2.xep_v2(b, ts(1, kieu_di="nhe_nhang"), ngay_bat_dau=sat))
    assert "thu7" not in v2.diem_v2(v2.xep_v2(b, ts(1, kieu_di="nhe_nhang"), ngay_bat_dau=sun))
    assert "thu7" not in v2.diem_v2(v2.xep_v2(b, ts(1, kieu_di="nhe_nhang")))  # không biết thứ ⇒ không xếp điểm chỉ mở vài ngày


def test_rule_rain_day_prefers_indoor_but_keeps_priority(tmp_path):
    """5c.2: ngày mưa (≥ 60 %) ⇒ điểm không ưu tiên xét trong nhà ⇒ cả hai ⇒ ngoài trời; điểm ưu tiên giữ chỗ (+ dòng "nếu mưa")."""
    rows = [_diem("uu", "bo_nam"), _diem("ngoai", "bo_nam"), dict(_diem("ca", "bo_nam"), trong_nha="ca_hai"), dict(_diem("trong", "bo_nam"), trong_nha="trong_nha")]
    b = _bang(tmp_path, rows, {"chung": ["uu"], "di_tich": ["uu"]})
    hom = D(2026, 11, 13)
    kho = v2.xep_v2(b, ts(1, kieu_di="nhe_nhang", so_thich=("di_tich",)), ngay_bat_dau=hom, mua={hom: 20})
    ua = v2.xep_v2(b, ts(1, kieu_di="nhe_nhang", so_thich=("di_tich",)), ngay_bat_dau=hom, mua={hom: 60})
    assert v2.diem_v2(kho) == ["uu", "ngoai"] and v2.diem_v2(ua) == ["uu", "trong"]
    db = {"ngay": {hom: {"ngay": hom, "tmax": 25, "tmin": 20, "xs": 60, "mua": 5.0}}, "nguon": "nguồn"}
    dong = [x["cau"] for x in lkh.dong_du_bao(b, ua, db)]
    assert dong[0].startswith("Ngày 1 — ") and dong[1] == "Nếu mưa ngày 1: có thể thay uu bằng ca (trong nhà)." and dong[-1] == "nguồn"
    assert lkh.dong_du_bao(b, ua, None) == []
    # ngày mưa không có điểm ngoài trời / ngoài trời không có điểm thay ⇒ vẫn đúng một dòng (review 14/11)
    ng = {"ngay": 1, "buoi": {"sang": ["trong"], "chieu": [], "toi": []}}
    assert lkh.dong_neu_mua(b, ua, ng).startswith("Nếu mưa ngày 1: các điểm trong ngày đều trong nhà")
    chi_ngoai = _bang(tmp_path, [_diem("ngoai", "bo_nam")], {"chung": ["ngoai"]}, ten="c.json")
    k1 = {"ngay": [{"ngay": 1, "buoi": {"sang": ["ngoai"], "chieu": [], "toi": []}}]}
    assert lkh.dong_neu_mua(chi_ngoai, k1, k1["ngay"][0]).startswith("Nếu mưa ngày 1: ngoai ở ngoài trời")


@pytest.mark.parametrize("kich_ban", ["khong_mua", "mua_ngay_1", "mua_moi_ngay"])
def test_forecast_scenarios_and_no_call_outside_7_days(kich_ban):
    """Ba kịch bản dự báo ghi sẵn (cách đo của E): chỉ ngày mưa đổi thứ tự xét; ngày ngoài 7 ngày ⇒ 0 lần gọi, 0 dòng dự báo; lỗi ⇒ như không có."""
    hom = D(2026, 11, 13)
    xs = {"khong_mua": [10] * 7, "mua_ngay_1": [80] + [10] * 6, "mua_moi_ngay": [80] * 7}[kich_ban]
    goi = []

    async def du_bao():
        goi.append(1)
        return tt.DuBao(trang_thai="ok", ngay=[{"ngay": hom + dt.timedelta(days=k), "tmax": 25, "tmin": 20, "xs": x, "mua": 1.0}
                                               for k, x in enumerate(xs)], cap_nhat="09:00 13/11")
    flags = dataclasses.replace(V2, thoi_tiet=True, du_bao=du_bao)
    trace = AnswerTrace()
    db = asyncio.run(lkh.du_bao_lich(flags, hom, 3, trace, hom))
    assert len(goi) == 1 and db is not None and trace.tools[-1]["name"] == "thoi_tiet"
    b = V2.bang_lich_v2
    k = v2.xep_v2(b, v2.ThamSoV2(3, so_thich=("di_tich",)), ngay_bat_dau=hom, mua={d: v["xs"] for d, v in db["ngay"].items()})
    assert v2.kiem_khung_v2(b, k) == []
    dong = [x["cau"] for x in lkh.dong_du_bao(b, k, db)]
    assert sum(x.startswith("Ngày ") for x in dong) == 3 and dong[-1].startswith(tt.GHI_CONG)
    so_ngay_mua = sum(x >= v2.NGUONG_MUA for x in xs[:3])  # thước ý 6: mỗi ngày mưa đúng một dòng "Nếu mưa", kể cả khi không có điểm để thay
    assert [x.split(":")[0] for x in dong if x.startswith("Nếu mưa")] == [f"Nếu mưa ngày {i}" for i in range(1, 4) if xs[i - 1] >= v2.NGUONG_MUA]
    assert sum(x.startswith("Nếu mưa") for x in dong) == so_ngay_mua
    # giao diện mới: mỗi dòng theo ngày mang đúng `ngay`; dòng nguồn không có
    goc = lkh.dong_du_bao(b, k, db)
    assert all(x["ngay"] == int(x["cau"].split(":")[0].split()[-1]) for x in goc if x["cau"].startswith("Nếu mưa"))
    assert all(x["ngay"] == int(x["cau"].split()[1]) for x in goc if x["cau"].startswith("Ngày ")) and "ngay" not in goc[-1]
    lich = v2.dung_lich(b, k, {i: n for n, i in enumerate(v2.diem_v2(k), start=1)}, hom.isoformat(), goc)
    assert [g for g in lich["ghi_chu"] if g["ma"] == "du_bao"] == [{"ma": "du_bao", **x} for x in goc]
    assert asyncio.run(lkh.du_bao_lich(flags, hom + dt.timedelta(days=7), 5, AnswerTrace(), hom)) is None and len(goi) == 1
    assert asyncio.run(lkh.du_bao_lich(flags, None, 5, AnswerTrace(), hom)) is None and len(goi) == 1

    async def loi():
        return tt.DuBao(trang_thai="loi", loi="http_500")
    assert asyncio.run(lkh.du_bao_lich(dataclasses.replace(flags, du_bao=loi), hom, 3, AnswerTrace(), hom)) is None


KIEU_NGAY = {"khong": (None, None), "kho_giua_tuan": (D(2027, 4, 7), None), "mua_cuoi_tuan": (D(2026, 11, 21), None),
             "trong_7_ngay_mua": (D(2026, 11, 13), "mua")}


@pytest.fixture(scope="module")
def mo_phong_ngay():
    b = V2.bang_lich_v2
    kq = {}
    for key in itertools.product(range(1, 6), (0, 1), (False, True), KIEU, ST_16, KIEU_NGAY):
        bat_dau, mua = KIEU_NGAY[key[5]]
        mua = None if mua is None else {bat_dau + dt.timedelta(days=k): 80 for k in range(7)}
        kq[key] = v2.xep_v2(b, v2.ThamSoV2(*key[:4], so_thich=key[4]), ngay_bat_dau=bat_dau, mua=mua)
    assert len(kq) == 3840
    return b, kq


def test_simulation_dates_always_rules(mo_phong_ngay):
    b, kq = mo_phong_ngay
    T = b.theo_id
    assert {key: v2.kiem_khung_v2(b, k) for key, k in kq.items() if v2.kiem_khung_v2(b, k)} == {}  # gồm 0 điểm tạm dừng trong tháng dừng
    for key, k in kq.items():
        bat_dau = KIEU_NGAY[key[5]][0]
        thang = {(bat_dau + dt.timedelta(days=i)).month for i in range(key[0])} if bat_dau else set()
        assert k["mua_mua"] == bool(thang & {9, 10, 11, 12})  # đúng một dòng nhắc khi có ngày tháng 9–12 (dòng dựng ở `dung_lich`)
        lich = v2.dung_lich(b, k, dict.fromkeys(v2.diem_v2(k), 1))
        assert sum(g["ma"] == "mua_mua" for g in lich["ghi_chu"]) == (1 if k["mua_mua"] else 0)
        for s in key[4] or ("chung",):  # ưu tiên số 1 có mặt — trừ cụm xa < 3 ngày và điểm đang tạm dừng (có ghi chú)
            dau = next(i for i in b.uu_tien[s] if T[i]["cum"] != v2.CUM_XA or key[0] >= 3)
            assert dau in v2.diem_v2(k) or dau in k["tam_dung_mua"], (key, s)


def test_simulation_dates_floor(mo_phong_ngay):
    """Sàn (plan (d)): đổi "mùa khô, giữa tuần" ↔ "mùa mưa, cuối tuần" ⇒ khung hoặc ghi chú khác ở ≥ 60 % tổ hợp có điểm ngoài trời."""
    b, kq = mo_phong_ngay
    T = b.theo_id
    cap = [(k, kq[key[:5] + ("mua_cuoi_tuan",)]) for key, k in kq.items() if key[5] == "kho_giua_tuan"
           and any(T[i]["trong_nha"] != "trong_nha" for i in v2.diem_v2(k))]
    khac = sum(a["ngay"] != c["ngay"] or a["mua_mua"] != c["mua_mua"] or a["tam_dung_mua"] != c["tam_dung_mua"] for a, c in cap)
    assert khac / len(cap) >= 0.60


# =====================================================================================================================================
# Bước (e): giờ gợi ý + buổi tối (plan §3 (e), spec 5c.3 / 5c.4) — 0 USD
# =====================================================================================================================================

def _gio(k, *ids):
    return [k["gio"][i] for i in ids]


def test_time_table_cases(tmp_path):
    """5c.3: bảng ca giờ — mọi số là bội 15 phút; điểm sau = điểm trước + phút đi; mở muộn ⇒ dời buổi; vượt giờ đóng ⇒ không xếp."""
    b = _bang(tmp_path, [_diem("a", "kinh_thanh"), _diem("b", "kinh_thanh"), _diem("c", "kinh_thanh"), _diem("d", "kinh_thanh")])
    k = v2.xep_v2(b, ts(1, kieu_di="can_bang"))
    assert _gio(k, "a", "c", "b", "d") == ["8:00 – 9:15", "9:30 – 10:45", "13:30 – 14:45", "15:00 – 16:15"]  # 2 ngắn cùng cụm
    b = _bang(tmp_path, [_diem("a", "kinh_thanh"), _diem("x", "bo_nam"), _diem("y", "bo_nam")])
    k = v2.xep_v2(b, ts(1, kieu_di="can_bang"))
    assert k["ngay"][0]["buoi"]["sang"] == ["a", "y"] and _gio(k, "a", "y") == ["8:00 – 9:15", "9:45 – 11:00"]  # cụm kề: 30 phút đi
    b = _bang(tmp_path, [_diem("h", "kinh_thanh", thoi_luong="nua_buoi"), _diem("c", "kinh_thanh"), _diem("n", "kinh_thanh")])
    k = v2.xep_v2(b, ts(1, kieu_di="kham_pha"))
    assert _gio(k, "h", "n", "c") == ["7:30 – 10:00", "10:15 – 11:30", "13:00 – 14:15"]  # nửa buổi + ngắn; khám phá nhiều bắt đầu 7:30 / 13:00
    b = _bang(tmp_path, [dict(_diem("muon", "kinh_thanh"), gio_mo=[["09:00", "17:00"]]), dict(_diem("som", "kinh_thanh"), gio_mo=[["07:00", "09:00"]]),
                         _diem("z", "kinh_thanh")], {"chung": ["muon", "som"], "di_tich": ["muon", "som"]})
    k = v2.xep_v2(b, ts(1, kieu_di="nhe_nhang", so_thich=("di_tich",)))
    assert k["ngay"][0]["buoi"]["sang"] == ["muon"] and _gio(k, "muon") == ["9:00 – 10:15"]  # mở muộn ⇒ dời cả buổi
    assert "som" not in v2.diem_v2(k) and v2.kiem_khung_v2(b, k) == []  # 8:00 + 75 phút > đóng 9:00 ⇒ không xếp (chọn điểm khác)
    bad = copy.deepcopy(k)
    bad["gio"]["muon"] = "8:00 – 9:15"
    assert "ngoai_gio_mo" in v2.kiem_khung_v2(b, bad)
    bad["gio"]["muon"] = "13:30 – 14:30"
    assert "ngoai_gio_mo" in v2.kiem_khung_v2(b, bad)  # sai thời lượng


def _bang_toi(tmp_path):
    return _bang(tmp_path, [*[_diem(f"d{i}", "kinh_thanh") for i in range(10)], _diem("xa", "nam_xa"), _diem("xa2", "nam_xa"),
                            dict(_diem("pho", "bo_nam", buoi=("toi",)), gio_toi="18:00 – 22:00"),
                            dict(_diem("cuoi_tuan", "bo_nam", buoi=("toi",)), ngay_hoat_dong=[4, 5, 6], gio_toi="19:30 – 22:30"),
                            dict(_diem("ngoai_tt", "thuy_xuan", buoi=("toi",)), gio_toi="19:00 – 20:00")],
                 {"chung": ["d0", "xa"], "di_tich": ["d0", "xa"]})


def test_evening_weekday_center_and_far_days(tmp_path):
    b = _bang_toi(tmp_path)
    for thu in range(7):
        bat_dau = D(2026, 11, 16) + dt.timedelta(days=thu)  # 16/11/2026 là thứ Hai
        for n in range(1, 6):
            k = v2.xep_v2(b, ts(n, kieu_di="nhe_nhang"), ngay_bat_dau=bat_dau)
            assert v2.kiem_khung_v2(b, k) == []
            for ng, ngay in zip(k["ngay"], k["ngay_thang"]):
                toi = ng["buoi"]["toi"]
                assert "ngoai_tt" not in toi  # chỉ hai cụm trung tâm
                if "cuoi_tuan" in toi:
                    assert D.fromisoformat(ngay).weekday() in (4, 5, 6)
                co_xa = any(b.theo_id[j]["cum"] == "nam_xa" for x in ("sang", "chieu") for j in ng["buoi"][x])
                assert (not toi and k["toi_nghi"][ng["ngay"]] == "xa") if co_xa else bool(toi)
    k = v2.xep_v2(b, ts(3, kieu_di="nhe_nhang"))  # không ngày đi ⇒ chỉ hoạt động diễn mọi tối; hết ⇒ lặp, có nhãn
    lich = v2.dung_lich(b, k, dict.fromkeys(v2.diem_v2(k), 1))
    toi = [m for ng in lich["ngay"] for m in ng["muc"] if m["loai"] == "hoat_dong_toi"]
    assert {m["id_diem"] for m in toi} == {"pho"} and [("co_the_di_lai" in m["nhan"]) for m in toi] == [False] + [True] * (len(toi) - 1)
    assert toi[0]["gio"] == "18:00 – 22:00"
    for te, lt_, ma in ((1, False, "tre_em"), (0, True, "lon_tuoi")):
        k = v2.xep_v2(b, ts(2, tre_em=te, lon_tuoi=lt_))
        assert all(not ng["buoi"]["toi"] for ng in k["ngay"]) and set(k["toi_nghi"].values()) == {ma}
        nghi = [m for ng in v2.dung_lich(b, k, dict.fromkeys(v2.diem_v2(k), 1))["ngay"] for m in ng["muc"] if m["loai"] == "nghi"]
        assert len(nghi) == 2 and nghi[0]["ten"] == v2.CAU_TOI[ma]


def test_simulation_evening_floor_and_times(mo_phong_ngay):
    """Sàn (e): ≥ 80 % số tối (không tính ngày cụm xa) của lịch nhóm không hạn chế có hoạt động. Luôn: giờ trong giờ mở cửa, tăng dần (kiểm
    ở `kiem_khung_v2` — 0 lỗi trên 3.840 khung ở test ngày đi); nhóm có trẻ em ⇒ 0 mục buổi tối."""
    b, kq = mo_phong_ngay
    T = b.theo_id
    toi = co = 0
    for key, k in kq.items():
        if key[1] or key[2]:
            assert all(not ng["buoi"]["toi"] for ng in k["ngay"])
            continue
        for ng in k["ngay"]:
            if any(T[j]["cum"] == v2.CUM_XA for x in v2.BUOI_NGAY for j in ng["buoi"][x]):
                continue
            toi += 1
            co += bool(ng["buoi"]["toi"])
    assert co / toi >= 0.80


def test_notes_required_by_scoring_definition():
    """Định nghĩa chấm của E (`dinh_nghia_cham.md`): ý 2 nhóm hạn chế + điểm nhiều bậc thang còn trong lịch ⇒ dòng ghi chú; ý 3 nhóm hạn chế ⇒
    luôn có dòng "giữ mức nhẹ nhàng"; ý 5 không có ngày đi ⇒ hoạt động tối có nhãn "kiểm lịch diễn" (chữ thuần cũng có)."""
    b = V2.bang_lich_v2
    for n, te, lt_ in itertools.product(range(1, 6), (0, 1), (False, True)):
        if not (te or lt_):
            continue
        k = v2.xep_v2(b, v2.ThamSoV2(n, te, lt_, "nhe_nhang", ("di_tich",)))
        lich = v2.dung_lich(b, k, dict.fromkeys(v2.diem_v2(k), 1))
        ma = [g["ma"] for g in lich["ghi_chu"]]
        assert "han_che" in ma
        bt = {j for j in v2.diem_ban_ngay(k) if b.theo_id[j]["bac_thang"] == "nhieu"}
        assert ma.count("bac_thang") == len(bt)
    # không ngày đi ⇒ nhãn "kiểm lịch diễn" CHỈ cho điểm tối có suất diễn (lượt thật 14/11: chợ / phố đêm bị gắn nhãn này)
    thay = {True: 0, False: 0}
    for n, st in itertools.product(range(2, 6), [(), ("am_thuc",), ("le_hoi_nghe_thuat",), ("le_hoi_nghe_thuat", "am_thuc")]):
        lich = v2.dung_lich(b, (k := v2.xep_v2(b, v2.ThamSoV2(n, kieu_di="can_bang", so_thich=st))), dict.fromkeys(v2.diem_v2(k), 1))
        for m in (m for ng in lich["ngay"] for m in ng["muc"] if m["loai"] == "hoat_dong_toi"):
            dien = v2.co_suat_dien(b.theo_id[m["id_diem"]])
            assert ("kiem_lich_dien" in m["nhan"]) == dien
            thay[dien] += 1
            if dien:
                assert "(kiểm lịch diễn trước khi đi)" in v2.ghep_chu(lich, {x["id_muc"]: "x [1]." for x in v2.moi_muc(lich)})
    assert thay[True] and thay[False]  # bộ thử có cả điểm diễn lẫn chợ / phố đêm
    k = v2.xep_v2(b, v2.ThamSoV2(2, kieu_di="can_bang"), ngay_bat_dau=D(2026, 11, 21))
    lich = v2.dung_lich(b, k, dict.fromkeys(v2.diem_v2(k), 1))
    assert not any("kiem_lich_dien" in m["nhan"] for ng in lich["ngay"] for m in ng["muc"])


def test_daytime_closed_weekday(tmp_path):
    """Điểm ban ngày đóng một thứ (cột `dong_cua_thu`): biết ngày ⇒ không xếp ngày đó (kiểm cũng bắt); không ngày ⇒ vẫn xếp."""
    b = _bang(tmp_path, [dict(_diem("bt", "kinh_thanh"), dong_cua_thu=[0]), _diem("a", "kinh_thanh"), _diem("c", "kinh_thanh")],
              {"chung": ["bt", "a"], "di_tich": ["bt", "a"]})
    thu2, thu3 = D(2026, 11, 16), D(2026, 11, 17)
    assert "bt" not in v2.diem_v2(v2.xep_v2(b, ts(1, kieu_di="nhe_nhang"), ngay_bat_dau=thu2))
    k = v2.xep_v2(b, ts(1, kieu_di="nhe_nhang"), ngay_bat_dau=thu3)
    assert v2.diem_v2(k)[0] == "bt" and v2.diem_v2(v2.xep_v2(b, ts(1, kieu_di="nhe_nhang")))[0] == "bt"
    assert "sai_thu" in v2.kiem_khung_v2(b, dict(k, ngay_thang=[thu2.isoformat()]))
    assert V2.bang_lich_v2.theo_id["kg_le_ba_dang"]["dong_cua_thu"] == [0]


# =====================================================================================================================================
# Cột "đoạn mô tả" chọn sẵn (vòng sửa bằng dữ liệu, User duyệt 13/11) — đọc Qdrant thật, 0 USD
# =====================================================================================================================================

def test_lay_doan_by_chunk_id(deps):
    service, _ = deps
    some = service.search("Đại Nội Huế").documents[:2]
    got = service.lay_doan([d.id for d in some] + ["khong/co.md#1"])
    assert set(got) == {d.id for d in some} and all(got[d.id].text == d.text and got[d.id].metadata["source"] == d.metadata["source"] for d in some)
    assert service.lay_doan([]) == {}


def test_doan_mo_ta_table_and_startup_checks(tmp_path, deps):
    service, _ = deps
    with pytest.raises(ValueError, match="doan_mo_ta"):
        _bang(tmp_path, [dict(_diem("a", "kinh_thanh"), doan_mo_ta="file/khac.md#3")])  # phải là đoạn của chính file nguồn
    that = service.search("Đại Nội Huế").documents[0]
    ok = _bang(tmp_path, [dict(_diem("a", "kinh_thanh"), nguon=that.metadata["source"], doan_mo_ta=that.id), _diem("b", "kinh_thanh")])
    v2.kiem_doan_mo_ta(ok, service.lay_doan)  # có trong chỉ mục ⇒ không lỗi
    thieu = _bang(tmp_path, [dict(_diem("a", "kinh_thanh"), nguon=that.metadata["source"], doan_mo_ta=that.metadata["source"] + "#99999")])
    with pytest.raises(ValueError, match="1 doan_mo_ta không có trong chỉ mục"):
        v2.kiem_doan_mo_ta(thieu, service.lay_doan)


def test_v2_turn_uses_chosen_passage(deps, tmp_path):
    """Điểm có `doan_mo_ta` ⇒ lịch dùng đúng đoạn đó (vào sổ nguồn, mã [n] của mục trỏ tới nó); điểm khác ⇒ luật tìm như trước."""
    service, cb = deps
    b = V2.bang_lich_v2
    truong = {"so_ngay": "1", "kieu_di": "nhe_nhang", "so_thich": ["di_tich"]}
    dau = v2.diem_ban_ngay(v2.xep_v2(b, v2.tu_truong(truong)))[0]
    d = b.theo_id[dau]
    chon = [x for x in service.search(d["ten"] + " lịch sử").documents if x.metadata["source"] == d["nguon"]][-1]
    rows = json.loads(Path(V2_BANG_PATH).read_text(encoding="utf-8"))
    for r in rows["diem"]:
        if r["id"] == dau:
            r["doan_mo_ta"] = chon.id
    p = tmp_path / "v8_chon.json"
    p.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    trace = AnswerTrace(truong=dict(truong), bieu_mau=True, search_query="x")
    asyncio.run(lkh.chuan_bi("x", service, cb, trace, dataclasses.replace(V2, bang_lich_v2=v2.nap_bang_v2(p)), None))
    muc = next(m for m in v2.moi_muc(trace.lich_v2["lich"]) if m["id_diem"] == dau)
    assert trace.seen_ids[muc["nguon"] - 1] == chon.id  # mã [n] của mục trỏ đúng đoạn chọn sẵn


# =====================================================================================================================================
# Đợt 2 phần (A): bản đồ trong lịch bản 2 (plan `2026-11-13-len-ke-hoach-dot-2-plan.md` bước A1) — 0 USD
# =====================================================================================================================================

V2_BD = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, ban_do_lich=True, anh_lich=False)


def test_map_table_coverage_floor():
    """Sàn A: điểm của bảng v8 thiếu toạ độ ≤ 3 (mỗi điểm có lý do ở biên bản A0 của C); bảng toạ độ nạp theo bảng v8 khi cờ bản 2 bật."""
    ids = set(V2_BD.bang_lich_v2.theo_id)
    assert set(V2_BD.toa_do_lich) <= ids and 0 < len(ids - set(V2_BD.toa_do_lich)) <= 3  # có điểm null ⇒ đường "chưa có trên bản đồ" được thử
    assert V2.toa_do_lich is None or not V2.ban_do_lich  # cờ bản đồ tắt ⇒ không nạp


def test_map_always_rules_on_960_frames(mo_phong):
    """Luôn: mọi toạ độ = đúng dòng bảng theo id_diem; mục thiếu ⇒ null (không ghim đoán); mục "nghỉ" không toạ độ; cờ tắt ⇒ `lich` giống hệt đợt 1;
    toạ độ không vào tin nhắn gửi model."""
    b, kq = mo_phong
    td = V2_BD.toa_do_lich
    for k in kq.values():
        nguon = dict.fromkeys(v2.diem_v2(k), 1)
        tat, bat = v2.dung_lich(b, k, nguon), v2.dung_lich(b, k, nguon, toa_do=td)
        assert all(m["toa_do"] is None for ng in tat["ngay"] for m in ng["muc"])
        for ng_t, ng_b in zip(tat["ngay"], bat["ngay"]):
            for mt, mb in zip(ng_t["muc"], ng_b["muc"]):
                assert {**mb, "toa_do": None} == mt  # chỉ khác trường toạ độ
                assert mb["toa_do"] == (list(td[mb["id_diem"]]) if mb["id_diem"] in td else None)
        assert v2.tin_nhan_model(tat, "tl") == v2.tin_nhan_model(bat, "tl")


def test_map_flag_on_turn_sends_same_model_text(app_client):
    app, client = app_client
    sent = {}
    for name, flags in (("tat", V2), ("bat", V2_BD)):
        gen = generator(lambda n, kw: viet_dung(kw))
        original = _with(app, flags, gen)
        client.cookies.clear()
        try:
            body = client.post("/api/chat", json={"query": "x", "bieu_mau": True, "truong": {"so_ngay": "2", "kieu_di": "can_bang"}}).json()
        finally:
            _restore(app, original)
        (call,) = gen.client.responses.calls
        sent[name] = (call["instructions"], chu_gui(call), body["lich_trinh"]["lich"])
    assert sent["tat"][:2] == sent["bat"][:2]
    muc = [m for ng in sent["bat"][2]["ngay"] for m in ng["muc"] if m["loai"] != "nghi"]
    assert any(m["toa_do"] for m in muc) and all(m["toa_do"] is None for ng in sent["tat"][2]["ngay"] for m in ng["muc"])


def test_v2_travel_minutes_only_between_items_of_the_same_daytime_slot():
    """Giao diện mới 14/11: `phut_di` = số bộ xếp đã dùng để giãn giờ giữa hai điểm liền nhau trong cùng buổi; mục đầu buổi / tối ⇒ không
    có trường; chuỗi gửi model và chữ ghép không đổi (trường mới chỉ cho giao diện)."""
    b = V2.bang_lich_v2
    k = v2.xep_v2(b, v2.ThamSoV2(3, kieu_di="kham_pha", so_thich=("di_tich",)))
    lich = v2.dung_lich(b, k, {i: n for n, i in enumerate(v2.diem_v2(k), start=1)})
    co = 0
    for ng in lich["ngay"]:
        for a, c in zip([None, *ng["muc"]], ng["muc"]):
            dau_buoi = a is None or a["buoi"] != c["buoi"] or c["buoi"] == "toi"
            if dau_buoi:
                assert "phut_di" not in c
            elif "phut_di" in c:
                co += 1
                assert c["phut_di"] in (v2.DI_CUNG_CUM, v2.DI_CUM_KE)
                assert v2.ra_phut(c["gio"].split("–")[0].strip()) >= v2.ra_phut(a["gio"].split("–")[1].strip()) + c["phut_di"]
    assert co > 0
    tin = v2.tin_nhan_model(lich, "tài liệu")
    assert "phut_di" not in tin and "ngay\"" not in tin
    assert "phut_di" not in v2.ghep_chu(lich, {m["id_muc"]: "x" for m in v2.moi_muc(lich)})


# ---------- Đợt 2 (B): ảnh từng điểm (cờ `anh_lich`) ----------

BANG_ANH = Path(__file__).resolve().parents[2] / "data" / "phase_9" / "lich_trinh" / "bang_anh_v1.json"


def test_photo_table_loads_and_maps_by_point_id():
    """Bảng ảnh thật (B0 của C): ≥ 24 / 34 điểm (sàn plan) · mỗi ảnh đúng `id_diem`, `src` dưới /anh/lich/ + file có thật, đủ ghi công. Cờ bật ⇒
    mục có ảnh khi điểm có dòng, không ảnh thay; cờ tắt ⇒ mọi `anh` null; chuỗi gửi model không đổi."""
    b = V2.bang_lich_v2
    assert BANG_ANH.is_file(), f"thiếu bảng ảnh private: {BANG_ANH} (clone không có data/ ⇒ test này không chạy được — đúng thiết kế)"
    anh = v2.nap_bang_anh(BANG_ANH, b)
    assert len(anh) >= 24 and all(a["src"] == f"/anh/lich/{i}.jpg" for i, a in anh.items())
    assert any("cắt" in a.get("doi", "") for a in anh.values())  # review C m-1: ảnh có chỉnh khác thu nhỏ mang `doi` tới giao diện
    k = v2.xep_v2(b, v2.ThamSoV2(3, kieu_di="kham_pha", so_thich=("di_tich",)))
    nguon = {i: n for n, i in enumerate(v2.diem_v2(k), start=1)}
    tat, bat = v2.dung_lich(b, k, nguon), v2.dung_lich(b, k, nguon, anh=anh)
    muc = [m for ng in bat["ngay"] for m in ng["muc"] if m["id_diem"]]
    assert all(m["anh"] == (anh.get(m["id_diem"])) for m in muc) and any(m["anh"] for m in muc)
    assert all(m["anh"] is None for ng in tat["ngay"] for m in ng["muc"])
    assert v2.tin_nhan_model(tat, "x") == v2.tin_nhan_model(bat, "x")


def test_photo_table_rejects_bad_rows(tmp_path):
    b = V2.bang_lich_v2
    goc = json.loads(BANG_ANH.read_text(encoding="utf-8"))["anh"][0]

    def nap(**doi):
        p = tmp_path / "a.json"
        p.write_text(json.dumps({"anh": [{**goc, **doi}]}), encoding="utf-8")
        return v2.nap_bang_anh(p, b)
    assert nap()  # dòng thật hợp lệ
    for doi in ({"id_diem": "khong_co"}, {"src": "https://x.vn/a.jpg"}, {"src": "/anh/lich/../anh.jpg"}, {"src": "/anh/lich/khong_co.jpg"},
                {"tac_gia": ""}, {"giay_phep": None}, {"trang": "https://example.com/a"}):
        with pytest.raises(ValueError):
            nap(**doi)


def test_photo_flag_needs_v2_and_table():
    with pytest.raises(ValueError):
        AssistantFlags(anh_lich=True)
    with pytest.raises(ValueError):
        dataclasses.replace(V2, anh_lich=True)  # thiếu bảng ảnh
    assert dataclasses.replace(V2, anh_lich=True, anh_lich_bang=v2.nap_bang_anh(BANG_ANH, V2.bang_lich_v2)).anh_lich


def test_sample_itinerary_is_built_by_the_real_scheduler_without_model():
    """Lịch mẫu "Ví dụ" (trang Lên kế hoạch lúc chưa xếp, User 14/11): đúng khung `xep_v2` của tổ hợp cố định — không viết tay, không gọi model,
    không nguồn, không câu tả; mỗi ngày có tên chặng, mỗi mục có loại điểm; khung qua kiểm của bộ xếp."""
    from api.routes import cong
    kq = cong.dung_lich_mau(V2)
    lich, cau = kq["lich"], kq["cau"]
    khung = v2.xep_v2(V2.bang_lich_v2, v2.tu_truong(cong.TRUONG_MAU))
    assert [[m["id_diem"] for m in ng["muc"] if m["id_diem"]] for ng in lich["ngay"]] == [
        [j for b in v2.BUOI for j in ng["buoi"][b]] for ng in khung["ngay"]]
    assert len(lich["ngay"]) == 2 and lich["tham_so"]["ngay_di"] is None and v2.kiem_khung_v2(V2.bang_lich_v2, khung) == []
    assert set(cau) == {m["id_muc"] for m in v2.moi_muc(lich)} and all(m["nguon"] is None for m in v2.moi_muc(lich))
    assert all(c == "" for c in cau.values())  # không câu tả, không mã nguồn
    assert all(ng["chang"] for ng in lich["ngay"]) and all(m["loai_diem"] for m in v2.moi_muc(lich))


def test_sample_itinerary_gets_lodging_and_food_by_the_same_step_as_real_plans():
    """Lịch mẫu đi qua đúng bước gắn nơi ở + quán của lịch thật (`len_ke_hoach.gan_o_an`), theo cờ; cờ tắt ⇒ không có hai khối (như lịch thật)."""
    from api.routes import cong
    from llm import len_ke_hoach as lkh
    tat = cong.dung_lich_mau(V2)["lich"]
    assert tat.get("o_dau") is None and "an" not in tat
    bat = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True, anh_lich=False, luu_tru_lich=True, quan_lich=True)
    lich = cong.dung_lich_mau(bat)["lich"]
    assert lich["o_dau"] and lich["o_dau"]["co_so"] and lich["an"]
    khung = v2.xep_v2(bat.bang_lich_v2, v2.tu_truong(cong.TRUONG_MAU))
    mau = v2.dung_lich(bat.bang_lich_v2, khung, {}, None, (), None, None)
    import dataclasses
    kho = dataclasses.replace(bat, quan_bang={c: [q for q in ds if q["nguon"] == "kho"] for c, ds in bat.quan_bang.items()})
    lkh.gan_o_an(mau, bat.bang_lich_v2, khung, kho)
    assert lich["o_dau"] == mau["o_dau"] and lich["an"] == mau["an"]
    # lịch mẫu chỉ quán có bài trong kho (không nhãn nguồn mở, có bai_id); lịch thật vẫn dùng đủ nguồn
    assert all(q["nhan"] is None and q["bai_id"] for a in lich["an"] for q in a["quan"])
