# Agent Session Prompt — Huế RAG Knowledge Base Preparation

## 1. Vai trò và cách làm việc

Bạn đang làm trong repo:

```text
/home/hieu0606sunny/hue_rag
```

Giao tiếp với người dùng bằng tiếng Việt. Code, comments, docstrings và tên biến dùng tiếng Anh chuẩn.

Người dùng là sinh viên đang học AI Engineering: Agents, LLMs, Deep Learning, ML, Data Science. Mục tiêu là xây dựng dữ liệu nền cho các dự án:

- RAG Chatbot về văn hoá, du lịch Huế
- Agentic RAG
- Hybrid Recommender + LLM cho trải nghiệm du lịch/văn hoá Huế

Phong cách làm việc mong muốn:

- Rõ ràng, thực tế, không over-engineer.
- Trước khi code, nêu giả định nếu task phức tạp hoặc có nhiều cách hiểu.
- Làm từng bước nhỏ, kiểm chứng sau mỗi bước quan trọng.
- Không sửa ngoài scope.
- Không tự gọi web hoặc enrich dữ liệu nếu chưa được yêu cầu rõ.
- Không đọc/in secrets như `.env`, token, key, auth files.
- Không sửa dữ liệu raw.
- Không push/commit nếu người dùng không yêu cầu.

Python package manager:

```text
uv
```

