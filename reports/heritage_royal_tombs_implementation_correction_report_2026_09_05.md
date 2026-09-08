# Implementation Report: Heritage Royal Tombs Correction (Entities 10–17)

Implementer: Implementer  
Date: 2026-09-05  
Canonical guide: `knowledge-base-hue/meta/heritage-template.md`, `knowledge-base-hue/heritage/heritage-entities-inventory.md`  
Review report căn cứ: `reports/heritage_royal_tombs_codex_review_2026_09_05.md`  

## 1. Phạm vi

Thực hiện hiệu chỉnh triệt để trong một batch toàn bộ các phát hiện Blocker (02) và Major (07) cùng các khuyến nghị Minor trên nhóm Lăng tẩm hoàng gia triều Nguyễn (thực thể 10 đến 17), đồng thời cập nhật đồng bộ các nội dung đính chính vào `knowledge-base-hue/meta/heritage-research-evidence.md` theo đúng chỉ đạo tại `session_prompt/CURRENT_HANDOFF.md`.

Các tệp thuộc phạm vi:
- `knowledge-base-hue/heritage/10 Lăng Gia Long.md`
- `knowledge-base-hue/heritage/11 Lăng Minh Mạng.md`
- `knowledge-base-hue/heritage/15 Lăng Đồng Khánh.md`
- `knowledge-base-hue/heritage/16 Lăng Khải Định.md`
- `knowledge-base-hue/heritage/14 Lăng Dục Đức.md` (Minor)
- `knowledge-base-hue/heritage/17 Lăng vua Hiệp Hòa.md` (Minor)
- `knowledge-base-hue/meta/heritage-research-evidence.md` (Mục 10, 11, 15, 16)

Ranh giới tuân thủ:
- Giữ nguyên các tệp corpus ngoài phạm vi (`12 Lăng Thiệu Trị.md`, `13 Lăng Tự Đức.md` và các di sản 1–9, 18–28).
- Không can thiệp runtime/backend/Qdrant/benchmark.
- Bảo toàn delta `Lễ hội Áo dài Huế.md` và các tệp untracked khác trong repository.
- Tuân thủ nghiêm ngặt chuẩn Markdown RAG Clean: bắt đầu bằng H1 `#`, không YAML frontmatter, không mục `## Nguồn dữ liệu`, không thuật ngữ nội bộ RAG, không giá vé cụ thể hay thời lượng tham quan ước tính chủ quan.
- Bảo toàn 100% cập nhật địa giới hành chính năm 2026 (phường Kim Long, Thủy Xuân, An Cựu).

## 2. Thay đổi chính

### 2.1. Tệp `knowledge-base-hue/heritage/10 Lăng Gia Long.md`
- **[GL-BLK-01] & [GL-MAJ-01] (Lăng tiền nhân):** Đính chính lăng Trường Phong là nơi an nghỉ của chúa Ninh Vương Nguyễn Phúc Chú (vị chúa Nguyễn thứ 7); làm rõ thân phụ vua Gia Long là Hưng Tổ Hiếu Khang Hoàng đế Nguyễn Phúc Luân (an táng tại Lăng Cơ Thánh ở làng Cư Chánh); đính chính chủ nhân Lăng Quang Hưng là Thái Tông Hiếu Triết Hoàng hậu Tống Thị Đôi (vợ thứ hai chúa Hiền; lăng chúa Hiền là Trường Hưng) và Lăng Vĩnh Mậu là Anh Tông Hiếu Nghĩa Hoàng hậu Tống Thị Lãnh (vợ chúa Nghĩa; lăng chúa Nghĩa là Trường Mậu).
- **[GL-BLK-02] (Lăng Thoại Thánh):** Đính chính thân mẫu vua Gia Long là Hoàng thái hậu Nguyễn Thị Hoàn (Hiếu Khang Hoàng hậu, 1736–1811), loại bỏ nhầm lẫn với bà Nguyễn Thị Mai (Triệu Tổ Tĩnh Hoàng hậu).
- **[GL-MAJ-02] (Đồi trung tâm):** Sửa tên đồi đặt Bửu thành từ "Cẩm Thi Sơn" thành "Chánh Trung Sơn" (cùng với Thanh Sơn bên trái và Bạch Sơn bên phải).
- **[GL-MAJ-03] (Phương vị mộ song táng):** Đính chính góc quan sát thực tế từ sân bái đình nhìn vào Bửu thành: mộ vua Gia Long nằm ở bên phải (ứng với Càn), mộ Thừa Thiên Cao Hoàng hậu nằm ở bên trái (ứng với Khôn), tuân thủ nguyên tắc phong thủy "nam tả nữ hữu" tính từ trong lăng nhìn ra ngoài.
- **Minor:** Chuẩn hóa ngày mất của vua Gia Long theo âm lịch: Ngày 19 tháng Chạp năm Kỷ Mão (tức ngày 03 tháng 02 năm 1820).

