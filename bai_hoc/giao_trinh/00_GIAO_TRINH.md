# Giáo trình hue_rag: hiểu cả hệ thống từ đầu, không cần đọc code

*Cập nhật 11:35, ngày 23/11/2026 · khớp các bài sáng 23/11 (giao diện mới, 48 tính năng, kho 267 bài): bốn dòng mới ở "Có gì mới" (giao diện "Dòng sông dẫn đường"; ba bản sửa nhỏ của lõi; hai phép đếm dẫn tới không làm; bộ test 2.218 ca và kịch bản chạy thử theo giao diện mới); số đếm phụ lục C, E, F theo bản mới · trước đó (22/11: các bản sửa nhỏ tối 22/11, mẫu đề bài cho AI khác hãng) · đủ 41 bài và 9 phụ lục; mỗi bài đã qua một lượt đối chiếu độc lập với chương trình và số đo · từ chiều 22/11 mọi thứ mới của hệ thống được ghi vào bộ này, liệt kê ở mục "Có gì mới" ngay dưới · mọi con số lấy từ hệ thống đang chạy và các phép đo đã ghi, không có phép thử mới.*

**Bộ này cho ai.** Cho anh, người sẽ tự chạy thử, tự trình bày và tự trả lời câu hỏi về đồ án. Không cần đọc code. Biết dùng một chatbot là đủ để bắt đầu.

**Đọc thế nào.** Đọc theo đúng số thứ tự: bài sau dựa trên bài trước, khái niệm mới luôn được giảng trước khi dùng. Mỗi bài chia hai nửa:

- **Nửa để hiểu** (từ đầu bài tới hết mục "Câu hỏi tự kiểm"): đọc lần đầu chỉ cần nửa này. Trong đó có hai mục để anh giải thích lại được chứ không chỉ kể lại được: **"Quyết định và lý do"** (vì sao làm thế này mà không làm thế khác, và cái giá của lựa chọn) và **"Nếu… thì sao"** (một thứ hỏng, hoặc điều kiện đổi, thì hệ thống làm gì).
- **Nửa để tra** (từ mục "Cấu hình đang chạy" trở xuống): model nào, tham số nào, đã thử phương án nào, ra số bao nhiêu, hỏng ở đâu. Không cần đọc để hiểu bài, nhưng đây là chỗ trả lời các câu "cụ thể là bao nhiêu" và "đã thử cách nào, ra số nào".

**Con số của hệ thống trong bộ này** (số bài, số đoạn, tính năng nào đang mở) là số lúc bài được viết, ghi ở dòng cập nhật của từng bài. Hệ thống vẫn đang được làm tiếp nên vài con số có thể đã lớn hơn khi anh đọc; cách hoạt động thì không đổi theo.

**Năm ví dụ dùng suốt cả bộ** (đều là lượt chạy thật qua hệ thống):

| Ví dụ | Người dùng gõ / chọn | Dùng để giảng |
|---|---|---|
| **Ví dụ chính** | *"Giá vé tham quan Đại Nội Huế là bao nhiêu?"* | đường đi bình thường của một câu hỏi: tìm ra 10 đoạn, model viết, có 5 nguồn |
| **Ví dụ "kho không có"** | *"Chùa Thiên Mụ có chỗ đậu ô tô không?"* | kho không nói tới thì hệ thống từ chối thay vì đoán, rồi tra web ở một mục riêng |
| **Ví dụ "phải tìm thêm"** | *"Mặc áo dài vào Đại Nội có được miễn vé không?"* | lần tìm đầu chưa đủ, trợ lý tự tìm thêm hai lần rồi mới trả lời |
| **Ví dụ "kho có mà tìm không ra"** | *"Vào chùa ở Huế có phải cởi giày không?"* | giới hạn của bước tìm: kho có một câu trả lời nhưng ba lần tìm đều không lấy ra |
| **Ví dụ lập lịch** | trang Lên kế hoạch: 3 ngày, 2 người lớn, thích di tích | chương trình xếp 11 điểm vào 3 ngày, model chỉ viết câu mô tả |

## Có gì mới

Hệ thống vẫn đang được làm tiếp. Mỗi khi người dùng thấy một thứ khác đi, bài của phần đó được sửa và một dòng được thêm vào đây, mới nhất ở trên. Đã đọc cả bộ rồi thì chỉ cần đọc mục này và các bài nó trỏ tới.

