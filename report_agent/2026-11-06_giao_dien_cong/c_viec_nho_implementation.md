# Implementation Report: việc nhỏ trước đóng gói — phần C (3, 8, 10, m-1, 11, 13)

Người làm: C (Claude Code, terminal `hue-rag-e9`)
Date: 08/11/2026 (bắt đầu khoảng 10:02, report 10:27 — `date`)
Nhánh: `p11-viec-nho-c` = `2c2c1bf` (từ `main` `1611d34`, 1 commit, **đã push origin**). Worktree `/tmp/c_vn` giữ tới khi review xong.
Giao việc: A (User 08/11 duyệt "Nhóm 1 + 2" việc nhỏ trước đóng gói). Nguồn ý: `data/ra_soat_tinh_nang_2026-11-08/C.md` (A31, A13, A29, B1, B38) + m-1
của `c_anh_cong_review.md`.
Tiền: **≈ 0,009 USD** (trần 0,01) — 2 câu qua server thật 0,002246 (`chat_metrics.usd`, gồm 1 lượt tra web) + 4 lần gọi model viết mục web trong
tiến trình 0,000572 (`CallLog`) + ≤ 6 lượt Serper × 0,001 (1 lượt chạy hỏng do công cụ của C, xem §5). Tính vào Phase 9 / cổng.

## 1. Phạm vi

| Ý | Người dùng thấy gì | Code |
|---|---|---|
| (3) tóm tắt thẻ Khám phá | thẻ hiện câu giới thiệu thay vì "Tên chính thức: …" | `backend/api/routes/cong.py` `_tom_tat` (+ `_doan_dau`) |
| (8) nút "Báo thông tin chưa đúng" | ở hộp bên phải trang bài; bấm ⇒ "Cảm ơn bạn — bài này sẽ được kiểm lại." | `backend/api/feedback.py` `POST /api/bao_sai`; `frontend/src/pages.jsx` `BaoSai`; `index.css` `.ct-bao` |
| (10) ảnh nhỏ cho điện thoại | trang nhẹ hơn trên điện thoại; máy tính như cũ | 7 file `frontend/public/anh/*_nho.jpg` (mới); `anh.js` `srcNho`, `MAN_NHO`; `pages.jsx` `Anh` (`<picture><source media>`); `index.css` `picture { display: contents }`; `vite.config.js` (ảnh riêng cần cả bản nhỏ) |
| m-1 link "Nguồn ảnh" | chân trang ⇒ cuộn tới mục "Nguồn ảnh", không bị thanh đầu trang che | `App.jsx` (`#/gioi-thieu/nguon-anh`), `route.js` (`muc`), `pages.jsx` `GioiThieu({ muc })`, `index.css` `#nguon-anh { scroll-margin-top }` |
| (11) chuỗi số mục "Từ web" | mục web có số nhà / điện thoại / giờ không có trong kết quả tìm ⇒ bị bỏ như luật tiền | `backend/llm/tra_web.py` `_CHUOI_SO`, `_chuoi_so`, `kiem_muc_web` mã `so_ngoai_trich` |
| (13) `turn_id` trong `chat_metrics` | (người vận hành) nối 👍 / 👎 với số đo của đúng lượt | `backend/api/routes/chat.py` `METRIC_FIELDS` + `_set_outcome` + `StreamEvents.done` |

Không đổi: lời dặn / chuỗi gửi model, tìm kho, cờ `settings.yaml`, CSP. Ngoài phạm vi: không sửa test giao diện cũ đang hỏng (§5).

## 2. Thay đổi chính và lý do

- **(3)** Đếm trước bằng đường production (`discover_full_corpus_files` ⇒ `nap_kham_pha`, 204 bài): **100 / 204** tóm tắt mở bằng nhãn trường (Tên chính thức 38 ·
  Tên chính 35 · Tên lễ hội 25 · 2 nhãn khác). 100 bài đó đều có mục "Thông tin chung" dạng danh sách rồi một đoạn văn xuôi (thường dưới "Tổng quan").
  Sửa: lấy khối **văn xuôi** đầu tiên (bỏ dòng gạch đầu); bài chỉ có danh sách ⇒ như cũ. Sau sửa: **100 thẻ đổi, đúng 100 thẻ có nhãn**, 0 thẻ khác đổi,
  0 thẻ rỗng, độ dài 131–200 ký tự (trung vị 198); 2 thẻ còn khớp mẫu "X: …" là câu văn xuôi có ngoặc chữ Hán (không phải nhãn).
