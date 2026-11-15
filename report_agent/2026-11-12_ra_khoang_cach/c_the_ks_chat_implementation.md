# Thẻ khách sạn trong chat — implementation (C, 15/11/2026)

Plan `docs/superpowers/plans/2026-11-15-the-khach-san-chat-plan.md` (sha `1952c39cfc46`, A duyệt). Nhánh `p9-the-ks-chat` @ `2d41e08` (worktree `/tmp/c_ks`; lần commit đầu bị hook chặn vì 1 dòng test chép tiêu đề bài kho — đã sửa). Đếm trước `c_dem_ks_chat.md`.

## Đổi gì (chỉ giao diện)
- `frontend/src/theKhachSan.js` (hàm thuần mới): `theKhachSan(turn, coSo)` ⇒ ≤ 3 cơ sở.
  - Chỉ khi trả lời bằng kho và có nguồn trích là bài `travel/services/Lưu trú ở Huế…`.
  - `tenLoi`: bỏ tiền tố loại hình, thêm bản bỏ "Huế" cuối nếu còn ≥ 2 chữ. Khớp bằng `tenKhop` của ảnh chat: ranh giới từ, giữ hoa / thường trừ chữ đầu.
  - Tên khớp nằm trọn trong một tên khớp dài hơn ⇒ bỏ.
  - Theo thứ tự xuất hiện trong chữ.
- `chat.jsx` `TheKhachSan`:
  - tải `/api/cho_o` **một lần**, chỉ khi lượt có nguồn `travel/services/`;
  - thẻ gồm ảnh (chỉ `/anh/khach_san/…jpg`) hoặc ô màu, tên, hạng, Bản đồ / Tìm phòng (chỉ 2 gốc, `_blank noopener`);
  - dòng "Theo danh mục, chưa kiểm giá / phòng trống".
- `tl.css`: lớp `the-ks*`.
- Server, kho, chuỗi gửi model: không đổi.

## Kiểm [đã chạy]
- **T1 + T2:** `test_the_khach_san.py` (node thật) + `test_anh_tra_loi.py` ⇒ 3 passed. Ca kiểm:
  - tên dài nhất (Villa Louise ⊂ Villa Louise Beach); tên lõi; bỏ "Huế" cuối; không lặp thẻ;
  - ≤ 3 theo thứ tự; tên lõi 1 chữ ⇒ bỏ; không trích bài lưu trú ⇒ 0; có mục web ⇒ 0; không theo ranh giới từ ⇒ 0.
- **T3** (`data/ks_chat_2026-11-15/tools/mo_phong.py`: chính `theKhachSan.js` trên 12 câu đã hỏi thật, cơ sở = `trang_cho_o(bảng v4)`):
  - 10 / 12 câu có thẻ, 18 thẻ, 7 câu có thẻ có ảnh.
  - C đọc tay từng thẻ cạnh câu trả lời: **18 / 18 đúng cơ sở**; ca "Villa Louise" đã hết.
  - Bỏ sót 1: model viết "Meliá" (sắc), bảng ghi "Meliã" (ngã) ⇒ không thẻ. Thiếu thẻ, không sai thẻ.
- **T4:** C nhìn lại cả 7 ảnh thẻ sẽ hiện (`data/ks_chat_2026-11-15/xem_lai_{1,2}.jpg`): 7 / 7 có biển tên đúng cơ sở; 0 số điện thoại đọc được.
- **T5 Playwright** (`tools/pw_the_ks.py`, server tạm 8040, đã tắt; câu tự đặt "gần biển Thuận An"):
  - 1440 + 390: 3 thẻ, tên + hạng, dòng "chưa kiểm";
  - link đúng 2 gốc; 0 lỗi console; 0 yêu cầu ra ngoài; không cuộn ngang ⇒ **DAT**.
  - Câu trả lời lần này nhắc 4 cơ sở ⇒ đúng trần 3.
  - Ảnh `data/ks_chat_2026-11-15/anh/`.
- **Test rộng:** `backend/tests` (`--env-file`) **1057 passed, 348 s**.

## Tiền
Đếm 0,0083 + Playwright 2 lượt ≈ 0,001 ⇒ ≈ **0,009 USD**.

## Giới hạn
- Tên viết khác bảng (dấu khác, "Saigon" ↔ "Sài Gòn" khi không kèm tên bảng) ⇒ không thẻ.
- "Hương Giang" là tên lõi của một khách sạn và cũng là tên sông ⇒ trong câu trả lời bằng bài lưu trú có nhắc "sông Hương Giang", thẻ khách sạn đó có thể hiện. Chưa gặp ở 12 câu.
- 58 / 137 cơ sở có ảnh; phần còn lại là ô màu.

## Sau review E (`e_review_the_ks_chat.md`, ready, m-1 — A chọn sửa)
- Tên lõi **1 chữ** (19 tên, vd một khách sạn hiện ở 3.036 lượt lịch) HOẶC trùng **địa danh / sự kiện / tên đường** ⇒ chỉ khớp khi ngay trước có chữ loại hình (khách sạn / khách sạn nghỉ dưỡng / khu nghỉ dưỡng / resort / hotel).
- Danh sách trùng **sinh bằng code** (`data/ks_chat_2026-11-15/tools/dung_trung.py` ⇒ `frontend/src/theKhachSanTrung.js`, không sửa tay). Hai luật:
  - xuất hiện ≥ 10 lần trong bài kho ngoài bài lưu trú. Địa danh thấp nhất 12 lần, tên khách sạn thật cao nhất 7 (một bài vịnh nhắc các khu nghỉ dưỡng) ⇒ ngưỡng 10;
  - trùng tên đường trong địa chỉ bảng.
  - Ra 10 tên: đủ 5 tên E nêu + 3 địa danh khác + 2 tên đường.
- 3 test mới (trong địa danh ⇒ 0; có "khách sạn" trước ⇒ 1; tên 1 chữ có / không chữ loại hình). Test cũ "tên 1 chữ ⇒ bỏ" đổi thành "chỉ khớp khi có chữ loại hình". 3 passed.
- **12 câu thật trước / sau: giống hệt**, 18 thẻ, 0 thẻ mất. Thẻ trùng tên sông vẫn ra vì câu trả lời viết đủ "Khách sạn nghỉ dưỡng …".
