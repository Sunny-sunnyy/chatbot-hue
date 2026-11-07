# Kịch bản demo 5 phút — buổi bảo vệ (NHÁP, E, 13:00 07/11/2026)

Việc A giao (B7). **Nháp để bạn đọc và sửa.** Chưa chạy thử câu nào trên hệ thống: mọi câu mẫu là **[chưa thử]**, phải tập trên bản cuối (bản deploy) trước buổi bảo vệ. Câu mẫu tự viết mới, ngắn, không lấy từ Golden / câu kín / bộ đo. Số chứng minh lấy từ `e_tb_bang_bang_chung.md`; đối chiếu lại trước khi in lên slide.

**Giả định:** giao diện cổng đợt 1 đã merge; cờ như hiện nay (tra web bật, thời tiết bật khi merge, biểu mẫu chỉ có nếu Q-F đạt, ảnh / giọng nói tắt).
**Chuẩn bị:**
- trình duyệt mở sẵn trang chủ, cửa sổ ẩn danh (cookie sạch);
- tab thứ hai mở video dự phòng;
- trước giờ trình bày gửi 1 câu "làm nóng", để lần gọi đầu không chậm do khởi động.

## Kịch bản (≈ 5 phút)

| # | Thời gian | Thao tác | Câu gõ mẫu [chưa thử] | Muốn hội đồng thấy | Số chứng minh (nói 1 câu) | Lỗi / chậm thì |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:30 | Mở trang chủ, chỉ ô hỏi, 5 chủ đề, dải "có thể sai"; ô thời tiết nếu bật | — | Đây là **ứng dụng trải nghiệm**, không chỉ là ô chat; cái gì cũng ghi rõ nguồn | Kho 204 bài / 5 lĩnh vực; 8.435 đoạn | Ô thời tiết không hiện ⇒ bỏ qua (giao diện tự ẩn khi lỗi) |
| 2 | 0:30–1:15 | Khám phá → Di sản → mở một bài lăng → bấm "Hỏi trợ lý về điểm này" | (nút tự điền câu) | Đọc được **bài gốc** của kho; trợ lý trả lời từ bài đó | — | Danh sách không tải ⇒ "tải lại"; vẫn lỗi ⇒ sang bước 3 |
| 3 | 1:15–2:00 | Hỏi tiếp trong khung trợ lý; bấm một tên ở dòng "Nguồn" | "Ở đó có cần mua vé riêng không?" | **Nhớ ngữ cảnh** ("ở đó" = lăng vừa hỏi); dòng "Nguồn" bấm ra đoạn gốc, có "Đọc cả bài" | Nhớ tên 10 / 10 trên bộ kín; 0 / 489 lỗi trích dẫn | Trợ lý từ chối ⇒ nói "khi kho không đủ, hệ thống từ chối thay vì đoán — đây là chủ đích" ⇒ hỏi lại đủ tên |
| 4 | 2:00–2:40 | Gõ một câu ngoài phạm vi, rồi một câu khẩn cấp | "Giá vàng hôm nay bao nhiêu?" · "Tôi vừa bị giật túi xách ở Huế, phải làm gì?" | **Từ chối đúng** câu ngoài phạm vi; câu khẩn cấp ra **câu soạn sẵn** có 113 / 115 — model không tự viết lời khuyên | 0 câu ngoài kho bị trả lời; định tuyến khẩn cấp bắt 10 / 10 câu kín | Câu khẩn cấp ra câu trả lời thường ⇒ dừng, nói thật đó là lỗi định tuyến, chỉ số đo |
| 5 | 2:40–3:30 | Gõ một câu về Huế mà kho không có (cơ sở cụ thể) | "Quán cà phê nào ở Huế mở cửa xuyên đêm?" | Kho từ chối ⇒ mục riêng **"Từ web (chưa kiểm)"**, link do code dựng, tách khỏi câu trả lời kho | Mục web ~13–18 s, ≈ 0,0018 USD | **Chậm là bình thường** — nói trước "bước này chờ tra web khoảng 15 giây"; nói phần bước 6 trong lúc chờ |
| 6 | 3:30–4:20 | Lên kế hoạch: chọn 2 ngày · gia đình có trẻ em · di tích → Gửi → mở bản đồ một điểm | (biểu mẫu) | **Code xếp lịch** theo buổi từ kho, điểm không xếp được ghi lý do; model chỉ viết lời; "Sửa — điền lại biểu mẫu" | Q-F (số C đo, điền sau); kín câu tự do 3 / 5 ⇒ chọn biểu mẫu | Biểu mẫu tắt (Q-F trượt) ⇒ **bỏ bước này**, nói "lịch trình đã thử, chưa đạt luật ⇒ chưa bật" + số 3 / 5 |
| 7 | 4:20–5:00 | Trang Giới thiệu, rồi slide bảng bằng chứng | — | Giới hạn + dữ liệu người dùng (cookie 30 phút, không lưu chữ); **thử nhiều, giữ ít** | Rà 8.1: chỉ "10 đoạn" thắng (Đủ +0,26 dev, +0,82 câu kín); các phương án bỏ: Qwen3-8B, rerank, luật từ khoá khẩn cấp, hỏi lại bằng model, tính tiền, SigLIP 2 | — |

