# Sổ vết debug có nội dung — chỉ ở máy local

E, 20:49 15/11/2026 (`date`). User quyết tối 15/11 (handoff "USER QUYẾT 20:39 — log chi tiết"): khi thử thấy lỗi, `chat_metrics` không có nội dung nên nhóm phải đoán + tái tạo. Nhánh `p9-so-vet` từ origin/main `a0166c8`.

## Tóm tắt

- Cờ `assistant.so_vet` — **mặc định TẮT**; bật bằng biến môi trường **`HUE_SO_VET=true`** (cùng kiểu `HUE_TRA_WEB`: chỉ nhận `true` / `false`, giá trị khác ⇒ server không khởi động).
- Bật ⇒ mỗi lượt ghi **một dòng JSON** vào `data/debug_trace/<YYYY-MM-DD>.jsonl` (`data/` không vào git). Xem: `uv run python scripts/xem_so_vet.py [-n 3] [--ngay YYYY-MM-DD] [--ma <turn_id>] [--day]`.
- `chat_metrics` **không đổi** (vẫn không nội dung). Cờ tắt ⇒ không tạo thư mục / file. Ghi hỏng ⇒ một dòng cảnh báo chỉ có tên lớp lỗi, lượt trả lời không bị ảnh hưởng.
- **Checklist deploy:** bản Docker / công khai KHÔNG đặt `HUE_SO_VET` (chữ người dùng nằm trên đĩa); `data/debug_trace/` không vào ảnh Docker (danh sách chừa không có).

## Bản ghi có gì

| Phần | Nội dung | Lấy từ đâu |
|---|---|---|
| `so_do` | NGUYÊN dòng `chat_metrics` của lượt (kết quả, `turn_id`, `git_sha`, token, USD, ms) ⇒ nối với log cũ không cần mã mới | route |
| `cau_go`, `cau_gui_model`, `lich_su` | câu người dùng gõ; câu thật gửi model (lượt ghép / biểu mẫu khác câu gõ); các lượt lịch sử gửi model | route + vết lượt |
| `tuyen` | tuyến định tuyến chọn, lỗi định tuyến, câu tìm định tuyến viết (nếu có) | vết lượt |
| `tim_kho` | **từng lần tìm**: câu tìm, do code hay model, 10 kết quả đầu (mã đoạn, file, điểm), mã đoạn vào ngữ cảnh | MỚI: trường `vet` |
| `cau_tim_model`, `ngu_canh`, `cong_cu` | câu model viết khi gọi công cụ tìm; chữ ngữ cảnh từng lần; mục số đo từng công cụ | vết lượt (đã có) |
| `goi_model` | từng lần gọi model: loại lượt, token vào / ra / suy luận / đệm, USD, ms | vết lượt (đã có) |
| `tra_loi` | chữ trả lời, nguồn được trích (số, tên bài, file, đường mục), kết quả cố định, lỗi trích dẫn, hỏi lại | vết lượt |
| `web` | câu gửi dịch vụ tìm kiếm, sổ web (tiêu đề, link, đoạn trích), chữ model viết (cả khi bị rào thay câu cố định), mục đã hiện, rào nào chặn | MỚI: 3 dòng ở cổng web |
| `sua_lich` | hành động model hiểu, số bị rào chặn, lựa chọn thẻ, danh sách "Đã đổi / Chưa làm" | MỚI: 2 dòng ở bước hiểu ý sửa |
| `lich`, `thoi_tiet` | lượt biểu mẫu / lịch: trường, khung, các bước, mã kiểm; kết quả công cụ thời tiết | vết lượt |
| `loi` | `repr` của ngoại lệ (≤ 500 ký tự) | MỚI: 2 chỗ bắt lỗi ở route |
| lượt ảnh (`duong: "anh"`) | tên gợi ý, kết quả, lần gọi model — **không ghi ảnh** | route ảnh |

Không ghi: cookie, IP, khoá, nội dung `.env` (bản ghi chỉ dựng từ vết lượt + dòng số đo — hai thứ này vốn không chứa các mục đó; test dò chuỗi).

