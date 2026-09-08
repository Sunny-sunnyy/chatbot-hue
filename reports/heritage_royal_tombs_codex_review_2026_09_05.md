# Codex Review: Heritage Domain - Royal Tombs (Entities 10–17)

Decision: changes_requested  
Reviewer: Reviewer  
Date: 2026-09-05  
Canonical guide: `knowledge-base-hue/meta/heritage-template.md`, `knowledge-base-hue/heritage/heritage-entities-inventory.md`  
Implementation report: `knowledge-base-hue/meta/heritage-research-evidence.md` (Mục 10–17)  

## 1. Phạm vi đã review

Reviewer cùng 4 sub-agent độc lập đã rà soát toàn diện, đối chiếu chéo và fact-check bằng công cụ tìm kiếm web (web search) mốc thời gian quy chiếu tháng 09/2026 trên 8 tập tin lăng tẩm hoàng gia triều Nguyễn:
- `knowledge-base-hue/heritage/10 Lăng Gia Long.md`
- `knowledge-base-hue/heritage/11 Lăng Minh Mạng.md`
- `knowledge-base-hue/heritage/12 Lăng Thiệu Trị.md`
- `knowledge-base-hue/heritage/13 Lăng Tự Đức.md`
- `knowledge-base-hue/heritage/14 Lăng Dục Đức.md`
- `knowledge-base-hue/heritage/15 Lăng Đồng Khánh.md`
- `knowledge-base-hue/heritage/16 Lăng Khải Định.md`
- `knowledge-base-hue/heritage/17 Lăng vua Hiệp Hòa.md`

Đối chiếu với các tài liệu quy chuẩn và minh chứng:
- `knowledge-base-hue/heritage/heritage-entities-inventory.md`
- `knowledge-base-hue/meta/heritage-template.md`
- `knowledge-base-hue/meta/heritage-research-evidence.md` (Mục 10 đến 17)

## 2. Findings

### 2.1. Tổng quan phân loại

- **Blocker:** 02 phát hiện (tại `10 Lăng Gia Long.md`: sai thân phụ/thân mẫu vua Gia Long, gán sai lăng Trường Phong).
- **Major:** 07 phát hiện (tại `10 Lăng Gia Long.md`: 03; `11 Lăng Minh Mạng.md`: 02; `15 Lăng Đồng Khánh.md`: 03; `16 Lăng Khải Định.md`: 02).
- **Minor:** 06 phát hiện (câu từ ước lượng chủ quan, mỹ từ, tách rời domain tickets).

---

### 2.2. Chi tiết các Findings Blocker & Major (Bắt buộc sửa)

#### [GL-BLK-01] Sai thân phụ vua Gia Long và gán sai chủ nhân Lăng Trường Phong
- **Vị trí:** `10 Lăng Gia Long.md` (dòng 62)
- **Hiện trạng:** `lăng Trường Phong (Tuyên Vương Nguyễn Phúc Hạo, thân phụ vua Gia Long)`
- **Requirement:** `heritage-template.md` mục 2.1, 4.1 (Chính xác tuyệt đối về nhân vật lịch sử và người được an táng).
- **Evidence & Sử liệu:** 
  - Thân phụ vua Gia Long là **Hưng Tổ Hiếu Khang Hoàng đế Nguyễn Phúc Luân** (1733–1765, còn gọi là Nguyễn Phúc Côn), an táng tại **Lăng Cơ Thánh** (làng Cư Chánh).
  - Tuyên Vương Nguyễn Phúc Hạo (1739–1760) là con trưởng chúa Vũ Nguyễn Phúc Khoát, tức là **bác ruột** của vua Gia Long.
  - **Lăng Trường Phong** là nơi an nghỉ của **chúa Ninh Vương Nguyễn Phúc Chú** (vị chúa Nguyễn thứ 7, trị vì 1725–1738).
