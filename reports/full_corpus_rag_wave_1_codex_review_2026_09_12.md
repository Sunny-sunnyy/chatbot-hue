# Codex Review: Full-corpus RAG Wave 1

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-12
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_rag_wave_1_implementation_report_2026_09_11.md`

## 1. Phạm vi đã review

Reviewer đã kiểm static/read-only:

- base `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`, hiện cũng là `HEAD`;
- toàn bộ `git status --short --untracked-files=all`, task paths và phần thay đổi
  so với base;
- `git diff --check ea87d3ed52851f6b6ab5c47b138540ebc8ff8340 --`;
- full Implementation Report, preview artifact, code/config/test Wave 1 đã đổi;
- approved Written Spec, Implementation Plan, Review Contract và exact Wave 1
  prompt;
- focused source anchors cho sáu mẫu acceptance và ngoại lệ Điện Hòn Chén.

Reviewer không chạy tests, preview CLI, model/API, embedding, Qdrant, frontend,
notebook hoặc benchmark theo authority hiện hành.

## 2. Findings

### W1-R1 — Major — Preview còn blocking error nhưng report đề nghị đóng Wave 1

- Vị trí: `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json:3-9`,
  `reports/full_corpus_rag_wave_1_implementation_report_2026_09_11.md:123-139`,
  `:201-206`, `backend/tests/test_full_corpus_chunker.py:353-364`.
- Requirement: exact Wave 1 prompt §6 yêu cầu preview zero blocking errors, mọi
  representation A vừa cả ba tokenizer limits và không truncate; Review Contract
  §6 yêu cầu zero-error preview. Wave 1 phải closure trước Wave 2.1.
- Evidence: artifact có `status: BLOCKED_OVERSIZED_GROUP`, một blocking error,
  HuyDang `280 > 256`; CLI exit 1. Test hiện khóa chính corpus ở trạng thái lỗi,
  trong khi report đánh criterion này `PASS` và chuyển ngoại lệ sang Wave 2.1.
- Tác động: Wave 1 chưa đạt deliverable/stop condition và Wave 2.1 chưa thể mở.
- Tiêu chí đóng: xử lý ngoại lệ ngay trong correction Wave 1, không sửa corpus,
  không đổi model/limit và không truncate. Theo Option A đã duyệt, dùng ranh giới
  câu nguồn cho exact oversized top-level list item; giữ nguyên thứ tự và mọi câu,
  lặp exact nhãn đậm đầu item dưới dạng source-sliced evidence part cần thiết,
  rồi kiểm full representation của từng phần với cả ba tokenizer. Nếu cách chia
  này không vừa hoặc làm mất nghĩa/evidence, dừng và trả Reviewer thay vì đổi
  contract. Preview thật phải `PASS`, exit 0, errors/oversized đều bằng 0.

### W1-R2 — Major — Các đường splitting/semantic grouping chưa đáp ứng contract

- Vị trí: `backend/ingestion/chunking/markdown_blocks.py:175-216`,
  `backend/ingestion/chunking/full_corpus_chunker.py:271-315`, `:318-389`.
- Requirement: Spec §4 và Wave 1 prompt §3/§5 yêu cầu paragraph split tại sentence
  boundary, nested list giữ/lặp nhãn cha, table giữ header/cell, không trộn sibling
  độc lập chỉ để lấp budget và không bỏ evidence.
- Evidence:
  - table row detection dùng `table_map[0]` (source-line index) làm token-list
    index tại `markdown_blocks.py:193`; row extraction vì thế phụ thuộc quan hệ
    ngẫu nhiên giữa số dòng và token index;
  - nhánh split nested list tại `full_corpus_chunker.py:334-355` chỉ phát sub-item,
    bỏ parent label/body khỏi evidence;
  - không có nhánh split paragraph dài tại sentence boundary;
  - vòng `:361-389` greedily ghép mọi adjacent block cùng `heading_path`, kể cả
    sibling độc lập, chỉ dựa trên chỗ trống tokenizer.
- Tác động: table/list/paragraph behavior và completeness của evidence không đáng
  tin theo contract dù current artifact báo counts.
- Tiêu chí đóng: dùng đúng parser token state để lấy tbody rows; giữ parent label
  bằng exact source slices khi chia nested list; thêm direct sentence-boundary
  split cho paragraph dài và exact exception W1-R1; bỏ blind budget-fill grouping,
  chỉ group khi có quan hệ cấu trúc rõ. Không thêm NLP framework, regex DSL,
  fallback hay special-case text hardcode.

### W1-R3 — Major — Condition validation không bảo đảm exact-one trên toàn corpus

- Vị trí: `backend/ingestion/chunking/full_corpus_chunker.py:74-185`, `:422-456`,
  `backend/ingestion/preview.py:243-258`.
- Requirement: Spec §4, Plan §4 và Review Contract §6 yêu cầu mọi condition và
  target selector match đúng một block; missing source/selector/target phải là
  blocking preview error, không match-first/fallback.
- Evidence: rules chỉ được lọc khi từng discovered document được xử lý. Rule có
  `source` sai/không được discover sẽ không bao giờ được kiểm và tạo zero error.
  `condition_rules_count` trong artifact bị hard-code là `3`, không derive từ
  config/resolution. `chunk_full_corpus(settings=...)` cũng dựng default
  `ConditionManager()` thay vì dùng `conditions_file` của settings được truyền.
- Tác động: preview có thể báo thành công dù một rule hoàn toàn không được resolve;
  count không chứng minh exact-one condition contract.
- Tiêu chí đóng: validate schema nhỏ và toàn bộ rules trên discovered source set;
  mỗi condition/target phải có exact-one match, mọi rule phải được accounted;
  artifact derive actual configured/resolved counts; custom settings phải điều
  khiển đúng condition file. Giữ implementation trực tiếp, không tạo rule engine.

### W1-R4 — Major — Tokenizer default path có silent fail-open và hai nguồn config

- Vị trí: `backend/ingestion/chunking/full_corpus_chunker.py:188-212`,
  `backend/ingestion/preview.py:51-99`, `:138-154`,
  `backend/config/settings.yaml:39-51`.
- Requirement: Spec §4-§5 và Wave 1 prompt §3 yêu cầu preprocessing thật của đủ
  ba candidates, `truncation=False`; thiếu tokenizer là blocker trung thực. Thiết
  kế phải đơn giản và không có silent fallback.
- Evidence: default checker trả `True` khi không load được tokenizer và bỏ qua
  tokenizer bị thiếu. Preview đồng thời hard-code model IDs/limits/prefix cùng
  absolute home-cache snapshot paths, trong khi settings khai báo lại cùng model
  contract nhưng không được dùng làm nguồn chính.
- Tác động: caller của canonical chunker có thể tạo chunk chưa được kiểm đủ ba
  model; config drift và cache layout khác nhau làm behavior khó theo dõi.
- Tiêu chí đóng: một nguồn trực tiếp cho IDs/limits/prefix; local-only resolution
  không phụ thuộc absolute home snapshot path; thiếu bất kỳ tokenizer nào phải
  fail closed ở mọi canonical entry point. Không download, inference, retry hoặc
  fallback.

### W1-R5 — Major — Tests/artifact chưa bao phủ acceptance bắt buộc

- Vị trí: `backend/tests/test_full_corpus_chunker.py:53-393`,
  `backend/ingestion/preview.py:207-258`.
- Requirement: exact Wave 1 prompt §5 và Review Contract §6 yêu cầu CRLF/CR
  locator, repeated text, intro/H1/H2+, nested list/table/blockquote/image/
  separator, condition success/missing/duplicate/mismatch, sáu named samples,
  any-error blocks preview, full repeated chunks/IDs/preview bytes và domain/P7
  breakdown.
- Evidence:
  - test mang tên Ca Huế dùng file tickets tại `:302-305`, không dùng named sample
    `performing_arts/arts/Ca Huế trên sông Hương.md`;
  - Mệ Kéo docstring nói kiểm giá nhưng không assert giá; Đại Nội không assert
    five-entrance relation; lịch trình chỉ tìm ba nhãn ngày; Gia Lạc không kiểm
    rõ historical/current separation;
  - không có focused nested-list, blockquote, repeated-text locator, long-paragraph
    split hoặc target mismatch/duplicate coverage;
  - determinism chỉ chạy `files[:10]` và không so preview artifact bytes;
  - real-corpus oversized test mong exit 1 thay vì tách synthetic failure behavior
    khỏi acceptance preview PASS;
  - artifact chỉ có five-domain breakdown, không có seven-P7 breakdown.
- Tác động: claim “16 tests bao phủ toàn diện” và six-sample PASS chưa được source
  evidence hỗ trợ; deterministic/full-corpus/error semantics còn hở.
- Tiêu chí đóng: bổ sung/siết các test đúng danh sách trên; six samples phải assert
  nội dung, range/evidence slice và quan hệ thật; full-corpus repeated run so
  deep-equal chunks/IDs/UUID5 và byte-identical preview; synthetic oversized/error
  case phải exit 1/no success, còn canonical corpus preview phải PASS. Artifact
  thêm deterministic seven-P7 file/chunk breakdown.

Không ghi minor riêng; correction tập trung toàn bộ vào năm Major trên. Không có
evidence về active Foods/Qdrant mutation trong task diff đã đọc.

## 3. Cách Reviewer chạy lại thật

Reviewer chỉ chạy các lệnh static/read-only sau, đều exit 0:

```bash
git rev-parse HEAD
git cat-file -t ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
git merge-base HEAD ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
git status --short --untracked-files=all
git diff --name-status ea87d3ed52851f6b6ab5c47b138540ebc8ff8340 --
git diff --check ea87d3ed52851f6b6ab5c47b138540ebc8ff8340 --
```

## 4. Kết quả quan sát

- `HEAD` đúng base đã khai báo; target là worktree.
- Mọi task path trong report tồn tại; worktree còn nhiều modified/untracked path
  được report phân loại là pre-existing.
- `git diff --check` sạch.
- Dependency delta trực tiếp chỉ thêm `markdown-it-py>=4.0.0,<5.0.0`; lock ghi
  `markdown-it-py 4.2.0` và hai metadata references tương ứng.
- Preview artifact hiện fail closed đúng ở bước phát hiện lỗi, nhưng chính kết quả
  đó chứng minh Wave 1 chưa đạt zero-error readiness.
- Implementer báo focused run `31 passed`; full backend run được báo exit 1 với
  `127 passed, 79 failed, 21 errors`. Reviewer không coi giải thích tổng quát về
  Qdrant/API keys là proof cho mọi failure vì report không lập exact failure index.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không rerun bất kỳ test/preview/tokenizer nào và không kiểm model cache
  theo authority hiện hành.
- Các claims execution từ Implementer chỉ được đối chiếu với source/report/artifact;
  correction phải cung cấp fresh results cho behavior đã đổi.
- Reviewer không đọc `.env`, logs, Qdrant storage hoặc generated model state.

## 6. Decision và bước tiếp theo

Decision là `changes_requested`. Implementer thực hiện đúng một correction Wave 1
theo `handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_1_PROMPT.md`, regenerate
report/preview và chuyển lại Reviewer/`correction`. Không mở Wave 2.1, không sửa
corpus và không thay requirement/model/token limits.