**Chưa có (không đục sâu lõi):** tham số model truyền cho các công cụ KHÁC công cụ tìm (lịch, thời tiết, ngày) — chỉ có mục số đo + kết quả (khung lịch); đầu ra thô của bước định tuyến (chỉ có tuyến đã chọn); chuỗi lời dặn gửi model (tra bằng `git_sha`); lượt lỗi TRƯỚC khi vào lõi (thân sai khuôn, chưa sẵn sàng) chỉ có `so_do` + câu gõ; lượt ảnh bị từ chối ở rào đầu vào không ghi.

## Thay đổi

- `backend/core/so_vet.py` (mới, ~70 dòng): `vet_tim`, `ban_ghi`, `ghi` — một module, ghi cuối lượt, mở file kiểu nối; không hàng đợi, không xoay vòng.
- `backend/llm/assistant.py`: cờ `so_vet`; trường `vet: dict` trong vết lượt (chỉ RAM, **luôn thu** — rẻ, không rẽ nhánh theo cờ ⇒ cờ bật / tắt cùng một đường code tới model); `search_into_trace` thêm một mục mỗi lần tìm; cổng web giữ câu gửi + sổ web + chữ model; gộp vết khi đường trả lời chạy song song định tuyến.
- `backend/llm/len_ke_hoach.py`: 2 dòng giữ hành động sửa lịch.
- `backend/api/routes/chat.py`: ghi sổ vết ngay sau dòng `chat_metrics` ở cả đường thường lẫn đường stream; `backend/api/routes/anh.py`: lượt ảnh.
- `backend/core/settings_loader.py`: `HUE_SO_VET`; `backend/config/settings.yaml`: `so_vet: false`.
- `scripts/xem_so_vet.py` (48 dòng); `backend/tests/test_so_vet.py` (4 test).

Không chạm chỗ dựng chuỗi gửi model, lời dặn, công cụ ⇒ không chạy riêng phép "giống byte"; bộ test rộng (có các test khoá chuỗi) chạy một lần — kết quả ở bảng dưới.

## Kiểm

| Bước | Kết quả | Thời gian / tiền |
|---|---|---|
| `test_so_vet.py`: cờ tắt ⇒ không file · cờ bật ⇒ một dòng JSON đủ phần, 10 kết quả / lần tìm · ghi hỏng không ném lỗi, cảnh báo không có nội dung · biến môi trường (`"1"` bị từ chối) | 4 passed | 2 s |
| 4 file chạm trực tiếp (sổ vết, lõi trợ lý, route chat, cờ môi trường), có khoá | 30 passed | 55 s |
| Server tạm của nhánh, `HUE_SO_VET=true`, 4 câu thật: câu trong kho · câu hỏi tiếp (model tự tìm thêm) · câu kho thiếu ⇒ tìm thêm + web · đường không stream | 4 lượt ⇒ 4 bản ghi; lượt hỏi tiếp thấy rõ câu tìm của code (câu cụt) ↔ câu model viết lại; lượt web thấy câu gửi tra web + 5 link + chữ model; `chat_metrics` 4 dòng, 0 chữ nội dung | ≈ 0,0032 USD |
| Bộ test rộng `backend/tests`, có khoá | 1.179 passed, 0 failed | 4 phút 38 giây |

Chưa chạy thật: lượt biểu mẫu, sửa lịch, ảnh với cờ bật (đường code đã có test lõi / route; phần sổ vết của ba loại này mới kiểm bằng đọc code) ⇒ A / User gặp bản ghi thiếu ở ba loại đó thì báo.

## Giới hạn

- File lớn dần (≈ 13 KB / lượt vì có cả ngữ cảnh); không tự xoá — xoá tay thư mục `data/debug_trace/` khi cần.
- Nhiều tiến trình cùng ghi một file (server tạm của các nhánh + server chính) ⇒ dòng xen nhau theo thứ tự giờ; mỗi dòng vẫn nguyên vẹn ở cỡ này trên Linux, không có khoá file.
- Ngày của tên file theo giờ máy lúc ghi.
