# Review: Streaming S3 — giao diện đọc luồng (`frontend/app.js`) + chặn tải từ máy khác (C106 R2)

Decision: **changes_requested** (0 blocker / 1 major / 3 minor) · Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-6a`) · Date: 11:57 01/11/2026 (`date`) · Việc: C107 (A giao 01/11).
Bản kiểm: nhánh `s3-giao-dien` **`9374212`** + **`fc10873`** trên `887cbc5` — `git diff 887cbc5 fc10873` (5 file). Report người làm: `report_agent/2026-10-31_streaming_spec/s3_giao_dien_implementation.md`.
Spec: `docs/superpowers/specs/2026-10-31-streaming-design.md` (`00fb57ee01b2`) §4.7, §7 (phần giao diện). Tiền review: **≈ 0,0005 USD** (2 lần gọi thật — trần review 0,002).

## 1. Phạm vi đã review

- Cổng tối thiểu: worktree riêng `/tmp/c_s3` tại `fc10873` (đã gỡ); 5 đường dẫn đổi (`backend/api/app.py`, `backend/tests/test_static_ui.py`, `frontend/app.js`, `pyproject.toml`, `uv.lock`) khớp report,
  không file ngoài phạm vi; `git diff --check 887cbc5 fc10873` sạch; đọc exact diff; `pytest tests/test_static_ui.py tests/test_chat_stream.py -q` ⇒ **17 passed** (chạy lại, worktree của C).
- Đối chiếu spec §4.7: `fetch` POST route stream, `!response.ok` ⇒ nhánh lỗi cũ (`app.js` `ask`); `getReader()` + `TextDecoder({stream: true})`; parser chịu sự kiện cắt / nhiều sự kiện / bỏ dòng `:`;
  `status` ⇒ `#status`; `delta` ⇒ buffer, vẽ lại **cả** buffer theo `requestAnimationFrame` qua `marked` + `DOMPurify`, không `innerHTML +=`; link `[n]` chỉ bật ở `sources`; `error` ⇒ xoá chữ + lời
  báo + "Thử lại"; luồng đứt không `done` ⇒ như `error`; ô hỏi khoá khi chờ — **khớp** (đọc diff `app.js:71-161` trên `fc10873`).
- Không review lại: route stream (S2, đã đóng), các ca B đã chạy bằng đường thật (§4 report B) — dùng lại làm bằng chứng vì `fc10873` chỉ đổi cấu hình làm sạch + CSP, B đã chạy lại luồng thường và
  rời trang dưới CSP (report B §7).
- `playwright==1.58.*` nhóm dev: lock chỉ thêm 3 gói (`playwright`, `greenlet`, `pyee`) — khớp report; A đã duyệt (report B §1).

## 2. Findings

**M-1 (major) — "không tự tải từ máy khác khi hiện chữ" (mục tiêu `fc10873`, C106 R2) chưa đúng hết: DOMPurify còn để lọt 2 đường tải tự động, và trang `/static/index.html` không có CSP.**
- Vị trí: `fc10873:frontend/app.js:76-80` (`SANITIZE_OPTIONS`); `fc10873:backend/api/app.py:148` (`app.mount("/static", StaticFiles(directory=FRONTEND_DIR))`) ↔ `:152` (CSP chỉ gắn cho `/`).
- Bằng chứng (C chạy thật, Chromium headless 1208, server thật cổng 8795, gọi **chính** `renderAnswer` của trang với chữ tự dựng, đếm `page.on("request")` tới host lạ — cách B dùng, nhưng **bộ ca khác**:
  thuộc tính / thẻ không có trong danh sách FORBID):
  | Ca | `/` (có CSP) | `/static/index.html` (không CSP) | còn trong HTML |
  |---|---|---|---|
  | `<table background="http://…">` | 1 request, **bị CSP chặn** | **1 request đi ra** (0 thông báo CSP) | `table` + `background=` |
  | `<td background="http://…">` | 1, bị chặn | **1 đi ra** | `background=` |
  | `<input type="image" src="http://…">` | 1, bị chặn | **1 đi ra** | `input` + `src=` |
  | `<form action="http://…"><button>` | 0 (cần bấm; `form-action 'self'` chặn khi gửi) | 0 (cần bấm; **không** có `form-action` nào chặn) | `form` + `button` |
  | `link rel=stylesheet`, `meta refresh`, `a ping`, `body background`, `svg use` / `image`, `object`, `embed`, `picture source`, thẻ `style`, ảnh Markdown kiểu tham chiếu, `<img>` thô trong Markdown | 0 | 0 | bị gỡ ✓ |
  `/` có 4 thông báo vi phạm CSP (đúng 3 ca trên + 1), `/static/index.html` 0 ⇒ ở trang thứ hai chỉ còn lớp DOMPurify, và lớp đó thiếu `background` / `input`. TestClient: `GET /static/index.html` ⇒ 200,
  `text/html`, **không** header CSP (trang chạy đủ `app.js`, gọi được route stream).
