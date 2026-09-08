# Codex Review: Cụm 5 Bãi biển Huế Đợt 1 (Thuận An, Hải Dương, Vinh Thanh, Phú Diên, Hàm Rồng)

Decision: changes_requested  
Reviewer: Codex (Reviewer Agent & Sub-agents Team)  
Date: 2026-09-06  
Canonical guide: `knowledge-base-hue/meta/tourism-template.md` & `knowledge-base-hue/tourism/tourism-research-and-entities-inventory.md`  
Implementation evidence: `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục XI, XII, XIII, XIV, XV)

---

## 1. Phạm vi đã review

Reviewer chính và 5 sub-agent chuyên trách đã hoàn thành thẩm định độc lập, tra cứu xác thực chéo thực địa bằng Web Search tiếng Việt thời gian thực (mốc tháng 09/2026), đối soát tiêu chuẩn Markdown RAG Clean và hồ sơ kiểm chứng đối với Cụm 5 thực thể bãi biển đợt 1:
1. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Bãi biển Thuận An.md`
2. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Bãi biển Hải Dương.md`
3. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Bãi biển Vinh Thanh.md`
4. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Bãi biển Phú Diên.md`
5. `/home/minhhieu/hue_rag/knowledge-base-hue/tourism/Bãi biển Hàm Rồng.md`
- Hồ sơ kiểm chứng tại: `knowledge-base-hue/meta/tourism-research-evidence.md` (Mục XI, XII, XIII, XIV, XV)

### Các trục nội dung đối soát chuyên sâu:
1. **Địa giới hành chính mốc tháng 09/2026:** Đối chiếu Nghị quyết số 175/2024/QH15 của Quốc hội (thành lập TP. Huế trực thuộc TW từ 01/01/2025), Nghị quyết 1314/NQ-UBTVQH15 (01/01/2025) và Nghị quyết 1675/NQ-UBTVQH15 của UBTVQH (hiệu lực 01/07/2025).
   - Thuận An & Hải Dương: Thuộc phường Thuận An, TP. Huế.
   - Vinh Thanh & Phú Diên: Thuộc xã Phú Vinh, TP. Huế (hợp nhất từ 4 xã Phú Diên, Vinh Xuân, Vinh An, Vinh Thanh).
   - Hàm Rồng: Thuộc xã Vinh Lộc, TP. Huế (hợp nhất từ 4 xã Vinh Hiền, Vinh Hưng, Vinh Mỹ, Giang Hải).
2. **Hạ tầng giao thông & Cầu ven biển:** Đối chiếu tiến độ thông xe kỹ thuật Cầu vượt cửa biển Thuận An dài 2,36 km (30/04/2026), vai trò Cầu Trường Hà vượt đầm Thủy Tú (TL10D nối QL49B), và xác thực các cung đường tiếp cận bãi biển không bị điều hướng sai.
3. **Di sản văn hóa, lịch sử & Khảo cổ học:**
   - Thuận An: Trấn Hải Thành (Gia Long 1813), Minh Mạng đổi tên 1834 & xây dựng Quan Hải Lâu (không có "đài Thái Hòa"); Miếu Thai Dương Phu Nhân (làng Thai Dương Hạ, nữ thần Yang Po Ino Nagar / Giàng Bô Um).
   - Phú Diên: Tháp Chăm Phú Diên phát hiện 18/04/2001 (khai thác titan), Quyết định 52/2001/QĐ-BVHTT; Kỷ lục thế giới năm 2022 do WorldKings & VietKings xác lập (xác minh rõ: KHÔNG PHẢI Guinness).
   - Hàm Rồng: Phân định rõ Chùa Thánh Duyên (Di tích Quốc gia 1996) trên núi Túy Vân vs Phế tích Tháp Chăm Linh Thái (Bảo vật Quốc gia Chóp tháp Linh Thái 2020) trên núi Linh Thái; mô tả địa mạo Động Hàm Rùa.
4. **An toàn bãi tắm & Mùa vụ biển:** Rãnh sụt cát bãi ngang, dòng chảy xa bờ (rip current), sự thiếu vắng lực lượng cứu hộ chuyên nghiệp thường trực tại các bãi tắm tự nhiên (Vinh Thanh, Phú Diên, Hàm Rồng), rủi ro trơn trượt ghềnh đá/kè tetrapod, hiện trạng sạt lở bờ biển 2026 và dự án đê kè 260 tỷ đồng tại Thuận An.
5. **Tiêu chuẩn Markdown RAG Clean:** H1 mở đầu trực tiếp, không YAML frontmatter, không wiki-link `[[]]`, không thuật ngữ nội bộ RAG (`chunk`, `metadata`, `canonical`), tính độc lập của tiêu đề H2/H3 (Chunk self-containment), loại bỏ hoàn toàn danh mục mỹ từ quảng bá bị cấm và tên quán ăn thương mại cá nhân.

---

## 2. Bảng tổng hợp Findings

| Thực thể | Blocker | Major | Minor | Đánh giá sơ bộ |
|:---|:---:|:---:|:---:|:---:|
| **Bãi biển Thuận An.md** | 0 | 4 | 3 | Changes Requested |
| **Bãi biển Hải Dương.md** | 0 | 3 | 2 | Changes Requested |
| **Bãi biển Vinh Thanh.md** | 0 | 2 | 2 | Changes Requested |
| **Bãi biển Phú Diên.md** | 0 | 4 | 4 | Changes Requested |
| **Bãi biển Hàm Rồng.md** | 0 | 3 | 4 | Changes Requested |
| **TỔNG CỘNG** | **0** | **16** | **15** | **CHANGES REQUESTED** |

---

## 3. Chi tiết Findings theo mức độ nghiêm trọng

### 3.1. Nhóm lỗi BLOCKER (0 lỗi)
Toàn bộ 5 tệp đều tuân thủ tốt cấu trúc RAG Clean cơ bản, ranh giới thực thể chuẩn xác, không tạo tệp trùng lặp theo đúng chỉ đạo inventory (`Bãi biển Vinh Hiền.md` được tích hợp trọn vẹn vào `Bãi biển Hàm Rồng.md`; không tạo file di sản tháp Chăm trùng lặp).

---

### 3.2. Nhóm lỗi MAJOR (16 lỗi)

#### [Thuận An] Finding M-01: Vi phạm danh mục mỹ từ quảng bá bị cấm theo template
- **Vị trí:** `Bãi biển Thuận An.md`, Dòng 15, 25, 31, 113, 127.
- **Hiện trạng:** Sử dụng các từ cấm hoặc mang tính tuyệt đối:
  + Dòng 15: *"nổi tiếng bậc nhất"*
  + Dòng 25: *"lộng lẫy"*
  + Dòng 31: *"đặc trưng bậc nhất"*
  + Dòng 113: *"lợi thế tuyệt vời... hai khoảnh khắc kỳ ảo nhất"*
  + Dòng 127: *"thời điểm vàng"*
- **Căn cứ đối chiếu:** `meta/tourism-template.md` Mục 2.6 quy định cấm các mỹ từ như "tuyệt mỹ", "bậc nhất", "tuyệt vời", "thời điểm vàng", "kỳ ảo nhất".
- **Phương án chỉnh sửa:** Khách quan hóa văn phong theo đúng tiêu chuẩn bách khoa (sửa thành "thắng cảnh lâu đời và quen thuộc", "lộng gió", "nét địa hình đặc thù", "lợi thế thuận tiện để quan sát", "khoảng thời gian thuận lợi nhất trong năm").

#### [Thuận An] Finding M-02: Lặp từ ngữ tán dương cảm tính ("nức tiếng... nức tiếng")
- **Vị trí:** `Bãi biển Thuận An.md`, Dòng 17.
- **Hiện trạng:** Viết lặp: *"...lễ hội Cầu ngư truyền thống **nức tiếng**. Vẻ đẹp của vùng biển – cửa biển này từng được vua Thiệu Trị ca ngợi và xếp ở vị trí thứ 10 trong chùm thơ "Thần kinh nhị thập cảnh" **nức tiếng** xứ Thần kinh."*
- **Căn cứ & Đánh giá:** Lặp từ biểu cảm văn học, làm giảm tính trang trọng khách quan của tài liệu bách khoa.
- **Phương án chỉnh sửa:** Đổi thành *"...lễ hội Cầu ngư truyền thống đặc sắc. Cảnh sắc của vùng cửa biển này từng được vua Thiệu Trị ca ngợi và xếp ở vị trí thứ 10 trong chùm thơ ngự chế "Thần kinh nhị thập cảnh" của Kinh đô Huế."*

#### [Thuận An] Finding M-03: Thiếu dữ kiện lịch sử vua Minh Mạng đổi tên Trấn Hải Thành & xây Quan Hải Lâu (loại bỏ nhầm lẫn "đài Thái Hòa")
- **Vị trí:** `Bãi biển Thuận An.md`, Dòng 55.
- **Hiện trạng:** Chỉ nêu vua Gia Long xây năm 1813 và Thiệu Trị xây pháo đài Hòa Duân 1847; thiếu mốc Minh Mạng năm 1834.
- **Căn cứ đối chiếu:** *Đại Nam thực lục*, Cổng TTĐT TP. Huế: Năm 1813 vua Gia Long cho xây **Trấn Hải Đài**. Đến năm 1834 (Minh Mạng thứ 15), vua Minh Mạng đổi tên thành **Trấn Hải Thành**, gia cố thêm pháo nhãn và cho xây **Quan Hải Lâu** (觀海樓) trên mặt thành để quan sát, canh phòng tàu bè từ khơi xa (bên trong đặt kính thiên lý, treo đèn lồng lớn báo hiệu hoa tiêu). Triều Nguyễn không hề xây "đài Thái Hòa" tại cửa biển (tránh nhầm với Điện Thái Hòa trong Đại Nội).
- **Phương án chỉnh sửa:** Bổ sung chính xác mốc năm 1834 vua Minh Mạng đổi tên Trấn Hải Thành và xây dựng Quan Hải Lâu.

#### [Thuận An] Finding M-04: Chưa cập nhật hiện trạng sạt lở bờ biển thực tế 2026 và dự án đê kè 260 tỷ đồng
- **Vị trí:** `Bãi biển Thuận An.md`, Dòng 131 và Dòng 172.
- **Căn cứ đối chiếu:** Dữ liệu thủy văn và báo chí Thừa Thiên Huế tháng 8–9/2026: Triều cường đã gây sạt lở tạo hàm ếch xói lở chân đường bê tông ven biển đoạn Thuận An – Phú Thuận; dự án chống sạt lở bờ biển Thuận An (tổng mức 260 tỷ đồng gồm 670m kè bờ và 365m đê ngầm giảm sóng) đang được thi công khẩn trương.
- **Phương án chỉnh sửa:** Bổ sung cảnh báo sạt lở hàm ếch thực tế vào mục mùa mưa bão (dòng 131) và bổ sung quy tắc an toàn (dòng 172) yêu cầu du khách tránh xa mép cát sạt lở và công trường đê ngầm giảm sóng.

---

#### [Hải Dương] Finding M-05: Vi phạm danh mục mỹ từ quảng bá bị cấm theo template
- **Vị trí:** `Bãi biển Hải Dương.md`, Dòng 72 và Dòng 84 (cùng các dòng 18, 38, 86, 116).
- **Hiện trạng:**
  + Dòng 72: *"sàn diễn thiên nhiên **độc nhất vô nhị**"* (từ cấm tuyệt đối theo mục 2.6).
  + Dòng 84: *"góc quan sát thiên nhiên **tuyệt mỹ**"* (từ cấm tuyệt đối theo mục 2.6).
  + Dòng 18: *"ngoạn mục"*, *"khung cảnh nên thơ hiếm có"*.
  + Dòng 38: *"đậm chất điện ảnh"*.
  + Dòng 86: *"hoàng hôn huyền thoại"*.
- **Phương án chỉnh sửa:** Thay thế toàn bộ các từ cấm bằng văn phong miêu tả trung tính, chuẩn xác ("không gian cảnh quan ven biển đặc sắc", "tầm nhìn cảnh quan thuận lợi", "vẻ đẹp góc cạnh thô mộc của khối bê tông", "cảnh sắc hoàng hôn").

#### [Hải Dương] Finding M-06: Nhầm lẫn vị trí địa lý và vi phạm quy định đưa tên thương hiệu quán ăn cá nhân
- **Vị trí:** `Bãi biển Hải Dương.md`, Dòng 90.
- **Hiện trạng:** Ghi du khách ghé thưởng thức bánh ép *"tiêu biểu như quán bánh ép Dì Kiều và nhiều quán lân cận"* trong làng Hải Dương.
- **Căn cứ đối chiếu:** Quán bánh ép Dì Kiều (O Kiều) thực tế nằm tại **số 04 đường Lê Sỹ, TDP Hải Thành, phường Thuận An** (ở **bờ nam** cửa biển), không nằm ở làng Hải Dương (bờ bắc). Ngoài ra, mục 5 template nghiêm cấm đưa tên cơ sở kinh doanh, quán ăn cụ thể vào bài trừ khi là di sản lâu đời mang tính thiết chế văn hóa.
- **Phương án chỉnh sửa:** Xóa bỏ cụm từ `(tiêu biểu như quán bánh ép Dì Kiều và nhiều quán lân cận)`, diễn đạt tổng quát về các hàng quán bánh ép dân dã trong làng chài Hải Dương.

#### [Hải Dương] Finding M-07: Mất ngữ cảnh độc lập của chunk con tại các H3
- **Vị trí:** `Bãi biển Hải Dương.md`, Dòng 36, 130, 134, 138, 142.
- **Hiện trạng:** Các câu mở đầu section H3 bị thiếu chủ thể định danh thực thể:
  + Dòng 36: *"Nằm cách bãi đá thấp một đoạn đi bộ ngắn là khu vực bãi đá cao..."*
  + Dòng 130: *"Bề mặt các khối bê tông tổ ong tại bãi đá thấp khi ngập nước..."*
  + Dòng 134: *"Các khối bê tông ba chân (tetrapod) ở bãi đá cao..."*
  + Dòng 138: *"Khu vực cửa biển và chân đê kè chắn sóng là nơi thường xuyên..."*
  + Dòng 142: *"Du khách khi tham quan trên các đê kè vươn ra biển cần chú ý..."*
- **Phương án chỉnh sửa:** Bổ sung thực thể "Bãi biển Hải Dương" vào câu mở đầu của từng chunk con để bảo toàn tính độc lập ngữ cảnh khi retrieval.

---

#### [Vinh Thanh] Finding M-08: Vi phạm danh mục mỹ từ quảng bá bị cấm theo template
- **Vị trí:** `Bãi biển Vinh Thanh.md`, Dòng 16, 78, 138.
- **Hiện trạng:**
  + Dòng 78: *"điểm ngắm bình minh trên biển **tuyệt mỹ** tại khu vực Thừa Thiên Huế"* (vi phạm trực tiếp từ cấm "tuyệt mỹ").
  + Dòng 16: *"bãi biển tự nhiên **duyên dáng**"*.
  + Dòng 138: *"Vẻ đẹp **thuần khiết** của Bãi biển Vinh Thanh"*.
- **Phương án chỉnh sửa:** Sửa dòng 78 thành "địa điểm thuận lợi để chiêm ngưỡng bình minh trên biển"; dòng 16 bỏ "duyên dáng"; dòng 138 sửa thành "Môi trường sinh thái và cảnh quan tự nhiên của Bãi biển Vinh Thanh".

#### [Vinh Thanh] Finding M-09: Cảnh báo an toàn bãi biển bãi ngang: bờ dốc và thiếu lực lượng cứu hộ thường trực
- **Vị trí:** `Bãi biển Vinh Thanh.md`, Dòng 26 và Dòng 127–135.
- **Hiện trạng:** Dòng 26 mô tả thềm cát "thoai thoải... không có các vực hẫng sụt sâu đột ngột gần mép sóng... an toàn"; dòng 127–135 hoàn toàn thiếu cảnh báo về việc bãi biển chưa có đội cứu hộ chuyên nghiệp thường trực.
- **Căn cứ đối chiếu:** Vinh Thanh là vùng bãi ngang hở đón trực diện sóng đại dương, đáy biển có độ dốc cao hơn bãi Thuận An, chân sóng khoét cát tạo rãnh sâu bất ngờ. Khác với Thuận An có lực lượng cứu hộ thường trực, Vinh Thanh chỉ có lực lượng dân phòng tuần tra bán thời gian trong mùa nắng nóng. Báo chí đã ghi nhận nhiều vụ đuối nước thương tâm (tháng 04/2025 và tháng 05/2023).
- **Phương án chỉnh sửa:** Hiệu đính dòng 26 về độ dốc đáy biển; bổ sung cảnh báo bắt buộc mặc áo phao và nêu rõ tình trạng thiếu lực lượng cứu hộ chuyên nghiệp thường trực vào quy tắc an toàn.

---

#### [Phú Diên] Finding M-10: Sai lệch nghiêm trọng chỉ dẫn hướng đi qua Thuận An (Cầu vượt Thuận An)
- **Vị trí:** `Bãi biển Phú Diên.md`, Dòng 58.
- **Hiện trạng:** Viết: `Từ trung tâm thành phố Huế, di chuyển theo Quốc lộ 49 hướng về biển Thuận An, qua cầu Thuận An rồi rẽ phải vào Quốc lộ 49B...`
- **Căn cứ đối chiếu:** Cầu vượt cửa biển Thuận An dài 2,36 km bắc qua luồng lạch cửa biển nối phường Thuận An sang bờ bắc xã Hải Dương (đi về Quảng Điền / Phong Điền). Bãi biển Phú Diên nằm ở **bờ nam** cửa biển, xuôi về phía đông nam. Nếu đi qua cầu Thuận An sang bờ bắc sẽ hoàn toàn ngược hướng và bị ngăn cách bởi cửa biển.
- **Phương án chỉnh sửa:** Sửa lại lộ trình chính xác: Đi theo QL49 ra phường Thuận An, đến nút giao ngã ba Thuận An (khu vực cầu Diên Trường 1) thì rẽ phải vào QL49B chạy xuôi về phía đông nam qua Phú Hải đến Phú Diên; tuyệt đối **không đi qua cầu vượt cửa biển Thuận An**.

#### [Phú Diên] Finding M-11: Bỏ sót Cầu Trường Hà trong lộ trình tiếp cận từ phía nam qua đầm phá
- **Vị trí:** `Bãi biển Phú Diên.md`, Dòng 59.
- **Hiện trạng:** Chỉ ghi chung chung "theo trục đường Tỉnh lộ 10A qua các vùng đầm phá ven sông Như Ý đến nút giao nối Quốc lộ 49B".
- **Căn cứ đối chiếu:** Dải cồn cát ven biển Phú Diên bị ngăn cách với đất liền nội địa bởi đầm Thủy Tú / Hà Trung. Muốn từ Tỉnh lộ 10/10B ra QL49B bắt buộc phải qua thị trấn Phú Đa và vượt **Cầu Trường Hà** (cầu bê tông dài 848m vượt đầm Thủy Tú sang xã Vinh Thanh), sau đó rẽ trái vào QL49B đi ngược lên bắc 5 km đến Phú Diên.
- **Phương án chỉnh sửa:** Bổ sung chi tiết vị trí vượt Cầu Trường Hà vào lộ trình đầm phá.

#### [Phú Diên] Finding M-12: Vi phạm nghiêm trọng Chunk Independence tại tất cả các tiêu đề H2
- **Vị trí:** `Bãi biển Phú Diên.md`, Các dòng 3, 13, 20, 30, 48, 54, 62, 69.
- **Hiện trạng:** Toàn bộ tiêu đề H2 đều dùng tên generic không chứa thực thể: `## Thông tin chung`, `## Tổng quan`, `## Địa hình bờ biển và cảnh quan cồn cát`, `## Hệ sinh thái và dải rừng phi lao phòng hộ`, `## Mùa biển và điều kiện thời tiết`, `## Tuyến tiếp cận và phương tiện di chuyển`, `## An toàn tắm biển và bảo vệ cảnh quan cồn cát`, `## Thông tin dành cho du khách`.
- **Căn cứ đối chiếu:** `meta/tourism-template.md` Mục 2.6 yêu cầu các heading phải tự chứa định danh thực thể để đảm bảo chất lượng semantic retrieval độc lập.
- **Phương án chỉnh sửa:** Chuẩn hóa toàn bộ tiêu đề H2 gắn kèm tên thực thể: `## Thông tin chung về Bãi biển Phú Diên`, `## Tổng quan về Bãi biển Phú Diên`, `## Địa hình bờ biển và cảnh quan cồn cát Bãi biển Phú Diên`...

