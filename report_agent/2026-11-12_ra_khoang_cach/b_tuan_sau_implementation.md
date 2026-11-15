# Thời tiết "tuần sau": tính phần nằm trong 7 ngày dự báo — B · 12:25 15/11/2026

Rà nợ 15/11 (`b_ra_no_cu.md`); cách làm theo C (A chốt). Nhánh `p9-tuan-sau` từ main `c842861`. Tiêu chí ghi trước: `data/tuan_sau_2026-11-15/TIEU_CHI.md`.

**Lỗi (tái hiện 0 USD):** `ngoai_7_ngay` coi mọi câu "tuần sau" là ngoài 7 ngày ⇒ câu cố định "chỉ có dự báo 7 ngày" — kể cả Chủ nhật hỏi "thứ hai tuần sau" (= ngày mai).
**Đếm trước:** log không ghi chữ câu hỏi / cờ `ngoai_7` ⇒ **chưa đếm được lượt thật** (chưa có người dùng thật); bộ đã lưu: 2 câu thời tiết có "tuần sau", cả 2 do nhóm viết.
A chọn làm vì đây sửa từ chối nhầm, **không nới rào**: ngày không có dự báo vẫn từ chối như cũ, số có dự báo vẫn qua kiểm số Q2.

**Đổi** (`backend/llm/thoi_tiet.py`, `backend/llm/assistant.py`):
- `ngay_tuan_sau(text, hom_nay)`: **code** tính thứ Hai…Chủ nhật tuần sau ∩ ngày 0–6 có dự báo ⇒ (đầu, cuối) hoặc None (hôm nay thứ Hai; "tuần sau nữa").
- `ngoai_7_ngay`: "tuần sau" chỉ ngoài khi giao rỗng; "tuần sau nữa" vẫn ngoài.
- Lượt có "tuần sau" một phần ⇒ có công cụ `thoi_tiet`; công cụ dùng khoảng ngày code tính (bỏ số ngày model gửi); khối số liệu thêm dòng
  "Dự báo chỉ có tới <thứ dd/mm>; những ngày sau đó của tuần sau chưa có dự báo." (model và người dùng đều thấy). Câu không có "tuần sau" ⇒ không đổi.

| Bước | Kết quả |
|---|---|
| Test 0 USD | `test_b5b_thoi_tiet.py` 92 đạt: đủ 7 ngày trong tuần (thứ Hai ⇒ None … Chủ nhật ⇒ +1…+6), "tuần sau nữa" vẫn ngoài; lượt có công cụ, khoảng ngày code đặt, dòng "chỉ có tới" (Q1 chuỗi mới). 2 test cũ khẳng định hành vi cũ ⇒ sửa (thứ Hai cho ca ngoài; "tuần sau nữa" cho ca câu cố định) |
| Câu chạm (`kiem_bo.py`, 0 USD, hôm nay CN) | chỉ **X01** đổi nhãn (ngoài 7 ⇒ có công cụ); Golden / an toàn: 0 lượt gọi `thoi_tiet` |
| X01 ×3 (server nhánh 8895, `app_thoi_tiet`) | gọi công cụ **3 / 3**, khoảng 6 ngày do code đặt; **0 số lạ** (Q2 chỉ báo 2 mã theo **nhãn cũ** của X01: "thiếu câu ngoài 7" + "công cụ lệch nhãn" — đúng chỗ hành vi đổi có chủ đích); 0 bị rút; không còn câu "chỉ có dự báo 7 ngày" — **đạt**; 0,0021 USD |
| An toàn 32 ×1 | 0 lỗi · **0 đổi lớp** (29 / 3) — **đạt**; 0,0215 USD |
| Test rộng (`backend/tests`, có key, sau build giao diện) | **1.064 đạt** / 0 trượt — 4 phút 47 |

Tiền: **≈ 0,024 USD**. **Bộ B5b (A giao):** nhãn X01 `cong_cu` False / `ngoai_7` True ⇒ **True / False** (luật mới: "tuần sau" chỉ ngoài 7 ngày khi hôm nay thứ Hai; nhãn đúng khi chạy ngày khác thứ Hai); md5 `7e1bc3da2e44` ⇒ `65c6d4bc33f2`, sao lưu `data/phase_9/bo_do_b5b/cau_da_thay.truoc_tuan_sau_2026-11-15.jsonl`; `kiem_bo.py` trên nhánh: OK.
Giới hạn: câu "thứ hai tuần sau" nhận cả các ngày có dự báo của tuần sau (không chỉ thứ Hai); "tuần tới" không thuộc bộ dò "ngoài 7 ngày" từ trước (không đổi).
