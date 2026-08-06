# Project Status

Last updated: `2026-08-06 15:57:57 +07`

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
    banh-ep-hue.md
    banh-ep-gia-di.md
    banh-loc-hue-ba-van.md
    bun-bo-ba-nga.md
    bun-bo-canh-van.md
    bun-bo-hanh.md
    bun-bo-mu-roi.md
    bun-bo-o-nhon.md
    com-hen-17-han-mac-tu.md
    com-hen-ba-cam.md
    com-hen-bun-hen-lanh.md
    com-hen-dap-da.md
    com-hen-hoa-dong.md
    com-hen-thu-hien.md
    nha-hang-banh-ba-do.md
    quan-ba-cu.md
    quan-banh-chi.md
    quan-bun-bo-me-keo.md
    quan-nho.md
    quan-o-giau.md
  cafes/
  local_specialties/
  food-guides.md
```

## Cập nhật gần nhất

### 2026-08-06 15:57:57 +07

Thay đổi đã thực hiện:

- Cập nhật `Session_Prompt.md` để session sau phản ánh trạng thái foods mới nhất:
  hiện có 20 file curated trong `knowledge-base-hue/foods/restaurants/`.
- Ghi lại các điểm cần rà soát ở session sau:
  - `banh-ep-hue.md`: địa chỉ `116` hay `118 Lê Ngô Cát`.
  - `quan-ba-cu.md`: giờ mở cửa `07:00 - 21:00` hay `07:15 - 20:00`.
  - `quan-o-giau.md`: giờ mở cửa `10:00 - 19:00` hay `10:00 - hết bánh`.
  - `banh-ep-gia-di.md`: chưa có giờ mở cửa.
- Cập nhật trạng thái trước khi commit/push các file Markdown cần thiết cho đợt
  curate foods chiều 2026-08-06 theo yêu cầu người dùng.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- `UV_CACHE_DIR=/tmp/uv-cache uv run python -c "..."`
  kiểm tra 20 file trong `knowledge-base-hue/foods/restaurants`: file bắt đầu
  bằng H1, không có YAML frontmatter, không có section `Liên kết nội bộ`, không
  có cụm `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính:
  pass.

Next action đề xuất:

- Session sau đọc lại `Session_Prompt.md`, `Project_Status.md` và
  `knowledge-base-hue/meta/foods-template.md` trước khi tiếp tục.
- Tiếp tục rà soát các điểm còn mâu thuẫn nhỏ về địa chỉ/giờ mở cửa, rồi cân
  nhắc tạo `local_specialties/com-hen.md` hoặc `local_specialties/banh-ep.md`.

### 2026-08-06 15:56:19 +07

Thay đổi đã thực hiện:

- Tạo file curated mới `knowledge-base-hue/foods/restaurants/banh-ep-hue.md` từ
  thông tin người dùng cung cấp.
- File mới dùng format restaurants hiện tại: không frontmatter, bắt đầu bằng H1,
  có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`, `Nguồn dữ liệu`.
- Ghi `Nguồn chính: hue.aeonmall-vietnam.com` theo dữ liệu người dùng cung cấp.
- Dữ liệu địa chỉ có hai số nhà `116` và `118`; file dùng `116 Lê Ngô Cát` theo
  dòng địa chỉ chính và giữ ghi chú cần rà soát trong phần trải nghiệm.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho `banh-ep-hue.md`: file bắt đầu bằng H1, không có
  YAML frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính.
- Đọc lại nội dung file sau khi tạo để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng rà soát `banh-ep-hue.md`, đặc biệt là địa chỉ `116` hay
  `118 Lê Ngô Cát`.
- Tiếp tục curate thêm các quán bánh ép/ăn vặt nổi bật hoặc tạo file
  `local_specialties/banh-ep.md` sau khi có đủ địa điểm tiêu biểu.

### 2026-08-06 15:54:52 +07

Thay đổi đã thực hiện:

- Tạo file curated mới `knowledge-base-hue/foods/restaurants/banh-ep-gia-di.md`
  từ thông tin người dùng cung cấp.
- File mới dùng format restaurants hiện tại: không frontmatter, bắt đầu bằng H1,
  có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`, `Nguồn dữ liệu`.
