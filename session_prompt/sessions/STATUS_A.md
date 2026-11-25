# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 17:13 25/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) tiếp nhận và xử lý 3 phản hồi sau buổi chủ dự án tự test chiều tối 25/11 (`vi_sao`, bong bóng dẫn web, lặp `"bỏ lăng"`).

## 2. Đã xong trong đợt 25/11
- Đợt `/swarm` chiều (`b57cdb2d`): gộp nút **Hoàn tác lần sửa này**, dải **Hồ sơ theo chủ đề** Trang chủ + đổi tiêu đề **"Khám phá theo lĩnh vực"**, 4 việc `deploy/`, chuyển về **`gpt-6-luna`**, đồng bộ 19 file giáo trình, vòng `improve-workflow`, chạy cả bộ test trên `c2d0ee68` (**97 chạy / 2.397 ca đạt / 0 file đỏ**).
- Đợt sửa sau buổi tự test (17:13 25/11, `0 USD`):
  1. Gỡ sạch `"Vì sao trả lời vậy?"` (`vi_sao`): xoá `backend/api/vi_sao.py`, `backend/tests/test_vi_sao.py`, `frontend/src/ViSao.jsx`, `frontend/src/vi_sao.css`, `bai_hoc/giao_trinh/42_VI_SAO_TRA_LOI_VAY.md`, rút sạch khỏi `app.py`, `chat.py`, `assistant.py`, `so_vet.py`, `settings.yaml` (**62 mở / 6 tắt**), `dong_goi.sh`, `LenKeHoach.jsx`, `chat.jsx`, runbook & giáo trình.
  2. Ẩn bong bóng `"Tư liệu của mình chưa có thông tin này…"` khi có khung `"Từ web (chưa kiểm)"` (`frontend/src/moDauWeb.js`, `frontend/src/chat.jsx`, `backend/tests/test_mo_dau_web.py`).
  3. Khử trùng lặp khung hỏi tên mơ hồ (`"bỏ lăng"`) trong `backend/llm/sua_lich_v2.py` + test hồi quy `backend/tests/test_sua_lich_hoi_truoc.py`.
- Dựng lại `frontend/dist` (`616ms`), chạy 8 file test liên quan (**111 passed**), giao agent con đọc chéo diff, cập nhật sổ & `data/loi_user/2026-11-25.md`, đẩy `main`.

## 3. Đang làm / còn mở
- Chờ chủ dự án khởi động lại server (`scripts/bat_he_thong.sh`) nếu muốn nhìn lại 3 điểm vừa sửa, rồi gõ lệnh chạy bộ câu kín 1 lần trên `gpt-6-luna`.

## 4. Điểm cần kiểm / quyết định chờ chủ dự án
- Chỉ còn lịch chạy bộ câu kín 1 lần trên `gpt-6-luna`. Thuê GPU ảnh, 4 bài kho thiếu giờ và deploy công khai vẫn gác chờ chủ dự án tự mở lại.

## 5. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang chạy, đủ **9.536 điểm**.
- **Cổng `8010`:** server của chủ dự án đang bật (KHÔNG đụng/tắt); nhắc chủ dự án tự khởi động lại để nhận code & `frontend/dist` mới.
- **Ngân sách OpenAI (nhóm agent):** **~0,67 USD** / trần **2–2,5 USD** (đợt sửa 17:13 tốn `0 USD`).

## 6. Môi trường / Lưu ý kỹ thuật khi chạy lệnh
- Trong phiên `agy` hiện tại, `run_command` sandbox lỗi `fork/exec /home/minhhieu/.local/bin/agy.*.old: no such file or directory`; chạy lệnh git/date/test thật bằng `BypassSandbox: true`.

## 7. Ghi nhận thêm từ các phiên (chuyển sang vòng cải tiến sau)
- **Từ D (`#35`):** `agy.*.old` khi `agy` tự cập nhật làm sandbox lệnh shell hỏng; DNS GitHub khi tắt mạng có thể cần thử lại.
