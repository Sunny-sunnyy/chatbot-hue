"""Việc agent (3) 14/11 — câu nhiều ý (plan `docs/superpowers/plans/2026-11-14-cau-nhieu-y-plan.md`, cờ `cau_nhieu_y`).
Khoá: lời dặn chỉ đổi đúng đoạn luật từ chối; cờ tắt ⇒ chuỗi gửi model giống byte; cổng web mở khi có dòng `CAU_Y_THIEU` không [n], đóng khi
dòng đó có [n] hoặc cờ tắt. Không gọi mạng (client giả ghi lại lời dặn gửi đi)."""
import asyncio
import dataclasses
import json
import itertools

import pytest
from openai.types.responses import Response

from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, co_y_thieu, web_gate_open
from llm.full_corpus_prompt import (ANSWER_SYSTEM_INSTRUCTIONS, ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y, CAU_Y_THIEU, INSUFFICIENT_ANSWER,
                                    _LUAT_NHIEU_Y, _LUAT_TU_CHOI)
from llm.generator_openai_full_corpus import OpenAIFullCorpusGenerator
from llm.tra_web import KetQuaWeb

_ids = itertools.count(1)
USAGE = {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120,
         "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 3}}
TRA_LOI = f"Vé lẻ người lớn 200.000 đồng [1].\n{CAU_Y_THIEU} chương trình dịp Tết năm tới."


class Client:
    """Trả một câu trả lời cố định, ghi kwargs mọi lần gọi (để đọc lời dặn thật sự gửi đi)."""

    def __init__(self, text):
        self.calls, self.text = [], text
        self.responses = self

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        out = [{"type": "message", "id": f"m{next(_ids)}", "role": "assistant", "status": "completed",
                "content": [{"type": "output_text", "text": json.dumps({"answer": self.text}, ensure_ascii=False), "annotations": []}]}]
        return Response.model_validate({"id": f"r{next(_ids)}", "created_at": 0, "model": "probe", "object": "response", "output": out,
                                        "parallel_tool_calls": False, "tool_choice": "auto", "tools": [], "usage": USAGE, "status": "completed"})

    async def close(self):
        return None


@pytest.fixture(scope="module")
def deps():
    from core.settings_loader import load_settings
    from evaluation.full_corpus_eval import build_context_builder, build_retrieval
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    yield service, build_context_builder(settings)
    service.close()


def chay(deps, flags, text=TRA_LOI):
    client = Client(text)
    trace = AnswerTrace()
    asyncio.run(answer_turn("Vé lẻ vào Đại Nội giá bao nhiêu, dịp Tết năm tới có chương trình gì?", *deps,
                            OpenAIFullCorpusGenerator(client=client, model="probe"), trace, flags))
    return trace, client.calls


def test_instructions_change_only_the_refusal_paragraph():
    assert ANSWER_SYSTEM_INSTRUCTIONS.count(_LUAT_TU_CHOI) == 1
    assert ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y == ANSWER_SYSTEM_INSTRUCTIONS.replace(_LUAT_TU_CHOI, _LUAT_NHIEU_Y)
    assert CAU_Y_THIEU in ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y and INSUFFICIENT_ANSWER in ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y
    assert CAU_Y_THIEU not in ANSWER_SYSTEM_INSTRUCTIONS


@pytest.mark.parametrize("text, co", [
    (TRA_LOI, True),
    (f"Giá 200.000 đồng [1].\n- {CAU_Y_THIEU} lịch Tết.", True),           # gạch đầu dòng
    (f"Giá 200.000 đồng [1].\n{CAU_Y_THIEU} lịch Tết [2].", False),        # dòng thiếu có trích dẫn ⇒ không tính
    (f"Giá 200.000 đồng [1].\n{CAU_Y_THIEU} lịch Tết [Nguồn 2].", False),
    (f"Giá vé có ghi: {CAU_Y_THIEU} x.", False),                             # không ở đầu dòng
    ("Giá 200.000 đồng [1].", False),
])
def test_missing_part_marker_detected_only_at_line_start_without_citation(text, co):
    assert co_y_thieu(text) is co


def _trace(answer):
    return AnswerTrace(route="tro_ly_hue", answer=answer)


def test_gate_opens_on_marker_only_with_flag():
    bat = AssistantFlags(router=True, tim_them=True, tra_web=True, cau_nhieu_y=True)
    tat = dataclasses.replace(bat, cau_nhieu_y=False)
    assert web_gate_open(_trace(TRA_LOI), bat, object())
    assert not web_gate_open(_trace(TRA_LOI), tat, object())                                     # cờ tắt ⇒ như cũ: trả lời một phần ⇒ kho thắng
    assert not web_gate_open(_trace(f"Giá [1].\n{CAU_Y_THIEU} x [2]."), bat, object())            # dòng thiếu có [n]
    assert web_gate_open(_trace(INSUFFICIENT_ANSWER), bat, object())                              # câu từ chối vẫn mở như cũ
    assert not web_gate_open(dataclasses.replace(_trace(TRA_LOI), web={"outcome": "co_muc"}), bat, object())  # ≤ 1 lần tra / câu


def test_flag_off_sends_old_instructions_byte_identical_and_on_sends_per_part_rule(deps):
    tat = AssistantFlags(tim_them=True)
    bat = dataclasses.replace(tat, cau_nhieu_y=True)
    _, goi_tat = chay(deps, tat)
    _, goi_bat = chay(deps, bat)
    lo_tat, lo_bat = goi_tat[0]["instructions"], goi_bat[0]["instructions"]
    assert lo_tat == OpenAIFullCorpusGenerator(client=Client(""), model="probe").assistant_instructions   # giống byte bản trước
    assert CAU_Y_THIEU not in lo_tat
    assert lo_bat == lo_tat.replace(_LUAT_TU_CHOI, _LUAT_NHIEU_Y)                                        # chỉ khác đúng đoạn luật
    assert goi_tat[0]["input"] == goi_bat[0]["input"]                                                  # tin nhắn người dùng / ngữ cảnh không đổi


def test_answer_with_marker_opens_web_once_with_user_question(deps):
    flags = AssistantFlags(router=True, tim_them=True, tra_web=True, cau_nhieu_y=True)  # định tuyến giả lỗi ⇒ về tro_ly_hue
    truy_van = []

    async def tim_web(q):
        truy_van.append(q)
        return KetQuaWeb(trang_thai="rong", so_web=[], ms=1.0, loi=None, usd=0.0)
    client = Client(TRA_LOI)
    trace = AnswerTrace()
    cau = "Vé lẻ vào Đại Nội giá bao nhiêu, dịp Tết năm tới có chương trình gì?"
    asyncio.run(answer_turn(cau, *deps, OpenAIFullCorpusGenerator(client=client, model="probe"), trace, flags, tim_web=tim_web))
    assert trace.answer.startswith("Vé lẻ") and CAU_Y_THIEU in trace.answer                            # phần kho giữ nguyên
    assert len(truy_van) == 1 and "Đại Nội" in truy_van[0]                                             # truy vấn từ câu người dùng (D2)
