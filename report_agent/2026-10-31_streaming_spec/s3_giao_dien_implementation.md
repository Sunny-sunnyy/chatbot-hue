# Implementation Report: Streaming S3 — giao diện đọc luồng (`frontend/app.js`)

Người làm: B (Claude Opus 5.5)
Date: 11:46 01/11/2026 (`date`)
Spec: `docs/superpowers/specs/2026-10-31-streaming-design.md` (`00fb57ee01b2`) §4.7, §5 hàng S3, §7 phần giao diện. Mục việc: tin A 01/11 (S3).
Nhánh: `s3-giao-dien`, commit **`9374212`** + **`fc10873`** (§7, rà bảo mật C106 R2), dựng trên `887cbc5` (S2 + sửa m-1 review S2) — đã push `origin`. Worktree `/tmp/b_s3`. Không merge (A chờ S2 ready rồi mới gộp).

## 1. Phạm vi

Sửa tối thiểu `frontend/app.js` (JS thuần) để giao diện dùng `POST /api/chat/stream`; `index.html` không cần sửa (đã có `#status` `aria-live="polite"`, nút "Thử lại").
Thêm `playwright` vào nhóm **dev** (A duyệt 01/11) cho phép kiểm bằng trình duyệt thật. Không đo D2 (S4), không đổi backend.

## 2. Thay đổi chính

| File | Đổi gì |
|---|---|
| `frontend/app.js` (+91 / −10) | `fetch` POST `/api/chat/stream`; `!response.ok` ⇒ đọc JSON lỗi như cũ (lỗi trước luồng, cách (b)). `readAnswerStream`: `response.body.getReader()` + `TextDecoder({stream: true})`; `createSseParser` giữ phần sự kiện dở giữa hai lần `read()`, tách nhiều sự kiện trong một lần, bỏ dòng chú thích `:`. `status` ⇒ chữ ở `#status` (không hiện số / tiêu đề nguồn). `delta` ⇒ chỉ nối `seq` mới, vẽ lại **cả** buffer bằng `marked` + `DOMPurify` theo `requestAnimationFrame` (không `innerHTML +=`). `sources` ⇒ vẽ bản cuối rồi `renderSources` + `wireCitations` (link `[n]` chỉ bật lúc này). `error` (D3 (a) và (b)) hoặc luồng hết mà không có `done` ⇒ **xóa** chữ đã hiện + nguồn, hiện lời báo, hiện "Thử lại". Ô hỏi + nút gửi khóa trong lúc chờ (như cũ). `renderResponse` (đường JSON) bỏ vì giao diện không gọi `/api/chat` nữa — route JSON vẫn giữ cho bộ đánh giá / máy khác |
| `pyproject.toml`, `uv.lock` | nhóm `dev = ["playwright==1.58.*"]` (`uv add --no-sync --group dev`); lock **chỉ thêm** 3 gói: `playwright` 1.58.0, `greenlet` 3.5.6, `pyee` 13.0.1. Chọn 1.58 vì gói này đi kèm Chromium build **1208** — đúng bản đã có trong `~/.cache/ms-playwright` ⇒ không tải trình duyệt. Cài vào `.venv` của dự án: `UV_PROJECT_ENVIRONMENT=/home/minhhieu/hue_rag/.venv uv sync --project /tmp/b_s3 --inexact` (dry-run trước: chỉ +3 gói, không gỡ gói nào; dự án không có `build-system` nên không cài lại code dự án) |

Công cụ kiểm (private, dùng lại cho S4): `data/streaming_s1_2026-11-01/tools/s3_ui_check.py` — Chromium headless, trang thật trên server thật, **không** chặn / giả mạng; MutationObserver ghi
độ dài chữ, số link `[n]`, số thẻ nguồn, trạng thái ô hỏi theo thời gian; chỉ in số đếm / cờ, không in chữ trả lời.

## 3. Cách đã chạy thật

Server từ `/tmp/b_s3/backend` (`uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`, `--env-file` tuyệt đối): production `uvicorn api.app:app --port 8793`; server trần token ra nhỏ
`data/streaming_s1_2026-11-01/tools/run_server.py --port 8794 --max-output-tokens 250` rồi `400` (đổi trong bộ nhớ). Script: `/home/minhhieu/hue_rag/.venv/bin/python -I …/s3_ui_check.py
--base-url … --case <ca> [--query "<câu tự viết>"]`. Kết quả `data/streaming_s1_2026-11-01/s3/*.json` + `metrics_all.log`. Test: `pytest tests/test_static_ui.py tests/test_chat_stream.py -q`.

## 4. Kết quả quan sát

