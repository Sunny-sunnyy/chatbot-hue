# STATUS C — kết phiên 05/11 (16:47 05/11/2026 `date`; luật ≤ 30 dòng; lịch sử: `git show 1d1fa77:session_prompt/sessions/STATUS_C.md`)

## PHIÊN SAU ĐỌC TRƯỚC
- **C192 sửa kho giờ mở cửa** (plan `65e7e2b2b68c`, A duyệt): chưa xong — xoá collection bị auto mode chặn ⇒ cần **User `!`**. Kho đã khôi phục, chỉ mục nguyên 8.424 point. Lệnh đã chép vào **`data/sua_kho_2026-11-05_gio/tools/chay.sh`** (`eb101131f146`, không phụ thuộc `/tmp`) ⇒ `! bash data/sua_kho_2026-11-05_gio/tools/chay.sh` (B / E tắt server trước).
  - Bước 0 kiểm backend = `5a8aa5e`. `main` đổi phần backend ⇒ bước 0 dừng ⇒ xem diff. Đường **không stream** (`answer_case`) chưa đổi ⇒ sửa dòng kiểm sang commit mới. Đã đổi ⇒ chạy lại bộ "trước" (Golden 11 + an toàn 10 ≈ 0,011) trước khi chạy lệnh.
  - Sao lưu: `knowledge-base-hue/meta/backup_gio_mo_cua_2026-11-05/` · `data/sua_kho_2026-11-05_gio/backup/` (record `51fb1ec63cbc`, sparse `c8134c49a648`) · snapshot Qdrant 13:05.
  - Sau lệnh: Golden 11 + an toàn 10 bên "sau" (`touched.json`) + 1 câu thật + judge. Ghi lệch nhỏ đã báo A: dòng nguồn "chép từ tài liệu vé Quần thể trong kho".
- **Bộ đo đã soạn (private, md5 12):**
  - Sửa lịch `data/phase_9/bo_do_sua_lich/`: `chuoi_da_thay` `d0ad12b6ed12` · `chuoi_sealed` `34b20600ac00` (B / E không mở) · `kiem_bo.py` OK 6/6 · `mo_phong_kin.py` (bản sao mo_phong của B trỏ kín).
    - Đã thấy 10/10 khớp code B (`/tmp/b_sualich`, chưa push); kín 4/5 + K-S2 ca biên "thẻ chỉ có nút Bỏ". Khi B push ⇒ chạy lại cả hai.
  - B5b: bảng `lich_trinh/diem_v4.json` `c7beec6b70a5` (`kiem_v4.py` OK, 23/23 căn cứ) · toạ độ `diem_toa_do.json` `74640c475399` (17/28; ghi chú `toa_do_ghi_chu.md`).
  - B6 `bo_do_b6/`: đã thấy `6ed74db21616` (+L01 lưu trú) · kín `4de04132600b` (+K-L01) · `kiem_bo` OK (cỡ 27).
  - B5c `bo_do_b5c/` (B5c đã âm — B dừng): đã thấy `bc6755a34dbe` · kín `13eedb9884a6` (không chạy) · chuỗi `79e458b7a023`.
- **Phiếu chờ User:**
  - (1) chấm Q3 B5 `data/phase_9/b5/kin/phieu_cham_user.md` `f83069cb5a67`;
  - (2) duyệt bảng v4 `data/phase_9/lich_trinh/diem_cho_user_v4.md` `12f1003cd3a3` + 5 điểm trong nhà gợi ý (`toa_do_ghi_chu.md`: Bảo tàng Cổ vật Cung đình, Duyệt Thị Đường, Lê Bá Đảng, Bảo tàng Mỹ thuật, Bảo tàng Hồ Chí Minh — chưa thêm).
- **Plan (C viết):** sửa lịch bản 3 `5b68f3cb666a` (A duyệt; trần 0,20) · B5b bản 2 `cc09fda9f634` (A duyệt; trần 0,07) · B6 bản 2 `b6a046e944c0` (B review sau B5c; trần 0,22).
- **Câu hỏi mở:** đổi link Maps B5 sang toạ độ cho 17 điểm? (đề xuất, chưa sửa code) · dự phóng Phase 9 ≈ 2,4 > 2,0 (A báo User).

## Worktree / tạm
- **Gỡ được** (việc đã merge): `/tmp/c_b5kin` (B5 `5bc45cf`, có `frontend/dist`), `/tmp/c_q1main` (`b019aab`), `/tmp/c_toc_do6b_r` (#6 `14db83b`), `/tmp/c_toc_do6` (#6 cũ `ea081b0`) ⇒ `git worktree remove --force <dir>` (có symlink `data` / `knowledge-base-hue` chưa theo dõi).
- `/tmp/c191`, `/tmp/c192`, `/tmp/c188`, `/tmp/c_b5kin_run`: tạm — phần cần giữ đã chép vào `data/`. Mất khi khởi động lại.

## Bẫy (giữ)
- Kiểm nhãn bộ đo bằng **code thật** của bậc (mô phỏng) trước lượt có phí — `kiem_bo` tự viết bỏ sót "thêm điểm không nêu chỗ" (B163 bắt 2 nhãn).
- Xoá / dựng lại chỉ mục ⇒ auto mode chặn ⇒ soạn lệnh `!` có bước 0 + tự lùi, đừng thử cách khác.
- Ca phá phải so với số lỗi gốc (lần đầu 6/6 là đạt giả vì bộ còn lỗi khác).
- Đọc số dòng từ đầu ra `grep` cẩn thận (C197 lấy nhầm số thứ tự danh sách làm số dòng kho — máy kiểm bắt).
- **Tiền C 05/11:** 0,035249 USD (C174 0,019846 + kín B5 0,004612 + C192 "trước" 0,010791).
