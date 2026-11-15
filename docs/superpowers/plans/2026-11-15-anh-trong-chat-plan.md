# Plan — ảnh trong chat theo tên nơi / món (bản 1, C, 11:38 15/11/2026)

User chốt 15/11 (qua A): món + nơi trước, khách sạn sau; ảnh giữ file + bảng mã bài (`anhBai.js`). Mức nhẹ: 0 USD, không đổi kiến trúc ⇒ plan 1 trang, A duyệt, code, đo 1 lượt, 1 review cả nhánh. Đếm trước: `report_agent/2026-11-12_ra_khoang_cach/c_dem_anh_chat.md`.

## Đổi gì (chỉ giao diện; server, kho, chuỗi gửi model không đổi)
- **Nguồn dữ liệu:** sự kiện `sources` của server đã là **nguồn được trích**, đúng thứ tự trích (`api/routes/chat.py:556`, `trace.cited`). Mỗi nguồn có `bai_id` và `title`.
- **`frontend/src/anhTraLoi.js`:** trả **danh sách** `[{anh, baiId, ten}]` (≤ 3) thay cho một ảnh.
  - Điều kiện chung giữ nguyên: lượt xong, trả lời bằng kho, không từ chối / web / lịch / hỏi lại.
  - Mọi nguồn thuộc **một** bài ⇒ như hiện nay: 1 ảnh, không cần tên trong chữ.
  - Nguồn thuộc **≥ 2** bài ⇒ xét từng bài theo thứ tự trích; lấy bài thoả cả bốn điều kiện:
    - loại "một nơi / món" (`LOAI_MOT_NOI`);
    - có ảnh chắc (không `kc`);
    - tên bài (bỏ phần trong ngoặc) dài **≥ 2 chữ**;
    - tên đó **xuất hiện trong chữ trả lời** (so chữ thường, chuẩn NFC).
  - Lấy tối đa 3 bài.
  - Không dùng "tên gọi khác": giao diện không có dữ liệu này; theo đếm trước chỉ mất 1 / 41 câu.
- **`chat.jsx` `AnhTraLoi`:** 1 ảnh ⇒ như cũ. 2–3 ảnh ⇒ một hàng ảnh nhỏ; dưới mỗi ảnh là **tên nơi** (ý E: so sánh 2 quán không thành ảnh quán A cạnh chữ quán B). Không chữ ghi công. Bấm ảnh mở bài.
- CSS cho hàng ảnh: 390 px xuống dòng, không cuộn ngang.
- Không làm khách sạn ở nhánh này: 0 / 154 câu Golden nhắc khách sạn ⇒ chưa có gì để đo; làm sau theo lời User.

## Tiêu chí + cách đo (ghi trước)
| # | Tiêu chí | Đo |
|---|---|---|
| T1 | Lượt nguồn chỉ một bài ⇒ kết quả giống hệt luật cũ (cùng ảnh); mọi ca "không ảnh" của test cũ vẫn không ảnh | `test_anh_tra_loi.py` (node thật, `anhBai.js` thật) |
| T2 | ≥ 2 bài ⇒ chỉ bài đã trích + đúng loại + ảnh chắc + tên ≥ 2 chữ có trong chữ; ≤ 3; đúng thứ tự trích; mỗi ảnh có `ten` | test |
| T3 | Mô phỏng 154 câu trả lời đã lưu (0 USD; nguồn trích dựng từ `[n]` ⇒ đoạn top 10): báo số câu có ≥ 1 ảnh (mốc luật cũ 77), số ảnh, số câu 2–3 ảnh | script `data/anh_chat_2026-11-15/tools/mo_phong.py` gọi chính `anhTraLoi.js` qua node |
| T4 | **Người xem nhìn lại 100 % ảnh MỚI sẽ hiện** (ước ~41 câu, ~60 ảnh): ảnh đúng nơi / món câu trả lời đang nói; sàn **0 ảnh sai nơi** | 1 agent con + C nhìn lại (luật chọn ảnh) |
| T5 | Playwright 1440 + 390: một câu ≥ 2 ảnh hiện tên dưới ảnh, link mở bài, 0 lỗi console, 0 yêu cầu ra ngoài, không cuộn ngang | 1 lượt hỏi thật (≈ 0,0005 USD), sau khi B báo xong đo độ trễ |

Test rộng `backend/tests` 1 lần trước bàn giao. Không bộ kín (code quyết, tất định).

## Tiền và công
≈ 0,001 USD (Playwright). Công ~2 giờ (hàm + giao diện + test + mô phỏng + nhìn lại ảnh).

## Khi nào sai
- Tên bài có trong chữ nhưng câu không nói về nơi đó (vd tên chợ nằm trong địa chỉ một quán). Rào "bài phải là nguồn được trích" giảm, không hết. T4 đo.
- Câu so sánh > 3 nơi ⇒ chỉ 3 ảnh đầu theo thứ tự trích.
- Model viết tên khác bài (viết tắt, không dấu) ⇒ không ảnh. An toàn: thiếu ảnh, không sai ảnh.

## Rà khung AI FDE (ngắn)
| Mục | Hiện trạng | Khớp / lệch |
|---|---|---|
| Có cần model không | Code khớp tên, model không chọn ảnh | khớp |
| Nguồn / đường ra mới | Không: ảnh tự host sẵn có, bảng mã bài sẵn có | khớp |
| Chữ không tin cậy | Chữ model chỉ dùng để **so** tên; không dựng URL từ chữ; ảnh chỉ lấy từ `anhBai.js` theo `bai_id` của server | khớp |
| Rào đo hai chiều | T1 (một bài giống hệt) + T4 (0 ảnh sai) | khớp |
