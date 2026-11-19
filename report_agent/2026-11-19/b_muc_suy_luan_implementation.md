# Thử mức suy luận của model viết câu trả lời: low · medium (đang chạy) · high — báo cáo của B

Viết 14:29 19/11/2026 (giờ `date`). Việc User giao sáng 19/11 ("thử low, medium, high trên bản đã bỏ trần"). E đặt tiêu chí · B chạy và chấm · C đọc tay · phiên điều phối duyệt plan theo mã băm.
Không có nhánh code: thử bằng tham số có sẵn của bộ sinh, **không sửa code chạy**. Hồ sơ riêng tư (có mã câu của bộ đo): `data/phase_9/muc_suy_luan/` — plan, `bac_1/KET_QUA_BAC_1.md`, `bac_2/KET_QUA_BAC_2.md`, `bac_2/doc_tay_C.md`.

Từ dùng: **mức suy luận** = model được "nghĩ" bao nhiêu trước khi viết (tham số `reasoning effort`); không gửi tham số = `medium` (đã kiểm bằng 10 câu: tiền ×1,00, số token suy luận cùng phân bố) · **bộ câu mẫu** = 176 câu có đáp án · **bộ an toàn** = 32 câu về cảnh báo / điều kiện · **sàn** = mức không được phạm · **mốc** = medium chạy LẠI cùng buổi, xen kẽ từng câu với mức thử (không so với điểm cũ).

## 1. Người dùng thấy gì khác
Không gì khác: **giữ medium** (không gửi tham số). Không cờ, không dòng cấu hình nào đổi.

## 2. Kết quả
**Bậc 1 — mẫu nhỏ 45 câu chọn có chủ đích × 3 mức (để biết GIÁ, không kết luận chất lượng):** ba mức gần bằng nhau về tiền (low ×0,94 · high ×0,97, tính trên 37 câu bộ mẫu của mẫu 45 câu); giây một lời gọi low ×0,80 · high ×1,03 nhưng đo khi máy có tải chung nên không quy cho mức suy luận; `high` hầu như không làm model nghĩ nhiều hơn (token suy luận trung vị 42 so với 21 của medium); 0 lỗi, 0 lượt bị hạn giờ. User xem số rồi chọn bậc 2 chỉ chạy medium + low.

**Bậc 2 — low so với medium, bộ đủ (code `76ef380`):**
| Phần đo | Số | Luật ghi trước | Kết |
|---|---|---|---|
| Bộ câu mẫu, 129 câu số chính — "Đủ ý" (chỉ số quyết) | chênh 0,000; khoảng tin cậy 95 % [−0,101; +0,093]; thắng / hoà / thua 5 / 119 / 5 | tốt hơn khi khoảng nằm trên 0 | **không khác** |
| "Đúng" · "Trọng tâm" | 0,000 · +0,047 | mỗi chỉ số ≥ −0,1 | đạt |
| Câu ngoài kho bị trả lời · lỗi kỹ thuật · lỗi trích dẫn | medium 1, low 0 · 0 · 0 | 0 mới | đạt |
| Câu trong kho bị từ chối | medium 7 · low 5 | ≤ medium + 1 | đạt |
| Bộ an toàn 32 × 2 lượt — nói trái nguồn / sai điều kiện MỚI | lượt 1: 0 · lượt 2: **1** | 0 | **phạm** |
| Bộ an toàn — thiếu cảnh báo MỚI (trước thủ tục sinh lại) | lượt 1: 2 · lượt 2: 2 | 0 sau sinh lại | sinh lại KHÔNG chạy (mục 4) |
| Bộ an toàn — câu ngoài kho bị trả lời | 0 / 3 ở mọi lượt | 0 | đạt |
| Một câu an toàn bắt buộc sinh lại 3 + 3 (dấu hiệu từ bậc 1) | thiếu cảnh báo: low 2 / 3 · medium 3 / 3 | low không nhiều hơn | đạt |
- **Ca phạm sàn:** ở một lượt, low so sánh sai một con số chiều cao với ngưỡng miễn vé trẻ em nên bảo phải mua vé; sáu lần chạy khác của đúng câu đó hôm nay (medium 3, low 2, high 1) đều đúng. Hai người chấm cùng gắn; B đã đọc chữ. Là lỗi "nói chắc mà sai" về tiền vé, không phải cảnh báo tính mạng. Một lần ⇒ dấu hiệu, không phải tỉ lệ.
- **Cặp nhiễu:** hai lượt medium KHÔNG đổi gì chấm cùng lô lệch nhau 1 "sai điều kiện mới" + 2 "thiếu cảnh báo mới" ⇒ sàn "0 mới" trên MỘT lượt không tách được khỏi nhiễu; kết luận về low dựa trên việc đã đọc chữ ca sai, không dựa riêng vào con số đếm.
- **Giá (chỉ đo và báo, không dùng để loại):** tiền / câu low 0,000405 so với medium 0,000424 USD (×0,96); một lời gọi trợ lý trung vị 2,08 so với 2,43 giây (×0,86; máy có tải chung của dự án khác), nhưng low gọi model và tìm thêm nhiều lần hơn một chút nên tổng thời gian model cả câu gần như bằng (5,26 so với 5,31 giây ở giữa); 98 % lời gọi ở low không suy luận (medium 56 %).
- **Kết luận theo luật ghi trước:** low "không khác" về chất lượng VÀ phạm một sàn an toàn ⇒ **không đề nghị low**. `high`: **NOT RUN ở bậc 2 (User chọn)** — thí nghiệm này không kết luận gì về chất lượng của high.

