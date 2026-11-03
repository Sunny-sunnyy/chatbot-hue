"""Nhớ hội thoại trong một cuộc trò chuyện (Phase 9 B3, plan `docs/superpowers/plans/2026-11-03-phase-9-b3-plan.md` D1, D2, D4).

Kho trong RAM của app: `conversation_id` (mã ngẫu nhiên, nằm trong cookie HttpOnly) → các lượt đã xong. Server giữ lịch sử — trình duyệt
không gửi lại "trợ lý đã nói…" (chỗ cài lệnh, spec §3). Hết hạn 30 phút từ lượt cuối; trần 500 cuộc; mỗi cuộc giữ 3 lượt gần nhất và
≤ 1.500 token lịch sử (bỏ lượt cũ nhất trước, không tóm tắt). Không ghi đĩa, không log chữ / mã cuộc. Khởi động lại server ⇒ mất hết.
Không khoá: hai yêu cầu cùng cuộc chạy song song thì lượt xong sau ghi sau (một người dùng — spec §7).
"""
import re
import secrets
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Callable

from llm.citations import CITATION_PATTERN

TTL_SECONDS = 30 * 60
MAX_CONVERSATIONS = 500
MAX_TURNS = 3
MAX_HISTORY_TOKENS = 1500
_SPACE_BEFORE_PUNCT = re.compile(r"\s+([.,;:!?])")


def stored_answer(answer: str) -> str:
    """Câu trả lời đem vào lịch sử: bỏ mã trích dẫn `[n]` / `[Nguồn n]` — số nguồn đánh lại mỗi lượt, mã cũ làm model trích nhầm sổ nguồn
    lượt mới (D2). Chỗ cắt mục "Từ web" của B6 đặt ở đây."""
    text = CITATION_PATTERN.sub("", answer)
    return _SPACE_BEFORE_PUNCT.sub(r"\1", re.sub(r"[ \t]{2,}", " ", text)).strip()


@dataclass
class Conversation:
    turns: list[tuple[str, str]] = field(default_factory=list)  # (câu hỏi, câu trả lời đã cắt) — câu trả lời "" khi chỉ nhớ câu hỏi
    expires_at: float = 0.0


class ConversationStore:
    def __init__(self, count_tokens: Callable[[str], int], *, ttl: float = TTL_SECONDS, max_conversations: int = MAX_CONVERSATIONS,
                 max_turns: int = MAX_TURNS, max_history_tokens: int = MAX_HISTORY_TOKENS, keep_answers: bool = True,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._count = count_tokens
        self._ttl, self._max_conversations = ttl, max_conversations
        self._max_turns, self._max_tokens = max_turns, max_history_tokens
        self._keep_answers = keep_answers
        self._clock = clock
        self._items: OrderedDict[str, Conversation] = OrderedDict()

    def _drop_expired(self) -> None:
        now = self._clock()
        for cid in [cid for cid, c in self._items.items() if c.expires_at <= now]:
            del self._items[cid]

    def ensure(self, conversation_id: str | None) -> str:
        """Mã cuộc dùng cho lượt này: mã còn hạn ⇒ giữ; không có / hết hạn / lạ ⇒ cuộc mới (mã mới)."""
        self._drop_expired()
        if conversation_id in self._items:
            return conversation_id
        new_id = secrets.token_urlsafe(16)
        self._items[new_id] = Conversation(expires_at=self._clock() + self._ttl)
        while len(self._items) > self._max_conversations:  # trần RAM: bỏ cuộc cũ nhất
            self._items.popitem(last=False)
        return new_id

    def history(self, conversation_id: str) -> tuple[tuple[str, str], ...]:
        conversation = self._items.get(conversation_id)
        return () if conversation is None else tuple(conversation.turns)

    def history_tokens(self, conversation_id: str) -> int:
        """Số token lịch sử của cuộc (chỉ số đếm cho log — không chữ)."""
        return sum(self._count(q) + self._count(a) for q, a in self.history(conversation_id))

    def append(self, conversation_id: str, question: str, answer: str) -> None:
        """Ghi một lượt đã xong rồi cắt theo trần lượt / token (bỏ lượt cũ nhất trước)."""
        conversation = self._items.get(conversation_id)
        if conversation is None:  # hết hạn trong lúc trả lời ⇒ không ghi
            return
        conversation.turns.append((question, stored_answer(answer) if self._keep_answers else ""))
        del conversation.turns[:-self._max_turns]
        while len(conversation.turns) > 1 and sum(self._count(q) + self._count(a) for q, a in conversation.turns) > self._max_tokens:
            conversation.turns.pop(0)
        conversation.expires_at = self._clock() + self._ttl
        self._items.move_to_end(conversation_id)

    def reset(self, conversation_id: str | None) -> str:
        """"Cuộc trò chuyện mới": xoá cuộc hiện tại khỏi RAM, trả mã mới."""
        self._items.pop(conversation_id, None)
        return self.ensure(None)
