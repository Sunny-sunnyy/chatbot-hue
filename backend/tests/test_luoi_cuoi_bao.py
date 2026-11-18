"""Lưới cuối câu bão / lũ (18/11): CHÍNH câu người dùng gõ khớp lưới bão mà thứ sắp gửi (câu trả lời, mục web, lời báo lỗi) chưa có câu bản tin chính thức
+ 112 ⇒ code đưa câu đó vào dòng ghi chú (`notice`) hoặc vào lời báo lỗi. Vì sao: câu 112 vốn chỉ được nối ở một chỗ trong đường trả lời thường — lượt kết thúc
sớm / đi đường khác (xếp ngoài phạm vi, trò chuyện, lần tìm đầu rỗng, sửa lịch, lỗi model) thì mất; ba lượt soát mù 18/11 đều tìm ra lỗi cùng gốc này.
Logic thuần + sự kiện SSE dựng từ trace có sẵn; không gọi model."""
import time

from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents, _error_response_for
from core.schema import GenerationError
from llm import thoi_tiet as tt
from llm import tra_web as tw
from llm.assistant import AnswerTrace, AssistantFlags, loi_bao_luoi_cuoi, luoi_cuoi_bao
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, MAY_HAVE_CHANGED_NOTICE, OUT_OF_SCOPE_ANSWER
from tests.test_chat_stream import parse_sse

BAT = AssistantFlags(router=True, tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True, du_bao=tt.lay_du_bao)
TAT = AssistantFlags(router=True, tim_them=True, thoi_tiet=True, du_bao=tt.lay_du_bao)
CAU_BAO = "Huế mấy hôm nay có bão không?"


def test_duong_11_xep_ngoai_pham_vi_van_co_cau_112_va_su_kien_notice():
    trace = AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=(), fixed_outcome="out_of_scope")
    assert luoi_cuoi_bao(CAU_BAO, trace, BAT) is True and trace.notice == tt.CAU_BAO_LU
    assert trace.answer == OUT_OF_SCOPE_ANSWER  # chữ câu trả lời không đổi ⇒ cờ từ chối / bộ đếm không đổi
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    events = parse_sse([stream.delta(trace.answer), *stream.fixed(trace)])
    assert ("notice", {"text": "", "an_toan": tt.CAU_BAO_LU}) in events and events[-1][0] == "done" and metrics["refusal"] is True  # câu an toàn tách riêng


def test_duong_13_tro_chuyen_va_duong_14_lan_tim_dau_rong():
    tro_chuyen = AnswerTrace(answer="Chào bạn, mình là trợ lý Huế.", cited=())
    assert luoi_cuoi_bao("Chào bạn, bão to quá nhỉ", tro_chuyen, BAT) and tro_chuyen.notice == tt.CAU_BAO_LU
    rong = AnswerTrace(answer=INSUFFICIENT_ANSWER, cited=(), fixed_outcome="refusal_no_sources")
    assert luoi_cuoi_bao(CAU_BAO, rong, BAT) and rong.notice == tt.CAU_BAO_LU  # tra web tắt / không mở: không còn đường nào khác mang câu 112
    co_web = AnswerTrace(answer=INSUFFICIENT_ANSWER, cited=(), fixed_outcome="refusal_no_sources", web={"outcome": "thien_tai", "text": tw.THIEN_TAI_TEXT})
    assert luoi_cuoi_bao(CAU_BAO, co_web, BAT) is False and co_web.notice is None  # mục web đã mang câu cố định có 112 ⇒ không lặp


def test_duong_15_luot_sua_lich_ghep_voi_dong_ghi_chu_da_co():
    trace = AnswerTrace(answer="", cited=(), notice=MAY_HAVE_CHANGED_NOTICE)  # lượt sửa lịch: giao diện không vẽ chữ, chỉ vẽ khung + dòng ghi chú
    assert luoi_cuoi_bao("Mai có bão, bỏ giúp mình lăng Tự Đức khỏi lịch", trace, BAT)
    assert trace.notice == f"{tt.CAU_BAO_LU} {MAY_HAVE_CHANGED_NOTICE}"  # câu an toàn đứng trước


