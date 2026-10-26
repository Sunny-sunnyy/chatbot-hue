import asyncio
import pytest

from core.settings_loader import load_settings
from core.schema import GenerationError
from llm.generator_openai_full_corpus import (
    AnswerOutput,
    GeneratedText,
    OpenAIFullCorpusGenerator,
)
from llm.full_corpus_prompt import build_answer_messages


def test_structured_outputs_have_one_field():
    assert AnswerOutput(answer="Câu trả lời [1].").model_dump() == {
        "answer": "Câu trả lời [1]."
    }


def test_real_environment_builds_openai_generator(require_openai_key):
    generator = OpenAIFullCorpusGenerator.from_environment(load_settings())
    assert generator.model == "gpt-6-luna"
    assert generator.timeout == 45
    assert generator.client.max_retries == 0

    # Verify absence of reasoning/temperature/sampling knobs
    model_settings = generator.answer_agent.model_settings
    assert model_settings.max_tokens == 2048
    assert model_settings.include_usage is True
    assert model_settings.store is False
    assert model_settings.temperature is None
    assert model_settings.top_p is None
    assert model_settings.reasoning is None
    assert model_settings.verbosity is None

    asyncio.run(generator.aclose())


def test_empty_or_blank_input_rejected_before_network(require_openai_key):
    generator = OpenAIFullCorpusGenerator.from_environment(load_settings())
    with pytest.raises((ValueError, GenerationError)):
        asyncio.run(generator.generate_answer("", "Ngữ cảnh"))
    with pytest.raises((ValueError, GenerationError)):
        asyncio.run(generator.generate_answer("   ", "Ngữ cảnh"))
    asyncio.run(generator.aclose())


def test_answer_call_sends_exactly_the_messages_counted_for_context(monkeypatch):
    """Chuỗi gửi model (instructions + input) phải đúng là chuỗi FullCorpusContextBuilder đếm token (C-03).
    Không gọi mạng: key giả chỉ để dựng client, bước gọi agent được thay bằng hàm ghi lại."""
    monkeypatch.setenv("OPENAI_API_KEY", "khong-dung-key-that")
    generator = OpenAIFullCorpusGenerator.from_environment(load_settings())
    sent = {}

    async def record(agent, user_prompt, expected_type):
        sent.update(instructions=agent.instructions, input=user_prompt)

    generator._execute_agent = record
    asyncio.run(generator.generate_answer("  Giá vé Đại Nội?  ", "[Nguồn 1]\nTiêu đề: Đại Nội\n"))
    asyncio.run(generator.aclose())
    system, user = build_answer_messages("  Giá vé Đại Nội?  ", "[Nguồn 1]\nTiêu đề: Đại Nội\n")
    assert sent == {"instructions": system["content"], "input": user["content"]}
    assert user["content"] == "Câu hỏi:\nGiá vé Đại Nội?\n\nNgữ cảnh truy xuất:\n[Nguồn 1]\nTiêu đề: Đại Nội"


def test_structured_output_rejects_extra_fields():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        AnswerOutput.model_validate({"answer": "OK", "extra_field": "disallowed"})


def test_parse_structured_output_accepts_valid():
    from llm.generator_openai_full_corpus import parse_structured_output

    # 1. Pydantic model instance
    assert parse_structured_output(AnswerOutput(answer="Câu trả lời."), AnswerOutput) == "Câu trả lời."

    # 2. Dictionary
    assert parse_structured_output({"answer": "Câu trả lời."}, AnswerOutput) == "Câu trả lời."

    # 3. JSON string
    assert parse_structured_output('{"answer": "Câu trả lời."}', AnswerOutput) == "Câu trả lời."


def test_parse_structured_output_rejects_malformed_and_extra_fields():
    from llm.generator_openai_full_corpus import parse_structured_output

    # 1. Extra fields in dict
    with pytest.raises(GenerationError, match="Invalid structured output dictionary"):
        parse_structured_output({"answer": "OK", "extra": 123}, AnswerOutput)

    # 2. Extra fields in JSON string
    with pytest.raises(GenerationError, match="Invalid structured output JSON string"):
        parse_structured_output('{"answer": "OK", "extra": 123}', AnswerOutput)

    # 3. Missing expected key in dict
    with pytest.raises(GenerationError, match="Invalid structured output dictionary"):
        parse_structured_output({"wrong_key": "OK"}, AnswerOutput)

    # 4. Invalid JSON syntax
    with pytest.raises(GenerationError, match="Invalid structured output JSON string"):
        parse_structured_output("{not valid json}", AnswerOutput)

    # 5. Empty or whitespace content
    with pytest.raises(GenerationError, match="empty structured content"):
        parse_structured_output(AnswerOutput(answer="   "), AnswerOutput)
    with pytest.raises(GenerationError, match="empty structured content"):
        parse_structured_output({"answer": ""}, AnswerOutput)
    with pytest.raises(GenerationError, match="empty structured content"):
        parse_structured_output('{"answer": "   "}', AnswerOutput)

    # 6. Non-dict, non-string, non-model types
    for invalid_val in (None, 123, [1, 2, 3], True):
        with pytest.raises(GenerationError, match="Invalid or missing structured final_output"):
            parse_structured_output(invalid_val, AnswerOutput)
