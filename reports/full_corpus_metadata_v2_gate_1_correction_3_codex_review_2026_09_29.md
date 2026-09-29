# Codex Review: Full-corpus Metadata v2 Gate 1 Correction 3

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-09-29 +07
Risk: high
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_metadata_v2_gate_1_implementation_2026_09_29.md`
Prior review: `reports/full_corpus_metadata_v2_gate_1_correction_2_codex_review_2026_09_29.md`

## 1. Phạm vi đã review

Reviewer xác nhận handoff `final_review`, kiểm tra worktree/delta hiện hành và
đọc trực tiếp Correction 3 trong migration module, hai regression tests,
implementation report và preflight artifact. Review đối chiếu C2-R1 với exact
acceptance: SHA ghi lineage phải là SHA đã được preflight xác minh, source bytes
phải được revalidate ngay trước final record write, và mismatch/missing phải
fail closed mà không ghi record hoặc cleanup partial target.

Không chạy real `migrate`, không create/upsert/delete Qdrant, không ghi build
record v2 và không mở runtime cutover.

## 2. Findings

Không còn blocker, major hoặc minor finding chặn Gate 1.

C2-R1 đã đóng:

- `run_migration()` lấy exact `source_build_record_sha256` từ successful
  single-pair preflight;
- sau complete target verification và trước final record write, code đọc lại
  legacy source record bytes và bắt buộc SHA hiện tại khớp SHA preflight;
- missing/unreadable/mismatched source dừng trước
  `write_final_full_corpus_build_record()`;
- v2 constructor chỉ nhận SHA preflight đã được so khớp;
- regression tests xác nhận source record bị sửa hoặc xóa đều không tạo final
  record và partial target vẫn tồn tại để chẩn đoán.

## 3. Cách Reviewer chạy lại thật

```bash
git diff --check
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_metadata_v2.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output /tmp/full_corpus_metadata_v2_reviewer_preflight_c3.json
```

Reviewer còn chạy lại pure mocked probe đã phát hiện C2-R1: preflight trả SHA A
trong khi source bytes sau đó có SHA B. Probe kiểm tra migration fail closed và
final record writer không được gọi.

## 4. Kết quả quan sát

- `git diff --check`: PASS.
- Focused suite: `133 passed in 138.94s`.
- C2-R1 negative probe: `fail_closed=True`,
  `final_record_writer_called=False`.
- Fresh real read-only preflight: exit `0`, `READY`, 4/4 pairs, 8.460 source
  points mỗi pair, targets/build records absent và `total_mutations: 0`.
- Reviewer artifact byte-identical với tracked artifact; SHA-256 cùng là
  `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b`.
- Privacy scan trên preflight artifact: không có absolute path, corpus/payload
  text hoặc synthetic secret marker.
- Không có file `data/full_corpus_builds/*_metadata_v2.json`.
- Preflight phát warning tokenizer-length đã quan sát ở các lượt trước nhưng
  hoàn tất thành công; không có dense embedding execution hoặc mutation.

## 5. Giới hạn hoặc phần chưa chạy

Gate 1 không cho phép kiểm chứng real write path. Vì vậy Reviewer chưa chạy
real target creation/upsert, real post-write equality verification hoặc v2
record write; các hành vi này được kiểm tra bằng deterministic recording-client
tests. Runtime retrieval/cutover, evaluation và Gate 3 cũng chưa được chạy.

## 6. Decision và Approval Closure Contract

Decision: `ready_for_user_confirmation`. Gate 1 Tasks 1–4 đạt technical review;
tất cả findings R1–R5, C1-R1..C1-R3 và C2-R1 đã đóng. Gate 2 vẫn đóng cho tới
khi User cấp approval rõ ràng.

User confirmation cần thiết:

```text
Tôi phê duyệt Gate 2 / Task 5 cho phép migrate tuần tự đúng bốn target
metadata-v2 đã khóa trong handoff, với create/upsert và ghi matching final v2
build records; không delete/cleanup legacy hoặc partial targets, không
re-embedding và không runtime cutover.
```

Sau confirmation, Reviewer sẽ chuyển một implementation handoff Gate 2 cho
Implementer. Handoff đó chỉ cho phép:

1. migrate tuần tự đúng bốn source/target pair đã khóa;
2. copy nguyên dense+sparse vectors và tạo exact seven-field payload;
3. verify đầy đủ 8.460 points, schema, payload/vector equality và lineage cho
   từng target trước khi tiếp tục pair kế tiếp;
4. ghi matching final v2 build record chỉ sau verification;
5. dừng ngay ở failure, giữ partial target để chẩn đoán, không delete/repair;
6. dừng sau Gate 2 để Reviewer đánh giá trước mọi Gate 3 cutover.

Git authorization vẫn là `none`. Approval Gate 2 không tự cấp commit/push,
không cấp quyền sửa runtime retrieval, legacy collections/build records,
embedding/model, evaluation hoặc Phase 6.

## 7. User confirmation recorded

User đã cấp đúng explicit Gate 2 approval ngày 2026-09-29 +07:

```text
Tôi phê duyệt Gate 2 / Task 5 cho phép migrate tuần tự đúng bốn target
metadata-v2 đã khóa trong handoff, với create/upsert và ghi matching final v2
build records; không delete/cleanup legacy hoặc partial targets, không
re-embedding và không runtime cutover.
```

Approval này kích hoạt riêng Task 5 theo các ranh giới ở trên. Gate 3, Git
writes, cleanup/repair và mọi target ngoài bốn tên cố định vẫn chưa được cấp
quyền.
