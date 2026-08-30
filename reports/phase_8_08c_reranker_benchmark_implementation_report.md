# Implementation Report: Phase 8 Notebook 08c MiniLM Reranker Benchmark (Complexity Reset)

Implementer: Gemini (Antigravity)
Date: 2026-08-30 (+07)
Canonical guide:

```text
docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md
docs/superpowers/plans/2026-08-30-phase-8-08c-reranker-benchmark-implementation-plan.md
```

Review feedback addressed:
```text
reports/phase_8_08c_reranker_benchmark_codex_review.md
session_prompt/CURRENT_HANDOFF.md
```

## 1. Phạm vi & Mục tiêu Complexity Reset

Thực hiện trọn gói Complexity Reset đã được duyệt:
1. **Thiết lập Single Numeric Normalization Boundary**:
   - Thêm các helper chuẩn xác `_parse_finite_float`, `_check_finite_close`, `_check_positive_finite`, `_check_finite_int` trong `backend/evaluation/reranker_benchmark.py`.
   - Toàn bộ các trường số học bắt buộc (per-case metrics, per-case latencies, summary metrics/deltas, bootstrap CIs, summary p50/p95, resource metrics) đều đi qua parser này để từ chối triệt để:
     - Giá trị rỗng (`""`, `None`)
     - Giá trị không thể parse số
     - Giá trị IEEE non-finite: `NaN`, `+Inf`, `-Inf`
     - Sai lệch vượt quá tolerance so với giá trị recomputed
2. **Loại bỏ hoàn toàn Coercion rủi ro**:
   - Không dùng `or 0.0` để coerce missing/blank thành 0.
   - Kiểm tra rạch ròi giữa trường bắt buộc có số và trường bắt buộc phải blank theo schema.
3. **Consolidation & Parameterization của Test Suite**:
   - Refactor toàn bộ các tamper tests trong `backend/tests/test_reranker_benchmark.py` bằng helper `_prepare_test_artifacts(tmp_path)`.
   - Giữ nguyên 100% độ bao phủ của 10 tamper boundaries trước đó.
   - Bổ sung 30 test probes tham số hóa (`@pytest.mark.parametrize`) kiểm tra `NaN`, `+Inf`, `-Inf` trên toàn bộ các vị trí số học trọng yếu.
   - Tổng cộng: **61 passed tests**.
4. **Bảo toàn bất biến (Immutable Boundaries)**:
   - Giữ nguyên 100% runtime producer (`load_runtime_reranker`, `run_reranker_input`, `run_all_reranker_inputs`).
   - Giữ nguyên `notebooks/08c_reranker_benchmark.ipynb`.
   - Giữ nguyên durable artifacts (`phase8_reranker_results.csv`, `phase8_reranker_cases.jsonl`).
   - Giữ nguyên concurrent modification tại `notebooks/08b_retrieval_fusion_benchmark.ipynb`.
   - Không chạy lại MiniLM model benchmark.

## 2. File Scope & Thay đổi

- `backend/evaluation/reranker_benchmark.py`: Tích hợp numeric normalization helpers vào `reconcile_reranker_artifacts()`.
- `backend/tests/test_reranker_benchmark.py`: Refactor DRY test setup và bổ sung non-finite parameterization (61 tests).
- `reports/phase_8_08c_reranker_benchmark_implementation_report.md`: Cập nhật báo cáo nghiệm thu Complexity Reset.
- `session_prompt/CURRENT_HANDOFF.md`: Cập nhật handoff packet `final_review` cho Reviewer.

## 3. Bằng chứng kiểm tra