#### [Phú Diên] Finding M-13: Dữ kiện Tháp Chăm Phú Diên thiếu chi tiết xác thực & nguy cơ ảo giác Kỷ lục Guinness
- **Vị trí:** `Bãi biển Phú Diên.md`, Dòng 16, 26.
- **Hiện trạng:** Dùng sai ngữ nghĩa từ "văn hóa tiền phong" (dòng 16); thiếu ngày phát hiện (18/04/2001 do công nhân khai thác titan); thiếu Quyết định số 52/2001/QĐ-BVHTT; dòng 26 chỉ ghi chung chung "xác lập kỷ lục thế giới" dễ gây hiểu nhầm thành Guinness World Records.
- **Căn cứ đối chiếu:** Kỷ lục này do **Tổ chức Kỷ lục Việt Nam (VietKings)** xác lập ngày 14/03/2022 và **Liên minh Kỷ lục Thế giới (WorldKings)** xác lập ngày 30/05/2022 (công bố 06/2022). Khẳng định rõ: **Không phải kỷ lục Guinness**.
- **Phương án chỉnh sửa:** Sửa "văn hóa tiền phong" thành "di sản văn hóa Champa cổ"; bổ sung ngày 18/04/2001, Quyết định 52/2001/QĐ-BVHTT, và ghi rõ tổ chức xác lập WorldKings / VietKings.

