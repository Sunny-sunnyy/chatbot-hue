"""Công tắc `het_luot_viet_lai` (22/11/2026). Vì sao: sau lần tìm kho cuối được phép, công cụ tìm bị cất (`het_luot_bo_cong_cu`); model đang chạy còn muốn
tìm tiếp nên nộp CHỮ GIỮ CHỖ làm câu trả lời ("placeholder", "tìm kho", "Tôi cần tìm thêm về…") ⇒ không có mã nguồn ⇒ câu bị rút ⇒ màn hình "Thử lại"
(5 / 72 lượt của bộ tin nhiều ý sáng 22/11, dồn vào hai tin; cùng tin đó lặp lại thì 13–21 mã nguồn). Báo trước cho model ở lần tìm cuối đã đo 21/11 và
phạm sàn (câu một ý ngoài tỉnh được trả lời từ bằng chứng mỏng 4 / 5 và 2 / 5) ⇒ ở đây chỉ chữa SAU khi đã hỏng: một lần viết không công cụ trên mọi Bằng
chứng đã gom; vẫn không có mã ⇒ câu từ chối cố định. 0 USD: tìm kho thật, model theo kịch bản."""
import asyncio
import dataclasses

import pytest

from llm.assistant import TEN_VIET_LAI, AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import CAU_Y_THIEU, INSUFFICIENT_ANSWER, VIET_LAI_NHIEU_Y_TEXT
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401  (`deps` = fixture tìm kho thật)

MOT_Y, NHIEU_Y = "Huế có món gì ngon?", "Vé vào Đại Nội giá bao nhiêu, mở cửa mấy giờ?"
TAT = AssistantFlags(lan_tim_dau="v2", cau_nhieu_y=True)
MO = dataclasses.replace(TAT, het_luot_viet_lai=True)
GIU_CHO, CO_NGUON = "placeholder", "Huế có nhiều món đáng thử [1]."


def kich_ban(lan_viet_lai=CO_NGUON, so_lan_tim=2):
    """Lời gọi 1..`so_lan_tim`: model xin tìm kho; lời gọi kế: nộp chữ giữ chỗ; lời gọi sau đó (lần viết lại, không công cụ): `lan_viet_lai`."""
    return lambda n, kw: [tool_call(f"câu tìm {n}")] if n <= so_lan_tim else [answer(GIU_CHO if n == so_lan_tim + 1 else lan_viet_lai)]


def chay(deps, cau, gen, flags, stream=False):
    trace = AnswerTrace()

    async def go():
        if stream:
            return [e async for e in answer_turn_stream(cau, *deps, gen, trace, flags)]
        await answer_turn(cau, *deps, gen, trace, flags)
    return trace, asyncio.run(go())


@pytest.mark.parametrize("stream", [False, True])
def test_filler_after_the_search_budget_is_rewritten_once_from_the_gathered_evidence(deps, stream):
    gen = generator(kich_ban())
    trace, events = chay(deps, MOT_Y, gen, MO, stream)
    assert trace.citation_error is None and trace.answer == CO_NGUON and [s.id for s in trace.cited] == [1]
    assert trace.tools[-1]["name"] == TEN_VIET_LAI and trace.tools[-1]["tu_choi"] is False
    goi = gen.client.responses.calls
    assert len(goi) == 4 and len(trace.llm_calls) == 4 and not goi[3].get("tools")  # lần viết lại: một lời gọi thêm, không công cụ, tiền vào sổ
    chu_gui = str(goi[3]["input"])
    assert "[Nguồn 1]" in chu_gui and f"[Nguồn {len(trace.so_nguon)}]" in chu_gui and len(trace.so_nguon) > 10  # đủ Bằng chứng của cả ba lần tìm
    assert VIET_LAI_NHIEU_Y_TEXT not in chu_gui  # tin một ý: đường viết một lần y như cũ (thiếu ⇒ từ chối cả câu)
    if stream:
        i = next(n for n, (k, _) in enumerate(events) if k == "thay_chu")
        assert GIU_CHO in "".join(d for k, d in events[:i] if k == "delta") and events[i] == ("thay_chu", CO_NGUON)  # chữ giữ chỗ đã hiện ⇒ được thay


