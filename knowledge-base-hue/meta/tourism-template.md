# Hướng dẫn và khuôn mẫu biên soạn nội dung du lịch Huế

Tài liệu này hướng dẫn Implementer nghiên cứu và biên soạn các file
answer-facing trong domain `tourism`. Mục tiêu là tạo nội dung chính xác, đúng
ranh giới entity, có giá trị lâu dài và hữu ích cho truy vấn về điểm đến, trải
nghiệm và lập kế hoạch du lịch tại Huế.

Đây là tài liệu điều phối, không phải một entity du lịch và phải được loại khỏi
nguồn ingestion.

## 1. Mục tiêu biên soạn

Mỗi file hoàn chỉnh phải đáp ứng đồng thời các yêu cầu:

- chính xác và đúng ranh giới entity;
- phân biệt đúng trạng thái vận hành, tổ chức và đầu tư;
- ưu tiên tri thức bền vững;
- đầy đủ theo nguồn đáng tin cậy, không điền cho đủ template;
- dùng tiếng Việt tự nhiên, hiện đại và khách quan;
- có cấu trúc Markdown dễ hiểu;
- mỗi section quan trọng đủ ngữ cảnh khi được tách để chunking và retrieval;
- không trùng nội dung đáng kể với entity trong `heritages`, `festivals`,
  `foods`, `performing_arts`, `services` hoặc `tickets`.

File tourism giúp người đọc hiểu bản chất của địa điểm hoặc trải nghiệm, lựa
chọn có phù hợp với nhu cầu hay không và nhận biết những điều cần kiểm tra trước
chuyến đi. File không phải bài quảng cáo, danh bạ nhà cung cấp hay bản sao của
một trang bán vé.

## 2. Nguyên tắc chung

### 2.1. Đầy đủ theo nguồn, không đầy đủ theo template

Template là khung lựa chọn section, không phải biểu mẫu bắt buộc điền mọi mục.
Chỉ viết nội dung có nguồn phù hợp và có ích cho việc hiểu entity. Bỏ field hoặc
section không áp dụng, không đủ nguồn hoặc chỉ tạo ra nội dung lặp.

Một file ngắn nhưng rõ ràng và được kiểm chứng tốt hơn một file dài chứa thông
tin quảng bá, suy đoán, chi tiết lỗi thời hoặc những đoạn văn có thể áp dụng cho
bất kỳ điểm đến nào.

Không dùng số lượng section, độ dài bài hoặc số lượng nguồn làm đại diện cho
chất lượng. Mức độ chi tiết phải tương xứng với độ phức tạp và bằng chứng của
entity.

### 2.2. Ranh giới entity và chống trùng lặp

Mỗi thực thể chỉ có một file chính theo inventory đã được duyệt. Trước khi viết,
Implementer phải xác định:

- entity là một địa điểm tự nhiên, khu vực, hệ thống địa lý, không gian đô thị,
  tuyến trải nghiệm, làng du lịch hay cơ sở dịch vụ;
- tên chính, tên gọi khác và những tên chỉ là cách quảng bá;
- phạm vi địa lý hoặc phạm vi trải nghiệm thuộc entity;
- các điểm thành phần được bao quát trong cùng file;
- các entity liên quan đã có file riêng và phần nội dung không được lặp lại;
- domain sở hữu phần tri thức chính.

Không tách một điểm thành nhiều file chỉ vì các nguồn dùng tên khác nhau. Không
gộp các địa điểm độc lập chỉ vì chúng nằm gần nhau hoặc thường xuất hiện trong
cùng hành trình.

Các quyết định cụ thể trong inventory có tính bắt buộc. Ví dụ:

- `Vịnh Lăng Cô.md` bao quát bãi biển Lăng Cô;
- `Bãi biển Cảnh Dương.md` bao quát tên quảng bá Tân Cảnh Dương khi đó là khu
  dịch vụ trên cùng không gian bãi biển;
- `Vườn quốc gia Bạch Mã.md` bao quát đỉnh Bạch Mã, Hải Vọng Đài, Ngũ Hồ và
  thác Đỗ Quyên trong phạm vi trải nghiệm của vườn quốc gia;
