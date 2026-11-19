"""Cờ `luu_y_an_toan` (19/11) — một câu thêm vào lời dặn trợ lý có công cụ: Bằng chứng đang dùng có cảnh báo an toàn / điều kiện tạm ngừng của chính
hoạt động được hỏi ⇒ nêu kèm một câu có trích.
Khoá: cờ tắt ⇒ yêu cầu gửi model giống byte ở MỌI loại lượt; cờ bật ⇒ lời dặn chỉ khác đúng một câu, tin nhắn + công cụ không đổi; lượt biểu mẫu và
đường sinh một lần (không công cụ) không nhận câu này. Không gọi mạng (client dựng sẵn ghi lại yêu cầu gửi đi); tìm kho là Qdrant thật (chỉ đọc).
Đây KHÔNG phải bằng chứng model thật nêu lưu ý — phần đó ở lượt đo có phí."""
import asyncio
import dataclasses
import json

import pytest

from llm.assistant import AnswerTrace, AssistantFlags, _assistant_instructions, answer_bieu_mau, answer_turn, answer_turn_stream, answer_turn_stream_parallel
from llm.full_corpus_prompt import (ANSWER_SYSTEM_INSTRUCTIONS, ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y, ASSISTANT_HISTORY_NOTE, LUU_Y_AN_TOAN, _DONG_LUU_Y,
                                    them_luu_y_an_toan)
from test_b2_tool_loop import answer, deps, generator  # noqa: F401 — `deps` là fixture (Qdrant thật)

CAU = "Vé vào Đại Nội giá bao nhiêu?"
CAU_HAI_Y = "Vé lẻ vào Đại Nội giá bao nhiêu, dịp Tết năm tới có chương trình gì?"
LICH_SU = (("Đại Nội mở cửa mấy giờ?", ""),)
TAT = AssistantFlags(tim_them=True, cau_nhieu_y=True)
BAT = dataclasses.replace(TAT, luu_y_an_toan=True)


def script(n, kw):
    ins = kw.get("instructions") or ""
    if "tro_ly_hue" in ins and "ngoai_pham_vi" in ins:  # lời dặn định tuyến
        return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                 "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
    return [answer("Vé lẻ người lớn 200.000 đồng [1].")]


def _goi_tro_ly(gen) -> dict:
    """Yêu cầu gửi model của lần gọi trợ lý (bỏ lần gọi định tuyến); khoá `stream` bỏ ra để so hai cờ cùng một đường."""
    goi = [c for c in gen.client.responses.calls if "ngoai_pham_vi" not in (c.get("instructions") or "")]
    assert len(goi) == 1
    return {k: v for k, v in goi[0].items() if k in ("instructions", "input", "tools")}


def _khong_stream(deps, flags, query=CAU, **trace_kw):
    gen = generator(script)
    asyncio.run(answer_turn(query, *deps, gen, AnswerTrace(**trace_kw), flags))
    return _goi_tro_ly(gen)


def _stream(deps, flags, parallel):
    gen = generator(script)
    flags = dataclasses.replace(flags, router=True, song_song_tra_loi=parallel)
    path = answer_turn_stream_parallel if parallel else answer_turn_stream

    async def go():
        return [e async for e in path(CAU, *deps, gen, AnswerTrace(), flags, None, None)]
    asyncio.run(go())
    return _goi_tro_ly(gen)


# Mỗi loại lượt đi vòng công cụ: tên ⇒ hàm chạy lượt với một bộ cờ (WORKFLOW §4 mục 4c — test "cờ tắt giống byte" một loại lượt là không đủ)
LOAI_LUOT = {
    "luot_dau": lambda deps, flags: _khong_stream(deps, flags),
    "co_lich_su": lambda deps, flags: _khong_stream(deps, flags, history=LICH_SU),
    "cau_nhieu_y": lambda deps, flags: _khong_stream(deps, flags, CAU_HAI_Y),
    "nhieu_y_co_lich_su": lambda deps, flags: _khong_stream(deps, flags, CAU_HAI_Y, history=LICH_SU),
    "luot_ghep_sau_nut": lambda deps, flags: _khong_stream(deps, flags, truong={}, search_query=CAU),
    "stream": lambda deps, flags: _stream(deps, flags, False),
    "stream_song_song": lambda deps, flags: _stream(deps, flags, True),
}


