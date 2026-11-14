# Review nhánh `p9-lich-mau-an-o` `a609ff3` (E): lịch mẫu "Ví dụ" có nơi ở + quán

- **Người kiểm:** B, 16:53 14/11/2026.
- **Mức:** nhẹ, một review cả nhánh, 0 USD.
- **Kết luận: `ready_for_user_confirmation`.** 0 blocker, 0 major, 2 minor. Một minor là lỗi luật trong khối "nơi ở" của chính B.

## Cổng tối thiểu
- **Diff:** 3 file, +37 / −13.
  - `len_ke_hoach.gan_o_an` là bước gắn `o_dau` + `an` **chép nguyên** từ `chuan_bi` ra một hàm; `chuan_bi` gọi lại đúng hàm đó ⇒ lịch thật không đổi hành vi.
  - `/api/lich_mau` gọi cùng hàm theo cờ.
  - Không gọi model, không đổi tin nhắn gửi model. Không có gì ngoài phạm vi.
- **Cache theo `id(flags)`:** cờ + bảng nạp một lần lúc khởi động và sống cùng app ⇒ đúng. Cách cũ `id(bang)` không đổi khi chỉ đổi cờ, nên đổi khoá là hợp lý.

## Kiểm [Chạy]
- `test_len_ke_hoach_v2.py` + `test_luu_tru_lich.py` không khoá, worktree tách ở `a609ff3`: **96 đạt** (21 s).
- Ảnh của E `data/ui_mau_2026-11-14/anh_chup/lich_mau_an_o_1411/sau_1440.png`: lịch mẫu có 4 dòng ăn (2 quán / dòng) và thẻ "Nơi ở gợi ý" ở cuối, đúng khuôn của lịch thật.

## Finding
- **m-1 (minor, lỗi luật của B, không phải của nhánh này) — luật chọn khu ở bỏ qua điểm buổi tối.**
  - Lịch mẫu: 3 / 5 điểm ban ngày ở phía tây (Thiên Mụ, Tự Đức, Khải Định) ⇒ khu "phía tây yên tĩnh". Nhưng **cả hai buổi tối** ở trung tâm (Chợ Đông Ba, phố đi bộ Nguyễn Đình Chiểu). Hoạt động tối chỉ được xếp ở hai cụm trung tâm (`CUM_TOI` của bộ xếp), nên khách ở phía tây phải đi về mỗi tối.
  - Mô phỏng 3.840 khung và người xem 10 / 10 không bắt được, vì bảng xem không ghi buổi tối.
  - Đề xuất (B làm nếu A giao, 0 USD): tính cả điểm buổi tối khi đếm khu, hoặc chỉ chọn phía tây khi không có buổi tối ở trung tâm; đo lại mô phỏng + người xem 10 lịch.
  - Lịch mẫu là thứ khách thấy đầu tiên ⇒ nên sửa trước khi trình User.
- **m-2 (minor) — lịch mẫu hiện tên quán OSM chưa kiểm, tên mỏng.**
  - Ví dụ ngày 2: "Truong Son", "Phong Nha" — không dấu, và "Phong Nha" dễ nhầm với hang ở Quảng Bình.
  - Đúng luật của nhánh quán (nhãn "chưa kiểm" có hiện), nhưng ở **lịch mẫu** — chỗ khách thấy đầu tiên — tên như vậy làm giảm tin.
  - Đề xuất: lịch mẫu chỉ hiện quán kho (có bài), hoặc chọn tổ hợp mẫu mà các bữa đều có quán kho. Chỗ này để A / User quyết.
