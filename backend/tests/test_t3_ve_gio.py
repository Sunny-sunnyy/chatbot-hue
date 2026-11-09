"""T3 hướng (a) — bảng vé + giờ chỉ để kiểm số sau khi model viết (User 09/11/2026; spec Phase 9 §12.2 phương án B) — 0 USD.

Bảng thật (`data/phase_9/t3_bang_ve_gio/bang_v1.json`, private — clone không có ⇒ skip); SDK thật + client kịch bản (không mạng) + Qdrant thật (đọc)
như `test_b5b_thoi_tiet.py`. Đây **không** là bằng chứng model thật viết đúng giá / giờ — phần đó ở lượt có phí (Q2 + bộ an toàn 32)."""
import asyncio
import dataclasses
import json
from pathlib import Path

import pytest

from core.settings_loader import BACKEND_DIR, load_settings
from llm import ve_gio as vg
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream, answer_turn_stream_parallel, chu_cua_model
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER, ROUTER_INSTRUCTIONS
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: F401  (fixture `deps`: Qdrant thật, chỉ đọc)

SETTINGS = load_settings(validate_private_paths=False)
BANG_PATH = BACKEND_DIR / SETTINGS["assistant"]["tra_ve_gio_bang"]
if not BANG_PATH.exists():
    pytest.skip("bảng vé / giờ private không có (clone public)", allow_module_level=True)
BANG = vg.nap_bang(BANG_PATH)
ON = AssistantFlags(tim_them=True, tra_ve_gio=True, bang_ve_gio=BANG)
OFF = AssistantFlags(tim_them=True)
AN_TOAN = Path(__file__).resolve().parents[2] / "data/loi_nang_2026-10-28/an_toan/questions.jsonl"
CAU_VE = "Vé vào Đại Nội bao nhiêu?"


# ---------- bảng + dò tên ----------

def test_table_loads_and_flag_off_does_not_read_it():
    assert len(BANG.diem) == 60 and all(d["nhom"] != "su_kien" for d in BANG.diem)  # User 08/11 câu 2: bỏ sự kiện đã diễn ra
    s = json.loads(json.dumps(SETTINGS))
    s["assistant"]["tra_ve_gio"] = False
    s["assistant"]["tra_ve_gio_bang"] = "../khong_co_file.json"
    assert AssistantFlags.from_settings(s).bang_ve_gio is None  # cờ tắt ⇒ không đọc file (clone public chạy được)


@pytest.mark.parametrize("cau, ten", [
    (CAU_VE, ["Đại Nội Huế"]),
    ("Giá vé lăng Tự Đức và lăng Khải Định?", ["Lăng vua Tự Đức", "Lăng vua Khải Định"]),
    ("Khiêm Lăng mở cửa mấy giờ?", ["Lăng vua Tự Đức"]),
    ("Vé vào chùa Thiên Mụ bao nhiêu?", []),
    ("Bây giờ đi đâu chơi?", []),
])
def test_code_detects_point_names_in_question(cau, ten):
    assert [d["ten"] for d in vg.do_diem(BANG, cau)] == ten


def test_table_rows_of_a_point_are_allowed_numbers():
    dai_noi = vg.do_diem(BANG, CAU_VE)[0]
    assert "200.000" in vg.chu_cua_diem(dai_noi)
    assert vg.kiem_so("Vé người lớn vào Đại Nội là 200.000 đồng.", vg.chu_cua_diem(dai_noi)) == []


# ---------- cổng từ khoá ----------

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


# ---------- kiểm số ----------

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


# ---------- nối vào lõi ----------

def kich_ban(text, route="tro_ly_hue", seen=None):
    """Định tuyến (nhận bằng lời dặn) ⇒ `route`; trợ lý viết `text` ngay. `seen` ghi (lời dặn, công cụ, tin nhắn) mỗi lần gọi trợ lý."""
    def script(n, kw):
        if str(kw.get("instructions", "")).startswith(ROUTER_INSTRUCTIONS[:80]):
            return [{"type": "message", "id": f"msg_{next(_ids)}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": route}), "annotations": []}]}]
        if seen is not None:
            seen.append(json.dumps({k: kw.get(k) for k in ("instructions", "tools", "input")}, ensure_ascii=False, sort_keys=True, default=str))
        return [answer(text)]
    return script


