"""Logic thuần của route stream (spec streaming §7 "Logic thuần phía server") — chữ / mảnh có sẵn, không gọi model, không stub model.

Bảo vệ: (1) bóc chữ từ JSON `{"answer": "…"}` đang stream đúng cả khi mảnh cắt giữa thoát JSON; (2) `[Nguồn n]` chỉ chuẩn hóa khi `]`
đã tới, chữ đã gửi không bao giờ phải sửa, ghép lại = chữ cuối đã chuẩn hóa (C5); (3) thứ tự `status … delta … sources | error … done`,
`seq` tăng; (4) định dạng SSE. Đây không phải bằng chứng cho provider / mạng (đường thật ở report S2).
"""
import asyncio
import json
import random
import time

from api.routes.chat import STREAM_METRIC_FIELDS, StreamEvents, _answer_events, sse_event
from core.schema import GenerationError
from llm.answer_stream import AnswerTextStream, decode_partial_string, displayable_prefix
from llm.citations import normalize_citations
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER
from llm.assistant import AnswerTrace, check_citations
from retrieval.full_corpus_context import PackedContext, PackedSource


def feed_all(pieces: list[str]) -> tuple[list[str], AnswerTextStream]:
    extractor = AnswerTextStream()
    return [extractor.feed(piece) for piece in pieces], extractor


def parse_sse(chunks: list[bytes]) -> list[tuple[str, object]]:
    events = []
    for chunk in chunks:
        text = chunk.decode("utf-8")
        assert text.endswith("\n\n")
        lines = text.strip("\n").split("\n")
        name = next(line[len("event: "):] for line in lines if line.startswith("event: "))
        data = "\n".join(line[len("data: "):] for line in lines if line.startswith("data: "))
        events.append((name, json.loads(data)))
    return events


# ---------- Bóc chữ JSON từng phần ----------

def test_no_text_until_json_prefix_is_complete():
    outputs, extractor = feed_all(['{"', 'answer', '":"', "Vé", " vào"])
    assert outputs == ["", "", "", "Vé", " vào"]
    assert extractor.shown == "Vé vào"


def test_unicode_escape_cut_between_pieces_is_decoded_once_complete():
    escaped = INSUFFICIENT_ANSWER.encode("ascii", "backslashreplace").decode().replace("\\x", "\\u00")
    cut = escaped.index("\\u") + 3  # cắt giữa "\uXXXX"
    outputs, extractor = feed_all(['{"answer":"' + escaped[:cut], escaped[cut:], '"}'])
    assert "\\" not in "".join(outputs)
    assert "".join(outputs) == INSUFFICIENT_ANSWER


def test_escaped_quote_and_newline_split_across_pieces():
    outputs, _ = feed_all(['{"answer":"Tên \\', '"Huế\\', '" mở cửa\\', 'n- Ý', '"}'])
    assert "".join(outputs) == 'Tên "Huế" mở cửa\n- Ý'


def test_emoji_escaped_as_surrogate_pair_cut_between_halves_is_held_then_sent_whole():
    # Review S2 m-1 (A 01/11): provider thoát ASCII ⇒ "😀" = "\\ud83d\\ude00"; mảnh cắt giữa hai nửa không được phát nửa đầu đứng lẻ
    # (sse_event sẽ ném UnicodeEncodeError ⇒ luồng lỗi).
    raw = json.dumps({"answer": "BMP 😀 rồi [1]."})
    cut = raw.index("\\ude")
    outputs, _ = feed_all([raw[:cut], raw[cut:]])
    assert outputs[0] == "BMP " and "".join(outputs) == "BMP 😀 rồi [1]."
    for text in outputs:
        sse_event("delta", {"seq": 1, "text": text})  # mã hóa UTF-8 được


def test_decode_partial_string_reports_closed_string():
    assert decode_partial_string('Ch\\u00f9a"}') == ("Chùa", True)
    assert decode_partial_string("Ch\\u00f") == ("Ch", False)


def test_nguon_citation_is_held_until_closing_bracket_then_normalized():
    outputs, _ = feed_all(['{"answer":"Mở 7 giờ [Ngu', 'ồn 2', "] và", ' [1].', '"}'])
    assert outputs == ["Mở 7 giờ ", "", "[2] và", " [1].", ""]


