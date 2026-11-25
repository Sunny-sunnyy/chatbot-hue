# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 20:50 25/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) mở phiên tối 25/11: kiểm khói `gpt-6-luna`, chuẩn bị & điều phối `/swarm` hậu kỳ bộ câu kín trên `ea96e47c`, gộp báo cáo + giáo trình, ghi nhận quyết định Phương án 2 (dừng phần xây ở local).

## 2. Đã xong trong đợt 25/11
- Đợt `/swarm` chiều (`b57cdb2d`) & đợt sửa sau buổi tự test 17:13 (`ea96e47c`).
- Kiểm khói `gpt-6-luna` qua giao diện cổng `8035` ĐẠT SẠCH (`data/playwright_mcp/luot_2511_luna_khoi/NHAT_KY.md`).
- Chuẩn bị & hậu kỳ bộ câu kín (`19:39–20:43`): dựng `/tmp/b7_moc`, chạy N (28/28 câu), Hiếu chạy `user_chay_kin.sh` (`K`, `S ×2`, `T`, `C`; `L kín = NOT RUN`), mở `/swarm` (`e`, `b`, `d`, `monitor` — 0 USD API ngoài): chấm mù đồng thuận K kín **14/14 = 100%**, gộp báo cáo `report_agent/2026-11-25/E_BO_CAU_KIN_LUNA_2511.md` (`p15-e-bao-cao-bo-kin-2511`), gộp 9 file giáo trình (`p15-d-giao-trinh-bo-kin-2511`), dọn sạch `/tmp/b7_moc`.
- **20:50:** Ghi nhận quyết định của Hiếu chọn Phương án 2 (dừng phần xây ở local, tiếp tục gác thuê GPU nhận ảnh).

## 3. Đang làm / còn mở
- Không còn việc xây ở local; sẵn sàng kết phiên hoặc mở việc mới (deploy / đọc giáo trình / mở lại GPU ảnh) khi Hiếu gọi.

## 4. Điểm cần kiểm / quyết định chờ chủ dự án
- Đã đóng mốc xây ở local theo lựa chọn Phương án 2 của Hiếu. Thuê GPU nhận ảnh, 4 bài kho thiếu giờ và deploy vẫn gác chờ Hiếu tự mở lại.

## 5. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.536 điểm**.
- **Cổng `8010`, `8035`, `888x`:** đều đang TRỐNG (đã tắt sạch server tạm).
- **Ngân sách OpenAI (nhóm agent):** kiểm khói `/api/chat` (`0,0051`) + bộ câu kín & N (`0,0665833`). Lũy kế đã ghi nhận ~**0,74 USD** / trần **2–2,5 USD**.

## 6. Môi trường / Lưu ý kỹ thuật khi chạy lệnh
- **Playwright MCP:** `~/.gemini/config/mcp_config.json` chạy `@playwright/mcp@0.0.86` báo thiếu `/opt/google/chrome/chrome` (cần thêm `--browser chromium` hoặc `--executable-path` ở lượt sửa cấu hình sau; tạm thời dùng `playwright` Python trong `.venv` bình thường).

## 7. Ghi nhận thêm từ các phiên (chuyển sang vòng cải tiến sau)
- **Từ D (`#35`):** `agy.*.old` khi `agy` tự cập nhật làm sandbox lệnh shell hỏng; DNS GitHub khi tắt mạng có thể cần thử lại.
- **Từ A (19:34 25/11):** `~/.gemini/config/mcp_config.json` chưa chỉ định `--browser chromium` nên `browser_navigate` lỗi thiếu `/opt/google/chrome/chrome`.
- **Từ A (19:42 25/11):** `chay_t1.py` có `U1_KHONG_BAT = {"U1"}` nên `chay_ngay.sh` chỉ chạy 27 câu dù `cap_mu_ngay.py` đòi 28 câu (phải bù riêng `u1_cau.jsonl` như 18/11).
