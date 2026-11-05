"""B4 (plan bản 2 `42fa62d2425f`; B4b bản 8 `69afbb2732cf` — chỉ lịch trình, bỏ Cách A): công cụ `hoi_lai` + `StopAtTools` chạy qua SDK thật với client giả có kịch bản (không mạng — logic);
lọc D3, câu ghép D4, cờ tắt ⇒ yêu cầu như trước (Q1), lượt ghép không có `hoi_lai`, route `clarify` / 422 / log không giá trị."""
import asyncio
import dataclasses
import json

import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient

from api.app import create_app
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import HOI_LAI_NOTE
from llm.hoi_lai import TruongInput, ghep_cau, loc_truong
from test_api_chat import chat_log_records, metric_lines
from test_b2_tool_loop import _ids, answer, deps, generator  # noqa: F401  (fixture `deps` dùng chung)

TOOLS_ON = AssistantFlags(tim_them=True, hoi_lai=True)
TOOLS_OFF = AssistantFlags(tim_them=True)
QUESTION = "Mình muốn đi Huế, xếp giúp mình lịch trình nhé"
HISTORY = (("Huế có món gì ngon?", ""),)


def hoi_lai_call(loai: str, truong: list[str]) -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "hoi_lai",
            "arguments": json.dumps({"loai": loai, "truong_thieu": truong}), "status": "completed"}


def tool_names(kwargs) -> list[str]:
    return [t["name"] for t in kwargs.get("tools", [])]


def test_loc_truong_keeps_boundary_and_reports_fill_or_cut():
    assert loc_truong("lich_trinh", ["so_ngay", "so_nguoi", "di_cung", "so_ngay"]) == (["so_ngay", "di_cung"], [])  # bỏ trường lạ + trùng
    assert loc_truong("lich_trinh", ["so_nguoi"]) == (["so_ngay"], ["dien"])  # rỗng sau lọc ⇒ trường bắt buộc
    assert loc_truong("lich_trinh", ["so_thich", "kieu_di", "di_cung", "so_ngay"]) == (["so_ngay", "di_cung", "kieu_di"], ["cat"])


def test_loc_truong_always_adds_missing_required_fields():
    # Plan B4 bản 5 D3 (C163 m-2): model chỉ hỏi trường không bắt buộc ⇒ code thêm trường bắt buộc, để thẻ không cho "Gửi" khi thiếu số ngày.
    assert loc_truong("lich_trinh", ["so_thich"]) == (["so_ngay", "so_thich"], ["dien"])
    # vừa thêm vừa cắt (C166 m-2): 3 trường không bắt buộc + so_ngay ⇒ 4 ⇒ cắt trường cuối bảng; trường bắt buộc không bị cắt
    assert loc_truong("lich_trinh", ["di_cung", "kieu_di", "so_thich"]) == (["so_ngay", "di_cung", "kieu_di"], ["dien", "cat"])


def test_ghep_cau_is_deterministic_and_empty_means_original():
    truong = TruongInput(so_ngay="2", di_cung="cap_doi", kieu_di="thong_tha")
    assert ghep_cau(" Xếp lịch đi Huế giúp mình ", truong) == "Xếp lịch đi Huế giúp mình (Thông tin thêm: 2 ngày; đi hai người (cặp đôi); đi thong thả.)"
    assert ghep_cau("Xếp lịch đi Huế giúp mình", TruongInput()) == "Xếp lịch đi Huế giúp mình"


@pytest.mark.parametrize("field", [{"so_nguoi": "2"}, {"muc_chi": "tieu_chuan"}])
def test_cost_fields_are_gone(field):
    # B4b D2′: trường chi phí không còn — trình duyệt gửi lên ⇒ lỗi kiểm (route trả 422)
    with pytest.raises(ValidationError):
        TruongInput(**field)


def test_stop_at_hoi_lai_gives_clarify_without_answer(deps):
    gen = generator(lambda n, kw: [hoi_lai_call("lich_trinh", ["so_ngay", "so_thich"])])
    trace = AnswerTrace()
    asyncio.run(answer_turn(QUESTION, *deps, gen, trace, TOOLS_ON))
    calls = gen.client.responses.calls
    assert len(calls) == 1  # dừng ngay ở `hoi_lai`, không lượt viết
    assert tool_names(calls[0]) == ["tim_kho", "hoi_lai"] and calls[0]["instructions"] == f"{gen.assistant_instructions}\n\n{HOI_LAI_NOTE}"
    schema = json.dumps(next(t for t in calls[0]["tools"] if t["name"] == "hoi_lai")["parameters"], ensure_ascii=False)
    assert '"lich_trinh"' in schema and "chi_phi" not in schema and "so_nguoi" not in schema and "muc_chi" not in schema  # D2′: enum chỉ lịch trình
    assert trace.fixed_outcome == "hoi_lai" and trace.answer == "" and trace.cited == ()
    assert [t["ten"] for t in trace.clarify["truong"]] == ["so_ngay", "so_thich"] and trace.clarify["cau_goc"] == QUESTION
    assert trace.hoi_lai_raw == {"loai": "lich_trinh", "truong_thieu": ["so_ngay", "so_thich"]} and trace.hoi_lai_d3 == []
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


