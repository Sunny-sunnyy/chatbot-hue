# Danh mục tên lễ hội ở Huế – Research Inventory
> **Ngày research:** 30/08/2026
> **Mục đích:** làm inventory đầu vào cho `knowledge-base-hue/festivals/` của dự án chatbot/RAG về Huế.
> **Số tên có định danh cụ thể đã tổng hợp trong file này:** **100**. Ngoài ra có 12 loại hình/tên gọi chung và 4 nhãn mùa của Festival Huế được tách riêng để tránh tạo duplicate entity.
## 1. Lưu ý rất quan trọng về chữ “toàn bộ”
Qua rà soát năm 2025, **Sở Văn hóa và Thể thao TP Huế cho biết trên địa bàn có khoảng 520 lễ hội**, gồm **472 lễ hội truyền thống, 23 lễ hội văn hóa, 20 lễ hội ngành nghề và 5 lễ hội có nguồn gốc từ nước ngoài**. Đề tài xây dựng CSDL lễ hội của Huế cũng công bố cùng con số 520.

Do đó, các bài viết kiểu “10 lễ hội Huế”, “11 lễ hội Huế” chỉ là danh sách **tiêu biểu**, không phải toàn bộ hệ thống lễ hội. Website công khai `lehoi.hue.gov.vn` hiện xác nhận quy mô CSDL nhưng giao diện danh sách không xuất toàn bộ 520 tên trong HTML/index công khai mà công cụ tìm kiếm có thể thu hồi. Vì vậy, **không nên gọi bất kỳ danh sách vài chục tên nào là danh mục chính thức đầy đủ 520 lễ hội** nếu chưa có export từ CSDL quản lý của Sở.

File này vì thế được thiết kế theo nguyên tắc: **liệt kê toàn bộ tên cụ thể mà quá trình research công khai lần này tìm thấy và có căn cứ**, đồng thời ghi rõ các loại hình chung và các tên cần chuẩn hóa. Đây là master research inventory để tiếp tục xây corpus, **không giả vờ là bản export 520/520 của Sở**.
## 2. Danh sách tên lễ hội/sự kiện lễ hội có định danh cụ thể

### A. Festival, lễ hội văn hóa – du lịch và các ngày hội có tên riêng
1. **Festival Huế** — Umbrella festival; hiện tổ chức theo định hướng Festival bốn mùa.
2. **Festival Nghề truyền thống Huế** — Festival chuyên đề về nghề thủ công truyền thống.
3. **Lễ hội Áo dài Huế** — Tên thường dùng trong các kỳ Festival Huế.
4. **Tuần lễ Áo dài cộng đồng Huế** — Chương trình cộng đồng về áo dài; không nên tự động đồng nhất với Lễ hội Áo dài Huế.
5. **Lễ hội Ẩm thực Huế** — Tên tổng quát xuất hiện trong các nguồn du lịch/Festival.
6. **Lễ hội Ẩm thực chay – Festival Huế** — Có chương trình riêng trong Festival Huế 2026.
7. **Tuần lễ Festival Nghệ thuật Quốc tế Huế** — Điểm nhấn nghệ thuật quốc tế trong Festival Huế.
8. **Tuần lễ Âm nhạc Quốc tế Huế** — Sự kiện âm nhạc quốc tế trong Festival Huế.
9. **Lễ hội Khinh khí cầu quốc tế tại Huế** — Được Khám Phá Huế xếp trong nhóm lễ hội có nguồn gốc/yếu tố nước ngoài.
10. **Ngày hội Sen Huế** — Sự kiện văn hóa – du lịch tôn vinh sen Huế.
11. **Ngày hội Hoàng Mai Huế** — Ngày hội tôn vinh Hoàng mai Huế.
12. **Ngày hội Thơ Huế** — Chuỗi hoạt động gắn Ngày thơ Việt Nam/Festival Huế.
13. **Lễ hội làng Dương Nỗ** — Lễ hội văn hóa tại làng Dương Nỗ.
14. **Lễ hội đường phố “Sắc màu văn hóa”** — Chương trình trong Festival Huế; nên giữ trạng thái program/sub-event.
15. **Lễ hội hoa đăng** — Chương trình trong Festival Huế; cần gắn năm/đợt khi xây entity.
16. **Lễ hội Bia** — Chương trình/sự kiện trong một số kỳ Festival; không phải lễ hội truyền thống.
17. **Hội đèn lồng Quốc tế Huế** — Tên chương trình được các nguồn Festival/du lịch nhắc đến.
18. **Ngày hội Lân Huế** — Sự kiện/Ngày hội Lân; có các chương trình quảng diễn Lân – Sư – Rồng liên quan.
19. **Lễ hội Thuận An Biển gọi** — Nguồn chính thức cũng dùng biến thể “Chương trình Thuận An biển gọi”.
20. **Lễ hội Lăng Cô – Vịnh đẹp thế giới** — Lễ hội/ngày hội văn hóa, thể thao, du lịch ở Lăng Cô.
21. **Lễ hội Thanh Trà Huế** — Lễ hội sản vật; năm 2026 tổ chức lần thứ VIII.
22. **Chợ quê ngày hội** — Gắn với không gian Cầu ngói Thanh Toàn/Thanh Thủy Chánh.
23. **Lễ hội Hương xưa làng cổ** — Gắn với làng cổ Phước Tích.
24. **Lễ hội Sóng nước Tam Giang** — Một số năm/nguồn dùng biến thể “Sông nước Tam Giang”.
25. **Hội Vui Xuân** — Được CSDL lễ hội Huế liệt kê trong nhóm lễ hội văn hóa.

