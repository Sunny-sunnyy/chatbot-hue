# Implementation Report: Phase <id> <name>

Người làm: <A|B|C> (<agent>)
Date:
Canonical guide:

```text
guides/phase_<id>_<short_name>.md
```

## 1. Phạm vi

Nêu ngắn gọn phần đã được duyệt và phần thực sự được thực hiện.

## 2. Thay đổi chính

Liệt kê các thay đổi giúp người kiểm hiểu luồng mới. Chỉ nêu file quan trọng và
mục đích; không chép toàn bộ `git diff --name-only`.

## 3. Cách đã chạy thật

Ghi exact commands hoặc notebook đã chạy cùng real data, database, model,
provider và profile liên quan.

Không ghi expected command nếu chưa chạy. Không expose secrets.

## 4. Kết quả quan sát

Ghi kết quả mới từ exact run:

- hành vi quan sát;
- số liệu có ý nghĩa;
- output/result path nếu có;
- failed, skipped hoặc partial outcome.

Không dùng fake/mock/stub hoặc replay làm PASS. Evidence reuse hợp lệ trong cùng
series phải ghi nguồn, phần không đổi và lý do theo coordination skill; không
gọi là fresh run. Docs-only ghi exact kiểm tra tài liệu đã thực hiện.

## 5. Lỗi và giới hạn

Nêu lỗi còn lại, phần chưa chạy và ảnh hưởng thực tế. Nếu không có, ghi
`Không có lỗi hoặc giới hạn đã biết trong phạm vi này.`

Chỉ ghi security hoặc data-safety detail khi task có rủi ro hay hành động liên
quan.

## 6. Bàn giao cho người kiểm

Nêu:

- người kiểm nên đọc gì trước;
- real path cần chạy lại;
- notebook nếu thuộc acceptance; user chỉ bắt buộc kiểm tra khi acceptance yêu cầu;
- deviation đã được user duyệt nếu có.

Người làm không tự sửa guide, review, user report hoặc `Project_Status.md`
(thuộc A). Không commit/push trừ khi việc ghi rõ. Xong thì cập nhật trạng thái mục
việc của mình trong `CURRENT_HANDOFF.md`, `sessions/STATUS_<X>.md` và nhắn A
(`WORKFLOW.md` §4).
