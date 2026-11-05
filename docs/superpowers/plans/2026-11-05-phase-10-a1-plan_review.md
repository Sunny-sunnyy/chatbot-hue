# Review: plan Phase 10 A0 + A1 + A1b (route ảnh) — vòng 1

Decision: **changes_requested** (0 blocker · 1 major · 7 minor)
Người kiểm: C (Claude Opus 5.5, `hue-rag-52`) — việc **C187**, A giao
Date: 10:44 05/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-05-phase-10-a1-plan.md` bản 1 — sha tính từ file **`2b30ebac8c02`** (E viết)

## 1. Phạm vi đã review

Chỉ theo mục "Căn cứ để review" của plan; không đọc STATUS / tin nhắn của E.
- Plan: toàn bộ, gồm bảng rà §8.
- Spec Phase 10 bản 2 — sha tính từ file **`bf67b90fb6fc`** (khớp plan): §2 A1–A10 · §3.1, §3.2 · §4 A0–A4 · §5 Q-a…Q-k + luật A/A + dòng "Không hồi quy" · §6 · §7 · §12.
- Code `main` (`ea114ae` lúc review; plan viết trên `b019aab` — các file dẫn không đổi giữa hai commit ở các dòng dẫn): `backend/api/app.py` :36–39 (CSP), :53–58 (lifespan nạp `settings`), :166–168 (đăng ký router), **:209 `app = create_app()`**; `backend/llm/generator_openai_full_corpus.py` :74 (`ROUTER_MAX_OUTPUT_TOKENS = 512`, "gồm cả token suy luận"), :206, :229–259 (`responses_model`, `ModelSettings(… store=False)`), :314–336 (`_run` nhận `str | list[dict]`); `backend/llm/pricing.py:12`; `backend/api/routes/chat.py` :36–40 (`METRIC_FIELDS`). 0 USD, chỉ đọc.

## 2. A quyết (ghi vào review theo A)

- **(1) Người dựng bộ ≠ người code (plan §1 "Lệch spec §3.2"):** **A đồng ý** — E chỉ viết **công cụ** tải ảnh (giấy phép mở, có phiếu nguồn — D12); **C chọn 33 ảnh đã thấy + 10 ảnh kín, gắn nhãn và giữ bộ kín**; E không mở phần kín.
- **(2) Bỏ rào "một lượt ảnh / phiên" (D10, lệch nhỏ spec §6):** **A đồng ý** — route ảnh không có phiên (cookie chỉ ở `/api/chat`); rào gửi chéo đã ở D6; giới hạn theo IP là **đầu vào Phase 12**.

## 3. Findings

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| **M-1** | major | §4 T9 "Q1" | Spec §5 dòng "Không hồi quy Golden / an toàn": **"kiểm bằng Q1 kiểu Phase 9 — cờ `anh` tắt **và** bật ⇒ chuỗi gửi model của `/api/chat*` giống byte `main`"**. T9 chỉ có "cờ tắt ⇒ 404 + pytest các file chat đạt" — không bắt chuỗi gửi model, không có ca cờ **bật** | Sàn hồi quy của spec không được đo. D1 chạm `app.py` + `settings.yaml` (file dùng chung với chat) và D3 dựng `Agent` thứ hai lúc nạp generator ⇒ chính chỗ có thể làm lệch đường chat mà pytest không bắt (Phase 9 dùng `capture_all.py` vì lý do này) | T9 thêm: `data/phase_9/b2_chay/tools/capture_all.py` (0 USD, không gọi mạng) trên nhánh với `anh.bat: false` **và** `anh.bat: true` ⇒ `cmp` với bản bắt của `main` cùng commit nền (228 / 228 mỗi bên) |
| m-1 | minor | D2, §3 dòng `app.py`, T9 | `app = create_app()` (`app.py:209`) chạy **không có** `settings`; `settings` chỉ nạp trong lifespan (`:55–58`) — **sau** khi `include_router` (`:166–168`) đã chạy ⇒ "chỉ `include_router` khi `bat: true`" (D2) không làm được như chữ plan ở đường chạy thật (`uvicorn api.app:app`); test dùng `create_app(load_settings())` (`tests/test_api_chat.py:38`) thì làm được ⇒ test qua mà server thật sai | cờ tắt có thể vẫn mở route (hoặc không bao giờ mở) tuỳ cách code chọn lúc làm | chọn một cách ghi vào D2: (a) **luôn đăng ký router**, lifespan đặt `app.state.anh` (cờ + danh sách + `MAX_IMAGE_PIXELS`), handler trả 404 khi cờ tắt — C nghiêng (a): không đổi thứ tự khởi động; hoặc (b) nạp `settings` trong `create_app` khi `None`. T9 / T8 chạy trên **uvicorn thật** (đường `create_app()` không tham số) |
| m-2 | minor | D3 `ModelSettings(max_tokens=200)` | Với model có suy luận, trần token ra **gồm cả token suy luận** (code ghi ở `generator_openai_full_corpus.py:74`, định tuyến dùng 512); spec §7 ước "đầu ra + suy luận ≈ 100–500 token" ⇒ 200 có thể cắt giữa chừng ⇒ đầu ra hỏng ⇒ mọi ảnh thành `khong_doan_duoc` (D8) và A2 đo nhầm chất lượng | Q-a / Q-c đo trên lỗi cấu hình, không phải năng lực model | đặt trần như định tuyến (512) hoặc ghi lý do; A1b ghi `reasoning_tokens` + trạng thái đầu ra (đủ / bị cắt) và thêm điều kiện dừng "đầu ra bị cắt ở bước 0 ⇒ báo A" |
| m-3 | minor | D11 nguồn tên | (a) `knowledge-base-hue/heritages/**` gồm cả file hướng dẫn / kiểm kê (vd `heritage-guides.md`) có dòng `# ` không phải tên di tích ⇒ lọt tên lạ vào danh sách (spec §3.1 đếm "29 file" di sản). (b) Đọc thẳng file kho thay vì `scripts/grep_kb.sh` (`Session_Prompt.md` §5: tìm trong nội dung kho dùng script này — luôn loại `evaluation/`, `meta/`, `*sealed*`) | danh sách enum có tên rác ⇒ model có thể chọn; khác cách đọc kho của mọi việc khác | loại `*-guides.md`, `*inventory*`; lấy dòng `# ` bằng `scripts/grep_kb.sh --dir heritages -H -n "^# "` (và `--dir foods/local_specialties`); ghi số file / tên đếm được so spec §3.1 |
| m-4 | minor | §1, D12, A1b | Theo A quyết (1): **C** chọn ảnh + giữ nhãn / kín. Plan còn: §1 "C hoặc A chọn"; spec §3.2 "ảnh chữ ra lệnh: E / C tự tạo" — E code rào chữ trong ảnh (D5) ⇒ E tạo ảnh tấn công là người code tự dựng ca đo của mình; A1b "ảnh Commons đầu tiên do người chọn đưa" chưa nói ảnh **đã thấy** hay kín | trộn vai người dựng / người code ở đúng ca Q-d; lỡ dùng ảnh kín ở bước 0 | §1: "C chọn 33 + 10, giữ nhãn + kín; **3 ảnh chữ ra lệnh do C tạo**; E chạy `tai_anh.py` trên danh sách tên file C đưa, ảnh kín C tự tải bằng công cụ của E"; A1b: ảnh lấy từ **phần đã thấy**, C chỉ định tên file |
| m-5 | minor | T8 | Spec §4 A1: mỗi ca bị từ chối khẳng định **0 lần gọi model và không có file tạm mới**. T8 có `n_llm_calls: 0` + RSS, chưa kiểm file tạm | Q-g "không ghi ảnh ra đĩa" + lý do bỏ multipart (spec A10: Starlette ghi file tạm) không có bằng chứng | T8 thêm: liệt kê thư mục tạm của tiến trình (`tempfile.gettempdir()`) trước / sau 5 ca + 1 ca 11 MB ⇒ không file mới |
| m-6 | minor | §6 bước 5 (A1b + cổng) | Spec §4 A2 + `WORKFLOW.md` §9.2 (W31): lượt có phí không chạy cùng lúc lượt đo tốc độ / việc nặng của Phase 9; plan chỉ ghi điều này cho A2 (trong spec), không cho A1b / cổng (server thật + model) | lượt có phí của Phase 10 chồng lượt đo latency Phase 9 ⇒ số p95 bên Phase 9 hỏng | §6 bước 4–5: "hỏi A trước khi chạy T8 / A1b / cổng — không chạy khi Phase 9 đang đo tốc độ" |
| m-7 | minor | §8 bảng rà | Thiếu hai dòng khung FDE: **trần + đường phục hồi** (một lần gọi, timeout 15 s, lỗi / hết giờ / đầu ra hỏng ⇒ 200 `khong_doan_duoc`, không thử lại — đã có ở D8 nhưng không trong bảng) và **đầu ra có cấu trúc kiểm lại ở backend** (D4: id ∈ danh sách, ≤ 3, bỏ trùng) | bảng rà là chỗ reviewer / báo cáo bảo vệ đọc nhanh | thêm 2 dòng, trỏ D4 / D8 + test T6 |

## 4. Đã kiểm, khớp (không phải finding)

- **Phạm vi:** A0 (danh sách tên + công cụ tải) / A1 (route + rào + xử lý ảnh + log) / A1b (bước 0) đúng bảng spec §4; không giao diện (A4), không P2, không giọng nói.
- **A10 ↔ D6:** đủ ba lớp đúng thứ tự spec (không multipart; `Sec-Fetch-Site` ≠ `same-origin` ⇒ 403, `Origin` khác gốc ⇒ 403, `Content-Type` ngoài 3 kiểu ⇒ 415; `Content-Length` thiếu / > 10 MB ⇒ 413 + đọc luồng có bộ đếm; không `UploadFile` / `Form`); T1 phủ cả `same-site`, `Origin` cùng host, tham số `charset`, `image/heic`.
- **§6 ↔ D7:** bom giải nén — `formats` cố định, đọc `size` trước `load()`, `MAX_IMAGE_PIXELS` + `DecompressionBombWarning` thành lỗi; EXIF — `exif_transpose` ⇒ `RGB` ⇒ `thumbnail(1024)` ⇒ JPEG không `exif`; không ghi đĩa. T3 dùng tham số nhỏ (đúng — máy 15 GB). Pillow có sẵn, không thư viện mới.
- **A4 ↔ D4:** enum id strict + `khong_nhan_ra`, backend kiểm lại; **Q-f ↔ D8:** phản hồi chỉ `ung_vien` + `khong_nhan_ra` (+ `loi` mã cố định); **Q-g ↔ D9:** log chỉ số đếm / USD / ms / outcome.
- **D3:** `_run` nhận `list[dict]` (`:314`) — đúng; dùng lại `responses_model`, `store=False`, `_run_config` (tracing) — đúng; gọi hàm "nội bộ" để không chạm file B đang sửa là đánh đổi có ghi; probe `input_image` 0 USD trước bước 0 + điều kiện dừng — đủ.
- **Tiền:** A1b ≈ 0,0003 USD, trần A1 0,005 / dừng 0,004 trong trần Phase 10 0,15 (spec §7); ghi USD từ `anh_metrics` ngay.
- **Đường ra:** OpenAI (spec §12 (1)), Commons (§12 (2)) — đúng mục User duyệt; D12 chỉ nhận giấy phép mở, phiếu nguồn đủ trường, ≤ 1 yêu cầu / giây, ảnh tải về để ở thư mục "không tin cậy", chỉ mở bằng Pillow có `formats`.

## 5. Giới hạn

- Không chạy code / probe (plan chưa code). m-1 suy từ đọc `app.py` [Code, chưa chạy]; m-2 dựa trên chú thích code + spec §7, chưa đo `reasoning_tokens` của lượt ảnh.
- Không mở bộ ảnh (chưa có) và không xét danh sách tên thật (chưa dựng).

## 6. Decision và bước tiếp

**changes_requested** — E sửa M-1 (+ minor), báo sha mới; C kiểm phần sửa; A duyệt sha. Việc kế của C theo A quyết (1): chọn 33 + 10 ảnh + tạo 3 ảnh chữ ra lệnh khi công cụ `tai_anh.py` của E chạy được.

## Vòng 2 — bản 2 `2fc2fcea33d4` (C187 · 10:50 05/11/2026 `date`)

Sha tính từ file = **`2fc2fcea33d4`**. Chỉ kiểm phần sửa theo vòng 1 (mục "Chỗ đổi bản 2" + các dòng D2, D3, D11, T8, T9, §1, §6, §7, §8).

| Finding | Sửa ở bản 2 | Kết luận |
|---|---|---|
| M-1 Q1 cờ tắt **và** bật | T9 (a) `capture_all.py` hai cờ ⇒ `cmp` giống byte `main` `b019aab` (228 / 228 mỗi bên); (b) 404 trên uvicorn thật; (c) pytest; §7 dừng khi khác byte | **đóng**. Ghi chú: giới hạn E ghi "(a) đi lõi chung, không qua route `/api`" thận trọng hơn mức cần — `capture_all.py` có 20 / 228 lượt đi qua `TestClient(create_app())` **có lifespan** (`capture_all.py:46–58`: 10 `api_chat` + 10 `api_chat_stream`) ⇒ với `anh.bat: true`, lifespan dựng `app.state.anh` + Agent ảnh **cũng được phủ**; không cần sửa |
| m-1 `include_router` trước `settings` | D2: luôn đăng ký, lifespan đặt `app.state.anh` khi `bat`, handler 404 khi `None` (không đọc thân); T8 / T9 trên `uvicorn api.app:app` | đóng |
| m-2 `max_tokens` | D3: 512; A1b ghi `reasoning_tokens` + đủ / bị cắt; §7 dừng khi bị cắt hoặc sai schema; §8 dòng trần | đóng |
| m-3 nguồn tên | D11 qua `scripts/grep_kb.sh … -m1 "^# "`, bỏ `*guides*` / `*inventory*`; 50 mục (giống byte bản đọc thẳng) | đóng |
| m-4 vai người dựng bộ | §1: C chọn 33 + 10, gắn nhãn, tạo 3 ảnh chữ ra lệnh; E tải phần đã thấy theo danh sách C đưa, ảnh kín C tự tải; A1b dùng ảnh thử **không thuộc bộ đo** | đóng |
| m-5 file tạm | T8 liệt kê `tempfile.gettempdir()` trước / sau 5 ca | đóng |
| m-6 W31 | §6 bước 4–5: hỏi A trước T8 / T9 / A1b / cổng | đóng |
| m-7 bảng rà | §8 thêm "trần + đường phục hồi" + "đầu ra có cấu trúc kiểm lại ở backend" | đóng |
| A quyết (1), (2) | §1 hai dòng | khớp |

Không thấy đổi ngoài phạm vi (D1, D4–D10, D12, T1–T7, tiền, trần giữ như bản 1).

**Decision vòng 2: ready_for_user_confirmation** — A duyệt sha `2fc2fcea33d4`.