| Ca (spec §7) | Kết quả |
|---|---|
| Chữ hiện dần (câu trong kho, so sánh / mô tả) | **PASS** — 83 độ dài khác nhau của `#answer` trước khi có nguồn, chỉ tăng; chữ đầu hiện sau 3.922 ms tính từ lúc bấm (một lần, không phải đo D2); cuối 647 ký tự |
| Link `[n]` bật sau `sources` | **PASS** — 0 link trong suốt lúc chữ chạy; sau `sources`: 6 link, 5 thẻ nguồn, **0** link trỏ tới thẻ không có |
| Ô hỏi khóa khi đang chờ | **PASS** — khóa ở mọi mốc lúc chữ đang chạy; mở lại khi xong |
| Câu ngoài kho | **PASS** — câu từ chối hiện dần (7 độ dài), 0 nguồn, 0 link; server `refusal: true` |
| Ngắt thật — rời trang trước chữ đầu (đợi "Đang viết…" rồi `goto about:blank`) | **PASS** — server: 1 dòng `client_disconnected`, token `None`; `chat_stream_drain` `finished: true` 0,1 ms |
| Ngắt thật — rời trang khi chữ đang hiện (34 ký tự) | **PASS** — server: 1 dòng `client_disconnected`; drain `finished: true` 0,8 ms |
| D3 (b) lỗi **sau** khi đã hiện chữ (trần 400 ⇒ `response.incomplete`) | **PASS** — chữ hiện tới 62 ký tự rồi **bị xóa hết** (cuối 0 ký tự, 0 nguồn); `#status` "Không thể tạo câu trả lời vào lúc này."; "Thử lại" hiện; server `stream_error_after_text` |
| Lỗi **trước** chữ đầu (trần 250 ⇒ hết token trong phần suy luận) + "Thử lại" | **PASS** — 0 chữ, lời báo + "Thử lại"; bấm "Thử lại" ⇒ đúng **1** yêu cầu mới (tổng 2), cùng câu; lần 2 cũng hết token (server cùng trần) ⇒ lại lời báo + "Thử lại"; server 2 dòng `generation_failed` |
| Markdown / XSS qua DOMPurify (gọi `renderAnswer` của chính trang với chữ tự dựng) | **PASS** — link `javascript:`: bị bỏ; `<img onerror>` + `<script>`: bỏ cả hai, cờ `window.__xss` không bị đặt; `<iframe>`: bỏ; Markdown thường (in đậm, danh sách, link `https://`): giữ đúng. **Quan sát:** thuộc tính `style` được giữ (mặc định DOMPurify) — xem §5 |
| Test | **PASS** `test_static_ui.py` + `test_chat_stream.py` 17 passed (khóa `DOMPurify.sanitize(marked.parse(` vẫn đúng) |

**Server:** 7 lần gọi ⇒ 7 dòng `chat_metrics` (`success` ×2, `client_disconnected` ×2, `generation_failed` ×2, `stream_error_after_text` ×1). Cả hai server đã tắt (`curl /health` không trả lời).
Cách ghi số "chỉ tăng" ở ca D3 (b) báo `false` vì mốc cuối là lúc xóa chữ (đúng hành vi).

**Tiền (gồm §7):** 3 lần gọi trọn: vào 5.022 / ra 806 token (≈ 0,0010 USD theo giá đủ). 6 lần ngắt / hết token không có usage — ước trên ≈ 0,0020 USD (vào ≈ 1.850 / lần ghi đệm, ra ≤ ~1.300
cộng lại). **≈ 0,0030 USD cận trên — chạm trần 0,003** (số thật thấp hơn: phần ước là cận trên). Không chạy thêm lượt có phí cho S3.

## 5. Lỗi và giới hạn

- **D3 (a)** (bộ kiểm cuối hỏng sau khi đã hiện chữ ⇒ rút lại): giao diện dùng **cùng** nhánh `error` với D3 (b) (đã chạy thật ở trên), nhưng sự kiện `citation_integrity_error` thật chưa gặp
  (0 / 489 lần, không tham số thật nào ép) ⇒ **chưa kiểm bằng đường thật** — đúng giới hạn spec §7.
- **Luồng đứt không có `done`**: có nhánh xử lý (coi như lỗi) — chưa kiểm bằng đường thật (chỉ xảy ra khi server chết / mạng đứt = đổi môi trường; spec §7).
- ~~`style` giữ lại qua DOMPurify mặc định~~ — đã bỏ ở `fc10873` (A đồng ý, §7).
- Kiểm XSS gọi `renderAnswer` trực tiếp trong trang thật với chữ tự dựng (model thật không sinh được các chuỗi này theo ý) — kiểm đúng code marked + DOMPurify chạy trên trang, không qua luồng model.
- Parser SSE tách sự kiện theo `\n\n` (server gửi `\n`); không xử lý `\r\n` (không cần với server của dự án).
- Không kiểm trình đọc màn hình, điện thoại, mạng yếu (spec §10). Thời gian trong bảng là một lần chạy, không phải lượt đo D2 (S4).

