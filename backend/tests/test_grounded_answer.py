"""Lõi chung `llm.grounded_answer` qua `answer_case` của bộ đánh giá — đường thật (Qdrant chỉ đọc, e5 + tokenizer local), không gọi model.

Bảo vệ spec streaming §4.8 khác biệt 3: lỗi kỹ thuật của một case thành `row["error"]` (lượt chấm incomplete), không ném ra
ngoài; các bước đã chạy trước lỗi vẫn ghi vào dòng như trước khi gom lõi chung.
"""
import asyncio

from core.settings_loader import load_settings
from evaluation.full_corpus_eval import RETRIEVAL_K, answer_case, build_context_builder, build_retrieval


def test_answer_case_turns_context_budget_error_into_row_error():
    settings = load_settings(validate_private_paths=False)
    settings["full_corpus_generation"] = dict(settings["full_corpus_generation"])
    settings["full_corpus_generation"]["context_limit"] = 2561  # cùng ngưỡng ép lỗi ngân sách như test_api_chat.py
    service = build_retrieval(settings, settings["full_corpus_runtime"]["retrieval_treatment"])
    try:
        case = {"case_index": 0, "category": "test", "question": "  Giá vé Đại Nội?  "}
        # generator=None: lỗi ngân sách xảy ra trước bước sinh nên model không bao giờ được gọi
        row = asyncio.run(answer_case(case, service, build_context_builder(settings), None))
    finally:
        service.close()
    assert row["error"].startswith("ContextBudgetError")
    assert len(row["top_chunk_ids"]) == RETRIEVAL_K  # bước tìm đã chạy ⇒ vẫn ghi
    assert row["context_sources"] is None and row["answer"] is None and row["refusal"] is None
    assert row["input_tokens"] is None and row["response_id"] is None
