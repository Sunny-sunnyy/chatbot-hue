# Việc đang mở (sổ việc — cập nhật 20:56 26/11/2026)

*Mỗi đầu việc có: **làm để chốt gì** · **ai làm** · **tới đâu** · **chỗ lưu**. Quy trình nhiều phiên: `session_prompt/WORKFLOW.md`. Việc đã xong chép 1 dòng sang `session_prompt/VIEC_DA_XONG.md`.*

## A. Sản phẩm & Vận hành

### A.1. Không còn việc xây ở local (đã chốt dừng phần xây ở local 20:50 25/11 & dọn xong phần tồn 26/11)
- **Trạng thái:** đã đóng trọn mốc local (`ea96e47c`), hoàn thiện 3 việc tối 25/11 (`bad77d14`, `bee77a0a`, `d2ebb8f8`), và hoàn tất đợt dọn gọn tối 26/11 (0 USD API): review chéo & gộp nhánh dọn 8 bài giáo trình (`b803b6fc`) kèm sửa 4 finding của người kiểm; ghép ảnh minh hoạ tạm cho *Lễ Kỳ yên đình làng Huế* đưa Khám phá đạt **269/269 (100 %)**; bổ sung giờ mở cửa trung thực cho 4 bài kho còn thiếu + cập nhật chỉ mục Qdrant riêng (**9.540 đoạn**, 86 test liên quan đạt); đồng bộ `RUNBOOK_BAN_GIAO.md` & sổ trạng thái; ghi kỷ luật commit/push chuyên nghiệp lên `main`; dọn sạch worktree và nhánh Git cũ.
- **Gác (chờ chủ dự án tự mở lại):**
  - Thuê GPU + huấn luyện model nhận ảnh (gác theo lời chủ dự án 15:17 & 20:50 25/11; gói `data/anh_huan_luyen_2026-11-24/goi_may_thue.tar` 3,3 GB giữ nguyên).
  - Bước triển khai thực tế (`deploy/`): chờ chọn tên miền/IP, email cảnh báo tiền, trần lượt/ngày (đã đủ guide `0 → 7` và Terraform trên `main`).

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
- **Chi phí OpenAI phần test của nhóm:** **~0,74 USD** (`0,66` đo bù 23/11 + `0,008213` Playwright C + `0,000572` kiểm `main` A + `0,0051` 5 lượt `/api/chat` kiểm khói 25/11 + `0,0665833` lượt bộ câu kín & N trên `ea96e47c`; đợt 26/11 dùng **0 USD**) / trần **2–2,5 USD** (không tính phần chủ dự án tự test, lời chủ dự án 15:44 25/11).
