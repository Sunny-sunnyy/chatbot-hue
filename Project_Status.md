# Project Status

Last updated: `2026-08-05 21:45:34 +07`

## Cách cập nhật file này

Sau mỗi task hoặc cuối mỗi session có thay đổi, agent phải cập nhật file này.

Mỗi lần cập nhật cần ghi rõ:

- Thời gian Việt Nam UTC+7.
- Ngày hiện tại.
- Thay đổi đã thực hiện.
- File chính đã tạo/sửa.
- Validation đã chạy và kết quả.
- Next action đề xuất.

Được phép sửa hoặc xóa nội dung không còn chính xác để file luôn phản ánh trạng
thái hiện tại của dự án.

## Mục tiêu dự án

Xây dựng dữ liệu nền cho:

- RAG Chatbot về văn hóa, du lịch Huế.
- Agentic RAG.
- Hybrid Recommender + LLM cho trải nghiệm du lịch/văn hóa Huế.

Định hướng dữ liệu đã chốt:

```text
raw
  -> Markdown source dumps
  -> curated category Markdown
  -> enrichment/update có nguồn xác minh
  -> chunks
  -> embeddings/index
```

Không chunk trực tiếp từ `_source-dumps` nếu chưa curate.

## Quy tắc làm việc quan trọng

- Giao tiếp với người dùng bằng tiếng Việt.
- Code, comments, docstrings và tên biến dùng English chuẩn.
- Dùng `uv`; khi chạy Python trong sandbox dùng:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python ...
```

- Không dùng `pip`.
- Không đọc/in secrets như `.env`, token, key, auth files.
- Không sửa raw data.
- Không gọi web hoặc enrich nếu người dùng chưa yêu cầu rõ.
- Không push/commit nếu người dùng chưa yêu cầu.
- Với task brainstorming, chốt design trước khi tạo/sửa file.

## Trạng thái dữ liệu raw

Raw data gốc do người dùng lấy từ `https://data.hue.gov.vn/`.

Raw folders:

```text
backend/data/huegov_department_of_tourism/raw
backend/data/huegov_culture_and_tourism/raw
```

### huegov_department_of_tourism/raw

Có 11 JSON files. Đã tạo source dumps.

Cấu trúc chính:

- Root list:
  - danh mục loại vé: 88 records
  - địa điểm di tích tham quan: 12 records
  - hướng dẫn viên du lịch: 1920 records
- Root object `{code, message, data, hienthi}`:
  - địa điểm ăn uống: 6794 `data` records, 20 `hienthi` records
  - di sản: 50 `data`, 10 `hienthi`
  - di tích văn hóa: 180 `data`, 19 `hienthi`
  - lễ hội: 138 `data`, 18 `hienthi`
- Root object `{data, totalRows}`:
  - điểm du lịch: 196 records
  - vận chuyển: 154 records
  - lữ hành: 10 records
- Root object `{totalCount, newsList}`:
  - giá vé dịch vụ di tích Huế: 12 records

Bất thường giữ nguyên theo raw:

- `Du-lieu-cac-doanh-nghiep-kinh-doanh-dich-vu-lu-hanh_1704353395.json`
  có `totalRows=190` nhưng `data` chỉ có 10 records.

### huegov_culture_and_tourism/raw

Có 21 raw files:

- 9 JSON
- 9 XLSX
- 3 RDF

Đã tạo source dumps.

Ghi chú:

- `Nhac_Chuong_Nha_Nhac_1744278211.json` là list rỗng.
- 3 JSON files duplicate byte-identical với department source:
  - `Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603.json`
  - `Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601.json`
  - `Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601.json`

## Source dumps đã hoàn thành

### Department of Tourism

Script:

```text
backend/scripts/convert_huegov_department_raw_to_md.py
```

Output:

```text
knowledge-base-hue/_source-dumps/huegov_department_of_tourism/
```

Kết quả:

- 11 Markdown files + `README.md`.
- Converter dùng Python standard library.
- HTML được strip/decode/collapse whitespace.
- Nested dict/list được render bằng fenced JSON block.
- Raw data không bị sửa trong quá trình tạo source dump.

### Culture and Tourism

Script:

```text
backend/scripts/convert_huegov_culture_raw_to_md.py
```

Output:

```text
knowledge-base-hue/_source-dumps/huegov_culture_and_tourism/
```

Kết quả:

- 21 Markdown files + `README.md`.
- Hỗ trợ JSON, XLSX, RDF.
- Chỉ dùng Python standard library.
- Empty dataset vẫn tạo Markdown và ghi `No records found.`
- Duplicate notes đã được ghi trong README.

Validation đã kiểm tra trong session:

- `UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile backend/scripts/convert_huegov_culture_raw_to_md.py`
- Converter chạy được với output tạm trong `/tmp`.
- 21 output Markdown files đều có frontmatter/sections bắt buộc.
- Duplicate files được kiểm tra md5 là byte-identical.

## Cấu trúc knowledge-base-hue hiện tại

Các category folders hiện có:

```text
knowledge-base-hue/_source-dumps
knowledge-base-hue/festivals
knowledge-base-hue/foods
knowledge-base-hue/heritage
knowledge-base-hue/meta
knowledge-base-hue/performing_arts
knowledge-base-hue/services
knowledge-base-hue/statistics
knowledge-base-hue/tickets
knowledge-base-hue/tourism
```

`foods` hiện có:

```text
knowledge-base-hue/foods/
  restaurants/
  cafes/
  local_specialties/
  food-guides.md
```

## Thiết kế foods đã chốt

Template/schema chính:

```text
knowledge-base-hue/meta/foods-template.md
```

Quyết định:

