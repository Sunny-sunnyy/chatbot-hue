# Review: cổng đợt 1 — S4 phần 2, giao diện S2 nhánh `p11-cong-dot-1` `f20fd28`

Decision: **ready_for_user_confirmation — phần giao diện (review code)** · 0 blocker · 0 major · 2 minor. Số đo Playwright (Q-G / Q-N) là việc C ở S3, không thuộc review này.
Người kiểm: E (Claude Opus 5.5) · 12:56 07/11/2026 (`date`)
Căn cứ: spec cổng đợt 1 (bản duyệt `ff3c317ec88b` + sửa chữ §3) D1, D5, D8–D14, §6 Q-G / Q-N / Q-C, §7.
Implementation report: `s2_implementation.md` (trên `main`).

## 1. Phạm vi đã review

- `git diff 0cb0b0a f20fd28`: 8 file, chỉ `frontend/src/` (`App.jsx`, `HoiBangAnh.jsx`, `chat.jsx` mới, `index.css`, `markdown.js`, `pages.jsx` mới, `route.js` mới, `stream.js`). **0 file `backend/`**, 0 đổi `package.json` / `package-lock.json` / `index.html` / `vite.config.js` ⇒ không gói mới, CSP server không đổi. `git diff --check` sạch.
- Đọc hết `markdown.js`, `route.js`, diff `stream.js`; các chỗ trong `chat.jsx` / `pages.jsx` / `App.jsx` có HTML thô, link, fetch, cờ, biểu mẫu, dòng Nguồn.
- Phần backend: `s4_review_backend.md`.

## 2. Đối chiếu tiêu chí

| Tiêu chí | Bằng chứng (`file:dòng` ở `f20fd28`) | Kết quả |
|---|---|---|
| HTML từ Markdown luôn qua DOMPurify, danh sách cho phép giữ như `main` | `markdown.js` `renderAnswerHtml` / `renderArticleHtml` / `renderWebHtml`: `DOMPurify.sanitize(marked.parse(…), SANITIZE_OPTIONS / WEB_SANITIZE_OPTIONS)`; 3 chỗ `dangerouslySetInnerHTML` (`chat.jsx:261`, `:328`, `pages.jsx:255`) đều nhận chuỗi từ 3 hàm này | khớp |
| D11 link ngoài `target=_blank rel=noopener noreferrer` | `markdown.js` `withSafeLinks`: sửa trên HTML **đã lọc**, bằng DOM | khớp — m-f1 |
| Chữ model ở mục web không tạo link | `WEB_SANITIZE_OPTIONS` bỏ `a` + `href`; link web chỉ từ `source.link` do server dựng (`chat.jsx:333`, `rel="noopener noreferrer nofollow"`) | khớp |
| Link bản đồ chỉ từ code | `LichExtras` lọc `map_url.startsWith(MAP_PREFIX)` (`chat.jsx:382`) | khớp |
| D1 không số `[n]` trong chữ; dòng "Nguồn" | `CITATION_SHOWN` + `CITATION_TAIL` bỏ mã trên chữ thô; `SourceLine` (`chat.jsx:~293`) tên = `source.title` của sự kiện `sources`, "Đọc cả bài" chỉ khi có `bai_id` | khớp (Q-N đếm ở S3) |
| D5 hash, 0 gói router | `route.js` (42 dòng); hash lạ / `%` lẻ ⇒ trang chủ; `baiHref` mã hoá từng đoạn | khớp |
| D8 một cuộc qua các trang | `useChat` ở `App`, `ChatView` dùng chung cho khung nổi + `#/tro-ly`; khung nổi ẩn khi đang ở `#/tro-ly`; huỷ luồng chỉ khi `pagehide` / gỡ `App` | khớp |
| Cờ tắt ⇒ ẩn | `/api/tinh_nang` lỗi ⇒ mọi cờ tắt (`App.jsx:31`); menu "Lên kế hoạch" + thẻ trang chủ + ô thời tiết + nút ảnh theo cờ; `#/len-ke-hoach` khi tắt ⇒ câu "chưa bật" | khớp |
| D3 / m-2 backend: lượt biểu mẫu "Sửa" ⇒ về biểu mẫu | `LichExtras` (`chat.jsx:393`): `bieuMau` ⇒ "Sửa — điền lại biểu mẫu" (`onEditPlan(sua.chon)`), không mở thẻ hỏi lại; câu tự do giữ thẻ cũ. `stream.js` gửi `bieu_mau` chỉ khi `bieuMau` | khớp — **đóng m-2** của review backend |
| Q-U3 không có "kiểu đi" | `pages.jsx` `BIEU_MAU`: số ngày / đi cùng / sở thích | khớp (đóng m-4) |
| D13 không chép nhận diện cổng nhà nước | grep `tripo`, `sở du lịch`, `cổng thông tin`, `hue.gov`, `ubnd`, `visithue`, `logo`, `mascot`, `bản quyền` trên `App.jsx` / `chat.jsx` / `pages.jsx` / `index.css` ⇒ 0; chân trang "… — đồ án tốt nghiệp … có thể sai" | khớp |
| D9 câu gợi ý không Golden / kín | report: dùng lại 5 câu gợi ý cũ (đã có trên `main`) | khớp (không đổi so với `main`) |
| Bundle gzip ≤ 200 KB | E build lại: JS **105,99 KB gzip**, CSS 6,45 KB | khớp |
| CSP: không script / style nội dòng | `dist/index.html` E build: chỉ `<script type=module src=/static/…>` + `<link rel=stylesheet>` | khớp |

