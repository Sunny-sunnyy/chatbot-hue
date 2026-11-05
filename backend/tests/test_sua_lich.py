"""Sửa lịch nhiều lượt (plan `docs/superpowers/plans/2026-11-05-phase-9-sua-lich-plan.md` bản 3 `5b68f3cb666a`): hành động có tên, code áp
theo luật B5, giữ chỗ điểm không chạm, điểm đã bỏ không quay lại, thẻ chọn, khung lưu của cuộc. Bảng điểm thật (User duyệt); model là client
kịch bản của test B2 (không phải bằng chứng hành vi model). Câu tự viết."""
import copy
import dataclasses
import json

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from llm import lich_trinh as lt
from llm import sua_lich as sl
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: F401
from test_b5_lich_trinh import BANG, ON, lich_call, tool_names, viet_theo_khung

SUA_ON = dataclasses.replace(ON, sua_lich=True, nho_hoi_thoai=True)
CAU = "Lên lịch Huế 2 ngày giúp mình, mình thích di tích"


def hd(**k) -> sl.HanhDong:
    return sl.HanhDong(**k)


def luu(**ts) -> dict:
    t = lt.ThamSo(**{"so_ngay": "2", "so_thich": "di_tich", **ts})
    return sl.luu_tu_lich(lt.xep(BANG, t), ["so_ngay", "so_thich"], [lt.khop_diem(BANG, x) for x in t.them_diem], CAU)


def vt(khung) -> dict:
    return sl._vi_tri(khung)


# ---------- xep(giu, loai) ----------

def test_xep_keeps_positions_and_never_brings_back_removed():
    goc = lt.xep(BANG, lt.ThamSo(so_ngay="2", so_thich="di_tich"))
    a, b = list(vt(goc).items())[:2]
    moi = lt.xep(BANG, lt.ThamSo(so_ngay="3", so_thich="di_tich"), giu=dict([a]), loai=frozenset([b[0]]))
    assert vt(moi)[a[0]] == a[1] and b[0] not in vt(moi) and not lt.kiem_khung(BANG, moi)
    assert lt.xep(BANG, lt.ThamSo(so_ngay="2", so_thich="di_tich"), None, frozenset()) == goc  # mặc định = B5


# ---------- mỗi hành động + một ca cố tình vi phạm ----------

def test_remove_keeps_every_other_slot():
    s = luu()
    i = next(iter(vt(s["khung"])))
    kq = sl.ap_hanh_dong(BANG, s, [hd(loai="bo_diem", ten=BANG.theo_id[i]["ten"])])
    assert i not in vt(kq["khung"]) and i in kq["luu"]["loai"]
    assert all(vt(kq["khung"])[x] == v for x, v in vt(s["khung"]).items() if x != i) and not lt.kiem_khung(BANG, kq["khung"])
    assert sl.ap_hanh_dong(BANG, s, [hd(loai="bo_diem", ten="Một quán lạ")])["khong_doi"] == [{"diem": "Một quán lạ", "ma_luat": "ngoai_bang"}]


def test_add_evening_with_elderly_is_refused():
    s = luu(di_cung="nguoi_lon_tuoi")
    kq = sl.ap_hanh_dong(BANG, s, [hd(loai="them_diem", ten="Phố đi bộ Nguyễn Đình Chiểu", ngay=1, buoi="toi")])
    assert kq["da_ap"] == [] and kq["khong_doi"][0]["ma_luat"] == "khong_buoi_hop_le" and kq["khung"] == s["khung"]
    assert "Không đổi được" in sl.khoi_sua(BANG, kq)


