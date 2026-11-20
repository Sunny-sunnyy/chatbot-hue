# Mâu thuẫn trong curated corpus (phát hiện khi làm Phase 7A, 2026-10-23)

Private. Đường dẫn tính trong `knowledge-base-hue/`, kèm số dòng. K1–K9 do
Implementer phát hiện khi đọc `heritages`; K10 do Reviewer phát hiện. Reviewer
đã định vị lại từng chỗ bằng tìm text. Chưa sửa gì; chưa kiểm với nguồn bên
ngoài để biết bên nào đúng.

| # | Chủ đề | Bên A (file:dòng → nội dung) | Bên B (file:dòng → nội dung) |
|---|---|---|---|
| K1 | Mã thành phần UNESCO | `heritages/heritage/Quần thể Di tích Cố đô Huế.md:38–51`: danh sách 14 cụm, gồm Đàn Nam Giao **678-005**, Lăng Tự Đức **678-009**, Lăng Đồng Khánh **678-011**, Lăng Khải Định **678-012**; không có Điện Hòn Chén | `Đàn Nam Giao.md:11,20,149` → **678-006** (mã của Lăng Gia Long trong danh sách); `Lăng Đồng Khánh.md:12` → **678-008** (mã của Thiệu Trị); `Lăng Khải Định.md:12` → **678-011** (mã của Đồng Khánh); `Điện Hòn Chén.md:11,101` → **678-009** (mã của Tự Đức), "cụm thành phần thứ 9" |
| K2 | "Lăng duy nhất quay hướng Tây Bắc" | `heritages/heritage/Lăng Thiệu Trị.md:33`: lăng hoàng đế **duy nhất** quay hướng Tây Bắc | `heritages/heritage/Lăng Dục Đức.md:41`: lăng quay mặt về hướng **Tây Bắc** |
| K3 | Lăng Tự Đức và di sản tư liệu MOWCAP 2016 | `heritages/heritage/Thơ văn trên kiến trúc cung đình Huế.md:42`: Lăng Tự Đức **không thuộc** danh mục | `heritages/heritage/Lăng Tự Đức.md:83`: thơ văn ở điện Hòa Khiêm, Lương Khiêm… là **bộ phận trọng yếu** được MOWCAP vinh danh 2016 |
| K4 | Năm Nguyễn Tất Thành vào Quốc Học | `heritages/heritage/Trường Quốc Học Huế.md:104–105`: **tháng 9/1907**, học niên khóa 1907–1908 và 1908–1909 | `heritages/heritage/Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md:46,86`: học Tiểu học Đông Ba **1906–1908**, rồi mới thi vào Quốc Học |
| K5 | Năm ghi danh "Tri thức dân gian về Bún bò Huế" | `heritages/heritage-guides.md:33`: **năm 2024** | `heritages/heritage/Tri thức dân gian về Bún bò Huế.md:11`: Quyết định 2203/QĐ-BVHTTDL ngày **27/06/2025** |
| K6 | Số tấm Mộc bản | `heritages/heritage-guides.md:24`: **34.618** tấm | `heritages/heritage/Mộc bản triều Nguyễn.md:12`: UNESCO xác nhận **34.555**; con số dao động **33.971–34.618** tùy cách phân loại |
| K7 | Năm lập Trường Hành Nhơn | `heritages/heritage/Trường Quốc Học Huế.md:10,34`: "năm **Tự Đức thứ 2 – 1868**" | Trong chính file này: năm 1868 không khớp niên hiệu Tự Đức thứ 2 (vua lên ngôi năm 1848) |
| K8 | Hậu chẩm Kinh thành; tên cồn | `heritages/heritage/Kinh thành Huế.md:44`: hậu chẩm là **núi Đột Sơn (Chân Sơn)**; dòng 42 viết "**Dã Viên**" | `heritages/heritage/Quần thể Di tích Cố đô Huế.md:63`: hậu chẩm là **dãy Trường Sơn**; viết "**Giã Viên**" |
| K9 | Năm đúc Cửu Đỉnh | `heritages/heritage/Hải Vân Quan.md:18,114`: đúc **năm 1836** | `heritages/heritage/Cửu Đỉnh Huế.md:17` và `Đại Nội Huế.md:119`: đúc từ **1835** đến **1837** |
| K10 | Nhà hát "cổ nhất" | `heritages/heritage/Đại Nội Huế.md:171`: Duyệt Thị Đường (1826) là nhà hát hoàng gia **cổ nhất còn lại** | `heritages/heritage/Lăng Tự Đức.md:54`: Minh Khiêm Đường (1864–1865) là nhà hát cung đình **cổ nhất còn tồn tại** |