def test_duong_16_loi_bao_khi_model_hoac_tim_kho_loi():
    goc = "Không thể tạo câu trả lời lúc này."
    assert loi_bao_luoi_cuoi(CAU_BAO, goc, BAT) == f"{goc}\n\n{tt.CAU_BAO_LU}"
    assert loi_bao_luoi_cuoi("Bún bò Huế ăn ở đâu?", goc, BAT) == goc
    da_co = f"{goc}\n\n{tt.CAU_BAO_LU}"
    assert loi_bao_luoi_cuoi(CAU_BAO, da_co, BAT) == da_co  # lời báo rút lại của lượt bão đã có câu 112 ⇒ không lặp
    sua = lambda m: loi_bao_luoi_cuoi(CAU_BAO, m, BAT)  # noqa: E731
    stream = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter(), sua_loi=sua)
    assert tt.CAU_BAO_LU in parse_sse(stream.failure(GenerationError("x")))[0][1]["message"]
    response = _error_response_for(GenerationError("x"), None, dict.fromkeys(STREAM_METRIC_FIELDS), sua)
    assert "112" in response.body.decode("utf-8")


def test_khong_them_khi_da_co_khi_cau_khong_khop_luoi_khi_co_tat_khi_luot_hoi_lai():
    da_co = AnswerTrace(answer=f"{INSUFFICIENT_ANSWER}\n\n{tt.CAU_BAO_LU}", cited=(), thoi_tiet_noi=tt.CAU_BAO_LU)
    assert luoi_cuoi_bao(CAU_BAO, da_co, BAT) is False and da_co.notice is None
    thuong = AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=(), fixed_outcome="out_of_scope")
    assert luoi_cuoi_bao("Giá vàng hôm nay bao nhiêu?", thuong, BAT) is False and thuong.notice is None
    assert luoi_cuoi_bao(CAU_BAO, AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=(), fixed_outcome="out_of_scope"), TAT) is False  # cờ câu bão tắt ⇒ như cũ
    assert luoi_cuoi_bao(CAU_BAO, AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=()), None) is False
    hoi_lai = AnswerTrace(answer="", cited=(), fixed_outcome="hoi_lai", clarify={"truong": []})
    assert luoi_cuoi_bao(CAU_BAO, hoi_lai, BAT) is False  # lượt chỉ có thẻ nút: không có chỗ vẽ dòng ghi chú


def test_luot_model_tu_chon_loai_bao_lu_roi_loi_thi_loi_bao_van_co_cau_112():
    """Soát tích hợp đợt 2 (18/11): câu gõ không có từ nào của lưới nhưng MODEL đã gọi công cụ thời tiết loại bão / lũ (`thoi_tiet_ctx["bao_lu_model"]`),
    rồi model lỗi / hết giờ giữa lượt ⇒ lời báo lỗi của cả đường luồng lẫn `/api/chat` phải có câu 112 (trước: chỉ lượt bị rút lại / chạm trần mới có)."""
    cau, goc = "Mai đi biển Thuận An thời tiết có nguy hiểm gì không?", "Không thể tạo câu trả lời lúc này."
    assert not tt.la_luot_bao_lu(cau, ())  # đúng ca: lưới từ khoá không khớp
    trace = AnswerTrace()
    sua = lambda m: loi_bao_luoi_cuoi(cau, m, BAT, trace.history, trace.thoi_tiet_ctx)  # noqa: E731 — như hai chỗ dựng `sua_loi` ở route
    assert sua(goc) == goc  # model chưa chọn loại bão / lũ (kể cả lượt chưa có ngữ cảnh thời tiết): lời báo nguyên
    trace.thoi_tiet_ctx = {"bao_lu": False}
    assert sua(goc) == goc
    trace.thoi_tiet_ctx = {"bao_lu": True, "bao_lu_model": True}  # `thoi_tiet(loai="bao_lu")` đặt hai khoá này
    for exc in (TimeoutError(), GenerationError("x")):
        stream = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter(), sua_loi=sua)
        assert tt.CAU_BAO_LU in parse_sse(stream.failure(exc))[0][1]["message"]
    response = _error_response_for(GenerationError("x"), None, dict.fromkeys(STREAM_METRIC_FIELDS), sua)
    assert "112" in response.body.decode("utf-8")


