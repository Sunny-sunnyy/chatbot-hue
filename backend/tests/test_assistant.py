"""Lõi chung `llm.assistant` qua `answer_case` của bộ đánh giá — đường thật (Qdrant chỉ đọc, e5 + tokenizer local), không gọi model.

Bảo vệ spec streaming §4.8 khác biệt 3: lỗi kỹ thuật của một case thành `row["error"]` (lượt chấm incomplete), không ném ra
ngoài; các bước đã chạy trước lỗi vẫn ghi vào dòng như trước khi gom lõi chung.
"""
import asyncio

from core.settings_loader import load_settings
from evaluation.full_corpus_eval import RETRIEVAL_K, answer_case, build_context_builder, build_retrieval


def test_answer_case_turns_context_budget_error_into_row_error():
    settings = load_settings(validate_private_paths=False)
    settings["full_corpus_generation"] = dict(settings["full_corpus_generation"])
    settings["full_corpus_generation"]["context_limit"] = 2561  # cùng ngưỡng ép lỗi ngân sách như test_api_chat.py
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    try:
        case = {"case_index": 0, "category": "test", "question": "  Giá vé Đại Nội?  "}
        # generator=None: lỗi ngân sách xảy ra trước bước sinh nên model không bao giờ được gọi
        row = asyncio.run(answer_case(case, service, build_context_builder(settings), None))
    finally:
        service.close()
    assert row["error"].startswith("ContextBudgetError")
    assert len(row["top_chunk_ids"]) == RETRIEVAL_K  # bước tìm đã chạy ⇒ vẫn ghi
    assert row["context_sources"] is None and row["answer"] is None and row["refusal"] is None
    assert row["input_tokens"] is None and row["response_id"] is None


# ---------- Phase 9 B1: rẽ tuyến (plan D1, D3–D5, D8; m-1) — generator thay thế ghi lại lần gọi, KHÔNG phải bằng chứng hành vi model ----------

from types import SimpleNamespace

import pytest

from core.schema import GenerationError
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER
from llm.generator_openai_full_corpus import RouteOutput

ALL_ON = AssistantFlags(router=True, today_line=True, may_have_changed_notice=True)
CALL = {"kind": ["message"], "ms": 1.0, "usd": 0.00001, "input_tokens": 10, "output_tokens": 2, "reasoning_tokens": 0,
        "cached_tokens": 0, "cache_write_tokens": 0}


class FakeGenerator:
    """Ghi mỗi lần gọi; định tuyến trả `route` cho trước (hoặc lỗi); mỗi lần gọi ghi một mục vào `call_log` như `CallLog` thật."""

    def __init__(self, route="tro_ly_hue", route_fails=False, answer_fails=False, answer="Có thông tin [1]."):
        self.route_value, self.route_fails, self.answer_fails, self.answer = route, route_fails, answer_fails, answer
        self.calls = []

    async def route(self, query, call_log):
        self.calls.append("route")
        call_log.calls.append(dict(CALL))
        if self.route_fails:
            raise GenerationError("x")
        return self.route_value

    async def generate_chat(self, query, call_log):
        self.calls.append("chat")
        call_log.calls.append(dict(CALL))
        return SimpleNamespace(text="Chào bạn!")

    async def generate_answer(self, query, context, call_log=None, today=None):
        self.calls.append(("answer", today is not None))
        call_log.calls.append(dict(CALL))  # model đã trả lời…
        if self.answer_fails:
            raise GenerationError("JSON hỏng")  # …rồi lượt mới lỗi (review C128 m-1)
        return SimpleNamespace(text=self.answer)


@pytest.fixture(scope="module")
def deps():
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    yield service, build_context_builder(settings)
    service.close()


def run(deps, query, generator, flags=ALL_ON):
    trace = AnswerTrace()
    asyncio.run(answer_turn(query, *deps, generator, trace, flags))
    return trace


def test_router_has_only_two_groups():
    # bậc G (spec bản 13 §12.5): bỏ tuyến khẩn cấp + ngoài phạm vi — nhãn cũ bị schema từ chối (lõi đổi thành `tro_ly_hue` như lỗi định tuyến)
    assert RouteOutput.model_validate({"route": "tro_chuyen"}).route == "tro_chuyen"
    for old in ("khan_cap", "ngoai_pham_vi"):
        with pytest.raises(ValueError):
            RouteOutput.model_validate({"route": old})


