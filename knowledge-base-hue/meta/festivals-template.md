# Hướng Dẫn & Khuôn Mẫu Biên Soạn Lễ Hội Xứ Huế (Festivals Knowledge Base)

Tài liệu này định nghĩa nguyên tắc biên soạn, chuẩn mực văn phong và khung cấu trúc gợi ý cho 25 entity lễ hội thuộc `knowledge-base-hue/festivals/`.

---

## 1. Triết Lý & Nguyên Tắc Biên Soạn

Mục tiêu của các file trong thư mục này là tạo ra **văn bản tri thức tự nhiên, chuẩn xác và sạch cho hệ thống RAG**, đóng vai trò nguồn tri thức tin cậy để trả lời câu hỏi của người dùng. File phải đọc như một bài viết thông tin hoàn chỉnh dành cho con người, không mang hình thức một bảng dữ liệu kỹ thuật hay schema database.

```text
Accuracy (Chính xác)
   ↓
Clear entity boundaries (Ranh giới rõ ràng)
   ↓
Stable knowledge (Tri thức bền vững)
   ↓
Sufficient detail (Đầy đủ theo nguồn)
   ↓
Natural Vietnamese (Tiếng Việt tự nhiên)
   ↓
Clear Markdown structure (Cấu trúc Markdown mạch lạc)
   ↓
Future chunking/retrieval (Sẵn sàng cho RAG)
```

### 1.1. Đầy Đủ Theo Nguồn, Không Đầy Đủ Theo Template
- Mức độ đầy đủ của file được đánh giá theo **lượng thông tin đáng tin cậy hiện có về lễ hội**, không theo số lượng section đã điền.
- Một file ngắn nhưng chỉ chứa thông tin đã kiểm chứng tốt hơn một file dài có nhiều nội dung suy đoán hoặc lặp lại.
- Ngược lại, nếu có nhiều nguồn đáng tin cậy và lễ hội có lịch sử, nghi lễ hoặc hoạt động phức tạp, file có thể dài và chi tiết mà không cần cố rút ngắn.

### 1.2. Tách Biệt Tri Thức Bền Vững và Dữ Liệu Biến Động Theo Năm
- **Tri thức bền vững (Đưa vào file):** Nguồn gốc lịch sử, ý nghĩa văn hóa, quy luật chu kỳ (theo âm lịch, mùa vụ), địa điểm/không gian, các nghi lễ và hoạt động đặc trưng của lễ hội. Áp dụng quy tắc kiểm chứng: *"Sau 3–5 năm nữa, thông tin này có còn đúng không?"*.
- **Dữ liệu biến động theo từng năm (Khái quát hóa):** Ngày diễn ra cụ thể theo năm dương lịch (ví dụ: ngày 13–18/6/2026), số lượng chương trình của một kỳ nhất định, chủ đề riêng của từng năm. Cần diễn đạt theo quy luật chung (ví dụ: *"thường diễn ra vào tháng 4 đến tháng 6; thời gian chi tiết được công bố theo từng năm"*), tránh biến lịch của một năm cụ thể thành thuộc tính vĩnh viễn của lễ hội.

### 1.3. Không Lấy Chương Trình Một Năm Làm Đặc Trưng Cố Định
- Không suy ra hoạt động cố định của lễ hội chỉ từ chương trình của một kỳ tổ chức cụ thể.
- Một hoạt động chỉ được mô tả là đặc trưng/thường lệ nếu có nguồn cho thấy nó được duy trì qua nhiều kỳ hoặc thuộc nghi thức truyền thống.
- Nếu hoạt động chỉ xuất hiện trong một kỳ cụ thể, dùng cách diễn đạt như *"đã từng được tổ chức"*, *"trong một số kỳ"* hoặc bỏ nếu không quan trọng.

### 1.4. Xử Lý Thông Tin Không Thống Nhất Giữa Các Nguồn
- Khi nhiều nguồn cung cấp thông tin khác nhau về cùng một dữ kiện, **không tự suy đoán để hợp nhất**.
- Ưu tiên nguồn chính thức của cơ quan quản lý, bảo tồn di tích, cơ quan báo chí uy tín hoặc tài liệu nghiên cứu có căn cứ rõ ràng.
- Nếu chưa thể xác định thông tin nào đáng tin cậy hơn, sử dụng cách diễn đạt thận trọng (ví dụ: *"theo một số nguồn..."*) hoặc không đưa dữ kiện chưa chắc chắn đó vào file.

