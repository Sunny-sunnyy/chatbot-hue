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

Các file curated ban đầu chỉ được dùng dữ liệu raw/source dump. Không gọi web,
không enrich và không thêm factual claim thiếu nguồn.

## Core Frontmatter

Mọi file trong `foods` phải có các field sau:

```yaml
---
title: ""
description: ""
slug: ""
entity_type: ""
category: "foods"
sub_category: ""
language: "vi"
source_name: "data.hue.gov.vn"
source_group: ""
source_file: ""
source_record_id: ""
source_record_index: ""
status: "draft"
enrichment_status: "needs_enrichment"
generated_at: ""
tags: []
---
```

Quy ước:

- YAML keys dùng English `snake_case`.
- Giá trị text trong YAML và body Markdown dùng tiếng Việt có dấu.
- Optional fields nên được bỏ qua khi không có dữ liệu.
- Không điền dữ liệu thiếu bằng giá trị suy đoán.
- `source_record_id` dùng raw `id` khi có.
- `source_record_index` dùng raw `sttbanghi` hoặc record number trong source dump.
- `status` là trạng thái biên tập.
- `enrichment_status` là trạng thái freshness/verification.

Các optional field chung nên dùng khi có dữ liệu:

```yaml
aliases: []
keywords: []
related_food_topics: []
related_places: []
price_note: ""
```

## Frontmatter Cho Restaurants Và Cafes

Dùng cho `restaurants/*.md` và `cafes/*.md`.

```yaml
address: ""
ward: ""
district: ""
city: "Huế"
latitude:
longitude:
price_min_vnd:
price_max_vnd:
opening_hours: ""
closing_hours: ""
phone: ""
email: ""
website: ""
signature_dishes: []
menu_items:
  - name: ""
    price_min_vnd:
    price_max_vnd:
    source: ""
meal_times: []
dietary_tags: []
related_food_topics: []
price_note: ""
```

`menu_items` trong frontmatter dùng cho retrieval/filtering có cấu trúc ở mức
ngắn. Menu chi tiết và ghi chú giá nằm trong body Markdown.

Nếu raw chỉ cung cấp khoảng giá chung theo địa điểm, không tự gán khoảng giá đó
cho từng món. Dùng `price_note` và giải thích rõ trong body.

## Body Cho Restaurants Và Cafes

```md
# <Tên quán>

## Tóm tắt

<Viết 2-4 câu ngắn từ dữ liệu gốc. Không thêm thông tin ngoài nguồn.>

## Thông tin địa điểm

- Địa chỉ:
- Khu vực:
- Tọa độ:
- Giá thấp nhất:
- Giá cao nhất:
- Giờ mở cửa:
- Giờ đóng cửa:
- Liên hệ:
- Website:

## Món / trải nghiệm nổi bật

- <Món hoặc trải nghiệm được nhắc trong dữ liệu gốc>

## Menu và giá tham khảo

| Món | Giá thấp nhất | Giá cao nhất | Ghi chú | Nguồn |
|---|---:|---:|---|---|
| <Tên món> | Chưa có dữ liệu | Chưa có dữ liệu | Món được nhắc trong mô tả gốc. | Raw huegov |

## Thông tin từ dữ liệu gốc

- Tên trong raw:
- Mô tả raw:
- Giá tham khảo từ:
- Giá tham khảo đến:
- Mở cửa:
- Đóng cửa:
- Số điện thoại:
- Email:
- Website:
- Source record:

## Cần kiểm chứng / bổ sung

- Tình trạng còn hoạt động.
- Giờ mở cửa hiện tại.
- Giá hiện tại.
- Menu hiện tại.
- Giá từng món.
- Số điện thoại.
- Nguồn xác minh.

## Liên kết nội bộ

- Món liên quan:
- Guide liên quan:
```

## Frontmatter Cho Local Specialties

Dùng cho `local_specialties/*.md`.

```yaml
dish_type: ""
main_ingredients: []
flavor_profile: []
meal_times: []
related_places: []
price_note: ""
```

Các file `local_specialties` chỉ nên tổng hợp những gì có thể suy ra từ mô tả
raw của các địa điểm liên quan. Phần giải thích ẩm thực độc lập cần được enrich
sau bằng nguồn đã xác minh.

## Body Cho Local Specialties

```md
# <Tên món>

## Tóm tắt

<Tổng hợp ngắn từ các mô tả raw liên quan.>

## Đặc điểm món ăn

- Loại món:
- Nguyên liệu chính:
- Hương vị:
- Thời điểm thường ăn:
- Phù hợp với:

## Thông tin từ dữ liệu gốc

<Liệt kê các record/mô tả raw liên quan đến món.>

## Địa điểm tiêu biểu từ dữ liệu gốc

| Địa điểm | Địa chỉ | Giá tham khảo | Ghi chú | File liên quan |
|---|---|---:|---|---|
| <Tên địa điểm> | <Địa chỉ> | <Khoảng giá nếu có> | <Ghi chú ngắn từ raw> | `foods/restaurants/<slug>.md` |

## Ghi chú về giá

<Nêu rõ raw cung cấp giá theo địa điểm hay theo món. Không tự suy giá.>

## Cần kiểm chứng / bổ sung

- Nguồn mô tả món ăn độc lập.
- Danh sách quán còn hoạt động.
- Giá hiện tại.
- Địa chỉ hiện tại.
- Giờ mở cửa hiện tại.

## Liên kết nội bộ

- Quán liên quan:
- Guide liên quan:
```

## Frontmatter Cho Food Guide

Dùng cho `food-guides.md`.

```yaml
guide_type: "theo nhu cầu người dùng"
target_audience: []
related_food_topics: []
related_places: []
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

## Cần kiểm chứng / bổ sung

- Giờ mở cửa hiện tại của các địa điểm.
- Giá hiện tại.
- Địa điểm còn hoạt động.
- Nguồn xác minh mới.

## Liên kết nội bộ

- Món liên quan:
- Địa điểm liên quan:
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

Dùng cross-reference nhẹ, không duplicate toàn bộ nội dung:

- File địa điểm chứa thông tin canonical của từng quán/địa điểm.
- File đặc sản chứa danh sách ngắn các địa điểm tiêu biểu.
- File guide tóm tắt theo nhu cầu người dùng và trỏ tới món/địa điểm liên quan.
- Query rewriting và second-hop retrieval sau này có thể dùng `related_places` và
  `related_food_topics`.
