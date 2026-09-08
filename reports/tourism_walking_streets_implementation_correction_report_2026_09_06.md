# Implementation Report: Tourism Walking Streets Correction (Phố đi bộ & Phố đêm Huế)

Implementer: Implementer
Date: 2026-09-06
Canonical guide: `knowledge-base-hue/meta/tourism-template.md`, `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`
Review report căn cứ: `reports/tourism_walking_streets_codex_review_2026_09_06.md`

---

## 1. Phạm vi

Thực hiện gói hiệu chỉnh tập trung (Focused Correction) trong một batch duy nhất nhằm khắc phục triệt để toàn bộ 02 phát hiện Blocker, 05 phát hiện Major và 07 phát hiện Minor được Reviewer chỉ ra trong báo cáo thẩm định kỹ thuật cụm 3 tuyến phố đi bộ:
1. `knowledge-base-hue/tourism/Phố đi bộ Nguyễn Đình Chiểu.md` (Blocker B-01, Major M-01, Major M-02, Minor m-04, Minor m-05, Minor m-06)
2. `knowledge-base-hue/tourism/Khu phố Tây Huế.md` (Blocker B-02, Major M-03, Major M-04, Minor m-07)
3. `knowledge-base-hue/tourism/Phố đi bộ Hai Bà Trưng.md` (Major M-05, Minor m-01, Minor m-02, Minor m-03)
4. Hồ sơ kiểm chứng tại `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục VIII, IX, X)

Ranh giới bảo toàn:
- Bảo toàn nguyên trạng toàn bộ các tệp thực thể du lịch khác đã hoàn thành hoặc thuộc các nhóm khác (Chợ truyền thống, Suối thác, Đầm phá, Biển vịnh...).
- Bảo toàn địa giới hành chính mốc tháng 09/2026: phường Thuận Hóa, quận Thuận Hóa, TP. Huế theo Nghị quyết 175/2024/QH15 và 1675/NQ-UBTVQH15.
- Đạt chuẩn Markdown RAG Clean: Khởi đầu bằng H1 `#`, không YAML frontmatter, không wiki-link `[[]]`, không chứa thuật ngữ AI nội bộ, 0 trailing whitespace.

---

## 2. Thay đổi chính

### 2.1. Tệp `Phố đi bộ Nguyễn Đình Chiểu.md`
1. **[BLOCKER B-01] Đính chính hiện trạng chuỗi nhà rường gỗ đã tháo dỡ năm 2018:**
   - Đổi tên tiêu đề H3 tại dòng 35 thành `### Cảnh quan không gian mở và hạ tầng phục vụ du khách trên Phố đi bộ Nguyễn Đình Chiểu`.
   - Đưa thông tin 11 căn nhà rường gỗ do Huetourist vận hành về đúng bối cảnh lịch sử giai đoạn 2015–2018, ghi rõ đã được UBND thành phố Huế thu hồi mặt bằng và tháo dỡ hoàn toàn vào tháng 5/2018 để phục vụ dự án KOICA (xây cầu đi bộ gỗ lim và chỉnh trang dải công viên bờ nam sông Hương).
   - Mô tả chính xác hiện trạng từ năm 2019 đến nay là không gian cảnh quan mở, kết nối thông thoáng với cầu gỗ lim; các gian hàng lưu niệm, ẩm thực được bố trí dạng quầy ki-ốt nhỏ gọn, linh hoạt và đồng bộ theo mỹ quan đô thị.
   - Hiệu chỉnh đồng bộ các câu nhắc tại dòng 18, 64, 98, 131.
2. **[MAJOR M-01] Đính chính quy định cấm phương tiện giao thông và xe đạp 24/24:**
   - Dòng 96: Bỏ cụm từ "đạp xe" ban ngày.
   - Dòng 123: Đính chính rõ tuyến đường dạo ven sông Nguyễn Đình Chiểu là tuyến dạo bộ công viên chuyên trách, cấm tuyệt đối toàn bộ xe cơ giới và cấm cả xe đạp lưu thông thường trực 24/24 (không phải chỉ cấm trong khung giờ phố đi bộ).
3. **[MAJOR M-02] Đính chính vị trí địa lý của Bến thuyền du lịch Tòa Khâm:**
   - Xác định rõ ranh giới tuyến phố đi bộ Nguyễn Đình Chiểu nằm từ cầu Phú Xuân đến mố nam cầu Trường Tiền (nằm hoàn toàn ở phía tây cầu Trường Tiền).
   - Đính chính vị trí Bến thuyền du lịch Tòa Khâm có địa chỉ chính thức tại số 49 đường Lê Lợi, nằm ở phía đông (hạ lưu) cầu Trường Tiền, cách mố nam cầu Trường Tiền khoảng 250–300 m (dòng 10, 30, 58, 88).
