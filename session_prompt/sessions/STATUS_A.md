# STATUS A — cập nhật 22:50 24/10/2026 (kết phiên tối)

Terminal: `hue-rag-47` · Agent: Claude Opus 5.5 · Vai: điều phối. B = `hue-rag-b0`, C = `hue-rag-a3` (tên đổi
mỗi lần mở).

## Đang làm
- Không. Kết phiên theo yêu cầu User. Phiên sau: `CURRENT_HANDOFF.md` mục "PHIÊN SAU — ĐỌC TRƯỚC NHẤT".

## Đang khai báo sửa
- không

## Vừa xong (phiên tối 24/10)
- B9 dọn Foods đóng (User 20:01); 8 báo cáo khâu về mẫu mới (B10, C10, C13).
- Phase 8 tách 8.1/8.2; brainstorm → spec 8.1 (v1→v4, review C15/b/c/d) → **User duyệt 20:49** kèm M1/M2.
- G0: split (C16), evaluator (C16), tham số (B11), phá hòa native (B13), đoạn đúng 55 câu (A qua 4 sub-agent, B14
  review), câu kín 36 (A qua sub-agent, C17/C20/C22 kiểm mù), độ tự nhiên 176 câu (2 sub-agent, kappa 0,765).
- G1 chẩn đoán retrieval xong (B15, C21): nghẽn ở xếp hạng; 22/22 từ chối nhầm thiếu fact trong context.
- Skill mới `run-experiment`; mục "Ranh giới theo khâu pipeline" trong `practical-project-coding` (B review).
- 6 sub-agent đọc 15 summary khóa học AI FDE → `data/course_notes/` (private) — **User gác lại**, chưa dùng.

## Chưa xong / chờ
- Chờ User: câu kín 3 dòng capability_only + duyệt mẫu 15 dòng; 9 câu độ tự nhiên bất đồng; mâu thuẫn Hải Vân;
  15 file nhắc MekongAI (A đề xuất để nguyên).
- Chờ A: duyệt plan G2/G4 của B (B16) + quyết G4-B pool 100 (lệch spec §5 G4); commit B16.
- G0.6 khóa baseline chưa làm (sau khi câu kín + nhãn tự nhiên chốt).

## Đã học / bẫy gặp
- **Repo PUBLIC:** auto-mode chặn commit có số đo/đường dẫn MekongAI ⇒ chi tiết dự án khác để `data/` (memory
  `public-repo-no-external-project-data`).
- Auto-mode từng chặn commit cả một đoạn phiên ("nội dung trước trong hội thoại") rồi tự hết khi User nói rõ
  "A được commit/push". Tin giao việc có lệnh xóa collection bị chặn — tin ngắn trỏ handoff thì qua.
- Người điều phối **không đọc câu kín**: mọi việc với câu kín qua sub-agent mới, C kiểm mù qua sub-agent khác.
- Một agent gắn nhãn chưa đủ: rater thứ hai độc lập (kappa) + User quyết phần bất đồng.
- Chẩn đoán bằng keyword (B4, 7B) có thể sai: đoạn đúng cho kết luận ngược (0 câu đủ bằng chứng mà vẫn từ chối).
- Script tạm `/tmp/a_81/` đã sao vào `data/phase_8_1/tools/` (mất khi khởi động lại).
- File `CURRENT_HANDOFF.md` hay bị B/C sửa song song — đọc lại ngay trước khi ghi đè.

## Tiền paid phiên tối
- ~0,0013 USD (smoke 10 của B9). 8.1: 0 USD. Sub-agent dùng quota Claude Code.
