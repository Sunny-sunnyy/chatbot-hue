# Bữa trưa lấy điểm khác trong ngày khi điểm cuối buổi sáng không có quán (C, 14:18 17/11/2026)

Lỗi tự thử 16/11 (TONG_HOP #24): lịch đi 18/11, ngày 2 không có bữa trưa. Việc A giao chiều 17/11; nhánh `p9-bua-trua-gan`, gốc main `c1fd6c9`.

## Tái hiện [Chạy, hàm thuần, 0 USD]
- `quan_lich.an_uong` chỉ xét **điểm cuối buổi sáng** cho bữa trưa; điểm đó không có quán trong 2 km ⇒ cả ngày không có mục trưa.
- Đếm 1.890 ngày (5 cỡ lịch × 3 kiểu đi × 7 bộ sở thích × 3 nhóm khách × khô / mưa mọi ngày, đi 18/11): **52 ngày thiếu bữa trưa** (khô 23, mưa 29) — Không gian lưu niệm Lê Bá Đảng 42, Điện Hòn Chén 6 (quán gần nhất cùng cụm 3,6 km), Bãi biển Thuận An 4. Ở **52 / 52** ngày đó, một điểm khác trong cùng ngày có quán trong 2 km.
- Script: `data/bua_trua_2026-11-17/tools/dem.py` (chạy từ `backend`).

## Sửa
`backend/llm/quan_lich.py` `an_uong`: bữa trưa xét lần lượt điểm sáng (từ cuối về đầu) rồi điểm đầu buổi chiều; dừng ở điểm đầu tiên có quán **hoặc** có ghi chú ăn của kho (Bạch Mã… vẫn giữ ghi chú). Điểm đầu có quán ⇒ y như trước. Cách chọn điểm cho bữa tối không đổi; quán bữa tối có thể đổi khi bữa trưa mới đã dùng quán gần đó (không lặp quán trong chuyến — B đếm 101 / 960 khung, đọc 2 ca: đúng ý). Khối `an` không vào tin nhắn gửi model ⇒ chuỗi gửi model không đổi.

## Kết quả [Chạy]
| Tiêu chí | Kết quả |
|---|---|
| Ngày thiếu bữa trưa trên 1.890 ngày | 52 ⇒ **0** |
| `tests/test_quan_lich.py` (thêm 1 test: Hòn Chén cuối sáng ⇒ trưa gần Thiên Mụ; Bạch Mã giữ ghi chú) | 17 passed (23 s) |
| Test rộng | KHÔNG chạy (nhánh chỉ đổi một hàm thuần + test của nó — Session_Prompt §8) |
