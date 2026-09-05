# Hướng dẫn và khuôn mẫu biên soạn di sản, di tích Huế

Tài liệu này định nghĩa nguyên tắc và cấu trúc gợi ý cho 28 file entity thuộc
`knowledge-base-hue/heritages/heritage/`. Danh sách tên file và ranh giới entity được khóa
tại `knowledge-base-hue/meta/heritage-entities-inventory.md`. Inventory là
tài liệu điều phối và phải được loại khỏi ingestion trong giai đoạn chunking đa
domain sau này.

## 1. Mục tiêu biên soạn

Mỗi file phải là một văn bản tri thức tự nhiên, chuẩn xác và sạch cho hệ thống
RAG, đồng thời đọc được như một bài viết thông tin hoàn chỉnh dành cho con
người. Không viết file như bản ghi cơ sở dữ liệu, phiếu kiểm kê máy móc hoặc
chuỗi field được điền cho đủ template.

Thứ tự ưu tiên:

```text
Chính xác và đúng phạm vi ghi danh
-> ranh giới entity rõ ràng
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
- Không điền nội dung suy đoán, không tạo placeholder và không viết “chưa có
  dữ liệu” để lấp chỗ trống.
- File ngắn nhưng chính xác tốt hơn file dài chứa diễn giải quảng bá, lặp lại
  hoặc chi tiết không kiểm chứng được.

### 2.2. Phân biệt đúng loại di sản và cấp ghi danh

Không dùng chung nhãn “Di sản thế giới UNESCO” cho mọi trường hợp. Nội dung phải
phân biệt chính xác:

- Di sản Văn hóa Thế giới theo Công ước 1972;
- Di sản văn hóa phi vật thể trong Danh sách đại diện của UNESCO;
- Di sản tư liệu thuộc Sổ đăng ký Ký ức Thế giới quốc tế;
- Di sản tư liệu thuộc Chương trình Ký ức Thế giới khu vực Châu Á - Thái Bình
  Dương;
- Di sản văn hóa phi vật thể quốc gia;
- di tích quốc gia đặc biệt, di tích quốc gia hoặc di tích cấp tỉnh.

Một công trình thành phần không được mô tả là tự nó được UNESCO ghi danh nếu
danh hiệu thực tế thuộc về toàn bộ Quần thể Di tích Cố đô Huế. Cách diễn đạt
phù hợp là “thuộc Quần thể Di tích Cố đô Huế được UNESCO ghi danh năm 1993”.

### 2.3. Ranh giới entity và chống trùng lặp

- Mỗi thực thể trong inventory có đúng một file canonical đặt trực tiếp trong
  `heritage/`.
- File tổng quan quần thể giải thích cấu trúc và quan hệ giữa các thành phần;
  file entity con tập trung vào lịch sử, đặc điểm và giá trị riêng của entity.
- Khi một công trình chưa được tách file, mô tả nó như một tiểu mục trong file
  cha, không viết một bài độc lập trá hình bên trong nhiều file.
- `Nhã nhạc`, `Bài Chòi` và tín ngưỡng thờ Mẫu chỉ có file entity trong
  `heritage/`; guide của `performing_arts/` chỉ được nhắc và định hướng người
  đọc, không tạo bản sao nội dung.
- `Tri thức dân gian về Bún bò Huế` là di sản tri thức; file Bún bò trong
  `foods/` tiếp tục là entity món ăn. Hai file không lặp lại các section dài về
  thành phần, chế biến, lịch sử và giá trị.

### 2.4. Tri thức bền vững và dữ liệu có tính thời điểm

- Ưu tiên lịch sử, kiến trúc, chức năng, giá trị, cộng đồng thực hành, nội dung
  tư liệu và quan hệ giữa các di sản.
- Một đợt trùng tu, thay đổi đơn vị quản lý hoặc trạng thái mở cửa chỉ được ghi
  khi quan trọng và phải gắn với mốc thời gian cụ thể.
- Không ghi giá vé cụ thể, giờ mở cửa, số điện thoại, lịch biểu diễn hoặc chính
  sách tham quan dễ hết hạn. Giá vé và loại vé thuộc domain `tickets`.
- Không biến trạng thái quan sát tại năm 2026 thành thuộc tính vĩnh viễn.

### 2.5. Nguồn và kiểm chứng

- Ưu tiên UNESCO, Bộ Văn hóa, Thể thao và Du lịch, Cục Di sản văn hóa, cơ quan
  lưu trữ quốc gia, chính quyền thành phố Huế, Trung tâm Bảo tồn Di tích Cố đô
  Huế và tài liệu nghiên cứu có căn cứ.
- Cẩm nang du lịch được dùng để nhận diện câu hỏi và nhu cầu tham quan, không
  làm nguồn duy nhất cho niên đại, xếp hạng, phạm vi di sản hoặc số liệu.
- **Cập nhật địa giới hành chính theo mốc hiện tại (2026):** Các URL do người
  dùng cung cấp có thể chứa dữ liệu cũ về địa giới hành chính (ví dụ: các bài viết
  cũ ghi Lăng Gia Long thuộc xã Hương Thọ hoặc phường Long Hồ, nhưng tính đến năm
  2026 đã được sáp nhập, điều chỉnh thành phường Kim Long...). Implementer bắt
  buộc phải chủ động dùng công cụ tìm kiếm web (web search) để tra cứu, đối chiếu
  và cập nhật chuẩn xác đơn vị hành chính hiện hành.
- **Đối chiếu URL và tự nghiên cứu kiểm tra (Self-research & Fact-checking):**
  Không sao chép thụ động thông tin từ URL được cấp. Phải dùng web search để đối
  chiếu lại thông tin từ URL. Khi tạo xong mỗi file entity, Implementer phải tiến
  hành bước tự kiểm tra lại (self-verification), độc lập research và web search
  để rà soát, xác thực lại tính chính xác của toàn bộ dữ kiện (địa điểm, niên đại,
  cấp ghi danh, hiện trạng bảo tồn) trước khi hoàn tất file.
- Khi nguồn mâu thuẫn, không tự hợp nhất. Implementer ghi lại nguồn, ngày truy
  cập, khác biệt và quyết định cần Reviewer xử lý.
- Theo quyết định của user, file entity không có section `## Nguồn dữ liệu`.
  Provenance phải được giữ trong implementation evidence hoặc research record
  nằm ngoài nội dung answer-facing.

