# Codex Review: Phase 2 Foods Markdown Chunking

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-09
Review path:

```text
reports/phase_2_foods_markdown_chunking_codex_review.md
```

Implementer report:

```text
reports/phase_2_foods_markdown_chunking_implementation_report.md
```

## Tóm tắt

Phần sửa bổ sung đã đạt yêu cầu kỹ thuật. Danh sách có dòng xuống hàng được
giữ theo đúng mục, bảng Markdown không bị cắt, nội dung thường không vượt 400
ký tự và toàn bộ nội dung nguồn được bảo toàn. Notebook và báo cáo triển khai
đã được cập nhật theo hiện trạng mới.

Phase 2 sẵn sàng để người dùng chạy lại notebook và xác nhận. Đây chưa phải là
phê duyệt cuối cùng và Phase 3 vẫn chưa được mở.

## Phát hiện

Không có lỗi mức blocker hoặc major.

- minor: Notebook dùng một số hàm nội bộ như `_discover_markdown_files`,
  `_is_table` và `_split_blocks` để minh họa. Mã xử lý vẫn nằm trong `backend/`,
  notebook không chép lại thuật toán. Giới hạn này chấp nhận được cho notebook
  học tập của MVP.

## Kiểm tra độc lập

Đã chạy từ `backend/`:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile ingestion/helpers/markdown_parser.py ingestion/helpers/make_metadata.py ingestion/helpers/split_text.py ingestion/chunking/markdown_chunker.py
# đạt

UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q
# 31 passed in 0.25s
```

Kết quả kiểm tra toàn bộ dữ liệu:

- 572 đoạn từ 91 tệp;
- restaurants 249, cafes 162, local_specialties 118, guide 43;
- độ dài phần nội dung: trung bình 272,75, trung vị 285, lớn nhất 927;
- 24 bảng, trong đó 8 bảng vượt 400 ký tự và đều được giữ nguyên;
- không có đoạn thường vượt 400 ký tự;
- không có nội dung rỗng, thiếu metadata, trùng mã đoạn hoặc đường dẫn tuyệt
  đối;
- không có mục `Nguồn dữ liệu` hoặc dòng ảnh trong dữ liệu đầu ra;
- ghép lại nội dung theo từng mục cho kết quả trùng với nội dung gốc sau khi bỏ
  khác biệt khoảng trắng;
- mọi mục danh sách không quá 400 ký tự, gồm cả dòng xuống hàng, đều nằm trọn
  trong một đoạn;
- mã đoạn không đổi giữa hai lần chạy;
- 38 loại tiêu đề dùng để trả lời đều có quy tắc nhãn.

Trường hợp từng bị lỗi đã đạt: đoạn
`foods/local_specialties/banh canh nam pho.md|Thành phần và đặc điểm|2` dài 208
ký tự và chứa cả `Nhân tôm cua` lẫn câu `Phần nhân có màu đỏ gạch`.

Notebook có 16 cell, gồm 7 cell mã. Toàn bộ cell mã chạy được theo thứ tự và
cho 572 đoạn. Tệp lưu trong repo có outputs rỗng và mọi `execution_count` là
`null`. Notebook dùng lại cách nhận diện bảng từ `backend/`; không gọi mạng,
mô hình hoặc dịch vụ ngoài.

`git diff --check` đạt. Quét các tệp trong phạm vi không phát hiện lệnh truy cập
bí mật hoặc gọi dịch vụ ngoài. URL duy nhất được tìm thấy là dữ liệu mẫu trong
một kiểm thử loại dòng ảnh.

## Kiểm tra phạm vi

DeepSeek chỉ sửa năm tệp đã được giao: hai tệp xử lý, một tệp kiểm thử, notebook
Phase 2 và báo cáo triển khai. Không sửa dữ liệu curated, guide, báo cáo Codex,
user report hoặc `Project_Status.md`. Các thay đổi ngoài phạm vi có sẵn trong
worktree không được đưa vào đánh giá.

## An toàn và chất lượng

- Bảo mật: không đọc hoặc in bí mật; không gọi dịch vụ ngoài.
- An toàn dữ liệu: chỉ đọc dữ liệu Foods, không sửa tài liệu nguồn.
- Độ ổn định: thứ tự tệp và mã đoạn ổn định giữa các lần chạy.
- Hiệu năng: xử lý cục bộ một lượt trên 91 tệp, phù hợp với MVP.
- Ảnh hưởng về sau: Phase 3 đến Phase 8 phải lập chỉ mục từ toàn bộ 572 đoạn và
  không dùng lại số liệu 366 đoạn cũ.

## Phần bắt buộc sửa

Không áp dụng.

## Kết luận

Kiểm tra kỹ thuật đã đạt. Báo cáo dành cho người dùng được cập nhật tại:

```text
reports/user_reports/phase_2_foods_markdown_chunking_user_report.md
```

Người dùng cần chạy lại notebook Phase 2 vì cách chia danh sách và tổng số đoạn
đã thay đổi. Chỉ sau khi người dùng xác nhận Phase 1-2, Reviewer mới chuyển
trạng thái sang `approved`, cập nhật `Project_Status.md` và thực hiện bước bàn
giao cuối theo quyền đã được cấp.