- **Tác động:** Làm sai lệch hệ thống phả hệ hoàng tộc triều Nguyễn, khiến mô hình RAG trả lời sai nghiêm trọng về thân phụ vua Gia Long.
- **Tiêu chí đóng:** Đính chính rõ: lăng Trường Phong là lăng của chúa Ninh Vương Nguyễn Phúc Chú; thân phụ vua Gia Long là Nguyễn Phúc Luân (lăng Cơ Thánh).

#### [GL-BLK-02] Sai tên thân mẫu vua Gia Long tại Lăng Thoại Thánh
- **Vị trí:** `10 Lăng Gia Long.md` (dòng 60)
- **Hiện trạng:** `Lăng Thoại Thánh: Nơi an táng Hiếu Khang Hoàng hậu (bà Nguyễn Thị Mai, thân mẫu của vua Gia Long)`
- **Requirement:** `heritage-template.md` mục 2.1, 4.1.
- **Evidence & Sử liệu:** Thân mẫu vua Gia Long là Hiếu Khang Hoàng hậu tên thật là **Nguyễn Thị Hoàn** (阮氏環, 1736–1811). Nhân vật "Nguyễn Thị Mai" là Triệu Tổ Tĩnh Hoàng hậu (vợ chúa Nguyễn Kim, sống trước đó gần 300 năm).
- **Tác động:** Sai lệch danh tính vị Hoàng thái hậu đầu tiên của triều Nguyễn.
- **Tiêu chí đóng:** Đổi "Nguyễn Thị Mai" thành "Nguyễn Thị Hoàn".

#### [GL-MAJ-01] Nhầm lẫn chủ nhân Lăng Quang Hưng và Lăng Vĩnh Mậu
- **Vị trí:** `10 Lăng Gia Long.md` (dòng 62)
- **Hiện trạng:** `lăng Quang Hưng (chúa Hiền Nguyễn Phúc Tần), lăng Vĩnh Mậu (chúa Nghĩa Nguyễn Phúc Thái)`
- **Requirement:** `heritage-template.md` mục 4.1.
- **Evidence & Sử liệu:** 
  - Lăng Quang Hưng là lăng của bà **Tống Thị Đôi** (Thái Tông Hiếu Triết Hoàng hậu, vợ thứ hai chúa Hiền; lăng chúa Hiền là Lăng Trường Hưng).
  - Lăng Vĩnh Mậu là lăng của bà **Tống Thị Lãnh** (Anh Tông Hiếu Nghĩa Hoàng hậu, vợ chúa Nghĩa; lăng chúa Nghĩa là Lăng Trường Mậu).
- **Tác động:** Gán nhầm lăng mộ của các vị hoàng hậu thành lăng mộ của các chúa Nguyễn.
- **Tiêu chí đóng:** Đính chính đúng chủ nhân của Lăng Quang Hưng và Lăng Vĩnh Mậu.

#### [GL-MAJ-02] Sai tên ngọn đồi trung tâm đặt Bửu thành
- **Vị trí:** `10 Lăng Gia Long.md` (dòng 33)
- **Hiện trạng:** `Khu lăng mộ trung tâm (Bửu thành): Tọa lạc trên đồi Cẩm Thi Sơn...`
- **Requirement:** `heritage-template.md` mục 4.1.
- **Evidence & Khảo sát:** Ba ngọn đồi trung tâm Lăng Gia Long gồm: đồi chính giữa là **Chánh Trung Sơn** (hay Chính Trung Sơn 正中山) đặt Bửu thành; đồi bên trái là **Thanh Sơn** đặt Bi đình; đồi bên phải là **Bạch Sơn** đặt Điện Minh Thành. Không tồn tại địa danh "Cẩm Thi Sơn".
- **Tiêu chí đóng:** Sửa "Cẩm Thi Sơn" thành "Chánh Trung Sơn".

