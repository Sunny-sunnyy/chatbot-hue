"""Tool-less OpenAI Agents SDK full-corpus answer generator for Phase 6."""
import asyncio
import dataclasses
from dataclasses import dataclass
import logging
import os
import time
from typing import Any, Literal

from agents import (
    Agent,
    ModelSettings,
    OpenAIResponsesModel,
    RunConfig,
    RunHooks,
    RunResultStreaming,
    Runner,
    function_tool,
)
from agents.agent import ToolsToFinalOutputResult
from agents.exceptions import AgentsException
from openai import AsyncOpenAI, OpenAIError
from openai.types.shared import Reasoning
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from core.schema import GenerationError
from llm.pricing import cost_usd
from llm.full_corpus_prompt import (
    ANSWER_SYSTEM_INSTRUCTIONS,
    ASSISTANT_TOOL_NOTE,
    LICH_TRINH_MO_TA,
    NGAY_LICH_MO_TA,
    THOI_TIET_MO_TA,
    CHAT_INSTRUCTIONS,
    INSUFFICIENT_ANSWER,
    LICH_TRINH_LUAT,
    ROUTER_INSTRUCTIONS,
    ROUTER_SEARCH_V1,
    ROUTER_SEARCH_V3,
    ROUTER_HISTORY_NOTE,
    ASSISTANT_HISTORY_NOTE,
    TU_WEB_LUAT,
    build_answer_input,
)

logger = logging.getLogger("llm.full_corpus")
# Cổng đợt 1 D3 — X1c của C (V5, bộ phát triển: 0 / 16 từ chối, chữ đầu p95 4,75 s): mức suy luận của RIÊNG lần gọi lượt biểu mẫu
BIEU_MAU_REASONING = "low"


class AnswerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answer: str


class RouteOutput(BaseModel):
    """Đầu ra định tuyến (Phase 9 B1 D3): đúng một trong 4 tuyến, strict."""
    model_config = ConfigDict(extra="forbid")
    route: Literal["tro_chuyen", "tro_ly_hue", "ngoai_pham_vi", "khan_cap"]


class RouteSearchOutput(BaseModel):
    """B2 V1 (plan D2): tuyến + một câu tìm kho đứng một mình."""
    model_config = ConfigDict(extra="forbid")
    route: Literal["tro_chuyen", "tro_ly_hue", "ngoai_pham_vi", "khan_cap"]
    cau_tim: str


class RouteSplitOutput(BaseModel):
    """B2 V3 (plan D2): tuyến + 1–3 câu tìm (schema gửi `maxItems` 3; API thật có nhận không kiểm ở pilot)."""
    model_config = ConfigDict(extra="forbid")
    route: Literal["tro_chuyen", "tro_ly_hue", "ngoai_pham_vi", "khan_cap"]
    cau_tim: list[str] = Field(max_length=3)


ROUTER_OUTPUTS = {"v1": (RouteSearchOutput, ROUTER_SEARCH_V1), "v3": (RouteSplitOutput, ROUTER_SEARCH_V3)}
ASSISTANT_MAX_TURNS = 4  # B2 D5 (A quyết (b)): ≤ 2 lần tìm thật + lần 3 "đã hết lượt" + 1 lượt viết


ROUTER_MAX_OUTPUT_TOKENS = 512  # gồm cả token suy luận của model
WEB_MAX_OUTPUT_TOKENS = 1024  # B6 D8: lần gọi viết mục web (gồm token suy luận); mục ≤ 3 đoạn văn ngắn


def _dung_khi_hoi_lai(_context, results) -> ToolsToFinalOutputResult:
    """B5 D12 (b) / D15 — `tool_use_behavior` dạng hàm (probe 0 USD `data/phase_9/b5/probe_tool_use_behavior.py`): `lich_trinh` trả dữ liệu thẻ
    hỏi lại (dict có `loai`) ⇒ dừng lượt, thẻ thành `final_output`; mọi kết quả khác (`tim_kho`, khung lịch) ⇒ model chạy tiếp."""
    for result in results:
        if result.tool.name == "lich_trinh" and isinstance(result.output, dict) and "loai" in result.output:
            return ToolsToFinalOutputResult(is_final_output=True, final_output=result.output)
    return ToolsToFinalOutputResult(is_final_output=False)


