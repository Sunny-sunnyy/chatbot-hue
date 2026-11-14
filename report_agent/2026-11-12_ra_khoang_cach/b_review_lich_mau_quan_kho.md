# Review nhánh `p9-lich-mau-quan-kho` `f2e43de` (E): lịch mẫu chỉ hiện quán có bài kho

- **Người kiểm:** B, 17:01 14/11/2026.
- **Mức:** nhẹ, 0 USD.
- **Kết luận: `ready_for_user_confirmation`.** 0 finding.

## Cổng tối thiểu
- **Diff:** 2 file (`api/routes/cong.py` +3, test +5). Đúng chốt m-2 của A: chỉ `dung_lich_mau` dùng bản cờ có `quan_bang` lọc `nguon == "kho"`; `chuan_bi` của lịch thật không đổi.
- `dataclasses.replace` tạo bản cờ mới chỉ trong hàm; bộ đệm `_mau` vẫn theo `id` của bộ cờ gốc nên không lẫn bản lọc với bản thật. Không gọi model.
- **Test khẳng định:** mọi quán của lịch mẫu không có nhãn nguồn mở và có `bai_id`; lịch mẫu bằng đúng khối `gan_o_an` dựng trên bản cờ lọc.
- E báo: 2 file 112 đạt có / không khoá; server thật 3 bữa, bữa trưa gần lăng Tự Đức không có quán kho trong 2 km ⇒ bỏ (không lấy OSM). Đúng ý "bản trưng bày".

## Ghi nhận
Khi nhánh luật khu buổi tối của B (`p9-o-toi`) vào main, khu ở của lịch mẫu sẽ đổi từ "phía tây yên tĩnh" sang trung tâm (lịch mẫu có hai buổi tối ở trung tâm). Ảnh lịch mẫu nên chụp lại sau khi cả hai nhánh vào.
