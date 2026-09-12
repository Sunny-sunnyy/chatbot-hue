# Prompt chuyển session — Implementer correction 3 schema Golden reference

Bạn là Implementer tại `/home/minhhieu/hue_rag`.

Đọc đầy đủ theo thứ tự; nếu output bị cắt, đọc tiếp phần thiếu:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. `handoff_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md`
8. `reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md`
   — đọc toàn bộ, mục 9–10 là verdict/delta hiện hành; R1–R3 đã đóng.
9. `reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md`
   — đọc toàn văn trước và sau sửa.
10. `docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md`
    — đọc mục 5 đầy đủ để xác nhận schema/evidence Foods V3.
11. `knowledge-base-hue/foods/evaluation/golden_v3.jsonl`
    — chỉ đọc vài rows đủ xác nhận schema; không audit dataset quality.
12. `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`
    — đọc snapshot đầu và mục 39–41 đầy đủ.
13. `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`
    — đọc đầy đủ, nhất là quyết định Golden evidence C.
14. `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`
    — đọc đầy đủ; chưa phải implementation plan approved.

Thực hiện toàn bộ CURRENT_HANDOFF correction lượt 3 cho R4. Chỉ sửa report
summary và trả CURRENT_HANDOFF về Reviewer/final_review. Sửa đúng schema Foods
V3, đồng bộ §4.2/bảng §6/§7 với quyết định C, bỏ câu hỏi đã được user chốt và
giữ rõ những phần full schema/evaluation còn mở. Cập nhật self-review §8 nhưng
không tự ghi R4 approved/closed.

Không chạy code/model/tokenizer/notebook/tests/API/Qdrant/benchmark, không đọc
`.env`, không dùng mạng/dependency, không sửa runtime/corpus/Golden/spec/plan/
review/context/prompt, không Git write và không sub-agent. Không mở lại R1–R3,
parser/source locator hoặc Ca Huế VN/QT. Được kiểm read-only HEAD/status/diff
và `git diff --check`.

Kết thúc bằng báo cáo ngắn và prompt trả Reviewer đọc bootstrap,
CURRENT_HANDOFF, Codex review mục 9–10 và report hiện hành.
