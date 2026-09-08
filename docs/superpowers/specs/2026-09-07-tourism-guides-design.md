# Thiết kế cẩm nang du lịch Huế tổng quan

Ngày thiết kế: 07/09/2026
Trạng thái: đã được người dùng duyệt bằng văn bản ngày 07/09/2026

## 1. Mục tiêu

Biên soạn `knowledge-base-hue/tourism/tourism_guides.md` thành cẩm nang tổng
quan duy nhất của toàn domain du lịch Huế. File giúp người dùng lựa chọn thời
điểm, thời lượng, phương tiện, khu vực và loại trải nghiệm phù hợp trước khi đi
sâu vào các file canonical chuyên biệt.

Cẩm nang phải chính xác tại mốc tháng 09/2026, ưu tiên tri thức bền vững, dùng
địa giới hành chính có hiệu lực từ ngày 01/07/2025 và không trở thành bản sao
của các guide về lịch trình, chi phí, vé, di sản, ẩm thực, lễ hội hoặc nghệ
thuật biểu diễn.

## 2. Quyết định canonical và phạm vi

`tourism/tourism_guides.md` là file canonical duy nhất cho intent cẩm nang du
lịch Huế tổng quan. Ứng viên `tourism/services/Cẩm nang du lịch Huế.md` được
loại khỏi inventory để không tồn tại hai tài liệu cùng phạm vi.

Nhánh `tourism/services/` tiếp tục giữ bốn guide chuyên biệt:

1. `Đến Huế nên đi đâu.md`;
2. `Lịch trình du lịch Huế ngắn ngày.md`;
3. `Lịch trình du lịch Huế 3 ngày 2 đêm.md`;
4. `Chi phí du lịch Huế.md`.

`tourism_guides.md` được phép tóm tắt logic lựa chọn, nhưng không chứa lịch
trình chi tiết từng ngày, bảng giá, danh bạ dịch vụ hoặc mô tả dài của từng
entity.

## 3. Đối tượng và nhu cầu trả lời

Cẩm nang phục vụ người lần đầu đến Huế và người cần xây khung chuyến đi trước
khi chọn lịch trình chi tiết. Nội dung phải trả lời được:

- Huế phù hợp với những kiểu chuyến đi nào;
- nên dành bao nhiêu thời gian;
- chọn thời điểm theo thời tiết, mục tiêu và khả năng chịu nóng hoặc mưa;
- cách đến Huế và lựa chọn phương tiện tại Huế;
- cách gom các khu vực để tránh di chuyển vòng;
- cách kết hợp di sản, ẩm thực, nghệ thuật, lễ hội, đô thị và thiên nhiên;
- cách lựa chọn theo sở thích, nhóm người và khả năng vận động;
- cách chọn khu vực lưu trú mà không quảng bá cơ sở cụ thể;
- hành lý, trang phục, ứng xử và an toàn;
- dữ liệu nào phải kiểm tra lại sát ngày đi.

## 4. Cấu trúc answer-facing

File dùng cấu trúc hỏi–đáp sau:

```markdown
# Cẩm nang du lịch Huế

## Du lịch Huế phù hợp với những kiểu chuyến đi nào?
## Lần đầu đến Huế nên dành bao nhiêu ngày?
## Nên du lịch Huế vào thời điểm nào?
## Đến Huế bằng những phương tiện nào?
## Di chuyển trong thành phố Huế như thế nào?
## Các khu vực du lịch Huế được phân bố ra sao?
### Khu vực Phú Xuân – Thuận Hóa và hai bờ sông Hương
### Khu vực Kim Long – Thủy Xuân
### Khu vực biển và đầm phá phía đông
### Khu vực Bạch Mã – Chân Mây – Lăng Cô
### Khu vực miền núi và du lịch cộng đồng
## Lần đầu đến Huế nên ưu tiên trải nghiệm gì?
## Chọn trải nghiệm du lịch Huế theo sở thích
## Du lịch Huế theo nhóm người như thế nào?
## Nên chọn khu vực lưu trú nào tại Huế?
## Cần chuẩn bị gì trước chuyến du lịch Huế?
## Điều chỉnh chuyến đi Huế khi nắng nóng hoặc mưa lớn
## Những lưu ý an toàn khi khám phá thiên nhiên Huế
## Quy tắc trang phục và ứng xử khi du lịch Huế
## Những thông tin nào cần kiểm tra lại trước ngày đi?
```

Không bổ sung một lịch trình 3 ngày 2 đêm rút gọn. Intent đó thuộc file chuyên
biệt trong `tourism/services/`.

## 5. Nguyên tắc nội dung

### 5.1. Khả năng đứng độc lập khi retrieval

- Mỗi H2/H3 nhắc rõ Huế, tên khu vực hoặc chủ thể đang được mô tả.
- Mỗi section mở bằng câu có chủ thể định danh rõ ràng trước danh sách.
- Không mở section bằng đại từ phụ thuộc vào chunk trước như “nơi đây” hoặc
  “khu vực trên”.
