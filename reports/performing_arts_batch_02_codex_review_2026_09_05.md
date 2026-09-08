# Codex Review: Performing Arts Batch 02 (5 thực thể gắn với Festival Huế)

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-05
Canonical guide: `knowledge-base-hue/meta/performing-arts-template.md` & `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md`
Implementation report / evidence: `knowledge-base-hue/meta/performing-arts-research-evidence.md`

## 1. Phạm vi đã review

Reviewer cùng 5 sub-agent chuyên trách độc lập đã thẩm định và kiểm chứng chéo toàn diện 5 tệp thực thể thuộc nhóm "Chương trình nghệ thuật gắn với Festival Huế" trong domain `performing_arts` tại mốc thời gian 05/09/2026:
1. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Tuần lễ Festival Nghệ thuật Quốc tế Huế.md`
2. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Lễ hội đường phố Sắc màu văn hóa.md`
3. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Đêm nhạc Trịnh Công Sơn tại Huế.md`
4. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Tuần lễ Âm nhạc Quốc tế Huế.md`
5. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế Symphony – Bản Giao hưởng Cố đô.md`
- Hồ sơ kiểm chứng tại `knowledge-base-hue/meta/performing-arts-research-evidence.md`

Quy trình thẩm định độc lập gồm:
- Rà soát 100% chuẩn Markdown RAG Clean (khởi đầu H1, không YAML frontmatter, không mục `## Nguồn dữ liệu`, không wiki-link `[[]]`, khả năng tự đứng độc lập của từng chunk H2/H3).
- Thẩm định ranh giới thực thể (Entity boundary) giữa các sự kiện thành phần với Festival Huế bốn mùa tổng thể và giữa các chương trình biểu diễn với nhau.
- Kiểm chứng thực tế thời gian thực (05/09/2026) bằng web search và đối chiếu các nguồn thẩm quyền: Nghị quyết số 175/2024/QH15, Nghị quyết số 1314/NQ-UBTVQH15, Nghị quyết số 1675/NQ-UBTVQH15 về đơn vị hành chính TP. Huế trực thuộc Trung ương; Cổng TTĐT Bộ VHTTDL, Cục Du lịch Quốc gia, Cổng TTĐT TP. Huế (`hue.gov.vn`), Trung tâm Bảo tồn Di tích Cố đô Huế (HMCC), và báo chí chính thống.

## 2. Findings

### Blocker (0 finding)
- Không có lỗi blocker làm gián đoạn pipeline RAG.

### Major (3 findings trên 2 tệp)

#### Finding M1: Khuyết thiếu kỳ tổ chức Tuần lễ Festival Nghệ thuật Quốc tế Huế 2026
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Tuần lễ Festival Nghệ thuật Quốc tế Huế.md`, mục `## Các kỳ tổ chức tiêu biểu` (dòng 97–117).
- **Hiện trạng:** Tệp chỉ mới ghi nhận kỳ 2022 và kỳ 2024, hoàn toàn bỏ trống kỳ 2026.
- **Requirement:** Mục 2.3 & 2.4 của `meta/performing-arts-template.md`: Tại mốc thời gian 05/09/2026, các sự kiện đã diễn ra phải được cập nhật đầy đủ và phân biệt đúng trạng thái tổ chức.
- **Evidence:** Tuần lễ Festival Nghệ thuật Quốc tế Huế 2026 đã diễn ra thành công từ ngày 13/06/2026 đến ngày 18/06/2026 với chủ đề "Di sản văn hóa với hội nhập và phát triển", Khai mạc kết hợp không gian ánh sáng di sản "Hoàng cung Huyễn Dạ" tại Đại Nội và tích hợp Tuần lễ Âm nhạc Quốc tế Huế tại sân khấu nổi bên bờ sông Hương.
- **Tác động:** Giảm tính cập nhật của corpus tri thức, gây thiếu hụt dữ liệu khi người dùng truy vấn về kỳ Festival Huế năm 2026.
- **Tiêu chí đóng:** Bổ sung tiểu mục `### Kỳ Tuần lễ Festival Nghệ thuật Quốc tế Huế 2026 (13/6/2026 – 18/6/2026)` với đầy đủ trạng thái "Đã diễn ra", chủ đề và các đặc điểm nghệ thuật nổi bật.

