# Project Status

Last updated: `2026-08-06 20:53:45 +07`

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

- `restaurants/`: 56 file curated.
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
- Curate 56 địa điểm trong `foods/restaurants/` từ dữ liệu người dùng cung cấp.

Chưa thực hiện:

- Curate các file trong `foods/local_specialties/`.
- Hoàn thiện `foods/food-guides.md` theo dữ liệu curated.
- Curate đầy đủ các category heritage, festivals, performing_arts, tourism,
  services, tickets và statistics.
- Enrichment có nguồn xác minh.
- Chunking, embedding, indexing, retriever và recommender.

## Cập nhật gần nhất

### 2026-08-06 20:53:45 +07

Thay đổi đã thực hiện:

- Rà soát worktree trước khi commit và push theo yêu cầu người dùng.
- Đồng bộ số lượng curated restaurants trong phần tổng quan từ 55 lên 56.
- Giữ nguyên các thay đổi hiện có của knowledge base, category guides, metadata và session context; không sửa raw data.

Validation đã chạy:

- Kiểm tra branch `main`, remote `origin` và danh sách thay đổi hiện tại.
- Đếm lại `knowledge-base-hue/foods/restaurants/`: 56 file Markdown.
- Kiểm tra không có filename untracked chứa pattern secret phổ biến.
- Validation cấu trúc và `git diff --check` sẽ được chạy lại sau khi stage toàn bộ thay đổi.

Next action đề xuất:

- Commit toàn bộ thay đổi hiện tại và push commit lên `origin/main`.

### 2026-08-06 20:51:02 +07

Thay đổi đã thực hiện:

- Curate `Bánh Canh Nam Phổ O Hằng` tại `foods/restaurants/banh-canh-nam-pho-o-hang.md` từ nội dung người dùng cung cấp.
- Ghi nhận 2 cơ sở, giờ hoạt động, ngày nghỉ định kỳ, mức giá chung, menu bánh Huế và dịch vụ đóng gói theo source `Google`.
- Không đưa rating Google hoặc claim đánh giá cao vào curated content.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên, địa chỉ và nhóm món với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:49:27 +07

Thay đổi đã thực hiện:

- Cập nhật file `foods/restaurants/thuy-banh-canh-nam-pho.md` bằng dữ liệu bổ sung từ Google.
- Bổ sung menu bánh Huế, đồ ăn kèm, mô tả nước dùng và thông tin đóng gói đi xa.
- Giữ riêng hai khoảng giá theo nguồn: `15.000 – 40.000 VNĐ tùy món` từ hue.aeonmall-vietnam.com và `20.000 – 30.000 VNĐ cho món chính` từ Google.
- Không tạo duplicate file và không sửa raw data.

Validation đã chạy:

- Kiểm tra file vẫn có cấu trúc curated Markdown hợp lệ và không có section/claim thiếu nguồn.
- Kiểm tra cả hai nguồn được ghi trong `## Nguồn dữ liệu`.
- Chạy `git diff --check` cho file Thúy và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:43:05 +07

Thay đổi đã thực hiện:

- Curate thương hiệu aggregate `Jollibee tại Huế` tại `foods/restaurants/jollibee-hue.md` từ nội dung người dùng cung cấp.
- Ghi nhận 4 chi nhánh, địa chỉ, giờ hoạt động, số điện thoại, khoảng giá hiển thị, menu, dịch vụ tiệc sinh nhật và giao hàng theo source `Google`.
- Không đưa các claim về thứ hạng, rating hoặc lượng khách vào curated content.
- Hoàn tất validation cho file `Texas Chicken tại Huế` vừa tạo ở batch trước.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo thương hiệu và 4 địa chỉ Jollibee với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown, slug ASCII dạng kebab-case và nội dung file Texas Chicken.
- Chạy `git diff --check` cho các file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:42:29 +07

Thay đổi đã thực hiện:

- Curate `Texas Chicken tại Huế` tại `foods/restaurants/texas-chicken-hue.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ chi nhánh, giờ hoạt động, hotline, không gian, dịch vụ giao hàng và bảng giá theo nhóm món từ source `Google`.
- Diễn đạt các claim về nguyên liệu và trải nghiệm thương hiệu dưới dạng thông tin được giới thiệu, không khẳng định mạnh hơn dữ liệu gốc.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo thương hiệu và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:35:40 +07

Thay đổi đã thực hiện:

- Curate thương hiệu aggregate `Lotteria tại Huế` tại `foods/restaurants/lotteria-hue.md` từ nội dung người dùng cung cấp.
- Ghi nhận 4 chi nhánh, địa chỉ, giờ hoạt động, số điện thoại, khoảng giá hiển thị, menu, dịch vụ giao hàng và combo ăn trưa theo source `Google`.
- Không đưa đánh giá tổng hợp của nền tảng bản đồ vào curated content.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo thương hiệu và 4 địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:30:03 +07

Thay đổi đã thực hiện:

- Curate thương hiệu aggregate `KFC tại Huế` tại `foods/restaurants/kfc-hue.md` từ nội dung người dùng cung cấp.
- Ghi nhận 3 chi nhánh, địa chỉ, giờ hoạt động, số điện thoại chung, dịch vụ giao hàng, thanh toán và menu theo source `Google`.
- Giữ khoảng giá theo từng chi nhánh ở dạng “khoảng giá hiển thị”, không diễn giải thành giá cố định của từng món.
- Không đưa rating hoặc nhận xét tổng hợp chưa có qualifier vào curated content.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo thương hiệu và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:22:09 +07

Thay đổi đã thực hiện:

- Curate `Bánh canh O Bướm` tại `foods/restaurants/banh-canh-o-buom.md` từ nội dung người dùng cung cấp.
- Ghi nhận qualifier địa chỉ `Số 3 hoặc 5 Trịnh Công Sơn`, giờ ăn đêm, khoảng giá, món bánh canh bột lộn và lưu ý di chuyển.
- Không tự bổ sung nguồn web; source tracking trong file ghi `Nội dung người dùng cung cấp`.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên, địa chỉ và khu vực Trịnh Công Sơn với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:22:06 +07

Thay đổi đã thực hiện:

- Curate `Bánh canh O Hoa` tại `foods/restaurants/banh-canh-o-hoa.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ, qualifier hành chính, giờ ăn đêm, khoảng giá, món bánh canh cua – chả và lưu ý di chuyển theo source `Foody.vn`.
- Không gộp quán này với file aggregate `Bánh canh cá lóc Thủy Dương` hoặc `Bánh canh cá lóc Hải Triều` vì khác entity và khác nhóm món.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên, địa chỉ và khu vực Trịnh Công Sơn với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:17:49 +07

Thay đổi đã thực hiện:

- Curate `Bánh canh cá lóc Hải Triều` tại `foods/restaurants/banh-canh-ca-loc-hai-trieu.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ, qualifier hành chính, giờ hoạt động, khoảng giá, lựa chọn sợi bánh và topping theo source `hue.aeonmall-vietnam.com`.
- Giữ nguyên qualifier `phường Phú Hội hoặc phường Xuân Phú` và không tự chọn một đơn vị hành chính duy nhất.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:15:52 +07

Thay đổi đã thực hiện:

- Tạo file aggregate `Bánh canh cá lóc Thủy Dương` tại `foods/restaurants/banh-canh-ca-loc-thuy-duong.md` theo lựa chọn của người dùng.
- Ghi nhận khu vực, qualifier địa lý/hành chính, khoảng giá, thời gian hoạt động thường gặp và đặc trưng món theo source `hue.aeonmall-vietnam.com`.
- Ghi rõ file đại diện cho khu vực, không phải một quán riêng lẻ.
- Không tự xác minh hoặc cập nhật thông tin hành chính ngoài nội dung người dùng cung cấp.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên khu vực và địa danh liên quan với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:12:49 +07

Thay đổi đã thực hiện:

- Curate `Cơm Tấm Okla` tại `foods/restaurants/com-tam-okla.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ, giờ phục vụ cơm tấm, số liên hệ, món ăn, dịch vụ cơm hộp và kênh giao hàng theo source `hue.aeonmall-vietnam.com`.
- Ghi chú riêng hoạt động OKLALA buổi tối tại cùng mặt bằng, không gộp vào menu cơm tấm ban ngày.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 20:10:51 +07

