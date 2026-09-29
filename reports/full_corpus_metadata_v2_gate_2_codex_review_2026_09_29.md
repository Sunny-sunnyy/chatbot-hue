# Codex Review: Full-corpus Metadata v2 Gate 2 / Task 5

Decision: approved — User-confirmed Gate 2 closure; Gate 3 / Task 6 authorized
Reviewer: Codex
Date: 2026-09-29 +07
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_metadata_v2_gate_2_implementation_2026_09_29.md`

## 1. Phạm vi đã review

- Full-read implementation report, current handoff và sanitized execution
  evidence của Gate 2.
- Targeted-read Task 5, Gate 2/Gate 3 boundary và Review Contract trong approved
  Metadata v2 Implementation Plan.
- Kiểm exact SHA/nội dung cấu trúc của bốn final v2 build records và SHA của bốn
  legacy v1 build records.
- Chạy độc lập combined `verify` trên bốn source/target pair thật; không chạy lại
  `migrate`.
- Đọc trực tiếp Qdrant collection info của bốn legacy và bốn metadata-v2 target.
- Kiểm tracked preflight/report/handoff về scope, privacy và `git diff --check`.

Gate 1 code/tests không có delta trong Task 5; kết quả correction 3 đã được
independent review trước khi User mở Gate 2 nên được reuse cho phần code không
đổi. Review này tập trung live write state, target equivalence, build-record
lineage và legacy immutability theo Review Contract.

## 2. Findings

Không có `blocker`, `major` hoặc `minor` trong phạm vi Gate 2 / Task 5.

Task 5 chỉ tạo đúng bốn target đã được User cho phép, bốn matching final v2
records và evidence/handoff. Không quan sát runtime cutover, cleanup/delete,
re-embedding, model/API execution hoặc thay đổi ngoài authority Gate 2.

## 3. Cách Reviewer chạy lại thật

```bash
git rev-parse HEAD
git status --short
git diff --check
sha256sum reports/artifacts/full_corpus_metadata_v2_preflight_2026_09_29.json
sha256sum data/full_corpus_builds/hue_full_corpus_a_e5_small_384_metadata_v2.json \
  data/full_corpus_builds/hue_full_corpus_a_e5_base_768_metadata_v2.json \
  data/full_corpus_builds/hue_full_corpus_a_huydang_dek21_768_metadata_v2.json \
  data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024_metadata_v2.json
sha256sum data/full_corpus_builds/hue_full_corpus_a_e5_small_384.json \
  data/full_corpus_builds/hue_full_corpus_a_e5_base_768.json \
  data/full_corpus_builds/hue_full_corpus_a_huydang_dek21_768.json \
  data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024.json
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env \
  python -m backend.ingestion.full_corpus_metadata_v2 verify
