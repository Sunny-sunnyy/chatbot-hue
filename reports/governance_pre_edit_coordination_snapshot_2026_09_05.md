# Bản lưu điều phối trước chỉnh governance — 2026-09-05

Archive state: inactive
Captured by: Reviewer

Bảo toàn nguyên văn hai tài liệu điều phối có thay đổi chưa commit, sau khi user
đã yêu cầu session khác tạm dừng cập nhật. Đây là claim và chỉ dẫn cũ, không phải
kết quả Reviewer đã xác minh hoặc user approved. Metadata `State: active`, quyền
và next action trong trích dẫn không còn hiệu lực. Chỉ
`session_prompt/CURRENT_HANDOFF.md` là handoff hiện hành.

Không cần đọc bản lưu khi bootstrap; chỉ mở khi cần khôi phục chi tiết tiến độ
chưa có trong inventory/report. Roadmap mới trong Project Status ưu tiên hơn
thứ tự công việc được mô tả trong bản lưu này.

## Handoff trước chỉnh sửa (nguyên văn)

````markdown
# Bàn giao hiện hành

Target role: implementer
Authored by: implementer
Handoff kind: post_review_correction_complete
State: active
Base commit: 45eb7e0
Head commit: worktree
Risk level: low
Git authorization: none
Sub-agent authorization: none

---

## 1. Objective

Hoàn tất kiểm chứng độc lập, giải quyết toàn bộ các phát hiện (blocker, major, minor) trong báo cáo re-review của Codex đối với Batch 01 (9 thực thể di sản đầu tiên); đồng bộ địa giới hành chính cho Thực thể 10 (Lăng Gia Long) và Thực thể 11 (Lăng Minh Mạng); cập nhật minh chứng đối chiếu và lập báo cáo phản hồi toàn diện tại mốc ngày 04/09/2026.

## 2. Kết quả hoàn thành

1. **Hiệu chỉnh toàn diện Batch 01 (1 đến 9):**
   - `1 Quần thể Di tích Cố đô Huế.md`: Phân định rõ 14 di tích thành phần UNESCO chính thức (serial 678-001 đến 678-014); Cung An Định, Đàn Xã Tắc, Điện Hòn Chén là di tích liên quan do HMCC quản lý; cập nhật địa giới hành chính theo NQ 1675 (Lăng Dục Đức thuộc phường An Cựu; Cung An Định thuộc phường Thuận Hóa; Chùa Thiên Mụ thuộc phường Kim Long); sửa mốc Điện Thái Hòa 2021–2024 (nghiệm thu 11/2024); xóa dòng meta-editorial thừa dòng 85.
   - `2 Nhã nhạc cung đình Huế.md`: Chuẩn hóa dòng lịch sử (thế kỷ XV thời Lê sơ đến đỉnh cao triều Nguyễn); bỏ chuỗi cơ quan lai tạp; bỏ đàn tam thập lục khỏi Tiểu nhạc; chuẩn hóa Nhạc chương; gán triết lý Âm Dương - Ngũ Hành cho các nhà nghiên cứu âm nhạc dân tộc thay vì gán cho UNESCO.
   - `3 Mộc bản triều Nguyễn.md`: Đính chính địa chỉ Trung tâm Lưu trữ Quốc gia IV tại số 02 Yết Kiêu, phường Cam Ly, thành phố Đà Lạt (theo NQ 1671/NQ-UBTVQH15); đồng nhất 152 đầu sách, 9 nhóm chủ đề; mốc 1984 là quy tập kho Đà Lạt, năm 2006 mới thành lập TTLTQG IV; Tàng Thơ Lâu mở cửa đón khách tháng 3/2021; trung tính hóa nhận định văn bản học.
   - `4 Châu bản triều Nguyễn.md`: Xóa bỏ tên gọi "Hồng bản"; viết lại lịch sử lưu chuyển chính xác 100% theo TTLTQG I (Nội các -> 1942 -> 1959 -> 1961 -> 03/1975 -> 1978 -> 1991); Tàng Thơ Lâu đón khách tháng 3/2021; mô tả kho bảo quản chuyên dụng trung tính.
   - `5 Thơ văn trên kiến trúc cung đình Huế.md`: Bỏ Tự Đức khỏi thời kỳ phát triển rực rỡ nhất; bổ sung đầy đủ 12 địa điểm di tích theo hồ sơ MOWCAP 2016 (có Khiêm Lăng và Chùa Thiên Mụ); bỏ số đếm con ước lượng theo chất liệu; Điện Thái Hòa nghiệm thu 11/2024; mô tả đúng mức tiến độ số hóa.
   - `6 Cửu Đỉnh Huế.md`: Sửa blocker cấp ghi danh: Di sản tư liệu khu vực Châu Á – Thái Bình Dương (MOWCAP 2024) cho 162 bản đúc nổi trên Cửu Đỉnh; 9 đỉnh đồng là Bảo vật quốc gia (QĐ 1426/QĐ-TTg năm 2012); sửa blocker vị trí chữ: bên phải cổ đỉnh đúc niên đại đúc, bên trái đúc trọng lượng đỉnh; dùng thuật ngữ "đúc nổi", bỏ "chạm cẩn/chạm"; làm rõ 7 đỉnh đầu gắn với án thờ 7 vua trong Thế Miếu, Dụ & Huyền đỉnh không gắn chính thức; khắc phục trùng lặp Hải Vân; phân biệt patin tự nhiên với ăn mòn điện hóa/vết đạn chiến tranh; bỏ khẳng định lắp rào chắn cố định.
   - `7 Thực hành tín ngưỡng thờ Mẫu Tam phủ của người Việt.md`: Sửa danh sách 21 tỉnh hồ sơ UNESCO 2016 (có Hòa Bình và Lào Cai, không có Hà Giang); cập nhật Điện Hòn Chén thuộc phường Kim Long; sửa niên đại vua Minh Mạng 1820–1841 và rút gọn mỹ tự; đính chính mốc Thiên Tiên Thánh Giáo thành lập năm 1953 tại Phước Linh điện, xây dựng cơ sở Chi Lăng năm 1965.
   - `8 Nghệ thuật Bài Chòi Trung Bộ.md`: Cấu trúc chuẩn 30 cặp quân bài (27 cặp thuộc ba pho Văn, Vạn, Sách + 3 cặp bài yêu), bỏ danh sách con từng quân bài để tránh mâu thuẫn dị bản; tách biệt rành mạch biến thể hội Bài Chòi xứ Huế: 11 chòi (1 chòi cái ở trung tâm và 10 chòi quân), mỗi chòi nhận 5 quân bài, ván chơi sử dụng 56 quân bài theo khảo cứu của Trần Đức Anh Sơn; biên chế nhạc cụ phụ họa linh hoạt theo địa phương; neo phương thức bảo tồn và phát huy giá trị (safeguarding).
   - `9 Tri thức dân gian về Bún bò Huế.md`: Sửa blocker nhãn hiệu: Giấy chứng nhận số 272400 cấp ngày 25/11/2016 có thời hạn hiệu lực 10 năm kết thúc ngày 14/07/2026; cắt giảm triệt để nội dung trùng domain Foods, chỉ giữ 3 nhóm tri thức bản địa được trao truyền; trung tính hóa truyền thuyết Bà Bún; định hướng tham gia Mạng lưới Thành phố Sáng tạo UNESCO (UCCN) giai đoạn 2026–2027; bảo tồn trung tính.