---

#### [Hàm Rồng] Finding M-14: Vi phạm danh mục mỹ từ quảng bá bị cấm theo template
- **Vị trí:** `Bãi biển Hàm Rồng.md`, Dòng 16, 18, 39, 99, 101, 108, 110, 114.
- **Hiện trạng:**
  + Dòng 99: *"tọa độ **tuyệt mỹ** để đón khoảnh khắc"* (từ cấm trực tiếp).
  + Dòng 110: *"bối cảnh **độc nhất vô nhị**"* (từ cấm trực tiếp).
  + Dòng 16: *"độc đáo **bậc nhất**"*.
  + Dòng 108: *"**thiên đường** cho các tín đồ nhiếp ảnh"*.
  + Dòng 18, 39, 101, 114: Các từ ngữ cảm thán ("ngọc bích", "bức tranh thủy mặc sống động", "tráng lệ khó quên", "thư thái tuyệt vời").
- **Phương án chỉnh sửa:** Khách quan hóa toàn bộ thành văn phong bách khoa, trung tính theo quy chuẩn RAG Clean.

#### [Hàm Rồng] Finding M-15: Chưa phân biệt và làm rõ di tích giữa Núi Túy Vân và Núi Linh Thái
- **Vị trí:** `Bãi biển Hàm Rồng.md`, Dòng 43–48 và Dòng 71.
- **Căn cứ đối chiếu:**
  + **Núi Túy Vân:** Nơi có **Chùa cổ Thánh Duyên** (xây dựng thời chúa Nguyễn, Minh Mạng trùng kiến 1836, được Bộ VHTT xếp hạng Di tích Lịch sử – Văn hóa cấp Quốc gia năm 1996 theo QĐ 398-QĐ/VH).
  + **Núi Linh Thái (ngay sau Bãi biển Hàm Rồng):** Trên đỉnh núi có **Phế tích Tháp Chăm Linh Thái** (thế kỷ XI–XII). Năm 2020, Thủ tướng Chính phủ ký Quyết định số 2283/QĐ-TTg công nhận hiện vật tìm thấy tại đây là **Bảo vật Quốc gia: Bộ Chóp tháp Chăm Pa Linh Thái**.
