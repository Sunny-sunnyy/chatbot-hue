# Review: chuẩn bị deploy — chạy thử bản deploy trên máy (B, 10/11)

Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-4f`) · 10/11/2026 · A giao (một vòng, chỉ chỗ rủi ro; không build lại, không lượt có phí). Đối tượng: report
`b_deploy_cuc_bo_implementation.md` (`main` `1fb6ae9`), nhánh `p12-deploy-nhap` `8d650ad`, nháp private `data/phase_12/deploy_nhap/` (`compose.yml`, `Caddyfile`,
`Dockerfile`, `Dockerfile.dockerignore`, `dung_dockerignore.py`), ảnh `hue-rag-app:dep10`. Repo public: không chép tên file kho.

## 1. Phạm vi đã review

- Code nhánh: `git diff main..8d650ad -- backend` = 2 file cũ (`core/settings_loader.py` `apply_env_overrides`: `HUE_QDRANT_URL`, `HUE_TRA_WEB` có kiểm giá trị; `tests/test_settings_env.py`).
- Nháp deploy: đọc đủ `compose.yml`, `Caddyfile`, `Dockerfile`, `Dockerfile.dockerignore`.
- Bốn câu A giao: (1) ảnh không chứa file private · (2) `--forwarded-allow-ips '*'` + Caddy · (3) 3 biến chốt · (4) report không lọt nội dung private.

## 2. Findings

**Blocker:** không.

**M-1 (major) · hỏi bằng ảnh tắt im lặng trên bản deploy** — `settings.yaml` `anh.bat: true` (User bật 08/11), nhưng ảnh Docker không có
`data/phase_10/anh/danh_sach_ten.json` (danh sách chừa chỉ 3 file `data/`; file này không tracked) ⇒ `api/app.py:186-194` bắt lỗi nạp danh sách ⇒ log
`Image route startup failed` ⇒ `app.state.anh = None` ⇒ route 404, `/api/tinh_nang` báo `anh: false` (report §2 ghi quan sát này nhưng không nói nguyên nhân, và §3 không có câu cho User).
- Tác động: bản công khai thiếu một tính năng User đã bật mà không ai quyết; mỗi lần khởi động có một dòng log lỗi. Bật trên bản công khai còn là một quyết định riêng
  (ảnh người dùng gửi OpenAI — giống câu `tra_web`).
- **Đóng:** thêm câu cho User ở report §3 ("hỏi bằng ảnh trên bản công khai: bật ⇒ chừa thêm `danh_sach_ten.json` vào ảnh; tắt ⇒ đặt tắt **rõ ràng**") và làm theo
  một trong hai: (a) chừa file vào `dung_dockerignore.py` + `COPY`; hoặc (b) tắt rõ (biến môi trường kiểu `HUE_TRA_WEB`, hoặc ghi chú trong `compose.yml`) để không còn
  dòng log lỗi. Mặc định đề xuất: (b) tới khi User trả lời — cùng cách đang làm với `tra_web`.

**Minor:**
- **m-1 · mặc định không khớp nhau:** `HUE_SITE` mặc định `:80` (http) nhưng `HUE_COOKIE_SECURE` mặc định `1` ⇒ chạy compose mà quên đặt `HUE_SITE` thì trang vẫn chạy
  qua http, còn cookie `Secure` không được gửi ⇒ **mất nhớ hội thoại không báo lỗi**. Ghi chú trong `compose.yml` đã nói cho bản thử cục bộ. Đóng: thêm 1 dòng vào
  checklist deploy AWS ("đặt `HUE_SITE` = tên miền / `<IP>.sslip.io` — thiếu ⇒ http + mất nhớ"), không cần đổi code.
- **m-2 · `caddy:2` chưa ghim digest** (đã có ghi chú "ghim khi deploy thật"). Lý do `'*'` (§2 dưới) dựa vào Caddy **không** tin `X-Forwarded-For` từ client khi không
  khai `trusted_proxies` — hành vi của Caddy 2 bản mới. Đóng: khi ghim, chạy lại đúng một phép thử "hết lượt + `X-Forwarded-For` giả ⇒ vẫn 429" (B đã có lệnh).

## 3. Trả lời bốn câu A giao

| # | Câu | Kết luận | Bằng chứng |
|---|---|---|---|
| 1 | Ảnh không chứa file private | **Đạt** | C đếm lại [Chạy, `docker run --rm --name c_kiem_anh --network none --entrypoint bash hue-rag-app:dep10`]: kho `.md` 204 (= build record) · kho mọi file 205 (+ file điều kiện) · `*sealed*` **0** (cả `/`) · `.env` 0 · `*backup*` 0 · `anh/rieng` **0** · `data/` đúng 3 file (build record, sparse state, bảng điểm v3) · `backend/` 107 file, 0 `__pycache__`, 0 log · đường dẫn "evaluation" / "golden" ngoài `.venv`: 6, đều là code + test đã có ở repo công khai (`backend/evaluation/*`, `tests/test_golden_full_corpus.py`) · ảnh giao diện `frontend/dist/anh` 14 = `git ls-files frontend/public/anh` 14. Giai đoạn `web` chỉ đưa `dist/` vào ảnh cuối |
| 2 | `--forwarded-allow-ips '*'` | **Lý do đứng** | `compose.yml`: service `app` **không** có `ports` ⇒ chỉ container trong mạng compose tới được (Caddy, Qdrant); IP Caddy trong mạng compose không cố định ⇒ ghi IP cố định khó. Lỗ còn lại (client giả `X-Forwarded-For`) B đã thử thật qua Caddy ⇒ vẫn 429. Một tiến trình uvicorn (không `--workers`) ⇒ sổ đếm lượt RAM đúng một sổ. Điều kiện giữ: không ai thêm `ports` cho `app` (report §4 đã ghi) + m-2 |
| 3 | 3 biến chốt | **Đạt** | `HUE_LUOT_MOI_NGAY: ${…:-50}` · `HUE_COOKIE_SECURE: ${…:-1}` · `HUE_TAT_DOCS: "1"` (cố định) trong `environment` của `app`; `HUE_TRA_WEB: "false"`, `HUE_QDRANT_URL` đúng cổng gốc Qdrant. Log xoay vòng nằm trong `logging.yaml` (luôn bật) + `json-file` 10 MB × 3 cho stdout. Test nhánh: C chạy lại `test_settings_env.py` + `test_chot_deploy.py` **11 passed** (7,7 s). Lưu ý m-1 |
| 4 | Report không lọt nội dung private | **Đạt** | report chỉ ghi số đếm, đường dẫn thư mục, tên cờ; không tên file kho, không câu hỏi / câu trả lời (2 câu thử ghi "tự viết", không chép), không khoá, không IP |

## 4. Giới hạn hoặc phần chưa chạy

Không build lại, không `compose up` lại, không gọi API (A giao). HTTPS thật chưa ai thử (report §4). Chưa đo cỡ ảnh nén.

## 5. Decision và bước tiếp theo

**`changes_requested`** — 0 blocker, **1 major (M-1: thêm câu cho User + chọn (a) / (b))**, 2 minor (ghi checklist). Phần còn lại đạt. Sửa nhỏ, 0 USD; không cần build lại để
đóng M-1 nếu chọn (b) bằng ghi chú + câu cho User (build lại khi deploy thật).

## 6. Xem delta sau sửa (report §5, 20:03 10/11/2026)

- **M-1 (a, A chọn):** `dung_dockerignore.py` + `Dockerfile.dockerignore` chừa `data/phase_10/anh/danh_sach_ten.json`, `Dockerfile` thêm `COPY`. C đếm lại ảnh `hue-rag-app:dep10b`
  [Chạy, `--network none`, `--rm --name c_kiem_anh3`]: `data/` đúng **4** file (thêm danh sách tên) · kho `.md` 204 · `*sealed*` 0 · `.env` 0 · `anh/rieng` 0 · `*backup*` 0.
  B chạy: `anh: true`, route trả 415 với thân rỗng (không 404), log "Image route enabled" 1 / "startup failed" 0. Rà file runtime theo cờ bật: đủ — **đóng**.
- **m-1:** dòng ⚠ `HUE_SITE` trong `compose.yml` (cạnh 3 biến chốt) + dòng checklist AWS — **đóng**.
- **m-2:** `caddy:2.11.7@sha256:36c24ad91a7f…`; digest khớp ảnh trên máy (`docker image inspect` RepoDigests); B chạy lại "hết lượt + `X-Forwarded-For` giả ⇒ 429" với bản ghim — **đóng**.

**Decision cập nhật: `ready_for_user_confirmation`** — 0 blocker, 0 major, 0 minor mở. Còn câu cho User ở report §3 (tra web, ảnh #5, số lượt, khoá / máy AWS / tên miền, xoá ảnh cũ).
