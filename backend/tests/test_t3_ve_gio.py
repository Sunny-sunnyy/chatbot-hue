"""T3 — bảng vé + giờ mở cửa (`tra_ve_gio`), plan `docs/superpowers/plans/2026-11-08-phase-9-t3-bang-plan.md` bản 2 — 0 USD.

Bảng thật (`data/phase_9/t3_bang_ve_gio/bang_v1.json`, private — clone không có ⇒ skip); SDK thật + client kịch bản (không mạng) + Qdrant thật (đọc)
như `test_b5b_thoi_tiet.py`. Đây **không** là bằng chứng model thật dùng bảng đúng — phần đó ở lượt có phí (Q2 / Q3 / S1 / S4)."""
import asyncio
import dataclasses
import json
import re
from pathlib import Path

import pytest

from api.routes.chat import _source_responses
from core.settings_loader import BACKEND_DIR, load_settings
from llm import ve_gio as vg
from llm.assistant import (AnswerTrace, AssistantFlags, _ve_gio_cuoi, answer_turn, answer_turn_stream, answer_turn_stream_parallel,
                           chu_cua_model, ve_gio_for_turn)
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER, ROUTER_INSTRUCTIONS
from llm.generator_openai_full_corpus import ASSISTANT_MAX_TURNS, max_turns_cho, max_turns_for
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: F401  (fixture `deps`: Qdrant thật, chỉ đọc)

SETTINGS = load_settings(validate_private_paths=False)
BANG_PATH = BACKEND_DIR / SETTINGS["assistant"]["tra_ve_gio_bang"]
if not BANG_PATH.exists():
    pytest.skip("bảng vé / giờ private không có (clone public)", allow_module_level=True)
BANG = vg.nap_bang(BANG_PATH)
ON = AssistantFlags(tim_them=True, tra_ve_gio=True, bang_ve_gio=BANG)
OFF = AssistantFlags(tim_them=True)
AN_TOAN = Path(__file__).resolve().parents[2] / "data/loi_nang_2026-10-28/an_toan/questions.jsonl"


def _diem_co_mien_phi():
    return next(d for d in BANG.diem if any(vg._la_mien_phi(v) for v in d["ve"]) and any(not vg._la_mien_phi(v) and v.get("gia") for v in d["ve"]))


# ---------- bảng + khớp tên ----------

def test_table_loads_and_names_match_by_name_and_alias():
    assert len(BANG.diem) == 60 and all(d["nhom"] != "su_kien" for d in BANG.diem)  # User 08/11 câu 2: bỏ sự kiện đã diễn ra
    dai_noi = next(d for d in BANG.diem if d["ten"] == "Đại Nội Huế")
    assert vg.khop(BANG, "đại nội huế") is dai_noi and vg.khop(BANG, "  Hoàng thành và Tử Cấm thành ") is dai_noi
    assert vg.khop(BANG, "Lăng Tự Đức") is vg.khop(BANG, "Khiêm Lăng") is not None
    assert vg.khop(BANG, "Chùa Thiên Mụ") is None  # kho không có giờ / vé ⇒ ngoài bảng


def test_flag_off_does_not_load_table():
    s = json.loads(json.dumps(SETTINGS))
    s["assistant"]["tra_ve_gio"] = False
    s["assistant"]["tra_ve_gio_bang"] = "../khong_co_file.json"
    assert AssistantFlags.from_settings(s).bang_ve_gio is None  # cờ tắt ⇒ không đọc file (clone public chạy được)


# ---------- cổng từ khoá (plan m-2) — chốt trước lượt có phí ----------

@pytest.mark.parametrize("cau", ["Vé vào Đại Nội bao nhiêu?", "Lăng Tự Đức mở cửa mấy giờ?", "Giờ tham quan lăng Khải Định?", "Trẻ em có được miễn vé không?",
                                 "Đi Hải Vân Quan mất tiền không?", "Phí tham quan Bạch Mã thế nào?", "Người cao tuổi có giảm giá không?",
                                 "Giảm 50% cho ai?", "Có ưu đãi cho sinh viên không?", "Mấy giờ đóng cửa?"])
def test_gate_hits_ticket_and_hours_questions(cau):
    assert vg.co_tu_khoa(cau)


@pytest.mark.parametrize("cau", ["Bây giờ nên đi đâu?", "Bao giờ có lễ hội?", "Đánh giá món bún bò thế nào?", "Miễn là trời không mưa thì đi đâu?",
                                 "Lăng Tự Đức có gì đẹp?", "Chợ Đông Ba bán gì?"])
def test_gate_skips_ordinary_questions(cau):
    assert not vg.co_tu_khoa(cau)