def test_replace_named_and_unnamed_and_empty_card():
    s = luu()
    cu = next(iter(vt(s["khung"])))
    kq = sl.ap_hanh_dong(BANG, s, [hd(loai="thay_diem", ten=BANG.theo_id[cu]["ten"])])
    assert kq["the"] is not None and kq["khung"] == s["khung"] and kq["luu"]["the_chon"]["cu"] == cu  # thẻ ⇒ khung không đổi
    lua = kq["the"]["lua_chon"]
    the = sl.the_chon(BANG, cu, lua, CAU)
    assert [c["gia_tri"] for c in the["lua_chon"]][-1] == "bo" and all(c in BANG.theo_id for c in lua)  # nút chỉ id code đưa
    if lua:
        bam = sl.ap_hanh_dong(BANG, kq["luu"], [], {"cu": cu, "moi": lua[0]})
        assert bam["the"] is None and vt(bam["khung"])[lua[0]] == vt(s["khung"])[cu] and cu not in vt(bam["khung"])
    bo = sl.ap_hanh_dong(BANG, kq["luu"], [hd(loai="thay_diem", ten=BANG.theo_id[cu]["ten"])], {"cu": cu, "moi": "bo"})
    assert bo["the"] is None and cu not in vt(bo["khung"])  # lượt bấm nút không bao giờ đưa thẻ lần hai


def test_no_valid_replacement_gives_not_changed_line_not_empty_card():
    """B166 (K-S2): hết điểm thay hợp lệ ⇒ không thẻ, khung giữ nguyên, khối "Không đổi được" có câu cố định của mã `het_diem_thay`."""
    s = luu(so_thich="am_thuc")
    vtri = vt(s["khung"])
    het = next((i for i in vtri if not sl._lua_chon_thay(BANG, s["khung"], s["them"], s["loai"], i)), None)
    if het is None:  # bảng hôm nay còn điểm thay cho mọi chỗ ⇒ dồn mọi điểm cùng sở thích vào `loai` để chắc chắn hết
        het = next(iter(vtri))
        s = {**s, "loai": [d["id"] for d in BANG.diem if d["id"] not in vtri]}
    assert sl._lua_chon_thay(BANG, s["khung"], s["them"], s["loai"], het) == []
    kq = sl.ap_hanh_dong(BANG, s, [hd(loai="thay_diem", ten=BANG.theo_id[het]["ten"])])
    assert kq["the"] is None and kq["luu"]["the_chon"] is None and vt(kq["khung"]) == vtri
    assert kq["khong_doi"] == [{"diem": BANG.theo_id[het]["ten"], "ma_luat": "het_diem_thay"}]
    assert sl.CAU_KHONG_DOI["het_diem_thay"].format(diem=BANG.theo_id[het]["ten"]) in sl.khoi_sua(BANG, kq)


def test_move_swaps_two_points_and_rejects_bad_slot():
    s = luu()
    ng1 = s["khung"]["ngay"][0]["buoi"]
    a, b = ng1["sang"][0], ng1["chieu"][0]
    kq = sl.ap_hanh_dong(BANG, s, [hd(loai="doi_buoi", ten=BANG.theo_id[a]["ten"], ngay=1, buoi="chieu")])
    if kq["da_ap"]:
        assert vt(kq["khung"])[a] == (1, "chieu") and vt(kq["khung"])[b] == (1, "sang") and not lt.kiem_khung(BANG, kq["khung"])
    else:
        assert kq["khong_doi"]  # phạm luật ⇒ nói rõ, không đổi
    ve = sl.ap_hanh_dong(BANG, s, [hd(loai="doi_buoi", ten=BANG.theo_id[a]["ten"], ngay=1, buoi="toi")])
    assert ve["khung"] == s["khung"] or not lt.kiem_khung(BANG, ve["khung"])


def test_day_change_keeps_added_and_never_restores_removed():
    s = luu(them_diem=("Chợ Đông Ba",))
    bo = next(i for i in vt(s["khung"]) if i != "cho_dong_ba")
    s = sl.ap_hanh_dong(BANG, s, [hd(loai="bo_diem", ten=BANG.theo_id[bo]["ten"])])["luu"]
    kq = sl.ap_hanh_dong(BANG, s, [hd(loai="doi_so_ngay", so_ngay="3")])
    assert "cho_dong_ba" in vt(kq["khung"]) and bo not in vt(kq["khung"]) and len(kq["khung"]["ngay"]) == 3
    assert kq["doi_truong"] == [("so_ngay", "2", "3")] and "Đã đổi số ngày: 2 ngày → 3 ngày." in sl.khoi_sua(BANG, kq)