Khi chạy Python trong sandbox, dùng:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python ...
```

Không dùng `pip`.

## 2. File nên đọc đầu session mới

Để nắm đúng trạng thái hiện tại, agent nên đọc các file/folder sau trước khi làm tiếp:

```text
/home/hieu0606sunny/hue_rag/Agent_session_prompt.md
/home/hieu0606sunny/hue_rag/brainstorming.md
/home/hieu0606sunny/hue_rag/backend/scripts/convert_huegov_department_raw_to_md.py
/home/hieu0606sunny/hue_rag/knowledge-base-hue/_source-dumps/huegov_department_of_tourism/README.md
```

Nên khảo sát read-only các folder:

```text
/home/hieu0606sunny/hue_rag/backend/data/huegov_department_of_tourism/raw
/home/hieu0606sunny/hue_rag/backend/data/huegov_culture_and_tourism/raw
/home/hieu0606sunny/hue_rag/knowledge-base-hue
/home/hieu0606sunny/hue_rag/knowledge-base
```

Không đọc `.env` trừ khi người dùng yêu cầu trực tiếp và có lý do rõ. Thực tế task dữ liệu này không cần secrets.

## 3. File brainstorming.md dùng như thế nào

Có file:

```text
/home/hieu0606sunny/hue_rag/brainstorming.md
```

File này mô tả phong cách làm việc có tính brainstorming: hỏi rõ yêu cầu, không code khi scope chưa thống nhất, ưu tiên quy trình kỹ lưỡng.

Tuy nhiên trong các task đã được xác nhận rõ, không áp dụng máy móc yêu cầu “dừng lại chờ xác nhận mới tạo file”. Nếu task mới đã có scope cụ thể, hãy thực hiện. Chỉ dừng hỏi khi có blocker thật sự như:

- thiếu folder/file đầu vào
- output path xung đột
- lựa chọn thiết kế có thể làm thay đổi scope lớn
- cần quyền ghi/đọc ngoài sandbox

## 4. Dữ liệu raw hiện có

Nguồn dữ liệu gốc do người dùng lấy từ:

```text
https://data.hue.gov.vn/
```

Raw data nằm trong hai folder chính:

```text
/home/hieu0606sunny/hue_rag/backend/data/huegov_department_of_tourism/raw
/home/hieu0606sunny/hue_rag/backend/data/huegov_culture_and_tourism/raw
```

### 4.1. huegov_department_of_tourism/raw

Folder này đã được xử lý bước source dump. Có 11 file JSON:

```text
Danh-muc-loai-ve_1757394149.json
Danh-sach-cac-diem-du-lich_1731690004 (1).json
Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603 (1).json
Danh-sach-dia-diem-an-uong-tren-dia-ban-tinh_1726311604.json
Danh-sach-dia-diem-di-tich-tham-quan_1757394149.json
Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601 (1).json
Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601 (1).json
Du-lieu-cac-doanh-nghiep-kinh-doanh-dich-vu-lu-hanh_1704353395.json
Du-lieu-danh-sach-co-so-kinh-doanh-dich-vu-van-chuyen-1_1731690004.json
Gia-ve-dich-vu-di-tich-Hue_1730079840.json
HuongDanVienDuLich_Hue_2024-06-23_1719914684 (1).json
```

Các cấu trúc JSON chính đã phát hiện:

- Root list:
  - danh mục loại vé: 88 records
  - địa điểm di tích tham quan: 12 records
  - hướng dẫn viên du lịch: 1920 records
- Root object `{code, message, data, hienthi}`:
  - địa điểm ăn uống: 6794 `data` records, 20 `hienthi` records
  - di sản: 50 `data`, 10 `hienthi`
  - di tích văn hoá: 180 `data`, 19 `hienthi`
  - lễ hội: 138 `data`, 18 `hienthi`
- Root object `{data, totalRows}`:
  - điểm du lịch: 196 records
  - vận chuyển: 154 records
  - lữ hành: 10 records
- Root object `{totalCount, newsList}`:
  - giá vé dịch vụ di tích Huế: 12 records

Bất thường đã ghi nhận:

- `Du-lieu-cac-doanh-nghiep-kinh-doanh-dich-vu-lu-hanh_1704353395.json` có `totalRows=190` nhưng `data` chỉ có 10 records. Giữ nguyên theo raw, không tự sửa.
- Một số record có field rỗng như `""`, `null`, `[]`; converter bỏ các field không có giá trị theo nguyên tắc “không bỏ field nào nếu có giá trị”.

### 4.2. huegov_culture_and_tourism/raw

Folder này chưa được xử lý source dump. Có 21 file:

```text
Am_nhac_Tuong_1744277620.xlsx
Ban_Nha_Nhac_1744278156.json
CHUA-DIEM-PHUNG--CONG-VIEN-THUY-TU-jpeg,.jpg.rdf
Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603.json
Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601.json
Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601.json
Dao_cu_san_khau_1744277648.xlsx
Diem-den-sinh-thai-van-hoa-dac-sac-1.rdf
Du-lieu-ve-gia-ve-tham-quan-di-tich-cua-Trung-tam-Bao-ton-di-tich-Co-do-Hue-1_1785085393.json
Du-lieu-ve-luot-khach-tham-quan-cac-diem-Di-tich-cua-Trung-tam-Bao-ton-Di-tich-Co-do-Hue-2_1785207796 (1).json
Hat_Tuong_1744277688.xlsx
Kich_ban_Tuong_1744277711.xlsx
Lang-du-lich-cong-dong-Hoa-giay-Thanh-Tien-1-jpeg,.jpg.rdf
Mat_na_Tuong_1744277740.xlsx
Nghe_nhan_Nha_Nhac_1744278182.json
Nhac_Chuong_Nha_Nhac_1744278211.json
Nhac_cu_Nha_Nhac_1744278236.json
Phuc_trang_Tuong_1744277759.xlsx
Trich_doan_Tuong_1744277783.xlsx
Tu_ngu_nghe_thuat_Tuong_1744277802.xlsx
Vu_dao_Tuong_1744277823.xlsx
```

Thành phần file:

- 9 JSON
- 9 XLSX
- 3 RDF

Các điểm đáng chú ý:

- `Nhac_Chuong_Nha_Nhac_1744278211.json` là list rỗng.
- 3 file JSON trong folder này bị duplicate nội dung với department folder:
  - `Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603.json`
  - `Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601.json`
  - `Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601.json`
- RDF chủ yếu là metadata/DCAT, nhưng có thể chứa title, description, apiHeader, issued/modified, downloadURL. Một RDF về “Điểm đến sinh thái, văn hóa đặc sắc” có nội dung mô tả dài về Bến thuyền Thủy Tú.
- XLSX liên quan đến Tuồng: âm nhạc, đạo cụ sân khấu, hát tuồng, kịch bản, mặt nạ, phục trang, trích đoạn, từ ngữ nghệ thuật, vũ đạo.

Schema JSON đã phát hiện trong folder culture:

- `Ban_Nha_Nhac_1744278156.json`: list 33 records, keys như `STT`, `ID`, `title`, `TheLoai`, `temporal`, `audience`, `source`, `description`, `LoiNhac`, `MoTa`, `PhanTich`, `HinhThuc`, `createdAt`, `updatedAt`.
- `Nghe_nhan_Nha_Nhac_1744278182.json`: list 12 records, keys như `title`, `alternative`, `NgheNghiep`, `date`, `spatial`, `NganhHoc`, `NhacCu`, `NamHoc`, `TheHe`, `DanhHieu`, ...
- `Nhac_cu_Nha_Nhac_1744278236.json`: list 18 records, keys như `title`, `BoNhacCu`, `source`, `HinhThuc`, `ViTri`, `TinhNang`, `DacTinh`, `description`.
- `Du-lieu-ve-gia-ve-tham-quan...json`: list 22 records, keys như `placeID`, `total`, `placeTitle`, `soVeDon`, `soVeTuyen`, `customerType`, `customerTypeName`.
- `Du-lieu-ve-luot-khach...json`: object có `chart` list 13 records và `grid` list 52 records.
- `Nhac_Chuong_Nha_Nhac_1744278211.json`: list rỗng.

## 5. Dữ liệu mẫu cũ đã tham khảo

Người dùng có dataset Markdown mẫu từ dự án RAG trước:

```text
/home/hieu0606sunny/hue_rag/knowledge-base
```

Folder này gồm 76 file `.md`:

```text
knowledge-base/company
knowledge-base/contracts
knowledge-base/employees
knowledge-base/products
```

Đặc điểm:

- Mỗi file thường là một entity/document độc lập.
- Dùng Markdown heading rõ: `#`, `##`, `###`.
- Không có YAML frontmatter.
- Dữ liệu metadata nằm trực tiếp trong nội dung.
- Phù hợp cho RAG demo, nhưng yếu cho source tracking, freshness tracking, filtering, recommender.

