# Review: Phase 9 B6 — tra web (Serper) qua cổng code, cả nhánh `p9-b6`

Decision: **changes_requested** (0 blocker / 2 major / 2 minor)
Người kiểm: E (Claude Opus 5.5, `hue-rag-bc`) · việc **E13** (A giao) · một vòng
Date: 20:56 05/11/2026 (`date`)
Canonical guide: plan `docs/superpowers/plans/2026-11-05-phase-9-b6-plan.md` bản 3 (`6e5c3b21065d` lúc duyệt; file nay `ea3d4b1fe31c` = + "Chỗ đổi vòng chỉnh 1") · spec Phase 9 bản 12 `77250689e605` §3 (sơ đồ "CỔNG WEB", "`tra_web` không là công cụ"), §5 B6 (rào 1–5), §7
Implementation report: `report_agent/2026-11-02_phase_9_code/b165_b6_implementation.md` (§1–§9)

## 1. Phạm vi đã review

- Nhánh `p9-b6` **`9140152`** (rebase lên `main` `b75fefc`; A chuyển sha). `git range-diff 2693422..cedac73 b75fefc..9140152`: commit 2, 3 giống hệt; commit 1 chỉ khác ngữ cảnh (import `nhan_anh`, khối `anh:`) ⇒ code B6 = khoá `cedac73`.
- Diff `b75fefc..9140152`: 12 file, +757 / −22 (`backend/llm/tra_web.py` mới, `assistant.py`, `chat.py`, `app.py`, `generator_openai_full_corpus.py`, `full_corpus_prompt.py`, `settings.yaml`, `conversations.py` (docstring), `frontend/src/markdown.js`, `App.jsx`, `test_b6_tra_web.py` mới, `test_assistant_boundary.py`). Không file untracked trong diff. `git diff --check` sạch.
- Đọc hết: `tra_web.py`; diff `assistant.py` (`web_gate_open`, `cong_web`, `_web_stream`, 3 đường gọi, `turn_usd`); diff `chat.py` (`_web_payload`, sự kiện `web`, log D9); `app.py` (`app.state.tim_web`); lần gọi `hue_web_section` + `TU_WEB_LUAT`; `markdown.js` `renderWebHtml` + `SANITIZE_OPTIONS`; `App.jsx` `WebSection`.
- Đối chiếu từng điểm A dặn: (1) cổng chỉ mở sau câu từ chối · (2) chữ web không vào `answer` · (3) kiểm `[w n]` ∈ sổ / link / tiền / câu thời gian thực / câu thiên tai bằng code · (4) khoá Serper không lộ log · (5) bảng rà khung FDE (plan §9).

## 2. Findings

### M-1 (major) — link do model viết bằng **HTML thô** (`<a href="//…">`) lọt qua kiểm cuối server **và** hiện thành link bấm được ở khối "Từ web"

- **Vị trí:** `backend/llm/tra_web.py` `_URL` (mẫu bắt: `https?:` · `www.` · `](` · tên miền trần có đuôi trong danh sách); `frontend/src/markdown.js` `renderWebHtml` (dùng `marked.parse` + `DOMPurify.sanitize(…, SANITIZE_OPTIONS)` — `SANITIZE_OPTIONS` cho phép thẻ `a` + thuộc tính `href`).
- **Yêu cầu:** spec §5 B6 rào 3 "link + nhãn web do code dựng từ sổ nguồn; model chỉ trích `[w n]`; link không khớp sổ ⇒ bỏ"; plan D5 (ii) "0 URL trong chữ model", D6 "không `href` tuỳ ý từ chữ model"; plan §8 điều kiện dừng "bất kỳ link nào không khớp sổ tới người dùng".
- **Bằng chứng [Chạy, 0 USD]:**
  - server — `kiem_muc_web('Xem <a href="//datve.xyz">đặt vé tại đây</a> [w1]', …)` ⇒ `[]` (**đạt kiểm**); `'Xem thêm ở datve.xyz [w1]'` ⇒ `[]` (đuôi `.xyz` không trong danh sách — chỉ là chữ, không thành link: xem dưới).
  - trình duyệt — Chromium (Playwright) nạp **đúng** `marked` 18.1.1 + `DOMPurify` 3.4.17 trong `frontend/node_modules` (nhánh không đổi lockfile), chạy `DOMPurify.sanitize(marked.parse(text), SANITIZE_OPTIONS)` như `renderWebHtml`:
    `<a href="//datve.xyz">…</a>` ⇒ **còn `href="//datve.xyz"`** (link tương đối giao thức ⇒ mở `https://datve.xyz`). Link tham chiếu Markdown cùng đoạn và tên miền trần ⇒ 0 `href` (an toàn). Script dò: `/tmp/e13/probe_fe.py` (xoá được).