```

Reviewer cũng đọc read-only endpoint collection info tại Qdrant localhost cho
cả tám collection để đối chiếu trạng thái, point count, dense dimension, sparse
vector name và payload-index schema.

## 4. Kết quả quan sát

- HEAD là `9242178bfe381011dd0d74875181a6a624410de3`; base/head khớp handoff.
- `git diff --check`: exit `0`.
- Fresh independent combined verify ngoài sandbox: exit `0`,
  `Verification status: VERIFIED`.
- Hai lần chạy trong sandbox trước đó trả exit `1` với
  `ResponseHandlingException`; traceback focused probe xác nhận nguyên nhân là
  sandbox chặn TCP với `[Errno 1] Operation not permitted`. Đây không phải data
  mismatch. Cùng exact command sau khi được cấp network access localhost đã PASS.
- Cả bốn metadata-v2 targets đều `green`, đúng 8.460 points, dense dimensions
  lần lượt `384/768/768/1024`, có sparse vector `sparse`, và
  `payload_schema == {}`.
- Combined verify đã kiểm đầy đủ 33.840 target points: exact ID set, exact
  seven-field payload, source-equal dense+sparse vectors và v2 lineage.
- Bốn v2 build-record SHA-256 khớp implementation report:
  `41d41bd5...196`, `922c5aae...d5f`, `287307ec...60c`,
  `40ebf9a9...14a`.
- Bốn v1 record SHA-256 fresh-check khớp Gate 1 và lineage tương ứng:
  `ea19021a...c76`, `0cd69406...d7b`, `10b3f847...c4a`,
  `2faa9d4f...dd5`.
- Bốn legacy collections đều vẫn `green`, đúng 8.460 points, đúng dense
  dimension/sparse name và empty payload-index schema.
- Fresh pre-write artifact có SHA
  `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b`,
  status `READY`, 4/4 pairs và `total_mutations: 0`.
- Tracked Gate 2 artifacts không chứa absolute path, serialized payload/evidence
  text, vector values, point-ID dump hoặc secret.

Evidence reused: Gate 1 correction 3 review cho code/tests và migration guards,
vì Task 5 không sửa các paths đó. Không gọi evidence reused này là fresh run.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không rerun `migrate`, đúng Review Contract và để tránh write lặp vào
  target đã tồn tại.
- Không chạy full backend suite; Task 7 chưa active.
- Không chạy runtime retrieval smoke hoặc sửa retrieval mapping; đây là Gate 3
  và vẫn chưa được User cấp authority.
- Các warning tokenizer-length xuất hiện khi chuẩn bị corpus nhưng verify hoàn
  tất thành công; không có embedding/model execution.

Các giới hạn trên không chặn kết luận Gate 2 vì complete target verification,
lineage và legacy immutability đều đã được kiểm độc lập bằng real Qdrant state.

## 6. Decision và Approval Closure Contract

Technical decision: `ready_for_user_confirmation`. Gate 2 / Task 5 đạt toàn bộ
acceptance trong approved scope. Gate 3 vẫn đóng cho tới khi User xác nhận rõ.

User confirmation được đề nghị:

```text
Tôi xác nhận closure Full-corpus Metadata v2 Gate 2 / Task 5 và phê duyệt
Gate 3 / Task 6 cho phép cutover canonical full-corpus retrieval sang đúng bốn
metadata-v2 targets đã được Reviewer xác minh, thực hiện strict v2 readiness,
focused tests và selected read-only retrieval smoke theo approved Plan; không
cleanup/delete legacy hoặc target, không re-embedding, không evaluation/Phase 6
và không Git commit/push.
```

Sau exact confirmation, Reviewer được phép:

1. ghi User-confirmed closure của Gate 2 trong review/status/guide liên quan;
2. thay `CURRENT_HANDOFF.md` bằng exact Implementer handoff cho riêng Gate 3 /
   Task 6;
3. cho phép sửa `backend/retrieval/full_corpus.py`,
   `backend/tests/test_full_corpus_retrieval.py`, và chỉ sửa
   `backend/retrieval/full_corpus_smoke.py` nếu contract thực sự yêu cầu;
4. cho phép focused tests và selected real read-only retrieval smoke đã khóa
   trong Task 6;
5. giữ `git_authorization: none` và dừng trước Task 7, Phase 6, cleanup/delete,
   re-embedding, evaluation hoặc mọi scope khác.

User có thể xác nhận riêng closure Gate 2 mà chưa mở Gate 3; trong trường hợp đó
Reviewer chỉ cập nhật closure và giữ Gate 3 đóng.

## 7. User confirmation recorded

Ngày 2026-09-29 +07, User đã xác nhận:

```text
Tôi xác nhận closure Full-corpus Metadata v2 Gate 2 / Task 5 và phê duyệt
Gate 3 / Task 6 theo Approval Closure Contract.
```

Gate 2 / Task 5 chuyển thành User-confirmed closure. Gate 3 chỉ mở đúng Task 6,
paths, focused tests và selected read-only retrieval smoke đã nêu trong
Approval Closure Contract. Task 7, Phase 6, cleanup/delete, re-embedding,
evaluation và Git vẫn chưa được cấp quyền.
