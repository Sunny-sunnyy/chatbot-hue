# Codex Review: Full-corpus Metadata v2 Gate 3 / Task 6

Decision: approved — User-confirmed closure 2026-09-30 +07
Reviewer: Codex
Date: 2026-09-30 +07
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_metadata_v2_gate_3_implementation_2026_09_29.md`

## 1. Phạm vi đã review

Reviewer đã đọc toàn bộ Written Spec, Implementation Plan/Review Contract,
implementation report, current handoff và exact diff của:

- `backend/retrieval/full_corpus.py`;
- `backend/tests/test_full_corpus_retrieval.py`;
- `session_prompt/CURRENT_HANDOFF.md`.

Reviewer kiểm riêng runtime payload/readiness/result/trace path, chạy focused
suite, corruption/privacy probes, selected read-only retrieval smoke trên bốn
metadata-v2 targets, MiniLM smoke và đọc collection info của bốn targets.

## 2. Findings

### F1 — Major — Startup chưa validate exact build-record target và lineage

Vị trí: `backend/retrieval/full_corpus.py`,
`validate_full_corpus_build_record()` quanh dòng 363–426.

Requirement: Plan Task 6 Step 3 yêu cầu exact v2 build/payload schema, matching
lineage, existing model/sparse/count invariants và exact metadata-v2 target
trước khi retrieval available. Written Spec mục 6 và 8 yêu cầu collection
record, vector-copy lineage và Qdrant build invariants được kiểm riêng.

Evidence: focused corruption probe trên exact Gate 3 code cho thấy validator
chấp nhận cả ba record malformed sau:

```text
wrong_collection_name ACCEPTED
bad_lineage_sha ACCEPTED
bad_qdrant_record_invariants ACCEPTED
```

Hiện validator không đối chiếu `record.collection_name` với
`candidate.metadata_v2_collection_name`; không đối chiếu
`migration.source_build_record_sha256` với SHA-256 bytes của exact legacy build
record; và không kiểm `qdrant.dense_vector_name`, `sparse_vector_name`,
`distance`, `point_count`. Implementation report lại khẳng định các kiểm tra
lineage SHA, point count và target collection đã tồn tại.

Tác động: runtime có thể trở thành ready với build record bị trỏ sai target,
lineage không còn chứng minh nguồn vector, hoặc record khai báo sai các
invariant đã duyệt. Live collection hiện đúng không đóng được fail-closed
contract cho startup về sau.

Tiêu chí đóng:

- startup đối chiếu exact target collection;
- tính SHA-256 từ exact legacy build-record bytes và đối chiếu exact lineage;
- kiểm đầy đủ Qdrant fields trong build record cùng current count/schema checks;
- regression tests chứng minh từng corruption trên bị reject;
- giữ data flow trực tiếp, không thêm registry/framework/compatibility fallback.

### F2 — Major — Payload validation error làm lộ private source/chunk path

Vị trí: `backend/retrieval/full_corpus.py` dòng 249–272.

Requirement: Plan Task 6 Step 3 yêu cầu validation failure chỉ nêu safe point
ID/reason; handoff yêu cầu public error không lộ path-level discrepancy. Source
path và logical chunk ID là private boundary của workstream.

Evidence: privacy probe với malformed identity quan sát được:

```text
Point <uuid> invalid chunk_id 'foods/other.md#0' for source 'foods/private.md'
```

Các nhánh point-ID mismatch, invalid source và domain mismatch cũng interpolate
`chunk_id`/`source` vào exception.

Tác động: malformed/stale payload có thể đưa canonical source path vào error
detail thay vì chỉ cung cấp safe point ID và reason.

Tiêu chí đóng:

- mọi identity/domain validation error chỉ chứa safe point ID và reason code/
  mô tả tổng quát;
- không chứa source, chunk ID, search/evidence text hoặc absolute path;
- focused tests dùng marker riêng tư và kiểm marker không xuất hiện trong error.

### F3 — Minor — Evidence report/handoff không tự nhất quán

Vị trí:

- implementation report dòng 11, 20–23, 58 và 121–123;
- current handoff dòng 3–11, 20–21 và 35.

Evidence:

- report ghi risk `medium`, trong khi approved Plan/handoff là `high`;
- report/handoff liệt kê sai seven-field payload bằng `chunk_index`/`content`
  thay cho `search_text`/`heading_path`;
- report ghi sai build schema literal và khẳng định lineage SHA/point-count/
  target validation chưa được code thực hiện;
- fresh `git diff --check` thất bại vì trailing whitespace tại handoff dòng
  3–11, trái claim exit code 0;
- `git diff --name-only` của toàn worktree không chỉ có hai file do handoff và
  unrelated pre-existing state; report cần nói rõ cách giới hạn exact Task 6
  diff thay vì khẳng định chung.

Tác động: evidence index không phản ánh chính xác risk, contract và observed
state. Đây không tự làm runtime sai nhưng phải được sửa trong correction đang
có major findings.

Tiêu chí đóng: sửa report/handoff theo exact canonical names và observed
results; `git diff --check` fresh đạt; không viết lại evidence cũ thành fresh.

## 3. Cách Reviewer chạy lại thật

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_full_corpus_qdrant_ingestion.py backend/tests/test_full_corpus_metadata_v2.py -q --tb=short

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 e5-base-768 huydang-dek21-768 qwen3-embedding-0.6b-1024 --treatment dense_bm25_rrf native_hybrid_rrf --reranker none --select P5-Q01 --output data/full_corpus_metadata_v2_reviewer_smoke.json

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache uv run --env-file .env python -m backend.retrieval.full_corpus_smoke run --candidate e5-small-384 --treatment dense_bm25_rrf native_hybrid_rrf --reranker minilm --select P5-Q01 --output data/full_corpus_metadata_v2_reviewer_minilm_smoke.json

git diff --check
```

