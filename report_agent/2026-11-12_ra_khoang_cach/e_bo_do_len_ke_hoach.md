# Bộ đo "Lên kế hoạch" bản 2 — đợt 1 (mô tả mức loại) — phần của E

Người viết: E · 22:02 12/11/2026 (`date`) · A giao · 0 USD. E không code tính năng, không viết spec / bản thử luật ⇒ bộ đo viết **trước** khi B code bước (b).
Dữ liệu private: `data/phase_9/lich_trinh/bo_do_v2/` — `yeu_cau_20.jsonl` sha256 `8f89c1b341ca` · `bo_quyet_12.jsonl` `f715aac06ddc` · `dinh_nghia_cham.md` `b837ecbb044e` (ghi ba mã này vào plan đợt 1).

## Có gì
| Bộ | Số dòng | Dùng cho | Chạy |
|---|---:|---|---|
| Bộ lịch thật | 20 yêu cầu | kiểm cuối, số câu dự phòng, tốc độ (khung · đủ câu), 6 ý bằng code | có phí, ×1 |
| Bộ quyết | 12 tổ hợp (không trùng bộ trên) | "lịch khớp điều đã chọn", 2 người chấm độc lập | có phí, ×2 lượt; sàn ≥ 11 / 12 mỗi lượt |

Mỗi dòng chỉ là **giá trị các ô của biểu mẫu** (số ngày, số người lớn, số trẻ em, có người lớn tuổi, kiểu đi, tối đa 2 sở thích) + **kiểu ngày đi** (không chọn · trong 7 ngày tới · mùa khô giữa tuần · mùa mưa cuối tuần); ngày thật do code của người chạy tính lúc chạy theo luật ghi trong file định nghĩa (để bộ đo dùng lại được ở lượt sau).

**Độ phủ bộ 20:** mỗi mức 1–5 ngày × 4 · có trẻ em 5 · có người lớn tuổi 5 · kiểu đi 6 / 8 / 6 · không chọn sở thích 3, một sở thích 9, hai sở thích 8 (cả 5 loại, mỗi loại ≥ 3 lần) · mỗi kiểu ngày đi × 5. **Bộ 12:** số ngày 2 / 3 / 3 / 2 / 2 · trẻ em 3 · lớn tuổi 3 · kiểu đi 3 / 5 / 4 · mỗi kiểu ngày × 3.

## "Lịch khớp điều đã chọn" — 6 ý
(1) đúng số ngày, ngày nào cũng có điểm · (2) nhóm hạn chế: không buổi tối muộn, mỗi buổi ≤ 1 điểm · (3) kiểu đi · (4) mỗi sở thích có mặt hoặc có ghi chú vì sao không · (5) hoạt động tối đúng thứ · (6) mùa mưa / dự báo mưa có dòng nhắc, mùa khô thì không. Thêm hai điều kiện loại ngay do code đếm: có số tiền hoặc tên ngoài bảng; > 30 % mục dùng câu dự phòng.

**Hai chỗ E viết khác chữ spec 5c.7 (đã báo C, B, A; ghi ở phần kiểm 5c):**
- Ý (3): spec ghi "khám phá 3–6 điểm / ngày" — không đạt được (quỹ 240 phút chỉ cho 2 điểm / buổi; 3 / 8 cụm không có điểm ngắn) ⇒ bộ đo dùng phép **đếm bằng code theo cặp**: cùng các ô khác, tổng số điểm nhẹ nhàng ≤ cân bằng ≤ khám phá và khám phá > nhẹ nhàng; người chấm chỉ chấm vế đọc được.
- Ý (4): spec ghi "mỗi sở thích có ≥ 1 điểm ưu tiên" — không đạt được ở lịch ngắn khi điểm ưu tiên chỉ nằm ở cụm xa, hoặc nhóm hạn chế hết suất ⇒ thêm vế "hoặc có ghi chú nói rõ không xếp được".

## Giới hạn
Giá trị ô do E đặt, không phải lựa chọn của người dùng thật; 32 dòng không thay cho mô phỏng 3.840 tổ hợp (0 USD, B chạy); vế "dự báo mưa" phụ thuộc thời tiết hôm chạy — hôm không mưa thì chỉ test có dự báo ghi sẵn kiểm được.
