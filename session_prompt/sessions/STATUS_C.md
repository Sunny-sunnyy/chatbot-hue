# STATUS C — kết phiên 08/11 (viết lại 12:17, bổ sung 12:50 08/11/2026 — `date`). Lịch sử: `git log -p session_prompt/sessions/STATUS_C.md`

## PHIÊN 09/11 (mở 20:10 09/11/2026) — C `hue-rag-6a` · A `hue-rag-87` · B `hue-rag-99` · E `hue-rag-ea`
**A giao (20:13 09/11/2026, User: việc A giao = "làm đi"), 0 USD:**
(1) dựng lại `/tmp/c_t3` từ `p9-t3-bang` `21ec06d`, rebase lên `main` `5c982a0`, chạy test file bị chạm (chưa đo). Khai báo sửa: nhánh `p9-t3-bang` (5 file của nhánh, chỉ giải xung đột rebase), push nhánh.
(2) review plan T2 `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` (`921f75d64a7c`) ⇒ file mới `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan_review.md`.
**(1) XONG:** `p9-t3-bang` rebase lên `main` `5c982a0` = **`0eeb6f9`** (pushed): giữ cả T1 + T3, `max_turns_for(ngay_lich, ve_gio, thoi_tiet)` cộng dồn + 1 test. Test file chạm 460 đạt; cả `backend/tests` 885 đạt / 8 hỏng-lỗi đã biết (5 cần khoá, 2 cần bản build UI), 3 phút 43 giây.
**(2) XONG:** review T2 `changes_requested` 0 blocker · 3 major (max_turns · sàn S2c/S5/S6/S1×2 · bộ hỏi kèm 10) — sha `2653316dd16a` (untracked, A commit). Đã nhắn B + A.
**(3) T3 ĐÓNG HỒ SƠ (20:50 09/11/2026, User chọn, A báo):** không merge; nhánh `p9-t3-bang` = `e547b9e` (pushed) — A gắn tag `hoso/p9-t3-bang` + xoá nhánh khi User duyệt. Kết luận report §13. Worktree `/tmp/c_t3` (cờ `false`) — gỡ: `rm /tmp/c_t3/data /tmp/c_t3/knowledge-base-hue && git worktree remove /tmp/c_t3` (User `!` nếu `rm` bị chặn). Câu kín b_kin_07: A bỏ (User đã chạy lệnh 1: câu thuộc loại pháp lý chung, nhãn ngoài phạm vi chắc; chưa ghi `kin_c_doc.md` vì A bỏ việc). Tiền T3 09/11 0,027667.
**(4) ĐANG LÀM (20:50 09/11/2026, A giao):** sửa plan T2 theo 3 major C ghi + chốt tự soi (sàn S1 + ngoài kho / ngoài phạm vi + đúng câu; S5 / S6 đo chung lúc đóng đợt; không bộ kín). Khai báo sửa: `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` (C cầm thay B). ≤ 0,2 USD ⇒ mức nhẹ, A đọc duyệt. Code chờ G vào `main`. **Bản 2 XONG — sha `88b1f0586e99`, chờ A duyệt** (≈ 0,17 USD); bộ hỏi kèm 10 nhờ E viết (`data/phase_9/t2_web/hoi_kem_10.jsonl`, md5 ghi vào plan §3 trước lượt có phí).
**(5) XONG — chờ review (21:01 09/11/2026; giao lúc 20:55 09/11/2026, A giao, 0 USD, mức nhẹ) — 4 chốt trước deploy, nhánh `p12-chot-deploy` từ `main` `2db09b8`, worktree `/tmp/c_dep`.** Plan ½ trang:
- **Mặc định = hành vi hiện tại** (không đặt biến môi trường ⇒ không đổi gì; chuỗi gửi model không chạm).
- (1) Log: `config/logging.yaml` handler `file` ⇒ `logging.handlers.RotatingFileHandler` 10 MB × 3 bản (luôn bật; dưới 10 MB y như cũ — log máy User ~0,6 MB).
- (2) Cookie: `HUE_COOKIE_SECURE=1` ⇒ cookie `conversation_id` có `Secure` (đọc mỗi lần đặt cookie, `api/routes/chat.py` `_set_cookie`); không đặt ⇒ `secure=False` như cũ.
- (3) Tài liệu API: `HUE_TAT_DOCS=1` ⇒ `FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` (`api/app.py`); không đặt ⇒ như cũ.
- (4) Giới hạn lượt: `HUE_LUOT_MOI_NGAY=<n>` (> 0) ⇒ đếm lượt POST `/api/chat`, `/api/chat/stream`, `/api/anh/ung_vien` theo IP (`request.client.host`) theo ngày giờ Việt Nam, trong RAM; vượt ⇒ 429 JSON `{error: {code: "rate_limited", message}}` (giao diện hiện `error.message`, không sửa giao diện); log 1 dòng cảnh báo không ghi IP. Không đặt / 0 ⇒ tắt. Sau proxy (Caddy): uvicorn phải chạy `--proxy-headers --forwarded-allow-ips <ip proxy>` để `client.host` là IP thật — ghi vào checklist deploy, không tự đọc `X-Forwarded-For` (giả mạo được).
- Khai báo sửa: `backend/config/logging.yaml`, `backend/api/app.py`, `backend/api/routes/chat.py`, `backend/api/gioi_han.py` (mới), `backend/tests/test_chot_deploy.py` (mới).
- Kiểm: test file mới + file chạm (`test_api_chat.py` không khoá, `test_static_ui.py`); 1 lần server thật bật cả 4 biến (`/docs` 404, cookie `Secure`, lượt thứ n+1 ⇒ 429) + 1 lần không biến (như cũ). 0 USD (dùng câu ngoài phạm vi / lượt bị chặn trước model — vẫn có 1–2 câu thật ≈ 0,001).
- **Kết quả:** nhánh `p12-chot-deploy` = **`a3db152`** (pushed). Test mới `test_chot_deploy.py` 5 đạt; file chạm (`test_api_chat` · `test_feedback` · `test_cong_dot_1`) 40 đạt / 1 lỗi = test cần khoá (đã biết). Server thật cổng 8897: **bật 3 biến** (`HUE_TAT_DOCS=1 HUE_COOKIE_SECURE=1 HUE_LUOT_MOI_NGAY=2`) ⇒ `/docs` 404 · `/openapi.json` 404 · cookie có `Secure` · lượt 1–2 200, lượt 3 `/api/chat` 429 + lời báo, `/api/chat/stream` 429 · log 2 dòng `chat_metrics` + 2 dòng "Rate limited", 0 lần chứa IP; **không biến** ⇒ `/docs` 200, cookie không `Secure`, không 429. Log xoay vòng nạp được (server khởi động bình thường). Tiền ≈ 0,00035 USD (4 câu ngoài phạm vi). Bỏ test cấu hình log (dictConfig trong test đổi logging toàn cục ⇒ hỏng test đếm dòng log).
- **Checklist deploy (cho A):** sau Caddy phải chạy uvicorn `--proxy-headers --forwarded-allow-ips <ip Caddy>` (không thì mọi người chung một IP ⇒ một sổ đếm); đặt 3 biến trong `compose.yml`; đếm trong RAM ⇒ khởi động lại là xoá sổ (chấp nhận cho đồ án).
**(6) XONG (21:08 09/11/2026):** review `p9-t2-web` `2ac126a` (E, phần 0 USD) — **ready** 0 blocker · 0 major · 2 minor; `report_agent/2026-11-08_phase_9_ban_13/c_t2_web_review.md` (untracked). Chạy lại: 183 test đạt · Q1 cờ tắt 228/228 giống byte. Worktree `/tmp/c_t2rv` (tách, symlink `data/`, `knowledge-base-hue/`) — gỡ khi xong.
**Bẫy (A ghi, 1 dòng):** harness đếm dòng `application.log` theo vị trí — từ `ccc9f4f` log xoay vòng 10 MB ⇒ lượt đo trùng lúc xoay đếm hụt; kiểm cỡ log trước lượt đo. `p12-chot-deploy` đã merge (`ccc9f4f`), nhánh chờ User `!` xoá; worktree `/tmp/c_dep` gỡ khi xoá nhánh.
**(7) XONG (21:11 09/11/2026, A giao):** review sớm `p9-t4-lich` `9780d93` (E) — 0 blocker · 1 major (thêm tiêu chí "câu xin lịch không hỏi kèm có câu cố định (b) = 0", code không sửa); `report_agent/2026-11-08_phase_9_ban_13/c_t4_lich_review.md` (untracked). 331 test · Q1 tắt 228/228. Worktree `/tmp/c_t4rv` (tách, symlink) — gỡ khi xong. Lệch: plan T4 sha trên ổ `5a22b51fe49c` ≠ A duyệt `29708ef92e30` (đã báo A).
**RẢNH CÓ LÝ DO (21:11 09/11/2026):** chờ G phương án B (`p9-g-b`, B) vào `main` ⇒ xem delta sau rebase của T2 (E) + T4 (E) + kết quả lượt có phí.