| Ngày | Người dùng thấy gì khác | Đọc ở |
|---|---|---|
| 23/11, sáng | Giao diện mới "Dòng sông dẫn đường", ở bản chính từ 10:00: Trang chủ có màn đầu với ảnh sông Hương trong hình khúc sông và sáu bến là sáu lối vào (ở cửa sổ thấp hơn 869 điểm ảnh, gồm máy demo 1536 × 695, bến chỉ còn tên); lúc chờ câu trả lời là thẻ chờ: con đò chạy, dòng trạng thái đổi theo từng bước, tên các bài đã tìm thấy thêm dần và bấm được để đọc trong lúc chờ (máy demo hiện 3 tên); dưới câu trả lời là khung "Nguồn đã dùng", mỗi bài một nút có chấm màu theo chủ đề. Chỉ đổi lớp nhìn: tính năng, luồng hỏi, lập lịch, xuất file không đổi, vẫn 48 tính năng đang mở. Trước khi gộp: 761 ảnh chụp tự động ở tám cỡ khung nhìn, kịch bản 50 bước (49 đạt, 1 bước để người xem ảnh, 0 trượt). Chưa ai thử trên điện thoại thật, chưa ai in bằng tay; thẻ chờ của tin dài đã được chụp tự động, nhưng thời gian chờ trên giao diện mới chưa đo. Ở trang Lên kế hoạch, cửa sổ rộng 1280 điểm ảnh, khung trợ lý nổi che hết cột bản đồ và mép phải cột lịch (chưa chữa). | bài 5, bảng các trang, mục "Một lượt hỏi", quyết định 4, "Thử trong 2 phút", "Giới hạn đã biết"; bài 35, mục "Lớp nhìn mới…", quyết định 4, "Đã so"; bài 27, "Giới hạn đã biết"; bài 30, "Quyết định nhỏ hơn" (tỉ lệ bản in) |
| 23/11, sáng | Ba bản sửa nhỏ của lõi, không thêm tính năng. (1) Hỏi về một nơi mà bài của nó đi qua công cụ liệt kê, "gần một điểm" hay thẻ nơi, và câu lưu ý an toàn của bài nằm trên hai dòng (đúng một bài: "Đi lại ở Huế"): dòng "Lưu ý trong nguồn …" nay không rơi; lượt thật từng gặp: 0 trên 27. (2) Nhờ làm thay (đặt phòng, mua vé…) ở lượt phải qua bước viết lại: câu "chưa làm thay được" nay hiện một lần, không còn hai lần liền nhau; lượt thật từng đi qua đường này: 0. (3) Nhà cung cấp model lỗi tạm thời ở một lời gọi: hệ thống chờ 1 giây rồi gọi lại đúng một lần; người dùng chỉ thấy lượt chậm hơn (có thể gần gấp đôi); lần hai vẫn lỗi thì vẫn "Không thể tạo câu trả lời vào lúc này." và nút "Thử lại". Loại lỗi này đã gặp hai lần thật (khoảng 1 trên 500 lượt); cơ chế gọi lại mới có ca test, chưa gặp lỗi thật. Bằng chứng của cả ba là ca test (bản (1) thêm một phép chạy trên cả 267 bài). | bài 24, mục "Chi tiết để tra"; bài 16, mục "Chi tiết để tra"; bài 33, mục "Quyết định nhỏ hơn" và bảng "Nếu… thì sao" |
| 23/11, sáng | Không phải thay đổi mà là hai phép đếm 0 đồng trên sổ các lượt đã chạy (218 lượt, Claude Sonnet 5.5), đều dẫn tới không làm. Hạ mức suy luận chỉ ở lần viết cuối của tin dài: lợi lớn nhất khoảng 6 trong 25 giây, vì thời gian chờ gần như chỉ là số token model viết ra. Cho chương trình làm thay các lần model tự tìm thêm: mỗi vòng tìm thêm chỉ khoảng 2 giây, và 75–100 % các lần tự tìm mang về đoạn mới được trích. Nhóm đóng hướng rút ngắn thời gian chờ tin dài trên máy hiện tại; thứ còn lại là chữ chạy dần trên bản đưa lên mạng. | bài 34, mục "Đã so"; bài 23, mục "Đã so" dòng 15 |
| 23/11, sáng | Không phải thứ người dùng thấy: lần chạy đủ bộ test mới nhất (09:41–09:59) trên bản có giao diện mới và ba bản sửa lõi: 82 file chạy, 2.218 ca đạt, không ca nào hỏng, 4 file bỏ vì cần khoá OpenAI (lần trước đó, 20:48–21:07 22/11: 2.197 ca). Cùng đợt, kịch bản chạy thử của bài 41 tả màn hình mới: thẻ chờ có tên bài (ở máy 1536 × 695 chỉ hiện 3 tên đầu), khung "Nguồn đã dùng", khung trợ lý nổi khi sửa lịch (ở máy 1536 × 695 che cột bản đồ), nút "In / Lưu PDF"; các lượt chạy lặp của kịch bản chạy trước giao diện mới, cột "Sẽ thấy gì" đọc từ chương trình, ảnh chụp và kịch bản thao tác của cổng gộp. | bài 38, mục "Ý chính" và "Chi tiết để tra"; bài 41, mục 3; bài 40, hàng Giao diện |
| 22/11, tối | Câu trả lời về ngày, lịch âm có trích nguồn "Lịch hệ thống": bấm mở nguồn đó nay chỉ thấy các dòng ngày, không còn thấy dòng "Ghi chú: người dùng không nêu năm…" (một lời dặn dành cho model). Bằng chứng là test, chưa nhìn trên trình duyệt. | bài 24, mục "Chi tiết để tra" |
| 22/11, tối | Câu trả lời về bão, lũ có trích nguồn "Tin bão / lũ chính thức": bấm mở nguồn đó nay đọc thấy câu bản tin chính thức + 112, không còn thấy lời dặn nội bộ dành cho model. Bằng chứng là test, chưa nhìn trên trình duyệt. | bài 24, mục "Chi tiết để tra" |
| 22/11, tối | Tin sửa lịch tả thời tiết xấu mà không có chữ "bão", "lũ"… (ví dụ "gió giật mạnh quá, bỏ Đầm Chuồn đi"): nếu trợ lý kịp tự tra cứu bão, lũ trước khi hiểu xong lệnh sửa thì câu bản tin chính thức + 112 nay không mất khi lịch được sửa; thường là không kịp, nên thường vẫn không có câu đó (giới hạn nhóm giữ). Tin có chữ "bão", "lũ"… thì vẫn luôn có câu đó, như trước. Bằng chứng là một ca test, chưa có lượt thật. | bài 24, mục "Giới hạn đã biết" và "Chi tiết để tra" |
| 22/11, tối | Ở lượt có một câu mang con số lạ bị bước kiểm số gỡ, với model đang chạy: câu trả lời nay hiện thẳng ở dạng đã gỡ câu đó (trước: có thể thấy câu sai rồi thấy nó biến mất). Bản viết lại còn lỗi kiểm thì không hiện, chỉ có lời báo và nút "Thử lại". Chưa người dùng nào gặp cả hai ca; bằng chứng là test. | bài 6, mục "Chi tiết để tra" |
| 22/11, tối | Ở cuộc đã có lịch, tin có số ngày viết bằng chữ "sáu" ("kéo dài thành sáu ngày") mà lần hiểu ý đọc ra một lệnh đổi số ngày thì cả lượt ra lời báo "Đã xảy ra lỗi trong hệ thống. Vui lòng thử lại sau."; nay được xử như mọi tin đổi số ngày (lịch dài nhất 5 ngày nên lịch không đổi). Chưa người dùng nào gặp; bằng chứng là test. Cùng đợt, bốn giới hạn đã đếm được ghi vào bài: ba cái nhóm chốt giữ, một cái (từ chỉ ngày ở câu hỏi trước) để sửa sau vì hiếm. | bài 31, mục "Chi tiết để tra" và "Giới hạn đã biết"; bài 23, mục "Giới hạn đã biết" |
| 22/11, tối | Không phải thứ người dùng thấy: đề bài gửi AI khác hãng nay phải nói rõ bên kia được dùng hết công cụ mạnh nhất của mình, mang đủ trạng thái của dự án, có danh sách nên đọc và cả những điểm nhóm đã tìm ra (anh dặn ba lần tối 22/11: "bạn nắm gì thì các model AI khác cũng vậy"). | bài 39, lớp 3 của mục ba lớp kiểm và mục "Chi tiết để tra"; bài 37, mục các đợt rà rủi ro |
| 22/11, tối | Ở cuộc đã có lịch, xin thêm vào buổi tối một điểm ban ngày đang có trong lịch ("thêm Đại Nội về đêm vô tối ngày 1") thì, khi trợ lý hiểu tên điểm là Đại Nội, nhận lý do thật: điểm tham quan ban ngày không xếp được vào buổi tối (trên màn hình dòng này đứng sau chữ "Không đổi được: "). Trước đó nhận câu "… đã có trong lịch." (một ca test; chưa có lượt thật qua trình duyệt). Cùng lúc bài ghi rõ một giới hạn dễ gặp khi thử: lịch vừa xếp thì lệnh "thêm X" gần như luôn bị trả "Chưa làm…", vì lịch kín giờ và chương trình không tự thế chỗ; lối ra là nhắn đúng câu "thay Y bằng X" được gợi ý, hoặc điền lại biểu mẫu với kiểu đi nhiều điểm hơn (với nhóm có trẻ em hay người lớn tuổi, đổi kiểu đi không thêm chỗ: lịch luôn mỗi buổi một điểm). | bài 31, bảng "Nếu… thì sao", quyết định 4, mục "Giới hạn đã biết" và "Chi tiết để tra" |
| 22/11, tối | Không phải thay đổi mà là hai cách làm nhanh tin dài nhiều ý đã đo rồi bỏ theo tiêu chí ghi trước: hạ mức suy luận xuống vừa (nhanh hơn khoảng 8 giây nhưng trượt một điều ghi trước, và 3 trên 6 lượt nói kho không có vé cho bé dưới 7 tuổi dù kho có) và cho lần tìm đầu phủ luôn chuyện miễn giảm vé (trung vị chỉ nhanh hơn 1,9 giây, cần 3). Điều rút ra: ở tin dài, lượt chậm là lượt model tự tìm thêm lần thứ hai. | bài 33, mục "Đã so"; bài 23, mục "Đã so" dòng 14; bài 34, mục "Giới hạn đã biết" |
| 22/11, tối | Không phải thứ người dùng thấy: lần chạy đủ bộ test mới nhất lúc đó (20:48–21:07; từ 23/11 là lần trước đó, dòng 23/11 ở trên) trên bản lúc đó: 78 file chạy, 2.197 ca đạt, không ca nào hỏng, 4 file bỏ vì cần khoá OpenAI. | bài 38, mục "Ý chính" và "Chi tiết để tra" |
| 22/11, tối | Không phải thứ người dùng thấy: bộ kiểm mà git tự chạy mỗi khi lưu một thay đổi vào lịch sử dự án: phép quét trùng chữ của nó nay chỉ còn so với bộ câu chấm cất riêng; chữ của kho và của bộ câu mẫu được trích nguyên văn vào tài liệu (anh chọn lúc 16:44). Các phép chặn khác giữ nguyên. | bài 37, mục "Chi tiết để tra"; bài 39, quyết định 5 |
| 22/11, tối | Với tin hỏi nhiều ý có chữ hỏi giờ, mở cửa, địa chỉ hay "ở đâu", trợ lý thôi ghi "Tư liệu chưa có thông tin về…" cho giờ, địa chỉ mà bài riêng của nơi đó có, và cho giá vé lẻ của những nơi có trong bảng vé lẻ. Chương trình tự gắn thêm cho mỗi nơi được nhắc tên một nguồn nhỏ chép nguyên dòng địa chỉ, giờ từ bài của nơi đó; hàng vé lẻ đi vào một nguồn riêng mở bài vé (gọi chung là thẻ nơi). Không gọi model thêm. Đây là tính năng thứ 48 đang mở. | bài 23, mục "Tin nhiều ý được trả lời theo từng ý", "Đã so" và "Giới hạn đã biết" |
| 22/11, tối | Trang Giới thiệu được viết lại hai chỗ cho đúng hiện trạng: thứ trợ lý nhớ trong một cuộc trò chuyện, và giới hạn về lễ hội, sự kiện theo ngày. Giao diện đã dựng lại và phiên đo đã nhìn trang này trên trình duyệt tối 22/11. | bài 37, mục "Giới hạn đã biết" |
| 22/11, tối | Không phải thay đổi mà là điều mới ghi rõ sau một lượt thử: gõ lại đúng một câu ở cuộc mới thì câu một ý về ngay (0,2 giây); câu nhiều ý mà lần đầu còn dòng "Tư liệu chưa có…" thì được tìm và viết lại. | bài 34, mục "Giới hạn đã biết" |
| 22/11, tối | Hỏi "kể các điểm tham quan miễn phí" thì Hải Vân Quan không còn bị kể; hỏi giá vé Hải Vân Quan thì nhận 70.000 đồng, không còn lời "hai nguồn không khớp". Kho từng có một dòng nói ngược bài vé; dòng đó đã sửa. | bài 7, bảng các lần kho đổi; bài 24, mục "Giới hạn đã biết" (công cụ liệt kê bài) |
| 22/11, chiều | Hỏi đường từ Huế đi Hội An thì có câu trả lời có nguồn: kho thêm một bài về việc này (kho nay 267 bài, 9.479 đoạn). | bài 7, bảng các lần kho đổi ở mục "Chi tiết để tra" |
| 22/11, chiều | Trong một cuộc trò chuyện đã lập lịch, trợ lý cũng nhớ câu nó vừa trả lời: nhờ "bỏ quán đầu đi rồi viết lại danh sách" thì nhận danh sách đã bỏ đúng quán đầu. Đây là tính năng thứ 47 đang mở. | bài 23, mục "Máy chủ nhớ ba lượt gần nhất, và chỉ một câu trả lời" và mục "Giới hạn đã biết"; bài 31, mục "Nếu… thì sao" |
| 22/11, chiều | Lệnh "bỏ … đi" hoặc "thay … đi" chỉ sửa lịch khi tin nêu tên điểm hoặc chỉ vào lịch ("của ngày 2", "khỏi lịch"); không thì lịch đứng yên và tin được trả lời như một câu hỏi thường. | bài 31, bước 2 và mục "Quyết định nhỏ hơn" |
| 22/11, chiều | Ở ô chat không còn cảnh chữ hiện ra rồi bị thay hoặc bị rút: lúc chờ chỉ có một dòng trạng thái (giao diện lúc đó; từ 23/11 lúc chờ là thẻ chờ, dòng 23/11 ở trên), rồi cả câu trả lời hiện một lần sau khi đã qua bước kiểm nguồn (lượt thường đã nhìn trên trình duyệt; lượt bị rút và lượt phải viết lại: theo chương trình và test). | bài 6, quyết định 4; bài 16 |

