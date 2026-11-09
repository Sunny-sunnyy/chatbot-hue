# STATUS C — kết phiên 09/11 (viết 22:28 09/11/2026 — `date`). Lịch sử: `git log -p session_prompt/sessions/STATUS_C.md`

## PHIÊN SAU ĐỌC TRƯỚC (C mới bắt đầu ở đây — viết 22:28 09/11/2026)

**Trạng thái:** **rảnh — không việc dở, không worktree `/tmp` nào, không nhánh của C đang mở.** Phiên 09/11 terminal: C `hue-rag-6a` · A `hue-rag-87` · B `hue-rag-99` · E
`hue-rag-ea` (tên đổi khi mở lại — `ListAgents`). Chờ A giao (việc A giao = User nói "làm đi").

**Việc C phiên 09/11 (đều xong):**
- T3 bảng vé + giờ: hướng (a) code + đo (Q1 bật cờ 228/228 giống byte · Q2 lưu ý 0/20 · an toàn 32: ngoài kho bị trả lời 0/4, 1 báo nhầm do lỗi bộ đọc giờ dấu phẩy ⇒ sửa) ⇒
  **đóng hồ sơ** (User), tag `hoso/p9-t3-bang` `e547b9e`; kết luận `report_agent/2026-11-06_giao_dien_cong/c_t3_bang_implementation.md` §13. Bảng `data/phase_9/t3_bang_ve_gio/bang_v1.json` giữ.
- T2: review plan bản nháp (3 major) ⇒ C viết lại plan bản 2 (A duyệt `88b1f0586e99`; + md5 bộ hỏi kèm của E ⇒ `69836a615353`) ⇒ review code E phần 0 USD (ready) ⇒ lượt đo của E **âm** ⇒ đóng hồ sơ.
- T4: review sớm code E (1 major: tiêu chí "câu cố định (b) không nói sai" — E đo 0/19, đóng) ⇒ lượt đo **âm** ở luật xếp ⇒ đóng hồ sơ.
- 4 chốt trước deploy: `p12-chot-deploy` ⇒ merge `ccc9f4f` (A review). Biến: `HUE_LUOT_MOI_NGAY`, `HUE_COOKIE_SECURE`, `HUE_TAT_DOCS`; log xoay vòng 10 MB × 3 luôn bật.
  **Checklist deploy:** uvicorn sau Caddy cần `--proxy-headers --forwarded-allow-ips <ip Caddy>`; đặt 3 biến trong `compose.yml`; sổ đếm lượt ở RAM.
- Nháp mục "Phiên 09/11" của `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md` (A duyệt / sửa; số S5 + tiền B / E / A để trống).
- Tự soi cuối phiên đã gửi A / B / E: bài học chính — **đếm lỗi thật trên mốc trước khi dựng tính năng** (T3 chữa lỗi chưa thấy; T2 + T4 âm cùng gốc "lời dặn từ chối cả câu" — một pilot
  mốc 10 câu ≈ 0,012 USD đã đủ thấy).

**Tiền C 09/11 ≈ 0,028 USD:** T3 (a) Q2 0,010562 + an toàn 32 0,017105 · chốt deploy ≈ 0,00035 · review / plan 0 USD.

**Bẫy mới 09/11:**
- Auto mode chặn đọc file `*sealed*` cả khi A giao rõ (rào đúng, không lách) ⇒ viết sẵn một lệnh `!` chỉ in dòng cần, gửi A; `cut -c1-4000` có thể cắt mất phần trả lời — bỏ trường `context` trước khi in.
- `git worktree remove` cần `--force` khi worktree còn file gitignore (`backend/logs/`); gỡ symlink `data/`, `knowledge-base-hue/` trước.
- Log `application.log` xoay vòng ở 10 MB (từ `ccc9f4f`) ⇒ harness đếm dòng theo vị trí có thể đếm hụt nếu xoay giữa lượt — kiểm cỡ log trước lượt đo.
- `@app.middleware("http")` (BaseHTTPMiddleware) bọc luồng SSE + dò ngắt kết nối ⇒ middleware chặn lượt viết dạng ASGI thuần (`api/gioi_han.py` `ChanLuot`).
- Test gọi `logging.config.dictConfig` đổi logging toàn cục cả tiến trình pytest ⇒ hỏng test đếm dòng log — không viết test kiểu đó.
- Bộ đọc giờ / số liệt kê: ranh giới số phải cho ", " (liệt kê) — luật cũ `(?![\d,])` bỏ mọi số đứng trước dấu phẩy.

### Bẫy (08/11, vẫn đúng)
- `kill` PID server tạm bị auto mode chặn ⇒ chạy server bằng `run_in_background` để tắt bằng TaskStop; nếu lỡ `nohup` ⇒ User `!`.
- `test_cong_dot_1::test_weather_and_feature_routes` hỏng **chỉ khi nạp khoá** (`--env-file`; có khoá ⇒ ảnh bật) — không do nhánh.
- `tim_so_tien` cần đơn vị ("đồng") — ô bảng giá trong kho thường ghi số trần ⇒ phía "cho phép" phải nhận cả số nhóm nghìn trần.
- Công cụ đo SSE: một `httpx.Client` giữ cookie ⇒ mọi câu chung một cuộc trò chuyện — mỗi câu một client.
- Bộ chấm: nhãn giá phải kèm đơn vị như bảng; tập cho phép theo đúng chữ plan — kiểm bộ chấm trên một câu trước khi đọc số.
- `an_toan_run.py` cũ gọi `answer_case` **không** cờ (= RAG 1–8) ⇒ đo trợ lý phải truyền `AssistantFlags.from_settings`.
- `wait_for_function` chuỗi của Playwright bị CSP chặn (`unsafe-eval`) ⇒ chờ bằng vòng Python.
- Sub-agent đọc kho đôi khi đổ đầu ra ra `/tmp` — brief nhắc "không ghi file ngoài đích".
- Giờ trong file: luôn `date`; không ghi "~hh:mm".


---

## (09/11) nhật ký trong phiên — chỉ tra cứu (mở 20:10 09/11/2026) — C `hue-rag-6a` · A `hue-rag-87` · B `hue-rag-99` · E `hue-rag-ea`
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
**T2 âm (E, 21:49 09/11/2026):** hỏi kèm có web 4/10 = mốc; C đồng ý đóng hồ sơ, không đề xuất vòng chỉnh mô tả (đã nhắn A). **RẢNH — chờ E** rebase + đo T4 ⇒ C xem delta. Worktree `/tmp/c_t2rv` hết dùng.
**T4 âm (E, 22:18 09/11/2026):** Q3 (ii) 21 · 15 / 27 < 26; review M-1 của C đóng (câu (b) nói sai 0/19). C đồng ý đóng hồ sơ (đã nhắn A). **RẢNH — chờ A** (không còn delta nào phải xem). Worktree `/tmp/c_t4rv` hết dùng.
**Dọn (22:19 09/11/2026, A giao):** đã gỡ 4 worktree `/tmp/c_dep`, `/tmp/c_t2rv`, `/tmp/c_t3`, `/tmp/c_t4rv` (gỡ symlink trước; chỉ còn file bị gitignore như `backend/logs/` ⇒ `--force`). C không còn worktree nào. **RẢNH — chờ A** (đang khoá máy cho S5 của B: không chạy lượt có phí / pytest rộng / build).

## (07/11) kết phiên — chỉ tra cứu
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
