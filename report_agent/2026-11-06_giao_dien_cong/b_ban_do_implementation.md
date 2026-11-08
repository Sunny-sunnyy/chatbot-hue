# Implementation Report: bản đồ lịch trình (P1 đợt 2 cổng)

Người làm: B (Claude Code, terminal `hue-rag-a1`)
Date: 08/11/2026 (bắt đầu ~09:40, report 09:59 — `date`)
Plan: `docs/superpowers/plans/2026-11-08-ban-do-lich-trinh-plan.md` bản 1 `e738f6f9f3ae` (A duyệt; §10: (a) Leaflet + tile OSM · chỉ dưới câu trả lời có lịch ·
toạ độ 11 điểm thiếu là việc riêng).
Nhánh: `p11-ban-do` = `d0adf31` (code `f2d8523` từ `main` `2a2a40e`, **rebase lên `main` `1611d34`** sau khi ảnh cổng vào `main`; đã push). Tiền: **0,00306 USD** (9 lượt thật) / trần 0,005.

## 1. Phạm vi

Làm đúng plan §2–§7: ghim có số theo thứ tự trong ngày dưới câu trả lời có lịch, toạ độ do code gắn, cờ `ban_do_lich` (tắt mặc định), CSP theo cờ, ghi
đường ra mới trên Giới thiệu. **Lệch plan (A duyệt giữa chừng):** CSP khi cờ bật thêm cả `data:` (xem §2). Thêm ngoài plan (A giao): sửa một test
B6 hỏng sẵn trên `main`.

## 2. Thay đổi chính

| File | Thay đổi |
|---|---|
| `backend/llm/lich_trinh.py` | `nap_toa_do` (đọc `diem_toa_do_v5.json`, chỉ điểm có trong bảng lịch, toạ độ phải là số trong khung Huế 16,0–16,8 / 107,0–108,0 — sai ⇒ `ValueError`); `ban_do(bang, khung, toa_do)` thêm `ngay`, `buoi`, `thu_tu` (từ 1 mỗi ngày, sáng → chiều → tối), `toa_do` (`None` khi thiếu); không truyền `toa_do` ⇒ khuôn cũ `{ten, map_url}` |
| `backend/llm/assistant.py` | cờ `ban_do_lich` + `toa_do_lich` (nạp ở rìa khi cờ bật); cờ bật mà thiếu bảng ⇒ `ValueError`; `lich_cho_giao_dien` truyền toạ độ chỉ khi cờ bật |
| `backend/config/settings.yaml` | `ban_do_lich: false`, `lich_trinh_toa_do: ../data/phase_9/lich_trinh/diem_toa_do_v5.json` |
| `backend/api/app.py` | `frontend_csp(state)`: cờ bật ⇒ `img-src 'self' blob: data: https://tile.openstreetmap.org`; cờ tắt / trước lifespan ⇒ chuỗi cũ |
| `backend/api/routes/cong.py` | `/api/tinh_nang` thêm `ban_do_lich` |
| `frontend/src/BanDoLich.jsx` (mới) | Leaflet: chọn ngày, ghim `divIcon` có số, ô ghim dựng bằng DOM + `textContent` (tên không qua HTML), khung tự vừa ghim (zoom ≤ 15), không đường nối, không cuộn chuột zoom; danh sách có số + "chưa có trên bản đồ"; ngày 0 toạ độ ⇒ dòng báo, không vẽ bản đồ; trình duyệt kiểm lại khung Huế |
| `frontend/src/chat.jsx` | `LichExtras`: lịch có ≥ 1 toạ độ ⇒ `lazy(BanDoLich)` (chunk riêng; lúc tải hiện danh sách cũ); không ⇒ danh sách link như trước (`MapLinks`) |
| `frontend/src/pages.jsx`, `App.jsx` | Giới thiệu theo cờ: bỏ "chưa có bản đồ", thêm câu "trình duyệt tải ảnh bản đồ từ OpenStreetMap — nhận IP + vùng đang xem (không nhận câu hỏi)" |
| `frontend/vite.config.js` | `build.assetsInlineLimit: 0` — CSS Leaflet có 3 ảnh PNG không dùng; Vite nhúng chúng thành `data:` làm CSS chunk 6,4 KB gzip (> sàn 5 KB); giờ là file riêng, chỉ tải khi dùng (A đồng ý) |
| `frontend/package.json` + lock | `leaflet` 1.9.4 (BSD-2, 0 phụ thuộc; lockfile chỉ thêm 1 gói; `.npmrc` giữ nguyên) |
| `backend/tests/test_ban_do_lich.py` (mới) | T1–T3 (§4) |
| `backend/tests/test_cong_dot_1.py` | tập khoá `/api/tinh_nang` có `ban_do_lich` |
| `backend/tests/test_b6_tra_web.py` | `test_web_section_renderer_uses_filter_without_links` **hỏng sẵn trên `main`** (đọc đúng dòng thứ 4 của `renderWebHtml`; hàm ngắn lại từ S2 `f20fd28`) ⇒ đọc theo thân hàm (tới dấu đóng hàm), vẫn kiểm `DOMPurify.sanitize(…, WEB_SANITIZE_OPTIONS)` và không dùng bộ lọc câu trả lời (A giao) |

