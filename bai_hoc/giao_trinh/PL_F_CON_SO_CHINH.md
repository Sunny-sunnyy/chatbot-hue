# Phụ lục F — Các con số chính trên một trang

*Cập nhật 14:43, ngày 23/11/2026 · khớp các bài 14:35 23/11 (50 tính năng mở, 5 tắt, kho 267 bài) · lượt 14:34: số tính năng 49 ⇒ 50 (đoạn dặn câu tỉnh khác); năm con số mới của câu hỏi việc ở tỉnh, thành khác — 12 ⇒ 0 trên 20, 1 trên 40 · 3 trên 10, 1.233 ⇒ 2.311 ký tự (mục 3), 113 trên 120, 12 ⇒ 1 trên 20 (mục 4) (118 dòng) · lượt hai: thẻ "Hôm nay ở Huế" (97 bài, 400 ngày); dòng bộ test ghi 88 file trong thư mục lúc 13:52 (120 dòng) · bản 12:55, lượt hai: lần chạy đủ bộ test mới nhất nay là 12:05–12:23 23/11 (2.228 ca đạt), lượt 09:41–09:59 thành lần trước đó; số tính năng 49 mở, 5 tắt; dòng 761 ảnh ghi đúng phạm vi lượt chụp lại thẻ chọn tên ảnh (113 dòng) · bản 12:31, ngày 23/11/2026, khớp các bài trưa 23/11 (49 tính năng, kho 267 bài): số tính năng 48 ⇒ 49; bảng quán bản 4; năm con số mới — 30 trên 41 quán có giờ và 5 trên 6 ⇒ 0 trên 6 của "gần một điểm" (bài 24), 11 trên 25 lịch mất câu tả lăng Thiệu Trị (bài 29), 766 ⇒ 0 trên 960 tổ hợp có quán lệch bữa (bài 30), lượt "dùng như người thật" đầu tiên (bài 38); dòng 761 ảnh ghi thẻ chọn tên ảnh đã sửa (113 dòng) · bản 11:33, ngày 23/11/2026, khớp các bài sáng 23/11 (giao diện mới, 48 tính năng, kho 267 bài): lần chạy đủ bộ test mới nhất 09:41–09:59 23/11 (82 file chạy, 2.218 ca đạt); năm con số của giao diện mới (mục 9); bốn con số của hai phép đếm 0 đồng và của việc gọi lại một lần (mục 8); dòng tin dài nói thẻ chờ (108 dòng) · trước đó (22/11: lần chạy 20:48–21:07, tin dài nhiều ý, lệnh thêm điểm, thẻ nơi; gom lần đầu); bài gốc đổi thì trang này phải gom lại.*

**Cách dùng trang này.** Mỗi dòng là một con số quan trọng của hệ thống, chép từ mục "Ý chính", bảng "Cấu hình đang chạy" hoặc bảng số chính của một bài. Cột thứ ba ghi điều kiện mà bài gốc ghi kèm: đếm trên bộ nào, model viết nào, ngày nào. Một con số không có điều kiện thì không so được với con số khác, nên đừng đọc cột hai mà bỏ cột ba. Dòng ghi "cấu hình" là giá trị đặt sẵn trong hệ thống, không phải kết quả đo. Dòng ghi "lúc đó" hay "đã cũ" là số của một thời điểm đã qua, giữ lại để so. Hai model viết: gpt-6-luna (tới trưa 21/11) và Claude Sonnet 5.5 (từ 21/11, đổi tạm).

## 1. Kho và giai đoạn chuẩn bị

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 267 bài | số bài của kho, chia 5 chủ đề, 7 thư mục | đếm từ bản ghi chỉ mục, 16:35 ngày 22/11 (265 lên 267 bài trong ngày 22/11) | 2, 7 |
| 9.479 đoạn | số đoạn sau khi cắt 267 bài; cũng là số điểm trong Qdrant | bản ghi chỉ mục và Qdrant, 16:35 ngày 22/11 | 2, 8, 12 |
| 512 token | độ dài tối đa model embedding đọc được; giới hạn thật lúc cắt còn chặt hơn (256 token của một model ứng viên cũ) | cấu hình, sáng 22/11 | 8, 10 |
| 4 tới 6 trên 32 câu | số câu mất đáp án khi gộp đoạn to (từ 256 token trở lên); gộp tới 128 token thì không khác | phép so 12 cách cắt, bộ 32 câu (lúc đó) | 8 |
| 384 con số | số chiều của mỗi vector (model multilingual-e5-small, chạy trên máy) | cấu hình, sáng 22/11 | 10 |
| 2 câu giúp, 3 câu hỏng trên 40 câu | model embedding lớn hơn khoảng 70 lần, gọi qua mạng, chậm hơn khoảng 100 lần | phép so 5 model khác (lúc đó) | 10 |
| 5.960 từ | từ điển của kho cho tìm theo từ khoá | kho hiện nay, 16:35 ngày 22/11 | 11 |
| khoảng 225 giây | lập lại toàn bộ chỉ mục | số đo ghi trong hướng dẫn vận hành | 2, 12 |
| 37,7 giây cho 105 đoạn | lần chạy thật đầu tiên của lệnh cập nhật riêng, sau khi sửa 2 bài; kết quả giống lập lại toàn bộ | sáng 22/11 (kho 9.436 lên 9.442 đoạn lúc đó) | 7, 12 |

