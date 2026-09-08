# Codex Review: Services Batch 1 hiệu chỉnh, Batch 2 và Batch 3

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-08
Canonical inventory: `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`
Implementation reports: `reports/services_batch_01_implementation_correction_report_2026_09_08.md`, `reports/services_batch_02_implementation_report_2026_09_08.md`, `reports/services_batch_03_implementation_report_2026_09_08.md`

## 1. Phạm vi đã review

Reviewer đã đọc toàn bộ bốn file answer-facing sau:

- `knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md`;
- `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md`;
- `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md`;
- `knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md`.

Reviewer cũng đọc lại Mục XL–XLIII của
`knowledge-base-hue/meta/tourism-research-evidence.md`, ba implementation
report, inventory của nhánh services, các guide/template liên domain được dẫn
chiếu và trạng thái bàn giao. Các claim pháp lý, địa giới, an toàn và dữ liệu
động có rủi ro đã được tìm kiếm bằng truy vấn tiếng Việt và đối chiếu với nguồn
chính thức hoặc nguồn hiện hành tính đến ngày review.

Phần ngoài bốn guide, bốn mục evidence và ba implementation report không thuộc
phạm vi quyết định này. Reviewer không sửa implementation, không commit và
không push.

### Kết quả tái thẩm định findings Batch 1 vòng trước

| Finding cũ | Kết quả tái thẩm định |
| :--- | :--- |
| B1 — quyền dùng sub-agent | **Đã đóng có điều kiện.** User đã xác nhận quyền dùng sub-agent cho lượt triển khai trước; lượt correction Batch 1 được Implementer khai báo tự rà soát trực tiếp. |
| M1 — bài dạng toplist, lấn canonical | **Chưa đóng.** File chỉ giảm từ 289 xuống 286 dòng và vẫn còn các vùng mô tả lịch sử, kiến trúc, món ăn và entity dài tại dòng 13–16, 55–109, 120–142, 211–252 và 258–274. |
| M2 — factual/admin/domain errors | **Đóng một phần.** Hà Cảng, Rú Chá/Mắt biếc, tên bảo tàng, Ca Huế/Nhã nhạc trong Batch 1 và cơ quan ban hành Nghị quyết 55 đã được sửa; ngày ban hành/hiệu lực Nghị quyết 55 và provenance Quyết định 83 vẫn sai. |
| M3 — claim động, an toàn, tiếp cận | **Chưa đóng.** Claim SUP, miễn phí, Bạch Mã, khả năng tiếp cận, đỗ xe và vận hành tuyến vẫn chưa có nguồn trực tiếp đủ mạnh. |
| M4 — evidence claim-level | **Chưa đóng.** Mục XL vẫn dùng bảng tổng hợp mơ hồ, không ánh xạ đầy đủ claim sang URL/ngày/phạm vi kiểm chứng. |
| N1 — văn phong | **Chưa đóng.** Bài vẫn mang giọng giới thiệu/quảng bá và chứa nhiều chi tiết không cần thiết cho quyết định chọn điểm. |

## 2. Findings

### Blocker B1 — Ghi nhận “đối chiếu thực địa” không có hồ sơ khảo sát

- **Vị trí:** `Chi phí du lịch Huế.md:319`; evidence Mục XLI dòng
  1860–1861, Mục XLII dòng 1918, 1920–1921 và Mục XLIII; các kết luận
  “Xác thực 100%”.
- **Observed:** tài liệu nói dữ liệu đã được “đối chiếu thực địa vào tháng
  09/2026”, nhưng không có người khảo sát, ngày/giờ, tuyến khảo sát, phương pháp,
  ảnh, biên bản hoặc record quan sát. Batch 1 từng được yêu cầu loại nhãn này,
  nhưng nhãn tương đương xuất hiện lại trong Batch 2–3.
- **Tác động:** tạo provenance không thể tái lập cho dữ liệu nhạy về giá, vận
  hành và an toàn; theo chuẩn dự án, evidence/provenance giả hoặc không chứng
  minh được là blocker.
- **Tiêu chí đóng:** xóa mọi tuyên bố “thực địa”/“100%” không có hồ sơ thật;
  thay bằng đúng phương pháp đã dùng (tra cứu web, đối chiếu văn bản, ngày truy
  cập). Nếu thực sự có khảo sát, phải nộp record tối thiểu gồm người, ngày, địa
  điểm, phương pháp và phạm vi claim.

### Blocker B2 — Lịch trình Bạch Mã bỏ qua tình trạng sạt lở Km12 năm 2026

