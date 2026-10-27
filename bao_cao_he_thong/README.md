# Báo cáo hệ thống hue_rag — mục lục cho bạn

**Cập nhật lần cuối: 22:31 26/10/2026.** Bạn chỉ cần đọc thư mục này. Báo cáo kỹ thuật của agent ở
`report_agent/`; report cũ tới 24/10 ở `reports/` (lịch sử).

## Muốn biết gì ⇒ đọc file nào

| Muốn biết | File | Cập nhật lần cuối |
|---|---|---|
| Chatbot đang chạy thế nào (toàn cảnh) | [LUONG_HOAT_DONG_HE_THONG.md](LUONG_HOAT_DONG_HE_THONG.md) | 13:30 27/10/2026 (API ghi một dòng số đo mỗi câu) |
| Chất lượng hiện tại, điểm mốc, chỗ yếu (Phase 7B) | [BAO_CAO_DANH_GIA.md](BAO_CAO_DANH_GIA.md) | 14:18 25/10/2026 (+ 8.1) |
| Nền tảng dự án (Phase 0–1) | [BAO_CAO_NEN_TANG.md](BAO_CAO_NEN_TANG.md) | 16:0x 26/10/2026 (đợt 3) |
| Chia tài liệu thành đoạn (Phase 2) | [BAO_CAO_CHIA_DOAN.md](BAO_CAO_CHIA_DOAN.md) | 16:0x 26/10/2026 (đợt 3, bản 4) |
| Vector nghĩa + từ khóa (Phase 3) | [BAO_CAO_EMBEDDING_TU_KHOA.md](BAO_CAO_EMBEDDING_TU_KHOA.md) | 14:18 25/10/2026 (+ 8.1) |
| Lưu vào Qdrant (Phase 4) | [BAO_CAO_LUU_TRU_QDRANT.md](BAO_CAO_LUU_TRU_QDRANT.md) | 24/10/2026 |
| Tìm đoạn liên quan (Phase 5) | [BAO_CAO_TIM_KIEM.md](BAO_CAO_TIM_KIEM.md) | 10:49 27/10/2026 (bản 8: K3, K3b — model chọn 10 / 30 đoạn) |
| Sinh câu trả lời, API, giao diện (Phase 6) | [BAO_CAO_SINH_CAU_TRA_LOI_API.md](BAO_CAO_SINH_CAU_TRA_LOI_API.md) | 13:30 27/10/2026 (bản 11: API ghi số đo mỗi câu; thời gian chờ thật) |
| Bộ câu hỏi chuẩn Golden (Phase 7, 7A) | [BAO_CAO_BO_CAU_HOI_GOLDEN.md](BAO_CAO_BO_CAU_HOI_GOLDEN.md) | 14:18 25/10/2026 (+ 8.1) |
| Sửa kho dữ liệu, tạo lại chỉ mục (Phase 7A2) | [BAO_CAO_KHO_DU_LIEU.md](BAO_CAO_KHO_DU_LIEU.md) | 24/10/2026 |
| Rà code: nên sửa gì (bạn duyệt 5 gói 19:4x 25/10 — **đã sửa xong cả 5**, 26/10) | [DE_XUAT_SUA_CODE.md](DE_XUAT_SUA_CODE.md) | 18:56 25/10/2026 |
| Chuyện từng ngày | [nhat_ky/](nhat_ky/) — mới nhất: [27/10 chiều — dọn phần tồn Phase cũ, soạn sẵn đợt sửa kho](nhat_ky/2026-10-27_chieu_phan_ton.md); trước: [27/10 sáng — chốt đợt cải tiến](nhat_ky/2026-10-27_chot_dot_cai_tien.md) | 15:28 27/10/2026 |

## Trạng thái ngắn

| Phần | Trạng thái |
|---|---|
| Chatbot full-corpus (205 file, 8.459 đoạn, e5-small + BM25, gpt-6-luna) | Đã xử lý, đóng gói |
| Thước đo + điểm mốc 176 câu | Đã xử lý, đóng gói (chưa có mốc người chấm) |
| Từ chối nhầm 22/158 câu, bảng giá khó tìm, đoạn vụn | Chưa thực hiện → đo ở 8.1, sửa ở 8.2 |
| Index Qwen3-8B | Chưa thực hiện → Phase 8.2 |
| Dọn code + 2 kho món ăn cũ | Đã xử lý, đóng gói (bạn đóng 20:01) |
| Rà 56 quyết định Phase 0–7 (Phase 8.1) | Đã xử lý, đóng gói (bạn đóng 15:27 25/10): **chỉ "10 đoạn thay vì 5" thắng** → áp dụng ở 8.2 sau mốc người |
| Phase 8.2 (áp dụng phương án thắng) | Xử lý một phần — thiết kế duyệt 16:21 25/10 + **sửa đổi 26/10 (§10: đợt cải tiến từng khâu, phạm vi B)**; "10 đoạn + NFC" đưa lên `main` mới, đạt, **chưa vào chatbot** (chờ bạn đọc cặp mù B0). Tối 26/10: K1 kém hơn, R2 kém hơn (gác), R3 không đủ câu; K3 (model xếp lại) duyệt, chạy phiên sau |
| Rà code các Phase trước | **Đã xử lý, đóng gói** — 5 gói sửa xong 26/10 (1a, 1b, 3, 4 ngày 25/10; đợt 3 = gói 2 + 5 ngày 26/10); mỗi gói review chéo + cổng ổn định; code backend 8.345 → 6.218 dòng |
| Câu hỏi gõ không dấu | Chưa thực hiện — **ngoài phạm vi** (bạn quyết 15:15 25/10: người dùng gõ có dấu). Đã đo: tìm kiếm gần như hỏng (13/32 → 1/32 câu) |

Thang 5 mức: Đã xử lý, đóng gói · Đã xử lý · Xử lý một phần · Đã thử, chưa áp dụng · Chưa thực hiện.

## Luật cập nhật (cho agent)

Mỗi thay đổi vào hệ thống đang chạy ⇒ sửa `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_<KHÂU>.md` của đúng
khâu (cả Tóm tắt), `nhat_ky/` của đợt, `session_prompt/Project_Status.md`, rồi bảng trên. Mẫu:
`session_prompt/TEMPLATE_USER_REPORT.md`, `session_prompt/TEMPLATE_NHAT_KY.md`; quy tắc
`session_prompt/WORKFLOW.md` §6. Giờ lấy bằng `date`.
