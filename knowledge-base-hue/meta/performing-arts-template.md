# Hướng dẫn và khuôn mẫu biên soạn nghệ thuật biểu diễn Huế

Tài liệu này định nghĩa nguyên tắc và cấu trúc gợi ý cho các file entity thuộc
`knowledge-base-hue/performing_arts/`. Danh sách và ranh giới entity được quản lý
tại `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md`.
Inventory là tài liệu điều phối và phải được loại khỏi ingestion trong giai đoạn
chunking đa domain sau này.

## 1. Mục tiêu biên soạn

Mỗi file phải là một văn bản tri thức tự nhiên, chuẩn xác và sạch cho hệ thống
RAG, đồng thời đọc được như một bài viết thông tin hoàn chỉnh dành cho con
người. Không viết file như lịch sự kiện, bài quảng bá, hồ sơ bán vé, bản chép
thông cáo báo chí hoặc chuỗi field được điền cho đủ template.

Template này áp dụng cho ba nhóm entity chính:

- chương trình biểu diễn thường xuyên hoặc gắn với thực hành truyền thống;
- chuỗi chương trình hoặc sự kiện nghệ thuật được tổ chức qua nhiều kỳ;
- chương trình, live show hoặc sản phẩm nghệ thuật thuộc một kỳ cụ thể.

Thứ tự ưu tiên:

```text
Chính xác và đúng ranh giới entity
-> phân biệt đúng trạng thái tổ chức
-> tri thức bền vững
-> đầy đủ theo nguồn đáng tin cậy
-> tiếng Việt tự nhiên, khách quan
-> cấu trúc Markdown dễ hiểu
-> section đủ ngữ cảnh cho chunking và retrieval
```

## 2. Nguyên tắc chung

### 2.1. Đầy đủ theo nguồn, không đầy đủ theo template

- Chỉ tạo field hoặc section khi có thông tin đáng tin cậy và thực sự giúp trả
  lời câu hỏi về entity.
- Không điền nội dung suy đoán, không tạo placeholder và không viết “chưa có dữ
  liệu” để lấp chỗ trống.
- File ngắn nhưng chính xác tốt hơn file dài chứa diễn giải quảng bá, lặp lại
  hoặc chi tiết không kiểm chứng được.
- Không suy rộng đặc điểm của một kỳ tổ chức thành bản chất ổn định của cả chuỗi
  sự kiện.

### 2.2. Ranh giới entity và chống trùng lặp

Phải phân biệt rõ:

- loại hình nghệ thuật với chương trình trình diễn loại hình đó;
- di sản văn hóa phi vật thể với hoạt động giới thiệu hoặc trình diễn di sản;
- chuỗi sự kiện với một kỳ tổ chức cụ thể;
- chương trình nghệ thuật thành phần với lễ hội hoặc sự kiện bao trùm;
- địa điểm biểu diễn với chương trình diễn ra tại địa điểm đó.

File về một chương trình biểu diễn chỉ giải thích những loại hình nghệ thuật liên
quan ở mức cần thiết để hiểu chương trình. Không sao chép toàn bộ lịch sử, giá
trị, phạm vi ghi danh hoặc hoạt động bảo vệ của entity di sản thuộc domain khác.

Ví dụ, file về chương trình nghệ thuật cung đình tại Duyệt Thị Đường tập trung
vào chương trình, không thay thế file về Nhã nhạc hoặc Tuồng cung đình. File về
một chương trình thuộc Festival Huế không viết lại toàn bộ lịch sử và cấu trúc
của Festival Huế.

### 2.3. Tri thức bền vững và dữ liệu theo từng kỳ

Phần lõi của file ưu tiên những nội dung có giá trị lâu dài:

- nguồn gốc và quá trình hình thành;
- ý tưởng, mục tiêu hoặc định hướng nghệ thuật đã được kiểm chứng;
- loại hình và cấu trúc chương trình;
- không gian biểu diễn đặc trưng;
- chủ thể tổ chức, sáng tạo, biểu diễn hoặc cộng đồng thực hành;
- vai trò của chương trình trong đời sống văn hóa Huế.

Những thông tin sau thường chỉ đúng với một kỳ hoặc một thời điểm:

