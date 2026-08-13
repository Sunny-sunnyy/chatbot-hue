"""Tool-less OpenAI Agents SDK answer generator running the real Runner."""
import asyncio
import logging
import os
import time

from agents import Agent, ModelSettings, Runner
from agents.exceptions import ModelBehaviorError
from pydantic import BaseModel

from core.schema import (
    GeneratorNotConfiguredError,
    GeneratorTimeoutError,
    GeneratorUnavailableError,
    InvalidGeneratorOutputError,
    InvalidQueryError,
)
from llm.prompt import SYSTEM_INSTRUCTIONS, build_user_message

logger = logging.getLogger("llm")


class GeneratedAnswer(BaseModel):
    """Structured output of the answer generator."""

    answer: str
    used_source_ids: list[str]


class OpenAIAnswerGenerator:
    """Grounded answer generator over one fixed tool-less Agent.

    Every call runs the real OpenAI Agents SDK Runner with a hard timeout;
    there is no injected runner path. The API key is read from the
    environment once at construction; a missing key marks the generator as
    not configured instead of raising at import time.
    """

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
        self._agent = Agent(
            name="hue_foods_answerer",
            instructions=SYSTEM_INSTRUCTIONS,
            model=model,
            model_settings=ModelSettings(
                temperature=temperature,
                # SDK 0.19 maps ModelSettings.max_tokens to the Responses
                # API max_output_tokens parameter.
                max_tokens=max_output_tokens,
            ),
            output_type=GeneratedAnswer,
        )

    @property
    def model(self):
        return self._model

    async def generate_answer(self, query, context, available_source_ids):
        """Generate a grounded answer; every failure raises a typed error."""
        if not self.configured:
            raise GeneratorNotConfiguredError("OpenAI generator is not configured")
        if not context.strip():
            raise InvalidQueryError("context must be a non-empty string")
        message = build_user_message(query, context, available_source_ids)
        started = time.monotonic()
        try:
            result = await asyncio.wait_for(
                Runner.run(self._agent, message),
                timeout=self._timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            raise GeneratorTimeoutError("answer generation timed out") from exc
        except ModelBehaviorError as exc:
            raise InvalidGeneratorOutputError(
                "model returned invalid structured output"
            ) from exc
        except Exception as exc:  # provider connection/API failures
            raise GeneratorUnavailableError("answer generation failed") from exc
        output = result.final_output
        if not isinstance(output, GeneratedAnswer):
            raise InvalidGeneratorOutputError("model returned an unexpected output type")
        if not output.answer or not output.answer.strip():
            raise InvalidGeneratorOutputError("model returned a blank answer")
        allowed = set(available_source_ids)
        unknown = [sid for sid in output.used_source_ids if sid not in allowed]
        if unknown:
            raise InvalidGeneratorOutputError("model referenced unknown source IDs")
        logger.info(
            "answer generated model=%s outcome=success latency_ms=%d "
            "source_count=%d tokens=%s",
            self._model,
            round((time.monotonic() - started) * 1000),
            len(output.used_source_ids),
            _usage_tokens(result),
        )
        return output


def _usage_tokens(result):
    """Return a compact token summary from the run result when available.

    Agents SDK 0.19.4 exposes usage on raw_responses entries, not on
    RunResult itself. Only an entry carrying both token counts is used;
    partial entries are skipped, and no complete entry yields "unknown".
    """
    for raw in getattr(result, "raw_responses", None) or []:
        usage = getattr(raw, "usage", None)
        if usage is None:
            continue
        tokens_in = getattr(usage, "input_tokens", None)
        tokens_out = getattr(usage, "output_tokens", None)
        if tokens_in is not None and tokens_out is not None:
            return f"{tokens_in}/{tokens_out}"
    return "unknown"
