# Project Status

Last updated: `2026-08-06 17:14:57 +07`

## Mục tiêu dự án

Xây dựng dữ liệu nền cho:

- RAG Chatbot về văn hóa và du lịch Huế.
- Agentic RAG.
- Hybrid Recommender + LLM cho trải nghiệm du lịch và văn hóa Huế.

## Pipeline dữ liệu

```text
raw
  -> Markdown source dumps
  -> curated category Markdown
  -> enrichment/update có nguồn xác minh
  -> chunks
  -> embeddings/index
```

Không chunk trực tiếp từ `_source-dumps` nếu chưa curate.

## Quy tắc trạng thái hiện tại

- Raw data chỉ đọc, không sửa.
- Không gọi web hoặc enrich nếu người dùng chưa yêu cầu rõ.
- Không commit hoặc push nếu người dùng chưa yêu cầu.
- Thông tin không được cung cấp sẽ không được ghi vào curated Markdown hoặc
  Project_Status.md.
- Khi chạy Python trong sandbox, dùng `UV_CACHE_DIR=/tmp/uv-cache uv run python ...`.
- Quy tắc giao tiếp và quy trình làm việc chi tiết nằm trong `Session_Prompt.md`.

## Raw data và source dumps

Raw data do người dùng lấy từ `https://data.hue.gov.vn/` và nằm tại:

```text
backend/data/huegov_department_of_tourism/raw
backend/data/huegov_culture_and_tourism/raw
```

Đã hoàn thành source dumps cho cả hai nhóm:

- Department of Tourism: 11 JSON files được chuyển sang
  `knowledge-base-hue/_source-dumps/huegov_department_of_tourism/` bằng
  `backend/scripts/convert_huegov_department_raw_to_md.py`.
- Culture and Tourism: 21 raw files gồm JSON, XLSX và RDF được chuyển sang
  `knowledge-base-hue/_source-dumps/huegov_culture_and_tourism/` bằng
  `backend/scripts/convert_huegov_culture_raw_to_md.py`.

README trong từng source dump ghi các dataset rỗng, duplicate và ghi chú chuyển
đổi kỹ thuật. Source dumps không phải curated knowledge base.

## Cấu trúc knowledge base

```text
knowledge-base-hue/
  _source-dumps/
  festivals/
  foods/
  heritage/
  meta/
  performing_arts/
  services/
  statistics/
  tickets/
  tourism/
```

## Trạng thái foods

Template chính:

```text
knowledge-base-hue/meta/foods-template.md
```

Số lượng Markdown hiện tại trong `knowledge-base-hue/foods/`:

- `restaurants/`: 33 file curated.
- `cafes/`: 0 file curated.
- `local_specialties/`: 0 file curated.
- `food-guides.md`: 1 file guide.

Chuẩn curated đã chốt:

- File bắt đầu trực tiếp bằng heading `#`, không dùng YAML frontmatter.
- Không ghi field hoặc section không có dữ liệu.
- Không ghi các câu `chưa có dữ liệu` hoặc `không có thông tin` vào body.
- Source tracking tối giản nằm trong section `## Nguồn dữ liệu`.
- Không thêm section `Liên kết nội bộ` vào body curated.
- Nếu raw chỉ có giá chung theo địa điểm, không tự gán giá cho từng món.
- Restaurants và cafes dùng các section chính `Tóm tắt`, `Thông tin`,
  `Món ăn / trải nghiệm` và `Nguồn dữ liệu`.
- `local_specialties` chỉ tổng hợp từ dữ liệu địa điểm hoặc nội dung có nguồn.

Phạm vi giai đoạn đầu là khoảng 20-50 địa điểm nổi bật và 5-8 món đặc sản,
không tạo hàng nghìn file từ toàn bộ raw records.

## Trạng thái triển khai

Đã hoàn thành:

- Khảo sát raw data và source dump của hai nguồn HueGov.
- Tạo source dumps và README ghi chú chuyển đổi.
- Tạo taxonomy folders trong `knowledge-base-hue/`.
- Chốt template và chuẩn curated cho `foods`.
- Curate 33 địa điểm trong `foods/restaurants/` từ dữ liệu người dùng cung cấp.

Chưa thực hiện:

- Curate các file trong `foods/local_specialties/`.
- Hoàn thiện `foods/food-guides.md` theo dữ liệu curated.
- Curate đầy đủ các category heritage, festivals, performing_arts, tourism,
  services, tickets và statistics.
- Enrichment có nguồn xác minh.
- Chunking, embedding, indexing, retriever và recommender.

## Cập nhật gần nhất

### 2026-08-06 17:14:57 +07

Thay đổi đã thực hiện:

- Cập nhật `Session_Prompt.md` theo workflow `using-superpowers` và
  `brainstorming` đã được người dùng xác nhận.
- Xóa danh sách foods cũ, commit history và next actions lỗi thời khỏi
  `Session_Prompt.md`.
- Bổ sung curation policy, source policy, worktree safety và approval gate.
- Không sửa raw data hoặc curated foods.

Validation đã chạy:

- Kiểm tra cấu trúc, stale content và các policy bắt buộc trong
  `Session_Prompt.md`.
- `git diff --check -- Session_Prompt.md` đã pass.

Next action đề xuất:

- Session sau đọc `Session_Prompt.md`, `Project_Status.md` và
  `knowledge-base-hue/meta/foods-template.md` trước khi tiếp tục.

### 2026-08-06 16:54:11 +07

- Rút gọn `Project_Status.md` thành trạng thái hiện tại, loại bỏ log chi tiết
  từng địa điểm và nội dung lỗi thời.
- Cập nhật số lượng foods hiện tại: 33 restaurants, 0 cafes, 0 local_specialties
  và 1 food guide.
- Loại bỏ danh sách các thông tin chưa được người dùng cung cấp hoặc chưa chốt.
- Giữ nguyên raw data và các file curated khác.

Validation:

- Kiểm tra cấu trúc Markdown và các section chính của file trạng thái.
- Kiểm tra số lượng file hiện tại trong `knowledge-base-hue/foods/`.
- Không sửa raw data và không gọi web.

## Next action

- Tiếp tục curate khi người dùng cung cấp dữ liệu có nguồn.
- Sau khi đủ địa điểm tiêu biểu, tạo 5-8 file `local_specialties/` từ dữ liệu đã
  curate.
- Hoàn thiện `food-guides.md`, sau đó mới thiết kế chunking và indexing cho dữ
  liệu curated.
