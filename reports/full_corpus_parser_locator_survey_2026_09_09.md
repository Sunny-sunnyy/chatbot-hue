# BÁO CÁO KHẢO SÁT PARSER VÀ SOURCE LOCATOR CHO FULL-CORPUS HUẾ
*(Bản cập nhật và khắc phục toàn diện theo Codex Review Lượt 3: R1 Closure, ngày 2026-09-09)*

**Dự án:** `/home/minhhieu/hue_rag`  
**Ngày thực hiện:** 2026-09-09  
**Vai trò:** Implementer  
**Nhiệm vụ:** Sửa khảo sát parser/source locator theo Review Correction Lượt 3 (`CURRENT_HANDOFF.md` và `reports/full_corpus_parser_locator_codex_review_2026_09_09.md` §8).  
**Hợp đồng khảo sát gốc:** `session_prompt/FULL_CORPUS_PARSER_LOCATOR_SURVEY_HANDOFF.md`  
**Trạng thái worktree:** Worktree **KHÔNG sạch** (có sẵn thay đổi tại `guides/README.md`, `guides/phase_2_foods_markdown_chunking.md`, `session_prompt/CURRENT_HANDOFF.md` cùng các tài liệu và reports untracked; được giữ nguyên vẹn ngoài phạm vi nhiệm vụ).  
**Phạm vi sửa đổi được cấp phép:** Đúng 3 artifacts:
- `reports/full_corpus_parser_locator_survey_2026_09_09.md` (Báo cáo này)
- `reports/artifacts/full_corpus_parser_locator_survey_2026_09_09.py` (Script khảo sát, probe và kiểm định)
- `reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json` (Dữ liệu mẫu, spans, probe results, bảng hạch toán coverage và kết quả kiểm định)

---

## 1. CÂU HỎI KHẢO SÁT VÀ KẾT LUẬN ĐIỀU HÀNH

### 1.1. Câu hỏi khảo sát
> `markdown-it-py` có giúp nhận diện các khối Markdown cần thiết và lấy lại đúng spans nguyên văn từ corpus hiện tại bằng cách trực tiếp, dễ hiểu không? Đồng thời phân định phần cấu trúc parser biết và quan hệ điều kiện cần Reviewer/chỉ dẫn riêng quyết định như thế nào?

### 1.2. Kết luận điều hành và đối chiếu sửa đổi R1–R3 (F1–F3)

1. **Khắc phục hoàn thiện R1 (Hoàn thiện toàn bộ các phép so selectors trong Probe Condition Mapping):**
   - **So sánh toàn bộ signature cho Rule "Không bao gồm" (Ca Huế):** Thay vì chỉ kiểm tra tiền tố `startswith`, probe đối chiếu **toàn văn 100%** khối list item với hằng số `EXPECTED_CA_HUE_EXCL_SIG` được khai báo độc lập.
   - **Lọc điều kiện và signature độc lập cho Rule "Chi phí":**
     + Thực sự lọc điều kiện theo `heading_path == []` (khối intro xuất hiện ở đầu file trước mọi H2 theo quy ước bỏ H1).
     + Hằng số kỳ vọng `EXPECTED_CHI_PHI_INTRO_SIG` được định nghĩa độc lập (bảo toàn nguyên văn 2 ký tự `\n` nội bộ), không lấy lại lát cắt nguồn `cp_text[23:261]` làm expected cho chính phép kiểm tra.
   - **Phân giải Target A/B và 3 bảng Chi phí theo Full Ancestor Heading Path:**
     + Khi tra cứu các bảng đích A và B tại Ca Huế, probe đối chiếu toàn bộ ngăn xếp phân cấp `['2. Ca Huế trên sông Hương và dịch vụ thuyền rồng', '2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế', 'A. Vé khách lẻ...']` và `[..., 'B. Thuê trọn gói...']` (không chỉ tìm kiếm tên H4 toàn file).
     + Cả 3 bảng dự toán tại Chi phí được tra cứu chính xác theo đường dẫn `['Dự toán một ngày tại Huế']`, `['Dự toán hai ngày một đêm tại Huế']`, `['Dự toán ba ngày hai đêm tại Huế']`.
   - **Tính toán ranh giới dừng (Stop Boundary):** Điểm dừng được kiểm tra thực tế: toàn bộ 4 hàng của Mục A kết thúc tại offset 11810, nằm trước vị trí bắt đầu heading Mục B (offset 12289); số lượng hàng giao thoa giữa Mục A và Mục B bằng 0; phép lọc theo target path của Rule 2 trả về đúng 0 hàng trong Mục B.
   - Kết quả: Toàn bộ 3 rules probe đều đạt trạng thái **RESOLVED_UNIQUE / PASS** với counts thực tế được xác nhận trước khi kết luận.

2. **Bảo toàn R2 (Hai chunk kết hợp từ Output Parser & Flat Schema):**
   - Đã đóng từ Lượt 2 và được giữ nguyên vẹn: Các thành phần `lead_part`, `header_part`, `vn_row_part`, `qt_row_part`, `exclusions_part` lấy động từ parser-resolved spans và lines.
   - Schema `evidence_parts` phẳng chuẩn contract: `[{"role": "condition"|"header"|"body", "start": int, "end": int, "text": str}, ...]`.
   - Ranh giới hàng đúng: Khách Việt Nam `[10901, 11141)` (240 ký tự) và Khách quốc tế `[11142, 11317)` (175 ký tự).
   - Token counts cho 2 input đã sửa tiếp tục ghi nhận rõ ràng là **chưa đo** (`not_measured`), không tái sử dụng số đo cũ.