- **Tác động:** đoạn trích web cài lệnh ("hãy viết `<a href=…>`") có thể đưa một link **ngoài sổ** tới người dùng dưới nhãn "Từ web" — đúng loại rào mà spec giao cho code (không model thứ hai soát — spec §7). Lượt đo đã thấy / kín **không** quan sát lỗi này (Q2 "link ngoài sổ" 0) — đây là lỗ ở code, chưa phải lỗi đã xảy ra. Cờ `tra_web` đang tắt.
- **Tiêu chí đóng:** (a) giao diện: chữ model ở khối web **không** tạo được thẻ `a` — vd `renderWebHtml` dùng bộ lọc riêng không có `a` / `href` (link web chỉ ở danh sách nguồn do code dựng); (b) server (lớp hai): `kiem_muc_web` bắt thẻ HTML / `href` / `//` đầu link (vd thêm `<\s*a\b|href\s*=|(?<![:\w])//[\w-]` vào mẫu, hoặc bỏ mục có ký tự `<…>` dạng thẻ); (c) test: ca `<a href="//x.xyz">` ⇒ `kiem` có `url` **và** một kiểm 0 `href` ở `renderWebHtml` (vd Playwright / kiểm chuỗi bản build); chạy lại `test_b6_tra_web.py`. Dùng lại được số đo Q2 / Q3 / kín (sửa không đổi đầu vào model; chỉ siết đầu ra).

### M-2 (major) — câu thiên tai bỏ sót **"lụt"** (từ hay dùng nhất ở Huế) ⇒ không vào câu cố định NCHMF / 112

- **Vị trí:** `backend/llm/tra_web.py` `_THIEN_TAI` = `lũ | bão | ngập | sạt lở | triều cường`.
- **Yêu cầu:** "Chỗ đổi vòng chỉnh 1" (A quyết 20:29): "câu có dấu hiệu thiên tai ⇒ không chữ web do model viết, code nối câu cố định (NCHMF / chính quyền / 112)".
- **Bằng chứng [Chạy]:** `la_cau_thien_tai("Huế đang lụt không?")` ⇒ **False**; `"Đường lên Bạch Mã có bị lụt không"` ⇒ False; `"Áp thấp nhiệt đới vào Huế chưa"` ⇒ False (và `la_cau_thoi_gian_thuc` cũng False cho ba câu này ⇒ không cả luật 0 chữ số). Đối chứng: `"Huế có lũ không"`, `"…có ngập không"` ⇒ True.
- **Tác động:** đúng loại câu đã phạm sàn ở đã thấy (X05 — mức lũ có số mét, câu an toàn) đi lại đường model viết từ đoạn trích, chỉ đổi một từ đồng nghĩa phổ biến. An toàn ⇒ không hạ thành minor.
- **Tiêu chí đóng:** thêm ít nhất `lụt` (gồm "lũ lụt", "ngập lụt") và `áp thấp` vào `_THIEN_TAI` + test cho từng từ (cả ca ranh giới từ như "lũy" đang có); kiểm lại trên bộ đã thấy rằng **không** câu `web_tra_loi_duoc` nào khớp thêm (như cách B đã làm ở vòng 1) ⇒ dùng lại Q3. Ghi giới hạn: danh sách từ khoá không bao giờ đủ (dò bằng từ khoá).

### m-1 (minor) — khoá Serper nằm trong `repr` của `app.state.tim_web`

- **Vị trí:** `backend/api/app.py` `app.state.tim_web = functools.partial(tim_web, api_key=…)`.
- **Bằng chứng [Chạy]:** `"KHOA_GIA_123" in repr(functools.partial(tim_web, api_key="KHOA_GIA_123", …))` ⇒ **True**. Hiện **không** chỗ nào log / in đối tượng này (grep `backend/api`, `backend/llm`) ⇒ chưa lộ.
- **Tác động:** một dòng debug / traceback có biến cục bộ sau này có thể in khoá vào log.
- **Tiêu chí đóng (sửa lúc merge hoặc bậc sau):** gói bằng hàm lồng (closure) không lộ khoá trong `repr`, hoặc ghi giới hạn.

### m-2 (minor) — câu "đang …" không thuộc luật thời gian thực

