"""Lớp dịch Bedrock (`llm/bedrock_model.py`, đổi tạm model viết 21/11/2026) — logic thuần + vòng chạy SDK thật, 0 USD, không mạng.

Phản hồi của Claude ở đây là bản DỰNG SẴN (qua `httpx.MockTransport`): kiểm cách dịch và việc SDK chạy được vòng công cụ / khuôn / stream giả
trên lớp này. Đây KHÔNG phải bằng chứng Bedrock thật nhận thân yêu cầu — phần đó ở lượt gọi thật ghi trong report của nhánh.
"""
import asyncio
import copy
import datetime as dt
import json

import httpx
import pytest
from agents import Agent, ModelSettings, OpenAIResponsesModel, RunConfig, Runner, function_tool
from agents.agent_output import AgentOutputSchema
from openai.types.shared import Reasoning

from core.schema import GenerationError
from core.settings_loader import load_settings, validate_phase6_settings
from llm.bedrock_model import BedrockClaudeModel, build_body, sign_headers, strip_constraints, to_messages, to_response
from llm.generator_openai_full_corpus import AnswerOutput, CallLog, OpenAIFullCorpusGenerator, RouteSplitOutput, SuaLichOutput
from llm.pricing import cost_usd

CLAUDE_USAGE = {"input_tokens": 100, "output_tokens": 50, "cache_creation_input_tokens": 30, "cache_read_input_tokens": 20,
                "output_tokens_details": {"thinking_tokens": 7}}


def claude_message(*blocks: dict, n: int = 1) -> dict:
    return {"id": f"msg_bdrk_{n}", "type": "message", "role": "assistant", "content": list(blocks), "stop_reason": "end_turn", "usage": CLAUDE_USAGE}


def bedrock_settings() -> dict:
    settings = copy.deepcopy(load_settings(validate_private_paths=False))
    settings["full_corpus_generation"]["provider"] = "bedrock"
    return settings


def scripted_model(tmp_path, replies: list[dict]) -> tuple[BedrockClaudeModel, list[httpx.Request]]:
    """Lớp dịch thật, chỉ thay đường mạng: mỗi yêu cầu nhận phản hồi kế tiếp trong `replies`; ghi lại mọi yêu cầu đã gửi."""
    creds = tmp_path / "creds.json"
    creds.write_text(json.dumps({"accessKeyId": "AKIDEXAMPLE", "secretAccessKey": "secret", "sessionToken": "token"}), encoding="utf-8")
    model = BedrockClaudeModel(model="claude-test", region="ap-southeast-1", creds_file=str(creds), timeout=5, max_tokens=1000, reasoning_default="low")
    sent: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(200, json=replies[len(sent) - 1])

    model.http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return model, sent


