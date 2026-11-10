"""Phase 9 B3 (plan `docs/superpowers/plans/2026-11-03-phase-9-b3-plan.md` D1–D5, D9 (b)) — logic nhớ hội thoại, 0 USD.

Kho cuộc trò chuyện + cookie + lịch sử đi vào model + đếm token. Model là `OpenAIResponsesModel` thật của SDK với client trả phản hồi dựng sẵn
(như `test_b2_tool_loop.py`); tìm kho là Qdrant thật (chỉ đọc). Không phải bằng chứng model thật nhớ đúng — phần đó ở lượt đo có phí.
"""
import asyncio
import copy
import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.conversations import ConversationStore, stored_answer
from api.routes.chat import METRIC_FIELDS
from core.settings_loader import load_settings
from core.schema import GenerationError
from llm.assistant import AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream
from llm.full_corpus_prompt import ASSISTANT_HISTORY_NOTE, INSUFFICIENT_ANSWER, ROUTER_HISTORY_NOTE
from llm.generator_openai_full_corpus import with_history
from retrieval.full_corpus_context import ITEM_OVERHEAD, TOOL_PATH_OVERHEAD
from test_api_chat import chat_log_records, metric_lines
from test_b2_tool_loop import answer, deps, generator, tool_call  # noqa: F401  (fixture `deps` dùng chung)

B2B = AssistantFlags(tim_them=True)


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def store(**kw) -> ConversationStore:
    return ConversationStore(lambda text: len(text.split()), **kw)


def test_store_keeps_last_three_turns_and_token_cap_dropping_oldest_first():
    s = store(max_history_tokens=12)
    cid = s.ensure(None)
    for i in range(5):
        s.append(cid, f"câu {i}", f"đáp {i}")
    assert s.history(cid) == (("câu 2", "đáp 2"), ("câu 3", "đáp 3"), ("câu 4", "đáp 4"))  # 3 lượt gần nhất
    s.append(cid, "một câu hỏi rất dài có tới mười chữ để vượt trần", "đáp")  # 12 chữ ⇒ vượt trần token ⇒ bỏ lượt cũ nhất trước
    assert s.history(cid) == (("một câu hỏi rất dài có tới mười chữ để vượt trần", "đáp"),)


def test_store_ttl_new_conversation_and_reset():
    clock = Clock()
    s = store(ttl=10, clock=clock)
    cid = s.ensure(None)
    s.append(cid, "Tên tôi là Lan", "Chào Lan")
    assert s.ensure(cid) == cid and s.history(cid)
    clock.now = 11  # hết hạn ⇒ mã cũ không còn, cuộc mới rỗng
    new = s.ensure(cid)
    assert new != cid and s.history(new) == () and s.history(cid) == ()
    s.append(new, "a", "b")
    fresh = s.reset(new)  # "Cuộc trò chuyện mới"
    assert fresh != new and s.history(new) == () and s.history(fresh) == ()


def test_store_caps_number_of_conversations_and_question_only_mode():
    s = store(max_conversations=2, keep_answers=False)
    ids = [s.ensure(None) for _ in range(3)]
    assert s.history(ids[0]) == () and s.ensure(ids[0]) != ids[0]  # cuộc cũ nhất bị bỏ khi vượt trần
    s.append(ids[2], "câu", "đáp")
    assert s.history(ids[2]) == (("câu", ""),)  # chỉ nhớ câu hỏi (đường dự phòng)


def test_stored_answer_drops_citation_marks():
    assert stored_answer("Mở cửa 7 giờ [1], giá 200.000 đồng [Nguồn 2].") == "Mở cửa 7 giờ, giá 200.000 đồng."


def test_with_history_empty_is_the_b2_string_and_items_keep_order():
    assert with_history("Câu hỏi:\nx", ()) == "Câu hỏi:\nx"
    items = with_history("lượt này", (("q1", "a1"), ("q2", "")))
    assert items == [{"role": "user", "content": "q1"}, {"role": "assistant", "content": "a1"}, {"role": "user", "content": "q2"},
                     {"role": "user", "content": "lượt này"}]


