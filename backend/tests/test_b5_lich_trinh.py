"""Phase 9 B5 (plan `docs/superpowers/plans/2026-11-03-phase-9-b5-plan.md` bản 7 `b572443dc9cd`) — 0 USD.

Phần thuần (bảng thật `data/phase_9/lich_trinh/diem_v3.json`, private): luật khớp tên, xếp, **mỗi luật xếp một test cố tình vi phạm** (#5),
kiểm cuối D8 từng mục một ca vi phạm, dò số ngày, bộ nhận tiền. Phần nối: SDK thật + client giả có kịch bản (không mạng) + Qdrant thật (đọc) —
chuỗi gửi model theo **mỗi loại lượt** (W55 4c), code tự hỏi số ngày (D15), "Trả lời luôn" ⇒ 0 hỏi lần hai, thứ tự dòng tiến độ (D14).
Thay `test_b4_hoi_lai.py` (công cụ `hoi_lai` đã gỡ — C183 m-2); phần còn dùng của B4 (thẻ, câu ghép, `TruongInput`) chuyển sang đây.
Đây **không** là bằng chứng model thật gọi công cụ đúng lúc — phần đó ở lượt có phí.
"""
import asyncio
import copy
import dataclasses
import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api.app import create_app
from core.settings_loader import load_settings
from llm import lich_trinh as lt
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream, nap_bang_lich
from llm.do_so import do_so_ngay
from llm.hoi_lai import TruongInput, ghep_cau, the_hoi_lai
from llm.so_tien import tim_so_tien
from retrieval.full_corpus_context import LICH_TRINH_TOOL_OVERHEAD, FullCorpusContextBuilder
from test_api_chat import chat_log_records, metric_lines
from test_b2_tool_loop import _ids, answer, deps, generator, tool_call  # noqa: F401  (fixture `deps` dùng chung)
from test_chat_stream import parse_sse

SETTINGS = load_settings(validate_private_paths=False)
BANG = nap_bang_lich(SETTINGS)
ON = AssistantFlags(tim_them=True, lich_trinh=True, bang_lich=BANG)
OFF = AssistantFlags(tim_them=True)
CAU = "Lên lịch đi Huế giúp mình nhé"


def lich_call(**args) -> dict:
    n = next(_ids)
    full = {"so_ngay": None, "di_cung": None, "kieu_di": None, "so_thich": None, "them_diem": None, **args}
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "lich_trinh",
            "arguments": json.dumps(full, ensure_ascii=False), "status": "completed"}


def tool_names(kwargs) -> list[str]:
    return [t["name"] for t in kwargs.get("tools", [])]


def last_tool_output(kwargs) -> str:
    return next(item["output"] for item in reversed(kwargs["input"]) if item.get("type") == "function_call_output")


def viet_theo_khung(kwargs) -> str:
    """Model giả "đúng luật": mỗi dòng khung ⇒ một dòng lời có tên điểm + [n] của điểm (để kiểm cuối D8 qua)."""
    dong = re.findall(r"^- (Sáng|Chiều|Tối): (.+?)(?: ◦)? \[(\d+)\]", last_tool_output(kwargs), re.M)
    return "\n".join(f"{buoi}: ghé {ten} — điểm đáng xem [{n}]." for buoi, ten, n in dong)


def khung(**ts) -> dict:
    return lt.xep(BANG, lt.ThamSo(**{"so_ngay": "2", **ts}))


# ---------- bảng + luật khớp tên (D2) ----------

def test_bang_loads_and_rejects_duplicate_name_key(tmp_path):
    assert len(BANG.diem) == 28 and all(lt.khop_diem(BANG, d["ten"]) == d["id"] for d in BANG.diem)
    raw = json.loads((Path(__file__).resolve().parents[1] / SETTINGS["assistant"]["lich_trinh_bang"]).read_text(encoding="utf-8"))
    raw["diem"][1]["ten_khac"] = raw["diem"][1]["ten_khac"] + [raw["diem"][0]["ten"]]  # khoá trỏ hai điểm ⇒ không khởi động
    bad = tmp_path / "bang.json"
    bad.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="trùng"):
        lt.nap_bang(bad)


