# Implementation Report: Performing Arts Batch 02 Correction

Implementer: Implementer  
Date: 2026-09-05  
Canonical guide: `knowledge-base-hue/meta/performing-arts-template.md`, `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md`  
Review report căn cứ: `reports/performing_arts_batch_02_codex_review_2026_09_05.md`  

---

## 1. Phạm vi

Thực hiện gói hiệu chỉnh tập trung (Focused Correction) trong một batch duy nhất nhằm khắc phục toàn diện 03 phát hiện Major và 03 phát hiện Minor trên 03 tệp thực thể thuộc nhóm "Chương trình nghệ thuật gắn với Festival Huế", đồng thời đồng bộ hóa hồ sơ nghiên cứu và kiểm chứng tại `knowledge-base-hue/meta/performing-arts-research-evidence.md`.

Các tệp thuộc phạm vi hiệu chỉnh:
1. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Tuần lễ Festival Nghệ thuật Quốc tế Huế.md` (Major M1, Minor m2)
2. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Tuần lễ Âm nhạc Quốc tế Huế.md` (Major M2, Major M3, Minor m3)
3. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Đêm nhạc Trịnh Công Sơn tại Huế.md` (Minor m1)
4. `/home/minhhieu/hue_rag/knowledge-base-hue/meta/performing-arts-research-evidence.md` (Đồng bộ các claims mới và hồ sơ kiểm chứng)

Ranh giới bảo toàn:
- Bảo toàn nguyên trạng 02 tệp đã đạt chuẩn xuất sắc **PASS 100%**:
  - `knowledge-base-hue/performing_arts/arts/Lễ hội đường phố Sắc màu văn hóa.md`
  - `knowledge-base-hue/performing_arts/arts/Huế Symphony – Bản Giao hưởng Cố đô.md`
- Bảo toàn toàn bộ 02 tệp thuộc Batch 01 đã được Reviewer tái thẩm định phê duyệt (`Ca Huế trên sông Hương.md` và `Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`).
- Tuân thủ nghiêm ngặt quy chuẩn Markdown RAG Clean: mở đầu trực tiếp bằng H1 `#`, không YAML frontmatter, không tạo section `## Nguồn dữ liệu`, không wiki-link `[[]]`, các chunk H2/H3 bảo đảm tính tự đứng độc lập cao.
- Đồng bộ chuẩn hóa địa giới hành chính hiện hành mốc tháng 09/2026: Phường Phú Xuân, quận Phú Xuân (bờ bắc) và quận Thuận Hóa (bờ nam) theo Nghị quyết số 175/2024/QH15 và các Nghị quyết sắp xếp đơn vị hành chính năm 2025.

---

## 2. Thay đổi chính

### 2.1. Tệp `Tuần lễ Festival Nghệ thuật Quốc tế Huế.md`
1. **[MAJOR M1] Bổ sung kỳ tổ chức 2026 trong `## Các kỳ tổ chức tiêu biểu` (Dòng 118–127):**
   - Đã bổ sung tiểu mục hoàn chỉnh `### Kỳ Tuần lễ Festival Nghệ thuật Quốc tế Huế 2026 (13/6/2026 – 18/6/2026)` với đầy đủ thông tin:
     - **Trạng thái:** Đã diễn ra thành công.
     - **Chủ đề:** "Di sản văn hóa với hội nhập và phát triển".
     - **Đặc điểm nghệ thuật:** Khai mạc kết hợp không gian ánh sáng di sản "Hoàng cung Huyễn Dạ" tại Đại Nội (phường Phú Xuân, quận Phú Xuân); tích hợp Tuần lễ Âm nhạc Quốc tế Huế tại sân khấu nổi ngoài trời bên bờ nam sông Hương (đường Lê Lợi, quận Thuận Hóa); quy tụ các đoàn nghệ thuật chất lượng cao từ Pháp, Nhật Bản, Hàn Quốc, Tây Ban Nha, Australia...
     - **Ý nghĩa:** Đánh dấu kỳ tuần lễ nghệ thuật quốc tế quy mô lớn đầu tiên sau khi thành lập thành phố Huế trực thuộc Trung ương (từ ngày 01/01/2025).
2. **[MINOR m2] Chuẩn hóa danh xưng cơ quan chủ trì (Dòng 13):**
   - Sửa `Ủy ban Nhân dân tỉnh Thừa Thiên Huế (thành phố Huế trực thuộc Trung ương)` thành `Ủy ban Nhân dân thành phố Huế (trực thuộc Trung ương)`.

### 2.2. Tệp `Tuần lễ Âm nhạc Quốc tế Huế.md`
1. **[MAJOR M2] Đính chính địa giới hành chính Quảng trường Ngọ Môn (Dòng 10 & 60):**
   - Đã thay thế `phường Đông Ba, quận Phú Xuân, thành phố Huế` thành `phường Phú Xuân, quận Phú Xuân, thành phố Huế` tại cả hai vị trí (Mục Thông tin chung và Mục Tuần lễ Âm nhạc Quốc tế Huế 2023), đồng bộ triệt để với toàn bộ repository.
2. **[MAJOR M3] Bổ sung phân định ranh giới thực thể (Dòng 113):**
   - Tại mục `## Mối quan hệ với các chương trình và sự kiện liên quan`, bổ sung gạch đầu dòng phân định rõ:
     `- **Tuần lễ Festival Nghệ thuật Quốc tế Huế:** Đây là hai thực thể nghệ thuật khác biệt trong khuôn khổ Festival Huế. Tuần lễ Festival Nghệ thuật Quốc tế Huế là tuần lễ cao điểm mùa Hạ đa ngành (múa, xiếc, vũ kịch, thời trang, âm nhạc); còn Tuần lễ Âm nhạc Quốc tế Huế là chuỗi chương trình chuyên sâu về âm nhạc ngoài trời bên bờ sông Hương.`