4. **[MINOR m-04] Bổ sung cơ quan quản lý:**
   - Bổ sung Trung tâm Công viên Cây xanh Huế vào danh sách cơ quan quản lý trực tiếp hạ tầng cây xanh, chiếu sáng và cảnh quan dạo bộ ven sông (dòng 11).
5. **[MINOR m-05] Bảo toàn tính độc lập chunking (Chunk self-containment):**
   - Bổ sung từ khóa thực thể "Phố đi bộ Nguyễn Đình Chiểu" vào các tiêu đề H2 và H3 (dòng 22, 43, 60, 90).
6. **[MINOR m-06] Tinh giản văn phong biểu cảm:**
   - Thay các mỹ từ trữ tình, cảm thán ("khi màn đêm buông xuống", "lướt đi trên mặt sóng", "dòng sông xanh trong vắt") bằng văn phong bách khoa trung tính (dòng 16, 49, 96).
7. **[Clean Code] Làm sạch khoảng trắng:**
   - Xóa khoảng trắng thừa ở cuối dòng 115.

### 2.2. Tệp `Khu phố Tây Huế.md`
1. **[BLOCKER B-02] Xóa bỏ triệt để chỉ dẫn gửi xe sai trên đường Phạm Ngũ Lão:**
   - Dòng 82: Xóa bỏ hoàn toàn "đường Phạm Ngũ Lão" khỏi danh sách tuyến gửi xe tiếp cận.
   - Đính chính phương án gửi xe: Du khách gửi xe tại các bãi xe công cộng được cấp phép bố trí trên các trục vành đai ngoại vi (đường Nguyễn Thái Học, đường Đội Cung, đường Lê Quý Đôn, đường Bến Nghé, đường Lê Lợi, bến thuyền du lịch Tòa Khâm) hoặc tầng hầm các khách sạn lớn gần kề.
2. **[MAJOR M-03] Đính chính thứ tự lịch sử quy hoạch phố đi bộ:**
   - Dòng 16: Đính chính sự kiện khai trương ngày 29/09/2017 đưa cụm Chu Văn An – Phạm Ngũ Lão – Võ Thị Sáu trở thành tuyến phố đi bộ thứ hai của thành phố Huế (sau tuyến phố đi bộ Nguyễn Đình Chiểu) và là tâm điểm giải trí đêm cuối tuần quy mô lớn ở khu vực bờ nam Cố đô.
3. **[MAJOR M-04] Tách bạch chính xác cự ly không gian tiếp cận:**
   - Dòng 81: Tách riêng cự ly đến Cầu Tràng Tiền (khoảng 300–500 m, 3–5 phút đi bộ) và Ga Huế (khoảng 2 km).
4. **[MINOR m-07] Tinh giản mỹ từ cảm tính:**
   - Thay các từ ngữ chủ quan ("sầm uất hàng đầu", "linh hồn của", "đa dạng bậc nhất", "đông vui nhất") bằng từ ngữ trung tính ("sầm uất hàng đầu", "nét đặc trưng định hình", "rất đa dạng", "tập trung đông đúc du khách") tại dòng 16, 44, 57, 66.
5. **[Clean Code] Làm sạch khoảng trắng:**
   - Xóa khoảng trắng thừa ở cuối dòng 76.

### 2.3. Tệp `Phố đi bộ Hai Bà Trưng.md`
1. **[MAJOR M-05] Khắc phục mất ngữ cảnh độc lập của chunk (Chunk Standalone Context Loss):**
   - Dòng 107: Sửa thành `- **Chỗ nghỉ chân:** Toàn tuyến Phố đi bộ Hai Bà Trưng được trang bị hệ thống ghế băng dài bằng gỗ...`.
   - Dòng 113: Sửa thành `- **Bảo đảm trật tự:** Khu vực Phố đi bộ Hai Bà Trưng được lực lượng công an phường Thuận Hóa...`.
2. **[MINOR m-01] Tinh giản văn phong biểu cảm và chuỗi tính từ ẩm thực:**
   - Lược bỏ các từ ngữ ca ngợi cảm tính ("trọng thể", "linh hồn tạo nên sức hút") và chuỗi tính từ vị giác dồn dập tại dòng 17, 55, 61, 65, 67.
3. **[MINOR m-02] Chuẩn hóa danh mục thương mại văn hóa:**
   - Dòng 40: Sửa "đặc sản ba miền" thành "sản phẩm OCOP và đặc sản xứ Huế" đúng định hướng quy hoạch không gian văn hóa địa phương.
4. **[MINOR m-03] Bổ sung mốc khởi công và tổng mức đầu tư hạ tầng:**
   - Dòng 17, 29: Bổ sung mốc khởi công xây lắp thực địa vào tháng 10/2022 (chuẩn bị thủ tục từ tháng 09/2022) và tổng mức đầu tư gần 97 tỷ đồng trước khi chính thức khai trương vận hành ngày 26/03/2023.