def test_gate_hits_every_safety_question_about_exemptions():
    if not AN_TOAN.exists():
        pytest.skip("bộ an toàn private không có")
    rows = [json.loads(l) for l in AN_TOAN.read_text(encoding="utf-8").splitlines() if l.strip()]
    mien = [r["question"] for r in rows if r["category"] == "mien_giam"]
    assert len(mien) == 6 and all(vg.co_tu_khoa(q) for q in mien)


# ---------- trường nào đi đâu (plan M-2) ----------

def test_free_row_and_conditions_never_reach_model_but_block_has_them():
    d = _diem_co_mien_phi()
    gui = "\n".join(c for _, c in vg.dong_gui_model(d))
    mien = [v for v in d["ve"] if vg._la_mien_phi(v)]
    assert gui and not any(f"{vg._sach(v.get('doi_tuong') or '')}: {vg._sach(v['gia'])}" in gui for v in mien)  # dòng miễn phí không vào model
    assert not any(vg._sach(m["nguyen_van"]) in gui for m in d["mien_giam"])
    khoi = vg.khoi_dieu_kien(BANG, [d], day_du=True)
    assert all(f"{d['ten']} — {vg._sach(v.get('doi_tuong') or '')}: {vg._sach(v['gia'])}" in khoi for v in mien)
    assert all(vg._sach(m["nguyen_van"]) in khoi for m in d["mien_giam"])


def test_short_block_when_question_is_not_about_who_pays():
    d = next(d for d in BANG.diem if d["ten"] == "Đại Nội Huế")
    ngan = vg.khoi_dieu_kien(BANG, [d], day_du=vg.hoi_dieu_kien("Vé Đại Nội bao nhiêu?"))
    du = vg.khoi_dieu_kien(BANG, [d], day_du=vg.hoi_dieu_kien("Trẻ 5 tuổi vào Đại Nội có mất vé không?"))
    assert ngan.startswith("Có điều kiện miễn / giảm vé") and du.startswith("**Điều kiện miễn / giảm vé**") and len(du) > len(ngan)
    assert vg.CAU_MAU_THUAN.format(ten="Đại Nội Huế") in du  # G4 — User 08/11 câu 1 (a)


# ---------- kiểm số (plan M-1, n-3) ----------

@pytest.mark.parametrize("chu, cho_phep, loi", [
    ("Vé 200.000 đồng, mở 7h30.", "vé người lớn: 200.000 đồng · giờ mở cửa: 07:30 – 17:30", []),
    ("Mở từ 7 giờ tới 17 giờ 30.", "giờ mở cửa: 07h00 – 17h30", []),
    ("Tham quan mất 2 giờ, vé 200.000 đồng.", "vé: 200.000 đồng", []),            # thời lượng không phải giờ trong ngày
    ("Vé 250.000 đồng.", "vé: 200.000 đồng", ["tien_ngoai_bang"]),
    ("Mở cửa lúc 8h.", "giờ mở cửa: 07h00 – 17h30", ["gio_ngoai_bang"]),
    ("Nhóm 3 người tốn 600.000 đồng.", "vé: 200.000 đồng · câu hỏi: 3 người", ["tien_ngoai_bang"]),  # không cộng / nhân
    # vòng 3 (lượt 2 T05): đoạn kho ghi ô bảng "420.000" không kèm "đồng" ⇒ vẫn là số được phép; số khác vẫn bị bắt
    ("Vé tuyến 420.000 đồng/người lớn và 80.000 đồng/trẻ em.", "| Tuyến 1 | 420.000 | 80.000 |", []),
    ("Vé tuyến 450.000 đồng.", "| Tuyến 1 | 420.000 | 80.000 |", ["tien_ngoai_bang"]),
    ("Vé 2.000 đồng.", "năm 2026, mở 7:30", ["tien_ngoai_bang"]),            # năm / giờ không thành số tiền được phép
])
def test_number_check(chu, cho_phep, loi):
    assert vg.kiem_so(chu, cho_phep) == loi


def test_max_turns_only_grows_with_ticket_tool():
    f = object()
    assert max_turns_cho(None, None) == max_turns_cho(None, f) == ASSISTANT_MAX_TURNS
    assert max_turns_cho(f, None) == ASSISTANT_MAX_TURNS + 1 and max_turns_cho(f, f) == ASSISTANT_MAX_TURNS + 2
    # rebase lên T1: lượt có cả `ngay_lich` lẫn `tra_ve_gio` + `thoi_tiet` ⇒ cộng cả hai phần (4 + 1 + 2)
    assert max_turns_for(None) == ASSISTANT_MAX_TURNS and max_turns_for(f, f, f) == ASSISTANT_MAX_TURNS + 3