def test_name_match_rule():
    assert lt.khop_diem(BANG, "đại nội") == lt.khop_diem(BANG, "Đại Nội Huế") == "dai_noi"  # hậu tố " Huế" (còn ≥ 2 chữ)
    assert lt.khop_diem(BANG, "Hiếu Lăng") == "lang_minh_mang"  # bí danh `ten_khac`
    assert lt.khop_diem(BANG, "Lycée Khải Định") is None and lt.khop_diem(BANG, "Khải Định") is None  # nguyên tên, không chuỗi con
    assert lt.khop_diem(BANG, "chùa Từ Hiếu") is None  # ngoài bảng


# ---------- xếp (D2–D5) trên bảng thật: khung đúng thật qua `kiem_khung` = 0 lỗi ----------

@pytest.mark.parametrize("ts", [
    {}, {"so_ngay": "1", "so_thich": "di_tich", "kieu_di": "thong_tha"}, {"so_thich": "am_thuc", "di_cung": "cap_doi"},
    {"so_ngay": "3", "di_cung": "nguoi_lon_tuoi"}, {"so_ngay": "4+", "so_thich": "thien_nhien", "kieu_di": "day_lich"},
    {"so_ngay": "3", "di_cung": "gia_dinh_tre_em", "so_thich": "am_thuc"}, {"so_thich": "chup_anh", "them_diem": ("Thác Nhị Hồ",)},
    {"so_ngay": "1", "so_thich": "le_hoi_nghe_thuat", "di_cung": "nhom_ban"},
])
def test_real_frames_pass_rule_check(ts):
    k = khung(**ts)
    assert lt.kiem_khung(BANG, k) == [] and lt.diem_trong_khung(k)
    nguon = {i: n for n, i in enumerate(lt.diem_trong_khung(k), 1)}
    assert lt.kiem_ghi_chu(BANG, k, lt.khoi_ghi_chu(BANG, k, nguon)) == []


def test_branches_of_the_plan():
    elderly = khung(so_ngay="3", di_cung="nguoi_lon_tuoi", them_diem=("Phố đi bộ Nguyễn Đình Chiểu",))
    assert {"diem": "Phố đi bộ Nguyễn Đình Chiểu", "ma_luat": "khong_buoi_hop_le"} in elderly["khong_xep"]  # D2b: phố đêm + người lớn tuổi
    assert all(not ng["buoi"]["toi"] and sum(len(v) for v in ng["buoi"].values()) <= 2 for ng in elderly["ngay"])  # D4
    one = khung(so_ngay="1", them_diem=("chùa Từ Hiếu",))
    assert one["khong_xep"] == [{"diem": "chùa Từ Hiếu", "ma_luat": "ngoai_bang"}]
    far = [BANG.theo_id[i]["cum"] for i in lt.diem_trong_khung(khung(so_ngay="2", so_thich="thien_nhien"))]
    assert "nam_xa" not in far  # D3: 2 ngày, không nêu ⇒ không cụm xa
    asked = lt.diem_trong_khung(khung(so_ngay="1", them_diem=("Vườn quốc gia Bạch Mã",)))
    assert "bach_ma" in asked  # nêu tên ⇒ xếp dù < 3 ngày
    food = khung(so_thich="am_thuc")
    assert food["ngoai_so_thich"] and food["thieu_so_thich"] is not None  # D2 #2: lấp có nhãn + câu cố định
    note = lt.khoi_ghi_chu(BANG, food, {i: 1 for i in lt.diem_trong_khung(food)})
    assert "đánh dấu ◦" in note and lt.CAU_GIA_DINH["kieu_di"] in note
    assert khung(so_ngay="4+")["gia_dinh"][0] == "so_ngay_4" and len(khung(so_ngay="4+")["ngay"]) == 4


# ---------- mỗi luật xếp một test cố tình vi phạm (#5) ----------

def frame(ngay: list[dict], **ts) -> dict:
    base = {"so_ngay": str(len(ngay)), "di_cung": None, "kieu_di": None, "so_thich": None, "them_diem": [], "so_ngay_tam": False}
    return {"tham_so": {**base, **ts}, "ngay": [{"ngay": i, "buoi": {"sang": [], "chieu": [], "toi": [], **b}} for i, b in enumerate(ngay, 1)],
            "ngoai_so_thich": [], "thieu_so_thich": None, "khong_xep": [], "gia_dinh": []}


