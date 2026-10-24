# Ngữ cảnh riêng của từng session

Mỗi session giữ một file `STATUS_<X>.md` (A, B, C…). Chính session đó ghi đè,
giữ ngắn (≤ ~60 dòng), cập nhật khi xong một việc và trước khi kết phiên. Session
mới mở với vai `<X>` đọc file này để nối tiếp. Việc được giao nằm ở
`CURRENT_HANDOFF.md`; lịch sử ở `PROJECT_HISTORY.md`; ở đây chỉ giữ ngữ cảnh làm
việc của riêng session.

Mẫu:

```markdown
# STATUS <X> — cập nhật <YYYY-MM-DD HH:MM>

Terminal: <tên trong ListAgents> · Agent: <Claude Opus 5.5 / Codex / …>

## Đang làm
- <việc, link mục trong CURRENT_HANDOFF>

## Đang khai báo sửa
- <đường dẫn> (hoặc "không")

## Vừa xong
- <việc — kết quả — report/commit>

## Đã học / bẫy gặp
- <điều session sau cần biết; bẫy chung thì báo A ghi vào Project_Status §8>

## Việc dở / câu hỏi cho A
- <…>
```