## Đường chính: chín chặng

Cột cuối: ✅ đã viết · ⬜ chưa viết.

### Chặng 0 — Nền: vì sao phải xây cả một hệ thống quanh model?

| Số | Bài | |
|---|---|---|
| 1 | [Model ngôn ngữ là gì, và vì sao nó viết trôi chảy mà vẫn sai](01_MODEL_NGON_NGU.md) | ✅ |
| 2 | [RAG là gì: cho model đọc tài liệu trước khi trả lời](02_RAG_LA_GI.md) | ✅ |
| 3 | [Trợ lý và công cụ: model chỉ "xin", chương trình mới là thứ chạy](03_TRO_LY_VA_CONG_CU.md) | ✅ |

### Chặng 1 — Bức tranh: hệ thống này làm gì, cho ai, gồm những khối nào?

| Số | Bài | |
|---|---|---|
| 4 | [Bài toán: ai dùng, hỏi gì, nhận gì, và những thứ cố ý không làm](04_BAI_TOAN.md) | ✅ |
| 5 | [Người dùng thấy gì: các trang của ứng dụng](05_NGUOI_DUNG_THAY_GI.md) | ✅ |
| 6 | [Kiến trúc: các khối, vì sao đặt như vậy, và khi một khối hỏng thì sao](06_KIEN_TRUC.md) — **bài mẫu theo khuôn mới** | ✅ |

