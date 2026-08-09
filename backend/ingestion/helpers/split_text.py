"""Split long text into content chunks with a character limit."""
import re

DEFAULT_MAX_CHARS = 400

_BLOCK_SEPARATOR = re.compile(r"\n\s*\n")
_TABLE_SEPARATOR = re.compile(r"^\s*\|?[\s|:.-]*\|\s*$")
_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
_SENTENCE_END = re.compile(r"[.!?]\s")


def split_text(text, max_chars=DEFAULT_MAX_CHARS):
    """Split markdown text into content chunks of at most max_chars.

    Paragraphs split at sentence ends, then at spaces, never inside a word.
    List blocks break between items, keeping wrapped lines with their item;
    an item is split internally only when it alone exceeds max_chars.
    Markdown tables are kept whole even when longer than max_chars.
    Chunks never overlap.
    """
    parts = []
    for block in _split_blocks(text):
        if _is_table(block):
            parts.append(block)
        elif _is_list(block):
            for item in _list_items(block):
                parts.extend(_split_long(item, max_chars))
        else:
            parts.extend(_split_long(block, max_chars))
    return _pack(parts, max_chars)


def _split_blocks(text):
    """Return non-empty blank-line separated blocks."""
    return [block.strip() for block in _BLOCK_SEPARATOR.split(text) if block.strip()]


def _is_table(block):
    """True when the second line is a Markdown table separator row."""
    lines = block.splitlines()
    return (
        len(lines) >= 2
        and "-" in lines[1]
        and bool(_TABLE_SEPARATOR.match(lines[1]))
    )


def _is_list(block):
    """True when the first non-empty line starts with a list marker."""
    for line in block.splitlines():
        if line.strip():
            return bool(_LIST_ITEM.match(line))
    return False


def _list_items(block):
    """Split a list block into items; wrapped lines stay with their item."""
    items = []
    current = []
    for line in block.splitlines():
        if _LIST_ITEM.match(line):
            if current:
                items.append("\n".join(current))
            current = [line.rstrip()]
        elif current:
            current.append(line.rstrip())
    if current:
        items.append("\n".join(current))
    return items


def _split_long(text, max_chars):
    """Split text longer than max_chars at natural boundaries."""
    if len(text) <= max_chars:
        return [text]
    pieces = []
    start = 0
    while len(text) - start > max_chars:
        end = _break_at(text, start, max_chars)
        pieces.append(text[start:end].strip())
        start = end
    if start < len(text):
        pieces.append(text[start:].strip())
    return pieces


def _break_at(text, start, max_chars):
    """Return the preferred cut position within (start, start + max_chars].

    Prefers the last sentence end, then the last space. When neither exists
    the whole remaining text is returned so words are never split.
    """
    limit = start + max_chars
    for match in reversed(list(_SENTENCE_END.finditer(text[start:limit]))):
        return start + match.end()
    pos = text.rfind(" ", start + 1, limit)
    if pos != -1:
        return pos + 1
    return len(text)


def _pack(parts, max_chars):
    """Greedily join parts into chunks, flushing when the limit is exceeded."""
    chunks = []
    current = ""
    for part in parts:
        if current and len(current) + 1 + len(part) > max_chars:
            chunks.append(current)
            current = part
        elif current:
            current = f"{current}\n{part}"
        else:
            current = part
    if current:
        chunks.append(current)
    return chunks
