"""Cờ `noi_dong_tam_ngung` (19/11) — CODE nối vào dòng ghi chú một câu "tạm ngừng khi lũ / lệnh cấm / thời tiết xấu" chép nguyên văn từ nguồn câu trả lời
ĐÃ TRÍCH, khi câu trả lời chưa nêu ý đó. Hàm thuần + chỗ gắn ở `set_notice`; không model, không mạng, không Qdrant.
Câu trong test tự đặt (không phải câu bộ đo). Đây KHÔNG phải bằng chứng trên câu trả lời thật — phần đó là bước "chạy lại bước nối" + lượt thật qua server."""
import dataclasses

import pytest

from llm.assistant import AnswerTrace, AssistantFlags, set_notice
from llm.full_corpus_prompt import MAY_HAVE_CHANGED_NOTICE
from llm.luu_y_nguon import dong_tam_ngung
from retrieval.full_corpus_context import PackedSource

DONG_NGUON = "- Khi nước lên to hoặc cảng vụ ra lệnh cấm, mọi chuyến đò đều tạm ngừng cho tới lúc an toàn. Khi đó, khách đổi vé ở quầy."
CAU_NGUON = "Khi nước lên to hoặc cảng vụ ra lệnh cấm, mọi chuyến đò đều tạm ngừng cho tới lúc an toàn."
NGUON = [("Thuyền trên sông", (f"- Khán giả mặc áo phao khi lên thuyền.\n{DONG_NGUON}",))]
MONG = f"Lưu ý trong nguồn «Thuyền trên sông»: {CAU_NGUON}"


def test_appends_exactly_one_source_sentence_when_answer_omits_it():
    assert dong_tam_ngung("Khán giả phải mặc áo phao [1].", NGUON) == MONG


@pytest.mark.parametrize("answer", [
    "Khán giả mặc áo phao [1]. Mùa mưa lũ hoặc khi có lệnh cấm, thuyền tạm ngừng xuất bến [1].",   # đã nêu ⇒ không nối trùng
    "Thuyền không xuất bến khi thời tiết xấu. [1]",
])
def test_no_duplicate_when_answer_already_states_it(answer):
    assert dong_tam_ngung(answer, NGUON) is None


@pytest.mark.parametrize("doan", [
    "- Khán giả mặc áo phao khi lên thuyền.\n- Thuyền chạy mỗi tối.",                                # không có ý
    "- Di tích tạm ngừng đón khách để tu bổ thành lũy.",                                             # "lũy" không phải "lũ"
    "- Nhà hàng tạm nghỉ trưa từ 14 giờ.",                                                           # tạm nghỉ, không điều kiện thời tiết
    "- Mùa mưa lũ kéo dài từ tháng 10.\n- Thuyền tạm ngừng vào thứ Hai để bảo dưỡng.",               # hai ý ở HAI dòng rời ⇒ không ghép
    "- Thuyền tạm ngừng. Mùa lũ thường từ tháng 10.",                                                # cùng dòng nhưng hai CÂU rời ⇒ không ghép
    "- " + "Vào mùa mưa lũ thuyền tạm ngừng " + "rất " * 120 + "lâu.",                               # câu quá dài ⇒ không cắt giữa câu, không nối
])
def test_returns_none_when_no_single_source_sentence_holds_the_idea(doan):
    assert dong_tam_ngung("Khán giả phải mặc áo phao [1].", [("Bài", (doan,))]) is None


def test_takes_first_cited_source_in_given_order_and_strips_list_markup():
    nguon = [("Bài A", ("- Giá vé 100.000 đồng.",)),
             ("Bài B", ("  4. **An toàn:** buổi diễn bị hoãn nếu thời tiết xấu.",)),
             ("Bài C", (DONG_NGUON,))]
    assert dong_tam_ngung("Vé 100.000 đồng [1].", nguon) == "Lưu ý trong nguồn «Bài B»: An toàn: buổi diễn bị hoãn nếu thời tiết xấu."


