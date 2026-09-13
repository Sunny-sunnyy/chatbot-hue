# Full-corpus Phase 4 Qdrant Ingestion — Implementation Report

## Authority and repository state

- **Role:** Implementer
- **Target Collections:**
  - `hue_full_corpus_a_e5_small_384`
  - `hue_full_corpus_a_e5_base_768`
  - `hue_full_corpus_a_huydang_dek21_768`
  - `hue_full_corpus_a_qwen3_06b_1024`
- **Base Commit:** `071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f` (ancestor)
- **Current HEAD:** `511e8a3eac783b324470f2da3ce5d5fddd786ab8`
- **Git authorization:** `none` (zero git commits, zero git push, zero git branch/tag mutations).
- **Sub-agent authorization:** none / task-specific read-only research only.
- **Pre-existing untracked files:** `PROJECT_DOCUMENT_REGISTRY.md` preserved intact in the worktree.

## Changed paths and immutable paths

### Changed / Added Deliverable Paths
- `backend/embedding/full_corpus.py` (NumPy embedding matrix support, validation helpers)
- `backend/embedding/sparse.py` (Reusable vocabulary index, document sparse encoding)
- `backend/ingestion/source_state.py` (Build record schema, serialization, atomic exclusive write via `os.link`)
- `backend/vectorstore/qdrant.py` (Strict default schema validation, fresh-target observation & guards)
- `backend/vectorstore/points.py` (Batch-64 point building with exact payload and UUID5 IDs)
- `backend/vectorstore/upsert.py` (Batch upsert, chunk mapping fix, collection verification)
- `backend/ingestion/full_corpus_pipeline.py` (Registry, candidate preparation, CLI, preflight & build orchestration)
- `backend/tests/conftest.py` (Removed `autouse=True` from cleanup sweep, isolated live fixtures)
- `backend/tests/test_full_corpus_embedding.py` (Dense spec & matrix validation tests)
- `backend/tests/test_full_corpus_sparse.py` (Sparse state, vocabulary index, BM25 equivalence tests)
- `backend/tests/test_full_corpus_qdrant_ingestion.py` (Pure offline schema, target guard, atomic record tests)
- `notebooks/04_qdrant_ingestion.ipynb` (Clean, canonical read-only inspector)
- `reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json` (Initial `READY` preflight artifact)
- `data/full_corpus_builds/hue_full_corpus_a_e5_small_384.json` (Final build record)
- `data/full_corpus_builds/hue_full_corpus_a_e5_base_768.json` (Final build record)
- `data/full_corpus_builds/hue_full_corpus_a_huydang_dek21_768.json` (Final build record)
- `data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024.json` (Final build record)

### Audited Immutable Paths
- `backend/config/settings.yaml`: Untouched, active collection remains `hue_foods_e5_small_384`.
- `docker-compose.yml`: Untouched, pinned Qdrant image digest `qdrant/qdrant@sha256:0bd98fa7977f1e75694779359ca4e212822e5a71334e28421182f72f209d5286`.
- `pyproject.toml` & `uv.lock`: Untouched, zero dependency modifications.
- All 205 source markdown files in `data/`: Untouched, CRLF/LF content preserved.
- Foods collections:
  - `hue_foods_e5_small_384`: 572 points, untouched.
  - `hue_foods_e5_small_384_dense`: 572 points, untouched.

## RED/GREEN deterministic checks

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py \
  -q --tb=short
```
- **Observed Result:** `41 passed in 4.54s` (Exit code: 0).
- **Fixture Isolation (`--fixtures-per-test`):** Verified no pure test lists or triggers `real_client` or `_live_cleanup_sweep`.
- **Pure Offline Enforcement:** Verified with unreachable Qdrant port (`QDRANT_URL=http://127.0.0.1:9999`) -> 41 passed without network attempt.
- **Git Diff Formatting:** `git diff --check` prints 0 errors.

## Initial read-only preflight