@dataclass(frozen=True)
class GeneratedText:
    text: str
    response_id: str | None
    model: str
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    latency_ms: int
    finish_reason: str | None = None
    # phần token suy luận nằm trong output_tokens (usage.output_tokens_details); để log số đo /api/chat
    reasoning_tokens: int | None = None
    # phần của input_tokens đọc lại từ đệm / ghi vào đệm (usage.input_tokens_details) — giá khác nhau (User 30/10, B95)
    cached_tokens: int | None = None
    cache_write_tokens: int | None = None
    # mỗi lần gọi model trong lượt (`CallLog.calls`): token, ms, USD — log Phase 9 (plan B0 D5)
    llm_calls: tuple[dict, ...] = ()
    # B2 D5: lượt trợ lý chạm `max_turns` ⇒ handler trả câu từ chối; lõi đọc cờ này để đặt `outcome="max_turns"`
    hit_max_turns: bool = False
    # B5 D15 (đường B4 D8): công cụ `lich_trinh` thiếu số ngày ⇒ lượt dừng, giá trị công cụ trả (dữ liệu thẻ hỏi lại), không có chữ trả lời
    clarify: dict | None = None


def input_cache_tokens(usage: Any) -> tuple[int | None, int | None]:
    """(cached_tokens, cache_write_tokens) của một usage OpenAI / Agents SDK; không có `input_tokens_details` ⇒ (None, None).
    Lưu ý: Agents SDK điền 0 khi provider không gửi trường (`agents/usage.py`), nên 0 ở đây có thể là "không gửi"."""
    details = getattr(usage, "input_tokens_details", None)
    if details is None:
        return None, None
    return getattr(details, "cached_tokens", None), getattr(details, "cache_write_tokens", None)


def parse_structured_output(
    final_output: Any, expected_type: type[BaseModel]
) -> str:
    """Strictly validate and extract text from structured agent output.

    Fails closed on missing fields, extra fields, invalid JSON, or non-conforming types.
    """
    if isinstance(final_output, expected_type):
        val = getattr(final_output, "answer", None)
    elif isinstance(final_output, dict):
        try:
            parsed = expected_type.model_validate(final_output)
            val = getattr(parsed, "answer", None)
        except Exception as exc:
            raise GenerationError(
                "Invalid structured output dictionary from OpenAI agent"
            ) from exc
    elif isinstance(final_output, str):
        try:
            parsed = expected_type.model_validate_json(final_output)
            val = getattr(parsed, "answer", None)
        except Exception as exc:
            raise GenerationError(
                "Invalid structured output JSON string from OpenAI agent"
            ) from exc
    else:
        raise GenerationError(
            "Invalid or missing structured final_output from OpenAI agent"
        )

    if not val or not str(val).strip():
        raise GenerationError("OpenAI generation returned empty structured content")

    return str(val).strip()


class CallLog(RunHooks):
    """Ghi một mục cho **mỗi** lần gọi model của một lượt `Runner.run` / `Runner.run_streamed` (B123 §1: SDK gọi `on_llm_end` sau mỗi lần
    gọi, kể cả khi stream; `response.usage` là của riêng lần đó). Mỗi lượt một đối tượng mới — bộ đánh giá chạy song song.
    Một `_started` đủ vì một agent gọi model tuần tự. Hook không đổi thân yêu cầu gửi model (plan B0 T-2 kiểm bằng máy)."""

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self._started: float | None = None

    async def on_llm_start(self, context, agent, system_prompt, input_items) -> None:
        self._started = time.monotonic()

    async def on_llm_end(self, context, agent, response) -> None:
        ms = None if self._started is None else round((time.monotonic() - self._started) * 1000, 1)
        self.calls.append(call_entry(response, ms))


