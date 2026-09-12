# BÁO CÁO KHẢO SÁT TÀI LIỆU VÀ SOURCE THAM KHẢO VỀ CHUNKING & CONTEXTUALIZATION (BẢN HIỆU CHỈNH KỸ THUẬT)

**Dự án:** `/home/minhhieu/hue_rag`  
**Ngày cập nhật hiệu chỉnh:** 2026-09-09  
**Vai trò:** Implementer (Khảo sát, đối chiếu bằng chứng kỹ thuật, phục vụ Reviewer và User thảo luận chốt thiết kế toàn corpus)  
**Phạm vi:** Khảo sát đối chiếu kiến trúc và bằng chứng thực nghiệm; không sửa mã runtime/corpus, không chạy benchmark/retrieval mới, không gọi paid API, giữ nguyên trạng thái Git.

---

## MỤC HIỆU CHỈNH (CORRECTION LOG - 2026-09-09)

Nhằm đảm bảo tính khách quan và trung thực tuyệt đối của báo cáo khảo sát kỹ thuật, dưới đây là bảng ghi nhận các điểm đã được kiểm tra lại đối chiếu với mã nguồn, dữ liệu thực tế và tài liệu nghiên cứu:

| Hạng mục | Khẳng định ở bản trước | Bằng chứng kiểm tra lại thực tế | Nội dung đã hiệu chỉnh / Ghi nhận |
| :--- | :--- | :--- | :--- |
| **Nguồn mẫu Ca Huế (Mục 3.4)** | Dẫn nhầm nguồn `performing_arts/ca_hue_on_huong_river.md` và dựng bảng thuyền đơn/đôi không khớp khảo sát. | Nguồn đúng trong JSON khảo sát lượt 3 là `knowledge-base-hue/travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`, section 2.3. | Lấy nguyên văn từ `reports/artifacts/full_corpus_chunk_samples_2026_09_09.json`: đúng chunk ID (`ca_hue_p3b_lead_chunk_2`, `ca_hue_p3b_lead_chunk_3`), span offset, search text, queries và tokenizer counts. |
| **Ví dụ `llm_rag` (Mục 3.1)** | Dùng ví dụ tự soạn "NMK Villa Hội An" không có trong dữ liệu. | File `llm_rag/backend/data/processed/projects.json` chứa các bản ghi thật như ID: 46 ("Homestay Nhơn Hải 14,3 x 12m...") và ID: 86. File helper thực tế là `split_paragraphs.py` (không phải `paragraph_helpers.py`). | Thay bằng bản ghi thực tế ID: 46 từ `projects.json`, cập nhật đúng đường dẫn file helper `split_paragraphs.py`. Ghi rõ pseudocode khi minh họa logic. |
| **Ví dụ `rag_old_0` (Mục 3.2, 3.3)** | Dùng ví dụ tự soạn "Section 4: Accidental Damage Cover" và giả định output LLM. | Thư mục `knowledge-base/` của `rag_old_0` gồm các file sản phẩm thật như `products/Carllm.md`. Trong code không có log lưu sẵn output LLM của từng file. | Dẫn trích đoạn thật từ `products/Carllm.md`. Output của LLM trong ingestion được ghi nhận là "chưa xác minh output thực tế", chỉ dẫn cấu trúc từ prompt và Pydantic schema. |
| **Model & Flow của `rag_old_0/pro_implementation`** | Ghi rerank dùng `gpt-4.1-nano`, generator dùng `gpt-5-nano`. | Kiểm tra file: `ingest.py` dùng `MODEL = "openai/gpt-4.1-nano"`; `answer.py` dùng `MODEL = "openai/gpt-5-nano"` cho CẢ `rewrite_query`, `rerank` và `answer_question`. | Sửa chính xác model name và flow gọi theo từng file và số dòng thực tế. |
| **Số liệu Bài 135 (Phiên âm Day 5)** | Trích dẫn số liệu dạng khẳng định nguyên văn lời giảng, suy đoán "hơn 80% mức tăng đến từ embedding". | File `rag_old_0/phien_am_bai_hoc/day5.txt` (dòng 596–660) là bản tóm tắt bài học. Giảng viên nêu 3 giai đoạn: Giai đoạn 2 đổi cả embedding lớn VÀ chunk size (MRR 0.73 -> 0.79); Giai đoạn 3 thêm Semantic Chunking, Query Rewrite, Reranker, Dual retrieval (MRR -> 0.91). | Dẫn đúng vị trí dòng của `day5.txt`. Xác định rõ đây là bản tổng hợp bài học, không có ablation study phân rã từng biến số; loại bỏ hoàn toàn phỏng đoán suy diễn "hơn 80%". |
| **Diễn giải bài báo NAACL 2025** | Khẳng định bài báo khuyến nghị "structural + context enrichment + hybrid retrieval". | Abstract và nội dung NAACL 2025 (Qu, Tu, Bao) chỉ đánh giá thực nghiệm semantic chunking (theo sentence embeddings) và kết luận chi phí không tương xứng với hiệu năng trên 3 tác vụ RAG. | Đính chính: Khuyến nghị về structural chunking hay hybrid retrieval là suy luận tổng hợp của kỹ sư từ các tài liệu khác, không phải kết luận của bài báo NAACL. Phân biệt rõ 3 khái niệm semantic boundaries. |
| **Diễn giải Anthropic Contextual Retrieval** | Quy đổi 50–100 tokens thành số token HuyDang; coi % giảm failure là chất lượng cho Huế. | Anthropic giữ nguyên boundaries và sinh context prefix bằng Claude Haiku. Tokenizer của Claude khác biệt với HuyDang. Kết quả công bố trên dataset riêng của Anthropic. | Làm rõ: Anthropic không chia lại boundaries; không quy đổi số token Claude sang HuyDang; kết quả nghiên cứu không dùng làm bằng chứng chất lượng cho corpus tiếng Việt của Huế. |
| **3 Hướng A, B, C đã thống nhất** | Đưa đề xuất metadata câu hỏi giả định vào C; kết luận loại bỏ Phương án B. | Quyết định đã thống nhất: A (Cấu trúc Markdown + local tokenizer), B (Giữ boundaries/evidence A + API context tìm kiếm riêng), C (LLM hỗ trợ boundaries chỉ khi có lý do từ A/B). | Khôi phục đúng định nghĩa A, B, C. Tách đề xuất metadata câu hỏi giả định/tags thành mục đề xuất mới riêng chưa duyệt. Ghi nhận ràng buộc mở của B thay vì tự ý kết luận loại bỏ B. |
| **Số đo token MiniLM và khẳng định tuyệt đối** | Ghi MiniLM tối đa 425 tokens; dùng từ "an toàn tuyệt đối", "0% hallucination", "tốc độ tính bằng giây", "tương thích hoàn hảo". | Trong JSON khảo sát lượt 3, chunk `ca_hue_p3b_lead_chunk_2` có `minilm_long` là **479 tokens** (gần sát 512). | Sửa lại đúng 479 tokens. Loại bỏ mọi khẳng định tuyệt đối hóa chưa đo đạc trên toàn bộ corpus. |

