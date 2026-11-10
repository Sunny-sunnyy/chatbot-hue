# Implementation Report: chuẩn bị deploy — chạy thử bản deploy trên máy (không AWS)

Người làm: B (Claude Code, `hue-rag-05`) · 19:47 10/11/2026 (`date`) · việc A giao (`CURRENT_HANDOFF.md` "VIỆC PHIÊN 10/11", dòng B thứ hai). Mức nhẹ: không plan riêng.
Nhãn: **[Chạy]** = chạy thật · **[Đọc]** = đọc code / cấu hình · **[Suy]** = suy luận. Không tạo gì trên AWS. Tiền: **≈ 0,00045 USD** (2 câu, log).

## 0. Kết luận

- Nhánh **`p12-deploy-nhap` `8d650ad`** (đã push) = `main` `bb78e1e` + 2 commit cũ của nhánh (`settings_loader.py` đọc `HUE_QDRANT_URL` / `HUE_TRA_WEB` + test).
  Merge không xung đột. Nhánh **chưa vào `main`** — A quyết khi nào merge (code nhánh chỉ thêm biến môi trường, không đặt ⇒ như cũ).
- Bản nháp deploy (`data/phase_12/deploy_nhap/`, private — không commit) đã áp phần checklist làm được không cần User. Build + chạy cả bộ Qdrant + app + Caddy trên máy:
  **đạt mọi điểm kiểm** (bảng §2).
- **Sửa một lỗ rò trước khi build:** danh sách chừa mở cả `frontend/` ⇒ ảnh #5 lễ hội thật (không giấy phép mở, `frontend/public/anh/rieng/`, gitignore) sẽ vào ảnh công khai.
  Đã loại `frontend/public/anh/rieng`; giao diện tự dùng ảnh Commons khi thiếu (`frontend/vite.config.js` quyết lúc build) — đếm trong ảnh: 0 file `rieng`.

## 1. Đã sửa (nháp `data/phase_12/deploy_nhap/`)

| File | Đổi |
|---|---|
| `compose.yml` (service `app`) | `HUE_LUOT_MOI_NGAY: ${HUE_LUOT_MOI_NGAY:-50}` (lượt gọi model / IP / ngày) · `HUE_COOKIE_SECURE: ${HUE_COOKIE_SECURE:-1}` · `HUE_TAT_DOCS: "1"`; ghi chú: thử qua http thì đặt `HUE_COOKIE_SECURE=0` |
| `dung_dockerignore.py` ⇒ `Dockerfile.dockerignore` (sinh lại theo build record `main`) | thêm `frontend/public/anh/rieng` vào phần loại; 204 bài kho + 8 mục khác |
| `Dockerfile` | chỉ chú thích: số đo cỡ ảnh sau `--no-cache` |

**Không đổi `--forwarded-allow-ips '*'`** (checklist gợi ý ghi IP Caddy): cổng app không mở ra máy (compose không `ports` cho `app`) ⇒ chỉ container trong mạng compose tới được;
IP Caddy trong mạng compose không cố định. Rủi ro còn lại: client tự gửi `X-Forwarded-For` giả để lách giới hạn ⇒ **[Chạy] đã thử**: hết lượt rồi gửi qua Caddy kèm
`X-Forwarded-For` giả ⇒ vẫn 429 (Caddy không tin header này từ client). Số mặc định 50 lượt / IP / ngày: B tự chọn (≈ 0,025 USD / IP / ngày ở mức 0,0005 / câu) — đổi bằng biến.

## 2. Chạy thật [Chạy]