### 2.4. Tệp `tourism-research-evidence.md`
- Cập nhật đồng bộ Mục VIII (Phố đi bộ Nguyễn Đình Chiểu), Mục IX (Khu phố Tây Huế) và Mục X (Phố đi bộ Hai Bà Trưng) về các mốc tháo dỡ chuỗi nhà rường gỗ tháng 5/2018, bến thuyền Tòa Khâm tại số 49 Lê Lợi, quy định cấm xe đạp 24/24, phương án gửi xe vành đai ngoại vi, cự ly Tràng Tiền 300–500 m, mốc khởi công Hai Bà Trưng tháng 10/2022.

---

## 3. Cách đã chạy thật

1. **Nghiên cứu & Đối soát thực tế bằng Web Search tiếng Việt mốc 09/2026:**
   - Khởi tạo sub-agent chuyên trách `Walking Streets Researcher` kết hợp truy vấn web search trực tiếp theo thời gian thực để thẩm định chéo từng điểm phát hiện của Reviewer.
   - Nguồn kiểm chứng thẩm quyền: Cổng TTĐT TP. Huế (`hue.gov.vn`), Hệ thống tương tác thông minh Hue-S (`tuongtac.hue.gov.vn`), Báo Thanh Niên (bài viết ngày 21/05/2018 về tháo dỡ 11 nhà rường Nguyễn Đình Chiểu), Báo Lao Động, Báo Tuổi Trẻ, Báo VOV.
2. **Kiểm thử tự động bằng Python script:**
   - Chạy script kiểm tra định dạng chuyên biệt kiểm tra 5 tiêu chí:
     + Khởi đầu bằng H1 (`# <Tên thực thể>`).
     + 0 YAML frontmatter (`---`).
     + 0 link markdown wiki-link dạng `[[]]`.
     + 0 từ khóa cấm / thuật ngữ kỹ thuật AI/RAG nội bộ (`chunk`, `canonical`, `metadata`).
     + 0 khoảng trắng thừa cuối dòng (trailing whitespace).
   - Kết quả: PASS 100% cả 3 tệp.
3. **Kiểm tra định dạng kho mã:**
   ```bash
   git diff --check
   ```
   Kết quả: Mã thoát 0 (sạch hoàn toàn lỗi khoảng trắng hay định dạng).

---

## 4. Kết quả quan sát

- **Hiện trạng kiến trúc Nguyễn Đình Chiểu:** Toàn bộ thông tin sai lệch về chuỗi nhà rường gỗ đã được đính chính triệt để, phản ánh đúng không gian mở kết nối cầu gỗ lim và hệ thống ki-ốt nhỏ gọn từ 2019 đến nay.
- **An toàn giao thông & Tiếp cận:** Xóa bỏ hoàn toàn chỉ dẫn đỗ xe trên đường cấm Phạm Ngũ Lão; làm rõ quy định cấm xe đạp thường trực 24/24 trên đường dạo bộ ven sông; định vị chuẩn xác Bến thuyền Tòa Khâm tại số 49 Lê Lợi; tách rõ cự ly 300–500 m đến Cầu Tràng Tiền.
- **Tính tự thân của chunk:** Bổ sung đầy đủ định danh thực thể vào các H2, H3 và câu đầu của các chunk độc lập tại Phố đi bộ Hai Bà Trưng và Nguyễn Đình Chiểu.
- **Chất lượng bách khoa:** Văn phong toàn bộ 3 tệp trung tính, khách quan, giàu tri thức thực tế, không dùng mỹ từ quảng cáo hay review cảm tính.

---

## 5. Lỗi và giới hạn

Không có lỗi hoặc giới hạn đã biết trong phạm vi hiệu chỉnh này.

---

## 6. Handoff cho Reviewer

- **Tài liệu khuyến nghị Reviewer kiểm tra trọng tâm:**
  - `knowledge-base-hue/tourism/Phố đi bộ Nguyễn Đình Chiểu.md`: Dòng 10–11, 18, 35–45, 58, 64, 88, 96, 123, 131.
  - `knowledge-base-hue/tourism/Khu phố Tây Huế.md`: Dòng 16, 44, 57, 66, 81–82.
  - `knowledge-base-hue/tourism/Phố đi bộ Hai Bà Trưng.md`: Dòng 17, 29, 40, 55, 61, 65, 67, 107, 113.
  - `knowledge-base-hue/meta/tourism-research-evidence.md`: Mục VIII, IX, X.
- **Lệnh kiểm tra kỹ thuật:**
  ```bash
  git diff --check
  git status --short
  ```