def test_history_reaches_router_and_assistant_with_history_notes(deps):
    """D3: lượt có lịch sử ⇒ định tuyến + trợ lý nhận lịch sử và bản lời dặn có câu dặn lịch sử; lượt không lịch sử ⇒ bản B2."""
    def script(n, kw):
        if n == 1:  # định tuyến
            return [answer_route("tro_ly_hue")]
        return [answer("Không có [1].") if n == 3 else tool_call("Giá vé lăng Tự Đức")]

    gen = generator(script)
    trace = AnswerTrace(history=(("Lăng Tự Đức mở cửa mấy giờ?", "Mở cửa từ 7 giờ."),))
    asyncio.run(answer_turn("Còn giá vé ở đó?", *deps, gen, trace, AssistantFlags(router=True, tim_them=True)))
    calls = gen.client.responses.calls
    assert ROUTER_HISTORY_NOTE in calls[0]["instructions"] and ASSISTANT_HISTORY_NOTE in calls[1]["instructions"]
    first_user = [i for i in calls[1]["input"] if isinstance(i, dict) and i.get("role") == "user"]
    assert first_user[0]["content"] == "Lăng Tự Đức mở cửa mấy giờ?" and first_user[-1]["content"].startswith("Câu hỏi:\nCòn giá vé ở đó?")

    gen2 = generator(script)
    asyncio.run(answer_turn("Lăng Tự Đức mở cửa mấy giờ?", *deps, gen2, AnswerTrace(), AssistantFlags(router=True, tim_them=True)))
    first = gen2.client.responses.calls
    assert ROUTER_HISTORY_NOTE not in first[0]["instructions"] and ASSISTANT_HISTORY_NOTE not in first[1]["instructions"]
    assert isinstance(first[0]["input"], list) and len(first[0]["input"]) == 1  # SDK gói một chuỗi thành đúng một tin user


