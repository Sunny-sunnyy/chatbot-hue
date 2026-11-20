# Nghiên cứu và inventory nội dung vé du lịch Huế

## Mục đích tài liệu

Tài liệu này khóa phạm vi, danh sách file và thành phần nội dung cần biên soạn
cho nhánh `knowledge-base-hue/travel/tickets/`. Đây là tài liệu điều phối giữa
reviewer và implementer, không phải bảng giá trực tiếp dành cho người dùng.

Inventory được xây dựng cho các nhu cầu: giá vé tham quan Huế, vé Đại Nội và
lăng tẩm, vé gộp di tích, phí tham quan Hải Vân Quan, vé xem nghệ thuật, Ca Huế
trên sông Hương, thuyền rồng và giá vào các điểm hoặc trải nghiệm du lịch khác.

Mốc nghiên cứu và kiểm tra thông tin hiện hành: **07/09/2026**.

## Trạng thái quyết định

- Đã chốt **05 file nội dung về vé**.
- Tên file dùng tiếng Việt tự nhiên, có dấu và khoảng trắng; H1 phải thống nhất
  với tên file đã duyệt.
- Giá vé và chính sách thuộc một điểm hoặc một hệ thống vé chỉ có một nơi
  canonical trong nhánh `tickets`.
- `services/Chi phí du lịch Huế.md` được dùng giá vé như một đầu vào để lập
  ngân sách, nhưng không duy trì lại bảng giá và chính sách chi tiết.
- Hải Vân Quan được tách khỏi Quần thể Di tích Cố đô Huế vì có văn bản thu phí,
  thời hạn áp dụng và điều kiện miễn giảm riêng.
- Vé chương trình biểu diễn và dịch vụ thuyền phải phân biệt giá do cơ quan hoặc
  đơn vị tổ chức trực tiếp công bố với giá bán của từng nhà cung cấp thương mại.
- Không tạo file riêng cho từng lăng, từng combo, từng suất diễn hoặc từng nhà
  bán vé nếu các mục đó cùng thuộc một hệ thống vé.
- Hai file khung rỗng `heritage-ticket-prices.md` và `ticket-types.md` không phải
  tên canonical đã chốt và đã được xóa ngày 07/09/2026. Không tạo lại hoặc duy
  trì song song với 05 file answer-facing đã duyệt.
- Inventory này chỉ khóa thiết kế. Việc biên soạn 05 file nội dung phải được
  giao và review ở bước triển khai riêng.

## Danh sách 05 file đã chốt

1. `Hướng dẫn mua và sử dụng vé du lịch Huế.md`
2. `Vé tham quan Quần thể Di tích Cố đô Huế.md`
3. `Vé tham quan Hải Vân Quan.md`
4. `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`
5. `Vé các điểm tham quan và trải nghiệm khác ở Huế.md`

## Ranh giới với `services/Chi phí du lịch Huế.md`

Hai nhánh phối hợp theo mô hình **ngân sách tổng hợp → dữ liệu vé canonical**:

- `services/Chi phí du lịch Huế.md` hướng dẫn tính tổng chi phí chuyến đi, gồm
  vận chuyển đến Huế, đi lại tại Huế, lưu trú, ăn uống, tham quan, trải nghiệm,
  mua sắm và dự phòng;
- file đó có thể minh họa tổng ngân sách vé theo một lịch trình hoặc nhóm nhu
  cầu, nhưng phải ghi ngày khảo sát và dẫn người đọc sang nhánh `tickets`;
- `tickets` giữ mức tiền cụ thể, loại vé, đối tượng, điều kiện miễn giảm, thời
  hạn sử dụng, thành phần bao gồm hoặc không bao gồm và kênh mua;
- khi giá vé thay đổi, chỉ cập nhật dữ liệu canonical trong `tickets`; mọi con
  số minh họa trong guide chi phí phải được rà lại theo nguồn canonical;
- các bài “chi phí du lịch Huế”, “ăn chơi Huế 3 ngày 2 đêm hết bao nhiêu” và
  “kinh nghiệm du lịch tiết kiệm” là nguồn nghiên cứu chính của `services`,
  không phải nguồn pháp lý để khóa giá vé.

