# Codex Review: Performing Arts Batch 03 (4 thực thể nghệ thuật đương đại và đại nhạc hội)

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-05
Canonical guide: `knowledge-base-hue/meta/performing-arts-template.md` & `knowledge-base-hue/performing_arts/performing-arts-entities-inventory.md`
Implementation report / evidence: `knowledge-base-hue/meta/performing-arts-research-evidence.md`

## 1. Phạm vi đã review

Reviewer cùng 4 sub-agent chuyên trách độc lập đã thẩm định và kiểm chứng chéo toàn diện 4 tệp thực thể thuộc nhóm "Đại nhạc hội và chương trình biểu diễn đương đại" trong domain `performing_arts` tại mốc thời gian 05/09/2026:
1. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Mega Booming – Huế.md`
2. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Đêm Hoàng cung – Dạ yến Hoàng cung.md`
3. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế Wonderverse Music Fest.md`
4. `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế by Light – The Live Show.md`
- Hồ sơ kiểm chứng tại `knowledge-base-hue/meta/performing-arts-research-evidence.md`

Quy trình thẩm định độc lập gồm:
- Rà soát 100% chuẩn Markdown RAG Clean: khởi đầu bằng H1 duy nhất, không YAML frontmatter, không mục `## Nguồn dữ liệu`, không wiki-link `[[]]`, và khả năng tự đứng độc lập của từng chunk H2/H3.
- Kiểm tra tính bền vững của tri thức: loại bỏ triệt để giá vé thương mại biến động khỏi nội dung answer-facing.
- Thẩm định ranh giới thực thể (Entity boundary) giữa các sự kiện thương mại tư nhân (Mega Booming), sự kiện hợp tác ngoại giao đặc biệt 1 kỳ (Huế by Light), dịch vụ trải nghiệm di sản kinh tế đêm (Dạ yến Hoàng cung) và IP lễ hội di sản thường niên mới (Huế Wonderverse).
- Kiểm chứng sự thật thời gian thực (05/09/2026) bằng 100% câu lệnh truy vấn tiếng Việt qua Web Search và đối chiếu các nguồn thẩm quyền: Cổng TTĐT TP. Huế (`hue.gov.vn`), Trung tâm Bảo tồn Di tích Cố đô Huế (HMCC), Viện Pháp tại Việt Nam, Sở VHTT, Sở Du lịch và báo chí chính thống (Nhân Dân, TTXVN, Tuổi Trẻ, Thanh Niên).

## 2. Findings

### Blocker (0 finding)
- Không có lỗi blocker làm gián đoạn pipeline RAG.

### Major (4 findings trên 2 tệp)

#### Finding M1: Khuyết thiếu mục `## Thông tin chung` và sai tiêu đề H2 đầu tiên
- **Tệp:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế Wonderverse Music Fest.md`
- **Vị trí:** Dòng 3.
- **Hiện trạng:** Tệp hoàn toàn thiếu khối thuộc tính `## Thông tin chung` (Core Metadata) ở đầu tệp sau H1. Tiêu đề mục H2 đầu tiên đang đặt là `## Tổng quan sự kiện / chương trình` thay vì `## Tổng quan`.
- **Requirement:** Mục 1 và Mục 2.1 của `meta/performing-arts-template.md`: Cấu trúc bắt buộc của thực thể sau H1 phải có mục `## Thông tin chung` (danh mục bullet-point gồm Tên chính thức, Loại hình, Tính chất tổ chức, Thời điểm lần đầu, Không gian biểu diễn, Đơn vị chủ trì/sản xuất...), sau đó đến `## Tổng quan`.
- **Tác động:** Gây mất đồng bộ schema với toàn bộ 10 tệp thực thể còn lại trong domain `performing_arts`, làm giảm hiệu quả trích xuất metadata nhanh của hệ thống RAG.
- **Tiêu chí đóng:** Bổ sung trọn vẹn mục `## Thông tin chung` chuẩn hóa theo template; đổi tiêu đề dòng 3 từ `## Tổng quan sự kiện / chương trình` thành `## Tổng quan`.