### Chặng 2 — Chuẩn bị kho: làm một lần, trước khi có câu hỏi nào

| Số | Bài | |
|---|---|---|
| 7 | [Kho dữ liệu: 267 bài viết về Huế, ai soạn, lấy từ đâu, kiểm thế nào](07_KHO_DU_LIEU.md) | ✅ |
| 8 | [Cắt bài thành đoạn (chunking)](08_CAT_DOAN.md) | ✅ |
| 9 | [Thông tin gắn kèm mỗi đoạn (metadata) và "chữ để tìm"](09_METADATA.md) | ✅ |
| 10 | [Biến mỗi đoạn thành một dãy số mang nghĩa: embedding](10_EMBEDDING.md) | ✅ |
| 11 | [Tìm theo chữ trùng: từ khoá BM25](11_TU_KHOA_BM25.md) | ✅ |
| 12 | [Cất vào Qdrant, cập nhật khi kho đổi, và vì sao kho lệch chỉ mục thì không câu hỏi nào được trả lời](12_QDRANT.md) | ✅ |

### Chặng 3 — Trả lời một câu hỏi: mỗi lần người dùng gõ

| Số | Bài | |
|---|---|---|
| 13 | [Tìm: lấy 30 ứng viên, trộn hai bảng xếp hạng, giữ 10 đoạn](13_TIM.md) | ✅ |
| 14 | [Xếp lại bằng model (reranking): đã thử ba cách, không dùng](14_XEP_LAI.md) | ✅ |
| 15 | [Viết câu trả lời: lời dặn, ngữ cảnh 10 đoạn, và số nguồn [n]](15_VIET_CAU_TRA_LOI.md) | ✅ |
| 16 | [Kiểm nguồn bằng chương trình, và câu từ chối cố định](16_KIEM_NGUON_VA_TU_CHOI.md) | ✅ |

