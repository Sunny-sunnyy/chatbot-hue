# Implementation Report: Khảo sát đo token hai input Ca Huế VN/QT đã sửa ranh giới

Implementer: Implementer  
Date: 2026-09-09  
Canonical contract: `session_prompt/FULL_CORPUS_VN_QT_TOKEN_CHECK_HANDOFF.md`  
Base commit: `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`  
Head commit: worktree  
Risk level: low (khảo sát tokenizer local, không đổi runtime)  
Git authorization: none  

---

## 1. Phạm vi

### Yêu cầu được giao
Thực hiện khảo sát đo token độc lập cho đúng hai input composite Ca Huế (khách Việt Nam và khách quốc tế) đã sửa ranh giới hàng hoàn chỉnh trong JSON parser:
- Đọc đúng hai composites từ `reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json`:
  - Khách Việt Nam: body span `[10901, 11141)` (240 ký tự), search_text 931 ký tự.
  - Khách quốc tế: body span `[11142, 11317)` (175 ký tự), search_text 866 ký tự.
- Đối chiếu toàn bộ 4 evidence parts của mỗi composite với tệp nguồn chuẩn hóa LF `knowledge-base-hue/travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`.
- Đo độ dài token đầy đủ không truncation (`truncation=False`) cho 3 mô hình embedding (E5-small, E5-base, HuyDang) và reranker cross-encoder MiniLM (với cả `query_orig` và `query_long`).
- Áp dụng exact snapshots và cấu hình trong local cache: E5-small (512), E5-base (512), HuyDang (256), MiniLM pair (512).
- Không sửa runtime, không tải mạng/dependencies, không suy luận weights/API/Qdrant/benchmark, không sửa dữ liệu cũ hay artifacts lịch sử.

### Trạng thái hoàn thành
Toàn bộ phạm vi khảo sát theo Review Contract đã được thực hiện và nghiệm thu đạt 100%. Cả hai input đều được xác nhận nằm trong toàn bộ các giới hạn token tương ứng.

---

## 2. Thay đổi chính

Chỉ tạo ba artifacts mới theo đúng đường dẫn quy định trong contract:
1. `reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.py`: Script Python độc lập thực hiện nạp nguồn, đối chiếu slice, nạp tokenizer local với `local_files_only=True`, đo token không truncation và ghi kết quả.
2. `reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.json`: Artifact JSON lưu trữ toàn bộ metadata môi trường, revision tokenizer, thông số input, 8 evidence parts và kết quả đo token thực tế để Reviewer kiểm chứng độc lập và tái lập.
3. `reports/full_corpus_vn_qt_token_check_2026_09_09.md`: Báo cáo triển khai chi tiết này.
4. Cập nhật `session_prompt/CURRENT_HANDOFF.md` chuyển quyền về Reviewer với kind `final_review`.

---

## 3. Cách đã chạy thật

### Lệnh thực thi
```bash
uv run python reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.py
```

### Môi trường thực tế và phiên bản gói
- Python: `3.13.15`
- Transformers: `5.14.1`
- PyVi: `0.1.1`

### Exact Snapshots & Tokenizer Revisions (Local HF Cache)
Toàn bộ nạp với `local_files_only=True` từ `/home/minhhieu/.cache/huggingface/hub/`:
1. `intfloat/multilingual-e5-small`:
   - Directory: `models--intfloat--multilingual-e5-small/snapshots/614241f622f53c4eeff9890bdc4f31cfecc418b3`
   - Config limit: `512`
   - Preprocessing: Thêm prefix `'passage: '`, `add_special_tokens=True`, `truncation=False`.
2. `intfloat/multilingual-e5-base`:
   - Directory: `models--intfloat--multilingual-e5-base/snapshots/d128750597153bb5987e10b1c3493a34e5a4502a`
   - Config limit: `512`
   - Preprocessing: Thêm prefix `'passage: '`, `add_special_tokens=True`, `truncation=False`.
3. `CODE4LIFEOFFICIAL/huydang-dek21-embedding`:
   - Directory: `models--CODE4LIFEOFFICIAL--huydang-dek21-embedding/snapshots/517f1af7dd04a57194f1de2990f0c6ede0a3109b`
   - Config limit: `256` (`sentence_bert_config.json` `max_seq_length=256`, `config.json` `max_position_embeddings=258`)
   - Preprocessing: Phân đoạn từ tiếng Việt bằng `ViTokenizer.tokenize(search_text)`, không thêm prefix `'passage: '`, `add_special_tokens=True`, `truncation=False`.
4. `cross-encoder/ms-marco-MiniLM-L-6-v2`:
   - Directory: `models--cross-encoder--ms-marco-MiniLM-L-6-v2/snapshots/233902d25c440f23af6f7d6e94d2946bac0bee0a`
   - Config limit: `512` (`tokenizer_config.json` và `config.json` `model_max_length=512`)
   - Preprocessing: Tokenize cặp `(query, search_text)`, không prefix, `add_special_tokens=True`, `truncation=False`.

### Queries Ca Huế cố định dùng cho MiniLM
- `query_orig`: `"Vé Ca Huế cho trẻ em được tính như thế nào?"`
- `query_long`: `"Giá vé xem Ca Huế ghép thuyền trên sông Hương cho người lớn và trẻ em bao nhiêu tiền một người, áp dụng điều kiện bao gồm và không bao gồm những dịch vụ gì?"`

---

## 4. Kết quả quan sát

### 4.1. Đối chiếu nguồn dữ liệu và ranh giới
Nguồn: `knowledge-base-hue/travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md` (chuẩn hóa LF, Unicode code points).