def test_history_tool_round_and_image_become_claude_messages():
    """Lịch sử dạng gọn + mục SDK tự sinh trong vòng công cụ + ảnh data URL ⇒ tin Claude xen kẽ vai, `tool_use` / `tool_result` khớp `call_id`."""
    items = [
        {"role": "user", "content": "câu 1"},
        {"role": "user", "content": "câu 2"},  # lượt trước chỉ nhớ câu hỏi ⇒ hai tin user liền nhau phải gộp
        {"role": "assistant", "content": "đáp 2"},
        {"role": "user", "content": [{"type": "input_text", "text": "Danh sách"},
                                     {"type": "input_image", "image_url": "data:image/jpeg;base64,QUJD", "detail": "auto"}]},
        {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "", "annotations": []}]},  # chữ rỗng ⇒ bỏ
        {"type": "function_call", "id": "toolu_1", "call_id": "toolu_1", "name": "tim_kho", "arguments": '{"cau_tim": "Đại Nội"}', "status": "completed"},
        {"type": "function_call_output", "call_id": "toolu_1", "output": "[Nguồn 1] …"},
    ]
    assert to_messages(items) == [
        {"role": "user", "content": [{"type": "text", "text": "câu 1"}, {"type": "text", "text": "câu 2"}]},
        {"role": "assistant", "content": [{"type": "text", "text": "đáp 2"}]},
        {"role": "user", "content": [{"type": "text", "text": "Danh sách"},
                                     {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": "QUJD"}}]},
        {"role": "assistant", "content": [{"type": "tool_use", "id": "toolu_1", "name": "tim_kho", "input": {"cau_tim": "Đại Nội"}}]},
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_1", "content": "[Nguồn 1] …"}]},
    ]
    assert to_messages("xin chào") == [{"role": "user", "content": [{"type": "text", "text": "xin chào"}]}]
    with pytest.raises(ValueError):
        to_messages([{"role": "system", "content": "x"}])


def test_schema_constraints_are_stripped_but_field_names_are_kept():
    """`maxItems` / `minimum`… bị Bedrock trả 400 (đo 21/11) ⇒ gỡ; trường mang TÊN trùng từ khoá vẫn còn. Hai khuôn thật có `max_length`."""
    schema = {"type": "object", "properties": {"pattern": {"type": "string", "maxLength": 5}, "n": {"type": "integer", "minimum": 1, "maximum": 3}},
              "required": ["pattern", "n"], "additionalProperties": False}
    assert strip_constraints(schema) == {"type": "object", "properties": {"pattern": {"type": "string"}, "n": {"type": "integer"}},
                                         "required": ["pattern", "n"], "additionalProperties": False}
    for output_type in (RouteSplitOutput, SuaLichOutput):
        original = AgentOutputSchema(output_type).json_schema()
        assert '"maxItems":' in json.dumps(original) and '"maxItems":' not in json.dumps(strip_constraints(original))


def test_body_carries_tools_format_and_an_explicit_reasoning_mode():
    def tim_kho(cau_tim: str) -> str:
        """Tìm trong kho."""
        return ""

    tool = function_tool(tim_kho, name_override="tim_kho", failure_error_function=None)
    # `max_tokens` của agent (nếu có) KHÔNG được hạ trần: luôn gửi số của cấu hình (User: không đặt trần token đầu ra)
    settings = ModelSettings(include_usage=True, store=False, parallel_tool_calls=False, extra_args={"prompt_cache_key": "k"}, max_tokens=50)
    body = build_body("lời dặn", "câu hỏi", settings, [tool], AgentOutputSchema(AnswerOutput), 1000, "none")
    assert body["anthropic_version"] == "bedrock-2023-05-31" and body["max_tokens"] == 1000 and body["system"] == "lời dặn"
    # khuôn + công cụ ⇒ KHÔNG ép khuôn (Claude sẽ gọi công cụ mãi không viết — đo 21/11); khuôn đi theo công cụ nội bộ `tra_loi`
    assert [(t["name"], t["strict"], t["input_schema"]["required"]) for t in body["tools"]] == [("tim_kho", True, ["cau_tim"]), ("tra_loi", True, ["answer"])]
    assert body["tools"][1]["input_schema"] == AgentOutputSchema(AnswerOutput).json_schema() and "output_config" not in body
    assert body["tool_choice"] == {"type": "auto", "disable_parallel_tool_use": True}
    # mức mặc định `none` ⇒ `between_tools`, không gửi effort; không trường nào của riêng OpenAI lọt sang
    assert body["thinking"] == {"type": "between_tools"}
    # không công cụ và lượt chưa có lời gọi công cụ nào ⇒ ép khuôn như cũ, không có công cụ nội bộ
    no_tools = build_body("lời dặn", "câu hỏi", settings, [], AgentOutputSchema(AnswerOutput), 1000, "none")
    assert no_tools["output_config"] == {"format": {"type": "json_schema", "schema": AgentOutputSchema(AnswerOutput).json_schema()}} and "tools" not in no_tools
    # mọi công cụ đã ẨN nhưng lượt đã có lời gọi công cụ (hết lượt tìm) ⇒ KHÔNG ép khuôn — ép thì Claude viết rác vào khuôn ("placeholder", tên công cụ,
    # rỗng; lỗi M03 21/11) — chỉ còn công cụ nội bộ để nộp câu trả lời
    rounds = [{"role": "user", "content": "câu hỏi"},
              {"type": "function_call", "id": "toolu_1", "call_id": "toolu_1", "name": "tim_kho", "arguments": '{"cau_tim": "x"}', "status": "completed"},
              {"type": "function_call_output", "call_id": "toolu_1", "output": "[Nguồn 1] …"}]
    hidden = build_body("lời dặn", rounds, settings, [], AgentOutputSchema(AnswerOutput), 1000, "none")
    assert [t["name"] for t in hidden["tools"]] == ["tra_loi"] and "output_config" not in hidden
    assert hidden["tool_choice"] == {"type": "auto", "disable_parallel_tool_use": True}
    assert not {"store", "prompt_cache_key", "temperature", "top_p", "model"} & body.keys()

    # agent KHÔNG tự đặt mức ⇒ mức mặc định của cấu hình; agent tự đặt "low" (nhóm lịch) ⇒ giữ "low" dù mặc định là "high"
    for settings, default, effort in ((ModelSettings(), "medium", "medium"), (ModelSettings(reasoning=Reasoning(effort="low")), "high", "low")):
        sent = build_body(None, "câu", settings, [], None, 1000, default)
        assert sent["thinking"] == {"type": "adaptive"} and sent["output_config"] == {"effort": effort} and "system" not in sent and "tools" not in sent


def test_response_drops_thinking_and_usage_counts_like_openai():
    """Khối suy luận bỏ; `tool_use` giữ `id` làm `call_id`; usage: phần vào = thường + ghi đệm + đọc đệm ⇒ `cost_usd` giá Bedrock đúng từng phần."""
    response = to_response(claude_message({"type": "thinking", "thinking": "…", "signature": "s"}, {"type": "text", "text": '{"answer": "a"}'},
                                          {"type": "tool_use", "id": "toolu_9", "name": "tim_kho", "input": {"cau_tim": "Huế"}}), "claude-test")
    assert [item.type for item in response.output] == ["message", "function_call"]
    assert response.output[0].content[0].text == '{"answer": "a"}'
    call = response.output[1]
    assert (call.call_id, call.name, json.loads(call.arguments)) == ("toolu_9", "tim_kho", {"cau_tim": "Huế"})
    usage = response.usage
    assert (usage.input_tokens, usage.output_tokens, usage.total_tokens) == (150, 50, 200)
    assert (usage.input_tokens_details.cached_tokens, usage.input_tokens_details.cache_write_tokens) == (20, 30)
    assert usage.output_tokens_details.reasoning_tokens == 7
    expected = (100 * 2.0 + 30 * 2.5 + 20 * 0.1 + 50 * 10.0) / 1_000_000
    assert cost_usd(150, 50, 30, 20, provider="bedrock") == pytest.approx(expected)
    assert cost_usd(150, 50, 30, 20) == pytest.approx((100 * 0.1 + 30 * 0.125 + 20 * 0.01 + 50 * 0.5) / 1_000_000)  # mặc định vẫn giá luna


def test_internal_answer_tool_never_reaches_the_sdk():
    """Công cụ nội bộ `tra_loi` (lượt có cả công cụ lẫn khuôn): (1) chỉ `tra_loi` ⇒ tham số thành tin trả lời JSON, chữ dẫn bỏ, hai lần gọi lấy lần
    đầu; (2) `tra_loi` cùng công cụ thật ⇒ chạy công cụ thật, bỏ `tra_loi`; (3) chữ thường không gọi gì ⇒ bọc vào khuôn một trường chuỗi, chữ đã
    là JSON thì giữ; khuôn nhiều trường ⇒ lỗi nhóm model; (4) lời gọi KHÔNG gửi `tra_loi` ⇒ chữ giữ nguyên như trước."""
    schema = AgentOutputSchema(AnswerOutput).json_schema()

    def submit(answer: str, n: int = 1) -> dict:
        return {"type": "tool_use", "id": f"toolu_a{n}", "name": "tra_loi", "input": {"answer": answer}}

    search = {"type": "tool_use", "id": "toolu_s", "name": "tim_kho", "input": {"cau_tim": "Huế"}}
    only = to_response(claude_message({"type": "text", "text": "Đã đủ."}, submit("Có [1]."), submit("Lần hai", 2)), "m", schema)
    assert [item.type for item in only.output] == ["message"] and json.loads(only.output[0].content[0].text) == {"answer": "Có [1]."}
    both = to_response(claude_message(submit("Có [1]."), search), "m", schema)
    assert [(item.type, getattr(item, "name", None)) for item in both.output] == [("function_call", "tim_kho")]
    plain = to_response(claude_message({"type": "text", "text": ' Có "thật" [1].\n'}), "m", schema)
    assert json.loads(plain.output[0].content[0].text) == {"answer": 'Có "thật" [1].'}
    already = to_response(claude_message({"type": "text", "text": '{"answer": "Có [1]."}'}), "m", schema)
    assert already.output[0].content[0].text == '{"answer": "Có [1]."}'
    fenced = to_response(claude_message({"type": "text", "text": '```json\n{"answer": "Vé 200.000 đồng [1]."}\n```'}), "m", schema)
    assert fenced.output[0].content[0].text == '{"answer": "Vé 200.000 đồng [1]."}'  # gỡ rào, dùng chính JSON bên trong
    code = to_response(claude_message({"type": "text", "text": "```\nkhông phải JSON\n```"}), "m", schema)
    assert json.loads(code.output[0].content[0].text) == {"answer": "```\nkhông phải JSON\n```"}  # rào không chứa JSON ⇒ bọc nguyên chữ
    with pytest.raises(GenerationError):
        to_response(claude_message({"type": "text", "text": "chữ thường"}), "m", AgentOutputSchema(RouteSplitOutput).json_schema())
    untouched = to_response(claude_message({"type": "text", "text": "chữ thường"}), "m")
    assert untouched.output[0].content[0].text == "chữ thường"


def test_sigv4_signature_is_stable_for_fixed_inputs():
    """Cùng đầu vào ⇒ cùng chữ ký; đổi thân ⇒ chữ ký đổi; header ký gồm token phiên. (Chữ ký ĐÚNG với AWS chỉ lượt gọi thật chứng minh.)"""
    creds = {"accessKeyId": "AKIDEXAMPLE", "secretAccessKey": "secret", "sessionToken": "token"}
    now = dt.datetime(2026, 11, 21, 3, 0, 0, tzinfo=dt.timezone.utc)
    args = ("POST", "bedrock-runtime.ap-southeast-1.amazonaws.com", "/model/claude-test/invoke")
    first = sign_headers(*args, b"{}", "ap-southeast-1", creds, now)
    assert first == sign_headers(*args, b"{}", "ap-southeast-1", creds, now)
    assert first["authorization"] != sign_headers(*args, b"{ }", "ap-southeast-1", creds, now)["authorization"]
    assert first["authorization"].startswith("AWS4-HMAC-SHA256 Credential=AKIDEXAMPLE/20261121/ap-southeast-1/bedrock/aws4_request, "
                                             "SignedHeaders=accept;content-type;host;x-amz-date;x-amz-security-token, Signature=")
    assert "secret" not in json.dumps(first)


@pytest.mark.parametrize("streamed", [False, True])
def test_sdk_tool_loop_runs_on_the_bedrock_model(tmp_path, streamed):
    """Vòng chạy THẬT của SDK trên lớp dịch: lần 1 Claude xin công cụ, lần 2 trả khuôn. Đường thường và đường stream giả ra cùng kết quả, cùng
    usage, cùng tiền (giá Bedrock); đường stream chỉ phát chữ ở lần gọi viết câu trả lời."""
    model, sent = scripted_model(tmp_path, [
        claude_message({"type": "thinking", "thinking": "…", "signature": "s"},
                       {"type": "tool_use", "id": "toolu_1", "name": "tim_kho", "input": {"cau_tim": "Đại Nội"}}, n=1),
        claude_message({"type": "text", "text": "Mình đã có đủ thông tin."},  # chữ dẫn đi kèm bị bỏ; câu trả lời = tham số của `tra_loi`
                       {"type": "tool_use", "id": "toolu_2", "name": "tra_loi", "input": {"answer": "Có [1]."}}, n=2),
    ])
    seen = []

    def tim_kho(cau_tim: str) -> str:
        """Tìm trong kho."""
        seen.append(cau_tim)
        return "[Nguồn 1] Đại Nội"

    agent = Agent(name="thu", instructions="lời dặn", model=model, output_type=AnswerOutput,
                  model_settings=ModelSettings(include_usage=True, store=False, parallel_tool_calls=False),
                  tools=[function_tool(tim_kho, name_override="tim_kho", failure_error_function=None)])
    call_log, config = CallLog(), RunConfig(tracing_disabled=True)

    async def run():
        if not streamed:
            return await Runner.run(agent, input="câu hỏi", max_turns=3, run_config=config, hooks=call_log), []
        result = Runner.run_streamed(agent, input="câu hỏi", max_turns=3, run_config=config, hooks=call_log)
        deltas = [event.data.delta async for event in result.stream_events()
                  if event.type == "raw_response_event" and event.data.type == "response.output_text.delta"]
        return result, deltas

    result, deltas = asyncio.run(run())
    assert result.final_output == AnswerOutput(answer="Có [1].") and seen == ["Đại Nội"]
    assert deltas == (['{"answer": "Có [1]."}'] if streamed else [])
    second = json.loads(sent[1].content)
    assert [m["role"] for m in second["messages"]] == ["user", "assistant", "user"]  # khối suy luận của lần 1 không gửi lại
    assert second["messages"][1]["content"] == [{"type": "tool_use", "id": "toolu_1", "name": "tim_kho", "input": {"cau_tim": "Đại Nội"}}]
    assert second["messages"][2]["content"] == [{"type": "tool_result", "tool_use_id": "toolu_1", "content": "[Nguồn 1] Đại Nội"}]
    assert sent[0].url.path == "/model/claude-test/invoke" and sent[0].headers["authorization"].startswith("AWS4-HMAC-SHA256 ")
    one_call = {"input_tokens": 150, "output_tokens": 50, "reasoning_tokens": 7, "cached_tokens": 20, "cache_write_tokens": 30,
                "usd": pytest.approx(cost_usd(150, 50, 30, 20, provider="bedrock"))}
    assert [{key: call[key] for key in one_call} for call in call_log.calls] == [one_call, one_call]
    assert [call["kind"] for call in call_log.calls] == [["function_call"], ["message"]]


def test_403_error_names_the_bedrock_key_and_hides_the_response_body(tmp_path):
    """Thân 403 của AWS có ARN / mã tài khoản ⇒ không được vào lời lỗi; lời lỗi phải có chữ "khoá Bedrock"."""
    model, _ = scripted_model(tmp_path, [])
    body = "User: arn:aws:sts::123456789012:assumed-role/ten-vai/x is not authorized"
    model.http = httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(403, text=body)))
    generator = OpenAIFullCorpusGenerator(client=None, model="claude-test", bedrock_model=model)
    with pytest.raises(GenerationError) as error:
        asyncio.run(generator.generate_chat("chào"))
    assert "khoá Bedrock" in str(error.value) and "123456789012" not in str(error.value) and "ten-vai" not in str(error.value.__cause__)


@pytest.mark.parametrize("fault", [httpx.Response(403, text="arn:aws:sts::123456789012:assumed-role/ten-vai/x"), httpx.Response(429, text="too many"),
                                   httpx.ReadTimeout("t"), httpx.ConnectError("c"), "khong_co_file_khoa"])
def test_stream_path_failures_are_generation_errors(tmp_path, fault):
    """Review C 21/11 (M1): trên đường STREAM lỗi của Bedrock đi thẳng tới nơi đọc (`chat.py`, `len_ke_hoach.py`), nơi chỉ nhận nhóm lỗi model
    (`GenerationError`…) ⇒ mọi lỗi của lớp dịch phải thuộc nhóm đó, không thì lịch mất câu dự phòng và ô chat báo sai loại lỗi."""
    model, _ = scripted_model(tmp_path, [])

    def handler(request: httpx.Request) -> httpx.Response:
        if isinstance(fault, Exception):
            raise fault
        return fault

    model.http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    if fault == "khong_co_file_khoa":
        model.creds_file = tmp_path / "khong_co.json"
    generator = OpenAIFullCorpusGenerator(client=None, model="claude-test", bedrock_model=model)

    async def read_stream():
        result, _ = generator.start_chat_stream("chào")
        async for _ in result.stream_events():
            pass

    with pytest.raises(GenerationError) as error:
        asyncio.run(read_stream())
    assert "123456789012" not in str(error.value) and "khong_co.json" not in str(error.value)


def test_error_text_masks_account_numbers_before_truncating(tmp_path):
    """Review C m1: che ARN / mã tài khoản TRƯỚC khi cắt 300 ký tự (mã vắt qua mốc cắt từng còn lại một phần)."""
    model, _ = scripted_model(tmp_path, [])
    body = "x" * 292 + "123456789012 het"
    model.http = httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(400, text=body)))
    with pytest.raises(GenerationError) as error:
        asyncio.run(OpenAIFullCorpusGenerator(client=None, model="claude-test", bedrock_model=model).generate_chat("chào"))
    assert "12345678" not in str(error.value) and "<aws>" in str(error.value)