- Mỗi section chỉ cung cấp đủ ngữ cảnh cho intent của chính section đó.

### 5.2. Ranh giới liên domain

- Di sản và di tích: tóm tắt để lựa chọn; chi tiết thuộc `heritages`.
- Món ăn và cơ sở ẩm thực: chỉ nêu loại trải nghiệm; chi tiết thuộc `foods`.
- Lễ hội: nêu nguyên tắc kiểm tra lịch; chi tiết thuộc `festivals`.
- Nghệ thuật biểu diễn: dành khoảng thời gian trong hành trình; lịch và chương
  trình thuộc `performing_arts`.
- Điểm tự nhiên, chợ và phố đi bộ: tóm tắt theo vai trò trong cụm; mô tả chi
  tiết thuộc file entity trong `tourism`.
- Giá và chính sách vé: thuộc `tourism/tickets`.
- Lịch trình và ngân sách: thuộc bốn guide chuyên biệt trong
  `tourism/services`.

Không thêm mục `Liên kết nội bộ`, đường dẫn repository hoặc thuật ngữ nội bộ
vào nội dung answer-facing.

### 5.3. Dữ liệu bền vững và dữ liệu động

Cẩm nang có thể khóa các nguyên tắc bền vững như phân cụm địa lý, đặc điểm mùa
mưa/nắng, mức vận động tương đối, cách lựa chọn phương tiện và nhu cầu chuẩn bị.

Cẩm nang không khóa:

- giá vé, giá phòng, giá vận chuyển hoặc tổng ngân sách;
- giờ mở cửa, suất biểu diễn hoặc lịch phương tiện;
- tên nhà cung cấp, khách sạn, nhà hàng hoặc hãng vận chuyển;
- lịch sự kiện của một năm như lịch thường lệ;
- trạng thái mở cửa hoặc tiếp cận chưa có xác nhận hiện hành.

Khi dữ liệu động cần được nhắc, nội dung chỉ giải thích người dùng phải kiểm tra
chủ thể nào và vào thời điểm nào.

### 5.4. Địa giới hành chính

Địa chỉ hiện hành dùng cấu trúc `[địa điểm], [phường hoặc xã], thành phố Huế`.
Không dùng quận, huyện, thị xã hoặc tỉnh Thừa Thiên Huế trong địa chỉ hiện
hành.

Tên địa giới cũ chỉ được dùng khi cần giải thích lịch sử hoặc hỗ trợ nhận diện,
và phải phân biệt rõ với địa chỉ hiện hành. Mỗi địa chỉ cụ thể phải được xác
minh bằng Nghị quyết 1675/NQ-UBTVQH15 cùng nguồn chính quyền hoặc đơn vị quản lý
hiện hành; không suy đoán từ tên đường.

### 5.5. Văn phong và an toàn

- Dùng tiếng Việt hiện đại, khách quan và trực tiếp.
- Không dùng mỹ từ quảng bá, xếp hạng tuyệt đối hoặc bảo đảm an toàn.
- Không khuyên người dùng đi vào hành lang đường sắt, tuyến tự phát hoặc khu
  vực có rủi ro tiếp cận.
- Với biển, đầm phá, núi, suối và thác, nêu điều kiện áp dụng và yêu cầu kiểm
  tra thời tiết, trạng thái quản lý và cảnh báo tại chỗ.
- Không mặc định mọi du khách có xe máy, đủ thể lực hoặc cùng khả năng tiếp
  cận.

## 6. Logic lựa chọn và phân cụm

Cẩm nang sử dụng các cụm ở mức định hướng:

- **Phú Xuân – Thuận Hóa và hai bờ sông Hương:** lõi đô thị, di sản, chợ, phố
  đi bộ và trải nghiệm buổi tối;
- **Kim Long – Thủy Xuân:** chùa, nhà vườn, làng nghề, đồi và phần lớn tuyến
  lăng tẩm phía tây/tây nam;
- **Biển và đầm phá phía đông:** chọn theo điều kiện biển, thủy văn và mục tiêu
  trải nghiệm cộng đồng;
- **Bạch Mã – Chân Mây – Lăng Cô:** nhóm xa trung tâm cần dành quỹ thời gian
  riêng, không mặc định ghép Bạch Mã với toàn bộ tuyến ven biển trong một ngày;
- **Miền núi và du lịch cộng đồng:** phụ thuộc khoảng cách, điều kiện tiếp cận,
  trạng thái vận hành và quy tắc ứng xử với cộng đồng.

Cẩm nang không biến các cụm trên thành lịch trình bắt buộc. Khi dành một ngày
cho ngoại thành, người dùng được hướng dẫn chọn một nhánh phù hợp thay vì nhồi
nhiều hướng xa nhau.

## 7. Nguồn và research evidence

