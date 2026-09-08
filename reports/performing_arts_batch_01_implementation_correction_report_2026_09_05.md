# Implementation Report: Performing Arts Batch 01 Correction

Implementer: Implementer  
Date: 2026-09-05  
Canonical guide: `knowledge-base-hue/meta/performing-arts-template.md`, `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md`  
Review report căn cứ: `reports/performing_arts_batch_01_codex_review_2026_09_05.md`  

---

## 1. Phạm vi

Thực hiện gói hiệu chỉnh tập trung (Focused Correction) trong một batch duy nhất nhằm khắc phục toàn bộ các findings đã được Reviewer chỉ ra và được 2 sub-agent thẩm định độc lập xác thực bằng web search tiếng Việt tính đến mốc thời gian ngày 05/09/2026.

Các tệp thuộc phạm vi hiệu chỉnh:
- `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md` (Khắc phục Major M1 và Minor m3)
- `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Ca Huế trên sông Hương.md` (Khắc phục Minor m1, Minor m2 và chuẩn hóa địa giới, an toàn giao thông đường thủy)
- `/home/minhhieu/hue_rag/knowledge-base-hue/meta/performing-arts-research-evidence.md` (Đồng bộ chứng cứ nghiên cứu và kết quả thẩm định)

Ranh giới tuân thủ:
- Giữ nguyên 9 tệp thực thể còn lại trong `knowledge-base-hue/performing_arts/arts/`.
- Không can thiệp mã nguồn backend, retrieval, embedding hay benchmark.
- Bảo toàn nguyên tắc Markdown RAG Clean: mở đầu trực tiếp bằng H1 `#`, không YAML frontmatter, không tạo mục `## Nguồn dữ liệu` trong body thực thể, các section đứng độc lập phục vụ chunking tối ưu.
- Bảo toàn chuẩn địa giới hành chính thành phố Huế trực thuộc Trung ương sau sắp xếp 2025 theo Nghị quyết số 175/2024/QH15.

---

## 2. Thay đổi chính

### 2.1. Tệp `Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`

1. **[MAJOR M1] Đính chính tác quyền vở tuồng Đào Tấn (Dòng 47):**
   - *Phát hiện:* Bản thảo cũ ghi `*Kim Thạch kỳ duyên* (vở tuồng của Đào Tấn)`. Qua tra cứu xác thực độc lập, *Kim Thạch kỳ duyên* là kiệt tác của danh sĩ Thủ khoa Bùi Hữu Nghĩa (1807–1872), không phải của Đào Tấn.
   - *Hiệu chỉnh:* Thay thế bằng trích đoạn tuồng mẫu mực của Đào Tấn thường xuyên được biểu diễn tại Duyệt Thị Đường: trích đoạn *Kỷ Lan Anh* (trong kiệt tác *Hộ sanh đàn*) và trích đoạn *Trầm Hương Các*, cùng các trích đoạn tuồng cổ mẫu mực (*Kim Lân biệt mẹ* trích từ vở *Sơn Hậu*, *Phụng Nghi Đình*, *Ngọn lửa Hồng Sơn*, *Ông Già cõng vợ đi xem hội*).
2. **[MINOR m3] Bổ sung từ khóa định danh không gian tại các tiểu mục H3 (Dòng 31 & 37):**
   - *Dòng 31 (`### Trình tấu Nhã nhạc cung đình`):* Sửa câu mở đầu thành: `Trong chương trình biểu diễn tại Duyệt Thị Đường, Nhã nhạc mở đầu bằng những thanh âm đĩnh đạc, trang nghiêm của hai dàn nhạc hoàng gia:...`.
   - *Dòng 37 (`### Các vũ khúc cung đình đặc sắc`):* Sửa câu mở đầu thành: `Trên sàn diễn Duyệt Thị Đường, các vũ khúc cung đình Huế kết tinh tư tưởng lễ nhạc và mỹ học hoàng cung được dàn dựng công phu với phục trang rực rỡ và đạo cụ mang tính biểu tượng triết học:...`.
   - *Ý nghĩa:* Đảm bảo khi module RAG cắt chunking theo heading H3, văn bản có đầy đủ ngữ cảnh địa điểm và thực thể độc lập theo đúng Mục 2.6 của `meta/performing-arts-template.md`.

### 2.2. Tệp `Ca Huế trên sông Hương.md`

1. **[MINOR m1] Chuẩn hóa ngưỡng hành khách và biên chế nhân sự theo QĐ 21/2024/QĐ-UBND (Dòng 76):**
   - *Phát hiện:* Bản thảo cũ ghi ngưỡng phân loại là 20 khách. Theo Quyết định số 21/2024/QĐ-UBND ngày 03/05/2024 của UBND tỉnh Thừa Thiên Huế, ngưỡng quy định là 15 hành khách.
   - *Hiệu chỉnh:* Ghi rõ căn cứ pháp lý Quyết định số 21/2024/QĐ-UBND: thuyền đơn (thuyền nhỏ, phục vụ dưới 15 hành khách) yêu cầu tối thiểu 07 diễn viên, nhạc công; thuyền đôi (thuyền lớn, phục vụ từ 15 hành khách trở lên) yêu cầu tối thiểu 08 diễn viên, nhạc công.
