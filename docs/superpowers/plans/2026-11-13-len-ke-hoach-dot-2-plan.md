# Plan — "Lên kế hoạch" đợt 2: bản đồ + ảnh trong lịch (mức nhẹ)

Người viết: C · bản 1 · 21:37 13/11/2026 (`date`) · **mức nhẹ** (≤ 0,05 USD, không đổi kiến trúc) ⇒ A đọc rồi duyệt, không review plan; một review cả nhánh.
**Trạng thái:** A đọc + DUYỆT 21:38 13/11/2026 (mức nhẹ, bản sha `d0f7bc56add0` tính trước dòng này). (A) bản đồ làm ngay; (B) ảnh chờ User duyệt phiếu ảnh.
Căn cứ: spec `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md` bản 3.3 §3.3, §4 cột "Đợt 2", §6 dòng 2 · plan bản đồ `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md` (Leaflet 1.9.4, CSP theo cờ, Q-M1–Q-M6) · code nhánh `p9-len-ke-hoach-v2` `49daaa7`.
Đếm trước khi xây: không cần — đây là cam kết của spec đã duyệt; hiện trạng đo được: lịch v2 trả `anh: null`, `toa_do: null` ở **mọi** mục (`lich_trinh_v2.dung_lich`), giao diện `LichV2` không vẽ bản đồ (đường lịch cũ có, cờ `ban_do_lich` tắt).

## Hiện trạng (đã kiểm 13/11, 0 USD)
- Bảng toạ độ đang trỏ (`diem_toa_do_v5.json`) có **18 / 34** điểm của bảng v8; bản nháp `data/phase_11/ban_do/diem_toa_do_v6_nhap.json` phủ thêm 11 ⇒ 29; **5 điểm thiếu hẳn** (Duyệt Thị Đường, hai điểm Lê Bá Đảng, Bảo tàng Hồ Chí Minh, Ca Huế trên sông Hương).
- `BanDoLich.jsx` đã có: chunk riêng tải lười, ghim số theo thứ tự, nút chọn từng ngày (= một lớp / ngày), danh sách điểm kèm link Maps.
- Phiếu ảnh: 21 dòng "ổn" + 4 ảnh thay **chưa ai nhìn** + 2 điểm không có ảnh thay (`phieu_anh_2026-11-13_ban2.md`, `kiem_anh_bang_mat_2026-11-13.md`) ⇒ tối đa **25 / 34 = 74 %** điểm có ảnh; sàn spec ≥ 70 % ⇒ chỉ còn biên **1 ảnh** (2 ảnh bị loại ⇒ 23 / 34 = 68 % ⇒ chưa bật).

**Ghi chú A (21:38 13/11/2026, không đổi tiêu chí):** agent con đã nhìn 4 ảnh thay — #15, #19, #27 ổn; #23 bị loại ⇒ tối đa **24 / 34** điểm có ảnh, đúng sàn ≥ 24 (0 biên): một ảnh bị User loại ⇒ phần (B) merge cờ tắt.

## (A) Bản đồ — làm ngay
| Bước | Ai | Việc |
|---|---|---|
| A0 dữ liệu (0 USD) | C | `data/phase_9/lich_trinh/diem_toa_do_v7.json` (private) = v5 + 11 dòng v6 (C đọc tay từng dòng: tên ↔ nguồn) + 5 điểm thiếu tra nguồn công khai (OSM / trang chính thức, ghi nguồn + ngày); không tìm được ⇒ `null` + lý do. Kiểm bằng script: 34 id ⊂ v8, toạ độ trong khung Huế, mỗi dòng có nguồn; biên bản ghi "số dòng ⇒ số điểm". |
| A1 code | B | `dung_lich` điền `toa_do` từng mục từ bảng khi `ban_do_lich` bật (cờ tắt ⇒ `null` như nay); mục "nghỉ" không toạ độ. `LichV2` vẽ `BanDoLich` dưới lịch từ mục có toạ độ (thứ tự = thứ tự mục trong ngày); mục thiếu toạ độ ⇒ dòng "chưa có vị trí trên bản đồ" + link Maps sẵn có, **không ghim đoán**; ghim mang màu theo ngày (lớp CSS, 0 gói mới). CSP như plan bản đồ (bật ⇒ `img-src` thêm `data:` + `tile.openstreetmap.org`; tắt ⇒ giống byte). Toạ độ **không** vào chuỗi gửi model. |

**Tiêu chí ghi trước (A):**
- **Luôn** (pytest + mô phỏng 960 khung của đợt 1, 0 USD): mọi ghim là một mục tham quan / buổi tối **của lịch**; số ghim / ngày = số mục có toạ độ; thứ tự ghim = thứ tự mục; 0 ghim cho mục `toa_do: null`; mọi toạ độ = đúng dòng bảng theo `id_diem`; cờ tắt ⇒ đối tượng `lich` giống byte bản hiện tại; chuỗi gửi model giống byte cờ bật / tắt (một test trên lượt biểu mẫu — không chạm phần dựng chuỗi nên không chạy Q1 228).
- **Sàn:** điểm của bảng thiếu toạ độ ≤ 3, mỗi điểm có lý do ở biên bản A0.
- **Hệ thống thật** (bản build FastAPI, Playwright 1440 + 390, cờ bật trên server thử, 3 lịch qua biểu mẫu: 1 · 3 · 5 ngày): Q-M1–Q-M6 của plan bản đồ (0 lỗi CSP / console; chỉ host tile; câu không lịch ⇒ 0 yêu cầu tile, chunk bản đồ không tải; chữ câu hỏi không có trong URL / header gửi host tile) + đủ ghim đúng thứ tự ở mỗi ngày. **Cỡ:** bundle chính tăng ≤ 3 KB gzip; chunk bản đồ tăng ≤ 2 KB.

