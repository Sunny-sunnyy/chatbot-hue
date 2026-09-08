# Implementation Report: Tourism Coastal Batch 02 Correction (Cụm 4 Bãi biển & Vịnh biển Huế Đợt 2)

Implementer: Implementer
Date: 2026-09-06
Canonical guide: `knowledge-base-hue/meta/tourism-template.md`, `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`
Review report căn cứ: `reports/tourism_coastal_batch_02_codex_review_2026_09_06.md`

---

## 1. Phạm vi

Thực hiện gói hiệu chỉnh tập trung (Focused Correction Batch) trong một batch duy nhất nhằm khắc phục triệt để **01 phát hiện Blocker**, **11 phát hiện Major** và **14 phát hiện Minor** được Đội ngũ Reviewer Codex chỉ ra trong Báo cáo thẩm định kỹ thuật Cụm 4 Bãi biển & Vịnh biển Huế Đợt 2:
1. `knowledge-base-hue/tourism/Bãi biển Lộc Bình.md` (0 Blocker, 2 Major: M-01, M-02; 4 Minor: m-01, m-02, m-03, m-04)
2. `knowledge-base-hue/tourism/Bãi biển Bình An.md` (0 Blocker, 4 Major: M-03, M-04, M-05, M-06; 2 Minor: m-05, m-06)
3. `knowledge-base-hue/tourism/Bãi biển Cảnh Dương.md` (0 Blocker, 2 Major: M-07, M-08; 4 Minor: m-07, m-08, m-09, m-10, m-11)
4. `knowledge-base-hue/tourism/Vịnh Lăng Cô.md` (01 Blocker: B-01; 3 Major: M-09, M-10, M-11; 4 Minor: m-12, m-13, m-14)
5. Hồ sơ kiểm chứng tại `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục XVI, XVII, XVIII, XIX)

**Ranh giới bảo toàn:**
- Mốc thời gian bắt buộc: **Tháng 09/2026**.
- Địa giới hành chính hiện hành theo Nghị quyết số 175/2024/QH15, Nghị quyết số 1314/NQ-UBTVQH15 (hiệu lực 01/01/2025) và Nghị quyết số 1675/NQ-UBTVQH15 (hiệu lực 01/07/2025).
- Đạt chuẩn Markdown RAG Clean: Khởi đầu bằng H1 `#`, không YAML frontmatter, không wiki-link `[[]]`, loại bỏ triệt để chuỗi metadata AI nội bộ (`file canonical`, `tệp `, `.md`, `domain heritages`), 0 trailing whitespace, 100% tiêu đề H2 và H3 tự chứa tên thực thể (Chunk Independence).
- Chính sách quản lý mã nguồn: Tuân thủ nghiêm ngặt `git_authorization: none` (không commit/push git).

---

## 2. Chi tiết hiệu chỉnh từng tệp thực thể

### 2.1. Tệp `Bãi biển Lộc Bình.md`
1. **[MAJOR M-01] Sửa lỗi điều hướng địa lý sai lệch nghiêm trọng về cầu Tư Hiền ở Tuyến 1:**
   - Dòng 103: Hầm Phước Tượng và thôn An Hải đều cùng nằm ở bờ nam đầm Cầu Hai; sửa lại hướng dẫn chính xác: Khi đến gần chân cầu Tư Hiền (thuộc bờ nam, địa phận xã Phú Lộc), rẽ phải vào đường liên thôn ven chân đồi đi tiếp 3–5 km ra bãi biển, **không đi qua cầu Tư Hiền sang bờ bắc (xã Vinh Lộc)**.
2. **[MAJOR M-02] Khắc phục liệt kê trùng lặp địa giới hành chính ở Tuyến 2:**
   - Dòng 104: Sửa "qua các xã Phú Diên, Phú Vinh" thành "qua các xã Phú Vinh (gồm địa bàn xã Phú Diên cũ) và xã Vinh Lộc... trước khi đi qua cầu Tư Hiền vượt cửa biển để sang bờ nam".
3. **[MINOR m-01] Xóa trailing space tiêu đề H2:**
   - Dòng 92: Làm sạch hoàn toàn ký tự khoảng trắng thừa cuối dòng `## Mùa biển và điều kiện thời tiết`.