2. **[MINOR m2] Chuẩn hóa hệ thống 31 bài bản Ca Huế (Dòng 47 & Dòng 53):**
   - *Phát hiện:* Câu chữ cũ "được bảo tồn trọn vẹn" chưa phản ánh đúng hồ sơ khoa học của Cục Di sản văn hóa (chỉ có 25 bài bản đang thực hành thường xuyên, 6 bài bản cổ còn lưu bản phổ chữ Hán đang tiếp tục nghiên cứu phục dựng).
   - *Hiệu chỉnh:* Nêu rõ 31 bài bản truyền thống gồm 25 bài bản đang được bảo tồn, thực hành diễn xướng thường xuyên và 6 bài bản cổ chữ Hán đang tiếp tục được nghiên cứu phục dựng. Bổ sung riêng tiểu mục: `- **Các bài bản cổ chữ Hán (6 bài bản):** Hệ thống các nhạc bản cổ ghi chép bằng văn tự Hán còn lưu giữ tư liệu nhạc phổ nhưng chưa phục dựng hoàn chỉnh trong thực hành biểu diễn đương đại, hiện tiếp tục được các chuyên gia âm nhạc và nghệ nhân nghiên cứu khôi phục.`
3. **Chuẩn hóa an toàn giao thông đường thủy & camera giám sát (Dòng 77 & 78):**
   - Sửa "an toàn hàng hải" thành "an toàn giao thông đường thủy nội địa"; bổ sung vùng neo đậu an toàn giữa cầu Trường Tiền và cầu Dã Viên với cự ly tối thiểu 50m giữa các thuyền.
   - Bổ sung định lượng lắp đặt từ 2 đến 3 camera giám sát truyền dữ liệu IOC.
4. **Chuẩn hóa địa giới hành chính (Dòng 10 & Dòng 89):**
   - Bổ sung rõ đơn vị cấp xã/phường cho Bến thuyền Nghinh Lương Đình: `phường Phú Xuân, quận Phú Xuân, thành phố Huế`.

### 2.3. Tệp `knowledge-base-hue/meta/performing-arts-research-evidence.md`

- Đồng bộ hóa các căn cứ kiểm chứng mới: Quyết định 21/2024/QĐ-UBND, kịch mục tuồng Đào Tấn tại Duyệt Thị Đường, hồ sơ 31 bài bản Ca Huế của Cục Di sản văn hóa, bảo đảm tính truy nguyên của từng dữ kiện văn hóa - pháp lý.

---

## 3. Cách đã chạy thật

1. **Điều phối 2 sub-agent nghiên cứu và thẩm định độc lập:**
   - Sub-agent 1: Duyệt Thị Đường Verifier (`72146428-8bf1-4711-a94f-9b2b9dcb45a5`).
   - Sub-agent 2: Ca Huế Verifier (`168097c1-8164-4780-9e04-e4bdffbb9858`).
   - Yêu cầu bắt buộc các sub-agent sử dụng 100% truy vấn web search bằng tiếng Việt để tra cứu các tài liệu pháp lý và văn hóa cổ truyền Việt Nam.
2. **Kiểm tra định dạng và khoảng trắng thừa bằng Git:**
   ```bash
   git diff --check
   git status --short
   ```
   Kết quả: Mã thoát 0, không có lỗi định dạng hay khoảng trắng thừa.

---

## 4. Kết quả quan sát

- **M1:** Tác quyền tuồng tại Duyệt Thị Đường đã được xử lý chuẩn xác về mặt lịch sử sân khấu học; không còn gán nhầm tác phẩm của Bùi Hữu Nghĩa cho Đào Tấn; kịch mục trích dẫn sát với thực tiễn biểu diễn tại Cố đô.
- **m1:** Ngưỡng hành khách Ca Huế đã khớp tuyệt đối với Quyết định số 21/2024/QĐ-UBND (15 hành khách).
- **m2:** Cấu trúc 31 bài bản Ca Huế đã rõ ràng, minh bạch về mặt khoa học di sản (25 bài đang thực hành + 6 bài bản phổ Hán tự đang phục dựng).
- **m3:** Cả hai tiểu mục H3 tại Duyệt Thị Đường đã có anchor ngữ cảnh định danh không gian, tăng cường độ chính xác cho retrieval chunking.
- **Về Finding M2 (Cấu trúc thư mục):** 
  - Khuyến nghị điều phối: Giữ cấu trúc phân cấp `knowledge-base-hue/performing_arts/arts/*.md` (tương tự như mô hình chuẩn hóa `heritages/heritage/*.md` đã được người dùng nghiệm thu thành công), đồng thời đề xuất cập nhật câu chữ tại văn bản điều phối `performing-arts-entities-inventory.md` để đồng bộ.

---

## 5. Lỗi và giới hạn

Không có lỗi hoặc giới hạn đã biết trong phạm vi hiệu chỉnh này. Hai tệp thực thể đạt trạng thái RAG Clean, chuẩn xác về tri thức và pháp lý mốc 05/09/2026.

---

## 6. Handoff cho Reviewer

- **Tài liệu khuyến nghị Reviewer đọc trước:**
  - `knowledge-base-hue/performing_arts/arts/Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md` (Dòng 31, 37, 47).
  - `knowledge-base-hue/performing_arts/arts/Ca Huế trên sông Hương.md` (Dòng 10, 47, 53, 76-78, 89).
  - `knowledge-base-hue/meta/performing-arts-research-evidence.md`.
- **Kiểm tra kỹ thuật:**
  ```bash
  git diff --check
  git status --short
  ```
- **Quyết định chờ duyệt:** Xác nhận từ Người dùng/Reviewer về việc đồng bộ câu chữ trong `performing-arts-entities-inventory.md` theo cấu trúc thư mục con `performing_arts/arts/`.