### B. Lễ hội truyền thống, cung đình, làng xã, tín ngưỡng và thể thao dân gian
26. **Lễ hội Điện Huệ Nam (Điện Hòn Chén)** — Tên chuẩn nên ưu tiên “Điện Huệ Nam”; “Điện Hòn Chén” là alias rất phổ biến.
27. **Lễ hội Cầu ngư làng Thai Dương Hạ** — Một lễ hội Cầu ngư cụ thể, không nên gom tất cả Cầu ngư thành một entity.
28. **Lễ hội Cầu ngư Thuận An** — Cổng lễ hội quốc gia ghi địa điểm đình làng Thai Dương Thượng.
29. **Lễ hội Cầu ngư Quảng An** — Cổng lễ hội quốc gia ghi địa điểm Miếu Đại Càn.
30. **Lễ hội Cầu Ngư Lăng Cô** — Lễ hội Cầu ngư riêng tại Lăng Cô.
31. **Lễ hội Cầu ngư các xã làng biển** — Bản ghi tổng hợp cho các làng biển Điền Hương, Điền Lộc, Điền Môn, Điền Hòa, Phong Hải.
32. **Lễ tế Nam Giao** — Nghi lễ cung đình triều Nguyễn được phục dựng.
33. **Lễ tế Xã Tắc** — Nghi lễ tại Đàn Xã Tắc.
34. **Lễ cúng Âm hồn** — Tín ngưỡng/lễ cúng cộng đồng ở Huế.
35. **Lễ tế đền Chiêu Ứng** — Lễ tế tại đền Chiêu Ứng.
36. **Lễ tế miếu Tiên Y** — Được CSDL lễ hội Huế liệt kê trong nhóm lễ hội truyền thống.
37. **Lễ tế đình La Chử** — Được CSDL lễ hội Huế liệt kê.
38. **Lễ tế đình Cổ Lão** — Được CSDL lễ hội Huế liệt kê.
39. **Lễ Thu tế làng An Cựu** — Lễ Thu tế làng.
40. **Lễ Thu tế làng Kim Long** — Lễ Thu tế làng.
41. **Lễ Thu tế làng Lương Quán** — Lễ Thu tế làng.
42. **Lễ Thu tế làng Nguyệt Biều** — Lễ Thu tế làng.
43. **Lễ Thu tế làng Phú Xuân** — Lễ Thu tế làng.
44. **Lễ Thu tế làng Thần Phù** — Lễ Thu tế làng.
45. **Lễ Thu tế làng Thanh Thủy Chánh** — Khám Phá Huế có bài riêng.
46. **Lễ Thu tế làng An Truyền** — Cổng lễ hội quốc gia có bản ghi riêng.
47. **Lễ tế Cô hồn làng Trúc Lâm** — Cổng lễ hội quốc gia ghi “Lế tế Cô hồn làng Trúc Lâm”; đã chuẩn hóa lỗi chính tả.
48. **Lễ kỵ bà Trần Thị Đạo** — Gắn với Cầu ngói Thanh Toàn.
49. **Lễ tế Chùa Ba Đồn** — Bản ghi lễ hội truyền thống trên cổng quốc gia.
50. **Lễ tế Bà Tơ** — Bản ghi tại Miếu Bà Tơ, khu vực Quảng Phú.
51. **Lễ hội đền Huyền Trân Công chúa** — Nguồn chính thức hiện vẫn tổ chức thường niên đầu xuân.
52. **Lễ Ban Sóc triều Nguyễn** — Nghi lễ phát lịch triều Nguyễn; hiện là chương trình mở đầu Festival Huế nhiều năm.
53. **Lễ Nguyên đán triều Nguyễn** — Nghi lễ triều hội Tết Nguyên đán được phục dựng.
54. **Lễ hội Quang Trung (Lễ Đăng quang Hoàng đế Quang Trung)** — Gắn với Núi Bân.
55. **Hội vật làng Sình** — Lễ hội vật truyền thống nổi tiếng ở làng Sình.
56. **Hội vật làng Thủ Lễ** — Lễ hội vật truyền thống tại Thủ Lễ.
57. **Hội đu tiên An Gia – Phước Yên** — Bản ghi cổng lễ hội quốc gia.
58. **Hội Đu tiên Phong Hiền / Gia Viên** — Bản ghi cổng lễ hội quốc gia; địa điểm Gia Viên, làng Thế Chí Tây.
59. **Lễ hội Đu tiên Phú Gia** — Lễ hội đu tiên được phục dựng tại khu vực Phú Lộc cũ.
60. **Chợ phiên Quảng Ngạn** — Được cổng lễ hội quốc gia xếp là lễ hội truyền thống.
61. **Chợ quê ngày Tết Vinh Mỹ** — Bản ghi cổng lễ hội quốc gia.
62. **Hội Mai Xuân Điền Hòa** — Bản ghi “Hội Mai Xuân” tại Điền Hòa.
63. **Hội Minh Hương** — Tên lễ hội cổ truyền được các nguồn du lịch và tư liệu địa phương ghi nhận.
64. **Hội Thanh Phước** — Lễ hội làng truyền thống được tư liệu địa phương ghi nhận.
65. **Hội đình làng Phú Xuân** — Lễ hội đình làng tại khu vực Phú Xuân.
66. **Hội An Truyền** — Tên lịch sử/tư liệu; cần đối chiếu với bản ghi Thu tế làng An Truyền để tránh duplicate entity.
67. **Hội làng Cổ Bi** — Lễ hội làng ở khu vực Phong Điền cũ.
68. **Hội làng Chí Long** — Lễ hội làng ở khu vực Phong Điền cũ.
69. **Hội xuân Gia Lạc** — Hội xuân truyền thống đầu năm.
70. **Hội đua thuyền trên sông Hương** — Cổng lễ hội quốc gia có bản ghi riêng.
71. **Lễ hội đua ghe truyền thống Huế** — Tên thường gặp; có giải đua ghe truyền thống thành phố Huế.
72. **Đua ghe thị trấn Sịa** — Bản ghi lễ hội truyền thống ở Sịa.
73. **Đua trải trên sông Vực** — Bản ghi lễ hội truyền thống trên cổng quốc gia.
74. **Lễ hội Bài Chòi Huế** — Sở VHTT Huế mô tả hoạt động lễ hội Bài Chòi mùa xuân, tiêu biểu tại Cầu ngói Thanh Toàn.

