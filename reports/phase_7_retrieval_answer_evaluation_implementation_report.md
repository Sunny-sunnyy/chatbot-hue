# Implementation Report: Phase 7 Retrieval & Answer Evaluation

Implementer: DeepSeek
Date: 2026-08-23 (revision 9 — Hardened Consent Gate, Calibration Raw Validation, Numeric Integrity & Exact Attempt Linkage)
Report path:

```text
reports/phase_7_retrieval_answer_evaluation_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_7_retrieval_answer_evaluation.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md
reports/phase_7_retrieval_answer_evaluation_codex_review.md
```

## Approved Scope

Remediation vòng 7 (Revision 9) của Phase 7 giải quyết dứt điểm toàn bộ 4 blocker findings và 3 major findings từ Codex Review:
1. **Consent Gate Hardening (Blocker 1)**:
   - Trong `backend/evaluation/evaluator.py:cmd_answers()`: Cho cả fresh run lẫn resume run, kiểm tra `if not getattr(args, "confirm_paid", False):` ngay lập tức sau preflight estimate và return với 0 calls trước khi khởi tạo Qdrant client, budget file, calibration state, generator/judge.

2. **Calibration Raw Validation (Blocker 2)**:
   - Thêm helper `raw_validate_calibration_records()` trong `backend/evaluation/answer_eval.py` để validate danh sách raw records tuần tự trước khi nạp vào dict/map.
   - Từ chối các bản ghi bị trùng lặp `generation_run_id`, non-dict, unexpected case/sample IDs, sai `run_id`, `case_id`, `category`, `dataset_checksum`, `config_checksum`, `samples_checksum`, `judge_model`, `rubric_version`, `prompt_hash`, hoặc trạng thái incomplete trong final package.
   - Trước khi finalize run, normalize thứ tự các rows theo đúng thứ tự frozen samples, ghi nguyên tử vào file partial, đọc lại và validate, sau đó mới finalize.
   - Nếu `final.jsonl` đã tồn tại mà thiếu summary, validate toàn bộ raw records và tái tạo summary với 0 provider calls.

3. **Numeric Integrity & No-Refund Policy trong `CallBudget` (Blocker 3)**:
   - Thêm các helper kiểm tra số nguyên dương, số nguyên không âm, và số thực hữu hạn không âm (`_is_positive_integer`, `_is_nonnegative_integer`, `_is_finite_nonnegative_number`).
   - Kiểm tra và từ chối `NaN`, `+Inf`, `-Inf`, số âm ở `create()`, `load()`, `reserve()`, `settle_success()`, `settle_error()`.
   - Bắt buộc `json.dump(..., allow_nan=False)` trong `_persist()`.
   - Xóa bỏ hoàn toàn method `cancel()` — các reservation đã persist vào đĩa vĩnh viễn không được hoàn lại.
   - Kiểm tra đối sánh chính xác (exact comparison không dùng loose float tolerances) để phát hiện giả mạo file state.

4. **Subcommand `all` Contract (Blocker 4)**:
   - Bổ sung `set_defaults(resume=None, calibration=None)` trong parser của subcommand `all` và gán fallback trong `cmd_all()` để ủy quyền sang `cmd_answers()` mà không gây `AttributeError`.

5. **Strict Budget Validation trong Notebook 07 Cell 15 (Major 5)**:
   - Bắt buộc `budget_artifact_path` là đường dẫn relative an toàn (từ chối path traversal `..` hoặc absolute path).
   - Kiểm tra file budget tồn tại, tính toán SHA-256 trên byte thật của file budget và đối sánh với `budget_artifact_checksum`.
   - Tải và xác thực đầy đủ identity, limits, và đối sánh chính xác các snapshot totals (calls, effective cost, unresolved count).
   - Assert từ 56 đến 64 calls cho package hợp lệ.

6. **Attempt Evidence & Generation Row `attempts` (Major 6)**:
   - Mở rộng schema `generation_record` và `judge_record` để lưu giữ `attempts`, `cost_usd_total`, và `attempt_ids`.
   - Ghi nhận đầy đủ lịch sử của tất cả các lần thử (kể cả lần 1 thất bại và lần 2 thành công) và tổng chi phí lũy kế.

7. **Fresh Calibration Reuse Policy (Major 7)**:
   - Từ chối cờ `--calibration` trên fresh runs trong bước preflight (dừng lại với 0 calls). Fresh paid run luôn chạy 8 mẫu calibration mới ứng với budget mới.
   - `--calibration` chỉ được phép dùng khi `--resume` và phải khớp chính xác với `calibration_run_id` trong durable budget state.

---

## Summary — findings đã sửa (vòng 7 = revision 9)

