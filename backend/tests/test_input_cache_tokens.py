"""`input_cache_tokens` đọc phần đệm từ đúng hai kiểu usage mà code gọi: `agents.usage.Usage` (generator, judge) và
`openai.types.responses.ResponseUsage` (rerank luna). Dựng bằng chính lớp của thư viện — không phải bằng chứng provider trả trường này
(lần gọi thật ở report B108)."""
from agents.usage import Usage
from openai.types.responses import ResponseUsage

from llm.generator_openai_full_corpus import input_cache_tokens


def test_reads_cache_fields_from_agents_usage():
    usage = Usage(requests=1, input_tokens=1916, output_tokens=85, total_tokens=2001,
                  input_tokens_details={"cached_tokens": 0, "cache_write_tokens": 1913})
    assert input_cache_tokens(usage) == (0, 1913)


def test_reads_cache_fields_from_openai_response_usage():
    usage = ResponseUsage(input_tokens=1916, output_tokens=85, total_tokens=2001,
                          input_tokens_details={"cached_tokens": 7, "cache_write_tokens": 1900},
                          output_tokens_details={"reasoning_tokens": 0})
    assert input_cache_tokens(usage) == (7, 1900)


def test_usage_without_details_gives_none():
    assert input_cache_tokens(object()) == (None, None)
