# Implementation Report: Tourism Batch 01 Correction

Implementer: Implementer (Gemini)  
Date: 2026-09-06  
Canonical guide: `knowledge-base-hue/meta/tourism-template.md`, `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`  
Review report căn cứ: BÁO CÁO THẨM ĐỊNH & REVIEW KỸ THUẬT: BATCH 01 – CHỢ TRUYỀN THỐNG VÀ KHÔNG GIAN PHỐ CỔ (06/09/2026)  

---

## 1. Phạm vi

Thực hiện gói hiệu chỉnh tập trung (Focused Correction) trong một batch duy nhất nhằm khắc phục toàn bộ 5 phát hiện Major và 8 phát hiện Minor được Reviewer (Codex) chỉ ra trong báo cáo thẩm định Batch 01 (Chợ truyền thống và không gian phố cổ).

Toàn bộ các nội dung phản hồi trong báo cáo của Reviewer đã được Implementer và hệ thống tra cứu đối chiếu, xác thực độc lập bằng web search tiếng Việt mốc tháng 09/2026 trước khi tiến hành chỉnh sửa.

Các tệp thuộc phạm vi hiệu chỉnh:
1. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Chợ Đông Ba.md` (Xử lý Major 1, Major 2, Minor 7, Minor 8)
2. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Phố cổ và chợ Bao Vinh.md` (Xử lý Major 3, Minor 5, Minor 6)
3. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Chợ Tây Lộc.md` (Xử lý Major 4, Minor 1, Minor 7, Minor 8)
4. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Chợ Xép.md` (Xử lý Major 5, Minor 2, Minor 3)
5. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Chợ Bến Ngự.md` (Xử lý Minor 7)
6. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Chợ An Cựu.md` (Xử lý Minor 4)
7. `/home/minhhieu/hue_rag/knowledge-base-hue/meta/tourism-research-evidence.md` (Đồng bộ hóa các dữ kiện kiểm chứng mới vào hồ sơ nghiên cứu)

Ranh giới tuân thủ:
- Giữ nguyên toàn bộ 29 tệp thực thể còn lại trong `knowledge-base-hue/tourism/`.
- Bảo toàn tuyệt đối chuẩn Markdown RAG Clean: mở đầu trực tiếp bằng H1 `#`, không YAML frontmatter, không chứa `## Nguồn dữ liệu` trong body answer-facing, không wiki-link `[[]]`, sạch hoàn toàn thuật ngữ AI/RAG nội bộ.
- Chuẩn hóa địa giới hành chính theo Nghị quyết số 175/2024/QH15 và Nghị quyết số 1675/NQ-UBTVQH15 mốc tháng 09/2026.

---

## 2. Thay đổi chính

### 2.1. Tệp `Chợ Đông Ba.md`

1. **[MAJOR 1] Đính chính lịch sử địa giới hành chính (Dòng 8):**
   - *Xác thực:* Chợ Đông Ba (số 2 Trần Hưng Đạo) trước 01/07/2021 thuộc phường Phú Hòa cũ. Theo Nghị quyết 1264/NQ-UBTVQH14, phường Phú Hòa hợp nhất với Thuận Thành thành phường Đông Ba (từ 01/07/2021 đến 30/06/2025). Chợ Đông Ba chưa từng thuộc phường Gia Hội (phường Gia Hội lập từ Phú Cát + Phú Hiệp, nằm bên bờ đông sông Đông Ba).
   - *Hiệu chỉnh:* Sửa đoạn trong ngoặc đơn thành: `(theo Nghị quyết số 1675/NQ-UBTVQH15, từ ngày 01/07/2025 chợ thuộc phường Phú Xuân; trước thời điểm này khu vực chợ từng thuộc địa giới hành chính của phường Phú Hòa cũ, giai đoạn từ tháng 07/2021 đến tháng 06/2025 thuộc phường Đông Ba)`.
