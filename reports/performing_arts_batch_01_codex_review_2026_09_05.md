# Codex Review: Performing Arts Batch 01 (Ca Huế trên sông Hương & Chương trình nghệ thuật cung đình tại Duyệt Thị Đường)

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-05
Canonical guide: `knowledge-base-hue/meta/performing-arts-template.md` & `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md`
Implementation report / evidence: `knowledge-base-hue/meta/performing-arts-research-evidence.md`

## 1. Phạm vi đã review

Reviewer và hai sub-agent thẩm định độc lập chuyên trách đã kiểm tra toàn diện hai tệp thực thể đầu tiên thuộc domain `performing_arts` mốc thời gian 05/09/2026:
- `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Ca Huế trên sông Hương.md`
- `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`
- Hồ sơ kiểm chứng tại `/home/minhhieu/hue_rag/knowledge-base-hue/meta/performing-arts-research-evidence.md`
- Cấu trúc thư mục thực tế tại `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/`

Kiểm tra đối chiếu độc lập gồm:
1. Chuẩn Markdown RAG Clean (khởi đầu H1, không YAML frontmatter, không `## Nguồn dữ liệu`, không `[[]]` wiki-links, tính độc lập của từng chunk H2/H3).
2. Ranh giới thực thể (Entity boundary: phân định giữa chương trình biểu diễn với bản thể di sản phi vật thể và di tích kiến trúc).
3. Thẩm tra sự thật bằng web search và đối chiếu nguồn thẩm quyền mốc 05/09/2026 (Nghị quyết 175/2024/QH15 về địa giới hành chính TP. Huế trực thuộc Trung ương; Quyết định số 21/2024/QĐ-UBND về Quy chế quản lý Ca Huế; hồ sơ UNESCO và Cục Di sản văn hóa; kịch mục chính thức của HMCC và Nhà hát Nghệ thuật Truyền thống Cung đình Huế; lịch sử sân khấu tuồng Việt Nam).

## 2. Findings

### Blocker (0 finding)
- Không có lỗi blocker làm gián đoạn pipeline RAG hoặc sai lệch hoàn toàn bản chất di sản.

### Major (2 findings)

