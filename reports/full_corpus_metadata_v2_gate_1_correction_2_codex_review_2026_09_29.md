# Codex Review: Full-corpus Metadata v2 Gate 1 Correction 2

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-29 +07
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_metadata_v2_gate_1_implementation_2026_09_29.md`
Prior review: `reports/full_corpus_metadata_v2_gate_1_correction_1_codex_review_2026_09_29.md`

## 1. Phạm vi đã review

Reviewer đọc đầy đủ Correction 2 handoff/report, source/test delta và fresh
preflight artifact; đối chiếu trực tiếp ba finding C1-R1..C1-R3 với Written
Spec, Plan và tiêu chí đóng trong prior review. Review tập trung vào sanitized
fail-closed behavior, exact v2 build-record lineage và duplicate selector
gating. Không chạy `migrate` thật, không ghi build record v2 và không mutation
Qdrant.

Kết quả:

- C1-R1 sanitized dependency failures: đóng.
- C1-R3 duplicate candidate selectors: đóng.
- C1-R2 full v2 record checks và final verifier: phần verifier đã đóng; đường
  write còn một lineage gap dưới đây.

## 2. Findings

### C2-R1 — Major: migration không ràng buộc SHA ghi lineage với SHA đã preflight

- **Vị trí:** `backend/ingestion/full_corpus_metadata_v2.py:787-795`,
  `backend/ingestion/full_corpus_metadata_v2.py:829-854`; tests
  `backend/tests/test_full_corpus_metadata_v2.py:865-931`.
- **Requirement:** tiêu chí đóng C1-R2 yêu cầu SHA dùng để ghi v2 record vẫn là
  SHA vừa được preflight/revalidated. Legacy source record là immutable input;
  nếu exact bytes thay đổi sau preflight, migration phải fail closed trước khi
  tạo final build record.
- **Evidence:** `run_preflight()` trả
  `candidates[0].source_build_record_sha256`, nhưng `run_migration()` không đọc
  hoặc so sánh giá trị đó. Hàm đọc source record lần nữa ở dòng 793–794 rồi
  dùng SHA mới trực tiếp ở dòng 843. Probe cô lập cho preflight SHA A và đổi
  bytes thành SHA B sau preflight quan sát `migration_status=MIGRATED`,
  `preflight_sha_reused=False`, `changed_unvalidated_sha_used=True`.
- **Tác động:** build record v2 có thể tuyên bố lineage tới exact legacy bytes
  chưa hề vượt qua preflight validation. Final `run_verify()` chỉ chứng minh
  target record khớp file hiện tại, không chứng minh file đó là file đã được
  preflight chấp nhận.
- **Tiêu chí đóng:** lấy exact source-record SHA từ successful single-pair
  preflight; ngay trước final record write, đọc lại exact legacy bytes và yêu
  cầu SHA hiện tại bằng SHA preflight. Chỉ dùng SHA đã so khớp để tạo v2 record.
  Mismatch/missing/parse failure phải dừng trước record write, giữ partial target
  để chẩn đoán và không tự xóa. Thêm deterministic test thay đổi source record
  giữa preflight và write, assert failure và target v2 record không tồn tại.

## 3. Cách Reviewer chạy lại thật

```bash
git diff --check
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output /tmp/full_corpus_metadata_v2_reviewer_preflight_c2.json
```

Reviewer còn chạy một pure mocked migration probe: preflight trả SHA A, source
record trả bytes có SHA B trước write, còn Qdrant client và record writer đều là
fakes không có external mutation.

## 4. Kết quả quan sát

- `git diff --check`: PASS.
- Focused suite: `131 passed in 139.65s`.
- Fresh real read-only preflight: exit `0`, `READY`, 4/4 pairs, 8.460 points
  mỗi source, targets/build records absent và `total_mutations: 0`.
- Reviewer artifact byte-identical với tracked artifact; SHA-256 cùng là
  `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b`.
- Privacy scan trên artifact: sạch đối với private absolute path, corpus text,
  payload field names và synthetic secret markers.
- C1-R1 negative tests và static inspection xác nhận exception messages chỉ
  phát safe stage + exception type; Qdrant inspection exceptions thành
  structured failure.
- C1-R3 static inspection xác nhận duplicate guard chạy trước
  `load_settings()`/`client_from_settings()`; function-level guards cũng có.
- Lineage mutation probe: FAILED theo acceptance; unvalidated SHA mới vẫn được
  dùng để hoàn tất migration.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không chạy real `migrate`, create/upsert, post-write Qdrant verify,
build-record v2 write, dense model hoặc Gate 3 path. Fresh preflight có phát
warning tokenizer length từ corpus preparation nhưng hoàn tất thành công; không
có evidence về dense embedding/model execution hay mutation. Lineage gap được
tái hiện hoàn toàn bằng fakes để không vượt Gate 1 authority.

## 6. Decision và bước tiếp theo

Decision: `changes_requested`. Gate 2 vẫn đóng. Correction 3 chỉ sửa C2-R1 và
test regression tương ứng; không mở lại các finding đã đóng, không chạy migrate
thật và không thay đổi Written Spec/Plan/runtime retrieval. Sau fresh focused
suite và four-pair read-only preflight, trả Reviewer final review lần nữa.
