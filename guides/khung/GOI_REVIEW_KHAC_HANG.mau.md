# Đề bài review độc lập — <việc cần soi> (<tên dự án>, bản `<mã commit>`)

Soạn <giờ lấy bằng `date`> bởi <ai>. Người gửi file này cho bạn là chủ dự án. Bạn là **người review khác hãng**: bạn không viết dòng code nào ở đây, và bạn KHÔNG
được cho biết nhóm đã tìm ra gì — để kết quả của bạn không bị dẫn dắt.

## 1. Bối cảnh (đủ để làm, không cần đọc tài liệu điều phối)
- Thư mục làm việc: <gốc repo>, nhánh <…>, commit `<…>`. Sản phẩm là gì, dựng bằng gì, code ở đâu — 3–5 dòng.
- Điều vừa thay đổi / phạm vi cần soi — 3–5 dòng.
- Bản đồ để đọc code: <file nào tả từng tính năng> · bẫy đã biết (đừng báo lại như phát hiện mới): <file nào>.

## 2. Việc của bạn
<Một câu hỏi rõ.> Ví dụ: "Tìm chỗ HAI tính năng gặp nhau mà bộ test hiện có không bắt được." Không chấm phong cách, không đề nghị dọn code.
Ưu tiên theo hậu quả với người dùng: <thứ tự lỗi của dự án, nặng → nhẹ>.
Gợi ý chỗ soi (không giới hạn): <3–6 gợi ý>. File chính: <danh sách>.

## 3. Ranh giới (bắt buộc)
- **Chỉ đọc.** Không sửa file nào của repo, không commit, không đẩy, không cài gói. File DUY NHẤT bạn được ghi là file kết quả ở mục 4.
- **Không mở, không in:** file khoá; <các thư mục dữ liệu riêng>.
- Không gọi API trả phí, không bật server. Được chạy lệnh đọc (`git log`, `git show`, tìm chữ) và <lệnh chạy hàm thuần của dự án, nếu có>. Không chạy được thì ghi "[chỉ đọc code]".
- Không chép dữ liệu riêng vào kết quả.

## 4. Kết quả — ghi vào `<đường dẫn>/KET_QUA_<tên model>.md`
1. Dòng đầu: tên model + mức suy luận + giờ bắt đầu / kết thúc (lấy bằng lệnh `date`).
2. Bảng phát hiện, nặng → nhẹ: # · chỗ nào (`file:dòng`) · đầu vào nào ⇒ ra gì (cụ thể) · bằng chứng gắn nhãn **[đã chạy]** (kèm lệnh + đầu ra) hoặc
   **[chỉ đọc code]** · vì sao test hiện có không bắt · mức (người dùng thấy / lệch log-tiền / chỉ lý thuyết) · đề nghị (ghi giới hạn / sửa nhỏ / cần đo).
3. Mục "Đã soi, thấy ổn" — mỗi dòng trỏ test đang khoá.
4. Mục "**CHƯA đọc gì / chưa kiểm gì**" — khai thật; file nào chỉ lướt thì ghi là lướt.
5. Kết luận nặng ("nghiêm trọng", "chắc chắn") phải kèm lệnh + đầu ra, hoặc ghi rõ "nghi, chưa chứng minh".

## 5. Cách dùng kết quả (để bạn biết mình được chấm thế nào)
Danh sách của bạn sẽ được so với danh sách của một reviewer cùng hãng với người viết: điểm nào trùng, điểm nào chỉ bạn thấy; mỗi điểm chỉ bạn thấy sẽ được chạy lại
để xác nhận. Phát hiện ít mà đúng có giá hơn nhiều mà đoán.

---
*Ghi chú cho người soạn (xoá trước khi gửi):* file phải tự đủ — người review không có lịch sử trò chuyện. Chủ dự án tự mở công cụ hãng khác và gửi file; agent không tự gọi
công cụ đó. Lưu cả đề bài lẫn file kết quả cạnh nhau (ngoài git nếu chứa chi tiết riêng). Mẫu này rút từ một lần dùng thật ngày 18/11/2026.