### C. Lễ hội tôn giáo và tín ngưỡng có phạm vi rộng
75. **Lễ Phật Đản tại Huế** — Có biến thể tên hiện hành “Tuần lễ Phật đản Huế”.
76. **Lễ Vu Lan tại Huế** — Được CSDL lễ hội Huế liệt kê.
77. **Lễ hội Quán Thế Âm tại Huế** — Năm 2026 tổ chức tại Trung tâm Du lịch tâm linh Phật giáo Quán Thế Âm, núi Tứ Tượng.
78. **Lễ Giáng sinh tại Huế** — Được CSDL lễ hội Huế liệt kê trong nhóm lễ hội văn hóa/tôn giáo.

### D. Lễ hội ngành nghề
79. **Lễ giỗ Tổ nghề Đúc đồng** — CSDL lễ hội Huế liệt kê.
80. **Lễ Giỗ Tổ nghề Kim hoàn** — Có bài riêng trên Khám Phá Huế.
81. **Lễ giỗ Tổ Thợ may** — CSDL lễ hội Huế liệt kê.
82. **Lễ giỗ Tổ nghề Thêu** — CSDL lễ hội Huế liệt kê.
83. **Lễ hội làng Bún (Phú Đô / Vân Cù)** — Nguồn Khám Phá Huế dùng tên “làng bún Phú Đô” nhưng địa điểm/di sản là Vân Cù; cần chuẩn hóa entity trước khi ingest.
84. **Lễ hội truyền thống ngành Ca nhạc Huế** — CSDL lễ hội Huế liệt kê.
85. **Lễ giỗ Tổ ngành Tuồng** — Một số nguồn dùng “Lễ tế giỗ tổ ngành Tuồng”.
86. **Lễ tế Tổ nghề Rèn Hiền Lương** — Có bài riêng trên Khám Phá Huế.
87. **Lễ giỗ Tổ nghề Mộc** — CSDL lễ hội Huế nêu như ví dụ lễ hội ngành nghề.
88. **Lễ giỗ Tổ nghề Nề ngõa** — CSDL lễ hội Huế nêu như ví dụ lễ hội ngành nghề.

