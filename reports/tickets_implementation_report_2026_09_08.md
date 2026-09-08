# Implementation Report: Du lịch Huế - Nhánh vé tham quan và trải nghiệm (Tickets)

Implementer: Implementer (Gemini 3.8 Flash High & Sub-agents)
Date: 2026-09-08
Canonical guide:

```text
knowledge-base-hue/tourism/tickets/tickets-research-and-entities-inventory.md
```

## 1. Phạm vi

Thực hiện đầy đủ nhiệm vụ được giao trong `session_prompt/CURRENT_HANDOFF.md` và `tickets-research-and-entities-inventory.md`:
- Biên soạn đầy đủ 05 file answer-facing trong thư mục `knowledge-base-hue/tourism/tickets/`:
  1. `Hướng dẫn mua và sử dụng vé du lịch Huế.md`
  2. `Vé tham quan Quần thể Di tích Cố đô Huế.md`
  3. `Vé tham quan Hải Vân Quan.md`
  4. `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`
  5. `Vé các điểm tham quan và trải nghiệm khác ở Huế.md`
- Cập nhật hồ sơ kiểm chứng đối chiếu độc lập (evidence) cho 05 file vé vào `knowledge-base-hue/meta/tourism-research-evidence.md` (mục XLIV đến XLVIII).
- Tuyệt đối không can thiệp các file ngoài phạm vi (không sửa 04 guide services, không sửa `heritages/`, `performing_arts/`, `tourism/` entity, không tự ý di chuyển thư mục sang `travel/`).
- Được user cấp phép sử dụng 05 sub-agent chuyên trách để thực hiện song song việc nghiên cứu nguồn URL, tìm kiếm web đối chiếu dữ liệu hiện hành (tháng 09/2026) và tự kiểm tra (self-check).

## 2. Thay đổi chính

- **05 file cẩm nang vé answer-facing mới được tạo**:
  + `knowledge-base-hue/tourism/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md`: Hướng dẫn tổng quan cách phân loại vé (vé lẻ, vé tuyến gộp, vé suất diễn, vé khách lẻ, thuê nguyên thuyền rồng, vé vào cổng khu du lịch, gói trải nghiệm); phân biệt rạch ròi giữa phí nhà nước, giá dịch vụ đơn vị sự nghiệp, giá niêm yết của doanh nghiệp và giá tour đại lý; hướng dẫn quy trình 5 bước mua và sử dụng vé điện tử e-ticket qua cổng chính thức `eticket.hueworldheritage.org.vn`, điều khoản thanh toán, chính sách không đổi/hoàn vé và xử lý hoàn tiền lỗi kỹ thuật; lưu ý sự không đồng nhất về quy chuẩn trẻ em giữa các điểm đến và lưu ý địa giới hành chính 40 xã/phường mới của thành phố Huế.
  + `knowledge-base-hue/tourism/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md`: Khóa toàn bộ hệ thống mức thu phí tham quan 12 điểm di tích theo văn bản pháp lý cấp 1 đang có hiệu lực - Nghị quyết số 55/2025/NQ-HĐND (áp dụng thống nhất khách Việt Nam và quốc tế); biểu phí vé lẻ người lớn và trẻ em 7–12 tuổi; chi tiết 07 tuyến vé gộp (03 tuyến 2 điểm, 03 tuyến 3 điểm, tuyến 4 điểm 530.000đ/100.000đ thời hạn 02 ngày - cảnh báo rõ không phải vé tất cả di tích, tuyến tất cả điểm 600.000đ/120.000đ thời hạn 05 ngày); quy định miễn giảm 50% và 100%; các ngày mở cửa miễn phí cho công dân Việt Nam (19/8, 2/9, Tết, 26/3, 23/11); cập nhật địa giới hành chính 12 di tích theo các phường Phú Xuân, Long Hồ, Thủy Xuân, Thuận Hóa, An Cựu; cảnh báo Hải Vân Quan không thuộc hệ thống này.
  + `knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md`: Khóa căn cứ pháp lý Nghị quyết số 05/2026/NQ-HĐND ngày 22/05/2026 (hiệu lực từ 02/06/2026); mức thu 70.000 đồng/người/lượt; thời hạn áp dụng thí điểm 3 năm đến hết 31/12/2028 trong chu kỳ luân phiên do TP Huế trực tiếp quản lý; giảm 50% cho cư dân TP Huế và TP Đà Nẵng; miễn phí trẻ em dưới 13 tuổi (hoặc dưới 1,3m - phân biệt rõ với ngưỡng 7–12 tuổi của di tích Huế); miễn phí các ngày lễ lớn (30/4, 1/5, 2/9, 23/11, Tết); cơ chế bán vé quét mã QR và camera AI đếm lượt khách tự động; khẳng định Hải Vân Quan độc lập và không nằm trong vé combo di tích Cố đô.
  + `knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`: Chuẩn hóa căn cứ pháp lý cấp 1 mới nhất - Quyết định số 104/2025/QĐ-UBND ngày 14/10/2025 của UBND thành phố Huế ban hành Quy chế quản lý biểu diễn Ca Huế (hiệu lực từ 25/10/2025, thay thế QĐ 24/2024); giá vé Nhã nhạc tại Nhà hát Duyệt Thị Đường 300.000 đồng/suất (kèm cảnh báo bắt buộc phải có vé vào cửa Đại Nội 200.000 đồng); các suất diễn định kỳ miễn phí trong Đại Nội (Đại Nhạc Thế Miếu, Tiểu Nhạc Thái Hòa, Ca Huế Nhật Thành Lâu, Lễ Đổi Gác); giá vé khách lẻ Ca Huế trên sông Hương (100.000–130.000đ/150.000đ); thuê nguyên thuyền rồng đơn/đôi (1.200.000–2.500.000đ); du thuyền cao cấp Azerai La Residence (Moon River, Long Giang); quy chuẩn an toàn áo phao, camera giám sát 7 ngày và cảnh báo bản chất giá thương mại của các nhà thuyền.
  + `knowledge-base-hue/tourism/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md`: Khóa giá vé vào cổng Vườn quốc gia Bạch Mã (60.000đ/20.000đ) kèm giá xe 16 chỗ trung chuyển lên đỉnh và cập nhật cảnh báo sạt lở Km12 tuyến đường lên đỉnh; phân định KDL Bạch Mã Village là điểm tư nhân độc lập (vé 100k-120k); biểu giá tắm khoáng, trò chơi mạo hiểm Zipline/Highwire và các gói combo tại Khu suối khoáng Alba Thanh Tân (230k-500k); Không gian lưu niệm Lê Bá Đảng (giờ mở cửa, vé chuẩn 200k, vé người Huế 120k-150k); Tuyến xe buýt 2 tầng City Sightseeing Huế (Night tour, 4h, 24h, 48h kèm cảnh báo không gồm vé vào cổng di tích); dịch vụ xe điện Hoàng Thành, Audio Guide cầm tay, VR "Đi tìm hoàng cung đã mất" trong Đại Nội; Trung tâm nghệ thuật số Sốnglab (170-172 Bà Triệu, phường Thuận Hóa).
