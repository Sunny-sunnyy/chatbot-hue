# Nghiên cứu và inventory nội dung hướng dẫn du lịch Huế

## Mục đích tài liệu

Tài liệu này khóa phạm vi, danh sách file và thành phần nội dung cần biên soạn
cho nhánh `knowledge-base-hue/travel/services/`. Đây là tài liệu điều phối giữa
reviewer và implementer, không phải bài hướng dẫn trực tiếp dành cho người dùng.

Inventory được chốt theo nhu cầu lập kế hoạch chuyến đi: lần đầu đến Huế nên đi
đâu, cách sắp xếp tham quan, lịch trình ngắn ngày và 3 ngày 2 đêm, cùng dự toán
chi phí. Cẩm nang tổng quan thuộc file `../places/travel_guides.md`; nhánh này không
được triển khai như danh bạ nhà cung cấp dịch vụ.

Mốc nghiên cứu và kiểm tra thông tin hiện hành: **07/09/2026**.

## Trạng thái quyết định

- Đã chốt **04 file nội dung hướng dẫn chuyên biệt**.
- Đã hoàn tất Taxonomy Migration sang cấu trúc mới:
  `knowledge-base-hue/travel/places/`, `knowledge-base-hue/travel/services/` và
  `knowledge-base-hue/travel/tickets/` theo xác nhận của người dùng.
- Tên file dùng tiếng Việt tự nhiên, có dấu và khoảng trắng; H1 phải thống nhất
  với tên file đã duyệt.
- `Cẩm nang du lịch Huế`, `Kinh nghiệm du lịch Huế tự túc` và `Hướng dẫn du
  lịch Huế từ A–Z` được xem là cùng một intent; file canonical duy nhất là
  `../places/travel_guides.md`, không tạo lại trong nhánh `services/`.
- `Lịch trình du lịch Huế 3 ngày 2 đêm` có nhu cầu độc lập đủ mạnh để tách file.
- Các lịch trình nửa ngày, 1 ngày và 2 ngày 1 đêm được gom trong một file ngắn
  ngày để tránh sinh nhiều biến thể trùng lặp.
- Lịch trình 4 ngày 3 đêm là phần mở rộng tùy chọn từ lịch trình 3 ngày 2 đêm;
  chưa tạo file riêng.
- Không tạo file riêng cho từng kỳ nghỉ, mùa quảng cáo, nhóm tuổi hoặc cụm từ
  SEO nếu phần lớn nội dung chỉ lặp lại một guide đã có.
- Inventory này chỉ khóa thiết kế. Việc biên soạn 04 file nội dung chuyên biệt
  phải được giao và review ở bước triển khai riêng.
- Các entity và `../places/travel_guides.md` đã hoàn tất review; bốn guide trong
  inventory này là phần answer-facing của nhánh `services/`.

## Danh sách 04 file đã chốt

1. `Đến Huế nên đi đâu.md`
2. `Lịch trình du lịch Huế ngắn ngày.md`
3. `Lịch trình du lịch Huế 3 ngày 2 đêm.md`
4. `Chi phí du lịch Huế.md`

## Ranh giới của nhánh services

Các file trong nhánh này giúp người dùng **lựa chọn và kết nối** thông tin để
lập kế hoạch. Chúng không thay thế file canonical của địa điểm, món ăn, di sản,
lễ hội hay chương trình biểu diễn.

- Địa điểm thiên nhiên, chợ, phố đi bộ và trải nghiệm du lịch đã có file riêng
  tiếp tục thuộc `knowledge-base-hue/tourism/`.
- Di sản, di tích, lăng tẩm và hướng dẫn tham quan di sản tiếp tục thuộc
  `knowledge-base-hue/heritages/`.
- Món ăn, quán ăn và hướng dẫn ẩm thực tiếp tục thuộc
  `knowledge-base-hue/foods/`.
- Lễ hội, lịch tổ chức và hướng dẫn tham dự lễ hội tiếp tục thuộc
  `knowledge-base-hue/festivals/`.
- Nhã nhạc, Ca Huế và các chương trình biểu diễn tiếp tục thuộc
  `knowledge-base-hue/performing_arts/`.
- Giá vé, loại vé, đối tượng miễn giảm và chính sách sử dụng vé thuộc
  `knowledge-base-hue/tourism/tickets/`.

