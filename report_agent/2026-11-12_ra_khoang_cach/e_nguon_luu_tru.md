# Nguồn dữ liệu cơ sở lưu trú ở Huế — khảo sát công khai để User quyết · phần của E

Người viết: E · 20:50 12/11/2026 (`date`) · A giao (User hỏi tối 12/11/2026) · **0 USD API** (1 lượt Codex + 12 lần E mở trang / file `robots.txt`). **Chỉ khảo sát — không cào thử, không đăng nhập, không gửi biểu mẫu.**
Mục tiêu User nêu: trợ lý **giới thiệu được cơ sở lưu trú theo khu + loại, không nói giá**. Nhãn: **[đã mở]** = E tự mở hôm nay · **[Codex]** · **[báo cáo cũ]** · **[chưa kiểm]**. Các câu về điều khoản / robots ghi như **sự thật để User quyết**, không phải lời khuyên pháp lý.

## 1. Trả lời nhanh
- **Dữ liệu mở đã tải (08/2026) không có file lưu trú** [báo cáo cũ — khảo sát nguồn 06/11]; cổng dữ liệu mở thành phố **chưa công bố** bộ lưu trú, kế hoạch của thành phố ghi dự kiến **12/2026** [Codex].
- **Có nguồn chính thức đọc được bằng trang HTML thường:** Cơ sở dữ liệu du lịch quốc gia (Cục Du lịch Quốc gia) — lọc được "Thành phố Huế", ước ~300 cơ sở ⇒ **~340 trang**, chạy xong trong chưa tới một giờ trên máy đang có, **không cần thuê máy**.
- Các sàn đặt phòng (Booking, Agoda, Traveloka, Trip.com): **điều khoản cấm thu thập tự động** (trích ở bảng); giá / phòng trống là thứ ta không dùng; không cần tới chúng cho mục tiêu trên.

## 2. Bảng nguồn (xếp theo cách lấy: file / dữ liệu mở → API chính thức → phải đọc trang)

