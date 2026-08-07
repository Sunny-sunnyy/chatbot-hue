# Project Status

Last updated: `2026-08-07 20:09:22 +07`

## Mục tiêu dự án

- RAG Chatbot về văn hóa và du lịch Huế.
- Agentic RAG.
- Hybrid Recommender + LLM cho trải nghiệm du lịch và văn hóa Huế.

## Pipeline dữ liệu

```text
raw -> Markdown source dumps -> curated Markdown -> enrichment có nguồn xác minh -> chunks -> embeddings/index
```

Không chunk trực tiếp từ `_source-dumps` nếu chưa curate.

## Nguồn và cấu trúc chính

- Raw Department of Tourism: `backend/data/huegov_department_of_tourism/raw`
- Raw Culture and Tourism: `backend/data/huegov_culture_and_tourism/raw`
- Source dumps: `knowledge-base-hue/_source-dumps/`
- Curated knowledge base: `knowledge-base-hue/`
- Foods template: `knowledge-base-hue/meta/foods-template.md`
- Food guides spec: `knowledge-base-hue/meta/food-guides-spec.md`

## Trạng thái foods

- `restaurants/`: 56 file curated.
- `cafes/`: 23 file curated.
- `local_specialties/`: 0 file curated; đã chốt scope 8 món hoặc nhóm món đặc sản đầu tiên.
- `food-guides.md`: 1 file guide hiện còn trống; đã có spec/plan để coding agent khác triển khai sau khi có dữ liệu research.

Chuẩn curated cốt lõi: không YAML frontmatter, file bắt đầu bằng `#`, chỉ ghi dữ liệu có nguồn, source tracking ở `## Nguồn dữ liệu`, không thêm `Liên kết nội bộ` vào body. Riêng `food-guides.md` là guide tổng hợp và không bắt buộc có `## Nguồn dữ liệu`. Tên file trong `restaurants/` và `cafes/` đã được chuẩn hóa bằng cách thay dấu gạch bằng khoảng trắng.

8 món hoặc nhóm món đặc sản dự kiến curate trước:

- Bún bò Huế
- Cơm hến / bún hến
- Cơm âm phủ
- Bánh Huế: bánh bèo, bánh nậm, bánh lọc
- Chè Huế / chè heo quay
- Bánh ép
- Mè xửng
- Bánh canh Huế: bánh canh Nam Phổ / bánh canh cá lóc

## Trạng thái triển khai

Đã hoàn thành:

- Khảo sát raw data và source dumps của hai nguồn HueGov.
- Tạo source dumps, README ghi chú chuyển đổi và taxonomy folders.
- Chốt template/chuẩn curated cho `foods`.
- Curate 56 restaurants và 23 cafes từ dữ liệu người dùng cung cấp.
- Cập nhật chuẩn `foods-template.md` cho `local_specialties` và exception của `food-guides.md`.
- Tạo spec/plan cho `food-guides.md` tại `knowledge-base-hue/meta/food-guides-spec.md`.

Chưa thực hiện:

- Curate 8 file đầu tiên trong `foods/local_specialties/` từ research/source do người dùng cung cấp.
- Hoàn thiện `foods/food-guides.md` dựa trên spec/plan và dữ liệu đã curate.
- Curate đầy đủ các category heritage, festivals, performing arts, tourism, services, tickets và statistics.
- Enrichment có nguồn xác minh; chunking, embedding, indexing, retriever và recommender.

## Cập nhật gần nhất

### 2026-08-07 20:09:22 +07

- Thay đổi: Chốt thiết kế mới cho `foods/local_specialties/` và `foods/food-guides.md`. `local_specialties` sẽ chứa 8 món hoặc nhóm món đặc sản đầu tiên; `food-guides.md` là guide tổng hợp theo thời điểm, ngân sách, nhóm người dùng và itinerary nửa ngày/1 ngày/2 ngày/3 ngày.
- File chính: `Project_Status.md`, `knowledge-base-hue/meta/foods-template.md`, `knowledge-base-hue/meta/food-guides-spec.md`.
- Validation: Kiểm tra số lượng `restaurants`, `cafes`, `local_specialties`; chạy `git diff --check` cho `foods-template.md` và `food-guides-spec.md`; scan `food-guides-spec.md` để loại marker placeholder phổ biến.
- Next action: Khi người dùng cung cấp research/source, curate lần lượt 8 file `foods/local_specialties/*.md`; sau đó giao `food-guides.md` cho coding agent khác triển khai theo `food-guides-spec.md`.
