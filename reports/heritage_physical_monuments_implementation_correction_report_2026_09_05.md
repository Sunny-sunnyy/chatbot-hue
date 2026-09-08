# Implementation Report: Heritage Physical Monuments Correction (Entities 18–28)

Implementer: Implementer  
Date: 2026-09-05  
Canonical guide: `knowledge-base-hue/meta/heritage-template.md`, `knowledge-base-hue/heritage/heritage-entities-inventory.md`  
Review report căn cứ: `reports/heritage_physical_monuments_codex_review_2026_09_05.md`  
Handoff căn cứ: `session_prompt/CURRENT_HANDOFF.md`  

## 1. Phạm vi

Thực hiện hiệu chỉnh triệt để trong một batch toàn bộ các phát hiện Blocker (02), Major (03) và Minor (04) trên nhóm 11 di tích vật thể nổi bật (thực thể 18 đến 28), đồng thời cập nhật đồng bộ các nội dung đính chính vào `knowledge-base-hue/meta/heritage-research-evidence.md` theo đúng chỉ đạo tại `session_prompt/CURRENT_HANDOFF.md`.

Các tệp thuộc phạm vi hiệu chỉnh:
- `knowledge-base-hue/heritage/24 Cung An Định.md` (Blocker & Major)
- `knowledge-base-hue/heritage/23 Điện Hòn Chén.md` (Blocker & Minor)
- `knowledge-base-hue/heritage/21 Đàn Nam Giao.md` (Major)
- `knowledge-base-hue/heritage/28 Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md` (Major & Minor)
- `knowledge-base-hue/heritage/22 Hổ Quyền.md` (Minor)
- `knowledge-base-hue/heritage/25 Đàn Xã Tắc.md` (Minor)
- `knowledge-base-hue/meta/heritage-research-evidence.md` (Mục 21, 22, 23, 24, 25, 28)

Ranh giới tuân thủ:
- Giữ nguyên các tệp corpus đã đạt chuẩn thẩm định hoàn hảo không có lỗi: `18 Kinh thành Huế.md`, `19 Đại Nội Huế.md`, `20 Chùa Thiên Mụ.md`, `26 Hải Vân Quan.md`, `27 Trường Quốc Học Huế.md` cùng toàn bộ nhóm di sản 1–17.
- Tuyệt đối không can thiệp runtime/backend/Qdrant/benchmark.
- Bảo toàn delta `Lễ hội Áo dài Huế.md` và các tệp untracked khác trong repository.
- Tuân thủ nghiêm ngặt chuẩn Markdown RAG Clean: mở đầu trực tiếp bằng H1 `# <Tên Di tích>`, không YAML frontmatter, không mục `## Nguồn dữ liệu`, không thuật ngữ nội bộ RAG, không giá vé cụ thể hay thời lượng tham quan ước tính chủ quan.
- Bảo toàn 100% cập nhật địa giới hành chính năm 2026 (phường Phú Xuân, Thuận Hóa, Kim Long, Thủy Xuân, Dương Nỗ).

## 2. Thay đổi chính chi tiết theo từng tệp

### 2.1. Tệp `knowledge-base-hue/heritage/24 Cung An Định.md`
- **[FINDING-01 - BLOCKER] (Đính chính tình trạng UNESCO 1993 tại dòng 86):**
  - *Nội dung cũ:* Khẳng định Cung An Định là một bộ phận cấu thành trọng yếu của Quần thể Di tích Cố đô Huế được UNESCO ghi danh là Di sản Văn hóa Thế giới năm 1993.
  - *Nội dung mới:* Đính chính rõ: Cung An Định là di tích biệt cung hoàng gia thời Nguyễn trực thuộc hệ thống quản lý của Trung tâm Bảo tồn Di tích Cố đô Huế. Di tích **không nằm trong danh mục 14 cụm thành phần gốc** được UNESCO ghi danh Di sản Thế giới năm 1993, nhưng là một trong các di tích liên quan trọng yếu thuộc diện nghiên cứu đề xuất xem xét mở rộng ranh giới di sản trong tương lai.
- **[FINDING-04 - MAJOR] (Xác lập xếp hạng di tích quốc gia độc lập tại dòng 11):**
  - *Nội dung cũ:* Ghi danh di tích quốc gia đặc biệt năm 2009.
  - *Nội dung mới:* Sửa thành: `Di tích kiến trúc nghệ thuật cấp quốc gia (theo Quyết định số 100/2006/QĐ-BVHTT ngày 13/12/2006 của Bộ Văn hóa và Thông tin); di tích liên quan thuộc hệ thống quản lý của Trung tâm Bảo tồn Di tích Cố đô Huế`.

