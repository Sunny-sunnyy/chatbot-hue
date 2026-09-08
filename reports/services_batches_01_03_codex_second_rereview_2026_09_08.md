# Codex Second Rereview: Services Batches 1–3

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-08
Canonical inventory: `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`
Previous rereview: `reports/services_batches_01_03_codex_rereview_2026_09_08.md`
Implementation report: `reports/services_batches_01_03_implementation_correction_report_2026_09_08.md`

## 1. Phạm vi đã review

Reviewer đã đọc toàn bộ bốn guide answer-facing, toàn bộ Mục XL–XLIII trong
`knowledge-base-hue/meta/tourism-research-evidence.md`, inventory services,
review/rereview trước, implementation correction report và handoff hiện hành.

Các guide, evidence và report vẫn untracked so với base
`8739744feabe6574d8bd6d1a9bf1664521dad0fa`; do đó không có exact base diff để
phân lập correction. Reviewer đã review toàn bộ current content trong exact
scope. Không sửa implementation/evidence, không review nội dung dirty/untracked
ngoài scope, không commit và không push.

Reviewer chạy fresh mechanical checks và websearch tiếng Việt đến ngày
08/09/2026 cho Bạch Mã, SUP, Ga Huế, địa giới Hải Vân và giá Ca Huế.

## 2. Findings

### Blocker B2 — Vẫn giữ lịch trình Bạch Mã mặc định khi chưa có thông báo mở tuyến mới

- **Vị trí:** `Lịch trình du lịch Huế 3 ngày 2 đêm.md:168–175`, đặc biệt dòng
  171–174; evidence dòng 1922 và 1945–1946; implementation report dòng 24–29.
- **Requirement:** khi chưa có thông báo trực tiếp, còn hiệu lực và mới hơn
  tháng 6/2026 của Vườn quốc gia Bạch Mã/đơn vị có thẩm quyền, guide phải bỏ
  lịch trình mặc định và chỉ yêu cầu kiểm tra trạng thái trong ngày.
- **Observed:** fresh search không tìm thấy thông báo mở tuyến mới. Báo Văn hóa
  ngày 13/06/2026 vẫn ghi Km12 chưa khắc phục và dự án chờ vốn. Guide đã bỏ các
  điểm trên đỉnh, nhưng vẫn dành nguyên “Ngày 2” cho Bạch Mã, khẳng định Đường
  mòn Trĩ Sao và “Vườn thực vật Bạch Mã” là tuyến tầm thấp/chân núi để tham
  quan. Evidence không có thông báo vận hành hiện hành cho hai lựa chọn này.
  Quyết định 942/QĐ-BNN-LN chỉ là đề án du lịch sinh thái; trong đó tuyến tới
  Trĩ Sao đi qua Km8, không chứng minh tuyến đang mở hoặc an toàn tháng 09/2026.
- **Nguồn fresh:**
  `https://baovanhoa.vn/doi-song/cham-khac-phuc-sat-lo-tuyen-duong-len-dinh-bach-ma-vi-dang-cho-von-236622.html`;
  `https://hue.gov.vn/Portals/0/Uploads/00.00.H57/Nam2025/Thang4/942_QD_BNN_LN_QDinh-De_an_DLST_BachMa_final.pdf`.
- **Tác động:** biến yêu cầu “kiểm tra trong ngày” thành một route thay thế được
  trình bày như đang khả dụng, vượt hard safety gate đã khóa.
- **Tiêu chí đóng:** bỏ lịch trình Ngày 2 mặc định và mọi khẳng định tuyến chân
  núi đang tham quan được; chỉ giữ bước liên hệ Ban quản lý trong ngày. Chỉ nêu
  route cụ thể khi có direct current notice xác nhận phạm vi tiếp cận.

### Major M1 — Ranh giới services và văn phong vẫn chưa được biên tập thực chất

- **Vị trí tiêu biểu:** `Đến Huế nên đi đâu.md:13–16, 53–145, 207–275`;
  `Lịch trình du lịch Huế ngắn ngày.md:147–168`;
  `Lịch trình du lịch Huế 3 ngày 2 đêm.md:69–153, 224–237`.