## 2. Tìm

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 30 ứng viên | số đoạn lấy theo nghĩa, rồi BM25 chấm lại | cấu hình, sáng 22/11; đã thử 100: kém hơn, mất đoạn đúng ở 1 câu | 10, 11, 13 |
| 10 đoạn | số đoạn ở lần tìm đầu; chương trình kiểm lúc bật | cấu hình, sáng 22/11; 5 đoạn kém hơn, 15 đoạn không khá hơn | 1, 2, 13 |
| 2 đoạn mỗi vế, nhiều nhất 6 vế | phần nối thêm cho tin nhiều ý | bật 09:47 22/11 | 13, 23 |
| 16 trên 40 câu khó | số câu thiếu đoạn đúng trong 10 đoạn (9 vì đứng dưới hạng 10, 7 vì không lọt 30 ứng viên) | 40 câu khó, kho cuối tháng 10 | 13, 40 |
| 33 / 24 trên 40 câu khó | số câu có đủ đoạn đúng trong 30 ứng viên / trong 10 đoạn | 40 câu khó, kho cuối tháng 10, bản nhãn thứ năm (30/10) | 13, 18 |
| 22 trên 38 câu | số câu có đủ đoạn đúng trong 10 đoạn, lần đo gần nhất | 19/11, 38 câu | 18 |
| 158 câu / 55 câu | thước nhanh chạy trên 158 câu có đáp án trong kho; thước chính xác (nhãn đoạn đúng) chỉ có cho 55 câu khó (40 để thử, 15 để kiểm lại) | cấu hình đo, sáng 22/11 | 18 |
| 22 lên 31 trên 40; 5 câu tệ đi (cho phép 4) | để gpt-6-luna tự chọn 10 trong 30 ứng viên: bước tìm tốt hơn, nhưng bị gác; cả câu 6,5 giây, đắt gần gấp 4 | gpt-6-luna, 40 câu khó, bản nhãn đầu tiên (27/10; theo bản nhãn thứ năm mốc là 24) | 14 |

## 3. Viết câu trả lời và kiểm nguồn

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 0 trên 489 lần viết | lỗi số nguồn | gpt-6-luna, đếm 30/10 | 16 |
| 0 trên 93 lượt | lỗi số nguồn | một lượt rà ngày 21/11, gpt-6-luna và các mức suy luận của Claude Sonnet 5.5 | 16 |
| 3 trên 7 ⇒ 0 trên 5 | số lần ra màn hình lỗi ở tin kiểu "bỏ X đi", trước và sau khi có lần chạy lại cả lượt | đo 22/11, Claude Sonnet 5.5 | 6, 16 |
| 12 trên 20 ⇒ 0 trên 20 | số lần câu "Từ Huế vào Hội An thì ở Hội An nên ăn món gì?" được trả lời bằng kho (không phải câu từ chối và có ít nhất một nguồn), đoạn dặn câu tỉnh khác tắt ⇒ mở; câu Đà Nẵng cùng phép: 10 ⇒ 0 trên 10. Đây là lời dặn, không phải bước kiểm: 0 trên 20 ở lượt đo chỉ cho nói mức hở dưới khoảng 14 % | Claude Sonnet 5.5 mức cao, gọi thẳng phần lõi, cùng buổi 23/11; mở từ chiều 23/11, chỉ đường model đang chạy | 16, 15 |
| 1 trên 40 · 3 trên 10 | cùng câu đó được trả lời bằng kho: mốc 21/11 (chưa có công cụ liệt kê bài) · trưa 23/11 trên nhánh chính, chưa có đoạn dặn; đường model cũ ngày 21/11: 2 trên 10 và 3 trên 5 | Claude Sonnet 5.5 mức cao (mốc 21/11 gộp năm lượt cùng điều kiện); gpt-6-luna (model cũ) | 16, 33 |
| 1.233 ⇒ 2.311 ký tự | lời dặn của lượt có công cụ, trước ⇒ sau khi nối đoạn dặn câu tỉnh khác | cấu hình từ chiều 23/11, chỉ đường Claude | 16 |

