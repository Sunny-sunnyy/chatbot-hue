# Bàn giao hiện hành — Full-corpus Metadata v2 Gate 1

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: 92f2e2cce0e85c9b4f733aaab038bc99cad314c0
Head commit: HEAD after the approved Metadata v2 documentation handoff commit
Risk level: high — thay đổi chunk/payload/build contracts và chuẩn bị migration bốn collections
Git authorization: none
Sub-agent authorization: none

## Quyết định và authority mới nhất của User

Ngày 2026-09-29, User đã duyệt:

- Full-corpus Metadata v2 Written Spec;
- Implementation Plan và embedded Review Contract;
- chỉ **Gate 1 / Tasks 1–4** của Plan.

Gate 1 cho phép sửa code/tests trong exact scope, đọc local corpus và chạy
read-only preflight/scroll trên bốn legacy Full-corpus collections. Gate 1
không cho phép Qdrant create/upsert, ghi build record v2, runtime cutover,
delete/cleanup, dense embedding, paid API/model, Phase 6 implementation hoặc
Git write.

## Active contracts — đọc đầy đủ

```text
session_prompt/Session_Prompt.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/Project_Status.md
session_prompt/CURRENT_HANDOFF.md
skills/practical-project-coding/SKILL.md
docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md
docs/superpowers/plans/2026-09-29-full-corpus-metadata-v2-implementation-plan.md
```

Targeted-read khi task tương ứng bắt đầu:

```text
guides/full_corpus_rag.md
backend/core/schema.py
backend/ingestion/full_corpus_pipeline.py
backend/ingestion/source_state.py
backend/vectorstore/points.py
backend/vectorstore/qdrant.py
backend/vectorstore/upsert.py
backend/retrieval/full_corpus.py
backend/tests/test_full_corpus_chunker.py
backend/tests/test_full_corpus_sparse.py
backend/tests/test_full_corpus_qdrant_ingestion.py
```

Phase 4/5/6 historical specs/plans/reports là `reference-only`; chỉ mở một phần
khi active Plan dẫn tới claim cụ thể. Không dùng package Phase 6 đã pause làm
authority.

## Mục tiêu Gate 1

Thực hiện tuần tự đúng Tasks 1–4 của approved Plan:

1. thêm canonical five-value `domain`, chunk-ID validation và exact seven-field
   payload;
2. thêm bốn fixed metadata-v2 target names và build-record v2 constructor trong
   khi giữ v1 behavior lịch sử;
3. tạo strict migration/vector-copy primitives cùng pure tests;
4. tạo guarded CLI, chạy focused tests và real read-only four-pair preflight;
5. dừng trước mọi Qdrant write và bàn giao evidence cho Reviewer.

Không bắt đầu Task 5, Task 6 hoặc Task 7.

## Exact allowed paths

Implementer được tạo/sửa trong Gate 1:

```text
backend/core/schema.py
backend/ingestion/full_corpus_pipeline.py
backend/ingestion/source_state.py
backend/ingestion/full_corpus_metadata_v2.py
backend/vectorstore/points.py
backend/tests/test_full_corpus_chunker.py
backend/tests/test_full_corpus_sparse.py
backend/tests/test_full_corpus_qdrant_ingestion.py
backend/tests/test_full_corpus_metadata_v2.py
reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json
reports/full_corpus_metadata_v2_gate_1_implementation_2026_09_29.md
session_prompt/CURRENT_HANDOFF.md  # chỉ replace ở final Gate 1 handoff
```

`backend/vectorstore/qdrant.py` và `backend/vectorstore/upsert.py` chỉ được đọc;
không sửa trừ khi một blocker thực tế chứng minh Task 1–4 không thể hoàn thành
đúng locked interfaces. Khi đó dừng và báo Reviewer, không tự mở scope.

Không sửa:

```text
knowledge-base-hue/**
qdrant_storage/**
data/full_corpus_builds/**
backend/retrieval/full_corpus.py
backend/retrieval/full_corpus_smoke.py
backend/config/settings.yaml
knowledge-base-hue/**/evaluation/**
docs/superpowers/specs/**
docs/superpowers/plans/**
guides/**
session_prompt/Project_Status.md
.gitignore
pyproject.toml
uv.lock
```

## Immutable external state

Legacy sources, chỉ read-only:

```text
hue_full_corpus_a_e5_small_384
hue_full_corpus_a_e5_base_768
hue_full_corpus_a_huydang_dek21_768
hue_full_corpus_a_qwen3_06b_1024
```

Fresh targets phải còn absent và tuyệt đối không được tạo trong Gate 1:

```text
hue_full_corpus_a_e5_small_384_metadata_v2
hue_full_corpus_a_e5_base_768_metadata_v2
hue_full_corpus_a_huydang_dek21_768_metadata_v2
hue_full_corpus_a_qwen3_06b_1024_metadata_v2
```

Không gọi `create_collection`, `upsert`, `delete`, `update_collection`, payload
mutation, alias hoặc reset. CLI `migrate` có thể được implement/test bằng
recording client theo Plan nhưng không được chạy với real Qdrant.

## Worktree boundary

Worktree đã có staged `.gitignore`/corpus untracking và các untracked User
files/reports từ trước. Curated files vẫn tồn tại local dù được staged untrack.
Ghi inventory trước khi sửa; không restore, stage, commit, clean, move hoặc sửa
các thay đổi ngoài exact allowed paths.

Reviewer documentation commit trước handoff không cấp Git authority cho
Implementer. Implementer không commit/push.

## Verification và evidence bắt buộc

Chạy đúng RED/GREEN commands trong từng Task. Final focused Gate 1 command:

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py -q --tb=short
```

Sau khi pure/focused tests PASS, chạy một real read-only preflight:

```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json
```

Expected: overall `READY`, bốn legacy sources hợp lệ, current source state
fresh, bốn fixed targets/build-record paths absent và mutation count zero.
Preflight artifact không chứa 205-path map, point IDs, payloads, vectors,
corpus/query text, absolute path hoặc secret.

Không chạy full backend suite, dense embedding, Qwen/CUDA model, benchmark hoặc
Phase 6 API.

## Stop conditions

Dừng ngay và chuyển Reviewer nếu:

- một legacy record/collection, source hash, point set, payload hoặc vector
  không khớp;
- một target/build-record path đã tồn tại;
- preflight cần Qdrant mutation hoặc dense model load;
- exact payload/domain/identity contract mâu thuẫn source hiện hành;
- thay đổi cần vượt exact allowed paths;
- focused tests hoặc preflight không đạt.

Không sửa dữ liệu, xóa target, nới validator, thêm compatibility fallback hoặc
tiếp tục Task 5 để “khắc phục”.

## Gate 1 report và final handoff

Tạo:

```text
reports/full_corpus_metadata_v2_gate_1_implementation_2026_09_29.md
```

Report phải có authority/worktree state, changed paths, RED/GREEN commands,
domain/payload/build-record evidence, four-pair preflight, zero-mutation/no-model
evidence, deviations, failed/skipped/not-verified và acceptance mapping. Không
chép private source/path map, point rows, payload/vector text hoặc secret.

Sau self-review, replace file này thành:

```text
Target role: reviewer
Handoff kind: final_review
```

Handoff mới dẫn exact diff, report, preflight artifact, command results và có
một next action duy nhất: Reviewer independently review Metadata v2 Gate 1 và
quyết định có trình User mở Gate 2 hay không.

## Next action duy nhất

Implementer đọc active contracts, ghi worktree baseline rồi thực hiện đúng
Task 1 của approved Metadata v2 Plan. Tiếp tục tuần tự tới hết Task 4 nếu không
gặp stop condition; tuyệt đối dừng trước Task 5/Qdrant write.