## 3. Bằng chứng và độ tin
- Sinh: bộ câu mẫu 176 + 176 dòng, 0 lỗi, 0 lượt bị hạn giờ 45 giây; an toàn 32 × 4 lượt + 6 lần sinh lại, 0 lỗi. [máy kiểm]
- Chấm: agent con, mù, 0 USD API — bộ câu mẫu 310 phiếu / 13 lô (câu trả lời trùng chữ dùng chung phiếu), 0 phiếu lỗi; bộ an toàn 130 mục × 2 người chấm, cổng đối chứng đạt ở cả hai (bắt 10 / 10 câu chèn sai; báo nhầm 0 / 5 và 1 / 5). [máy kiểm]
- Đọc tay (C, không phải người chạy): 29 cặp lệch của bộ câu mẫu — low thêm ý thật 7, mất ý thật 3, cùng nội dung 18, 1 câu ngoài kho; khớp hướng "không khác"; 0 chỗ nói chắc mà sai ở cả hai mức. [người thứ hai kiểm] Phần an toàn: xem mục 5.
- Công cụ chấm an toàn bốn bên (bản bọc ~50 dòng quanh công cụ của lượt đo cuối) B viết hôm nay; C đọc code, ba điểm đã sửa trước khi chạy; **chưa ai chạy lại độc lập**. [chưa kiểm]
- Chưa chạy bước "kiểm người chấm bằng 4 phiếu biết trước" (cùng thước và cách chấm với lô sáng 19/11).

## 4. Chưa làm / tự hoãn / phép thêm
- Sinh lại 3 + 3 cho ba câu an toàn "thiếu mới" ở low: **tự hoãn — không cần** (phiên điều phối chốt: kết quả không đổi được kết luận; ≈ 0,012 USD).
- Bậc 3 (chữ đầu qua server): không chạy — chỉ dành cho mức được đề nghị.
- Lượt biểu mẫu / hiểu ý sửa lịch (đang chạy low): là thí nghiệm riêng trong plan, CHƯA làm.
- **Phép thêm sau khi thấy số (phiên điều phối cho; không dùng để đổi dòng quyết):** ở lượt low có một câu trong kho bị bước định tuyến đẩy ra "ngoài phạm vi". Bước định tuyến KHÔNG nhận tham số mức suy luận (`backend/llm/generator_openai_full_corpus.py:298` chỉ đặt cho agent trả lời; bản chụp yêu cầu ở bậc 1 giống byte giữa các mức) nên không thể do low; sinh lại riêng bước đó 5 + 5 lần: **10 / 10 đúng tuyến** ⇒ nhiễu một lần của bước định tuyến (1 / 12 lần hôm nay trên câu đó: hai lượt bậc 2 + 10 lần chạy lại). Chưa ai nhận việc xem tần suất này trên cả bộ.