#### [GL-MAJ-03] Đảo ngược phương vị nhìn hai ngôi mộ đá song táng
- **Vị trí:** `10 Lăng Gia Long.md` (dòng 34)
- **Hiện trạng:** `Mộ vua Gia Long đặt bên trái (nhìn từ ngoài vào, ứng với vị trí Càn), mộ Thừa Thiên Cao Hoàng hậu đặt bên phải (ứng với vị trí Khôn).`
- **Requirement:** `heritage-template.md` mục 2.1, 4.1.
- **Evidence & Thực tế:** Nguyên tắc phong thủy "nam tả nữ hữu" tính từ trong lăng nhìn ra. Khi đứng ở bái đình **nhìn từ ngoài vào trong**: Mộ vua Gia Long nằm ở bên **phải**, mộ Thừa Thiên Cao Hoàng hậu nằm ở bên **trái**.
- **Tiêu chí đóng:** Sửa lại đúng phương vị quan sát thực tế từ ngoài nhìn vào.

#### [MM-MAJ-01] Nhầm lẫn nơi an táng của Tá Thiên Nhân Hoàng hậu Hồ Thị Hoa
- **Vị trí:** `11 Lăng Minh Mạng.md` (dòng 14)
- **Hiện trạng:** Gộp chung dưới mục `- **Nhân vật phụng thờ và an táng:** Thánh Tổ Chương Hoàng đế Minh Mạng (...) và Tá Thiên Nhân Hoàng hậu (Hồ Thị Hoa...)`
- **Requirement:** `heritage-template.md` mục 4.1.
- **Evidence & Sử liệu:** Bà Tá Thiên Nhân Hoàng hậu Hồ Thị Hoa chỉ được **phụng thờ** bài vị tại Điện Sùng Ân thuộc Hiếu Lăng. Bà **không an táng tại đây**. Nơi an táng của bà là **Hiếu Đông Lăng** (tại làng Cư Chánh). Bửu thành chỉ an táng duy nhất vua Minh Mạng.
- **Tác động:** Gây hiểu lầm Hiếu Lăng là mộ song táng.
- **Tiêu chí đóng:** Tách rõ: *Nhân vật an táng: Hoàng đế Minh Mạng*; *Nhân vật phụng thờ: Hoàng đế Minh Mạng và Tá Thiên Nhân Hoàng hậu*.

#### [MM-MAJ-02] Sai loại ngói kiến trúc tại Đại Hồng Môn
- **Vị trí:** `11 Lăng Minh Mạng.md` (dòng 34)
- **Hiện trạng:** `lợp ngói lưu ly đỏ`
- **Requirement:** `heritage-template.md` mục 2.1, 4.1.
- **Evidence & Khảo sát:** Đại Hồng Môn lợp bằng **ngói hoàng lưu ly** (men vàng hoàng gia, 24 mái). Kiến trúc cung đình Huế chỉ dùng ngói hoàng lưu ly và thanh lưu ly, không có "ngói lưu ly đỏ".
- **Tiêu chí đóng:** Sửa "ngói lưu ly đỏ" thành "ngói hoàng lưu ly".

#### [ĐK-MAJ-01] Sai số hiệu Quyết định Di tích quốc gia đặc biệt
- **Vị trí:** `15 Lăng Đồng Khánh.md` (dòng 13)
- **Hiện trạng:** `theo Quyết định số 548/QĐ-TTg ngày 10/05/2012 của Thủ tướng Chính phủ`
- **Requirement:** `heritage-template.md` mục 2.2.
- **Evidence:** Quần thể Di tích Cố đô Huế được xếp hạng Di tích quốc gia đặc biệt đợt đầu tại **Quyết định số 1272/QĐ-TTg ngày 12/8/2009**. Quyết định số 548/QĐ-TTg là đợt 3 xếp hạng cho 13 di tích khác (Pác Bó, Tân Trào, Tràng An...).
- **Tiêu chí đóng:** Sửa thành: `theo Quyết định số 1272/QĐ-TTg ngày 12/8/2009 của Thủ tướng Chính phủ`.

#### [ĐK-MAJ-02] Sai mã định danh thành phần UNESCO World Heritage
- **Vị trí:** `15 Lăng Đồng Khánh.md` (dòng 12)
- **Hiện trạng:** `(mã định danh thành phần 678-006)`
- **Requirement:** `heritage-template.md` mục 2.2.
- **Evidence:** Theo danh mục chính thức UNESCO Serial ID 678: **678-006** là **Đàn Nam Giao**. Mã chuẩn của **Lăng Đồng Khánh** là **`678-008`**.
- **Tiêu chí đóng:** Đổi mã thành **`678-008`** (hoặc chỉ ghi nhận thuộc Quần thể Di tích Cố đô Huế tiêu chí iv).