Guide được phép nhắc ngắn gọn một entity để giải thích lựa chọn hoặc thứ tự
lịch trình, nhưng không sao chép toàn bộ lịch sử, mô tả, giá vé, giờ mở cửa,
địa chỉ, danh sách món/quán hay lịch biểu diễn từ file canonical.

## Thành phần của từng file

### 1. `Đến Huế nên đi đâu.md`

File này trả lời intent lựa chọn, không phải một toplist sao chép mô tả địa điểm.

Thành phần bắt buộc:

- lựa chọn cốt lõi cho người lần đầu đến Huế;
- gợi ý theo quỹ thời gian: vài giờ, nửa ngày, 1 ngày và nhiều ngày;
- gợi ý theo sở thích: di sản, kiến trúc, tâm linh, ẩm thực, nghệ thuật, thiên
  nhiên, làng quê, biển–đầm phá, chụp ảnh và trải nghiệm điện ảnh;
- gợi ý theo nhóm: đi một mình, cặp đôi, nhóm bạn, gia đình có trẻ nhỏ, người
  cao tuổi và người hạn chế vận động;
- gợi ý theo điều kiện: ngày nắng nóng, ngày mưa, buổi tối và ngân sách thấp;
- gom điểm theo cụm địa lý để tránh di chuyển zig-zag;
- thời lượng tương đối và mức độ đi bộ cho từng nhóm lựa chọn;
- chỉ dẫn sang file canonical để xem thông tin chi tiết.

Các chủ đề “Huế trên phim ảnh”, “địa điểm check-in”, “Huế về đêm”, “điểm miễn
phí” và “Huế cho người trẻ” trước mắt là các mục lựa chọn trong file này, không
tạo file độc lập.

### 2. `Lịch trình du lịch Huế ngắn ngày.md`

File này bao quát các hành trình có thời lượng từ nửa ngày đến 2 ngày 1 đêm.

Thành phần bắt buộc:

- nguyên tắc chọn ít điểm nhưng đủ thời gian trải nghiệm;
- lịch trình nửa ngày buổi sáng;
- lịch trình nửa ngày buổi chiều–tối;
- lịch trình 1 ngày cho người lần đầu;
- lịch trình 2 ngày 1 đêm;
- biến thể cho khách đến bằng tàu, máy bay hoặc đi về từ Đà Nẵng;
- biến thể ngày mưa và ngày nắng nóng;
- phương án cho gia đình có trẻ nhỏ hoặc người cao tuổi;
- logic gom điểm theo khu vực và thời gian di chuyển đệm;
- hạng mục nào cần đặt trước hoặc kiểm tra lại trong ngày đi.

Lịch trình chỉ khóa logic tuyến, thứ tự khu vực và thời lượng tương đối. Không
khóa giá dịch vụ, nhà vận hành, số hiệu chuyến, giờ khởi hành hoặc giờ mở cửa dễ
hết hạn.

### 3. `Lịch trình du lịch Huế 3 ngày 2 đêm.md`

Đây là file độc lập vì 3 ngày 2 đêm là intent xuất hiện lặp lại mạnh nhất trong
nhóm nguồn lịch trình được khảo sát.

Thành phần bắt buộc:

- lịch trình cân bằng cho người lần đầu: trung tâm–di sản, lăng tẩm–làng nghề,
  thiên nhiên hoặc đầm phá;
- phương án ưu tiên văn hóa và di sản;
- phương án cân bằng di sản, ẩm thực, nghệ thuật và nhịp sống địa phương;
- phương án thiên nhiên, sinh thái hoặc cộng đồng;
- phương án cho gia đình và người hạn chế vận động;
- phương án thay thế khi một ngày mưa lớn hoặc hoạt động ngoài trời không phù
  hợp;
- cách điều chỉnh khi đến muộn ngày đầu hoặc rời Huế sớm ngày cuối;
- lựa chọn mở rộng thành 4 ngày 3 đêm;
- ước lượng thời lượng, khoảng đệm và logic gom cụm, không nhồi quá nhiều điểm;
- checklist những thông tin động phải xác minh trước khi đi.

Không mặc định tất cả du khách đều có xe máy hoặc đủ thể lực để thực hiện cùng
một tuyến. Các phương án phải thể hiện điều kiện áp dụng.

### 4. `Chi phí du lịch Huế.md`

File này hướng dẫn lập ngân sách, không phải bảng báo giá của doanh nghiệp.

Thành phần bắt buộc:

- định nghĩa rõ chi phí có hoặc không bao gồm hành trình đến Huế;
- các hạng mục: vận chuyển liên tỉnh, di chuyển tại Huế, lưu trú, ăn uống, tham
  quan, trải nghiệm, mua sắm và khoản dự phòng;
- khung tiết kiệm, trung bình và thoải mái;
- dự toán cho 1 ngày, 2 ngày 1 đêm và 3 ngày 2 đêm;
- cách tính cho người đi một mình, cặp đôi, nhóm bạn và gia đình;
- các khoản có thể chia sẻ và các khoản tính theo đầu người;
- yếu tố làm chi phí tăng: mùa cao điểm, lễ hội, cuối tuần, đặt sát ngày và di
  chuyển xa trung tâm;
- cách tiết kiệm hợp lý mà không đánh đổi an toàn;
- liên kết tới nhánh tickets để kiểm tra giá vé hiện hành;
- ngày khảo sát, phạm vi ước tính và cảnh báo giá có thể thay đổi.

Không dùng một mức “tổng chi phí” duy nhất như kết luận áp dụng cho mọi nơi khởi
hành, mọi nhóm người hoặc mọi mùa. Giá của nhà cung cấp thương mại chỉ được dùng
như một quan sát có ngày kiểm tra, không phải mức giá chính thức.

## Quy tắc địa chỉ hành chính hiện hành

Từ ngày 01/07/2025, thành phố Huế vận hành hệ thống 40 đơn vị hành chính cấp xã
sau sắp xếp. Mọi địa chỉ trong nội dung triển khai phải dùng mô hình hiện hành:
`[số nhà/đường/thôn], [phường hoặc xã], thành phố Huế`; không tiếp tục chèn quận,
huyện cũ vào địa chỉ hiện hành.

Nguồn nền bắt buộc để đối chiếu đơn vị hành chính là
[Nghị quyết 1675/NQ-UBTVQH15](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-1675-nq-ubtvqh15-sap-xep-cac-dvhc-cap-xa-cua-thanh-pho-hue-nam-2025-119250616195617897.htm).

Một số ánh xạ có ảnh hưởng trực tiếp tới các điểm thường xuất hiện trong guide:

- Gia Hội, Phú Hậu, Tây Lộc, Thuận Lộc, Thuận Hòa và Đông Ba → phường Phú Xuân;
- Phú Hội, Phú Nhuận, Phường Đúc, Vĩnh Ninh, Phước Vĩnh và Trường An → phường
  Thuận Hóa;
- Thủy Vân, Xuân Phú và Vỹ Dạ → phường Vỹ Dạ;
- Thủy Biều, Thủy Bằng và Thủy Xuân → phường Thủy Xuân;
- Long Hồ, Hương Long và Kim Long → phường Kim Long;
- Thủy Dương, Thủy Phương và Thủy Thanh → phường Thanh Thủy.

Không được suy địa chỉ mới chỉ từ tên đường hoặc từ một bài viết gắn nhãn 2026.
Mỗi địa điểm phải được đối chiếu vị trí thực tế với nguồn chính thức của đơn vị
quản lý, cơ quan địa phương hoặc bản đồ đáng tin cậy.

## Thứ bậc nguồn và quy tắc xác minh

### Cấp 1 — nguồn dùng để khóa dữ kiện

- văn bản quy phạm pháp luật và văn bản của UBND/HĐND thành phố Huế;
- cổng của Sở Du lịch thành phố Huế và cơ quan quản lý chuyên ngành;
- website chính thức của đơn vị trực tiếp quản lý điểm đến hoặc dịch vụ công;
- Tổng công ty Đường sắt Việt Nam, hãng hàng không hoặc nhà vận tải cho dữ liệu
  do chính đơn vị đó vận hành.

### Cấp 2 — nguồn đối chiếu biên tập

- cổng du lịch quốc gia;
- báo chí địa phương và báo chí toàn quốc có quy trình biên tập;
- bài tổng hợp có tác giả, ngày cập nhật và dấu vết nguồn rõ ràng.

Nguồn cấp 2 có thể hỗ trợ diễn giải và phát hiện thay đổi, nhưng dữ liệu động vẫn
phải quay về nguồn cấp 1 khi có thể.

### Cấp 3 — nguồn phát hiện intent và ứng viên

- blog của sàn đặt dịch vụ, hãng lữ hành, trung tâm thương mại, khách sạn;
- toplist, bài SEO và bài bán tour;
- trang tổng hợp không nêu nguồn gốc claim.

