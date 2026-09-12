# Báo cáo khảo sát phân chia mẫu văn bản và đo token bằng tokenizer local (Lượt cập nhật 3)

- **Ngày thực hiện:** 2026-09-09
- **Vai trò:** Implementer (thực hiện khảo sát có giới hạn theo yêu cầu trực tiếp của người dùng và yêu cầu bổ sung của Reviewer)
- **Đối tượng thụ hưởng:** Reviewer (phục vụ phân tích evidence, cân nhắc trade-offs và quyết định thiết kế chunking/token policy)
- **Tình trạng:** Khảo sát text và tokenizer local (Lượt 3: Bổ sung câu dẫn khảo sát mục 2.3 `tháng 09/2026`, đo phương án gộp vs tách khách VN/QT, đính chính overhead MiniLM pair); **KHÔNG** phải triển khai runtime full-corpus, không sửa backend hay benchmark chất lượng.

---

## 1. Trạng thái thực thi và môi trường kỹ thuật

### 1.1. Git commit và Worktree
- **Commit HEAD:** `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340` (nhánh `main`).
- **Trạng thái worktree:** Bảo toàn nguyên vẹn snapshot bàn giao:
  - 02 tệp hướng dẫn modified có sẵn: `guides/README.md`, `guides/phase_2_foods_markdown_chunking.md`.
  - 04 tệp ngữ cảnh/thiết kế untracked: `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`, `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`, `session_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`, `session_prompt/FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md`.
  - 03 tệp artifacts của khảo sát được cập nhật đồng bộ tại chỗ:
    + `reports/full_corpus_chunk_samples_tokenizer_survey_2026_09_09.md`
    + `reports/artifacts/full_corpus_chunk_samples_2026_09_09.json`
    + `reports/artifacts/full_corpus_chunk_samples_2026_09_09.py`

### 1.2. Môi trường thực thi và cấu hình Tokenizer local
- **Runtime:** Project virtual environment thông qua `uv` (`requires-python >= 3.13`), `transformers==5.14.1`, `pyvi==0.1.1` (ghim cứng trong project dependencies).
- **Tokenizer cache local:** Đọc trực tiếp từ `/home/minhhieu/.cache/huggingface/hub` với cờ `local_files_only=True`:
  1. `intfloat/multilingual-e5-small` (snapshot `614241f622f53c4eeff9890bdc4f31cfecc418b3`): giới hạn `max_length = 512`. Preprocessing: prefix `passage: ` cho tài liệu.
  2. `intfloat/multilingual-e5-base` (snapshot `d128750597153bb5987e10b1c3493a34e5a4502a`): giới hạn `max_length = 512`. Preprocessing: prefix `passage: ` cho tài liệu.
  3. `CODE4LIFEOFFICIAL/huydang-dek21-embedding` (snapshot `517f1af7dd04a57194f1de2990f0c6ede0a3109b`): giới hạn `max_length = 256`. Preprocessing: tách từ bằng `pyvi.ViTokenizer.tokenize()`, không thêm prefix E5.
  4. `cross-encoder/ms-marco-MiniLM-L-6-v2` (snapshot `233902d25c440f23af6f7d6e94d2946bac0bee0a`): giới hạn cặp `(query, document)` là `512`. Không thêm prefix E5, đếm cả câu hỏi, văn bản và special tokens `[CLS] ... [SEP] ... [SEP]`.
- **An toàn ranh giới:** Tuyệt đối không nạp hoặc đọc `.env`, không gọi Qdrant, không inference embedding/reranking, không gọi paid API.

---

## 2. Giải trình các điểm lệch tính nhất quán và Chuẩn hóa câu hỏi

Trong lượt rà soát này, Implementer đã đối chiếu kỹ lưỡng giữa báo cáo, mã nguồn đo lường và tệp JSON để giải quyết dứt điểm 3 điểm chưa nhất quán:

### 2.1. Giải thích chênh lệch số đo MiniLM giữa Ngọ Môn P1 Chunk 1 và P2 Chunk 1
- **Hiện tượng:** Ở báo cáo trước, cùng một khối nội dung văn bản (đoạn dẫn + đài nền 5 cửa vòm, 849 ký tự), `ngo_mon_p1_chunk_1` ghi nhận MiniLM orig là 393 tokens, trong khi `ngo_mon_p2_chunk_1` lại ghi nhận 386 tokens.
- **Nguyên nhân gốc:** Khi cấu hình kịch bản đo ở lượt trước, `ngo_mon_p2_chunk_1` đã vô tình bị truyền một câu hỏi rút gọn khác (`"Ngọ Môn có cấu trúc như thế nào?"` — ngắn hơn 7 tokens so với câu hỏi chuẩn của mục 19).
- **Khắc phục:** Áp dụng nguyên tắc chuẩn hóa: **Với mỗi tài liệu nguồn, dùng đúng 01 câu hỏi gốc cố định (từ mục 19) và đúng 01 câu hỏi dài cố định cho tất cả các phương án đem so sánh**. Cả P1 Chunk 1 và P2 Chunk 1 sau khi đo lại bằng cùng một cặp truy vấn đã cho kết quả **đồng nhất tuyệt đối**: MiniLM orig = **393**, MiniLM long = **429**.

### 2.2. Đính chính mô tả token của Hội xuân Gia Lạc Phương án 2
- **Hiện tượng:** Văn bản mô tả ở lượt 1 ghi "tạo thêm nhiều chunk vụn (~51–85 token HuyDang)", trong khi bảng số liệu có chunk đạt 155 tokens.
- **Đính chính:** Mô tả trên đã khái quát hóa thiếu chính xác khi chỉ nhìn vào Chunk 2 (51 tokens) và Chunk 3 (85 tokens) mà bỏ quên Chunk 1 (`gia_lac_p2_chunk_1`: Định danh & Tính chất phi thương mại) đạt **155 tokens HuyDang**. Văn bản đã được chỉnh sửa để phản ánh đúng phân bố thực tế: Chunk 1 là 155 tokens, Chunk 2 và 3 là các chunk ngắn 51 và 85 tokens.

### 2.3. Quy chuẩn hóa định nghĩa Độ bao phủ (Coverage Audit)
- **Đính chính:** Không gọi các trường hợp có khoảng hở ký tự xuống dòng (`\n`, `\n\n`) phân cách là "exact character coverage 100%".
- **Quy định rành mạch:**
  1. **Bao phủ nội dung (Content Coverage):** Đạt **100%** nội dung ngữ nghĩa thông tin, không bỏ sót bất kỳ từ, câu hay ý nghĩa nào trong khối văn bản mục tiêu.
  2. **Ký tự khoảng cách/ngắt dòng (Whitespace Gaps):** Mọi ký tự khoảng trắng hoặc phân dòng giữa các đoạn (`\n`, `\n\n`) không nằm trong evidence parts đều được kiểm kê và giải trình số lượng chính xác tại Mục 5 của báo cáo.

