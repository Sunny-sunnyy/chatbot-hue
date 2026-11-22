"""Phép kiểm số (thời tiết / khoảng cách) trượt ⇒ gỡ câu chứa số lạ, không rút cả câu trả lời (21/11/2026, plan
`report_agent/2026-11-21/c_phuc_hoi_sau_kiem_plan.md`). Chữ model dựng tay, không gọi model, không Qdrant: chỉ kiểm phần code chạy SAU khi model viết.
Hai chiều: 8 ca model tự thêm số (4 thời tiết, 4 khoảng cách) ⇒ số đó không tới người dùng; ca đối chứng ⇒ chữ giữ nguyên."""
import pytest

from llm import assistant as at
from llm import khoang_cach as kc
from llm import thoi_tiet as tt
from llm.assistant import AnswerTrace
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from retrieval.full_corpus_context import PackedSource
from test_b5b_thoi_tiet import WEATHER, du_bao_ok
from test_khoang_cach import BANG

KHOI = tt.khoi_du_bao(du_bao_ok(), 1, 1)  # một ngày: 23–27 °C, khả năng mưa 80 %
DONG = kc.ket_qua(BANG, "a", "b")  # "khoảng 4,0 km đường đi, khoảng 10 phút đi xe"
KHO = PackedSource(1, "Bài kho", (), ("Chùa nằm bên sông, mở cửa buổi sáng. Nên mang ô khi trời mưa.",), "diem-den/bai.md")


def luot(text, query="Câu hỏi?", history=(), thoi_tiet=False, khoang_cach=False, **ctx):
    """Một lượt đã qua bộ kiểm trích dẫn, tới đúng chỗ `_finish_generated` chạy phép kiểm số rồi phần code nối. Nguồn [1] = bài kho;
    [2] = nguồn hệ thống (dự báo hoặc khoảng cách)."""
    he_thong = (PackedSource(2, "Dự báo", (), (KHOI,), tt.NGUON_SOURCE) if thoi_tiet else PackedSource(2, "Khoảng cách", (), DONG, kc.NGUON_SOURCE))
    trace = AnswerTrace(answer=text, so_nguon=[KHO, he_thong], history=tuple(history))
    at.check_citations(trace)
    assert trace.citation_error is None, "ca dựng sai: chữ model phải qua bộ kiểm trích dẫn trước"
    trace.thoi_tiet_ctx = {"bao_lu": False, "ngoai_7": False, "buoi": False, "co_cong_cu": thoi_tiet, "tu_khoa": thoi_tiet, **ctx}
    if thoi_tiet:
        trace.thoi_tiet = {"trang_thai": "ok", "khoi": KHOI, "bao_lu": ctx.get("bao_lu", False)}
    if khoang_cach:
        trace.khoang_cach = [{"diem_a": "a", "diem_b": "b", "dong": DONG}]
    at.kiem_so_sau_khi_viet(trace, text, WEATHER, query)
    at._thoi_tiet_cuoi(trace)
    return trace


# ---------- hàm thuần gỡ câu ----------

def test_remove_sentence_or_list_line_keeps_the_rest_verbatim():
    van = "Câu một [1]. Câu hai có 35 độ [2]. Câu ba [1]."
    a = van.index("35")
    assert at.go_cau_chua(van, [(a, a + 2)]) == "Câu một [1]. Câu ba [1]."
    ds = "Mở đầu [1]:\n- dòng một [1]\n- dòng hai 50 mm [2]. Thêm ý.\n- dòng ba [1]\n\nKết [1]."
    a = ds.index("50")
    # gạch đầu dòng nhiều câu: chỉ mất câu có số lạ, ký hiệu đầu dòng + câu còn lại ở lại; gạch đầu dòng một câu: mất cả dòng
    assert at.go_cau_chua(ds, [(a, a + 2)]) == "Mở đầu [1]:\n- dòng một [1]\n- Thêm ý.\n- dòng ba [1]\n\nKết [1]."
    mot_cau = "Mở đầu [1]:\n- dòng một [1]\n- dòng hai 50 mm [2]\n- dòng ba [1]"
    a = mot_cau.index("50")
    assert at.go_cau_chua(mot_cau, [(a, a + 2)]) == "Mở đầu [1]:\n- dòng một [1]\n- dòng ba [1]"
    that = "- Lăng nên xem 1,5–2 giờ. [4] Như vậy bạn xong khoảng 17h20, trước giờ đóng cửa. Mức dự phòng chỉ còn khoảng 10–40 phút."
    a = that.index("10–40")
    assert at.go_cau_chua(that, [(a, a + 10)]) == "- Lăng nên xem 1,5–2 giờ. [4] Như vậy bạn xong khoảng 17h20, trước giờ đóng cửa."  # dạng của lượt thật 21/11
    assert at.go_cau_chua(van, []) == van
    # trích dẫn đứng SAU dấu chấm: không cắt giữa câu và "[2]" của nó ⇒ câu kế (không có dấu chấm ngăn) đi theo — gỡ rộng hơn, không để sót số
    sau_cham = "Trời 35 độ. [2] Chùa mở cửa buổi sáng [1]. Câu ba [1]."
    assert at.go_cau_chua(sau_cham, [(5, 7)]) == "Câu ba [1]."