## 4. Trợ lý (harness), nhớ cuộc trò chuyện, xếp loại câu, công cụ

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 3 lần | số lần model được tự tìm kho mỗi lượt hỏi | cấu hình từ 14:47 22/11 (trước là 2) | 3, 21, 23 |
| 5 vòng (+1 mỗi công cụ ngoài tìm kho, trừ thời tiết) | trần vòng gọi model của một lượt; trần thực tế của lượt hỏi đáp hiện là 6 trở lên | cấu hình từ 14:47 22/11 (trước là 4) | 21 |
| 45 giây | hạn cho các vòng của trợ lý cộng lại; lần viết lại, lần chạy lại, lần viết mục web mỗi cái có 45 giây riêng | cấu hình, sau 14:47 22/11 | 6, 15, 21 |
| +1,17 điểm đủ ý; từ chối nhầm 12 ⇒ 4–6 trên 158 | khi mở cho trợ lý tự tìm thêm (lúc đó trần 2 lần) | gpt-6-luna, 18 câu cần nhiều nguồn và 158 câu (khoảng tin cậy +0,44 tới +2,00) | 3, 21 |
| 6 trên 6 | số lần nêu đúng cả hai ý kho có ở một tin 4 ý, sau bốn thay đổi khâu tìm mở cùng nhau; 0 màn hình lỗi (trước: 3 trên 6 lần ra "Thử lại") | một tin 4 ý, 6 lần, Claude, chiều 22/11 | 3, 16, 40 |
| giờ 4, 3, 1 trên 9 ⇒ 0 trên 12 · vé lẻ An Định 7 trên 9 ⇒ 0 trên 12 | câu trả lời có dòng "Tư liệu chưa có thông tin về…" sai về giờ của ba điểm phụ (Lăng Dục Đức, Cung An Định, Bảo tàng Cổ vật) và về vé lẻ Cung An Định, trước ⇒ sau thẻ nơi (trước đó 8 trên 9 câu trả lời có ít nhất một dòng sai); sau: nêu đúng giờ Cung An Định 11 trên 12, vé lẻ An Định 11 trên 12; nơi kho không có giờ, vé 0 trên 12 lượt bịa | một tin 4 ý, Claude Sonnet 5.5, 22/11: trước = 9 câu trả lời đã ghi; sau = hai lượt thật × 6; phiên đo chấm | 23, 40 |
| 34 trên 34 · 113 trên 174 | cặp (nơi, thuộc tính) bị ghi thiếu sai thuộc loại giờ, địa chỉ, vé có đúng dòng trong thẻ nơi · số bài nơi có dòng để chép thành thẻ | dựng thử bằng chương trình trên ngữ cảnh đã ghi của 54 lượt nhiều ý, 22/11, không qua model · kho 267 bài, đếm 17:22 22/11 | 23 |
| 4 trên 60 câu | số câu cần công cụ mà cách đưa công cụ theo từ khoá bỏ sót | đếm 21/11 trên 310 câu của sổ ghi lượt hỏi | 3, 21 |
| 3 lượt, 30 phút, 500 cuộc | máy chủ nhớ 3 lượt gần nhất mỗi cuộc, hết hạn sau 30 phút, nhiều nhất 500 cuộc | cấu hình, sáng 22/11 | 6, 23, 35 |
| 4.000 ký tự | phần câu trả lời liền trước được gửi kèm (trước là 1.200) | cấu hình, bật 09:40 22/11 | 23 |
| 3 trên 3 · 3 trên 3 | trong cuộc đã lập lịch, nhờ "Bỏ quán đầu đi rồi viết lại danh sách": lịch không đổi · danh sách bỏ đúng quán đầu và đủ các quán còn lại (2 lần khớp đúng, 1 lần thêm một mục có nguồn); bên không nhớ: câu "không xác định được quán đầu" | 9 lượt thật, một chuỗi tin × 3, Claude Sonnet 5.5, 22/11; mở từ 16:08 22/11 | 23, 31 |
| 10 giây | hạn của bước xếp loại câu; quá hạn thì coi là "về Huế" | cấu hình, sáng 22/11 | 6, 22 |
| 113 trên 120 | số lần câu "Từ Huế vào Hội An thì ở Hội An nên ăn món gì?" (có chữ "Huế") được bước xếp loại cho đi đường "về Huế"; ngày 21/11 cùng câu: 39 trên 40 | sáu ô đo 23/11, Claude Sonnet 5.5, gọi thẳng phần lõi | 16, 22 |
| 12 ⇒ 1 trên 20 | lần câu ví dụ trên được trả lời bằng kho khi tắt riêng công cụ liệt kê bài (kèm một vòng), dù model không gọi công cụ đó ở lần nào trong 12 lần sai; chỉ đưa hai giới hạn tìm, vòng về như 21/11: 8 trên 20. Việc công cụ có mặt làm model bớt từ chối là cách nhóm đang hiểu, chưa phải kết luận chắc | một câu, 20 lần mỗi ô, Claude Sonnet 5.5 mức cao, 23/11; ô này không có ngưỡng ghi trước | 21, 16 |
| sớm hơn 1,37 giây | chữ đầu tới sớm hơn khi xếp loại câu chạy song song (khoảng tin cậy 0,34 tới 2,14) | gpt-6-luna, 20 cặp, 04–05/11; chưa đo lại với Claude | 6, 22, 34 |
| 9 câu từ chối nhầm bớt, 0 câu sai ngày | khi chương trình tính ngày thay model | gpt-6-luna, 09/11 | 1, 3, 24, 40 |
| 40 điểm, 1.560 cặp | bảng khoảng cách dựng sẵn; không gọi mạng lúc trả lời | cấu hình, trưa 22/11 | 24 |
| 30 trên 41 quán | quán có bài kho mà bài riêng có dòng "Giờ hoạt động", nên công cụ "gần một điểm" in được giờ cạnh tên quán (11 quán kia không in gì, chương trình không đoán giờ) | bảng quán bản 4, đếm trưa 23/11; in giờ từ 11:56 23/11 | 24 |
| tắt 5 trên 6 ⇒ bật 0 trên 6 | câu hỏi "ăn gì gần X" kèm bữa mà câu trả lời gợi ý cho bữa được hỏi một quán kho ghi đóng bữa đó, trước ⇒ sau khi "gần một điểm" in giờ quán; 2 câu không kèm bữa dài hơn tới 1,4 lần | 8 câu (6 kèm bữa + 2 không), mỗi bên một lượt, Claude Sonnet 5.5, 23/11; phiên đo chưa chấm | 24 |

## 5. Tra web và hỏi bằng ảnh

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 1 lần, 5 giây, 5 kết quả | một lần gọi dịch vụ tìm web, không gọi lại | cấu hình, trưa 22/11 | 6, 25 |
| 2 trên 44 câu | câu ngoài phạm vi lọt vào đường "về Huế" vì xếp loại nhầm và bị đem đi tra web, với bốn tuyến như đang chạy; người dùng chỉ thấy câu cố định, nhưng câu hỏi đã bị gửi ra dịch vụ tìm web (phương án "hai nhóm", đo 09/11, đã bỏ, cũng ra 2 trên 44 nhưng là một phép đo khác: câu ra tới người dùng kèm mục web — bài 22) | lượt đo giữa kỳ 12/11 | 22, 25, 40 |
| 42 tên | danh sách nơi và món dễ nhận ra bằng ảnh; model trả tối đa 3 mã | cấu hình, trưa 22/11 | 26 |
| 20 giây | hạn của lần nhìn ảnh | cấu hình, trưa 22/11 (bản đầu 15 giây) | 6, 26 |
| 2 trên 5 ảnh | ảnh không phải Huế bị model gán tên Huế khi cho trả lời thẳng (ngưỡng ghi trước: nhiều nhất 1) | gpt-6-luna, 05/11 | 26, 40 |

