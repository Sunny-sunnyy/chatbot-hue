# Việc đang mở (sổ việc — cập nhật 17:13 25/11/2026)

*Mỗi đầu việc có: **làm để chốt gì** · **ai làm** · **tới đâu** · **chỗ lưu**. Quy trình nhiều phiên: `session_prompt/WORKFLOW.md`. Việc đã xong chép 1 dòng sang `session_prompt/VIEC_DA_XONG.md`.*

## A. Sản phẩm & Vận hành

### A.1. Chờ lượt bộ câu kín 1 lần trên `gpt-6-luna` (sau đợt tự test 25/11)
- **Làm để chốt:** chạy bộ câu kín 1 lần (và so "RAG mốc" nếu cần) trên bản `main` đã sửa xong 3 phản hồi của chủ dự án chiều tối 25/11 (`vi_sao` đã gỡ sạch, ẩn bong bóng dẫn web lặp phía trên, sửa lặp `"bỏ lăng"`).
- **Ai làm:** chủ dự án tự bấm xác nhận lại 3 chỗ vừa sửa nếu muốn (khởi động lại `scripts/bat_he_thong.sh`) ⇒ sau đó chủ dự án gõ lệnh chạy bộ câu kín (E / B hỗ trợ so sánh).
- **Trạng thái:** 3 phản hồi buổi tự test 25/11 đã xử lý & kiểm sạch trên `main` (`111` ca test + `npm run build`); Qdrant 9.536 điểm đang chạy; cổng `8010` đang chạy bản trước đó của chủ dự án (không tự tắt).
- **Gác (chờ chủ dự án tự mở lại):**
  - Thuê GPU + huấn luyện model nhận ảnh (gác theo lời chủ dự án 15:17 25/11; gói `data/anh_huan_luyen_2026-11-24/goi_may_thue.tar` 3,3 GB giữ nguyên).
  - Bốn bài kho chưa có giờ mở cửa (Chùa Thiên Mụ, Hổ Quyền, Đàn Xã Tắc, Suối Voi): chờ kết quả tra URL từ chủ dự án nếu có.
  - Bước triển khai thực tế (`deploy/`): chờ chọn tên miền/IP, email cảnh báo tiền, trần lượt/ngày.

### A.2. Nợ kỹ thuật nhỏ (gom làm khi sửa file liên quan, không mở đợt riêng)
- **Độ dài tên trong gói deploy `gpt-6-luna`:** kiểm lại chỗ cắt tên hoặc chữ dài nếu phát hiện trong thực tế (E ghi chú sau rà).
- **Chuẩn hoá 1–2 dòng docstring/comment nhỏ** còn dư từ đợt rà B (`ho_so_chu_de` / `sua_lich_hoan_tac`) nếu có dịp chạm file.

### A.4. Bản thử trên nhánh — trạng thái
- **Đã gộp lên `main` (25/11):** `p15-b-hoan-tac-mo` + `p15-c-hoan-tac-mo` · `p15-b-chu-de-trang-chu` + `p15-c-trang-chu-chu-de-mo` · `p15-b-chuyen-ve-luna` · `p15-c-deploy-4-viec` · `p9-d-giao-trinh-2511` · `p15-a-vong-cai-tien-2511` · và đợt 3 bản sửa sau tự test của chủ dự án (17:13 25/11: gỡ `vi_sao`, ẩn bong bóng dẫn web lặp, sửa lặp `bỏ lăng`).
- **Đóng, KHÔNG gộp (giữ nhánh để đối chiếu):** `origin/thu-b-mo-doc-tiep` (tỉ lệ đạt bằng mốc 7/12 = 58,3%) · `origin/thu-c-khung-truoc` (chủ dự án chọn bỏ).

## B. Chỉ số nền & Trần OpenAI của nhóm
- **Model viết mặc định (từ 15:41 25/11):** `gpt-6-luna` (`full_corpus_generation.provider: openai`).
- **Tính năng (`backend/config/settings.yaml`):** **62 MỞ · 6 TẮT** (`anh.bat` + 61 cờ mở / 6 cờ tắt trong `assistant:`, sau khi gỡ sạch `vi_sao`).
- **Cả bộ test (`c2d0ee68` + chạy kiểm lại sau đợt sửa 17:13 25/11):** nền đầy đủ **101 file · 4 bỏ · 97 chạy · 2.397 ca đạt · 0 file đỏ** (`data/test_rong_2026-11-22/KET_QUA_c2d0ee68.tsv`); sau 3 bản sửa 17:13 chạy lại 8 file test liên quan (`111 passed`, `npm run build` sạch).
- **Chi phí OpenAI phần test của nhóm:** **~0,67 USD** (`0,66` đo bù 23/11 + `0,008213` Playwright C + `0,000572` kiểm `main` A; đợt sửa 17:13 tốn `0 USD`) / trần **2–2,5 USD** (không tính phần chủ dự án tự test, lời chủ dự án 15:44 25/11).
