# Phụ lục F — Các con số chính trên một trang

*Cập nhật 17:11, ngày 22/11/2026 · khớp các bài lúc tối 22/11 (47 tính năng, kho 267 bài) · trước đó: gom từ các bài của giáo trình lúc đó; bài gốc đổi thì trang này phải gom lại.*

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

## 4. Trợ lý (harness), nhớ cuộc trò chuyện, xếp loại câu, công cụ

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 3 lần | số lần model được tự tìm kho mỗi lượt hỏi | cấu hình từ 14:47 22/11 (trước là 2) | 3, 21, 23 |
| 5 vòng (+1 mỗi công cụ ngoài tìm kho, trừ thời tiết) | trần vòng gọi model của một lượt; trần thực tế của lượt hỏi đáp hiện là 6 trở lên | cấu hình từ 14:47 22/11 (trước là 4) | 21 |
| 45 giây | hạn cho các vòng của trợ lý cộng lại; lần viết lại, lần chạy lại, lần viết mục web mỗi cái có 45 giây riêng | cấu hình, sau 14:47 22/11 | 6, 15, 21 |
| +1,17 điểm đủ ý; từ chối nhầm 12 ⇒ 4–6 trên 158 | khi mở cho trợ lý tự tìm thêm (lúc đó trần 2 lần) | gpt-6-luna, 18 câu cần nhiều nguồn và 158 câu (khoảng tin cậy +0,44 tới +2,00) | 3, 21 |
| 6 trên 6 | số lần nêu đúng cả hai ý kho có ở một tin 4 ý, sau bốn thay đổi khâu tìm mở cùng nhau; 0 màn hình lỗi (trước: 3 trên 6 lần ra "Thử lại") | một tin 4 ý, 6 lần, Claude, chiều 22/11 | 3, 16, 40 |
| 4 trên 60 câu | số câu cần công cụ mà cách đưa công cụ theo từ khoá bỏ sót | đếm 21/11 trên 310 câu của sổ ghi lượt hỏi | 3, 21 |
| 3 lượt, 30 phút, 500 cuộc | máy chủ nhớ 3 lượt gần nhất mỗi cuộc, hết hạn sau 30 phút, nhiều nhất 500 cuộc | cấu hình, sáng 22/11 | 6, 23, 35 |
| 4.000 ký tự | phần câu trả lời liền trước được gửi kèm (trước là 1.200) | cấu hình, bật 09:40 22/11 | 23 |
| 3 trên 3 · 3 trên 3 | trong cuộc đã lập lịch, nhờ "Bỏ quán đầu đi rồi viết lại danh sách": lịch không đổi · danh sách bỏ đúng quán đầu và đủ các quán còn lại (2 lần khớp đúng, 1 lần thêm một mục có nguồn); bên không nhớ: câu "không xác định được quán đầu" | 9 lượt thật, một chuỗi tin × 3, Claude Sonnet 5.5, 22/11; mở từ 16:08 22/11 | 23, 31 |
| 10 giây | hạn của bước xếp loại câu; quá hạn thì coi là "về Huế" | cấu hình, sáng 22/11 | 6, 22 |
| sớm hơn 1,37 giây | chữ đầu tới sớm hơn khi xếp loại câu chạy song song (khoảng tin cậy 0,34 tới 2,14) | gpt-6-luna, 20 cặp, 04–05/11; chưa đo lại với Claude | 6, 22, 34 |
| 9 câu từ chối nhầm bớt, 0 câu sai ngày | khi chương trình tính ngày thay model | gpt-6-luna, 09/11 | 1, 3, 24, 40 |
| 40 điểm, 1.560 cặp | bảng khoảng cách dựng sẵn; không gọi mạng lúc trả lời | cấu hình, trưa 22/11 | 24 |

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
| khoảng 13 % | dòng "Tư liệu chưa có thông tin về…" sai (kho có) | một phiên đọc tay 30 trong 119 dòng của ba lượt mốc; khoảng tin cậy 4–31 % | 40 |

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
| 16 trên 20 ⇒ 20 trên 20 | nghiệm thu câu mô tả: lần đầu trượt, sau khi chọn tay đoạn kho thì đạt | nghiệm thu lịch (lúc đó) | 29 |
| 136 cơ sở, tối đa 5 | cơ sở lưu trú (bản 6, 67 có ảnh) và số cơ sở gợi ý | cấu hình, trưa 22/11 | 30 |
| 467 quán; 2 quán mỗi bữa, 2 km | bảng quán (bản 2, 21/11); giới hạn mỗi bữa | cấu hình, trưa 22/11 | 30 |
| 9 trên 10 | bộ 10 chuỗi sửa lịch đạt (cả hai lần chạy) | đo 14–19/11, trước khi đổi sang Claude | 31, 40 |
| 90 % trong 15.360 cặp, 0 lỗi | đổi chỗ hai ngày làm được | đếm bằng chương trình | 31 |
| 5 / 6 · 2 / 6 · 0 / 6 | lệnh sửa lịch khó làm đúng ở mức suy luận cao / thấp / vừa | Claude Sonnet 5.5, 21/11 | 31, 33 |