def answer_route(route: str) -> dict:
    return {"type": "message", "id": "m_route", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": json.dumps({"route": route}), "annotations": []}]}


def test_budget_count_with_history_matches_sent_text_and_adds_item_overhead(deps):
    """D5 (a): lịch sử 3 lượt + 2 lần `tim_kho` — số đếm của bộ dựng ngữ cảnh (bỏ phần đệm API) lệch phần chữ của thân yêu cầu < 128;
    phần đệm cộng theo số mục (ITEM_OVERHEAD mỗi mục). Phần đệm thật của API đo ở lượt có phí (review C142 m-1)."""
    history = (("Đại Nội mở cửa mấy giờ?", "Mở cửa từ 6 giờ 30."), ("Giá vé bao nhiêu?", "Giá vé người lớn 200.000 đồng."),
               ("Có giảm cho học sinh không?", "Học sinh được giảm giá vé."))
    gen = generator(lambda n, kw: [tool_call(f"vé lăng {n}")] if n <= 2 else [answer(INSUFFICIENT_ANSWER)])
    trace = AnswerTrace(history=history)
    asyncio.run(answer_turn("Còn lăng Khải Định thì sao?", *deps, gen, trace, B2B))
    builder = deps[1]
    sent = gen.client.responses.calls[2]
    texts = [sent["instructions"]] + [_text(i) for i in sent["input"]]
    sent_tokens = sum(len(builder._tokenizer.encode(t)) for t in texts if t)
    counted = builder._token_count("Còn lăng Khải Định thì sao?", "\n\n".join(trace.context_parts), None, gen.assistant_history_instructions,
                                   history, n_tool_items=4)
    n_items = 2 * len(history) + 1 + 4
    assert abs(counted - TOOL_PATH_OVERHEAD - ITEM_OVERHEAD * n_items - sent_tokens) < 128
    assert counted > builder._token_count("Còn lăng Khải Định thì sao?", "\n\n".join(trace.context_parts), None, gen.assistant_history_instructions)


def _text(item) -> str:
    if isinstance(item, str):
        return item
    if item.get("type") == "function_call":
        return item["arguments"]
    if item.get("type") == "function_call_output":
        return item["output"]
    content = item.get("content")
    return content if isinstance(content, str) else " ".join(c.get("text", "") for c in content or [])


def test_stream_tool_path_sends_generating_right_before_first_text(deps):
    """D9 (b): đường trợ lý có công cụ ⇒ `generating` ngay trước `delta` đầu, sau các lượt `searching` / `searched`."""
    gen = generator(lambda n, kw: [tool_call("Giá vé Đại Nội")] if n == 1 else [answer("Giá vé có trong nguồn [1].")])

    async def collect():
        return [e async for e in answer_turn_stream("Giá vé Đại Nội?", *deps, gen, AnswerTrace(), B2B)]

    names = [data["stage"] if kind == "status" else kind for kind, data in asyncio.run(collect())]
    first_delta = names.index("delta")
    assert names[first_delta - 1] == "generating" and names.count("generating") == 1 and "searching" in names[:first_delta]


class MemoryGenerator:
    """Generator thay thế cho route (không mạng): ghi lịch sử mỗi lượt nhận được."""
    assistant_instructions = ""

    def __init__(self):
        self.seen = []

    def assistant_instructions_for(self, history):
        return ""

    async def route(self, query, call_log, history=()):
        return "tro_ly_hue"

    async def generate_with_tools(self, prompt, tool_fn, call_log, history=(), **_cong_cu):  # nhận mọi công cụ theo cờ (ngay_lich_fn…) — test chỉ kiểm lịch sử
        self.seen.append(history)
        return SimpleNamespace(text="Mở cửa từ 7 giờ [1].")


def test_api_cookie_carries_history_and_new_conversation_clears_it(caplog):
    """D1, D4: cookie HttpOnly / SameSite=Strict / Path=/api; lượt 2 nhận lịch sử lượt 1 (câu trả lời đã bỏ mã trích dẫn); "cuộc mới" xoá;
    log có số đếm lịch sử, không có mã cuộc."""
    app = create_app()
    with TestClient(app) as client:
        app.state.conversations = ConversationStore(lambda t: len(t.split()))
        gen = MemoryGenerator()
        original = app.state.generator, app.state.generator_ready
        app.state.generator, app.state.generator_ready = gen, True
        with chat_log_records(caplog) as records:
            first = client.post("/api/chat", json={"query": "Mình tên là Lan, Đại Nội mở cửa mấy giờ?"})
            cookie = first.headers["set-cookie"]
            second = client.post("/api/chat", json={"query": "Còn hôm thứ Hai thì sao?"})
            client.post("/api/conversation/new")
            third = client.post("/api/chat", json={"query": "Đại Nội mở cửa mấy giờ?"})
            messages = [r.getMessage() for r in records if r.name == "chat"]
            metrics = metric_lines(records)
        app.state.generator, app.state.generator_ready = original
    assert first.status_code == second.status_code == third.status_code == 200
    assert "HttpOnly" in cookie and "SameSite=strict" in cookie and "Path=/api" in cookie and "Secure" not in cookie
    assert gen.seen[0] == () and gen.seen[1] == (("Mình tên là Lan, Đại Nội mở cửa mấy giờ?", "Mở cửa từ 7 giờ."),) and gen.seen[2] == ()
    conversation_id = cookie.split(";")[0].split("=", 1)[1]
    assert [m["n_history_turns"] for m in metrics] == [0, 1, 0] and set(metrics[0]) == set(METRIC_FIELDS)
    assert metrics[1]["history_tokens"] > 0 and all(conversation_id not in m and "Lan" not in m for m in messages)


class FailingGenerator(MemoryGenerator):
    async def generate_with_tools(self, prompt, tool_fn, call_log, history=()):
        raise GenerationError("x")


def test_api_error_turn_still_sets_cookie_and_is_not_remembered():
    """Review C145 m-2: lượt lỗi vẫn gửi cookie (không cuộc mồ côi) và không ghi vào lịch sử."""
    app = create_app()
    with TestClient(app) as client:
        app.state.conversations = ConversationStore(lambda t: len(t.split()))
        original = app.state.generator, app.state.generator_ready
        app.state.generator, app.state.generator_ready = FailingGenerator(), True
        response = client.post("/api/chat", json={"query": "Đại Nội mở cửa mấy giờ?"})
        app.state.generator, app.state.generator_ready = original
        conversation_id = response.headers["set-cookie"].split(";")[0].split("=", 1)[1]
        assert response.status_code == 502 and app.state.conversations.history(conversation_id) == ()


def test_api_without_memory_flag_sets_no_cookie():
    settings = copy.deepcopy(load_settings())  # cờ nhớ TẮT tường minh — `settings.yaml` bật từ B3b (B141)
    settings["assistant"]["nho_hoi_thoai"] = False
    app = create_app(settings)
    with TestClient(app) as client:
        gen = MemoryGenerator()
        original = app.state.generator, app.state.generator_ready
        app.state.generator, app.state.generator_ready = gen, True
        response = client.post("/api/chat", json={"query": "Đại Nội mở cửa mấy giờ?"})
        app.state.generator, app.state.generator_ready = original
    assert response.status_code == 200 and "set-cookie" not in response.headers and app.state.conversations is None


@pytest.mark.parametrize("flag", ["nho_hoi_thoai", "nho_cau_tra_loi"])
def test_memory_flags_read_from_settings(flag):
    assert getattr(AssistantFlags.from_settings({"assistant": {flag: not AssistantFlags.__dataclass_fields__[flag].default}}), flag) \
        is not AssistantFlags.__dataclass_fields__[flag].default