- **Preflight Artifact:** `reports/artifacts/full_corpus_phase_4_qdrant_preflight_2026_09_12.json`
- **Status:** `READY`
- **Corpus Identity:** `0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223` (205 files, 8,460 chunks)
- **Source State SHA-256:** `ffeb682812c3355118091fd65820c39fcd6b0ef8670edc9c44c06283593c160d`
- **Sparse State SHA-256:** `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be` (5,662 terms)
- **Initial Target States:** All 4 candidate collections reported `state: absent`, `build_record_exists: false`, `blockers: []`.

## Exact live-write approval

### Initial Live-Write Gate Approval (Verbatim)
> *"Tôi phê duyệt Task 7 sequential live build và Task 8 read-only inspection/report cho đúng bốn targets:*
> *hue_full_corpus_a_e5_small_384,*
> *hue_full_corpus_a_e5_base_768,*
> *hue_full_corpus_a_huydang_dek21_768,*
> *hue_full_corpus_a_qwen3_06b_1024.*
> *Không cấp quyền delete/reset/recovery, truy cập Foods collections, replacement, cleanup, cutover, Phase 5, thay đổi dependency/settings, paid API hoặc Git operation."*

### Guarded Recovery Approval (Verbatim)
> *"Tôi phê duyệt guarded recovery cho duy nhất hue_full_corpus_a_e5_small_384, hiện có 8.460 points và không có final build record, với confirmation string DELETE hue_full_corpus_a_e5_small_384. Sau khi xác minh target absent, cho phép tiếp tục Task 7 tuần tự từ Candidate 1 qua đúng bốn targets đã phê duyệt và Task 8 read-only nếu cả bốn thành công. Không cấp quyền xóa target khác, truy cập Foods, cleanup, cutover, Phase 5 hoặc Git operation."*

## Candidate 1 — e5-small-384

- **Command:** `python -m backend.ingestion.full_corpus_pipeline build --candidate e5-small-384`
- **Target Collection:** `hue_full_corpus_a_e5_small_384`
- **Dense Model:** `intfloat/multilingual-e5-small` @ `614241f622f53c4eeff9890bdc4f31cfecc418b3`
- **Runtime:** CPU, FP32, SDPA, batch size 8
- **Dense Matrix:** Shape `[8460, 384]`, dtype `float32`
- **Unit Norms:** min `0.9999999004790692`, max `1.000000140478028`
- **Qdrant Operations:**
  - Collection created: named dense 384 cosine + named sparse default
  - Completed upserts: `8460` points (batch size 64)
- **Verification:**
  - Count verified: `8460`
  - Payloads verified: `8460`
  - Sample vectors verified: `12`
- **Final Build Record:** `data/full_corpus_builds/hue_full_corpus_a_e5_small_384.json`
  - SHA-256: `ea19021a57c1adb9b283b3198d4883d26f0f18a2451eaf2eaafc815f83571c76`
  - Status: `complete`

## Candidate 2 — e5-base-768

- **Command:** `python -m backend.ingestion.full_corpus_pipeline build --candidate e5-base-768`
- **Target Collection:** `hue_full_corpus_a_e5_base_768`
- **Dense Model:** `intfloat/multilingual-e5-base` @ `d128750597153bb5987e10b1c3493a34e5a4502a`
- **Runtime:** CPU, FP32, SDPA, batch size 8
- **Dense Matrix:** Shape `[8460, 768]`, dtype `float32`
- **Unit Norms:** min `0.9999998875684614`, max `1.0000001535460215`
- **Qdrant Operations:**
  - Collection created: named dense 768 cosine + named sparse default
  - Completed upserts: `8460` points (batch size 64)
- **Verification:**
  - Count verified: `8460`
  - Payloads verified: `8460`
  - Sample vectors verified: `12`
- **Final Build Record:** `data/full_corpus_builds/hue_full_corpus_a_e5_base_768.json`
  - SHA-256: `0cd69406b4bc8ab17953ea0abac3c93011660882cf34c85b0b8645b095ea9d7b`
  - Status: `complete`

## Candidate 3 — huydang-dek21-768