- **(8)** Cùng rào với `/api/feedback`: pydantic `extra="forbid"`, chỉ một trường `bai_id` ≤ 300 ký tự; `bai_id` phải **trùng nguyên chuỗi** một bài trong
  `app.state.kham_pha` (như `/api/kham_pha/bai`) ⇒ không ghi được chuỗi tuỳ ý vào log. Log `chat_bao_sai {"bai_id": …}`; thời điểm = dấu giờ của dòng log
  (formatter `[%(asctime)s]`). Không có chữ tự do.
- **(10)** Dùng `<picture><source media="(max-width: 760px)">` thay `srcset`: `srcset` chọn theo mật độ điểm ảnh ⇒ điện thoại 3× vẫn có thể chọn ảnh lớn;
  `media` chắc chắn theo khổ (cùng mốc 760 px của `index.css`). Bản nhỏ do `data/phase_11/anh_cong/tools/anh_nho.py` (private) dựng từ ảnh đã đóng, chạy 2 lần
  ra cùng byte: nền trang chủ **cắt dải giữa 720 × 602** (trên điện thoại khung đầu trang cao 640–790 px nên `cover` vốn chỉ hiện dải giữa ≤ ~720 px — người
  xem thấy đúng như cũ); dải đầu Khám phá thu 800 px ngang; 5 ảnh tròn cạnh ngắn 160 px (vòng 64 px). Ảnh riêng `rieng/` (gitignore): `vite.config.js` chỉ
  dùng ảnh riêng khi có **cả** `lv_festivals.jpg` và `lv_festivals_nho.jpg` (thiếu bản nhỏ ⇒ dùng ảnh Commons cho cả hai khổ, ghi công luôn khớp).
- **m-1** Hash `#/gioi-thieu/nguon-anh` ⇒ `parseHash` trả `muc`; `GioiThieu` cuộn tới id đó sau khi vẽ (effect chạy sau `scrollTo(0, 0)` của `useRoute`).
  `scroll-margin-top: 88px` vì thanh đầu trang dính.
- **(11)** "Chuỗi số" = dãy chữ số nối bằng đúng một dấu ` . : / , h` (hoặc `)` / `) ` của mã vùng) giữa hai chữ số; so bằng phần chữ số ⇒ "7h30" ↔ "7:30",
  "(0234) 3822.123" ↔ "0234 3822 123". `-` và `, ` không nối (khoảng giờ, liệt kê). Bỏ trước khi tìm: mã `[w n]` / `[n]` và số tiền (luật riêng) ⇒ mỗi lỗi
  một mã. So với chuỗi số của **tiêu đề + đoạn trích** (model thấy cả hai — `dau_vao_model`; tính riêng từng phần để không ghép nhầm số giữa hai phần).
  Câu thời gian thực: luật cũ đã cấm mọi chữ số ⇒ không kiểm thêm, giữ đường "chưa xác minh" + link nguồn. Như luật tiền: có số ngoài ⇒ cả mục bị bỏ
  ("Mình chưa tra được thông tin đáng tin trên web."). Tiêu đề được thêm **sau lượt thật đầu** (§4: bỏ nhầm "… 24/7" ở tiêu đề).
- **(13)** `turn_id` thêm cuối `METRIC_FIELDS` (cả `/api/chat` và stream dùng chung); đặt đúng chỗ mã được cấp: `_set_outcome` (không stream, từ
  `ChatResponse.turn_id`) và `StreamEvents.done` (stream). Lượt lỗi / bị rút lại / hỏi lại ⇒ `null` như trước (không có mã).

Bảng rà AI FDE: (11) là luật kiểm **bằng code** sau chữ model (đúng nguyên tắc "phép tính / trường bắt buộc ⇒ code"); không thêm công cụ, nguồn dữ liệu hay
đường ra mới. (8) là đường ghi mới nhưng chỉ ghi mã bài đã có trong danh sách (không dữ liệu người dùng).

## 3. Cách đã chạy thật

- Đếm thẻ: `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project … python data/phase_11/viec_nho_c/c_vn_tom_tat.py <out.json>` trước / sau (từ `backend/` của worktree);
  so 2 file JSON (private).
- Test: `cd backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python -m pytest tests/test_static_ui.py
  tests/test_cong_dot_1.py tests/test_feedback.py tests/test_chat_stream.py tests/test_b3_memory.py tests/test_b6_tra_web.py tests/test_api_chat.py
  tests/test_b5b_thoi_tiet.py tests/test_assistant_boundary.py -q`.
- Build `cd frontend && npm ci && npm run build`; server thật `uvicorn api.app:app --port 8896` (`--env-file` tuyệt đối), tắt bằng TaskStop.
- Ảnh: `data/phase_11/viec_nho_c/c_vn_do_anh.py` (Playwright, cộng byte mọi phản hồi `/static/anh/`, cuộn hết trang) trên bản **trước** (cùng worktree, giao diện
  chưa sửa) và **sau**; khổ 390 @1× và @3×, 1440 @1×.
