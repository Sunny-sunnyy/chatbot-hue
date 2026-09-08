# Codex Review: Final Approval Report - Cụm 7 Thực thể Đồi núi & Danh thắng Huế (Núi Ngự Bình, Vườn quốc gia Bạch Mã, Núi Kim Phụng, Hòn Vượn, Đồi Vọng Cảnh, Đồi Thiên An, Đèo Hải Vân)

Decision: approved  
Reviewer: Codex (Reviewer Agent)  
Date: 2026-09-07  
Canonical guide: `knowledge-base-hue/meta/tourism-template.md` & `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`  
Implementation evidence: `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục XXV đến XXXI)  
Implementation report: `reports/tourism_mountain_batch_implementation_correction_report_2026_09_07.md`  

---

## 1. Quyết định kỹ thuật tối cao (Technical Verdict: APPROVED)

Sau khi hoàn tất quá trình kiểm chứng độc lập chuyên sâu, đối chiếu thực địa mốc thời gian **tháng 09/2026**, và thực thi kiểm thử mã nguồn tự động đối với toàn bộ kết quả triển khai Đợt hiệu chỉnh tập trung (Focused Correction Batch) của Implementer, Reviewer Codex chính thức phê duyệt và cấp kết luận kỹ thuật:

**VERDICT: APPROVED**

Toàn bộ Cụm 7 thực thể danh thắng tự nhiên, đồi núi và đèo Hải Vân của Cố đô Huế:
1. `knowledge-base-hue/tourism/Núi Ngự Bình.md`
2. `knowledge-base-hue/tourism/Vườn quốc gia Bạch Mã.md`
3. `knowledge-base-hue/tourism/Núi Kim Phụng.md`
4. `knowledge-base-hue/tourism/Hòn Vượn.md`
5. `knowledge-base-hue/tourism/Đồi Vọng Cảnh.md`
6. `knowledge-base-hue/tourism/Đồi Thiên An.md`
7. `knowledge-base-hue/tourism/Đèo Hải Vân.md`
cùng hồ sơ đối chiếu kiểm chứng tại `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục XXV đến XXXI) đã được khắc phục triệt để **0 Blocker, 29 nhóm lỗi Major, 17 lỗi Minor**, đạt chuẩn 100% các tiêu chí kỹ thuật và nghiệp vụ RAG Cố đô Huế.

---

## 2. Kết quả kiểm chứng chi tiết sau hiệu chỉnh (Detailed Verification Results)

### 2.1. Vệ sinh mã nguồn và Markdown RAG Clean (Automated Hygiene Tests):
- **Trailing whitespace:** Lệnh `git diff --check` và script Python quét từng dòng trên toàn bộ 7 tệp đạt mã thoát `0` (Clean 100%, không còn bất kỳ khoảng trắng thừa cuối dòng nào).
- **Cấu trúc H1:** Mỗi tệp bắt đầu bằng đúng **duy nhất một H1** `# [Tên thực thể]` tại dòng 1. Không có tiêu đề H1 trùng lặp.
- **Thanh lọc siêu dữ liệu repo & RAG leaks:**
  + Không sử dụng YAML frontmatter, không chứa wiki-link `[[]]`.
  + Đã loại bỏ triệt để 100% các chuỗi rò rỉ `.md` và thuật ngữ RAG nội bộ hiển thị cho người dùng: `Núi Ngự Bình.md` (dòng 137), `Vườn quốc gia Bạch Mã.md` (dòng 18), `Núi Kim Phụng.md` (dòng 19), `Đồi Vọng Cảnh.md` (dòng 19), `Đèo Hải Vân.md` (dòng 81–82).

### 2.2. Tính độc lập ngữ cảnh (Chunk Independence) và Tiêu đề:
- **100% trong tổng số 219 tiêu đề H2 và H3** trên cả 7 tệp đều chứa tên định danh đầy đủ của thực thể.
- Đã chuẩn hóa viết hoa danh từ riêng thực thể 100% trong toàn bộ các tiêu đề:
  + `Núi Ngự Bình.md`: 30/30 tiêu đề tuân thủ Chunk Independence.
  + `Vườn quốc gia Bạch Mã.md`: 37/37 tiêu đề tuân thủ Chunk Independence.
  + `Núi Kim Phụng.md`: 31/31 tiêu đề tuân thủ Chunk Independence.
  + `Hòn Vượn.md`: 32/32 tiêu đề tuân thủ Chunk Independence.
  + `Đồi Vọng Cảnh.md`: 29/29 tiêu đề tuân thủ Chunk Independence.
  + `Đồi Thiên An.md`: 30/30 tiêu đề tuân thủ Chunk Independence; đã loại bỏ đánh số thứ tự cơ học `1.`, `2.`, `3.` ở các heading H3.
  + `Đèo Hải Vân.md`: 30/30 tiêu đề tuân thủ Chunk Independence.
- 100% các section và danh sách bullet đều có câu mở đầu dẫn nhập định danh rõ thực thể, bảo đảm câu văn không bị mồ côi ngữ cảnh khi vector search cắt chunk.