- **Vị trí:** `Lịch trình du lịch Huế 3 ngày 2 đêm.md:173–179,281,312`;
  `Đến Huế nên đi đâu.md:49,98,272`; `Chi phí du lịch Huế.md:259`; evidence
  dòng 1919.
- **Observed:** các file khẳng định xe chuyên dụng có thể chạy lên đỉnh và đề
  xuất Hải Vọng Đài–Ngũ Hồ–Thác Đỗ Quyên như tuyến hoạt động bình thường.
  Trong khi đó, Báo Văn hóa tháng 6/2026 ghi điểm sạt lở Km12 chưa được khắc
  phục do chờ vốn; Huế-S ngày 23/06/2026 tiếp tục ghi nhận vị trí nguy hiểm.
- **Nguồn:**
  https://baovanhoa.vn/doi-song/cham-khac-phuc-sat-lo-tuyen-duong-len-dinh-bach-ma-vi-dang-cho-von-236622.html;
  https://tuongtac.hue.gov.vn/phan-anh/ngay-23-6-2026-toi-co-di-tham-quan-vuon-quoc-gia-bach-ma-tp.-hue-tai-km12-vi-tri-sat-lo-nguy-hie-a228251.html.
- **Tác động:** hướng người dùng vào một tuyến có trạng thái tiếp cận chưa được
  xác nhận và rủi ro an toàn thực tế.
- **Tiêu chí đóng:** chỉ khôi phục lịch trình cụ thể nếu có thông báo trực tiếp,
  còn hiệu lực của Vườn quốc gia Bạch Mã sau tháng 6/2026 xác nhận tuyến đã mở
  và nêu rõ phạm vi tiếp cận. Nếu chưa có nguồn đó, bỏ lịch trình mặc định, giá
  xe và khẳng định xe lên đỉnh; ghi rõ người dùng phải kiểm tra trạng thái trong
  ngày với đơn vị quản lý.

### Major M1 — Cả ba batch vẫn vượt ranh giới của services và dùng giọng quảng bá

- **Vị trí tiêu biểu:** Batch 1 dòng 13–16, 55–109, 120–142, 211–252,
  258–274; file ngắn ngày dòng 27–31, 45–49, 64–78, 92–116; file 3 ngày 2
  đêm dòng 45–80, 92–118, 128–188, 233–242, 299–327.
- **Observed:** các guide vẫn sao chép mô tả lịch sử/kiến trúc, danh sách món,
  địa chỉ, hiện vật và entity detail thay vì tập trung vào logic lựa chọn/lịch
  trình. Batch 2 còn nhiều từ như “kiệt tác”, “đỉnh cao”, “lộng lẫy”, “hoàn
  mỹ”, “độc nhất vô nhị”, “kỳ quan”, “ngoạn mục”. Điều này trái trực tiếp với
  implementation report nói đã loại mỹ từ.
- **Tác động:** trùng canonical corpus, làm chunk dài, giảm tính trung lập và
  tăng chi phí bảo trì factual claims.
- **Tiêu chí đóng:** rút guide về thứ tự tuyến, vị trí tương đối, thời lượng,
  nhịp nghỉ, điều kiện áp dụng, khả năng tiếp cận và bước tra cứu domain chuyên
  trách; loại mô tả entity dài, danh sách món/hiện vật và ngôn ngữ quảng bá.

### Major M2 — Còn lỗi địa giới, tên tổ chức và phân loại văn hóa

- **Vị trí và correction bắt buộc:**
  - `Lịch trình du lịch Huế ngắn ngày.md:131` và evidence dòng 1863: bỏ “thị
    xã Hương Thủy”; dùng `phường Phú Bài, thành phố Huế` theo Nghị quyết
    1675/NQ-UBTVQH15.
  - `Lịch trình du lịch Huế 3 ngày 2 đêm.md:50`: không gộp Nhã nhạc vào chương
    trình Ca Huế trên thuyền khi không có chương trình cụ thể chứng minh.
  - Cùng file dòng 220: “hò câu quan họ” tại Thanh Toàn là sai; Quan họ thuộc
    không gian văn hóa Bắc Ninh–Bắc Giang, còn bài chòi dùng câu hô/câu hò.
  - Dòng 235: địa chỉ hai không gian mỹ thuật phải được sửa theo nguồn hiện
    hành: Trung tâm Nghệ thuật Lê Bá Đảng tại 15 Lê Lợi và Điềm Phùng Thị tại
    17 Lê Lợi, không phải “17 và 97 Lê Lợi”.
  - Dòng 236 và 334: thay tên cũ bằng `Bảo tàng Lịch sử thành phố Huế` và `Đài
    Khí tượng Thủy văn thành phố Huế`.
  - `Chi phí du lịch Huế.md:36`: Bến xe phía Nam thuộc phường An Cựu, Bến xe
    phía Bắc thuộc phường Hương An; dòng 323 phải dùng “Ngày giải phóng thành
    phố Huế”, không dùng tên đơn vị cũ.
  - Evidence Batch 1 dòng 1773 không được dẫn Quyết định 83/2025/QĐ-UBND như
    văn bản quy định địa bàn hành chính; văn bản này sửa quy định hạn mức giao
    đất ở/công nhận đất ở. Dòng 1774 và correction report phải sửa Nghị quyết
    55: ban hành ngày 25/12/2025, hiệu lực 04/01/2026.
