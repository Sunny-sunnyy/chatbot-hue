"""Giá `gpt-6-luna` và tiền một lần gọi — một chỗ cho log của chatbot (`chat_metrics`) và bộ đánh giá (dời từ `evaluation/full_corpus_eval.py`,
plan Phase 9 B0 D5: lõi `llm/` không import `evaluation/`)."""

# Giá gpt-6-luna (User 2026-10-30, ngữ cảnh < 272k token), USD cho 1M token. Phần vào chia ba: đọc lại từ đệm, ghi vào đệm (đệm 30 phút),
# còn lại giá thường. B95 (30/10): mỗi lần gọi ghi đệm gần hết phần vào, đọc đệm 0 ⇒ giá phẳng cũ ghi thiếu ~20 % / câu.
PRICE_INPUT_PER_M = 0.1
PRICE_CACHED_INPUT_PER_M = 0.01
PRICE_CACHE_WRITE_PER_M = 0.125
PRICE_OUTPUT_PER_M = 0.5


def cost_usd(input_tokens: int, output_tokens: int, cache_write_tokens: int = 0, cached_tokens: int = 0) -> float:
    """`input_tokens` đã gồm phần ghi đệm / đọc đệm (cách OpenAI đếm). Không truyền phần đệm (dòng cũ chưa ghi) ⇒ giá phẳng như trước."""
    regular_input = input_tokens - cache_write_tokens - cached_tokens
    return (regular_input * PRICE_INPUT_PER_M + cache_write_tokens * PRICE_CACHE_WRITE_PER_M
            + cached_tokens * PRICE_CACHED_INPUT_PER_M + output_tokens * PRICE_OUTPUT_PER_M) / 1_000_000