@pytest.mark.parametrize("dong, mong", [
    # đúng khuôn dòng thật: hai câu, câu sau mở bằng "Khi đó" ⇒ chỉ chép câu đầu
    (DONG_NGUON, CAU_NGUON),
    # viết tắt + số tiền có dấu chấm KHÔNG phải ranh câu
    ("- Ở TP. Huế, vé 1.200.000 đồng không hoàn khi thuyền tạm ngừng do mưa bão. Liên hệ quầy vé.",
     "Ở TP. Huế, vé 1.200.000 đồng không hoàn khi thuyền tạm ngừng do mưa bão."),
    # ý nằm ở câu mở bằng từ chỉ ngược ⇒ không chép
    ("- Mùa lũ thường từ tháng 10. Khi đó thuyền tạm ngừng nếu có lệnh cấm.", None),
    ("- Tại đây thuyền tạm ngừng khi có bão.", None),
    # dòng bảng ⇒ không chép
    ("| Mùa lũ | thuyền tạm ngừng khi có lệnh cấm |", None),
    # chữ thường sau dấu chấm không phải ranh câu (tách thừa sẽ ra câu cụt)
    ("- Thuyền tạm ngừng khi có lệnh cấm (theo quy định số 12. ban hành năm 2020) của cảng vụ.",
     "Thuyền tạm ngừng khi có lệnh cấm (theo quy định số 12. ban hành năm 2020) của cảng vụ."),
])
def test_copied_sentence_stands_alone(dong, mong):
    from llm.luu_y_nguon import cau_tam_ngung
    assert cau_tam_ngung(dong) == mong


def test_no_sources_or_empty_answer():
    assert dong_tam_ngung("Câu trả lời.", []) is None
    assert dong_tam_ngung("", NGUON) == MONG  # không có chữ model nhưng có nguồn được trích: hàm vẫn tất định (nơi gọi chỉ gọi khi có trích)


def _trace(answer, source="places/thuyen.md"):
    return AnswerTrace(route="tro_ly_hue", answer=answer,
                       cited=(PackedSource(id=2, title="Thuyền trên sông", heading_path=("An toàn",), excerpts=NGUON[0][1], source=source),))


def test_set_notice_flag_off_is_unchanged_and_on_adds_the_line_before_other_notes():
    tat, bat = AssistantFlags(may_have_changed_notice=True), AssistantFlags(may_have_changed_notice=True, noi_dong_tam_ngung=True)
    # nguồn thường ⇒ cờ tắt không có ghi chú; nguồn vé ⇒ cờ tắt có dòng "có thể đã thay đổi" (ca gặp nhau thật: câu thuyền trích bài vé)
    for src, cu in (("foods/x.md", None), ("travel/tickets/ve thuyen.md", MAY_HAVE_CHANGED_NOTICE)):
        t_tat, t_bat = _trace("Khán giả phải mặc áo phao [2].", src), _trace("Khán giả phải mặc áo phao [2].", src)
        set_notice(t_tat, tat)
        set_notice(t_bat, bat)
        assert t_tat.notice == cu and t_tat.luu_y_nguon is None
        assert t_bat.notice == (MONG if cu is None else f"{MONG} {cu}") and t_bat.luu_y_nguon == MONG   # dòng an toàn đứng TRƯỚC, không mất dòng cũ
        assert t_bat.answer == t_tat.answer                                                             # chữ câu trả lời không đổi