### E. Lễ hội các dân tộc thiểu số miền núi Huế
89. **Lễ cúng lúa mới** — Bản ghi cổng lễ hội quốc gia; tên khái quát.
90. **Lễ cúng rẫy** — Bản ghi cổng lễ hội quốc gia.
91. **Lễ hội A Riêu Piing** — Cổng quốc gia ghi “A Riêu PIING”; lễ hội của cộng đồng Tà Ôi/Pa Cô.
92. **Lễ hội A Riêu Aza** — Cổng quốc gia ghi “A Riêu AZA”; cần giữ alias khi chuẩn hóa.
93. **Lễ hội Ada Koonh (Mừng lúa mới) của người Pa Cô** — Di sản văn hóa phi vật thể quốc gia; còn gặp dạng A Da Koonh/A Da Pựưt.
94. **Lễ hội A Riêu Car** — Đại lễ quan trọng của người Pa Cô; chu kỳ tổ chức dài.
95. **Lễ hội Mừng lúa mới của người Cơ Tu (Cha ha ro tơ me / Bhuôih Haro Tơme)** — Được công nhận di sản văn hóa phi vật thể quốc gia năm 2025.
96. **Lễ hội Tế/Cúng Thần Nước của người Pa Cô** — Được bảo tồn, phục dựng tại A Lưới; kế hoạch Huế 2026 tiếp tục tổ chức.

### F. Lễ hội/sự kiện có nguồn gốc hoặc yếu tố nước ngoài được ghi nhận tại Huế
97. **Lễ đón mừng năm mới Bunpimay tại Huế** — Tết cổ truyền Lào được tổ chức cho cộng đồng/sinh viên Lào tại Huế.
98. **Lễ Tình nhân (Valentine)** — CSDL Huế nêu trong nhóm lễ hội du nhập từ nước ngoài; không nên tạo entity du lịch Huế riêng nếu corpus tập trung đặc trưng địa phương.
99. **Lễ Cá tháng Tư** — CSDL Huế nêu trong nhóm lễ hội du nhập từ nước ngoài; không đặc trưng Huế.
100. **Lễ Halloween** — CSDL Huế nêu trong nhóm lễ hội du nhập từ nước ngoài; không đặc trưng Huế.

## 3. Các loại hình/tên gọi chung được nguồn chính thức mô tả, nhưng chưa nên coi là một entity duy nhất
1. Lễ hội Cầu ngư (loại hình chung)
2. Lễ hội Nghinh Ông
3. Lễ Kỳ yên / Cầu an
4. Lễ hội thờ Mẫu / Thánh Mẫu / Nữ thần
5. Lễ hội thờ Cô hồn / Cô bác
6. Lễ hội cầu mưa
7. Lễ hội cầu mùa
8. Lễ cúng rừng
9. Lễ cúng Thần làng
10. Lễ hội kết nghĩa anh em
11. Lễ hội đâm trâu (dạng thức lịch sử trong tư liệu vùng cao; cần xử lý thận trọng theo thực hành hiện nay)
12. Lễ lấp lỗ

**Lý do tách riêng:** ví dụ “Lễ hội Cầu ngư” tồn tại ở nhiều làng/địa bàn khác nhau. Nếu tạo một file `le-hoi-cau-ngu.md` duy nhất sẽ làm mất thông tin địa phương và dễ gây retrieval sai. Nên ưu tiên các entity cụ thể như `cau-ngu-thai-duong-ha`, `cau-ngu-quang-an`, `cau-ngu-lang-co`, v.v.

