# Bảng quán của thẻ lịch — bản 2: bỏ một quán mà bài kho ghi đã đóng cửa (nhánh `p9-c-bang-quan-v2`)

Phiên C ghi 21:53 21/11/2026 (giờ `date`). Từ main `a4f1aa56`. Phiên điều phối quyết: tạo bản bảng mới, không sửa đè bản cũ. Người đọc: phiên B.

- **Lỗi:** bảng quán (riêng tư, dùng cho mục "Ăn uống gợi ý" của thẻ lịch, đang bật) còn một quán cà phê có bài kho ghi trạng thái đã đóng cửa vĩnh viễn. Quét kho bằng `scripts/grep_kb.sh`: đó là bài quán duy nhất ghi như vậy.
- **Sửa:** bảng bản 2 = bản 1 bỏ đúng dòng đó (468 ⇒ 467 quán: kho 41 · dữ liệu mở 4 · bản đồ mở 422; phần còn lại giống hệt bản 1 — đã so từng dòng); bản 1 giữ nguyên trên máy. `settings.yaml` trỏ sang bản 2 (đường dẫn + con số + mã băm ở chú thích).
- **Test rẻ thêm:** mọi quán nguồn kho trong bảng — bài còn trong kho và dòng "Trạng thái" của bài (nếu có) không nói đóng cửa / ngừng hoạt động. Kho đổi ⇒ test báo để dựng lại bảng.

| Lệnh kiểm (0 đồng, không gọi model) | Đầu ra |
|---|---|
| `pytest tests/test_quan_lich.py -q` | `18 passed`; trỏ tạm cấu hình về bảng bản 1 ⇒ `1 failed, 17 passed` (đúng test mới) |
| `test_len_ke_hoach_v2` · `test_phase6_settings` · `test_settings_env` | 93 · 5 · 6 passed |
| Mô phỏng 3.840 khung lịch, mục ăn uống bản 1 ↔ bản 2 | khung có mục ăn uống đổi: 0; khung bản 1 gợi ý quán đã đóng: 0 (luật hiện tại chỉ gợi ý cà phê khi quanh điểm không có quán ăn nào) |
| Quét tên quán đó trong `data/` (bỏ file câu kín, chỉ in tên file) | 222 file nhắc tên — đều là câu trả lời / bộ câu hỏi đáp về chính bài kho của quán, và hai bản xem tay 10 lịch ngày 14/11 (luật gợi ý cũ). Không bộ nhãn nào của mục ăn uống thẻ lịch chờ quán này ⇒ không nhãn lệch |

- **Người dùng thấy gì khác:** ở thẻ lịch — không (0 / 3.840 khung mô phỏng đổi). Việc này cần cho công cụ "gần một điểm có gì" đang làm: không có nó thì công cụ sẽ nêu quán đã đóng là quán cà phê gần Đại Nội nhất.
- Phép này KHÔNG cho biết các quán nguồn mở (426 dòng, chưa kiểm ngoài đời) còn mở hay không · hướng rộng hơn: không · đếm rẻ nhất: test mới chạy lại mỗi khi kho đổi.
