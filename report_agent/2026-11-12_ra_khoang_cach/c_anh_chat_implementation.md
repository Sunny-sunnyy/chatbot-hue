# Ảnh trong chat theo tên nơi / món — implementation (C, 15/11/2026)

Plan `docs/superpowers/plans/2026-11-15-anh-trong-chat-plan.md` (sha `bf43cc57f6ea`, A duyệt; User cho bật khi đạt). Nhánh `p9-anh-chat` (worktree `/tmp/c_ac`). Đếm trước: `c_dem_anh_chat.md`.

## Đổi gì (chỉ giao diện)
- `frontend/src/anhTraLoi.js`:
  - `anhTraLoi(turn)` nay trả **danh sách** `[{anh, baiId, ten}]` (rỗng ⇒ không ảnh).
  - Nguồn trích thuộc một bài ⇒ như luật cũ (1 ảnh).
  - Nguồn ≥ 2 bài ⇒ theo thứ tự trích, lấy bài thoả cả bốn: `LOAI_MOT_NOI`, ảnh không `kc`, `tenKhop(title)` ≥ 2 chữ (bỏ ngoặc, chữ thường, NFC), tên có trong chữ trả lời. Tối đa 3.
- `frontend/src/chat.jsx` `AnhTraLoi`: 1 ảnh như cũ; 2–3 ảnh ⇒ hàng ảnh nhỏ, tên nơi dưới mỗi ảnh, bấm mở bài. `tl.css` thêm lớp `anh-tra-loi-hang / -o / -khung / -ten`.
- Server, kho, chuỗi gửi model: không đổi. `turn.sources` vốn là nguồn được trích (`api/routes/chat.py:556`).
- Test: `backend/tests/test_anh_tra_loi.py` — test cũ đổi sang dạng danh sách (T1), thêm test luật nhiều ảnh (T2).

## Kiểm [đã chạy]
- **T1 + T2:** `test_anh_tra_loi.py` 2 passed (node thật, `anhBai.js` thật).
  - T1: một bài ⇒ cùng ảnh như cũ; mọi ca "không ảnh" cũ vẫn rỗng.
  - T2 có 7 ca: 2 ảnh theo thứ tự trích · tên không có trong chữ ⇒ bỏ · tên 1 chữ ⇒ bỏ · bỏ ngoặc khi khớp · ảnh `kc` ⇒ bỏ · ≤ 3 · bài vé ⇒ bỏ · có mục web ⇒ không ảnh.
- **T3 mô phỏng** (`data/anh_chat_2026-11-15/tools/mo_phong.py`, chạy CHÍNH `anhTraLoi.js` qua node trên 154 câu trả lời Golden đã lưu; nguồn trích dựng từ `[n]` ⇒ đoạn top 10):
  - câu có ảnh **77 ⇒ 103 / 154**;
  - 26 câu mới, 39 ảnh mới;
  - 13 câu 2 ảnh, 0 câu 3 ảnh.
  - Ước lúc đếm trước (~118) cao hơn vì lúc đó khớp cả tên gọi khác và tên 1 chữ.
- **T4 nhìn lại 100 % ảnh mới** (1 agent con xem 39 ảnh + C tự xem ảnh bị đánh dấu; biên bản `data/anh_chat_2026-11-15/nhin_lai_anh_moi.md`): **0 sai nơi** — ĐẠT sàn.
  - Ảnh Lăng Dục Đức agent ghi "không chắc"; C tra bảng nguồn lịch: Commons "Cổng An Lăng" = lăng Dục Đức ⇒ đạt.
  - **3 ảnh đúng nơi nhưng có quảng cáo / số điện thoại**, trái luật chọn ảnh ở MỌI chỗ hiện từ 14/11:
    - `kp/k1uulq5d` (Chợ An Cựu: bảng taxi có số điện thoại);
    - `kp/k1hfh0ms` (Chợ Tây Lộc: biển karaoke góc trái);
    - `kp/kj4y0wm` (phố Hai Bà Trưng: biển neon thẩm mỹ viện; cùng file với `lich/pho_hai_ba_trung`).
  - A chọn sửa tận gốc (E che mờ / thay / gỡ), không thêm danh sách chặn ⇒ đã báo E.