| Bước | Kết quả | Thời gian |
|---|---|---|
| `docker build -f data/phase_12/deploy_nhap/Dockerfile --build-context code=/tmp/b_dep/backend -t hue-rag-app:dep10 .` (từ gốc working tree chính) | đạt | **191 s** |
| Cỡ ảnh (`docker images`) | **3,57 GB** (bản 07/11 6,12 GB — `--no-cache` bỏ cache uv; `/root/.cache` nay 32 KB). Cỡ nén khi chuyển máy: chưa đo | — |
| Đếm trong ảnh (`--network none`, bỏ qua `.venv`) | kho `.md` **204**, kho mọi loại 205 (+ `meta/full_corpus_conditions.json`) · `*sealed*` **0** · `*backup*` 0 · `_source-dumps` 0 · `.env` 0 · ảnh `rieng` **0** · `data/` đúng 3 file chừa (build record, sparse state, bảng điểm v3) · đường dẫn có "evaluation" / "golden" ngoài `backend/` **0** (5 trong `backend/` là mã gói đánh giá + test, đã ở repo công khai) · `backend/` 107 file = `git ls-files backend` 107 | — |
| `compose up` (`-p hue_deploy_thu`, Caddy `:80` ⇒ cổng máy 8880, `HUE_LUOT_MOI_NGAY=2`, `HUE_COOKIE_SECURE=0`; Qdrant = bản chép collection chatbot 50 MB, Qdrant chatbot 6335 không bị đụng) | Qdrant healthy ⇒ app ⇒ Caddy | `/health` 5 / 5 sau **10 s** |
| Qua Caddy | `/` 200, có CSP · `/docs` `/openapi.json` `/redoc` **404** · `/api/tinh_nang`: `tra_web` false, `anh` false | — |
| Câu trong kho (stream, tự viết) | success, tuyến Huế, 53 `delta` + `sources` (nguồn đúng bài) · 0,00036 USD · chữ đầu 3,3 s (1 câu, ngay sau khởi động — tham khảo) | — |
| Câu ngoài kho (tự viết) | câu từ chối chuẩn · 0,000085 USD | — |
| Lượt 3 (quá giới hạn 2) | **429** `rate_limited` + câu báo cho người dùng | — |
| Lượt 4: giả `X-Forwarded-For` | **429** | — |
| `/api/chat` (không stream) cùng IP | **429** | — |
| Log (`logs/application.log`, `RotatingFileHandler` trong ảnh) | `chat_metrics` = 2 (đúng 2 lượt gọi model) · `Rate limited` 3 dòng · 0 chữ câu hỏi · 0 IP | — |
| RAM (`docker stats`) | app 939 MiB / 2 GiB · Qdrant 230 MiB · Caddy 18 MiB | — |
| Dọn | `compose down -v` ⇒ 0 container; xoá thư mục chạy thử (bản chép Qdrant + log). **Giữ ảnh** `hue-rag-app:dep10` | — |
| Test nhánh đã merge | `test_settings_env.py` + `test_chot_deploy.py` 11 đạt (9 s) · test rộng (có key, bỏ `test_static_ui.py`) **851 đạt / 1 trượt**: `test_ban_do_lich.py::test_csp_adds_tile_host…` đòi bản build giao diện (worktree không build; cùng test chạy ở working tree chính có `frontend/dist`: đạt) — không phải lỗi code; ảnh Docker tự build giao diện ở stage `web` | 3 phút 36 giây |

## 3. Câu cho User (A hỏi khi User về — B không quyết)

1. **Tra web trên bản công khai:** đang tắt (`HUE_TRA_WEB=false`). Bật ⇒ mỗi câu kho không có thông tin gửi câu hỏi ra Serper (0,001 USD / lượt) + mục "Từ web (chưa kiểm)";
   cần hạn mức Serper (gói trả trước, không tự nạp). Giữ tắt ⇒ câu ngoài kho chỉ nhận câu từ chối.
2. **Ảnh #5 lễ hội thật:** bản công khai hiện **không** có (ảnh Commons thay). Muốn có ⇒ cần quyền dùng ảnh.
3. **Số lượt / IP / ngày:** mặc định 50 — User chọn số khác nếu muốn.
4. Việc chỉ User làm được (đã có trong checklist): khoá OpenAI riêng có hạn mức chi tiêu; tài khoản / máy AWS; tên miền hoặc `<IP>.sslip.io`.
5. Ảnh cũ trên máy: `hue-rag-app:nhap2` (07/11, sạch) và `hue-rag-app:dep10` (thiếu danh sách ảnh) — không cần thì xoá: `! docker image rm hue-rag-app:nhap2 hue-rag-app:dep10`; giữ `dep10b`.