3. **Bảo toàn và chuẩn hóa R3 (Đính chính Factual về Hải Vân Quan):**
   - Đã đóng từ Lượt 2 và chuẩn hóa câu chữ theo Reviewer:
     + **Thời gian áp dụng thu phí chính thức:** Bắt đầu từ ngày **`02/06/2026`** đến hết ngày **`31/12/2028`** (giai đoạn thí điểm 3 năm do thành phố Huế trực tiếp quản lý), căn cứ Nghị quyết 05/2026/NQ-HĐND ngày 22/05/2026 của HĐND thành phố Huế (không phải 01/01/2025).
     + **Đơn vị trực tiếp quản lý và thu phí:** **Trung tâm Bảo tồn Di tích Cố đô Huế** (100% nguồn thu để lại cho đơn vị này).
     + **Chuẩn hóa ghi chú địa giới:** Nguồn chỉ nhắc tên *"quận Liên Chiểu"* trong chú thích lịch sử phân định địa giới hành chính cũ của Đà Nẵng trước ngày 01/07/2025 (*"trước ngày 01/07/2025 là phường Hòa Hiệp Bắc, quận Liên Chiểu"*), hoàn toàn **không có chữ "UBND"** hay vai trò vận hành/thu phí di tích nào được gán cho quận Liên Chiểu trong đoạn nguồn.
     + Trích dẫn nguyên văn 4 đoạn nguồn cốt lõi chứng minh Section 1 mang thông tin trả lời hữu ích, không thể loại bỏ như `pure_administrative`.

4. **Tính tái lập độc lập & Giới hạn Coverage (F2):**
   - Reproducibility test 2-pass trên cả 6 files: 100% token maps trùng khớp tuyệt đối (PASS).
   - Validator kiểm định **40/40 parts** xuất hiện trong artifact: 100% bounds hợp lệ và exact-match tuyệt đối với nguồn.
   - Giới hạn: Bảng hạch toán coverage là minh họa tĩnh trên các vùng mục tiêu; validator 40/40 là kết quả duyệt cho 40 parts văn bản nguồn cụ thể được kiểm tra (không bao gồm các probe records dùng cấu trúc `span: [start, end]`); phiên bản parser đọc trực tiếp từ `markdown_it.__version__` (`4.2.0`).

---

## 2. MÔI TRƯỜNG, PHIÊN BẢN VÀ CẤU HÌNH THỰC THI

- **Lệnh thực thi:**
  ```bash
  uv run --no-sync python reports/artifacts/full_corpus_parser_locator_survey_2026_09_09.py
  ```
- **Phiên bản gói cài đặt thực tế (đọc trực tiếp từ runtime package):**
  - `markdown-it-py`: phiên bản **4.2.0** (đọc qua `markdown_it.__version__`, không dùng chuỗi fallback).
  - `mistune`: phiên bản **3.3.4** (có sẵn trong môi trường ảo).
- **Cấu hình parser chuẩn:**
  ```python
  from markdown_it import MarkdownIt
  md = MarkdownIt().enable('table')
  ```

---

## 3. BẢNG ĐỐI CHIẾU CÁC CẤU TRÚC MARKDOWN TRÊN PARSER

| Cấu trúc Markdown | Token Type chính | Có `Token.map`? | Đặc điểm hành vi và giải pháp kỹ thuật |
| :--- | :--- | :---: | :--- |
| **Tiêu đề (H1–H4)** | `heading_open` | **CÓ** `[sl, el]` | `sl` là dòng chứa `#`, `el = sl + 1`. Map chính xác dòng tiêu đề. Lập được heading stack và heading path phân cấp (quy ước bỏ H1 để tra cứu nhất quán). |
| **Đoạn văn (Paragraph)** | `paragraph_open` | **CÓ** `[sl, el]` | Map từ dòng bắt đầu đến kết thúc. Nhận diện chuẩn xác các đoạn văn nằm ở giữa cấp heading và đoạn intro đầu file (`heading_path == []`). |
| **Danh sách (List cha & con)** | `bullet_list_open`, `list_item_open` | **CÓ** `[sl, el]` | **Đặc tính lồng nhau:** `list_item_open` của mục cha có map bao trùm toàn bộ các dòng con bên trong (ví dụ: mục *Thời gian tổ chức* map `[7, 10]`). |
| **Bảng tổng thể (Table)** | `table_open` | **CÓ** `[sl, el]` | Map bao trùm toàn bộ bảng từ header đến hết hàng dữ liệu cuối cùng. |
| **Table Header** | `thead_open` | **CÓ** `[sl, el]` | `thead_open.map` trỏ vào dòng tiêu đề cột (`[sl, sl+1]`). Dòng phân cách cú pháp `|---|---|` nằm ngay sau đó (`sl+1`).<br>👉 Range dòng lấy trọn vẹn header và delimiter: `[thead_open.map[0], thead_open.map[1] + 1]`. |
| **Từng hàng của bảng (Table Row)** | `tr_open` | **CÓ** `[sl, el]` | **Điểm mạnh then chốt:** Mọi hàng dữ liệu trong `tbody` đều có `tr_open.map = [sl, sl+1]`. Định vị và cắt rời **từng hàng riêng lẻ** bằng Unicode span offset độc lập. |
| **Ô của bảng (Cell: th, td)** | `th_open`, `td_open` | **KHÔNG** | Parser không cấp map riêng cho từng ô cột. Không ảnh hưởng vì ranh giới chia chunk là cấp độ hàng (`tr`). |
| **HTML bên trong bảng (`<br>`)** | `inline` | N/A | Các thẻ HTML nội dòng như `<br>` trong ô bảng (ví dụ: bảng giá trẻ em Ca Huế) được parser giữ nguyên vẹn, không làm vỡ cấu trúc hàng. |
| **Cảnh báo / Trích dẫn (Blockquote)**| `blockquote_open` | **CÓ** `[sl, el]` | Map chính xác từ dòng `>` đầu tiên đến hết khối trích dẫn (ví dụ: blockquote `[!WARNING]` tại Vé Ca Huế có map `[9, 11]`). |
| **Đường phân cách ngang (HR)** | `hr` | **CÓ** `[sl, el]` | Map đúng dòng chứa `---`. |
| **Dòng chỉ chứa ảnh (Image-only)** | `paragraph_open` (chứa `image`) | **CÓ** `[sl, el]` | Nhận diện dòng ảnh như một paragraph có token con `image`. Cho phép phát hiện và loại bỏ dòng ảnh cục bộ, bảo toàn hai vùng văn bản trước/sau. |
| **Dòng trống ở cuối khối** | N/A | Gộp vào `el` | Hàm `get_block_span` với cờ `trim_trailing_blank=True` lùi dòng kết thúc về dòng văn bản có nghĩa cuối cùng, tránh khoảng trắng thừa. |

