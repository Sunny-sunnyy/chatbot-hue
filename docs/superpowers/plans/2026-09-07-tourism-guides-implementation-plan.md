# Tourism Guides Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Sub-agent implementation is not authorized.

**Goal:** Biên soạn `tourism_guides.md` thành cẩm nang du lịch Huế tổng quan canonical, đồng thời loại bỏ ứng viên cẩm nang trùng phạm vi khỏi inventory services và lưu đầy đủ research evidence.

**Architecture:** `tourism_guides.md` là lớp điều phối answer-facing ở cấp domain; các entity và guide chuyên ngành tiếp tục giữ tri thức chi tiết. Hai inventory khóa quyền sở hữu intent, còn `tourism-research-evidence.md` giữ provenance và kết quả kiểm chứng bên ngoài nội dung answer-facing.

**Tech Stack:** Markdown, nguồn web chính thức/độc lập, `rg`, Git read-only inspection và `git diff --check`.

## Global Constraints

- Canonical design: `docs/superpowers/specs/2026-09-07-tourism-guides-design.md`.
- Giao tiếp và nội dung answer-facing dùng tiếng Việt tự nhiên, khách quan.
- Địa chỉ hiện hành dùng cấp phường/xã sau ngày 01/07/2025; không dùng quận, huyện, thị xã hoặc tỉnh Thừa Thiên Huế trong địa chỉ hiện hành.
- Không đưa bảng giá, giờ hoạt động, lịch phương tiện, danh bạ nhà cung cấp hoặc lịch trình 3 ngày 2 đêm chi tiết vào `tourism_guides.md`.
- Không thêm YAML frontmatter, `## Nguồn dữ liệu`, `Liên kết nội bộ` hoặc đường dẫn repository vào nội dung answer-facing.
- Không sửa các entity tourism hoặc guide chuyên ngành đang được session khác review.
- Chỉ dùng claim từ entity tourism sau khi entity đó đã đạt technical review; nếu trạng thái chưa rõ, kiểm chứng lại từ nguồn trực tiếp hoặc bỏ claim.
- Không dùng mock, fake source, search snippet đơn lẻ hoặc nhãn “2026” của bài SEO làm bằng chứng.
- Git authorization: `none`; không commit hoặc push trong implementation này.
- Sub-agent authorization: `none` cho implementation; thực hiện tuần tự trong một session Implementer.

---

## File map

- Modify: `knowledge-base-hue/tourism/tourism_guides.md` — cẩm nang tổng quan answer-facing.
- Modify: `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md` — giảm inventory từ 05 xuống 04 guide và loại ứng viên cẩm nang trùng intent.
- Modify: `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md` — khóa `tourism_guides.md` là cẩm nang tổng quan canonical.
- Modify: `knowledge-base-hue/meta/tourism-research-evidence.md` — thêm hồ sơ nguồn và self-verification cho cẩm nang.
- Create: `reports/tourism_guides_implementation_report_2026_09_07.md` — implementation evidence index.
- Modify: `session_prompt/CURRENT_HANDOFF.md` — bàn giao exact final review cho Reviewer sau khi hoàn tất.

## Review Contract

**Risk level:** `medium` — nội dung answer-facing mới tổng hợp nhiều domain và thay đổi quyết định canonical trong hai inventory; không thay runtime hay active data.

**Implementer evidence:**

- mapping từng tiêu chí nghiệm thu tới section và nguồn;
- research record cho 15 URL do user cung cấp, nguồn chính thức bổ sung, ngày truy cập và quyết định giữ/loại claim;
- căn cứ cho mọi địa giới cụ thể;
- đối chiếu trùng lặp với các guide/entity liên quan;
- kết quả kiểm tra heading/chunk independence, forbidden content và `git diff --check`;
- failed, skipped, partial và not verified được ghi đúng trạng thái.

**Minimum independent Reviewer gate:**

1. resolve base/head và kiểm tra toàn bộ changed/untracked paths;
2. đọc exact diff và map vào acceptance;
3. kiểm tra quyết định canonical trong hai inventory;
4. kiểm tra toàn bộ H2/H3 cùng câu mở đầu về chunk independence;
5. kiểm tra mẫu có chủ đích của claim địa giới, khí hậu, giao thông và an toàn bằng nguồn trực tiếp;
6. kiểm tra trùng lặp liên domain, dữ liệu động và văn phong quảng bá;
7. chạy `git diff --check` và đối chiếu report với trạng thái thực tế.

