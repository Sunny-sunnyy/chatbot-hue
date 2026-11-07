# E-dep — chuẩn bị deploy lát mỏng (12:38 07/11/2026)

Việc A giao: chỉ chuẩn bị + đề xuất. **Chưa** tạo tài khoản, chưa `docker build`, chưa sửa `backend/`. Tiền: **0,000953 USD** (3 câu đo RAM) + Codex tra web 0.
Nhãn: **[Chạy]** đo / chạy thật · **[Web]** trang AWS E đã tự mở (WebFetch) · **[Codex]** chỉ Codex tra, E chưa kiểm · **[Suy]** suy luận.

## 1. Số đo RAM trên máy User [Chạy]

Server tạm `uvicorn` cổng 8851, `HF_HUB_OFFLINE=1`, cờ như `main` (ảnh tắt). C xác nhận lúc đó không đo latency. Server đã tắt bằng TaskStop.

| | RSS |
|---|---|
| App lúc chờ (`/health` 5 / 5 ready) | **1,49 GB** |
| App sau 3 câu (1 câu kho, 1 câu kho có tìm thêm, 1 câu ngoài phạm vi) | **1,51 GB** (tăng ~20 MB) |
| Qdrant (`docker stats`) | **378 MiB** |

Ba câu đều HTTP 200: 4,2 s · 7,3 s · 1,6 s. Có 3 dòng `chat_metrics` mới, câu hỏi không xuất hiện trong log.

⇒ App + Qdrant ≈ **1,9 GB**, chưa tính hệ điều hành, Docker, Caddy. **Máy 2 GB không đủ; cần 4 GB** [Suy]. Phần lớn RAM là torch + e5-small. Nếu bật giọng nói (+~300 MB model) hoặc ảnh thì cần đo lại.

## 2. Nháp `data/phase_12/deploy_nhap/` (chưa build)

- **`Dockerfile`** gồm 2 bước:
  - (1) `node:24` chạy `npm ci && npm run build` ⇒ `frontend/dist`.
  - (2) `python:3.13-slim` + uv 0.12.5:
    - `uv export` từ `uv.lock`, **lọc 15 gói `nvidia-*` + 3 `cuda-*` + `triton`**, rồi `uv pip install --torch-backend cpu`. Lý do: `.venv` máy User là torch `2.13.0+cu130`; [Chạy] đã thấy các gói CUDA này trong `uv export`.
    - Tải e5-small đúng revision `614241f6…` (runtime chỉ nạp model này — `embedding/full_corpus.py:45`), chỉ file cần (~470 MB; cache máy User 2,2 GB vì có onnx / openvino).
    - Tải sẵn `tiktoken o200k_base`.
    - Chép `backend/`, kho runtime và build record — runtime so hash kho lúc khởi động.
- **`compose.yml`**: qdrant (cùng digest v1.18.3, nghe 6335 bên trong) + app + Caddy.
  - App dùng `network_mode: service:qdrant`, vì `settings.yaml` viết cứng `localhost:6335` ⇒ **không sửa code**. Cách sạch hơn: một dòng đọc `QDRANT_URL` (việc của B).
  - Khoá API chỉ nằm trong `.env` (quyền 600) trên máy, không vào ảnh.