- **Hiện trạng:** Tệp thiếu ghi nhận cấp di tích quốc gia của Chùa Thánh Duyên và bỏ sót hoàn toàn giá trị khảo cổ di tích Tháp Chăm Linh Thái / Bảo vật Quốc gia 2020 trên đỉnh núi Linh Thái.
- **Phương án chỉnh sửa:** Bổ sung giá trị khảo cổ phế tích Tháp Chăm Linh Thái (Bảo vật Quốc gia 2020) vào dòng 48; bổ sung cấp xếp hạng Di tích Quốc gia (1996) cho Chùa Thánh Duyên vào dòng 71.

#### [Hàm Rồng] Finding M-16: Bỏ sót mô tả địa danh "Động Hàm Rùa" trong thân bài địa mạo
- **Vị trí:** `Bãi biển Hàm Rồng.md`, Dòng 10 và Dòng 22–40.
- **Hiện trạng:** Dòng 10 nêu cụm bãi ôm dọc "chân núi Linh Thái và động Hàm Rùa", nhưng toàn bộ mục `## Địa hình bờ biển và cấu trúc cảnh quan đá trầm tích` lại không giải thích "động Hàm Rùa" là gì, nằm ở đâu.
- **Căn cứ đối chiếu:** "Động Hàm Rùa" là tên dân gian địa phương chỉ cụm hang hốc đá tự nhiên do sóng biển khoét mòn chân vách đá núi Linh Thái sát mép nước (khu vực chuyển tiếp giữa bãi Hàm Rồng và bãi Đông Dương).
- **Phương án chỉnh sửa:** Bổ sung đoạn mô tả địa mạo cấu tạo hang hốc đá vòm "động Hàm Rùa" vào cuối dòng 34.

---

### 3.3. Nhóm lỗi MINOR (15 lỗi)

