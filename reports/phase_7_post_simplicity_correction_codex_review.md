# Codex Review: Phase 7 Post-Simplicity Correction

Decision: `ready_for_user_confirmation`
Reviewer: Codex
Date: 2026-08-26 15:49:54 +0700
User confirmation: 2026-08-26 +07, sau khi chạy Notebook 07
Canonical guide: `guides/phase_7_retrieval_answer_evaluation.md`
Implementation report:
`reports/phase_7_post_simplicity_correction_implementation_report.md`

## 1. Phạm vi đã review

Reviewer đã đọc prompt, design, plan, implementation report, exact scoped diff,
source của answer/retrieval paths, Phase 7 tests và Notebook 07. Reviewer kiểm
tra hai CSV, public signatures, tracing contract và active Qdrant collection,
sau đó chạy lại focused integration suite và Notebook 07 bằng dependency,
Qdrant, E5 và OpenAI thật.

## 2. Findings

Không có blocker hoặc major.

Thay đổi code là surgical: `run_answer_batch()` và `run_answer_ui()` không còn
nhận collection override; `run_retrieval_batch()`, `run_retrieval_ui()` và
shared `build_services()` vẫn giữ override đúng retrieval-only scope. Không có
wrapper, abstraction, retry, fallback, dependency hoặc test cơ chế mới.

`git diff --check` đạt cho source và notebook. Hai CSV dùng CRLF do Python
`csv` writer nên full scoped check báo trailing whitespace; đây là format sinh
tự động đã được implementation plan dự liệu, không phải lỗi dữ liệu.

## 3. Cách Reviewer chạy lại thật

Reviewer dùng `UV_CACHE_DIR=/tmp/hue-rag-phase7-review-uv-cache` và chạy:

```bash
uv run python -m py_compile backend/evaluation/eval.py \
  backend/evaluation/evaluator.py

cd backend
uv run --env-file ../.env python -m pytest \
  tests/test_evaluation.py -q --tb=short -s

cd ..
uv run --env-file .env jupyter nbconvert --execute --to notebook \
  notebooks/07_evaluation.ipynb \
  --output /tmp/07_evaluation-phase7-review.ipynb \
  --ExecutePreprocessor.timeout=1800
```

Reviewer cũng inspect signatures/source, validate notebook, đối chiếu row order
với `test2.jsonl`, tính lại summary từ CSV và đọc Qdrant collection state trước
và sau run.

## 4. Kết quả quan sát

- Public answer signatures không có `collection_name`; retrieval signatures
  vẫn có optional override.
- `py_compile` đạt.
- Focused suite: `9 passed, 4 warnings in 83.07s`; guarded test collection được
  cleanup thành công. Warnings là rename notice từ `sentence-transformers`.
- Temporary Notebook 07 Run All thành công và ghi
  `/tmp/07_evaluation-phase7-review.ipynb`; 10/10 code cells đã execute.
- Canonical Notebook 07 có 22 cells, 10 code cells, toàn bộ execution counts
  null và outputs rỗng sau run.
- Retrieval CSV: 20 rows đúng thứ tự, 0 errors; MRR `0.7917`, nDCG `0.8020`,
  keyword coverage `96.67%`.
- Answer CSV: 20 rows đúng thứ tự, 0 errors; accuracy `4.40`, completeness
  `4.05`, relevance `4.25`.
- Active `hue_foods_e5_small_384` giữ trạng thái green và 572 points trước/sau;
  không có bằng chứng mutation active collection.
- Dataset, validator, config, provider/model và retrieval/generation semantics
  không đổi. Không chạy paid 104-answer batch.

Lần chạy đầu trong sandbox đạt 6 test thuần nhưng 3 integration setup errors do
DNS bị chặn. Reviewer chạy lại ngoài network sandbox theo đúng live contract và
suite đạt đầy đủ; không dùng offline flag, fake hay fallback.

## 5. Giới hạn hoặc phần chưa chạy

Không chạy full 104-answer batch theo exact correction scope. Reviewer không
thao tác Gradio bằng browser, nhưng đã inspect app wiring/signatures; focused
suite chạy real retrieval UI path và Notebook chạy real answer batch path.

Golden dataset findings vẫn thuộc session dữ liệu riêng và không ảnh hưởng
decision của correction code/notebook này.

## 6. Decision và bước tiếp theo

Decision: `ready_for_user_confirmation`.

Người dùng đã chạy Notebook 07 và xác nhận correction ngày 2026-08-26 +07.
Canonical guide, guide index, user report và `Project_Status.md` được đồng bộ
sang trạng thái approved. Phase 8 vẫn đóng; golden dataset chỉ được thay đổi sau
session brainstorming riêng.
