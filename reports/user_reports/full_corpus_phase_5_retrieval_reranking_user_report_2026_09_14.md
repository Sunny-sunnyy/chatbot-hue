# Báo cáo dành cho người dùng: Giai đoạn 5 - Truy xuất toàn corpus và xếp hạng lại

```text
Trạng thái: Đã được người dùng xác nhận
Cập nhật lúc: 14-09-2026 09:50 +07
Xác nhận closure: 14-09-2026 +07
```

## 1. Bạn nhận được gì

Phase 5 bổ sung đường truy xuất local cho bốn kho vector toàn corpus. Mỗi kho có
thể chạy hai cách kết hợp semantic/lexical và có thể bật hoặc tắt MiniLM
reranker. Kết quả cuối là Top 10 có thứ tự xác định, kèm trace kỹ thuật nội bộ
đủ giải thích các stage nhưng không đưa nội dung riêng tư vào báo cáo tracked.

Phase này đã chứng minh hệ thống tuân thủ contract và chạy được với Qdrant cùng
các model thật. Nó chưa đánh giá model nào trả lời hay nhất và chưa thay đổi
production.

## 2. Hệ thống hoạt động như thế nào

Một câu hỏi được mã hóa bằng đúng model của collection đã chọn. Hệ thống lấy
dense candidates, sau đó kết hợp với BM25 local hoặc một sparse query độc lập,
dùng RRF để tạo thứ tự chung và tùy cấu hình có thể rerank bằng MiniLM. Mọi
payload trả về được kiểm schema trước khi đi tiếp; lỗi dependency được báo rõ,
không âm thầm fallback.

## 3. Codex đã chạy và quan sát gì

| Nội dung | Kết quả quan sát | Ý nghĩa |
|---|---|---|
| Focused retrieval/Foods regression suite sau Correction 3 | `23 passed, 1 warning in 63.14s` | Type guard mới đạt và Foods behavior vẫn được bảo toàn |
| Direct malformed-role probe | 7 nhóm giá trị sai đều trả typed dependency error | Payload dạng array/object không còn gây raw `TypeError` |
| `git diff --check` | Đạt | Diff không có lỗi whitespace |
| Selected live Qdrant/model matrix từ Correction 2 | Reuse hợp lệ: `8/8 PASS`, deterministic, không anomaly | Bốn candidates và hai treatments đã chạy trên normal path thật |

Live matrix không chạy lại sau Correction 3 vì delta chỉ thêm type guard cho
payload malformed; input, dependencies, environment và normal data flow không
đổi. Full 16-cell/MiniLM, selector, safe-output và privacy evidence từ cùng
implementation series cũng vẫn hợp lệ.

## 4. Cách bạn kiểm tra thêm nếu cần

Bạn không bắt buộc chạy lại kỹ thuật để xác nhận. Phase 5 không có notebook mới
vì notebook không mang thêm giá trị so với runtime và báo cáo hiện có.

## 5. Giới hạn và bước tiếp theo

Phase 5 chưa đo retrieval quality, chưa chọn model/treatment thắng, chưa cutover
production và không thay đổi collection. Những quyết định đó thuộc các phase
sau và vẫn cần scope cùng phê duyệt riêng.

Người dùng đã xác nhận closure Full-corpus Phase 5 ngày 14-09-2026 +07. Phase
tiếp theo vẫn đóng cho tới khi có một nhiệm vụ thiết kế mới được giao rõ ràng.