def test_refilling_old_values_changes_nothing_and_drop_interest():
    s = luu()
    kq = sl.ap_hanh_dong(BANG, s, [hd(loai="doi_tham_so", so_thich="di_tich")])  # Travel-AI: điền lại giá trị cũ không được ghi đè gì
    assert kq["doi_truong"] == [] and kq["da_ap"] == [] and sl.khoi_sua(BANG, kq) == ""
    bo = sl.ap_hanh_dong(BANG, s, [hd(loai="doi_tham_so", so_thich="bo")])  # bỏ sở thích được (lỗi gộp thứ hai của Travel-AI)
    assert bo["doi_truong"] == [("so_thich", "di_tich", None)] and bo["khung"]["tham_so"]["so_thich"] is None
    assert bo["luu"]["tham_so"]["so_ngay"] == "2"  # trường khác giữ


def test_three_actions_apply_two_and_say_not_done():
    s = luu()
    ids = list(vt(s["khung"]))
    kq = sl.ap_hanh_dong(BANG, s, [hd(loai="bo_diem", ten=BANG.theo_id[ids[0]]["ten"]), hd(loai="bo_diem", ten=BANG.theo_id[ids[1]]["ten"]),
                                   hd(loai="doi_so_ngay", so_ngay="3")])
    assert len(kq["da_ap"]) == 2 and kq["chua_lam"] == ["doi_so_ngay"] and "Chưa làm: đổi số ngày" in sl.khoi_sua(BANG, kq)


def test_saved_state_is_never_mutated():
    s = luu()
    goc = copy.deepcopy(s)
    sl.ap_hanh_dong(BANG, s, [hd(loai="bo_diem", ten=BANG.theo_id[next(iter(vt(s["khung"])))]["ten"]), hd(loai="doi_so_ngay", so_ngay="1")])
    assert s == goc


# ---------- route + lõi: khung lưu của cuộc ----------

def _script(hanh_dong):
    """Lượt có `sua_lich` ⇒ gọi với `hanh_dong`; lượt chỉ có `lich_trinh` ⇒ xếp 2 ngày; sau kết quả công cụ ⇒ viết theo khung."""
    def s(_n, kw):
        if any(i.get("type") == "function_call_output" for i in kw["input"]):
            return [answer(viet_theo_khung(kw))]
        if "sua_lich" in tool_names(kw):
            n = next(_ids)
            return [{"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "sua_lich", "status": "completed",
                     "arguments": json.dumps({"hanh_dong": hanh_dong}, ensure_ascii=False)}]
        return [lich_call(so_ngay="2", so_thich="di_tich")]
    return s


def _client_turns(turns, flags=SUA_ON):
    app = create_app()
    out = []
    with TestClient(app) as client:
        original = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        app.state.generator_ready, app.state.assistant_flags = True, dataclasses.replace(flags, router=False)
        for body, script in turns:
            app.state.generator = generator(script)
            r = client.post("/api/chat", json=body)
            cid = client.cookies.get("conversation_id")
            out.append((r, app.state.generator.client.responses.calls, app.state.conversations.lich(cid)))
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = original
    return out


