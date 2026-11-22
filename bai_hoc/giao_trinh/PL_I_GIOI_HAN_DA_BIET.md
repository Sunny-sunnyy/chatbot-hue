# Phụ lục I — Mọi giới hạn đã biết trên một trang

*Cập nhật 18:13, ngày 22/11/2026 · khớp các bài lúc tối 22/11 (48 tính năng, kho 267 bài): năm giới hạn của thẻ nơi (17:15) · trước đó: giới hạn mới của việc nhớ trong cuộc đã lập lịch, của dòng trạng thái ở tin dài, của công cụ liệt kê bài, trang Giới thiệu · trước đó: phân xử chỗ lệch giữa các bài; giữ chữ tới khi kiểm (15:42); rào bỏ / thay của lịch; gom từ các bài của giáo trình lúc đó; bài gốc đổi thì trang này phải gom lại.*

**Giới hạn đã biết khác với thứ cố ý không làm (bài 4).** Giới hạn đã biết là chỗ hệ thống làm chưa tốt trong chính phạm vi của nó: kho có mà tìm không ra, chờ lâu, bước kiểm chưa kiểm nghĩa. Thứ cố ý không làm là một ranh giới đã được chọn, không phải một lỗi còn nợ: câu gõ không dấu, tiếng Anh, tình huống khẩn cấp, giá phòng, đặt chỗ thay người dùng. Trang này liệt kê loại thứ nhất, nhóm theo chặng; loại thứ hai nằm ở bảng nhỏ riêng cuối trang.

**Cách dùng trang này.** Mỗi dòng gom một gạch của mục "Giới hạn đã biết" ở bài 1–40; giới hạn nhiều bài cùng nêu thì gộp một dòng, cột Bài ghi mọi bài. Cột "Người dùng gặp gì" ghi "giới hạn của phép đo" khi người dùng không thấy trực tiếp, chỉ con số của nhóm có thể lạc quan hơn thực tế. Lời trong ngoặc kép chép từ bài gốc.

## Những giới hạn chạy xuyên cả hệ thống

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Bước kiểm chỉ kiểm số nguồn có thật, chưa kiểm đoạn được trích có nói đúng điều câu trả lời viết. | — | model có thể viết sai nghĩa kèm một số nguồn có thật | 15, 16, 21, 40 |
| Một hãng model tại một thời điểm, không có dự phòng tự động. | — | hãng chậm hay lỗi thì hệ thống chậm hay lỗi theo | 6, 15, 33 |
| Với Claude, chữ hiện ra một lần sau khi model viết xong, không hiện dần (bộ khoá đang dùng không có quyền nhận chữ dần). | lượt đứng giữa khoảng 13 giây, một phần ba số lượt quá 15 giây | có lượt phần chữ trống hơn 15 giây, chỉ có dòng trạng thái | 5, 15, 33, 34 |
| Cuộc trò chuyện, lịch đang giữ và câu trả lời đã nhớ 24 giờ chỉ nằm trong bộ nhớ của máy chủ. | cuộc và lịch hết sau 30 phút; câu trả lời nhớ 24 giờ | khởi động lại máy chủ, tải lại trang hay quá 30 phút là mất, không có lời báo; màn hình vẫn hiện thẻ lịch cũ tới khi tải lại | 6, 23, 27, 35, 36 |
| Một máy, một bản máy chủ, chưa đưa lên mạng; các chốt để đưa lên mạng đang tắt, chưa thử trên bản thật. | nhiều người hỏi cùng lúc mới đo một lần (27/10) | — | 6, 37, 40 |
| Đường báo tình trạng chỉ biết tình trạng lúc bật, và không gọi ra ngoài. | đã thử: Qdrant ngừng giữa chừng thì nó vẫn báo đủ (trả "ok") | có thể báo đủ trong khi hãng model đang từ chối mọi lần gọi | 6, 35 |
| Mới bốn tình huống hỏng được thử thật, mỗi ca một lượt; các dòng "hỏng thì thấy gì" còn lại đọc từ chương trình. | 4 ca (22/11) | — (giới hạn của phép đo) | 6, 40 |

## Chặng 1 — Bức tranh

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Chưa thử trên điện thoại thật, mới thử ở bề rộng màn hình điện thoại trên máy tính; chưa có ứng dụng điện thoại riêng. | — | trang web chạy được trong trình duyệt của điện thoại; chưa ai xác nhận trên máy thật | 5, 40 |
| Số [n] không hiện trong chữ; dòng "Nguồn:" chỉ cho biết cả câu trả lời dựa vào những bài nào (lựa chọn của chủ dự án về giao diện). | — | không thấy ý nào đến từ nguồn nào | 5, 16 |
| Trang Bản đồ chỉ có điểm tham quan. | — | chưa có quán ăn hay chỗ ở trên trang Bản đồ | 5 |
| Số lượt tải PowerPoint chỉ bị giới hạn (30 mỗi địa chỉ mỗi ngày) khi bộ giới hạn lượt được bật; mặc định tắt, nên trên máy phát triển chưa giới hạn. | 30 mỗi ngày khi bật | — (phải bật trước khi đưa lên mạng) | 5, 30, 37 |

