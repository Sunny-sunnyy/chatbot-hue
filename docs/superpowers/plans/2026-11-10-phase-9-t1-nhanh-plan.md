# Plan — câu ngày nhanh hơn (T1 nhanh) · mức nhẹ · E · bản 1

Người viết: E (`hue-rag-e4`), 10/11/2026. Việc: `CURRENT_HANDOFF.md` "VIỆC PHIÊN 10/11" (A giao 19:05 10/11/2026). Nhánh `p9-t1-nhanh` từ `main` `624a17b`, worktree `/tmp/e_t1_nhanh`.

## 1. Vấn đề (đã thấy ở lượt đo thật)

S5 09/11 (`data/phase_9/s5_chung/s5_main_r1.jsonl`, n = 5 câu ngày): chữ đầu p50 5,19 s, max 11,0 s; 0,00063 USD / câu. Mỗi câu gọi trợ lý **2–4 lần** sau định tuyến:
lần 1 model gọi `ngay_lich` (thường `hom_nay` hoặc đổi một ngày âm đọc được trong kho), lần sau mới viết. Mỗi lần ~1,5–3 s và trả lại cả ngữ cảnh 10 đoạn.

## 2. Thay đổi (một thứ: ngày do code tính **trước** lần gọi model đầu)

- **D1 — `ngay_lich.lich_san(cau, ngu_canh, hom)`** (code, tất định) ⇒ các dòng chữ:
  hôm nay · ngày mai · ngày kia (thứ, dương, âm) · "tuần này / tuần sau" ⇒ **từng ngày** trong tuần · "tháng này" như `khoang_ngay` hiện có ·
  ngày dương viết rõ trong câu (`dd/mm/yyyy`, theo đúng bộ dò hiện có) ⇒ ngày âm ·
  ngày âm trong **câu hỏi** (Tết / mùng 1 Tết ⇒ 1/1; "rằm tháng Giêng / tháng N"; "mùng / mồng N tháng X"; "N/N âm lịch"; "rằm tháng này / tới / sau")
  và trong **đoạn kho của lần tìm đầu** (chỉ dạng có "âm lịch" theo sau, hoặc "rằm / mùng / mồng … tháng …") ⇒ lần gần nhất đã qua + lần sắp tới
  (dùng lại `_hai_lan`, kèm "còn / đã qua N ngày"); câu nêu năm 1976–2100 ⇒ thêm ngày của năm đó. Tối đa 6 ngày âm (câu hỏi trước, rồi kho theo thứ tự).
- **D2 — chỗ gắn:** `assistant._before_model`, sau lần tìm đầu, khi cờ `ngay_lich` bật **và** `co_tu_ngay_luot` thấy từ chỉ ngày ⇒ các dòng D1 thành
  **một nguồn** "Lịch hệ thống" trong sổ nguồn (id kế tiếp, khuôn như nguồn `ngay_lich` hiện có) nối sau ngữ cảnh. Một chỗ này phủ cả `/api/chat`,
  `/api/chat/stream` và đường song song #6 (cùng gọi `_before_model`).
- **D3 — công cụ `ngay_lich` giữ làm đường dự phòng** (ngày âm chỉ hiện ở lần `tim_kho` sau, ngày ngoài 6 mục): mô tả `NGAY_LICH_MO_TA` đổi thành
  "hôm nay, mai, ngày kia, tuần, và ngày âm trong câu / tài liệu đã có trong nguồn Lịch hệ thống — chỉ gọi khi cần đổi một ngày chưa có ở đó".
  `max_turns` + 1 khi có công cụ giữ nguyên.
- **Không đổi:** câu không có từ chỉ ngày (không qua D2, danh sách công cụ như cũ); lời dặn trả lời, định tuyến, model.
- **Bỏ (đã cân):** gỡ hẳn công cụ — nhanh chắc hơn nhưng ngày âm đọc được ở lần `tim_kho` sau sẽ bị model tự đổi (rủi ro sai ngày L2) ⇒ không.

## 3. Tiêu chí (ghi trước) — mỗi mục ghi sàn nó giữ

| # | Tiêu chí | Sàn giữ | Đo |
|---|---|---|---|
| 1 | Câu ngày chữ đầu **p50 ≤ 3 s, p95 ≤ 5 s** (bên nhánh) | tốc độ (User 28/10) | `chat_metrics.first_text_ms` theo `turn_id` |
| 2 | **≤ 0,0005 USD / câu** trung bình (bên nhánh) | tiền (User 28/10) | `chat_metrics.usd` |
| 3 | **Đúng ngày không tụt:** số câu L1 / L2 / L3 của nhánh ≤ mốc; từ chối nhầm không tăng | nói chắc sai (lỗi thứ 2) | 1 người chấm mù (sub-agent, brief T1 `data/phase_9/t1/cham/brief_cham.md`) + `kiem_l2.py` (code) |
| 4 | Câu không có từ chỉ ngày ⇒ chuỗi gửi model **giống byte** `main` | không đổi hành vi câu khác | Q1 `capture_all` (0 USD, không mạng): khác ⇔ đúng các ca bộ dò bật |
| 5 | 4 câu an toàn bộ dò bật (S01 S02 S03 S12) × 2 lượt: 0 đảo · 0 sai điều kiện · 0 thiếu cảnh báo · 0 ngoài kho | an toàn S1 | cùng người chấm; 28 câu an toàn còn lại giống byte (mục 4) nên không chạy |
| 6 | Câu Golden bộ dò bật (9 / 176) không tụt nhãn so mốc | S4 | cùng người chấm, 1 lượt mỗi bên |

Không đạt 1–2 mà 3–6 đạt ⇒ báo A số đo, không tự chỉnh vòng 2. Tụt 3 / 5 ⇒ dừng, báo A.

## 4. Bộ đo + tiền

- **Câu ngày 19 câu** (bộ đã dùng cho T1, đổi bộ đo không được): `bo_sau_g.jsonl` 14 + `bo_xac_nhan.jsonl` X2 X5 X6 X9 X13 — gồm 5 câu ngày của S5.
  Loại câu: hôm nay / mai là ngày âm nào · ngày âm nêu trong câu · lễ hội có ngày âm trong kho · giờ mở cửa hôm nay · 1 câu ngoài kho.
- **Thứ tự** (một server một lúc; nhắn A + B "bắt đầu đo" / "đo xong"): mốc = server `main` (cờ đang bật) ⇒ tắt ⇒ nhánh = server worktree. Cùng giờ để "hôm nay" giống nhau.
- **Tiền dự phóng:** ngày 19 × 2 bên × ~0,0006 ≈ 0,023 · an toàn 4 × 2 lượt ≈ 0,005 · Golden 9 × 2 ≈ 0,009 ⇒ **≈ 0,04 USD** (trần 0,1). Chấm bằng sub-agent: 0 USD API.
- **Test (0 USD):** `test_ngay_lich.py` thêm test cho `lich_san` (ngày âm trong câu / trong kho, năm nêu rõ, trần 6, tuần từng ngày) + test gắn nguồn ở
  lượt đầu / lượt có lịch sử / stream; cả `backend/tests` một lần trước bàn giao.