- `Làng du lịch cộng đồng Thác A Nôr.md` bao quát cả thác và mô hình trải
  nghiệm cộng đồng tại A Nôr;
- `Đèo Hải Vân.md` không viết lại lịch sử, kiến trúc và giá trị di sản đã thuộc
  file `Hải Vân Quan.md`.

File tổng quan một hệ thống và file thành phần được phép cùng tồn tại khi có nhu
cầu truy vấn độc lập. File hệ thống giải thích cấu trúc, phạm vi và quan hệ giữa
các hợp phần; file thành phần đi sâu vào đặc điểm riêng. Không sao chép nguyên
phần tổng quan từ file này sang file kia.

Cẩm nang, lịch trình và bài gợi ý chỉ tổng hợp vừa đủ để hỗ trợ quyết định và
điều hướng tới entity liên quan. Chúng không thay thế hoặc nhân bản file điểm
đến.

### 2.3. Tri thức bền vững và dữ liệu biến động

Phần lõi ưu tiên tri thức có giá trị lâu dài:

- loại hình, vị trí tương đối và phạm vi không gian;
- đặc điểm địa hình, sinh thái, cảnh quan hoặc cấu trúc đô thị;
- lịch sử hình thành đã được kiểm chứng;
- quan hệ với đời sống, sinh kế và văn hóa địa phương;
- trải nghiệm đặc trưng có tính ổn định;
- điều kiện tự nhiên và rủi ro mang tính quy luật;
- quan hệ với các điểm đến hoặc hệ thống liên quan.

Các thông tin sau có tính thời điểm và phải được xử lý thận trọng:

- giờ mở cửa, giờ hoạt động và mùa khai thác;
- giá vé, phí dịch vụ, giá thuê phương tiện và chính sách bán vé;
- số điện thoại, kênh đặt chỗ và nhà cung cấp;
- trạng thái mở cửa, đóng cửa, tạm dừng hoặc hạn chế tiếp cận;
- tiến độ dự án, chỉnh trang, xây dựng và sửa chữa;
- chất lượng đường vào, phương án giao thông và lịch phương tiện;
- hoạt động của một mùa hoặc một kỳ sự kiện;
- quy định tắm biển, cắm trại, bơi suối, trekking và cứu hộ;
- số lượt khách, doanh thu, công suất hoặc mục tiêu phát triển.

Chỉ đưa dữ liệu biến động vào khi thực sự cần cho việc hiểu entity, có nguồn
phù hợp và gắn rõ mốc kiểm chứng. Không biến lịch một năm thành lịch thường lệ,
một dự án thành dịch vụ hiện hữu hoặc một kế hoạch thành kết quả thực tế.

Giá vé và chính sách vé chi tiết thuộc `tourism/tickets`. Danh sách nhà cung
cấp, đơn vị vận chuyển, hướng dẫn viên và đại lý thuộc `tourism/services`.

### 2.4. Trạng thái vận hành, tổ chức và đầu tư

Implementer phải dùng đúng trạng thái áp dụng cho từng claim:

- **Tự nhiên hoặc hiện hữu:** địa hình, mặt nước, cảnh quan hay không gian đã
  tồn tại; trạng thái này không tự chứng minh nơi đó đang được tổ chức đón khách.
- **Đang đón khách:** có bằng chứng cập nhật về hoạt động tham quan hoặc dịch
  vụ và không có thông tin đáng tin cậy hơn cho thấy đang tạm dừng.
- **Hoạt động theo mùa hoặc theo điều kiện:** chỉ đón khách trong một số thời
  điểm, phụ thuộc thời tiết, thủy văn, cứu hộ hoặc điều kiện quản lý.
- **Tạm hạn chế hoặc tạm đóng:** có quyết định, thông báo hoặc bằng chứng cập
  nhật về việc hạn chế tiếp cận.
- **Đang chỉnh trang hoặc thi công:** có công trình đang triển khai; không được
  suy ra toàn bộ điểm đến đóng cửa hoặc đã hoàn thành nếu nguồn không nói rõ.
- **Đang thí điểm hoặc hoàn thiện mô hình:** sản phẩm du lịch chưa vận hành ổn
  định ở quy mô công bố.
