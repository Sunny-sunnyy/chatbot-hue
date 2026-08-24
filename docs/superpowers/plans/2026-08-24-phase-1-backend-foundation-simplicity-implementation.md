# Phase 1 Backend Foundation Simplicity Implementation Plan

> **For the Implementer:** REQUIRED SUB-SKILL: start with `using-superpowers`,
> then use `executing-plans` to execute this plan task by task. Use
> `systematic-debugging` if a verification step fails and
> `verification-before-completion` before the handoff.

**Goal:** Connect the existing logging configuration to real Hue RAG entrypoints
and remove Phase 1 artifacts that duplicate code, without changing RAG behavior.

**Architecture:** Keep one direct YAML loader, one `setup_logging()` function
and one shared `RetrievedDocument`. Runtime entrypoints configure logging before
their existing work; child modules continue using ordinary Python loggers.

**Tech Stack:** Python 3.13, PyYAML, Python logging, FastAPI, Gradio, pytest,
Qdrant, local `intfloat/multilingual-e5-small`, `uv`.

## Global constraints

- Read `session_prompt/IMPLEMENTER_WORKFLOW.md`, `session_prompt/Session_Prompt.md`,
  `session_prompt/Project_Status.md`, `guides/phase_1_backend_skeleton.md` and
  the approved design before editing.
- Run `git status --short` and inspect the exact diffs first. Preserve every
  unrelated change in the dirty worktree.
- Code, docstrings, comments and symbols use clear English. The implementation
  and report remain small and direct.
- Do not add a config class, logging wrapper, factory, middleware, decorator,
  retry, rotation, remote logging, dependency or test-only runtime hook.
- Do not change `settings.yaml`, `logging.yaml`, `core/schema.py`, retrieval
  profiles, provider/model values or any Phase 2–7 business behavior.
- Do not mutate `hue_foods_e5_small_384`. Tests may mutate only the marked
  isolated collections already guarded by `backend/tests/conftest.py`.
- Do not use mock/fake services, replayed outputs or prior results as completion
  evidence.
- Do not run the paid 104-question Phase 7 evaluation; this scope cannot change
  RAG quality.
- Do not edit canonical guides, role workflows, Project Status, living
  simplicity review, Codex review or historical reports.
- Do not stage, commit or push.

## File map

**Modify:**

- `backend/core/settings_loader.py` — load YAML and validate the active profile
  in one public function.
- `backend/api/app.py` — configure logging at FastAPI lifespan startup.
- `backend/ingestion/pipeline.py` — configure logging in the CLI entrypoint.
- `backend/evaluation/evaluator.py` — configure logging in the Gradio
  entrypoint.

**Delete:**

- `notebooks/01_backend_foundation.ipynb` — smoke/validation notebook with no
  necessary learning flow.
- `backend/config/README_config.md` — duplicates YAML comments and phase guides.

**Create:**

- `reports/phase_1_backend_skeleton_simplicity_implementation_report.md` — new
  six-section report; do not overwrite the historical Phase 1 report.

**Do not modify:**

- `backend/config/settings.yaml`
- `backend/config/logging.yaml`
- `backend/core/logging_setup.py`
- `backend/core/schema.py`
- `backend/evaluation/retrieval_results.csv`
- `backend/evaluation/answer_results.csv`

The current Phase 4 and Phase 5 guides and historical reports may still mention
`backend/config/README_config.md`. Implementer must not edit them. Record this
as a Reviewer-owned downstream documentation follow-up, not as a runtime issue.

---

### Task 1: Make settings loading direct and remove Phase 1 duplicate artifacts

**Files:**

- Modify: `backend/core/settings_loader.py:1-25`
- Delete: `notebooks/01_backend_foundation.ipynb`
- Delete: `backend/config/README_config.md`

**Interfaces:**

- Consumes: `SETTINGS_PATH: pathlib.Path`, canonical YAML mapping.
- Produces: `load_settings() -> dict`; unchanged public behavior.

- [ ] **Step 1: Capture the exact Before state**

Run from the repository root:

```bash
git status --short
git diff -- backend/core/settings_loader.py notebooks/01_backend_foundation.ipynb backend/config/README_config.md
```

Expected: inspect and preserve any pre-existing changes. Stop if any of these
three files contains an unrelated user change that overlaps this task.

- [ ] **Step 2: Run the public settings smoke before editing**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run python -c 'from core.settings_loader import load_settings; s = load_settings(); print(s["active_profile"]); print([(n, p["retrieval_mode"], p["use_bm25"], p["use_reranker"]) for n, p in s["profiles"].items()])'
```

Expected output includes:

```text
dense_only
('dense_only', 'dense', False, False)
('hybrid_no_rerank', 'hybrid', True, False)
('hybrid_rerank', 'hybrid', True, True)
```

- [ ] **Step 3: Replace the single-use validation helper with direct code**

Make `backend/core/settings_loader.py` exactly follow this structure:

```python
"""Load application settings from config/settings.yaml."""
from pathlib import Path