1. **Composite Khách Việt Nam (`ca_hue_tour_ghep_vn`):**
   - Body span: `[10901, 11141)` (240 ký tự) — Đúng nguyên văn hàng `| **Khách Việt Nam** | ... |`.
   - Lead span: `[10409, 10591)` (182 ký tự) — Câu dẫn khảo sát thực tế tháng 09/2026.
   - Header span: `[10760, 10900)` (140 ký tự) — Tiêu đề bảng và dòng phân cách `|---|...|`.
   - Exclusions span: `[12117, 12287)` (170 ký tự) — Mục `- **Không bao gồm:** ...`.
   - Label tài liệu & mục: 194 ký tự.
   - Tổng độ dài `search_text`: 931 ký tự.
   - Kết quả đối chiếu: 4/4 parts khớp 100% lát cắt nguồn `source_lf[start:end] == part['text']`.

2. **Composite Khách quốc tế (`ca_hue_tour_ghep_qt`):**
   - Body span: `[11142, 11317)` (175 ký tự) — Đúng nguyên văn hàng `| **Khách quốc tế** | ... |`.
   - Lead span: `[10409, 10591)` (182 ký tự).
   - Header span: `[10760, 10900)` (140 ký tự).
   - Exclusions span: `[12117, 12287)` (170 ký tự).
   - Label tài liệu & mục: 194 ký tự.
   - Tổng độ dài `search_text`: 866 ký tự.
   - Kết quả đối chiếu: 4/4 parts khớp 100% lát cắt nguồn `source_lf[start:end] == part['text']`.

### 4.2. Bảng kết quả đo token thực tế (không truncation)

| Mẫu composite | Ký tự search_text | E5-small (limit 512) | E5-base (limit 512) | HuyDang (limit 256) | MiniLM orig (limit 512) | MiniLM long (limit 512) | Kết luận |
|---|---:|---:|---:|---:|---:|---:|---|
| **Khách Việt Nam (đã sửa)** | 931 | **290** (dư 222) | **290** (dư 222) | **224** (dư 32) | **411** (dư 101) | **453** (dư 59) | **VỪA (PASS_ALL)** |
| **Khách quốc tế (đã sửa)** | 866 | **268** (dư 244) | **268** (dư 244) | **208** (dư 48) | **385** (dư 127) | **427** (dư 85) | **VỪA (PASS_ALL)** |
| *Giới hạn mô hình* | - | *512* | *512* | *256* | *512* | *512* | - |

### 4.3. So sánh với số đo lịch sử của input sai ranh giới

| Input / Phiên bản | Ký tự search_text | E5-small/base | HuyDang | MiniLM long | Ghi chú ranh giới |
|---|---:|---:|---:|---:|---|
| Khách VN (cũ - ranh giới sai) | 948 | 298 | 230 | 462 | Bị lấn 17 ký tự sang hàng QT (`\n\| **Khách quốc t`) |
| **Khách VN (mới - ranh giới đúng)** | **931** | **290** | **224** | **453** | **Đúng ranh giới nguyên hàng `[10901, 11141)` (240 chars)** |
| Khách QT (cũ - ranh giới sai) | 849 | 260 | 203 | 418 | Mất nhãn hàng khách quốc tế (bắt đầu từ `** \| 150.000`) |
| **Khách QT (mới - ranh giới đúng)** | **866** | **268** | **208** | **427** | **Đúng ranh giới nguyên hàng `[11142, 11317)` (175 chars)** |

**Nhận xét kỹ thuật:**
- Cả hai input composite Ca Huế (VN và QT) hoàn chỉnh với đầy đủ Lead (khảo sát tháng 09/2026), Header bảng, nguyên hàng giá và Điều kiện Không bao gồm **đều vừa hoàn toàn** trong tất cả giới hạn của E5-small, E5-base, HuyDang và MiniLM pair (kể cả với câu hỏi dài 45 từ).
- Khoảng dư an toàn (margin) của HuyDang là **32 tokens** đối với khách VN và **48 tokens** đối với khách QT.
- Khoảng dư an toàn của MiniLM pair long là **59 tokens** đối với khách VN và **85 tokens** đối với khách QT.
- Điều này chứng minh phương án P3B lượt 3 (chia theo hàng kèm câu dẫn và điều kiện loại trừ) hoàn toàn khả thi về mặt kỹ thuật tokenization đối với cả 4 mô hình ứng viên.

---

## 5. Lỗi và giới hạn

1. **Lỗi và Blocker:** Không có lỗi hoặc blocker nào trong quá trình thực thi.
2. **Giới hạn phạm vi:**
   - Phép đo áp dụng cho representation mẫu cụ thể hiện tại trong artifact parser. Kết quả này chứng minh độ dài token của hai composite mẫu là hợp lệ, không tự động coi là acceptance của mọi representation runtime khác trong tương lai.
   - Kết quả đo token thuần túy không thay thế cho benchmark đánh giá chất lượng retrieval hoặc generation trên toàn bộ corpus.

---

## 6. Handoff cho Reviewer

1. **Tài liệu Reviewer nên đọc:**
   - Báo cáo này: `reports/full_corpus_vn_qt_token_check_2026_09_09.md`
   - Dữ liệu chi tiết: `reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.json`
2. **Lệnh tái lập độc lập:**
   ```bash
   uv run python reports/artifacts/full_corpus_vn_qt_token_check_2026_09_09.py
   ```
3. **Trạng thái Git:**
   - `git_authorization: none` (không commit/push).
   - `session_prompt/CURRENT_HANDOFF.md` được cập nhật chuyển vai trò sang Reviewer (`final_review`).