---

## 1. TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

### 1.1. Mục đích khảo sát
Báo cáo này thu thập và đối chiếu các bằng chứng kỹ thuật từ mã nguồn thực tế và các công bố chính thức nhằm cung cấp cơ sở dữ liệu khách quan cho Reviewer và User thảo luận chốt thiết kế chunking toàn corpus Huế:
1. **Mã nguồn tham khảo:**
   - `llm_rag`: Hệ thống production tiếng Việt với dữ liệu JSON records (lĩnh vực kiến trúc NMK), hoạt động độc lập không phụ thuộc LLM trong pha ingestion (`backend/ingestion/`).
   - `rag_old_0/implementation`: Pipeline LangChain cơ bản trên văn bản Markdown tiếng Anh (Insurellm), phân đoạn cơ học bằng ký tự.
   - `rag_old_0/pro_implementation`: Pipeline nâng cao dùng LLM API (`gpt-4.1-nano`) để sinh chunk có cấu trúc (`headline`, `summary`, `original_text`), kết hợp query rewrite và list-wise reranker bằng `gpt-5-nano`.
   - `rag_old_0/phien_am_bai_hoc`: Tóm tắt bài học Day 5 (đặc biệt là bài 135) ghi lại các giai đoạn cải tiến chỉ số đánh giá.
2. **Tài liệu nghiên cứu và công bố chính thức:**
   - Nghiên cứu thực nghiệm NAACL 2025: *"Is Semantic Chunking Worth the Computational Cost?"* (Qu, Tu, Bao).
   - Anthropic Engineering: *"Contextual Retrieval"* (2024).
   - Docling Architecture: *Chunking Concepts & HybridChunker* (IBM, 2024–2026).
   - LangChain: *MarkdownHeaderTextSplitter*.

### 1.2. Các điểm đã được kiểm chứng từ bằng chứng thực tế
- **Đánh giá đa biến số trong `rag_old_0`:** Dữ liệu bài học 135 cho thấy sự cải thiện từ MRR 0.73 lên 0.91 không thể quy riêng cho việc chia chunk bằng LLM. Quá trình nâng cấp gồm 2 bước: bước 1 đổi embedding model lớn hơn kèm chỉnh chunk size (tăng lên ~0.79 MRR); bước 2 kết hợp đồng thời semantic chunking, query rewrite, dual retrieval (lấy 40 candidates) và reranker bằng LLM (đạt 0.91 MRR). Không có thử nghiệm bóc tách riêng lẻ (ablation study) cho từng thành phần.
- **Tính toàn vẹn của bằng chứng trong `rag_old_0/pro_implementation`:** Mã nguồn `ingest.py` giao toàn quyền cho prompt LLM trích xuất `original_text`, hoàn toàn không có bước kiểm tra exact match so với văn bản gốc.
- **Kết luận của NAACL 2025:** Phương pháp semantic chunking dựa trên cosine distance của sentence embeddings tốn kém tài nguyên tính toán nhưng không mang lại cải thiện ổn định và nhất quán trên các tác vụ retrieval và answer generation so với fixed-size chunking.
- **Ràng buộc đo lường mẫu tại Huế:** Mô hình embedding `huydang-dek21-embedding` có trần cứng 256 tokens; reranker `ms-marco-MiniLM-L-6-v2` có trần cứng 512 tokens. Trên mẫu bảng vé Ca Huế khảo sát (Lượt 3), việc bổ sung đầy đủ nhãn phân cấp và câu dẫn điều kiện thời gian 09/2026 đã khiến độ dài đạt **248 tokens HuyDang** và **479 tokens MiniLM (với query dài)**.

### 1.3. Các vấn đề kiến trúc còn mở cần Reviewer và User quyết định
1. Lựa chọn giữa 3 hướng thiết kế đã thống nhất (A, B, C) phù hợp với ngân sách token và hạ tầng vận hành.
2. Thiết kế representation và token budget cho Hướng B nếu muốn sử dụng API sinh context tìm kiếm mà không gây tràn trần 256 tokens của HuyDang.
3. Quy chuẩn kỹ thuật xử lý bảng biểu và điều kiện câu dẫn thời gian trên toàn bộ các tài liệu còn lại của corpus.

---

## 2. BẢNG SO SÁNH 3 PIPELINE THAM KHẢO

