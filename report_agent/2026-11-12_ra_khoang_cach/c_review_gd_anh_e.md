# Review: bỏ ghi công trang chủ / Lên kế hoạch / lịch + lịch mẫu "Ví dụ" (E, nhánh `p9-gd-anh-e` `5b477b1`)

Cập nhật: 15:22 14/11/2026 (C). Mức nhẹ. Kết luận: **ready_for_user_confirmation sau m-1** (một dòng). E sửa xong thì A merge thẳng, C không cần kiểm lại.

## Đã kiểm
- **Diff 3 commit:** 8 file. Không thấy file nào ngoài phạm vi.
- **Ghi công:**
  - Đã bỏ hết ở trang chủ, ô "Thích gì", thẻ lịch, dòng Open-Meteo.
  - `GP` không còn ai import ở 3 file này; dọn `anh.js` để sau, như E đã nói.
  - Link "Nguồn ảnh" ở chân trang vẫn còn trên nhánh E (gốc từ main). Nhánh C gỡ link này ⇒ hết sau khi merge cả hai.
- **`/api/lich_mau`:**
  - Chỉ đọc, không gọi model, cờ `len_ke_hoach_v2` tắt ⇒ 404.
  - Dựng bằng chính `xep_v2` + `dung_lich`, giữ trong RAM theo bảng.
  - Câu mỗi điểm do code dựng, không có nguồn. Test khoá: khung trùng `xep_v2`, qua `kiem_khung_v2`, 0 nguồn.
- **Ảnh chụp của E** (`anh_e_1411/sau_len_ke_hoach_1440.png`): có nhãn "Ví dụ", câu "Lịch của bạn có thêm câu tả … kèm nguồn" đúng với lịch thật.

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| m-1 | minor | `LenKeHoach.jsx` `LichMau`: `minh_hieu.replace(/\s*—\s*sai thì bấm Sửa\.?$/, ".")` | Server ghi `— sai thì bấm **Sửa**.` (có dấu `**`, `lich_trinh_v2.py:585`) nên mẫu regex không khớp. Lịch ví dụ vẫn hiện "sai thì bấm Sửa" dù ví dụ không có nút Sửa (thấy trong ảnh chụp của E). | regex nhận cả `**` (vd `/\s*—\s*sai thì bấm \*{0,2}Sửa\*{0,2}\.?$/`); mở trang thấy dòng "Mình hiểu" kết thúc bằng dấu chấm |

## Ghi nhận (không phải finding)
- Điểm không có ảnh (vd phố đi bộ) hiện ô xám `lkh-khong-anh`: thiết kế có sẵn trên main, nhánh này không đổi.
