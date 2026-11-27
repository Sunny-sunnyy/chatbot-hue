# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 09:57 27/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã hoàn tất cả **2 đợt `/swarm`** sáng 27/11/2026 (`b`, `c`, `e`, `monitor`; `0 USD` AWS, tổng `0,00705963 USD` OpenAI).

## 2. Đã xong trong sáng 27/11
- **Đợt 1 (`a3d1aed0`, `21843ed2`, `372145b6` — `0,00706 USD` OpenAI):** đồng bộ `deploy/` + spec 26/11, vá Terraform `1_nen_tang`/`2_may_chu` + `hue-rag-deploy-policy.json`, cắt 13 gói dev ở `pyproject.toml`, bảo vệ `Caddyfile`/`compose.yml`, xây `smoke_eval.py`; `e` kiểm thật `terraform validate`, ảnh `hue-rag-app:21843ed` (`3,49 GB`), `thu_o_may.sh` cổng `8880` (1 câu OpenAI thật `200`), và `smoke_eval` **14/14 PASS**.
- **Đợt 2 (`9c385952` — `0 USD`):**
  - `b` sửa & `e` kiểm chứng độc lập: `RLock` quanh `FullCorpusDenseRunner` / `OpenRouterDenseRunner` + chuyển 3 chỗ `context_builder.build` sang `asyncio.to_thread` (benchmark 8 luồng song song giảm `wall` **-38% đến -45,5%**, `/health` max `47,97 → 12,54 ms`); `gioi_han.py` tính trọng số `chat=1`, `so_tay=10`, `ho_so=8`; `Caddyfile` bỏ gzip `/api/so_tay` & `/api/ho_so`; `dong_goi.sh` thêm `HUE_MO_SO_TAY_HO_SO=0` mặc định; `thu_o_may.sh` kiểm `GET /` CSP; pytest **96 passed**.
  - `c` viết & `e` đối chiếu 100%: `data/nghien_cuu_2026-11-27/KIEM_TOAN_PRODUCTION_LOCAL.md` (Prompt Caching thật trên `application.log`: `16/63` lượt = `28,89%` cached tokens, lộ lỗi trung bình thiếu `CancelScope(shield=True)` thu hồi task ở `so_tay.py`/`ho_so.py` và thiếu `--timeout-graceful-shutdown`) và `NGHIEN_CUU_AGENTIC_HARNESS_TOOLS_2026.md` (4 nâng cấp Harness + 4 Tool mới phù hợp).

## 3. Đang làm / còn mở
- Không còn việc dở; chờ Hiếu đọc tóm tắt kết quả đợt 2 và chọn hướng tiếp theo (hoặc dừng gọn & dọn 3 nhánh tạm đã gộp `p16-b-deploy-tf-docs`, `p16-c-docker-smoke-eval`, `p17-b-async-retrieval-limit`).

## 4. Điểm cần kiểm / quyết định chờ chủ dự án
- Chọn có làm tiếp một trong các đề xuất tiếp theo (vd sửa `CancelScope` ở `so_tay`/`ho_so` + graceful shutdown, Blue-Green Qdrant Alias, quét CVE/ghim `@sha256`, hay thử nghiệm 1 nâng cấp Harness/Tool/MCP) hoặc kết phiên gọn & dọn nhánh.

## 5. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.540 điểm**.
- **Cổng `8010`, `8038`, `8880`:** đều đang TRỐNG.
- **Chi phí OpenAI sáng 27/11:** **`0,00705963 USD`** (đợt 2 dùng `0 USD`; lũy kế phần test của nhóm ~**0,75 USD** / trần **2–2,5 USD**).

## 6. Môi trường / Lưu ý kỹ thuật khi chạy lệnh
- Ảnh Docker `hue-rag-app:21843ed` dựng ở đợt 1 chưa gồm bản sửa `9c385952` — trước khi đóng gói deploy thật cần chạy lại `deploy/docker/dung_anh.sh origin/main`.