# W36 (4c), B4b D7′: mỗi loại lượt khi cờ bật — chuỗi lời dặn + danh sách công cụ gửi model đúng như plan bản 8.
#   lượt đầu / lượt có lịch sử chưa có trường ⇒ lời dặn gốc (± câu dặn lịch sử) + HOI_LAI_NOTE, có công cụ `hoi_lai`;
#   lượt ghép / "Trả lời luôn" (đã có trường, kể cả `{}`) và cờ tắt ⇒ lời dặn **đúng như `main`**, chỉ `tim_kho` (không còn Cách A).
@pytest.mark.parametrize("flags, da_co_truong, history, offer", [
    (TOOLS_OFF, False, (), False), (TOOLS_OFF, False, HISTORY, False),  # cờ tắt (Q1)
    (TOOLS_ON, False, (), True), (TOOLS_ON, False, HISTORY, True),     # lượt đầu / lượt có lịch sử
    (TOOLS_ON, True, (), False), (TOOLS_ON, True, HISTORY, False),     # lượt ghép / "Trả lời luôn"
])
@pytest.mark.parametrize("stream", [False, True])
def test_instructions_and_tools_per_turn_type(deps, flags, da_co_truong, history, offer, stream):
    gen = generator(lambda n, kw: [answer("Đại Nội mở cửa từ 7 giờ [1].")])
    trace = AnswerTrace(da_co_truong=da_co_truong, history=history)

    async def run():
        if stream:
            return [event async for event in answer_turn_stream(QUESTION, *deps, gen, trace, flags)]
        await answer_turn(QUESTION, *deps, gen, trace, flags)

    asyncio.run(run())
    kwargs = gen.client.responses.calls[0]
    base = gen.assistant_history_instructions if history else gen.assistant_instructions
    assert kwargs["instructions"] == (f"{base}\n\n{HOI_LAI_NOTE}" if offer else base)
    assert tool_names(kwargs) == (["tim_kho", "hoi_lai"] if offer else ["tim_kho"]) and trace.clarify is None


def test_route_clarify_then_composed_turn(deps, caplog):
    """`/api/chat`: lượt hỏi lại ⇒ `clarify`, không mã đánh giá, log chỉ số đếm; gửi `truong` ⇒ câu ghép tới model, không `hoi_lai`;
    giá trị lạ / trường lạ ⇒ 422."""
    script = lambda n, kw: [hoi_lai_call("lich_trinh", ["so_ngay", "kieu_di"])] if "hoi_lai" in tool_names(kw) else [answer("Đại Nội mở cửa từ 7 giờ [1].")]  # noqa: E731
    app = create_app()
    with TestClient(app) as client:
        gen = generator(script)
        original = app.state.generator, app.state.generator_ready, app.state.assistant_flags
        app.state.generator, app.state.generator_ready = gen, True
        app.state.assistant_flags = dataclasses.replace(app.state.assistant_flags, hoi_lai=True, router=False)
        with chat_log_records(caplog) as records:
            asked = client.post("/api/chat", json={"query": QUESTION})
            composed = client.post("/api/chat", json={"query": QUESTION, "truong": {"so_ngay": "2", "kieu_di": "thong_tha"}})
        bad_value = client.post("/api/chat", json={"query": QUESTION, "truong": {"so_ngay": "7"}})
        bad_field = client.post("/api/chat", json={"query": QUESTION, "truong": {"ten_toi": "Lan"}})
        cost_field = client.post("/api/chat", json={"query": QUESTION, "truong": {"so_nguoi": "2"}})  # D2′: trường chi phí đã bỏ
        app.state.generator, app.state.generator_ready, app.state.assistant_flags = original
    body = asked.json()
    assert asked.status_code == 200 and body["answer"] == "" and body["turn_id"] is None
    assert [t["ten"] for t in body["clarify"]["truong"]] == ["so_ngay", "kieu_di"]
    sent = json.dumps(gen.client.responses.calls[-1]["input"], ensure_ascii=False)
    assert composed.status_code == 200 and "Thông tin thêm: 2 ngày; đi thong thả." in sent and "hoi_lai" not in tool_names(gen.client.responses.calls[-1])
    assert gen.client.responses.calls[-1]["instructions"] in (gen.assistant_instructions, gen.assistant_history_instructions)  # D7′: như `main`
    assert bad_value.status_code == 422 and bad_field.status_code == 422 and cost_field.status_code == 422
    first, second = metric_lines(records)
    assert first["outcome"] == "hoi_lai" and first["hoi_lai"] == {"loai": "lich_trinh", "n": 2, "d3": []} and first["co_truong"] is None
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
