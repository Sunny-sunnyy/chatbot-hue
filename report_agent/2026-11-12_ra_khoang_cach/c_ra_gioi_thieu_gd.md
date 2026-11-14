# Trang Giới thiệu: chỗ thiếu so với bản mẫu + đề xuất điểm nhấn (C, bàn nhóm vòng 1)

Cập nhật: 15:05 14/11/2026 (C). Ảnh: `data/ui_anh_gt_2026-11-14/` (`truoc/`, `sau/`, `sau_rm/` = chụp cả trang ở chế độ giảm chuyển động, bản thật ↔ bản mẫu).
Đo: Playwright trên bản build do FastAPI phục vụ (nhánh `p9-gd-anh-gt` `adc35ed`, cổng 8873), khổ 1366 và 390. 0 USD.

## 1. Khối hiện dần có kẹt mờ không — KHÔNG

- Cuộn từng bước 400 px tới cuối trang: 12 / 12 khối `.hien` / `.vao` có độ mờ 1,0, cả hai khổ, 0 lỗi console. B đo riêng (cuộn từng bước 100 px, khổ 1440) cũng ra 9 / 9.
- Vùng trống trong ảnh chụp cả trang là do hiệu ứng gắn độ mờ với vị trí cuộn (`animation-timeline: view()`): khối chưa cuộn tới thì còn mờ. Đây không phải lỗi. Ảnh trình User chụp ở chế độ giảm chuyển động.

## 2. Code ↔ bản mẫu `data/ui_mau_2026-11-14/h1/gioi_thieu.html`

Gần như trùng khớp từng khối: đầu trang có ảnh sông, 4 thẻ "làm được gì", 3 bước nối bằng đường sông, "Giới hạn" ↔ "Dữ liệu của bạn". Mục "Nguồn ảnh" của bản mẫu đã bỏ theo User.
⇒ Trang "đơn giản" vì **chính bản mẫu đã đơn giản**, không phải code làm thiếu. Muốn nổi bật thì phải thêm thứ bản mẫu không có (mục 4).

## 3. Chữ trên trang đã cũ so với hệ thống đang chạy (sửa dù chọn gì ở mục 4)

- "Giới hạn" ghi "Chưa có … nơi lưu trú": kho đã có bài lưu trú (ghi kho lần 2, 14/11). Câu này sai, nên sửa.
- "Làm được gì" thiếu những việc đã chạy: xuất lịch ra lịch điện thoại (.ics), ảnh từng điểm trong lịch, thời tiết. Thêm thẻ theo cờ server như các thẻ đang có. Sửa lịch bằng lời chỉ hiện thẻ khi cờ `sua_lich_v2` bật.

## 4. Đề xuất điểm nhấn (0 USD, chỉ dùng dữ liệu thật, không hứa thêm)

| # | Điểm nhấn | Lợi | Công | Rủi ro |
|---|---|---|---|---|
| G1 | **Gắn màn "Huế qua các thời kỳ" của B**, đặt giữa "làm được gì" và "ba bước" | khoảnh khắc chính của trang, kể chuyện bằng dữ kiện trong kho | B làm component; C chỉ gắn vào trang | phụ thuộc B xong |
| G2 | **Dải "Kho tư liệu" 5 lĩnh vực**: mỗi ô có ảnh + số bài (lấy từ `/api/kham_pha`, không gõ tay: hôm nay 91 món · 52 đi lại · 30 di tích · 27 lễ hội · 12 nghệ thuật) + link sang Khám phá theo lĩnh vực | khách thấy ngay "trợ lý biết gì", trang có ảnh, có đường đi tiếp | nhỏ (~40 dòng JSX + CSS, dùng ảnh lĩnh vực đã có) | không — số theo kho thật |
| G3 | **"Ba bước" có câu ví dụ**: mỗi bước kèm một ô minh hoạ nhỏ (câu hỏi mẫu → tên 2–3 bài kho tìm được → đoạn trả lời có [1]), cuối dải có nút "Hỏi thử câu này" mở Trợ lý với câu đó | biến sơ đồ khô thành ví dụ sống | vừa: phải lấy một câu trả lời thật (1 lần chạy ≈ 0,0005 USD), ghi nhãn "Ví dụ" | câu trả lời mẫu cũ đi khi kho đổi ⇒ chỉ hiện tên bài + 1 câu ngắn |

**C khuyến nghị:** mục 3 + G2 + G1 (khi B xong). G3 để sau: lợi có thật nhưng phải giữ một câu trả lời mẫu cho khớp với kho.
**Không đề xuất:** số đếm chạy, parallax thêm lớp, nghiêng 3D (đã loại ở `c_nghien_cuu_wow.md` §3).
