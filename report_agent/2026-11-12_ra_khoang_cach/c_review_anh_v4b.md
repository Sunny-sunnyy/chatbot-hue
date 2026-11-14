# Review nhánh `p9-anh-v4b` @ `1eb8d09` (E) — C · 18:26 14/11/2026

**Kết luận: `changes_requested`** — 0 blocker · 1 major · 2 minor. 0 USD.

## Cổng tối thiểu
- Diff: `anhBai.js` (8 dòng mới / đổi + 2 `kc` theo m-1 / m-2 của C), 7 jpg mới + 1 jpg đổi (`kp/` của bài biển Thuận An), `anh/lich/bien_thuan_an.jpg`, `settings.yaml` (chỉ trỏ `bang_anh_v3.json`, md5 `eef35f994e31` — C tính lại khớp), report. Đối chiếu khoá ↔ bài: 10 / 10 đúng bài như report. `git diff --check` sạch.
- [Chạy] worktree riêng của C (không đụng `/tmp/e_v4b`): `test_cong_dot_1.py` + `test_len_ke_hoach_v2.py` 112 passed (bảng ảnh lịch v3 nạp được khi khởi động).
- m-1 / m-2 vòng trước: `travel_guides` + Cơm hến Đập Đá ⇒ `kc`: đóng.
- C nhìn 8 / 8 ảnh mới (`/tmp/e_v4b_xem.jpg` + ảnh lịch bản đầy đủ).

## M-1 (major) — ảnh biển Thuận An có trẻ em mặc đồ bơi
- **Vị trí:** `frontend/public/anh/lich/bien_thuan_an.jpg` (+ ảnh Khám phá cùng nguồn, KHÔNG `kc` ⇒ hiện cả cạnh câu trả lời và mọi lịch có Thuận An).
- **Yêu cầu bị ảnh hưởng:** tiêu chí E ghi trước `data/anh_day_du_2026-11-14/TIEU_CHI.md:14-15` và brief v4 dòng 16: bỏ ảnh "trẻ em đồ bơi".
- **Bằng chứng:** ảnh đầy đủ có nhiều trẻ nhỏ mặc đồ bơi ở cận cảnh / giữa ảnh (bờ nước giữa khung, nhóm bên trái), nhìn rõ dáng người.
- **Tiêu chí đóng:** đổi ảnh Commons khác của Thuận An không có trẻ em đồ bơi nhận ra được (cảnh bãi / bờ / cổng biển xa người), hoặc cắt sao cho không còn người nhận ra được; không đạt ⇒ để trống như trước (ảnh lịch 33 / 34) — "thà trống còn hơn sai luật".

## Minor
- **m-1:** Đầm Chuồn Hội Quán (`kc`): ảnh là cửa hàng / chỗ thuê ván chèo đứng có chữ "Quán" ở góc — không thấy dấu hiệu là nhà chòi ăn uống của bài; `kc` vẫn hiện ở Khám phá như ảnh của bài ⇒ đề xuất để trống (cùng lý do E bác ở lượt trước: ảnh có thể là quán khác trên đầm).
- **m-2:** Ru coffee (`kc`) có logo trang nguồn ở góc dưới trái — luật "logo to che chủ thể" không chạm (logo nhỏ, không che), ghi để biết; không cần sửa.
- Bảo Thạnh (không `kc`, một người chọn): biển tên "Bảo Thạnh" đọc rõ — C đồng ý không `kc`. Phúc Long / 2 cơm hến / An Phú `kc`: hợp luật (ảnh món / ly chung).

## Vòng 2 @ `179fc0f` (C · 18:29 14/11/2026)
**Kết luận: `ready_for_user_confirmation`** — M-1 + m-1 đóng, 0 finding mới.
- M-1: `anh/lich/bien_thuan_an.jpg` không còn trong nhánh; `kp/` của bài Thuận An giống main (ảnh v4, `kc`); bảng ảnh lịch trả về như main ⇒ lịch 33 / 34.
- m-1: dòng + file Hội Quán gỡ; 6 jpg mới khớp 6 dòng mới của `anhBai.js`.
- Ghi chú: diff ba chấm cho thấy `settings.yaml` đổi dòng bảng quán — do E chép bản main hiện tại (đã có merge `p9-anh-quan`); `git diff origin/main origin/p9-anh-v4b -- backend/config/settings.yaml` rỗng ⇒ merge không đổi gì. `git diff --check` sạch.
