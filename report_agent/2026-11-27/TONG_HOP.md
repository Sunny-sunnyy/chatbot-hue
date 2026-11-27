# Tổng hợp đợt 27/11/2026 — Chuẩn hoá bộ deploy/Docker (Phương án A) & Lệnh smoke eval rẻ

**Thời gian:** 08:38 – 09:07 27/11/2026 (giờ `date`)  
**Điều phối:** Session A (`agy` CLI + `/swarm` gồm `b`, `c`, `e`, `monitor`)  
**Phạm vi đã duyệt:** Gói A trong `data/x14_deploy_2026-11-23/BAN_DO_PRODUCTION_2026-11-26.md` + 1 câu OpenAI thật qua Docker cổng `8880` + xây và chạy thử 1 lượt lệnh `smoke_eval` (`0 USD` AWS, ~`0,02–0,03 USD` OpenAI).

---

## 1. Kết quả gộp lên `main`
- **`a3d1aed0` (`b` — `origin/p16-b-deploy-tf-docs` @ `ab6b7419`):**
  - `deploy/terraform/1_nen_tang/main.tf`: thêm `aws_sns_topic_policy.alerts` (cho `cloudwatch.amazonaws.com` gọi `sns:Publish` kèm điều kiện `aws:SourceAccount`) và `aws_s3_bucket_lifecycle_configuration.artifacts` (`abort_incomplete_multipart_upload` 3 ngày).
  - `deploy/terraform/2_may_chu/` (`main.tf`, `variables.tf`, `outputs.tf`, `terraform.tfvars.example`, `README.md`): thêm EventBridge Scheduler (`aws_scheduler_schedule.auto_stop`, `cron(30 23 * * ? *)`, `Asia/Ho_Chi_Minh`) + IAM role riêng (`ec2:StopInstances` trên đúng `aws_instance.app.arn`) + biến `auto_stop_enabled` (`true`), `auto_stop_schedule`.
  - `deploy/guides/hue-rag-deploy-policy.json`: thêm quyền `GiaoVaiChoScheduler`, `LichTuDungMayEC2` và `cloudwatch:GetMetricStatistics` trong `XemTrangThai` (bắt qua review chéo của `e`, finding #7).
  - Đồng bộ tài liệu `deploy/README.md`, `deploy/docker/README.md`, `deploy/guides/0..7` (thêm hướng dẫn kiểm `CPUCreditBalance` ở guide `5`), `docs/superpowers/specs/2026-11-23-deploy-aws-design-ban-3.md` sang mốc 26/11 (`gpt-6-luna` mặc định cả local lẫn deploy, `269` bài / `9.540` điểm / `269/269` ảnh, thống nhất `9 + 2 = 11` file riêng tư, gỡ nhắc `vi_sao`).
- **`21843ed2` (`c` — `origin/p16-c-docker-smoke-eval` @ `a64c0efc`):**
  - `pyproject.toml` + `uv.lock`: chuyển 13 gói không dùng trực tiếp ở runtime sang `[dependency-groups] dev` (`uv export --frozen --no-dev` giảm từ **706** xuống **345** dòng).
  - `deploy/docker/Caddyfile`: thêm `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `X-Frame-Options: DENY` (không đặt đè `Content-Security-Policy` của FastAPI), `Strict-Transport-Security` chỉ trên `@https protocol https`, `Cache-Control` cho `/static/assets/*` (`immutable`) và `/static/anh/*`, kèm mẫu `basic_auth` tắt mặc định.
  - `deploy/docker/compose.yml` & `deploy/docker/thu_o_may.sh`: thêm `no-new-privileges:true` cho `qdrant`, `mem_limit: 128m` cho `caddy`, và kiểm `id -u` (`10001`), security headers, `Cache-Control` trong `thu_o_may.sh kiem`.
  - `backend/evaluation/smoke_eval.py` + `backend/tests/test_smoke_eval.py`: lệnh smoke eval 14 ca công khai (0 câu kín `*sealed*`), chấm tất định không dùng LLM judge, hỗ trợ `--dry-run` (có ca đối chứng FAIL).

---

## 2. Kiểm chứng thực tế (`e` trên bản ghép `21843ed2`)
- **Kiểm 0 USD:**
  - `dung_ngu_canh.py --ref HEAD --du-lieu data --chi-kiem`: đủ **9 + 2 = 11** file riêng tư, thiếu `0`.
  - `terraform fmt -check -recursive deploy/terraform/` + `terraform init -backend=false` + `terraform validate` cho `1_nen_tang` và `2_may_chu`: đều hợp lệ.
  - `pytest tests/test_smoke_eval.py tests/test_assistant_boundary.py`: **8 passed** (trước đó `c` chạy thêm `test_static_ui.py` đạt **12 passed**).
  - `smoke_eval --dry-run`: **14/14 PASS**, `control_fail=CAUGHT`.
- **Docker mới & `thu_o_may.sh` cổng `8880`:**
  - Ảnh `hue-rag-app:21843ed`: **3,49 GB** (giảm **0,13 GB** so với `3,62 GB` trước đó), `269` bài kho, `0` file cấm.
  - Ba hộp `healthy` sau `27,7 s`; `app` chạy `UID=10001` (`hue`, `CapDrop=[ALL]`, `no-new-privileges:true`); `qdrant` có `no-new-privileges:true`; `caddy` `mem_limit=128m`; `/` `200` (đủ CSP của FastAPI + header Caddy), `/health` `ok`, `/docs` `404`, `/api/kham_pha` `269 bài`, thân JSON 13 MB `413`, `/static/assets/*.js` có `Cache-Control: public, max-age=31536000, immutable`, nguồn Qdrant 6335 giữ nguyên `9.540` điểm và `0` snapshot thừa.
  - 1 câu OpenAI thật qua Caddy `:8880` (`"Vé tham quan Đại Nội bao nhiêu?"`): `status_code: 200`, `outcome: success`, `model: gpt-6-luna`, `n_cited_sources: 2`, `total_ms: 6885,9 ms`, chi phí **`0,00058635 USD`**. Đã chạy `thu_o_may.sh don` sạch sẽ.
- **Lượt thật `smoke_eval` trên `gpt-6-luna` (cổng `8038`):**
  - Kết quả: **14/14 PASS**, `p50=3614,6 ms`, `p95=5258,0 ms`, chi phí **`0,00647328 USD`**.
  - Dữ liệu chi tiết: `data/smoke_eval/smoke_eval_20261127_020614.json`.
- **Tổng chi phí OpenAI đợt 27/11:** **`0,00705963 USD`** (~`0,0071 USD`); lũy kế phần test của nhóm ~**0,75 USD** / trần **2–2,5 USD**.

---

## 3. Giới hạn / phần chưa chạy
- Toàn bộ thao tác tạo tài nguyên thật trên AWS (`terraform plan/apply`, EventBridge Scheduler, SNS email, HTTPS qua tên miền thật) vẫn ở trạng thái `[chưa kiểm trên AWS]` theo phạm vi `0 USD AWS`.
- Ghi chú `thu_o_may.sh kiem` dùng `curl -sI` (`HEAD /`) ở đợt 1 đã được sửa sang `curl -sD - -o /dev/null` (`GET /`) trong đợt 2 (`9c385952`).

---

## 4. Đợt 2 (09:43 – 09:57 27/11/2026, `0 USD` AWS, `0 USD` OpenAI) — Production Local 1 & Kiểm toán / Nghiên cứu Agentic–Harness
- **Gộp lên `main` (`9c385952`, nhánh `origin/p17-b-async-retrieval-limit`, `e` duyệt `READY`):**
  - `backend/embedding/full_corpus.py`: thêm `threading.RLock` quanh `FullCorpusDenseRunner` (`load`, `embed_documents_matrix`, `embed_queries`, `close`) và `OpenRouterDenseRunner` (`load`, `_embed`) ngăn PyTorch CPU thread oversubscription.
  - `backend/llm/assistant.py`: chuyển 3 lời gọi `context_builder.build(...)` sang `asyncio.to_thread(...)`.
  - `backend/api/gioi_han.py`: thêm `TRONG_SO_DUONG` (`/api/chat`, `/api/chat/stream`, `/api/anh/ung_vien` = `1`; `/api/so_tay` = `10`; `/api/ho_so` = `8`) áp dụng cho cả trần IP và trần tổng, giữ tương thích ngược `cho_qua()` và `tai_file=True`.
  - `deploy/docker/Caddyfile`: bỏ nén gzip cho `/api/so_tay` và `/api/ho_so` (`caddy validate` = `Valid configuration`).
  - `deploy/docker/dong_goi.sh`: thêm tuỳ chọn `HUE_MO_SO_TAY_HO_SO=1` (mặc định `0` cho tới khi kiểm thật trên `gpt-6-luna`); `deploy/docker/thu_o_may.sh`: sửa kiểm `GET /` CSP (`bash -n` đạt).
  - **Số đo kiểm chứng độc lập bởi `e` (`data/nghien_cuu_2026-11-27/bench_event_loop.py`, Qdrant `6335` 9.540 điểm):**
    - `3_concurrent_api_chat_x8`: `wall` `811,13 → 503,24 ms` (`-38%`), `/health` max `47,97 → 12,54 ms` (`p50 2,45 → 1,17 ms`).
    - `4_concurrent_to_thread_search_x8`: `wall` `874,00 → 476,02 ms` (`-45,5%`), `/health` max `21,03 → 5,57 ms`.
    - Pytest 8 file chạm (`HF_HUB_OFFLINE=1`): **96 passed in 29.09s**.
- **2 báo cáo riêng tư của `c` (`data/nghien_cuu_2026-11-27/`, `e` đối chiếu khớp 100% log & `file:dòng`):**
  - `KIEM_TOAN_PRODUCTION_LOCAL.md`: thống kê Prompt Caching thật trên `63` lượt `gpt-6-luna` (`16/63 = 25,40%` lượt trúng, `89.643 / 310.320 = 28,89%` tokens; `sua_lich` `60,83%`, `tro_ly_hue` `28,64%` ở vòng 2+); chỉ ra 2 điểm đáng sửa gọn (`CancelScope(shield=True)` thu hồi task khi client ngắt SSE ở `so_tay.py:148-155` & `ho_so.py:160-169`, và `--timeout-graceful-shutdown` cho `uvicorn`) cùng 4 điểm không nên sửa để tránh over-engineer.
  - `NGHIEN_CUU_AGENTIC_HARNESS_TOOLS_2026.md`: đề xuất 4 nâng cấp Harness (`TurnBudget` + *Actionable Feedback*, tách Fast-path vs Agentic Loop, chuẩn hoá `CancelScope` + graceful shutdown, *Trajectory Eval Gate* `0 USD` + Blue-Green Alias) và 4 tool mới dùng dữ liệu sẵn có (`tinh_ve_va_gio_tham_quan`, `so_sanh_diem_den`, `goi_y_phuong_an_mua_nang`, `tim_tuyen_di_lai`).