### 2.3. Loại bỏ dynamic pricing & tên cơ sở thương mại tư nhân:
- **Đồi Thiên An.md:** Đã loại bỏ toàn bộ các thông số giá biến động (dynamic pricing) như giá thuê xe máy, cước taxi, phí gửi xe tự phát; thay thế bằng khuyến cáo thực tế khách quan.
- **Núi Kim Phụng.md:** Đã xóa sạch tên công ty khai khoáng tư nhân `(COXANO Hương Thọ)` tại chỉ dẫn đường vào chân núi, thay bằng địa danh địa lý trung tính `khu mỏ đá Khe Phèn`.
- **Đèo Hải Vân.md:** Đã loại bỏ tên quán cà phê tư nhân tự phát ven đèo khỏi danh mục ngắm cảnh, chuyển hóa thành cảnh báo an toàn giao thông nghiêm cấm dừng đỗ phương tiện sai quy định.

### 2.4. Thanh lọc triệt để mỹ từ quảng bá và ví von cấm:
- Đã quét tự động kiểm tra toàn diện danh mục từ ngữ cấm:
  + Loại bỏ hoàn toàn hình ảnh ví von sang địa phương khác: *"Đà Lạt giữa lòng Cố đô"*, *"tiểu Đà Lạt xứ Huế"* tại `Đồi Thiên An.md`.
  + Thay thế sạch sẽ các tính từ cực đoan quảng bá: *"tuyệt đẹp"*, *"lý tưởng"*, *"ngoạn mục nhất"*, *"độc nhất vô nhị"*, *"tuyệt tác"*, *"kỳ vĩ"*, *"thỏi nam châm"*, *"ma mị"*, *"chốn bồng lai"*, *"đắt giá nhất"*, *"mỹ miều"*, *"lừng danh"*.
  + Danh hiệu vua Lê Thánh Tông ban cho Hải Vân Quan (*"Thiên hạ đệ nhất hùng quan"*) chỉ được dùng ở ngữ cảnh dẫn chứng sử liệu cửa ải, không dùng làm nhận định marketing cho cung đường đèo.
  + Từ ngữ "vịnh đẹp nhất thế giới" tại `Đèo Hải Vân.md` được chuẩn hóa chuẩn xác theo tên danh hiệu chính thức của Câu lạc bộ Các vịnh đẹp nhất thế giới (Worldbays).

### 2.5. Độ chính xác dữ liệu lịch sử, pháp lý và an toàn mốc tháng 09/2026:
- **Địa giới hành chính theo Nghị quyết 175/2024/QH15 & Nghị quyết 1675/NQ-UBTVQH15 (hiệu lực 01/07/2025):**
  + `Núi Ngự Bình`: Phường An Cựu mới (khu vực quận Thuận Hóa tương lai).
  + `Vườn quốc gia Bạch Mã`: Không ép thành một địa chỉ đơn nhất; trải rộng trên các xã Phú Lộc, Lộc An, Chân Mây – Lăng Cô, Khe Tre, Nam Đông (thành phố Huế) và huyện Đông Giang (tỉnh Quảng Nam); cổng vườn tại xã Phú Lộc.
  + `Núi Kim Phụng`: Phường Kim Long mới (sáp nhập từ xã Hương Thọ).
  + `Hòn Vượn`: Phường Kim Long mới (sáp nhập từ phường Hương Hồ, thôn Đồng Chẩm/Chầm).
  + `Đồi Vọng Cảnh`: Phường Thủy Xuân mới.
  + `Đồi Thiên An`: Phường Thủy Xuân mới (sáp nhập từ xã Thủy Bằng).
  + `Đèo Hải Vân`: Sườn bắc thuộc xã Chân Mây – Lăng Cô, thành phố Huế; sườn nam thuộc phường Hòa Hiệp Bắc (nay là phường Hải Vân), quận Liên Chiểu, thành phố Đà Nẵng.
- **Sử liệu & Thông số thực địa:**
  + `Núi Ngự Bình.md`: Đính chính chính xác cặp núi phụ tá phong thủy là **Tả Phù Sơn – Hữu Bật Sơn** (do vua Minh Mạng đặt tên năm 1821–1822).
  + `Vườn quốc gia Bạch Mã.md`: Độ cao đỉnh trắc địa chính xác là 1.448 m; căn cứ pháp lý thành lập gồm Quyết định số 214-CT (1991, 22.030 ha), Quyết định số 01/QĐ-TTg (2008, 37.487 ha), diện tích quản lý tự nhiên hiện hành 37.423,1 ha (sau điều chỉnh cao tốc La Sơn – Túy Loan); chứng nhận Vườn Di sản ASEAN (AHP8, tháng 12/2025).
  + `Núi Kim Phụng.md` & `Hòn Vượn.md`: Phân định minh bạch giữa hiện trạng cảnh quan/tuyến trekking tự nhiên hiểm trở với các dự án quy hoạch sinh thái; bổ sung cảnh báo mất sóng điện thoại di động và nguy cơ lạc đường vào các lối mòn cạo mủ thông rừng.
  + `Đồi Vọng Cảnh.md`: Đính chính hình thái dòng chảy sông Hương uốn lượn hình chữ C êm đềm; xác thực trạng thái công viên sinh thái mở cửa tự do.
  + `Đèo Hải Vân.md`: Bổ sung **Quy tắc an toàn thứ 6** cảnh báo phương tiện du lịch giữ khoảng cách an toàn 30–50 m với xe bồn chở xăng dầu, khí hóa lỏng và hàng nguy hiểm bắt buộc phải đi đường đèo.

