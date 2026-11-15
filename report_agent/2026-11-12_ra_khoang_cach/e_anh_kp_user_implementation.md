# Ảnh Khám phá User tự tìm cho 8 bài còn trống (E · 15:59 15/11/2026, `date`)

Người làm: E. A giao (User để 8 ảnh ở thư mục private, tên file = tên bài). Nhánh `p9-anh-kp-user`. 0 USD.

## 1. Kết quả: ghép 4 / 8 ⇒ Khám phá 255 ⇒ **259 / 263** bài có ảnh (kỳ vọng tối đa của A: 263)
E nhìn từng ảnh theo luật chọn ảnh (không trẻ em · không người rõ mặt làm trọng tâm · không số điện thoại · không rõ là nơi / lễ khác).

| # | Bài (loại) | Quyết định | Lý do |
|---|---|---|---|
| 1 | quán bún bò (quán) | **ghép** | ảnh món; không người, không chữ |
| 2 | quán cà phê kiểu Nhật (quán) | **ghép** — A xem lại | mặt tiền có biển tên quán; **có dấu nước to của một trang tin giữa ảnh** (không thuộc 3 điều cấm; vòng trước E đã loại ảnh cùng loại vì lý do này — nay là ảnh User chọn) |
| 3 | nhà hàng chay (quán) | **ghép** | mâm món; không người, không chữ |
| 4 | nhà hàng trên đầm (quán) | **ghép** | toàn cảnh nhà sàn giữa đầm; không người |
| 5 | bài ca kịch | **chưa ghép** | diễn viên rõ mặt là trọng tâm (người áo vàng giữa ảnh, cả tốp nhìn rõ mặt) — đúng lý do các vòng trước loại |
| 6 | làng nón (cũng là điểm lịch chưa có ảnh) | **chưa ghép** | người rõ mặt là trọng tâm (bà cụ chằm nón giữa ảnh). Có **bản thử cắt** phần chồng nón bên trái, không còn người (ô 9 tấm ghép) — dùng được nếu User / A chấp nhận ảnh nón chung |
| 7 | lễ Kỳ yên đình làng | **chưa ghép** | biển trong ảnh ghi tên một đình **không có trong kho** (E grep kho: 0 kết quả); theo hiểu biết của E đó là đình ở Nam Bộ ⇒ nơi khác, lễ khác vùng |
| 8 | lễ Tiến Xuân ngưu | **chưa ghép** | nền là toà nhà vàng có bức vẽ rồng + tháp gạch — rất giống cảnh tái hiện ở Hà Nội mà vòng trước đã loại; **E không chắc 100 %** (suy luận từ cảnh, không có chú thích nguồn) |

Bốn ảnh chưa ghép: chờ User / A quyết (ghép kèm cờ "không chắc" để chỉ hiện ở Khám phá, không hiện cạnh câu trả lời · dùng bản cắt · ảnh khác · để trống). Ảnh lịch cho làng nón: chưa làm (ảnh chưa đạt) ⇒ ảnh lịch vẫn 39 / 41.

## 2. Đã đổi
- Bảng ảnh Khám phá v9 (private, cùng khuôn v4–v8; lý do từng ảnh chưa ghép ghi trong bảng) + 1 dòng đọc v9 trong script dựng (private).
- Tracked: `frontend/src/anhBai.js` (+4 dòng, sinh bằng script) + 4 ảnh mới `frontend/public/anh/kp/` (≤ 480 px, ≤ 40 KB như các đợt trước). Chạy lại script: 231 ảnh cũ giống byte (git không báo đổi).
- Không cờ "không chắc" mới (vẫn 54) ⇒ 4 ảnh mới hiện được cả cạnh câu trả lời của trợ lý khi bài được trích.

## 3. Kiểm
| Bước | Kết quả |
|---|---|
| Đếm bằng code: bài trong build record có dòng ảnh | 259 / 263; 4 bài trống đúng là 4 bài ở bảng trên |
| `test_anh_tra_loi.py` + `test_static_ui.py` | 6 đạt (8 s) |
| `npm ci && npm run build` | đạt |
| Playwright, test rộng | NOT RUN — chỉ đổi ảnh + bảng ảnh |

Tấm ghép để A nhìn lại 100 % (private): `data/anh_kp_user_2026-11-15/ghep_8_anh.jpg` (ô 1–4 ảnh sẽ hiện; ô 5–8 chưa ghép; ô 9 bản thử cắt).

**Giải thích ngắn:** 4 quán có thêm ảnh do User chọn. 4 ảnh còn lại phạm đúng những điều luật ảnh cấm (mặt người là trọng tâm, hoặc ảnh chụp ở nơi khác) nên E giữ lại chờ quyết, không tự thay.
