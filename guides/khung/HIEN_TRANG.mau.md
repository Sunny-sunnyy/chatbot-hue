# HIỆN TRẠNG <tên dự án> — trang agent đọc khi mở phiên (MẪU — chép sang dự án khác rồi điền)

<!-- Cách dùng mẫu: chép file này thành `HIEN_TRANG.md` ở nơi `AGENTS.md` của dự án trỏ tới; xoá các dòng chú thích trong ngoặc nhọn; điền từng mục.
     Bản đã điền của dự án hue_rag: `session_prompt/HIEN_TRANG.md`. Ý tưởng: tách "bộ nhớ khởi động" (ngắn, viết lại tại chỗ, bắt đọc) khỏi "nhật ký"
     (nối đuôi, dài bao nhiêu cũng được, KHÔNG bắt đọc). -->

Viết lại lần cuối: <giờ lấy bằng lệnh `date`>, trên nhánh chính <mã commit>. Người giữ: <ai viết lại trang này mỗi lần kết phiên>.

**Trang này là gì.** <2–3 câu: ảnh chụp "bây giờ"; viết lại tại chỗ, không nối thêm; đọc `AGENTS.md` + trang này là đủ để bắt đầu; file nào thắng khi lệch nhau.>

Từ dùng trong trang: <5–8 từ riêng của dự án mà một agent mới sẽ không hiểu — mỗi từ một vế giải nghĩa.>

## 1. Hệ thống đang chạy
<Là gì, cho ai, chạy ở đâu (một câu). Các con số hôm nay (dữ liệu, model, dịch vụ ngoài). Tính năng đang BẬT / đang TẮT — đọc từ file cấu hình, không chép lịch sử.
 Trỏ sang: trang lời thường cho chủ dự án; danh sách giới hạn đã biết.>

## 2. Mốc và việc đang mở
<Bảng bước theo thứ tự + điều kiện đạt (ngày chỉ là ghi chép). Một câu "trước mốc X thì không được làm gì". Việc đang mở KHÔNG chép ở đây: một dòng trỏ sang mục lục việc
 (`VIEC_DANG_MO.mau.md`) — hai nơi cùng ghi thì sẽ lệch nhau. Dự án nhỏ chưa có mục lục việc: ghi thẳng ai · việc · trạng thái · nhánh ở đây.>

<Các con số đo cách làm (trang cách làm việc mục 7) ghi ở MỘT nơi là sổ cải tiến; trang này chỉ trỏ.>

## 3. Đang chờ chủ dự án
<Gom MỘT chỗ mọi thứ đang chờ người quyết / người làm. Mục nào chưa chắc còn hiệu lực thì ghi "chưa kiểm". Thứ không có ở đây thì agent không hỏi lại.>

## 4. Quyết định còn hiệu lực — không hỏi lại
<≤ 25 dòng, chia "Sản phẩm" và "Cách làm". Mỗi dòng là một quyết định viết thành việc làm được ngay; không kể chuyện vì sao (để ở nhật ký). Cuối mục trỏ nơi có danh
 sách đủ kèm ngày.>

## 5. Bật hệ thống và kiểm
<Trỏ runbook (lệnh từng bước). Ghi 2–3 điều hay vấp nhất ngay tại đây.>

## 6. Lệnh kiểm các con số của trang này
<Bảng: kiểm gì · lệnh · phải ra gì · nhãn [đã chạy <ngày>] / [chưa chạy]. Mọi con số ở mục 1 phải có một dòng ở đây.>

## 7. Nhật ký ở đâu (không bắt đọc)
<Đường dẫn: thư mục báo cáo theo NGÀY (tổng hợp ngày, nhật ký từng phiên), lịch sử quyết định, sổ riêng từng phiên, mục lục việc. Một vế cho biết mở chỗ đó khi cần trả lời loại câu nào.>

## 8. Cách giữ trang này
<Ai viết lại, lúc nào; giới hạn cỡ (gợi ý ≤ 150 dòng và ≤ 12.000 byte — có công cụ cắt file hướng dẫn dài mà không báo); quyết định mới thêm ngay trong phiên.>

## Phép thử (chạy mỗi khi trang đổi nhiều; 0 đồng, ~10 phút)

Mở một agent ngữ cảnh MỚI (tốt nhất khác hãng), chỉ cho đọc `AGENTS.md` + trang đã điền, cấm mở file khác, hỏi tám câu. Câu nào sai hoặc "không thấy" ⇒ trang
thiếu chỗ đó, sửa trang rồi hỏi lại đúng câu ấy.

1. Dự án này là gì, cho ai dùng, đang chạy ở đâu?
2. Kể ba việc hệ thống đang làm được và một tính năng đang tắt (kèm lý do tắt); danh sách đủ các tính năng bật / tắt nằm ở file nào?
3. Mốc gần nhất là gì, điều kiện đạt là gì, và trước mốc đó không được làm gì?
4. Ai đang làm việc gì? Việc nào chưa ai nhận?
5. Bạn được tự làm những gì mà không cần hỏi, việc gì phải hỏi trước, việc gì không bao giờ làm?
6. Muốn bật hệ thống và chạy test thì mở tài liệu nào, mục nào? Điều gì hay vấp?
7. Kể ba điều chủ dự án đã chốt mà bạn không được hỏi lại.
8. Việc nào đang chờ chủ dự án? Nếu gặp một hành vi trông như lỗi, bạn tra ở đâu trước khi sửa?
