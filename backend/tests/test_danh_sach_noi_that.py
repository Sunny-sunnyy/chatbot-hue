"""Cờ `danh_sach_noi_that` (20/11) — câu XIN DANH SÁCH có nguồn kho ⇒ code nối một dòng "danh sách có thể chưa đủ" vào dòng ghi chú.
Hàm thuần + chỗ gắn ở `set_notice`; không model, không mạng, không Qdrant. Câu trong test tự đặt (không phải câu bộ đo).
Đây KHÔNG phải bằng chứng trên câu trả lời thật — phần đó là bộ dò độc lập + một lượt thật qua giao diện."""
import dataclasses

import pytest

from llm.assistant import AnswerTrace, AssistantFlags, set_notice
from llm.danh_sach import CAU_DANH_SACH, hoi_ve_mot_noi, xin_danh_sach
from llm.full_corpus_prompt import CAU_Y_THIEU, INSUFFICIENT_ANSWER
from retrieval.full_corpus_context import PackedSource


@pytest.mark.parametrize("cau", [
    "Ở Huế có những quán nào mở cửa từ sáng sớm?",
    "những quán chay nào có chỗ ngồi ngoài vườn",
    "Các lăng vua nào đang mở cho khách tham quan?",
    "Huế có những lễ hội nào vào mùa xuân",
    "Kể hết các lăng trong bài đó giúp mình",
    "liệt kê các quán cà phê ven sông",
    "cho mình danh sách các làng nghề quanh Huế",
    "Kể tên những món đặc sản nên thử",
])
def test_recognises_requests_for_a_list(cau):
    assert xin_danh_sach(cau)


@pytest.mark.parametrize("cau", [
    "Cơm hến ăn ở quán nào ngon?",                      # xin MỘT gợi ý, không phải cả danh sách
    "Lăng Tự Đức mở cửa mấy giờ?",
    "Lăng Minh Mạng với lăng Tự Đức, lăng nào xa trung tâm hơn?",   # so sánh
    "Trong các quán vừa nêu, quán nào gần cầu Trường Tiền nhất?",   # chọn một
    "trong các quán vừa nêu quán nào gần nhất",                     # bộ dò mù của E 20/11 (B18): hỏi tiếp chọn MỘT trong các nơi đã nêu
    "trong số những lăng đó lăng nào đẹp",
    # review E 20/11 (F1): chữ "nào" thuộc cụm hỏi GIỜ / CÁCH / THỜI ĐIỂM ("lúc nào", "khi nào", "thế nào", "mùa nào"…) của nhiều nơi — không phải xin danh sách
    "các lăng này mở cửa lúc nào",
    "những quán đó mở cửa đến khi nào",
    "các lễ hội ở Huế diễn ra khi nào",
    "các chùa ở Huế vào cửa thế nào, có mất vé không",
    "những điểm đó đi lại như thế nào",
    "các quán này giá cả thế nào",
    "các bãi biển ở Huế mùa nào đẹp",
    "những món đó ăn vào lúc nào trong ngày",
    "các lăng vua nên đi vào buổi nào",
    "các chợ ở Huế họp vào giờ nào",
    "các nhà vườn này bán vé ở chỗ nào",
    "Vé vào các lăng giá bao nhiêu?",                   # "các lăng" nhưng hỏi giá
    "Các bạn cho mình hỏi đường ra chợ Đông Ba",
    "Đi Huế 2 ngày nên ở khách sạn hay homestay?",
    "Kể cho mình nghe về vua Tự Đức",
    "Những lưu ý khi đi thuyền trên sông Hương là gì?",  # "lưu ý" không phải nơi / món
    "",
])
def test_ignores_sentences_that_only_look_like_a_list_request(cau):
    assert not xin_danh_sach(cau)


def test_question_naming_one_cited_place_is_about_that_place():
    assert hoi_ve_mot_noi("Các món ở quán O Giàu gồm những món nào?", ["Quán O Giàu"])
    assert not hoi_ve_mot_noi("Ở Huế có những quán nào mở sớm?", ["Quán O Giàu", "Bún bò Mệ Kéo"])
    assert not hoi_ve_mot_noi("những quán nào ngon", ["Huế"])  # tên quá ngắn không tính


def _trace(cau: str | None, **kw) -> AnswerTrace:
    nguon = (PackedSource(id=1, title="Quán O Giàu", heading_path=("Thông tin",), excerpts=("Quán mở từ 6 giờ sáng.",), source="foods/restaurants/quan o giau.md"),)
    return AnswerTrace(answer="Quán O Giàu mở từ 6 giờ sáng [1].", cited=nguon, xin_danh_sach=cau, **kw)


CAU = "Ở Huế có những quán nào mở cửa từ sáng sớm?"
BAT = dataclasses.replace(AssistantFlags(), danh_sach_noi_that=True)


def test_set_notice_adds_the_line_for_a_list_request_with_sources_and_keeps_the_answer():
    trace = _trace(CAU)
    set_notice(trace, BAT)
    assert trace.notice == CAU_DANH_SACH
    assert trace.answer == "Quán O Giàu mở từ 6 giờ sáng [1]."


def test_flag_off_never_marks_the_turn_so_notice_is_unchanged():
    # cờ tắt ⇒ `_before_model` không đặt `xin_danh_sach` ⇒ `set_notice` không có gì để nối
    trace = _trace(None)
    set_notice(trace, AssistantFlags())
    assert trace.notice is None


@pytest.mark.parametrize("trace", [
    AnswerTrace(answer=INSUFFICIENT_ANSWER, cited=(), xin_danh_sach=CAU),                                   # câu từ chối: không có nguồn trích
    _trace(CAU, bieu_mau=True),                                                                             # lượt biểu mẫu lịch
    _trace(CAU, lich_v2={"lich": {}}),                                                                      # lượt có lịch bản 2
    _trace("Các món ở quán O Giàu gồm những món nào?"),                                                     # hỏi về MỘT nơi được trích
])
def test_set_notice_skips_refusals_itinerary_turns_and_single_place_questions(trace):
    set_notice(trace, BAT)
    assert CAU_DANH_SACH not in (trace.notice or "")


def test_set_notice_skips_answers_with_a_missing_idea_line():
    trace = _trace(CAU)
    trace.answer = f"Quán O Giàu mở từ 6 giờ sáng [1].\n{CAU_Y_THIEU} quán mở sau 22 giờ."
    set_notice(trace, BAT)
    assert trace.notice is None