## (B) Ảnh — CHỜ User duyệt phiếu ảnh bản 2 (và agent con nhìn 4 ảnh thay)
| Bước | Ai | Việc |
|---|---|---|
| B0 dữ liệu (0 USD) | C | `data/phase_9/lich_trinh/bang_anh_v1.json`: `id_diem` ⇒ file, tác giả, giấy phép, link trang ảnh — **chỉ** dòng User duyệt + người nhìn "ổn"; tải bản 800 px từ Commons một lần (chậm, ≥ 10 s / yêu cầu — lần trước bị 429), thu nhỏ bằng công cụ sẵn có trong `.venv` / máy, mỗi ảnh ≤ 80 KB; ảnh #7 cắt dải xanh đáy. |
| B1 code | B | `dung_lich` điền `anh` = `{src, tac_gia, giay_phep, trang}` theo `id_diem` khi cờ mới `anh_lich` bật; điểm không có dòng ⇒ `null` ⇒ không ảnh (không ảnh thay). Ảnh nằm trong `frontend/public/anh/lich/` như bộ ảnh cổng (CSP không đổi); dưới ảnh một dòng tác giả + giấy phép + link trang ảnh. |

**Tiêu chí ghi trước (B):** **Luôn:** mỗi ảnh hiện ra có trong bảng ảnh, đúng `id_diem`, có dòng tác giả + giấy phép; 0 ảnh từ host ngoài (`src` bắt đầu `/anh/lich/`); CSP giống byte. **Sàn (spec):** ≥ 70 % điểm của bảng (≥ 24 / 34) có ảnh ⇒ bật; dưới ⇒ merge cờ tắt. **Cỡ:** thư mục ảnh lịch ≤ 2,5 MB; bundle JS không đổi > 1 KB. **Người xem** (spec §6): một người (agent con xem được ảnh) xem 10 lịch ⇒ ảnh đúng điểm 10 / 10.

## Chung
- **Nhánh:** dựng **trên** `p9-len-ke-hoach-v2` (thẻ lịch v2 ở đó); (A) và (B) mỗi phần một commit, merge cùng nhánh đợt 1 hoặc sau, một review cả nhánh (E). Người code B, người dựng dữ liệu C, người kiểm E.
- **File chạm:** `backend/llm/lich_trinh_v2.py` (`dung_lich`) · `backend/llm/assistant.py` (nạp toạ độ / ảnh cho `bang_lich_v2`) · `backend/config/settings.yaml` (`lich_trinh_toa_do` ⇒ v7; cờ `anh_lich: false`, `lich_trinh_bang_anh`) · `frontend/src/chat.jsx` (`LichV2`) · `frontend/src/BanDoLich.jsx` (màu theo ngày) · CSS · `frontend/public/anh/lich/` · danh sách chừa Docker · `backend/tests/test_len_ke_hoach_v2.py`, `test_ban_do_lich.py`, `test_static_ui.py`.
- **Tiền:** chỉ lượt Playwright qua biểu mẫu thật ≈ 3–6 lượt × 0,0004 ≈ **0,003 USD**; dữ liệu + mô phỏng 0 USD. **Trần 0,05.** Đo Playwright là việc nặng ⇒ không chạy trùng lượt đo tốc độ của người khác.
- **Dừng:** toạ độ hai nguồn lệch > 300 m ⇒ ghi chú, không ghim, báo A · ảnh dưới sàn ⇒ không bật (không hạ ngưỡng) · một "Luôn" sai ⇒ sửa code, không sửa tiêu chí.

## Rà khung AI FDE (ngắn)
| Mục | Đợt 2 | Khớp |
|---|---|---|
| Cần model? | không — ảnh, toạ độ, thứ tự ghim đều do code gắn theo `id_diem` | khớp |
| Công cụ mới cho model | không | khớp |
| Đường ra mới | không mới so với plan bản đồ đã duyệt (tile OSM từ trình duyệt, chỉ khi cờ bật); ảnh tự host | khớp |
| Dữ liệu ngoài vào sản phẩm | ảnh giấy phép mở có phiếu User duyệt; toạ độ có nguồn từng dòng | khớp |
| Phục hồi | mỗi phần một cờ; thiếu toạ độ / ảnh ⇒ ẩn phần đó, lịch vẫn hiện | khớp |
| Dữ liệu cá nhân | không thêm; toạ độ ghim gửi host tile = vùng điểm tham quan, không chữ câu hỏi (Q-M6) | khớp |