## PHIÊN SAU ĐỌC TRƯỚC (C mới bắt đầu ở đây — viết 12:17 08/11/2026)

**Trạng thái:** rảnh có lý do — việc dở duy nhất là **T3 chờ User chọn hướng**. Phiên 08/11 terminal: C `hue-rag-e9` · A `hue-rag-a8` · B `hue-rag-a1` · E `hue-rag-22` (tên đổi khi mở lại — `ListAgents`).

### 1. T3 bảng vé + giờ mở cửa — cờ `tra_ve_gio` TẮT, chờ User
- Nhánh **`p9-t3-bang` = `21ec06d`** (pushed; rebase trên `main` `f124527`). Worktree **`/tmp/c_t3`** còn (symlink `data/`, `knowledge-base-hue/`; cờ trong worktree đã trả `false`).
  Gỡ khi xong: `rm /tmp/c_t3/data /tmp/c_t3/knowledge-base-hue && git worktree remove /tmp/c_t3` (`rm` bị chặn ⇒ User `!`).
- Report `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` (§1–§11). Plan bản 2 `docs/superpowers/plans/2026-11-08-phase-9-t3-bang-plan.md` `dbcd1a2f6d81` (A duyệt).
- Kết quả: Q2 (20 câu) `main` 16 · v1 17 · v2 18 · **v3 19 / 20 ✓** · khối điều kiện 4 / 4 ✓ · **sàn Q3 trượt 6 / 10** (model tự nêu điều kiện miễn giảm, chép từ đoạn kho) ⇒ **âm** theo luật.
- **Câu chờ User — phiếu `data/phase_9/t3_bang_ve_gio/phieu_chon_huong.md` (C khuyến nghị (a)):**
  - **(a) phương án B:** bỏ tra bảng đưa model + khối; bảng chỉ dùng kiểm số **sau** khi model viết, số lạ ⇒ câu cố định "giá / giờ có thể khác — xem nguồn" (≈ 0,05 USD, ~1 giờ).
    Làm: trong `_ve_gio_cuoi` bỏ khối / câu dẫn, kiểm mọi câu tuyến Huế khi cờ bật có từ khoá; bỏ `tra_truoc` + công cụ; đo lại Q2 (mốc + nhánh, `do_t3.py` đã sửa) + S1 ×2.
  - **(b) code lọc câu điều kiện khỏi chữ model** (giữ dòng giá theo nhãn), vòng 4 ngoài plan (≈ 0,1 USD, 1–2 giờ): thêm bộ lọc trong `_ve_gio_cuoi` khi có khối; test cắt nhầm /
    bỏ sót; đo Q2 + Q3 + S1 ×2 + S4.
  - **(c) đổi sàn Q3** (User duyệt — nới tiêu chí sau khi thấy số): không code; chạy S1 ×2 + mốc + S4 rồi quyết theo S1.
- **Bảng + quyết định User:** `bang_v1.json` `874af96dd995` — User 08/11 câu 1 (a) hiện cả hai nguyên văn khi kho ghi khác nhau; A theo khuyến nghị câu 2–5 (bỏ sự kiện đã diễn
  ra · giữ dịch vụ · quy định chung chỉ cho Quần thể · giờ chung Quần thể cho Bảo tàng Cổ vật + vé tuyến · chợ = "giờ hoạt động (kho mô tả)").
- **Dữ liệu (private):** `data/phase_9/t3_bang_ve_gio/` — `bang_v1.json` `874af96dd995` (User duyệt 08/11 câu 1; A câu 2–5), `bang_nhap.json`, `phieu_cho_user.md`, `q1/`, `do/` (bộ
  `bo_t3.jsonl` md5 `c89955f1bed9`, kết quả Q2 mốc + v1–v3, `q3_cham.json`, `s1_nhanh/` sinh nhánh ×2 **chưa chấm**), `tools/` (`kiem_nhap.py`, `gop.py`, `chot_v1.py`, `do_t3.py`,
  `an_toan_t3.py`, `anh_nho.py` ở `data/phase_11/anh_cong/tools/`).
