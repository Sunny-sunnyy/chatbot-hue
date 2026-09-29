# Bàn giao hiện hành — Full-corpus Metadata v2 Gate 3 / Task 6

Target role: implementer
Authored by: reviewer
Handoff kind: implementation
State: active
Base commit: 92f2e2cce0e85c9b4f733aaab038bc99cad314c0
Head commit: HEAD after Metadata v2 Gate 1–2 checkpoint commit
Risk level: high — canonical full-corpus retrieval cutover trên bốn metadata-v2 targets
Git authorization: none
Sub-agent authorization: none

## 1. Quyết định và authority mới nhất

Gate 2 / Task 5 đã independent review đạt `ready_for_user_confirmation` tại:

```text
reports/full_corpus_metadata_v2_gate_2_codex_review_2026_09_29.md
```

Ngày 2026-09-29 +07, User xác nhận:

```text
Tôi xác nhận closure Full-corpus Metadata v2 Gate 2 / Task 5 và phê duyệt
Gate 3 / Task 6 theo Approval Closure Contract.
```

Authority này chỉ mở Task 6 của approved Metadata v2 Plan: strict runtime
retrieval cutover, focused tests và selected read-only retrieval smoke. Không tự
mở Task 7 hoặc Phase 6.

## 2. Active inputs và read level

```text
full-read: session_prompt/IMPLEMENTER_WORKFLOW.md
full-read: session_prompt/Session_Prompt.md
full-read: session_prompt/Project_Status.md
full-read: session_prompt/CURRENT_HANDOFF.md
full-read: skills/risk-gated-agent-review/SKILL.md
full-read: skills/practical-project-coding/SKILL.md
full-read: docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md
full-read: docs/superpowers/plans/2026-09-29-full-corpus-metadata-v2-implementation-plan.md
targeted-read: guides/full_corpus_rag.md (status, metadata-v2 decisions và boundaries)
reference-only: reports/full_corpus_metadata_v2_gate_2_codex_review_2026_09_29.md
reference-only: reports/full_corpus_metadata_v2_gate_2_implementation_2026_09_29.md
```

Task 6 source/tests phải đọc đầy đủ trước khi sửa:

```text
backend/retrieval/full_corpus.py
backend/tests/test_full_corpus_retrieval.py
backend/retrieval/full_corpus_smoke.py  # chỉ sửa nếu contract thật sự yêu cầu
```

## 3. Verified dependency state

Bốn metadata-v2 targets đã được Reviewer fresh verify đủ 33.840 points:

```text
hue_full_corpus_a_e5_small_384_metadata_v2
hue_full_corpus_a_e5_base_768_metadata_v2
hue_full_corpus_a_huydang_dek21_768_metadata_v2
hue_full_corpus_a_qwen3_06b_1024_metadata_v2
```

Mỗi target có 8.460 points, exact seven-field payload, source-equal dense+sparse
vectors, matching v2 lineage record và `payload_schema == {}`. Bốn legacy
collections/v1 records không đổi. Gate 3 coi cả legacy và metadata-v2 targets là
read-only.

## 4. Exact allowed paths

Được sửa:

```text
backend/retrieval/full_corpus.py
backend/tests/test_full_corpus_retrieval.py
backend/retrieval/full_corpus_smoke.py  # only if required by Task 6 behavior
reports/full_corpus_metadata_v2_gate_3_implementation_2026_09_29.md
session_prompt/CURRENT_HANDOFF.md        # chỉ khi bàn giao Reviewer
```

Được tạo/update ignored runtime evidence:

```text
data/full_corpus_metadata_v2_smoke.json
data/full_corpus_metadata_v2_minilm_smoke.json
```

Không sửa Gate 1 migration/schema/build code, spec, plan, guide, Project Status,
corpus, Qdrant collections/build records, public API, Golden/evaluation hoặc
Phase 6 package.

## 5. Exact Task 6 workflow

### Step 1 — Baseline và RED tests

Ghi `git status --short`, bảo toàn unrelated staged/untracked state. Thêm đúng
các cases Task 6 Plan yêu cầu cho exact v2 payload/readiness/freshness,
point-UUID/chunk-ID relation, logical result identity, unchanged point-ID
ranking/tie-break và sanitized trace cho cả no-rerank/MiniLM-success boundary.