- Tác động: trên trang chính `/` hôm nay **an toàn nhờ CSP** (lớp 2); mục tiêu "nhiều lớp độc lập" (skill `agent-security-review` mục 3) chưa đạt vì lớp DOMPurify hở, và có một URL thứ hai của cùng
  ứng dụng không có lớp CSP. Rủi ro gốc vẫn thấp (C106 R2: không bí mật trong ngữ cảnh) — nhưng đây là hành vi bảo mật mà commit tuyên bố, nên không hạ thành minor.
- Tiêu chí đóng (quan sát được): (1) `FORBID_ATTR` thêm `background` (và xét `poster`, `formaction`), `FORBID_TAGS` thêm `input`, `form`, `button` (câu trả lời không cần form) — hoặc cách tương đương
  (`ALLOWED_TAGS` danh sách cho phép thay vì danh sách cấm); (2) `/static/index.html` **không** phục vụ được trang không CSP — ví dụ dời `index.html` ra khỏi thư mục mount, hoặc gắn cùng header CSP cho
  mọi phản hồi `text/html`; (3) chạy lại ca dò của C (script private `data/streaming_s1_2026-11-01/s3_review_c107/probe.py`, 0 USD) ⇒ **0 request ra ngoài ở cả hai đường dẫn**, bất biến Markdown (§4) giữ;
  (4) test `test_static_ui.py` khoá điều (2) (ví dụ `/static/index.html` 404 hoặc có CSP).

**m-1 — test khoá tùy chọn làm sạch bằng chuỗi** (`fc10873:backend/tests/test_static_ui.py:18`: `'"img"' in js and '"style"' in js`) — đúng mục đích (chống lỡ xoá), nhưng không bắt được thiếu sót kiểu M-1.
Tiêu chí đóng: không bắt buộc; nếu sửa M-1 bằng danh sách cho phép thì đổi chuỗi khoá theo.

**m-2 — parser SSE không nhận `\r\n`** (`app.js` `createSseParser` tách theo `"\n\n"`): ca dò C — cùng luồng đổi `\n` ⇒ `\r\n` ra **0 sự kiện** (luồng sẽ bị coi là đứt). Server dự án gửi `\n`
(B đã ghi giới hạn này, report §5) ⇒ chỉ ghi lại; chỉ cần sửa nếu sau này có proxy đổi xuống dòng. Không mở vòng.

**m-3 — `report §4` "chữ đầu hiện sau 3.922 ms" và "hiện tới 62 ký tự rồi bị xoá"** là một lần chạy, đã ghi đúng là không phải đo D2. Không cần sửa — ghi để người đọc báo cáo khâu không lấy làm số tốc độ.

## 3. Cách người kiểm chạy lại thật

- Worktree `/tmp/c_s3` tại `fc10873` (symlink `data/`, `knowledge-base-hue/` — đã gỡ cùng worktree); `uv run --project /home/minhhieu/hue_rag`; server `uvicorn api.app:app --port 8795`
  (`HF_HUB_OFFLINE=1`, `--env-file` tuyệt đối) ⇒ `/health` 5 / 5 ready; đã tắt (TaskStop; `curl /health` không trả lời).
- **Ca dò 1 — làm sạch** (khác cách B: 16 ca thẻ / thuộc tính ngoài danh sách FORBID + 1 bất biến; chạy trên **cả** `/` và `/static/index.html`): kết quả M-1.
- **Ca dò 2 — parser SSE** (gọi chính `createSseParser` của trang, logic thuần): luồng 6 sự kiện (gồm dòng `: ping`, chữ có dấu tổ hợp + emoji, `\n` trong chữ) cắt ở **mọi** vị trí ký tự (268 cách) ⇒ 268 / 268
  giống bản không cắt; đưa từng ký tự một ⇒ giống; UTF-8 cắt giữa byte qua `TextDecoder({stream: true})` (mỗi 7 byte) ⇒ giống; `data:` nhiều dòng ⇒ ghép đúng; `\r\n` ⇒ 0 sự kiện (m-2).
