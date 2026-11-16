# Chatbot Huế chạy thế nào — dòng chảy dữ liệu

Cập nhật 21:40 15/11/2026 (tối 15/11: tải trang = cuộc trò chuyện mới; khung nguồn hiện đoạn trích sạch; bỏ khối đánh giá; hỏi bằng ảnh luồng mới — đính kèm, bấm Hỏi mới xử lý, một tên thì trả lời luôn; sửa lịch có thêm dòng báo; ghi chú ăn Tây Hồ + Hải Vân tối, ảnh Hải Vân; sổ vết debug chỉ ở máy local. Trước 18:23 15/11/2026 — viết lại theo trạng thái cuối phiên chiều 15/11: lịch 41 điểm; khối Nơi ở chỉ hiện khi người dùng hỏi; sửa lịch bằng lời thêm đổi hạng chỗ ở + đổi ngày đi; buổi để trống không hiện; quán ăn trong lịch; ảnh + thẻ khách sạn dưới câu trả lời; câu hỏi nối tiếp khi tra web; lúc chờ một dòng bước đang chạy; bỏ dòng báo cạnh nút gửi ảnh; log có mã bản code. Trước: 16:19 14/11/2026 — bản cũ xem trong lịch sử phiên bản, git). Tả bản **đang chạy**. Số đo (tốc độ, tiền, điểm) không ghi ở đây — xem bảng
"Số chính" và "Từ hay gặp" trong [README](README.md).

Hệ thống có hai phần: **chuẩn bị kho** (chạy một lần, mỗi khi kho đổi) và **trả lời** (mỗi câu hỏi).

```text
CHUẨN BỊ (một lần):  265 bài ─► cắt thành đoạn ─► mỗi đoạn: vector nghĩa + từ khoá ─► cất vào Qdrant (kèm "phiếu" ghi dấu từng bài)

TRẢ LỜI (mỗi câu):
  [cuộc đã có lịch "Lên kế hoạch"] ─► cùng lúc với phân loại: model đọc xem câu có phải yêu cầu sửa lịch ─► có (và không khẩn cấp) ⇒ code sửa lịch
  câu hỏi ─► phân loại (model, một lần gọi ngắn) ──┬─ xã giao ───────► model đáp ngắn, không tìm kho
                                                   ├─ ngoài phạm vi ─► câu từ chối cố định (không gọi thêm model)
                                                   └─ về Huế / khẩn cấp
                                                        │
              tìm 10 đoạn trong kho ◄───────────────────┘
                 │  (+ code tính sẵn ngày nếu câu có từ chỉ ngày)
                 ▼
              model đọc ngữ cảnh, viết câu trả lời ─ có thể nhờ công cụ: tìm thêm (≤ 2 lần) · dự báo thời tiết · đổi ngày
                 │
                 ▼
              code kiểm nguồn ─► hiện câu trả lời + dòng "Nguồn"
                 │
                 └─ nếu câu trả lời là "không đủ thông tin" (hoặc có dòng ý thiếu) ⇒ tra web một lần ⇒ mục riêng "Từ web (chưa kiểm)"
```

## Chuẩn bị kho

1. **Kho** là 265 bài Markdown tiếng Việt (5 chủ đề, 9.436 đoạn) đã được biên soạn và sửa qua nhiều đợt (14/11: thêm bài lưu trú, địa điểm, quán, món, lễ hội qua 6 lần ghi kho; 15/11: sửa 2 câu về năm Tây Sơn); câu trả lời của chatbot không đọc gì ngoài kho (trừ web, thời tiết — dưới); riêng lịch và trang Chỗ ở còn dùng hai bảng dữ liệu ngoài kho: bảng quán (có quán lấy từ bản đồ mở) và bảng lưu trú (danh mục Cục Du lịch Quốc gia).
2. **Cắt đoạn** theo cấu trúc bài: mỗi đoạn văn, mỗi mục danh sách, mỗi dòng bảng (kèm hàng tiêu đề) là một đoạn. Đoạn mang theo tên bài và đường tiêu đề
   (vd "Bún bò Huế > Quán nổi tiếng") để dễ tìm.
