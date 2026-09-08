# Codex Review: Phase di-tich-vat-the-noi-bat Nhóm Di tích vật thể nổi bật (Thực thể 18 đến 28)

Decision: changes_requested
Reviewer: Codex (Independent Reviewer)
Date: 2026-09-05
Canonical guide: `knowledge-base-hue/meta/heritage-template.md`, `knowledge-base-hue/heritage/heritage-entities-inventory.md`
Implementation report: Báo cáo tự kiểm tra triển khai 11 thực thể di tích vật thể nổi bật của Implementer

---

## 1. Phạm vi đã review

Reviewer đã tiến hành rà soát, kiểm chứng độc lập chuyên sâu đối với toàn bộ 11 tập tin markdown thuộc nhóm Di tích vật thể nổi bật trong thư mục `knowledge-base-hue/heritage/` và đối chiếu với Mục 18 đến 28 trong `knowledge-base-hue/meta/heritage-research-evidence.md`:
1. `knowledge-base-hue/heritage/18 Kinh thành Huế.md`
2. `knowledge-base-hue/heritage/19 Đại Nội Huế.md`
3. `knowledge-base-hue/heritage/20 Chùa Thiên Mụ.md`
4. `knowledge-base-hue/heritage/21 Đàn Nam Giao.md`
5. `knowledge-base-hue/heritage/22 Hổ Quyền.md`
6. `knowledge-base-hue/heritage/23 Điện Hòn Chén.md`
7. `knowledge-base-hue/heritage/24 Cung An Định.md`
8. `knowledge-base-hue/heritage/25 Đàn Xã Tắc.md`
9. `knowledge-base-hue/heritage/26 Hải Vân Quan.md`
10. `knowledge-base-hue/heritage/27 Trường Quốc Học Huế.md`
11. `knowledge-base-hue/heritage/28 Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md`

Tiêu chí kiểm tra trọng tâm:
- **Địa giới hành chính mốc 05/09/2026:** Đối chiếu Nghị quyết số 175/2024/QH15 (Thành phố Huế trực thuộc Trung ương) và Nghị quyết số 1675/NQ-UBTVQH15 (sắp xếp 40 đơn vị hành chính cấp xã mới có hiệu lực từ 01/07/2025).
- **Ranh giới thực thể con theo Inventory:** Tích hợp đúng các công trình con (Kỳ Đài, Phu Văn Lâu, Trấn Bình Đài... trong Kinh thành; Ngọ Môn, Thái Hòa, Kiến Trung, Thế Miếu... trong Đại Nội; Điện Voi Ré trong Hổ Quyền; 4 điểm di tích quốc gia đặc biệt trong Hệ thống di tích Hồ Chí Minh).
- **Cấp xếp hạng & Ranh giới UNESCO 1993:** Phân định chính xác giữa 14 cụm serial ID của UNESCO 1993 với các di tích quốc gia độc lập (Hải Vân Quan, Cung An Định, Trường Quốc Học, Hệ thống di tích Bác Hồ).
- **RAG Cleanliness & Tính bền vững:** Mở đầu trực tiếp bằng `# <Tên thực thể>`, không YAML frontmatter, không section `## Nguồn dữ liệu`, không thuật ngữ nội bộ RAG, không chứa thông tin biến động về vé/giờ mở cửa.
- **Fact-checking lịch sử & bảo tồn:** Xác thực các mốc đại trùng tu hoàn thành năm 2024 (Điện Kiến Trung, Điện Thái Hòa, Hải Vân Quan).

---

## 2. Findings

