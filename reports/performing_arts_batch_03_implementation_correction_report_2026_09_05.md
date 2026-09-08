# Implementation Report: Performing Arts Batch 03 Correction

Implementer: Implementer  
Date: 2026-09-05  
Canonical guide: `knowledge-base-hue/meta/performing-arts-template.md`, `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md`  
Review report căn cứ: `reports/performing_arts_batch_03_codex_review_2026_09_05.md`  

---

## 1. Phạm vi

Thực hiện gói hiệu chỉnh tập trung (Focused Correction) trong một batch duy nhất nhằm khắc phục toàn diện 04 phát hiện Major và 04 phát hiện Minor trên 02 tệp thực thể thuộc nhóm "Đại nhạc hội và chương trình biểu diễn đương đại tạo dấu ấn":
1. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế Wonderverse Music Fest.md` (Major M1, Major M2, Minor m2, Minor m3)
2. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế by Light – The Live Show.md` (Major M3, Major M4, Minor m1, Minor m2)

Ranh giới bảo toàn:
- Bảo toàn nguyên trạng 02 tệp đã đạt chuẩn xuất sắc **PASS 100%** trong Batch 03:
  - `knowledge-base-hue/performing_arts/arts/Mega Booming – Huế.md`
  - `knowledge-base-hue/performing_arts/arts/Đêm Hoàng cung – Dạ yến Hoàng cung.md`
- Bảo toàn toàn bộ 7 tệp thực thể thuộc Batch 01 và Batch 02 đã nghiệm thu.
- Tuyệt đối tuân thủ chỉ đạo của Người dùng: Không can thiệp bất kỳ tệp hay thư mục nào ngoài `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts`.
- Đạt chuẩn Markdown RAG Clean: Khởi đầu bằng H1 `#`, không YAML frontmatter, không mục `## Nguồn dữ liệu`, không wiki-link `[[]]`, các section độc lập cao.

---

## 2. Thay đổi chính

### 2.1. Tệp `Huế Wonderverse Music Fest.md`
1. **[MAJOR M1] Bổ sung khối `## Thông tin chung` và chuẩn hóa tiêu đề `## Tổng quan`:**
   - Đã bổ sung khối thuộc tính Core Metadata ngay sau tiêu đề H1 gồm: Tên chính thức, Tên viết tắt / gọi khác (HWF), Loại hình, Tính chất tổ chức, Thời điểm lần đầu tổ chức (30/08 – 01/09/2026), Không gian biểu diễn, Cơ quan chỉ đạo / chủ trì, Đơn vị phát triển IP và đồng sản xuất.
   - Sửa tiêu đề H2 từ `## Tổng quan sự kiện / chương trình` thành `## Tổng quan`.
2. **[MAJOR M2] Đính chính địa giới hành chính và tính chất công cộng của Quảng trường Văn hóa – Thể thao:**
   - Sửa đoạn 1 & đoạn 2 mục Không gian biểu diễn: Xác định rõ đây là công trình công cộng của Nhà nước tại số 01 đường Hà Huy Tập, thuộc địa bàn **phường Vỹ Dạ, quận Thuận Hóa, TP. Huế**, chỉ tiếp giáp/đối diện Khu đô thị An Cựu City chứ không thuộc dự án bất động sản tư nhân An Cựu City.
   - Sửa dòng `- **Địa điểm:**` tại mục kỳ 2026: Đổi từ cách ghi lưỡng lự "phường An Đông/Xuân Phú" thành: `Quảng trường Văn hóa – Thể thao thành phố Huế (số 01 đường Hà Huy Tập, phường Vỹ Dạ, quận Thuận Hóa, TP. Huế)`.
3. **[MINOR] Tiết chế mỹ từ PR quảng cáo, loại bỏ thuật ngữ nội bộ RAG và bổ sung Beyond Communication:**
   - Bổ sung **Beyond Communication** vào đơn vị phát triển IP và đồng sản xuất cùng Carlsberg Việt Nam (Huda).
   - Thay thế các từ mang sắc thái PR cảm tính ("bùng nổ", "độc bản", "huyền thoại") sang văn phong bách khoa trung tính ("sôi động", "đặc trưng", "tiêu biểu").
   - Loại bỏ thuật ngữ nội bộ RAG tại câu dẫn mục Ranh giới thực thể.