def test_provider_switch_picks_the_model_class_and_openai_stays_openai(monkeypatch):
    """`provider: openai` ⇒ vẫn `OpenAIResponsesModel` với model luna; `bedrock` ⇒ lớp dịch, không cần khoá OpenAI. Không khoá giá trị đang ghi
    trong `settings.yaml` (dòng đó là công tắc — lật nó không được làm đỏ test)."""
    settings = copy.deepcopy(load_settings(validate_private_paths=False))
    settings["full_corpus_generation"]["provider"] = "openai"
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    openai_generator = OpenAIFullCorpusGenerator.from_environment(settings)
    assert type(openai_generator.responses_model) is OpenAIResponsesModel and openai_generator.responses_model.model == "gpt-6-luna"
    assert (openai_generator.provider, openai_generator.model) == ("openai", "gpt-6-luna")

    monkeypatch.delenv("OPENAI_API_KEY")
    with pytest.raises(GenerationError, match="HUE_BEDROCK_CREDS_FILE"):
        OpenAIFullCorpusGenerator.from_environment(bedrock_settings())
    monkeypatch.setenv("HUE_BEDROCK_CREDS_FILE", "/khong/co/file.json")  # file chỉ được đọc lúc gọi model
    bedrock_generator = OpenAIFullCorpusGenerator.from_environment(bedrock_settings())
    assert isinstance(bedrock_generator.responses_model, BedrockClaudeModel)
    assert (bedrock_generator.provider, bedrock_generator.model) == ("bedrock", "global.anthropic.claude-sonnet-5-5")
    assert all(agent.model is bedrock_generator.responses_model for agent in (
        bedrock_generator.answer_agent, bedrock_generator.router_agent, bedrock_generator.chat_agent, bedrock_generator.assistant_agent,
        bedrock_generator.bieu_mau_agent, bedrock_generator.lich_v2_agent, bedrock_generator.sua_lich_agent, bedrock_generator.web_agent))