### Bảng tổng hợp trạng thái 11 thực thể:
| Thực thể | Template RAG Clean | Bền vững (No tickets) | Địa giới HC 2026 | Ranh giới Inventory | Fact-check Lịch sử | Cấp ghi danh / Xếp hạng | Trạng thái kỹ thuật |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **18. Kinh thành Huế** | PASS | PASS | PASS (Phú Xuân) | PASS | PASS | PASS (UNESCO 678-001) | **PASS** |
| **19. Đại Nội Huế** | PASS | PASS | PASS (Phú Xuân) | PASS | PASS (Kiến Trung, Thái Hòa 2024) | PASS (UNESCO 1993) | **PASS** |
| **20. Chùa Thiên Mụ** | PASS | PASS | PASS (Kim Long) | PASS | PASS (Bảo vật QG 2013, 2020) | PASS (UNESCO 678-002) | **PASS** |
| **21. Đàn Nam Giao** | PASS | PASS | PASS (Thuận Hóa) | PASS | PASS | **MAJOR** *(Nhầm mã UNESCO)* | **CHANGES REQUESTED** |
| **22. Hổ Quyền** | PASS | PASS | PASS (Thủy Xuân) | PASS (Điện Voi Ré) | PASS | **MINOR** *(Bổ sung số QĐ 1998)* | **PASS (Có Minor)** |
| **23. Điện Hòn Chén** | PASS | PASS | PASS (Kim Long) | PASS | PASS | **BLOCKER** *(Thiếu UNESCO 1993)* | **CHANGES REQUESTED** |
| **24. Cung An Định** | PASS | PASS | PASS (Thuận Hóa) | PASS | PASS | **BLOCKER + MAJOR** *(Gán sai UNESCO)* | **CHANGES REQUESTED** |
| **25. Đàn Xã Tắc** | PASS | PASS | PASS (Phú Xuân) | PASS | PASS | **MINOR** *(Tinh chỉnh câu chữ UNESCO)* | **PASS (Có Minor)** |
| **26. Hải Vân Quan** | PASS | PASS | PASS (Phú Lộc - Đà Nẵng) | PASS | PASS (Trùng tu 2024, Dụ Đỉnh) | PASS (QĐ 1531/QĐ-BVHTTDL) | **PASS (XUẤT SẮC)** |
| **27. Trường Quốc Học Huế** | PASS | PASS | PASS (Thuận Hóa) | PASS | PASS (QĐ 2280/QĐ-TTg 2020) | PASS (QG đặc biệt, no UNESCO) | **PASS** |
| **28. Hệ thống DT Bác Hồ** | PASS | PASS | PASS (Dương Nỗ, Phú Xuân...) | PASS (4 điểm lõi) | PASS | **MAJOR** *(Sai số QĐ 1990, 1995)* | **CHANGES REQUESTED** |

---

### Chi tiết các Findings cần khắc phục:

#### FINDING-01: Gán sai danh hiệu Di sản Thế giới UNESCO 1993 cho Cung An Định
- **Mức độ:** `BLOCKER`
- **Vị trí:** `knowledge-base-hue/heritage/24 Cung An Định.md`, Dòng 86.
- **Yêu cầu & Quy chuẩn:** Theo `heritage-template.md` (mục 2.2: Không dùng chung nhãn Di sản thế giới cho mọi trường hợp) và `heritage-research-evidence.md` (dòng 23, dòng 644), Cung An Định là di tích biệt cung thời Nguyễn do TTBT Di tích Cố đô Huế quản lý, **không nằm trong 14 cụm di tích thành phần nguyên bản được UNESCO ghi danh năm 1993 (Serial ID 678-001 đến 678-014)**.
- **Nội dung vi phạm:** Dòng 86 ghi: *"Cung An Định là một bộ phận cấu thành trọng yếu của Quần thể Di tích Cố đô Huế được UNESCO ghi danh là Di sản Văn hóa Thế giới năm 1993."*
- **Tác động:** Sai lệch nghiêm trọng về tình trạng pháp lý quốc tế của di tích, khiến RAG sinh hallucination rằng Cung An Định đã là Di sản Thế giới từ năm 1993.
- **Tiêu chí đóng:** Sửa lại dòng 86 khẳng định rõ Cung An Định là di tích thời Nguyễn trực thuộc hệ thống quản lý của Trung tâm Bảo tồn Di tích Cố đô Huế; di tích không thuộc danh mục 14 cụm thành phần gốc được UNESCO ghi danh năm 1993 mà là di tích liên quan trọng yếu thuộc diện nghiên cứu đề xuất mở rộng trong tương lai.

