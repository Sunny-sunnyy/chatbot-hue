# Báo cáo hệ thống hue_rag — mục lục cho bạn

**Cập nhật lần cuối: 17:18 31/10/2026.** (31/10 chiều: rà lại cả 11 báo cáo cho đúng hiện trạng, xoá phần không còn đúng — bạn yêu cầu.) Bạn chỉ cần đọc thư mục này. Báo cáo kỹ thuật của agent ở
`report_agent/`; report cũ tới 24/10 ở `reports/` (lịch sử).

## Muốn biết gì ⇒ đọc file nào

| Muốn biết | File | Cập nhật lần cuối |
|---|---|---|
| Chatbot đang chạy thế nào (toàn cảnh) | [LUONG_HOAT_DONG_HE_THONG.md](LUONG_HOAT_DONG_HE_THONG.md) | 17:10 31/10/2026 (bản 14: rà lại cả file — số hiện hành 204 file / 8.424 đoạn, 12 / 158 từ chối nhầm, 2,19 / 4,90 s, ≈ 0,00025 USD / câu; khối "đã thử, không đưa vào"; bật Docker Desktop) |
| Chất lượng hiện tại, điểm mốc, chỗ yếu, thước đo (7B, 8.1, 8.2, đợt sửa kho 1–2) | [BAO_CAO_DANH_GIA.md](BAO_CAO_DANH_GIA.md) | 17:12 31/10/2026 (bản 6: rà lại — thước đang dùng gold v5, Golden, bộ an toàn 32 câu, bộ 15 câu theo ngày; thước streaming chưa code) |
| Nền tảng dự án (Phase 0–1) | [BAO_CAO_NEN_TANG.md](BAO_CAO_NEN_TANG.md) | 17:12 31/10/2026 (bản 5: rà lại — 11 gói Python, mốc test 197 đạt 26/10, số dòng code đúng lại) |
| Chia tài liệu thành đoạn (Phase 2) | [BAO_CAO_CHIA_DOAN.md](BAO_CAO_CHIA_DOAN.md) | 17:10 31/10/2026 (bản 6: rà lại — 204 file / 8.424 đoạn, bộ chia đoạn không đổi; file danh mục đã loại 28/10; thống kê token đo trên kho cũ) |
| Vector nghĩa + từ khóa (Phase 3) | [BAO_CAO_EMBEDDING_TU_KHOA.md](BAO_CAO_EMBEDDING_TU_KHOA.md) | 17:10 31/10/2026 (bản 5: rà lại — e5-small + BM25, từ vựng 5.631; Qwen3-8B kém hơn, không chọn) |
| Lưu vào Qdrant (Phase 4) | [BAO_CAO_LUU_TRU_QDRANT.md](BAO_CAO_LUU_TRU_QDRANT.md) | 17:13 31/10/2026 (bản 4: rà lại — 8.424 điểm, build lại 28/10 + 30/10; collection thử Qwen3-8B đã xoá; Docker Desktop) |
| Tìm đoạn liên quan (Phase 5) | [BAO_CAO_TIM_KIEM.md](BAO_CAO_TIM_KIEM.md) | 17:14 31/10/2026 (bản 11: rà lại — số đo trên kho hiện tại 24 / 40, MRR 0,731; các cách đã thử và bỏ; cách tìm không đổi) |
| Sinh câu trả lời, API, giao diện (Phase 6) | [BAO_CAO_SINH_CAU_TRA_LOI_API.md](BAO_CAO_SINH_CAU_TRA_LOI_API.md) | 17:10 31/10/2026 (bản 14: rà lại — số 30/10, streaming "đang thiết kế"; số cấu hình cũ ghi rõ là cũ) |
| Bộ câu hỏi chuẩn Golden (Phase 7, 7A) | [BAO_CAO_BO_CAU_HOI_GOLDEN.md](BAO_CAO_BO_CAU_HOI_GOLDEN.md) | 17:18 31/10/2026 (bản 7: rà lại; **chạy lại kiểm Golden sau 2 đợt sửa kho: 1 câu có keyword không còn nguyên văn trong kho — chờ bạn duyệt sửa**) |
| Sửa kho dữ liệu, tạo lại chỉ mục (Phase 7A2 → đợt 1 28/10 → đợt 2 **đã áp** 30/10) | [BAO_CAO_KHO_DU_LIEU.md](BAO_CAO_KHO_DU_LIEU.md) | 17:14 31/10/2026 (bản 7: rà lại — 2 đợt sửa kho đóng, giữ sao lưu; 204 file / 8.424 đoạn) |
| Rà code: nên sửa gì (bạn duyệt 5 gói 25/10 — **đã sửa xong cả 5**, 26/10) | [DE_XUAT_SUA_CODE.md](DE_XUAT_SUA_CODE.md) | 17:11 31/10/2026 (bản 3: viết lại thành "5 gói đã xong", kèm commit) |
| Chuyện từng ngày | [nhat_ky/](nhat_ky/) — mới nhất: [31/10 chiều — áp khung AI FDE vào cách làm; sửa 4 báo cáo bị cũ](nhat_ky/2026-10-31_khung_fde_va_cap_nhat_bao_cao.md); trước: [31/10 sáng — spec streaming (D1–D3 chốt), tra web bằng Codex, cấm Claude gọi AGY](nhat_ky/2026-10-31_spec_streaming_tra_web_codex.md) | 17:00 31/10/2026 |

