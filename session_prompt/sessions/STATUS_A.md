# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 16:28 25/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đóng đợt `/swarm` local chiều 25/11 trên `agy` CLI. Không tự sửa code ứng dụng; chỉ tổng hợp, giải xung đột gộp, kiểm sống cuối và cập nhật bộ sổ.

## 2. Đã xong trong đợt 25/11
- Nhận & chốt 4 quyết định chiều 25/11 + 3 cập nhật sau đó (15:17 gác GPU · 15:41 chuyển về `gpt-6-luna` · 15:44 trần 2–2,5 USD chỉ tính cho agent test), lưu nguyên văn ở `data/loi_user/2026-11-25.md`.
- Phối hợp `/swarm` (`b`, `c`, `d`, `e`, `monitor`) gộp lên `main`:
  - `9a22503c` + `bc1dbbbf` (`fb666a1f`): giáo trình đầu đợt & 4 việc bộ `deploy/`.
  - `d1d1bd18`, `2633b35d`, `b34394de`, `0a3346fe`, `37787894` ⇒ `c2d0ee68`: chuyển về `gpt-6-luna` (`provider: openai`), nút **Hoàn tác lần sửa này** (`sua_lich_hoan_tac: true`), dải **Hồ sơ theo chủ đề** Trang chủ (`chu_de_trang_chu: true`) + đổi tiêu đề 5 ô thành **"Khám phá theo lĩnh vực"**; dựng mới `frontend/dist`.
  - `3abd261a`: đồng bộ 19 file `bai_hoc/giao_trinh/` theo trạng thái 63 mở / 6 tắt & `gpt-6-luna` (E kiểm khớp 100%).
  - `f67e8bfe`: vòng `improve-workflow` 24–25/11 & chốt thử nghiệm 3 ngày (0 luật mới, D đọc chéo khớp).
- Kiểm thật `main` `c2d0ee68` trên cổng tạm `8032`: `/health` xanh, `/api/tinh_nang` khớp `OpenAI` + 2 cờ mới bật, 1 câu `POST /api/chat` trả `model: gpt-6-luna` (`0,000571625 USD`), đóng cổng `8032`. E chạy trọn bộ test trên `c2d0ee68`: **97 file chạy / 2.397 ca đạt / 0 file đỏ** (`1.320` giây).
- Cập nhật `data/test_cuoi/TEST_2411_TRUA.md` (lệnh bật `scripts/bat_he_thong.sh` không cần Bedrock + mục 6 cho buổi test tối 25/11).

## 3. Đang làm / còn mở
- Không còn việc code đang chạy dở. Chờ chủ dự án tự test tối 25/11, sau đó sửa lỗi (nếu có) và chạy 1 lượt bộ câu kín trên `gpt-6-luna`.

## 4. Điểm cần kiểm / quyết định chờ chủ dự án
- Chỉ còn buổi tự test tối 25/11 của chủ dự án (`data/test_cuoi/TEST_2411_TRUA.md`). Phần thuê GPU huấn luyện ảnh, 4 bài kho thiếu giờ mở cửa và thông số deploy thực tế đều đã gác theo lịch chờ chủ dự án tự mở lại.

## 5. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang chạy, đủ **9.536 điểm**.
- **Server `80xx`:** không có tiến trình nào đang chiếm cổng (đã đóng hết `8031`, `8032`).
- **Ngân sách OpenAI (nhóm agent):** đã dùng **~0,67 USD** (`0,66` đo bù 23/11 + `0,008213` Playwright C + `0,000572` kiểm `main` A) / trần **2–2,5 USD** (phần chủ dự án tự test không tính vào trần này).

## 6. Môi trường / Lưu ý kỹ thuật khi chạy lệnh
- Trong phiên `agy` hiện tại, `run_command` sandbox lỗi `fork/exec /home/minhhieu/.local/bin/agy.1795591646957095365.old: no such file or directory` sau khi `agy` tự cập nhật; chạy lệnh git/date/test thật bằng `BypassSandbox: true`.

## 7. Ghi nhận thêm từ các phiên (chuyển sang vòng cải tiến sau)
- **Từ D (`#35`):** (1) Ghi nhận sandbox trong `agy` tự nâng cấp có thể đổi tên file tạm `.old` gây lỗi chạy lệnh sandbox; (2) thỉnh thoảng đẩy GitHub trong môi trường không bật mạng có thể vấp DNS tạm thời, chạy lại ngoài sandbox là qua.