#### FINDING-02: Bỏ sót danh hiệu Di sản Thế giới UNESCO năm 1993 tại Điện Hòn Chén
- **Mức độ:** `BLOCKER`
- **Vị trí:** `knowledge-base-hue/heritage/23 Điện Hòn Chén.md`, Dòng 10, 11, 101 và `heritage-research-evidence.md`, Mục 23.
- **Yêu cầu & Quy chuẩn:** Danh mục chính thức của Trung tâm Di sản Thế giới UNESCO (Site 678 - Complex of Hué Monuments).
- **Nội dung vi phạm:** File ghi nhận Điện Hòn Chén chỉ là "di tích liên quan thuộc hệ thống quản lý của Trung tâm Bảo tồn Di tích Cố đô Huế", bỏ sót hoàn toàn danh hiệu Di sản Văn hóa Thế giới UNESCO năm 1993 trong mục Ghi danh / Xếp hạng.
- **Chứng cứ độc lập:** Điện Hòn Chén (Temple Hon Chen) là **một trong 14 cụm di tích thành phần chính thức** cấu thành Quần thể Di tích Cố đô Huế được UNESCO ghi danh Di sản Văn hóa Thế giới ngày 11/12/1993 với mã định danh thành phần quốc tế là **678-009**.
- **Tác động:** Hạ thấp cấp bậc di sản quốc tế được UNESCO công nhận, mâu thuẫn với hồ sơ di sản chính thức của UNESCO.
- **Tiêu chí đóng:**
  + Dòng 10 sửa thành: `- **Thuộc quần thể:** Quần thể Di tích Cố đô Huế (Di sản Văn hóa Thế giới UNESCO)`.
  + Dòng 11 bổ sung: `- **Ghi danh / Xếp hạng:** Di sản Văn hóa Thế giới UNESCO (năm 1993, mã định danh thành phần 678-009); Di tích lịch sử - văn hóa cấp quốc gia (Quyết định số 2014-VH/QĐ ngày 16/12/1993 của Bộ Văn hóa - Thông tin); Di tích quốc gia đặc biệt (Quyết định số 1272/QĐ-TTg ngày 12/08/2009 của Thủ tướng Chính phủ)`.
  + Dòng 101 khẳng định rõ Điện Hòn Chén là cụm thành phần chính thức thứ 9 (mã 678-009) được UNESCO ghi danh.
  + Bổ sung mã 678-009 vào mục 23 của file `heritage-research-evidence.md`.

#### FINDING-03: Ghi sai mã định danh thành phần UNESCO tại Đàn Nam Giao
- **Mức độ:** `MAJOR`
- **Vị trí:** `knowledge-base-hue/heritage/21 Đàn Nam Giao.md`, Dòng 11, 20, 149 và `heritage-research-evidence.md`, Dòng 549, 555.
- **Nội dung vi phạm:** File ghi mã thành phần UNESCO của Đàn Nam Giao là `678-005`.
- **Chứng cứ độc lập:** Theo danh mục WHC Inscription Components của UNESCO cho Quần thể Cố đô Huế (Site 678), mã `678-005` là Lăng Dục Đức (*Tombeau de Duc Duc*). Mã thành phần chính thức của Đàn Nam Giao là **`678-006`** (*Esplanade Nam Giao*).
- **Tác động:** Sai lệch mã định danh di sản chuẩn hóa quốc tế, gây xung đột đối chiếu chéo giữa Lăng Dục Đức và Đàn Nam Giao trong cơ sở tri thức RAG.
- **Tiêu chí đóng:** Thay thế mã `678-005` thành mã chính xác **`678-006`** tại tất cả các vị trí trong file `21 Đàn Nam Giao.md` và `heritage-research-evidence.md`.

#### FINDING-04: Thiếu căn cứ pháp lý xếp hạng Di tích quốc gia độc lập của Cung An Định
- **Mức độ:** `MAJOR`
- **Vị trí:** `knowledge-base-hue/heritage/24 Cung An Định.md`, Dòng 11.
- **Nội dung vi phạm:** File ghi: *"- Ghi danh / Xếp hạng: Di tích quốc gia đặc biệt (thuộc Quần thể Di tích Cố đô Huế, Quyết định số 1272/QĐ-TTg ngày 12/08/2009 của Thủ tướng Chính phủ)"* mà bỏ qua quyết định xếp hạng di tích quốc gia độc lập.
- **Chứng cứ độc lập:** Cung An Định được Bộ Văn hóa và Thông tin xếp hạng Di tích kiến trúc nghệ thuật cấp quốc gia theo **Quyết định số 100/2006/QĐ-BVHTT ngày 13/12/2006**.
- **Tác động:** Thiếu căn cứ pháp lý di sản quan trọng nhất chứng nhận tính độc lập của di tích trước khi được kết nối bảo tồn chung.
- **Tiêu chí đóng:** Cập nhật dòng 11 nêu rõ: Di tích kiến trúc nghệ thuật cấp quốc gia theo Quyết định số 100/2006/QĐ-BVHTT ngày 13/12/2006 của Bộ Văn hóa và Thông tin; di tích liên quan thuộc hệ thống quản lý của Trung tâm Bảo tồn Di tích Cố đô Huế.