- ngày và giờ diễn ra cụ thể;
- chủ đề, nghệ sĩ, danh sách tiết mục và sân khấu của một kỳ;
- giá vé, hạng vé, kênh bán vé và chính sách vào cửa;
- số lượng khán giả, nghệ sĩ, chương trình hoặc buổi diễn;
- đơn vị tài trợ, đối tác hoặc nhân sự sản xuất theo kỳ;
- trạng thái mở cửa, tạm dừng hoặc lịch biểu diễn hiện tại.

Dữ liệu theo kỳ chỉ được đưa vào `## Các kỳ tổ chức tiêu biểu` khi giúp giải
thích quá trình phát triển, dấu mốc nghệ thuật hoặc mức độ tiếp nhận của entity
và có nguồn phù hợp. Mỗi dữ kiện phải gắn với năm hoặc ngày cụ thể. Không biến
lịch của một năm thành lịch thường lệ.

### 2.4. Trạng thái tổ chức và cách sử dụng số liệu

Mỗi kỳ sự kiện phải được phân biệt đúng trạng thái:

- **Dự kiến / được công bố:** xuất hiện trong kế hoạch hoặc thông cáo trước sự
  kiện nhưng chưa có bằng chứng đã diễn ra.
- **Được chấp thuận:** đã hoàn thành một thủ tục quản lý có liên quan; trạng thái
  này không tự chứng minh sự kiện đã diễn ra.
- **Bị hoãn:** không diễn ra theo lịch ban đầu và có thể được tổ chức lại.
- **Bị hủy:** không diễn ra theo kế hoạch đã công bố.
- **Đã diễn ra:** có nguồn hậu kiểm, báo cáo, tin tường thuật hoặc bằng chứng phù
  hợp sau thời điểm tổ chức.
- **Kết quả sau sự kiện:** số liệu hoặc đánh giá được công bố sau khi chương
  trình kết thúc.

Không dùng kế hoạch, thông cáo trước sự kiện hoặc nội dung bán vé để khẳng định
kết quả thực tế. Nếu một chương trình từng bị hoãn rồi được tổ chức vào ngày
khác, phải mô tả hai mốc này rõ ràng.

Khi sử dụng số liệu, phải xác định đúng:

- số thực tế, số ước tính hay mục tiêu dự kiến;
- phạm vi đo là một buổi diễn, toàn bộ chương trình, một chuỗi sự kiện hay một
  khoảng thời gian;
- đối tượng đo là người tham dự trực tiếp, vé phát hành, lượt khách du lịch,
  lượt xem trực tuyến hay mức độ tiếp cận truyền thông;
- cơ quan hoặc tổ chức công bố và thời điểm công bố.

Không cộng, so sánh hoặc chuyển đổi các số liệu khác phạm vi nếu nguồn không
cho phép. Chỉ giữ số liệu có ý nghĩa giải thích; không bắt buộc đưa số liệu vào
mọi file.

### 2.5. Nguồn và kiểm chứng

- Ưu tiên UNESCO, Bộ Văn hóa, Thể thao và Du lịch, Cục Di sản văn hóa, cơ quan
  lưu trữ quốc gia, chính quyền thành phố Huế, Trung tâm Bảo tồn Di tích Cố đô
  Huế, đơn vị nghệ thuật công lập và tài liệu nghiên cứu có căn cứ.
- Nguồn của ban tổ chức, nhà sản xuất và nghệ sĩ được dùng cho ý tưởng sáng tạo,
  thành phần tham gia, kế hoạch và thông tin công bố. Tuyên bố quảng bá hoặc số
  liệu dự kiến từ các nguồn này không được trình bày như kết quả thực tế.
- Báo chí uy tín được dùng để đối chiếu diễn biến, trạng thái tổ chức, phản hồi
  và số liệu sau sự kiện. Với claim quan trọng, ưu tiên thêm nguồn chính thức
  hoặc nguồn độc lập thứ hai nếu có.
- Cẩm nang du lịch được dùng để nhận diện câu hỏi và nhu cầu của khán giả, không
  làm nguồn duy nhất cho niên đại, địa điểm, cấp ghi danh, phạm vi di sản, trạng
  thái tổ chức hoặc số liệu.

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
- Trang bản đồ, mạng xã hội và nền tảng bán vé không được dùng làm căn cứ duy
  nhất để xác nhận địa giới hành chính.