## 6. Đo

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 176 câu | bộ câu hỏi mẫu chính, năm loại; 120 câu để thử, 56 câu để kiểm lại | cấu hình đo, sáng 22/11 | 17 |
| 29 câu | câu "không tự nhiên" bị bỏ khỏi số chính | như trên | 17 |
| 129 câu | số câu của số chính (bỏ câu không tự nhiên và câu ngoài kho) | như trên | 19 |
| 32 câu (+15 đối chứng) | bộ an toàn: 28 kho có, 4 kho không có | như trên | 17 |
| 36 câu và 40 câu | hai bộ câu cất riêng đi kèm bộ 176 câu; cả hai đã dùng | như trên | 17 |
| đúng 4,71 · đủ ý 4,58 · trọng tâm 4,72 | ba điểm (thang 1–5) trên 129 câu; bản đầu tiên 4,43 · 4,28 · 4,45 | gpt-6-luna | 19 |
| 3,50 | điểm đủ ý của câu nhiều nguồn (câu một dữ kiện 4,91) | gpt-6-luna | 19 |
| 3 trên 158 câu | từ chối nhầm, khoảng 2 % (22 khi đưa 5 đoạn; 12 khi đưa 10 đoạn) | gpt-6-luna, lượt đo cả hệ thống 12/11; lượt đo cuối 18/11 cũng ra 3 | 4, 19, 40 |
| 0 trên 78 câu | từ chối nhầm | Claude, 21/11, mẫu nhỏ hơn | 4, 40 |
| 0 trên 18 · 1 trên 18 | câu ngoài kho bị trả lời: 0 ở bản hỏi đáp (01/11) và ở lượt 12/11; 1 ở lượt đo cuối 18/11 của bản trợ lý (điều kiện: 0) | gpt-6-luna | 19 |
| 4,18 so với 4,58 | điểm đủ ý trên bộ cất riêng 40 câu so với bộ quen; số trên bộ quen lạc quan hơn khoảng 0,4 | gpt-6-luna | 17, 19, 40 |
| 7 · 7 · 8 trên 12 so với 6 · 5 · 6 | số phiên đạt của 12 người dùng mô phỏng, ba lượt mỗi bên | Claude Sonnet 5.5 so với gpt-6-luna, 21/11 | 32, 40 |
| 8 trên 12 phiên, 33 trên 38 ý | đo lại 12 vai, trong khoảng nhiễu; chạy trước bốn thay đổi khâu tìm | Claude, 14:13 22/11 | 32, 40 |
| 39 trên 41 | bộ 41 câu khó, đạt máy | Claude, lượt mới nhất | 32 |
| 0 trên 10 | số lần kịch bản demo hỏng | cả hai model | 32 |
| 3 mục · 1 phiên | mức nhiễu: bộ 41 câu lệch tới 3 mục, 12 vai lệch 1 phiên khi chạy cùng một hệ thống hai lần | đo ở bài 32 | 32 |
| 12 trên 19 · 2 trên 5 | số ý trượt do kho thiếu: 12 trong 19 lần ý trượt (1 do tìm); lượt đo lại còn 5 ý trượt, 2 do kho thiếu, 0 do tìm | ba lượt mốc 21/11; lượt đo lại 22/11 | 40 |
| khoảng 13 % | dòng "Tư liệu chưa có thông tin về…" sai (kho có), TRƯỚC khi có thẻ nơi (17:15 22/11); chưa đếm lại | một phiên đọc tay 30 trong 119 dòng của ba lượt mốc; khoảng tin cậy 4–31 % | 40 |

## 7. Lên kế hoạch và sửa lịch

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 8 giá trị | số ô của biểu mẫu máy chủ nhận và kiểm | cấu hình, trưa 22/11 | 5, 27 |
| 41 điểm | bảng điểm tham quan (bản 10); 40 điểm có toạ độ, 40 điểm có ảnh | cấu hình, trưa 22/11 | 27, 30 |
| 8 cụm, 8 cặp kề | nhóm điểm theo khu; một ngày nhiều nhất 2 cụm kề nhau | cấu hình, trưa 22/11 | 27, 28 |
| 5 ngày · 2 sở thích · 180 ngày | số ngày tối đa, số sở thích tối đa, ngày đi xa nhất | cấu hình, trưa 22/11 | 27, 28 |
| 210 / 240 phút / 1 điểm | quỹ một buổi: cân bằng / khám phá nhiều / nhẹ nhàng | cấu hình, trưa 22/11 | 28 |
| 0,2 giây · 9,3 giây | khung lịch hiện · đủ câu mô tả | ví dụ, Claude, 21/11 | 27, 40 |
| 23 luật, 0 lỗi | bước kiểm khung đối chiếu lịch; đã chạy trên mọi tổ hợp biểu mẫu | mô phỏng bằng chương trình | 29 |
| 11 trên 25 lịch ⇒ 0 câu dự phòng | lịch mặc định mà câu tả lăng Thiệu Trị (câu so sánh đúng tư liệu) bị thay bằng câu dự phòng, trước ⇒ sau khi nới luật kiểm câu; lượt chấm sau sửa: 81 câu, 0 câu bị thay | lịch chạy qua chương trình máy chủ, Claude Sonnet 5.5, 23/11: trước 25 lịch, sau 6 lịch; lượt chấm 9 lịch | 29 |
| 16 trên 20 ⇒ 20 trên 20 | nghiệm thu câu mô tả: lần đầu trượt, sau khi chọn tay đoạn kho thì đạt | nghiệm thu lịch (lúc đó) | 29 |
| 136 cơ sở, tối đa 5 | cơ sở lưu trú (bản 6, 67 có ảnh) và số cơ sở gợi ý | cấu hình, trưa 22/11 | 30 |
| 467 quán; 2 quán mỗi bữa, 2 km | bảng quán (bản 4, 23/11: 6 quán kho mang dấu "bữa không hợp", 30 quán kho mang dòng giờ); giới hạn mỗi bữa | cấu hình, trưa 23/11 | 30, 24 |
| 766 ⇒ 0 trên 960 tổ hợp | tổ hợp biểu mẫu (không ngày đi) có ít nhất một quán ở bữa mà bài kho ghi quán đóng, trước ⇒ sau dấu "bữa không hợp" (riêng Bún bò Bà Nga ở bữa trưa: 756); phép đếm độc lập trên 3.840 khung: 3.066 ⇒ 0 | chỉ chương trình, 0 USD, 23/11; chỉ tính 6 quán kho có giờ rõ | 30 |
| 9 trên 10 | bộ 10 chuỗi sửa lịch đạt (cả hai lần chạy) | đo 14–19/11, trước khi đổi sang Claude | 31, 40 |
| 90 % trong 15.360 cặp, 0 lỗi | đổi chỗ hai ngày làm được | đếm bằng chương trình | 31 |
| 5 / 6 · 2 / 6 · 0 / 6 | lệnh sửa lịch khó làm đúng ở mức suy luận cao / thấp / vừa | Claude Sonnet 5.5, 21/11 | 31, 33 |
| 0 trên 14.725 lệnh | lệnh thêm một điểm làm được mà giữ đủ điểm cũ, trên lịch vừa xếp (lịch xếp kín giờ, chương trình không tự thế chỗ) | liệt kê bằng chính bộ xếp và phần áp lệnh trên 108 lịch mẫu, tối 22/11; không phải lượt người dùng thật | 31, 40 |

