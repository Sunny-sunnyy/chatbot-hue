# Implementation Report: B121 — giao diện mới (React + Vite + Tailwind)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-d6`) · 10:16 02/11/2026 (`date`) · Việc: `session_prompt/CURRENT_HANDOFF.md` mục B121 (A giao 09:53 02/11/2026).
Nhánh `giao-dien-moi` từ `main` `411bbc5`, worktree `/tmp/b_giao_dien`. Guide: `guides/phase_6_generation_api.md` mục "Hiện hành" (việc ghi rõ "lệnh build ghi vào guide").
Nhãn: **[Chạy]** = đã chạy thật trên bản build cuối · **[Tự dựng]** = luồng SSE tự dựng qua Playwright `page.route` (kiểm logic phía trình duyệt; trang, CSP, bundle thật; không phải đường thật) · **[Code, chưa chạy]**.

## Căn cứ để review
1. Diff nhánh `giao-dien-moi` so với `411bbc5` — `frontend/src/` (5 file, 426 dòng), `backend/api/app.py`, `backend/tests/test_static_ui.py`, `.gitignore`, guide Phase 6 "Hiện hành".
2. `report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md` (17 yêu cầu) + `report_agent/2026-11-01_giao_dien_moi/b116_so_sanh_giao_dien.md` (yêu cầu 18, bố cục, màu, 6 trạng thái, mục dò CSP).
3. Bằng chứng (private): `data/giao_dien_moi_2026-11-01/do_csp/` (dò Radix), `data/giao_dien_moi_2026-11-01/b121/` (script, JSON kết quả, log, ảnh `anh/`).

## 1. Phạm vi
- Thay `frontend/` JS thuần bằng React + Vite + Tailwind; FastAPI phục vụ bản build `frontend/dist/`. Chỉ trang hỏi đáp + khung nguồn bên cạnh; laptop trước, điện thoại không vỡ.
- **Không đổi:** API, thân SSE, CSP (`FRONTEND_CSP` giữ nguyên từng chữ), route `/api/chat`. Không thêm tính năng Phase 9. Streaming giữ **PA1** (chữ hiện dần).
- Gói: đúng danh sách User duyệt 09:53, **trừ** shadcn / Radix — dò xong thì không dùng gói nào (mục 4.1; A đồng ý).

## 2. Thay đổi chính
| File | Làm gì |
|---|---|
| `frontend/src/stream.js` | gọi `/api/chat/stream`, bộ tách SSE (chuyển nguyên logic `app.js` cũ), luồng đứt / `error` ⇒ ném lỗi có lời báo; nhận `signal` để **huỷ `fetch`** (yêu cầu 17 — bản cũ chưa có) |
| `frontend/src/markdown.js` | `marked` → `DOMPurify` với **đúng** danh sách cho phép cũ (25 thẻ / 4 thuộc tính); đổi `[n]` **và** `[Nguồn n]` (cùng mẫu với `backend/llm/citations.py`) thành số nhỏ nâng lên — mờ khi chưa có `sources`, link khi có; đổi trên nút chữ sau bộ lọc, phần tử dựng bằng DOM trong `<template>` (trơ), bỏ qua chữ trong `a` / `code` / `pre` |
| `frontend/src/App.jsx` | trang + trạng thái (chưa hỏi / đang tìm / đang viết / xong / từ chối / lỗi — bảng B116); vẽ lại cả buffer tối đa một lần mỗi khung hình; lọc mảnh theo `seq`; lỗi ⇒ xoá chữ + nguồn, hộp lỗi + "Thử lại"; khoá ô hỏi khi chờ; bấm số nguồn ⇒ nguồn sáng (`accent-soft`) + focus; đoạn trích gập bằng `<details>`; Enter gửi, Shift + Enter xuống dòng, bỏ Enter khi bộ gõ đang ghép chữ; `pagehide` ⇒ huỷ `fetch`; **nhãn yêu cầu 19** dưới ô hỏi |
| `frontend/src/index.css` | 12 token màu B116 (`bg` ⇒ `page`, `text` ⇒ `ink` để tránh lớp `bg-bg`, `text-text`), font Be Vietnam Pro, kiểu chữ cho HTML câu trả lời (Tailwind xoá kiểu mặc định) |
| `frontend/package.json`, `package-lock.json`, `.npmrc`, `vite.config.js`, `index.html`, `src/main.jsx` | 5 gói chạy + 4 gói build, khoá đúng phiên bản; `.npmrc`: `ignore-scripts`, `save-exact`, `before=2026-10-19` (chỉ lấy bản phát hành ≥ 2 tuần); Vite `base: "/static/"`; font tự host (latin + vietnamese, 400 + 600) |
| `backend/api/app.py` | `FRONTEND_DIR` ⇒ `frontend/dist`; thiếu bản build ⇒ log cảnh báo kèm lệnh (API vẫn chạy). CSP, `FrontendStaticFiles`, route `/` giữ nguyên |
| `backend/tests/test_static_ui.py` | 3 test: bản build chạy được dưới CSP (script chỉ `type=module src=/static/assets/…`, không nội dòng, không `http(s)://`, bundle 0 `eval` / `new Function`); bộ lọc vẫn là danh sách cho phép không có thẻ tải tài nguyên; `/` + `/static/index.html` cùng CSP, mọi tài nguyên trong `index.html` trả 200 không CSP. Thiếu bản build ⇒ báo lệnh cần chạy |
| `.gitignore` | `frontend/node_modules/`, `frontend/dist/` (không commit bản build — chạy `npm ci && npm run build`) |
| xoá | `frontend/app.js`, `styles.css`, `index.html` cũ, `vendor/marked.umd.js`, `vendor/purify.min.js` |

