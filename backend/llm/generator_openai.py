"""Tool-less OpenAI Agents SDK answer generator."""
import asyncio
import logging
import os
import time

from agents import Agent, ModelSettings, Runner, set_tracing_disabled
from agents.exceptions import AgentsException
from openai import OpenAIError
from pydantic import BaseModel

from core.schema import GenerationError
from llm.prompt import SYSTEM_INSTRUCTIONS, build_user_message

logger = logging.getLogger("llm")


class AnswerOutput(BaseModel):
    answer: str


class OpenAIAnswerGenerator:
    """Generate one grounded answer with one fixed tool-less Agent."""

    def __init__(
        self,
        *,
        model: str,
        api_key_env: str = "OPENAI_API_KEY",
        temperature: float = 0.2,
        max_output_tokens: int = 1024,
        timeout_seconds: float = 45.0,
    ):
        self._model = model
        self._timeout_seconds = timeout_seconds
        key = os.environ.get(api_key_env)
        self.configured = bool(key and key.strip())
        set_tracing_disabled(True)
        self._agent = Agent(
            name="hue_foods_answerer",
            instructions=SYSTEM_INSTRUCTIONS,
            model=model,
            model_settings=ModelSettings(
                temperature=temperature,
                max_tokens=max_output_tokens,
            ),
            output_type=AnswerOutput,
        )

    @property
    def model(self):
        return self._model

    async def generate_answer(self, query: str, context: str) -> str:
        if not self.configured:
            raise GenerationError("OpenAI generator is not configured")
        if not context.strip():
            raise GenerationError("context is empty")

        logger.info(f"Generating answer with model: {self._model}")
        started = time.monotonic()
        try:
            result = await asyncio.wait_for(
                Runner.run(self._agent, build_user_message(query, context)),
                timeout=self._timeout_seconds,
            )
        except asyncio.TimeoutError as error:
            raise GenerationError(
                f"Answer generation timed out after {self._timeout_seconds} seconds"
            ) from error
        except AgentsException as error:
            raise GenerationError(f"OpenAI agent execution failed: {error}") from error
        except OpenAIError as error:
            raise GenerationError(f"OpenAI answer generation failed: {error}") from error

        output = result.final_output
        if not isinstance(output, AnswerOutput):
            raise GenerationError("Model returned an unexpected output type")
        answer = output.answer.strip()
        if not answer:
            raise GenerationError("Model returned an empty answer")

        latency_ms = round((time.monotonic() - started) * 1000)
        logger.info(
            f"Generated answer successfully in {latency_ms} ms; "
            f"tokens={_usage_tokens(result)}"
        )
        return answer


def _usage_tokens(result):
    for response in getattr(result, "raw_responses", None) or []:
        usage = getattr(response, "usage", None)
        if usage is None:
            continue
        input_tokens = getattr(usage, "input_tokens", None)
        output_tokens = getattr(usage, "output_tokens", None)
        if input_tokens is not None and output_tokens is not None:
            return f"{input_tokens}/{output_tokens}"
    return "unknown"