4. **[MINOR m-02] Sửa diễn đạt dễ gây hiểu nhầm về thôn An Hải:**
   - Dòng 6: Sửa "thuộc địa phận thôn An Hải trước đây" -> "thuộc thôn An Hải, trước đây thuộc xã Lộc Bình, nay thuộc xã Phú Lộc".
5. **[MINOR m-03] Khách quan hóa văn phong biểu cảm:**
   - Dòng 79: Thay "khoảnh khắc đẹp nhất trong ngày" bằng "thời điểm thuận lợi trong ngày".
   - Dòng 89: Thay "vị trí buông cần lý tưởng" bằng "vị trí buông cần thích hợp".
   - Dòng 96: Thay "thời gian lý tưởng nhất" bằng "thời gian thuận lợi nhất trong năm".
   - Dòng 137: Thay "Khung giờ lý tưởng nhất" bằng "Khung giờ thích hợp nhất".
6. **[MINOR m-04] Bổ sung tên thực thể đảm bảo Chunk Independence:**
   - Dòng 49: Bổ sung định danh "tại Bãi biển Lộc Bình" vào đầu đoạn Hệ động vật đáy và rạn đá.
   - Dòng 89: Bổ sung định danh "tại Bãi biển Lộc Bình" vào đầu đoạn Câu cá giải trí ven ghềnh.

---

### 2.2. Tệp `Bãi biển Bình An.md`
1. **[MAJOR M-03 & M-04] Loại bỏ từ cấm tiếp thị hoa mỹ:**
   - Dòng 69: Sửa "phát triển sôi động bậc nhất khu vực" thành "phát triển sôi động, thu hút đông đảo du khách trong khu vực".
   - Dòng 70: Sửa "khu phức hợp nghỉ dưỡng đẳng cấp quốc tế" thành "khu phức hợp nghỉ dưỡng tiêu chuẩn quốc tế quy mô lớn".
2. **[MAJOR M-05] Khắc phục lỗi lặp từ:**
   - Dòng 33: Sửa "vùng biển bãi biển Bình An" thành "vùng biển ven bãi biển Bình An".
3. **[MAJOR M-06] Bổ sung tên thực thể tối ưu hóa Chunk Independence:**
   - Dòng 34: Bổ sung "Vùng biển ven bãi biển Bình An và vịnh Chân Mây...".
   - Dòng 49: Bổ sung "tại bãi biển Bình An" vào câu mở đầu mục Dã ngoại và cắm trại ven biển.
   - Dòng 55: Bổ sung "Khu vực bãi biển Bình An chịu ảnh hưởng...".
   - Dòng 56: Bổ sung "lấy bãi biển Bình An làm địa điểm thực hành ngoài biển trọng tâm...".
4. **[MINOR m-05] Bổ sung pháp nhân xử phạt hành chính:**
   - Dòng 35: Ghi rõ tên pháp nhân vận hành bến cảng bị xử phạt 532 triệu đồng: `(Công ty TNHH MTV Hào Hưng Huế)` theo đúng Quyết định 3089/QĐ-XPHC ngày 02/12/2024 của UBND tỉnh Thừa Thiên Huế.
5. **[MINOR m-06] Chuẩn hóa danh xưng thực thể:**
   - Dòng 25, 63, 77, 79: Đổi các danh xưng rút gọn ("Bờ biển Bình An", "bờ biển Bình An", "Biển Bình An", "Bãi biển") thành tên chuẩn hóa "Bãi biển Bình An" ở đầu câu.

---

### 2.3. Tệp `Bãi biển Cảnh Dương.md`
1. **[MAJOR M-07] Loại bỏ từ ngữ cấm quảng cáo hoa mỹ:**
   - Dòng 15: Sửa "nổi bật bậc nhất" thành "tiêu biểu".
   - Dòng 177 (nay dòng 181): Sửa "siêu tàu du lịch đẳng cấp" thành "các chuyến tàu du lịch biển quốc tế tải trọng lớn".
