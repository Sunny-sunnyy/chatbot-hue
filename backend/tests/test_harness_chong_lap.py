"""Unit test cho Đợt 1A (`chong_lap_cong_cu`, `cuu_max_turns`) và Đợt 1B (`siet_tro_chuyen`) — 0 USD."""
import asyncio
import copy
import datetime as dt
import json
import time

import pytest

from api.routes.chat import METRIC_FIELDS, STREAM_METRIC_FIELDS, _answer_events, _copy_trace_metrics
from core.settings_loader import load_settings
from llm import khoang_cach as kc
from llm import liet_ke as lk
from llm import thoi_tiet as tt
from llm.assistant import (
    TEN_CUU_MAX_TURNS,
    AnswerTrace,
    AssistantFlags,
    answer_turn,
    answer_turn_stream,
    answer_turn_stream_parallel,
    gan_diem_for_turn,
    khoang_cach_for_turn,
    liet_ke_for_turn,
    ngay_lich_for_turn,
    thoi_tiet_for_turn,
)
from llm.full_corpus_prompt import (
    CHAT_INSTRUCTIONS,
    CHAT_SIET_TRO_CHUYEN,
    OUT_OF_SCOPE_ANSWER,
    ROUTER_HISTORY_NOTE,
    ROUTER_INSTRUCTIONS,
    ROUTER_SEARCH_V1,
    ROUTER_SEARCH_V3,
    ROUTER_SIET_TRO_CHUYEN,
    INSUFFICIENT_ANSWER,
)
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401
from test_chat_stream import parse_sse
from test_het_luot_tim import sent_requests


def _du_bao_mau() -> tt.DuBao:
    hom = tt.hom_nay_vn()
    ngay = [
        {"ngay": hom + dt.timedelta(days=i), "tmax": 29, "tmin": 22, "xs": 30, "mua": 1.0}
        for i in range(tt.SO_NGAY)
    ]
    return tt.DuBao(trang_thai="ok", ngay=ngay, cap_nhat=f"09:00 {hom:%d/%m}", ms=5.0)


def _tool_call(name: str, args: dict) -> dict:
    return {
        "type": "function_call",
        "id": f"fc_{name}",
        "call_id": f"call_{name}_{len(args)}",
        "name": name,
        "arguments": json.dumps(args, ensure_ascii=False),
        "status": "completed",
    }


def _router_reply(route: str) -> list[dict]:
    return [{
        "type": "message",
        "id": "r_1",
        "role": "assistant",
        "status": "completed",
        "content": [{"type": "output_text", "text": json.dumps({"route": route}), "annotations": []}],
    }]


# ---------- Mặc định TẮT & giống hệt hành vi cũ ----------


def test_new_flags_default_off_in_code_and_settings():
    flags = AssistantFlags()
    assert (flags.chong_lap_cong_cu, flags.cuu_max_turns, flags.siet_tro_chuyen) == (False, False, False)
    settings = load_settings(validate_private_paths=False)
    loaded = AssistantFlags.from_settings(settings)
    for key in ("chong_lap_cong_cu", "cuu_max_turns", "siet_tro_chuyen"):
        assert isinstance(settings["assistant"][key], bool)
        assert getattr(loaded, key) is settings["assistant"][key]


def test_all_flags_off_keep_exact_requests_and_old_max_turns_behavior(deps):
    """Mọi cờ mới tắt: gửi model giống từng byte và hành vi chạm max_turns vẫn như cũ."""
    cau = "Huế có món gì ngon?"
    always_tool = lambda n, kw: [tool_call(f"món {n}")]  # noqa: E731

    gen_a = generator(always_tool)
    trace_a = AnswerTrace()
    asyncio.run(answer_turn(cau, *deps, gen_a, trace_a, AssistantFlags(tim_them=True)))

    gen_b = generator(always_tool)
    trace_b = AnswerTrace()
    asyncio.run(answer_turn(cau, *deps, gen_b, trace_b, AssistantFlags(tim_them=True, chong_lap_cong_cu=False, cuu_max_turns=False)))

    assert sent_requests(gen_a) == sent_requests(gen_b)
    assert trace_a.fixed_outcome == trace_b.fixed_outcome == "max_turns"
    assert trace_a.cuu_max_turns is None and trace_b.cuu_max_turns is None
    metrics = dict.fromkeys(METRIC_FIELDS)
    _copy_trace_metrics(trace_a, metrics)
    assert "cuu_max_turns" not in metrics and set(metrics) == set(METRIC_FIELDS)


