# Ảnh quán ở thẻ bữa trong lịch — implementation · C · 18:13 14/11/2026

Nhánh `p9-anh-quan` @ `496206d` (từ `origin/main` `7da2ea7`). Tiêu chí ghi trước: `data/anh_quan_2026-11-14/TIEU_CHI.md` (private). Tiền: Serper 45 lượt ≈ 0,045 USD + lượt chụp giao diện 4 lịch ≈ 0,0043 USD; tra "còn mở" bằng Codex (gói ChatGPT của User).

## Đổi gì
- `backend/llm/quan_lich.py`: bảng quán nhận trường `anh` tuỳ chọn — chỉ dòng KHÔNG phải kho, chỉ mẫu `quan/[a-z0-9_]{1,40}`; sai ⇒ không khởi động (như các trường khác). `_hien` gửi `anh` cho giao diện. Không vào chuỗi gửi model (khối `an` vốn không vào model).
- `frontend/src/LichV2.jsx` + `lkh.css`: ảnh 44 px cạnh tên quán. Quán kho ⇒ ảnh Khám phá của bài (`anhCuaBai`, file E giữ); quán ngoài kho ⇒ `anh/quan/<mã>` (giao diện kiểm lại mẫu). Không ảnh ⇒ như cũ. 0 chữ ghi công.
- `frontend/public/anh/quan/`: 6 ảnh ≤ 40 KB (tổng 202 KB); nguồn từng ảnh chỉ ở `data/anh_quan_2026-11-14/bang_anh_quan.json`.
- `settings.yaml:89`: chỉ comment md5 bảng (`494587811136`, 468 quán).

## Đếm trước khi làm (vì sao chỉ 6 ảnh)
- Lượt thử 30 quán OSM ngẫu nhiên: 11 / 30 nhận được ảnh đúng (ngưỡng ghi trước ≥ 9) — nhưng **0 / 30 thuộc các quán lịch thật sự chọn**.
- Đếm 3.840 lịch (`dem_quan_hien.py`): chỉ **15** quán ngoài kho từng hiện; 10 quán đầu = 96 % lượt hiện ⇒ chỉ tìm ảnh cho 15 quán đó (không làm ~400 quán không ai thấy).
- 15 quán: 2 agent con chọn độc lập; cùng chọn 6; C nhìn lại 6 / 6 đúng quán. Biển Bà Tý có số điện thoại ⇒ cắt ảnh (thẻ bữa không hiện điện thoại). 3 ảnh gắn `kc` trong data (không dùng ở giao diện lịch).
- Phủ: 6 quán = 48 % lượt hiện quán ngoài kho. Quán kho: ảnh do E (bài Khám phá).
- Còn mở: Codex tra 15 quán ⇒ 8 còn mở · 0 đã đóng · 7 không rõ (`data/tra_cuu_cli/2026-11-14_quan-osm-con-mo/`); C WebFetch 3 nguồn khớp. Lỗi thật lộ ra lúc đếm: một quán đã đóng hiện ở 324 lịch ⇒ đã bỏ (`p9-quan-bo-da-dong`, merge `ac4f8a8`).

## Kiểm
- [Chạy] `tests/test_quan_lich.py` 15 passed (thêm 1: luật trường `anh` + mọi ảnh bảng nhắc tới có file thật); 4 file test chạm lịch / quán: 372 passed (65 s); `test_static_ui.py` 4 passed. `npm ci && npm run build` ok.
- [Chạy] Playwright thật (server worktree cổng 8031, cờ như main), lịch 5 ngày: khổ 1440 — 14 ảnh tải được (13 kho + 1 OSM), 0 lỗi console, 0 yêu cầu ra ngoài, không tràn ngang ⇒ ĐẠT; khổ 390 — lần 1 KHÔNG ĐẠT do script đo ảnh `loading="lazy"` chưa cuộn tới (w = 0), sửa script cuộn từng ảnh ⇒ ĐẠT 14 / 14. Ảnh: `data/anh_quan_2026-11-14/anh_chup/`. 5 dòng `chat_metrics` = 5 lượt xếp lịch. Server đã tắt (TaskStop).
- Giới hạn: 9 / 15 quán ngoài kho chưa có ảnh (ảnh tìm được không chắc đúng quán); bảng đổi ⇒ chạy lại `dem_quan_hien.py` để biết quán nào cần ảnh.
