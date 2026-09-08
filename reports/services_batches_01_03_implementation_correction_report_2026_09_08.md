# Báo cáo kết quả hiệu chỉnh vòng 3: Tourism Services (Batches 1 – 3)

- **Vai trò:** Implementer
- **Ngày thực hiện:** 08/09/2026
- **Phạm vi hiệu chỉnh:**
  1. `knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md`
  2. `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md`
  3. `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md`
  4. `knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md`
  5. Mục XL, XLI, XLII, XLIII tại `knowledge-base-hue/meta/tourism-research-evidence.md`
- **Căn cứ thẩm định:** `reports/services_batches_01_03_codex_second_rereview_2026_09_08.md`
- **Trạng thái:** ready_for_rereview

---

## 1. Chi tiết delta hiệu chỉnh vòng 3 theo từng Finding

### Blocker B2 — Tuyến Vườn quốc gia Bạch Mã
- **Vấn đề trước đây:** Bản thảo trước đã bỏ các điểm trên đỉnh núi nhưng vẫn bố trí trọn vẹn Ngày 2 tại Bạch Mã và khẳng định tuyến Trĩ Sao, Vườn thực vật là route chân núi đang khả dụng tham quan, trong khi nguồn Báo Văn Hóa (13/06/2026) ghi nhận Km12 chưa khắc phục và chưa có thông báo mở tuyến mới.
- **Delta hiệu chỉnh:**
  1. **Thay thế toàn bộ Ngày 2:** Tại `Lịch trình du lịch Huế 3 ngày 2 đêm.md`, thay thế toàn bộ hành trình Ngày 2 cũ bằng **"Ngày 2: Khu du lịch suối khoáng nóng Alba Thanh Tân và Làng cổ Phước Tích"** (thuộc địa giới hành chính hiện hành phường Phong Thái và phường Phong Dinh).
  2. **Xóa bỏ triệt để tuyến chân núi Bạch Mã:** Xóa hoàn toàn mọi đề cập đến đường mòn Trĩ Sao, Vườn thực vật Bạch Mã và giá thuê xe ô tô lên đỉnh trong cả 4 guide answer-facing.
  3. **Quy chuẩn cảnh báo an toàn:** Tại cả 4 guide (`Đến Huế nên đi đâu.md:49, 98, 272`, `Lịch trình du lịch Huế 3 ngày 2 đêm.md:175-179, 274`, `Chi phí du lịch Huế.md:256`), chỉ giữ cảnh báo sạt lở Km12 và hướng dẫn du khách bắt buộc phải liên hệ Ban quản lý Vườn quốc gia Bạch Mã để kiểm tra thông báo mở tuyến và điều kiện thời tiết trong ngày trước khi lên kế hoạch.
  4. **Module mở rộng A:** Chuyển đổi thành "Khám phá thiên nhiên Vịnh Lăng Cô, Đầm Lập An và Suối Voi" (xã Chân Mây – Lăng Cô).

### Major M1 — Ranh giới services và lược bỏ mô tả chi tiết, slot giờ cứng
- **Vấn đề trước đây:** Bản thảo còn chứa các mô tả kiến trúc sâu, danh mục cổ vật ngự dụng, chi tiết tác phẩm tranh tượng, thực đơn món ăn cụ thể và một số mốc giờ cứng.
- **Delta hiệu chỉnh:**
  1. **Xóa sạch toàn bộ mốc giờ cứng:**
     - Tại `Đến Huế nên đi đâu.md`, chuyển các mốc giờ cũ thành các khung buổi linh hoạt kèm thời lượng tương đối.
     - Tại `Lịch trình du lịch Huế ngắn ngày.md`, xóa toàn bộ các mốc giờ cứng trong lịch trình gia đình (`8:00 – 8:45`, `9:00 – 11:00`, `14:00 – 15:30`...), thay thế bằng: *Đầu buổi sáng*, *Giữa buổi sáng*, *Khung giờ giữa ngày*, *Buổi chiều*, *Buổi tối*.
  2. **Tinh giản mô tả sâu và danh mục chi tiết:**
     - Tại `Lịch trình du lịch Huế ngắn ngày.md`, lược bỏ toàn bộ đoạn mô tả nhà rường gỗ lim, cổ vật ngự dụng, tranh tường nội thất và thưởng trà hoa cúc; chỉ giữ tên điểm đến và thời lượng gợi ý.
     - Tại `Lịch trình du lịch Huế 3 ngày 2 đêm.md`, lược bỏ danh sách mô tả tác phẩm mỹ thuật, danh mục món ăn/quà tặng và lịch trình ngày mưa; tập trung vào thứ tự tuyến, bán kính di chuyển, phân bổ sức lực và điều phối sang các cẩm nang chuyên ngành (`heritages/`, `foods/`, `performing_arts/`).

