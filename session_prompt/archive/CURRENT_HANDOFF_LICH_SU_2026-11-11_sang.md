# Lưu trữ — khối "PHIÊN SAU ĐỌC TRƯỚC" kết phiên sáng 11/11/2026 (dời 16:24 11/11/2026)

## PHIÊN SAU ĐỌC TRƯỚC (viết lại 10:43 11/11/2026, kết phiên 11/11)

**Phiên 11/11 đã kết** (mở 08:18, chỉ A mở; User: "đọc sau"). Quyền phiên 11/11 **hết hạn** ⇒ A mới hỏi lại User một câu. **Dự án chưa xong** — Phase 9 tiếp tục.
Khối kết phiên 10/11 nguyên văn: `archive/CURRENT_HANDOFF_LICH_SU_2026-11-11.md`.

**Hệ thống:** không đổi so với 10/11 (`main` chỉ thêm tài liệu). **Qdrant tắt lúc mở phiên 11/11** (không container; dữ liệu `qdrant_storage/` còn đủ) ⇒ việc cần chatbot: `docker compose up -d qdrant` trước.
**Tiền 11/11:** 0 USD API (5 agent con chỉ đọc = quota Claude). Phase 9 ≈ 3,88 / 4,2.

### Xong 11/11 — bài học cho User (VIỆC SỐ 1 của 10/11)
- **`bai_hoc/` ở gốc repo, 17 bài (0–16)** + `README.md` (dàn bài + trạng thái). User **chỉ đọc folder này**; `bao_cao_he_thong/` = sổ ghi việc (quá khứ) của agent, vẫn cập nhật theo luật. Khuôn + luật: `WORKFLOW.md` §6 "Bài học cho User" (User chốt từng câu 11/11: bảo vệ đồ án, không phần dự án công ty; bám RAG 2 giai đoạn User đã biết; **kể thẳng, không so "bản cơ bản ↔ hue_rag"**; đủ chi tiết kỹ thuật; hình ảnh nền hướng dẫn viên + sổ tay; bảng từ đầu bài; mình / anh; "chuyện thật"; mỗi số kèm mốc + tốt tới đâu; mermaid khi cần).
- Ghi chú private cách đọc của User (gồm 2 tin của A dự án khác): `data/hoc_cung_user_2026-11-10/ghi_chu_cach_doc_cua_user.md`.

### Làm tiếp (theo thứ tự)
1. **Hỏi User quyền phiên** (một câu).
2. **Góp ý bài học:** User đọc dần ⇒ sửa ngay theo góp ý; câu sai ⇒ sửa + ghi ở mục Nguồn của bài + báo User. Không viết thêm bài khi User chưa yêu cầu. **Hệ thống đổi ⇒ sửa bài bị chạm trong `bai_hoc/` cùng đợt** với sổ ghi việc.
3. **Phase 9 tiếp (như 10/11):** **B7** lượt đo cuối (nháp plan `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md` + A chốt Q1–Q4; quỹ B7 thiếu ≈ 0,03 — hỏi User lúc chạy) · bản đồ (chờ phiếu toạ độ) · giọng nói (chờ 40 câu, nhánh `p10-giong-noi`) · deploy AWS (câu Q-DP dưới). Đợt 2 cổng (lưu trú, ăn gần, sự kiện): trước khi xây ⇒ lượt đếm rẻ (W61).
4. **Ứng viên từ bài 16 "chỗ còn yếu"** (đề xuất, chưa duyệt — trình User khi bàn việc mới; mỗi cái cần lượt đếm rẻ trước): thử lại model xếp lại ở cấu hình 10 đoạn; kiểm số tiền / giờ trong câu trả lời kho phải có trong đoạn được trích; thu câu người dùng thật khi deploy.
5. **User khi rảnh (không chặn):** đọc `bai_hoc/` · bảng điểm v7 `data/phase_9/lich_trinh/diem_cho_user_v7.md` · phiếu toạ độ `data/phase_11/ban_do/phieu_toa_do_11_diem.md` · thu 40 câu giọng nói `data/phase_10/giong_noi/bo_40_cau/huong_dan_thu_cho_user.md`.
6. Giới hạn biết (như 10/11): biểu mẫu "dày lịch" gần như không tác dụng; người lớn tuổi / trẻ em không có buổi tối; câu lịch bị rút khi thiếu `[n]` (1 / 9); log truy cập uvicorn ghi IP. Lệch nhỏ fact sheet thấy 11/11 (sửa khi chạm): chú thích `settings.yaml` cạnh `ngay_lich: true` và `anh.bat: true` còn ghi "TẮT tới khi đạt"; `07_BAO_CAO…` checklist còn dòng "câu lịch thuần ⇒ ngoài phạm vi" (sai từ 10/11); vài số dòng `file:dòng` cũ trong 05 / 06 / 07 / 10.

**Vòng tự soi 11/11:** chỉ A ⇒ tự soi một mình (STATUS_A): không test / đo nào chạy; agent con lập fact sheet đáng (bắt 3 câu sai). Sổ vòng 25 (S118–S120), không luật mới.

### Nhánh
`main`; 4 nhánh 10/11 User xoá 08:35 11/11/2026. Đang mở cũ: `p9-sua-lich` (hoãn), `p10-giong-noi` (E), `p9-b5c` + `p9-toc-do-6` (hồ sơ). Worktree `/tmp`: không còn. Ảnh docker cục bộ: `hue-rag-app:dep10b` (đạt), `dep10`, `nhap2` (cũ, xoá được).

### Mã hay gặp
G = cổng 2 nhóm (đóng); T1 ngày + âm lịch (bật, bản nhanh 10/11); T2 / T3 / T4 đóng hồ sơ 09/11; S1–S6 / S2b = sàn §12.3; B0–B7 = bậc Phase 9; S / W / I = sổ `SO_CAI_TIEN_CACH_LAM.md`.

