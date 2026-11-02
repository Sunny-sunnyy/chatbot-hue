# Báo cáo hệ thống hue_rag — mục lục cho bạn

**Cập nhật lần cuối: 14:33 01/11/2026 (B0 xong; Phase 8 bạn đóng 14:29 01/11/2026).** Trước: 17:18 31/10/2026. (31/10 chiều: rà lại cả 11 báo cáo cho đúng hiện trạng, xoá phần không còn đúng — bạn yêu cầu.) Bạn chỉ cần đọc thư mục này. Báo cáo kỹ thuật của agent ở
`report_agent/`; report cũ tới 24/10 ở `reports/` (lịch sử).

## Muốn biết gì ⇒ đọc file nào

| Muốn biết | File | Cập nhật lần cuối |
|---|---|---|
| Chatbot đang chạy thế nào (toàn cảnh) | [LUONG_HOAT_DONG_HE_THONG.md](LUONG_HOAT_DONG_HE_THONG.md) | 10:36 02/11/2026 (bản 19: giao diện web mới) · 14:33 01/11/2026 (B0, Phase 8 đóng) · 12:51 01/11/2026 (bản 17: streaming chạy; lượt đo cuối xong — mọi sàn đạt) · 11:33 01/11/2026 (bản 15: giới hạn đã biết theo mức nặng; streaming đang code; nhiều lượt ⇒ Phase 9) · 17:10 31/10/2026 (bản 14: rà lại cả file — số hiện hành 204 file / 8.424 đoạn, 12 / 158 từ chối nhầm, 2,19 / 4,90 s, ≈ 0,00025 USD / câu; khối "đã thử, không đưa vào"; bật Docker Desktop) |
| **Nghiên cứu rộng trước Phase 9** (thực tế triển khai, người dùng cần gì, paper, repo; Huế TRIPO) | [BAO_CAO_NGHIEN_CUU_PHASE_9.md](BAO_CAO_NGHIEN_CUU_PHASE_9.md) | 14:55 02/11/2026 (bản 3: đổi hướng agent có công cụ — khoá AI FDE, ChatGPT, Serper, SDK; spec duyệt) · 16:13 01/11/2026 (bản 2: ChatGPT đã kiểm, thử Huế TRIPO 10 câu, hướng Phase 9 bạn chọn, lịch đến bảo vệ) · 15:25 01/11/2026 (bản 1 sơ bộ) |
| **So sánh mọi phương án đã thử / chọn / bỏ** (Phase 0 → 8.2, sửa kho, Qwen3-8B) — theo khâu + theo Phase | [BAO_CAO_SO_SANH_PHUONG_AN.md](BAO_CAO_SO_SANH_PHUONG_AN.md) | 14:33 01/11/2026 (bản 5: B0 — E7, S2, §6) · 11:29 01/11/2026 (bản 3: mới; 62 khối, có số đo + nhãn độ tin; 2 lượt kiểm độc lập đạt; phần streaming / đo cuối thêm sau) |
| Chất lượng hiện tại, điểm mốc, chỗ yếu, thước đo (7B, 8.1, 8.2, đợt sửa kho 1–2) | [BAO_CAO_DANH_GIA.md](BAO_CAO_DANH_GIA.md) | 14:33 01/11/2026 (B0 — mốc người tham khảo) · 12:03 01/11/2026 (đo lại theo loại câu) · 11:34 01/11/2026 (câu Golden lệch: điểm không lệch, giữ nguyên) · 17:12 31/10/2026 (bản 6: rà lại — thước đang dùng gold v5, Golden, bộ an toàn 32 câu, bộ 15 câu theo ngày; thước streaming chưa code) |
| Nền tảng dự án (Phase 0–1) | [BAO_CAO_NEN_TANG.md](BAO_CAO_NEN_TANG.md) | 17:12 31/10/2026 (bản 5: rà lại — 11 gói Python, mốc test 197 đạt 26/10, số dòng code đúng lại) |
| Chia tài liệu thành đoạn (Phase 2) | [BAO_CAO_CHIA_DOAN.md](BAO_CAO_CHIA_DOAN.md) | 17:10 31/10/2026 (bản 6: rà lại — 204 file / 8.424 đoạn, bộ chia đoạn không đổi; file danh mục đã loại 28/10; thống kê token đo trên kho cũ) |
| Vector nghĩa + từ khóa (Phase 3) | [BAO_CAO_EMBEDDING_TU_KHOA.md](BAO_CAO_EMBEDDING_TU_KHOA.md) | 17:10 31/10/2026 (bản 5: rà lại — e5-small + BM25, từ vựng 5.631; Qwen3-8B kém hơn, không chọn) |
| Lưu vào Qdrant (Phase 4) | [BAO_CAO_LUU_TRU_QDRANT.md](BAO_CAO_LUU_TRU_QDRANT.md) | 17:13 31/10/2026 (bản 4: rà lại — 8.424 điểm, build lại 28/10 + 30/10; collection thử Qwen3-8B đã xoá; Docker Desktop) |
| Tìm đoạn liên quan (Phase 5) | [BAO_CAO_TIM_KIEM.md](BAO_CAO_TIM_KIEM.md) | 12:03 01/11/2026 (đo lại theo loại câu, nhiều nguồn ⇒ Phase 9) · 11:07 01/11/2026 (sửa lý do gác chọn đoạn bằng luna) · 17:14 31/10/2026 (bản 11: rà lại — số đo trên kho hiện tại 24 / 40, MRR 0,731; các cách đã thử và bỏ; cách tìm không đổi) |
| Sinh câu trả lời, API, giao diện (Phase 6) | [BAO_CAO_SINH_CAU_TRA_LOI_API.md](BAO_CAO_SINH_CAU_TRA_LOI_API.md) | 10:36 02/11/2026 (bản 18: giao diện web mới — React, nguồn số nhỏ bấm được, nhãn AI) · 14:33 01/11/2026 (B0) · 12:51 01/11/2026 (bản 16: streaming vào chatbot, chữ đầu 1,23 / 2,61 s) · 11:07 01/11/2026 (bản 15: streaming spec duyệt + bước 1 / 4 xong trên nhánh; tốc độ qua API p95 6,0 s chưa đạt) · 17:10 31/10/2026 (bản 14: rà lại — số 30/10, streaming "đang thiết kế"; số cấu hình cũ ghi rõ là cũ) |
| Bộ câu hỏi chuẩn Golden (Phase 7, 7A) | [BAO_CAO_BO_CAU_HOI_GOLDEN.md](BAO_CAO_BO_CAU_HOI_GOLDEN.md) | 11:04 01/11/2026 (bản 8: 1 câu keyword lệch kho chỉ ở hoa / thường — chấm không sai; **bạn giữ nguyên**) |
| Sửa kho dữ liệu, tạo lại chỉ mục (Phase 7A2 → đợt 1 28/10 → đợt 2 **đã áp** 30/10) | [BAO_CAO_KHO_DU_LIEU.md](BAO_CAO_KHO_DU_LIEU.md) | 11:04 01/11/2026 (câu Golden lệch: giữ nguyên) · 17:14 31/10/2026 (bản 7: rà lại — 2 đợt sửa kho đóng, giữ sao lưu; 204 file / 8.424 đoạn) |
| Rà code: nên sửa gì (bạn duyệt 5 gói 25/10 — **đã sửa xong cả 5**, 26/10) | [DE_XUAT_SUA_CODE.md](DE_XUAT_SUA_CODE.md) | 17:11 31/10/2026 (bản 3: viết lại thành "5 gói đã xong", kèm commit) |
| Chuyện từng ngày | [nhat_ky/](nhat_ky/) — mới nhất: [02/11 — giao diện web mới vào chatbot; Phase 9 thành trợ lý agent, spec duyệt](nhat_ky/2026-11-02_giao_dien_moi_va_spec_phase_9.md) · trước: [01/11 — streaming vào chatbot, lượt đo cuối Phase 1–8 (mọi sàn đạt), báo cáo so sánh; chiều: B0, đóng Phase 8](nhat_ky/2026-11-01_streaming_va_dong_goi.md); trước: [31/10 chiều — áp khung AI FDE; rà lại cả 11 báo cáo; khung báo cáo so sánh](nhat_ky/2026-10-31_khung_fde_va_cap_nhat_bao_cao.md); trước: [31/10 sáng — spec streaming (D1–D3 chốt), tra web bằng Codex, cấm Claude gọi AGY](nhat_ky/2026-10-31_spec_streaming_tra_web_codex.md) | 14:33 01/11/2026 |

