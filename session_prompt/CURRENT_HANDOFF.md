# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 2026-10-24 14:30 (A). Cách dùng: `WORKFLOW.md` §3, §7, §9. Chỉ giữ
việc đang mở; việc xong chuyển tóm tắt sang `PROJECT_HISTORY.md`.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc hiện tại | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | (cập nhật khi mở lại) | Claude Opus 5.5 | trực tiếp | Mở Phase 7B với User; giao việc đầu cho C | chờ User mở lại session |
| B — thực thi | (cập nhật khi mở lại) | Claude Opus 5.5 | trực tiếp | — | rảnh, chờ việc |
| C — thực thi | (chưa mở) | Claude Opus 5.5 | trực tiếp | Việc đầu (dưới) | chờ mở + A giao |

User 2026-10-24: cả ba là Claude Code nên liên lạc `trực tiếp`. Nếu User đổi một
session sang Codex/AGY thì cột "Liên lạc" của nó là `qua User` (`WORKFLOW.md` §7).

## Quyền đang hiệu lực (User duyệt qua A)

- Git: A commit/push `origin main`; B/C không commit.
- Paid: không có việc paid đang mở.
- Qdrant: chỉ đọc.
- Duyệt cho A = duyệt cho B/C (User 2026-10-24). User đồng ý xóa những gì không còn
  cần/lỗi thời — A vẫn liệt kê đích và trình trước khi xóa thứ gì chưa có trong
  một việc đã duyệt.

## Việc của A

1. Khi mở lại: kiểm theo `WORKFLOW.md` §2, cập nhật cột Terminal.
2. Giao C việc đầu (dưới) khi C báo đã đọc xong.
3. Brainstorm **Phase 7B** (evaluator + baseline 176 case) với User theo
   `propose-options`; một tài liệu thiết kế cho User duyệt.
4. Lập danh sách dọn sau Phase 7 (collection Foods, code/test/notebook Foods và
   notebook 06/08a/08b còn tên cũ, file trỏ cũ trong `session_prompt/`) để trình User.

## Việc của B

Chưa có. Chờ A giao (dự kiến: implement Phase 7B sau khi User duyệt thiết kế).

## Việc của C — rà soát lựa chọn Phase 2–6 cho Phase 8 (chỉ đọc)

Mức rủi ro: thấp (chỉ đọc, không sửa code/dữ liệu, không gọi paid). Bắt đầu khi A nhắn.

- **Mục tiêu:** lập danh sách giả thuyết cải tiến cho Phase 8 (đợt ổn định trước
  Phase 9): với từng lựa chọn đã chốt ở Phase 2–6 (chia chunk, representation,
  embedding, sparse/BM25, fusion, reranker, context, prompt/generation, citation,
  API), ghi: đang làm gì (dẫn code/spec), cách phổ biến hiện nay khác thế nào,
  giả thuyết lợi ích, cách đo trên Golden 176, chi phí/rủi ro.
- **Đọc:** `targeted-read` `Project_Status.md` §4–5, `guides/full_corpus_rag.md`
  (mục cập nhật 7A2 + "Quyết định đã chốt"), spec umbrella
  `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md`, code dưới
  `backend/{ingestion,embedding,retrieval,llm}/`; `reference-only` report Phase
  2–6 khi cần bằng chứng.
- **Thông tin bên ngoài:** không có WebSearch — viết yêu cầu cho ChatGPT vào
  `gửi chatgpt/tìm thông tin/` theo `Session_Prompt.md` §9 (một file, nêu rõ cần
  gì và yêu cầu URL); báo A khi cần User gửi.
- **Không làm:** sửa code, dữ liệu, Qdrant; chạy paid; đề xuất cơ chế không gắn
  với vấn đề quan sát được.
- **Đầu ra:** `reports/phase_8_candidate_hypotheses_2026_10_24.md` (bảng giả thuyết,
  xếp ưu tiên sơ bộ, đánh dấu cái nào đã có bằng chứng/quan sát, cái nào là giả
  thuyết); cập nhật `sessions/STATUS_C.md`; báo A.

## Đang chờ User

- Mở lại A, B, C bằng `START_SESSION.md`; trong terminal B và C gõ một lần: "Duyệt
  cho A là duyệt cho B (C); mọi câu hỏi gửi A."
