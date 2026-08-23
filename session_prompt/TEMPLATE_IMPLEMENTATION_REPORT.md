# Implementation Report: Phase <id> <name>

Implementer:
Date:
Canonical guide:

```text
guides/phase_<id>_<short_name>.md
```

## 1. Phạm vi

Nêu ngắn gọn phần đã được duyệt và phần thực sự được thực hiện.

## 2. Thay đổi chính

Liệt kê các thay đổi giúp Reviewer hiểu luồng mới. Chỉ nêu file quan trọng và
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

Không dùng fake/mock, replay hoặc kết quả cũ làm bằng chứng.

## 5. Lỗi và giới hạn

Nêu lỗi còn lại, phần chưa chạy và ảnh hưởng thực tế. Nếu không có, ghi
`Không có lỗi hoặc giới hạn đã biết trong phạm vi này.`

Chỉ ghi security hoặc data-safety detail khi task có rủi ro hay hành động liên
quan.

## 6. Handoff cho Reviewer

Nêu:

- Reviewer nên đọc gì trước;
- real path cần chạy lại;
- notebook người dùng sẽ chạy;
- deviation đã được user duyệt nếu có.

Implementer không sửa guide, Codex review, user report hoặc
`Project_Status.md`; không commit/push.
