# Tourism Services Minimal Reset Implementation Plan

> **Dành cho người thực hiện:** dùng quy trình `executing-plans` để hoàn thành
> từng task theo thứ tự và đánh dấu checkbox. Không dùng sub-agent.

**Mục tiêu:** Viết lại tối giản bốn cẩm nang dịch vụ du lịch Huế, đồng bộ hồ
sơ bằng chứng và bàn giao một implementation có thể tái thẩm định độc lập.

**Kiến trúc:** Mỗi cẩm nang sở hữu một nhu cầu riêng: chọn điểm, lịch trình
ngắn ngày, lịch trình ba ngày hai đêm và lập ngân sách. Nội dung chi tiết của
di sản, ẩm thực, nghệ thuật biểu diễn, điểm đến và vé tham quan tiếp tục thuộc
các cẩm nang chuyên ngành.

**Công cụ:** Markdown, nguồn web trực tiếp, `rg`, `awk`, `wc`, Git read-only và
`git diff --check`.

## Ràng buộc chung

- Thiết kế canonical:
  `docs/superpowers/specs/2026-09-08-tourism-services-minimal-reset-design.md`.
- Giữ nguyên bốn guide dưới `knowledge-base-hue/tourism/services/`.
- Không sửa inventory hoặc nội dung canonical liên domain.
- Không migration, ingestion, Golden, Qdrant, runtime hoặc Agentic RAG.
- Không dùng sub-agent; không commit hoặc push.
- Không xóa/reset thay đổi ngoài scope.
- Bốn cẩm nang dành cho người đọc không chứa URL ngoài, đường dẫn repository,
  tên file `.md`, wiki-link, frontmatter, metadata hoặc mục nguồn nội bộ.
- Mọi tài liệu Markdown dùng ngôn ngữ tự nhiên; không dùng mã định danh kỹ
  thuật, nhãn kiểm thử hoặc khẳng định tuyệt đối.
- Homepage không được coi là nguồn trực tiếp.
- Dữ liệu động không đủ nguồn phải bị xóa hoặc chuyển thành bước kiểm tra trước
  chuyến đi.

## Bản đồ file

- Viết lại: `knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md`.
- Viết lại: `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md`.
- Viết lại: `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md`.
- Viết lại: `knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md`.
- Viết lại đúng Mục XL–XLIII:
  `knowledge-base-hue/meta/tourism-research-evidence.md`.
- Tạo: `reports/services_batches_01_03_minimal_reset_implementation_report_2026_09_08.md`.
- Cập nhật: `session_prompt/CURRENT_HANDOFF.md`.

---

### Task 1: Khóa nguồn và trạng thái đầu vào

**Files:**

- Đọc: bốn guide trong phạm vi.
- Đọc: Mục XL–XLIII của `knowledge-base-hue/meta/tourism-research-evidence.md`.
- Đọc: spec và report third rereview.
- Không sửa file trong task này.

- [x] **Bước 1: Ghi nhận trạng thái worktree và base**

Chạy:

```bash
git rev-parse HEAD
git status --short
```

Kỳ vọng: HEAD là `8739744feabe6574d8bd6d1a9bf1664521dad0fa`; ghi nhận
đúng các file untracked/dirty và không xử lý thay đổi ngoài scope.

- [x] **Bước 2: Đọc lại exact source hiện tại**

Đọc toàn bộ bốn guide, Mục XL–XLIII, implementation report gần nhất và
third rereview. Lập ghi chú tạm về nội dung được giữ, viết lại hoặc xóa; không
chèn ghi chú này vào answer-facing Markdown.

- [x] **Bước 3: Xác minh lại nguồn có tính thời điểm**

Tìm kiếm bằng tiếng Việt và mở trang trực tiếp cho:

1. trạng thái tuyến Bạch Mã sau tháng 06/2026;
2. yêu cầu an toàn SUP trên sông Hương;
3. quy định quản lý Ca Huế và hoạt động tại Bến Tòa Khâm;
4. địa giới có hiệu lực từ ngày 01/07/2025;
5. địa chỉ Ga Huế;
6. từng đầu vào giá dự kiến giữ trong cẩm nang chi phí.

