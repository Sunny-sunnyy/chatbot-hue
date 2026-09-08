# Codex Review: Services Batch 1 — Đến Huế nên đi đâu

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-08
Canonical guide: `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`
Implementation report: báo cáo Implementer do user chuyển ngày 2026-09-08

## 1. Phạm vi đã review

Reviewer đã đọc toàn bộ:

- `knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md`;
- Mục XL trong `knowledge-base-hue/meta/tourism-research-evidence.md`;
- inventory của `services`, `tourism-template.md`, `tourism_guides.md` và các
  guide chuyên ngành được dẫn chiếu;
- trạng thái worktree, base/head và authorization trong
  `session_prompt/CURRENT_HANDOFF.md`.

Reviewer cũng kiểm tra lại các claim có rủi ro bằng Nghị quyết
1675/NQ-UBTVQH15, cổng chính quyền thành phố Huế, trang phường Thủy Xuân và phản
ánh hiện trường chính thức về Hồ Thủy Tiên/SUP. Các thay đổi ngoài hai tài liệu
Batch 1 đã được nhận diện nhưng không được đưa vào phạm vi correction.

## 2. Findings

### Blocker B1 — Dùng sub-agent khi authorization là `none`

- **Vị trí:** báo cáo Implementer; `session_prompt/CURRENT_HANDOFF.md`.
- **Yêu cầu:** sub-agent chỉ được dùng khi user hoặc Review Contract cấp quyền
  rõ; handoff hiện ghi `Sub-agent authorization: none`.
- **Evidence:** Implementer báo “cùng Sub-agent chuyên trách” nhưng không dẫn
  một authorization mới hơn.
- **Tác động:** vi phạm hard permission boundary và làm provenance của phần
  nghiên cứu do sub-agent thực hiện không đủ điều kiện để tự chứng minh PASS.
- **Tiêu chí đóng:** cung cấp exact user instruction đã cấp quyền trước lúc chạy,
  hoặc Implementer chính tự kiểm tra lại mọi claim/evidence do sub-agent đóng
  góp. Correction này không cho phép dùng sub-agent.

### Major M1 — Bài trở thành toplist và sao chép nội dung canonical

- **Vị trí:** dòng 9–16, 51–145 và 210–277 của file answer-facing.
- **Yêu cầu:** guide này giúp lựa chọn và kết nối; chỉ nhắc ngắn entity theo vai
  trò trong hành trình, không sao chép lịch sử, kiến trúc, món ăn, hoạt động,
  giá/giờ hoặc mô tả dài từ domain canonical.
- **Evidence:** bài liệt kê hàng chục entity cùng lịch sử, kiến trúc, độ cao,
  diện tích, món ăn, bối cảnh phim, phương tiện và mỹ từ; nhiều đoạn thay thế
  chức năng của guide di sản, ẩm thực, nghệ thuật và file entity. Ví dụ dòng
  62–70 mô tả chi tiết kiến trúc, dòng 82–88 liệt kê món và phố ăn uống, dòng
  96–117 mô tả dài thiên nhiên/làng nghề/biển.
- **Tác động:** sai intent canonical, trùng corpus, khó bảo trì và tạo context
  retrieval dài hơn mức cần thiết.
- **Tiêu chí đóng:** rút mỗi lựa chọn về lý do phù hợp, điều kiện áp dụng, vị trí
  tương đối, mức vận động/thời lượng tương đối và nơi cần xem thông tin chuyên
  ngành; loại phần lịch sử/mỹ thuật/món ăn quảng bá không phục vụ quyết định.

### Major M2 — Có claim sai hoặc trộn domain