2. **Đồng bộ Thực thể 10 & 11:**
   - `10 Lăng Gia Long.md` và `11 Lăng Minh Mạng.md`: Đồng bộ cập nhật địa giới hành chính thuộc **phường Kim Long, thành phố Huế** theo Nghị quyết 1675/NQ-UBTVQH15 (hiệu lực từ 01/07/2025).
3. **Biên soạn hoàn tất Thực thể 12 (Lăng Thiệu Trị):**
   - `12 Lăng Thiệu Trị.md`: Hoàn thành theo chuẩn `heritage-template.md`; cập nhật địa giới hành chính làng Cư Chánh, xã Thủy Bằng cũ nay thuộc **phường Thủy Xuân, thành phố Huế** theo Nghị quyết số 1675/NQ-UBTVQH15 (hiệu lực từ 01/07/2025); làm rõ tính đặc thù: lăng duy nhất quay hướng Tây Bắc, không La thành gạch, kết hợp mô thức lăng Gia Long (lăng và tẩm song song biệt lập) và lăng Minh Mạng (Bửu thành hình tròn, hồ Ngưng Thúy bán nguyệt, Bi Đình, vọng lâu Hồng Trạch Môn); hơn 450 ô thơ văn tại điện Biểu Đức thuộc Di sản tư liệu MOWCAP 2016; cập nhật tiến độ dự án bảo tồn giai đoạn 3 (2023–2026, 60,5 tỷ đồng) phục hồi Bi Đình và lầu Đức Hinh.
4. **Biên soạn hoàn tất Thực thể 13 (Lăng Tự Đức):**
   - `13 Lăng Tự Đức.md`: Hoàn thành theo chuẩn `heritage-template.md`; vị trí thuộc thôn Thượng Ba, làng Dương Xuân Thượng cũ, địa bàn **phường Thủy Xuân, thành phố Huế**; làm rõ nguồn gốc Vạn Niên Cơ, biến cố Loạn Chày Vôi (1866) và nguồn gốc chữ "Khiêm" trong gần 50 công trình; cảnh quan lâm viên, hồ Lưu Khiêm, Xung Khiêm Tạ, Dũ Khiêm Tạ; nhà hát cổ Minh Khiêm Đường; Bi Đình và tấm bia "Khiêm Cung Ký" (Bảo vật quốc gia 2015, nặng 20 tấn, 4.935 chữ); trình bày Bồi Lăng (nơi an táng vua Kiến Phúc) theo chỉ dẫn inventory; cập nhật dự án trùng tu 99,8 tỷ đồng giai đoạn 2024–2026 (Minh Khiêm Đường 98%, Điện Hòa Khiêm 90%).
5. **Biên soạn hoàn tất Thực thể 14 (Lăng Dục Đức):**
   - `14 Lăng Dục Đức.md`: Hoàn thành theo chuẩn `heritage-template.md`; vị trí tại số 08 đường Duy Tân, thôn Tây Nhất, làng An Cựu cũ, địa bàn **phường An Cựu, thành phố Huế** (phường An Cựu mới theo NQ 1675/NQ-UBTVQH15); làm rõ tính đặc thù cốt lõi: An Lăng là nơi an táng và thờ phụng chung của 3 thế hệ hoàng đế (vua Dục Đức, vua Thành Thái, vua Duy Tân); huyền tích mộ ban đầu, bi kịch "Tứ nguyệt tam vương"; cấu trúc khiêm tốn gồm khu lăng mộ (Bửu thành song táng cùng Từ Minh Hoàng thái hậu, nhà Huỳnh Ốc, không có tượng đá ở Bái Đình) và khu tẩm điện (Điện Long Ân kiểu trùng thiềm điệp ốc); cập nhật hoàn thành dự án trùng tu 40 tỷ đồng (tháng 8/2024) và chính thức mở cửa bán vé đón khách từ ngày 01/01/2025.
6. **Biên soạn hoàn tất Thực thể 15 (Lăng Đồng Khánh):**
   - `15 Lăng Đồng Khánh.md`: Hoàn thành theo chuẩn `heritage-template.md`; vị trí tại thôn Thượng Hai, đường Đoàn Nhữ Hải, địa bàn **phường Thủy Xuân, thành phố Huế** (theo NQ 1675/NQ-UBTVQH15); làm rõ tính đặc thù: ngôi lăng xây dựng qua 4 đời vua kéo dài 35 năm (1888–1923), khởi nguồn từ Điện Truy Tư thờ Kiên Thái Vương; bước trung chuyển bản lề giữa kiến trúc cung đình cổ truyền và giao thoa Á - Âu cận đại; điện Ngưng Hy mang thức trùng thiềm điệp ốc 3 tòa nhà gỗ lim ghép liền (tam điện liên hoàn), 100 cột thếp vàng, 24 bức vẽ tích Nhị thập tứ hiếu, tranh tĩnh vật sơn dầu phương Tây, kính màu Saint-Gobain; khu mộ trên đồi Hộ Thuận Sơn với tượng quan viên xi măng cao gầy; cập nhật dự án trùng tu tổng thể trên 76 tỷ đồng và chính thức mở cửa đón khách trở lại từ ngày 30/01/2022.
