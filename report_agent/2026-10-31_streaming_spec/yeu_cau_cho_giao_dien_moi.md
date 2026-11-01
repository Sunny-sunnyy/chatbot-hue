# Yêu cầu giao diện mới (sau Phase 8) PHẢI giữ từ streaming — làm lại đúng một lần

C, 12:44 01/11/2026 (`date`). Nguồn: spec `docs/superpowers/specs/2026-10-31-streaming-design.md` (`00fb57ee01b2`) §4.4, §4.7, D3; code tham chiếu **`716ba4d`** (`backend/api/routes/chat.py` = `chat.py`,
`backend/api/app.py` = `app.py`, `frontend/app.js` = `app.js`). Giao diện JS thuần hiện tại sẽ bỏ — đây là hợp đồng để bản mới không phải tìm lại.

**Gọi API và lỗi trước luồng**
1. `POST /api/chat/stream` thân `{"query": "…"}` (1–500 ký tự). `!response.ok` ⇒ thân là JSON `{"error": {code, message}}` như `/api/chat` (lỗi trước khi mở luồng) — `chat.py:222-252`, `app.js:173-181`.
2. Thành công ⇒ `text/event-stream`, header `Cache-Control: no-cache`, `X-Accel-Buffering: no` (proxy khi deploy phải không đệm) — `chat.py:253-256`.

**Hợp đồng sự kiện SSE** (`event:` + `data:` JSON, cách nhau bằng dòng trống; dòng bắt đầu `:` là chú thích — bỏ) — `chat.py:269-328`, parser `app.js:104-121`
3. `status` `{"stage": "searched", "n_sources": n}` rồi `{"stage": "generating"}` ⇒ chỉ hiện chữ trạng thái, không hiện tên nguồn trước — `chat.py:343, :349`; `app.js:125-126`.
4. `delta` `{"seq": k, "text": "…"}`: `seq` tăng dần; chỉ nối mảnh có `seq` mới — `chat.py:288-293`; `app.js:127-131`.
5. `sources` (danh sách như `SourceResponse`: `id`, `title`, `heading_path`, `excerpts`) chỉ tới khi kiểm trích dẫn **qua** — `chat.py:303-316`; câu từ chối không gọi model: `delta` câu chuẩn + `sources` rỗng + `done` — `chat.py:298-301`.
6. `error` `{"code", "message", "after_text": bool}`; `done` `{"outcome"}` luôn là sự kiện cuối — `chat.py:303-328`, `:295`.
7. Parser phải chịu được một sự kiện bị cắt qua nhiều lần đọc, nhiều sự kiện trong một lần đọc, UTF-8 cắt giữa byte (`TextDecoder` `stream: true`) — `app.js:104-121, :148-160`
   (C kiểm 268 / 268 vị trí cắt — `s3_giao_dien_review.md`). Server dự án gửi `\n`, không `\r\n`.

**Hiển thị — D3 (User 31/10)**
8. Chữ hiện dần: vẽ lại **cả** buffer theo khung hình, luôn qua bộ lọc HTML; không `innerHTML +=` theo mảnh — `app.js:84-94`.
9. Link `[n]` (trỏ thẻ nguồn) **chỉ bật sau `sources`**; trước đó `[n]` là chữ thường — `app.js:132-138` (`wireCitations` `app.js:39`).
10. `error` (kiểm cuối hỏng = rút lại; lỗi / đứt giữa chừng = xoá) ⇒ **xoá hết** chữ + nguồn đã hiện, hiện `message` + nút **"Thử lại"** (gửi lại đúng câu, một yêu cầu) — `app.js:139-141, :184-187`.
11. Luồng kết thúc mà **không có `done`** ⇒ xử lý như `error` ("Kết nối bị gián đoạn. Vui lòng thử lại.") — `app.js:71, :162`.
12. Ô hỏi / nút gửi **khoá** khi đang chờ (không hai câu chồng nhau); không nút "Dừng" ở bản này — `app.js:11-16` (spec §2).

**An toàn khi hiện chữ do model viết** (rà bảo mật C106 R2; review S3)
13. Lọc HTML theo **danh sách cho phép**: 25 thẻ Markdown thường (`p br hr strong em del code pre blockquote ul ol li h1–h6 a table thead tbody tr th td`) và **4 thuộc tính** `href`,
    `title`, `align`, `start` — không thẻ / thuộc tính nào tự tải tài nguyên (ảnh, media, `style`, `background`, form…) — `app.js:77-81`. Đổi thư viện Markdown ⇒ giữ đúng danh sách này.
14. **CSP cho mọi trang HTML** của giao diện (cả trang phục vụ dưới `/static`): `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; object-src 'none';
    base-uri 'none'; form-action 'self'; frame-ancestors 'none'` — `app.py:33-34, :37-46, :163`. Bản build (React / Vite…) không được cần script nội dòng hay `eval` (nếu cần ⇒ nonce, không nới CSP).
15. Không nạp script / font / CSS từ CDN: thư viện để trong bản build, phục vụ từ chính server (`test_static_ui.py` khoá điều này cho bản cũ).
16. Link ngoài trong câu trả lời chỉ mở khi người dùng **bấm**; ảnh hợp lệ sau này phải phục vụ từ chính server.

**Ngắt**
17. Rời trang / đóng tab / bấm hỏi lại ⇒ huỷ `fetch` (đóng kết nối) để server dừng model và ghi một dòng `client_disconnected` — server xử lý ở `chat.py:379-400`; giao diện mới nên gọi
    `AbortController.abort()` khi bỏ câu đang chờ (bản cũ dựa vào trình duyệt đóng kết nối khi rời trang).

**Kiểm khi làm lại** (một lần, Playwright, server thật): chữ hiện dần + link chỉ bật sau `sources`; ca `error` sau chữ (trần token nhỏ — S3 §4); phát lại luồng cắt / không `done`; 25 ca dò lọc HTML ⇒ 0 request ra ngoài
trên mọi trang (`data/streaming_s1_2026-11-01/s3_review_c107/probe_v2.py`); 0 vi phạm CSP ở luồng thường.