## 3. Findings

- **m-f1 (minor) — link dạng `//máy-khác/…` trong câu trả lời không được gắn `target` / `rel`.** `markdown.js` `EXTERNAL = /^https?:\/\//i` ⇒ link không ghi giao thức (DOMPurify giữ) mở **cùng tab**, rời trang, mất phần hiển thị cuộc trò chuyện. Link trong câu trả lời kho do model viết đã có từ `main`; chỉ là cùng loại với D11. *Đóng:* `EXTERNAL = /^(https?:)?\/\//i` (1 ký tự nhóm), không cần test riêng.
- **m-f2 (minor) — tên tab trình duyệt vẫn là tên cũ.** `frontend/index.html` `<title>Hỏi về Huế — trợ lý văn hoá và du lịch Huế</title>` (không đổi ở S2); Q-U5 User chọn "Huế · Trải nghiệm văn hóa & du lịch". *Đóng:* sửa `<title>` (hoặc đặt `document.title` theo trang).

**Câu hỏi độ đơn giản:** `markdown.js` ngắn lại (−112 / + phần mới), bỏ cả cơ chế dựng số `sup` bằng DOM vì D1 không hiện số ⇒ gọn hơn `main`. `route.js` 42 dòng thay cho gói router. Tách `chat.jsx` / `pages.jsx` khỏi `App.jsx` theo trang — hợp lý. Không thấy over-engineering.

## 4. Người kiểm chạy lại [Chạy, 0 USD]

- Worktree `/tmp/e_rv` checkout `f20fd28`: `cd frontend && npm ci && npm run build` ⇒ build 245 ms, JS 334,37 KB (gzip 105,99), CSS 26,43 KB (gzip 6,45); `dist/index.html` không nội dòng.
- Ca dò riêng (khác cách B), `node /tmp/e_rv_do/do_route.mjs` — hàm thật của `route.js` + regex chép nguyên từ `markdown.js`:
  - `parseHash`: `""` / `#` / `#/` / `#/tro-ly?x=1` / `#/javascript:alert(1)` / `#/kham-pha/%` ⇒ trang chủ; `#/kham-pha/bai/<mã hoá tên có dấu>` ⇒ đúng id có dấu; vòng `parseHash(baiHref(id)) == id` đúng; `#/kham-pha/bai/..%2F..%2F.env` ⇒ `baiId = "../../.env"` ⇒ server trả 404 (đã thử ở review backend) — giao diện hiện lỗi; `#/kham-pha/<img src=x>` ⇒ chỉ là chữ (React tự thoát), lĩnh vực lạ ⇒ trang báo không có.
  - bỏ số: "Huế đẹp [1]." ⇒ "Huế đẹp."; "[Nguồn 2]" / "[3][4]" ⇒ mất; chữ đang hiện dừng ở "[1" / "[ngu" / "[" ⇒ mất phần dở; link Markdown `[bài này](https://…)` **giữ nguyên**.
- Không chạy Playwright / server (Q-G / Q-N là S3 của C); không lượt có phí.

**Bất biến kiểm:** mọi chuỗi vào `dangerouslySetInnerHTML` đều đi qua DOMPurify với danh sách cho phép của `main` (đọc 3 chỗ gọi).