### Chặng 4 — Vì sao tin được: đo

| Số | Bài | |
|---|---|---|
| 17 | [Bộ 176 câu hỏi mẫu: đề kiểm tra của hệ thống](17_BO_CAU_HOI_MAU.md) | ✅ |
| 18 | [Chấm bước tìm: đoạn đúng có lọt vào 10 đoạn không](18_CHAM_BUOC_TIM.md) | ✅ |
| 19 | [Chấm câu trả lời: ba thang điểm, người chấm là model, và nhiễu](19_CHAM_CAU_TRA_LOI.md) | ✅ |
| 20 | [Một thí nghiệm được làm thế nào, và nhìn cả bảng các lần so sánh thấy gì](20_MOT_THI_NGHIEM.md) | ✅ |

### Chặng 5 — Trợ lý hỏi đáp: khi tìm một lần rồi viết là chưa đủ

| Số | Bài | |
|---|---|---|
| 21 | [Harness: phần chương trình bao quanh model](21_HARNESS.md) | ✅ |
| 22 | [Xếp loại câu trước khi tìm: bốn tuyến](22_XEP_LOAI_CAU.md) | ✅ |
| 23 | [Tìm thêm, nhớ câu hỏi trước, và câu hỏi nhiều ý](23_TIM_THEM_NHO_NHIEU_Y.md) | ✅ |
| 24 | [Việc phải đúng thì chương trình tính: ngày âm lịch làm mẫu, rồi thời tiết, khoảng cách và các công cụ khác](24_VIEC_PHAI_DUNG_THI_CHUONG_TRINH_TINH.md) | ✅ |
| 25 | [Khi kho không có: tra web một lần, để riêng mục "chưa kiểm"](25_TRA_WEB.md) | ✅ |
| 26 | [Hỏi bằng ảnh](26_HOI_BANG_ANH.md) | ✅ |