3. Mỗi đoạn được tính **vector nghĩa** (model e5-small chạy ngay trên máy, không tốn tiền) và **từ khoá** (BM25), rồi cất vào **Qdrant**.
4. Một **phiếu dựng** ghi dấu từng bài. Mỗi lần khởi động, chatbot so dấu với kho hiện tại; kho đã sửa mà chưa dựng lại ⇒ **chatbot từ chối chạy** (để không trả
   lời bằng dữ liệu cũ).

## Trả lời một câu hỏi

1. **Nhận câu hỏi** từ trang web (≤ 500 ký tự), đưa dấu tiếng Việt về một dạng chuẩn. Nếu đang trong một cuộc trò chuyện, kèm theo **3 câu hỏi trước** (chỉ câu hỏi,
   không kèm câu trả lời cũ). **Tải lại trang = cuộc trò chuyện mới** (từ tối 15/11): lúc trang nạp, máy chủ quên cuộc cũ cùng lúc màn hình trống — trước đó tải
   lại trang chỉ xoá màn hình, máy chủ vẫn nhớ 30 phút nên câu đầu sau khi tải lại bị hiểu như câu hỏi tiếp của cuộc cũ.
2. **Phân loại** — một lần gọi model ngắn xếp câu vào 4 loại. Câu khẩn cấp (bị cướp, tai nạn, ốm nặng…) đi đúng đường câu về Huế. Phân loại lỗi hoặc quá 10 giây
   ⇒ coi là câu về Huế. Để đỡ chờ, phần "về Huế" (bước 3–4) **chạy luôn cùng lúc** với phân loại; nếu hoá ra không phải câu về Huế thì bỏ phần đó, người dùng không
   thấy chữ nào của nó (đổi lại: câu không phải về Huế tốn thêm một ít tiền cho phần bị bỏ).
3. **Tìm** — câu hỏi được so với mọi đoạn theo nghĩa (lấy 30 đoạn gần nhất), chấm lại 30 đoạn đó theo từ trùng (BM25), gộp hai bảng xếp hạng (RRF) ⇒ giữ **10 đoạn đầu** làm ngữ cảnh.
   Câu có từ chỉ ngày ("hôm nay", "cuối tuần", "rằm", "Tết"…) ⇒ **code** tính sẵn hôm nay, các ngày được hỏi, đổi ngày âm ↔ dương (cả ngày âm nhắc trong 10 đoạn)
   và thêm thành một nguồn "Lịch hệ thống".
4. **Viết câu trả lời** — model đọc lời dặn + ngữ cảnh, viết tiếng Việt, mỗi ý ghi số nguồn. Thiếu bằng chứng ⇒ phải trả đúng câu "Tôi không tìm thấy đủ thông tin
   trong nguồn dữ liệu để trả lời câu hỏi này." Trong lúc viết, model được nhờ **công cụ**: tìm thêm trong kho bằng câu tìm nó tự đặt (tối đa 2 lần), lấy dự báo thời
   tiết Huế, đổi một ngày chưa có trong nguồn "Lịch hệ thống". Mọi con số ngày / thời tiết do code tính, model chỉ chép.
   **Câu hỏi nhiều ý (từ 14/11):** code đếm được ≥ 2 vế hỏi (tách theo dấu phẩy / chấm phẩy / chấm hỏi, và "và / còn / với" khi cả hai phần có từ hỏi) ⇒ model trả lời
   ý nào có bằng chứng, ý thiếu ghi đúng một dòng "Tư liệu chưa có thông tin về: …" (trước: thiếu một ý là từ chối cả câu). Chỉ còn dòng ý thiếu ⇒ code đổi về câu
   từ chối chuẩn. Câu đếm được một vế ⇒ như cũ.