- **Lệnh khi đi tiếp** (chạy từ `/tmp/c_t3/backend`, bật cờ tạm `sed -i 's/^  tra_ve_gio: false /  tra_ve_gio: true  /' config/settings.yaml`, trả lại sau):
  - Q2: server `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --host 127.0.0.1 --port 8899` (chạy nền, tắt bằng
    TaskStop) ⇒ từ gốc repo `uv run python data/phase_9/t3_bang_ve_gio/tools/do_t3.py chay http://127.0.0.1:8899 /tmp/c_t3/backend/logs/application.log data/phase_9/t3_bang_ve_gio/do/bo_t3.jsonl <ra.jsonl> --dung 0.04`
    ⇒ `… do_t3.py cham data/phase_9/t3_bang_ve_gio/do/bo_t3.jsonl <ra.jsonl> data/phase_9/t3_bang_ve_gio/do/q2_moc_main.jsonl` (công cụ đã sửa: client mới mỗi câu ⇒ chạy lại cả mốc).
  - S1 nhánh: `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python /home/minhhieu/hue_rag/data/phase_9/t3_bang_ve_gio/tools/an_toan_t3.py <thư mục mới> --repeat 2 --cap 0.06`;
    S1 mốc: cùng lệnh từ `/home/minhhieu/hue_rag/backend` (`main`, cờ tắt) `--repeat 1`; chấm 4 số theo thủ tục bộ an toàn (2 người chấm mù).
  - S4: mẫu Golden 30 (`data/phase_9/bo_do_b1/mau_golden_30.json`) nhánh + mốc cùng lượt chấm mù — **chưa có công cụ** (dựng theo khuôn `an_toan_t3.py`).
  - S5 (tốc độ): A xếp lượt riêng (máy dùng chung) — `do_t3.py chay` ghi `first_text_ms`.
- Lỗi đã biết: (1) fallback "câu hỏi liền trước" gắn điểm cũ khi đổi chủ đề (report §11); (2) `do_t3.py` bản cũ chạy cả bộ trong một cuộc (đã sửa).

### 2. Việc khác hôm nay — xong, đã vào `main` (chi tiết ở nhật ký dưới + report)
- Review 7 ảnh cổng (`c9931be`) · review bật hỏi bằng ảnh (`3da1cb1`) · việc nhỏ của C (`ad21b6c`: tóm tắt thẻ, nút báo sai, ảnh nhỏ điện thoại, link "Nguồn ảnh", số mục web ⊂ kết quả
  tìm, `turn_id` trong `chat_metrics`) · rà tính năng chưa làm (`data/ra_soat_tinh_nang_2026-11-08/C.md`) · nháp bộ đo định tuyến (`data/phase_9/dinh_tuyen_2/bo_do_nhap.md`) · spec
  bản 13 §12 (User duyệt `5557f0fd7650`) · nháp `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md` (A duyệt lúc kết phiên).

### 3. Bẫy gặp hôm nay
- **Không `uv sync` thường** khi nhánh T1 (thư viện `lunar-vn`) chưa vào `main` — dùng `uv sync --inexact --frozen` nếu cần.
- `kill` PID server tạm bị auto mode chặn ⇒ chạy server bằng `run_in_background` để tắt bằng TaskStop; nếu lỡ `nohup` ⇒ User `!`.
- `test_cong_dot_1::test_weather_and_feature_routes` hỏng **chỉ khi nạp khoá** (`--env-file`; có khoá ⇒ ảnh bật) — không do nhánh.
- `tim_so_tien` cần đơn vị ("đồng") — ô bảng giá trong kho thường ghi số trần ⇒ phía "cho phép" phải nhận cả số nhóm nghìn trần.
- Công cụ đo SSE: một `httpx.Client` giữ cookie ⇒ mọi câu chung một cuộc trò chuyện — mỗi câu một client.
- Bộ chấm: nhãn giá phải kèm đơn vị như bảng; tập cho phép theo đúng chữ plan — kiểm bộ chấm trên một câu trước khi đọc số.
- `an_toan_run.py` cũ gọi `answer_case` **không** cờ (= RAG 1–8) ⇒ đo trợ lý phải truyền `AssistantFlags.from_settings`.
- `wait_for_function` chuỗi của Playwright bị CSP chặn (`unsafe-eval`) ⇒ chờ bằng vòng Python.
- Sub-agent đọc kho đôi khi đổ đầu ra ra `/tmp` — brief nhắc "không ghi file ngoài đích".
- Giờ trong file: luôn `date`; không ghi "~hh:mm".

### 4. Thắc mắc / câu hỏi còn treo
- T3: chờ User chọn (a) / (b) / (c) — trước đó không code thêm.
- Q3 hiện đếm "model tự nêu điều kiện" kể cả khi đúng với kho (T06 đúng) — nếu chọn (c) cần định nghĩa lại sàn bằng chữ trước khi đo.
- Kiểm cuối T3 chỉ chạy ở lượt có tra bảng; câu tiền / giờ không nêu tên điểm có trong bảng không được kiểm (giới hạn thiết kế, report §11).

### 5. Tiền C 08/11 ≈ **0,096 USD**: review bật ảnh 0,0020 · việc nhỏ ≈ 0,009 · T3 0,0853 (Q2 mốc 0,0128 + v1 0,0128 + v2 0,0119 + v3 0,0122 + S1 sinh 0,0355); mọi việc khác 0 USD.

---

## (08/11) nhật ký trong phiên — chỉ tra cứu