Kỳ vọng: mỗi thông tin còn giữ có URL trang hoặc tài liệu trực tiếp, chủ thể,
ngày nguồn, ngày truy cập và phạm vi hỗ trợ. Nếu không có nguồn đủ phạm vi,
đánh dấu xóa hoặc chuyển thành hướng dẫn kiểm tra.

- [x] **Bước 4: Chốt tập đầu vào giá**

Chọn không quá mười nhóm đầu vào thực sự cần cho công thức ngân sách. Không
giữ giá nhà cung cấp cụ thể, giá vé từng điểm hoặc các bảng giá lặp theo từng
kiểu khách.

Kết quả của Task 1 là một tập nguồn đủ để viết, không phải thay đổi file.

---

### Task 2: Viết lại cẩm nang chọn điểm đến và Mục XL

**Files:**

- Viết lại: `knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md`.
- Viết lại: Mục XL trong `knowledge-base-hue/meta/tourism-research-evidence.md`.

- [x] **Bước 1: Viết đúng outline đã duyệt**

Dùng một H1 và các H2 theo thứ tự:

```markdown
# Đến Huế nên đi đâu

## Chọn điểm đến Huế theo quỹ thời gian
## Chọn điểm đến Huế theo sở thích
## Chọn điểm đến Huế theo nhóm khách và khả năng vận động
## Chọn điểm đến Huế theo thời tiết
## Năm cụm điểm đến chính tại Huế
## Thông tin cần kiểm tra trước chuyến đi
```

Trong mục năm cụm, dùng H3 cho Phú Xuân–Thuận Hóa, Kim Long–Thủy Xuân, biển
và đầm phá phía đông, Bạch Mã–Chân Mây–Lăng Cô, miền núi–du lịch cộng đồng.
Mỗi cụm chỉ nêu vai trò, thời lượng tương đối, đối tượng phù hợp và điều kiện
chính. Không viết lại lịch sử, kiến trúc, món ăn hoặc chương trình biểu diễn.

- [x] **Bước 2: Xử lý các thông tin rủi ro**

Bạch Mã chỉ là lựa chọn phải kiểm tra trạng thái tuyến với Ban quản lý. SUP chỉ
giữ yêu cầu áo phao, thiết bị cứu sinh và tránh luồng tàu. Khả năng tiếp cận
được diễn đạt theo nhu cầu liên hệ trước, không bảo đảm điều kiện hạ tầng.

- [x] **Bước 3: Viết lại Mục XL**

Giữ phần phạm vi, nguồn trực tiếp, bảng kiểm chứng và quyết định biên tập bằng
tiếng Việt tự nhiên. Xóa bảng toplist, homepage, lời tự nghiệm thu và mọi record
không còn nội dung tương ứng trong cẩm nang.

- [x] **Bước 4: Kiểm tra riêng Task 2**

Chạy:

```bash
wc -l 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md'
rg -n 'https?://|\[\[|\.md\b|^---$|^## Nguồn dữ liệu' 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md'
git diff --no-index --check /dev/null 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md'
```

Kỳ vọng: khoảng 120–180 dòng; lệnh `rg` không có kết quả; kiểm tra no-index
không in lỗi whitespace và có thể trả exit 1 vì file khác `/dev/null`.

---

### Task 3: Viết lại lịch trình ngắn ngày và Mục XLI

**Files:**

- Viết lại: `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md`.
- Viết lại: Mục XLI trong evidence.

- [x] **Bước 1: Viết đúng outline**

```markdown
# Lịch trình du lịch Huế ngắn ngày

## Nguyên tắc xếp lịch trình Huế ngắn ngày
## Lịch trình Huế nửa ngày
## Lịch trình Huế một ngày
## Lịch trình Huế hai ngày một đêm
## Điều chỉnh lịch trình theo điểm đến và điểm rời Huế
## Điều chỉnh lịch trình theo thời tiết
## Lịch trình cho gia đình và người hạn chế vận động
## Checklist trước khi khởi hành
```

Mỗi lịch trình dùng đầu/giữa/cuối buổi, thời lượng tương đối và khoảng đệm.
Biến thể ga Huế, sân bay Phú Bài hoặc Đà Nẵng chỉ nêu khác biệt tuyến, không
khóa giờ tàu, giờ bay hoặc giờ đồng hồ cụ thể.

