# Báo cáo dành cho người dùng: Phase <id> <name>

## Trạng thái và xác nhận

```text
Phase status: awaiting_user_confirmation | approved
Technical review decision: ready_for_user_confirmation
User confirmation: pending | confirmed
Updated at +07: YYYY-MM-DD HH:MM
Report path: reports/user_reports/phase_<id>_<short_name>_user_report.md
Notebook: notebooks/0<phase>_<short_name>.ipynb
```

Khi tạo report lần đầu, dùng `awaiting_user_confirmation` và `pending`. Chỉ sau
khi user xác nhận mới đổi thành `approved` và `confirmed`.

## Phase này là gì

Giải thích phase bằng ngôn ngữ dễ hiểu trong một hoặc hai đoạn ngắn.

## Mục tiêu

Nêu kết quả người dùng nhận được, không chỉ liệt kê implementation tasks.

## Vấn đề phase này giải quyết

Giải thích vấn đề trước phase và vì sao cần giải quyết trước phase tiếp theo.

## Phase này đã xây được gì

Tóm tắt các deliverables đã được technical review xác minh.

## Chức năng đã có

Liệt kê behavior người dùng hoặc phase sau có thể sử dụng thực sự.

## Chức năng hoạt động như thế nào

Giải thích components và cách chúng phối hợp, tránh jargon không cần thiết.

## Luồng hoạt động

Mô tả input, các bước xử lý chính và output theo đúng implementation hiện tại.

## File quan trọng

Với mỗi file, ghi mục đích và khi nào người dùng cần đọc. Liên kết tới guide,
notebook và các entry point quan trọng; không sao chép toàn bộ technical report.

## Notebook xác nhận

Ghi canonical notebook path, safe-default behavior, prerequisites, thứ tự cells,
expected observations và những điểm người dùng cần xác nhận.

## Cách tự kiểm tra và chạy code

Chỉ ghi commands đã được xác minh. Python commands phải dùng:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ...
```

Nếu command cần model download, Qdrant mutation, live API hoặc chi phí, ghi rõ
approval gate trước command.

## Kết quả validation thực tế

Ghi command/check, trạng thái `passed`, `failed` hoặc `skipped`, kết quả quan
trọng và limitation. Không suy diễn pass từ report của agent khác.

## Kỹ thuật sử dụng

Giải thích ngắn gọn kỹ thuật chính và lý do dùng trong phase này.

## Giới hạn và vấn đề hiện tại

Ghi accepted limitations, known issues, failed/skipped checks và ảnh hưởng thực
tế. Không che giấu issue để phase trông hoàn thiện hơn.

## API, model và chi phí bên ngoài

Ghi actual provider/model/call scope/cost khi có. Nếu không dùng, ghi:

```text
Không áp dụng cho phase này.
```

Không ghi API key, raw header, private payload hoặc chain-of-thought.

## Bước tiếp theo

Nêu phase/action hợp lệ tiếp theo và hard gate còn lại. Khi report còn `pending`,
phase tiếp theo chưa được mở.

## Checklist xác nhận của người dùng

- [ ] Tôi đã đọc mục tiêu, chức năng và giới hạn của phase.
- [ ] Tôi đã mở/chạy notebook theo safe-default instructions.
- [ ] Kết quả quan sát phù hợp với expected observations trong report.
- [ ] Tôi hiểu các failed/skipped checks, external-call gates và known issues.
- [ ] Tôi xác nhận phase hoặc yêu cầu thay đổi cụ thể.

Khi user xác nhận, Codex cập nhật checklist/evidence phù hợp, `User confirmation`
thành `confirmed`, ghi thời gian UTC+7 và tiếp tục finalization theo
`REVIEWER_WORKFLOW.md`.