**Evidence reuse:** Chỉ dùng evidence của entity tourism đã đạt technical review khi claim, nguồn, thời điểm và nội dung không đổi. Không dùng lại evidence cho claim bị sửa hoặc trạng thái vận hành có tính thời điểm.

**New authority required:** commit, push, sửa runtime, mutate active data, mở rộng số guide, sửa entity ngoài scope hoặc thay đổi provider/dataset.

---

### Task 1: Khóa trạng thái đầu vào và lập hồ sơ nghiên cứu cẩm nang

**Files:**

- Read: `docs/superpowers/specs/2026-09-07-tourism-guides-design.md`
- Read: `knowledge-base-hue/meta/tourism-template.md`
- Read: `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`
- Read: `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`
- Read: `knowledge-base-hue/tourism/tickets/tickets-research-and-entities-inventory.md`
- Read: `knowledge-base-hue/performing_arts/performing_arts_guides.md`
- Read: `knowledge-base-hue/heritages/heritage-guides.md`
- Read: `knowledge-base-hue/foods/food-guides.md`
- Read: `knowledge-base-hue/festivals/festival-guides.md`
- Modify: `knowledge-base-hue/meta/tourism-research-evidence.md`

**Produces:** Section `## XXXVIII. Cẩm nang du lịch Huế tổng quan (`tourism_guides.md`)` chứa nguồn, claim matrix, mâu thuẫn, quyết định và self-verification.

- [ ] **Step 1: Kiểm tra worktree và cô lập thay đổi đồng thời**

Run:

```bash
git status --short
git diff --name-only
git ls-files --others --exclude-standard
```

Expected: ghi lại toàn bộ changed/untracked paths; không sửa hoặc ghi đè thay đổi của session khác. Nếu một trong bốn file implementation đang được session khác sửa, dừng mutation file đó cho tới khi trạng thái ổn định.

- [ ] **Step 2: Xác nhận đầu vào canonical đã sẵn sàng**

Run:

```bash
rg -n "Technical verdict:|ready_for_user_confirmation|changes_requested" reports/tourism_*_codex_*report_2026_09_0*.md session_prompt/CURRENT_HANDOFF.md
rg -n '^# |^## ' knowledge-base-hue/tourism/*.md
```

Expected: xác định rõ entity nào đã đạt technical review và entity nào còn correction. Không dùng claim của entity chưa đạt để khóa nội dung tổng hợp.

- [ ] **Step 3: Đọc lại 15 URL sạch và ghi tình trạng truy cập**

Đọc các URL đã được user cung cấp sau khi bỏ `utm_source`. Với mỗi URL, ghi trong evidence: ngày truy cập `07/09/2026`, trạng thái `truy cập được`, `bị chặn`, `cache miss` hoặc `chỉ có bản chỉ mục`; loại nguồn; nhóm intent hữu ích; claim không được dùng.

Các nhóm claim bắt buộc tách riêng:

- thời điểm và khí hậu;
- cách đến Huế và di chuyển tại Huế;
- phân cụm địa lý và thời lượng;
- khu vực lưu trú;
- trang phục, khả năng tiếp cận và an toàn;
- địa giới;
- giá, giờ, lịch và nhà cung cấp cần loại khỏi guide tổng quan.

- [ ] **Step 4: Kiểm chứng claim quan trọng bằng nguồn trực tiếp**

Dùng truy vấn web tiếng Việt và ưu tiên:

- Nghị quyết 175/2024/QH15 cho trạng thái thành phố trực thuộc Trung ương từ 01/01/2025;
- Nghị quyết 1675/NQ-UBTVQH15 và bản đồ hành chính thành phố Huế cho 40 phường/xã từ 01/07/2025;
- UBND/Sở Du lịch Huế và Cục Khí tượng Thủy văn cho mùa mưa, nắng nóng, bão và lũ;
- ACV/Cảng hàng không quốc tế Phú Bài cho sân bay và địa chỉ hiện hành;
- Đường sắt Việt Nam cho kênh tra lịch/giá tàu;
- cơ quan quản lý trực tiếp cho trạng thái tiếp cận hoặc cảnh báo an toàn.

Expected: mỗi claim được giữ có ít nhất một nguồn trực tiếp; claim quan trọng có mâu thuẫn hoặc ảnh hưởng an toàn có thêm nguồn độc lập thứ hai.

- [ ] **Step 5: Thêm section evidence XXXVIII**

Section phải có đúng các tiểu mục:

```markdown
## XXXVIII. Cẩm nang du lịch Huế tổng quan (`tourism_guides.md`)

### 1. Nguồn do người dùng cung cấp và tình trạng truy cập
### 2. Nguồn đối chiếu độc lập và phạm vi thẩm quyền
### 3. Đối chiếu địa giới hành chính tại tháng 09/2026
### 4. Bảng claim và quyết định biên soạn
### 5. Mâu thuẫn, dữ liệu động và nội dung bị loại
### 6. Kết quả self-verification sau bản thảo
```

Trong bước này điền các mục 1–5. Mục 6 ghi `Chưa thực hiện — chỉ hoàn tất sau khi bản thảo tourism_guides.md tồn tại`; đây là trạng thái quy trình có chủ đích, không phải acceptance cuối.

- [ ] **Step 6: Kiểm tra evidence trước khi viết**

Run:

```bash
rg -n '^## XXXVIII|^### [1-6]\.' knowledge-base-hue/meta/tourism-research-evidence.md
rg -n 'utm_source=chatgpt|tỉnh Thừa Thiên Huế|quận |huyện |thị xã ' knowledge-base-hue/meta/tourism-research-evidence.md
```

Expected: section XXXVIII và sáu tiểu mục tồn tại; URL đã bỏ tracking. Các kết quả địa giới cũ chỉ được giữ trong ngữ cảnh nguồn cũ/mâu thuẫn và phải được gắn nhãn rõ.

---

### Task 2: Khóa lại quyền sở hữu canonical trong hai inventory

**Files:**

- Modify: `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`
- Modify: `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`

**Consumes:** Quyết định đã duyệt rằng `tourism_guides.md` là cẩm nang tổng quan duy nhất.

**Produces:** Một inventory tourism sở hữu guide tổng quan và một inventory services chỉ còn bốn guide chuyên biệt.

- [ ] **Step 1: Cập nhật inventory services từ 05 thành 04 guide**

Thực hiện toàn bộ thay đổi sau:

- đổi mọi tuyên bố tổng số `05 file` thành `04 file` trong đúng ngữ cảnh inventory;
- xóa `Cẩm nang du lịch Huế.md` khỏi danh sách file và thứ tự triển khai;
- xóa subsection mô tả file này như một deliverable của services;
- ghi rõ intent cẩm nang tổng quan thuộc `../tourism_guides.md`;
- giữ nguyên bốn file `Đến Huế nên đi đâu.md`, `Lịch trình du lịch Huế ngắn ngày.md`, `Lịch trình du lịch Huế 3 ngày 2 đêm.md`, `Chi phí du lịch Huế.md`;
- cập nhật số thứ tự và tiêu chí nghiệm thu tương ứng;
- không thay đổi yêu cầu nội dung của bốn guide còn lại ngoài tham chiếu cần thiết để tránh trùng.

- [ ] **Step 2: Cập nhật inventory tourism**

Trong phần `Cẩm nang tổng hợp`, khóa:

```text
tourism_guides.md là cẩm nang du lịch Huế tổng quan canonical duy nhất.
```

Thay ứng viên `cam-nang-du-lich-hue.md` và mọi diễn đạt “cần tiếp tục chốt” liên quan đến số lượng cẩm nang bằng quyết định đã duyệt. Mô tả ranh giới: guide tổng quan giữ logic lựa chọn; lịch trình/chi phí chi tiết thuộc `services`; vé thuộc `tickets`; tri thức entity thuộc domain tương ứng.

- [ ] **Step 3: Kiểm tra không còn hai canonical guide**

Run:

```bash
rg -n "Cẩm nang du lịch Huế\.md|cam-nang-du-lich-hue\.md|05 file|5 file|tourism_guides\.md" knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md
```

Expected: không còn `Cẩm nang du lịch Huế.md` hoặc `cam-nang-du-lich-hue.md` như deliverable; tổng services là 04; `tourism_guides.md` xuất hiện với vai trò canonical duy nhất.

---

### Task 3: Biên soạn cẩm nang answer-facing

**Files:**

- Modify: `knowledge-base-hue/tourism/tourism_guides.md`

**Consumes:** Design section 4, evidence XXXVIII mục 1–5, các entity đã đạt review và ranh giới canonical vừa cập nhật.

**Produces:** Một file Markdown answer-facing hoàn chỉnh với đúng H1/H2/H3 đã duyệt.

- [ ] **Step 1: Tạo đúng outline đã duyệt**