| Tiêu chí | `llm_rag` (Production Tiếng Việt) | `rag_old_0/implementation` (Basic LangChain) | `rag_old_0/pro_implementation` (Advanced Native) |
| :--- | :--- | :--- | :--- |
| **Định dạng dữ liệu đầu vào** | JSON records có cấu trúc domain nghiệp vụ rõ ràng (`backend/data/processed/projects.json`, `companyInfo.json`). | File Markdown thô (`.md`) trong `knowledge-base/` (văn bản Insurellm). | File Markdown thô (`.md`) trong `knowledge-base/` (văn bản Insurellm). |
| **Cách xác định ranh giới chunk** | Phân tách theo Semantic Fields của JSON (overview, description, style, specs). Trường text dài dùng `split_paragraphs(max_len=400)` cắt theo dấu câu `. ` và cắt cứng 400 ký tự nếu câu quá dài. Không overlap ký tự. | Phân đoạn theo cửa sổ ký tự cố định: `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""])`. | Phân đoạn bằng LLM: Prompt gửi toàn bộ text của file tới `openai/gpt-4.1-nano`, yêu cầu tự chia thành các chunk có overlap ~25% (~50 từ), ép schema Pydantic `Chunks`. |
| **Biểu diễn đưa vào Vector Search** | Chuỗi template ghép các trường: `"Dự án {name}."` hoặc `"Mô tả dự án {name}: {part}"`. | Nguyên văn chuỗi ký tự cắt từ splitter. | Ghép 3 trường do LLM sinh: `headline + "\n\n" + summary + "\n\n" + original_text`. |
| **Cơ chế neo ngữ cảnh (Contextualization)** | Tiền định bằng code Python: Chèn tên thực thể vào đầu chuỗi (`"Dự án " + name + ". "`). | Không có. Chunk bị tách rời khỏi tiêu đề tài liệu. | LLM sinh `headline` và `summary` (1–2 câu tóm tắt) đứng trước đoạn văn bản gốc. |
| **Bảo toàn bằng chứng (Evidence Preservation)** | Không lưu offset span hoặc exact match validation. Dựa vào tính súc tích của trường dữ liệu. | Chuỗi ký tự giữ nguyên văn bản gốc trong phạm vi cắt, nhưng mất cấu trúc bảng biểu và phân cấp. | Rủi ro đột biến: Prompt yêu cầu trích `original_text` "exactly as is", nhưng **hoàn toàn không có mã nguồn kiểm tra exact match** so với file gốc. |
| **Mô hình Vector & Cơ sở dữ liệu** | Sentence-transformers local tiếng Việt / đa ngữ, lưu Qdrant vector DB. Payload chứa `chunk_id`, `chunk_type`, `priority`, `source`. | `all-MiniLM-L6-v2` (384 chiều), lưu ChromaDB (`preprocessed_db`). Metadata: `source`, `doc_type`. | `text-embedding-3-large` (3072 chiều), lưu ChromaDB (`preprocessed_db`). Metadata: `source`, `type`. |
| **Quy trình Retrieval & Rerank** | Vector search trên Qdrant với payload filtering, lấy top 5 chunks (giới hạn context ≤ 3000 ký tự). Không rerank. | Vector search `as_retriever(k=5)`. Không rewrite, không rerank. | - LLM Rewrite: `openai/gpt-5-nano` viết lại câu hỏi.<br>- Dual retrieval: Query bằng câu hỏi gốc (k=20) và câu hỏi rewrite (k=20), merge và deduplicate (tối đa 40 candidates).<br>- LLM List-wise Rerank: `openai/gpt-5-nano` sắp xếp lại 40 candidates, chọn top 10 đưa vào generator (`openai/gpt-5-nano`). |
| **Chi phí API bước Chunking** | **0 USD**, hoàn toàn local, chạy tiền định (deterministic). | **0 USD**, hoàn toàn local, chạy tiền định (deterministic). | **Phát sinh chi phí API** gọi `gpt-4.1-nano` cho từng tài liệu; kết quả phụ thuộc phản hồi của API (non-deterministic). |
| **Source pointers thực tế** | - `backend/ingestion/chunking/projects.py:13-96`<br>- `backend/ingestion/helpers/split_paragraphs.py:5-45`<br>- `backend/ingestion/helpers/make_metadata.py:1-25` | - `implementation/ingest.py:27-35`<br>- `implementation/answer.py:18-28` | - `pro_implementation/ingest.py:14, 34-55, 72-109`<br>- `pro_implementation/answer.py:12, 47-75, 89-108, 128-135` |

---

## 3. MINH HỌA INPUT → CHUNK/SEARCH TEXT → EVIDENCE TỪ DỮ LIỆU THỰC TẾ

### 3.1. Dữ liệu thực tế từ `llm_rag`
- **Bản ghi thực tế (Trích từ `backend/data/processed/projects.json`, Record ID: 46):**
  ```json
  {
    "id": 46,
    "title": "Homestay Nhơn Hải 14,3 x 12m. Địa điểm: Nhơn Hải, Quy Nhơn. Mức đầu tư: 4.8 tỷ",
    "location": "Nhơn Hải, Quy Nhơn",
    "description": "Nguyen Minh Khang thiết kế & thi công biệt thự mini 9x15m tại Tân Phú, diện tích 135m², tổng chi phí 4.8 tỷ. Kiến trúc hiện đại ấm cúng, sân vườn nhỏ, hoàn thiện 7.5 tháng."
  }
  ```
- **Xử lý Chunking thực tế trong `chunking/projects.py` (Mã nguồn thực tế):**
  ```python
  # Overview chunk (dòng 80-84)
  if project_name:
      chunks.append({
          "text": f"Dự án {project_name}.",
          "metadata": make_metadata(base_metadata, chunk_type="overview", priority=1)
      })

  # Description chunk qua split_paragraphs (dòng 87-96)
  for i, part in enumerate(split_paragraphs(project_description)):
      chunks.append({
          "text": f"Mô tả dự án {project_name}: {part}",
          "metadata": make_metadata(base_metadata, chunk_type="description", priority=2, part_index=i)
      })
  ```
- **Search Text thực tế đưa vào Qdrant:**
  - Chunk overview: `"Dự án Homestay Nhơn Hải 14,3 x 12m. Địa điểm: Nhơn Hải, Quy Nhơn. Mức đầu tư: 4.8 tỷ."`
  - Chunk description: `"Mô tả dự án Homestay Nhơn Hải 14,3 x 12m. Địa điểm: Nhơn Hải, Quy Nhơn. Mức đầu tư: 4.8 tỷ: Nguyen Minh Khang thiết kế & thi công biệt thự mini 9x15m tại Tân Phú, diện tích 135m², tổng chi phí 4.8 tỷ. Kiến trúc hiện đại ấm cúng, sân vườn nhỏ, hoàn thiện 7.5 tháng."`