### 2.2. Tệp `knowledge-base-hue/heritage/11 Lăng Minh Mạng.md`
- **[MM-MAJ-01] (Phân định an táng và phụng thờ):** Tách bạch rõ rệt mục *Nhân vật an táng* (chỉ an táng duy nhất Thánh Tổ Chương Hoàng đế Minh Mạng tại Bửu thành đồi Khai Trạch Sơn) và *Nhân vật phụng thờ* (vua Minh Mạng và phối thờ bài vị Tá Thiên Nhân Hoàng hậu Hồ Thị Hoa tại Điện Sùng Ân; làm rõ mộ phần của bà an táng riêng tại Hiếu Đông Lăng thuộc làng Cư Chánh).
- **[MM-MAJ-02] (Ngói lợp Đại Hồng Môn):** Đính chính từ "ngói lưu ly đỏ" thành "ngói hoàng lưu ly" (men vàng hoàng gia, quy cách 24 mái).
- **Minor:** Lược bỏ ước tính thời lượng tham quan 1,5–2 giờ tại mục thông tin du khách, thay bằng mô tả khách quan về không gian trục Thần đạo.

### 2.3. Tệp `knowledge-base-hue/heritage/15 Lăng Đồng Khánh.md`
- **[ĐK-MAJ-01] (Quyết định di tích):** Sửa số hiệu văn bản Di tích quốc gia đặc biệt thành **Quyết định số 1272/QĐ-TTg ngày 12/8/2009 của Thủ tướng Chính phủ** (đợt đầu).
- **[ĐK-MAJ-02] (Mã UNESCO):** Đính chính mã thành phần chuẩn của Lăng Đồng Khánh theo danh mục UNESCO Serial ID 678 là **`678-008`** (thay cho mã 678-006 vốn là Đàn Nam Giao).
- **[ĐK-MAJ-03] (Cấu trúc nhân vật):** Tách rõ mục *Hoàng đế an táng và phụng thờ: Cảnh Tông Thuần Hoàng đế Đồng Khánh* (phối thờ Thánh Cung và Tiên Cung Hoàng hậu) với mục *Nhân vật lịch sử liên quan: Kiên Thái Vương Nguyễn Phúc Hồng Cai* (thân phụ, lăng mộ kề bên ngoài) và *Hoàng đế Khải Định* (con trưởng, chủ trì đại kiến thiết 1916–1923, an táng tại Lăng Khải Định).
- **Minor:** Bổ sung chú thích tên đường Đoàn Nhữ Hải (tức danh nhân Đoàn Nhữ Hài).

