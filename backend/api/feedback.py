"""Đánh giá 👍 / 👎 cho một lượt trả lời (B142 — User chọn "chỉ lưu đánh giá"; nghiên cứu sản phẩm thật `BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 00).

Server cấp **mã lượt** ngẫu nhiên (không suy ra từ mã cuộc trò chuyện, không nằm trong cookie) khi lượt có câu trả lời cuối, giữ trong RAM
mã ⇒ {tuyến, outcome, số nguồn được trích} (trần số lượt, khởi động lại server ⇒ mất). `POST /api/feedback` chỉ nhận mã đó + `up` / `down`
rồi ghi **một dòng log** `chat_feedback`: mã lượt, tuyến, outcome, số nguồn, đánh giá — không chữ câu hỏi / câu trả lời, không mã cuộc.
Bấm lại (đổi ý) ⇒ thêm một dòng; dòng sau cùng là ý cuối.

`POST /api/bao_sai` (việc nhỏ 8, A 08/11): nút "Báo thông tin chưa đúng" ở trang bài Khám phá ⇒ một dòng log `chat_bao_sai` chỉ có `bai_id`
(thời điểm = dấu giờ của dòng log). Không nhận chữ tự do; `bai_id` phải trùng **nguyên chuỗi** một bài trong danh sách Khám phá (như
`/api/kham_pha/bai`) ⇒ không ghi được chuỗi tuỳ ý vào log.
"""
import json
import logging
import secrets
from collections import OrderedDict
from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger("chat")
router = APIRouter()

MAX_TURNS = 2000  # trần RAM: bỏ lượt cũ nhất
# Test khoá đúng tập trường này (thêm trường phải sửa có chủ đích, như `METRIC_FIELDS`).
FEEDBACK_FIELDS = ("turn_id", "route", "outcome", "n_cited_sources", "rating")


class FeedbackTurns:
    def __init__(self, max_turns: int = MAX_TURNS) -> None:
        self._items: OrderedDict[str, dict] = OrderedDict()
        self._max = max_turns

    def add(self, route: str | None, outcome: str | None, n_cited_sources: int) -> str:
        turn_id = secrets.token_urlsafe(12)  # 16 ký tự
        self._items[turn_id] = {"route": route, "outcome": outcome, "n_cited_sources": n_cited_sources}
        while len(self._items) > self._max:
            self._items.popitem(last=False)
        return turn_id

    def get(self, turn_id: str) -> dict | None:
        return self._items.get(turn_id)


class FeedbackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    turn_id: str = Field(pattern=r"^[A-Za-z0-9_-]{16}$")
    rating: Literal["up", "down"]


@router.post("/api/feedback")
async def feedback(body: FeedbackRequest, request: Request):
    from api.routes.chat import error_response  # một chỗ dựng thân lỗi JSON

    turn = request.app.state.feedback_turns.get(body.turn_id)
    if turn is None:  # mã lạ / server đã khởi động lại / lượt quá cũ
        return error_response(404, "unknown_turn", "Không tìm thấy lượt trả lời này.")
    logger.info("chat_feedback %s", json.dumps({"turn_id": body.turn_id, **turn, "rating": body.rating}))
    return {"ok": True}


class BaoSaiRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bai_id: str = Field(min_length=1, max_length=300)


@router.post("/api/bao_sai")
async def bao_sai(body: BaoSaiRequest, request: Request):
    from api.routes.chat import error_response

    bai = getattr(request.app.state, "kham_pha", None)
    if bai is None or body.bai_id not in bai:
        return error_response(404, "not_found", "Không tìm thấy bài này.")
    logger.info("chat_bao_sai %s", json.dumps({"bai_id": body.bai_id}, ensure_ascii=False))
    return {"ok": True}