- **Sửa sau Playwright lượt đầu:** ảnh xếp theo thứ tự `turn.sources` của server (id nguồn), còn dòng "Nguồn" xếp theo `turn.numbers` (số trích hiện trong chữ). Ảnh 1440 lượt đầu ra Bà Nga trước, trong khi dòng Nguồn ghi Mụ Rơi trước.
  - Sửa: ảnh dùng cùng thứ tự với dòng Nguồn (`SourceLine.jsx`). Thêm 1 ca test.
  - Mô phỏng không đổi số (lượt đã lưu không có `numbers`).
- **T5 Playwright** (`tools/pw_anh_chat.py`, server tạm 8039 cwd `/tmp/c_ac/backend`, đã tắt; câu tự đặt so sánh 2 quán bún bò, 2 lượt hỏi thật):
  - khổ 1440 + 390: 2 ảnh, mỗi ảnh có tên, đúng thứ tự dòng Nguồn;
  - link `#/kham-pha/bai/…`, ảnh `/static/anh/…`;
  - 0 lỗi console, 0 yêu cầu ra ngoài, không cuộn ngang ⇒ **DAT**.
  - Ảnh `data/anh_chat_2026-11-15/anh/`.
- **Test rộng:** cả `backend/tests` (`--env-file`) **1056 passed, 511 s**. `vite build` qua.

## Bật
Không có cờ: merge = bật. User cho bật khi đạt T1–T5 — cả 5 đạt.

## Tiền
4 lượt hỏi thật trong Playwright (2 lượt đầu + 2 lượt sau sửa thứ tự) ≈ 0,002 USD; mô phỏng + nhìn lại ảnh 0 USD (agent con không gọi API trả phí).

## Giới hạn
- Chỉ khớp đúng tên bài (≥ 2 chữ). Câu trả lời gọi tên khác (viết tắt, tên gọi khác, không dấu) ⇒ không ảnh — thiếu ảnh chứ không sai ảnh.
- Khách sạn chưa làm (User: sau).
- 3 ảnh có quảng cáo / số điện thoại (trên) vẫn hiện tới khi E sửa tận gốc.

## Sau review E (`e_review_anh_chat.md`, ready, m-1) — nhánh @ commit sau `41da66b`
- **m-1 sửa:** khớp tên theo **ranh giới từ** (lookaround Unicode `\p{L}\p{N}`, cờ `u`, chuỗi NFC) và **giữ hoa / thường trừ chữ đầu** ⇒ "một quán nhỏ ven đường" không còn khớp "Quán Nhỏ"; tên lọt giữa một chữ dài hơn ⇒ không khớp. 2 ca test mới; `test_anh_tra_loi.py` 2 passed.
- **Giới hạn còn lại (đo, không sửa):** "Lý Huế" ↔ "quản lý Huế" vẫn khớp — "lý" là một âm tiết riêng nên có ranh giới từ hợp lệ. Thử giữ hoa cả chữ đầu: chặn được, nhưng mô phỏng mất **14 / 39** ảnh mới đúng (39 ⇒ 25; câu có ảnh 103 ⇒ 98), vì model hay viết "chợ …", "lăng …" ⇒ không chọn. Chỉ sai khi bài đó cũng được trích.
- **Mô phỏng sau sửa:** 103 / 154, 39 ảnh mới — **giống hệt** bộ 39 ảnh đã nhìn lại (so từng cặp case · ảnh) ⇒ kết quả T4 (0 sai nơi) vẫn đúng.

## Sau merge (`e801c83`)
- 3 ảnh quảng cáo / số điện thoại: E đã sửa tận gốc (commit `133d29e`). C xem lại ảnh Chợ An Cựu: hai bảng số đã được làm mờ.
- Ảnh phố Hai Bà Trưng (người xem ghi chưa chắc): nguồn là bài tuoitre.vn về đêm khai trương chính phố đi bộ đó ⇒ có căn cứ đúng nơi.
- Bài học 25 §8 + bài 24 + sổ 07 + README đã viết; kiểm độc lập `data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_25_anh_chat.md` (8 chỗ sai / dễ hiểu nhầm — đã sửa).