- **Đã được chấp thuận đầu tư:** dự án đã hoàn thành một thủ tục; không có nghĩa
  công trình đã khởi công, hoàn thành hay đang đón khách.
- **Quy hoạch hoặc định hướng:** mới là mục tiêu quản lý/phát triển trong tương
  lai.
- **Chưa xác minh:** chưa có đủ nguồn để kết luận trạng thái hiện hành.

Đối với sự kiện tại điểm du lịch, phải phân biệt **dự kiến/được công bố**,
**được chấp thuận**, **bị hoãn**, **bị hủy**, **đã diễn ra** và **kết quả sau sự
kiện**. Không dùng kế hoạch, thông cáo trước sự kiện hoặc trang bán vé để khẳng
định sự kiện đã diễn ra.

Khi sử dụng số liệu, phải xác định đó là số thực tế, ước tính, công suất thiết
kế hay mục tiêu dự kiến; đồng thời ghi đúng phạm vi, thời điểm và chủ thể công
bố trong research record. Không cộng hoặc so sánh các số liệu khác phạm vi nếu
nguồn không cho phép.

### 2.5. Nguồn và kiểm chứng

- Ưu tiên UNESCO, Bộ Văn hóa, Thể thao và Du lịch, Cục Du lịch Quốc gia Việt
  Nam, Cục Di sản văn hóa, cơ quan lưu trữ quốc gia, chính quyền thành phố Huế,
  Trung tâm Bảo tồn Di tích Cố đô Huế, đơn vị nghệ thuật hoặc quản lý công lập
  và tài liệu nghiên cứu có căn cứ.
- Nguồn của ban tổ chức, nhà đầu tư, đơn vị vận hành, nhà sản xuất và nghệ sĩ
  được dùng cho ý tưởng, thành phần tham gia, kế hoạch và thông tin công bố
  thuộc phạm vi của họ. Tuyên bố quảng bá, công suất thiết kế hoặc số liệu dự
  kiến từ các nguồn này không được trình bày như kết quả thực tế.
- Báo chí uy tín được dùng để đối chiếu diễn biến, trạng thái vận hành/tổ chức,
  phản hồi, sự cố và số liệu sau sự kiện. Với claim quan trọng, ưu tiên thêm
  nguồn chính thức hoặc nguồn độc lập thứ hai nếu có.
- Cẩm nang du lịch được dùng để nhận diện câu hỏi, tên gọi phổ biến và nhu cầu
  của du khách; không làm nguồn duy nhất cho niên đại, địa điểm, địa giới, cấp
  ghi danh, phạm vi di sản, ranh giới tự nhiên, trạng thái hoạt động, mức độ an
  toàn hoặc số liệu.
- Mạng xã hội, trang bản đồ, nội dung do người dùng đăng và nền tảng bán vé có
  thể giúp phát hiện vấn đề cần tra cứu nhưng không phải căn cứ duy nhất cho
  claim quan trọng.

Nguồn có thẩm quyền phải được dùng đúng phạm vi. Một kế hoạch phát triển chứng
minh định hướng quản lý, không tự chứng minh điểm đã hoàn thành hoặc đang đón
khách. Một bài của đơn vị vận hành có thể xác nhận dịch vụ do chính đơn vị đó
cung cấp, nhưng không tự xác nhận danh hiệu, địa giới hoặc tác động xã hội rộng
hơn.

#### Cập nhật địa giới hành chính tại tháng 09/2026

Các URL do người dùng cung cấp có thể ghi đơn vị hành chính đã thay đổi. Sau đợt
sắp xếp đơn vị hành chính cấp xã năm 2025, Implementer bắt buộc phải dùng web
search và nguồn chính thức để xác định địa chỉ hiện hành tại thời điểm tháng
09/2026 trước khi hoàn tất file.

- Ưu tiên nghị quyết và văn bản pháp luật, Cổng Thông tin điện tử Chính phủ,
  Cổng Thông tin điện tử thành phố Huế và trang chính thức của đơn vị quản lý
  địa điểm.