## Trạng thái ngắn

| Phần | Trạng thái |
|---|---|
| Chatbot full-corpus (204 file, 8.424 đoạn từ 30/10 sau đợt 2 sửa kho; e5-small + BM25, gpt-6-luna, 10 đoạn ngữ cảnh) | Đã xử lý, đóng gói |
| Thước đo + điểm mốc 176 câu | Đã xử lý, đóng gói; mốc người B0 (01/11) chỉ tham khảo — xem dòng Phase 8.2 |
| Từ chối nhầm, bảng giá khó tìm, đoạn vụn | Xử lý một phần: từ chối nhầm 22 / 158 câu (8.1, 5 đoạn) ⇒ **12 / 158** (30/10, 10 đoạn + kho sửa đợt 2); bảng giá khó tìm, đoạn vụn chưa xử lý |
| Model vector Qwen3-8B thay e5-small | **Đã thử, chưa áp dụng** (30/10): kém hơn — 3 / 40 câu thử mất đoạn đúng, bước tìm theo nghĩa chậm 0,02 ⇒ 2,2 s; chỉ mục thử đã xóa |
| Dọn code + 2 kho món ăn cũ | Đã xử lý, đóng gói (bạn đóng 20:01) |
| Rà 56 quyết định Phase 0–7 (Phase 8.1) | Đã xử lý, đóng gói (bạn đóng 15:27 25/10): **chỉ "10 đoạn thay vì 5" thắng** → đã áp dụng 28/10 (Phase 8.2) |
| Phase 8.2 (áp dụng phương án thắng) | **Đã xử lý, đóng gói** (bạn đóng 10:23 28/10): **10 đoạn + NFC** vào chatbot (`510e1a8`); phép kiểm cuối 36 câu kín: đủ ý +0,82, đúng +0,70, 0 câu kém đi, câu ngoài kho vẫn từ chối 3 / 3; tốc độ khi đó chưa đạt (01/11 có streaming: đạt). B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp). |
| Phase 8 (đóng gói Phase 1–8: streaming, giá đủ, lượt đo cuối, B0) | **Đã xử lý, đóng gói** — Phase 8 bạn đóng 14:29 01/11/2026; lượt đo cuối mọi sàn đạt |
| Rà code các Phase trước | **Đã xử lý, đóng gói** — 5 gói sửa xong 26/10 (1a, 1b, 3, 4 ngày 25/10; đợt 3 = gói 2 + 5 ngày 26/10); mỗi gói review chéo + cổng ổn định; code backend 8.345 → 6.218 dòng |
| Câu hỏi theo ngày tương đối ("tối nay", "tuần này") | Xử lý một phần — an toàn (0 câu đoán ngày sai, đo 30/10); 6 / 14 câu bị từ chối nhầm ⇒ **để Phase 9** (bạn quyết 14:44 30/10) |
| Hiện chữ dần (streaming) | **Đã xử lý, đóng gói** 01/11 (merge `a80e12d`) — chữ đầu trên trình duyệt 1,23 / 2,61 s; giao diện JS thuần sẽ làm lại sau Phase 8 |
| Phase 9 | **Spec duyệt 14:55 02/11/2026** (bạn duyệt bản 9 `169c2dd5f86a`): trợ lý **agent có công cụ** (định tuyến ⇒ trò chuyện / trợ lý Huế: tìm kho, hỏi lại, lịch trình, tra web khi kho không có; nhớ trong cuộc trò chuyện); 8 bậc, chưa code; Phase 1–8 = "RAG mức 1" |
| Cách làm việc của các agent (luật, skill, hook) | 31/10 chiều áp khung AI FDE: hook giờ ước, xét lại luật đang thử (40 ⇒ 7), skill D + 2 skill agent — xem nhật ký 31/10 chiều |
| Câu hỏi gõ không dấu | Chưa thực hiện — **ngoài phạm vi** (bạn quyết 15:15 25/10: người dùng gõ có dấu). Đã đo: tìm kiếm gần như hỏng (13/32 → 1/32 câu) |

Thang 5 mức: Đã xử lý, đóng gói · Đã xử lý · Xử lý một phần · Đã thử, chưa áp dụng · Chưa thực hiện.

## Luật cập nhật (cho agent)

Mỗi thay đổi vào hệ thống đang chạy ⇒ sửa `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_<KHÂU>.md` của đúng
khâu (cả Tóm tắt), `nhat_ky/` của đợt, `session_prompt/Project_Status.md`, rồi bảng trên. Mẫu:
`session_prompt/TEMPLATE_USER_REPORT.md`, `session_prompt/TEMPLATE_NHAT_KY.md`; quy tắc
`session_prompt/WORKFLOW.md` §6. Giờ lấy bằng `date`.
