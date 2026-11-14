# Rà lời dặn bản 2 — theo HÀNH VI THẬT (XONG 09:51 14/11/2026, `date`)

Người rà: C (`hue-rag-b4`; bắt đầu 13/11 ở `hue-rag-eb`) · A giao (hướng thường trực User: rà khả năng trợ lý) · skill `agent-design-review` · **chỉ đọc, 0 USD, không sửa code / lời dặn**.
Bản 1: `c_ra_loi_dan.md` (12/11, rà bằng đọc code, 5 đề xuất Đ1–Đ5). B rà harness song song (`b_ra_harness_tro_ly.md`) — không chồng.

**Kết luận ngắn:** hành vi thật trong log không cho thấy lỗi mới nào do lời dặn. **Không cần sửa lời dặn đang chạy lúc này.** Giữ Đ1 (lời dặn riêng cho vai lịch mới — đang nằm trên nhánh đợt 1 của B) và Đ5 (ghi 3 luật vào tài liệu, 0 USD).
**Bỏ Đ3**, vì bản 1 tính sai giả định (mục 2). **Không làm Đ4**, vì lợi quá nhỏ. Đ2 giữ đúng thứ tự handoff: chỉ làm khi lượt đếm thấy lỗi.

## 1. Hành vi thật từ log `chat_metrics` (không chứa chữ câu hỏi)

Nguồn: `backend/logs/application.log`, 1.152 dòng có trường tuyến (02/11 19:45 → 13/11 21:05). Phần lớn là **lượt đo của agent**, không phải người dùng thật ⇒ tỉ lệ là của các bộ đo.

| Quan sát | Số | Đọc |
|---|---|---|
| Tuyến (mọi dòng có tuyến) | trợ lý Huế 1.090 · ngoài phạm vi 55 · khẩn cấp 3 (+ 7 dòng `emergency_by=router` từ 09/11, đi đường trợ lý Huế) · trò chuyện 4 | 687 dòng trợ lý Huế không có model / USD = lỗi trước model (`generation_failed` 285 · `internal_error` 276); suy luận: phần lớn là pytest, vì log dùng chung cho pytest và server (`Project_Status.md` §8) — không phải hành vi model |
| Câu trợ lý Huế có model (403) | token vào trung vị 2.057 (p90 9.633) · lần gọi model trung vị 2 (p90 5) · 0,00047 USD · cả câu 4,5 s | khớp số bản 1 |
| Model tự gọi `tim_kho` / câu | 0 lần: 301 · 1: 39 · 2: 26 · **3: 37** (lần 3 bị chặn "hết lượt") | lượt xin thứ ba là lượt thừa ⇒ đã chữa bằng **code** (cờ "hết lượt tìm thì dừng", bật 13/11), không bằng chữ ✔ |
| Câu ngoài phạm vi (55) | đúng 1 lần gọi model (định tuyến) · trung vị 2,06 s · 0,000105 USD · 0 lần tra web | đường rẻ nhất; không có gì cần sửa |
| Công cụ ít dùng | `thoi_tiet` 2 / 403 câu · `ngay_lich` 12 / 403 (lịch tính sẵn 40 lần — đường chính của câu hỏi ngày, đúng như thiết kế) · `lich_trinh` 166 (biểu mẫu) | xem mục 2 |
| Kết cục | thành công 389 · hỏi lại 17 · ngắt kết nối 1 | — |

Script đếm (0 USD): `data/ra_khoang_cach_2026-11-12/tools/dem_log_chat_metrics.py` (chạy `python3 -I`). Khuôn `llm_calls[i]` có trường `kind` = **danh sách loại đầu ra** (`reasoning` / `message` / `function_call`), không phải tên vai ⇒ muốn đếm theo vai phải dùng trường `route` của từng lần gọi.

## 2. Sửa số bản 1 — Đ3 dựa trên giả định sai

