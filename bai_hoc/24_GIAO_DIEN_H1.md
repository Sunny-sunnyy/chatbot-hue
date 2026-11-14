# Bài 24 — Giao diện "Sông Hương": đẹp hơn mà không chậm hơn, và đo được

*Cập nhật lần cuối: 18:50, ngày 14/11/2026 · thêm ảnh tối 14/11 (184 ⇒ 218 / 224 bài; ảnh hiện được cạnh câu trả lời 146 ⇒ 169). Trước: 16:17, ngày 14/11/2026 · nối tiếp bài 17; đã sửa theo một lượt kiểm độc lập và thêm ảnh Khám phá (ghi ở Nguồn). Thêm chiều 14/11: dòng sông đi qua từng điểm của lịch (cả trên điện thoại), trang Giới thiệu có ba bến dọc sông và màn "Huế qua các thời kỳ", bỏ mọi dòng ghi công trên trang. Thêm ảnh chiều 14/11: 184 / 216 bài.*

## Bảng từ — tên mình dùng và tên gốc

Từ đánh dấu **mới** là lần đầu gặp; các từ còn lại đã có ở bài trước.

| Tên trong bài | Tên gốc | Nghĩa ngắn |
|---|---|---|
| Hiệu ứng theo cuộn — **mới** | **scroll-driven animation** (CSS `animation-timeline`) | Chuyển động chạy theo vị trí cuộn trang, trình duyệt tự làm, không cần thư viện. |
| Chuyển trang mượt — **mới** | **View Transitions** (`document.startViewTransition`) | Trình duyệt tự làm mờ / trượt giữa trang cũ và trang mới. |
| Giảm chuyển động | **prefers-reduced-motion** | Cài đặt của máy cho người dễ chóng mặt. Bật lên thì trang phải đứng yên. |
| Độ xô lệch bố cục — **mới** | **CLS** (Cumulative Layout Shift) | Phần trang bị xê dịch lúc đang tải. Dưới 0,1 là tốt. |
| Tương phản | **contrast ratio** (ngưỡng **4,5 : 1**) | Chữ sáng hơn nền bao nhiêu lần. Dưới 4,5 thì khó đọc. |

---

*Bài 17 kể trang cổng bản đầu và tốc độ trả lời. Bài này kể lần làm lại giao diện ngày 14/11: chọn hướng thế nào, hiệu ứng làm bằng gì, và mình đo ra sao để
trang đẹp lên mà không chậm đi, không khó đọc hơn.*

## Quay lại người hướng dẫn viên

Một người hướng dẫn viên giỏi mà mặc đồ nhàu, cầm cuốn sổ chữ chi chít, khách vẫn thấy kém tin. Trình bày là một phần của nghề. Nhưng trình bày cũng không
được che mất nội dung: chữ phải đọc được, trang không được nhảy lung tung, người hay chóng mặt phải xem được.

Ngày 14/11 anh nhận xét trang Giới thiệu "chỉ có văn bản", trang Lên kế hoạch "đơn giản quá", và đặt mức tối thiểu: **ít nhất phải được như Huế TRIPO**.
TRIPO là trang du lịch Huế đang chạy thật, có trợ lý lên lịch.

## Chọn hướng

**Học gì từ TRIPO.** Mình chụp TRIPO ở hai khổ màn hình rồi đếm. TRIPO trông "sinh động" nhờ năm thứ: ảnh thật, biểu tượng có màu, nhãn dạng viên, nền đổi màu
theo từng khối, con số nổi bật. Không phải nhờ chuyển động: nó chỉ có thẻ nhấc nhẹ khi rê chuột, chữ chat hiện dần, khung chờ lấp lánh. Mình chỉ học phần
trình bày, không học cách xếp lịch, vì lần đo trước đã thấy lịch của TRIPO có lỗi giờ.

**Ba hướng mẫu,** dựng thành trang HTML để anh xem trước:
- **H1 "Sông Hương":** xanh ngọc và màu nước sâu, tiêu đề chữ có chân, ảnh tràn viền. Đây là bước tiếp của tên anh đã chọn từ 07/11.
- **H2 "Men lam Hoàng cung":** lam men với vàng, bố cục kiểu sách.
- **H3 "Hoàng hôn tím":** tím với cam, lưới ảnh nhiều cỡ.