### 2.4. Danh mục câu hỏi chuẩn hóa cố định theo từng tài liệu nguồn

| Tài liệu nguồn | Câu hỏi gốc cố định (`query_orig` từ mục 19) | Câu hỏi dài tự nhiên cố định (`query_long`) |
|:---|:---|:---|
| **Hội xuân Gia Lạc** | `Hội xuân Gia Lạc tổ chức ở đâu và vào thời gian nào?` | `Lễ hội xuân Gia Lạc trong lịch sử và các kỳ phục dựng chuyên đề hiện nay được tổ chức vào thời gian nào, tại địa điểm nào?` |
| **Đại Nội Huế (Ngọ Môn)** | `Ngọ Môn có cấu trúc và ý nghĩa lịch sử như thế nào?` | `Cửa Ngọ Môn Hoàng thành Huế được xây dựng vào năm nào, cấu trúc đài nền cùng lầu Ngũ Phụng có đặc điểm kiến trúc và ý nghĩa lịch sử ra sao?` |
| **Vé Ca Huế trên sông Hương** | `Vé Ca Huế cho trẻ em được tính như thế nào?` | `Giá vé xem Ca Huế ghép thuyền trên sông Hương cho người lớn và trẻ em bao nhiêu tiền một người, áp dụng điều kiện bao gồm và không bao gồm những dịch vụ gì?` |
| **Quán bún bò Mệ Kéo** | `Quán bún bò Mệ Kéo mở cửa đến mấy giờ?` | `Quán bún bò Mệ Kéo nằm ở địa chỉ nào tại Huế, mở bán trong khung giờ nào và mức giá mỗi tô dao động khoảng bao nhiêu?` |
| **Lịch trình Biển & Đầm phá** | `Có thể thay ngày cuối bằng đi biển và đầm phá không?` | `Nếu muốn đổi lịch trình ngày thứ ba sang tham quan biển Thuận An hoặc phá Tam Giang thì cần lưu ý những điều kiện thời tiết nào?` |

---

## 3. Phân tích nguyên văn điều kiện trong và xung quanh Bảng Ca Huế

Thực hiện đọc trực tiếp nguyên văn tệp nguồn `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` tại các mục 2.1, 2.2, 2.3A, Implementer làm rõ bản chất và phạm vi của các điều kiện:

### 3.1. Điều kiện nào bắt buộc đi cùng mức giá/chính sách để tránh hiểu sai?
1. **Giới hạn loại trừ tiêu cực (`- **Không bao gồm:**`):**
   - *Nguyên văn:* `- **Không bao gồm:** Phương tiện đưa đón tận nơi (khách tự di chuyển đến Bến Tòa Khâm), ăn uống cá nhân trên thuyền, tiền tip bồi dưỡng nghệ sĩ (không bắt buộc, tùy tâm).` (170 ký tự).
   - *Lý do:* Đây là điều kiện tối cần thiết để tránh hiểu sai về mức giá. Nếu người dùng hỏi "Vé 100k đã có đón tận khách sạn hay ăn tối chưa?", nếu chunk giá vé không có thông tin loại trừ này, mô hình rất dễ suy đoán sai hoặc không khẳng định được.
2. **Tên nhà cung cấp gắn với tiêu chuẩn vé trẻ em:**
   - *Nguyên văn:* Hàng chiều cao ghi rõ *"Tiêu chuẩn chiều cao quy định bởi đơn vị Lá Quê Travel (cahuetrensonghuong.com)"*; hàng độ tuổi ghi rõ *"Tiêu chuẩn độ tuổi áp dụng tại Thuyền Rồng Huế (thuyenronghue.com)"*.
   - *Lý do:* Phải giữ tên nhà cung cấp đi liền với từng hàng trẻ em để tránh người đọc hiểu lầm rằng cả hai chính sách (chiều cao và độ tuổi) áp dụng đồng thời cho mọi nhà thuyền.
3. **Đơn vị tính và quyền lợi cốt lõi trong bảng:**
   - Đơn vị tính (`đồng/người/suất`, `đồng/trẻ/suất`) và dịch vụ cốt lõi (chỗ ngồi thuyền rồng, xem 50 phút, hoa đăng thả sông) đã nằm sẵn trong các cột của bảng và bắt buộc phải đi cùng giá.

### 3.2. Điều kiện nào là thông tin dịch vụ bổ sung, có thể trả lời riêng?
1. **Quy chuẩn dịch vụ và mô tả chi tiết của `- **Bao gồm:**`:**
   - *Nguyên văn:* `- **Bao gồm:** Suất nghe trọn vẹn chương trình Ca Huế đúng quy chuẩn nhà nước (tối thiểu 50 phút, dàn nghệ sĩ ca sĩ nhạc công trang phục áo dài truyền thống), thuyền rồng di chuyển ngắm cảnh cầu Trường Tiền, cầu Phú Xuân, mỗi khách được phát 01 hoa đăng giấy thắp nến để thả xuống sông Hương cầu bình an.` (304 ký tự).
   - *Lý do:* Bản thân từng hàng trong bảng đã có cột "Thành phần bao gồm" tóm tắt (chỗ ngồi, xem 50 phút, hoa đăng, thuyết minh song ngữ). Khối văn bản này bổ sung chi tiết về lộ trình di chuyển (cầu Trường Tiền - Phú Xuân) và quy chuẩn nghệ sĩ (áo dài). Đây là thông tin dịch vụ bổ sung, có thể đứng thành chunk dịch vụ độc lập.
2. **Hình thức tour ghép đoàn (Đoạn dẫn trước bảng):**
   - *Nguyên văn:* `Hình thức ghép chung du khách lẻ lên một thuyền rồng đôi lớn (sức chứa từ 25 đến 35 khách) để thưởng thức đêm nhạc:` (115 ký tự). Mô tả loại phương tiện và quy mô đoàn, có thể đứng cùng khối dịch vụ.
3. **Khung giờ suất diễn ban đêm (Mục 2.2):**
   - Suất 1 (19h–20h), Suất 2 (20h–21h), Suất 3 (21h–22h). Trả lời riêng cho câu hỏi "Ca Huế có những khung giờ nào?".
