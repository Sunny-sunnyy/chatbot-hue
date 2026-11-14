# Review — giao diện H1 đợt 0 của E (nhánh `p9-gd-h1` `848eafa`, từ `main` `a192843`)

Người kiểm: C (`hue-rag-b4`) · 11:47 14/11/2026 (`date`) · skill `risk-gated-agent-review` · một review cả đợt · 0 USD.

**Kết luận: ready_for_user_confirmation — 0 blocker, 0 major, 3 minor.**

## Đã kiểm
- **Tách file là chép nguyên:**
  - so từng dòng `pages.jsx` cũ với `TrangChu` / `KhamPha` / `LenKeHoach` / `GioiThieu` / `chung.jsx`: 9 dòng "khác", tất cả chỉ do thêm `export` (hằng / hàm dùng chung);
  - `chat.jsx`: 4 dòng "khác", cũng chỉ do `export` khi dời sang `LichV2.jsx` / `SourceLine.jsx`; phần thêm vào `chat.jsx` chỉ có 3 dòng import;
  - hành vi trang bài giữ nguyên: chặn mã không có trong danh sách trước khi gọi server, `BaoSai` chỉ gửi mã bài.
- **Thay đổi thật:**
  - `route.js`: bọc `startViewTransition` + `flushSync`; không hỗ trợ hoặc máy giảm chuyển động ⇒ đổi trang như cũ;
  - `hieuUng.js`: gắn `html.hieu-ung` khi máy không giảm chuyển động; trình duyệt thiếu `animation-timeline` ⇒ dùng IntersectionObserver + MutationObserver; menu dùng sự kiện cuộn;
  - `hieu_ung.css`: chỉ `transform` / `opacity`, mọi luật nằm dưới `.hieu-ung`;
  - `index.css`: font serif cho tiêu đề, đầu trang + chân trang nền nước sâu;
  - thêm gói font `@fontsource/noto-serif-display` 5.2.5 (một độ đậm 600, tự host).
- **Build (worktree của C):** JS chính **112,46 KB gzip** (khớp số E báo), CSS 7,92 KB.
- **Test:** `test_static_ui.py` + `test_cong_dot_1.py` 26 / 26 đạt (65 s).
- **3 phép đo trên bản build thật** do FastAPI phục vụ (cổng 8897; Playwright chỉ tắt CSP cho công cụ đo chèn style, trang thật giữ CSP), 6 đường × 1440 / 390:
  - tương phản: **0 trượt / 12**;
  - giảm chuyển động ⇒ **0 animation / 12**;
  - CLS đạt ở 10 / 12. Trượt ở `#/kham-pha/<lĩnh vực>`: 0,23 (1440) / 0,34 (390).

## Finding
| # | Mức | Vị trí | Vấn đề | Tiêu chí đóng |
|---|---|---|---|---|
| m-1 | minor (có sẵn trước đợt 0) | trang danh sách lĩnh vực (`LinhVuc`) | CLS 0,23 / 0,34 vì thẻ bài tải sau (`/api/kham_pha`) đẩy chân trang và dòng ghi chú xuống; tắt giảm chuyển động vẫn giữ nguyên số ⇒ không do hiệu ứng. Đợt 0 không đổi trang này. | **C sửa ở đợt 1** (`KhamPha.jsx` là file của C): giữ chỗ cho lưới thẻ lúc đang tải. |
| m-2 | minor | `hieu_ung.css` `.nang.lop-mau::after` | Lớp màu phủ toàn bộ phần tử, từ dưới lên, đậm .55. Nếu gắn `.lop-mau` cho cả thẻ (ảnh + chữ), lúc rê chuột lớp màu đè lên chữ ở đáy thẻ. | ghi rõ: chỉ gắn `.lop-mau` cho khung ảnh của thẻ; C làm đúng như vậy ở đợt 1. |
| m-3 | minor | `index.css` | `.nav-a` khai hai lần liền nhau (lần sau đè màu + bo góc). Trang chủ 390 CLS 0,095 và Lên kế hoạch 390 CLS 0,096 đạt nhưng sát ngưỡng 0,1. | gộp `.nav-a` khi tiện; theo dõi hai số CLS ở đợt 1. |