| Finding | Fix |
|---|---|
| blocker: Resume thiếu `--confirm-paid` vượt consent gate | Kiểm tra `--confirm-paid` ngay sau preflight estimate cho cả fresh lẫn resume, return ngay trước khi chạm tới Qdrant/budget. |
| blocker: Calibration duplicate raw ID bị collapse thay vì reject | Triển khai `raw_validate_calibration_records()` kiểm tra tuần tự raw records trước khi tạo dict map. |
| blocker: Durable budget chấp nhận NaN | Thêm strict numeric validation trong `budget.py`, reject NaN/Inf/negatives, enforce `allow_nan=False`, xóa bỏ `cancel()`. |
| blocker: Subcommand `all` thiếu resume/calibration gây `AttributeError` | Thêm `set_defaults(resume=None, calibration=None)` vào parser `all` và fallback trong `cmd_all()`. |
| major: Notebook chưa bắt buộc kiểm checksum budget | Cập nhật Cell 15 bắt buộc kiểm tra path relative, SHA-256 checksum byte, và snapshot totals của budget. |
| major: Generation row làm mất attempts | Cập nhật `generation_record` và `_gen_case` ghi nhận `attempts`, `cost_usd_total`, và `attempt_ids`. |
| major: Fresh calibration reuse tạo linkage không nhất quán | Khóa reuse calibration trên fresh run, bắt buộc chạy fresh calibration với budget mới. |

---

## Files Modified & Created (delta revision 9)

- `backend/evaluation/budget.py` — Bổ sung strict numeric validation (`_is_positive_integer`, `_is_nonnegative_integer`, `_is_finite_nonnegative_number`), `allow_nan=False`, xóa `cancel()`, sửa logic `attempt_number`.
- `backend/evaluation/answer_eval.py` — Bổ sung `raw_validate_calibration_records()`, nạp/validate/normalize calibration rows, ghi nhận `attempts`, `cost_usd_total`, `attempt_ids` trong generation và judge records.
- `backend/evaluation/evaluator.py` — Khóa consent gate trước mọi thao tác cho cả fresh/resume, từ chối `--calibration` trên fresh run, fix parser/delegation cho subcommand `all`.
- `notebooks/07_evaluation.ipynb` — Cập nhật Cell 15 với strict budget path/checksum/totals validation, bảo đảm nbformat 4.5, outputs rỗng, `execution_count=null`.
- `backend/tests/test_evaluation_budget.py` — Mở rộng lên 22 deterministic tests (thêm test numeric validation NaN/Inf/negatives và no-refund API).
- `backend/tests/test_evaluation_controls.py` — Mở rộng lên 64 tests (thêm test raw calibration validation, 0-call summary rebuild, Cell 15 budget checksum/tamper, attempt history tracking).
- `backend/tests/test_evaluator_cli.py` — Mở rộng lên 7 tests (thêm test resume consent gate, fresh calibration rejection, `cmd_all` delegation mà không bị `AttributeError`).

---

## Commands Run (exact, fresh)

```bash
# từ backend/
uv run python -m py_compile evaluation/budget.py evaluation/artifacts.py \
  evaluation/answer_eval.py evaluation/evaluator.py \
  tests/test_evaluation_budget.py tests/test_evaluation_controls.py \
  tests/test_evaluator_cli.py

uv run python -m pytest tests/test_evaluation_budget.py \
  tests/test_evaluation_loader.py tests/test_evaluation_metrics.py \
  tests/test_evaluation_artifacts.py tests/test_retrieval_evaluation.py \
  tests/test_answer_evaluation.py tests/test_evaluation_controls.py \
  tests/test_evaluator_cli.py -q --tb=short
# -> 141 passed in 3.93s

# từ repo root
uv run --env-file .env python knowledge-base-hue/foods/evaluation/validate_tests.py
# -> PASS: 104 tests, all checks green

# notebook format check
uv run python -c "import json; nb=json.load(open('notebooks/07_evaluation.ipynb')); assert nb['nbformat']==4 and nb['nbformat_minor']==5; assert all(c['execution_count'] is None and len(c['outputs'])==0 for c in nb['cells'] if c['cell_type']=='code')"
# -> PASS (nbformat 4.5, execution_count null, outputs empty)

# Qdrant active collection verification
PYTHONPATH=backend uv run --env-file .env python -c "from backend.vectorstore.qdrant import get_client; from backend.core.settings_loader import load_settings; s=load_settings(); c=get_client(s['vector_database']['url'], s['vector_database']['timeout']); assert c.get_collection(s['vector_database']['collection_name']).points_count == 572"
# -> Qdrant collection hue_foods_e5_small_384: points_count = 572

codegraph sync . && codegraph status .   # -> ✓ Index is up to date
git diff --check                          # -> clean
```

---

## Tests And Verification

- **141 targeted tests (22 budget + 45 module + 64 controls + 7 CLI)** toàn bộ passed.
- Dataset validator 104/104; checksum `6d023e0a…`.
- Active Qdrant giữ nguyên 572 points (read-only verification).
- 0 paid provider calls thực hiện trong suốt Revision 9.