- Địa chỉ hiện hành dùng tên phường hoặc xã mới đã được xác minh.
- Khi mô tả một sự kiện lịch sử, giữ tên địa giới đúng với thời điểm lịch sử nếu
  tên đó cần thiết cho bối cảnh; có thể chú thích quan hệ với địa giới hiện hành
  khi thông tin này giúp người đọc tránh nhầm lẫn.
- Không tự động thay mọi tên địa giới cũ bằng tên mới trong trích dẫn hoặc diễn
  giải lịch sử.
- Nếu chưa xác định chắc đơn vị hành chính hiện hành, chỉ ghi địa điểm ở mức đã
  kiểm chứng, không suy đoán phường hoặc xã.
- Với thực thể tự nhiên trải rộng qua nhiều đơn vị hành chính, mô tả đúng phạm
  vi đã kiểm chứng; không ép thành một địa chỉ đơn nhất.
- Trang bản đồ, mạng xã hội và nền tảng bán vé không được dùng làm căn cứ duy
  nhất để xác nhận địa giới hành chính.

Mốc pháp lý nền là Nghị quyết 1675/NQ-UBTVQH15 ngày 16/06/2025; chính quyền tại
các đơn vị mới hoạt động từ ngày 01/07/2025. Implementer vẫn phải kiểm tra nguồn
mới hơn nếu biên soạn sau tháng 09/2026.

#### Đối chiếu URL và tự nghiên cứu kiểm tra

Không sao chép thụ động thông tin từ URL được người dùng cung cấp. Quy trình bắt
buộc cho mỗi entity gồm:

1. Đọc đầy đủ các URL được cung cấp và ghi nhận ngày truy cập.
2. Tách các claim cần kiểm chứng, gồm tên, loại hình, tên gọi khác, niên đại,
   ranh giới, địa điểm, địa giới, đơn vị quản lý/tổ chức, trạng thái, danh hiệu,
   điều kiện tiếp cận, an toàn và số liệu.
3. Dùng web search để tìm nguồn độc lập và nguồn có thẩm quyền cho từng nhóm
   claim quan trọng.
4. Kiểm tra địa giới hành chính hiện hành tại tháng 09/2026 bằng nguồn chính
   thức.
5. Phân loại tri thức bền vững, dữ liệu theo kỳ và trạng thái vận hành/tổ chức
   trước khi viết.
6. Biên soạn file theo nguồn đã đối chiếu và đúng ranh giới inventory.
7. Sau khi tạo xong file, thực hiện một lượt self-verification độc lập bằng
   research và web search để rà soát lại toàn bộ dữ kiện, không chỉ kiểm tra lại
   các nguồn đã dùng ở lượt đầu.
8. Kiểm tra lần cuối tính chính xác, ổn định, rõ ràng, ranh giới entity, văn
   phong và Markdown.

Khi nguồn mâu thuẫn, Implementer không tự hợp nhất hoặc chọn cách diễn đạt làm
mờ khác biệt. Phải ghi lại URL, ngày truy cập, claim đang xét, nội dung khác
nhau và đánh giá sơ bộ về thẩm quyền của từng nguồn để Reviewer quyết định.

Theo quyết định của user, file entity không có section `## Nguồn dữ liệu`.
Provenance phải được giữ trong implementation evidence hoặc research record nằm
ngoài nội dung answer-facing.

### 2.6. Văn phong và khả năng đứng độc lập của section

- Dùng tiếng Việt hiện đại, khách quan, câu ngắn đến trung bình và mô tả trực
  tiếp.
- Tránh mỹ từ quảng bá như “tuyệt mỹ”, “độc nhất vô nhị”, “hùng vĩ bậc nhất”,
  “bùng nổ”, “đẳng cấp”, “mãn nhãn” hoặc “chưa từng có” nếu đó không phải nhận
  định có nguồn và cần thiết để giải thích giá trị.
- Không chuyển lời giới thiệu của cơ quan xúc tiến, nhà đầu tư, đơn vị vận hành
  hoặc thông cáo báo chí thành nhận định khách quan của bài viết.
