# Implementation Report: Full-corpus Metadata v2 Gate 2 / Task 5

Implementer: Gemini Implementer
Date: 2026-09-29 +07
Status: complete — 4/4 targets migrated, verified and build records created
Canonical guide: `guides/full_corpus_rag.md`
Spec: `docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md`
Plan: `docs/superpowers/plans/2026-09-29-full-corpus-metadata-v2-implementation-plan.md`
User Authorization: Phê duyệt Gate 2 / Task 5 ngày 2026-09-29 +07
Git authorization: none
Risk level: high

---

## 1. Phạm vi

- **Được duyệt:**
  - Migrate tuần tự đúng 4 target metadata-v2 đã khóa:
    - `hue_full_corpus_a_e5_small_384_metadata_v2`
    - `hue_full_corpus_a_e5_base_768_metadata_v2`
    - `hue_full_corpus_a_huydang_dek21_768_metadata_v2`
    - `hue_full_corpus_a_qwen3_06b_1024_metadata_v2`
  - Create collection và upsert copied vectors từ immutable source sang fresh target kèm payload 7 trường canonical (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`).
  - Ghi 4 matching final v2 build records tại `data/full_corpus_builds/`.
  - Sinh/cập nhật `data/full_corpus_metadata_v2_execution.json` (ignored).
  - Cập nhật fresh preflight artifact và `session_prompt/CURRENT_HANDOFF.md`.
- **Ranh giới nghiêm ngặt:**
  - Không xóa, dọn dẹp (cleanup/delete) hoặc reconcile partial targets hay legacy collections.
  - Không tải dense embedding model, không re-encode vectors, không gọi external/paid API.
  - Không cutover runtime retrieval (thuộc Gate 3).
  - Không thao tác Git (`git_authorization: none`).
- **Thực tế thực hiện:**
  - Hoàn tất 100% phạm vi được duyệt cho Gate 2 / Task 5 mà không vi phạm bất kỳ ranh giới an toàn nào.

---

## 2. Thay đổi chính

| Đường dẫn | Thao tác | Mô tả |
|---|---|---|
| Qdrant collections | Create/Upsert | Tạo mới 4 collection metadata-v2 với đúng 8.460 points/collection (tổng 33.840 points), schema vector gốc, payload 7 trường và `payload_schema == {}`. |
| `data/full_corpus_builds/hue_full_corpus_a_e5_small_384_metadata_v2.json` | Create | Build record v2 cho candidate `e5-small-384`, SHA: `41d41bd5fb96ca7146216d002c576a8cda1712a2fb1882600ed0fb80616fd196`. |
| `data/full_corpus_builds/hue_full_corpus_a_e5_base_768_metadata_v2.json` | Create | Build record v2 cho candidate `e5-base-768`, SHA: `922c5aae699169e0773b4cd0ccd32acfd3fa3320419d0edafa418078dc1b4d5f`. |
| `data/full_corpus_builds/hue_full_corpus_a_huydang_dek21_768_metadata_v2.json` | Create | Build record v2 cho candidate `huydang-dek21-768`, SHA: `287307ec5e250c07252e9088b8d4f483440a51382efc82eb3bbf9b0a9542d60c`. |
| `data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024_metadata_v2.json` | Create | Build record v2 cho candidate `qwen3-embedding-0.6b-1024`, SHA: `40ebf9a94e06aaccfa1e0163c514fe3ebdca75fe1f4f665c7d068dddb2d3414a`. |
| `data/full_corpus_metadata_v2_execution.json` | Create (ignored) | Ghi nhận chi tiết toàn bộ chuỗi lệnh, trạng thái preflight, per-target counts, lineage SHA, tính bất biến legacy và confirmations an toàn. |
| `reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json` | Re-verified | Fresh preflight artifact xác nhận trạng thái READY, SHA: `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b`. |

---

## 3. Cách đã chạy thật

Tất cả các lệnh được thực thi tuần tự trên máy chủ với biến môi trường `.env` an toàn:

### Bước 1 — Reconfirm focused tests và preflight trước write
```bash
# 1. Chạy lại bộ focused tests (133 tests)
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py -q --tb=short

# 2. Fresh read-only preflight
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json
```

### Bước 2 — Migrate và verify tuần tự từng cặp
```bash
# Pair 1: e5-small-384
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 migrate --candidate e5-small-384 --confirm-target hue_full_corpus_a_e5_small_384_metadata_v2
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify --candidate e5-small-384

# Pair 2: e5-base-768
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 migrate --candidate e5-base-768 --confirm-target hue_full_corpus_a_e5_base_768_metadata_v2
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify --candidate e5-base-768

# Pair 3: huydang-dek21-768
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 migrate --candidate huydang-dek21-768 --confirm-target hue_full_corpus_a_huydang_dek21_768_metadata_v2
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify --candidate huydang-dek21-768

# Pair 4: qwen3-embedding-0.6b-1024
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 migrate --candidate qwen3-embedding-0.6b-1024 --confirm-target hue_full_corpus_a_qwen3_06b_1024_metadata_v2
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify --candidate qwen3-embedding-0.6b-1024
```

### Bước 3 — Final combined verification và git diff check
```bash
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
git diff --check
```

---

## 4. Kết quả quan sát

### 4.1. Preflight trước write
- Exit code: `0`
- Trạng thái: `READY`
- Tổng pairs: `4/4 READY`, `0 BLOCKED`, `total_mutations: 0`
- Preflight artifact SHA-256: `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b`

### 4.2. Quá trình Migrate và Verify tuần tự
1. **`e5-small-384`:**
   - Migrate: Exit `0`, `upserted_points: 8460`, build record SHA `41d41bd5fb96ca7146216d002c576a8cda1712a2fb1882600ed0fb80616fd196`, `status: MIGRATED`.
   - Verify: Exit `0`, `status: VERIFIED`.
2. **`e5-base-768`:**
   - Migrate: Exit `0`, `upserted_points: 8460`, build record SHA `922c5aae699169e0773b4cd0ccd32acfd3fa3320419d0edafa418078dc1b4d5f`, `status: MIGRATED`.
   - Verify: Exit `0`, `status: VERIFIED`.
3. **`huydang-dek21-768`:**
   - Migrate: Exit `0`, `upserted_points: 8460`, build record SHA `287307ec5e250c07252e9088b8d4f483440a51382efc82eb3bbf9b0a9542d60c`, `status: MIGRATED`.
   - Verify: Exit `0`, `status: VERIFIED`.
4. **`qwen3-embedding-0.6b-1024`:**
   - Migrate: Exit `0`, `upserted_points: 8460`, build record SHA `40ebf9a94e06aaccfa1e0163c514fe3ebdca75fe1f4f665c7d068dddb2d3414a`, `status: MIGRATED`.
   - Verify: Exit `0`, `status: VERIFIED`.

### 4.3. Final Combined Verification
- Exit code: `0`
- Kết quả: `Verification status: VERIFIED`
- Toàn bộ 4/4 target collections đã được kiểm tra:
  - Đúng 8.460 IDs trên mỗi target (tổng 33.840 points).
  - Exact 7 fields payload (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`, `chunk_id`, `domain`).
  - Toàn bộ dense và sparse vectors khớp 100% giá trị nguồn.
  - `payload_schema == {}` trên cả 4 target (không tự tạo payload index).
  - Khớp exact v2 lineage record và SHA v1 tương ứng.