## 8. Model viết, thời gian chờ, tiền

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 9 loại lời gọi | số việc dùng chung một model viết; đổi model là đổi tất cả | hồ sơ đếm, trưa 22/11 | 33 |
| khoảng 3 lần · 20 lần | Claude viết dài hơn khoảng ba lần; đắt hơn 20 lần mỗi token | Claude Sonnet 5.5 so với gpt-6-luna | 33, 34 |
| 2 / 10 USD · 0,10 / 0,50 USD | giá mỗi 1 triệu token chữ vào / chữ ra: Claude Sonnet 5.5 · gpt-6-luna | cấu hình, sáng 22/11 | 15 |
| khoảng 0,3 giây | mức cao chậm hơn mức vừa ở câu hỏi một lượt (bốn mức ngang nhau về chất lượng) | Claude, 66 câu | 33, 34 |
| khoảng 8 giây | mức vừa nhanh hơn mức cao ở tin dài nhiều ý (trung vị 19,3 so với 27,3 giây), nhưng trượt một điều ghi trước, và 3 trên 6 lượt nói kho không có vé cho bé dưới 7 tuổi ⇒ bỏ | một tin gia đình 4 ý, 6 lượt mỗi mức, Claude, 22/11; mốc không chạy xen kẽ | 33 |
| 6 ⇒ 0 trên 29 | số câu chạm trần vòng trước và sau khi sửa lớp nối Claude (trước đó Claude xin công cụ mãi: 0 trên 8 lần viết được, ở mỗi mức) | Claude, khi đổi model | 33 |
| 3,7 giây (model viết 3,6 giây) | thời gian cả câu ở ví dụ chính | ví dụ chính, lượt chạy thật | 6 |
| khoảng 13 giây | thời gian chờ ở lượt hỏi đáp đứng giữa; một phần ba số lượt quá 15 giây | Claude mức cao, 49 lượt của người dùng mô phỏng, 21/11 | 34, 40 |
| 9,7 giây (72 %) · 3,1 giây (25 %) · 3 % | phần của lần viết cuối · các vòng công cụ (khoảng 2,2 giây một vòng) · phần của chương trình | như trên | 34 |
| 6,9 giây; 95 % dưới 13,1 giây | thời gian cả câu ở lượt đứng giữa, 0 màn hình lỗi | 41 tin phần lớn ngắn qua trình duyệt, lượt kiểm chốt trưa 22/11, lúc máy rảnh | 34, 40 |
| 25–34 giây | thời gian chờ của tin dài nhiều ý (trước khoảng 20 giây), suốt lúc đó chỉ có thẻ chờ rồi cả câu trả lời; lượt phải viết lại một lần lâu thêm khoảng 10 giây (tới 25–37 giây; ca này chưa nhìn trên trình duyệt) | một tin 4 ý, 6 lần, từ 14:47 22/11; trên trình duyệt 22/11, giao diện cũ, tin gia đình bốn ý 29,5 giây; trên giao diện mới mới có ảnh chụp tự động lúc chờ, chưa đo thời gian | 23, 34, 40 |
| 23,4 giây · 29,1 giây | tin dài nhiều ý: trung vị của lượt model tự tìm một lần · hai lần (lần tìm thứ hai làm lượt dài thêm khoảng 5,7 giây) | 19 lượt đã ghi của một tin gia đình, Claude mức cao, 22/11, nhiều bản chương trình trong buổi; đếm trên sổ, không chạy thêm | 34 |
| khoảng 0,15 giây + 8,67 phần nghìn giây mỗi token | giây của một lời gọi model theo số token viết ra; 218 điểm gần như nằm trên một đường thẳng (hệ số tương quan 0,995): thời gian chờ gần như chỉ là số token model viết ra | 218 lời gọi viết, sổ vết 22–23/11, Claude Sonnet 5.5 mức cao; đếm 0 đồng sáng 23/11, không phải lượt đo mới | 34 |
| 18,5 trong 24,8 giây · khoảng 6 trong 25 giây | tin dài, trung vị: riêng lần viết trong các lời gọi trợ lý (74,9 %; 669 token suy luận, khoảng 5,9 giây) · lợi lớn nhất nếu lần viết không suy luận chút nào ⇒ không dựng | 60 tin dài (lời gọi viết từ 15 giây) trong 218 lượt như trên; 60 tin dài chỉ gồm hai câu khác nhau | 34 |
| 193 trên 259 · khoảng 2 giây | số lần model tự tìm thêm mà thứ tìm đã có trong câu vừa gõ · một vòng tìm thêm; 75–100 % mỗi nhóm mang về đoạn mới được trích ⇒ không dựng | 218 lượt, 259 lần model tự tìm, sổ vết 22–23/11, Claude Sonnet 5.5; đếm 0 đồng sáng 23/11 | 23 |
| khoảng 1 trên 500 lượt | lỗi tạm thời phía nhà cung cấp model (ước từ hai lần gặp thật); từ 09:31 23/11 lời gọi đó được gọi lại một lần, lượt đó có thể chờ gần gấp đôi (tin dài tới khoảng 50 giây) | Claude Sonnet 5.5 qua Amazon Bedrock; gọi lại mới có ca test, chưa gặp lỗi thật | 33 |
| 17–24 giây | lượt nhờ "viết lại danh sách" (trợ lý tra kho lại và viết lại từng mục, không chỉ xoá một dòng); bên không nhớ câu trả lời: 10–12 giây cho một câu "không xác định được" | trên trình duyệt 22/11: 17,3 và 24,1 giây; lượt thật: 19–20 giây, khoảng 0,13–0,17 USD; Claude | 23 |
| 0,018 USD | tiền ví dụ chính (0,0178 USD) | Claude, lượt ví dụ chính 21/11 (bài 2, 6) | 2, 4, 6, 34 |
| 0,0004 USD · 0,0146 USD | tiền một câu trả lời có nguồn: gpt-6-luna · Claude mức cao (gấp khoảng 37 lần) (trung bình trên 66 câu tính điểm của 85 câu đầu bộ mẫu, không lọc theo loại câu) | 66 câu, 21/11 | 33, 34 |
| khoảng 0,0007 USD · khoảng 0,018 USD | tiền một câu ví dụ: gpt-6-luna · Claude (khoảng 25 lần) | câu ví dụ chạy thẳng qua code sản phẩm (không qua máy chủ), 21/11; mức suy luận: báo cáo gốc không ghi, hướng dẫn đổi model ghi "mức thấp" | 33 |
| đúng 4,97 ↔ 4,94 · đủ ý 4,83 ↔ 4,88 | điểm thang 1–5 của gpt-6-luna ↔ Claude; trọng tâm Claude thấp hơn rõ | 66 câu tính điểm, 21/11 | 33 |
| 24 giờ, 500 câu, khoảng 0,1 giây | bộ nhớ câu trả lời: hạn, trần, thời gian trả lại câu đã nhớ | cấu hình (bật từ 20/11) | 6, 34 |