4. **Căn cứ pháp lý và an toàn (Mục 2.1):**
   - Quyết định 104/2025/QĐ-UBND, bến Tòa Khâm, quy chuẩn dàn nhạc 7–8 người, cấm cò mồi. Trả lời riêng cho các câu hỏi về pháp lý/an toàn đường thủy.

### 3.3. Điều kiện áp dụng chung hay chỉ cho đối tượng/nhà cung cấp cụ thể?
- **Áp dụng chung:**
  - Khối điều kiện `Bao gồm` và `Không bao gồm` áp dụng chung cho toàn bộ hình thức vé khách lẻ ghép thuyền (tiểu mục A).
  - Điểm đón khách tập trung tại Bến Tòa Khâm.
- **Áp dụng cho đối tượng cụ thể:**
  - Mức giá 150.000đ chỉ áp dụng cho khách quốc tế (kèm thuyết minh song ngữ).
  - Mức giá 100.000 – 130.000đ chỉ áp dụng cho khách Việt Nam.
- **Áp dụng cho nhà cung cấp cụ thể:**
  - Tiêu chuẩn vé trẻ em theo chiều cao: Nguồn nêu rõ chỉ áp dụng tại Lá Quê Travel.
  - Tiêu chuẩn vé trẻ em theo độ tuổi: Nguồn nêu rõ chỉ áp dụng tại Thuyền Rồng Huế.
  - *Lưu ý nguồn:* Tệp nguồn KHÔNG nêu rõ tiêu chuẩn trẻ em của các đơn vị khác (như Đại Việt Tourist). Vì vậy không được tự suy diễn đây là quy chuẩn chung của toàn bộ bến thuyền.

---

## 4. Khảo sát Phương án 3 (P3): Chia nhỏ kèm lặp điều kiện khi Ingest

Để kiểm tra xem việc **chia nhỏ theo hàng/nhà cung cấp kết hợp lặp điều kiện nguyên văn ngay khi ingest** có vừa vặn input limits của chung bộ model hay không, Implementer đã thử nghiệm 2 biến thể kỹ thuật độc lập:

### 4.1. Biến thể 3A (P3a): Chia lẻ từng hàng + Lặp ĐẦY ĐỦ cả Bao gồm & Không bao gồm (475 ký tự)
- Cấu hình thử nghiệm: Mỗi chunk gồm Table Header + 01 hàng dữ liệu đơn lẻ + Toàn bộ 475 ký tự điều kiện (`Bao gồm` và `Không bao gồm`).
- Kết quả đo đạc thực tế:
  1. `ca_hue_p3a_chunk_1` (Khách VN + Header + Cả 2 điều kiện, 1.069 chars): HuyDang = 249 (sát trần), MiniLM long = **517 tokens (VƯỢT trần 512)**.
  2. `ca_hue_p3a_chunk_2` (Khách QT + Header + Cả 2 điều kiện, 970 chars): HuyDang = 222, MiniLM long = 473 (**PASS** do hàng QT ngắn).
  3. `ca_hue_p3a_chunk_3` (Trẻ em Lá Quê [chiều cao] + Header + Cả 2 điều kiện, 1.075 chars): HuyDang = **267 tokens (VƯỢT trần 256)**, MiniLM long = **534 tokens (VƯỢT trần 512)**.
  4. `ca_hue_p3a_chunk_4` (Trẻ em Thuyền Rồng [độ tuổi] + Header + Cả 2 điều kiện, 1.040 chars): HuyDang = **264 tokens (VƯỢT trần 256)**, MiniLM long = **514 tokens (VƯỢT trần 512)**.
  5. `ca_hue_p3a_chunk_5` (Đoạn dẫn hình thức tour ghép, 309 chars): HuyDang = 66, MiniLM = 192 (**PASS**).
- **Kết luận kỹ thuật Biến thể 3A:** Ngay cả khi đã chia nhỏ xuống mức tối đa (01 hàng duy nhất cho mỗi chunk), việc cố gắng lặp ĐẦY ĐỦ cả 2 đoạn văn điều kiện (475 ký tự) **vẫn gây tràn token trên 3/4 chunk dữ liệu** đối với HuyDang và MiniLM.

### 4.2. Biến thể 3B Lượt 2 (P3b v1): Nhóm hàng có nghĩa + Lặp điều kiện loại trừ 'Không bao gồm' (170 ký tự) — Chưa có câu dẫn mục 2.3
- Cấu hình thử nghiệm (Lượt 2):
  - Nhóm các hàng giá theo phân khúc rõ ràng (Vé người lớn VN+QT; Vé trẻ em Lá Quê; Vé trẻ em Thuyền Rồng).
  - Lặp lại điều kiện loại trừ tối cần thiết `- **Không bao gồm:**` (170 ký tự) trong từng chunk giá vé.
  - Tách phần mô tả dịch vụ chi tiết (Đoạn dẫn tour ghép 115 chars + Điều kiện `- **Bao gồm:**` chi tiết 304 chars) thành 01 chunk dịch vụ bổ sung độc lập.
- Kết quả đo đạc thực tế (Lượt 2):
  1. `ca_hue_p3b_chunk_1` (Vé người lớn VN+QT + Header + `Không bao gồm`, 923 chars):
     - E5-small: 296 | E5-base: 296 | HuyDang: **224 / 256** | MiniLM long: **458 / 512** -> **PASS ALL**.
  2. `ca_hue_p3b_chunk_2` (Trẻ em Lá Quê [chiều cao] + Header + `Không bao gồm`, 770 chars):
     - E5-small: 258 | E5-base: 258 | HuyDang: **208 / 256** | MiniLM long: **410 / 512** -> **PASS ALL**.
  3. `ca_hue_p3b_chunk_3` (Trẻ em Thuyền Rồng [độ tuổi] + Header + `Không bao gồm`, 735 chars):
     - E5-small: 249 | E5-base: 249 | HuyDang: **205 / 256** | MiniLM long: **390 / 512** -> **PASS ALL**.
  4. `ca_hue_p3b_chunk_4` (Tour ghép rồng đôi + `Bao gồm` chi tiết, 615 chars):
     - E5-small: 168 | E5-base: 168 | HuyDang: **125 / 256** | MiniLM long: **316 / 512** -> **PASS ALL**.

### 4.3. Biến thể 3B Lượt 3 (P3b v2): Bổ sung nguyên văn Câu dẫn khảo sát mục 2.3 theo Reviewer
Reviewer đã đối chiếu nguồn và phát hiện P3B thiếu câu dẫn ngay dưới heading `### 2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế`. Câu này đóng vai trò quyết định vì xác định danh sách 3 đơn vị khảo sát thực tế và thời điểm khảo sát `tháng 09/2026`. Nếu thiếu, bảng giá mất neo thời gian và người dùng có thể nhầm tưởng là giá niêm yết nhà nước vĩnh viễn hoặc giá hiện hành mọi thời điểm.

