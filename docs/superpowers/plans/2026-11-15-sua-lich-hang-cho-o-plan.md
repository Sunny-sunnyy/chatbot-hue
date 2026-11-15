# Plan (mức nhẹ) — Sửa lịch bằng lời: đổi hạng chỗ ở (bậc 1) · C · 15:18 15/11/2026

User chọn 15:14 15/11/2026 "làm cả hai, từng bậc": bậc 1 hạng chỗ ở (plan này); đạt rồi mới bậc 2 ngày đi (plan riêng). Nền: `main` `e54c19d`, cờ `sua_lich_v2` + `luu_tru_lich` đang bật.

**Căn cứ để review:** `report_agent/2026-11-12_ra_khoang_cach/c_dem_sua_lich_truong.md` (số đếm) · `backend/llm/sua_lich_v2.py` (`HanhDong`, `ap`, `thay_doi`) · `backend/llm/full_corpus_prompt.py` (`SUA_LICH_LOI_DAN`) · `backend/llm/luu_tru_lich.py` (`chon_co_so`, `o_dau`).

## Lỗi đã đếm (trước khi xây)
- Câu xin đổi hạng chỗ ở sau khi có lịch: lần hiểu ý trả rỗng **5 / 5** ⇒ hệ thống trả lời như một câu hỏi thường, lịch không đổi, **không có dòng "Chưa làm"** (câu tự đặt; log không lưu chữ nên không có số nhu cầu thật).
- Biểu mẫu đã có nút hạng (bình dân = 1 sao / đạt chuẩn · vừa = 2–3 sao · cao = 4–5 sao) và code giữ mức qua các lượt sửa ⇒ thiếu đúng một đường: nói bằng lời.
- Mức trống có thật (đếm bảng v5, 136 cơ sở): ven biển phía nam không có cơ sở 2–3 sao ⇒ hôm nay code lặng lẽ hiện mọi hạng.

## Thiết kế (model chỉ hiểu ý, code quyết)
1. **Hành động mới `doi_hang_o`** trong `HanhDong`, trường `ngan_sach` ∈ {`binh_dan`, `vua`, `cao`} hoặc trống. Lời dặn thêm 1 gạch đầu dòng + 1 dòng cách nói ("1 sao / đạt chuẩn / bình dân ⇒ binh_dan; 2–3 sao / tầm trung ⇒ vua; 4–5 sao / cao cấp ⇒ cao; chỉ nói rẻ hơn / sang hơn / đổi khách sạn khác mà không nêu hạng ⇒ để trống").
2. **Code áp** (không gọi bộ xếp — hạng không ảnh hưởng điểm tham quan):
   - `ngan_sach` trống ⇒ dòng "Chưa làm: đổi hạng chỗ ở — bạn nói rõ 1 sao, 2–3 sao hay 4–5 sao nhé."
   - trùng mức đang dùng ⇒ "Lịch đang gợi ý chỗ ở hạng đó rồi."
   - khu của lịch không có cơ sở mức đó (code đếm bằng `chon_co_so`) ⇒ "Khu … chưa có cơ sở hạng … trong danh mục nên mình giữ nguyên."
   - lịch 1 ngày / không có ô Nơi ở ⇒ "Lịch 1 ngày không có gợi ý chỗ ở."
   - còn lại ⇒ ghi `tham_so.ngan_sach`, khung ngày / buổi giữ nguyên, ô Nơi ở dựng lại bằng đúng hàm của biểu mẫu; dòng "Đã đổi hạng chỗ ở: 2–3 sao → 4–5 sao."; câu của mọi mục giữ nguyên ⇒ **0 lần gọi model viết lại**.
3. Không cờ mới (nằm trong `sua_lich_v2`); không đổi `tin_nhan_hieu`; nút hạng trên biểu mẫu đồng bộ với mức mới nếu giao diện đang giữ giá trị riêng (kiểm lúc code).
4. **Không làm ở bậc này:** "rẻ hơn / sang hơn" tự suy mức; bỏ chọn hạng ("hạng nào cũng được"); gọi tên một khách sạn cụ thể; giá phòng.

