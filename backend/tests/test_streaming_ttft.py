"""Mốc thời gian của harness C70 (`experiments/streaming/ttft.py`) — logic thuần, sự kiện tự dựng nhỏ.

Bảo vệ định nghĩa đo ghi trước ở plan §3: chữ đầu tiên chỉ tính sau tiền tố JSON `{"answer":"`; "câu đầu có citation" cần citation đóng rồi
dấu kết câu; số `1.000` không phải kết câu. Đây không phải bằng chứng cho provider (pilot thật kiểm loại sự kiện).
"""
from experiments.streaming.ttft import timeline
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER


def delta(ms: float, text: str) -> dict:
    return {"ms": ms, "type": "response.output_text.delta", "delta": text}


def test_first_visible_waits_for_json_prefix_and_reasoning_done_is_recorded():
    events = [
        {"ms": 100.0, "type": "response.created"},
        {"ms": 900.0, "type": "response.output_item.done", "item_type": "reasoning"},
        delta(1000.0, '{"'),
        delta(1010.0, 'answer":"'),
        delta(1020.0, "Vé"),
        {"ms": 1500.0, "type": "response.completed"},
    ]
    marks = timeline(events)
    assert marks["t_first_event"] == 100.0
    assert marks["t_reasoning_done"] == 900.0
    assert marks["t_first_delta"] == 1000.0
    assert marks["t_first_visible"] == 1020.0  # tiền tố JSON xong ở 1010 nhưng chưa có chữ nào
    assert marks["t_last_event"] == 1500.0
    assert marks["t_first_cited_sentence"] is None


def test_cited_sentence_needs_closed_citation_then_sentence_end_and_skips_thousands_separator():
    events = [
        delta(1.0, '{"answer":"Giá 1.000 đồng [1'),
        delta(2.0, "]"),          # citation đóng nhưng chưa kết câu
        delta(3.0, " vé 1.5"),    # "1.5": sau dấu chấm là chữ số ⇒ không phải kết câu
        delta(4.0, "00. Tiếp"),   # dấu chấm + khoảng trắng ⇒ kết câu
    ]
    assert timeline(events)["t_first_cited_sentence"] == 4.0


def test_cited_sentence_accepts_nguon_form_and_end_of_json_string():
    events = [delta(1.0, '{"answer":"Mở cửa từ 7 giờ [Nguồn 2]'), delta(2.0, '"}')]
    assert timeline(events)["t_first_cited_sentence"] == 2.0


def test_refusal_complete_only_when_whole_standard_refusal_arrived():
    half = len(INSUFFICIENT_ANSWER) // 2
    events = [delta(1.0, '{"answer":"' + INSUFFICIENT_ANSWER[:half]), delta(2.0, INSUFFICIENT_ANSWER[half:]), delta(3.0, '"}')]
    marks = timeline(events)
    assert marks["t_first_visible"] == 1.0
    assert marks["t_refusal_complete"] == 2.0
    assert marks["t_first_cited_sentence"] is None


def test_no_events_gives_no_marks():
    assert set(timeline([]).values()) == {None}
