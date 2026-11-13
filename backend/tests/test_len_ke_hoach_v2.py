"""“Lên kế hoạch” đợt 1 — bước (a): hợp đồng `truong` mới + biểu mẫu bốn nhóm, bộ xếp cũ (plan `docs/superpowers/plans/2026-11-12-len-ke-hoach-dot-1-plan.md`
§3 (a), spec bản 3.3 §5) — 0 USD.

Kiểm: bảng giá trị hợp lệ / không hợp lệ từng trường · đổi giá trị cũ ⇒ mới ⇒ cũ · cờ tắt ⇒ giá trị mới bị 422 như thân sai khuôn hôm nay và
`/api/tinh_nang` không có khoá mới · cờ bật ⇒ giá trị mới ra đúng chuỗi gửi model như giá trị cũ tương ứng (bộ xếp cũ). Đường biểu mẫu: SDK thật +
client giả có kịch bản (không mạng) + Qdrant thật (đọc) + bảng điểm thật (private) — như `test_cong_dot_1.py`. “Cờ tắt giống byte” của chuỗi gửi
model đo thêm bằng Q1 (`capture_all.py`, report).
"""
import dataclasses
import json
import datetime as dt
import itertools

import pytest
from pydantic import ValidationError

from llm import ngay_lich as nl
from llm.assistant import AssistantFlags
from llm.hoi_lai import GIA_TRI, NGAY_DI_TOI_DA, TruongInput, co_gia_tri_moi, doi_sang_cu, doi_sang_moi, loi_v2
from test_api_chat import chat_log_records, metric_lines
from test_b2_tool_loop import answer, deps, generator  # noqa: F401  (fixture `deps` dùng chung)
from test_cong_dot_1 import FORM, OFF, _restore, _with, app_client, chu_gui, flags_from, viet_theo_khung  # noqa: F401  (fixture `app_client`)

V2 = flags_from(lich_trinh_bieu_mau=True, len_ke_hoach_v2=True)
HOM_NAY = dt.date(2026, 11, 13)


# ---------- bảng giá trị của từng trường (khuôn) ----------

HOP_LE = [
    {"so_ngay": "5"}, {"so_ngay": "4+"}, {"so_ngay": "1", "nguoi_lon": 1}, {"so_ngay": "2", "nguoi_lon": 10, "tre_em": 6},
    {"so_ngay": "2", "tre_em": 0}, {"so_ngay": "2", "lon_tuoi": False}, {"so_ngay": "3", "kieu_di": "can_bang"},
    {"so_ngay": "3", "so_thich": ["di_tich", "am_thuc"]}, {"so_ngay": "3", "so_thich": "di_tich"}, {"so_ngay": "1", "ngay_di": "2026-12-20"},
    {"so_ngay": "2", "di_cung": "cap_doi", "kieu_di": "thong_tha"},
]
KHONG_HOP_LE = [
    {"so_ngay": "6"}, {"so_ngay": "0"}, {"so_ngay": 2}, {"nguoi_lon": 0}, {"nguoi_lon": 11}, {"nguoi_lon": "2"}, {"nguoi_lon": True},
    {"nguoi_lon": 2.0}, {"tre_em": -1}, {"tre_em": 7}, {"lon_tuoi": "co"}, {"lon_tuoi": 1}, {"kieu_di": "vua"},
    {"so_thich": ["di_tich", "am_thuc", "chup_anh"]}, {"so_thich": []}, {"so_thich": ["di_tich", "di_tich"]}, {"so_thich": ["mua_sam"]},
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


def test_v2_limits_by_vietnam_day_and_old_scheduler():
    def loi(**t):
        return loi_v2(TruongInput(**t), HOM_NAY)
    assert loi(ngay_di=HOM_NAY) is None and loi(ngay_di=HOM_NAY + dt.timedelta(days=NGAY_DI_TOI_DA)) is None
    assert loi(ngay_di=HOM_NAY - dt.timedelta(days=1)) == "ngay_di"
    assert loi(ngay_di=HOM_NAY + dt.timedelta(days=NGAY_DI_TOI_DA + 1)) == "ngay_di"
    assert loi(so_ngay="4") is None and loi(so_ngay="4+") is None and loi(so_ngay="5") == "so_ngay"  # bộ xếp cũ tới 4 ngày (ý 7)
    assert loi(so_thich=["di_tich"]) is None and loi(so_thich=["di_tich", "am_thuc"]) == "so_thich"  # bộ xếp cũ một sở thích


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
def test_flag_on_limits_rejected(app_client, path):
    app, client = app_client
    hom = nl.hom_nay()
    original = _with(app, V2, generator(lambda n, kw: [answer("x")]))
    try:
        rs = [_post(client, path, t) for t in (
            {"so_ngay": "5"}, {"so_ngay": "2", "so_thich": ["di_tich", "am_thuc"]},
            {"so_ngay": "2", "ngay_di": (hom - dt.timedelta(days=1)).isoformat()},
            {"so_ngay": "2", "ngay_di": (hom + dt.timedelta(days=NGAY_DI_TOI_DA + 1)).isoformat()})]
    finally:
        _restore(app, original)
    assert [r.status_code for r in rs] == [422] * 4


@pytest.mark.parametrize("path", ["/api/chat", "/api/chat/stream"])
def test_flag_on_new_form_sends_same_model_text_as_old_values(app_client, caplog, path):
    """Bước (a) dùng bộ xếp cũ ⇒ giá trị mới đổi về bốn trường cũ: chuỗi gửi model (lời dặn + tin nhắn) đúng như biểu mẫu cũ cùng nghĩa; log chỉ
    thêm số đếm. Ngày đi hợp lệ được nhận (chưa dùng ở bước này)."""
    app, client = app_client
    sent = {}
    for name, flags, truong in (("cu", FORM, OLD_SAME), ("moi", V2, {**NEW_FORM, "ngay_di": nl.hom_nay().isoformat()})):
        gen = generator(lambda n, kw: [answer(viet_theo_khung(kw))])
        original = _with(app, flags, gen)
        client.cookies.clear()  # lượt mới, không lịch sử hội thoại của lượt trước
        try:
            with chat_log_records(caplog) as records:
                r = _post(client, path, truong)
        finally:
            _restore(app, original)
        (call,) = gen.client.responses.calls
        line = metric_lines(records)[-1]  # `caplog.records` cộng dồn trong một test
        assert r.status_code == 200 and line["outcome"] == "success" and line["lich_trinh_ok"] is True
        sent[name] = (call["instructions"], chu_gui(call), line["co_truong"])
    assert sent["moi"][:2] == sent["cu"][:2]
    assert (sent["cu"][2], sent["moi"][2]) == (3, 6)


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
    assert on == {**co_cu, "len_ke_hoach_v2": {"o_hien": list(V2.len_ke_hoach_o_hien), "so_ngay_toi_da": 4, "so_thich_toi_da": 1}}
