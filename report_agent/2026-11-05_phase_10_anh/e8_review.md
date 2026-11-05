# Review: Phase 10 A1 — hỏi bằng ảnh P1 v1 (nhánh `p10-anh` `0632e10`), một vòng cả nhánh

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 3 minor)
Người kiểm: C (Claude Code, Opus 5.5, `hue-rag-3c`) — việc **C198** (A giao tối 05/11)
Date: 20:03 05/11/2026 (`date`)
Implementation report: `report_agent/2026-11-05_phase_10_anh/e8_a1_implementation.md` (sha `b0cc8cdb4ba2` lúc đọc)
Căn cứ: spec Phase 10 bản 2 `bf67b90fb6fc` (A3, A9, A10, Q-f, Q-g, §6) · plan A1 bản 2 `2fc2fcea33d4` (D1–D10, T1–T9) — sha tính từ file, khớp tin giao.

## 1. Phạm vi đã review

- **Git:** `main..p10-anh` = 1 commit `0632e10`; gốc nhánh `268466d`; `git diff 268466d main -- backend frontend` **rỗng** ⇒ merge không cần rebase phần code. 9 file, chỉ `backend/` + `frontend/src/` (không `data/`, không kho); `git diff --check` sạch.
- **Đọc toàn bộ diff:** `llm/nhan_anh.py`, `api/routes/anh.py`, `api/app.py`, `config/settings.yaml` (`anh.bat: false`), `tests/test_p10_anh.py`, `tests/test_assistant_boundary.py`, `frontend/src/HoiBangAnh.jsx`, `App.jsx`, `index.css`; `generator._run` trên nhánh (chỗ bắt lỗi).
- Report người làm: đọc như chỉ mục bằng chứng, kể cả quyết định User giữ v1 dạng gợi ý có xác nhận (ghi rõ "âm theo tiêu chí gốc") và phần Playwright tối nay.
- **Không** mở bộ ảnh kín, không gọi API.

## 2. Findings

### m-1 — test rào thư viện mạng nới theo **gói**, không theo **tên**

- **Vị trí:** `backend/tests/test_assistant_boundary.py` `ALLOWED["llm.nhan_anh"] = {"agents"}`.
- **Yêu cầu:** T-3 "chỉ module được phép mới import thư viện gọi mạng, mỗi nhà cung cấp một module"; plan D3 "lần gọi model vẫn qua `generator._run`".
- **Bằng chứng [Chạy]:** `import_tree()` trên nhánh ⇒ `llm.nhan_anh` import `('agents', ['Agent', 'ModelSettings'])` — đúng như report nói, chỉ dựng agent. Nhưng `ALLOWED` cho **cả gói** `agents` ⇒ nếu sau này `nhan_anh` import `Runner` để gọi model thẳng (bỏ qua `_run`: hạn giờ, bắt lỗi ⇒ `GenerationError`, `call_log` / tiền), test vẫn qua.
- **Tác động:** rào yếu đi so với ý định; hôm nay code đúng.
- **Tiêu chí đóng:** thu hẹp theo tên — vd `ALLOWED_NAMES = {"llm.nhan_anh": {"agents": {"Agent", "ModelSettings"}}}` kiểm trong `test_only_allowed_modules_import_network_clients`, hoặc một test riêng `nhan_anh` chỉ import hai tên đó. Sửa lúc merge hoặc ở bậc sau — không chặn.

### m-2 — bảng §2–§3 của report người làm còn số của bản A1 cũ

- **Vị trí:** `e8_a1_implementation.md` §2 dòng `nhan_anh.py` ("`max_tokens` 512", "120 dòng"), dòng `settings.yaml` ("15 s"), §4 "36 passed".
- **Bằng chứng:** code trên nhánh `MAX_OUTPUT_TOKENS = 1024`, `timeout: 20`, `nhan_anh.py` 126 dòng; phần A2 / "Quyết định User" ở cuối report đã ghi 1024 / 20 s. Pytest C chạy: 80 passed / 1 error (mục 4).
- **Tác động:** người đọc phần đầu report hiểu sai cấu hình đang merge.
- **Tiêu chí đóng:** sửa 3 chỗ ở §2 / §4 cho khớp code (hoặc ghi "bản A1 trước A2" ngay cạnh).

### m-3 — đầu vào Phase 12 (không sửa trên nhánh này): rào gốc dựa vào `Host`, chưa giới hạn số lượt đồng thời

- **Vị trí:** `routes/anh.py` `kiem_dau_vao(…, f"{request.url.scheme}://{request.url.netloc}", …)`; plan D10 (đã ghi lệch spec §6 "một lượt ảnh / phiên").
- **Bằng chứng (đọc code, suy luận):** gốc so sánh lấy từ chính `Host` của yêu cầu ⇒ (a) trang lạ dùng DNS rebinding (tên miền trỏ về 127.0.0.1) có `Origin` = `Host` và `Sec-Fetch-Site: same-origin` ⇒ qua rào — chung cho cả `/api/chat`, không riêng nhánh này; (b) sau proxy TLS (AWS), `scheme` có thể là `http` trong khi `Origin` là `https` ⇒ chặn nhầm người dùng thật. Không giới hạn số yêu cầu ảnh song song: mỗi ảnh 40 MP giải mã ≈ 120 MB RGB (cộng bản xoay / chuyển màu) ⇒ vài yêu cầu cùng lúc tốn vài trăm MB – vài GB.
- **Tác động:** trên máy User một người dùng — thấp. Khi deploy — cần làm.
- **Tiêu chí đóng:** A ghi vào danh sách đầu vào Phase 12 (spec deploy): danh sách `Host` / gốc cố định (vd `TrustedHostMiddleware` + gốc từ cấu hình), xử lý `X-Forwarded-Proto`, và trần đồng thời cho route ảnh (semaphore hoặc theo IP) như D10 đã ghi.

