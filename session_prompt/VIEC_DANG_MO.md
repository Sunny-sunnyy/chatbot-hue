# Việc đang mở (sổ việc — cập nhật 22:00 25/11/2026)

*Mỗi đầu việc có: **làm để chốt gì** · **ai làm** · **tới đâu** · **chỗ lưu**. Quy trình nhiều phiên: `session_prompt/WORKFLOW.md`. Việc đã xong chép 1 dòng sang `session_prompt/VIEC_DA_XONG.md`.*

## A. Sản phẩm & Vận hành

### A.1. Không còn việc xây ở local (đã chốt dừng phần xây ở local 20:50 25/11)
- **Trạng thái:** đã đóng trọn mốc local (`ea96e47c`) kèm kiểm khói `gpt-6-luna`, bộ câu kín 1 lần (`report_agent/2026-11-25/E_BO_CAU_KIN_LUNA_2511.md`), đồng bộ 9 file giáo trình, và 3 hoàn thiện gọn tối 25/11 (`bad77d14` rút gọn trang Giới thiệu, `bee77a0a` ghép 7/8 ảnh mới, `d2ebb8f8` cập nhật `README.md` + `bai_hoc/README.md`). Chủ dự án chốt Phương án 2: **dừng phần xây ở local**, chỉ mở lại khi có yêu cầu mới.
- **Việc nhỏ đang gác sang phiên sau (đã chốt tối 25/11, 0 USD API):**
  1. **Dọn nốt 4 nhóm chỗ lệch trong 8 file `bai_hoc/giao_trinh/`** (`00`, `05`, `30`, `37`, `41`, `PL_G`, `PL_H`, `PL_I`): Hiếu duyệt 21:49, tạm gác 21:58 để kết phiên; `d` vừa kịp hoàn tất và đẩy nhánh `origin/p15-d-don-giao-trinh-2511` (`06670463`) trước khi nghỉ (`waiting`), đầu phiên sau chỉ cần review chéo rồi gộp `main`.
  2. **Đổi ảnh bài *Lễ Kỳ yên đình làng Huế*** sang ảnh đình làng ở Huế (Hiếu chọn 21:49 25/11): tạm giữ ô màu (`268 / 269`) tới khi Hiếu tìm ảnh thay tấm Đình Tân Lân (Biên Hòa, Đồng Nai) để Khám phá tròn `269 / 269`.
- **Gác (chờ chủ dự án tự mở lại):**
  - Thuê GPU + huấn luyện model nhận ảnh (gác theo lời chủ dự án 15:17 & 20:50 25/11; gói `data/anh_huan_luyen_2026-11-24/goi_may_thue.tar` 3,3 GB giữ nguyên).
  - Bốn bài kho chưa có giờ mở cửa (Chùa Thiên Mụ, Hổ Quyền, Đàn Xã Tắc, Suối Voi): chờ kết quả tra URL từ chủ dự án nếu có.
  - Bước triển khai thực tế (`deploy/`): chờ chọn tên miền/IP, email cảnh báo tiền, trần lượt/ngày.

### A.2. Nợ kỹ thuật nhỏ (gom làm khi sửa file liên quan, không mở đợt riêng)
- **Độ dài tên trong gói deploy `gpt-6-luna`:** kiểm lại chỗ cắt tên hoặc chữ dài nếu phát hiện trong thực tế (E ghi chú sau rà).
- **Chuẩn hoá 1–2 dòng docstring/comment nhỏ** còn dư từ đợt rà B (`ho_so_chu_de` / `sua_lich_hoan_tac`) nếu có dịp chạm file.

### A.4. Bản thử trên nhánh — trạng thái
- **Đã gộp lên `main` (25/11):** `p15-b-hoan-tac-mo` + `p15-c-hoan-tac-mo` · `p15-b-chu-de-trang-chu` + `p15-c-trang-chu-chu-de-mo` · `p15-b-chuyen-ve-luna` · `p15-c-deploy-4-viec` · `p9-d-giao-trinh-2511` · `p15-a-vong-cai-tien-2511` · đợt 3 bản sửa sau tự test của chủ dự án (`ea96e47c`) · `p15-e-bao-cao-bo-kin-2511` + `p15-d-giao-trinh-bo-kin-2511` (báo cáo & giáo trình bộ câu kín) · `p15-e-gon-gioi-thieu` (`bad77d14`) · `p15-e-anh-user-2511` (`bee77a0a`) · `p15-e-readme-2511` (`d2ebb8f8`).
- **Đang chờ review chéo & gộp đầu phiên sau:** `origin/p15-d-don-giao-trinh-2511` (`06670463` — `d` đã dọn xong 8 file `bai_hoc/giao_trinh/`).
- **Đóng, KHÔNG gộp (giữ nhánh để đối chiếu):** `origin/thu-b-mo-doc-tiep` (tỉ lệ đạt bằng mốc 7/12 = 58,3%) · `origin/thu-c-khung-truoc` (chủ dự án chọn bỏ).

## B. Chỉ số nền & Trần OpenAI của nhóm
- **Model viết mặc định (từ 15:41 25/11):** `gpt-6-luna` (`full_corpus_generation.provider: openai`).
- **Tính năng (`backend/config/settings.yaml`):** **62 MỞ · 6 TẮT** (`anh.bat` + 61 cờ mở / 6 cờ tắt trong `assistant:`, sau khi gỡ sạch `vi_sao`).
- **Cả bộ test (`c2d0ee68` + chạy kiểm lại sau đợt sửa 17:13 25/11):** nền đầy đủ **101 file · 4 bỏ · 97 chạy · 2.397 ca đạt · 0 file đỏ** (`data/test_rong_2026-11-22/KET_QUA_c2d0ee68.tsv`); sau 3 bản sửa 17:13 chạy lại 8 file test liên quan (`111 passed`, `npm run build` sạch).
- **Chi phí OpenAI phần test của nhóm:** **~0,74 USD** (`0,66` đo bù 23/11 + `0,008213` Playwright C + `0,000572` kiểm `main` A + `0,0051` 5 lượt `/api/chat` kiểm khói 25/11 + `0,0665833` lượt bộ câu kín & N trên `ea96e47c`; phần gọi trực tiếp `so_tay` / `ho_so` lúc kiểm khói và bên `moc` trong N / K chưa ghi `usd`) / trần **2–2,5 USD** (không tính phần chủ dự án tự test, lời chủ dự án 15:44 25/11).