Ghi chú:

- K6 một phần đã được chính file Mộc bản giải thích là có dao động; mâu thuẫn
  thật là `heritage-guides.md` nêu 34.618 như một con số chắc chắn.
- K10 có thể chỉ do cách diễn đạt (Minh Khiêm Đường nằm ngoài Đại Nội), nhưng
  hai câu cùng lúc đều nói "cổ nhất" nên người đọc sẽ bối rối.
- Chỉ mới rà `heritages`. Bốn domain còn lại có thể còn mâu thuẫn; Task 3 sẽ ghi
  thêm nếu gặp.

## Bổ sung Task 3 (K11 trở đi)

Do các sub-agent Task 3 báo lại khi đọc partition; Implementer đã định vị lại
từng dòng bằng tìm text. Golden không dùng dữ kiện nào dưới đây. Chưa sửa gì.
Đường dẫn tính trong `knowledge-base-hue/`.

### foods

| # | Chủ đề | Bên A | Bên B |
|---|---|---|---|
| K11 | Phường của AEON MALL Huế (8 Võ Nguyên Giáp) | "An Cựu": `foods/cafes/phuc long hue.md:9`, `foods/restaurants/jollibee hue.md:10`, `foods/restaurants/kfc hue.md:10`, `foods/restaurants/banh cuon thit heo donald trung.md:11`, `foods/cafes/anh kafe hue.md:12` | "An Đông": `foods/cafes/cat cafe mocha hue.md:9`, `foods/cafes/highlands coffee hue.md:12`, `foods/cafes/koi the hue.md:10`, `foods/restaurants/lotteria hue.md:12`, `foods/restaurants/texas chicken hue.md:9` |
| K12 | "Bánh lá" có phải bánh nậm | `foods/local_specialties/banh nam.md:5`: bánh nậm "còn gọi là bánh lá" | `foods/restaurants/nha hang banh ba do.md:21–23`: bánh nậm "gần với" bánh lá; "bánh lá chả tôm" là món riêng |
| K13 | Bánh ép kiểu Cầu Hai giòn hay dẻo | `travel/places/Đầm Cầu Hai.md:160–162`: vỏ giòn, khác bánh ép dẻo nội đô | `foods/restaurants/banh ep 1992.md:17`, `foods/local_specialties/banh ep.md:87`: "phong cách Cầu Hai, ép dẻo" |
| K14 | Giá trị kép trong cùng một file | Giờ Cơm Âm Phủ gốc `com am phu nguyen thai hoc.md:11` với `:12` (và `food-guides.md:33`); giờ chiều Hủ tiếu Nam Vang `hu tieu nam vang tran phu.md:11` với `:12`; giờ Quán Bà Cư `quan ba cu.md:11` với `:21` | Giá và số nhà Bánh ép Huệ `banh ep hue.md:9–10` với `:16,20`; giá Thúy `thuy banh canh nam pho.md:10` với `:11`; địa chỉ điểm bán `me xung thien huong.md:11` |
| K15 | Giờ CỦI Coffee | `foods/food-guides.md:68`: 6:30–22:00 | `foods/cafes/cui coffee.md:12`: cuối tuần 06:00–22:30 |

### travel_tickets

Tên file viết tắt: **QT** = `travel/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md`;
**HD** = `travel/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md`;
**VBD** = `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`;
**VK** = `travel/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md`.