### 2.4. Tệp `knowledge-base-hue/heritage/16 Lăng Khải Định.md`
- **[KĐ-MAJ-01] (Quyết định di tích):** Sửa số hiệu văn bản Di tích quốc gia đặc biệt thành **Quyết định số 1272/QĐ-TTg ngày 12/8/2009 của Thủ tướng Chính phủ**.
- **[KĐ-MAJ-02] (Mã UNESCO):** Đính chính mã thành phần chuẩn của Lăng Khải Định theo danh mục UNESCO Serial ID 678 là **`678-011`** (thay cho mã 678-007 vốn là Lăng Tự Đức).
- **Minor:** Tiết chế các từ ngữ ca ngợi cảm tính ("đỉnh cao tuyệt mỹ", "như một thế giới thần tiên") sang miêu tả khách quan, trung tính.

### 2.5. Hoàn thiện các góp ý Minor tại Tệp 14 và 17
- `14 Lăng Dục Đức.md`: Giảm nhẹ từ ngữ tuyệt đối hóa thành "Điểm đặc biệt nổi bật"; lược bỏ từ "bán vé" ("mở cửa đón khách tham quan"); lược bỏ câu khuyến nghị thời lượng tham quan 45 phút - 1 giờ.
- `17 Lăng vua Hiệp Hòa.md`: Chỉnh "không thu vé tham quan" thành "không gian tưởng niệm tâm linh mở cửa tự do đón khách viếng thăm và dâng hương".

### 2.6. Đồng bộ `knowledge-base-hue/meta/heritage-research-evidence.md`
- Cập nhật Mục 10 (Lăng Gia Long), Mục 11 (Lăng Minh Mạng), Mục 15 (Lăng Đồng Khánh), Mục 16 (Lăng Khải Định) với `### Nhật ký hiệu chỉnh sau review độc lập (05/09/2026)` ghi nhận đầy đủ chi tiết các căn cứ đính chính và mốc kiểm chứng ngày 05/09/2026.

## 3. Cách đã chạy thật

1. **Kiểm tra worktree và Git status:**
   - Lệnh: `git status --short`
   - Kết quả: Không có tệp ngoài ý muốn bị sửa đổi, bảo toàn delta Áo dài và các tệp untracked.
2. **Kiểm tra định dạng và khoảng trắng:**
   - Lệnh: `git diff --check`
   - Kết quả: Exit code 0, không có lỗi whitespace hay định dạng.
3. **Kiểm tra tiêu chuẩn Markdown RAG Clean:**
   - Kiểm tra H1: 100% tệp bắt đầu bằng `# <Tên Lăng>`.
   - Kiểm tra `## Nguồn dữ liệu`: Không có tệp corpus nào chứa đề mục này (`grep_search` trả về rỗng trong các file entity).
   - Kiểm tra YAML frontmatter: Không có tệp nào chứa frontmatter `---` ở đầu tệp.
   - Kiểm tra thuật ngữ cấm: Không chứa `canonical`, `chunk`, `metadata`, `repository`, đường dẫn tệp nội bộ.

## 4. Kết quả quan sát

