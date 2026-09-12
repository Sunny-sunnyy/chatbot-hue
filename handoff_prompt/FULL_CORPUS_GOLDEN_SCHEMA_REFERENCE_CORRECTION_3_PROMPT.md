# Implementer — correction lượt 3 khảo sát sâu Golden schema

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

## Đọc bắt buộc

Đọc đầy đủ theo thứ tự; nếu output bị cắt, đọc tiếp phần thiếu:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. `handoff_prompt/FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_CORRECTION_2_PROMPT.md`
8. `reports/full_corpus_golden_schema_reference_deep_dive_codex_review_2026_09_10.md`,
   đặc biệt §§8–9
9. `reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`

## Correction scope

R1, R2, R4 và R5 đã đạt. R3 chỉ còn một mâu thuẫn:

- sơ đồ §6 vẫn ghi `case_id (định danh bất biến)`, trái với các đoạn đã sửa rằng
  Foods V3 ID tuần tự theo file order và không bất biến qua insert/reorder;
- thay nhãn đó bằng `case_id (định danh tường minh)`;
- quét toàn report để xác nhận không còn nhãn/câu tương tự gọi Foods V3 hoặc
  proposed Full Corpus `case_id` là bất biến hay độc lập với file order;
- cập nhật self-review và CURRENT_HANDOFF cho correction lượt 3. Không tự claim
  PASS, approval hoặc closure.

Không đọc lại 64 Markdown, không viết lại coverage, candidates hay findings đã
đạt. Không chọn schema.

## Output và giới hạn

Chỉ sửa:

- `reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`;
- `session_prompt/CURRENT_HANDOFF.md`.

Không tạo review/user report/report phụ; không sửa Project Status, context,
spec, plan, guides hoặc index. Không chạy Python/code/script/notebook/model/
tokenizer/API/Qdrant/tests/benchmark; không đọc `.env`, không dùng mạng, không
sửa runtime/tests/corpus/Golden/index/reference, không Git write và không spawn
subagent.

Sau self-review read-only, trả CURRENT_HANDOFF thành Reviewer/final_review và
báo đúng một correction hẹp đã làm. Reviewer sẽ kiểm độc lập trước khi PASS.
