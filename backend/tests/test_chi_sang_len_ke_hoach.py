"""Cờ `chi_sang_len_ke_hoach` (19/11/2026, plan private `data/len_lich_chat_2026-11-19/PLAN.md`) — lời NHỜ XẾP LỊCH gõ tự do trong ô chat mà câu trả
lời là câu từ chối khuôn ⇒ câu cố định chỉ sang trang Lên kế hoạch. 0 USD, không model, không bộ tìm.

Giữ: (1) hàm thuần chỉ nhận lời nhờ xếp lịch, không nhận câu hỏi VỀ lịch / chi phí / lịch đã có; (2) loại `xep_lich` chỉ được gán khi đủ cờ, cuộc chưa
có lịch, không phải lượt biểu mẫu; (3) câu cố định đi đúng đường `_noi_that_lam_thay` (chỉ thay câu từ chối khuôn; là câu từ chối với log và bộ chấm).
Không phải bằng chứng model thật trả câu từ chối khuôn ở các lượt này — phần đó ở lượt có phí.
"""
from types import SimpleNamespace

import pytest

from evaluation.full_corpus_eval import is_refusal
from llm.assistant import ROUTE_TRO_LY_HUE, AnswerTrace, AssistantFlags, _finish_generated, _loai_lam_thay, web_gate_open
from llm.full_corpus_prompt import CAU_LAM_THAY, INSUFFICIENT_ANSWER, REFUSAL_ANSWERS
from llm.lam_thay import DAT_CHO, XEP_LICH, nho_xep_lich

NHO = "lên lịch 3 ngày 2 đêm đi Huế giúp mình"
BANG = object()   # cờ biểu mẫu đòi có bảng lịch; test này không đọc bảng


@pytest.mark.parametrize("cau", [
    NHO,
    "Xếp giúp mình lịch trình 2 ngày ở Huế nhé",
    "lập kế hoạch đi Huế 3n2đ cho nhà mình được không",
    "bạn lên cho mình một lịch trình tham quan Huế",
    "Lịch 1 ngày chỉ đi các lăng, xuất phát 8 giờ",                 # mở đầu bằng cụm lịch + số ngày, không có từ hỏi
    "tụi mình tới Huế 2 ngày 1 đêm",                               # kể chuyến đi, không hỏi gì
    "Chiều mai mới tới nơi, xếp giúp mình với",                    # "xếp giúp" ở cuối câu
    # sau bộ dò của người khác (19/11, một lần sửa): "sắp" / "gợi ý" làm động từ lập lịch · ràng buộc tiền không phải câu hỏi chi phí
    "bạn sắp cho mình lịch 3 ngày ở Huế đi các làng nghề",
    "gợi ý lịch trình Huế 3 ngày 2 đêm theo từng buổi",
    "nhờ bạn sắp xếp lịch trình đi Huế 4 ngày cho cả nhà, ít tiền thôi",
])
def test_requests_for_an_itinerary_are_recognised(cau):
    assert nho_xep_lich(cau) is True