- **Requirement:** services giữ decision logic, thứ tự tuyến, thời lượng tương
  đối, nhịp nghỉ, điều kiện và an toàn; không lặp mô tả dài về kiến trúc, hiện
  vật, món ăn hoặc biến file lựa chọn thành toplist.
- **Observed:** file lựa chọn vẫn là toplist 286 dòng với mô tả từng entity;
  các itinerary vẫn liệt kê chi tiết công trình, hiện vật và thực đơn. Ví dụ
  file ngắn ngày dòng 153–155 mô tả nhà rường gỗ lim, cổ vật ngự dụng, tranh
  tường/nội thất và trà hoa cúc; file 3N2Đ dòng 145–152 tiếp tục liệt kê tác
  phẩm và món/quà. Nhiều slot giờ cứng vẫn còn dù report dòng 34 nói đã chuyển
  sang khung buổi linh hoạt.
- **Tác động:** trùng canonical `heritages`, `foods`, `performing_arts` và tăng
  số claim động/factual phải bảo trì.
- **Tiêu chí đóng:** biên tập lại theo decision logic bắt buộc của inventory;
  chỉ giữ chi tiết cần để chọn/gom tuyến và đánh giá khả thi, bỏ mô tả entity,
  danh sách món/hiện vật và time slot cứng không cần thiết.

### Major M2 — Provenance SUP sai ngày và nâng claim vượt nguồn

- **Vị trí:** file lựa chọn dòng 133; file ngắn ngày dòng 157; file 3N2Đ phần
  SUP; evidence dòng 1775, 1808, 1866 và 1925; report dòng 42.
- **Requirement:** claim an toàn phải có exact source, đúng ngày và đúng phạm
  vi; không nâng phản ánh của người dân thành quy định của cơ quan chức năng.
- **Observed:** trang Hue-S có ngày gửi 28/06/2023 và ngày xử lý 13/09/2023,
  không phải 18/06/2024. Phản hồi chính thức yêu cầu tránh luồng tàu, áo phao và
  thiết bị cứu sinh; đồng thời nói SUP không thuộc danh mục đăng ký/đăng kiểm và
  khó quản lý. Guide/report lại yêu cầu đơn vị “được cấp phép”, “có đăng ký”,
  hướng dẫn viên hoặc đi theo đoàn. Các ý này chỉ xuất hiện trong lời phản ánh,
  không phải kết quả xử lý của Công an.
- **Nguồn fresh:**
  `https://tuongtac.hue.gov.vn/phan-anh/kien-nghi-kiem-tra-viec-cho-thue-thuyen-sup-gay-mat-an-toan-a111861.html`.
- **Tác động:** evidence sai provenance và biến khuyến nghị chưa được chứng minh
  thành nghĩa vụ an toàn.
- **Tiêu chí đóng:** sửa đúng ngày nguồn; chỉ giữ ba yêu cầu được phản hồi chính
  thức hỗ trợ, hoặc bổ sung văn bản trực tiếp khác cho license/đoàn/hướng dẫn
  viên.

### Major M3 — Claim tiếp cận và vận hành đường thủy vẫn không truy vết được

- **Vị trí:** file ngắn ngày dòng 177–200; file 3N2Đ dòng 189–212; evidence
  dòng 1867 và các bảng Facts XL–XLII.
- **Requirement:** với trẻ nhỏ/người cao tuổi/người hạn chế vận động, không được
  bảo đảm khả năng tiếp cận nếu chưa có record trực tiếp; điều kiện Ca Huế/thuyền
  phải có exact rule/notice hoặc được hạ thành bước hỏi đơn vị vận hành.
- **Observed:** body vẫn khẳng định xe đỗ sát cổng, nền/bậc thoải, ô tô đỗ tận
  cổng, xe điện chở qua các cung viện và công viên gỗ lim “an toàn, không có xe
  cơ giới”. Evidence không có record URL trực tiếp cho các claim này. Record Ca
  Huế chỉ ghi chung “Quy chế quản lý bến thuyền Tòa Khâm và Cảng vụ đường thủy”,
  không số văn bản, URL hay ngày nguồn cụ thể.
