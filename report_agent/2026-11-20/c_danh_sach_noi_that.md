# C — câu xin danh sách: code nối một dòng nói thật "danh sách có thể chưa đủ" (nhánh `p9-c-liet-ke-noi-that`)

Chủ dự án chọn 15:3x 20/11/2026 sau phép đếm 0 USD (số đếm: file riêng tư `data/kiem_ke_phase_2026-11-20/C_dem_18_19.md`): làm ĐÚNG phần nhỏ — không
chữa độ đủ của danh sách (cần bảng thuộc tính + bổ sung kho), chỉ để trợ lý không còn im lặng khi danh sách có thể thiếu. Mức nhẹ: không plan riêng.

## Tiêu chí ghi TRƯỚC khi viết code (15:34 20/11/2026, giờ `date`)
1. Xong khi: `uv run pytest tests/test_danh_sach_noi_that.py -q` đạt, và trong đó có ca ĐỎ trên code cũ (cờ bật, câu xin danh sách, có nguồn ⇒ `notice` có dòng mới).
2. Dòng do CODE nối vào `notice`; chữ câu trả lời và chuỗi gửi model không đổi. Cờ tắt ⇒ `notice` y như trước (test so chuỗi).
3. KHÔNG nối ở: câu từ chối / câu cố định (không có nguồn trích) · lượt có lịch (biểu mẫu, sửa lịch, công cụ lịch) · câu trả lời có dòng ý thiếu (lượt mở mục web) ·
   câu chỉ hỏi về MỘT nơi (câu gõ có tên bài của một nguồn được trích).
4. Khuôn nhận câu HẸP, danh sách cho phép: sót câu xin danh sách thì chấp nhận; nối nhầm vào câu không xin danh sách thì không. Bộ dò độc lập của phiên E
   (20 phải nhận + 20 giống-mà-không-phải, E không xem khuôn): nối nhầm 0 / 20 là sàn; nhận ≥ 14 / 20 là mức mong, dưới mức đó chỉ báo, không nới khuôn theo bộ dò.
5. Trước gộp: file test mới + các file test chạm `set_notice` + file test dựng app chạm route chat đều đạt. Lượt thật qua giao diện: gộp vào lượt bật server chung
   của nhóm — tới lúc đó ghi "[chưa đo trên đường thật]".
6. Không làm: sửa lời dặn, đổi cách tìm, bảng thuộc tính, bổ sung kho.

## Kết quả (ghi 15:43 20/11/2026, giờ `date`) — cờ `danh_sach_noi_that`, mặc định TẮT
- **Người dùng thấy gì khác (khi cờ bật):** hỏi kiểu "ở Huế có những quán nào mở từ sáng sớm", "kể hết các lăng", "liệt kê các quán cà phê ven sông" mà trợ lý trả lời được
  từ kho ⇒ dưới câu trả lời, ở dòng ghi chú, có thêm câu: "Danh sách trên chỉ gồm những nơi có trong các bài tìm được, nên có thể chưa đủ." Chữ câu trả lời không đổi.
  Cờ tắt (hiện nay) ⇒ không khác gì.
- **Đã sửa:** `backend/llm/danh_sach.py` (mới, hàm thuần `xin_danh_sach`, `hoi_ve_mot_noi`, hằng `CAU_DANH_SACH`) · `backend/llm/assistant.py` (+10 dòng: cờ, một trường
  của lượt đặt ở `_before_model`, một nhánh trong `set_notice`) · `backend/config/settings.yaml` (+1 dòng, `false`) · `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 (hai dòng:
  giới hạn của cờ này; số đếm 20/11 của "kho có một phần thì từ chối cả câu" — chủ dự án chọn giữ giới hạn).
- **Bằng chứng [máy kiểm, test bằng đồ giả — chưa có người thứ hai]:** `tests/test_danh_sach_noi_that.py` 26 đạt; ca "cờ bật + câu xin danh sách + có nguồn ⇒ có dòng"
  ĐỎ khi gỡ dòng nối (1 hỏng / 25 đạt) rồi xanh lại. File chạm đường ghi chú / cờ: `test_noi_dong_tam_ngung` 32 · `test_khoang_cach` 101 · `test_settings_env` 6 ·
  `test_nho_ten_goi_y` 19 đạt. File dựng app chạm route chat `test_api_chat`: 14 đạt không khoá + 1 test cần khoá API chạy riêng có khoá, đạt (≈ 0,001 USD).
  Chạy bằng môi trường Python 3.13 của cây chính, từng file một.
- **Chưa làm / giới hạn:** [chưa đo trên đường thật] — chưa có lượt nào qua server và giao diện · bộ dò độc lập của phiên E (20 phải nhận + 20 giống-mà-không-phải) CHƯA chạy
  ⇒ cờ để TẮT · khuôn hẹp: "quán nào …" không có "những / các", câu xin gợi ý, câu so sánh đều không nhận · phép "câu về một nơi" chỉ so tên bài được trích với câu gõ
  (người dùng gõ tên khác tên bài thì không bắt được) · lượt trong cuộc có lịch đã lưu vẫn nhận dòng nếu là câu hỏi đáp thường · không chữa độ đủ của danh sách.
- **Cách thử trong 2 phút (sau khi bật cờ + mở server):** hỏi "Ở Huế có những quán nào bán cơm hến?" ⇒ dưới câu trả lời có dòng ghi chú trên; hỏi "Cơm hến ăn ở quán nào ngon?" ⇒ không có dòng đó.

| Đã làm | Chưa làm | Tự hoãn + lý do | Lệnh kiểm + đầu ra |
|---|---|---|---|
| hàm nhận câu + nhánh nối + cờ tắt + test + hai dòng runbook | lượt thật; bộ dò của E; bật cờ | lượt thật gộp vào lượt bật server chung (phiên điều phối xếp) | `cd backend && uv run pytest tests/test_danh_sach_noi_that.py -q` ⇒ `26 passed` |