## 8. Model viết, thời gian chờ, tiền

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 9 loại lời gọi | số việc dùng chung một model viết; đổi model là đổi tất cả | hồ sơ đếm, trưa 22/11 | 33 |
| khoảng 3 lần · 20 lần | Claude viết dài hơn khoảng ba lần; đắt hơn 20 lần mỗi token | Claude Sonnet 5.5 so với gpt-6-luna | 33, 34 |
| 2 / 10 USD · 0,10 / 0,50 USD | giá mỗi 1 triệu token chữ vào / chữ ra: Claude Sonnet 5.5 · gpt-6-luna | cấu hình, sáng 22/11 | 15 |
| khoảng 0,3 giây | mức cao chậm hơn mức vừa ở câu hỏi một lượt (bốn mức ngang nhau về chất lượng) | Claude, 66 câu | 33, 34 |
| 6 ⇒ 0 trên 29 | số câu chạm trần vòng trước và sau khi sửa lớp nối Claude (trước đó Claude xin công cụ mãi: 0 trên 8 lần viết được, ở mỗi mức) | Claude, khi đổi model | 33 |
| 3,7 giây (model viết 3,6 giây) | thời gian cả câu ở ví dụ chính | ví dụ chính, lượt chạy thật | 6 |
| khoảng 13 giây | thời gian chờ ở lượt hỏi đáp đứng giữa; một phần ba số lượt quá 15 giây | Claude mức cao, 49 lượt của người dùng mô phỏng, 21/11 | 34, 40 |
| 9,7 giây (72 %) · 3,1 giây (25 %) · 3 % | phần của lần viết cuối · các vòng công cụ (khoảng 2,2 giây một vòng) · phần của chương trình | như trên | 34 |
| 6,9 giây; 95 % dưới 13,1 giây | thời gian cả câu ở lượt đứng giữa, 0 màn hình lỗi | 41 tin phần lớn ngắn qua trình duyệt, lượt kiểm chốt trưa 22/11, lúc máy rảnh | 34, 40 |
| 25–34 giây | thời gian chờ của tin dài nhiều ý (trước khoảng 20 giây), suốt lúc đó chỉ một dòng trạng thái rồi cả câu trả lời; lượt phải viết lại một lần lâu thêm khoảng 10 giây (tới 25–37 giây; ca này chưa nhìn trên trình duyệt) | một tin 4 ý, 6 lần, từ 14:47 22/11; trên trình duyệt 22/11 tin gia đình bốn ý 29,5 giây | 23, 34, 40 |
| 17–24 giây | lượt nhờ "viết lại danh sách" (trợ lý tra kho lại và viết lại từng mục, không chỉ xoá một dòng); bên không nhớ câu trả lời: 10–12 giây cho một câu "không xác định được" | trên trình duyệt 22/11: 17,3 và 24,1 giây; lượt thật: 19–20 giây, khoảng 0,13–0,17 USD; Claude | 23 |
| 0,018 USD | tiền ví dụ chính (0,0178 USD) | Claude, lượt ví dụ chính 21/11 (bài 2, 6) | 2, 4, 6, 34 |
| 0,0004 USD · 0,0146 USD | tiền một câu trả lời có nguồn: gpt-6-luna · Claude mức cao (gấp khoảng 37 lần) (trung bình trên 66 câu tính điểm của 85 câu đầu bộ mẫu, không lọc theo loại câu) | 66 câu, 21/11 | 33, 34 |
| khoảng 0,0007 USD · khoảng 0,018 USD | tiền một câu ví dụ: gpt-6-luna · Claude (khoảng 25 lần) | câu ví dụ chạy thẳng qua code sản phẩm (không qua máy chủ), 21/11; mức suy luận: báo cáo gốc không ghi, hướng dẫn đổi model ghi "mức thấp" | 33 |
| đúng 4,97 ↔ 4,94 · đủ ý 4,83 ↔ 4,88 | điểm thang 1–5 của gpt-6-luna ↔ Claude; trọng tâm Claude thấp hơn rõ | 66 câu tính điểm, 21/11 | 33 |
| 24 giờ, 500 câu, khoảng 0,1 giây | bộ nhớ câu trả lời: hạn, trần, thời gian trả lại câu đã nhớ | cấu hình (bật từ 20/11) | 6, 34 |