### Major M2 — Chuẩn hóa Provenance an toàn chèo SUP sông Hương
- **Vấn đề trước đây:** Ghi sai ngày phản hồi trên Hue-S (ghi 18/06/2024); nâng claim yêu cầu đơn vị phải "được cấp phép", "có đăng ký", có hướng dẫn viên hoặc đi theo đoàn vượt nội dung phản hồi của cơ quan chức năng.
- **Delta hiệu chỉnh:**
  1. **Cập nhật ngày nguồn chuẩn xác:** Cập nhật ngày nguồn phản ánh hiện trường trên Hue-S là **Ngày gửi: 28/06/2023, Ngày xử lý: 13/09/2023**.
  2. **Chỉ giữ 3 yêu cầu cốt lõi được Công an TP. Huế xác nhận:**
     - Mặc áo phao đạt chuẩn;
     - Trang bị thiết bị cứu sinh;
     - Di chuyển tránh luồng tàu thuyền du lịch lưu thông.
  3. **Loại bỏ triệt để các claim vượt nguồn:** Xóa bỏ hoàn toàn các yêu cầu về giấy phép kinh doanh ván SUP, đăng kiểm phương tiện (do cơ quan công an nêu rõ SUP không thuộc diện đăng ký/đăng kiểm), hướng dẫn viên đi kèm hoặc bắt buộc đi theo đoàn trên toàn bộ 4 guide answer-facing và hồ sơ evidence.

### Major M3 — Khả năng tiếp cận cho đối tượng đặc thù và vận hành đường thủy
- **Vấn đề trước đây:** Các khẳng định hạ tầng như "ô tô đỗ sát chân đồi", "ô tô đỗ tận cổng", xe điện và công viên "an toàn tuyệt đối" thiếu bằng chứng trực tiếp; quy định Ca Huế sông Hương chỉ ghi chung tên quy chế.
- **Delta hiệu chỉnh:**
  1. **Hạ claim tiếp cận thành yêu cầu liên hệ xác minh:** Tại `Đến Huế nên đi đâu.md`, `Lịch trình du lịch Huế ngắn ngày.md` và `Lịch trình du lịch Huế 3 ngày 2 đêm.md`, chuyển đổi toàn bộ các khẳng định tiếp cận thành khuyến nghị du khách chủ động liên hệ trước Ban quản lý điểm đến để kiểm tra điều kiện bãi đỗ xe thực tế, khả năng tiếp cận bằng xe lăn/xe đẩy trẻ em và phương án xe điện hỗ trợ.
  2. **Minh định vận hành đường thủy Ca Huế:** Nêu rõ hoạt động biểu diễn Ca Huế trên thuyền rồng sông Hương phải tuân thủ điều kiện cấp phép xuất bến của Ban Quản lý Bến thuyền Tòa Khâm và Cảng vụ Đường thủy nội địa; khi gặp thời tiết bất lợi (mưa lớn, gió bão, lũ trên sông Hương), du khách phải chuyển sang phương án thính phòng trong nhà trên bờ hoặc dời lịch trình.

