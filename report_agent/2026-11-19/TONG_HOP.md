# Tổng hợp ngày 19/11/2026 (thứ Năm)

Viết: 10:56 19/11/2026 (giờ `date`), phiên điều phối. Thư mục này gom mọi báo cáo viết trong ngày — từ 19/11 mỗi ngày làm việc một thư mục `report_agent/<năm-tháng-ngày>/` (chủ dự án yêu cầu). Phần riêng tư (kết quả đo có câu của bộ đo, kế hoạch, câu dò) không vào repo công khai; file này chỉ trỏ tên thư mục trong `data/`.

## PHIÊN SAU ĐỌC TRƯỚC (GHI ĐÈ lúc kết phiên; ≤ 20 dòng) — viết 22:33 19/11/2026, KẾT PHIÊN CUỐI NGÀY 19/11

- **Thứ tự mở đầu:** `session_prompt/HIEN_TRANG.md` ⇒ `session_prompt/VIEC_DANG_MO.md` (4 khối; bước kế CHỈ ghi ở đó) ⇒ `session_prompt/sessions/STATUS_A.md`. `CURRENT_HANDOFF.md` nay chỉ còn khối trỏ.
- **Việc đầu tiên:** sửa nhỏ cờ nhớ tên nơi vừa trích (hỏi tiếp "kể hết các chỗ vừa nêu" có lúc ra danh sách thiếu) ⇒ soát mù khác hãng (đề bài đã sẵn; phần Gemini cần chủ dự án lái) ⇒ chạy trọn danh sách test cuối bằng trình duyệt thật ⇒ cả bộ test ⇒ mời chủ dự án test một lần.
- **Bản đang chạy:** 29 cờ bật. Tối 19/11 bật thêm bốn: lịch đã lưu vào lượt hỏi thường · câu nói thật cho yêu cầu "làm thay" · hai nút xuất lịch (PDF + PowerPoint) · nhớ tên nơi vừa trích. Cả bộ test trên đúng tổ hợp này: 1.542 đạt, 0 hỏng. Giao diện ở cây chính đã dựng lại.
- **Đo lại bộ kịch bản việc phổ thông (80 kịch bản, một lượt):** xong việc 51 ⇒ 58, 0 kịch bản có điều sai mới, kịch bản đích của cả bốn việc đạt; hai người chấm lệch 1 / 80. Một ca do cơ chế mới (danh sách thiếu khi hỏi "kể hết") — việc đầu tiên ở trên.
- **Thử rồi không đổi / không gộp:** đưa 15 đoạn hoặc cả mục vào ngữ cảnh (không khác về "đủ ý", mỗi nhánh phạm một sàn; giữ 10 đoạn) · câu cố định khi gõ lời nhờ xếp lịch (lỗi đích không còn tái hiện).
- **Chủ dự án chọn tối 19/11:** điểm dừng = danh sách đóng (nay bốn việc) · xong hết ở local ⇒ test một lần ⇒ không phát triển nữa ⇒ deploy · bật ba cờ (một sàn được đọc theo mục đích, ghi rõ) · ghi giới hạn cho hai lỗi không chữa được rẻ (câu "những quán nào có đặc điểm X"; kho có một phần thì từ chối cả câu) · không thêm tính năng mới.
- **Đang chờ chủ dự án:** không có câu nào treo. Khi tới bước soát khác hãng nhóm sẽ nhờ lái một model. Không gấp: khoảng 20 câu tự gõ; một lệnh xoá nhánh cục bộ (`VIEC_DANG_MO.md` khối 4).
- **Lỗi lọt trong ngày, đã sửa:** hai biến cùng tên trong file lập lịch sống trên main ~3,5 giờ (gộp code khi chưa chạy cả bộ test) · câu của bộ kịch bản lọt vào file được git theo dõi hai lần (đã thay; lịch sử git không viết lại) · bản in bị che ảnh / cắt khối (người thứ hai nhìn PDF mới thấy).
- **Sao lưu:** ổ D `2026-11-19_ba_co_bat_ea777c2` (3,6 GB). **Tiền API cả ngày ≈ 1,7 USD** (số từng phiên báo, chưa cộng lại từ log; tối ≈ 0,34).
- **Bẫy của ngày + vòng cải tiến:** `STATUS_A.md` mục 7; cuối `session_prompt/SO_CAI_TIEN_CACH_LAM.md`.

## 1. Việc trong ngày và kết quả