Quyết định đã thống nhất:

- Với Huế, vẫn dùng Markdown làm artifact chính cho RAG.
- Nhưng nên thêm YAML frontmatter để trace source, trạng thái enrich, ngày generate, source file.
- Markdown không nên là database duy nhất cho mọi thứ về lâu dài, nhưng ở giai đoạn hiện tại ưu tiên convert raw sang Markdown trước vì schema raw quá khác nhau.

## 6. Quyết định thiết kế đã chốt

### 6.1. Hướng xử lý dữ liệu

Ban đầu có đề xuất normalize structured data trước rồi sinh Markdown. Người dùng phản biện đúng: mỗi file có format khác nhau, mỗi JSON có schema khác nhau, nhiều file thiếu thông tin. Nếu normalize ngay, phải viết handler riêng cho từng file, trong khi dữ liệu vẫn cần cập nhật/enrich sau.

Quyết định hiện tại:

```text
raw
  -> Markdown source dumps
  -> curated category Markdown
  -> enrich/update content
  -> chunks
  -> embeddings/index
```

Tức là làm Markdown trước, nhưng chia làm 2 lớp:

```text
knowledge-base-hue/_source-dumps
knowledge-base-hue/<category folders>
```

`_source-dumps` là bản chuyển thô từ raw sang Markdown để dễ đọc/review và giữ dấu vết nguồn.

Các folder category như `foods`, `heritage`, `festivals`, `performing-arts`, `tourism` là bản curate/enrich cho RAG thật sự. Không chunk trực tiếp từ `_source-dumps` nếu chưa curate.

### 6.2. Source dump không phải enrich

Source dump chỉ được làm các biến đổi kỹ thuật nhẹ:

- strip HTML tags
- decode HTML entities
- collapse whitespace
- render JSON/XLSX/RDF thành Markdown đọc được
- ghi rõ detected structure
- giữ source metadata

Không được:

- tự cập nhật thông tin năm 2026
- gọi web
- thêm thông tin không có trong raw
- sửa sai factual nếu không có nguồn

Lưu ý: script hiện tại có thêm một số limited diacritic fixes trong source dump. Việc này đã được ghi trong README, nhưng cần cẩn trọng vì `_source-dumps` nên gần raw nhất có thể. Hai fix `Nem chua -> Nem chua` và `Kim chi chay -> Kim chi chay` là no-op, nên nếu có dịp sửa script thì nên bỏ để tránh README gây hiểu nhầm.

### 6.3. Folder taxonomy cho knowledge-base-hue

Người dùng muốn chia rõ folder như:

- foods
- heritage
- festivals
- performing-arts
- tourism

Folder hiện tại đã tồn tại:

```text
knowledge-base-hue
knowledge-base-hue/_source-dumps
knowledge-base-hue/_source-dumps/huegov_department_of_tourism
knowledge-base-hue/festivals
knowledge-base-hue/foods
knowledge-base-hue/heritage
knowledge-base-hue/performing-arts
```

Đề xuất taxonomy đầy đủ hơn cho các bước sau:

```text
knowledge-base-hue/
  _source-dumps/
    huegov_department_of_tourism/
    huegov_culture_and_tourism/

  foods/
    restaurants/
    cafes/
    local-specialties/
    food-guides.md

  heritage/
    cultural-heritage/
    heritage-sites/
    intangible-heritage/
    monuments/

  festivals/
    traditional-festivals/
    annual-events/
    festival-guides.md

  performing-arts/
    nha-nhac/
    tuong/
    artists/
    instruments/
    scripts/
    costumes/
    masks/
    stage-props/
    terminology/

  tourism/
    attractions/
    community-tourism/
    eco-tourism/
    suggested-places/
    itineraries/
    travel-guides.md

  services/
    tour-guides/
    travel-agencies/
    transport-providers/

  tickets/
    heritage-ticket-prices.md
    ticket-types.md

  statistics/
    visitor-statistics.md

  meta/
    sources.md
    update-log.md
    enrichment-needed.md
    duplicates.md
```

Quan trọng: `tourism` có thể chứa bài guide tổng hợp và có thể nhắc tới quán ăn, quán cà phê, di tích, di sản, lễ hội. Nhưng không nên copy toàn bộ nội dung entity từ `foods`, `heritage`, `festivals` sang `tourism`, vì vector search sẽ dễ bị duplicate chunk. `tourism` nên là curated guide layer.

### 6.4. Mapping dữ liệu raw sang category sau này

Mapping dự kiến:

| Raw data | Folder category sau curate |
|---|---|
| `Danh-sach-dia-diem-an-uong...json` | `foods/restaurants`, `foods/cafes`, có thể được tham chiếu trong `tourism/suggested-places` |
| `Danh-sach-di-san-van-hoa...json` | `heritage/intangible-heritage`, `heritage/cultural-heritage` |
| `Danh-sach-dia-diem-di-tich-van-hoa...json` | `heritage/heritage-sites`, `heritage/monuments`, `tourism/attractions` |
| `Danh-sach-le-hoi...json` | `festivals/traditional-festivals` |
| `Danh-sach-cac-diem-du-lich...json` | `tourism/attractions` |
| RDF về Chùa Diêm Phụng, Bến thuyền Thủy Tú, Hoa giấy Thanh Tiên | `tourism/community-tourism`, `tourism/eco-tourism`, `heritage` nếu liên quan |
| `Ban_Nha_Nhac`, `Nhac_cu_Nha_Nhac`, `Nghe_nhan_Nha_Nhac` | `performing-arts/nha-nhac` |
| Các XLSX Tuồng | `performing-arts/tuong/*` |
| `HuongDanVienDuLich...json` | `services/tour-guides` |
| doanh nghiệp lữ hành | `services/travel-agencies` |
| cơ sở vận chuyển | `services/transport-providers` |
| giá vé, loại vé | `tickets/` |
| lượt khách tham quan | `statistics/visitor-statistics.md` |

