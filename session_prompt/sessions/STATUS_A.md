# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 10:55 27/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã hoàn tất trọn **3 đợt `/swarm`** sáng 27/11/2026 (`0 USD` AWS, tổng `0,00705963 USD` OpenAI), dọn sạch 4 nhánh tạm đã gộp, đóng `/swarm` gọn, và ghi nhận chốt dừng mở rộng `hue_rag` + đóng hẳn hướng thuê GPU fine-tune model nhận ảnh.

## 2. Đã xong trong sáng 27/11
- **Đợt 1 (`a3d1aed0`, `21843ed2`, `372145b6` — `0,00706 USD` OpenAI):** đồng bộ `deploy/` + spec 26/11, vá Terraform `1_nen_tang`/`2_may_chu` + `hue-rag-deploy-policy.json`, cắt 13 gói dev ở `pyproject.toml`, bảo vệ `Caddyfile`/`compose.yml`, xây `smoke_eval.py`; `e` kiểm thật `terraform validate`, ảnh `hue-rag-app:21843ed` (`3,49 GB`), `thu_o_may.sh` cổng `8880` (1 câu OpenAI thật `200`), và `smoke_eval` **14/14 PASS**.
- **Đợt 2 (`9c385952`, `7da121b2` — `0 USD`):** `RLock` cho `e5-small` + tách `context_builder.build` sang `asyncio.to_thread` (benchmark 8 luồng giảm `wall` **-38% đến -45,5%**, `/health` max `47,97 → 12,54 ms`), `gioi_han.py` tính trọng số (`chat=1 / so_tay=10 / ho_so=8`), `Caddyfile`/`dong_goi.sh`/`thu_o_may.sh`, pytest **96 passed**; 2 báo cáo kiểm toán & nghiên cứu tại `data/nghien_cuu_2026-11-27/` (`e` đối chiếu 100%).
- **Đợt 3 (`19cbb878`, `8244747a` — `0 USD`):** bọc `anyio.CancelScope(shield=True)` ở `so_tay.py` & `ho_so.py` thu hồi sạch task con khi client ngắt SSE; thêm `--timeout-graceful-shutdown 15` (`stop_grace_period: 20s`) ở `Dockerfile`/`compose.yml`; 2 test hồi quy mới (`56 passed`, `docker compose config` hợp lệ); dọn sạch 4 nhánh tạm sáng 27/11 và worktree swarm.
- **Chốt cuối (`10:55 27/11`):** ghi nhận đóng hẳn mở rộng `hue_rag`, đóng hẳn thuê GPU fine-tune model nhận ảnh, bỏ `MCP Server`.

## 3. Đang làm / còn mở
- Không còn việc xây hay việc tồn mở ở local. Chỉ còn bước triển khai thực tế lên AWS (`deploy/`) gác chờ Hiếu tự mở lại khi rảnh. (Thuê GPU fine-tune model ảnh **đã đóng hẳn**.)

## 4. Điểm cần kiểm / quyết định chờ chủ dự án
- Không còn quyết định treo. Lưu ý khi đóng gói deploy thật sau này cần chạy lại `deploy/docker/dung_anh.sh origin/main` để ảnh mang đủ bản sửa `9c385952` + `19cbb878`.

## 5. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8010`, `8038`, `8880`:** đều đang TRỐNG.
- **Chi phí OpenAI sáng 27/11:** **`0,00705963 USD`** (lũy kế phần test của nhóm ~**0,75 USD** / trần **2–2,5 USD**).

## 6. Môi trường / Lưu ý kỹ thuật khi chạy lệnh
- Trong sandbox mặc định, `.git/` và loopback `127.0.0.1:6335` không mở ghi/nối nên các thao tác git ghi (`merge/commit/push/branch`) và lệnh đụng Qdrant chạy bằng `BypassSandbox: true`.
