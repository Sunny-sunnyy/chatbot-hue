# Implementer — correction lượt 2 báo cáo simplicity evaluation `rag_old_0`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Đây là correction docs-only rất hẹp. Đọc đầy đủ bootstrap bắt buộc trong
`session_prompt/IMPLEMENTER_WORKFLOW.md`, sau đó đọc:

1. `session_prompt/CURRENT_HANDOFF.md`
2. `handoff_prompt/FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_CORRECTION_1_PROMPT.md`
3. mục 6–7 trong
   `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_codex_review_2026_09_10.md`
4. report cần sửa:
   `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md`
5. exact canonical field decisions tại `guides/full_corpus_rag.md` và mục
   “Golden record field set” trong working decision notes.

Không khảo sát lại và không mở lại C1/C4 hoặc phần benchmark đã đạt.

## Sửa bắt buộc

1. **Exact source lines**
   - `calculate_mrr`: `evaluation/eval.py:45-51`; aggregation case: 96-97.
   - `calculate_ndcg`: `evaluation/eval.py:62-78`; aggregation case: 100-101.
   - `evaluator2.py`: `category_mrr` dòng 132 và `category_accuracy` dòng 216.
   - Quét các source citations còn lại và sửa nếu label không khớp line hiện
     hành. Không claim “toàn bộ đúng” nếu chưa đối chiếu.

2. **Canonical field decisions**
   - `claim_id`: canonical không lưu; chỉ nói evaluator/report derive từ
     `case_id` + claim ordinal. Không tự chốt format string/delimiter.
   - Candidate C phải bỏ `claim_id`, đổi `claim_text` thành `text`.
   - `case_type`: canonical đã chốt không lưu vì không có consumer; không mở lại
     factual/negative/conflict routing trong report này.
   - `domain`: canonical không lưu và hiện không có code consumer như report mô
     tả; nếu cần có thể suy từ authoring partition/manifest hoặc evidence source,
     không từ case-ID prefix chưa được chốt.
   - `partition`: chỉ là P7 authoring/review metadata, bị loại khi merge và không
     có trong canonical JSONL.
   - Không trình bày representation chi tiết chưa chốt như một schema approved;
     nếu giữ Candidate C JSON thì ghi rõ `evidence_groups` syntax minh họa và
     semantics chi tiết vẫn unresolved.

3. **Metric boundary**
   - Thay `True Corpus Retrieval Recall` bằng mô tả đúng: coverage/completeness
     của expected claims/evidence groups đã khai báo.
   - Không nói evidence groups tự tạo exhaustive relevant-chunk labels cho toàn
     corpus.

4. **Reproducibility claim**
   - Bỏ quy nguyên nhân cụ thể cho server drift/floating-point vì khảo sát không
     kiểm chứng chúng.
   - Chỉ giữ: seed là best-effort, core/single-run judge không cung cấp bảo đảm
     deterministic.

5. Đồng bộ Executive Summary, matrix, candidates, self-review và handoff. Giữ
   nguyên các phần C1/C4 đã PASS và benchmark attribution đã đạt.

## Quyền và output

Chỉ sửa:

- `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md`
- `session_prompt/CURRENT_HANDOFF.md`

Không sửa review/prompt/canonical/runtime/tests/notebooks/corpus/Golden/index.
Không chạy/import code, Python, tests, notebook, model, API, Qdrant hay
benchmark; không đọc `.env`/knowledge-base data, không mạng, không Git write và
không spawn subagent.

Khi xong trả `reviewer/final_review`, `State: active`, liệt kê mapping bốn nhóm
sửa trên và không tự claim PASS/approval/closure.