- **Đặc điểm Evidence:** Dữ liệu ngắn gọn và có tiền tố thực thể rõ ràng. Tuy nhiên, hệ thống không lưu span offset trong file nguồn và không có cơ chế đối chiếu exact match.

### 3.2. Dữ liệu thực tế từ `rag_old_0/implementation`
- **Văn bản thực tế (Trích từ `knowledge-base/products/Carllm.md`, dòng 25–41):**
  ```markdown
  ## Pricing

  Carllm is offered under a subscription-based pricing model tailored to meet the needs of insurance companies of all sizes. Our pricing tiers are designed to provide maximum flexibility and value:

  - **Basic Tier**: $1,000/month
    - Ideal for small insurance firms.
    - Access to core features and standard reporting.

  - **Professional Tier**: $2,500/month
    - For medium-sized companies.
    - All Basic Tier features plus advanced analytics and fraud detection.

  - **Enterprise Tier**: $5,000/month
    - Customized solutions for large insurance firms.
    - Comprehensive support, full feature access, and integration with existing systems.
  ```
- **Cơ chế cắt ký tự của `implementation/ingest.py`:**
  - Dùng `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`.
  - Nếu file markdown vượt quá 1000 ký tự, điểm ngắt sẽ ưu tiên tại `\n\n`. Đoạn danh sách giá trên có thể bị tách rời khỏi tiêu đề gốc `# Product Summary \n # Carllm` nếu nằm ở nửa sau tài liệu, khiến search text không có tên sản phẩm nếu người dùng tìm kiếm cụm từ chung.

### 3.3. Dữ liệu thực tế từ `rag_old_0/pro_implementation`
- **Cấu trúc Ingestion (`pro_implementation/ingest.py`):**
  - Prompt yêu cầu `openai/gpt-4.1-nano` chia tài liệu thành danh sách Pydantic `Chunks`:
    ```python
    class Chunk(BaseModel):
        headline: str
        summary: str
        original_text: str
    ```
  - Search text được tạo bằng: `f"{chunk.headline}\n\n{chunk.summary}\n\n{chunk.original_text}"`.
- **Ghi nhận về dữ liệu thực tế:** Trong repo `rag_old_0`, cơ sở dữ liệu `preprocessed_db` đã được nạp sẵn dưới dạng vector binary của ChromaDB, không lưu kèm raw JSON log của các cuộc gọi API `gpt-4.1-nano`. Do đó, nội dung chi tiết của `headline` và `summary` cho từng file cụ thể là **chưa được xác minh qua bản ghi log trung gian**.
- **Đặc điểm Evidence:** Mã nguồn không chứa bất kỳ assertion nào để đảm bảo chuỗi trong `original_text` trùng khớp 100% ký tự với văn bản đầu vào `document["text"]`.