Dùng nguyên outline tại section 4 của design. Không thêm lịch trình 3 ngày 2 đêm rút gọn, bảng giá, source section hoặc guide mới.

- [ ] **Step 2: Viết phần định vị, thời lượng và thời điểm**

Nội dung phải:

- mô tả Huế phù hợp với chuyến đi văn hóa–di sản, ẩm thực, nghệ thuật, đô thị, biển–đầm phá, sinh thái và cộng đồng;
- trình bày thời lượng như lựa chọn theo nhu cầu, không như một lịch trình cố định;
- phân biệt giai đoạn thuận lợi hơn cho tham quan, giai đoạn nóng phù hợp mục tiêu biển và giai đoạn tăng rủi ro mưa/bão/lũ;
- yêu cầu kiểm tra dự báo gần ngày đi và không dùng “mùa đẹp nhất” tuyệt đối.

- [ ] **Step 3: Viết phần tiếp cận, di chuyển và phân cụm**

Nội dung phải:

- nêu máy bay qua Phú Bài, đường sắt và đường bộ ở mức lựa chọn;
- không nêu hãng, giá, số hiệu chuyến hoặc lịch chạy;
- hướng dẫn chọn đi bộ, xe đạp, phương tiện có lái hoặc tự lái theo khoảng cách, nhóm người, thời tiết và thể lực;
- mô tả đúng năm cụm đã duyệt;
- khuyên chọn một nhánh ngoại thành phù hợp mỗi ngày thay vì ghép các hướng xa.

- [ ] **Step 4: Viết phần lựa chọn trải nghiệm và khu vực lưu trú**

Nội dung phải điều hướng vừa đủ tới di sản, ẩm thực, nghệ thuật, lễ hội, chợ/phố đi bộ, thiên nhiên và cộng đồng. Khu vực lưu trú được mô tả theo nhịp sống, khả năng đi bộ, nhu cầu yên tĩnh và hướng hành trình; không nêu khách sạn, homestay hoặc cơ sở thương mại cụ thể.

- [ ] **Step 5: Viết phần chuẩn bị, khả năng tiếp cận, an toàn và dữ liệu động**

Nội dung phải:

- điều chỉnh hành lý cho nóng, mưa và hoạt động ngoài trời;
- khuyên trang phục lịch sự tại di tích, cơ sở tôn giáo và cộng đồng mà không bịa chế tài;
- nêu phương án cho trẻ nhỏ, người cao tuổi và người hạn chế vận động;
- tách rủi ro giao thông, nắng nóng, mưa/lũ và hoạt động biển–đầm–núi–suối;
- yêu cầu kiểm tra giá, giờ, lịch vận chuyển/sự kiện, trạng thái tiếp cận và cảnh báo thời tiết sát ngày đi.

- [ ] **Step 6: Kiểm tra cấu trúc và nội dung cấm**

Run:

```bash
rg -n '^# ' knowledge-base-hue/tourism/tourism_guides.md
rg -n '^## |^### ' knowledge-base-hue/tourism/tourism_guides.md
rg -n 'Nguồn dữ liệu|Liên kết nội bộ|utm_source|quận |huyện |thị xã |tỉnh Thừa Thiên Huế|TBD|TODO|placeholder' knowledge-base-hue/tourism/tourism_guides.md
rg -ni 'tuyệt mỹ|độc nhất vô nhị|hùng vĩ bậc nhất|đẹp nhất|an toàn tuyệt đối|chữa lành tuyệt đối|bùng nổ|đẳng cấp|mãn nhãn|chưa từng có' knowledge-base-hue/tourism/tourism_guides.md
```

Expected: đúng một H1; outline khớp design; hai lệnh tìm nội dung cấm không trả kết quả. Nếu địa giới cũ cần xuất hiện trong ngữ cảnh lịch sử, Reviewer phải phê duyệt ngoại lệ có evidence.

---

### Task 4: Đối chiếu liên domain và hoàn tất self-verification

**Files:**

- Modify: `knowledge-base-hue/tourism/tourism_guides.md`
- Modify: `knowledge-base-hue/meta/tourism-research-evidence.md`

**Produces:** Bản thảo đã loại duplication và evidence XXXVIII có kết quả self-verification thật.

- [ ] **Step 1: Đối chiếu từng section với nguồn canonical**

Đọc song song section tương ứng trong:

```text
knowledge-base-hue/heritages/heritage-guides.md
knowledge-base-hue/foods/food-guides.md
knowledge-base-hue/festivals/festival-guides.md
knowledge-base-hue/performing_arts/performing_arts_guides.md
knowledge-base-hue/tourism/tickets/tickets-research-and-entities-inventory.md
knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md
```

Với mỗi đoạn trùng ý, giữ ở `tourism_guides.md` tối đa phần cần để người dùng lựa chọn và chuyển chi tiết về đúng domain. Không sao chép bảng, danh sách dài, giá, giờ hoặc mô tả lịch sử.

- [ ] **Step 2: Kiểm tra chunk independence**

Với từng H2/H3, đọc section mà không dựa vào section trước và xác nhận:

- heading xác định rõ Huế hoặc khu vực;
- câu đầu có chủ thể;
- danh sách có câu dẫn;
- đại từ không làm mất nghĩa khi section đứng riêng;
- section không lặp đáng kể một section khác.

Ghi kết quả theo từng heading vào evidence XXXVIII mục 6.

- [ ] **Step 3: Kiểm chứng lại độc lập các claim quan trọng**

Không chỉ mở lại nguồn đã dùng ở Task 1. Dùng truy vấn tiếng Việt mới để kiểm tra mẫu có chủ đích gồm:

- cơ cấu 40 phường/xã và ít nhất bốn ánh xạ địa giới xuất hiện trong guide;
- mùa mưa, tháng có rủi ro mưa lớn và giai đoạn nắng nóng;
- sân bay Phú Bài và lựa chọn đường sắt;
- logic cụm Phú Xuân–Thuận Hóa, Kim Long–Thủy Xuân và các nhánh ngoại thành;
- cảnh báo an toàn cho ít nhất một hoạt động biển/đầm và một hoạt động núi/suối.

Nếu nguồn mới mâu thuẫn, loại claim khỏi bản thảo hoặc ghi mâu thuẫn trong evidence; không tự chọn cách diễn đạt che khác biệt.

- [ ] **Step 4: Hoàn tất evidence mục 6**

Thay trạng thái “Chưa thực hiện” bằng ngày kiểm tra, truy vấn mới, kết quả quan sát, claim đã sửa/loại và giới hạn còn lại. Không ghi PASS cho phần chưa kiểm chứng.

---

### Task 5: Kiểm tra exact diff và bàn giao final review

**Files:**

- Create: `reports/tourism_guides_implementation_report_2026_09_07.md`
- Modify: `session_prompt/CURRENT_HANDOFF.md`

**Produces:** Evidence index và một handoff `final_review` duy nhất cho Reviewer.

- [ ] **Step 1: Kiểm tra changed paths và exact diff**

Run:

```bash
git status --short
git diff -- knowledge-base-hue/tourism/tourism_guides.md knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md knowledge-base-hue/meta/tourism-research-evidence.md
git diff --check
```

Expected: chỉ các path đã duyệt chứa thay đổi của task; `git diff --check` không có output. Với file untracked, đọc toàn bộ file và dùng `git diff --no-index --check /dev/null <path>`; exit 1 do có diff là bình thường, nhưng không được có cảnh báo whitespace.

- [ ] **Step 2: Lập implementation report**

Report phải có:

- scope và changed paths;
- mapping acceptance → section/evidence;
- nguồn và ngày kiểm tra;
- các claim bị loại hoặc hạ mức khẳng định;
- lệnh đã chạy và kết quả quan sát thực tế;
- failed, skipped, partial, not verified;
- xác nhận không commit/push và không sửa runtime/entity ngoài scope;
- exact checks Reviewer cần chạy lại theo Review Contract.

- [ ] **Step 3: Cập nhật handoff cho Reviewer**

Thay `CURRENT_HANDOFF.md` bằng một task duy nhất có:

```text
Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Risk level: medium
Git authorization: none
Sub-agent authorization: none
Technical verdict: pending_reviewer_review
```

Handoff dẫn tới design, plan, implementation report, changed paths và exact Reviewer reruns; không chép lại toàn bộ report.

- [ ] **Step 4: Kiểm tra handoff và dừng**

Run:

```bash
rg -n '^Target role: reviewer$|^Handoff kind: final_review$|^State: active$|^Risk level: medium$|^Git authorization: none$|^Sub-agent authorization: none$' session_prompt/CURRENT_HANDOFF.md
git diff --check
```

Expected: đủ bảy trường điều phối cần thiết và không có lỗi whitespace. Implementer dừng sau bàn giao; không tự approve, commit hoặc push.