## Trạng thái ngắn

| Phần | Trạng thái |
|---|---|
| Chatbot full-corpus (204 file, 8.424 đoạn từ 30/10 sau đợt 2 sửa kho; e5-small + BM25, gpt-6-luna, 10 đoạn ngữ cảnh) | Đã xử lý, đóng gói |
| Thước đo + điểm mốc 176 câu | Đã xử lý, đóng gói (chưa có mốc người chấm) |
| Từ chối nhầm, bảng giá khó tìm, đoạn vụn | Xử lý một phần: từ chối nhầm 22 / 158 câu (8.1, 5 đoạn) ⇒ **12 / 158** (30/10, 10 đoạn + kho sửa đợt 2); bảng giá khó tìm, đoạn vụn chưa xử lý |
| Model vector Qwen3-8B thay e5-small | **Đã thử, chưa áp dụng** (30/10): kém hơn — 3 / 40 câu thử mất đoạn đúng, bước tìm theo nghĩa chậm 0,02 ⇒ 2,2 s; chỉ mục thử đã xóa |
| Dọn code + 2 kho món ăn cũ | Đã xử lý, đóng gói (bạn đóng 20:01) |
| Rà 56 quyết định Phase 0–7 (Phase 8.1) | Đã xử lý, đóng gói (bạn đóng 15:27 25/10): **chỉ "10 đoạn thay vì 5" thắng** → đã áp dụng 28/10 (Phase 8.2) |
| Phase 8.2 (áp dụng phương án thắng) | **Đã xử lý, đóng gói** (bạn đóng 10:23 28/10): **10 đoạn + NFC** vào chatbot (`510e1a8`); phép kiểm cuối 36 câu kín: đủ ý +0,82, đúng +0,70, 0 câu kém đi, câu ngoài kho vẫn từ chối 3 / 3; **chưa có mốc người** (bạn đọc cặp mù sau); tốc độ chưa đạt mức bạn chốt |
| Rà code các Phase trước | **Đã xử lý, đóng gói** — 5 gói sửa xong 26/10 (1a, 1b, 3, 4 ngày 25/10; đợt 3 = gói 2 + 5 ngày 26/10); mỗi gói review chéo + cổng ổn định; code backend 8.345 → 6.218 dòng |
| Câu hỏi theo ngày tương đối ("tối nay", "tuần này") | Xử lý một phần — an toàn (0 câu đoán ngày sai, đo 30/10); 6 / 14 câu bị từ chối nhầm ⇒ **để Phase 9** (bạn quyết 14:44 30/10) |
| Hiện chữ dần (streaming) | Chưa thực hiện — đang thiết kế: spec bản 4 review đạt, bạn chốt D1–D3 (31/10); còn câu Q1 + bạn duyệt bản ⇒ mới code |
| Phase 9 | Chưa thực hiện — **mở bằng nghiên cứu rộng** (đề tài, dự án, paper, ứng dụng thật), bạn chốt 31/10; Phase 1–8 = "RAG mức 1" |
| Cách làm việc của các agent (luật, skill, hook) | 31/10 chiều áp khung AI FDE: hook giờ ước, xét lại luật đang thử (40 ⇒ 7), skill D + 2 skill agent — xem nhật ký 31/10 chiều |
| Câu hỏi gõ không dấu | Chưa thực hiện — **ngoài phạm vi** (bạn quyết 15:15 25/10: người dùng gõ có dấu). Đã đo: tìm kiếm gần như hỏng (13/32 → 1/32 câu) |

Thang 5 mức: Đã xử lý, đóng gói · Đã xử lý · Xử lý một phần · Đã thử, chưa áp dụng · Chưa thực hiện.

## Luật cập nhật (cho agent)

Mỗi thay đổi vào hệ thống đang chạy ⇒ sửa `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_<KHÂU>.md` của đúng
khâu (cả Tóm tắt), `nhat_ky/` của đợt, `session_prompt/Project_Status.md`, rồi bảng trên. Mẫu:
`session_prompt/TEMPLATE_USER_REPORT.md`, `session_prompt/TEMPLATE_NHAT_KY.md`; quy tắc
`session_prompt/WORKFLOW.md` §6. Giờ lấy bằng `date`.