---

## 4. KẾT QUẢ KHẢO SÁT VÀ ĐÍNH CHÍNH RANH GIỚI F1 & FACTUAL R3

Toàn bộ dữ liệu kiểm chứng và spans trích xuất thực tế được lưu tại artifact:  
[reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json](file:///home/minhhieu/hue_rag/reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json).

### 4.1. Vùng 1: `festivals/festival/Hội xuân Gia Lạc.md` (Danh sách cha/con lồng nhau)
- **Đặc điểm:** Danh sách thông tin chung chứa mục cha (`- **Thời gian tổ chức:**`) và các gạch đầu dòng con lùi lề (`  - *Truyền thống lịch sử:* ...`, `  - *Giai đoạn hiện nay:* ...`).
- **Kết quả parser:**
  - Mục `- **Thời gian tổ chức:**` có `token_map = [7, 10]`, span `[312, 590)` (278 ký tự).
  - Mục `- **Nơi tổ chức:**` có `token_map = [10, 13]`, span `[591, 997)` (406 ký tự).
- **Đánh giá:** `markdown-it-py` bảo toàn hoàn hảo quan hệ cha-con; khi lấy span theo `list_item_open` cha, toàn bộ nội dung con được trích xuất nguyên vẹn 100%.

### 4.2. Vùng 2: `heritages/heritage/Đại Nội Huế.md` (Đoạn văn giữa cấp heading & Ngọ Môn)
- **Đặc điểm:** Đoạn văn dòng 68 (*"Hoàng thành Huế là khu vực chứa đựng các công trình biểu tượng..."*) nằm giữa H2 `## Các công trình kiến trúc hạt nhân...` và H3 `### Ngọ Môn`.
- **Kết quả parser:**
  - H2 `## Các công trình kiến trúc hạt nhân...`: span `[10004, 10056)`.
  - Đoạn văn giữa cấp: Parser sinh riêng token `paragraph_open` độc lập, map `[67, 68]`, span `[10058, 10204)` (146 ký tự).
  - H3 `### Ngọ Môn`: map `[69, 70]`, span `[10206, 10217)`.
  - Đoạn mô tả Ngọ Môn: map `[71, 72]`, span `[10219, 10550)`.
  - Danh sách cấu trúc đài nền & Lầu Ngũ Phụng: map `[73, 80]`, span `[10552, 11945)`.
- **Đánh giá:** Parser không làm mất đoạn văn giữa cấp. Đoạn này có thể đóng vai trò context lead cho section H2.

### 4.3. Vùng 3: `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` (Đính chính F1)
#### Đính chính sai lệch ranh giới hàng Ca Huế (F1):
- **Phát hiện lỗi trong khảo sát tokenizer Lượt 3 cũ:**
  + Mẫu `ca_hue_p3b_lead_chunk_1a` dùng span `[10901, 11158)` (257 ký tự): bị cắt lấn 17 ký tự sang dòng tiếp theo (`\n| **Khách quốc t`).
  + Mẫu `ca_hue_p3b_lead_chunk_1b` dùng span `[11159, 11317)` (158 ký tự): bị cắt mất 17 ký tự đầu dòng, dẫn đến text bắt đầu bằng `** | 150.000` (mất nhãn `| **Khách quốc tế`).
  + Hai mẫu P3A tương ứng (`ca_hue_p3a_chunk_1` và `ca_hue_p3a_chunk_2`) cũng bị cắt sai ranh giới tương tự.
- **Ranh giới đúng được xác định từ parser:**
  + Header bảng kèm delimiter: line 110–112, span `[10760, 10900)` (140 ký tự).
  + Hàng 1 - Khách Việt Nam: line 112, span `[10901, 11141)` (240 ký tự). Kết thúc chuẩn xác tại ký tự `|` cuối hàng, trước newline.
  + Hàng 2 - Khách quốc tế: line 113, span `[11142, 11317)` (175 ký tự). Bắt đầu chuẩn xác từ ký tự `|` đầu dòng và bảo toàn trọn vẹn nhãn `| **Khách quốc tế**`.
  + Hàng 3 - Trẻ em theo chiều cao (chứa `<br>`): line 114, span `[11318, 11581)` (263 ký tự).
  + Hàng 4 - Trẻ em theo độ tuổi (chứa `<br>`): line 115, span `[11582, 11810)` (228 ký tự).
- **Tách biệt Exact Substring Match với Ranh giới Ngữ nghĩa:**
  Lát cắt `text[10901:11158]` trong dữ liệu cũ vẫn trả về chuỗi con có thật trong file (nên từng pass kiểm tra substring), nhưng ranh giới của nó bị sai (chứa một mẩu của hàng sau). Exact match chỉ chứng minh trích xuất đúng lát cắt từ file, không chứng minh lát cắt đó có đúng ranh giới ngữ nghĩa của hàng dữ liệu hay không.
- **Tác động tới Token Counts:**
  Các số đo token cũ (E5 298/HuyDang 230/MiniLM long 462 cho VN và 260/203/418 cho QT) được đo trên khối input sai ranh giới; do đó **không chứng minh** độ dài thực tế của hai hàng hoàn chỉnh đã sửa. Token counts cho 2 input đã sửa được ghi nhận là **chưa đo** (`not_measured`).

### 4.4. Vùng 4: `travel/services/Chi phí du lịch Huế.md` (Intro hạn mức kế hoạch & 3 Bảng dự toán)
- **Đoạn Intro (lines 2–5):** `token_map = [2, 5]`, span `[23, 261)` (238 ký tự), `heading_path = []` (xuất hiện trước mọi H2). Đoạn này chứa 2 ký tự xuống dòng `\n` nội bộ.
- **3 Bảng dự toán chi phí du lịch tại Huế:**
  1. *Dự toán một ngày tại Huế:* Hàng tổng `| **Tổng tại Huế** | **280.000–850.000** | ... |` tại line 83, span `[3066, 3158)` (92 ký tự).
  2. *Dự toán hai ngày một đêm tại Huế:* Hàng tổng `| **Tổng tại Huế** | **710.000–1.700.000** | ... |` tại line 98, span `[3871, 3967)` (96 ký tự).
  3. *Dự toán ba ngày hai đêm tại Huế:* Hàng tổng `| **Tổng tại Huế** | **1.140.000–2.650.000** | ... |` tại line 113, span `[4666, 4765)` (99 ký tự).
- **Đánh giá:** Đoạn intro nằm cách xa các bảng dự toán (từ 70 đến 110 dòng). Việc gắn đoạn intro này để bảo vệ bản chất "hạn mức kế hoạch" cho cả 3 bảng dự toán là yêu cầu nghiệp vụ cần thực hiện qua declarative mapping.

### 4.5. Vùng 5: `travel/tickets/Vé tham quan Hải Vân Quan.md` (Đính chính Factual R3)
- **Mục 1:** `## Căn cứ pháp lý và cơ chế phối hợp quản lý liên tỉnh` (span `[29, 83)`):
  *Đính chính phân tích và dữ liệu factual:* Mặc dù chứa số hiệu Nghị quyết 05/2026/NQ-HĐND ngày 22/05/2026 của HĐND thành phố Huế, section này **đồng thời chứa các thông tin trả lời hữu ích**:
  + **Thời gian áp dụng thu phí chính thức:** Bắt đầu từ ngày **`02/06/2026`** đến hết ngày **`31/12/2028`** (giai đoạn thí điểm 3 năm do thành phố Huế trực tiếp quản lý). *(Đính chính: Báo cáo Lượt 1 ghi nhầm 01/01/2025; ngày 01/01/2029 mới là thời điểm bàn giao tiếp theo cho Đà Nẵng).*
  + **Cơ quan trực tiếp quản lý và tổ chức thu phí:** **Trung tâm Bảo tồn Di tích Cố đô Huế** (đơn vị được UBND thành phố Huế giao trực tiếp quản lý, đón tiếp khách và tổ chức thu phí; toàn bộ 100% nguồn thu để lại cho đơn vị này).
  + **Chuẩn hóa ghi chú địa giới:** Nguồn chỉ nhắc tên *"quận Liên Chiểu"* trong chú thích lịch sử phân định địa giới hành chính cũ của Đà Nẵng trước ngày 01/07/2025 (*"trước ngày 01/07/2025 là phường Hòa Hiệp Bắc, quận Liên Chiểu"*), hoàn toàn **không có chữ "UBND"** hay vai trò vận hành/thu phí di tích nào được gán cho quận Liên Chiểu trong đoạn nguồn.
  + *Trích dẫn nguyên văn nguồn chứng minh:*
    > - *"Ngày có hiệu lực thi hành: Chính thức áp dụng thu phí từ ngày 02/06/2026."*
    > - *"Thời hạn áp dụng chính sách: Áp dụng thí điểm đến hết ngày 31/12/2028 (giai đoạn 3 năm do thành phố Huế trực tiếp quản lý)."*
    > - *"Trong giai đoạn từ ngày 02/06/2026 đến hết ngày 31/12/2028, Ủy ban nhân dân thành phố Huế chịu trách nhiệm quản lý, bảo vệ và vận hành di tích; đơn vị được giao trực tiếp quản lý, đón tiếp khách và tổ chức thu phí là Trung tâm Bảo tồn Di tích Cố đô Huế."*
    > - *"Cơ quan thu phí hiện hành: Trung tâm Bảo tồn Di tích Cố đô Huế."*
  + *Kết luận:* Không thể coi Mục 1 là `pure_administrative` để loại bỏ tùy tiện; Reviewer sẽ quyết định phạm vi trích xuất factual.
- **Mục 2:** `## Ranh giới pháp lý và các cảnh báo quan trọng` (span `[2998, 3045)`):
  **BẮT BUỘC GIỮ LÀM ANSWER CONTENT.** Chứa 4 cảnh báo cốt tử cho du khách: không thuộc quần thể Huế, không áp dụng vé combo 530k/600k, trẻ em < 13 tuổi (hoặc chiều cao < 1,3 m) được **miễn phí hoàn toàn** (khác biệt căn bản với quy chuẩn 7–12 tuổi của Quần thể Huế), thời hạn thí điểm đến 31/12/2028.
- **Mục 3:** `## Biểu phí tham quan di tích Hải Vân Quan`: Biểu phí 70k/35k/0k (Answer content cốt lõi).
- **Mục 4:** `## Mô hình dữ liệu chuẩn hóa của vé tham quan Hải Vân Quan`: Bảng nghiên cứu chuẩn hóa 14 trường. Chứa thông tin về quyền lợi và chính sách giảm phí; Reviewer sẽ xem xét xử lý để tránh trùng lặp với bảng biểu phí phía trên.

### 4.6. Vùng 6: Xử lý Dòng ảnh (Image-only line) và Blockquote Cảnh báo
- **Blockquote:** Trích từ `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` (span `[1280, 1748)`): Token `blockquote_open` map `[9, 11]`, trích xuất trọn vẹn cảnh báo thương mại `> [!WARNING] ...`.
- **Dòng chỉ chứa ảnh (Image-only):** Trích từ `foods/restaurants/quan bun bo me keo.md` (line 16, span `[474, 621)`):
  + Dòng ảnh bị loại bỏ cục bộ tại span `[474, 621)`.
  + Span văn bản trước ảnh: span `[318, 472)` (154 ký tự).
  + Span văn bản sau ảnh: span `[623, 1073)` (450 ký tự).
  + *Ghi chú giới hạn phạm vi:* Đây là minh họa kỹ thuật trên một mẫu dòng ảnh cụ thể với vị trí xác định; chưa phải bộ lọc ảnh tự động tổng quát cho toàn bộ corpus.

---

## 5. MINH HỌA 2 CHUNK KẾT HỢP HOÀN CHỈNH CHO VN VÀ QT (R2 / F1 / F2)

Toàn bộ các thành phần trong 2 chunk kết hợp được **tái sử dụng trực tiếp từ kết quả resolve của parser** (không dùng bất kỳ literal offset nào). Schema `evidence_parts` tuân thủ đúng dạng phẳng với các role `condition`, `header`, `body`:

### 5.1. Chunk 1: Vé khách Việt Nam kèm đầy đủ điều kiện
- **`chunk_id`:** `ca_hue_tour_ghep_vn_with_lead_and_exclusions`
- **`source`:** `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`
- **`title`:** `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương`
- **`heading_path`:**
  1. `2. Ca Huế trên sông Hương và dịch vụ thuyền rồng`
  2. `2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế`
  3. `A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)`
- **`evidence_parts` (Schema phẳng chuẩn: `[{"role": str, "start": int, "end": int, "text": str}]`):**
  1. `{"role": "condition", "start": 10409, "end": 10591, "text": "Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu (Thuyền Rồng Huế, Ca Huế Trên Sông Hương - Lá Quê Travel, Đại Việt Tourist) tại thời điểm tháng 09/2026:"}`
  2. `{"role": "header", "start": 10760, "end": 10900, "text": "| Hạng mục đối tượng | Mức giá niêm yết khảo sát | Đơn vị tính | Thành phần bao gồm | Ghi chú & Điều kiện áp dụng |\n|---|---:|:---:|---|---|"}`
  3. `{"role": "body", "start": 10901, "end": 11141, "text": "| **Khách Việt Nam** | 100.000 – 130.000 | đồng/người/suất | Chỗ ngồi thuyền rồng, xem Ca Huế 50 phút, ngắm sông Hương, 01 đèn hoa đăng | Giá phổ biến thực tế là 100.000 đồng; một số đơn vị niêm yết giá gốc 130.000đ khuyến mại về 100.000đ |"}`
  4. `{"role": "condition", "start": 12117, "end": 12287, "text": "- **Không bao gồm:** Phương tiện đưa đón tận nơi (khách tự di chuyển đến Bến Tòa Khâm), ăn uống cá nhân trên thuyền, tiền tip bồi dưỡng nghệ sĩ (không bắt buộc, tùy tâm)."}`
- **`search_text_characters`:** 931 ký tự.
- **`tokens`:** `status: not_measured` (Chưa đo; không tái sử dụng counts 298/230/462 cũ).
- **Đính chính ranh giới (F1 / R2):** Trích xuất tự động từ parser, span `[10901, 11141)` (240 ký tự), dừng chính xác trước newline `\n`.

### 5.2. Chunk 2: Vé khách quốc tế kèm đầy đủ điều kiện
- **`chunk_id`:** `ca_hue_tour_ghep_qt_with_lead_and_exclusions`
- **`source`:** `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`
- **`title`:** `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương`
- **`heading_path`:** (tương tự mục 5.1)
- **`evidence_parts` (Schema phẳng chuẩn):**
  1. `{"role": "condition", "start": 10409, "end": 10591, "text": "Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu (Thuyền Rồng Huế, Ca Huế Trên Sông Hương - Lá Quê Travel, Đại Việt Tourist) tại thời điểm tháng 09/2026:"}`
  2. `{"role": "header", "start": 10760, "end": 10900, "text": "| Hạng mục đối tượng | Mức giá niêm yết khảo sát | Đơn vị tính | Thành phần bao gồm | Ghi chú & Điều kiện áp dụng |\n|---|---:|:---:|---|---|"}`
  3. `{"role": "body", "start": 11142, "end": 11317, "text": "| **Khách quốc tế** | 150.000 | đồng/người/suất | Chỗ ngồi thuyền rồng, xem Ca Huế 50 phút, hoa đăng thả sông, thuyết minh song ngữ ngắn | Áp dụng cho khách người nước ngoài |"}`
  4. `{"role": "condition", "start": 12117, "end": 12287, "text": "- **Không bao gồm:** Phương tiện đưa đón tận nơi (khách tự di chuyển đến Bến Tòa Khâm), ăn uống cá nhân trên thuyền, tiền tip bồi dưỡng nghệ sĩ (không bắt buộc, tùy tâm)."}`
- **`search_text_characters`:** 866 ký tự.
- **`tokens`:** `status: not_measured` (Chưa đo; không tái sử dụng counts 260/203/418 cũ).
- **Đính chính ranh giới (F1 / R2):** Trích xuất tự động từ parser, span `[11142, 11317)` (175 ký tự), bảo toàn trọn vẹn nhãn `| **Khách quốc tế**`.

---

## 6. BẢNG HẠCH TOÁN COVERAGE CÁC VÙNG MỤC TIÊU (CHARACTER ACCOUNTING)

Để chứng minh tính toàn vẹn và không làm mất ký tự nguồn trên các vùng mục tiêu, artifact thiết lập bảng hạch toán coverage chi tiết:

### 6.1. Vùng vé ghép Ca Huế H3 2.3 & H4 A: Span `[10409, 12287)` (Tổng: 1.878 ký tự)
- **Phần giữ làm evidence (9 parts):**
  - Câu dẫn khảo sát 09/2026: `[10409, 10591)` -> 182 ký tự
  - Đoạn dẫn tour ghép: `[10643, 10758)` -> 115 ký tự
  - Header bảng + delimiter: `[10760, 10900)` -> 140 ký tự
  - Hàng Khách Việt Nam: `[10901, 11141)` -> 240 ký tự
  - Hàng Khách quốc tế: `[11142, 11317)` -> 175 ký tự
  - Hàng Trẻ em Lá Quê: `[11318, 11581)` -> 263 ký tự
  - Hàng Trẻ em Thuyền Rồng: `[11582, 11810)` -> 228 ký tự
  - Danh sách Bao gồm: `[11812, 12116)` -> 304 ký tự
  - Danh sách Không bao gồm: `[12117, 12287)` -> 170 ký tự  
  👉 **Tổng evidence giữ lại:** **1.817 ký tự**
- **Phần heading metadata:**
  - Tiêu đề H4 A `#### A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)`: `[10593, 10641)` -> **48 ký tự** (chuyển vào metadata `heading_path`, không nằm trong body evidence).
- **Khoảng trắng phân cách (Whitespace separators):**
  - 9 khoảng trống giữa các block: 2 + 2 + 2 + 1 + 1 + 1 + 1 + 2 + 1 = **13 ký tự** (gồm các ký tự `\n`).
- **Phần bị loại bỏ:** **0 ký tự**.
- **Kiểm tra đối chiếu hạch toán:**
  $$\text{Evidence } (1.817) + \text{Metadata } (48) + \text{Whitespace } (13) + \text{Discarded } (0) = 1.878 \text{ ký tự (Khớp chính xác 100%)}$$

### 6.2. Vùng danh sách lồng Gia Lạc: Span `[312, 997)` (Tổng: 685 ký tự)
- Evidence giữ lại: Mục *Thời gian tổ chức* (278 ký tự) + Mục *Nơi tổ chức* (406 ký tự) = 684 ký tự.
- Khoảng trắng: `[590, 591)` (`\n`) = 1 ký tự.
- Metadata / Discarded: 0 ký tự.
- **Tổng đối chiếu:** $684 + 1 = 685 \text{ ký tự}$ (Khớp chính xác 100%).

### 6.3. Vùng xử lý ảnh Mệ Kéo: Span `[318, 1073)` (Tổng: 755 ký tự)
- Evidence giữ lại: Thông tin quán trước ảnh (154 ký tự) + Giới thiệu sau ảnh (450 ký tự) = 604 ký tự.
- Phần loại bỏ: Dòng Markdown ảnh `![Tô bún bò Mệ Kéo](...)` tại `[474, 621)` = 147 ký tự.
- Khoảng trắng: 2 cặp `\n\n` tại `[472, 474)` và `[621, 623)` = 4 ký tự.
- **Tổng đối chiếu:** $604 + 147 + 4 = 755 \text{ ký tự}$ (Khớp chính xác 100%).

---

## 7. BẰNG CHỨNG THỰC THI TÍNH TÁI LẬP VÀ KIỂM ĐỊNH TOÀN BỘ PARTS (F2 / R2)

### 7.1. Kiểm tra tính tái lập độc lập (Reproducibility Test)
Script thực thi parse 2 lần độc lập trên toàn bộ 6 tệp khảo sát với cùng cấu hình `MarkdownIt().enable('table')`:

| Tệp khảo sát | Số token Lần 1 | Số token Lần 2 | Token Maps Lần 1 == Lần 2 | Kết luận |
| :--- | :---: | :---: | :---: | :---: |
| `festivals/festival/Hội xuân Gia Lạc.md` | 209 | 209 | **Trùng khớp 100%** | **PASS** |
| `heritages/heritage/Đại Nội Huế.md` | 743 | 743 | **Trùng khớp 100%** | **PASS** |
| `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` | 1.221 | 1.221 | **Trùng khớp 100%** | **PASS** |
| `travel/services/Chi phí du lịch Huế.md` | 504 | 504 | **Trùng khớp 100%** | **PASS** |
| `travel/tickets/Vé tham quan Hải Vân Quan.md` | 866 | 866 | **Trùng khớp 100%** | **PASS** |
| `foods/restaurants/quan bun bo me keo.md` | 67 | 67 | **Trùng khớp 100%** | **PASS** |

*Kết luận:* `markdown-it-py` bảo đảm tính tiền định tuyệt đối giữa các lần thực thi độc lập.

### 7.2. Kiểm định toàn bộ Evidence Parts xuất trong Artifact và Giới hạn Coverage
Hàm `collect_and_validate_parts` trong script tự động duyệt qua toàn bộ cấu trúc dữ liệu JSON để xác thực:
- **Cơ chế xác thực kép:** Validator hỗ trợ cả hai cấu trúc:
  1. Schema phẳng của composite chunk: `{"role": str, "start": int, "end": int, "text": str}` (8 parts).
  2. Schema lồng của các bản ghi chẩn đoán: `{"span": {"start": int, "end": int}, "text": str}` (32 parts).
- **Tổng số parts được kiểm tra:** **40/40 parts**.
- **Số parts có bounds hợp lệ (`0 <= start < end <= len(source)`):** **40/40 (100%)**.
- **Số parts có lát cắt khớp tuyệt đối (`source_text[start:end] == part["text"]`):** **40/40 (100%)**.
- **Trạng thái tổng hợp:** **PASS tuyệt đối (100%)**.
- **Ghi chú giới hạn phạm vi:**
  + Kết quả **40/40 PASS** là kết quả dành cho 40 parts văn bản nguồn cụ thể được validator duyệt (bao gồm 8 parts dạng flat của 2 composite chunks và 32 parts chẩn đoán trong các vùng mục tiêu); không bao gồm các probe records (vốn dùng cấu trúc `span: [start, end]`) hay bảng hạch toán coverage tĩnh, và không đại diện cho toàn bộ các đối tượng khác hay tính đầy đủ toàn corpus.
  + Bảng hạch toán coverage (Section 6) là minh họa tĩnh trên các vùng mục tiêu được chọn lọc, không phải phép quét động mọi vị trí trong file hay bảo đảm tính đầy đủ cho toàn bộ corpus.
  + Phiên bản parser được đọc trực tiếp từ thuộc tính package runtime: `markdown_it.__version__` (`4.2.0`).

### 7.3. Thử nghiệm chuẩn hóa CRLF trong bộ nhớ
- Tạo bản giả lập CRLF bằng cách thay toàn bộ `\n` bằng `\r\n` trên dữ liệu `Hội xuân Gia Lạc.md` (5.464 ký tự).
- Sau khi đi qua hàm `normalize_lf()`, chuỗi thu được có độ dài 5.256 ký tự, trùng khớp 100% từng byte so với bản LF gốc.
- *Ghi chú:* Đây là deterministic probe trong bộ nhớ để kiểm chứng quy ước tính toán locator, không phải tệp corpus trên đĩa.

---

## 8. KẾT QUẢ THỰC THI PROBE CONDITION MAPPING VÀ QUY TẮC LIÊN KẾT (R1 ĐÃ ĐÓNG)

### 8.1. Kết quả thực thi Probe thực tế trên Token Stream (R1)
Hàm `run_condition_mapping_probe` đã thực thi kiểm chứng 3 rules trực tiếp trên luồng tokens của `markdown-it-py`, tuân thủ đúng các yêu cầu của Reviewer:

| Rule ID | Khối Condition & Phép so | Trạng thái Condition Match | Khối Target & Ancestor Path | Số Target Sections & Hàng khớp thực tế | Ranh giới dừng & Trạng thái Probe |
| :--- | :--- | :---: | :--- | :---: | :---: |
| `ca_hue_survey_lead_to_pricing_tables` | Paragraph dẫn giá 09/2026 tại line 104; `path == ['2. Ca Huế...', '2.3. Chi tiết...']`; so khớp 100% `EXPECTED_CA_HUE_LEAD_SIG` | **RESOLVED_UNIQUE** (1 match, span `[10409, 10591)`) | Full ancestor path H2/H3/H4 cho cả Mục A và Mục B | **2 sections, 2 bảng, 6 hàng**<br>- Mục A: 4 hàng (`[10901..11810)`)<br>- Mục B: 2 hàng (`[12617, 12968)` và `[12969, 13386)`) | **PASS** |
| `ca_hue_exclusions_to_tour_ghep_only` | List item "Không bao gồm" tại line 118; `path == ['2. Ca Huế...', '2.3. ...', 'A. Vé khách lẻ...']`; **so khớp toàn bộ 100% signature** `EXPECTED_CA_HUE_EXCL_SIG` | **RESOLVED_UNIQUE** (1 match, span `[12117, 12287)`) | Full ancestor path H2/H3/H4 Mục A; Stop boundary: Mục B | **Mục A: 4 hàng; Mục B: 0 hàng**<br>Hàng cuối Mục A kết thúc tại offset 11810 < heading Mục B (offset 12289); giao thoa spans A và B bằng 0 | **PASS** |
| `chi_phi_intro_to_all_three_daily_budget_tables` | Paragraph intro hạn mức kế hoạch tại line 2; **lọc `path == []`** (trước mọi H2); **so khớp signature độc lập** `EXPECTED_CHI_PHI_INTRO_SIG` (có literal LF) | **RESOLVED_UNIQUE** (1 match, span `[23, 261)`) | Full path 3 section H2: `['Dự toán một ngày...']`, `['Dự toán hai ngày...']`, `['Dự toán ba ngày...']` | **3 sections độc lập, 3 bảng, 3 hàng Tổng tại Huế**<br>- Line 83: `[3066, 3158)`<br>- Line 98: `[3871, 3967)`<br>- Line 113: `[4666, 4765)` | **PASS** |

### 8.2. Cấu trúc khai báo Declarative Mapping
Các quy tắc khai báo tối thiểu dạng JSON dùng cho quá trình ingest (thống nhất quy ước bỏ H1):

```json
[
  {
    "rule_id": "ca_hue_survey_lead_to_pricing_tables",
    "source_file": "travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md",
    "condition_locator": {
      "heading_path": ["2. Ca Huế trên sông Hương và dịch vụ thuyền rồng", "2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế"],
      "block_type": "paragraph",
      "exact_text_signature": "Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu (Thuyền Rồng Huế, Ca Huế Trên Sông Hương - Lá Quê Travel, Đại Việt Tourist) tại thời điểm tháng 09/2026:"
    },
    "target_scope": {
      "heading_prefix": ["2. Ca Huế trên sông Hương và dịch vụ thuyền rồng", "2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế"],
      "apply_to_sections": [
        "A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)",
        "B. Thuê trọn gói nguyên thuyền rồng biểu diễn Ca Huế riêng (Bao chuyến)"
      ],
      "expected_target_sections_count": 2,
      "apply_to_roles": ["table_row"],
      "boundary_rule": "Áp dụng cho các hàng trong cả 2 bảng giá vé thuộc tiểu mục 2.3 (Mục A và Mục B)"
    },
    "mismatch_policy": "FAIL_INGEST_ON_SIGNATURE_OR_TARGET_MISMATCH"
  },
  {
    "rule_id": "ca_hue_exclusions_to_tour_ghep_only",
    "source_file": "travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md",
    "condition_locator": {
      "heading_path": [
        "2. Ca Huế trên sông Hương và dịch vụ thuyền rồng",
        "2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế",
        "A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)"
      ],
      "block_type": "bullet_list_item",
      "exact_text_signature": "- **Không bao gồm:** Phương tiện đưa đón tận nơi (khách tự di chuyển đến Bến Tòa Khâm), ăn uống cá nhân trên thuyền, tiền tip bồi dưỡng nghệ sĩ (không bắt buộc, tùy tâm)."
    },
    "target_scope": {
      "heading_path": [
        "2. Ca Huế trên sông Hương và dịch vụ thuyền rồng",
        "2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế",
        "A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)"
      ],
      "expected_target_sections_count": 1,
      "apply_to_roles": ["table_row"],
      "explicit_stop_boundary": "DỪNG TRƯỚC '#### B. Thuê trọn gói nguyên thuyền rồng biểu diễn Ca Huế riêng (Bao chuyến)'. Tuyệt đối KHÔNG lan điều kiện sang mục B."
    },
    "mismatch_policy": "FAIL_INGEST_ON_SIGNATURE_OR_TARGET_MISMATCH"
  },
  {
    "rule_id": "chi_phi_intro_to_all_three_daily_budget_tables",
    "source_file": "travel/services/Chi phí du lịch Huế.md",
    "condition_locator": {
      "heading_path": [],
      "block_type": "paragraph",
      "exact_text_signature": "Ngân sách du lịch Huế phụ thuộc nơi khởi hành, thời điểm đặt dịch vụ, số người\nvà loại trải nghiệm. Các bảng dưới đây là hạn mức lập kế hoạch được đối chiếu\ntừ nguồn công khai ngày 08/09/2026, không phải giá niêm yết của một nhà cung cấp.",
      "signature_contains_literal_lf": true,
      "internal_lf_count": 2
    },
    "target_scope": {
      "apply_to_sections": [
        "Dự toán một ngày tại Huế",
        "Dự toán hai ngày một đêm tại Huế",
        "Dự toán ba ngày hai đêm tại Huế"
      ],
      "expected_target_tables_count": 3,
      "apply_to_roles": ["table_row", "table_total_row"],
      "target_verification": "Xác nhận sự tồn tại của hàng '| **Tổng tại Huế** |' trong cả 3 bảng mục tiêu"
    },
    "mismatch_policy": "FAIL_INGEST_ON_SIGNATURE_OR_TARGET_MISMATCH"
  }
]
```

### 8.3. Cơ chế phân giải duy nhất và chính sách Fail-Fast
1. **Phân giải duy nhất khối điều kiện:**  
   Bộ nạp tìm khối điều kiện dựa trên `heading_path` phân cấp đầy đủ và `block_type`. Sau đó kiểm tra:
   $$\text{block.text} == \text{exact\_text\_signature}$$
   Kể cả các ký tự `\n` nội dòng cũng phải khớp tuyệt đối. Nếu số khối tìm được bằng 0 hoặc lớn hơn 1 (mơ hồ), hoặc signature không khớp từng ký tự, tiến trình ingest lập tức **dừng và báo lỗi (FAIL FAST)**.
2. **Phân giải và kiểm định khối đích (Target Verification):**  
   Bộ nạp xác định danh sách các bảng/hàng đích qua `heading_path` hoặc `apply_to_sections`. Để chống trỏ nhầm khi cấu trúc thay đổi, bộ nạp đối chiếu số lượng khối đích tìm được với `expected_target_tables_count` (ví dụ: đúng 3 bảng dự toán cho Chi phí) và kiểm tra sự tồn tại của các hàng định danh (ví dụ: hàng `| **Tổng tại Huế** |`).
3. **Giới hạn phạm vi bảo vệ của Signature:**  
   *Đính chính claim cũ:* Signature của một khối **chỉ bảo vệ tính toàn vẹn của chính khối đó**, không thể phát hiện các thay đổi bất kỳ ở những phần khác trong file. Việc bảo vệ khối đích đòi hỏi phải kết hợp kiểm tra số lượng mục tiêu và cấu trúc bảng đích như đã mô tả ở trên.

---

## 9. ĐÍNH CHÍNH CÁC TUYÊN BỐ VÀ GIỚI HẠN KHẢO SÁT

1. **Về tính đầy đủ và chất lượng RAG:**  
   Việc các evidence parts đạt exact match 100% với nguồn chỉ chứng minh parser trích xuất nguyên văn chính xác, **không đồng nghĩa** với việc chunk đã hoàn chỉnh về mặt ngữ nghĩa hoặc mô hình LLM sẽ loại trừ hoàn toàn ảo giác. Chất lượng RAG cần được đánh giá qua benchmark trên Golden Dataset ở các giai đoạn sau.
2. **Về so sánh với parser dự phòng:**  
   Do `markdown-it-py` (v4.2.0) với `MarkdownIt().enable('table')` đã đáp ứng đầy đủ và vượt qua toàn bộ các bài kiểm định kỹ thuật, không cần thiết phải triển khai so sánh sâu với `mistune` 3.3.4 hay các parser khác.
3. **Về tình trạng worktree và mã nguồn:**  
   Khảo sát này chỉ thao tác trên 3 artifacts được cấp phép; không thay đổi mã nguồn trong `backend/`, không thay đổi dữ liệu trong `knowledge-base-hue/`, không chạy model inference hay benchmark tokenizer.

---

## 10. DANH MỤC ARTIFACTS BÀN GIAO VÀ BƯỚC TIẾP THEO

### 10.1. Ba artifacts đã hoàn thiện và kiểm định thành công:
1. [reports/full_corpus_parser_locator_survey_2026_09_09.md](file:///home/minhhieu/hue_rag/reports/full_corpus_parser_locator_survey_2026_09_09.md) (Báo cáo chi tiết này)
2. [reports/artifacts/full_corpus_parser_locator_survey_2026_09_09.py](file:///home/minhhieu/hue_rag/reports/artifacts/full_corpus_parser_locator_survey_2026_09_09.py) (Script khảo sát, chạy lại bằng `uv run --no-sync python ...`)
3. [reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json](file:///home/minhhieu/hue_rag/reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json) (Dữ liệu mẫu, spans, probe execution results và kết quả kiểm định 40/40 parts PASS)

### 10.2. Bước tiếp theo:
User chuyển giao báo cáo khảo sát đã được hoàn thiện cho Reviewer để tiến hành review closure Lượt 3. Sau khi Reviewer xác nhận đạt yêu cầu, Reviewer sẽ tiếp tục hoàn thiện written spec về schema/locator và condition mapping cho full-corpus RAG để trình User phê duyệt.
