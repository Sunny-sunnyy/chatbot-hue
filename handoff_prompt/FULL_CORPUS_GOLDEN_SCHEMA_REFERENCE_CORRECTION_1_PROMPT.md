# Implementer — correction lượt 1 khảo sát sâu Golden schema

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Thực hiện correction theo review thật của Reviewer. Báo cáo tự xưng “Reviewer
Codex”, user report và closure do Implementer tạo không có giá trị approval;
Reviewer đã loại bỏ/thay thế các file đó. Không tái tạo chúng.

## 1. Đọc bắt buộc

Đọc đầy đủ theo thứ tự; nếu output bị cắt, đọc tiếp phần thiếu:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. `handoff_prompt/FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_DEEP_DIVE_PROMPT.md`
8. `reports/full_corpus_golden_schema_reference_deep_dive_codex_review_2026_09_10.md`
9. `reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`

Canonical decisions liên quan vẫn là evidence C, một canonical JSONL đích, P7
và giữ nguyên Foods V3 lịch sử. Không hỏi lại hoặc thay đổi chúng.

## 2. Findings phải sửa

Sửa đầy đủ R1–R5 trong Codex review, ưu tiên:

1. **Role và scope:** implementation report chỉ mang attribution Implementer.
   Không viết Codex review, user report, approval, closure hoặc claim Reviewer
   đã chạy lệnh. Không sửa Project Status/context/spec/plan/guides/index.
2. **Full-reading coverage:** đọc nốt toàn bộ nội dung first-party còn thiếu dưới
   `rag_old_0`, đặc biệt đủ 76 Markdown knowledge-base và toàn bộ năm `.txt`,
   bằng lệnh đọc text. Nếu thật sự không thể đọc một file/phần, ghi exact path và
   omission; không claim 100%. Inventory coverage và full-reading coverage phải
   là hai khái niệm riêng.
3. **Evidence-bounded claims:** sửa provenance producer, audit causality,
   category distribution/timing, điều kiện nDCG có thể 1.0, API determinism và
   mô tả Foods V3. Xóa nguyên nhân speculative và các tuyệt đối “triệt để/100%”.
4. **Schema analysis:** tách observed current consumer khỏi proposed
   full-corpus need; xem lại `claim_id`, `domain`, `partition`, `category`,
   `case_type`; không gộp category với case_type; ghi đúng loss của candidate
   không có category; sửa contradiction keywords của Candidate 3; không khóa
   kiểu `heading_path` hoặc enum `case_type` chưa chốt.
5. **Giọng và nội dung:** sửa giải thích JSON/JSONL, bỏ ngôn ngữ quảng bá và bảo
   đảm candidates/field counts/examples nhất quán.

Không cần mở lại hoặc thay đổi các phần kỹ thuật đã đúng ngoài việc đồng bộ câu
chữ liên quan. Không audit fact correctness của toàn bộ 150 test cases.

## 3. Output được phép

Chỉ sửa:

- `reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`
- `session_prompt/CURRENT_HANDOFF.md`

Không tạo report phụ, review, user report, script, JSON audit hoặc notebook.

## 4. Giới hạn

- Không chạy Python hoặc bất kỳ code/script nào.
- Không import/execute notebook, model, tokenizer, API, Qdrant, tests hoặc
  benchmark.
- Không đọc `.env`, không dùng mạng/download/dependency.
- Không sửa runtime/tests/corpus/Golden/index/settings/reference hoặc tài liệu
  canonical ngoài hai file được phép.
- Chỉ dùng lệnh đọc text/JSON/notebook và Git read-only; không Git write.
- Không spawn subagent.

## 5. Self-review và bàn giao

Đối chiếu từng acceptance criterion trong Codex review. Dùng `git diff --check`
cho tracked Markdown và lệnh tìm text read-only để kiểm trailing whitespace;
không dùng Python. Không tự claim finding closed, PASS hoặc approval.

Khi hoàn tất, cập nhật CURRENT_HANDOFF thành:

- `Target role: reviewer`
- `Authored by: implementer`
- `Handoff kind: final_review`
- `State: active`

Bàn giao dẫn implementation report, tóm tắt sửa R1–R5, full-reading coverage
thật, skipped/not verified và nhắc Reviewer phải kiểm độc lập. S1/S2/S3 cùng
các candidates mới vẫn hoãn cho tới khi Reviewer review đạt rồi thảo luận với
User.