@pytest.mark.parametrize("bad, code", [
    (frame([{"sang": ["dai_noi"], "chieu": ["lang_tu_duc"], "toi": ["pho_tay"]}]), "qua_2_cum"),
    (frame([{"sang": ["dai_noi"], "chieu": ["lang_minh_mang"]}]), "cum_khong_ke"),
    (frame([{"sang": ["pho_tay"]}]), "buoi_ngoai_buoi"),
    (frame([{"sang": ["bach_ma"]}, {"sang": ["dai_noi"]}]), "nam_xa"),
    (frame([{"sang": ["dai_noi", "kinh_thanh"]}], kieu_di="thong_tha"), "qua_day_buoi"),
    (frame([{"sang": ["lang_thieu_tri", "lang_tu_duc"]}], kieu_di="day_lich"), "day_lich_sai"),  # có điểm nửa buổi
    (frame([{"sang": ["lang_thieu_tri", "dai_noi"]}], kieu_di="day_lich"), "day_lich_sai"),  # khác cụm
    (frame([{"sang": ["dai_noi"], "chieu": ["kinh_thanh"], "toi": ["cho_dong_ba"]}], di_cung="nguoi_lon_tuoi"), "han_che_qua_day"),
    (frame([{"sang": ["dai_noi"]}], them_diem=["Lăng Tự Đức"]), "them_diem_lac"),
    (frame([{"sang": ["dai_noi"]}], so_thich="am_thuc"), "lap_khong_nhan"),
    (frame([{"sang": ["dai_noi"]}], so_ngay="2"), "so_ngay"),
])
def test_rule_check_catches_each_violation(bad, code):
    assert code in lt.kiem_khung(BANG, bad)


def test_note_check_catches_missing_flood_warning():
    k = khung(so_thich="chup_anh", them_diem=("Thác Nhị Hồ",))
    nguon = {i: 1 for i in lt.diem_trong_khung(k)}
    full = lt.khoi_ghi_chu(BANG, k, nguon)
    assert lt.kiem_ghi_chu(BANG, k, full) == []
    broken = "\n".join(d for d in full.splitlines() if "mùa mưa lũ" not in d)  # D3: Thác Nhị Hồ thiếu câu mùa lũ
    assert lt.kiem_ghi_chu(BANG, k, broken) == ["ghi_chu_thieu"]


# ---------- kiểm cuối D8: mỗi mục một ca vi phạm + một lời đúng ----------

def test_final_check_each_item():
    k = khung(so_ngay="1", so_thich="di_tich", kieu_di="thong_tha")
    nguon = {"dai_noi": 3, "kinh_thanh": 4}
    ok = "Sáng: Đại Nội Huế, nên đi lúc 07h00 [3].\nChiều: Kinh thành Huế (Ngọ Môn – Kỳ Đài) [4]."
    assert lt.kiem_cuoi(BANG, ok, k, nguon) == []
    assert lt.kiem_cuoi(BANG, ok + "\nTối: Phố đi bộ Nguyễn Đình Chiểu [4].", k, nguon) == ["diem_ngoai_khung"]  # (1)
    assert "gio_ngoai_khung" in lt.kiem_cuoi(BANG, ok.replace("07h00", "6h30"), k, nguon)  # (2) giờ ngoài khung
    for gio in ("6 giờ", "5:45", "8h", "5 giờ 30"):
        assert "gio_ngoai_khung" in lt.kiem_cuoi(BANG, ok + f" Mở {gio}.", k, nguon)
    assert "thoi_luong" in lt.kiem_cuoi(BANG, ok + " Mất khoảng 2 tiếng.", k, nguon)  # (2) thời lượng
    for tien in ("50.000đ", "1,5 triệu", "200k", "200.000 VNĐ"):
        assert "gia" in lt.kiem_cuoi(BANG, ok + f" Vé {tien}.", k, nguon)  # (3)
    assert "thieu_trich_dan" in lt.kiem_cuoi(BANG, ok.replace("[4]", "[3]"), k, nguon)  # (4) [n] của điểm khác
    assert "thieu_trich_dan" in lt.kiem_cuoi(BANG, ok.splitlines()[0], k, nguon)  # (4) bớt điểm
    assert "url" in lt.kiem_cuoi(BANG, ok + " https://example.org", k, nguon)  # (6)
    viet_tu_lich = "Ngày 1\nSáng: Đại Nội Huế [1]\nNgày 2\nSáng: Lăng Tự Đức [2]"
    assert lt.co_dang_lich(viet_tu_lich) and lt.kiem_cuoi(BANG, viet_tu_lich, None) == ["diem_ngoai_khung"]  # (7) không gọi công cụ


