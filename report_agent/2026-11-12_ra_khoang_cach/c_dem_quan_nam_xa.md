# Đếm bữa ăn vùng nam xa (Bạch Mã / Nhị Hồ) — trước khi tìm quán

C, 09:39 15/11/2026 (`date`). Việc A giao: handoff mục 3(iii). 0 USD, 0 server, không cào.
Script + kết quả: `data/dem_quan_nam_xa_2026-11-15/tools/dem.py`, `data/dem_quan_nam_xa_2026-11-15/dem.json`.

## Kết luận

**Đếm rồi không làm (không đi tìm quán).** Lý do chính không phải số nhỏ mà là kho đã nói rõ: gần các điểm này không có quán để gợi ý.
- Bạch Mã: kho dặn mang đồ ăn trưa vì trong vùng lõi không có hàng quán.
- Nhị Hồ: có chòi ăn uống ngay tại điểm nhưng không có tên quán; điểm đóng cửa 17:30.

Tìm quán ở đây vừa trái với kho vừa ít lợi. Đề xuất nhẹ hơn ở cuối (chưa làm, chờ nhóm / A).

## Số đếm [đã chạy]

Tập đếm: đúng 3.840 khung như lần đếm 69,1 % (`dem_theo_cum.py`), bảng quán hiện hành (md5 `ab481586d46f`). Mỗi khung có trọng số bằng nhau.

| Đo gì | Số | Ý nghĩa |
|---|---|---|
| Khung lịch có ≥ 1 bữa ở nam xa | 720 / 3.840 = **18,8 %** | |
| Bữa ở nam xa | 1.080 / 22.680 = **4,8 %** | = 24,7 % của 4.374 bữa đang không có quán |
| — trưa sau buổi sáng ở Bạch Mã | 720 | |
| — tối sau buổi chiều ở Nhị Hồ | 360 | Nhị Hồ đóng 17:30 ⇒ thực tế người đi về Huế ăn tối, không ăn gần thác |
| Chỉ xuất hiện khi | sở thích có "thiên nhiên" **và** chuyến ≥ 3 ngày | 144 / 240 khung của mỗi tổ hợp đó; chuyến 1–2 ngày 0 / 768 |
| Quán gần nhất trong bảng | 36–38 km (cụm Thủy Xuân) | 0 quán trong 10 km |

**Người dùng gặp bao nhiêu lần:** không đo được. Hệ thống không ghi log yêu cầu lịch của người dùng thật, và chưa có người dùng thật. Số ở trên là tỉ lệ trong mô phỏng, không phải tần suất thật.

Mốc so sánh: vùng biển / đầm có 2.040 bữa không quán (3.960 − 1.920), gần gấp đôi nam xa. Nếu sau này bổ sung quán thì nên ưu tiên vùng đó.

## Đề xuất (chưa làm, gửi nhóm)

- **Không cào quán** cho Bạch Mã / Nhị Hồ.
- **Tuỳ chọn, rẻ:** thêm vào bảng điểm lịch một dòng ghi chú ăn uống cho 2 điểm, lấy theo kho; thẻ bữa hiện dòng đó thay cho chỗ trống:
  - Bạch Mã: "mang đồ ăn trưa — trong vùng lõi không có quán";
  - Nhị Hồ: "chòi ăn uống ven hồ, đóng cửa 17:30".
  - Ước công: 1 trường dữ liệu + vài dòng ở `quan_lich.py` / `LichV2.jsx` + 1 test, 0 USD, khoảng 1 giờ.
  - Giữ sàn: không bịa quán.
  - Nếu không làm: thẻ bữa ở đó vẫn trống như hiện nay (không sai, chỉ thiếu lời nhắc).
- Bữa tối sau Nhị Hồ: bộ xếp đang gắn bữa tối với điểm cuối buổi chiều. Thấy ở đây nhưng chưa đếm ở chỗ khác. Không đề xuất sửa (hiện không hiện gì nên không gây sai).
