# Implementation Report: C210 — "tin số ngày code dò khi rõ ràng" (B5, lỗi hỏi lại thừa)

Người làm: C (Claude Code, Opus 5.5)
Date: 22:27 06/11/2026 (`date`)
Canonical guide: mục việc C210 trong `session_prompt/CURRENT_HANDOFF.md` + tin A (sau khi giao C210, 06/11): làm theo `systematic-debugging` — tái tạo trước; không tái tạo được trong ≤ 0,005 USD ⇒ dừng, không sửa phòng xa.

## 1. Kết luận

**CHƯA TÁI TẠO ĐƯỢC** lỗi "hỏi lại số ngày thừa" trên `main` `3ec526d` ⇒ **không sửa code** (theo dặn của A). Nhánh `p9-so-ngay` đã xoá (rỗng, chưa push).
Tiền: **0,003855 USD**.

## 2. Đã làm

1. **Thứ tự sai đã sửa lại:** C viết sửa trước khi tái tạo (đổi `chot_so_ngay` "lệch ⇒ hỏi" thành "code dò thắng" + thêm dạng "3N2D" / "N hôm" vào bộ dò + test). A nhắc ⇒ C **cất phần sửa** (chưa commit), tái tạo trên code `main`. Phần sửa giữ ở `data/phase_9/c210/sua_khong_ap_dung.patch` (hồ sơ phương án không áp dụng).
2. **Tái tạo mức code [Chạy, 0 USD]** — `data/phase_9/c210/tools/do_dang_viet.py`, 20 cách viết số ngày do C tự viết. Đường dẫn tới hỏi lại (`lich_trinh.chot_so_ngay` trả None) có 2 nhánh:
   - **(A)** model gửi số ngày khác số code dò;
   - **(B)** code không dò ra **và** model không gửi.

   Code `main` **không dò được**: "3N2D" (D không gạch), "4n3d", "3d2n", "2 hôm", "đi trong ngày", "nửa ngày", "1 tuần", "cuối tuần" ⇒ khi gặp các dạng này, hỏi hay không tuỳ model có gửi số không (nhánh B).
   Câu khoảng ("2-3 ngày", "tầm 2, 3 ngày") ⇒ code dò ra **3** (chỉ số đứng ngay trước "ngày") ⇒ nếu model gửi "2" thì rơi vào nhánh A, hỏi lại.
3. **Tái tạo có phí [Chạy, 0,003855 USD]** — `data/phase_9/c210/tools/tai_tao.py`. Cách chạy:
   - app thật trong tiến trình, `lich_trinh` bật trên bản sao settings, `/api/chat/stream`;
   - bọc `chot_so_ngay` (hàm thật vẫn chạy) để ghi **tham số `so_ngay` model gửi + số code dò + kết quả**;
   - 5 câu C tự viết, không lấy từ bộ kín. Kết quả: `data/phase_9/c210/tai_tao_main.jsonl`.

| Câu (dạng) | Model gửi | Code dò | Kết quả chốt | Hỏi lại? |
|---|---|---|---|---|
| "3N2D" | 3 | không ra | 3 | không |
| "4n3d" (+ sở thích) | 4+ | không ra | 4+ | không |
| "2 hôm" | 2 | không ra | 2 | không |
| "đi trong ngày" | 1 | không ra | 1 | không |
| "tầm 2, 3 ngày" + hỏi kèm khách sạn | không gửi | 3 | 3 | không |

5 / 5 ra lịch (`outcome success`, tuyến `tro_ly_hue`, `lich_trinh_kiem` rỗng). Khớp E20: số model gửi trùng số code dò ở 10 / 10 câu.

## 3. Giả thuyết còn lại (chưa chứng minh — cần dữ liệu của lượt kín mới)

1. **Harness kín cũ không lưu tham số** ⇒ không biết "hỏi lại" ở kín v2 là thẻ hỏi số ngày (D12 (b)) hay model tự viết câu hỏi trong lời. **Đề xuất đo (0 USD, không sửa chatbot):** harness kín lần sau ghi `tham số so_ngay model gửi · số code dò · có thẻ clarify không` (bọc `chot_so_ngay` như `tai_tao.py`). Lỗi thật lộ ⇒ sửa đúng nhánh.
2. **Câu khoảng / lẻ** ("2-3 ngày", "1 ngày rưỡi") + model gửi số khác số code dò ⇒ nhánh A hỏi lại. Lượt này model không gửi số nên không hỏi; có thể xảy ra ngẫu nhiên.
3. **Câu không có số rõ** ("cuối tuần", "1 tuần") + model không gửi ⇒ hỏi **đúng luật D12 (b)**, nhưng người đọc có thể thấy là thừa. Đây là câu hỏi luật cho A / User, không phải lỗi code.
4. **Nhiều lượt:** câu sau nói số tương đối ("thêm 1 ngày nữa") ⇒ code dò "1" lệch số model gửi ⇒ nhánh A hỏi. Bộ kín v2 không có câu hai lượt (A chốt) ⇒ không giải thích được kết quả kín v2. Đáng nhớ khi bật sửa lịch.

## 4. Không làm / giới hạn

- Không đọc `data/phase_9/b5_v2/`, `data/phase_9/b5/kin/`.
- Không chạy lượt có phí nhiều lượt: phần còn lại dưới trần 0,005 (~0,0011) không đủ một chuỗi có ích.
- Q1 / test: không chạy (không có code đổi trên nhánh).
- 5 câu là mẫu nhỏ; model chạy ngẫu nhiên ⇒ "0 / 5 hỏi lại" không chứng minh tỉ lệ 0.
