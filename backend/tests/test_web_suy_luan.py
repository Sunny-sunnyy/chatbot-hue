"""Cờ `web_suy_luan_thap` (plan `2026-11-14-web-suy-luan-thap-plan.md`): lần viết mục web với mức suy luận "low".
Khoá đúng một điều: yêu cầu gửi model chỉ khác ở `reasoning`; cờ tắt ⇒ yêu cầu như bản trước (không có `reasoning`)."""
import asyncio

from llm.assistant import AssistantFlags, cong_web
from test_b2_tool_loop import answer, generator
from test_b6_tra_web import CAU, refused, serper

MUC_WEB = "Theo một trang du lịch, khu này có nhiều quán mở khuya [w1]."


def _goi(thap: bool) -> dict:
    calls = []
    gen = generator(lambda n, kw: (calls.append(kw), [answer(MUC_WEB)])[1])
    asyncio.run(cong_web(CAU, gen, refused(), serper(), thap))
    assert len(calls) == 1
    return calls[0]


def test_low_reasoning_changes_only_reasoning():
    tat, bat = _goi(False), _goi(True)
    assert getattr(tat.get("reasoning"), "effort", None) is None  # cờ tắt: SDK không gửi reasoning (giá trị Omit), như bản trước
    assert bat["reasoning"].effort == "low"
    assert {k: v for k, v in bat.items() if k != "reasoning"} == {k: v for k, v in tat.items() if k != "reasoning"}


def test_flag_defaults_off():
    assert AssistantFlags().web_suy_luan_thap is False
