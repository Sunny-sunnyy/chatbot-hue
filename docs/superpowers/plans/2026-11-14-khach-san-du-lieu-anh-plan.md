# Plan — dữ liệu + ảnh khách sạn, sửa cách chọn ≤ 5 cơ sở · B · 17:58 14/11/2026

A giao theo ưu tiên mới của User (17:50 14/11/2026: dữ liệu, ảnh khách sạn phải đầy đủ; vẫn không nói giá phòng). Mức nhẹ: plan 1 trang ⇒ A duyệt ⇒ code ⇒ đo 1 lượt ⇒ C review cả nhánh.

## Đếm trước khi xây (0 USD, đã chạy)
- Bảng 140 cơ sở (`data/luu_tru_2026-11-14_lich/bang_luu_tru_lich.json`): tên, hạng, địa chỉ, khu, nguồn có đủ 140 / 140. **Mô tả 0 / 140 · ảnh 0 / 140 · link riêng 0 / 140** (chỉ link tìm Booking do code dựng). Toạ độ: ước mức con đường (~1 km) 117, không có 23 (cả 10 cơ sở ven biển).
- Cách chọn hiện hành, mô phỏng 3.840 khung (`data/khach_san_2026-11-14/tools/dem_chon.py`): **lỗi thật** — trong một mức hạng xếp theo tên (abc) ⇒
  - **5 sao xuất hiện 0 / 6.108 lượt** ở mức cao cấp (luôn hai khách sạn 4 sao đầu bảng chữ cái); **3 sao 0 lần**;
  - chỉ 16 / 140 cơ sở từng được gợi ý; 72 % lịch (2.219 / 3.072) nhận cùng một bộ 5.

## Làm gì (3 phần, một nhánh `p9-khach-san` từ main)
1. **Sửa cách chọn (code, 0 USD)** `backend/llm/luu_tru_lich.py` `chon_co_so`: trong mỗi mức, lấy lần lượt từng hạng, hạng cao trước (mức cao cấp: 1 × 5 sao + 1 × 4 sao khi có; mức giữa: 1 × 3 sao + 1 × 2 sao; mức thấp: 1 sao trước đạt chuẩn); trong cùng hạng: cùng cụm có nhiều điểm nhất trước ⇒ có ảnh trước ⇒ theo tên (tất định). Vẫn ≤ 5, vẫn một khu, vẫn không giá.
2. **Dữ liệu (Serper, ≈ 0,15 USD)**:
   - Serper Places `"<tên>, <địa chỉ>, Huế"` cho 140 cơ sở ⇒ toạ độ (chỉ nhận khi tên khớp sau bỏ dấu / chữ "khách sạn" và điểm cách toạ độ ước ≤ 3 km hoặc cùng khu); ghi `toa_do`, `toa_do_nguon`. Không lấy số sao / đánh giá / giá / điện thoại.
   - **Mô tả ngắn do code viết từ trường đã có** (hạng + loại hình + đường + khu + cụm gần, vd "Khách sạn 4 sao trên đường Lê Lợi, khu trung tâm bờ nam sông Hương") — không model, không ý ngoài nguồn, **không tính từ** ("sang trọng", "yên tĩnh"… — A 14/11).
   - Link: link Google Maps theo toạ độ (cùng mẫu link bản đồ của lịch); giữ link tìm phòng Booking. Website riêng của cơ sở: KHÔNG làm đợt này (khó kiểm đúng trang).
3. **Ảnh (Serper Images, ≈ 0,14 USD) — cách v3**: truy vấn tên + số nhà + đường + "Huế"; 5 ứng viên / cơ sở ⇒ tấm ghép ⇒ **2 agent con chọn độc lập** (brief theo `BRIEF_CHON_ANH_V3.md`, luật riêng: ảnh mặt tiền / sảnh / phòng của ĐÚNG cơ sở, đối chiếu biển tên hoặc tiêu đề trang; ảnh chung chung / khách sạn khác cùng tên ở tỉnh khác ⇒ không chọn) ⇒ chỉ nhận khi 2 lượt cùng chọn; một lượt "vừa" ⇒ `kc`. Ảnh thu nhỏ vào `frontend/public/` như ảnh lịch; giao diện thẻ "Nơi ở gợi ý" hiện ảnh nhỏ + mô tả ngắn; **0 chữ ghi công**.

## Tiêu chí (ghi trước khi đo)
- **Luôn (3.840 khung, 0 USD):** mọi luật "Luôn" của test lưu trú hiện hành vẫn đạt (đúng khu, ≤ 5, có nhãn, 0 link ngoài mẫu); **5 sao xuất hiện ở ≥ 80 % lịch khu trung tâm có mức cao cấp trong ≤ 5** (mẫu số ghi rõ trong report; bảng có 5 cơ sở 5 sao ở trung tâm); **3 sao ≥ 80 %** (khi có); số cơ sở khác nhau chỉ báo, không đặt sàn (khách cần 5 gợi ý tốt cho khu của mình, không cần mỗi lịch một bộ khác).
- **Dữ liệu:** toạ độ Places nhận ≥ 100 / 140 (còn lại giữ toạ độ ước, ghi rõ); 0 cơ sở bị đổi khu vì toạ độ mới (lệch khu ⇒ không nhận, liệt kê); mô tả 140 / 140.
- **Ảnh:** báo số nhận / `kc` / trống thật (không đặt sàn — thà trống còn hơn sai); B mở xem 10 ảnh nhận ngẫu nhiên, 0 sai cơ sở; nếu ≥ 1 sai ⇒ báo A trước khi merge.
- **Q1:** khối nơi ở không vào tin nhắn gửi model (test hiện có) ⇒ chuỗi gửi model giống byte; không cần lượt có phí cho câu trả lời.
- **UI:** Playwright 1440 + 390 trên bản build: thẻ có ảnh, mô tả, link Maps + Tìm phòng đúng gốc, 0 lỗi console, 0 chữ ghi công.
- Test chạm (`test_luu_tru_lich.py`) + test rộng một lần trước bàn giao.

## Tiền + thời gian
≈ 0,30 USD (Places 140 + Images 140 lượt × 0,001; agent con: quota Claude). Trần đợt 0,40 USD. ~2–3 giờ.

## Không làm (đợt này)
Collection Qdrant mới (chưa có tính năng cần) · ghi kho bài khách sạn mới (5 bài lưu trú đã có) · website riêng · đánh giá / số sao từ Google · giá.
