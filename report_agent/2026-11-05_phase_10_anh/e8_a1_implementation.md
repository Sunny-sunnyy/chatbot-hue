# Implementation Report: Phase 10 A0 + A1 + A1b — danh sách tên, công cụ tải ảnh, route `POST /api/anh/ung_vien`, bước 0

Người làm: E (Claude Opus 5.5, `hue-rag-7a`) · việc **E8** (A giao)
Date: 11:16 05/11/2026 (`date`)
Plan: `docs/superpowers/plans/2026-11-05-phase-10-a1-plan.md` bản 2 **`2fc2fcea33d4`** (A duyệt; review C vòng 2 ready `bf48ae1e2620`). Spec: `docs/superpowers/specs/2026-11-05-phase-10-design.md` bản 2 `bf67b90fb6fc` (User duyệt §12 (1)–(4)).
Nhánh: `p10-anh` từ `main` `b019aab`, worktree `/tmp/e_anh`. **Đã commit + push `0632e10`** (19:50 05/11/2026, phiên tối — E10: dựng lại worktree từ `268466d` + patch `9138ca6b1fc3`, 9 file +542 / −2, 40 test passed). Trước đó chưa commit vì auto mode chặn. Cờ `anh.bat: false`.

## 1. Phạm vi

A0a danh sách tên · A0b công cụ tải ảnh · A1 route + rào A10 + xử lý ảnh + một lần gọi model đầu ra enum + log · A1b bước 0 (một lần gọi thật). **Không:** giao diện (A4), lượt đo P1 (A2), P2 SigLIP, giọng nói.
Repo public: report không chép kho / bộ đo; tên món trong ví dụ là tên công khai.

## 2. Thay đổi chính

| File | Thay đổi |
|---|---|
| `backend/llm/nhan_anh.py` (mới, 126 dòng — bản merge, sau A2) | `chuan_bi_anh` (Pillow `formats` cố định, chặn `w*h > max_pixels` **trước** `load()`, `exif_transpose` ⇒ RGB ⇒ `thumbnail(1024)` ⇒ JPEG **không EXIF**, không ghi đĩa) · `nap_danh_sach` (id / khoá tên trùng ⇒ lỗi) · `kieu_dau_ra` (Pydantic `Literal[<42 id>]`, ≤ 3, `extra="forbid"`) · `NHAN_ANH_INSTRUCTIONS` · `dau_vao` (danh sách chữ + ảnh data URL) · `kiem_lai` (id ∈ danh sách, bỏ trùng, `khong_nhan_ra` ⇒ rỗng) · `tao_agent` / `doan_ten` (một `Agent` dùng `generator.responses_model`, `max_tokens` **1024** (A1 512 ⇒ đổi sau A2 vì lỗi cắt), `store=False`; gọi qua `generator._run`) |
| `backend/api/routes/anh.py` (mới, 108 dòng) | `kiem_dau_vao` (hàm thuần: `Sec-Fetch-Site` ≠ same-origin ⇒ 403 · `Origin` khác gốc ⇒ 403 · `Content-Type` ∉ jpeg/png/webp ⇒ 415 · `Content-Length` thiếu / sai / > 10 MB ⇒ 413) · `doc_than` (đọc `request.stream()` có bộ đếm, không `UploadFile`) · route: cờ tắt ⇒ 404; lỗi model ⇒ 200 `khong_doan_duoc`, không thử lại · một dòng `anh_metrics` / yêu cầu (chỉ số đếm / mã / ms / USD) |
| `backend/api/app.py` (+19 / −1) | luôn `include_router(anh_router)`; lifespan đặt `app.state.anh` khi `anh.bat` + có generator (nạp danh sách, `Image.MAX_IMAGE_PIXELS`), không thì `None` |
| `backend/config/settings.yaml` (+10) | khối `anh:` (`bat: false`, đường danh sách, 10 MB, 40 MP, 1024, **20 s** — A1 15 s, đổi sau A2) |
| `backend/tests/test_p10_anh.py` (mới, 165 dòng) | T1–T7 + test mức route |
| `backend/tests/test_assistant_boundary.py` (+2) | **`ALLOWED` thêm `"llm.nhan_anh": {"agents"}`** — test rào "chỉ module được phép import thư viện mạng" hỏng khi thêm `nhan_anh` (import `Agent`, `ModelSettings`); docstring test ghi "thêm module ⇒ sửa `ALLOWED` có chủ đích"; `nhan_anh` chỉ **dựng** agent, lần gọi mạng qua client của generator. **Người kiểm xem kỹ dòng này** |
| `data/phase_10/anh/tools/dung_danh_sach.py` (private) | dựng `danh_sach_ten.json` + `ca_trung.md` qua `scripts/grep_kb.sh`; áp `duyet_user.json` (quyết định User) |
| `data/phase_10/anh/tools/tai_anh.py` (private) | tải ảnh: mỗi dòng URL `https` hoặc tên file Commons; chặn scheme khác (`file:`), ≤ 15 MB, Pillow `formats` cố định; phiếu `phieu_nguon.jsonl` (URL + sha256) |