#### Finding M1: Ghi sai tác giả kiệt tác tuồng *Kim Thạch kỳ duyên*
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`, Dòng 47.
- **Hiện trạng:**
  ```markdown
  - **Các trích đoạn mẫu mực:** Gồm các trích đoạn nổi tiếng như *Kim Thạch kỳ duyên* (vở tuồng của Đào Tấn), trích đoạn *Phụng Nghi Đình*, *Ngọn lửa Hồng Sơn*, hay hoạt cảnh dân gian cung đình hóa *Ông Già cõng vợ đi xem hội*.
  ```
- **Requirement:** Mục 2.1 & 2.5 của `meta/performing-arts-template.md`: Tri thức phải chuẩn xác theo lịch sử văn hóa, không đưa dữ kiện sai lệch vào nội dung RAG.
- **Evidence:** *Kim Thạch kỳ duyên* là kiệt tác tuồng nổi tiếng bậc nhất của danh sĩ, Thủ khoa Bùi Hữu Nghĩa (1807–1872, Nam Bộ), hoàn thành khoảng năm 1858–1862; không phải sáng tác của Đào Tấn. Đào Tấn là tác giả của các vở tuồng kinh điển như *Hộ sanh đàn*, *Cổ thành*, *Trầm hương các*, *Khuê các anh hùng*.
- **Tác động:** Sai lệch kiến thức lịch sử sân khấu học và tác quyền văn học cổ điển Việt Nam, làm giảm độ tin cậy của corpus tri thức.
- **Tiêu chí đóng:** Hiệu chỉnh chính xác tác giả: `*Kim Thạch kỳ duyên* (của tác giả Bùi Hữu Nghĩa)` hoặc thay bằng một vở tuồng thực sự của Đào Tấn (ví dụ `*Hộ sanh đàn* (vở tuồng của Đào Tấn)`).

#### Finding M2: Cấu trúc thư mục chưa đồng bộ với văn bản Inventory điều phối
- **Vị trí:** Đường dẫn lưu trữ 11 tệp thực thể tại `knowledge-base-hue/performing_arts/arts/*.md`.
- **Requirement:** `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md` (Dòng 9–13) quy định:
  *"Implementer sẽ tạo đúng 11 file entity dưới đây, đặt trực tiếp trong knowledge-base-hue/performing_arts/. Mỗi thực thể chỉ có một file canonical; không tạo lại các thư mục phân loại..."*
- **Evidence:** Cả 11 tệp hiện được đặt trong thư mục con `arts/` (`knowledge-base-hue/performing_arts/arts/`), đồng nhất với cấu trúc `heritages/heritage/`.
- **Tác động:** Lệch ranh giới đường dẫn giữa quy định văn bản và triển khai thực tế.
- **Tiêu chí đóng:** Cần một quyết định điều phối chính thức từ User/Lead Reviewer: Nếu giữ mô hình thư mục con `performing_arts/arts/` (để đồng bộ với `heritages/heritage/`), cần cập nhật văn bản điều phối tại `performing-arts-entities-inventory.md`; nếu giữ nguyên văn bản inventory, di chuyển 11 tệp ra thẳng thư mục gốc `performing_arts/`.

### Minor (3 findings)

#### Finding m1: Ngưỡng hành khách trong quy chế biên chế nhân sự Ca Huế trên thuyền
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Ca Huế trên sông Hương.md`, Dòng 75.
- **Hiện trạng:** Ghi `tối thiểu 7 diễn viên, nhạc công đối với thuyền nhỏ (chở dưới 20 hành khách) và tối thiểu 8 diễn viên, nhạc công đối với thuyền lớn (chở từ 20 hành khách trở lên)`.
- **Requirement & Evidence:** Quyết định số 21/2024/QĐ-UBND của UBND tỉnh Thừa Thiên Huế (Quy chế quản lý và tổ chức hoạt động biểu diễn Ca Huế) quy định phân loại theo thuyền đơn / thuyền đôi với ngưỡng **15 hành khách**: Thuyền đơn (dưới 15 khách) tối thiểu 7 diễn viên, nhạc công; Thuyền đôi (từ 15 khách trở lên) tối thiểu 8 diễn viên, nhạc công.
- **Tác động:** Lệch ngưỡng số lượng khách quy định theo văn bản pháp quy địa phương.
- **Tiêu chí đóng:** Hiệu chỉnh ngưỡng từ `20 hành khách` thành `15 hành khách` (thuyền đơn dưới 15 khách / thuyền đôi từ 15 khách trở lên).

#### Finding m2: Diễn đạt số lượng bài bản Ca Huế chưa phản ánh 6 bài chưa phục dựng
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Ca Huế trên sông Hương.md`, Dòng 47.
- **Hiện trạng:** Ghi `31 bài bản truyền thống được bảo tồn trọn vẹn: 13 điệu Bắc, 5 điệu Nam, 5 điệu Nam xuân, hơi dựng...`.
- **Requirement & Evidence:** Tư liệu Cục Di sản văn hóa (`dsvh.gov.vn`) và Viện Âm nhạc: Hệ thống 31 bài bản truyền thống gồm 25 bài bản đang được thực hành diễn xướng (13 Bắc, 5 Nam, 5 Nam xuân, 2 hơi dựng) và 6 bài bản còn bản nhạc phổ chữ Hán đang tiếp tục được nghiên cứu phục dựng. Diễn đạt "được bảo tồn trọn vẹn" có thể gây ngộ nhận là toàn bộ 31 bài bản đều đang diễn xướng hằng đêm trên thuyền.
- **Tác động:** Diễn đạt chưa phản ánh chính xác trạng thái thực hành di sản.
- **Tiêu chí đóng:** Diễn đạt rõ: 31 bài bản truyền thống, trong đó 25 bài bản đang được diễn xướng thường xuyên và các bài bản còn lưu bản phổ đang được tiếp tục nghiên cứu phục dựng.

#### Finding m3: Tăng cường từ khóa ngữ cảnh chunking tại các tiểu mục H3
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`, Dòng 31 (`### Trình tấu Nhã nhạc cung đình`) và Dòng 37 (`### Các vũ khúc cung đình đặc sắc`).
- **Hiện trạng:** Câu đầu của hai mục H3 viết tiếp dẫn (`Nhã nhạc mở đầu chương trình...`, `Múa cung đình Huế là sự kết tinh...`), thiếu từ khóa không gian "tại Duyệt Thị Đường".
- **Requirement:** Mục 2.6 của `meta/performing-arts-template.md`: Mỗi section quan trọng cần nhắc tên hoặc ngữ cảnh của entity một cách tự nhiên để vẫn hiểu được khi section trở thành một chunk độc lập.
- **Tác động:** Khi hệ thống RAG cắt chunk ở mức tiểu mục H3, ngữ cảnh định danh địa điểm và chương trình có thể bị giảm độ nổi bật.
- **Tiêu chí đóng:** Bổ sung ngữ cảnh "trong chương trình tại Duyệt Thị Đường" hoặc "trình diễn tại Duyệt Thị Đường" vào câu đầu của hai tiểu mục H3.

## 3. Cách Reviewer chạy lại thật

1. **Kiểm tra cấu trúc và diff repo:**
   ```bash
   git status --short
   git diff --check
   ```
2. **Kiểm tra định dạng Markdown và rà soát cú pháp:**
   - Đọc trực tiếp toàn bộ 100% dòng của `Ca Huế trên sông Hương.md` và `Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`.
   - Đối chiếu chéo với `performing-arts-research-evidence.md`.
3. **Thực hiện tra cứu và kiểm chứng độc lập qua Web Search:**
   - Nghị quyết số 175/2024/QH15 và Nghị quyết 1314/NQ-UBTVQH15 về đơn vị hành chính TP. Huế trực thuộc Trung ương (hiệu lực 01/01/2025).
   - Quyết định số 21/2024/QĐ-UBND ngày 03/05/2024 của UBND tỉnh Thừa Thiên Huế ban hành Quy chế quản lý biểu diễn Ca Huế.
   - Cơ sở dữ liệu Cục Di sản văn hóa (`dsvh.gov.vn`) về 31 bài bản Ca Huế và Quyết định số 1877/QĐ-BVHTTDL ngày 08/06/2015.
   - Lịch sử sân khấu tuồng Việt Nam: Vở tuồng *Kim Thạch kỳ duyên* của Thủ khoa Bùi Hữu Nghĩa.
   - Hồ sơ kịch mục và thời gian hoạt động của Nhà hát Nghệ thuật Truyền thống Cung đình Huế (HMCC).

## 4. Kết quả quan sát

- **Markdown RAG Clean:** Cả 2 tệp đều tuân thủ nghiêm ngặt quy định: bắt đầu bằng H1 `#`, không YAML frontmatter, không có `## Nguồn dữ liệu` trong body answer-facing, không wiki-links `[[]]`, không chứa thông tin vé biến động.
- **Ranh giới thực thể:** Xử lý rất tốt, không bị đồng nhất chương trình biểu diễn với bản thể di sản hay di tích kiến trúc toàn cảnh.
- **Địa giới hành chính 09/2026:** Đã cập nhật chuẩn xác: Bến Tòa Khâm thuộc quận Thuận Hóa; Bến Nghinh Lương Đình và Nhà hát Duyệt Thị Đường thuộc phường Phú Xuân, quận Phú Xuân, TP. Huế trực thuộc Trung ương.
- **Tồn tại kỹ thuật:** Xuất hiện lỗi tri thức văn học tại tệp Duyệt Thị Đường (gán sai tác giả vở tuồng) và chi tiết số liệu hành khách tại tệp Ca Huế.

## 5. Giới hạn hoặc phần chưa chạy

- Đợt review này mới hoàn tất cho Batch 01 (2 tệp: `Ca Huế trên sông Hương.md` và `Chương trình nghệ thuật cung đình tại Duyệt Thị Đường.md`).
- 9 tệp thực thể còn lại trong `knowledge-base-hue/performing_arts/arts/` và tệp rỗng `performing_arts_guides.md` chưa được review trong báo cáo này.

## 6. Decision và bước tiếp theo

- **Technical Decision:** `changes_requested` (Yêu cầu chỉnh sửa khắc phục 1 lỗi Major M1 và các lỗi Minor m1, m2, m3).
- **Quyết định điều phối:** Người dùng xác nhận phương án cấu trúc thư mục (chấp thuận giữ cấu trúc `performing_arts/arts/` hay di chuyển ra `performing_arts/`).
- **Bước tiếp theo:**
  1. Gửi báo cáo chi tiết này tới Implementer để thực hiện gói hiệu chỉnh nhỏ (Focused Correction) cho 2 tệp trên.
  2. Tiếp tục triển khai sub-agent thẩm định cho nhóm thực thể tiếp theo thuộc domain Performing Arts theo chỉ đạo của Người dùng.
