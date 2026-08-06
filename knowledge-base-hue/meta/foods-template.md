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
- `local_specialties/*.md`: entity món ăn hoặc đặc sản Huế.
- `food-guides.md`: guide được tổ chức theo nhu cầu của du khách.

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
- Thông tin nguồn tối giản nằm trong section Markdown ở cuối file.
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

Các file `local_specialties` chỉ nên tổng hợp những gì có trong mô tả raw của
các địa điểm liên quan hoặc nội dung đã được người dùng cập nhật thủ công. Phần
giải thích ẩm thực độc lập cần được enrich sau bằng nguồn đã xác minh nếu chưa
có dữ liệu đáng tin.


```md
# <Tên món>

## Tóm tắt

<Tổng hợp ngắn từ các mô tả raw liên quan.>

## Đặc điểm món ăn

<Tổng hợp đặc điểm món ăn từ dữ liệu có nguồn. Nếu chưa đủ thông tin thì bỏ section này hoặc dừng lại hỏi người dùng, không tự bịa.>

## Địa điểm tiêu biểu từ dữ liệu gốc

<Chỉ tạo section này khi có dữ liệu địa điểm tiêu biểu.>

| Địa điểm | Địa chỉ | Giá tham khảo | Ghi chú | File liên quan |
|---|---|---:|---|---|
| <Tên địa điểm> | <Địa chỉ> | <Khoảng giá nếu có> | <Ghi chú ngắn từ raw> | `foods/restaurants/<slug>.md` |

## Ghi chú về giá

<Chỉ tạo section này khi cần làm rõ raw cung cấp giá theo địa điểm hay theo món. Không tự suy giá.>

## Nguồn dữ liệu

- Nguồn chính:
- Ngày cập nhật nội dung:
```

## Body Cho Food Guide

```md
# Food Guides Huế

## Lần đầu đến Huế nên thử gì?

## Gợi ý ăn sáng

## Gợi ý món chay

## Gợi ý món ngọt

## Gợi ý đi chợ và ăn vặt

## Theo ngân sách

## Nguồn dữ liệu

- Nguồn chính:
- Ngày cập nhật nội dung:
```

`food-guides.md` nên tóm tắt và điều hướng người dùng tới các món/địa điểm liên
quan. Không duplicate mô tả dài từ file địa điểm hoặc file đặc sản.

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
