# Báo cáo hệ thống hue_rag — mục lục cho bạn

**Cập nhật lần cuối: 14:19 30/10/2026.** Bạn chỉ cần đọc thư mục này. Báo cáo kỹ thuật của agent ở
`report_agent/`; report cũ tới 24/10 ở `reports/` (lịch sử).

## Muốn biết gì ⇒ đọc file nào

| Muốn biết | File | Cập nhật lần cuối |
|---|---|---|
| Chatbot đang chạy thế nào (toàn cảnh) | [LUONG_HOAT_DONG_HE_THONG.md](LUONG_HOAT_DONG_HE_THONG.md) | 14:19 30/10/2026 (đợt 2 sửa kho: 204 file / 8.424 đoạn; thời gian chờ ở 10 đoạn; cách chạy không đổi) |
| Chất lượng hiện tại, điểm mốc, chỗ yếu, thước đo (7B, 8.1, 8.2, đợt sửa kho 1–2) | [BAO_CAO_DANH_GIA.md](BAO_CAO_DANH_GIA.md) | 14:32 30/10/2026 (bản 5: nhãn bản 5, đợt 2 không làm hỏng, bộ 32 câu an toàn + thước lỗi nặng, Golden sửa 2 đáp án) |
| Nền tảng dự án (Phase 0–1) | [BAO_CAO_NEN_TANG.md](BAO_CAO_NEN_TANG.md) | 16:0x 26/10/2026 (đợt 3) |
| Chia tài liệu thành đoạn (Phase 2) | [BAO_CAO_CHIA_DOAN.md](BAO_CAO_CHIA_DOAN.md) | 16:0x 26/10/2026 (đợt 3, bản 4) |
| Vector nghĩa + từ khóa (Phase 3) | [BAO_CAO_EMBEDDING_TU_KHOA.md](BAO_CAO_EMBEDDING_TU_KHOA.md) | 14:18 25/10/2026 (+ 8.1) |
| Lưu vào Qdrant (Phase 4) | [BAO_CAO_LUU_TRU_QDRANT.md](BAO_CAO_LUU_TRU_QDRANT.md) | 24/10/2026 |
| Tìm đoạn liên quan (Phase 5) | [BAO_CAO_TIM_KIEM.md](BAO_CAO_TIM_KIEM.md) | 09:38 28/10/2026 (bản 9: chuẩn hóa NFC câu hỏi vào chatbot) |
| Sinh câu trả lời, API, giao diện (Phase 6) | [BAO_CAO_SINH_CAU_TRA_LOI_API.md](BAO_CAO_SINH_CAU_TRA_LOI_API.md) | 09:38 28/10/2026 (bản 12: chatbot đưa 10 đoạn vào ngữ cảnh — chưa có mốc người) |
| Bộ câu hỏi chuẩn Golden (Phase 7, 7A) | [BAO_CAO_BO_CAU_HOI_GOLDEN.md](BAO_CAO_BO_CAU_HOI_GOLDEN.md) | 14:28 30/10/2026 (bản 6: 2 đáp án sửa sau đợt 2, md5 mới; câu kín đã dùng; nhãn bản 5) |
| Sửa kho dữ liệu, tạo lại chỉ mục (Phase 7A2 → đợt 1 28/10 → đợt 2 **đã áp** 30/10) | [BAO_CAO_KHO_DU_LIEU.md](BAO_CAO_KHO_DU_LIEU.md) | 14:19 30/10/2026 (bản 6: đợt 2 123 sửa / 40 file, 204 file / 8.424 đoạn, không làm hỏng, 0 câu sai điều kiện mới) |
| Rà code: nên sửa gì (bạn duyệt 5 gói 19:4x 25/10 — **đã sửa xong cả 5**, 26/10) | [DE_XUAT_SUA_CODE.md](DE_XUAT_SUA_CODE.md) | 18:56 25/10/2026 |
| Chuyện từng ngày | [nhat_ky/](nhat_ky/) — mới nhất: [30/10 — áp đợt 2 sửa kho, chuẩn bị Qwen3-8B, đọc khoá học](nhat_ky/2026-10-30_ap_dot_2_sua_kho.md); trước: [29/10 — chuẩn bị đợt 2 sửa kho, đo nhiễu thước lỗi nặng](nhat_ky/2026-10-29_chuan_bi_dot_2.md) | 14:17 30/10/2026 |

## Trạng thái ngắn

| Phần | Trạng thái |
|---|---|
| Chatbot full-corpus (204 file, 8.426 đoạn từ 28/10 sau sửa kho; e5-small + BM25, gpt-6-luna, 10 đoạn ngữ cảnh) | Đã xử lý, đóng gói |
| Thước đo + điểm mốc 176 câu | Đã xử lý, đóng gói (chưa có mốc người chấm) |
| Từ chối nhầm 22/158 câu, bảng giá khó tìm, đoạn vụn | 8.1 đo; 8.2: 10 đoạn ngữ cảnh đã vào chatbot 28/10 (đỡ câu thiếu bằng chứng); phần còn lại chưa xử lý |
| Index Qwen3-8B | Chưa thực hiện → thí nghiệm sau đợt sửa kho (User 27/10) |
| Dọn code + 2 kho món ăn cũ | Đã xử lý, đóng gói (bạn đóng 20:01) |
| Rà 56 quyết định Phase 0–7 (Phase 8.1) | Đã xử lý, đóng gói (bạn đóng 15:27 25/10): **chỉ "10 đoạn thay vì 5" thắng** → đã áp dụng 28/10 (Phase 8.2) |
| Phase 8.2 (áp dụng phương án thắng) | **Đã xử lý, đóng gói** (bạn đóng 10:23 28/10): **10 đoạn + NFC** vào chatbot (`510e1a8`); phép kiểm cuối 36 câu kín: đủ ý +0,82, đúng +0,70, 0 câu kém đi, câu ngoài kho vẫn từ chối 3 / 3; **chưa có mốc người** (bạn đọc cặp mù sau); tốc độ chưa đạt mức bạn chốt |
| Rà code các Phase trước | **Đã xử lý, đóng gói** — 5 gói sửa xong 26/10 (1a, 1b, 3, 4 ngày 25/10; đợt 3 = gói 2 + 5 ngày 26/10); mỗi gói review chéo + cổng ổn định; code backend 8.345 → 6.218 dòng |
| Câu hỏi gõ không dấu | Chưa thực hiện — **ngoài phạm vi** (bạn quyết 15:15 25/10: người dùng gõ có dấu). Đã đo: tìm kiếm gần như hỏng (13/32 → 1/32 câu) |

Thang 5 mức: Đã xử lý, đóng gói · Đã xử lý · Xử lý một phần · Đã thử, chưa áp dụng · Chưa thực hiện.

## Luật cập nhật (cho agent)

Mỗi thay đổi vào hệ thống đang chạy ⇒ sửa `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_<KHÂU>.md` của đúng
khâu (cả Tóm tắt), `nhat_ky/` của đợt, `session_prompt/Project_Status.md`, rồi bảng trên. Mẫu:
`session_prompt/TEMPLATE_USER_REPORT.md`, `session_prompt/TEMPLATE_NHAT_KY.md`; quy tắc
`session_prompt/WORKFLOW.md` §6. Giờ lấy bằng `date`.
