# Phase 7 Post-Simplicity Correction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove collection selection from public answer evaluation, clean Notebook 07, and produce fresh 20-question verification evidence without changing Phase 7 semantics or datasets.

**Architecture:** Keep the shared `build_services()` composition root and the existing four-module evaluation package. Answer batch/UI construct services from configured active settings only; retrieval retains the already-approved exact collection override. Verification uses the existing real integration path and a temporary executed notebook.

**Tech Stack:** Python 3.12, asyncio, Gradio, OpenAI Agents SDK, Qdrant, pytest, Jupyter/nbconvert, uv.

## Global Constraints

- Read `session_prompt/Session_Prompt.md`, `session_prompt/Project_Status.md`, `session_prompt/IMPLEMENTER_WORKFLOW.md`, the canonical Phase 7 guide, and the approved design before editing.
- Run `git status --short` and exact scoped diffs before editing; preserve all unrelated dirty-worktree changes.
- Active `hue_foods_e5_small_384` is read-only. Tests may mutate only the guarded test collection already owned by the test suite.
- Real online Qdrant and paid OpenAI calls in this approved Phase 7 correction are allowed. Do not expose secrets.
- Do not use mocks, fake responses, replayed outputs, or prior artifacts as fresh evidence.
- Do not edit `test2.jsonl`, `tests.jsonl`, `validate_tests.py`, metrics, prompts, models, providers, retrieval semantics, or generation semantics.
- Do not run the full paid 104-answer batch. Use the current 20-question smoke set.
- Do not add a signature/mechanism-only test. Existing real integration coverage plus explicit source/signature inspection is the approved evidence.
- Do not add abstractions, wrappers, retries, fallbacks, cost logic, run packages, or dependencies.
- Implementer must not modify canonical guides, project status, user reports, commit, or push.

---

### Task 1: Restrict collection override to retrieval-only public paths

**Files:**
- Modify: `backend/evaluation/eval.py`
- Modify: `backend/evaluation/evaluator.py`
- Inspect only: `backend/tests/test_evaluation.py`
- Inspect only: `backend/evaluation/retrieval_comparison.py`

**Interfaces:**
- Consumes: `build_services(profile: str = "dense_only", collection_name: str | None = None) -> EvaluationServices`.
- Produces: `run_answer_batch(test_path=DEFAULT_TEST_FILE, concurrency=3, profile="dense_only", progress=None) -> tuple[list[dict], dict]` with no collection override.
- Produces: `run_answer_ui(test_path, concurrency, progress=gr.Progress())` with no collection override.
- Preserves: `run_retrieval_batch(..., collection_name=None)` and `run_retrieval_ui(..., collection_name=None)`.

- [ ] **Step 1: Record the exact pre-change surface**

Run from repository root:

```bash
rg -n "def build_services|def run_retrieval_batch|def run_answer_batch|def run_retrieval_ui|def run_answer_ui|collection_name" backend/evaluation backend/tests/test_evaluation.py
```

Expected: `collection_name` appears in both answer public functions before the
change; retrieval comparison and guarded service construction also use it.

- [ ] **Step 2: Remove the option from answer batch only**

Change `run_answer_batch()` in `backend/evaluation/eval.py` to this signature
and service construction while leaving its remaining body unchanged:

```python
async def run_answer_batch(
    test_path: str | Path = DEFAULT_TEST_FILE,
    concurrency: int = 3,
    profile: str = "dense_only",
    progress=None,
) -> tuple[list[dict], dict]:
    tests = load_tests(test_path)
    services = build_services(profile)
```

- [ ] **Step 3: Remove the option from answer UI only**

Change `run_answer_ui()` in `backend/evaluation/evaluator.py` to:

```python
async def run_answer_ui(test_path, concurrency, progress=gr.Progress()):
    rows, summary = await run_answer_batch(
        test_path, concurrency, "dense_only", progress
    )
    table = format_table(rows, ANSWER_COLUMNS)
    return summary_text("Kết quả câu trả lời", summary, ANSWER_RESULTS_FILE), table
```

Do not change `run_retrieval_ui()`.

- [ ] **Step 4: Compile the affected modules**

Run from repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run python -m py_compile \
  backend/evaluation/eval.py backend/evaluation/evaluator.py
```

Expected: exit code 0 with no traceback.

- [ ] **Step 5: Verify the final public surface without adding a test**

Run:

```bash
rg -n "def run_retrieval_batch|def run_answer_batch|def run_retrieval_ui|def run_answer_ui|collection_name" backend/evaluation/eval.py backend/evaluation/evaluator.py backend/evaluation/retrieval_comparison.py
```

Expected: answer batch/UI signatures and calls contain no `collection_name`;
retrieval batch/UI, shared composition root, and retrieval comparison retain it.

### Task 2: Clean and verify canonical Notebook 07

**Files:**
- Modify mechanically: `notebooks/07_evaluation.ipynb`
- Create outside repository: `/tmp/07_evaluation-phase7-correction.ipynb`

**Interfaces:**
- Consumes: the existing public Phase 7 evaluation functions.
- Produces: a canonical notebook with null execution counts and empty outputs.
- Produces: a temporary executed notebook as live evidence.

- [ ] **Step 1: Clear canonical notebook outputs mechanically**

Run from repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run jupyter nbconvert \
  --ClearOutputPreprocessor.enabled=True --inplace notebooks/07_evaluation.ipynb
```

