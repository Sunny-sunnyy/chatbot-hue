# Template Knowledge Base Cho Foods

Tài liệu này định nghĩa cấu trúc Markdown đã thống nhất cho các file curated
trong `knowledge-base-hue/foods`.

## Phạm vi

Folder `foods` dùng các file Markdown curated được tạo từ source dumps. Không
chunk trực tiếp từ `_source-dumps`.

Cấu trúc hiện tại:

```text
knowledge-base-hue/foods/
  restaurants/
  cafes/
  local_specialties/
  food-guides.md
```

Vai trò file:

- `restaurants/*.md`: entity địa điểm ăn uống.
- `cafes/*.md`: entity quán cà phê hoặc đồ uống.
- `local_specialties/*.md`: entity món ăn hoặc nhóm món đặc sản Huế.
- `food-guides.md`: guide tổng hợp được tổ chức theo nhu cầu của du khách.

Các file curated ban đầu chỉ được dùng dữ liệu raw/source dump hoặc nội dung đã
được người dùng cập nhật thủ công. Không gọi web, không enrich và không thêm
factual claim thiếu nguồn nếu người dùng chưa yêu cầu rõ.

## Nguyên tắc Markdown không frontmatter

Các file curated trong `foods` không dùng YAML frontmatter. File phải bắt đầu
trực tiếp bằng heading `#`.

Lý do:

- Tránh nhiễu dữ liệu khi chunk/embedding nội dung cho RAG.
- Tránh metadata cũ mâu thuẫn với nội dung đã được cập nhật trong body.
- Giữ file dễ đọc và dễ chỉnh thủ công.

Quy ước:

- Không đặt block `--- ... ---` ở đầu file curated.
- Không lưu metadata phục vụ pipeline dưới dạng YAML trong file nội dung.
- Thông tin nguồn tối giản nằm trong section Markdown ở cuối file, ngoại trừ
  `food-guides.md` là guide tổng hợp nên không bắt buộc có `## Nguồn dữ liệu`.
- Nếu sau này cần structured metadata cho recommender/filtering, tạo sidecar
  hoặc index riêng, ví dụ `.meta.yml`/`.json`, thay vì nhúng vào `.md`.
- Nội dung người dùng nhìn thấy và nội dung RAG đọc ưu tiên tiếng Việt có dấu.
- Không điền dữ liệu thiếu bằng giá trị suy đoán.
- Không ghi field hoặc section không có dữ liệu. Ví dụ: nếu không có liên hệ thì
  bỏ dòng `Liên hệ`; nếu không có menu thì bỏ section `Menu và giá tham khảo`.
- Không ghi các câu như `chưa có dữ liệu`, `không có thông tin`, hoặc ghi chú
  thiếu dữ liệu vào body curated, vì chatbot có thể hiểu nhầm đó là thông tin về
  entity.
- Nếu raw chỉ cung cấp khoảng giá chung theo địa điểm, không tự gán khoảng giá đó
  cho từng món; giải thích rõ trong body.

## Body Cho Restaurants Và Cafes

Các dòng trong section `Thông tin` chỉ ghi khi có dữ liệu. Tối thiểu nên có địa
chỉ nếu source cung cấp. `Menu và giá tham khảo` là section optional; chỉ tạo khi
có dữ liệu menu hoặc giá theo từng món.
Nếu có liên hệ hoặc website thì thêm dòng tương ứng trong section `Thông tin`;
không có thì bỏ hẳn.

```md
# <Tên quán>

## Tóm tắt

<Viết 2-4 câu ngắn từ dữ liệu gốc. Không thêm thông tin ngoài nguồn.>

## Thông tin

- Địa chỉ:
- Mức giá: Dao động từ giá thấp nhất đến giá cao nhất, ví dụ: Dao động từ 25.000 VNĐ – 50.000 VNĐ
- Giờ hoạt động: điền thông tin giờ mở cửa - đóng cửa, ví dụ: Khoảng 6:00 sáng – 10:00 sáng (thường hết sớm hơn).

## Món ăn / trải nghiệm

<Nếu có ảnh, đặt Markdown image ngay đầu section này. Không thêm caption nguồn ảnh vào body.>

- <Món ăn hoặc trải nghiệm được nhắc trong dữ liệu gốc>

## Nguồn dữ liệu

- Nguồn chính:
- Ngày cập nhật nội dung:
```

Optional section, chỉ dùng khi có dữ liệu menu hoặc giá theo từng món:

```md
## Menu và giá tham khảo

| Món | Giá thấp nhất | Giá cao nhất | Ghi chú | Nguồn |
|---|---:|---:|---|---|
| <Tên món> | <Giá thấp nhất nếu có> | <Giá cao nhất nếu có> | <Ghi chú ngắn nếu có> | <Nguồn> |
```

## Body Cho Local Specialties

Các file `local_specialties` đại diện cho món ăn hoặc nhóm món đặc sản Huế. Nội
dung có thể dùng dữ liệu research có nguồn do người dùng cung cấp, kết hợp với
dữ liệu quán đã curate trong `restaurants/` và `cafes/`. Không tự viết thêm
thành phần, cách làm, nguồn gốc hoặc claim lịch sử nếu nguồn không cung cấp.

Giai đoạn đầu ưu tiên 8 món hoặc nhóm món:

- Bún bò Huế
- Cơm hến / bún hến
- Cơm âm phủ
- Bánh Huế: bánh bèo, bánh nậm, bánh lọc
- Chè Huế / chè heo quay
- Bánh ép
- Mè xửng
- Bánh canh Huế: bánh canh Nam Phổ / bánh canh cá lóc


```md
# <Tên món>

## Tóm tắt

<Giới thiệu ngắn về món hoặc nhóm món từ dữ liệu có nguồn.>

## Thành phần và đặc điểm

<Tổng hợp thành phần và đặc điểm món ăn từ dữ liệu có nguồn. Nếu chưa đủ thông tin thì bỏ section này.>

## Cách làm tóm tắt

<Tóm tắt cách làm từ dữ liệu có nguồn. Không biến section này thành recipe chi tiết nếu source không đủ rõ.>

## Nguồn gốc và bối cảnh

<Chỉ tạo section này khi source cung cấp thông tin nguồn gốc hoặc bối cảnh văn hóa đáng tin cậy.>

## Địa điểm tiêu biểu

<Chỉ tạo section này khi có dữ liệu địa điểm tiêu biểu đã curate. Không đưa file path vào body.>

| Tên quán | Địa chỉ |
|---|---|
| <Tên quán> | <Địa chỉ> |

## Nguồn dữ liệu

- Nguồn chính:
- Ngày cập nhật nội dung:
```

## Body Cho Food Guide

`food-guides.md` là guide tổng hợp cho du khách, tập trung vào câu hỏi ăn gì,
ăn ở đâu, đi theo lịch trình nào và chọn theo nhu cầu nào. File này không phải
entity món ăn và không chứa mô tả dài về thành phần, cách làm hoặc nguồn gốc.
Các phần chi tiết đó nằm trong `local_specialties/*.md`.

`food-guides.md` là exception của chuẩn source tracking: không bắt buộc có
section `## Nguồn dữ liệu`, vì nội dung guide được tổng hợp từ các file curated
khác trong `foods`.

```md
# Food Guides Huế

## Lần đầu đến Huế nên thử gì?

## Gợi ý ăn sáng

## Gợi ý ăn trưa

## Gợi ý ăn chiều và ăn vặt

## Gợi ý ăn tối

## Cà phê và đồ uống

## Gợi ý món chay

## Gợi ý món ngọt

## Theo ngân sách

## Gợi ý theo nhóm người dùng

## Food tour nửa ngày

## Food tour 1 ngày

## Food tour 2 ngày

## Food tour 3 ngày
```

Trong `food-guides.md`, mỗi món chỉ diễn giải rất ngắn để phục vụ ngữ cảnh du
lịch. Gợi ý địa điểm dùng tên quán và địa chỉ ngắn, không duplicate mô tả dài
từ file địa điểm hoặc file đặc sản.

## Tiêu chí chọn dữ liệu ban đầu

Curate 20-50 địa điểm ăn uống trước. Ưu tiên record có:

- Mô tả raw hữu ích.
- Địa chỉ.
- Giá, giờ mở cửa hoặc tọa độ khi có.
- Tính đại diện cho nhiều nhu cầu và nhóm món:
  - bún bò
  - bánh Huế
  - chè Huế
  - cơm hến / bún hến
  - món chay
  - chợ / ăn vặt
  - cà phê hoặc đồ uống khi có
- Tránh quá nhiều record trùng cùng một địa điểm/món.

## Ghi chú thiết kế retrieval

Curated `.md` ưu tiên nội dung sạch cho RAG:

- Không thêm section `Liên kết nội bộ` vào body.
- Không duplicate mô tả dài giữa file địa điểm, file món và file guide.
- Nếu sau này cần graph/cross-reference cho recommender hoặc agentic retrieval,
  tạo sidecar/index riêng thay vì nhúng vào nội dung `.md`.
