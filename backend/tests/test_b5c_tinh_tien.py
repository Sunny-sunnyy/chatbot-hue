"""B5c (plan `docs/superpowers/plans/2026-11-05-phase-9-b5c-plan.md` bản 3 `bab730a57798`): công cụ `tinh_tien` — code đọc bảng kho, nhân / cộng,
dựng bảng + ghi chú, kiểm số tiền; code tự hỏi số người / ngày. Bảng nạp từ **kho thật** lúc chạy test; số kỳ vọng tính lại trong test từ chính
ô bảng (không chép giá kho vào repo). Model là client kịch bản của test B2 (không phải bằng chứng hành vi model)."""
import asyncio
import dataclasses
import itertools
import json
import re

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from core.settings_loader import load_settings
from llm import tinh_tien as tt
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream, nap_bang_lich, nap_bang_tien
from llm.do_so import SoNguoi, do_ngay_du_toan, do_so_nguoi
from llm.hoi_lai import TruongInput, ghep_cau, the_hoi_lai
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: F401  (fixture `deps` dùng chung)

SETTINGS = load_settings(validate_private_paths=False)
BANG = nap_bang_tien(SETTINGS)
ON = AssistantFlags(tim_them=True, tinh_tien=True, bang_tien=BANG)
OFF = AssistantFlags(tim_them=True)
CAU_THIEU = "Đi Huế thì dự trù bao nhiêu tiền?"


def tien_call(**args) -> dict:
    n = next(_ids)
    full = {"loai": "du_toan", "muc_chi": None, "diem": None, **args}
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "tinh_tien",
            "arguments": json.dumps(full, ensure_ascii=False), "status": "completed"}


def tool_names(kwargs) -> list[str]:
    return [t["name"] for t in kwargs.get("tools", [])]


def ts(loai="du_toan", so_nguoi=2, so_ngay="2", muc=None, diem=(), nguoi_lon=None, tre_em=None, tam=(), ngoai=None):
    return tt.ThamSoTien(loai, so_nguoi, nguoi_lon, tre_em, so_ngay, muc, tuple(diem), tuple(tam), ngoai)


# ---------- bảng kho (D2, D2b) ----------

def test_tables_load_from_real_kho_with_schema_and_totals():
    assert {n: len(b.hang_muc) for n, b in BANG.du_toan.items()} == {1: 5, 2: 6, 3: 6}
    for b in BANG.du_toan.values():  # tổng kho = tổng code (nạp đã kiểm; kiểm lại ở đây bằng phép cộng riêng)
        for m in tt.MUC:
            assert b.tong[m] == (sum(o[m][0] for _, o in b.hang_muc), sum(o[m][1] for _, o in b.hang_muc))
    assert len(BANG.ve) == tt.SO_DONG_VE and re.fullmatch(r"\d{2}/\d{2}/\d{4}", BANG.ve_hieu_luc)
    assert re.fullmatch(r"\d{2}/\d{2}/\d{4}", BANG.ngay_doi_chieu) and "tuổi" in BANG.ve_dieu_kien_tre
    quan_the = [d["id"] for d in BANG.diem.diem if d["quan_the"]]
    assert all(sum(v.id_diem == i for v in BANG.ve) == 1 for i in quan_the)


def _kho(rel: str) -> str:
    from pathlib import Path
    root = Path(__file__).resolve().parents[1] / SETTINGS["full_corpus"]["knowledge_base"]["root_dir"]
    return (root / rel).read_text(encoding="utf-8")


def test_loader_rejects_broken_tables():
    text = _kho(BANG.nguon_du_toan)
    dong_tong = next(d for d in text.splitlines() if "Tổng tại Huế" in d)
    so = re.findall(r"\d{1,3}(?:\.\d{3})+", dong_tong)[-1]  # cận cao mức cuối
    sai = f"{int(so.replace('.', '')) + 1000:,}".replace(",", ".")
    with pytest.raises(ValueError, match="tổng kho"):  # sửa một số ở dòng tổng ⇒ tổng kho ≠ tổng cộng
        tt.nap_du_toan(text.replace(dong_tong, dong_tong[::-1].replace(so[::-1], sai[::-1], 1)[::-1], 1))
    with pytest.raises(ValueError, match="ngày đối chiếu"):
        tt.nap_du_toan(text.replace("đối chiếu", "so sánh"))
    ve = _kho(BANG.nguon_ve)
    with pytest.raises(ValueError, match="hiệu lực"):
        tt.nap_ve(ve.replace("Ngày có hiệu lực", "Ngày ban hành"), BANG.diem)
    dong_ve = next(d for d in ve.splitlines() if d.startswith("| 1 |"))
    with pytest.raises(ValueError, match="ô giá"):
        tt.nap_ve(ve.replace(dong_ve, dong_ve.replace("|", "| khoảng", 4)[:len(dong_ve) + 20], 1), BANG.diem)