- Phân biệt dữ kiện lịch sử, truyền thuyết, ký ức cộng đồng, tên gọi dân gian,
  tuyên bố quảng bá, đánh giá báo chí và diễn giải hiện đại. Không trình bày
  truyền thuyết, ký ức hoặc ý tưởng quảng bá như sự kiện đã được kiểm chứng.
- Không suy diễn quan hệ nhân quả, mức độ nổi tiếng, tác động kinh tế, mức độ an
  toàn hoặc phản ứng của du khách từ các dữ kiện rời rạc.
- Mỗi section quan trọng cần nhắc tên hoặc ngữ cảnh của entity một cách tự
  nhiên để vẫn hiểu được khi section trở thành một chunk độc lập.
- Tránh mở section bằng các đại từ thiếu chủ thể như “nơi đây”, “địa điểm này”
  hoặc “khu vực trên” nếu chunk có thể mất phần văn bản đứng trước.
- Không dùng thuật ngữ nội bộ như `canonical`, `chunk`, `metadata`, tên file
  hoặc đường dẫn repository trong nội dung answer-facing.

### 2.7. Markdown sạch

- File bắt đầu trực tiếp bằng `# <Tên điểm đến hoặc trải nghiệm>`.
- Không dùng YAML frontmatter.
- Không tạo section rỗng, placeholder hoặc bảng field dài.
- Không thêm `Liên kết nội bộ` vào body.
- Không tạo section `## Nguồn dữ liệu`.
- Không bắt buộc dùng đường phân cách `---` giữa các section.
- Chỉ tạo heading khi section có nội dung thực chất. Không dùng heading để lặp
  lại một hoặc hai câu đã có ở section khác.
- Danh sách chỉ dùng khi giúp đọc nhanh các mục song song; phần giải thích chính
  vẫn phải là văn xuôi tự nhiên.

## 3. Cấu trúc lõi dùng chung

Các section dưới đây là khung gợi ý. Chỉ H1, `## Thông tin chung`, `## Tổng
quan` và ít nhất một section nội dung đặc trưng của entity là bắt buộc.

```markdown
# <Tên điểm đến hoặc trải nghiệm>

## Thông tin chung

- **Tên chính:** <Tên đã được kiểm chứng và khớp inventory>
- **Tên gọi khác:** <Chỉ thêm tên có căn cứ>
- **Loại hình:** <Bãi biển, đầm phá, núi, chợ, phố đi bộ, làng du lịch...>
- **Địa điểm:** <Địa giới hiện hành tháng 09/2026 ở mức đã kiểm chứng>
- **Phạm vi:** <Chỉ thêm khi entity là một cụm hoặc trải trên nhiều địa bàn>
- **Đơn vị quản lý:** <Chỉ thêm khi vai trò và thời điểm được xác minh>
- **Trạng thái:** <Chỉ thêm khi cần; ghi rõ mốc kiểm chứng>

## Tổng quan

<Hai đến ba đoạn giới thiệu bản chất, ranh giới, đặc điểm chính và vai trò của
entity trong không gian du lịch Huế.>

## Đặc điểm không gian và cảnh quan

<Mô tả địa hình, mặt nước, sinh thái, cấu trúc đô thị hoặc cảnh quan đặc trưng
bằng dữ kiện đã kiểm chứng.>

## Lịch sử hình thành và biến đổi

<Chỉ tạo khi lịch sử giúp giải thích entity; phân biệt lịch sử tự nhiên, lịch sử
địa phương và quá trình hình thành sản phẩm du lịch.>

## Trải nghiệm đặc trưng

<Những hoạt động có tính đại diện và tương đối ổn định; không biến danh sách
dịch vụ của một nhà cung cấp thành thuộc tính chung của điểm đến.>

## Quan hệ với đời sống và văn hóa địa phương

<Sinh kế, cộng đồng, tập quán hoặc giá trị văn hóa có liên quan trực tiếp và có
nguồn.>

## Mùa và điều kiện tham quan

<Quy luật thời tiết, thủy văn hoặc mùa vụ; tách khỏi dự báo và lịch vận hành
ngắn hạn.>

## Tiếp cận và di chuyển

<Vị trí tương đối, đặc điểm tuyến tiếp cận và những giới hạn ổn định; thông tin
động phải có mốc kiểm chứng.>

## An toàn và bảo vệ môi trường

<Rủi ro đặc thù, nguyên tắc ứng xử và các điều cần kiểm tra trước chuyến đi.>

## Mối quan hệ với các điểm đến liên quan

<Chỉ tạo khi cần làm rõ quan hệ hệ thống, điểm thành phần hoặc ranh giới với
entity khác.>

## Thông tin dành cho du khách

<Thông tin bền vững, hữu ích và đã kiểm chứng; nhắc rõ nội dung động cần kiểm
tra lại thay vì đưa chi tiết dễ lỗi thời.>
```

