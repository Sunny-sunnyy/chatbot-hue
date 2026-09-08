# Thiết kế lại tối giản bốn cẩm nang dịch vụ du lịch Huế

Ngày thiết kế: 08/09/2026
Trạng thái: được người dùng duyệt ngày 08/09/2026

## 1. Mục tiêu

Viết lại bốn cẩm nang trong `knowledge-base-hue/tourism/services/` thành các
tài liệu ngắn, tự nhiên và dễ dùng. Mỗi tài liệu chỉ trả lời đúng nhu cầu của
mình, không lặp nội dung chi tiết đã thuộc các cẩm nang di sản, ẩm thực, nghệ
thuật biểu diễn, điểm đến hoặc vé tham quan.

Bốn cẩm nang tiếp tục nằm dưới `tourism/services/`. Công việc này không đổi tên
hoặc di chuyển nhánh `tourism/`, không mở rộng ingestion, Golden, Qdrant,
runtime hoặc Agentic RAG.

## 2. Phạm vi thực hiện

### Nội dung chính

1. `Đến Huế nên đi đâu.md`;
2. `Lịch trình du lịch Huế ngắn ngày.md`;
3. `Lịch trình du lịch Huế 3 ngày 2 đêm.md`;
4. `Chi phí du lịch Huế.md`.

### Tài liệu hỗ trợ cần đồng bộ

1. Mục XL–XLIII trong `knowledge-base-hue/meta/tourism-research-evidence.md`;
2. báo cáo triển khai của đợt viết lại;
3. `session_prompt/CURRENT_HANDOFF.md`.

Không sửa inventory, cẩm nang canonical liên domain hoặc file ngoài phạm vi
trên nếu không phát hiện một mâu thuẫn làm thay đổi acceptance. Nếu có mâu
thuẫn như vậy, dừng phần liên quan và xin quyết định của người dùng.

## 3. Nguyên tắc chung

- Nội dung Markdown phải tự nhiên, rõ ràng và chỉ chứa thông tin cần thiết cho
  mục đích của tài liệu.
- Không dùng mã định danh kỹ thuật, nhãn kiểm thử, thuật ngữ RAG, đường dẫn
  repository hoặc ghi chú quy trình trong bốn cẩm nang dành cho người đọc.
- Không dùng nhãn khẳng định tuyệt đối hoặc tuyên bố thực địa khi không có hồ
  sơ khảo sát thực tế.
- Không dùng mỹ từ quảng bá, xếp hạng tuyệt đối hoặc bảo đảm an toàn.
- Không khóa giờ đồng hồ cụ thể trong lịch trình. Dùng đầu, giữa hoặc cuối buổi
  cùng thời lượng tương đối và khoảng đệm di chuyển.
- Không mặc định mọi du khách có xe máy, đủ thể lực hoặc cùng khả năng tiếp
  cận.
- Dữ liệu động chỉ được giữ khi có nguồn trực tiếp, ngày nguồn, ngày truy cập
  và phạm vi hỗ trợ phù hợp. Nếu không đủ căn cứ, nội dung phải được xóa hoặc
  chuyển thành hướng dẫn kiểm tra trước chuyến đi.
- Địa chỉ hiện hành dùng cấp phường hoặc xã có hiệu lực từ ngày 01/07/2025.

Giới hạn mềm cho mỗi cẩm nang là khoảng 120–180 dòng. Chất lượng và sự đầy đủ
của intent quan trọng hơn việc đạt một số dòng cố định.

## 4. Vai trò và cấu trúc từng cẩm nang

### 4.1. Đến Huế nên đi đâu

Cẩm nang giúp người đọc chọn khu vực và loại trải nghiệm, không đóng vai trò
danh sách mô tả chi tiết từng địa điểm.

Cấu trúc dự kiến:

1. cách chọn theo quỹ thời gian;
2. cách chọn theo sở thích;
3. cách chọn theo nhóm khách và khả năng vận động;
4. cách chọn theo thời tiết;
5. năm cụm địa lý, mỗi cụm chỉ nêu vai trò, thời lượng và điều kiện chính;
6. thông tin cần kiểm tra trước chuyến đi.

Mỗi điểm đến chỉ được nhắc ở mức đủ để người đọc quyết định chọn hay không.
Lịch sử, kiến trúc, hiện vật, món ăn và chương trình biểu diễn được điều phối
sang cẩm nang chuyên ngành bằng tên gọi tự nhiên.

### 4.2. Lịch trình du lịch Huế ngắn ngày

Cẩm nang sở hữu các hành trình nửa ngày, một ngày và hai ngày một đêm.

Cấu trúc dự kiến:

1. nguyên tắc gom tuyến và chừa khoảng đệm;
2. lịch trình nửa ngày;
3. lịch trình một ngày;
4. lịch trình hai ngày một đêm;
5. cách thay đổi khi mưa, nắng nóng hoặc có người hạn chế vận động;
6. checklist trước khi khởi hành.

Các hành trình dùng khung buổi và thời lượng tương đối. Biến thể theo ga Huế,
sân bay Phú Bài hoặc Đà Nẵng chỉ giữ khi làm thay đổi tuyến; không dùng bảng
giờ phương tiện hoặc lịch cố định.

### 4.3. Lịch trình du lịch Huế 3 ngày 2 đêm

Cẩm nang này là nơi duy nhất sở hữu lịch trình ba ngày hai đêm.

Cấu trúc dự kiến:

1. nguyên tắc phân bổ ba ngày;
2. một lịch trình mặc định;
3. tối đa ba module thay thế: biển và đầm phá; làng nghề và nghỉ dưỡng; gia
   đình có người hạn chế vận động;
4. cách điều chỉnh theo thời tiết và trạng thái điểm đến;
5. checklist trước chuyến đi.

