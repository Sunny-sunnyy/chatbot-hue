# Codex Third Rereview: Services Batches 1–3

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-08
Base commit: `8739744feabe6574d8bd6d1a9bf1664521dad0fa`
Previous rereview: `reports/services_batches_01_03_codex_second_rereview_2026_09_08.md`
Implementation report: `reports/services_batches_01_03_implementation_correction_report_2026_09_08.md`

## 1. Phạm vi đã review

Reviewer đã đọc toàn bộ bốn guide answer-facing, Mục XL–XLIII của evidence,
inventory services, implementation report, handoff và các review trước. Vì đây
là verdict `changes_requested` thứ tư của cùng implementation, Reviewer cũng
audit lại guide, design, plan, acceptance và bốn vòng findings theo workflow.

Bốn guide, evidence và implementation report vẫn untracked tại base nêu trên;
không có exact base diff để phân lập delta vòng 3. Reviewer đã đọc toàn bộ
current content trong exact scope, không đưa thay đổi ngoài scope vào verdict.
Reviewer chạy fresh checks và websearch tiếng Việt đến ngày 08/09/2026 cho
Bạch Mã, SUP và Ca Huế; không sửa implementation, commit hoặc push.

## 2. Findings

### Blocker B1 — Báo cáo dùng nhãn tuyệt đối và khai sai kết quả kiểm tra

- **Vị trí:** implementation report dòng 57, 68, 84 và 94–98; handoff dòng
  52, 56, 68 và 77.
- **Requirement:** không dùng nhãn `100%`, `thực địa` hoặc xác thực tuyệt đối
  không có hồ sơ tái lập; report phải phản ánh đúng lệnh và observed result.
- **Observed:** report dùng `100%` để tuyên bố đã rà soát phép cộng, thay mọi
  placeholder và có direct URL, rồi liệt kê chính `100%` trong regex bị cấm
  nhưng tuyên bố scan 0 match. Fresh `rg` tìm thấy ba match trong report và ba
  match trong handoff. Mục XL–XLIII không có match nhóm từ khóa rủi ro, nhưng
  implementation report thuộc exact scope vẫn tự mâu thuẫn.
- **Tác động:** provenance/self-verification không tái lập được.
- **Tiêu chí đóng:** bỏ nhãn tuyệt đối và ghi đúng phạm vi/observed result của
  từng lệnh; không tuyên bố 0 match khi artifact được quét chứa mẫu.

### Major M1 — Ranh giới services và slot giờ cứng vẫn chưa được sửa

- **Vị trí:** `Đến Huế nên đi đâu.md:13–16,53–145,207–275`;
  `Lịch trình du lịch Huế ngắn ngày.md:135–168`;
  `Lịch trình du lịch Huế 3 ngày 2 đêm.md:69–153,255,308,336`.
- **Observed:** guide lựa chọn vẫn là toplist 286 dòng với mô tả entity dài.
  Guide ngắn ngày vẫn giữ `7:00–10:00`, `10:15–11:15`, `11:30–14:30`,
  `14:45–16:30`, `17:00` ở dòng 139–143 và `10:30–15:00` ở dòng 163.
  Guide 3N2Đ còn giờ cứng và nhiều mô tả công trình/món ăn. Điều này bác bỏ
  report/evidence rằng toàn bộ slot cứng và mô tả chuyên sâu đã bị bỏ.
- **Tác động:** tiếp tục lấn canonical liên domain và làm evidence sai body.
- **Tiêu chí đóng:** cần cấu trúc đích được duyệt cho từng guide rồi biên tập
  theo cấu trúc đó, không tiếp tục xử lý bằng scan/xóa cụm từ riêng lẻ.

### Major M3 — Claim tiếp cận và vận hành đường thủy vẫn vượt evidence

- **Vị trí:** guide ngắn ngày dòng 177–188; guide 3N2Đ dòng 192–215; evidence
  dòng 1814, 1867, 1922 và 1926.
- **Observed:** body vẫn khẳng định xe đỗ sát cổng, nền/đường bằng phẳng, bậc
  thấp, 127 bậc không có dốc chuyên dụng, xe điện đi trong Hoàng cung, xe đỗ
  sát gian hàng và cầu gỗ lim “an toàn, không có xe cơ giới”. Một câu “nên
  liên hệ trước” không biến các mệnh đề trước đó thành claim có điều kiện.
  Evidence chỉ dẫn homepage, không có trang trực tiếp cho từng điều kiện.
- **Ca Huế:** record dòng 1867 chỉ dẫn homepage Hue-S cho điều kiện xuất bến.
  Fresh websearch tìm được quy chế trực tiếp và Công báo 2025 về quản lý Ca
  Huế/Bến Tòa Khâm; artifact chưa dùng chúng. Giá Ca Huế dòng 1990 cũng chỉ
  dẫn homepage, không phải bảng giá/niêm yết.
