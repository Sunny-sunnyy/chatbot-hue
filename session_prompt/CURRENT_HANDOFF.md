# Bàn giao hiện hành — Full-corpus Phase 4 Tasks 1–6

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: 071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f
Head commit at authoring: worktree
Risk level: high
Git authorization: none
Sub-agent authorization: user-standing

## Approved package

User đã duyệt conceptual design, Written Spec, Implementation Plan và Review
Contract Full-corpus Phase 4 ngày 2026-09-12 +07.

Canonical artifacts:

- Written Spec:
  `docs/superpowers/specs/2026-09-12-phase-4-full-corpus-qdrant-ingestion-written-spec.md`;
- Implementation Plan + Review Contract:
  `docs/superpowers/plans/2026-09-12-phase-4-full-corpus-qdrant-ingestion-implementation-plan.md`;
- canonical guide: `guides/phase_4_qdrant_ingestion.md`.

Closed dependency: Full-corpus Phase 3 User-closed với `205` files, `8.460`
chunks, corpus identity
`0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223`,
sparse SHA-256
`5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`
và bốn bounded dense candidates PASS.

## Objective duy nhất

Thực hiện đúng **Tasks 1–6** của approved Plan bằng
`superpowers:executing-plans`: NumPy dense matrix path; reusable sparse lookup;
deterministic record helpers; exact Qdrant schema/fresh-target guards; bounded
64-point construction/completion verification; static registry, CLI, checks và
một exact read-only preflight package.

Sau Task 6, dừng và trả exact preflight evidence cho User/Reviewer. Không thực
hiện Task 7 hoặc Task 8 trong handoff này.

## Context loading

### Full-read

- `session_prompt/Session_Prompt.md`;
- `session_prompt/IMPLEMENTER_WORKFLOW.md`;
- file này;
- `skills/risk-gated-agent-review/SKILL.md`;
- `skills/practical-project-coding/SKILL.md`;
- Written Spec, Implementation Plan + Review Contract và guide Phase 4 nêu trên.

### Targeted-read

- `backend/embedding/full_corpus.py` và test tương ứng: Phase 3 dense APIs;
- `backend/embedding/sparse.py` và test tương ứng: sparse contract;
- `backend/ingestion/source_state.py`, full-corpus chunker/schema anchors;
- `backend/vectorstore/qdrant.py`, `points.py`, `upsert.py`: giữ Foods behavior;
- Phase 3 preflight JSON: corpus/sparse/model/sample identities;
- `session_prompt/Project_Status.md`: current Phase 4 snapshot.

### Reference-only

- Phase 2/3 correction history ngoài final review;
- Foods Phase 4–8 reports, Golden/evaluation và old benchmark artifacts;
- umbrella full-corpus package và `llm_rag` reports trừ khi có mâu thuẫn;
- Notebook 04, API/frontend/generation/retrieval và phases 5–8.

## Allowed paths

```text
backend/embedding/full_corpus.py
backend/embedding/sparse.py
backend/ingestion/source_state.py
backend/vectorstore/qdrant.py
backend/vectorstore/points.py
backend/vectorstore/upsert.py
backend/ingestion/full_corpus_pipeline.py
backend/tests/test_full_corpus_embedding.py
backend/tests/test_full_corpus_sparse.py
backend/tests/test_full_corpus_qdrant_ingestion.py
reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json
```

Không sửa Spec/Plan/Review Contract, guide/status/workflow,
`CURRENT_HANDOFF.md`, Notebook 04 hoặc implementation report trong handoff này.
Giữ nguyên mọi thay đổi User/phase trước đang có trong dirty worktree.

## Authority hiện hành

Được phép code/TDD/pure checks Tasks 1–6; đọc canonical input/closed artifacts;
không load dense model. Sau khi pure checks PASS, được kết nối cùng Hue RAG
Qdrant local và chỉ gọi `info`, `collection_exists`, `get_collection`, `count`
cho đúng bốn targets:

```text
hue_full_corpus_a_e5_small_384
hue_full_corpus_a_e5_base_768
hue_full_corpus_a_huydang_dek21_768
hue_full_corpus_a_qwen3_06b_1024
```

Được ghi atomic preflight artifact đúng allowed path.

Không được load/run dense model hoặc dense-encode full corpus; không
create/upsert/delete/reset/recreate/query/scroll/retrieve collection; không truy
cập Foods collections; không Task 7/8; không đổi model/schema/payload/ID,
dependency/settings/Docker/corpus/Golden/retrieval/generation/API/frontend;
không paid service hay Git operation.

## Required execution and evidence

1. Resolve base/head và complete dirty-worktree inventory trước khi sửa.
2. Thực hiện Tasks 1–6 theo dependency order và RED/GREEN commands.
3. Chạy focused deterministic suite trong Review Contract; không fake/mock/stub
   Qdrant client, embedded Qdrant hoặc disposable collection.
4. Chạy `git diff --check` và audit exact diff/immutable paths.
5. Chỉ khi code/pure checks đạt, chạy exact read-only commands:

```bash
docker compose ps
docker compose config --images
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-preflight-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline \
  preflight \
  --output reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json
```

6. Report actual results, target states/blockers, identities/resources và mọi
   failed/skipped/not-verified; không biến expected value thành observed result.

## Stop conditions

- Cần đổi requirement/architecture/model/schema/payload/ID/risk/authority/path:
  dừng và trả Reviewer/User.
- Qdrant unavailable, target mismatched/non-empty, record exists hoặc identity
  lệch: ghi `BLOCKED`; không model, mutation, delete/recovery/retry.
- Preflight `READY`: vẫn dừng và trả artifact/evidence. Task 7 chỉ mở sau User
  live-write approval riêng nêu đủ bốn targets.

## Next action duy nhất

Implementer đọc full active package, thực hiện Tasks 1–6, tự review rồi trả kết
quả preflight qua User. Không claim PASS/approval/closure và không tự thay handoff.