2. **[MAJOR M-08 & MINOR m-08] Khắc phục đại từ thiếu ngữ cảnh và bổ sung câu dẫn nhập:**
   - Dòng 123: Thay "Đây là khoảng thời gian..." bằng "Giai đoạn từ tháng 4 đến tháng 8 là khoảng thời gian lý tưởng nhất để tham quan, tắm biển và cắm trại tại Bãi biển Cảnh Dương."
   - Dòng 127: Thay "Từ tháng 9 trở đi..." bằng "Tại Bãi biển Cảnh Dương, từ tháng 9 trở đi, vùng biển bước vào mùa mưa bão lớn...".
   - Dòng 131: Thay "Khí hậu thời kỳ này..." bằng "Trong giai đoạn từ tháng 1 đến tháng 3, khí hậu tại Bãi biển Cảnh Dương mang nét se lạnh chuyển tiếp của đầu xuân...".
   - Bổ sung câu dẫn nhập cho 2 tiểu mục: dòng 145 ("Để đến Bãi biển Cảnh Dương, du khách có thể lựa chọn các phương tiện di chuyển phổ biến sau:") và dòng 162 ("Khi tham gia cắm trại dã ngoại và đốt lửa trại qua đêm tại Bãi biển Cảnh Dương, du khách cần tuân thủ nghiêm các nguyên tắc an toàn:").
   - Dòng 194: Cập nhật "vùng biển thành phố Huế (trước đây là Thừa Thiên Huế)".
3. **[MINOR m-07] Xóa trailing space:**
   - Dòng 42: Xóa khoảng trắng thừa ở cuối dòng sau dấu ngoặc đơn `cửa Khế/Lăng Cô).`.
4. **[MINOR m-09] Khách quan hóa văn phong:**
   - Dòng 19: Thay "lựa chọn hàng đầu" bằng "lựa chọn phổ biến".
   - Dòng 81: Thay "hoạt động hấp dẫn hàng đầu" bằng "một trong những hoạt động thu hút đông đảo du khách nhất".
   - Dòng 112: Thay "Món ăn trứ danh" bằng "Món ăn đặc sản phổ biến".
5. **[MINOR m-10] Sửa cách ghép từ không tự nhiên:**
   - Dòng 64, 70, 75: Sửa "làng chài Bãi biển Cảnh Dương" thành "làng chài Cảnh Dương ven Bãi biển Cảnh Dương", "làng chài Cảnh Dương tại Bãi biển Cảnh Dương".
6. **[MINOR m-11] Sửa lỗi lặp từ:**
   - Dòng 56: Sửa "dưới bóng râm râm mát" thành "dưới bóng cây râm mát".

---

### 2.4. Tệp `Vịnh Lăng Cô.md`
1. **[BLOCKER B-01] Xóa bỏ triệt để chuỗi rò rỉ siêu dữ liệu AI/RAG nội bộ:**
   - Dòng 18: Xóa hoàn toàn câu chứa `tệp Vịnh Lăng Cô.md`, viết lại tự nhiên: "Không gian Vịnh Lăng Cô bao quát trọn vẹn cả vùng mặt nước vịnh biển lẫn dải bờ cát bãi biển Lăng Cô liên hoàn."
   - Dòng 235, 236, 237, 238: Xóa triệt để các chú thích rò rỉ metadata kỹ thuật:
     + Xóa `*(nội dung chi tiết thuộc file canonical Đầm Lập An.md)*`.
     + Xóa `*(nội dung chi tiết thuộc file canonical Vườn quốc gia Bạch Mã.md)*`.
     + Xóa `*(nội dung cung đường thuộc file Đèo Hải Vân.md, nội dung di tích lịch sử kiến trúc thuộc file canonical domain heritages Hải Vân Quan.md)*`.
     + Xóa `*(nội dung chi tiết thuộc file canonical Bãi biển Cảnh Dương.md)*`.
2. **[MAJOR M-09] Loại bỏ hàng loạt mỹ từ cấm quảng cáo:**
   - Dòng 16: Thay "nổi tiếng bậc nhất", "ngút ngàn" bằng văn phong trung tính ("danh thắng duyên hải tiêu biểu", "rặng núi đá thuộc sườn đông").
   - Dòng 53: Bỏ "đẹp nhất hành tinh", sửa thành "Để được công nhận là thành viên Câu lạc bộ Các vịnh đẹp nhất thế giới...".
   - Dòng 86: Bỏ "phức hợp bậc nhất", sửa thành "Vịnh Lăng Cô mang cấu trúc sinh thái liên hoàn tiêu biểu của duyên hải miền Trung."
   - Dòng 121: Bỏ "an toàn và dễ chịu nhất", sửa thành "điểm tắm biển thuận lợi...".
   - Dòng 158: Bỏ "độc đáo bậc nhất".
   - Dòng 208: Bỏ "đường sắt đẹp nhất hành tinh", sửa thành "hành trình đường sắt ấn tượng hàng đầu thế giới".
   - Dòng 235: Bỏ từ biểu cảm "tuyệt đẹp".