### Chặng 6 — Lên kế hoạch: chương trình xếp lịch, model chỉ diễn đạt

| Số | Bài | |
|---|---|---|
| 27 | [Trang Lên kế hoạch: từ mấy nút chọn tới một lịch, và bảng điểm tham quan đứng sau](27_TRANG_LEN_KE_HOACH.md) | ✅ |
| 28 | [Chương trình xếp lịch theo luật nào: một lịch thật được xếp từng bước](28_CHUONG_TRINH_XEP_LICH.md) | ✅ |
| 29 | [Khi không xếp được, bước kiểm lịch, và phần việc của model](29_KHONG_XEP_DUOC_KIEM_LICH_VIEC_CUA_MODEL.md) | ✅ |
| 30 | [Quanh một lịch: chỗ ở, quán ăn, ảnh, bản đồ, xuất file](30_QUANH_MOT_LICH.md) | ✅ |
| 31 | [Sửa lịch bằng lời: model hiểu ý, chương trình áp và kiểm](31_SUA_LICH_BANG_LOI.md) | ✅ |
| 32 | [Đo một trợ lý: hội thoại nhiều lượt, người dùng mô phỏng, kịch bản chạy lặp](32_DO_MOT_TRO_LY.md) | ✅ |

### Chặng 7 — Máy móc bên dưới

| Số | Bài | |
|---|---|---|
| 33 | [Model viết, mức suy luận, và đổi model bằng một dòng cấu hình](33_MODEL_VIET_VA_DOI_MODEL.md) | ✅ |
| 34 | [Người dùng chờ bao lâu, một câu tốn bao nhiêu tiền](34_CHO_BAO_LAU_TON_BAO_NHIEU.md) | ✅ |
| 35 | [Trang web và máy chủ: ai gửi gì cho ai](35_TRANG_WEB_VA_MAY_CHU.md) | ✅ |
| 36 | [Bật hệ thống trên máy, và đóng gói bằng Docker](36_BAT_HE_THONG_VA_DOCKER.md) | ✅ |
| 37 | [Bảo mật: khoá bí mật, dữ liệu người dùng, và chữ lạ chen vào lời dặn](37_BAO_MAT_VA_DU_LIEU_NGUOI_DUNG.md) | ✅ |
| 38 | [Bộ test: chương trình tự kiểm những gì](38_BO_TEST.md) | ✅ |

### Chặng 8 — Nhìn lại

| Số | Bài | |
|---|---|---|
| 39 | [Đồ án được làm thế nào: một người quyết định và nhiều coding agent](39_DO_AN_DUOC_LAM_THE_NAO.md) | ✅ |
| 40 | [Làm được tới đâu, còn yếu ở đâu, hướng phát triển](40_LAM_DUOC_TOI_DAU.md) | ✅ |
| 41 | [Kể lại toàn bộ trong một phút, trong năm phút, và kịch bản chạy thử](41_KE_LAI_TOAN_BO.md) | ✅ |

## Phụ lục để tra

| | Phụ lục | |
|---|---|---|
| A | [Mọi tham số cấu hình: giá trị đang chạy, dùng để làm gì, bài nào giảng](PL_A_THAM_SO.md) | ✅ |
| B | [Mọi tính năng đang mở và đang tắt: làm gì, một con số, bài nào giảng](PL_B_TINH_NANG.md) | ✅ |
| C | [Sổ mọi phép so sánh đã làm, kể cả phương án bị bỏ: 166 phép so gom từ các bài](PL_C_SO_PHEP_SO.md) | ✅ |
| D | [Lời dặn gửi model và mô tả từng công cụ, chép nguyên văn từ chương trình](PL_D_LOI_DAN.md) | ✅ |
| E | [Thuật ngữ Việt – Anh: 218 từ, có bảng tra ngược Anh – Việt](PL_E_THUAT_NGU.md) | ✅ |
| F | [Các con số chính trên một trang: 108 con số kèm điều kiện đo](PL_F_CON_SO_CHINH.md) | ✅ |
| G | [Mọi quyết định của hệ thống trên một trang: 296 quyết định gom từ bài 1–38](PL_G_MOI_QUYET_DINH.md) | ✅ |
| H | [Mọi tình huống hỏng trên một trang: 152 tình huống gom từ bài 1–38](PL_H_MOI_TINH_HUONG_HONG.md) | ✅ |
| I | [Mọi giới hạn đã biết trên một trang: 147 giới hạn, và bảng riêng các thứ cố ý không làm](PL_I_GIOI_HAN_DA_BIET.md) | ✅ |