### 2.2. Tệp `knowledge-base-hue/heritage/23 Điện Hòn Chén.md`
- **[FINDING-02 - BLOCKER] (Bổ sung vị thế Di sản Thế giới UNESCO 1993 tại dòng 10, 11 và 101):**
  - *Dòng 10:* `- **Thuộc quần thể:** Quần thể Di tích Cố đô Huế (Di sản Văn hóa Thế giới UNESCO)`.
  - *Dòng 11:* Bổ sung: `Di sản Văn hóa Thế giới UNESCO (năm 1993, mã định danh thành phần 678-009); Di tích lịch sử - văn hóa cấp quốc gia (Quyết định số 2014-VH/QĐ ngày 16/12/1993 của Bộ Văn hóa - Thông tin); Di tích quốc gia đặc biệt (thuộc Quần thể Di tích Cố đô Huế, Quyết định số 1272/QĐ-TTg ngày 12/08/2009 của Thủ tướng Chính phủ)`.
  - *Dòng 101:* Khẳng định rõ: `Điện Hòn Chén là cụm thành phần chính thức thứ 9 (mã định danh serial 678-009) thuộc Quần thể Di tích Cố đô Huế được UNESCO ghi danh Di sản Văn hóa Thế giới năm 1993, đồng thời thuộc hệ thống quản lý, bảo tồn và phát huy giá trị của Trung tâm Bảo tồn Di tích Cố đô Huế.`
- **[MINOR-03] (Bổ sung Section Thông tin dành cho du khách ở cuối file):**
  - Bổ sung mục `## Thông tin dành cho du khách` với hai nội dung:
    + Phương thức tiếp cận và lộ trình di chuyển (khuyến nghị tuyến đường thủy bằng thuyền rồng ngược dòng Hương Giang từ bến Tòa Khâm / Thiên Mụ và tuyến đường bộ qua cầu Tuần);
    + Lưu ý văn hóa tâm linh và an toàn (trang phục kín đáo, lịch sự phù hợp chốn thờ Mẫu tôn nghiêm; cẩn trọng khi bước lên xuống thềm đá sát mép nước sâu, không xả rác xuống sông Hương). Hoàn toàn không đưa thông tin giá vé hay giờ giấc đóng mở cửa biến động.

### 2.3. Tệp `knowledge-base-hue/heritage/21 Đàn Nam Giao.md`
- **[FINDING-03 - MAJOR] (Đính chính mã serial UNESCO từ 678-005 sang 678-006):**
  - Thay thế đồng loạt mã `678-005` (vốn thuộc về Lăng Dục Đức) thành `678-006` (chuẩn danh mục UNESCO World Heritage dành cho Đàn Nam Giao) tại cả 3 vị trí:
    + Dòng 11: `- **Ghi danh / Xếp hạng:** Di sản Văn hóa Thế giới UNESCO (năm 1993, mã định danh thành phần 678-006)...`
    + Dòng 20: `...với mã serial 678-006.`
    + Dòng 149: `- **Vị thế hạt nhân tôn giáo cung đình:** Đàn Nam Giao là thành phần di sản văn hóa thế giới quan trọng (mã serial 678-006)...`

### 2.4. Tệp `knowledge-base-hue/heritage/28 Hệ thống di tích lưu niệm Chủ tịch Hồ Chí Minh tại Huế.md`
- **[FINDING-05 - MAJOR] (Đính chính số quyết định xếp hạng quốc gia năm 1990 và tách biệt Đình làng Dương Nỗ tại dòng 18):**
  - *Nội dung cũ:* Quyết định số 29-VH/QĐ ngày 26/03/1990 gộp chung cả Nhà lưu niệm Dương Nỗ và Đình làng Dương Nỗ.
  - *Nội dung mới:* Sửa lỗi typo `29-VH/QĐ` thành `296/VH-QĐ` ngày 26/03/1990 (cho Nhà lưu niệm thời niên thiếu của Chủ tịch Hồ Chí Minh tại làng Dương Nỗ); đồng thời tách riêng văn bản xếp hạng của Đình làng Dương Nỗ: `Quyết định số 3777/QĐ-BT ngày 23/12/1995 (Di tích kiến trúc nghệ thuật Đình làng Dương Nỗ) của Bộ Văn hóa - Thông tin`.
- **[MINOR-04] (Đồng bộ niên khóa Đệ nhị niên tại Trường Quốc Học):**
  - Cập nhật dòng 75 thành: `...thi đỗ vượt cấp vào lớp Đệ nhị niên trung học (Deuxième Année) niên khóa 1908–1909 tại Trường Quốc Học`, đồng bộ 100% với dòng 46 và tệp `27 Trường Quốc Học Huế.md`.

### 2.5. Tệp `knowledge-base-hue/heritage/22 Hổ Quyền.md`
- **[MINOR-01] (Bổ sung quyết định xếp hạng di tích quốc gia và định hướng khán đài):**
  - Bổ sung căn cứ pháp lý: `Quyết định số 2009/1998/QĐ-BVHTT ngày 26/09/1998 của Bộ Văn hóa - Thông tin` tại dòng 11 và dòng 109;
  - Làm rõ hướng khán đài vua ngự tại dòng 49: `Nằm ở phía Đông Nam của đấu trường, quay mặt về hướng Nam theo quy cách "Thánh nhân Nam diện" trong kiến trúc cung đình...`