- **Văn bản câu dẫn nguyên văn:**
  ```text
  Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu (Thuyền Rồng Huế, Ca Huế Trên Sông Hương - Lá Quê Travel, Đại Việt Tourist) tại thời điểm tháng 09/2026:
  ```
  - Span: `[10409, 10591)` (182 ký tự). Kiểm tra exact match 100%. Không tự thêm nhãn "giá hiện hành", không diễn đạt lại.

- **Thử nghiệm 1: Gộp người lớn VN + QT + Header + Câu dẫn 2.3 + Không bao gồm (`ca_hue_p3b_lead_chunk_1_merged`, 1.107 ký tự):**
  - E5-small: 349 | E5-base: 349 | HuyDang: **264 / 256 (VƯỢT TRẦN +8 tokens)** | MiniLM orig: 485 | MiniLM long: **527 / 512 (VƯỢT TRẦN +15 tokens)**.
  - **Kết luận:** Khi thêm 182 ký tự câu dẫn vào khối gộp cả người lớn VN và QT, chunk bị **tràn ngưỡng kỹ thuật của cả HuyDang (264 > 256) và MiniLM-long (527 > 512)**. Phương án gộp không còn khả thi nếu muốn duy trì câu dẫn 2.3.

- **Thử nghiệm tách 2 hàng đơn lẻ theo yêu cầu Reviewer:**
  1. `ca_hue_p3b_lead_chunk_1a` (Khách VN riêng + Header + Câu dẫn 2.3 + Không bao gồm, 948 ký tự):
     - E5-small: 298 | E5-base: 298 | HuyDang: **230 / 256** (PASS, 89.8% trần) | MiniLM orig: 420 | MiniLM long: **462 / 512** (PASS, 90.2% trần) -> **PASS ALL**.
  2. `ca_hue_p3b_lead_chunk_1b` (Khách QT riêng + Header + Câu dẫn 2.3 + Không bao gồm, 849 ký tự):
     - E5-small: 260 | E5-base: 260 | HuyDang: **203 / 256** (PASS, 79.3% trần) | MiniLM orig: 376 | MiniLM long: **418 / 512** (PASS, 81.6% trần) -> **PASS ALL**.
  - **So sánh với chunk gộp:** Việc tách riêng giúp giảm 34 tokens HuyDang (cho VN) và 61 tokens HuyDang (cho QT), đưa cả 2 chunk từ trạng thái vi phạm (264 tokens) về vùng an toàn tuyệt đối (< 230 tokens), loại bỏ hoàn toàn nguy cơ truncation.

- **Đo đạc các chunk vé trẻ em khi bổ sung câu dẫn 2.3:**
  1. `ca_hue_p3b_lead_chunk_2` (Trẻ em Lá Quê [chiều cao] + Header + Câu dẫn 2.3 + Không bao gồm, 954 ký tự):
     - E5-small: 311 | E5-base: 311 | HuyDang: **248 / 256** (PASS, sát trần 96.9%, cách trần 8 tokens) | MiniLM orig: 437 | MiniLM long: **479 / 512** (PASS, 93.6% trần) -> **PASS ALL**.
  2. `ca_hue_p3b_lead_chunk_3` (Trẻ em Thuyền Rồng [độ tuổi] + Header + Câu dẫn 2.3 + Không bao gồm, 919 ký tự):
     - E5-small: 302 | E5-base: 302 | HuyDang: **245 / 256** (PASS, sát trần 95.7%, cách trần 11 tokens) | MiniLM orig: 417 | MiniLM long: **459 / 512** (PASS, 89.6% trần) -> **PASS ALL**.

- **Phân tích kỹ thuật đối với chunk dịch vụ riêng:**
  1. `ca_hue_p3b_lead_chunk_4_service` (Tour ghép + `Bao gồm` chi tiết, 615 ký tự, không mang theo câu dẫn 2.3):
     - E5-small: 168 | E5-base: 168 | HuyDang: **125 / 256** | MiniLM orig: 274 | MiniLM long: **316 / 512** -> **PASS ALL**.
  2. `ca_hue_p3b_lead_chunk_4_service_with_lead` (Biến thể đối chiếu: mang theo câu dẫn 2.3, 799 ký tự):
     - E5-small: 221 | E5-base: 221 | HuyDang: **165 / 256** | MiniLM orig: 343 | MiniLM long: **385 / 512** -> **PASS ALL**.
  - **Lý do vì sao chunk dịch vụ riêng KHÔNG nhất thiết mang theo câu dẫn 2.3:**
    - *Khác biệt về bản chất nội dung:* Chunk 4 chỉ chứa quy cách dịch vụ chung (thuyền rồng đôi 25–35 khách, thời lượng biểu diễn tối thiểu 50 phút đúng quy chuẩn nhà nước, dàn nghệ sĩ áo dài truyền thống, hoa đăng giấy thả sông). Đây là quy chuẩn dịch vụ và trải nghiệm văn hóa chung, **hoàn toàn không chứa bất kỳ con số giá vé khảo sát nào**.
    - *Tránh nhiễu ngữ nghĩa (Semantic noise):* Câu dẫn 2.3 mở đầu bằng cụm từ *"Dưới đây là mức giá khảo sát thực tế..."*. Nếu đưa câu này vào một chunk không hề chứa mức giá nào, sẽ tạo ra sự bất nhất về ngữ nghĩa, có nguy cơ gây nhiễu cho retriever khi nhận các câu hỏi thuần túy về dịch vụ ("thời lượng biểu diễn Ca Huế bao lâu?", "nghệ sĩ biểu diễn mặc trang phục gì?").
    - *Dư địa kỹ thuật:* Nếu Reviewer muốn áp dụng quy tắc hình thức đồng bộ (mọi chunk trong mục 2.3 đều mang theo câu dẫn), biến thể có câu dẫn (799 ký tự, 165 tokens HuyDang) vẫn hoàn toàn an toàn và nằm sâu dưới trần kỹ thuật.

### 4.4. Đo lường và Đính chính Overhead của Cặp Query - Nhãn ngữ cảnh trong MiniLM và Embedding
- Nhãn ngữ cảnh của bảng Ca Huế:
  ```text
  Vé biểu diễn nghệ thuật và trải nghiệm sông Hương
  2. Ca Huế trên sông Hương và dịch vụ thuyền rồng > 2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế > A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)
  ```