**Lệch plan (có lý do, A đã đồng ý):**
- **D7:** bỏ `warnings.catch_warnings` + `simplefilter("error", DecompressionBombWarning)` — `chuan_bi_anh` chạy trong `asyncio.to_thread`, bộ lọc cảnh báo là trạng thái chung (không an toàn đa luồng); kiểm `w*h > max_pixels` trước khi giải mã chặn cùng ngưỡng; `MAX_IMAGE_PIXELS` toàn cục = lớp sau (Pillow lỗi ở 2×).
- **D12 + spec §3.2 "chỉ giấy phép mở":** **bỏ theo User 05/11** (A báo) — ảnh công khai dùng cho đồ án học tập; `tai_anh.py` không lọc giấy phép, chỉ ghi URL nguồn (bản đầu có lọc + phiếu tác giả / giấy phép — đã gỡ).
- **D11:** danh sách sau User duyệt = **42 mục** (28 điểm · 9 món · 5 di sản), sha `9e9ed63ecbdb`; quyết định ở `data/phase_10/anh/duyet_user.json`.

## 3. Cách đã chạy thật

```bash
# T1–T7 + route + file chat (không khoá OpenAI ⇒ không thể có lời gọi trả phí)
cd /tmp/e_anh/backend && env -u OPENAI_API_KEY HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest \
  tests/test_api_chat.py tests/test_assistant.py tests/test_assistant_boundary.py tests/test_chat_stream.py tests/test_feedback.py tests/test_static_ui.py tests/test_p10_anh.py -q
# T8: uvicorn api.app:app (create_app() không tham số), cờ bật, TMPDIR riêng /tmp/e8_tmpdir, cổng 8871; curl 7 ca; đọc log sau mốc dòng
# T9 (b): uvicorn cờ tắt, cổng 8872: POST ảnh, /, /health
# T9 (a): data/phase_9/b2_chay/tools/capture_all.py trên main (ea114ae — backend giống b019aab, `git diff --stat` rỗng), nhánh cờ tắt, nhánh cờ bật; cmp
# A1b: uvicorn cờ bật cổng 8873 + --env-file; 1 POST ảnh thử data/phase_10/anh/thu_tai/khong_tin_cay/001_… (không thuộc bộ đo)
```
Worktree nối `data/`, `knowledge-base-hue/`, `frontend/dist` bằng symlink (untracked, không commit). Cờ bật tạm trong `settings.yaml` lúc chạy, trả về `false` sau mỗi lượt (đã kiểm `grep`).

## 4. Kết quả quan sát