- [x] **Bước 2: Giảm nội dung liên domain**

Chỉ nêu tên loại bữa ăn, điểm di sản hoặc trải nghiệm biểu diễn khi cần xác
định nhịp hành trình. Không mô tả món, hiện vật, kiến trúc hoặc tiết mục.

- [x] **Bước 3: Xử lý an toàn và tiếp cận**

Hoạt động đường thủy luôn có điều kiện thời tiết và thông báo vận hành. Nhóm có
nhu cầu tiếp cận đặc thù được hướng dẫn liên hệ điểm đến, không nhận các bảo
đảm về bãi đỗ, bậc cấp, đường dốc hoặc xe điện.

- [x] **Bước 4: Viết lại Mục XLI và kiểm tra**

Chỉ giữ nguồn trực tiếp cho thông tin thực sự xuất hiện. Chạy:

```bash
rg -n '[0-2]?[0-9]:[0-5][0-9]|[0-2]?[0-9]h[0-5]?[0-9]?' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md'
rg -n 'https?://|\[\[|\.md\b|^---$|^## Nguồn dữ liệu' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md'
git diff --no-index --check /dev/null 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md'
```

Kỳ vọng: hai lệnh `rg` không có kết quả; no-index không in lỗi whitespace.

---

### Task 4: Viết lại lịch trình ba ngày hai đêm và Mục XLII

**Files:**

- Viết lại: `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md`.
- Viết lại: Mục XLII trong evidence.

- [x] **Bước 1: Viết lịch trình mặc định**

Dùng một lịch trình duy nhất:

1. Ngày 1: lõi Phú Xuân–Thuận Hóa và hai bờ sông Hương;
2. Ngày 2: Kim Long–Thủy Xuân;
3. Ngày 3: chọn một nhánh nhẹ, phù hợp điểm rời Huế.

Mỗi ngày dùng khung buổi, thời lượng tương đối, nhịp nghỉ và phương án cắt bớt.

- [x] **Bước 2: Viết tối đa ba module thay thế**

Các module là biển–đầm phá, làng nghề–nghỉ dưỡng và gia đình có người hạn chế
vận động. Mỗi module nêu phần lịch trình được thay, điều kiện áp dụng và yêu
cầu kiểm tra. Không tạo thêm một lịch trình đầy đủ song song.

- [x] **Bước 3: Khóa Bạch Mã và khả năng tiếp cận**

Không đưa Bạch Mã vào lịch trình/module mặc định, không nêu tuyến cụ thể hoặc
giá xe. Chỉ hướng dẫn liên hệ Ban quản lý. Xóa các khẳng định xe đỗ sát, nền
phẳng, số bậc, đường dốc và xe điện nếu không có nguồn trực tiếp.

- [x] **Bước 4: Viết lại Mục XLII và kiểm tra**

```bash
rg -n 'Hải Vọng Đài|Ngũ Hồ|Thác Đỗ Quyên|Trĩ Sao|Vườn thực vật|xe vận chuyển chuyên dụng' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md'
rg -n '[0-2]?[0-9]:[0-5][0-9]|[0-2]?[0-9]h[0-5]?[0-9]?' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md'
rg -n 'https?://|\[\[|\.md\b|^---$|^## Nguồn dữ liệu' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md'
git diff --no-index --check /dev/null 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md'
```

Kỳ vọng: các lệnh `rg` không có kết quả; no-index không in lỗi whitespace.

---

### Task 5: Viết lại cẩm nang chi phí và Mục XLIII

**Files:**

- Viết lại: `knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md`.
- Viết lại: Mục XLIII trong evidence.

- [x] **Bước 1: Viết cấu trúc ngân sách**

```markdown
# Chi phí du lịch Huế

## Cách tính tổng ngân sách du lịch Huế
## Tách chi phí đến Huế và chi phí tại Huế
## Các đầu vào dùng để lập ngân sách
## Dự toán một ngày tại Huế
## Dự toán hai ngày một đêm tại Huế
## Dự toán ba ngày hai đêm tại Huế
## Điều chỉnh ngân sách theo quy mô nhóm
## Quỹ dự phòng và thông tin cần kiểm tra lại
```

