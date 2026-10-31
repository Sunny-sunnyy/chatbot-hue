# Nhật ký 31/10/2026 — spec streaming, tra web bằng Codex

**Cập nhật lần cuối: 12:42 31/10/2026.** Tiền paid trong ngày: 0 USD. Codex / AGY chạy bằng gói tài khoản của bạn, không tính thêm tiền.

## Tóm tắt
- **Chatbot không đổi trong ngày.** Mọi việc hôm nay là thiết kế và cách làm, chưa động vào code chatbot.
- **Streaming** (chữ trả lời hiện dần): bạn đã chốt 3 câu.
  - D1: chữ hiện ngay, kiểm citation ở cuối.
  - D2: đo tốc độ tới lúc **chữ đầu tiên** hiện trên trình duyệt.
  - D3: gặp lỗi thì **xóa hết** phần đã hiện, báo lỗi và cho "Thử lại".
- Spec streaming đã viết xong, qua 2 vòng Claude review và 1 lần Codex review. Còn **một con số** cần bạn chọn (mục tiêu "chữ đầu tiên"), rồi bạn duyệt spec.
- **Tra web:** từ hôm nay các session tự gọi Codex qua một script để tra web. Bạn không phải chép tay sang ChatGPT cho câu tra nhanh nữa. Nghiên cứu lớn thì vẫn dùng cả ChatGPT web.
- **AGY:** điều khoản Google **cấm** Claude gọi AGY. Đã chặn bằng máy, bạn tự dùng AGY thì vẫn được.

## Bạn cần làm gì (phiên sau)
- Chọn **mục tiêu "chữ đầu tiên"**.
  - A khuyên: giữ mức bắt buộc 3 s / 5 s như D2, thêm mục tiêu 1,5 s / 3 s để báo cáo cạnh.
  - Cách khác: đổi mức bắt buộc ngay thành 1,5 s / 3 s. Có thể trượt, vì model còn suy nghĩ trước khi viết chữ đầu tiên.
- Duyệt spec streaming. A sẽ đưa mã sha của bản cuối.
- Trả lời quyền phiên.
- Duyệt 3 đề xuất trong sổ cải tiến, vòng 11 (A trình).
- Không gấp: file `báo cáo nghiên cứu github.txt` ở gốc repo, và 4 worktree cũ của AGY: giữ hay gỡ?

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Kiểm nghiên cứu streaming của ChatGPT | 21/22 link mở được, không ý nào bị nguồn nói ngược | Dùng được làm căn cứ cho spec |
| Spec streaming | Bản 4 `cf1ae9ef6c2c` đạt review; Codex tìm thêm 2 lỗi nhỏ, đã sửa | Chỉ còn 1 con số + bạn duyệt là bắt đầu code |
| Thử Codex / AGY tra web (3 bài × 2 công cụ) | Codex: tra nhanh dùng được, ngang ChatGPT ở 2/3 bài. AGY: kém rõ cả 3 bài (có link không tồn tại, link sai bài) | Codex thành cách tra web chính |
| Script `scripts/tra_web_codex.sh` | Tự ghi ngày hôm nay, đòi thông tin mới nhất, cảnh báo nếu Codex chạy lệnh shell, ghi lại trang Codex thật sự mở | Mọi session dùng chung một cách tra |
| Tra "mức chuẩn chữ đầu tiên" | Không có chuẩn ngành. Codex suy ra mục tiêu 1,5 s / 3 s | Là căn cứ cho câu hỏi ở trên |

## Giải thích ngắn (để bạn tự nói lại được)
**Streaming.** Hôm nay câu trả lời dài phải chờ trắng tới 7,6 giây. Với streaming, chữ hiện dần từ khoảng 1,9 giây sớm hơn. Bộ kiểm citation vẫn chạy ở cuối như hiện nay. Nếu kiểm hỏng hoặc luồng bị đứt giữa chừng thì xóa phần đã hiện, để không ai đọc nửa câu về điều kiện an toàn rồi làm theo. Giới hạn: bộ kiểm chỉ xem có số `[n]` hợp lệ, không xem câu chữ có đúng nguồn không. Vì vậy câu sai nghĩa vẫn hiện ra, như hôm nay.

**Tra web bằng Codex.** Claude không có công cụ tìm web. Codex có, và được phép gọi từ script. Codex tra nhanh (2–3 phút) và không bịa link. Nhưng ở bài sâu nhất, Codex kém ChatGPT rõ. Vì vậy câu nghiên cứu lớn vẫn chạy cả hai.

## Đọc thêm
- `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`, spec `docs/superpowers/specs/2026-10-31-streaming-design.md`
- `report_agent/2026-10-31_tra_web_codex/TONG_HOP.md`