| # | Nguồn | Số cơ sở ở Huế | Trường có | Trường cũ nhanh | Cách lấy | robots.txt · điều khoản · chống bot | Dữ liệu cá nhân |
|---|---|---|---|---|---|---|---|
| 1 | **Dữ liệu mở Huế đã tải** (`data/nguon_mo_huegov_2026-08-05/`) | **0** — không có file lưu trú [báo cáo cũ] | — | — | đã có | — | bộ này có file cá nhân khác (hướng dẫn viên, mã số thuế quán ăn) — không liên quan lưu trú, không mở |
| 2 | **Cổng dữ liệu mở TP Huế** (data.hue.gov.vn) | chưa có bộ lưu trú; dự kiến 12/2026 [Codex] | chưa biết | — | khi có: tải file / API | [chưa kiểm] | chưa biết |
| 3 | **OpenStreetMap** (Overpass API) | **208** ở khung trung tâm (tên 166 · điện thoại 47 · website 24) [báo cáo cũ, đếm 06/11] | tên, loại (`tourism=hotel / guest_house / hostel…`), **toạ độ**; địa chỉ / sao lúc có lúc không | ít | **API công khai**, một truy vấn | giấy phép ODbL: phải ghi công; phát hành lại cơ sở dữ liệu rút ra thì theo cùng giấy phép [Codex] | số điện thoại do cộng đồng nhập (của cơ sở) |
| 4 | **Cơ sở dữ liệu du lịch quốc gia** — csdl.vietnamtourism.gov.vn/cslt (Cục Du lịch Quốc gia VN) | cả nước **14.549** bản ghi [đã mở]; riêng Huế **~313** theo một trang tổng hợp bên thứ ba [Codex, chưa kiểm trên trang gốc] | danh sách: tên + địa chỉ + nguồn (cơ quan quản lý nhập / cơ sở tự đăng ký); trang chi tiết: loại hình, **hạng sao**, số phòng, điện thoại, email, website, tiện nghi [Codex]; **không toạ độ** | hạng sao (đổi theo quyết định), điện thoại | **đọc trang HTML**: có bộ lọc "Thành phố Huế", loại hình, hạng; 15 bản ghi / trang, phân trang `?page=N`, nội dung có sẵn trong HTML (không cần trình duyệt giả) [đã mở] ⇒ ước ~21 trang danh sách + ~313 trang chi tiết ≈ **340 lượt tải** | `robots.txt`: **không có file** (404) [đã mở 12/11]; chân trang **không có** điều khoản / câu cấm [đã mở]; không thấy dấu hiệu chống bot [chưa kiểm sâu] | điện thoại di động + email của cơ sở nhỏ (hộ kinh doanh) ⇒ **không lấy** hai trường này |
| 5 | **Huế TRIPO** — huetripo.hue.gov.vn/co-so-luu-tru (Sở VH-TT-DL TP Huế) | "826" theo kết quả tìm [Codex, chưa xác minh]; E mở trang thấy danh sách **rỗng** vì nạp bằng JavaScript | bộ lọc: loại, phường / xã, hạng sao, giá, điểm yêu thích [đã mở]; trường từng thẻ [chưa kiểm] | giá, điểm đánh giá | **phải cào**, và phải dùng trình duyệt tự động hoặc tìm API nội bộ (không có tài liệu) | `robots.txt`: **không có file** (404) [đã mở]; chân trang chỉ ghi bản quyền của Sở, không có điều khoản [đã mở] | [chưa kiểm] |
| 6 | **Visit Huế** (visithue.vn, mục Lưu trú) · tin của Sở Du lịch | không có tổng; riêng 4–5 sao: **21** cơ sở đầu 2026 [Codex] | tên, địa chỉ, loại, hạng (bài viết) | hạng sao | đọc bài HTML, nhập tay được (21 dòng) | trang chủ yêu cầu ghi nguồn khi đăng lại [Codex] | không thấy |
| 7 | **Google Places API** | theo truy vấn | tên, loại, địa chỉ, toạ độ, điện thoại, website, điểm đánh giá | điểm đánh giá | **API trả phí**: 32–35 USD / 1.000 lượt sau phần miễn phí [Codex] | điều khoản **cấm lưu** ngoài mã địa điểm (toạ độ tối đa 30 ngày) [Codex] ⇒ không dựng kho từ đây được | — |
| 8 | **Booking.com** | [chưa kiểm] | tên, loại, sao, địa chỉ, toạ độ, tiện nghi, điểm, giá | giá, phòng trống, điểm | API **chỉ cho đối tác** được duyệt [Codex]; còn lại phải cào | `robots.txt` không chặn trang kết quả tìm / trang khách sạn cho mọi bot, nhưng chặn các đường dữ liệu bản đồ [đã mở]. **Điều khoản A15.2 (cập nhật 25/08/2025): "you're not allowed to access, monitor, copy, scrape/crawl, download…"** bằng phương tiện tự động khi chưa có văn bản cho phép; A15.3: họ chặn hệ thống tự động bị nghi thu thập [đã mở] | không |
| 9 | **Agoda** | [chưa kiểm] | như trên | giá, điểm | chương trình đối tác (cần duyệt) [Codex] | `robots.txt` chặn `/*/hotel/all/`, không có Crawl-delay [đã mở]; điều khoản cấm theo dõi / sao chép / trích xuất tự động khi chưa có chấp thuận bằng văn bản [Codex] | API nhà riêng có liên hệ chủ nhà ⇒ không dùng |
| 10 | **Traveloka** | [chưa kiểm] | như trên | giá, điểm | API đối tác phải đăng ký + chứng nhận [Codex] | `robots.txt` **chặn** `/hotel`, trang chi tiết, trang tìm kiếm cho bot chung [đã mở]; điều khoản cấm truy cập / sao chép tự động [Codex] | — |
| 11 | **Trip.com** | [chưa kiểm] | như trên | giá, điểm | không thấy API mở | `robots.txt` **chặn** `/hotels/list`, mọi `*searchresults*`, trang chi tiết theo mã [đã mở] | — |
| 12 | **Mytour** · **iVIVU** · Vntrip | [chưa kiểm] | tên, địa chỉ, sao, giá | giá | không thấy API / file | Mytour: `robots.txt` chặn `/quick-search`, có sơ đồ trang `/sitemap/hotels` [đã mở]; quy chế cấm sao chép để cung cấp cho bên thứ ba khi chưa có văn bản [Codex]. iVIVU: chỉ chặn `/du-lich/*?*` [đã mở]. Vntrip: không có `robots.txt` (404) [đã mở] | — |