def test_cau_khong_khop_luoi_thi_su_kien_gui_ra_giong_het_khi_khong_co_luoi():
    """Giống byte: lượt không khớp lưới ⇒ chuỗi sự kiện y như trước khi có lưới cuối (không thêm `notice`, lời báo lỗi nguyên)."""
    def su_kien(sua_loi):
        trace = AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=(), fixed_outcome="out_of_scope")
        luoi_cuoi_bao("Giá vàng hôm nay bao nhiêu?", trace, BAT)
        stream = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), 0.0, sua_loi=sua_loi)
        return [stream.delta(trace.answer), *stream.fixed(trace)], StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), 0.0, sua_loi=sua_loi).failure(GenerationError("x"))
    sua = lambda m: loi_bao_luoi_cuoi("Giá vàng hôm nay bao nhiêu?", m, BAT)  # noqa: E731
    assert su_kien(sua) == su_kien(None)
    assert [e[0] for e in parse_sse(su_kien(None)[0])] == ["delta", "sources", "done"]


def test_chu_dong_la_cach_viet_khac_cua_giong():
    trace = AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=(), fixed_outcome="out_of_scope")
    assert luoi_cuoi_bao("Chiều nay Huế có dông không?", trace, BAT) and trace.notice == tt.CAU_BAO_LU


def test_cau_hoi_tiep_sau_cau_bao_cung_la_luot_bao_va_ghi_chu_thuong_khong_mang_co_an_toan():
    """A chốt 18/11: xét cả câu hỏi LIỀN TRƯỚC (như đường trả lời thường) — "thế có nên đi không" sau một câu bão mà rơi vào đường kết thúc sớm vẫn có
    câu 112; câu trước nữa thì không. Ghi chú thường ("có thể đã thay đổi") không mang cờ `an_toan`."""
    tiep = AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=(), fixed_outcome="out_of_scope", history=[("Huế có lũ không?", "…")])
    assert luoi_cuoi_bao("Thế có nên đi không?", tiep, BAT) and tiep.notice == tt.CAU_BAO_LU
    xa = AnswerTrace(answer=OUT_OF_SCOPE_ANSWER, cited=(), fixed_outcome="out_of_scope", history=[("Huế có lũ không?", "…"), ("Bún bò ăn ở đâu?", "…")])
    assert luoi_cuoi_bao("Thế có nên đi không?", xa, BAT) is False
    assert loi_bao_luoi_cuoi("Thế có nên đi không?", "Lỗi.", BAT, [("Chiều nay có dông không?", "…")]).endswith(tt.CAU_BAO_LU)
    thuong = AnswerTrace(answer="Vé vào cổng 200.000 đồng [1].", cited=(), notice=MAY_HAVE_CHANGED_NOTICE)
    events = parse_sse(StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter()).fixed(thuong))
    assert ("notice", {"text": MAY_HAVE_CHANGED_NOTICE}) in events


def test_su_kien_notice_tach_cau_an_toan_khoi_ghi_chu_thuong():
    """Giao diện vẽ câu an toàn đậm, ở lượt có lịch thì trên đầu khung; ghi chú thường ("có thể đã thay đổi") không đậm theo ⇒ hai phần đi hai trường."""
    trace = AnswerTrace(answer="", cited=(), notice=MAY_HAVE_CHANGED_NOTICE)
    assert luoi_cuoi_bao("Mai có bão, bỏ giúp mình lăng Tự Đức khỏi lịch", trace, BAT)
    events = parse_sse(StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter()).finish(trace))
    assert ("notice", {"text": MAY_HAVE_CHANGED_NOTICE, "an_toan": tt.CAU_BAO_LU}) in events
