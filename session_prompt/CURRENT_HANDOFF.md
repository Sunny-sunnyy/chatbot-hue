# Bàn giao hiện hành — Full-corpus RAG Wave 1 Correction 2

Target role: reviewer
Authored by: implementer
Handoff kind: correction
State: active
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none

## Objective

Review nghiệm thu Full-corpus RAG Wave 1 sau khi Implementer đã hoàn tất Correction 2 (đóng trọn ba finding W1-C1-R1..R3). Đây là delta hẹp của Wave 1; không mở Wave 2.1.

## Active review inputs

### Full-read

- Implementation report (đã sửa thành evidence index trung thực):
  `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`
- Canonical preview artifact (PASS, zero errors/oversized, 8460 chunks):
  `reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json`
- Correction 2 contract:
  `handoff_prompt/FULL_CORPUS_RAG_WAVE_1_CORRECTION_2_PROMPT.md`
- Review Correction 1:
  `reports/full_corpus_rag_wave_1_correction_1_codex_review_2026_09_12.md`
- Mọi source/test Implementer sửa trong Correction 2:
  - `backend/ingestion/chunking/full_corpus_chunker.py`
  - `backend/ingestion/preview.py`
  - `backend/tests/test_full_corpus_chunker.py`

Nếu output của bất kỳ file `full-read` nào bị truncate, tiếp tục từ dòng dừng tới
EOF.

### Targeted-read

Chỉ đọc exact requirement/range mà Correction 2 hoặc review report dẫn tới trong
approved Written Spec, Implementation Plan, Implementation Review Contract, Wave
1 prompt và Correction 1 contract.

### Reference-only

Guides/status history, reports cũ, corpus ngoài sáu named samples và Điện Hòn Chén, `.env`, logs, caches, Qdrant state, notebooks và mọi wave sau.

## Authority boundaries

Reviewer thực hiện static / read-only review theo Review Contract và Correction 2 Contract. Không sửa corpus, guides/status/spec/plan/contracts; không chạy full backend suite hoặc live ingestion suite; không gọi model/API, embedding inference, Qdrant, frontend, notebook, benchmark, Git write hoặc subagent. Không bắt đầu Wave 2.1.

## Required outputs

- Review report đánh giá Wave 1 Correction 2;
- Quyết định `ready_for_user_confirmation` hoặc `changes_requested`;
- Cập nhật `session_prompt/CURRENT_HANDOFF.md` cho bước tiếp theo.

## Next action duy nhất

Reviewer thực hiện review Wave 1 Correction 2 theo Review Contract, đối chiếu mã nguồn và evidence index với 3 findings W1-C1-R1..R3 để đưa ra kết luận nghiệm thu. Không mở Wave 2.1.