### Major M5 — Thu hẹp tập giá thương mại, bổ sung Direct URLs và sửa chuẩn xác phép cộng
- **Vấn đề trước đây:** Tập giá thương mại rộng (101 dòng khớp giá); thiếu URL trực tiếp cho một số mẫu khảo sát; dòng 147 tính sai cận trên ngân sách 1 ngày tiết kiệm (`550.000` thay vì `700.000`).
- **Delta hiệu chỉnh:**
  1. **Sửa chuẩn xác phép cộng ngân sách 1 ngày tiết kiệm:**
     `80.000 – 100.000` (đi lại) + `0 – 150.000` (lưu trú) + `110.000 – 150.000` (ăn uống) + `150.000 – 200.000` (vé tham quan) + `25.000 – 50.000` (trải nghiệm) + `50.000` (dự phòng) = **415.000 đến 700.000 VNĐ/người**. Khắc phục dứt điểm số cũ 550.000 VNĐ.
  2. **Rà soát lại toàn bộ 100% phép cộng trong cả 3 bảng dự toán:**
     - 1 ngày: Tiết kiệm (415k – 700k), Tiêu chuẩn (740k – 1.250k), Thoải mái (1.750k – 2.780k).
     - 2N1Đ: Tiết kiệm (990k – 1.490k), Tiêu chuẩn (1.940k – 2.830k), Thoải mái (4.230k – 7.000k).
     - 3N2Đ: Tiết kiệm (1.650k – 2.370k), Tiêu chuẩn (2.980k – 4.150k), Thoải mái (6.400k – 11.550k).
     - Tổng 3N2Đ Tiêu chuẩn cộng vé máy bay khứ hồi (2.000k – 3.500k) = **4.980.000 đến 7.650.000 VNĐ/người**.
  3. **Thu hẹp tập giá thương mại:** Lược bỏ hàng loạt dải giá chi li phụ (cước taxi từng km, xích lô theo giờ, xe điện theo giờ, cước xe limousine/xe khách chi li, giá từng loại đặc sản cụ thể). Số dòng khớp pattern giá giảm mạnh từ 101 dòng xuống còn 71 dòng, chỉ giữ mẫu đại diện cần thiết phục vụ phương pháp lập ngân sách.
  4. **Bổ sung Direct URLs:** Cung cấp URL trực tiếp cho toàn bộ các record trong Bảng Facts Mục XLIII (bao gồm cả các thành phần cấu thành phép tính tổng).

### Major M6 — Đồng bộ Evidence, Report và Answer-Facing Artifacts
- **Vấn đề trước đây:** Nhiều ô nguồn trong bảng Facts còn là tên văn bản chung; evidence/report chưa đồng bộ với current body về Bạch Mã, time slots và khoảng ngân sách tham quan.
- **Delta hiệu chỉnh:**
  1. **Thay thế 100% placeholder nguồn bằng Direct URLs:** Cả 4 bảng Facts & Verification tại Mục XL, XLI, XLII, XLIII của `tourism-research-evidence.md` đều sử dụng Direct URLs công khai (`https://...` trên Cổng TTĐT Chính phủ, HĐND, ACV, VNR, Hue-S, Báo Văn Hóa, TTBT Di tích Cố đô Huế).
  2. **Đồng bộ khoảng ngân sách tham quan:** Đồng bộ con số **200.000 – 600.000 VNĐ/người lớn** giữa dòng 69 của `Chi phí du lịch Huế.md` và Mục XLIII dòng 1989 của evidence file.
  3. **Đồng bộ tuyến Bạch Mã:** Cả 4 guide answer-facing, 4 mục evidence và báo cáo triển khai thống nhất: không đưa tuyến lên đỉnh vào lịch trình mặc định; không khẳng định tuyến chân núi đang mở; chỉ giữ lưu ý liên hệ BQL kiểm tra mở tuyến trong ngày.