1. **Finding m-01 (`Bãi biển Thuận An.md` - Dòng 29, 73, 77, 101, 111, 117, 125, 129, 133, 154, 177):** Tối ưu hóa tính độc lập chunking (Chunk Heading Independence) tại 11 tiêu đề H3 chưa có tên thực thể.
2. **Finding m-02 (`Bãi biển Thuận An.md` - Dòng 97, 108):** Bổ sung đặc sản mắm cá rò Thuận An, mực nháy tươi rói hấp sả và bánh bột lọc ven bãi.
3. **Finding m-03 (`Bãi biển Thuận An.md` - Dòng 91–92):** Làm rõ vị trí Miếu Thai Dương Phu Nhân (làng Thai Dương Hạ bờ bắc) và nguồn gốc thờ nữ thần biển Chăm Pa (Yang Po Ino Nagar / Giàng Bô Um).
4. **Finding m-04 (`Bãi biển Hải Dương.md` - Dòng 8):** Chuẩn hóa chuỗi pháp lý sáp nhập ĐVHC theo Nghị quyết 1314/NQ-UBTVQH15 (hiệu lực 01/01/2025) và Nghị quyết 1675/NQ-UBTVQH15 (01/07/2025).
5. **Finding m-05 (`Bãi biển Hải Dương.md` - Dòng 62, 110):** Làm rõ lịch sử phân chia làng cổ Thai Dương sau bão Giáp Thìn 1904: nhánh bờ bắc là làng Thai Dương Hạ (xã Hải Dương cũ), bờ nam là Thai Dương Thượng / Thai Dương Hạ.
6. **Finding m-06 (`Bãi biển Vinh Thanh.md` - Dòng 58, 64, 72, 76, 80, 94, 100, 106, 119, 136, 145, 150):** Tối ưu hóa tính độc lập chunking tại 11 tiêu đề H3 chưa gắn tên thực thể.
7. **Finding m-07 (`Bãi biển Vinh Thanh.md` - Dòng 62, 148):** Bổ sung nhịp cập bến buổi chiều (khoảng 15h00 – 16h30) của thuyền thúng đi câu lộng ban ngày.
8. **Finding m-08 (`Bãi biển Phú Diên.md` - Dòng 7):** Bổ sung cấp thôn (Thôn Mỹ Khánh) và trích dẫn Nghị quyết 1675/NQ-UBTVQH15.
9. **Finding m-09 (`Bãi biển Phú Diên.md` - Dòng 5):** Bổ sung tên gọi dân gian của bãi biển ("Bãi tắm Tháp Chàm", "Bãi tắm Mỹ Khánh").
10. **Finding m-10 (`Bãi biển Phú Diên.md` - Dòng 28, 44, 51):** Tiết chế các từ ngữ biểu cảm chủ quan ("lý tưởng", "hiếm có mà ít nơi có được").
11. **Finding m-11 (`Bãi biển Phú Diên.md` - Dòng 65):** Làm rõ đặc thù cứu hộ của bãi tắm tự nhiên cộng đồng, không có trạm cứu hộ chuyên trách thường trực.
12. **Finding m-12 (`Bãi biển Hàm Rồng.md` - Dòng 49, 59, 77, 83, 104, 108, 142):** Tối ưu hóa tính độc lập chunking tại các tiêu đề H3 chưa có tên thực thể.
13. **Finding m-13 (`Bãi biển Hàm Rồng.md` - Dòng 87–88):** Bổ sung các loài thủy hải sản đặc hữu vùng nước lợ cửa Tư Hiền / đầm Cầu Hai: cá ong (cá căng), tôm bạc đầm phá, vẹm xanh bám ghềnh đá.
14. **Finding m-14 (`Bãi biển Hàm Rồng.md` - Dòng 8):** Đổi nhãn `- **Địa chỉ:**` thành `- **Địa điểm:**` cho thực thể thắng cảnh tự nhiên theo template.
15. **Finding m-15 (`Bãi biển Hàm Rồng.md` - Dòng 121, 138):** Nâng cao mức độ cảnh báo: tuyệt đối cấm tắm biển trong mùa mưa bão; cảnh báo hiểm họa ghềnh đá ngầm chìm khuất dưới mép sóng.

---

## 4. Bảng hướng dẫn hiệu chỉnh chi tiết (Action Items & Text Patch Matrix)

Dưới đây là các đoạn văn bản chính xác đã được chuẩn hóa để Implementer thay thế trực tiếp vào các tệp Markdown tương ứng:

### 4.1. Bản vá cho `Bãi biển Thuận An.md`

#### Thay thế đoạn Dòng 15–17 (M-01, M-02):
```markdown
Bãi biển Thuận An là một trong những thắng cảnh biển lâu đời và quen thuộc của đất Cố đô, tọa lạc tại cửa ngõ biển quan trọng nơi dòng sông Hương hòa vào hệ đầm phá Tam Giang trước khi đổ ra Biển Đông. Không gian Bãi biển Thuận An trải dài trên một dải đất doi cát duyên hải độc đáo, giữ vị trí tự nhiên ngăn cách giữa một bên là đại dương bao la với những đợt sóng vỗ miên man và một bên là vùng đầm phá nước lợ phẳng lặng, mênh mang. Nằm cách trung tâm thành phố Huế chỉ chừng 15 km, Bãi biển Thuận An từ lâu đã trở thành điểm đến nghỉ ngơi, tắm biển và giải nhiệt mùa hè quen thuộc của nhiều thế hệ người dân Cố đô cũng như du khách thập phương.

Bên cạnh giá trị về cảnh quan thiên nhiên với bờ cát trắng mịn thoai thoải và dải rừng phi lao phòng hộ xanh ngắt, Bãi biển Thuận An còn gắn liền với một chiều sâu lịch sử – văn hóa đặc sắc. Nơi đây từng là tiền đồn quân sự trọng yếu bảo vệ Kinh đô Huế thời triều Nguyễn, ghi dấu nhiều biến thiên địa lý tự nhiên qua các thế kỷ, đồng thời là địa bàn sinh sống lâu đời của cư dân làng chài Thai Dương với các phong tục tập quán ngư nghiệp thuần hậu và lễ hội Cầu ngư truyền thống đặc sắc. Cảnh sắc của vùng cửa biển này từng được vua Thiệu Trị ca ngợi và xếp ở vị trí thứ 10 trong chùm thơ ngự chế "Thần kinh nhị thập cảnh" của Kinh đô Huế.
```