7. **Biên soạn hoàn tất Thực thể 16 (Lăng Khải Định):**
   - `16 Lăng Khải Định.md`: Hoàn thành theo chuẩn `heritage-template.md`; vị trí tại triền núi Châu Chữ (núi Châu Ê), địa bàn **phường Thủy Xuân, thành phố Huế** (xã Thủy Bằng cũ đã sáp nhập vào phường Thủy Xuân theo NQ 1675/NQ-UBTVQH15); làm rõ tính đặc thù: lăng tẩm hoàng gia cuối cùng của triều Nguyễn, xây dựng ròng rã 11 năm (1920–1931) qua hai triều vua Khải Định và Bảo Đại; bố cục giật cấp 5 tầng sân với 127 bậc thang vươn theo sườn núi dốc; đỉnh cao phong cách kiến trúc chiết trung (eclecticism) giao thoa Á - Âu (Ấn Độ giáo, Phật giáo, Gothic, Roman); Cung Thiên Định với nghệ thuật khảm ghép sành sứ, pha lê và thủy tinh màu đạt trình độ bậc thầy; chiếc Bửu tán bằng bê tông cốt thép nặng gần 1 tấn tạo hình thanh thoát như lụa; pho tượng đồng vua Khải Định tỉ lệ 1:1 do Paul Ducuing tạc và Ferdinand Barbedienne đúc năm 1920 tại Paris, mạ vàng năm 1922 tại Huế; kiệt tác bích họa trần cung "Cửu Long Ẩn Vân" của nghệ nhân Phan Văn Tánh; công tác bảo tồn, chống sạt lở và chống phong hóa của HMCC.
8. **Biên soạn hoàn tất Thực thể 17 (Lăng vua Hiệp Hòa):**
   - `17 Lăng vua Hiệp Hòa.md`: Hoàn thành theo chuẩn `heritage-template.md`; vị trí tại đường Tam Thai, khu vực đồi thông núi Tam Thai, địa bàn **phường An Cựu, thành phố Huế** (phường An Tây cũ đã sáp nhập vào phường An Cựu mới theo NQ 1675/NQ-UBTVQH15); làm rõ ranh giới di sản: đây là **Di tích lịch sử cấp tỉnh** theo Quyết định số 2743/QĐ-UBND ngày 26/11/2015 của UBND tỉnh Thừa Thiên Huế, **không** thuộc Quần thể Di tích Cố đô Huế được UNESCO ghi danh; làm rõ cuộc đời bi kịch của vua Hiệp Hòa (Nguyễn Phúc Hồng Dật) trong biến loạn "Tứ nguyệt tam vương", bị quyền thần phế truất và ép uống thuốc độc ngày 29/11/1883; lăng mộ ban đầu chôn cất sơ sài theo nghi thức Quốc Công, trải qua 130 năm hoang phế giữa đồi thông; đợt trùng tu xã hội hóa năm 2013 do thân hữu người Huế và Phòng Văn Lãng Quận Vương thực hiện khôi phục diện mạo tôn nghiêm (200 m2) với tẩm lăng, bi đình, trụ biểu, bình phong sành sứ chữ Hỷ, chữ Thọ và câu đối lịch sử.
9. **Biên soạn hoàn tất Thực thể 18 (Kinh thành Huế):**
   - `18 Kinh thành Huế.md`: Hoàn thành theo chuẩn `heritage-template.md` và ranh giới phân định theo `heritage-entities-inventory.md`; cập nhật địa giới hành chính thuộc **phường Phú Xuân, thành phố Huế** theo Nghị quyết số 1675/NQ-UBTVQH15 (hiệu lực từ 16/06/2025, vận hành từ 01/07/2025 sáp nhập 6 phường nội thành: Tây Lộc, Thuận Lộc, Thuận Hòa, Đông Ba, Gia Hội, Phú Hậu; trụ sở tại 394 Đinh Tiên Hoàng); làm rõ tính đặc thù: kinh đô của triều Nguyễn suốt 140 năm (1805–1945), quy mô 520 ha, chu vi vòng thành gần 10 km (9.950 m), cao 6,6 m, dày 21 m; kiến trúc công sự Vauban kết hợp nguyên lý Dịch học phương Đông; tích hợp Kỳ Đài (ba tầng đài 17,5 m, cột cờ 37 m, tổng chiều cao 54 m), Phu Văn Lâu (xây 1819, bia "Khuynh cái hạ mã"), Nghinh Lương Đình (xây 1852, đại tu 1903, bến thuyền rồng ngự; cặp di tích in trên tờ 50.000 VNĐ), Trấn Bình Đài (Đồn Mang Cá nhỏ / Mang Cá, pháo đài thứ 25 độc lập góc Đông Bắc, chu vi 1.048 m, cao 5,1 m, tường dày 15 m, hào 32 m, cửa Trấn Bình Môn và Trường Định Môn; chiến trường biến cố Thất thủ Kinh đô đêm 05/07/1885); 10 cửa thành đường bộ có vọng lâu, 2 cửa thủy quan (Đông Thành Thủy Quan và Tây Thành Thủy Quan), bộ Cửu vị thần công (Bảo vật quốc gia 2012); cập nhật tiến độ Đề án di dời dân cư khu vực I di tích Kinh thành Huế (hơn 4.200 hộ dân sang Bắc Hương Sơ), chỉnh trang mở tuyến đường dạo bộ trên đỉnh Thượng Thành (đoạn Nam Xương sang Nam Thắng) và thông tuyến cửa Kẻ Trài (tháng 5/2026).
