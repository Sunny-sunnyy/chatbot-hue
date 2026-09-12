# Codex Review: Full-corpus RAG Wave 1 Correction 2

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-12
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`

## 1. Phạm vi đã review

Reviewer đã kiểm static/read-only:

- base `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`, HEAD tài liệu
  `d631d3cc47a66d7a43c71f36c585d73ae9d21f9e`, toàn bộ
  `git status --short --untracked-files=all`, task paths và `git diff --check`;
- full Correction 2 Implementation Report, canonical preview artifact, Correction
  2 Contract, Review Correction 1 và ba source/test file được handoff đánh dấu
  `full-read`;
- targeted requirements trong approved Written Spec, Implementation Plan, Review
  Contract, Wave 1 prompt và Correction 1 contract;
- exact source text của hai sample liên quan finding còn mở: Mệ Kéo và Gia Lạc.

Reviewer không chạy tests, preview CLI, tokenizer/model/API, embedding, Qdrant,
frontend, notebook hoặc benchmark; không đọc `.env`, logs hoặc model cache; không
thực hiện Git write.

## 2. Kết quả đóng findings cũ

- **W1-C1-R1 — closed:** report hiện khớp artifact ở 205 files, 8460 chunks,
  five-domain/seven-P7 counts; 24 + 15 test names khớp source; stdout và các lệnh
  `NOT RUN` được phân định, không tự tuyên bố approved/closed.
- **W1-C1-R2 — closed:** `_validate_selector_schema()` bắt buộc đúng types/giá trị
  không rỗng; global validation và per-document resolution cùng gọi
  `match_block_selector()` exact; `_CHECKER_CACHE` key gồm ID/limit/prefix/
  word-segmentation và regression test đổi settings trong cùng process đã có.
- **W1-C1-R3 — partially closed:** blockquote, focused split cases, condition
  failures, separated preview error modes, artifact comparison và phần lớn sample
  assertions đã được bổ sung. Phần còn thiếu được nêu dưới đây.

## 3. Finding còn mở

### W1-C2-R1 — Major — Repeated ID/UUID5 và hai sample relationships chưa có direct test evidence

- Vị trí:
  `backend/tests/test_full_corpus_chunker.py:14`, `:24`, `:541-605`,
  `:924-964`.
- Requirement:
  Correction 2 §Required correction delta mục 3 yêu cầu six named samples kiểm
  evidence/range/relationship trong đúng chunk, không ghép nhiều chunk rồi tìm từ
  rời; đồng thời yêu cầu full repeated chunks/IDs/UUID5 và hai preview outputs
  `read_bytes()` bằng nhau. Wave 1 prompt §5-6 và Correction 1 §Acceptance cũng yêu
  cầu repeated chunks/IDs/UUID5 ổn định và six samples kiểm content/range/quan hệ
  thật.
- Evidence:
  - test `test_full_corpus_determinism_and_preview_byte_equality` chỉ gọi
    `chunk_full_corpus()` một lần tại dòng 938. Hai lần lặp tại dòng 953-954 chỉ
    sinh preview artifact; artifact chỉ chứa counts/errors/paths, không chứa
    chunks, chunk IDs hoặc UUID5. `point_id_for_chunk_id` được import nhưng không
    được dùng ở bất kỳ assertion nào;
  - test Mệ Kéo nối mọi `search_text` dưới heading `Món ăn / trải nghiệm` tại dòng
    577 rồi mới tìm hai mệnh đề, nên không chứng minh mỗi quan hệ được bảo toàn
    trong một chunk/evidence cụ thể;
  - test Gia Lạc nối mọi chunk dưới `Không gian tổ chức` và `Thông tin chung` tại
    dòng 594 và 603. Nó không chứng minh cặp địa điểm lịch sử, cặp địa điểm phục
    dựng và quan hệ phi thương mại/cầu may nằm trong các chunk/evidence xác định,
    cũng không bảo vệ sự tách biệt lịch sử–đương đại.
- Tác động: test suite có thể vẫn PASS nếu chunk/point IDs không deterministic giữa
  hai lần build, hoặc nếu các quan hệ sample bị phân tán sai giữa nhiều chunks.
  Đây là thiếu required acceptance evidence nên là Major theo Review Contract.
- Tiêu chí đóng:
  1. chạy `chunk_full_corpus()` hai lần trong cùng test và deep-compare ordered
     chunks, `chunk_id`, `point_id`; assert mỗi point ID bằng
     `point_id_for_chunk_id(chunk_id)`, unique và có UUID5 version đúng;
  2. giữ so sánh hai preview files byte-identical;
  3. thay các phép nối Mệ Kéo/Gia Lạc bằng việc chọn exact chunk(s), assert các cặp
     nội dung/quan hệ trên chính `search_text` hoặc exact `evidence_parts` của chunk
     đó, assert source slices, và với Gia Lạc chứng minh historical/contemporary là
     hai chunks phân biệt;
  4. không sửa production code, corpus, artifact counts hoặc thêm framework.

## 4. Quan sát artifact và static checks

- `git diff --check` exit 0.
- Canonical artifact có `PASS`, 205 unique sorted sources, 8460 chunks, 3 rules,
  zero errors và zero oversized groups.
- Tổng domain và P7 đều tự cộng về 205 files/8460 chunks; max token lần lượt
  `366/512`, `366/512`, `255/256`.
- Artifact không chứa absolute path, timestamp, corpus excerpt, `search_text`,
  `evidence_parts` hoặc chunk dump.
- 24 test functions trong `test_full_corpus_chunker.py` và 15 trong
  `test_markdown_chunker.py` khớp danh sách report.
- Các command/result động và byte equality là Implementer evidence; Reviewer không
  rerun theo authority hiện hành.

## 5. Decision và bước tiếp theo

Decision là `changes_requested` vì còn W1-C2-R1 Major. Implementer thực hiện đúng
Correction 3 hẹp tại
`handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_3_PROMPT.md`, chạy lại offline
checks, cập nhật evidence index và trả Reviewer với handoff kind `correction`.
Không mở Wave 2.1 và không sửa production runtime cho finding chỉ thuộc test.