- Độ dài chuỗi nhãn: **194 ký tự**.
- Phân rã token chi tiết theo từng mô hình:
  - **E5-small / E5-base:** Nhãn chiếm **54 tokens** (10.5% ngân sách 512).
  - **HuyDang:** Nhãn chiếm **42 tokens** (**16.4%** ngân sách 256).
  - **MiniLM (chỉ riêng chuỗi nhãn, text-only):** **79 tokens** (15.4% ngân sách 512).
- **Đính chính cách diễn giải con số 141 tokens trong MiniLM:**
  Ở báo cáo trước, số đo 141 tokens bị ghi nhận chưa rõ ràng là overhead của nhãn. Nay Implementer đính chính chính xác: **141 tokens KHÔNG PHẢI là nhãn đơn lẻ**, mà là **tổng overhead cố định của toàn bộ cặp đầu vào `(query_long, label)` trước khi thêm nội dung trích xuất của chunk**:
  + Chuỗi câu hỏi dài `query_long` (text-only): **59 tokens**
  + Chuỗi nhãn ngữ cảnh `label` (text-only): **79 tokens**
  + Special tokens cross-encoder (`[CLS]`, `[SEP]`, `[SEP]`): **3 tokens**
  + Tổng overhead cố định: `59 + 79 + 3 = 141 tokens` (**27.5%** tổng ngân sách 512 tokens).
  + Ngân sách tối đa còn lại cho phần thân chunk (body text): `512 - 141 = 371 tokens`.
- Với câu hỏi gốc `query_orig`:
  + Chuỗi câu hỏi gốc `query_orig` (text-only): **17 tokens**
  + Chuỗi nhãn ngữ cảnh `label` (text-only): **79 tokens**
  + Special tokens cross-encoder (`[CLS]`, `[SEP]`, `[SEP]`): **3 tokens**
  + Tổng overhead cố định: `17 + 79 + 3 = 99 tokens` (**19.3%** tổng ngân sách 512 tokens).
  + Ngân sách tối đa còn lại cho phần thân chunk (body text): `512 - 99 = 413 tokens`.
- **Ý nghĩa:** Với tokenizer HuyDang, dung lượng thực tế dành cho thân chunk là `256 - 42 = 214 tokens`. Với MiniLM, khi gặp truy vấn dài tự nhiên, dung lượng dành cho thân chunk là `371 tokens`. Cả 2 ngưỡng này ràng buộc việc thiết kế kích thước chunk phải luôn tính đến overhead cặp (query + nhãn + special tokens).

### 4.5. Đánh đổi (Trade-offs) của Phương án 3B Lượt 3
1. **Số lượng chunk tăng lên:** Tiểu mục A từ 1 khối ban đầu tăng thành 5 chunks (khi tách Khách VN và Khách QT thành 1a và 1b).
2. **Lặp lại nội dung:** Câu dẫn khảo sát 2.3 (182 ký tự), tiêu đề bảng (140 ký tự) và điều kiện `Không bao gồm` (170 ký tự) được lặp lại tại 4 chunk giá vé. Tổng dung lượng lặp tăng thêm nhưng đảm bảo mỗi chunk giá vé đều là một đơn vị thông tin độc lập, có neo thời gian rõ ràng và không bị hiểu sai phạm vi giá.
3. **Mức độ sát trần của các chunk trẻ em:** `ca_hue_p3b_lead_chunk_2` (248 tokens) và `ca_hue_p3b_lead_chunk_3` (245 tokens) chỉ còn cách trần HuyDang (256) từ 8 đến 11 tokens (đạt 96–97% công suất). Mặc dù PASS về mặt kỹ thuật, đây là các chunk cần được Reviewer lưu ý đặc biệt nếu sau này có điều chỉnh nhãn ngữ cảnh dài hơn.

---

## 5. Bảng tổng hợp số đo Token toàn diện (Đã chuẩn hóa Query)

*Giới hạn tối đa (Limits): E5-small: 512 | E5-base: 512 | HuyDang: 256 | MiniLM pair: 512.*
*Lưu ý: Nhãn "PASS" chỉ có ý nghĩa kỹ thuật: độ dài input thực tế không vượt ngưỡng token của mô hình và kiểm tra exact-span đạt; KHÔNG mang nghĩa quality PASS về độ chính xác hay chất lượng câu trả lời.*

