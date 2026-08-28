# Codex Re-review: Phase 8 Golden Dataset V2 — Gate 0

> **Historical finding record:** User đã duyệt Golden Dataset V3 complexity
> reset ngày 2026-08-27; report này là input/candidate audit, không còn là next
> correction authorization.

Decision: `changes_requested`
Review round: 3 (Correction Round 2 review)
Reviewer: Codex
Date: `2026-08-27 +07`
Canonical design: `docs/superpowers/specs/2026-08-26-phase-8-golden-dataset-v2-design.md`
Implementation plan: `docs/superpowers/plans/2026-08-26-phase-8-golden-dataset-v2-implementation-plan.md`
Implementation report: `reports/phase_8_golden_dataset_v2_implementation_report.md`

User-confirmed language audit:
`reports/phase_8_golden_dataset_v2_language_quality_audit.md`
Hướng dẫn correction hợp nhất đã được loại khỏi cây hiện hành sau V3 reset;
snapshot cuối của tài liệu vẫn có thể truy xuất tại
`6c44c0b:session_prompt/phase_8_golden_dataset_v2_correction_round_3_prompt.md`.

## 1. Kết quả các finding vòng 2

| Finding vòng 2 | Trạng thái vòng 3 |
|---|---|
| Primary-authoring matrix / `foods-0070` | Đã đóng |
| Sáu semantic cases được nêu cụ thể | Đã sửa, nhưng audit cùng kiểu còn lỗi |
| `foods-0034` và `foods-0035` alternative evidence | Đã đóng |
| Task 7 integration test | Đã đóng |
| Smoke counts và no-fake statement | Đã đóng |
| Implementation report completeness | Chưa đóng hoàn toàn |

## 2. Findings còn mở

### Major 1 — Manual audit vẫn còn unsupported/overclaimed ground truth

Các correction được báo cáo đã xuất hiện trong dataset, nhưng review trực tiếp
source phát hiện các lỗi chắc chắn khác:

- `foods-0098` mới thêm hai khoảng giờ `7:00 – 8:00` và `8:30 – 10:00` vào
  reference answer. Declared section `food-guides.md :: Food tour nửa ngày` chỉ
  nói “Buổi sáng”, sau đó ăn bún bò rồi uống cà phê; không có hai khoảng giờ
  trên. Đây là fabricated detail được đưa vào trong chính correction no-fake.
- `foods-0063` hỏi loại lá gói nhưng reference/keywords còn khẳng định bánh nậm
  làm từ `bột gạo tẻ`. Declared source nói một công thức dùng bột gạo tẻ pha bột
  năng, một mô tả khác dùng bột gạo nếp và loại bột thay đổi theo công thức.
  Reference vừa trả lời thừa phạm vi câu hỏi vừa tuyệt đối hóa một biến thể.
- `foods-0072` tiếp tục ghi `Bánh nậm (bột gạo tẻ)`, trong khi declared section
  `banh nam.md :: Tóm tắt` không nêu loại bột và source chi tiết nói công thức có
  thể dùng bột gạo nếp. Đây là unsupported evidence mapping/reference.
- `foods-0087` hỏi “món ăn vặt, món ngọt” nhưng reference đưa cả Cơm hến Hoa
  Đông, một bữa/món cơm chứ không phải món ăn vặt hoặc món ngọt. Source chỉ gợi
  ý các địa điểm cho nhóm bạn, không gán toàn bộ chúng vào phạm vi câu hỏi này.
- `foods-0059` hỏi cả “trải nghiệm tại quán”, nhưng reference chỉ trả lời lịch
  sử, địa chỉ, nguồn gốc sáng tạo và danh tiếng CNN; declared evidence cũng
  không gồm section `Món ăn / trải nghiệm`. Question và answer chưa khớp.

Golden V2 là ground truth chấm model nên các lỗi này chặn Gate 0 dù validator và
runtime tests đều PASS.

### Major 2 — Alternative-evidence audit vẫn chưa đầy đủ

Hai counterexample vòng trước đã được sửa, nhưng claim “đầy đủ” vẫn không đúng:

- `foods-0052` hỏi giá đồ uống DeChill `20.000 – 55.000 VNĐ` nhưng chỉ khai báo
  `cafes/dechill.md :: Thông tin`. `food-guides.md :: Theo ngân sách` cũng ghi
  trực tiếp DeChill, địa chỉ và đúng khoảng giá này.
- `foods-0062` hỏi nguồn gốc bánh ép từ địa danh nào nhưng chỉ khai báo
  `local_specialties/banh ep.md :: Tóm tắt`. Section
  `restaurants/banh ep gia di.md :: Món ăn / trải nghiệm` cũng nói trực tiếp
  bánh ép tại quán có nguồn gốc từ món bánh lọc ép nóng vùng biển Thuận An.