@pytest.mark.parametrize("stream", [False, True])
def test_switch_off_keeps_the_old_error(deps, stream):
    gen = generator(kich_ban())
    trace, events = chay(deps, MOT_Y, gen, TAT, stream)
    assert trace.citation_error is not None and len(gen.client.responses.calls) == 3 and all(t["name"] != TEN_VIET_LAI for t in trace.tools)
    assert not [e for e in (events or []) if e[0] == "thay_chu"]


def test_rewrite_that_still_has_no_citation_ends_as_the_fixed_refusal_not_an_error(deps):
    gen = generator(kich_ban(lan_viet_lai="Tôi cần tìm thêm."))
    trace, _ = chay(deps, MOT_Y, gen, MO)
    assert trace.citation_error is None and trace.answer == INSUFFICIENT_ANSWER and trace.cited == () and trace.tools[-1]["tu_choi"] is True
    assert len(gen.client.responses.calls) == 4  # đúng một lần viết lại, không lặp


def test_not_triggered_when_the_model_never_searched_or_when_the_answer_passes(deps):
    gen = generator(kich_ban(so_lan_tim=0))  # model không tìm lần nào mà nộp chữ không mã nguồn (kiểu chép lại lời cũ) ⇒ không thuộc lưới này: lỗi như cũ
    trace, _ = chay(deps, MOT_Y, gen, MO)
    assert trace.citation_error is not None and len(gen.client.responses.calls) == 1
    gen = generator(lambda n, kw: [tool_call(f"câu tìm {n}")] if n <= 2 else [answer(CO_NGUON)])  # tìm rồi trả lời có nguồn ⇒ không gọi thêm
    trace, _ = chay(deps, MOT_Y, gen, MO)
    assert trace.citation_error is None and len(gen.client.responses.calls) == 3 and all(t["name"] != TEN_VIET_LAI for t in trace.tools)
    gen = generator(lambda n, kw: [tool_call(f"câu tìm {n}")] if n <= 2 else [answer(INSUFFICIENT_ANSWER)])  # câu từ chối đúng khuôn ⇒ không gọi thêm
    trace, _ = chay(deps, MOT_Y, gen, MO)
    assert trace.answer == INSUFFICIENT_ANSWER and len(gen.client.responses.calls) == 3


def test_model_that_stops_searching_below_the_cap_and_writes_uncited_text_is_caught_too(deps):
    """Lượt thật 22/11 (trần tìm 3 lần, tin hai ý kho thiếu): model tìm 2 lần rồi tự dừng, viết hai dòng "chưa có" kèm một đoạn giải thích không mã nguồn
    ⇒ bản đầu của lưới (đòi "đã hết lượt tìm") không kích hoạt ⇒ màn hình lỗi. Nay: đã tìm ít nhất một lần là đủ; lần viết lại ra câu từ chối ⇒ câu từ
    chối cố định, không lỗi."""
    chu = f"{CAU_Y_THIEU} phòng gym nào ở Huế mở cửa sớm.\n{CAU_Y_THIEU} giá vé tập một ngày.\n\nTôi đã tìm trong tư liệu nhưng không thấy phòng gym nào."
    tran_3 = dataclasses.replace(MO, so_lan_tim_kho=3)
    kich = lambda n, kw: [tool_call(f"câu tìm {n}")] if n <= 2 else [answer(chu if n == 3 else INSUFFICIENT_ANSWER)]  # noqa: E731
    gen = generator(kich)
    trace, _ = chay(deps, NHIEU_Y, gen, tran_3)
    assert trace.model_searches == 2 and trace.citation_error is None and trace.answer == INSUFFICIENT_ANSWER
    assert trace.tools[-1]["name"] == TEN_VIET_LAI and len(gen.client.responses.calls) == 4
    gen = generator(kich)
    tat, _ = chay(deps, NHIEU_Y, gen, dataclasses.replace(TAT, so_lan_tim_kho=3))
    assert tat.citation_error is not None and len(gen.client.responses.calls) == 3      # công tắc tắt: đúng lỗi đã thấy ở lượt thật