# ---------- 4 ca thời tiết: số model tự thêm không tới người dùng ----------

@pytest.mark.parametrize("text, so_la, nac, con_lai", [
    # câu giữa đoạn văn ⇒ gỡ đúng câu đó
    ("Mai Huế 23–27 °C, khả năng mưa 80 % [2]. Buổi trưa có thể lên tới 35 độ [2]. Chùa mở cửa buổi sáng [1].", ["35"], 1,
     "Mai Huế 23–27 °C, khả năng mưa 80 % [2]. Chùa mở cửa buổi sáng [1]."),
    # dòng gạch đầu dòng ⇒ gỡ cả dòng
    ("Dự báo ngày mai [2]:\n- Nhiệt độ 23–27 °C [2]\n- Lượng mưa khoảng 50 mm [2]\n- Nên mang ô [1]", ["50"], 1,
     "Dự báo ngày mai [2]:\n- Nhiệt độ 23–27 °C [2]\n- Nên mang ô [1]"),
    # cả câu trả lời là câu có số lạ ⇒ không còn gì ⇒ câu dẫn cố định (khối số liệu của hệ thống nối sau)
    ("Mai Huế khoảng 35 độ [2].", ["35"], 2, tt.CAU_DAN_DU_BAO),
    # phần còn lại không còn trích dẫn nào ⇒ không đứng được ⇒ câu dẫn cố định
    ("Mai trời nóng tới 35 độ [2]. Bạn nhớ mang ô nhé.", ["35"], 2, tt.CAU_DAN_DU_BAO),
])
def test_invented_weather_number_is_removed_not_retracted(text, so_la, nac, con_lai):
    trace = luot(text, "Mai Huế thời tiết thế nào?", thoi_tiet=True)
    assert trace.thoi_tiet_kiem == so_la and trace.citation_error is None  # lần trượt vẫn được ghi; lượt không còn báo lỗi
    assert trace.kiem_so_go["nac"] == nac and trace.kiem_so_go["thoi_tiet"] == so_la and trace.kiem_so_go["so_ky_tu_go"] > 0
    assert trace.answer == f"{con_lai}\n\n{KHOI}"  # khối dự báo vẫn nối
    assert so_la[0] not in at.chu_cua_model(trace) and trace.vet["kiem_so_go"]["chu_model"] == text


def test_weather_number_without_tool_keeps_kho_sentence():
    trace = luot("Chùa nằm bên sông [1]. Mùa này trời khoảng 30 °C [1].", "Chùa ở đâu?")
    assert trace.answer == "Chùa nằm bên sông [1]." and trace.kiem_so_go["nac"] == 1 and [s.id for s in trace.cited] == [1]


def test_storm_turn_still_gets_official_bulletin_line_after_removal():
    trace = luot("Mai có thể mưa tới 300 mm [2].", "Mai Huế có bão không?", thoi_tiet=True, bao_lu=True)
    assert "300" not in trace.answer and trace.citation_error is None
    assert trace.answer.startswith(tt.CAU_DAN_BAO_LU) and trace.answer.endswith(tt.CAU_BAO_LU) and KHOI in trace.answer


# ---------- 4 ca khoảng cách ----------

