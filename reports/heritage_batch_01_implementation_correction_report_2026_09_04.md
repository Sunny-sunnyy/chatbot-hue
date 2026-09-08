# Báo cáo Thực thi và Hiệu chỉnh Đợt 01 Miền Di sản (Heritage Batch 01 Correction Report)

- **Vai trò:** Implementer
- **Ngày thực hiện:** `04/09/2026` (`Asia/Bangkok`, UTC+7)
- **Căn cứ điều phối:** Nhận xét tại `knowledge-base-hue/heritage/heritage-batch-01-codex-review-2026-09-04.md`
- **Chỉ đạo trực tiếp của người dùng:** 
  1. Tự nghiên cứu, web search và kiểm chứng độc lập lại toàn bộ các nhận xét của Reviewer trước khi sửa; không tin 100% vào Reviewer.
  2. Giữ nguyên tiền tố số thứ tự trước tên file (`1 ` đến `9 `) để tiện theo dõi tiến độ công việc đã hoàn thành.
  3. Lập báo cáo chi tiết về các nội dung đã xác thực, các thay đổi và kết quả research độc lập.

---

## 1. Tóm tắt kết quả nghiên cứu và kiểm chứng độc lập (Self-Research & Fact-Checking)

Implementer đã sử dụng các công cụ tra cứu web, đối chiếu văn bản quy phạm pháp luật, hồ sơ di sản quốc tế (UNESCO, MOWCAP) và các cổng thông tin chính thức của cơ quan nhà nước để kiểm tra từng finding của Reviewer:

### 1.1. Địa giới hành chính năm 2026 tại Cố đô Huế
- **Kết quả xác minh:** Reviewer nhận định hoàn toàn chính xác. 
  - Ngày 30/11/2024, Quốc hội khóa XV đã thông qua **Nghị quyết số 175/2024/QH15** về việc thành lập thành phố Huế trực thuộc Trung ương (có hiệu lực từ **01/01/2025**). Do đó, kể từ 01/01/2025, đơn vị hành chính là "thành phố Huế", không còn là "tỉnh Thừa Thiên Huế".
  - Ngày 16/06/2025, Ủy ban Thường vụ Quốc hội ban hành **Nghị quyết số 1675/NQ-UBTVQH15** về sắp xếp các đơn vị hành chính cấp xã của thành phố Huế năm 2025 (hiệu lực từ **01/07/2025**), tổ chức lại thành 40 xã, phường mới:
    - Các phường cũ Long Hồ, Hương Long, Kim Long sáp nhập thành **phường Kim Long**.
    - Các phường/xã cũ Thủy Biều, Thủy Bằng, Thủy Xuân sáp nhập thành **phường Thủy Xuân**.
    - Các phường cũ Gia Hội, Phú Hậu, Tây Lộc, Thuận Lộc, Thuận Hòa, Đông Ba sáp nhập thành **phường Phú Xuân**.
    - Các phường cũ Phú Hội, Phú Nhuận, Phường Đúc, Vĩnh Ninh, Phước Vĩnh, Trường An sáp nhập thành **phường Thuận Hóa**.
    - Các xã cũ Hương Xuân, Hương Chữ, Hương Toàn sáp nhập thành **phường Kim Trà** (chứa làng bún Vân Cù).
    - Các xã/phường cũ Thủy Dương, Thủy Phương, Thủy Thanh sáp nhập thành **phường Thanh Thủy** (chứa cầu ngói Thanh Toàn).
    - Các xã/phường cũ Hương Phong, Hương Vinh, Quảng Thành sáp nhập thành **phường Hóa Châu** (chứa làng Địa Linh).
    - Xã Quảng Vinh sáp nhập vào **xã Đan Điền** (chứa làng bún Ô Sa).
- **Hành động:** Đã cập nhật triệt để trên toàn bộ 9 file Markdown và file research evidence.

