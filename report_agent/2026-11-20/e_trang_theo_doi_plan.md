# Plan một trang — mục [6] "trang theo dõi" cho chủ dự án (E viết 16:24 20/11/2026, giờ `date`; chờ phiên điều phối duyệt; chưa viết code)

**Từ dùng:** *dòng số đo* = mỗi lượt hỏi, hệ thống ghi MỘT dòng `chat_metrics` vào `backend/logs/application.log` gồm số đếm, mã kết cục, thời gian, tiền — không có chữ câu hỏi / câu trả lời (test đang khoá đúng tập trường này) · *xoay vòng* = file log đầy 10 MB thì đổi tên thành `.1`, `.2`, `.3`, bản cũ nhất bị xoá · *khoá quản trị* = một chuỗi bí mật đặt bằng biến môi trường lúc bật server.

**1. Điều đã chốt và hiện trạng.** Gốc: `bao_cao_he_thong/93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md` dòng 78 "Trang theo dõi: số câu, tuyến, tiền, độ trễ, 👍/👎 (từ log có sẵn)"; khối 👍/👎 chủ dự án đã bỏ 15/11 ⇒ không làm. Hôm nay muốn xem các số này phải chạy `scripts/dem_chat_metrics.py` ở cửa sổ lệnh. E đã đọc log thật (chỉ đếm): 4.375 dòng số đo từ 27/10 tới 20/11 (22 ngày), 55 trường; file 6,7 MB, chưa xoay vòng lần nào.

**2. Phản biện trước khi làm (phiên điều phối quyết).**
- Ở máy local, log TRỘN lượt thật với lượt của các bộ test và của mọi bản code cũ (ví dụ 611 dòng "sinh câu trả lời lỗi", 496 "lỗi nội bộ" phần lớn là test cố ý gây lỗi) ⇒ trang đọc thẳng log sẽ cho số xấu giả. Trang chỉ thật sự có ích SAU deploy (máy chủ không chạy test). Đề nghị: vẫn làm bản nhỏ (đã nằm trong danh sách chủ dự án chọn), nhưng trang BỎ dòng của model giả mà test dùng (`model = "probe"`) và ghi rõ trên trang "ở máy phát triển số còn lẫn lượt thử của nhóm".
- "Chỉ mở ở máy local" KHÔNG an toàn sau deploy: nếu máy chủ đặt một proxy cùng máy trước ứng dụng thì mọi yêu cầu đều trông như từ chính máy đó ⇒ E đề nghị KHOÁ quản trị, không dựa vào địa chỉ máy.

**3. Người dùng (chủ dự án) thấy gì.** Trang `#/theo-doi`, KHÔNG có trong menu. Mở trang ⇒ một ô nhập khoá. Đúng khoá ⇒ bảng 14 ngày gần nhất, mỗi ngày một dòng: số lượt · trả lời từ kho · từ chối (kho không có) · ngoài phạm vi · có mục web · lượt lịch / sửa lịch · trúng bản lưu (cache) · lỗi · tiền USD · độ trễ p50 và p95 (giây), kèm thanh ngang CSS cho số lượt; dòng tổng; dòng chú thích nguồn số và giờ đọc log. Sai khoá / chưa đặt khoá ⇒ trang chỉ báo "không mở được".

**4. Cách làm** (không thêm gì vào log, không cơ sở dữ liệu, không thư viện mới, không model)
- Backend: `backend/api/theo_doi.py` (mới) — hàm thuần `tong_hop(dong_log, so_ngay)` đọc các dòng `chat_metrics`, gom theo ngày ghi ở đầu dòng log; và `GET /api/theo_doi`: đọc `application.log` + ba bản xoay vòng nếu có (bản cũ trước), dòng bị cắt dở thì bỏ qua như script đếm đang làm; kết quả giữ 60 giây trong RAM.
- Ai xem được: chỉ khi server được bật với biến môi trường `HUE_KHOA_THEO_DOI` dài ≥ 16 ký tự VÀ yêu cầu mang đúng khoá ở header `X-Khoa-Theo-Doi` (so bằng phép so chống dò thời gian); thiếu biến ⇒ đường này trả 404 như không tồn tại (mặc định TẮT — cùng kiểu các chốt deploy `HUE_LUOT_MOI_NGAY`, `HUE_TAT_DOCS`). Khoá không nằm trong URL (URL hay bị ghi vào log proxy), trình duyệt chỉ giữ trong bộ nhớ trang (không lưu xuống máy), server không ghi khoá vào log.
- Frontend: `frontend/src/TheoDoi.jsx` (mới, tải riêng) + một dòng `route.js`, một dòng `App.jsx`. Ước: backend ~70 dòng + test ~50 · frontend ~90 dòng + ~10 dòng CSS.

**5. Rà rủi ro lộ dữ liệu** (theo skill `agent-security-review` mục 4, 5; mức theo skill review)
| Rủi ro | Hiện trạng | Mức | Cách xử lý trong bản này |
|---|---|---|---|
| Lộ chữ câu hỏi / câu trả lời của người dùng | Dòng số đo KHÔNG có chữ (`backend/api/routes/chat.py` `METRIC_FIELDS`, có test khoá) | — | Trang chỉ nhận số đã gom theo ngày; test mới khẳng định phản hồi chỉ có các khoá số đã liệt kê |
| Lộ dấu vết từng người (mã lượt `turn_id`, IP) | Log có `turn_id` ngẫu nhiên; không có IP | minor | Không đưa `turn_id` hay bất kỳ dòng riêng lẻ nào ra trang — chỉ tổng theo ngày |
| Người lạ xem tiền + lưu lượng | Chưa có đường nào | major nếu mở công khai | Khoá quản trị + mặc định tắt + không có trong menu |
| Dò khoá | Chưa có giới hạn số lần thử cho đường này | minor | Khoá ≥ 16 ký tự ngẫu nhiên; ghi giới hạn; không thêm bộ đếm thử sai ở bản này |
| Khoá lọt vào log / git | — | major | Khoá chỉ ở biến môi trường + header; test tìm chuỗi khoá trong log sau một lượt gọi |

**6. Xong khi (ghi trước)**
- a. Hàm `tong_hop` trên một file log mẫu dựng trong test (gồm dòng test giả, dòng bị cắt, hai ngày, một lượt trúng cache, một lượt lỗi) ra đúng từng ô; test đỏ trước xanh sau.
- b. Trên log THẬT của máy này: số lượt / tiền / số trúng cache của ngày 20/11 trên trang = kết quả một lệnh đếm tay trên cùng file (lệnh ghi trong report, dạng `grep 'chat_metrics' … | python3 -c …`), lệch 0.
- c. Không khoá / sai khoá / chưa đặt biến ⇒ 404 hoặc 403, phản hồi không có số nào; sau một lượt gọi đúng khoá, `grep` chuỗi khoá trong log ra 0 dòng.
- d. Một lượt trên trình duyệt (rộng 1440 và 390): nhập khoá ⇒ thấy bảng; không tràn ngang; trang khác không tải file của trang này. E mở ảnh ra nhìn.

**7. Giới hạn biết trước.** Chỉ còn số của tối đa ~40 MB log gần nhất (xoay vòng xoá bản cũ) ⇒ sau này lưu lượng lớn thì trang không còn đủ 14 ngày. Ngày tính theo giờ của máy chủ ghi log. Ở máy phát triển số lẫn lượt thử của nhóm (chỉ bỏ được dòng model giả). Không biểu đồ, không theo dõi theo giờ, không cảnh báo tự động.
