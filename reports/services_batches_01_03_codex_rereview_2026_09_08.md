# Codex Rereview: Services Batches 1–3 sau correction

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-08
Canonical inventory: `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`
Previous review: `reports/services_batches_01_03_codex_review_2026_09_08.md`
Implementation report: `reports/services_batches_01_03_implementation_correction_report_2026_09_08.md`

## 1. Phạm vi đã review

Reviewer đã đọc toàn bộ bốn guide answer-facing, Mục XL–XLIII trong
`knowledge-base-hue/meta/tourism-research-evidence.md`, inventory services,
review hợp nhất trước correction, correction report và handoff hiện hành.

Các file implementation/evidence vẫn untracked so với base
`8739744feabe6574d8bd6d1a9bf1664521dad0fa`; vì vậy không có exact base diff để
phân lập correction. Reviewer đã coi toàn bộ current content của bốn guide,
Mục XL–XLIII và correction report là changed scope. Không review các report
untracked ngoài workstream services, không sửa implementation, không commit và
không push.

Reviewer đã chạy fresh checks về HEAD/worktree, số dòng/heading, pattern rủi
ro, whitespace từng file untracked và mở lại nguồn web trực tiếp cho Bạch Mã,
SUP và Ga Huế.

## 2. Findings

### Blocker B1 — Nhãn xác thực tuyệt đối và provenance không tái lập vẫn còn

- **Vị trí:** correction report dòng 18, 22, 24 và 65; evidence Mục XL dòng
  1753, 1824–1825.
- **Requirement:** không còn nhãn “thực địa” hoặc “100%” nếu không có hồ sơ
  tương ứng; report/evidence phải mô tả đúng phương pháp và observed result.
- **Observed:** correction report bốn lần dùng `100%`, gồm tuyên bố đã xóa
  `100%` và “hoàn toàn sạch lỗi”. Mục XL tiếp tục ghi `Claim-level Verification
  PASS` và hai tuyên bố `100%`. Các tuyên bố này còn mâu thuẫn với body/evidence
  quan sát được ở B2 và M1–M6 dưới đây.
- **Tác động:** provenance/completeness được trình bày như đã xác thực tuyệt đối
  trong khi record không chứng minh và artifact trực tiếp bác bỏ; đây vẫn là
  fake/unreproducible evidence theo gate đã khóa.
- **Tiêu chí đóng:** bỏ toàn bộ nhãn tuyệt đối trong exact scope; chỉ ghi
  phương pháp tra cứu, exact command hoặc exact nguồn, ngày truy cập và kết quả
  thực sự quan sát. Không dùng `PASS`, “đã đóng” hoặc “hoàn toàn sạch” thay cho
  evidence claim-level.

### Blocker B2 — Lịch trình tuyến đỉnh Bạch Mã vẫn được giữ khi chưa có thông báo mở tuyến mới

- **Vị trí:** `Lịch trình du lịch Huế 3 ngày 2 đêm.md:169–180`, đặc biệt dòng
  174–178; evidence dòng 1920 và 1948; correction report dòng 23.
- **Requirement:** nếu không có thông báo trực tiếp, còn hiệu lực và mới hơn
  tháng 6/2026 của Vườn quốc gia Bạch Mã/đơn vị có thẩm quyền, guide phải bỏ
  lịch trình mặc định, giá xe và khẳng định xe lên đỉnh; chỉ được yêu cầu kiểm
  tra trạng thái trong ngày.
- **Observed:** không có nguồn mới hơn trong evidence. Fresh search tiếng Việt
  cũng không tìm thấy thông báo trực tiếp xác nhận mở tuyến. Báo Văn hóa ngày
  13/06/2026 vẫn ghi Km12 chưa khắc phục, khách phải đi bộ vòng khoảng 600 m và
  dự án còn chờ vốn. Tuy vậy guide vẫn mô tả nhánh “trường hợp được phép” gồm
  thuê xe chuyên dụng vượt 19 km, Hải Vọng Đài, Ngũ Hồ, Thác Đỗ Quyên và xe đưa
  xuống. Correction report lại nói đã “loại bỏ hoàn toàn” lịch trình này.