Nguồn cấp 3 hữu ích để nhận diện câu hỏi phổ biến và cách du khách tổ chức chuyến
đi. Không dùng đơn lẻ để khóa giá, địa chỉ, giờ, lịch vận hành, tình trạng mở cửa,
tuyến giao thông hoặc quy định an toàn.

### Quy trình cho claim động

1. Xác định chủ thể có thẩm quyền công bố claim.
2. Tìm nguồn trực tiếp bằng truy vấn tiếng Việt.
3. Kiểm tra ngày ban hành, ngày hiệu lực và văn bản thay thế nếu có.
4. Đối chiếu thêm ít nhất một nguồn độc lập khi claim có ảnh hưởng lớn tới hành
   trình hoặc chi phí.
5. Ghi rõ mốc khảo sát trong evidence record.
6. Nếu chưa xác minh được, diễn đạt dưới dạng cần kiểm tra hoặc loại claim khỏi
   nội dung; không đoán.

## Mâu thuẫn và cảnh báo phát hiện trong nghiên cứu

- Nhãn “cập nhật 2026” không bảo đảm dữ liệu đã được kiểm tra theo đơn vị hành
  chính mới.
- Một số bài cập nhật năm 2026 vẫn ghi Trường Quốc Học Huế tại phường Phú Xuân,
  trong khi nguồn của Bảo tàng Hồ Chí Minh thành phố Huế ghi địa chỉ hiện hành
  tại phường Thuận Hóa.
- Một nguồn thương mại mô tả vé 530.000 đồng như vé tham quan tất cả di tích.
  Theo Nghị quyết 55/2025/NQ-HĐND có hiệu lực từ 04/01/2026, 530.000 đồng là
  tuyến gộp 04 điểm; tuyến gộp tất cả điểm là 600.000 đồng.
- Các bài thương mại đưa ra tổng chi phí rất khác nhau vì không thống nhất nơi
  khởi hành, số người, tiêu chuẩn lưu trú, mùa đi và phần đã bao gồm. Không thể
  lấy trung bình cơ học rồi coi đó là chi phí chuẩn.
- Danh sách hãng bay, hãng xe, khách sạn, quán ăn và giá thuê phương tiện trong
  bài cẩm nang có thể đã hết hiệu lực dù ngày bài viết vừa được cập nhật.
- Một số trang chính thức hoặc bán chính thức vẫn có mô tả thiếu chính xác; mọi
  claim quan trọng vẫn cần kiểm tra ở cấp dữ kiện, không mặc định đúng toàn bài.

