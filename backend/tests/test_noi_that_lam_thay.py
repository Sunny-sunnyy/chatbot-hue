"""Cờ `noi_that_lam_thay` (19/11/2026) — câu NHỜ TRỢ LÝ TỰ LÀM việc hệ thống không có (đặt chỗ, gửi thư / tin, xem tình trạng phòng) mà câu trả lời
đã là câu từ chối khuôn ⇒ code thay bằng câu nói thật giới hạn, kết thúc `lam_thay`, không mở mục web.

Ba lớp: (1) hàm thuần `nho_lam_thay` — không model, không kho; (2) chỗ thay + cổng web + dòng `done` — trace dựng tay; (3) lõi thật với model giả
+ bộ tìm thật (`deps`: cần Qdrant) ở cả đường không stream, stream, stream song song. Câu trong test tự đặt (không phải câu bộ đo).
Đây KHÔNG phải bằng chứng trên model thật — phần đó là lượt qua server ghi ở report của nhánh."""
import asyncio
import dataclasses
import json
import time
from types import SimpleNamespace

import pytest

from api.routes.chat import REMEMBERED_OUTCOMES, STREAM_METRIC_FIELDS, StreamEvents
from evaluation.full_corpus_eval import is_refusal
from llm.assistant import (AnswerTrace, AssistantFlags, ROUTE_TRO_LY_HUE, _finish_generated, _noi_that_lam_thay, answer_turn, answer_turn_stream,
                           answer_turn_stream_parallel, web_gate_open)
from llm.full_corpus_prompt import CAU_LAM_THAY, INSUFFICIENT_ANSWER, REFUSAL_ANSWERS
from llm.citations import CITATION_PATTERN
from llm.lam_thay import DAT_CHO, GUI, TINH_TRANG, nho_lam_thay
from test_chat_stream import parse_sse

CAU_DAT = "đặt giúp mình một phòng đôi cho tối thứ bảy gần sông Hương"


# ---------- (1) hàm thuần ----------
@pytest.mark.parametrize("cau, loai", [
    (CAU_DAT, DAT_CHO),
    ("cho mình xin link đặt phòng homestay đó", DAT_CHO),
    ("Bạn đặt bàn giúp mình tối nay 4 người nhé", DAT_CHO),
    ("Giúp mình đặt vé xem ca Huế tối mai", DAT_CHO),
    ("gửi lịch qua email cho mình với", GUI),
    ("Gửi giúp mình lịch qua Zalo", GUI),
    ("mình vừa gửi yêu cầu rồi, có phòng chưa vậy", TINH_TRANG),   # có chữ "gửi" nhưng là hỏi tình trạng
    ("đơn đặt phòng của mình xác nhận chưa", TINH_TRANG),
    # sau bộ dò của người khác (19/11): nhờ GỬI có chữ "đặt phòng" (không phải nhờ đặt) · tới số điện thoại · "email" làm động từ
    ("Gửi giấy xác nhận đặt phòng vào email của mình giúp với", GUI),
    ("gửi lịch 3 ngày này tới số điện thoại của em mình nhé", GUI),
    ("Email cho mình bản kế hoạch này được không", GUI),
    ("nhờ bạn đặt bàn 5 người tối nay ở quán đó", DAT_CHO),
    ("đặt vé này giúp mình nhé", DAT_CHO),
])
def test_requests_to_act_are_recognised_by_kind(cau, loai):
    assert nho_lam_thay(cau) == loai