#### Thay thế đoạn Dòng 53–58 (M-03):
```markdown
### Hệ thống phòng thủ Trấn Hải Thành và biến cố lịch sử 1883

Nhằm bảo vệ tuyệt đối cửa ngõ phía biển của Kinh thành Huế, triều Nguyễn đã dày công xây dựng tại cửa biển Thuận An một mạng lưới công trình quân sự liên hoàn. Năm 1813 (Gia Long thứ 12), triều đình cho xây đắp Trấn Hải Đài (về sau gọi là Trấn Hải Thành), một pháo đài phòng thủ hình tròn kiên cố bằng đá bazan và gạch vồ ngay sát bờ nam cửa biển. Đến năm 1834 (Minh Mạng thứ 15), vua Minh Mạng cho đổi tên đài thành Trấn Hải Thành, củng cố hệ thống pháo nhãn và cho dựng thêm tòa lầu Quan Hải Lâu trên mặt thành nhằm phục vụ việc ngự lãm và quan sát, canh phòng tàu thuyền từ khơi xa. Đến năm 1847, vua Thiệu Trị tiếp tục cho xây thêm pháo đài Hòa Duân ở bờ nam để gia tăng năng lực hỏa lực phòng thủ.

Ngày 18 đến ngày 20 tháng 8 năm 1883, hạm đội viễn chinh Pháp do Chuẩn đô đốc Courbet chỉ huy đã nổ súng tấn công dữ dội vào cửa biển Thuận An. Quân đội triều đình nhà Nguyễn dưới sự chỉ huy của các tướng lĩnh Lâm Hoành, Trần Thúc Nhẫn và Lê Chuẩn đã kiên cường chiến đấu bảo vệ Trấn Hải Thành nhưng thất thủ trước hỏa lực vượt trội của đối phương. Sự thất thủ tại cửa biển Thuận An đã mở toang đường tiến binh uy hiếp thẳng vào Kinh đô Huế, dẫn tới việc triều đình nhà Nguyễn phải ký kết Bản Hiệp ước Quý Mùi (Hiệp ước Harmand) vào ngày 25/08/1883, đánh dấu bước ngoặt đau thương trong lịch sử dân tộc. Ngày nay, di tích Trấn Hải Thành tọa lạc sát Bãi biển Thuận An đã được xếp hạng là Di tích Quốc gia đặc biệt trong Quần thể Di tích Cố đô Huế.
```

#### Bổ sung mắm cá rò và mực nháy tại Dòng 97 & 108 (m-02):
- Tại dòng 97, bổ sung: `Bên cạnh nước mắm cá cơm và mắm ruốc, Thuận An đặc biệt nổi tiếng với đặc sản mắm cá rò. Được ủ từ cá rò tươi sống vùng nước lợ cửa biển lên men cùng ớt tươi và thính gạo, mắm cá rò giữ nguyên con, vị đậm đà cay nồng, là món chấm đặc trưng dùng kèm thịt heo luộc và dưa giá.`
- Tại dòng 108, bổ sung: `Tại các hàng quán ven biển, du khách có thể thưởng thức món mực nháy hấp sả gừng tươi giòn ngọt tự nhiên vừa cập cảng cá buổi sớm, cùng các gánh bánh bột lọc tôm biển gói lá chuối nóng hổi.`

#### Cập nhật cảnh báo sạt lở 2026 tại Dòng 131 & 172 (M-04):
- Tại dòng 131, bổ sung: `Vào mùa này, sóng biển dữ dội cao hàng mét kết hợp triều cường thường gây xói lở cục bộ bờ cát (điển hình như các đợt sạt lở khoét sâu chân đường ven biển đoạn Thuận An – Phú Thuận trong năm 2026). Thành phố Huế hiện đang triển khai dự án kè chống sạt lở quy mô 260 tỷ đồng; du khách cần tuân thủ nghiêm ngặt lệnh cấm tắm biển và chú ý biển báo tại các triền cát xói lở.`
- Tại dòng 172, bổ sung gạch đầu dòng: `- **Tránh xa vùng sạt lở và công trường thi công:** Không di chuyển đến gần các mép cát có hiện tượng sụt hàm ếch hoặc khu vực đang thi công đê ngầm giảm sóng và kè bờ.`

---

### 4.2. Bản vá cho `Bãi biển Hải Dương.md`

#### Sửa Dòng 8 (m-04):
```markdown
- **Địa điểm:** Phường Thuận An, thành phố Huế (sáp nhập xã Hải Dương vào phường Thuận An từ ngày 01/01/2025 theo Nghị quyết 1314/NQ-UBTVQH15 và tiếp tục kiện toàn theo Nghị quyết 1675/NQ-UBTVQH15; trước tháng 07/2021 thuộc thị xã Hương Trà, tỉnh Thừa Thiên Huế)
```

#### Sửa Dòng 62 & 110 (m-05):
- Dòng 62 sửa thành: `Trước đây, cộng đồng cư dân vùng đất Hải Dương có nguồn gốc gắn liền với làng cổ Thai Dương Hạ (nhánh bờ bắc hình thành sau biến cố bão Giáp Thìn năm 1904 mở ra luồng cửa biển Thuận An mới).`
- Dòng 110 sửa thành: `Tại ngã tư này, rẽ phải theo bảng chỉ dẫn đi vào trục đường khu dân cư làng Thai Dương Hạ (xã Hải Dương cũ), tiếp tục chạy thẳng...`

#### Loại bỏ từ cấm và tên quán Dì Kiều tại Dòng 72, 84, 90 (M-05, M-06):
- Dòng 72 sửa thành: `Vào mùa rêu xanh đầu năm, bãi đá thấp trở thành một không gian cảnh quan ven biển đặc sắc.`
- Dòng 84 sửa thành: `Nhờ địa thế kẹp giữa biển Đông và đầm phá Tam Giang, Bãi biển Hải Dương sở hữu tầm nhìn cảnh quan thuận lợi vào hai thời khắc chuyển giao của ngày:`
- Dòng 90 sửa thành: `Sau khi dạo biển, du khách có thể ghé vào các hàng quán dân dã trong làng để thưởng thức món bánh ép nóng giòn, cuộn cùng rau sống, dưa leo, dưa chua và chấm ngập trong chén nước mắm ớt chua ngọt thơm lừng.`

#### Đảm bảo Chunk Independence tại Dòng 36, 130, 134, 138, 142 (M-07):
- Dòng 36: `Nằm cách bãi đá thấp Bãi biển Hải Dương một đoạn đi bộ ngắn là khu vực bãi đá cao...`
- Dòng 130: `Tại Bãi biển Hải Dương, bề mặt các khối bê tông tổ ong ở bãi đá thấp khi ngập nước...`
- Dòng 134: `Tại bãi đá cao Bãi biển Hải Dương, các khối bê tông ba chân (tetrapod) được xếp đan xen...`
- Dòng 138: `Khu vực cửa biển và chân đê kè chắn sóng Bãi biển Hải Dương là nơi thường xuyên diễn ra...`
- Dòng 142: `Du khách khi tham quan trên các đê kè Bãi biển Hải Dương vươn ra biển cần chú ý...`

---