- `git diff --check`: Exit `0`, sạch định dạng và whitespace.

### 4.4. Bằng chứng bất biến của 4 Legacy Collections
Đối soát sau write cho thấy 4 collection legacy và 4 file build record v1 hoàn toàn không đổi so với trạng thái Gate 1:
- `hue_full_corpus_a_e5_small_384`: 8.460 points, v1 SHA `ea19021a57c1adb9b283b3198d4883d26f0f18a2451eaf2eaafc815f83571c76` (khớp).
- `hue_full_corpus_a_e5_base_768`: 8.460 points, v1 SHA `0cd69406b4bc8ab17953ea0abac3c93011660882cf34c85b0b8645b095ea9d7b` (khớp).
- `hue_full_corpus_a_huydang_dek21_768`: 8.460 points, v1 SHA `10b3f847d9e30bf06acc0e21d83a1cb4b166455bef45c0dd3d5703b3f8371c4a` (khớp).
- `hue_full_corpus_a_qwen3_06b_1024`: 8.460 points, v1 SHA `2faa9d4f102127093c0ebd5c14c19eef3bd7743ca0e34d434beb5aa40919bdd5` (khớp).

---

## 5. Lỗi và giới hạn

- **Lỗi:** Không có. Không xảy ra bất kỳ lỗi hoặc dị thường nào trong toàn bộ chuỗi di chuyển và kiểm chứng.
- **Giới hạn đã tuân thủ nghiêm ngặt:**
  - Không xóa/dọn dẹp bất kỳ collection nào.
  - Không tải model dense embedding, không re-encode vectors, không gọi API ngoài.
  - Không cutover runtime retrieval (chờ Gate 3 được User phê duyệt).
  - Giữ nguyên các thay đổi staged và untracked không liên quan theo đúng `git_authorization: none`.

---

## 6. Handoff cho Reviewer

- **Tài liệu bàn giao:**
  - Báo cáo này: `reports/full_corpus_metadata_v2_gate_2_implementation_2026_09_29.md`
  - Hồ sơ thực thi chi tiết: `data/full_corpus_metadata_v2_execution.json`
  - Bốn hồ sơ v2 build records: `data/full_corpus_builds/*_metadata_v2.json`
- **Lệnh tối thiểu để Reviewer thẩm định độc lập:**
  ```bash
  UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify
  ```
- **Next action:** Reviewer thực hiện independent final review cho Gate 2 / Task 5, xác nhận tính toàn vẹn của 4 target mới, lineage records và tính bất biến của legacy collections; sau đó tổng hợp báo cáo trình User quyết định việc mở Gate 3 (Runtime cutover).
