# Tải lại trang ⇒ cuộc trò chuyện mới ở server — implementation (C, 20:35 15/11/2026)

Giao: A, tối 15/11, từ lỗi User gặp khi thử trang Trợ lý. Nhánh `p9-f5-cuoc-moi`. Sửa 1 file `frontend/src/chat.jsx` (8 dòng). Tiền **0,0159 USD** (12 lượt hỏi thật, đếm theo log của server tạm).

## Lỗi User gặp

Hỏi câu vị trí một di tích (A, trả lời đúng) ⇒ hỏi tiếp khoảng cách sang một di tích khác (B, kho từ chối + mục web) ⇒ tải lại trang (màn hình trống) ⇒ hỏi lại đúng câu A ⇒ bị **từ chối**, mục web nói về khoảng cách của câu B.

## Tái tạo [đã chạy] — đúng đường người dùng (`POST /api/chat/stream`, giữ cookie), server tạm cổng 8041 từ worktree

| Lần | Lượt 3 (hỏi lại A): số lượt lịch sử server đưa vào | Từ chối | Mục web nói về |
|---|---|---|---|
| 1 | 2 | có | (chưa ghi chữ web ở lần này) |
| 2 | 2 | có | khoảng cách của câu B |
| 3 | 2 | có | khoảng cách của câu B |

- **Nguyên nhân đã chứng minh (phần tải lại trang):** lịch sử nằm ở server theo cookie 30 phút (`backend/api/conversations.py`); tải lại trang chỉ xoá lượt trên màn hình, cookie còn ⇒ lượt 3 chạy như lượt thứ ba của cuộc cũ (`n_history_turns = 2` trong `chat_metrics`).
- **Lỗi riêng, CHƯA sửa (quan sát, chưa có nguyên nhân):** tải lại trang không đổi gì ở server, nên ba lần trên cũng chính là ca "trong CÙNG một cuộc: hỏi A ⇒ hỏi tiếp B ⇒ hỏi lại A" ⇒ câu A bị từ chối **3 / 3**; model tự tìm kho thêm 1–2 lần ở lượt 3 rồi vẫn từ chối; câu tra web lấy từ câu tìm của model (`cau_tu_model: true`). Log không ghi chữ câu tìm nên chưa biết model đã viết gì; cuộc chỉ nhớ câu hỏi, không nhớ câu trả lời (`nho_cau_tra_loi: false`). n = 3, một bộ ba câu ⇒ chưa biết rộng cỡ nào. Sửa chỗ này là đổi lời dặn / cách đưa lịch sử ⇒ cần plan + đo riêng; A quyết.

## Sửa

- `useChat`: lúc ứng dụng nạp gọi `POST /api/conversation/new` một lần (đúng route nút "Cuộc trò chuyện mới" đang dùng) ⇒ server quên cuộc cũ, cùng lúc màn hình trống. Trong vài chục mili giây chờ lệnh này nút Hỏi bị khoá (dùng lại trạng thái "đang đặt lại" sẵn có) để câu đầu không rơi vào cuộc sắp bị xoá. Lỗi mạng ⇒ bỏ qua, vẫn cho hỏi.
- Hệ quả đã biết (A nêu trước): lịch đã lưu trong cuộc để sửa bằng lời cũng mất khi tải lại trang — khớp với màn hình trống. Khung chat nổi và trang Trợ lý dùng chung một cuộc nên cùng được đặt lại.
- Không đổi backend, lời dặn, chuỗi gửi model.

## Kiểm sau sửa [đã chạy] — Playwright 1440, cùng server tạm, bản build của nhánh

| Bước | Kết quả |
|---|---|
| Nạp trang | 1 lần gọi đặt cuộc mới; nút Hỏi mở lại |
| Hỏi A ⇒ hỏi tiếp B | lịch sử 0 ⇒ 1; B bị kho từ chối như trước (không thuộc việc này) |
| Tải lại trang | màn hình 0 lượt; thêm 1 lần gọi đặt cuộc mới |
| Hỏi lại A | **lịch sử 0, được trả lời, 0 câu từ chối trên màn hình** |
| Nút "Cuộc trò chuyện mới" | vẫn xoá màn hình |
| Lỗi console | 0 |
| `npm run build` · `test_static_ui.py` | đạt · 4 passed (9 s) |

- Không có test đơn vị mới: thay đổi là một lệnh gọi lúc nạp trang, dự án không có bộ test JS; ca Playwright trên là phép kiểm (script giữ lại để chạy lại).
- Thời gian: Playwright ~40 s; lượt có phí: 9 lượt tái tạo + 3 lượt sau sửa.
- Dữ liệu (private): `data/f5_cuoc_moi_2026-11-15/` — `tai_tao.py`, `tai_tao.json`, `pw_f5.py`, `ket_qua_pw.json`, `sau_f5_1440.png`, `chat_metrics.log`.
