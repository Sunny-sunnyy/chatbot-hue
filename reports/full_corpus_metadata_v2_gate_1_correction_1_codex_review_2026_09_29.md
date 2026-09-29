# Codex Review: Full-corpus Metadata v2 Gate 1 Correction 1

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-29 +07
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_metadata_v2_gate_1_implementation_2026_09_29.md`
Prior review: `reports/full_corpus_metadata_v2_gate_1_codex_review_2026_09_29.md`

## 1. Phạm vi đã review

Reviewer đọc đầy đủ Correction 1 handoff/report, source/test delta hiện hành và
fresh preflight artifact; đối chiếu lại R1–R5 với Written Spec, Plan và Review
Contract. Review tập trung fail-closed/sanitization, exact legacy validation,
target paging/equality, final-record gating, v2 lineage verification và test
coverage. Không chạy `migrate` hoặc mutation Qdrant.

Kết quả đóng finding cũ:

- R2 exact legacy record/payload checks: đóng.
- R3 complete target payload/vector verification trước record write: phần này
  đã đóng.
- R4 exact target retrieve theo IDs/multi-page: đóng.
- R1 fail-closed và R5 coverage: còn các delta dưới đây.

## 2. Findings

### C1-R1 — Major: dependency failures chưa thành sanitized `BLOCKED`

- **Vị trí:** `backend/ingestion/full_corpus_metadata_v2.py:250-275`,
  `backend/ingestion/full_corpus_metadata_v2.py:366-369`;
  tests `backend/tests/test_full_corpus_metadata_v2.py:543-595`.
- **Requirement:** Correction 1 yêu cầu mọi corpus preparation hoặc dependency
  inspection failure tạo sanitized `BLOCKED`, non-zero CLI exit, zero mutation
  và không lộ private path/text/secret.
- **Evidence:** preparation error nối nguyên `str(exc)` vào tracked artifact.
  Probe với synthetic exception chứa `/home/private/corpus.md
  FAKE_SECRET_MARKER` ghi nguyên marker vào `errors`. Hai lời gọi
  `client.collection_exists()` nằm ngoài vùng bắt lỗi; probe dependency error
  làm `run_preflight()` ném `RuntimeError` thay vì trả artifact `BLOCKED`.
  Tests hiện còn assert raw exception text phải xuất hiện, nên bảo vệ hành vi
  ngược privacy contract.
- **Tác động:** một lỗi Qdrant có thể không tạo evidence có cấu trúc; lỗi corpus
  có thể ghi absolute/private detail vào tracked artifact.
- **Tiêu chí đóng:** mọi preparation/Qdrant inspection failure được quy về safe
  stage + exception type allowlist, không `str(exc)`; result/artifact `BLOCKED`,
  CLI non-zero, zero mutations. Tests dùng sensitive marker phải assert marker
  và path không xuất hiện; dependency failure không được escape.

### C1-R2 — Major: `run_verify()` chưa xác minh exact v2 record lineage

- **Vị trí:** `backend/ingestion/full_corpus_metadata_v2.py:502-525`,
  `backend/tests/test_full_corpus_metadata_v2.py:879-905`.
- **Requirement:** build record v2 phải được verify đầy đủ, đặc biệt
  `migration.mode`, exact source collection và
  `source_build_record_sha256` của exact current legacy record, cùng corpus,
  dense, sparse và Qdrant identities.
- **Evidence:** verifier chỉ kiểm một phần schema/status/name/payload version,
  source collection, candidate và dimension. Test multi-page tạo target record
  với lineage hash giả `"0" * 64`, không tạo legacy source build record, nhưng
  vẫn yêu cầu và nhận `VERIFIED`.
- **Tác động:** Gate 2 có thể kết luận target verified dù lineage trỏ tới bytes
  legacy không tồn tại/không khớp; post-write proof không bảo vệ contract mà v2
  record được tạo ra để mang.
- **Tiêu chí đóng:** khi `require_build_record=True`, validate exact full v2
  record và hash exact bytes của current legacy source record. Missing/changed
  source record, wrong mode/hash, corpus/dense/sparse/qdrant mismatch phải fail.
  `run_migration()` phải bảo đảm SHA dùng để write vẫn là SHA vừa preflight/
  revalidated, rồi final verification phải kiểm lại lineage đó.

### C1-R3 — Major: duplicate candidate selectors vẫn được chấp nhận

- **Vị trí:** `backend/ingestion/full_corpus_metadata_v2.py:743-747`,
  `backend/ingestion/full_corpus_metadata_v2.py:774-778`,
  `backend/ingestion/full_corpus_metadata_v2.py:785-804`;
  tests `backend/tests/test_full_corpus_metadata_v2.py:531-538`.
- **Requirement:** approved Task 4 và Correction 1 R5 yêu cầu reject unknown và
  duplicate candidate selectors.
- **Evidence:** argparse `nargs="+"` chấp nhận duplicates rồi code map trực tiếp
  từng ID; tests chỉ phủ unknown candidate và missing migrate confirmation.
- **Tác động:** CLI có thể trả success/evidence cho danh sách lặp, làm pair
  counts và selection không còn là tập candidate xác định.
- **Tiêu chí đóng:** reject duplicate selectors trước Qdrant interaction cho cả
  `preflight` và `verify`, giữ deterministic order và thêm exact zero-mutation
  CLI tests.

## 3. Cách Reviewer chạy lại thật

```bash
git diff --check
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_chunker.py backend/tests/test_full_corpus_sparse.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_metadata_v2.py -q --tb=short
UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 preflight --output /tmp/full_corpus_metadata_v2_reviewer_preflight_c1.json
```

Reviewer còn chạy hai pure negative probes: preparation exception chứa fake
private marker và Qdrant client ném exception tại `collection_exists()`.

## 4. Kết quả quan sát

- `git diff --check`: PASS.
- Focused suite: `115 passed in 141.18s`.
- Fresh real read-only preflight: exit `0`, `READY`, 4/4 pairs, zero mutations.
- Reviewer artifact byte-identical với tracked artifact; SHA-256 cùng là
  `e2275e193883a814e26fbe91da39be9edc944f2bbbb2132509d217b044c6659b`.
- Happy path xác nhận 4 targets/build records absent và current legacy state
  phù hợp checks hiện hành.
- Negative sanitization probe: FAILED, raw fake private path/marker xuất hiện.
- Negative dependency probe: FAILED, `RuntimeError` escape khỏi preflight.
- Static/test inspection: v2 record giả lineage vẫn được unit test coi là
  `VERIFIED`; duplicate selection không có guard/test.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không chạy `migrate`, post-write Qdrant verification thật, build-record
v2 write, dense model hoặc Gate 3 paths theo hard boundary. Vì vậy record/write
behavior được review bằng exact code và deterministic tests; đây là lý do các
lineage/negative gates phải đúng trước khi mở Gate 2.

## 6. Decision và bước tiếp theo

Decision: `changes_requested`. Gate 2 vẫn đóng. Correction 2 chỉ xử lý ba delta
C1-R1..R3; không mở lại exact legacy payload validation, target retrieve paging
hoặc vector equality đã đạt. Implementer chạy fresh focused suite và full
four-pair read-only preflight, cập nhật report/artifact/handoff rồi trả Reviewer.