# ---------- Đợt 1A: chong_lap_cong_cu ----------


def test_chong_lap_ngay_lich_blocks_duplicate_with_source_id():
    trace = AnswerTrace()
    fn = ngay_lich_for_turn(trace, "Tết âm lịch năm sau là ngày nào?", chong_lap=True)
    r1 = asyncio.run(fn("am", 1, 1, 2027, False))
    assert "[Nguồn 1]" in r1 and len(trace.so_nguon) == 1
    r2 = asyncio.run(fn("am", 1, 1, 2027, False))
    assert "[1]" in r2 and "Không gọi lặp lại nữa" in r2
    assert len(trace.so_nguon) == 1 and trace.tools[-1]["lap"] is True

    # "hom_nay" với các số phụ khác nhau vẫn chuẩn hoá thành cùng một khoá
    trace_hom_nay = AnswerTrace()
    fn_hom_nay = ngay_lich_for_turn(trace_hom_nay, "Hôm nay là thứ mấy?", chong_lap=True)
    r3 = asyncio.run(fn_hom_nay("hom_nay", 0, 0, 0, False))
    assert "[Nguồn 1]" in r3 and len(trace_hom_nay.so_nguon) == 1
    r4 = asyncio.run(fn_hom_nay("hom_nay", 1, 2, 2026, False))
    assert "[1]" in r4 and trace_hom_nay.tools[-1]["lap"] is True and len(trace_hom_nay.so_nguon) == 1


def test_chong_lap_liet_ke_bai_normalizes_phrase_order_and_points_to_source():
    muc_luc = (
        lk.bai_tu_markdown("foods/restaurants/a.md", "# Quán A\n\nBán bún bò và chè."),
        lk.bai_tu_markdown("foods/restaurants/b.md", "# Quán B\n\nChỉ bán cơm."),
    )
    trace = AnswerTrace()
    fn = liet_ke_for_turn(trace, muc_luc, chong_lap=True)
    r1 = asyncio.run(fn("quan_an", ["bún", "chè"]))
    assert "[Nguồn 1]" in r1 and len(trace.so_nguon) == 1
    r2 = asyncio.run(fn("quan_an", ["CHÈ ", "bún"]))
    assert "[1]" in r2 and "Không gọi lặp lại nữa" in r2
    assert len(trace.so_nguon) == 1 and trace.tools[-1]["lap"] is True


def test_chong_lap_khoang_cach_and_gan_diem_prevent_reexecution():
    bang = kc.BangKhoangCach(
        ten={"a": "Điểm A", "b": "Điểm B"},
        ten_khac={"a": (), "b": ()},
        cap={"a|b": {"km": 2.5, "phut": 7}},
    )
    trace_kc = AnswerTrace()
    fn_kc = khoang_cach_for_turn(trace_kc, bang, trang_thai=True, chong_lap=True)
    r1 = asyncio.run(fn_kc("a", "b"))
    assert "[Nguồn 1]" in r1 and len(trace_kc.khoang_cach) == 1
    r2 = asyncio.run(fn_kc("a", "b"))
    assert "[1]" in r2 and "Không gọi lặp lại nữa" in r2
    assert trace_kc.tools[-1]["lap"] is True and len(trace_kc.khoang_cach) == 1 and len(trace_kc.so_nguon) == 1

    quan = {"c": [{"ten": "Quán Gần", "loai": "quan_an", "nguon": "kho", "toa": (16.4637, 107.5909), "bai_id": "foods/restaurants/q.md"}]}
    toa_do = {"a": (16.4637, 107.5909), "b": (16.47, 107.60)}
    trace_gd = AnswerTrace()
    fn_gd = gan_diem_for_turn(trace_gd, bang, quan, toa_do, chong_lap=True)
    g1 = asyncio.run(fn_gd("a", "quan_an"))
    assert "[Nguồn 1]" in g1 and len(trace_gd.gan_diem) == 1
    g2 = asyncio.run(fn_gd("a", "quan_an"))
    assert "[1]" in g2 and "Không gọi lặp lại nữa" in g2
    assert trace_gd.tools[-1]["lap"] is True and len(trace_gd.gan_diem) == 1 and len(trace_gd.so_nguon) == 1