## 9. Giao diện, máy móc, bảo mật, bộ test, cách làm

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 50 mở, 5 tắt | số tính năng đang mở / đang tắt (từ chiều 23/11 — dòng cấu hình ghi mở 13:11, vào nhánh chính 13:28 — thêm đoạn dặn câu tỉnh khác, tính năng thứ 50; từ 12:34 23/11 thêm hai dòng đang tắt, trước đó 3 tắt; lúc 10:25 22/11 là 42 mở; từ 14:47 thêm ba; từ 15:42 thêm một; từ 16:08 thêm việc nhớ câu trả lời liền trước cả trong cuộc đã lập lịch; từ 17:15 thêm thẻ nơi, là 48; từ 11:56 23/11 thêm giờ quán trong "gần một điểm") | đếm 14:24 23/11; từ 14:56 23/11 là 50 mở, 7 tắt (đếm 15:02, thêm hai tính năng buổi tối đang tắt, chờ chủ dự án quyết) (lúc 12:51 23/11: 49 mở, 5 tắt; lúc 12:25 23/11: 49 mở, 3 tắt; lúc 17:21 22/11: 48 mở) | 4, 16, 24, 40, phụ lục B |
| 5 khối · 6 bước · 4 thứ gửi ra ngoài | khối của hệ thống; bước của một câu hỏi; thứ rời máy (lời gọi model, ảnh, dự báo thời tiết, câu tra web) | kiến trúc, sáng 22/11 | 6 |
| khoảng 18 đường gọi | số đường gọi giữa giao diện và máy chủ; 3 đường gọi model | chương trình, trưa 22/11 | 35 |
| 869 điểm ảnh | chiều cao khung nhìn: thấp hơn thì sáu bến ở màn đầu Trang chủ chỉ còn tên, mất dòng mô tả, vì dòng mô tả chạm ảnh sông (đo tương phản 1,8 : 1 ở 1536 × 695; ngưỡng 4,5 : 1); gồm máy demo 1536 × 695 | cấu hình giao diện, bản chính từ 10:00 23/11 | 5, 35 |
| 6 · 3 tên bài | số tên bài nhiều nhất trong thẻ chờ: màn rộng (phần còn lại gộp thành "+k bài") · điện thoại, khung trợ lý nổi và khung nhìn cao tới 700 điểm ảnh, gồm máy demo 1536 × 695 (không có "+k bài") | cấu hình giao diện, 23/11 | 5, 35 |
| 761 ảnh · 8 khung nhìn · 49 cảnh | ảnh chụp tự động trước khi gộp giao diện mới: 0 cảnh không chụp được; máy dò tràn ngang và chữ bị cắt gắn cờ 1 ô (thẻ chọn tên ảnh ở 390 px, có từ giao diện cũ; sửa sau gộp, vào nhánh chính 11:26 23/11; chụp lại nhóm hỏi bằng ảnh ở 390 px (3 cảnh): 0 ô tràn — bài 26) | bản gộp thử, chạy trên máy, server thật, Claude Sonnet 5.5; 22/11 tối và 23/11 sáng; chạy trước ba bản sửa nhỏ của lõi (ba bản đó không chạm giao diện) | 35 |
| 97 bài (40 · 38 · 19) | vòng xoay của thẻ "Hôm nay ở Huế": điểm đến · di tích – di sản · đặc sản có ảnh chắc; hai bản trước 208 rồi 141 bài; hết 97 ngày thì quay lại | phép đếm trên danh sách 267 bài thật, 23/11; ở nhánh chính từ 13:32 23/11 | 5 |
| 400 ngày · 0 · 0 | kiểm phép chọn bài theo ngày bằng máy: 400 ngày liền, 0 ngày ra bài ngoài vòng xoay, 0 lần hai ngày liền trùng bài, đổi bài đúng 0 giờ Việt Nam | bản đầu (208 bài), bản dựng tĩnh, không máy chủ, 23/11; bản đang chạy (97 bài) thử trên máy chủ thật với ngày giả, bằng script; chưa ai dùng như người thật | 5 |
| 49 trên 50 bước | kịch bản thao tác đủ của cổng gộp: 49 đạt, 1 bước để người xem ảnh (trang Chỗ ở), 0 trượt | như trên | 35, 40 |
| 32 phút · 107 lượt công cụ · 3 điều mới | lượt "dùng như người thật" đầu tiên (agent tự lái trình duyệt, đọc chữ trên trang): ba điều mà 761 ảnh và 50 bước kịch bản không thấy; khoảng 82 nghìn ký tự đi vào ngữ cảnh của agent; một phiên chịu được khoảng một lượt cỡ đó | 10:36–11:08 23/11, máy chủ tạm của nhánh chính, 15 lượt gọi model | 38, 39 |
| 1.523 ⇒ 1.850 phép, 0 dưới ngưỡng | đo tương phản chữ / nền của giao diện mới: 1.523 phép trên 24 màn ở bốn bề rộng (bản dựng 19:56 22/11); đo lại trên bản đã gộp, có thêm sáu cỡ máy xách tay: 1.850 phép | chưa đo thẻ lịch đã xếp, khung trợ lý nổi, màn lỗi | 35 |
| khoảng 14 giây · 34 giây | lệnh bật ra "SẴN SÀNG" khi mọi thứ đủ · khi bắt đầu từ lúc Qdrant đang tắt | 14 giây: bốn ca chạy thật ở cổng tạm; 34 giây: lượt kiểm chốt trưa 22/11 | 36, 40 |
| 76 file, 2.060 ca | lần chạy đủ của lượt kiểm chốt trưa | trưa 22/11 | 38 |
| 75 file, 1.961 ca đạt, 4 file bỏ | lần chạy cuối buổi sáng; 4 file bỏ vì cần khoá OpenAI | sáng 22/11 | 38 |
| 82 file chạy, 2.228 ca đạt, 0 file đỏ, 4 file bỏ | lần chạy đủ mới nhất của cả bộ test (86 file trong bảng; 4 file bỏ cả file vì cần khoá OpenAI), trên nhánh chính đã có mọi bản sửa của sáng 23/11 (49 tính năng); 10 ca thêm so với lần trước đó (bảng quán của lịch, "gần một điểm", câu tả điểm); lần trước đó, 09:41–09:59 23/11, trên bản có giao diện mới và ba bản sửa lõi: 82 file chạy, 2.218 ca đạt (trước nữa, 20:48–21:07 22/11: 2.197 ca). Sau lượt này, 12:34 23/11 nhánh chính nhận một bản gộp có code (hai tính năng đang tắt); chưa có lượt đủ sau bản gộp đó. Lúc 13:52 23/11 thư mục test có 88 file (thêm một file của nhánh hết-vòng và một cho chữ đầu thẻ lịch của nhóm có trẻ em hay người lớn tuổi); chưa lượt chạy đủ nào có hai file này | 12:05–12:23 ngày 23/11 | 38, 40 |
| khoảng 16 tới 19 phút · khoảng 4,4 GB | cả bộ test chạy từng file một · bộ nhớ khi chạy cả bộ một lượt | hướng dẫn vận hành (khoảng 16 phút); lần chạy 12:05–12:23 ngày 23/11 khoảng 18 phút, lần 09:41–09:59 khoảng 18,5 phút | 38 |
| 5 phiên · 11 skill | số phiên làm việc (điều phối, hai thực thi, đo, giảng) · số file skill | cách làm lúc viết, trưa 22/11 | 39 |

