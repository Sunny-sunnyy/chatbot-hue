# Plan (một trang) — "sự kiện theo ngày": hỏi "tối nay / cuối tuần này / tháng 3 ở Huế có gì" (C, 15:53 20/11/2026, giờ `date`; nền main `f6fe2279`; CHỜ phiên điều phối duyệt — chưa viết dòng code nào, 0 USD)

**Điều chủ dự án ĐÃ chốt (nguyên văn):** `bao_cao_he_thong/93_DE_XUAT_TINH_NANG_MO_RONG_PHASE_9.md:10` — "Phase 11 = trải nghiệm Huế (bản đồ, sự kiện theo ngày, tiếng Anh, ăn gần, ứng xử)" (05/11);
cùng file dòng 70 tả ý này: "'Tối nay / cuối tuần ở Huế có gì': sự kiện theo ngày đi … lịch dễ cũ ⇒ ghi nguồn + ngày; chỉ nêu sự kiện có ngày trong nguồn". Spec Phase 9 dòng 442: "sự kiện theo ngày ⇒ Phase 11".
**Chỗ chưa rõ, nói thẳng:** (1) "theo ngày đi" có thể hiểu là sự kiện hiện TRONG lịch "Lên kế hoạch" theo ngày khách đi — bản dưới KHÔNG làm phần đó, chỉ làm ở ô hỏi đáp;
(2) chưa có spec riêng nào (đợt 2 của cổng ghi "spec riêng, sau nghiên cứu" — không thấy file).

**Kho hiện có gì (C đếm bằng `scripts/grep_kb.sh`, đọc dòng "Thời gian" của từng bài; chưa ai đếm lại):**
| Nhóm | Số bài | Ví dụ dạng ngày |
|---|---:|---|
| Lễ hội có NGÀY cố định hằng năm (đa số âm lịch) | **17** / 39 bài lễ hội | "ngày 22 tháng Giêng âm lịch", "15 đến 17 tháng 7 âm lịch", "ngày 2 tháng 9" |
| Lễ hội chỉ có KHOẢNG (tuần / tháng) | 8 | "trung tuần tháng Giêng âm lịch", "khoảng tháng 5 đến tháng 6 dương lịch" |
| Lễ hội "theo kế hoạch / thông báo từng năm", không có ngày | 8 | Festival bốn mùa, lễ hội ẩm thực, áo dài, diều… |
| Nghi lễ triều Nguyễn chỉ tái hiện không định kỳ | 5 | ngày lịch sử, không phải lịch hằng năm |
| Hoạt động LẶP THEO TUẦN / hằng đêm (bài nghệ thuật + địa điểm) | 3–4 | ca Huế hằng đêm, phố đi bộ tối cuối tuần, suất diễn ở Đại Nội |
Nghĩa là: 17 ngày cố định dồn vào tháng Giêng, tháng 5, tháng 7, tháng Chạp âm ⇒ một tuần bất kỳ thường KHÔNG có lễ hội nào; thứ trả lời được câu "tối nay / cuối tuần có gì" nhiều nhất
lại là 3–4 hoạt động lặp theo tuần. Kho KHÔNG có sự kiện một lần (hoà nhạc, hội chợ của năm nay). Lượt đếm 12/11: 4 / 6 câu sự kiện kho đã trả lời đủ; 2 câu hỏng là
"cuối tuần này có sự kiện gì" (từ chối) và "lễ hội X lần tới rơi ngày dương nào" (từ chối dù có bài).

**Bản NHỎ NHẤT đề nghị (không thêm nguồn, không sửa kho, không trang mới):**
1. **Một bảng nhỏ dẫn xuất từ kho** (~28 dòng = 17 + 8 + 3–4): tên · bài nguồn · loại lịch (âm / dương / theo tuần) · ngày hoặc khoảng · ghi chú chu kỳ chép nguyên từ bài ("đại lễ 3 năm một lần"…).
   C soạn tay từ dòng "Thời gian" của bài; một script kiểm MỖI dòng: chuỗi ngày của dòng có mặt trong đúng bài nguồn (không khớp ⇒ dừng). Người thứ hai đọc 100 % dòng. Kho đổi ⇒ chạy lại script.
   Các bài "theo kế hoạch từng năm" KHÔNG vào bảng (không có ngày thì không nêu — đúng chữ đã chốt).
