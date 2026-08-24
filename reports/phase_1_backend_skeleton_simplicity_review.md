# Phase 1 Backend Skeleton Simplicity Review

Date: `2026-08-24 +07`

Status: `Approved by user`

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
- Confirm the active collection and Phase 7 CSV files remain unchanged.
- Keep the active collection read-only.
- Run `git diff --check` and scan for conflict markers.
- Use no mock, fake service or replayed output as completion evidence.

Phase 1 không cần automated test theo blast-radius policy hiện hành. Affected
và full suites đã được chạy trong review trước khi policy được làm rõ; chúng là
observed history, không phải requirement cho Phase 1.

## 7. After state

Implementation đã hoàn tất đúng approved scope:

- `load_settings()` đọc YAML và kiểm tra active profile trong một flow trực
  tiếp, không còn helper một-caller;
- API lifespan, ingestion CLI và evaluation UI gọi chung `setup_logging()`
  trước runtime work;
- Notebook 01 và config README trùng lặp đã được xóa;
- settings values, shared schema và downstream RAG behavior không đổi.

Fresh independent review đạt `74 passed, 3 warnings` cho affected suite và
`222 passed, 4 warnings` cho full backend suite. API health đạt `status=ok`,
Gradio phục vụ tại local URL, active collection vẫn có 572 points và hai CSV
Phase 7 kết thúc review với zero diff.

Hai test runs là observed history từ verification scope cũ, không phải
acceptance target và không chứng minh mọi test trong suite đều cần thiết.
Phase 1 acceptance dựa trên exact settings/logging/API/Gradio/Qdrant live paths.

## 8. Before/After comparison

| Area | Before | Target After |
|---|---|---|
| Settings | Loader plus single-use helper | One direct loader function |
| Logging | Config exists but runtime does not activate it | Three real entrypoints activate it |
| Config docs | YAML, guide and duplicate README | YAML comments plus canonical guides |
| Phase 1 notebook | Smoke/validation notebook | Removed; no unnecessary notebook |
| Error classes | Mixed into shared schema by later phases | Unchanged until Phase 5–6 review |
| RAG behavior | Approved through Phase 7 | Preserved by fresh full-suite and live checks |

## 9. Bugs and resolutions

- Missing runtime logging hookup: fixed by calling the existing setup directly
  at the three approved entrypoints.
- Reviewer run exposed a pre-existing evaluation-test side effect:
  `test_retrieval_handler_returns_named_columns_and_rows` writes the canonical
  retrieval CSV with CRLF line endings. Reviewer restored the exact line-ending
  change and confirmed zero final CSV diff. This belongs to the Phase 7 test
  impact review and does not require Phase 1 runtime expansion.

## 10. Remaining limitations

- Gradio served successfully, but its `inbrowser=True` attempt could not open a
  GUI browser in the headless review environment; the local server itself was
  healthy and stopped cleanly.
- The paid 104-question evaluation was not rerun because this scope does not
  affect RAG quality, as explicitly defined by the guide.
- Affected/full suites đã chạy rộng hơn nhu cầu Phase 1. Test relevance và
  cleanup tiếp tục theo ownership của Phase 2–6, không kéo ngược vào Phase 1.
- Downstream config/error cleanup remains owned by Phase 2–7 reviews.
- Existing unrelated worktree changes remain owned by the user.

## 11. Reviewer conclusion

Decision kỹ thuật: `ready_for_user_confirmation`; không có blocker hoặc major
finding. User đã xác nhận Phase 1 ngày `2026-08-24 +07`; phase hiện
`approved`. Bước tiếp theo là brainstorm simplicity review Phase 2.