**Câu nói chung khi chậm:** "Mỗi câu gọi model qua mạng; đo trên máy thật, chữ đầu trung vị khoảng 2–3,5 giây, p95 có lúc vượt 5 giây — chúng tôi ghi lại, không giấu." Không hứa con số chưa đo trên bản deploy.

**Không demo** (đang tắt hoặc chưa có số): hỏi bằng ảnh, giọng nói, câu lịch trình gõ tự do, tính tiền chuyến đi.

## Dự phòng mất mạng / provider lỗi — cần chuẩn bị (chưa làm)

| # | Chuẩn bị | Ai | Ghi chú |
|---|---|---|---|
| 1 | **Video quay sẵn** đúng 7 bước trên bản deploy (màn 1440 + 1 đoạn điện thoại), có phụ đề thời gian chờ | User quay, agent viết danh sách cảnh | Quay lại khi giao diện đổi |
| 2 | **Bản chạy local** trên laptop trình bày: Docker (Qdrant + app, cùng `compose` deploy), `.env` riêng, khởi động trước 15 phút | B (theo `data/phase_12/deploy_nhap/`) | Vẫn cần mạng tới OpenAI ⇒ không thay được video khi mất mạng hẳn |
| 3 | **Ảnh chụp màn hình** từng bước, chèn vào slide dự phòng | agent (Playwright, như `chup_s2.py`) | Rẻ nhất |
| 4 | **Phát wifi riêng** (điện thoại 4G) + kiểm mạng phòng bảo vệ trước 1 ngày | User | Mạng trường có thể chặn cổng / proxy |
| 5 | **Khoá OpenAI riêng cho buổi demo**, hạn mức nhỏ; Serper còn credit | User | Tránh hết tiền / khoá bị thu giữa buổi |
| 6 | **Câu dự phòng** cho mỗi bước (câu thứ hai đã thử chạy tốt) | agent soạn, User duyệt | Khi câu chính bị từ chối |
| 7 | Tập 2 lần trọn 5 phút trên bản deploy; ghi lại câu nào chậm / lỗi | User + một session | Sửa kịch bản theo lượt tập |

## Việc cần trước khi chốt kịch bản

1. Chạy thử 7 câu mẫu trên bản cuối (≈ 0,005 USD), thay câu nào bị từ chối hoặc chậm bất thường.
2. Điền số Q-F của C vào bước 6, hoặc bỏ bước 6.
3. Bạn quyết thứ tự: demo trước rồi slide số, hay slide trước.
