# Plan — thẻ khách sạn trong chat (bản 1, C, 12:17 15/11/2026)

Bước "khách sạn sau" của ảnh chat (User chọn hướng; A duyệt / làm / đạt thì bật). Đếm trước: `report_agent/2026-11-12_ra_khoang_cach/c_dem_ks_chat.md` (10 / 12 câu nêu tên cơ sở, 7 / 12 có cơ sở có ảnh). Mức nhẹ: ≈ 0,01 USD, chỉ giao diện.

## Đổi gì (chỉ giao diện; server, kho, chuỗi gửi model không đổi)
- **Dữ liệu:** dùng lại `GET /api/cho_o` đã có (137 cơ sở: tên, hạng, địa chỉ, ảnh, link Bản đồ / Tìm phòng; không giá / điện thoại / toạ độ). Giao diện tải một lần khi cần, giữ trong bộ nhớ.
- **`frontend/src/theKhachSan.js`** (hàm thuần, như `anhTraLoi.js`): `theKhachSan(turn, coSo)` ⇒ ≤ 3 cơ sở. Chỉ khi:
  - lượt xong, trả lời bằng kho (cùng điều kiện chung với ảnh);
  - **ít nhất một nguồn được trích là bài lưu trú** (`travel/services/Lưu trú ở Huế…`);
  - **tên lõi** của cơ sở (bỏ tiền tố loại hình) dài ≥ 2 chữ, có trong chữ trả lời, đứng thành từ riêng; giữ hoa / thường trừ chữ đầu (như ảnh chat);
  - nhiều tên khớp chồng nhau ⇒ lấy **tên dài nhất** (chặn "Villa Louise" trong "Villa Louise Beach").
  - Tối đa 3, theo thứ tự xuất hiện trong chữ.
- **`chat.jsx`:** dưới câu trả lời, sau ảnh (nếu có), một hàng **thẻ khách sạn**:
  - ảnh nếu có, không có ⇒ ô màu như trang Chỗ ở;
  - tên, hạng sao;
  - link **Bản đồ** / **Tìm phòng**, chỉ 2 gốc đã kiểm như ô Nơi ở;
  - một dòng "Theo danh mục, chưa kiểm giá / phòng trống".
- Ảnh chat (nơi / món) và thẻ khách sạn **tách riêng**: tổng tối đa 3 ảnh + 3 thẻ.

## Tiêu chí + cách đo (ghi trước)
| # | Tiêu chí | Đo |
|---|---|---|
| T1 | Lượt không trích bài lưu trú ⇒ 0 thẻ (mọi câu ảnh chat cũ giữ nguyên) | test node |
| T2 | Khớp tên lõi, ranh giới từ, tên dài nhất, ≤ 3, thứ tự xuất hiện; ca "Villa Louise" ↔ "Villa Louise Beach" ⇒ chỉ Beach | test node |
| T3 | 12 câu đã chạy (`hoi.jsonl`): 0 thẻ sai cơ sở (C đọc tay từng thẻ); báo số câu có thẻ, có ảnh | script 0 USD gọi chính `theKhachSan.js` |
| T4 | Người xem nhìn lại 100 % ảnh của thẻ sẽ hiện (ảnh đúng cơ sở, không quảng cáo / số điện thoại) | 1 agent con + C |
| T5 | Playwright 1440 + 390: 1 câu ≥ 2 thẻ; link đúng gốc + `noopener`; 0 lỗi console; 0 yêu cầu ra ngoài; không cuộn ngang | 1 lượt hỏi thật |

Test rộng 1 lần trước bàn giao. Không bộ kín.

## Tiền và công
≈ 0,002 USD (Playwright); đếm đã tốn 0,0083. Công ~2 giờ.

## Khi nào sai
- Model viết tên khác bảng (vd "Saigon Morin" ↔ "Sài Gòn Morin") ⇒ không thẻ. Thiếu thẻ, không sai thẻ.
- Danh mục lấy 12/11/2026; cơ sở có thể đổi ⇒ dòng "chưa kiểm".
- Câu nêu > 3 cơ sở ⇒ chỉ 3 đầu theo thứ tự trong chữ.

## Rà khung AI FDE (ngắn)
| Mục | Hiện trạng | Khớp / lệch |
|---|---|---|
| Có cần model không | Code khớp tên; model không chọn thẻ | khớp |
| Nguồn / đường ra mới | Không: `/api/cho_o` + ảnh tự host có sẵn; link chỉ 2 gốc, người dùng tự bấm | khớp |
| Chữ không tin cậy | Chữ model chỉ dùng để **so** tên; không dựng URL từ chữ | khớp |
| Rào hai chiều | T1 (không lưu trú ⇒ 0 thẻ) + T3 / T4 (0 thẻ / ảnh sai) | khớp |
