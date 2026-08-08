# Project Status

Last updated: `2026-08-08 15:58:50 +07`

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

- `restaurants/`: 57 file curated.
- `cafes/`: 23 file curated.
- `local_specialties/`: 8 file hiện có và đã hoàn thiện: `bun bo hue.md`, `com hen.md`, `com am phu.md`, `banh ep.md`, `me xung.md`, `che heo quay.md`, `banh canh nam pho.md` và `banh nam.md`.
- `food-guides.md`: 1 file guide hiện còn trống; đã có spec/plan để coding agent khác triển khai sau khi có dữ liệu research.

Chuẩn curated cốt lõi: không YAML frontmatter, file bắt đầu bằng `#`, chỉ ghi dữ liệu có nguồn, source tracking ở `## Nguồn dữ liệu`, không thêm `Liên kết nội bộ` vào body. Riêng `food-guides.md` là guide tổng hợp và không bắt buộc có `## Nguồn dữ liệu`. Tên file trong `restaurants/` và `cafes/` đã được chuẩn hóa bằng cách thay dấu gạch bằng khoảng trắng.

8 món hoặc nhóm món đặc sản đã curate:

- Bún bò Huế
- Cơm hến
- Cơm âm phủ
- Bánh nậm
- Chè heo quay
- Bánh ép
- Mè xửng
- Bánh canh Nam Phổ

## Trạng thái triển khai

Đã hoàn thành:

- Khảo sát raw data và source dumps của hai nguồn HueGov.
- Tạo source dumps, README ghi chú chuyển đổi và taxonomy folders.
- Chốt template/chuẩn curated cho `foods`.
- Curate 56 restaurants và 23 cafes từ dữ liệu người dùng cung cấp.
- Cập nhật chuẩn `foods-template.md` cho `local_specialties` và exception của `food-guides.md`.
- Tạo spec/plan cho `food-guides.md` tại `knowledge-base-hue/meta/food-guides-spec.md`.
- Curate `foods/local_specialties/bun bo hue.md`.
- Curate `foods/local_specialties/banh ep.md`.
- Đổi tên và curate `foods/local_specialties/com hen.md`.
- Curate `foods/local_specialties/com am phu.md`.
- Curate `foods/local_specialties/me xung.md`.
- Curate `foods/local_specialties/che heo quay.md`.
- Đổi tên và curate `foods/local_specialties/banh canh nam pho.md`.
- Đổi tên và curate `foods/local_specialties/banh nam.md`.
- Curate `foods/restaurants/che mo ton dich.md`.

Chưa thực hiện:

- Hoàn thiện `foods/food-guides.md` dựa trên spec/plan và dữ liệu đã curate.
- Curate đầy đủ các category heritage, festivals, performing arts, tourism, services, tickets và statistics.
- Enrichment có nguồn xác minh; chunking, embedding, indexing, retriever và recommender.

## Cập nhật gần nhất

### 2026-08-08 15:58:50 +07

- Thay đổi: Hoàn thiện 8 local specialties đầu tiên, bổ sung Chè Mợ Tôn Đích vào restaurants và cập nhật process curation đơn giản dùng brainstorming nhẹ trong chat, không tạo spec/plan file.
- File chính: `Session_Prompt.md`, `Project_Status.md`, `knowledge-base-hue/foods/local_specialties/`, `knowledge-base-hue/foods/restaurants/che mo ton dich.md`.
- Validation: Kiểm tra heading, frontmatter, section `Liên kết nội bộ`, dữ liệu rỗng và địa chỉ liên quan của các file mới/cập nhật; chạy `git diff --check`.
- Next action: Hoàn thiện `foods/food-guides.md` theo spec hiện có, sau đó chuyển sang các category heritage, festivals, performing arts, tourism, services, tickets và statistics.