def test_chong_lap_thoi_tiet_normal_and_bao_lu_avoid_refetch():
    calls = 0

    async def fake_du_bao():
        nonlocal calls
        calls += 1
        return _du_bao_mau()

    # Thường
    trace = AnswerTrace(thoi_tiet_ctx={"bao_lu": False, "bao_lu_cong_cu": False, "buoi": False})
    fn = thoi_tiet_for_turn(trace, fake_du_bao, chong_lap=True)
    r1 = asyncio.run(fn(0, 1))
    assert "[Nguồn 1]" in r1 and calls == 1
    r2 = asyncio.run(fn(0, 1))
    assert "[1]" in r2 and "Không gọi lặp lại nữa" in r2 and calls == 1 and trace.tools[-1]["lap"] is True

    # Bão/lũ wrapper
    calls = 0
    trace_bl = AnswerTrace(thoi_tiet_ctx={"bao_lu": False, "bao_lu_cong_cu": True, "buoi": False})
    fn_bl = thoi_tiet_for_turn(trace_bl, fake_du_bao, chong_lap=True)
    b1 = asyncio.run(fn_bl("bao_lu", 0, 2))
    assert "[Nguồn 1]" in b1 and calls == 1
    b2 = asyncio.run(fn_bl("bao_lu", 0, 2))
    assert "[1]" in b2 and "Không gọi lặp lại nữa" in b2 and calls == 1 and trace_bl.tools[-1]["lap"] is True


def test_chong_lap_end_to_end_turn_records_lap_and_answers(deps):
    bang = kc.BangKhoangCach(ten={"a": "Điểm A", "b": "Điểm B"}, ten_khac={"a": (), "b": ()}, cap={"a|b": {"km": 3.0, "phut": 8}})
    flags = AssistantFlags(tim_them=True, khoang_cach=True, khoang_cach_bang=bang, chong_lap_cong_cu=True)

    def script(n, kw):
        if n in (1, 2):
            return [_tool_call("khoang_cach", {"diem_a": "a", "diem_b": "b"})]
        # Lần 3 sau khi nhận actionable feedback về nguồn [N] -> model viết câu trả lời trích đúng mã đó
        outputs = [i["output"] for i in kw["input"] if isinstance(i, dict) and i.get("type") == "function_call_output"]
        assert "Không gọi lặp lại nữa" in outputs[-1]
        ma = len(trace.so_nguon)
        return [answer(f"Từ Điểm A đến Điểm B khoảng 3 km, đi xe khoảng 10 phút [{ma}].")]

    trace = AnswerTrace()
    gen = generator(script)
    asyncio.run(answer_turn("Từ Điểm A sang Điểm B cách nhau mấy cây?", *deps, gen, trace, flags))
    assert trace.citation_error is None and trace.fixed_outcome is None
    kc_entries = [t for t in trace.tools if t["name"] == "khoang_cach"]
    assert len(kc_entries) == 2 and kc_entries[1].get("lap") is True


# ---------- Đợt 1A: cuu_max_turns ----------


