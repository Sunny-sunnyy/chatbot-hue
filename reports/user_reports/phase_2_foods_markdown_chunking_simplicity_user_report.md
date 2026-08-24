# Báo cáo dành cho người dùng: Giai đoạn 2 - Chia tài liệu ẩm thực thành đoạn

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 24-08-2026 +07
Notebook cần kiểm tra: notebooks/02_foods_data_and_chunking.ipynb
```

## 1. Bạn nhận được gì

Phần đọc và chia tài liệu ẩm thực Huế đã gọn hơn nhưng giữ nguyên toàn bộ dữ
liệu đưa vào các bước tìm kiếm. Hệ thống vẫn tạo đúng 572 đoạn hiện hành từ 91
tệp, với cùng nội dung, thứ tự, nhãn và thông tin nguồn như trước refactor.

Hai module phụ chỉ chuyển dữ liệu qua lại đã được xóa. Notebook cũng chỉ gọi
một hàm công khai của backend, nên luồng học tập dễ theo dõi hơn.

## 2. Hệ thống hoạt động như thế nào

```text
curated Foods Markdown
-> đọc H1 làm tên tài liệu và H2 làm chủ đề
-> bỏ dòng chỉ chứa ảnh và mục Nguồn dữ liệu
-> chia phần nội dung dài tại ranh giới tự nhiên
-> thêm nhãn ngắn và thông tin nguồn
-> trả danh sách đoạn theo thứ tự ổn định
```

Bảng Markdown được giữ nguyên khối dù dài hơn 400 ký tự để không làm vỡ hàng
và cột. File thiếu tiêu đề hoặc không còn mục trả lời hợp lệ sẽ báo lỗi ngay.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| So sánh trước/sau | 572 đoạn khớp tuyệt đối, cùng SHA-256 | Refactor không đổi dữ liệu mà các phase sau nhận |
| Notebook 02 | Run All thành công; 91 files và ba ví dụ | Người học quan sát được paragraph, table và food guide thật |
| Focused Phase 2 | 15 tests đạt trước và sau full run | Các hành vi chia đoạn và lỗi quan trọng được giữ |
| Downstream smoke | 79 tests đạt | Ingestion, index, startup và chat không có regression quan sát được |
| Full backend | 206 tests đạt | Fresh evidence bổ sung theo kế hoạch Phase 2 |
| Active Qdrant | 572 points trước và sau | Collection đang dùng không bị thay đổi |

Full suite tạo lại một thay đổi định dạng xuống dòng trong retrieval CSV. Codex
đã xác nhận nội dung không đổi, hoàn nguyên side effect của reviewer run và kết
thúc với zero diff.

## 4. Cách bạn chạy lại

Mở `notebooks/02_foods_data_and_chunking.ipynb` từ repository root và chọn
**Run All** từ trên xuống.

Bạn cần quan sát:

- `tổng số đoạn: 572` và `số file được xử lý: 91`;
- bảy trường metadata gồm `chunk_id`, `source`, `title`, `section`, `category`,
  `subcategory`, `chunk_type`;
- một đoạn văn thường có nhãn ngữ cảnh;
- một bảng menu được render đủ hàng/cột và có thể dài hơn 400 ký tự;
- một ví dụ từ `food-guides.md`.

Những kết quả này chứng minh notebook gọi đúng chunker thật và giúp quan sát
output mà các phase sau sử dụng. Notebook không gọi web, Qdrant, model hoặc
paid API.

## 5. Giới hạn và bước tiếp theo

- Phase 7 evaluation không chạy lại vì 572 ordered chunks khớp tuyệt đối; không
  có thay đổi retrieval input hay RAG quality behavior.
- Còn hai chi tiết nhỏ không ảnh hưởng kết quả: một import không dùng và một
  lỗi chính tả trong dữ liệu test tổng hợp.
- Bạn đã xác nhận Phase 2 ngày 24-08-2026 +07.
- Bước tiếp theo là brainstorm simplicity review Phase 3.
- Commit/push vẫn cần yêu cầu riêng và chưa được thực hiện.
