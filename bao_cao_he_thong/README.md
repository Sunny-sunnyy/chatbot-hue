# Báo cáo hệ thống hue_rag — mục lục cho bạn

**Cập nhật lần cuối: 17:07 25/10/2026.** Bạn chỉ cần đọc thư mục này. Báo cáo kỹ thuật của agent ở
`report_agent/`; report cũ tới 24/10 ở `reports/` (lịch sử).

## Muốn biết gì ⇒ đọc file nào

| Muốn biết | File | Cập nhật lần cuối |
|---|---|---|
| Chatbot đang chạy thế nào (toàn cảnh) | [LUONG_HOAT_DONG_HE_THONG.md](LUONG_HOAT_DONG_HE_THONG.md) | 19:58 24/10/2026 |
| Chất lượng hiện tại, điểm mốc, chỗ yếu (Phase 7B) | [BAO_CAO_DANH_GIA.md](BAO_CAO_DANH_GIA.md) | 14:18 25/10/2026 (+ 8.1) |
| Nền tảng dự án (Phase 0–1) | [BAO_CAO_NEN_TANG.md](BAO_CAO_NEN_TANG.md) | 24/10/2026 |
| Chia tài liệu thành đoạn (Phase 2) | [BAO_CAO_CHIA_DOAN.md](BAO_CAO_CHIA_DOAN.md) | 14:18 25/10/2026 (+ 8.1) |
| Vector nghĩa + từ khóa (Phase 3) | [BAO_CAO_EMBEDDING_TU_KHOA.md](BAO_CAO_EMBEDDING_TU_KHOA.md) | 14:18 25/10/2026 (+ 8.1) |
| Lưu vào Qdrant (Phase 4) | [BAO_CAO_LUU_TRU_QDRANT.md](BAO_CAO_LUU_TRU_QDRANT.md) | 24/10/2026 |
| Tìm đoạn liên quan (Phase 5) | [BAO_CAO_TIM_KIEM.md](BAO_CAO_TIM_KIEM.md) | 14:18 25/10/2026 (+ 8.1) |
| Sinh câu trả lời, API, giao diện (Phase 6) | [BAO_CAO_SINH_CAU_TRA_LOI_API.md](BAO_CAO_SINH_CAU_TRA_LOI_API.md) | 14:18 25/10/2026 (+ 8.1) |
| Bộ câu hỏi chuẩn Golden (Phase 7, 7A) | [BAO_CAO_BO_CAU_HOI_GOLDEN.md](BAO_CAO_BO_CAU_HOI_GOLDEN.md) | 14:18 25/10/2026 (+ 8.1) |
| Sửa kho dữ liệu, tạo lại chỉ mục (Phase 7A2) | [BAO_CAO_KHO_DU_LIEU.md](BAO_CAO_KHO_DU_LIEU.md) | 24/10/2026 |
| Chuyện từng ngày | [nhat_ky/](nhat_ky/) — mới nhất: [25/10 tối — thiết kế 8.2, dừng để rà code](nhat_ky/2026-10-25_phase_8_2_va_ra_soat_code.md) | 17:07 25/10/2026 |

## Trạng thái ngắn

| Phần | Trạng thái |
|---|---|
| Chatbot full-corpus (205 file, 8.459 đoạn, e5-small + BM25, gpt-6-luna) | Đã xử lý, đóng gói |
| Thước đo + điểm mốc 176 câu | Đã xử lý, đóng gói (chưa có mốc người chấm) |
| Từ chối nhầm 22/158 câu, bảng giá khó tìm, đoạn vụn | Chưa thực hiện → đo ở 8.1, sửa ở 8.2 |
| Index Qwen3-8B | Chưa thực hiện → Phase 8.2 |
| Dọn code + 2 kho món ăn cũ | Đã xử lý, đóng gói (bạn đóng 20:01) |
| Rà 56 quyết định Phase 0–7 (Phase 8.1) | Đã xử lý, đóng gói (bạn đóng 15:27 25/10): **chỉ "10 đoạn thay vì 5" thắng** → áp dụng ở 8.2 sau mốc người |
| Phase 8.2 (áp dụng phương án thắng) | Xử lý một phần — thiết kế duyệt 16:21 25/10; "10 đoạn + NFC" chạy đạt nhưng **chưa vào chatbot**; **tạm dừng** để rà code |
| Rà code các Phase trước | Chưa thực hiện → đang làm (dở), tiếp phiên sau |
| Câu hỏi gõ không dấu | Chưa thực hiện — **ngoài phạm vi** (bạn quyết 15:15 25/10: người dùng gõ có dấu). Đã đo: tìm kiếm gần như hỏng (13/32 → 1/32 câu) |

Thang 5 mức: Đã xử lý, đóng gói · Đã xử lý · Xử lý một phần · Đã thử, chưa áp dụng · Chưa thực hiện.

## Luật cập nhật (cho agent)

Mỗi thay đổi vào hệ thống đang chạy ⇒ sửa `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_<KHÂU>.md` của đúng
khâu (cả Tóm tắt), `nhat_ky/` của đợt, `session_prompt/Project_Status.md`, rồi bảng trên. Mẫu:
`session_prompt/TEMPLATE_USER_REPORT.md`, `session_prompt/TEMPLATE_NHAT_KY.md`; quy tắc
`session_prompt/WORKFLOW.md` §6. Giờ lấy bằng `date`.