#### Đối chiếu URL và tự nghiên cứu kiểm tra

Không sao chép thụ động thông tin từ URL được người dùng cung cấp. Quy trình bắt
buộc cho mỗi entity gồm:

1. Đọc đầy đủ các URL được cung cấp và ghi nhận ngày truy cập.
2. Tách các claim cần kiểm chứng, gồm tên, loại hình, niên đại, địa điểm, đơn vị
   tổ chức, trạng thái, nội dung nghệ thuật, danh hiệu và số liệu.
3. Dùng web search để tìm nguồn độc lập và nguồn có thẩm quyền cho từng nhóm
   claim quan trọng.
4. Kiểm tra địa giới hành chính hiện hành tại tháng 09/2026 bằng nguồn chính
   thức.
5. Phân loại tri thức bền vững, dữ liệu theo kỳ và trạng thái tổ chức trước khi
   viết.
6. Biên soạn file theo nguồn đã đối chiếu.
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
- Không chuyển lời giới thiệu của ban tổ chức hoặc thông cáo báo chí thành nhận
  định khách quan của bài viết.
- Phân biệt dữ kiện lịch sử, truyền thuyết, ký ức nghệ sĩ hoặc cộng đồng, tuyên
  bố của nhà sản xuất, đánh giá báo chí và diễn giải hiện đại. Không trình bày
  truyền thuyết, ký ức hoặc ý tưởng quảng bá như sự kiện đã được kiểm chứng.
- Không suy diễn quan hệ nhân quả, mức độ ảnh hưởng hoặc phản ứng của công chúng
  từ các dữ kiện rời rạc.
- Mỗi section quan trọng cần nhắc tên hoặc ngữ cảnh của entity một cách tự nhiên
  để vẫn hiểu được khi section trở thành một chunk độc lập.
- Không dùng thuật ngữ nội bộ như `canonical`, `chunk`, `metadata`, tên file hoặc
  đường dẫn repository trong nội dung answer-facing.

### 2.7. Markdown sạch

- File bắt đầu trực tiếp bằng `# <Tên chương trình hoặc sự kiện nghệ thuật>`.
- Không dùng YAML frontmatter.
- Không tạo section rỗng, placeholder hoặc bảng field dài.
- Không thêm `Liên kết nội bộ` vào body.
- Không tạo section `## Nguồn dữ liệu`.
- Không bắt buộc dùng đường phân cách `---` giữa các section.

## 3. Cấu trúc lõi dùng chung

Các section dưới đây là khung gợi ý. Chỉ H1, `## Thông tin chung`, `## Tổng
quan` và ít nhất một section nội dung đặc trưng của entity là bắt buộc.

```markdown
# <Tên chương trình hoặc sự kiện nghệ thuật>

## Thông tin chung

- **Tên chính thức:** <Tên đã được kiểm chứng>
- **Tên gọi khác:** <Chỉ thêm khi có>
- **Loại hình:** <Chương trình biểu diễn, chuỗi sự kiện, hòa nhạc, live show...>
- **Tính chất tổ chức:** <Thường xuyên, định kỳ hoặc một kỳ cụ thể>
- **Thời điểm hình thành / Lần đầu tổ chức:** <Chỉ thêm khi xác minh được>
- **Không gian biểu diễn:** <Địa điểm và địa giới hiện hành đã kiểm chứng>
- **Đơn vị tổ chức / biểu diễn:** <Chỉ thêm chủ thể có vai trò rõ ràng>

## Tổng quan

<Hai đến ba đoạn giới thiệu bản chất, phạm vi, đặc điểm chính và vị trí của
entity trong đời sống văn hóa Huế.>

## Lịch sử hình thành và phát triển

<Hoàn cảnh ra đời, các giai đoạn hoặc thay đổi quan trọng đã được kiểm chứng.>

## Nội dung và hình thức nghệ thuật

<Cấu trúc chương trình, loại hình, tiết mục, ngôn ngữ sân khấu hoặc phương thức
trình diễn có tính đại diện.>

## Không gian biểu diễn và trải nghiệm khán giả

<Quan hệ giữa chương trình với địa điểm, cách tổ chức không gian và những đặc
điểm ổn định ảnh hưởng đến việc tiếp nhận của khán giả.>

## Chủ thể sáng tạo, biểu diễn và tổ chức

<Nghệ sĩ, nghệ nhân, cộng đồng, đơn vị nghệ thuật hoặc ban tổ chức có vai trò
quan trọng và ổn định.>

## Các kỳ tổ chức tiêu biểu

<Chỉ ghi những kỳ có ý nghĩa đối với quá trình phát triển của entity; mọi dữ
kiện biến động phải gắn với năm và trạng thái tổ chức.>

## Ý nghĩa trong đời sống văn hóa Huế

<Giải thích giá trị hoặc vai trò bằng dữ kiện cụ thể, không dùng lời tán dương
chung chung.>

## Mối quan hệ với các loại hình hoặc sự kiện liên quan

<Chỉ tạo khi cần làm rõ quan hệ với di sản, loại hình nghệ thuật, chương trình
thành phần hoặc sự kiện bao trùm.>

## Thông tin dành cho khán giả

<Chỉ cung cấp thông tin bền vững, hữu ích và đã kiểm chứng.>
```