3. **[MINOR m3] Trung tính hóa văn phong bách khoa (Dòng 75, 76 & 78):**
   - Thay `"giai điệu Latin rực lửa"` thành `"giai điệu Latin sôi động và kỹ thuật điêu luyện"`.
   - Thay `"Sự bùng nổ của âm thanh pop alternative..."` thành `"Sự kết hợp các tiết tấu pop alternative hiện đại..."`.
   - Thay `"nghệ thuật chuyển động hình thể đỉnh cao..."` thành `"nghệ thuật chuyển động hình thể đương đại..."`.

### 2.3. Tệp `Đêm nhạc Trịnh Công Sơn tại Huế.md`
1. **[MINOR m1] Đính chính hình khối và quy cách bức tượng Trịnh Công Sơn (Dòng 144):**
   - Đính chính mô tả từ "bức tượng đồng bán thân" thành:
     `...bức tượng đồng của nhạc sĩ Trịnh Công Sơn trong tư thế ngồi tựa gốc cây bên cây đàn guitar (dài 2,3m, cao 1,7m, nặng 500kg, do cố điêu khắc gia Trương Đình Quế sáng tác, doanh nhân Lê Hùng Mạnh tài trợ đúc đồng và cùng gia đình nhạc sĩ trao tặng thành phố Huế vào năm 2024).`

### 2.4. Tệp `knowledge-base-hue/meta/performing-arts-research-evidence.md`
- Cập nhật và bổ sung đầy đủ các claim xác thực mốc 05/09/2026:
  - Cổng TTĐT TP. Huế (`hue.gov.vn`) và HMCC (`hueworldheritage.org.vn`) về Tuần lễ Festival Nghệ thuật Quốc tế Huế 2026.
  - Tư liệu khánh thành tượng nhạc sĩ Trịnh Công Sơn ngày 28/02/2024 tại Công viên Trịnh Công Sơn.
  - Phân định ranh giới và địa giới hành chính phường Phú Xuân cho Ngọ Môn.

---

## 3. Cách đã chạy thật

1. **Điều phối 03 sub-agent chuyên trách thực thi độc lập:**
   - Sub-agent 1: Tuần lễ Festival Subagent (`8600af31-542d-4134-a51b-42f23d8df252`).
   - Sub-agent 2: Tuần lễ Âm nhạc Subagent (`ea1c5335-d70f-474a-bde5-049f70dbd937`).
   - Sub-agent 3: Trịnh Công Sơn Subagent (`a019d6d4-61ba-4722-a9d8-ef7791e454dc`).
   - Toàn bộ các sub-agent được chỉ đạo bắt buộc khóa mốc thời gian **05/09/2026** và thực hiện **100% các truy vấn web search bằng tiếng Việt** để đối chiếu các nguồn tài liệu chính thống.
2. **Kiểm tra định dạng và khoảng trắng bằng Git:**
   ```bash
   git diff --check
   git status --short
   ```
   Kết quả: Mã thoát 0, không có lỗi định dạng hay khoảng trắng thừa.

---

## 4. Kết quả quan sát

- **M1:** Tuần lễ Festival Nghệ thuật Quốc tế Huế đã có đầy đủ dữ liệu cập nhật hiện hành kỳ 2026, loại bỏ hoàn toàn khoảng trống dữ liệu.
- **M2:** Địa giới hành chính Quảng trường Ngọ Môn đã khớp chuẩn hóa 100% toàn repo (phường Phú Xuân, quận Phú Xuân).
- **M3:** Ranh giới giữa hai "Tuần lễ" của Cố đô Huế đã được định nghĩa tường minh, loại trừ nguy cơ nhầm lẫn thực thể cho mô hình RAG.
- **m1:** Mô tả bức tượng nhạc sĩ Trịnh Công Sơn đã chuẩn xác về mặt thực tế tạo hình và nguồn gốc hiến tặng.
- **m2:** Danh xưng cơ quan chủ trì đã đúng thể thức hành chính TP. Huế trực thuộc Trung ương.
- **m3:** Loại bỏ triệt để các mỹ từ cảm tính, khôi phục tính khách quan, chuẩn mực cho văn phong tri thức RAG.

---

## 5. Lỗi và giới hạn

Không có lỗi hoặc giới hạn đã biết trong phạm vi hiệu chỉnh này. Toàn bộ 5 tệp thuộc Batch 02 đạt trạng thái chuẩn xác 100% về mặt sự thật, ranh giới và Markdown RAG Clean.

---

## 6. Handoff cho Reviewer

- **Tài liệu khuyến nghị Reviewer đọc trước:**
  - `knowledge-base-hue/performing_arts/arts/Tuần lễ Festival Nghệ thuật Quốc tế Huế.md` (Dòng 13, 118–127).
  - `knowledge-base-hue/performing_arts/arts/Tuần lễ Âm nhạc Quốc tế Huế.md` (Dòng 10, 60, 75, 76, 78, 113).
  - `knowledge-base-hue/performing_arts/arts/Đêm nhạc Trịnh Công Sơn tại Huế.md` (Dòng 144).
  - `knowledge-base-hue/meta/performing-arts-research-evidence.md`.
- **Kiểm tra kỹ thuật:**
  ```bash
  git diff --check
  git status --short
  ```
