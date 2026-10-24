# Mẫu báo cáo khâu cho User — `bao_cao_he_thong/BAO_CAO_<KHÂU>.md`

Mỗi khâu một file **sống**: sửa tại chỗ khi khâu đổi, không tạo file mới theo ngày (chuyện theo ngày
nằm ở `nhat_ky/`, mẫu `TEMPLATE_NHAT_KY.md`). Quy tắc chung: `WORKFLOW.md` §6. Lời thường, số kèm ý
nghĩa, không chép corpus/Golden/secret.

```markdown
# Báo cáo cho bạn: <Khâu> (Phase <số>)

**Cập nhật lần cuối: <HH:MM DD/MM/YYYY lấy bằng `date`> — bản <N>: <mục nào mới / đổi gì>.**
Người viết: <X> · Review: <Y>. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- Khâu này làm gì, đang chạy cách nào (công cụ / thư viện / thông số).
- Lợi đo được (số trước ⇒ sau, bộ đo nào).
- Giới hạn chính.
- Chi phí / tốc độ nếu có.
- Bạn cần quyết gì (nếu có).

## 2. Hoạt động thế nào (bản đang chạy)

Luồng bằng lời thường hoặc khối ```text```, kèm đường dẫn code để lần theo.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| <…> | <một trong 5 mức dưới> | <…> |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### <DD/MM/YYYY> — <việc>
Tiêu chí ghi trước · cách đo · kết quả (PASS / PARTIAL / FAIL / NOT RUN) · giữ hay bỏ, vì sao · tiền.
Phương án đã thử và bỏ ghi đủ như phương án được chọn.

## 5. Hôm nay còn đúng không

| Kết quả / quyết định | Trạng thái (còn dùng / đã thay bởi … / đã bỏ) | Căn cứ (file:dòng) |
|---|---|---|

## 6. Việc còn lại / cần quyết

## Phụ lục — hồ sơ kỹ thuật

Mã nội bộ (H1, B4, Gate…), spec, report, commit chỉ ở đây.
```
