"""OpenAI tiktoken tokenizer loader for Phase 6 full-corpus budget management."""
from functools import lru_cache
import tiktoken

OPENAI_GENERATION_MODEL: str = "gpt-5.4-nano"
OPENAI_TOKEN_ENCODING: str = "o200k_base"


@lru_cache(maxsize=1)
def load_openai_tokenizer() -> tiktoken.Encoding:
    """Return cached o200k_base tiktoken encoding for Phase 6 budget packing."""
    return tiktoken.get_encoding(OPENAI_TOKEN_ENCODING)