2. **Hàm thuần** `su_kien_trong_khoang(bang, tu, den)`: đổi ngày âm ⇒ dương bằng hàm đang có (`llm/ngay_lich.py`), trả các dòng rơi vào khoảng; không có dòng nào ⇒ trả sự kiện GẦN NHẤT sắp tới.
3. **Chỗ gắn** (mẫu "Lịch hệ thống" đang chạy, `assistant.py` `_nguon_lich_san`): câu gõ vừa có từ chỉ ngày (code đã dò: hôm nay, tối nay, cuối tuần, tuần sau, tháng này, một ngày cụ thể)
   vừa có từ hỏi sự kiện (danh sách hẹp: lễ hội, sự kiện, hoạt động, "có gì") ⇒ code nối MỘT nguồn "Lễ hội và hoạt động theo ngày (theo các bài của kho)" vào ngữ cảnh trước lần gọi model đầu;
   model chỉ diễn đạt và trích nguồn đó. Mỗi dòng nguồn kèm chữ "ngày có thể đổi theo thông báo của ban tổ chức". Cờ `su_kien_theo_ngay`, mặc định TẮT; câu không khớp cổng ⇒ chuỗi gửi model giống byte.

**Tiêu chí ghi TRƯỚC:**
- Bảng: script khớp 100 % dòng; người thứ hai đọc 100 % dòng, 0 dòng sai ngày / sai bài.
- Hàm thuần (test, có ca đỏ trước): khoảng chứa một ngày âm đầu năm (vắt qua Tết dương) · khoảng không có gì ⇒ trả đúng sự kiện gần nhất · hoạt động theo tuần đúng thứ.
- Sàn (đọc bằng máy trên lượt thật): 0 lễ hội được nói là "diễn ra trong khoảng hỏi" mà bảng không xếp vào khoảng đó; 0 ngày dương trong câu trả lời khác ngày code tính.
- Lượt thật MỘT lần, cặp cờ tắt ↔ bật cùng buổi: 6 câu của lượt 12/11 + 4 câu mới (tối nay · cuối tuần này · tháng Giêng âm · một ngày không có gì) ⇒ bật: 0 / 10 câu bị từ chối khuôn; câu "không có gì" phải nói thật là kho không ghi lễ hội cố định nào trong khoảng đó.
  Ước ≈ 20 lượt × 0,001 ≈ 0,02 USD, trần 0,04. Bộ an toàn / bộ câu mẫu KHÔNG chạy lại: câu không qua cổng thì giống byte (kiểm bằng phép chụp có sẵn).
- Không đạt một dòng ⇒ cờ TẮT, báo phiên điều phối (không lặng lẽ ghi giới hạn).

**Không làm ở bản này:** sự kiện một lần của năm · tra web cho sự kiện · hiện sự kiện trong lịch "Lên kế hoạch" · trang / thẻ riêng · đọc ngày tự động bằng regex lúc chạy (chữ trong bài lẫn ngày lịch sử "năm 1807", dễ sai).
**Rủi ro:** cổng đọc chữ người dùng ⇒ cần bộ dò nhỏ của phiên khác (nối nhầm = thêm một nguồn thừa vào ngữ cảnh, có thể kéo lệch câu trả lời — nặng hơn nối nhầm một dòng ghi chú, nên cổng phải hẹp) ·
ngày âm của năm nhuận · bài kho ghi "thường", "tuỳ năm" ⇒ dòng nguồn giữ nguyên chữ đó.
**Cần phiên điều phối quyết trước khi viết code (một câu mỗi ý):** (a) bảng dẫn xuất ~28 dòng có cần chủ dự án duyệt như các bảng lịch trước đây, hay người thứ hai đọc 100 % là đủ; (b) có nhận cách hiểu "chỉ ở ô hỏi đáp" cho chữ "theo ngày đi" không.
**Ý C:** với 17 ngày cố định + 3–4 hoạt động theo tuần, đây là tính năng NHỎ nhưng làm được trọn và chữa đúng câu đang hỏng ("cuối tuần này có gì"); phần giá trị nhất là nói thật "khoảng này kho không ghi lễ hội nào, gần nhất là …" thay cho câu từ chối.
