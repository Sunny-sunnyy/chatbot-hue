# Rà harness trợ lý (định tuyến, vòng công cụ, phục hồi, nhớ, song song) — B · **DỞ** (dừng vì kết phiên, 22:38 13/11/2026)

A giao 13/11 (hướng thường trực User: nghiên cứu khả năng / harness của trợ lý). Chỉ đọc, **0 USD**. Theo skill `skills/agent-design-review/SKILL.md`.
Đã đọc trước để không đề xuất trùng: `e_khoang_cach_agentic.md`, `c_ra_loi_dan.md`, `c_phan_chua_on.md` (mục 3b–3e).

## 1. Đã làm: đếm log thật (0 USD) — `data/ra_harness_2026-11-13/dem_log.py` ⇒ `dem_log.txt`

**Thước:** chỉ dòng `chat_metrics` của `backend/logs/application.log` (main) có **gọi model thật** (`model = gpt-6-luna`). Log trộn dòng pytest mô phỏng lỗi
(`internal_error`, `generation_failed`, `retrieval_unavailable`… không tách sạch được bằng trường nào) ⇒ **mọi con số lỗi / outcome lỗi của log không dùng làm bằng chứng**.
Còn **354 lượt** (27/10 – 13/11), **gần như toàn bộ là lượt đo của agent** (B7, thí nghiệm, Playwright), không phải người dùng thật ⇒ chỉ là **dấu hiệu**, không phải phân bố thật.

| Số | Giá trị | Ghi chú |
|---|---|---|
| Tuyến | `tro_ly_hue` 295 · `tro_chuyen` 4 · không ghi tuyến 55 (dòng trước khi có định tuyến, 27/10) | `ngoai_pham_vi` không gọi model trả lời ⇒ không có trong thước này |
| `tro_ly_hue`: cả câu p50 / p95 | 5,99 s / 20,8 s | gồm lượt lịch (biểu mẫu) + câu nhiều lần tìm |
| `tro_ly_hue`: chữ đầu p50 / p95 (stream, n = 189) | 3,22 s / 9,43 s | sàn User: chữ đầu p50 ≤ 3 s, p95 ≤ 5 s ⇒ **vượt** trên tập đo này (tập lệch về câu khó) |
| Lần gọi model / lượt `tro_ly_hue` | 1: 82 · 2: 101 · 3: 29 · 4: 31 · 5: 21 · 6: 31 | 6 lần ⇒ định tuyến + 4 lượt vòng công cụ + web |
| `tim_kho` / lượt `tro_ly_hue` | 0: 82 · 1: 111 · 2: 39 · 3: 26 · 4: 37 | 3–4 = lần tìm đầu của code + model tìm thêm tới trần |
| Chạm trần tìm / `max_turns` | 37 lượt | đúng ca cờ "hết lượt tìm thì dừng" (bật 13/11) nhắm tới |
| USD / lượt `tro_ly_hue` | TB 0,00079 · p95 0,0021 | sàn User ≤ 0,0005 / câu ⇒ **vượt** ở TB trên tập đo này |
| Từ chối (`tro_ly_hue`) | 58 / 295; cổng web có mục 27 / 58 | web không tin cậy 15 · chưa xác minh 13 · thiên tai 1 |
| Định tuyến | `routing_ms` p50 1,83 s / p95 3,82 s · `route_error` 0 · khẩn cấp do định tuyến 4 | |
| Song song định tuyến (#6) | phần trả lời chạy trước bị bỏ 3 / 192 lượt stream, 0,0005 USD tổng | rẻ |
| Nhớ hội thoại | 0 lượt lịch sử 272 · có lịch sử 27; `history_tokens` p95 36 | chỉ nhớ câu hỏi (cờ) |
| Công cụ (số lần) | `tim_kho` 415 · `lich_trinh` 82 · `tra_web` 57 · `lich_san` 40 · `ngay_lich` 19 · `thoi_tiet` 2 | |

## 2. CÒN (chưa làm — phiên sau)
- Bảng rà theo skill (mục · hiện trạng `file:hàm` · khớp / lệch · số đo) cho: `_pick_route`, vòng công cụ (`tool_for_turn`, `tra_web`, `thoi_tiet_for_turn`, `ngay_lich_for_turn`, `lich_trinh_for_turn`), `max_turns` / `het_luot_bo_cong_cu`, phục hồi khi lỗi / hết giờ, `api/conversations.py`, `answer_turn_stream_parallel`, chia việc code ↔ model.
- Tách số đo theo **loại lượt** (câu kho / câu lịch / câu ngày / câu web) — log chưa có nhãn loại câu (việc "nhãn loại câu" đang chờ); tạm tách bằng `tools` + `lich_trinh_ok` + `has_web_section`.
- ≤ 5 đề xuất xếp theo lợi / công, mỗi cái ghi "lỗi đã thấy bao nhiêu lần" — CHƯA đề xuất gì (chưa đủ bảng). Lưu ý cho người làm tiếp: số tốc độ / tiền ở trên lệch về câu khó; muốn kết luận "vượt sàn" phải đo trên bộ câu đại diện, không trên log đo.