Nhánh `tickets` không tính giá phòng, vé máy bay hoặc tàu xe đến Huế, chi phí ăn
uống, thuê xe tự lái, mua sắm, tiền công hướng dẫn viên hay tổng giá tour trọn
gói. Một sản phẩm tour chỉ được nhắc để giải thích rằng giá tour khác vé vào
cổng và phải nêu rõ thành phần bao gồm.

## Ranh giới với các domain khác

- Lịch sử, kiến trúc và giá trị của Đại Nội, lăng tẩm và Hải Vân Quan thuộc các
  file canonical trong `heritages/`; `tickets` chỉ giữ thông tin vào cửa và sử
  dụng vé.
- Nội dung nghệ thuật của Nhã nhạc, Ca Huế và chương trình Duyệt Thị Đường thuộc
  `performing_arts/`; `tickets` chỉ giữ giá, suất, đối tượng và điều kiện mua.
- Mô tả Vườn quốc gia Bạch Mã, Bạch Mã Village và Không gian lưu niệm Lê Bá
  Đảng thuộc entity du lịch tương ứng; `tickets` không sao chép bài giới thiệu.
- Lịch trình thuộc `services`; file vé không đề xuất hành trình đầy đủ ngoài
  việc giải thích combo nào phù hợp với số điểm và thời hạn sử dụng.

## Thành phần của từng file

### 1. `Hướng dẫn mua và sử dụng vé du lịch Huế.md`

Đây là guide tổng quan cho người chưa biết Huế có những loại vé nào và nên mua
ở đâu. File không thay thế bảng giá chuyên biệt trong bốn file còn lại.

Thành phần bắt buộc:

- phân biệt vé lẻ, vé tuyến gộp, vé tất cả điểm, vé suất diễn, vé khách lẻ,
  thuê nguyên thuyền, vé vào cổng và gói trải nghiệm;
- phân biệt phí nhà nước quy định, giá do đơn vị vận hành công bố, giá niêm yết
  của doanh nghiệp và giá khuyến mại của đại lý;
- các kênh mua chính thức, gồm quầy vé trực tiếp và cổng vé điện tử khi đang
  hoạt động;
- cách kiểm tra đúng tên điểm, ngày sử dụng, số người, nhóm tuổi và giấy tờ cần
  xuất trình trước khi thanh toán;
- cách đọc điều kiện hiệu lực, số lần vào, thành phần bao gồm, phụ thu, đổi hoặc
  hoàn vé;
- lưu ý rằng ngưỡng trẻ em có thể theo tuổi hoặc chiều cao và không đồng nhất
  giữa các điểm;
- cách nhận biết tour, combo của đại lý hoặc thuê thuyền riêng không phải vé vào
  cửa do cơ quan quản lý phát hành;
- quy trình kiểm tra lại giá và lịch vận hành sát ngày đi;
- liên kết tới bốn file giá vé chuyên biệt và `services/Chi phí du lịch Huế.md`.

Không tạo một bảng tổng hợp sao chép toàn bộ giá từ bốn file còn lại. Các ví dụ
chỉ nhằm giải thích loại vé và phải dẫn về file canonical.

### 2. `Vé tham quan Quần thể Di tích Cố đô Huế.md`

File này giữ toàn bộ hệ thống phí theo Nghị quyết 55/2025/NQ-HĐND và cổng bán vé
của Trung tâm Bảo tồn Di tích Cố đô Huế.

Thành phần bắt buộc:

- căn cứ pháp lý, ngày ban hành, ngày có hiệu lực và trạng thái hiệu lực được
  kiểm tra tại thời điểm biên soạn;
- giá vé lẻ người lớn và trẻ em từ 7–12 tuổi;
- phạm vi từng nhóm giá: Đại Nội; các lăng Minh Mạng, Tự Đức, Khải Định; lăng
  Gia Long; lăng Đồng Khánh; nhóm Thiệu Trị, Bảo tàng Cổ vật Cung đình Huế,
  điện Hòn Chén, cung An Định, đàn Nam Giao và lăng Dục Đức;
- ba tuyến gộp 02 điểm, ba tuyến gộp 03 điểm, tuyến gộp 04 điểm và tuyến gộp
  tất cả các điểm;
- thời hạn tối đa 02 ngày của tuyến 04 điểm và 05 ngày của tuyến tất cả điểm;
- các nhóm miễn phí, giảm 50%, ngày miễn phí cho công dân Việt Nam và giấy tờ
  chứng minh tương ứng;