### 4.3. Bản vá cho `Bãi biển Vinh Thanh.md`

#### Sửa Dòng 16 & Dòng 78 (M-08):
- Dòng 16 sửa thành: `Bãi biển Vinh Thanh là một bãi biển tự nhiên tọa lạc trên dải cồn cát ven biển phía đông nam của thành phố Huế. Nằm trải dài giữa một bên là Biển Đông và một bên là hệ thống đầm phá Tam Giang – Cầu Hai (đoạn đầm Thủy Tú và đầm Hà Trung), Bãi biển Vinh Thanh sở hữu vị thế địa lý đặc trưng của vùng bãi ngang duyên hải miền Trung...`
- Dòng 78 sửa thành: `Tọa lạc tại bờ đông hướng trọn ra đại dương, Bãi biển Vinh Thanh là địa điểm thuận lợi để chiêm ngưỡng bình minh trên biển tại khu vực Thừa Thiên Huế...`
- Dòng 138 sửa thành: `Môi trường sinh thái và cảnh quan tự nhiên của Bãi biển Vinh Thanh...`

#### Sửa Dòng 26 và nâng cấp Quy tắc an toàn Dòng 127–135 (M-09):
- Dòng 26 sửa thành: `Là bãi tắm vùng bãi ngang mở trực diện ra Biển Đông, thềm cát ven bờ tương đối thoải nhưng có độ dốc đáy biển nhanh hơn so với bãi biển Thuận An, đồng thời chịu tác động trực tiếp của lực sóng vỗ bờ, đòi hỏi người tắm biển cần quan sát kỹ mép nước và không chủ quan trước các vùng cát lún.`
- Tại mục Quy tắc an toàn (Dòng 127–135), bổ sung hai gạch đầu dòng then chốt:
  + `- **Độ dốc bờ biển và hiện tượng hẫng chân:** Bờ biển Vinh Thanh có độ dốc đáy biển lớn hơn so với bãi biển Thuận An; sóng vỗ bờ có lực rút cát mạnh và có thể hình thành các rãnh sụt cát ngầm tạm thời. Người tắm biển (đặc biệt là người bơi yếu và trẻ em) chỉ nên tắm gần mép nước, không đi ra vùng nước sâu quá ngực.`
  + `- **Lưu ý về lực lượng cứu hộ:** Bãi biển Vinh Thanh là bãi tắm dân sinh tự nhiên, chưa được trang bị lực lượng cứu hộ chuyên nghiệp thường trực liên tục như các bãi biển du lịch tập trung. Du khách cần nâng cao ý thức tự bảo vệ, bắt buộc mặc áo phao và chỉ tắm ở khu vực tập trung đông người.`

#### Bổ sung phiên cá cập bến buổi chiều tại Dòng 62 & 148 (m-07):
- Dòng 62 bổ sung: `Bên cạnh phiên chợ sáng sớm, vào khoảng 15h00 đến 16h30 chiều, các thuyền thúng đi câu lộng ban ngày trở về cập bãi, cung cấp nguồn hải sản tươi rói phục vụ trực tiếp cho du khách tắm biển buổi chiều.`

---

### 4.4. Bản vá cho `Bãi biển Phú Diên.md`

#### Chuẩn hóa H2 theo Chunk Independence (M-12):
Thay toàn bộ H2 generic bằng:
- `## Thông tin chung về Bãi biển Phú Diên`
- `## Tổng quan về Bãi biển Phú Diên`
- `## Địa hình bờ biển và cảnh quan cồn cát Bãi biển Phú Diên`
- `## Mối liên kết không gian giữa Bãi biển Phú Diên và Tháp Chăm Phú Diên`
- `## Hệ sinh thái và dải rừng phi lao phòng hộ ven Bãi biển Phú Diên`
- `## Đời sống cộng đồng và sinh kế làng chài Bãi biển Phú Diên`
- `## Trải nghiệm và hoạt động đặc trưng tại Bãi biển Phú Diên`
- `## Mùa biển và điều kiện thời tiết tại Bãi biển Phú Diên`
- `## Tuyến tiếp cận và phương tiện di chuyển đến Bãi biển Phú Diên`
- `## An toàn tắm biển và bảo vệ môi trường cồn cát Bãi biển Phú Diên`
- `## Thông tin hướng dẫn du khách tại Bãi biển Phú Diên`

#### Hiệu đính lộ trình di chuyển Dòng 58–59 (M-10, M-11):
```markdown
- **Tuyến đường di chuyển chính:**
  + *Lộ trình qua Thuận An:* Từ trung tâm thành phố Huế, di chuyển theo Quốc lộ 49 (đường Phạm Văn Đồng) về phía đông bắc đến ngã ba giao cắt với Quốc lộ 49B tại phường Thuận An (khu vực cầu Diên Trường 1), sau đó rẽ phải vào Quốc lộ 49B chạy xuôi theo hướng đông nam dọc dải cồn cát ven biển qua các xã Phú Hải, Phú Diên (thuộc xã Phú Vinh) để đến Bãi biển Phú Diên. Tuyến đường này không đi qua cầu vượt cửa biển Thuận An.
  + *Lộ trình qua đầm Tam Giang:* Từ khu vực phía nam thành phố Huế, di chuyển theo trục đường Tỉnh lộ 10 hoặc Tỉnh lộ 10B qua thị trấn Phú Đa, vượt cầu Trường Hà bắc qua đầm Thủy Tú sang xã Phú Vinh (khu vực Vinh Thanh cũ), sau đó rẽ trái vào Quốc lộ 49B đi tiếp khoảng 5 km theo hướng bắc để đến bãi biển và khu di tích Tháp Chăm.
```

#### Chuẩn hóa dữ kiện Tháp Chăm Phú Diên Dòng 16, 26 (M-13):
- Dòng 16: Sửa "văn hóa tiền phong" thành "di sản văn hóa Champa cổ".
- Dòng 26 thay thế thành:
```markdown
Ngày 18 tháng 4 năm 2001, trong quá trình khai thác quặng titan ven bờ biển, nhóm công nhân địa phương đã tình cờ phát hiện khối tháp gạch cổ bị vùi lấp ở độ sâu 5 đến 7 mét dưới lòng cồn cát biển, cách mép nước hiện tại chỉ khoảng 120 mét. Công trình có niên đại khoảng thế kỷ VIII, được Bộ Văn hóa – Thông tin xếp hạng Di tích kiến trúc nghệ thuật cấp quốc gia theo Quyết định số 52/2001/QĐ-BVHTT ngày 28/12/2001.

Năm 2022, di tích tháp Chăm này được Tổ chức Kỷ lục Việt Nam (VietKings) và Liên minh Kỷ lục Thế giới (WorldKings) chính thức xác lập kỷ lục: "Tháp Chăm cổ bằng gạch chìm sâu dưới cồn cát ven biển được khai quật và bảo tồn đầu tiên trên thế giới" (lưu ý kỷ lục thế giới do tổ chức WorldKings xác lập, không thuộc hệ thống Kỷ lục Guinness thế giới).
```