| # | Chủ đề | Bên A | Bên B |
|---|---|---|---|
| K16 | Ngày miễn vé dịp Tết | QT:114: chỉ mùng 1 Tết | HD:135: mùng 1 đến mùng 3 Tết |
| K17 | Ngoại lệ hoàn vé | QT:162: hoàn khi bất khả kháng (thiên tai, di tích tạm dừng) | HD:179–181: trường hợp **duy nhất** được hoàn là lỗi giao dịch |
| K18 | Đối tượng học sinh, sinh viên được ưu đãi | QT:122,133–134: học sinh, sinh viên đi ngoại khóa, hoặc sinh viên tại Huế | HD:140: học sinh, sinh viên thuộc hệ thống giáo dục quốc dân |
| K19 | Thời hạn vé combo | QT:96–101,158: vé gộp 2–3 điểm dùng trong ngày; QT:90: toàn tuyến tối đa 05 ngày | `heritages/heritage-guides.md:121`: combo 3–4 điểm dùng trong 02 ngày; toàn tuyến 03–05 ngày |
| K20 | Mức tiết kiệm vé toàn tuyến | QT:88,103,183: tổng mua lẻ 1.050.000, tiết kiệm 450.000 (chưa đối chiếu được với tổng các dòng giá lẻ ở QT:26–37) | `heritages/heritage-guides.md:116`: tiết kiệm hơn 400.000 |
| K21 | Giá vé Ca Huế trên sông Hương | VBD:113,229: khách lẻ 100.000–130.000; VBD:128: thuyền đôi 1.600.000–2.500.000; VBD:115–116: mốc tuổi/chiều cao trẻ em | `performing_arts/performing_arts_guides.md:170`: 80.000–100.000; `:175`: thuyền đôi 1.600.000–2.000.000; `:171–172`: mốc khác |
| K22 | Xe trung chuyển Bạch Mã | VK:39–40: giá theo nhóm 1–5 và 6–12 khách, khứ hồi 1.000.000/1.200.000 | `travel/places/Vườn quốc gia Bạch Mã.md:164`: khứ hồi khoảng 900.000/chuyến cho cả đoàn |

VBD:21 lặp lại K10 (Duyệt Thị Đường "cổ nhất Việt Nam còn tồn tại").

### travel_services

| # | Chủ đề | Bên A | Bên B |
|---|---|---|---|
| K23 | Thời điểm sạt lở Km12 đường lên Bạch Mã | `travel/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md:162–163`: ghi nhận trong tháng 06/2026 | `travel/places/Vườn quốc gia Bạch Mã.md:147`: mùa mưa lũ 2025 – đầu 2026; VK:58: sau mưa lũ cuối năm 2025 |
| K24 | Địa danh suối khoáng | `travel/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md:123`: suối khoáng tại Phong Thái | VK:101,295: Alba Thanh Tân ở xã Phong Sơn |

### performing_arts

**PG** = `performing_arts/performing_arts_guides.md`; **CH** = `performing_arts/arts/Ca Huế trên sông Hương.md`.

| # | Chủ đề | Bên A | Bên B |
|---|---|---|---|
| K25 | Thuyền Ca Huế có chạy khi diễn | CH:29: thuyền di chuyển chậm trên sông khi nghe | CH:77, PG:61: cấm vừa chạy vừa diễn, phải neo |
| K26 | Suất 3 Ca Huế | PG:56–59: suất 21h00 hằng đêm | VBD:101: suất 3 chỉ tăng cường cuối tuần/cao điểm |
| K27 | Văn bản quy định và số nhạc cụ | CH:76: Quyết định 21/2024/QĐ-UBND; CH:40: 3–5 nhạc cụ | VBD:244: Quyết định 104/2025/QĐ-UBND; PG:65: 3–4 nhạc cụ; VBD:87: tối thiểu 4/5 loại |
| K28 | Đến sớm trước giờ diễn Duyệt Thị Đường | PG:191: 15–20 phút | `performing_arts/arts/Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md:83`: 10–15 phút |
| K29 | Ngày các đêm Dạ yến thính phòng 2026 tại Duyệt Thị Đường | `performing_arts/arts/Đêm Hoàng cung – Dạ yến Hoàng cung.md:33`: dịp 30/4 – 1/5/2026 | Cùng file `:128`: ngày 29/4 và 01/5/2026 |
| K30 | Thời điểm Tuần lễ Âm nhạc Quốc tế Huế | `performing_arts/arts/Huế Wonderverse Music Fest.md:90`: sự kiện mùa Hạ | `performing_arts/arts/Tuần lễ Âm nhạc Quốc tế Huế.md:9,21,59`: lần đầu tháng 12/2023, mùa Đông |
| K31 | Đội hình đêm Trịnh 14/6/2026 | `performing_arts/arts/Đêm nhạc Trịnh Công Sơn tại Huế.md:123` | `performing_arts/arts/Tuần lễ Âm nhạc Quốc tế Huế.md:75,79` |
| K32 | Ngày Tuần lễ Festival 2024 | `performing_arts/arts/Tuần lễ Festival Nghệ thuật Quốc tế Huế.md:108`: 07/6–12/6/2024 | Cùng file `:114`: 6/6–12/6/2024 |
| K33 | Điện hay Cung Khôn Thái | PG:136,181: "Điện Khôn Thái" | `performing_arts/arts/Đêm Hoàng cung – Dạ yến Hoàng cung.md:10,33`: "Cung Khôn Thái" |