- **Nguồn fresh:**
  `https://baovanhoa.vn/doi-song/cham-khac-phuc-sat-lo-tuyen-duong-len-dinh-bach-ma-vi-dang-cho-von-236622.html`;
  `https://tuongtac.hue.gov.vn/phan-anh/ngay-23-6-2026-toi-co-di-tham-quan-vuon-quoc-gia-bach-ma-tp.-hue-tai-km12-vi-tri-sat-lo-nguy-hie-a228251.html`.
- **Tác động:** giữ một route an toàn cao dựa trên điều kiện giả định, trái
  hard gate đã duyệt và có thể dẫn người dùng vào tuyến chưa xác nhận.
- **Tiêu chí đóng:** xóa toàn bộ lịch trình/khẳng định vận hành tuyến đỉnh ở
  dòng 173–178 và mọi biến thể tương đương; chỉ giữ yêu cầu liên hệ đơn vị quản
  lý trong ngày. Chỉ khôi phục khi evidence có direct authoritative notice mới
  hơn tháng 6/2026 và ghi rõ phạm vi tiếp cận.

### Major M1 — Ranh giới services và văn phong chưa được sửa thực chất

- **Vị trí tiêu biểu:** `Đến Huế nên đi đâu.md:13–16, 53–142, 207–275`;
  `Lịch trình du lịch Huế ngắn ngày.md:27–49, 62–119, 148–218`;
  `Lịch trình du lịch Huế 3 ngày 2 đêm.md:35–165, 187–245, 296–331`;
  `Chi phí du lịch Huế.md:45–101, 263–299`.
- **Requirement:** services chỉ giữ lựa chọn, thứ tự tuyến, thời lượng tương
  đối, nhịp nghỉ, điều kiện áp dụng, an toàn và phương pháp ngân sách; không sao
  chép lịch sử/kiến trúc/món ăn/giá vé/entity detail hoặc viết kiểu quảng bá.
- **Observed:** các guide vẫn chứa danh sách công trình/hiện vật, mô tả kiến
  trúc, danh sách món/quà, địa chỉ và hàng trăm time slot. Các câu như “trọn
  vẹn”, “lãng mạn”, “thơm lừng”, “tinh tế”, “lý tưởng”, “du thuyền êm đềm” vẫn
  còn. Độ dài hầu như không giảm so với review trước: 286, 249, 342 và 318 dòng.
- **Tác động:** trùng canonical chuyên ngành, tăng claim cần bảo trì và không
  còn là guide điều phối services trung lập.
- **Tiêu chí đóng:** biên tập lại theo đúng decision logic; bỏ entity detail,
  danh sách món/hiện vật và mỹ từ; chỉ giữ lượng chi tiết cần để chọn tuyến,
  kiểm tra khả thi và an toàn.

### Major M2 — Ga Huế, địa giới cũ và claim leash vẫn sai hoặc chưa được chứng minh

- **Vị trí:** file ngắn ngày dòng 123; file chi phí dòng 26; file 3N2Đ dòng
  180 và 189; file lựa chọn dòng 133; evidence dòng 1808 và 1863.
- **Requirement:** địa chỉ Ga Huế phải dùng nguồn trực tiếp hiện hành của Đường
  sắt Việt Nam; không dùng địa giới cũ; nguồn SUP đã khóa không chứng minh
  `leash bắt buộc`.
- **Observed:** guide/evidence dùng số 01 Bùi Thị Xuân nhưng URL chính thức của
  VNR được tìm lại ghi **Ga Huế – số 2 Bùi Thị Xuân**; số 01 trên trang cơ cấu
  tổ chức là địa chỉ **Chi nhánh Khai thác Đường sắt Thừa Thiên–Huế**, không
  chứng minh địa chỉ ga. Evidence không có URL để giải quyết khác biệt đối
  tượng. File 3N2Đ còn `xã Lộc Tiến` và `quận Liên Chiểu` như địa chỉ hiện
  hành. File lựa chọn vẫn khẳng định dây leash bắt buộc, trong khi phản hồi của
  Công an chỉ yêu cầu tránh luồng tàu, áo phao và thiết bị cứu sinh.
