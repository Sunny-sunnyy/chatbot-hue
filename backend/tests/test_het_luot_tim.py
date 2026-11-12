"""Hết lượt tìm thì dừng (plan `docs/superpowers/plans/2026-11-12-het-luot-tim-plan.md` §2, §3 "test theo loại lượt") — 0 USD.

Cờ `assistant.het_luot_bo_cong_cu` bật: sau `MODEL_SEARCH_LIMIT` lần model tìm thật, lượt gọi model kế tiếp KHÔNG gửi công cụ `tim_kho`.
Model là `OpenAIResponsesModel` thật của SDK với client trả phản hồi dựng sẵn (như `test_b2_tool_loop.py`); tìm kho là Qdrant thật (chỉ đọc).
Test tự đặt cờ (không đọc cờ này từ `settings.yaml` thật). Đây không phải bằng chứng model thật viết gì khi mất công cụ — phần đó đo có phí.
"""
import asyncio
import copy
import json

import pytest

from llm.assistant import MODEL_SEARCH_LIMIT, AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, TOOL_LIMIT_TEXT
from llm.generator_openai_full_corpus import GenerationError
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401  (fixture `deps` dùng chung)
from test_cong_dot_1 import SETTINGS, form_trace, run, viet_theo_khung

OFF = AssistantFlags(tim_them=True)
ON = AssistantFlags(tim_them=True, het_luot_bo_cong_cu=True)
CAU = "Huế có món gì ngon?"


def tools_sent(gen) -> list[list[str]]:
    """Tên công cụ gửi model ở từng lần gọi của lượt."""
    return [[t.get("name") for t in kw.get("tools") or []] for kw in gen.client.responses.calls]


def searches_then_answer(n_searches: int):
    return lambda n, kw: [tool_call(f"câu tìm {n}")] if n <= n_searches else [answer(INSUFFICIENT_ANSWER)]


def turn(deps, script, flags, history=()) -> tuple[AnswerTrace, object]:
    gen, trace = generator(script), AnswerTrace(history=history)
    asyncio.run(answer_turn(CAU, *deps, gen, trace, flags))
    return trace, gen


def sent_requests(gen) -> str:
    """Thân yêu cầu gửi model của cả lượt, bỏ `call_id` / id mục (bộ đếm dùng chung của test tăng dần giữa hai lượt)."""
    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items() if k not in ("call_id", "id")}
        return [clean(x) for x in o] if isinstance(o, list) else o
    return json.dumps(clean([{k: v for k, v in kw.items() if k != "extra_headers"} for kw in gen.client.responses.calls]), ensure_ascii=False, sort_keys=True, default=str)


def test_flag_default_off_and_in_settings_off():
    assert AssistantFlags().het_luot_bo_cong_cu is False and SETTINGS["assistant"]["het_luot_bo_cong_cu"] is False


def test_after_two_real_searches_next_call_has_no_search_tool(deps):
    """Lượt đầu · sau 1 lần tìm · sau 2 lần tìm: `tim_kho` có · có · KHÔNG; model viết ngay ở lần gọi thứ 3 (cờ tắt: phải 4 lần gọi)."""
    trace, gen = turn(deps, searches_then_answer(2), ON)
    assert [("tim_kho" in names) for names in tools_sent(gen)] == [True, True, False]
    assert trace.model_searches == MODEL_SEARCH_LIMIT == 2 and len(trace.llm_calls) == 3
    assert not any(t.get("het_luot") for t in trace.tools)  # không còn lượt xin thứ ba bị chặn
    assert trace.fixed_outcome is None and trace.answer == INSUFFICIENT_ANSWER

    trace_off, gen_off = turn(deps, searches_then_answer(3), OFF)  # hành vi cũ: lần xin thứ 3 nhận chữ "đã hết lượt", viết ở lần gọi thứ 4
    assert [("tim_kho" in names) for names in tools_sent(gen_off)] == [True] * 4 and len(trace_off.llm_calls) == 4
    assert any(isinstance(i, dict) and i.get("output") == TOOL_LIMIT_TEXT for i in gen_off.client.responses.calls[3]["input"])