10. **Biên soạn hoàn tất Thực thể 19 (Đại Nội Huế):**
    - `19 Đại Nội Huế.md`: Hoàn thành theo chuẩn `heritage-template.md` và ranh giới theo `heritage-entities-inventory.md`; cập nhật địa giới hành chính thuộc **phường Phú Xuân, thành phố Huế** theo Nghị quyết số 1675/NQ-UBTVQH15 (sáp nhập 6 phường nội thành: Tây Lộc, Thuận Lộc, Thuận Hòa, Đông Ba, Gia Hội, Phú Hậu; trụ sở tại 394 Đinh Tiên Hoàng); làm rõ tính đặc thù: trái tim chính trị, hành chính và sinh hoạt hoàng gia suốt 143 năm (1802–1945); cấu trúc không gian "tam trùng thành quách" kinh đô Huế (Hoàng thành bao bọc Tử Cấm thành); chu vi Hoàng thành 2.411 m, tường cao 4 m, hào nước hồ Ngoại Kim Thủy bao quanh; 4 cửa Hoàng thành (Ngọ Môn, Hiển Nhơn, Chương Đức, Hòa Bình); trục Dũng đạo xuyên suốt từ Nam sang Bắc; tích hợp đầy đủ các công trình kiến trúc hạt nhân được phân định:
      - *Ngọ Môn:* Đài nền chữ U bằng đá Thanh và gạch vồ trổ 5 cửa vòm cuốn; bên trên là Lầu Ngũ Phụng 100 cột lim, 2 tầng 9 bộ mái lợp ngói hoàng lưu ly và thanh lưu ly; nơi cử hành lễ Truyền Lô, lễ Ban Sóc, duyệt binh và lễ thoái vị của vua Bảo Đại ngày 30/08/1945;
      - *Hồ Thái Dịch, Cầu Trung Đạo, Sân Đại Triều Nghi:* Cầu đá Thanh dành riêng cho hoàng đế; sân hai cấp thềm lát đá với các bia phẩm trật (Phẩm Sơn) phân hàng quan văn, quan võ từ nhất phẩm đến cửu phẩm;
      - *Điện Thái Hòa:* Công trình cung điện quan trọng bậc nhất, thức trùng thiềm điệp ốc tiền điện 7 gian 2 chái kép và chính điện 5 gian 2 chái kép, 80 cột gỗ lim dát vàng họa tiết long vân đồng khánh, mái ngói hoàng lưu ly, đỉnh nóc trang trí pháp lam và sành sứ; nơi diễn ra lễ Đăng quang, lễ Vạn thọ, lễ Tết Nguyên đán và các buổi đại triều mùng 1, ngày rằm; nơi đặt Ngai vàng vua triều Nguyễn (Bảo vật quốc gia 2015); mốc đại trùng tu toàn diện 128 tỷ đồng khởi công 11/2021 và nghiệm thu kỹ thuật đón khách tháng 11/2024;
      - *Khu vực thờ tự hoàng tộc:* Thế Miếu (thờ 10 vị hoàng đế triều Nguyễn), Hiển Lâm Các (đài kỷ niệm 3 tầng bằng gỗ lim cao 17 m - công trình cao nhất Hoàng thành), Cửu Đỉnh (Bảo vật quốc gia 2012, 162 bản đúc nổi ghi danh Di sản Tư liệu Ký ức Thế giới MOWCAP ngày 08/05/2024), Hưng Miếu, Triệu Miếu, Thái Miếu, Điện Phụng Tiên;
      - *Khu vực cung thất Hoàng Thái Hậu:* Cung Diên Thọ (quy mô hơn 17.500 m2, chính điện Diên Thọ, Thọ Ninh Cung, Tạ Trường Du trên hồ nước, Lầu Tịnh Minh), Cung Trường Sanh;
      - *Tử Cấm thành (Cung Thành):* Chu vi 1.298 m, 7 cửa; Điện Cần Chánh (nơi làm việc thường triều, bị phá hủy 1947, dự án phục hồi tổng thể gần 200 tỷ đồng giai đoạn 2024–2029); Điện Càn Thành và Cung Khôn Thái;
      - *Duyệt Thị Đường:* Nhà hát hoàng gia cổ nhất Việt Nam (xây năm 1826), không gian bảo tồn và diễn xướng Nhã nhạc cung đình Huế và tuồng cung đình;
      - *Thái Bình Lâu:* Nhà đọc sách ngâm thơ của hoàng đế, tái thiết thời Khải Định với nghệ thuật khảm sành sứ tinh xảo;
      - *Điện Kiến Trung:* Kiệt tác kiến trúc kết hợp Phục Hưng Pháp, Art Nouveau và mỹ thuật cung đình cổ truyền thời Khải Định và Bảo Đại; bị chiến hỏa phá hủy năm 1947; kỳ tích phục hồi 123 tỷ đồng hoàn thành xuất sắc và mở cửa đón khách từ đầu Tết Giáp Thìn 2024;
      - *Ngự uyển và bảo vật:* Vườn Thiệu Phương, Vườn Cơ Hạ; Bộ vạc đồng triều Nguyễn gồm 11 chiếc đúc thế kỷ XVII thời chúa Nguyễn (Bảo vật quốc gia 2013).
11. **Biên soạn hoàn tất Thực thể 20 (Chùa Thiên Mụ):**
    - `20 Chùa Thiên Mụ.md`: Hoàn thành theo chuẩn `heritage-template.md` và ranh giới theo `heritage-entities-inventory.md`; cập nhật địa giới hành chính thuộc **phường Kim Long, thành phố Huế** theo Nghị quyết số 1675/NQ-UBTVQH15 (sáp nhập toàn bộ diện tích và dân số phường Hương Long vào phường Kim Long); làm rõ tính đặc thù: Đệ nhất Quốc tự thời Nguyễn khởi lập năm Tân Sửu (1601) bởi chúa Tiên Nguyễn Hoàng trên đồi Hà Khê uốn lượn bên bờ sông Hương; thuộc Quần thể Di tích Cố đô Huế (Di sản Thế giới UNESCO năm 1993, mã serial 678-002); tích hợp đầy đủ hai Bảo vật quốc gia:
      - *Đại Hồng Chung chùa Thiên Mụ:* Đúc năm Canh Dần 1710 thời chúa Nguyễn Phúc Chu (nặng 1.986 kg, cao 2,5 m, đường kính miệng 1,4 m, quai bồ lao hai đầu, khắc minh văn chúa ngự bút), công nhận Bảo vật quốc gia theo Quyết định số 2599/QĐ-TTg năm 2013;
      - *Bia đá "Ngự kiến Thiên Mụ tự bia":* Dựng năm Ất Mùi 1715 thời chúa Nguyễn Phúc Chu (cao 2,6 m, rộng 1,25 m, đế rùa đá hoa cương nguyên khối, trán cẩm thạch trắng chạm ấn triện vương quyền thiêng liêng *"Đại Việt quốc Nguyễn Chúa vĩnh trấn chi bảo"* và bài ký 1.250 chữ Hán), công nhận Bảo vật quốc gia theo Quyết định số 88/QĐ-TTg năm 2020;
      - *Tháp Phước Duyên (Từ Nhân Tháp):* Biểu tượng kiến trúc của chùa và Cố đô, xây dựng năm 1844 thời vua Thiệu Trị mừng bát thọ Hoàng thái hậu Thuận Thiên, cao 21 m bát giác 7 tầng; bài thơ ngự chế "Thiên Mụ chung thanh" khắc trên văn bia thuộc Di sản Tư liệu Ký ức Thế giới MOWCAP 2016 ("Thơ văn trên kiến trúc cung đình Huế");
      - *Cụm công trình tôn giáo hạt nhân:* Cổng Tam quan 2 tầng 8 mái thờ tượng Hộ pháp; Điện Đại Hùng kiểu trùng thiềm điệp ốc (thờ Tam Thế Phật, tượng Phật Di Lặc bằng gỗ quý, hoành phi Linh Thửu Cao Phong 1714, chuông đồng nhỏ thời Gia Long 1804, khánh đồng cổ); Điện Địa Tạng, Điện Quan Âm;
      - *Dấu ấn lịch sử cận hiện đại:* Chiếc xe ô tô Austin DBA 599 (nguyên bản BMA-078) chở Bồ tát Thích Quảng Đức đi tự thiêu tại Sài Gòn ngày 11/06/1963 trong phong trào tranh đấu Phật giáo miền Nam; hòn non bộ do tổ nghề tuồng Đào Tấn cúng dường; khu tháp mộ 7 tầng của Cố Đại lão Hòa thượng Thích Đôn Hậu.