## Chặng 2 — Chuẩn bị kho

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Kho thiếu ở vài mảng người dùng hỏi thật: chỗ đậu ô tô, quy định chụp ảnh ở chùa và lăng (bài leo bậc vào kho sáng 22/11, bài đường đi Hội An chiều 22/11). | lượt đo trợ lý 21/11 chỉ ra 4 thứ, còn 2 | nhận câu từ chối, rồi mục "Từ web (chưa kiểm)" | 7, 40 |
| Kho cũ dần: giá và giờ đổi theo thời gian; phần lớn mức giá không ghi ngày. | — | câu trích bài vé, địa điểm, lễ hội, lưu trú kèm dòng "Giờ mở cửa, giá vé, lịch lễ hội có thể đã thay đổi…"; giá coi là tương đối | 7, 16 |
| Dòng "có thể đã thay đổi" chỉ áp cho bốn nhóm bài (vé, địa điểm, lễ hội, lưu trú). | 4 nhóm | câu về món ăn, quán không có dòng này | 16 |
| Kho còn vài con số các nguồn nói khác nhau, giữ nguyên và ghi vào một danh sách riêng. | — | — | 7 |
| Kho có mà tìm không ra: lỗi của bước tìm, hay gặp hơn cả. | 16 trên 40 câu khó thiếu đoạn đúng trong 10 đoạn | bị từ chối câu mà kho có (ví dụ câu cởi giày khi vào chùa) | 7, 11, 13, 40 |
| Dòng bảng giá là đoạn rất ngắn, ít chữ; câu hỏi viết khác chữ thì dễ bị bỏ sót. | từng có một dòng giá đúng đứng tận hạng 191 | bước tìm dễ bỏ sót dòng giá | 8, 13 |
| Nhiều đoạn rất ngắn: ít chữ để so nghĩa, và tên bài, tên mục chiếm phần lớn chữ để tìm nên các đoạn cùng bài trông giống nhau. | gần 1.800 đoạn ngắn hơn 50 token (kho cuối tháng 10) | đoạn đúng khó được phân biệt | 8, 9 |
| Bài đặt tên mục nghèo thì các đoạn mang nhãn kém và khó tìm. | — | các đoạn của bài đó khó tìm | 9 |
| Mã đoạn dồn số khi sửa giữa bài. | — | — (khi so trước / sau sửa kho phải so theo nội dung) | 8 |
| Ba cặp đoạn lặp một phần ở 3 bài di tích; bỏ phần lặp đã thử, không khác. | 3 cặp | — | 8 |
| Không có cách "chỉ tìm trong lễ hội"; mọi câu tìm trên cả kho. | — | — (muốn lọc thì phải thêm) | 9 |
| Vector không giữ chính xác tên riêng và con số; hai đoạn về hai quán khác nhau có thể có vector rất gần nhau. | — | — (bài 11 thêm từ khoá để bù) | 10 |
| Đoạn không lọt 30 ứng viên theo nghĩa thì không được chấm lại theo từ khoá, kể cả khi trùng chữ y hệt câu hỏi. | 7 trên 40 câu khó | không gì phía sau cứu được trong cùng lần tìm | 10, 11, 13 |
| Bước tìm luôn trả về đủ số đoạn, không có khái niệm "không tìm thấy". | 30 ứng viên, 10 đoạn | việc nhận ra không đoạn nào trả lời được là của model viết | 10, 13 |
| Con số bị tách đôi ở dấu chấm ("40.000" thành "40" và "000"); giữ nguyên cụm số đã thử, không đổi gì. | 32 câu | một con số giá không được nhận như một từ riêng | 11 |
| Từ không có trong từ điển của kho được 0 điểm. | — | tên một nơi chưa có bài nào nhắc tới không giúp tìm | 11 |
| Phải tắt máy chủ trước khi cập nhật chỉ mục; lệnh chỉ kiểm một cổng cố định. | — | máy chủ tắt trong lúc cập nhật; máy chủ chạy ở cổng khác thì không bị bắt (đọc từ chương trình) | 12 |
| Lệnh cập nhật bị ngắt từ lúc bắt đầu ghi vào Qdrant thì máy chủ bật sau đó không trả lời câu nào tới khi chạy lại (cố ý). | — | máy chủ không trả lời câu nào | 12 |
| Sửa đúng một câu mà quy tắc gắn lưu ý ghi nguyên văn thì lệnh cập nhật dừng ở bước cắt đoạn. | 3 câu ở 2 bài | — (người sửa kho phải sửa quy tắc rồi chạy lại) | 12 |
| Bản chụp trước khi ghi nằm bên trong hộp Qdrant; tạo lại hộp là mất. | — | — (đường lùi cuối cùng là lập lại toàn bộ) | 12, 36 |
| Bản ghi chỉ mục không giữ dấu của chương trình cắt đoạn; đổi cách cắt mà không lập lại thì phép kiểm không bắt được (suy ra từ chương trình). | — | — | 12 |
| Kho lớn gấp nhiều lần thì bước cắt đoạn lại cả kho thành phần chính của lệnh cập nhật. | 21 giây hiện nay | — | 12 |

