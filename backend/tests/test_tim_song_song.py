"""Tìm thêm song song (plan `docs/superpowers/plans/2026-11-15-toc-do-tim-song-song-plan.md`, 86d295b16017) — 0 USD.
Model là `OpenAIResponsesModel` thật của SDK, client trả phản hồi dựng sẵn (như `test_het_luot_tim.py`); tìm kho là Qdrant thật (chỉ đọc).
Đây không phải bằng chứng model thật có gọi song song hay không — phần đó đo có phí."""
import asyncio
import json
import re

from llm.assistant import MODEL_SEARCH_LIMIT, AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401  (fixture `deps` dùng chung)
from test_het_luot_tim import CAU, sent_requests

OFF = AssistantFlags(tim_them=True, het_luot_bo_cong_cu=True)
ON = AssistantFlags(tim_them=True, het_luot_bo_cong_cu=True, tim_song_song=True)


def hai_cung_luc(n, kw):
    return [tool_call("bún bò Huế"), tool_call("cơm hến Huế")] if n == 1 else [answer(INSUFFICIENT_ANSWER)]


def _chay(deps, script, flags, stream=False):
    gen, trace = generator(script), AnswerTrace()
    if stream:
        async def hết():
            async for _ in answer_turn_stream(CAU, *deps, gen, trace, flags):
                pass
        asyncio.run(hết())
    else:
        asyncio.run(answer_turn(CAU, *deps, gen, trace, flags))
    return trace, gen


def test_flag_off_request_unchanged_and_on_only_sets_parallel(deps):
    """Cờ tắt ⇒ yêu cầu gửi model như trước (`parallel_tool_calls: false`); bật ⇒ chỉ khoá đó đổi."""
    script = lambda n, kw: [tool_call("câu tìm 1")] if n == 1 else [answer(INSUFFICIENT_ANSWER)]
    _, g0 = _chay(deps, script, AssistantFlags(tim_them=True, het_luot_bo_cong_cu=True))
    _, g_off = _chay(deps, script, OFF)
    _, g_on = _chay(deps, script, ON)
    assert sent_requests(g_off) == sent_requests(g0)
    assert [kw.get("parallel_tool_calls") for kw in g_off.client.responses.calls] == [False, False]
    assert [kw.get("parallel_tool_calls") for kw in g_on.client.responses.calls] == [True, True]
    assert sent_requests(g_on).replace('"parallel_tool_calls": true', '"parallel_tool_calls": false') == sent_requests(g_off)


def test_two_searches_in_one_call_save_a_model_call_and_sources_match(deps):
    """Hai `tim_kho` trong MỘT phản hồi ⇒ cả hai tìm thật, model viết ở lần gọi thứ 2 (nối tiếp thì 3). Số nguồn liền nhau, không trùng đoạn,
    mỗi `[Nguồn k]` trong kết quả công cụ gửi lại model trỏ đúng nguồn có cùng tiêu đề trong sổ nguồn (thứ tự có thể theo lần tìm xong trước)."""
    for stream in (False, True):
        trace, gen = _chay(deps, hai_cung_luc, ON, stream)
        assert trace.model_searches == MODEL_SEARCH_LIMIT and len(gen.client.responses.calls) == 2, stream
        ids = [s.id for s in trace.so_nguon]
        assert ids == list(range(1, len(ids) + 1)), stream
        tra_ve = [it["output"] for it in gen.client.responses.calls[1]["input"] if isinstance(it, dict) and it.get("type") == "function_call_output"]
        assert len(tra_ve) == 2
        theo_id = {s.id: s.title for s in trace.so_nguon}
        for out in tra_ve:
            for k, tieu_de in re.findall(r"\[Nguồn (\d+)\]\nTiêu đề: ([^\n]+)", out):
                assert theo_id[int(k)] == tieu_de, (stream, k)


def test_three_in_one_call_third_is_blocked(deps):
    """Trần đếm trước `await` ⇒ lần thứ 3 trong cùng phản hồi vẫn bị chặn: được đếm (`model_searches` đếm cả lần xin), không tìm thật, nhận chữ hết lượt."""
    script = lambda n, kw: [tool_call("a Huế"), tool_call("b Huế"), tool_call("c Huế")] if n == 1 else [answer(INSUFFICIENT_ANSWER)]
    trace, _ = _chay(deps, script, ON)
    assert trace.model_searches == MODEL_SEARCH_LIMIT + 1
    tim = [t for t in trace.tools if t.get("name") == "tim_kho" and t.get("by") == "model"]
    assert sum(not t.get("het_luot") for t in tim) == MODEL_SEARCH_LIMIT and sum(bool(t.get("het_luot")) for t in tim) == 1
