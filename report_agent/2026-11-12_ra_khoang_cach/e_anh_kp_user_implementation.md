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

## 4. Cập nhật 16:06 15/11/2026 (`date`) — sau khi A nhìn tấm ghép (nhánh `p9-anh-tay-ho`)
- A quyết: ảnh quán cà phê có dấu nước to — **giữ** (ảnh User chọn, không phạm 3 điều cấm; ghi là giới hạn thẩm mỹ). Ba ảnh bài ca kịch + hai bài lễ — **không ghép**, không dùng cờ "không chắc" cho ảnh nghi sai nơi; User đưa ảnh khác thì làm tiếp.
- **Làng nón:** A chấp nhận bản cắt không người (phần chồng nón, 235 × 375) ⇒ ghép vào Khám phá **và** ảnh lịch.
  - Khám phá **259 ⇒ 260 / 263** (đếm bằng code; 3 bài trống đúng là 3 bài trên).
  - Ảnh lịch **39 ⇒ 40 / 41** (còn thiếu một bãi biển): bảng ảnh lịch v5 (private, md5 `5ed8f32903a9`) = v4 + 1 dòng; `settings.yaml` 1 dòng.
  - **Đổi code nhỏ (cần review):** ảnh User không có trang nguồn, mà loader bảng ảnh lịch chỉ nhận ảnh Commons (tác giả + giấy phép) hoặc ảnh web (trang https) ⇒ thêm loại thứ ba `nguon: "user"` (không được kèm trang); và sửa một dòng đọc trường trang (giá trị rỗng không còn bị đổi thành chữ). Test thêm 3 ca (2 ca phải bị từ chối, 1 ca hợp lệ).
- Kiểm: `test_len_ke_hoach_v2` + `test_anh_tra_loi` + `test_static_ui` + `test_cong_dot_1` 119 đạt không khoá / 119 đạt có khoá (72 s / 52 s); build đạt; nạp bảng ảnh v5 bằng loader thật: 40 dòng.
- Giới hạn: ảnh làng nón là ảnh nón chung (không nhận ra được làng) và khổ dọc hẹp; ảnh gốc của User có người rõ mặt nên không dùng nguyên.
