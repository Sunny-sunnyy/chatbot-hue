# Nhãn "khả năng mưa cao nhất trong ngày" — B · 11:46 15/11/2026

User duyệt 15/11 (A giao). Nhánh `p9-nhan-mua` từ main `0870fba`. Tiêu chí ghi trước: `data/nhan_mua_2026-11-15/TIEU_CHI.md`.

**Vì sao:** `precipitation_probability_max` của Open-Meteo là **giờ có xác suất mưa cao nhất trong ngày** (sự kiện > 0,1 mm / giờ), không phải khả năng mưa cả ngày
(tra cứu 15/11, `b_nguong_mua_3_model.md`). Chữ cũ "khả năng mưa 80 %" dễ đọc như "80 % ngày mai mưa".

**Đổi (3 dòng):** `backend/llm/thoi_tiet.py` `dong_ngay` ⇒ "khả năng mưa cao nhất trong ngày X %" (vào kết quả công cụ `thoi_tiet` gửi model + dòng dự báo của lịch);
`frontend/src/TrangChu.jsx` ô thời tiết ⇒ "khả năng mưa cao nhất X %"; `backend/tests/test_b5b_thoi_tiet.py` khẳng định khối mới (Q1: chuỗi mới). Số không đổi.

| Bước | Kết quả |
|---|---|
| Câu chạm (code, 0 USD) | Golden 176 + 65 + an toàn 32: 0 lượt gọi `thoi_tiet` ⇒ không chạm. Chạm = bộ B5b đã thấy, 14 câu / 15 lượt có công cụ |
| Mô phỏng 0 USD | `kiem_bo.py` trên nhánh: OK |
| Test file chạm | `test_b5b_thoi_tiet.py` + `test_len_ke_hoach_v2.py`: 175 đạt (25 s) |
| B5b ×1 (server nhánh qua `app_thoi_tiet`, 11:22–11:24) | Q2 **0 sai** (0 số ngoài bản ghi API / đoạn trích) · 0 lượt bị rút · gọi công cụ **9 / 9** câu dự báo (sàn ≥ 8 / 9) — **đạt**; 0,0102 USD |
| An toàn 32 ×1 (11:35–11:37) | 0 lỗi · **0 đổi lớp** so với lượt kho 6 (29 trả lời / 3 từ chối kho, như mốc) · 0 ngoài kho bị trả lời — **đạt**; 0,0221 USD |
| Test rộng (`backend/tests`, có key, sau build giao diện) | **1.055 đạt** / 0 trượt — 5 phút 44 |

Bốn số an toàn: đảo cảnh báo 0 · sai điều kiện mới 0 · thiếu cảnh báo mới 0 (không đổi lớp, không chấm S-AT vì câu an toàn không chạm chuỗi đổi) · ngoài kho bị trả lời 0.
Tiền: **0,032 USD**. Lượt B5b chạy lúc C vừa dựng xong chỉ mục, trước tin "chờ E build Docker" — lượt không đo độ trễ nên không ảnh hưởng số.