Các field trong `## Thông tin chung` không phải danh sách bắt buộc. Bỏ field
không áp dụng hoặc không có nguồn đáng tin cậy. Không thêm trạng thái như “đang
hoạt động” hoặc “đang biểu diễn hằng ngày” nếu không gắn với mốc kiểm chứng và
nội dung đó dễ thay đổi.

## 4. Section chuyên biệt theo loại entity

### 4.1. Chương trình biểu diễn truyền thống hoặc thường xuyên

Các section phù hợp có thể gồm:

```markdown
## Hình thức và cấu trúc chương trình

## Tiết mục, nhạc cụ, phục trang và ngôn ngữ trình diễn

## Nghệ nhân, nghệ sĩ và cộng đồng thực hành

## Trao truyền, bảo tồn và thích ứng đương đại
```

Không biến một chương trình trình diễn di sản thành toàn bộ di sản. Phải phân
biệt thực hành trong bối cảnh gốc, hình thức sân khấu hóa, chương trình phục vụ
khách tham quan và hoạt động bảo vệ di sản.

Nếu lịch diễn, thời lượng, giá vé hoặc địa điểm đón khách có thể thay đổi, không
đưa chúng vào như thuộc tính ổn định. Chỉ mô tả quy luật tổ chức khi có nguồn
cho thấy quy luật được duy trì qua thời gian.

### 4.2. Chuỗi sự kiện hoặc chương trình định kỳ

Các section phù hợp có thể gồm:

```markdown
## Định hướng và bản sắc nghệ thuật

## Cấu trúc chương trình qua các kỳ

## Các kỳ tổ chức tiêu biểu

## Mức độ tiếp nhận và ảnh hưởng
```

Không dùng một kỳ duy nhất để xác định cấu trúc cố định của toàn chuỗi. Một hoạt
động chỉ được gọi là thường lệ khi có bằng chứng từ nhiều kỳ hoặc tuyên bố chính
thức về mô hình tổ chức.

Số liệu khán giả hoặc truyền thông phải gắn với đúng kỳ và phạm vi. Không trình
bày mục tiêu tổ chức hằng năm như bằng chứng rằng chuỗi đã được duy trì hằng
năm.

### 4.3. Chương trình, live show hoặc sản phẩm nghệ thuật một kỳ

Các section phù hợp có thể gồm:

```markdown
## Bối cảnh và ý tưởng sáng tạo

## Cấu trúc chương trình và thành phần nghệ thuật

## Thiết kế sân khấu, công nghệ và không gian trình diễn

## Quá trình tổ chức và mức độ tiếp nhận
```

Phải xác định chương trình đã diễn ra, bị hoãn, bị hủy hay chỉ mới được công bố.
Đội ngũ sáng tạo, nghệ sĩ, thời lượng và công nghệ chỉ được ghi khi nguồn phù
hợp xác nhận. Không suy ra tác động lâu dài từ lượng người xem hoặc phản ứng
truyền thông của một đêm diễn.

### 4.4. Chương trình tái hiện hoặc diễn giải văn hóa cung đình

Các section phù hợp có thể gồm:

```markdown
## Cơ sở lịch sử và phạm vi tái hiện

## Cấu trúc nghi thức và nội dung biểu diễn

## Thành tố được phục dựng hoặc diễn giải

## Bối cảnh phục vụ công chúng đương đại
```

Phải phân biệt nghi thức lịch sử với chương trình phục dựng, tái hiện hoặc diễn
giải đương đại. Không mô tả một bản tái hiện như nghi lễ nguyên trạng nếu nguồn
không chứng minh được tính liên tục và nguyên bản.

## 5. Thông tin dành cho khán giả

Section này chỉ chứa thông tin tương đối bền vững và có ích, chẳng hạn:

- đặc điểm không gian ảnh hưởng đến khả năng tiếp cận hoặc theo dõi chương
  trình;
- quy tắc trang phục và ứng xử tại không gian cung đình, tôn nghiêm hoặc di
  tích;
- giới hạn tiếp cận mang tính ổn định và đã được xác minh;
- cách phân biệt chương trình thường xuyên với kỳ sự kiện đặc biệt.

Không mặc định đưa giá vé, giờ diễn, sơ đồ chỗ ngồi, số điện thoại, kênh bán vé,
đường dẫn đăng ký, lịch nghệ sĩ hoặc chính sách hoàn vé vào file. Khi người dùng
cần dữ liệu vận hành hiện tại, hệ thống phải tra cứu nguồn cập nhật thay vì dựa
vào file tri thức bền vững.

## 6. Implementation evidence và research record

Với mỗi entity, Implementer phải lưu bằng chứng bên ngoài file answer-facing,
gồm tối thiểu:

- tên entity và ngày thực hiện research;
- URL do người dùng cung cấp và ngày truy cập;
- các nguồn đối chiếu độc lập và ngày truy cập;
- bảng hoặc danh sách claim quan trọng cùng nguồn hỗ trợ;
- căn cứ xác định địa chỉ cũ, địa chỉ hiện hành và quan hệ chuyển đổi địa giới;
- trạng thái của từng kỳ sự kiện được nhắc đến;
- phân loại số liệu là dự kiến, ước tính hay kết quả thực tế;
- các nguồn mâu thuẫn, nội dung khác biệt và điểm cần Reviewer quyết định;
- kết quả self-verification sau khi hoàn thành bản thảo.

Research record phải đủ để Reviewer lần ngược từ claim quan trọng đến nguồn,
nhưng không được chép nguyên vào body của entity.

## 7. Tiêu chí hoàn thành cho mỗi entity

Một file chỉ sẵn sàng để review khi:

- tên file và H1 khớp entity trong inventory;
- loại hình, tính chất tổ chức và ranh giới entity được diễn đạt chính xác;
- chương trình biểu diễn không bị đồng nhất với di sản, địa điểm hoặc lễ hội bao
  trùm;
- mọi claim quan trọng có evidence nguồn bên ngoài file answer-facing;
- URL do người dùng cung cấp đã được đọc và đối chiếu bằng web search độc lập;
- địa giới hành chính và địa điểm đã được kiểm tra theo hiện trạng tháng
  09/2026 qua nguồn chính thức;
- tên địa giới lịch sử và tên địa giới hiện hành được dùng đúng ngữ cảnh;
- trạng thái dự kiến, được chấp thuận, hoãn, hủy và đã diễn ra không bị trộn
  lẫn;
- mọi số liệu đều có năm, phạm vi, loại đo lường và nguồn công bố rõ ràng trong
  evidence;
- dữ liệu biến động được loại bỏ hoặc đặt trong kỳ tổ chức cụ thể;
- không có suy đoán, placeholder, văn phong quảng bá hoặc mâu thuẫn bị che giấu;
- section chuyên biệt phù hợp với loại entity, không điền template máy móc;
- không lặp nội dung đáng kể với entity di sản, lễ hội hoặc chương trình liên
  quan;
- Markdown bắt đầu bằng H1, không có frontmatter, section rỗng, bảng field dài,
  `## Nguồn dữ liệu` hoặc `Liên kết nội bộ`;
- mỗi section quan trọng đủ ngữ cảnh để hiểu độc lập;
- đã hoàn tất lượt self-verification độc lập sau khi biên soạn;
- nội dung cuối cùng đã được kiểm tra về tính chính xác, ổn định và rõ ràng.
