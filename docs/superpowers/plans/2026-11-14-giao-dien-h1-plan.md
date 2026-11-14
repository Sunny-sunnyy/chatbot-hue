# Plan — chuyển 5 trang mẫu H1 "Sông Hương" (hiệu ứng bản 2) thành code thật (mức nhẹ)

Viết: E, 14/11/2026. User: "làm đi, bắt đầu ngay" (qua A). Mẫu đã duyệt: `data/ui_mau_2026-11-14/h1/` (5 trang, C đo đạt 3 phép ở 2 khổ). Ràng buộc gom ở `data/ui_mau_2026-11-14/GHI_CHU_KHI_CODE.md`. Chỉ giao diện: chuỗi gửi model không đổi, backend không đổi (dùng sẵn `du_bao.ngay`, `phut_di`, `anh` đã có trên `main` `a192843`).

## Chia việc (mỗi người một nhóm file — không chồng nhau)
| Đợt | Người | File | Việc |
|---|---|---|---|
| 0 chung (làm trước, push sớm) | E, nhánh `p9-gd-h1` từ `main` | `index.css` (token, đầu trang, nút / chip, chân trang) · `hieu_ung.css` + `hieu_ung.js` → `src/hieuUng.js` (một hàm `batHieuUng()` gọi ở `main.jsx`) · `route.js` (bọc đổi hash bằng `startViewTransition`) · `package.json`: thêm `@fontsource/noto-serif-display` (OFL, 2 độ đậm) · `App.jsx` (đầu trang + menu đổi nền khi cuộn) · tách `pages.jsx` thành `TrangChu.jsx`, `KhamPha.jsx` (gồm lĩnh vực + bài), `LenKeHoach.jsx`, `GioiThieu.jsx`; tách `LichV2` + phần dùng chung ra `LichV2.jsx` | Không đổi hành vi; tên lớp cũ giữ (danh sách B) |
| 1 | E | `TrangChu.jsx`, `LenKeHoach.jsx`, `LichV2.jsx` (+ CSS `tc-` / `lkh-`) | Trang chủ như mẫu + ảnh đầu trang đổi 3 ảnh có giấy phép bằng chuyển mờ CSS (B, `b_hieu_ung_tham_khao.md` §3; có nút Dừng vì WCAG 2.2.2 với nội dung tự chạy > 5 s; giảm chuyển động ⇒ một ảnh đứng yên); Lên kế hoạch: biểu mẫu 4 nhóm (giữ aria) + lịch dòng thời gian: ảnh + ghi công (`anh` / null), `phut_di` "khoảng N phút đi" chỉ giữa hai mục cùng buổi, "Nếu mưa" theo `du_bao.ngay` (không bóc chữ), "Tổng quan" + neo ngày; bật cờ `anh_lich` nếu A duyệt |
| 1 | C | `KhamPha.jsx`, `GioiThieu.jsx` + `src/kp.css` / `src/gt.css` | Như mẫu; câu "chưa có…" theo `/api/tinh_nang`; giữ hành vi trang bài (chặn mã ngoài danh sách trước khi gọi server, BaoSai chỉ gửi mã bài) |
| 1 | B | `chat.jsx`, `HoiBangAnh.jsx` (+ `tl-`) | Như mẫu trợ lý; giữ `.turn .answer .composer textarea [role=status] .clarify .notice .feedback #khung-tro-ly .nguon-ten` |

## Điểm cần A / B chốt trước đợt 1
**Lịch hiện ở đâu.** Mẫu đặt lịch ngay cạnh biểu mẫu trên `#/len-ke-hoach`. Code hiện tại gửi xong thì chuyển sang `#/tro-ly`. Đề xuất: ở lại `#/len-ke-hoach`, cột phải vẽ `LichV2` của lượt lịch mới nhất trong `chat` (một nguồn dữ liệu, không gọi API thêm). Lượt đó vẫn nằm trong lịch sử trò chuyện. `pw_nghiem_thu.py` mở `#/len-ke-hoach` rồi chờ `.lich-v2 .lich-ten`, nên vẫn chạy. **B đã xác nhận (14/11):** 3 script không chờ đổi hash. Điều kiện: khối lịch tại trang phải có `.lich-v2 .lich-ten / .lich-cau`, một `.feedback` hiện khi lượt xong, và khối nút `.lich` (Lưu / Sửa) trong `.lich-v2`. Không để hai bản lịch cùng hiện trên một trang: đang ở `#/len-ke-hoach` thì khung chat nổi không vẽ lại lượt lịch đó.

## Giữ nguyên
CSP không đổi. Ảnh nền là file SVG trong `public/`, không dùng `data:`. 0 script / font ngoài. `aria-*`, thứ tự Tab, bàn phím như cũ. Khung lịch vào DOM trước câu; hiệu ứng chỉ là CSS trên phần tử đã có. Mọi hiệu ứng tắt khi `prefers-reduced-motion`, không có nút "Xem hiệu ứng" (nút đó chỉ có ở bản mẫu). `test_static_ui.py` đếm 8 ảnh `.jpg` trong `public/anh` ⇒ SVG mới để ở `public/hoa_tiet/`.

## Tiêu chí + cách kiểm (mỗi đợt; bản build do FastAPI phục vụ)
1. `cd backend && uv run python -m pytest tests/test_static_ui.py tests/test_cong_dot_1.py tests/test_len_ke_hoach_v2.py` đạt. Test rộng một lần trước merge.
2. `npm run build`: bundle JS gzip trước ↔ sau (mốc ~106 KB). Tăng > 8 KB ⇒ ghi lý do. Font: ghi KB.
3. C chạy `kiem_tuong_phan.py` + `kiem_hieu_ung.py` ở 1440 + 390, mỗi trang: tương phản 0 trượt · CLS ≤ 0,1 · reduced-motion ⇒ 0 animation.
4. Playwright 2 khổ: chụp so với mẫu. `pw_nghiem_thu.py` + `pw_bieu_mau_a.py` của B chạy lại đạt (B chạy, ≈ 0,01 USD câu thật). 0 lỗi console / CSP.
5. Review: E ↔ C, B ↔ E (đợt 0 do C review). A cổng ổn định + merge từng đợt.

Tiền: ≈ 0,01 USD (chỉ lượt Playwright có câu thật). Thời gian: đợt 0 ~1,5 giờ; đợt 1 song song.