| Mã định danh Chunk (`chunk_id`) | Chars search_text | E5-sm (512) | E5-bs (512) | HuyDang (256) | MiniLM orig (512) | MiniLM long (512) | Trạng thái kỹ thuật |
|:---|---:|---:|---:|---:|---:|---:|:---:|
| **Hội xuân Gia Lạc** | | | | | | |
| `gia_lac_baseline_oversized` *(khối cũ)* | 1.204 | 352 | 352 | **272** ❌ | 512 | **540** ❌ | VƯỢT HuyDang & MLM-long |
| `gia_lac_p1_chunk_1` *(P1: Tên, loại hình, thời gian)* | 583 | 177 | 177 | 142 | 256 | 284 | **PASS** |
| `gia_lac_p1_chunk_2` *(P1: Nơi tổ chức, tính chất)* | 653 | 186 | 186 | 138 | 290 | 318 | **PASS** |
| `gia_lac_p2_chunk_1` *(P2: Định danh & tính chất)* | 662 | 192 | 192 | 155 | 292 | 320 | **PASS** |
| `gia_lac_p2_chunk_2` *(P2: Thời gian tổ chức)* | 226 | 65 | 65 | 51 | 109 | 137 | **PASS** |
| `gia_lac_p2_chunk_3` *(P2: Địa điểm tổ chức)* | 380 | 118 | 118 | 85 | 180 | 208 | **PASS** |
| **Đại Nội Huế — Ngọ Môn** | | | | | | |
| `ngo_mon_baseline_oversized` *(khối cũ)* | 1.798 | **530** ❌ | **530** ❌ | **423** ❌ | **738** ❌ | **774** ❌ | VƯỢT TẤT CẢ MODEL |
| `ngo_mon_p1_chunk_1` *(P1: Khái quát & Đài nền 5 cửa)* | 921 | 273 | 273 | 223 | 393 | 429 | **PASS** |
| `ngo_mon_p1_chunk_2` *(P1: Lầu Ngũ Phụng & Lịch sử)* | 948 | 278 | 278 | 214 | 394 | 430 | **PASS** |
| `ngo_mon_p2_chunk_1` *(P2: Khái quát & Đài nền)* | 921 | 273 | 273 | 223 | 393 | 429 | **PASS** |
| `ngo_mon_p2_chunk_2` *(P2: Lầu Ngũ Phụng kiến trúc)* | 553 | 168 | 168 | 129 | 235 | 271 | **PASS** |
| `ngo_mon_p2_chunk_3` *(P2: Ý nghĩa lịch sử thoái vị)* | 466 | 131 | 131 | 99 | 208 | 244 | **PASS** |
| **Vé Ca Huế trên sông Hương** | | | | | | |
| `ca_hue_baseline_table_only` *(khối cũ)* | 1.244 | 444 | 444 | **339** ❌ | **574** ❌ | **616** ❌ | VƯỢT HuyDang & MLM |
| `ca_hue_test_forced_adult_with_cond` *(ép gộp)* | 1.228 | 379 | 379 | **283** ❌ | **540** ❌ | **582** ❌ | VƯỢT HuyDang & MLM |
| `ca_hue_test_forced_child_with_cond` *(ép gộp)* | 1.304 | 434 | 434 | **344** ❌ | **598** ❌ | **640** ❌ | VƯỢT HuyDang & MLM |
| `ca_hue_p1_chunk_1` *(P1: Vé người lớn VN & QT)* | 751 | 249 | 249 | 182 | 342 | 384 | **PASS** |
| `ca_hue_p1_chunk_2` *(P1: Vé trẻ em 2 nhà cung cấp)* | 827 | 304 | 304 | 243 | 400 | 442 | **PASS (sát trần)** |
| `ca_hue_p1_chunk_3` *(P1: Tour ghép & Bao gồm/Không)* | 786 | 215 | 215 | 167 | 348 | 390 | **PASS** |
| `ca_hue_p2_chunk_1` *(P2: Vé người lớn VN & QT)* | 751 | 249 | 249 | 182 | 342 | 384 | **PASS** |
| `ca_hue_p2_chunk_2a` *(P2: Trẻ em chiều cao — Lá Quê)* | 598 | 211 | 211 | 166 | 294 | 336 | **PASS** |
| `ca_hue_p2_chunk_2b` *(P2: Trẻ em độ tuổi — Thuyền Rồng)*| 563 | 202 | 202 | 163 | 274 | 316 | **PASS** |
| `ca_hue_p2_chunk_3` *(P2: Tour ghép & Bao gồm/Không)* | 786 | 215 | 215 | 167 | 348 | 390 | **PASS** |
| `ca_hue_p3a_chunk_1` *(P3a: Hàng VN + Đủ 2 điều kiện)* | 1.069 | 328 | 328 | 249 | 475 | **517** ❌ | VƯỢT MLM-long |
| `ca_hue_p3a_chunk_2` *(P3a: Hàng QT + Đủ 2 điều kiện)* | 970 | 290 | 290 | 222 | 431 | 473 | **PASS** |
| `ca_hue_p3a_chunk_3` *(P3a: Trẻ em Lá Quê + Đủ 2 đk)* | 1.075 | 341 | 341 | **267** ❌ | 492 | **534** ❌ | VƯỢT HuyDang & MLM |
| `ca_hue_p3a_chunk_4` *(P3a: Trẻ em Thuyền Rồng + Đủ 2 đk)*| 1.040 | 332 | 332 | **264** ❌ | 472 | **514** ❌ | VƯỢT HuyDang & MLM |
| `ca_hue_p3a_chunk_5` *(P3a: Đoạn dẫn tour ghép lẻ)* | 309 | 85 | 85 | 66 | 150 | 192 | **PASS** |
| `ca_hue_p3b_chunk_1` *(P3b Lượt 2: Vé lớn VN+QT + Không bg - chưa câu dẫn)*| 923 | 296 | 296 | 224 | 416 | 458 | **PASS** |
| `ca_hue_p3b_chunk_2` *(P3b Lượt 2: Trẻ Lá Quê + Không bg - chưa câu dẫn)*| 770 | 258 | 258 | 208 | 368 | 410 | **PASS** |
| `ca_hue_p3b_chunk_3` *(P3b Lượt 2: Trẻ Thuyền Rồng + Không bg - chưa câu dẫn)*| 735 | 249 | 249 | 205 | 348 | 390 | **PASS** |
| `ca_hue_p3b_chunk_4` *(P3b Lượt 2: Tour ghép + Bao gồm chi tiết)*| 615 | 168 | 168 | 125 | 274 | 316 | **PASS** |
| `ca_hue_p3b_lead_chunk_1_merged` *(P3b Lượt 3: Gộp VN+QT + Câu dẫn 2.3 + Không bg)*| 1.107 | 349 | 349 | **264** ❌ | 485 | **527** ❌ | VƯỢT HuyDang & MLM-long |
| `ca_hue_p3b_lead_chunk_1a` *(P3b Lượt 3: Khách VN riêng + Câu dẫn 2.3 + Không bg)*| 948 | 298 | 298 | 230 | 420 | 462 | **PASS** |
| `ca_hue_p3b_lead_chunk_1b` *(P3b Lượt 3: Khách QT riêng + Câu dẫn 2.3 + Không bg)*| 849 | 260 | 260 | 203 | 376 | 418 | **PASS** |
| `ca_hue_p3b_lead_chunk_2` *(P3b Lượt 3: Trẻ Lá Quê + Câu dẫn 2.3 + Không bg)*| 954 | 311 | 311 | 248 | 437 | 479 | **PASS (sát trần 97%)** |
| `ca_hue_p3b_lead_chunk_3` *(P3b Lượt 3: Trẻ Thuyền Rồng + Câu dẫn 2.3 + Không bg)*| 919 | 302 | 302 | 245 | 417 | 459 | **PASS (sát trần 96%)** |
| `ca_hue_p3b_lead_chunk_4_service` *(P3b Lượt 3: Tour ghép + Bao gồm - không câu dẫn)*| 615 | 168 | 168 | 125 | 274 | 316 | **PASS** |
| `ca_hue_p3b_lead_chunk_4_service_with_lead` *(P3b Lượt 3: Tour ghép + Bao gồm + Câu dẫn)*| 799 | 221 | 221 | 165 | 343 | 385 | **PASS** |
| **Đối chứng mục ngắn** | | | | | | |
| `control_me_keo_info` *(Bún bò Mệ Kéo)* | 303 | 97 | 97 | 78 | 144 | 173 | **PASS** |
| `control_sea_module` *(Lịch trình Biển & Đầm phá)* | 698 | 204 | 204 | 160 | 305 | 334 | **PASS** |

---

## 6. Kiểm tra độ bao phủ (Coverage Audit) và Khoảng cách ký tự

