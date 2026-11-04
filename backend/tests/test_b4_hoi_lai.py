"""B4 (plan bản 2 `42fa62d2425f`): công cụ `hoi_lai` + `StopAtTools` chạy qua SDK thật với client giả có kịch bản (không mạng — logic);
lọc D3, câu ghép D4, cờ tắt ⇒ yêu cầu như trước (Q1), lượt ghép không có `hoi_lai`, route `clarify` / 422 / log không giá trị."""
import asyncio
import dataclasses
import json

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import CACH_A_NOTE, HOI_LAI_NOTE
from llm.hoi_lai import TruongInput, ghep_cau, loc_truong
from test_api_chat import chat_log_records, metric_lines
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: F401  (fixture `deps` dùng chung)

TOOLS_ON = AssistantFlags(tim_them=True, hoi_lai=True)
TOOLS_OFF = AssistantFlags(tim_them=True)
QUESTION = "Hai đứa mình đi Huế thì hết khoảng bao nhiêu tiền?"


def hoi_lai_call(loai: str, truong: list[str]) -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "hoi_lai",
            "arguments": json.dumps({"loai": loai, "truong_thieu": truong}), "status": "completed"}


def tool_names(kwargs) -> list[str]:
    return [t["name"] for t in kwargs.get("tools", [])]


def test_loc_truong_keeps_boundary_and_reports_fill_or_cut():
    assert loc_truong("chi_phi", ["so_nguoi", "so_ngay", "di_cung", "so_ngay"]) == (["so_nguoi", "so_ngay"], [])  # bỏ trường sai loại + trùng
    assert loc_truong("lich_trinh", ["so_nguoi"]) == (["so_ngay"], ["dien"])  # rỗng sau lọc ⇒ trường bắt buộc
    assert loc_truong("lich_trinh", ["so_thich", "kieu_di", "di_cung", "so_ngay"]) == (["so_ngay", "di_cung", "kieu_di"], ["cat"])


def test_loc_truong_always_adds_missing_required_fields():
    # Plan B4 bản 5 D3 (C163 m-2): model chỉ hỏi trường không bắt buộc ⇒ code thêm trường bắt buộc, để thẻ không cho "Gửi" khi thiếu số ngày.
    assert loc_truong("lich_trinh", ["so_thich"]) == (["so_ngay", "so_thich"], ["dien"])
    assert loc_truong("chi_phi", ["so_ngay"]) == (["so_nguoi", "so_ngay"], ["dien"])
    assert loc_truong("chi_phi", ["muc_chi"]) == (["so_nguoi", "so_ngay", "muc_chi"], ["dien"])
    # vừa thêm vừa cắt (C166 m-2): 3 trường không bắt buộc + so_ngay ⇒ 4 ⇒ cắt trường cuối bảng; trường bắt buộc không bị cắt
    assert loc_truong("lich_trinh", ["di_cung", "kieu_di", "so_thich"]) == (["so_ngay", "di_cung", "kieu_di"], ["dien", "cat"])


def test_ghep_cau_is_deterministic_and_empty_means_original():
    truong = TruongInput(so_nguoi="2", so_ngay="2", muc_chi="tieu_chuan")
    assert ghep_cau(" Đi Huế hết bao nhiêu? ", truong) == "Đi Huế hết bao nhiêu? (Thông tin thêm: 2 ngày; 2 người; mức chi tiêu chuẩn.)"
    assert ghep_cau("Đi Huế hết bao nhiêu?", TruongInput()) == "Đi Huế hết bao nhiêu?"