Anh chọn H1. Xem mẫu đầu, anh thấy "ổn hơn nhưng không có hiệu ứng gì đặc biệt". Mình làm bản hiệu ứng thứ hai, anh thấy "đã ổn hơn" và cho làm thật.

## Hiệu ứng làm bằng gì

Câu hỏi là có nên dùng thư viện hiệu ứng như các trang "wow" hay dùng. Mình đo trước khi chọn (cỡ sau nén, số byte trình duyệt thật sự tải):

| Cách | Cỡ thêm vào trang | So với gói JS lúc đó (112 KB) |
|---|---|---|
| Motion (bản đầy đủ) | 51,8 KB | khoảng +46 % |
| GSAP kèm hiệu ứng cuộn | 44,2 KB | khoảng +39 % |
| **CSS của trình duyệt + khoảng 30 dòng JS** | **0 KB thư viện** | — |

Mình cũng mở 6 trang du lịch đẹp để xem họ dùng gì: **0 / 6 dùng thư viện hiệu ứng nặng**, 5 / 6 dùng hiệu ứng theo cuộn bằng CSS. Ở 17 trang khác, các trang
dựng cảnh 3D gần như không chạy được trên máy không có card đồ hoạ (một trang 0 khung hình mỗi giây, một trang chờ gần 2 phút). Ba trang nhẹ nhất mượt 57–60
khung hình mỗi giây; các trang CSS nặng hơn chậm hơn (khoảng 31–44). Máy đo không có card đồ hoạ, nên số này chỉ để so các trang với nhau.