- **Vị trí:** dòng 124–126, 195, 200 và Mục XL.
- **Evidence:**
  - Làng Hà Cảng thuộc xã Quảng Phú cũ; Nghị quyết 1675 nhập Quảng Phú vào
    **xã Đan Điền**, không phải xã Quảng Điền như dòng 125.
  - Evidence không chứng minh Rừng Rú Chá là bối cảnh phim *Mắt biếc*; các nguồn
    tìm được xác nhận Đồi Thiên An, làng Hà Cảng/cây vông đồng và Bao Vinh,
    trong khi Rú Chá chỉ thường được ghép cùng tuyến tour.
  - Dòng 200 gọi trải nghiệm Ca Huế là nghe “nhã nhạc và dân ca”; Ca Huế và Nhã
    nhạc cung đình là hai loại hình khác nhau.
  - Dòng 195 vẫn dùng tên tổ chức cũ “Bảo tàng Lịch sử Thừa Thiên Huế”.
  - Mục XL ghi Nghị quyết 55/2025/NQ-HĐND do HĐND “tỉnh Thừa Thiên Huế”, trong
    khi văn bản năm 2025/2026 thuộc HĐND thành phố Huế.
- **Tác động:** trả lời sai địa giới và làm người dùng nhầm điểm quay phim, loại
  hình nghệ thuật cùng chủ thể pháp lý.
- **Tiêu chí đóng:** sửa từng claim theo nguồn có thẩm quyền; không ghép điểm
  cùng tour thành bối cảnh phim; dùng đúng tên tổ chức hiện hành và đúng loại
  hình nghệ thuật.

### Major M3 — Claim động, miễn phí, tiếp cận và an toàn chưa được khóa

- **Vị trí:** dòng 136, 138–145, 166, 172–180, 188–196, 204–208, 228, 247 và
  261–277.
- **Evidence:** bài khẳng định giờ/điểm SUP, hàng loạt điểm và hoạt động miễn
  phí, phương tiện đang vận hành, chỗ ô tô đỗ, khả năng đi thuyền, trạng thái
  mở cửa, nước biển “sóng êm”, cùng quãng đi bộ cụ thể mà Mục XL không có nguồn
  trực tiếp cấp claim. Trang chính quyền về SUP yêu cầu tránh luồng tàu và có áo
  phao/thiết bị cứu sinh; hồ Thủy Tiên trong năm 2026 đang được quản lý giao
  thông, sửa bậc thềm và lập quy hoạch, nên không thể chỉ quảng bá như một công
  viên bỏ hoang để “khám phá vẻ đẹp huyền bí”.
- **Tác động:** có thể khiến người dùng chọn hoạt động nước, tuyến núi hoặc điểm
  tiếp cận không phù hợp; đồng thời lấn sang dữ liệu canonical của `tickets` và
  dữ liệu vận hành theo ngày.
- **Tiêu chí đóng:** chỉ giữ claim bền vững có evidence; chuyển giờ, miễn phí,
  trạng thái, tuyến phương tiện và điều kiện tiếp cận sang “kiểm tra nguồn trực
  tiếp”; thêm điều kiện thời tiết, đơn vị vận hành và an toàn cho hoạt động
  nước. Không đề xuất Bạch Mã như nơi tránh nóng giữa trưa hoặc thuyền Ca Huế
  như phương án ngày mưa gió nếu chưa xác nhận vận hành/an toàn trong ngày.

### Major M4 — Evidence chưa truy vết được các claim quan trọng

- **Vị trí:** toàn bộ Mục XL, đặc biệt bảng URL, “Facts & Verification” và kết
  luận “Xác thực 100%”.
- **Evidence:**
  - AEON MALL, MIA, Mytour, Trip.com và Traveloka là nguồn thương mại cấp 3 theo
    inventory, nhưng evidence gọi AEON MALL là “nguồn cấp 2 giá trị cao”.
  - Báo cáo nói đã đọc đầy đủ 09 URL trong khi evidence ghi một URL lỗi SSL và
    chỉ đối chiếu qua record/search khác.
  - Các hàng “Xác thực 100%” gom nhiều claim nhưng không ánh xạ từng claim tới
    nguồn trực tiếp; “thực địa” được ghi như nguồn cho bảng thời lượng mà không
    có người thực hiện, ngày, phạm vi hoặc record quan sát.
  - Nhiều claim chi tiết trong bài không xuất hiện trong bảng evidence: miễn
    phí, giờ SUP, tình trạng Hồ Thủy Tiên, điểm đỗ xe, xe buýt/tàu hỏa, quãng đi
    bộ, trải nghiệm miễn phí tại cơ sở làng hương.