2. **[MAJOR 2] Sắp xếp đúng công năng 3 tầng Lầu Chuông trung tâm (Dòng 74–76):**
   - *Xác thực:* Sơ đồ quy hoạch thực tế của BQL Chợ Đông Ba và cẩm nang du lịch: Tầng 1 là đặc sản khô, mắm Huế, bánh kẹo; Tầng 2 là thủ công mỹ nghệ, nón lá bài thơ, quà lưu niệm; Tầng 3 là "Lầu may" chuyên doanh vải may áo dài, lụa gấm và tiệm may đo lấy nhanh.
   - *Hiệu chỉnh:* Cập nhật cấu trúc phân tầng chuẩn xác:
     + **Tầng 1 (tầng trệt):** Khu vực tầng trệt chuyên doanh các mặt hàng đồ khô, hải sản khô, bánh kẹo đặc sản Cố đô, các loại mắm truyền thống Huế (mắm tôm chua, mắm ruốc, mắm nêm, mắm cá rò) cùng các mặt hàng đồ tiêu dùng gia đình và quầy ăn vặt dân dã.
     + **Tầng 2:** Thế giới hàng thủ công mỹ nghệ và quà lưu niệm truyền thống Huế (nón lá bài thơ, đồ đồng Phường Đúc, chạm bạc Kế Môn, gốm sứ lưu niệm, đồ gỗ mỹ nghệ).
     + **Tầng 3 ("Lầu may"):** Đại bản doanh của ngành hàng vải vóc may mặc và trang phục (vải may áo dài, lụa tơ tằm, voan, nhung, vải thêu, quần áo may sẵn, tiệm cắt may đo thủ công lấy ngay).
3. **[MINOR 7] Làm sạch khoảng trắng thừa (Dòng 41):**
   - Đã thay 2 dấu cách cuối dòng trong trích đoạn thơ lục bát bằng thẻ `<br>` chuẩn, làm sạch 100% trailing whitespace.
4. **[MINOR 8] Bổ sung từ khóa định danh "Chợ Đông Ba" vào các H3:**
   - Dòng 29: `### Tái lập Chợ Đông Ba dưới triều vua Đồng Khánh (1887)`
   - Dòng 52: `### Chỉnh trang hạ tầng và xây dựng nếp sống văn minh thương mại tại Chợ Đông Ba`
   - Dòng 78: `### Hệ thống nhà hai tầng bốn góc và các dãy ki-ốt vệ tinh Chợ Đông Ba`
   - Dòng 133: `### Vai trò kinh tế và phân phối hàng hóa đầu mối của Chợ Đông Ba`
   - Dòng 164: `### Thời điểm tham quan Chợ Đông Ba phù hợp`

### 2.2. Tệp `Phố cổ và chợ Bao Vinh.md`

1. **[MAJOR 3] Đính chính địa chỉ Chùa Thiên Giang (Dòng 58):**
   - *Xác thực:* Số 66 Bao Vinh là ngôi nhà cổ của gia đình bác Đoan (quán Cà phê Mắt Biếc, bối cảnh nhà Hà Lan). Chùa Thiên Giang là ngôi cổ tự độc lập nằm ở cuối tuyến phố cổ Bao Vinh (gần cống Địa Linh).
   - *Hiệu chỉnh:* Xóa cụm từ `tại số 66 Bao Vinh`, sửa thành: `Ngôi cổ tự tọa lạc ở khu vực cuối tuyến phố cổ Bao Vinh (gần cống Địa Linh), nép mình tĩnh lặng bên tán cây xanh mát...`.
2. **[MINOR 5] Nhất quán tên dòng sông trước đò ngang (Dòng 146):**
   - *Hiệu chỉnh:* Sửa `qua sông Hương` thành: `Khi trải nghiệm đi đò ngang Bao Vinh vượt sông Đông Ba sang Tiên Nộn...`.