## 7. Công việc đã hoàn thành

### 7.1. Tạo source dump cho huegov_department_of_tourism

Script đã được tạo:

```text
/home/hieu0606sunny/hue_rag/backend/scripts/convert_huegov_department_raw_to_md.py
```

Script dùng standard library:

- `pathlib`
- `json`
- `re`
- `html`
- `datetime`

Chức năng:

- Duyệt toàn bộ `.json` trong `backend/data/huegov_department_of_tourism/raw`.
- Tự phát hiện root structure: list/object.
- Render toàn bộ field có giá trị.
- Strip HTML, decode entities, collapse whitespace.
- Nested dict/list khó render thì đưa vào fenced JSON block.
- Tạo Markdown source dump cho từng raw file.
- Tự sinh README index.

Output đã tạo:

```text
/home/hieu0606sunny/hue_rag/knowledge-base-hue/_source-dumps/huegov_department_of_tourism/
```

Gồm 11 file `.md` + `README.md`:

```text
README.md
danh-muc-loai-ve_1757394149.md
danh-sach-cac-diem-du-lich_1731690004-1.md
danh-sach-di-san-van-hoa-tinh-thua-thien-hue-1_1726311603-1.md
danh-sach-dia-diem-an-uong-tren-dia-ban-tinh_1726311604.md
danh-sach-dia-diem-di-tich-tham-quan_1757394149.md
danh-sach-dia-diem-di-tich-van-hoa-tinh-thua-thien-hue_1726311601-1.md
danh-sach-le-hoi-tren-dia-ban-tinh-thua-thien-hue_1726311601-1.md
du-lieu-cac-doanh-nghiep-kinh-doanh-dich-vu-lu-hanh_1704353395.md
du-lieu-danh-sach-co-so-kinh-doanh-dich-vu-van-chuyen-1_1731690004.md
gia-ve-dich-vu-di-tich-hue_1730079840.md
huongdanviendulich_hue_2024-06-23_1719914684-1.md
```

Validation đã chạy bởi agent trước:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python backend/scripts/convert_huegov_department_raw_to_md.py
```

Kết quả:

- Script chạy thành công.
- 11 raw JSON convert thành 11 Markdown files.
- README được sinh.
- Sample 3 file đã kiểm tra: ăn uống, hướng dẫn viên, giá vé.
- HTML đã sạch.
- Record count khớp.
- Raw không bị sửa theo md5 trước/sau.

File rất lớn:

- `danh-sach-dia-diem-an-uong-tren-dia-ban-tinh_1726311604.md`: khoảng 1.77 MB, 6794 data records + 20 hienthi records.
- `danh-sach-dia-diem-di-tich-van-hoa-tinh-thua-thien-hue_1726311601-1.md`: khoảng 800 KB, 180 records.
- `huongdanviendulich_hue_2024-06-23_1719914684-1.md`: khoảng 528 KB, 1920 records.

### 7.2. Sửa title tiếng Việt có dấu trong output department

Agent trước đã thêm mapping tay cho H1 title trong script:

- `# Danh sách địa điểm ăn uống trên địa bàn tỉnh`
- `# Danh sách các điểm du lịch`
- `# Danh sách di sản văn hóa tỉnh Thừa Thiên Huế`
- `# Danh sách địa điểm di tích tham quan`
- `# Danh sách địa điểm di tích văn hóa tỉnh Thừa Thiên Huế`
- `# Danh sách lễ hội trên địa bàn tỉnh Thừa Thiên Huế`
- `# Dữ liệu các doanh nghiệp kinh doanh dịch vụ lữ hành`
- `# Dữ liệu danh sách cơ sở kinh doanh dịch vụ vận chuyển`
- `# Danh mục loại vé`
- `# Giá vé dịch vụ di tích Huế`
- `# Hướng dẫn viên du lịch Huế 2024-06-23`

