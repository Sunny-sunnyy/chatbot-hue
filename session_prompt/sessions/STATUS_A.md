# STATUS_A — Phiên điều phối A (`agy` CLI)

Cập nhật: 22:00 25/11/2026 (giờ `date`).

## 1. Đang giữ vai trò & phạm vi
- Phiên điều phối (A) đã hoàn tất phiên tối 25/11: kiểm khói `gpt-6-luna`, hậu kỳ bộ câu kín trên `ea96e47c`, rút gọn trang Giới thiệu (`bad77d14`), ghép 7/8 ảnh mới (`bee77a0a`), cập nhật `README.md` + `bai_hoc/README.md` (`d2ebb8f8`), và kết phiên theo yêu cầu Hiếu (`21:58`).

## 2. Đã xong trong đợt 25/11
- Đợt `/swarm` chiều (`b57cdb2d`) & đợt sửa sau buổi tự test 17:13 (`ea96e47c`).
- Kiểm khói `gpt-6-luna` qua giao diện cổng `8035` ĐẠT SẠCH (`data/playwright_mcp/luot_2511_luna_khoi/NHAT_KY.md`).
- Bộ câu kín trên `ea96e47c` + hậu kỳ `/swarm` (`0 USD` API ngoài): đồng thuận K kín **14/14 = 100%**, báo cáo `report_agent/2026-11-25/E_BO_CAU_KIN_LUNA_2511.md`, đồng bộ 9 file giáo trình, dọn `/tmp/b7_moc`.
- **20:50:** Ghi nhận quyết định Phương án 2 (dừng phần xây ở local, tiếp tục gác thuê GPU nhận ảnh).
- **21:22–22:00 (`0 USD` API):**
  - Rút gọn trang Giới thiệu theo Phương án 1 (`bad77d14`, `b` duyệt `READY`, Playwright 1536 px & 390 px 0 lỗi / 0 tràn).
  - Ghép 7/8 ảnh mới Hiếu gửi (`bee77a0a`: Khám phá `268/269`, lịch trình `bang_anh_v10.json` `47/47`, lưu trú `bang_luu_tru_lich_v7.json` `70/136` với 4–5 sao `24/24`; `b` duyệt `READY` với `99 passed`; dựng lại `frontend/dist` cây chính; 9 URL `/static/anh/...` HTTP 200 & 4 thẻ Khám phá xanh trên cổng `8036` đã tắt).
  - Cập nhật `README.md` + `bai_hoc/README.md` (`d2ebb8f8`, `b` duyệt `READY`).

## 3. Đang làm / còn mở (gác sang phiên sau theo lời 21:58)
- **Dọn 8 file `bai_hoc/giao_trinh/`** (`00, 05, 30, 37, 41, PL_G, PL_H, PL_I`): `d` vừa kịp đẩy trọn lên `origin/p15-d-don-giao-trinh-2511` (`06670463`) trước khi nghỉ (`waiting`); tạm gác sang đầu phiên sau để review chéo rồi gộp `main` theo lệnh kết phiên `21:58`.
- **Đổi ảnh bài *Lễ Kỳ yên đình làng Huế*** sang ảnh đình làng ở Huế (`268 → 269/269` khi Hiếu gửi ảnh thay tấm Đình Tân Lân Biên Hòa).

## 4. Điểm cần kiểm / quyết định chờ chủ dự án
- Đã đóng mốc xây ở local theo lựa chọn Phương án 2 của Hiếu. Thuê GPU nhận ảnh, 4 bài kho thiếu giờ và deploy vẫn gác chờ Hiếu tự mở lại.

## 5. Tài nguyên & Chi phí
- **Qdrant (`hue_rag-qdrant-1`, cổng 6335):** đang BẬT, đủ **9.536 điểm**.
- **Cổng `8010`, `8035`, `8036`, `888x`:** đều đang TRỐNG (đã tắt sạch server tạm).
- **Ngân sách OpenAI (nhóm agent):** kiểm khói `/api/chat` (`0,0051`) + bộ câu kín & N (`0,0665833`); các việc từ 21:00–22:00 dùng `0 USD`. Lũy kế đã ghi nhận ~**0,74 USD** / trần **2–2,5 USD**.

## 6. Môi trường / Lưu ý kỹ thuật khi chạy lệnh
- **Playwright MCP:** `~/.gemini/config/mcp_config.json` chạy `@playwright/mcp@0.0.86` báo thiếu `/opt/google/chrome/chrome` (tạm thời dùng `playwright` Python trong `.venv` bình thường).

## 7. Ghi nhận thêm từ các phiên (chuyển sang vòng cải tiến sau)
- **Từ D (`#35`):** `agy.*.old` khi `agy` tự cập nhật làm sandbox lệnh shell hỏng; DNS GitHub khi tắt mạng có thể cần thử lại.
- **Từ A (19:34 25/11):** `~/.gemini/config/mcp_config.json` chưa chỉ định `--browser chromium` nên `browser_navigate` lỗi thiếu `/opt/google/chrome/chrome`.
- **Từ A (19:42 25/11):** `chay_t1.py` có `U1_KHONG_BAT = {"U1"}` nên `chay_ngay.sh` chỉ chạy 27 câu dù `cap_mu_ngay.py` đòi 28 câu (phải bù riêng `u1_cau.jsonl` như 18/11).