## 4. Nhãn mùa của Festival Huế — không mặc định là lễ hội độc lập
1. Lễ hội mùa Xuân – Festival Huế
2. Lễ hội mùa Hạ – Festival Huế
3. Lễ hội mùa Thu – Festival Huế
4. Lễ hội mùa Đông – Festival Huế

Các tên trên là **season/program labels** trong mô hình Festival Huế bốn mùa. Trong RAG nên cân nhắc lưu trong `festival-hue.md` hoặc metadata/section của Festival Huế thay vì tạo bốn entity hoàn toàn độc lập, trừ khi corpus có đủ nội dung riêng cho từng mùa.

## 5. Các điểm cần chuẩn hóa trước khi biến inventory thành file entity
- **Điện Huệ Nam / Điện Hòn Chén:** dùng `Lễ hội Điện Huệ Nam` làm canonical name; giữ `Điện Hòn Chén` làm alias.
- **Lễ hội làng Bún:** nguồn Khám Phá Huế dùng tên `Lễ hội làng bún Phú Đô` nhưng mô tả địa điểm tại **làng Vân Cù**; hồ sơ hiện hành về nghề bún cũng gắn với Vân Cù. Không nên đưa `Phú Đô` vào filename trước khi đối chiếu hồ sơ gốc.
- **Cầu ngư:** không gom Thai Dương Hạ, Thuận An/Thai Dương Thượng, Quảng An, Lăng Cô và các làng biển khác thành một festival entity duy nhất.
- **Hội An Truyền / Lễ Thu tế làng An Truyền:** có khả năng là hai cách ghi cho cùng hoặc các lớp nghi lễ liên quan; cần research riêng trước khi tạo hai file.
- **Sóng nước Tam Giang / Sông nước Tam Giang:** giữ alias; cần chọn canonical name theo kỳ tổ chức được research.
- **Áo dài:** `Lễ hội Áo dài Huế`, `Tuần lễ Áo dài cộng đồng Huế`, `Tuần lễ Áo dài Huế` có quan hệ gần nhưng không nhất thiết là cùng một program qua mọi năm.
- **Mừng lúa mới miền núi:** Pa Cô (`Ada Koonh`) và Cơ Tu (`Cha ha ro tơ me/Bhuôih Haro Tơme`) là hai truyền thống khác nhau, không được merge chỉ vì cùng dịch là “Mừng lúa mới”.
- **A Riêu Aza / Ada Koonh / A Riêu Car / A Riêu Piing:** không merge theo similarity tên. Đây là các nghi lễ/lễ hội có chức năng và chu kỳ khác nhau; cần giữ alias và ethnic group trong metadata.
- **Bài Chòi:** có thể là lễ hội/sân chơi mùa xuân, đồng thời cũng xuất hiện như một hoạt động trong các lễ hội khác. Metadata nên phân biệt `standalone_event` và `festival_activity`.

## 6. Nguồn do người dùng cung cấp — đã được đọc/đối chiếu trong research này
1. https://khamphahue.com.vn/Van-hoa/Le-hoi
2. https://vinwonders.com/vi/wonderpedia/news/le-hoi-hue/
3. https://cellphones.com.vn/sforum/le-hoi-hue
4. https://lehoi.hue.gov.vn/Le-hoi/Le-hoi-tieu-bieu
5. https://vinpearl.com/vi/le-hoi-hue-kham-pha-nhung-su-kien-van-hoa-doc-dao-dat-co-do
6. https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/le-hoi-hue.html
7. https://sovaba.travel/blog/bai-viet-hue-va-nhung-le-hoi-truyen-thong-hoi-tho-van-hoa-suot-4-mua
8. https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/festival-hue.html
9. https://hue.aeonmall-vietnam.com/cam-nang-aeon-mall-hue/le-hoi-ao-dai-hue.html
10. https://dulichdaibang.com/kinh-nghiem-du-lich/diem-danh-cac-le-hoi-truyen-thong-noi-bat-o-hue.html