| Tiêu chí | Kết quả |
|---|---|
| **T1–T7 + route** | `test_p10_anh.py` **36 passed** ở A1 (bản merge `0632e10`: cùng boundary **40 passed**; C198 chạy 7 file 80 passed / 1 error cần khoá) (T1 21 ca rào; T2 EXIF GPS + Orientation xoá, xoay đúng; T3 1200×1000 với ngưỡng 1 MP ⇒ 413 trước `load()`; T4 GIF / BMP / rác / rỗng ⇒ 415; T5 4032×3024 ⇒ 1024×768; T6 enum strict + kiểm lại; T7 trùng id / khoá ⇒ lỗi + danh sách thật nạp được; route: tắt ⇒ 404, 403 / 403 / 415 multipart / 413 trước bước cần generator, ảnh hợp lệ ⇒ 503 khi chưa có generator) — **PASS** |
| **T9 (c)** pytest 7 file | **83 passed, 1 error** — lỗi là `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan` (cần khoá; **giống `main`**: main 47 passed / 1 error cùng test). Lần đầu nhánh có thêm 1 failed `test_only_allowed_modules_import_network_clients` ⇒ sửa `ALLOWED` (mục 2) ⇒ hết — **PASS** |
| **T8** (server thật, cờ bật) | 7 ca: cross-site 403 · Origin lạ 403 · multipart 415 · multipart 11 MB 415 · chunked thiếu `Content-Length` 413 · thân **11 MB** 413 · `text/plain` cùng gốc 415; mỗi ca **≈ 1 ms**, đúng 1 dòng `anh_metrics` **`n_llm_calls: 0`**, `bytes_vao: null` (không đọc thân); **RSS chênh 0 kB**; **0 file tạm mới** (so `find` cây `TMPDIR` riêng trước / sau) — **PASS** |
| **T9 (b)** cờ tắt | `POST /api/anh/ung_vien` **404** (`anh_metrics` `outcome: tat`, 0 lần gọi), `/` 200, `/health` 5 / 5 ready, không nạp danh sách — **PASS** |
| **T9 (a)** Q1 | `capture_all` 228 / 228 mỗi lượt (208 `answer_case` + 10 `/api/chat` + 10 `/api/chat/stream`): **cờ tắt giống byte `main`**, **cờ bật giống byte `main`** (`cmp`). Lượt cờ bật có dòng "Image route enabled (42 names)" ⇒ lifespan + `app.state.anh` được phủ (đúng ghi chú review C vòng 2) — **PASS** |
| **A1b** bước 0 (có phí) | 1 lần gọi: ảnh 1920×1440 ⇒ 1024×768; **`input_tokens` 2.334** · `output_tokens` 185 (**`reasoning_tokens` 156**) — **không bị cắt** (trần 512), đầu ra đúng schema; trả `bun_bo_hue` (ảnh nồi bún bò — đúng); **0,00038418 USD**; `ms_xu_ly` 69 · `ms_model` 4.471 · `ms_tong` 4.541 (curl ghi 4,22 s — xem §5). Đếm token chữ bằng tokenizer máy (0 USD): lời dặn 165 + danh sách 914 + schema ≈ 400 ⇒ **phần ảnh ≈ 855** ↔ ước spec §7 **922** (giả định như `gpt-5.6-luna`) — trong 2× ⇒ giữ ước tiền A2 |
| Cổng (log) | log sau lượt có ảnh: 0 dòng chứa tên file / id / tên món |

**Tiền A1:** 0,00038418 USD (một lần gọi) — trong trần A1 0,005 / dừng 0,004; trần Phase 10 0,15. `capture_all`, pytest, T8: 0 USD.

## 5. Lỗi và giới hạn

- **Chưa commit / push** (auto mode — cần User đồng ý; xem đầu file).
- Bước 0 là **một** mẫu: độ trễ 4,5 s (mục tiêu báo cáo p95 ≤ 5 s — Q-h theo dõi), chất lượng **chưa đo** (A2). Phía server ghi 4,54 s mà curl ghi 4,22 s — server lớn hơn client là bất thường, **chưa rõ nguyên nhân** (một mẫu); A2 đo cả hai phía.
- Token ảnh tách bằng cách trừ ước token chữ (schema ước bằng JSON schema Pydantic — không phải chuỗi OpenAI dựng thật) ⇒ "≈ 855" là ước.
- `test_startup_model_missing.py` không chạy (cần `HF_HOME` rỗng — bẫy auto mode đã biết); không nằm trong vùng chạm.
- Lời gọi model dùng `generator._run` (hàm "nội bộ") — đánh đổi có ghi ở plan D3 để không chạm file Phase 9 đang sửa.
- Symlink `data/`, `knowledge-base-hue/`, `frontend/dist` trong worktree — gỡ khi đóng việc.
- Probe 0 USD cho `input_image` (plan D3) không chạy riêng — bước 0 xác nhận thật SDK 0.19.4 nhận `input_image` qua `_run`.

## 6. Bàn giao cho người kiểm

