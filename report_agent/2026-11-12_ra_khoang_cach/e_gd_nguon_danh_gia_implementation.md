# Khung nguồn hiện đoạn trích sạch + bỏ khối đánh giá dưới câu trả lời

E, 20:36 15/11/2026 (`date`). Hai lỗi / yêu cầu User nêu khi thử trang Trợ lý tối 15/11 (handoff "USER THỬ PHẦN 2" mục 2, 3). Nhánh `p9-gd-nguon-danh-gia` từ origin/main `e48d210`. Chỉ `frontend/`; server không đổi.

## Tóm tắt

| Việc | Trước | Sau |
|---|---|---|
| Đoạn trích trong khung nguồn | chữ thô của bài kho ⇒ lộ dấu in đậm, gạch đầu dòng, dấu tiêu đề, dấu kẻ bảng | dựng qua bộ Markdown + bộ lọc đang có (bản **không link** của mục web) ⇒ in đậm, gạch đầu dòng, bảng hiện đúng; không ký hiệu thô |
| Bảng trong khung nguồn | mỗi lát một dòng kẻ rời | các lát của cùng một bảng (lát tiêu đề + từng lát một hàng) ghép lại thành một bảng thật; hàng bảng mồ côi (không có dòng tiêu đề) ⇒ "ô · ô" |
| Dòng "Câu trả lời có hữu ích không?" + 2 nút | dưới mỗi câu trả lời và dưới lịch ở trang Lên kế hoạch | **gỡ khỏi giao diện** (cả hai nơi — cùng một thành phần); route `POST /api/feedback` + test phía server GIỮ |

Nút gợi ý dưới câu ngoài phạm vi giữ nguyên. Trang Giới thiệu / Trang chủ không có câu nào nhắc tới đánh giá (đã tìm) ⇒ không sửa chữ.

## Thay đổi

- `frontend/src/markdown.js`: `renderExcerptHtml` (Markdown ⇒ HTML qua `WEB_SANITIZE_OPTIONS` — danh sách thẻ cho phép sẵn có, **không thẻ link, không thuộc tính chứa URL**; không thêm thư viện, CSP không đổi), `hangBangLe`, `gopLatBang` (hai hàm thuần).
- `frontend/src/SourceLine.jsx`: đoạn trích dựng bằng hàm trên (dùng chung cho Trợ lý và thẻ lịch — nơi duy nhất hiện đoạn trích; bài Khám phá vốn đã dựng Markdown).
- `frontend/src/chat.jsx`, `LenKeHoach.jsx`: gỡ `Feedback`, biểu tượng ngón cái, câu báo lỗi gửi đánh giá. Thêm thuộc tính `data-phase` trên mỗi lượt và trên cột lịch.
- CSS: gỡ kiểu `.feedback`; thêm kiểu cho danh sách / bảng / tiêu đề bên trong khung trích (cỡ chữ bằng khung, bảng cuộn ngang trong khung).

**Chú ý cho người chạy script đo cũ:** nhiều script Playwright trong `data/` chờ lớp `.feedback` làm dấu "lượt đã xong" (đếm được 8 file, đều là script một lần) ⇒ chạy lại thì đổi sang `.turn[data-phase="done"]` (Trợ lý) / `.lkh-lich[data-phase="done"]` (Lên kế hoạch).

## Kiểm [đã chạy]

| Bước | Kết quả | Thời gian / tiền |
|---|---|---|
| Hàm thuần `hangBangLe` + `gopLatBang` (node, 11 ca: hàng lẻ, bảng thật giữ nguyên, mất dòng tiêu đề, chữ thường có dấu kẻ, lát văn không ghép…) | 11 / 11 | < 1 s, 0 USD |
| Playwright 1440 trên server tạm của nhánh: 5 câu thật (loại câu: món ở một chợ, giá vé, điểm tham quan, vé có bảng, chi phí có bảng), mở từng nguồn | 22 đoạn trích: **0 đoạn còn ký hiệu thô**; có in đậm, gạch đầu dòng, bảng thật; 0 link trong đoạn trích; link "Đọc cả bài" còn; 0 khối đánh giá; 0 lỗi console; 0 yêu cầu ra ngoài; không cuộn ngang | ~2 phút; 9 lượt = 0,0048 USD (theo `git_sha`) |
| `npm run build` | đạt (JS 128,5 KB gzip, giảm nhẹ) | < 1 s |
| `test_static_ui.py` | 4 passed | 9 s |
| Test server của `/api/feedback` | không chạy — code server không đổi | — |

Không có bộ chạy test JS trong repo ⇒ ca thử hàm thuần để ở `data/gd_nguon_danh_gia_2026-11-15/thu_hang_bang.mjs` (private, chạy bằng node), không thêm thư viện test chỉ vì hai hàm. Script + ảnh: cùng thư mục (`pw_nguon.py`, `anh/`, `anh_bang/`, `anh_cuoi/`). Ảnh cho User: `anh_cuoi/luot_1.png` (câu trả lời không còn dòng đánh giá + khung nguồn sạch), `anh_cuoi/nguon_bang_0.png` (khung nguồn có bảng).

## Giới hạn

- Xuống dòng đơn trong đoạn trích nay được nối lại như trang bài ở Khám phá (trước: giữ ngắt dòng 80 cột của file). Đoạn trích nào cố ý mỗi dòng một ý mà không phải danh sách sẽ thành một đoạn liền — chưa gặp trong 22 đoạn đã xem.
- Lát bảng chỉ ghép khi đứng liền nhau trong cùng một nguồn; hai lát hàng của hai bảng khác nhau mà cùng số cột, đứng liền, sẽ bị ghép thành một bảng (chưa gặp).
- Mới chụp khổ 1440; bảng rộng ở khổ hẹp cuộn ngang trong khung (kiểu CSS), chưa chụp 390.