- **Ca dò 3 — giao diện khi luồng lỗi / đứt** (khác cách B — B dùng trần token thật cho D3 (b)): lấy **một luồng thật** từ server 8795 (63 `delta`, `sources`, `done{success}`), rồi cho trình duyệt nhận
  (`page.route` + `fulfill`) **bản phát lại** của chính luồng đó: đủ / cắt sau 20 `delta` không `done` / cắt giữa một sự kiện / 20 `delta` + `error{citation_integrity_error, after_text: true}` + `done`.
  Đây là **phát lại**, không phải đường thật — dùng cho ca spec §7 ghi "không tạo được bằng đường thật" (luồng đứt, D3 (a)); kiểm logic xử lý của giao diện.
- **Bất biến** (hành vi phải giữ): route JSON `POST /api/chat` vẫn trả `{answer, sources}` 200 (1 lần gọi thật); Markdown thường (đậm, danh sách, bảng, link `https://`) qua `renderAnswer` giữ đủ.
- Số đo server: đúng **2** dòng `chat_metrics` cho 2 lần gọi (`success` ×2, vào 1.569 / 1.670, ra 165 / 39 token) — chép ở `data/streaming_s1_2026-11-01/s3_review_c107/chat_metrics.log` (private).
  Tiền ≈ (3.239 vào × 0,125 ghi đệm + 204 ra × 0,50) / 1M ≈ **0,0005 USD** (giá đủ; log nhánh này chưa có trường `cache_write_tokens` — ước theo B95: ghi đệm ≈ toàn bộ phần vào).

## 4. Kết quả quan sát

| Ca | Kết quả |
|---|---|
| Test file chạm (`test_static_ui.py`, `test_chat_stream.py`) | **17 passed** |
| Làm sạch — 16 ca: 12 bị gỡ hẳn; `form` còn (cần bấm mới gửi); 3 ca tải tự động lọt | 12 ✓ · 1 ghi chú · 3 ✗ (dòng dưới) |
| Làm sạch — `background` (table, td), `input type=image` | **lọt** — `/`: CSP chặn; `/static/index.html`: request đi ra (M-1) |
| `/static/index.html` có CSP | **không** (M-1) |
| Bất biến Markdown thường | giữ: `<strong>`, 2 `<li>`, `<table>`, link `https://` |
| Parser: 268 vị trí cắt, từng ký tự, UTF-8 cắt giữa byte, `data:` nhiều dòng | 268 / 268 · giống · giống · đúng |
| Parser: `\r\n` | 0 sự kiện (m-2, không cần với server dự án) |
| Phát lại luồng đủ | 158 ký tự, 1 link `[n]` ↔ 1 thẻ nguồn, không "Thử lại", ô hỏi mở |
| Phát lại cắt không `done` / cắt giữa sự kiện | chữ **0**, 0 nguồn, lời báo "Kết nối bị gián đoạn…", "Thử lại" hiện; bấm ⇒ đúng **1** yêu cầu mới |
| Phát lại `error` sau chữ (dạng D3 (a)) | chữ 0, lời báo đúng thông điệp lỗi trích dẫn, "Thử lại" hiện; bấm ⇒ 1 yêu cầu mới |
| Route JSON `/api/chat` | 200, `{answer, sources}` |

Ghi chú: ở bản phát lại, chữ không kịp hiện (`max` 0) vì cả thân tới một lần — khung hình vẽ bị huỷ khi `error` tới; "hiện rồi xoá" đã được B chạy bằng đường thật (D3 (b), report §4).

## 5. Giới hạn hoặc phần chưa chạy

- D3 (a) thật và luồng đứt thật vẫn **chưa kiểm bằng đường thật** (đúng spec §7); C chỉ thêm bằng chứng logic qua bản phát lại.
- Không chạy lại các ca rời trang / trần token của B (dùng lại — lý do ở §1). Không đo tốc độ (S4).
- Không kiểm trình đọc màn hình / điện thoại / Firefox / Safari (chỉ Chromium 1208).
- Script dò (private) giữ ở `data/streaming_s1_2026-11-01/s3_review_c107/` (`probe.py`, `replay.py`, `probe_sanitizer_parser.json`); bản luồng thật dùng phát lại đã xoá cùng `/tmp` (chứa chữ trả lời).