- Đọc diff: `git -C /tmp/e_anh diff --cached` (6 file) — chú ý `test_assistant_boundary.py` (`ALLOWED`) và thứ tự rào trong `routes/anh.py`.
- Chạy lại rẻ nhất: pytest lệnh §3 (≈ 50 s, 0 USD); T8 nếu muốn (server thật, 0 USD).
- Bộ ảnh đã thấy C dựng: `data/phase_10/bo_do_anh/da_thay/` (33 ảnh + nhãn) — dùng ở **A2** (chưa chạy). Bộ kín `bo_do_anh_sealed/` — E không mở.
- **Giải thích ngắn:** thêm một đường "gửi ảnh ⇒ 2–3 tên để bấm" đứng riêng cạnh chatbot, đang tắt; rào chặn trang lạ / ảnh quá to / ảnh hỏng chạy trước khi đọc ảnh hay gọi model; khi tắt hay bật, chatbot hỏi đáp gửi model đúng từng byte như cũ; thử thật một ảnh tốn 0,0004 USD và nhận đúng món.

---

# A2 — lượt đo P1 (`gpt-6-luna`) trên bộ ảnh ĐÃ THẤY (11:36 05/11/2026)

**Kết luận: KẾT QUẢ ÂM theo tiêu chí ghi trước** (spec Phase 10 bản 2 §5 "Kết quả âm": Q-a hoặc Q-c phạm sau 2 vòng chỉnh ⇒ cờ `anh` tắt, xét P2). Cờ đang tắt; chưa tag `hoso/p10-anh` (chờ A / User).
Luật dùng (A giao theo luật cắt giảm User duyệt): spec §5 **bỏ Q-k (bộ kín)**; 2 lượt cùng cấu hình, đạt ⇔ **cả hai lượt**; chỉnh lời dặn chỉ trên bộ đã thấy, ≤ 2 vòng. Bộ: C dựng `data/phase_10/bo_do_anh/da_thay/` (`nhan.jsonl` md5 `1f37c7f11821` — khớp README C), 25 trong danh sách + 5 ngoài + 3 chữ ra lệnh. Bộ kín **không mở**.
Cách đo: `data/phase_10/anh/tools/do_a2.py` gửi 33 ảnh **tuần tự qua route thật** (uvicorn worktree, cờ bật tạm), đọc USD / token từ `anh_metrics`; chấm theo luật nhãn README của C (tên đúng = `id` hoặc `chap_nhan` trong ≤ 3; ngoài danh sách đúng khi rỗng / `khong_nhan_ra`). Kết quả thô: `data/phase_10/anh/a2/v{0,1,2}_luot{1,2}.jsonl` (private).

| Vòng | Đổi | Q-a ≥ 22/25 (+ từng loại) | Q-c bị ép ≤ 1/5 | Q-d theo lệnh ≤ 1/3 | Q-b top-1 | Q-e đổi giữa 2 lượt | lỗi cắt | p50 / p95 ms (client) | USD 2 lượt |
|---|---|---|---|---|---|---|---|---|---|
| v0 | lời dặn plan; `max_tokens` 512, timeout 15 | 21 · 21 ✗ | 0 · 0 ✓ | 1 · 1 ✓ | 21 · 21 | 4/33 | **1 · 3** | 3.363 / 6.414 · 2.978 / 7.114 | 0,024055 |
| v1 | `max_tokens` 1024 + timeout 20 (sửa lỗi cắt) **+** lời dặn: đưa thêm 1–2 tên dễ nhầm; chữ dán trên ảnh không được quyết định | **22 · 22 ✓** (loại đều đạt) | 0 · **2** ✗ | 1 · 1 ✓ | 21 · 21 | **6/33** (> 5) | 0 · 0 | 2.959 / 7.688 · 3.173 / 6.780 | 0,026456 |
| v2 | + "chỉ đưa id khi có dấu hiệu riêng; giống chung kiểu ⇒ không nhận ra" | 21 · 20 ✗ (cảnh 2/4 lượt 2 ✗) | **0 · 0 ✓** | 1 · 1 ✓ | 20 · 20 | **7/33** (> 5) | 1 · 0 | 3.221 / 9.077 · 3.071 / 6.266 | 0,027650 |

