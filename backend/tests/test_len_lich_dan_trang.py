"""Cờ `len_lich_dan_trang` (20/11) — câu nhờ lập lịch nhiều ngày gõ trong ô chat ⇒ code nối một dòng trỏ sang trang Lên kế hoạch.
Hàm thuần + chỗ gắn ở `set_notice`; không model, không mạng, không Qdrant. Câu trong test tự đặt (không phải câu bộ đo).
Đây KHÔNG phải bằng chứng trên câu trả lời thật — phần đó là bộ dò độc lập + một lượt thật qua giao diện."""
import dataclasses

import pytest

from llm.assistant import AnswerTrace, AssistantFlags, set_notice
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.len_lich import CAU_DAN_TRANG, TEN_TRANG, nho_len_lich
from retrieval.full_corpus_context import PackedSource

PHAI_NHAN = [
    "lên lịch giúp mình 2 ngày ở Huế",
    "mình đi Huế 3 ngày với gia đình, xếp lịch trình giúp mình với",
    "Lập giúp tôi kế hoạch đi Huế 4 ngày",
    "gợi ý lịch trình Huế 2 ngày 1 đêm",
    "Xếp cho mình lịch đi Huế ba ngày nhé",
    "tư vấn lịch trình 3 ngày 2 đêm ở Huế cho cặp đôi",
    "bạn lên giúp mình một lịch trình tham quan Huế trong 2 ngày được không?",
    "Sắp xếp lịch trình 5 ngày ở Huế cho nhà có trẻ nhỏ",
    "soạn kế hoạch du lịch Huế 1 ngày",
    "làm cho mình lịch trình đi Huế hai ngày, thích di tích",
    "tạo lịch trình 3 ngày khám phá Huế",
    "thiết kế giúp em lịch trình Huế 4 ngày 3 đêm",
    "cho mình xin lịch trình Huế 3 ngày 2 đêm",   # ba câu bộ dò mù của phiên C trượt ở bản đầu
    "Lên lịch 2N1Đ ở Huế giúp mình",
    "mình cần một lịch trình 2 ngày đi các lăng và Đại Nội",
]
KHONG_NHAN = [
    "dời Đại Nội trong lịch này sang ngày 2",                      # sửa lịch đã lập
    "tóm gọn lịch đó để mình chép, đi 2 ngày thôi",                 # hỏi về lịch đã có
    "lịch trình Huế 3 ngày 2 đêm tốn bao nhiêu tiền",               # hỏi giá
    "Lễ hội Cầu ngư tổ chức mấy ngày",                               # không nhờ lập lịch
    "gợi ý lịch diễn ca Huế trong 2 ngày tới",                       # lịch diễn
    "xếp lịch mở cửa các lăng trong 3 ngày Tết giúp mình",           # lịch mở cửa
    "ở Huế 2 ngày thì nên ăn gì",                                    # có số ngày, không nhờ lập lịch
    "Huế có gì chơi trong 3 ngày",                                   # hỏi gợi ý chung, không có động từ nhờ + lịch
    "bài Lịch trình du lịch Huế ngắn ngày viết gì",                  # hỏi về một bài
    "lên lịch giúp mình đi ăn tối nay",                              # không có số ngày
    "tạo lịch tàu từ Huế đi Đà Nẵng 2 ngày tới",                     # lịch tàu
    "mình cần lịch mở cửa Đại Nội 2 ngày Tết",                       # "cần" + lịch mở cửa
    "xin lịch diễn Nhã nhạc 3 ngày tới",                             # "xin" + lịch diễn
    "cần mấy ngày để đi hết các lăng",                               # "cần" + số ngày, không có lịch
    "",
]


@pytest.mark.parametrize("cau", PHAI_NHAN)
def test_recognises_a_request_to_plan_a_multi_day_trip(cau):
    assert nho_len_lich(cau)


@pytest.mark.parametrize("cau", KHONG_NHAN)
def test_ignores_sentences_that_only_look_like_a_planning_request(cau):
    assert not nho_len_lich(cau)


def _trace(**kw) -> AnswerTrace:
    nguon = (PackedSource(id=1, title="Lịch trình du lịch Huế ngắn ngày", heading_path=("Gợi ý",), excerpts=("Ngày 1 đi Đại Nội.",), source="guides/lich trinh ngan ngay.md"),)
    return AnswerTrace(answer="Ngày 1: Đại Nội [1].", cited=nguon, **kw)


BAT = dataclasses.replace(AssistantFlags(), len_lich_dan_trang=True, may_have_changed_notice=False)  # điều kiện "trang Lên kế hoạch đang bật" kiểm ở `_before_model`


def test_set_notice_adds_the_pointer_and_keeps_the_answer():
    trace = _trace(nho_len_lich=True)
    set_notice(trace, BAT)
    assert trace.notice == CAU_DAN_TRANG and TEN_TRANG in CAU_DAN_TRANG  # giao diện tìm đúng cụm `TEN_TRANG` để làm link
    assert trace.answer == "Ngày 1: Đại Nội [1]."
    tu_choi = AnswerTrace(answer=INSUFFICIENT_ANSWER, cited=(), nho_len_lich=True)  # kho không trả lời được vẫn trỏ sang trang
    set_notice(tu_choi, BAT)
    assert tu_choi.notice == CAU_DAN_TRANG


def test_turn_not_marked_or_itinerary_turn_gets_no_pointer():
    for trace in (_trace(), _trace(nho_len_lich=True, bieu_mau=True), _trace(nho_len_lich=True, lich_v2={"lich": {}}), _trace(nho_len_lich=True, lich={"x": 1})):
        set_notice(trace, BAT)
        assert CAU_DAN_TRANG not in (trace.notice or "")