- **Tác động:** người hạn chế vận động có thể lập lịch theo điều kiện chưa xác
  nhận; provenance vận hành/giá Ca Huế không đạt claim-level.
- **Tiêu chí đóng:** mỗi điều kiện còn giữ phải có direct page đúng phạm vi,
  hoặc hạ hoàn toàn thành bước liên hệ; dùng direct regulation cho Ca Huế.

### Major M5 — Giá thương mại còn rộng và không khớp record claim-level

- **Vị trí:** `Chi phí du lịch Huế.md:20,46,54–80,93–115,125–165,174–243`;
  evidence dòng 1984–1994.
- **Observed:** fresh scan theo pattern Reviewer công khai cho 74 dòng có giá,
  không phải 71. Body vẫn giữ hàng chục giá động về phòng, xe máy, taxi, ô tô,
  thuyền rồng, hướng dẫn viên, cổ phục, ăn uống và giá theo nhóm; XLIII chỉ có
  11 record tổng hợp.
- **Mismatch:** body dùng xe máy `90–120k/130–180k`, lưu trú `130–200k`,
  `250–450k`, `1,3–3,2 triệu`, `3,5–9 triệu`, ăn uống
  `130–220k/250–450k`; evidence ghi xe máy `100–150k`, lưu trú
  `200–350k/550–950k/1,4–3,2 triệu`, ăn uống
  `120–180k/250–400k/500–800k`. Nhiều dải khác không có record.
- **Phần đã đóng:** Reviewer tính lại độc lập các cận thấp/cao trong ba bảng và
  phép cộng vé máy bay; tất cả tổng hiện đúng, gồm `415–700k` và
  `4,98–7,65 triệu`.
- **Tác động:** ngân sách dựa vào giá không tái lập và evidence sai body.
- **Tiêu chí đóng:** thiết kế file theo công thức với tập giả định nhỏ; mỗi đầu
  vào động còn giữ phải map một-một tới URL/chủ thể/ngày/phạm vi.

### Major M6 — “Direct URL” vẫn là homepage và artifacts không đồng bộ

- **Vị trí:** evidence dòng 1804, 1806–1808, 1810, 1812–1814, 1861–1867,
  1922, 1924–1928, 1989–1991, 1993–1994; report dòng 63, 68 và 84.
- **Observed:** ít nhất 24 record/đoạn dùng URL gốc như `https://hue.gov.vn`,
  `https://xaydungchinhsach.chinhphu.vn`, `https://svhtt.thuathienhue.gov.vn`,
  `https://tuongtac.hue.gov.vn`, `https://hdnd.thuathienhue.gov.vn`,
  `https://vr.com.vn` hoặc `https://hueworldheritage.org.vn`. Đây không phải
  direct URL tới tài liệu hỗ trợ exact claim. Nghị quyết 55 dòng 1989, giá Ca
  Huế dòng 1990 và Kế hoạch 155 dòng 1991 chỉ có homepage dù prompt đã cung cấp
  URL tài liệu trực tiếp cho Nghị quyết/Kế hoạch.
- **Đồng bộ:** evidence nói slot giờ và claim tiếp cận tuyệt đối đã bỏ nhưng
  body còn giữ; report nói mọi record có direct URL nhưng bảng dùng homepage;
  report nói scan 0 match nhưng chính report chứa mẫu.
- **Tác động:** evidence không phải index tái lập và không chứng minh được
  acceptance claim-level.
- **Tiêu chí đóng:** dùng URL trang/tài liệu trực tiếp và ma trận claim-ID để
  so sánh body, evidence, report.

### Findings đã đóng

- **B2:** đã bỏ lịch trình Bạch Mã mặc định, Trĩ Sao/Vườn thực vật và giá xe
  lên đỉnh. Fresh search không tìm thấy notice mở tuyến mới hơn tháng 06/2026;
  guide hiện chỉ yêu cầu liên hệ Ban quản lý trước khi lập kế hoạch.
- **M2:** SUP dùng đúng ngày gửi 28/06/2023, ngày xử lý 13/09/2023 và chỉ giữ
  áo phao, thiết bị cứu sinh, tránh luồng tàu.
- **M4, N1:** vẫn đóng; answer-facing không có bảng vé/policy từng điểm, URL
  ngoài, wiki-link hoặc tên file `.md`.

## 3. Cách Reviewer chạy lại

