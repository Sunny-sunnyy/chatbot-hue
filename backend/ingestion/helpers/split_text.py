"""Split long text into paragraph-sized chunks."""
import re

DEFAULT_MAX_CHARS = 1500

_BLOCK_SEPARATOR = re.compile(r"\n\s*\n")


def split_text(text, max_chars=DEFAULT_MAX_CHARS):
    """Split text into blank-line separated blocks, packing greedily to max_chars.

    A block larger than max_chars stays whole so tables are never broken.
    """
    blocks = [block.strip() for block in _BLOCK_SEPARATOR.split(text) if block.strip()]
    chunks = []
    current = ""
    for block in blocks:
        if current and len(current) + 1 + len(block) > max_chars:
            chunks.append(current)
            current = block
        elif current:
            current = f"{current}\n{block}"
        else:
            current = block
    if current:
        chunks.append(current)
    return chunks