Vì vậy mình chọn **CSS + chút JS**. Nghiên cứu "vì sao một trang gây ấn tượng" cũng cho cùng kết luận: ấn tượng đến từ **một khoảnh khắc chính được dàn
dựng**, không phải từ nhiều hiệu ứng rải khắp nơi. Khoảnh khắc chính của mình là **dòng sông vẽ dần khi cuộn**:
- trên lịch trình: mỗi ngày một dòng sông **đi qua từng điểm** theo thứ tự trong ngày (bản đầu chỉ là một đường nối các ngày);
- ở trang Giới thiệu: sông chảy dọc qua **ba bến** (hỏi ⇒ tìm trong kho ⇒ trả lời kèm nguồn). Ba bến cùng kể **một** câu hỏi thật ("Ăn sáng ở Huế nên
  thử món gì?"): bến 1 là câu hỏi, bến 2 là số đoạn tìm được, bến 3 là câu trả lời (rút gọn) kèm nút "Hỏi thử câu này".

Bản đầu ẩn đường sông trên điện thoại; từ chiều 14/11 cả hai chỗ đều có sông trên điện thoại.

Thêm chiều 14/11:
- **"Huế qua các thời kỳ"** ở trang Giới thiệu: sáu mốc từ 1306 tới nay. Chữ viết lại từ bài trong kho. Trên máy tính, ảnh đứng yên bên trái và đổi theo mốc
  đang đọc; trên điện thoại, mỗi mốc có ảnh riêng.
- **Lịch:** tên chặng mỗi ngày (vd "Kinh thành → Đầm phá và biển") và nhãn loại điểm có màu. Màu luôn đi kèm chữ, nên không phải đoán màu.
- **Trang chưa xếp lịch:** hiện một lịch "Ví dụ" do chính bộ xếp dựng, kèm nút "Xếp lịch như ví dụ".
- Người review bắt một lỗi trước khi vào bản chạy: hiệu ứng ảnh lộ dần trên khung ảnh đứng yên làm số năm "1306" bị cắt thành "306" ở mốc đầu tiên.
  Hiệu ứng theo cuộn chỉ chạy trước khi khung đứng yên, nên tới mốc 1 vẫn chưa mở hết. Sửa: bỏ hiệu ứng đó cho khung ảnh trên máy tính.

Các hiệu ứng khác:
- ảnh đầu trang chủ đổi qua lại giữa 3 ảnh, có nút **Dừng ảnh**;
- thẻ nhấc nhẹ, chữ hiện dần khi cuộn tới;
- chuyển trang mượt; ảnh trên thẻ bài "bay" sang ảnh đầu trang bài.

**Luật cứng:**
- Mọi hiệu ứng chỉ chạy khi máy **không bật giảm chuyển động**. Bật lên thì trang đứng yên, ảnh đầu trang chỉ hiện một ảnh.
- Hiệu ứng chỉ dùng phép dịch và độ mờ, không đổi kích thước khối, để trang không bị xô lệch.

## Đo ba thứ trên bản thật

Mỗi đợt code xong, một người đo chạy trình duyệt tự động (Chromium) trên bản build thật, ở hai khổ màn hình (1440 và 390 điểm ảnh). Tương phản thì đo cả trên
bản mẫu HTML lúc chọn hướng:

| Đo gì | Ngưỡng | Lần đầu | Sau khi sửa |
|---|---|---|---|
| Tương phản chữ / nền, **bản mẫu** | ≥ 4,5 : 1 | menu chỉ 1,83–2,71 | 0 lần trượt; thấp nhất 6,07 |
| Tương phản chữ / nền, **code thật** | ≥ 4,5 : 1 | — | 0 lần trượt / 12 lần đo |
| Độ xô lệch (CLS), trang danh sách bài | ≤ 0,1 | 0,23 – 0,34 (thẻ bài tải sau đẩy chân trang) | ≤ 0,045, nhờ ô giữ chỗ đúng cỡ |
| CLS trang chủ và Lên kế hoạch trên điện thoại | ≤ 0,1 | 0,148 và 0,226 | ≤ 0,040 (ô thời tiết chừa sẵn chỗ; trang chờ biết tính năng nào bật rồi mới vẽ) |
| CLS trang Giới thiệu trên điện thoại | ≤ 0,1 | 0,17 – 0,66 (thẻ "làm được gì" nở ra khi biết tính năng bật) | ≤ 0,03 (chờ đủ dữ liệu rồi mới vẽ thân trang) |
| Máy bật giảm chuyển động | 0 hiệu ứng | — | 0 |

**Cái giá:** gói JS tăng **+10,5 KB** (112 ⇒ 122,6 KB sau nén), vượt mức 8 KB của kế hoạch. Phần lớn nhất là trang Khám phá (bảng ghi công ảnh). Mình
không thêm thư viện nào. Mức 8 KB là mức "phải ghi lý do"; lý do đã ghi, người điều phối nhận.

**Ảnh cho trang Khám phá (đợt đầu, chiều 14/11).** Đợt này **167 / 207 bài** có ảnh (nay 218 / 224, xem dưới): 35 ảnh Wikimedia Commons (giấy phép mở) và 132 ảnh lấy từ trang web, ghi nguồn
từng ảnh. 29 ảnh từng có nhãn **"Ảnh minh hoạ"**, vì người xem không chắc ảnh chụp đúng chính nơi đó. Bài không có ảnh vẫn là ô màu, không mượn ảnh bài
khác. **Từ chiều 14/11** trang không hiện dòng ghi công hay nhãn nào dưới ảnh nữa (anh yêu cầu); nguồn ảnh vẫn giữ trong bảng dữ liệu.
Lúc đó bảng ghi công 167 ảnh được tách ra một file riêng, chỉ tải khi mở trang bài hoặc Giới thiệu, nên gói JS chỉ còn **123,5 KB**. Chiều 14/11 bảng này
bỏ hẳn khỏi trang (nguồn ảnh giữ trong thư mục dữ liệu riêng). Bảng vốn đã ở file riêng nên bỏ nó không làm gói nhỏ đi. Lần đo gần nhất (bản gộp thử chiều
14/11, đã có "Huế qua các thời kỳ") là **124,44 KB**; sau đó thêm sông ba bến, điểm nhấn lịch, ảnh dưới câu trả lời — chưa đo lại.

**Thêm ảnh chiều 14/11: 167 ⇒ 184 / 216 bài.** Thêm 13 ảnh cho những bài về một nơi hoặc một quán còn trống: hai agent con chọn ảnh **độc lập**, chỉ giữ ảnh
mà cả hai cùng chọn; 7 ảnh trong số đó bị đánh "không chắc". Rồi thêm ảnh cho ba trong bốn bài kho mới (bài 22): cầu, nhà ga, nhà vườn (nhà vườn "không chắc").
Bài chùa thì hai người chọn hai ảnh khác nhau, cả hai đều là cổng chùa thật; người làm chọn ảnh rõ hơn theo luật người điều phối đặt và đánh "không chắc".
Lúc đó có **38 ảnh "không chắc"**: chúng vẫn hiện ở Khám phá, nhưng **không hiện cạnh câu trả lời** của trợ lý (bài 25).

**Thêm ảnh tối 14/11: 184 ⇒ 218 / 224 bài** (anh dặn ảnh ở mọi địa điểm, món ăn, di tích phải tìm đầy đủ). Kho lúc này có 224 bài (bài 22). Làm ba lượt:
- **Lượt chính:** bài về một nơi, một món đang trống được 9 ảnh. 19 bài chủ đề (vé, đi lại, lưu trú theo khu, cẩm nang) trước để ô màu, nay có **ảnh minh hoạ
  đúng chủ đề ở Huế** (ví dụ quầy vé cho bài vé), luôn gắn "không chắc" nên không bao giờ hiện cạnh câu trả lời. Xem lại 38 ảnh "không chắc": 11 bài được nâng
  lên "chắc" (6 thay ảnh có biển tên đọc được, 5 giữ ảnh cũ đã xem tay).
- **Lượt bổ sung:** tra thêm cho những quán còn trống; còn **6 bài trống** (đều là quán), có lý do từng bài — ảnh dính dấu nước lớn, chỉ có ảnh ghép, trang lỗi, hoặc
  không tìm ra trang nào, hay ảnh tìm được không chắc là đúng quán.
- **Lượt nâng "không chắc":** 8 / 37 bài một nơi được nâng lên "chắc".

Số ảnh **hiện được cạnh câu trả lời** (có ảnh, không "không chắc"): **146 ⇒ 169**. Ảnh "không chắc" nay là 49 (38 lúc chiều): 20 ảnh bài chủ đề, 29 ảnh bài một nơi. Tốn khoảng 0,1 USD tiền tìm ảnh (Serper — dịch vụ tìm trên Google, trả
tiền theo lượt); tra trang bằng Codex (một trợ lý AI khác, tự mở trang công khai) tính vào gói ChatGPT.

**Người làm nhìn trước, người review nhìn lại mọi ảnh sẽ hiện** — bước này bắt nhiều lỗi nhất. Ba ảnh mà **cả hai** agent con đều chấm "chắc" vẫn bị người làm bác khi nhìn lại: múa lân
không rõ làng nào, hai quán cà phê không thấy biển tên. Ảnh duy nhất trên kho ảnh mở ghi đúng tên biển Thuận An có trẻ nhỏ mặc đồ bơi ở giữa khung, trái luật chọn ảnh ⇒ người
review bắt, bài Thuận An giữ ảnh "không chắc" cũ và lịch vẫn **33 / 34** điểm có ảnh. Ở lượt nâng, 10 ảnh được nâng chỉ vì "lấy từ trang chính thức" bị người review trả lại:
9 ảnh món hay ly nước chung chung, không nhìn ra quán nào, và 1 ảnh múa lân không rõ làng. Luật rút ra: nguồn chính thức chỉ đủ khi **chính tấm ảnh** nhận ra được nơi đó; bài về một món thì đúng
món là đủ.

## Một chuyện thật: thẻ "Thông tin nhanh" lặng lẽ xoá mất giờ mở cửa

Trang bài mới có một thẻ bên phải tên "Thông tin nhanh". Code tách mục "Thông tin chung" của bài ra thẻ đó, rồi **xoá mục đó khỏi thân bài** cho khỏi lặp.
Trên vài bài mẫu thì nhìn rất gọn.

Lúc review, mình không xem mẫu. Mình gọi API lấy **cả 207 bài** rồi chạy đúng luật tách đó. Kết quả:
- 103 bài có thẻ, nhưng **51 bài mất dòng**;
- 29 bài bị cắt từ dòng thứ 8.

Dòng bị mất thường là **danh sách con**: giờ mở cửa theo mùa, giá vé theo nhóm khách. Thẻ không hiện được, mà thân bài cũng đã xoá. Khách thấy "Giờ mở cửa:" rồi
không có giờ.

Sửa: chỉ tách khi **mọi dòng** của mục đều đúng dạng và có 2–7 dòng. Không đạt thì giữ nguyên mục trong thân bài. Đo lại cả 207 bài: 28 bài có thẻ, **0 bài mất
dòng**.

Một lỗi khác cùng tinh thần: trang Trợ lý và trang Giới thiệu luôn ghi "trợ lý tra được web, lên được kế hoạch", kể cả khi tính năng đó đang tắt. Sửa: mỗi
dòng đi theo đúng cờ của máy chủ. Trang không được hứa điều nó không làm.

Bài học: **thứ gì rút gọn nội dung thì phải đo trên toàn bộ dữ liệu thật**. Vài bài mẫu không bao giờ lộ ra trường hợp khó.

## Khi nào hỏng

- **Trình duyệt cũ** không có hiệu ứng theo cuộn hay chuyển trang mượt: trang vẫn chạy, chỉ đứng yên.
- **Gói JS đã to hơn mức kế hoạch** (≈ 124,4 KB ở lần đo gần nhất, so với 112 KB lúc đầu). Bảng ghi công nay đã bỏ khỏi trang; thêm trang mới thì nên tách mỗi trang thành gói riêng.
- **Máy tính không có hiệu ứng ảnh lộ dần ở "Huế qua các thời kỳ"**: đã bỏ vì làm cắt số năm (xem trên).
- **Mọi phép đo chạy trên Chromium**, chưa đo Safari.
- **Ảnh lấy từ web** không có giấy phép mở; dùng trong đồ án không thương mại theo quyết định của anh.

## Ba điều chính

1. Chọn **H1 "Sông Hương"** sau khi xem 3 mẫu. Học cách trình bày của TRIPO, không học cách xếp lịch của nó.
2. Hiệu ứng làm bằng **CSS của trình duyệt + khoảng 30 dòng JS**, không thêm thư viện (thư viện sẽ thêm khoảng 39–46 % cỡ JS). Một khoảnh khắc chính là dòng sông vẽ
   dần. Máy bật giảm chuyển động thì không có hiệu ứng nào.
3. Mỗi đợt đều **đo tương phản, độ xô lệch, giảm chuyển động** trên bản thật, hai khổ màn hình. Chuyện thật: thẻ "Thông tin nhanh" làm mất dòng ở 51 / 207 bài,
   chỉ lộ ra khi đo cả 207 bài.

**Bài sau:** Bài 25 — Trợ lý làm việc thật: sửa lịch bằng lời, câu hỏi nhiều ý, chỗ ở trong lịch, ảnh dưới câu trả lời.

---

<details>
<summary>Nguồn (để giữ bài đúng — anh không cần đọc)</summary>

- Nhận xét của anh ("chỉ có văn bản", "đơn giản quá", "ít nhất phải được như Huế TRIPO", "ổn hơn nhưng không có hiệu ứng gì đặc biệt", "đã ổn hơn"): `session_prompt/CURRENT_HANDOFF.md` mục 10:37, 10:42, 11:20, 11:27 ngày 14/11 [tài liệu]
- TRIPO: 5 yếu tố, 3 chuyển động, không học luật xếp lịch: `report_agent/2026-11-12_ra_khoang_cach/b_tripo_v7_giao_dien.md` [đã chạy]
- Ba hướng: `data/ui_mau_2026-11-14/TOKEN_3_HUONG.md` [tài liệu]
- Cỡ thư viện (Motion 51,8; GSAP + ScrollTrigger 44,2): `report_agent/…/c_framework_hieu_ung.md` [đã chạy]; tỉ lệ tính trên gói thật lúc đó 112,08 KB (`e_giao_dien_h1_implementation.md`); 6 trang du lịch, 17 trang khác, FPS (Pudding 60, Vercel 58, Dropbox 57; Linear 31, Apple 44; máy không GPU): `report_agent/…/b_hieu_ung_tham_khao.md` [đã chạy]; "một khoảnh khắc chính": `report_agent/…/c_nghien_cuu_wow.md`
- Hiệu ứng, lớp `html.hieu-ung`, dòng sông (`frontend/src/lkh.css`, `gt.css`), ẩn ≤ 980 / ≤ 760 px, View Transitions (`frontend/src/route.js`): [code]
- Tương phản bản mẫu 1,83–2,71 ⇒ thấp nhất 6,07: `data/ui_mau_2026-11-14/c/BIEN_BAN_GIOI_THIEU.md`; code thật 0 / 12: `report_agent/…/c_review_gd_h1_dot0.md` [đã chạy]; CLS danh sách 0,23 / 0,34: `c_review_gd_h1_dot0.md`, sau sửa ≤ 0,045: commit `d72e7f0` ("CLS 0.23 -> 0.03", "CLS <= 0.045") [đã chạy]; CLS 390 trang chủ 0,148, Lên kế hoạch 0,226 ⇒ ≤ 0,040: `data/ui_mau_2026-11-14/do_cls_390_lan_sua_1411.md` (ghi lại từ tin nhắn đo của C và E) [đã chạy]; Giới thiệu 390 0,17–0,66 ⇒ ≤ 0,03: `session_prompt/sessions/STATUS_C.md`, merge `ef8bc46`, `report_agent/…/e_review_anh_kham_pha.md` (E đo 0,027) [đã chạy]; Chromium: `data/ui_mau_2026-11-14/tools/kiem_tuong_phan.py`, `kiem_hieu_ung.py` [code]
- Ảnh Khám phá 167 / 207, 35 Commons + 132 web, 29 minh hoạ, JS 123,48 KB: merge `ef8bc46`, `report_agent/…/e_review_anh_kham_pha.md` [đã chạy]
- Ảnh chiều 14/11: +13 (hai người chọn độc lập, 7 `kc`) ⇒ 180 / 212, merge `970951c`; 3 bài kho mới ⇒ 183 / 216 (`94aadc9`); chùa Từ Hiếu (hai người chọn khác, `kc`) ⇒ 184 / 216 (`c038167`); 38 dòng `kc` đếm trong `frontend/src/anhBai.js` [đã chạy]
- **Sửa 13:40 14/11/2026 theo kiểm độc lập** (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_22_24.md`): tỉ lệ thư viện tính trên 112 KB (bản trước dùng ~106 KB); 57–60 FPS chỉ là 3 trang nhẹ nhất; tương phản tách bản mẫu ↔ code thật; thêm dòng CLS Giới thiệu; số CLS 390 nay có file nguồn; bảng ghi công đã ra file riêng; thêm phần ảnh Khám phá.
- Gói JS 112,08 ⇒ 122,61 KB, theo từng trang: `report_agent/…/e_giao_dien_h1_implementation.md` [đã chạy]
- Thông tin nhanh 51 / 207, 29 bài bị cắt ⇒ 28 bài có thẻ, 0 mất dòng; trang hứa không theo cờ: `report_agent/…/e_review_gd_h1_dot1_c.md`, `e_review_gd_h1_tro_ly_b.md` [đã chạy]

- Ảnh tối 14/11: lượt chính 184 ⇒ 212 / 224, hiện được 146 ⇒ 162, 19 ảnh chủ đề, người xem lại bác 3 / 19, Serper ≈ 0,095 USD: `report_agent/2026-11-12_ra_khoang_cach/e_anh_v4_implementation.md`, review `c_review_anh_v4.md`; lượt bổ sung 218 / 224, Thuận An bị bác (trẻ em), lịch 33 / 34: `e_anh_v4b_implementation.md`, `c_review_anh_v4b.md`; nâng kc 8 / 37, hiện được 161 ⇒ 169, 10 ảnh "luật nguồn" trả lại: `e_anh_nang_kc_implementation.md`, `c_review_anh_kc.md` [đã chạy]
- Kiểm độc lập phần tối 14/11 (`data/hoc_cung_user_2026-11-10/kiem_doc_lap_bai_24_25_toi_1411.md`): 77 ý — 58 đúng, 6 sai, 10 dễ hiểu nhầm, 3 không kiểm được; đã sửa cả 16 + bỏ ngoặc kép câu dặn không nguyên văn.
</details>