### 3.1 Fresh Evidence (Tạo mới trong Complexity Reset)
1. **Focused deterministic tests (61 passed)**:
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-reset-uv-cache uv run python -m pytest tests/test_reranker_benchmark.py -q --tb=short -s
   ```
   Kết quả: `61 passed, 1 warning in 30.56s`.
   Bao gồm:
   - 10 tamper tests: experiment_version, summary metric mismatch, case metric contradiction, flag tamper, failed status, bootstrap CI mismatch, repetitions mismatch, ranking stability mismatch, state order mismatch, relevant rank mismatch, pre-rerank chunk identity, minilm top 5 subset, summary p95 latency, negative case latency, negative cold_load_ms.
   - 30 non-finite tests: `NaN`, `+Inf`, `-Inf` trên per-case metrics, per-case latencies, summary metrics, summary deltas, bootstrap CIs, summary latencies, resource metrics.

2. **Reconciliation trên Untampered Artifacts**:
   ```bash
   PYTHONPATH=. HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-reset-uv-cache uv run python -c "from evaluation.reranker_benchmark import reconcile_reranker_artifacts; r=reconcile_reranker_artifacts(); assert r.complete and r.summary_rows == 60 and r.case_records == 135 and not r.errors"
   ```
   Kết quả: `complete=True`, `summary_rows=60`, `case_records=135`, `errors=()`.

3. **Định dạng Git Diff**:
   ```bash
   git diff --check
   ```
   Kết quả: Exit 0, không có formatting issues.

### 3.2 Reused Evidence (Từ Live Run Round 2)
- **Live single-load notebook execution**: Current durable artifacts đến từ live Run All cuối cùng trong cùng implementation series (`cold_load_ms` 11163.306627, RSS 931.2890625 -> 956.875 MB, peak RSS 1118.96484375 MB, exit code 0). Closure Reviewer đã reconcile và rerun focused suite trên exact artifacts này.
- **Durable artifacts**: `evaluation/results/phase8_reranker_results.csv` (60 rows) và `evaluation/results/phase8_reranker_cases.jsonl` (135 records) giữ nguyên từ live run thật.
- **Tài nguyên bất biến**: SHA256 hashes của Golden V3 full, Golden V3 smoke, 572 chunks corpus, markdown chunker, artifact 08a/08b và `notebooks/08b_retrieval_fusion_benchmark.ipynb` được bảo toàn 100%.

## 4. Kết quả quan sát (Reused from Live Run)

| Setting | Input Key | State | Recall@5 | MRR@5 | nDCG@5 | ΔnDCG@5 | 95% Bootstrap CI ΔnDCG | Eligible | Clear Gain | Production Safety | Warm p50 / p95 (ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | `dense__e5-small-384` | `no-rerank`<br>`minilm` | 0.8185<br>0.7852 | 0.7748<br>0.6944 | 0.7425<br>0.6723 | <br>-0.0703 | <br>[-0.1349, -0.0083] | <br>`False` | <br>`False` | <br>— | <br>246.13 / 538.79 |
| **2** | `dense__huydang-dek21-embedding-768` | `no-rerank`<br>`minilm` | 0.8370<br>0.8741 | 0.7211<br>0.7204 | 0.7164<br>0.7228 | <br>+0.0065 | <br>[-0.0891, +0.1057] | <br>`False` | <br>`False` | <br>— | <br>231.58 / 487.66 |
| **3** | `hybrid-bm25-weighted__huydang-dek21-embedding-768` | `no-rerank`<br>`minilm` | 0.9111<br>0.8407 | 0.7674<br>0.7230 | 0.7655<br>0.7050 | <br>-0.0605 | <br>[-0.1496, +0.0243] | <br>`False` | <br>`False` | <br>`False` | <br>248.27 / 481.02 |

## 5. Đối chiếu Acceptance Criteria Complexity Reset

1. **Single finite numeric normalization boundary**: ĐẠT (`_parse_finite_float`, `_check_finite_close`, `_check_positive_finite`, `_check_finite_int`).
2. **Không lọt lưới IEEE NaN / Inf**: ĐẠT (từ chối 100% các giá trị non-finite).
3. **Consolidated & parameterized test suite**: ĐẠT (61 tests pass trong ~30s).
4. **Untampered artifacts reconcile**: ĐẠT (`complete=True, summary_rows=60, case_records=135, errors=()`).
5. **Bảo toàn bất biến**: ĐẠT (không đổi runtime producer, notebook, artifacts, concurrent files).
6. **Git diff check**: ĐẠT (exit 0).

## 6. Handoff cho Reviewer

- **Lệnh Reviewer chạy lại (deterministic checks)**:
  ```bash
  HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-reset-uv-cache uv run python -m pytest tests/test_reranker_benchmark.py -q --tb=short -s
  PYTHONPATH=. HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-08c-reset-uv-cache uv run python -c "from evaluation.reranker_benchmark import reconcile_reranker_artifacts; r=reconcile_reranker_artifacts(); assert r.complete and r.summary_rows == 60 and r.case_records == 135 and not r.errors"
  git diff --check
  ```
- **Trạng thái quyết định**: Bàn giao cho Reviewer đánh giá độc lập.
