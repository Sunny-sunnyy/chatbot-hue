# Tổng hợp ngày 19/11/2026 (thứ Năm)

Viết: 10:56 19/11/2026 (giờ `date`), phiên điều phối. Thư mục này gom mọi báo cáo viết trong ngày — từ 19/11 mỗi ngày làm việc một thư mục `report_agent/<năm-tháng-ngày>/` (chủ dự án yêu cầu). Phần riêng tư (kết quả đo có câu của bộ đo, kế hoạch, câu dò) không vào repo công khai; file này chỉ trỏ tên thư mục trong `data/`.

## PHIÊN SAU ĐỌC TRƯỚC (GHI ĐÈ lúc kết phiên; ≤ 20 dòng) — viết 13:42 19/11/2026, kết phiên nhẹ đầu chiều, chủ dự án mở lại cả bốn phiên

- **Thứ tự mở đầu:** `session_prompt/HIEN_TRANG.md` ⇒ `session_prompt/VIEC_DANG_MO.md` (6 việc; bước kế CHỈ ghi ở đó) ⇒ `session_prompt/sessions/STATUS_A.md` mục 1, 3, 5.
- **Máy:** dùng chung ba dự án; trưa nay chạm sàn 4 GB RAM một lần (một tiến trình pytest 20 file của nhóm lên 2,8 GB — đã dừng). Từ giờ: test dựng cả app chạy từng file ở cây chính, không chạy cùng lúc với server; trước việc nạp model nhìn `free -m`. Qdrant bật, 9.436 điểm.
- **Đã có số buổi trưa:** thí nghiệm mức suy luận bậc 1 (ba mức gần bằng nhau về tiền / giây; cổng đạt) · bộ 80 kịch bản phổ thông (xong việc 51 / 80 chấm nới, 40 sát chữ; nguyên nhân gốc đã xếp hạng) · bước đếm 0 USD của việc "ngữ cảnh lớn hơn". Đã vào main: bản sửa "lượt báo thành công nhưng câu trả lời rỗng" (`76ef380`; chưa chạy cả bộ test, chưa có lượt thật) · các mục 7–11 của `bai_hoc/VIEC_MOI_XONG.md` kèm kết quả thử tay.
- **Chủ dự án chọn buổi trưa:** bậc 2 mức suy luận chỉ medium + low · thứ tự sửa: lịch đã lưu vào lượt hỏi thường ⇒ nói thật giới hạn thay câu từ chối khuôn ⇒ các bước cũ · việc "ngữ cảnh lớn hơn" vượt 1 USD vẫn duyệt.
- **Đang chờ chủ dự án:** cách có giá vé cho "tổng tiền vé của lịch" (ba phương án, đã nêu) · câu chữ "nói thật giới hạn". Hộp hỏi hôm nay: 9 ⇒ gom câu.
- **Đang chạy lúc viết:** phần sinh bậc 2 mức suy luận (phiên B cũ bật nền) — phiên mới kiểm file kết quả đủ dòng chưa.
- **Chưa làm cho ngày này:** cả bộ test trên bản mới · sao lưu ổ D cho mốc · cắt `CURRENT_HANDOFF.md` · vòng cải tiến cuối ngày · `bai_hoc/` cho việc buổi chiều.
- **Bẫy của ngày:** `STATUS_A.md` mục 7; nhật ký `b_nhat_ky.md`, `c_nhat_ky.md`, `e_nhat_ky.md`.

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
