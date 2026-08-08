# Project Status

Last updated: `2026-08-08 16:57:54 +07`

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
- `food-guides.md`: đã hoàn thiện với 17 sections, tổng hợp từ dữ liệu curated và 4 bài Cẩm nang AEON MALL Huế cập nhật 2026 (chi phí, ăn sáng, ăn trưa, ăn đêm). Spec tương ứng đã cập nhật tại `meta/food-guides-spec.md`.

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
- Hoàn thiện `foods/food-guides.md` (17 sections) và cập nhật `meta/food-guides-spec.md` cho khớp design đã duyệt.

Chưa thực hiện:

- Curate đầy đủ các category heritage, festivals, performing arts, tourism, services, tickets và statistics.
- Enrichment có nguồn xác minh; chunking, embedding, indexing, retriever và recommender.

## Cập nhật gần nhất

### 2026-08-08 16:57:54 +07

- Thay đổi: Hoàn thiện `foods/food-guides.md` với 17 sections (8 món đặc sản, ăn theo thời điểm trong ngày gồm cả ăn đêm, cà phê, chay, ngọt, ngân sách, nhóm người dùng, 4 food tour) từ dữ liệu curated + 4 bài Cẩm nang AEON MALL Huế 2026 do người dùng cung cấp; cập nhật `meta/food-guides-spec.md` cho khớp (tên 8 file món thực tế, section ăn đêm, quy tắc ngân sách/nghiên cứu, địa chỉ đã xác nhận). Quy trình: brainstorming đầy đủ trong chat, user duyệt từng quyết định trước khi viết file. Chỉ dùng quán có trong curated; địa chỉ chuẩn theo xác nhận của người dùng (Bà Cam 49 Tùng Thiện Vương, O Hoa 3 Trịnh Công Sơn, O Tho 14 Trần Cao Vân); Bánh bà Chi (2/64 Hoàng Diệu) là quán khác nên không dùng.
- File chính: `knowledge-base-hue/foods/food-guides.md`, `knowledge-base-hue/meta/food-guides-spec.md`, `Project_Status.md`.
- Validation: 51/51 quán trong guide có file curated, địa chỉ khớp từng file; đủ headings, không YAML, không section `Nguồn dữ liệu`, không file path; không section rỗng; `git diff --check` sạch; không đụng thay đổi có sẵn của người dùng trong `knowledge-base/`.
- Next action: Chuyển sang curate các category heritage, festivals, performing arts, tourism, services, tickets và statistics; sau đó enrichment có nguồn xác minh, chunking, embedding, indexing, retriever và recommender.
