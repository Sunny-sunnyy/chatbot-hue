# Codex Re-Review: Performing Arts Batch 01 (Ca Huế trên sông Hương & Duyệt Thị Đường)

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-09-05
Canonical guide: `knowledge-base-hue/meta/performing-arts-template.md` & `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md`
Implementation report: `reports/performing_arts_batch_01_implementation_correction_report_2026_09_05.md`

## 1. Phạm vi đã review

Reviewer đã tái thẩm định độc lập gói hiệu chỉnh (Focused Correction) của Implementer cho 2 thực thể thuộc Batch 01 domain `performing_arts`:
- `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`
- `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Ca Huế trên sông Hương.md`
- `/home/minhhieu/hue_rag/knowledge-base-hue/meta/performing-arts-research-evidence.md`
- Báo cáo Implementer: `reports/performing_arts_batch_01_implementation_correction_report_2026_09_05.md`
- Bàn giao: `session_prompt/CURRENT_HANDOFF.md`

## 2. Findings và Kết quả xử lý

### Đánh giá các phát hiện trước đó:
1. **[MAJOR M1] Tác quyền tuồng Đào Tấn (Duyệt Thị Đường: Dòng 47):**
   - *Kết quả rà soát:* Đã đính chính triệt để. Thay thế bằng các trích đoạn tuồng mẫu mực đích thực của danh nhân Đào Tấn (*Kỷ Lan Anh* trong *Hộ sanh đàn*, *Trầm Hương Các*) cùng các trích đoạn tuồng cổ kinh điển (*Kim Lân biệt mẹ* từ *Sơn Hậu*, *Phụng Nghi Đình*, *Ngọn lửa Hồng Sơn*). Không còn gán nhầm *Kim Thạch kỳ duyên* của Bùi Hữu Nghĩa cho Đào Tấn.
   - *Trạng thái:* **ĐÃ ĐÓNG (RESOLVED)**.
2. **[MAJOR M2] Cấu trúc thư mục `performing_arts/arts/`:**
   - *Kết quả rà soát:* Cả 11 tệp thực thể hiện nằm trong thư mục con `arts/`, tương đồng hoàn toàn với mô hình `heritages/heritage/` đã được người dùng nghiệm thu. Khuyến nghị chuẩn hóa giữ mô hình này và cập nhật câu chữ tại `performing-arts-entities-inventory.md:L9-13`.
   - *Trạng thái:* **CHỜ USER XÁC NHẬN ĐIỀU PHỐI (PENDING USER CONFIRMATION)**.
3. **[MINOR m1] Ngưỡng hành khách trong quy chế Ca Huế (Ca Huế: Dòng 76):**
   - *Kết quả rà soát:* Đã cập nhật chuẩn xác theo Quyết định số 21/2024/QĐ-UBND với ngưỡng 15 khách (thuyền đơn <15 khách: tối thiểu 07 người; thuyền đôi >=15 khách: tối thiểu 08 người).
   - *Trạng thái:* **ĐÃ ĐÓNG (RESOLVED)**.
4. **[MINOR m2] Hệ thống 31 bài bản Ca Huế (Ca Huế: Dòng 47 & 53):**
   - *Kết quả rà soát:* Đã phân định minh bạch về mặt khoa học di sản: 25 bài bản đang thực hành diễn xướng thường xuyên và 6 bài bản cổ chữ Hán đang tiếp tục được nghiên cứu phục dựng.
   - *Trạng thái:* **ĐÃ ĐÓNG (RESOLVED)**.
5. **[MINOR m3] Ngữ cảnh chunking H3 (Duyệt Thị Đường: Dòng 31 & 37):**
   - *Kết quả rà soát:* Đã bổ sung anchor ngữ cảnh "tại Duyệt Thị Đường" ở câu đầu của cả 2 tiểu mục H3, đảm bảo trích xuất chunk độc lập đạt độ chính xác cao.
   - *Trạng thái:* **ĐÃ ĐÓNG (RESOLVED)**.

### Rà soát phát hiện mới:
- Không có phát hiện blocker hay major mới.
- Các cải tiến bổ sung của Implementer (chuẩn hóa an toàn đường thủy nội địa, cự ly neo đậu >=50m, định lượng 2-3 camera IOC, bổ sung phường Phú Xuân) đều có căn cứ pháp lý và nguồn đối chiếu xác thực.

## 3. Cách Reviewer chạy lại thật

1. **Kiểm tra cú pháp và định dạng Git:**
   ```bash
   git diff --check
   git status --short
   ```
   Kết quả: Mã thoát 0, không có lỗi định dạng hay khoảng trắng thừa.
2. **Đọc trực tiếp exact diff và toàn văn các tệp đã sửa:**
   - Đọc các dòng 28–50 của `Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`.
   - Đọc các dòng 10, 45–55, 70–92 của `Ca Huế trên sông Hương.md`.
   - Đối chiếu với hồ sơ bằng chứng `performing-arts-research-evidence.md`.

## 4. Kết quả quan sát

- Cả 2 tệp thực thể đáp ứng hoàn hảo tiêu chuẩn Markdown RAG Clean: mở đầu H1 `#`, không YAML frontmatter, không chứa mục `## Nguồn dữ liệu` trong body answer-facing, không có liên kết nội bộ `[[]]`.
- Dữ liệu tri thức đạt độ chuẩn xác cao về lịch sử văn hóa, sân khấu học, âm nhạc cổ truyền và pháp lý quản lý du lịch văn hóa mốc 05/09/2026.
- Địa giới hành chính cập nhật đúng theo mô hình thành phố Huế trực thuộc Trung ương gồm quận Phú Xuân và quận Thuận Hóa.

## 5. Giới hạn hoặc phần chưa chạy

- Báo cáo này giới hạn trong việc thẩm định lại Batch 01 (2 tệp).
- 9 tệp thực thể còn lại trong `knowledge-base-hue/performing_arts/arts/` sẽ được thẩm định trong các batch tiếp theo.

## 6. Decision và bước tiếp theo

- **Technical Decision:** `ready_for_user_confirmation` cho 2 tệp thực thể Batch 01.
- **Khuyến nghị điều phối cấu trúc thư mục (Finding M2):** Kính trình Người dùng phê duyệt giữ cấu trúc chuẩn hóa `knowledge-base-hue/performing_arts/arts/*.md` và cho phép cập nhật đồng bộ văn bản điều phối tại `performing-arts-entities-inventory.md`.
- **Bước tiếp theo:** Sau khi Người dùng duyệt kết quả Batch 01, tiếp tục triển khai sub-agent thẩm định Batch 02 (các chương trình gắn với Festival Huế hoặc đại nhạc hội đương đại).