Terminal: C `hue-rag-e9` · A `hue-rag-a8` · B `hue-rag-a1` · E `hue-rag-22`. User cấp lại quyền phiên "như 07/11" (A báo).
**Việc A giao (09:22 08/11/2026):** review cả nhánh `p11-anh-cong` của B (7 ảnh cổng) **khi B nhắn xong** ⇒ report `report_agent/2026-11-06_giao_dien_cong/c_anh_cong_review.md`. Tiêu chí: git ls-files / log -p không chứa ảnh #5 thật; clone sạch hiện `5_3` + đúng ghi công; ghi công 7 ảnh khớp `data/nghien_cuu_giao_dien_2026-11-06/anh/viwiki/danh_sach.md`; CSP 0 vi phạm; build + `test_static_ui.py`; hook.
Chuẩn bị (0 USD): git blob hash ảnh #5 thật (`ngoai_git/lv_festivals.jpg`) = `b2005024230b` (md5 `7eb7c9dc3625`) ⇒ tìm trong mọi blob của nhánh. Dự phòng `lv_festivals.jpg` blob `81d76895dfee`. Ghi công #1 trong `danh_sach.md` bị cắt cụt ("…Feel free to") ⇒ kiểm B ghi tên tác giả đúng.
**Việc A giao ưu tiên trước (sau 09:22 08/11/2026):** rà .md tìm tính năng đã ghi mà chưa làm — phạm vi C: `session_prompt/` (kể cả archive, bỏ SO_CAI_TIEN), `report_agent/`, `data/**/*.md` nghiên cứu; E làm `bao_cao_he_thong/` + `docs/` + `guides/`. Đầu ra **duy nhất** `data/ra_soat_tinh_nang_2026-11-08/C.md` (private). Cách làm: 4 sub-agent chỉ đọc (session_prompt · report_agent 24/10–01/11 · report_agent 02/11+ · data nghiên cứu), C gộp + kiểm trạng thái bằng `settings.yaml` / code. 0 USD. **XONG 09:42 08/11/2026:** `C.md` sha256 `be44d3d54342` — A 31 ý · B 47 ý + mục quyết không làm + mục đã làm; đã nhắn A. Tiếp: review ảnh khi B nhắn.
**Review ảnh XONG 09:50 08/11/2026:** `report_agent/2026-11-06_giao_dien_cong/c_anh_cong_review.md` sha256 `c9ecc607ff64` (untracked — A commit) — **ready_for_user_confirmation**, 0 blocker / 0 major / 2 minor (link "Nguồn ảnh" chân trang không cuộn tới mục; số tương phản làm tròn). Bằng chứng `data/phase_11/anh_cong/c_review/`. Worktree `/tmp/c_anh_rv` đã gỡ. 0 USD. Rảnh có lý do — chờ A.
**Review bật ảnh XONG 10:01 08/11/2026:** `report_agent/2026-11-05_phase_10_anh/c_bat_anh_review.md` — ready (E rebase: xung đột `GioiThieu` với `c9931be`, giữ cả hai). ≈ 0,0020 USD (Phase 10).
**ĐANG LÀM — Việc 2 "việc nhỏ" (User 08/11 duyệt Nhóm 1 + 2, A giao):** nhánh `p11-viec-nho-c` worktree `/tmp/c_vn` (symlink `data/`, `knowledge-base-hue/`) từ `main` `1611d34`. Ý: (3) tóm tắt thẻ · (8) nút báo sai trang bài · (10) ảnh nhỏ điện thoại · m-1 link Nguồn ảnh cuộn tới mục · (11) chuỗi số mục web ⊂ đoạn trích · (13) `turn_id` vào `chat_metrics`. Trần ≤ 0,01 USD.
Khai báo file sẽ sửa: `backend/api/routes/cong.py`, `backend/api/feedback.py` (hoặc route mới cạnh đó), `backend/api/routes/chat.py` (chỉ dòng metrics), `backend/llm/tra_web.py` (`kiem_muc_web`), test tương ứng (`tests/test_cong_dot_1.py`, `tests/test_tra_web*.py`, `tests/test_api_chat.py` nếu cần), `frontend/src/pages.jsx` (trang bài, ảnh `srcset`), `frontend/src/App.jsx` (chân trang), `frontend/src/anh.js`, `frontend/src/route.js` (nếu cần cuộn mục), `frontend/src/index.css`, `frontend/public/anh/*_800*.jpg` (mới). Chồng: B `p11-ban-do` (pages.jsx Giới thiệu, chat.jsx, app.py), E (chat.jsx stream, assistant.py) — bên merge sau rebase.
**XONG — chờ review (10:27 08/11/2026):** `p11-viec-nho-c` = `2c2c1bf` (pushed). Report `report_agent/2026-11-06_giao_dien_cong/c_viec_nho_implementation.md` sha256 `ddde67946081` (untracked — A commit). Tiền ≈ 0,009 USD. Bằng chứng `data/phase_11/viec_nho_c/`; công cụ ảnh nhỏ `data/phase_11/anh_cong/tools/anh_nho.py`. Worktree `/tmp/c_vn` (symlink `data/`, `knowledge-base-hue/`) giữ tới khi review xong — gỡ symlink trước `git worktree remove`. Test hỏng sẵn trên `main`: `test_b6_tra_web.py::test_web_section_renderer_uses_filter_without_links` (từ `27ed091`) — A: B đã sửa (`a4fde29`) ⇒ rebase là hết; gộp `GioiThieu({ banDo, anh, muc })` khi rebase.
**Nháp bộ đo đổi định tuyến XONG 10:34 08/11/2026:** `data/phase_9/dinh_tuyen_2/bo_do_nhap.md` + `tools/dem_tuyen.py` (0 USD). Chờ A / User chốt sàn. A quyết 4 điểm (ghi trong nháp). **Chờ A nhắn "viết spec"** (sửa đổi spec Phase 9: định tuyến 2 nhóm + 4 công cụ: ngày + âm lịch · tra web thành công cụ · bảng vé + giờ có cấu trúc · lịch trình câu tự do). Đã đọc trước (10:39 08/11/2026): spec Phase 9 §3, §5 B6, §7, §11; plan B5c (âm 2 lần — `b162`), plan B6 D1; TONG_HOP `2026-11-06_b5_cau_tu_nhien` (kín v2 3/5), E20 (Sửa 1 / 2), e19_kin_v2 (K2 hỏi lại thừa do model gửi số khác). `OUT_OF_SCOPE_ANSWER` đã có + cổng web đã đóng với nó.
**Spec bản 13 XONG — chờ review (khoảng 10:50 08/11/2026):** `docs/superpowers/specs/2026-11-02-phase-9-design.md` §12 (dòng 491–608, +131) + dòng trạng thái + bảng căn cứ bản 13; sha256 lúc viết `0845b1caefbc` (A tính lại). Chưa commit (A). 0 USD. Đợt 1 phần C sau khi duyệt: **T3 dữ liệu** (bảng vé + giờ từ kho, User duyệt).
**ĐANG LÀM (A giao, spec đang B review `5d5edde`):** nháp bảng T3 — 2 sub-agent (giá vé · giờ) đọc kho qua `grep_kb.sh` ⇒ `data/phase_9/t3_bang_ve_gio/ve_nhap.json`, `gio_nhap.json`; C kiểm bằng `tools/kiem_nhap.py` (chuỗi có thật ở file:dòng) ⇒ gộp `bang_nhap.json` + `phieu_cho_user.md`. 0 USD.
**XONG 11:08 08/11/2026:** `bang_nhap.json` sha256 `22df90450f0c` (66 điểm · 161 dòng vé · 107 dòng giờ · 42 + 59 miễn giảm; kiểm 1.011 / 1.011 chuỗi có thật ở file:dòng) + `phieu_cho_user.md` `25145f6123b7` (5 câu: 14 chỗ kho mâu thuẫn · sự kiện đã qua · dịch vụ · áp quy định chung / giờ chung · chợ). Công cụ `tools/kiem_nhap.py`, `tools/gop.py`. Plan T3 `docs/superpowers/plans/2026-11-08-phase-9-t3-bang-plan.md` (A sha `81767d819e13`, sub-agent review). Chưa code tới khi plan duyệt + User duyệt bảng. Sub-agent giờ lỡ đổ một đầu ra `grep_kb` (travel/places) ra `/tmp` rồi xoá ngay. User: phiên dừng ~13:00, A nhắn "kết phiên".
**T3 (11:36 08/11/2026):** User duyệt bảng (câu 1 (a); A câu 2–5) ⇒ `bang_v1.json` `874af96dd995`. Plan bản 2 `dbcd1a2f6d81` A duyệt. Code `p9-t3-bang` = **`7ae4faf`** (pushed, cờ tắt), worktree **`/tmp/c_t3`** (symlink `data/`, `knowledge-base-hue/`; gỡ symlink trước `git worktree remove`). Test 36 + 542/1 (hỏng sẵn main, phụ thuộc thứ tự). Q1 off 228/228, on 181/181 + 45 câu có công cụ. **Q2 lượt 1 ÂM** (nhánh 17/20 < 19, mốc 16/20; model gọi công cụ 2/20; Q3 khối 0/4) — report `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` `f77b5f023be9` (untracked). Tiền T3 0,025679. **Chờ A chọn:** (a) phương án B (bảng chỉ kiểm cuối) · (b) khuyến nghị: code tự tra khi có từ khoá + dò được tên điểm ⇒ dòng bảng thành nguồn trước lần sinh. Lệnh chạy lại Q2 (server nhánh cờ bật, cổng 8898): `uv run python data/phase_9/t3_bang_ve_gio/tools/do_t3.py chay http://127.0.0.1:8898 /tmp/c_t3/backend/logs/application.log data/phase_9/t3_bang_ve_gio/do/bo_t3.jsonl <ra.jsonl> --dung 0.04` rồi `… cham data/phase_9/t3_bang_ve_gio/do/bo_t3.jsonl <ra.jsonl> data/phase_9/t3_bang_ve_gio/do/q2_moc_main.jsonl`. S1 (an toàn 32 nhánh ×2 + mốc ×1, `data/loi_nang_2026-10-28/tools/an_toan_run.py`) + S4 chưa chạy; S5 A xếp riêng. **Tiền C 08/11 ≈ 0,05 USD** (review bật ảnh 0,0020 · việc nhỏ 0,009 · T3 0,0375 · khác 0).
**12:15 08/11/2026:** nháp `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md` (A duyệt / sửa lúc kết phiên; chỗ trống cho B / E). C rảnh.
**12:14 08/11/2026 (A giao, 0 USD) xong:** T06 "trẻ 7–12 tuổi miễn phí" (Bảo tàng Cổ vật) **ĐÚNG với kho** (file vé Quần thể dòng 24 + 33) ⇒ không phải lỗi đang chạy; `do_t3.py` sửa: client mới mỗi câu (lượt đã chạy cùng thước, ghi report); lỗi T17 vào report §11 giới hạn. Report `ca952b559efc`. C rảnh — chờ A / kết phiên.
**T3 vòng 3 (User duyệt) — KẾT QUẢ 12:12 08/11/2026: ÂM** (Q2 19/20 ✓ nhưng sàn Q3 trượt 6/10 — model tự nêu điều kiện miễn giảm, chép từ đoạn kho). Cờ `tra_ve_gio` tắt. Nhánh `p9-t3-bang` = **`21ec06d`** (pushed). Report §9 `8fb8a3949a66` (untracked — A commit). Lỗi phát hiện: (1) `do_t3.py` chạy 20 câu trong **một cuộc** (một `httpx.Client` giữ cookie) ⇒ lần sau client mới mỗi câu; (2) fallback "câu hỏi liền trước" gắn điểm cũ khi đổi chủ đề (T17 ⇒ lưu ý Chợ Đông Ba trên câu chùa Thiên Mụ). S1 nhánh ×2 đã **sinh** (`do/s1_nhanh/`, chưa chấm, chưa mốc). **Chờ A / User:** phương án B hay thiết kế lại. Tiền T3 0,085253; **C 08/11 ≈ 0,096 USD**. Worktree `/tmp/c_t3` (cờ đã trả false; symlink `data/`, `knowledge-base-hue/`) — gỡ: `rm /tmp/c_t3/data /tmp/c_t3/knowledge-base-hue && git worktree remove /tmp/c_t3`. Worktree `/tmp/c_vn` (p11-viec-nho-c, chờ review) giữ.
**T3 vòng 2 (11:49 08/11/2026, A chọn (b)):** code tự tra khi có từ khoá + dò ra tên — `c706c2f` (rebase lên `f124527`, pushed). Q1 vòng 2: tắt 228/228, bật 181/181 + 45 (21 code tra · 24 công cụ). **Q2 18/20 < 19 ⇒ âm sát ngưỡng** (Q3 khối 4/4 ✓; 2 câu trượt chữ đúng: T05 rút lại do lỗi kiểm cuối — số bảng kho không kèm "đồng", sửa 1 dòng, CHƯA sửa; T14 luật chấm chặt). Report §8 `4ce54e5cb540`. **Chờ A / User:** giữ âm (phương án B) hay sửa T05 + đo lại (vòng 3, ngoài plan). Server tạm cổng 8898 PID 360806 / 360799 còn chạy — `kill` bị auto mode chặn ⇒ User `!`. Worktree `/tmp/c_t3` giữ (cờ trong worktree đã trả `false`). Lệnh S1 khi cần: từ `/tmp/c_t3/backend` bật cờ tạm ⇒ `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python ../data/loi_nang_2026-10-28/tools/an_toan_run.py --out t3_nhanh_<ngày> --repeat 2 --cap 0.05` (+ mốc từ `main` `--repeat 1`), chấm 4 số theo thủ tục bộ an toàn.
Câu cũ: mô phỏng kín sửa lịch KHÔNG chạy (A 08/11); phiếu v7 A hỏi User.
Ghi chú cũ bên dưới (07/11) chỉ tra cứu.

