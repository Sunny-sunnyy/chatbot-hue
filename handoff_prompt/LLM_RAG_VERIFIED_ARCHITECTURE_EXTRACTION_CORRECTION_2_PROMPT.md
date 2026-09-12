# Implementer — Correction 2 cho Verified Architecture Extraction từ `llm_rag`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Đây là delta hẹp sau re-review Correction 1. VAE-R1 đã đóng; chỉ sửa phần còn
mở của VAE-R2, VAE-R3 và VAE-R4. Không mở lại quyết định hoặc source checks đã
đạt.

## 1. Bootstrap và mức đọc

Đọc đúng thứ tự; mọi file `full-read` phải đọc tới EOF nếu output bị cắt:

1. `full-read` — `session_prompt/Session_Prompt.md`.
2. `targeted-read` — `session_prompt/Project_Status.md`: current full-corpus
   design, decisions, safety và đoạn `llm_rag`.
3. `full-read` — `session_prompt/IMPLEMENTER_WORKFLOW.md`.
4. `full-read` — `skills/risk-gated-agent-review/SKILL.md`.
5. `full-read` — `session_prompt/CURRENT_HANDOFF.md`.
6. `full-read` —
   `handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md`.
7. `full-read` —
   `handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_1_PROMPT.md`.
8. `full-read` —
   `reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md`.
9. `full-read` —
   `reports/llm_rag_verified_architecture_extraction_2026_09_11.md`.
10. `full-read` —
    `reports/llm_rag_verified_architecture_extraction_correction_1_implementation_report_2026_09_11.md`.
11. `full-read` — correction prompt này.

Survey 885 dòng, survey corrections cũ và hai tài liệu lịch sử trong `tai_lieu`
là `reference-only`; không mở. Không cần mở rộng source ngoài exact anchors ở
§2. Không dùng `practical-project-coding`, network hay subagent.

## 2. Exact correction

1. **Đóng VAE-R2:** thay tám bullets §4 bằng một mapping tối thiểu không nhắc
   lại technical details ở §§2–3. Section chỉ cần nói:
   - observations ở §§2–3 là evidence/contrast, không tự là Hue requirement;
   - canonical Hue decisions chỉ nằm ở §5.1;
   - adaptation chưa chốt chỉ nằm ở Decision Queue §5.2.
   Không lặp UUID, E5, sparse, fusion, reranker, separator, streaming/session,
   one-shot hoặc source anchors tại §4. Kiểm semantic claim uniqueness bằng đọc
   nội dung; không dùng riêng duplicate URL target làm proxy.
2. **Đóng test boundary của VAE-R3:** dòng test chỉ được kết luận trong đúng ba
   file đã đọc: chúng gồm pure deterministic tests và fake/monkeypatch cho
   API/provider, nên không cung cấp live Qdrant/model integration evidence.
   Không nói toàn repository không có integration test. Xóa câu §6 “Toàn bộ dữ
   liệu kiểm thử của `llm_rag` là mock”; gap tải/độ trễ chỉ cần nói chưa được đo
   vì task không chạy runtime.
3. **Đóng anchor 30 candidates của VAE-R3:** claim phải dẫn đồng thời source cho
   `top_k: 10`/`TOP_K` và `limit=TOP_K * 3`, ví dụ
   `settings.yaml:48-52` cùng `hybrid_retriever.py:38-44`. Nếu không, diễn đạt
   là `TOP_K * 3` thay vì hard-code 30. Mỗi link label phải khớp URL fragment và
   range không vượt EOF.
4. **Đóng VAE-R4:** không sửa report Correction 1. Tạo report Correction 2 mới,
   ngắn, chỉ gồm acceptance→evidence, observed commands/results, exact task paths
   và skipped/not-verified. Không chép scripts, toàn findings, source inventory
   hoặc artifact prose; không tự tuyên bố Reviewer đã đóng finding.

Không thay nội dung đã đóng của VAE-R1 hoặc các anchors đã đạt trong VAE-R3.
Giữ đúng sáu H2 và giới hạn 320 dòng/55.000 bytes của extraction.

## 3. File được phép thay đổi

Chỉ sửa/tạo:

```text
reports/llm_rag_verified_architecture_extraction_2026_09_11.md
reports/llm_rag_verified_architecture_extraction_correction_2_implementation_report_2026_09_11.md
session_prompt/CURRENT_HANDOFF.md
```

Không sửa correction reports cũ, Codex review, contracts, guide/decision notes,
runtime/tests/corpus/Golden/index/dependencies hoặc reference repository.

## 4. Verification và evidence reuse

- Full-read extraction sau sửa; kiểm sáu H2, kích thước, labels và forbidden
  content.
- Đọc semantic §§2–6 để chứng minh không còn claim lặp; URL uniqueness không đủ.
- Kiểm mọi local path/range bằng existence và `awk 'END { print NR }'`; kiểm
  label khớp fragment.
- Focused-check ba test files và source của `TOP_K * 3`.
- Chạy `git diff --check` và `git status --short --untracked-files=all`; phân
  biệt task paths với pre-existing worktree.

Có thể reuse VAE-R1 và source checks không đổi từ cùng correction series; không
gọi evidence reuse là fresh run. Không chạy/import project code, tests, model,
API, Qdrant, frontend, notebook hoặc benchmark; không đọc `.env`/logs/data.

## 5. Review Contract và bàn giao

Risk giữ `medium`. Reviewer sẽ chạy lại minimum diff gate, full-read extraction
và Correction 2 report, semantic duplicate/test boundary, anchor 30 candidates,
toàn link/range validator, structure/size/labels. Không chạy runtime.

Khi hoàn tất, trả `CURRENT_HANDOFF.md` về:

```text
Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none
```

Next action duy nhất: Reviewer re-review Correction 2. Không claim
approved/completed và không resume Decision Queue/Written Spec/Plan.
