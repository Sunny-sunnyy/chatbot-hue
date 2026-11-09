"""Phase 9 T2 — công cụ `yeu_cau_tra_web` (plan `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` bản 2 §1.5). 0 USD, không gọi mạng:
Serper ghi sẵn (`serper()` của test B6), model là SDK thật với client kịch bản (test B2), Qdrant thật chỉ đọc (fixture `deps`). Không phải bằng chứng model
thật gọi công cụ đúng lúc (lượt đo có phí §2). Câu tự viết, không chép kho.
"""
import asyncio
import dataclasses
import json

import pytest

from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream, answer_turn_stream_parallel, web_gate_open
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER, ROUTER_INSTRUCTIONS, TU_WEB_LUAT, YEU_CAU_TRA_WEB_KQ, YEU_CAU_TRA_WEB_MO_TA
from llm.generator_openai_full_corpus import ASSISTANT_MAX_TURNS, max_turns_for
from test_b2_tool_loop import _ids, answer, deps, generator, tool_call  # noqa: F401  (fixture `deps`: Qdrant thật, chỉ đọc)
from test_b6_tra_web import serper

ON = AssistantFlags(router=True, tim_them=True, tra_web=True, tra_web_cong_cu=True)
OFF = AssistantFlags(router=True, tim_them=True, tra_web=True)
CAU = "Đại Nội mở cửa mấy giờ, gần đây có chương trình gì mới không?"
KHO = "Đại Nội mở cửa theo giờ ghi trong nguồn [1]."
WEB_TEXT = "Phòng tập A mở từ 5h sáng [w1]."


def web_call() -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "yeu_cau_tra_web", "arguments": "{}", "status": "completed"}


def tool_names(kw) -> list[str]:
    return [t["name"] for t in kw.get("tools") or []]


def script(steps, router_route="tro_ly_hue"):
    """Định tuyến ⇒ `router_route`; lần gọi mục web ⇒ `WEB_TEXT`; các lần gọi trợ lý ⇒ `steps` theo thứ tự (lần cuối lặp lại). Ghi kwargs lần gọi trợ lý."""
    seen = []

    def run(n, kw):
        instructions = kw.get("instructions") or ""
        if instructions == TU_WEB_LUAT:
            return [answer(WEB_TEXT)]
        if instructions.startswith(ROUTER_INSTRUCTIONS):
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": router_route}), "annotations": []}]}]
        seen.append(kw)
        return [steps[min(len(seen), len(steps)) - 1]()]
    run.seen = seen
    return run


def go(path, deps, steps, flags=ON, trace=None, calls=None):
    sc = script(steps)
    trace = trace or AnswerTrace()

    async def run():
        if path is answer_turn:
            await answer_turn(CAU, *deps, generator(sc), trace, flags, None, serper(calls=calls))
            return []
        return [e async for e in path(CAU, *deps, generator(sc), trace, flags, None, serper(calls=calls))]
    events = asyncio.run(run())
    return trace, events, sc.seen


PATHS = [(answer_turn, ON), (answer_turn_stream, ON), (answer_turn_stream_parallel, dataclasses.replace(ON, song_song_tra_loi=True))]
PATH_IDS = ["api_chat", "stream", "song_song_6"]


@pytest.mark.parametrize("path, flags", PATHS, ids=PATH_IDS)
@pytest.mark.parametrize("steps, mo", [
    ((web_call, lambda: answer(KHO)), True),                  # yêu cầu ∧ câu trả lời thường ⇒ mở
    ((web_call, lambda: answer(OUT_OF_SCOPE_ANSWER)), False),  # yêu cầu ∧ câu ngoài phạm vi ⇒ đóng
    ((lambda: answer(KHO),), False),                           # không yêu cầu ∧ câu thường ⇒ đóng (như B6)
    ((lambda: answer(INSUFFICIENT_ANSWER),), True),            # "không đủ thông tin" ⇒ mở như cũ (cổng B6)
], ids=["yeu_cau_thuong", "yeu_cau_ngoai_pham_vi", "khong_yeu_cau", "tu_choi_kho"])
def test_gate_four_cases_on_three_paths(deps, path, flags, steps, mo):
    calls = []
    trace, events, seen = go(path, deps, steps, flags, calls=calls)
    assert all("yeu_cau_tra_web" in tool_names(kw) for kw in seen)  # có công cụ ở mọi lần gọi trợ lý (cả phần chạy song song của #6)
    assert (trace.web is not None and trace.web["outcome"] == "co_muc") is mo and len(calls) == (1 if mo else 0)
    if mo and trace.answer != INSUFFICIENT_ANSWER:
        assert trace.answer == KHO and trace.cited  # câu kho giữ nguyên; mục web tách riêng
    if path is not answer_turn and mo:
        assert "".join(d for k, d in events if k == "delta") == trace.answer  # chữ web không đi qua `delta`