12. **Biên soạn hoàn tất Thực thể 21 (Đàn Nam Giao):**
    - `21 Đàn Nam Giao.md`: Hoàn thành theo chuẩn `heritage-template.md` và ranh giới theo `heritage-entities-inventory.md`; cập nhật địa giới hành chính thuộc **phường Thuận Hóa, thành phố Huế** theo Nghị quyết số 1675/NQ-UBTVQH15 (sáp nhập 6 phường gồm Phú Hội, Phú Nhuận, Phường Đúc, Vĩnh Ninh, Phước Vĩnh và Trường An thành phường Thuận Hóa); làm rõ tính đặc thù: Đàn tế Trời Đất duy nhất còn hiện hữu tại Việt Nam và quy mô nhất trong lịch sử, khởi công ngày 25/03/1806 và tổ chức lễ tế đầu tiên ngày 27/03/1807 thời vua Gia Long; diễn ra 98 kỳ đại tế qua 10 đời vua đến lễ tế cuối cùng ngày 23/03/1945 thời vua Bảo Đại; thuộc Quần thể Di tích Cố đô Huế (Di sản Thế giới UNESCO năm 1993, mã serial 678-005);
      - *Kiến trúc Giao đàn ba tầng:* Đỉnh cao triết lý Tam tài (Thiên - Địa - Nhân) và quan niệm Trời tròn Đất vuông; tầng trên cùng là Viên đàn (Trời, hình tròn đường kính 40,5 m, cao 2,8 m, lan can quét vôi màu xanh thiên thanh, 28 tảng đá chân cột dựng nhà bạt Thanh ốc / Hoàng khung vũ, thềm Nam 15 bậc); tầng giữa là Phương đàn (Đất, hình vuông mỗi cạnh 83 m, cao 1,1 m, lan can màu vàng địa hoàng, dựng Hoàng ốc, thềm 5 bậc tế thần linh tự nhiên); tầng dưới cùng (Người, hình vuông mỗi cạnh 165 m, cao 0,84 m, lan can màu đỏ xích tử, thềm 4 bậc, lò thiêu phần sài ở góc Đông Nam, huyệt chôn lông huyết ế mao huyết ở góc Tây Bắc);
      - *Cụm công trình phụ trợ:* Trai Cung ở góc Tây Nam (dài 85 m, rộng 65 m, tọa bắc hướng nam, chính điện Trai Cung, tả túc, hữu túc, thượng trà, thượng thiện) nơi nhà vua trai giới thanh tịnh ăn chay 3 ngày; dấu tích Thần khố, Thần trù, Tế sinh sở ở góc Đông Bắc; hệ thống 3 bình phong đá Thanh đồ sộ (mặt Nam, Đông, Tây);
      - *Rừng thông Nam Giao và đạo trị quốc:* Khởi nguồn truyền thống trồng thông quân tử từ vua Gia Long, mở rộng quy chế thời vua Minh Mạng, Thiệu Trị buộc hoàng tử và quan đại thần khi thăng chức phải lên đàn tự tay trồng một cây thông gắn biển đồng khắc tên;
      - *Lịch sử phục hồi và phát huy:* Di dời đài tưởng niệm năm 1992 để khôi phục nguyên trạng di tích, phục dựng lễ tế Nam Giao trong các kỳ Festival Huế từ năm 2004.
13. **Governance & QA Audit:**
    - Đã cập nhật đầy đủ claim-to-source mapping và fact-check vào `knowledge-base-hue/meta/heritage-research-evidence.md`.
    - Script tự động kiểm tra đạt `ALL QA CHECKS PASSED: 0 errors, 0 warnings` (không YAML frontmatter, không section cấm, không từ cấm nội bộ, không trailing whitespace) cho toàn bộ 21 file thực thể đã biên soạn.

## 3. Next Steps

Tiếp tục biên soạn Thực thể 22 (`22 Hổ Quyền.md`) thuộc nhóm Di tích vật thể nổi bật theo danh mục di sản Huế (tập trung vào đấu trường La Mã phương Đông duy nhất của Việt Nam thời Nguyễn, kiến trúc hình vành khăn lộ thiên, các trận quyết đấu voi - hổ, mối quan hệ mật thiết với Điện Voi Ré theo chỉ dẫn inventory, địa giới hành chính phường Thủy Xuân, thành phố Huế).
````

## Status trước chỉnh sửa (nguyên văn)

````markdown
# Project Status

Last updated: `2026-09-04 +07`

## Project overview

`hue_rag` xây dựng hệ thống RAG về văn hóa và du lịch Huế. Milestone hiện tại
là Hue Foods RAG MVP: truy vấn dữ liệu ẩm thực đã curate, tìm đúng evidence,
tạo context có giới hạn và sinh câu trả lời grounded. Sau khi MVP ổn định,
roadmap mới mở rộng sang Hybrid Recommender và Agentic RAG.

Project ưu tiên code/data flow dễ hiểu, complexity tương xứng nhu cầu và bằng
chứng từ dữ liệu, database, model cùng API thật.

## System and data map

Luồng chính:

```text
raw sources -> curated foods Markdown -> 572 chunks
-> embeddings/Qdrant + optional local lexical scoring
-> retrieval -> optional reranking -> bounded context
-> grounded generation -> answer-only API
```

Foods corpus hiện gồm:

- 57 restaurants;
- 24 cafes;
- 9 local specialties;
- `food-guides.md` với 18 sections;
- 91 curated Markdown files tạo 572 deterministic chunks;
- Golden Dataset V3 canonical có 45 full cases và 10 smoke rows deep-equal.

Không chunk trực tiếp từ source dumps. Curated Markdown là closed-world source
cho retrieval/evaluation; web research không tự trở thành Golden evidence.

## Current runtime and data

Production baseline hiện dùng:

- local embedding `intfloat/multilingual-e5-small`, 384 dimensions;
- active Qdrant collection `hue_foods_e5_small_384`, 572 points;
- profiles `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`;
- Python BM25 và concrete local MiniLM cross-encoder reranker;
- bounded whole-chunk context;
- grounded generation bằng `gpt-5.4-nano`;
- answer-only JSON API và startup warm-up.

Active collection còn legacy sparse vector state từ các phase trước nhưng là
read-only trong implementation/review thông thường. Dense-only candidate
`hue_foods_e5_small_384_dense` tồn tại làm blue-green evidence; production chưa
cutover.

