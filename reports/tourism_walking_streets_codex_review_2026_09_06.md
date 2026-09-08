# Codex Review: Phố đi bộ & Phố đêm (Nguyễn Đình Chiểu, Khu phố Tây Huế, Hai Bà Trưng)

Decision: changes_requested  
Reviewer: Codex (Reviewer Agent & Sub-agents Team)  
Date: 2026-09-06  
Canonical guide: `knowledge-base-hue/meta/tourism-template.md` & `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`  
Implementation evidence: `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục VIII, IX, X)

---

## 1. Phạm vi đã review

Reviewer và 3 sub-agent chuyên trách đã hoàn thành thẩm định độc lập, tra cứu xác thực thực địa bằng web search tiếng Việt mốc tháng 09/2026, đối soát tiêu chuẩn Markdown RAG Clean và hồ sơ kiểm chứng đối với 3 tệp thực thể phố đi bộ:
- `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Phố đi bộ Nguyễn Đình Chiểu.md`
- `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Khu phố Tây Huế.md`
- `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Phố đi bộ Hai Bà Trưng.md`
- Hồ sơ kiểm chứng tại: `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục VIII, IX, X)

Nội dung đối soát chuyên sâu:
1. **Địa giới hành chính mốc tháng 09/2026:** Nghị quyết số 175/2024/QH15 và Nghị quyết số 1675/NQ-UBTVQH15 (hiệu lực 01/07/2025). Cả 3 tuyến phố đều đã được sáp nhập chính xác về **phường Thuận Hóa, quận Thuận Hóa, thành phố Huế**.
2. **Xác thực dữ kiện lịch sử, hạ tầng & quy hoạch:** Đối chiếu ngày khai trương, chiều dài tuyến, dự án tài trợ (KOICA), tổng mức đầu tư, các mốc thời gian quy hoạch và tháo dỡ công trình.
3. **Quy chế giao thông & Vận hành thực tế:** Đối chiếu cơ chế cấm xe, khung giờ đi bộ, phân luồng giao thông và vị trí các bãi giữ xe tiếp cận.
4. **Tiêu chuẩn Markdown RAG Clean:** H1 mở đầu, không YAML frontmatter, không wiki-links `[[]]`, không thuật ngữ nội bộ RAG (`chunk`, `canonical`, `metadata`), tính độc lập của tiêu đề H2/H3 (Chunk self-containment) và văn phong bách khoa khách quan.

---

## 2. Findings

### 2.1. Blocker (2 findings)

#### Finding B-01 [BLOCKER]: Mô tả sai thực tế chuỗi nhà rường gỗ đã bị tháo dỡ từ năm 2018 tại Phố đi bộ Nguyễn Đình Chiểu
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Phố đi bộ Nguyễn Đình Chiểu.md`, Dòng 18, Dòng 35–42, Dòng 64, Dòng 98, Dòng 131; và `knowledge-base-hue/meta/tourism-research-evidence.md` Dòng 299, 313.
- **Hiện trạng:** Tệp dành riêng cả H3 `### Không gian kiến trúc nhà rường gỗ truyền thống trên Phố đi bộ Nguyễn Đình Chiểu` (Dòng 35–42) và liên tục nhắc đến việc các tiểu thương dọn hàng vào các gian nhà rường gỗ, coi đây là nét kiến trúc nổi bật hiện hữu dọc tuyến phố.
- **Evidence đối chiếu:** Hệ thống 11–13 căn nhà rường gỗ do Huetourist khai thác từ năm 2015 đã được UBND thành phố Huế thông báo thu hồi mặt bằng và **tháo dỡ hoàn toàn vào tháng 5/2018** để giải phóng mặt bằng, tạo không gian mở phục vụ dự án KOICA (xây cầu gỗ lim và chỉnh trang dải công viên bờ sông Hương) *(Báo Thanh Niên 21/05/2018, Cổng TTĐT TP. Huế hue.gov.vn)*. Từ năm 2019 đến nay, tuyến phố là không gian cảnh quan mở, kết nối trực tiếp với cầu gỗ lim; thành phố chỉ bố trí các cụm ki-ốt gỗ gọn nhẹ đồng bộ.
- **Tác động:** Sai lệch nghiêm trọng về hiện trạng thực tế công trình kiến trúc, khiến hệ thống RAG tạo câu trả lời sai sự thật cho du khách.
- **Tiêu chí đóng:**
  1. Đưa thông tin chuỗi nhà rường gỗ về đúng bối cảnh lịch sử giai đoạn 2015–2018, ghi rõ đã tháo dỡ tháng 5/2018.
  2. Đổi tên H3 thành `### Cảnh quan không gian mở và hạ tầng phục vụ du khách trên Phố đi bộ Nguyễn Đình Chiểu`, mô tả không gian mở thông thoáng hiện hữu và hệ thống ki-ốt nhỏ gọn.
  3. Cập nhật hồ sơ kiểm chứng tại Mục VIII của `tourism-research-evidence.md`.

