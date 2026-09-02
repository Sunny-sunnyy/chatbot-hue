# Codex Review: 23 lễ hội còn lại trong danh mục cốt lõi Huế

**Decision hiện hành sau correction review vòng 3:** `ready_for_user_confirmation`
**Kết quả hiện hành:** 23/23 file đạt technical review; không còn `blocker` hoặc `major` trong scope
**Phạm vi:** 23 file entity còn lại sau khi loại trừ `Festival Huế`, `Festival Nghề truyền thống Huế` và `Lễ hội Áo dài Huế`
**Ranh giới đã được người dùng xác nhận:** Không yêu cầu section `## Nguồn dữ liệu` trong các file entity lễ hội.

> Findings ban đầu ở mục 3 được giữ làm audit trail. Kết quả nghiệm thu bản sửa ngày 02/09/2026 và correction delta hiện hành nằm tại mục 6.

## 1. Cách đọc báo cáo

- `blocker`: sai ranh giới entity, dữ kiện cốt lõi hoặc nội dung có nguy cơ làm hệ thống trả lời sai nghiêm trọng.
- `major`: claim quan trọng chưa đúng, chưa đủ căn cứ, bị khái quát từ một kỳ tổ chức hoặc không phù hợp với curated RAG.
- `minor`: lỗi nhỏ về mốc, cách diễn đạt, địa danh hoặc chi tiết không làm sai bản chất entity.
- URL trong báo cáo là evidence phục vụ correction/re-review; Implementer không cần chép URL vào body file entity.

## 2. Findings chung áp dụng theo batch

### C1 — Văn phong quảng bá và tuyệt đối hóa

Nhiều file sử dụng các cụm như “bậc nhất”, “độc nhất vô nhị”, “hoàn mỹ”, “tráng lệ”, “rực rỡ”, “kịch tính”, “hàng đầu” hoặc mô tả cảm giác chủ quan. Implementer cần chuyển sang câu mô tả trung tính và chỉ giữ nhận định so sánh khi có danh hiệu hoặc nguồn có thẩm quyền xác nhận trực tiếp.

### C2 — Dữ liệu của một kỳ bị viết thành thuộc tính ổn định

Giờ bắt đầu, thời lượng, lịch trình nhiều ngày, số người, số thuyền, chủ đề, hoạt động biểu diễn, giải thưởng và địa điểm phụ thường đến từ một kỳ cụ thể. Chỉ giữ như tri thức bền vững nếu có bằng chứng lặp lại; nếu không, gắn năm hoặc dùng “trong một số kỳ”.

### C3 — Giá vé và khẳng định miễn phí

Theo template lễ hội, không đưa giá vé cụ thể vào entity file. Các câu “hoàn toàn miễn phí”, “miễn vé”, giờ mở cửa hoặc chính sách vào cửa theo một kỳ phải được thay bằng hướng dẫn kiểm tra quy định của ban tổ chức/đơn vị quản lý từng năm.

### C4 — Địa giới hành chính hiện hành

Các phần answer-facing hiện tại còn dùng “tỉnh Thừa Thiên Huế”, “thị xã” hoặc “huyện” như địa giới đương thời. Implementer phải đối chiếu đơn vị hành chính hiện hành của thành phố Huế cho từng địa điểm; tên cũ chỉ giữ khi mô tả đúng bối cảnh lịch sử. Không thay hàng loạt nếu chưa xác minh địa bàn mới.

### C5 — Chi tiết nghi lễ, lịch sử và truyền thuyết vượt quá evidence

Các diễn trình nghi lễ quá chi tiết, lời giải thích biểu tượng, giai thoại và quan hệ nhân quả phải bám nguồn trực tiếp. Truyền thuyết phải được gắn nhãn rõ; không trình bày suy diễn hoặc kịch bản phục dựng của một năm như nghi thức cổ truyền nguyên gốc.

## 3. Findings theo từng file

Line number dưới đây trỏ vào phiên bản trước correction và có thể thay đổi sau khi Implementer sửa.

### 3.1. Lễ hội Điện Huệ Nam.md — `changes_requested`