@pytest.mark.parametrize("text, so_la, nac, con_lai", [
    ("Từ Điểm A đến Điểm B khoảng 4,0 km, khoảng 10 phút đi xe [2]. Nếu đi bộ thì mất khoảng 45 phút [2].", ["45"], 1,
     "Từ Điểm A đến Điểm B khoảng 4,0 km, khoảng 10 phút đi xe [2]."),
    ("Hai cách đi [2]:\n- Xe máy: khoảng 10 phút [2]\n- Xe đạp: khoảng 25 phút [2]", ["25"], 1, "Hai cách đi [2]:\n- Xe máy: khoảng 10 phút [2]"),
    ("Khoảng 5 km, đi xe 12 phút [2].", ["5", "12"], 2, INSUFFICIENT_ANSWER),
    ("Chùa mở cửa buổi sáng [1]. Từ đó sang Điểm B chừng 7 km [2].", ["7"], 1, "Chùa mở cửa buổi sáng [1]."),
])
def test_invented_distance_number_is_removed_not_retracted(text, so_la, nac, con_lai):
    trace = luot(text, "Từ A sang B bao xa?", khoang_cach=True)
    assert trace.khoang_cach_kiem == so_la and trace.citation_error is None
    assert trace.kiem_so_go == {"thoi_tiet": [], "khoang_cach": so_la, "nac": nac, "so_ky_tu_go": len(text) - (len(con_lai) if nac == 1 else 0)}
    assert trace.answer == con_lai
    assert [s.id for s in trace.cited] == sorted({int(n) for n in at.CITATION_PATTERN.findall(con_lai)})  # nguồn được trích tính lại trên chữ còn lại


# ---------- đối chứng: không có số lạ ⇒ chữ gửi đi giống hệt chữ model ----------

@pytest.mark.parametrize("text, query, history, kw", [
    ("Mai Huế 23–27 °C, khả năng mưa 80 % [2]. Nên mang ô [1].", "Mai Huế thế nào?", (), {"thoi_tiet": True}),
    ("Từ Điểm A đến Điểm B khoảng 4,0 km, khoảng 10 phút đi xe [2].", "Từ A sang B bao xa?", (), {"khoang_cach": True}),
    # người dùng tự nêu con số trong câu hỏi của lượt này ⇒ model được nhắc lại (hệ thống in 80 %, người dùng gõ 63 %)
    ("Khả năng mưa 63 % là khá cao, còn dự báo ngày mai là 80 % [2].", "Mưa 63 % thì có nhiều không?", (), {"thoi_tiet": True}),
    # … hoặc trong câu hỏi LIỀN TRƯỚC
    ("Mưa 2 mm chỉ là mưa nhỏ [2].", "Vậy có cần áo mưa không?", (("Lượng mưa 2 mm là sao?", "…"),), {"thoi_tiet": True}),
    # giờ đồng hồ ("lúc 13h") không phải thời lượng đi đường
    ("Bạn nên xuất phát lúc 13h cho kịp [1]. Quãng đường khoảng 4,0 km [2].", "Từ A sang B bao xa?", (), {"khoang_cach": True}),
    # soát khác hãng 22/11 (G9): "từ 6h đến 21h" là giờ mở cửa — "21h" đứng sau "đến" từng bị coi là thời lượng và cả câu bị gỡ
    ("Quán mở cửa từ 6h đến 21h [1]. Quãng đường khoảng 4,0 km [2].", "Từ A sang B bao xa?", (), {"khoang_cach": True}),
    ("Chợ đêm mở tới 23 giờ [1]. Quãng đường khoảng 4,0 km [2].", "Từ A sang B bao xa?", (), {"khoang_cach": True}),
])
def test_control_answer_without_unknown_number_is_untouched(text, query, history, kw):
    trace = luot(text, query, history, **kw)
    assert trace.kiem_so_go is None and trace.citation_error is None and "kiem_so_go" not in trace.vet
    assert at.chu_cua_model(trace) == text


def test_number_from_older_question_or_previous_answer_is_not_allowed():
    cu = (("Lượng mưa 2 mm là sao?", "…"), ("Chùa ở đâu?", "Hôm đó mưa 9 mm."))  # "2 mm": cách hai lượt; "9 mm": chỉ có ở câu TRẢ LỜI trước
    trace = luot("Mưa 2 mm chỉ là mưa nhỏ [2]. Mai mưa 80 % [2].", "Vậy có cần áo mưa không?", cu, thoi_tiet=True)
    assert trace.thoi_tiet_kiem == ["2"] and at.chu_cua_model(trace) == "Mai mưa 80 % [2]."
    trace = luot("Hôm đó mưa 9 mm [2]. Mai mưa 80 % [2].", "Vậy có cần áo mưa không?", cu, thoi_tiet=True)
    assert trace.thoi_tiet_kiem == ["9"]


