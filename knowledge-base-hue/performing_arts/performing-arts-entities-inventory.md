# Danh mục biên soạn sự kiện và chương trình nghệ thuật biểu diễn nổi bật ở Huế

Tài liệu này khóa phạm vi biên soạn đợt đầu cho domain `performing_arts` tại
thời điểm ngày 05/09/2026. Danh mục chỉ chọn những sự kiện hoặc chương trình
biểu diễn nổi tiếng, có tính đại diện cho Huế, được công chúng quan tâm hoặc có
bằng chứng rõ về quy mô và mức độ đón nhận. Đây không phải danh sách toàn bộ
hoạt động nghệ thuật biểu diễn từng được tổ chức tại Huế.

Implementer sẽ tạo đúng 11 file entity dưới đây, đặt trực tiếp trong
`knowledge-base-hue/performing_arts/`. Mỗi thực thể chỉ có một file canonical;
không tạo lại các thư mục phân loại `artists`, `costumes`, `instruments`,
`masks`, `nha_nhac`, `stage-props`, `terminology` hoặc `tuong`.

File này là inventory điều phối biên soạn, không phải một entity nghệ thuật
biểu diễn và không được dùng thay cho nội dung answer-facing của 11 file
canonical. Khi thiết kế chunking đa domain, file inventory này phải được loại
khỏi nguồn ingestion.

## Trải nghiệm biểu diễn truyền thống tiêu biểu

1. `Ca Huế trên sông Hương.md`
2. `Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`

File `Ca Huế trên sông Hương.md` tập trung vào trải nghiệm biểu diễn trên sông,
đặc trưng chương trình và mối quan hệ với di sản Ca Huế. Không trình bày Ca Huế
như một loại hình chỉ tồn tại trên thuyền hoặc đồng nhất mọi không gian diễn
xướng Ca Huế với dịch vụ trên sông Hương.

File `Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md` tập trung vào
chương trình biểu diễn Nhã nhạc, múa cung đình và Tuồng cung đình dành cho công
chúng. Lịch sử, giá trị UNESCO và hệ thống bài bản của Nhã nhạc tiếp tục thuộc
file canonical `knowledge-base-hue/heritages/heritage/2 Nhã nhạc cung đình Huế.md`; lịch
sử kiến trúc Duyệt Thị Đường tiếp tục là nội dung thành phần của
`knowledge-base-hue/heritages/heritage/19 Đại Nội Huế.md`.

## Chương trình nghệ thuật gắn với Festival Huế

3. `Tuần lễ Festival Nghệ thuật Quốc tế Huế.md`
4. `Lễ hội đường phố Sắc màu văn hóa.md`
5. `Đêm nhạc Trịnh Công Sơn tại Huế.md`
6. `Tuần lễ Âm nhạc Quốc tế Huế.md`
7. `Huế Symphony – Bản Giao hưởng Cố đô.md`

Các file trong nhóm này chỉ trình bày chương trình biểu diễn tương ứng, quá
trình hình thành, những kỳ tổ chức tiêu biểu, nghệ thuật được giới thiệu và mức
độ đón nhận của công chúng. Không sao chép phần tổng quan Festival bốn mùa đã
thuộc file canonical `knowledge-base-hue/festivals/festival/Festival Huế.md`.

`Đêm nhạc Trịnh Công Sơn tại Huế.md` là entity cho chuỗi chương trình tưởng
niệm và trình diễn nhạc Trịnh tại Huế qua nhiều kỳ, không khóa canonical entity
vào riêng chủ đề của năm 2022, 2024 hoặc 2026.

## Đại nhạc hội và chương trình biểu diễn đương đại tạo dấu ấn

8. `Mega Booming – Huế.md`
9. `Huế by Light – The Live Show.md`
10. `Đêm Hoàng cung – Dạ yến Hoàng cung.md`
11. `Huế Wonderverse Music Fest.md`

`Mega Booming – Huế.md` phải phản ánh đúng diễn biến: kế hoạch tháng 4/2025 bị
hoãn, sau đó chương trình thực tế được tổ chức vào tháng 7/2025 và có đợt thứ
hai vào tháng 12/2025. Không dùng số vé dự kiến của kế hoạch ban đầu thay cho
số khán giả thực tế.

`Huế by Light – The Live Show.md` là chương trình âm nhạc và trình diễn ánh
sáng tại Ngọ Môn năm 2023. Đây là một production nổi bật diễn ra trong một kỳ
cụ thể, không mô tả như chương trình thường niên nếu chưa có căn cứ.

`Đêm Hoàng cung – Dạ yến Hoàng cung.md` trình bày quan hệ giữa định dạng Đêm
Hoàng cung trong các kỳ Festival trước và chương trình Dạ yến Hoàng cung được
phát triển lại năm 2026. Nội dung tập trung vào nghi thức và nghệ thuật trình
diễn; không biến file thành bài giới thiệu nhà hàng hoặc thực đơn.

`Huế Wonderverse Music Fest.md` ghi rõ kỳ 2026 là lần tổ chức đầu tiên và định
hướng phát triển thành sự kiện thường niên giai đoạn 2026–2030. Không trình bày
số khán giả kỳ vọng trước sự kiện như số người tham dự thực tế khi chưa có báo
cáo tổng kết đáng tin cậy.

## Ranh giới với domain lễ hội và di sản

Không tạo thêm file trong `performing_arts` cho các entity đã có canonical file
ở domain khác:

- `Festival Huế.md` và `Lễ hội Áo dài Huế.md` tiếp tục thuộc
  `knowledge-base-hue/festivals/festival/`;
- `Nhã nhạc cung đình Huế.md` tiếp tục thuộc `knowledge-base-hue/heritages/heritage/`;
- các chương trình khai mạc, bế mạc hoặc chủ đề thay đổi theo từng năm được
  trình bày trong file sự kiện cha phù hợp, không mặc định tách thành entity;
- nghệ sĩ, nhạc cụ, trang phục, mặt nạ, đạo cụ, thuật ngữ và từng trích đoạn
  biểu diễn riêng lẻ chưa thuộc phạm vi 11 file đợt đầu.

## Quy tắc triển khai

- Dùng tên file canonical trong inventory; H1 bên trong file phải trùng tên
  thực thể, có thể bỏ phần alias sau dấu gạch nếu câu chữ tự nhiên hơn.
- Chỉ viết claim đã được đối chiếu với nguồn chính thức hoặc báo chí đáng tin
  cậy; số liệu khán giả phải phân biệt rõ `thực tế`, `ước tính` và `kỳ vọng`.
- Với chương trình có nhiều kỳ tổ chức, tách đặc trưng ổn định khỏi thông tin
  riêng của từng năm; không suy diễn một lịch biểu, nghệ sĩ hoặc địa điểm thành
  thuộc tính cố định của toàn chuỗi.
- Không tạo `## Nguồn dữ liệu` trong file entity. URL, ngày truy cập, claim được
  hỗ trợ và mâu thuẫn nguồn phải được giữ trong evidence/research record tách
  khỏi nội dung answer-facing.
- Không ghi giá vé, lịch diễn hoặc thông tin bán vé dễ hết hạn; dữ liệu vé thuộc
  domain `tickets`.
- Không tự mở rộng quá 11 file. Mọi đề xuất thêm entity cần một quyết định phạm
  vi mới.
