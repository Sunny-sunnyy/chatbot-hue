# Review: B121 — giao diện mới (React + Vite + Tailwind), cả nhánh `giao-dien-moi`

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 2 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-29`)
Date: 10:25 02/11/2026 (`date`)
Canonical guide: `report_agent/2026-10-31_streaming_spec/yeu_cau_cho_giao_dien_moi.md` (17 yêu cầu) + yêu cầu 18 (`report_agent/2026-11-01_giao_dien_moi/b116_so_sanh_giao_dien.md`) + mục B121 trong `session_prompt/CURRENT_HANDOFF.md` (yêu cầu 19, gói duyệt, `.npmrc`)
Implementation report: `report_agent/2026-11-02_giao_dien_moi_code/b121_giao_dien_implementation.md` (trên nhánh) — đọc như chỉ mục bằng chứng, không tự chứng minh PASS. Không đọc `STATUS_B.md`.

## 1. Phạm vi đã review

- **Nhánh:** `origin/giao-dien-moi` = `11a0f3a`, một commit trên `main` `411bbc5`. 19 file, +2.236 / −523, khớp report. `git diff --check main...origin/giao-dien-moi` sạch.
- **Đọc hết exact diff:**
  - `frontend/src/{App.jsx, markdown.js, stream.js, main.jsx, index.css}`;
  - `frontend/{index.html, package.json, .npmrc, vite.config.js}`; `package-lock.json` đọc bằng script;
  - `backend/api/app.py`, `backend/tests/test_static_ui.py`, `.gitignore`, guide Phase 6 "Hiện hành";
  - 5 file xoá (`frontend/app.js`, `styles.css`, `index.html` cũ, `vendor/*`).
- **Ngoài phạm vi / sai lệch chưa khai:** không thấy.
  - CSP `FRONTEND_CSP` không đổi một chữ; `FrontendStaticFiles` + route `/` giữ; API / thân SSE không đổi.
  - 0 gói Radix / shadcn đã khai, A đồng ý.
  - `node_modules/`, `dist/` nằm trong `.gitignore`, không có trong commit.
- **Độ đơn giản:** 426 dòng nguồn cho một trang hỏi đáp; một component trang + một khung nguồn; không thư viện trạng thái / router; parser SSE chuyển nguyên logic cũ. Tương xứng.

## 2. Findings

Không có blocker. Không có major.

### m-1 (minor) — lỗi không do server viết hiện ra người dùng nguyên chữ kỹ thuật tiếng Anh

- **Vị trí:** `frontend/src/stream.js:35-38`, `:42-46`, `:53-56`; `App.jsx:83-88` (`setError(failure.message)`).
- **Yêu cầu:** yêu cầu 10 / 11 — lỗi ⇒ xoá hết + lời báo + "Thử lại". Văn phong giao diện là tiếng Việt.
- **Bằng chứng** — [Tự dựng], ca dò của C qua `page.route`, `probe.json`. Đều đã xoá chữ + nguồn và có "Thử lại", nhưng lời báo là chữ kỹ thuật:

  | Ca | Lời báo hiện ra |
  |---|---|
  | `fetch` thất bại (mạng / server tắt) | `Failed to fetch` |
  | 502 thân HTML (kiểu proxy khi deploy) | `Unexpected token '<', "<html>Bad "... is not valid JSON` |
  | `data:` hỏng JSON | `Expected property name or '}' in JSON at position 1 …` |

- **Không phải hồi quy:** bản cũ cũng in `error.message` (`frontend/app.js:180-186` trên `main`).
- **Tác động:** người dùng thấy chữ máy; không lộ dữ liệu, không đổi hành vi an toàn.
- **Tiêu chí đóng:** lỗi **không** mang lời của server hiện một câu tiếng Việt cố định — vd `INTERRUPTED_MESSAGE`, hoặc "Không kết nối được máy chủ…" cho lỗi `fetch`. Lời của server vẫn giữ: `error.message` của JSON trước luồng và của sự kiện `error`. Chạy lại 3 ca trên.

### m-2 (minor) — chỗ đọc ngoài nhánh còn tả giao diện cũ (việc của A khi merge)

- `bao_cao_he_thong/BAO_CAO_SINH_CAU_TRA_LOI_API.md:46, :58` trỏ `api/app.py:141–146`. Nay đoạn phục vụ trang là `app.py:159-166`.
- `session_prompt/chạy_môi_trường.md` chưa có `cd frontend && npm ci && npm run build`. B đã ghi "A cần".
- `pytest tests/test_static_ui.py` nay cần bản build: chưa build thì 2 test báo lệnh cần chạy. Đây là thiết kế; nên nhắc trong bẫy `Project_Status.md` §8.
- **Tiêu chí đóng:** A sửa trong 5 chỗ báo cáo lúc merge. Không phải việc của B.

**Quan sát, không phải finding:** payload lạ của C sinh **7 báo cáo CSP** lúc DOMPurify phân tích bằng `DOMParser`, gồm `style-src-elem`, `style-src-attr`, `base-uri` ×4. Report B ghi 1 báo cáo cho bộ C107.
DOM cuối không còn thẻ / thuộc tính nào ngoài danh sách cho phép, 0 request ra ngoài, 0 script chạy. Tức là CSP chặn ngay ở lớp phân tích: rào hai lớp đang làm việc. Khi deploy có `report-uri` thì các báo cáo này là tiếng ồn đã biết.

## 3. Cách người kiểm chạy lại thật

Môi trường riêng của C: worktree `/tmp/c119` (detached `11a0f3a`; symlink `data/`, `knowledge-base-hue/`), **không** dùng `/tmp/b_giao_dien`. Đã gỡ worktree + symlink + `/tmp/c119_probe` sau khi xong.

1. `cd frontend && npm ci && npm run build` — từ lockfile sạch, Node v24.19.0 / npm 11.17.0.
2. Script Node đọc `package-lock.json`: số gói, `integrity`, `resolved`, `hasInstallScript`, gói gốc. Grep bản build: `eval(` / `new Function`, URL `http(s)://`.
3. `git grep` trên nhánh tìm chỗ còn trỏ file đã xoá (`app.js`, `vendor/marked|purify`, `styles.css`) và `frontend/` trong `backend/ scripts/ guides/ bao_cao_he_thong/`.
4. `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_static_ui.py tests/test_api_chat.py -q`.
5. Server thật: `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8823`. Kiểm `/health`, `/`. Đã tắt (TaskStop).
6. Playwright (chromium headless, `uv run`) — script **của C** (`data/giao_dien_moi_2026-11-01/c119_review/probe.py` `82cadfd874c4`), cách dò khác B:
   - **A1 — câu trong kho tự viết, loại nghệ thuật biểu diễn:**
     - **cách khác B:** thăm DOM mỗi 50 ms trong lúc chữ chạy, đếm link `[data-cite]` ở mọi lần thăm trước khi khung nguồn hiện;
     - so mã nguồn của link ⊆ danh sách khung bên; bấm số ⇒ phần tử focus.
   - **A2 — câu ngoài kho tự viết, loại giá dịch vụ ngoài Huế.**
   - **B1 [Tự dựng] — payload lạ, khác bộ 25 ca C107:**
     - URI `javascript:` (Markdown, thẻ, mã hoá `&#106;`), `data:`, `vbscript:`;
     - mXSS `<svg><style>`, `<math><mglyph><style>`;
     - `<details ontoggle>`, `style=url()`, ảnh Markdown, `iframe` / `object` / `link` / `video poster` / `table background` / `form` / `base`;
     - trích dẫn `[Nguồn 1]`, `[ nguồn  2 ]`, `[3]`, `` `[2]` `` trong code, `[1]` trong link ngoài;
     - Markdown thường (đậm, danh sách, bảng).
     Kiểm: tập thẻ / thuộc tính trong DOM, `href` còn lại, `window.__x` (dấu script chạy), request tới `evil.test`.
   - **B2–B5 [Tự dựng] — đường lỗi:**
     - B2: sự kiện `error` **sau** `sources` (rút lại), rồi "Thử lại";
     - B3: `fetch` bị huỷ ở tầng mạng;
     - B4: 502 thân HTML;
     - B5: `data:` không phải JSON.
7. Log server: đếm `chat_metrics` trước / sau; grep chữ hai câu hỏi trong log.

## 4. Kết quả quan sát

- **Lockfile + bản build** [Chạy]:
  - 86 gói, 86 / 86 có `integrity`, 0 `resolved` ngoài `registry.npmjs.org`;
  - gói gốc đúng danh sách duyệt: 5 chạy + 4 build;
  - `hasInstallScript` chỉ ở `fsevents` (gói tuỳ chọn của macOS, không cài trên Linux; `.npmrc` `ignore-scripts` cũng chặn);
  - `npm ci` báo 0 lỗ hổng; build 214 ms, JS 303 kB (khớp report);
  - bản build: 0 `eval(` / `new Function`. URL trong bundle chỉ là chuỗi namespace `w3.org`, link tài liệu React / GitHub trong thông báo lỗi — không phải tải;
  - `dist/index.html`: 1 `script type=module src=/static/assets/…`, 1 `link stylesheet` cùng gốc, 0 script nội dòng, 0 `<style>`.
- **Test** [Chạy]: **12 passed, 1 error**. Error là `test_health_is_cached_and_ready_after_real_lifespan`, test cần khoá, đã biết (`Project_Status.md` §8). Khớp report B.
- **Chỗ còn trỏ file đã xoá:** 0 trong code / script / guide. Còn trong báo cáo User → m-2. Một dòng lịch sử trong `CURRENT_HANDOFF.md` mục B116 trỏ `app.js:44` — lịch sử, không sửa.
- **Cổng ổn định** [Chạy]:
  - `/health` 5 / 5 ready; `/` 200;
  - CSP của `/` **giống từng chữ** hằng `FRONTEND_CSP` trên `main`;
  - `chat_metrics` 5 ⇒ 7 = **2 dòng mới cho 2 câu**, cả hai `success`, `delta_matches_final: true`;
  - grep chữ hai câu hỏi trong log = **0**.
- **A1 câu trong kho** [Chạy]:
  - 18 lần thăm có chữ trước khi khung nguồn hiện, **0 link** ở mọi lần (yêu cầu 8 + 9 theo cách đo khác B);
  - sau `sources`: 3 link, 3 nguồn ở khung bên, mã link ⊆ khung bên;
  - bấm số đầu ⇒ đúng `#source-n` nhận focus;
  - 0 vi phạm CSP, 0 request ra ngoài; chữ đầu ở server 2,27 s (một lần, không phải phép đo tốc độ).
- **A2 câu ngoài kho** [Chạy]: chữ đúng câu từ chối chuẩn, 0 link, khung nguồn "Kho chưa có nguồn…", không hộp lỗi, 0 vi phạm CSP, 0 request ra ngoài.
- **B1 payload lạ** [Tự dựng]:
  - thẻ còn lại ⊆ danh sách cho phép + `sup` (p, strong, ul, li, table…, a, code); thuộc tính chỉ `class`, `href`, `data-cite`, `aria-label`;
  - `href` còn lại: `#source-1..3` + đúng link ngoài `http` hợp lệ. **0** `javascript:` / `data:` / `vbscript:`;
  - `window.__x` = null (0 script chạy); **0 request tới `evil.test`**;
  - trích dẫn 1, 2, 3 thành link (cả `[Nguồn n]`, `[ nguồn  2 ]` — yêu cầu 18); `[2]` trong code giữ nguyên; `[1]` trong link ngoài không đổi;
  - bảng + danh sách giữ (câu bất biến: Markdown thường hiện như cũ).
- **B2 lỗi sau `sources`** [Tự dựng]: chữ = 0, link = 0, khung nguồn ẩn, hộp lỗi hiện; "Thử lại" gửi **đúng 1** yêu cầu, cùng thân câu hỏi (yêu cầu 10).
- **B3–B5** [Tự dựng]: đều xoá hết + hộp lỗi + "Thử lại", nhưng lời báo là chữ kỹ thuật → m-1.
- **Tiền:** 2 câu thật, token từ `chat_metrics`: vào 1.606 + 2.820 (ghi đệm 1.603 + 2.817), ra 108 + 31. Theo giá đủ ≈ **0,0006 USD** / trần 0,01.
- **Bằng chứng (private):** `data/giao_dien_moi_2026-11-01/c119_review/` — `probe.py` `82cadfd874c4`, `probe.json` `eda535df6f9f`, `chat_metrics_2.txt` `a1cf7fcdb7f1` (2 dòng số đo, không chữ).

**Câu bất biến đã kiểm:** CSP và hợp đồng API / SSE không đổi; câu đủ ý vẫn hiện Markdown thường; trích dẫn chỉ thành link sau `sources`. Cả ba đúng.

## 5. Giới hạn hoặc phần chưa chạy

- **Dùng lại bằng chứng B, không chạy lại** (đầu vào không đổi giữa lần B chạy cuối và `11a0f3a`; report ghi chạy trên bản build cuối):
  - rời trang ⇒ `client_disconnected`;
  - bố cục 390 / 1280 px;
  - parser 268 + 283 vị trí cắt;
  - dò Radix.
  Theo `risk-gated-agent-review`, không lặp mọi lệnh của người làm. Ca huỷ `fetch` khi rời trang C **không** tự chạy lại.
- B1–B5 là [Tự dựng] — kiểm cách trang xử lý luồng cho trước, không phải bằng chứng server.
- Không kiểm trên Firefox / Safari; không kiểm trình đọc màn hình.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.**
- **Đạt:**
  - 19 yêu cầu: phần rủi ro (9, 13–16, 18) kiểm lại bằng cách khác B; 8, 10 trên đường thật / tự dựng;
  - CSP không nới; 0 CDN; lockfile sạch, đúng gói duyệt; bản build không lọt commit;
  - cổng ổn định đạt.
- **m-1:** B sửa được trong một lượt nhỏ trước merge, hoặc A ghi giới hạn — không chặn.
- **m-2:** A làm lúc merge (5 chỗ báo cáo + `chạy_môi_trường.md` + bẫy §8).
- **Việc trung bình** (Phase 8 đã chốt hướng) ⇒ A đóng, báo User.