## Chặng 3 — Trả lời một câu hỏi

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Câu cần ghép nhiều nguồn và câu so sánh khó có đủ mảnh cùng lọt 10 đoạn. | điểm thứ hạng khoảng 0,53–0,54, so với 0,80 của câu một dữ kiện | câu trả lời thiếu ý; trợ lý chữa một phần bằng tự tìm thêm | 13 |
| Không có bước xếp lại, nên đoạn đúng đứng hạng 11 tới 30 thì model không thấy ở lần tìm đầu; kết luận "không dùng" đứng trên phép đo cũ. | 9 trên 40 câu khó | model viết không thấy đoạn đó ở lần tìm đầu | 14 |
| Model có thể bỏ sót ý nằm trong 10 đoạn; chỉ thấy khi chấm. | — | câu trả lời thiếu ý | 15 |
| Câu trả lời của Claude dài hơn gpt-6-luna; chủ dự án nhận độ dài này. | khoảng 2,6 tới 3,6 lần tuỳ loại câu | câu trả lời dài, chờ lâu hơn | 15, 33 |
| Thiếu số nguồn chỉ bị phát hiện ở cuối; câu đúng mà quên số nguồn cũng bị rút. | 3 trên 48 lượt (gpt-6-luna), 4 trên 53 lượt (Claude) có câu bị rút, 21/11, trước bản sửa 13:51; trên trình duyệt 22/11: lượt qua kiểm 16 trên 16 thành công, không chữ nào hiện trước khi cả câu hiện; ca bị rút và ca viết lại chưa gặp trên trình duyệt | model trả chữ dần: thấy chữ rồi thấy nó bị rút, kèm nút "Thử lại"; model đang chạy, từ 15:42 22/11: chỉ thấy lời báo và nút "Thử lại" (chữ được giữ tới khi kiểm) | 16 |

## Chặng 4 — Đo

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Chưa có câu nào do người dùng thật hỏi; mọi bộ do AI soạn hoặc nhóm gõ; chưa đối chiếu thước nhiều lượt với người thật. | đủ ý trên bộ cất riêng thấp hơn bộ quen khoảng 0,4 | giới hạn của phép đo | 17, 32, 40 |
| Bộ quen đã dễ, khó thấy cải tiến nhỏ. | 121 trên 176 câu đạt điểm tối đa từ bản đầu tiên | giới hạn của phép đo | 17 |
| Đáp án mẫu cũ dần theo kho. | đã sửa 10 câu (25/10) và 2 câu (30/10) | giới hạn của phép đo | 17 |
| Hai bộ cất riêng của bộ 176 câu đều đã dùng. | 2 bộ | giới hạn của phép đo | 17 |
| Bộ 176 câu chỉ có câu hỏi một lượt, và chưa chạy đủ trên model đang chạy. | mới 85 câu đầu và 54 câu so sánh, nhiều nguồn | giới hạn của phép đo | 17, 19, 32, 40 |
| Thước chính xác của bước tìm nhỏ; một ý có thể chỉ được đánh dấu ở một chỗ. | 55 câu | giới hạn của phép đo | 18 |
| Thước nhanh gần đúng: đoạn diễn đạt khác chữ bị tính trượt, đoạn trùng chữ mà không chứa đáp án bị tính trúng. | — | giới hạn của phép đo | 18 |
| Số của bước tìm đo trên kho cuối tháng 10 tới giữa tháng 11; nhãn mới nhất chưa xét các bài thêm sau. | bản nhãn thứ sáu (14/11) | giới hạn của phép đo | 18 |
| Cả hai thước bước tìm chỉ nhìn lần tìm đầu, không đo việc trợ lý tự tìm thêm. | — | giới hạn của phép đo | 18 |
| Người chấm là model; mốc từ người thật mới có một lần; từ tối 21/11 người chấm cùng họ với model viết, có thể chấm dễ hơn. | chủ dự án đọc 20 cặp, không đủ phân thắng thua | giới hạn của phép đo | 19, 33, 39 |
| Luật "không làm hỏng" chỉ bắt được tụt lan rộng; tụt nhỏ dồn vào một loại câu ít có thể lọt. | — | giới hạn của phép đo | 19 |
| Bộ an toàn nhỏ. | 0 lỗi trên 28 câu chỉ cho biết tỉ lệ lỗi dưới khoảng 10–12 % | giới hạn của phép đo | 19 |
| Nhiều lần thử dùng bộ câu nhỏ, làm ở cấu hình cũ (kho cuối tháng 10, thời còn đưa 5 đoạn), gần như mọi lần với gpt-6-luna; số của hai model không so thẳng. | — | giới hạn của phép đo | 20, 33 |
| Có lần giữ dù một ngưỡng không đạt, đều có ghi lý do (bài 21 dòng 3; hỏi bằng ảnh). | — | giới hạn của phép đo | 20 |