## (07/11) PHIÊN SAU ĐỌC TRƯỚC
**Trạng thái:** rảnh có lý do — không việc đang dở, không worktree `/tmp` nào của C. Chờ A giao (việc A giao = User nói "làm đi"). `main` khi viết: `fbcb903`.
Phiên 07/11: terminal C `hue-rag-a0` · A `hue-rag-7a` · B `hue-rag-10` · E `hue-rag-81` (tên đổi khi mở lại — `ListAgents`).

### 1. Việc xong 07/11 (report tracked — sha256 12 lúc viết)
- **S3 đo cổng đợt 1** — `report_agent/2026-11-06_giao_dien_cong/c_s3_q_f_implementation.md` `b178c47c6abe`:
  - bộ quyết 12 tổ hợp `data/phase_9/cong_dot_1/to_hop_chinh_thuc.jsonl` md5 `792a3cbe3fe5` (ẩn "đi dày" theo Q-U3) — **đã dùng để quyết**, từ nay chỉ là bộ hồi quy;
  - **Q-G + Q-N trên `27ed091`: ĐẠT** (7 / 7 đích × 1440 / 390, 0 CSP / console, JS gzip 101,9 KB, tương phản thấp nhất 5,42; Q-N 10 / 10) — đã merge;
  - **Q-F bộ quyết trên `632a4f7` (V5): ĐẠT** — sàn code 24 / 24, F-a 12 / 12 + 12 / 12 (2 sub-agent, 0 bất đồng); User duyệt bật biểu mẫu + F-a (4) = "không trái nhóm đi cùng" ⇒ `main` `a884de4` cờ `lich_trinh_bieu_mau` BẬT;
  - §6 chữ đầu trên `main` `a884de4` (theo dõi): biểu mẫu p50 2,30 / p95 4,22 s · câu kho 1,78 / 3,61 s (n = 10 mỗi loại).
  - Data private: `data/phase_9/cong_dot_1/s3/` (lan_1 / lan_2 / `fa/` phiếu + 2 file chấm), `qn/` (10 câu Q-N + kết quả), `qg_tuong_phan_27ed091.json`, `chu_dau_main_a884de4.jsonl`.