- `_THOI_GIAN_THUC` không có "đang" ("đường lên Bạch Mã đang đóng không?") — mục web được viết số / giờ từ đoạn trích. Ít rủi ro hơn M-2 (không phải câu an toàn). **Đóng:** ghi vào giới hạn (dò từ khoá) hoặc thêm "đang" nếu B thấy không bắt nhầm câu `web_tra_loi_duoc` trên bộ đã thấy.

**Không có blocker.** Không thấy over-engineering phải gỡ: `tra_web.py` ~190 dòng, mỗi hàm một việc; lệch plan (D7 không cắt vì chữ web không bao giờ vào `answer`; mục web một sự kiện) là cách trực tiếp hơn và có test.

## 3. Cách người kiểm chạy lại thật

```bash
git -C /home/minhhieu/hue_rag worktree add --detach /tmp/e13/wt origin/p9-b6   # rồi checkout 9140152; symlink data/ + knowledge-base-hue/
cd /tmp/e13/wt/frontend && npm ci && npm run build
cd /tmp/e13/wt/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest -q -p no:cacheprovider \
  tests/test_b6_tra_web.py tests/test_assistant_boundary.py tests/test_p10_anh.py tests/test_static_ui.py tests/test_b5_lich_trinh.py \
  tests/test_b2_tool_loop.py tests/test_b3_memory.py tests/test_toc_do_song_song.py tests/test_assistant.py tests/test_chat_stream.py \
  tests/test_feedback.py tests/test_emergency.py tests/test_citations.py
# dò server: uv run … python - (gọi tra_web.kiem_muc_web / la_cau_thien_tai / la_cau_thoi_gian_thuc với chuỗi tự viết)
# dò trình duyệt: uv run python -I /tmp/e13/probe_fe.py  (Chromium + marked/DOMPurify của frontend/node_modules)
```
Qdrant thật (6 test B6 cần), không khoá Serper, không khoá OpenAI, 0 USD.

## 4. Kết quả quan sát

| Điểm A dặn | Kết quả | Căn cứ |
|---|---|---|
| (1) cổng chỉ sau câu từ chối | **khớp** — `web_gate_open` một chỗ: `answer.strip() == INSUFFICIENT_ANSWER` ∧ tuyến `tro_ly_hue` ∧ `fixed_outcome ∈ {None, refusal_no_sources}` ∧ không lỗi citation / công cụ / hỏi lại / lịch / `truong` ∧ chưa tra ∧ cờ ∧ có hàm tra; gọi ở `answer_turn`, `answer_turn_stream` (cả nhánh `refusal_no_sources`), `answer_turn_stream_parallel` **sau** `_merge_spec`; phần chạy song song tắt `tra_web` ⇒ câu trò chuyện không ra Serper | đọc code; test 13 nhánh cổng + 3 đường (trong 264 passed) |
| (2) chữ web không vào `answer` | **khớp** — chữ web chỉ ở `trace.web`, không qua `delta`; `stored_answer` không cần cắt; tra web nằm **ngoài** hạn giờ từng sự kiện của lần gọi model chính (không làm hỏng câu kho đã xong) | đọc `answer_turn_stream`; test route "lịch sử không chứa chữ web" |
| (3a) `[w n]` ∈ sổ, mỗi đoạn có mã, không mã kho | khớp | `kiem_muc_web` |
| (3b) link | **lệch — M-1** | dò server + trình duyệt |
| (3c) tiền ⊂ đoạn trích; lưu trú 0 tiền | khớp (dùng `so_tien.tim_so_tien` B5c) | đọc code + test |
| (3d) câu thời gian thực | khớp theo từ khoá; thiếu "đang" (m-2) | dò |
| (3e) câu thiên tai | **lệch — M-2** ("lụt", "áp thấp") | dò |
| (4) khoá Serper | không vào log / trace / phản hồi (chỉ header `X-API-KEY`; lỗi ghi mã ngắn, không thông điệp); thiếu khoá ⇒ `loi`, 0 kết nối; `repr` của partial có khoá (m-1) | đọc code + dò |
| (5) bảng rà FDE (plan §9) | đủ mục §1–§5 + bộ ba + cài lệnh + trước deploy; dòng "link chỉ từ sổ" ghi **khớp** nhưng code chưa khớp ở giao diện (M-1) | plan §9 |
| Test | **264 passed** (13 file, gồm 6 test B6 cần Qdrant, test ảnh Phase 10, `test_static_ui` trên bản build của worktree) | chạy |
| Q1 sau rebase | **dùng lại** bằng chứng của B: file nhánh `9140152` và file `main` `80faf1a` cùng sha `dba1f578eef1` (E tự `sha256sum`, 228 dòng); `80faf1a..b75fefc` chỉ đổi `frontend/src/index.css` (E tự `git diff --stat backend frontend/src`) ⇒ lý do dùng lại đúng | kiểm lại |
| Số đo có phí (Q2–Q5, Q8, kín C203) | **không chạy lại** — dùng số của report §7–§9 + tin A (kín ×2 đạt, B6 ≈ 0,185 / 0,22) | ngoài phạm vi một vòng review code |