#### Finding B-02 [BLOCKER]: Chỉ dẫn gửi xe sai thực tế nghiêm trọng tại Khu phố Tây Huế
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Khu phố Tây Huế.md`, Dòng 82.
- **Hiện trạng:** Hướng dẫn du khách trong khung giờ cấm xe gửi xe tại: `...các bãi đỗ xe công cộng được cấp phép bố trí tại các tuyến tiếp cận lân cận (đường Phạm Ngũ Lão, đường Lê Quý Đôn, đường Đội Cung hoặc bãi xe của các khách sạn lớn gần kề)...`
- **Evidence đối chiếu:** Đường Phạm Ngũ Lão là một trong ba trục xương sống của phố đi bộ, bị **cấm hoàn toàn tất cả phương tiện lưu thông và dừng đỗ từ 18:00** (lực lượng chức năng lập barie chốt chặn hai đầu). Hướng dẫn du khách vào đường Phạm Ngũ Lão để gửi xe là mâu thuẫn trực tiếp với phương án phân luồng giao thông của thành phố Huế.
- **Tác động:** Chỉ dẫn sai thực tế điều hành giao thông đô thị, gây cản trở cho du khách khi tra cứu lịch trình di chuyển.
- **Tiêu chí đóng:** Xóa bỏ "đường Phạm Ngũ Lão" khỏi danh sách tuyến gửi xe tiếp cận, thay bằng các trục ngoại vi hợp lệ: đường Nguyễn Thái Học, đường Đội Cung, đường Lê Quý Đôn, đường Bến Nghé, đường Lê Lợi hoặc các bãi xe trung tâm thương mại gần kề.

---

### 2.2. Major (5 findings)

#### Finding M-01 [MAJOR]: Sai quy định phân luồng giao thông và hoạt động đạp xe tại Phố đi bộ Nguyễn Đình Chiểu
- **Vị trí:** `Phố đi bộ Nguyễn Đình Chiểu.md`, Dòng 96 và Dòng 123.
- **Hiện trạng:** Dòng 96 ghi ban ngày người dân "đạp xe"; Dòng 123 ghi cấm xe "trong khung giờ phố đi bộ hoạt động".
- **Evidence đối chiếu:** Khác với Khu phố Tây hay Hai Bà Trưng là đường giao thông hỗn hợp ban ngày, tuyến đường dạo ven sông Nguyễn Đình Chiểu là tuyến dạo bộ công viên chuyên trách, **cấm tuyệt đối toàn bộ phương tiện cơ giới và cấm cả xe đạp lưu thông thường trực 24/24** *(Hệ thống tương tác đô thị thông minh Hue-S, Trung tâm Công viên Cây xanh Huế)*.
- **Tác động:** Sai quy định an toàn giao thông đô thị đối với tuyến dạo bộ bờ sông Hương.
- **Tiêu chí đóng:** Bỏ cụm từ "đạp xe" tại dòng 96; đính chính tại dòng 123: tuyến đường cấm hoàn toàn ô tô, xe máy và xe đạp 24/24.

#### Finding M-02 [MAJOR]: Nhầm lẫn vị trí địa lý của Bến thuyền Tòa Khâm
- **Vị trí:** `Phố đi bộ Nguyễn Đình Chiểu.md`, Dòng 10, Dòng 30, Dòng 58, Dòng 88.
- **Hiện trạng:** Mô tả bến thuyền du lịch Tòa Khâm nằm "ngay dưới chân cầu Trường Tiền", "ngay sát tuyến phố là bến đỗ của các thuyền rồng... sau khi tản bộ dễ dàng bước xuống thuyền".
- **Evidence đối chiếu:** Tuyến phố đi bộ Nguyễn Đình Chiểu nằm từ cầu Phú Xuân đến mố nam cầu Trường Tiền (nằm hoàn toàn ở phía tây cầu Trường Tiền). Bến thuyền Tòa Khâm có địa chỉ chính thức tại **số 49 đường Lê Lợi**, nằm ở bờ nam nhưng ở phía **đông (hạ lưu) cầu Trường Tiền**, cách mố cầu khoảng 200–300 m. Ngay chân cầu phía tây chỉ có công viên Tứ Tượng và bậc tam cấp ngắm cảnh.
- **Tác động:** Sai lệch vị trí bến thuyền du lịch đường thủy lớn nhất Cố đô.
- **Tiêu chí đóng:** Đính chính rõ: tuyến phố kết thúc ở mố nam cầu Trường Tiền; du khách đi tiếp theo đường dạo bờ sông qua bên kia cầu Trường Tiền để đến Bến thuyền du lịch Tòa Khâm tại số 49 Lê Lợi.

#### Finding M-03 [MAJOR]: Sai thứ tự lịch sử quy hoạch phố đi bộ tại Khu phố Tây Huế
- **Vị trí:** `Khu phố Tây Huế.md`, Dòng 16.
- **Hiện trạng:** Ghi nhận sự kiện khai trương ngày 29/09/2017: `...thành tuyến phố đi bộ đêm cuối tuần quy mô đầu tiên ở bờ nam Cố đô.`
- **Evidence đối chiếu:** Tuyến phố đi bộ Nguyễn Đình Chiểu (ven bờ nam sông Hương) đã hoạt động từ 2012 và chỉnh trang quy củ năm 2015. Tuyến phố đi bộ Chu Văn An – Phạm Ngũ Lão – Võ Thị Sáu năm 2017 là **tuyến phố đi bộ thứ hai của thành phố Huế** (và là tuyến phố đi bộ dịch vụ nightlife thứ hai ở bờ nam) *(Báo VOV, Dân Trí, Cổng TTĐT TP. Huế)*.
- **Tác động:** Sai lệch lịch sử phát triển đô thị và hệ thống phố đi bộ của Cố đô.
- **Tiêu chí đóng:** Sửa thành: `...thành tuyến phố đi bộ thứ hai của thành phố Huế (sau tuyến phố đi bộ Nguyễn Đình Chiểu) và là tâm điểm giải trí đêm cuối tuần quy mô lớn ở khu vực bờ nam Cố đô.`

#### Finding M-04 [MAJOR]: Sai cự ly thực tế giữa Khu phố Tây và Cầu Tràng Tiền
- **Vị trí:** `Khu phố Tây Huế.md`, Dòng 81.
- **Hiện trạng:** `...cách đường Lê Lợi vài bước chân, cách cầu Tràng Tiền và ga Huế từ 1 km đến 2 km...`
- **Evidence đối chiếu:** Tuyến Chu Văn An và Phạm Ngũ Lão nối thẳng ra đường Lê Lợi kề cận bờ sông Hương. Từ nút giao Chu Văn An – Lê Lợi đi bộ đến mố cầu Tràng Tiền chỉ khoảng **300 m đến 500 m** (khoảng 3–5 phút đi bộ). Cự ly 1–2 km là khoảng cách đến Ga Huế. Cách viết hiện tại làm người đọc hiểu sai khoảng cách thực tế và mâu thuẫn với chính dòng 30 của bài viết.
- **Tác động:** Sai dữ kiện cự ly không gian tiếp cận.
- **Tiêu chí đóng:** Tách rõ: `...cách cầu Tràng Tiền khoảng 300–500 m, cách ga Huế khoảng 2 km...`

#### Finding M-05 [MAJOR]: Mất ngữ cảnh độc lập của chunk (Chunk Standalone Context Loss) tại Phố đi bộ Hai Bà Trưng
- **Vị trí:** `Phố đi bộ Hai Bà Trưng.md`, Dòng 107 và Dòng 113.
- **Hiện trạng:**
  - Dòng 107: `- **Chỗ nghỉ chân:** Toàn tuyến phố được trang bị hệ thống ghế băng dài bằng gỗ...`
  - Dòng 113: `- **Bảo đảm trật tự:** Tuyến phố có lực lượng công an phường Thuận Hóa, lực lượng bảo vệ đô thị túc trực thường xuyên...`
- **Evidence đối chiếu:** Khi chunk được vector database trích xuất độc lập theo các H3 `### Tiện ích công cộng và vệ sinh môi trường` hoặc `### An ninh trật tự và quy tắc ứng xử`, câu mở đầu chỉ dùng đại từ "Toàn tuyến phố" / "Tuyến phố" làm mất hoàn toàn chủ thể nhận diện của thực thể.
- **Tác động:** Giảm độ chuẩn xác khi RAG trả lời các câu hỏi truy vấn riêng về tiện ích hoặc an ninh tại Huế.
- **Tiêu chí đóng:** Bổ sung rõ danh xưng thực thể:
  - Dòng 107: `- **Chỗ nghỉ chân:** Toàn tuyến Phố đi bộ Hai Bà Trưng được trang bị...`
  - Dòng 113: `- **Bảo đảm trật tự:** Khu vực Phố đi bộ Hai Bà Trưng được lực lượng công an phường Thuận Hóa...`

