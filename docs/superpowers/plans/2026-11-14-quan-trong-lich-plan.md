# Plan (mức nhẹ): quán ăn gợi ý trong lịch bản 2 — C

Cập nhật: 16:26 14/11/2026 (C). Đếm trước khi xây **đạt** (số sửa 16:28 14/11/2026): `report_agent/2026-11-12_ra_khoang_cach/c_dem_truoc_khi_xay.md` (2) — **74,7 %** bữa có ≥ 2 quán cùng cụm (kho + OSM), **33,5 %** chỉ quán kho (quán kho chỉ có ở 3 cụm trung tâm; Thủy Xuân / Kim Long chỉ có OSM). Bản đầu ghi 95,2 / 74,7 % là sai (đếm nhầm 14 dòng OSM / dữ liệu mở là quán kho).
Theo chốt của User 13/11: quán cho lịch lấy từ **bảng JSON riêng** (quán kho đứng trước, OSM lấp chỗ), dòng quán **do code viết**, không Qdrant, không vào kho chính.
Mức nhẹ: ≤ 0,05 USD, không đổi kiến trúc (cùng khuôn với "nơi ở gợi ý" đã chạy) ⇒ A đọc rồi duyệt, một review cả nhánh.

## Người dùng thấy gì
Mỗi ngày trong lịch có hai dòng do code viết:
- "Ăn trưa gần <điểm cuối buổi sáng>: <quán 1> · <quán 2>";
- "Ăn tối gần <điểm cuối buổi chiều>: …".

Cách hiện mỗi quán:
- **Quán kho:** tên + loại (quán ăn / cà phê) + link "Đọc bài".
- **Quán OSM:** tên + loại + nhãn "từ bản đồ mở, chưa kiểm" + link Google Maps do code dựng từ toạ độ.
- **Không hiện:** giá, giờ mở cửa, số điện thoại. Bảng OSM chỉ 27 % quán có giờ, và không quán nào có ngày kiểm.
- Cụm không đủ 1 quán ⇒ không có dòng. Không đoán, không lấy quán cụm khác.

## Đổi gì
- `data/phase_9/lich_trinh/bang_quan_lich_v1.json` (private): gộp 28 quán kho có toạ độ + 4 quán dữ liệu mở thành phố (nhãn riêng của nguồn đó) + 428 quán OSM trong cụm. Mỗi quán: tên, loại, cụm, toạ độ, nguồn (mã bài kho | link OSM). Dựng bằng script từ hai bảng có sẵn, không gõ tay.
- `backend/llm/quan_lich.py` (mới):
  - **nạp + kiểm lúc khởi động** (chặn tên > 80 ký tự / ký tự điều khiển / link trong tên — như chốt 13/11);
  - **chọn quán:** ≤ 2 quán cùng cụm cho mỗi bữa, gần điểm nhất theo toạ độ, quán kho trước, không lặp một quán trong cả chuyến;
  - **viết dòng chữ** cho nút chép.
- `len_ke_hoach.py` / `lich_trinh_v2.py`: cờ bật ⇒ gán `lich["an"]` sau `dung_lich` (cả lượt sửa lịch); `ghep_chu` thêm dòng. **Không vào tin nhắn gửi model.**
- `LichV2.jsx` + `lkh.css`: dòng "Ăn trưa / Ăn tối" giữa các buổi. Link chỉ nhận đúng gốc Google Maps / mã bài có trong danh sách.
- Cờ `quan_lich` (cần `len_ke_hoach_v2` + bảng) — **tắt** tới khi đạt.

## Đo (theo luật "đo phần đổi")
- **3.840 khung, mô phỏng 0 USD:**
  - 0 quán ngoài bảng;
  - 0 quán khác cụm;
  - 0 quán lặp trong một chuyến;
  - khoảng cách quán ↔ điểm: ghi trung vị + p95 (chưa đặt sàn — ghi số trước, A xem);
  - tỉ lệ bữa có dòng ≈ 95 % như lượt đếm.
- **Chuỗi gửi model:** giống byte dù có hay không `lich["an"]` (test). Không chạy bộ 228.
- **Người xem 10 lịch** (agent con ngữ cảnh mới; có ngày đi / không, có trẻ em, cụm biển, cụm Thủy Xuân): ≥ 9 / 10 "quán hợp chỗ, nhãn đúng nguồn, không có số / giờ lạ".
- **Playwright 1 khổ** trên bản build thật: dòng hiện, link đúng gốc, 0 lỗi console.
- **Test:** file chạm, có / không khoá.
- **Tiền:** vài lượt xếp lịch thật cho Playwright ≈ 0,003 USD.

## Bảng AI FDE (rút gọn)
| Mục | Hiện trạng / đề xuất | Khớp / lệch |
|---|---|---|
| Code ↔ model | code chọn quán + viết dòng; model không thấy tên quán OSM | khớp ("con số, danh sách bắt buộc ⇒ code") |
| Dữ liệu ngoài | OSM: chữ người khác viết ⇒ coi là dữ liệu. Chặn link / ký tự điều khiển trong tên; chỉ hiện tên + loại | khớp (chốt 13/11) |
| Đường ra ngoài | link Maps / Đọc bài chỉ mở khi người dùng bấm; không gửi gì thêm ra ngoài | khớp |
| Nói chắc sai | không giờ / giá / điện thoại; nhãn "chưa kiểm" cho mỗi quán OSM | khớp |
| Phục hồi | bảng hỏng ⇒ không khởi động (như bảng nơi ở); cụm thiếu quán ⇒ không dòng | khớp |

## Câu cần A / User chốt trước khi code
- **Dòng ghi nguồn OSM.** Giấy phép ODbL đòi ghi "© OpenStreetMap contributors"; chốt 13/11 có dòng này. Nhưng User 14/11 bỏ mọi chữ ghi công trên giao diện (khi đó nói về ảnh).
  - **C đề xuất:** giữ nhãn "từ bản đồ mở, chưa kiểm" cạnh từng quán OSM — nhãn này là cảnh báo dữ liệu, không phải ghi công. Ghi "© OpenStreetMap contributors" một lần, chữ nhỏ cuối khối quán, như bản đồ lịch đã làm.
  - Nếu User không muốn dòng © này thì bỏ; nhãn "chưa kiểm" vẫn giữ.