Gói (phiên bản trong lockfile): react / react-dom 19.3.1, marked 18.1.1, dompurify 3.4.17, @fontsource/be-vietnam-pro 5.3.0; build: vite 8.3.4, @vitejs/plugin-react 6.1.2,
tailwindcss / @tailwindcss/vite 4.3.3. Lockfile: 86 gói, 86 / 86 có `integrity`, mọi `resolved` là `registry.npmjs.org` [Chạy]. Bản build: JS 303 kB (gzip 97 kB), CSS 13 kB, font woff2 4 file ~67 kB.

## 3. Cách đã chạy thật
- Dò CSP: `/tmp/b_csp_probe` (ngoài repo) dựng Vite + React + Tailwind + 5 linh kiện Radix, `npm run build`; phục vụ bằng **chính** `FRONTEND_CSP` + `FrontendStaticFiles` import từ `api.app`
  (`do_csp/serve_dist.py`, cổng 8811); `do_csp/probe_radix.py` (mỗi linh kiện một trang `?only=`, nghe `securitypolicyviolation` + console + request ra ngoài) + `do_csp/probe_opened.py` (nội dung linh kiện thật sự hiện).
- `cd frontend && npm ci && npm run build` (từ lockfile) [Chạy].
- `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_static_ui.py tests/test_api_chat.py -q` ⇒ 12 passed + 1 error (test cần khoá — đã biết);
  test đó chạy riêng với `--env-file /home/minhhieu/hue_rag/.env` ⇒ 1 passed (chỉ `/health`, không gọi model). Thêm: dời `dist/` tạm ⇒ 2 test báo đúng lệnh cần chạy, `import api.app` in cảnh báo.
- Server thật: `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8812` (worktree, symlink `data/` +
  `knowledge-base-hue/`); `/health` 5 / 5 ready; `/` 200 + CSP; `/static/index.html` 200 + cùng CSP. Đã tắt (TaskStop).
- Playwright (chromium headless, `uv run`), câu **tự viết** (không Golden / câu kín; lưu ở `b121/cau_tu_viet.json`):
  `b121/ui_real.py` (server thật, không chặn mạng) · `b121/ui_replay.py` [Tự dựng] · `b121/ui_layout.py` (390 / 1280 px) · `b121/parser_check.mjs` (Node, logic thuần trên `src/stream.js`) · `b121/probe_style_origin.py`.
  `ui_real.py` + `ui_replay.py` chạy **lần 2 trên bản build cuối** (sau sửa bố cục điện thoại / xoá ô hỏi sau khi gửi); số dưới là lần 2. Sửa cuối (bề rộng nút chỉ từ 640 px) chỉ đổi lớp CSS ⇒ chạy lại `ui_layout.py`.