- nguyên tắc áp dụng thống nhất cho khách Việt Nam và khách quốc tế;
- kênh mua vé trực tiếp và cổng e-ticket chính thức;
- cách chọn vé lẻ hay vé gộp dựa trên đúng danh sách điểm, không chỉ dựa vào
  phép cộng giá;
- cảnh báo không gọi vé 530.000 đồng là “vé tất cả di tích”.

Baseline pháp lý tại ngày 06/09/2026:

- Đại Nội: 200.000 đồng/người lớn, 40.000 đồng/trẻ em;
- Minh Mạng, Tự Đức hoặc Khải Định: 150.000 đồng/người lớn,
  30.000 đồng/trẻ em;
- Gia Long: 150.000 đồng/người lớn, trẻ em miễn phí;
- Đồng Khánh: 100.000 đồng/người lớn, trẻ em miễn phí;
- nhóm điểm 50.000 đồng: trẻ em miễn phí;
- tuyến gộp 04 điểm: 530.000 đồng/người lớn, 100.000 đồng/trẻ em;
- tuyến gộp tất cả điểm: 600.000 đồng/người lớn, 120.000 đồng/trẻ em.

Implementer phải đọc toàn văn nghị quyết thay vì chỉ sao chép baseline trên.

### 3. `Vé tham quan Hải Vân Quan.md`

File này độc lập vì Hải Vân Quan có cơ chế phối hợp quản lý và biểu phí riêng.

Thành phần bắt buộc:

- Nghị quyết 05/2026/NQ-HĐND, ngày ban hành 22/05/2026, hiệu lực từ 02/06/2026
  và thời hạn áp dụng đến hết 31/12/2028;
- mức phí 70.000 đồng/người/lượt, áp dụng thống nhất cho khách Việt Nam và khách
  quốc tế;
- trẻ em dưới 13 tuổi và các đối tượng miễn phí khác;
- các nhóm giảm 50%, gồm điều kiện áp dụng cho người dân thành phố Huế và thành
  phố Đà Nẵng theo đúng văn bản;
- các ngày miễn phí và phạm vi đối tượng hưởng miễn phí;
- địa điểm hoặc kênh mua vé được đơn vị quản lý xác nhận tại thời điểm viết;
- cảnh báo không áp dụng ngưỡng trẻ em 7–12 tuổi của vé di tích Huế cho Hải Vân
  Quan;
- cảnh báo thời hạn của chính sách và yêu cầu nghiên cứu văn bản thay thế khi
  biên soạn hoặc cập nhật sau năm 2028.

Không gộp vé Hải Vân Quan vào vé tất cả điểm của Quần thể Di tích Cố đô Huế khi
không có căn cứ từ cơ quan phát hành.

### 4. `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`

File này điều phối các khoản tiền để xem chương trình biểu diễn hoặc tham gia
trải nghiệm bằng thuyền trên sông Hương. Nó không phải danh bạ hãng thuyền.

Thành phần bắt buộc:

- vé chương trình Nhã nhạc, múa cung đình và Tuồng cung đình tại Nhà hát Duyệt
  Thị Đường;
- chương trình Đại Nhạc miễn phí tại Thế Miếu nếu còn hoạt động theo lịch được
  đơn vị tổ chức xác nhận;
- vé khách lẻ nghe Ca Huế, suất diễn, địa điểm bán vé tập trung và yêu cầu niêm
  yết giá;
- sự khác nhau giữa vé khách lẻ, thuê nguyên thuyền, thuyền đơn, thuyền đôi,
  gói ăn tối, gói thả hoa đăng và các tuyến du ngoạn;
- tên đơn vị trực tiếp tổ chức hoặc bán dịch vụ, ngày kiểm tra, giá niêm yết và
  điều kiện áp dụng cho từng mức giá thương mại;
- thành phần bao gồm và không bao gồm trong từng loại sản phẩm;
- quy định về trẻ em theo tuổi hoặc chiều cao của đúng đơn vị cung cấp;
- thời lượng, giờ tập trung và suất hoạt động chỉ được ghi sau khi xác minh sát
  thời điểm biên soạn;
- cảnh báo không trình bày giá của một website bán thuyền như mức giá chung của
  toàn bộ Ca Huế trên sông Hương.