# ---------- công cụ + sổ nguồn (M-5, n-5) ----------

def test_tool_result_is_a_source_with_corpus_file_and_bai_id():
    trace = AnswerTrace()
    chu = asyncio.run(ve_gio_for_turn("Vé Đại Nội bao nhiêu?", trace, BANG)(["Đại Nội", "Chùa Thiên Mụ"]))
    assert "[Nguồn 1]" in chu and vg.CAU_CO_DIEU_KIEN in chu and f"Chùa Thiên Mụ: {vg.CAU_NGOAI_BANG}" in chu
    src = trace.so_nguon[0]
    assert src.source.startswith("travel/tickets/") or src.source.startswith("heritages/")
    bai_ids = {s.source: {} for s in trace.so_nguon}
    assert all(r.bai_id == s.source for r, s in zip(_source_responses(tuple(trace.so_nguon), bai_ids), trace.so_nguon))
    assert [d["ten"] for d in trace.ve_gio["diem"]] == ["Đại Nội Huế"]
    assert trace.tools[-1] == {"name": "tra_ve_gio", "n_diem": 2, "n_khop": 1, "n_khong_bang": 1, "co_dieu_kien": True, "by": "model", "ms": 0.0}
    n_nguon = len(trace.so_nguon)  # Đại Nội: dòng vé (file vé) + dòng giờ (file di tích) ⇒ 2 nguồn, mỗi file một nguồn
    assert n_nguon == len({s.source for s in trace.so_nguon}) == 2
    lan2 = asyncio.run(ve_gio_for_turn("x", trace, BANG)(["Đại Nội"]))
    assert "lần gọi trước" in lan2 and len(trace.so_nguon) == n_nguon  # ≤ 1 lần / câu


def _tra(query, diem):
    trace = AnswerTrace()
    asyncio.run(ve_gio_for_turn(query, trace, BANG)(diem))
    return trace


def test_refusal_with_rows_is_replaced_out_of_scope_keeps_no_block():
    tu_choi = _tra("Vé Đại Nội bao nhiêu?", ["Đại Nội"])
    tu_choi.answer = INSUFFICIENT_ANSWER
    _ve_gio_cuoi(tu_choi, INSUFFICIENT_ANSWER, BANG)
    assert tu_choi.answer.startswith(vg.CAU_DAN_TU_CHOI) and tu_choi.ve_gio["thay_tu_choi"] and tu_choi.citation_error is None
    assert chu_cua_model(tu_choi) != INSUFFICIENT_ANSWER and tu_choi.answer.endswith(tu_choi.ve_gio_noi)
    ngoai = _tra("Vé Đại Nội bao nhiêu?", ["Đại Nội"])
    ngoai.answer = OUT_OF_SCOPE_ANSWER
    _ve_gio_cuoi(ngoai, OUT_OF_SCOPE_ANSWER, BANG)
    assert ngoai.answer == OUT_OF_SCOPE_ANSWER and ngoai.ve_gio_noi is None and chu_cua_model(ngoai) == OUT_OF_SCOPE_ANSWER


# ---------- nối vào lõi: 3 đường (M-1 (d), n-2) ----------

def ve_call(diem) -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "tra_ve_gio",
            "arguments": json.dumps({"diem": diem}, ensure_ascii=False), "status": "completed"}


def ma_nguon(kw) -> int:
    """Mã [k] của nguồn bảng: vòng 2 — code tự tra ⇒ nguồn nằm trong tin nhắn đầu (không phải kết quả công cụ)."""
    chu = json.dumps(kw["input"], ensure_ascii=False)
    return int(re.search(rf"\[Nguồn (\d+)\]\\nTiêu đề: {vg.TIEU_DE_NGUON}", chu).group(1))


def kich_ban(text_fn, route="tro_ly_hue"):
    """Định tuyến (nhận bằng lời dặn) ⇒ `route`; trợ lý viết `text_fn(k)` ngay (k = nguồn bảng code đã tra). Ghi tên công cụ mỗi lần gọi trợ lý."""
    seen, n_tro_ly = [], [0]

    def script(n, kw):
        if str(kw.get("instructions", "")).startswith(ROUTER_INSTRUCTIONS[:80]):
            return [{"type": "message", "id": f"msg_{next(_ids)}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": route}), "annotations": []}]}]
        n_tro_ly[0] += 1
        seen.append(sorted(t.get("name") for t in kw.get("tools") or []))
        return [answer(text_fn(ma_nguon(kw)))]
    return script, seen


