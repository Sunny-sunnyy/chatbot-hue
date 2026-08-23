# Báo cáo dành cho người dùng: Giai đoạn <số> - <tên dễ hiểu>

```text
Trạng thái: Đang chờ bạn xác nhận
Cập nhật lúc: DD-MM-YYYY HH:MM +07
Notebook cần kiểm tra: notebooks/0<số>_<tên>.ipynb
```

Báo cáo phải đơn giản, rõ ràng, dễ đọc và dễ hiểu. Chỉ dùng kết quả Codex đã
chạy thật. Không chép technical report, mã trạng thái nội bộ, chi tiết audit,
mã băm, cost accounting hoặc nội dung gỡ lỗi không giúp user quyết định.

## 1. Bạn nhận được gì

Giải thích trong một hoặc hai đoạn:

- phase giải quyết vấn đề gì;
- kết quả user có thể dùng hoặc quan sát;
- một ví dụ cụ thể nếu cần.

## 2. Hệ thống hoạt động như thế nào

Mô tả data flow bằng từ thông thường. Chỉ giữ các bước user cần để hiểu; không
liệt kê toàn bộ kiến trúc hoặc module.

## 3. Codex đã chạy và quan sát gì

Chỉ ghi fresh observed results. Mỗi số liệu phải có ý nghĩa đi kèm.

Nếu có từ ba kiểm tra trở lên, dùng bảng:

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| <real check> | Đạt / Không đạt / Chưa chạy | <user hiểu được gì> |

Nói rõ failed, skipped hoặc partial outcome. Không dùng expected result,
mock/fake hoặc output cũ như bằng chứng.

## 4. Cách bạn chạy lại

Notebook là cách kiểm tra chính. Ghi:

- đường dẫn notebook;
- prerequisite cần thiết;
- cách Run All từ trên xuống;
- kết quả quan trọng cần nhìn thấy;
- kết quả đó chứng minh điều gì;
- notebook có dùng online hoặc paid API hay không.

Chỉ thêm command ngoài notebook khi thật sự cần. Không yêu cầu user paste
secret vào chat.

## 5. Giới hạn và bước tiếp theo

Nêu:

- điều chưa làm hoặc lỗi còn lại;
- ảnh hưởng thực tế;
- user cần xác nhận hay yêu cầu sửa như thế nào;
- phase tiếp theo có đang đóng hay không.

Khi chờ xác nhận, kết thúc bằng:

```text
Sau khi chạy notebook, bạn có thể phản hồi:
- Tôi xác nhận Giai đoạn <số>.
- Tôi muốn sửa: <nội dung cần sửa>.
```

Khi user xác nhận, Reviewer đổi trạng thái thành `Đã được bạn xác nhận`, cập
nhật guide và `Project_Status.md`. Commit/push vẫn cần yêu cầu riêng.