### 1.5. Phân Biệt Dữ Kiện Lịch Sử, Truyền Thuyết và Nhận Định
- Phân biệt rõ mức độ xác thực của nguồn tin:
  - **Dữ kiện lịch sử:** *"Theo tư liệu lịch sử ghi nhận...", "Năm 2000, sự kiện..."*
  - **Truyền thuyết / Ký ức dân gian:** *"Theo truyền thuyết dân gian tại địa phương...", "Tương truyền rằng..."*
  - **Diễn giải hiện đại:** *"Trong đời sống đương đại, hoạt động này thường được hiểu là..."*
- Không trình bày truyền thuyết hoặc giai thoại dân gian như một sự kiện lịch sử đã được kiểm chứng.

### 1.6. Tránh Suy Diễn Quan Hệ Nhân Quả
- Không tự kết nối các dữ kiện rời rạc từ các nguồn khác nhau thành quan hệ nguyên nhân – kết quả nếu tài liệu gốc không trực tiếp khẳng định.

### 1.7. Hạn Chế Trùng Lặp Thông Tin Giữa Các Entity
- Với các sự kiện tổng hợp lớn (như Festival Huế), các lễ hội thành viên đã có file entity độc lập (như Lễ hội Điện Huệ Nam, Hội vật làng Sình, Ngày hội Sen...) chỉ được nhắc đến như **ví dụ tiêu biểu kết nối trong chương trình**, không đi sâu vào chi tiết tổ chức để tránh xung đột dữ liệu khi tìm kiếm.

### 1.8. Không Săn Số Liệu Từng Kỳ & Tách Riêng Giá Vé
- Không ưu tiên số liệu thống kê theo từng kỳ tổ chức (như số lượng đoàn, số lượng khách từng năm) nếu số liệu đó không cần thiết để giải thích bản chất hay lịch sử của lễ hội (trừ mốc lịch sử quan trọng như kỳ đầu tiên).
- **Giá vé cụ thể không đưa vào festivals file** (thông tin vé biến động và được quản lý tập trung ở domain `tickets/`). Trong file lễ hội, chỉ cần ghi nhận ở mức: *"Một số chương trình hoặc khu vực di tích có thể áp dụng quy định vé riêng"*.
- Không đưa các thông tin dễ stale như link website, tên fanpage, kênh cập nhật vào template mặc định.

### 1.9. Độc Lập Ngữ Cảnh Tự Nhiên (Local Completeness)
- Mỗi section hoặc tiểu mục quan trọng cần đủ ngữ cảnh để có thể hiểu tương đối độc lập khi trích xuất chunk.
- Khi cần, nhắc lại tên lễ hội một cách tự nhiên, đặc biệt ở câu mở đầu của các phần có khả năng được tách riêng; không bắt buộc lặp tên lễ hội máy móc trong mọi đoạn.
- Hạn chế mở đầu đoạn bằng đại từ mơ hồ (*"Sự kiện này...", "Nơi đây...", "Đây là..."*) nếu danh từ gốc ở quá xa.

### 1.10. Văn Phong Tri Thức: Tự Nhiên, Khách Quan, Dễ Đọc
- **Ưu tiên:** Tiếng Việt hiện đại, rõ ràng, câu ngắn đến trung bình, mô tả trực tiếp sự việc.
- **Tránh:**
  - Văn phong quảng bá, mỹ từ cảm tính (*"rực rỡ sắc màu", "độc bản", "tuyệt phẩm", "then chốt", "công phu", "lãng mạn", "vô cùng phong phú"*).
  - Văn phong hành chính quá nặng nề hoặc sáo rỗng.
  - Từ định lượng ước lệ thiếu căn cứ (*"hàng chục", "hàng triệu", "hàng vạn"*).

### 1.11. Địa Giới Hành Chính Hiện Hành
- Ưu tiên tên địa danh và đơn vị hành chính hiện hành tại thời điểm biên soạn (**thành phố Huế**).
- Trong các đoạn mô tả lịch sử trước năm 2025, giữ nguyên tên hành chính đúng với thời kỳ lịch sử đó (ví dụ: *tỉnh Thừa Thiên Huế* khi nhắc về sự kiện năm 2000).

### 1.12. Định Dạng Markdown Sạch
- Bắt đầu trực tiếp bằng tiêu đề `# <Tên lễ hội>`.
- Không sử dụng YAML frontmatter (`--- ... ---` ở đầu file).
- Không để placeholder hoặc câu ghi chú thiếu dữ liệu (*"chưa có thông tin", "không có dữ liệu"*).
- Không đưa các thuật ngữ kỹ thuật nội bộ (*canonical, alias, year-specific, chunk, metadata*) hoặc section nguồn tham khảo vào file nội dung.

---

## 2. Khung Cấu Trúc Gợi Ý