- **Nguồn:** Nghị quyết 1675:
  https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-quyet-so-1675-nq-ubtvqh15-sap-xep-cac-dvhc-cap-xa-cua-thanh-pho-hue-nam-2025-119250616195617897.htm;
  kế hoạch bến xe 2026:
  https://hue.gov.vn/Portals/0/Uploads/VBPL/Nam2026/Thang3/00.00.H57-155-KH-UBND-2026-PL1_signed.pdf;
  Nghị quyết 55:
  https://hue.gov.vn/Portals/0/Uploads/VBPL/Nam2026/Thang1/000.00.00.K57-55-2025-NQ-HDND-2025-PL1.pdf;
  Quyết định 83:
  https://vbpl.vn/thuathienhue/Pages/vbpq-toanvan.aspx?ItemID=182326&Keyword=.
- **Tiêu chí đóng:** sửa từng claim ở answer-facing, evidence và report; mỗi
  claim cần URL trực tiếp cùng ngày kiểm tra và phạm vi nguồn.

### Major M3 — Lịch trình có tuyến thiếu khả thi hoặc thiếu điều kiện an toàn

- `Lịch trình du lịch Huế 3 ngày 2 đêm.md:63–65` dành 105 phút để đi từ Thủy
  Xuân tới Đầm Chuồn, lên thuyền, ngắm hoàng hôn và ăn tại chòi; cự ly nêu ra
  không có nguồn trực tiếp. Dòng 281 ghép Bạch Mã buổi sáng với Lăng Cô–Lập An
  buổi chiều, trái `tourism_guides.md:58` và chính evidence dòng 1939.
- `Lịch trình du lịch Huế ngắn ngày.md:131` đưa SUP 16:30–18:00 nhưng thiếu
  điều kiện đơn vị hợp pháp, áo phao/thiết bị cứu sinh và tránh luồng tàu.
  Nguồn chính quyền yêu cầu rõ các điều kiện này:
  https://tuongtac.hue.gov.vn/phan-anh/kien-nghi-kiem-tra-viec-cho-thue-thuyen-sup-gay-mat-an-toan-a111861.html.
- File ngắn ngày dòng 158 đưa Ca Huế trên thuyền vào phương án ngày mưa dầm;
  điều kiện chỉ được phép là bến và đơn vị vận hành xác nhận xuất bến an toàn
  trong ngày. Các dòng 188, 206 và file 3 ngày 2 đêm dòng 208–211 gọi thuyền
  “êm ái”/phù hợp gia đình mà bỏ qua bước lên xuống và áo phao.
- File ngắn ngày dòng 191 gọi Hồ Thủy Tiên là công viên “bỏ hoang”, không phản
  ánh trạng thái quản lý/chỉnh trang/quy hoạch năm 2026.
- **Tiêu chí đóng:** tính lại các tuyến từ đúng điểm xuất phát, có thời gian
  đệm và thời gian quay về; mọi hoạt động nước hoặc vận hành theo ngày phải là
  lựa chọn có điều kiện; không ghép tuyến mâu thuẫn với canonical guide.

### Major M4 — File chi phí vi phạm ranh giới với nhánh tickets

- **Vị trí:** `Chi phí du lịch Huế.md:78–83,113,122,147–148,161,176,218,
  230,236,238,285–290`.
- **Observed:** bài sao chép giá từng vé, combo, hạn dùng và chính sách miễn
  giảm dù inventory yêu cầu chỉ dùng giá như đầu vào ước tính và điều phối sang
  tickets. Phần 285–290 thực chất là bảng so sánh vé chi tiết.