### 3.4. Dữ liệu thực tế từ Khảo sát Huế (Mẫu Ca Huế Lượt 3)
Dữ liệu được lấy nguyên văn từ tệp kết quả khảo sát: [reports/artifacts/full_corpus_chunk_samples_2026_09_09.json](file:///home/minhhieu/hue_rag/reports/artifacts/full_corpus_chunk_samples_2026_09_09.json).

- **Tài liệu nguồn:** `knowledge-base-hue/travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`
- **Tiêu đề tài liệu:** `Vé biểu diễn nghệ thuật và trải nghiệm sông Hương`
- **Heading path:**
  1. `2. Ca Huế trên sông Hương và dịch vụ thuyền rồng`
  2. `2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế`
  3. `A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)`

#### Mẫu Chunk ID: `ca_hue_p3b_lead_chunk_2` (Trẻ em Lá Quê Travel)
- **evidence_parts (Exact match span trên file gốc):**
  1. `survey_lead_2_3` (span: `[10409, 10591]`, 182 ký tự):  
     `"Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu (Thuyền Rồng Huế, Ca Huế Trên Sông Hương - Lá Quê Travel, Đại Việt Tourist) tại thời điểm tháng 09/2026:"`
  2. `table_header` (span: `[10760, 10900]`, 140 ký tự):  
     `"| Hạng mục đối tượng | Mức giá niêm yết khảo sát | Đơn vị tính | Thành phần bao gồm | Ghi chú & Điều kiện áp dụng |\n|---|---:|:---:|---|---|"`
  3. `child_row_la_que` (span: `[11318, 11581]`, 263 ký tự):  
     `"| **Trẻ em (theo chiều cao)** | Miễn phí (< 1.0m)<br>70.000 – 100.000 (1.0m – < 1.3m)<br>Tính như người lớn (≥ 1.3m) | đồng/trẻ/suất | Dịch vụ tương đương người lớn theo phân khúc | Tiêu chuẩn chiều cao quy định bởi đơn vị Lá Quê Travel (cahuetrensonghuong.com) |"`
  4. `condition_exclusions` (span: `[12117, 12287]`, 170 ký tự):  
     `"- **Không bao gồm:** Phương tiện đưa đón tận nơi (khách tự di chuyển đến Bến Tòa Khâm), ăn uống cá nhân trên thuyền, tiền tip bồi dưỡng nghệ sĩ (không bắt buộc, tùy tâm)."`
- **Search Text thực tế:**
  ```text
  Vé biểu diễn nghệ thuật và trải nghiệm sông Hương
  2. Ca Huế trên sông Hương và dịch vụ thuyền rồng > 2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế > A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)
  Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu (Thuyền Rồng Huế, Ca Huế Trên Sông Hương - Lá Quê Travel, Đại Việt Tourist) tại thời điểm tháng 09/2026:

  | Hạng mục đối tượng | Mức giá niêm yết khảo sát | Đơn vị tính | Thành phần bao gồm | Ghi chú & Điều kiện áp dụng |
  |---|---:|:---:|---|---|
  | **Trẻ em (theo chiều cao)** | Miễn phí (< 1.0m)<br>70.000 – 100.000 (1.0m – < 1.3m)<br>Tính như người lớn (≥ 1.3m) | đồng/trẻ/suất | Dịch vụ tương đương người lớn theo phân khúc | Tiêu chuẩn chiều cao quy định bởi đơn vị Lá Quê Travel (cahuetrensonghuong.com) |

  - **Không bao gồm:** Phương tiện đưa đón tận nơi (khách tự di chuyển đến Bến Tòa Khâm), ăn uống cá nhân trên thuyền, tiền tip bồi dưỡng nghệ sĩ (không bắt buộc, tùy tâm).
  ```
- **Số đo độ dài thực tế (Tokens):**
  - `CODE4LIFEOFFICIAL--huydang-dek21-embedding`: **248 / 256 tokens** (chỉ còn trống 8 tokens).
  - `multilingual-e5-small`: **311 / 512 tokens**.
  - `cross-encoder--ms-marco-MiniLM-L-6-v2` với `query_orig`: **437 / 512 tokens**.
  - `cross-encoder--ms-marco-MiniLM-L-6-v2` với `query_long`: **479 / 512 tokens** (còn trống 33 tokens).
- **Queries chuẩn hóa tương ứng:**
  - `query_orig`: `"Vé Ca Huế cho trẻ em được tính như thế nào?"`
  - `query_long`: `"Giá vé xem Ca Huế ghép thuyền trên sông Hương cho người lớn và trẻ em bao nhiêu tiền một người, áp dụng điều kiện bao gồm và không bao gồm những dịch vụ gì?"`

#### Mẫu Chunk ID: `ca_hue_p3b_lead_chunk_3` (Trẻ em Thuyền Rồng Huế)
- **evidence_parts:** Câu dẫn 2.3 (`[10409, 10591]`) + Table Header (`[10760, 10900]`) + Row Thuyền Rồng (`[11582, 11810]`, 228 ký tự) + Không bao gồm (`[12117, 12287]`).
- **Số đo độ dài thực tế (Tokens):**
  - `huydang`: **245 / 256 tokens** (còn trống 11 tokens).
  - `e5_small`: **302 / 512 tokens**.
  - `minilm_orig`: **417 / 512 tokens**.
  - `minilm_long`: **459 / 512 tokens**.

---

## 4. ĐỐI CHIẾU NỘI DUNG PHIÊN ÂM BÀI HỌC (`rag_old_0/phien_am_bai_hoc`)

### 4.1. Vị trí nguồn và bản chất tài liệu
Nội dung phân tích được đối chiếu trực tiếp từ tệp văn bản:
`/home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day5.txt`
- **Bài 128 (dòng 1–62):** *"Day 5 - Chunking: Beyond Character Splitting"*. Giới thiệu cách dùng Pydantic schema ép kiểu đầu ra LLM (`headline`, `summary`, `original_text`). Giảng viên lý giải việc bổ sung `headline` và `summary` giúp embedding bao quát được cả ý chính lẫn chi tiết.
- **Bài 129 (dòng 63–140):** *"Day 5 - Advanced Chunking: Tables & Comparison"*. Nêu khó khăn khi phân đoạn các bảng biểu bằng parser thông thường và gợi ý dùng LLM đọc bảng.
- **Bài 131 (dòng 230–310):** *"Day 5 - Re-ranking: The Power of Second Opinions"*. Giải thích vai trò của Reranker trong việc lọc lại pool ứng viên lớn từ retrieval thô.
- **Bài 132 (dòng 311–390):** *"Day 5 - Query Rewriting"*. Giải thích kỹ thuật viết lại câu hỏi để tối ưu hóa truy vấn vector.
- **Bài 135 (dòng 596–660):** *"135. Day 5 - Advanced RAG Evaluation: From 0.73 to 0.91 MRR with GPT-4o"*.

*Lưu ý về bản chất tài liệu:* Tệp `day5.txt` là bản ghi chép/tổng hợp nội dung bài giảng của khóa học, ghi nhận lại các kết quả mà giảng viên đã thực hiện trong bài giảng, không phải là tệp log chạy benchmark tự động hay kết quả kiểm chứng độc lập trong phiên làm việc này.

### 4.2. Phân tích kết quả cải tiến chỉ số trong Bài 135
Trong mục *"3. Hành trình cải tiến con số (Metric Journey)"* (dòng 612–616 của `day5.txt`), tiến trình đo lường được ghi nhận qua 3 giai đoạn:
1. **Giai đoạn 1 (Baseline):** Basic RAG đạt MRR ~0.73, Answer Accuracy ~3.99/5.
2. **Giai đoạn 2 (Thay đổi Embedding & Chunk size):** *"Đổi sang Embedding lớn và Chunk size tối ưu, MRR ~0.79, Accuracy ~4.21."*
3. **Giai đoạn 3 (Bản Pro hoàn chỉnh):** *"Advanced RAG (Pro), MRR 0.91 (chính xác 0.9116), Accuracy 4.62."*

#### Bóc tách các biến số kỹ thuật:
- **Tại Giai đoạn 2:** Hệ thống **thay đổi đồng thời 2 biến số**: mô hình embedding (chuyển sang `text-embedding-3-large`) và kích thước chunk. Mức tăng +0.06 MRR (từ 0.73 lên 0.79) là kết quả chung của cả 2 thay đổi, không thể quy riêng cho một mình mô hình embedding.
- **Tại Giai đoạn 3:** Hệ thống **thay đổi đồng thời nhiều biến số mới**:
  1. Chuyển sang LLM Semantic Chunking (có `headline` và `summary`).
  2. Bổ sung Query Rewriting (`rewrite_query`).
  3. Mở rộng Retrieval Pool: thực hiện Dual Retrieval (truy vấn cả câu hỏi gốc lẫn câu hỏi viết lại, lấy `k=20` mỗi luồng, tổng gộp tối đa 40 candidates).
  4. Bổ sung LLM List-wise Reranker: dùng `openai/gpt-5-nano` sắp xếp lại 40 candidates và lọc lấy top 10 đưa vào generator.
- **Kết luận khách quan:** Trong tài liệu không có bất kỳ thử nghiệm bóc tách riêng lẻ nào (ablation study) đo đạc hiệu quả độc lập của riêng bước semantic chunking khi giữ nguyên các thành phần còn lại. Mọi phỏng đoán quy kết tỷ lệ phần trăm đóng góp cụ thể của semantic chunking (như phỏng đoán "hơn 80%" ở các thảo luận trước) là **suy diễn không có căn cứ dữ liệu** và cần được loại bỏ hoàn toàn.

---

## 5. ĐỐI CHIẾU NGHIÊN CỨU CHÍNH THỨC VÀ CHUẨN CÔNG NGHIỆP

### 5.1. Nghiên cứu thực nghiệm NAACL 2025
- **Tài liệu:** Renyi Qu, Ruixuan Tu, Forrest Sheng Bao. *"Is Semantic Chunking Worth the Computational Cost?"*. *Findings of the Association for Computational Linguistics: NAACL 2025*, pages 2155–2177, Albuquerque, New Mexico (April 2025). URL: `https://aclanthology.org/2025.findings-naacl.114/`.
- **Phương pháp khảo sát của bài báo:**
  - Khảo sát phương pháp semantic chunking truyền thống: tính cosine distance giữa embedding vector của các câu liên tiếp để xác định ranh giới chuyển đổi ngữ nghĩa dựa trên ngưỡng (threshold/percentile).
  - Đánh giá có hệ thống trên 3 tác vụ: Document retrieval, Evidence retrieval, và Retrieval-based answer generation.
- **Kết quả và kết luận thực nghiệm của bài báo:**
  - Tác giả kết luận: Chi phí tính toán tăng thêm trong giai đoạn tiền xử lý (do phải gọi embedding cho từng câu) **không mang lại sự cải thiện hiệu năng ổn định và nhất quán** so với fixed-size chunking khi kích thước chunk và overlap được chọn hợp lý.
  - Các mô hình tạo sinh hiện đại có khả năng bù đắp các khiếm khuyết nhỏ về ranh giới chunk.
- **Lưu ý hiệu chỉnh attribution:** Bài báo NAACL 2025 **không đưa ra khuyến nghị cụ thể** về việc "phải kết hợp structural chunking với context enrichment và hybrid retrieval". Khuyến nghị này là phân tích tổng hợp của kỹ sư khi đối chiếu thêm với tài liệu Docling và Anthropic, không được trích dẫn như là kết luận trực tiếp của bài báo NAACL.
- **Phân biệt 3 khái niệm ranh giới ngữ nghĩa:**
  1. *Semantic chunking bằng khoảng cách vector câu:* Tính toán embedding giữa các câu để tìm điểm ngắt (đối tượng nghiên cứu của NAACL 2025).
  2. *LLM xác định ranh giới chunk:* Giao toàn bộ văn bản cho LLM tự quyết định điểm cắt (cách làm của `rag_old_0/pro_implementation`).
  3. *LLM bổ sung ngữ cảnh:* Giữ nguyên ranh giới văn bản có sẵn, chỉ dùng LLM tạo chuỗi tóm tắt ngữ cảnh đặt vào đầu chunk (cách làm của Anthropic).

### 5.2. Công bố Anthropic Contextual Retrieval (2024)
- **Phương pháp luận:** Anthropic đề xuất giải pháp giữ nguyên các ranh giới chunk có sẵn (không dùng LLM chia lại tài liệu), sau đó dùng mô hình Claude Haiku để sinh một đoạn văn bản ngắn (khoảng 50–100 tokens theo tokenizer của Claude) giải thích vị trí và ngữ cảnh của chunk trong toàn bộ tài liệu, rồi ghép vào đầu chunk trước khi embedding.
- **Lưu ý kỹ thuật:**
  1. *Khác biệt về ranh giới:* Anthropic **không chia lại cấu trúc tài liệu bằng LLM** như cách làm của `rag_old_0/pro_implementation`.
  2. *Không đồng nhất về Tokenizer:* Độ dài "50–100 tokens" được Anthropic tính toán theo tokenizer của Claude (họ BPE cho tiếng Anh). Không thể quy đổi cơ học số lượng này thành một số lượng token cố định trên tokenizer của mô hình khác như `huydang-dek21-embedding` (vốn sử dụng SentencePiece / BPE tối ưu hóa cho tiếng Việt).
  3. *Phạm vi áp dụng:* Kết quả giảm tỷ lệ lỗi truy xuất (35%–67%) được Anthropic công bố trên tập dữ liệu benchmark nội bộ của họ. Đây là tài liệu tham khảo về mặt phương pháp, **không phải là bằng chứng bảo đảm chất lượng truy xuất cho corpus tiếng Việt của Huế RAG**.

### 5.3. Kiến trúc Docling Chunking (IBM, 2024–2026)
- **Nguyên lý:** Phân đoạn dựa trên cấu trúc tài liệu (`HybridChunker`).
- Parser nhận diện các thành phần cấu trúc: tiêu đề phân cấp, bảng biểu, danh sách, đoạn văn.
- Sử dụng trực tiếp tokenizer của mô hình embedding đích để kiểm soát kích thước: gộp các đơn vị nhỏ nằm cùng cấp (`merge_peers=True`), lặp lại header cho các hàng của bảng (`repeat_table_header=True`).
- Tách biệt rõ giữa nội dung gốc sạch của chunk (`chunk.text`) và chuỗi văn bản được bổ trợ ngữ cảnh dùng cho vector search (`chunk.contextualize()`).

### 5.4. LangChain `MarkdownHeaderTextSplitter`
- Tách văn bản dựa trên các cấp độ header Markdown (`#`, `##`, `###`), chuyển tiêu đề vào metadata của Document.
- Hạn chế: Không nhận biết độ dài token của mô hình embedding. Nếu một section chứa văn bản dài hoặc bảng biểu lớn, người dùng phải tự xử lý cắt tiếp, dễ dẫn đến phá vỡ cấu trúc bảng.

---

## 6. MA TRẬN PHÂN TÍCH 3 HƯỚNG KIẾN TRÚC CHO HUẾ RAG

Dựa trên các quyết định đã được định hình giữa Reviewer và User, dưới đây là phân tích chi tiết 3 hướng kiến trúc chunking:

### 6.1. Hướng A: Cấu trúc Markdown tiền định + Kiểm soát Tokenizer Local (Deterministic Structural)
- **Định nghĩa:** Phân đoạn tài liệu hoàn toàn dựa trên cấu trúc cú pháp Markdown (H2, H3, hàng/nhóm hàng bảng biểu, danh sách). Không sử dụng LLM để chia chunk hay sinh văn bản. Độ dài chunk được kiểm soát chặt chẽ bằng chính tokenizer local (`huydang` và `minilm`).
- **Ưu điểm kỹ thuật:**
  - **Không phát sinh chi phí API** trong pha ingestion.
  - **Bảo toàn nguyên vẹn bằng chứng:** `evidence_parts` khớp 100% từng ký tự và vị trí span trong file nguồn `.md`.
  - **Kiểm soát chính xác giới hạn token:** Đảm bảo không vượt quá trần 256 tokens của HuyDang trên các mẫu đã được đo đạc.
- **Ràng buộc và đánh đổi:**
  - Đòi hỏi phải xây dựng và tinh chỉnh các bộ quy tắc parser riêng cho từng cấu trúc văn bản đặc thù (như bảng giá vé, bảng so sánh tuyến tham quan).
  - *Lưu ý:* Việc bảo vệ nguyên vẹn ký tự (exact match) chỉ chứng minh tính trung thực của văn bản trích xuất, không bảo đảm rằng đoạn trích đã tự mang đầy đủ ngữ nghĩa độc lập hoặc mô hình tạo sinh (generator) sẽ không mắc lỗi ảo giác khi trả lời.

### 6.2. Hướng B: Giữ nguyên Ranh giới Cấu trúc A + Dùng API sinh Ngữ cảnh Tìm kiếm Riêng
- **Định nghĩa:** Kế thừa toàn bộ ranh giới chunk và `evidence_parts` từ Hướng A để bảo toàn bằng chứng gốc. Sử dụng LLM API (như OpenAI hoặc Gemini) để tạo thêm một chuỗi ngữ cảnh tìm kiếm riêng biệt bổ trợ cho việc truy xuất.
- **Hiện trạng đo lường và ràng buộc mở:**
  - Thử nghiệm trên mẫu bảng vé Ca Huế (P3B) cho thấy các chunk giá vé chi tiết kèm câu dẫn đã chiếm tới **245–248 tokens HuyDang**.
  - Nếu áp dụng cách nối chuỗi ngữ cảnh do LLM sinh trực tiếp vào đầu chunk (như cách làm của Anthropic hay `rag_old_0`), chunk sẽ lập tức vượt trần 256 tokens của HuyDang và bị cắt cụt (truncation).
  - **Ràng buộc thiết kế:** Hướng B không bị loại bỏ hoàn toàn, nhưng **bắt buộc phải có thiết kế kiến trúc riêng** về biểu diễn tìm kiếm (representation) và ngân sách token:
    + Ví dụ: Tạo vector riêng cho context prefix, hoặc chỉ áp dụng context sinh bởi LLM cho các chunk ngắn có ngân sách dư dả, hoặc sử dụng mô hình embedding có context window lớn hơn 256 tokens.
  - Việc thay đổi mô hình embedding, ranh giới chunk hoặc ngân sách token sẽ làm thay đổi bản chất các phép so sánh trước đây và cần Reviewer xem xét, quyết định.

### 6.3. Hướng C: LLM hỗ trợ xác định Ranh giới Chunk khi Hướng A/B gặp trở ngại
- **Định nghĩa:** Sử dụng LLM để hỗ trợ xác định ranh giới chunk **chỉ khi có lý do kỹ thuật rõ ràng** từ Hướng A hoặc B (ví dụ: các tài liệu phi cấu trúc phức tạp, các đoạn văn dài đan xen nhiều chủ đề mà quy tắc phân đoạn Markdown không thể xử lý hợp lý).
- **Hiện trạng tại Huế RAG:** Phần lớn tài liệu trong `knowledge-base-hue/` (di tích, vé, văn hóa, ẩm thực) đã được chuẩn hóa với hệ thống tiêu đề Markdown (H1, H2, H3), danh sách bullet points và bảng biểu rõ ràng. Do đó, nhu cầu sử dụng LLM để phân đoạn tự do là chưa cấp thiết ở giai đoạn hiện tại.

---

### 6.4. Đề xuất Mới (Chưa được phê duyệt): Bổ sung Metadata Ngoại tuyến (Offline Synthetic Metadata)
Trong quá trình khảo sát, Implementer ghi nhận thêm một hướng mở rộng kỹ thuật: Sử dụng LLM (chạy batch ngoại tuyến 1 lần) để sinh thêm metadata hỗ trợ tìm kiếm cho từng chunk (như các câu hỏi giả định `hypothetical_questions` hoặc các từ khóa thực thể `domain_tags`).
- **Tình trạng:** Đây là **đề xuất kỹ thuật mới từ Implementer, chưa được Reviewer hay User phê duyệt**.
- **Yêu cầu về Consumer:** Cần lưu ý rằng việc chỉ lưu thêm các trường metadata này vào payload của Qdrant sẽ **không mang lại bất kỳ cải thiện nào cho vector search hiện tại** nếu không có thành phần sử dụng (consumer) tương ứng:
  - Phải có bộ tìm kiếm từ khóa (BM25 / Sparse search) lập chỉ mục trên các câu hỏi giả định.
  - Hoặc phải chạy vector embedding riêng cho từng câu hỏi giả định.
- Do đó, đề xuất này cần được xem xét riêng biệt trong workstream thiết kế retrieval, không đưa vào làm yêu cầu bắt buộc của bước chunking hiện tại.

---

### 6.5. Bảng So sánh Tổng hợp 3 Hướng (A, B, C)

| Tiêu chí so sánh | Hướng A: Cấu trúc Tiền định | Hướng B: Cấu trúc A + API Context riêng | Hướng C: LLM hỗ trợ Ranh giới |
| :--- | :--- | :--- | :--- |
| **Kiểm soát trần HuyDang (256 tokens)** | **Đã đo đạc an toàn** trên các mẫu khảo sát (giữ dưới 250 tokens). | **Cần thiết kế lại representation/budget** vì chunk bảng biểu đã đạt 248 tokens. | **Khó kiểm soát tiền định**; độ dài chunk do LLM sinh có thể biến thiên. |
| **Kiểm soát trần MiniLM (512 tokens)** | Mẫu dài nhất đạt **479 tokens** với câu hỏi dài (còn trống 33 tokens). | Nguy cơ vượt trần cao nếu ghép thêm context dài và query mở rộng. | Nguy cơ biến thiên theo độ dài do LLM quyết định. |
| **Bảo toàn bằng chứng & Đối soát** | **100% nguyên vẹn ký tự**, span offset khớp trực tiếp với file nguồn. | **100% nguyên vẹn ký tự** cho phần thân văn bản trích xuất. | Khó đối soát exact match nếu LLM tự trích đoạn văn bản. |
| **Xử lý Bảng vé & Câu dẫn thời gian** | Lặp lại header bảng và câu dẫn thời điểm 09/2026 bằng code tiền định. | Kế thừa cơ chế lặp của Hướng A; context bổ trợ xử lý riêng. | Phụ thuộc vào chất lượng trích xuất và hiểu bảng của prompt LLM. |
| **Chi phí API bước Ingestion** | **0 USD**, hoàn toàn local. | **Phát sinh phí API** sinh context cho các chunk tài liệu. | **Phát sinh phí API** phân đoạn cho các tài liệu được chỉ định. |
| **Tính tiền định (Reproducibility)** | **100% tiền định**, cùng mã nguồn luôn cho ra đúng các chunk giống nhau. | Không tiền định ở phần context do API sinh ra. | Không tiền định trong việc xác định điểm cắt văn bản. |
| **Tác động tới mã nguồn hiện tại** | Kế thừa và mở rộng parser cấu trúc hiện có tại `backend/ingestion/chunking/markdown_chunker.py`. | Cần bổ sung client API và thiết kế lại trường payload / vector storage. | Cần thay đổi hoàn toàn kiến trúc nạp dữ liệu. |

---

## 7. CÁC ĐIỂM ĐỀ XUẤT REVIEWER VÀ USER THẢO LUẬN

Để chuẩn bị cho phiên chốt thiết kế full-corpus, đề xuất Reviewer và User tập trung thảo luận các câu hỏi trọng tâm:

1. **Lựa chọn hướng kiến trúc nền tảng cho giai đoạn hiện tại:**
   - Đánh giá tính khả thi của **Hướng A** như là baseline an toàn nhất về chi phí (0 USD), tính tiền định và khả năng kiểm soát trần token 256 của HuyDang.
   - Thảo luận xem có cần thiết lập thử nghiệm riêng cho **Hướng B** hay không, và nếu có thì giải quyết bài toán biểu diễn context và ngân sách token như thế nào.

2. **Quy chuẩn kỹ thuật gắn nhãn phân cấp (Heading Labels):**
   - Thống nhất cấu trúc chuỗi nhãn phân cấp: Áp dụng đầy đủ `Document Title > H2 > H3` cho mọi chunk hay có phương án rút gọn đối với các bảng biểu đã chiếm dung lượng token lớn?

3. **Chính sách phân đoạn bảng biểu và câu dẫn điều kiện:**
   - Đối với các bảng dịch vụ phụ thuộc vào câu dẫn (như bảng giá vé Ca Huế gắn với câu dẫn thời điểm khảo sát tháng 09/2026): Thống nhất việc parser tự động gắn câu dẫn vào tất cả các chunk của bảng.
   - *Lưu ý:* Việc chia bảng theo nhóm 1–2 hàng hay áp dụng ngưỡng cứng dưới 250 tokens hiện là quan sát thực nghiệm trên mẫu khảo sát, **chưa phải là chính sách chính thức**; cần Reviewer và User xem xét phê duyệt.

4. **Tách biệt workstream Retrieval & Reranker:**
   - Các đề xuất về mở rộng candidate pool (từ top 5 lên top 20–30) hoặc sử dụng LLM Reranker (rút ra từ bài học `rag_old_0`) được ghi nhận như các hướng tối ưu hóa retrieval tiềm năng, nhưng **được chuyển giao cho workstream retrieval chuyên biệt** xem xét sau khi thiết kế chunking được hoàn tất.

---

## 8. GIỚI HẠN KHẢO SÁT VÀ TỆP BÀN GIAO

- **Giới hạn khảo sát:** Báo cáo này thuần túy đối chiếu tài liệu kỹ thuật, mã nguồn tham khảo và các số đo tokenizer trên mẫu khảo sát Lượt 3; không thay thế cho các quyết định thiết kế hoặc kết quả benchmark retrieval toàn corpus.
- **Cam kết bảo toàn hệ thống:**
  - Không sửa đổi mã nguồn trong `backend/` hay `knowledge-base-hue/`.
  - Không thay đổi các tệp `specs/`, `plans/`, hay `guides/`.
  - Không phát sinh API calls hay thay đổi dữ liệu trên Qdrant.
  - Snapshot Git của repository được giữ nguyên trạng.
- **Tệp tài liệu hiệu chỉnh duy nhất bàn giao:**
  - [reports/full_corpus_chunking_reference_research_2026_09_09.md](file:///home/minhhieu/hue_rag/reports/full_corpus_chunking_reference_research_2026_09_09.md)