Phase 8 Notebook 08a đã benchmark local dense embeddings trên CPU FP32 với 45
Golden V3 cases và 572 chunks. Executable catalog hiện chỉ gồm:

1. `e5-small-384` — control 384D;
2. `huydang-dek21-embedding-768` — candidate 768D;
3. `e5-base-768` — candidate 768D.

Mỗi model có 3/3 repetition evidence trên 45 Golden V3 cases và 572 chunks.

Phase 8 Notebook 08b đã hoàn tất 20-setting retrieval/fusion matrix với 70
calibration rows, 200 result rows và 900 per-case records. Unicode tokenizer
được giữ vì Underthesea không cải thiện đủ để tăng complexity. Hybrid tăng
overall recall nhưng cả BM25 và TF-IDF finalist đều `None`: category
`relationship` có nDCG@5 delta `-0.0279273`, thấp hơn guardrail `-0.02`.
Production config và active collection không thay đổi.

Curated content ngoài Foods hiện có:

- 26 entity lễ hội trong `knowledge-base-hue/festivals/festival/`;
- `festival-guides.md` là cẩm nang tổng hợp bền vững, trả lời câu hỏi phổ thông,
  định hướng theo mùa, dịp lễ và nhu cầu trải nghiệm;
- `performing_arts/performing_arts_guides.md` là file Markdown duy nhất hiện có
  trong domain nghệ thuật biểu diễn; các thư mục con hiện chưa có entity;
- `services/` và các thư mục con hiện chưa có file Markdown;
- `statistics/visitor-statistics.md` hiện có một file;
- `tickets/` hiện có `heritage-ticket-prices.md` và `ticket-types.md`;
- `tourism/travel_guides.md` là file Markdown duy nhất hiện có trong domain du
  lịch; các thư mục con hiện chưa có entity.

Commit `45eb7e0` đã bổ sung hai guide Festivals/Foods và xóa hai báo cáo trung
gian của batch 23 lễ hội. Delta riêng tại `Lễ hội Áo dài Huế.md` vẫn được giữ
ngoài commit và chưa được xử lý trong workstream kế tiếp.

## Phase status

| Phase | Status | Current result / next boundary |
|---:|---|---|
| 0 | `approved` | MVP foundation và simplicity governance |
| 1 | `approved` | Backend foundation |
| 2 | `approved` | Foods Markdown chunking |
| 3 | `approved` | Dense embedding và sparse representation simplification |
| 4 | `approved` | Qdrant ingestion; dense-only candidate chưa cutover |
| 5 | `approved` | Retrieval profiles và reranking |
| 6 | `approved` | Context, generation và answer-only API |
| 7 | `approved` | Retrieval/answer evaluation baseline |
| 8 | `not_ready` | Gate 0, Gate 1 và Notebooks 08a/08b/08c approved; post-08c multi-domain design is next |
| 9 | `not_ready` | Agentic RAG roadmap chưa có approved scope |

Git và canonical artifacts giữ lifecycle history; file này chỉ mô tả trạng thái
đang có hiệu lực.

## Decisions currently in force

- Mỗi phase có một canonical guide; reports/status không tự tạo requirement.
- Golden Dataset V3 45+10 đã approved và không được sửa trong Phase 8 benchmark
  nếu chưa có scope riêng.
- Main local benchmark profile là CPU FP32; failed/OOM phải được ghi đúng, không
  silent fallback hoặc đổi setting.
- Khi quality không khác biệt đáng tin cậy, ưu tiên model nhẹ, nhanh và đơn giản.
- Local dense Phase 8 chỉ có ba model executable hiện hành nêu trên.
- Active reranker comparison chỉ có no-rerank và current local
  `cross-encoder/ms-marco-MiniLM-L-6-v2`; BGE/Qwen rerankers không còn thuộc
  08c/08d scope.
- Initial fusion comparison dùng RRF và independent min-max weighted sum
  `0.6 dense / 0.4 sparse`; không weight grid khi chưa có observed need.
- Notebook 08b chỉ so sánh tokenizer BM25 Unicode `\w+` hiện hành với
  Underthesea `word_tokenize(..., format="text")`; không mở tokenizer grid.
- Notebook 08b có exact 20-setting matrix trên 45 Golden V3 cases. `900`
  per-case records là một record cho mỗi setting/case để audit ranking và
  fusion, không phải mở rộng Golden Dataset lên 900 câu.
- Implementer 08b được chia run thành số batch tùy tài nguyên, persist atomically
  sau từng setting, resume theo exact provenance và giải phóng tài nguyên giữa
  batch. Không shortlist trước khi reconcile đủ matrix.
- Canonical notebooks là learning documents, gọi backend trực tiếp và giữ sạch
  outputs/execution counts trong repo.
- Runtime/code/test practice dùng `skills/practical-project-coding/SKILL.md`.
- Reviewer/Implementer coordination dùng
  `skills/risk-gated-agent-review/SKILL.md` và một current handoff.
- Không thêm cost accounting, repeated consent gate, resume/run-identity,
  checksum/tamper audit hoặc validator machinery nếu exact approved scope không
  có observed need tương xứng.

## Safety and authorization boundaries

- Active `hue_foods_e5_small_384` chỉ read-only nếu không có exact user approval.
- Không expose secret hoặc đọc raw `.env` content.
- Không dùng fake provider/data/artifact hoặc old output làm fresh PASS evidence.
- Provider/model/dataset mới, paid run ngoài approved guide, deploy, active
  mutation, destructive cleanup và production cutover cần authority mới.
- Commit/push chỉ thực hiện khi latest user instruction hoặc current handoff ghi
  exact Git authorization.
- Implementer không tự approve; Reviewer không sửa runtime thay Implementer.

## Canonical document map