def call_entry(response: Any, ms: float | None) -> dict:
    """Một mục log từ `ModelResponse` của một lần gọi: loại đầu ra, ms, USD giá đủ (`llm.pricing.cost_usd`), token."""
    usage = response.usage
    cached, cache_write = input_cache_tokens(usage)
    reasoning = getattr(getattr(usage, "output_tokens_details", None), "reasoning_tokens", None)
    return {
        "kind": [getattr(item, "type", None) for item in response.output],
        "ms": ms,
        "usd": cost_usd(usage.input_tokens, usage.output_tokens, cache_write or 0, cached or 0),
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "reasoning_tokens": reasoning,
        "cached_tokens": cached,
        "cache_write_tokens": cache_write,
    }


def with_history(user_prompt: str, history) -> "str | list[dict]":
    """Đầu vào một lần chạy (B3 D3): lịch sử rỗng ⇒ đúng chuỗi như B2 (chuỗi gửi model không đổi — Q1); có lịch sử ⇒ danh sách tin
    user / assistant theo thứ tự rồi tin user lượt này. Câu trả lời rỗng (chỉ nhớ câu hỏi) ⇒ bỏ tin assistant đó."""
    if not history:
        return user_prompt
    items: list[dict] = []
    for question, answer in history:
        items.append({"role": "user", "content": question})
        if answer:
            items.append({"role": "assistant", "content": answer})
    return items + [{"role": "user", "content": user_prompt}]


def _sum_or_none(values) -> int | None:
    """Cộng các số có mặt; không có số nào ⇒ None (giữ nghĩa "không có usage" như khi chỉ đọc một lần gọi)."""
    present = [v for v in values if v is not None]
    return sum(present) if present else None


def _run_config() -> RunConfig:
    # Cùng một cấu hình cho lần gọi thường và lần gọi stream: hai đường gọi model phải giống nhau (spec streaming §4.3 bước 1).
    return RunConfig(
        tracing_disabled=True,
        trace_include_sensitive_data=False,
    )