- Giao diện: `c_vn_probe.py` (link chân trang từ Khám phá + khi đang ở Giới thiệu, đo vị trí mục so với đáy thanh đầu trang; nút báo sai bấm thật ⇒ mã HTTP +
  chữ; ảnh giải mã; CSP nghe trong trang; console; chụp màn hình) · `playwright_cong.py` (7 đích, CSP / console, bundle) · `tuong_phan.py` (thêm trang bài).
- Ảnh riêng: chép `rieng/lv_festivals.jpg` của B vào worktree ⇒ build (chỉ ảnh lớn) ⇒ `anh_nho.py` ⇒ build (có cả bản nhỏ) ⇒ kiểm ảnh + ghi công 390 / 1440 ⇒
  **gỡ** `rieng/` ⇒ build lại.
- Cổng ổn định trên server: 1 câu trong kho qua `/api/chat/stream` + 1 câu ngoài kho (kích tra web) qua `/api/chat` ⇒ đọc `chat_metrics` mới sau mốc dòng.
- (11) lượt thật kiểm đôi: `c_vn_web.py` gọi **đúng hàm production** `app.state.tim_web` (Serper) + `generator.generate_web_section` (gpt-6-luna) trong tiến
  trình để thấy đoạn trích; 3 câu tự viết (loại "dịch vụ đời thường ở Huế" — không từ Golden / bộ đo); mã cũ = mã mới trừ `so_ngoai_trich`.
- Hook `pre-commit` khi commit (14 file 0 trùng). `git diff --check` sạch.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Test 9 file | **244 passed / 1 failed** — failed là `test_b6_tra_web.py::test_web_section_renderer_uses_filter_without_links`, **hỏng sẵn trên `main` `1611d34`** (C chạy trên working tree chính: cùng lỗi; test đọc dòng thứ 4 của `renderWebHtml` trong `markdown.js`, file đổi ở `27ed091` 07/11) — không do nhánh |
| (3) thẻ | 100 / 204 đổi, đúng 100 thẻ có nhãn; 0 thẻ khác đổi; test `test_card_summary_skips_label_bullets` |
| (8) API | bài có thật ⇒ 200 `{"ok": true}`; `../.env`, bài không có, đổi hoa, rỗng, thiếu trường, thêm trường chữ tự do, 301 ký tự ⇒ 404 / 404 / 404 / 422 / 422 / 422 / 422; log đúng 1 dòng `{"bai_id": …}` (test `test_report_wrong_info_logs_only_known_article_id`) |
| (8) giao diện | 1440 + 390: bấm ⇒ HTTP 200, chữ "Cảm ơn bạn — bài này sẽ được kiểm lại."; server ghi 2 dòng `chat_bao_sai` chỉ có `bai_id` |
| (10) byte ảnh | **390 (@1× và @3×): trang chủ 424,1 ⇒ 148,2 KB (−65 %), Khám phá 447,2 ⇒ 106,8 KB (−76 %)**; 1440: 424,1 / 447,2 KB **không đổi** (vẫn ảnh lớn); mọi ảnh giải mã; ảnh tròn 64 px (390) / 112 px (1440) |
| (10) ảnh riêng | chỉ ảnh lớn ⇒ cờ tắt (bundle không có "Cục Du lịch"), dùng Commons; có cả bản nhỏ ⇒ 390 tải `rieng/lv_festivals_nho.jpg`, 1440 tải `rieng/lv_festivals.jpg`, ghi công "Cục Du lịch Quốc gia Việt Nam" cả hai; `git ls-tree` nhánh: 0 đường dẫn `rieng` |
| m-1 | từ Khám phá ⇒ hash `#/gioi-thieu/nguon-anh`; 390: tiêu đề mục ở 88 px, đáy thanh đầu trang 57 px (không bị che); 1440: mục ở 281 px (trang ngắn, đã cuộn hết); bấm khi đang ở Giới thiệu cũng cuộn |
| (11) test | 9 ca mới: số cách viết khác vẫn đạt; số nhà / giờ / điện thoại bịa ⇒ `so_ngoai_trich`; số ở tiêu đề đạt; mã kho / tiền / thời gian thực vẫn một mã |
| (11) lượt thật lần 1 | câu phòng tập: mục web bị bỏ vì số "247" của tên "… 24/7" — tên nằm ở **tiêu đề** kết quả, luật bản đầu chỉ so đoạn trích ⇒ **bỏ nhầm** ⇒ sửa so cả tiêu đề + test |
| (11) lượt thật sau sửa | 3 / 3 câu đạt kiểm (mã mới = mã cũ = rỗng): câu phòng tập giờ có mục web; câu rạp chiếu phim (tầng, số nhà có trong trích) và câu sửa xe (2 số nhà có trong trích) đạt. Chưa gặp ca **bắt đúng** số bịa trên lượt thật (n = 3) — ca bắt đúng chỉ có ở test |
| (13) | server: `chat_metrics.turn_id` = `turn_id` trong sự kiện `done` (stream) và trong thân `/api/chat`; test khoá cả hai route + lượt lỗi `null` |
| Cổng ổn định | `/health` 5 / 5; câu trong kho: success, có nguồn, chữ đầu 2,70 s, tổng 4,56 s; câu ngoài kho: từ chối + tra web (lượt này mục bị bỏ nhầm — trước sửa tiêu đề); `chat_metrics` mới = 2 = số câu; grep chữ câu hỏi trong log = 0 |
| Giao diện chung | `playwright_cong.py`: 7 / 7 đích ở 1440 + 390, CSP 0, console 0, JS gzip 103,0 KB; `tuong_phan.py` (thêm trang bài): 16 cặp, 0 cặp < 4,5; không cuộn ngang |