- Ghi `Nguồn chính: hue.aeonmall-vietnam.com` theo dữ liệu người dùng cung cấp.
- Ghi khoảng giá chung theo cái trong section `Thông tin`; không tạo bảng
  `Menu và giá tham khảo` vì chưa có giá theo từng loại bánh.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho `banh-ep-gia-di.md`: file bắt đầu bằng H1, không có
  YAML frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính.
- Đọc lại nội dung file sau khi tạo để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng rà soát `banh-ep-gia-di.md`, bổ sung giờ mở cửa hoặc kênh liên hệ
  nếu có.
- Tiếp tục curate thêm các quán bánh Huế/ăn vặt nổi bật hoặc tạo file
  `local_specialties` cho nhóm bánh Huế sau khi có đủ địa điểm tiêu biểu.

### 2026-08-06 15:48:46 +07

Thay đổi đã thực hiện:

- Tạo file curated mới `knowledge-base-hue/foods/restaurants/quan-o-giau.md` từ
  thông tin người dùng cung cấp.
- File mới dùng format restaurants hiện tại: không frontmatter, bắt đầu bằng H1,
  có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`, `Nguồn dữ liệu`.
- Ghi `Nguồn chính: hue.aeonmall-vietnam.com` theo dữ liệu người dùng cung cấp.
- Dữ liệu giờ mở cửa có hai cách ghi; file dùng `10:00 - 19:00` trong section
  `Thông tin` và giữ ghi chú thường hết bánh sớm trong phần trải nghiệm.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho `quan-o-giau.md`: file bắt đầu bằng H1, không có
  YAML frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính.
- Đọc lại nội dung file sau khi tạo để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng rà soát `quan-o-giau.md`, đặc biệt là giờ mở cửa nếu muốn ghi
  `10:00 - hết bánh` thay cho khung giờ cố định.
- Tiếp tục curate thêm các quán bánh Huế nổi bật hoặc tạo file
  `local_specialties` cho nhóm bánh Huế sau khi có đủ địa điểm tiêu biểu.

### 2026-08-06 15:45:35 +07

Thay đổi đã thực hiện:

- Tạo file curated mới `knowledge-base-hue/foods/restaurants/banh-loc-hue-ba-van.md`
  từ thông tin người dùng cung cấp.
- File mới dùng format restaurants hiện tại: không frontmatter, bắt đầu bằng H1,
  có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`, `Menu và giá
  tham khảo`, `Nguồn dữ liệu`.
- Ghi `Nguồn chính: hue.aeonmall-vietnam.com` theo dữ liệu người dùng cung cấp.
- Thêm bảng `Menu và giá tham khảo` vì dữ liệu có giá theo đĩa và giá túi mang
  về cụ thể.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho `banh-loc-hue-ba-van.md`: file bắt đầu bằng H1,
  không có YAML frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính.
- Đọc lại nội dung file sau khi tạo để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng rà soát `banh-loc-hue-ba-van.md`, đặc biệt là bảng giá mang về nếu
  muốn tách riêng bánh sống và bánh chín.
- Tiếp tục curate thêm các quán bánh Huế nổi bật hoặc tạo file
  `local_specialties` cho nhóm bánh Huế sau khi có đủ địa điểm tiêu biểu.

### 2026-08-06 15:42:55 +07

Thay đổi đã thực hiện:

- Tạo file curated mới `knowledge-base-hue/foods/restaurants/quan-ba-cu.md` từ
  thông tin người dùng cung cấp.