## Khuôn của mỗi bài

**Nửa để hiểu**

1. **Tên bài** là một câu hỏi hoặc một câu khẳng định.
2. **Dòng cập nhật:** viết lúc nào, số lấy từ đâu.
3. **Nối mạch:** "Bài trước đã biết… Bài này thêm…".
4. **Ý chính:** 3–5 gạch; đọc riêng mục này cũng nắm được bài.
5. **Từ dùng trong bài:** chỉ các từ mới của bài; tên dùng trong bài · tên gốc tiếng Anh · nghĩa.
6. **Thân bài:** 3–5 mục, tên mỗi mục là một câu khẳng định (đọc riêng các tên mục là ra dàn ý của bài). Nói thẳng cơ chế, không dùng ẩn dụ; ví dụ lấy từ lượt chạy thật; mỗi hình tối đa 6 ô.
7. **Quyết định và lý do:** mỗi quyết định thiết kế của phần này viết thành một câu hỏi "Vì sao…?". Mở bằng hai ba câu kể tình huống bằng lời thường (giảng luôn khái niệm mới nếu có), rồi chốt bằng bốn gạch: **đã chọn** gì · **vì sao** · **cách khác** (ghi rõ là "đã đo", "chưa thử" hay "quyết định đã ghi") · **cái giá** phải trả cho lựa chọn đó. Chỗ nào không tìm thấy lý do được ghi lại thì viết đúng một dạng: "chưa thấy ghi lý do; điều thấy được là…", không thêm câu đoán. Mỗi bài giữ bốn tới sáu quyết định quan trọng ở đây; quyết định nhỏ nằm ở nửa để tra. Chỉ viết về thứ hệ thống thật sự có. Có ba loại câu hỏi: *vì sao đặt ở đây* (việc này làm ở máy chủ hay ở giao diện; chương trình làm hay giao cho model; tính sẵn hay tính lúc hỏi) · *vì sao làm cách này* (gọi thẳng hay xếp hàng chờ; một lần hay nhiều lần; tự viết hay dùng đồ có sẵn) · *vì sao là con số này*.
8. **Nếu… thì sao:** kể trọn một tình huống, rồi một bảng ngắn các tình huống đáng nhớ nhất (nếu · người dùng thấy gì · muốn hết lỗi thì ai làm gì); bảng đủ nằm ở nửa để tra. Hai loại tình huống. *Khi có thứ hỏng:* dịch vụ bên ngoài sập hoặc chậm, quá hạn giờ, dữ liệu lệch nhau, người dùng làm điều không ngờ. *Khi điều kiện đổi:* kho lớn gấp mười, nhiều người dùng cùng lúc, đổi model. Mỗi tình huống ghi: hệ thống làm gì · người dùng thấy gì · đã có hay chưa có. Chỗ nào chưa xử lý thì ghi thẳng "chưa có". Lời báo cho người dùng chép nguyên văn từ chương trình; tình huống nào chưa được thử thật thì ghi rõ là đọc từ chương trình.
9. **Dễ nhầm:** 1–3 câu người mới hay nói, kèm câu sửa.
10. **Câu hỏi tự kiểm** (anh chọn thêm trưa 22/11): khoảng 4 câu kiểu "vì sao…", "nếu… thì sao", đáp án một hai câu, gập lại, bấm mới hiện. Mục này thay cho mục "Những điều cần nhớ" của khuôn cũ (nó lặp lại "Ý chính").

**Luật về độ dài** (anh duyệt trưa 22/11, sau khi đọc bài 6): nửa để hiểu không nói một điều hai lần. Đoạn dẫn trước một quyết định chỉ có khi phải giảng một khái niệm mới; bảng chi tiết nằm ở nửa để tra; "Dễ nhầm" nhiều nhất 3 gạch. Không bỏ: mục giảng nền, đủ bốn gạch của mỗi quyết định, bảng tình huống hỏng.

**Nửa để tra** (bài nào có mục nào thì ghi mục đó; bài nền thường chỉ có hai mục cuối)