## 5. Đọc tay phần an toàn (C)
C đọc đủ 32 câu × 2 lượt của low, đặt cạnh hai lượt medium cùng buổi, và 3 + 3 lần sinh lại của câu an toàn bắt buộc; chỗ nghi thì mở đúng đoạn ngữ cảnh model đã nhận; mở số máy SAU khi xếp xong. Không mù (biết bên nào là low), một người đọc. [người thứ hai kiểm]
- **Xác nhận ca phạm sàn là sai thật:** ngưỡng miễn vé và các mức giá nằm trong ngữ cảnh của mọi lượt (phần chung của hai bên); câu trả lời của low ở lượt 2 tự mâu thuẫn rồi kết luận sai. Low lượt 1 và hai lượt medium đúng.
- **Ba mã máy gắn "thiếu cảnh báo mới" ở low: người đọc xét KHÔNG phạm** — hai câu về vé (điều kiện vẫn có mặt, không có ý an toàn nào bị bỏ), một câu cùng nội dung với medium. Mức lệch này nằm trong cỡ lệch giữa hai lượt medium.
- Câu an toàn sinh lại 3 + 3: người đọc thấy 6 / 6 lần đều có các ý cảnh báo chính; riêng ý mà low bỏ ở bậc 1, máy gắn thiếu ở low 2 / 3 và medium 3 / 3 (người đọc ghi low 0 / 3 — lệch với máy) ⇒ low không thiếu nhiều hơn medium; dấu hiệu "low bỏ ý riêng" của bậc 1 không lặp lại.
- Người đọc đề nghị sinh lại chính câu phạm sàn 3 + 3 trước khi coi là "mới thật"; phiên điều phối gác vì low đã "không khác" nên kết luận "không đề nghị low" không đổi dù kết quả sinh lại ra sao.
- Ghi nhận thêm (không phải lỗi): low từ chối nhầm một câu kho có ở một lượt (medium 0 / 2); low ngắn hơn ở ba câu (bớt chi tiết phụ).
Theo plan, phần đọc tay báo CẠNH số máy, không lật kết luận máy.

## 6. Tiền thật
Bậc 1: 0,085 USD. Bậc 2: 0,238 USD (sinh 0,146 · an toàn 0,087 · sinh lại 0,0035 · định tuyến lại 0,0014; trần bậc 2: 0,35). **Cả việc: 0,323 USD** (ước sau khi bỏ high ≈ 0,36–0,40; ước ban đầu cho ba mức 0,6–1,0; trần cứng 1,2).

## 7. Giới hạn
Bộ câu mẫu đã dùng hơn mười lượt có chấm, không có bộ kín cho việc này ⇒ kết luận là "trên bộ đã thấy". Mỗi mức một lượt bộ câu mẫu. Giây đo khi máy có tải chung. Lần thử cũ (25–27/10, bản một lần gọi, kho cũ) cũng giữ mặc định: khi đó low / none "kém hơn" vì lỗi trích dẫn (đếm bằng bộ kiểm cũ), high không khác; lần này low "không khác" về chất lượng, 0 lỗi trích dẫn, chỉ phạm một sàn an toàn — cùng quyết định, không cùng kết quả.

| Đã làm | Chưa làm | Tự hoãn + lý do | Lệnh kiểm ⇒ đầu ra |
|---|---|---|---|
| Bậc 1 ba mức · bậc 2 medium + low (sinh, chấm, bảng giá) · câu an toàn sinh lại bắt buộc · phép thêm định tuyến | bậc 2 cho high (User chọn) · thí nghiệm lượt biểu mẫu / sửa lịch · kiểm người chấm 4 phiếu | sinh lại ba câu "thiếu mới" + bậc 3: không đổi kết luận | `cat data/phase_9/muc_suy_luan/bac_2/golden/ba_muc_in.txt` ⇒ dòng `low \| xếp loại: không khác` · `python3 data/phase_9/muc_suy_luan/tools/in_gia.py data/phase_9/muc_suy_luan/bac_2/sinh/medium.jsonl data/phase_9/muc_suy_luan/bac_2/sinh/low.jsonl` ⇒ `tien_x: 0.96` |