<details><summary>Nguồn (để giữ trang đúng — anh không cần đọc)</summary>

Gom từ mục "Ý chính", bảng "Cấu hình đang chạy", bảng "Các con số chính của đường hỏi đáp" (bài 19), các bảng "Người dùng làm được" và "Chỗ yếu" (bài 40), cùng vài dòng "Chi tiết để tra" có số (bài 12, 34, 36, 40) của các bài 1–40 trong cùng thư mục, bản lúc 15:22 ngày 22/11/2026; không thêm sự thật mới. Gom lại 17:00 22/11/2026 theo các bài vừa sửa: số tính năng (bài 4, 40), hai dòng tiền (bài 33 "Chi tiết để tra": câu ví dụ chạy thẳng qua code sản phẩm; bài 34 bảng tiền: "không lọc theo loại câu"), "2 trên 44" (bài 22 quyết định về luật nghiêng về Huế, "Cái giá" và "Cách khác"), tin dài trên trình duyệt (bài 34 bảng "Nếu… thì sao"), hai dòng mới về cuộc đã lập lịch (bài 23 "Đã so" dòng 12 và "Giới hạn đã biết"). Lệnh đếm tính năng chạy lại 16:57 22/11 ra `47` [đã chạy]. Mỗi dòng giữ điều kiện bài gốc ghi; dòng nào bài gốc không ghi model thì không ghi. Chỗ hai bài ghi khác nhau về cùng một con số ghi ở báo cáo gom [riêng tư].

