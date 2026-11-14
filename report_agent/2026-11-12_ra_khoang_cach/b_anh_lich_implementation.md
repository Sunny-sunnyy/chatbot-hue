# "Lên kế hoạch" đợt 2 phần (B) — ảnh từng điểm trong lịch · B · 11:12 14/11/2026

Nhánh `p9-anh-lich` (từ `p9-lich-truong-gd` `3ba7e9b`), commit **`6c779ff`** (push). Cờ `anh_lich` **TẮT**.

**Căn cứ:** plan `docs/superpowers/plans/2026-11-13-len-ke-hoach-dot-2-plan.md` phần (B) (A duyệt 13/11, mức nhẹ). Bảng ảnh B0 của C: `data/phase_9/lich_trinh/bang_anh_v1.json` md5 `a5e210e5a1f0`. 0 USD model.

## Làm gì
- **Ảnh:** 24 ảnh `data/phase_9/lich_trinh/anh_lich_v1/*.jpg` (không chép `goc/`) ⇒ `frontend/public/anh/lich/`, tổng **1,8 MB** (trần 2,5). Ảnh nằm trong repo public như ảnh cổng; giấy phép mở, có ghi công.
- **Backend:**
  - cờ `assistant.anh_lich` (cần `len_ke_hoach_v2`) + `lich_trinh_bang_anh`;
  - `lich_trinh_v2.nap_bang_anh` kiểm lúc khởi động, sai ⇒ không khởi động: id có trong bảng điểm, `src` là file có thật dưới `/anh/lich/` (không `..`), đủ tác giả + giấy phép, trang ảnh là Wikimedia Commons;
  - `dung_lich` điền `anh` theo `id_diem`; điểm không có dòng ⇒ `null` (không ảnh thay);
  - chuỗi gửi model không đổi (test so `tin_nhan_model` cờ bật ↔ tắt).
- **Giao diện** (`chat.jsx` `LichV2` + CSS):
  - ảnh dưới câu mô tả, kèm dòng "Ảnh: tác giả · giấy phép · trang ảnh trên Wikimedia Commons";
  - trình duyệt kiểm lại `src` / link Commons trước khi vẽ;
  - đường ảnh ghép `BASE_URL` (`/static/`) như `anh.js`. **Lỗi bắt được trước lượt đo:** bản đầu dùng thẳng `/anh/lich/…` ⇒ 404.
- **Docker:** danh sách chừa thêm `bang_anh_v1.json` (`data/phase_12/deploy_nhap/dung_dockerignore.py`, đã sinh lại).

## Tiêu chí ghi trước (plan §B) ⇒ kết quả
| Tiêu chí | Kết quả | |
|---|---|---|
| Luôn: mỗi ảnh hiện ra có trong bảng ảnh, đúng `id_diem`, có dòng ghi công | test `test_photo_table_loads_and_maps_by_point_id` + Playwright: 7 / 7 ảnh đúng tên điểm, đủ ghi công | ĐẠT |
| Luôn: 0 ảnh từ host ngoài; CSP giống byte | Playwright: 0 yêu cầu ra ngoài origin; `api/app.py` không đổi | ĐẠT |
| Sàn: ≥ 24 / 34 điểm có ảnh | **24 / 34** (đúng sàn, 0 biên — như A ghi 13/11) | ĐẠT |
| Cỡ: thư mục ảnh ≤ 2,5 MB; bundle JS không tăng > 1 KB | 1,8 MB; bundle 352,26 ⇒ 353,03 kB (+0,8 kB; gzip +0,2) | ĐẠT |
| Người xem: 10 lịch ⇒ ảnh đúng điểm 10 / 10 | agent con ngữ cảnh mới xem bảng ghép 10 lịch (127 mục, 98 ảnh, 21 ảnh khác nhau; `data/len_ke_hoach_v2_2026-11-13/xem_anh/`): **10 / 10**, 0 ảnh hỏng. Một ảnh lăng "đúng loại, không chắc đúng lăng" | ĐẠT |

## Đã chạy
- **Test** (cờ tắt; file chạm, có và không `--env-file`): 125 đạt (1 phút 7 giây) / 110 đạt (1 phút 5 giây). Test mới:
  - bảng ảnh thật nạp đúng + gắn theo id + chuỗi model không đổi;
  - 7 dòng hỏng bị từ chối: id lạ, host ngoài, `..`, file không có, thiếu tác giả, thiếu giấy phép, trang không phải Commons;
  - cờ cần bản 2 + bảng.
- **Playwright chạy thật** (server nhánh 8896, cờ `anh_lich` bật tạm trong worktree; `tools/pw_nghiem_thu.py --anh`; ≈ 0,001 USD): 1440 + 390 đều đạt — điền bằng bàn phím, khung trước câu, 7 ảnh tải được (naturalWidth > 0), đủ ghi công, 0 lỗi console.
  - Ảnh toàn trang có 2 ảnh trống: trang chụp trước khi ảnh tải lười (`loading="lazy"`) kịp tải. Lúc dùng thật ảnh tải khi cuộn tới.

## Giới hạn / việc sau
- 10 / 34 điểm không có ảnh (phiếu ảnh của User) ⇒ thêm ảnh = thêm dòng vào bảng + file, không sửa code.
- Giao diện mới của E (H1) sẽ thay `LichV2`; đã dặn E dùng đúng trường `anh` + ghi công.
- Nhánh dựng trên `p9-lich-truong-gd` ⇒ rebase lên `main` khi merge. Bật cờ = A trình User.