@pytest.mark.parametrize("cau", [
    "cho mình xin địa chỉ và số điện thoại để đặt bàn",            # ca biên review plan (n1): hỏi thông tin, có chữ "đặt"
    "Soạn tin hỏi phòng cho 3 người ở hai đêm",                 # ca biên review plan (n1): việc bằng chữ, hệ thống làm được
    "Tóm lịch lại để mình chép gửi vào nhóm Zalo",             # người gửi là người dùng
    "soạn giúp mình tin nhắn gửi qua zalo cho chủ nhà",            # nhờ soạn, không nhờ gửi
    "đặt phòng khách sạn ở Huế qua kênh nào thì rẻ",
    "chỉ giúp mình cách đặt vé Đại Nội online",
    "có nên đặt phòng trước giúp cả nhà không",
    "gửi hành lý ở đâu gần ga Huế",
    "mình muốn gửi bưu thiếp qua thư về Hà Nội thì ra bưu điện nào",
    "khách sạn nào còn phòng view sông",
    # review nhánh (19/11): có "đặt" + "giúp" / "bạn đặt" nhưng không nhờ đặt chỗ
    "mình đã đặt phòng ở Kim Long rồi, gợi ý giúp mình quán cà phê gần đó",
    "đặt vé xe khách đi Đà Nẵng giúp rẻ hơn đi tàu không",
    "bạn đặt lịch ngày 1 sao cho xe đỡ phải quay đầu nhé",
    "đặt giúp mình một câu hỏi về phòng trưng bày cổ vật",
    "bạn đặt phòng hộ ai bao giờ chưa",
    "gửi bưu thiếp qua thư về Sài Gòn mất mấy ngày",               # gửi đồ vật: việc của người dùng
    "nhắn giúp mình tên quán bún bò ngon",                         # nhờ trợ lý nói, không nhờ nhắn cho bên thứ ba
    # bản sửa cuối (thu hẹp): "giúp" đi với động từ khác, không kề đại từ / không ở cuối câu ⇒ câu hỏi thông tin
    "nhắn tin cho nhà nghỉ trước có giúp giữ phòng không",
    "gửi tin nhắn cho tổng đài có giúp tra được giờ xe không",
    "mình muốn nhắn chủ homestay trước, nên gửi qua zalo hay gọi điện thì hơn",
    "đặt cọc phòng khoảng bao nhiêu là vừa giúp mình với",
    # SÓT có chủ ý sau khi thu hẹp (nhờ thật nhưng không bắt — lượt đó chạy y như cờ tắt)
    "Gửi tin nhắn cho homestay báo giúp mình là 9 giờ tối mới đến",
    "Nhắn giúp mình cho nhà hàng là nhóm mình tới muộn 20 phút",
    "Chia đều thì mỗi người bao nhiêu, phòng tính chung",
    "Đại Nội mở cửa mấy giờ",
    "",
])
def test_information_questions_and_text_tasks_are_not_caught(cau):
    assert nho_lam_thay(cau) is None


# ---------- (2) chỗ thay, cổng web, tập câu từ chối ----------
def test_every_honest_sentence_counts_as_a_refusal_everywhere():
    """Khoá: câu nói thật ∈ tập câu từ chối của log (`REFUSAL_ANSWERS`) và của bộ đánh giá (`is_refusal`) — thiếu thì một câu ngoài kho bị thay
    nhầm sẽ bị đếm là "được trả lời"."""
    assert set(CAU_LAM_THAY) == {DAT_CHO, GUI, TINH_TRANG} and "lam_thay" in REMEMBERED_OUTCOMES
    for cau in CAU_LAM_THAY.values():
        assert cau in REFUSAL_ANSWERS and is_refusal(cau) and not CITATION_PATTERN.search(cau)   # không mã trích dẫn [n]
    assert "(#/cho-o)" in CAU_LAM_THAY[DAT_CHO] and "http" not in "".join(CAU_LAM_THAY.values())   # chỉ link NỘI BỘ tới trang Chỗ ở


def _trace(loai, text=INSUFFICIENT_ANSWER, **kw):
    return AnswerTrace(route=ROUTE_TRO_LY_HUE, lam_thay=loai, generated=SimpleNamespace(text=text), **kw)


WEB_BAT = AssistantFlags(router=True, tim_them=True, tra_web=True, noi_that_lam_thay=True)


def test_boilerplate_refusal_is_replaced_and_web_gate_stays_closed():
    trace = _trace(GUI)
    _finish_generated(trace, WEB_BAT)
    assert trace.answer == CAU_LAM_THAY[GUI] and trace.fixed_outcome == "lam_thay" and trace.cited == () and trace.citation_error is None
    assert not web_gate_open(trace, WEB_BAT, object())
    assert trace.tools == [{"name": "lam_thay", "ms": 0.0, "loai": GUI}]   # log chỉ có mã loại


def test_nothing_changes_when_the_turn_is_not_a_request_to_act():
    """Lượt hàm không bắt (và mọi lượt khi cờ tắt: `trace.lam_thay` luôn None) ⇒ câu từ chối khuôn giữ nguyên, cổng web mở như cũ."""
    trace = _trace(None)
    _finish_generated(trace, WEB_BAT)
    assert trace.answer == INSUFFICIENT_ANSWER and trace.fixed_outcome is None and web_gate_open(trace, WEB_BAT, object())


@pytest.mark.parametrize("kw", [
    {"text": "Bạn có thể đặt qua tổng đài của khách sạn [1]."},     # kho CÓ đáp án ⇒ không bao giờ thay
    {"lich": {"khung": {}}},                                       # lượt có lịch
    {"thoi_tiet": {"khoi": "x"}},                                  # lượt có dự báo
    {"thoi_tiet_ctx": {"bao_lu_cau": True}},                       # câu khớp lưới bão / lũ: các lớp an toàn giữ nguyên
    {"thoi_tiet_ctx": {"bao_lu": True}},
    {"thoi_tiet_ctx": {"luoi_cuoi": True}},                        # "dông": chỉ lưới cuối bắt (soát khác hãng 20/11) ⇒ cũng không thay
])
def test_guard_conditions_leave_the_answer_alone(kw):
    text = kw.pop("text", INSUFFICIENT_ANSWER)
    trace = _trace(DAT_CHO, text, **kw)
    assert _noi_that_lam_thay(trace, text) is False and trace.fixed_outcome is None and trace.tools == []


