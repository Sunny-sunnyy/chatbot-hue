# So mốc bước (b) lịch trình — C tính lại số của B (20:26 13/11/2026, `date`)

Việc A giao (plan đợt 1 §3 (b): "số ở cột phải là mốc so, lệch nhiều thì tìm lý do"). 0 USD, chỉ đọc, không chạm kho / bảng / nhánh. Đầu vào: nhánh `p9-len-ke-hoach-v2` `edbeefb` (đọc `backend/llm/lich_trinh_v2.py` bằng `git show`, không đổi nhánh) · bảng `data/phase_9/lich_trinh/diem_v8.json` md5 `6335b21eb243` (khác bảng đề xuất 12/11 đúng 2 chỗ: Cung An Định thêm nhãn lễ hội – nghệ thuật; thác Nhị Hồ xếp cả tháng 3).

## Kết quả: KHÔNG lệch

| Sàn (plan) | Số B (test `test_simulation_floors`) | C tính lại — code đếm riêng trên đầu ra `xep_v2` | Mốc bản thử của C (`mo_phong_kieu_di.py`, cùng bảng) |
|---|---|---|---|
| kiểu đi: 3 khung khác nhau ≥ 70 % | 65 / 80 = 81 % | 65 / 80 = 81 % (so danh sách id theo ngày / buổi) | 24 / 30 = 80 % (bản thử chỉ có một sở thích ⇒ 30 nhóm) |
| bậc thang giảm ≥ 50 % cặp | 420 / 720 = 58 % | 420 / 720 = 58 %, 0 cặp tăng · nếu chỉ tính cặp mà bản không hạn chế có ≥ 1 điểm nhiều bậc: 420 / 555 = 76 % | chưa có trong bản thử |
| điểm ban ngày không bao giờ xếp ≤ 3 | 1 | 1 (lăng Gia Long) | 1 (lăng Gia Long; 4 điểm chỉ-buổi-tối không tính) |
| mỗi sở thích ≥ 50 % (lịch 2 ngày, từng tổ hợp) | thấp nhất 50 % (chụp ảnh, lễ hội) | tính theo **điểm**: thấp nhất 50 % (lễ hội, chụp ảnh), 0 / 60 tổ hợp dưới sàn · tính theo **buổi** có ≥ 1 điểm hợp: lễ hội thấp nhất 100 %, chụp ảnh 50 % | chưa có trong bản thử |
| (Luôn) kiem_khung | 0 lỗi / 960 | 0 / 960 | — |

Bản thử của C trên cùng bảng còn khớp các "Luôn" so được: ưu tiên số 1 có mặt 30 / 30 mỗi lựa chọn · 0 lịch có cụm xa ngày 1 · 18 / 18 điểm ưu tiên cụm xa ở ngày 2 · tổng số điểm nhẹ nhàng ≤ cân bằng ≤ khám phá 0 / 60 sai. Bộ xếp CŨ (`mo_phong_v8.py` cấu hình A, bảng v3 đang chạy): `kiem_khung` 0 / 360 — không bị bước (b) chạm.

## Ghi chú
- **Hai sở thích đứng đúng ngưỡng 50 %** (lễ hội – nghệ thuật, chụp ảnh — tính theo điểm). Đạt sàn nhưng không có biên: đổi một dòng bảng (vd bỏ đề xuất gắn nhãn Đàn Nam Giao / thêm điểm khác loại vào cụm đó) có thể đẩy xuống dưới ⇒ test `test_simulation_floors` sẽ bắt (đúng thiết kế: ô ẩn bằng cấu hình).
- Số bậc thang phụ thuộc mẫu số: 58 % (mọi cặp) ↔ 76 % (cặp có điểm nhiều bậc để giảm). Cả hai qua sàn; ghi để người đọc report không so lệch thước.
- Chỉnh script của C để chạy lại trên bảng khác: `mo_phong_kieu_di.py`, `mo_phong_v8.py` nhận biến môi trường `BANG` (mặc định vẫn bảng đề xuất).
- Lệnh tính lại: `BANG=data/phase_9/lich_trinh/diem_v8.json uv run python data/phase_9/lich_trinh/tools/mo_phong_kieu_di.py` (tương tự `mo_phong_v8.py`); code đếm riêng: `data/phase_9/lich_trinh/tools/dem_lai_buoc_b.py` (lệnh ở dòng đầu file).
