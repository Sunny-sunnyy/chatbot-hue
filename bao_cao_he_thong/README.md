# Báo cáo hệ thống hue_rag — mục lục cho bạn

**Cập nhật lần cuối: 19:32 10/11/2026** — sửa mọi chỗ cũ / sai so với hiện trạng 10/11 ở mục lục và 10 báo cáo khâu (bạn yêu cầu báo cáo luôn đúng); các bản trước: xem lịch sử git. Bạn chỉ cần đọc thư mục này. Báo cáo kỹ thuật của agent ở
`report_agent/`; report cũ tới 24/10 ở `reports/` (lịch sử).

## Muốn biết gì ⇒ đọc file nào

| Muốn biết | File | Cập nhật lần cuối |
|---|---|---|
| Chatbot đang chạy thế nào (toàn cảnh) | [LUONG_HOAT_DONG_HE_THONG.md](LUONG_HOAT_DONG_HE_THONG.md) | 19:32 10/11/2026 (bản 34: sửa chỗ cũ — số tốc độ 09/11, hỏi bằng ảnh, 4 chốt deploy) |
| **Nghiên cứu rộng trước Phase 9** (thực tế triển khai, người dùng cần gì, paper, repo; Huế TRIPO) | [BAO_CAO_NGHIEN_CUU_PHASE_9.md](BAO_CAO_NGHIEN_CUU_PHASE_9.md) | 21:05 04/11/2026 (bản 5: đọc code 8 repo + paper, TRIPO vòng 3, agent ⇒ tính năng theo bậc) · 18:40 03/11/2026 (bản 4: sản phẩm thật — 15 trợ lý thế giới + Huế TRIPO vòng 2 ⇒ tính năng đáng học theo bậc) · 14:55 02/11/2026 (bản 3: đổi hướng agent có công cụ — khoá AI FDE, ChatGPT, Serper, SDK; spec duyệt) · 16:13 01/11/2026 (bản 2: ChatGPT đã kiểm, thử Huế TRIPO 10 câu, hướng Phase 9 bạn chọn, lịch đến bảo vệ) · 15:25 01/11/2026 (bản 1 sơ bộ) |
| **Đề xuất mở rộng + lộ trình Phase 9–12** (agent nhìn thấy được, tính tiền bằng code, ảnh, giọng nói, trải nghiệm Huế, lưu trú, vận hành / AWS) — bậc 1 bạn duyệt; ý khác là backlog | [DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md](DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md) | 10:24 05/11/2026 (bản 2: chia Phase 10–12, nghiên cứu ảnh + lưu trú, backlog) · 09:27 05/11/2026 (bản 1: brainstorm 21 ý + nghiên cứu Codex 3 mạch, A kiểm 8 nguồn) |
| **So sánh mọi phương án đã thử / chọn / bỏ** (Phase 0 → 8.2, sửa kho, Qwen3-8B) — theo khâu + theo Phase | [BAO_CAO_SO_SANH_PHUONG_AN.md](BAO_CAO_SO_SANH_PHUONG_AN.md) | 14:33 01/11/2026 (bản 5: B0 — E7, S2, §6) · 11:29 01/11/2026 (bản 3: mới; 62 khối, có số đo + nhãn độ tin; 2 lượt kiểm độc lập đạt; phần streaming / đo cuối thêm sau) |
| Chất lượng hiện tại, điểm mốc, chỗ yếu, thước đo (7B, 8.1, 8.2, đợt sửa kho 1–2) | [BAO_CAO_DANH_GIA.md](BAO_CAO_DANH_GIA.md) | 19:32 10/11/2026 (bản 7: nói rõ chatbot Phase 9 chưa đo lại cả bộ 176 câu (đo ở B7); số tốc độ 09/11) |
| Nền tảng dự án (Phase 0–1) | [BAO_CAO_NEN_TANG.md](BAO_CAO_NEN_TANG.md) | 19:32 10/11/2026 (bản 6: 6 nhóm cấu hình, log xoay vòng) |
| Chia tài liệu thành đoạn (Phase 2) | [BAO_CAO_CHIA_DOAN.md](BAO_CAO_CHIA_DOAN.md) | 19:32 10/11/2026 (bản 7: số đoạn 8.435) |
| Vector nghĩa + từ khóa (Phase 3) | [BAO_CAO_EMBEDDING_TU_KHOA.md](BAO_CAO_EMBEDDING_TU_KHOA.md) | 19:32 10/11/2026 (bản 6: trợ lý tìm thêm ≤ 2 lần) |
| Lưu vào Qdrant (Phase 4) | [BAO_CAO_LUU_TRU_QDRANT.md](BAO_CAO_LUU_TRU_QDRANT.md) | 19:32 10/11/2026 (bản 5: 2 collection (thêm collection thử ảnh), build lại 05/11) |
| Tìm đoạn liên quan (Phase 5) | [BAO_CAO_TIM_KIEM.md](BAO_CAO_TIM_KIEM.md) | 19:32 10/11/2026 (bản 12: thêm bước định tuyến + tìm thêm) |
| Sinh câu trả lời, API, giao diện (Phase 6) | [BAO_CAO_SINH_CAU_TRA_LOI_API.md](BAO_CAO_SINH_CAU_TRA_LOI_API.md) | 19:32 10/11/2026 (bản 47: sửa chỗ cũ — cổng du lịch, từ chối nhầm 4–6 / 158, số 09/11) |
| Bộ câu hỏi chuẩn Golden (Phase 7, 7A) | [BAO_CAO_BO_CAU_HOI_GOLDEN.md](BAO_CAO_BO_CAU_HOI_GOLDEN.md) | 09:40 08/11/2026 (bản 9: sửa chỗ ghi sai — bộ kín mới 40 câu đã dùng 01/11, cần bộ mới nữa) · 11:04 01/11/2026 (bản 8: 1 câu keyword lệch kho chỉ ở hoa / thường — chấm không sai; **bạn giữ nguyên**) |
| **Hỏi bằng ảnh (Phase 10)** — **bật từ 08/11** (10:31 08/11/2026); luna gợi tên + bạn xác nhận; SigLIP 2 thử âm | [BAO_CAO_HOI_BANG_ANH.md](BAO_CAO_HOI_BANG_ANH.md) | 19:32 10/11/2026 (bản 4: đã bật 08/11 — bỏ chỗ ghi "cờ tắt") |
| Sửa kho dữ liệu, tạo lại chỉ mục (Phase 7A2 → đợt 1 28/10 → đợt 2 **đã áp** 30/10) | [BAO_CAO_KHO_DU_LIEU.md](BAO_CAO_KHO_DU_LIEU.md) | 19:32 10/11/2026 (bản 10: 2 collection, giờ mở cửa 11 điểm) |
| Rà code: nên sửa gì (bạn duyệt 5 gói 25/10 — **đã sửa xong cả 5**, 26/10) | [DE_XUAT_SUA_CODE.md](DE_XUAT_SUA_CODE.md) | 17:11 31/10/2026 (bản 3: viết lại thành "5 gói đã xong", kèm commit) |
| Chuyện từng ngày | [nhat_ky/](nhat_ky/) — mới nhất: [10/11 — tăng tốc câu xã giao và câu hỏi ngày (đang làm)](nhat_ky/2026-11-10_toc_do_xa_giao_cau_ngay.md) | 19:16 10/11/2026 |