Bằng chứng private: `data/phase_11/viec_nho_c/` (JSON trước / sau, ảnh chụp, công cụ dò, kết quả lượt web).

## 5. Lỗi và giới hạn

- **Test hỏng sẵn trên `main`** (ngoài phạm vi): `test_web_section_renderer_uses_filter_without_links` — C không sửa; báo A.
- (11) Luật **chặt theo cách viết**: số bỏ mã vùng ("3822.123" khi trích ghi "(0234) 3822.123") hay cắt dở ⇒ cả mục bị bỏ (phía an toàn — mất mục web, không nói
  sai). Lượt thật mới n = 3 nên tỉ lệ bỏ nhầm còn chưa biết; nên theo dõi `web_kiem` có `so_ngoai_trich` trong `chat_metrics` sau khi bật.
- (11) Lượt chạy hỏng 1 lần: công cụ của C gọi `asyncio.run` nhiều lần ⇒ client OpenAI mất event loop (`Event loop is closed`) — lỗi công cụ, không phải hệ
  thống; tốn ≤ 2 lượt Serper + 1 lần gọi model, đã tính vào tiền ở trên.
- m-1: bấm lại link khi hash đã là `#/gioi-thieu/nguon-anh` (đã cuộn lên) thì không cuộn lại (không có sự kiện đổi hash).
- (10) Ảnh nền trang chủ trên điện thoại vẫn bị phóng như cũ (ảnh gốc chỉ cao 602 px, khung cao ~760 px) — bản cắt giữ đúng điểm ảnh cũ, không tệ hơn.
- Sau merge: working tree chính muốn hiện ảnh #5 thì chạy `dong_anh.py` (B) **rồi** `anh_nho.py` (C) trước `npm run build`; thiếu bản nhỏ ⇒ dùng ảnh Commons.
- Chồng file: B `p11-ban-do` (`pages.jsx` Giới thiệu, `chat.jsx`, `app.py`), E `p10-anh-bat` (`GioiThieu({ anh })` — nhánh này `GioiThieu({ muc })`: gộp
  thành `GioiThieu({ anh, muc })`) ⇒ bên merge sau rebase.

## 6. Bàn giao cho người kiểm

- Đọc `git diff 1611d34..p11-viec-nho-c` (14 file + 7 ảnh `_nho`).
- Rủi ro nên chạy lại: (1) luật (11) với ca dò khác cách C (số trong tiêu đề / trích nhiều dạng, câu thời gian thực, tiền + số); (2) `/api/bao_sai` thử phá
  (chuỗi lạ, id gần đúng, thân lớn); (3) điện thoại 390 tải bản nhỏ, 1440 bản lớn; ảnh riêng có / không có bản nhỏ; (4) `turn_id` trong `chat_metrics` hai route.
- Công cụ: `data/phase_11/viec_nho_c/c_vn_do_anh.py <base>`, `c_vn_probe.py <base> <thư mục ảnh chụp>`; `data/phase_11/anh_cong/tools/anh_nho.py <frontend>`.

**Giải thích ngắn:** sáu sửa nhỏ để cổng dùng được ngay. Thẻ Khám phá giờ hiện câu giới thiệu thay vì nhãn trường. Trang bài có nút báo sai (chỉ ghi
mã bài). Điện thoại tải ảnh nhẹ hơn khoảng 3 lần. Link "Nguồn ảnh" cuộn tới đúng chỗ. Mục web không được nêu số (địa chỉ, điện thoại, giờ) mà kết quả tìm
không có. Mỗi dòng số đo có mã lượt để nối với 👍 / 👎.