def test_tool_result_is_neutral_and_capped_once(deps):
    calls = []
    trace, _, seen = go(answer_turn, deps, (web_call, web_call, lambda: answer(KHO)), calls=calls)
    muc = [t for t in trace.tools if t["name"] == "yeu_cau_tra_web"]
    assert len(muc) == 2 and "het_luot" not in muc[0] and muc[1]["het_luot"] is True and trace.web_yeu_cau
    outputs = [i["output"] for kw in seen for i in kw["input"] if i.get("type") == "function_call_output"]
    assert outputs[-2:] == [YEU_CAU_TRA_WEB_KQ, YEU_CAU_TRA_WEB_KQ]  # câu cố định, không hứa mục web
    assert len(calls) == 1  # ≤ 1 lần Serper / câu


def test_composed_turn_has_no_tool_and_gate_stays_closed(deps):
    calls = []
    trace, _, seen = go(answer_turn, deps, (lambda: answer(KHO),), trace=AnswerTrace(truong={}), calls=calls)
    assert seen and all("yeu_cau_tra_web" not in tool_names(kw) for kw in seen)
    trace.web_yeu_cau = True  # kể cả khi cờ đã đặt, lượt ghép từ nút không mở
    assert not web_gate_open(trace, ON, serper()) and calls == []


@pytest.mark.parametrize("history", [(), (("Huế có món gì ngon?", ""),)], ids=["luot_dau", "co_lich_su"])
def test_request_per_turn_type(deps, history):
    sent = {}
    for name, flags in (("on", ON), ("off", OFF)):
        _, _, seen = go(answer_turn, deps, (lambda: answer(KHO),), flags, trace=AnswerTrace(history=history))
        sent[name] = seen[0]
    assert tool_names(sent["off"]) == ["tim_kho"] and tool_names(sent["on"]) == ["tim_kho", "yeu_cau_tra_web"]
    assert sent["on"]["instructions"] == sent["off"]["instructions"] and sent["on"]["input"] == sent["off"]["input"]
    mo_ta = next(t for t in sent["on"]["tools"] if t["name"] == "yeu_cau_tra_web")
    assert mo_ta["description"] == YEU_CAU_TRA_WEB_MO_TA and mo_ta["parameters"]["properties"] == {}  # không tham số


def test_worst_chain_does_not_hit_max_turns(deps):
    # review M-1: tìm, tìm, tìm ("hết lượt"), yêu cầu web, viết = 5 vòng; trần +1 khi có công cụ ⇒ không chạm
    steps = (lambda: tool_call("a"), lambda: tool_call("b"), lambda: tool_call("c"), web_call, lambda: answer(KHO))
    trace, _, seen = go(answer_turn, deps, steps)
    assert len(seen) == 5 and trace.fixed_outcome is None and trace.answer == KHO
    assert max_turns_for(None, object()) == ASSISTANT_MAX_TURNS + 1 and max_turns_for(object(), object()) == ASSISTANT_MAX_TURNS + 2
    assert max_turns_for(None) == ASSISTANT_MAX_TURNS


def test_flag_needs_tra_web_in_settings():
    with pytest.raises(ValueError):
        AssistantFlags.from_settings({"assistant": {"router": True, "tim_them": True, "tra_web_cong_cu": True}})