### 2.2. Tệp `Huế by Light – The Live Show.md`
1. **[MAJOR M3] Loại bỏ triệt để thuật ngữ nội bộ "hệ thống RAG" (Dòng 71):**
   - Đã thay thế câu dẫn mang tính nội bộ kỹ thuật thành: `Để đảm bảo tính chuẩn xác và tránh nhầm lẫn với các hoạt động biểu diễn khác tại Cố đô Huế, Huế by Light – The Live Show cần được phân định rõ ràng với các thực thể liên quan:`.
2. **[MAJOR M4] Đính chính tên nghệ sĩ thành viên nhóm Limebócx (Dòng 53):**
   - Đã sửa cụm từ nhầm lẫn "Chu Duyên Tùng" thành tên chính xác: `Hà Đăng Tùng (nghệ danh Đờ Tùng – phụ trách guitar, hiệu ứng điện tử và beatbox)`.
3. **[MINOR] Bổ sung danh xưng thực thể tại mục thông tin khán giả và tiết chế mỹ từ:**
   - Bổ sung định danh thực thể "Huế by Light – The Live Show" vào câu mở đầu mục thông tin khán giả (dòng 80) để chunk đứng độc lập.
   - Tiết chế các từ ngữ ca ngợi cảm tính: sửa "hiện đại bậc nhất" thành "tiêu chuẩn kỹ thuật cao", "biến ảo kỳ ảo" thành "biến chuyển sống động", "Thành công vang dội" thành "Sự đón nhận tích cực của công chúng".

---

## 3. Cách đã chạy thật

1. **Điều phối 02 sub-agent chuyên trách thực thi độc lập:**
   - Sub-agent 1: Hue Wonderverse Subagent (`8602cc3e-8a4c-4661-8699-23120a1ddfde`).
   - Sub-agent 2: Hue by Light Subagent (`b06ead98-e0be-4a29-afba-abbaa01887e6`).
   - Khóa mốc thời gian hệ thống **05/09/2026**, áp dụng nghiêm ngặt `meta/performing-arts-template.md` và thực hiện **100% các truy vấn web search bằng tiếng Việt** để xác thực các thông tin trước khi sửa.
2. **Kiểm tra định dạng và ranh giới:**
   ```bash
   git diff --check
   git status --short knowledge-base-hue/performing_arts/
   ```
   Kết quả: Mã thoát 0, sạch lỗi khoảng trắng và cú pháp.

---

## 4. Kết quả quan sát

- **Huế Wonderverse Music Fest:** Khối `## Thông tin chung` đã được bổ sung đầy đủ, đồng bộ hoàn toàn với cấu trúc của toàn bộ 10 thực thể còn lại trong domain; địa giới hành chính số 01 Hà Huy Tập, phường Vỹ Dạ, quận Thuận Hóa chuẩn hóa 100%; ngôn từ bách khoa khách quan.
- **Huế by Light – The Live Show:** 100% sạch thuật ngữ RAG nội bộ; tên nghệ sĩ Hà Đăng Tùng (nhóm Limebócx) được đính chính chuẩn xác; các chunk thông tin khán giả tự đứng độc lập hoàn hảo.
- Toàn bộ 11/11 tệp thực thể của domain `performing_arts` hiện đã hoàn tất qua 3 đợt review/correction và đạt trạng thái hoàn thiện triệt để.

---

## 5. Lỗi và giới hạn

Không có lỗi hoặc giới hạn đã biết trong phạm vi hiệu chỉnh này.

---

## 6. Handoff cho Reviewer

- **Tài liệu khuyến nghị Reviewer đọc trước:**
  - `knowledge-base-hue/performing_arts/arts/Huế Wonderverse Music Fest.md` (Dòng 3–13, 28, 53, 73–74, 85).
  - `knowledge-base-hue/performing_arts/arts/Huế by Light – The Live Show.md` (Dòng 39, 41, 53, 67, 71, 80).
- **Kiểm tra kỹ thuật:**
  ```bash
  git diff --check
  git status --short
  ```