# ---------- phép tính (D3, D4, D5, D2b) ----------

@pytest.mark.parametrize("so_ngay, so_nguoi, muc", itertools.product(["1", "2", "3"], [1, 2, 5], [None, "tieu_chuan"]))
def test_budget_is_cell_times_people_summed_per_bound(so_ngay, so_nguoi, muc):
    kq = tt.tinh(BANG, ts(so_nguoi=so_nguoi, so_ngay=so_ngay, muc=muc))
    b = BANG.du_toan[int(so_ngay)]
    assert kq["du_toan"]["muc"] == ((muc,) if muc else tt.MUC)
    for (ten, o), (ten2, goc) in zip(kq["du_toan"]["hang_muc"], b.hang_muc):
        assert ten == ten2 and all(o[m] == (goc[m][0] * so_nguoi, goc[m][1] * so_nguoi) for m in kq["du_toan"]["muc"])
    for m in kq["du_toan"]["muc"]:
        assert kq["du_toan"]["tong"][m] == (b.tong[m][0] * so_nguoi, b.tong[m][1] * so_nguoi)


def test_budget_notes_children_and_odd_people():
    assert tt.tinh(BANG, ts(so_nguoi=4, nguoi_lon=2, tre_em=2))["luu_y"] == ["D3_tre_em"]
    assert tt.tinh(BANG, ts(so_nguoi=3, so_ngay="3"))["luu_y"] == ["D5_luu_tru"]
    assert tt.tinh(BANG, ts(so_nguoi=1, so_ngay="1"))["luu_y"] == []  # 1 ngày không có lưu trú


def test_tickets_alias_unknown_children_and_free():
    v0 = next(v for v in BANG.ve if v.bi_danh and v.tre_em > 0)
    v_mien = next(v for v in BANG.ve if v.tre_em == 0 and v.id_diem)
    kq = tt.tinh(BANG, ts("ve", 3, None, diem=[v0.bi_danh, BANG.diem.theo_id[v_mien.id_diem]["ten"], "Một điểm lạ"], nguoi_lon=2, tre_em=1))
    hang = {h["ten"]: h for h in kq["ve"]["hang"]}
    assert hang[v0.ten]["tien_lon"] == v0.nguoi_lon * 2 and hang[v0.ten]["tien_tre"] == v0.tre_em
    assert hang[v_mien.ten]["tien_tre"] == 0
    assert kq["ve"]["tong"] == sum(h["tien_lon"] + h["tien_tre"] for h in kq["ve"]["hang"]) and kq["khong_co"] == ["Một điểm lạ"]
    khong_ro = tt.tinh(BANG, ts("ve", None, None, diem=[v0.ten], nguoi_lon=2, tre_em=None))
    assert khong_ro["ve"]["tong"] is None and tt.CAU["ve_tre_khong_so"] in tt.khoi_ghi_chu(BANG, khong_ro)
    assert tt.tinh(BANG, ts("ve", 2, None, diem=["Một điểm lạ"]))["ngoai"] == "ve_ngoai_bang_ve_le"
    ca_hai = tt.tinh(BANG, ts("ca_hai", 2, "2", diem=[v0.ten]))
    assert ca_hai["du_toan"] and ca_hai["ve"] and "D4_khong_cong_ve" in ca_hai["luu_y"]  # hai bảng riêng, không cộng vé vào dự toán


# ---------- tham số (D6, D7) ----------

def test_params_ask_only_missing_and_answer_now_sets_temporary_values():
    assert tt.chot_tham_so("du_toan", None, None, None, SoNguoi(), (None, None)) == (None, ["so_nguoi", "so_ngay"])
    assert tt.chot_tham_so("du_toan", None, None, None, SoNguoi(), ("2", None)) == (None, ["so_nguoi"])
    assert tt.chot_tham_so("ve", None, ["x"], None, SoNguoi(), (None, None)) == (None, ["so_nguoi"])
    t, thieu = tt.chot_tham_so("du_toan", None, None, {}, SoNguoi(), ("2", None))  # "Trả lời luôn": giữ 2 ngày, tạm 1 người
    assert not thieu and (t.so_nguoi, t.so_ngay, t.tam) == (1, "2", ("so_nguoi",))
    t, _ = tt.chot_tham_so("du_toan", None, None, {"so_nguoi": 4, "muc_chi": "tiet_kiem"}, SoNguoi(tong=2), ("3", None))
    assert (t.so_nguoi, t.so_ngay, t.muc_chi, t.tam) == (4, "3", "tiet_kiem", ())  # nút thắng chữ dò