Baseline nghiên cứu hiện có: website Nhà hát Nghệ thuật Truyền thống Cung đình
Huế công bố 300.000 đồng/người/suất tại Duyệt Thị Đường nhưng trang hiển thị mốc
cập nhật 12/12/2024. Con số này phải được kiểm tra lại trước khi khóa trong file
answer-facing.

### 5. `Vé các điểm tham quan và trải nghiệm khác ở Huế.md`

File này bao phủ các khoản vé không thuộc bốn hệ thống phía trên nhưng đủ nhu
cầu tìm kiếm và có nguồn trực tiếp có thể kiểm tra.

Ứng viên đợt đầu:

- vé vào Vườn quốc gia Bạch Mã và các dịch vụ nội bộ do đơn vị quản lý công bố;
- vé hoặc gói tại Bạch Mã Village;
- vé Không gian lưu niệm Lê Bá Đảng;
- xe điện, thuyết minh tự động, thực tế ảo và dịch vụ tham quan bổ sung trong
  Đại Nội, nếu đơn vị vận hành hiện hành công bố rõ;
- thuyền điện hoặc trải nghiệm mới trên sông Ngự Hà khi đã xác minh đơn vị vận
  hành, tình trạng khai thác và giá chính thức.

Mỗi mục bắt buộc có:

- tên chính xác của điểm hoặc trải nghiệm;
- chủ thể công bố giá và phân loại nguồn;
- giá niêm yết, đơn vị tính và ngày kiểm tra;
- nhóm khách, điều kiện miễn giảm hoặc giá đoàn;
- thành phần bao gồm và các khoản chưa bao gồm;
- cách mua hoặc thông tin liên hệ chính thức;
- địa chỉ theo đơn vị hành chính hiện hành nếu cần chỉ đường;
- cảnh báo xác minh lại đối với giá thương mại hoặc dịch vụ theo mùa.

Không đưa một ứng viên vào chỉ vì blog du lịch có bảng giá. Nếu chưa tìm được
nguồn trực tiếp, giữ ứng viên trong evidence record và chưa khóa giá trong nội
dung trả lời người dùng.

## Mô hình dữ liệu bắt buộc cho một khoản vé

Mọi mức giá trong bốn file chuyên biệt phải xác định được các trường sau:

- `tên vé hoặc dịch vụ`;
- `điểm/chương trình áp dụng`;
- `đối tượng`;
- `mức tiền` và `đơn vị tính`;
- `bao gồm` và `không bao gồm`;
- `điều kiện áp dụng`;
- `thời hạn sử dụng` nếu có;
- `kênh mua hoặc nơi niêm yết`;
- `chủ thể công bố`;
- `loại nguồn`;
- `ngày ban hành hoặc ngày cập nhật`;
- `ngày truy cập và kiểm tra`;
- `trạng thái hiệu lực`;
- `mâu thuẫn nguồn hoặc lưu ý độ tin cậy`.

Không được lưu một con số giá đứng riêng mà thiếu đối tượng, đơn vị tính hoặc
phạm vi bao gồm. “Vé trẻ em” phải ghi rõ được xác định theo tuổi, chiều cao hay
quy định riêng của điểm.

## Thứ bậc nguồn và quy tắc khóa giá

### Cấp 1 — nguồn có thẩm quyền

- văn bản quy phạm pháp luật, nghị quyết HĐND và văn bản của UBND;
- cổng chính thức của cơ quan quản lý di tích;
- website hoặc quầy niêm yết của đơn vị trực tiếp vận hành điểm, chương trình
  hoặc dịch vụ;
- cổng bán vé điện tử do chính đơn vị phát hành vận hành.

Nguồn cấp 1 được dùng để khóa giá, nhưng vẫn phải kiểm tra ngày hiệu lực. Website
chính thức của một đơn vị có thể chưa cập nhật địa chỉ hành chính hoặc lịch hoạt
động mới nhất; không mặc định mọi claim trên cùng trang đều hiện hành.

### Cấp 2 — nguồn đối chiếu

- Sở Du lịch, VisitHue, Khám Phá Huế và cổng thông tin địa phương;
- báo chí có quy trình biên tập;
- website của khách sạn hoặc doanh nghiệp lớn có ngày cập nhật và dẫn nguồn.

Nguồn cấp 2 hỗ trợ phát hiện thay đổi và diễn giải, nhưng không thay văn bản pháp
lý hoặc nguồn trực tiếp khi các nguồn này tồn tại.