## 4. Kết quả quan sát

### 4.1 Dò CSP shadcn / Radix (tiêu chí ghi trước ở B116: mỗi linh kiện 0 vi phạm + 0 request ra ngoài) [Chạy]
| Linh kiện | Vi phạm CSP | Request ra ngoài | Kết luận |
|---|---:|---:|---|
| mốc: React + Tailwind | 0 | 0 | đạt |
| Collapsible | 0 | 0 | đạt |
| Tooltip | 0 | 0 | đạt |
| Popover | 0 | 0 | đạt |
| Dialog | 1 (`style-src-elem`) | 0 | **không đạt** — khoá cuộn chèn `<style>` |
| ScrollArea | 1 (`style-src-elem`) | 0 | **không đạt** — chèn `<style>` lúc hiện |

Lượt đầu để 5 linh kiện chung một trang ⇒ mọi trang đều 1 vi phạm (do ScrollArea) ⇒ tách mỗi linh kiện một trang mới ra bảng trên. Bốn linh kiện "đạt" đều được kiểm là nội dung hiện thật sau thao tác.
**Quyết định (A đồng ý):** trang chỉ cần nút, ô hỏi, danh sách, phần gập ⇒ dùng thẻ HTML gốc + Tailwind, **0 gói Radix / shadcn** (ít gói hơn danh sách duyệt).

### 4.2 Server thật (`ui_real.json`) [Chạy]
| Ca | Quan sát |
|---|---|
| Câu trong kho (loại một dữ kiện) | chữ hiện qua **17 lần vẽ** trước `sources`; trước `sources`: 3 số nguồn, **0 link**; sau: 3 link, 3 nguồn ở khung bên; khi chờ ô hỏi khoá + nút "Đang trả lời…"; bấm số ⇒ đúng nguồn nhận focus + nền `accent-soft`; "Xem đoạn trích" mở được; 0 vi phạm CSP (cả sau các lần bấm), 0 request ra ngoài |
| Câu ngoài kho | câu từ chối chuẩn, không hộp lỗi, khung nguồn "Kho chưa có nguồn cho câu này.", 0 link |
| Lỗi thật (câu > 500 ký tự) | server trả 422 trước luồng ⇒ hộp lỗi "Yêu cầu không hợp lệ." + "Thử lại", 0 chữ / nguồn; bấm "Thử lại" ⇒ đúng **1** yêu cầu nữa (tổng 2) |
| Rời trang khi chữ đã hiện | log server: `outcome: client_disconnected` (yêu cầu 17 qua đường thật) |
| Điện thoại 390 px / laptop 1280 px | không cuộn ngang; 0 vi phạm CSP; ô hỏi ở cuối khung (ảnh `06_dien_thoai.png`, `01_chua_hoi.png`) |

Log (`b121/log/new_log2.txt`): 3 dòng `chat_metrics` mới = 3 câu tới model (câu > 500 ký tự bị kiểm đầu vào chặn, không có dòng — như route cũ); `delta_matches_final` true ở 2 câu xong;
grep câu hỏi trong log = **0**. Ảnh: `b121/anh/01`–`06`.

### 4.3 Logic phía trình duyệt [Tự dựng] (`ui_replay.json`) và logic thuần
- **Yêu cầu 18:** chữ có `[1]`, `[Nguồn 2]`, `[ nguồn 3 ][1]` ⇒ 4 link `1, 2, 3, 1`; `[2]` trong `code` giữ nguyên. Không có `sources` ⇒ 2 số mờ, 0 link (yêu cầu 9). Mảnh `seq` trùng bị bỏ (`A`,`A`,`B` ⇒ "AB").
- **Yêu cầu 13 / 16:** 25 ca dò của C107 (`probe_v2.py`, dùng lại đúng khối CASES) + 1 ca bất biến ⇒ 0 request ra ngoài, 0 thẻ / thuộc tính tải tài nguyên còn lại, 0 script chạy; Markdown thường giữ (đậm, 2 mục danh sách, bảng, link ngoài).
  **1 báo cáo CSP** ở ca chữ có thẻ `<style>`: probe tách bước cho thấy nó sinh khi DOMPurify phân tích bằng `DOMParser` (0 ở bước `<template>` của mình) — CSP chặn ngay lúc phân tích, thẻ không còn trên trang. Bản cũ cũng đúng 1 ở cùng bộ ca (`probe_v2_716ba4d.json`). Luồng thường: 0.