## 4. Giới hạn

- HTTPS (Caddy xin chứng chỉ thật) chưa thử — cục bộ chỉ http. Chữ hiện dần qua Caddy: không thử lại (Caddyfile không đổi từ lần đo 07/11).
- Cỡ ảnh nén, độ trễ trên máy AWS: chưa đo (cần máy thật).
- `--forwarded-allow-ips '*'` dựa vào việc cổng app không mở ra ngoài — nếu ai thêm `ports` cho `app` thì phải đổi.

## Giải thích ngắn

Đã đóng app thành ảnh Docker theo `main` mới nhất và chạy đủ bộ (cơ sở dữ liệu + app + cổng Caddy) trên máy: trả lời được, đã tắt trang tài liệu API, chặn đúng khi hỏi
quá số lượt (kể cả khi giả địa chỉ), log không ghi câu hỏi hay IP, ảnh không chứa dữ liệu kín. Một lỗ được bịt trước khi build: ảnh lễ hội không giấy phép suýt lọt vào ảnh
công khai. Bước tiếp cần User: khoá OpenAI riêng, máy AWS, và quyết tra web.

## 5. Sửa theo review C (`b_deploy_cuc_bo_review.md`; A quyết) — 20:01 10/11/2026 (`date`)

| Finding | Sửa (nháp `data/phase_12/deploy_nhap/`) | Kiểm [Chạy] |
|---|---|---|
| **M-1** ảnh thiếu `data/phase_10/anh/danh_sach_ten.json` ⇒ hỏi bằng ảnh (bật trên `main`) tắt im lặng | A chọn (a): `dung_dockerignore.py` chừa file + `Dockerfile` COPY (danh sách tên, không private) | ảnh `hue-rag-app:dep10b`: `data/` = 4 file chừa; `/api/tinh_nang` `anh: true`; POST `/api/anh/ung_vien` rỗng ⇒ **415** (route chạy, không 404); log `Image route enabled` 1, `startup failed` 0 |
| Rà file runtime (A) | theo `settings.yaml` + mã `api/`, `llm/`, `retrieval/`: cờ bật đọc kho 204 bài + `meta/full_corpus_conditions.json`, build record + sparse state, `diem_v3.json` (biểu mẫu lịch), `danh_sach_ten.json` (ảnh). `diem_toa_do_v5.json` chỉ nạp khi `ban_do_lich` bật (đang tắt); ngày âm = thư viện `lunar-vn`; thời tiết = mạng | đủ trong ảnh |
| m-1 `HUE_SITE=:80` + cookie Secure ⇒ mất nhớ hội thoại không báo | dòng ⚠ trong `compose.yml` | — |
| m-2 ghim Caddy + thử lại XFF giả | `caddy:2.11.7@sha256:36c24ad91a7f…` — v2.11.7 phát hành 03/10/2026 (tra `data/tra_cuu_cli/2026-11-10_caddy-ban/`, WebFetch GitHub release kiểm: 03 Oct, không pre-release; v2.11.9 = 05/11 chưa đủ 2 tuần) | stack với Caddy ghim: hết lượt + `X-Forwarded-For` giả ⇒ **429**; log 0 câu hỏi, 0 IP |

Build lại 4 s (cache, chỉ thêm 1 lớp). Đếm lại ảnh: kho 204 md · `*sealed*` 0 · `*backup*` 0 · ảnh `rieng` 0 · `.env` 0. Đã `down -v`, xoá thư mục chạy thử. Tiền thêm ≈ 0,0004
(1 câu). **Checklist AWS (thêm):** `HUE_SITE` = tên miền https hoặc `<IP>.sslip.io`, không để `:80`. Ảnh trên máy: `dep10b` (dùng), `dep10` (cũ, xoá được), `nhap2`.