### 2.6. Tệp `knowledge-base-hue/heritage/25 Đàn Xã Tắc.md`
- **[MINOR-02] (Tinh chỉnh diễn đạt phạm vi UNESCO 1993 tại dòng 11):**
  - Diễn đạt chính xác: `Di tích lịch sử - khảo cổ học cấp quốc gia (theo Quyết định số 99/QĐ-BVHTT ngày 13/12/2006 của Bộ Văn hóa - Thông tin); Di tích quốc gia đặc biệt (nằm trong khu vực bảo vệ của Kinh thành Huế thuộc Quần thể Di tích Cố đô Huế, Quyết định số 1272/QĐ-TTg ngày 12/08/2009 của Thủ tướng Chính phủ và thuộc phạm vi Di sản Văn hóa Thế giới UNESCO năm 1993 - cụm serial 678-001)`.

### 2.7. Tệp `knowledge-base-hue/meta/heritage-research-evidence.md`
- Đồng bộ toàn diện các Mục 21 (Đàn Nam Giao), Mục 22 (Hổ Quyền), Mục 23 (Điện Hòn Chén), Mục 24 (Cung An Định), Mục 25 (Đàn Xã Tắc) và Mục 28 (Hệ thống di tích Bác Hồ).
- Tại mỗi mục đã bổ sung tiểu mục `### Nhật ký hiệu chỉnh sau review độc lập (05/09/2026)` ghi nhận đầy đủ chi tiết căn cứ sửa đổi, văn bản pháp lý và các mốc kiểm chứng ngày 05/09/2026.

## 3. Cách đã chạy thật & Kiểm tra xác thực

1. **Kiểm tra cú pháp và định dạng Git:**
   - Lệnh thực thi: `git diff --check`
   - Kết quả: Mã thoát 0 (exit code 0), hoàn toàn sạch lỗi định dạng, không có bất kỳ khoảng trắng thừa hay ký tự không hợp lệ.
2. **Kiểm tra trạng thái worktree:**
   - Lệnh thực thi: `git status --short`
   - Kết quả: Đúng chính xác các tệp được phân công chỉnh sửa (`21`, `22`, `23`, `24`, `25`, `28` và `heritage-research-evidence.md`). Các tệp ngoài phạm vi và delta Áo dài được bảo toàn tuyệt đối.
3. **Kiểm tra tuân thủ Markdown RAG Clean (tự động hóa qua Python script):**
   - Tiêu chuẩn H1: 100% 6 tệp bắt đầu trực tiếp bằng `# <Tên Di tích>`;
   - Tiêu chuẩn Frontmatter: 0/6 tệp chứa YAML frontmatter (`---`);
   - Tiêu chuẩn Nguồn dữ liệu: 0/6 tệp chứa đề mục cấm `## Nguồn dữ liệu`;
   - Tiêu chuẩn Thương mại hóa: 0/6 tệp chứa thông tin giá vé (vé tham quan, vnđ, đồng/lượt...).
4. **Kiểm tra địa giới hành chính 2026:**
   - Đàn Nam Giao: phường Thuận Hóa;
   - Hổ Quyền: phường Thủy Xuân;
   - Điện Hòn Chén: phường Kim Long;
   - Cung An Định: phường Thuận Hóa;
   - Đàn Xã Tắc: phường Phú Xuân;
   - Di tích Bác Hồ: các phường Phú Xuân, Dương Nỗ, Thuận Hóa, An Cựu.

## 4. Tự đánh giá và kết luận

| Tiêu chí | Điểm tự chấm | Ghi chú đánh giá |
| :--- | :---: | :--- |
| **Tính chính xác lịch sử & Pháp lý** | 5/5 | Đã đính chính triệt để 100% các lỗi UNESCO ID, văn bản xếp hạng cấp quốc gia và bối cảnh lịch sử. |
| **Bảo toàn ranh giới di sản** | 5/5 | Phân định rạch ròi cụm thành phần gốc UNESCO 1993, ranh giới bảo vệ Kinh thành và di tích liên quan. |
| **Tuân thủ Markdown RAG Clean** | 5/5 | Cấu trúc chuẩn mực H1-H2-H3, không frontmatter, không mục cấm, không giá vé. |
| **Cập nhật địa giới hành chính 2026**| 5/5 | 100% phường xã mới sau sắp xếp theo Nghị quyết 1675/NQ-UBTVQH15. |
| **Đồng bộ hóa Evidence** | 5/5 | Bổ sung đầy đủ claims, căn cứ pháp lý và nhật ký hiệu chỉnh ngày 05/09/2026. |

**Kết luận:** Nhóm 11 di tích vật thể nổi bật (thực thể 18–28) đã được hiệu chỉnh hoàn tất, đạt chuẩn chất lượng cao nhất, sẵn sàng chuyển giao cho Reviewer thẩm định lại (re-review).