#### Finding M2: Sai lệch địa giới hành chính và bản chất không gian Quảng trường Văn hóa – Thể thao
- **Tệp:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế Wonderverse Music Fest.md`
- **Vị trí:** Dòng 17 và dòng 63.
- **Hiện trạng:**
  - Dòng 17 ghi: `...thuộc Khu đô thị mới An Cựu City`.
  - Dòng 63 ghi: `...phường An Đông/Xuân Phú, quận Thuận Hóa, TP. Huế`.
- **Requirement:** Mục 2.5 của `meta/performing-arts-template.md` và Nghị quyết số 1675/NQ-UBTVQH15 về đơn vị hành chính TP. Huế trực thuộc Trung ương.
- **Evidence:**
  - Quảng trường Văn hóa – Thể thao tỉnh/thành phố Huế tọa lạc tại số 01 Hà Huy Tập (giao lộ Tố Hữu – Hà Huy Tập) là công trình thiết chế văn hóa thể thao công cộng do Nhà nước đầu tư và quản lý. Công trình nằm tiếp giáp/đối diện khu đô thị An Cựu City chứ KHÔNG PHẢI thuộc dự án bất động sản tư nhân An Cựu City.
  - Về địa giới hành chính sau sắp xếp năm 2025: Khu vực này thuộc phường Vỹ Dạ (sau khi điều chỉnh, sáp nhập phường Xuân Phú cũ), quận Thuận Hóa, TP. Huế (khu vực bờ nam sông Hương). Trong khi đó, An Cựu City nằm tại phường An Đông. Không được ghi lưỡng lự "phường An Đông/Xuân Phú".
- **Tác động:** Gây sai lệch bản chất pháp lý của không gian công cộng thành dự án tư nhân, đồng thời làm sai lệch địa giới hành chính cấp phường.
- **Tiêu chí đóng:**
  - Sửa dòng 17 thành: `Quảng trường Văn hóa – Thể thao thành phố Huế (số 01 đường Hà Huy Tập, tiếp giáp trục đường Tố Hữu, tiếp giáp Khu đô thị An Cựu City)`.
  - Sửa dòng 63 thành: `Quảng trường Văn hóa – Thể thao thành phố Huế (số 01 đường Hà Huy Tập, phường Vỹ Dạ, quận Thuận Hóa, TP. Huế)`.

#### Finding M3: Dò rỉ thuật ngữ kỹ thuật AI nội bộ trong nội dung answer-facing
- **Tệp:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế by Light – The Live Show.md`
- **Vị trí:** Dòng 71.
- **Hiện trạng:** Câu dẫn nguyên văn ghi: *"Để đảm bảo tính chính xác cho công tác tra cứu thông tin và hệ thống RAG, Huế by Light – The Live Show cần được phân định rõ ràng với các thực thể văn hóa - lễ hội khác tại Cố đô Huế:"*.
- **Requirement:** Mục 2.6 của `meta/performing-arts-template.md`: Tuyệt đối không để lộ các thuật ngữ nội bộ như "hệ thống RAG", "cơ sở tri thức", "corpus", "chunk", "prompt" trong phần nội dung answer-facing của tệp tri thức.
- **Tác động:** Dò rỉ meta-terminology vào văn bản tri thức, làm giảm tính tự nhiên và tính bách khoa của câu trả lời khi hệ thống RAG trích xuất trả lời người dùng cuối.
- **Tiêu chí đóng:** Hiệu chỉnh câu dẫn dòng 71 thành văn phong tự nhiên: *"Để đảm bảo tính chuẩn xác và tránh nhầm lẫn với các hoạt động biểu diễn khác tại Cố đô Huế, Huế by Light – The Live Show cần được phân định rõ ràng với các thực thể liên quan:"*.

