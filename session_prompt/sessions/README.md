# Sổ riêng của từng session

Mỗi session giữ một file `STATUS_<X>.md` (A, B, C…). Chính session đó GHI ĐÈ cả file (không nối, không chồng khối mới lên khối cũ) khi xong một việc và
trước khi kết phiên; session mới mở với vai `<X>` đọc file này để nối tiếp. Việc được giao và bước kế nằm ở sổ việc `VIEC_DANG_MO.md` — ở đây chỉ trỏ tên
khối, không chép lại. Số đo để ở report, ở đây chỉ trỏ.

Khuôn bảy mục (`guides/CACH_LAM_VIEC.md` mục 5):

```markdown
# STATUS_<X> — ghi đè <giờ lấy bằng `date`>

1. Đang dở: <việc — khối nào của sổ việc — nhánh / mã commit>
2. Đã soạn / đã review, chưa gộp: <nhánh — chờ ai>
3. Việc kế + "xong khi": <trỏ khối của sổ việc>
4. Ai chờ mình ↔ mình chờ ai: <…>
5. Câu treo: <…>
6. Thứ đang chạy / rác: <đầu ra `git worktree list`, tiến trình, cổng, file tạm>
7. Bẫy của phiên: <điều phiên sau cần biết>
```