### festivals

| # | Chủ đề | Bên A | Bên B |
|---|---|---|---|
| K34 | Mùa tái hiện lễ Ban Sóc | `festivals/festival-guides.md:46`: cuối năm âm lịch, mùa đông | `festivals/festival/Lễ Ban Sóc triều Nguyễn.md:10,69,127–128,198`, `festivals/festival/Festival Huế.md:54`: ngày 1/1 Dương lịch, mở màn Festival mùa Xuân |
| K35 | Vua có trực tiếp chủ tế lễ Xã Tắc | `festivals/festival/Lễ tế Xã Tắc.md:9`: từ Thành Thái trở đi vua không trực tiếp chủ tế | `heritages/heritage/Đàn Xã Tắc.md:33`: cả 13 vị hoàng đế đều từng thân hành chủ lễ |
| K36 | Giờ canh tư khi tế Nam Giao | `festivals/festival/Lễ tế Nam Giao.md:84`: khoảng 2–4 giờ sáng | `heritages/heritage/Đàn Nam Giao.md:134`: khoảng 2–3 giờ sáng |
| K37 | Phường của Điện Hòn Chén | `festivals/festival/Lễ hội Điện Huệ Nam.md:12`, `heritages/heritage/Điện Hòn Chén.md:8`: Kim Long | QT:34: Long Hồ |
| K38 | Lệch nhỏ | `festivals/festival/Lễ hội Cầu ngư.md:78` (cung nghinh ngày 10) với `:96` (chiều ngày 11); `festivals/festival/Lễ hội Hương xưa làng cổ – Phước Tích.md:22` ("gần 30" nhà rường) với `:53` (26) | `festivals/festival/Lễ Thu tế làng An Truyền.md:81` (9–10 km) với `travel/places/Đầm Chuồn.md:15` (10–12 km); `festivals/festival/Lễ tế Xã Tắc.md:45` (thám sát 2007) với `heritages/heritage/Đàn Xã Tắc.md:22` (2006–2007) |

### travel_places

Thư mục gốc các file dưới đây là `travel/places/` trừ khi ghi khác.