- Giữ cấu trúc `restaurants`, `cafes`, `local_specialties`, `food-guides.md`.
- `restaurants/*.md`: entity địa điểm ăn uống.
- `cafes/*.md`: entity quán cà phê hoặc đồ uống.
- `local_specialties/*.md`: entity món ăn/đặc sản.
- `food-guides.md`: guide tổng hợp theo nhu cầu người dùng.
- Core frontmatter bắt buộc có metadata phục vụ source tracking, RAG,
  recommender và Agentic RAG.
- YAML keys dùng English `snake_case`.
- YAML text values và Markdown body dùng tiếng Việt có dấu.
- Optional fields thiếu dữ liệu thì bỏ, không bịa dữ liệu.
- `menu_items` lưu cả frontmatter ngắn và body chi tiết.
- Nếu raw chỉ có khoảng giá chung theo địa điểm, không tự gán giá cho từng món.
- Ban đầu dùng `status: "draft"` và `enrichment_status: "needs_enrichment"`.
- Dùng cross-reference nhẹ:
  - file quán chứa chi tiết canonical
  - file món có danh sách địa điểm tiêu biểu ngắn
  - guide trỏ tới món/quán liên quan
- Query rewriting và second-hop retrieval sau này có thể dùng
  `related_places` và `related_food_topics`.

Tiêu chí chọn 20-50 địa điểm đầu tiên:

- Có mô tả raw hữu ích.
- Có địa chỉ.
- Có giá/giờ/tọa độ nếu có.
- Đại diện nhiều nhóm món:
  - bún bò
  - bánh Huế
  - chè Huế
  - cơm hến / bún hến
  - món chay
  - chợ / ăn vặt
  - cà phê hoặc đồ uống khi có
- Tránh trùng lặp quá nhiều cùng một địa điểm/món.

## Git/GitHub

Git metadata trong workspace `.git` từng bị read-only/không hợp lệ. Đã dùng git
metadata tạm tại:

```text
/tmp/hue_rag_git
```

Đã push initial commit lên GitHub:

```text
https://github.com/Sunny-sunnyy/chatbot-hue.git
```

Branch:

```text
main
```

Commit đã push:

```text
2830f58 Initial commit
```

Lưu ý:

- `.env`, `.venv`, `.claude`, `__pycache__`, `backend/data/` không được commit.
- Nếu cần commit/push trong session sau, kiểm tra lại trạng thái `.git`. Nếu `.git`
  vẫn không hợp lệ, có thể tiếp tục dùng `/tmp/hue_rag_git` hoặc khởi tạo git hợp
  lệ nếu môi trường cho phép.

## Trạng thái hiện tại

Đã hoàn thành:

- Khảo sát raw data hai nguồn.
- Khảo sát knowledge-base mẫu cũ.
- Chốt hướng Markdown-first với `_source-dumps`.
- Tạo source dumps cho `huegov_department_of_tourism/raw`.
- Tạo source dumps cho `huegov_culture_and_tourism/raw`.
- Tạo taxonomy folders trong `knowledge-base-hue`.
- Chốt thiết kế folder và template cho `foods`.
- Tạo `knowledge-base-hue/meta/foods-template.md`.
- Tạo `Session_Prompt.md` và `Project_Status.md` để thay thế vai trò context
  chính của `Agent_session_prompt.md`.
- `Agent_session_prompt.md` đã được thay thế và không còn là file context chính.

Chưa hoàn thành:

- Curate 20-50 địa điểm nổi bật trong `foods/restaurants` và `foods/cafes`.
- Curate 5-8 món đặc sản trong `foods/local_specialties`.
- Hoàn thiện `foods/food-guides.md`.
- Curate các category khác như heritage, festivals, performing_arts, tourism,
  services, tickets, statistics.
- Enrichment/cập nhật thông tin bằng nguồn xác minh.
- Chunking.
- Embedding.
- Retriever/index.
- Recommender.

## Next best action

Bước tiếp theo nên là curate batch đầu tiên cho:

```text
knowledge-base-hue/foods
```

Đề xuất làm theo thứ tự:

1. Đọc `knowledge-base-hue/meta/foods-template.md`.
2. Phân tích source dump ăn uống:

```text
knowledge-base-hue/_source-dumps/huegov_department_of_tourism/danh-sach-dia-diem-an-uong-tren-dia-ban-tinh_1726311604.md
```

3. Chọn 20-50 địa điểm theo tiêu chí đã chốt.
4. Chọn 5-8 món đặc sản có đủ raw mentions.
5. Tạo curated files theo template.
6. Validate frontmatter/sections.
7. Cập nhật `Project_Status.md`.

## Update log

### 2026-08-05 21:40:09 +07

- Tạo `Session_Prompt.md` làm entrypoint context mới cho coding agent session sau.
- Tạo `Project_Status.md` làm file trạng thái sống của dự án.
- Ghi rõ quy tắc cập nhật Project Status theo giờ Việt Nam UTC+7.
- Ghi lại trạng thái hiện tại: source dumps hai nguồn đã hoàn thành, foods
  template đã chốt, task tiếp theo là curate batch đầu tiên cho `foods`.

### 2026-08-05 21:45:34 +07

- Kiểm tra remote GitHub `origin/main`; remote đang ở commit `2830f58 Initial commit`
  trước khi commit/push thay đổi context mới.
- Chuẩn bị commit các file context mới:
  - `Session_Prompt.md`
  - `Project_Status.md`
  - `knowledge-base-hue/meta/foods-template.md`
- Ghi nhận `Agent_session_prompt.md` đã được thay thế bởi hai file context mới.
- Không commit các file `.md` rỗng trong taxonomy folders để tránh placeholder
  không có nội dung.
