# Bậc 3 và 4 của đợt cải thiện trợ lý — mô tả công cụ và trạng thái kết quả công cụ (plan một trang)

Viết: 12:08 21/11/2026 (giờ `date`), phiên B. Người duyệt: phiên điều phối. Chưa code gì.
Từ dùng: *công cụ* = hàm trợ lý được gọi trong lúc trả lời (tìm kho, thời tiết, ngày lịch, khoảng cách, lịch trình) · *mô tả công cụ* = đoạn chữ model đọc để quyết có gọi không và gọi thế nào ·
*kết quả công cụ* = chữ code trả lại cho model · *thước* = bộ đo agent của phiên đo, chạy trên cả gpt-6-luna lẫn Claude Sonnet 5.5 mức high · *bản 0* = bản chính sau các bản sửa sáng 21/11.

## 1. Lỗi đã thấy thật (chỉ làm cho những thứ này)

| # | Thấy gì | Số | Ở model nào |
|---|---|---|---|
| a | Hỏi mưa nắng thường ("ngày mai nắng hay mưa, có nên ra biển") ⇒ model chọn loại `bao_lu` của công cụ thời tiết ⇒ theo thiết kế câu bão / lũ, câu trả lời KHÔNG có số, chỉ trỏ xuống khối dự báo | 3 / 3 lượt | Sonnet high (người viết đo) |
| b | Model CHÉP số dự báo vào câu trả lời dù mô tả công cụ dặn "không chép lại số"; khối số do code nối vẫn hiện bên dưới ⇒ người dùng thấy số hai lần (số chép đúng) | 16 / 16 lượt thời tiết | Sonnet high (phiên review đo); luna: CHƯA đếm |
| c | Câu hai ý, một ý không có dữ liệu (nơi không có trong bảng khoảng cách + giá vé) ⇒ từ chối CẢ câu thay vì trả lời ý có | câu ghép của thước: cả hai model còn trượt | luna + Sonnet (phiên đo đang đếm vì sao cơ chế "câu nhiều ý" sẵn có không kích hoạt) |
| d | Kết quả "không có dữ liệu / đã hết lượt" mỗi công cụ một kiểu chữ (5 câu khác nhau, có câu là mệnh lệnh "hãy viết câu trả lời", có câu chỉ báo) | đọc code | cả hai |

Chưa thấy lần nào (KHÔNG làm, chỉ thêm phép đếm vào thước): lỗi 429 / 5xx / rớt mạng của Bedrock (0 lần trong khoảng 700 lời gọi hôm nay) ⇒ chưa thêm "thử lại có lùi";
model nộp sai khuôn qua công cụ nội bộ (khuôn strict nên không thể) ⇒ không cần đường "trả lỗi cho model nộp lại".

## 2. Đổi gì

**Bậc 3 — mô tả công cụ (chữ, không đổi code công cụ).** Viết lại năm mô tả theo một khuôn bốn ý, mỗi ý một câu: *làm gì · gọi khi nào · KHÔNG gọi khi nào · trả về gì và không trả về gì*. Hai chỗ đổi nghĩa:
1. `loai` của công cụ thời tiết: `bao_lu` CHỈ khi tin nhắn của người dùng có từ chỉ nguy hiểm thời tiết (bão, áp thấp, lũ, lụt, ngập, giông lốc, sạt lở, triều cường, nước sông lên) hoặc hỏi thẳng "có an toàn / nguy hiểm không" vì thời tiết;
   hỏi mưa, nắng, nóng, lạnh, nên mang gì, nên đi đâu ⇒ `du_bao`. (Lưới bằng code cho từ nguy hiểm đã có sẵn và không đổi: câu có từ đó vẫn thành lượt bão dù model chọn gì.)
2. Số dự báo: đo trước rồi mới chọn luật — xem mục 3 bước 0.