- `foods-0090` liệt kê ba thương hiệu mè xửng và địa chỉ nhưng không khai báo
  `local_specialties/me xung.md :: Địa điểm tiêu biểu`, section chứa đủ cả ba
  thương hiệu và các địa chỉ trong reference.

Với exact `source + section` binary relevance, các chunk đúng trên vẫn bị gán
nonrelevant. Reviewer không tuyên bố ba ví dụ này là exhaustive list.

### Major 3 — Implementation report chưa đủ thông tin tái lập/handoff

Report đã sửa smoke counts và có no-fake statement, nhưng còn thiếu các mục plan
yêu cầu:

- không còn ghi totals `reused / rewritten / new`;
- không ghi kết quả source conflicts hoặc user-approved reallocations (nếu không
  có thì cần nói rõ `none`);
- Hit/MRR/NDCG chỉ nói được đo bằng “script Python”, không có exact command hoặc
  script path để tái lập;
- Hit@5 là 19/20 nhưng không báo case retrieval miss còn lại như handoff prompt
  yêu cầu.

Đây là correction tài liệu hẹp; không cần tạo thêm artifact hoặc framework.

## 3. Những phần đã đạt

- `foods-0070` hiện là numerical case author đúng từ
  `local_specialties/me xung.md :: Mua làm quà`; primary-authoring matrix được
  khôi phục.
- `foods-0061`, `foods-0065`, `foods-0084`, `foods-0095` và `foods-0097` đã được
  sửa đúng theo finding vòng 2. `foods-0098` đã bỏ “không gian đẹp” nhưng lại
  thêm giờ không có nguồn như Major 1.
- `foods-0034` và `foods-0035` đã bổ sung đúng alternative evidence được chỉ ra.
- Task 7 test hiện lặp đủ 20 smoke cases, kiểm tra metadata/relevance cho mọi
  returned document và không còn current-model hit threshold.
- Smoke distribution trong report hiện cộng đúng 20 và no-fake statement đã có.

## 4. Verification độc lập

| Kiểm tra | Kết quả Reviewer quan sát |
|---|---|
| Full/smoke validator | PASS: 100/20, exact global category counts |
| Focused Golden V2 tests | PASS: 2, deselected 10 |
| Non-paid affected tests | PASS: 9, deselected 3 |
| Corrected isolated Task 7 test | PASS: 1, 2 warnings, 35.00s |
| Isolated cleanup | PASS: `hue_rag_live_test_e5_small_384` cleanup reported `ok` |
| Active collection safety | PASS: `hue_foods_e5_small_384` vẫn 572 points |
| Phase 7 datasets | PASS: không có diff |
| `git diff --check` | PASS |
| Manual semantic/evidence audit | FAIL: Major 1 và Major 2 |

Reviewer không chạy paid generator/judge hoặc Phase 8 model comparison. Reviewer
cũng không xác nhận lại live Hit/MRR/NDCG claims vì report chưa cung cấp exact
reproduction command và các metric này không phải acceptance requirement của
Gate 0.

## 5. Decision và correction hẹp tiếp theo

Decision: `changes_requested`.

Implementer cần:

1. sửa `foods-0098`, `foods-0063`, `foods-0072`, `foods-0087` và `foods-0059`
   để question/reference/evidence khớp trực tiếp source;
2. audit lại alternative evidence, tối thiểu đóng ba counterexample Major 2;
3. cập nhật report với reused/rewritten/new totals, conflict/reallocation outcome,
   exact metric command/path và retrieval-miss ID;
4. chạy lại validator, non-paid tests và isolated Task 7 test rồi bàn giao exact
   outcomes.

Sau review vòng 3, user yêu cầu mở rộng correction thành full 100-case
natural-language/keyword pass. Rubric đã được user xác nhận và phạm vi đầy đủ nằm
trong language audit cùng consolidated correction prompt nêu ở đầu báo cáo. Các
finding tại đó là acceptance input bắt buộc, không chỉ là gợi ý tùy chọn.

User cũng cho phép Implementer research internet về ẩm thực, đồ uống, địa điểm
và nhu cầu du lịch Huế để phát hiện mâu thuẫn và thảo luận. Quyền này không thay
đổi closed-world relevance contract: external pages chỉ là research/reporting
input, không được tự đưa vào Golden evidence hoặc ground truth nếu chưa có quyết
định riêng của user về cập nhật corpus.

Không cần sửa validator, thêm test mới, tạo audit package hoặc chạy benchmark.
Phase 8 vẫn `not_ready`; chưa mở Gate 1, paid calls, production cutover, active
mutation, commit hoặc push.