Bootstrap và role governance:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/IMPLEMENTER_WORKFLOW.md
session_prompt/CURRENT_HANDOFF.md
skills/risk-gated-agent-review/SKILL.md
skills/practical-project-coding/SKILL.md
```

Project/Phase 8 entrypoints:

```text
guides/README.md
guides/phase_0_mvp_foundation.md
guides/phase_8_benchmark_model_selection.md
reports/hue_foods_rag_benchmark.md
docs/superpowers/specs/2026-08-26-phase-8-benchmark-model-selection-design.md
docs/superpowers/plans/2026-08-26-phase-8-benchmark-model-selection-experiment-plan.md
```

Golden V3 and completed 08a:

```text
docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md
reports/phase_8_golden_dataset_v3_codex_review.md
docs/superpowers/specs/2026-08-28-phase-8-08a-embedding-benchmark-design.md
docs/superpowers/plans/2026-08-28-phase-8-08a-embedding-benchmark-implementation-plan.md
reports/phase_8_08a_embedding_benchmark_codex_review.md
evaluation/results/phase8_embedding_results.csv
```

Approved 08b work package:

```text
docs/superpowers/specs/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-design.md
docs/superpowers/plans/2026-08-29-phase-8-08b-retrieval-fusion-benchmark-implementation-plan.md
notebooks/08b_retrieval_fusion_benchmark.ipynb
reports/phase_8_08b_retrieval_fusion_benchmark_codex_review.md
reports/user_reports/phase_8_08b_retrieval_fusion_benchmark_user_report.md
evaluation/results/phase8_sparse_manifest.json
evaluation/results/phase8_sparse_calibration.csv
evaluation/results/phase8_sparse_results.csv
evaluation/results/phase8_sparse_cases.jsonl
```

Approved 08c work package, confirmed by the user on `2026-08-30 +07`:

```text
docs/superpowers/specs/2026-08-30-phase-8-08c-reranker-benchmark-design.md
docs/superpowers/plans/2026-08-30-phase-8-08c-reranker-benchmark-implementation-plan.md
notebooks/08c_reranker_benchmark.ipynb
evaluation/results/phase8_reranker_results.csv
evaluation/results/phase8_reranker_cases.jsonl
reports/phase_8_08c_reranker_benchmark_codex_review.md
reports/user_reports/phase_8_08c_reranker_benchmark_user_report.md
```

Governance designs and plans:

```text
docs/superpowers/specs/2026-08-29-risk-gated-agent-review-design.md
docs/superpowers/plans/2026-08-29-risk-gated-agent-review-implementation-plan.md
docs/superpowers/specs/2026-08-29-restore-core-coding-behaviors-design.md
docs/superpowers/plans/2026-08-29-restore-core-coding-behaviors-implementation-plan.md
```

## Current next action

Hai guide Festivals/Foods đã hoàn thiện ở mức curated hiện hành. Current next
action là Reviewer kiểm kê và thiết kế work package bổ sung dữ liệu answer-facing
cho năm domain: `performing_arts`, `services`, `statistics`, `tickets` và
`tourism`. Bắt đầu bằng việc xác định nhu cầu người dùng, ranh giới entity/guide,
nguồn phù hợp, mức độ biến động và thứ tự triển khai cho từng domain; chưa mở
rộng sang chunking, embeddings, index hoặc Combined Golden Dataset.

Sau khi năm domain được curate và review, roadmap mới chuyển sang thiết kế
domain-aware chunking/metadata, embedding mới, isolated full-corpus index và
Combined Golden Dataset có quota theo domain. Evaluation khi đó phải bắt đầu lại
từ Phase 7 baseline rồi chạy lại các phần Phase 8 bị ảnh hưởng; các benchmark
hiện tại chỉ là historical evidence cho Foods.

Chưa có authorization tạo embedding/index/Golden mới, mutate Qdrant, chạy
benchmark đa lĩnh vực hoặc xử lý delta `Lễ hội Áo dài Huế.md`. Exact quyền sửa
corpus cho từng domain sẽ được ghi trong handoff triển khai sau khi scope và
nguồn được chốt.

### Tiến độ miền Di sản (Heritage Domain - 2026-09-05)
- Đã hoàn thành 21/28 thực thể di sản Huế:
  - Batch 01 (1 đến 9): Đã tiếp nhận re-review từ Codex, tiến hành kiểm chứng độc lập và hoàn tất toàn bộ hiệu chỉnh theo các chuẩn mực khoa học, hành chính (Nghị quyết 1671, Nghị quyết 1675) và bảo tồn.
  - Thực thể 10 (Lăng Gia Long) và 11 (Lăng Minh Mạng): Đã khởi tạo hoàn tất và đồng bộ địa giới hành chính thuộc phường Kim Long, thành phố Huế.
  - Thực thể 12 (Lăng Thiệu Trị) và 13 (Lăng Tự Đức): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md`, cập nhật địa giới hành chính thuộc phường Thủy Xuân, thành phố Huế theo Nghị quyết 1675/NQ-UBTVQH15.
  - Thực thể 14 (Lăng Dục Đức): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md`, cập nhật địa giới hành chính thuộc phường An Cựu (mới), thành phố Huế theo Nghị quyết 1675/NQ-UBTVQH15; làm rõ An Lăng là nơi an táng và thờ phụng 3 vị vua Dục Đức, Thành Thái, Duy Tân.
  - Thực thể 15 (Lăng Đồng Khánh): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md`, cập nhật địa giới hành chính thuộc phường Thủy Xuân, thành phố Huế theo Nghị quyết 1675/NQ-UBTVQH15; làm rõ quá trình xây dựng qua 4 đời vua (1888–1923), bước chuyển tiếp kiến trúc Á - Âu và nghệ thuật sơn thếp điện Ngưng Hy.
  - Thực thể 16 (Lăng Khải Định): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md`, cập nhật địa giới hành chính thuộc phường Thủy Xuân, thành phố Huế theo Nghị quyết 1675/NQ-UBTVQH15; làm rõ kiến trúc giật cấp 5 tầng sân với 127 bậc thang, đỉnh cao nghệ thuật khảm sành sứ, bửu tán bê tông cốt thép, pho tượng đồng đúc tại Paris năm 1920 và bích họa Cửu Long Ẩn Vân.
  - Thực thể 17 (Lăng vua Hiệp Hòa): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md`, cập nhật địa giới hành chính thuộc phường An Cựu (mới), thành phố Huế theo Nghị quyết 1675/NQ-UBTVQH15; phân định chính xác ranh giới di sản: đây là Di tích lịch sử cấp tỉnh (QĐ 2743/QĐ-UBND năm 2015), không thuộc Quần thể Di tích Cố đô Huế được UNESCO ghi danh; làm rõ bi kịch "Tứ nguyệt tam vương" và dự án trùng tu xã hội hóa năm 2013.
  - Thực thể 18 (Kinh thành Huế): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md`, cập nhật địa giới hành chính thuộc **phường Phú Xuân, thành phố Huế** theo Nghị quyết 1675/NQ-UBTVQH15 (sáp nhập 6 phường nội thành: Tây Lộc, Thuận Lộc, Thuận Hòa, Đông Ba, Gia Hội, Phú Hậu); tích hợp Kỳ Đài, Phu Văn Lâu, Nghinh Lương Đình, Trấn Bình Đài (Đồn Mang Cá nhỏ / Mang Cá), 24 pháo đài Vauban, 10 cửa thành đường bộ, 2 cửa thủy quan, Cửu vị thần công (Bảo vật quốc gia 2012), hệ thống Hộ thành hào, Hộ thành hà và sông Ngự Hà; cập nhật tiến độ Đề án di dời dân cư khu vực I di tích Kinh thành Huế và tuyến đường dạo bộ trên Thượng Thành mốc 2026.
  - Thực thể 19 (Đại Nội Huế): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md` và ranh giới theo `heritage-entities-inventory.md`; cập nhật địa giới hành chính thuộc **phường Phú Xuân, thành phố Huế** theo Nghị quyết 1675/NQ-UBTVQH15; tích hợp đầy đủ các công trình kiến trúc hạt nhân: Ngọ Môn (Lầu Ngũ Phụng 100 cột, 9 bộ mái, 5 cửa vòm cuốn, nơi diễn ra lễ Ban Sóc, Truyền Lô và lễ thoái vị của vua Bảo Đại ngày 30/08/1945), Điện Thái Hòa (kiến trúc trùng thiềm điệp ốc, 80 cột lim dát vàng long vân đồng khánh, mái hoàng lưu ly, đỉnh nóc pháp lam; Ngai vàng vua triều Nguyễn - Bảo vật quốc gia 2015; mốc đại trùng tu 128 tỷ đồng nghiệm thu tháng 11/2024), Thế Miếu (thờ 10 vị vua triều Nguyễn), Hiển Lâm Các (đài kỷ niệm cao 17 m - công trình cao nhất Hoàng thành), Cửu Đỉnh (Bảo vật quốc gia 2012; các bản đúc nổi ghi danh Ký ức Thế giới MOWCAP ngày 08/05/2024), Cung Diên Thọ (cung thất quy mô nhất dành cho Hoàng Thái Hậu, Tạ Trường Du, Lầu Tịnh Minh), Cung Trường Sanh, Tử Cấm thành (Cung Thành, chu vi 1.298 m, 7 cửa), Duyệt Thị Đường (nhà hát hoàng gia cổ nhất xây năm 1826), Thái Bình Lâu (nhà đọc sách ngâm thơ của vua), Điện Kiến Trung (phong cách giao thoa Á - Âu thời Khải Định và Bảo Đại; kỳ tích phục hồi 123 tỷ đồng hoàn thành đón khách từ đầu Tết Giáp Thìn 2024), dự án phục hồi Điện Cần Chánh (gần 200 tỷ đồng giai đoạn 2024–2029), Bộ vạc đồng triều Nguyễn (Bảo vật quốc gia 2013).
  - Thực thể 20 (Chùa Thiên Mụ): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md` và ranh giới theo `heritage-entities-inventory.md`; cập nhật địa giới hành chính thuộc **phường Kim Long, thành phố Huế** theo Nghị quyết số 1675/NQ-UBTVQH15 (sáp nhập phường Hương Long vào phường Kim Long); làm rõ tính đặc thù: Đệ nhất Quốc tự thời Nguyễn khởi lập năm 1601 bởi chúa Tiên Nguyễn Hoàng trên đồi Hà Khê bên dòng sông Hương; thuộc Quần thể Di tích Cố đô Huế (Di sản Thế giới UNESCO 1993, mã serial 678-002); sở hữu 02 Bảo vật quốc gia: Đại Hồng Chung (đúc năm 1710 thời chúa Nguyễn Phúc Chu, nặng gần 2 tấn, QĐ 2599/QĐ-TTg năm 2013) và Bia đá "Ngự kiến Thiên Mụ tự bia" (dựng năm 1715 thời chúa Nguyễn Phúc Chu, đế rùa đá hoa cương, trán bia khắc ấn triện vương quyền "Đại Việt quốc Nguyễn Chúa vĩnh trấn chi bảo", QĐ 88/QĐ-TTg năm 2020); Tháp Phước Duyên (Từ Nhân Tháp, xây năm 1844 thời Thiệu Trị, cao 21 m bát giác 7 tầng); bài thơ ngự chế "Thiên Mụ chung thanh" thuộc Di sản tư liệu MOWCAP 2016; Cổng Tam quan, Điện Đại Hùng (thức trùng thiềm điệp ốc, thờ Tam Thế Phật, tượng Di Lặc, hoành phi Linh Thửu Cao Phong 1714, chuông đồng Gia Long 1804); di vật chiếc xe ô tô Austin DBA 599 của Bồ tát Thích Quảng Đức trong phong trào Phật giáo 1963; khu mộ tháp cố Đại lão Hòa thượng Thích Đôn Hậu và hòn non bộ Đào Tấn.
  - Thực thể 21 (Đàn Nam Giao): Đã khởi tạo hoàn tất theo chuẩn `heritage-template.md` và ranh giới theo `heritage-entities-inventory.md`; cập nhật địa giới hành chính thuộc **phường Thuận Hóa, thành phố Huế** theo Nghị quyết số 1675/NQ-UBTVQH15 (sáp nhập 6 phường gồm Phú Hội, Phú Nhuận, Phường Đúc, Vĩnh Ninh, Phước Vĩnh và Trường An thành phường Thuận Hóa); làm rõ tính đặc thù: Đàn tế Trời Đất duy nhất còn hiện hữu tại Việt Nam khởi công ngày 25/03/1806, khánh thành 27/03/1807 thời vua Gia Long; tổ chức 98 kỳ đại lễ qua 10 đời vua Nguyễn đến lễ tế cuối cùng ngày 23/03/1945; thuộc Quần thể Di tích Cố đô Huế (Di sản Thế giới UNESCO 1993, mã serial 678-005); kiến trúc ba tầng Giao đàn đỉnh cao triết lý Tam tài (Viên đàn - Trời - tròn, màu xanh thiên thanh; Phương đàn - Đất - vuông, màu vàng địa hoàng; Tầng dưới - Người - vuông, màu đỏ xích tử, lò phần sài và hố ế mao huyết); cụm Trai Cung khép kín nơi vua trai giới 3 ngày; dấu tích Thần khố, Thần trù, Tế sinh sở; rừng thông Nam Giao gắn với truyền thống trồng cây ghi nhận công đức của vua Gia Long, Minh Mạng, Thiệu Trị và các quan đại thần triều Nguyễn; công tác di dời đài tưởng niệm năm 1992 để khôi phục nguyên trạng di tích và phục dựng lễ tế Nam Giao trong các kỳ Festival Huế.
  - Đã cập nhật bằng chứng đối chiếu tại `knowledge-base-hue/meta/heritage-research-evidence.md`.
  - Kiểm tra QA tự động: 100% file đạt chuẩn (0 error, 0 warning). Sẵn sàng tiếp tục thực thể 22 (Hổ Quyền).
````