Ngoài ra có limited diacritic fixes trong render field lines:

- `Le Loi` -> `Lê Lợi`
- `Phan Chu Trinh` -> `Phan Châu Trinh`

README ghi chú “Diacritic fixes applied on conversion” để trace.

## 8. Công việc chưa làm

Chưa xử lý:

```text
/home/hieu0606sunny/hue_rag/backend/data/huegov_culture_and_tourism/raw
```

Chưa tạo:

```text
/home/hieu0606sunny/hue_rag/knowledge-base-hue/_source-dumps/huegov_culture_and_tourism/
```

Chưa curate/enrich category folders:

```text
knowledge-base-hue/foods
knowledge-base-hue/heritage
knowledge-base-hue/festivals
knowledge-base-hue/performing-arts
knowledge-base-hue/tourism
```

Chưa làm:

- cập nhật thông tin tới ngày 2026-08-05
- gọi web để xác minh
- tạo chunks
- tạo embeddings
- xây retriever/index
- xây recommender

## 9. Công việc tiếp theo khuyến nghị

### Bước tiếp theo gần nhất

Tạo source dump cho:

```text
backend/data/huegov_culture_and_tourism/raw
```

Output:

```text
knowledge-base-hue/_source-dumps/huegov_culture_and_tourism/
```

Nên tạo script mới hoặc mở rộng pattern cũ:

```text
backend/scripts/convert_huegov_culture_raw_to_md.py
```

Khuyến nghị tạo script riêng để tránh làm script department phức tạp quá sớm.

Script mới cần xử lý:

- JSON
- XLSX
- RDF

Vẫn là source dump, không enrich.

### Yêu cầu cho converter culture

1. Duyệt toàn bộ file trong:

```text
backend/data/huegov_culture_and_tourism/raw
```

2. Với mỗi file `.json`, `.xlsx`, `.rdf`, tạo một `.md` tương ứng trong:

```text
knowledge-base-hue/_source-dumps/huegov_culture_and_tourism/
```

3. Mỗi Markdown file cần có YAML frontmatter:

```yaml
---
source_name: "data.hue.gov.vn"
source_group: "huegov_culture_and_tourism"
source_file: "<raw filename>"
source_path: "backend/data/huegov_culture_and_tourism/raw/<raw filename>"
source_format: "json|xlsx|rdf"
conversion_type: "source_dump"
enrichment_status: "not_enriched"
generated_at: "<ISO datetime>"
---
```

Nếu áp dụng text transformations thì nên thêm:

```yaml
text_transformations:
  - strip_html
  - decode_html_entities
```

Không nên thêm diacritic fixes mới nếu không cần thiết. Nếu thêm, phải ghi rõ trong README.

4. Tạo README:

```text
knowledge-base-hue/_source-dumps/huegov_culture_and_tourism/README.md
```

README cần liệt kê:

- tổng số file raw đã convert
- từng file `.md` được tạo
- source format
- root type hoặc detected structure
- record count/list count/sheet count nếu có
- empty dataset nếu có
- duplicate notes với department folder

