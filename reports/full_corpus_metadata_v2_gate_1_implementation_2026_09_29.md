# Full-corpus Metadata v2 Gate 1 Implementation Report

Implementer: Gemini Implementer
Date: 2026-09-29 +07
Status: complete (Correction 3 applied) — stopped at Gate 2 boundary
Authority: User approved Metadata v2 Gate 1 (Tasks 1–4) & Reviewer Correction 3 Handoff
Git authorization: none
Live Qdrant write/cutover authorization: none (Gate 2/3 pending User approval)

---

## 1. Authority, gates and repository state

- **User authorization:** Ngày 2026-09-29, User chính thức phê duyệt Full-corpus Metadata v2 Written Spec, Implementation Plan và cấp quyền triển khai riêng **Gate 1 / Tasks 1–4**.
- **Correction 3 Authority:** Bàn giao correction từ Reviewer (`session_prompt/CURRENT_HANDOFF.md`) yêu cầu giải quyết Major finding duy nhất (**C2-R1**) theo `reports/full_corpus_metadata_v2_gate_1_correction_2_codex_review_2026_09_29.md` trong một batch duy nhất.
- **Ranh giới an toàn nghiêm ngặt:**
  - Tuyệt đối không chạy `migrate` hoặc tạo/ghi/upsert collection trong Qdrant trên môi trường production/live.
  - Không ghi build record v2 thực tế trong Gate 1.
  - Không cutover runtime retrieval (Gate 3).
  - Không tải dense embedding model, không re-encode text, không refit sparse state, không gọi paid API.
  - Không thao tác Git (`git_authorization: none`).
- **Worktree baseline:**
  - Giữ nguyên các thay đổi staged (`D knowledge-base-hue/**`) từ việc untrack corpus trước đó.
  - Giữ nguyên các file untracked (`PROJECT_DOCUMENT_REGISTRY.md` và các báo cáo Phase 5).
  - Mọi thay đổi nằm chính xác trong các paths được cấp phép của Gate 1.

---

## 2. Changed paths and responsibilities

| Path | Action | Trách nhiệm |
|---|---|---|
| `backend/core/schema.py` | Modify | Thêm `FULL_CORPUS_DOMAINS`, hàm `domain_for_source()`, `validate_chunk_id()`, thuộc tính `FullCorpusChunk.domain` và payload 7 trường. |
| `backend/ingestion/full_corpus_pipeline.py` | Modify | Thêm `metadata_v2_collection_name` vào `FullCorpusCandidate` và đăng ký 4 target metadata v2 cố định. |
| `backend/ingestion/source_state.py` | Modify | Thêm `FULL_CORPUS_BUILD_SCHEMA_V2`, `FULL_CORPUS_PAYLOAD_SCHEMA_V2` và constructor `make_full_corpus_metadata_v2_build_record()`. |
| `backend/vectorstore/points.py` | Modify | Cập nhật validation điểm dữ liệu và tạo batch điểm dữ liệu sang payload 7 trường kèm ràng buộc `validate_chunk_id()`. |
| `backend/tests/test_full_corpus_sparse.py` | Modify | Sửa synthetic source path trong test sparse từ `knowledge-base-hue/foods/test.md` về `foods/test.md`. |
| `backend/tests/test_full_corpus_chunker.py` | Modify | Thêm unit tests cho `domain_for_source()`, `validate_chunk_id()`, payload 7 trường và chuẩn hóa synthetic doc paths (`foods/`). |
| `backend/tests/test_full_corpus_qdrant_ingestion.py` | Modify | Cập nhật assertions payload 7 trường, kiểm tra reject invalid chunk IDs và test constructor build record v2. |
| `backend/ingestion/full_corpus_metadata_v2.py` | Modify | Triển khai primitives, fail-closed preflight, sanitized dependency error handling, lineage verification, pre-write SHA revalidation gate, duplicate candidate rejection. |
| `backend/tests/test_full_corpus_metadata_v2.py` | Modify | Bộ test focused (65 tests) bao phủ deterministic mocks, negative probes cho C1-R1..C1-R3, regression tests cho C2-R1, zero mutations và CLI duplicate rejection. |
| `reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json` | Generate | Tracked artifact preflight được sinh lại fresh từ real read-only preflight, xác nhận READY cho 4 cặp, 0 mutations, SHA `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b`. |

---

## 3. Resolution of Correction 3 Finding (C2-R1)