## 3. Xếp hạng cho mục tiêu "giới thiệu cơ sở theo khu + loại, không nói giá"

1. **Nguồn 4 (cơ sở dữ liệu du lịch quốc gia) — đủ nhất, công ít nhất.** Là danh sách của cơ quan quản lý ngành, có loại hình + hạng sao + địa chỉ (đúng 3 thứ cần), trang HTML thường. Thiếu toạ độ ⇒ khu suy từ **phường / xã trong địa chỉ** (đủ cho "theo khu"). Chỉ lấy: tên, loại, hạng, địa chỉ, số phòng, nguồn nhập; **bỏ** điện thoại, email, giá.
2. **Nguồn 3 (OpenStreetMap) — bổ sung toạ độ** cho cơ sở trùng tên (nếu sau này muốn "gần điểm X"); một truy vấn API, ghi công theo giấy phép.
3. **Nguồn 6 — 21 cơ sở 4–5 sao:** nhập tay được trong 30 phút, dùng để đối chiếu hạng sao của nguồn 4.
4. **Nguồn 5 (TRIPO):** nhiều cơ sở hơn (nếu số 826 đúng) nhưng khó lấy hơn (JavaScript), và cùng chủ quản thành phố với bộ dữ liệu mở dự kiến công bố 12/2026 ⇒ **chờ bộ chính thức** hợp lý hơn cào.
5. **Các sàn đặt phòng (8–12): không cần và không nên là nguồn đầu.** Thứ chúng hơn nguồn 4 là giá, phòng trống, điểm đánh giá — đúng những trường cũ nhanh và ta đã quyết không nói giá. Sự thật để User cân: Booking / Agoda / Traveloka có câu cấm thu thập tự động trong điều khoản; Traveloka và Trip.com chặn cả trong `robots.txt`; Booking nói rõ sẽ chặn hệ thống tự động.

**Nếu cào (User đã nói sẵn sàng):** cào **nguồn 4 trước** — ~340 lượt tải, mỗi lượt cách 2–3 giây ⇒ ~15–20 phút, chạy trên máy đang có (**không cần thuê máy**; thuê máy chỉ đáng khi cào sàn lớn có chống bot). Độ khó: thấp (HTML có sẵn, phân trang bằng tham số). Việc cần làm trước khi cào thật: mở một trang chi tiết bằng tay để chốt danh sách trường; xác nhận số ~313 bằng bộ lọc Huế trên trang gốc.

## 4. Đưa vào kho được không — và cần User quyết gì
- **Được về kỹ thuật**, nhưng là **mở rộng phạm vi kho** (kho hiện là 204 bài tự soạn, có kiểm) ⇒ theo luật dự án cần User duyệt: (a) nguồn (đề xuất nguồn 4 + 6); (b) dạng đưa vào: **bảng có cấu trúc do code đọc** (như bảng điểm lịch trình — khuyến nghị: lọc theo khu / loại / hạng bằng code, không qua tìm theo nghĩa) hay bài Markdown trong kho; (c) nhãn hiển thị: "theo danh mục của Cục Du lịch Quốc gia, cập nhật <ngày tải>; chưa kiểm từng cơ sở"; (d) không lấy điện thoại / email / giá.
- **Rủi ro biết trước:** dữ liệu ngành có bản ghi "cơ sở tự đăng ký" chất lượng không đều; hạng sao có thể hết hạn; không có toạ độ; ~300 dòng tên riêng trong kho có thể làm nhiễu tầng tìm nếu đưa vào dạng bài ⇒ thêm lý do chọn dạng bảng.
- **Thứ tự đề xuất:** bản "khu nên ở + link bản đồ" (plan `docs/superpowers/plans/2026-11-12-luu-tru-khu-va-link-plan.md`) làm trước — không phụ thuộc dữ liệu này; danh sách cơ sở là bước sau, có plan riêng khi User chọn nguồn.

