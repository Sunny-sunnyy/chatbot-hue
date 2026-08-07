# Project Status

Last updated: `2026-08-07 16:53:16 +07`

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

## Trạng thái foods

- `restaurants/`: 56 file curated.
- `cafes/`: 23 file curated.
- `local_specialties/`: 0 file curated.
- `food-guides.md`: 1 file guide.

Chuẩn curated cốt lõi: không YAML frontmatter, file bắt đầu bằng `#`, chỉ ghi dữ liệu có nguồn, source tracking ở `## Nguồn dữ liệu`, không thêm `Liên kết nội bộ` vào body. Tên file trong `restaurants/` và `cafes/` đã được chuẩn hóa bằng cách thay dấu gạch bằng khoảng trắng.

## Trạng thái triển khai

Đã hoàn thành:

- Khảo sát raw data và source dumps của hai nguồn HueGov.
- Tạo source dumps, README ghi chú chuyển đổi và taxonomy folders.
- Chốt template/chuẩn curated cho `foods`.
- Curate 56 restaurants và 23 cafes từ dữ liệu người dùng cung cấp.

Chưa thực hiện:

- Curate `foods/local_specialties/`.
- Hoàn thiện `foods/food-guides.md` theo dữ liệu curated.
- Curate đầy đủ các category heritage, festivals, performing arts, tourism, services, tickets và statistics.
- Enrichment có nguồn xác minh; chunking, embedding, indexing, retriever và recommender.

## Cập nhật gần nhất

### 2026-08-07 16:53:16 +07

- Thay đổi: Cập nhật snapshot foods sau khi curate thêm các cafe có nguồn do người dùng cung cấp; tổng số cafe curated hiện tại là 23. Chuẩn hóa tên file trong `restaurants/` và `cafes/`.
- File chính: `Project_Status.md`, `knowledge-base-hue/foods/cafes/`.
- Validation: Kiểm tra số lượng `restaurants`, `cafes`, `local_specialties` và `food-guides.md`; chạy `git diff --check` cho các file cafe mới.
- Next action: Tiếp tục curate cafe hoặc địa điểm ăn uống khi người dùng cung cấp dữ liệu có nguồn; sau đó hoàn thiện `local_specialties` và `food-guides.md`.