Reviewer còn chạy deterministic corruption/privacy probes trực tiếp trên
`validate_full_corpus_build_record()` và `validate_point_payload()`, đồng thời
đọc Qdrant collection info bằng read-only REST cho bốn exact targets.

## 4. Kết quả quan sát

- Focused suite: `106 passed in 5.47s`.
- No-rerank live smoke: `8/8 PASS`, determinism `true`, không anomaly.
- MiniLM live smoke: `2/2 PASS`, 21 warm observations/cell, determinism `true`;
  p95 quan sát `1470.8 ms` và `1168.8 ms`.
- Bốn metadata-v2 target đều `green`, mỗi target `8460` points và
  `payload_schema == {}`.
- Lần verify/smoke đầu trong sandbox thất bại với `Operation not permitted`;
  xác định là sandbox chặn Python TCP localhost. Reviewer chạy lại exact smoke
  ngoài sandbox và đạt các kết quả trên. Không dùng lần thất bại đó làm evidence
  về runtime.
- Corruption probe: ba malformed build records nêu ở F1 đều bị code hiện tại
  chấp nhận.
- Privacy probe: error detail chứa private `source` và `chunk_id` như F2.
- `git diff --check`: failed do trailing whitespace trong current handoff.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không chạy full backend suite, đúng boundary Gate 3. Full target vector
equality không rerun thành công trong lượt này; Gate 2 independent verification
đã đóng và Gate 3 không thay collections/vectors. Reviewer chỉ kiểm fresh
collection info và exact retrieval path bị ảnh hưởng.

Reviewer không khẳng định timestamp/content bất biến của toàn bộ build records
từ report; correction F1 phải đọc exact legacy record bytes để validate lineage
ở runtime nhưng không được mutate record nào.

## 6. Initial decision và bước correction

Initial decision: `changes_requested` (đã được Correction 1 mục 7 supersede).

Implementer xử lý một correction delta cho F1–F3 theo
`session_prompt/CURRENT_HANDOFF.md`, chạy lại focused tests, hai selected
read-only smoke và `git diff --check`, rồi trả exact correction diff/report về
Reviewer. Không mở Task 7, Phase 6, full backend suite, Qdrant mutation hoặc Git
write.

## 7. Correction 1 independent review — 2026-09-30 +07

Correction 1 được review trên exact delta F1–F3. Kết quả:

- F1 `major`: **closed**. Startup hiện reject sai target collection, sai hoặc
  malformed legacy lineage SHA và sai Qdrant build-record invariants. Focused
  corruption probe quan sát `REJECTED` cho cả wrong collection, bad lineage và
  bad Qdrant invariants.
- F2 `major`: **closed**. Privacy probe quan sát không có source/chunk/text/path
  marker trong error và exception cause là `None`.
- F3 `minor`: **closed** cho risk/schema/hygiene chính; `git diff --check` đạt.
  Còn một minor evidence-only không chặn: implementation report/handoff nói có
  test riêng cho missing legacy build record nhưng test file không có case đó.
  Runtime branch vẫn fail closed; correction contract không bắt buộc riêng case
  này và Reviewer không mở vòng sửa chỉ để sửa minor.

Fresh Correction 1 evidence:

- focused suite: `116 passed in 5.18s`;
- no-rerank live smoke: `8/8 PASS`, determinism `true`, không anomaly;
- MiniLM live smoke: `2/2 PASS`, determinism `true`, p95 `1386.8 ms` và
  `1554.7 ms`, đều dưới gate `3000 ms`;
- `git diff --check`: exit code `0`;
- không quan sát thay đổi ngoài correction scope trong exact Task 6 paths.

Final technical decision: `ready_for_user_confirmation`. Task 7, Phase 6,
cleanup, Git write và mọi Qdrant mutation vẫn đóng.

## 8. User confirmation

User xác nhận closure Full-corpus Metadata v2 Gate 3 / Task 6 ngày
2026-09-30 +07. Final lifecycle state: `approved` / User-closed. Xác nhận này
không mở Task 7, Phase 6, cleanup, Qdrant mutation hoặc Git commit/push.