- **Hồ sơ nghiên cứu đối chiếu**:
  + Cập nhật các mục XLIV, XLV, XLVI, XLVII, XLVIII vào `knowledge-base-hue/meta/tourism-research-evidence.md` với đầy đủ bảng nguồn trực tiếp, URL kiểm chứng, ngày nguồn, ngày truy cập (08/09/2026), tính ổn định và quyết định biên tập.

## 3. Cách đã chạy thật

1. Khởi chạy 05 sub-agent chuyên trách (`invoke_subagent` theo sự cho phép của user) để đọc sâu toàn bộ các URL do user chỉ định, kết hợp tìm kiếm web bằng tiếng Việt để đối chiếu dữ liệu động tại mốc tháng 09/2026:
   - Trích xuất toàn văn Nghị quyết 55/2025/NQ-HĐND và Nghị quyết 05/2026/NQ-HĐND.
   - Trích xuất toàn văn Quyết định 104/2025/QĐ-UBND từ Công báo TP Huế Số 59/2025.
   - Phân tích file kỹ thuật `Ticket_purchase_guide.pdf` của Trung tâm Bảo tồn Di tích Cố đô Huế.
   - Phân tích các điều khoản giao dịch từ mã nguồn JavaScript của cổng `eticket.hueworldheritage.org.vn`.
   - Đối chiếu địa giới hành chính theo Nghị quyết số 1675/NQ-UBTVQH15 (40 xã/phường mới của TP Huế từ 01/07/2025).
2. Kiểm tra tính tuân thủ quy chuẩn định dạng answer-facing trên cả 05 file:
   - Kiểm tra H1: Duy nhất 01 H1 khớp chính xác tên file.
   - Kiểm tra frontmatter: Không có YAML frontmatter.
   - Kiểm tra liên kết ngoài: Không có URL `http://` hay `https://` trong bài viết.
   - Kiểm tra liên kết nội bộ: Không có wiki-link `[[...]]`, không có đuôi file `.md`.
   - Kiểm tra metadata: Không có metadata RAG, mã claim, mã finding, trạng thái kiểm thử.