- **X1 / X1b / X1c lượt biểu mẫu bị model từ chối** — `report_agent/2026-11-06_giao_dien_cong/c_x1_luot_bieu_mau.md` `99abfe79ee01`; data `data/phase_11/cong_dot_1/x1/`. Nguyên nhân (ủng hộ, chưa chứng minh): `LICH_TRINH_LUAT` nằm trong phần Bằng chứng ⇒ model coi là dữ liệu. V0 từ chối 10 / 16 · V1 (giả lượt công cụ) 12 / 16 · V2 (luật lên lời dặn hệ thống) 1 / 16 → 0 / 16 nhưng chữ đầu p95 8,8 s · V4 (thêm câu dặn) kém · **V5 = V2 + reasoning `low`** đạt (p95 4,75 s) ⇒ B đưa vào nhánh · V6 `minimal` ⇒ 400 · V3 (code dựng lời, 0 USD) đọc như trích máy. Đề xuất dự phòng chưa làm: "hiện khung code trước, lời model sau".
- **Tự soi** — `report_agent/2026-11-07_tu_soi_lo_trinh/tu_soi_C.md` `69727aa946ad` (deploy chưa thử = rủi ro lớn nhất; đóng hồ sơ sửa lịch; gỡ 3 cờ âm ở B7; giọng nói cắt nếu chưa có 40 câu trước ~20/11; đợt 2 chỉ P1).
- **C-tl thời lượng tham quan từ web** (0 USD; private): `data/phase_9/lich_trinh/thoi_luong_web.json` (link + ngày + trích từng nguồn) · `diem_v7_thoi_luong_web_nhap.json` sha256 `363763ae2101` (trường khác giống v6) · `tools/dung_v7.py` · tra thô `data/tra_cuu_cli/2026-11-07_c-tl-thoi-gian-1/`, `-2/`. 19 / 26 điểm có số (11 ngắn · 8 nửa buổi); mức chắc cao 4 · vừa 5 · thấp 6 · lệch 4.
- Dữ kiện Q-U3: `kieu_di` không đổi khung ở 0 / 120 tổ hợp với bảng v3/v6; v7 ⇒ 12 / 120.

### 2. Đang chờ User (qua A) — C không tự làm
- **Phiếu v7** `data/phase_9/lich_trinh/diem_cho_user_v7.md` (sha256 `ee2f22328691`): A dùng cả bảng / B chỉ dòng chắc cao + vừa (9 điểm) / C giữ v6. `settings.yaml` `lich_trinh_bang` vẫn `diem_v3.json`.
- **3 luật xếp "đi dày" đề xuất, CHƯA ĐO** (phiếu v7 §2): điểm thứ hai lấy cả di tích lấp chỗ · cho cặp ngắn ở cụm kề · "đi dày" mở buổi tối hợp sở thích cho nhóm không hạn chế. Biểu mẫu đợt 1 đã ẩn "đi dày" ⇒ không chặn gì.
- **Mô phỏng kín sửa lịch: vẫn DỜI** (sửa lịch hoãn, có thể đổi cách "điền lại biểu mẫu") — lệnh ở mục (cũ) dưới, chỉ chạy khi A giao lại.