def test_bracket_that_cannot_become_citation_is_shown_immediately():
    assert displayable_prefix("Giá [Ngày lễ", closed=False) == "Giá [Ngày lễ"
    assert displayable_prefix("Giá [x", closed=False) == "Giá [x"
    assert displayable_prefix("Giá [ 12 ", closed=False) == "Giá "
    assert displayable_prefix("Giá [nguồn", closed=False) == "Giá "
    assert displayable_prefix("Giá [1", closed=True) == "Giá [1"  # chuỗi đã đóng ⇒ hiện hết


def test_random_cuts_always_join_to_normalized_final_answer():
    answer = 'Chùa "Thiên Mụ" mở cửa 7:00 [Nguồn 1], vé 1.000 đồng [ nguồn 12 ].\nXem thêm [3] và [Ngày hội].'
    raw = json.dumps({"answer": answer})  # ensure_ascii mặc định ⇒ có \uXXXX như provider có thể gửi
    rng = random.Random(20261101)
    for _ in range(300):
        cuts = sorted(rng.sample(range(1, len(raw)), rng.randint(1, 25)))
        pieces = [raw[a:b] for a, b in zip([0, *cuts], [*cuts, len(raw)])]
        outputs, _ = feed_all(pieces)
        assert "".join(outputs) == normalize_citations(answer)


# ---------- Chuỗi sự kiện ----------

def packed_two_sources() -> PackedContext:
    sources = tuple(PackedSource(id=i, title=f"Nguồn thử {i}", heading_path=("Mục",), excerpts=(f"đoạn {i}",)) for i in (1, 2))
    return PackedContext(text="", sources=sources, input_tokens=0)


def stream_with_text(answer: str) -> tuple[StreamEvents, list[bytes], AnswerTrace]:
    """Đi như `_answer_events`: status ⇒ các delta bóc từ JSON ⇒ kiểm citation chữ cuối ⇒ sự kiện kết."""
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    packed = packed_two_sources()
    trace = AnswerTrace(packed=packed, so_nguon=list(packed.sources), answer=answer)  # như `tim_kho` ghi sổ nguồn
    chunks = [stream.status({"stage": "searched", "n_sources": 2}), stream.status({"stage": "generating"})]
    extractor = AnswerTextStream()
    raw = json.dumps({"answer": answer}, ensure_ascii=False)
    for start in range(0, len(raw), 7):
        text = extractor.feed(raw[start:start + 7])
        if text:
            chunks.append(stream.delta(text))
    check_citations(trace)
    chunks += stream.finish(trace)
    return stream, chunks, trace


def test_success_order_seq_and_only_cited_sources():
    stream, chunks, _ = stream_with_text("Mở cửa từ 7 giờ [Nguồn 2].")
    events = parse_sse(chunks)
    names = [name for name, _ in events]
    assert names[:2] == ["status", "status"] and names[-2:] == ["sources", "done"]
    assert set(names[2:-2]) == {"delta"}
    seqs = [data["seq"] for name, data in events if name == "delta"]
    assert seqs == list(range(1, len(seqs) + 1))
    assert "".join(data["text"] for name, data in events if name == "delta") == "Mở cửa từ 7 giờ [2]."
    assert [source["id"] for source in events[-2][1]] == [2]
    assert events[-1][1] == {"outcome": "success"}
    assert stream.metrics["delta_matches_final"] is True and stream.metrics["refusal"] is False
    assert isinstance(stream.metrics["first_event_ms"], float) and isinstance(stream.metrics["first_text_ms"], float)


def test_final_answer_without_citation_is_retracted_without_sources():
    stream, chunks, trace = stream_with_text("Mở cửa từ 7 giờ.")
    events = parse_sse(chunks)
    assert trace.citation_error is not None
    assert [name for name, _ in events][-2:] == ["error", "done"]
    assert "sources" not in [name for name, _ in events]
    assert events[-2][1]["code"] == "citation_integrity_error" and events[-2][1]["after_text"] is True
    assert stream.metrics["outcome"] == "retracted"


def test_unknown_citation_number_is_retracted():
    _, chunks, _ = stream_with_text("Mở cửa từ 7 giờ [9].")
    assert parse_sse(chunks)[-2][1]["code"] == "citation_integrity_error"


def test_model_refusal_streams_with_empty_sources():
    stream, chunks, _ = stream_with_text(INSUFFICIENT_ANSWER)
    events = parse_sse(chunks)
    assert events[-2] == ("sources", []) and stream.metrics["refusal"] is True and stream.metrics["outcome"] == "success"