### 6.1. Quy ước Source Locator
- Tệp nguồn giải mã UTF-8, chuyển đổi `\r\n` và `\r` thành `\n`.
- Không Unicode-normalize (NFC/NFD), không loại bỏ dấu thanh hay chỉnh sửa ký tự nguồn.
- Vị trí `[start, end)` là chỉ số điểm mã Unicode (zero-based Unicode code points), `end` exclusive.
- **Tính nguyên văn:** 100% các phân đoạn `evidence_parts` của tất cả các chunk đều đạt `source_text[start:end] == part['text']` (`True`).

### 6.2. Kiểm kê chi tiết ký tự và khoảng hở (Character & Content Accounting)

#### Mẫu 1: Hội xuân Gia Lạc (`## Thông tin chung`)
- Vùng mục tiêu: `[40, 1211)` — tổng số ký tự: **1.171 ký tự**.
- Phân bổ theo Phương án 1:
  - `gia_lac_p1_chunk_1`: span `[40, 590)` (550 ký tự nội dung).
  - Khoảng hở phân tách (whitespace gap): span `[590, 591)` là **01 ký tự `\n`** phân dòng giữa 2 bullet list.
  - `gia_lac_p1_chunk_2`: span `[591, 1211)` (620 ký tự nội dung).
- **Hạch toán:** `550 (chunk 1) + 1 (\n) + 620 (chunk 2) = 1.171 / 1.171 ký tự`.
- **Độ bao phủ nội dung:** 100% nội dung thông tin được bao phủ, không có phần lặp lại, không có phần lấy thêm ngoài mục.

#### Mẫu 2: Ngọ Môn (`### Ngọ Môn`)
- Vùng mục tiêu: `[10219, 11945)` — tổng số ký tự: **1.726 ký tự**.
- Phân bổ theo Phương án 1:
  - `ngo_mon_p1_chunk_1`: span `[10219, 11068)` (849 ký tự nội dung: đoạn dẫn + đài nền).
  - Khoảng hở phân tách (whitespace gap): span `[11068, 11069)` là **01 ký tự `\n`** giữa bullet đài nền và bullet Lầu Ngũ Phụng.
  - `ngo_mon_p1_chunk_2`: span `[11069, 11945)` (876 ký tự nội dung: Lầu Ngũ Phụng + lịch sử thoái vị).
- **Hạch toán:** `849 (chunk 1) + 1 (\n) + 876 (chunk 2) = 1.726 / 1.726 ký tự`.
- **Độ bao phủ nội dung:** 100% nội dung thông tin được bao phủ, không có phần lặp lại, không có phần lấy thêm ngoài mục.

#### Mẫu 3: Bảng Ca Huế (`### 2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế` đến hết tiểu mục A)
- **Vùng mục tiêu mở rộng:** `[10409, 12287)` — tổng số ký tự: **1.878 ký tự** (bao gồm câu dẫn khảo sát mục 2.3, tiêu đề mục A và toàn bộ nội dung tiểu mục A).
- **Hạch toán chi tiết cấu phần (Character Accounting):**
  1. Câu dẫn khảo sát mục 2.3: span `[10409, 10591)` (182 ký tự: *"Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu..."*).
  2. Khoảng hở: span `[10591, 10593)` là **02 ký tự `\n\n`** (dòng trống trước heading A).
  3. Tiêu đề tiểu mục A: span `[10593, 10641)` (48 ký tự: `#### A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)` — được lưu và biểu diễn đầy đủ trong metadata `heading_path` / nhãn ngữ cảnh).
  4. Khoảng hở: span `[10641, 10643)` là **02 ký tự `\n\n`** (dòng trống trước đoạn dẫn tour ghép).
  5. Đoạn dẫn tour ghép: span `[10643, 10758)` (115 ký tự).
  6. Khoảng hở: span `[10758, 10760)` là **02 ký tự `\n\n`** (dòng trống trước bảng).
  7. Tiêu đề cột bảng: span `[10760, 10900)` (140 ký tự).
  8. Khoảng hở: span `[10900, 10901)` là **01 ký tự `\n`** (xuống dòng sau header).
  9. Hàng vé Khách VN: span `[10901, 11158)` (257 ký tự).
  10. Khoảng hở: span `[11158, 11159)` là **01 ký tự `\n`** (xuống dòng giữa hàng VN và hàng QT).
  11. Hàng vé Khách QT: span `[11159, 11317)` (158 ký tự).
  12. Khoảng hở: span `[11317, 11318)` là **01 ký tự `\n`** (xuống dòng giữa hàng QT và hàng Trẻ em Lá Quê).
  13. Hàng vé Trẻ em Lá Quê (chiều cao): span `[11318, 11581)` (263 ký tự).
  14. Khoảng hở: span `[11581, 11582)` là **01 ký tự `\n`** (xuống dòng giữa hàng Trẻ em Lá Quê và hàng Trẻ em Thuyền Rồng).
  15. Hàng vé Trẻ em Thuyền Rồng (độ tuổi): span `[11582, 11810)` (228 ký tự).
  16. Khoảng hở: span `[11810, 11812)` là **02 ký tự `\n\n`** (dòng trống sau bảng).
  17. Điều kiện `Bao gồm` chi tiết: span `[11812, 12116)` (304 ký tự).
  18. Khoảng hở: span `[12116, 12117)` là **01 ký tự `\n`** (xuống dòng giữa 2 bullet điều kiện).
  19. Điều kiện `Không bao gồm`: span `[12117, 12287)` (170 ký tự).
- **Hạch toán tổng cộng:** `182 (lead) + 2 (gap) + 48 (heading A) + 2 (gap) + 115 (intro) + 2 (gap) + 140 (header) + 1 (gap) + 257 (VN) + 1 (gap) + 158 (QT) + 1 (gap) + 263 (child Lá Quê) + 1 (gap) + 228 (child Thuyền Rồng) + 2 (gap) + 304 (bao gồm) + 1 (gap) + 170 (không bao gồm) = 1.878 / 1.878 ký tự` (100.0% khớp tuyệt đối).
- **Phân bổ theo Phương án 3B Lượt 3 (5 chunks đề xuất):**
  - `ca_hue_p3b_lead_chunk_1a`: mang câu dẫn 2.3 (182), header bảng (140), hàng VN (257), Không bao gồm (170).
  - `ca_hue_p3b_lead_chunk_1b`: mang câu dẫn 2.3 (182), header bảng (140), hàng QT (158), Không bao gồm (170).
  - `ca_hue_p3b_lead_chunk_2`: mang câu dẫn 2.3 (182), header bảng (140), hàng Trẻ em Lá Quê (263), Không bao gồm (170).
  - `ca_hue_p3b_lead_chunk_3`: mang câu dẫn 2.3 (182), header bảng (140), hàng Trẻ em Thuyền Rồng (228), Không bao gồm (170).
  - `ca_hue_p3b_lead_chunk_4_service`: mang đoạn dẫn tour ghép (115) và điều kiện Bao gồm chi tiết (304).