**Không có finding ở:**
- Cờ tắt ⇒ 404, không đọc thân, giao diện không hiện nút.
- Rào A10 đúng thứ tự trước khi đọc thân. Bộ đếm luồng đúng.
- `chuan_bi_anh`: chặn ảnh khổng lồ trước khi giải mã, xoá EXIF, không ghi đĩa.
- Đầu ra enum strict + backend kiểm lại (Q-f: route không có chữ tự do).
- Chữ trong ảnh không lái được gì ngoài chọn id trong danh sách, và người dùng còn phải bấm xác nhận.
- `anh_metrics` có danh sách trường cố định, không chứa ảnh / tên file / id / tên (Q-g).
- Câu ghép A3 do code dựng từ tên chuẩn của server; câu A9 cố định.
- CSP chỉ thêm `img-src blob:` (spec A7, User duyệt).
- Mọi lỗi của `_run` ⇒ `GenerationError` ⇒ 200 `khong_doan_duoc`, không thử lại.
- Độ phức tạp tương xứng: một module xử lý, một route, không wrapper / retry / cấu hình thừa.

## 3. Cách người kiểm chạy lại thật

Worktree riêng `/tmp/c198` (detached `0632e10`, symlink `data/`, `knowledge-base-hue/`); chỉ mục **mới** sau C192 (8.435 point). Tất cả 0 USD.

```bash
cd /tmp/c198/backend && env -u OPENAI_API_KEY HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest \
  tests/test_p10_anh.py tests/test_assistant_boundary.py tests/test_api_chat.py tests/test_assistant.py tests/test_chat_stream.py tests/test_feedback.py -q
# Q1 cờ tắt: capture_all trên main (working tree chung) và trên nhánh, cùng chỉ mục, rồi cmp
for T in /home/minhhieu/hue_rag /tmp/c198; do cd $T/backend && env -u OPENAI_API_KEY OPENAI_API_KEY=capture-only HF_HUB_OFFLINE=1 PYTHONPATH=$PWD \
  uv run --project /home/minhhieu/hue_rag python /home/minhhieu/hue_rag/data/phase_9/b2_chay/tools/capture_all.py /tmp/c198_probe/cap_$(basename $T).jsonl; done
cmp /tmp/c198_probe/cap_hue_rag.jsonl /tmp/c198_probe/cap_c198.jsonl
# probe 0 USD: chuan_bi_anh với 11 ảnh hỏng tự tạo; doc_than với luồng giả 11 MB (khai thấp) — /tmp/c198_probe/probe*.py
# import_tree() của test rào: các import mạng của llm.nhan_anh / api.routes.anh
```

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| pytest 6 file (không khoá) | **80 passed, 1 error** — error là `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan` (cần khoá OpenAI — giống `main`, bẫy đã biết) |
| **Q1 cờ tắt** | `capture_all` 228 / 228 mỗi bên, `cmp` **giống byte** `main` (trên chỉ mục mới) — **PASS** |
| `chuan_bi_anh` 11 ảnh hỏng / lạ | JPEG cắt đôi / chỉ phần đầu, WEBP cắt, rỗng, chỉ chữ ký PNG ⇒ **415**; PNG khai 60.000 × 60.000 ⇒ **413** (trước giải mã); PNG RGBA / bảng màu / 16 bit, JPEG CMYK, PNG thiếu dữ liệu ⇒ ra JPEG hợp lệ; **0 ngoại lệ khác** (không 500) — **PASS** |
| `doc_than` | 11 × 1 MB ⇒ dừng (None) · đúng 10 MB ⇒ nhận đủ · một khối 11 MB ⇒ dừng — **PASS** |
| `generator._run` | `TimeoutError`, lỗi SDK / OpenAI, mọi `Exception` ⇒ `GenerationError` ⇒ route trả 200 `khong_doan_duoc` — **PASS** (đọc code) |
| Rào thư viện mạng | `llm.nhan_anh` chỉ import `Agent`, `ModelSettings`; `api.routes.anh` không import gói mạng — đúng; rào nới theo gói (m-1) |
| Server thật T8 / Playwright | **Không chạy lại** — dùng bằng chứng của E (T8 7 ca, Playwright 2 lượt có phí); phần rào đã kiểm lại bằng test + probe ở trên. Lý do: cùng commit `0632e10`, rủi ro chính (rào, cờ tắt) đã chạy lại 0 USD |

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy server thật / Playwright, không lượt có phí (chất lượng P1 đã đo ở A2; User đổi thước có ghi).
- Câu ghép A3 nhánh "có chữ gõ kèm" chưa có test tự động (Playwright đi nhánh "Giới thiệu về …"); hàm `cauGhep` đơn giản, đọc code đúng spec (cắt phần chữ người dùng khi > 500).
- Giao diện ở khổ điện thoại chưa thử (E đã nêu) — User xem khi duyệt.

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation`. A merge được (cờ `anh.bat: false` ⇒ hành vi người dùng không đổi). m-1, m-2 sửa lúc merge hoặc bậc sau; m-3 ghi vào đầu vào Phase 12. Worktree `/tmp/c198` + `/tmp/c198_probe` gỡ được sau khi A xong.