#### Finding M4: Sai tên nhạc sĩ thành viên ban nhạc Limebócx
- **Tệp:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế by Light – The Live Show.md`
- **Vị trí:** Dòng 53.
- **Hiện trạng:** Ghi nghệ sĩ thành viên ban nhạc Limebócx là *"Chu Duyên Tùng (nghệ danh Đờ Tùng – phụ trách guitar, hiệu ứng điện tử và beatbox)"*.
- **Evidence:** Ban nhạc Limebócx là bộ đôi gồm nghệ sĩ Trang Lê (Lê Trang) và **Hà Đăng Tùng** (nghệ danh Đờ Tùng). Tên "Chu Duyên Tùng" là lỗi ghép nhầm biệt danh "Chuối" của ca sĩ Trang Lê với nghệ danh Đờ Tùng.
- **Tác động:** Sai lệch thông tin nhân vật nghệ thuật thực tế (fact-checking error), gây hallucination khi tra cứu về nghệ sĩ tham gia chương trình.
- **Tiêu chí đóng:** Đính chính tên nghệ sĩ tại dòng 53 thành: **Hà Đăng Tùng (nghệ danh Đờ Tùng)**.

### Minor (4 findings trên 3 tệp)

#### Finding m1: Bổ sung định danh thực thể tại tiêu đề và câu dẫn mục thông tin khán giả
- **Tệp:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế by Light – The Live Show.md`
- **Vị trí:** Dòng 78–80.
- **Hiện trạng:** Tiêu đề và câu mở đầu viết chung chung: *"## Thông tin dành cho khán giả và lưu ý thưởng thức nghệ thuật di sản / Đối với các sự kiện nghệ thuật công nghệ cao ngoài trời tại không gian di sản kiến trúc Huế..."* thiếu danh xưng thực thể trực tiếp.
- **Tiêu chí đóng:** Bổ sung định danh thực thể vào câu dẫn để đảm bảo tính độc lập ngữ cảnh khi chunking: *"Khi tham gia thưởng thức chương trình nghệ thuật âm thanh – ánh sáng như Huế by Light – The Live Show hoặc các sự kiện 3D mapping quy mô tương tự tại không gian di sản Ngọ Môn..."*.

#### Finding m2: Tiết chế một số mỹ từ mang sắc thái ca ngợi, quảng bá cảm tính
- **Tệp:** `Huế by Light – The Live Show.md` và `Huế Wonderverse Music Fest.md`.
- **Vị trí:**
  - `Huế by Light`: "hiện đại bậc nhất" (dòng 39), "biến ảo kỳ ảo" (dòng 41), "Thành công vang dội" (dòng 67).
  - `Huế Wonderverse`: "độc bản" (dòng 36), "bùng nổ" (dòng 45), "huyền thoại" (dòng 55).
- **Tiêu chí đóng:** Chuyển đổi sang văn phong bách khoa trung tính, khách quan (ví dụ: "tiêu chuẩn kỹ thuật cao", "biến chuyển sống động", "sự đón nhận tích cực của công chúng", "điểm nhấn đặc trưng", "các ca khúc tiêu biểu").