---

### 2.3. Minor (7 findings)

1. **Finding m-01 (`Phố đi bộ Hai Bà Trưng.md` - Dòng 17, 55, 61, 65, 67):** Tinh giản văn phong biểu cảm, ẩm thực dồn dập tính từ vị giác kiểu review du lịch ("trọng thể", "linh hồn tạo nên sức hút", "thế giới ẩm thực", "giòn rụm, mềm mịn, trong suốt, dẻo giòn, bùi béo").
2. **Finding m-02 (`Phố đi bộ Hai Bà Trưng.md` - Dòng 40):** Sửa cụm từ "đặc sản ba miền" thành "sản phẩm OCOP và đặc sản xứ Huế" để đúng định hướng quy hoạch không gian văn hóa địa phương.
3. **Finding m-03 (`Phố đi bộ Hai Bà Trưng.md` - Dòng 17/29):** Bổ sung mốc khởi công chỉnh trang hạ tầng kỹ thuật (tháng 09/2022) trước khi khai trương ngày 26/03/2023.
4. **Finding m-04 (`Phố đi bộ Nguyễn Đình Chiểu.md` - Dòng 11):** Bổ sung **Trung tâm Công viên Cây xanh Huế** vào danh sách cơ quan quản lý trực tiếp hạ tầng, cây xanh và cảnh quan dạo bộ ven sông.
5. **Finding m-05 (`Phố đi bộ Nguyễn Đình Chiểu.md` - Dòng 22, 43, 60, 90):** Thêm từ khóa "Phố đi bộ Nguyễn Đình Chiểu" vào các tiêu đề H2/H3 để bảo toàn 100% tính độc lập chunking.
6. **Finding m-06 (`Phố đi bộ Nguyễn Đình Chiểu.md` - Dòng 16, 49, 96):** Tinh giản văn phong cảm thán, trữ tình ("điểm đến quen thuộc khi màn đêm buông xuống", "lướt đi trên mặt sóng", "dòng sông xanh trong vắt").
7. **Finding m-07 (`Khu phố Tây Huế.md` - Dòng 16, 44, 57, 66 & Evidence Dòng 349):** Thay các mỹ từ cảm tính ("nổi tiếng bậc nhất", "linh hồn của", "đa dạng bậc nhất", "đông vui nhất") bằng các từ ngữ trung tính ("sầm uất hàng đầu", "nét đặc trưng định hình", "rất đa dạng", "tập trung đông đúc du khách"), và đồng bộ đính chính lại dòng 349 trong `tourism-research-evidence.md`.

