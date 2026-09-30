# Implementation Report: Full-corpus Metadata v2 Gate 3 / Task 6

Implementer: Gemini Implementer
Date: 2026-09-30 +07
Status: complete — strict runtime cutover implemented, all startup invariants & lineage validated, payload validation errors sanitized, all focused regression tests passed, fresh read-only smoke passed
Canonical guide: `guides/full_corpus_rag.md`
Spec: `docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md`
Plan: `docs/superpowers/plans/2026-09-29-full-corpus-metadata-v2-implementation-plan.md`
Review findings addressed: F1, F2, F3 from `reports/full_corpus_metadata_v2_gate_3_codex_review_2026_09_29.md`
User Authorization: Phê duyệt Gate 3 / Task 6
Git authorization: none
Risk level: high

---

## 1. Phạm vi

- **Được duyệt:**
  - Thực hiện chuyển đổi runtime retrieval sang các metadata-v2 collections (`<collection>_metadata_v2`).
  - Thiết lập cơ chế kiểm tra tính hợp lệ nghiêm ngặt (strict validation) khi khởi tạo service và xử lý payload retrieval:
    - Bắt buộc kiểm tra v2 build record (`schema_version: "phase_4_full_corpus_build:v2"`).
    - Bắt buộc kiểm tra `record.collection_name == candidate.metadata_v2_collection_name`.
    - Bắt buộc kiểm tra `migration.source_build_record_sha256` khớp chính xác với SHA-256 tính từ toàn bộ bytes của legacy build record (`data/full_corpus_builds/<candidate.collection_name>.json`).
    - Bắt buộc kiểm tra các trường Qdrant trong build record: `dense_vector_name == "dense"`, `sparse_vector_name == "sparse"`, `distance == "cosine"`, `point_count == 8460`, và `payload_schema_version == "full_corpus_qdrant_payload:v2"`.
    - Bắt buộc kiểm tra độ tươi của filesystem corpus (205 files, 8.460 chunks, corpus identity `0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223`). Nếu có file thêm, sửa, xóa sẽ fail-closed ngay lập tức.
    - Bắt buộc kiểm tra live Qdrant target: point count == 8.460, `payload_schema == {}` (zero payload schema indexes).
    - Chiếu chính xác 7 trường canonical (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`) trong `with_payload`.
    - Kiểm tra tính toàn vẹn payload: `domain == domain_for_source(source)`, `chunk_id` có định dạng `<source>#<chunk_index>`, và point UUID khớp chính xác với `point_id_for_chunk_id(chunk_id)`.
    - Khử hoàn toàn rò rỉ dữ liệu riêng tư trong thông báo lỗi payload: chỉ chứa safe `point_id` (UUID) và generic reason code/mô tả tổng quát, tuyệt đối không interpolate `source`, `chunk_id`, `search_text`, `evidence_parts` hoặc đường dẫn tuyệt đối.
    - Bảo đảm `RetrievedDocument` có `id == chunk_id` và metadata chứa `domain`.
    - Bảo đảm technical trace (`RetrievalTrace`) tuân thủ allowlist an toàn (`point_id`, `chunk_id`, `domain`, `rank`, `score`), không rò rỉ text, payload thô, secrets hay đường dẫn tuyệt đối.
  - Bổ sung bộ unit tests nghiêm ngặt và privacy probe tests.
  - Chạy bộ kiểm thử hồi quy tập trung (focused regression suite).
  - Thực thi fresh smoke test truy vấn thực tế ở chế độ read-only (8 cells no-rerank + 2 cells MiniLM).
- **Ranh giới nghiêm ngặt:**
  - Mọi Qdrant collection (4 legacy + 4 metadata-v2) và build records đều giữ trạng thái chỉ đọc (read-only). Không có bất kỳ mutation nào được thực hiện lên database.
  - Không tự ý mở rộng sang Task 7 (full backend test suite) hay Phase 6.
  - Không thao tác Git (`git_authorization: none`).
  - Không rò rỉ nội dung văn bản corpus, câu hỏi truy vấn riêng tư, secrets hay đường dẫn tuyệt đối trong báo cáo.

---

## 2. Thay đổi chính

| Đường dẫn | Thao tác | Mô tả |
|---|---|---|
| `backend/retrieval/full_corpus.py` | Update | Chuyển đổi runtime retrieval sang metadata-v2 collections: cập nhật `REQUIRED_PAYLOAD_FIELDS` thành 7 trường canonical (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`); kiểm tra v2 build record (`phase_4_full_corpus_build:v2`), target collection, exact legacy lineage SHA-256 bytes, build-record Qdrant invariants (`dense`, `sparse`, `cosine`, 8460 points), freshness corpus, và collection info khi khởi tạo; khử hoàn toàn rò rỉ source/chunk_id trong payload validation exceptions; giới hạn allowlist trong technical trace (`point_id`, `chunk_id`, `domain`, `rank`, `score`); trả về `RetrievedDocument(id=chunk_id, metadata={"domain": domain, ...})`. |
| `backend/tests/test_full_corpus_retrieval.py` | Update | Bổ sung và cập nhật test cases: kiểm tra từ chối wrong target, bad lineage SHA, malformed lineage SHA, wrong dense/sparse vector name, wrong distance, wrong point count; bổ sung privacy probe test kiểm tra thông báo lỗi payload tuyệt đối không chứa marker riêng tư, source, chunk_id hay đường dẫn; cập nhật các mock payloads tương thích v2 schema và compute exact legacy build record SHA cho các test build record/freshness. |
| `session_prompt/CURRENT_HANDOFF.md` | Update | Cập nhật bàn giao sang vai trò Reviewer, chuẩn hóa formatting, loại bỏ trailing whitespace để bảo đảm `git diff --check` sạch hoàn toàn. |

---

## 3. Quy trình thực hiện & Sửa đổi Correction 1

### Bước 1 — Xử lý F1: Exact startup target, lineage SHA và Qdrant invariants
Cập nhật `validate_full_corpus_build_record` trong `backend/retrieval/full_corpus.py`:
- Kiểm tra `record.collection_name == candidate.metadata_v2_collection_name`.
- Đọc exact legacy build record từ `BUILD_RECORDS_DIR / f"{candidate.collection_name}.json"`, tính SHA-256 từ file bytes thực tế và đối chiếu với `migration.source_build_record_sha256`.
- Kiểm tra `qdrant.dense_vector_name == "dense"`, `qdrant.sparse_vector_name == "sparse"`, `qdrant.distance == "cosine"`, và `qdrant.point_count == 8460`.
- Thêm các unit test cases trong `test_v2_build_record_rejects_wrong_build_or_payload_schema` chứng minh từng trường hợp sai target, sai lineage SHA, malformed lineage SHA, sai tên vector, sai khoảng cách, sai số lượng point, hoặc thiếu file legacy record đều bị từ chối fail-closed.

### Bước 2 — Xử lý F2: Sanitize payload validation errors
Cập nhật `validate_point_payload` trong `backend/retrieval/full_corpus.py`:
- Thay thế toàn bộ các thông báo lỗi có interpolate `chunk_id`, `source`, `domain`, `expected_point_id` bằng các thông báo an toàn chỉ chứa safe `point_id` (UUID) và generic reason code.
- Sử dụng `from None` để dập tắt exception chaining, ngăn chặn rò rỉ đường dẫn từ các hàm phụ trợ bên dưới.
- Thêm test `test_v2_payload_validation_errors_never_leak_private_paths_or_text` với các marker riêng tư bảo đảm không rò rỉ source, chunk_id, text, hay absolute path trong 4 kịch bản lỗi: invalid chunk relation, point UUID mismatch, invalid source cho domain derivation, và domain mismatch.

### Bước 3 — Xử lý F3: Chuẩn hóa báo cáo, schema, và hygiene
- Cập nhật Risk level thành `high`.
- Liệt kê chính xác 7 trường canonical v2: `search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`.
- Sử dụng đúng schema literal `phase_4_full_corpus_build:v2` và `full_corpus_qdrant_payload:v2`.
- Phân biệt rõ phạm vi thay đổi của Task 6 với trạng thái staged/untracked có sẵn từ trước.
- Loại bỏ toàn bộ trailing whitespace, bảo đảm `git diff --check` đạt exit code 0.

### Bước 4 — Kiểm thử Unit & Hồi quy tập trung
1. **Unit tests (`backend/tests/test_full_corpus_retrieval.py`):**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py -v
   ```
   - Kết quả: **25 passed in 5.49s**, 0 failed.

2. **Focused regression suite (116 tests):**
   ```bash
   HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest \
     backend/tests/test_full_corpus_retrieval.py \
     backend/tests/test_full_corpus_qdrant_ingestion.py \
     backend/tests/test_full_corpus_metadata_v2.py \
     backend/tests/test_full_corpus_sparse.py -q --tb=short
   ```
   - Kết quả: **116 passed in 6.74s**, 0 failed, 0 warnings.

### Bước 5 — Fresh read-only retrieval smoke runs
Chạy lại fresh toàn bộ smoke test sau khi đã sửa logic startup lineage:

1. **8 cells no-rerank (4 candidates × 2 treatments × query P5-Q01):**
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run \
  --candidate e5-small-384 e5-base-768 huydang-dek21-768 qwen3-embedding-0.6b-1024 \
  --treatment dense_bm25_rrf native_hybrid_rrf \
  --reranker none \
  --select P5-Q01 \
  --output data/full_corpus_metadata_v2_smoke.json
```
- Kết quả: **PASS on all 8 cells** (exit code `0`).
- Determinism pass: `True` trên toàn bộ 8 cells, anomalies: `[]`.
- Latency p95:
  - `e5-small-384__dense_bm25_rrf__none`: 95.8 ms
  - `e5-small-384__native_hybrid_rrf__none`: 35.1 ms
  - `e5-base-768__dense_bm25_rrf__none`: 172.4 ms
  - `e5-base-768__native_hybrid_rrf__none`: 52.5 ms
  - `huydang-dek21-768__dense_bm25_rrf__none`: 51.0 ms
  - `huydang-dek21-768__native_hybrid_rrf__none`: 56.1 ms
  - `qwen3-embedding-0.6b-1024__dense_bm25_rrf__none`: 224.3 ms
  - `qwen3-embedding-0.6b-1024__native_hybrid_rrf__none`: 223.7 ms
- Trace artifact: `data/full_corpus_metadata_v2_smoke.json` (gitignored).

2. **2 cells MiniLM reranker (candidate `e5-small-384` × 2 treatments × query P5-Q01):**
```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run \
  --candidate e5-small-384 \
  --treatment dense_bm25_rrf native_hybrid_rrf \
  --reranker minilm \
  --select P5-Q01 \
  --output data/full_corpus_metadata_v2_minilm_smoke.json
```
- Kết quả: **PASS on all 2 cells** (exit code `0`, 21 warm observations mỗi cell).
- Determinism pass: `True`.
- Latency p95:
  - `e5-small-384__dense_bm25_rrf__minilm`: 1475.2 ms (< 3000 ms latency gate).
  - `e5-small-384__native_hybrid_rrf__minilm`: 1197.8 ms (< 3000 ms latency gate).
- Trace artifact: `data/full_corpus_metadata_v2_minilm_smoke.json` (gitignored).

---

## 4. Xác nhận an toàn & Ranh giới Git / Database

1. **Legacy Collections & Targets:**
   - 4 legacy collections và 4 metadata-v2 collections hoàn toàn nguyên vẹn, không có mutation nào. Mỗi metadata-v2 target có đúng 8.460 points và `payload_schema == {}`.
2. **Build Records:**
   - Tất cả các build records trong `data/full_corpus_builds/` chỉ được đọc để kiểm tra lineage bytes và schema; không bị sửa đổi hay ghi đè.
3. **Git Workspace Hygiene:**
   - `git diff --check` sạch hoàn toàn, không có lỗi whitespace hay trailing newline.
   - Các tệp thay đổi thực tế của Task 6:
     - `backend/retrieval/full_corpus.py`
     - `backend/tests/test_full_corpus_retrieval.py`
     - `session_prompt/CURRENT_HANDOFF.md`
   - Toàn bộ staged deletions trong `knowledge-base-hue/` và các untracked reports trước đó được bảo toàn nguyên vẹn, không bị commit hay clean.

---

## 5. Kết luận

Correction 1 cho Gate 3 / Task 6 đã hoàn thành trọn vẹn mọi yêu cầu F1, F2 và F3.
Trạng thái hệ thống đã sẵn sàng cho Reviewer thực hiện independent final review.
