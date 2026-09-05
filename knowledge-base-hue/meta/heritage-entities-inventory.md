# Danh mục biên soạn di sản và di tích tiêu biểu ở Huế

Tài liệu này khóa phạm vi biên soạn đợt đầu cho domain `heritage`. Implementer
sẽ tạo đúng 28 file entity dưới đây, đặt trực tiếp trong
`knowledge-base-hue/heritages/heritage/`. Mỗi thực thể chỉ có một file canonical; không
tạo lại các thư mục phân loại `cultural_heritage`, `heritage_sites`,
`intangible_heritage` hoặc `monuments`.

Theo quyết định và chỉ đạo trực tiếp của người dùng, trong quá trình triển khai,
tên tập tin entity được phép lưu giữ tiền tố số thứ tự tương ứng từ `1 ` đến `28 `
(ví dụ: `1 Quần thể Di tích Cố đô Huế.md`, `10 Lăng Gia Long.md`) để tiện theo dõi
tiến độ thực hiện. Tiêu đề H1 bên trong tập tin luôn giữ đúng tên chuẩn của thực
thể không có tiền tố số.

File này là inventory điều phối biên soạn, không phải một entity di sản và
không được dùng thay cho nội dung answer-facing của 28 file canonical. Khi
thiết kế chunking đa domain, file inventory này phải được loại khỏi nguồn
ingestion.

## Di sản được UNESCO hoặc Bộ Văn hóa, Thể thao và Du lịch ghi danh

1. `Quần thể Di tích Cố đô Huế.md`
2. `Nhã nhạc cung đình Huế.md`
3. `Mộc bản triều Nguyễn.md`
4. `Châu bản triều Nguyễn.md`
5. `Thơ văn trên kiến trúc cung đình Huế.md`
6. `Cửu Đỉnh Huế.md`
7. `Thực hành tín ngưỡng thờ Mẫu Tam phủ của người Việt.md`
8. `Nghệ thuật Bài Chòi Trung Bộ.md`
9. `Tri thức dân gian về Bún bò Huế.md`

Hai di sản Bài Chòi và tín ngưỡng thờ Mẫu là di sản chung với các địa phương
khác; nội dung phải giải thích đúng mối liên hệ với Huế, không trình bày chúng
như di sản chỉ thuộc riêng Huế.

`Tri thức dân gian về Bún bò Huế.md` chỉ trình bày di sản tri thức, cộng đồng
thực hành, sự trao truyền, giá trị văn hóa và việc ghi danh. Nội dung món ăn,
thành phần và cách thưởng thức tiếp tục thuộc file canonical hiện có tại
`foods/local_specialties/Bún bò Huế.md`; không sao chép hai bài thành hai phiên
bản của cùng một nội dung.

## Lăng tẩm các vua triều Nguyễn tại Huế

10. `Lăng Gia Long.md`
11. `Lăng Minh Mạng.md`
12. `Lăng Thiệu Trị.md`
13. `Lăng Tự Đức.md`
14. `Lăng Dục Đức.md`
15. `Lăng Đồng Khánh.md`
16. `Lăng Khải Định.md`
17. `Lăng vua Hiệp Hòa.md`

File Lăng Dục Đức phải giải thích An Lăng là nơi an táng các vua Dục Đức,
Thành Thái và Duy Tân. File Lăng Tự Đức có thể trình bày Bồi Lăng và mối liên
hệ với vua Kiến Phúc. Lăng vua Hiệp Hòa là di tích lịch sử cấp tỉnh, không phải
thành phần được UNESCO ghi danh của Quần thể Di tích Cố đô Huế.

## Di tích vật thể nổi bật

18. `Kinh thành Huế.md`
19. `Đại Nội Huế.md`
20. `Chùa Thiên Mụ.md`
21. `Đàn Nam Giao.md`
22. `Hổ Quyền.md`
23. `Điện Hòn Chén.md`
24. `Cung An Định.md`
25. `Đàn Xã Tắc.md`
26. `Hải Vân Quan.md`
27. `Trường Quốc Học Huế.md`
28. `Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md`

## Ranh giới với các thực thể chưa tách file

Các công trình sau được trình bày như thành phần trong file cha ở đợt đầu,
không tạo thêm file canonical:

- `Đại Nội Huế.md`: Ngọ Môn, Điện Thái Hòa, Điện Kiến Trung, Thế Miếu,
  Hiển Lâm Các, Cung Diên Thọ và Duyệt Thị Đường;
- `Kinh thành Huế.md`: Kỳ Đài, Phu Văn Lâu, Nghinh Lương Đình và Trấn Bình
  Đài;
- `Quần thể Di tích Cố đô Huế.md`: tổng quan đầy đủ các thành phần được UNESCO
  ghi danh, bao gồm Văn Miếu, Võ Miếu, Điện Voi Ré và Trấn Hải Thành;
- `Hổ Quyền.md`: mối quan hệ giữa Hổ Quyền và Điện Voi Ré;
- `Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md`: các địa điểm
  thành phần tiêu biểu của hệ thống.

Chùa Từ Hiếu, Chùa Diệu Đế, Quốc Tử Giám Huế và Điện Long An chưa thuộc phạm
vi 28 file đợt đầu. Cầu Trường Tiền và Huyền Không Sơn Thượng được để lại cho
thiết kế domain `tourism` thay vì đưa vào heritage chỉ vì mức độ phổ biến với
du khách.

## Quy tắc triển khai

- Mỗi file phải tuân theo `knowledge-base-hue/meta/heritage-template.md`.
- Chỉ viết claim đã được đối chiếu với nguồn phù hợp; không dùng cẩm nang du
  lịch thương mại làm căn cứ duy nhất cho xếp hạng, niên đại hoặc phạm vi UNESCO.
- Không tạo `## Nguồn dữ liệu` trong file entity. Implementer giữ URL, ngày truy
  cập, claim được hỗ trợ và mâu thuẫn nguồn trong evidence/research record tách
  khỏi nội dung answer-facing.
- Không ghi giá vé, giờ mở cửa hoặc lịch hoạt động dễ hết hạn trong file
  heritage; dữ liệu vé thuộc domain `tickets`.
- Không tự mở rộng quá 28 file. Mọi đề xuất tách thêm entity cần một quyết định
  thiết kế mới.
