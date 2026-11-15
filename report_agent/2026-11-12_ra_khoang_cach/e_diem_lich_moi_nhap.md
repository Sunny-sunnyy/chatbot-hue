# Bảng nháp: thêm nơi vào bảng điểm lịch (E · 13:28 15/11/2026, `date`) — CHỈ CHUẨN BỊ, chưa sửa bảng đang chạy

A giao (chờ User chọn). C chọn 10 nơi (`data/diem_lich_moi_2026-11-15/c_chon_10.md`); E gom căn cứ từng trường; **B review chéo** bảng nháp.
Main vẫn trỏ `diem_v8` (34 điểm). Tiền ≈ 0,05 USD (Serper tìm 32 + Places 15 lượt; Codex 1 lượt = gói ChatGPT; WebFetch kiểm 6 trang).

## Kết quả
- **7 / 10 nơi đủ căn cứ ⇒ vào nháp:** chùa Từ Hiếu, cầu Trường Tiền, đèo Hải Vân, chợ Bến Ngự, làng nón Tây Hồ, nhà vườn An Hiên, đầm Lập An.
- **3 nơi không đưa vào** (`bo_ra.json`): Cồn Hến, chợ Tây Lộc — **không tìm được nguồn ghi thời lượng tại chỗ** (Serper 2 vòng + Codex "KHÔNG CÓ"), không ước; Suối Voi — **chính bài kho cảnh báo** nơi này chưa vận hành đón khách bài bản ⇒ không xếp khách tới.
- Nạp thử bằng chính `nap_bang_v2` (v8 + nháp = 41 điểm): **đúng khuôn**.
- Mô phỏng 3.840 khung (`tools/mo_phong.py`, **cùng 4 ngày đi như C** ⇒ số mốc v8 khớp bảng của C): **0 lỗi `kiem_khung_v2`**; cả 7 điểm mới đều được xếp (136–740 lượt / điểm); % điểm ban ngày phải lấy NGOÀI sở thích (khung chọn một sở thích):

| Sở thích | v8 | v8 + nháp | Buổi sáng / chiều trống (v8 ⇒ nháp) |
|---|---|---|---|
| ẩm thực | 56,4 % (868 / 1.540) | **44,0 %** (680 / 1.544) | 0 ⇒ 0 |
| chụp ảnh | 51,7 % (808 / 1.564) | **36,8 %** (564 / 1.532) | 0 ⇒ 0 |
| thiên nhiên | 24,4 % (352 / 1.444) | **17,6 %** (258 / 1.462) | **72 ⇒ 64** (còn trống: bỏ Suối Voi) |
| lễ hội / nghệ thuật | 39,0 % | 39,1 % (kho không có nơi để bù — giới hạn) | 0 ⇒ 0 |
| di tích | 0 % | **0 %** | 0 ⇒ 0 |

(Bản đầu của report dùng mô phỏng không ngày đi ⇒ thiên nhiên 23,2 ⇒ 16,6 %; C phát hiện lệch mốc ⇒ E chạy lại đúng cách của C. Số trên là bản đúng.)

## Căn cứ từng trường (chi tiết: `diem_moi_nhap.json`, mỗi trường có `*_can_cu`)
- **Thời lượng** — kho không ghi ở cả 7 nơi ⇒ lấy web, **E tự mở trang kiểm câu trích** (WebFetch / tải trang):
  - "ngắn" (≤ 90 phút): Từ Hiếu (30–45 phút), Trường Tiền (20–40 phút), Hải Vân (30–45 phút ở đỉnh / Hải Vân Quan), An Hiên (45–90 phút).
  - "nửa buổi": Bến Ngự (~2 giờ), Tây Hồ (2–3 tiếng), Lập An (2–3 giờ).
  - Riêng nguồn Bến Ngự trả 403 với E; Codex đã mở được trang (có trong `url_da_mo.txt`). ⇒ B nên coi là **một nguồn, E chưa tự đọc**.
- **Giờ mở:** từ kho ở Bến Ngự, An Hiên; web ở Hải Vân Quan (07:00–17:30, trang ghi kiểm 10/2026). Từ Hiếu: kho ghi không niêm yết, 3 nguồn web lệch nhau ⇒ **không đặt giờ** (chỉ "ban ngày"). Còn lại mở tự do theo kho.
- **Trong nhà / ngoài trời:** 5 nơi có dòng kho tả (nhãn `kho`). **Từ Hiếu, Tây Hồ là `uoc`** — kho chỉ tả hoạt động (tản bộ trong khuôn viên; đường làng). Bảng v8 hiện cũng có 13 / 34 điểm `uoc` ở trường này.
- **Toạ độ / cụm:** Serper Places, khớp tên. Cụm = tâm cụm gần nhất (code). Cần B soát: **Tây Hồ** dùng toạ độ chùa làng làm đại diện làng (Places không có điểm "làng nón"), và ra cụm `an_cuu` vì gần nhất (~6 km), dù làng ở phía đông; **Hải Vân, Lập An** ra `nam_xa` (đi trong ngày, cụm xa) — đúng ý C.
- **Đoạn mô tả:** chunk của chính bài, top 1 khi tìm bằng tên.
- **Ảnh lịch:** 6 / 7 có ảnh Khám phá chắc (không `kc`) ⇒ khi xây sẽ chép sang `/anh/lich/`. Tây Hồ không có ảnh (8 bài trống đang chờ User).

## Khi User chọn xây
1. B review nháp xong ⇒ dựng `diem_v9` = v8 + nháp, toạ độ v8 + ảnh lịch v3 (chép 6 ảnh), `settings.yaml` trỏ bảng mới; nhánh riêng.
2. Đo: mô phỏng 3.840 khung đủ sàn hiện có + bộ lịch 20 / 12 đã thấy (có phí nhỏ; lịch đổi ở mọi khung chạm điểm mới).
3. Không bộ kín (code xếp, không đổi lời dặn).

## Sau review B (`b_review_diem_lich_moi.md`: ready, 3 minor) — 13:32 15/11/2026 (`date`)
- m-1 Bến Ngự: căn cứ sửa đúng sự thật — **1 nguồn, Codex mở được, E và B đều bị 403 ⇒ chưa tự đọc**. Tìm nguồn thứ hai (Serper 2 câu, đọc nội dung trang) không ra. Giữ "nửa buổi" kèm cờ; **User quyết giữ / bỏ điểm này** khi duyệt xây (bỏ ⇒ 6 điểm).
- m-2 Tây Hồ: `vi_tri_can_cu` ghi rõ cụm `an_cuu` là tâm gần nhất (~3,5–4 km) nhưng điểm gần nhất của cụm ~6 km, làng ở phía đông.
- m-3 Hải Vân: giờ Hải Vân Quan ghi "1 nguồn".
- Chỉ đổi chữ căn cứ; giá trị bảng không đổi; nạp lại `nap_bang_v2` đúng khuôn (41 điểm).