@pytest.mark.parametrize("text, found", [
    ("vé 50.000đ", True), ("50.000 đ", True), ("1,5 triệu", True), ("200k", True), ("200.000 VNĐ", True), ("300 nghìn", True),
    ("đi 3N2Đ", False), ("hơn 1 nghìn năm", False), ("127 bậc", False), ("mở 7h00", False),
])
def test_money_detector(text, found):
    assert bool(tim_so_tien(text)) is found


@pytest.mark.parametrize("text, so_ngay", [
    ("đi Huế 2 ngày", "2"), ("ba ngày hai đêm", "3"), ("3N2Đ cho 1 người", "3"), ("đi 5 ngày", "4+"),
    ("đi 3 ngày, ngày thứ 2 nghỉ", "3"), ("đi 3 ngày hay 4 ngày", None), ("cả nhà đi cuối tuần", None), ("mỗi ngày đi đâu", None),
])
def test_day_count_detector(text, so_ngay):
    assert do_so_ngay(text) == so_ngay


def test_day_count_resolution_d15():
    assert lt.chot_so_ngay({}, None, CAU) == ("1", True)  # "Trả lời luôn" ⇒ 1 ngày tạm, không hỏi lần hai
    assert lt.chot_so_ngay({"so_ngay": "3"}, "1", CAU) == ("3", False)  # nút thắng
    assert lt.chot_so_ngay(None, "1", "đi Huế 3 ngày") == (None, False)  # dò số lệch tham số ⇒ hỏi
    assert lt.chot_so_ngay(None, None, "đi Huế 3 ngày") == ("3", False)
    assert lt.chot_so_ngay(None, None, CAU) == (None, False)  # thiếu ⇒ hỏi
    assert lt.chot_so_ngay(None, "2", CAU) == ("2", False)


def test_map_link_is_built_by_code():
    assert lt.map_url("Đại Nội Huế") == "https://www.google.com/maps/search/?api=1&query=%C4%90%E1%BA%A1i%20N%E1%BB%99i%20Hu%E1%BA%BF%2C%20Hu%E1%BA%BF"


# ---------- phần còn dùng của B4 (thẻ, câu ghép, trường) ----------

def test_composed_question_and_fields():
    truong = TruongInput(so_ngay="2", di_cung="cap_doi", kieu_di="thong_tha")
    assert ghep_cau(" Xếp lịch đi Huế giúp mình ", truong) == "Xếp lịch đi Huế giúp mình (Thông tin thêm: 2 ngày; đi hai người (cặp đôi); đi thong thả.)"
    assert ghep_cau("Xếp lịch đi Huế giúp mình", TruongInput()) == "Xếp lịch đi Huế giúp mình"
    for field in ({"so_nguoi": "2"}, {"muc_chi": "tieu_chuan"}, {"so_ngay": "7"}):
        with pytest.raises(ValidationError):
            TruongInput(**field)


def test_stream_route_sends_clarify_event_and_done_without_turn_id():
    import time
    from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents

    clarify = the_hoi_lai("lich_trinh", ["so_ngay"], CAU)
    stream = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter(), lambda: "C" * 16)
    events = parse_sse(stream.fixed(AnswerTrace(answer="", cited=(), fixed_outcome="hoi_lai", clarify=clarify)))
    assert events == [("clarify", clarify), ("done", {"outcome": "hoi_lai"})]


def test_tool_overhead_counts_only_on_tool_path():
    class Words:
        def encode(self, text):
            return text.split()

    b = FullCorpusContextBuilder(Words())
    base = b._token_count("câu hỏi", "ngữ cảnh", None, "lời dặn")
    assert b._token_count("câu hỏi", "ngữ cảnh", None, "lời dặn", extra_tool_tokens=LICH_TRINH_TOOL_OVERHEAD) == base + LICH_TRINH_TOOL_OVERHEAD
    assert b._token_count("câu hỏi", "ngữ cảnh", extra_tool_tokens=LICH_TRINH_TOOL_OVERHEAD) == b._token_count("câu hỏi", "ngữ cảnh")


# ---------- nối vào lõi: SDK thật + client giả ----------

