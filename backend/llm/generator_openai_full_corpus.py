"""Tool-less OpenAI Agents SDK full-corpus answer and Representation B generator for Phase 6."""
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
    Runner,
)
from agents.exceptions import AgentsException
from openai import AsyncOpenAI, OpenAIError
from pydantic import BaseModel, ConfigDict, ValidationError

from core.schema import GenerationError
from llm.full_corpus_prompt import (
    ANSWER_SYSTEM_INSTRUCTIONS,
    REPRESENTATION_B_SYSTEM_INSTRUCTIONS,
)

logger = logging.getLogger("llm.full_corpus")


class AnswerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answer: str


class SearchContextOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    search_context: str


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


def parse_structured_output(
    final_output: Any, expected_type: type[BaseModel]
) -> str:
    """Strictly validate and extract text from structured agent output.

    Fails closed on missing fields, extra fields, invalid JSON, or non-conforming types.
    """
    if isinstance(final_output, expected_type):
        val = getattr(final_output, "answer", None) or getattr(
            final_output, "search_context", None
        )
    elif isinstance(final_output, dict):
        try:
            parsed = expected_type.model_validate(final_output)
            val = getattr(parsed, "answer", None) or getattr(
                parsed, "search_context", None
            )
        except Exception as exc:
            raise GenerationError(
                "Invalid structured output dictionary from OpenAI agent"
            ) from exc
    elif isinstance(final_output, str):
        try:
            parsed = expected_type.model_validate_json(final_output)
            val = getattr(parsed, "answer", None) or getattr(
                parsed, "search_context", None
            )
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


class OpenAIFullCorpusGenerator:
    """Tool-less full-corpus generator using OpenAI Agents SDK."""

    def __init__(
        self,
        *,
        client: AsyncOpenAI,
        model: str,
        timeout: int = 45,
        answer_max_output_tokens: int = 2048,
        representation_b_max_output_tokens: int = 256,
    ) -> None:
        self.client = client
        self.model = model
        self.timeout = timeout
        self.answer_max_output_tokens = answer_max_output_tokens
        self.representation_b_max_output_tokens = representation_b_max_output_tokens

        # Create one shared OpenAIResponsesModel with gpt-5.4-nano alias
        self.responses_model = OpenAIResponsesModel(
            model=self.model, openai_client=self.client
        )

        # Answer agent: max_tokens=2048, include_usage=True, store=False
        # No temperature, reasoning, verbosity, top_p or sampling knobs
        self.answer_agent = Agent(
            name="hue_full_corpus_answer_generator",
            instructions=ANSWER_SYSTEM_INSTRUCTIONS,
            model=self.responses_model,
            model_settings=ModelSettings(
                max_tokens=self.answer_max_output_tokens,
                include_usage=True,
                store=False,
            ),
            output_type=AnswerOutput,
        )

        # Search context agent: max_tokens=256, include_usage=True, store=False
        # No temperature, reasoning, verbosity, top_p or sampling knobs
        self.search_context_agent = Agent(
            name="hue_full_corpus_search_context_generator",
            instructions=REPRESENTATION_B_SYSTEM_INSTRUCTIONS,
            model=self.responses_model,
            model_settings=ModelSettings(
                max_tokens=self.representation_b_max_output_tokens,
                include_usage=True,
                store=False,
            ),
            output_type=SearchContextOutput,
        )

    @classmethod
    def from_environment(cls, settings: dict[str, Any]) -> "OpenAIFullCorpusGenerator":
        """Instantiate generator from settings and process environment fail-closed."""
        config = settings.get("full_corpus_generation", {})
        api_key_env = config.get("api_key_env", "OPENAI_API_KEY")
        api_key = os.getenv(api_key_env, "").strip()
        if not api_key:
            raise GenerationError(f"{api_key_env} is missing from environment")

        model = config.get("model", "gpt-5.4-nano")
        timeout = config.get("timeout_seconds", 45)
        answer_max = config.get("answer_max_output_tokens", 2048)
        rep_b_max = config.get("representation_b_max_output_tokens", 256)

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
            representation_b_max_output_tokens=rep_b_max,
        )

    async def _execute_agent(
        self, agent: Agent, user_prompt: str, expected_type: type[BaseModel]
    ) -> GeneratedText:
        started = time.monotonic()
        run_cfg = RunConfig(
            tracing_disabled=True,
            trace_include_sensitive_data=False,
        )
        try:
            result = await asyncio.wait_for(
                Runner.run(
                    agent,
                    input=user_prompt,
                    max_turns=1,
                    run_config=run_cfg,
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

        # Extract usage and response metadata
        response_id = None
        input_tokens = None
        output_tokens = None
        total_tokens = None
        finish_reason = None
        if hasattr(result, "raw_responses") and result.raw_responses:
            last_resp = result.raw_responses[-1]
            response_id = getattr(last_resp, "response_id", None)
            usage = getattr(last_resp, "usage", None)
            if usage:
                input_tokens = getattr(usage, "input_tokens", None)
                output_tokens = getattr(usage, "output_tokens", None)
                total_tokens = getattr(usage, "total_tokens", None)
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
        )

    async def generate_answer(self, query: str, context: str) -> GeneratedText:
        if not query or not query.strip():
            raise ValueError("Query must not be empty or blank")
        prompt = f"Câu hỏi:\n{query.strip()}\n\nNgữ cảnh truy xuất:\n{context.strip()}"
        return await self._execute_agent(self.answer_agent, prompt, AnswerOutput)

    async def generate_search_context(self, search_text: str) -> GeneratedText:
        if not search_text or not search_text.strip():
            raise ValueError("Search text must not be empty or blank")
        prompt = f"Representation A:\n{search_text.strip()}"
        return await self._execute_agent(
            self.search_context_agent, prompt, SearchContextOutput
        )

    async def aclose(self) -> None:
        """Close AsyncOpenAI client connection."""
        await self.client.close()