- **Tác động:** tạo hai nguồn giá canonical, dễ lệch khi nghị quyết hoặc đơn vị
  vận hành thay đổi.
- **Tiêu chí đóng:** trong guide chi phí chỉ giữ giả định tổng ngân sách và mốc
  khảo sát; bỏ chi tiết giá/policy từng vé. Nhánh tickets là nơi duy nhất quản
  lý biểu phí và điều kiện miễn giảm.

### Major M5 — Dự toán có phép cộng sai và nhiều giá động không đủ nguồn

- **Sai số học:** dòng 180 cho khung Tiêu chuẩn 3N2Đ là 2,98–4,15 triệu; cộng
  vé máy bay 2–3,5 triệu phải thành **4,98–7,65 triệu**, không phải 3,7–5,8
  triệu như dòng 182. Dòng 20 lại dùng khoảng vé máy bay khác, 1,8–3,8 triệu.
- **Sai giá:** dòng 82 ghi Không gian lưu niệm Lê Bá Đảng khoảng 150.000 đồng
  như giá chung, trong khi trang trực tiếp niêm yết giá khách phổ thông 200.000
  đồng; 150.000 đồng là mức đoàn từ 30 người:
  https://lebadangmemoryspace.com/language/vi/khong-gian-luu-niem-le-ba-dang/.
- **Nguồn không đủ:** giá Ca Huế ở dòng 230/238 là giá nhà cung cấp, không phải
  mức nhà nước thống nhất; quy chế yêu cầu tổ chức/cá nhân niêm yết giá đã kê
  khai. Các claim tăng giá 15–50%, phụ thu 150.000–400.000, tiết kiệm 20–50%
  và hàng loạt giá xe/phòng/ăn chỉ có nguồn tổng hợp hoặc không có URL cấp
  claim.
- **Tiêu chí đóng:** tính lại toàn bộ bảng từ một bộ giả định nhất quán; kiểm
  tra từng tổng thấp/cao; chỉ giữ khoảng giá động có mẫu nguồn, ngày truy cập và
  mô tả phạm vi; phân biệt giá nhà nước với giá nhà cung cấp; bỏ mọi phần trăm
  tuyệt đối không tái lập được.

### Major M6 — Evidence và implementation report không phản ánh observed result

- Mục XL–XLIII chỉ có vài hàng Facts & Verification cho hàng trăm claim động,
  an toàn, khoảng cách và giá; nhiều hàng không có URL trực tiếp, ngày, chủ thể
  hoặc phạm vi.
- Thống kê sai: Mục XLI ghi file ngắn ngày có 10 H3 thay vì 21; Mục XLII ghi
  349 dòng/10 H2/28 H3 thay vì 338/11/26; Mục XLIII ghi
  326 dòng/8 H2/23 H3 thay vì 325/11/31.
- Implementation report nói không khóa giờ chi tiết/số hiệu tàu nhưng file ngắn
  ngày có lịch từng 15 phút và các số HĐ1/HĐ2/HĐ3/HĐ4; nói đã tách Ca Huế/Nhã
  nhạc và khóa an toàn SUP nhưng body vẫn trái các tuyên bố đó.
- Mục XL dòng 1770–1777 và 1802–1813 chưa ánh xạ nguồn trực tiếp; correction
  report Batch 1 ghi evidence 1.994 dòng trong khi file thực tế 1.993 dòng.
- `Chi phí du lịch Huế.md:26` dùng số nhà Ga Huế khác file ngắn ngày/evidence;
  cần xác nhận bằng nguồn trực tiếp hiện hành của Đường sắt Việt Nam và thống
  nhất, không suy ra từ blog cũ.
- **Tiêu chí đóng:** lập bảng claim-level cho mọi claim còn giữ, gồm claim,
  nguồn trực tiếp, cơ quan/chủ thể, ngày nguồn, ngày truy cập, mức hỗ trợ và
  quyết định giữ/hạ mức/xóa; sửa report và self-check theo kết quả đo thật; cấm
  dùng “100%” như thay thế cho evidence.

### Minor N1 — Kiểm tra Git chưa bao phủ file mới và có lỗi EOF

- Bốn guide, evidence và report đang untracked; `git diff --check` không kiểm
  tra nội dung untracked nên kết luận “PASS toàn repo” của handoff không đủ.
- `Chi phí du lịch Huế.md` có một dòng trắng thừa ở cuối file theo
  `git diff --no-index --check`.