def test_stop_at_hoi_lai_gives_clarify_without_answer(deps):
    gen = generator(lambda n, kw: [hoi_lai_call("chi_phi", ["so_nguoi", "so_ngay", "di_cung"])])
    trace = AnswerTrace()
    asyncio.run(answer_turn(QUESTION, *deps, gen, trace, TOOLS_ON))
    calls = gen.client.responses.calls
    assert len(calls) == 1  # dừng ngay ở `hoi_lai`, không lượt viết
    assert tool_names(calls[0]) == ["tim_kho", "hoi_lai"] and calls[0]["instructions"].endswith(HOI_LAI_NOTE)
    assert trace.fixed_outcome == "hoi_lai" and trace.answer == "" and trace.cited == ()
    assert [t["ten"] for t in trace.clarify["truong"]] == ["so_nguoi", "so_ngay"] and trace.clarify["cau_goc"] == QUESTION
    assert trace.hoi_lai_raw == {"loai": "chi_phi", "truong_thieu": ["so_nguoi", "so_ngay", "di_cung"]} and trace.hoi_lai_d3 == []
    assert trace.hoi_lai_offered  # ngân sách lượt này cộng HOI_LAI_TOOL_OVERHEAD


def test_stream_hoi_lai_has_no_searching_status_and_no_text(deps):
    gen = generator(lambda n, kw: [hoi_lai_call("lich_trinh", [])])
    trace = AnswerTrace()

    async def run():
        return [event async for event in answer_turn_stream(QUESTION, *deps, gen, trace, TOOLS_ON)]

    events = asyncio.run(run())
    assert ("status", {"stage": "searching"}) not in events and not [e for e in events if e[0] == "delta"]
    searched = [e for e in events if e[0] == "status" and e[1]["stage"] == "searched"]
    assert searched == [("status", {"stage": "searched", "n_sources": len(trace.packed.sources)})]  # chỉ lần tìm đầu của code (C163 m-1)
    assert trace.fixed_outcome == "hoi_lai" and [t["ten"] for t in trace.clarify["truong"]] == ["so_ngay"] and trace.hoi_lai_d3 == ["dien"]


@pytest.mark.parametrize("flags, da_co_truong", [(TOOLS_OFF, False), (TOOLS_ON, True)])
def test_no_hoi_lai_when_flag_off_or_turn_already_has_fields(deps, flags, da_co_truong):
    """Q1: cờ tắt ⇒ danh sách công cụ + lời dặn như B3; D4: lượt ghép / "Trả lời luôn" ⇒ không đưa `hoi_lai` (không hỏi lại lần hai)."""
    gen = generator(lambda n, kw: [answer("Vé vào Đại Nội 200.000 đồng [1].")])
    trace = AnswerTrace(da_co_truong=da_co_truong)
    asyncio.run(answer_turn(QUESTION, *deps, gen, trace, flags))
    kwargs = gen.client.responses.calls[0]
    assert tool_names(kwargs) == ["tim_kho"] and HOI_LAI_NOTE not in kwargs["instructions"]
    # cờ tắt ⇒ lời dặn y như B3 (Q1); lượt ghép khi cờ bật ⇒ thêm đúng câu Cách A (D7 khoá 2 — khoá 1 thiếu ⇒ câu chi phí ghép tự cộng tổng)
    expected = f"{gen.assistant_instructions}\n\n{CACH_A_NOTE}" if flags.hoi_lai else gen.assistant_instructions
    assert kwargs["instructions"] == expected and trace.clarify is None


def test_stream_composed_turn_sends_cach_a_without_hoi_lai(deps):
    """D7 khoá 2, đường stream: lượt ghép (đã có giá trị trường) khi cờ bật ⇒ lời dặn có Cách A, không công cụ `hoi_lai`."""
    gen = generator(lambda n, kw: [answer("Vé vào Đại Nội 200.000 đồng [1].")])
    trace = AnswerTrace(da_co_truong=True)

    async def run():
        return [event async for event in answer_turn_stream(QUESTION, *deps, gen, trace, TOOLS_ON)]

    asyncio.run(run())
    kwargs = gen.client.responses.calls[0]
    assert tool_names(kwargs) == ["tim_kho"] and kwargs["instructions"] == f"{gen.assistant_instructions}\n\n{CACH_A_NOTE}"