---

## 2. Số liệu đo đạc cơ học thực tế (Fresh Mechanical Metrics)

Số liệu ghi nhận trực tiếp từ các lệnh shell trên repository tại mốc 08/09/2026:

| Tên file | Đường dẫn | Số dòng (`wc -l`) | H1 | H2 | H3 | Trailing Whitespace | Trạng thái định dạng |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **File 1: Điểm đến** | `knowledge-base-hue/tourism/services/Đến Huế nên đi đâu.md` | **286** | 1 | 9 | 29 | 0 | Đạt chuẩn LF, không frontmatter, không link ngoài |
| **File 2: Ngắn ngày** | `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế ngắn ngày.md` | **247** | 1 | 10 | 21 | 0 | Đạt chuẩn LF, không frontmatter, không link ngoài |
| **File 3: 3N2Đ** | `knowledge-base-hue/tourism/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md` | **338** | 1 | 11 | 26 | 0 | Đạt chuẩn LF, không frontmatter, không link ngoài, không tên file đuôi md |
| **File 4: Chi phí** | `knowledge-base-hue/tourism/services/Chi phí du lịch Huế.md` | **302** | 1 | 11 | 31 | 0 | Đạt chuẩn LF, không frontmatter, không link ngoài, phép cộng khớp chính xác |
| **Evidence** | `knowledge-base-hue/meta/tourism-research-evidence.md` | **2007** | 3 | 43 | 165 | 0 | Chuẩn schema 7 cột tại Mục XL–XLIII; 100% có direct URL |
| **Báo cáo này** | `reports/services_batches_01_03_implementation_correction_report_2026_09_08.md` | **106** | 1 | 4 | 6 | 0 | Đạt chuẩn LF, phản ánh đúng observed delta |

*Ghi chú về Mục XL–XLIII trong `tourism-research-evidence.md` (dòng 1749 đến 2007):* Heading counts đo được: `H2=4, H3=19, H4=1`.

---

## 3. Kết quả kiểm tra mẫu chuỗi ký tự (Pattern Screening)

Lệnh kiểm tra regex được thực thi trên toàn bộ các file thuộc phạm vi:
- **Từ khóa rủi ro bị cấm:** `100%`, `thực địa`, `PASS`, `dây leash`, `Hải Vọng Đài`, `Ngũ Hồ`, `Thác Đỗ Quyên`, `xã Lộc Tiến`, `quận Liên Chiểu`, `18/06/2024`.
- **Kết quả scan:**
  - Cả 4 file guide answer-facing: **0 match**.
  - Không có YAML frontmatter, không có link ngoài `https://`, không có wiki-link `[[]]`, không có tên file `.md`, không có section `## Nguồn dữ liệu` trong 4 guide answer-facing.
  - Mục XL–XLIII trong `tourism-research-evidence.md`: **0 match** cho các claim sai; các từ ngữ địa danh cũ (`thị xã Hương Thủy`, `huyện Phú Vang`) chỉ xuất hiện trong cột/mục đối chiếu để bác bỏ; từ ngữ `Trĩ Sao`, `Vườn thực vật` chỉ xuất hiện trong mục bác bỏ.
  - Lệnh `git diff --check`: Exit code 0, không có output lỗi.
  - Lệnh `git diff --no-index --check /dev/null <file>` trên cả 6 file: Exit code 1 (do khác /dev/null), output rỗng (không phát hiện whitespace error), kết thúc bằng đúng một LF.

---

## 4. Kết luận bàn giao

Toàn bộ các finding còn mở (Blocker B2 và 5 nhóm Major M1, M2, M3, M5, M6) đã được xử lý triệt để và đồng bộ giữa answer-facing files, evidence records và báo cáo triển khai. Các phép tính toán số học đã được kiểm chứng chuẩn xác từng thành phần. Hồ sơ sẵn sàng bàn giao cho Reviewer Codex tiến hành tái thẩm định.