5. Validation:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python backend/scripts/convert_huegov_culture_raw_to_md.py
```

Kiểm tra:

- số file `.md` bằng số file raw culture + README
- sample JSON Nhã nhạc đọc được
- sample XLSX Tuồng đọc được
- sample RDF đọc được
- file rỗng `Nhac_Chuong_Nha_Nhac_1744278211.json` vẫn có Markdown và ghi `No records found`
- raw files không bị sửa

### Parser đề xuất cho culture

JSON:

- Reuse logic từ `convert_huegov_department_raw_to_md.py`.
- Root list: render từng record.
- Root object: render scalar, list fields, nested JSON block.
- Empty list: tạo Markdown với `No records found`.

XLSX:

- Ưu tiên standard library nếu có thể: `zipfile`, `xml.etree.ElementTree`.
- Không bắt buộc dùng `openpyxl`; nếu muốn thêm dependency thì phải hỏi người dùng trước.
- Render mỗi sheet thành Markdown section.
- Nếu detect được rows/cells, render bảng Markdown hoặc compact row records.
- Các file XLSX hiện có title preview như “Danh sách Âm nhạc tuồng”, “Danh sách Đạo cụ sân khấu”, ...

RDF:

- Dùng `xml.etree.ElementTree`.
- Parse các trường nếu có:
  - `dcterms:identifier`
  - `dcterms:created`
  - `dcterms:modified`
  - `dcterms:title`
  - `dcterms:issued`
  - `dcterms:description`
  - `hueod:apiHeader`
  - `hueod:downloadURL`
  - `dcat:mediaType`
  - `dcat:byteSize`
  - `hueod:ratingStars`
- Nếu parse namespace khó, fallback bằng regex có kiểm soát.
- Render raw XML excerpt hoặc parsed fields rõ ràng, nhưng không bỏ thông tin quan trọng.

### Duplicate notes cần ghi

Các file culture sau duplicate với department source dumps:

```text
Danh-sach-di-san-van-hoa-tinh-Thua-Thien-Hue-1_1726311603.json
Danh-sach-dia-diem-di-tich-van-hoa-tinh-Thua-Thien-Hue_1726311601.json
Danh-sach-le-hoi-tren-dia-ban-tinh-Thua-Thien-Hue_1726311601.json
```

Không xoá, không skip nếu chưa có yêu cầu. Vẫn convert thành source dump, nhưng ghi duplicate note trong README.

## 10. Prompt gợi ý cho agent tiếp theo

Nếu cần giao task tiếp theo cho agent khác, có thể dùng prompt này:

```text
Bạn đang làm trong repo:

/home/hieu0606sunny/hue_rag

Đọc trước:

/home/hieu0606sunny/hue_rag/Agent_session_prompt.md
/home/hieu0606sunny/hue_rag/backend/scripts/convert_huegov_department_raw_to_md.py
/home/hieu0606sunny/hue_rag/knowledge-base-hue/_source-dumps/huegov_department_of_tourism/README.md

Mục tiêu:
Tạo Markdown source dumps cho toàn bộ raw files trong:

/home/hieu0606sunny/hue_rag/backend/data/huegov_culture_and_tourism/raw

Output:

/home/hieu0606sunny/hue_rag/knowledge-base-hue/_source-dumps/huegov_culture_and_tourism/

Tạo script:

/home/hieu0606sunny/hue_rag/backend/scripts/convert_huegov_culture_raw_to_md.py

Scope:
- Xử lý `.json`, `.xlsx`, `.rdf`.
- Không enrich.
- Không gọi web.
- Không cập nhật thông tin 2026.
- Không sửa raw.
- Không tạo/chỉnh category folders.
- Vẫn convert duplicate files, nhưng ghi duplicate note trong README.

Yêu cầu converter:
- Markdown có YAML frontmatter.
- Có Source Summary.
- Có Detected Structure.
- Có Content.
- JSON reuse pattern từ converter department.
- XLSX parse bằng standard library nếu có thể.
- RDF parse bằng xml.etree.ElementTree hoặc fallback regex kiểm soát.
- File rỗng vẫn tạo Markdown và ghi rõ No records found.
- Tạo README index tổng hợp.

Validation:
Chạy:

UV_CACHE_DIR=/tmp/uv-cache uv run python backend/scripts/convert_huegov_culture_raw_to_md.py

Sau đó kiểm tra:
- số file .md = số raw files culture + README
- sample JSON Nhã nhạc
- sample XLSX Tuồng
- sample RDF
- raw không bị sửa