def chay(deps, duong, text_fn, flags=ON, query="Vé vào Đại Nội bao nhiêu?"):
    script, seen = kich_ban(text_fn)
    gen, trace = generator(script), AnswerTrace()
    f = dataclasses.replace(flags, router=True, song_song_tra_loi=True) if duong == "song_song" else flags

    async def go():
        if duong == "chat":
            await answer_turn(query, *deps, gen, trace, f)
            return []
        fn = answer_turn_stream if duong == "stream" else answer_turn_stream_parallel
        return [e async for e in fn(query, *deps, gen, trace, f)]
    events = asyncio.run(go())
    return trace, events, seen


@pytest.mark.parametrize("duong", ["chat", "stream", "song_song"])
def test_invented_price_is_retracted_on_all_three_paths(deps, duong):
    ok, ev_ok, seen = chay(deps, duong, lambda k: f"Vé người lớn vào Đại Nội là 200.000 đồng [{k}].")
    assert ok.citation_error is None and ok.ve_gio_kiem == [] and "tra_ve_gio" not in seen[0]  # code đã tra ⇒ không đưa công cụ
    assert [t for t in ok.tools if t["name"] == "tra_ve_gio"][0]["by"] == "code"
    bia, ev_bia, _ = chay(deps, duong, lambda k: f"Vé người lớn vào Đại Nội là 250.000 đồng [{k}].")
    assert bia.citation_error is not None and bia.ve_gio_kiem == ["tien_ngoai_bang"]
    if duong != "chat":
        shown = "".join(d for kind, d in ev_ok if kind == "delta")
        assert shown == ok.answer and ok.ve_gio_noi and shown.endswith(ok.ve_gio_noi)
        assert not any(kind == "delta" and bia.ve_gio_noi and bia.ve_gio_noi in d for kind, d in ev_bia)  # đã rút lại ⇒ không nối khối


@pytest.mark.parametrize("duong", ["chat", "stream"])
def test_stream_holds_refusal_when_rows_exist(deps, duong):
    trace, events, _ = chay(deps, duong, lambda k: INSUFFICIENT_ANSWER)
    assert trace.answer.startswith(vg.CAU_DAN_TU_CHOI) and trace.citation_error is None
    if duong == "stream":
        shown = "".join(d for kind, d in events if kind == "delta")
        assert INSUFFICIENT_ANSWER not in shown and shown == trace.answer


def test_tool_offered_only_with_keyword_and_flag(deps):
    seen_all = []
    for flags, q in ((ON, "Lăng Tự Đức có gì đẹp?"), (OFF, "Vé vào Đại Nội bao nhiêu?"), (ON, "Vé vào chỗ này bao nhiêu?"), (ON, "Vé vào Đại Nội bao nhiêu?")):
        seen = []
        gen = generator(lambda n, kw: (seen.append(sorted(t.get("name") for t in kw.get("tools") or [])), [answer("Có trong nguồn [1].")])[1])
        asyncio.run(answer_turn(q, *deps, gen, AnswerTrace(), flags))
        seen_all.append(seen[0])
    # từ khoá + không dò ra tên ⇒ công cụ; dò ra tên ⇒ code tự tra, không đưa công cụ (vòng 2)
    assert seen_all == [["tim_kho"], ["tim_kho"], ["tim_kho", "tra_ve_gio"], ["tim_kho"]]


@pytest.mark.parametrize("cau, ten", [
    ("Vé vào Đại Nội bao nhiêu?", ["Đại Nội Huế"]),
    ("Giá vé lăng Tự Đức và lăng Khải Định?", ["Lăng vua Tự Đức", "Lăng vua Khải Định"]),
    ("Khiêm Lăng mở cửa mấy giờ?", ["Lăng vua Tự Đức"]),
    ("Vé tham quan Hải Vân Quan bao nhiêu?", ["Hải Vân Quan"]),
    ("Vé vào chùa Thiên Mụ bao nhiêu?", []),
    ("Bây giờ đi đâu chơi?", []),
])
def test_code_detects_point_names_in_question(cau, ten):
    assert [d["ten"] for d in vg.do_diem(BANG, cau)] == ten


def test_code_lookup_puts_rows_into_model_input(deps):
    seen = []
    gen = generator(lambda n, kw: (seen.append(json.dumps(kw["input"], ensure_ascii=False)), [answer("Có trong nguồn [1].")])[1])
    trace = AnswerTrace()
    asyncio.run(answer_turn("Vé vào Đại Nội bao nhiêu?", *deps, gen, trace, ON))
    assert f"Tiêu đề: {vg.TIEU_DE_NGUON}" in seen[0] and "200.000" in seen[0] and trace.ve_gio["diem"][0]["ten"] == "Đại Nội Huế"