```bash
git rev-parse HEAD
git status --short
wc -l <bốn-guide> knowledge-base-hue/meta/tourism-research-evidence.md <implementation-report>
awk '<đếm H1/H2/H3>' <từng-guide>
sed -n '1749,2007p' knowledge-base-hue/meta/tourism-research-evidence.md
rg -n -i '<pattern-rủi-ro>' <bốn-guide> <evidence> <implementation-report> <handoff>
rg -n '<pattern-slot-giờ>' <ba-guide-lịch-trình>
rg -n '<pattern-khả-năng-tiếp-cận>' <hai-guide-lịch-trình>
rg -n '<pattern-giá>' 'knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md'
git diff --check
git diff --no-index --check /dev/null <từng-file-untracked-trong-scope>
tail -c 2 <từng-file> | od -An -t x1
```

Reviewer tính lại tổng bằng `awk BEGIN`. Websearch tiếng Việt và mở các nguồn:

- `https://baovanhoa.vn/doi-song/cham-khac-phuc-sat-lo-tuyen-duong-len-dinh-bach-ma-vi-dang-cho-von-236622.html`;
- `https://tuongtac.hue.gov.vn/phan-anh/ngay-23-6-2026-toi-co-di-tham-quan-vuon-quoc-gia-bach-ma-tp.-hue-tai-km12-vi-tri-sat-lo-nguy-hie-a228251.html`;
- `https://tuongtac.hue.gov.vn/phan-anh/kien-nghi-kiem-tra-viec-cho-thue-thuyen-sup-gay-mat-an-toan-a111861.html`;
- `https://stp.hue.gov.vn/van-ban-phap-luat/tinh-thua-thien-hue-ban-hanh-quy-che-quan-ly-va-to-chuc-hoat-dong-bieu-dien-ca-hue-tren-dia-ban-tinh.html`;
- `https://congbao.hue.gov.vn/2025/59/BanInCB_2025_59_31_signed.pdf`.

## 4. Kết quả quan sát

- HEAD: `8739744feabe6574d8bd6d1a9bf1664521dad0fa`.
- Line counts: `286 / 247 / 338 / 302`; evidence `2007`; report `106`.
- Heading counts: `1/9/29`, `1/10/21`, `1/11/26`, `1/11/31`.
- Bốn guide/evidence/report untracked; không có exact correction diff.
- `git diff --check`: exit 0, không output; không bao phủ untracked.
- Sáu lệnh no-index: exit 1 vì khác `/dev/null`, output rỗng; không phát hiện
  whitespace error. Sáu file kết thúc bằng LF.
- Bốn guide sạch frontmatter, external URL, wiki-link, tên file `.md` và
  section `## Nguồn dữ liệu`.
- XL–XLIII không có match nhóm từ khóa rủi ro. Report/handoff có sáu match
  `100%`, trái tuyên bố scan 0 match.
- Tìm thấy 10 slot giờ cứng trong hai guide lịch trình.
- Pattern giá của Reviewer khớp 74 dòng; tất cả phép cộng bảng hiện đúng.
- Websearch không tìm thấy notice mở tuyến Bạch Mã mới hơn tháng 06/2026.
- Tổng hợp: **1 blocker, 4 nhóm major, 0 minor**.

## 5. Phần chưa chạy và giới hạn

- Không có exact base diff do artifact vẫn untracked; review toàn bộ current
  files, không tuyên bố phân lập delta vòng 3.
- Không xác minh từng dải giá trong 74 dòng. Dải không có record claim-level là
  `not verified`; acceptance không cho phép mặc định giữ.
- Không liên hệ điện thoại/email với Vườn quốc gia, Cảng vụ hoặc nhà cung cấp;
  chỉ dùng nguồn công khai đến 08/09/2026.
- Search không chứng minh tuyệt đối không có notice Bạch Mã ngoài web index.
- Không chạy runtime, ingestion, Golden hoặc Qdrant vì ngoài scope.
- Không sửa guide/evidence/report; không commit/push.

## 6. Decision và next step

Decision: **changes_requested**. Chưa nghiệm thu Batch 1, 2 hoặc 3.

Đây là verdict `changes_requested` thứ tư. Theo workflow, Reviewer dừng trước
correction thứ năm và không phát hành thêm checklist vá cục bộ.

Audit complexity reset cho thấy inventory/acceptance đã nêu đúng ranh giới,
nhưng không có written design hoặc implementation plan riêng cho bốn services
guide. Design/plan duy nhất được tìm thấy dành cho `tourism_guides.md` và ghi
rõ không sửa guide chuyên ngành. Bốn vòng correction dựa nhiều vào xóa từ khóa
và tự khai trạng thái, không có ánh xạ một-một body–evidence–report. Findings
hiện tại là mâu thuẫn trực tiếp với acceptance, không phải review quá khắt khe.

Next step cần user duyệt design reset tối giản: viết lại bốn guide theo outline
ngắn; khóa ngân sách vào một số ít giả định có evidence; dùng claim-ID matrix
để kiểm body/evidence/report. Không migration, ingestion, Golden, Qdrant,
runtime hoặc correction vòng 5 trước quyết định của user.
