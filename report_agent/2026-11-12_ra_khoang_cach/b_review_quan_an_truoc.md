# Review nhánh `p9-quan-an-truoc` `bfe4957` (C): bữa chính chỉ gợi ý quán ăn

- **Người kiểm:** B, 17:22 14/11/2026.
- **Mức:** nhẹ, 0 USD.
- **Kết luận: `ready_for_user_confirmation`.** 0 finding chặn, kèm đề xuất cho câu A hỏi.

## Cổng tối thiểu
- **Diff:** `quan_lich._chon` + test mô phỏng. Không có gì ngoài phạm vi.
- **Luật mới:**
  - xếp theo (loại: quán ăn trước, rồi nguồn: kho trước, rồi khoảng cách);
  - có quán ăn ⇒ chỉ lấy quán ăn (1–2);
  - không có quán ăn nào trong 2 km ⇒ mới lấy cà phê.
- Đúng lỗi A thấy: bản cũ xếp nguồn trước loại, nên một quán cà phê có bài kho đứng trước quán ăn chỉ có trên bản đồ mở ở bữa tối.
- Không vào chuỗi gửi model, trần 2 km giữ nguyên.

## Kiểm [Chạy] (0 USD, worktree tách ở `bfe4957`)
- `test_quan_lich.py` không khoá: **14 đạt** (11 s).
- **Đếm trên 3.840 khung** (18.306 bữa có dòng):
  - 2 quán: 14.594;
  - **1 quán: 3.712 (20 %)**;
  - bữa có ít nhất 1 quán kho: 8.675 (47 %);
  - **bữa chỉ có quán bản đồ mở chưa kiểm: 9.631 (53 %)**.
- Số bữa có dòng **không đổi** so với bản cũ: cà phê vẫn được dùng khi không có quán ăn. Chỉ ô thứ hai bị bỏ trống.

## Câu A hỏi: đổi chác "ít lựa chọn hơn" có chấp nhận được không?
**B đề xuất: giữ đúng luật của C (bữa chính chỉ quán ăn), không cho cà phê làm lựa chọn thứ hai.**
- Dòng ghi "Ăn trưa / Ăn tối gần X". Một quán cà phê trong dòng đó là gợi ý sai mục đích, dù có nhãn "cà phê". Lỗi A thấy chính là kiểu này, chỉ khác vị trí.
- Một lựa chọn đúng mục đích tốt hơn hai lựa chọn mà một cái không ăn được bữa chính. Khách vẫn có link bản đồ để tự tìm thêm quanh đó.
- 20 % bữa chỉ 1 quán là số thật, nhưng không phải lỗi. Gốc của nó là thiếu dữ liệu quán ăn trong 2 km, không phải do luật.

**Cái đáng làm hơn nếu muốn bữa ăn tốt lên** (việc riêng, chưa làm): 53 % bữa chỉ có quán bản đồ mở chưa kiểm, tên thường mỏng. Bổ sung quán có bài kho cho các cụm thiếu (Thủy Xuân, Kim Long) sẽ có lợi hơn là nới loại quán.

**Nếu A / User vẫn muốn 2 lựa chọn:** cho cà phê làm ô thứ hai **chỉ khi** cà phê đó có bài kho, kèm nhãn "cà phê (ăn nhẹ)". Cách này đổi `_chon` thêm 2 dòng và cần đo lại.