#### FINDING-05: Sai số hiệu Quyết định 1990 và gộp sai Quyết định xếp hạng Đình làng Dương Nỗ
- **Mức độ:** `MAJOR`
- **Vị trí:** `knowledge-base-hue/heritage/28 Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md`, Dòng 18 và `heritage-research-evidence.md`, Dòng 805.
- **Nội dung vi phạm:** File ghi: *"Quyết định số 29-VH/QĐ ngày 26/03/1990 (Nhà lưu niệm thời niên thiếu của Bác Hồ tại làng Dương Nỗ và Đình làng Dương Nỗ)"*.
- **Chứng cứ độc lập:**
  1. Số hiệu Quyết định xếp hạng di tích quốc gia cho Nhà lưu niệm thời niên thiếu của Bác Hồ tại làng Dương Nỗ ngày 26/03/1990 chính xác là **Quyết định số 296/VH-QĐ** (thiếu số 6).
  2. Đình làng Dương Nỗ **không được xếp hạng chung trong quyết định ngày 26/03/1990**. Đình làng Dương Nỗ được Bộ Văn hóa - Thông tin xếp hạng Di tích kiến trúc nghệ thuật cấp quốc gia riêng biệt theo **Quyết định số 3777/QĐ-BT ngày 23/12/1995**.
- **Tác động:** Trích dẫn sai văn bản quy phạm pháp luật di sản, làm sai lệch hồ sơ khoa học của di tích lịch sử - kiến trúc.
- **Tiêu chí đóng:** Sửa lại dòng 18 tách biệt rõ ràng: Quyết định số 296/VH-QĐ ngày 26/03/1990 cho Nhà lưu niệm làng Dương Nỗ; và Quyết định số 3777/QĐ-BT ngày 23/12/1995 cho Đình làng Dương Nỗ. Đồng bộ cập nhật sang dòng 805 của `heritage-research-evidence.md`.

#### Các kiến nghị hoàn thiện (MINOR FINDINGS):
- **MINOR-01 (Hổ Quyền):** Dòng 11 và 109 bổ sung số hiệu quyết định xếp hạng di tích quốc gia: `Quyết định số 2009/1998/QĐ-BVHTT ngày 26/09/1998 của Bộ Văn hóa - Thông tin`. Tại dòng 49, làm rõ thêm hướng khán đài vua ngự: tọa lạc phía Đông Nam, quay mặt về hướng Nam theo quy cách *"Thánh nhân Nam diện"*.
- **MINOR-02 (Đàn Xã Tắc):** Dòng 11 tinh chỉnh câu chữ để tránh gây hiểu nhầm Đàn Xã Tắc là di tích thành phần nguyên bản năm 1993: *"nằm trong khu vực bảo vệ của Kinh thành Huế thuộc Quần thể Di tích Cố đô Huế (Di tích quốc gia đặc biệt năm 2009)"*.
- **MINOR-03 (Điện Hòn Chén):** Bổ sung section `## Thông tin dành cho du khách` ngắn gọn, bền vững về tuyến tiếp cận đường thủy trên sông Hương và lưu ý trang phục văn hóa tâm linh.
- **MINOR-04 (Trường Quốc Học & Hệ thống Bác Hồ):** Thống nhất cách diễn đạt niên khóa nhập học của Bác tại Quốc Học giữa hai file (niên khóa 1908–1909 tại lớp Đệ nhị niên, giải thích sự kiện tham gia phong trào chống thuế tháng 4/1908 trong giai đoạn chuyển tiếp học tập).

---

## 3. Cách Reviewer chạy lại thật

