# Kiểm tiền của mục web theo giá trị — implementation (B, 16:28 14/11/2026)

- **Plan:** `docs/superpowers/plans/2026-11-14-tien-web-chuan-hoa-plan.md` (A duyệt sha `e34fa9cc0ff0`, không cờ, kèm 4 điều kiện test).
- **Nhánh:** `p9-tien-web` `4656d91` (đã push), từ `main` `07c4537`.
- **Tiền:** 0 USD (đo trên 76 mục web đã lưu từ lượt thử suy luận).

## Đổi gì
- `llm/tra_web.py`:
  - hàm mới `gia_tri_tien(chuoi)`: chuỗi tiền ⇒ số đồng nguyên, đúng tuyệt đối;
  - `_so_tien_chuan` trả khoá `("gia_tri", số)`, hoặc `("chuoi", chuỗi gọn)` khi mơ hồ;
  - luật `tiền mục web ⊂ tiền đoạn trích` **giữ nguyên**, chỉ đổi cách so.
- **Không đoán (điều kiện (b)):**
  - số lẻ với đơn vị đồng ("1,5 đ");
  - số nhóm nghìn kèm hệ số ("1.500 triệu");
  - giá trị không nguyên.
  - Mấy ca này ⇒ so nguyên dạng như trước.
- `tests/test_b6_tra_web.py`: +12 ca.
  - 5 ca khác dạng phải qua: VNĐ ↔ đồng · k ↔ đ · dấu phẩy ↔ chấm · triệu ↔ đồng · nghìn ↔ VND.
  - 6 ca phải chặn: (c) số bịa 220.000; (a) 15.000 ↔ 150.000, 1,5 triệu ↔ 15 triệu, 1.500.001 ↔ 1,5 triệu; (b) "1.500 triệu" mơ hồ; (d) đoạn trích không có tiền.
  - 1 ca khoá hàm đọc giá trị.
- Không đổi lời dặn, model, Serper, `assistant.py`, chuỗi gửi model (code chỉ chạm phép kiểm sau model) ⇒ không cần Q1 (luật §8).

## Đo [Chạy] — tiêu chí ghi trước
| Mã | Kết quả | Sàn | |
|---|---|---|---|
| V | Ra mục web trên 76 mục đã lưu: **43 ⇒ 51** (khong_tin_cay 33 ⇒ 21; 4 sang `chua_xac_minh` vì câu thời gian thực có số — đúng luật) | tăng | ĐẠT |
| L | B đọc tay **8 / 8** mục mới qua: mọi giá trị tiền có trong đoạn trích; lời thận trọng ("chưa xác minh giá một chiều"); không có năm / ngày lệch câu hỏi (ý C) | 0 | ĐẠT |
| C | 6 ca vi phạm vẫn chặn; số bịa 220.000 ở đầu ra thật vẫn chặn 4 / 4 | chặn hết | ĐẠT |
| G | 5 ca khác dạng qua | qua hết | ĐẠT |
| Q1 | không chạm chuỗi gửi model | — | không cần |

**Test:**
- `test_b6_tra_web.py` không khoá: 97 đạt (19 s).
- Có khoá, mọi file chạm tiền / tra web (`test_b5_lich_trinh.py` + `test_b6_tra_web.py`): **582 đạt** (75 s).

## Giới hạn
- **Mẫu hẹp:** 8 mục mới qua đến từ chỉ 2 câu hỏi (giá đồ uống, giá vé tàu). Câu tiền dạng khác (tour, phòng) chưa gặp trong 76 mục.
- **Ca chuỗi bị chặn khác** (`so_ngoai_trich`: giờ, số nhà, năm) không đổi: đếm nhanh trước đó cho thấy phần lớn là số model tự thêm.
- **Năm / ngày lệch** (C: đoạn trích "chương trình Tết" là Tết năm trước) không do phép kiểm tiền bắt. Cần mục việc riêng nếu muốn chặn bằng code.

## Review E — ready (`e_review_tien_web.md`)
- E tính lại khớp: V 43 ⇒ 51; 220.000 vẫn chặn 4 / 4; 8 mục mới qua sạch.
- **3 minor**, đều là lỗ có từ trước của bộ nhận tiền `so_tien.tim_so_tien`; không chặn, không sửa trong việc này:
  - "2 triệu rưỡi" chỉ được đọc là 2 triệu;
  - "150K" (chữ K hoa) không được nhận là tiền;
  - "1,500 đ" được đọc là 1.500 (theo kiểu nhóm nghìn).

## Sửa tiếp m-1 / m-2 của E (A giao) — nhánh `p9-tien-ruoi` `716af4e`, 0 USD
- **m-1 "rưỡi":** bộ nhận tiền bắt cả "triệu / nghìn rưỡi".
  - Đọc chắc khi số là 1–9: "2 triệu rưỡi" = 2.500.000, "1 nghìn rưỡi" = 1.500.
  - Số ≥ 10 thì mơ hồ ("300 nghìn rưỡi" hay nói là 350.000) ⇒ không đoán.
  - Ca cố tình vi phạm có test: đoạn trích ghi 2.000.000, mục web ghi "2 triệu rưỡi" ⇒ chặn. Trước đây đọc thành 2 triệu nên có thể lọt.
- **m-2 "K" hoa:** "150K" được nhận là tiền. "K" hoa chỉ tính khi đứng sau số ≥ 2 chữ số, để "4K" (độ phân giải) không bị coi là tiền.
- **m-3 "1,500 đ" = 1.500:** giữ, đọc theo kiểu nhóm nghìn. **Giới hạn:** người viết theo nghĩa "1,5 đồng" (vô nghĩa với tiền Việt) sẽ bị đọc khác.
- **Tác động phụ:** bộ nhận tiền còn dùng ở kiểm câu tả của lịch (chỉ hỏi "có tiền không"). Nhận thêm "150K" / "rưỡi" thì kiểm đó chỉ chặt hơn.
- **Test:**
  - `test_b6_tra_web.py` không khoá: 99 đạt;
  - có khoá, `test_b5_lich_trinh` + `test_b6_tra_web` + `test_len_ke_hoach_v2`: 433 đạt.
- **76 mục đã lưu:** vẫn 51 ra mục web, 21 bị chặn, 4 chưa xác minh — không lùi.