**Vì sao `data:` trong `img-src` (A chọn (a) 08/11):** Leaflet 1.9.4 huỷ tile đang tải dở (kéo / zoom / đổi ngày / gỡ bản đồ) bằng cách gán GIF rỗng
`data:image/gif;base64,…` (`leaflet-src.esm.js` `_removeTile`, `_abortLoading`). Lượt đo đầu (CSP chưa có `data:`): **28 lỗi CSP** console, bản đồ vẫn chạy.
`data:` không mở mạng ra ngoài; chữ model không chèn được ảnh vì DOMPurify không cho thẻ `img` / thuộc tính `src`
(`backend/tests/test_static_ui.py::test_answer_sanitizer_is_an_allowlist_without_fetching_tags`). Hai cách bỏ: giữ lỗi console (trượt tiêu chí, che lỗi thật);
vá hàm nội bộ Leaflet (dễ vỡ khi nâng gói).

## 3. Cách đã chạy thật

- Build: `cd frontend && npm ci && npm install leaflet@1.9.4 && npm run build` (worktree `/tmp/b_bando`). Mốc bundle: worktree tạm `main` `2a2a40e`, build cùng cách.
- Test rộng (không khoá): mọi `tests/test_*.py` trừ `test_phase6_live_smoke`, `test_openai_full_corpus_generator`, `test_startup_model_missing`.
- Q1: `capture_all.py` trên `main` `2a2a40e` (mốc) và nhánh với cờ tắt / bật (sửa tạm `settings.yaml` rồi trả lại — `git diff` xác nhận).
- Server thử cờ bật: `uvicorn --factory --app-dir data/phase_11/ban_do/tools app_ban_do:make_app --port 8873` (bản sao settings trong RAM, `PYTHONPATH` = `backend/`
  của worktree, `--env-file` tuyệt đối); tắt bằng TaskStop.
- Trình duyệt: `uv run python data/phase_11/ban_do/tools/kiem_ban_do.py http://127.0.0.1:8873/ <thư mục>` — 1 câu thường tự viết (Q-M4, cũng là câu trong kho của
  cổng ổn định) + 3 lượt biểu mẫu (1 ngày · Di tích / 2 ngày · Ẩm thực / 3 ngày · Thiên nhiên); đọc sự kiện SSE `lich_trinh` làm đáp án, đếm `.ghim` từng ngày,
  ghi mọi request (host, mã, header gửi máy chủ tile), lỗi console / pageerror; chụp từng ngày ở 1440 + 390.
- Câu ngoài kho: `curl POST /api/chat` (câu tự viết về giá cổ phiếu).

## 4. Kết quả quan sát

| Tiêu chí (plan §7) | Kết quả |
|---|---|
| T1 dữ liệu giao diện (bảng thật, lịch 3 ngày từ `xep` thật) | đạt — thứ tự = khung, `thu_tu` 1..k mỗi ngày, toạ độ = bảng, thiếu ⇒ `None`; cờ tắt ⇒ khuôn cũ (khoá tập trường) |
| T2 toạ độ sai ⇒ không khởi động | đạt — 5 ca (ngoài khung Huế, 0, chuỗi, `True`, `None`) |
| T3 CSP | đạt — cờ tắt / trước lifespan = chuỗi cũ; cờ bật chỉ khác ở `img-src` (+ `data:` + đúng 1 host `https://`), cả `/` và `/static/index.html` |
| T4 Q1 chuỗi gửi model | **228 / 228 giống byte** — mốc `main` = nhánh cờ tắt = nhánh cờ bật (sha256 file `d9bdb467a501` cả ba) |
| Test rộng | **731 đạt**; 2 hỏng + 1 lỗi = đúng test cần khoá (như sổ tay) + test B6 hỏng sẵn (đã sửa, đạt); sau sửa: 4 file chạm 109 đạt |
| Q-M1 ghim | lượt 2 (sau sửa CSP): 6 / 6 ngày đúng — số ghim = số điểm có toạ độ, số trên ghim = `thu_tu`; danh sách đủ điểm; nhãn thiếu đúng. Số điểm có toạ độ: 1 ngày 2 / 2 · 2 ngày 2 / 5 · 3 ngày 1 / 6 (2 ngày của lịch 3 ngày không có ghim ⇒ chỉ danh sách + dòng báo) |
| Q-M2 lỗi / request | lượt 2: **0 lỗi** console / CSP / pageerror / request hỏng; tile 66 / 66 trả 200 từ `tile.openstreetmap.org`; 0 request tới host khác |
| Q-M3 ghi công | hiện trong khung bản đồ ở 1440 và 390 (mọi ngày có bản đồ) |
| Q-M4 câu thường | 0 request chunk `BanDoLich`, 0 tile |
| Q-M5 cỡ | bundle chính 107,27 KB gzip (mốc `main` 105,99 ⇒ **+1,28** / sàn ≤ 3); chunk bản đồ **44,54 KB** JS (≤ 60) + **2,63 KB** CSS (≤ 5) |
| Q-M6 lộ chữ | 0 chữ câu hỏi trong URL / header gửi máy chủ tile; Referer = gốc trang (`http://127.0.0.1:8873/`) |
| Cổng ổn định | `/health` 5 / 5; `/` 200 + CSP mới; câu trong kho trả lời, câu ngoài kho ⇒ `ngoai_pham_vi` (câu chuẩn, 0 nguồn); `chat_metrics` mới = 5 = số câu lượt 2; grep 2 câu hỏi trong log = 0; Giới thiệu khi cờ bật có câu OSM, 0 lỗi |
| Q-M7 ảnh cho User | `data/phase_11/ban_do/anh_v2/` (12 ảnh: 6 ngày × 1440 / 390) — chưa có nhận xét User |