### 2.6. Văn phong và khả năng đứng độc lập của section

- Dùng tiếng Việt hiện đại, khách quan, câu ngắn đến trung bình và mô tả trực
  tiếp.
- Tránh mỹ từ quảng bá như “tuyệt mỹ”, “độc nhất vô nhị”, “hùng vĩ bậc nhất”
  nếu đó không phải nhận định có nguồn và cần thiết để giải thích giá trị.
- Phân biệt dữ kiện lịch sử, truyền thuyết, ký ức dân gian và diễn giải hiện
  đại. Không trình bày truyền thuyết như sự kiện đã được kiểm chứng.
- Mỗi section quan trọng cần nhắc tên hoặc ngữ cảnh của entity một cách tự
  nhiên để vẫn hiểu được khi section trở thành một chunk độc lập.
- Không dùng thuật ngữ nội bộ như `canonical`, `chunk`, `metadata`, tên file
  hoặc đường dẫn repository trong nội dung answer-facing.

### 2.7. Markdown sạch

- File bắt đầu trực tiếp bằng `# <Tên di sản hoặc di tích>`.
- Không dùng YAML frontmatter.
- Không tạo section rỗng, placeholder hoặc bảng field dài.
- Không thêm `Liên kết nội bộ` vào body.
- Không bắt buộc dùng đường phân cách `---` giữa các section.

## 3. Cấu trúc lõi dùng chung

Các section dưới đây là khung gợi ý. Chỉ `#`, `## Thông tin chung`,
`## Tổng quan` và ít nhất một section nội dung đặc trưng của entity là bắt buộc.

```markdown
# <Tên di sản hoặc di tích>

## Thông tin chung

- **Tên chính thức:** <Tên chính thức hoặc tên phổ biến nhất>
- **Tên gọi khác / Tên chữ:** <Chỉ thêm khi có>
- **Loại hình:** <Loại hình chính xác>
- **Địa điểm / Phạm vi thực hành:** <Phù hợp với loại entity>
- **Niên đại / Thời kỳ hình thành:** <Chỉ thêm khi áp dụng>
- **Thuộc quần thể:** <Chỉ thêm khi có quan hệ quần thể>
- **Ghi danh / Xếp hạng:** <Tên danh hiệu, cấp và năm chính xác>
- **Nhân vật / Cộng đồng liên quan:** <Chỉ thêm khi có ích>

## Tổng quan

<Hai đến ba đoạn giới thiệu bản chất, vị trí trong lịch sử hoặc đời sống văn
hóa và lý do entity quan trọng.>

## Lịch sử hình thành và biến đổi

<Hoàn cảnh ra đời, các giai đoạn phát triển hoặc thay đổi quan trọng đã được
kiểm chứng.>

## <Section chuyên biệt theo loại entity>

<Nội dung cụ thể theo hướng dẫn tại mục 4.>

## Giá trị lịch sử và văn hóa

<Giải thích giá trị bằng dữ kiện cụ thể, không dùng lời tán dương chung chung.>

## Mối quan hệ với các di sản liên quan

<Chỉ tạo khi cần giải thích quan hệ cha - con, tránh nhầm lẫn hoặc tránh lặp
nội dung giữa các entity.>

## Bảo tồn và phát huy giá trị

<Chỉ ghi hoạt động hoặc trạng thái quan trọng có nguồn và mốc thời gian rõ.>

## Thông tin dành cho du khách

<Chỉ dùng cho địa điểm có thể tham quan; cung cấp thông tin bền vững và quy tắc
ứng xử hữu ích, không danh sách mẹo du lịch quảng bá.>
```

## 4. Section chuyên biệt theo loại entity

