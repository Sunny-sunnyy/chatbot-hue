# Phase 7 Post-Simplicity Correction Implementation Report

Date: 2026-08-26 15:40:17 +0700
Status: `ready_for_review`

## Scope implemented

1. **Answer Evaluation Signature Correction**:
   - Loại bỏ tham số `collection_name` khỏi public `run_answer_batch()` trong `backend/evaluation/eval.py`.
   - Loại bỏ tham số `collection_name` khỏi `run_answer_ui()` trong `backend/evaluation/evaluator.py`.
   - Giữ nguyên `build_services(profile="dense_only", collection_name=None)` làm composition root nội bộ để phục vụ retrieval comparison và guarded real verification.
   - Giữ nguyên `collection_name` trên `run_retrieval_batch()` và `run_retrieval_ui()`.

2. **Notebook 07 Cleanliness & Temporary Execution**:
   - Làm sạch toàn bộ execution counts và outputs trong canonical notebook `notebooks/07_evaluation.ipynb`.
   - Xác thực canonical notebook đạt trạng thái sạch (`execution_count: null`, không có outputs).
   - Thực thi Run All notebook đến bản tạm `/tmp/07_evaluation-phase7-correction.ipynb` bằng Qdrant và OpenAI API thật.
   - Kiểm tra lại canonical notebook vẫn giữ nguyên trạng thái sạch sau khi chạy.

3. **Live Verification & Artifact Integrity**:
   - Chạy bộ test tích hợp `backend/tests/test_evaluation.py` với Qdrant và OpenAI API thật (`9 passed, 4 warnings in 81.64s`).
   - Xác minh hai file CSV kết quả (`backend/evaluation/retrieval_results.csv` và `backend/evaluation/answer_results.csv`) có đúng 20 dòng, khớp thứ tự 20 câu hỏi từ `test2.jsonl`, và không có row error nào.

## Exact files changed

- `backend/evaluation/eval.py`: bỏ `collection_name` khỏi signature và call của `run_answer_batch()`.
- `backend/evaluation/evaluator.py`: bỏ `collection_name` khỏi signature và call của `run_answer_ui()`.
- `notebooks/07_evaluation.ipynb`: xóa execution counts và cell outputs.
- `backend/evaluation/retrieval_results.csv`: cập nhật kết quả fresh smoke run 20 câu.
- `backend/evaluation/answer_results.csv`: cập nhật kết quả fresh smoke run 20 câu.
- `reports/phase_7_post_simplicity_correction_implementation_report.md`: tạo mới implementation report.

## Commands executed

```bash
# 1. Surface check trước thay đổi
grep -En "def build_services|def run_retrieval_batch|def run_answer_batch|def run_retrieval_ui|def run_answer_ui|collection_name" backend/evaluation/*.py backend/tests/test_evaluation.py

# 2. Biên dịch kiểm tra syntax sau khi sửa eval.py và evaluator.py
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run python -m py_compile \
  backend/evaluation/eval.py backend/evaluation/evaluator.py

# 3. Xác minh lại surface sau thay đổi
grep -En "def run_retrieval_batch|def run_answer_batch|def run_retrieval_ui|def run_answer_ui|collection_name" backend/evaluation/eval.py backend/evaluation/evaluator.py backend/evaluation/retrieval_comparison.py

# 4. Làm sạch outputs của canonical notebook
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run jupyter nbconvert \
  --ClearOutputPreprocessor.enabled=True --inplace notebooks/07_evaluation.ipynb

# 5. Kiểm tra cấu trúc và tính sạch sẽ của canonical notebook
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run python -c 'import nbformat; p="notebooks/07_evaluation.ipynb"; n=nbformat.read(p, 4); nbformat.validate(n); code=[c for c in n.cells if c.cell_type=="code"]; assert all(c.execution_count is None for c in code); assert all(not c.outputs for c in code); print(len(n.cells), "cells; canonical notebook clean")'

# 6. Khởi động Qdrant và thực thi Notebook 07 ra file tạm
docker compose up -d
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run --env-file .env \
  jupyter nbconvert --execute --to notebook notebooks/07_evaluation.ipynb \
  --output /tmp/07_evaluation-phase7-correction.ipynb \
  --ExecutePreprocessor.timeout=1800

# 7. Kiểm tra lại canonical notebook vẫn sạch sau execution
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run python -c 'import nbformat; p="notebooks/07_evaluation.ipynb"; n=nbformat.read(p, 4); nbformat.validate(n); code=[c for c in n.cells if c.cell_type=="code"]; assert all(c.execution_count is None for c in code); assert all(not c.outputs for c in code); print(len(n.cells), "cells; canonical notebook clean")'

# 8. Chạy focused integration suite
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_evaluation.py -q --tb=short -s

# 9. Xác thực số dòng và thứ tự câu hỏi trong 2 CSV kết quả
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run python -c 'import csv, json; from pathlib import Path; q=Path("knowledge-base-hue/foods/evaluation/test2.jsonl"); expected=[json.loads(line)["question"] for line in q.open(encoding="utf-8") if line.strip()]; base=Path("backend/evaluation"); files=[base/"retrieval_results.csv", base/"answer_results.csv"]; rows=[list(csv.DictReader(p.open(encoding="utf-8"))) for p in files]; assert all(len(r)==20 for r in rows); assert all([x["question"] for x in r]==expected for r in rows); print([(p.name, len(r)) for p,r in zip(files,rows)], "ordered")'

# 10. Kiểm tra diff whitespace và git status
git diff --check -- backend/evaluation/eval.py backend/evaluation/evaluator.py notebooks/07_evaluation.ipynb
git status --short
```

