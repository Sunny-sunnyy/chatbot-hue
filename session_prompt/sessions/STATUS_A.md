# STATUS A — cập nhật 15:55 25/10/2026 (MỞ PHIÊN tối 25/10)

Terminal: `hue-rag-00` · Agent: Claude Opus 5.5 · Vai: điều phối. B = `hue-rag-de`, C = `hue-rag-d6` (cả ba Claude Code,
liên lạc trực tiếp).

## Phiên tối 25/10
- Mở 15:50; kiểm nhanh khớp (`f26485b`, hook bật, Qdrant 1 collection 8.459).
- Quyền (User 15:5x, hết hạn cuối phiên): tự điều phối B/C rộng; API ≤ 1 USD.
- Brainstorm 8.2 xong (User chọn: PA2 hai bước; mốc người đọc cặp mù; Bước 2 cả ba, luna cuối; A tự đưa vào chatbot, E1 chờ User; trần 0,5 USD).
- Đang làm: nháp spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` bản 1 (sha `2c8d40e3aa4c`); B22 review (giao 16:1x). Đợt `report_agent/2026-10-25_phase_8_2_ap_dung/` mở. Tiền: 0 USD.
- Đang khai báo sửa: spec 8.2, `CURRENT_HANDOFF.md`, `report_agent/README.md`, file này.

---
Phần dưới: trạng thái kết phiên chiều 25/10 (terminal cũ `hue-rag-c6`).

## Commit cuối
- Đầu phiên: `c3528be`. Phiên chiều: `2b0010b` … commit kết phiên (`git log -1`).

## Đang làm
- Không. Phiên sau: brainstorm 8.2 (`CURRENT_HANDOFF.md` "PHIÊN SAU" mục 1–3).

## Đang khai báo sửa
- không

## Vừa xong (phiên chiều 25/10)
- Điều phối 8.1: G4, G2, G3, G4K, G5, G0.6 — mọi gate review chéo; 6 báo cáo `bao_cao_he_thong/`; User đóng 8.1 15:27.
- Vòng cải tiến 2: W11 (WORKFLOW §9.1 "Căn cứ để review"), W12 (Session_Prompt §5 giữ mù câu kín), W13 (skill review),
  I4 (bẫy ra Project_Status §8); sổ `SO_CAI_TIEN_CACH_LAM.md`; thử mở phiên bằng sub-agent mới (xem kết quả trong sổ).
- Handoff rút 343 → ~100 dòng.

## Tiền paid phiên này
- 0,1653 USD (B: luna G4 + G2). A, C: 0 USD (sub-agent dùng quota).

## Quyền phiên này (User 25/10, hết hạn cuối phiên)
- A tự điều phối B/C rộng; API ≤ 1 USD cả phiên (8.1 vẫn trần 0,5 USD); duyệt G4-A + G4-B; GPU mỗi lượt 20–30 câu, kiểm
  GPU thật trước khi chạy.

## Đã học / bẫy gặp
- (giữ) Brief sub-agent: đọc lại trước khi gửi; kết quả sub-agent: tự kiểm 2–3 khẳng định chính.
- (giữ) Sửa tài liệu bằng script: `uv run python`, không `python3` hệ thống.
- (giữ) Luật deny `.env*` chặn cả lệnh shell nhắc tới tên file đó — nhờ User chạy `!`.
- (giữ) `git worktree list` có 4 worktree cũ của AGY dưới `~/.gemini/` — để nguyên.
- (giữ) Repo PUBLIC; người điều phối không đọc câu kín; `CURRENT_HANDOFF.md` đọc lại trước khi sửa.
- Xác nhận User gõ ở terminal B ("việc A giao = làm đi") không thay câu trả lời User cho A.
- 11:33: User trích nguyên văn 2 câu kín cho A (hỏi về câu không dấu) ⇒ A đã thấy 2 câu; không đề xuất biến thể nhắm vào chúng.
  Bài học cho vòng cải tiến: khi User hỏi về câu kín, nhắc User mô tả chung, không dán nguyên câu.
- 12:05: User trích thêm 1 câu kín + đáp án (nhận xét đáp án lặp chủ ngữ) ⇒ A đã thấy 3 câu kín. A chép nhận xét vào
  `sealed_user_feedback_private.md` (C không đọc). Đang chạy: 2 sub-agent chỉ đọc rà `reference_answer` Golden
  (`data/phase_8_1/golden_reference_audit_{1_88,89_176}.md`).
- C24 (11:5x): báo cáo cuối của sub-agent kiểm câu kín liệt kê tên file nguồn đã grep ⇒ C biết chủ đề câu kín (không
  biết câu / đáp án). Vòng cải tiến: brief giữ mù cấm cả tên file nguồn trong báo cáo cuối.
- C26: grep của sub-agent sửa câu kín vô tình in 1 dòng từ `sealed_user_sample*` ⇒ vòng cải tiến: brief grep corpus phải
  loại trừ `evaluation/` (và `meta/`).
- Golden sửa 10 câu: keyword chứa cụm lặp (46, 157) chặn sửa văn phong — keyword và đáp án dính nhau.
- 12:35 bẫy: heredoc `<<EOF` không quote + backtick trong text ⇒ bash chạy backtick như lệnh (chỉ lỗi "not found", không
  hại). Script sửa tài liệu: luôn `<<'EOF'` và truyền giờ qua biến môi trường / argv.
- 13:1x: A tự duyệt plan G3 (không chờ B review) ⇒ B review sau tìm 3 lỗi tiêu chí (ngưỡng keyword sai thang 0–100,
  H3/H2 chưa nói phép so quyết, baseline không chấm lại cùng lượt judge). Bắt được trước khi đo biến thể. Vòng cải tiến:
  plan có tiêu chí ghi trước luôn cần một session khác (không phải người viết, không chỉ A) review trước khi A duyệt.
- Lệch skill `risk-gated-agent-review` (Correction: người kiểm ghi vào mục của người làm) ↔ `WORKFLOW.md` §3.2 (cấm sửa
  mục session khác) — C báo 11:31; đã sửa (W13).

## Việc dở / câu hỏi cho User
- `CURRENT_HANDOFF.md` "Câu hỏi cho User" (quyền phiên, phạm vi 8.2, Hải Vân, tên dự án khác, 3 câu kín A đã thấy).