def test_duration_written_with_h_is_still_checked():
    trace = luot("Đi xe mất 13h [2]. Chùa mở cửa buổi sáng [1].", "Từ A sang B bao xa?", khoang_cach=True)
    assert trace.khoang_cach_kiem == ["13"] and trace.answer == "Chùa mở cửa buổi sáng [1]."


def test_clock_time_rule_applies_to_model_text_only_not_to_the_allowed_set():
    nguon = "Bắt đầu lúc 8 giờ, đi xe 15 phút."
    assert kc.tap_so_theo_loai(nguon)["tg"] >= {"8", "15"}  # tập số được phép không hẹp đi vì luật giờ đồng hồ
    assert kc.kiem_so("Khởi hành 8 giờ, đi xe 15 phút.", kc.tap_so_theo_loai(nguon)) == []  # model viết lại không có "lúc" vẫn qua như trước
    assert kc.kiem_so("Bạn đến lúc 9h, đi xe mất 9h.", kc.tap_so_theo_loai(nguon)) == ["9"]  # "lúc 9h" bỏ qua; "mất 9h" là thời lượng ⇒ vẫn bắt
    assert kc.kiem_so("Mở cửa đến 21h. Đi xe mất tới 9h.", kc.tap_so_theo_loai(nguon)) == ["9"]  # "đến 21h" là giờ đồng hồ; "mất tới 9h" vẫn là thời lượng


def test_itinerary_turn_keeps_old_retraction():
    trace = AnswerTrace(answer="Ngày 1 đi xe 45 phút [2].", so_nguon=[KHO, PackedSource(2, "Khoảng cách", (), DONG, kc.NGUON_SOURCE)])
    at.check_citations(trace)
    trace.lich, trace.khoang_cach = {"nguon": []}, [{"diem_a": "a", "diem_b": "b", "dong": DONG}]
    at.kiem_so_sau_khi_viet(trace, trace.answer, WEATHER, "Lên lịch 1 ngày")
    assert trace.citation_error is not None and trace.kiem_so_go is None and trace.answer == "Ngày 1 đi xe 45 phút [2]."


# ---------- đường stream: chữ đã hiện có câu bị gỡ ⇒ `thay_chu` mang chữ cuối, trước `sources` ----------

def test_stream_sends_replace_text_before_sources_when_a_sentence_was_removed():
    import time

    from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents, _copy_trace_metrics
    from test_chat_stream import parse_sse

    text = "Từ Điểm A đến Điểm B khoảng 4,0 km [2]. Nếu đi bộ thì mất khoảng 45 phút [2]. Chùa mở cửa buổi sáng [1]."
    stream = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter())
    da_hien = [stream.delta(text[:40]), stream.delta(text[40:])]  # người dùng đã thấy cả chữ model trước khi kiểm
    trace = luot(text, "Từ A sang B bao xa?", khoang_cach=True)
    events = parse_sse(da_hien + stream.finish(trace))
    cuoi = "Từ Điểm A đến Điểm B khoảng 4,0 km [2]. Chùa mở cửa buổi sáng [1]."
    assert [name for name, _ in events] == ["delta", "delta", "thay_chu", "sources", "done"]
    assert dict(events)["thay_chu"] == {"text": cuoi} and [s["id"] for s in dict(events)["sources"]] == [1, 2]
    assert dict(events)["done"]["outcome"] == "success" and stream.metrics["thay_chu"] is True
    _copy_trace_metrics(trace, stream.metrics)
    assert stream.metrics["kiem_so_go"] == {"nac": 1, "n_thoi_tiet": 0, "n_khoang_cach": 1, "so_ky_tu_go": len(text) - len(cuoi)}  # số đếm, không chữ
    # đối chứng: không có số lạ ⇒ không có sự kiện mới, số đo để None
    stream = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter())
    trace = luot(cuoi, "Từ A sang B bao xa?", khoang_cach=True)
    events = parse_sse([stream.delta(cuoi)] + stream.finish(trace))
    _copy_trace_metrics(trace, stream.metrics)
    assert "thay_chu" not in dict(events) and stream.metrics["thay_chu"] is None and stream.metrics["kiem_so_go"] is None


# ---------- review phiên B 21/11/2026 (M1 + m1 + m2 + m3) ----------