def test_turns_with_zero_or_one_search_send_the_same_bytes_as_flag_off(deps):
    """Câu không tìm thêm / tìm thêm 1 lần: cờ bật gửi model đúng từng byte như cờ tắt (plan §2)."""
    for n_searches in (0, 1):
        _, gen_on = turn(deps, searches_then_answer(n_searches), ON)
        _, gen_off = turn(deps, searches_then_answer(n_searches), OFF)
        assert sent_requests(gen_on) == sent_requests(gen_off), n_searches
    # sau 2 lần tìm: mọi lần gọi TRƯỚC lần thứ ba cũng giống byte; lần thứ ba chỉ khác ở danh sách công cụ
    _, gen_on = turn(deps, searches_then_answer(2), ON)
    _, gen_off = turn(deps, searches_then_answer(2), OFF)
    on, off = json.loads(sent_requests(gen_on)), json.loads(sent_requests(gen_off))
    assert on[:2] == off[:2]
    assert {k: v for k, v in on[2].items() if k != "tools"} == {k: v for k, v in off[2].items() if k != "tools"}
    assert "tim_kho" in json.dumps(off[2].get("tools")) and "tim_kho" not in json.dumps(on[2].get("tools"))


def test_turn_with_history_also_drops_the_tool_after_two_searches(deps):
    trace, gen = turn(deps, searches_then_answer(2), ON, history=(("Đại Nội mở cửa mấy giờ?", ""),))
    assert [("tim_kho" in names) for names in tools_sent(gen)] == [True, True, False] and len(trace.llm_calls) == 3


def test_model_asking_for_the_hidden_tool_gets_fixed_refusal_not_an_error(deps):
    """Ca xấu (probe 12/11): model vẫn xin `tim_kho` ở lượt công cụ đã ẩn ⇒ SDK ném lỗi ⇒ câu từ chối cố định như chạm `max_turns`, không lỗi 500."""
    always_tool = lambda n, kw: [tool_call(f"câu tìm {n}")]  # noqa: E731
    trace, gen = turn(deps, always_tool, ON)
    assert trace.fixed_outcome == "max_turns" and trace.answer == INSUFFICIENT_ANSWER and trace.cited == ()
    assert trace.model_searches == 2 and len(gen.client.responses.calls) == 3

    async def collect():
        trace = AnswerTrace()
        events = [e async for e in answer_turn_stream(CAU, *deps, generator(always_tool), trace, ON)]
        return trace, events

    trace, events = asyncio.run(collect())
    assert trace.fixed_outcome == "max_turns" and [data for kind, data in events if kind == "delta"] == [INSUFFICIENT_ANSWER]


def test_other_model_errors_still_raise_when_tool_is_still_offered(deps):
    """Chỉ đúng ca "xin công cụ đã ẩn" mới thành câu từ chối: model gọi một công cụ không tồn tại khi `tim_kho` còn ⇒ vẫn là lỗi."""
    def script(n, kw):
        call = tool_call("x")
        return [{**call, "name": "cong_cu_la"}]

    with pytest.raises(GenerationError):
        turn(deps, script, ON)


def test_form_turn_is_unchanged_by_the_flag(deps):
    """Lượt biểu mẫu "Lên kế hoạch": không có vòng công cụ ⇒ cờ bật / tắt gửi model giống byte, 1 lần gọi, 0 công cụ."""
    sent = {}
    for name, value in (("on", True), ("off", False)):
        s = copy.deepcopy(SETTINGS)
        s["assistant"].update(lich_trinh_bieu_mau=True, het_luot_bo_cong_cu=value)
        gen = generator(lambda n, kw: [answer(viet_theo_khung(kw))])
        query, trace = form_trace({"so_ngay": "2", "di_cung": "cap_doi"})
        run(deps, query, gen, AssistantFlags.from_settings(s), trace)
        assert tools_sent(gen) == [[]] and trace.clarify is None
        sent[name] = sent_requests(gen)
    assert sent["on"] == sent["off"]
