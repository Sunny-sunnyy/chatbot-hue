# Đếm trước khi xây: mục web cho ý thiếu + quán ăn trong lịch (C, 16:25 14/11/2026)

A duyệt cả hai lượt đếm, ngưỡng ghi trước trong tin của C. Tiền: 16 lượt Serper ≈ **0,016 USD** + 0 USD.

## (1) Mục web cho dòng ý thiếu — KHÔNG đổi, KHÔNG bỏ
- **Bộ:** 16 lượt có mục web của lượt đo `p9-web-y-thieu` (`data/web_y_thieu_2026-11-14/do_r.jsonl`): hỏi kèm 10 + 3 câu tự viết × 2.
- **Hiện tại:** mục web có thông tin dùng được ở **3 / 16** lượt; 16 / 16 có câu kiểu "chưa xác minh được".
- **Mức tốt nhất của câu tìm** (`data/dem_web_y_thieu_2026-11-14/`): tìm bằng chính dòng ý thiếu (đã có tên nơi), mỗi lượt lấy 5 kết quả. C đọc tay từng lượt, lượt nào có ≥ 1 đoạn trích đúng loại thông tin được hỏi thì tính:
  - **6 / 16** có ích: giá thuê thuyền phá Tam Giang; làng nón; karaoke × 2; đổi ngoại tệ × 2.
  - Bỏ các lượt lặp câu thì còn 4 / 13.
- **Đối chiếu ngưỡng:**
  - ≥ 6 / 16 ⇒ đổi câu tìm: chỉ chạm ngưỡng, và chỉ khi gửi chữ do **model** viết ra ngoài — trái quy ước D2 (chỉ chữ người dùng). Bản chỉ dùng chữ người dùng sẽ thấp hơn.
  - < 3 / 16 ⇒ bỏ tra web: không chạm (hiện tại 3 / 16).
- ⇒ **Giữ nguyên.** Không đủ lợi để xây cách tìm mới; cũng không đủ căn cứ để bỏ tra web.
- **Rủi ro thấy được:** một đoạn trích về "chương trình Tết" thực ra là của Tết năm trước. Mục web có thể nói chắc sai về năm ⇒ đã báo B (đang sửa kiểm cuối mục web) để thêm ca này vào bộ đo.

## (2) Quán ăn trong lịch — ĐẠT ngưỡng ⇒ plan mức nhẹ
- **Bộ:** 3.840 khung (mọi tổ hợp, cách của E / B; `xep_v2` trên main) ⇒ **22.680 bữa**.
  - Bữa trưa = cụm của điểm cuối buổi sáng; bữa tối = cụm của điểm cuối buổi chiều.
  - Script: `data/dem_quan_lich_2026-11-14/dem.py`; kết quả: `ket_qua.json`.
- **Nguồn quán:**
  - (a) quán kho có toạ độ đã gán cụm (`data/sua_kho_2026-11-12_an_gan/quan_theo_cum.json`). **Sửa 16:28 14/11/2026 (C tự bắt):** file này trộn 3 nguồn ⇒ chỉ **28** dòng `nguon == "kho"` là quán kho (bản đầu đếm cả 42 dòng là kho — sai). 4 dòng dữ liệu mở thành phố tính riêng; 10 dòng OSM bỏ, vì đã có trong bảng (b).
  - (b) bảng OpenStreetMap riêng cho lịch (`data/osm_quan_2026-11-12/bang_quan_osm_v1.json`, 428 quán trong cụm). Đây là bảng User chốt 13/11: JSON riêng, dòng do code viết, nhãn "chưa kiểm".
- **Kết quả** (bữa có ≥ 2 quán cùng cụm; số đã sửa):
  - chỉ quán kho: **33,5 %**;
  - kho + OSM: **74,7 %** (ngưỡng ≥ 50 % ⇒ vẫn đạt); thêm dữ liệu mở: 74,7 %.
  - Bản đầu ghi 74,7 % / 95,2 % là sai.
- **Chỗ yếu:**
  - quán kho chỉ có ở 3 cụm trung tâm: bờ nam 22, Kinh thành 5, An Cựu 1;
  - Thủy Xuân (27 % số bữa) và Kim Long chỉ có quán OSM (16 và 4 quán);
  - "đông — biển, đầm phá" (20 % số bữa) có 1 quán OSM ⇒ không đủ 2 quán; "nam xa" 0 quán.
  - ⇒ Ngoài trung tâm, quán gợi ý gần như toàn là quán OSM "chưa kiểm".