*Hai mục 7 và 8 thêm trưa 22/11/2026 theo yêu cầu của anh: đọc xong phải giải thích được từng quyết định và nói được "hỏng thì sao", không chỉ kể được hệ thống gồm những gì. Mục "Vì sao không làm cách khác" của khuôn cũ nhập vào mục 7. **Bài 6 (kiến trúc) là bài mẫu đầu tiên theo khuôn mới**; anh đã đọc và duyệt trưa 22/11. Mọi bài từ 1 tới 40 đã theo khuôn này; bài 41 (kể lại và kịch bản chạy thử) có cấu trúc riêng.*

11. **Cấu hình đang chạy:** bảng mục · giá trị · dùng để làm gì và vì sao là giá trị đó · đã thử giá trị khác chưa.
12. **Đã so:** vấn đề thật đã gặp · so cái gì với cái gì, trên bộ câu nào · bảng kết quả kể cả phương án bị bỏ · đọc bảng thế nào · đã chọn gì · giới hạn của phép đo. Mỗi con số ghi rõ đo với model viết nào.
    Bài nào giảng lời dặn thì có thêm bảng **lời dặn**: từng phần, một câu nguyên văn.
13. **Giới hạn đã biết:** chỗ hệ thống còn yếu, kèm con số.
14. **Chi tiết để tra:** con số phụ, ngoại lệ, ngày đo.
15. **Bài sau.**
16. **Nguồn** (thu gọn, anh không cần đọc): mỗi con số và mỗi khẳng định trỏ về file code hoặc file số đo.

Luật viết: thân bài không có tên file, tên hàm, mã bản code, ngày giờ phép thử, tên phiên làm việc. Mỗi chữ "vì" trong bài phải có căn cứ ở code, ở số đo hoặc ở một quyết định đã ghi; không có thì viết "chưa rõ vì sao". Mỗi con số đi kèm thứ nó đếm và mốc để so.

## Bộ bài cũ

Bộ 27 bài ở thư mục [`bai_hoc/`](../README.md), trang [Việc mới xong](../VIEC_MOI_XONG.md) và trang bản đồ dự án là hồ sơ cũ: giữ nguyên để tra, không ai ghi thêm từ chiều 22/11. Bộ giáo trình này là chỗ đọc duy nhất; thứ gì mới đều vào đây, và được liệt kê ở mục "Có gì mới" đầu trang.

<details>
<summary>Nguồn (để giữ trang đúng — anh không cần đọc)</summary>

- Bốn câu anh trả lời sáng 22/11/2026 (mức nền: ba bài nền ngắn · bốn chỗ vướng của bộ cũ: không ghép được bức tranh, quá nhiều chi tiết thi công, thiếu cấu hình và kết quả so sánh, ẩn dụ che cơ chế · nhịp giao: viết tiếp theo chặng · bài mẫu thứ ba: harness): ghi chép riêng của phiên viết giáo trình.
- Năm ví dụ: sổ ghi từng lượt của hệ thống trên máy phát triển, các ngày 20–21/11/2026 [đã chạy; người viết không chạy lại]; bản sao riêng tư ở `data/hoc_cung_D/vi_du_*_vet.json`. "Kho không nói về chỗ đậu xe ở chùa Thiên Mụ": dò bằng `scripts/grep_kb.sh` ngày 22/11/2026. "Kho có câu về giày dép": biên bản kiểm độc lập `data/hoc_cung_D/kiem/bai_02_10.md`.
- Model viết: hệ thống đang chạy Claude Sonnet 5.5 (đổi tạm từ 21/11/2026); phần lớn phép so cũ đo với gpt-6-luna. Mỗi bài ghi rõ con số nào đo với model nào.
- Luật nội dung: `session_prompt/WORKFLOW.md` mục 6 và mục 10.
- Mục "Có gì mới" và việc bộ cũ đứng yên: lời anh lúc 16:28 ngày 22/11/2026 ("những gì mới sẽ ở giáo trình"), ghi ở `session_prompt/HIEN_TRANG.md` mục 4. Dòng Hải Vân Quan: phiếu của phiên điều phối tối 22/11 (nguồn ở bài 7). Bốn dòng của sáng 23/11/2026 chép từ các bài 5, 16, 23, 24, 27, 30, 33, 34, 35, 38, 40, 41 bản 11:10–11:17 23/11 (mục ghi ở cột "Đọc ở"); đọc lại câu của bài gốc trước khi viết, không thêm sự thật mới. Bốn dòng của chiều 22/11 chép từ mục 44 của `bai_hoc/VIEC_MOI_XONG.md` (mục cuối của bộ cũ; phiên đo đã nhìn cả bốn thứ trên trình duyệt lúc 16:17–16:20 ngày 22/11; riêng dòng giữ chữ mới nhìn ở lượt thường, ca phải viết lại chưa trúng lần nào) [đã chạy, phiên khác].

</details>