## Chặng 5 — Trợ lý hỏi đáp

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Chạm trần vòng thì mất cả câu trả lời, và vẫn tốn tiền cho các vòng đã chạy; bản "vòng cuối chỉ viết từ những gì đã tìm được" viết xong, chưa mở. | — | nhận câu từ chối dù 10 đoạn của lần tìm đầu đã đủ | 21 |
| Công cụ chỉ được đưa khi câu có từ khoá; câu không có từ trong danh sách thì thiếu công cụ. | 4 trên 60 câu cần công cụ bị sót (3 về nguy hiểm thời tiết, 1 về ngày) | model không được đưa công cụ | 21 |
| Lưới từ nguy hiểm thời tiết vẫn sót vài cách nói tự nhiên và nhận thừa vài câu. | — | "nước có lên nữa không" bị sót; "bão giá", tên phim bị nhận thừa | 24, 40 |
| Mỗi công cụ ăn một vòng, gọi lần lượt. | câu cần ba công cụ mất ba vòng | ba lần chờ model | 21 |
| Tin dài nhiều ý chờ lâu hơn; lần viết lại và lần chạy lại mỗi lần có hạn 45 giây riêng. | 25–34 giây (trước khoảng 20), viết lại lâu thêm khoảng 10 giây; mới đo trên một tin, 6 lần | chờ lâu; một lượt có thể chờ quá 45 giây | 21, 34 |
| Lúc chờ ở tin dài chỉ có một dòng trạng thái đứng yên (giá của việc giữ chữ tới khi kiểm); ý "đổi dòng theo từng lần tìm" đã ghi, chưa làm. | khoảng 20–30 giây | nhìn một dòng chữ không đổi suốt lúc chờ (chỉ số đoạn đã tìm ghi trong ngoặc tăng dần) | 16, 21, 23 |
| Bước viết lại còn ba chỗ chưa đo: điều kiện "đã tìm ít nhất một lần" mới có ca test; cuộc đã có lịch lưu (bước này vẫn chạy ở đó theo chương trình, chỉ chưa đo; lần chạy lại trong cuộc có lịch mới có ca test, chưa có lượt thật); model cũ. | — | đọc từ chương trình, chưa thử thật | 21, 34 |
| Đổi model thì chỗ nối harness có thể hỏng. | với Claude cách cũ: 0 trên 8 lần viết được (đã chữa) | — | 21 |
| Mỗi lượt hỏi tốn thêm một lần gọi model để xếp loại; câu chào tốn hai lần gọi; câu không về Huế tốn thêm phần chạy trước bị bỏ. | ví dụ chính: 0,0034 USD xếp loại so với 0,0144 USD lần viết (Claude) | — (tiền) | 22 |
| Câu chào hỏi không chạy song song nên chậm hơn ở chữ đầu. | câu chậm 5,74 giây khi thử chạy song song | chữ đầu tới chậm hơn câu về Huế | 22 |
| Ranh giới "Huế hay nơi khác" dựa vào hiểu biết địa lý của model. | — | nơi ở rìa Huế có thể bị xếp "ngoài phạm vi" | 22 |
| Câu ngoài phạm vi có thể lọt vào đường "về Huế" và bị đem đi tra web; tên riêng trong câu vẫn tới dịch vụ tìm web, chỉ email và số điện thoại bị bỏ. | 2 trên 44 câu (12/11) | chỉ thấy câu cố định, nhưng câu hỏi đã rời máy | 22, 25, 37 |
| Chỉ nhớ câu trả lời LIỀN TRƯỚC: tin trỏ theo thứ tự vào câu trả lời của hai lượt trước không hiểu được; nơi chỉ nêu qua bài tổng hợp không có trong dòng ghi chú tên nơi. | chuỗi "kể quán ⇒ quán thứ hai ở đâu ⇒ viết gọn lại ⇒ còn quán thứ ba?": tin cuối đúng chỗ một phần nhờ may | trợ lý không xác định được "cái thứ hai" của lượt cũ | 23, 31 |
| Vế cụt không được tìm riêng: thứ vế cụt thật sự hỏi không được tìm, và có vế bị lọc oan. | trước khi mở: 327 trên 1.240 vế (26 %) không có chủ thể; lọc oan dưới 2 % | thứ vế đó hỏi không được tìm riêng | 23 |
| Câu tìm gộp được tách bằng luật chữ ("và", ";", "+"). | 41 % câu tìm của model là câu gộp; 6 % phần tách ra là mẩu cụt (1.116 câu) | cắt hỏng chỉ tốn vài đoạn thừa | 23 |
| Câu phải gom nhiều bài để so ("lăng nào ít leo bậc") không được tìm theo vế cứu. | 0 ⇒ 1 trên 13 tin | tìm theo vế không cứu được | 23 |
| Thẻ nơi gắn cả cho nơi không ai hỏi; thẻ Đại Nội có ở mọi lượt nhiều ý đã đo. | tin 4 ý: 16 thẻ mỗi lượt, khoảng 10 của nơi không ai hỏi; câu trả lời dài thêm khoảng 11–18 % | trợ lý không kể giờ của các nơi đó; câu trả lời dài hơn | 23 |
| Có lúc không có thẻ dù kho có giờ: bài của nơi đã có mặt bằng một đoạn khác; trợ lý gọi công cụ liệt kê hay "gần một điểm" rồi viết luôn; tin một ý hoặc không có chữ hỏi hẹp; quá 25 nơi một lượt (giữ theo thứ tự chữ cái). | ca đoạn khác: đọc từ chương trình, chưa gặp trong mẫu; công cụ rồi viết luôn: đọc từ chương trình, chưa gặp trong mẫu; trần 25: chưa lượt nào chạm | dòng "Tư liệu chưa có thông tin về…" về giờ, địa chỉ, vé vẫn có thể sai | 23 |
| Thẻ chỉ chữa giờ, địa chỉ, vé lẻ; số bậc, năm xây không chữa. Nơi bài không ghi giờ, vé không bao giờ có thẻ (đúng ý). | 13 cặp ngoài thẻ trong mẫu | dòng ý thiếu sai về số bậc, năm xây vẫn có thể còn | 23 |
| Hai bản chữa của thẻ nơi sau khi đọc code (tên lồng "Đầm Chuồn" trong tên quán; câu an toàn "tạm ngừng khi lũ, bão" đi theo thẻ) chưa có lượt thật nào trúng. | 2 trên 113 nơi có thẻ có câu an toàn; chỉ ca test và phép chạy hàm trên kho thật | — (giới hạn của phép đo) | 23 |
| Thẻ nơi mới đo trên một tin 4 ý và ba tin đối chứng; dòng ý thiếu tự trái với câu trả lời có gặp một lần. | tự trái: 1 trên 6 (lượt 1), 0 trên 6 (lượt 2), mốc bên tắt 0 trên 9; tin nhiều ý kiểu khác, model cũ, trình duyệt chưa đo | — (giới hạn của phép đo) | 23 |
| Nhờ "viết lại danh sách" thì trợ lý tra kho lại và viết lại từng mục, không chỉ xoá một dòng; danh sách dài có thể thiếu mục. | 17–24 giây (trình duyệt 22/11: 17,3 và 24,1 giây; lượt thật 19–20 giây, khoảng 0,13–0,17 USD; bên không nhớ 10–12 giây); một lượt thử 8 điểm, bỏ 1, chỉ còn 4 (lần nhìn trên trình duyệt còn đủ 7) | chờ lâu hơn; danh sách mới có thể ngắn hơn, trợ lý nói rõ nó chỉ giữ điểm tìm lại được nguồn — câu đó có thể bị đọc nhầm thành "ba điểm kia chưa chắc miễn phí" | 23, 31 |
| Lần chạy lại một lần khi câu bị rút, trong cuộc đã lập lịch, mới có ca test. | chưa có lượt thật nào trúng | — (giới hạn của phép đo) | 23, 31 |
| Ngày model viết không bị chương trình kiểm lại; dạng ngày ít gặp đi đường công cụ, chậm hơn. | — | ngày chỉ được bảo đảm nhờ nguồn tính sẵn và số nguồn | 24 |
| Thời tiết "tuần sau" chỉ có số cho phần nằm trong 7 ngày. | 7 ngày | chương trình ghi rõ dự báo có tới ngày nào | 24 |
| Khoảng cách và "gần" chỉ cho các điểm có vị trí; "gần" là đường chim bay, không biết giờ mở cửa. | 40 điểm và 41 quán | nơi ngoài bảng không có khoảng cách | 24, 40 |
| Công cụ liệt kê bài so nguyên cụm từ, không hiểu cụm đó nói về cái gì; chương trình chưa lọc. | cụm "miễn phí", đếm trên cả kho: 31 bài khớp, 19 bài chỉ vì một thứ phụ (wifi, vé trẻ em, gửi xe…), trong đó hai điểm thu vé | trợ lý có thể kể một điểm thu vé là miễn phí; ở hai lượt hỏi thật 22/11 model tự bỏ các bài đó (chưa đủ để nói là luôn bỏ); danh sách đổi giữa các lần gõ cùng một câu (8 điểm rồi 6 điểm) | 24 |
| Tổng tiền vé là số model tự cộng, không phải số chương trình tính. | lượt thật 19/11: đúng 3 trên 3 | nhận tổng do model tự cộng | 24, 27, 40 |
| Mục web chỉ được kiểm con số so với đoạn trích, không kiểm địa chỉ hay nội dung; kết quả phần lớn không có ngày đăng. | 4 trên 5 kết quả không có ngày (một lượt đo) | mục web có thể sai hoặc cũ | 25, 40 |
| Một con số không khớp là mất cả mục web; giờ viết theo buổi vẫn bị bỏ oan. | — | mất cả mục web | 25 |
| Cả câu có mục web chậm. | khoảng 15 giây (sổ ghi) | chờ lâu | 25 |
| Câu nhắc sức khoẻ có thể thừa ở câu sát chủ đề. | 3 trên 9 câu đo | dòng nhắc thừa | 25 |
| Các lăng, các điện trông giống nhau dễ nhầm; một tên sai thì trả lời luôn về sai nơi. | — | câu trả lời về sai nơi (đã gặp khi thử) | 26, 40 |
| Chỉ 42 tên; không hỏi được chi tiết trong ảnh vì người trả lời không nhìn ảnh. | 42 | thứ ngoài danh sách nhận "chưa nhận ra" | 26, 40 |
| Lời báo lỗi và lời báo không nhận ra là một; chưa giới hạn số ảnh mỗi người; ảnh rời máy tới hãng model. | — | không phân biệt được hỏng hay không nhận ra | 26, 6 |
| Chống chữ lạ chưa có phép đo hai chiều. | ảnh có chữ ra lệnh: 1 trên 3 ảnh lừa được model (05/11) | bị lừa thì tệ nhất là một câu sai cho chính người đang hỏi | 37, 26 |

