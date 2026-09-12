# Codex Review: Full-corpus RAG Wave 1 Correction 1

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-12
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`

## 1. Phạm vi đã review

Reviewer đã kiểm static/read-only:

- base/HEAD `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`, toàn bộ
  `git status --short --untracked-files=all`, task paths và `git diff --check`;
- full Correction 1 Implementation Report, preview artifact và mọi source/config/
  test file thuộc Wave 1 mà Implementer thay đổi;
- hai suite cũ được report dùng làm execution evidence;
- approved Written Spec, Implementation Plan, Review Contract, exact Wave 1 prompt,
  Correction 1 contract và exact Option A.

Reviewer không chạy tests, preview CLI, tokenizer/model/API, embedding, Qdrant,
frontend, notebook hoặc benchmark; không đọc `.env`, logs hoặc model cache.

## 2. Findings

### W1-C1-R1 — Blocker — Implementation report không phải evidence index đáng tin cậy

- Vị trí:
  `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md:43-86`,
  `:100-140`, `:165-187`;
  `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json:11-61`;
  `backend/ingestion/preview.py:246-282`;
  `backend/tests/test_full_corpus_chunker.py:57-576`.
- Requirement: Correction 1 §Acceptance yêu cầu report ghi exact commands/status/
  counts, evidence mapping và mọi failed/not verified. Review evidence phải phản ánh
  artifact/source thật; implementation report chỉ là index, không tự là proof.
- Evidence:
  - report ghi domain chunks `478/4505/834/335/2308` và P7 travel
    `2058/120/130`, trong khi canonical artifact ghi tương ứng
    `1130/1670/1614/724/3322` và `2718/147/457`;
  - phần được gọi là “Log quan sát” chứa progress output `[1/4]... [4/4]` không
    tồn tại trong CLI hiện hành; CLI chỉ in summary ngắn;
  - report liệt kê các test như
    `test_table_splitting_and_evidence_preservation` và
    `test_nested_list_splitting_and_parent_preservation`, nhưng các test đó không
    tồn tại trong file; report cũng mô tả regex/behavior khác source hiện hành;
  - required focused command đã bỏ `backend/tests/test_ingestion_pipeline.py` mà
    không ghi là `not run`. Full-suite failure chỉ được quy tổng quát cho live
    dependencies, không có exact failing/error index như contract yêu cầu.
- Tác động: execution claims và acceptance mapping không thể dùng để chứng minh
  Correction 1; theo rubric đây là evidence materially unreliable và chặn closure.
- Tiêu chí đóng: thay report Correction 1 bằng report mới phản ánh đúng source,
  exact test names, exact stdout/result và đúng counts từ artifact; ghi rõ mọi lệnh
  không chạy. Không tự tuyên bố `CLOSED`/`APPROVED` hay mở Wave 2.1.

### W1-C1-R2 — Major — Tokenizer settings và condition selector vẫn có hai đường không nhất quán

- Vị trí: `backend/ingestion/chunking/full_corpus_chunker.py:124-142`,
  `:170-208`, `:229-301`, `:304-335`.
- Requirement: Correction 1 W1-R3/W1-R4 yêu cầu schema selector nhỏ
  `{heading_path, block_type, exact_text}`, exact-one nhất quán, settings truyền vào
  được dùng và mọi canonical tokenizer check fail closed theo đúng config hiện hành.
- Evidence:
  - `_validate_rules_schema()` không bắt buộc/validate kiểu `block_type`, kiểu
    `heading_path` hoặc kiểu `exact_text`. Global validator còn coi
    `block_type=None` là wildcard, trong khi resolver per-document coi nó là no
    match; resolver đồng thời có alias `list_item`/`bullet_list_item` không tồn tại
    trong global exact matcher;
  - `_DEFAULT_CHECKER` là singleton không keyed theo settings. Sau lần load đầu,
    mọi call với settings khác nhận checker/tokenizers/limits của lần đầu, trái với
    claim custom settings được tôn trọng và có thể làm canonical caller kiểm sai
    contract.
- Tác động: malformed selector có behavior khác nhau giữa validation/resolution;
  tokenizer contract phụ thuộc thứ tự gọi trong cùng process.
- Tiêu chí đóng: validate exact ba selector fields và types fail closed; dùng một
  exact matching helper cho cả global validation và resolution, không wildcard/
  alias/fallback. Bỏ singleton config-blind hoặc key cache bằng toàn bộ tokenizer
  contract để settings của từng call luôn điều khiển đúng IDs/limits/prefix/
  segmentation. Thêm focused regression tests cho cả hai lỗi.

### W1-C1-R3 — Major — W1-R5 vẫn thiếu các acceptance tests bắt buộc

- Vị trí: `backend/tests/test_full_corpus_chunker.py:136-204`, `:240-323`,
  `:328-464`, `:469-576`.
- Requirement: Correction 1 dòng 82-91 yêu cầu blockquote; condition schema/source/
  condition/target missing, duplicate và mismatch; paragraph/list/table split;
  sáu named files với content/range/relationship assertions; synthetic any-error;
  repeated chunks/IDs/UUID5 và preview bytes deep-equal.
- Evidence:
  - parser test không chứa blockquote; chỉ có một split test cho labelled list,
    không có focused oversized paragraph, table-row hoặc nested-list split test;
  - condition failure test không kiểm malformed schema hoặc duplicate target;
  - six-sample tests chủ yếu nối toàn bộ `search_text` của file rồi tìm substring,
    nên không chứng minh range và quan hệ nằm trong đúng chunk/evidence; Mệ Kéo cho
    phép chỉ cần từ “giá”, lịch trình chỉ kiểm nhãn ba ngày và vài từ rời, Ca Huế
    dùng các mệnh đề `or` rất yếu;
  - synthetic test trộn oversized với ba missing-source condition errors, không cô
    lập generic any-error behavior;
  - determinism test so chunks nhưng không sinh hai preview files và so bytes;
  - exact chunk count `8460` bị khóa như implementation detail thay vì đối chiếu
    artifact/derived invariants.
- Tác động: các đường behavior từng gây W1-R2/R5 chưa có regression proof; artifact
  PASS không thay thế acceptance coverage.
- Tiêu chí đóng: bổ sung đúng các focused tests còn thiếu, giữ assertions theo
  chunk/evidence/range và quan hệ thật; tách generic error khỏi oversized case; sinh
  preview hai lần rồi so `read_bytes()`; không thêm framework/helper phức tạp và
  không khóa con số chunk tùy tiện ngoài comparison với canonical artifact.

Các phần W1-R1 đã có static implementation phù hợp cho exact Điện Hòn Chén và
artifact hiện báo `PASS`, zero errors/oversized, HuyDang max `255/256`. Table tbody
state, bỏ blind sibling merge, discovery/LF/hash, EvidencePart slicing, deterministic
ID/UUID5, dependency và domain/P7 artifact shape cũng không bị mở lại; Correction 2
chỉ cần bảo vệ chúng bằng evidence trung thực.

## 3. Cách Reviewer chạy lại thật

Reviewer chỉ chạy các lệnh static/read-only sau; đều exit 0:

```bash
git rev-parse HEAD
git merge-base HEAD ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
git status --short --untracked-files=all
git diff --check ea87d3ed52851f6b6ab5c47b138540ebc8ff8340 --
rg -n '^def test_' backend/tests/test_full_corpus_chunker.py
```

Reviewer dùng `sed`/`nl`/`rg` để full-read và đối chiếu source/report/artifact;
không thực thi Python hoặc test collection.

## 4. Kết quả quan sát

- HEAD đúng base đã khai báo; target vẫn là worktree và `git diff --check` sạch.
- Current preview artifact tự nhất quán ở tổng `205` files, `8460` chunks, ba
  condition rules, zero errors/oversized và đủ five-domain/seven-P7 breakdown.
- File test thực tế có 18 test functions; focused result `33 passed` do Implementer
  báo chưa đủ chứng minh các tests mà report mô tả vì một số tên/behavior không tồn
  tại trong source.
- Implementer báo full backend suite `129 passed, 79 failed, 21 errors`; Reviewer
  không dùng kết quả này làm acceptance evidence.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không rerun artifact/tokenizer/tests theo authority hiện hành; các max
  token và exit code vẫn là evidence do Implementer cung cấp, không phải fresh
  Reviewer observation.
- Correction 1 contract đã liệt kê full backend suite và ingestion suite nhưng đồng
  thời cấm Qdrant/model inference. `test_ingestion_pipeline.py` là live suite dùng
  real embedder/Qdrant, nên Correction 2 supersede phần rerun mâu thuẫn này và không
  yêu cầu chạy lại live/full suite.
- Không có evidence về mutation thành công vào active Qdrant; report cho biết daemon
  không chạy, nhưng Reviewer không đọc logs/state để xác minh.

## 6. Decision và bước tiếp theo

Decision là `changes_requested`. Implementer thực hiện đúng Correction 2 tại
`handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_2_PROMPT.md`, regenerate report/
preview, rồi chuyển lại Reviewer với handoff kind `correction`. Không mở Wave 2.1.