### 1.2. Quyết định công nhận Bảo vật quốc gia
- **Kết quả xác minh:**
  - **Mộc bản triều Nguyễn:** Kiểm tra văn bản Quyết định số 2599/QĐ-TTg ngày 30/12/2013 và danh mục Bảo vật quốc gia chính thức của Cục Di sản văn hóa. Xác nhận: Khối tài liệu Mộc bản triều Nguyễn là Di sản tư liệu thế giới của UNESCO (2009), **không có tên trong danh mục Bảo vật quốc gia** theo QĐ 2599/QĐ-TTg. Nhận xét của Reviewer là đúng -> Đã xóa bỏ hoàn toàn bullet này ở File 3.
  - **Cửu Đỉnh Huế:** File cũ ghi "Quyết định 2599/QĐ-TTg ngày 30/12/2012". Kiểm tra văn bản chính thức của Thủ tướng Chính phủ: Quyết định đúng là **Quyết định số 1426/QĐ-TTg ngày 01/10/2012** công nhận đợt 1 Bảo vật quốc gia cho "Bộ Cửu Đỉnh (gồm 9 chiếc)" -> Đã sửa chuẩn xác văn bản và ngày ban hành ở File 6.

### 1.3. Lịch sử Cửu Đỉnh và danh sách hoàng đế
- **Kết quả xác minh:**
  - Trong file cũ ghi Dụ Đỉnh ứng với vua Hàm Nghi, Huyền Đỉnh ứng với vua Duy Tân. Đối chiếu sử liệu (*Khâm định Đại Nam hội điển sự lệ*) và tài liệu Bảo tàng Lịch sử Quốc gia: Khi đúc Cửu Đỉnh (1835-1837), vua Minh Mạng đặt Cao Đỉnh ứng với vua Gia Long, Nhân Đỉnh ứng với chính mình, 7 đỉnh còn lại để dự phòng cho các hoàng đế kế nghiệp. Về sau các vua Thiệu Trị, Tự Đức, Kiến Phúc, Đồng Khánh, Khải Định được đưa vào thờ tại Thế Miếu gắn với các đỉnh tương ứng; còn Dụ Đỉnh và Huyền Đỉnh vẫn là hai đỉnh dự phòng, chưa từng được triều đình gán cho vua Hàm Nghi hay Duy Tân. Nhận xét của Reviewer là chính xác -> Đã xóa bỏ hoàn toàn sự gán ghép sai lệch này.
  - Cấp ghi danh: Được ghi danh vào Danh mục Di sản tư liệu khu vực Châu Á – Thái Bình Dương thuộc Chương trình Ký ức Thế giới của UNESCO (MOWCAP) ngày 08/05/2024 tại Ulaanbaatar (Mông Cổ) với tên *Những bản đúc nổi trên chín đỉnh đồng ở Hoàng cung Huế*.
  - Số lượng: Mỗi đỉnh có 18 ô (17 ô hình tượng + 1 ô khắc tên đỉnh gồm 2 chữ Hán) = 162 ô bản đúc nổi. Đã điều chỉnh mô tả rõ ràng.

### 1.4. Thơ văn trên kiến trúc cung đình Huế
- **Kết quả xác minh:**
  - Hồ sơ đề cử MOWCAP 2016 (*Royal Literature on Hue Royal Architecture*): Danh mục công trình đề cử không có Lăng Tự Đức (Khiêm Lăng), do vua Tự Đức không áp dụng mô thức trang trí thơ văn "nhất thi nhất họa" trên liên ba đố bản lăng của mình. Nhận xét của Reviewer đúng -> Đã xóa Khiêm Lăng khỏi danh sách di sản MOWCAP ở File 5.
  - Hai bài thơ hồi văn của vua Thiệu Trị tại Điện Long An: Hồ sơ khoa học xác nhận tên đúng là *Vũ trung sơn thủy* (雨中山水) và *Phước viên văn hội lương dạ mạn ngâm* (福園文會良夜漫吟). File cũ ghi nhầm thành *Vũ Hải thi* và *Minh Mạng miếu thi*. Nhận xét của Reviewer đúng -> Đã sửa chính xác ở File 5.
  - Cấp ghi danh: MOWCAP khu vực Châu Á – Thái Bình Dương năm 2016, không phải Sổ quốc tế.

### 1.5. Bộ Bài Tới và Nghệ thuật Bài Chòi
- **Kết quả xác minh:**
  - Cơ cấu bộ Bài Tới: 3 pho (Pho Văn, Pho Vạn, Pho Sách), mỗi pho có **9 cặp quân bài** (chứ không phải 10 cặp; 3 x 9 = 27 cặp), cộng với **3 cặp bài yêu** (Ông Ầm, Thái Tử, Bạch Tuyết) = **30 cặp quân bài** (tương đương 60 quân bài). File cũ ghi 10 cặp mỗi pho dẫn đến tổng 33 cặp là sai toán học. Nhận xét của Reviewer đúng -> Đã sửa chính xác ở File 8.

