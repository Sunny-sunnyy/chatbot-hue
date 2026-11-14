# Plan (mức nhẹ) — Chuẩn hoá cách viết tiền trước khi so ở kiểm cuối mục web · B · 16:23 14/11/2026

## Lỗi (đọc tay, 0 USD, trên `data/web_suy_luan_2026-11-14/buoc2.jsonl`)
- `tra_web.kiem_muc_web` so tiền bằng **nguyên chuỗi** (chỉ bỏ khoảng trắng + chữ hoa): `_so_tien_chuan`.
- Vì vậy "100.000 đồng" ≠ "100.000 VNĐ", "65.000 đồng" ≠ "65.000đ" / "65k", "594.000 đồng" ≠ "594,000 đồng" ⇒ mục web đúng nguồn bị thay bằng câu cố định "chưa tra được tin đáng tin".
- 6 ca đọc tay: 5 ca chỉ khác cách viết.
- Có một ca bịa thật ("220.000 đồng" không có trong đoạn trích) ⇒ ca này **phải tiếp tục bị chặn**.

## Đổi một thứ
`_so_tien_chuan` trả **giá trị số nguyên (đồng)** thay vì chuỗi:
- bỏ đơn vị (đ / đồng / VND / VNĐ);
- bỏ dấu ngăn nghìn (. , khoảng trắng);
- "k / nghìn / ngàn" ×1.000, "triệu / tr" ×1.000.000 (nhận phần lẻ "1,5 triệu").
- Luật **không nới**: tiền trong mục web phải ⊂ tiền trong đoạn trích, chỉ là so theo giá trị.
- Không đổi lời dặn, model, Serper, các phép kiểm khác.
- Có dùng cờ hay không: phép so là code tất định, đo được trên đầu ra đã lưu ⇒ B đề xuất **không cờ**. A chọn khác thì thêm.

## Tiêu chí ghi trước
| Mã | Tiêu chí | Đo | Sàn |
|---|---|---|---|
| V | Tỉ lệ ra mục web trên 76 đầu ra đã lưu (`buoc2.jsonl`, chạy lại kiểm cuối, 0 USD) | trước 43 / 76 | tăng |
| L | Tiền lạ lọt qua: mọi mục mới qua đều có mọi giá trị tiền ∈ đoạn trích (B đọc tay mọi mục mới qua) | — | 0 |
| C | Ca cố tình vi phạm vẫn bị chặn (test): tiền không có trong trích; khác 10 lần ("15.000" ↔ "150.000"); "1,5 triệu" ↔ "15 triệu" | test | chặn hết |
| G | Ca khác dạng qua (test): đồng ↔ VND ↔ đ ↔ k ↔ dấu phẩy / chấm ↔ "triệu" | test | qua hết |
| Q1 | Chuỗi gửi model không đổi (code chỉ chạm phép kiểm sau model) | test hiện có | giống byte |

- **Thử nhanh bản nháp** (không phải số nghiệm thu): 43 ⇒ 51 / 76 ra mục web; "220.000" vẫn chặn 4 / 4; 4 ca chuyển sang "chưa xác minh" vì câu hỏi thời gian thực (đúng luật).
- **Tiền:** 0 USD (đo trên đầu ra đã lưu). Không lượt có phí.
- **Chạm cùng cổng web với việc của C** (C đang đếm có nên bỏ tra web cho dòng ý thiếu không) ⇒ B báo C, không sửa `assistant.py`; chỉ sửa `llm/tra_web.py` + test.

## Bảng AI FDE
| Mục | Thiết kế | Khớp / lệch |
|---|---|---|
| Luật tiền ⇒ code | Vẫn code, chỉ đổi cách so | khớp |
| Nói chắc sai | Luật ⊂ đoạn trích giữ nguyên; test ca vi phạm | khớp |
| Đổi một thứ | Một hàm `_so_tien_chuan` | khớp |