- **Phần lặp lại (repeated parts):**
  - Câu dẫn khảo sát 2.3 (182 ký tự): lặp tại 4 chunk giá vé để bảo toàn danh sách đơn vị và mốc thời gian T9/2026.
  - Tiêu đề cột bảng (140 ký tự): lặp tại 4 chunk giá vé để bảo toàn cấu trúc bảng.
  - Điều kiện `Không bao gồm` (170 ký tự): lặp tại 4 chunk giá vé để bảo toàn giới hạn loại trừ dịch vụ tối cần thiết.
- **Phân tích đối với chunk dịch vụ riêng:**
  - Chunk `ca_hue_p3b_lead_chunk_4_service` không chứa mức giá khảo sát nào nên không bắt buộc mang theo câu dẫn 2.3. Nếu gắn thêm (biến thể `ca_hue_p3b_lead_chunk_4_service_with_lead`), chunk vẫn PASS an toàn (165 tokens HuyDang), nhưng việc gắn câu "Dưới đây là mức giá..." vào một chunk thuần túy về dịch vụ có thể gây nhiễu ngữ nghĩa (semantic noise).

---

## 7. Điều chỉnh kết luận và Khuyến nghị kỹ thuật cho Reviewer

Tuân thủ nghiêm ngặt các chỉ đạo điều chỉnh của Reviewer:

1. **Ranh giới của trạng thái "PASS":**
   - Kết luận "PASS" trong toàn bộ báo cáo này thuần túy chỉ ra rằng số lượng token của chunk không vượt ngưỡng kỹ thuật tối đa của tokenizer (`max_length`) và văn bản trích xuất khớp chính xác tuyệt đối với tệp nguồn (`exact_match = True`).
   - "PASS" **không phải là quality PASS** và không bảo đảm chất lượng truy xuất (Recall/MRR) hay tính chính xác của câu trả lời do LLM sinh ra.
2. **Về việc phân tách nhà cung cấp:**
   - Việc tách bảng giá của Lá Quê Travel và Thuyền Rồng Huế thành 2 chunk riêng biệt (như ở P2 và P3b) giúp biểu diễn dữ liệu rành mạch ở tầng lưu trữ, nhưng **không bảo đảm 100% LLM sẽ không nhầm lẫn** nếu ngữ cảnh truy xuất sau này có sự nhiễu loạn.
3. **Về nguy cơ của retrieval baseline Top-5:**
   - Việc tách điều kiện ra chunk riêng (ở P1) tạo nguy cơ thiếu thông tin điều kiện nếu Top-5 chỉ truy xuất được bảng giá. Tuy nhiên, đây là nhận định dựa trên phân tích cấu trúc dữ liệu; **chưa có retrieval benchmark run nào được thực hiện** trên corpus mới để khẳng định điều kiện chắc chắn bị bỏ sót trong thực tế.
4. **Hủy bỏ các đề xuất cứng về token policy:**
   - Bỏ toàn bộ đề xuất hard limit 235–240 dựa trên giả định cố định 16–20 tokens cho nhãn (bởi vì thực tế đã đo cho thấy nhãn có thể tốn từ 15 đến hơn 42 tokens tùy theo độ sâu của heading).
   - Không thiết lập công thức quy đổi gần đúng giữa tokens HuyDang, tokens E5 và số lượng ký tự như một contract ràng buộc.
   - Không chốt token target cho toàn bộ corpus từ 6 mẫu khảo sát có giới hạn này.
   - Khẳng định nguyên tắc: **Heading Markdown là dấu hiệu tổ chức trực quan của tài liệu, không mặc định mỗi heading phải trở thành một chunk độc lập**.
5. **Đề xuất kỹ thuật để Reviewer cân nhắc khi thiết kế spec:**
   - Reviewer có thể đối chiếu giữa:
     + **Phương án 1** (3 chunks: gộp người lớn VN+QT, gộp trẻ em 2 đơn vị, tách điều kiện ra chunk riêng).
     + **Phương án 3B Lượt 3** (5 chunks: tách riêng Khách VN `1a` [230 tokens HuyDang] và Khách QT `1b` [203 tokens HuyDang] để tránh tràn token; tách riêng trẻ em Lá Quê `2` và Thuyền Rồng `3`; lặp lại nguyên văn cả câu dẫn khảo sát 2.3 [182 chars, xác định mốc 09/2026 và 3 đơn vị] cùng điều kiện loại trừ `Không bao gồm` [170 chars] tại cả 4 chunk giá vé; chunk dịch vụ `4` đứng độc lập [125 tokens HuyDang]).
   - **Lưu ý biên độ an toàn token:** Trong P3B Lượt 3, `ca_hue_p3b_lead_chunk_2` (248 tokens) và `ca_hue_p3b_lead_chunk_3` (245 tokens) đã chạm mức 96–97% giới hạn 256 của HuyDang (cách trần 8–11 tokens). Nếu cây thư mục hoặc nhãn ngữ cảnh sau này thay đổi dài hơn, đây là 2 chunk đầu tiên có nguy cơ vượt trần.

---

## 8. Lệnh tái lập thực nghiệm và Danh mục tệp bàn giao

### 8.1. Lệnh tái lập thực nghiệm độc lập
Toàn bộ khảo sát có thể được tái lập độc lập bằng lệnh:
```bash
uv run --no-sync python reports/artifacts/full_corpus_chunk_samples_2026_09_09.py
```
Script nạp 4 tokenizer local từ cache HF, đo đạc toàn bộ các chunk với các query cố định chuẩn hóa và cập nhật tệp artifact JSON.

### 8.2. Danh mục tệp bàn giao
1. `reports/artifacts/full_corpus_chunk_samples_2026_09_09.py` — Kịch bản Python đo lường độc lập (đã cập nhật các chunk P3b bổ sung câu dẫn 2.3 và split VN/QT).
2. `reports/artifacts/full_corpus_chunk_samples_2026_09_09.json` — Dữ liệu JSON chi tiết chứa đầy đủ text, query cố định, spans, tokens và coverage audit mở rộng.
3. `reports/full_corpus_chunk_samples_tokenizer_survey_2026_09_09.md` — Báo cáo tổng hợp cập nhật lượt 3 này.