**Bất biến kiểm:** cờ `tra_web` tắt ⇒ 0 lần gọi Serper + chuỗi gửi model giống byte `main` — giữ (test "flag off never" trong 264 + Q1 dùng lại có căn cứ).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy server thật / Playwright / lượt có phí. Dò M-1 chạy bộ lọc thật của dự án trong Chromium nhưng **ngoài** trang của app (không dựng lại toàn bộ `WebSection`) — đủ cho kết luận "bộ lọc giữ `href`".
- Không kiểm model có thật sự viết HTML khi đoạn trích cài lệnh (cần lượt có phí) — finding là lỗ của rào code, không phải lỗi đã quan sát.
- Không đọc bộ kín (đúng vai).

## 6. Decision và bước tiếp theo

**changes_requested** — B sửa M-1 (giao diện không tạo link từ chữ model + server bắt thẻ / `href` / `//`) và M-2 (`lụt`, `áp thấp` + test + kiểm bộ đã thấy) trong một lượt; m-1, m-2 sửa luôn hoặc ghi giới hạn. Kiểm lại: E xem đúng hai chỗ sửa + chạy `test_b6_tra_web.py` + lặp lại hai dò (server + `probe_fe.py`); **dùng lại** Q1–Q5 / Q8 / kín vì sửa chỉ siết đầu ra / thêm từ khoá (với điều kiện M-2 không khớp thêm câu `web_tra_loi_duoc`). Sau đó A merge **cờ tắt** như kế hoạch; bật cờ là quyết định của User (chữ đầu mục web p50 ≈ 13 s — Q5).

---

## Vòng 2 — kiểm phần sửa `77d51b6` (B169) · 21:05 05/11/2026 (`date`) · E (việc **E15**)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 0 minor mở)
Phạm vi: diff `9140152..77d51b6` — 4 file (`tra_web.py`, `app.py`, `markdown.js`, `test_b6_tra_web.py`), +65 / −10, `git diff --check` sạch; report b165 §11. Code ngoài 4 file không đổi ⇒ phần đã khớp ở vòng 1 dùng lại.

| Finding | Kiểm lại [Chạy, 0 USD] — cách **khác** B | Kết quả |
|---|---|---|
| **M-1** link HTML thô | (giao diện) nạp **chính `renderWebHtml` của nhánh** (`frontend/src/markdown.js` qua import map, `marked.esm` + `purify.es.mjs` của `frontend/node_modules`) vào Chromium — không chép lại bộ lọc như dò vòng 1 / B — 5 ca: `<a href="//…">`, `[x](https://…)`, `<a href="https://…">`, link tham chiếu `[x][d]` + `[d]: //…`, mã ngoài sổ `[w9]` ⇒ mọi ca chỉ còn link nội bộ `#web-L1-1` (của `[w1]`), **0 link ngoài** (`/tmp/e13/probe_fe2.py`). Đối chứng cùng script trên `9140152`: 4 / 4 ca có link ngoài — dò bắt được lỗi cũ, kể cả link tham chiếu tách đoạn mà dò vòng 1 không phủ. (server) `kiem_muc_web`: `<a href="//…">`, `< A HREF = …>`, `//1.2.3.4/x` ⇒ `url`; chữ thường `7h–22h`, `1/2` ⇒ không bắt nhầm | **đóng** |
| **M-2** thiên tai | `la_cau_thien_tai`: "Huế đang lụt không?", "… ngập lụt …", "Áp thấp nhiệt đới …", "Áp thấp vào chưa" ⇒ True; "Thành lũy …", câu món ăn ⇒ False | **đóng** |
| m-1 khoá trong `repr` | `_tim_web_server({})` với khoá giả trong env ⇒ khoá **không** có trong `repr`, không nằm trong closure (đọc env mỗi lần tra) | **đóng** |
| m-2 "đang" | E tự đếm trên `data/phase_9/bo_do_b6/cau_da_thay.jsonl`: câu có "đang" = **W08 (`web_tra_loi_duoc`)** — khớp lý do B. Thêm "đang" ⇒ luật "0 chữ số" chạm cả câu web trả lời được (giờ / giá có ích) và chữ này quá phổ biến ⇒ lý do **đủ**; ghi giới hạn (report §11) | **đóng bằng giới hạn** |
| Test | build `npm run build` worktree; `test_b6_tra_web` + boundary + `test_static_ui` + `test_p10_anh` + `test_chat_stream` + `test_toc_do_song_song`: **147 passed** (B báo 277 cho 13 file + test mới) | đạt |
| Q1 | dùng lại (B: `q1_e13/nhanh.jsonl` ↔ `main_80faf1a`; sửa không chạm chuỗi gửi model — chỉ đầu ra / từ khoá / cách cầm khoá) | lý do đủ |