def run(deps, query, gen, flags, trace=None, stream=False):
    trace = trace or AnswerTrace()

    async def go():
        if stream:
            return [e async for e in answer_turn_stream(query, *deps, gen, trace, flags)]
        await answer_turn(query, *deps, gen, trace, flags)

    return trace, asyncio.run(go())


# W55 (4c): mỗi loại lượt — cờ bật chỉ thêm đúng một mục công cụ `lich_trinh`; lời dặn hệ thống giống hệt cờ tắt (D7, Q1m mức test).
@pytest.mark.parametrize("history", [(), (("Huế có món gì ngon?", ""),)])
@pytest.mark.parametrize("truong", [None, {}, {"so_ngay": "2"}])
@pytest.mark.parametrize("stream", [False, True])
def test_request_per_turn_type_only_adds_one_tool(deps, history, truong, stream):
    sent = {}
    for name, flags in (("on", ON), ("off", OFF)):
        gen = generator(lambda n, kw: [answer("Đại Nội mở cửa từ 7 giờ [1].")])
        run(deps, CAU, gen, flags, AnswerTrace(history=history, truong=truong), stream)
        sent[name] = gen.client.responses.calls[0]
    assert tool_names(sent["off"]) == ["tim_kho"] and tool_names(sent["on"]) == ["tim_kho", "lich_trinh"]
    assert sent["on"]["instructions"] == sent["off"]["instructions"] and sent["on"]["input"] == sent["off"]["input"]
    schema = json.dumps(next(t for t in sent["on"]["tools"] if t["name"] == "lich_trinh"), ensure_ascii=False)
    assert all(d["ten"] not in schema for d in BANG.diem)  # ý #12: mô tả / lược đồ không dùng tên điểm thật


def test_code_asks_only_days_when_missing(deps):
    gen = generator(lambda n, kw: [lich_call(so_thich="di_tich")])
    trace, _ = run(deps, CAU, gen, ON)
    assert len(gen.client.responses.calls) == 1  # thẻ ⇒ dừng lượt (tool_use_behavior hàm), không lượt viết
    assert trace.fixed_outcome == "hoi_lai" and [t["ten"] for t in trace.clarify["truong"]] == ["so_ngay"] and trace.clarify["cau_goc"] == CAU
    assert trace.lich is None and trace.answer == ""


def test_detected_day_count_mismatch_asks(deps):
    gen = generator(lambda n, kw: [lich_call(so_ngay="1")])
    trace, _ = run(deps, "Lên lịch đi Huế 3 ngày giúp mình", gen, ON)
    assert trace.fixed_outcome == "hoi_lai"  # D12 (b): câu nói 3 ngày, model gửi 1 ⇒ hỏi lại


def test_answer_now_never_asks_twice_and_marks_one_day(deps):
    gen = generator(lambda n, kw: [lich_call()] if n == 1 else [answer(viet_theo_khung(kw))])
    trace, _ = run(deps, CAU, gen, ON, AnswerTrace(truong={}, search_query=CAU))
    assert trace.clarify is None and trace.citation_error is None and trace.lich_kiem == []
    k = trace.lich["khung"]
    assert k["tham_so"]["so_ngay"] == "1" and k["tham_so"]["so_ngay_tam"] and len(k["ngay"]) == 1
    assert trace.answer.startswith("Mình hiểu: 1 ngày (tạm)") and lt.CAU_GIA_DINH["so_ngay_tam"] in trace.answer


def test_full_itinerary_turn_stream_order_and_text(deps):
    script = lambda n, kw: [lich_call(so_ngay="1", so_thich="di_tich", them_diem=["chùa Từ Hiếu"])] if n == 1 else [answer(viet_theo_khung(kw))]  # noqa: E731
    trace, events = run(deps, "Lên lịch Huế 1 ngày, mình thích di tích", generator(script), ON, stream=True)
    statuses = [d for kind, d in events if kind == "status"]
    i = statuses.index({"stage": "lich_trinh", "buoc": "dang_xep"})
    after = [s.get("buoc") for s in statuses[i:] if s["stage"] == "lich_trinh"]
    assert after[:3] == ["dang_xep", "xep_xong", "kiem_luat_ok"] and after[-1] == "lay_nguon" and "bo_diem" in after  # D14 thứ tự việc code
    j = next(k for k, s in enumerate(statuses) if s.get("buoc") == "xep_xong")
    assert not [s for s in statuses[i:j] if s["stage"] in ("searching", "searched")]  # m-6
    text = "".join(d for kind, d in events if kind == "delta")
    assert trace.citation_error is None and text == trace.answer and text.startswith("Mình hiểu: 1 ngày")
    assert lt.TIEU_DE_GHI_CHU in text and "chùa Từ Hiếu" in text  # khối D4b có dòng `khong_xep`
    assert {b["buoc"] for b in trace.buoc_lich if b["buoc"] == "kiem_luat_ok"} and trace.lich["nguon"]


