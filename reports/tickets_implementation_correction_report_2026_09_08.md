# Implementation Correction Report: Du lịch Huế - Nhánh vé tham quan và trải nghiệm (Tickets)

Implementer: Implementer (Gemini 3.8 Flash High)
Date: 2026-09-08
Canonical guide: `knowledge-base-hue/tourism/tickets/tickets-research-and-entities-inventory.md`
Review report: `reports/tickets_codex_review_2026_09_08.md`

---

## 1. Phạm vi sửa đổi (Correction Scope)

Thực hiện đầy đủ và triệt để 100% các điểm trong Correction Delta theo yêu cầu của Reviewer Codex tại `reports/tickets_codex_review_2026_09_08.md` và `session_prompt/CURRENT_HANDOFF.md`:
- Khắc phục 03 Major Findings liên quan đến tính chính xác của ngày miễn phí vé và chuẩn hóa địa giới hành chính theo Nghị quyết 1675/NQ-UBTVQH15 (hiệu lực từ 01/07/2025).
- Khắc phục 03 Minor Findings liên quan đến số hiệu quyết định, mốc phân loại sức chứa thuyền Ca Huế và nhấn mạnh tiêu chí độ tuổi trẻ em.
- Đồng bộ lại các nội dung tương ứng trong hồ sơ kiểm chứng `knowledge-base-hue/meta/tourism-research-evidence.md`.

---

## 2. Chi tiết các thay đổi đã thực hiện

### Major Finding 1: Loại bỏ ngày miễn vé 30/4 và 01/5 tại Di tích Hải Vân Quan
- **Tệp chỉnh sửa:** `knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md` (dòng 82–83) và `knowledge-base-hue/meta/tourism-research-evidence.md` (dòng 1953).
- **Hành động:** Đã xóa bỏ hoàn toàn 2 gạch đầu dòng về việc miễn phí ngày 30/4 và ngày 01/5. Căn cứ chuẩn xác theo toàn văn Nghị quyết số 05/2026/NQ-HĐND ngày 22/05/2026 của HĐND thành phố Huế, các ngày lễ được miễn vé cho công dân Việt Nam gồm: Tết Nguyên Đán, 26/3 (Giải phóng Huế), 29/3 (Giải phóng Đà Nẵng), 19/8 (Cách mạng Tháng Tám), 02/9 (Quốc khánh), 23/11 & 24/11 (Ngày Di sản Văn hóa Việt Nam).

### Major Finding 2: Cập nhật địa giới hành chính đỉnh đèo Hải Vân
- **Tệp chỉnh sửa:** `knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md` (dòng 19).
- **Hành động:** Đã chuẩn hóa địa danh hành chính theo Nghị quyết 1675/NQ-UBTVQH15: Di tích tọa lạc trên đường phân định giữa **xã Chân Mây – Lăng Cô, thành phố Huế** (trước ngày 01/07/2025 là thị trấn Lăng Cô, huyện Phú Lộc) và **phường Hải Vân, thành phố Đà Nẵng** (trước ngày 01/07/2025 là phường Hòa Hiệp Bắc, quận Liên Chiểu), đồng bộ hoàn toàn với file canonical `knowledge-base-hue/tourism/Đèo Hải Vân.md`.

### Major Finding 3: Cập nhật địa giới hành chính Không gian lưu niệm Lê Bá Đảng
- **Tệp chỉnh sửa:** `knowledge-base-hue/tourism/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md` (dòng 155, 156 và dòng 298).
- **Hành động:** Đã chuyển đổi địa chỉ từ `xã Thủy Bằng` thành **Thôn Kim Sơn, phường Thủy Xuân, thành phố Huế** (chú thích rõ khu vực xã Thủy Bằng cũ trước khi sáp nhập vào phường Thủy Xuân theo Nghị quyết số 1675/NQ-UBTVQH15 có hiệu lực từ ngày 01/07/2025), giải quyết triệt để mâu thuẫn nội bộ với File 2.

### Minor Finding 1: Số hiệu quyết định cũ bị thay thế về Quy chế Ca Huế
- **Tệp chỉnh sửa:** `knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` (dòng 79) và `meta/tourism-research-evidence.md` (dòng 1973).
- **Hành động:** Đã sửa số hiệu quyết định ngày 03/05/2024 từ `24/2024/QĐ-UBND` thành **`21/2024/QĐ-UBND`** theo đúng văn bản lưu trữ công báo.

### Minor Finding 2: Đồng bộ mốc phân loại thuyền đơn và thuyền đôi Ca Huế
- **Tệp chỉnh sửa:** `knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` (dòng 86–87).
- **Hành động:** Đã điều chỉnh mốc phân loại sức chứa thành **dưới 15 khách** (thuyền đơn) và **từ 15 khách trở lên** (thuyền đôi), đồng bộ hoàn toàn với dòng 127 và quy chế thực tế tại Bến Tòa Khâm.

### Minor Finding 3: Đồng bộ diễn đạt tiêu chuẩn trẻ em Quần thể Di tích Cố đô Huế
- **Tệp chỉnh sửa:** `knowledge-base-hue/tourism/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md` (dòng 119–124 và dòng 135).
- **Hành động:** Diễn đạt rõ ràng **độ tuổi 7–12 tuổi** là căn cứ pháp lý chính thức của Nghị quyết số 55/2025/NQ-HĐND (dưới 7 tuổi miễn phí hoàn toàn); mốc chiều cao dưới 1,2m chỉ mang tính hỗ trợ nhận diện nhanh tại thực địa. Đồng thời bổ sung đầy đủ các ngày lễ miễn vé cho công dân Việt Nam (19/8 và 23/11).

---

## 3. Cách đã chạy thật (Verification Commands & Results)

1. `git diff --check`:
   - Trả về mã thoát 0 (sạch sẽ, không có bất kỳ xung đột hay lỗi định dạng).
2. `git diff --no-index --check /dev/null <file>` trên cả 5 file tickets:
   - Output chẩn đoán hoàn toàn rỗng, không có trailing whitespace.
3. Rà soát định dạng answer-facing:
   - Cả 5 file đều giữ đúng 01 H1 khớp chính xác tên file, không YAML frontmatter, không URL ngoài, không wiki-link, không nhắc đuôi `.md`, không metadata RAG.

---

## 4. Bàn giao cho Reviewer

- Toàn bộ 03 Major Findings và 03 Minor Findings đã được khắc phục hoàn toàn trong một batch duy nhất.
- Handoff hiện hành tại `session_prompt/CURRENT_HANDOFF.md` đã được chuyển giao sang Reviewer Codex để tiến hành tái thẩm định (re-review).
