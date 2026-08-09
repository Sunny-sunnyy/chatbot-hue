# Báo cáo triển khai: Phase 2 Foods Markdown Chunking

Người triển khai: DeepSeek
Ngày: 2026-08-09
Bản hiện trạng sau khi sửa theo Codex review. Các số liệu lịch sử được ghi rõ trong phần riêng.

## Mục tiêu và phạm vi được duyệt

Chuyển dữ liệu foods đã curate thành các đoạn nội dung (chunk) ổn định, answer-facing, có metadata đủ để index, truy xuất, trích nguồn và đánh giá ở các phase sau. Thay đổi gần nhất được người dùng phê duyệt trong `guides/phase_2_foods_markdown_chunking.md`: giới hạn phần nội dung thường ở 400 ký tự, giữ nguyên bảng Markdown, thêm nhãn ngữ cảnh ngắn theo quy tắc cố định, không chồng lặp, và sửa cách nhận diện danh sách theo yêu cầu của Codex review.

Phạm vi file: `split_text.py`, `markdown_chunker.py`, `test_markdown_chunker.py`, `notebooks/02_foods_data_and_chunking.ipynb` và file báo cáo này. Không sửa guide, Codex review, user report, `Project_Status.md` hay dữ liệu curated.

## Tóm tắt hiện trạng

- Corpus: 91 file Markdown curated, 454 mục H2 tổng cộng, loại 90 mục `Nguồn dữ liệu`, còn 364 mục dùng để tạo nội dung trả lời.
- Kết quả: 572 đoạn nội dung từ 91 file.
- Giới hạn phần nội dung thường: 400 ký tự (nhãn ngữ cảnh không tính).
- Bảng Markdown: giữ nguyên cả khối, được phép vượt 400 ký tự; 8 bảng trong corpus dài hơn 400, bảng dài nhất 927 ký tự.
- Mỗi đoạn bắt đầu bằng nhãn ngữ cảnh dạng `Tên tài liệu — nhãn ngắn`, tạo theo quy tắc cố định, không gọi mô hình.
- Bảy trường metadata và công thức `chunk_id` giữ nguyên; mã đoạn unique và ổn định qua các lần chạy.
- Kiểm thử: 31 test đạt. Notebook: 16 cells, an toàn, outputs rỗng.

## Files canonical

```text
backend/ingestion/helpers/markdown_parser.py
backend/ingestion/helpers/make_metadata.py
backend/ingestion/helpers/split_text.py
backend/ingestion/chunking/markdown_chunker.py
backend/tests/test_markdown_chunker.py
notebooks/02_foods_data_and_chunking.ipynb
```

## Cách chia nội dung 400 ký tự

`split_text(text, max_chars=...)` trong `backend/ingestion/helpers/split_text.py` giữ chữ ký hiệu cũ, giá trị mặc định mới là `DEFAULT_MAX_CHARS = 400`. Văn bản được tách thành block theo dòng trống trước, sau đó xử lý theo loại block:

- Đoạn văn thường: nếu dài hơn giới hạn, ngắt tại cuối câu gần nhất (sau dấu chấm, chấm than, chấm hỏi); nếu không có dấu câu thì ngắt tại khoảng trắng gần nhất trước giới hạn. Không bao giờ cắt giữa từ; không chồng lặp ký tự giữa hai đoạn liên tiếp.
- Danh sách: một mục gồm dòng bắt đầu bằng dấu danh sách (`-`, `*`, `+` hoặc số) và các dòng xuống hàng thụt lề thuộc chính mục đó. Các dòng này luôn đi cùng nhau; pipeline ưu tiên chia giữa các mục. Chỉ chia bên trong một mục khi riêng mục đó vượt 400 ký tự.
- Bảng Markdown: giữ nguyên cả khối, được phép vượt giới hạn.
- Block không dấu câu và không khoảng trắng (bất khả thi với văn bản thật): giữ nguyên để không phá từ.

## Cách giữ bảng

Một block được nhận diện là bảng khi dòng thứ hai là hàng phân cách `---` (chỉ gồm `|`, `-`, `:`, khoảng trắng và chứa `-`). Bảng là khối nguyên tử: không bao giờ bị cắt. Corpus hiện tại có 24 bảng, trong đó 8 bảng dài hơn 400 ký tự, bảng dài nhất 927 ký tự; toàn bộ được giữ nguyên.

## Cách tạo nhãn ngữ cảnh

`_context_label(subcategory, heading, text)` trong `markdown_chunker.py` trả về nhãn ngắn tiếng Việt theo quy tắc cố định:

- Bảng ánh xạ trực tiếp `_DIRECT_LABELS` phủ toàn bộ 38 loại mục H2 đang dùng: `Tóm tắt` -> `giới thiệu`, `Menu và giá tham khảo` -> `menu`, `Món ăn / trải nghiệm` -> `trải nghiệm`, `Thành phần và đặc điểm` -> `thành phần`, `Cách làm tóm tắt` -> `cách làm`, `Nguồn gốc và bối cảnh` -> `nguồn gốc`, `Địa điểm tiêu biểu` -> `địa điểm`, các mục `food-guides.md` như `Gợi ý ăn sáng` -> `ăn sáng`, `Food tour 1 ngày` -> `tour 1 ngày`, v.v.
- Mục `Thông tin` dùng nhãn cụ thể (`địa chỉ`, `giờ hoạt động`, `mức giá`) khi đoạn chỉ chứa đúng một chủ đề nhận diện được; còn lại dùng `thông tin quán`.
- Mục chưa biết: fallback là tên mục viết thường. Trong corpus hiện tại không mục nào phải dùng fallback.

Đoạn có dạng `"{title} — {label}\n{nội dung}"`. Nhãn không tính vào giới hạn 400 ký tự và không thêm trường metadata mới.

## Metadata contract

Bảy trường giữ nguyên: `chunk_id` (dạng `{source}|{section}|{index}` với index chạy theo file), `source` (đường dẫn tương đối với `knowledge-base-hue/`), `title`, `section`, `category` (`foods`), `subcategory` (folder dưới `foods/`; `food-guides.md` dùng `guide`), `chunk_type` (`section`). Không có trường nào bị thêm, bớt hoặc đổi ý nghĩa.

## Notebook Phase 2

`notebooks/02_foods_data_and_chunking.ipynb` có 16 cells (7 cell mã, 9 cell markdown), viết bằng tiếng Việt, dùng lại các module của backend:

- Giải thích đoạn nội dung là gì, một mục H2 có thể tạo nhiều đoạn, giới hạn 400 ký tự và thứ tự ưu tiên khi ngắt.
- Giải thích dấu `|` và hàng `---` là cú pháp bảng Markdown, và bảng là ngoại lệ được phép dài hơn 400.
- Giải thích nhãn ngữ cảnh theo nhóm dữ liệu; mục danh sách dài hơn 400 ký tự vẫn có thể bị chia nhưng chỉ khi riêng mục đó vượt giới hạn.
- Ba ví dụ đã duyệt: một đoạn văn (`giới thiệu`), một bảng menu hiển thị đúng hàng/cột qua `IPython.display.Markdown`, một đoạn trong `food-guides.md` (`lần đầu`); có ghi độ dài phần nội dung và phân biệt rõ dữ liệu đoạn thật với bản xem trước.
- Cell kiểm tra gate dùng lại `_is_table` và `_split_blocks` từ backend, không chép lại biểu thức nhận diện bảng.

## Kiểm thử

`backend/tests/test_markdown_chunker.py`: 31 test đạt (28 cũ còn phù hợp cộng thêm 3 test mới theo Codex review). Các test phủ: parser, metadata, bỏ dòng ảnh, ngắt tại cuối câu, ngắt tại khoảng trắng cho câu dài, giữ nguyên bảng, chia danh sách giữa mục, giữ nguyên mục danh sách có dòng xuống hàng (tái hiện `foods/local_specialties/banh canh nam pho.md`), ánh xạ nhãn, nhãn `Thông tin` một chủ đề và nhiều chủ đề, fallback nhãn, đoạn có nhãn, không có đoạn thường vượt 400, đoạn không bắt đầu bằng dòng tiếp nối bị tách khỏi mục trước, corpus đủ 91 file, mã đoạn unique và ổn định.

## Lệnh đã chạy

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile ingestion/helpers/markdown_parser.py ingestion/helpers/make_metadata.py ingestion/helpers/split_text.py ingestion/chunking/markdown_chunker.py
# đạt

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q
# 31 passed in 0.39s

UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); print(len(chunks)); print(chunks[0])"
# 572
# {'text': 'ANH KAFE tại Huế — giới thiệu\nANH KAFE là hệ thống ...',
#  'metadata': {'chunk_id': 'foods/cafes/anh kafe hue.md|Tóm tắt|0', ...}}
```

## Kết quả kiểm tra dữ liệu (đo trực tiếp)

```text
tổng số đoạn: 572
theo nhóm: restaurants 249, cafes 162, local_specialties 118, guide 43
độ dài phần nội dung: trung bình 272,8; trung vị 285; lớn nhất 927
đoạn thường vượt 400: 0
bảng vượt 400: 8
số file được xử lý: 91
đoạn rỗng: 0
thiếu metadata: 0
mã đoạn trùng: 0
mã đoạn thay đổi giữa hai lần chạy: 0
đoạn chứa bảng: 24
đoạn thiếu nhãn: 0
loại mục H2 trả lời chưa có quy tắc nhãn: 0
```

Số đoạn 572 so với 571 của lần chạy trước tăng một đoạn do sửa nhận diện danh sách: một mục danh sách có dòng xuống hàng được giữ nguyên thay vì bị tách, làm cách gộp các đoạn trong một file thay đổi.

## Số liệu lịch sử (trước thay đổi, không phải hiện trạng)

Các số liệu sau thuộc bản triển khai cũ và chỉ để đối chiếu; không được dùng làm kết quả hiện tại:

```text
giới hạn phần nội dung: 1.500 ký tự (nay là 400)
tổng số đoạn: 366 (nay là 572)
kiểm thử: 17 (nay là 31)
notebook: 9 cells (nay là 16)
mục H2 khảo sát ban đầu: 908 (sau khi đo lại chính xác là 454 tổng cộng)
```

## Giới hạn còn lại

- Giới hạn 400 vẫn nằm trong module (`DEFAULT_MAX_CHARS`), chưa đưa vào `settings.yaml` vì chưa có nhóm config chunking được phê duyệt. Phase 8 sẽ so sánh 400 với 600 hoặc 800 bằng cùng bộ câu hỏi đánh giá.
- Nhãn `Thông tin` nhận diện chủ đề bằng chuỗi `Địa chỉ`, `Giờ hoạt động`, `Mức giá`; mục viết theo cách khác sẽ rơi vào nhãn chung `thông tin quán`. Đây là giới hạn chấp nhận được của quy tắc cố định, không dùng mô hình.
- Một mục danh sách dài hơn 400 ký tự vẫn bị chia bên trong mục; phần sau không lặp lại dấu danh sách. Trường hợp này chỉ xảy ra khi riêng mục đó vượt giới hạn.
- Số đoạn tăng từ 366 lên 572: Phase 3–8 phải index lại toàn bộ đoạn mới, không tái sử dụng số liệu cũ.

## Tự kiểm tra an toàn

- Bảo mật: không đọc, in, ghi log hoặc phơi bày bí mật; không mở `.env`.
- An toàn dữ liệu: dữ liệu curated chỉ được đọc, không bị sửa; metadata chỉ chứa đường dẫn tương đối.
- Độ ổn định: thứ tự file sorted và xác định; mã đoạn ổn định qua các lần chạy.
- Hiệu năng: một lượt quét cục bộ trên 91 file nhỏ; không tải mô hình, không gọi dịch vụ ngoài.
- Kiểm thử: toàn bộ chạy không cần bí mật, mô hình trả phí, deploy hoặc dịch vụ ngoài.
- Notebook: JSON hợp lệ, outputs rỗng, `execution_count` là `null`, cell mặc định an toàn, dùng lại mã backend.

## Lời khai live access

Không có lời gọi mạng, mô hình, deploy hoặc truy cập bí mật nào trong toàn bộ quá trình triển khai và các lần sửa theo review.

## Bàn giao cho Codex

Codex cần kiểm tra lại trước nhất:

- `split_text.py`: nhận diện mục danh sách gồm dòng dấu danh sách và các dòng xuống hàng; ưu tiên chia giữa mục; chỉ chia trong mục khi mục vượt 400 ký tự.
- `markdown_chunker.py`: bảng ánh xạ nhãn và cách prepend nhãn vào đoạn.
- `backend/tests/test_markdown_chunker.py`: 31 test, trong đó 3 test mới tái hiện `banh canh nam pho.md` (mục `Thành phần và đặc điểm`) và kiểm tra đoạn không bắt đầu bằng dòng tiếp nối bị tách.
- `notebooks/02_foods_data_and_chunking.ipynb`: 16 cells, dùng lại `_is_table`/`_split_blocks` từ backend, ba ví dụ đã duyệt, outputs rỗng, `execution_count` null.
- Kết quả dữ liệu: 572 đoạn, 91 file, đoạn thường không vượt 400, 8 bảng vượt 400 được giữ nguyên, mã đoạn unique và ổn định.

Cách kiểm tra lại:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile ingestion/helpers/markdown_parser.py ingestion/helpers/make_metadata.py ingestion/helpers/split_text.py ingestion/chunking/markdown_chunker.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from ingestion.chunking.markdown_chunker import chunk_foods_markdown; chunks = chunk_foods_markdown(); print(len(chunks)); print(chunks[0])"
```