## Chặng 6 — Lên kế hoạch và đo trợ lý

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Bảng chỉ có 41 điểm; điểm ngoài bảng không bao giờ vào lịch, dù kho có bài. | 41 điểm | không xếp được điểm mình muốn | 27, 40 |
| Thời lượng của nhiều điểm dựa vào web hoặc là ước. | 31 điểm dựa vào web, 2 điểm ước | giờ gợi ý có thể sai | 27 |
| Ô số người lớn chưa làm đổi lịch, và không sửa được bằng lời. | — | đổi số người lớn không đổi gì | 27, 31 |
| Chưa có ô giờ tới, giờ về. | — | ngày đầu và ngày cuối vẫn xếp đủ buổi | 27, 28, 40 |
| Ca "đi rồi quay lại cùng khu" còn; nhóm giữ giới hạn từ 20/11. | 104 trên 960 cách điền có ít nhất một ngày như vậy, tính cả buổi tối (đếm theo ngày, chỉ ban ngày: 65) | có lịch đi Đại Nội, sang Thiên Mụ, rồi quay lại Ngọ Môn | 28 |
| Phút đi tính theo cụm, không theo đường thật. | — | giờ in ra là phép cộng số cố định | 28 |
| Ngày mưa to vẫn có thể toàn điểm ngoài trời. | 181 trên 300 ngày mưa không chọn sở thích (17/11) | lịch ngày mưa vẫn ngoài trời | 28 |
| Lịch mặc định 1 ngày có điểm đầm phá buổi chiều, trong khi bảng ghi đẹp nhất lúc hoàng hôn; chủ dự án chọn giữ (17/11). | 13:30 – 16:00 | — | 28 |
| Điểm lấp ngoài sở thích không có nhãn trên thẻ lịch. | — | không biết điểm nào không hợp sở thích | 28 |
| Câu dự phòng hiện ra không kèm lời giải thích; buổi trống và tối nghỉ vì ngày đi xa không có dòng nào. | — | câu dự phòng không kèm lời giải thích; ngày đi xa không có dòng tối nghỉ | 29 |
| Bộ 20 yêu cầu chưa chạy lại trên Claude; câu mô tả với Claude dài tới khoảng 50 từ. | — | giới hạn của phép đo | 29 |
| Bước kiểm câu thẻ lịch không bắt được ý sai trong câu; Claude có thể ghép sai ý của câu nguồn dài. | một mục, 12 lượt: sai 1, nói lỏng 4 | câu mô tả có thể gán nhầm danh hiệu cho một vật | 29, 33, 40 |
| File PowerPoint không có mục "Nơi ở", trang chi phí, bản đồ nền; nút ở thẻ lịch cũ tải lịch mới nhất. | — | file thiếu phần so với thẻ lịch; chỉ được báo sau khi tải | 30 |
| Đưa lên mạng phải chép cả thư mục ảnh, không thì file PowerPoint mất ảnh. | — | — | 30 |
| Tệp lịch điện thoại: khung giờ qua nửa đêm sẽ mất sự kiện (bảng hiện chưa có điểm như vậy). | — | — | 30 |
| Quán và khách sạn từ nguồn mở chưa kiểm giờ mở cửa, giá. | — | thông tin có thể đã đổi | 30 |
| Bản đồ không có dòng ghi nguồn của bản đồ mở; phải xem lại trước khi công khai. | — | — | 30 |
| Vài lệnh sửa lịch bị trả "chưa hỗ trợ" dù làm được; câu dời hai điểm kết bằng dấu hỏi có thể nghe như đã đổi; câu giả định có lần bị làm như lệnh thật. | câu giả định: 1 lượt (19/11) | lịch không đổi như ý, hoặc đổi khi chỉ hỏi | 31 |
| Không thay được hoạt động buổi tối, không xếp tay một điểm vào buổi tối; ngày tương đối và ngày âm không đọc được. | — | chương trình nói thật hai điều đầu | 31, 40 |
| Câu gợi ý "thay Y bằng X" chỉ được nhớ đúng một lượt kế; đổi chỗ với ngày không có trong lịch nhận câu chung dễ hiểu nhầm. | — | — | 31 |
| Lệnh bỏ / thay không tên điểm, không mốc lịch ("Bỏ điểm này", "Bớt lăng đi", "Bỏ điểm đầu tiên đi", "ngày 2-3 bỏ điểm đầu") không sửa lịch mà thành câu hỏi thường (từ 22/11). Còn hở: tin có đủ tên một điểm của lịch mà nói về danh sách vừa kể. | chỗ hở: chưa thấy thật | lịch không đổi; phải nhắn kèm tên điểm, "ngày N" hoặc "khỏi lịch" | 31, 23 |
| Ba trong bốn vai chưa đạt ở 12 vai vướng ý kho thiếu; người mô phỏng hay tự kết sớm. | trần thước khoảng 8–9 trên 12; kết trước lượt 5: 6 trên 12 (gpt-6-luna), 5 trên 12 (Claude) | giới hạn của phép đo | 32 |
| Thước 12 vai có một điểm mù: người mô phỏng không thấy dòng báo của lượt sửa lịch; công cụ đã chữa, chưa đo lại. | 26 lượt, thuộc một vai | giới hạn của phép đo | 32, 40 |
| Lượt 12 vai đo lại 22/11 chạy trước bốn thay đổi khâu tìm mở 14:47, nên chưa đo bộ đó; luật "ba lượt" chưa sửa chữ cho khớp lựa chọn tối 21/11. | 8 trên 12 phiên, 33 trên 38 ý | giới hạn của phép đo | 32 |