5. **Hiện dần + kiểm** — trong lúc chờ, trang hiện **một dòng** báo bước đang chạy (đang hiểu câu hỏi, đang tìm…, theo sự kiện thật của máy chủ) và ba chấm; chữ trả lời đầu tiên hiện thì dòng đó mất (trong lúc model còn viết, phía trên chữ chỉ còn một dòng "đang viết câu trả lời…" tới khi xong), và sau khi xong không để lại danh sách bước nào (từ 15/11, bạn yêu cầu). Chữ hiện dần trong lúc model viết. Viết xong, **code kiểm nguồn**: mỗi số nguồn phải trỏ tới đoạn có thật. Không qua ⇒ trang rút
   lại chữ và báo lỗi (rất hiếm — chưa gặp trong các lượt đo). Qua ⇒ hiện dòng **"Nguồn: tên bài · tên bài"**, bấm vào xem đoạn gốc hoặc cả bài; đoạn gốc hiện **sạch** (từ tối 15/11: in đậm, gạch đầu dòng, bảng thật — trước đó lộ ký hiệu thô của bài; các dòng của cùng một bảng được ghép lại thành một bảng; không tạo link nào trong đoạn trích). Câu trả lời trích bài về vé, địa điểm
   tham quan, lễ hội hoặc lưu trú có thêm dòng "thông tin có thể đã thay đổi". **Ảnh dưới câu trả lời:** chỉ bài về **một nơi / một món** có ảnh "chắc". Mọi nguồn được trích thuộc một bài như vậy ⇒ một ảnh (từ 14/11, không cần nhắc tên, không có chữ dưới ảnh). Từ 15/11: tên món / nơi được nhắc trong chữ trả lời hoặc trong câu hỏi, và bài đó được trích
   ⇒ tối đa 3 ảnh (từ 2 ảnh trở lên có tên nơi dưới mỗi ảnh); câu trả lời **trích bài lưu trú** và nhắc tên một cơ sở trong danh mục (so theo phần chính của tên, bỏ chữ loại hình ở đầu) ⇒ **thẻ khách sạn** (tối đa 3: tên, hạng, link). Đều do code quyết; không ảnh khi từ chối, có mục web hay có lịch.
6. **Tra web (chỉ khi kho không có)** — câu về Huế mà câu trả lời là "không đủ thông tin", hoặc có dòng ý thiếu ⇒ code gửi một câu tới Serper (máy tìm Google) **một lần**, model viết một
   mục riêng **"Từ web (chưa kiểm)"** ghi link; câu nhiều ý ⇒ model chỉ viết mục web cho vế thiếu (code chọn vế từ chữ người dùng). **Câu gửi đi tìm:** lượt đầu của cuộc ⇒ đúng câu người dùng gõ. **Câu hỏi nối tiếp (bật chiều 15/11, bạn chọn):** lượt đã có câu hỏi trước **và** model đã tự tìm kho ⇒ gửi câu tìm kho cuối cùng model viết (câu đó thường đã ghép tên nơi của lượt trước — lượt đo 8 / 8 lần có đủ tên; code không kiểm điều này. Trước đây gửi nguyên câu cụt kiểu "mở cửa mấy giờ" nên mục web lạc sang nơi khác; model không tự tìm kho lần nào ⇒ vẫn gửi câu gõ như cũ); riêng lượt nhiều ý vẫn gửi câu gõ. Câu nào cũng qua bộ lọc bỏ email / số điện thoại, cắt độ dài. Code chặn trước khi hiện: link không có trong kết quả tìm, mã trang web thô, số tiền không có trong đoạn trích, giờ / ngày ở câu cần tin "ngay lúc này" (vd giá hôm nay); câu về bão, lũ ⇒
   câu cố định "xem trung tâm dự báo / chính quyền, khẩn cấp gọi 112".
7. **Ghi số đo** — mỗi câu ghi đúng một dòng log: loại câu, thời gian từng bước, số token, tiền, và (từ 15/11) **mã bản code đang chạy** để đếm đúng lượt của một bản. **Không ghi chữ câu hỏi hay câu trả lời.**
   **Sổ vết debug (tối 15/11, chỉ ở máy local):** mặc định **tắt**; người vận hành bật bằng biến môi trường `HUE_SO_VET=true` ⇒ mỗi lượt ghi thêm một bản ghi **có nội dung**
   (câu hỏi, từng lần tìm kho, từng lần gọi model, câu trả lời, phần web, sửa lịch, lỗi) vào `data/debug_trace/<ngày>.jsonl` trên chính máy đó để tìm lỗi khi thử; dòng số đo ở
   trên không đổi. Bản đưa lên mạng **không bật** (chữ người dùng sẽ nằm trên đĩa).

