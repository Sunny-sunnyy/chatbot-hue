# Review C96: governance vòng 10 (phiên 30/10)

Người kiểm: C (Claude Opus 5.5, `hue-rag-0e`) · Date: 16:19 30/10/2026 (`date`) · Việc: A giao C96. Người làm: A (`hue-rag-0f`). Chỉ đọc; 0 USD. Skill `risk-gated-agent-review` + W32.
Phạm vi: `git diff HEAD` (`bfb0b41`) của `skills/risk-gated-agent-review/SKILL.md`, `session_prompt/SO_CAI_TIEN_CACH_LAM.md`, `session_prompt/CURRENT_HANDOFF.md`, `session_prompt/sessions/STATUS_A.md`,
`session_prompt/archive/` (mới); `git show 751b352` cho `WORKFLOW.md` §9.6 và `skills/run-experiment/SKILL.md:29`.

## 1. Kết luận

`ready_for_user_confirmation` — 0 blocker / 0 major / 4 minor. Luật mới đúng ý User cho thử và có bằng chứng; hai file archive là bản cũ **nguyên văn**; handoff mới (106 dòng) giữ
đủ quyết định / sha / thứ tự việc / câu hỏi User — chỉ thiếu vài con trỏ (m-1, m-2) và một câu tả nguồn archive chưa đúng (m-3).

## 2. Đã kiểm, đạt

| Mục | Kiểm | Kết quả |
|---|---|---|
| W32 (`risk-gated-agent-review` sau bảng "Kiểm thêm theo tác động") | đọc diff (+3 dòng); đối chiếu sổ vòng 10 dòng W32 (cùng nội dung, nguồn S10 / S21 / S38 / W27 — cả 4 dòng có trong sổ); "User cho thử 30/10" khớp sổ `đang thử` | ✓ |
| `WORKFLOW.md` §9.6 (`751b352`) | +2 dòng: nhánh xong việc ⇒ A **đề xuất** xoá + tag `hoso/<tên>` trước; xoá chỉ khi User duyệt (`!`) — không trao quyền xoá mới. Thực tế: 6 tag `hoso/*` có (`git tag -l`), nhánh tương ứng đã xoá; còn `b92-qwen3-harness` (handoff dòng 19 ghi đúng điều kiện tag trước) | ✓ |
| `run-experiment` `SKILL.md:29` (`751b352`) | dòng code đổi `chat.py:127-135` ⇒ `:182-190`; C đã đọc `backend/api/routes/chat.py:182-190` ở C89: đúng khối `except CitationIntegrityError` ⇒ 500 | ✓ |
| Sổ vòng 10 | W32, I7, W33 `đang thử` (User 30/10); S49–S54 có cột bằng chứng; ý chờ "review bằng họ model khác" **bỏ khỏi danh sách** vì thành W33 (không mất); "Kết vòng 10" tóm đúng | ✓ |
| I7 — archive handoff | ca dò (khác cách A tự kiểm): `diff <(git show HEAD:session_prompt/CURRENT_HANDOFF.md) <(tail -n +5 archive)` ⇒ **0 dòng khác** — giống từng dòng bản đã commit | ✓ (xem m-3 về phạm vi) |
| I7 — archive STATUS_A | thân archive (bỏ 4 dòng đầu) là **một khối nguyên văn** của `git show HEAD:session_prompt/sessions/STATUS_A.md` (kiểm chuỗi con, 375 dòng); phần không dời = khối "phiên 30/10 đang chạy" 11:46, được thay bằng khối kết phiên 16:14 (trạng thái của chính A) | ✓ |
| Handoff mới — nội dung còn hiệu lực | đối chiếu bản cũ (HEAD): hệ thống (kho đợt 2, record `51fb1ec63cbc`, sparse, T1 `4d5bbe9e0edc`), gold v5 `33d16fd6b8f4`, Golden md5 `6331e88fb171`, sàn bộ an toàn, thứ tự việc (PA2), mục tiêu sản phẩm, câu hỏi User (quyền, ChatGPT, lưu câu hỏi, B0, sao lưu), nợ A (W30 m-1 / m-2, log, C65), bảng file private (split, câu kín md5, b0, dot2 4b `c0b5876ea510`, an toàn `9fa81b0fcec4`, yêu cầu streaming `c573949ac59a`), luật chung + cổng ổn định + test cần key | ✓ giữ đủ |
| Quyết định User sau `bfb0b41` | 14:39 (đóng đợt 2) ⇒ handoff dòng 12 + `Project_Status` §5; 14:44 (ngày tương đối ⇒ Phase 9) ⇒ `TONG_HOP.md` §8 dòng 127, `Project_Status` dòng 37, bảng giới hạn dòng 37 | ✓ không mất |
| Rào | `overlap_scan.py` 6 file: 0 trùng; mẫu tên dự án khác (như hook): 0 dòng | ✓ |