#### [ĐK-MAJ-03] Xếp sai vua Khải Định và Kiên Thái Vương vào mục "Nhân vật phụng thờ và an táng"
- **Vị trí:** `15 Lăng Đồng Khánh.md` (dòng 14–17)
- **Hiện trạng:** Đặt vua Khải Định và Kiên Thái Vương dưới mục `- **Nhân vật phụng thờ và an táng:**`
- **Requirement:** `heritage-template.md` mục 2.1, 2.3, 4.1.
- **Evidence:** 
  - Vua Khải Định an táng tại Lăng Khải Định, không an táng và không thờ tự tại Lăng Đồng Khánh.
  - Kiên Thái Vương chỉ thờ ở Điện Truy Tư giai đoạn 1888–1889, sau đó bài vị rước về Phủ Kiên Thái Vương. Lăng mộ Kiên Thái Vương kề bên ngoài khuôn viên Tư Lăng.
  - Nhân vật phụng thờ chính tại Điện Ngưng Hy là vua Đồng Khánh cùng 2 hoàng hậu (Thánh Cung, Tiên Cung).
- **Tiêu chí đóng:** Tách mục: *Hoàng đế an táng và phụng thờ: Hoàng đế Đồng Khánh (phối thờ Thánh Cung, Tiên Cung)*; *Nhân vật lịch sử liên quan: Kiên Thái Vương (thân phụ), Hoàng đế Khải Định (con trưởng, chủ trì đại kiến thiết 1916–1923)*.

#### [KĐ-MAJ-01] Sai số hiệu Quyết định Di tích quốc gia đặc biệt
- **Vị trí:** `16 Lăng Khải Định.md` (dòng 13)
- **Hiện trạng:** `theo Quyết định số 548/QĐ-TTg ngày 10/05/2012 của Thủ tướng Chính phủ`
- **Requirement:** `heritage-template.md` mục 2.2.
- **Evidence:** Lỗi tương tự Lăng Đồng Khánh, phải là **Quyết định số 1272/QĐ-TTg ngày 12/8/2009**.
- **Tiêu chí đóng:** Sửa thành Quyết định số 1272/QĐ-TTg ngày 12/8/2009.

#### [KĐ-MAJ-02] Sai mã định danh thành phần UNESCO World Heritage
- **Vị trí:** `16 Lăng Khải Định.md` (dòng 12)
- **Hiện trạng:** `(mã định danh thành phần 678-007)`
- **Requirement:** `heritage-template.md` mục 2.2.
- **Evidence:** Mã **678-007** là **Lăng Tự Đức**. Mã thành phần chuẩn của **Lăng Khải Định** là **`678-011`**.
- **Tiêu chí đóng:** Đổi mã thành **`678-011`**.

---

### 2.3. Chi tiết các Findings Minor (Khuyến nghị hoàn thiện)

1. `10 Lăng Gia Long.md` (dòng 26): Chỉnh ngày mất của vua Gia Long 03/02/1820 thành âm lịch ngày 19 tháng Chạp năm Kỷ Mão.
2. `11 Lăng Minh Mạng.md` (dòng 91): Lược bỏ thời lượng tham quan ước tính 1,5 - 2 giờ để bảo đảm tính khách quan theo mục 5 template.
3. `14 Lăng Dục Đức.md` (dòng 24): Giảm nhẹ cụm từ *"Điểm độc nhất vô nhị"* thành *"Điểm đặc biệt nổi bật"*.
4. `14 Lăng Dục Đức.md` (dòng 79): Lược bỏ chữ "bán vé" (*"mở cửa bán vé đón khách tham quan"*) -> chuyển thành *"mở cửa đón khách tham quan"*.
5. `14 Lăng Dục Đức.md` (dòng 84): Lược bỏ câu thời lượng tham quan khuyến nghị.
6. `15 Lăng Đồng Khánh.md` (dòng 8): Chú thích tên đường *"Đoàn Nhữ Hải (tức danh nhân Đoàn Nhữ Hài)"*.
7. `16 Lăng Khải Định.md` (dòng 67, 74): Tiết chế các từ ca ngợi cảm tính: *"đỉnh cao tuyệt mỹ"*, *"như một thế giới thần tiên"*.
8. `17 Lăng vua Hiệp Hòa.md` (dòng 77): Chỉnh *"không thu vé tham quan"* thành *"không gian tưởng niệm tâm linh mở cửa tự do đón khách viếng thăm"*.

