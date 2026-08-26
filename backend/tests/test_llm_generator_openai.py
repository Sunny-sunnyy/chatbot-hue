import asyncio
import logging

from llm.generator_openai import AnswerOutput, OpenAIAnswerGenerator
from llm.prompt import (
    INSUFFICIENT_ANSWER,
    SYSTEM_INSTRUCTIONS,
    build_user_message,
)
from retrieval.context_builder import ContextBuilder

MODEL = "gpt-5.4-nano"


def test_prompt_keeps_policy_in_system_instructions_and_data_in_runner_message():
    context = (
        "[Nguồn 1]\nTiêu đề: Bún bò Huế\nMục: Tóm tắt\n"
        "Nội dung:\nBún bò Huế có nước dùng từ xương."
    )
    message = build_user_message("Bún bò Huế là gì?", context)
    assert INSUFFICIENT_ANSWER in SYSTEM_INSTRUCTIONS
    assert "không đáng tin" in SYSTEM_INSTRUCTIONS
    assert "Câu hỏi của người dùng" in message
    assert context in message
    assert SYSTEM_INSTRUCTIONS not in message
    assert "chunk_id" not in message
    assert "used_source_ids" not in SYSTEM_INSTRUCTIONS


def test_answer_output_has_only_answer():
    output = AnswerOutput(answer="Bún bò Huế là một món ăn của Huế.")
    assert output.model_dump() == {
        "answer": "Bún bò Huế là một món ăn của Huế."
    }


def test_live_generator_returns_answer_string(
    require_openai_key,
    real_retrieved_docs,
    caplog,
):
    caplog.set_level(logging.INFO, logger="llm")
    context = ContextBuilder().build(real_retrieved_docs)
    generator = OpenAIAnswerGenerator(model=MODEL)
    answer = asyncio.run(
        generator.generate_answer(
            "Bún bò Huế có đặc điểm gì nổi bật?",
            context,
        )
    )
    assert isinstance(answer, str)
    assert answer.strip()
    messages = [record.getMessage() for record in caplog.records]
    assert any("Generating answer with model" in message for message in messages)
    assert any("Generated answer successfully" in message for message in messages)