#### Finding M2: Sai lệch địa giới hành chính khu vực Quảng trường Ngọ Môn (kỳ 2023)
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Tuần lễ Âm nhạc Quốc tế Huế.md`, dòng 10 và dòng 60.
- **Hiện trạng:** Ghi `Quảng trường Ngọ Môn (Đại Nội Huế, phường Đông Ba, quận Phú Xuân, thành phố Huế)`.
- **Requirement:** Mục 2.5 của `meta/performing-arts-template.md` và Nghị quyết số 1675/NQ-UBTVQH15: Sau đợt sắp xếp ĐVHC năm 2025, 6 phường trung tâm bờ bắc (gồm Đông Ba, Thuận Hòa, Thuận Lộc...) đã sáp nhập thành phường Phú Xuân mới. Toàn bộ repo chuẩn hóa địa giới Đại Nội / Ngọ Môn là **phường Phú Xuân, quận Phú Xuân**.
- **Evidence:** Đồng bộ với `Huế by Light – The Live Show.md`, `Mega Booming – Huế.md` và `performing-arts-research-evidence.md`.
- **Tác động:** Xung đột chéo dữ liệu địa giới hành chính (knowledge contradiction) giữa các chunk khi truy vấn về địa chỉ của Quảng trường Ngọ Môn.
- **Tiêu chí đóng:** Hiệu chỉnh `phường Đông Ba` thành `phường Phú Xuân` tại dòng 10 và dòng 60.

#### Finding M3: Thiếu phân định ranh giới thực thể với "Tuần lễ Festival Nghệ thuật Quốc tế Huế"
- **Vị trí:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Tuần lễ Âm nhạc Quốc tế Huế.md`, mục `## Mối quan hệ với các chương trình và sự kiện liên quan` (dòng 108–117).
- **Requirement:** Mục 2.2 của `meta/performing-arts-template.md`: Phân định ranh giới rõ ràng với các thực thể liên quan dễ nhầm lẫn.
- **Evidence:** Tệp đã so sánh với *Festival Huế tổng thể*, *Huế by Light*, *Đêm nhạc Trịnh Công Sơn*, *Huế Wonderverse*, *Huế Symphony*, nhưng bỏ sót chính thực thể dễ gây nhầm lẫn nhất là **Tuần lễ Festival Nghệ thuật Quốc tế Huế** (thực thể số 3 trong inventory).
- **Tác động:** Khi truy vấn phân biệt giữa hai "Tuần lễ" của Cố đô Huế, mô hình RAG có thể bị nhầm lẫn tính chất đa ngành với chuyên sâu âm nhạc.
- **Tiêu chí đóng:** Bổ sung 01 gạch đầu dòng phân định rõ: *Tuần lễ Festival Nghệ thuật Quốc tế Huế* là tuần lễ tổng hợp đa ngành (múa, xiếc, vũ kịch, thời trang, âm nhạc) làm hạt nhân mùa Hạ; còn *Tuần lễ Âm nhạc Quốc tế Huế* là chương trình chuyên sâu về âm nhạc ngoài trời bên bờ sông Hương.

### Minor (3 findings)

#### Finding m1: Mô tả hình khối bức tượng Trịnh Công Sơn (Đêm nhạc Trịnh Công Sơn - Dòng 144)
- **Hiện trạng:** Ghi là `bức tượng đồng bán thân của nhạc sĩ Trịnh Công Sơn`.
- **Thực tế kiểm chứng:** Tượng khánh thành ngày 28/02/2024 tại Công viên Trịnh Công Sơn là **tượng toàn thân dáng ngồi tựa gốc cây bên cây đàn guitar** (dài 2,3m, rộng 1,6m, cao 1,7m, nặng 500kg), do cố điêu khắc gia Trương Đình Quế sáng tác, doanh nhân Lê Hùng Mạnh (Chủ tịch Công ty Gia Hòa) tài trợ đúc đồng và cùng gia đình cố nhạc sĩ trao tặng TP. Huế.
- **Tiêu chí đóng:** Sửa lại thành tượng toàn thân dáng ngồi tựa gốc cây bên cây đàn guitar do doanh nhân Lê Hùng Mạnh cùng gia đình nhạc sĩ trao tặng.

#### Finding m2: Chuẩn hóa danh xưng cơ quan chủ trì (Tuần lễ Festival Nghệ thuật Quốc tế - Dòng 13)
- **Hiện trạng:** Ghi `Ủy ban Nhân dân tỉnh Thừa Thiên Huế (thành phố Huế trực thuộc Trung ương)`.
- **Tiêu chí đóng:** Chuẩn hóa theo thể thức thành phố trực thuộc Trung ương từ 01/01/2025: `Ủy ban Nhân dân thành phố Huế (trực thuộc Trung ương)`.