### Cấp 3 — nguồn thương mại và phát hiện ứng viên

- đại lý vé, hãng lữ hành, website thuê thuyền và trang bán tour;
- blog SEO, toplist và bài tổng hợp giá;
- nền tảng đặt dịch vụ có giá khuyến mại theo phiên truy cập.

Nguồn cấp 3 có thể khóa **giá của chính nhà cung cấp đó** nếu trang nêu rõ sản
phẩm và điều kiện, nhưng không được suy thành giá chính thức hoặc giá chung của
toàn thị trường. Với giá vào cửa do cơ quan nhà nước quy định, nguồn cấp 3 chỉ
dùng để phát hiện mâu thuẫn.

### Quy trình cho dữ liệu động

1. Xác định chủ thể có quyền ban hành hoặc niêm yết giá.
2. Tìm nguồn trực tiếp bằng truy vấn tiếng Việt.
3. Kiểm tra ngày ban hành, ngày hiệu lực, thời hạn và văn bản thay thế.
4. Đối chiếu cổng bán vé hoặc thông báo vận hành hiện tại.
5. So sánh ít nhất một nguồn độc lập nếu giá có ảnh hưởng đáng kể tới ngân sách.
6. Ghi ngày kiểm tra và điều kiện của mức giá trong evidence record.
7. Nếu chưa xác minh được, không đoán và không gắn nhãn “giá vé 2026”.

## Baseline pháp lý và nguồn ưu tiên

### Quần thể Di tích Cố đô Huế