def test_budget_with_point_names_becomes_both_tables():
    t, _ = tt.chot_tham_so("du_toan", None, [BANG.ve[0].ten], None, SoNguoi(tong=2), ("2", None))
    kq = tt.tinh(BANG, t)
    assert t.loai == "ca_hai" and kq["du_toan"] and kq["ve"] and "D4_khong_cong_ve" in kq["luu_y"]


@pytest.mark.parametrize("cau, ngoai", [("đi 5 ngày cho 2 người", "so_ngay_4_tro_len"), ("2 ngày 2 đêm cho 2 người", "dem_lech"),
                                        ("nhóm 30 người đi 2 ngày", "qua_20_nguoi")])
def test_out_of_range_has_fixed_sentence_and_no_total(cau, ngoai):
    t, _ = tt.chot_tham_so("du_toan", None, None, None, do_so_nguoi(cau), do_ngay_du_toan(cau))
    kq = tt.tinh(BANG, t)
    assert kq["ngoai"] == ngoai and kq["du_toan"] is None and tt.bang_markdown(BANG, kq, 1, {}) == ""
    assert "Chưa đủ dữ liệu để tính tổng" in tt.khoi_ghi_chu(BANG, kq)
    assert tt.tinh(BANG, ts("ngoai_bang", None, None, ngoai="ngoai_bang"))["ngoai"] == "ngoai_bang"


def test_clarify_card_and_composed_question():
    the = the_hoi_lai("chi_phi", ["so_nguoi"], CAU_THIEU)
    assert the["bat_buoc"] == ["so_nguoi"] and [c["gia_tri"] for c in the["truong"][0]["lua_chon"]][-1] == "6+"
    assert ghep_cau(CAU_THIEU, TruongInput(so_nguoi=7, so_ngay="2")) == f"{CAU_THIEU} (Thông tin thêm: 2 ngày; 7 người.)"
    with pytest.raises(ValueError):
        TruongInput(so_nguoi=21)


# ---------- kiểm số tiền (D9) ----------

def test_money_check_allows_kho_and_code_numbers_only():
    kq = tt.tinh(BANG, ts(so_nguoi=2, so_ngay="1", muc="tieu_chuan"))
    code = kq["du_toan"]["tong"]["tieu_chuan"][1]
    kho = "Phòng tầm trung khoảng 300.000–600.000 đồng một đêm."
    assert tt.kiem_tien("Bạn có thể tham khảo bảng dưới.", [kho], kq) == []
    assert tt.kiem_tien("Phòng tầm trung khoảng 300.000 đồng [1].", [kho], kq) == []           # số có trong đoạn kho
    assert tt.kiem_tien(f"Cao nhất khoảng {tt.dong(code)}.", [kho], kq) == []                  # số code tính
    assert tt.kiem_tien("Mỗi người cần khoảng 777.000 đ.", [kho], kq) == ["so_tien_ngoai"]      # số tự nghĩ
    assert tt.kiem_tien("Mỗi người cần khoảng 777.000.", [kho], kq) == ["so_tien_ngoai"]        # không đơn vị vẫn bắt
    assert tt.kiem_tien("Tổng cộng khoảng 300.000 đồng.", [kho], kq) == ["tong_tu_viet"]        # tổng chỉ do code nối


# ---------- lõi: công cụ, thẻ hỏi lại, bảng code nối, stream (D1, D7, D8, D10, D12) ----------

def run(deps, query, gen, flags, trace=None, stream=False):
    trace = trace or AnswerTrace()

    async def go():
        if stream:
            return [e async for e in answer_turn_stream(query, *deps, gen, trace, flags)]
        await answer_turn(query, *deps, gen, trace, flags)

    return trace, asyncio.run(go())


@pytest.mark.parametrize("truong", [None, {}, {"so_nguoi": 2}])
@pytest.mark.parametrize("stream", [False, True])
def test_flag_adds_exactly_one_tool_and_same_instructions(deps, truong, stream):
    sent = {}
    for name, flags in (("on", ON), ("off", OFF)):
        gen = generator(lambda n, kw: [answer("Đại Nội mở cửa từ 7 giờ [1].")])
        run(deps, CAU_THIEU, gen, flags, AnswerTrace(truong=truong), stream)
        sent[name] = gen.client.responses.calls[0]
    assert tool_names(sent["off"]) == ["tim_kho"] and tool_names(sent["on"]) == ["tim_kho", "tinh_tien"]
    assert sent["on"]["instructions"] == sent["off"]["instructions"] and sent["on"]["input"] == sent["off"]["input"]
    schema = json.dumps(next(t for t in sent["on"]["tools"] if t["name"] == "tinh_tien"), ensure_ascii=False)
    assert not re.search(r"\d{1,3}\.\d{3}", schema) and all(v.ten not in schema for v in BANG.ve)  # ý #12


