"""Bóc chữ trả lời từ luồng JSON `{"answer": "…"}` đang stream, để hiện chữ ngay khi model viết (spec streaming §4.3 bước 2–3).

Model trả đầu ra có cấu trúc (`AnswerOutput`), nên mảnh chữ từ provider là mảnh của một chuỗi JSON. Ở đây chỉ bóc phần thân chuỗi
`answer`, giải mã thoát JSON (cả `\\uXXXX` bị cắt giữa mảnh) và chuẩn hóa `[Nguồn n]` → `[n]` như `llm.citations.normalize_citations`.
Chữ cuối vẫn do `parse_structured_output` + bộ kiểm citation quyết; phần này chỉ là chữ hiện tạm.
"""
import json
import re

from llm.citations import normalize_citations

# Chữ người dùng thấy bắt đầu sau tiền tố JSON này (C73, tag `hoso/c70-ttft` `backend/experiments/streaming/ttft.py`).
ANSWER_PREFIX = re.compile(r'^\s*\{\s*"answer"\s*:\s*"')
# Thoát JSON còn dở ở cuối mảnh: một số lẻ dấu `\` (tùy chọn kèm `u` + < 4 chữ số hex).
PARTIAL_ESCAPE = re.compile(r"(\\+)(u[0-9a-fA-F]{0,3})?$")
# Đuôi chữ có thể còn thành citation khi mảnh sau tới: mọi tiền tố của `[ nguồn 12 ]` chưa có `]` (cùng dạng `CITATION_PATTERN`).
OPEN_CITATION_TAIL = re.compile(r"\[\s*(?:n|ng|ngu|nguồ|(?:nguồn\s*)?(?:\d+\s*)?)", re.IGNORECASE)


def decode_partial_string(raw: str) -> tuple[str, bool]:
    """Phần thân chuỗi JSON đang stream ⇒ (chữ đã giải mã, chuỗi đã đóng chưa); bỏ phần thoát còn dở ở cuối mảnh (C73, có test)."""
    escaped, end = False, None
    for index, char in enumerate(raw):
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            end = index
            break
    body = raw if end is None else raw[:end]
    partial = PARTIAL_ESCAPE.search(body)
    if end is None and partial and len(partial.group(1)) % 2 == 1:
        body = body[: partial.start(1) + len(partial.group(1)) - 1]
    return json.loads(f'"{body}"'), end is not None


def displayable_prefix(answer: str, closed: bool) -> str:
    """Phần chữ hiện được ngay: giữ lại đuôi `[…` có thể còn thành citation (chờ `]` rồi mới chuẩn hóa). Chuỗi đã đóng ⇒ hiện hết."""
    if closed:
        return answer
    start = answer.rfind("[")
    if start != -1 and "]" not in answer[start:] and OPEN_CITATION_TAIL.fullmatch(answer[start:]):
        return answer[:start]
    return answer


class AnswerTextStream:
    """Nhận lần lượt các mảnh `response.output_text.delta`, trả phần chữ **mới** hiện được (đã chuẩn hóa citation).

    Ghép mọi phần trả về = `normalize_citations` của chữ trong JSON tới lúc đó; khi chuỗi đóng, = toàn bộ chữ `answer` (chưa `.strip()`)."""

    def __init__(self) -> None:
        self.raw = ""
        self.shown = ""

    def feed(self, delta: str) -> str:
        self.raw += delta
        prefix = ANSWER_PREFIX.match(self.raw)
        if prefix is None:
            return ""
        answer, closed = decode_partial_string(self.raw[prefix.end():])
        visible = normalize_citations(displayable_prefix(answer, closed))
        # Đuôi bị giữ chỉ nằm sau phần đã hiện ⇒ chữ hiện được chỉ dài thêm; không bao giờ phải sửa chữ đã gửi.
        new_text = visible[len(self.shown):]
        self.shown = visible
        return new_text
