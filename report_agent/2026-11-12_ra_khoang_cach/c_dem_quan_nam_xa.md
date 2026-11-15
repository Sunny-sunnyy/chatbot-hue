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

## Đã làm: ghi chú ăn uống (nhánh `p9-ghi-chu-an` @ `81e3aff`, A duyệt 15/11) — chờ E review

Viết 09:50 15/11/2026 (`date`).

**Đổi gì.** Bữa không chọn được quán và (điểm, bữa) có trong `GHI_CHU_AN` ⇒ server trả mục `quan: []` kèm `ghi_chu`. Thẻ bữa hiện câu đó; chữ chép / tải cũng có.
- `backend/llm/quan_lich.py`: `GHI_CHU_AN` có 3 câu, chữ theo kho (dò bằng `scripts/grep_kb.sh`): Bạch Mã trưa · Nhị Hồ trưa · Nhị Hồ tối. `an_uong` và `dong_chu` đọc từ đây.
- `frontend/src/LichV2.jsx` + `lkh.css`: thêm một `span.lkh-an-gc`. Chữ do server gửi, React tự thoát ký tự đặc biệt.
- Không đổi dữ liệu `data/`, cờ hay chuỗi gửi model: khối `an` không vào tin nhắn gửi model, test Q1 hiện có vẫn qua.

**Kiểm [đã chạy].**
- `tests/test_quan_lich.py`: 16 passed, 13 s. Có test mới: 2 điểm không có quán trong 2 km ⇒ ghi chú đúng bữa và vào chữ chép. Test sàn mô phỏng bỏ qua mục ghi chú và kiểm rằng mục đó thuộc `GHI_CHU_AN`.
- Cả `backend/tests` (có `--env-file`): **1048 passed, 265 s**.
- `vite build` qua.
- Playwright khổ 1440 trên server tạm cổng 8037 (cwd `/tmp/c_ga/backend`, đã tắt). Lịch 3 ngày + Thiên nhiên, 1 lần gọi model ≈ 0,0007 USD:
  - ngày 2 có 2 dòng ghi chú, 0 quán, các bữa khác vẫn 2 quán;
  - 0 lỗi console, 0 yêu cầu ra ngoài ⇒ DAT.
  - Ảnh `data/dem_quan_nam_xa_2026-11-15/anh/`, script `tools/pw_ghi_chu.py`.

**Điểm để reviewer xét.** Dòng tiêu đề vẫn là "Ăn tối gần Thác Nhị Hồ" trong khi ghi chú bảo về nơi nghỉ ăn tối, hơi ngược nghĩa. C giữ tiêu đề chung cho mọi thẻ; nếu E thấy cần, có thể đổi tiêu đề riêng cho mục có ghi chú.

**Tiền:** 1 lượt Playwright ≈ 0,0007 USD; bộ test đủ có vài lượt gọi thật (chưa tách số).

**Sau review E (`e_review_ghi_chu_an.md`, ready 0/0/2) — nhánh @ `e001cb2`:** m-1 câu Bạch Mã thu về "khu Ngũ Hồ và đỉnh núi" như kho; m-2 bỏ câu trưa Nhị Hồ (0 / 3.840 khung) ⇒ còn 2 câu. Test file 16 passed.
