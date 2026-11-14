# Plan — câu nhiều ý VÒNG 2: hai chốt bằng code (mức nhẹ)

Viết: C, 14/11/2026. A mở vòng 2 sau vòng 1 trượt sàn Golden (`report_agent/2026-11-12_ra_khoang_cach/c_cau_nhieu_y_do.md`).
Nền: nhánh `p9-cau-nhieu-y` `31d38f3` (kết quả âm vòng 1 giữ ở đó). Chờ A duyệt.

**Lời dặn giữ nguyên chữ vòng 1.** Chỉ thêm hai chốt bằng code, tất định, không gọi model thêm. Cờ `cau_nhieu_y` vẫn mặc định tắt.

## Hai chốt

**(a) Câu trả lời chỉ còn dòng ý thiếu ⇒ câu từ chối chuẩn**
- Áp sau khi sinh, trước kiểm trích dẫn và cổng web.
- Điều kiện: mọi dòng có chữ của câu trả lời đều là dòng `CAU_Y_THIEU`.
- Khi đó code thay cả câu bằng `INSUFFICIENT_ANSWER` ⇒ đi đúng đường từ chối cũ (cổng web như cũ).
- Sửa ca Golden 146 vòng 1.

**(b) Luật theo ý chỉ bật khi câu hỏi có ≥ 2 ý**
- Code đếm ý trên **câu người dùng của lượt** (`so_y`):
  - tách vế theo `,` `;` `?`;
  - một vế là một ý hỏi khi có từ hỏi (bao nhiêu · gì · nào · đâu · mấy · bao lâu · bao giờ · khi nào · tại sao · vì sao · thế nào · ra sao) hoặc kết thúc bằng tiểu từ hỏi (không · chưa · nhỉ · vậy · hả).
- `so_y ≥ 2` ⇒ lời dặn theo ý + điều kiện cổng mới. Ngược lại ⇒ lời dặn cũ, giống byte khi cờ tắt.
- Đây là cách tách nhỏ nhất: không đổi lời dặn định tuyến, không thêm lần gọi model.
- Luật ghi trước, chỉ thử trên 10 câu hỏi kèm (10 / 10 ⇒ 2 ý). **Không xem số đếm trên Golden / an toàn trước khi đo.**
- Nhắm ca 160 / 161 vòng 1: câu ngoài kho một ý không còn được nới luật.
- Giới hạn đã biết: câu nhiều ý viết không có dấu phẩy, hoặc nối bằng "và" không dấu, sẽ bị đếm 1 ⇒ về luật cũ. Đây là hướng an toàn: như hôm nay.

**(c) Ghi traceback lỗi trong `data/phase_9/g_cong/tools/do_g.py`** (0 USD, việc X01 `TypeError`). Có traceback thì tìm gốc.
Nếu gốc nằm ở code nhánh thì sửa trong vòng này; nếu ở đường web cũ thì báo A.

## Tiêu chí (như vòng 1, thêm bộ mới) — trượt một sàn ⇒ đóng hồ sơ hẳn

| Bộ | Sàn |
|---|---|
| Hỏi kèm 10 ×1 | phần kho được trả lời ≥ 7 / 10; 0 câu bịa phần thiếu (C đọc tay cả 10) |
| 10 câu ngoài kho mới (E viết, C không xem trước khi đo) | 0 / 10 bị trả lời; 0 lỗi trích dẫn |
| Golden 176 ×1 ↔ mốc E "sau" | ngoài kho 0 / 18; 0 lỗi trích dẫn mới; từ chối ≤ mốc + 1; 0 lỗi kỹ thuật; Đủ / Đúng theo cặp ≥ −0,1 (chấm mù cặp các câu bị cờ chạm: có dòng ý thiếu hoặc đổi từ chối) |
| An toàn 32 ×2 | 0 đổi lớp, 0 câu ngoài kho mới bị trả lời (máy); 4 số S-AT bằng 2 judge + cổng đối chứng (`an_toan_ny.py`) |
| Test | (a), (b) có test; cờ tắt ⇒ chuỗi gửi model giống byte; câu 1 ý khi cờ bật ⇒ cũng giống byte |

**Tiền ≈ 0,2 USD** (vòng 1 tốn 0,16 + 10 câu mới). Chấm bằng agent con (quota Claude). Review: E.

## File chạm
`backend/llm/assistant.py` (`so_y`, chốt (a), điều kiện (b)) · test trong `backend/tests/test_cau_nhieu_y.py` · `data/phase_9/g_cong/tools/do_g.py` (traceback, private).
