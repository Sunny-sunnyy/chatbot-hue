"""Phase 9 B2 (plan `docs/superpowers/plans/2026-11-03-phase-9-b2-plan.md` D2–D5, D10; review C135 m-6) — logic vòng công cụ, 0 USD.

Model là `OpenAIResponsesModel` **thật** của SDK với một client chỉ có `responses.create` trả phản hồi dựng sẵn (cách
`data/phase_9/b2/probe_sdk.md`): vòng lặp, công cụ, hook, `error_handlers` là code SDK thật; tìm kho là Qdrant thật (chỉ đọc).
Đây **không** phải bằng chứng model thật gọi công cụ đúng lúc — phần đó ở pilot có phí.
"""
import asyncio
import itertools
import json

import pytest
from openai.types.responses import Response, ResponseCompletedEvent, ResponseCreatedEvent, ResponseTextDeltaEvent

from core.schema import RetrievalDependencyError, RetrievedDocument
from core.settings_loader import load_settings
from evaluation.full_corpus_eval import build_context_builder, build_retrieval
from llm.assistant import MODEL_SEARCH_LIMIT, AnswerTrace, AssistantFlags, answer_turn, answer_turn_stream, search_into_trace
from llm.full_corpus_prompt import INSUFFICIENT_ANSWER, TOOL_LIMIT_TEXT
from llm.generator_openai_full_corpus import ASSISTANT_MAX_TURNS, OpenAIFullCorpusGenerator