Nguồn pháp lý giá vé hiện hành:
[Nghị quyết 55/2025/NQ-HĐND](https://hue.gov.vn/Portals/0/Uploads/VBPL/Nam2026/Thang1/000.00.00.K57-55-2025-NQ-HDND-2025-PL1.pdf).

Nguồn đối chiếu địa chỉ Trường Quốc Học Huế:
[Bảo tàng Hồ Chí Minh thành phố Huế](https://bthcm.hue.gov.vn/H%E1%BB%97-tr%E1%BB%A3-kh%C3%A1ch-tham-quan/Thuy%E1%BA%BFt-minh-t%E1%BB%B1-%C4%91%E1%BB%99ng/Nh%C3%A0-l%C6%B0u-ni%E1%BB%87m-Mai-Th%C3%BAc-Loan/pid/895/cid/12?tid=Di-tich-Truong-Quoc-Hoc-Hue.html).

## Đối chiếu với các guide chuyên ngành hiện có

### `heritages/heritage-guides.md`

Đã bao phủ lựa chọn di sản, phân cụm di tích, phương tiện tham quan, mùa tham
quan, vé và lịch trình di sản từ nửa ngày đến 3 ngày 2 đêm. Guide services chỉ
được dùng phần di sản như một thành phần của chuyến đi tổng hợp; không lặp lại
toàn bộ tuyến hoặc bảng vé di tích.

### `foods/food-guides.md`

Đã bao phủ món nên thử, bữa ăn theo thời điểm, ngân sách ăn uống, nhóm người dùng
và food tour. Guide services chỉ bố trí khung bữa ăn hoặc lựa chọn loại món; danh
sách quán và nội dung ẩm thực chi tiết phải quay về guide thực phẩm.

### `festivals/festival-guides.md`

Đã bao phủ lựa chọn lễ hội, thời điểm, chuẩn bị và ứng xử. Guide services chỉ nêu
cách điều chỉnh chuyến đi nếu trùng mùa lễ hội; không sao chép lịch sự kiện.

### `performing_arts/performing_arts_guides.md`

Đã bao phủ loại hình biểu diễn, địa điểm, lịch diễn, giá và cách thưởng thức.
Guide services chỉ dành một khoảng thời gian hợp lý cho trải nghiệm nghệ thuật và
yêu cầu người dùng kiểm tra lịch hiện hành ở nguồn chuyên trách.

Các bảng giá, giờ và địa chỉ động đang tồn tại trong bốn guide chuyên ngành không
được sao chép mặc định. Khi sử dụng lại một claim, implementer phải kiểm tra lại
tại thời điểm biên soạn.

## Danh mục URL do chủ dự án cung cấp đã đọc hoặc đối chiếu

### Cẩm nang tổng hợp và lựa chọn điểm đến

- [Thế Giới Di Động — Du lịch Huế 2026: Cẩm nang tự túc từ A–Z](https://www.thegioididong.com/hoi-dap/du-lich-hue-cam-nang-tu-tuc-tu-a-z-1591265)
- [Vietnam Tourism — Vi vu Huế](https://www.vietnamtourism.com/vi/vi-vu-hue-cam-nang-du-lich-hue-ay-u)
- [Jungle Boss — Kinh nghiệm du lịch Huế từ A–Z](https://junglebosstours.com/vi/kham-pha/blog-du-lich/du-lich-hue)
- [Du lịch Dân Dã — Du lịch Huế](https://dulichdanda.com/du-lich/hue/)
- [Klook — Lần đầu đến Huế nên đi đâu](https://www.klook.com/vi/blog/hue-tren-phim-anh/)
- [Klook — Địa điểm du lịch Huế](https://www.klook.com/vi/blog/dia-diem-du-lich-hue/)
- [MIA.vn — Cẩm nang du lịch Huế](https://mia.vn/cam-nang-du-lich/hue)
- [VnExpress — Cẩm nang du lịch Huế](https://vnexpress.net/cam-nang-du-lich-hue-4126937.html)
- [iVIVU — Du lịch Huế: Cẩm nang từ A đến Z](https://www.ivivu.com/blog/2024/03/du-lich-hue-cam-nang-tu-a-z/)
- [VinWonders — Kinh nghiệm du lịch Huế tự túc](https://vinwonders.com/vi/wonderpedia/news/kinh-nghiem-du-lich-hue-tu-tuc/)
- [Mường Thanh — Kinh nghiệm du lịch Huế tự túc](https://booking.muongthanh.com/tin-tuc/kinh-nghiem-du-lich-hue-tu-tuc)
- [Khám Phá Huế — Cẩm nang du lịch Huế tự túc](https://khamphahue.com.vn/Du-lich/Ban-can-biet/Chi-tiet/tid/Cam-nang-du-lich-Hue-tu-tuc-Nhung-dieu-ban-can-biet.html/pid/17453/cid/598)
- [MIA.vn — Kinh nghiệm du lịch Huế 2026](https://mia.vn/cam-nang-du-lich/kinh-nghiem-du-lich-hue-12059)
- [Phan Văn Travel — Kinh nghiệm du lịch Huế 2026](https://phanvantravel.com/kinh-nghiem-du-lich-hue)
- [Mường Thanh — Địa điểm du lịch Huế](https://booking.muongthanh.com/tin-tuc/dia-diem-du-lich-hue)
- [Sovaba Travel — Kinh nghiệm du lịch Huế từ A–Z](https://sovaba.travel/blog/bai-viet-cam-nang-du-lich-hue-chi-tiet-tat-tan-tat-tu-a-den-z)

### Lịch trình 3 ngày 2 đêm

- [Mytour — Gợi ý kế hoạch du lịch Huế 3 ngày 2 đêm](https://mytour.vn/vi/blog/bai-viet/goi-y-lich-trinh-hanh-trinh-tham-hiem-hue-trong-vong-3-ngay-2-dem.html)
- [VisitHue — 3 ngày 2 đêm ở Huế](https://visithue.vn/3-ngay-2-dem-o-Hue.html/?pid=MTk4NzN8Y3NkbGRs0)
- [AEON MALL Huế — Du lịch Huế 3 ngày 2 đêm](https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/du-lich-hue-3-ngay-2-dem.html)
- [Xe Đi Huế — Lịch trình du lịch Huế 3 ngày 2 đêm](https://xedihue.com/cam-nang-du-lich/du-lich-hue-31.html)
- [BestPrice — Gợi ý lịch trình du lịch Huế 3 ngày 2 đêm](https://www.bestprice.vn/blog/diem-den-8/hue-5/goi-y-lich-trinh-du-lich-hue-3-ngay-2-dem_2-3503.html)
- [Vinpearl — Du lịch Huế 3 ngày 2 đêm](https://vinpearl.com/vi/du-lich-hue-3-ngay-2-dem-lich-trinh-an-choi-chi-phi)

### Chi phí

- [AEON MALL Huế — Chi phí du lịch Huế](https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/chi-phi-di-hue.html)
- [Đà Nẵng Best — Kinh nghiệm du lịch Huế tự túc 2026](https://danangbest.com/kinh-nghiem-du-lich-hue-tu-tuc-2026-huong-dan-chi-tiet-tu-a-z-cho-nguoi-lan-dau.html)

## Nguồn bổ sung đáng ưu tiên khi triển khai

- [Vietnam Tourism — 3 ngày ở Huế dành cho người yêu văn hóa](https://www.vietnam.travel/vi/things-to-do/3-days-hue-culture-seekers)
- [Cổng vé Trung tâm Bảo tồn Di tích Cố đô Huế](https://eticket.hueworldheritage.org.vn/)
- [Sở Du lịch thành phố Huế](https://huetourism.gov.vn/)
- [VisitHue](https://visithue.vn/)
- [Nghị quyết 1675/NQ-UBTVQH15 về đơn vị hành chính](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-1675-nq-ubtvqh15-sap-xep-cac-dvhc-cap-xa-cua-thanh-pho-hue-nam-2025-119250616195617897.htm)
- [Nghị quyết 55/2025/NQ-HĐND về phí tham quan di tích](https://hue.gov.vn/Portals/0/Uploads/VBPL/Nam2026/Thang1/000.00.00.K57-55-2025-NQ-HDND-2025-PL1.pdf)

## Thứ tự triển khai đề xuất

1. `Đến Huế nên đi đâu.md`
2. `Lịch trình du lịch Huế ngắn ngày.md`
3. `Lịch trình du lịch Huế 3 ngày 2 đêm.md`
4. `Chi phí du lịch Huế.md`

Thứ tự này khóa trước logic lựa chọn điểm đến, sau đó mới xây lịch trình và ngân
sách. Implementer phải đối chiếu `../places/travel_guides.md` sau mỗi file để tránh
lặp nội dung đã có ở guide tổng quan hoặc domain khác.

## Tiêu chí nghiệm thu

- Chỉ có đúng 04 file nội dung chuyên biệt đã duyệt trong nhánh `services/`.
- Mỗi intent có một file canonical, không có hai cẩm nang A–Z cùng phạm vi.
- Lịch trình khả thi về khoảng cách, thời lượng, thời gian nghỉ và nhóm người.
- Có phương án mưa/nắng và phương án cho người hạn chế vận động.
- Không dùng quận, huyện hoặc phường cũ như địa chỉ hiện hành.
- Không sao chép bảng vé sang services; mọi giá vé được điều phối về tickets.
- Mọi giá, giờ, lịch chạy, địa chỉ và trạng thái vận hành có nguồn cùng mốc kiểm
  tra phù hợp.
- Nguồn thương mại không được dùng đơn lẻ để khóa claim quan trọng.
- Không biến guide thành toplist quảng cáo hoặc danh bạ nhà cung cấp.
- Không lặp mô tả dài đã có trong `heritages`, `foods`, `festivals`,
  `performing_arts` hoặc file entity của `tourism`.
- Các nhận định chưa đủ bằng chứng phải được loại bỏ hoặc diễn đạt rõ là cần
  kiểm tra, không suy đoán.

## Việc chưa thuộc phạm vi inventory này

- biên soạn nội dung hoàn chỉnh của 04 guide chuyên biệt;
- chốt giá vé và chính sách vé cho nhánh `tickets`;
- lập danh bạ doanh nghiệp, hướng dẫn viên hoặc đơn vị vận chuyển;
- sửa các guide chuyên ngành đang được review ở session khác;
- tạo thêm guide theo mùa, dịp lễ hoặc nhóm người ngoài danh sách đã duyệt.
