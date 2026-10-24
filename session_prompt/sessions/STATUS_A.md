# STATUS A — cập nhật 17:10 24/10/2026 (kết phiên)

Terminal (24/10): `hue-rag-77` · Agent: Claude Opus 5.5 · Vai: điều phối (User chỉ làm việc với A)

## Đang làm
- Không. Kết phiên theo yêu cầu User. Phiên sau: `CURRENT_HANDOFF.md` mục "PHIÊN SAU — ĐỌC TRƯỚC NHẤT".

## Đang khai báo sửa
- không

## Vừa xong (24/10)
- Phase 7B: brainstorm → spec → điều phối Gate 0–4 → User đóng (bỏ chấm tay). Baseline Claude
  4,43 / 4,28 / 4,45; từ chối nhầm 22/158. Guide + Project_Status cập nhật.
- Đóng các việc B1–B8, C1–C8; review chéo đủ; tiền paid cả phiên ~0,09 USD.
- Tổ chức báo cáo: `bao_cao_he_thong/` (README, luồng hệ thống, 9 báo cáo khâu, nhật ký 24/10),
  `report_agent/<đợt>/`, `gửi chatgpt/<ngày>/`. Cách làm MekongAI áp dụng (`0a709db`).
- Giao B9 (dọn Foods, User duyệt) — chưa xong/chưa review lúc kết phiên.

## Đã học / bẫy gặp
- **Stage từng file đã review**, không `git add <thư mục>`: `8c57701` lỡ đẩy nháp chưa review (gồm
  một số liệu corpus) lên `origin`. Luôn `git diff --cached --stat` trước commit.
- Auto mode có lúc chặn lệnh commit vì "nội dung trước đó trong hội thoại" — không lách; nhờ User
  chuyển permission mode mặc định hoặc chạy bằng `!`.
- User rất nhạy chi phí: ước USD trước mọi lượt paid; ưu tiên đường free (retrieval local, Claude judge).
- Không đưa ngưỡng cố định "chênh ≥ X là thật" — dùng so cặp (paired bootstrap) như nghiên cứu 7B.
- Khi review báo cáo cho User: kiểm cả nguyên nhân được gán (B bắt lỗi A gán sai nguyên nhân chunk vụn).
- Script tạm của A: `/tmp/a_7b/` (chọn tập con, tạo file chấm User) — mất khi khởi động lại; dữ liệu
  thật ở `data/evaluation/phase_7b/`.

## Việc dở / câu hỏi
- Phiên sau: hỏi lại quyền phiên; C review B9 → A commit; brainstorm Phase 8 (câu hỏi đánh số trong
  `CURRENT_HANDOFF.md` "Câu hỏi cho User").
- `báo cáo nghiên cứu github.txt` ở gốc: User bảo giữ nguyên (untracked, không commit).