Các field trong `## Thông tin chung` không phải danh sách bắt buộc. Bỏ field
không áp dụng hoặc không có nguồn đáng tin cậy. Không đưa tọa độ, quãng đường,
độ cao, diện tích hoặc đơn vị quản lý chỉ vì một nguồn tổng hợp có nêu; các dữ
kiện này phải được kiểm chứng và thực sự hữu ích.

## 4. Section chuyên biệt theo loại entity

### 4.1. Chợ, phố đi bộ và không gian ban đêm

Các section phù hợp có thể gồm:

```markdown
## Cấu trúc không gian và các khu vực chính

## Hàng hóa, ẩm thực và trải nghiệm đặc trưng

## Nhịp hoạt động và vai trò trong đời sống đô thị

## Văn hóa mua bán và ứng xử
```

Phân biệt chợ dân sinh với sản phẩm du lịch, phố đi bộ với phố đêm và không gian
thường xuyên với sự kiện chỉ diễn ra theo kỳ. Không viết giờ mở cửa, lịch cấm xe
hoặc khu vực biểu diễn như thuộc tính cố định nếu chưa có nguồn cập nhật.

Món ăn cụ thể chỉ được nhắc để mô tả trải nghiệm; lịch sử và tri thức chính của
món ăn thuộc domain `foods`. Chương trình biểu diễn và lễ hội có file riêng chỉ
được dẫn chiếu vừa đủ.

### 4.2. Bãi biển, vịnh và đầm phá

Các section phù hợp có thể gồm:

```markdown
## Địa hình bờ biển và cảnh quan mặt nước

## Hệ sinh thái và điều kiện tự nhiên

## Sinh kế ngư nghiệp và đời sống cộng đồng

## Hoạt động trên biển hoặc đầm phá

## Mùa biển, thủy triều và điều kiện thời tiết
```

Phân biệt địa danh tự nhiên với bãi tắm, trung tâm dịch vụ, khu nghỉ dưỡng hoặc
dự án ven biển. Không suy ra chất lượng nước, độ an toàn tắm biển hay sự hiện
diện của cứu hộ từ vẻ đẹp cảnh quan.

Với đầm phá, phải làm rõ entity là toàn hệ thống, một hợp phần địa lý hay điểm
trải nghiệm cụ thể. Các claim về diện tích, chiều dài, độ mặn, đa dạng sinh học
và phạm vi hành chính cần nguồn chuyên môn hoặc chính thức.

### 4.3. Núi, đồi, đèo và điểm trekking

Các section phù hợp có thể gồm:

```markdown
## Địa hình và cảnh quan

## Tuyến tiếp cận và đặc điểm hành trình

## Điểm quan sát và các thành phần tiêu biểu

## Giá trị lịch sử, văn hóa hoặc biểu tượng

## Điều kiện trekking và rủi ro tự nhiên
```

Không đồng nhất một ngọn núi với dự án du lịch trên núi, một cung đường đèo với
công trình di sản tại đỉnh đèo hoặc một tuyến đi tự phát với tuyến trekking được
quản lý. Độ cao, độ khó, thời lượng và quãng đường chỉ được ghi khi đã xác định
đúng mốc đo và nguồn.

Thông tin về cháy rừng, sạt lở, thời tiết, kiểm soát ra vào, thi công và cứu hộ
có thể thay đổi nhanh. Nội dung phải nêu nguyên tắc an toàn bền vững và yêu cầu
kiểm tra trạng thái hiện hành trước chuyến đi.

### 4.4. Suối, thác và điểm sinh thái

