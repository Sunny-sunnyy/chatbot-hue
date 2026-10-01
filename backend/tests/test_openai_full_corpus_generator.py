import asyncio
import pytest

from core.settings_loader import load_settings
from core.schema import GenerationError
from llm.generator_openai_full_corpus import (
    AnswerOutput,
    GeneratedText,
    OpenAIFullCorpusGenerator,
    SearchContextOutput,
)
from llm.representation_b import build_representation_b_search_text


def test_structured_outputs_have_one_field():
    assert AnswerOutput(answer="Câu trả lời [1].").model_dump() == {
        "answer": "Câu trả lời [1]."
    }
    assert SearchContextOutput(search_context="Ngữ cảnh Huế.").model_dump() == {
        "search_context": "Ngữ cảnh Huế."
    }


def test_real_environment_builds_openai_generator(require_openai_key):
    generator = OpenAIFullCorpusGenerator.from_environment(load_settings())
    assert generator.model == "gpt-5.4-nano"
    assert generator.timeout == 45
    assert generator.client.max_retries == 0

    # Verify absence of reasoning/temperature/sampling knobs
    for agent, expected_max in [
        (generator.answer_agent, 2048),
        (generator.search_context_agent, 256),
    ]:
        assert agent.model_settings.max_tokens == expected_max
        assert agent.model_settings.include_usage is True
        assert agent.model_settings.store is False
        assert agent.model_settings.temperature is None
        assert agent.model_settings.top_p is None
        assert agent.model_settings.reasoning is None
        assert agent.model_settings.verbosity is None

    asyncio.run(generator.aclose())


def test_empty_or_blank_input_rejected_before_network(require_openai_key):
    generator = OpenAIFullCorpusGenerator.from_environment(load_settings())
    with pytest.raises((ValueError, GenerationError)):
        asyncio.run(generator.generate_answer("", "Ngữ cảnh"))
    with pytest.raises((ValueError, GenerationError)):
        asyncio.run(generator.generate_answer("   ", "Ngữ cảnh"))
    with pytest.raises((ValueError, GenerationError)):
        asyncio.run(generator.generate_search_context(""))
    with pytest.raises((ValueError, GenerationError)):
        asyncio.run(generator.generate_search_context("   "))
    asyncio.run(generator.aclose())


def test_representation_b_keeps_a_when_combined_text_is_too_long():
    result = build_representation_b_search_text(
        "Representation A thật.",
        "Ngữ cảnh tìm kiếm bổ sung.",
        fits_all_embedding_tokenizers=lambda text: False,
    )
    assert result.search_text == "Representation A thật."
    assert result.used_representation_b is False
    assert result.reason == "combined_text_exceeds_embedding_limit"


def test_representation_b_uses_combined_when_fits():
    result = build_representation_b_search_text(
        "Representation A thật.",
        "Ngữ cảnh tìm kiếm bổ sung.",
        fits_all_embedding_tokenizers=lambda text: True,
    )
    assert (
        result.search_text
        == "Representation A thật.\n\n[Ngữ cảnh tìm kiếm bổ sung]\nNgữ cảnh tìm kiếm bổ sung."
    )
    assert result.used_representation_b is True
    assert result.reason == "representation_b_used"


def test_structured_output_rejects_extra_fields():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        AnswerOutput.model_validate({"answer": "OK", "extra_field": "disallowed"})
    with pytest.raises(ValidationError):
        SearchContextOutput.model_validate({"search_context": "OK", "extra": 1})


def test_parse_structured_output_accepts_valid():
    from llm.generator_openai_full_corpus import parse_structured_output

    # 1. Pydantic model instance
    assert parse_structured_output(AnswerOutput(answer="Câu trả lời."), AnswerOutput) == "Câu trả lời."
    assert parse_structured_output(SearchContextOutput(search_context="Ngữ cảnh."), SearchContextOutput) == "Ngữ cảnh."

    # 2. Dictionary
    assert parse_structured_output({"answer": "Câu trả lời."}, AnswerOutput) == "Câu trả lời."
    assert parse_structured_output({"search_context": "Ngữ cảnh."}, SearchContextOutput) == "Ngữ cảnh."

    # 3. JSON string
    assert parse_structured_output('{"answer": "Câu trả lời."}', AnswerOutput) == "Câu trả lời."
    assert parse_structured_output('{"search_context": "Ngữ cảnh."}', SearchContextOutput) == "Ngữ cảnh."


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