Tiền (từ `chat_metrics`, `data/phase_11/ban_do/chat_metrics.log` — file có cả dòng pytest không tốn tiền): lượt 1 (CSP cũ) 4 lượt 0,00153 USD; lượt 2 5 lượt
0,001529 USD ⇒ **0,00306 USD**.

Dữ liệu: `data/phase_11/ban_do/` (`kiem_ban_do.json` lượt 1 + `kiem_ban_do_v2.json` lượt 2, `q1/`, `anh/` lượt 1, `anh_v2/`, `tools/`).

## 5. Lỗi và giới hạn

- **Toạ độ có thể lệch** (dữ liệu mở; C197: 3 điểm lệch 0,3–1,3 km giữa các file): ảnh lịch 1 ngày, ghim "Kinh thành Huế (Ngọ Môn – Kỳ Đài)" nằm phía đông
  khu Đại Nội — cần User nhìn (Q-M7). Không sửa toạ độ ở bậc này.
- 11 / 28 điểm chưa có toạ độ (phần lớn cảnh / phố) ⇒ lịch thiên nhiên nhiều ngày gần như không có ghim (3 ngày: 1 / 6). Bổ sung = việc dữ liệu riêng (A §10 (3)).
- Phụ thuộc OSMF best-effort: bị chặn ⇒ mất ảnh nền, danh sách + link Google Maps vẫn dùng được (không thử bằng cách chặn thật).
- Leaflet thêm tiền tố "Leaflet" (có cờ Ukraina dạng SVG nội dòng) vào dòng ghi công — mặc định của gói, giữ.
- **Deploy:** allow-list `dung_dockerignore.py` (nhánh `p12-deploy-nhap`) chưa có `diem_toa_do_v5.json` — cờ bật trên máy deploy cần thêm (ghi checklist deploy).
- **Rebase lên `main` `1611d34`** (ảnh cổng đã vào): xung đột 2 chỗ (`vite.config.js` `define` + `build`; Giới thiệu: câu OSM + mục Nguồn ảnh) — giữ cả hai. Sau rebase: build lại (bundle chính 108,15 KB so với `main` 106,90 ⇒ +1,25; chunk bản đồ không đổi), 5 file test 355 đạt, server cờ bật + `kiem_anh.py`: ảnh cổng đủ, 7 dòng ghi công, 0 lỗi ở 1440 / 390 (`data/phase_11/ban_do/sau_rebase/`). Lượt có phí **không** chạy lại sau rebase (phần bản đồ — `BanDoLich.jsx`, `chat.jsx`, backend — không có xung đột).
- Cờ `ban_do_lich` vẫn **tắt** trong `settings.yaml` — bật là quyết định của A / User.

## 6. Bàn giao cho người kiểm

- Đọc: `git diff 1611d34..d0adf31` (nhánh `p11-ban-do`), plan §7.
- Rủi ro cần chạy lại: (1) CSP cờ tắt giống byte + cờ bật chỉ đổi `img-src` (T3); (2) Q1 cờ bật; (3) trình duyệt trên server cờ bật: 0 lỗi CSP, không host lạ,
  câu thường không tải chunk; (4) ô ghim không đưa tên qua HTML (`BanDoLich.jsx` `oGhim`).
- Script: `data/phase_11/ban_do/tools/kiem_ban_do.py` (có phí ≈ 0,0015 USD / lần), `app_ban_do.py`. Worktree `/tmp/b_bando` giữ tới khi review xong.