---

### 4.5. Bản vá cho `Bãi biển Hàm Rồng.md`

#### Loại bỏ mỹ từ quảng bá và tiết chế cảm tính (M-14):
- Dòng 16 sửa thành: `Bãi biển Hàm Rồng là một trong những cảnh quan duyên hải nguyên sơ tiêu biểu của thành phố Huế, tọa lạc tại xã Vinh Lộc...`
- Dòng 18 sửa thành: `...vừa chắn sóng tạo nên những vũng vịnh kín gió với làn nước trong, vừa tạo điều kiện cho lớp rêu xanh phát triển trên bề mặt đá vào mùa đông – xuân.`
- Dòng 99 sửa thành: `Địa hình và hướng nhìn mở rộng của Bãi biển Hàm Rồng mang lại vị trí quan sát thuận lợi cho cả bình minh và hoàng hôn:`
- Dòng 108 sửa thành: `Khu vực bãi đá trầm tích vươn dài ra biển là điểm thu hút người yêu thích chụp ảnh phong cảnh tự nhiên.`
- Dòng 110 sửa thành: `...trở thành bối cảnh đặc trưng cho các bộ ảnh tư liệu nghệ thuật, ảnh cưới ngoại cảnh và phong cảnh duyên hải.`

#### Bổ sung di tích Phế tích Tháp Chăm Linh Thái & Chùa Thánh Duyên (M-15):
- Tại Dòng 48, bổ sung: `Bên cạnh giá trị cảnh quan, núi Linh Thái còn lưu giữ phế tích Tháp Chăm Linh Thái có niên đại từ thế kỷ XI–XII trên đỉnh núi. Đây là nơi phát hiện bộ Chóp tháp Chăm Pa Linh Thái – hiện vật đã được Thủ tướng Chính phủ công nhận là Bảo vật Quốc gia vào năm 2020 theo Quyết định số 2283/QĐ-TTg.`
- Tại Dòng 71, hiệu đính: `...Vua cũng cho xây dựng, tôn tạo chùa Thánh Duyên trên ngọn núi Túy Vân kế cận cửa biển, xếp cảnh quan "Vân Sơn thắng tích" vào hàng danh thắng tiêu biểu đất Thần kinh (chùa Thánh Duyên đã được Bộ Văn hóa – Thông tin xếp hạng Di tích Lịch sử – Văn hóa cấp Quốc gia năm 1996 theo Quyết định 398-QĐ/VH).`

#### Bổ sung mô tả Động Hàm Rùa tại Dòng 34 (M-16):
- Bổ sung vào cuối dòng 34: `Đặc biệt, tại khu vực bờ đá giáp chân núi, các khối đá tảng xếp chồng so le kiến tạo nên những hốc đá và vòm đá tự nhiên ăn sâu vào vách núi, được cư dân địa phương gọi là động Hàm Rùa. Đây là nét địa hình độc đáo hình thành do quá trình sóng biển khoét mòn chân núi đá qua thời gian dài.`

#### Bổ sung đặc sản cá ong, tôm bạc, vẹm xanh tại Dòng 87–88 (m-13):
- Dòng 87 bổ sung: `Cá mú biển, cá hồng, cá hanh, cá dìa bông, cá ong (cá căng đặc sản vùng cửa biển), cá bớp, cá đuối...`
- Dòng 88 bổ sung: `Mực cơm, mực lá nháy tươi rói, tôm bạc đầm phá, tôm hùm đá, ghẹ xanh, cua biển gạch, sò điệp, vẹm xanh và hàu đá cạy từ các vách đá chân núi Linh Thái.`

---

## 5. Đồng bộ hóa Evidence (`tourism-research-evidence.md`)

Sau khi hoàn tất hiệu chỉnh 5 tệp nội dung trên, Implementer cần đồng bộ các dữ kiện thẩm định vào các Mục XI, XII, XIII, XIV, XV của `knowledge-base-hue/meta/tourism-research-evidence.md`:
1. **Mục XI (Thuận An):** Ghi rõ mốc 1834 Minh Mạng đổi tên Trấn Hải Thành & dựng Quan Hải Lâu; cập nhật dự án kè 260 tỷ chống sạt lở 2026.
2. **Mục XII (Hải Dương):** Cập nhật chuỗi Nghị quyết 1314 và 1675; loại bỏ quán Dì Kiều khỏi bờ bắc; ghi rõ cầu vượt cửa biển thông xe kỹ thuật 30/04/2026.
3. **Mục XIII (Vinh Thanh):** Ghi nhận độ dốc thềm cát và lưu ý thiếu cứu hộ thường trực; bổ sung chợ cá buổi chiều 15h–16h30.
4. **Mục XIV (Phú Diên):** Ghi rõ ngày phát hiện 18/04/2001, Quyết định 52/2001/QĐ-BVHTT, kỷ lục thế giới WorldKings 2022 (không phải Guinness), bổ sung vai trò kết nối của Cầu Trường Hà.
5. **Mục XV (Hàm Rồng):** Ghi rõ chùa Thánh Duyên (Di tích Quốc gia 1996) ở núi Túy Vân; Phế tích tháp Chăm Linh Thái (Bảo vật Quốc gia 2020) ở núi Linh Thái; mô tả Động Hàm Rùa; bổ sung cá ong, tôm bạc, vẹm xanh.

---

## 6. Tiêu chí nghiệm thu (Acceptance Criteria)

Tập tin hiệu chỉnh sẽ được Reviewer nghiệm thu đạt yêu cầu (PASS) khi:
1. Đã giải quyết triệt để 16 lỗi Major và 15 lỗi Minor theo đúng bảng Action Items tại Mục 4.
2. Không còn bất kỳ từ ngữ quảng bá bị cấm nào theo danh mục tại `meta/tourism-template.md` Mục 2.6.
3. Toàn bộ các tiêu đề H2/H3 đều bảo đảm 100% tính độc lập chunking (Chunk self-containment).
4. Các chỉ dẫn giao thông (Cầu Thuận An, Cầu Trường Hà) và dữ kiện di sản (Quan Hải Lâu, Tháp Chăm WorldKings, Bảo vật Quốc gia Linh Thái) đạt độ chính xác thực tế tuyệt đối mốc tháng 09/2026.
5. Không có lỗi định dạng Markdown (`git diff --check` sạch).
