# Phase 1 Backend Foundation Simplicity Design

Date: `2026-08-24 +07`

Status: `approved by user`

## Purpose

Simplify the Phase 1 foundation without changing RAG behavior. The result must
remain easy to trace: one YAML settings loader, one logging setup, one shared
retrieval document model and ordinary Python packages.

This design uses `/home/minhhieu/llm_rag` as a readability reference. It adapts
the direct YAML and logging pattern to Hue RAG; it does not copy the reference
project's JSON pipeline, environment override list, import-time side effects or
mock-based evidence.

## Before state

Phase 1 is historically approved and currently provides:

- the backend package layout;
- central `settings.yaml` and `load_settings()`;
- `logging.yaml` and `setup_logging()`;
- `RetrievedDocument` in `core/schema.py`;
- Notebook 01 and `backend/config/README_config.md`.

Later phases extended the settings groups and added retrieval/generation error
classes to `core/schema.py`. They are part of the current system but are not
all owned by Phase 1.

The fresh full-backend baseline before the Phase 0–6 simplicity review is:

```text
222 passed, 4 warnings in 260.37s
```

## Approved approach

Use a focused foundation cleanup:

- keep central YAML settings;
- keep the current package layout;
- make `load_settings()` direct and readable;
- connect the existing logging system to real runtime entrypoints;
- remove documentation and notebook artifacts that duplicate code or act as
  smoke-test suites;
- leave downstream config groups and error behavior to their owning phases.

Do not add typed settings, dependency injection, a logging wrapper, a config
factory or compatibility layers.

## Architecture

```text
settings.yaml
-> load_settings()
-> validate active_profile
-> return the settings mapping

runtime entrypoint
-> setup_logging()
-> console + backend/logs/application.log
-> existing runtime flow

retrieval result
-> RetrievedDocument
-> retrieval, reranking and context
```

## Runtime scope

The Implementer changes only the following runtime behavior:

1. `backend/core/settings_loader.py`
   - keep YAML loading and `active_profile` validation;
   - place the validation directly inside `load_settings()`;
   - remove `_validate_active_profile()`, which has no remaining external
     consumer after Notebook 01 is removed.
2. `backend/api/app.py`
   - call `setup_logging()` when the FastAPI lifespan starts and before runtime
     components are built;
   - preserve import safety: importing the module must not create the log file.
3. `backend/ingestion/pipeline.py`
   - call `setup_logging()` in `main()`;
   - remove the separate `logging.basicConfig()` call.
4. `backend/evaluation/evaluator.py`
   - call `setup_logging()` in `main()` before Gradio launches.

Keep `backend/core/logging_setup.py` and `backend/config/logging.yaml` small and
direct. Do not add new runtime files or dependencies.

## Removal scope

Delete:

```text
notebooks/01_backend_foundation.ipynb
backend/config/README_config.md
```

Notebook 01 mainly lists packages, prints settings, triggers an invalid profile,
writes a smoke log and constructs a dataclass. Those checks belong in code
review, commands or tests, not a learning notebook. The config README repeats
the YAML comments and canonical guides.

Historical implementation, Codex and user reports remain unchanged.

## Configuration ownership

`settings.yaml` remains central. Phase 1 owns only loading and `active_profile`
validation. Each downstream group is simplified in its owning phase:

| Settings group | Owning review |
|---|---:|
| `knowledge_base` | Phase 2 |
| `embedding` | Phase 3 |
| `vector_database` | Phase 4 |
| `retrieval`, `reranking` | Phase 5 |
| `llm` | Phase 6 |
| `evaluation` | Phase 7 impact assessment |

Phase 1 must not remove or wire unused downstream fields prematurely.

## Shared schema and errors

`RetrievedDocument` remains the only Phase 1 shared data contract.

The retrieval and generation error classes currently stored in
`core/schema.py` remain unchanged in Phase 1. Phase 5 reviews retrieval errors;
Phase 6 reviews generation errors and HTTP mappings. They may be removed or
relocated only after the affected Phase 5–7 flows and the full system are safe.

## Logging behavior

- Entry points configure logging once; child modules only call
  `logging.getLogger(...)`.
- Logs go to the console and `backend/logs/application.log`.
- Missing or invalid logging configuration fails explicitly. There is no
  silent fallback.
- Logs may contain profile/model/collection identifiers, counts, startup state
  and non-sensitive summaries.
- Logs must not contain API keys, environment values, full settings, raw
  questions, contexts, answers, vectors or knowledge-base bodies.
- Do not add retries, rotation, remote logging, middleware or decorators.

## Notebook policy

A notebook is no longer mandatory for every implementation phase. A phase has
one only when it materially helps a human understand or observe the system.

Any retained notebook must:

- make one cell do one job;
- explain briefly before code;
- use short cells that call clear backend functions;
- avoid becoming a validator, audit package or test suite;
- keep repository outputs and execution counts empty;
- use these mandatory style references:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_old_0/*.ipynb
/home/minhhieu/llm_rag/tai_lieu/notebook_simple/**/*.ipynb
```

Phase 1 does not need a notebook after this change. Phase 2–8 decide separately
in their canonical guides.

## Verification

Verification uses real local code and services:

```text
compile affected modules
-> load canonical settings and resolve all three profiles
-> run setup_logging and observe console + application.log
-> start the API with real Qdrant and local E5, then inspect health/startup
-> start the evaluation UI and confirm logging setup
-> run affected downstream integration tests
-> run the full backend suite
-> git diff --check and merge-marker scan
```

Do not mutate the active Hue collection. If ingestion verification is needed,
use an isolated real Qdrant test collection. Mocks, fake services and replayed
outputs are not completion evidence.

The 104-question Phase 7 evaluation is not required for this change because no
chunk, vector, retrieval, context, prompt, model or metric behavior changes. If
implementation changes RAG behavior unexpectedly, stop and expand verification.

## Downstream impact

- Phase 2–7 continue reading the same settings values.
- Logging becomes active at real entrypoints but does not change business
  outputs.
- Retrieval and API error mappings remain unchanged.
- Phase 7 CSV files and evaluation logic remain unchanged.
- Phase 8 remains closed.
- The active Qdrant collection remains read-only.

## Acceptance

Phase 1 can return to `approved` only when:

1. the code changes match this exact scope and remain easy to read;
2. logging works through the three real entrypoints;
3. settings and `RetrievedDocument` behavior remain intact;
4. Notebook 01 and the duplicate config README are removed;
5. downstream and full-suite verification pass without fake evidence;
6. unrelated worktree changes are preserved and no conflict remains;
7. the Reviewer independently verifies the implementation and the user
   confirms the result.

No commit or push is authorized by this design.