## 4b. Bổ sung 20:51 12/11/2026 — số người, ngày nhận / trả phòng, mức giá (User hỏi)

**Hướng mặc định A nêu:** số người + ngày = **tham số của link tìm phòng do code dựng** (trang đặt phòng hiện giá thật); trợ lý không nói giá phòng cụ thể, không cộng tiền phòng vào đâu; nếu sau này đưa cơ sở vào kho thì chỉ lưu **mức giá** nếu nguồn có.

**Trang nào nhận số người / ngày / khu trên URL tìm kiếm công khai** (từ khảo sát 05/11 của E — hồ sơ private `data/phase_11_nghien_cuu/luu_tru/e5_khu_o_va_link.md`; hôm nay không mở lại trang đặt phòng):

| Đích | Mẫu URL | Mang được | Căn cứ | Lưu ý để User quyết |
|---|---|---|---|---|
| **Google Maps** | `https://www.google.com/maps/search/?api=1&query=<khách sạn gần <khu>, Huế>` | khu / cụm tìm — **không** ngày, **không** số người | **tài liệu chính thức** của Google (Maps URLs), không cần khoá | đang dùng cho thẻ lịch trình; ổn định nhất |
| **Booking.com** | `https://www.booking.com/searchresults.html?ss=<khu, Huế>&checkin=YYYY-MM-DD&checkout=YYYY-MM-DD&group_adults=N&group_children=M&no_rooms=K&lang=vi` | khu + **ngày nhận / trả + số người lớn / trẻ em + số phòng** | tham số **quan sát từ URL thật** của bên thứ ba; **không có tài liệu chính thức** cho URL website (tài liệu chính thức chỉ có cho API đối tác) | đặt một link để người dùng tự bấm **không phải** thu thập tự động (điều khoản A15.2 nói về truy cập / sao chép bằng máy); rủi ro: tham số có thể đổi mà không báo ⇒ cần test định kỳ "link còn mở đúng trang kết quả" |
| **Agoda** | `…/?textToSearch=…&checkIn=…&checkOut=…&rooms=…&adults=…` (quan sát) | như Booking | không tài liệu | điều khoản Agoda **cấm đặt link sâu** khi chưa có chấp thuận bằng văn bản ⇒ **không dùng** |
| **Google Travel / Hotels** | `https://www.google.com/travel/search?q=<chuỗi>&hl=vi` | chỉ chuỗi tìm; ngày trong chuỗi chỉ là gợi ý, không đặt được số khách | không có đặc tả URL | không đáng tin để mang tham số |
| Traveloka · Trip.com · Mytour | [chưa kiểm] | [chưa kiểm] | — | cần khảo sát riêng nếu User muốn |

**Nguồn nào có hạng sao / mức giá ổn định:** hạng sao — nguồn 4 (cơ sở dữ liệu du lịch quốc gia) và nguồn 6 (danh sách 4–5 sao của ngành) là **hạng chính thức** theo quyết định công nhận (đổi chậm, theo kỳ xếp hạng). Mức giá — **không nguồn chính thức nào** có mức giá ổn định; nguồn 4 có giá ở "một số bản ghi" [Codex] (không rõ ngày); các sàn có giá theo ngày (cũ ngay). ⇒ Nếu cần "mức": **suy từ hạng sao + loại hình** bằng luật ghi rõ (vd homestay / nhà nghỉ / 1–2 sao = bình dân · 3 sao = tầm trung · 4–5 sao / resort = cao cấp) và ghi nhãn "mức ước theo hạng, không phải giá" — đây là **đề xuất**, cần User duyệt luật.

## 5. Giới hạn
- Số cơ sở của các sàn đặt phòng **không lấy được** (Codex không mở trang đặt chỗ theo luật script; E không mở trang tìm phòng).
- Con số ~313 (nguồn 4) và 826 (nguồn 5) **chưa xác minh trên trang gốc**.
- E mở `robots.txt` của 9 tên miền ngày 12/11/2026 (2 trang chính quyền + Vntrip: không có file); trích điều khoản Booking do E mở, Agoda / Traveloka / Mytour theo Codex.
- Chưa kiểm cơ chế chống bot thực tế của bất kỳ trang nào (không cào thử).