def test_sentence_is_added_once_right_after_the_safety_note_line():
    moi = them_luu_y_an_toan(ANSWER_SYSTEM_INSTRUCTIONS)
    assert moi == ANSWER_SYSTEM_INSTRUCTIONS.replace(_DONG_LUU_Y, f"{_DONG_LUU_Y}\n{LUU_Y_AN_TOAN}") and moi.count(LUU_Y_AN_TOAN) == 1
    assert LUU_Y_AN_TOAN not in ANSWER_SYSTEM_INSTRUCTIONS and LUU_Y_AN_TOAN not in ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y
    assert them_luu_y_an_toan(ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y).count(LUU_Y_AN_TOAN) == 1
    with pytest.raises(ValueError):
        them_luu_y_an_toan("lời dặn lạ không có dòng lưu ý")


@pytest.mark.parametrize("history", [(), LICH_SU])
@pytest.mark.parametrize("nhieu_y", [False, True])
def test_budget_string_equals_instructions_of_the_agent_that_is_sent(history, nhieu_y):
    """Chuỗi lõi dùng để đếm ngân sách ngữ cảnh = đúng lời dặn của agent generator dựng cho lượt, ở cả bốn bản trợ lý, cờ bật lẫn tắt."""
    gen = generator(script)
    trace = AnswerTrace(history=history)
    for bat in (False, True):
        extra = {"luu_y_an_toan": True} if bat else {}
        agent, _, _ = gen._assistant_for(lambda cau_tim: "", history=history, nhieu_y=nhieu_y, **extra)
        assert agent.instructions == _assistant_instructions(gen, trace, nhieu_y, bat)
        assert agent.instructions.count(LUU_Y_AN_TOAN) == (1 if bat else 0)
        assert (ASSISTANT_HISTORY_NOTE in agent.instructions) is bool(history)


@pytest.mark.parametrize("loai", list(LOAI_LUOT))
def test_every_tool_turn_type_flag_off_is_byte_identical_and_on_adds_one_sentence(deps, loai):
    mac_dinh = LOAI_LUOT[loai](deps, AssistantFlags(tim_them=True, cau_nhieu_y=True))  # không nhắc tới cờ mới = bản đang chạy
    tat, bat = LOAI_LUOT[loai](deps, TAT), LOAI_LUOT[loai](deps, BAT)
    assert tat == mac_dinh and LUU_Y_AN_TOAN not in json.dumps(tat, ensure_ascii=False)
    assert bat["instructions"] == them_luu_y_an_toan(tat["instructions"]) != tat["instructions"]
    assert bat["input"] == tat["input"] and bat["tools"] == tat["tools"]            # tin nhắn người dùng, ngữ cảnh, công cụ không đổi


def test_one_shot_path_without_tools_does_not_get_the_sentence(deps):
    """Cờ cần `tim_them`: đường sinh một lần (không công cụ) gửi lời dặn gốc dù cờ bật."""
    goi = _khong_stream(deps, AssistantFlags(luu_y_an_toan=True))
    assert goi["instructions"] == ANSWER_SYSTEM_INSTRUCTIONS


def test_form_turn_does_not_get_the_sentence(deps):
    """Lượt biểu mẫu "Lên kế hoạch" (lời dặn riêng, ghi chú do code nối) không nhận câu mới, cờ bật hay tắt gửi cùng yêu cầu."""
    from core.settings_loader import load_settings
    that = AssistantFlags.from_settings(load_settings(validate_private_paths=False))
    if not that.lich_trinh_bieu_mau:
        pytest.skip("cờ lich_trinh_bieu_mau tắt ở settings")
    gui = {}
    for ten, bat in (("tat", False), ("bat", True)):
        gen = generator(lambda n, kw: [answer("")])
        trace = AnswerTrace(truong={"so_ngay": "1", "kieu_di": "nhe_nhang", "so_thich": ["di_tich"]}, bieu_mau=True, search_query="x")
        try:
            asyncio.run(answer_bieu_mau("x", *deps, gen, trace, dataclasses.replace(that, luu_y_an_toan=bat)))
        except Exception:  # đầu ra dựng sẵn không hợp khuôn lịch ⇒ lỗi SAU khi yêu cầu đã gửi; test này chỉ đọc yêu cầu
            pass
        gui[ten] = [{k: c.get(k) for k in ("instructions", "input")} for c in gen.client.responses.calls]
    assert gui["tat"] and gui["tat"] == gui["bat"]
    assert all(LUU_Y_AN_TOAN not in (c["instructions"] or "") for c in gui["bat"])