Mười lăm URL do người dùng cung cấp được dùng để nhận diện intent, câu hỏi và
logic hành trình. Không URL nào được coi là nguồn duy nhất cho địa giới, giá,
giờ, trạng thái vận hành, an toàn hoặc dữ kiện lịch sử quan trọng.

Thứ bậc kiểm chứng:

1. văn bản pháp luật, UBND thành phố Huế, cơ quan quản lý chuyên ngành và đơn
   vị trực tiếp vận hành;
2. cổng du lịch quốc gia, báo chí có quy trình biên tập và nguồn địa phương có
   căn cứ;
3. blog thương mại, hãng lữ hành, nền tảng đặt dịch vụ và bài SEO chỉ dùng để
   nhận diện intent hoặc phát hiện claim cần kiểm tra.

Claim về địa giới đối chiếu Nghị quyết 1675 và nguồn hiện hành. Claim về khí
hậu, giao thông, an toàn hoặc trạng thái hoạt động cần nguồn chính thức; khi có
mâu thuẫn hoặc tác động lớn, cần thêm nguồn độc lập thứ hai. Dữ kiện chưa xác
minh được bị loại khỏi bản thảo.

Research evidence nằm ngoài file answer-facing và ghi tối thiểu URL, ngày truy
cập, claim, nguồn xác nhận, tính thời điểm, mâu thuẫn và kết quả self-verification.
`tourism_guides.md` không có section `## Nguồn dữ liệu`.

## 8. Phạm vi thay đổi dự kiến

Implementation sau khi được duyệt chỉ sửa:

1. `knowledge-base-hue/tourism/tourism_guides.md`;
2. `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`;
3. `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`;
4. hồ sơ research evidence phù hợp cho cẩm nang tổng quan;
5. báo cáo implementation và handoff theo workflow của dự án.

Không sửa các entity tourism đang được session khác review, các guide chuyên
ngành hiện có hoặc runtime RAG.

## 9. Tiêu chí nghiệm thu

Implementation đạt yêu cầu khi:

- `tourism_guides.md` là cẩm nang tổng quan canonical duy nhất;
- inventory services chỉ còn đúng bốn guide chuyên biệt và không còn tham
  chiếu triển khai `services/Cẩm nang du lịch Huế.md`;
- inventory tourism ghi rõ vai trò và ranh giới của `tourism_guides.md`;
- cấu trúc H1/H2/H3 khớp thiết kế và mỗi section quan trọng đứng độc lập;
- không có lịch trình 3 ngày 2 đêm chi tiết, bảng giá hoặc danh bạ dịch vụ;
- không lặp mô tả dài từ entity hoặc guide chuyên ngành;
- mọi địa giới hiện hành dùng cấp xã/phường sau ngày 01/07/2025;
- mọi claim quan trọng truy ngược được tới evidence phù hợp;
- không có claim chưa xác minh, mỹ từ quảng bá hoặc bảo đảm an toàn;
- file bắt đầu bằng H1, không có YAML frontmatter, section rỗng,
  `## Nguồn dữ liệu` hoặc `Liên kết nội bộ`;
- research evidence ghi rõ lượt kiểm chứng độc lập sau khi hoàn thành bản thảo;
- exact diff không chứa thay đổi ngoài phạm vi và vượt qua `git diff --check`.

## 10. Review Contract

Mức rủi ro: **medium**, do nội dung answer-facing mới tổng hợp nhiều domain và
thay đổi quyết định canonical trong hai inventory, dù không đổi runtime.

Implementer phải cung cấp:

- bảng ánh xạ từng tiêu chí nghiệm thu tới file/section và evidence;
- danh sách claim quan trọng cùng nguồn, ngày kiểm tra và quyết định giữ/loại;
- bằng chứng địa giới cho mọi địa chỉ cụ thể xuất hiện trong guide;
- kết quả kiểm tra trùng lặp với các guide và entity liên quan;
- kết quả self-review Markdown, chunk independence và `git diff --check`;
- danh sách failed, skipped, partial hoặc chưa xác minh.

Reviewer sẽ kiểm tra độc lập:

- toàn bộ changed paths, untracked files và exact diff;
- quyết định canonical trong hai inventory;
- mọi H2/H3 và câu mở đầu về khả năng đứng độc lập;
- một mẫu có chủ đích của claim địa giới, khí hậu, giao thông và an toàn bằng
  nguồn trực tiếp;
- các claim bị ảnh hưởng bởi kết quả review cuối của entity tourism;
- trùng lặp liên domain, dữ liệu động và văn phong quảng bá;
- `git diff --check`.

Không dùng lại evidence cho claim đã thay đổi. Evidence của entity tourism chỉ
được dùng lại sau khi entity tương ứng đã đạt review kỹ thuật và claim, nguồn,
thời điểm cùng data flow không đổi.

Không được commit, push, sửa runtime, thay đổi active data hoặc mở rộng số guide
nếu chưa có quyền riêng.