Báo cáo cuối bằng tiếng Việt:
- script đã tạo
- output đã tạo
- số file convert theo format
- file rỗng/bất thường
- duplicate notes
- validation command đã chạy
- bước tiếp theo đề xuất
```

## 11. Giai đoạn sau source dump

Sau khi cả hai source dump folders hoàn tất, mới bắt đầu curate/enrich.

### 11.1. Tạo category knowledge base

Tạo hoặc bổ sung các folder:

```text
knowledge-base-hue/foods
knowledge-base-hue/heritage
knowledge-base-hue/festivals
knowledge-base-hue/performing-arts
knowledge-base-hue/tourism
knowledge-base-hue/services
knowledge-base-hue/tickets
knowledge-base-hue/statistics
knowledge-base-hue/meta
```

### 11.2. Curate từ source dumps

Không chunk trực tiếp từ `_source-dumps`.

Quy trình sau này:

```text
_source-dumps
  -> chọn nội dung đáng dùng
  -> tạo category Markdown có metadata
  -> enrich/xác minh thông tin
  -> tạo chunks
  -> embedding/index
```

### 11.3. Template Markdown category đề xuất

Ví dụ cho food/place:

```md
---
title: "Quán bún Mệ Kéo"
category: "foods"
sub_category: "restaurant"
source_file: "Danh-sach-dia-diem-an-uong-tren-dia-ban-tinh_1726311604.json"
source_type: "huegov_raw"
status: "needs_enrichment"
last_verified: null
updated_for: "2026-08-05"
---

# Quán bún Mệ Kéo

## Tóm tắt

...

## Thông tin hiện có từ dữ liệu gốc

...

## Thông tin cần cập nhật

- Giờ mở cửa
- Số điện thoại
- Tình trạng còn hoạt động
- Giá hiện tại
- Nguồn xác minh

## Nguồn

...
```

### 11.4. Enrichment/freshness

Người dùng muốn cập nhật thông tin đúng tới thời điểm hiện tại là ngày:

```text
2026-08-05
```

Không được để LLM tự bịa thông tin. Mỗi thông tin enrich/cập nhật cần có:

- nguồn xác minh
- ngày xác minh
- mức tin cậy
- ghi chú nếu dữ liệu không chắc

Nếu dùng web/API ở giai đoạn enrich, cần người dùng xác nhận scope cụ thể.

## 12. Rủi ro kỹ thuật cần nhớ

- Dữ liệu raw không đồng nhất, không nên ép schema chung quá sớm.
- Source dump quá lớn không nên dùng trực tiếp cho embedding.
- Duplicate giữa hai nguồn có thể làm vector search trả nhiều chunk giống nhau.
- Folder `tourism` nên là guide/tổng hợp, không duplicate nguyên văn toàn bộ entity.
- Field HTML cần strip/decode.
- RDF không phải knowledge graph đầy đủ, chủ yếu là metadata/distribution.
- XLSX có thể có cell rỗng/merged/header không chuẩn; cần parser tolerant.
- Không nên bỏ dữ liệu chỉ vì thiếu field.
- Không nên tự sửa factual content nếu không có nguồn.

## 13. Trạng thái hoàn tất hiện tại

Đã hoàn thành:

- Khảo sát raw data hai nguồn.
- Khảo sát knowledge-base mẫu cũ.
- Chốt hướng Markdown-first với `_source-dumps` trước.
- Tạo `knowledge-base-hue`.
- Tạo source dumps cho `huegov_department_of_tourism/raw`.
- Tạo script converter department.
- Tạo README index cho department source dumps.

Chưa hoàn thành:

- Source dumps cho `huegov_culture_and_tourism/raw`.
- Category curated Markdown.
- Enrichment/cập nhật 2026.
- Chunking.
- Embedding.
- Retrieval/recommender implementation.

Next best action:

```text
Implement convert_huegov_culture_raw_to_md.py and generate knowledge-base-hue/_source-dumps/huegov_culture_and_tourism/
```



## Đọc cả các hướng dẫn/link liên quan nếu thực sự cần để hiểu đúng context.

## Đừng bắt đầu bất kỳ công việc nào khác ngoài việc đọc và kiểm tra cấu trúc thư mục. Khi bạn đã đọc xong tất cả, hãy cho tôi biết nếu bạn có thắc mắc trước khi chúng ta bắt đầu.