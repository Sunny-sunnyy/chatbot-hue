"""B4 (plan bản 2 `42fa62d2425f`): công cụ `hoi_lai` + `StopAtTools` chạy qua SDK thật với client giả có kịch bản (không mạng — logic);
lọc D3, câu ghép D4, cờ tắt ⇒ yêu cầu như trước (Q1), lượt ghép không có `hoi_lai`, route `clarify` / 422 / log không giá trị."""
import asyncio
import dataclasses
import json

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import HOI_LAI_NOTE
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
    assert loc_truong("chi_phi", ["so_ngay", "di_cung", "so_ngay"]) == (["so_ngay"], None)  # bỏ trường sai loại + trùng
    assert loc_truong("lich_trinh", ["so_nguoi"]) == (["so_ngay"], "dien")  # rỗng sau lọc ⇒ trường bắt buộc
    assert loc_truong("lich_trinh", ["so_thich", "kieu_di", "di_cung", "so_ngay"]) == (["so_ngay", "di_cung", "kieu_di"], "cat")


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
    assert trace.hoi_lai_raw == {"loai": "chi_phi", "truong_thieu": ["so_nguoi", "so_ngay", "di_cung"]} and trace.hoi_lai_d3 is None


def test_stream_hoi_lai_has_no_searching_status_and_no_text(deps):
    gen = generator(lambda n, kw: [hoi_lai_call("lich_trinh", [])])
    trace = AnswerTrace()

    async def run():
        return [event async for event in answer_turn_stream(QUESTION, *deps, gen, trace, TOOLS_ON)]

    events = asyncio.run(run())
    assert ("status", {"stage": "searching"}) not in events and not [e for e in events if e[0] == "delta"]
    searched = [e for e in events if e[0] == "status" and e[1]["stage"] == "searched"]
    assert searched == [("status", {"stage": "searched", "n_sources": len(trace.packed.sources)})]  # chỉ lần tìm đầu của code (C163 m-1)
    assert trace.fixed_outcome == "hoi_lai" and [t["ten"] for t in trace.clarify["truong"]] == ["so_ngay"] and trace.hoi_lai_d3 == "dien"


@pytest.mark.parametrize("flags, da_co_truong", [(TOOLS_OFF, False), (TOOLS_ON, True)])
def test_no_hoi_lai_when_flag_off_or_turn_already_has_fields(deps, flags, da_co_truong):
    """Q1: cờ tắt ⇒ danh sách công cụ + lời dặn như B3; D4: lượt ghép / "Trả lời luôn" ⇒ không đưa `hoi_lai` (không hỏi lại lần hai)."""
    gen = generator(lambda n, kw: [answer("Vé vào Đại Nội 200.000 đồng [1].")])
    trace = AnswerTrace(da_co_truong=da_co_truong)
    asyncio.run(answer_turn(QUESTION, *deps, gen, trace, flags))
    kwargs = gen.client.responses.calls[0]
    assert tool_names(kwargs) == ["tim_kho"] and HOI_LAI_NOTE not in kwargs["instructions"]
    assert kwargs["instructions"] == gen.assistant_instructions and trace.clarify is None


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
    assert bad_value.status_code == 422 and bad_field.status_code == 422
    first, second = metric_lines(records)
    assert first["outcome"] == "hoi_lai" and first["hoi_lai"] == {"loai": "chi_phi", "n": 2, "d3": None} and first["co_truong"] is None
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
