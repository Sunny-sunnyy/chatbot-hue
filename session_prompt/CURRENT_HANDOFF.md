# Bàn giao hiện hành

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: 93109c2e383f7f19554e2ceb03f10f8c199bc8ea
Head commit: worktree
Risk level: high
Git authorization: none
Sub-agent authorization: none

## 1. Mục tiêu duy nhất

Thực hiện exact Notebook 08b retrieval/fusion work package theo approved spec và
plan, bao gồm implementation, focused/regression verification, real isolated
Qdrant evaluation theo batch, durable artifacts, notebook sạch và implementation
report. Kết thúc bằng `final_review` handoff cho Reviewer; Implementer không tự
approve hoặc cutover.

## 2. Canonical requirements

```text
docs/superpowers/specs/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-design.md
docs/superpowers/plans/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-implementation-plan.md
guides/phase_8_benchmark_model_selection.md
```

Spec và plan đã được user duyệt ngày `2026-08-29 +07`. Không brainstorm hoặc
viết lại architecture. Nếu source/API thật chứng minh contract không thực hiện
được, dừng và trả Reviewer/user thay vì tự đổi requirement.

## 3. Exact authorized scope

Implementer được phép:

- thực hiện Tasks 1–9 trong approved plan theo TDD;
- thêm Underthesea đúng evaluation dependency group và cập nhật `uv.lock`;
- tạo backend evaluation module, focused tests và canonical Notebook 08b;
- tạo/reuse đúng isolated TF-IDF collection có deterministic approved name khi
  `ALLOW_EXPERIMENT_MUTATION=true`;
- chạy ba real 08a dense models, canonical 572 chunks và 45 Golden V3 cases;
- chạy đủ ba repetitions cho exact 20-setting matrix;
- ghi bốn approved artifacts dưới `evaluation/results/`;
- tạo exact 08b implementation report và final-review handoff.

Không được phép:

- sửa active production collection, production settings/startup/retrieval,
  runtime BM25, Golden V3 hoặc ba 08a collections;
- thêm model/tokenizer/fusion grid, reranker, generation, paid API hoặc cutover;
- mở rộng task sang `knowledge-base-hue/festivals`;
- xóa durable artifacts, TF-IDF review collection, 08a collections, model cache,
  repository data hoặc production resources;
- commit hoặc push trong implementation session nếu user chưa cấp Git authority
  mới.

Festivals là một queued Reviewer task riêng cho session khác, không phải input
hoặc acceptance criterion của 08b.

## 4. Incremental execution contract

Implementer tự chọn một, năm, mười hoặc số batch phù hợp với RAM/VRAM/disk và
runtime quan sát được. Không cần hoàn tất benchmark trong một process/kernel.

Mỗi batch phải:

1. khai báo exact setting keys theo canonical order;
2. validate exact manifest/provenance trước resume;
3. persist atomically sau từng completed setting;
4. ghi đúng completed/partial/failed/skipped;
5. release models, clients và large objects trước batch tiếp theo;
6. chỉ xóa task-created ephemeral paths có target chính xác;
7. giữ nguyên models, formulas, depths, repetitions, metrics và gates.

Final shortlist chỉ được tính sau khi reconcile đủ 5 BM25 parameter settings, 2
tokenizer settings, 20 main settings, 200 summary rows, 900 setting/case records
và TF-IDF collection 572 points.

## 5. Expected implementation paths

```text
pyproject.toml
uv.lock
backend/evaluation/sparse_benchmark.py
backend/tests/test_sparse_benchmark.py
notebooks/08b_retrieval_fusion_benchmark.ipynb
evaluation/results/phase8_sparse_manifest.json
evaluation/results/phase8_sparse_calibration.csv
evaluation/results/phase8_sparse_results.csv
evaluation/results/phase8_sparse_cases.jsonl
reports/phase_8_08b_retrieval_fusion_benchmark_implementation_report.md
session_prompt/CURRENT_HANDOFF.md
```

Any additional changed path requires an exact plan dependency or renewed user
approval. Preserve all pre-existing user changes.

## 6. Required workflow

After bootstrap, use the plan-required execution workflow:

1. `executing-plans` for task/batch checkpoints;
2. `test-driven-development` for behavior changes;
3. `systematic-debugging` only after a real reproducible failure;
4. `verification-before-completion` before the final handoff;
5. `requesting-code-review` for the Implementer self-review boundary.

Also apply the project-local `risk-gated-agent-review` and
`practical-project-coding` skills required by `IMPLEMENTER_WORKFLOW.md`.

## 7. Review Contract

Reviewer must independently:

1. validate this base commit, exact changed/untracked paths and full diff;
2. map implementation to every approved spec section and plan task;
3. reject scope creep, runtime duplication and unjustified checkpoint/audit
   machinery;
4. run `git diff --check` and the focused/relevant regression commands;
5. execute or inspect the exact real temporary-notebook path required by the
   plan, using checkpoint reuse where provenance is unchanged;
6. reconcile five parameter settings, two tokenizer settings, 20 main settings,
   200 result rows and 900 per-case records;
7. independently recompute one BM25 score, one TF-IDF norm, one RRF result, one
   weighted fusion result, one metric and one category gate;
8. validate the exact isolated TF-IDF schema/provenance/572 points;
9. prove active collection/config and 08a collections remain unchanged;
10. confirm notebook source parses with empty outputs and null execution counts;
11. verify batch history, failures, limitations and zero-to-two 08b finalists
    agree across notebook, artifacts and implementation report.

No fake/mock/replay/old output counts as integration PASS.

## 8. Stop conditions

Stop and return to Reviewer/user when:

- approved formula, API, dependency or collection contract is incompatible with
  the real environment and fixing it changes architecture or scope;
- exact 08a/corpus/Golden provenance fails;
- active production state changes;
- completion requires destructive cleanup, paid API, provider/model change,
  festivals data, Golden changes or another unapproved path;
- four correction rounds later still leave blocker/major findings.

Otherwise continue through safe in-scope batches until the exact plan is
complete, then create the implementation report and `final_review` handoff.