- **Yêu cầu 10 / 11:** luồng không `done`, cắt giữa sự kiện, `sources` rồi đứt ⇒ xoá hết + "Kết nối bị gián đoạn. Vui lòng thử lại." + "Thử lại"; `error` sau chữ ⇒ xoá hết + lời của server.
- **Yêu cầu 7** (Node, `parser_check.mjs` trên `src/stream.js`): 268 / 268 vị trí cắt chuỗi, từng ký tự một, **283 / 283** vị trí cắt giữa byte UTF-8 (bản cũ C107 thử mỗi 7 byte), `data:` nhiều dòng ⇒ đúng.

### 4.4 Khớp 19 yêu cầu
| # | Yêu cầu | Chỗ | Kiểm |
|---|---|---|---|
| 1 | POST thân `{query}`; `!ok` ⇒ JSON `error.message` | `stream.js` | [Chạy] câu > 500 ký tự |
| 2 | `text/event-stream` (header do server) | server | [Chạy] luồng đọc được |
| 3 | `status` chỉ hiện chữ trạng thái | `App.jsx` `STATUS_TEXT` | [Chạy] ảnh 02 |
| 4 | chỉ nối `seq` mới | `App.jsx` | [Tự dựng] |
| 5 | `sources` sau kiểm; từ chối = `sources` rỗng | `App.jsx`, `SourcePanel` | [Chạy] |
| 6 | `error` / `done` cuối | `stream.js` | [Chạy] + [Tự dựng] |
| 7 | parser chịu cắt / nhiều sự kiện / UTF-8 | `stream.js` | logic thuần 268 + 283 ca |
| 8 | vẽ lại cả buffer theo khung hình, luôn qua lọc | `App.jsx` rAF + `renderAnswerHtml` | [Chạy] 17 lần vẽ |
| 9 | link chỉ bật sau `sources` | `markdown.js` `citedIds` | [Chạy] 0 link trước |
| 10 | `error` ⇒ xoá hết + "Thử lại" gửi lại đúng câu | `App.jsx` | [Chạy] + [Tự dựng] |
| 11 | không `done` ⇒ như lỗi | `stream.js` | [Tự dựng] |
| 12 | khoá ô hỏi khi chờ, không nút Dừng | `App.jsx` | [Chạy] |
| 13 | lọc theo danh sách cho phép 25 / 4 | `markdown.js` | [Tự dựng] 26 ca + test |
| 14 | CSP mọi trang HTML, không nội dòng / `eval` | `app.py` (giữ), bản build | [Chạy] + test |
| 15 | không CDN | font / thư viện trong bản build | [Chạy] 0 request ra ngoài + test |
| 16 | link ngoài chỉ mở khi bấm | lọc HTML | [Tự dựng] |
| 17 | huỷ `fetch` khi rời trang | `AbortController` + `pagehide` | [Chạy] `client_disconnected` |
| 18 | link cả `[n]` lẫn `[Nguồn n]` | `markdown.js` | [Tự dựng] (model ít viết `[Nguồn n]` — không tạo được theo ý trên đường thật) |
| 19 | nhãn "Trợ lý AI … có thể sai" | dưới ô hỏi | [Chạy] ảnh |

Tiền: lượt 1 ≈ 0,00047 + lượt 2 ≈ 0,00047 USD (tính từ token trong `chat_metrics`, giá đủ) + 2 câu rời trang (không có số token — cận trên ~0,0003 mỗi câu) ⇒ **< 0,002 USD** / trần 0,02.

