# Nhật ký phiên C — 19/11/2026 (file NỐI; mỗi việc ≤ 3 dòng: việc · kết quả + sha · tiền · bẫy)

Tạo 11:20 19/11/2026 (giờ `date`) lúc kết phiên nhẹ. Sổ cũ nguyên văn: `session_prompt/archive/STATUS_C_LICH_SU_2026-11-18_19.md`. Dữ liệu riêng tư ở `data/` (không vào git).

## Việc đã xong trong ngày (theo thứ tự làm)
1. **Câu thiếu cảnh báo "tạm ngừng mùa lũ" — bản LỜI DẶN** (cờ `luu_y_an_toan`, nhánh `p9-c-s09-luu-y-an-toan` `2d613ce`, KHÔNG vào main): ý được nêu 8 / 8 lần, sàn an toàn đạt, nhưng bộ câu mẫu "Đủ ý" 7 câu tụt > ngưỡng 5 ⇒ KHÔNG ĐẠT, không đo lại. **0,21179 USD.** Bẫy: đổi chữ lời dặn sau khi người review đã đọc nhánh.
2. **Cùng việc — bản CODE** (cờ `noi_dong_tam_ngung`, `backend/llm/luu_y_nguon.py`; đã ở main `55d01a8`, cờ BẬT theo lựa chọn của User): nối đúng 7 / 7 lần trên dữ liệu cũ, 0 nối trùng, 0 dòng của nơi khác; lượt thật 2 / 3. Report `c_s09_noi_dong_tam_ngung_implementation.md`. **0,00213 USD.** Bẫy: `git checkout` xoá sửa chưa commit; hàm đọc từng dòng chép mẩu câu cụt (người review bắt); chạy pytest `-q -q` mất dòng tổng.
3. **Số nhiễu "số câu tụt" của bản trợ lý** (hai lượt bộ câu mẫu cờ tắt, cách một ngày, chấm cùng lô mù): Đúng 1 · Đủ ý 2 · Trọng tâm 7 — `data/phase_9/s09_luu_y/KET_QUA.md` mục 3. Kèm: bản chụp yêu cầu gửi model đổi theo NGÀY (13 / 228 dòng) ⇒ chỉ so với main chụp cùng buổi.
4. **Bộ dò cho hàm "dời hai điểm" của B**: 43 câu + bộ bù 20 câu; bản đầu 4 câu áp sai, sau hai lần sửa 0 / 63. 0 USD.
5. **Tài liệu**: trang hiện trạng viết lại hai lần (25 cờ bật, hướng việc phổ thông, mục 2 chỉ còn bảng bước + trỏ mục lục việc, mục 4 tách "User tự nêu" ↔ "User chọn ô") · runbook 10.1 một hàng giới hạn · một dòng runbook điểm sửa lịch. Bẫy: trang sát trần 14.000 byte — cổng `[ cỡ ≤ 14000 ] &&` chặn đúng bốn lần.
6. **Script cách làm theo ngày** `scripts/mo_ngay.sh` (mở ngày + lệnh `kiem`) + một dòng cảnh báo trong `scripts/commit_push.sh` — đã ở main. Bẫy: vòng đếm sau dấu ống mất bộ đếm; hai lần commit / push bằng git thường thay `scripts/commit_push.sh` (vấp luật đã đọc: 1).
7. **Đọc / phản biện (0 USD)**: nhánh nhật ký của B (ready) · nhánh trang cách làm việc của E (4 chỗ sửa chữ) · bảng kiểm kê giới hạn · vòng tự soi · cách làm theo thư mục ngày · góc lịch trình + ngân sách của hướng việc phổ thông (kho có giá vé 6 / 6 bài, món ăn 83 / 111 bài; đi lại + chỗ ở gần như không có giá; ba bảng lịch không có cột giá).

### Buổi trưa (phiên mở 11:25 19/11/2026; C ghi 13:21 19/11/2026, giờ `date`) — 0 USD
8. **Plan "đưa ngữ cảnh lớn hơn vào model"** (việc 3 của mục lục việc; riêng tư): bản duyệt `689f192dc249` sau hai vòng review của B. Bước đếm 0a + 0b xong: 15 đoạn (N chọn theo luật ghi trước) thêm đủ đoạn đúng ở 7 câu, "cả mục" 6 câu, trên 55 câu có nhãn ⇒ cổng đang ở vùng "6–9, phiên điều phối quyết", chờ người đọc 26 câu yếu. Công cụ bọc bước tìm + chạy có phí đã viết, chưa chạy lượt có phí nào. Bẫy: phép đối chứng "10 đoạn giống bản đang chạy" lúc đầu RỖNG (B bắt) — đã thay bằng so từng đoạn, đã thấy đỏ.
9. **Đọc tay bậc 1 thí nghiệm mức suy luận** (37 câu × 3 mức + 8 câu an toàn × 3): 0 nói chắc sai mới ở low / high; một dấu hiệu thiếu cảnh báo ở low (một câu an toàn, một lần chạy); không thấy khác biệt nhất quán về đủ ý. Cổng sang bậc 2 đạt cho cả hai.
10. **Chấm 80 kịch bản phổ thông** (độc lập với B): xong việc 53 / 80 · có điều sai 4 · hỏi lại / quá dài 2. Lỗi nặng nhất: lượt hỏi thường không thấy lịch đã lưu nên trả lời trên một lịch khác (3 ca).
11. **Review** nhánh sửa "trả lời rỗng" của B (ready; test mới đỏ khi bỏ bản sửa — C tự chạy; một ca còn sót ghi vào report) · liếc diff công cụ chấm hai bên của B (đạt).
12. **Sửa nhãn bằng chứng** ở report bản code câu thiếu cảnh báo: C đã ghi "người thứ hai kiểm" cho việc người khác chỉ ĐỌC — báo xong bị lật lại: 1.
13. **Test đổi cờ `noi_dong_tam_ngung`**: 31 đạt / 0 hỏng, cả có lẫn không `--env-file` (RSS 130 MB). SỰ CỐ trước đó: C chạy 20 file test trong một tiến trình (hiểu "file chạm cờ" quá rộng), xâu sẵn lượt hai ⇒ RAM cả máy chạm sàn, phiên điều phối phải dừng tiến trình. Bẫy: việc nặng chạy TỪNG lệnh, đo RSS trước, không xâu hai lượt trong một lệnh nền.

## Tiền thật của C trong ngày
0,21179 (lượt đo bản lời dặn) + 0,00213 (lượt thật bản code) = **0,2139 USD**. Buổi trưa: 0 USD. Hai con số cả ngày: báo xong bị lật lại 1 (nhãn bằng chứng, mục 12) · User phải nhắc lại 0.

## Việc ĐANG DỞ — xem `session_prompt/sessions/STATUS_C.md`