**Câu bất biến (W32) C kiểm:** "dời lịch sử không làm mất nội dung còn hiệu lực" ⇒ với mỗi nhóm (quyết định / sha / việc dở / câu hỏi User) của bản cũ, C tìm chỗ nó còn sống
(handoff mới, `Project_Status`, `TONG_HOP` §8, report) — chỉ 4 chỗ dưới không còn con trỏ ở file đang dùng.

## 3. Findings (minor — sửa chữ, không chặn)

- **m-1 — B0 mất con trỏ quy trình + ràng buộc mù.** Bản cũ (mục 6 cũ) ghi: User đọc `data/phase_8_2/b0/doc_cap_mu.md` ⇒ ghi `nhan_xet_user.md` ⇒ A mở `khoa.json` (`5b9240842b7b`), sub-agent
  **mới** tóm nhãn, **B đã thấy khóa — không tóm nhãn**, luật dừng spec 8.2 §11 ⇒ giữ 10 / về 5. Handoff mới chỉ còn "B0 (mốc người)" + "`khoa.json` chỉ A". Ràng buộc vẫn có trong
  `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b0_prep_implementation.md:54`, `_review.md:78, :104`, nhưng phiên sau không có đường tới đó.
  **Đóng khi:** dòng 33 (hoặc bảng file private) thêm 1 dòng trỏ `phase_8_2_b0_prep_implementation.md` + "B đã thấy khóa ⇒ không tóm nhãn; luật dừng spec 8.2 §11".
- **m-2 — lệnh User còn chờ không nằm trong handoff.** `STATUS_A` (16:14) ghi "Lệnh User: xoá `emb/` 8B, tag + xoá nhánh `b92-qwen3-harness`…"; handoff chỉ nhắc nhánh (dòng 19). `data/qwen3_8b_2026-10-28/emb/`
  **vẫn còn** (138 MB lúc C kiểm) trong khi `TONG_HOP.md` §8 dòng 160 viết "bộ đệm `emb/` xoá theo User" như đã xong. **Đóng khi:** handoff "Câu hỏi cho User" / "PHIÊN SAU" thêm "kiểm `emb/`
  đã xoá chưa (User `!`)"; `TONG_HOP` §8 ghi "User duyệt xoá; lệnh `!` chờ chạy" cho tới khi xoá thật.
- **m-3 — câu tả archive handoff chưa đúng phạm vi.** Header archive: "bản đầy đủ trước khi viết lại kết phiên 30/10"; handoff dòng 3: "mục việc B90–B97 / C84–C94". Thực tế archive **= bản
  commit `bfb0b41` (14:45)**: không có C94, C95, B98, kết quả Qwen3-8B, chữ quyết định 14:44 (grep 0) — các mục thêm 14:45–16:13 trong working tree **không** vào archive. Nội dung còn hiệu lực
  của khoảng đó đã có ở `TONG_HOP` §8 / `Project_Status` (bảng §2) nên không mất, nhưng câu tả làm người đọc tưởng archive đủ. **Đóng khi:** sửa header + dòng 3 thành "bản đã commit
  `bfb0b41` (14:45 30/10); mục sau 14:45 (C94–C95, B98, Qwen3-8B, quyết định 14:44): `TONG_HOP.md` §8".
- **m-4 — "Quyền thường trực" đổi chữ khi câu hỏi User còn mở.** Bản cũ: "A commit/push `origin main`"; bản mới: "A stage + đưa lệnh commit / push (auto mode chặn A commit — S50)". Đúng thực tế
  phiên này, nhưng là quyền **thường trực** và User chưa trả lời câu hỏi 3. **Đóng khi:** ghi "(tạm, theo thực tế 30/10 — chờ User câu hỏi 3)".
- Nhỏ hơn nữa (không cần sửa riêng): bản cũ có 2 con trỏ hữu ích đã rơi — file untracked của User ở gốc (`báo cáo nghiên cứu github.txt` — "không đụng"), và `data/streaming_ttft_2026-10-28/`
  (số C73, căn cứ spec streaming; nháp v2 có dẫn lại số nên không mất).

## 4. Không kiểm

- `Project_Status.md`, `PROJECT_HISTORY.md`, `TONG_HOP.md` §8, `bao_cao_he_thong/` (ngoài việc A giao) — chỉ dùng làm nơi tra "nội dung còn sống". Thử mở phiên bằng sub-agent (I7) là việc riêng của A.
