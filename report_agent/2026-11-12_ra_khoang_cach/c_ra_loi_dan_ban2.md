# Rà lời dặn bản 2 — theo HÀNH VI THẬT (DỞ — dừng vì kết phiên 22:38 13/11/2026, `date`)

Người rà: C (`hue-rag-eb`) · A giao 13/11 (hướng thường trực User: nghiên cứu khả năng trợ lý, lời dặn, harness, hành vi) · skill `agent-design-review` · **chỉ đọc, 0 USD, không sửa code / lời dặn**.
Bản 1: `c_ra_loi_dan.md` (12/11, rà bằng đọc code). B rà harness song song (`b_ra_harness_tro_ly.md`) — không chồng.

## Đã làm tới đâu
1. **Lời dặn hiện tại** (`backend/llm/full_corpus_prompt.py` trên `main` `73c66b4`): KHÔNG đổi so với bản 1, trừ nhánh `p9-len-ke-hoach-v2` thêm vai mới `LICH_V2_LOI_DAN` (đúng khung bản 1 mục 7, chưa merge). Token từng vai: dùng lại số bản 1 (chưa đếm lại — chuỗi không đổi).
2. **Hành vi thật từ log `chat_metrics`** (`backend/logs/application.log`, không chứa chữ câu hỏi; chỉ lấy dòng có model + tiền ⇒ bỏ dòng pytest): **407 lượt, 03/11 18:29 → 13/11 21:05**. Phần lớn là **lượt đo của agent**, không phải người dùng thật ⇒ tỉ lệ dưới đây là của các bộ đo, không phải của người dùng.
   - Tuyến: `tro_ly_hue` 403 · `tro_chuyen` 4 (câu ngoài phạm vi trả câu cố định không qua model ⇒ không lọt bộ lọc "có model" — **chưa đếm**).
   - Câu `tro_ly_hue`: token vào trung vị **2.057** (p90 9.633) · ra 186 · suy luận 56 · lần gọi model trung vị 2 (p90 5) · **0,00047 USD** (p90 0,0018) · cả câu 4,5 s (p90 14,9 s).
   - **Model tự gọi `tim_kho`**: 0 lần 301 câu · 1 lần 39 · 2 lần 26 · **3 lần 37** (lần thứ 3 bị chặn "hết lượt" — 37 dòng có dấu `het_luot`) ⇒ khớp số đếm 12/11 (6 / 8 câu kho thiếu): lượt xin thứ ba là lượt thừa — nay cờ "hết lượt tìm thì dừng" đã bật (13/11).
   - **Công cụ ít dùng mà mô tả gửi kèm**: `thoi_tiet` được gọi ở **2 / 403** câu; `ngay_lich` ở **12 / 403** (lịch tính sẵn `lich_san` 40 lần — đường chính của câu ngày đúng như thiết kế); `lich_trinh` 166 (biểu mẫu). Mô tả `thoi_tiet` (168 token) đi kèm mọi lượt có cờ ⇒ **củng cố đề xuất Đ3 của bản 1** (chuyển luật viết khỏi mô tả); cần đếm: `thoi_tiet` có trong danh sách công cụ ở bao nhiêu lượt (log chưa ghi danh sách công cụ đưa, chỉ ghi công cụ đã chạy).
   - Kết cục: success 389 · hỏi lại 17 · ngắt kết nối 1.
3. Script đếm (0 USD): `data/ra_khoang_cach_2026-11-12/tools/dem_log_chat_metrics.py` — chạy `python3 -I <file>` (đọc dòng `chat_metrics {json}`, lọc `model` + `usd`).

## CÒN LẠI (phiên sau)
- Đối chiếu từng câu dặn (định tuyến, trả lời, ghi chú công cụ, lịch sử, mô tả 4 công cụ, biểu mẫu, Từ web, trò chuyện) với: lượt đo đã lưu ở `data/` (B7 `data/phase_9/b7/`, hết lượt tìm `data/het_luot_tim_2026-11-12/`, lịch trình `data/phase_9/lich_trinh/bo_do_v2/` + nghiệm thu đợt 1) ⇒ mỗi câu: giữ sàn nào · đã bắt lỗi gì · thừa / mâu thuẫn / dài vô ích.
- Đếm câu ngoài phạm vi (tuyến không qua model) + `n_llm_calls` theo tuyến; khoá trường `llm_calls` (trường loại lần gọi không phải `loai` — xem khuôn trước khi đếm).
- Hai câu dặn kéo ngược nhau (bản 1: :19 ↔ :97 ↔ `TOOL_LIMIT_TEXT`): đếm trên B7 số câu nhiều ý bị từ chối cả câu.
- Đầu ra: ≤ 5 đề xuất xếp theo lợi / công, mỗi cái kèm số lần lỗi đã thấy; gửi cả nhóm.
