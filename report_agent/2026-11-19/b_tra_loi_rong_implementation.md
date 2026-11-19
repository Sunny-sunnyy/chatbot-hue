# Sửa lỗi: lượt "thành công" nhưng người dùng không thấy chữ nào — báo cáo của B

Viết 13:10 19/11/2026 (giờ `date`). Nhánh `p9-b-tra-loi-rong` từ `origin/main` `457a37a`. Việc do phiên điều phối giao (lỗi đã tái hiện). Chẩn đoán chi tiết (riêng tư): `data/kich_ban_pho_thong_2026-11-19/luot_1/chan_doan_tra_loi_rong_B.md`.

## 1. Người dùng thấy gì khác
Trước: thỉnh thoảng một câu hỏi được ghi là trả lời thành công (có cả danh sách nguồn) nhưng khung trả lời TRỐNG. Sau: câu trả lời hiện ra đủ, một lần, ngay trước danh sách nguồn. Mọi lượt bình thường không đổi gì.

## 2. Nguyên nhân và bản sửa
- Model đôi khi phát 2–3 khối chữ trong MỘT lần trả lời. Phần hiện chữ lúc đang stream (`backend/llm/answer_stream.py`) coi mọi mảnh chữ là một chuỗi `{"answer":"…"}` duy nhất; khối đầu không đúng khuôn
  (hoặc là câu trả lời rỗng) thì không mảnh nào được hiện, trong khi câu trả lời cuối (khối cuối) vẫn hợp lệ và qua kiểm trích dẫn.
- Sửa: một lưới cuối ở `backend/api/routes/chat.py` (`StreamEvents.finish`, +3 dòng code): lượt đã qua kiểm trích dẫn mà CHƯA phát mảnh chữ nào và có câu trả lời ⇒ phát cả câu một sự kiện `delta` trước `sources`.
  Không tách lại bộ bóc chữ, không thêm cờ, không thêm số đo. Lượt bị rút vì trích dẫn vẫn bị rút (không phát bù).
- Nơi gọi `finish` (`git grep -n '\.finish('`): 1 nơi trong code chạy (`chat.py` `_answer_events`), 6 nơi trong test (3 file) — đã mở cả 7.

## 3. Bằng chứng
**Test bằng chữ dựng sẵn (không gọi model — KHÔNG phải bằng chứng đường thật):**
| Lệnh (từ `backend/`, từng file một) | Kết quả | RSS tối đa |
|---|---|---|
| `uv run python -m pytest tests/test_chat_stream.py -q` — TRƯỚC khi sửa, đã có test mới | **1 đỏ** (test mới: thiếu `delta`), 22 đạt | 158 MB |
| cùng lệnh — SAU khi sửa | 23 đạt, 8,99 s | 147 MB |
| `… tests/test_luoi_cuoi_bao.py -q` | 10 đạt, 5,21 s | 146 MB |
| `… tests/test_feedback.py -q` (không có khoá API) | 3 đạt · **1 đỏ** (`test_chat_turn_id_feedback_logs_counts_only`) | 1.159 MB |
- Hai test mới: (a) khối đầu là chữ thường / là `{"answer":""}` ⇒ đúng một `delta` mang cả câu, đứng trước `sources`, kể cả khi câu cuối là câu từ chối của model; (b) câu cuối thiếu trích dẫn ⇒ vẫn `error`, không phát bù.
- Một test cũ sửa một dòng (`test_notice_event_follows_sources_when_set`): nó gọi `finish` trên một stream MỚI chưa phát chữ — trạng thái mà nay là điều kiện của lưới cuối — đổi sang dùng lại stream đã phát chữ; điều test bảo vệ (thứ tự `sources · notice · done`) giữ nguyên.
- Ca đỏ ở `test_feedback.py` KHÔNG do nhánh này, cũng không phải lỗi của `main` [máy kiểm, chạy lại sau khi viết bản đầu của report]: đúng ca đó trên cây chính `main` `e72a312` — **đạt** cả không lẫn có
  `--env-file` (31,8 s và 38,0 s; RSS ≈ 1,5 GB). Ở worktree tạm của nhánh nó đỏ vì `FileNotFoundError` — worktree trong `/tmp` không có thư mục `data/` (dữ liệu riêng tư, không nằm trong git) mà `create_app` cần.
  Ca đó đi đường `/api/chat` không stream, không chạm `finish`. ⇒ test nào dựng cả app (`create_app` + lifespan) phải chạy ở cây chính, không chạy ở worktree tạm.
**Lượt thật:** [chưa đo trên đường thật] — lỗi chỉ xuất hiện ở khoảng 3 / 1.093 lượt nên không tái hiện ổn định qua model; chưa có lượt nào chạy qua server với bản sửa. Cả bộ `backend/tests`: CHƯA chạy (phiên điều phối xếp sau).

## 4. Số đếm từ log (0 USD) — ca "đã phát một phần nhưng khác bản cuối"
Mọi lượt stream thành công có phí còn trong log (1.093 lượt, từ 24/08): cờ `delta_matches_final = false` xuất hiện **3 lượt**, cả 3 đều "chưa có mảnh chữ nào" (1 lượt 16/11, 2 lượt 19/11) — **0 lượt** "đã phát chữ nhưng khác bản cuối".
⇒ ca đó chưa từng thấy; nhánh này không sửa nó. Sau bản sửa, cờ này về `true` ở ca rỗng (người dùng đã thấy đúng câu cuối); lượt nhiều khối chữ vẫn nhận ra được ở cột `kind` của `llm_calls`.
Lỗi không phải do bỏ trần token đầu ra hôm 19/11: đã có một lượt ngày 16/11, và hai lời gọi lỗi hôm nay dùng ít token hơn trần cũ.

## 5. Chưa làm / giới hạn
- Chưa biết nội dung khối chữ đầu (log không ghi chữ) — không cần để sửa.
- Chưa xét lượt bị rút vì trích dẫn có nhiều khối chữ có cùng gốc hay không.
- Giao diện: không sửa; sự kiện `delta` duy nhất đi đúng đường hiện chữ sẵn có [chưa kiểm trên trình duyệt].

## 6. Cách thử trong 2 phút
`cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_chat_stream.py -q` ⇒ `23 passed`. Muốn thấy đỏ: bỏ dòng `bu = …` trong `StreamEvents.finish` rồi chạy lại ⇒ 1 test đỏ.

| Đã làm | Chưa làm | Tự hoãn + lý do | Lệnh kiểm + đầu ra |
|---|---|---|---|
| Test đỏ trước, sửa 3 dòng, 2 test mới + 1 test cũ sửa một dòng | Lượt thật qua server; cả bộ test | — | `pytest tests/test_chat_stream.py -q` ⇒ `23 passed in 6.38s` |