- File mới dùng format restaurants hiện tại: không frontmatter, bắt đầu bằng H1,
  có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`, `Nguồn dữ liệu`.
- Ghi `Nguồn chính: hue.aeonmall-vietnam.com` theo dữ liệu người dùng cung cấp.
- Dữ liệu giờ mở cửa có hai phiên bản; file ghi khoảng giờ chung trong section
  `Thông tin` và giữ ghi chú chi tiết `07:15 - 20:00 hằng ngày` trong phần trải
  nghiệm.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho `quan-ba-cu.md`: file bắt đầu bằng H1, không có YAML
  frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính.
- Đọc lại nội dung file sau khi tạo để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng rà soát `quan-ba-cu.md`, đặc biệt là giờ mở cửa nếu muốn chốt một
  phiên bản duy nhất.
- Tiếp tục curate thêm các quán bánh Huế nổi bật hoặc tạo file
  `local_specialties` cho nhóm bánh Huế sau khi có đủ địa điểm tiêu biểu.

### 2026-08-06 15:38:14 +07

Thay đổi đã thực hiện:

- Tạo file curated mới `knowledge-base-hue/foods/restaurants/quan-banh-chi.md`
  từ thông tin người dùng cung cấp.
- File mới dùng format restaurants hiện tại: không frontmatter, bắt đầu bằng H1,
  có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`, `Nguồn dữ liệu`.
- Ghi `Nguồn chính: hue.aeonmall-vietnam.com` theo dữ liệu người dùng cung cấp.
- Ghi mức giá chung trong section `Thông tin`; thông tin `15.000 VNĐ - 20.000
  VNĐ/đĩa` được ghi trong phần trải nghiệm vì chưa có bảng giá theo từng món đầy
  đủ.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho `quan-banh-chi.md`: file bắt đầu bằng H1, không có
  YAML frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính.
- Đọc lại nội dung file sau khi tạo để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng rà soát `quan-banh-chi.md`, bổ sung ảnh hoặc URL Facebook cụ thể
  nếu muốn.
- Tiếp tục curate thêm các quán bánh Huế nổi bật hoặc tạo file
  `local_specialties` cho nhóm bánh Huế sau khi có đủ địa điểm tiêu biểu.

### 2026-08-06 15:34:03 +07

Thay đổi đã thực hiện:

- Tạo file curated mới `knowledge-base-hue/foods/restaurants/nha-hang-banh-ba-do.md`
  từ thông tin người dùng cung cấp.
- File mới dùng format restaurants hiện tại: không frontmatter, bắt đầu bằng H1,
  có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`, `Nguồn dữ liệu`.
- Ghi `Nguồn chính: khamphahue.com.vn` theo dữ liệu người dùng cung cấp.
- Ghi khoảng giá chung trong section `Thông tin`; không tạo bảng
  `Menu và giá tham khảo` vì chưa có giá theo từng món.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho `nha-hang-banh-ba-do.md`: file bắt đầu bằng H1,
  không có YAML frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính.
- Đọc lại nội dung file sau khi tạo để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng rà soát `nha-hang-banh-ba-do.md`, bổ sung ảnh hoặc URL Facebook
  cụ thể nếu muốn.
- Tiếp tục curate thêm các quán bánh Huế nổi bật hoặc tạo file
  `local_specialties` cho nhóm bánh bèo, bánh nậm, bánh lọc sau khi có đủ địa
  điểm tiêu biểu.

### 2026-08-06 15:26:33 +07

Thay đổi đã thực hiện:

- Tạo 6 file curated mới trong `knowledge-base-hue/foods/restaurants/` từ thông
  tin người dùng cung cấp:
  - `com-hen-ba-cam.md`
  - `quan-nho.md`
  - `com-hen-dap-da.md`
  - `com-hen-17-han-mac-tu.md`
  - `com-hen-bun-hen-lanh.md`
  - `com-hen-thu-hien.md`
- Các file mới dùng format restaurants hiện tại: không frontmatter, bắt đầu
  bằng H1, có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`,
  `Nguồn dữ liệu`.