- **Command:** `python -m backend.ingestion.full_corpus_pipeline build --candidate huydang-dek21-768`
- **Target Collection:** `hue_full_corpus_a_huydang_dek21_768`
- **Dense Model:** `CODE4LIFEOFFICIAL/huydang-dek21-embedding` @ `517f1af7dd04a57194f1de2990f0c6ede0a3109b`
- **Runtime:** CPU, FP32, SDPA, batch size 8 (with PyVi word segmentation)
- **Dense Matrix:** Shape `[8460, 768]`, dtype `float32`
- **Unit Norms:** min `0.999999840021476`, max `1.0000001550621564`
- **Qdrant Operations:**
  - Collection created: named dense 768 cosine + named sparse default
  - Completed upserts: `8460` points (batch size 64)
- **Verification:**
  - Count verified: `8460`
  - Payloads verified: `8460`
  - Sample vectors verified: `12`
- **Final Build Record:** `data/full_corpus_builds/hue_full_corpus_a_huydang_dek21_768.json`
  - SHA-256: `10b3f847d9e30bf06acc0e21d83a1cb4b166455bef45c0dd3d5703b3f8371c4a`
  - Status: `complete`

## Candidate 4 — qwen3-embedding-0.6b-1024

- **Command:** `python -m backend.ingestion.full_corpus_pipeline build --candidate qwen3-embedding-0.6b-1024`
- **Target Collection:** `hue_full_corpus_a_qwen3_06b_1024`
- **Dense Model:** `Qwen/Qwen3-Embedding-0.6B` @ `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3`
- **Runtime:** CUDA (`cuda:0`), FP16, eager attention, batch size 1 on NVIDIA GeForce GTX 1650 (Peak VRAM: 1,323,238,400 bytes ≈ 1.26 GB)
- **Dense Matrix:** Shape `[8460, 1024]`, dtype `float16`
- **Unit Norms:** min `0.999755871925492`, max `1.000481951573514` (strictly within the locked `1e-3` tolerance)
- **Qdrant Operations:**
  - Collection created: named dense 1024 cosine + named sparse default
  - Completed upserts: `8460` points (batch size 64)
- **Verification:**
  - Count verified: `8460`
  - Payloads verified: `8460`
  - Sample vectors verified: `12`
- **Final Build Record:** `data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024.json`
  - SHA-256: `2faa9d4f102127093c0ebd5c14c19eef3bd7743ca0e34d434beb5aa40919bdd5`
  - Status: `complete`

## Cross-collection/build-record verification

1. **Identity Integrity across 4 Records:**
   - `corpus.identity`: Exactly `0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223` across all 4 records.
   - `corpus.sources`: Identical 205 relative source paths and SHA-256 mapping across all 4 records.
   - `sparse.state_sha256`: Exactly `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be` across all 4 records.
   - `qdrant.point_count`: Exactly `8460` across all 4 records.