## Chặng 7 — Máy móc bên dưới

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Đổi sang Claude là đổi tạm; đường gpt-6-luna nguyên vẹn nhưng tài khoản đang ngừng dùng; các tính năng mở từ tối 21/11 chưa đo trên gpt-6-luna. | — | — | 33, 40 |
| Chưa đo lại mức suy luận vừa và thấp ở lượt có công cụ sau khi sửa lớp nối. | — | giới hạn của phép đo | 33 |
| Phụ thuộc một khoá Bedrock tạm do chủ dự án giữ; bản đưa lên mạng chưa có cách cấp khoá lâu dài. | — | khoá hết hạn là ô hỏi đáp ngừng cho tới khi làm mới | 33, 37 |
| Số chờ tới chữ đầu đo khi hai model chạy cùng lúc trên một máy. | khoảng 13,0 giây trên 153 lượt; dài hơn chạy một mình khoảng 2,5 tới 4,5 giây | giới hạn của phép đo | 34 |
| Chưa đo lại với Claude lợi của chạy song song và của tính sẵn ngày. | — | giới hạn của phép đo | 34 |
| Gõ lại đúng một câu chưa chắc về ngay: câu trả lời nhiều ý còn dòng "Tư liệu chưa có thông tin về…" không được lưu (chủ ý từ tối 21/11); bỏ dấu hỏi cuối câu cũng là một câu khác. | thử trên trình duyệt 22/11: câu một ý lần hai 0,2 giây, chữ y hệt; câu hai ý lần hai 9,4 giây, chữ khác | gõ lại câu nhiều ý thì có lúc về ngay, có lúc chờ như lượt thường và nhận chữ khác lần đầu | 34 |
| Bộ nhớ câu trả lời chỉ nằm trong đúng một máy chủ đang chạy; trúng thì không hiện dòng tiến độ; tỉ lệ trúng ngoài đời chưa có số. | — | — | 34 |
| Tiền ghi sổ của Claude chưa đối chiếu hoá đơn; trang theo dõi trên máy phát triển lẫn lượt thử của nhóm. | — | — | 34, 33 |
| Hai tab cùng trình duyệt dùng chung một cuộc; tab mở sau xoá cuộc cùng lịch của tab trước. | đã xác nhận bằng một lượt thử thật trưa 22/11 | mở tab thứ hai là mất cuộc của tab thứ nhất | 35, 40 |
| Đường đánh giá một lượt có ở máy chủ nhưng giao diện chưa dùng. | — | — | 35 |
| Lệnh bật chỉ cho máy phát triển và không gọi thử model. | — | không bắt được khoá hết hạn lúc bật | 36 |
| Gói ba hộp là bản nháp từ 10–18/11, chưa theo kịp chương trình hiện tại. | lần chạy thử là của gpt-6-luna và kho 204 bài | — | 36 |
| Trần kích thước yêu cầu và lớp chặn tiền ở phía hãng chưa có. | — | — (rủi ro khi đưa lên mạng) | 37 |
| Trang Giới thiệu vừa được sửa cho khớp thứ trợ lý thật sự nhớ (ba câu hỏi gần nhất, câu trả lời liền trước, tên nơi vừa gợi ý, lịch đã lập; câu trả lời cho câu mở đầu giữ tới 24 giờ), nhưng chưa ai nhìn trên trình duyệt; bản giao diện dựng sẵn chưa dựng lại. Phần nơi nhận câu hỏi và ảnh đã đúng từ chiều 22/11. | — | máy đang chạy lúc viết còn hiện chữ cũ ("nhớ các câu hỏi") tới khi giao diện được dựng lại | 37 |
| Hãng model và dịch vụ tìm web giữ dữ liệu bao lâu ở phía họ: chưa kiểm. | — | — | 37 |