## 9. Máy móc, bảo mật, bộ test, cách làm

| Con số | Đếm cái gì | Đo trên gì, model nào, ngày nào | Bài |
|---|---|---|---|
| 47 mở, 3 tắt | số tính năng đang mở / đang tắt (lúc 10:25 là 42 mở; từ 14:47 thêm ba; từ 15:42 thêm một; từ 16:08 thêm việc nhớ câu trả lời liền trước cả trong cuộc đã lập lịch) | đếm 16:13 22/11 (đếm lại 16:57: 47) | 4, 40, phụ lục B |
| 5 khối · 6 bước · 4 thứ gửi ra ngoài | khối của hệ thống; bước của một câu hỏi; thứ rời máy (lời gọi model, ảnh, dự báo thời tiết, câu tra web) | kiến trúc, sáng 22/11 | 6 |
| khoảng 18 đường gọi | số đường gọi giữa giao diện và máy chủ; 3 đường gọi model | chương trình, trưa 22/11 | 35 |
| khoảng 14 giây · 34 giây | lệnh bật ra "SẴN SÀNG" khi mọi thứ đủ · khi bắt đầu từ lúc Qdrant đang tắt | 14 giây: bốn ca chạy thật ở cổng tạm; 34 giây: lượt kiểm chốt trưa 22/11 | 36, 40 |
| 76 file, 2.060 ca | lần chạy đủ mới nhất của bộ test | lượt kiểm chốt trưa 22/11 | 38 |
| 75 file, 1.961 ca đạt, 4 file bỏ | lần chạy cuối buổi sáng; 4 file bỏ vì cần khoá OpenAI | sáng 22/11 | 38 |
| khoảng 16 phút · khoảng 4,4 GB | cả bộ test chạy từng file một · bộ nhớ khi chạy cả bộ một lượt | hướng dẫn vận hành | 38 |
| 5 phiên · 11 skill | số phiên làm việc (điều phối, hai thực thi, đo, giảng) · số file skill | cách làm lúc viết, trưa 22/11 | 39 |

<details><summary>Nguồn (để giữ trang đúng — anh không cần đọc)</summary>

Gom từ mục "Ý chính", bảng "Cấu hình đang chạy", bảng "Các con số chính của đường hỏi đáp" (bài 19), các bảng "Người dùng làm được" và "Chỗ yếu" (bài 40), cùng vài dòng "Chi tiết để tra" có số (bài 12, 34, 36, 40) của các bài 1–40 trong cùng thư mục, bản lúc 15:22 ngày 22/11/2026; không thêm sự thật mới. Gom lại 17:00 22/11/2026 theo các bài vừa sửa: số tính năng (bài 4, 40), hai dòng tiền (bài 33 "Chi tiết để tra": câu ví dụ chạy thẳng qua code sản phẩm; bài 34 bảng tiền: "không lọc theo loại câu"), "2 trên 44" (bài 22 quyết định về luật nghiêng về Huế, "Cái giá" và "Cách khác"), tin dài trên trình duyệt (bài 34 bảng "Nếu… thì sao"), hai dòng mới về cuộc đã lập lịch (bài 23 "Đã so" dòng 12 và "Giới hạn đã biết"). Lệnh đếm tính năng chạy lại 16:57 22/11 ra `47` [đã chạy]. Mỗi dòng giữ điều kiện bài gốc ghi; dòng nào bài gốc không ghi model thì không ghi. Chỗ hai bài ghi khác nhau về cùng một con số ghi ở báo cáo gom [riêng tư].

</details>