2. **Post-Build Guard Enforcement Test:**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-postbuild-uv-cache \
   uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline preflight
   ```
   - **Observed Exit Code:** `2` (Expected nonzero guard block).
   - **Status:** `BLOCKED`
   - **Blockers:** Every target correctly reports `["target is non-empty: 8460 points", "final build record already exists"]`.
   - **Proof:** Confirms that subsequent runs fail-closed before any model inference or Qdrant mutation can take place.

## Notebook 04 read-only evidence

1. **Canonical Notebook Cleanliness:**
   - Path: `notebooks/04_qdrant_ingestion.ipynb`
   - Verified that all code cell outputs are empty and `execution_count` is `null`.
   - Verified zero forbidden symbols (`build_candidate`, `create_collection`, `.upsert(`, `delete_collection`, `reset_collection`, `FullCorpusDenseRunner`).
2. **Read-Only Execution Evidence:**
   - Executed copy `/tmp/04_qdrant_ingestion-phase4-live.ipynb` via `nbconvert --execute`:
     - Cell 1: `repository root resolved`
     - Cell 2: All 4 candidates verified read-only:
       - `e5-small-384`: status `complete`, verified 8460 points, 8460 payloads, 12 sample vectors.
       - `e5-base-768`: status `complete`, verified 8460 points, 8460 payloads, 12 sample vectors.
       - `huydang-dek21-768`: status `complete`, verified 8460 points, 8460 payloads, 12 sample vectors.
       - `qwen3-embedding-0.6b-1024`: status `complete`, verified 8460 points, 8460 payloads, 12 sample vectors.
       - Sample payload projections printed only metadata fields (`id`, `payload_fields`, `search_text_length`, `evidence_part_count`), no full text dumps.
   - Exit code: 0.

## Acceptance mapping

| Requirement (Written Spec / Plan) | Implementation Evidence | Status |
| :--- | :--- | :---: |
| §2 Fresh corpus / sparse dependencies | 205 files, 8460 chunks, exact corpus & sparse SHAs verified | PASS |
| §3 Two authority checkpoints | Plan approval gate + Verbatim Live approval gates recorded | PASS |
| §4 Static 4-candidate registry | Fixed registry mapping in `full_corpus_pipeline.py` | PASS |
| §5 Exact dense+sparse schema | Verified in `test_full_corpus_qdrant_ingestion.py` & live collections | PASS |
| §6 UUID5, 5-field payload | Verified across all 8460 points per collection | PASS |
| §7 Fresh-target, TOCTOU, partial failure guard | Proved during Incident (fail-closed) and postbuild preflight | PASS |
| §8 NumPy matrix, batch 64, sequential models | Verified row-by-row batch 64 upsert; models run sequentially | PASS |
| §9 8460 count, 8460 payload, 12 sample vector check | 100% verified across all 4 candidates | PASS |
| §10 Final-only atomic records | 4 JSON records published atomically via `os.link` | PASS |
| §11 Component ownership & clean diffs | Pure unit tests and clean `git diff --check` | PASS |
| §12 Pure tests + Real integration evidence | 41 pure tests pass offline; 4 real Qdrant collections built | PASS |
| §13 Notebook 04 read-only | Canonical notebook clean; executed copy passed | PASS |
| §14 All-four acceptance | All 4 candidates complete with matching corpus/sparse hashes | PASS |
| §15 Phase 5 boundary preserved | No retrieval/reranker/cutover/Phase 5 code executed | PASS |

## Failed, skipped and not verified

- **Initial Incident in Task 7 Step 2:**
  - During the first run of Candidate 1 (`e5-small-384`), a mapping bug occurred in `backend/vectorstore/upsert.py:194` (`TypeError: 'set' object is not subscriptable`).
  - Pipeline halted fail-closed immediately without writing a final build record or proceeding to subsequent candidates.
  - Resolved via **Correction 2** (one-line fix changing set comprehension to dict comprehension).
  - User approved guarded reset with `DELETE hue_full_corpus_a_e5_small_384`. Target was verified absent, and Clean Rebuild proceeded cleanly from Candidate 1 through Candidate 4.
- **Skipped / Not Verified Items:**
  - **Zero skipped candidates:** All four candidates completed full builds, upserts, payload comparisons, sample vector verifications, and record writes.
  - Retrieval benchmarking, hybrid fusion (RRF), cross-encoder reranking, and collection cutover are explicitly outside Phase 4 scope and deferred to Phase 5 & Phase 8.

## Limitations and Reviewer handoff

- Candidate 4 (`qwen3-embedding-0.6b-1024`) ran on local GTX 1650 (4GB VRAM) in CUDA FP16 eager batch 1 mode, taking ~65 minutes. Memory usage remained safe (peak ~1.26 GB VRAM), but throughput on 4GB non-TensorCore GPUs is slow. For future phases or larger models, offloading to remote GPU batch workers (e.g. Google Colab T4 / Vast.ai via batch artifact transfer) has been researched and documented.
- Foods collections (`hue_foods_e5_small_384` and `hue_foods_e5_small_384_dense`) remain read-only and intact at 572 points.

This report is Implementer evidence and does not constitute Reviewer approval or User closure.
