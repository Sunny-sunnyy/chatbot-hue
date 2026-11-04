# Nhật ký 04/11/2026 — Phase 9: câu khẩn cấp mới, hai thí nghiệm tốc độ, B4 gần xong, nghiên cứu 8 repo + TRIPO

**Cập nhật lần cuối: 21:34 04/11/2026 (kết phiên).** Tiền paid trong ngày: ≈ 0,226 USD (~5.650 đồng) — B4 ≈ 0,108 · tốc độ #1 0,057 + #6 0,059 · cổng A ≈ 0,001. Tiền Phase 9 ≈ 1,20 / 2,0 USD.

## Tóm tắt
- Phiên 19:34–21:50. Bạn cấp quyền như 03/11 và giao: "tiếp tục điều phối, phát triển, triển khai, tự nghiên cứu, so sánh, đánh giá, viết báo cáo".
- **Vào chatbot:** câu khẩn cấp soạn sẵn đổi dòng mở (bạn chọn PA1) — phủ cả người **vừa** gặp chuyện (bị cướp, tai nạn…).
- **Tốc độ:** thí nghiệm #1 (tắt suy luận khi định tuyến) **âm** — 2 câu an toàn bị xếp nhầm ⇒ bỏ. Thí nghiệm #6 (viết câu trả lời song song với định tuyến) **đạt** — chữ đầu câu về Huế nhanh hơn trung vị 1,37 s, an toàn giữ nguyên; chưa merge (phiên sau: report ⇒ review ⇒ merge). Vẫn chưa về sàn 3 / 5 s hôm provider chậm.
- **B4 (hỏi lại khi câu thiếu thông tin):** khoá 1 lộ lỗi cài đặt (câu dặn "không tự tính tổng" đặt sai chỗ), khoá 2 còn 1 / 5 câu chi phí nhân giá theo số người ⇒ bạn chọn sửa chữ thêm một vòng ⇒ **khoá 3 đạt mọi phần đã thấy**. Còn phần câu kín + vài bước đo ⇒ merge.
- **Nghiên cứu (bạn giao):** đọc **code** 8 repo + 1 paper bạn gửi, đọc lại github.txt, thử Huế TRIPO vòng 3, tra web về agent ⇒ 18 ý đưa vào kế hoạch; bạn chọn thêm bậc **"sửa lịch nhiều lượt"** sau B5 và cột "tên khác" cho bảng điểm.
- Plan B5 (lịch trình) bản 3 duyệt; bảng điểm bản 2 bạn duyệt. Vòng cải tiến 17 + 18 (4 luật nhỏ cho thử); 5 nhánh cũ được xoá / lưu tag.

## Bạn cần làm gì
- Phiên sau (đầu phiên): chạy lệnh `!` ở terminal C cho phần câu kín B4 (nếu tối nay chưa chạy) — C ghi lệnh trong `STATUS_C.md`; xác nhận cho 20 câu kín bộ tuyến (terminal B hoặc giao C).
- Duyệt bảng điểm B5 bản 3 (thêm cột tên khác) khi C soạn xong.
- Xoá nhánh `p9-chu-khan-cap` (đã merge) khi A đưa lệnh.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Câu khẩn cấp PA1 | vào chatbot `4e3cb4e`, review + cổng thật đạt | người vừa bị giật đồ thấy câu nói đúng hoàn cảnh |
| Tốc độ #1 | âm — phạm sàn an toàn | bỏ; code giữ bằng tag |
| Tốc độ #6 | **đạt** −1,37 s [0,34; 2,14] | chờ report + review + merge |
| B4 hỏi lại | khoá 3 đạt đã thấy (hỏi đúng 8 / 10, hỏi thừa 0 / 7, 0 câu nhân giá, an toàn 0 lỗi) | còn câu kín + Q5 / Q7 / Q8 |
| B5 lịch trình | plan bản 3 + bảng v2 duyệt | plan bản 4 thêm 9 ý từ nghiên cứu |
| Nghiên cứu tính năng | xong — báo cáo nghiên cứu bản 5 mục 000 | 18 ý có bậc / người làm |

## Giải thích ngắn (để bạn tự nói lại được)
Bước định tuyến (chọn loại câu) tốn ~1,7 s trước khi chatbot bắt đầu viết. Tắt phần "suy nghĩ" của model ở bước này thì nhanh hơn chút nhưng xếp sai câu an toàn ⇒ bỏ. Cách thứ hai: bắt đầu viết câu trả lời **cùng lúc** với định tuyến, xếp ra loại khác thì bỏ phần đã viết — người dùng thấy chữ sớm hơn ~1,4 s, đổi lại tốn thêm chút tiền cho lượt bỏ. Ở B4, lỗi nằm ở chỗ đặt câu dặn trong code chứ không ở thiết kế; sửa xong vẫn còn model tự nhân giá ⇒ thêm một câu dặn rõ hơn, rồi kiểm lại bằng bộ câu kín chưa ai nhìn.

## Đọc thêm
- `BAO_CAO_SINH_CAU_TRA_LOI_API.md` (mục 04/11: câu khẩn cấp, tốc độ #1); `BAO_CAO_NGHIEN_CUU_PHASE_9.md` mục 000; `LUONG_HOAT_DONG_HE_THONG.md`.
- Hồ sơ agent: `report_agent/2026-11-02_phase_9_code/` (`b154_review.md`, `c156_toc_do_dinh_tuyen*.md`, `b144_b4_implementation.md`).