3. **[MINOR 6] Bổ sung đặc sản Bánh Pháp Lam (sau dòng 88):**
   - *Hiệu chỉnh:* Bổ sung 1 gạch đầu dòng giới thiệu món Bánh Pháp Lam (bánh ngũ sắc) phố cổ Bao Vinh – loại bánh tiến vua nhân bột đậu xanh, mứt bí, hạt sen bọc giấy ngũ sắc được lưu truyền tại các gia đình truyền thống ở Bao Vinh.

### 2.3. Tệp `Chợ Tây Lộc.md`

1. **[MAJOR 4] Bổ sung mốc lịch sử 1977 và 2 món đặc sản biểu tượng:**
   - *Xác thực:* Năm 1977, thành phố di dời gần 400 lô hàng "chợ trời" từ phía bắc cầu Trường Tiền sang Chợ Tây Lộc, tạo bước ngoặt biến chợ thành trung tâm đồ si lớn nhất Huế. Khu ẩm thực Chợ Tây Lộc nức tiếng với Bánh canh Nam Phổ sánh sệt gạch cua tôm và Bún mắm nêm thịt quay/chả lụa đậm đà.
   - *Hiệu chỉnh:* Bổ sung mốc năm 1977 vào đoạn lịch sử dòng 21; bổ sung 2 tiểu mục chi tiết cho `Bánh canh Nam Phổ Chợ Tây Lộc` và `Bún mắm nêm Chợ Tây Lộc` trong mục ẩm thực.
2. **[MINOR 1] Chuẩn hóa cấp quận trong địa chỉ mốc 09/2026 (Dòng 8 & 25):**
   - *Hiệu chỉnh:* Cập nhật đầy đủ cấp quận: `Số 209 đường Nguyễn Trãi, phường Phú Xuân, quận Phú Xuân, thành phố Huế`.
3. **[MINOR 7] Làm sạch khoảng trắng thừa (Dòng 11):**
   - *Hiệu chỉnh:* Xóa khoảng trắng thừa ở cuối dòng 11 sau từ `thường nhật`.
4. **[MINOR 8] Bổ sung từ khóa "Chợ Tây Lộc" vào mục du khách (Dòng 75 & 76):**
   - *Hiệu chỉnh:* Sửa thành `Bảo quản tư trang cá nhân tại Chợ Tây Lộc:` và `Ứng xử văn hóa khi tham quan Chợ Tây Lộc:`.

### 2.4. Tệp `Chợ Xép.md`

1. **[MAJOR 5] Bổ sung món ăn sáng biểu tượng Bánh ướt và Xôi thịt hon (Dòng 79):**
   - *Xác thực:* Bánh ướt mộc (chả lụa/thịt heo quay giòn rụm) và Xôi thịt hon (xôi nếp dẻo thịt/sườn non thấm vị củ nén, bột cà ri, sả ớt) là hai món ăn sáng đặc sắc nổi danh bậc nhất của trục Ngô Đức Kế – Chợ Xép trong Thành Nội.
   - *Hiệu chỉnh:* Bổ sung mô tả chi tiết hai món signature này vào tiểu mục điểm tâm sáng tại dòng 79.
2. **[MINOR 2] Cập nhật địa giới hành chính làng Chuồn (Dòng 65):**
   - *Hiệu chỉnh:* Sửa `làng Chuồn (xã Phú An)` thành: `làng Chuồn (trước thuộc xã Phú An, nay thuộc phường Mỹ Thượng, thành phố Huế)`.
3. **[MINOR 3] Loại bỏ mỹ từ quảng cáo (Dòng 16):**
   - *Hiệu chỉnh:* Đổi `thiên đường săn "đồ bành"` thành `địa chỉ săn "đồ bành" quen thuộc`.

### 2.5. Tệp `Chợ Bến Ngự.md`

1. **[MINOR 7] Làm sạch khoảng trắng thừa (Dòng 34):**
   - *Hiệu chỉnh:* Xóa 1 dấu cách thừa ở cuối dòng 34 sau cụm từ `(1940).`.

### 2.6. Tệp `Chợ An Cựu.md`

