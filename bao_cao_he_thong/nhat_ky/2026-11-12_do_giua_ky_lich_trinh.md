# Nhật ký 12/11/2026 — đo giữa kỳ, soi lại với Huế TRIPO, thiết kế lịch trình mới

**Cập nhật lần cuối: 22:26 12/11/2026.** Tiền trong ngày: ≈ 0,73 USD API (B ≈ 0,479 · E ≈ 0,195 · C ≈ 0,059 · A ≈ 0,001) + ≈ 0,82 USD tín dụng miễn phí của Exa. Hành vi chatbot **không đổi** (code mới nằm sau một cờ đang tắt).

## Tóm tắt
- Mở 18:40, bốn session. Anh chốt: **chưa deploy, chưa đóng Phase 9**; lượt B7 hôm nay là **đo giữa kỳ**.
- **B7 giữa kỳ** (so trợ lý hiện tại với bản RAG Phase 1–8, cùng kho): trợ lý hơn ở cả 3 nhóm — câu theo ngày dùng được 27 ↔ 11 / 28; câu hỏi tiếp điểm "đủ ý" 5,00 ↔ 3,33; câu nhiều nguồn 4,44 ↔ 3,44; từ chối nhầm câu trong kho 3 ↔ 13 / 158. Ba sàn bị phạm, ghi nguyên: 2 / 44 câu ngoài phạm vi mở tra web; thiếu cảnh báo ở 1 câu miễn / giảm vé; 1 lượt hỏi tiếp ngoài kho bị trả lời. Hai chỗ đạt đúng ngưỡng, hết biên: 4 câu tụt điểm; mục web 6 / 10.
- **Đếm lỗi trước khi xây** (0 USD trên kết quả B7 + vài chục câu tự viết): hạ 3 ứng viên (sửa lời dặn bớt từ chối; kiểm số tiền / giờ; 4 câu tụt), giữ: câu "ăn gần điểm X", đi lại / thuê xe, lưu trú, đường web chậm.
- **"Hết lượt tìm thì dừng"**: code + đo xong, gộp vào `main` với cờ **tắt**. Câu kho thiếu hẳn nhanh hơn ~6,7 giây (22,85 ⇒ 16,15 giây, 8 / 8 câu). Bật hay không: chờ anh.
- **Exa** (anh cấp khoá): ở riêng bước tra, Exa cho 25 mục web trả lời được so với 17 của Serper; nhưng đo **qua server thật** chỉ 14 so với 13 ⇒ không đạt luật ghi trước ⇒ **giữ Serper**.
- **Huế TRIPO**: anh tự thử và chụp phần lập kế hoạch; chỉ ra các vòng thử trước của agent không chạy phần này (lỗi do A dặn "không gửi biểu mẫu"). Vòng 6 chạy lại đủ luồng có lưu ảnh: xong 2 / 6 cấu hình, còn dở.
- **Lịch trình**: phát hiện 7 / 28 điểm (gồm chùa nổi tiếng nhất và 5 lăng) không bao giờ được xếp; nút "đi dày" không đổi lịch. Anh chốt mức **"đủ 4 phần, 1 lịch"** (tham quan, ăn uống theo buổi, lưu trú, buổi tối; biểu mẫu đầy đủ; ảnh; bản đồ). Bản thiết kế bản 3.3 + kế hoạch đợt 1 + bộ đo đã xong; **chưa code**.
- **Đợt bổ sung kho 3** (khách sạn theo khu, bài đi lại, quán gần điểm tham quan): bản thiết kế đã duyệt; đã tải 316 cơ sở lưu trú và 581 quán từ OpenStreetMap vào `data/`; **chưa đưa gì vào kho**.

## Đính chính trong ngày (đã sửa ở report)
- Bộ dữ liệu mở về nơi ăn uống có 6.794 **dòng** nhưng chỉ 208 cơ sở khác nhau (các số "276 quanh Đại Nội", "174 quanh Thiên Mụ" là số dòng).
- Bài quán có câu định vị: 12 / 81 (không phải 15 / 81). Nhóm nhiều nguồn: 6 tăng / 11 hoà / 1 tụt (không phải 5 / 12 / 1). Gán khu lưu trú: 54 % (không phải 71 %).

## Bạn cần làm gì (phiên sau A hỏi từng câu)
- Cấp quyền phiên + trần tiền Phase 9 mới.
- Quyết bật cờ "hết lượt tìm thì dừng".
- Liếc danh sách điểm ưu tiên theo sở thích; xem phiếu ảnh (`data/phase_9/lich_trinh/phieu_anh_2026-11-12.md`).
- Quyết có đưa quán từ OpenStreetMap vào kho không (phía đầm Chuồn / Thuận An vẫn gần như chưa có quán ở mọi nguồn).

## Mã / đường dẫn
B7: `report_agent/2026-11-08_phase_9_ban_13/b7_implementation.md`. Đợt hôm nay: `report_agent/2026-11-12_ra_khoang_cach/`. Thiết kế: `docs/superpowers/specs/2026-11-12-len-ke-hoach-ban-2-design.md`, `docs/superpowers/specs/2026-11-12-bo-sung-kho-dot-3-design.md`. Merge `cd1f6ef`; tag `hoso/p9-tra-web-exa`.