| Việc | Kết quả | Báo cáo trong thư mục này | Phần riêng tư |
|---|---|---|---|
| Báo cáo lượt đo cuối Phase 9 (đo tối 18/11) | Phần lớn sàn đạt; sáu mục chưa đạt theo máy (một mục do nhãn cũ, đã sửa nhãn), tốc độ chưa đo; bộ kín chưa chạy | `b_do_cuoi_b7_implementation.md` | `data/phase_9/b7_cuoi/` |
| Vòng máy tự dò cấu hình bước tìm | 15 cấu hình, 0 cấu hình vượt nhiễu; thước "đủ đoạn đúng" phân biệt yếu | `b_tu_toi_uu_buoc_tim_implementation.md` | `data/cach_lam_2026-11-18/tu_toi_uu/` |
| Thiếu cảnh báo "tạm ngừng" — thử MỘT câu lời dặn | Câu đích nêu ý 8 / 8 lần nhưng "Đủ ý" tụt 7 câu > ngưỡng ⇒ không đạt luật ghi trước, cờ giữ tắt, nhánh giữ làm hồ sơ | (kết quả riêng tư) | `data/phase_9/s09_luu_y/` |
| Thiếu cảnh báo "tạm ngừng" — bản bằng code | Đã vào main, cờ `noi_dong_tam_ngung` BẬT (chủ dự án chọn "bật ngay, ghi giới hạn"): dòng chỉ hiện khi câu trả lời trích bài có cảnh báo — lượt thật 2 / 3, dữ liệu cũ 7 / 7, 0 ca gán nhầm trên dữ liệu đã có | `c_s09_noi_dong_tam_ngung_implementation.md` | `data/phase_9/s09_code/` |
| Sửa lịch bằng lời: câu "dời hai điểm" | Đã vào main, cờ `sua_lich_doi_cho_code` BẬT (chủ dự án duyệt): bộ 10 chuỗi 7 / 10 ⇒ 9 / 10, 0 lượt sửa sai; 63 câu dò của người không viết code: 0 câu áp sai | `b_sua_lich_doi_cho_implementation.md` | `data/phase_9/sua_lich_doi_cho/` |
| Bỏ trần token đầu ra (chủ dự án yêu cầu) | Đã vào main; đếm 3.974 lần gọi: 2 lần gọi định tuyến có đầu ra đúng bằng trần 512 (một lần chắc chắn bị cắt), 0 lần ở lời gọi trả lời; token suy luận tính vào trần | (ghi ở sổ việc) | `data/phase_9/bo_max_token/` |
| Bỏ ngân sách ngữ cảnh 16.384 token + trần lịch sử 1.500 token (chủ dự án yêu cầu) | Đã vào main; đếm: chưa lượt nào từng chạm (đầu vào lớn nhất 6.233 token) | (ghi ở sổ việc) | `data/phase_9/bo_ngan_sach/` |
| Một test qua đường stream thật (lỗi giữa lượt bão vẫn kèm câu 112) | Đã vào main; thấy đỏ hai lần khi phá code | (ghi ở sổ việc) | — |
| Thử công cụ soát code `ruff` một lần | 401 cảnh báo, 0 lỗi hành vi ⇒ không đưa vào rào commit | (ghi ở sổ việc) | `data/cach_lam_2026-11-18/ruff_2026-11-19/` |
| Kiểm kê các giới hạn của hệ thống | 99 hàng, 97 giới hạn khác nhau (27 đã đo chất lượng · 33 an toàn · 5 tiền / tốc độ · 34 không rõ lý do) + 10 thứ model không được cho biết — agent con lập, phần lớn chưa có người thứ hai kiểm | — | `data/kiem_ke_gioi_han_2026-11-19/` |
| Mốc "Phase 9 xong phần nhóm, kèm danh sách mục chưa đạt" | Ghi trong buổi sáng 19/11 (giờ đúng ở sổ việc); mốc code `55d01a8`; cả bộ test 1.437 đạt, 0 hỏng | sổ việc `session_prompt/CURRENT_HANDOFF.md` | `data/test_rong_2026-11-19/` |

Ai kiểm việc nào (người thứ hai): biên bản review / đọc tay nằm cạnh từng việc trong `data/phase_9/<việc>/` (file tên `*review*`, `doc_tay_*`).

## 2. Quyết định của chủ dự án trong ngày (đủ ở `session_prompt/HIEN_TRANG.md` mục 4)

- Chất lượng trước, chi phí / tốc độ sau: bỏ trần token đầu ra, ngân sách ngữ cảnh, trần lịch sử, sàn tiền / câu và sàn tốc độ chữ đầu; cho dùng tiền API để thử; thử mức suy luận low / medium / high.
- Cách đếm "thiếu cảnh báo mới": phần ngữ cảnh chung tính sàn; ý chỉ có ở nguồn tìm thêm đọc tay.
- Không đầu tư thêm cho câu bão / lũ / khẩn cấp; ưu tiên việc phổ thông mà 100 người dùng thật sẽ thử: hỏi đáp + xác thực · gợi ý quán / chỗ ở / địa chỉ · lịch trình + ngân sách · làm thay (đặt phòng, gửi thư).
- Báo cáo chia theo ngày.

## 3. Đang mở khi viết file này

- Thí nghiệm mức suy luận (kế hoạch đã duyệt, công cụ sẵn; chưa chạy) — `data/phase_9/muc_suy_luan/`.
- Hướng "việc phổ thông": đã có ba bản liệt kê của nhóm, một lượt tra cứu công khai, ba bản tư vấn của model khác hãng; chưa chốt thứ tự làm.
- Thử lại "tìm đoạn nhỏ, đưa cả mục / cả bài vào model" — chưa bắt đầu.
- `bai_hoc/VIEC_MOI_XONG.md`: mới có mục lượt đo cuối; các việc còn lại của ngày chưa viết.

## 4. Tiền API trong ngày (số từng phiên báo, chưa cộng lại từ log)

Thử câu lời dặn ≈ 0,212 USD · bản code cảnh báo ≈ 0,002 · sửa lịch ≈ 0,030 · bỏ trần / bỏ ngân sách ≈ 0,009 ⇒ khoảng 0,25 USD.

## Dòng theo giờ dời nguyên văn từ `session_prompt/CURRENT_HANDOFF.md` (17:47 21/11/2026)

- 22:32 19/11/2026 — tên terminal tối 19/11 (CŨ khi mở lại): A `hue-rag-67` · B `hue-rag-02` · C `hue-rag-c6` · E `hue-rag-29`. Lần "đọc ngắn" thứ sáu: 0 tin rải, 0 lần vấp luật do chưa đọc (tự khai).