### C2-R1 Major — Ràng buộc SHA ghi lineage với SHA preflight
- **Vấn đề trước correction:** `run_migration()` bỏ qua SHA đã được preflight xác minh và đọc lại file legacy source record mới mà không so sánh với preflight SHA, có thể dẫn đến việc ghi nhận một unvalidated SHA vào v2 build record nếu file trên đĩa bị thay đổi sau preflight.
- **Giải pháp:**
  1. Lấy exact `source_build_record_sha256` từ candidate result của `run_preflight()`:
     ```python
     preflight_cand = preflight["candidates"][0]
     preflight_source_sha = preflight_cand.get("source_build_record_sha256", "")
     if not preflight_source_sha:
         raise RuntimeError(f"Preflight did not return source_build_record_sha256 for {pair.candidate_id}")
     ```
  2. Sau khi hoàn thành upsert và sau khi target collection verification vượt qua 100% (`run_verify(require_build_record=False)`), ngay trước khi ghi final build record v2, thực hiện re-validation gate:
     ```python
     source_record_path = BUILD_RECORD_ROOT / f"{pair.source_collection}.json"
     try:
         current_source_bytes = source_record_path.read_bytes()
         current_source_sha = hashlib.sha256(current_source_bytes).hexdigest()
     except Exception as exc:
         raise RuntimeError(
             f"Failed reading legacy source build record before final write: {type(exc).__name__}"
         ) from exc

     if current_source_sha != preflight_source_sha:
         raise RuntimeError(
             f"Legacy source build record SHA changed after preflight: "
             f"preflight={preflight_source_sha} != current={current_source_sha}"
         )
     ```
  3. Chỉ truyền `preflight_source_sha` đã được đối chiếu khớp với `current_source_sha` vào `make_full_corpus_metadata_v2_build_record()`.
  4. Nếu file source record bị sửa đổi hoặc bị xóa giữa preflight và record write: raise `RuntimeError`, tuyệt đối **không ghi target build record v2**, giữ nguyên partial target collection trong Qdrant để chẩn đoán, không cleanup/delete.
  5. Bổ sung 2 deterministic regression tests trong `test_full_corpus_metadata_v2.py`:
     - `test_migration_fails_when_source_record_modified_after_preflight`: sửa file legacy record trong quá trình upsert -> revalidation gate phát hiện mismatch, raise `RuntimeError`, target record không tồn tại, partial target collection còn nguyên.
     - `test_migration_fails_when_source_record_deleted_after_preflight`: xóa file legacy record trong quá trình upsert -> revalidation gate phát hiện missing file, raise `RuntimeError`, target record không tồn tại, partial target collection còn nguyên.

---

## 4. Fresh Verification Results

### Focused Test Suite (4 suites, 133 tests):
```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py -q --tb=short
```
**Kết quả:**
```text
133 passed in 122.90s (0:02:02)
```
*(Trong đó `backend/tests/test_full_corpus_metadata_v2.py` đạt 65/65 tests pass).*

### Whitespace Cleanliness:
```bash
git diff --check
```
**Kết quả:** Exit code `0`, không có whitespace error hoặc trailing whitespace nào.

### Real Read-only Preflight:
```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json
```
**Kết quả quan sát:**
- Exit code: `0`
- Output: `Preflight status: READY`
- Summary: `total_pairs: 4`, `ready_pairs: 4`, `blocked_pairs: 0`, `total_mutations: 0`
- Artifact SHA-256: `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b` (byte-identical với artifact được Reviewer xác nhận).
- Chi tiết 4 candidate collections:
  1. `e5-small-384`: source `hue_full_corpus_a_e5_small_384` (8.460 points validated), target absent, target record absent, status: `READY`.
  2. `e5-base-768`: source `hue_full_corpus_a_e5_base_768` (8.460 points validated), target absent, target record absent, status: `READY`.
  3. `huydang-dek21-768`: source `hue_full_corpus_a_huydang_dek21_768` (8.460 points validated), target absent, target record absent, status: `READY`.
  4. `qwen3-embedding-0.6b-1024`: source `hue_full_corpus_a_qwen3_06b_1024` (8.460 points validated), target absent, target record absent, status: `READY`.
- Toàn bộ 33.840 legacy points qua 4 collections đã được kiểm tra đối chiếu sâu giá trị 5 trường với fresh canonical chunks.
- Observed build record hashes và corpus identity hoàn toàn khớp với v1 build records.

---

## 5. Privacy and Sanitization Audit

Artifact `reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json`:
- Không chứa file paths hoặc file map 205 tài liệu.
- Không chứa point text, search text hay chunk IDs.
- Không chứa dense vectors hay sparse vectors.
- Không chứa queries, user text hay secret credentials.
- Chỉ chứa allowlisted metadata: candidate IDs, collection names, dimensions, validated point counts, observed SHA256 hashes, absent flags, status, và errors list.

---

## 6. Zero-mutation and Gate 2 Boundaries

- `total_mutations: 0`: Hoàn toàn không có mutation nào đối với Qdrant (0 collections created, 0 points upserted/modified/deleted).
- Chưa có file build record v2 nào được tạo trong `data/full_corpus_builds/`.
- Không tải dense embedding runner/model, không re-embedding.
- Không chạy `migrate` trên bất kỳ candidate nào.
- Dừng chính xác tại Gate 2 boundary.

---

## 7. Failed, Skipped and Not Verified

- **Failed:** Không có. (Tất cả 133 focused tests và preflight đều PASS).
- **Skipped:**
  - Task 5: Live migration (`migrate`) trên Qdrant — bị chặn bởi Gate 2 checkpoint.
  - Task 6: Gate 3 cutover runtime retrieval — ngoài phạm vi Gate 1.
  - Task 7: Final full backend regression — ngoài phạm vi Gate 1.
- **Not verified:**
  - Real post-write target verification trên Qdrant thật (vì chưa thực hiện write nào trong Gate 1; logic đã được chứng minh qua 65 focused unit tests).

---

## 8. Bàn giao cho Reviewer

Reviewer có thể thẩm định độc lập theo các lệnh chuẩn:
```bash
git status --short
git diff --check
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output /tmp/full_corpus_metadata_v2_reviewer_preflight_c3.json
```
Implementer dừng công việc và bàn giao lại Reviewer để tiến hành final review cho Gate 1.