---

## 3. Tổng kết tiến trình thẩm định Cụm 7 Đồi núi & Danh thắng Huế

| Vòng thẩm định | Ngày thực hiện | Đánh giá kỹ thuật | Tình trạng xử lý |
|:---|:---:|:---:|:---|
| **Vòng 1 (Round 1 Audit)** | 2026-09-07 | `changes_requested` | Phát hiện 0 Blocker, 29 nhóm Major, 17 Minor (rò rỉ `.md`, thiếu tên thực thể trong tiêu đề, mỹ từ cấm, sai sót ĐVHC, chi tiết sử liệu). |
| **Hiệu chỉnh tập trung** | 2026-09-07 | Sửa chữa tập trung | Implementer khắc phục 100% toàn bộ findings theo đúng biên bản review; cập nhật hồ sơ bằng chứng tại Mục XXV đến XXXI. |
| **Tái thẩm định (Re-Review)** | 2026-09-07 | **`approved`** | **Kiểm tra tự động và rà soát chuyên sâu 100% đạt chuẩn hoàn hảo. Cấp phê duyệt kỹ thuật chính thức.** |

---

## 4. Bảng lũy kế tiến độ Domain Du lịch (Cumulative Tourism Progress)

Tính đến ngày 07/09/2026, toàn bộ các cụm thực thể du lịch Cố đô Huế đã được Reviewer Codex thẩm định độc lập và phê duyệt chính thức gồm:

1. **Cụm Chợ & Không gian đi bộ (9 thực thể):**
   - Chợ Đông Ba, Phố cổ và chợ Bao Vinh, Chợ Tây Lộc, Chợ Xép, Chợ Bến Ngự, Chợ An Cựu, Phố đi bộ Nguyễn Đình Chiểu, Khu phố Tây Huế, Phố đi bộ Hai Bà Trưng. *(Phố đêm Hoàng Thành Huế đã được User xác nhận loại bỏ).* -> **APPROVED (9/9)**
2. **Cụm Bãi biển Đợt 1 (5 thực thể):**
   - Bãi biển Thuận An, Bãi biển Hải Dương, Bãi biển Vinh Thanh, Bãi biển Phú Diên, Bãi biển Hàm Rồng. -> **APPROVED (5/5)**
3. **Cụm Bãi biển & Vịnh Đợt 2 (4 thực thể):**
   - Bãi biển Lộc Bình, Bãi biển Bình An, Bãi biển Cảnh Dương, Vịnh Lăng Cô. -> **APPROVED (4/4)**
4. **Cụm Đầm phá Huế (5 thực thể):**
   - Hệ đầm phá Tam Giang – Cầu Hai, Phá Tam Giang, Đầm Chuồn, Đầm Lập An, Đầm Cầu Hai. -> **APPROVED (5/5)**
5. **Cụm Đồi núi & Danh thắng Huế (7 thực thể):**
   - Núi Ngự Bình, Vườn quốc gia Bạch Mã, Núi Kim Phụng, Hòn Vượn, Đồi Vọng Cảnh, Đồi Thiên An, Đèo Hải Vân. -> **APPROVED (7/7)**

**Tổng số tệp tourism đã được thẩm định và APPROVED chính thức: 30 / 30 thực thể điểm đến tự nhiên & văn hóa đô thị.**

---

## 5. Handoff & Định hướng cụm tiếp theo

- **Technical Verdict:** **`approved`**.
- **Chính sách mã nguồn:** Tuân thủ nghiêm ngặt `git_authorization: none` (không commit/push git).
- **Handoff:** Cập nhật `session_prompt/CURRENT_HANDOFF.md` sang trạng thái hoàn tất đợt review Cụm 7 Đồi núi & Danh thắng Huế.
- **Cụm thực thể tiếp theo đề xuất:**
  - **Cụm 5 Suối thác & Du lịch sinh thái cộng đồng Huế** (đã có tệp triển khai sẵn trong repo):
    1. `Làng du lịch cộng đồng Thác A Nôr.md`
    2. `Suối Pâr Le.md`
    3. `Thác Nhị Hồ.md`
    4. `Suối Mơ.md`
    5. `Suối Voi.md`
  - *(Tệp `tourism_guides.md` sẽ được xử lý riêng sau theo đúng chỉ đạo của User).*