---

## 3. Cách Reviewer chạy lại thật

1. Kiểm tra worktree và sự hiện diện của 8 file Markdown lăng tẩm cùng file evidence.
2. Đọc trực tiếp 100% nội dung từng file và đối chiếu mục tương ứng tại `knowledge-base-hue/meta/heritage-research-evidence.md`.
3. Kiểm tra tính tuân thủ quy chuẩn Markdown RAG Clean: cú pháp tiêu đề H1, không YAML frontmatter, không có `## Nguồn dữ liệu`, không chứa thuật ngữ RAG nội bộ.
4. Tra cứu đối chiếu web search độc lập theo mốc 2026:
   - Tra cứu Nghị quyết 175/2024/QH15, Nghị quyết 1314/NQ-UBTVQH15, Nghị quyết 1675/NQ-UBTVQH15 về sáp nhập ĐVHC cấp xã của TP Huế (phường Kim Long, phường Thủy Xuân, phường An Cựu).
   - Tra cứu danh mục 14 thành phần UNESCO World Heritage mã 678 (*Complex of Hué Monuments*).
   - Tra cứu văn bản Quyết định 1272/QĐ-TTg (2009) và 548/QĐ-TTg (2012) về Di tích quốc gia đặc biệt.
   - Tra cứu phả hệ Nguyễn Phúc tộc (*Đại Nam thực lục*, *Nguyễn Phúc tộc thế phả*) về các chúa Nguyễn, thân phụ/thân mẫu vua Gia Long, lăng Trường Phong, Cơ Thánh, Thoại Thánh, Quang Hưng, Vĩnh Mậu.
   - Tra cứu nơi an táng của Tá Thiên Nhân Hoàng hậu Hồ Thị Hoa (Hiếu Đông Lăng) và ngói hoàng lưu ly Đại Hồng Môn.
   - Tra cứu quyết định xếp hạng di tích cấp tỉnh Lăng vua Hiệp Hòa (Quyết định 2743/QĐ-UBND ngày 26/11/2015 của UBND tỉnh Thừa Thiên Huế).

## 4. Kết quả quan sát

- **Địa giới hành chính năm 2026:** Cả 8 file đều xử lý cực kỳ tốt, cập nhật chuẩn xác đơn vị hành chính sau sáp nhập:
  - Lăng Gia Long, Lăng Minh Mạng: Phường Kim Long, TP Huế.
  - Lăng Thiệu Trị, Lăng Tự Đức, Lăng Đồng Khánh, Lăng Khải Định: Phường Thủy Xuân, TP Huế.
  - Lăng Dục Đức, Lăng vua Hiệp Hòa: Phường An Cựu, TP Huế.
- **Ranh giới Di sản:**
  - Lăng vua Hiệp Hòa phân định ranh giới di sản xuất sắc: khẳng định là Di tích lịch sử cấp tỉnh, không thuộc Quần thể UNESCO 1993, triệt để ngăn chặn hallucination cho LLM.