**Quan sát (đã chứng minh từ dữ liệu lượt đo):**
- **Lỗi cắt** v0: cả 4 lần `khong_doan_duoc` có `output_tokens` = 512, `reasoning_tokens` 489–512 ⇒ suy luận ăn hết trần ⇒ đầu ra hỏng. Lỗi này còn làm số đo **lạc quan**: 1 ảnh ngoài danh sách bị lỗi được chấm là "không nhận ra" đúng. 1024 hết cắt ở v1, v2 còn 1 lần chạm đúng 1024.
- **Đánh đổi Q-a ↔ Q-c trên cùng bộ:** cho model đưa thêm tên (v1) ⇒ Q-a đạt nhưng ép tên Huế cho Ngọ Môn Bắc Kinh (⇒ `dai_noi`) và tô phở Hà Nội (⇒ `bun_bo_hue`) ở lượt 2; siết lại (v2) ⇒ Q-c đạt nhưng chợ Đông Ba, biển Thuận An thành "không nhận ra" và Q-a tụt.
- **Sai lặp lại cả 3 vòng / 6 lượt:** điện Hòn Chén (⇒ các lăng), lăng Gia Long (⇒ lăng Hiệp Hòa ở 5 / 6 lượt), bánh canh Nam Phổ (⇒ chè heo quay ở 5 / 6), **ảnh chữ ra lệnh L2** (bảng tiếng Anh dán lên ảnh lăng Minh Mạng ⇒ `dai_noi` ở **6 / 6 lượt** — lời dặn "bỏ qua chữ dán thêm" ở v1, v2 không có tác dụng với ca này). Q-d vẫn trong sàn (≤ 1/3) vì L1, L3 không theo lệnh.
- **Nhiễu A/A lớn:** 4–7 / 33 ảnh đổi tập ứng viên giữa hai lượt cùng cấu hình (v1, v2 vượt mức "> 5 ⇒ báo"). Với luật "đạt cả hai lượt", kết quả sát ngưỡng (22 / 25, 1 / 5) quyết bằng nhiễu.
- Độ trễ: p50 ≈ 3,0–3,4 s, p95 6,3–9,1 s (mục tiêu báo cáo p95 ≤ 5 s — Q-h theo dõi, **không đạt**). Tiền ≈ **0,0004 USD / ảnh**.

**Giả thuyết (chưa chứng minh):** (1) lỗi gốc là nhận dạng — các lăng / điện Huế giống nhau và món địa phương ít dữ liệu; chỉnh lời dặn chỉ dời lỗi giữa Q-a và Q-c; (2) chữ trên bảng in kiểu "biển chính thức" (L2) khó tách khỏi biển tên thật mà lời dặn cho dùng.

**Tiền Phase 10:** bước 0 0,000384 + A2 0,078161 = **0,078545 USD** / trần 0,15 (dừng 0,13). 3 vòng × 2 lượt × 33 ảnh = 198 lần gọi.
**Trạng thái code:** lời dặn **v2** + `max_tokens` 1024 + timeout 20 trong working tree `/tmp/e_anh` (chưa staged lại; bản staged là A1). Cờ `bat: false`. pytest `test_p10_anh.py` + boundary 40 passed.

**Hướng tiếp (chờ A / User — không tự làm):** (a) P2 SigLIP 2 chạy máy (spec A6 — **User chưa duyệt** tải ~1,6 GB); (b) giữ P1 làm "gợi ý" nhưng giao diện **luôn kèm ô gõ tên / chọn danh sách (M0)** — vẫn phạm sàn đã ghi, cần User quyết đổi tiêu chí (không áp ở bản này); (c) dừng tính năng ảnh, ghi kết quả âm vào báo cáo (spec "phương án B" cuối: giữ M0). Thử thêm `reasoning` thấp / `detail` khác = thí nghiệm mới, cần tiêu chí + bộ mới (bộ này đã chỉnh 2 vòng).