3. **[MAJOR M-10] Chuẩn hóa dữ kiện gia nhập Worldbays Club:**
   - Dòng 12 và dòng 47: Chuẩn hóa mốc thời gian kép: Trao chứng nhận kết nạp ngày 16/05/2009 tại Setúbal (Bồ Đào Nha) và lễ đón nhận danh hiệu tại Huế ngày 06/06/2009; ghi nhận rõ thành viên thứ 28 hoặc thứ 30 tùy danh mục thống kê từng thời kỳ.
4. **[MAJOR M-11] Bổ sung tên thực thể vào 100% tiêu đề H2 và H3:**
   - Bổ sung định danh "Vịnh Lăng Cô" vào toàn bộ tiêu đề:
     + Dòng 22: `## Cấu trúc địa lý và cảnh quan Vịnh Lăng Cô`
     + Dòng 24: `### Hình thế lòng vịnh hình trăng khuyết và dải bãi cát Vịnh Lăng Cô`
     + Dòng 30: `### Màu nước biển và chế độ thủy động lực tại Vịnh Lăng Cô`
     + Dòng 43: `## Vị thế danh hiệu Vịnh đẹp thế giới của Vịnh Lăng Cô`
     + Dòng 45: `### Mốc lịch sử gia nhập Worldbays Club năm 2009`
     + Dòng 65: `## Dấu ấn lịch sử và văn hóa nghỉ dưỡng hoàng gia tại Vịnh Lăng Cô`
     + Dòng 82: `## Hệ sinh thái giao thoa biển – đầm phá – núi rừng tại Vịnh Lăng Cô`
     + Dòng 100: `## Đời sống ngư nghiệp và các làng chài cổ ven Vịnh Lăng Cô`
     + Dòng 117: `## Trải nghiệm du lịch và nghỉ dưỡng biển tại Vịnh Lăng Cô`
     + Dòng 119: `### Hoạt động tắm biển và vui chơi trên bãi cát Vịnh Lăng Cô`
     + Dòng 169: `## Mùa biển, khí hậu và quy luật thời tiết tại Vịnh Lăng Cô`
     + Dòng 193: `## Tuyến giao thông tiếp cận và kết nối Vịnh Lăng Cô`
     + Dòng 216: `## An toàn tắm biển và bảo tồn môi trường Vịnh Lăng Cô`
     + Dòng 232: `## Mối liên kết không gian du lịch vùng của Vịnh Lăng Cô`
     + Dòng 240: `## Thông tin dành cho du khách tham quan Vịnh Lăng Cô`
5. **[MINOR m-12] Đính chính nguyên liệu đặc sản mắm sò:**
   - Dòng 159: Sửa nguyên liệu sò huyết thành "sò lông tươi (người dân địa phương quen gọi là con sặc) đánh bắt từ vùng rạn đá và bãi cát ven vịnh".
6. **[MINOR m-13] Bổ sung niên đại khắc dựng bia đá Tịnh Viêm:**
   - Dòng 80: Bổ sung niên đại khắc dựng tấm bia đá "Tịnh Viêm hành cung bi ký" vào khoảng năm 1919 (năm Kỷ Mùi).
7. **[MINOR m-14] Khách quan hóa an toàn giao thông và thời điểm tham quan:**
   - Dòng 202: Sửa "an toàn nhất" -> "thuận tiện và nhanh chóng".
   - Dòng 242: Sửa "Thời điểm lý tưởng nhất" -> "Thời điểm thích hợp: Từ tháng 4 đến tháng 8 hằng năm khi thời tiết nhiều nắng, biển lặng và sóng êm."

---