def test_edit_understanding_agents_run_at_their_own_reasoning_level(monkeypatch):
    """Đường Bedrock: hai agent hiểu ý sửa lịch gửi mức `bedrock.reasoning_sua_lich` (high); viết câu lịch + lượt biểu mẫu giữ "low" của code; lời gọi
    không tự đặt mức (trả lời) theo `reasoning_default`. Đường OpenAI: agent sửa lịch vẫn "low" như trước."""
    monkeypatch.setenv("HUE_BEDROCK_CREDS_FILE", "/khong/co/file.json")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    settings = bedrock_settings()
    settings["full_corpus_generation"]["bedrock"].update(reasoning_sua_lich="high", reasoning_default="medium")
    generator = OpenAIFullCorpusGenerator.from_environment(settings)

    def sent_effort(agent) -> str:
        body = build_body(agent.instructions, "câu", agent.model_settings, [], AgentOutputSchema(agent.output_type), 1000,
                          generator.responses_model.reasoning_default)
        return body["output_config"]["effort"]

    assert [sent_effort(a) for a in (generator.sua_lich_agent, generator.sua_lich_cht_agent)] == ["high", "high"]
    assert [sent_effort(a) for a in (generator.lich_v2_agent, generator.bieu_mau_agent)] == ["low", "low"]
    assert sent_effort(generator.answer_agent) == "medium"

    openai_settings = copy.deepcopy(settings)
    openai_settings["full_corpus_generation"]["provider"] = "openai"
    openai_generator = OpenAIFullCorpusGenerator.from_environment(openai_settings)
    assert [a.model_settings.reasoning.effort for a in (openai_generator.sua_lich_agent, openai_generator.sua_lich_cht_agent)] == ["low", "low"]