@pytest.mark.parametrize("cau", [
    "lịch lễ hội tháng 12 ở Huế có gì",                             # hỏi VỀ một loại lịch khác
    "lịch diễn Nhã nhạc ở Duyệt Thị Đường",
    "cho mình lịch tàu Huế – Đà Nẵng buổi sáng",
    "lịch mở cửa Đại Nội dịp Tết",
    "đi Huế 3 ngày 2 đêm hết khoảng bao nhiêu",                      # hỏi chi phí
    "đi Huế 2 ngày thì nên đi mấy điểm",                             # xin lời khuyên, có từ hỏi
    "lên lịch đi Huế 2 ngày hết bao nhiêu tiền",                     # có động từ lập lịch nhưng là hỏi chi phí
    "nên lên lịch đi Huế thế nào cho hợp lý",                        # hỏi cách làm
    "bỏ điểm đầu tiên khỏi lịch",                                    # sửa lịch đã có
    "lịch này dày quá, bớt giúp mình",
    "tóm gọn lịch trình 2 ngày để mình chép",                        # việc bằng chữ
    "lịch sử Huế 200 năm có gì đáng nhớ",                            # "lịch sử" không phải "lịch"
    "hãng xe nào ở Huế nhận lên lịch trình riêng cho đoàn đông người",   # sau bộ dò: có động từ lập lịch nhưng là hỏi AI làm dịch vụ đó
    "xep lich hue 2n1d giup minh",                                   # SÓT có chủ ý: không dấu (sản phẩm chỉ nhận tiếng Việt có dấu)
    "xếp giúp mình hành lý vào cốp xe thế nào",                      # "xếp giúp" nhưng không ở cuối câu và có từ hỏi
    "Đại Nội mở cửa mấy giờ",
    "",
])
def test_questions_about_schedules_and_existing_itineraries_are_not_caught(cau):
    assert nho_xep_lich(cau) is False


DU = AssistantFlags(router=True, tim_them=True, tra_web=True, noi_that_lam_thay=True, lich_trinh_bieu_mau=True, bang_lich=BANG, chi_sang_len_ke_hoach=True)


@pytest.mark.parametrize("flags, kw, mong", [
    (DU, {}, XEP_LICH),
    (AssistantFlags(noi_that_lam_thay=True, lich_trinh_bieu_mau=True, bang_lich=BANG), {}, None),                                   # cờ mới tắt
    (AssistantFlags(lich_trinh_bieu_mau=True, bang_lich=BANG, chi_sang_len_ke_hoach=True), {}, None),                               # thiếu `noi_that_lam_thay`
    (AssistantFlags(noi_that_lam_thay=True, chi_sang_len_ke_hoach=True), {}, None),                                 # không có trang Lên kế hoạch
    (DU, {"lich_luu": {"khung": {"ngay": []}}}, None),                                                             # cuộc đã có lịch
    (DU, {"bieu_mau": True}, None),                                                                                # lượt biểu mẫu
])
def test_kind_is_assigned_only_with_all_flags_and_no_saved_itinerary(flags, kw, mong):
    assert _loai_lam_thay(NHO, flags, AnswerTrace(**kw)) == mong


def test_existing_kinds_win_and_missing_dependencies_do_not_raise():
    assert _loai_lam_thay("đặt giúp mình một phòng đôi cho tối thứ bảy", DU, AnswerTrace()) == DAT_CHO   # loại đang có không đổi
    AssistantFlags(chi_sang_len_ke_hoach=True)   # cờ bật mà thiếu cờ phụ thuộc: im lặng, không ném lỗi (test khác tự tắt biểu mẫu vẫn chạy được)


def test_fixed_sentence_replaces_only_the_boilerplate_refusal_and_counts_as_refusal():
    cau = CAU_LAM_THAY[XEP_LICH]
    assert "(#/len-ke-hoach)" in cau and "http" not in cau and cau in REFUSAL_ANSWERS and is_refusal(cau)
    trace = AnswerTrace(route=ROUTE_TRO_LY_HUE, lam_thay=XEP_LICH, generated=SimpleNamespace(text=INSUFFICIENT_ANSWER))
    _finish_generated(trace, DU)
    assert trace.answer == cau and trace.fixed_outcome == "lam_thay" and not web_gate_open(trace, DU, object())
    assert trace.tools == [{"name": "lam_thay", "ms": 0.0, "loai": XEP_LICH}]
    co_dap_an = AnswerTrace(route=ROUTE_TRO_LY_HUE, lam_thay=XEP_LICH, generated=SimpleNamespace(text="Hai ngày ở Huế có thể đi Đại Nội [1]."),
                            so_nguon=None)
    assert co_dap_an.lam_thay == XEP_LICH   # model trả lời được từ kho ⇒ đường thay không chạy (khoá ở `test_noi_that_lam_thay`: câu khác câu khuôn không bị đụng)