## 6. Bàn giao cho người kiểm

- Đọc: `git diff 887cbc5 fc10873` (5 file); spec §4.7, §7; §7 dưới.
- Chạy lại (server thật, ≈ 0,0005 USD): ca `stream` + 1 ca rời trang của `s3_ui_check.py`. Ca dò khác cách (W32) gợi ý: SSE bị cắt giữa một sự kiện ở nhiều chỗ khác nhau (proxy / `curl --limit-rate`);
  câu trả lời có Markdown bảng / danh sách dài để xem vẽ lại theo khung hình không nhấp nháy.
- Bàn giao chỉ khi A báo S2 ready (A 01/11: S2 review ready; m-1 đã sửa ở `887cbc5`, chờ A kiểm phần sửa).

**Giải thích ngắn:** trang hỏi đáp giờ hiện chữ trả lời dần ngay khi model viết, thay vì chờ cả câu; link nguồn `[n]` chỉ bật khi câu đã qua kiểm trích dẫn; nếu giữa chừng lỗi hoặc kiểm
không đạt thì trang xóa chữ đã hiện và mời "Thử lại", để người dùng không giữ lại chữ chưa được kiểm. Người dùng rời trang giữa chừng thì server dừng model và vẫn ghi đúng một dòng số đo.

## 7. Thêm sau giao việc: không tự tải từ máy khác khi hiện chữ (rà bảo mật C106 R2, A quyết — 11:51 01/11/2026, `date`)

**Vì sao:** chữ trả lời là Markdown do model viết; `![](https://…)`, `<img>`, `<video>`, CSS `background:url(…)` làm trình duyệt người dùng **tự** gọi máy lạ lúc hiện chữ (lộ IP / lúc đọc).
DOMPurify mặc định chặn script nhưng **giữ** `<img>` và `style`.