def test_code_asks_only_missing_fields(deps):
    gen = generator(lambda n, kw: [tien_call()])
    trace, _ = run(deps, "Đi Huế 2 ngày dự trù bao nhiêu?", gen, ON)
    assert len(gen.client.responses.calls) == 1 and trace.fixed_outcome == "hoi_lai"
    assert trace.clarify["loai"] == "chi_phi" and [t["ten"] for t in trace.clarify["truong"]] == ["so_nguoi"]


def test_numbers_from_previous_question_and_answer_now(deps):
    gen = generator(lambda n, kw: [tien_call()] if n == 1 else [answer("Bạn xem bảng dưới nhé.")])
    trace, _ = run(deps, "2 người, đi 3 ngày", gen, ON, AnswerTrace(history=((CAU_THIEU, ""),)))
    assert trace.clarify is None and trace.tien["kq"]["tham_so"].so_nguoi == 2 and trace.tien["kq"]["tham_so"].so_ngay == "3"
    gen = generator(lambda n, kw: [tien_call()] if n == 1 else [answer("Bạn xem bảng dưới nhé.")])
    trace, _ = run(deps, CAU_THIEU, gen, ON, AnswerTrace(truong={}, search_query=CAU_THIEU))
    assert trace.clarify is None and trace.tien["kq"]["tham_so"].tam == ("so_nguoi", "so_ngay")
    assert trace.answer.startswith("Mình hiểu: 1 người (tạm) · 1 ngày (tạm)") and "Mình tạm tính cho 1 người · 1 ngày" in trace.answer


def test_full_turn_stream_table_after_model_text(deps):
    script = lambda n, kw: [tien_call(muc_chi="tieu_chuan")] if n == 1 else [answer("Đây là dự trù cho chuyến của bạn.")]  # noqa: E731
    trace, events = run(deps, "Hai vợ chồng đi Huế 3 ngày 2 đêm hết bao nhiêu?", generator(script), ON, stream=True)
    tien = [d for k, d in events if k == "status" and d["stage"] == "tinh_tien"]
    assert [d["buoc"] for d in tien] == ["dang_tinh", "nap_bang", "tinh_xong"]
    text = "".join(d for k, d in events if k == "delta")
    assert trace.citation_error is None and text == trace.answer and text.startswith("Mình hiểu: 2 người · 3 ngày · mức tiêu chuẩn")
    n = re.search(r"\*\*Dự toán ba ngày hai đêm tại Huế cho 2 người\*\* \[(\d+)\]", text)
    src = trace.so_nguon[int(n.group(1)) - 1]
    assert n and src.source == BANG.nguon_du_toan and "Tổng tại Huế" in "".join(src.excerpts)  # D10: [n] là đoạn bảng thật
    assert tt.dong(BANG.du_toan[3].tong["tieu_chuan"][1] * 2) in text and tt.TIEU_DE_GHI_CHU in text


def test_out_of_range_refusal_keeps_fixed_sentence_and_passes(deps):
    from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
    gen = generator(lambda n, kw: [tien_call(loai="ngoai_bang")] if n == 1 else [answer(INSUFFICIENT_ANSWER)])
    trace, _ = run(deps, "Một đêm ở một khách sạn ven sông hết bao nhiêu?", gen, ON)
    assert trace.citation_error is None and trace.cited == () and INSUFFICIENT_ANSWER in trace.answer
    assert "Chưa đủ dữ liệu để tính tổng" in trace.answer


def test_invented_money_is_retracted_even_without_tool(deps):
    gen = generator(lambda n, kw: [answer("Đi Huế mỗi người cần khoảng 777.000 đ [1].")])
    trace, _ = run(deps, "Huế có gì vui?", gen, ON)
    assert trace.tien is None and trace.tien_kiem == ["so_tien_ngoai"] and "money check failed" in str(trace.citation_error)
    gen = generator(lambda n, kw: [answer("Đi Huế mỗi người cần khoảng 777.000 đ [1].")])
    trace, _ = run(deps, "Huế có gì vui?", gen, OFF)
    assert trace.citation_error is None  # cờ tắt: như `main`


def test_route_cost_fields_validate_and_flag_off_composes():
    app = create_app()
    with TestClient(app) as client:
        gen = generator(lambda n, kw: [answer("Đại Nội mở cửa từ 7 giờ [1].")])
        original = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        app.state.generator, app.state.generator_ready = gen, True
        app.state.assistant_flags = dataclasses.replace(OFF, router=False)
        ok = client.post("/api/chat", json={"query": CAU_THIEU, "truong": {"so_nguoi": 3, "muc_chi": "thoai_mai"}})
        qua = client.post("/api/chat", json={"query": CAU_THIEU, "truong": {"so_nguoi": 25}})
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = original
    assert ok.status_code == 200 and "Thông tin thêm: 3 người; mức thoải mái." in json.dumps(gen.client.responses.calls[0]["input"], ensure_ascii=False)
    assert qua.status_code == 422