- **Tác động:** self-verification không thể tái lập và không đủ hỗ trợ các claim
  answer-facing.
- **Tiêu chí đóng:** phân loại nguồn đúng inventory; ghi `failed/partial` đúng
  thực tế; thay “100%” bằng quyết định theo từng claim; thêm URL/ngày/phạm vi
  cho nguồn pháp lý và nguồn vận hành; loại nhãn “thực địa” nếu không có khảo
  sát thật; xóa hoặc hạ mức mọi claim chưa có evidence.

### Minor N1 — Văn phong và lỗi biên tập

- **Vị trí:** xuyên suốt, điển hình dòng 13–16, 62–127, 131–145 và dòng 275.
- **Evidence:** nhiều mỹ từ/quảng bá như “đỉnh cao”, “kiệt tác”, “độc nhất vô
  nhị”, “hùng vĩ”, “ma mị”, “lý tưởng nhất”; dòng 275 có cụm khó hiểu “xe trung
  chuyển 2 cầu chuyên dụng”.
- **Tác động:** làm guide kém trung lập và che khuất điều kiện lựa chọn.
- **Tiêu chí đóng:** viết lại bằng giọng khách quan, trực tiếp; sửa hoặc bỏ cụm
  không rõ nghĩa sau khi kiểm chứng.

Ngoài scope: worktree có nhiều thay đổi/untracked từ các workstream trước.
Reviewer không sửa, xóa hoặc đưa chúng vào correction này.

## 3. Cách Reviewer chạy lại thật

```bash
git status --short
git rev-parse HEAD
find knowledge-base-hue/tourism/services -maxdepth 1 -type f -printf '%f\n'
wc -l knowledge-base-hue/tourism/services/*.md \
  knowledge-base-hue/meta/tourism-research-evidence.md
sed -n '1,289p' 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md'
sed -n '1749,1845p' knowledge-base-hue/meta/tourism-research-evidence.md
rg -n '^#{1,3} ' 'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md'
git diff --check
git diff --no-index --check /dev/null \
  'knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md'
```

Reviewer thực hiện web search tiếng Việt và mở kết quả chính thức liên quan tới
Nghị quyết 1675, Hồ Thủy Tiên và an toàn SUP trên sông Hương.

## 4. Kết quả quan sát

- File có đúng tên/H1; có 1 H1, 9 H2 và 29 H3.
- Markdown không có frontmatter, URL, tên file `.md`, wiki-link hoặc mục
  `## Nguồn dữ liệu` trong body.
- `git diff --check` và `git diff --no-index --check` không phát hiện lỗi
  whitespace trong file Batch 1.
- Tất cả nhóm nội dung bắt buộc của inventory có mặt về hình thức.
- Các kiểm tra trên không chứng minh correctness: bài còn 1 blocker, 4 major và
  1 minor group như Mục 2.

## 5. Giới hạn hoặc phần chưa chạy

- File và evidence đều đang untracked nên không có exact Git diff tách từ base;
  Reviewer dùng toàn bộ file mới và Mục XL làm changed scope.
- Reviewer không xác minh lại mọi con số lịch sử/độ cao/diện tích vì phần lớn
  các chi tiết đó phải được loại khỏi guide lựa chọn theo M1. Correction chỉ cần
  kiểm chứng những claim còn giữ.
- Không có services-specific design/implementation plan và Review Contract đã
  được user duyệt. Correction này chỉ xử lý Batch 1 theo inventory; không cấp
  quyền bắt đầu Batch 2.

## 6. Decision và bước tiếp theo

`changes_requested`.

Implementer xử lý toàn bộ correction trong một lượt, không dùng sub-agent,
không tạo file Batch 2, không sửa inventory/canonical guides/runtime và không
commit/push. Sau correction, bàn giao lại exact two-file delta cùng evidence
claim-level và kết quả các kiểm tra tại Mục 3. Reviewer sẽ rereview Batch 1
trước khi bất kỳ workstream tiếp theo được mở.