## Trạng thái ngắn

| Phần | Trạng thái |
|---|---|
| Chatbot full-corpus (204 file, 8.435 đoạn từ 05/11 tối sau đợt giờ mở cửa; e5-small + BM25, gpt-6-luna, 10 đoạn ngữ cảnh) | Đã xử lý, đóng gói |
| Thước đo + điểm mốc 176 câu | Đã xử lý, đóng gói; mốc người B0 (01/11) chỉ tham khảo — xem dòng Phase 8.2 |
| Từ chối nhầm, bảng giá khó tìm, đoạn vụn | Xử lý một phần: từ chối nhầm 22 / 158 câu (8.1, 5 đoạn) ⇒ 12 / 158 (30/10, 10 đoạn + kho sửa đợt 2) ⇒ **4–6 / 158** (03/11, trợ lý được tìm thêm ≤ 2 lần); bảng giá khó tìm, đoạn vụn chưa xử lý |
| Model vector Qwen3-8B thay e5-small | **Đã thử, chưa áp dụng** (30/10): kém hơn — 3 / 40 câu thử mất đoạn đúng, bước tìm theo nghĩa chậm 0,02 ⇒ 2,2 s; chỉ mục thử đã xóa |
| Dọn code + 2 kho món ăn cũ | Đã xử lý, đóng gói (bạn đóng 20:01) |
| Rà 56 quyết định Phase 0–7 (Phase 8.1) | Đã xử lý, đóng gói (bạn đóng 15:27 25/10): **chỉ "10 đoạn thay vì 5" thắng** → đã áp dụng 28/10 (Phase 8.2) |
| Phase 8.2 (áp dụng phương án thắng) | **Đã xử lý, đóng gói** (bạn đóng 10:23 28/10): **10 đoạn + NFC** vào chatbot (`510e1a8`); phép kiểm cuối 36 câu kín: đủ ý +0,82, đúng +0,70, 0 câu kém đi, câu ngoài kho vẫn từ chối 3 / 3; tốc độ khi đó chưa đạt (01/11 có streaming: đạt). B0 (01/11): bạn đọc 20 cặp mù 5 ↔ 10 đoạn — phần lớn như nhau; 3 cặp bản 5 đoạn từ chối nhầm, bản 10 trả lời được; luật dừng "chưa rõ" (0 cặp quyết) ⇒ bạn chọn giữ 10. Mốc người tham khảo (kho cũ, không chọn bên theo cặp). |
| Phase 8 (đóng gói Phase 1–8: streaming, giá đủ, lượt đo cuối, B0) | **Đã xử lý, đóng gói** — Phase 8 bạn đóng 14:29 01/11/2026; lượt đo cuối mọi sàn đạt |
| Rà code các Phase trước | **Đã xử lý, đóng gói** — 5 gói sửa xong 26/10 (1a, 1b, 3, 4 ngày 25/10; đợt 3 = gói 2 + 5 ngày 26/10); mỗi gói review chéo + cổng ổn định; code backend 8.345 → 6.218 dòng |
| Câu hỏi theo ngày, ngày âm lịch ("hôm nay", "rằm tháng Giêng là ngày nào") | **Đã xử lý** — công cụ ngày + âm lịch **bật 09/11**: code tính ngày, model chỉ diễn đạt; đúng ngày trên bộ đo; **còn chậm** (chữ đầu trung vị 5,2 s, sàn 3 s; 0,00063 USD / câu, trần 0,0005) ⇒ 10/11 đang làm bản nhanh (code tính sẵn ngày) |
| Hiện chữ dần (streaming) | **Đã xử lý, đóng gói** 01/11 (merge `a80e12d`) — chữ đầu trên trình duyệt 1,23 / 2,61 s (trước định tuyến); trên cổng mới 07/11 trung vị 2,03 s (10 câu, một lần) |
| Phase 9 (trợ lý có công cụ) | **Đang làm** (tiền đã dùng ≈ 3,6 / trần 4,2 USD). **Đang chạy:** phân loại câu hỏi 4 tuyến (trò chuyện / về Huế / ngoài phạm vi / khẩn cấp — từ 09/11 câu khẩn cấp đi thẳng trợ lý Huế, **bỏ câu soạn sẵn**), tìm thêm ≤ 2 lần, nhớ câu hỏi 3 lượt, 👍 / 👎, chạy song song câu về Huế, tra web khi kho không có ("Từ web, chưa kiểm"), thời tiết, ngày + âm lịch, cổng du lịch (trang chủ, Khám phá 204 bài), biểu mẫu "Lên kế hoạch", hỏi bằng ảnh, 4 chốt trước deploy (giới hạn lượt / ngày…, bật bằng biến môi trường). **Có code, cờ tắt:** lịch trình câu gõ tự do, bản đồ lịch trình (chờ phiếu toạ độ). **Thử rồi không áp dụng (09/11):** cổng 2 nhóm, web thành công cụ, bảng vé + giờ, lịch trình câu gõ. **Tốc độ (đo chung 09/11):** câu Huế chữ đầu 2,16 / 4,32 s ✓; xã giao chậm nhất 7,7 s ✗; câu ngày 5,2 s ✗ — 10/11 đang sửa. Còn: B7 so sánh cuối với RAG 1–8 |
| Hỏi bằng ảnh (Phase 10) | **Đã xử lý, đang chạy** (bật 08/11): bạn chụp ảnh ⇒ model gợi ≤ 3 tên trong danh sách 42 điểm / món ⇒ bạn bấm xác nhận ⇒ mới trả lời; ảnh thu nhỏ gửi OpenAI. Đúng trong 3 gợi ý 22 / 25 ảnh |
| Giọng nói (Phase 10), bản đồ lịch trình | Chưa thực hiện xong — giọng nói chờ bạn thu 40 câu; bản đồ có code, chờ bạn tick phiếu toạ độ |
| Deploy AWS (Phase 12) | Chưa thực hiện — 4 chốt an toàn đã có code (09/11); deploy sau khi đóng tính năng |
| Cách làm việc của các agent (luật, skill, hook) | 31/10 chiều áp khung AI FDE: hook giờ ước, xét lại luật đang thử (40 ⇒ 7), skill D + 2 skill agent — xem nhật ký 31/10 chiều |
| Câu hỏi gõ không dấu | Chưa thực hiện — **ngoài phạm vi** (bạn quyết 15:15 25/10: người dùng gõ có dấu). Đã đo: tìm kiếm gần như hỏng (13/32 → 1/32 câu) |

Thang 5 mức: Đã xử lý, đóng gói · Đã xử lý · Xử lý một phần · Đã thử, chưa áp dụng · Chưa thực hiện.

## Luật cập nhật (cho agent)

Mỗi thay đổi vào hệ thống đang chạy ⇒ sửa `LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_<KHÂU>.md` của đúng
khâu (cả Tóm tắt), `nhat_ky/` của đợt, `session_prompt/Project_Status.md`, rồi bảng trên. Mẫu:
`session_prompt/TEMPLATE_USER_REPORT.md`, `session_prompt/TEMPLATE_NHAT_KY.md`; quy tắc
`session_prompt/WORKFLOW.md` §6. Giờ lấy bằng `date`.