## Observed test and Notebook results

- **`py_compile`**: exit code 0, không có lỗi cú pháp.
- **Canonical Notebook Cleanliness Check**: `22 cells; canonical notebook clean`.
- **Notebook 07 Run All**:
  - Ghi thành công vào `/tmp/07_evaluation-phase7-correction.ipynb` (49,411 bytes).
  - Exit code: 0.
  - Quá trình chạy gọi thực tế Qdrant vector retrieval, OpenAI `gpt-5.4-nano` generation và `gpt-5.4-mini` judge.
  - Recheck sau khi chạy: canonical notebook vẫn giữ nguyên `22 cells; canonical notebook clean`.
- **Integration Tests (`backend/tests/test_evaluation.py`)**:
  - Kết quả: `9 passed, 4 warnings in 81.64s`.
  - Cảnh báo: `FutureWarning` liên quan đến phương thức dimension của thư viện sentence-transformers (không phải lỗi logic).
  - Tự động dọn dẹp guarded collection `hue_rag_live_test_e5_small_384: ok`.

## CSV row counts, summaries, and row errors

- **`retrieval_results.csv`**:
  - Số dòng: 20 data rows, khớp tuyệt đối 20 câu hỏi và thứ tự của `test2.jsonl`.
  - Row errors: 0 (`retrieval errors: []`).
  - Summary:
    - Questions: 20
    - Successful: 20
    - Failed: 0
    - MRR: 0.7917
    - nDCG: 0.8020
    - Keyword coverage: 96.67%

- **`answer_results.csv`**:
  - Số dòng: 20 data rows, khớp tuyệt đối 20 câu hỏi và thứ tự của `test2.jsonl`.
  - Row errors: 0 (`answer errors: []`).
  - Summary:
    - Questions: 20
    - Successful: 20
    - Failed: 0
    - Accuracy: 4.20 / 5.0
    - Completeness: 4.05 / 5.0
    - Relevance: 4.10 / 5.0

## Scope audit and unchanged contracts

- Public answer evaluation (`run_answer_batch`, `run_answer_ui`) không còn nhận `collection_name`.
- Retrieval-only path (`run_retrieval_batch`, `run_retrieval_ui`) vẫn giữ optional `collection_name`.
- `build_services()` giữ signature linh hoạt để phục vụ retrieval comparison và tests.
- Không thay đổi `test2.jsonl`, `tests.jsonl`, `validate_tests.py` hoặc thêm golden dataset mới.
- Không chạy batch 104 câu trả lời trả phí (chỉ chạy smoke set 20 câu đã được duyệt).
- Không thêm abstraction, wrapper, retry, fallback, cost logic hay dependency mới.
- Tracing của OpenAI Agents SDK tiếp tục tắt theo quyết định đơn giản hóa Phase 6.
- Active Qdrant collection `hue_foods_e5_small_384` luôn ở trạng thái read-only (nguyên vẹn 572 points).
- Toàn bộ thay đổi dirty-worktree không liên quan được giữ nguyên.
- Không thực hiện commit hoặc push git.

## Handoff to Reviewer

Tất cả các bước trong plan [2026-08-26-phase-7-post-simplicity-correction.md](file:///home/minhhieu/hue_rag/docs/superpowers/plans/2026-08-26-phase-7-post-simplicity-correction.md) đã hoàn thành. Reviewer có thể kiểm tra độc lập:

1. Chạy inspect surface:
   ```bash
   grep -En "def run_retrieval_batch|def run_answer_batch|def run_retrieval_ui|def run_answer_ui|collection_name" backend/evaluation/eval.py backend/evaluation/evaluator.py backend/evaluation/retrieval_comparison.py
   ```
2. Kiểm tra tính sạch sẽ của canonical notebook:
   ```bash
   uv run python -c 'import nbformat; p="notebooks/07_evaluation.ipynb"; n=nbformat.read(p, 4); nbformat.validate(n); code=[c for c in n.cells if c.cell_type=="code"]; assert all(c.execution_count is None for c in code); assert all(not c.outputs for c in code); print("Canonical notebook is clean")'
   ```
3. Xem notebook đã thực thi tại `/tmp/07_evaluation-phase7-correction.ipynb`.
4. Chạy lại bộ test tích hợp:
   ```bash
   cd backend && uv run --env-file ../.env python -m pytest tests/test_evaluation.py -q --tb=short -s
   ```
5. Kiểm tra 20 dòng trong 2 file CSV:
   ```bash
   uv run python -c 'import csv, json; from pathlib import Path; q=Path("knowledge-base-hue/foods/evaluation/test2.jsonl"); expected=[json.loads(line)["question"] for line in q.open(encoding="utf-8") if line.strip()]; base=Path("backend/evaluation"); files=[base/"retrieval_results.csv", base/"answer_results.csv"]; rows=[list(csv.DictReader(p.open(encoding="utf-8"))) for p in files]; assert all(len(r)==20 for r in rows); assert all([x["question"] for x in r]==expected for r in rows); print("CSVs 20 rows verified")'
   ```
