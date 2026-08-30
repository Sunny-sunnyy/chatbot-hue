# Codex Review: Phase 8 Notebook 08b Retrieval and Fusion Benchmark

Decision: `ready_for_user_confirmation`
Reviewer: Codex
Date: `2026-08-30 +07`
Canonical guide: `guides/phase_8_benchmark_model_selection.md`
Implementation report:
`reports/phase_8_08b_retrieval_fusion_benchmark_implementation_report.md`

## 1. Phạm vi đã review

Reviewer đã review Correction Round 4 trên base
`93109c2e383f7f19554e2ceb03f10f8c199bc8ea`, documentation HEAD
`1fda0c24ebf6c329f549396901cf1d69765b903e` và current worktree.

Phạm vi gồm module/test 08b, source notebook 26 cells, bốn durable artifacts,
implementation report và final-review handoff. Reviewer tập trung vào hai
acceptance cuối: exact immutable/live reconciliation và bounded secret-safe
failure evidence, sau đó chạy fresh prescribed suite, source notebook với
Qdrant thật, negative probes, hash stability và diff-format check.

## 2. Findings

Không còn `blocker` hoặc `major` finding.

- `reconcile_sparse_benchmark` hiện fail-closed khi thiếu explicit `client` và
  dùng chung `build_expected_immutable_identity` với manifest creation. Fresh
  probe xác nhận missing client và immutable lexical/TF-IDF/fusion contract sai
  đều trả `complete=False`.
- Error output chỉ còn exception type và một bounded category do code sở hữu;
  raw provider payload không được đưa vào persisted message. Fresh probes với
  single quote, double quote, quoted Bearer và multiline traceback không làm lộ
  sentinel.
- Shared identity builder và bounded sanitizer trực tiếp hơn các validator/regex
  của vòng trước; không quan sát abstraction hoặc correction machinery dư cần
  chặn approval.

`minor`: sentence-transformers vẫn phát một `FutureWarning` về method lấy
embedding dimension trong test retrieval service. Kích thước/runtime hiện đúng;
warning này không thuộc behavior 08b và không chặn user confirmation.

## 3. Cách Reviewer chạy lại thật

Từ `backend/`, với Qdrant local và project `.env`:

```bash
PYTHONPATH=. HF_HUB_OFFLINE=1 \
UV_CACHE_DIR=/tmp/hue-rag-08b-review-uv-cache \
uv run --group evaluation --env-file ../.env python \
  /tmp/phase8_08b_round3_review_probe.py

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation --env-file ../.env python -m pytest \
  tests/test_sparse_benchmark.py tests/test_embedding_benchmark.py \
  tests/test_bm25.py tests/test_retrieval_service.py -q --tb=short
```

Từ repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase8-08b-test-uv-cache \
uv run --group evaluation jupyter nbconvert --to notebook --execute \
  notebooks/08b_retrieval_fusion_benchmark.ipynb \
  --output /tmp/reviewer_08b_round4_executed.ipynb \
  --ExecutePreprocessor.timeout=1800

git diff --check 93109c2e383f7f19554e2ceb03f10f8c199bc8ea
```

Reviewer còn kiểm notebook JSON, artifact line/record counts, SHA-256 trước/sau
suite và notebook, executed outputs cùng implementation-report metrics.

## 4. Kết quả quan sát

- Negative probe: missing explicit client `False`; wrong immutable contract
  `False`; bốn secret cases chỉ trả safe bounded descriptions.
- Prescribed suite: `85 passed`, một warning, `44.30s`.
- Repository notebook: 26 cells, 16 code cells, không output và mọi execution
  count là `null`.
- Temporary Run All: exit `0`; active production collection
  `hue_foods_e5_small_384` có 572 points; 20 cached settings được đọc đầy đủ.
- Reconciliation live: 5 BM25 parameter settings, 2 tokenizer settings,
  20 main settings, 70 calibration rows, 200 result rows và 900 case records;
  `complete=True`, BM25 finalist `None`, TF-IDF finalist `None`.
- Relationship evidence khớp artifact: Huydang dense control nDCG@5
  `0.8586956`, hybrid weighted `0.8307683`, delta `-0.0279273`; guardrail
  `-0.02` vì vậy fail-closed đúng thiết kế.
- Bốn durable artifact hashes không đổi qua suite và source notebook.
- `git diff --check` trên base: PASS.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không rerun full 20-setting retrieval/model matrix vì Correction Round
4 không đổi corpus, models, retrieval formulas, metrics hoặc durable evidence.
Notebook chạy exact live checkpoint/reconciliation path và kiểm toàn bộ isolated
TF-IDF collection; đây là reuse có chủ đích, không được gọi là fresh model run.

Không có paid API, reranker, generation hoặc production cutover trong 08b.
Reviewer không sửa runtime/implementation report/artifacts và không commit/push.

## 6. Decision và bước tiếp theo

Decision là `ready_for_user_confirmation`. Báo cáo dành cho user:

```text
reports/user_reports/phase_8_08b_retrieval_fusion_benchmark_user_report.md
```

Approval Closure Contract:

1. User xác nhận bằng câu:
   `Tôi xác nhận Notebook 08b của Giai đoạn 8.`
2. Sau xác nhận, closure chỉ được sửa cơ học:
   - report này để ghi user confirmation và ngày xác nhận;
   - user report 08b để chuyển trạng thái sang đã xác nhận;
   - `guides/phase_8_benchmark_model_selection.md` để ghi 08b approved và next
     boundary;
   - `session_prompt/Project_Status.md` để cập nhật row Phase 8/current action;
   - `session_prompt/CURRENT_HANDOFF.md` để tạo exact next-design handoff cho
     Notebook 08c.
3. Closure giữ nguyên runtime, tests, notebooks, artifacts, Qdrant collections,
   Golden V3, production config và kết luận không có 08b sparse finalist.
4. Phase 8 tổng thể vẫn `not_ready`; 08c implementation/run chỉ được mở sau
   design/spec/plan và user approval riêng.
5. Sau closure chạy `git diff --check` và kiểm đúng closure paths. Git
   authorization vẫn `none`; user confirmation không tự cấp quyền commit/push.

Guide giữ trạng thái hiện hành cho tới khi user xác nhận.

User đã xác nhận Notebook 08b của Giai đoạn 8 ngày `2026-08-30 +07`.
Approval closure đã hoàn tất: canonical guide, Project Status, user report và
current handoff được cập nhật; 08b hiện `approved`, Phase 8 tổng thể vẫn
`not_ready`, production giữ nguyên và next action chuyển sang research/design
exact Notebook 08c. Không có quyền commit/push nào được suy ra từ xác nhận;
quyền Git cho closure được user cấp riêng trong cùng yêu cầu xác nhận.