V2 = AssistantFlags(lan_tim_dau="v2")
_ids = itertools.count(1)
USAGE = {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120,
         "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 3}}


def tool_call(query: str) -> dict:
    n = next(_ids)
    return {"type": "function_call", "id": f"fc_{n}", "call_id": f"call_{n}", "name": "tim_kho",
            "arguments": json.dumps({"cau_tim": query}, ensure_ascii=False), "status": "completed"}


def answer(text: str) -> dict:
    return {"type": "message", "id": f"msg_{next(_ids)}", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": json.dumps({"answer": text}, ensure_ascii=False), "annotations": []}]}


class ScriptedResponses:
    """`script(n, kwargs)` ⇒ danh sách mục đầu ra của lần gọi thứ n (từ 1). Ghi kwargs mọi lần gọi."""

    def __init__(self, script):
        self.script, self.calls = script, []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        output = self.script(len(self.calls), kwargs)
        response = Response.model_validate({"id": f"resp_{next(_ids)}", "created_at": 0, "model": "probe", "object": "response",
                                            "output": output, "parallel_tool_calls": False, "tool_choice": "auto", "tools": [],
                                            "usage": USAGE, "status": "completed"})
        if not kwargs.get("stream"):
            return response

        async def events():
            yield ResponseCreatedEvent.model_validate({"type": "response.created", "response": response.model_dump(), "sequence_number": 0})
            for seq, item in enumerate(output, start=1):
                if item["type"] == "message":
                    yield ResponseTextDeltaEvent.model_validate({"type": "response.output_text.delta", "item_id": item["id"], "output_index": 0,
                                                                 "content_index": 0, "delta": item["content"][0]["text"],
                                                                 "sequence_number": seq, "logprobs": []})
            yield ResponseCompletedEvent.model_validate({"type": "response.completed", "response": response.model_dump(), "sequence_number": 99})
        return events()


class ScriptedClient:
    def __init__(self, script):
        self.responses = ScriptedResponses(script)

    async def close(self):
        return None


def generator(script) -> OpenAIFullCorpusGenerator:
    return OpenAIFullCorpusGenerator(client=ScriptedClient(script), model="probe")


@pytest.fixture(scope="module")
def deps():
    settings = load_settings(validate_private_paths=False)
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    yield service, build_context_builder(settings)
    service.close()


def run_turn(deps, query, gen, flags=V2) -> AnswerTrace:
    trace = AnswerTrace()
    asyncio.run(answer_turn(query, *deps, gen, trace, flags))
    return trace


def test_two_model_searches_number_on_and_second_batch_can_be_cited(deps):
    """D5: lần tìm thứ hai đánh số tiếp, bỏ đoạn đã có; câu trả lời trích nguồn của lần hai vẫn qua kiểm citation; D10 token = tổng."""
    first_batch = []  # số nguồn lần tìm 1, đọc từ kết quả công cụ model nhận được

    def script(n, kw):
        if n == 1:
            return [tool_call("Giá vé tham quan Đại Nội Huế")]
        if n == 2:
            first_batch.append(_tool_outputs(kw)[0].count("[Nguồn "))
            return [tool_call("Giờ mở cửa lăng Tự Đức")]
        return [answer(f"Có thông tin [1] và [{first_batch[0] + 1}].")]

    trace = run_turn(deps, "Đại Nội và lăng Tự Đức có gì?", generator(script))
    ids = [s.id for s in trace.so_nguon]
    assert ids == list(range(1, len(ids) + 1)) and len(ids) > first_batch[0]  # đánh số liền, lần 2 có nguồn mới
    assert len(trace.seen_ids) == len(set(trace.seen_ids)) == len(ids)  # không đoạn nào vào hai lần
    assert trace.model_searches == 2 and [t.get("by") for t in trace.tools] == ["model", "model"]
    assert trace.citation_error is None and {s.id for s in trace.cited} == {1, first_batch[0] + 1}
    assert len(trace.llm_calls) == 3 and trace.generated.input_tokens == 300 and trace.generated.reasoning_tokens == 9  # D10


def _tool_outputs(kwargs) -> list[str]:
    return [item["output"] for item in kwargs["input"] if isinstance(item, dict) and item.get("type") == "function_call_output"]


def test_third_model_search_gets_limit_text_and_does_not_search(deps):
    """D5 (A quyết (b)): lần model gọi `tim_kho` thứ 3 ⇒ chuỗi "đã hết lượt", không tìm Qdrant; model còn lượt 4 để viết."""
    gen = generator(lambda n, kw: [tool_call(f"câu tìm {n}")] if n <= 3 else [answer(INSUFFICIENT_ANSWER)])
    trace = run_turn(deps, "Huế có món gì ngon?", gen)
    assert trace.model_searches == 3 and MODEL_SEARCH_LIMIT == 2 and ASSISTANT_MAX_TURNS == 4
    assert [t.get("het_luot", False) for t in trace.tools] == [False, False, True]
    last_input = gen.client.responses.calls[3]["input"]
    assert any(isinstance(i, dict) and i.get("output") == TOOL_LIMIT_TEXT for i in last_input)
    assert trace.fixed_outcome is None and trace.answer == INSUFFICIENT_ANSWER


def test_max_turns_gives_fixed_refusal_and_one_delta_on_stream(deps):
    """D5: model vẫn gọi công cụ ở lượt 4 ⇒ handler ⇒ câu từ chối cố định `max_turns`; stream phát đúng một `delta` câu đó."""
    always_tool = lambda n, kw: [tool_call(f"câu tìm {n}")]  # noqa: E731
    trace = run_turn(deps, "Huế có món gì ngon?", generator(always_tool))
    assert trace.fixed_outcome == "max_turns" and trace.answer == INSUFFICIENT_ANSWER and trace.cited == ()

    async def collect():
        trace = AnswerTrace()
        events = [e async for e in answer_turn_stream("Huế có món gì ngon?", *deps, generator(always_tool), trace, V2)]
        return trace, events

    trace, events = asyncio.run(collect())
    deltas = [data for kind, data in events if kind == "delta"]
    stages = [data["stage"] for kind, data in events if kind == "status"]
    assert trace.fixed_outcome == "max_turns" and deltas == [INSUFFICIENT_ANSWER]
    assert stages[0] == "generating" and stages.count("searching") == 4 and "searched" in stages  # thẻ công cụ (D7): mỗi lần gọi


def test_concurrent_turns_do_not_share_max_turns_flag(deps):
    """Review C135 m-6: handler + cờ dựng mỗi lượt ⇒ hai câu chạy cùng lúc trên một generator không lẫn cờ."""
    def script(n, kw):
        text = json.dumps(kw["input"], ensure_ascii=False)
        if "câu chạm trần" in text:
            return [tool_call("tìm mãi")]
        return [answer(INSUFFICIENT_ANSWER)]

    gen = generator(script)

    async def both():
        a, b = AnswerTrace(), AnswerTrace()
        await asyncio.gather(answer_turn("câu chạm trần về Huế", *deps, gen, a, V2), answer_turn("câu thường về Huế", *deps, gen, b, V2))
        return a, b

    hit, normal = asyncio.run(both())
    assert hit.fixed_outcome == "max_turns" and normal.fixed_outcome is None


class BrokenRetrieval:
    """Qdrant hỏng giữa lượt (chỉ để kiểm đường lỗi trong công cụ)."""

    def search(self, query):
        raise RetrievalDependencyError("qdrant down")


def test_retrieval_error_inside_tool_surfaces_as_original_error(deps):
    """Lỗi tìm trong công cụ không thành chữ cho model và ra đúng lỗi gốc ⇒ route trả câu lỗi như B1."""
    gen = generator(lambda n, kw: [tool_call("Đại Nội")])
    with pytest.raises(RetrievalDependencyError):
        asyncio.run(answer_turn("Đại Nội có gì?", BrokenRetrieval(), deps[1], gen, AnswerTrace(), V2))


def test_budget_count_for_tool_path_is_within_safety_margin_of_sent_request(deps):
    """D5 (4): số đếm của bộ dựng ngữ cảnh (lời dặn trợ lý + câu hỏi + kết quả công cụ đã nối) lệch số token của thân yêu cầu thật
    gửi ở lượt viết < `safety_margin` (512). Đếm thân yêu cầu bằng cùng tokenizer — số token thật của API kiểm ở pilot (review C135 m-7)."""
    gen = generator(lambda n, kw: [tool_call("Giá vé Đại Nội"), ] if n <= 2 else [answer(INSUFFICIENT_ANSWER)])
    trace = run_turn(deps, "Giá vé Đại Nội và lăng Tự Đức?", gen)
    builder = deps[1]
    sent = gen.client.responses.calls[2]
    texts = [sent["instructions"]] + [_item_text(i) for i in sent["input"]]
    sent_tokens = sum(len(builder._tokenizer.encode(t)) for t in texts if t)
    counted = builder._token_count("Giá vé Đại Nội và lăng Tự Đức?", "\n\n".join(trace.context_parts), None, gen.assistant_instructions)
    assert abs(counted - sent_tokens) < 512


def _item_text(item) -> str:
    if isinstance(item, str):
        return item
    if item.get("type") == "function_call":
        return item["arguments"]
    if item.get("type") == "function_call_output":
        return item["output"]
    content = item.get("content")
    return content if isinstance(content, str) else " ".join(c.get("text", "") for c in content or [])


def test_v3_search_many_one_query_equals_search_and_merge_is_deterministic(deps):
    """D4: một câu ⇒ đúng `search`; nhiều câu ⇒ trộn RRF tất định, mỗi đoạn một lần, chỉ gồm đoạn của các câu nhỏ."""
    service = deps[0]
    one = service.search_many(["Giá vé Đại Nội Huế"])
    assert [d.id for d in one.documents] == [d.id for d in service.search("Giá vé Đại Nội Huế").documents]
    queries = ["Giá vé Đại Nội Huế", "Giờ mở cửa lăng Tự Đức"]
    first, second = service.search_many(queries), service.search_many(queries)
    ids = [d.id for d in first.documents]
    assert ids == [d.id for d in second.documents] and len(ids) == len(set(ids))
    union = {d.id for q in queries for d in service.search(q).documents}
    assert set(ids) <= union and first.trace.counts["n_queries"] == 2


def test_search_text_and_question_are_counted_separately(deps):
    """D3: tìm bằng câu tìm, đếm ngân sách bằng câu hỏi thật gửi model."""
    service, builder = deps
    trace = AnswerTrace()
    question = "Cho mình hỏi chi tiết giá vé và giờ mở cửa Đại Nội Huế dịp cuối tuần này với ạ, cảm ơn nhiều nhé"
    asyncio.run(search_into_trace(["Giá vé Đại Nội"], cau_hoi=question, retrieval_service=service, context_builder=builder, trace=trace))
    docs = service.search("Giá vé Đại Nội").documents
    assert trace.packed == builder.build(question, docs)
    assert trace.packed.input_tokens != builder.build("Giá vé Đại Nội", docs).input_tokens


def test_build_continues_numbering_and_skips_seen_documents(deps):
    """D5: lần dựng sau đánh số từ `first_id`, bỏ đoạn đã có; mặc định = một lần dựng như B1."""
    builder = deps[1]
    docs = [RetrievedDocument(id=f"f.md#{i}", score=1.0, text="", metadata={"evidence_parts": [{"text": f"bằng chứng {i}"}],
                                                                               "title": "T", "heading_path": ["M"], "source": "f.md"})
            for i in range(3)]
    first = builder.build("câu hỏi", docs[:2])
    more = builder.build("câu hỏi", docs, first_id=3, prior_context=first.text, skip_ids=frozenset(first.document_ids))
    assert [s.id for s in first.sources] == [1, 2] and more.document_ids == ("f.md#2",) and [s.id for s in more.sources] == [3]
    assert more.input_tokens > builder.build("câu hỏi", docs[2:]).input_tokens  # có tính phần ngữ cảnh trước


def test_flags_reject_router_variants_without_router():
    with pytest.raises(ValueError):
        AssistantFlags(lan_tim_dau="v1")
    assert AssistantFlags(lan_tim_dau="v2").uses_tools and AssistantFlags(router=True, tim_them=True).uses_tools
    assert not AssistantFlags(router=True, lan_tim_dau="v3").uses_tools
