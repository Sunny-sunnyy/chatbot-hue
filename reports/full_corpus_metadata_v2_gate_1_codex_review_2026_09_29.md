# Codex Review: Full-corpus Metadata v2 Gate 1

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-29 +07
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_metadata_v2_gate_1_implementation_2026_09_29.md`

## 1. Phạm vi đã review

Reviewer đã đọc đầy đủ Written Spec, Implementation Plan/Review Contract,
implementation report, preflight artifact, current handoff và toàn bộ exact
diff/new files của Gate 1. Review bao phủ canonical chunk/payload, candidate
mapping, build-record v2, migration/preflight/verify CLI, focused tests,
privacy của tracked artifact và ranh giới không ghi Qdrant.

Các staged `.gitignore`/corpus untracking và bốn untracked User/historical
files đã có trong baseline được inventory và giữ ngoài phạm vi; không có bằng
chứng chúng bị Gate 1 sửa. HEAD khi review là
`9242178bfe381011dd0d74875181a6a624410de3`.

## 2. Findings

### R1 — Major: preflight fail-open khi không chuẩn bị được canonical corpus

- **Vị trí:** `backend/ingestion/full_corpus_metadata_v2.py:250-258`,
  `backend/ingestion/full_corpus_metadata_v2.py:298-305`,
  `backend/ingestion/full_corpus_metadata_v2.py:368-374`.
- **Requirement:** Task 4 preflight phải fresh-prepare corpus, kiểm source
  hashes/chunks/IDs và fail closed với overall `BLOCKED` trước mọi write nếu
  bước này lỗi.
- **Evidence:** code bắt mọi exception từ `prepare_full_corpus_input()` rồi gán
  `None`, bỏ qua freshness và canonical ID-set checks. Negative probe read-only
  ép preparation ném `RuntimeError` nhưng preflight trên legacy E5-small vẫn
  trả `{'status': 'READY', 'source_points_count': 8460, 'errors': []}`.
- **Tác động:** một corpus không đọc/chunk/validate được vẫn có thể được trình
  là sẵn sàng cho Gate 2; artifact còn ghi các identity constant như observed
  evidence.
- **Tiêu chí đóng:** mọi preparation/dependency failure trở thành sanitized
  `BLOCKED`, non-zero CLI exit và zero mutation; không phát identity/count như
  đã quan sát khi canonical preparation thất bại. Có focused negative test tái
  tạo đúng nhánh này.

### R2 — Major: preflight chưa kiểm exact legacy record/payload contract

- **Vị trí:** `backend/ingestion/full_corpus_metadata_v2.py:275-306`,
  `backend/ingestion/full_corpus_metadata_v2.py:332-353`,
  `backend/ingestion/full_corpus_metadata_v2.py:362-375`.
- **Requirement:** Review Contract yêu cầu từng source record/collection khớp
  exact candidate, current source/corpus/sparse identities, Qdrant schema/count,
  canonical point-ID set và exact five-field legacy payload values.
- **Evidence:** record check chỉ xét schema/status và bốn dense fields; không
  validate `collection_name`, representation, corpus identity/counts/sources,
  sparse schema/hash/vocabulary hoặc qdrant names/distance/count. Point loop chỉ
  kiểm payload field set cùng vài top-level types, không đối chiếu năm legacy
  values với fresh chunk. Artifact xuất `EXPECTED_CORPUS_IDENTITY` và
  `EXPECTED_SPARSE_SHA256` constants thay vì giá trị đã validate từ record.
- **Tác động:** build record hoặc legacy payload sai vẫn có thể nhận `READY`,
  nên claim 33.840 points “khớp chính xác” trong implementation report chưa
  được code/evidence chứng minh.
- **Tiêu chí đóng:** validate toàn bộ locked v1 record fields và exact legacy
  payload của mỗi canonical point trước `READY`; artifact chỉ phát observed
  values đã kiểm. Thêm focused failures cho stale/mismatched record, payload,
  missing/foreign/duplicate IDs và source/target mismatch.

### R3 — Major: write path có thể ghi final v2 record trước complete verification

- **Vị trí:** `backend/ingestion/full_corpus_metadata_v2.py:539-592`.
- **Requirement:** Task 4 khóa `migrate` theo thứ tự preflight → create/copy →
  complete target verification của toàn bộ IDs/payloads/dense+sparse vectors →
  atomic final build-record write.
- **Evidence:** sau upsert, implementation chỉ kiểm `target_info.points_count`
  rồi gọi `write_final_full_corpus_build_record()`; không chạy full equality,
  exact target ID set, payload, vector schema, payload-index hoặc vector-value
  verification trước final record.
- **Tác động:** Gate 2 có thể tạo build record `complete` cho target corrupt hoặc
  sai payload/vector, làm mất ý nghĩa readiness/lineage.
- **Tiêu chí đóng:** final record chỉ được ghi sau complete target verification
  thật; bất kỳ mismatch nào giữ target để điều tra và tuyệt đối không ghi final
  record. Focused recording-client test phải chứng minh mismatch chặn record
  write.

### R4 — Major: `run_verify()` không lấy đúng target IDs theo từng source page

- **Vị trí:** `backend/ingestion/full_corpus_metadata_v2.py:443-483`.
- **Requirement:** Task 3 yêu cầu retrieve cùng IDs từ target cho từng bounded
  source page, so sánh toàn bộ set và phát hiện missing/extra/duplicate point.
- **Evidence:** mỗi vòng luôn `scroll(target, offset=None, limit=len(ids))`, nên
  luôn đọc page đầu của target thay vì đúng IDs/page tương ứng. Target schema
  cũng chưa được validate bằng full collection validator.
- **Tác động:** verification sẽ fail sai từ source page thứ hai hoặc có thể so
  sánh không đúng tập; không thể dùng làm post-write proof của 8.460 points.
- **Tiêu chí đóng:** đối chiếu đúng target records cho exact source-page IDs,
  validate full target schema/payload index/count và toàn expected ID set; tests
  phải phủ ít nhất hai pages cùng missing/extra target cases.

### R5 — Major: orchestration tests không bảo vệ các gate bắt buộc

- **Vị trí:** `backend/tests/test_full_corpus_metadata_v2.py:324-379`.
- **Requirement:** Task 3–4 yêu cầu pure focused tests cho duplicate/foreign/
  missing points, target extra/missing, build-record/source-hash mismatch,
  stale source, unknown/duplicate selectors, preflight BLOCKED/non-zero/zero
  writes và full verification behavior.
- **Evidence:** no-mutation test trên client rỗng chỉ assert key `status` tồn
  tại; `run_verify` tương tự chỉ assert có status. Các required cases trên
  không có. Tests còn tự đọc/chunk toàn corpus thay vì truyền deterministic
  prepared input, nên chậm nhưng vẫn không phát hiện R1–R4.
- **Tác động:** suite `80 passed` không chứng minh migration/readiness safety và
  đã cho phép implementation report kết luận `PASS` quá mức evidence.
- **Tiêu chí đóng:** thêm tập test nhỏ, trực tiếp cho R1–R4 và toàn required
  guards; assert exact outcome/mutation/build-record behavior, không chỉ sự tồn
  tại của một field. Xóa/điều chỉnh test không có giá trị bảo vệ contract.

Implementation report và handoff phải được cập nhật sau correction: bỏ claim
“không deviation”/exact legacy validation cho tới khi có fresh evidence, ghi
đúng failed/skipped/not-verified và dẫn lại commands/results mới.

## 3. Cách Reviewer chạy lại thật

```bash
git status --short
git diff --check
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_metadata_v2.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output /tmp/full_corpus_metadata_v2_reviewer_preflight.json
```

Negative probe read-only được chạy trên riêng candidate `e5-small-384`, ép
`prepare_full_corpus_input()` ném lỗi trước khi gọi `run_preflight()`.

## 4. Kết quả quan sát

- `git diff --check`: PASS.
- Focused four-suite rerun: `80 passed in 175.92s`.
- Independent real read-only preflight: exit `0`, reported `READY`; tokenizer
  phát các warning độ dài đã biết.
- Artifact tracked và reviewer `/tmp` không chứa corpus path map, point rows,
  payload/vector text, query/evidence text, absolute path hoặc secret.
- Static call-path review xác nhận chỉ `run_migration()` gọi create/upsert;
  Reviewer không chạy path này và bốn target vẫn được preflight báo absent.
- Negative probe fail-closed: **FAILED** — preparation lỗi nhưng result vẫn là
  `READY`, `source_points_count=8460`, `errors=[]`.

Do preflight hiện fail-open và migration verification chưa đúng, kết quả
`READY` chỉ chứng minh trạng thái happy path quan sát được; nó chưa đủ làm Gate
2 authorization evidence.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không chạy `migrate`, không tạo/upsert collection, không ghi v2 build
record, không load dense model và không chạy Gate 3/runtime retrieval, đúng hard
boundary. Không có target v2 để chạy post-write `verify`; review phần đó dựa
trên exact code path và focused negative evidence.

## 6. Decision và bước tiếp theo

Decision: `changes_requested` với 5 Major findings. **Không mở Gate 2** và không
chạy bất kỳ lệnh `migrate` nào.

Implementer thực hiện một correction batch theo
`session_prompt/CURRENT_HANDOFF.md`, chạy lại focused tests và fresh read-only
four-pair preflight, cập nhật implementation report/artifact rồi chuyển exact
delta về Reviewer. Evidence về fixed target absence và không có Qdrant write có
thể reuse như baseline; mọi readiness/validation claim bị R1–R5 ảnh hưởng phải
được tạo lại fresh.