**Bậc 4 — trạng thái kết quả công cụ (code nhỏ ở `backend/llm/assistant.py`).** Mọi kết quả công cụ mở đầu bằng MỘT dòng trạng thái cùng khuôn, đứng NGOÀI khối nguồn [n] (không vào sổ nguồn, không trích được):
`Trạng thái: có dữ liệu` · `Trạng thái: không có dữ liệu cho yêu cầu này — <vì sao, một vế>; ý này của câu hỏi coi như kho không có, các ý khác vẫn trả lời` ·
`Trạng thái: đã dùng hết lượt của công cụ này trong câu — viết câu trả lời từ Bằng chứng đã có`. Thay cho năm câu rời hiện nay. Dòng "không có dữ liệu… các ý khác vẫn trả lời" nhắm thẳng lỗi (c).

**Cách bật để đo:** một khoá cấu hình `assistant.cong_cu_ban: 1 | 2` (1 = chữ hiện nay, giống từng byte; 2 = mô tả mới + dòng trạng thái) đọc từ dict settings ⇒ phiên đo chạy 2 × 2 (bản × model) cùng buổi.
Khi chốt: bên nào tốt hơn thì đặt bản đó theo provider; nếu chỉ một bên dùng bản 2 thì khoá thành theo provider.

## 3. Thứ tự và tiêu chí ghi TRƯỚC

0. **Đếm trước, 0 đồng (người viết):** trong các lượt thời tiết đã có của hôm nay — luna chép số bao nhiêu lượt; câu trả lời có số khi KHÔNG có khối nối không. Chọn luật cho số dự báo theo kết quả:
   cả hai model đều chép ⇒ luật mới "được nêu số của nguồn dự báo, phải ghi [n]; code thôi nối khối trùng khi câu trả lời đã có đủ số của các ngày được hỏi" (cần bước kiểm số bằng code — có sẵn cho khoảng cách, viết thêm cho dự báo);
   chỉ Sonnet chép ⇒ giữ luật cũ, sửa mô tả cho Sonnet nghe, đo lại; vẫn chép ≥ một nửa số lượt ⇒ chuyển sang luật mới cho riêng Sonnet.
1. Viết bản 2, test: bản 1 ⇒ danh sách công cụ + kết quả gửi model giống byte; bản 2 ⇒ mỗi công cụ một ca cho ba trạng thái.
2. Phiên đo chạy thước 2 × 2. Tiêu chí:
   - **Phải được:** câu mưa nắng thường chọn `du_bao` ≥ 5 / 6 lượt (hôm nay 0 / 3 ở Sonnet) · "đạt máy — câu ghép" tăng quá nhiễu ở ít nhất một model · lượt thời tiết không còn số lặp hai lần (theo luật đã chọn ở bước 0).
   - **Sàn không được xấu đi:** bộ bão / an toàn — câu có từ nguy hiểm vẫn ra lượt bão đủ số lượt như bản 1, 0 câu trấn an · "an toàn 10 — ngoài kho bị trả lời" rỗng · "ngoài phạm vi 10" không đổi · "gọi thừa công cụ cấm" rỗng · chạm trần vòng vẫn 0 · lỗi kỹ thuật rỗng.
   - **Không tụt quá nhiễu:** "đạt máy — công cụ", "đạt máy — rìa Huế", chuỗi "phải trả lời mà bị từ chối".
3. Một dòng sàn xấu đi ⇒ gỡ đúng phần gây ra (mô tả của công cụ đó hoặc dòng trạng thái đó), không vòng hai.

## 4. Rủi ro

- Sàn "không trấn an khi có bão": thu hẹp `bao_lu` có thể làm một câu bão nói vòng không được nhận. Giữ được nhờ lưới từ khoá bằng code (không đổi); đo riêng bộ bão.
- Dòng "các ý khác vẫn trả lời" có thể đẩy model trả lời một ý bằng bằng chứng mỏng ⇒ đo ba dòng sàn ngoài kho; người thứ hai đọc tay các lượt câu ghép được cứu.
- Đổi mô tả công cụ là đổi tiền tố lời gọi ⇒ mọi so sánh phải cùng buổi, hai lượt để biết nhiễu.

## 5. Không làm ở hai bậc này

Thử lại có lùi, gom "năng lực model" thành bảng ở lớp nối, công cụ mới (liệt kê theo loại, mở bài theo tên), nhiều câu tìm ở lần tìm đầu (đề nghị đo riêng bằng cờ sẵn có `lan_tim_dau: v3`), đổi lời dặn hệ thống.