## Chặng 8 — Nhìn lại

| Giới hạn (một câu) | Con số kèm theo | Người dùng gặp gì | Bài |
|---|---|---|---|
| Chưa so một phiên với nhiều phiên bằng phép đo nào; chưa thử để Codex hay Antigravity làm phiên thực thi với bộ luật hiện tại. | — | — | 39 |
| Rào bằng máy không chặn việc đọc: một đoạn chương trình tự mở file khoá vẫn đọc được; bộ câu chấm cất riêng chỉ được giữ bằng luật chữ. | kiểm bằng file giả ngày 18/11 | — | 39 |
| Ba ngày thử "nhóm tự giữ luật" chưa có kết quả xét lại lúc viết. | — | — | 39 |

## Thứ cố ý không làm (không phải giới hạn)

Bảng này chép từ bài 4. Mỗi dòng là một ranh giới đã được chọn, không phải một lỗi còn nợ.

| Không làm | Người dùng gặp gì | Bài |
|---|---|---|
| Câu hỏi gõ không dấu | hay nhận câu từ chối (đo trên 32 câu: có dấu 13 câu đủ đoạn đúng, bỏ dấu còn 1; câu không dấu không bật công cụ) | 4, 10, 11, 13, 24 |
| Tiếng Anh | không hỗ trợ | 4 |
| Tình huống khẩn cấp (bị cướp, mất giấy tờ, số điện thoại khẩn cấp) | được xử lý như một câu hỏi thường về Huế; không có phần hướng dẫn riêng | 4, 22 |
| Đặt phòng, đặt bàn, mua vé, gửi tin thay người dùng | nhận một câu nói thật "mình chưa làm thay được", kèm cách tự làm | 4 |
| Giá phòng trong phần gợi ý chỗ ở | không hiện | 4, 30 |
| Giọng nói | không có (còn chờ chủ dự án nói rõ bỏ hẳn hay làm sau) | 4 |
| Nhớ sở thích của từng người giữa các lần dùng | không có; mỗi lần mở lại trang là một cuộc trò chuyện mới | 4 |
| Câu hỏi không thuộc văn hoá, du lịch Huế | nhận một câu cố định: "Mình chỉ hỗ trợ thông tin về văn hoá và du lịch Huế…" | 4, 22 |