### 2.5. Hồ sơ kiểm chứng `tourism-research-evidence.md`
- **Mục XVI (Lộc Bình):** Bổ sung ghi chú định hướng địa lý Tuyến 1 (đi men bờ nam đầm Cầu Hai, không qua cầu Tư Hiền) và Tuyến 2 (đi qua xã Phú Vinh rồi qua cầu Tư Hiền sang bờ nam).
- **Mục XVII (Bình An):** Bổ sung tên pháp nhân bị xử phạt 532 triệu đồng: Công ty TNHH MTV Hào Hưng Huế theo Quyết định 3089/QĐ-XPHC.
- **Mục XIX (Vịnh Lăng Cô):** Cập nhật ngày trao kết nạp Worldbays Club (16/05/2009 tại Setúbal) và ngày đón nhận (06/06/2009 tại Huế), niên đại bia Tịnh Viêm năm 1919, và nguyên liệu mắm sò lông (con sặc).
- **Làm sạch định dạng:** Cắt bỏ 100% khoảng trắng thừa (trailing whitespace) trong toàn bộ tệp evidence.

---

## 3. Cách đã chạy thật (Real Execution & Verification)

1. **Thực thi bản vá văn bản:**
   - Sử dụng công cụ `replace_file_content` áp dụng chính xác từng khối thay đổi từ đề xuất Unified Diff Proposals của Reviewer Codex.
2. **Kiểm thử tự động bằng Python script:**
   - Chạy script kiểm tra lint trên cả 4 tệp thực thể với 7 tiêu chí nghiêm ngặt:
     + Tiêu đề H1 bắt đầu dòng 1: **PASS 100%**.
     + Không YAML frontmatter: **PASS 100%**.
     + Không wiki-link `[[]]`: **PASS 100%**.
     + Không tồn tại chuỗi rò rỉ metadata AI/RAG (`canonical`, `file `, `tệp `, `.md`, `domain heritages`): **PASS 100%**.
     + Không có từ cấm tiếp thị hoa mỹ (`bậc nhất`, `đẳng cấp`, `đẹp nhất hành tinh`, v.v.): **PASS 100%**.
     + Trailing whitespace: **0 lỗi trên toàn bộ 4 tệp thực thể và tệp evidence**.
     + Tiêu đề H2/H3 tự chứa định danh thực thể: **PASS 100%**.
3. **Kết quả kiểm thử tự động:**
   ```
   === Checking: Bãi biển Lộc Bình.md (141 lines) === PASSED
   === Checking: Bãi biển Bình An.md (80 lines) === PASSED
   === Checking: Bãi biển Cảnh Dương.md (194 lines) === PASSED
   === Checking: Vịnh Lăng Cô.md (246 lines) === PASSED
   ALL 4 FILES PASSED LINT CHECKS 100%!
   Total trailing whitespace issues: 0
   ```

---

## 4. Ma trận giải quyết vi phạm (Resolution Matrix)