def test_route_clarify_then_composed_turn(deps, caplog):
    """`/api/chat`: lượt hỏi lại ⇒ `clarify`, không mã đánh giá, log chỉ số đếm; gửi `truong` ⇒ câu ghép tới model, không `hoi_lai`;
    giá trị lạ / trường lạ ⇒ 422."""
    script = lambda n, kw: [hoi_lai_call("chi_phi", ["so_nguoi", "so_ngay"])] if "hoi_lai" in tool_names(kw) else [answer("Vé 200.000 đồng [1].")]  # noqa: E731
    app = create_app()
    with TestClient(app) as client:
        gen = generator(script)
        original = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        app.state.generator, app.state.generator_ready = gen, True
        app.state.assistant_flags = dataclasses.replace(app.state.assistant_flags, hoi_lai=True, router=False)
        with chat_log_records(caplog) as records:
            asked = client.post("/api/chat", json={"query": QUESTION})
            composed = client.post("/api/chat", json={"query": QUESTION, "truong": {"so_nguoi": "2", "so_ngay": "2"}})
        bad_value = client.post("/api/chat", json={"query": QUESTION, "truong": {"so_nguoi": "7"}})
        bad_field = client.post("/api/chat", json={"query": QUESTION, "truong": {"ten_toi": "Lan"}})
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = original
    body = asked.json()
    assert asked.status_code == 200 and body["answer"] == "" and body["turn_id"] is None
    assert [t["ten"] for t in body["clarify"]["truong"]] == ["so_nguoi", "so_ngay"]
    sent = json.dumps(gen.client.responses.calls[-1]["input"], ensure_ascii=False)
    assert composed.status_code == 200 and "Thông tin thêm: 2 ngày; 2 người." in sent and "hoi_lai" not in tool_names(gen.client.responses.calls[-1])
    assert gen.client.responses.calls[-1]["instructions"].endswith(CACH_A_NOTE)  # D7 khoá 2: lượt ghép có Cách A
    assert bad_value.status_code == 422 and bad_field.status_code == 422
    first, second = metric_lines(records)
    assert first["outcome"] == "hoi_lai" and first["hoi_lai"] == {"loai": "chi_phi", "n": 2, "d3": []} and first["co_truong"] is None
    assert second["outcome"] == "success" and second["co_truong"] == 2 and second["hoi_lai"] is None


def test_stream_route_sends_clarify_event_and_done_without_turn_id():
    import time
    from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents
    from llm.hoi_lai import the_hoi_lai
    from test_chat_stream import parse_sse

    clarify = the_hoi_lai("lich_trinh", ["so_ngay"], QUESTION)
    stream = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter(), lambda: "C" * 16)
    events = parse_sse(stream.fixed(AnswerTrace(answer="", cited=(), fixed_outcome="hoi_lai", clarify=clarify)))
    assert events == [("clarify", clarify), ("done", {"outcome": "hoi_lai"})]


def test_hoi_lai_tool_overhead_counts_only_on_tool_path():
    # A quyết (a) 04/11: lược đồ `hoi_lai` = hằng 185 token, chỉ cộng ở đường trợ lý có công cụ; đường sinh một lần (B1) đếm như cũ.
    from retrieval.full_corpus_context import HOI_LAI_TOOL_OVERHEAD, FullCorpusContextBuilder

    class Words:
        def encode(self, text):
            return text.split()

    b = FullCorpusContextBuilder(Words())
    base = b._token_count("câu hỏi", "ngữ cảnh", None, "lời dặn")
    assert b._token_count("câu hỏi", "ngữ cảnh", None, "lời dặn", extra_tool_tokens=HOI_LAI_TOOL_OVERHEAD) == base + 185
    assert b._token_count("câu hỏi", "ngữ cảnh", extra_tool_tokens=HOI_LAI_TOOL_OVERHEAD) == b._token_count("câu hỏi", "ngữ cảnh")