## Ví dụ trọn vẹn (câu tự viết)

Người dùng gõ: *"Cuối tuần này mình ở Huế, nên ăn bún bò ở đâu?"*

| Bước | Chuyện gì xảy ra |
|---|---|
| Phân loại | model xếp "về Huế"; cùng lúc phần tìm + viết đã bắt đầu chạy |
| Tìm | 10 đoạn gần nhất — chủ yếu từ bài món bún bò và các bài quán bún bò trong kho |
| Lịch | có "cuối tuần này" ⇒ code thêm nguồn "Lịch hệ thống": hôm nay là thứ mấy, các ngày trong tuần này (dương + âm) |
| Viết | model kể vài quán có trong kho kèm địa chỉ / giờ mở như bài ghi, mỗi ý một số nguồn; nhắc ngày cuối tuần đúng như nguồn lịch; không thêm quán ngoài kho |
| Kiểm + hiện | số nguồn hợp lệ ⇒ dòng "Nguồn: …" gồm các bài quán (bài quán ăn không kèm dòng "thông tin có thể đã thay đổi" — dòng đó chỉ cho bài vé, địa điểm, lễ hội, lưu trú) |
| Không tra web | vì kho đã trả lời được |
| Log | một dòng: loại "về Huế", 1 lần phân loại + 1 lần viết, có nguồn "Lịch hệ thống" (code tính sẵn), thời gian, tiền — không có chữ câu hỏi |

Hỏi tiếp *"Còn chè thì nên ăn ở đâu?"* ⇒ câu hỏi trước được gửi kèm, nên model hiểu vẫn là chuyện ăn uống ở Huế dịp cuối tuần; nếu kho không có và phải tra web, mà model đã tự tìm kho ở lượt đó, thì câu đem đi tìm là câu tìm model viết (thường đã đủ chủ thể), không phải câu cụt (bước 6). Nhưng *"Quán thứ hai mở
mấy giờ?"* thì **chưa hiểu được**: chatbot không nhớ câu trả lời trước nên không biết "quán thứ hai" là quán nào (giới hạn đã chọn — nhớ cả câu trả lời từng
làm lọt câu sai ở lượt đo).

## Các đường khác