| Mã vi phạm | Tệp thực thể | Phân loại | Trạng thái | Ghi chú giải quyết |
|:---|:---|:---:|:---:|:---|
| **B-01** | Vịnh Lăng Cô | **Blocker** | **RESOLVED** | Xóa sạch chuỗi `tệp Vịnh Lăng Cô.md`, `file canonical...`, `domain heritages...`. |
| **M-01** | Bãi biển Lộc Bình | Major | **RESOLVED** | Sửa sai lệch địa lý cầu Tư Hiền ở Tuyến 1 (đi bờ nam không qua cầu). |
| **M-02** | Bãi biển Lộc Bình | Major | **RESOLVED** | Sửa trùng lặp xã Phú Diên và Phú Vinh ở Tuyến 2. |
| **m-01** | Bãi biển Lộc Bình | Minor | **RESOLVED** | Xóa khoảng trắng thừa dòng 92. |
| **m-02** | Bãi biển Lộc Bình | Minor | **RESOLVED** | Đính chính thôn An Hải thuộc xã Phú Lộc. |
| **m-03** | Bãi biển Lộc Bình | Minor | **RESOLVED** | Khách quan hóa 4 vị trí văn phong cảm tính ("đẹp nhất", "lý tưởng nhất"). |
| **m-04** | Bãi biển Lộc Bình | Minor | **RESOLVED** | Bổ sung tên thực thể vào bullet rạn đá và câu cá giải trí. |
| **M-03** | Bãi biển Bình An | Major | **RESOLVED** | Loại bỏ "sôi động bậc nhất" tại dòng 69. |
| **M-04** | Bãi biển Bình An | Major | **RESOLVED** | Loại bỏ "đẳng cấp quốc tế" tại dòng 70. |
| **M-05** | Bãi biển Bình An | Major | **RESOLVED** | Sửa lỗi lặp từ "vùng biển bãi biển Bình An". |
| **M-06** | Bãi biển Bình An | Major | **RESOLVED** | Bổ sung thực thể bãi biển Bình An vào câu mở đầu các bullet items. |
| **m-05** | Bãi biển Bình An | Minor | **RESOLVED** | Bổ sung tên pháp nhân xử phạt: Công ty TNHH MTV Hào Hưng Huế. |
| **m-06** | Bãi biển Bình An | Minor | **RESOLVED** | Chuẩn hóa danh xưng "Bãi biển Bình An" thay cho từ rút gọn. |
| **M-07** | Bãi biển Cảnh Dương | Major | **RESOLVED** | Loại bỏ "nổi bật bậc nhất", "siêu tàu du lịch đẳng cấp". |
| **M-08** | Bãi biển Cảnh Dương | Major | **RESOLVED** | Bổ sung chủ ngữ/thực thể mở đầu đoạn và 2 câu dẫn nhập tiểu mục. |
| **m-07** | Bãi biển Cảnh Dương | Minor | **RESOLVED** | Xóa khoảng trắng thừa sau dấu đóng ngoặc đơn dòng 42. |
| **m-08** | Bãi biển Cảnh Dương | Minor | **RESOLVED** | Cập nhật "vùng biển thành phố Huế (trước đây là Thừa Thiên Huế)". |
| **m-09** | Bãi biển Cảnh Dương | Minor | **RESOLVED** | Khách quan hóa văn phong ("lựa chọn phổ biến", "thu hút đông đảo du khách"). |
| **m-10** | Bãi biển Cảnh Dương | Minor | **RESOLVED** | Sửa cách ghép từ không tự nhiên về làng chài Cảnh Dương. |
| **m-11** | Bãi biển Cảnh Dương | Minor | **RESOLVED** | Sửa typo lặp từ "dưới bóng râm râm mát". |
| **M-09** | Vịnh Lăng Cô | Major | **RESOLVED** | Loại bỏ toàn diện mỹ từ hoa mỹ ("bậc nhất", "đẹp nhất hành tinh", "tuyệt đẹp"). |
| **M-10** | Vịnh Lăng Cô | Major | **RESOLVED** | Chuẩn hóa mốc thời gian Worldbays (16/05/2009 tại Setúbal, 06/06/2009 tại Huế). |
| **M-11** | Vịnh Lăng Cô | Major | **RESOLVED** | Bổ sung tên thực thể "Vịnh Lăng Cô" vào 100% tiêu đề H2 và H3. |
| **m-12** | Vịnh Lăng Cô | Minor | **RESOLVED** | Đính chính mắm sò làm từ sò lông (con sặc), không dùng sò huyết. |
| **m-13** | Vịnh Lăng Cô | Minor | **RESOLVED** | Bổ sung niên đại bia đá Tịnh Viêm khắc dựng năm 1919. |
| **m-14** | Vịnh Lăng Cô | Minor | **RESOLVED** | Khách quan hóa an toàn giao thông hầm Hải Vân và thời điểm tham quan. |

---

## 5. Kết luận và Bàn giao

1. **Tổng kết:** 100% các vi phạm (01 Blocker, 11 Major, 14 Minor) đã được xử lý dứt điểm, chính xác và được tự động kiểm chứng đạt chuẩn RAG Clean.
2. **Trạng thái sẵn sàng:** Bộ 4 tệp thực thể Cụm Bãi biển & Vịnh biển Huế Đợt 2 đã sẵn sàng cho đợt kiểm tra tái thẩm định (re-review) của Reviewer Codex.
3. **Chuyển giao vai trò:** Chuyển trạng thái bàn giao trong `session_prompt/CURRENT_HANDOFF.md` sang `ready_for_re_review` với `Target role: reviewer`.