@pytest.mark.parametrize("text, query, kw, so_la", [
    # M1: số trong câu hỏi KHÔNG kèm đơn vị của phép kiểm (ngày tháng, số người) không mở cửa cho số model tự thêm trùng giá trị
    ("Ngày đó trời khoảng 30 °C [2].", "Ngày 30/11 mình tới Huế, trời thế nào?", {"thoi_tiet": True}, ["30"]),
    ("Quãng đường khoảng 15 km [2].", "Đoàn mình 15 người, từ A sang B bao xa?", {"khoang_cach": True}, ["15"]),
    ("Đi xe mất khoảng 15 phút [2].", "Mình nghe nói cách 15 km, đi mất bao lâu?", {"khoang_cach": True}, ["15"]),  # km của câu hỏi không mở cho phút
    ("Khả năng mưa khoảng 50 % [2].", "Vé giảm 50 % thì còn bao nhiêu, mai trời thế nào?", {"thoi_tiet": True}, ["50"]),  # "%" không phải về mưa
])
def test_question_number_without_the_checks_unit_does_not_widen_the_allowed_set(text, query, kw, so_la):
    trace = luot(text, query, **kw)
    assert (trace.thoi_tiet_kiem or trace.khoang_cach_kiem) == so_la and so_la[0] not in at.chu_cua_model(trace) and trace.kiem_so_go["nac"] == 2


def test_question_number_with_unit_is_allowed_wherever_the_rain_word_stands():
    assert tt.so_kem_don_vi("63% thì mưa nhiều k? 2mm là mưa phùn hay sao, mai nóng 45 độ à") == {"63", "2", "45"}
    assert tt.so_kem_don_vi("Ngày 30/11 đoàn 15 người, vé giảm 50 %") == set()
    trace = luot("Đi 2 tiếng là vừa, quãng đường khoảng 4,0 km [2].", "Mình định đi 2 tiếng, từ A sang B bao xa?", khoang_cach=True)
    assert trace.kiem_so_go is None


def test_abbreviation_is_not_a_sentence_end_and_orphan_lead_line_is_removed():
    van = "Chùa mở cửa buổi sáng [1]. Từ TP. Huế sang Điểm B chừng 7 km [2]."
    a = van.index("7 km")
    assert at.go_cau_chua(van, [(a, a + 4)]) == "Chùa mở cửa buổi sáng [1]."  # m1: không còn mảnh "Từ TP."
    ket_o_hue = "Chùa ở Huế. Đi mất 45 phút [2]."
    a = ket_o_hue.index("45")
    assert at.go_cau_chua(ket_o_hue, [(a, a + 7)]) == "Chùa ở Huế."  # "Huế." vẫn là hết câu
    ds = "Chùa mở cửa buổi sáng [1].\n\nHai cách đi [2]:\n- Xe đạp: khoảng 25 phút [2]\n- Đi bộ: khoảng 45 phút [2]"
    assert at.go_cau_chua(ds, [(ds.index("25"), ds.index("25") + 2), (ds.index("45"), ds.index("45") + 2)]) == "Chùa mở cửa buổi sáng [1]."  # m2
    con_mot = at.go_cau_chua(ds, [(ds.index("45"), ds.index("45") + 2)])
    assert con_mot == "Chùa mở cửa buổi sáng [1].\n\nHai cách đi [2]:\n- Xe đạp: khoảng 25 phút [2]"  # còn một dòng danh sách ⇒ dòng dẫn ở lại
    khong_ds = "Lưu ý:\nĐi bộ mất 45 phút [2].\nChùa mở cửa buổi sáng [1]."
    a = khong_ds.index("45")
    assert at.go_cau_chua(khong_ds, [(a, a + 2)]) == "Lưu ý:\nChùa mở cửa buổi sáng [1]."  # dòng dẫn vốn không đứng trước danh sách ⇒ không đụng
    trace = luot("Hai cách đi [2]:\n- Xe đạp: khoảng 25 phút [2]\n- Đi bộ: khoảng 45 phút [2]", "Từ A sang B bao xa?", khoang_cach=True)
    assert trace.answer == INSUFFICIENT_ANSWER and trace.kiem_so_go["nac"] == 2


def test_turn_with_a_removed_sentence_is_not_saved_to_the_answer_cache():
    from api.cache_tra_loi import luot_luu_duoc
    assert luot_luu_duoc(luot("Chùa nằm bên sông [1].", "Chùa ở đâu?"), False) is True  # đối chứng: lượt kho thường vẫn lưu được
    assert luot_luu_duoc(luot("Chùa nằm bên sông [1]. Mùa này trời khoảng 30 °C [1].", "Chùa ở đâu?"), False) is False  # m3