### 1.6. Thực hành tín ngưỡng thờ Mẫu Tam phủ
- **Kết quả xác minh:**
  - 21 địa phương trong hồ sơ đề cử UNESCO 2016: Gồm Nam Định, Hà Nội, Hà Nam, Hưng Yên, Hải Dương, Hải Phòng, Thái Bình, Quảng Ninh, Vĩnh Phúc, Phú Thọ, Yên Bái, Tuyên Quang, Hà Giang, Bắc Ninh, Bắc Giang, Lạng Sơn, **Thanh Hóa**, Nghệ An, Hà Tĩnh, Thừa Thiên Huế, TP Hồ Chí Minh. Xác nhận có Thanh Hóa và không có Lào Cai. Nhận xét của Reviewer đúng -> Đã cập nhật chuẩn xác ở File 7.

### 1.7. Tri thức dân gian về Bún bò Huế
- **Kết quả xác minh:**
  - Phân định ranh giới di sản: Quyết định 2203/QĐ-BVHTTDL ngày 27/06/2025 công nhận loại hình "Tri thức dân gian", tập trung vào tri thức chọn nguyên liệu bản địa, kỹ nghệ ép bún thủ công (Vân Cù, Ô Sa), nghệ thuật dùng sả và mắm ruốc lóng, triết lý âm dương trong ẩm thực Cố đô.
  - Đã rút gọn triệt để các nội dung hướng dẫn nấu ăn chi tiết (cắt thịt, ninh xương, luộc giò...) và hướng dẫn thưởng thức thực tế để không lặp lại nội dung của entity món ăn trong domain Foods.

---

## 2. Chi tiết các nội dung đã hiệu chỉnh trên từng file

### Nhóm quyết định về tên file và cấu trúc:
- **Tiền tố số thứ tự:** Tuân thủ chỉ đạo của người dùng, **giữ nguyên số thứ tự** từ `1 ` đến `9 ` ở đầu tên file để phục vụ theo dõi tiến độ công việc.
- **Đổi tên File 6:** Đã đổi từ `6 Cửu Đỉnh.md` thành `6 Cửu Đỉnh Huế.md` (H1: `# Cửu Đỉnh Huế`) để khớp tên entity được quy định trong `heritage-entities-inventory.md`.

### Bảng tổng hợp hiệu chỉnh cụ thể:

| STT | Tên file | Các thay đổi chính đã thực hiện |
|:---:|---|---|
| 1 | `1 Quần thể Di tích Cố đô Huế.md` | - Cập nhật địa giới hành chính năm 2026: thành phố Huế trực thuộc Trung ương, các phường Phú Xuân, Thuận Hóa, Kim Long, Thủy Xuân, Hương Hồ, Thuận An.<br>- Phân định rõ ranh giới thành phần UNESCO năm 1993 với Cung An Định (di tích do Trung tâm quản lý, đề xuất xem xét mở rộng tương lai).<br>- Ghi rõ nơi bảo quản hiện nay của Mộc bản (Đà Lạt) và Châu bản (Hà Nội).<br>- Xóa sạch toàn bộ thuật ngữ repository (`file`, `canonical`, `domain`).<br>- Lược bỏ các dữ liệu tour, xe điện, VR audio mang tính vận hành biến động. |
| 2 | `2 Nhã nhạc cung đình Huế.md` | - Chuẩn hóa tên chính thức theo hồ sơ UNESCO: *Nhã nhạc - Âm nhạc cung đình Việt Nam*.<br>- Bổ sung Quyết định số 5079/QĐ-BVHTTDL năm 2012 ghi danh di sản phi vật thể quốc gia.<br>- Sửa chuỗi thiết chế quản lý âm nhạc thời Nguyễn (Ty Hòa Thanh/Việt Hòa, Đội Nhạc, Ban Nhã Nhạc).<br>- Xóa bỏ hoàn toàn chi tiết sai lịch sử "Lễ Tuyên ngôn độc lập".<br>- Đưa nghệ nhân, nhạc công lên hàng đầu chủ thể di sản; đánh giá khách quan thách thức bảo tồn di sản sống. |
| 3 | `3 Mộc bản triều Nguyễn.md` | - Đính chính địa chỉ Trung tâm Lưu trữ Quốc gia IV: **Số 02 đường Yết Kiêu, Phường 5, thành phố Đà Lạt, tỉnh Lâm Đồng**.<br>- Xóa bỏ hoàn toàn xếp hạng Bảo vật quốc gia (không có trong QĐ 2599/QĐ-TTg).<br>- Minh bạch số liệu kiểm kê: 34.555 tấm (UNESCO) vs 34.618 tấm (truyền thống) vs 33.971 - 33.976 tấm (thực tế kiểm kê).<br>- Đính chính phương tiện di dời năm 1960: xe tải và tàu hỏa (đường sắt), không dùng hàng không.<br>- Cập nhật địa chỉ Tàng Thơ Lâu tại phường Phú Xuân, thành phố Huế. |
| 4 | `4 Châu bản triều Nguyễn.md` | - Chuẩn hóa địa chỉ Trung tâm Lưu trữ Quốc gia I tại Hà Nội: số 5 phố Vũ Phạm Hàm, phường Yên Hòa, thành phố Hà Nội.<br>- Điều chỉnh mô tả ngự phê: nêu rõ Châu bản là khối văn thư hành chính trong đó có nhiều văn bản mang bút tích ngự phê mực son.<br>- Rút gọn các khẳng định tuyệt đối ("toàn vẹn", "xác thực tuyệt đối"), bỏ số liệu vận hành nhiệt độ/độ ẩm không có SOP chứng minh.<br>- Cập nhật địa chỉ Tàng Thơ Lâu thuộc phường Phú Xuân, thành phố Huế. |
| 5 | `5 Thơ văn trên kiến trúc cung đình Huế.md` | - Xóa bỏ Lăng Tự Đức (Khiêm Lăng) khỏi danh mục công trình thuộc hồ sơ MOWCAP 2016.<br>- Sửa chính xác tên 2 bài thơ hồi văn của vua Thiệu Trị tại Điện Long An: *Vũ trung sơn thủy* và *Phước viên văn hội lương dạ mạn ngâm*.<br>- Chuẩn hóa cấp ghi danh: Sổ đăng ký Ký ức Thế giới khu vực Châu Á – Thái Bình Dương (MOWCAP) năm 2016.<br>- Thống nhất số lượng 2.679 ô thơ văn chữ Hán theo hồ sơ Cục Di sản văn hóa.<br>- Cập nhật địa giới hành chính năm 2026 và hiện trạng bảo tồn khách quan. |
| 6 | `6 Cửu Đỉnh Huế.md` | - Đổi tên file thành `6 Cửu Đỉnh Huế.md`, H1: `# Cửu Đỉnh Huế`.<br>- Sửa văn bản Bảo vật quốc gia đúng: **Quyết định số 1426/QĐ-TTg ngày 01/10/2012** của Thủ tướng Chính phủ (đợt 1).<br>- Xóa bỏ hoàn toàn việc gán ghép Dụ Đỉnh cho vua Hàm Nghi và Huyền Đỉnh cho vua Duy Tân.<br>- Chuẩn hóa cấp ghi danh: Di sản tư liệu khu vực Châu Á – Thái Bình Dương (MOWCAP) năm 2024.<br>- Mô tả chính xác 162 mảng bản đúc nổi (mỗi đỉnh 18 ô = 17 ô hình tượng + 1 ô khắc tên đỉnh gồm 2 chữ Hán).<br>- Đánh giá hiện trạng bảo tồn ngoài trời theo hồ sơ MOWCAP 2024. |
| 7 | `7 Thực hành tín ngưỡng thờ Mẫu Tam phủ của người Việt.md` | - Sửa danh sách 21 địa phương theo hồ sơ đề cử UNESCO 2016: bổ sung Thanh Hóa, bỏ Lào Cai.<br>- Xóa sạch toàn bộ thuật ngữ repository, tên file `.md`, domain khỏi nội dung answer-facing.<br>- Làm rõ ranh giới giữa hồ sơ UNESCO chung của người Việt và nét bản sắc địa phương tại Huế (Tứ phủ, thần chủ Thiên Y A Na).<br>- Điều chỉnh mô tả 36 giá đồng là con số tượng trưng, mỗi buổi lễ chỉ hầu một số giá phù hợp.<br>- Cập nhật địa giới hành chính năm 2026 (phường Phú Xuân, phường Hương Hồ). |
| 8 | `8 Nghệ thuật Bài Chòi Trung Bộ.md` | - Sửa lỗi toán và cơ cấu bộ Bài Tới: 3 pho x 9 cặp = 27 cặp + 3 cặp bài yêu = **đúng 30 cặp quân bài** (60 quân bài).<br>- Cập nhật địa giới hành chính năm 2026: cầu ngói Thanh Toàn thuộc **phường Thanh Thủy**, làng Địa Linh thuộc **phường Hóa Châu**.<br>- Xóa thuật ngữ repository `(domain festivals)`.<br>- Neo rõ 9 tỉnh thành dải đất miền Trung theo hồ sơ đề cử UNESCO 2017.<br>- Bỏ văn phong tuyệt đối hóa, trình bày nguồn gốc và mối liên hệ Bài Tới dưới góc nhìn nghiên cứu. |
| 9 | `9 Tri thức dân gian về Bún bò Huế.md` | - Rút gọn triệt để phần tutorial công thức nấu nướng và hướng dẫn ăn uống chi tiết để không lặp nội dung với file món ăn trong domain Foods.<br>- Tập trung vào bản chất di sản phi vật thể: kỹ nghệ ép bún thủ công (Vân Cù, Ô Sa), nghệ thuật sả và mắm ruốc lóng, triết lý âm dương.<br>- Xóa sạch toàn bộ đường dẫn local `file://`, path và thuật ngữ repository.<br>- Làm rõ nguồn gốc dân gian và truyền thuyết Cô Bún, bỏ tính chất cung đình hóa ban đầu.<br>- Cập nhật địa giới hành chính năm 2026: làng Vân Cù thuộc **phường Kim Trà**, làng Ô Sa thuộc **xã Đan Điền**.<br>- Nêu rõ tình trạng nhãn hiệu chứng nhận từ năm 2016 và tiến trình xây dựng hồ sơ tham gia UCCN UNESCO. |