1. **[MINOR 4] Sửa phương hướng di chuyển đến Cung An Định (Dòng 174):**
   - *Xác thực:* Cung An Định nằm ở 179 Phan Đình Phùng, ngược dòng sông An Cựu về hướng Bến Ngự/Ga Huế (hướng tây bắc so với Chợ An Cựu).
   - *Hiệu chỉnh:* Sửa `phía đông bắc` thành: `khoảng 600m về phía tây bắc dọc theo bờ sông An Cựu (đường Phan Đình Phùng)`.

### 2.7. Tệp `knowledge-base-hue/meta/tourism-research-evidence.md`

- Cập nhật đồng bộ thông tin địa giới lịch sử của Chợ Đông Ba (dòng 41).
- Bổ sung mốc 1977, Bánh canh Nam Phổ, Bún mắm nêm vào bảng Facts của Chợ Tây Lộc (dòng 160–168).
- Bổ sung Bánh ướt, Xôi thịt hon và cập nhật làng Chuồn vào bảng Facts của Chợ Xép (dòng 201–207).
- Đính chính địa chỉ Chùa Thiên Giang, đò ngang sông Đông Ba và bổ sung Bánh Pháp Lam vào bảng Facts của Phố cổ Bao Vinh (dòng 242–248).

---

## 3. Cách đã chạy thật

1. **Xác thực Web Search độc lập bằng tiếng Việt**:
   - Truy vấn Nghị quyết 1264/NQ-UBTVQH14 về việc thành lập phường Đông Ba từ Phú Hòa + Thuận Thành (2021–2025).
   - Tra cứu cấu trúc lầu chuông 3 tầng Chợ Đông Ba từ cổng TTĐT TP. Huế, Traveloka, VinWonders.
   - Tra cứu vị trí Chùa Thiên Giang và số 66 Bao Vinh (Cà phê Mắt Biếc) từ Cục Du lịch Quốc gia, Báo Huế Ngày Nay.
   - Tra cứu sự kiện di dời chợ trời 1977 về Chợ Tây Lộc và các món ăn Bánh canh Nam Phổ, Bún mắm nêm.
   - Tra cứu món ăn sáng Bánh ướt và Xôi thịt hon tại Chợ Xép / Ngô Đức Kế.
2. **Kiểm thử tự động bằng Python script**:
   - Quét cấu trúc H1, không frontmatter, không `## Nguồn dữ liệu`, không `[[]]`, không từ khóa AI (`canonical`, `chunk`, `metadata`).
   - Quét toàn bộ dòng của cả 6 file để phát hiện và loại trừ triệt để trailing whitespaces (`line.endswith(' ')`).
3. **Kiểm tra cú pháp Git**:
   - `git diff --check` đạt mã thoát 0.

---

## 4. Kết quả quan sát

- **Automated Linting:** 100% (6/6 tệp) vượt qua kiểm thử tự động, không còn bất kỳ lỗi trailing whitespace nào (đã xử lý dòng 41 Chợ Đông Ba, dòng 11 Chợ Tây Lộc, dòng 34 Chợ Bến Ngự).
- **Facts & Accuracy:** 100% các phát hiện Major và Minor đã được đối chiếu khớp hoàn toàn với thực tế và sửa đổi chính xác.
- **RAG Chunk Independence:** Mọi tiêu đề H3 và tiểu mục trong các tệp đã được bổ sung đầy đủ tên thực thể, đảm bảo tính độc lập ngữ cảnh khi vector embedding.

---

## 5. Lỗi và giới hạn

Không có lỗi hoặc giới hạn đã biết trong phạm vi này. Toàn bộ 5 phát hiện Major và 8 phát hiện Minor đã được giải quyết triệt để trong một batch duy nhất.

---

## 6. Handoff cho Reviewer

- **Tài liệu đối soát ưu tiên**:
  + 6 tệp thực thể đã hiệu chỉnh tại `knowledge-base-hue/tourism/`
  + `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục I đến VI)
- **Rerun checks**:
  + `git diff --check`
  + Python linting quét H1, RAG Clean và trailing whitespaces.