3. Chạy kiểm tra định dạng và khoảng trắng trên kho mã:
   - `git status --short`
   - `git diff --check`
   - `git diff --no-index --check /dev/null <untracked_file>` trên cả 05 file mới tạo.

## 4. Kết quả quan sát

- **Cấu trúc thư mục**: Thư mục `knowledge-base-hue/tourism/tickets/` hiện có đúng 05 file answer-facing và 01 file inventory điều phối `tickets-research-and-entities-inventory.md`.
- **Độ chính xác dữ liệu**:
  + Địa giới hành chính: Đã rà soát và điều chỉnh triệt để các địa danh cũ (phường Phú Hội cũ đã được cập nhật chuẩn xác thành phường Thuận Hóa; Bến Tòa Khâm, Sốnglab, Kiosk City Sightseeing đều thuộc phường Thuận Hóa; Đại Nội thuộc phường Phú Xuân).
  + Biểu phí di tích: Khớp 100% Nghị quyết 55/2025/NQ-HĐND; tuyến 4 điểm và tuyến tất cả điểm được định danh rành mạch; phân định rõ với Hải Vân Quan.
  + Hải Vân Quan: Khớp 100% Nghị quyết 05/2026/NQ-HĐND; làm rõ chu kỳ thí điểm đến hết 31/12/2028 và ngưỡng trẻ em dưới 13 tuổi được miễn phí.
  + Ca Huế và sông Hương: Cập nhật văn bản mới nhất Quyết định 104/2025/QĐ-UBND; phân biệt rạch ròi vé Duyệt Thị Đường, các suất miễn phí trong Đại Nội, vé ghép lẻ, thuê nguyên thuyền rồng và du thuyền Azerai.
  + Điểm tham quan khác: Đầy đủ thông tin về VQG Bạch Mã (cảnh báo sạt lở Km12), Bạch Mã Village, Alba Thanh Tân, Không gian Lê Bá Đảng, xe buýt 2 tầng, xe điện/Audio Guide/VR Đại Nội, Sốnglab.
- **Kết quả kiểm tra Git và Whitespace**:
  + `git diff --check` trả về mã thoát 0 (sạch sẽ).
  + `git diff --no-index --check /dev/null` cho cả 05 file untracked trả về output chẩn đoán hoàn toàn rỗng (mã thoát 1 thuần túy do khác biệt nội dung với `/dev/null`, không có bất kỳ lỗi trailing whitespace nào sau khi đã dọn dẹp các khoảng trắng thừa ở dòng 14 của file Hải Vân Quan và dòng 52, 131 của file Điểm khác).

## 5. Lỗi và giới hạn

Không có lỗi hoặc giới hạn kỹ thuật trong phạm vi này.
- Mức giá thương mại của các nhà thuyền Ca Huế, xe buýt 2 tầng, KDL Bạch Mã Village, Alba Thanh Tân và Sốnglab là giá niêm yết tại thời điểm khảo sát tháng 09/2026; cẩm nang đã khuyến cáo người đọc xác nhận lại trước ngày đi.
- Tình trạng tuyến đường lên đỉnh VQG Bạch Mã (sạt lở Km12) có thể thay đổi sau các đợt thi công hoặc mưa lũ; cẩm nang đã cung cấp hotline Ban quản lý (0234.3871330) để du khách chủ động liên hệ.

## 6. Handoff cho Reviewer

- **Tài liệu Reviewer nên đọc trước**:
  1. `knowledge-base-hue/tourism/tickets/tickets-research-and-entities-inventory.md` (khung thiết kế và tiêu chí nghiệm thu đã chốt).
  2. 05 file answer-facing trong `knowledge-base-hue/tourism/tickets/`.
  3. Hồ sơ kiểm chứng mới bổ sung tại các mục XLIV – XLVIII trong `knowledge-base-hue/meta/tourism-research-evidence.md`.
- **Lệnh kiểm tra định dạng nên chạy lại**:
  ```bash
  git status --short
  git diff --check
  git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Hướng dẫn mua và sử dụng vé du lịch Huế.md"
  git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé tham quan Quần thể Di tích Cố đô Huế.md"
  git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé tham quan Hải Vân Quan.md"
  git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md"
  git diff --no-index --check /dev/null "knowledge-base-hue/tourism/tickets/Vé các điểm tham quan và trải nghiệm khác ở Huế.md"
  ```
- **Trạng thái Git**: Không có thao tác commit/push nào được thực hiện theo đúng `Git authorization: none`.