- **`Caddyfile`**: HTTPS tự động (Let's Encrypt), dùng `<IP>.sslip.io` nếu không mua tên miền; `flush_interval -1` cho luồng SSE.
- ⚠ **Ảnh chứa kho private ⇒ không đẩy lên registry công khai.** Build ngay trên máy deploy, hoặc chuyển bằng `docker save | ssh`. Cần thêm `.dockerignore` (danh sách ở cuối `Dockerfile`).
- Ảnh ước ~2–2,5 GB [Suy]. Lý do: `pyproject.toml` còn `jupyter`, `gradio`, `pytest` trong phụ thuộc chính; có thể chuyển sang nhóm dev.

## 3. Chọn máy AWS (Singapore, ~2 tháng 12/2026 – 01/2027)

| Lựa chọn | vCPU / RAM | USD / tháng | Ghi chú |
|---|---|---|---|
| **Lightsail Linux 4 GB** | 2 / 4 GB | **24** [Web] | Gồm 80 GB SSD, 4 TB truyền, IPv4. Đơn giản nhất. |
| EC2 t3.medium | 2 / 4 GiB | ~38 + IPv4 ~3,65 + EBS [Codex] | Đắt hơn, không lợi gì cho demo. |
| EC2 free plan: `c7i-flex.large` / `m7i-flex.large` | 2 vCPU / 4 / 8 GiB [Suy theo dòng máy] | trừ vào credit | Tài khoản tạo từ 15/07/2025 được **100 USD + tối đa 100 USD** credit, kéo dài **6 tháng** hoặc tới khi hết credit [Web]. Hai loại này có tên trong danh sách "Free tier eligible" [Web]; t3.small / t4g.small (2 GiB) cũng có nhưng **không đủ RAM**. |

- ⚠ Free plan hết hạn ⇒ AWS **đình chỉ tài khoản, mất truy cập tài nguyên**; giữ dữ liệu 90 ngày [Web]. Tài khoản tạo ngay bây giờ (11/2026) hết hạn khoảng 05/2027 ⇒ vẫn qua kỳ bảo vệ.
- Giá giờ của c7i / m7i-flex ở Singapore: **chưa kiểm** — cần AWS Pricing Calculator để biết credit dùng được bao lâu.
- Khoá: `.env` quyền 600 là đủ cho một máy demo. Parameter Store Standard 0 USD; Secrets Manager 0,40 USD / khoá / tháng [Codex].
- HTTPS: Caddy + tên miền hoặc sslip.io. Lightsail load balancer có HTTPS nhưng tốn **18 USD / tháng** [Codex].
- AWS Budgets: cảnh báo miễn phí, nhưng **không phải trần cứng** [Codex].

**Đề xuất [Suy]:** **Lightsail 4 GB, 24 USD / tháng** (≈ 600.000 đồng; khoảng 48 USD cho 2 tháng) nếu User muốn đơn giản, chắc chắn.

## 4. Việc bắt buộc trước khi đưa link công khai

| # | Việc | Hiện trạng | Cách nhỏ nhất |
|---|---|---|---|
| 1 | **Trần tiền / giới hạn lượt** | Không có giới hạn nào (`backend/api/routes/chat.py` `/api/chat`, `/api/chat/stream` — [Chạy] grep 0 kết quả) | (a) **Đếm lượt / ngày trong RAM**, vượt N ⇒ 429 (~15 dòng, một chỗ cho cả 2 route); (b) **khoá OpenAI riêng cho deploy**, đặt hạn mức chi tiêu ở dashboard OpenAI; (c) Serper dùng gói trả trước ⇒ tự có trần. Chặn theo IP chỉ nên thêm khi (a) chưa đủ. |
| 2 | Kiểm `Host` | Không kiểm | Caddy chỉ phục vụ đúng một tên miền và app không mở cổng ra ngoài ⇒ đã đủ, không cần code [Suy]. |
| 3 | Tra web (Serper) trên máy công khai | `settings.yaml` `tra_web: true` | Spec Phase 9 review v10 M-1: **tắt mặc định trên AWS** tới khi xét lại điều khoản + hạn mức ⇒ bản deploy để `tra_web: false`, hoặc User quyết bật. |
| 4 | `/api/kham_pha/bai` trả toàn văn bài kho | Chưa có trên `main` (thuộc S1 D6); spec đợt 1 ghi "trước deploy: xét lại" | User quyết: kho là nội dung sản phẩm ⇒ chấp nhận công khai và để giới hạn lượt ở #1 bọc chung. Không thêm rào riêng. |
| 5 | Cookie `Secure` | `chat.py:153–154` `secure=False` (chạy http://127.0.0.1) | Một cờ trong `settings.yaml`, bật khi chạy HTTPS. |
| 6 | Trang `/docs`, `/openapi.json` của FastAPI | Mặc định đang mở (`app.py` `FastAPI(...)` không truyền `docs_url`) | `docs_url=None, openapi_url=None` khi deploy (1 dòng). |
| 7 | Xoay log | `config/logging.yaml` `FileHandler`, không xoay; log hiện 0,53 MB sau khoảng 1 tuần | `RotatingFileHandler` 10 MB × 3 (chỉ sửa cấu hình) + compose `logging: max-size`. Ưu tiên thấp. |
| 8 | Một tiến trình | Kho cuộc trò chuyện + mã 👍/👎 nằm trong RAM | Giữ `--workers 1` (đã ghi trong `Dockerfile`); khởi động lại ⇒ mất lịch sử cuộc, chấp nhận được cho demo. |
| 9 | Proxy + scheme | Route ảnh so `Origin` với `scheme://netloc` (`anh.py:78`) | uvicorn `--proxy-headers --forwarded-allow-ips '*'` (đã ghi). Ảnh đang tắt. |

## 5. Lát mỏng một ngày — đề xuất [Suy]

1. **User (~30 phút):**
   - tạo tài khoản AWS + bật cảnh báo Budgets 10 USD;
   - tạo khoá OpenAI riêng có hạn mức;
   - chọn máy (đề xuất Lightsail 4 GB).
2. **B (nhánh nhỏ, ~2 giờ):** làm #1 (a), #5, #6, `.dockerignore`, cấu hình `tra_web: false` cho bản deploy. Review: C.
3. **A xếp lịch một lần build trên máy User** (nặng RAM / đĩa ⇒ không chạy song song việc khác):
   - `docker build` + `compose up` cục bộ;
   - `/health` 5 / 5, 1 câu trong kho + 1 câu ngoài kho.
4. **Lên máy:**
   - chép `qdrant_storage` (51 MB) + `.env`, build trên máy;
   - Caddy với sslip.io;
   - chạy lại bước 3 + 10 câu đo latency trên máy thật (≤ 0,005 USD).
   - Đây là mốc "đã chạy trên AWS" sớm. Đợt 2 / B7 deploy lại bằng cùng lệnh.

**Chưa kiểm / rủi ro còn mở:**
- `uv pip install --torch-backend cpu` với danh sách đã lọc: chưa chạy thử.
- Giá c7i / m7i-flex: chưa có.
- Latency trên máy 2 vCPU: chưa đo. e5 trên CPU yếu hơn có thể kéo p95 > 5 s.