- **Tiêu chí đóng:** chạy `git diff --no-index --check /dev/null <file>` cho
  từng file untracked và sửa EOF; báo đúng giới hạn của từng lệnh.

## 3. Cách Reviewer chạy lại thật

```bash
git status --short -- session_prompt/CURRENT_HANDOFF.md \
  knowledge-base-hue/tourism/services \
  knowledge-base-hue/meta/tourism-research-evidence.md reports
git rev-parse HEAD
wc -l knowledge-base-hue/tourism/services/*.md \
  knowledge-base-hue/meta/tourism-research-evidence.md
rg -n '^#{1,3} ' knowledge-base-hue/tourism/services/*.md
rg -n 'thực địa|Xác thực 100%|Thừa Thiên Huế|thị xã Hương Thủy|Nhã nhạc|quan họ|Bạch Mã|Km12|2 cầu' \
  knowledge-base-hue/tourism/services \
  knowledge-base-hue/meta/tourism-research-evidence.md reports/services_batch_*.md
git diff --check
git diff --no-index --check /dev/null \
  'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md'
git diff --no-index --check /dev/null \
  'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md'
git diff --no-index --check /dev/null \
  'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md'
git diff --no-index --check /dev/null \
  'knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md'
```

Reviewer đã tìm kiếm web bằng tiếng Việt và mở nguồn trực tiếp/chính thức cho
Nghị quyết 55, Nghị quyết 05, Nghị quyết 1675, bến xe, SUP, Ca Huế, bảo tàng,
Hồ Thủy Tiên, Không gian lưu niệm Lê Bá Đảng và trạng thái Bạch Mã. Ba lượt
review độc lập theo batch được dùng để đối chiếu chéo; Reviewer chính kiểm tra
lại các finding được đưa vào quyết định này.

## 4. Kết quả quan sát

- Số dòng/heading thực tế:
  - `Đến Huế nên đi đâu.md`: 286 dòng, 1 H1, 9 H2, 29 H3.
  - `Lịch trình du lịch Huế ngắn ngày.md`: 249 dòng, 1 H1, 10 H2, 21 H3.
  - `Lịch trình du lịch Huế 3 ngày 2 đêm.md`: 338 dòng, 1 H1, 11 H2, 26 H3.
  - `Chi phí du lịch Huế.md`: 325 dòng, 1 H1, 11 H2, 31 H3.
- Bốn file không có YAML frontmatter, URL ngoài, wiki-link hoặc tên file `.md`
  trong answer-facing body.
- Heading và coverage có mặt về hình thức, nhưng không chứng minh correctness.
- Verdict theo batch: Batch 1 **chưa đóng correction**, Batch 2
  **changes_requested**, Batch 3 **changes_requested**.
- Tổng hợp: 2 blocker, 6 major group và 1 minor group.

## 5. Giới hạn hoặc phần chưa chạy

- Các file trong scope đang untracked, nên không có exact diff từ base commit;
  Reviewer coi toàn bộ file và Mục XL–XLIII là changed scope.
- Không có phép thử runtime vì đây là corpus Markdown. Review dựa trên cấu trúc,
  tính toán, đối chiếu nội bộ và xác minh nguồn web.
- Reviewer không xác minh từng giá thương mại trong hàng trăm giá hiện có. Đây
  không phải lý do cho phép giữ chúng: mọi giá còn lại sau correction phải có
  evidence claim-level và mốc khảo sát tái lập được.
- Nguồn tháng 6/2026 chứng minh rủi ro Bạch Mã chưa được xử lý tại thời điểm đó;
  Implementer phải tìm thông báo trực tiếp mới hơn trước khi khẳng định trạng
  thái tháng 9/2026.

## 6. Decision và bước tiếp theo

`changes_requested`.

Không nghiệm thu Batch 1, Batch 2 hoặc Batch 3 ở trạng thái hiện tại.
Implementer thực hiện một correction batch tập trung cho đúng bốn guide, Mục
XL–XLIII và ba implementation/correction report liên quan. Không mở rộng sang
corpus khác, không thực hiện migration `tourism/` sang `travel/`, không sửa
inventory/canonical chuyên ngành và không commit/push.

Thứ tự correction bắt buộc:

1. đóng provenance blocker và Bạch Mã safety blocker;
2. sửa factual/admin/cultural claims và tính lại toàn bộ ngân sách;
3. rút nội dung về đúng ranh giới services;
4. xây lại evidence claim-level và đồng bộ report/self-check;
5. chạy lại kiểm tra cơ học cho từng file untracked rồi bàn giao `rereview`.