@pytest.mark.parametrize("cau, ket_thuc", [
    (CAU_DAT, "lam_thay"),
    ("bão sắp vào Huế, " + CAU_DAT, "refusal_no_sources"),   # câu khớp lưới bão / lũ: giữ câu từ chối cũ + các lớp an toàn của lượt bão
])
def test_empty_context_refusal_is_replaced_except_on_storm_turns(monkeypatch, cau, ket_thuc):
    """Nơi thay thứ nhất (ngữ cảnh rỗng ⇒ câu từ chối do code đặt, trước khi gọi model). Ở bước này `thoi_tiet_ctx` chưa có ⇒ lưới bão / lũ
    phải xét thẳng trên câu người dùng (review nhánh m1). Bộ tìm được thay bằng hàm giả trả ngữ cảnh rỗng — chỉ khoá nhánh điều kiện."""
    from llm import assistant

    async def rong(query, retrieval_service, context_builder, generator, trace, recorder, today, instructions):
        trace.packed = SimpleNamespace(text="", sources=())
        trace.answer, trace.fixed_outcome = INSUFFICIENT_ANSWER, "refusal_no_sources"
    monkeypatch.setattr(assistant, "prepare_answer", rong)
    flags = AssistantFlags(router=True, tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True, noi_that_lam_thay=True, du_bao=lambda *a, **k: None)
    trace = AnswerTrace(route=ROUTE_TRO_LY_HUE)
    asyncio.run(assistant._before_model(cau, None, None, None, trace, None, None, flags))
    assert trace.lam_thay == DAT_CHO and trace.fixed_outcome == ket_thuc
    assert trace.answer == (CAU_LAM_THAY[DAT_CHO] if ket_thuc == "lam_thay" else INSUFFICIENT_ANSWER)


@pytest.mark.parametrize("tu, thay", [("dông", False), ("giông", False), ("nắng", True)])
def test_model_refusal_is_not_replaced_when_the_final_storm_net_matches(tu, thay):
    """Nơi thay thứ hai (model tự trả câu từ chối): ngữ cảnh thời tiết do ĐÚNG hàm của lượt dựng (`_lich_extra`). "dông" và "giông" phải chạy như
    nhau — trước bản sửa, "dông" (chỉ lưới cuối bắt) vẫn bị thay bằng câu nói thật và đóng cổng tra web; "nắng" là ca đối chứng: vẫn được thay."""
    from llm import assistant
    flags = AssistantFlags(router=True, tim_them=True, thoi_tiet=True, bao_lu_cong_cu=True, noi_that_lam_thay=True, du_bao=lambda *a, **k: None)
    trace = _trace(DAT_CHO)
    assistant._lich_extra(f"Chiều nay trời {tu}, " + CAU_DAT, None, None, trace, None, None, flags)
    _finish_generated(trace, flags)
    assert (trace.fixed_outcome == "lam_thay") is thay and (trace.answer == CAU_LAM_THAY[DAT_CHO]) is thay


def test_done_event_has_no_ask_tips_for_honest_limit_turn():
    """Giao diện hiện khối "gợi ý cách hỏi" khi `done` có `tu_choi_kho`; lượt nói thật giới hạn đã tự chỉ cách làm ⇒ không có khối đó, nhưng log
    vẫn ghi `refusal`."""
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    trace = AnswerTrace(answer=CAU_LAM_THAY[DAT_CHO], cited=(), fixed_outcome="lam_thay")
    events = parse_sse([stream.delta(trace.answer), *stream.fixed(trace)])
    assert events == [("delta", {"seq": 1, "text": CAU_LAM_THAY[DAT_CHO]}), ("sources", []), ("done", {"outcome": "lam_thay"})]
    assert metrics["refusal"] is True and metrics["delta_matches_final"] is True


# ---------- (3) lõi thật, model giả, bộ tìm thật ----------
@pytest.fixture(scope="module")
def deps():
    from core.settings_loader import load_settings
    from evaluation.full_corpus_eval import build_context_builder, build_retrieval
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    yield service, build_context_builder(settings)
    service.close()