| Người dùng làm gì | Đường đi |
|---|---|
| Chào / cảm ơn / hỏi chatbot là ai | phân loại "xã giao" ⇒ model đáp ngắn, không tìm kho, không nguồn |
| Hỏi chuyện ngoài Huế (code, giá vàng, nơi khác…) | phân loại "ngoài phạm vi" ⇒ câu từ chối cố định + vài câu gợi ý hỏi được |
| Điền biểu mẫu "Lên kế hoạch" (bản 2, từ 14/11) | **không** phân loại; biểu mẫu: ai đi · bao lâu, ngày đi · kiểu đi · thích gì · hạng chỗ ở (không bắt buộc); **code xếp** từ bảng **41 điểm** (15/11 thêm 7 nơi) theo chuỗi luật (an toàn nhóm có trẻ em / người lớn tuổi ⇒ giờ mở cửa, mùa ⇒ cụm gần ⇒ mưa theo dự báo — chỉ đổi điểm khi khả năng mưa ≥ 60 % **và** lượng mưa ≥ 6 mm ⇒ sở thích ⇒ kiểu đi) với quỹ phút, giờ gợi ý, "khoảng N phút đi" giữa hai điểm; khung hiện ngay, model chỉ viết mỗi điểm một câu tả từ một đoạn kho chọn sẵn (câu trượt kiểm, kể cả câu chỉ có số nguồn ⇒ code thay câu dự phòng); ảnh 40 / 41 điểm; link Google Maps do code dựng; nút tải lịch `.ics` dựng trong trình duyệt (cần ngày đi). **Ăn uống gợi ý:** mỗi bữa code chọn ≤ 2 quán trong 2 km quanh điểm (quán có bài kho trước; quán từ bản đồ mở ghi "chưa kiểm"); nơi không có quán gần mà kho có nói ⇒ một câu ghi chú theo kho, chỉ ở đúng bữa kho nói tới (Bạch Mã: bữa trưa · thác Nhị Hồ: bữa tối · đầm Lập An: trưa và tối · đèo Hải Vân: bữa trưa). **Nơi ở gợi ý chỉ hiện khi người dùng hỏi (từ chiều 15/11, bạn yêu cầu):** đã chọn hạng sao ở biểu mẫu hoặc nói hạng bằng lời ⇒ thẻ khu + ≤ 5 cơ sở của hạng đó + link tìm phòng, không giá (ca hiếm, chưa đếm: khu được chọn không có cơ sở hạng đó ⇒ ở lịch từ biểu mẫu code đưa cơ sở hạng khác mà không báo); chưa hỏi ⇒ chỉ một dòng link sang trang Chỗ ở, kèm gợi ý nhắn trợ lý hạng sao muốn ở (lịch 1 ngày: không có gì). **Buổi để trống không hiện** thành mục (từ chiều 15/11); nhóm có trẻ em / người lớn tuổi có một dòng "không xếp buổi tối" ở phần ghi chú. Chưa xếp ⇒ trang hiện **lịch mẫu "Ví dụ"** do chính bộ xếp dựng, không gọi model. Bản đồ cả lịch trình chưa bật |
| Nhắn sửa lịch khi cuộc đã có lịch (từ 14/11) | một lần gọi model chỉ để **hiểu ý** ⇒ danh sách hành động có tên (bỏ / thêm / thay / dời buổi / đổi số ngày / đổi kiểu, sở thích, trẻ em, người lớn tuổi / **đổi hạng chỗ ở** / **đổi ngày đi** — hai hành động sau thêm chiều 15/11; gửi ≤ 3, áp ≤ 2), chạy **song song** với phân loại; phân loại ra khẩn cấp ⇒ khẩn cấp thắng, đi đường thường. **Code** khớp tên điểm, xếp lại giữ chỗ các điểm không chạm, kiểm luật; khối đầu lịch "Đã đổi / Không đổi được / Chưa làm" do code viết (từ tối 15/11: xin đổi kiểu đi / sở thích / trẻ em… mà không đổi được gì ⇒ có dòng báo thay vì im lặng; đổi được ⇒ thêm dòng "Lịch xếp lại theo lựa chọn mới: …" nêu điểm bớt / thêm — quá 6 tên thì chỉ nêu số — hoặc "Các điểm trong lịch giữ nguyên chỗ"); "thay" không nói thay bằng gì ⇒ thẻ chọn ≤ 3 điểm. Đổi số ngày chỉ nhận khi câu có số ngày mới kèm chữ chỉ ngày, hoặc nói tương đối ("thêm một ngày", "bỏ ngày cuối"). **Đổi hạng chỗ ở:** người dùng phải nêu hạng (1 sao / đạt chuẩn · 2–3 sao · 4–5 sao); "rẻ hơn / sang hơn" ⇒ code hỏi lại hạng; lịch chưa có khối Nơi ở mà nói hạng ⇒ khối bật ở hạng đó. **Đổi ngày đi:** model chỉ nhận ra ý, **ngày do code đọc từ chính chữ người dùng** (dd/mm, "ngày d tháng m", hôm nay, mai, ngày kia, thứ…, cuối tuần; "tuần sau" chỉ khi đi kèm thứ hoặc cuối tuần); không đọc được đúng một ngày, ngày âm, hay chữ giống ngày (phân số, số thứ tự, tên có chữ "Mai") ⇒ "chưa rõ ngày", không đổi; đổi được ⇒ thử giữ chỗ mọi điểm, phạm luật thì xếp lại, câu báo in ngày + thứ. Câu không phải câu sửa ⇒ đường thường |
| Hỏi kèm ảnh (luồng mới tối 15/11) | bấm **dấu cộng trong ô nhập** hoặc **dán ảnh** ⇒ ảnh nằm trong ô như tệp đính kèm, **chưa gửi gì**; gõ câu (hoặc để trống) rồi bấm Hỏi ⇒ ảnh được thu nhỏ, gửi model kèm danh sách 42 điểm / món dễ nhận ra bằng ảnh (lập từ kho; model chỉ được chọn tên trong danh sách). Model đưa **đúng một tên** ⇒ code ghép tên vào câu đã gõ và hỏi luôn như câu thường (ô rỗng ⇒ "Giới thiệu về <tên>"); đầu câu trả lời có dòng "Mình đoán trong ảnh là <tên> — có thể sai" + nút gõ lại tên. Đưa **2–3 tên** ⇒ người dùng bấm đúng tên rồi mới trả lời. Không nhận ra / lỗi ⇒ lời báo, giữ chữ đã gõ. Model viết câu trả lời **không nhìn ảnh** — chỉ nhận tên, trả lời từ kho có nguồn. Tải lại trang / cuộc mới ⇒ ảnh đính kèm bị gỡ. Trang Giới thiệu nói ảnh gửi tới đâu, không lưu |
| Đọc "Khám phá", trang "Chỗ ở", ô thời tiết trang chủ | đọc thẳng bài kho / bảng lưu trú / dự báo, **không gọi model**; **262 / 265** bài Khám phá có ảnh (2 bài quán thêm 16/11 có ảnh từ tối 16/11) (3 bài để trống theo quyết định của bạn 15/11); trang Chỗ ở: 136 cơ sở theo khu, 67 có ảnh; giao diện **không hiện chữ ghi công ảnh** (bạn yêu cầu; nguồn từng ảnh giữ trong bảng dữ liệu); thẻ "Thông tin nhanh" bên bài |
| Bấm "Cuộc trò chuyện mới", "Dừng" | xoá nhớ cuộc hiện tại (và gỡ ảnh đang đính kèm) · máy chủ huỷ lần gọi model đang chạy. Khối "Câu trả lời có hữu ích không?" + nút 👍 / 👎 **đã gỡ khỏi giao diện** tối 15/11 (bạn yêu cầu); đường nhận đánh giá ở máy chủ còn, bản công khai muốn thì bật lại |