def test_search_twice_then_itinerary_within_turn_limit(deps):
    # D1 (bản 5 m-4): `tim_kho` ×2 + `lich_trinh` + lượt viết = 4 lần gọi = trần `max_turns` 4 ⇒ ghi rõ kết quả
    script = lambda n, kw: [tool_call("a")] if n <= 2 else ([lich_call(so_ngay="1")] if n == 3 else [answer(viet_theo_khung(kw))])  # noqa: E731
    trace, _ = run(deps, CAU, generator(script), ON)
    assert trace.fixed_outcome is None and trace.lich is not None  # vừa đủ trần: ra lời (lần gọi thứ 5 mới chạm)


def test_self_written_itinerary_without_tool_is_retracted(deps):
    gen = generator(lambda n, kw: [answer("Ngày 1\nSáng: Đại Nội Huế [1]\nNgày 2\nSáng: Lăng Tự Đức [1]")])
    trace, _ = run(deps, CAU, gen, ON)
    assert trace.citation_error is not None and trace.lich_kiem == ["diem_ngoai_khung"]  # D8 (7)
    trace_off, _ = run(deps, CAU, generator(lambda n, kw: [answer("Ngày 1\nSáng: Đại Nội Huế [1]\nNgày 2\nSáng: Lăng Tự Đức [1]")]), OFF)
    assert trace_off.citation_error is None  # cờ tắt ⇒ như `main`


def test_route_clarify_then_answer_now(deps, caplog):
    script = lambda n, kw: [lich_call()] if "lich_trinh" in tool_names(kw) and not any(  # noqa: E731
        i.get("type") == "function_call_output" for i in kw["input"]) else [answer(viet_theo_khung(kw))]
    app = create_app()
    with TestClient(app) as client:
        original = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        app.state.generator, app.state.generator_ready = generator(script), True
        app.state.assistant_flags = dataclasses.replace(ON, router=False)
        with chat_log_records(caplog) as records:
            asked = client.post("/api/chat", json={"query": CAU})
            now = client.post("/api/chat", json={"query": CAU, "truong": {}})
        cost_field = client.post("/api/chat", json={"query": CAU, "truong": {"so_nguoi": "2"}})
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = original
    assert asked.json()["clarify"]["truong"][0]["ten"] == "so_ngay" and asked.json()["answer"] == ""
    body = now.json()
    assert now.status_code == 200 and body["clarify"] is None and body["answer"].startswith("Mình hiểu: 1 ngày (tạm)")
    assert body["lich_trinh"]["ban_do"] and all(b["map_url"].startswith(lt.MAP_BASE) for b in body["lich_trinh"]["ban_do"])
    assert body["lich_trinh"]["sua"]["chon"] == {} and body["lich_trinh"]["sua"]["cau_goc"] == CAU  # "1 ngày (tạm)" không chọn sẵn
    assert cost_field.status_code == 422
    first, second = metric_lines(records)
    assert first["outcome"] == "hoi_lai" and first["hoi_lai"] == {"loai": "lich_trinh", "n": 1}
    assert second["lich_trinh_ok"] is True and second["lich_trinh_buoc"][:2] == ["xep_xong", "kiem_luat_ok"] and second["co_truong"] == 0
    assert CAU not in json.dumps(first, ensure_ascii=False) + json.dumps(second, ensure_ascii=False)  # log chỉ số đếm


def test_flags_need_table_and_tool_loop():
    with pytest.raises(ValueError):
        AssistantFlags(tim_them=True, lich_trinh=True)
    with pytest.raises(ValueError):
        AssistantFlags(lich_trinh=True, bang_lich=BANG)
    s = copy.deepcopy(SETTINGS)
    s["assistant"]["lich_trinh"] = True
    assert AssistantFlags.from_settings(s).bang_lich is not None and AssistantFlags.from_settings(SETTINGS).bang_lich is None