**Quyết định User sau A2 (A chuyển, E ghi 16:49 05/11/2026):** **giữ P1 bản v1 dạng GỢI Ý có xác nhận** — nhãn "Gợi ý từ ảnh, có thể sai — chọn đúng tên", luôn có "Không phải các tên này" + ô gõ tên,
trợ lý chỉ trả lời sau khi người dùng bấm. **Ghi trung thực:** P1 **âm theo tiêu chí gốc** (spec §5); User **đổi thước** vì có bước xác nhận (lỗi nhận sai không thành câu trả lời sai).
Code đã đưa lời dặn về v1 (`max_tokens` 1024, timeout 20). Song song: thí nghiệm P2 SigLIP 2 (E9, tiêu chí ghi trước `data/phase_10/anh/e9/tieu_chi_ghi_truoc.md`) — chưa chạy.

---

# Giao diện P1 v1 — Playwright trên server thật (19:50 05/11/2026)

**Kết luận: ĐẠT mọi kiểm đã ghi** (A giao E10; 2 lượt đường đầy đủ A duyệt ≈ 0,003 USD).
Cách chạy: nhánh `p10-anh` `0632e10`, worktree `/tmp/e_anh`, `npm ci && npm run build` trong worktree, uvicorn thật cổng 8841 (chỉ mục mới sau C192), **không chặn / giả mạng**;
script `data/phase_10/anh/a1_playwright/ui_p1.py` (Chromium headless, 1280×900), kết quả + ảnh chụp `data/phase_10/anh/a1_playwright/ket_qua/` (private). Cờ `anh.bat` bật **tạm** trong worktree rồi trả về `false` (không commit).

| Kiểm | Kết quả |
|---|---|
| Cờ tắt | `GET /api/anh/ung_vien` 404 · **0 nút** "Hỏi bằng ảnh" · 0 vi phạm CSP · 0 request ra ngoài — **PASS** |
| Cờ bật, 0 USD | có nút + dòng báo "Ảnh được gửi tới OpenAI…" · file GIF ⇒ "Chọn ảnh JPEG, PNG hoặc WEBP." · file > 10 MB ⇒ báo lỗi · **0 POST** tới server cho hai ca này — **PASS** |
| Lượt có phí 1 — ảnh công trình trong danh sách (bộ đã thấy) | xem trước `blob:` hiện được (CSP `img-src 'self' blob:` không chặn) · nhãn "Gợi ý từ ảnh, có thể sai" · 1 tên gợi ý (đúng chủ thể) + nút "Không phải các tên này — tôi gõ tên" · **0 câu gửi chatbot trước khi bấm** · bấm tên ⇒ câu ghép "Giới thiệu về <tên>" (spec A3) ⇒ `/api/chat/stream` ⇒ có câu trả lời, 7 nguồn; thẻ ảnh đóng — **PASS** |
| Lượt có phí 2 — ảnh ngoài danh sách (con mèo) | "Mình chưa nhận ra ảnh này…" · 0 tên · bấm "Gõ tên" ⇒ con trỏ về ô gõ câu hỏi · **không gửi câu nào tới chatbot** — **PASS** |
| Toàn lượt | 0 vi phạm CSP · 0 request ra ngoài gốc · 2 POST ảnh · 1 lượt chat |

**Tiền thật (log `anh_metrics` / `chat_metrics` worktree):** ảnh 0,00042005 + 0,00031405 · chat 0,000540875 · **cộng một lần gọi ảnh thừa 0,00035855** (lần chạy đầu script hỏng ở bước chờ — xem dưới) ⇒ **0,001634 USD**. **Tiền Phase 10: 0,078545 + 0,001634 = 0,080179 USD** / trần 0,15 (dừng 0,13). Độ trễ model ảnh 5,2–5,9 s / lần (một mẫu mỗi loại; p95 mục tiêu ≤ 5 s — vẫn không đạt như A2).

**Lỗi / giới hạn:**
- Lần chạy đầu: `page.wait_for_function` bị **CSP của trang chặn** (`script-src 'self'`, không `unsafe-eval`) — rào đúng, lỗi ở script đo ⇒ đổi sang chờ bằng locator; ảnh đã gửi một lần (tiền tính ở trên).
- Quan sát giao diện (ảnh chụp, chưa sửa): thẻ ảnh (xem trước + nút) cao ~330 px ở khung 1280×900, phần câu trả lời phía trên co lại còn ít dòng. **Chưa thử khung điện thoại** — reviewer / User xem có cần thu nhỏ xem trước không.
- Một ảnh mỗi loại — đây là kiểm luồng giao diện, không phải đo chất lượng (chất lượng: A2).