Các section phù hợp có thể gồm:

```markdown
## Dòng chảy, địa hình và cảnh quan

## Các khu vực trải nghiệm

## Mùa nước và điều kiện tiếp cận

## Quản lý, cứu hộ và an toàn dưới nước

## Hệ sinh thái và trách nhiệm bảo vệ môi trường
```

Phân biệt thắng cảnh tự nhiên với khu dịch vụ đang khai thác. Không viết “an
toàn để tắm”, “luôn có cứu hộ” hoặc “mở cửa hằng ngày” nếu không có xác nhận
cập nhật. Sau mưa lớn, lũ, sự cố hoặc yêu cầu rà soát, trạng thái phải được kiểm
chứng lại bằng nguồn chính thức hay báo chí đáng tin cậy.

Không dùng kế hoạch nâng cấp đường, nhà vệ sinh hoặc điểm cứu hộ làm bằng chứng
rằng hạng mục đã hoàn thành.

### 4.5. Làng du lịch cộng đồng

Các section phù hợp có thể gồm:

```markdown
## Cộng đồng chủ thể và không gian cư trú

## Trải nghiệm văn hóa và sinh kế

## Mô hình tổ chức và sự tham gia của cộng đồng

## Lưu trú, đón khách và nguyên tắc ứng xử
```

Không biến cộng đồng thành phông nền quảng bá. Phải xác định người dân, tổ hợp
tác, hợp tác xã, chính quyền hay doanh nghiệp có vai trò gì và vai trò đó đúng ở
thời điểm nào. Không suy ra lợi ích cộng đồng từ doanh thu, lượt khách hoặc tuyên
bố của một đơn vị nếu thiếu bằng chứng.

Phong tục, truyền thuyết và ký ức cộng đồng phải được ghi đúng loại nguồn và
ngữ cảnh. Thông tin lưu trú, suất ăn, biểu diễn hoặc đặt chỗ là dữ liệu vận hành,
không phải đặc tính cố định của cả làng.

### 4.6. Vườn quốc gia, hệ thống địa lý hoặc cụm điểm đến

Các section phù hợp có thể gồm:

```markdown
## Phạm vi và các thành phần

## Cấu trúc không gian hoặc hệ sinh thái

## Các tuyến và điểm trải nghiệm chính

## Giá trị chung của hệ thống

## Quản lý, bảo tồn và tiếp cận
```

File tổng quan phải giúp người đọc hiểu toàn hệ thống mà không làm mất tính độc
lập của các file thành phần. Mỗi thành phần chỉ được tóm tắt đủ để giải thích
quan hệ; chi tiết riêng thuộc file tương ứng.

Nếu phạm vi bảo vệ, vùng lõi, vùng đệm hoặc địa giới trải trên nhiều xã/phường,
không rút gọn thành một địa chỉ duy nhất. Phân biệt ranh giới tự nhiên, ranh
giới quản lý và phạm vi sản phẩm du lịch.

### 4.7. Cẩm nang, lịch trình và bài gợi ý

Đây là nội dung tổng hợp theo ý định người dùng, không phải entity điểm đến.
Cấu trúc có thể gồm:

```markdown
## Phạm vi và đối tượng phù hợp

## Nguyên tắc lựa chọn điểm đến

## Trình tự khu vực hoặc logic hành trình

## Phương án điều chỉnh theo thời tiết và thời lượng

## Những thông tin cần kiểm tra trước chuyến đi
```

Không tạo biến thể chỉ bằng cách thay tên mùa, ngày lễ hoặc số ngày khi nội dung
gần như giống nhau. Lịch trình không khóa giá, nhà cung cấp, giờ chạy hoặc lịch
biểu dễ hết hạn. Mỗi điểm đến chỉ được tóm tắt theo vai trò trong hành trình,
không nhân bản nội dung canonical của entity.

## 5. Thông tin dành cho du khách

Section này chỉ chứa thông tin tương đối bền vững và hữu ích, chẳng hạn:

- đối tượng và mức vận động phù hợp;
- đặc điểm địa hình hoặc không gian ảnh hưởng đến khả năng tiếp cận;
- điều kiện thời tiết, thủy văn hoặc mùa vụ cần lưu ý;
- quy tắc ứng xử tại cộng đồng, nơi tôn nghiêm hoặc khu bảo tồn;
- nguyên tắc an toàn tại biển, đầm phá, núi, đèo, suối và thác;
- nội dung động người đọc cần kiểm tra lại trước chuyến đi.

Không mặc định đưa giá vé, giờ mở cửa, số điện thoại, liên kết đặt chỗ, danh
sách nhà hàng, tên đơn vị tour hoặc lịch phương tiện vào file. Khi người dùng
cần dữ liệu vận hành hiện tại, hệ thống phải tra cứu nguồn cập nhật thay vì dựa
vào file tri thức bền vững.

## 6. Implementation evidence và research record

Với mỗi entity, Implementer phải lưu bằng chứng bên ngoài file answer-facing,
gồm tối thiểu:

- tên entity và ngày thực hiện research;
- URL do người dùng cung cấp và ngày truy cập;
- các nguồn đối chiếu độc lập và ngày truy cập;
- danh sách claim quan trọng cùng nguồn hỗ trợ;
- căn cứ xác định tên chính, tên gọi khác và quyết định gộp/tách entity;
- căn cứ xác định địa chỉ cũ, địa chỉ hiện hành và quan hệ chuyển đổi địa giới;
- trạng thái vận hành, tổ chức hoặc đầu tư tại mốc kiểm chứng;
- phân loại số liệu là thực tế, ước tính, công suất hay mục tiêu dự kiến;
- các nguồn mâu thuẫn, nội dung khác biệt và điểm cần Reviewer quyết định;
- kết quả self-verification sau khi hoàn thành bản thảo.

Đối với claim an toàn hoặc khả năng tiếp cận, record phải ghi ngày của sự cố,
thông báo, quyết định hoặc lần kiểm tra gần nhất và không suy ra trạng thái hiện
hành nếu bằng chứng đã cũ.

Research record phải đủ để Reviewer lần ngược từ claim quan trọng đến nguồn,
nhưng không được chép nguyên vào body của entity.

## 7. Tiêu chí hoàn thành cho mỗi entity

Một file chỉ sẵn sàng để review khi:

- tên file và H1 khớp entity trong inventory, dùng tiếng Việt có dấu và khoảng
  trắng theo đúng tên đã duyệt;
- loại hình, phạm vi và ranh giới entity được diễn đạt chính xác;
- entity không bị đồng nhất với điểm thành phần, dự án, doanh nghiệp, sự kiện
  hoặc domain khác;
- trạng thái hiện hữu, đang đón khách, theo mùa, hạn chế, thi công, thí điểm,
  đầu tư và quy hoạch không bị trộn lẫn;
- mọi claim quan trọng có evidence nguồn bên ngoài file answer-facing;
- URL do người dùng cung cấp đã được đọc và đối chiếu bằng web search độc lập;
- địa giới hành chính đã được kiểm tra theo hiện trạng tháng 09/2026 qua nguồn
  chính thức;
- tên địa giới lịch sử và tên địa giới hiện hành được dùng đúng ngữ cảnh;
- dữ liệu biến động được loại bỏ, gắn mốc rõ ràng hoặc chuyển đúng domain;
- số liệu có thời điểm, phạm vi, loại đo lường và nguồn công bố rõ trong
  evidence;
- không có suy đoán, placeholder, văn phong quảng bá hoặc mâu thuẫn bị che giấu;
- section chuyên biệt phù hợp với loại entity, không điền template máy móc;
- không lặp nội dung đáng kể với file hệ thống, điểm thành phần hoặc entity ở
  domain khác;
- Markdown bắt đầu bằng H1, không có frontmatter, section rỗng, bảng field dài,
  `## Nguồn dữ liệu` hoặc `Liên kết nội bộ`;
- mỗi section quan trọng đủ ngữ cảnh để hiểu độc lập khi được retrieval;
- đã hoàn tất lượt self-verification độc lập sau khi biên soạn;
- nội dung cuối cùng đã được kiểm tra về tính chính xác, ổn định, rõ ràng, an
  toàn và tiếng Việt tự nhiên.