Chạy RED:

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py -q --tb=short
```

Ghi đúng failures chứng minh runtime năm-field/v1 hiện hành chưa đạt v2; không
biến expected RED thành PASS evidence.

### Step 2 — Implement strict v2 runtime cutover

- Chọn `candidate.metadata_v2_collection_name` tại composition.
- Require build schema v2, payload schema v2, exact source lineage, current
  source freshness, existing model/sparse/count invariants và empty Qdrant
  payload-index schema.
- Payload phải đúng bảy field; validate `chunk_id`, point UUID relation và
  `domain`/`source` consistency trước result construction.
- Giữ candidate docs, dense/sparse branches, BM25, RRF và reranker tie-break theo
  point UUID; chỉ map sang logical `chunk_id`/`domain` tại result/trace boundary.
- Public error không lộ path-level discrepancies; trace chỉ dùng allowlist trong
  approved Plan.
- Không dùng `domain` để filter, boost hoặc route scoring.

Giữ data flow trực tiếp; không thêm compatibility fallback, registry/framework,
retry, cache, migration logic hay abstraction phòng xa.

### Step 3 — GREEN và focused regression

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_sparse.py -q --tb=short
```

Không chạy full backend suite; Task 7 chưa được mở.

### Step 4 — Selected real read-only retrieval smoke

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 e5-base-768 huydang-dek21-768 qwen3-embedding-0.6b-1024 --treatment dense_bm25_rrf native_hybrid_rrf --reranker none --select P5-Q01 --output data/full_corpus_metadata_v2_smoke.json
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 --treatment dense_bm25_rrf native_hybrid_rrf --reranker minilm --select P5-Q01 --output data/full_corpus_metadata_v2_minilm_smoke.json
```

Expected scope: 8 no-rerank cells và 2 MiniLM cells. Báo observed result thật;
ranking difference không tự là failure nếu identity/payload/vector/score
semantics vẫn đúng contract.

### Step 5 — Self-review và bàn giao Reviewer

Chạy `git diff --check`, đọc exact diff, kiểm scope/privacy/simplicity. Tạo
sanitized interim report:

```text
reports/full_corpus_metadata_v2_gate_3_implementation_2026_09_29.md
```

Report phải map Task 6 acceptance vào RED/GREEN, runtime freshness/identity,
selected smoke, changed paths, failed/skipped/not-verified và giới hạn. Không
chép query/evidence/corpus text, source-path map, point rows, vectors, absolute
paths hoặc secrets.

Replace handoff thành `Target role: reviewer`, `Handoff kind: final_review`, dẫn
exact diff/report/artifacts và Reviewer minimum checks. Dừng trước Task 7.

## 6. Stop conditions

Dừng và chuyển Reviewer, không nới validator/fallback hoặc mở scope, nếu:

- một metadata-v2 target/v2 record/legacy source không còn khớp verified state;
- cần Qdrant create/upsert/delete/repair/index/alias hoặc sửa build record;
- cần re-embedding, external/paid model/API, evaluation hoặc Phase 6;
- strict freshness hoặc payload/identity contract mâu thuẫn canonical source;
- cần sửa ngoài exact allowed paths;
- selected real smoke cho thấy data/identity/vector/score semantics sai mà
  focused Task 6 fix không thể giải quyết trong approved architecture.

Không chạy Task 7 để xử lý failure. Không restore/stage/commit/clean unrelated
worktree state.

## 7. Hard boundaries

- Bốn legacy collections, bốn metadata-v2 targets và mọi build record chỉ
  read-only.
- Không cleanup/delete/reconcile/re-ingest/re-encode hoặc payload index.
- Không đổi public API, Golden, evaluation, generator/provider hoặc Phase 6.
- Không full backend suite, Git add/commit/push hoặc sub-agent.
- Không expose `.env`, secret, corpus/query/evidence text, vectors hoặc private
  source paths trong tracked artifact/report.

## 8. Next action duy nhất

Implementer ghi baseline rồi bắt đầu Task 6 Step 1 bằng exact RED tests; tiếp tục
tuần tự tới selected real smoke và Reviewer handoff nếu không gặp stop condition.