## Code quyết, model không quyết

Model hay tính sai hoặc tự thêm con số, nguồn, giờ giấc (các lần thử chỉ dặn model "đừng làm" đều không đủ) ⇒ những việc này do code: câu từ chối cố định · kiểm số nguồn · tính ngày, đổi âm ↔ dương · số dự báo thời tiết · xếp lịch, áp lệnh sửa lịch, **đọc ngày đi mới từ chữ người dùng**, chọn nơi ở và quán gợi ý, quyết có hiện khối Nơi ở hay không · đếm vế câu nhiều ý, đổi câu chỉ còn ý thiếu về câu từ chối · chọn ảnh và thẻ khách sạn dưới câu trả lời · chọn câu đem đi tra web ·
chặn link / số tiền lạ ở mục web · câu bão lũ · giới hạn số lần tìm. Model chỉ phân loại câu, chọn khi nào nhờ công cụ, và diễn đạt.

## Dữ liệu người dùng gửi đi đâu

| Đi tới | Gửi gì | Khi nào |
|---|---|---|
| OpenAI (model `gpt-6-luna`) | câu hỏi + tối đa 3 câu hỏi trước + đoạn kho + nguồn lịch / thời tiết; ảnh đã thu nhỏ (khi hỏi bằng ảnh) | mọi câu cần model |
| Serper (tìm Google) | lượt đầu: chữ câu hỏi; lượt hỏi tiếp mà model đã tìm kho (từ chiều 15/11): câu tìm model viết — có thể mang tên nơi và chi tiết của câu hỏi trước; đều đã bỏ email / số điện thoại | chỉ khi câu về Huế mà kho không có |
| Open-Meteo (thời tiết) | **chỉ** toạ độ Huế + số ngày — không có chữ người dùng | câu hỏi thời tiết, ô thời tiết trang chủ |
| Google Maps, trang tìm phòng bên ngoài | không gì từ máy chủ — chỉ khi người dùng tự bấm link (link do code dựng) | lịch trình, quán gợi ý, thẻ khách sạn, trang Chỗ ở |
| Máy chủ (RAM) | 3 câu hỏi gần nhất của cuộc trò chuyện + (từ 14/11) lịch mới nhất của cuộc — chỉ dữ liệu code dựng (khung, ngày đi, điểm đã bỏ, câu tả đã kiểm), không chữ người dùng; xoá sau 30 phút không hỏi hoặc khi bấm "Cuộc trò chuyện mới"; ảnh **không** lưu | — |
| Trình duyệt (cookie) | một mã cuộc trò chuyện ngẫu nhiên, 30 phút, trang web không đọc được | — |
| Log của chatbot (file trên máy chủ) | số đo, loại câu, tiền, mã bản code — **không** chữ câu hỏi / câu trả lời, không IP; file xoay vòng (≤ 10 MB × 3) | mọi câu |
| Sổ vết debug (file trên máy local, **chỉ khi người vận hành bật**) | chữ câu hỏi, câu trả lời, câu tìm, đoạn kho đã dùng, chữ mục web — không cookie, không IP, không ảnh | mặc định tắt; bản công khai không bật |
| Log truy cập của máy chủ web | phép thử 15:04 11/11/2026: cấu hình log của chatbot (nạp lúc khởi động) **tắt** log truy cập mặc định của uvicorn ⇒ nhiều khả năng **không** in IP; chưa kiểm trên máy chủ thật đang chạy | — |