- Hai dòng thẻ nơi và số 48 (thêm 17:30 22/11/2026): bài 23 "Đã so" dòng 13, "Quyết định nhỏ hơn", Nguồn; bài 40 hàng "4. Thiếu ý"; số gốc ở `data/thu_bedrock_2026-11-21/b_dem_chua_co_2211/KET_QUA.md` phép đếm 3 và `…/b_x10_the_noi/luot_1/CHAM_E.md`, `luot_2/CHAM_E.md` [riêng tư; đã chạy, phiên khác]; 113 / 174: chạy `dung_bang` trên mục lục kho thật 17:22 22/11/2026 [tự chạy lệnh đếm]; 48: lệnh runbook mục 0 tự chạy 17:21 [tự chạy lệnh đếm]. Dòng 13 % thêm "trước thẻ nơi" cho khớp bài 40. Bảng từ 93 thành 95 hàng.

- Đợt 23/11/2026 (11:33): bộ test — bài 38 "Ý chính" và "Chi tiết để tra" (bản 11:15); 25–34 giây — bài 34 bảng "Nếu… thì sao" hàng tin dài (11:14); hai phép đếm 0 đồng — bài 34 "Đã so" (11:14), bài 23 "Đã so" dòng 15 (11:12); gọi lại một lần — bài 33 "Quyết định nhỏ hơn" (11:13); 869, 6 / 3 tên bài — bài 5 "Cấu hình đang chạy" (11:10) và bài 35 bảng lớp nhìn (11:17); 761 ảnh, 49 / 50 bước, 1.523 ⇒ 1.850 phép — bài 35 "Đã so" bảng cổng gộp. Bảng từ 99 thành 108 hàng.

- Đợt trưa 23/11/2026 (12:31): 30 trên 41 quán và 5 / 6 ⇒ 0 / 6 — bài 24 đoạn "Gần một điểm in kèm giờ của quán", "Đã so" dòng 7b; 11 trên 25 lịch — bài 29 "Đã so" khối "Câu so sánh bị thay oan"; 766 ⇒ 0, 756, 3.066 ⇒ 0 — bài 30 "Đã so" khối "Quán lệch bữa"; bảng quán bản 4 — bài 30 "Cấu hình đang chạy"; lượt "dùng như người thật" (32 phút, 107 lượt công cụ, khoảng 82 nghìn ký tự, 15 lượt gọi model) — bài 38 "Quyết định nhỏ hơn" và "Chi tiết để tra"; thẻ chọn tên ảnh đã sửa 11:26 — bài 26 "Giới hạn đã biết", bài 35 "Đã so"; bản các bài lúc 12:14–12:19 23/11 [chép từ bài]. 49 / 3: người gom tự chạy lệnh đếm 12:25 23/11 trên main `0367e775` [tự chạy lệnh đếm]. Bảng từ 108 thành 113 hàng.
- Lượt hai (12:55 23/11/2026): lần chạy đủ 12:05–12:23 (86 file, 4 bỏ, 82 chạy, 2.228 ca, 0 file đỏ; 10 ca thêm ở ba file; bản gộp 12:34 sau lượt này) — bài 38 "Ý chính" và "Chi tiết để tra" (bản đã áp biên bản 12:45 23/11); 09:41–09:59 nay là "lần trước đó" theo cùng bài [chép từ bài]. 49 / 5: người gom tự chạy lệnh đếm 12:51 23/11 trên main `5138622d` [tự chạy lệnh đếm]. Thẻ chọn tên ảnh: bài 35 "Đã so" hàng ảnh chụp tự động [chép]. Số hàng không đổi.
- Đợt đầu chiều 23/11/2026 (14:34, người gom phụ lục): 12 ⇒ 0 trên 20, câu Đà Nẵng 10 ⇒ 0, "dưới khoảng 14 %", định nghĩa "được trả lời bằng kho" — bài 16 "Đã so" khối tỉnh khác (bảng "Mở ↔ tắt", "Vấn đề thật", "Đọc bảng"); 1 trên 40 (năm lượt), 3 trên 10, 2 trên 10 · 3 trên 5 — bài 16 "Đã so" "Vấn đề thật" và "Giới hạn đã biết"; 1.233 ⇒ 2.311 — bài 16 "Cấu hình đang chạy"; 113 trên 120, 39 trên 40 — bài 16 thân bài và bài 22 "Chi tiết để tra"; 12 ⇒ 1, 8 trên 20, nhãn "cách nhóm đang hiểu" — bài 21 "Đã so" dòng 8 và bài 16 câu dưới bảng ô (bản 14:17 23/11, đã áp biên bản kiểm độc lập) [chép từ bài]. 50 / 5: người gom tự chạy lệnh đếm 14:24 23/11 trên cây chính (main `6089f8bd`) [tự chạy lệnh đếm]. Bảng từ 113 thành 118 hàng.
- Lượt hai (14:43 23/11/2026, người gom phụ lục): 97 bài, 208, 141 — bài 5 "Đã so" bảng ba vòng xoay; 400 ngày, 0, 0, ngày giả — bài 5 "Giới hạn đã biết" gạch thẻ "Hôm nay ở Huế"; 88 file lúc 13:52, hai file mới, chưa lượt chạy đủ nào có hai file — bài 38 "Chi tiết để tra" (lượt chạy đủ mới nhất vẫn 86 file trong bảng, 82 chạy) [chép từ bài]. Bảng 118 ⇒ 120 hàng.

</details>