def test_sonnet_only_instructions_are_appended_on_bedrock_and_absent_on_openai(monkeypatch):
    """Ba đoạn dặn chỉ dành cho Sonnet (21/11/2026): đường OpenAI gửi ĐÚNG các hằng lời dặn cũ (không thêm ký tự nào); đường Bedrock nối đoạn
    dặn vào đúng agent — trả lời / trợ lý (kể cả bản lịch sử, bản nhiều ý), viết câu lịch (bản nới một đến hai câu), hai agent hiểu ý sửa lịch."""
    from llm import full_corpus_prompt as p

    monkeypatch.setenv("HUE_BEDROCK_CREDS_FILE", "/khong/co/file.json")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    settings = bedrock_settings()
    sonnet = OpenAIFullCorpusGenerator.from_environment(settings)
    settings["full_corpus_generation"]["provider"] = "openai"
    luna = OpenAIFullCorpusGenerator.from_environment(settings)

    tool = f"{p.ANSWER_SYSTEM_INSTRUCTIONS}\n\n{p.ASSISTANT_TOOL_NOTE}"
    assert luna.answer_agent.instructions == p.ANSWER_SYSTEM_INSTRUCTIONS and luna.assistant_instructions == luna.assistant_agent.instructions == tool
    assert luna.assistant_history_agent.instructions == luna.assistant_instructions_for([("q", "a")]) == f"{tool}\n\n{p.ASSISTANT_HISTORY_NOTE}"
    assert luna.assistant_agent_nhieu_y.instructions == f"{p.ANSWER_SYSTEM_INSTRUCTIONS_NHIEU_Y}\n\n{p.ASSISTANT_TOOL_NOTE}"
    assert luna.bieu_mau_agent.instructions == f"{p.ANSWER_SYSTEM_INSTRUCTIONS}\n\n{p.LICH_TRINH_LUAT}"
    assert (luna.lich_v2_agent.instructions, luna.sua_lich_agent.instructions, luna.sua_lich_cht_agent.instructions) == (
        p.LICH_V2_LOI_DAN, p.SUA_LICH_LOI_DAN, p.SUA_LICH_LOI_DAN_CHT)
    assert (luna.router_agent.instructions, luna.router_history_agent.instructions) == (
        p.ROUTER_INSTRUCTIONS, f"{p.ROUTER_INSTRUCTIONS}\n\n{p.ROUTER_HISTORY_NOTE}")
    assert [a.instructions for a in luna.router_search_agents.values()] == [f"{p.ROUTER_INSTRUCTIONS}\n\n{p.ROUTER_SEARCH_V1}", f"{p.ROUTER_INSTRUCTIONS}\n\n{p.ROUTER_SEARCH_V3}"]
    assert (luna.chat_agent.instructions, luna.web_agent.instructions) == (sonnet.chat_agent.instructions, sonnet.web_agent.instructions)  # hai vai không có đoạn dặn riêng
    assert sonnet.router_agent.instructions == f"{p.ROUTER_INSTRUCTIONS}\n\n{p.SONNET_DINH_TUYEN}"
    assert all(p.SONNET_DINH_TUYEN in a.instructions for a in (sonnet.router_history_agent, *sonnet.router_search_agents.values()))

    # đoạn dặn riêng cho phần trả lời đã thử và gỡ (đo lại không đạt) ⇒ lời dặn trả lời / trợ lý của Sonnet y như luna
    for ten in ("answer_agent", "assistant_agent", "assistant_history_agent", "assistant_agent_nhieu_y", "assistant_history_agent_nhieu_y", "bieu_mau_agent"):
        if ten != "bieu_mau_agent":
            assert getattr(sonnet, ten).instructions == getattr(luna, ten).instructions
    assert sonnet.assistant_instructions == luna.assistant_instructions and not hasattr(p, "SONNET_TRA_LOI")
    assert sonnet.assistant_instructions_for([("q", "a")]) == sonnet.assistant_history_agent.instructions  # chuỗi đếm = chuỗi gửi
    assert sonnet.lich_v2_agent.instructions == p.LICH_V2_LOI_DAN_SONNET
    assert "một hoặc hai câu" in p.LICH_V2_LOI_DAN_SONNET and "đúng một câu" not in p.LICH_V2_LOI_DAN_SONNET
    assert sonnet.bieu_mau_agent.instructions.endswith(p.SONNET_GIU_DUNG_VAT)
    assert sonnet.sua_lich_agent.instructions.startswith(p.SUA_LICH_LOI_DAN) and "trả danh sách rỗng. Trường hợp" in sonnet.sua_lich_agent.instructions
    assert sonnet.sua_lich_cht_agent.instructions.startswith(p.SUA_LICH_LOI_DAN_CHT) and "trả chua_ho_tro để" in sonnet.sua_lich_cht_agent.instructions
    assert "{khong_ro}" not in sonnet.sua_lich_agent.instructions + sonnet.sua_lich_cht_agent.instructions


def test_settings_loader_accepts_bedrock_and_rejects_a_broken_block():
    settings = bedrock_settings()
    validate_phase6_settings(settings)
    for provider in ("anthropic", None):
        broken = copy.deepcopy(settings)
        broken["full_corpus_generation"]["provider"] = provider
        with pytest.raises(ValueError):
            validate_phase6_settings(broken)
    for key, value in (("region", None), ("reasoning_default", "minimal"), ("reasoning_sua_lich", None), ("max_tokens", 0)):
        broken = copy.deepcopy(settings)
        broken["full_corpus_generation"]["bedrock"][key] = value
        with pytest.raises(ValueError):
            validate_phase6_settings(broken)