class OpenAIFullCorpusGenerator:
    """Tool-less full-corpus generator using OpenAI Agents SDK."""

    def __init__(
        self,
        *,
        client: AsyncOpenAI,
        model: str,
        timeout: int = 45,
        answer_max_output_tokens: int = 2048,
        answer_instructions: str = ANSWER_SYSTEM_INSTRUCTIONS,
        reasoning_effort: str | None = None,
        router_timeout: float = 10,
    ) -> None:
        # answer_instructions / reasoning_effort: chỉ để harness Phase 8.1 thử prompt và mức suy luận;
        # mặc định giữ đúng hành vi runtime (prompt hiện hành, không gửi reasoning; None hoặc "" = không gửi).
        self.client = client
        self.model = model
        self.timeout = timeout
        self.answer_max_output_tokens = answer_max_output_tokens
        self.router_timeout = router_timeout

        # Create one shared OpenAIResponsesModel with gpt-6-luna alias
        self.responses_model = OpenAIResponsesModel(
            model=self.model, openai_client=self.client
        )

        # Answer agent: max_tokens=2048, include_usage=True, store=False
        # No temperature, verbosity, top_p or sampling knobs; reasoning only when reasoning_effort is set
        self.answer_agent = Agent(
            name="hue_full_corpus_answer_generator",
            instructions=answer_instructions,
            model=self.responses_model,
            model_settings=ModelSettings(
                max_tokens=self.answer_max_output_tokens,
                include_usage=True,
                store=False,
                reasoning=Reasoning(effort=reasoning_effort) if reasoning_effort else None,
            ),
            output_type=AnswerOutput,
        )
        # Phase 9 B1: định tuyến (D3) — không công cụ, không stream, không lịch sử; trò chuyện (D4) — không ngữ cảnh kho, đầu ra {answer}.
        self.router_agent = Agent(
            name="hue_router",
            instructions=ROUTER_INSTRUCTIONS,
            model=self.responses_model,
            model_settings=ModelSettings(max_tokens=ROUTER_MAX_OUTPUT_TOKENS, include_usage=True, store=False),
            output_type=RouteOutput,
        )
        self.chat_agent = Agent(
            name="hue_chat",
            instructions=CHAT_INSTRUCTIONS,
            model=self.responses_model,
            model_settings=ModelSettings(max_tokens=self.answer_max_output_tokens, include_usage=True, store=False),
            output_type=AnswerOutput,
        )
        # Phase 9 B2 (plan D2): định tuyến viết câu tìm — cùng agent định tuyến B1, lời dặn thêm một đoạn, kiểu đầu ra theo biến.
        self.router_search_agents = {
            variant: self.router_agent.clone(instructions=f"{ROUTER_INSTRUCTIONS}\n\n{note}", output_type=output_type)
            for variant, (output_type, note) in ROUTER_OUTPUTS.items()
        }
        # B2 D5: trợ lý có công cụ — lời dặn trả lời + đoạn công cụ, cùng model setting, một công cụ mỗi lượt gọi.
        # Công cụ gắn mỗi lượt (`_assistant_for`): lõi đưa hàm của lượt đó (giữ trace / sổ nguồn riêng).
        self.assistant_instructions = f"{answer_instructions}\n\n{ASSISTANT_TOOL_NOTE}"
        self.assistant_agent = self.answer_agent.clone(
            name="hue_assistant",
            instructions=self.assistant_instructions,
            model_settings=dataclasses.replace(self.answer_agent.model_settings, parallel_tool_calls=False),
        )
        # B3 D3: bản agent cho lượt có lịch sử — thêm đúng một câu dặn; lượt không lịch sử dùng bản trên (chuỗi gửi model như B2).
        self.router_history_agent = self.router_agent.clone(instructions=f"{ROUTER_INSTRUCTIONS}\n\n{ROUTER_HISTORY_NOTE}")
        self.assistant_history_instructions = f"{self.assistant_instructions}\n\n{ASSISTANT_HISTORY_NOTE}"
        self.assistant_history_agent = self.assistant_agent.clone(instructions=self.assistant_history_instructions)
        # Cổng đợt 1 D3 (V5 — X1c): lượt biểu mẫu = agent trả lời + luật viết lịch trong lời dặn hệ thống + mức suy luận "low". Chỉ lượt biểu
        # mẫu dùng; mọi lượt khác gọi `answer_agent` như cũ (Q1). Luật vẫn nằm cả trong khung ngữ cảnh — giữ đúng cấu hình C đã đo.
        self.bieu_mau_agent = self.answer_agent.clone(
            instructions=f"{answer_instructions}\n\n{LICH_TRINH_LUAT}",
            model_settings=dataclasses.replace(self.answer_agent.model_settings, reasoning=Reasoning(effort=BIEU_MAU_REASONING)),
        )
        # B6 D4: lần gọi riêng viết mục "Từ web" — không công cụ, không lịch sử, không kho; đầu ra {answer} như trả lời kho.
        self.web_agent = Agent(
            name="hue_web_section",
            instructions=TU_WEB_LUAT,
            model=self.responses_model,
            model_settings=ModelSettings(max_tokens=WEB_MAX_OUTPUT_TOKENS, include_usage=True, store=False),
            output_type=AnswerOutput,
        )

    @classmethod
    def from_environment(
        cls,
        settings: dict[str, Any],
        *,
        answer_instructions: str = ANSWER_SYSTEM_INSTRUCTIONS,
        reasoning_effort: str | None = None,
    ) -> "OpenAIFullCorpusGenerator":
        """Instantiate generator from settings and process environment fail-closed."""
        config = settings.get("full_corpus_generation", {})
        api_key_env = config.get("api_key_env", "OPENAI_API_KEY")
        api_key = os.getenv(api_key_env, "").strip()
        if not api_key:
            raise GenerationError(f"{api_key_env} is missing from environment")

        model = config.get("model", "gpt-6-luna")
        timeout = config.get("timeout_seconds", 45)
        answer_max = config.get("answer_max_output_tokens", 2048)

        client = AsyncOpenAI(
            api_key=api_key,
            timeout=timeout,
            max_retries=0,
        )
        return cls(
            client=client,
            model=model,
            timeout=timeout,
            answer_max_output_tokens=answer_max,
            answer_instructions=answer_instructions,
            reasoning_effort=reasoning_effort,
            router_timeout=settings.get("assistant", {}).get("router_timeout_seconds", 10),
        )

    async def _run(self, agent: Agent, user_prompt: "str | list[dict]", call_log: "CallLog", timeout: float, *, max_turns: int = 1,
                   error_handlers: dict | None = None):
        """Một `Runner.run` không stream; lỗi ⇒ `GenerationError`. `call_log` do nơi gọi tạo ⇒ lần gọi đã xong vẫn còn mục khi lượt lỗi sau phản hồi
        (review C128 m-1). `max_turns` / `error_handlers` chỉ đường trợ lý có công cụ đổi (B2 D5); mặc định = một lần gọi như B1."""
        extra = {} if error_handlers is None else {"error_handlers": error_handlers}
        try:
            return await asyncio.wait_for(
                Runner.run(
                    agent,
                    input=user_prompt,
                    max_turns=max_turns,
                    run_config=_run_config(),
                    hooks=call_log,
                    **extra,
                ),
                timeout=timeout,
            )
        except asyncio.TimeoutError as exc:
            raise GenerationError(f"OpenAI generation timed out after {timeout}s") from exc
        except (AgentsException, OpenAIError) as exc:
            raise GenerationError("OpenAI generation failed") from exc
        except Exception as exc:
            raise GenerationError("OpenAI generation encountered unexpected failure") from exc

    def assistant_instructions_for(self, history) -> str:
        """Lời dặn trợ lý thật sự gửi đi ở lượt này — bộ dựng ngữ cảnh đếm ngân sách bằng chính chuỗi này (B3 D5). B5: công cụ `lich_trinh`
        **không** thêm lời dặn (plan B5 bản 7 D7)."""
        return self.assistant_history_instructions if history else self.assistant_instructions

    async def route(self, query: str, call_log: "CallLog", history=()) -> str:
        """Định tuyến (B1 D3): tuyến model chọn. Lỗi / hết giờ (`router_timeout`) / đầu ra hỏng ⇒ `GenerationError` (lõi đổi thành `tro_ly_hue`)."""
        agent = self.router_history_agent if history else self.router_agent
        result = await self._run(agent, with_history(query.strip(), history), call_log, self.router_timeout)
        output = getattr(result, "final_output", None)
        try:
            return (output if isinstance(output, RouteOutput) else RouteOutput.model_validate(output)).route
        except Exception as exc:
            raise GenerationError("Invalid router output") from exc

    async def route_search(self, query: str, call_log: "CallLog", variant: str) -> tuple[str, list[str]]:
        """B2 V1 / V3 (plan D2): một lần gọi định tuyến trả tuyến + câu tìm (V1 một câu, V3 1–3 câu). Lỗi như `route` — kể cả V3 trả > 3 câu:
        SDK kiểm đầu ra theo schema (`maxItems` 3) và báo lỗi trước khi tới đây ⇒ lõi đi `tro_ly_hue` bằng câu gốc."""
        output_type = ROUTER_OUTPUTS[variant][0]
        result = await self._run(self.router_search_agents[variant], query.strip(), call_log, self.router_timeout)
        output = getattr(result, "final_output", None)
        try:
            parsed = output if isinstance(output, output_type) else output_type.model_validate(output)
        except Exception as exc:
            raise GenerationError("Invalid router output") from exc
        queries = [parsed.cau_tim] if isinstance(parsed.cau_tim, str) else list(parsed.cau_tim)
        return parsed.route, queries

    def _assistant_for(self, tool_fn, *, stop_on_first_tool: bool = False, history=(), lich_trinh_fn=None, thoi_tiet_fn=None, ngay_lich_fn=None) -> tuple[Agent, dict, dict]:
        """Agent trợ lý của **một lượt**: công cụ `tim_kho` bọc từ hàm của lõi (closure giữ trace / sổ nguồn của lượt — T-3: lõi không import SDK),
        handler `max_turns` + cờ dựng mới mỗi lượt (review C135 m-6: nhiều câu chạy cùng lúc không lẫn cờ). Lỗi trong công cụ đi thẳng ra
        (`failure_error_function=None`), không thành chữ cho model."""
        state = {"hit_max_turns": False}

        def on_max_turns(_input) -> AnswerOutput:
            state["hit_max_turns"] = True
            return AnswerOutput(answer=INSUFFICIENT_ANSWER)

        tools = [function_tool(tool_fn, name_override="tim_kho", failure_error_function=None)]
        extra = {"tool_use_behavior": "stop_on_first_tool"} if stop_on_first_tool else {}
        base = self.assistant_history_agent if history else self.assistant_agent
        if lich_trinh_fn is not None:  # B5 D1: công cụ thứ hai; mô tả ngắn, không đổi lời dặn (D7); dừng lượt chỉ khi code trả thẻ hỏi lại (D15)
            tools.append(function_tool(lich_trinh_fn, name_override="lich_trinh", description_override=LICH_TRINH_MO_TA, failure_error_function=None))
            extra = {**extra, "tool_use_behavior": _dung_khi_hoi_lai}
        if thoi_tiet_fn is not None:  # B5b D4: chỉ khi code thấy từ khoá thời tiết (lượt khác ⇒ danh sách công cụ như trước)
            tools.append(function_tool(thoi_tiet_fn, name_override="thoi_tiet", description_override=THOI_TIET_MO_TA, failure_error_function=None))
        if ngay_lich_fn is not None:  # Phase 9 T1: chỉ khi code thấy từ chỉ ngày (lượt khác ⇒ danh sách công cụ như trước)
            tools.append(function_tool(ngay_lich_fn, name_override="ngay_lich", description_override=NGAY_LICH_MO_TA, failure_error_function=None))
        return base.clone(tools=tools, **extra), {"max_turns": on_max_turns}, state

    async def generate_with_tools(self, user_prompt: str, tool_fn, call_log: "CallLog | None" = None, history=(), lich_trinh_fn=None,
                                  thoi_tiet_fn=None, ngay_lich_fn=None) -> GeneratedText:
        """B2 D5 không stream: trợ lý tự gọi `tim_kho` (≤ `ASSISTANT_MAX_TURNS` lượt). Chạm trần ⇒ câu từ chối + `hit_max_turns`."""
        started = time.monotonic()
        call_log = call_log if call_log is not None else CallLog()
        agent, handlers, state = self._assistant_for(tool_fn, history=history, lich_trinh_fn=lich_trinh_fn, thoi_tiet_fn=thoi_tiet_fn, ngay_lich_fn=ngay_lich_fn)
        result = await self._run(agent, with_history(user_prompt, history), call_log, self.timeout, max_turns=ASSISTANT_MAX_TURNS,
                                 error_handlers=handlers)
        return self._tools_result(result, started, call_log, state)

    def _tools_result(self, result, started: float, call_log: "CallLog", state: dict) -> GeneratedText:
        """Kết quả lượt trợ lý có công cụ. Dừng ở thẻ hỏi lại (B5 D15, đường B4 D8) ⇒ `final_output` là dict công cụ trả ⇒ đọc **trước** khi ép
        `AnswerOutput`."""
        output = getattr(result, "final_output", None)
        if isinstance(output, dict) and "loai" in output:
            return dataclasses.replace(self._generated_text(result, "", started, call_log), clarify=output)
        text = parse_structured_output(output, AnswerOutput)
        return dataclasses.replace(self._generated_text(result, text, started, call_log), hit_max_turns=state["hit_max_turns"])

    def start_tools_stream(self, user_prompt: str, tool_fn, history=(), lich_trinh_fn=None, thoi_tiet_fn=None, ngay_lich_fn=None) -> tuple[RunResultStreaming, "CallLog", dict]:
        """Như `generate_with_tools` nhưng stream; trả kèm `state` của lượt (cờ `hit_max_turns`) cho `finish_answer_stream`."""
        call_log = CallLog()
        agent, handlers, state = self._assistant_for(tool_fn, history=history, lich_trinh_fn=lich_trinh_fn, thoi_tiet_fn=thoi_tiet_fn, ngay_lich_fn=ngay_lich_fn)
        result = Runner.run_streamed(agent, input=with_history(user_prompt, history), max_turns=ASSISTANT_MAX_TURNS, run_config=_run_config(), hooks=call_log,
                                     error_handlers=handlers)
        return result, call_log, state

    async def first_tool_search(self, user_prompt: str, tool_fn, call_log: "CallLog") -> None:
        """Harness tầng tìm V2 (plan D6): trợ lý chạy tới lần gọi `tim_kho` đầu rồi dừng (`stop_on_first_tool`), không viết câu trả lời.
        Kết quả tìm nằm ở trace mà công cụ ghi; model không gọi ⇒ trace không có lần tìm nào."""
        agent, handlers, _ = self._assistant_for(tool_fn, stop_on_first_tool=True)
        await self._run(agent, user_prompt, call_log, self.timeout, max_turns=ASSISTANT_MAX_TURNS, error_handlers=handlers)

    async def generate_chat(self, query: str, call_log: "CallLog | None" = None, history=()) -> GeneratedText:
        """Trò chuyện (B1 D4): lời dặn riêng, không ngữ cảnh kho."""
        return await self._execute_agent(self.chat_agent, with_history(query.strip(), history), AnswerOutput, call_log)

    async def generate_web_section(self, user_prompt: str, call_log: "CallLog | None" = None) -> GeneratedText:
        """B6 D4: mục "Từ web" từ câu hỏi + đoạn trích (`tra_web.dau_vao_model`). Một lần gọi, không lịch sử; lỗi ⇒ `GenerationError`."""
        return await self._execute_agent(self.web_agent, user_prompt, AnswerOutput, call_log)

    def start_chat_stream(self, query: str, history=()) -> tuple[RunResultStreaming, "CallLog"]:
        return self._start_stream(self.chat_agent, with_history(query.strip(), history))

    async def _execute_agent(
        self, agent: Agent, user_prompt: "str | list[dict]", expected_type: type[BaseModel], call_log: "CallLog | None" = None
    ) -> GeneratedText:
        started = time.monotonic()
        call_log = call_log if call_log is not None else CallLog()
        result = await self._run(agent, user_prompt, call_log, self.timeout)

        # Extract structured output strictly - fail closed
        final_output = getattr(result, "final_output", None)
        text = parse_structured_output(final_output, expected_type)
        return self._generated_text(result, text, started, call_log)

    def _generated_text(self, result: Any, text: str, started: float, call_log: CallLog) -> GeneratedText:
        """Usage + metadata của một lượt đã xong (`Runner.run` hoặc `Runner.run_streamed` đọc hết) ⇒ `GeneratedText`."""
        # Extract usage and response metadata
        response_id = None
        input_tokens = None
        output_tokens = None
        total_tokens = None
        reasoning_tokens = None
        cached_tokens = cache_write_tokens = None
        finish_reason = None
        if hasattr(result, "raw_responses") and result.raw_responses:
            last_resp = result.raw_responses[-1]
            response_id = getattr(last_resp, "response_id", None)
            # B2 D10: token = tổng mọi lần gọi của lượt (vòng công cụ nhiều lần gọi); một lần gọi ⇒ đúng số như trước. Từng lần: `llm_calls`.
            usages = [u for u in (getattr(r, "usage", None) for r in result.raw_responses) if u]
            if usages:
                input_tokens = _sum_or_none(getattr(u, "input_tokens", None) for u in usages)
                output_tokens = _sum_or_none(getattr(u, "output_tokens", None) for u in usages)
                total_tokens = _sum_or_none(getattr(u, "total_tokens", None) for u in usages)
                reasoning_tokens = _sum_or_none(getattr(getattr(u, "output_tokens_details", None), "reasoning_tokens", None) for u in usages)
                caches = [input_cache_tokens(u) for u in usages]
                cached_tokens = _sum_or_none(c[0] for c in caches)
                cache_write_tokens = _sum_or_none(c[1] for c in caches)
            choices = getattr(last_resp, "choices", None)
            if choices and len(choices) > 0:
                finish_reason = getattr(choices[0], "finish_reason", None)
        if not response_id:
            response_id = getattr(result, "last_response_id", None)

        latency_ms = round((time.monotonic() - started) * 1000)

        return GeneratedText(
            text=text,
            response_id=response_id,
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
            finish_reason=finish_reason,
            reasoning_tokens=reasoning_tokens,
            cached_tokens=cached_tokens,
            cache_write_tokens=cache_write_tokens,
            llm_calls=tuple(call_log.calls),
        )

    async def generate_answer(self, query: str, context: str, today: str | None = None, call_log: "CallLog | None" = None,
                              history=(), bieu_mau: bool = False) -> GeneratedText:
        """`bieu_mau`: lượt biểu mẫu (cổng D3) ⇒ `bieu_mau_agent`; mặc định = `answer_agent` như cũ."""
        if not query or not query.strip():
            raise ValueError("Query must not be empty or blank")
        return await self._execute_agent(self.bieu_mau_agent if bieu_mau else self.answer_agent, with_history(build_answer_input(query, context, today), history), AnswerOutput,
                                         call_log)

    def _start_stream(self, agent: Agent, user_prompt: "str | list[dict]") -> tuple[RunResultStreaming, "CallLog"]:
        call_log = CallLog()
        result = Runner.run_streamed(agent, input=user_prompt, max_turns=1, run_config=_run_config(), hooks=call_log)
        return result, call_log

    def start_answer_stream(self, query: str, context: str, today: str | None = None, history=(),
                            bieu_mau: bool = False) -> tuple[RunResultStreaming, CallLog]:
        """Cùng agent + cùng tham số lần gọi như `generate_answer`, nhưng stream (spec streaming §4.3 bước 1). Trả ngay; model chạy
        trong lúc nơi gọi đọc `result.stream_events()` — nơi gọi tự đặt hạn giờ `self.timeout` cho cả vòng đọc và tự `cancel()`.
        `CallLog` của lượt trả kèm: nơi gọi đọc `calls` cả khi lượt bị ngắt / lỗi (chỉ có mục của lần gọi đã xong)."""
        if not query or not query.strip():
            raise ValueError("Query must not be empty or blank")
        return self._start_stream(self.bieu_mau_agent if bieu_mau else self.answer_agent,
                                  with_history(build_answer_input(query, context, today), history))

    def finish_answer_stream(self, result: RunResultStreaming, call_log: CallLog, started: float, state: dict | None = None) -> GeneratedText:
        """Sau khi `stream_events()` đã đọc hết: chữ cuối kiểm chặt như `generate_answer` (`parse_structured_output`) + usage.
        `started` lấy bằng `time.monotonic()` trước `start_answer_stream`. `state`: của `start_tools_stream` (cờ `hit_max_turns`)."""
        if state is not None:  # lượt có công cụ (có thể dừng ở thẻ hỏi lại — B5 D15)
            return self._tools_result(result, started, call_log, state)
        text = parse_structured_output(getattr(result, "final_output", None), AnswerOutput)
        return self._generated_text(result, text, started, call_log)

    async def aclose(self) -> None:
        """Close AsyncOpenAI client connection."""
        await self.client.close()