Vườn quốc gia Bạch Mã không nằm trong lịch trình hoặc module mặc định. Cẩm nang
chỉ nhắc người đọc liên hệ Ban quản lý để kiểm tra thông báo mở tuyến và điều
kiện an toàn trong ngày. Chỉ được bổ sung tuyến cụ thể khi có thông báo trực
tiếp mới hơn nguồn tháng 06/2026 và xác nhận rõ phạm vi tiếp cận.

### 4.4. Chi phí du lịch Huế

Cẩm nang hướng dẫn cách lập ngân sách, không trở thành bảng giá dịch vụ hoặc
canonical thứ hai cho vé tham quan.

Cấu trúc dự kiến:

1. công thức tổng ngân sách;
2. cách tách chi phí liên tỉnh khỏi chi phí tại Huế;
3. một tập nhỏ các đầu vào đại diện;
4. ba bảng dự toán cho một ngày, hai ngày một đêm và ba ngày hai đêm;
5. cách điều chỉnh theo quy mô nhóm;
6. quỹ dự phòng và các khoản cần kiểm tra lại.

Chỉ giữ tối đa mười đầu vào giá động. Mỗi đầu vào phải có một dòng bằng chứng
khớp đúng khoảng giá trong cẩm nang. Không giữ giá từng điểm tham quan, nhà cung
cấp cụ thể, nhiều phân khúc phòng chi li hoặc các bảng ngân sách lặp lại theo
từng kiểu khách.

## 5. An toàn và khả năng tiếp cận

- Bạch Mã giữ cách xử lý thận trọng nêu trên cho tới khi có thông báo mới đủ
  thẩm quyền và đúng phạm vi.
- Chèo SUP trên sông Hương chỉ giữ ba yêu cầu được nguồn Hue-S hỗ trợ: mặc áo
  phao, có thiết bị cứu sinh và tránh luồng tàu du lịch.
- Ca Huế trên sông Hương phải dùng văn bản hoặc thông báo trực tiếp về quản lý
  bến thuyền và vận tải đường thủy. Không suy ra giá hoặc điều kiện xuất bến từ
  trang chủ của website.
- Với người cao tuổi, trẻ nhỏ hoặc người hạn chế vận động, không khẳng định xe
  đỗ sát, đường bằng phẳng, số bậc, xe điện hoặc lối tiếp cận nếu chưa có nguồn
  trực tiếp. Khi chưa đủ căn cứ, chỉ hướng dẫn liên hệ đơn vị quản lý trước.
- Hoạt động trên sông, biển, đầm phá, suối hoặc đồi chỉ là lựa chọn có điều
  kiện, phụ thuộc thời tiết, cảnh báo và trạng thái vận hành trong ngày.

## 6. Research evidence

Mục XL–XLIII dùng bảng tiếng Việt tự nhiên với các trường:

- nội dung cần kiểm chứng;
- URL trang hoặc tài liệu trực tiếp;
- chủ thể nguồn;
- ngày nguồn;
- ngày truy cập;
- phạm vi nguồn hỗ trợ;
- tính ổn định hoặc biến động của thông tin;
- quyết định biên tập và vị trí nội dung sử dụng.

Trang chủ của website không được tính là nguồn trực tiếp. Một nguồn tổng hợp không được dùng
để bảo chứng các khoảng giá hoặc điều kiện vận hành mà trang nguồn không nêu.
Evidence không dùng mã định danh, nhãn tuyệt đối hoặc lời tự nghiệm thu.

## 7. Đồng bộ và báo cáo

Báo cáo triển khai phải mô tả thay đổi thực tế bằng ngôn ngữ tự nhiên. Với mỗi
thông tin động, an toàn, pháp lý, địa giới hoặc giá còn giữ, báo cáo chỉ ra mục
trong cẩm nang và dòng bằng chứng tương ứng bằng tên nội dung, không dùng mã
kỹ thuật.

Báo cáo không tự tuyên bố đã nghiệm thu. Kết quả lệnh phải ghi đúng exit code,
output và giới hạn, đặc biệt với file untracked và
`git diff --no-index --check`.

## 8. Kiểm tra và nghiệm thu

Sau khi viết lại, Implementer phải:

1. đọc lại toàn bộ bốn cẩm nang và Mục XL–XLIII;
2. kiểm tra ranh giới canonical, văn phong, địa giới, Bạch Mã, SUP, Ca Huế và
   khả năng tiếp cận;
3. tính lại từng cận thấp và cao trong các bảng ngân sách;
4. đối chiếu từng giá còn giữ với evidence trực tiếp;
5. kiểm tra frontmatter, URL ngoài, wiki-link, tên file `.md`, mục nguồn nội
   bộ, metadata, nhãn tuyệt đối và giờ đồng hồ cố định trong cẩm nang;
6. chạy `git diff --check` và kiểm tra no-index cho từng file untracked;
7. ghi trung thực phần chưa chạy, không xác minh được hoặc chỉ kiểm tra một
   phần.

Nghiệm thu đạt khi không còn lỗi nghiêm trọng; bốn cẩm nang đúng vai trò, mọi
thông tin rủi ro cao truy vết được, các phép cộng đúng và cẩm nang, hồ sơ bằng
chứng, báo cáo mô tả cùng một trạng thái thực tế.

Kết quả cuối được bàn giao cho một lượt review độc lập mới. Người triển khai
không tự nghiệm thu implementation của mình.

## 9. Quyền và giới hạn

- Người dùng đã cho phép Codex trực tiếp triển khai sau khi spec và plan được
  duyệt.
- Không dùng sub-agent trong implementation này.
- Git authorization là `none`; không commit hoặc push.
- Không xóa/reset thay đổi ngoài scope.
- Không sửa runtime hoặc dữ liệu đang hoạt động.