@pytest.mark.parametrize("tran, so_lan_tim", [(2, 1), (3, 1), (3, 2)])
def test_single_part_turn_that_stops_below_the_cap_and_writes_uncited_text_is_rewritten(deps, tran, so_lan_tim):
    """Tin MỘT Ý (câu hỏi của phiên đo khi đọc lượt thử lại cuối): model tìm 1–2 lần DƯỚI trần rồi nộp chữ không mã nguồn ⇒ lưới kích hoạt, viết lại theo
    đường viết-một-lần cũ (không có dòng dặn "từng ý"); lần viết lại có nguồn ⇒ câu đó; lần viết lại vẫn không nguồn ⇒ câu từ chối cố định."""
    flags = dataclasses.replace(MO, so_lan_tim_kho=tran)
    gen = generator(kich_ban(so_lan_tim=so_lan_tim))
    trace, _ = chay(deps, MOT_Y, gen, flags)
    assert trace.model_searches == so_lan_tim < tran and trace.citation_error is None and trace.answer == CO_NGUON and trace.tools[-1]["name"] == TEN_VIET_LAI
    assert VIET_LAI_NHIEU_Y_TEXT not in str(gen.client.responses.calls[-1]["input"]) and not gen.client.responses.calls[-1].get("tools")
    gen = generator(kich_ban(lan_viet_lai="Tôi đã tìm nhưng không thấy.", so_lan_tim=so_lan_tim))
    trace, _ = chay(deps, MOT_Y, gen, flags)
    assert trace.citation_error is None and trace.answer == INSUFFICIENT_ANSWER and trace.tools[-1]["tu_choi"] is True
    gen = generator(kich_ban(so_lan_tim=so_lan_tim))
    tat, _ = chay(deps, MOT_Y, gen, dataclasses.replace(TAT, so_lan_tim_kho=tran))
    assert tat.citation_error is not None                                           # công tắc tắt: màn hình lỗi như cũ


def test_multi_part_turn_rewrite_may_answer_part_and_mark_the_missing_part(deps):
    co_phan = f"Vé vào Đại Nội có bán tại cổng [1].\n- {CAU_Y_THIEU} giờ mở cửa."
    gen = generator(kich_ban(lan_viet_lai=co_phan))
    trace, _ = chay(deps, NHIEU_Y, gen, MO)
    assert trace.nhieu_y and trace.citation_error is None and CAU_Y_THIEU in trace.answer and [s.id for s in trace.cited] == [1]
    assert VIET_LAI_NHIEU_Y_TEXT in str(gen.client.responses.calls[3]["input"])


@pytest.mark.parametrize("parallel", [False, True])
def test_through_the_route_events_the_user_gets_the_rewritten_answer_instead_of_the_error_screen(deps, parallel):
    """Đúng đường người dùng đi: định tuyến (chạy song song khi `parallel`) ⇒ lõi stream ⇒ sự kiện gửi trình duyệt. Trước: sự kiện `error`."""
    import json
    import time

    from api.routes.chat import STREAM_METRIC_FIELDS, _answer_events
    from llm.assistant import answer_turn_stream_parallel
    from test_chat_stream import parse_sse

    dem = []

    def script(n, kw):
        if "ngoai_pham_vi" in (kw.get("instructions") or ""):  # lời dặn định tuyến
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        dem.append(n)
        return [tool_call(f"câu tìm {len(dem)}")] if len(dem) <= 2 else [answer(GIU_CHO if len(dem) == 3 else CO_NGUON)]

    flags = AssistantFlags(router=True, tim_them=True, song_song_tra_loi=parallel, het_luot_viet_lai=True)
    trace, metrics = AnswerTrace(), dict.fromkeys(STREAM_METRIC_FIELDS)

    async def go():
        turn = answer_turn_stream_parallel(MOT_Y, *deps, generator(script), trace, flags, None, None)
        return parse_sse([e async for e in _answer_events(turn, trace, metrics, time.perf_counter())])
    events = asyncio.run(go())
    ten = [k for k, _ in events]
    assert "error" not in ten and ten[-1] == "done" and "sources" in ten and metrics["outcome"] == "success"
    assert ("thay_chu", {"text": CO_NGUON}) in events and len(dem) == 4
    assert any(t["name"] == TEN_VIET_LAI for t in trace.tools) and trace.answer == CO_NGUON
