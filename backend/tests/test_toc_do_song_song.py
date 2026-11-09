"""Thí nghiệm tốc độ #6 (plan `docs/superpowers/plans/2026-11-04-phase-9-toc-do-song-song-plan.md`, tiêu chí T + Q1 mức đơn vị):
phần `tro_ly_hue` chạy cùng lúc định tuyến, sự kiện giữ tới khi có tuyến. Đường tìm thật (Qdrant chỉ đọc, e5 local); model thay bằng client
trả lời theo kịch bản có độ trễ cho trước — **không** phải bằng chứng hành vi model, chỉ kiểm thứ tự / giữ / bỏ / gộp của code."""
import asyncio
import dataclasses
import itertools
import json

import pytest
from openai.types.responses import Response, ResponseCompletedEvent, ResponseCreatedEvent, ResponseTextDeltaEvent

from core.settings_loader import load_settings
from evaluation.full_corpus_eval import build_context_builder, build_retrieval
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn_stream, answer_turn_stream_parallel
from llm.full_corpus_prompt import OUT_OF_SCOPE_ANSWER, ROUTER_INSTRUCTIONS
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator

ON = AssistantFlags(router=True, tim_them=True, song_song_tra_loi=True)
OFF = dataclasses.replace(ON, song_song_tra_loi=False)
QUERY = "Giá vé tham quan Đại Nội Huế là bao nhiêu?"
USAGE = {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120,
         "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 0}}
_ids = itertools.count(1)


def message(payload: dict) -> dict:
    return {"type": "message", "id": f"msg_{next(_ids)}", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": json.dumps(payload, ensure_ascii=False), "annotations": []}]}


class TimedResponses:
    """Định tuyến (nhận ra bằng lời dặn) trả `route` sau `router_delay`; lần gọi khác (trợ lý / trò chuyện) trả câu có `[1]` sau `answer_delay`.
    Ghi kwargs mọi lần gọi + thời điểm định tuyến xong."""

    def __init__(self, route, router_delay, answer_delay, answer_fails=False):
        self.route, self.router_delay, self.answer_delay, self.answer_fails = route, router_delay, answer_delay, answer_fails
        self.calls, self.router_done = [], False

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        is_router = str(kwargs.get("instructions", "")).startswith(ROUTER_INSTRUCTIONS[:80])
        await asyncio.sleep(self.router_delay if is_router else self.answer_delay)
        if is_router:
            self.router_done = True
            output = [message({"route": self.route})]
        else:
            if self.answer_fails:
                raise RuntimeError("lần trả lời lỗi")
            output = [message({"answer": "Vé Đại Nội có trong bảng giá [1]."})]
        response = Response.model_validate({"id": f"resp_{next(_ids)}", "created_at": 0, "model": "probe", "object": "response",
                                            "output": output, "parallel_tool_calls": False, "tool_choice": "auto", "tools": [],
                                            "usage": USAGE, "status": "completed"})
        if not kwargs.get("stream"):
            return response

        async def events():
            yield ResponseCreatedEvent.model_validate({"type": "response.created", "response": response.model_dump(), "sequence_number": 0})
            yield ResponseTextDeltaEvent.model_validate({"type": "response.output_text.delta", "item_id": output[0]["id"], "output_index": 0,
                                                         "content_index": 0, "delta": output[0]["content"][0]["text"],
                                                         "sequence_number": 1, "logprobs": []})
            yield ResponseCompletedEvent.model_validate({"type": "response.completed", "response": response.model_dump(), "sequence_number": 2})
        return events()


class Client:
    def __init__(self, responses):
        self.responses = responses

    async def close(self):
        return None


@pytest.fixture(scope="module")
def deps():
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    yield service, build_context_builder(settings)
    service.close()


def collect(deps, fn, flags, **script):
    """Chạy một lượt stream; ghi mỗi sự kiện kèm "định tuyến đã xong chưa" lúc sự kiện ra."""
    responses = TimedResponses(**script)
    gen = OpenAIFullCorpusGenerator(client=Client(responses), model="probe")

    async def go():
        trace, seen = AnswerTrace(), []
        async for kind, data in fn(QUERY, *deps, gen, trace, flags):
            seen.append((kind, data, responses.router_done))
        return trace, seen

    trace, seen = asyncio.run(go())
    return trace, seen, responses.calls


def _request_bytes(calls):
    return sorted(json.dumps(c, ensure_ascii=False, sort_keys=True, default=str) for c in calls)


def test_flag_off_is_exactly_the_old_stream(deps):
    old = collect(deps, answer_turn_stream, OFF, route="tro_ly_hue", router_delay=0, answer_delay=0)
    new = collect(deps, answer_turn_stream_parallel, OFF, route="tro_ly_hue", router_delay=0, answer_delay=0)
    assert [(k, d) for k, d, _ in new[1]] == [(k, d) for k, d, _ in old[1]]
    assert _request_bytes(new[2]) == _request_bytes(old[2])  # Q1 mức đơn vị: cùng yêu cầu gửi model


def test_kept_route_holds_events_until_routed_and_sends_same_requests(deps):
    """Trợ lý xong trước định tuyến ⇒ không sự kiện nào ngoài `routing` ra trước khi có tuyến; chuỗi sự kiện + yêu cầu như đường cũ."""
    old_trace, old_events, old_calls = collect(deps, answer_turn_stream, OFF, route="tro_ly_hue", router_delay=0, answer_delay=0)
    trace, events, calls = collect(deps, answer_turn_stream_parallel, ON, route="tro_ly_hue", router_delay=0.4, answer_delay=0)
    assert events[0][:2] == ("status", {"stage": "routing"})
    assert all(done for _, _, done in events[1:])  # mọi sự kiện sau `routing` ra khi định tuyến đã xong
    assert [(k, d) for k, d, _ in events] == [(k, d) for k, d, _ in old_events]
    assert _request_bytes(calls) == _request_bytes(old_calls)
    assert trace.answer == old_trace.answer and [s.id for s in trace.so_nguon] == [s.id for s in old_trace.so_nguon]
    assert [c["route"] for c in trace.llm_calls] == [c["route"] for c in old_trace.llm_calls]  # định tuyến rồi trả lời
    assert trace.n_tra_loi_bo == 0 and trace.usd_bo is None


def test_other_route_discards_everything_of_the_early_answer(deps):
    trace, events, _ = collect(deps, answer_turn_stream_parallel, ON, route="ngoai_pham_vi", router_delay=0.3, answer_delay=0)
    assert [(k, d) for k, d, _ in events] == [("status", {"stage": "routing"}), ("delta", OUT_OF_SCOPE_ANSWER)]
    assert trace.so_nguon == [] and trace.tools == [] and trace.packed is None and trace.cited == ()  # như câu cố định đường cũ
    assert [c["route"] for c in trace.llm_calls] == ["router"]
    assert trace.n_tra_loi_bo == 1 and trace.bo_huy_giua is False and trace.usd_bo > 0  # xong trước tuyến ⇒ usage thật


def test_cancelled_mid_answer_counts_lower_bound_and_does_not_delay_fixed_answer(deps):
    trace, events, _ = collect(deps, answer_turn_stream_parallel, ON, route="ngoai_pham_vi", router_delay=0, answer_delay=2)
    assert [d for k, d, _ in events if k == "delta"] == [OUT_OF_SCOPE_ANSWER]
    assert trace.n_tra_loi_bo == 1 and trace.bo_huy_giua is True
    assert trace.usd_bo is not None and trace.usd_bo >= 0  # lần gọi bị huỷ: không usage ⇒ chỉ cận dưới (có thể 0 khi huỷ trước model)


def test_chat_route_uses_old_chat_path(deps):
    trace, events, calls = collect(deps, answer_turn_stream_parallel, ON, route="tro_chuyen", router_delay=0.2, answer_delay=0)
    assert trace.route == "tro_chuyen" and trace.so_nguon == [] and trace.cited == ()
    assert [c["route"] for c in trace.llm_calls] == ["router", "tro_chuyen"] and trace.n_tra_loi_bo == 1
    assert "searched" not in [d.get("stage") for k, d, _ in events if k == "status"]


def test_router_error_keeps_early_answer(deps):
    class FailingRouter(TimedResponses):
        async def create(self, **kwargs):
            if str(kwargs.get("instructions", "")).startswith(ROUTER_INSTRUCTIONS[:80]):
                self.calls.append(kwargs)
                await asyncio.sleep(0.2)
                self.router_done = True
                raise RuntimeError("định tuyến lỗi")
            return await super().create(**kwargs)

    responses = FailingRouter(route="tro_ly_hue", router_delay=0, answer_delay=0)
    gen = OpenAIFullCorpusGenerator(client=Client(responses), model="probe")

    async def go():
        trace = AnswerTrace()
        events = [e async for e in answer_turn_stream_parallel(QUERY, *deps, gen, trace, ON)]
        return trace, events

    trace, events = asyncio.run(go())
    assert trace.route_error == "router_failed" and trace.route == "tro_ly_hue"
    assert any(k == "delta" for k, _ in events) and trace.n_tra_loi_bo == 0


def test_early_answer_error_is_dropped_when_route_is_other(deps):
    trace, events, _ = collect(deps, answer_turn_stream_parallel, ON, route="ngoai_pham_vi", router_delay=0.3, answer_delay=0, answer_fails=True)
    assert [d for k, d, _ in events if k == "delta"] == [OUT_OF_SCOPE_ANSWER] and trace.n_tra_loi_bo == 1


def test_emergency_route_keeps_early_answer(deps):
    """Phương án B bậc G: khan_cap đi đường trợ lý Huế ⇒ giữ phần đã chạy song song như tuyến tro_ly_hue."""
    trace, events, _ = collect(deps, answer_turn_stream_parallel, ON, route="khan_cap", router_delay=0.2, answer_delay=0)
    assert trace.route == "tro_ly_hue" and trace.emergency_by == "router" and trace.n_tra_loi_bo == 0
    assert any(k == "delta" for k, _, _ in events)


# ---------- B161 M-1: lượt mang giá trị nút (B4b / B5) — phần chạy trước nhận đủ đầu vào route đặt ----------

def _run(deps, fn, flags, trace, query, gen):
    async def go():
        return [e async for e in fn(query, *deps, gen, trace, flags)]
    return asyncio.run(go())


def test_button_turn_sends_same_requests_and_keeps_route_inputs(deps):
    from llm.hoi_lai import TruongInput, ghep_cau
    query = ghep_cau(QUERY, TruongInput(so_ngay="2"))  # câu ghép tới model; lần tìm đầu bằng câu gốc (B4 m-3)
    sent = {}
    for name, fn, flags, delay in (("old", answer_turn_stream, OFF, 0), ("new", answer_turn_stream_parallel, ON, 0.3)):
        responses = TimedResponses(route="tro_ly_hue", router_delay=delay, answer_delay=0)
        trace = AnswerTrace(truong={"so_ngay": "2"}, search_query=QUERY)
        events = _run(deps, fn, flags, trace, query, OpenAIFullCorpusGenerator(client=Client(responses), model="probe"))
        sent[name] = (trace, events, responses.calls)
    (t_old, e_old, c_old), (t_new, e_new, c_new) = sent["old"], sent["new"]
    assert _request_bytes(c_new) == _request_bytes(c_old) and e_new == e_old
    assert (t_new.truong, t_new.search_query) == ({"so_ngay": "2"}, QUERY) and [s.id for s in t_new.so_nguon] == [s.id for s in t_old.so_nguon]


def test_b5_answer_now_on_parallel_path_does_not_ask_twice(deps):
    from test_b2_tool_loop import answer, generator as scripted
    from test_b5_lich_trinh import BANG, CAU, lich_call, tool_names, viet_theo_khung

    def script(_n, kw):  # theo nội dung lần gọi (định tuyến và trợ lý chạy cùng lúc ⇒ thứ tự không cố định)
        if str(kw.get("instructions", "")).startswith(ROUTER_INSTRUCTIONS[:80]):
            return [message({"route": "tro_ly_hue"})]
        has_output = any(isinstance(i, dict) and i.get("type") == "function_call_output" for i in kw["input"])
        return [answer(viet_theo_khung(kw))] if has_output else [lich_call()] if "lich_trinh" in tool_names(kw) else [answer("x [1].")]

    flags = dataclasses.replace(ON, lich_trinh=True, bang_lich=BANG)
    now = AnswerTrace(truong={}, search_query=CAU)  # "Trả lời luôn": `truong` rỗng ⇒ code đặt tạm 1 ngày, không thẻ lần hai (B5 D15)
    _run(deps, answer_turn_stream_parallel, flags, now, CAU, scripted(script))
    assert now.clarify is None and now.lich["khung"]["tham_so"]["so_ngay_tam"] and now.answer.startswith("Mình hiểu: 1 ngày (tạm)")
    ask = AnswerTrace()  # cùng câu, không bấm nút ⇒ code hỏi số ngày (đối chứng: trường quyết định kết quả)
    _run(deps, answer_turn_stream_parallel, flags, ask, CAU, scripted(script))
    assert ask.fixed_outcome == "hoi_lai" and [t["ten"] for t in ask.clarify["truong"]] == ["so_ngay"]