def test_storm_final_net_and_source_line_meet_in_one_turn_without_losing_either():
    """Lượt bão / lũ: lưới cuối đặt câu bản tin + 112 lên ĐẦU dòng ghi chú; dòng chép từ nguồn và ghi chú thường vẫn còn, đúng thứ tự."""
    from llm import thoi_tiet as tt
    from llm.assistant import luoi_cuoi_bao
    flags = AssistantFlags(may_have_changed_notice=True, noi_dong_tam_ngung=True, tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True,
                           du_bao=lambda *a, **k: None)  # hàm dự báo chỉ để dựng cờ; lưới cuối không gọi nó
    trace = _trace("Khán giả phải mặc áo phao [2].", "travel/tickets/ve thuyen.md")
    set_notice(trace, flags)
    assert luoi_cuoi_bao("Sắp có bão, đi thuyền nghe ca Huế cần biết gì?", trace, flags) is True
    assert trace.notice == f"{tt.CAU_BAO_LU} {MONG} {MAY_HAVE_CHANGED_NOTICE}"


@pytest.mark.parametrize("them", [{"bieu_mau": True}, {"lich": {"khung": {}}}, {"lich_v2": {"lich": {}}}])
def test_schedule_turns_do_not_get_the_line(them):
    """Lượt có lịch (biểu mẫu, công cụ lịch, lịch bản 2 / sửa lịch) không nhận dòng này — ghi chú của lượt đó y như cờ tắt."""
    tat, bat = AssistantFlags(may_have_changed_notice=True), AssistantFlags(may_have_changed_notice=True, noi_dong_tam_ngung=True)
    t_tat = dataclasses.replace(_trace("Khán giả phải mặc áo phao [2].", "travel/tickets/ve thuyen.md"), **them)
    t_bat = dataclasses.replace(t_tat)
    set_notice(t_tat, tat)
    set_notice(t_bat, bat)
    assert t_bat.notice == t_tat.notice == MAY_HAVE_CHANGED_NOTICE and t_bat.luu_y_nguon is None


def test_set_notice_does_nothing_for_refusal_or_answer_that_states_it():
    bat = AssistantFlags(noi_dong_tam_ngung=True)
    da_neu = _trace("Mùa mưa lũ thuyền tạm ngừng [2].")
    set_notice(da_neu, bat)
    assert da_neu.notice is None
    tu_choi = dataclasses.replace(_trace("x"), answer="Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.", cited=())
    set_notice(tu_choi, bat)
    assert tu_choi.notice is None


def test_stream_notice_event_puts_the_source_line_in_the_safety_part_and_is_unchanged_without_it():
    """Sự kiện `notice`: câu chép từ nguồn đi vào `an_toan` (giao diện vẽ nổi như câu bão / lũ); lượt không có câu đó ⇒ sự kiện y như trước."""
    import json

    from api.routes.chat import _notice_event
    from llm import thoi_tiet as tt

    def data(trace):
        return json.loads(_notice_event(trace).decode("utf-8").split("data: ", 1)[1])

    thuong = AnswerTrace(notice=MAY_HAVE_CHANGED_NOTICE)
    assert data(thuong) == {"text": MAY_HAVE_CHANGED_NOTICE}
    bao = AnswerTrace(notice=f"{tt.CAU_BAO_LU} {MAY_HAVE_CHANGED_NOTICE}")
    assert data(bao) == {"text": MAY_HAVE_CHANGED_NOTICE, "an_toan": tt.CAU_BAO_LU}
    co = AnswerTrace(notice=f"{MONG} {MAY_HAVE_CHANGED_NOTICE}", luu_y_nguon=MONG)
    assert data(co) == {"text": MAY_HAVE_CHANGED_NOTICE, "an_toan": MONG}
    chi = AnswerTrace(notice=MONG, luu_y_nguon=MONG)
    assert data(chi) == {"text": "", "an_toan": MONG}
    ca_hai = AnswerTrace(notice=f"{tt.CAU_BAO_LU} {MONG} {MAY_HAVE_CHANGED_NOTICE}", luu_y_nguon=MONG)  # lưới cuối câu bão đặt câu 112 lên đầu
    assert data(ca_hai) == {"text": MAY_HAVE_CHANGED_NOTICE, "an_toan": f"{tt.CAU_BAO_LU} {MONG}"}
