"""Giá `gpt-6-luna` và tiền một lần gọi — một chỗ cho log của chatbot (`chat_metrics`) và bộ đánh giá (dời từ `evaluation/full_corpus_eval.py`,
plan Phase 9 B0 D5: lõi `llm/` không import `evaluation/`)."""

# Giá gpt-6-luna (User 2026-10-30, ngữ cảnh < 272k token), USD cho 1M token. Phần vào chia ba: đọc lại từ đệm, ghi vào đệm (đệm 30 phút),
# còn lại giá thường. B95 (30/10): mỗi lần gọi ghi đệm gần hết phần vào, đọc đệm 0 ⇒ giá phẳng cũ ghi thiếu ~20 % / câu.
PRICE_INPUT_PER_M = 0.1
PRICE_CACHED_INPUT_PER_M = 0.01
PRICE_CACHE_WRITE_PER_M = 0.125
PRICE_OUTPUT_PER_M = 0.5

# Theo `full_corpus_generation.provider`: (vào, đọc đệm, ghi đệm, ra), USD cho 1M token. `bedrock` = Claude Sonnet 5.5 trên Amazon Bedrock
# (đổi tạm 21/11/2026) — giá ghi sổ, CHƯA đối chiếu hoá đơn.
PRICES_PER_M = {
    "openai": (PRICE_INPUT_PER_M, PRICE_CACHED_INPUT_PER_M, PRICE_CACHE_WRITE_PER_M, PRICE_OUTPUT_PER_M),
    "bedrock": (2.0, 0.1, 2.5, 10.0),
}


def cost_usd(input_tokens: int, output_tokens: int, cache_write_tokens: int = 0, cached_tokens: int = 0, *, provider: str = "openai") -> float:
    """`input_tokens` đã gồm phần ghi đệm / đọc đệm (cách OpenAI đếm; lớp dịch Bedrock cộng lại cho cùng nghĩa). Không truyền phần đệm (dòng cũ
    chưa ghi) ⇒ giá phẳng như trước. `provider` mặc định = giá `gpt-6-luna` như trước."""
    price_input, price_cached, price_cache_write, price_output = PRICES_PER_M[provider]
    regular_input = input_tokens - cache_write_tokens - cached_tokens
    return (regular_input * price_input + cache_write_tokens * price_cache_write
            + cached_tokens * price_cached + output_tokens * price_output) / 1_000_000