## 6. Decision và bước tiếp theo

`changes_requested` — B sửa M-1 (m-1 tùy theo cách sửa); C kiểm phần sửa bằng cách chạy lại ca dò 1 trên cả hai đường dẫn (0 USD) + test. m-2, m-3 không mở vòng.

# Vòng 2 — kiểm phần sửa `716ba4d` (C, 12:08 01/11/2026 `date`)

Decision: **ready_for_user_confirmation** (M-1 đóng; m-1 đổi theo cách sửa — đóng; m-2, m-3 giữ như vòng 1, không mở vòng) · 0 USD (server chạy **không** nạp key — không thể gọi model).

- Cổng: `git diff --stat fc10873 716ba4d` = 3 file (`backend/api/app.py`, `backend/tests/test_static_ui.py`, `frontend/app.js`), khớp tin B; `git diff --check` sạch; worktree riêng `/tmp/c_s3` tại `716ba4d`
  (đã gỡ); `pytest tests/test_static_ui.py tests/test_chat_stream.py -q` ⇒ **17 passed**.
- Đọc diff: `SANITIZE_OPTIONS` thành **danh sách cho phép** (`ALLOWED_TAGS` 25 thẻ Markdown thường, `ALLOWED_ATTR` `href`, `title`, `align`, `start` — không thuộc tính nào khác chứa URL);
  `FrontendStaticFiles` gắn cùng `FRONTEND_CSP` cho phản hồi `text/html` dưới `/static` (không middleware HTTP chung — đúng lý do: không bọc luồng SSE); test khoá `/static/index.html` có CSP = `/`,
  `/static/app.js` không, tùy chọn là allowlist không chứa `img` / `input` / `form` / `style` / `background` / `src`.
- Server thật (cổng 8795): `curl -sI /static/index.html` ⇒ có `content-security-policy`; `/static/app.js` ⇒ không (0).
- **Chạy lại ca dò 1 của C** (bản mở rộng `probe_v2.py`: 16 ca vòng 1 + 9 ca mới — `javascript:` href, `<img onerror>`, danh sách việc `- [x]`, khối code có ngôn ngữ, danh sách số bắt đầu từ 3, bảng căn lề,
  `video poster`, `button formaction`, `area href`) trên **cả** `/` và `/static/index.html`:
  | | `/` | `/static/index.html` |
  |---|---|---|
  | request ra máy khác (tổng mọi ca) | **0** | **0** |
  | thuộc tính tải được còn lại (`background`, `src`, `ping`, `srcset`, `style`, href ngoài lạ) | 0 | 0 |
  | cờ XSS `window.__xss` | không đặt | không đặt |
  | `<form>` còn | không | không |
  | bất biến Markdown (đậm, 2 `<li>`, bảng, link `https://`) | giữ | giữ |
  | danh sách số `start="3"` · bảng `align` · code `<pre><code>` | giữ · giữ · giữ | như `/` |
  Còn `<table>` ở 2 ca `background` nhưng **không** còn thuộc tính `background` ⇒ không tải. Mỗi trang có 1 thông báo CSP — **không** phải request ra ngoài (0 request); khả năng là thẻ / thuộc tính `style`
  trong chữ thử lúc DOMPurify phân tích (B đã ghi hiện tượng này, report §7) — chưa xác định từng dòng.
- Parser SSE: 268 / 268 vị trí cắt, từng ký tự, UTF-8 cắt giữa byte — vẫn đạt.
- Ghi chú (không phải finding): danh sách việc Markdown `- [x]` mất ô đánh dấu (thẻ `input` không nằm trong allowlist) — đúng chủ ý chặn `input`; câu trả lời của chatbot hiếm khi dùng; khối code mất
  `class="language-…"` (không ảnh hưởng hiển thị hiện tại — trang không tô màu code).
- Bằng chứng private: `data/streaming_s1_2026-11-01/s3_review_c107/probe_v2.py`, `probe_v2_716ba4d.json`. Không chạy lại phần phát lại luồng (ca dò 3) — `716ba4d` không đổi `readAnswerStream` /
  `handleEvent` / `createSseParser` (diff chỉ đổi `SANITIZE_OPTIONS`) ⇒ dùng lại kết quả vòng 1.
