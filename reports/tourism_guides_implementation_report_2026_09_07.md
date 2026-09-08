# Báo cáo triển khai `tourism_guides.md` ngày 07/09/2026

## Kết luận

Đã biên soạn cẩm nang du lịch Huế tổng quan theo thiết kế và implementation plan được duyệt. `knowledge-base-hue/tourism/tourism_guides.md` là file answer-facing canonical duy nhất cho intent cẩm nang tổng quan; inventory `services/` còn bốn guide chuyên biệt.

Trạng thái hiện hành: **APPROVED** — ngày 07/09/2026, user xác nhận
`tourism_guides.md` đã được reviewer ở terminal khác duyệt.

## Phạm vi thay đổi

- `knowledge-base-hue/tourism/tourism_guides.md`: biên soạn mới cẩm nang tổng quan.
- `knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md`: giảm từ 05 xuống 04 guide chuyên biệt, loại ứng viên cẩm nang trùng intent.
- `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`: từng
  khóa `tourism_guides.md` là cẩm nang tổng quan canonical duy nhất; inventory
  này đã hoàn thành vai trò điều phối và được xóa theo chỉ đạo ngày 07/09/2026.
- `knowledge-base-hue/meta/tourism-research-evidence.md`: thêm section XXXVIII cho 15 URL do người dùng cung cấp, nguồn kiểm chứng độc lập, claim matrix, mâu thuẫn và self-verification.
- `docs/superpowers/specs/2026-09-07-tourism-guides-design.md`: đặc tả đã được người dùng duyệt trước triển khai.
- `docs/superpowers/plans/2026-09-07-tourism-guides-implementation-plan.md`: kế hoạch triển khai đã được người dùng duyệt trước triển khai.

Không sửa entity du lịch, guide chuyên ngành, runtime, active data hoặc `session_prompt/CURRENT_HANDOFF.md`. File handoff được terminal khác cập nhật đồng thời nên được giữ nguyên để tránh ghi đè thay đổi ngoài phạm vi.

## Đối chiếu tiêu chí nghiệm thu

| Tiêu chí | Kết quả | Evidence |
|:---|:---:|:---|
| Đúng outline đã duyệt | PASS | 1 H1, 15 H2, 5 H3; không có lịch trình 3 ngày 2 đêm rút gọn |
| Chunk đứng độc lập | PASS | Mỗi section mở bằng chủ thể Huế, tên khu vực hoặc loại thông tin cụ thể |
| Một canonical cho intent tổng quan | PASS | Tourism inventory sở hữu `tourism_guides.md`; services inventory không còn deliverable trùng |
| Ranh giới liên domain | PASS | Không sao chép bảng vé, danh sách món/quán, lịch lễ hội, lịch biểu diễn hoặc mô tả dài của entity |
| Dữ liệu động | PASS | Giá, giờ, lịch, trạng thái và nhà cung cấp chỉ xuất hiện như hạng mục phải kiểm tra lại |
| Địa giới tháng 09/2026 | PASS | Dùng tên phường/xã hiện hành ở mức cụm; không công bố địa chỉ chi tiết chưa cần thiết |
| Thời tiết và an toàn | PASS | Diễn đạt có điều kiện; yêu cầu kiểm tra dự báo, cảnh báo và trạng thái quản lý trong ngày |
| Nhóm người và khả năng tiếp cận | PASS | Không mặc định xe máy, thể lực hoặc khả năng tiếp cận giống nhau |
| Nội dung cấm trong answer-facing | PASS | Không YAML, source section, URL, wiki-link, đường dẫn repository hoặc thuật ngữ quy trình nội bộ |

## Nguồn và quyết định biên tập

Section XXXVIII của `knowledge-base-hue/meta/tourism-research-evidence.md` lưu toàn bộ provenance. Mười lăm URL do người dùng cung cấp chỉ được dùng để nhận diện intent và cấu trúc nhu cầu. Dữ kiện quan trọng được đối chiếu với Nghị quyết 175/2024/QH15, Nghị quyết 1675/NQ-UBTVQH15, bản đồ hành chính thành phố Huế, cổng thông tin thành phố Huế, Vietnam Tourism, ACV/Cảng hàng không quốc tế Phú Bài và cổng vé của đơn vị quản lý di tích.

Các nhóm dữ liệu bị loại gồm địa giới cũ, mức giá, danh bạ doanh nghiệp, lịch chạy, giờ mở cửa, lịch sự kiện theo năm, claim quảng bá tuyệt đối và lịch trình ghép quá nhiều hướng.

## Lệnh kiểm tra và kết quả

Đã chạy tại `/home/minhhieu/hue_rag`:

```bash
rg -c '^# ' knowledge-base-hue/tourism/tourism_guides.md
rg -c '^## ' knowledge-base-hue/tourism/tourism_guides.md
rg -c '^### ' knowledge-base-hue/tourism/tourism_guides.md
```

Kết quả: `1`, `15`, `5`.

```bash
rg -n '^---$|^## Nguồn dữ liệu|Liên kết nội bộ|\[\[|https?://|utm_source=chatgpt' knowledge-base-hue/tourism/tourism_guides.md
```

Kết quả: không có match.

```bash
rg -n '05 file|5 file|^### [5-9]\.|^[5-9]\. `' knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md
rg -n 'Cẩm nang du lịch Huế\.md|cam-nang-du-lich-hue\.md' knowledge-base-hue/tourism/services/services-research-and-entities-inventory.md
```

Kết quả: không có match; bốn heading guide chuyên biệt mang số 1–4.

```bash
git diff --check
git diff --no-index --check /dev/null <từng-file-trong-phạm-vi>
```

Kết quả: PASS, không phát hiện lỗi whitespace. Các file nội dung hiện là untracked nên kiểm tra `--no-index` được dùng để không bỏ sót.

## Trạng thái xác minh

- Kiểm tra nội dung và định dạng của implementer: hoàn tất.
- Runtime test: không áp dụng; thay đổi chỉ gồm Markdown và inventory nghiên cứu.
- Independent Reviewer gate: user xác nhận đã hoàn tất ở terminal reviewer khác.
- Commit/push: không thực hiện; Git authorization là `none`.
- Known blocker: không có.