@pytest.mark.parametrize("stream", [False, True])
def test_cuu_max_turns_rescues_when_documents_exist_and_disables_all_tools(deps, stream):
    flags = AssistantFlags(tim_them=True, cuu_max_turns=True)
    cau = "Đại Nội Huế có gì tham quan?"

    def script(n, kw):
        if kw.get("tools"):
            # Cố tình gọi tim_kho mãi cho đến khi chạm max_turns
            return [tool_call(f"Đại Nội vòng {n}")]
        # Lần viết lại của cuu_max_turns không có tool nào -> viết câu có trích dẫn
        return [answer("Đại Nội Huế là khu di tích trung tâm của Kinh thành Huế [1].")]

    gen = generator(script)
    trace = AnswerTrace()
    if stream:
        metrics = dict.fromkeys(STREAM_METRIC_FIELDS)

        async def go():
            turn = answer_turn_stream_parallel(cau, *deps, gen, trace, flags)
            return parse_sse([e async for e in _answer_events(turn, trace, metrics, time.perf_counter())])

        events = asyncio.run(go())
        names = [k for k, _ in events]
        assert "error" not in names and names[-1] == "done" and metrics["outcome"] == "success"
        assert metrics["cuu_max_turns"] == {"thanh_cong": True}
        assert any(k == "delta" and "[1]" in d["text"] for k, d in events)
    else:
        asyncio.run(answer_turn(cau, *deps, gen, trace, flags))
        metrics = dict.fromkeys(METRIC_FIELDS)
        _copy_trace_metrics(trace, metrics)
        assert metrics["cuu_max_turns"] == {"thanh_cong": True}

    assert trace.fixed_outcome is None and trace.citation_error is None
    assert [s.id for s in trace.cited] == [1]
    assert trace.cuu_max_turns == {"thanh_cong": True}
    assert trace.tools[-1]["name"] == TEN_CUU_MAX_TURNS and trace.tools[-1]["thanh_cong"] is True
    # Lần gọi cuối cùng là lần viết lại: tắt toàn bộ tool
    assert not gen.client.responses.calls[-1].get("tools")


def test_cuu_max_turns_keeps_refusal_floor_on_bad_citation_or_no_documents(deps):
    flags_v0 = AssistantFlags(tim_them=True, cuu_max_turns=True)

    # 1) Có documents nhưng lần viết lại bịa nguồn [999] -> vẫn giữ sàn 0 bịa nguồn, trả câu từ chối max_turns
    def bad_citation_script(n, kw):
        return [tool_call(f"tìm {n}")] if kw.get("tools") else [answer("Thông tin bịa nguồn [999].")]

    trace_bad = AnswerTrace()
    asyncio.run(answer_turn("Đại Nội Huế ở đâu?", *deps, generator(bad_citation_script), trace_bad, flags_v0))
    assert trace_bad.fixed_outcome == "max_turns" and trace_bad.answer == INSUFFICIENT_ANSWER and trace_bad.cited == ()
    assert trace_bad.citation_error is None
    assert trace_bad.cuu_max_turns == {"thanh_cong": False}
    assert trace_bad.tools[-1] == {"name": TEN_CUU_MAX_TURNS, "ms": trace_bad.tools[-1]["ms"], "thanh_cong": False}

    # 2) Không có bằng chứng (v2 với tim_them=True, khoang_cach=True, không gọi tim_kho -> trace không có documents)
    bang = kc.BangKhoangCach(ten={"a": "A"}, ten_khac={"a": ()}, cap={})
    flags_v2 = AssistantFlags(lan_tim_dau="v2", tim_them=True, khoang_cach=True, khoang_cach_bang=bang, cuu_max_turns=True)
    calls = []

    def v2_no_docs(n, kw):
        calls.append(kw.get("tools"))
        return [_tool_call("khoang_cach", {"diem_a": "a", "diem_b": "khac"})]

    trace_no_docs = AnswerTrace()
    asyncio.run(answer_turn("Từ A tới B bao xa?", *deps, generator(v2_no_docs), trace_no_docs, flags_v2))
    assert not trace_no_docs.documents
    assert trace_no_docs.fixed_outcome == "max_turns" and trace_no_docs.answer == INSUFFICIENT_ANSWER
    assert trace_no_docs.cuu_max_turns is None
    assert all(bool(t) for t in calls)  # không gọi thêm bước viết lại vì chưa có trace.documents