Expected: notebook structure remains intact and stored outputs are removed.

- [ ] **Step 2: Validate notebook structure and cleanliness**

Run:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run python -c 'import nbformat; p="notebooks/07_evaluation.ipynb"; n=nbformat.read(p, 4); nbformat.validate(n); code=[c for c in n.cells if c.cell_type=="code"]; assert all(c.execution_count is None for c in code); assert all(not c.outputs for c in code); print(len(n.cells), "cells; canonical notebook clean")'
```

Expected: exit code 0 and a clean-notebook message.

- [ ] **Step 3: Execute Notebook 07 to a temporary file**

Run from repository root with real environment configuration:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run --env-file .env \
  jupyter nbconvert --execute --to notebook notebooks/07_evaluation.ipynb \
  --output /tmp/07_evaluation-phase7-correction.ipynb \
  --ExecutePreprocessor.timeout=1800
```

Expected: exit code 0. This command uses real Qdrant and paid OpenAI calls and
may refresh the two fixed CSVs with the 20-question smoke results.

- [ ] **Step 4: Recheck that execution did not dirty canonical outputs**

Repeat the structural command from Step 2.

Expected: canonical notebook remains clean because execution output was written
to `/tmp`.

### Task 3: Run focused verification and write the implementation report

**Files:**
- Verify: `backend/tests/test_evaluation.py`
- Verify generated: `backend/evaluation/retrieval_results.csv`
- Verify generated: `backend/evaluation/answer_results.csv`
- Create: `reports/phase_7_post_simplicity_correction_implementation_report.md`

**Interfaces:**
- Consumes: corrected answer API and existing retrieval-only override.
- Produces: real focused test evidence, ordered 20-row CSV artifacts, and an implementation report for independent Reviewer execution.

- [ ] **Step 1: Run the focused real integration suite**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run --env-file ../.env \
  python -m pytest tests/test_evaluation.py -q --tb=short -s
```

Expected: all existing Phase 7 tests pass. Record the exact count, duration,
warnings, provider failures, and any skipped tests; do not invent an expected
test count in the report.

- [ ] **Step 2: Verify current CSV row count and input ordering**

Run from repository root:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase7-correction-uv-cache uv run python -c 'import csv, json; from pathlib import Path; q=Path("knowledge-base-hue/foods/evaluation/test2.jsonl"); expected=[json.loads(line)["question"] for line in q.open(encoding="utf-8") if line.strip()]; base=Path("backend/evaluation"); files=[base/"retrieval_results.csv", base/"answer_results.csv"]; rows=[list(csv.DictReader(p.open(encoding="utf-8"))) for p in files]; assert all(len(r)==20 for r in rows); assert all([x["question"] for x in r]==expected for r in rows); print([(p.name, len(r)) for p,r in zip(files,rows)], "ordered")'
```

Expected: both CSVs report 20 ordered rows. Model/provider row errors are
allowed only when preserved truthfully in the CSV and implementation report.

- [ ] **Step 3: Audit scope and whitespace**

Run:

```bash
git diff --check -- backend/evaluation/eval.py backend/evaluation/evaluator.py notebooks/07_evaluation.ipynb backend/evaluation/retrieval_results.csv backend/evaluation/answer_results.csv reports/phase_7_post_simplicity_correction_implementation_report.md
git status --short
```

Expected: no new whitespace errors in hand-edited source/report files. CSV CRLF
may be reported by Git as trailing whitespace; record it rather than rewriting
CSV semantics solely to satisfy `git diff --check`. Status must show no dataset,
validator, config, provider/model, or unrelated file changed by this correction.

- [ ] **Step 4: Write the implementation report**

First capture the report timestamp:

```bash
TZ=Asia/Bangkok date '+%Y-%m-%d %H:%M:%S %z'
```

Create `reports/phase_7_post_simplicity_correction_implementation_report.md`
with these exact sections:

```markdown
# Phase 7 Post-Simplicity Correction Implementation Report

Date: paste the exact output of the timestamp command above
Status: `ready_for_review`

## Scope implemented
## Exact files changed
## Commands executed
## Observed test and Notebook results
## CSV row counts, summaries, and row errors
## Scope audit and unchanged contracts
## Handoff to Reviewer
```

Replace the timestamp and all evidence with observed values. Explicitly state:

- answer batch/UI no longer accepts collection override;
- retrieval-only override remains;
- canonical Notebook 07 is clean and temporary Run All result path;
- whether all focused tests passed;
- both CSV row counts and any real row errors;
- no 104-answer batch or dataset change occurred;
- active Hue collection stayed read-only;
- no commit or push was performed.

- [ ] **Step 5: Stop for Reviewer**

Do not edit canonical guides/status/user report. Do not commit or push. Return
the implementation report path, exact changed-file list, commands, results, and
any failure to the user for Reviewer handoff.