def _script(tra_loi, goi=None):
    """Định tuyến ⇒ tro_ly_hue; trợ lý ⇒ `tra_loi`. `goi` ghi kwargs mọi lần gọi model."""
    from test_b2_tool_loop import answer

    def script(n, kw):
        if goi is not None:
            goi.append(kw)
        ins = kw.get("instructions") or ""
        if "tro_ly_hue" in ins and "ngoai_pham_vi" in ins:
            return [{"type": "message", "id": f"r{n}", "role": "assistant", "status": "completed",
                     "content": [{"type": "output_text", "text": json.dumps({"route": "tro_ly_hue"}), "annotations": []}]}]
        return [answer(tra_loi)]
    return script


def _chay_stream(deps, flags, cau, tra_loi, parallel, goi=None):
    from test_b2_tool_loop import generator
    from test_b6_tra_web import _events, serper
    web = []
    trace = AnswerTrace()
    path = answer_turn_stream_parallel if parallel else answer_turn_stream
    events = _events(path, cau, *deps, generator(_script(tra_loi, goi)), trace, dataclasses.replace(flags, song_song_tra_loi=parallel), None,
                     serper(calls=web))
    return trace, events, web


@pytest.mark.parametrize("parallel", [False, True])
@pytest.mark.parametrize("tra_loi", [INSUFFICIENT_ANSWER, INSUFFICIENT_ANSWER + "\n"])   # khoảng trắng cuối: vẫn không lọt câu khuôn ra màn hình
def test_stream_shows_only_the_honest_sentence_and_never_calls_web(deps, parallel, tra_loi):
    trace, events, web = _chay_stream(deps, WEB_BAT, CAU_DAT, tra_loi, parallel)
    assert [d for k, d in events if k == "delta"] == [CAU_LAM_THAY[DAT_CHO]]          # không mảnh nào của câu khuôn
    assert trace.answer == CAU_LAM_THAY[DAT_CHO] and trace.fixed_outcome == "lam_thay" and trace.lam_thay == DAT_CHO
    assert trace.web is None and web == [] and ("status", {"stage": "tra_web"}) not in events


@pytest.mark.parametrize("parallel", [False, True])
def test_stream_real_answer_to_a_request_passes_through_unchanged(deps, parallel):
    """Hàm bắt câu nhưng model trả lời được từ kho ⇒ chữ model ra nguyên (giữ chữ chỉ chừng nào còn là khúc đầu câu khuôn)."""
    tra_loi = "Tôi gợi ý bạn liên hệ trực tiếp cơ sở lưu trú [1]."     # mở đầu trùng chữ "Tôi" của câu khuôn
    trace, events, _ = _chay_stream(deps, WEB_BAT, CAU_DAT, tra_loi, parallel)
    assert "".join(d for k, d in events if k == "delta") == tra_loi and trace.fixed_outcome is None and trace.answer == tra_loi


def test_non_stream_path_replaces_too(deps):
    from test_b2_tool_loop import generator
    from test_b6_tra_web import serper
    web = []
    trace = AnswerTrace()
    asyncio.run(answer_turn("gửi lịch qua email cho mình với", *deps, generator(_script(INSUFFICIENT_ANSWER)), trace, WEB_BAT, None,
                            serper(calls=web)))
    assert trace.answer == CAU_LAM_THAY[GUI] and trace.fixed_outcome == "lam_thay" and trace.web is None and web == []


@pytest.mark.parametrize("parallel", [False, True])
def test_flag_changes_no_byte_sent_to_the_model_and_off_keeps_old_behaviour(deps, parallel):
    """Cờ bật ↔ tắt trên CÙNG một câu nhờ làm thay: mọi yêu cầu gửi model (định tuyến, trợ lý) giống nhau; cờ tắt ⇒ câu khuôn + mục web như cũ."""
    goi_bat, goi_tat = [], []
    _chay_stream(deps, WEB_BAT, CAU_DAT, INSUFFICIENT_ANSWER, parallel, goi_bat)
    trace, events, web = _chay_stream(deps, dataclasses.replace(WEB_BAT, noi_that_lam_thay=False), CAU_DAT, INSUFFICIENT_ANSWER, parallel, goi_tat)
    assert trace.answer == INSUFFICIENT_ANSWER and trace.fixed_outcome is None and trace.lam_thay is None and len(web) == 1

    def khoa(ds):
        return sorted(json.dumps({k: v for k, v in kw.items() if k in ("instructions", "input", "tools", "model")}, ensure_ascii=False,
                                 sort_keys=True, default=str) for kw in ds)
    tro_ly_tat = [k for k in khoa(goi_tat) if "Phòng tập" not in k]
    assert khoa(goi_bat) == tro_ly_tat[:len(goi_bat)] and len(goi_tat) == len(goi_bat) + 1   # bên tắt chỉ thừa đúng lần gọi viết mục web