---

## 3. Cách Reviewer chạy lại thật

- Tra cứu web search độc lập theo thời gian thực (real-time live verification) với các nguồn thẩm quyền:
  + Cổng TTĐT TP. Huế (`hue.gov.vn`), Hệ thống tương tác thông minh Hue-S (`tuongtac.hue.gov.vn`).
  + Các văn bản pháp quy: Nghị quyết 175/2024/QH15 của Quốc hội, Nghị quyết 1675/NQ-UBTVQH15 của UBTVQH.
  + Báo chí chính thống: Báo Nhân Dân, Báo Tuổi Trẻ, Báo Thanh Niên, Báo Lao Động, Đài Tiếng nói Việt Nam (VOV), Cục Du lịch Quốc gia Việt Nam (`vietnamtourism.gov.vn`).
- Chạy kiểm tra định dạng và khoảng trắng kho mã:
  + `git status --short`
  + `git diff --check`
- Toàn bộ kết quả đều đối chiếu trực tiếp trên văn bản nguồn thật, không dùng dữ liệu mô phỏng.

---

## 4. Kết quả quan sát

- **Địa giới hành chính:** 100% tệp đã cập nhật chuẩn xác đơn vị hành chính cấp phường/quận mới nhất mốc 09/2026: phường Thuận Hóa, quận Thuận Hóa, thành phố Huế.
- **Chất lượng chung:** Cả 3 tệp đều được viết rất công phu, cấu trúc rõ ràng, dung lượng tri thức dồi dào, đáp ứng tốt khung `tourism-template.md`.
- **Tuy nhiên:** Việc dựa vào các bài viết cẩm nang cũ mà không đối soát thời điểm đã dẫn tới 2 sai sót nghiêm trọng về hiện trạng (Blocker): chuỗi nhà rường Nguyễn Đình Chiểu đã dỡ bỏ từ năm 2018 và chỉ dẫn gửi xe vào đường đi bộ Phạm Ngũ Lão.

---

## 5. Giới hạn hoặc phần chưa chạy

Không có giới hạn review đã biết trong phạm vi cụm 3 tuyến phố đi bộ này.

---

## 6. Decision và bước tiếp theo

- **Technical verdict:** `changes_requested`.
- **Bước tiếp theo:**
  1. Gửi báo cáo này cho Implementer để tiến hành một đợt hiệu chỉnh tập trung duy nhất (Focused Correction Batch) khắc phục toàn bộ 2 Blocker, 5 Major và 7 Minor đã nêu chi tiết ở Mục 2.
  2. Implementer cập nhật đồng bộ các căn cứ kiểm chứng mới vào Mục VIII và IX của `knowledge-base-hue/meta/tourism-research-evidence.md`.
  3. Sau khi Implementer hoàn tất và tự kiểm tra, Reviewer sẽ tiến hành re-review nhanh để ra phán quyết đóng duyệt (PASS) cho nhóm phố đi bộ trước khi chuyển sang nhóm Biển & Vịnh.
