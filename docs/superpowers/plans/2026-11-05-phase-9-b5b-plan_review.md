# Review: plan Phase 9 B5b — thời tiết Huế (`thoi_tiet`) + phương án ngày mưa

## Vòng 1 — bản 1 (sha tính từ file `6d6454fd9fae`, E, 13:32 05/11/2026)

Decision: **changes_requested** (0 blocker · 1 major · 6 minor) — tối đa 2 vòng; vòng 2 chỉ còn minor ⇒ ready.
Người kiểm: E (`hue-rag-7a`) · A giao (xem kỹ: cổng từ khoá — bỏ sót thì sao; kiểm số °C / % / mm; API lỗi ⇒ không số; bảng rà FDE). Chỉ bảng "Căn cứ để review" + code `main`
theo file + hàm. 0 USD. Đếm kho chỉ bằng `scripts/grep_kb.sh` (in số file).

### Đã khớp
- Lệch đề bài (spec không có "§5 B5b") được báo và lấy căn cứ đúng chỗ (plan B5 §2c (b) + D9; spec §11). Phương án (b) User chọn 03/11.
- Số liệu, nguồn, giờ cập nhật, câu bão lũ, câu > 7 ngày đều do code (D5, D6); toạ độ + URL do code, model chỉ gửi enum 0–6 (D2, D3); API lỗi ⇒ câu cố định, không trả như "không mưa" (D7);
  chữ của API không vào model (§9) ⇒ không có kênh cài lệnh. Bộ kín "không" có lý do (sàn chính là code tất định). Tiền 0,045–0,055 / trần 0,06.

### Findings

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| **M-1** | major | D4 (cổng từ khoá) ↔ D8 (kiểm số) ↔ §10 | Câu A hỏi: **bỏ sót từ khoá thì sao?** Plan §10: "không có công cụ ⇒ trả từ kho / từ chối" — nhưng **không nói D8 chạy ở lượt không có công cụ**. Nếu D8 chỉ chạy khi có `thoi_tiet`: câu thời tiết viết lạ ("mai đi Huế mang ô không?", "thứ bảy ra biển Thuận An được không") hoặc hỏi tiếp không từ khoá ("thế còn ngày kia?" — nhớ hội thoại chỉ giữ câu hỏi) ⇒ model **tự viết số dự báo**, không bị bắt — đúng loại lỗi "LLM tự dự báo là bịa số" ở §1. Nếu D8 chạy ở **mọi** lượt với tập cho phép = "số code đưa": kho có **17 file** chứa số kèm °C, 12 file "lượng mưa", 14 file "độ ẩm" ⇒ câu khí hậu trả từ kho (bộ đo có 2 câu) bị **rút nhầm** | Bỏ sót cổng ⇒ hoặc lọt số bịa (sai, nói chắc), hoặc rút nhầm câu kho đúng — plan chưa chọn | D8 ghi rõ: chạy ở **mọi** câu tuyến `tro_ly_hue` khi cờ bật; tập số cho phép = **{số code đưa} ∪ {số có trong các đoạn kho được trích ở lượt đó}** (như sàn tiền B5c spec §11.2 (1)); câu có số dạng thời tiết mà ∉ tập ⇒ rút lại. Đo thêm (Q2): ≥ 3 câu dự báo **không có từ khoá** + 1 chuỗi hỏi tiếp ⇒ 0 số ngoài tập; 2 câu khí hậu kho ⇒ 0 rút nhầm. Kết quả bỏ sót cổng được phép = "không có số dự báo", không phải "số bịa" |
| m-1 | minor | D8 dạng số | "°C / % / mm" chưa đủ cách viết tiếng Việt: "30 độ", "30 độ C", "30°", "70 phần trăm", "5 mi-li-mét", "5 li"; khoảng "24–30", "từ 24 đến 30"; số thập phân "29,6" ↔ code làm tròn | lọt hoặc báo nhầm | ghi danh sách dạng + ca test từng dạng; code làm tròn **trước** khi dựng tập (D5), tập gồm đúng chuỗi số code in |
| m-2 | minor | D4 cổng ↔ lịch sử | Câu hỏi tiếp không từ khoá sau câu thời tiết ("còn chủ nhật?") ⇒ không có công cụ | trả lời rỗng / chung chung ở câu hỏi tiếp rất hay gặp | cổng xét **tin nhắn cuối hoặc câu hỏi liền trước trong lịch sử** (đã có trong trace B3) — rẻ, vẫn tất định; Q1m vẫn giữ cho lượt đơn |
| m-3 | minor | D6 từ khoá "cảnh báo" | "cảnh báo" hay gặp ở câu an toàn không phải thời tiết (vd cảnh báo bậc thang / đường trơn — bộ an toàn 32) ⇒ nối câu NCHMF + 112 vào câu không liên quan | câu trả lời an toàn có dòng khẩn cấp lạc chỗ | D6 chỉ bắt "bão / lũ / ngập" (hoặc "cảnh báo" **cùng** từ thời tiết); ca test "cảnh báo bậc thang" ⇒ không nối |
| m-4 | minor | §3 `thoi_tiet.py` gọi mạng | `tests/test_assistant_boundary.py` `NETWORK_PACKAGES` gồm `httpx`, `urllib.request`… và chỉ `ALLOWED` cho 2 module ⇒ module mới gọi Open-Meteo làm hỏng test rào; gọi đồng bộ trong vòng sự kiện sẽ chặn luồng SSE khác tới 3 s | test đỏ / thêm `ALLOWED` không chủ đích; chặn luồng | §3 ghi: thêm `"llm.thoi_tiet": {<gói>}` vào `ALLOWED` (có lý do); gọi bằng client async hoặc `asyncio.to_thread` |
| m-5 | minor | D3, D5, D9 | (a) "chiều nay có mưa không" (bộ đo) — D5 chỉ có số **theo ngày** ⇒ câu trả lời có thể hiểu là dự báo buổi chiều; (b) Open-Meteo daily cần tham số múi giờ (`timezone`) để "ngày" khớp giờ Việt Nam; (c) D9 không nói đường lỗi API khi lịch có ngày | trả lời lệch ý / sai ngày / lịch hỏng khi API lỗi | (a) câu cố định "dự báo theo cả ngày" khi câu có buổi; (b) D2 ghi `timezone=Asia/Ho_Chi_Minh` (probe bước 3 kiểm); (c) D9: API lỗi ⇒ lịch như B5 + câu cố định "chưa lấy được dự báo", 0 số |
| m-6 | minor | §9 bảng rà FDE | Thiếu cột **hiện trạng** (file + hàm) và **đề xuất** (`Session_Prompt.md` §7 — như plan sửa lịch bản 3 đã thêm) | khó đối chiếu | thêm hai cột (vd `lich_trinh.py` `kiem_cuoi`, `so_tien.py` `tim_so_tien`, `assistant.py` `ROUTE_INPUTS` — trường nào cổng D4 cần, nếu xét lịch sử thì `history` đã có) |

**Ghi chú (không finding):** Q2 "khi API lỗi (fixture ở harness)" — đường lỗi chỉ kiểm bằng **test** trên bản ghi (logic thuần, `Session_Prompt.md` §6, §8: không dựng lỗi giả trên hệ thống thật); nên ghi rõ đó là bằng chứng test, không tính là lượt chạy thật.

### Giới hạn
- Không chạy code / không gọi Open-Meteo. Đếm kho chỉ là số file có mẫu (`grep_kb.sh -l`), không đọc nội dung.

### Decision và bước tiếp
**changes_requested** — C sửa M-1 (+ minor) thành bản 2, báo sha; E kiểm vòng 2 (cuối).