### 3. Công cụ dùng lại được (private, chạy từ `backend/` của worktree nhánh cần đo; `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag [--env-file /home/minhhieu/hue_rag/.env] python …`)
- `data/phase_9/cong_dot_1/tools/do_bieu_mau.py` md5 `4de78cb35999` — Q-F biểu mẫu: `kiem <bộ>` (0 USD: luật phủ + xếp thật + 9 ca phá) · `chay <bộ> <out.jsonl> --lan N [--dung 0.025]` (CÓ PHÍ, `/api/chat/stream` qua TestClient, bọc `_remember`; `--dung` cộng mọi *.jsonl cùng thư mục) · `cham` · `phieu <bộ> <kq> <thư_mục>` (đầu vào 2 người chấm F-a) · `gop <thư_mục> <c1> <c2>`.
- `data/phase_9/cong_dot_1/tools/tuong_phan.py` md5 `f53a31153ce3` — tương phản WCAG trên trang đã dựng (Playwright): `uv run python …/tuong_phan.py http://127.0.0.1:<cổng>/ --trang '#/,#/kham-pha,#/kham-pha/foods,#/kham-pha/bai/<id>,#/len-ke-hoach,#/tro-ly,#/gioi-thieu' [--json out]`.
- `data/phase_9/cong_dot_1/tools/playwright_cong.py` md5 `fa580e39f5ed` — 7 / 7 đích ≤ 2 lần bấm + mở thẳng / tải lại + CSP / console + bundle: `uv run python …/playwright_cong.py http://127.0.0.1:<cổng>/ --dist <worktree>/frontend/dist`.
- `data/phase_9/cong_dot_1/tools/qn_nguon.py` md5 `3710c9c69c4e` — Q-N 10 câu (`qn/cau_qn.txt`) qua giao diện + chữ đầu phía trình duyệt (CÓ PHÍ ~0,004).
- `data/phase_9/cong_dot_1/tools/do_chu_dau_main.py` md5 `5915e4a681ef` — chữ đầu qua server thật: `uv run python …/do_chu_dau_main.py http://127.0.0.1:<cổng> <log server> <out.jsonl>` (CÓ PHÍ ~0,008).
- `data/phase_11/cong_dot_1/x1/x1.py` (gọi hàm lõi trong tiến trình, V0–V3) · `x1b.py` / `x1c.py` (đường stream, agent clone đổi lời dặn / reasoning) · `tong.py` / `tong_b.py` (in bảng). Mẫu để thử biến thể lời dặn / tham số model mà không sửa nhánh.
- Cổng server tạm: worktree tách (`git worktree add --detach /tmp/<tên> <sha>` + symlink `data/`, `knowledge-base-hue/`), `cd frontend && npm ci && npm run build` nếu cần giao diện, `uvicorn api.app:app --port <trống>` chạy nền, tắt bằng TaskStop, gỡ symlink rồi `git worktree remove --force`.

### 4. Bẫy đã gặp 07/11
- `gpt-6-luna` **không nhận `reasoning.effort = "minimal"`** ở đường trả lời ⇒ 400 (`BadRequestError`, app không log chữ lỗi). `low` được.
- **Chỉnh trên bộ phát triển, quyết trên bộ giữ riêng**: X1 dùng 8 tổ hợp phát triển; bộ quyết 12 không chạy / không xem tới khi chốt biến thể. Giữ cách này cho thí nghiệm sau.
- **Đo latency không chồng việc nặng**: trước lượt đo nhắn B / E (và hỏi A — có lúc một dự án khác trên máy cũng chờ dùng máy); xong nhắn "xong đo". Lượt latency là việc của một người một lúc.
- `kiem_cuoi` không phân biệt biến thể khi lượt từ chối được code thay bằng lời tối thiểu (B171) ⇒ đếm từ chối riêng (chữ model = câu từ chối hoặc có `chu_thay`).
- `kiem_khung` coi ngày bị cắt vì vượt ngân sách (`vuot_ngan_sach`) là hợp lệ ⇒ đếm riêng (`cat_ngay_cuoi`).
- Tiêu chí chấm bằng người / sub-agent có chữ mơ hồ ("phù hợp người đi cùng") ⇒ ghi cách hiểu **trước** khi chấm; người làm không tự chốt cách hiểu sau khi thấy số.
- Sub-agent chấm có thể ghi file bằng Bash thay vì Write — kiểm file ra đủ mã, ghi vào report.
- **Sửa trước khi tái tạo** (C210): việc "sửa lỗi X" mà nguyên nhân chưa chứng minh ⇒ tái tạo trên code gốc TRƯỚC (đọc tham số thật), chưa viết sửa — A phải nhắc lần này.
- Đổi hành vi code (vd B171 đổi khung) ⇒ chạy lại mô phỏng nhãn (`mo_phong.py`, kín qua `!`) **trước** lượt có phí.
- Q1m: `data/phase_9/b5b/tools/capture_flags.py <out> lich_trinh=1 sua_lich=0|1`. Script import `llm.*`: không `-I`, `PYTHONPATH=$PWD`.
- Rebase "hai bên cùng thêm": giữ cả hai, kiểm `git range-diff`. Heredoc shell có backtick ⇒ dùng Write.
- Ca dò của người kiểm gồm cả câu **hợp lệ** model hay viết. Giờ trong file: luôn `date` trước.
- Overpass máy chủ công khai hay quá tải (06/11: 3 / 5 lượt 502) ⇒ `out count` nhẹ qua được; lấy thẻ thì một lần, giãn cách, không gửi dồn.
- Tin A có thể đến lúc C đang làm việc khác ⇒ việc mới ưu tiên theo lời A (vd B171 trước harness); việc dở ghi STATUS trước khi chuyển.

### 5. Tiền C 07/11 ≈ **0,078 USD**: X1 0,0247 · X1b 0,0174 · X1c 0,0143 · Q-N 0,0042 · S3 0,0087 · chữ đầu `main` 0,0084; mọi việc khác 0 USD (Codex tra web dùng tài khoản ChatGPT).

### 6. Tạm
- `/tmp/c_tl/` chỉ còn file thử / bảng tạm (yêu cầu tra web, kết quả thử V3, bảng tương phản) — không dữ liệu kín; mất khi khởi động lại cũng được.

---

## (cũ) — kết phiên tối 06/11 (chỉ tra cứu)

### Việc + lệnh của phiên tối 06/11 (S3 / S4 trong đó đã XONG 07/11; harness + lệnh sửa lịch vẫn đúng khi mở lại)
- **Đã xong tối 06/11** (terminal `hue-rag-42`):
  - **Harness sửa lịch:** `data/phase_9/sua_lich/tools/chay_sua_lich.py` md5 `559ebaf5f81e` — E review vòng 2 + vòng 3: **ready**. Bộ Q4 `bo_do_sua_lich/chuoi_q4.jsonl` `d35f8d9c5027`. Pilot = S01 + S06 (A duyệt). Report `report_agent/2026-11-02_phase_9_code/c207_rebase_sua_lich.md` §7–§8.
  - **B171 review:** ready trên `b0e52f8` (đã merge `dbb4004`) — `report_agent/2026-11-06_b5_cau_tu_nhien/b171_review.md` §7–§8.
  - **C208:** `p9-sua-lich` ⇒ **`79b3d9c`** trên `main` `d930867` (pushed). Gỡ xung đột B5b; sửa `hoi_toi` khi xếp lại / sửa trực tiếp + 4 test. 411 test; Q1 / Q1m 228/228 (`data/phase_9/sua_lich/q1_c208/`). Nhãn đã thấy S03 / S08 sửa theo B171 ⇒ `chuoi_da_thay.jsonl` **`c00de07114b5`**. E kiểm rebase: ready.
  - **C209:** `data/nghien_cuu_giao_dien_2026-11-06/nguon_du_lieu_dot_2.md` (P1 / P2 / P3 bản đồ + dữ liệu; C khuyên P1) — chờ User quyết khi A trình spec.
  - **C210:** chưa tái tạo được "hỏi lại số ngày thừa" ⇒ không sửa code (`report_agent/2026-11-06_b5_cau_tu_nhien/c210_implementation.md`). Đề xuất: harness kín lần sau ghi `so_ngay` model gửi + số code dò + có thẻ hỏi không.
  - **C211:** nháp kỹ thuật spec đợt 1 `data/nghien_cuu_giao_dien_2026-11-06/spec_dot1_ky_thuat_nhap.md` — A dùng khi viết spec.