Giữ không quá mười nhóm đầu vào. Vé tham quan chỉ là một khoản dự toán tổng có
mốc khảo sát; chính sách và biểu phí chi tiết được điều phối sang cẩm nang vé.

- [x] **Bước 2: Tạo ba bảng dự toán không lặp**

Mỗi bảng có ba mức chi tiêu và cùng một nhóm hạng mục. Mọi tổng thấp/cao phải
bằng đúng tổng các thành phần. Chi phí đến Huế không được cộng ngầm vào chi
phí tại Huế.

- [x] **Bước 3: Viết lại Mục XLIII**

Mỗi khoảng giá trong cẩm nang phải xuất hiện đúng một lần trong bảng bằng
chứng cùng URL trực tiếp, chủ thể, ngày nguồn, ngày truy cập và phạm vi. Xóa
giá Ca Huế, taxi, thuyền riêng, hướng dẫn viên hoặc dịch vụ khác nếu không có
nguồn trực tiếp khớp khoảng giá.

- [x] **Bước 4: Tính lại và kiểm tra**

Dùng lệnh `awk` viết đầy đủ từ các số đã chốt trong Task 1 để cộng riêng từng
cận thấp và cao. Ghi chính lệnh cùng output vào implementation report. Sau đó
chạy:

```bash
rg -n 'https?://|\[\[|\.md\b|^---$|^## Nguồn dữ liệu' 'knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md'
git diff --no-index --check /dev/null 'knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md'
```

Kỳ vọng: `rg` không có kết quả; các tổng tính lại khớp bảng; no-index không in
lỗi whitespace.

---

### Task 6: Kiểm tra chéo, báo cáo và handoff

**Files:**

- Đọc lại: bốn guide và Mục XL–XLIII.
- Tạo: `reports/services_batches_01_03_minimal_reset_implementation_report_2026_09_08.md`.
- Cập nhật: `session_prompt/CURRENT_HANDOFF.md`.

- [x] **Bước 1: Đọc lại toàn bộ artifact**

So sánh từng thông tin động, an toàn, địa giới, pháp lý và giá giữa cẩm nang và
evidence bằng nội dung tự nhiên. Xóa hoặc sửa mọi record không còn khớp.

- [x] **Bước 2: Chạy kiểm tra toàn phạm vi**

```bash
wc -l 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md' 'knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md' knowledge-base-hue/meta/tourism-research-evidence.md
rg -n 'https?://|\[\[|\.md\b|^---$|^## Nguồn dữ liệu' 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md' 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md' 'knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md'
sed -n '/^## XL\./,$p' knowledge-base-hue/meta/tourism-research-evidence.md | rg -n -i 'thực địa|dây leash|Hải Vọng Đài|Ngũ Hồ|Thác Đỗ Quyên|xe vận chuyển chuyên dụng'
git diff --check
git diff --no-index --check /dev/null 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md'
git diff --no-index --check /dev/null 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md'
git diff --no-index --check /dev/null 'knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md'
git diff --no-index --check /dev/null 'knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md'
git diff --no-index --check /dev/null knowledge-base-hue/meta/tourism-research-evidence.md
git diff --no-index --check /dev/null reports/services_batches_01_03_minimal_reset_implementation_report_2026_09_08.md
```

Đếm H1/H2/H3 của từng guide, kiểm tra mỗi file kết thúc bằng một LF và tính lại
tất cả tổng ngân sách. Ghi đúng rằng `git diff --check` không bao phủ file
untracked và no-index có thể trả exit 1 vì file khác `/dev/null`.

- [x] **Bước 3: Viết implementation report**

Report gồm phạm vi, thay đổi theo từng guide, nguồn đã dùng, command thực chạy,
observed result, phần chưa xác minh, quyền và next action. Không tự gắn nhãn
nghiệm thu và không dùng tuyên bố tuyệt đối.

- [x] **Bước 4: Cập nhật handoff**

Chuyển target role sang reviewer, trỏ tới spec, plan, implementation report,
bốn guide và Mục XL–XLIII. Giữ Git/sub-agent authorization là `none` và next
action duy nhất là review độc lập.

- [x] **Bước 5: Kiểm tra chính report và handoff**

Chạy `git diff --check` lần cuối và no-index check cho report mới. Không commit
hoặc push.