#### Finding m3: Lược bỏ một số mỹ từ mang tính quảng bá cảm tính (Tuần lễ Âm nhạc Quốc tế - Dòng 75, 76)
- **Hiện trạng:** Xuất hiện các từ `"bùng nổ"`, `"rực lửa"`, `"đỉnh cao"`.
- **Tiêu chí đóng:** Biên tập lại sang ngôn ngữ trung tính bách khoa: thay `"Sự bùng nổ của âm thanh..."` thành `"Sự kết hợp các tiết tấu pop alternative hiện đại..."`, thay `"giai điệu Latin rực lửa"` thành `"giai điệu Latin sôi động và kỹ thuật điêu luyện"`.

## 3. Cách Reviewer chạy lại thật

1. **Kiểm tra cú pháp và định dạng Git:**
   ```bash
   git diff --check
   git status --short
   ```
2. **Đọc và đối chiếu toàn văn 5 tệp thực thể:**
   - `Tuần lễ Festival Nghệ thuật Quốc tế Huế.md` (137 dòng).
   - `Lễ hội đường phố Sắc màu văn hóa.md` (172 dòng).
   - `Đêm nhạc Trịnh Công Sơn tại Huế.md` (179 dòng).
   - `Tuần lễ Âm nhạc Quốc tế Huế.md` (124 dòng).
   - `Huế Symphony – Bản Giao hưởng Cố đô.md` (136 dòng).
3. **Thực hiện tra cứu đối chiếu độc lập bằng Web Search (05/09/2026):**
   - Nghị quyết số 175/2024/QH15, 1314/NQ-UBTVQH15, 1675/NQ-UBTVQH15 về địa giới hành chính TP. Huế, quận Phú Xuân, quận Thuận Hóa, phường Phú Xuân.
   - Báo cáo kết quả Tuần lễ Festival Nghệ thuật Quốc tế Huế và Tuần lễ Âm nhạc Quốc tế Huế tháng 6/2026 từ Cổng TTĐT TP. Huế, Sở Du lịch và TTXVN.
   - Tư liệu khánh thành tượng nhạc sĩ Trịnh Công Sơn tại Công viên Trịnh Công Sơn ngày 28/02/2024.
   - Báo cáo tổng kết hòa nhạc Huế Symphony tháng 10/2024 từ HMCC, BAA và báo Tuổi Trẻ.

## 4. Kết quả quan sát

| Tệp thực thể | Đánh giá Markdown Clean | Ranh giới thực thể | Xác thực sự thật | Kết luận thẩm định |
|:---|:---:|:---:|:---:|:---:|
| `Lễ hội đường phố Sắc màu văn hóa.md` | ĐẠT 100% | ĐẠT 100% | ĐẠT 100% | **PASS 100%** |
| `Huế Symphony – Bản Giao hưởng Cố đô.md` | ĐẠT 100% | ĐẠT 100% | ĐẠT 100% | **PASS 100%** |
| `Đêm nhạc Trịnh Công Sơn tại Huế.md` | ĐẠT 100% | ĐẠT 100% | ĐẠT 99% | **PASS (Cần sửa 1 lỗi Minor m1)** |
| `Tuần lễ Festival Nghệ thuật Quốc tế Huế.md` | ĐẠT 100% | ĐẠT 100% | ĐẠT 95% | **Changes Requested (M1, m2)** |
| `Tuần lễ Âm nhạc Quốc tế Huế.md` | ĐẠT 100% | Cần bổ sung | ĐẠT 95% | **Changes Requested (M2, M3, m3)** |

## 5. Giới hạn hoặc phần chưa chạy

- Nhóm 4 tệp thực thể còn lại trong inventory (Đại nhạc hội và chương trình biểu diễn đương đại: `Mega Booming – Huế`, `Huế by Light – The Live Show`, `Đêm Hoàng cung – Dạ yến Hoàng cung`, `Huế Wonderverse Music Fest`) chưa thuộc phạm vi báo cáo này và sẽ được thẩm định ở Batch 03.

## 6. Decision và bước tiếp theo

- **Technical Decision:** `changes_requested` (Yêu cầu hiệu chỉnh tập trung đối với 3 tệp: `Tuần lễ Festival Nghệ thuật Quốc tế Huế.md`, `Tuần lễ Âm nhạc Quốc tế Huế.md`, và `Đêm nhạc Trịnh Công Sơn tại Huế.md`).
- **Bước tiếp theo:** Chuyển giao danh mục findings chi tiết cho Implementer thực hiện gói hiệu chỉnh tập trung cho Batch 02 trước khi tiến hành nghiệm thu.