def test_emergency_text_goes_to_kho_agent(deps):
    # không còn câu soạn sẵn: câu khẩn cấp đi định tuyến rồi agent Huế như câu thường (User 08/11)
    gen = FakeGenerator()
    trace = run(deps, "Có người vừa bị đuối nước ở bãi biển Thuận An", gen)
    assert gen.calls == ["route", ("answer", True)] and trace.fixed_outcome is None and trace.answer == "Có thông tin [1]."


@pytest.mark.parametrize("text", [OUT_OF_SCOPE_ANSWER, f"  {OUT_OF_SCOPE_ANSWER}\n"])
def test_agent_out_of_scope_answer_gets_out_of_scope_outcome(deps, text):
    # review B M-1: code nhận đúng câu ⇒ outcome `out_of_scope` như câu cố định cũ (không kiểm citation, giao diện / log / gợi ý như trước)
    trace = run(deps, "Viết giúp mình một hàm sắp xếp mảng", FakeGenerator(answer=text))
    assert trace.fixed_outcome == "out_of_scope" and trace.answer == OUT_OF_SCOPE_ANSWER and trace.cited == () and trace.citation_error is None


def test_other_text_is_not_out_of_scope(deps):
    # câu từ chối kho / câu có thêm chữ ⇒ không phải `out_of_scope` (không so lỏng)
    for text in (INSUFFICIENT_ANSWER, OUT_OF_SCOPE_ANSWER + " Ví dụ về Đại Nội [1]."):
        assert run(deps, "Đại Nội mở cửa mấy giờ?", FakeGenerator(answer=text)).fixed_outcome != "out_of_scope"


def test_chat_route_does_not_search(deps):
    gen = FakeGenerator(route="tro_chuyen")
    trace = run(deps, "Chào bạn", gen)
    assert gen.calls == ["route", "chat"] and trace.documents is None and trace.cited == () and trace.answer == "Chào bạn!"
    assert [c["route"] for c in trace.llm_calls] == ["router", "tro_chuyen"]


def test_router_error_falls_back_to_kho_path_with_date(deps):
    gen = FakeGenerator(route_fails=True)
    trace = run(deps, "Giá vé Đại Nội?", gen)
    assert trace.route == "tro_ly_hue" and trace.route_error == "router_failed" and gen.calls == ["route", ("answer", True)]
    assert trace.today.startswith("Hôm nay: ")


def test_flags_off_is_the_b0_path(deps):
    gen = FakeGenerator()
    trace = run(deps, "Giá vé Đại Nội?", gen, AssistantFlags())
    assert gen.calls == [("answer", False)] and trace.today is None and trace.notice is None
    assert [c["route"] for c in trace.llm_calls] == ["tro_ly_hue"]


def test_calls_already_made_are_logged_when_answer_fails(deps):
    gen = FakeGenerator(answer_fails=True)
    trace = AnswerTrace()
    with pytest.raises(GenerationError):
        asyncio.run(answer_turn("Giá vé Đại Nội?", *deps, gen, trace, ALL_ON))
    assert [c["route"] for c in trace.llm_calls] == ["router", "tro_ly_hue"]  # cả lần định tuyến lẫn lần trả lời đã có phản hồi


def test_notice_only_for_cited_target_folders(deps):
    gen = FakeGenerator()
    trace = run(deps, "Giá vé Đại Nội?", gen)
    targets = [s.source for s in trace.so_nguon if s.source.startswith(("travel/tickets/", "travel/places/", "festivals/"))]
    assert targets, "câu thử phải có nguồn thuộc thư mục đích trong ngữ cảnh"
    first = next(s for s in trace.so_nguon if s.source in targets)
    trace = run(deps, "Giá vé Đại Nội?", FakeGenerator(answer=f"Có thông tin [{first.id}]."))
    assert trace.notice is not None
    other = next((s for s in trace.so_nguon if s.source not in targets), None)
    if other is not None:
        assert run(deps, "Giá vé Đại Nội?", FakeGenerator(answer=f"Có thông tin [{other.id}].")).notice is None
    refusal = run(deps, "Giá vé Đại Nội?", FakeGenerator(answer="Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này."))
    assert refusal.notice is None and refusal.cited == ()