Thay đổi đã thực hiện:

- Curate thương hiệu `Nhà hàng cơm tấm Sài Gòn - Thành Na` tại `foods/restaurants/com-tam-thanh-na.md` từ nội dung người dùng cung cấp.
- Ghi nhận 2 cơ sở, khoảng giá chung, các nhóm món, không gian và kênh giao hàng theo source `hue.aeonmall-vietnam.com`.
- Không đưa các claim quảng bá như “nổi tiếng nhất” hoặc “được đánh giá cao nhất” vào curated content.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên thương hiệu và 2 địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:42:08 +07

Thay đổi đã thực hiện:

- Curate thương hiệu `Bún thịt nướng và nem lụi Bà Tý` tại `foods/restaurants/bun-thit-nuong-ba-ty.md` từ nội dung người dùng cung cấp.
- Ghi nhận 2 cơ sở, giờ hoạt động riêng, không gian, món ăn, giá bún thịt nướng và giá nem lụi theo source `hue.aeonmall-vietnam.com`.
- Không gán giá cho các món không có giá cụ thể trong nội dung cung cấp.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên thương hiệu và 2 địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:41:12 +07

Thay đổi đã thực hiện:

- Curate `Bánh Ướt - Bún Thịt Nướng Huyền Anh` tại `foods/restaurants/banh-uot-bun-thit-nuong-huyen-anh.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ, giờ hoạt động, không gian, mức giá chung và các món được nhắc đến theo source `hue.aeonmall-vietnam.com`.
- Giữ qualifier rằng khoảng giá là mức chung, không gán cho từng món; không đưa rating giao diện vào curated content.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:35:51 +07

Thay đổi đã thực hiện:

- Curate thương hiệu `Hiệu bánh Bảo Thạnh` tại `foods/restaurants/hieu-banh-bao-thanh.md` từ nội dung người dùng cung cấp.
- Ghi nhận 3 cơ sở, các nhóm sản phẩm và kênh đặt hàng theo source Facebook.
- Giữ nguyên qualifier chưa thống nhất của cơ sở Bà Triệu: `Số 167 hoặc khu vực đường Bà Triệu`.
- Không đưa rating hoặc khoảng giá hiển thị vào curated content vì không có thông tin giá chi tiết theo món.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên thương hiệu và các địa chỉ được cung cấp với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:33:30 +07

Thay đổi đã thực hiện:

- Curate thương hiệu `Mè xửng Thuận Hưng` tại `foods/restaurants/me-xung-thuan-hung.md` từ nội dung người dùng cung cấp.
- Ghi nhận cửa hàng trưng bày, xưởng sản xuất, giờ hoạt động, thông tin liên hệ, khoảng giá và các dòng sản phẩm.
- Giữ khoảng giá ở mức thương hiệu chung, không gán giá cho từng sản phẩm.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên thương hiệu và các địa chỉ được cung cấp với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:32:44 +07

Thay đổi đã thực hiện:

- Curate thương hiệu `Mè xửng Nam Thuận` tại `foods/restaurants/me-xung-nam-thuan.md` từ nội dung người dùng cung cấp.
- Ghi nhận trụ sở sản xuất, cơ sở 2, cửa hàng phân phối, giờ hoạt động được cung cấp, khoảng giá và các sản phẩm đặc trưng.
- Không nâng các claim quảng bá như “lâu đời nhất” hoặc “giá tốt nhất” thành factual claim trong curated content.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên thương hiệu và các địa chỉ được cung cấp với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:30:03 +07

Thay đổi đã thực hiện:

- Curate thương hiệu `Mè xửng Thiên Hương` tại `foods/restaurants/me-xung-thien-huong.md` từ nội dung người dùng cung cấp.
- Ghi nhận 3 cơ sở/điểm bán, giờ hoạt động, sản phẩm mè xửng và các đặc sản được phân phối.
- Giữ nguyên conflict địa chỉ của điểm bán Trần Thúc Nhẫn: `230 Hùng Vương` theo phần hiển thị và `18 Trần Thúc Nhẫn` theo phần chi tiết.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên thương hiệu và các địa chỉ được cung cấp với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:28:26 +07

Thay đổi đã thực hiện:

- Curate `Nhà hàng cơm niêu Vỹ Dạ Xưa` tại `foods/restaurants/com-nieu-vy-da-xua.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ, giờ hoạt động, khoảng giá, cơm niêu, các món được nhắc đến và mô tả không gian theo source `hue.aeonmall-vietnam.com`.
- Không sửa các file Đông Ba hoặc Ba Bự vì phần nội dung tương ứng trong input là dữ liệu lặp lại.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:22:10 +07