## 5. Lỗi và giới hạn
- **Phase 9 cần hộp thoại / vùng cuộn ⇒ tự viết** bằng React + Tailwind; Radix Dialog và ScrollArea vi phạm CSP (4.1).
- Chạy API giờ cần bước `npm ci && npm run build` (Node). Không có chế độ dev (`vite dev`) — cố ý: CSP chỉ áp khi FastAPI phục vụ. `session_prompt/chạy_môi_trường.md` (governance — A sửa) chưa có lệnh build.
- Câu > 500 ký tự: lời báo của server là "Yêu cầu không hợp lệ." (như bản cũ) — chưa có đếm ký tự / lời rõ hơn ở giao diện; để Phase 9 nếu cần.
- Link ngoài trong câu trả lời mở ở cùng tab (như bản cũ; `target` không có trong danh sách thuộc tính cho phép).
- Câu đầu tiên sau khởi động server chậm hơn (lượt 1: chữ đầu 5,1 s ↔ lượt 2: 2,8 s cùng câu) — chỉ quan sát hai lần, không đo latency trong việc này.
- `[Tự dựng]` không phải bằng chứng server; các ca đó chỉ kiểm cách giao diện xử lý chữ / luồng cho trước.

## 6. Bàn giao cho người kiểm
- Đọc trước: mục "Căn cứ để review"; rồi `frontend/src/markdown.js` (an toàn), `stream.js`, `App.jsx`.
- Chạy lại: `cd frontend && npm ci && npm run build`; pytest như mục 3; server cổng trống + `b121/ui_real.py <base> <thư mục ảnh> b121/cau_tu_viet.json` (~0,0005 USD) và `b121/ui_replay.py <base> data/streaming_s1_2026-11-01/s3_review_c107` (0 USD);
  dò Radix: `do_csp/` (`npm ci && npm run build` trong bản sao ở `/tmp`, rồi `serve_dist.py <dist> <cổng>` + `probe_radix.py`).
- Không có lệch phạm vi ngoài "0 gói Radix" (A đồng ý). Guide Phase 6 do việc giao ghi rõ. 5 chỗ báo cáo + merge: A.

**Giải thích ngắn:** trang hỏi đáp được viết lại bằng React để Phase 9 thêm màn hình / nhiều lượt dễ hơn. Người dùng thấy chữ hiện dần như cũ, số nguồn gọn hơn (số nhỏ tím, bấm vào thì nguồn bên cạnh sáng lên), có nhãn "Trợ lý AI … có thể sai". Rời trang thì server dừng model ngay. Rào an toàn (lọc HTML + CSP) giữ nguyên; thư viện linh kiện Radix bị bỏ vì hai linh kiện của nó phạm CSP.

## 7. Sửa sau review C119 (B, 10:32 02/11/2026)
**m-1** (lỗi không do server viết hiện chữ kỹ thuật tiếng Anh của trình duyệt): `frontend/src/stream.js` — mọi lỗi ném ra (trừ `AbortError`) là `StreamError` mang lời tiếng Việt.
Lời của server giữ nguyên (JSON lỗi trước luồng, sự kiện `error`). Còn lại thay bằng câu cố định:
- `fetch` hỏng ⇒ "Không kết nối được máy chủ. Vui lòng thử lại."
- thân lỗi không phải JSON ⇒ "Đã xảy ra lỗi trong hệ thống. Vui lòng thử lại sau." (cùng lời `internal_error` của server)
- đọc luồng hỏng / `data:` không phải JSON ⇒ `INTERRUPTED_MESSAGE`

`App.jsx` không đổi.

Kiểm (0 USD — server API chạy **không nạp `.env`**, không thể gọi model; `data/giao_dien_moi_2026-11-01/b121/m1/`):
- [Chạy] câu > 500 ký tự ⇒ "Yêu cầu không hợp lệ." (lời server giữ).
- [Chạy] trang đã nạp, rồi **tắt server thật** ⇒ "Không kết nối được máy chủ…" + "Thử lại"; bấm "Thử lại" ⇒ cùng lời.
- [Tự dựng] 3 ca của C119: mạng hỏng ⇒ "Không kết nối được máy chủ…"; 502 thân HTML ⇒ "Đã xảy ra lỗi trong hệ thống…"; `data:` hỏng ⇒ "Kết nối bị gián đoạn…". Sự kiện `error` sau chữ ⇒ lời server. Mọi ca: xoá hết chữ, có "Thử lại".
- Không hồi quy: `ui_replay.py` chạy lại (trích dẫn, 26 ca lọc HTML, 4 ca luồng đứt) — như mục 4.3; parser 268 / 268 + 283 / 283; `test_static_ui.py` 3 passed.