- **Tác động:** người dùng có nhu cầu tiếp cận đặc thù có thể lập lịch dựa trên
  điều kiện hạ tầng chưa được xác nhận.
- **Tiêu chí đóng:** hạ các claim thành yêu cầu hỏi đơn vị vận hành/kiểm tra tại
  chỗ, hoặc thêm exact direct evidence cho từng điều kiện tiếp cận còn giữ; bổ
  sung URL và ngày cho quy định đường thủy/Ca Huế.

### Major M5 — Tập giá chưa thu hẹp, provenance thiếu và còn lỗi phép cộng

- **Vị trí:** `Chi phí du lịch Huế.md:19–94, 107–129, 139–179, 185–257`;
  evidence dòng 1969–1993; report dòng 52–55.
- **Requirement:** giá thương mại chỉ là mẫu quan sát có ngày, nguồn trực tiếp
  và phạm vi; mọi phép cộng thấp/cao phải đúng.
- **Observed:** body có 101 dòng khớp pattern giá, gồm hàng chục dải giá hành
  lý, taxi, tàu, xe, lưu trú, món ăn, quà, xe điện, Ca Huế và hướng dẫn viên.
  Bảng XLIII chỉ có vài record tổng hợp; các mục “khảo sát OTA”, “khảo sát niêm
  yết bến thuyền” không có URL. Dòng 147 còn tính sai cận trên khung tiết kiệm
  một ngày: `100.000 + 150.000 + 150.000 + 200.000 + 50.000 + 50.000 =
  700.000`, không phải `550.000`. Phép cộng 3N2Đ tiêu chuẩn 4,98–7,65 triệu đã
  đúng.
- **Tác động:** budget không tái lập và có tổng sai trực tiếp.
- **Tiêu chí đóng:** thu hẹp thật sự về mẫu đủ dùng; mỗi khoảng còn giữ có
  direct URL/chủ thể/ngày/phạm vi; sửa cận trên một ngày và chạy lại toàn bộ
  phép cộng.

### Major M6 — Evidence/report chưa khớp current body

- **Vị trí:** bốn bảng Facts XL–XLIII và implementation report dòng 19–59.
- **Requirement:** schema không chỉ đủ bảy cột mà từng record phải có exact URL,
  ngày nguồn và phạm vi; body/evidence/report phải mô tả cùng một observed state.
- **Observed:** nhiều ô “Nguồn URL” vẫn là tên văn bản/file nội bộ/nguồn chung
  không URL (`Nghị quyết...`, `Cảnh báo Ban chỉ huy...`, `Quy chuẩn cự ly...`,
  `Khảo sát OTA`, `Quy chế...`). Evidence/report nói đã bỏ mô tả chi tiết, time
  slot cứng, route Bạch Mã mặc định và đã thu hẹp tập giá, nhưng body trực tiếp
  bác bỏ các tuyên bố này. XLIII nói khoảng ngân sách tham quan 200.000–600.000,
  trong khi body dòng 78 và các bảng dùng 150.000–750.000.
- **Tác động:** Reviewer không thể dùng evidence như index tái lập và không thể
  tin trạng thái “đã đóng” trong report.
- **Tiêu chí đóng:** sửa report theo observed delta; thay mọi placeholder nguồn
  bằng direct URL/date/scope hoặc xóa/hạ claim; đồng bộ con số và quyết định giữa
  ba lớp artifact.

### Findings đã đóng

- **B1:** không còn nhãn `100%`, `thực địa`, `Xác thực`, PASS tuyệt đối trong
  bốn guide, exact evidence XL–XLIII và implementation report.
- **M4:** đã bỏ giá/policy từng địa điểm cụ thể; các khoảng vé còn lại được trình
  bày ở tầng giả định tổng, chưa tạo finding riêng về boundary tickets.
- **N1:** bốn guide không còn tên file `.md`.
- Phần Ga Huế, địa giới Chân Mây–Lăng Cô/Hải Vân và loại `leash bắt buộc` đã sửa
  đúng hướng. VNR xác nhận Ga Huế ở số 2; Nghị quyết 1659/NQ-UBTVQH15 xác lập
  phường Hải Vân.