- [Sở Tư pháp thành phố Huế — nội dung Nghị quyết 55/2025/NQ-HĐND](https://stp.hue.gov.vn/van-ban-phap-luat/muc-thu-che-do-thu-nop-quan-ly-va-su-dung-phi-tham-quan-di-tich-lich-su-van-hoa-hue-thuoc-quan-the-di-tich-co-do-hue.html)
- [Toàn văn Nghị quyết 55/2025/NQ-HĐND](https://hue.gov.vn/Portals/0/Uploads/VBPL/Nam2026/Thang1/000.00.00.K57-55-2025-NQ-HDND-2025-PL1.pdf)
- [Cổng vé điện tử Trung tâm Bảo tồn Di tích Cố đô Huế](https://eticket.hueworldheritage.org.vn/chon-ve)

### Hải Vân Quan

- [Hồ sơ Nghị quyết 05/2026/NQ-HĐND](https://hue.gov.vn/Trang-chu/He-thong-van-ban-phap-luat/tp/7/vb/59037)
- [Toàn văn Nghị quyết 05/2026/NQ-HĐND](https://hue.gov.vn/Portals/0/Uploads/VBPL/Nam2026/Thang6/000.00.00.K57-05-2026-NQ-HDND-2026-PL1.pdf)

### Nghệ thuật và sông Hương

- [Nhà hát Nghệ thuật Truyền thống Cung đình Huế](https://nhanhac.com.vn/)
- [Quy chế quản lý và tổ chức biểu diễn Ca Huế](https://stp.hue.gov.vn/van-ban-phap-luat/tinh-thua-thien-hue-ban-hanh-quy-che-quan-ly-va-to-chuc-hoat-dong-bieu-dien-ca-hue-tren-dia-ban-tinh.html)
- [Ca Huế trên sông Hương — nguồn nhà cung cấp](https://cahuetrensonghuong.com/)
- [Thuyền Rồng Huế — giá vé Ca Huế của nhà cung cấp](https://thuyenronghue.com/gia-ve-ca-hue)
- [Thuyền Rồng Huế — bảng giá dịch vụ của nhà cung cấp](https://thuyenronghue.com/bang-gia-dich-vu-thuyen-rong-hue-tren-song-huong-khuyen-mai.html)

### Các điểm và trải nghiệm khác

- [Không gian lưu niệm Lê Bá Đảng — chính sách vé](https://lebadangmemoryspace.com/language/vi/lien-he/)
- [AEON MALL Huế — thông tin tham khảo Vườn quốc gia Bạch Mã](https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/vuon-quoc-gia-bach-ma-hue.html)
- [Klook — thông tin tham khảo Bạch Mã Village](https://www.klook.com/vi/blog/bach-ma-village/)

## Mâu thuẫn và cảnh báo phát hiện trong nghiên cứu

- Nghị quyết 55/2025/NQ-HĐND xác định 530.000 đồng là tuyến gộp 04 điểm, còn
  tuyến tất cả điểm là 600.000 đồng. Một số bài thương mại gọi sai vé 530.000
  đồng là vé tất cả di tích.
- Trẻ em của hệ thống di tích Huế là nhóm 7–12 tuổi, trong khi Hải Vân Quan miễn
  phí cho trẻ dưới 13 tuổi. Không được tạo một quy tắc trẻ em chung cho cả Huế.
- Bài giá vé của Huế Tourism được cập nhật tháng 12/2023; dùng làm lịch sử hoặc
  đối chiếu, không dùng thay Nghị quyết có hiệu lực năm 2026.
- Một số trang thuyền rồng tự ghi “mới nhất 2026” trên bài có ngày xuất bản từ
  năm 2021. Nhãn năm trong tiêu đề không chứng minh giá còn hiệu lực.
- Các nhà cung cấp Ca Huế công bố các mức giá khác nhau. Điều này phù hợp với mô
  hình doanh nghiệp đăng ký và niêm yết giá, không phải bằng chứng rằng một trang
  đúng còn trang khác sai.
- Giá Vườn quốc gia Bạch Mã trong các nguồn đang dao động 60.000–65.000 đồng cho
  người lớn. Chưa khóa mức giá cho tới khi có công bố trực tiếp hiện hành của
  đơn vị quản lý.
- Website chính thức của Không gian lưu niệm Lê Bá Đảng công bố giá vé nhưng vẫn
  dùng địa chỉ `xã Thủy Bằng, thị xã Hương Thủy, tỉnh Thừa Thiên Huế`. Giá và địa
  chỉ là hai claim phải được xác minh độc lập.
- Trang dịch vụ trong Đại Nội của HueCIT hữu ích để phát hiện xe điện, chụp ảnh,
  thuyết minh hoặc trải nghiệm thực tế ảo, nhưng dữ liệu cũ không đủ để khóa giá
  hiện hành.
- Dữ liệu `_source-dumps` có tiêu đề “giá vé tham quan” nhưng các trường
  `total`, `soVeDon`, `soVeTuyen` phản ánh giao dịch hoặc số lượng vé, không phải
  bảng giá công bố. Không suy giá vé từ các bản ghi này.

## Địa chỉ hành chính hiện hành

Từ ngày 01/07/2025, thành phố Huế vận hành 40 đơn vị hành chính cấp xã sau sắp
xếp. Mọi địa chỉ trong nội dung triển khai phải dùng mô hình hiện hành:
`[số nhà/đường/thôn], [phường hoặc xã], thành phố Huế`; không chèn quận, huyện,
thị xã hoặc tỉnh Thừa Thiên Huế cũ như thành phần của địa chỉ hiện hành.

Nguồn nền bắt buộc:
[Nghị quyết 1675/NQ-UBTVQH15](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-1675-nq-ubtvqh15-sap-xep-cac-dvhc-cap-xa-cua-thanh-pho-hue-nam-2025-119250616195617897.htm).

Không suy địa chỉ mới chỉ từ tên đường hoặc từ nhãn “cập nhật 2026”. Với một
điểm nằm gần ranh giới đơn vị hành chính, phải đối chiếu tọa độ hoặc vị trí thực
tế với nguồn chính thức. Nếu file chỉ giải thích giá và không cần chỉ đường,
không thêm địa chỉ chưa được xác minh.

## Danh mục URL do chủ dự án cung cấp đã đọc hoặc đối chiếu

### Vé di tích, Đại Nội, lăng tẩm và combo

- [Sở Tư pháp — mức thu phí tham quan di tích](https://stp.hue.gov.vn/van-ban-phap-luat/muc-thu-che-do-thu-nop-quan-ly-va-su-dung-phi-tham-quan-di-tich-lich-su-van-hoa-hue-thuoc-quan-the-di-tich-co-do-hue.html)
- [Cơ sở dữ liệu văn bản pháp luật](https://vbpl.vn/thuathienhue/Pages/vbpq-toanvan.aspx?ItemID=185769&Keyword=)
- [Cổng e-ticket di sản Huế](https://eticket.hueworldheritage.org.vn/chon-ve)
- [Cổng thông tin Huế — Hue Monuments Complex](https://hue.gov.vn/en-us/Home/Tourism/Details/tb/Hue-Monuments-Complex-721558)
- [Huế Tourism — giá vé tham quan di tích](https://huetourism.gov.vn/gia-ve-tham-quan-cac-diem-di-tich-tai-tinh-thua-thien-hue/?pid=MjMwNjB8Y3NkbGRs0)
- [Đại Việt Tourist — bảng giá tham khảo](https://daivietourist.vn/gia-ve-tham-quan-hue/)
- [Huế City Tour — bảng giá tham khảo](https://huecitytour.com/bang-gia-ve-tham-quan-hue.html)
- [Homestay Huế — bảng giá tham khảo 2026](https://homestayhue.com.vn/tin-tuc/bang-gia-ve-tham-quan-hue-2026-cap-nhat-moi-day-du-nhat)
- [Mường Thanh — tổng hợp giá vé tham quan](https://booking.muongthanh.com/tin-tuc/tong-hop-gia-ve-tham-quan-hue)
- [Thế Giới Di Động — cẩm nang tham quan Đại Nội](https://www.thegioididong.com/hoi-dap/cam-nang-tham-quan-dai-noi-hue-gia-ve-va-so-do-1591885)

URL `vbpl.vn` đã trả lỗi khi kiểm tra bằng công cụ nghiên cứu. Implementer phải
tìm lại văn bản theo số hiệu thay vì coi URL lỗi là bằng chứng duy nhất.

### Hải Vân Quan

- [Cổng thông tin thành phố Huế — Nghị quyết 05/2026/NQ-HĐND](https://hue.gov.vn/Trang-chu/He-thong-van-ban-phap-luat/tp/7/vb/59037)

### Nghệ thuật, Ca Huế và thuyền rồng

- [Nhà hát Nghệ thuật Truyền thống Cung đình Huế](https://nhanhac.com.vn/)
- [Ca Huế trên sông Hương](https://cahuetrensonghuong.com/)
- [Thuyền Rồng Huế — giá vé Ca Huế](https://thuyenronghue.com/gia-ve-ca-hue)
- [Thuyền Rồng Huế — bài giá vé gắn nhãn mới nhất](https://thuyenronghue.com/bang-gia-ve-ca-hue-moi-nhat.html)
- [Thuyền Rồng Huế — bảng giá dịch vụ](https://thuyenronghue.com/bang-gia-dich-vu-thuyen-rong-hue-tren-song-huong-khuyen-mai.html)
- [Khám Phá Huế bản cũ — giá dịch vụ trong Đại Nội](https://kph2022.huecit.com/Du-lich/Chi-tiet/tid/Gia-cac-dich-vu-trong-Dai-Noi.html/pid/7831/cid/195)

### Sinh thái, vui chơi và nghệ thuật

- [AEON MALL Huế — Vườn quốc gia Bạch Mã](https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/vuon-quoc-gia-bach-ma-hue.html)
- [Klook — Bạch Mã Village](https://www.klook.com/vi/blog/bach-ma-village/)
- [Không gian lưu niệm Lê Bá Đảng](https://lebadangmemoryspace.com/language/vi/lien-he/)

### Nguồn về tổng chi phí chuyến đi

Các nguồn dưới đây thuộc research set của `services/Chi phí du lịch Huế.md`.
Trong `tickets`, chúng chỉ dùng để phát hiện khoản vé hoặc mâu thuẫn cần quay về
nguồn trực tiếp:

- [Thế Giới Di Động — cẩm nang du lịch Huế tự túc](https://www.thegioididong.com/hoi-dap/du-lich-hue-cam-nang-tu-tuc-tu-a-z-1591265)
- [VinWonders — chi phí du lịch Huế](https://vinwonders.com/vi/wonderpedia/news/chi-phi-du-lich-hue/)
- [AEON MALL Huế — chi phí đi Huế](https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/chi-phi-di-hue.html)
- [Vui Ví Vu Đà Nẵng — chi phí ăn uống Huế 2026](https://vuivivudanang.vn/blogs/tin-tuc-hue/chi-phi-an-uong-hue-2026-an-gi-gia-bao-nhieu-cap-nhat-moi-nhat)
- [Vinpearl — chi phí du lịch Huế](https://vinpearl.com/vi/luu-ngay-chi-phi-du-lich-hue-va-bi-kip-de-co-chuyen-di-ngon-bo-re)
- [Khám Phá Huế — tour ẩm thực đặc sản buổi tối](https://khamphahue.com.vn/Du-lich/Chi-tiet/tid/Tour-Am-thuc-Dac-san-Hue-buoi-toi.html/pid/17251/cid/363)
- [Sovaba Travel — kinh nghiệm du lịch Huế tự túc](https://sovaba.travel/blog/bai-viet-kinh-nghiem-du-lich-hue-tu-tuc-meo-giup-chuyen-di-hoan-hao)
- [VnExpress — cẩm nang du lịch Huế](https://vnexpress.net/cam-nang-du-lich-hue-4126937.html)
- [Mường Thanh — kinh nghiệm du lịch Huế tự túc](https://booking.muongthanh.com/tin-tuc/kinh-nghiem-du-lich-hue-tu-tuc)
- [Review Đà Nẵng — kinh nghiệm du lịch Huế](https://reviewdanang.com.vn/diem-du-lich/kinh-nghiem-du-lich-hue.html)
- [Vi vu du hí — chi phí đi Huế 3 ngày 2 đêm](https://vivuduhi.com/chi-phi-di-hue-3-ngay-2-dem/)

## Thứ tự triển khai đề xuất

1. `Vé tham quan Quần thể Di tích Cố đô Huế.md`
2. `Vé tham quan Hải Vân Quan.md`
3. `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`
4. `Vé các điểm tham quan và trải nghiệm khác ở Huế.md`
5. `Hướng dẫn mua và sử dụng vé du lịch Huế.md`
6. Đối chiếu phần ngân sách tham quan–trải nghiệm trong
   `services/Chi phí du lịch Huế.md` để phát hiện chênh lệch. File services chỉ
   là tài liệu tham khảo trong đợt triển khai 05 file tickets; không sửa nếu
   handoff không cấp scope riêng.

Thứ tự này khóa các nguồn giá chuyên biệt trước, sau đó mới viết guide tổng hợp
và phép tính ngân sách. Guide mua vé và guide chi phí không được trở thành hai
bản sao của bảng giá.

## Tiêu chí nghiệm thu

- Chỉ có đúng 05 file nội dung vé đã duyệt.
- Mỗi hệ thống vé có một file canonical; không có bảng giá trùng nhau giữa
  `tickets`, `services`, `heritages` và `performing_arts`.
- Mọi mức giá có đối tượng, đơn vị tính, phạm vi bao gồm, nguồn và mốc thời gian.
- Phân biệt rõ phí nhà nước, giá đơn vị vận hành, giá nhà cung cấp, giá đại lý và
  tổng giá tour.
- Không dùng nhãn “2026” của bài SEO như bằng chứng về tính hiện hành.
- Không dùng địa chỉ hành chính cũ như địa chỉ hiện tại.
- Không suy một chính sách trẻ em, miễn giảm hoặc thời hạn vé cho điểm khác.
- Vé 530.000 đồng không bị mô tả sai thành vé tất cả di tích.
- Hải Vân Quan không bị gộp vào hệ thống vé Quần thể Di tích Cố đô Huế.
- Giá Ca Huế của một doanh nghiệp không bị trình bày thành giá chung.
- Mâu thuẫn chưa giải quyết như giá Vườn quốc gia Bạch Mã phải được ghi rõ hoặc
  loại khỏi nội dung, không chọn tùy ý một con số.
- `services/Chi phí du lịch Huế.md` dùng dữ liệu vé để tính ngân sách nhưng không
  sao chép toàn bộ chính sách và bảng giá.
- Inventory này được loại khỏi ingestion; chỉ 05 file nội dung đã triển khai mới
  là tài liệu phục vụ trả lời người dùng.

## Việc chưa thuộc phạm vi inventory này

- biên soạn hoàn chỉnh 05 file nội dung;
- viết hoàn chỉnh `services/Chi phí du lịch Huế.md`;
- tạo bảng giá cho mọi điểm vui chơi tư nhân ở thành phố Huế;
- lưu giá khuyến mại ngắn hạn hoặc giá được cá nhân hóa theo phiên đặt chỗ;
- sửa các file di sản, nghệ thuật biểu diễn hoặc du lịch đang được review ở
  session khác;
- tự động hóa việc theo dõi thay đổi giá hoặc hiệu lực văn bản.