Reviewer đã kích hoạt và điều phối 4 sub-agent nghiên cứu độc lập để thực thi việc kiểm chứng chéo và tra cứu dữ liệu thời gian thực:
1. **Subagent 1 (`c3a3e24c`):** Rà soát chuyên sâu `18 Kinh thành Huế.md`, `19 Đại Nội Huế.md`, `20 Chùa Thiên Mụ.md`.
   - Web queries: `Kinh thành Huế chu vi cửa thành 1805 1832`, `Điện Kiến Trung hoàn thành trùng tu 2024`, `Điện Thái Hòa trùng tu 2024 hoàn thành`, `Chùa Thiên Mụ bia ngự kiến bảo vật quốc gia quyết định 88 2020`.
2. **Subagent 2 (`1429bddb`):** Rà soát chuyên sâu `21 Đàn Nam Giao.md`, `22 Hổ Quyền.md`, `23 Điện Hòn Chén.md`.
   - Web queries: `UNESCO WHC 678 components list`, `Điện Hòn Chén UNESCO 678`, `Hổ Quyền quyết định xếp hạng 1998 Bộ Văn hóa`, `Đàn Nam Giao component id UNESCO`.
3. **Subagent 3 (`bb37eb73`):** Rà soát chuyên sâu `24 Cung An Định.md`, `25 Đàn Xã Tắc.md`, `26 Hải Vân Quan.md`.
   - Web queries: `Cung An Định di tích quốc gia quyết định 100 2006`, `Cung An Định UNESCO 1993 component`, `Hải Vân Quan quyết định 1531 2017 khánh thành 2024`, `Đàn Xã Tắc quyết định 99 2006 khảo cổ`.
4. **Subagent 4 (`544f5554`):** Rà soát chuyên sâu `27 Trường Quốc Học Huế.md`, `28 Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md`.
   - Web queries: `Trường Quốc Học Huế di tích quốc gia đặc biệt quyết định 2280 2020`, `Di tích Bác Hồ Thừa Thiên Huế quyết định 2280 2020`, `Đình làng Dương Nỗ quyết định xếp hạng di tích 1995 3777`.

Thao tác kiểm tra tính toàn vẹn hệ thống:
- Kiểm tra trạng thái Git bằng `git status`.
- Kiểm tra diff ranh giới bằng `git diff --check`.
- Đối chiếu văn bản hành chính: Nghị quyết số 175/2024/QH15 và Nghị quyết số 1675/NQ-UBTVQH15.

---

## 4. Kết quả quan sát

1. **Địa giới hành chính năm 2026:** Toàn bộ 11/11 tập tin đã cập nhật chuẩn xác đơn vị hành chính mới theo Nghị quyết 1675/NQ-UBTVQH15:
   - Kinh thành Huế, Đại Nội Huế, Đàn Xã Tắc, 112 Mai Thúc Loan: **phường Phú Xuân, TP Huế**.
   - Chùa Thiên Mụ, Điện Hòn Chén: **phường Kim Long, TP Huế**.
   - Đàn Nam Giao, Cung An Định, Trường Quốc Học Huế: **phường Thuận Hóa, TP Huế**.
   - Hổ Quyền: **phường Thủy Xuân, TP Huế**.
   - Cụm di tích làng Dương Nỗ: **phường Dương Nỗ, TP Huế**.
   - Hải Vân Quan: Ranh giới **thị trấn Lăng Cô, huyện Phú Lộc, TP Huế** và **phường Hòa Hiệp Bắc, quận Liên Chiểu, TP Đà Nẵng**.
2. **Tuân thủ quy chuẩn RAG Clean:** Cả 11 file đều bắt đầu bằng `# <Tên thực thể>`, không YAML frontmatter, không section nguồn dữ liệu, không rò rỉ thuật ngữ kỹ thuật RAG.
3. **Tính bền vững thông tin:** Không có file nào đưa thông tin nhất thời về giá vé, giờ mở cửa du lịch.
4. **Hiện trạng bảo tồn năm 2024–2026:** Các công trình tiêu biểu như Điện Kiến Trung (mở cửa Tết Giáp Thìn 2024), Điện Thái Hòa (hoàn thành trùng tu cuối năm 2024), Hải Vân Quan (mở cửa 01/08/2024) đều được cập nhật mốc lịch sử chính xác.

---

## 5. Giới hạn hoặc phần chưa chạy

Không có giới hạn review đã biết trong phạm vi này. Toàn bộ 11 tập tin và các bằng chứng lịch sử, pháp lý, hành chính liên quan đều đã được kiểm tra chéo và đối chiếu thực tế đầy đủ.

---

## 6. Decision và bước tiếp theo

