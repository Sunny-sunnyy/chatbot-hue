# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 09:07 27/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã hoàn tất đợt `/swarm` sáng 27/11/2026 (`b`, `c`, `e`, `monitor`; `0 USD` AWS, `0,00705963 USD` OpenAI) cho Gói A chuẩn hoá bộ `deploy/` + Docker + lệnh `smoke_eval` rẻ.

## 2. Đã xong trong đợt sáng 27/11 (`0 USD` AWS · `0,00706 USD` OpenAI)
- **Gộp nhánh `b` (`origin/p16-b-deploy-tf-docs` @ `ab6b7419` → `main` `a3d1aed0`):** vá `deploy/terraform/1_nen_tang/main.tf` (`aws_sns_topic_policy`, `aws_s3_bucket_lifecycle_configuration` 3 ngày) và `deploy/terraform/2_may_chu/` (EventBridge Scheduler tự dừng EC2 23:30 giờ VN + IAM role riêng + biến bật/tắt); cập nhật `deploy/guides/hue-rag-deploy-policy.json` (kèm finding #7 `cloudwatch:GetMetricStatistics`); đồng bộ toàn bộ `deploy/README.md`, `deploy/docker/README.md`, `deploy/guides/0..7` (thêm `CPUCreditBalance`), spec `2026-11-23-deploy-aws-design-ban-3.md`.
- **Gộp nhánh `c` (`origin/p16-c-docker-smoke-eval` @ `a64c0efc` → `main` `21843ed2`):** chuyển 13 gói dev/test/notebook khỏi runtime ở `pyproject.toml` + `uv.lock` (`--no-dev` giảm 706 → 345 dòng); thêm security headers / `Cache-Control` / mẫu `basic_auth` ở `Caddyfile`; thêm `no-new-privileges:true` cho `qdrant` và `mem_limit: 128m` cho `caddy` ở `compose.yml`; cập nhật `thu_o_may.sh`; viết `backend/evaluation/smoke_eval.py` + `backend/tests/test_smoke_eval.py`.
- **Kiểm chứng thật bởi `e` trên `21843ed2`:** `dung_ngu_canh --chi-kiem` đủ 11 file riêng tư · `terraform fmt/init/validate` 2 tầng đạt · `pytest` 8 passed · ảnh `hue-rag-app:21843ed` **3,49 GB** (giảm `0,13 GB` từ `3,62 GB`) · `thu_o_may.sh` cổng `8880` đạt kèm 1 câu OpenAI thật (`0,00058635 USD`) · `smoke_eval` **14/14 PASS** (`0,00647328 USD`, `data/smoke_eval/smoke_eval_20261127_020614.json`).
- **Báo cáo & đồng bộ sổ:** `report_agent/2026-11-27/TONG_HOP.md`, `HIEN_TRANG.md`, `VIEC_DANG_MO.md`, `VIEC_DA_XONG.md`, `CURRENT_HANDOFF.md`, `data/bo_nho_agent/MEMORY.md`.

## 3. Đang làm / còn mở
- Không còn việc xây hay kiểm dở ở đợt sáng 27/11. Hai nhánh tạm đã gộp còn chờ duyệt dọn nếu Hiếu muốn (`origin/p16-b-deploy-tf-docs`, `origin/p16-c-docker-smoke-eval`).
- Các việc gác chờ Hiếu tự mở lại: thuê GPU huấn luyện model nhận ảnh (`goi_may_thue.tar`) và triển khai thực tế lên AWS (`deploy/`). Các hướng bàn tiếp ở `BAN_DO_PRODUCTION_2026-11-26.md`: đo thử tải `e5-small` CPU và Blue-Green Qdrant Alias.

## 4. Điểm cần kiểm / quyết định chờ chủ dự án
- Hỏi Hiếu có cần giữ ảnh `hue-rag-app:21843ed` (3,49 GB) để đóng gói sau hoặc dọn hai nhánh `p16-b-deploy-tf-docs` / `p16-c-docker-smoke-eval` hay không; đồng thời xác nhận hướng tiếp theo nếu muốn làm tiếp hôm nay.

## 5. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8010`, `8038`, `8880`:** đều đang TRỐNG.
- **Chi phí OpenAI đợt 27/11:** **`0,00705963 USD`** (lũy kế phần test của nhóm ~**0,75 USD** / trần **2–2,5 USD**).

## 6. Môi trường / Lưu ý kỹ thuật khi chạy lệnh
- Trong sandbox mặc định, `.git/` và loopback `127.0.0.1:6335` không mở ghi/nối nên các thao tác git ghi (`merge/commit/push/branch`) và lệnh đụng Qdrant chạy bằng `BypassSandbox: true`.
- `thu_o_may.sh kiem` dùng `curl -sI` (`HEAD /`) nhận `405` từ FastAPI; `GET /` xác nhận có đủ `Content-Security-Policy` của FastAPI + security headers của Caddy.