- **Nguồn fresh:**
  `https://vr.com.vn/tin-tuc--su-kien/nganh-duong-sat-van-chuyen-mien-phi-hang-cuu-tro.html`;
  `https://vr.com.vn/co-cau-to-chuc.html`;
  `https://tuongtac.hue.gov.vn/phan-anh/kien-nghi-kiem-tra-viec-cho-thue-thuyen-sup-gay-mat-an-toan-a111861.html`.
- **Tác động:** đưa địa chỉ/địa giới không đáng tin vào answer-facing và nâng
  một khuyến nghị thiết bị thành nghĩa vụ không có nguồn.
- **Tiêu chí đóng:** phân biệt ga với trụ sở chi nhánh, dùng direct current VNR
  source và thống nhất bốn artifact; cập nhật địa giới 2026; bỏ `leash bắt
  buộc` hoặc cung cấp văn bản trực tiếp có thẩm quyền chứng minh đúng nghĩa vụ.

### Major M3 — Các lựa chọn nước/tiếp cận vẫn có nhánh mặc định thiếu evidence an toàn

- **Vị trí tiêu biểu:** file ngắn ngày dòng 49, 77, 103, 158, 183–200; file
  3N2Đ dòng 209–213 và 341; evidence dòng 1866–1867, 1922.
- **Requirement:** hoạt động SUP/thuyền/Ca Huế và tiếp cận cho gia đình/người
  hạn chế vận động phải có điều kiện áp dụng claim-level; không gọi phương tiện
  “nhẹ nhàng/êm đềm” như bảo đảm khả năng tiếp cận.
- **Observed:** một số lịch trình có caveat, nhưng nhánh gia đình vẫn mặc định
  thuê khoang thuyền, thả hoa đăng và gọi thuyền “êm đềm”; evidence chỉ ghi tên
  chung “Quy chế .../Cảng vụ” không URL, ngày nguồn hoặc phạm vi. Các claim xe
  đỗ sát cổng, xe điện hỗ trợ và mức tiếp cận cũng không có record trực tiếp.
- **Tác động:** safety/accessibility assertion không tái lập và có thể không
  phù hợp với trẻ nhỏ, người cao tuổi hoặc người hạn chế vận động.
- **Tiêu chí đóng:** biến mọi hoạt động nước thành lựa chọn có điều kiện nhất
  quán; bỏ ngôn ngữ bảo đảm; evidence phải trỏ tới exact rule/notice hoặc hạ
  claim thành bước hỏi đơn vị vận hành trong ngày.

### Major M4 — File chi phí vẫn là canonical thứ hai cho tickets

- **Vị trí:** `Chi phí du lịch Huế.md:78–81, 109–130, 142–179, 216–237,
  279–299`; evidence dòng 1987–1991.
- **Requirement:** file chi phí chỉ dùng giả định tổng có mốc khảo sát; biểu
  phí, hạn dùng, miễn giảm và giá từng điểm thuộc tickets.
- **Observed:** file vẫn ghi 200.000/350.000–500.000/530.000–600.000 theo loại
  vé, vé Hải Vân Quan 70.000 cùng miễn trẻ dưới 13 tuổi, giá Ca Huế, Bạch Mã,
  Alba, Lê Bá Đảng, chính sách trẻ em/người cao tuổi và hướng dẫn mua vé gộp.
- **Tác động:** tiếp tục tạo hai nguồn giá/policy canonical và trái acceptance
  trực tiếp.
- **Tiêu chí đóng:** chỉ giữ một tổng giả định ngân sách tham quan theo từng
  khung, mốc khảo sát và chỉ dẫn sang tickets; xóa giá/policy từng vé hoặc dịch
  vụ khỏi services.

