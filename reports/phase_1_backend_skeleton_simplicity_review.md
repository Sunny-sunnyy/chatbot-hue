# Phase 1 Backend Skeleton Simplicity Review

Date: `2026-08-24 +07`

Status: `Before recorded; plan ready; Implementer not assigned`

## 1. Before state

Phase 1 was approved on `2026-08-09 +07` with central YAML settings, logging
configuration, a shared `RetrievedDocument`, package markers and Notebook 01.

The current project has since grown through Phase 7. Phase 1 files now support
real ingestion, Qdrant retrieval, generation, API and evaluation consumers.
The fresh pre-review backend baseline is:

```text
222 passed, 4 warnings in 260.37s
```

## 2. Capabilities to preserve

- One readable backend package layout.
- One central `settings.yaml`.
- Three valid retrieval profiles and fail-fast invalid-profile behavior.
- Console and file logging independent of the current working directory.
- Shared `RetrievedDocument` behavior.
- All downstream Phase 2–7 runtime behavior.
- Active Qdrant collection contents and schema.

## 3. Findings

1. `setup_logging()` and `logging.yaml` exist, but Hue RAG runtime entrypoints
   do not call them. In the `llm_rag` reference, API and ingestion do call the
   logging setup.
2. Notebook 01 is mostly a package/config/logging smoke suite, not a useful RAG
   learning notebook.
3. `backend/config/README_config.md` duplicates YAML comments and canonical
   guides, including rules owned by later phases.
4. `_validate_active_profile()` has one remaining production caller and can be
   read more directly inside `load_settings()` after Notebook 01 is removed.
5. Downstream config keys must not be deleted before their owning phase review.
6. Error classes added by Phase 5–6 should not be redesigned prematurely in
   Phase 1.

## 4. Approved changes

- Connect logging at API lifespan, ingestion `main()` and evaluation `main()`.
- Keep import safety and avoid module-level logging side effects.
- Inline active-profile validation in `load_settings()`.
- Delete Notebook 01.
- Delete the duplicate config README.
- Make notebooks conditional on real learning value project-wide.
- Preserve downstream settings and errors until their owning reviews.

## 5. Downstream impact

| Phase | Expected impact |
|---:|---|
| 2 | Settings values unchanged; ingestion entrypoint gains configured logging |
| 3 | Embedding config unchanged |
| 4 | Qdrant config and active collection unchanged |
| 5 | Retrieval config, profiles and error behavior unchanged |
| 6 | API/generation output unchanged; API runtime gains configured logging |
| 7 | Evaluation UI gains configured logging; metrics and CSV behavior unchanged |

No Phase 7 quality rerun is planned unless implementation changes RAG behavior.

## 6. Verification plan

- Compile affected modules.
- Load canonical settings and verify all three profiles.
- Write a real non-sensitive log and observe console/file output.
- Start API against real Qdrant and local E5; inspect startup and health.
- Start the real evaluation UI far enough to confirm logging configuration.
- Run affected integration tests and the full backend suite.
- Keep the active collection read-only.
- Run `git diff --check` and scan for conflict markers.
- Use no mock, fake service or replayed output as completion evidence.

## 7. After state

Pending. The implementation plan is ready, but the user has not assigned it to
the Implementer. No Phase 1 runtime change has started.

## 8. Before/After comparison

| Area | Before | Target After |
|---|---|---|
| Settings | Loader plus single-use helper | One direct loader function |
| Logging | Config exists but runtime does not activate it | Three real entrypoints activate it |
| Config docs | YAML, guide and duplicate README | YAML comments plus canonical guides |
| Phase 1 notebook | Smoke/validation notebook | No unnecessary notebook |
| Error classes | Mixed into shared schema by later phases | Unchanged until Phase 5–6 review |
| RAG behavior | Approved through Phase 7 | Preserved |

## 9. Bugs and resolutions

No implementation bug has been fixed yet. The missing runtime logging hookup is
an approved design finding awaiting implementation.

## 10. Remaining limitations

- Runtime changes have not been implemented or verified.
- Downstream config cleanup remains Phase 2–7 work.
- Error cleanup remains Phase 5–6 work and requires downstream safety evidence.
- Existing unrelated worktree changes remain owned by the user.

## 11. Reviewer conclusion

The focused Phase 1 design and implementation plan are ready. The user has not
assigned the work to the Implementer. Phase 1 is not re-approved until the
After state and independent verification are recorded.
