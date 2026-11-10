"""B142: đánh giá 👍 / 👎 — mã lượt do server cấp (không liên quan mã cuộc), `POST /api/feedback` kiểm đầu vào, log chỉ số đếm.
Generator thay thế (không mạng) cho phần sinh; tìm kho thật như các test API khác (logic route, không phải bằng chứng model)."""
import json
import time

from fastapi.testclient import TestClient

from api.app import create_app
from api.feedback import FEEDBACK_FIELDS, FeedbackTurns
from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents
from llm.assistant import AnswerTrace
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from test_api_chat import chat_log_records, metric_lines
from test_b3_memory import MemoryGenerator
from test_chat_stream import parse_sse, stream_with_text

QUESTION = "Đại Nội mở cửa mấy giờ?"


def feedback_lines(records) -> list[dict]:
    return [json.loads(r.getMessage().removeprefix("chat_feedback ")) for r in records
            if r.name == "chat" and r.getMessage().startswith("chat_feedback ")]


def test_chat_turn_id_feedback_logs_counts_only(caplog):
    app = create_app()
    with TestClient(app) as client:
        original = app.state.generator, app.state.generator_ready
        app.state.generator, app.state.generator_ready = MemoryGenerator(), True
        with chat_log_records(caplog) as records:
            answer = client.post("/api/chat", json={"query": QUESTION})
            turn_id = answer.json()["turn_id"]
            up = client.post("/api/feedback", json={"turn_id": turn_id, "rating": "up"})
            down = client.post("/api/feedback", json={"turn_id": turn_id, "rating": "down"})  # đổi ý ⇒ thêm một dòng
        app.state.generator, app.state.generator_ready = original
    assert answer.status_code == 200 and len(turn_id) == 16
    assert up.status_code == 200 and down.status_code == 200
    lines = feedback_lines(records)
    assert [line["rating"] for line in lines] == ["up", "down"]
    assert all(tuple(line) == FEEDBACK_FIELDS for line in lines)
    assert lines[0] == {"turn_id": turn_id, "route": "tro_ly_hue", "outcome": "success", "n_cited_sources": 1, "rating": "up"}
    assert metric_lines(records)[0]["turn_id"] == turn_id  # việc nhỏ 13: nối 👍 / 👎 với số đo của đúng lượt
    logged = "\n".join(r.getMessage() for r in records)
    assert QUESTION not in logged and "Mở cửa từ 7 giờ" not in logged and "conversation_id" not in logged


def test_feedback_rejects_bad_input_and_unknown_turn():
    app = create_app()
    client = TestClient(app)  # không cần lifespan: kho mã lượt dựng trong create_app
    known = app.state.feedback_turns.add("tro_ly_hue", "success", 2)
    for body in ({"turn_id": known, "rating": "meh"}, {"turn_id": known}, {"turn_id": known, "rating": "up", "text": "câu"},
                 {"turn_id": "ngắn", "rating": "up"}, {"turn_id": "../" + known[3:], "rating": "up"}):
        assert client.post("/api/feedback", json=body).status_code == 422, body
    unknown = client.post("/api/feedback", json={"turn_id": "A" * 16, "rating": "up"})
    assert unknown.status_code == 404 and unknown.json()["error"]["code"] == "unknown_turn"
    assert client.post("/api/feedback", json={"turn_id": known, "rating": "down"}).status_code == 200


def test_turn_id_is_random_not_conversation_cookie():
    turns = FeedbackTurns(max_turns=3)
    ids = [turns.add("tro_ly_hue", "success", 1) for _ in range(5)]
    assert len(set(ids)) == 5 and turns.get(ids[0]) is None and turns.get(ids[-1])["outcome"] == "success"  # trần RAM bỏ lượt cũ nhất


def test_stream_done_has_turn_id_only_for_answered_turns():
    """Có hàm cấp mã ⇒ `done` của lượt trả lời / câu cố định mang `turn_id`; lượt lỗi hoặc bị rút lại thì không. Không truyền ⇒ `done` như cũ."""
    calls = []
    new_id = lambda: calls.append(1) or "B" * 16  # noqa: E731

    stream, chunks, trace = stream_with_text("Mở cửa từ 7 giờ [1].")
    stream.new_turn_id = new_id
    done = parse_sse(stream.finish(trace))[-1]
    assert done == ("done", {"outcome": "success", "turn_id": "B" * 16}) and stream.metrics["turn_id"] == "B" * 16

    stream, chunks, trace = stream_with_text("Mở cửa từ 7 giờ [9].")  # mã trích dẫn ngoài sổ ⇒ rút lại
    stream.new_turn_id = new_id
    assert parse_sse(stream.finish(trace))[-1] == ("done", {"outcome": "retracted"})

    fixed = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter(), new_id)
    events = parse_sse(fixed.fixed(AnswerTrace(answer=INSUFFICIENT_ANSWER, cited=(), fixed_outcome="refusal_no_sources")))
    assert events[-1] == ("done", {"outcome": "refusal_no_sources", "tu_choi_kho": True, "turn_id": "B" * 16})

    failed = StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter(), new_id)
    assert "turn_id" not in parse_sse(failed.failure(TimeoutError()))[-1][1] and failed.metrics["turn_id"] is None
    assert len(calls) == 2