**Decision:** `changes_requested`

### Hướng dẫn sửa chữa cụ thể dành cho Implementer:

1. **`24 Cung An Định.md`:**
   - **Khắc phục FINDING-01 (Blocker):** Sửa dòng 86 thành: *"Cung An Định là di tích biệt cung hoàng gia thời Nguyễn trực thuộc hệ thống quản lý của Trung tâm Bảo tồn Di tích Cố đô Huế. Di tích không nằm trong danh mục 14 cụm thành phần gốc được UNESCO ghi danh Di sản Thế giới năm 1993, nhưng là một trong các di tích liên quan trọng yếu thuộc diện nghiên cứu đề xuất xem xét mở rộng ranh giới di sản trong tương lai."*
   - **Khắc phục FINDING-04 (Major):** Sửa dòng 11 thành: *"- **Ghi danh / Xếp hạng:** Di tích kiến trúc nghệ thuật cấp quốc gia (theo Quyết định số 100/2006/QĐ-BVHTT ngày 13/12/2006 của Bộ Văn hóa và Thông tin); di tích liên quan thuộc hệ thống quản lý của Trung tâm Bảo tồn Di tích Cố đô Huế."*
2. **`23 Điện Hòn Chén.md`:**
   - **Khắc phục FINDING-02 (Blocker):** 
     + Sửa dòng 10: `- **Thuộc quần thể:** Quần thể Di tích Cố đô Huế (Di sản Văn hóa Thế giới UNESCO)`.
     + Sửa dòng 11: `- **Ghi danh / Xếp hạng:** Di sản Văn hóa Thế giới UNESCO (năm 1993, mã định danh thành phần 678-009); Di tích lịch sử - văn hóa cấp quốc gia (Quyết định số 2014-VH/QĐ ngày 16/12/1993 của Bộ Văn hóa - Thông tin); Di tích quốc gia đặc biệt (Quyết định số 1272/QĐ-TTg ngày 12/08/2009 của Thủ tướng Chính phủ)`.
     + Sửa dòng 101: Khẳng định rõ Điện Hòn Chén là cụm thành phần chính thức thứ 9 (mã 678-009) thuộc Quần thể Di tích Cố đô Huế được UNESCO ghi danh.
     + Đồng bộ cập nhật mục 23 trong `heritage-research-evidence.md`.
     + Bổ sung section `## Thông tin dành cho du khách` (Minor-03).
3. **`21 Đàn Nam Giao.md`:**
   - **Khắc phục FINDING-03 (Major):** Sửa mã `678-005` thành mã chính xác **`678-006`** tại Dòng 11, 20, 149 và đồng bộ sang Dòng 549, 555 của `heritage-research-evidence.md`.
4. **`28 Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md`:**
   - **Khắc phục FINDING-05 (Major):** Sửa dòng 18 thành:
     *"- **Di tích lịch sử - văn hóa cấp quốc gia:** Quyết định số 296/VH-QĐ ngày 26/03/1990 (Nhà lưu niệm thời niên thiếu của Chủ tịch Hồ Chí Minh tại làng Dương Nỗ); Quyết định số 298/VH-QĐ ngày 26/03/1990 (Địa điểm Trường Quốc Học Huế); Quyết định số 74-VH/QĐ ngày 02/02/1993 (Nhà lưu niệm Chủ tịch Hồ Chí Minh tại số 112 Mai Thúc Loan); Quyết định số 3777/QĐ-BT ngày 23/12/1995 (Di tích kiến trúc nghệ thuật Đình làng Dương Nỗ) của Bộ Văn hóa - Thông tin."*
     Đồng bộ cập nhật sang dòng 805 của `heritage-research-evidence.md`.
5. **`22 Hổ Quyền.md`:**
   - Bổ sung số quyết định di tích quốc gia năm 1998: `Quyết định số 2009/1998/QĐ-BVHTT ngày 26/09/1998 của Bộ Văn hóa - Thông tin` tại dòng 11 và 109 (Minor-01).
6. **`25 Đàn Xã Tắc.md`:**
   - Tinh chỉnh câu chữ ghi danh tại dòng 11 theo Minor-02.

Sau khi Implementer hoàn tất việc hiệu chỉnh, Reviewer sẽ tiến hành re-review độc lập trước khi trình Người dùng nghiệm thu chính thức.
