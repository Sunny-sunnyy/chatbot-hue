# Báo cáo dành cho người dùng: Giai đoạn 1 - Nền tảng backend đơn giản

```text
Trạng thái: Đã được bạn xác nhận
Cập nhật lúc: 24-08-2026 16:56 +07
Notebook cần kiểm tra: Không áp dụng theo thiết kế đã duyệt
```

## 1. Bạn nhận được gì

Nền tảng backend đã gọn hơn mà vẫn giữ nguyên khả năng hiện có. Hệ thống dùng
một luồng trực tiếp để đọc cấu hình, và cấu hình logging chung nay thực sự được
bật khi API, ingestion CLI hoặc giao diện evaluation khởi động.

Notebook smoke và README cấu hình trùng lặp đã được xóa. Settings, ba retrieval
profiles, shared retrieval document và hành vi RAG downstream vẫn được giữ.

## 2. Hệ thống hoạt động như thế nào

```text
runtime entrypoint
-> bật logging chung
-> chạy API, ingestion hoặc evaluation như trước

settings.yaml
-> load_settings()
-> kiểm tra active profile
-> trả settings cho backend
```

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| API thật | `/health` trả `status=ok`; Qdrant/retrieval ready | Backend khởi động đầy đủ với database và local E5 thật |
| Evaluation UI | Chạy tại `127.0.0.1:7860` | Entrypoint Gradio và logging hoạt động |
| Test runs bổ sung | 74 affected và 222 full tests đều passed | Lịch sử quan sát; phạm vi này rộng hơn nhu cầu Phase 1 và không phải thước đo chất lượng |
| Active Qdrant | 572 points trước và sau tests | Collection đang dùng không bị thay đổi |
| Phase 7 CSV | Zero final diff | Kết quả evaluation đã lưu được giữ nguyên |

Một test evaluation hiện ghi lại retrieval CSV bằng kiểu xuống dòng CRLF.
Codex đã hoàn nguyên đúng thay đổi định dạng đó và xác nhận nội dung cuối cùng
không đổi. Đây là follow-up cho review Phase 7, không ảnh hưởng runtime Phase 1.

Bạn đã xác nhận Phase 1 dựa trên live settings, logging, API, Gradio và Qdrant
checks. Các test cũ sẽ được audit/xóa theo phase sở hữu; full suite không còn
là checkpoint mặc định.

## 4. Cách bạn chạy lại

Phase 1 không còn notebook vì notebook cũ chỉ lặp smoke checks. Nếu muốn kiểm
tra trực tiếp, từ `backend/` bạn có thể chạy:

```bash
uv run --env-file ../.env uvicorn api.app:app --host 127.0.0.1 --port 8011
```

Sau đó mở `http://127.0.0.1:8011/health`. Kết quả quan trọng là `status: ok`,
`qdrant: ready`, `retrieval: ready` và `generator: configured`. Lệnh này dùng
Qdrant và local embedding model thật, nhưng không tự gọi paid answer API.

## 5. Giới hạn và bước tiếp theo

- Môi trường review headless không thể tự mở browser cho Gradio, nhưng local UI
  đã phục vụ và trả HTTP 200.
- Full 104-question paid evaluation không chạy lại vì Phase 1 không thay đổi
  retrieval, context, prompt, model hoặc metric.
- Phase 1 đã được xác nhận. Tại thời điểm report, bước tiếp theo là simplicity
  review Phase 2; tiến độ hiện hành xem tại `session_prompt/Project_Status.md`.

Không còn bước xác nhận nào cho Phase 1. Commit/push vẫn cần yêu cầu riêng.