- **Việc đầu phiên sau — lệnh `!` mô phỏng bộ kín sửa lịch** (0 USD, chỉ in số đếm + mã chuỗi / số lượt hỏng, trên nền `79b3d9c`):
  1. C dựng lại worktree (đã gỡ):
     ```
     git worktree prune; git worktree add /tmp/c_sualich p9-sua-lich
     ln -s /home/minhhieu/hue_rag/data /tmp/c_sualich/data
     ln -s /home/minhhieu/hue_rag/knowledge-base-hue /tmp/c_sualich/knowledge-base-hue
     ```
  2. Đưa User lệnh nguyên văn (cũng ở report C207 §8):
     ```
     ! cd /tmp/c_sualich/backend && PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python ../data/phase_9/bo_do_sua_lich/tools/mo_phong_kin.py | python3 -c "import json,sys,re; d=json.load(sys.stdin); print('kin ok', sum(v=='ok' for v in d.values()), '/', len(d)); [print(k, [re.match(r'L[0-9]+', x).group() for x in v]) for k, v in d.items() if v != 'ok']"
     ```
  3. Kết quả hỏng ⇒ sửa nhãn kín bằng `bo_do_sua_lich/tools/cau_truc.py` (không in câu) **trước** lượt có phí. `main` đổi code ⇒ rebase + Q1 / Q1m trước.
- **Sửa lịch — HOÃN** (handoff 22:41 06/11): cần cờ `lich_trinh` câu tự do; A xem lại cách sửa sau biểu mẫu ("điền lại biểu mẫu"). Khi đi tiếp:
  - thư mục kết quả `data/phase_9/sua_lich/do/` chỉ chứa file kết quả (`--dung 0.19` cộng mọi `*.jsonl` trong đó);
  - pilot S01 + S06 lần 1 ⇒ đọc file ⇒ lần 1 / lần 2 / Q4 ×2 ⇒ kín ×2 qua User `!` ⇒ `cham`.
- **S3 — đo Q-F biểu mẫu lịch trình** (spec cổng đợt 1 `docs/superpowers/specs/2026-11-06-giao-dien-cong-dot-1-design.md` bản 2 `ff3c317ec88b` §6; khi B xong S1 trên `p11-cong-dot-1`; cờ mới `assistant.lich_trinh_bieu_mau`):
  - **trước lượt có phí:** ghi 12 tổ hợp vào report S3, **sau khi User chốt Q-U3** (đi dày). Phủ đủ 5 `di_cung`; mỗi `so_ngay` 1 / 2 / 3 ≥ 3 lần; ≥ 4 có `so_thich`; ≥ 2 không chọn sở thích;
  - harness lưu **khung + chữ model + tham số** mỗi lượt (dựng theo mẫu `chay_sua_lich.py`: TestClient trong tiến trình, bọc hàm, đọc log sau mốc). Ghi cả `so_ngay` model gửi / số code dò (đề xuất C210);
  - ×2 = 24 lượt. Sàn code 24 / 24: 0 câu từ chối thay lịch, `kiem_cuoi` 0 lỗi, 0 rút lại;
  - F-a: 2 sub-agent mới độc lập chấm (khung + chữ + giá trị nút), ≥ 11 / 12 mỗi lượt theo cả hai, bất đồng ⇒ trượt;
  - Playwright §6 (Q-G phần C được giao); tiền cả spec ≤ 0,03 USD.
- **S4 — review cả nhánh `p11-cong-dot-1`** một lần (`risk-gated-agent-review`; bảng rà AI FDE §7 là một tiêu chí). Ca dò khác cách người làm: API Khám phá `../`, `sealed`, id ngoài `corpus.sources`; form gửi `truong` lạ ⇒ 422.
- **Đợt 2 (dữ liệu bản đồ / lưu trú / ăn uống / sự kiện):** chờ User chọn P1 / P2 / P3 (C209). Chọn P1 / P3 ⇒ Overpass **một** lần lấy thẻ tên ⇒ khớp toạ độ 15 điểm thiếu (người xem bằng mắt). Chọn P2 ⇒ đo dung lượng PMTiles + cỡ gói MapLibre trước.
- **Câu treo cho A** (không chặn):
  1. mô phỏng kín sửa lịch có còn cần chạy đầu phiên không, khi sửa lịch hoãn và có thể đổi cách ("điền lại biểu mẫu");
  2. C210: câu nêu số ngày mơ hồ ("3 hay 4 ngày") + model gửi số ⇒ code hiện dùng số model, không hỏi — giữ hay hỏi;
  3. link trong chữ câu trả lời chưa có `target` / `rel` — gộp vào S1 / S2?
- **Bộ đo (private, md5 12):** sửa lịch đã thấy `c00de07114b5` (trước C208 `d0ad12b6ed12`) · kín `daf762bcbbe5` · Q4 `d35f8d9c5027`; B6 `6ed74db21616` / kín `4de04132600b`; B5b `7e1bc3da2e44`; bảng `diem_v5.json` `c7d294fcacd5`.
- **Không đọc:** `data/phase_9/b5_v2/`, `data/phase_9/b5/kin/`.
- **Tiền C tối 06/11: 0,003855 USD** (C210 tái tạo; mọi việc khác 0 USD). Overpass (OSM) quá tải 3/5 lượt — lần sau gọi một lần, ngoài giờ cao điểm.
- **Backlog cho A:**
  - kho mâu thuẫn vị trí Bảo tàng Cổ vật · câu thiên tai vẫn gọi Serper · case 67 Golden từ chối ngẫu nhiên;
  - link trong chữ câu trả lời chưa có `target` / `rel` (C211);
  - câu `toi_khong_diem` nói "hợp sở thích" cả khi không nêu sở thích (E, có sẵn trên `main`).