> **Lưu ý:** Các section dưới đây là **khung tham khảo, không phải danh sách bắt buộc**. Số lượng và cách tổ chức section phải dựa trên lượng thông tin đáng tin cậy thu thập được, quy mô, đặc điểm và tính chất của từng lễ hội. Không tạo section chỉ để hoàn thành khuôn mẫu.

```markdown
# <Tên lễ hội>

## Thông tin chung

- **Tên lễ hội:** <Tên chính thức hoặc tên phổ biến nhất>
- **Tên gọi khác:** <Chỉ thêm khi thực sự tồn tại tên khác, nếu không có thì bỏ dòng này>
- **Loại hình:** <Mô tả ngắn loại hình lễ hội>
- **Thời gian tổ chức:** <Chu kỳ âm lịch, mùa trong năm hoặc thời điểm thường diễn ra>
- **Nơi tổ chức:** <Địa điểm, di tích hoặc khu vực chính>
- **Không nhầm với:** <Chỉ thêm khi có lễ hội/sự kiện dễ gây nhầm lẫn>

---

## Tổng quan

<2-3 đoạn văn ngắn giới thiệu súc tích bản chất, vị thế và bối cảnh của lễ hội bằng ngôn ngữ khách quan, tự nhiên.>

---

## Nguồn gốc và lịch sử

<Mô tả nguồn gốc ra đời, quá trình phát triển qua các thời kỳ và hoạt động duy trì/phục dựng. Các tiểu mục cấp 3 (###) là hoàn toàn tùy chọn, chỉ tạo khi cần phân kỳ thời gian rõ ràng.>

---

## Ý nghĩa và giá trị

<Trình bày ý nghĩa văn hóa, tín ngưỡng, tinh thần đoàn kết cộng đồng hoặc giá trị đối với đời sống văn hóa địa phương. Sử dụng văn xuôi hoặc danh sách ngắn gọn tùy nội dung.>

---

## Thời gian và chu kỳ tổ chức

<Mô tả quy luật tổ chức (hằng năm, định kỳ nhiều năm, thời điểm âm lịch hoặc mùa vụ). Nếu lịch thay đổi theo từng năm, nêu rõ thời gian cụ thể được công bố trước mỗi kỳ tổ chức.>

---

## Địa điểm và không gian tổ chức

<Mô tả các không gian chính diễn ra lễ hội: khu vực đền, đình, chùa, đàn tế, sông nước, bãi hội, đường phố hoặc các khu vực lân cận.>

---

## Hoạt động chính

<Mô tả các hoạt động tiêu biểu. Cấu trúc tiểu mục (###) thích ứng linh hoạt theo từng loại lễ hội:
- Lễ hội truyền thống: Phần lễ, Phần hội
- Lễ hội đương đại: Chương trình nghệ thuật, Hoạt động cộng đồng
- Lễ hội thượng võ: Nghi thức, Thể thức thi đấu, Hội hè
- Lễ hội sông nước: Lễ nghinh thần, Diễn xướng trên sông, Đua trải...>

---

## Những nét đặc trưng

<Trình bày 2-4 đặc điểm giúp nhận diện nét riêng của lễ hội hoặc phân biệt với các lễ hội liên quan (về nghi thức, đạo cụ, trang phục, diễn xướng, không gian di sản...).>

---

## Thông tin dành cho du khách

<Các tiểu mục dưới đây là tùy chọn, chỉ đưa vào các lưu ý thực sự có ích:>

### Thời điểm tham quan
<Khung thời gian hoặc thời điểm thích hợp để trải nghiệm không khí lễ hội.>

### Văn hóa ứng xử
<Yêu cầu trang phục lịch sự tại nơi tôn nghiêm, thái độ tôn trọng nghi lễ.>

### Lưu ý khi tham dự
<Lưu ý về không gian đông người, an toàn, hoặc việc một số khu vực di tích có thể áp dụng quy định riêng.>
```

---

## 3. Các Section Chuyên Biệt Tùy Chọn (Ngang Cấp `##`)

Nếu một chủ đề là thành phần quan trọng để hiểu rõ lễ hội và có đủ dữ liệu đáng tin cậy, người biên soạn **hoàn toàn có thể tạo thành section `##` riêng** thay vì cố nhét vào các section chuẩn.

Ví dụ:
- `## Thể thức và luật đấu vật` (Hội vật làng Sình, Hội vật làng Thủ Lễ).
- `## Tín ngưỡng thờ Cá Ông` (Lễ hội Cầu ngư Thai Dương Hạ).
- `## Đối tượng thờ phụng và thần tích` (Lễ hội Điện Huệ Nam, Lễ hội Đền Huyền Trân Công chúa).
- `## Nghi thức diễn xướng chèo cạn` (Lễ hội Cầu ngư).