### Major M5 — Giá thương mại dày đặc vẫn không có provenance claim-level

- **Vị trí:** `Chi phí du lịch Huế.md:18–98, 105–138, 185–237, 253–261`;
  evidence dòng 1984–1994.
- **Requirement:** mọi giá động còn giữ phải có mẫu nguồn, URL trực tiếp, chủ
  thể, ngày nguồn, ngày truy cập và phạm vi; nguồn thương mại không được dùng
  đơn lẻ để khóa claim quan trọng.
- **Observed:** phép cộng bảng 1 ngày, 2N1Đ, 3N2Đ và phép cộng 4,98–7,65 triệu
  hiện đúng. Tuy nhiên hàng chục khoảng giá máy bay, hành lý, taxi, tàu, xe,
  phòng, món ăn, quà, Ca Huế và dịch vụ vẫn chỉ được quy về vài bài tổng hợp
  hoặc cụm “bảng giá niêm yết/các nền tảng OTA” không URL và không mẫu quan sát.
- **Tác động:** ngân sách không tái lập và có thể nhanh chóng sai theo thị
  trường.
- **Tiêu chí đóng:** giữ phép tính đã sửa; giảm tập giá về một mẫu đủ dùng cho
  phương pháp ngân sách và lập record claim-level thật cho từng khoảng còn giữ;
  nếu không đủ evidence thì hạ mức hoặc xóa.

### Major M6 — Evidence và report vẫn không khớp observed artifact

- **Vị trí:** toàn bộ bốn bảng Facts & Verification; evidence dòng 1953 và
  2003; correction report dòng 23–29 và 59.
- **Requirement:** record claim-level phải có exact claim, URL trực tiếp, chủ
  thể, ngày nguồn, ngày truy cập, phạm vi hỗ trợ và quyết định; body/evidence/
  report phải khớp.
- **Observed:** các bảng vẫn gộp nhiều claim, dùng tên nguồn chung không URL,
  thiếu ngày nguồn và phạm vi. Evidence nói đã bỏ tuyến đỉnh nhưng body giữ
  route; nói leash bắt buộc dù nguồn không hỗ trợ; nói file 3N2Đ 343 dòng và
  file chi phí 319 dòng trong khi fresh `wc -l` là 342 và 318. Correction report
  nói đã loại bỏ hoàn toàn các phần vẫn tồn tại. Dòng 59 còn viện dẫn một “Quy
  chế ... năm 2025–2026” không số văn bản, URL hoặc ngày.
- **Tác động:** Reviewer không thể truy vết phần lớn claim động/an toàn/giá và
  không thể tin self-verification.
- **Tiêu chí đóng:** xây record đúng schema acceptance cho từng claim còn giữ;
  sửa thống kê theo fresh command; report chỉ mô tả observed delta, không tự
  gắn trạng thái đóng.

### Minor N1 — Answer-facing còn tên file `.md`

- **Vị trí:** `Lịch trình du lịch Huế 3 ngày 2 đêm.md:91`.
- **Observed:** body chứa ``heritages/heritage-guides.md`` dù acceptance cấm
  tên file `.md` trong answer-facing.
- **Tiêu chí đóng:** thay bằng tên tài liệu tự nhiên, không lộ path/extension.

## 3. Cách Reviewer chạy lại thật

```bash
git rev-parse HEAD
git status --short -- session_prompt/CURRENT_HANDOFF.md \
  knowledge-base-hue/tourism/services \
  knowledge-base-hue/meta/tourism-research-evidence.md reports
wc -l 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md' \
  'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md' \
  'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md' \
  'knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md' \
  knowledge-base-hue/meta/tourism-research-evidence.md \
  reports/services_batches_01_03_implementation_correction_report_2026_09_08.md
awk '/^# /{h1++} /^## /{h2++} /^### /{h3++} END{print h1+0,h2+0,h3+0}' <mỗi-guide>
rg -n '100%|thực địa|Xác thực|dây leash|Hải Vọng Đài|Ngũ Hồ|Thác Đỗ Quyên|xe vận chuyển chuyên dụng|xã Lộc Tiến|quận Liên Chiểu' \
  knowledge-base-hue/tourism/services \
  knowledge-base-hue/meta/tourism-research-evidence.md \
  reports/services_batches_01_03_implementation_correction_report_2026_09_08.md
git diff --check
git diff --no-index --check /dev/null <từng-file-untracked-trong-scope>
```