## Tiêu chí ghi trước (mỗi lượt gửi qua `/api/chat/stream` trên server thật, cuộc đã có lịch)
| Mã | Bộ (cỡ) | Tiêu chí | Ngưỡng | Tiền |
|---|---|---|---|---|
| Luôn | test 0 USD: 3.840 khung × 3 mức | khung ngày / buổi giống hệt trước sửa; ô Nơi ở sau sửa = ô Nơi ở khi điền biểu mẫu cùng mức; 4 dòng "không đổi" đúng điều kiện | 0 lệch | 0 |
| Q1 | chuỗi gửi model các đường khác | giống byte (chỉ lời dặn hiểu ý đổi) | 228 / 228 | 0 |
| **H1 (quyết)** | 12 câu nêu rõ hạng, C viết trước (4 câu / mức, mức hiện tại khác mức xin), chạy 2 lượt | code áp đúng mức ở cả 2 lượt | ≥ 10 / 12 | ≈ 0,03 (H1–H3) |
| **H1-sai (sàn)** | cùng 12 câu | áp **khác** mức nhãn (làm sai mà báo "Đã đổi") | 0 / 24 | |
| **H2 (quyết)** | 6 câu không nêu hạng (rẻ hơn, sang hơn, đổi khách sạn khác…) × 2 | không đổi mức | 0 / 12 đổi | |
| H2-nói | cùng 6 câu | có dòng "Chưa làm … nói rõ hạng" (không im lặng) | ≥ 4 / 6 ở cả 2 lượt | |
| **H3 (sàn)** | 6 câu hỏi thông tin có chữ "sao / khách sạn" nhưng không xin sửa × 2 | thành lượt sửa | 0 / 12 | |
| H4 | 8 câu diễn đạt lạ do E viết **sau khi** lời dặn đã chốt, chạy 1 lượt | đúng mức · sai mức | ≥ 6 / 8 · 0 | ≈ 0,005 |
| **Q3 (hồi quy)** | bộ chuỗi đã thấy 10, pass^2 (mốc 9 / 10) | hành động đúng nhãn | ≥ 8 / 10 | ≈ 0,10 |
| **Q5 (sàn)** | an toàn 32 × 2 trong cuộc có lịch | thành lượt sửa / ra hành động | 0 / 64 | ≈ 0,03 |
| **Q5b (sàn)** | 8 câu trộn sửa + khẩn cấp × 2 | thành lượt sửa | 0 / 16 | ≈ 0,02 |

- **Đếm câu chạm:** lời dặn hiểu ý đổi ⇒ mọi lượt trong cuộc có lịch đều chạm ⇒ Q3, Q5, Q5b chạy đủ; Golden 176 và an toàn 32 ngoài cuộc có lịch **không chạm** (lần hiểu ý không được gọi) ⇒ không chạy. Trước lượt có phí: một test xác nhận điều này bằng băm chuỗi gửi model.
- **Thứ tự:** test 0 USD ⇒ H1–H3 ⇒ (trượt thì **một** vòng chỉnh lời dặn, chạy lại H1–H3) ⇒ chốt lời dặn ⇒ H4, Q3, Q5, Q5b **một lần** trên bản chốt. Không đo thêm sau khi thấy số.
- **Bộ kín: không.** Lý do: một trường enum 3 giá trị, tối đa một vòng chỉnh; H4 (người khác viết, sau khi chốt) giữ vai kiểm quá khớp với giá ≈ 0,005. Cần vòng chỉnh thứ hai ⇒ dừng, báo A.
- **Tốc độ:** không thêm lần gọi model, lời dặn dài thêm ~70 token ⇒ không đo độ trễ riêng; lượt đổi hạng không viết lại câu nên nhanh hơn lượt sửa thường (ghi số từ log H1 để theo dõi).
- **Giao diện:** dùng khối "Đã đổi / Chưa làm" sẵn có ⇒ không Playwright; nếu phải sửa nút hạng trên biểu mẫu ⇒ 1 ca Playwright một khổ màn.
- **Tiền:** ≈ 0,19 USD, **trần 0,25**. **Dừng:** phạm sàn H1-sai / H3 / Q5 / Q5b sau vòng chỉnh, hoặc Q3 < 8 / 10 ⇒ không merge, báo A (không hạ ngưỡng).
- **Review:** một review cả nhánh (đổi lời dặn + xử lý chữ người dùng). Tài liệu: `bai_hoc/25` + sổ 07 cùng đợt khi đạt.

## Bảng rà AI FDE
| Mục | Thiết kế | Khớp / lệch |
|---|---|---|
| Có cần model? | Hiểu câu tự do ⇒ mức hạng: model. Mức hợp lệ (enum), có cơ sở ở mức đó không, chọn khách sạn, câu báo: code | khớp |
| Tham số | 1 enum 3 giá trị, `extra="forbid"`; không nhận tên khách sạn, giá, link từ model | khớp |
| Từ chối thành kết quả | 4 trường hợp không đổi đều có dòng lý do do code viết, lượt không sập | khớp |
| Làm sai mà báo đã làm | Sàn H1-sai 0 / 24; nếu thấy ≥ 1 ⇒ thêm rào "mức phải có căn cứ trong chữ người dùng" như rào số ngày (chỉ xây khi đã thấy lỗi) | khớp |
| Trí nhớ | Chỉ `tham_so.ngan_sach` trong khung đã lưu của cuộc (đường có sẵn) | khớp |
| Chữ người dùng là dữ liệu | Câu ⇒ enum; Q5 / Q5b giữ 0 câu an toàn / khẩn cấp lạc sang sửa | khớp |
| Đường ra mới · dữ liệu mới | Không (bảng lưu trú v5 đã dùng; link tìm phòng do code dựng như cũ) | khớp |