**Dùng lại bằng chứng có phí** (Q2–Q5, Q8, kín C203): hợp lệ — sửa chỉ siết đầu ra (bộ lọc giao diện, mẫu URL) + thêm 2 từ khoá thiên tai không khớp thêm câu `web_tra_loi_duoc` (B kiểm; E kiểm W08 riêng cho "đang").

**Giới hạn còn lại (không chặn):** dò thiên tai / thời gian thực bằng từ khoá không bao giờ đủ; chữ đầu mục web p50 ≈ 13 s (Q5); điều khoản Serper chưa rõ (User chấp nhận P5); tên trong cùng câu ra Serper (theo dõi).

**Kết luận:** ready — A merge **cờ `tra_web` tắt** được; **bật cờ là quyết định của User** (chất lượng Q2 / Q3 / kín đạt; đánh đổi: độ trễ ~13 s cho câu kho từ chối, 0,0018 USD / câu đường web, điều khoản Serper).

## Kiểm bật cờ (C) — C206, 21:18 05/11/2026 (`date`)

Kết luận: **ready** — 0 blocker · 0 major · 1 minor. Người kiểm: C (`hue-rag-3c`); A làm, C kiểm (review chéo). 0 USD.
- **Diff `b7c024e`:** phần code đúng **1 dòng** — `backend/config/settings.yaml` `tra_web: false ⇒ true`; 3 file còn lại là báo cáo cho User (SINH, LUONG, README).
- **Khớp khoá B6:**
  - `TU_WEB_LUAT` trên `main` = **`e5f516aa383e`**;
  - `backend/llm/tra_web.py` `main` = bản sau sửa E13 `77d51b6` (sha256 `f6f8704e2dd2` cả hai);
  - `full_corpus_prompt.py`, `assistant.py`, `generator_openai_full_corpus.py`, `api/routes/chat.py`: diff `77d51b6..HEAD` rỗng;
  - `load_settings()`: `tra_web` True, kèm `router` + `tim_them` True, timeout 5 s.
- **Test trên `main`** (không khoá OpenAI / Serper): `tests/test_b6_tra_web.py` + `tests/test_assistant_boundary.py` — **80 passed**.
- **Log `chat_metrics` 3 câu cổng** (`backend/logs/application.log`, 21:13:53 / 21:14:02 / 21:14:05) — khớp số A ghi:
  - (1) `co_muc`, 5 kết quả, 1 mã, `web_kiem` [], 18,2 s, 0,00184 USD;
  - (2) `thien_tai`, 5 kết quả, 0 mã, không mục web (câu cố định), 9,1 s;
  - (3) không tra web, 3,1 s.
  - Mọi trường thuộc `METRIC_FIELDS` / `STREAM_METRIC_FIELDS`, không trường lạ, không chuỗi > 40 ký tự (không chữ câu hỏi).
  - 16 dòng log 21:10–21:19: **0** dấu hiệu khoá (`x-api-key`, `api_key`, `bearer`, `sk-…`).
- **m-1 (minor, theo dõi):** câu thiên tai vẫn **gọi Serper** (5 kết quả, 0,00157 USD) rồi mới trả câu cố định.
  - Đúng thiết kế `cedac73`: câu cố định kèm link sổ, nên cần kết quả.
  - Nhưng tốn ~0,001 USD / câu cho phần không dùng chữ web. Nếu sau này chỉ cần link cố định (NCHMF / chính quyền) ⇒ có thể bỏ lần gọi. Không chặn.
- Ghi chú: 2 dòng `chat_metrics` lúc 21:17:29 (72–92 ms) không phải câu cổng — nhiều khả năng do pytest ghi cùng file log (bẫy `Project_Status` §8).

