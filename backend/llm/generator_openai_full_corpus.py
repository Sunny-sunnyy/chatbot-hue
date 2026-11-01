"""Tool-less OpenAI Agents SDK full-corpus answer generator for Phase 6."""
import asyncio
from dataclasses import dataclass
import logging
import os
import time
from typing import Any

from agents import (
    Agent,
    ModelSettings,
    OpenAIResponsesModel,
    RunConfig,
    RunResultStreaming,
    Runner,
)
from agents.exceptions import AgentsException
from openai import AsyncOpenAI, OpenAIError
from openai.types.shared import Reasoning
from pydantic import BaseModel, ConfigDict, ValidationError

from core.schema import GenerationError
from llm.full_corpus_prompt import (
    ANSWER_SYSTEM_INSTRUCTIONS,
    build_answer_input,
)

logger = logging.getLogger("llm.full_corpus")


class AnswerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answer: str


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
    ) -> None:
        # answer_instructions / reasoning_effort: chỉ để harness Phase 8.1 thử prompt và mức suy luận;
        # mặc định giữ đúng hành vi runtime (prompt hiện hành, không gửi reasoning; None hoặc "" = không gửi).
        self.client = client
        self.model = model
        self.timeout = timeout
        self.answer_max_output_tokens = answer_max_output_tokens

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
        )

    async def _execute_agent(
        self, agent: Agent, user_prompt: str, expected_type: type[BaseModel]
    ) -> GeneratedText:
        started = time.monotonic()
        try:
            result = await asyncio.wait_for(
                Runner.run(
                    agent,
                    input=user_prompt,
                    max_turns=1,
                    run_config=_run_config(),
                ),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError as exc:
            raise GenerationError(
                f"OpenAI generation timed out after {self.timeout}s"
            ) from exc
        except (AgentsException, OpenAIError) as exc:
            raise GenerationError("OpenAI generation failed") from exc
        except Exception as exc:
            raise GenerationError("OpenAI generation encountered unexpected failure") from exc

        # Extract structured output strictly - fail closed
        final_output = getattr(result, "final_output", None)
        text = parse_structured_output(final_output, expected_type)
        return self._generated_text(result, text, started)

    def _generated_text(self, result: Any, text: str, started: float) -> GeneratedText:
        """Usage + metadata của một lượt đã xong (`Runner.run` hoặc `Runner.run_streamed` đọc hết) ⇒ `GeneratedText`."""
        # Extract usage and response metadata
        response_id = None
        input_tokens = None
        output_tokens = None
        total_tokens = None
        reasoning_tokens = None
        finish_reason = None
        if hasattr(result, "raw_responses") and result.raw_responses:
            last_resp = result.raw_responses[-1]
            response_id = getattr(last_resp, "response_id", None)
            usage = getattr(last_resp, "usage", None)
            if usage:
                input_tokens = getattr(usage, "input_tokens", None)
                output_tokens = getattr(usage, "output_tokens", None)
                total_tokens = getattr(usage, "total_tokens", None)
                reasoning_tokens = getattr(getattr(usage, "output_tokens_details", None), "reasoning_tokens", None)
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
        )

    async def generate_answer(self, query: str, context: str) -> GeneratedText:
        if not query or not query.strip():
            raise ValueError("Query must not be empty or blank")
        return await self._execute_agent(self.answer_agent, build_answer_input(query, context), AnswerOutput)

    def start_answer_stream(self, query: str, context: str) -> RunResultStreaming:
        """Cùng agent + cùng tham số lần gọi như `generate_answer`, nhưng stream (spec streaming §4.3 bước 1). Trả ngay; model chạy
        trong lúc nơi gọi đọc `result.stream_events()` — nơi gọi tự đặt hạn giờ `self.timeout` cho cả vòng đọc và tự `cancel()`."""
        if not query or not query.strip():
            raise ValueError("Query must not be empty or blank")
        return Runner.run_streamed(
            self.answer_agent,
            input=build_answer_input(query, context),
            max_turns=1,
            run_config=_run_config(),
        )

    def finish_answer_stream(self, result: RunResultStreaming, started: float) -> GeneratedText:
        """Sau khi `stream_events()` đã đọc hết: chữ cuối kiểm chặt như `generate_answer` (`parse_structured_output`) + usage.
        `started` lấy bằng `time.monotonic()` trước `start_answer_stream`."""
        text = parse_structured_output(getattr(result, "final_output", None), AnswerOutput)
        return self._generated_text(result, text, started)

    async def aclose(self) -> None:
        """Close AsyncOpenAI client connection."""
        await self.client.close()
