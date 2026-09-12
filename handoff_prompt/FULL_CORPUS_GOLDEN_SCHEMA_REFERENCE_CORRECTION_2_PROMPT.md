# Implementer — correction lượt 2 khảo sát sâu Golden schema

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

## 1. Đọc bắt buộc

Đọc đầy đủ theo thứ tự; nếu output bị cắt, đọc tiếp phần thiếu:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. `handoff_prompt/FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_DEEP_DIVE_PROMPT.md`
8. `handoff_prompt/FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_CORRECTION_1_PROMPT.md`
9. `reports/full_corpus_golden_schema_reference_deep_dive_codex_review_2026_09_10.md`,
   đặc biệt §§6–7
10. `reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`

## 2. Correction scope

Không viết lại các phần R1/R5 đã đạt. Sửa bốn việc còn lại:

1. **R2 full reading:** đọc toàn văn từng file trong cả
   `knowledge-base/employees/` và `knowledge-base/contracts/` dưới
   `/home/minhhieu/llm_rag/tai_lieu/rag_old_0`. Đây là 64 Markdown còn thiếu.
   Dùng lệnh đọc text, không dùng Python/script. Nếu một file không đọc được,
   ghi exact path và hạ coverage; không claim `omission = 0` hoặc task hoàn tất.
   Phân biệt inventory, structural inspection và full-text reading.
2. **R3 quota/ID:** reference chỉ có observed category distribution, không có
   evidence quota định trước. Foods V3 explicitly không enforce quota. Foods V3
   IDs được validator yêu cầu tuần tự theo file order; không gọi chúng độc lập
   với line order hoặc bất biến qua insert/reorder.
3. **R4 support boundary:** trong candidate table, đổi “hỗ trợ đầy đủ IR” và
   “hỗ trợ negative/conflict” thành structural capacity dự kiến. Exact
   case-type representation, empty/alternative evidence rules, retrieval
   scoring và judge rubric vẫn unresolved.
4. Đồng bộ Executive Summary, coverage table, matrix/candidates, self-review và
   CURRENT_HANDOFF. Không tự claim PASS/approval.

## 3. Output và quyền

Chỉ sửa:

- `reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`
- `session_prompt/CURRENT_HANDOFF.md`

Không tạo review, user report, report phụ hoặc sửa Project Status/context/spec/
plan/guides/index.

Không chạy Python/code/script/notebook/model/tokenizer/API/Qdrant/tests/
benchmark; không đọc `.env`, không mạng/download, không sửa runtime/tests/
corpus/Golden/index/reference, không Git write và không spawn subagent.

## 4. Bàn giao

Sau self-review read-only, trả CURRENT_HANDOFF thành Reviewer/final_review.
Tóm tắt đúng full-text coverage và bốn chỉnh sửa; không gọi findings closed.
Schema candidates vẫn là proposals chờ Reviewer kiểm và User thảo luận.