import yaml


BACKEND_DIR = Path(__file__).resolve().parents[1]
SETTINGS_PATH = BACKEND_DIR / "config" / "settings.yaml"


def load_settings():
    """Load settings and reject an unknown active retrieval profile."""
    with SETTINGS_PATH.open() as file:
        settings = yaml.safe_load(file)
    active_profile = settings.get("active_profile")
    profiles = settings.get("profiles", {})
    if active_profile not in profiles:
        raise ValueError(
            f"Unknown active_profile: {active_profile!r}. "
            f"Valid profiles: {sorted(profiles)}"
        )
    return settings
```

Do not add a path argument or validation for unrelated config fields.

- [ ] **Step 4: Delete the two approved artifacts**

Use `apply_patch` to delete:

```text
notebooks/01_backend_foundation.ipynb
backend/config/README_config.md
```

Do not edit historical reports that describe their previous existence.

- [ ] **Step 5: Verify the public settings behavior and removals**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run python -m py_compile core/settings_loader.py
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run python -c 'from core.settings_loader import load_settings; s = load_settings(); assert s["active_profile"] == "dense_only"; assert list(s["profiles"]) == ["dense_only", "hybrid_no_rerank", "hybrid_rerank"]; print("settings ok")'
cd ..
test ! -e notebooks/01_backend_foundation.ipynb
test ! -e backend/config/README_config.md
```

Expected:

```text
settings ok
```

All commands exit `0`. Do not add a persistent test file for this direct
refactor.

---

### Task 2: Activate existing logging at the three real entrypoints

**Files:**

- Modify: `backend/api/app.py:15-50`
- Modify: `backend/ingestion/pipeline.py:1-5,95-98`
- Modify: `backend/evaluation/evaluator.py:1-14,69-70`

**Interfaces:**

- Consumes: `core.logging_setup.setup_logging() -> None`.
- Produces: the same API, ingestion and evaluation entrypoints with logging
  configured before runtime work.

- [ ] **Step 1: Verify the existing logging function with real file output**

Run from `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run python -c 'import logging; from core.logging_setup import LOGS_DIR, LOG_FILE_NAME, setup_logging; setup_logging(); logging.getLogger("retrieval").info("phase1 logging baseline"); path = LOGS_DIR / LOG_FILE_NAME; print(path); print(path.exists())'
```

Expected: the message appears on the console, the printed path ends with
`backend/logs/application.log`, and the final line is `True`.

- [ ] **Step 2: Configure logging at FastAPI lifespan startup**

Add this import to `backend/api/app.py`:

```python
from core.logging_setup import setup_logging
```

Make logging the first action inside the existing lifespan:

```python
@asynccontextmanager
async def lifespan(app):
    setup_logging()
    retrieval_service = None
    retrieval_ready = False
```

Do not call `setup_logging()` at module import time or inside `create_app()`
outside the lifespan.

- [ ] **Step 3: Configure logging in the ingestion CLI entrypoint**

Add this import to `backend/ingestion/pipeline.py`:

```python
from core.logging_setup import setup_logging
```

Replace the existing `main()` body with:

```python
def main():
    """Run ingestion with settings from disk and print the summary."""
    setup_logging()
    print(run_ingestion())
```

Keep `import logging` because the module-level logger still uses it. Do not run
this CLI against the active collection.

- [ ] **Step 4: Configure logging in the evaluation UI entrypoint**

Add this import to `backend/evaluation/evaluator.py`:

```python
from core.logging_setup import setup_logging
```

Replace `main()` with:

```python
def main():
    setup_logging()
    build_app().launch(inbrowser=True)
```

Do not change the Gradio UI, profiles, handlers, CSV files or evaluation logic.

- [ ] **Step 5: Compile and inspect the hookup**

```bash
cd backend
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run python -m py_compile core/settings_loader.py core/logging_setup.py api/app.py ingestion/pipeline.py evaluation/evaluator.py
rg -n 'setup_logging' core/logging_setup.py api/app.py ingestion/pipeline.py evaluation/evaluator.py
```

Expected: compile exits `0`; `rg` shows one definition and one call/import pair
in each of the three entrypoint modules. There is no module-level call in
`api/app.py`.

- [ ] **Step 6: Start the real API and inspect health/logging**