Riêng việc đưa lên mạng thì khác loại: chưa làm, không bắt buộc với đồ án, và còn nằm trong lộ trình sau khi mọi thứ xong ở máy (bài 4, 40).

<details><summary>Nguồn (để giữ trang đúng — anh không cần đọc)</summary>

Gom từ mục "Giới hạn đã biết" của các bài 5–37 và 39 trong cùng thư mục (bài 1–4, 38 không có mục này; bài 40 không có mục riêng, các dòng ghi bài 40 lấy từ bảng "Chỗ yếu đã biết" và "Những thứ chưa đo" của bài 40), bản lúc 15:22 ngày 22/11/2026; bảng cuối trang chép từ mục "Những thứ cố ý không làm" của bài 4. Không thêm sự thật mới. Cột "Người dùng gặp gì" ghi "giới hạn của phép đo" khi bài gốc không nói người dùng thấy gì và giới hạn nằm ở cách đo. Chỗ hai bài nói khác nhau ghi ở báo cáo gom [riêng tư].

Gom lại 17:05 22/11/2026 theo các bài vừa sửa (khớp hệ thống 16:35 22/11): bỏ dòng "Cuộc có lịch lưu không nhớ câu trả lời liền trước và không có lần chạy lại" (sai từ 16:08 22/11, khi mở việc nhớ câu trả lời liền trước cả trong cuộc đã lập lịch); thêm dòng "viết lại danh sách", dòng "lần chạy lại trong cuộc đã lập lịch mới có ca test", và đổi dòng "tin trỏ theo thứ tự…" thành "chỉ nhớ câu trả lời LIỀN TRƯỚC" (bài 23 "Giới hạn đã biết" gạch 1, 2, 5; bài 31 "Giới hạn đã biết"); dòng dòng trạng thái đứng yên (bài 16, 21, 23); nhãn trình duyệt của dòng "Thiếu số nguồn…" (bài 16); dòng "Bước viết lại còn ba chỗ chưa đo" (bài 21); dòng liệt kê bài so nguyên cụm từ (bài 24, gạch thứ năm); dòng trang Giới thiệu (bài 37, bản 16:54 22/11) [chép từ bài].

- Năm dòng thẻ nơi (thêm 17:31 22/11/2026): bài 23 "Giới hạn đã biết" năm gạch thẻ nơi; gốc ở `guides/RUNBOOK_BAN_GIAO.md` mục 10.1 hàng "Thẻ nơi" [chép]. Không có dòng nào của trang này ghi "dòng 'Tư liệu chưa có…' có lúc sai" để sửa cho khớp bài 40. Bảng tăng năm hàng.

</details>