Bản 1 (mục 5, Đ3) và bản nháp 2 đều viết: mô tả `thoi_tiet` (168 token) và `ngay_lich` (211 token) "đọc ở mọi lượt". **Sai.** Code chỉ đưa hai công cụ này khi câu cuối hoặc câu hỏi liền trước có từ khoá:
`assistant.py` `_lich_extra` (`co_cong_cu = tu_khoa and not ngoai_7` cho thời tiết; `nl.co_tu_ngay_luot(...)` cho ngày). Ở các lượt khác, danh sách công cụ không có hai công cụ này.
⇒ Lợi của Đ3 chỉ còn ở số ít câu có từ khoá. Hai công cụ dùng 14 / 403 lần, chưa thấy lỗi nào do luật viết nằm trong mô tả ⇒ **bỏ Đ3**. Lỗi này của bản 1 do C đọc mô tả mà không đọc điều kiện đưa công cụ.

## 3. Đề xuất sau khi có số (≤ 5, xếp theo lợi / công)

| # | Đề xuất | Lợi đã thấy | Công | Kết luận |
|---|---|---|---|---|
| Đ1 | Lời dặn riêng, ngắn cho vai lịch mới (một câu cho mỗi điểm trong lịch) | lịch biểu mẫu đang dùng lại lời dặn trả lời (chữ thừa, sai từ) | đã có trên nhánh `p9-len-ke-hoach-v2`; đo trong lượt nghiệm thu lại đợt 1 | **giữ — đang làm (B)** |
| Đ5 | Ghi 3 luật vào `skills/agent-design-review`: việc mới ⇒ lần gọi hẹp hoặc công cụ có luật **trong kết quả**; luật kiểm được ⇒ code; sửa một câu dặn = một bậc đo có sàn an toàn + ngoài phạm vi | 4 lần gộp việc vào vai chính ⇒ 4 lần tụt sàn (bản 1 mục 3); lần thứ 5 (gọi tìm kho thừa) cũng chữa bằng code | 0 USD, A sửa tài liệu | **nên làm** — thêm một vế: "trước khi ước lợi của mô tả công cụ, đọc điều kiện đưa công cụ" |
| Đ2 | Nói rõ cách trả lời câu nhiều ý | đã đếm 3 / 4 ở bộ câu hỏi kèm (12/11) | ≈ 0,10 USD; rủi ro sàn ngoài phạm vi (Phase 8.1 đã phạm) | **theo handoff mục 6**: sau đợt 1 lịch trình, chỉ làm khi lượt đếm thấy lỗi |
| Đ4 | Gộp tuyến khẩn cấp vào tuyến trợ lý Huế trong lời dặn định tuyến | ≈ 120 token / lượt định tuyến; tuyến khẩn cấp chỉ còn đổi một trường log (10 / 1.152 dòng) | phải đo lại bộ an toàn 32 | **không làm**: người dùng không cảm nhận được (dưới 1 % tiền một câu), mà chạm vào phần an toàn |
| Đ3 | Dời luật viết của `thoi_tiet` / `ngay_lich` từ mô tả sang kết quả công cụ | ~0 (mục 2) | ≈ 0,05 USD | **bỏ** |

**Không đề xuất:** viết lại lời dặn theo khuôn có tiêu đề; thêm ví dụ mẫu; tách trợ lý chính thành nhiều agent theo chủ đề (bản 1 mục 1 và 4 vẫn đúng; log không cho thấy chọn sai công cụ).

## 4. Đã kiểm ↔ suy luận ↔ chưa làm

- **Đã kiểm (0 USD):** số mục 1 (đếm log, đã thấy đầu ra); điều kiện đưa công cụ thời tiết / ngày (`assistant.py` `_lich_extra`, `thoi_tiet.co_tu_khoa_luot`, `ngay_lich.co_tu_ngay_luot`); tuyến khẩn cấp đi đường trợ lý Huế (`assistant.py` `ROUTE_KHAN_CAP`).
- **Suy luận:** "dưới 1 % tiền một câu" của Đ4 (120 token định tuyến so với ~2.000 token vào của một câu, chưa tính theo giá); tỉ lệ ở mục 1 là của các bộ đo, không phải của người dùng.
- **Chưa làm (cố ý, theo mức lợi):** đối chiếu từng câu dặn với từng lượt đo trong `data/`. Lượt đo của từng bậc đã giữ sàn khi bậc đó bật, nên lượt đối chiếu này không bảo vệ sàn nào mới. Chưa đếm câu nhiều ý trên B7 (để cho lượt đếm của Đ2 ở handoff mục 6). Log không ghi danh sách công cụ đã đưa, chỉ ghi công cụ đã chạy.