| Mã Finding | Mức độ | Tệp | Nội dung hiệu chỉnh | Trạng thái |
|---|---|---|---|---|
| **GL-BLK-01** | Blocker | `10 Lăng Gia Long.md` | Thân phụ vua Gia Long là Nguyễn Phúc Luân (Lăng Cơ Thánh); Lăng Trường Phong là của chúa Ninh Vương Nguyễn Phúc Chú | **Đã sửa triệt để** |
| **GL-BLK-02** | Blocker | `10 Lăng Gia Long.md` | Thân mẫu vua Gia Long tại Lăng Thoại Thánh là Hoàng thái hậu Nguyễn Thị Hoàn | **Đã sửa triệt để** |
| **GL-MAJ-01** | Major | `10 Lăng Gia Long.md` | Lăng Quang Hưng thờ Tống Thị Đôi, Lăng Vĩnh Mậu thờ Tống Thị Lãnh | **Đã sửa triệt để** |
| **GL-MAJ-02** | Major | `10 Lăng Gia Long.md` | Sửa tên đồi đặt Bửu thành thành đồi Chánh Trung Sơn | **Đã sửa triệt để** |
| **GL-MAJ-03** | Major | `10 Lăng Gia Long.md` | Phương vị từ bái đình nhìn vào: Mộ vua bên phải, mộ hoàng hậu bên trái | **Đã sửa triệt để** |
| **MM-MAJ-01** | Major | `11 Lăng Minh Mạng.md` | Tách riêng mục an táng (vua Minh Mạng) và phụng thờ (phối thờ Tá Thiên Nhân Hoàng hậu, mộ bà tại Hiếu Đông Lăng) | **Đã sửa triệt để** |
| **MM-MAJ-02** | Major | `11 Lăng Minh Mạng.md` | Sửa ngói lưu ly đỏ thành ngói hoàng lưu ly tại Đại Hồng Môn | **Đã sửa triệt để** |
| **ĐK-MAJ-01** | Major | `15 Lăng Đồng Khánh.md` | Sửa Quyết định Di tích quốc gia đặc biệt thành Quyết định số 1272/QĐ-TTg ngày 12/8/2009 | **Đã sửa triệt để** |
| **ĐK-MAJ-02** | Major | `15 Lăng Đồng Khánh.md` | Sửa mã thành phần UNESCO thành `678-008` | **Đã sửa triệt để** |
| **ĐK-MAJ-03** | Major | `15 Lăng Đồng Khánh.md` | Tách bạch vua Đồng Khánh (an táng & phụng thờ) với Kiên Thái Vương và vua Khải Định (nhân vật liên quan) | **Đã sửa triệt để** |
| **KĐ-MAJ-01** | Major | `16 Lăng Khải Định.md` | Sửa Quyết định Di tích quốc gia đặc biệt thành Quyết định số 1272/QĐ-TTg ngày 12/8/2009 | **Đã sửa triệt để** |
| **KĐ-MAJ-02** | Major | `16 Lăng Khải Định.md` | Sửa mã thành phần UNESCO thành `678-011` | **Đã sửa triệt để** |
| **Minor (GL, MM, ĐK, KĐ, DĐ, HH)** | Minor | 6 tệp | Đã xử lý toàn bộ: ngày âm lịch vua Gia Long, bỏ giờ tham quan, chỉnh tên đường Đoàn Nhữ Hài, tiết chế từ ngữ ca ngợi cảm tính, bỏ chữ "bán vé" | **Đã hoàn tất** |
| **Đồng bộ Evidence** | Major | `heritage-research-evidence.md` | Cập nhật nhật ký hiệu chỉnh ngày 05/09/2026 cho cả 4 Mục 10, 11, 15, 16 | **Đã hoàn tất** |

## 5. Lỗi và giới hạn

Không có lỗi hoặc giới hạn đã biết trong phạm vi này. Toàn bộ các phát hiện Blocker và Major đã được hiệu chỉnh hoàn tất, các khuyến nghị Minor được tinh chỉnh tối ưu và đồng bộ với khuôn mẫu di sản.

## 6. Handoff cho Reviewer

Reviewer có thể kiểm tra:
1. Đọc trực tiếp các diff tại `knowledge-base-hue/heritage/10 Lăng Gia Long.md`, `11 Lăng Minh Mạng.md`, `15 Lăng Đồng Khánh.md`, `16 Lăng Khải Định.md`, `14 Lăng Dục Đức.md`, `17 Lăng vua Hiệp Hòa.md`.
2. Kiểm tra phần `### Nhật ký hiệu chỉnh sau review độc lập (05/09/2026)` tại các Mục 10, 11, 15, 16 của `knowledge-base-hue/meta/heritage-research-evidence.md`.
3. Kiểm tra tính tuân thủ quy chuẩn Markdown RAG Clean và việc bảo toàn các cập nhật địa giới hành chính năm 2026.