From `backend/`, start the server in a terminal:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8011
```

In another terminal:

```bash
curl --fail --silent http://127.0.0.1:8011/health
```

Expected: HTTP succeeds with JSON containing `components.app = "alive"`.
With real Qdrant, cached E5 and the configured API key available, expect
`status = "ok"`, Qdrant/retrieval `ready` and generator `configured`. Record
the actual output if an external component is unavailable; do not hide a
degraded result. Confirm `backend/logs/application.log` receives the startup
messages, then stop Uvicorn with `Ctrl-C`.

- [ ] **Step 7: Start the real evaluation UI far enough to verify logging**

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run --env-file ../.env python -m evaluation.evaluator
```

Expected: Gradio reports a local URL and logging is configured without an
exception. Do not click either paid evaluation button for this Phase 1 check.
Stop the process with `Ctrl-C` after observing startup.

---

### Task 3: Run real downstream verification and write the handoff

**Files:**

- Create: `reports/phase_1_backend_skeleton_simplicity_implementation_report.md`
- Verify only: `backend/evaluation/retrieval_results.csv`
- Verify only: `backend/evaluation/answer_results.csv`

**Interfaces:**

- Consumes: the simplified loader and three logging-enabled entrypoints.
- Produces: fresh observed evidence for independent Reviewer verification.

- [ ] **Step 1: Record the active collection count before tests**

From `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s = load_settings(); c = client_from_settings(s); n = s["vector_database"]["collection_name"]; print(n, c.count(n, exact=True).count)'
```

Expected:

```text
hue_foods_e5_small_384 572
```

Stop if the active collection name differs; do not mutate it.

- [ ] **Step 2: Run the affected live integration tests**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run --env-file ../.env python -m pytest tests/test_startup.py tests/test_api_chat.py tests/test_ingestion_pipeline.py tests/test_evaluation.py -q --tb=short
```

Expected: all selected tests pass using real Qdrant, local models and provider
APIs where the tests require them. The suite may create/delete only marked
`hue_rag_live_test_...` collections. Record the exact pass count and warnings.

If a test fails, use `systematic-debugging`; do not weaken assertions, add a
fake dependency or broaden runtime scope.

- [ ] **Step 3: Run the complete backend suite**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run --env-file ../.env python -m pytest tests -q --tb=short
```

Expected: the full suite passes. Record the fresh count and warnings rather
than copying the old `222 passed` baseline.

- [ ] **Step 4: Prove the active collection and Phase 7 outputs were preserved**

```bash
UV_CACHE_DIR=/tmp/hue-rag-phase1-uv-cache uv run python -c 'from core.settings_loader import load_settings; from vectorstore.qdrant import client_from_settings; s = load_settings(); c = client_from_settings(s); n = s["vector_database"]["collection_name"]; print(n, c.count(n, exact=True).count)'
cd ..
git diff -- backend/evaluation/retrieval_results.csv backend/evaluation/answer_results.csv
```

Expected: active collection remains `hue_foods_e5_small_384 572`; the CSV diff
is empty. Do not run the 104-question evaluation.

- [ ] **Step 5: Run repository hygiene checks**

From the repository root:

```bash
git diff --check
rg -n '^(<<<<<<<|=======|>>>>>>>)' backend docs guides reports session_prompt || true
git status --short
git diff -- backend/core/settings_loader.py backend/api/app.py backend/ingestion/pipeline.py backend/evaluation/evaluator.py notebooks/01_backend_foundation.ipynb backend/config/README_config.md
```

Expected: no whitespace errors or merge markers. Inspect the final diff and
confirm all unrelated dirty-worktree changes are untouched.

- [ ] **Step 6: Write the new six-section implementation report**

Create
`reports/phase_1_backend_skeleton_simplicity_implementation_report.md` using
`session_prompt/TEMPLATE_IMPLEMENTATION_REPORT.md` with:

1. exact approved and implemented scope;
2. the four modified runtime files and two deleted artifacts;
3. only commands actually run, including real dependencies used;
4. fresh observed results, active collection count and logging observations;
5. failures, degraded/skipped steps and the stale Phase 4/5 guide references;
6. a Reviewer handoff naming the source files and real commands to rerun.

Write `Notebook: not applicable for Phase 1 by approved design`. Do not modify
the living simplicity review or historical Phase 1 reports.

- [ ] **Step 7: Final scope check**

```bash
git status --short
git diff --check
```

Expected changed implementation scope:

```text
backend/core/settings_loader.py
backend/api/app.py
backend/ingestion/pipeline.py
backend/evaluation/evaluator.py
notebooks/01_backend_foundation.ipynb                 deleted
backend/config/README_config.md                        deleted
reports/phase_1_backend_skeleton_simplicity_implementation_report.md created
```

Existing user-owned and Reviewer-owned documentation changes may also remain in
the dirty worktree. Do not stage, commit or push anything. Hand control back to
the user for Codex Reviewer verification.