| Sửa (commit `fc10873`) | |
|---|---|
| `frontend/app.js` | `DOMPurify.sanitize(marked.parse(text), SANITIZE_OPTIONS)`: `USE_PROFILES: {html: true}` (bỏ SVG / MathML), `FORBID_TAGS` img, picture, source, video, audio, track, iframe, object, embed; `FORBID_ATTR` style, srcset. Link thường giữ (chỉ mở khi người dùng bấm) |
| `backend/api/app.py` | header **Content-Security-Policy** cho trang `/`: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`. Thêm được vì: trang chỉ nạp `/static/…` (`index.html:7, :33-35`), không script / style nội dòng, `marked.umd.js` + `purify.min.js` không dùng `eval` / `new Function` (`grep` = 0) |
| `backend/tests/test_static_ui.py` | `/` có header CSP `default-src 'self'`; `app.js` có tùy chọn bỏ `img` + `style` |

**Kiểm thật (Chromium headless, server thật `8793` có CSP; mọi request ra ngoài bị trình duyệt hủy tại chỗ nhưng vẫn đếm qua `page.on("request")` ⇒ không gói tin nào rời máy):**

| Ca | Kết quả |
|---|---|
| `![x](https://…)`, `<img src=https://…>`, `<video src=https://…>`, `<p style="background:url(https://…)">`, `<svg><image href=https://…>` qua `renderAnswer` | **0** request ra ngoài; HTML ra không còn `<img>` / `<video>` / `<svg>` / `style=` |
| Đối chứng dương: cùng chữ ảnh ngoài nhưng làm sạch bằng cấu hình **mặc định** | **1** request ra ngoài (bị CSP chặn: "Loading the image … violates … img-src 'self'") ⇒ phép đếm bắt được ca hỏng |
| XSS cũ (`javascript:`, `onerror`, `<script>`, `<iframe>`) | vẫn bị gỡ; cờ `window.__xss` không đặt |
| Markdown thường (in đậm, danh sách, link `https://`) | giữ đúng |
| Luồng thường dưới CSP (câu trong kho) | **0** vi phạm CSP; chữ hiện dần 81 độ dài, 0 link trước `sources`, 7 link / 6 thẻ, 0 link mồ côi |
| Rời trang giữa chừng dưới CSP | 0 vi phạm; server 1 dòng `client_disconnected`, drain xong 0,7 ms |
| Test | `test_static_ui.py` 2 passed |

**Ghi chú công cụ:** `page.wait_for_function` của Playwright dựng điều kiện bằng `eval` trong trang ⇒ bị CSP mới chặn (lần chạy đầu ca stream lỗi `EvalError` — lỗi của công cụ kiểm, không phải
của trang) ⇒ `s3_ui_check.py` đổi sang vòng chờ `page.evaluate` (không bị CSP trang chặn). 2 vi phạm "inline style" thấy ở ca thử có `style=` là lúc DOMPurify đọc chữ thử — bị chặn, vô hại.

**Giới hạn:** CSP chỉ gắn cho trang `/` (tài nguyên `/static` và API JSON không cần); người dùng vẫn mở được link ngoài khi **bấm** (đúng ý: link nguồn / tham khảo). Ảnh hợp lệ trong câu trả lời (nếu
sau này kho có ảnh) sẽ không hiện — cần thiết kế riêng (ảnh phục vụ từ chính server).

## 8. Sửa theo review C107 (`s3_giao_dien_review.md` `d5c144357d65`) — 12:06 01/11/2026 (`date`)

**M-1** (danh sách cấm của DOMPurify sót `background` ở `table` / `td`, `<input type="image">`, form; trang `/static/index.html` chạy được app mà **không** có CSP ⇒ 3 request thật ra ngoài) —
sửa ở commit **`716ba4d`** (nhánh `s3-giao-dien`, đã push):

| Sửa | |
|---|---|
| `frontend/app.js` | `SANITIZE_OPTIONS` đổi sang **danh sách cho phép**: `ALLOWED_TAGS` = đúng thẻ marked tạo cho Markdown thường (p, br, hr, strong, em, del, code, pre, blockquote, ul, ol, li, h1–h6, a, table, thead, tbody, tr, th, td — B `grep` `marked.umd.js`); `ALLOWED_ATTR` = href, title, align, start. Bỏ ô tick danh sách việc (`<input type=checkbox>`) và `class` của khối code — không cần |
| `backend/api/app.py` | `FrontendStaticFiles` (con của `StaticFiles`): trang `text/html` phục vụ dưới `/static` mang **cùng** CSP như `/`. Không dùng middleware HTTP chung vì `BaseHTTPMiddleware` bọc cả luồng SSE |
| `backend/tests/test_static_ui.py` | `/static/index.html` 200 + CSP giống `/`; `/static/app.js` không cần CSP; tùy chọn làm sạch là danh sách cho phép, không có thẻ / thuộc tính tải được (`img`, `input`, `form`, `style`, `background`, `src`) — m-1 của C |

**Kiểm (server thật 8793, Chromium headless):**
- Header: `/` có CSP, `/static/index.html` có CSP, `/static/app.js` không (đúng ý).
- **Ca dò của C** `data/streaming_s1_2026-11-01/s3_review_c107/probe.py` (chạy lại nguyên văn): **0** request ra ngoài ở **cả** `/` lẫn `/static/index.html` (trước: 3 ở đường `/static`);
  `table` còn nhưng không còn `background=`; `form` / `input` / `img` / `svg` … bị gỡ; bất biến Markdown giữ (`<strong>`, 2 `<li>`, `<table>`, link `https://`); parser 268 / 268 cách cắt đúng,
  UTF-8 cắt giữa byte đúng. Kết quả `data/streaming_s1_2026-11-01/s3/c107_probe_after_fix.json`. 1 thông báo CSP mỗi đường = ca `<style>` của chữ thử (style nội dòng bị chặn lúc DOMPurify đọc chữ; không tải gì, thẻ bị gỡ); nạp trang: 0.
- 1 câu thật qua trang (danh sách cho phép không làm hỏng chữ thật): chữ hiện dần 79 độ dài, 0 link trước `sources`, 7 link / 4 thẻ, 0 link mồ côi, **0** vi phạm CSP. Vào 1.714 / ra 249 token ≈ 0,00034 USD (giá đủ).
- `pytest tests/test_static_ui.py tests/test_chat_stream.py` 17 passed (lần đầu 1 fail vì test khóa bắt nhầm `querySelector("form")` của trang ⇒ test chỉ xét khối `SANITIZE_OPTIONS`).

**m-2** (parser không nhận `\r\n`): **không sửa** — server dự án gửi `\n`; đổi `\r\n` ⇒ `\n` theo từng mảnh có bẫy (mảnh kết bằng `\r`, mảnh sau bắt đầu `\n` ⇒ thành hai dòng trống = ranh giới sự kiện giả).
Giữ ở giới hạn §5. **m-1**: đã đổi theo (trên). **m-3**: không cần sửa (số một lần, đã ghi không phải D2).

Tiền thêm ≈ 0,00034 USD (trần lần sửa 0,001).
