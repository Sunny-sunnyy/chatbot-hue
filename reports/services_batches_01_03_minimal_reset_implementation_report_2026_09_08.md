# Báo cáo triển khai thiết kế lại bốn cẩm nang dịch vụ du lịch Huế

Ngày thực hiện: 08/09/2026
Người thực hiện: Codex
Base commit: `8739744feabe6574d8bd6d1a9bf1664521dad0fa`
Git authorization: none
Sub-agent authorization: none

## 1. Phạm vi

Đợt triển khai viết lại bốn cẩm nang:

1. `knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md`;
2. `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md`;
3. `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md`;
4. `knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md`.

Mục XL–XLIII của `knowledge-base-hue/meta/tourism-research-evidence.md` được
viết lại để khớp bốn cẩm nang. Công việc tuân theo written spec và
implementation plan đã được người dùng duyệt.

Không sửa inventory, canonical liên domain, ingestion, Golden, Qdrant hoặc
runtime. Không commit hoặc push.

## 2. Nội dung đã thay đổi

### Cẩm nang chọn điểm đến

Tài liệu được rút từ dạng toplist 286 dòng xuống cấu trúc lựa chọn theo thời
gian, sở thích, nhóm khách, thời tiết và năm cụm địa lý. Mô tả lịch sử, kiến
trúc, món ăn, xếp hạng và lời quảng bá đã được loại bỏ.

Bạch Mã chỉ còn bước liên hệ Ban quản lý trước khi lập kế hoạch. SUP trên sông
Hương chỉ giữ ba yêu cầu được nguồn Hue-S hỗ trợ: áo phao, thiết bị cứu sinh và
tránh luồng tàu du lịch.

### Cẩm nang lịch trình ngắn ngày

Tài liệu chỉ giữ lịch trình nửa ngày, một ngày và hai ngày một đêm. Toàn bộ
khung được trình bày theo đầu, giữa hoặc cuối buổi; không còn giờ đồng hồ cố
định. Các biến thể ga Huế, sân bay Phú Bài và Đà Nẵng chỉ nêu khác biệt ảnh
hưởng đến tuyến.

Các khẳng định về bãi đỗ, bậc cấp, nền đường và xe điện đã được thay bằng bước
liên hệ đơn vị quản lý khi nhóm có nhu cầu tiếp cận đặc thù.

### Cẩm nang ba ngày hai đêm

Tài liệu có một lịch trình chính và ba module thay thế. Ngày đầu dành cho
Phú Xuân–Thuận Hóa, ngày thứ hai cho Kim Long–Thủy Xuân và ngày cuối chọn một
nhánh nhẹ thuận đường rời Huế.

Bạch Mã không nằm trong lịch trình hoặc module. Tài liệu không còn tuyến cụ
thể, giá xe hoặc khẳng định đường lên đỉnh đang hoạt động. Hồ Thủy Tiên được mô
tả theo trạng thái quản lý và chỉnh trang, không phải công viên bỏ hoang.

### Cẩm nang chi phí

Tài liệu được rút từ 302 dòng xuống còn 146 dòng. Giá Ca Huế, thuyền riêng,
hướng dẫn viên, taxi từng chặng, xe thuê ngoại thành, cổ phục và giá nhà cung
cấp cụ thể đã bị loại bỏ.

Tài liệu chỉ giữ hai mẫu giá lưu trú, một mẫu chi ăn uống và ba bảng hạn mức
lập kế hoạch. Giá vé từng điểm không xuất hiện; khoản tham quan chỉ là dự toán
tổng và người đọc được hướng sang cẩm nang vé.

## 3. Nguồn và phương pháp đối chiếu

Việc đối chiếu được thực hiện bằng websearch tiếng Việt và mở trang hoặc tài
liệu trực tiếp vào ngày 08/09/2026. Không có khảo sát tại chỗ.

Các nguồn chính gồm:

- Nghị quyết 1675/NQ-UBTVQH15 cho địa giới có hiệu lực từ ngày 01/07/2025;
- Báo Văn Hóa và Cổng tương tác thành phố Huế cho sạt lở Km12 tại Bạch Mã;
- phản hồi của Công an thành phố Huế trên Cổng tương tác cho an toàn SUP;
- quy chế của thành phố và Công báo năm 2025 cho quản lý Ca Huế;
- Tổng công ty Đường sắt Việt Nam cho địa chỉ Ga Huế;
- thông báo quy hoạch cùng phản hồi của cơ quan thành phố cho Hồ Thủy Tiên;
- bài tổng hợp chi phí của AEON MALL Huế ngày 12/05/2026 và bài khảo sát thương
  mại VuiVivu Đà Nẵng để đặt, đối chiếu độ lớn của hạn mức;
- Nghị quyết 55/2025/NQ-HĐND cho trần khoản dự toán tham quan.

Mục XL–XLIII chỉ dùng URL tới trang hoặc tài liệu cụ thể. Trang chủ website và
nguồn không khớp phạm vi đã bị loại bỏ.

## 4. Lệnh đã chạy và kết quả quan sát

### Kích thước và cấu trúc

Lệnh `wc -l` ghi nhận số dòng lần lượt là 159, 167, 181 và 146. Evidence có
1892 dòng sau khi thay bốn mục cuối.

Đếm heading cho bốn cẩm nang lần lượt là:

- `1 H1 / 6 H2 / 18 H3`;
- `1 H1 / 8 H2 / 20 H3`;
- `1 H1 / 9 H2 / 26 H3`;
- `1 H1 / 8 H2 / 11 H3`.

### Nội dung bốn cẩm nang

Lệnh `rg` kiểm tra URL ngoài, wiki-link, tên file có đuôi `.md`, frontmatter,
mục nguồn nội bộ, mã định danh kỹ thuật và nhãn kiểm thử không tìm thấy kết
quả trong bốn cẩm nang.

Lệnh kiểm tra giờ đồng hồ cố định không tìm thấy kết quả trong ba cẩm nang lựa
chọn và lịch trình. Lệnh kiểm tra các tuyến Bạch Mã cũ, khẳng định tiếp cận cũ và
mỹ từ quảng bá cũng không tìm thấy kết quả.

### Phép cộng ngân sách

Reviewer dùng `awk` cộng riêng từng cận. Kết quả thu được:

```text
1 ngày: 280–850; 850–1700; 1800–3400
2 ngày 1 đêm: 710–1700; 1600–3250; 3450–6800
3 ngày 2 đêm: 1140–2650; 2550–5050; 5350–10800
```

Các kết quả khớp ba bảng, đơn vị nghìn đồng mỗi người và chưa gồm chi phí đến,
rời Huế.

### Định dạng

`git diff --check` trả exit 0 và không có output. Lệnh này chỉ kiểm tra thay đổi
tracked, không bao phủ các guide và evidence đang untracked.

Các lệnh no-index được chạy riêng với đường dẫn đầy đủ của từng guide và
evidence. Chúng trả exit 1 vì file khác `/dev/null`, không có output chẩn đoán
whitespace. Đây không phải exit 0 nhưng không phát hiện lỗi whitespace.

## 5. Phần chưa xác minh và giới hạn

- Websearch không tìm thấy thông báo trực tiếp mới hơn tháng 06/2026 xác nhận
  mở lại tuyến lên đỉnh Bạch Mã. Vì vậy tài liệu giữ cách xử lý thận trọng và
  không đưa tuyến vào lịch trình.
- Không gọi điện hoặc gửi email cho Vườn quốc gia, Cảng vụ, điểm tham quan hoặc
  nhà cung cấp.
- Các hạn mức đi lại, trải nghiệm, mua sắm và dự phòng là khoản tự phân bổ để
  lập kế hoạch, không phải báo giá thị trường.
- Giá lưu trú và ăn uống là mẫu tại ngày truy cập; người đọc vẫn phải kiểm tra
  báo giá thực tế.
- Không có exact base diff cho các file untracked; việc kiểm tra dựa trên toàn
  bộ nội dung hiện hành.

## 6. Quyền và bước tiếp theo

Công việc được thực hiện trực tiếp trong current worktree theo quyền người dùng
đã cấp. Không dùng sub-agent, không commit, không push và không sửa dữ liệu
đang hoạt động.

Bước tiếp theo là một lượt review độc lập đối với bốn cẩm nang, Mục XL–XLIII,
written spec, implementation plan và báo cáo này. Người thực hiện không tự đưa
ra quyết định nghiệm thu.
