# Việc đang mở (sổ việc — cập nhật 09:07 27/11/2026)

*Mỗi đầu việc có: **làm để chốt gì** · **ai làm** · **tới đâu** · **chỗ lưu**. Quy trình nhiều phiên: `session_prompt/WORKFLOW.md`. Việc đã xong chép 1 dòng sang `session_prompt/VIEC_DA_XONG.md`.*

## A. Sản phẩm & Vận hành

### A.1. Đã hoàn tất đợt sáng 27/11/2026 (Gói A `deploy/` + Docker + `smoke_eval`, chờ Hiếu chốt hướng tiếp)
- **Trạng thái:** đã xong trọn gói sáng 27/11 qua `/swarm` (`b`, `c`, `e`, `monitor`; `0 USD` AWS, `0,00706 USD` OpenAI): gộp `a3d1aed0` (Terraform `1_nen_tang`/`2_may_chu`, IAM policy, đồng bộ `deploy/` + spec 26/11) và `21843ed2` (`pyproject.toml` cắt 13 gói dev khỏi runtime, `Caddyfile` security headers + cache + mẫu `basic_auth`, `compose.yml` + `thu_o_may.sh`, `backend/evaluation/smoke_eval.py`). `e` đã kiểm thật trên `21843ed2`: `terraform validate` 2 tầng đạt, `dung_ngu_canh --chi-kiem` đủ 11 file, ảnh Docker mới `hue-rag-app:21843ed` **3,49 GB** (giảm `0,13 GB`), `thu_o_may.sh` cổng `8880` (`USER hue`, `cap_drop: [ALL]`, headers, 1 câu OpenAI thật `200`), và `smoke_eval` 14/14 PASS (`report_agent/2026-11-27/TONG_HOP.md`).
- **Hướng có thể bàn tiếp khi Hiếu muốn (chưa mở):**
  - Đo thử tải thực tế xem `e5-small` CPU có làm nghẽn event loop FastAPI khi nhiều người hỏi cùng lúc không (`0 USD`, theo `BAN_DO_PRODUCTION_2026-11-26.md` mục 4).
  - Nâng cấp cập nhật kho không downtime bằng Blue-Green + Qdrant Collection Alias.
- **Vẫn gác (chờ chủ dự án tự mở lại):**
  - Thuê GPU + huấn luyện model nhận ảnh (gác theo lời chủ dự án 15:17 & 20:50 25/11; gói `data/anh_huan_luyen_2026-11-24/goi_may_thue.tar` 3,3 GB giữ nguyên).
  - Bước triển khai thực tế lên AWS (`deploy/`): chờ chọn tên miền/IP, email cảnh báo tiền, trần lượt/ngày.

### A.2. Nợ kỹ thuật nhỏ (gom làm khi sửa file liên quan, không mở đợt riêng)
- **Độ dài tên trong gói deploy `gpt-6-luna`:** kiểm lại chỗ cắt tên hoặc chữ dài nếu phát hiện trong thực tế (E ghi chú sau rà).
- **Chuẩn hoá 1–2 dòng docstring/comment nhỏ** còn dư từ đợt rà B (`ho_so_chu_de` / `sua_lich_hoan_tac`) nếu có dịp chạm file.

### A.4. Nhánh Git đang giữ (sau đợt dọn sạch tối 26/11 — còn `main` + 9 nhánh giữ)
- **Đã gộp lên `main` (26/11):** `origin/p15-d-don-giao-trinh-2511` (`06670463` → `b803b6fc`), bổ sung 4 bài kho + ảnh *Lễ Kỳ yên*, đồng bộ giáo trình + runbook + sổ trạng thái.
- **Nhánh hồ sơ / bản thử còn giữ đối chiếu (9 nhánh):** `thu-b-mo-doc-tiep` · `thu-c-khung-truoc` · `thu-b-ba-duong-tim` · `thu-b-dem-loi-dan` · `p9-b-dem-y-go-tat-2` · `p9-c-ve-loi-nho` · `p9-c-sua-2-het-vong` · `p9-b-vong-cuoi-chu-2` · `p9-e-chi-sang-len-ke-hoach`. Toàn bộ nhánh đã gộp và nhánh nháp cũ không còn dùng đã được xoá sạch.

## B. Chỉ số nền & Trần OpenAI của nhóm
- **Model viết mặc định (từ 15:41 25/11):** `gpt-6-luna` (`full_corpus_generation.provider: openai`).
- **Tính năng (`backend/config/settings.yaml`):** **62 MỞ · 6 TẮT** (`anh.bat` + 61 cờ mở / 6 cờ tắt trong `assistant:`, sau khi gỡ sạch `vi_sao`).
- **Kho & Chỉ mục Qdrant (`hue_full_corpus_7a2_e5_small_384`):** **269 bài · 9.540 đoạn** (cập nhật 26/11; Khám phá **269/269** có ảnh).
- **Cả bộ test (`c2d0ee68` + chạy kiểm lại sau đợt sửa 17:13 25/11 + 26/11):** nền đầy đủ **101 file · 4 bỏ · 97 chạy · 2.397 ca đạt · 0 file đỏ** (`data/test_rong_2026-11-22/KET_QUA_c2d0ee68.tsv`); sau đợt sửa 17:13 25/11 chạy 8 file (`111 passed`); sau đợt sửa kho & ảnh 26/11 chạy 4 file chạm (`86 passed`).
- **Chi phí OpenAI phần test của nhóm:** **~0,75 USD** (`0,66` đo bù 23/11 + `0,008213` Playwright C + `0,000572` kiểm `main` A + `0,0051` 5 lượt `/api/chat` kiểm khói 25/11 + `0,0665833` lượt bộ câu kín & N trên `ea96e47c` + `0,00705963` kiểm Docker `:8880` & `smoke_eval` 27/11) / trần **2–2,5 USD** (không tính phần chủ dự án tự test, lời chủ dự án 15:44 25/11).
