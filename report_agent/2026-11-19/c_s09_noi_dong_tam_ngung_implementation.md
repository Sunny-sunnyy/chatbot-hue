# Câu thiếu cảnh báo "tạm ngừng mùa lũ": bản lời dặn KHÔNG đạt, bản CODE đã bật — report của C (10:49 19/11/2026, giờ `date`)

Việc A giao sáng 19/11/2026 sau khi User chọn "sửa lỗi an toàn trước khi ghi mốc". Chi tiết có câu của bộ đo nằm ở file riêng tư
`data/phase_9/s09_luu_y/KET_QUA.md` và `data/phase_9/s09_code/PLAN.md`; file này không chép câu hỏi bộ đo hay chữ của kho.

## Cho User — bốn ý
1. **Người dùng thấy gì khác:** hỏi về quy định / cách tham gia một hoạt động mà bài kho có câu "tạm ngừng khi mưa lũ, có lệnh cấm hay thời tiết xấu" ⇒ dưới câu
   trả lời có thêm một dòng in ĐẬM "Lưu ý trong nguồn «tên bài — tên mục»: …" chép nguyên câu đó của bài. Chữ câu trả lời không đổi. [máy kiểm: đo độ đậm trên trình duyệt + ảnh màn hình; chưa có người thứ hai xem ảnh]
2. **Bằng chứng:**
   - Lỗi gốc (lượt đo cuối 18/11): câu thuộc bộ an toàn bỏ ý này 7 / 7 lần dù đoạn đang trích có ghi. [máy kiểm]
   - Bản thứ nhất — thêm MỘT câu vào lời dặn của model (cờ `luu_y_an_toan`, nhánh `p9-c-s09-luu-y-an-toan`, không vào `main`): ở đúng câu đó ý được nêu 8 / 8 lần
     và mọi sàn an toàn đạt, NHƯNG câu dặn đi vào mọi câu hỏi (228 / 228 yêu cầu gửi model đổi) và trên bộ 176 câu mẫu có 7 câu tụt "Đủ ý" — vượt ngưỡng ghi trước
     (số câu tụt của hai lượt không đổi gì + 3 = 5) ⇒ KHÔNG ĐẠT, không bật, không đo lại. Người thứ hai đọc tay: 5 / 6 câu tụt "Trọng tâm" đúng là do lưu ý chen vào
     câu không hỏi tới. Tiền thật 0,212 USD. [máy kiểm + người thứ hai kiểm]
   - Bản thứ hai — CODE (cờ `noi_dong_tam_ngung`, `backend/llm/luu_y_nguon.py`, đang BẬT): không gọi model, yêu cầu gửi model giống từng byte cả khi cờ tắt lẫn bật
     (228 / 228). Chạy lại bước nối trên mọi câu trả lời đã có: câu lỗi được nối đúng 7 / 7 lần; 0 / 8 lần nối trùng khi câu trả lời đã nêu; 0 lần nối cho ba câu có
     cảnh báo của nơi KHÁC trong ngữ cảnh; 0 câu của bốn lượt bộ câu mẫu bị nối. Cả kho chỉ có 10 câu ở 7 bài mà luật có thể chép — người thứ hai đã đọc hết, đều
     đứng một mình được. [máy kiểm + người thứ hai kiểm — phần chạy lại bước nối và danh sách câu của kho]
   - Lượt thật qua server × 3 (0,002 USD): 2 / 3 lần có dòng đậm. [máy kiểm, chưa có người thứ hai]
   - Test: 31 test của file mới, đã thấy đỏ khi phá code; cả bộ test trên nhánh trước lần gộp cuối: 1.429 đạt, 0 hỏng. [máy kiểm]
   - Số dùng lại được: hai lượt bộ câu mẫu KHÔNG đổi gì, cách một ngày, lệch nhau 1 câu "Đúng" · 2 câu "Đủ ý" · 7 câu "Trọng tâm" (129 câu số chính, chấm cùng một
     lô mù) ⇒ ngưỡng "≤ 4 câu tụt" của lượt đo cuối nằm sát mức dao động này. [máy kiểm; một cặp, hai ngày khác nhau]
3. **Giới hạn (User đã nhận 19/11: "bật ngay, ghi giới hạn"):** dòng chỉ hiện khi câu trả lời TRÍCH đúng bài có câu cảnh báo — lần thứ ba của lượt thật model
   trích bài khác nên không có dòng. Xét cả đoạn chưa trích thì gán nhầm cảnh báo của nơi khác (đếm thử: một câu bị nhầm ở cả bốn lượt) ⇒ không làm; User cũng đã
   đóng việc đầu tư thêm cho mảng bão / lũ. Chỉ bắt kiểu "tạm ngừng + điều kiện" nằm trong MỘT câu của bài; câu điều khoản hoàn vé không nối; lượt có lịch không có
   dòng này; tối đa một dòng. Bản code không chữa ba câu an toàn khác mà bản lời dặn từng làm hết thiếu. Người chấm bộ an toàn từ lần đo kế phải đọc cả câu trả lời
   lẫn ghi chú (dòng này nằm ở ghi chú). [chưa kiểm trên câu mới ngoài bộ đã thấy]
4. **Cách thử trong 2 phút:** bật server (runbook mục 2), hỏi trợ lý quy định khi đi thuyền nghe ca Huế trên sông ⇒ dưới dòng Nguồn có một dòng đậm bắt đầu bằng
   "Lưu ý trong nguồn". Không thấy ⇒ xem dòng Nguồn: thiếu bài vé biểu diễn là đúng ca giới hạn ở ý 3.

## Bảng xong / chưa
| Việc | Trạng thái | Lệnh kiểm ⇒ đầu ra |
|---|---|---|
| Hàm thuần + chỗ nối + phần tách cho giao diện vẽ đậm + cờ | xong, trong `main` | `cd backend && uv run pytest tests/test_noi_dong_tam_ngung.py -q` ⇒ `31 passed` |
| Cờ bật | xong (commit riêng) | `grep -c "noi_dong_tam_ngung: true" backend/config/settings.yaml` ⇒ `1` |
| Chạy lại bước nối trên câu trả lời đã có · quét kho | xong (riêng tư) | `data/phase_9/s09_code/ket_qua/lan_3/bang.json`, `cau_trong_kho_lan_2.md` |
| Lượt thật × 3 + ảnh hai khổ màn | xong: 2 / 3 | `data/phase_9/s09_code/ket_qua/luot_that/` |
| Test các file đọc cờ từ settings với cờ BẬT, không `--env-file` | CHƯA chạy riêng | lượt cả bộ test trên `main` sau gộp phủ phần có `--env-file` |
| Harness đo an toàn ghi cả ghi chú cho người chấm | CHƯA làm | làm trước lần đo bộ an toàn kế |
| Bản lời dặn | bỏ, nhánh giữ làm hồ sơ | — |