### 4.1. Di tích kiến trúc, lăng tẩm và địa điểm lịch sử

Các section phù hợp có thể gồm:

```markdown
## Kiến trúc, cảnh quan và các hạng mục tiêu biểu

## Chức năng trong lịch sử

## Nhân vật và sự kiện liên quan
```

Không ép mọi di tích phải được giải thích bằng phong thủy. Chỉ mô tả tiền án,
hậu chẩm, trục thần đạo, minh đường hoặc nguyên lý tương tự khi nguồn đáng tin
cậy xác nhận và thông tin đó giúp hiểu bố cục công trình.

Với lăng tẩm, ưu tiên làm rõ người được an táng, tên chữ của lăng, quá trình xây
dựng, bố cục, các công trình chính, cảnh quan và khác biệt với những lăng liên
quan. Không suy diễn tính cách của vị vua từ phong cách kiến trúc nếu nguồn
không trực tiếp hỗ trợ nhận định đó.

### 4.2. Di sản văn hóa phi vật thể

Các section phù hợp có thể gồm:

```markdown
## Hình thức và không gian thực hành

## Cộng đồng nắm giữ và trao truyền

## Thành tố nghệ thuật, nghi lễ hoặc tri thức

## Sức sống và hoạt động bảo vệ di sản
```

Không biến di sản sống thành một mô tả sân khấu cố định. Phải làm rõ ai thực
hành, thực hành trong bối cảnh nào, tri thức được truyền như thế nào và phạm vi
ghi danh có riêng Huế hay thuộc nhiều địa phương.

### 4.3. Di sản tư liệu

Các section phù hợp có thể gồm:

```markdown
## Thành phần và nội dung tư liệu

## Hình thức, chất liệu và kỹ thuật tạo tác

## Quá trình hình thành và lưu giữ

## Giá trị nghiên cứu và khả năng tiếp cận
```

Phải phân biệt nơi hình thành, nơi gắn với lịch sử Huế và nơi bộ sưu tập đang
được bảo quản. Không ngụ ý rằng toàn bộ Mộc bản hoặc Châu bản hiện được lưu giữ
tại Huế nếu nguồn chính thức cho biết địa điểm bảo quản khác.

### 4.4. File tổng quan quần thể hoặc hệ thống

File tổng quan giải thích phạm vi, cấu trúc và quan hệ giữa các thành phần. Nó
không sao chép toàn bộ lịch sử và mô tả kiến trúc từ các file entity con.

Các section phù hợp có thể gồm:

```markdown
## Phạm vi và các thành phần

## Cấu trúc không gian hoặc hệ thống

## Giá trị chung của quần thể

## Gợi ý tìm hiểu theo chủ đề
```

## 5. Thông tin dành cho du khách

Section này chỉ chứa thông tin bền vững và có ích, chẳng hạn:

- đặc điểm không gian ảnh hưởng đến khả năng di chuyển;
- yêu cầu trang phục và ứng xử tại nơi thờ tự hoặc khu vực tôn nghiêm;
- giới hạn tiếp cận mang tính ổn định và đã được xác minh;
- quan hệ địa lý tự nhiên với một điểm tham quan liền kề.

Không mặc định đưa “thời lượng tham quan khuyến nghị”, “mùa đẹp nhất”, tuyến đi
gộp nhiều điểm hoặc tình trạng miễn phí/thu phí vào mọi file. Những nội dung đó
dễ mang tính chủ quan hoặc thay đổi và chỉ được thêm khi có nhu cầu answer-facing
rõ cùng nguồn phù hợp.

## 6. Tiêu chí hoàn thành cho mỗi entity

Một file chỉ sẵn sàng để review khi:

- tên file và H1 khớp entity trong inventory (cho phép tiền tố số thứ tự từ `1 ` đến `28 ` theo chỉ đạo trực tiếp của người dùng để theo dõi tiến độ biên soạn);
- loại hình, phạm vi ghi danh và cấp xếp hạng được diễn đạt chính xác;
- mọi claim quan trọng có evidence nguồn bên ngoài file answer-facing;
- không có dữ liệu suy đoán, placeholder, văn phong quảng bá hoặc nguồn mâu
  thuẫn chưa được xử lý;
- section chuyên biệt phù hợp với loại entity, không điền template máy móc;
- dữ liệu biến động được loại bỏ hoặc gắn mốc thời gian phù hợp;
- không lặp nội dung đáng kể với file cha, file con hoặc domain khác;
- Markdown bắt đầu bằng H1, không có frontmatter, không có section
  `## Nguồn dữ liệu` và không có section rỗng;
- địa giới hành chính và địa điểm được kiểm tra, cập nhật chuẩn xác theo hiện
  trạng năm 2026 qua web search và văn bản chính thức;
- đã hoàn tất bước tự kiểm tra (self-verification), độc lập research và web
  search lại toàn bộ dữ kiện ngay sau khi biên soạn file;
- nội dung đủ tự nhiên và đủ ngữ cảnh để con người đọc trực tiếp cũng như để
  RAG chunk theo section trong giai đoạn sau.