| # | Chủ đề | Bên A | Bên B |
|---|---|---|---|
| K39 | Ngày Nghị quyết 1675/NQ-UBTVQH15 | `Bãi biển Phú Diên.md:7`: ngày 19/12/2024 | `Chợ Tây Lộc.md:25`, `Làng du lịch cộng đồng Thác A Nôr.md:8`, `Suối Voi.md:21`, `Phá Tam Giang.md:8`: ngày 16/06/2025 |
| K40 | Năm Nguyễn Tất Thành học Tiểu học Đông Ba (gần K4) | `Chợ Đông Ba.md:37`: 1906–1909 | `heritages/heritage/Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md:46,86`: 1906–1908 |
| K41 | Quyết định Bảo vật quốc gia chóp tháp Champa Linh Thái | `Đầm Cầu Hai.md:36`: QĐ 88/QĐ-TTg ngày 15/01/2020 | `Bãi biển Hàm Rồng.md:47`: QĐ 2283/QĐ-TTg ngày 31/12/2020 |
| K42 | Địa giới cũ của Suối Mơ | `Suối Voi.md:80`: trước đây thuộc xã Lộc Thủy, gần đèo Phước Tượng | `Suối Mơ.md:8,21,100`: trước 01/07/2025 thuộc thị trấn Lăng Cô, đi từ chân đèo Phú Gia |
| K43 | Hướng và cự ly Bình An – Cảnh Dương | `Bãi biển Bình An.md:27,61,69`: Cảnh Dương ở phía đông nam Bình An; Bình An cách Huế 60–65 km | `Bãi biển Cảnh Dương.md:9,180`: Bình An ở phía đông nam vịnh Chân Mây; Cảnh Dương cách Huế 50–55 km |
| K44 | Diện tích đầm Cầu Hai | `Bãi biển Hàm Rồng.md:61`: khoảng 112 km² | `Hệ đầm phá Tam Giang – Cầu Hai.md:39`: khoảng 104 km² (`Đầm Cầu Hai.md:10` tự ghi 104–112 km²) |
| K45 | Đầm Chuồn có thuộc đầm Sam | `Đầm Chuồn.md:6,9,15,201`: là bộ phận của đầm Sam | `Hệ đầm phá Tam Giang – Cầu Hai.md:31`: đầm An Truyền (Chuồn) và đầm Thanh Lam (Sam) là hai đầm riêng |
| K46 | Thời gian ủ mắm sò | `Vịnh Lăng Cô.md:159`: 8–20 ngày | `Đầm Lập An.md:132`: 10–20 ngày |
| K47 | Đường đến Cồn Tộc | `Hệ đầm phá Tam Giang – Cầu Hai.md:243`: 22–25 km, 40–45 phút | `Phá Tam Giang.md:199`: 25–28 km, 40–50 phút |
| K48 | Xe máy qua khu vực Hải Vân | `Đầm Lập An.md:171`: xe máy bắt buộc đi đường đèo | `Đèo Hải Vân.md:130`, `Vịnh Lăng Cô.md:202`: có dịch vụ xe trung chuyển xe máy qua hầm |
| K49 | Mùa leo núi Kim Phụng | `Núi Kim Phụng.md:139`: mùa thích hợp từ tháng 11 đến tháng 4 | Cùng file `:141`: mùa mưa bão từ tháng 9 đến tháng 11 |
| K50 | Chiều dài đèo Hải Vân (nhẹ) | `Vịnh Lăng Cô.md:203`: khoảng 20 km | `Đèo Hải Vân.md:11`: khoảng 21 km |

### Bổ sung GATE R (Reviewer phát hiện, Implementer đã định vị lại)

| # | Chủ đề | Bên A | Bên B |
|---|---|---|---|
| K51 | Chu kỳ Lễ hội Cầu ngư Thai Dương Hạ | `festivals/festival/Lễ hội Cầu ngư.md:10,75–76`: đại lễ 3 năm một lần (tam niên đáo lệ); năm khác chỉ có lễ cúng thường niên | `travel/places/Hệ đầm phá Tam Giang – Cầu Hai.md:194`: lễ hội diễn ra ngày 11 và 12 tháng Giêng hằng năm |
| K52 | Độ cao đỉnh đèo Hải Vân | `travel/places/Đèo Hải Vân.md:12,19,74`: 496 m | `heritages/heritage/Hải Vân Quan.md:8,16` và `travel/tickets/Vé tham quan Hải Vân Quan.md:19`: khoảng 490 m |
| K53 | Cự ly Huế – khu Lăng Cô/Hải Vân | `travel/places/Vịnh Lăng Cô.md:9`: Lăng Cô cách trung tâm Huế khoảng 60 km | `heritages/heritage/Hải Vân Quan.md:137`: từ trung tâm Huế đi Quốc lộ 1 khoảng 70 km (tới Hải Vân Quan, qua Lăng Cô). Kết luận so sánh của case `travel_services` không đổi |

Ghi chú thêm cho K45: `travel/places/Hệ đầm phá Tam Giang – Cầu Hai.md:224`
còn ghi Đầm Chuồn (đầm An Truyền) là "một bộ phận thuộc Đầm Thủy Tú", khác cả
hai cách ghi ở K45.