## Khi có lỗi, người dùng thấy gì

Model lỗi / mạng đứt giữa chừng ⇒ chữ đã hiện bị xoá, có lời báo tiếng Việt + nút "Thử lại" · kho chưa dựng lại sau khi sửa ⇒ chatbot không chạy (người vận hành dựng
lại) · Qdrant tắt ⇒ báo lỗi tạm thời · khi đưa lên mạng có giới hạn số lượt hỏi mỗi máy mỗi ngày ⇒ quá lượt nhận câu báo.

## Giới hạn chính (đang chạy)

- Câu khẩn cấp: phân loại nhận ra, nhưng trợ lý Huế thường từ chối (kho không có bài khẩn cấp) và không có số 112–115 — đo lại 14/11 trên main: từ chối 10 / 12, có số 0 / 12; giới hạn đã nhận (bạn quyết 12/11 không làm dòng số khẩn cấp).
- Chỉ một nhà cung cấp model, không dự phòng. Không đăng nhập. Chưa có câu hỏi của người dùng thật — mọi số đo trên câu tự viết / Golden.
- Kiểm nguồn chỉ kiểm **số nguồn có thật**, không kiểm câu chữ có đúng với nguồn — "có nguồn" chưa phải "đã kiểm nghĩa".
- Từ chối nhầm còn là lỗi nhiều nhất: đoạn chứa đáp án xếp hạng 11–30 (không lọt vào 10 đoạn đưa model), hoặc nằm ngoài cả 30 ứng viên (khoảng một nửa số ca) ⇒ model không thấy nên nói "không đủ thông tin".
- Câu xã giao chờ phân loại xong mới viết ⇒ có lúc chậm (cách chạy song song đã thử 10/11, chưa đạt — không áp dụng).
- Mục web có thể cũ / sai dù đã ghi "chưa kiểm"; với ý ngoài kho, mục web hay chỉ nói "chưa xác minh được".
- Câu hai ý mà code chỉ đếm được một vế (không dấu phẩy, một vế không có từ hỏi, kiểu "A hay B") ⇒ vẫn bị từ chối cả câu.
- Câu hỏi nối tiếp: mục web nay nói đúng nơi, nhưng nhiều mục vẫn bị bộ kiểm số thay bằng câu "chưa tra được"; chữ model viết (có chi tiết lượt trước) đi ra dịch vụ tìm — tên người dùng mới đo trên rất ít lượt, không có bộ lọc tên ⇒ xét lại trước khi đưa lên mạng.
- Đổi ngày đi bằng lời: luật nhận chữ giống ngày dựa trên danh sách từ nên có thể còn sót; "tuần sau" tính theo tuần lịch; câu báo luôn in ngày + thứ để người dùng thấy và sửa.
- Lịch: bữa ở làng nón Tây Hồ nay có ghi chú "chưa có gợi ý quán gần làng… nên ăn ở trung tâm" (không nêu tên quán — chưa có nguồn nào nêu quán tại làng), bữa tối sau đèo Hải Vân dùng ghi chú chỉ sang khu Lăng Cô; bữa còn trống nhiều nhất: vùng phá, một điện thờ thượng nguồn, một không gian nghệ thuật; ngày đi xa không có buổi tối và không có dòng giải thích (bạn chọn không thêm); 1 / 41 điểm chưa có ảnh.
- Hỏi kèm ảnh: model đưa **một tên mà sai** ⇒ trợ lý trả lời luôn về sai nơi, chỉ còn dòng "có thể sai" nhắc (đã gặp khi thử); cùng một ảnh, kết quả nhận ảnh có thể khác nhau giữa các lần; chưa có nút huỷ lúc "Đang xem ảnh…"; bản đang chạy không còn dòng báo cạnh nút — bản công khai cần dòng báo lại.
- Đang mở (chưa xong, chưa vào chatbot): lỗi "hỏi A ⇒ hỏi tiếp B ⇒ hỏi lại A thì A bị từ chối" trong cùng một cuộc; thử nhận ảnh bằng so ảnh với ảnh mẫu; mục web viết gọn hơn.