def chay(deps, duong, text, flags=ON, query=CAU_VE, seen=None):
    gen, trace = generator(kich_ban(text, seen=seen)), AnswerTrace()
    f = dataclasses.replace(flags, router=True, song_song_tra_loi=True) if duong == "song_song" else flags

    async def go():
        if duong == "chat":
            await answer_turn(query, *deps, gen, trace, f)
            return []
        fn = answer_turn_stream if duong == "stream" else answer_turn_stream_parallel
        return [e async for e in fn(query, *deps, gen, trace, f)]
    return trace, asyncio.run(go())


def test_flag_on_sends_model_the_same_request_as_flag_off(deps):
    """Hướng (a): bảng không vào model ⇒ lời dặn + công cụ + tin nhắn giống hệt khi cờ tắt (khác: chỉ phần code làm sau lần sinh)."""
    on, off = [], []
    chay(deps, "chat", "Vé người lớn là 200.000 đồng [1].", ON, seen=on)
    chay(deps, "chat", "Vé người lớn là 200.000 đồng [1].", OFF, seen=off)
    assert on and on == off


@pytest.mark.parametrize("duong", ["chat", "stream", "song_song"])
def test_odd_price_gets_fixed_note_and_answer_is_kept_on_all_three_paths(deps, duong):
    ok, ev_ok = chay(deps, duong, "Vé người lớn vào Đại Nội là 200.000 đồng [1].")
    assert ok.ve_gio_kiem == [] and ok.ve_gio_noi is None and ok.citation_error is None
    assert [t for t in ok.tools if t["name"] == "kiem_ve_gio"] == [{"name": "kiem_ve_gio", "ms": 0.0, "n_diem": 1, "loi": []}]
    la, ev_la = chay(deps, duong, "Vé người lớn vào Đại Nội là 987.000 đồng, mở cửa lúc 4h15 [1].")
    assert la.ve_gio_kiem == ["tien_ngoai_bang", "gio_ngoai_bang"] and la.citation_error is None  # không rút lại — chỉ nối câu cố định
    assert la.ve_gio_noi == vg.CAU_CO_THE_KHAC and la.answer.endswith(f"\n\n{vg.CAU_CO_THE_KHAC}")
    assert vg.CAU_CO_THE_KHAC not in chu_cua_model(la)
    if duong != "chat":
        assert "".join(d for kind, d in ev_ok if kind == "delta") == ok.answer
        assert "".join(d for kind, d in ev_la if kind == "delta") == la.answer


@pytest.mark.parametrize("text, query", [
    (INSUFFICIENT_ANSWER, CAU_VE),                                   # câu từ chối ⇒ không kiểm, không nối
    (OUT_OF_SCOPE_ANSWER, CAU_VE),                                   # câu ngoài phạm vi ⇒ không nối (G: code đặt outcome riêng)
    ("Lăng có kiến trúc đẹp, mở từ năm 1999 lúc 4h15 [1].", "Lăng Tự Đức có gì đẹp?"),  # không từ khoá vé / giờ ⇒ không kiểm
])
def test_no_check_on_refusals_or_questions_without_ticket_words(deps, text, query):
    trace, _ = chay(deps, "chat", text, query=query)
    assert trace.ve_gio_kiem is None and trace.ve_gio_noi is None and not any(t["name"] == "kiem_ve_gio" for t in trace.tools)


def test_flag_off_never_checks(deps):
    trace, _ = chay(deps, "chat", "Vé người lớn vào Đại Nội là 987.000 đồng [1].", OFF)
    assert trace.ve_gio_kiem is None and vg.CAU_CO_THE_KHAC not in trace.answer
