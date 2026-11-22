"""Công tắc `giu_chu_toi_kiem` (22/11/2026). Vì sao: model đang chạy (lớp dịch Bedrock) trả CẢ câu một lần ở cuối lượt có công cụ; chữ đó được phát
ngay, rồi mới tới phép kiểm nguồn. Chữ không qua kiểm (chữ giữ chỗ kiểu "placeholder", câu chép lại không nguồn) vì thế hiện lên rồi bị thay / bị gỡ —
số đo phiên E 22/11: lưới viết lại nổ 9 / 114 lượt, chữ giữ chỗ khoảng 80 ký tự đứng 17–25 giây trước khi được thay. Bật ⇒ ở lượt có công cụ mà generator
báo "chữ về một lần" (`chu_ve_mot_lan`), chữ được giữ tới sau phép kiểm: qua ⇒ phát y như cũ (muộn hơn cỡ mili giây); lưới viết lại nổ ⇒ chỉ phát bản
viết lại; bị rút ⇒ không phát chữ nào. Đường chữ chạy dần thật (OpenAI) không có thuộc tính đó ⇒ y như cũ. 0 USD: tìm kho thật, model theo kịch bản."""
import asyncio
import dataclasses

import pytest

from llm.assistant import AnswerTrace, AssistantFlags, answer_turn_stream
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401  (`deps` = fixture tìm kho thật)
from test_het_luot_viet_lai import CO_NGUON, GIU_CHO, MOT_Y, NHIEU_Y, kich_ban

VIET_LAI = AssistantFlags(lan_tim_dau="v2", cau_nhieu_y=True, het_luot_viet_lai=True)
GIU = dataclasses.replace(VIET_LAI, giu_chu_toi_kiem=True)


def chay(deps, cau, script, flags, mot_lan=True):
    gen, trace = generator(script), AnswerTrace()
    if mot_lan:
        gen.chu_ve_mot_lan = True  # như lớp dịch Bedrock: chữ của lượt có công cụ về một lần ở cuối
    return trace, asyncio.run(_gom(answer_turn_stream(cau, *deps, gen, trace, flags)))


async def _gom(luong):
    return [e async for e in luong]


def chu(events):
    return "".join(d for k, d in events if k == "delta")


@pytest.mark.parametrize("cau", [MOT_Y, NHIEU_Y])
def test_turn_that_passes_the_check_shows_exactly_what_it_showed_before(deps, cau):
    qua = lambda n, kw: [tool_call("ẩm thực Huế")] if n == 1 else [answer(CO_NGUON)]  # noqa: E731
    cu, moi = chay(deps, cau, qua, VIET_LAI), chay(deps, cau, qua, GIU)
    assert moi[0].citation_error is None and moi[0].answer == cu[0].answer
    assert moi[1] == cu[1] and chu(moi[1]) == CO_NGUON  # cùng sự kiện, cùng thứ tự: chỉ thời điểm phát chữ lùi sau phép kiểm


def test_filler_is_never_shown_only_the_rewrite_is(deps):
    trace, events = chay(deps, MOT_Y, kich_ban(), GIU)
    assert trace.citation_error is None and trace.answer == CO_NGUON
    assert chu(events) == CO_NGUON and not [e for e in events if e[0] == "thay_chu"]  # không còn gì để thay
    assert ("status", {"stage": "generating"}) in events  # dòng "đang viết" vẫn hiện trong lúc lần viết lại chạy
    cu = chay(deps, MOT_Y, kich_ban(), VIET_LAI)[1]
    assert GIU_CHO in chu(cu) and ("thay_chu", CO_NGUON) in cu  # công tắc tắt: chữ giữ chỗ hiện rồi được thay, như trước


def test_retracted_text_is_never_shown(deps):
    rut = dataclasses.replace(GIU, het_luot_viet_lai=False)
    trace, events = chay(deps, MOT_Y, kich_ban(), rut)
    assert trace.citation_error is not None and chu(events) == ""  # route gửi lỗi với `after_text` sai: không có chữ nào loé lên rồi mất
    assert GIU_CHO in chu(chay(deps, MOT_Y, kich_ban(), dataclasses.replace(rut, giu_chu_toi_kiem=False))[1])


def test_true_streaming_generator_is_left_alone(deps):
    """Đường OpenAI (chữ chạy dần thật): giữ tới hết sẽ mất hẳn hiệu ứng chữ chạy ⇒ công tắc bật cũng không giữ."""
    assert chay(deps, MOT_Y, kich_ban(), GIU, mot_lan=False)[1] == chay(deps, MOT_Y, kich_ban(), VIET_LAI, mot_lan=False)[1]
