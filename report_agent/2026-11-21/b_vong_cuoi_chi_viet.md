# Vòng cuối chỉ viết · báo cho model khi hết công cụ · trạng thái "không có số" của công cụ khoảng cách (nhánh `p9-b-vong-cuoi-chi-viet`)

Viết: 13:36 21/11/2026 (giờ `date`), phiên B. Plan đã duyệt: `report_agent/2026-11-21/b_bac_1_vong_cong_cu_plan.md` phần 1a (cổng "có lượt chạm trần vòng" đạt nhờ số người dùng mô phỏng).
Trạng thái: code + test xong, BA cờ đều TẮT; chờ phiên đo chạy thước và bộ câu khó trên cả hai model rồi phiên điều phối quyết bật.
Từ dùng: *vòng* = một lần gọi model trong một lượt hỏi · *chạm trần vòng* = hết số vòng cho phép mà model chưa viết ⇒ người dùng nhận câu từ chối trống ·
*công cụ bị ẩn* = lần gọi model đó không được đưa công cụ ấy · *luna* = gpt-6-luna · *Sonnet* = Claude Sonnet 5.5 mức suy luận high (model đang chạy từ chiều 21/11).

## 1. Lỗi và nguyên nhân

Người dùng mô phỏng (phiên khác chạy và đọc tay): luna chạm trần vòng 6 lượt / 48, một khuôn — MỘT tin có 3–5 ý, trong đó có "từ … ra … bao xa / đi đường nào" tới một nơi không có trong
bảng khoảng cách ⇒ model tìm kho 3 lần + gọi công cụ khoảng cách 3 lần cho cùng nơi ⇒ hết 6 vòng ⇒ câu từ chối trống cho cả tin.
Tái hiện bằng câu tự đặt: bộ 5 câu HAI ý viết trước khi xem lượt hỏng không tái hiện được (luna 0 / 10); bộ 5 câu viết lại theo hình dạng "một tin 3–5 ý" thì ra (luna 3 / 15).

## 2. Ba phần, mỗi phần một cờ (đều mặc định TẮT; tắt ⇒ chuỗi gửi model giống từng byte)

| Cờ (`assistant.…`) | Đổi gì |
|---|---|
| `vong_cuoi_chi_viet` | Lần gọi model CUỐI của lượt không kèm công cụ nào ⇒ model viết từ bằng chứng đã có. Kết quả của công cụ chạy ở lượt sát cuối được nối một dòng báo "bước kế không còn công cụ, hãy viết; ý nào bằng chứng không nói thì nói rõ là tư liệu chưa có". Model vẫn xin công cụ ⇒ kết cục như hôm nay (câu từ chối cố định), không thành lỗi. |
| `bao_het_luot_tim` | Kết quả của lần tìm kho cuối được phép (lần thứ hai) được nối một dòng báo "từ bước kế không còn công cụ tìm kho". Từ 12/11 công cụ tìm bị ẩn sau lần đó mà model không được báo. |
| `khoang_cach_trang_thai` | Công cụ khoảng cách không có số cho cặp nơi ⇒ kết quả mở đầu bằng dòng "Trạng thái: không có số liệu… đừng gọi lại cho cùng cặp nơi; vẫn trả lời các ý khác". Dòng đứng ngoài khối nguồn; nguồn "chưa có số" vẫn được đăng để trích. |

Hai dòng báo đều nối vào CUỐI kết quả công cụ ⇒ không đổi phần đã gửi model trước đó, áp cho cả hai model.

## 3. Số đo — 5 câu tự đặt dạng "một tin 3–5 ý có bao xa", qua `answer_turn` (code sản phẩm, không server)

| Cấu hình | Model | Chạm trần / từ chối trống | Lỗi | Lời gọi model nhiều nhất / lượt | Lâu nhất |
|---|---|---|---|---|---|
| bản chính, không cờ | luna (× 3) | 3 / 15 | 0 | 6 | 17,9 s |
| chỉ `vong_cuoi_chi_viet` | luna (× 3) | 0 / 15 | 0 | 6 | 18,3 s |
| cả ba cờ | luna (× 3) | 0 / 15 | 0 | 4 | 13,2 s |
| cả ba cờ | Sonnet (× 2) | 0 / 10 | 0 | 4 | 21,3 s |

Ba câu đối chứng mỗi lượt (khoảng cách có trong bảng · câu một dữ kiện · câu kho không có): kết cục không đổi; câu kho không có vẫn ra câu từ chối cố định. Lỗi trích nguồn: 0 ở mọi dòng.
Chưa đo: Sonnet không cờ trên 5 câu này (người dùng mô phỏng cho Sonnet 0 lượt chạm trần ⇒ phần này chủ yếu cứu luna).

**Hai lần làm sai trong lúc viết, ghi lại vì đều lộ ra nhờ chạy thật:**
1. Bản đầu chỉ ẩn công cụ ở vòng cuối, KHÔNG báo gì: luna vẫn xin công cụ ⇒ 3 / 15 lượt thành LỖI. Ẩn mà không nói chỉ đổi dạng hỏng.
2. Bản hai tính "vòng cuối" bằng bộ đếm số lần gọi đã xong: SDK kiểm công cụ còn bật hay không cả lúc THỰC HIỆN lời xin của lần gọi vừa xong, lúc đó bộ đếm đã bằng mốc ⇒ chính công cụ model vừa xin bị coi là đã tắt.
   Sửa: công tắc chỉ lật SAU KHI công cụ của lượt sát cuối chạy xong. Số ở bảng trên là của bản đã sửa; test `test_vong_cuoi_chi_viet` bắt đúng lỗi này (đỏ trước khi sửa).

**Câu "một ngọn núi cao bao nhiêu mét" của bộ chuỗi (kho có đáp án ở bài mang tên chính của núi), Sonnet × 5:** không cờ — 3 câu từ chối, 1 câu trả lời phần kho có, 1 lỗi kiểm trích nguồn;
ba cờ — 4 câu từ chối, 1 câu trả lời phần kho có, 0 lỗi. Tức các dòng báo KHÔNG giúp model tìm ra đáp án (muốn vậy model phải tìm lần ba bằng tên chính — thuộc việc mô tả công cụ tìm),
chỉ làm lượt kết thúc sạch hơn. Mẫu 5 lượt: không đủ để nói "hết dạng nộp câu tìm làm câu trả lời".

## 4. Kiểm

`test_vong_cuoi_chi_viet` 6 ca (vòng cuối không công cụ + dòng báo đúng chỗ · lượt kết thúc sớm gửi giống byte cờ tắt, cả lượt có lịch sử · model vẫn xin công cụ ⇒ câu từ chối cố định ·
dòng báo ở lần tìm cuối · trạng thái khoảng cách) · `test_het_luot_tim` 7 · `test_b2_tool_loop` 12 · `test_khoang_cach` 101 · `test_bedrock_model` 20 · `test_cau_nhieu_y` 44 · `test_chat_stream` 25 · `test_phase6_settings` 5.
Chưa chạy: đường stream với model thật; cả bộ test.

## 5. Giới hạn / chưa làm

- Lượt được "cứu" ở vòng cuối viết từ bằng chứng đã có ⇒ rủi ro với sàn "câu ngoài kho không được trả lời bằng kho": phải đo ở thước (ba dòng sàn) trước khi bật.
- Sonnet ở vòng cuối không công cụ vẫn có thể viết chữ thường thay vì nộp qua công cụ nội bộ — đã có đường bọc (bản sửa trưa 21/11).
- Người dùng nhận câu trả lời thiếu ý "bao xa" kèm lời nói rõ chưa có số — không phải số ước.