## 3. Cách Reviewer chạy lại

```bash
git rev-parse HEAD
git status --short -- session_prompt/CURRENT_HANDOFF.md \
  knowledge-base-hue/tourism/services \
  knowledge-base-hue/meta/tourism-research-evidence.md reports
wc -l <bốn-guide> knowledge-base-hue/meta/tourism-research-evidence.md \
  reports/services_batches_01_03_implementation_correction_report_2026_09_08.md
awk '/^# /{h1++} /^## /{h2++} /^### /{h3++} END{print h1+0,h2+0,h3+0}' <mỗi-guide>
sed -n '1749,2006p' knowledge-base-hue/meta/tourism-research-evidence.md
rg -n '<pattern-rủi-ro>' <bốn-guide> <exact-evidence-sections> <report>
git diff --check
git diff --no-index --check /dev/null <từng-file-untracked-trong-scope>
```

Reviewer websearch bằng truy vấn tiếng Việt, sau đó mở trực tiếp các nguồn ghi
trong B2/M2 và nguồn VNR/Nghị quyết 1659 để kiểm tra đối tượng, ngày và phạm vi.

## 4. Kết quả quan sát

- HEAD: `8739744feabe6574d8bd6d1a9bf1664521dad0fa`.
- Bốn guide/evidence/report là untracked; handoff tracked đang modified. Không có
  exact base diff cho nội dung untracked.
- Fresh line counts: `286 / 247 / 336 / 316`; evidence `2006`; report `91`.
- Heading counts bốn guide: `1/9/29`, `1/10/21`, `1/11/26`, `1/11/31`; exact
  sections XL–XLIII: `H2=4, H3=19, H4=1`.
- `git diff --check`: exit 0, không output; lệnh này không kiểm tra untracked.
- Sáu lệnh `git diff --no-index --check /dev/null <file>`: exit 1 vì khác
  `/dev/null`, không output chẩn đoán whitespace. Đây không phải exit-PASS nhưng
  không phát hiện whitespace error. Bốn guide kết thúc bằng một LF.
- Bốn answer-facing guide không có frontmatter, external URL hoặc wiki-link.
- Pattern rủi ro đã khai báo: 0 match trên bốn guide và exact evidence sections.
- Phép cộng 3N2Đ tiêu chuẩn đúng; cận trên khung tiết kiệm một ngày sai
  `550.000` so với tổng thành phần `700.000`.
- Fresh websearch không tìm thấy notice có thẩm quyền mới hơn tháng 6/2026 xác
  nhận phạm vi Bạch Mã được mở lại.
- Tổng hợp: **1 blocker, 5 nhóm major, 0 minor**.

## 5. Phần chưa chạy và giới hạn

- Không có exact base diff do các artifact implementation vẫn untracked; review
  là toàn bộ current files, không tuyên bố phân lập được delta vòng 2.
- Không xác minh riêng từng dải giá thương mại trong 101 dòng giá. Việc thiếu
  claim-level direct evidence khiến chúng ở trạng thái `not verified`; acceptance
  yêu cầu xóa/hạ mức hoặc cung cấp evidence, không cho phép mặc định giữ.
- Không liên hệ qua điện thoại/email với Vườn quốc gia, Cảng vụ hoặc nhà cung
  cấp; chỉ dùng nguồn web/văn bản công khai đến 08/09/2026.
- Không sửa guide/evidence/report thay Implementer; không commit/push.

## 6. Decision và next action

Decision: **changes_requested**.

Batch 1, Batch 2 và Batch 3 chưa được nghiệm thu vì còn 1 blocker và 5 nhóm
major. Chuyển một correction delta cho Implementer theo
`session_prompt/CURRENT_HANDOFF.md`. Rereview kế tiếp chỉ tái kiểm các finding
còn mở, các artifact bị ảnh hưởng và fresh evidence Bạch Mã/SUP; không mở rộng
scope, migration, ingestion, Golden, Qdrant hoặc runtime.
