"""Phase 9 bậc G — cổng 2 nhóm (plan `docs/superpowers/plans/2026-11-08-phase-9-g-cong-plan.md` bản 2 §4.1) — 0 USD.

Chuỗi gửi model theo mỗi loại lượt (4c): lời dặn agent có câu ngoài phạm vi ở lượt đầu / có lịch sử; định tuyến 2 nhãn; lượt biểu mẫu giữ lời dặn
cũ **giống byte**. Câu ngoài phạm vi do agent viết (M-1): outcome `out_of_scope` ở cả 3 đường, chữ phát đúng một lần, cổng web đóng, không nối
khối thời tiết; sự kiện `done` không có `tu_choi_kho`. SDK thật + client giả có kịch bản (không mạng) + Qdrant thật (đọc).
"""
import asyncio
import dataclasses
import hashlib
import time

from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents
from llm.assistant import (AnswerTrace, AssistantFlags, _finish_generated, answer_turn, answer_turn_stream, answer_turn_stream_parallel,
                           web_gate_open)
from llm.full_corpus_prompt import (ANSWER_BIEU_MAU_INSTRUCTIONS, ANSWER_SYSTEM_INSTRUCTIONS, LICH_TRINH_LUAT, OUT_OF_SCOPE_ANSWER,
                                    ROUTER_INSTRUCTIONS)
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from test_chat_stream import parse_sse
from test_toc_do_song_song import ON, QUERY, Client, TimedResponses, collect, deps  # noqa: F401  (fixture `deps` dùng chung)

OFF = dataclasses.replace(ON, song_song_tra_loi=False)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def test_prompts_per_turn_type():
    gen = OpenAIFullCorpusGenerator(client=Client(TimedResponses("tro_ly_hue", 0, 0)), model="probe")
    for instructions in (gen.answer_agent.instructions, gen.assistant_instructions, gen.assistant_history_instructions):
        assert OUT_OF_SCOPE_ANSWER in instructions and "vẫn là câu về Huế" in instructions  # lượt đầu / có công cụ / có lịch sử
    assert ANSWER_SYSTEM_INSTRUCTIONS in gen.assistant_instructions and ANSWER_SYSTEM_INSTRUCTIONS in gen.assistant_history_instructions
    for router in (gen.router_agent.instructions, gen.router_history_agent.instructions):
        assert router.startswith(ROUTER_INSTRUCTIONS) and "khan_cap" not in router and "ngoai_pham_vi" not in router
    # lượt biểu mẫu: lời dặn trước bậc G giống byte (A quyết M-4 — Q-F / V5 đo trên bản này)
    assert gen.bieu_mau_agent.instructions == f"{ANSWER_BIEU_MAU_INSTRUCTIONS}\n\n{LICH_TRINH_LUAT}"
    assert _sha(ANSWER_BIEU_MAU_INSTRUCTIONS) == "81d3040cf53f" and OUT_OF_SCOPE_ANSWER not in ANSWER_BIEU_MAU_INSTRUCTIONS


def _run(deps, fn, flags, answer_text):
    responses = TimedResponses(route="tro_ly_hue", router_delay=0.2, answer_delay=0, answer_text=answer_text)
    gen = OpenAIFullCorpusGenerator(client=Client(responses), model="probe")

    async def go():
        trace = AnswerTrace()
        if fn is answer_turn:
            await answer_turn(QUERY, *deps, gen, trace, flags, tim_web=_no_web)
            return trace, []
        return trace, [e async for e in fn(QUERY, *deps, gen, trace, flags, tim_web=_no_web)]
    return asyncio.run(go())


async def _no_web(cau):  # cổng web mở là lỗi của test (không có câu từ chối "không đủ thông tin")
    raise AssertionError("cổng web không được mở với câu ngoài phạm vi")


def test_out_of_scope_from_agent_on_all_three_paths(deps):
    flags = dataclasses.replace(ON, tra_web=True)
    trace, _ = _run(deps, answer_turn, flags, OUT_OF_SCOPE_ANSWER)  # `/api/chat`
    assert trace.fixed_outcome == "out_of_scope" and trace.answer == OUT_OF_SCOPE_ANSWER and trace.web is None
    for fn, path_flags in ((answer_turn_stream, dataclasses.replace(OFF, tra_web=True)), (answer_turn_stream_parallel, flags)):  # stream thường, #6
        trace, events, _ = collect(deps, fn, path_flags, route="tro_ly_hue", router_delay=0.2, answer_delay=0, answer_text=OUT_OF_SCOPE_ANSWER)
        assert "".join(d for k, d, _ in events if k == "delta") == OUT_OF_SCOPE_ANSWER  # đúng một lần
        assert trace.fixed_outcome == "out_of_scope" and trace.cited == () and trace.citation_error is None
        assert not web_gate_open(trace, path_flags, _no_web)
    assert trace.n_tra_loi_bo == 0  # #6: phần đã chạy được giữ (không bỏ như tuyến ngoài phạm vi cũ)


def test_out_of_scope_done_event():
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    trace = AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=(), fixed_outcome="out_of_scope")
    events = parse_sse([stream.delta(OUT_OF_SCOPE_ANSWER), *stream.fixed(trace)])
    assert events[-1][0] == "done" and events[-1][1]["outcome"] == "out_of_scope" and "tu_choi_kho" not in events[-1][1]
    assert metrics["outcome"] == "out_of_scope" and metrics["refusal"] is True and metrics["delta_matches_final"] is True


def test_out_of_scope_skips_weather_block():
    # câu ngoài phạm vi có từ "thời tiết" ⇒ có dự báo trong trace, nhưng code không nối khối số liệu sau câu cố định
    flags = AssistantFlags(tim_them=True, thoi_tiet=True, du_bao=lambda: None)
    trace = AnswerTrace(generated=type("G", (), {"text": OUT_OF_SCOPE_ANSWER})())
    trace.thoi_tiet = {"khoi": "Dự báo Huế: …"}
    _finish_generated(trace, flags)
    assert trace.fixed_outcome == "out_of_scope" and trace.answer == OUT_OF_SCOPE_ANSWER and not getattr(trace, "thoi_tiet_noi", None)