def test_two_edit_turns_build_on_what_user_saw_and_tool_only_with_saved_plan():
    (r1, c1, l1), = _client_turns([({"query": CAU}, _script([]))])
    assert "sua_lich" not in tool_names(c1[0]) and l1 is not None  # lượt đầu: chưa có khung ⇒ không có công cụ thứ ba; sau lượt đạt ⇒ lưu
    dau = next(iter(vt(l1["khung"])))
    rows = _client_turns([({"query": CAU}, _script([])),
                          ({"query": "Bỏ điểm đầu tiên giúp mình"}, _script([{"loai": "bo_diem", "ten": BANG.theo_id[dau]["ten"]}])),
                          ({"query": "Thêm một ngày nữa nhé"}, _script([{"loai": "doi_so_ngay", "so_ngay": "3"}]))])
    (_, _, a), (r2, c2, b), (r3, c3, c) = rows
    assert "sua_lich" in tool_names(c2[0]) and r2.json()["answer"].startswith("Mình hiểu: 2 ngày")
    assert dau not in vt(b["khung"]) and all(vt(b["khung"])[x] == v for x, v in vt(a["khung"]).items() if x != dau)  # lượt 2 sửa trên khung lượt 1
    assert dau not in vt(c["khung"]) and len(c["khung"]["ngay"]) == 3 and sl.TIEU_DE_SUA in r3.json()["answer"]  # lượt 3 sửa trên khung lượt 2


def test_card_turn_keeps_plan_and_choice_turn_never_asks_twice_and_bad_choice_422():
    first = _client_turns([({"query": CAU}, _script([]))])[0][2]
    cu = next(iter(vt(first["khung"])))
    app = create_app()
    with TestClient(app) as client:
        original = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        app.state.generator_ready, app.state.assistant_flags = True, dataclasses.replace(SUA_ON, router=False)
        app.state.generator = generator(_script([]))
        client.post("/api/chat", json={"query": CAU})
        cid = client.cookies.get("conversation_id")
        truoc = app.state.conversations.lich(cid)
        app.state.generator = generator(_script([{"loai": "thay_diem", "ten": BANG.theo_id[cu]["ten"]}]))
        the = client.post("/api/chat", json={"query": "Đổi điểm đầu sang chỗ khác"}).json()
        sau_the = app.state.conversations.lich(cid)
        bad = client.post("/api/chat", json={"query": "x", "sua_chon": {"cu": cu, "moi": "dai_noi_gia"}})
        app.state.generator = generator(_script([{"loai": "thay_diem", "ten": BANG.theo_id[cu]["ten"]}]))  # model gửi lại thay không tên ⇒ code bỏ qua
        chon = client.post("/api/chat", json={"query": "x", "sua_chon": {"cu": cu, "moi": "bo"}}).json()
        sau = app.state.conversations.lich(cid)
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = original
    assert the["clarify"]["loai"] == "sua_chon" and sau_the["khung"] == truoc["khung"] and sau_the["the_chon"]["cu"] == cu
    assert bad.status_code == 422
    assert chon["clarify"] is None and cu not in vt(sau["khung"]) and sau["the_chon"] is None


def test_retracted_turn_does_not_save_plan(deps):
    def viet_sai(_n, kw):  # lượt lịch mà chữ model có giờ ngoài khung ⇒ kiểm cuối hỏng ⇒ rút lại
        if any(i.get("type") == "function_call_output" for i in kw["input"]):
            return [answer(viet_theo_khung(kw) + " Mở cửa lúc 5h15.")]
        return [lich_call(so_ngay="2", so_thich="di_tich")]
    (r, _, saved), = _client_turns([({"query": CAU}, viet_sai)])
    assert r.json()["error"]["code"] == "citation_integrity_error" and saved is None


def test_flag_off_or_no_plan_sends_b5_request(deps):
    from test_b5_lich_trinh import run
    sent = {}
    for name, flags in (("b5", ON), ("sua", SUA_ON)):
        gen = generator(lambda n, kw: [answer("Đại Nội mở cửa từ 7 giờ [1].")])
        run(deps, CAU, gen, flags)
        sent[name] = gen.client.responses.calls[0]
    assert json.dumps(sent["b5"], sort_keys=True, default=str) == json.dumps(sent["sua"], sort_keys=True, default=str)  # Q1m mức test