## Đọc chi tiết (báo cáo kỹ thuật)

Muốn hiểu từng khâu: đọc tiếp các file theo thứ tự trong [README](README.md). Dưới đây là báo cáo kỹ thuật của agent, cho khi cần kiểm sâu.


- Tìm + 10 đoạn ngữ cảnh: `report_agent/2026-10-25_phase_8_2_ap_dung/TONG_HOP.md` · các cách đã thử ở khâu tìm / trả lời: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`
- Chữ hiện dần, lượt đo cuối Phase 8: `report_agent/2026-10-31_streaming_spec/TONG_HOP.md`
- Trợ lý Phase 9 (thiết kế, từng bậc): `docs/superpowers/specs/2026-11-02-phase-9-design.md` · `report_agent/2026-11-02_phase_9_code/` · `report_agent/2026-11-08_phase_9_ban_13/TONG_HOP.md`
- Cổng du lịch + biểu mẫu: `report_agent/2026-11-06_giao_dien_cong/c_s3_q_f_implementation.md` · hỏi bằng ảnh: `report_agent/2026-11-05_phase_10_anh/`
- Chiều 15/11 (trong `report_agent/2026-11-12_ra_khoang_cach/`): bảng 41 điểm `e_diem_v9_implementation.md` · ba sửa giao diện `e_gd_3_sua_implementation.md` · buổi để trống `e_bo_buoi_trong_implementation.md` · ảnh bạn tự tìm `e_anh_ks_user_implementation.md`, `e_anh_kp_user_implementation.md` · khối Nơi ở chỉ khi hỏi `c_noi_o_khi_hoi_implementation.md` · đổi ngày đi `c_sua_ngay_di_implementation.md` · câu hỏi nối tiếp `b_web_noi_tiep_implementation.md`
- Tối 15/11 (cùng thư mục): tải trang = cuộc mới `c_f5_cuoc_moi_implementation.md` · khung nguồn + bỏ đánh giá `e_gd_nguon_danh_gia_implementation.md` · ảnh: `c_nut_anh_cong_implementation.md`, `c_anh_dinh_kem_implementation.md`, `e_anh_tra_loi_thang_implementation.md` · dòng báo sửa lịch `c_no_nho_sua_lich_implementation.md` · ghi chú ăn + ảnh Hải Vân `e_lich_ho_implementation.md` · sổ vết debug `e_so_vet_implementation.md`
- Ngày tính sẵn: `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md` · chạy thử bản Docker: `report_agent/2026-11-08_phase_9_ban_13/b_deploy_cuc_bo_implementation.md`
- Dựng lại kho / chạy máy: `guides/full_corpus_rag.md` · mọi phương án đã thử: [91_BAO_CAO_SO_SANH_PHUONG_AN.md](91_BAO_CAO_SO_SANH_PHUONG_AN.md)