---

## 3. Cập nhật nhật ký bằng chứng (`knowledge-base-hue/meta/heritage-research-evidence.md`)

Implementer đã cập nhật toàn diện file `knowledge-base-hue/meta/heritage-research-evidence.md`:
- Bổ sung nhật ký kiểm chứng độc lập ngày 04/09/2026 cho cả 9 entity.
- Lưu trữ đầy đủ các văn bản pháp lý làm căn cứ: Nghị quyết 175/2024/QH15, Nghị quyết 1675/NQ-UBTVQH15, Quyết định 1426/QĐ-TTg, Quyết định 2203/QĐ-BVHTTDL, Quyết định 5079/QĐ-BVHTTDL.
- Trình bày rõ ràng các điểm mâu thuẫn số liệu (số lượng Mộc bản, hành trình di chuyển, quy mô các ô Thơ văn) và phương pháp xử lý trung lập.

---

## 4. Kết quả kiểm tra tự động sau hiệu chỉnh

Đã chạy kiểm tra tự động trên toàn bộ 9 file Markdown:
- **Kiểm tra tiêu đề H1:** 9/9 file có dòng H1 bắt đầu trực tiếp bằng `# <Tên entity>`, khớp hoàn toàn với tên gọi danh mục inventory.
- **Kiểm tra thuật ngữ cấm / repository:** Lệnh `grep -nE 'file://|canonical|chunk|metadata|tên file|đường dẫn|## Nguồn dữ liệu' knowledge-base-hue/heritage/[1-9]*.md` trả về kết quả rỗng (exit code 1 - hoàn toàn sạch sẽ).
- **Kiểm tra địa giới hành chính cũ:** Lệnh `grep -nE 'tỉnh Thừa Thiên Huế|quận Cầu Giấy' knowledge-base-hue/heritage/[1-9]*.md` trả về kết quả rỗng (exit code 1).
- **Kiểm tra văn phong quảng bá tuyệt đối:** Lệnh `grep -nE 'độc nhất vô nhị|tuyệt mỹ|đỉnh cao chói lọi|hoàn mỹ|tuyệt đối|bất diệt|thánh địa tối cao|xác thực tuyệt đối' knowledge-base-hue/heritage/[1-9]*.md` trả về kết quả rỗng (exit code 1).

---

## 5. Trạng thái hiện tại và kiến nghị

- Toàn bộ 9 file entity đợt 01 đã được làm sạch, xác thực và chuẩn hóa về cả dữ kiện lịch sử, tính pháp lý, cấu trúc Markdown và văn phong khách quan.
- Hồ sơ sẵn sàng để Reviewer Codex tiến hành vòng rà soát lại (re-review).
- Không thực hiện commit/push theo đúng quy định phân quyền Git (`git_authorization: none`).