## 7. Nguồn bổ sung ưu tiên cao
- **Sở Văn hóa và Thể thao TP Huế – thống kê khoảng 520 lễ hội:** https://svhtt.hue.gov.vn/p/chuyen-trang-phong-trao/tin-chuyen-trang-phong-trao/thuc-hien-chinh-quyen-dia-phuong-2-cap.html
- **CSDL Lễ hội TP Huế – các loại hình và danh sách lễ hội chính:** https://lehoi.hue.gov.vn/Le-hoi/Gioi-thieu-le-hoi-Thanh-pho-Hue/tid/Cac-loai-hinh-le-hoi-o-Thua-Thien-Hue.html/pid/26/cid/5/
- **CSDL Lễ hội TP Huế – lễ hội các vùng miền:** https://lehoi.hue.gov.vn/Le-hoi/Gioi-thieu-le-hoi-Thanh-pho-Hue/tid/Ve-le-hoi-cac-vung-mien-o-Thua-Thien-Hue.html/pid/25/cid/5/
- **Cổng thông tin điện tử Lễ hội – Cục Văn hóa Cơ sở, Gia đình và Thư viện:** https://lehoi.com.vn/lehoi/danhsach.aspx
- **Cục Di sản Văn hóa – Ada Koonh:** https://dsvh.gov.vn/le-hoi-ada-koonh-mung-lua-moi-cua-nguoi-pa-co-3212
- **Sở VHTT Huế – A Riêu Car:** https://svhtt.hue.gov.vn/tin-trong-tinh/soi-dong-le-hoi-a-rieu-car-vung-cao-a-luoi.html
- **Bộ VHTTDL – Mừng lúa mới của người Cơ Tu:** https://bvhttdl.gov.vn/huong-di-moi-cho-le-hoi-mung-lua-moi-cua-dong-bao-co-tu-20251113112454079.htm
- **Cổng TTĐT TP Huế – Lễ hội Quán Thế Âm 2026:** https://hue.gov.vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/4309a7bd-ae8c-f111-9a81-1866dae8d0c9
- **Cổng TTĐT TP Huế – Thuận An biển gọi 2026:** https://hue.gov.vn/Trang-chu/Cac-hoat-%C4%91ong-su-kien-noi-bat-cua-%C4%91ia-phuong-trong-thanh-pho/Chi-tiet/mlid/68e0cd6b-2327-f111-9a80-1866dae8d0c9
- **Khám Phá Huế – nhóm lễ hội truyền thống:** https://khamphahue.com.vn/Van-hoa/Chi-tiet/tid/Le-hoi-truyen-thong/cid/198/pid/0
- **Khám Phá Huế – nhóm lễ hội văn hóa:** https://khamphahue.com.vn/Van-hoa/Chi-tiet/tid/Le-hoi-van-hoa/cid/68/pid/0

## 8. Khuyến nghị dùng inventory này cho `knowledge-base-hue/festivals/`
1. **Không tạo ngay 1 file cho cả 520 lễ hội.** Trước hết chọn các lễ hội có giá trị trả lời du lịch cao, có nguồn đủ mạnh và có đủ thông tin để tạo một entity file chất lượng.
2. Với mỗi tên trong danh sách, research riêng để xác định: `canonical_name`, `aliases`, `festival_type`, `recurrence`, `calendar_basis`, `location`, `organizer`, `parent_program`, `tourist_relevance`, `sources`.
3. Ưu tiên nguồn theo thứ tự: **Sở VHTT/UBND TP Huế/CSDL lễ hội Huế → Trung tâm Bảo tồn Di tích/Sở Du lịch → Bộ VHTTDL/Cục Di sản/Cục Du lịch → nguồn báo chí uy tín → website du lịch thương mại**.
4. Chỉ tạo file riêng cho một program con của Festival Huế khi nó có identity ổn định qua nhiều kỳ hoặc có đủ nội dung answer-facing; nếu không, giữ nó trong `festival-hue.md` hoặc guide theo năm/mùa.
5. Nếu mục tiêu là đạt **520/520**, bước tiếp theo đúng nhất không phải tiếp tục Google thủ công mà là xin/thu hồi **export dữ liệu từ CSDL quản lý của Sở VHTT TP Huế** (CSV/Excel/API/database export), sau đó deduplicate và chuẩn hóa tên.

## 9. Ghi chú provenance
- Inventory này ưu tiên **recall**: giữ lại các tên có căn cứ để không bỏ sót candidate quan trọng.
- Một tên xuất hiện trong inventory **không đồng nghĩa** nó chắc chắn nên trở thành một file `.md` độc lập trong corpus cuối.
- Những sự kiện một lần hoặc tên chương trình thay đổi theo năm phải được đánh dấu `year_specific` khi research chi tiết.
- Không dùng số thứ tự/tổng số trong file này như bằng chứng rằng Huế chỉ có từng đó lễ hội; con số quản lý hiện công bố là **khoảng 520**.