- **Trạng thái đạt chuẩn từng file:**
  - `12 Lăng Thiệu Trị.md`: **PASS** (100% chuẩn xác).
  - `13 Lăng Tự Đức.md`: **PASS** (100% chuẩn xác).
  - `14 Lăng Dục Đức.md`: **CONDITIONAL PASS** (nội dung xuất sắc, chỉ có góp ý minor).
  - `17 Lăng vua Hiệp Hòa.md`: **PASS** (rất xuất sắc, chỉ có góp ý minor).
  - `10 Lăng Gia Long.md`: **CHANGES REQUESTED** (2 Blocker, 3 Major).
  - `11 Lăng Minh Mạng.md`: **CHANGES REQUESTED** (2 Major).
  - `15 Lăng Đồng Khánh.md`: **CHANGES REQUESTED** (3 Major).
  - `16 Lăng Khải Định.md`: **CHANGES REQUESTED** (2 Major).

## 5. Giới hạn hoặc phần chưa chạy

- Đây là đợt review chuyên sâu nhóm Lăng tẩm hoàng gia (thực thể 10 đến 17). Các thực thể 1–9 (di sản UNESCO/phi vật thể) và 18–28 (di tích vật thể nổi bật) chưa được rà soát trong lượt này.
- Báo cáo này là kiểm tra dữ liệu và tài liệu độc lập (docs-only fact-check), không can thiệp hay sửa đổi trực tiếp vào nội dung các file corpus theo đúng nguyên tắc phân định vai trò Reviewer.

## 6. Decision và bước tiếp theo

**Technical verdict:** `changes_requested`

### Hướng dẫn hiệu chỉnh (Correction Guidance cho Implementer):

1. **Hiệu chỉnh `10 Lăng Gia Long.md`:**
   - Sửa dòng 60: Đổi tên thân mẫu vua Gia Long thành Hoàng thái hậu **Nguyễn Thị Hoàn**.
   - Sửa dòng 62: Ghi rõ lăng Trường Phong là lăng chúa Ninh Vương Nguyễn Phúc Chú; thân phụ vua Gia Long là Nguyễn Phúc Luân (lăng Cơ Thánh); đính chính lăng Quang Hưng (bà Tống Thị Đôi) và lăng Vĩnh Mậu (bà Tống Thị Lãnh).
   - Sửa dòng 33: Đổi "đồi Cẩm Thi Sơn" thành "đồi Chánh Trung Sơn".
   - Sửa dòng 34: Đính chính phương vị nhìn từ ngoài vào: Mộ vua Gia Long ở bên phải, mộ Thừa Thiên Cao Hoàng hậu ở bên trái.

2. **Hiệu chỉnh `11 Lăng Minh Mạng.md`:**
   - Sửa dòng 14: Tách rõ mục an táng (chỉ an táng vua Minh Mạng) và phụng thờ (phối thờ Tá Thiên Nhân Hoàng hậu Hồ Thị Hoa; làm rõ bà an táng tại Hiếu Đông Lăng).
   - Sửa dòng 34: Đổi "ngói lưu ly đỏ" thành "ngói hoàng lưu ly".

3. **Hiệu chỉnh `15 Lăng Đồng Khánh.md`:**
   - Sửa dòng 12: Đổi mã thành phần UNESCO thành `678-008`.
   - Sửa dòng 13: Đổi số hiệu Quyết định Di tích quốc gia đặc biệt thành `Quyết định số 1272/QĐ-TTg ngày 12/8/2009`.
   - Sửa dòng 14–17: Tách bạch rõ: an táng & phụng thờ vua Đồng Khánh (phối thờ 2 hoàng hậu Thánh Cung, Tiên Cung); đưa Kiên Thái Vương và vua Khải Định sang mục *Nhân vật lịch sử liên quan*.

4. **Hiệu chỉnh `16 Lăng Khải Định.md`:**
   - Sửa dòng 12: Đổi mã thành phần UNESCO thành `678-011`.
   - Sửa dòng 13: Đổi số hiệu Quyết định Di tích quốc gia đặc biệt thành `Quyết định số 1272/QĐ-TTg ngày 12/8/2009`.

5. **Đồng bộ `heritage-research-evidence.md`:**
   - Cập nhật các đính chính trên vào Mục 10, 11, 15, 16 trong file evidence để đảm bảo tính nhất quán tuyệt đối giữa dữ liệu answer-facing và bằng chứng kiểm chứng.