def test_refusal_without_model_still_goes_through_stream():
    """B1: lõi phát chữ từ chối thành một `delta`; route kết bằng `sources` rỗng + `done` mang outcome của câu cố định."""
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    trace = AnswerTrace(answer=INSUFFICIENT_ANSWER, cited=(), fixed_outcome="refusal_no_sources")
    events = parse_sse([stream.delta(trace.answer), *stream.fixed(trace)])
    assert events == [("delta", {"seq": 1, "text": INSUFFICIENT_ANSWER}), ("sources", []), ("done", {"outcome": "refusal_no_sources"})]
    assert metrics["refusal"] is True and metrics["delta_matches_final"] is True


def test_retrieval_error_inside_stream_keeps_old_503_message():
    """B1 D6 (đổi cố ý): lỗi Qdrant giữa luồng ⇒ sự kiện `error` mang đúng mã + câu của JSON 503 trước B1 (review C129 m-3)."""
    from core.schema import RetrievalDependencyError

    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    events = parse_sse(StreamEvents(metrics, time.perf_counter()).failure(RetrievalDependencyError("x")))
    assert events[0] == ("error", {"code": "retrieval_unavailable", "message": "Hệ thống tra cứu tạm thời không khả dụng.", "after_text": False})
    assert events[1][0] == "done" and metrics["outcome"] == "retrieval_unavailable"


def test_notice_event_follows_sources_when_set():
    stream, chunks, trace = stream_with_text("Mở cửa từ 7 giờ [1].")
    assert "notice" not in [name for name, _ in parse_sse(chunks)]  # không đặt notice ⇒ không có sự kiện
    trace.notice = "dòng thử"
    names = [name for name, _ in parse_sse(StreamEvents(dict.fromkeys(STREAM_METRIC_FIELDS), time.perf_counter()).finish(trace))]
    assert names == ["sources", "notice", "done"]


def test_any_error_after_stream_opened_ends_with_error_then_done():
    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    before = parse_sse(stream.failure(GenerationError("x")))
    assert [name for name, _ in before] == ["error", "done"]
    assert before[0][1]["code"] == "generation_unavailable" and before[0][1]["after_text"] is False
    assert metrics["outcome"] == "generation_failed"

    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    stream = StreamEvents(metrics, time.perf_counter())
    stream.delta("Mở cửa")
    after = parse_sse(stream.failure(TimeoutError()))
    assert after[0][1]["after_text"] is True and metrics["outcome"] == "stream_error_after_text"

    metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
    unexpected = parse_sse(StreamEvents(metrics, time.perf_counter()).failure(KeyError("x")))
    assert unexpected[0][1]["code"] == "internal_error" and metrics["outcome"] == "internal_error"


def test_disconnect_while_route_sends_text_still_logs_calls_the_core_records_on_close():
    """C132 m-1: người dùng ngắt đúng lúc route đang ở `yield` (gửi mảnh chữ) ⇒ route phải đóng lõi trước khi chép số đo vào dòng log,
    vì lõi chỉ ghi `llm_calls` ở `finally` của nó. Lõi ở đây là generator chữ có sẵn (không model)."""
    async def core(trace: AnswerTrace):
        try:
            yield "delta", "Mở cửa"
            yield "delta", " từ 7 giờ"
        finally:
            trace.llm_calls.append({"route": "tro_ly_hue", "usd": 0.0001})  # như `record_llm_calls` ở `finally` của lõi

    async def run() -> dict:
        metrics = dict.fromkeys(STREAM_METRIC_FIELDS)
        trace = AnswerTrace()
        events = _answer_events(core(trace), trace, metrics, time.perf_counter())
        await anext(events)  # route đứng ở `yield` của mảnh chữ đầu
        await events.aclose()  # Starlette đóng generator khi người dùng ngắt ⇒ GeneratorExit tại `yield`
        return metrics

    metrics = asyncio.run(run())
    assert metrics["outcome"] == "client_disconnected"
    assert metrics["n_llm_calls"] == 1 and metrics["usd"] == 0.0001


def test_sse_format_keeps_vietnamese_and_puts_multiline_text_on_one_data_line():
    chunk = sse_event("delta", {"seq": 1, "text": "Huế\nđẹp"})
    assert chunk == 'event: delta\ndata: {"seq": 1, "text": "Huế\\nđẹp"}\n\n'.encode("utf-8")