- `major` — Dòng 89–110, 125–128 biến chương trình của một số kỳ thành nghi thức ổn định cho cả hai mùa lễ. Rước bộ/carnival từ 352 Chi Lăng là điểm nhấn của một số kỳ tháng 3 gần đây; không đủ căn cứ coi hoa đăng và phóng sinh cuối lễ là thành tố thường lệ. Tách lõi bền vững (hai kỳ tháng 3 và 7 âm lịch, rước thủy, Điện Huệ Nam–Hải Cát, thực hành thờ Mẫu) khỏi chương trình từng năm. [Sở Du lịch Huế](https://sdl.hue.gov.vn/tin-trong-tinh/dac-sac-le-hoi-truyen-thong-dien-hue-nam.html), [chương trình 2025](https://hue.gov.vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/5380a76b-8084-f011-9a7f-1866dae8d0c9).
- `minor` — Dòng 18, 22, 49, 54, 60–63, 96, 116–119 có mỹ từ, số lượng và so sánh tuyệt đối; trung tính hóa.

### 3.2. Lễ hội Cầu ngư.md — `changes_requested`

- `major` — Dòng 6, 11–12, 18–22, 53–54, 83–88 trộn địa điểm/cộng đồng Thai Dương Hạ với đình Thai Dương ở Thuận An. Hồ sơ quản lý liệt kê riêng Đình Thái Dương Hạ và Đình Thai Dương–Miếu Âm Linh. Phải xác định file mô tả lễ của cộng đồng/đình nào; nếu canonical tiếp tục gom thì phải nói rõ đây là nhóm lễ chung nguồn gốc nhưng địa điểm và chương trình riêng. [Dự thảo quy chế kiến trúc Huế](https://hue.gov.vn/Portals/0/Uploads/H57.115/Nam2026/Thang6/DU_THAO_QUY_CHE_QUAN_LY_KIEN_TRUC_THANH_PHO_HUE.pdf), [nghiên cứu ĐH Huế](https://hueuni.edu.vn/portal/vi/data/bandtdhlocal/20220301_080858_NOIDUNGLA_THANGLONG.pdf).
- `major` — Dòng 73–79, 112–120 đóng đinh lịch 10–12, đua trải và số tàu xuất quân cho mọi kỳ. Giữ quy luật tam niên Tý–Mão–Ngọ–Dậu và chính lệ 12 tháng Giêng; các hoạt động khác dùng “trong kỳ lớn/đã từng có” hoặc gắn năm.

### 3.3. Lễ tế Nam Giao.md — `changes_requested`

- `major` — Dòng 9, 49–50, 160 sai/mâu thuẫn chronology. Sửa thành: hằng năm đến 1885; gián đoạn 1886–1890; từ 1891 ba năm/lần; kỳ cuối 23/3/1945. Không gọi 1942 là kỳ cuối. [Bảo tàng Lịch sử Quốc gia](https://baotanglichsu.vn/vi/Articles/3101/70850/djoc-djao-djan-va-le-te-nam-giao-qua-tai-lieu-luu-tru.html), [Trung tâm Lưu trữ quốc gia](https://www.archives.org.vn/gioi-thieu-tai-lieu-nghiep-vu/te-giao-le-te-troi-dat-va-cac-vi-than-linh-cua-cac-vua-trieu-nguyen.htm).
- `major` — Dòng 112–145 trình bày một kịch bản/trang phục duy nhất cho toàn triều Nguyễn; kỳ 1945 ghi vua dùng mũ Cửu Long và áo bào vàng. Tách điển lệ từng giai đoạn, không khẳng định Cổn Miện là trang phục cố định xuyên suốt.

### 3.4. Lễ tế Xã Tắc.md — `changes_requested`

- `major` — Dòng 10, 56, 153–156 đặt quy luật hai năm một lần có đoàn ngự đạo lớn nhưng không có căn cứ. Bỏ quy luật này; quy mô và đoàn ngự đạo tùy kế hoạch từng năm. [Lễ tế 2025](https://nhandan.vn/trang-nghiem-le-te-xa-tac-nam-2025-tai-hue-post864232.html).
- `major` — Dòng 27, 53, 175 gọi di tích “phục hồi nguyên vẹn/còn toàn bộ cấu trúc”. Tư liệu khảo cổ cho biết di tích từng bị tàn phá nghiêm trọng. Đổi thành được khảo cổ, trùng tu/phục hồi trên cơ sở dấu tích; không gọi toàn bộ là nguyên gốc. [Bảo tàng Lịch sử Quốc gia](https://baotanglichsu.vn/vi/Articles/3127/4660/khai-quat-di-tich-djan-xa-tac-o-hue.html).

### 3.5. Lễ Ban Sóc triều Nguyễn.md — `ready_for_user_confirmation` sau minor

- `minor` — Dòng 123 nói “luôn đúng mồng 1 tháng Chạp” nhưng chính file có ngoại lệ. Đổi thành “theo lệ mồng 1; có ngoại lệ do thiên tượng hoặc hoàn cảnh”. [Trung tâm Lưu trữ quốc gia](https://www.archives.org.vn/gioi-thieu-tai-lieu-nghiep-vu/nghi-thuc-le-ban-soc-duoi-trieu-nguyen.htm).
- `minor` — Dòng 174–184, 199–209 đóng đinh thời lượng, súng thần công, quà lịch/thư pháp và miễn phí cho mọi năm. Gắn với “các kỳ phục dựng gần đây” và hướng người dùng kiểm tra chương trình. [Festival Huế 2026](https://svhtt.hue.gov.vn/tin-trong-tinh/cong-bo-festival-hue-2026-va-tai-hien-le-ban-soc-trieu-nguyen.html).

### 3.6. Lễ hội Đền Huyền Trân Công chúa.md — `changes_requested`

- `major` — Dòng 40–41 sai địa điểm tu hành/viên tịch khi ghi chùa Nôm ở Hưng Yên. Nguồn nghiên cứu ghi Trâu Sơn (Bắc Ninh), sau đó Hổ Sơn/Nộn Sơn (Nam Định); không khẳng định nơi viên tịch nếu nguồn chưa thống nhất. [Hội thảo Bảo tàng Lịch sử Quốc gia](https://baotanglichsu.vn/vi/Articles/3091/75071/hoi-thao-khoa-hoc-huyen-tran-cong-chua-cuoc-doi-va-giai-thoai.html).
- `major` — Dòng 34–41 trình bày động cơ, tục tuẫn táng và cuộc giải cứu như lịch sử chắc chắn. Chỉ giữ các mốc vững 1301, 1306, 1307; gắn chi tiết cứu thoát/động cơ bằng “theo sử liệu/giai thoại/truyền tụng”. [Tư liệu Bảo tàng](https://baotanglichsu.vn/vi/Articles/3098/15311/cong-chua-huyen-tran-voi-lich-su-dan-toc.html).
- `minor` — Dòng 107–169 biến lịch trình một kỳ thành chương trình hằng năm; giữ dâng hương, tế lễ và hoạt động văn hóa chung, các mục khác gắn năm.

### 3.7. Đại lễ Phật đản tại Huế.md — `changes_requested`

- `major` — Dòng 10–16, 87–118, 134–159, 174–178 đóng đinh ngày/giờ/tuyến và hoạt động của một số năm. Giữ chính lễ quanh rằm tháng 4 âm lịch; lễ tắm/rước Phật và sen sông Hương mô tả như nét thường gặp, lịch cụ thể theo từng năm. [Chương trình 2025](https://thuanhoa.hue.gov.vn/Trang-chu/Su-kien/Chi-tiet-su-kien/mlid/1e109d63-7922-f011-9a7e-1866dae8d0c9).
- `major` — Dòng 29, 64–65, 165 dùng số liệu “hơn 80% dân số”, “hầu hết/gần như toàn thể” ăn chay hoặc hưởng ứng mà không có căn cứ. Bỏ tỷ lệ và tuyệt đối hóa; dùng “nhiều người/nhiều gia đình”.
- `minor` — Dòng 94–95, 181–182: số lễ đài/xe hoa và miễn phí là dữ liệu theo kỳ; bỏ số lượng, dùng điều kiện.

### 3.8. Lễ hội Quán Thế Âm tại Huế.md — `changes_requested`

- `major` — Dòng 27, 43–46 nhập lịch sử dựng tượng 1969–1971 thành lịch sử lễ hội. Tách hai lớp; lễ hội thường niên được quyết định tổ chức từ năm 2001. [Phật giáo Việt Nam](https://phatgiao.org.vn/tham-thanh-tich-quan-the-am-giua-xu-hue-mong-mo-d17519.html).
- `major` — Dòng 37–41, 100, 126 tự mâu thuẫn giữa “Khánh đản”, “thành đạo” và “chứng đắc Phật quả”. Ghi trung tính: lễ hội chính tại Huế diễn ra 18–19/6 âm lịch theo cách gọi của ban tổ chức; bỏ diễn giải giáo lý không chắc. [Giác Ngộ](https://giacngo.vn/ban-tri-su-phat-giao-thua-thien-hue-se-to-chuc-le-hoi-quan-the-am-cau-nguyen-quoc-thai-dan-an-post62603.html).
- `major` — Dòng 90–135, 150–157 đóng đinh giờ, nghi thức và số lượng. Rút về nhóm hoạt động đã xác nhận; phần còn lại gắn năm hoặc bỏ.

### 3.9. Hội vật làng Sình.md — `changes_requested`

- `major` — Dòng 23, 35–46 trình bày doanh trại thủy quân, chúa Nguyễn ấn định ngày hội và huyền tích “Ông tổ môn vật” như lịch sử xác lập. Rút về truyền tụng/giả thuyết địa phương; bỏ niên đại và quan hệ nhân quả không có nguồn trực tiếp. [Tạp chí Du lịch TP.HCM](https://tcdulichtphcm.vn/du-lich-bien/mong-10-tet-ve-lang-sinh-xem-hoi-vat-c9a110461.html).
- `major` — Dòng 75–93, 110–151, 167–180 cố định kích thước sới, timeline, luật, nhóm tuổi và giải thưởng. Chỉ giữ ngày mồng 10, vật lệ và nguyên tắc “lấm lưng trắng bụng”; điều lệ khác theo từng kỳ.
- `minor` — Cập nhật địa giới hiện hành sang phường Dương Nỗ và trung tính hóa mỹ từ. [Sự kiện 2026](https://duongno.hue.gov.vn/Trang-chu/Su-kien/Chi-tiet-su-kien/mlid/2b7d7268-bf08-f111-9a80-1866dae8d0c9).

### 3.10. Hội vật làng Thủ Lễ.md — `changes_requested`

- `major` — Dòng 21–23, 38–45 khẳng định người thắng được chúa Nguyễn tuyển vào cấm quân/thủy binh nhưng nguồn chỉ xác nhận hội có lịch sử lâu đời và giá trị phát hiện tài năng. Bỏ hoặc gắn rõ là truyền tụng. [Báo Văn Hóa](https://baovanhoa.vn/doi-song-van-hoa/tung-bung-hoi-vat-truyen-thong-lang-thu-le-43124.html).
- `major` — Dòng 69–82, 93–97, 112–146 đưa 57 sắc phong, kiến trúc đình, lịch/luật/giải thành tri thức cố định. Chỉ giữ đình Thủ Lễ, mồng 6 và nguyên tắc vật cơ bản; phần còn lại cần nguồn chuyên biệt hoặc phải bỏ.
- `minor` — Cập nhật địa giới; bỏ tuyến đường, miễn phí và dịch vụ dễ stale.

### 3.11. Lễ hội Đua ghe truyền thống Huế.md — `changes_requested`

- `major` — Dòng 70–99, 129–142 áp một điều lệ cố định cho mọi trộ/kỳ. Kỳ 2024 dùng độ Tiền 2 vòng 4 tráo, độ Cúng/Phá 3 vòng 6 tráo. Giữ ba loại trộ như truyền thống chung; thể thức, cự ly, biên chế theo điều lệ từng năm. [Saigon Times](https://sgtt.thesaigontimes.vn/soi-dong-giai-dua-ghe-truyen-thong-tinh-thua-thien-hue-lan-thu-35/), [Khám phá Huế](https://khamphahue.com.vn/Hue-24h/Chi-tiet/tid/Quy-uoc-cua-cac-%E2%80%9Ctro%E2%80%9D-dua-thuyen-truyen-thong.html/pid/16881/cid/28).
- `major` — Dòng 11, 22, 42–45, 119–123, 161–164 đóng cứng địa điểm và dựng mốc khôi phục sau 1975 không có nguồn. Ghi thường tổ chức trên sông Hương, địa điểm theo công bố từng năm; lịch sử hiện đại chỉ giữ dữ kiện đã chứng minh.

### 3.12. Lễ hội Thanh Trà Huế.md — `changes_requested`

- `major` — Dòng 9–16, 47–50, 94–120 dựng chronology hai năm/lần nhưng nguồn chính thức tự mâu thuẫn về số kỳ (2026 “lần VIII”, kế hoạch 2024 từng ghi “lần XIII”). Không tự hợp nhất; bỏ danh sách kỳ và quy luật năm chẵn, ghi mùa thu hoạch và lịch theo từng kỳ. Dùng phường Thủy Xuân cho địa giới hiện hành. [Sự kiện 2026](https://hue.gov.vn/vi-vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/24637302-c597-f111-9a81-1866dae8d0c9).
- `major` — Dòng 38–50, 100–141 biến giai thoại tiến vua và hoạt động một kỳ thành nghi thức truyền thống. Giữ “tiến vua” ở mức truyền tụng; chỉ giữ các hoạt động chính thức đã công bố, gắn năm nếu cần.
- `minor` — Bỏ claim sức khỏe, bảo quản dài ngày và lời khuyên mua hàng khi không có nguồn.

### 3.13. Chợ quê ngày hội – Cầu ngói Thanh Toàn.md — `changes_requested`

- `major` — Dòng 6, 11, 49, 94–95, 154–156 coi Chợ đêm là alias và ghi tối thứ Sáu–Chủ Nhật hằng tuần. Hồ sơ hiện hành nêu phiên chợ đêm tối ngày 16 âm lịch hằng tháng; “Chợ quê ngày hội” là chương trình theo kỳ Festival. Tách hai event và sửa lịch. [Hồ sơ địa phương](https://thanhthuy.hue.gov.vn/Portals/57/Uploads/H57.125/Nam2025/Thang12/BAO_CAO_DTM_KHU_DO_THI_THUY_THANH_trang.pdf), [kỳ 2026](https://hue.gov.vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/d1229be5-5748-f111-9a81-1866dae8d0c9).
- `major` — Dòng 109–139 biến nghi lễ và danh mục trò chơi/món ăn thành cấu trúc cố định; dùng “thường/đã từng” hoặc gắn kỳ.
- `major` — Dòng 165–168 có giá 10–20 nghìn và 5–30 nghìn; xóa theo template tickets.
- `minor` — Cập nhật địa giới sang phường Thanh Thủy.

### 3.14. Lễ hội Hương xưa làng cổ – Phước Tích.md — `changes_requested`

- `major` — Dòng 26, 91–96, 109–136 biến hoạt động kỳ 2024 (SUP, chèo thuyền, sen Hà Trì, chợ quê, liên kết làng nghề) thành cấu trúc mọi kỳ và thêm Kỳ Phước/hoa đăng chưa được xác nhận. Giữ lõi nhà rường–gốm–chợ quê; gắn hoạt động với 2024 hoặc bỏ. [Ngày hội 2024](https://bthcm.hue.gov.vn/Tin-t%E1%BB%A9c-S%E1%BB%B1-ki%E1%BB%87n/Ho%E1%BA%A1t-%C4%91%E1%BB%99ng-v%C4%83n-h%C3%B3a-trong-t%E1%BB%89nh/pid/1538/cid/139?tid=Khai-mac-Ngay-hoi-%E2%80%9CHuong-xua-lang-co%E2%80%9D-nam-2024.html).
- `major` — Dòng 162–166 có giá vé/lưu trú và số homestay; xóa giá, chỉ ghi dịch vụ có thể thu phí/đặt trước.
- `minor` — Cập nhật địa giới và giảm số liệu kỹ thuật nung, số nhà, tuổi cây nếu không có nguồn trực tiếp.

### 3.15. Lễ hội Sóng nước Tam Giang.md — `changes_requested`

- `major` — Dòng 37 ghi hệ đầm phá dài 128 km; số đúng khoảng **68 km**, diện tích khoảng 22.000 ha. Sửa trực tiếp và không trộn chiều dài bờ biển với đầm phá. [Cổng TTĐT Huế](https://hue.gov.vn/en-us/Home/Investment-information/Details/Dam-pha-song-ngoi-960265).
- `major` — Dòng 26–30, 68–96, 109–133, 148–152 biến dù lượn, SUP, sân khấu và timeline của kỳ 2024 thành thường lệ. Giữ nhóm văn hóa–thể thao–ẩm thực chung; gắn hoạt động mới với 2024. [Festival 2024](https://dttm.hue.gov.vn/tin-tuc-va-su-kien/tuan-le-festival-nghe-thuat-quoc-te-hue-2024-le-hoi-song-nuoc-tam-giang.html).
- `major` — Dòng 9, 41–42, 80–82 chốt hai năm/lần/năm chẵn chưa đủ căn cứ. Ghi tổ chức theo kế hoạch, thường tháng 5–6.

### 3.16. Ngày hội Sen Huế.md — `changes_requested`

- `major` — Dòng 27, 41–43, 77–103, 120–131 biến concept “Ngự Liên/Thức Thủy”, show thực cảnh, fine dining và workshop kỳ 2026 thành cấu trúc lặp lại. Chuyển thành ví dụ/kỳ 2026; hoạt động bền vững chỉ giữ tôn vinh sen, trưng bày, sản phẩm và ẩm thực. [Sự kiện 2026](https://hue.gov.vn/Trang-chu/Cac-hoat-%C4%91ong-su-kien-noi-bat-cua-%C4%91ia-phuong-trong-thanh-pho/Chi-tiet/mlid/17bb1149-5748-f111-9a81-1866dae8d0c9).
- `major` — Dòng 34–35, 49–52, 62–66, 107–116 trộn bối cảnh văn hóa/sản phẩm sen với entity lễ hội và có nhiều claim cung đình, sinh học, ẩm thực chưa được nguồn ngày hội hỗ trợ. Rút về bối cảnh sen Huế đã kiểm chứng.

### 3.17. Ngày hội Hoàng Mai Huế.md — `changes_requested`

- `major` — Dòng 83–100 viết kích thước bảng thi, tiêu chí Cổ–Kỳ–Mỹ–Văn, giải và đấu giá như quy chuẩn cố định. Chỉ giữ nhóm hoạt động lặp lại; điều lệ phải gắn năm/quy chế. [Sự kiện 2025](https://hue.gov.vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/e25be70f-c8d7-ef11-9a7c-1866dae8d0c9).
- `major` — Dòng 113–117 gọi nhiều tên biến thể là giống Hoàng mai quý nhưng hồ sơ chỉ dẫn địa lý không hỗ trợ. Xóa section nếu không có hồ sơ; giữ đặc tính chỉ dẫn địa lý và sửa “vàng tươi” thành “vàng đậm”. [Cục SHTT](https://www.ipvietnam.gov.vn/en_US/web/guest/cac-bai-viet-ve-chi-dan-ia-ly/-/asset_publisher/fNUbGw2ZxGKy/content/bao-ho-chi-dan-ia-ly-hue-cho-san-pham-hoang-mai-mai-vang-).
- `minor` — Không chốt 10–12 ngày, ngày khai/bế mạc hoặc miễn phí; lịch/địa điểm theo từng kỳ.

### 3.18. Lễ hội làng Dương Nỗ.md — `changes_requested`

- `major` — Dòng 37–39 nói từ 2022 được định hình thành lễ hội; nguồn 2024 gọi lần hai và 2025 lần ba, suy ra kỳ đầu 2023. Sửa mốc, bỏ lịch sử “từ những năm 2000” nếu không có tư liệu. [Bảo tàng Hồ Chí Minh Huế](https://bthcm.hue.gov.vn/Tin-t%E1%BB%A9c-S%E1%BB%B1-ki%E1%BB%87n/Ho%E1%BA%A1t-%C4%91%E1%BB%99ng-b%E1%BA%A3o-t%C3%A0ng-H%E1%BB%93-Ch%C3%AD-Minh/tid/Ngay-hoi-lang-Duong-No--Hanh-trinh-thang-nam.html/pid/1517/cid/59).
- `major` — Dòng 26, 76–96 thêm hoa đăng, nghi lễ đặt họ Hồ/A Lưới và timeline ba ngày như thường lệ nhưng nguồn chỉ xác nhận rước/dâng sen, nghề, ẩm thực, trò chơi, triển lãm, Ca Huế, Bài Chòi, đua trải. Bỏ hoạt động chưa truy được; gắn năm cho phần riêng.
- `major` — Dòng 11, 74, 119–122 hardcode 14–16/5 và giờ; thực tế các năm khác nhau. Ghi “trung tuần tháng 5, lịch từng năm”.

### 3.19. Lễ Thu tế làng An Truyền.md — `changes_requested`

- `major` — Dòng 12 dùng xã Phú An; địa giới hiện hành là làng An Truyền, phường Mỹ Thượng. [Cổng TTĐT Huế](https://hue.gov.vn/Trang-chu/Cac-hoat-%C4%91ong-su-kien-noi-bat-cua-%C4%91ia-phuong-trong-thanh-pho/Chi-tiet/mlid/3cffe0ef-e2de-f011-9a80-1866dae8d0c9).
- `major` — Dòng 31–38, 55–68, 87–92, 114–120 có danh sách họ, niên đại đình, kiến trúc, lễ vật tam sinh và ẩm thực/rượu tiến vua vượt nguồn chính thức. Giữ lõi 15–17/7, ba kiệu/ba Thành hoàng, linh vật thay đổi và hát Thài; phần khác chỉ giữ khi có hồ sơ chuyên biệt.
- `minor` — Hạ giọng “nguyên vẹn nhất/độc nhất vô nhị”; bỏ giờ/đỗ xe dễ stale.

### 3.20. Hội xuân Gia Lạc.md — `changes_requested`

- `major` — Dòng 12, 51–57 trộn vị trí chợ lịch sử với địa điểm tái hiện hiện nay. Chương trình Tết Huế 2025 tổ chức tại ngã ba chợ Mai và đường Nguyễn Đình Tứ. Phân biệt vị trí lịch sử với điểm tổ chức từng năm. [Visit Hue](https://visithue.vn/cac-hoat-dong-tet-hue-tet-doan-ket-xuan-at-ty-2025-cua-quan-thuan-hoa/?pid=MjM1NTF8Y3NkbGRs0).
- `major` — Dòng 14–15, 55–57, 73–103, 113–115 biến quy ước lý tưởng của chợ xưa thành sự thật tuyệt đối hiện tại. Dùng “theo mô tả/truyền thống của chợ xưa”; chương trình hiện đại tùy kế hoạch.
- `minor` — Rút tiểu sử và chuỗi phục dựng chưa đủ nguồn; giữ Nguyễn Phúc Bính lập chợ năm 1826 và chợ họp ba ngày Tết.

### 3.21. Lễ giỗ Tổ nghề Kim hoàn.md — `changes_requested`

- `major` — Dòng 33–50 có niên đại Cao Đình Hương và quyết định di tích mâu thuẫn giữa các nguồn; “quốc tang”, sắc phong và năm dựng nhà thờ chưa có hồ sơ gốc. Không tự chọn một nguồn: giữ hai tổ sư, truyền nghề, các ngày tưởng niệm; bỏ chi tiết mâu thuẫn cho đến khi có hồ sơ di tích. [Khám phá Huế](https://khamphahue.com.vn/Du-lich/Ban-can-biet/Chi-tiet/tid/Le-gio-to-nghe-kim-hoan.html/pid/12660/cid/82).
- `major` — Dòng 10 gán 7/2 và 27/2 cho ngày mất từng tổ nhưng nguồn ngành mâu thuẫn. Ghi “ngày tế chính 7/2; có lệ tưởng niệm 27/2” đến khi xác minh.
- `major` — Dòng 65–71, 75–92 dựng kiến trúc, bài trí, giờ và lễ vật như ổn định; rút về thời điểm, nơi tổ chức, ý nghĩa và kỹ pháp nghề đã xác nhận.

### 3.22. Lễ tế Bà Bún Vân Cù.md — `changes_requested`

- `major` — Dòng 12, 58, 112–113 dùng xã Hương Toàn/thị xã Hương Trà; hiện là TDP Vân Cù–Nam Thanh, phường Kim Trà, TP Huế. [Sự kiện 2026](https://kimlong.hue.gov.vn/Trang-chu/Su-kien/Chi-tiet-su-kien/mlid/47d0536e-011d-f111-9a80-1866dae8d0c9).
- `major` — Dòng 11, 28, 63, 72–88, 103–109 lấy chương trình đón bằng năm 2025 làm lệ thường niên. Lõi là tế ngày 22 tháng Giêng; đua ghe có nguồn lặp; các hoạt động khác gắn năm 2025 hoặc “một số kỳ”. [Bộ VHTTDL](https://bvhttdl.gov.vn/don-nhan-di-san-van-hoa-phi-vat-the-quoc-gia-nghe-lam-bun-van-cu-20250220091526189.htm).
- `major` — Dòng 26, 50, 94–99 có claim an toàn thực phẩm tuyệt đối (“diệt khuẩn”, “khử triệt để”, không hóa chất, “tiêu chuẩn vàng”). Xóa; chỉ mô tả đặc điểm sợi bún theo nguồn.

### 3.23. Lễ hội Ẩm thực Huế.md — `changes_requested`

- `major` — Dòng 6–15, 21, 35–41, 55–64 gộp Lễ hội Ẩm thực chay, “Huế–Kinh đô Ẩm thực”, “Ẩm thực Kinh đô Huế với bốn phương” và các ngày hội quốc tế thành alias/một chu kỳ giả. Phải mô tả đây là nhóm chương trình liên quan nhưng không đồng nhất; không coi tên từng kỳ là alias. [Kế hoạch Festival 2025](https://hue.gov.vn/Portals/0/Uploads/VBPL/Nam2025/T2/00.00.H57-35-KH-UBND-2025-PL3.pdf).
- `major` — Dòng 39, 60, 81–105 lấy kỳ 2026 (23–26/7, khoảng 80 gian, các phân khu/show) làm quy luật. Gắn rõ 2026 hoặc bỏ; hoạt động chung chỉ giữ trưng bày, thưởng thức, quảng diễn và giao lưu.
- `major` — Dòng 8–12, 57–64, 120–123 tạo ba đợt thường niên và giờ 9–23h không đúng cho mọi chương trình. Bỏ lịch tổng hợp; tra chương trình cụ thể từng năm.
- `major` — Dòng 39, 111–114, 130–131 có lượng khách, “nơi duy nhất”, niêm yết và giám sát ATTP tuyệt đối nhưng chưa truy được. Xóa hoặc gắn nguồn/kỳ cụ thể.

## 4. Thứ tự correction đề xuất

1. **Ranh giới entity:** Cầu ngư, Lễ hội Ẩm thực Huế, Chợ quê/Chợ đêm.
2. **Sai dữ kiện cốt lõi:** Nam Giao, Huyền Trân, Quán Thế Âm, Sóng nước Tam Giang, Kim hoàn, Dương Nỗ.
3. **Temporal grounding:** Điện Huệ Nam, Xã Tắc, Phật đản, hai hội vật, Đua ghe, Thanh Trà, Phước Tích, Sen, Hoàng Mai, An Truyền, Bà Bún.
4. **Địa giới, ticket, travel advice và văn phong:** áp dụng một batch cuối sau khi nội dung cốt lõi ổn định.

Không sửa máy móc theo search/replace. Mỗi file cần giữ lại verified core và loại bỏ phần không đủ evidence thay vì cố bảo toàn độ dài hiện tại.

## 5. Acceptance cho Implementer

- Sửa đủ 22 file có `major`; xử lý hai minor của Ban Sóc trong cùng batch nếu thuận tiện.
- Không thay đổi ba file đã duyệt: `Festival Huế.md`, `Festival Nghề truyền thống Huế.md`, `Lễ hội Áo dài Huế.md`.
- Không thêm `## Nguồn dữ liệu` vào entity file theo quyết định của người dùng.
- Mọi hoạt động theo kỳ phải gắn năm hoặc được diễn đạt có điều kiện; không biến lịch/giờ/địa điểm/chủ đề của một năm thành thuộc tính vĩnh viễn.
- Không còn giá cụ thể, khẳng định miễn phí cố định hoặc travel advice chưa được chứng minh.
- Phần hiện tại dùng địa giới hành chính hiện hành; tên cũ chỉ nằm trong bối cảnh lịch sử.
- Truyền thuyết/giai thoại được gắn nhãn; không suy diễn quan hệ nhân quả.
- Văn phong trung tính, answer-facing; bỏ mỹ từ và so sánh tuyệt đối không có căn cứ.
- Mỗi file bắt đầu bằng một H1, không YAML frontmatter, không placeholder, không link nội bộ trong body.
- Implementer chạy `git diff --check`, báo exact changed paths và mapping từng finding vào correction; Reviewer re-review exact diff và chỉ mở lại nguồn khi correction thay claim.

## 6. Nghiệm thu correction ngày 02/09/2026

### 6.1. Kết luận

- **Decision:** `changes_requested`.
- **Đạt để người dùng xác nhận (5/23):** `Lễ tế Nam Giao.md`, `Lễ tế Xã Tắc.md`, `Lễ Ban Sóc triều Nguyễn.md`, `Lễ hội làng Dương Nỗ.md`, `Lễ tế Bà Bún Vân Cù.md`.
- **Còn major (18/23):** 18 file còn lại, với correction delta tối thiểu ở mục 6.2.
- `git diff --check`: pass. Cấu trúc kỹ thuật đạt: mỗi file có một H1, không có `## Nguồn dữ liệu`, không còn giá tiền cụ thể trong batch.
- Không file entity nào được Reviewer chỉnh sửa trong vòng nghiệm thu này.

### 6.2. Correction delta bắt buộc cho 18 file

#### Lễ hội Điện Huệ Nam.md

- `major`, dòng 111–113: phần tư vấn vẫn bảo đảm buổi sáng có rước bộ và buổi tối có hoa đăng, trái với chính phần mô tả hoạt động tùy kỳ ở dòng 83, 96–97. Đổi thành điều kiện: chỉ tham dự nếu chương trình năm đó có rước bộ/hoa đăng và phải kiểm tra lịch ban tổ chức.
- `minor`: sửa typo “rước rước bộ” ở dòng 27; các dòng 74–76, 103 cũng cần giữ cùng điều kiện theo kỳ.

#### Lễ hội Cầu ngư.md

- `major`, dòng 11–15, 21, 87: vẫn nhập tên di tích. Dùng **“Đình làng Thai Dương (cộng đồng Thai Dương Hạ hạ giáp), phường Thuận An”** cho nơi tổ chức bờ Nam; phân biệt với **Đình Thái Dương Hạ** ở địa bàn Hải Dương cũ phía bờ Bắc. Evidence: [nghiên cứu ĐH Huế](https://hueuni.edu.vn/portal/vi/data/bandtdhlocal/20220301_080858_NOIDUNGLA_THANGLONG.pdf), [lịch sự kiện Sở VHTT](https://svhtt.hue.gov.vn/tin-trong-tinh/cac-hoat-dong-van-hoa-va-the-thao-mung-dang-mung-xuan-at-ty-2025.html).

#### Lễ hội Đền Huyền Trân Công chúa.md

- `major`, dòng 11, 57, 77: địa chỉ hiện hành vẫn là phường An Tây. Sửa thành **151 Thiên Thai, phường An Cựu, thành phố Huế**. Evidence: [thông cáo Sở VHTT Huế 2026](https://svhtt.hue.gov.vn/thong-tin-tuyen-truyen/thong-cao-bao-chi-le-hoi-den-huyen-tran-xuan-binh-ngo-nam-2026.html).
- `minor`, dòng 94–96: mở đầu danh mục phần hội bằng “tùy kế hoạch từng năm”.

#### Đại lễ Phật đản tại Huế.md

- `major`, dòng 64–69, 101–103: vẫn đóng đinh tuần lễ 8–15 tháng 4 âm lịch và hoạt động vào mùng 8, 14, 15 cho mọi năm. Chỉ giữ chính lễ rằm tháng 4 là lõi; lễ tắm Phật, rước Phật, sen và hoa đăng phải ghi theo lịch từng năm. Chương trình 2026 kéo dài 21/5–7/6/2026 và hoa đăng ngày 22/4 âm lịch, cho thấy các mốc phụ trợ thay đổi. Evidence: [chương trình chính thức 2026](https://phongdinh.hue.gov.vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/3317bba8-5548-f111-9a81-1866dae8d0c9).

#### Lễ hội Quán Thế Âm tại Huế.md

- `major`, dòng 62–64, 82–83, 103–104: có thể giữ hai ngày 18–19 tháng 6 âm lịch và chính lễ ngày 19; không được đóng đinh khai hội, hoa đăng, thả chim và khung buổi cho mọi kỳ. Đổi các nội dung phụ thành “thường/tùy chương trình từng năm”.

#### Hội vật làng Sình.md

- `major`, dòng 12, 14, 63, 97: sửa địa chỉ hiện hành từ xã Phú Mậu thành **phường Dương Nỗ, thành phố Huế**; Phú Mậu chỉ dùng trong bối cảnh địa giới cũ. Evidence: [Kế hoạch UBND TP Huế 2026](https://hue.gov.vn/Portals/0/Uploads/VBPL/Nam2026/Thang1/00.00.H57-07-KH-UBND-2026-PL2_signed.pdf).
- `major`, dòng 30–32: quan hệ từ vị trí quân sự đến sự hình thành hội vật vẫn được viết như lịch sử xác lập. Gắn rõ “theo truyền tụng/nguồn địa phương” hoặc bỏ quan hệ nhân quả.

#### Hội vật làng Thủ Lễ.md

- `major`, dòng 11, 13, 19, 64, 97: thay thị trấn Sịa/huyện Quảng Điền bằng địa chỉ hiện hành **xã Quảng Điền, thành phố Huế**. Evidence: [Kế hoạch Festival Huế 2026](https://hue.gov.vn/Portals/0/Uploads/00.00.H57/Nam2026/Thang1/00.00.H57_500_KH_UBND_2025_PL3.pdf).
- `major`, dòng 21, 32–34: nguồn gốc thao luyện/tuyển tráng đinh thời chúa Nguyễn vẫn được trình bày như fact. Gắn nhãn truyền tụng hoặc bỏ.

#### Lễ hội Đua ghe truyền thống Huế.md

- `major`, dòng 11, 71–74, 92–94: không coi đoạn Dã Viên–Phú Xuân/Công viên Lý Tự Trọng là địa điểm cố định. Viết “trên sông Hương, địa điểm/lễ đài theo công bố từng năm”; địa điểm cũ chỉ là ví dụ có gắn năm. Kỳ 2026 công bố tại Công viên Phú Xuân. Evidence: [sự kiện 2026](https://adminthanhthuy.hue.gov.vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/b2e9ccb8-b08c-f111-9a81-1866dae8d0c9).
- `major`, dòng 22, 37–39: bỏ quan hệ chưa có văn bản gốc rằng sau 1975 giải được định hình cấp tỉnh và “ấn định” ngày 2/9; nếu cần chỉ giữ dữ kiện giải đã được duy trì nhiều năm.

#### Lễ hội Thanh Trà Huế.md

- `major`, dòng 13, 32, 69, 105: sửa địa giới hiện hành thành **phường Thủy Xuân**; Thủy Biều, Lương Quán và Nguyệt Biều chỉ là không gian văn hóa/địa danh gốc. Kỳ VIII năm 2026 tổ chức tại 423 Bùi Thị Xuân. Evidence: [Cổng TP Huế](https://hue.gov.vn/vi-vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/24637302-c597-f111-9a81-1866dae8d0c9).
- `major`, dòng 35–36, 80: giữ chuyện tiến vua và tuyến rước thủy ở mức giai thoại/hoạt cảnh đã từng tái hiện; không viết thành thông lệ lịch sử nếu chưa có nguồn trực tiếp.

#### Chợ quê ngày hội – Cầu ngói Thanh Toàn.md

- `major`, dòng 11, 66: bỏ nhánh “cuối tuần/tùy thời kỳ” nếu không có evidence; nguồn hiện có chỉ xác nhận chợ đêm ngày 16 âm lịch hằng tháng.
- `major`, dòng 46, 84–86: không khẳng định lễ rước bài vị từ nhà thờ họ Trần và tuần tế là cấu trúc bền vững. Gắn với kỳ cụ thể có nguồn, hoặc rút thành hoạt động dâng hương/tri ân tùy chương trình.

#### Lễ hội Hương xưa làng cổ – Phước Tích.md

- `major`, dòng 12, 20, 68, 107: sửa xã Phong Hòa/huyện Phong Điền thành **phường Phong Dinh, thành phố Huế** cho địa chỉ hiện hành. Evidence: [Kế hoạch Festival Huế 2026](https://phongphu.hue.gov.vn/Portals/0/Uploads/00.00.H57/Nam2026/Thang1/00.00.H57_500_KH_UBND_2025_PL3.pdf).

#### Lễ hội Sóng nước Tam Giang.md

- `major`, dòng 12, 14, 21, 33, 36, 45, 51, 53, 67, 78, 108: địa điểm hiện hành ở Cồn Tộc thuộc **xã Đan Điền, thành phố Huế**; Quảng Lợi/Quảng Điền chỉ dùng cho các kỳ trước sắp xếp. Evidence: [Kế hoạch Festival Huế 2026](https://phongphu.hue.gov.vn/Portals/0/Uploads/00.00.H57/Nam2026/Thang1/00.00.H57_500_KH_UBND_2025_PL3.pdf), [sự kiện xã Đan Điền](https://dandien.hue.gov.vn/Du-khach/Thong-tin-du-khach/Su-kien/Chi-tiet-su-kien/mlid/be7e102b-e72b-f111-9a81-1866dae8d0c9).

#### Ngày hội Sen Huế.md

- `major`, dòng 24, 69–83: workshop nón lá sen, hoa sen giấy và nghệ thuật ánh sáng là format được xác nhận ở kỳ 2026, không phải cấu trúc thường lệ. Gắn rõ “kỳ 2026/đã từng” hoặc chỉ giữ nhóm hoạt động lặp qua nhiều kỳ.
- `major`, dòng 30–32: bỏ hoặc bổ sung nguồn lịch sử trực tiếp cho claim triều Nguyễn quy hoạch sen trắng để dâng cúng và ướp trà tiến vua; nguồn sự kiện không đủ chứng minh.

#### Ngày hội Hoàng Mai Huế.md

- `major`, dòng 10, 60–61: bỏ thời lượng “thường 7–10 ngày”; ghi tổ chức vào nửa sau tháng Chạp và lịch cụ thể theo kế hoạch năm.
- `major`, dòng 75–77: bỏ phân nhóm và tiêu chí chấm thi như quy chuẩn ổn định, hoặc gắn đúng kỳ/quy chế có nguồn.
- `minor`: cập nhật phường Đông Ba cũ ở dòng 11, 53; sửa “vàng tươi sáng” thành “vàng đậm”; bỏ đảm bảo “mở cửa tự do”.

#### Lễ Thu tế làng An Truyền.md

- `major`, dòng 12, 91: sửa xã Phú An thành **phường Mỹ Thượng, thành phố Huế**.
- `major`, dòng 22, 32–36, 75–80: bỏ hoặc cung cấp nguồn chuyên biệt cho niên đại Hậu Lê/thế kỷ XV–XVI, lần trùng tu 1903, xếp hạng 1994, diễn giải nguồn gốc mùa vụ và phần ẩm thực/rượu làng chưa được chứng minh.
- `major`, dòng 10–11, 59: nguồn chính thức xác nhận lễ diễn ra ba ngày cố định 15, 16, 17 tháng 7 âm lịch; không viết “khoảng” hoặc “2–3 ngày”.

#### Hội xuân Gia Lạc.md

- `major`, dòng 11, 47–50: phân biệt địa điểm lịch sử ở Nam Phổ với địa điểm tái hiện năm 2025 tại ngã ba Chợ Mai–Nguyễn Đình Tứ; không dùng phường Phú Thượng như địa giới hiện hành.
- `major`, dòng 22, 54–60: các quy ước lý tưởng hóa của chợ xưa như không mặc cả và danh mục trò chơi/sản vật không phải thuộc tính cố định của chương trình hiện đại. Gắn “theo mô tả về chợ xưa”; chương trình phục dựng tùy kỳ.
- `minor`: phục hồi mốc thành lập đã kiểm chứng là năm 1826, không dùng khoảng 1820–1830.

#### Lễ giỗ Tổ nghề Kim hoàn.md

- `major`, dòng 31–34: năm sinh–mất của Cao Đình Độ và Cao Đình Hương vẫn đang được khẳng định dù nguồn mâu thuẫn. Bỏ các năm 1744–1810 và 1773–1821, hoặc chỉ giữ khi có hồ sơ di sản/tư liệu gốc đủ mạnh.

#### Lễ hội Ẩm thực Huế.md

- `major`, dòng 107: không khái quát rằng các hội chợ ở công viên “thường miễn phí” và món ăn bán theo “giá niêm yết” cho cả nhóm sự kiện. Hướng người dùng kiểm tra chính sách vào cửa và giá của từng chương trình.
- `minor`, dòng 69–70, 94: địa điểm/chức năng và việc hội tụ đủ ba dòng ẩm thực chỉ đúng với một số chương trình; dùng “đã từng/tùy kỳ/qua các chương trình khác nhau”.

### 6.3. Minor còn lại trong 5 file đã đạt

- `Lễ Ban Sóc triều Nguyễn.md`: thống nhất dòng 10 với dòng 69, 198 thành “các kỳ phục dựng gần đây thường tổ chức ngày 1/1; kiểm tra thông báo từng năm”.
- `Lễ hội làng Dương Nỗ.md`: dòng 82, bỏ “nặn tò he” hoặc ghi rõ là ví dụ tùy kỳ nếu chưa có evidence cho các kỳ đã đối chiếu.
- `Lễ tế Bà Bún Vân Cù.md`: không gán chắc nhân vật cô Bún mang họ Bùi; bám đúng dị bản truyền thuyết được chọn hoặc bỏ chi tiết không thống nhất. Không bảo đảm cơ sở nghề luôn nhận khách tham quan.

### 6.4. Acceptance vòng correction tiếp theo

- Chỉ cần sửa 18 file ở mục 6.2 và có thể xử lý minor ở mục 6.3 trong cùng batch.
- Không mở lại 5 file đã đạt ngoài các minor được nêu, trừ khi correction bắt buộc làm thay đổi claim liên quan.
- Báo cáo implementation phải mapping từng bullet ở mục 6.2 sang dòng đã sửa; không dùng tuyên bố chung “đã chuẩn hóa địa giới”.
- Chạy `git diff --check`; không commit/push khi chưa có chỉ thị Git mới từ người dùng.

## 7. Nghiệm thu correction vòng 2 ngày 02/09/2026

### 7.1. Kết luận

- **Decision:** `changes_requested`; chưa đủ điều kiện commit/push.
- `git diff --check`: pass.
- Cấu trúc kỹ thuật pass: mỗi entity có đúng một H1, không YAML frontmatter,
  không `## Nguồn dữ liệu`, placeholder hoặc liên kết nội bộ.
- Địa giới đã sửa đúng cho An Cựu, Dương Nỗ, Thủy Xuân, Phong Dinh, Đan
  Điền, Quảng Điền, Mỹ Thượng, Kim Trà và Thanh Thủy. Tuy nhiên sáu file vẫn
  dùng đơn vị trước sắp xếp như địa giới hiện hành.
- Worktree có 24 entity thay đổi so với `HEAD` `66e58a7`, trong đó
  `Lễ hội Áo dài Huế.md` nằm ngoài phạm vi 23 file và chưa được khai báo trong
  implementation report. Handoff ghi base `ba6b694` nhưng base review thực tế
  phải là `66e58a7`; vì vậy chưa thể coi declared diff là khớp.

### 7.2. Correction delta bắt buộc

#### Lễ hội Điện Huệ Nam.md

- `major`, dòng 12, 74, 77, 116: `phường Gia Hội` và `xã Hương Thọ` đang được
  dùng như địa giới hiện hành. Cập nhật địa chỉ answer-facing theo đơn vị sau
  sắp xếp; 352 Chi Lăng thuộc phường Phú Xuân, còn Điện Huệ Nam/Hải Cát thuộc
  phường Kim Long. Chỉ giữ tên cũ khi ghi rõ bối cảnh lịch sử.

#### Đại lễ Phật đản tại Huế.md

- `major`, dòng 15–16, 56–57: Tổ đình Từ Đàm không còn thuộc phường Trường An
  và Quốc tự Diệu Đế không còn thuộc phường Gia Hội theo địa giới hiện hành.
  Dùng phường Thuận Hóa cho Từ Đàm và phường Phú Xuân cho Diệu Đế; tên cũ chỉ
  dùng trong bối cảnh lịch sử.

#### Lễ tế Nam Giao.md

- `major`, dòng 11, 34, 108: Đàn Nam Giao đang được đặt tại phường Trường An
  như địa giới hiện hành. Cập nhật thành phường Thuận Hóa; nếu nhắc Trường An
  thì phải ghi rõ là địa bàn cũ.

#### Lễ tế Xã Tắc.md

- `major`, dòng 11, 52, 93: Đàn Xã Tắc đang được đặt tại phường Thuận Hòa như
  địa giới hiện hành. Cập nhật thành phường Phú Xuân; nếu nhắc Thuận Hòa thì
  phải ghi rõ là địa bàn cũ.

#### Lễ giỗ Tổ nghề Kim hoàn.md

- `major`, dòng 13, 33, 53: khu lăng mộ tại kiệt 175 Phan Bội Châu đang được
  đặt tại phường Trường An như địa giới hiện hành. Cập nhật thành phường Thuận
  Hóa; tên cũ chỉ dùng trong bối cảnh lịch sử.

#### Lễ hội Quán Thế Âm tại Huế.md

- `major`, dòng 11, 53, 71: núi Tứ Tượng/thôn Bằng Lãng đang được đặt tại xã
  Thủy Bằng như địa giới hiện hành. Cập nhật thành phường Thủy Xuân; `Thủy
  Bằng` chỉ giữ như địa bàn cũ hoặc trong bối cảnh lịch sử.
- `major`, dòng 26: phần tổng quan vẫn liệt kê lễ thắp hoa đăng như thành phần
  không điều kiện. Đồng bộ với dòng 83: đây là hoạt động tùy chương trình từng
  kỳ.

#### Lễ Ban Sóc triều Nguyễn.md

- `major`, dòng 127: vẫn khẳng định lễ phục dựng diễn ra “định kỳ mỗi năm một
  lần vào ngày 1 tháng 1”, trái correction minor và chính các dòng 10, 69,
  198. Đổi thành “các kỳ phục dựng gần đây thường tổ chức ngày 1/1; kiểm tra
  thông báo từng năm”.

#### Chợ quê ngày hội – Cầu ngói Thanh Toàn.md

- `major`, dòng 66: vẫn khẳng định có “chợ đêm cuối tuần”, trong khi evidence
  hiện có chỉ xác nhận phiên chợ đêm ngày 16 Âm lịch hằng tháng. Bỏ nhánh cuối
  tuần và mô tả đúng phiên được xác nhận.
- `major`, dòng 120: không khẳng định khuôn viên chợ quê “mở cửa tự do” như
  chính sách ổn định; hướng người dùng kiểm tra quy định hiện hành của đơn vị
  quản lý.

#### Lễ Thu tế làng An Truyền.md

- `major`, dòng 32, 74–79, 87: correction yêu cầu bỏ phần ẩm thực/rượu làng
  chưa được chứng minh, nhưng nội dung về nghề nấu rượu, `Rượu làng Chuồn`,
  món ăn đầm phá và lời khuyên thưởng thức vẫn còn. Xóa các claim này; không
  thay bằng travel advice khác nếu chưa có nguồn chuyên biệt.

#### Ngày hội Sen Huế.md

- `major`, dòng 103: không khẳng định các gian hàng “mở cửa tự do” cho mọi kỳ.
  Chính sách vào cửa/đăng ký phải được mô tả là tùy chương trình và cần kiểm
  tra thông báo của ban tổ chức.

#### Lễ hội Ẩm thực Huế.md

- `major`, dòng 107: đổi “thường miễn phí” thành “thường vào cửa tự do” không
  giải quyết finding. Bỏ khái quát chính sách vào cửa cho cả nhóm sự kiện;
  hướng người dùng kiểm tra vé/voucher/giá của từng chương trình.

### 7.3. Evidence và nguồn hành chính

- Nghị quyết 1675/NQ-UBTVQH15: phường Gia Hội và Thuận Hòa cũ thuộc phường
  Phú Xuân; Trường An cũ thuộc phường Thuận Hóa; Thủy Bằng cũ thuộc phường
  Thủy Xuân; đồng thời xác nhận các đơn vị Phong Dinh, Kim Trà, Mỹ Thượng,
  Đan Điền, Quảng Điền, Thanh Thủy và Dương Nỗ:
  https://xaydungchinhsach.chinhphu.vn/sap-xep-dvhc-danh-sach-40-xa-phuong-moi-cua-thanh-pho-hue-119250622214953671.htm
- Cổng TP Huế xác nhận phường Thủy Xuân hình thành từ Thủy Biều, Thủy Bằng và
  Thủy Xuân:
  https://hue.gov.vn/Trang-chu/To-chuc-hanh-chinh/orgid/913a6173-d73f-4f3c-9862-139ca29c6264
- Văn bản TP Huế năm 2026 xác nhận Hải Cát hiện thuộc phường Kim Long:
  https://hue.gov.vn/Trang-chu/He-thong-van-ban-phap-luat/doc/all/vb/58442

### 7.4. Acceptance vòng correction 3

- Chỉ sửa 11 file ở mục 7.2; không mở lại 12 entity còn lại.
- Không sửa `Lễ hội Áo dài Huế.md`; giữ nguyên delta ngoài scope để Reviewer
  xử lý tách biệt khi đóng Git.
- Cập nhật implementation report với mapping từng bullet mục 7.2 và ghi đúng
  base `66e58a7`.
- Chạy `git diff --check`; không commit/push. User đã cấp quyền cho Reviewer
  commit/push sau khi technical review đạt, không phải cho Implementer bỏ qua
  review gate.

## 8. Nghiệm thu correction vòng 3 ngày 02/09/2026

### 8.1. Kết luận

- **Technical verdict:** `ready_for_user_confirmation`.
- **Scope đạt:** 23/23 entity thuộc báo cáo này; 11/11 correction ở Mục 7.2 đã
  được áp dụng đầy đủ, không còn `blocker` hoặc `major` trong scope.
- Người dùng đã cấp quyền đóng Git bằng commit/push sau khi technical review
  đạt. Reviewer có thể thực hiện closure mà không cần consent gate lặp lại.
- `Lễ hội Áo dài Huế.md` là delta ngoài scope 23 file, không được đưa vào commit
  closure này và vẫn được giữ nguyên trong worktree.

### 8.2. Kết quả quan sát

- Địa giới hiện hành đã đồng bộ theo Nghị quyết 1675/NQ-UBTVQH15 và evidence
  chính thức được ghi ở Mục 7.3.
- Các nội dung còn sót về chợ đêm cuối tuần, chính sách mở cửa tự do, phần
  ẩm thực/rượu An Truyền, mốc phục dựng Ban Sóc và hoa đăng Quán Thế Âm đã
  được sửa đúng correction delta.
- Mỗi entity có đúng một H1; không YAML frontmatter, `## Nguồn dữ liệu`, liên
  kết nội bộ hoặc placeholder.
- `git diff --check`: pass.

### 8.3. Git closure

- Stage đúng 23 entity thuộc scope cùng Codex review và implementation report.
- Không stage `Lễ hội Áo dài Huế.md` hoặc thay đổi ngoài package.
- Commit và push lên nhánh `main` theo quyền người dùng đã cấp.