# ---------- Đợt 1B: siet_tro_chuyen ----------


def test_siet_tro_chuyen_wires_prompts_only_when_enabled(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("HUE_BEDROCK_CREDS_FILE", "/khong/co/file.json")
    base = load_settings(validate_private_paths=False)

    s_off = copy.deepcopy(base)
    s_off["full_corpus_generation"]["provider"] = "openai"
    s_off["assistant"]["siet_tro_chuyen"] = False
    gen_off = OpenAIFullCorpusGenerator.from_environment(s_off)

    assert gen_off.router_agent.instructions == ROUTER_INSTRUCTIONS
    assert gen_off.router_history_agent.instructions == f"{ROUTER_INSTRUCTIONS}\n\n{ROUTER_HISTORY_NOTE}"
    assert [a.instructions for a in gen_off.router_search_agents.values()] == [
        f"{ROUTER_INSTRUCTIONS}\n\n{ROUTER_SEARCH_V1}",
        f"{ROUTER_INSTRUCTIONS}\n\n{ROUTER_SEARCH_V3}",
    ]
    assert gen_off.chat_agent.instructions == CHAT_INSTRUCTIONS

    s_on = copy.deepcopy(s_off)
    s_on["assistant"]["siet_tro_chuyen"] = True
    gen_on = OpenAIFullCorpusGenerator.from_environment(s_on)

    assert gen_on.router_agent.instructions == f"{ROUTER_INSTRUCTIONS}\n\n{ROUTER_SIET_TRO_CHUYEN}"
    assert ROUTER_SIET_TRO_CHUYEN in gen_on.router_history_agent.instructions
    assert all(ROUTER_SIET_TRO_CHUYEN in a.instructions for a in gen_on.router_search_agents.values())
    assert gen_on.chat_agent.instructions == f"{CHAT_INSTRUCTIONS}\n\n{CHAT_SIET_TRO_CHUYEN}"
    assert OUT_OF_SCOPE_ANSWER in CHAT_SIET_TRO_CHUYEN
    for ten in ("answer_agent", "assistant_agent", "bieu_mau_agent", "web_agent", "lich_v2_agent", "sua_lich_agent"):
        assert getattr(gen_on, ten).instructions == getattr(gen_off, ten).instructions


def test_siet_tro_chuyen_leaked_off_topic_refusal_counts_as_refusal_in_metrics(deps):
    def script(n, kw):
        if "ngoai_pham_vi" in str(kw.get("instructions", "")):
            return _router_reply("tro_chuyen")
        assert CHAT_SIET_TRO_CHUYEN in str(kw.get("instructions", ""))
        return [answer(OUT_OF_SCOPE_ANSWER)]

    gen = OpenAIFullCorpusGenerator(client=generator(script).client, model="probe", siet_tro_chuyen=True)
    flags = AssistantFlags(router=True, tim_them=True, siet_tro_chuyen=True)
    trace = AnswerTrace()
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)

    async def go():
        turn = answer_turn_stream("Chào bạn, 1+1 bằng mấy?", *deps, gen, trace, flags)
        return parse_sse([e async for e in _answer_events(turn, trace, metrics, time.perf_counter())])

    events = asyncio.run(go())
    assert trace.route == "tro_chuyen" and trace.answer == OUT_OF_SCOPE_ANSWER
    assert metrics["outcome"] == "success" and metrics["refusal"] is True and events[-1][1]["outcome"] == "success"