Thay đổi đã thực hiện:

- Curate `Chè Hẻm Huế` tại `foods/restaurants/che-hem-hue.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ, giờ hoạt động, giá chung theo ly, các món chè được bài viết gợi ý và lưu ý trải nghiệm theo source `hue.aeonmall-vietnam.com` ngày 05/12/2025.
- Không gán giá chung cho từng món và không đưa caption ảnh lặp vào curated content.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:19:55 +07

Thay đổi đã thực hiện:

- Curate `Bánh Mì Ba Bự` tại `foods/restaurants/banh-mi-ba-bu.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ, các lựa chọn bánh mì, không gian, hình thức phục vụ và hoạt động cộng đồng theo source `hue.aeonmall-vietnam.com`.
- Không đưa rating hoặc khoảng giá hiển thị vào curated content vì chưa có thông tin chi tiết về nền tảng và giá từng món.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:17:37 +07

Thay đổi đã thực hiện:

- Curate thương hiệu `Bánh mì Đông Ba` tại `foods/restaurants/banh-mi-dong-ba.md` từ nội dung người dùng cung cấp.
- Ghi nhận năm khởi nguồn được cung cấp, 5 cơ sở, giờ hoạt động tổng quát, mức giá và đặc trưng bánh mì theo source `hue.aeonmall-vietnam.com`.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên thương hiệu và 5 địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:15:29 +07

Thay đổi đã thực hiện:

- Curate `Bánh mì Trường Tiền O Tho` tại `foods/restaurants/banh-mi-truong-tien-o-tho.md` từ nội dung người dùng cung cấp.
- Ghi nhận cơ sở chính, cơ sở khác, hai ca hoạt động, mức giá, nhân bánh, đồ uống và hình thức giao hàng theo source `hue.aeonmall-vietnam.com`.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên thương hiệu và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

### 2026-08-06 19:11:30 +07

Thay đổi đã thực hiện:

- Curate `Thúy - Bánh canh Nam Phổ` tại `foods/restaurants/thuy-banh-canh-nam-pho.md` từ nội dung người dùng cung cấp.
- Ghi nhận địa chỉ, giờ hoạt động, mức giá, món ăn, đồ uống và thông tin đóng gói theo source `hue.aeonmall-vietnam.com`.
- Không sửa raw data hoặc các restaurant Markdown có sẵn.

Validation đã chạy:

- Kiểm tra duplicate theo tên, loại món và địa chỉ với các file trong `foods/restaurants/`.
- Kiểm tra cấu trúc Markdown và slug ASCII dạng kebab-case.
- Chạy `git diff --check` cho file mới và file trạng thái.

Next action đề xuất:

- Tiếp tục curate địa điểm tiếp theo khi người dùng cung cấp dữ liệu có nguồn.

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