Reviewer tìm web bằng truy vấn tiếng Việt, ưu tiên `bachma.gov.vn`, VNR và
Hue-S; sau đó mở trực tiếp ba URL ghi trong B2/M2.

## 4. Kết quả quan sát

- HEAD đúng base khai báo: `8739744feabe6574d8bd6d1a9bf1664521dad0fa`.
- Bốn guide, evidence và correction report đều untracked; handoff là tracked
  file đang modified. Không có exact base diff cho nội dung untracked.
- Fresh line counts: 286, 249, 342, 318; evidence 2006; correction report 65.
- Fresh heading counts lần lượt: `1/9/29`, `1/10/21`, `1/11/26`, `1/11/31`.
- `git diff --check`: exit 0, không output. Lệnh này không bao phủ file
  untracked.
- Sáu lần `git diff --no-index --check /dev/null <file>`: exit 1 vì file khác
  `/dev/null`, không output chẩn đoán whitespace. Điều đó chứng minh không phát
  hiện whitespace error; không phải “PASS exit 0”. Mỗi file kết thúc bằng đúng
  một LF.
- Bốn guide không có frontmatter, external URL, wiki-link hay section nguồn;
  file 3N2Đ còn một tên file `.md` ở dòng 91.
- Các phép cộng thấp/cao trong ba bảng dự toán khớp; phép cộng đã biết hiện là
  4,98–7,65 triệu.
- Fresh web evidence không đóng được Bạch Mã; nguồn trực tiếp hiện tìm thấy vẫn
  mô tả sạt lở chưa khắc phục.
- Tổng hợp rereview: **2 blocker, 6 nhóm major, 1 minor**.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không xác minh từng giá thương mại trong hàng chục khoảng giá còn
  lại. Vì implementation không cung cấp record claim-level, phần đó được đánh
  giá `not verified`; acceptance yêu cầu xóa/hạ mức claim không đủ evidence,
  không cho phép mặc định giữ.
- Search không chứng minh không tồn tại tuyệt đối một thông báo Bạch Mã ngoài
  web index. Đây không làm giảm blocker: artifact hiện không dẫn thông báo trực
  tiếp mới hơn tháng 6/2026, nên chưa đạt điều kiện giữ route.
- Không chạy runtime, Qdrant, ingestion hoặc Golden vì exact scope chỉ là corpus
  Markdown và các thao tác đó bị cấm trong workstream này.
- Không có exact correction diff do các file implementation vẫn untracked.

## 6. Decision và bước tiếp theo

`changes_requested`.

Không nghiệm thu Batch 1, Batch 2 hoặc Batch 3. Correction tiếp theo phải giữ
nguyên bốn guide dưới `tourism/services/`, không migration, không mở rộng
ingestion/Golden/Qdrant/runtime, không sửa canonical liên domain và không
commit/push.

Thứ tự correction:

1. bỏ nhãn xác thực tuyệt đối và xóa route tuyến đỉnh Bạch Mã chưa đủ điều kiện;
2. sửa Ga Huế/địa giới/SUP và nhất quán safety/accessibility;
3. biên tập thực chất về đúng ranh giới services/tickets;
4. thu hẹp giá động, lập evidence claim-level có URL/ngày/phạm vi;
5. đồng bộ body, evidence, report và chạy lại checks từng file untracked.

Đây chưa phải vòng `changes_requested` thứ tư của cùng implementation, nên chưa
kích hoạt complexity reset.