- Ghi `Nguồn chính: mia.vn` cho các quán theo yêu cầu của người dùng.
- Ghi khoảng giá chung trong section `Thông tin`; không tạo bảng
  `Menu và giá tham khảo` vì chưa có giá theo từng món.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho 7 file cơm hến/bún hến hiện có trong
  `knowledge-base-hue/foods/restaurants`: file bắt đầu bằng H1, không có YAML
  frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`, có đủ các section chính.
- Đọc lại danh sách file trong `restaurants` sau khi tạo.

Next action đề xuất:

- Người dùng rà soát 7 file cơm hến/bún hến, bổ sung ảnh hoặc nguồn URL cụ thể
  nếu muốn.
- Sau khi nhóm địa điểm cơm hến ổn, tạo file `local_specialties/com-hen.md` để
  tổng hợp món cơm hến và trỏ về các địa điểm tiêu biểu.

### 2026-08-06 15:19:25 +07

Thay đổi đã thực hiện:

- Tạo file curated mới `knowledge-base-hue/foods/restaurants/com-hen-hoa-dong.md`
  từ thông tin người dùng cung cấp.
- File mới dùng format restaurants hiện tại: không frontmatter, bắt đầu bằng H1,
  có các section `Tóm tắt`, `Thông tin`, `Món ăn / trải nghiệm`, `Nguồn dữ liệu`.
- Ghi khoảng giá chung của quán trong section `Thông tin`; không tạo bảng
  `Menu và giá tham khảo` vì chưa có giá theo từng món.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Kiểm tra format cơ bản cho `com-hen-hoa-dong.md`: file bắt đầu bằng H1, không
  có YAML frontmatter, không có section `Liên kết nội bộ`, không có cụm
  `chưa có dữ liệu` hoặc `không có thông tin`.
- Đọc lại nội dung file sau khi tạo để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng rà soát `com-hen-hoa-dong.md`, bổ sung ảnh hoặc nguồn cụ thể nếu
  muốn.
- Tiếp tục curate thêm các địa điểm cơm hến/bún hến Huế hoặc tạo file
  `local_specialties` cho món cơm hến sau khi có đủ vài địa điểm tiêu biểu.

### 2026-08-06 12:05:49 +07

Thay đổi đã thực hiện:

- Cập nhật `Session_Prompt.md` để phản ánh trạng thái mới nhất cho session buổi
  chiều:
  - foods template hiện dùng Markdown không frontmatter;
  - không ghi field/section thiếu dữ liệu;
  - không dùng section `Liên kết nội bộ`;
  - ảnh đặt trong section `## Món ăn / trải nghiệm`;
  - đã có 6 file bún bò trong `knowledge-base-hue/foods/restaurants/`;
  - commit đã push: `3ca366b Curate Hue beef noodle restaurants`.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- Đọc lại `Session_Prompt.md`, `Project_Status.md` và `foods-template.md` sau
  cập nhật context.
- `git status --short --branch` xác nhận `main` đang track `origin/main`; commit
  foods đã push, hiện chỉ còn thay đổi context chưa commit.

Next action đề xuất:

- Buổi chiều bắt đầu bằng việc đọc lại `Session_Prompt.md`,
  `Project_Status.md`, `knowledge-base-hue/meta/foods-template.md`.
- Người dùng rà soát 5 file bún bò mới và bổ sung thông tin/ảnh nếu cần.
- Sau đó curate tiếp nhóm bánh Huế hoặc chè Huế theo format tối giản.

### 2026-08-06 11:53:16 +07

Thay đổi đã thực hiện:

- Tạo 5 file curated mới trong `knowledge-base-hue/foods/restaurants/` từ thông
  tin người dùng cung cấp:
  - `bun-bo-mu-roi.md`
  - `bun-bo-canh-van.md`
  - `bun-bo-hanh.md`
  - `bun-bo-o-nhon.md`
  - `bun-bo-ba-nga.md`
- Cập nhật `knowledge-base-hue/meta/foods-template.md`:
  - bỏ section `Liên kết nội bộ`;
  - thống nhất heading `## Món ăn / trải nghiệm`;
  - giữ `Menu và giá tham khảo` là optional section, chỉ dùng khi có menu hoặc
    giá theo từng món;
  - field hoặc section thiếu dữ liệu thì bỏ hẳn, không ghi `chưa có dữ liệu`
    hoặc `không có thông tin`.
  - ghi chú retrieval chuyển sang hướng không nhúng graph/cross-reference vào
    nội dung `.md`; nếu cần thì dùng sidecar/index riêng.
- 5 file mới không dùng frontmatter, không có section menu rỗng, không có liên
  hệ/website khi không có dữ liệu.
- Không sửa raw data, không gọi web.

Validation đã chạy:

- `UV_CACHE_DIR=/tmp/uv-cache uv run python -c "..."`
  kiểm tra 6 file trong `knowledge-base-hue/foods/restaurants`: bắt đầu bằng
  H1, không có YAML frontmatter, không có `Liên kết nội bộ`, không có
  `chưa có dữ liệu`/`không có thông tin`, không có dòng `Liên hệ:` hoặc
  `Website:` khi thiếu dữ liệu: pass.
- `rg` kiểm tra restaurants không chứa section `Liên kết nội bộ` hoặc các mẫu
  thiếu dữ liệu; template chỉ còn nhắc `Liên kết nội bộ` trong quy tắc cấm thêm
  section này vào body.
- Đọc lại phần đầu của 5 file mới để kiểm tra cấu trúc và nội dung.

Next action đề xuất:

- Người dùng đọc 5 file mới và bổ sung thông tin/ảnh nếu cần.
- Sau khi mẫu 6 file bún bò ổn, curate tiếp nhóm bánh Huế hoặc chè Huế theo
  cùng format tối giản.

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
- Curated `.md` trong `foods` không dùng YAML frontmatter; file bắt đầu trực
  tiếp bằng heading `#` để giảm nhiễu khi chunk/embedding.
- Source tracking tối giản được lưu trong section `## Nguồn dữ liệu`, không
  nhúng metadata pipeline vào đầu file.
- Nếu sau này cần structured metadata cho recommender/filtering, tạo sidecar
  hoặc index riêng thay vì nhúng YAML vào `.md`.
- Nội dung người dùng nhìn thấy và nội dung RAG đọc ưu tiên tiếng Việt có dấu.
- Field hoặc section thiếu dữ liệu thì bỏ hẳn, không ghi `chưa có dữ liệu` hoặc
  `không có thông tin`.
- Nếu raw chỉ có khoảng giá chung theo địa điểm, không tự gán giá cho từng món.
- Không thêm section `Liên kết nội bộ` vào curated `.md` ở giai đoạn này để
  tránh nhiễu nội dung RAG.

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
6. Validate file bắt đầu bằng heading `#`, không có YAML frontmatter và có các
   section nội dung chính.
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

### 2026-08-05 21:49:29 +07

- Khôi phục `.git` hợp lệ trực tiếp trong `/home/hieu0606sunny/hue_rag` bằng Git
  metadata từ `/tmp/hue_rag_git`.
- Xác nhận lệnh Git bình thường trong project đã hoạt động lại:
  - `git status --short --branch`
  - `git log -2 --oneline --decorate`
  - `git remote -v`
- Remote vẫn là `https://github.com/Sunny-sunnyy/chatbot-hue.git`, branch `main`
  đang track `origin/main`.
- Sau khi khôi phục, Git UI/VS Code có thể hiển thị lại trạng thái `modified` và
  `untracked` trong chính folder dự án.