#### Finding m3: Bổ sung đối tác đồng phát triển IP và sản xuất Lễ hội Wonderverse
- **Tệp:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Huế Wonderverse Music Fest.md`
- **Vị trí:** Dòng 50–53.
- **Hiện trạng:** Mới chỉ nêu UBND TP. Huế, Ban Tổ chức Festival Huế và Carlsberg Việt Nam / Huda, chưa ghi nhận đơn vị đối tác tư vấn, sáng tạo và đồng phát triển IP lễ hội.
- **Tiêu chí đóng:** Ghi nhận thêm Beyond Communication trong danh sách đơn vị đối tác đồng phát triển IP và phối hợp sản xuất cùng Carlsberg Việt Nam.

#### Finding m4: Nhấn mạnh tính chất địa phương đối với sự kiện mở rộng của Mega Booming
- **Tệp:** `/home/minhhieu/hue_rag/knowledge-base-hue/performing_arts/arts/Mega Booming – Huế.md`
- **Vị trí:** Dòng 92.
- **Hiện trạng:** Đề cập sự kiện Day 3 "Mega Booming – Charmora City" tại TP. Nha Trang (Khánh Hòa) năm 2026.
- **Tiêu chí đóng:** Làm rõ đây là sự kiện mở rộng thương hiệu tổ chức tại tỉnh thành khác, nhằm phân định rõ ràng để hệ thống truy vấn không nhầm lẫn không gian địa lý của corpus Cố đô Huế.

## 3. Cách Reviewer chạy lại thật

1. **Kiểm tra cú pháp và định dạng Git:**
   ```bash
   git diff --check
   git status --short
   ```
2. **Đọc và đối chiếu toàn văn 4 tệp thực thể:**
   - `Mega Booming – Huế.md` (119 dòng).
   - `Đêm Hoàng cung – Dạ yến Hoàng cung.md` (152 dòng).
   - `Huế Wonderverse Music Fest.md` (89 dòng).
   - `Huế by Light – The Live Show.md` (85 dòng).
3. **Thực hiện tra cứu đối chiếu độc lập bằng Web Search (mốc 05/09/2026):**
   - Lịch trình và sự thật lịch sử của đại nhạc hội Mega Booming Huế năm 2025: quyết định hoãn ngày 23/03/2025; Day 1 diễn ra 06/07/2025 tại Ngọ Môn; Day 2 diễn ra 21/12/2025 tại Ngọ Môn dưới mưa rét; địa giới Quảng trường Ngọ Môn (phường Phú Xuân, quận Phú Xuân).
   - Tiến trình lịch sử Đêm Hoàng cung từ Festival 2006 và sản phẩm Dạ yến Hoàng cung 2026: sự kiện 11/04/2026 tại Khôn Thái (600 khách); sự kiện 29/04 và 01/05/2026 tại Duyệt Thị Đường (130 khách/đêm); địa giới Đại Nội (phường Phú Xuân, quận Phú Xuân).
   - Lễ hội Di sản và Âm nhạc Quốc tế Huế Wonderverse Music Fest 2026: họp báo ngày 23/07/2026, tổ chức từ 30/08 đến 01/09/2026 tại Quảng trường Văn hóa - Thể thao (số 01 Hà Huy Tập, phường Vỹ Dạ, quận Thuận Hóa); dàn nghệ sĩ Mỹ Tâm, HIEUTHUHAI, MONO, Phương Mỹ Chi, Hoaprox; linh vật Long Mã 3D; đơn vị Beyond Communication & Huda.
   - Show diễn Huế by Light – The Live Show tối 12/12/2023 tại Ngọ Môn: sự kiện 1 kỳ 50 phút kỷ niệm 50 năm quan hệ Việt - Pháp; Sébastien Tellier và Limebócx (Trang Lê, Hà Đăng Tùng); công nghệ 3D mapping AC3 Studio 300.000 lumens; âm thanh vòm spatial sound.

## 4. Kết quả quan sát

| Tệp thực thể | Đánh giá Markdown Clean | Ranh giới thực thể | Xác thực sự thật | Kết luận thẩm định |
|:---|:---:|:---:|:---:|:---:|
| `Mega Booming – Huế.md` | ĐẠT 100% | ĐẠT 100% | ĐẠT 100% | **PASS 100% (Lưu ý 1 Minor m4)** |
| `Đêm Hoàng cung – Dạ yến Hoàng cung.md` | ĐẠT 100% | ĐẠT 100% | ĐẠT 100% | **PASS 100% (Không có lỗi)** |
| `Huế Wonderverse Music Fest.md` | Thiếu Thông tin chung | ĐẠT 100% | Cần sửa địa chỉ | **Changes Requested (M1, M2, m2, m3)** |
| `Huế by Light – The Live Show.md` | Dò rỉ từ khóa RAG | ĐẠT 100% | Sai tên nghệ sĩ | **Changes Requested (M3, M4, m1, m2)** |

## 5. Giới hạn hoặc phần chưa chạy

- Batch 03 là đợt review cuối cùng trong toàn bộ 11 thực thể của domain `performing_arts`. 
- Sau khi Implementer hoàn tất gói hiệu chỉnh Batch 03, Reviewer sẽ thực hiện re-review và tổng kết toàn diện toàn bộ phân hệ `performing_arts` để bàn giao cho người dùng.

## 6. Decision và bước tiếp theo

- **Technical Decision:** `changes_requested` (Yêu cầu hiệu chỉnh tập trung đối với 2 tệp: `Huế Wonderverse Music Fest.md` và `Huế by Light – The Live Show.md`; 2 tệp `Mega Booming – Huế.md` và `Đêm Hoàng cung – Dạ yến Hoàng cung.md` đã hoàn thành xuất sắc).
- **Bước tiếp theo:** Người dùng chuyển tiếp báo cáo review này đến Implementer để tiến hành cập nhật theo tiêu chí đóng chi tiết trên.
