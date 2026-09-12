# Báo cáo tổng hợp Reference: Thiết kế Golden Dataset và Đánh giá RAG (rag_old_0 & rag_old)

Implementer: Implementer  
Date: 2026-09-09  
Canonical contract: `handoff_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md`  
Base commit: `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`  
Head commit: worktree  
Risk level: low (đọc/tổng hợp reference, không chạy code)  
Git authorization: none  

---

## 1. Tóm tắt điều hành (Executive Summary)

Báo cáo này thực hiện khảo sát có mục tiêu về phương pháp xây dựng Golden Dataset và khung đánh giá RAG trong phạm vi các tài liệu khóa học và kho mã nguồn tham khảo được người dùng cung cấp (`/home/minhhieu/llm_rag/tai_lieu/rag_old_0` và `/home/minhhieu/llm_rag/tai_lieu/rag_old`), phân biệt rành mạch giữa **Nội dung bài học/tổng hợp**, **Hành vi code thực tế**, **Kết quả lưu sẵn** và **Nhận xét/Đề xuất cho Huế**.

### 1.1. Những bài học cốt lõi học được từ Reference
1. **Triết lý "Sao Bắc Đẩu" (North Star) & Tách biệt 2 trụ cột:** Đánh giá RAG chuyển từ "nghệ thuật thử-sai cảm tính" sang "khoa học định lượng" bằng cách đo lường độc lập hai khâu: Truy xuất (**Retrieval**) và Trả lời (**Answer/Generation**). Nếu không có số liệu định lượng, việc tinh chỉnh hệ thống sẽ rơi vào cái bẫy "đập chuột chũi" (whack-a-mole: sửa lỗi này làm hỏng phần khác).
2. **Cấu trúc hóa tập test & Phân loại câu hỏi (Categorical Breakdown):** Bộ test 150 câu được quản lý bằng JSONL (`tests.jsonl`) và validate qua Pydantic (`TestQuestion`). Điểm số không chỉ nhìn ở giá trị trung bình tổng thể mà bắt buộc phải phân rã theo 7 danh mục: `direct_fact` (70), `temporal` (20), `spanning` (20), `comparative` (10), `numerical` (10), `relationship` (10), `holistic` (10). Các nhóm câu hỏi phức tạp (`spanning`, `holistic`, `relationship`) chính là nơi bộc lộ rõ nhất các điểm yếu kiến trúc của Basic RAG.
3. **LLM-as-a-judge với Structured Outputs:** Đánh giá câu trả lời sử dụng mô hình LLM làm giám khảo (`gpt-4.1-nano` hoặc `gpt-5-nano`) chấm trên thang điểm 1–5 theo 3 tiêu chí: Độ chính xác (`accuracy`), Độ đầy đủ (`completeness`), Mức độ liên quan (`relevance`), đồng thời ép trả về JSON có cấu trúc qua Pydantic (`AnswerEval`) để tổng hợp tự động và hiển thị Dashboard Gradio.
4. **Mã màu trực quan hóa trên Dashboard (Tham khảo):** Dashboard Gradio của khóa học thiết lập các ngưỡng màu hiển thị trực quan: Retrieval (MRR/nDCG $\ge 0.9$ Xanh, $\ge 0.75$ Vàng, $< 0.75$ Đỏ; Coverage $\ge 90\%$ Xanh, $\ge 75\%$ Vàng, $< 75\%$ Đỏ); Answer (Điểm $\ge 4.5$ Xanh, $\ge 4.0$ Vàng, $< 4.0$ Đỏ). Đây là công cụ trực quan hóa cho bài toán InsureLLM, không phải ngưỡng nghiệm thu định trước cho Huế.

### 1.2. Hạn chế và rủi ro cốt lõi ảnh hưởng trực tiếp đến thiết kế Huế
1. **Gán Evidence hoàn toàn bằng `keywords` (Không có Chunk ID / Span / Source Path):**
   - Trong reference, `TestQuestion` chỉ lưu danh sách `keywords: list[str]`. Hàm kiểm tra bằng phép so khớp chuỗi con đơn giản: `keyword_lower in doc.page_content.lower()`.
   - **Rủi ro cho Huế:** Cơ chế này dễ sinh lỗi dương tính giả (false positive) nếu một chunk bất kỳ chứa từ khóa nhưng không chứa thông tin cần tìm. Đặc biệt khi chunk có thêm trường tóm tắt (summary do LLM sinh), nguy cơ trùng khớp từ khóa càng tăng (dù mức độ đóng góp cụ thể vào MRR của PRO chưa được đo cô lập trong reference). Cơ chế này không thể dùng để đánh giá năng lực trích dẫn nguồn (citation) và định vị chính xác (`source_locator`) mà Huế đã chốt.
2. **Khác biệt về phạm vi đo giữa các Retrieval Metrics (MRR, Coverage vs. nDCG):**
   - Không thể coi mọi chỉ số retrieval đều áp dụng chung Top-K cutoff. Trong code (`evaluation/eval.py`), tham số `k` không được truyền vào hàm truy xuất; `calculate_mrr` và `keyword_coverage` duyệt trên toàn bộ danh sách tài liệu được trả về; chỉ riêng `calculate_ndcg` cắt `retrieved_docs[:k]`. Ngoài ra, IDCG chỉ sắp xếp lại các nhãn tìm thấy trong danh sách đã kéo về, không biết các tài liệu liên quan trong corpus nhưng nằm ngoài `retrieved_docs[:k]`.
3. **LLM Judge KHÔNG nhận ngữ cảnh truy xuất (`retrieved_context`) hoặc Citation:**
   - Trong code thực tế (`evaluation/eval.py`), Prompt gửi tới LLM Judge chỉ bao gồm: `test.question`, `generated_answer`, và `test.reference_answer`. Bối cảnh truy xuất `retrieved_docs` được hàm `answer_question` trả về nhưng **hoàn toàn bị bỏ qua**, không đưa vào prompt của giám khảo!
   - **Rủi ro cho Huế:** Điểm số `accuracy` và `completeness` của reference thực chất chỉ là đo mức độ tương đồng ngữ nghĩa giữa câu trả lời sinh ra và đáp án chuẩn. Nó **không đo lường tính bám sát nguồn (groundedness)** và **không phát hiện ảo giác (hallucination)** nếu LLM trả lời đúng nhờ trí nhớ tham số (parametric memory) dù retrieval kéo sai hoàn toàn.
4. **Chất lượng Ground Truth & Thiếu ca kiểm thử Negative / Mâu thuẫn:**
   - Về hình thức, 100% 150 dòng trong `tests.jsonl` đều có nội dung text `reference_answer` và không có ca kiểm thử negative (ngoài corpus/không trả lời được) được thiết kế có chủ đích.
   - Tuy nhiên, việc có text không đồng nghĩa với ground truth hoàn chỉnh: đối chiếu các records thực tế cho thấy tồn tại lỗi không khớp giữa câu hỏi và đáp án (ví dụ dòng 101 hỏi về sản phẩm nhưng đáp án chỉ nêu chức danh; dòng 141 hỏi số lượng nhân viên nhưng đáp án chỉ ghi "several" và nêu 2 ví dụ).
   - Đồng thời, trong phạm vi quan sát của reference, schema không có field/category riêng và chưa xác minh các ca kiểm thử được thiết kế, gán nhãn có chủ đích cho câu hỏi ngoài corpus (negative), thiếu bằng chứng một phần (partial-evidence), hoặc mâu thuẫn nguồn trong cùng phạm vi (nguyên tắc mà Huế đã chốt bắt buộc phải trình bày đa nguồn thay vì bịa đặt).
5. **Không có phân chia Test Split (Train / Dev / Held-out Test) & Nguy cơ Overfitting:**
   - Cùng một bộ 150 câu được dùng để chạy lặp đi lặp lại qua tất cả các thử nghiệm (chunking, embedding, reranker, PRO). Có nguy cơ cao hệ thống bị tối ưu hóa quá mức (overfitting) riêng cho 150 câu này thay vì cải thiện tính tổng quát thực tế.
6. **Bước nhảy chỉ số của PRO RAG là kết quả tổng hợp nhiều biến số:**
   - Điểm số MRR tăng từ ~0.73 lên ~0.91 và Accuracy từ ~3.99 lên ~4.62 trong PRO RAG không phải do riêng kỹ thuật chunking, mà là kết quả cộng gộp của 5 thay đổi đồng thời: đổi embedding sang OpenAI Large (3072D), viết lại truy vấn (Query Rewriting), truy xuất kép (Dual Retrieval k=20+20), tái xếp hạng bằng LLM (LLM Reranking), và sinh ngữ cảnh bổ sung (LLM Semantic Chunking). Không được ngộ nhận đây là chiến thắng của riêng một kỹ thuật.

---

## 2. Bản đồ phạm vi đã đọc (Reading Map & Coverage)

Báo cáo phân định rõ mức độ đọc giữa các khu vực: **Đọc sâu từng dòng** cho mã nguồn đánh giá và ingestion cốt lõi; **Đọc sâu theo vùng chuyên đề** cho các bài học và tài liệu lý thuyết liên quan đến evaluation; **Quét cấu trúc và tìm kiếm từ khóa** cho các tài liệu/notebooks còn lại.

Trong phạm vi các file mã nguồn và tài liệu đã khảo sát, không phát hiện script hoặc loader sinh tự động Golden Dataset; điều này phản ánh cấu trúc repo hiện có, không khẳng định tuyệt đối toàn bộ codebase khóa học không có công cụ bên ngoài.

### 2.1. Thư mục `rag_old_0`
- **Mã nguồn cốt lõi (Đọc sâu từng dòng):**
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/test.py` (25 dòng): Lớp Pydantic `TestQuestion` và hàm `load_tests()`.
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py` (250 dòng): Các hàm tính toán `calculate_mrr`, `calculate_dcg`, `calculate_ndcg`, `evaluate_retrieval`, `evaluate_answer`, vòng lặp batch và CLI runner. (Lưu ý: hiện đang kích hoạt import từ `pro_implementation.answer`).
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py` (237 dòng): Ứng dụng Gradio giao diện Dashboard, ngưỡng màu Xanh/Vàng/Đỏ, phân nhóm điểm theo `category`.
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py` (373 dòng): Bản nâng cấp hỗ trợ đa luồng (`ThreadPoolExecutor`), cấu hình tái lập (`configure_reproducibility(seed=42)`).
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/implementation/answer.py` (52 dòng) & `implementation/ingest.py` (65 dòng): Basic RAG (Chroma + LangChain + RecursiveCharacterTextSplitter).
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation/answer.py` (146 dòng) & `pro_implementation/ingest.py` (104 dòng): PRO RAG (Native Chroma + LLM Semantic Chunking + Query Rewriting + Dual Retrieval + LLM Reranking).
- **Notebooks (Đọc sâu outputs liên quan & Quét cấu trúc):**
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/day4.ipynb` (15 cells, đọc sâu cell 2–13): Nạp 150 records `tests[0]`, phân phối 7 categories, saved output của `evaluate_retrieval` (cell 7) và `evaluate_answer` (cell 9 & 13: 4/3/4).
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/day5.ipynb` (48 cells, quét cấu trúc & đọc cells rerank): Ingestion bất đồng bộ (`create_chunks_async`), logic `rerank` với `RankOrder`, `rewrite_query`, và `answer_question`.
  - `day1.ipynb`, `day2.ipynb`, `day3.ipynb`: Quét cấu trúc (ingest, chunking, retrieval cơ bản).
- **Tập dữ liệu kiểm thử (Đọc và phân tích cấu trúc):**
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/tests.jsonl` (150 dòng): Phân tích toàn bộ 150 records, thống kê phân phối 7 danh mục, kiểm tra các trường dữ liệu và đối chiếu thực tế các lỗi khớp câu hỏi - đáp án.

### 2.2. Thư mục `rag_old`
- **So sánh mã nguồn (Diff & Đọc sâu phần khác biệt):**
  - `evaluation/test.py`, `evaluator.py`, `evaluator2.py`, `evaluation/tests.jsonl`: Giống hệt bản `rag_old_0` (xác nhận qua so sánh nhị phân `cmp`).
  - `evaluation/eval.py` (276 dòng, đọc sâu từng dòng): Kết nối với Agentic Router `fetch_context_router`; kiểm tra keyword trong cấu trúc phân cấp `parent_headline + parent_chunk + child_chunks[0]` (lưu ý: chỉ kiểm tra child chunk đầu tiên, không phải toàn bộ child chunks).
  - `implementation/ingest.py` (315 dòng, đọc sâu): Pipeline chia chunk phân cấp cha-con (Parent-Child) lưu parent vào SQLite (`parent_chunks.db`) và child vào Chroma (`preprocessed_hierarchic_db`).
  - `implementation/answer.py` (477 dòng, đọc sâu): Router Agent với các chiến lược `fetch_context_single_doc`, `fetch_context_multi_hop`, `fetch_context_directory_scan`.
- **Tài liệu Study Guide & Ghi chú (Đọc sâu các phần liên quan đến Evaluation):**
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old/day4-rag-study-guide.html`: Section 5 (Retrieval Metrics), Section 6 (Evaluation Workflow), Section 7 (Structured Outputs & LLM-as-a-judge), Section 8 (Test Categories).
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old/day5-rag-study-guide.html`: Section 10 (Metric journey L1330–1346, Optimization workflow), Section 11 (Pitfalls & Overfitting).
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old/agentic-rag-insurellm-study-guide-codex.html`: Kiến trúc tổng quan của Agentic RAG và Router (đọc lướt để hiểu bối cảnh thế hệ 3).
  - `/home/minhhieu/llm_rag/tai_lieu/rag_old/test.md`: Ghi chú gốc của người dùng về việc tham khảo bộ test của khóa học để xây dựng dataset đánh giá cho Foods.

### 2.3. Thư mục phiên âm `phien_am_bai_hoc/`
*Lưu ý về nguồn tư liệu:* Các file trong thư mục này là tài liệu ghi chép/tổng hợp bài học đồng hành (gồm tóm tắt cốt lõi bài giảng, code minh họa phác thảo, và mục "Kiến thức liên quan & mở rộng"), không phải biên bản gỡ băng nguyên văn từng lời của giảng viên. Báo cáo phân biệt rõ nội dung tài liệu tổng hợp này với hành vi code thực tế trong file `.py`.
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day4.txt` (812 dòng, đọc sâu các bài liên quan eval): Bài 121 (Tổng quan Evals), Bài 122 (Retrieval Metrics & Golden Data), Bài 123 (Pydantic & Công thức MRR/Coverage), Bài 124 (LLM-as-a-judge & Case study Maxine L585–596), Bài 125 (Gradio Dashboard), Bài 126–127 (Thí nghiệm Chunking & Encoders).
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day5.txt` (746 dòng, đọc sâu): Bài 128 (Advanced RAG Overview), Bài 129 (Re-ranking & Scientific Evals), Bài 135 (Hành trình cải tiến chỉ số từ Basic lên Pro, L648: MRR 0.9116 / Accuracy 4.62).
- `day1.txt`, `day2.txt`, `day3.txt` (887 dòng tổng cộng): Tìm kiếm từ khóa, xác nhận không chứa nội dung chuyên sâu về Golden Dataset hay Evaluation.

---

## 3. Luồng dữ liệu và sự khác biệt giữa 3 implementation trong reference

Qua đối chiếu mã nguồn thực tế, reference tồn tại 3 thế hệ kiến trúc RAG với luồng dữ liệu đánh giá khác nhau:

```text
[Thế hệ 1: Basic RAG] (rag_old_0/implementation - ghi chú: đã bị comment out trong eval.py)
  tests.jsonl -> fetch_context(question) -> [Chroma Bi-encoder k=10] -> retrieved_docs
  -> MRR & Coverage: duyệt TOÀN BỘ retrieved_docs (không cắt k)
  -> nDCG: cắt retrieved_docs[:k], tính IDCG nội bộ trên kết quả kéo về
  -> Relevance: kiểm tra keyword_lower in doc.page_content.lower()
  -> answer_question -> LLM Judge (chỉ nhận question, answer, ref_answer)

[Thế hệ 2: PRO RAG] (rag_old_0/pro_implementation - HIỆN ĐANG IMPORT TRONG eval.py)
  tests.jsonl -> rewrite_query (LLM) -> 2x retrieval (k=20 câu gốc + k=20 câu rewrite)
  -> merge & dedup (tối đa 40 chunks) -> LLM Reranking (gpt-5-nano) -> Top 10 chunks (FINAL_K)
  -> MRR & Coverage: duyệt TOÀN BỘ 10 chunks đã rerank (không cắt thêm)
  -> nDCG: cắt retrieved_docs[:k] (với k=10 trùng độ dài danh sách)
  -> Relevance: kiểm tra keyword_lower in doc.page_content.lower() (gồm headline+summary+text)
  -> answer_question -> LLM Judge (chỉ nhận question, answer, ref_answer)

[Thế hệ 3: Agentic / Hierarchical RAG] (rag_old/evaluation/eval.py)
  tests.jsonl -> fetch_context_router (LLM Agent phân loại câu hỏi)
  -> gọi 1 trong 3 công cụ: Single Doc / Multi-hop (decompose) / Directory Scan
  -> kéo child chunks từ Chroma -> tra cứu parent chunk từ SQLite (parent_chunks.db)
  -> MRR & Coverage: duyệt TOÀN BỘ retrieved_docs do router trả về
  -> nDCG: cắt retrieved_docs[:k]
  -> Relevance: kiểm tra keyword trong parent_headline + parent_chunk + child_chunks[0] (chỉ child đầu tiên!)
  -> answer_question -> LLM Judge (chỉ nhận question, answer, ref_answer)
```

### So sánh các thành phần dữ liệu giữa 3 thế hệ

| Thành phần | Basic RAG (`rag_old_0`) | PRO RAG (`rag_old_0/pro`) | Agentic / Hierarchical RAG (`rag_old`) |
|---|---|---|---|
| **Trạng thái import trong `eval.py`** | Đã bị comment out (`#from implementation...`) | **Đang active** (`from pro_implementation...`) | Active (`fetch_context_router`) |
| **Chunking** | Ký tự đệ quy (1000/200) hoặc Markdown Splitter | LLM Semantic Chunking (headline + summary + original_text) | LLM Parent-Child Chunking (parent ~1000 chars, child ~200 chars) |
| **Lưu trữ** | Chroma DB (`vector_db`) | Chroma DB Native Client (`vector_db`) | Chroma DB (`preprocessed_hierarchic_db`) + SQLite (`parent_chunks.db`) |
| **Embedding** | `all-MiniLM-L6-v2` hoặc `text-embedding-3-small/large` | `text-embedding-3-large` (3072D) | `text-embedding-3-large` (3072D) |
| **Truy xuất đầu vào** | Truy xuất 1 lần câu gốc ($k=5$ hoặc $10$) | Truy xuất kép (câu gốc $k=20$ + câu rewrite $k=20$, gộp tối đa 40) | Router Agent tự động chọn Single / Multi-hop / Directory Scan |
| **Tái xếp hạng** | Không có (No rerank) | LLM Reranker (`gpt-5-nano` với Pydantic `RankOrder`) | LLM Reranker (`gpt-4.1-nano` với Pydantic `RankOrder`) |
| **Văn bản so khớp Relevance** | `doc.page_content` | `doc.page_content` (chứa cả summary do LLM sinh) | `parent_headline + parent_chunk + child_chunks[0]` (chỉ child đầu tiên) |
| **Cơ chế Cutoff $k$ khi đo** | MRR & Coverage: toàn bộ kết quả; chỉ nDCG cắt `[:k]` | MRR & Coverage: toàn bộ Top 10 sau rerank; nDCG cắt `[:k]` | MRR & Coverage: toàn bộ kết quả từ router; chỉ nDCG cắt `[:k]` |

---

## 4. Đối chiếu chi tiết theo từng khía cạnh kỹ thuật

### 4.1. Quy trình tạo câu hỏi & Ground Truth (Golden Dataset)

- **Nội dung bài học/tổng hợp (`day4.txt`, dòng 17, 64–67, 104–107):**
  - Tài liệu bài học định nghĩa Dữ liệu Vàng (Golden Data) là tập hợp các câu hỏi điển hình kèm câu trả lời tham chiếu "hoàn hảo" và các từ khóa bắt buộc phải xuất hiện.
  - Về nguồn gốc dữ liệu: Tài liệu ghi chép/tổng hợp hướng dẫn tự biên soạn thủ công dựa trên tài liệu kho tri thức, hoặc tốt nhất là lấy từ nhật ký câu hỏi thực tế của người dùng và câu trả lời đã được chuyên gia thẩm định trong sản xuất ("Living, breathing document", kết hợp phản hồi 👍/👎 của người dùng).
  - Trong các bài học đã khảo sát, không có hướng dẫn dùng LLM sinh tự động toàn bộ Golden Dataset trong Day 4/5.
- **Hành vi code thực tế:**
  - Trong các file mã nguồn đã kiểm tra, không có bất kỳ script hay hàm nào tự động tạo ra hoặc ghi đè file `tests.jsonl`.
  - File `tests.jsonl` là fixture tĩnh gồm 150 dòng được chuẩn bị trước. Lớp `TestQuestion` trong `evaluation/test.py` (dòng 8–24) chỉ thực hiện đọc và validate dữ liệu qua Pydantic.
- **Kết quả lưu sẵn:**
  - `day4.ipynb` (Cell 2–5): Xác nhận nạp thành công 150 records, in ra phân phối 7 danh mục.
- **Nhận xét của Implementer cho Huế:**
  - Việc tồn tại chuỗi text trong `reference_answer` không chứng minh đáp án đó đúng và đầy đủ về mặt nội dung. Khi kiểm tra sâu các records thực tế (như phân tích ở Mục 5), phát hiện các lỗi chất lượng ground truth: ví dụ dòng 101 hỏi về sản phẩm nhưng đáp án chỉ nêu chức danh; dòng 141 hỏi số lượng nhân viên nhưng đáp án chỉ ghi "several" và nêu hai ví dụ.
  - Về phương pháp: Biên soạn câu hỏi thủ công bảo đảm kiểm soát chất lượng nhưng tốn công sức khi mở rộng ra 204 tài liệu trên 5 domain của Huế. Huế cần quy trình xây dựng Golden có kiểm duyệt chặt chẽ (human-in-the-loop): câu hỏi, câu trả lời tham chiếu và ranh giới bằng chứng bắt buộc phải được kiểm toán (audit) trước khi dùng làm căn cứ đánh giá.

### 4.2. Schema của Golden Dataset & Cách gán Evidence

- **Nội dung bài học/tổng hợp (`day4.txt`, dòng 448–466; `day4-rag-study-guide.html`, dòng 831):**
  - Schema gồm: câu hỏi người dùng (`question`), các từ khóa bắt buộc (`keywords`), câu trả lời chuẩn (`reference_answer`) và danh mục câu hỏi (`category`).
- **Hành vi code thực tế (`evaluation/test.py`, dòng 8–15):**
  ```python
  class TestQuestion(BaseModel):
      question: str = Field(description="The question to ask the RAG system")
      keywords: list[str] = Field(description="Keywords that must appear in retrieved context")
      reference_answer: str = Field(description="The reference answer for this question")
      category: str = Field(description="Question category (e.g., direct_fact, spanning, temporal)")
  ```
  - **Cách gán Evidence:** Hoàn toàn dựa vào danh sách chuỗi con `keywords: list[str]`.
  - Trong `evaluation/eval.py` (dòng 45–57):
    ```python
    def calculate_mrr(keyword: str, retrieved_docs: list) -> float:
        keyword_lower = keyword.lower()
        for rank, doc in enumerate(retrieved_docs, start=1):
            if keyword_lower in doc.page_content.lower():
                return 1.0 / rank
        return 0.0
    ```
- **Kết quả lưu sẵn:**
  - `day4.ipynb` (Cell 4): `example = tests[0]` in ra:
    `Keywords: ['Maxine', 'Thompson', 'IIOTY']`.
- **Nhận xét của Implementer cho Huế:**
  - **Hạn chế kỹ thuật:** Cơ chế gán bằng từ khóa hoàn toàn không có `chunk_id`, `source_file`, `heading_path` hay `evidence_span` `[start, end)`.
  - Nếu một tài liệu khác ngẫu nhiên chứa từ "Maxine", thuật toán vẫn tính là tìm trúng (dương tính giả). Đặc biệt khi chunk được bổ sung tóm tắt (summary do LLM sinh), nguy cơ trùng khớp từ khóa càng cao (đây là rủi ro thiết kế tiềm ẩn cần tránh, dù mức độ đóng góp cụ thể vào MRR của PRO chưa được đo riêng trong reference).
  - Đối với Huế, theo quyết định Phương án C đã được User xác nhận, Golden dataset toàn corpus vẫn duy trì định dạng file JSONL đơn giản (theo tinh thần Foods V3), nhưng ở tầng bằng chứng sẽ liên kết từng expected claim với các `evidence_groups` chứa exact source spans (`source`, `heading_path`, `start`, `end`, `text` trên file nguồn chuẩn hóa LF) thay vì lưu `chunk_id` làm canonical ground truth. Chunk ID sẽ được ánh xạ động tại thời điểm đánh giá ứng với từng cấu hình chunking, phục vụ đo retrieval chính xác và kiểm chứng trích dẫn nguồn (citation validation).

### 4.3. Chỉ số Retrieval (MRR, nDCG, Keyword Coverage)

- **Nội dung bài học/tổng hợp (`day4.txt`, dòng 25–28, 73–78, 469–490; `day5.txt`, dòng 69–72):**
  - MRR đo thứ hạng nghịch đảo của kết quả đúng đầu tiên. Nếu kết quả đúng luôn ở vị trí 1 thì MRR = 1.
  - nDCG đo chất lượng phân phối xếp hạng, phạt nặng hơn nếu tài liệu liên quan nằm ở cuối danh sách bằng hàm logarit $\log_2(rank + 1)$.
  - Keyword Coverage đo tỷ lệ phần trăm từ khóa vàng được tìm thấy.
- **Hành vi code thực tế (`evaluation/eval.py`, dòng 45–115):**
  - **Khác biệt về phạm vi áp dụng Cutoff $k$:**
    * Tham số $k$ (mặc định $k=10$) **hoàn toàn không được truyền vào hàm truy xuất** (`fetch_context(test.question)` hoặc `fetch_context_router(test.question)`). Số lượng tài liệu trả về hoàn toàn do bản thân module retrieval quyết định (ví dụ: PRO RAG trả về Top 10 sau khi rerank, Basic RAG trả về Top 10 từ vector store).
    * `calculate_mrr(keyword, retrieved_docs)`: **duyệt qua toàn bộ danh sách `retrieved_docs`**, không có tham số cắt $k$ (dòng 48–51).
    * `calculate_coverage`: tính bằng tỷ lệ số từ khóa có `score > 0` trong `mrr_scores` chia cho tổng số từ khóa. Do MRR duyệt toàn bộ, **Coverage cũng sử dụng toàn bộ danh sách `retrieved_docs`**, không áp dụng cutoff $k$.
    * **Chỉ duy nhất `calculate_ndcg(keyword, retrieved_docs, k)` áp dụng cắt danh sách theo Top-$k$:** `retrieved_docs[:k]` (dòng 68).
  - **Công thức tính nDCG và giới hạn của IDCG:**
    * Code gán binary relevance: $rel_i = 1$ nếu `keyword` xuất hiện trong tài liệu thứ $i$ của `retrieved_docs[:k]`, ngược lại $0$.
    * $DCG = \sum_{i=0}^{min(k, len)-1} \frac{rel_i}{\log_2(i+2)}$.
    * $Ideal\text{ }DCG\text{ }(IDCG)$: Code tính bằng cách sắp xếp giảm dần chính các giá trị relevance đã trích xuất: `ideal_relevances = sorted(relevances, reverse=True)`.
    * **Giới hạn quan trọng:** IDCG ở đây **chỉ biết các bằng chứng liên quan đã nằm sẵn trong danh sách kéo về được**. IDCG hoàn toàn không biết có bao nhiêu bằng chứng liên quan thực sự tồn tại trong toàn bộ kho dữ liệu bị retrieval bỏ sót. Do đó, nếu retrieval chỉ kéo về đúng 1 chunk liên quan và chunk đó xếp đầu, nDCG vẫn bằng $1.0$ dù retrieval đã bỏ sót nhiều chunk liên quan khác trong corpus!
  - **Đơn vị văn bản kiểm tra tính liên quan (Relevance Text):**
    * Trong `rag_old_0/evaluation/eval.py`: so khớp `keyword_lower in doc.page_content.lower()`.
    * Trong `rag_old/evaluation/eval.py` (Hierarchical): so khớp `keyword_lower in doc.parent_headline.lower() + "\n" + doc.parent_chunk.lower() + "\n" + doc.child_chunks[0].lower()`. Chú ý: code **chỉ kiểm tra child chunk đầu tiên (`child_chunks[0]`)**, không kiểm tra toàn bộ các child chunks còn lại!
  - **Thời điểm đo:** Code đo trên danh sách tài liệu cuối cùng trả về bởi `fetch_context`. Trong PRO RAG, đây là danh sách sau khi đã Query Rewrite, Dual Retrieve và LLM Rerank. Code không đo riêng rẽ retrieval ban đầu và sau rerank trong cùng một run.
- **Kết quả lưu sẵn:**
  - `day4.ipynb` (Cell 7): `evaluate_retrieval(example)` trả về:
    `RetrievalEval(mrr=0.1667, ndcg=0.2871, keywords_found=2, total_keywords=3, keyword_coverage=66.67%)`.
- **Nhận xét của Implementer cho Huế:**
  - Không thể sao chép nguyên xi cách đo này cho Huế vì sự thiếu đồng nhất về cutoff và việc IDCG tính nội bộ trên danh sách đã kéo về sẽ làm sai lệch bản chất của nDCG chuẩn trong IR.
  - Trong Phase 8 của Huế, dự án đã chuẩn hóa việc đo retrieval bằng Recall@K, MRR@K, nDCG@K rõ ràng trên **cặp (source, section)** hoặc **chunk ID**, biết rõ tổng số relevant chunks trong corpus. Huế cần tiếp tục chuẩn hóa cutoff đồng nhất cho từng metric cho full corpus.

### 4.4. Đánh giá câu trả lời (Answer Evaluation: LLM-as-a-judge)

- **Nội dung bài học/tổng hợp (`day4.txt`, dòng 29–31, 79–84, 507–522):**
  - Tài liệu bài học nhấn mạnh sử dụng LLM làm giám khảo độc lập chấm điểm tự động thay cho việc đọc thủ công.
  - 3 tiêu chí:
    * **Accuracy (Độ chính xác):** Có đúng sự thật so với câu trả lời chuẩn không? (Nếu sai, điểm phải là 1).
    * **Completeness (Độ đầy đủ):** Có bao quát toàn bộ thông tin từ câu trả lời chuẩn không?
    * **Relevance (Mức độ liên quan):** Có trả lời thẳng vào câu hỏi, không lan man, không đưa thừa thông tin không?
  - Bắt buộc dùng **Structured Outputs** (Pydantic model) để nhận kết quả định dạng JSON chuẩn.
- **Hành vi code thực tế (`evaluation/eval.py`, dòng 28–42, 117–160):**
  - **Lớp Pydantic:**
    ```python
    class AnswerEval(BaseModel):
        feedback: str = Field(description="Concise feedback on the answer quality...")
        accuracy: float = Field(description="How factually correct is the answer compared to the reference answer? 1 to 5...")
        completeness: float = Field(description="How complete is the answer in addressing all aspects...")
        relevance: float = Field(description="How relevant is the answer to the specific question asked...")
    ```
  - **Prompt gửi LLM Judge (`eval.py`, dòng 131–154):**
    ```python
    judge_messages = [
        {"role": "system", "content": "You are an expert evaluator assessing the quality of answers. Evaluate the generated answer by comparing it to the reference answer. Only give 5/5 scores for perfect answers."},
        {"role": "user", "content": f"Question:\n{test.question}\n\nGenerated Answer:\n{generated_answer}\n\nReference Answer:\n{test.reference_answer}\n\nPlease evaluate..."}
    ]
    ```
  - **Sự thật quan sát từ code:** Prompt của Judge **hoàn toàn KHÔNG chứa** `retrieved_docs`, `context`, `citation` hay nguồn tài liệu!
  - Mô hình gọi judge: `gpt-4.1-nano` (trong `rag_old`) hoặc `gpt-5-nano` (trong `rag_old_0`).
- **Kết quả lưu sẵn và phân biệt hai mốc quan sát:**
  - **Mốc 1 (Lời tổng hợp bài học, `day4.txt`, dòng 592):** Thuật lại một ví dụ minh họa case Maxine thiếu họ, theo đó Giám khảo AI cho Accuracy 5/5 và Completeness 4/5.
  - **Mốc 2 (Kết quả lưu sẵn trong notebook `day4.ipynb`, Cell 9 & 13):** Khi chạy `evaluate_answer` trên `example = tests[0]` với Basic RAG, output thực tế lưu lại là:
    `accuracy=4.0, completeness=3.0, relevance=4.0` (4/3/4).
    Feedback: *"The generated answer correctly identifies the winner as 'Maxine' and correctly names the award and year, but it is not a perfect match to the reference. It omits her last name ('Thompson') and adds unverified details (her title and the reasons for recognition) that are not present in the reference."*
  - **Phân định rõ:** Hai kết quả trên (5/4 vs. 4/3/4) là hai quan sát lưu sẵn ở các tài liệu/bối cảnh khác nhau; do không có thử nghiệm lặp lại có kiểm soát (controlled repetition) trên cùng một input/setup nên nguyên nhân gây ra sự chênh lệch này chưa được cô lập (không quy riêng cho độ biến thiên tự nhiên của LLM Judge). Kết quả lưu trong notebook không phải là kết quả thực thi của code hiện tại (vì `eval.py` hiện tại đang import PRO RAG).
- **Nhận xét của Implementer cho Huế:**
  - Việc Prompt của Judge hoàn toàn thiếu `retrieved_docs` là một lỗ hổng nghiêm trọng: **Judge không thể đo Groundedness (tính bám sát nguồn) và không thể phát hiện Hallucination**. Nếu Generator trả lời đúng đáp án nhờ trí nhớ tham số của LLM dù retrieval lấy sai hoàn toàn, Judge vẫn cho điểm tối đa!
  - Với Huế, đề xuất Judge prompt cần nhận thêm `retrieved_context` để có căn cứ đánh giá: (1) Groundedness (câu trả lời có dựa trên context được cung cấp không), (2) Citation Validity (trích dẫn có đúng văn bản nguồn không), và (3) Tuân thủ việc từ chối khi thiếu dữ liệu; tuy nhiên cấu trúc prompt, số lượng tiêu chí và thang điểm cụ thể vẫn là đề xuất thiết kế mở để Reviewer và User quyết định.

### 4.5. So sánh thực nghiệm (Experimentation, Baseline, Split, Leakage, Variability)

- **Nội dung bài học/tổng hợp (`day4.txt`, dòng 678–738; `day5.txt`, dòng 88–94; `day5-rag-study-guide.html`, dòng 1330–1346):**
  - Tài liệu ghi chép/tổng hợp nhấn mạnh nguyên tắc "Táo so với Táo" (Apple-to-Apple): Khi đổi chunk size từ 1000 xuống 500, phải tăng $K$ từ 5 lên 10 để tổng lượng ngữ cảnh nạp vào LLM tương đương nhau.
  - Phải lập bảng Benchmark theo dõi: `Chunk Size | K | Model | MRR | Accuracy`.
  - Cảnh báo bẫy "Overfitting to eval set" (`day5-rag-study-guide.html`, dòng 1372): tối ưu để thắng 150 câu trong `tests.jsonl` nhưng thất bại với câu hỏi người dùng thực tế.
- **Hành vi code thực tế:**
  - **Baseline:** Được xác lập ở Day 4 (Chunk 1000, K=5, MiniLM embedding) với MRR = 0.7298, Accuracy = 3.99/5 (`day4.txt`, dòng 669, 698).
  - **Không có Data Split:** Toàn bộ 150 câu được chạy chung một lượt. Không có hàm `train_test_split`, không có validation set riêng, không có held-out test set.
  - **Không có lặp lại (Repetitions) trong `eval.py` gốc:** Mỗi câu hỏi chỉ chạy 1 lần.
  - **Kiểm soát tính tái lập (Reproducibility) trong `evaluator2.py` (dòng 22, 41–60):** Thiết lập `SEED = 42` cho `random`, `numpy`, `ChatOpenAI(temperature=0, seed=42)` và patch hàm `completion` của LiteLLM để cố định `seed=42`. Cần lưu ý: Đây là cấu hình kiểm soát thực nghiệm (control configuration), không bảo đảm tính tất định 100% (deterministic) của LLM API do các yếu tố hạ tầng của provider (MoE routing, tính toán dấu phẩy động song song trên GPU).
  - **Phân nhóm Category:** `evaluator.py` (dòng 84–94, 116–123, 131–141) tổng hợp điểm theo 7 nhóm để vẽ bar chart trên giao diện Gradio.
- **Kết quả lưu sẵn (Tổng hợp qua các mốc bài học):**

| Cấu hình thử nghiệm | File / Vị trí trích xuất | MRR | Accuracy (1–5) | Completeness (1–5) | Ghi chú biến số thay đổi |
|---|---|:---:|:---:|:---:|---|
| **Baseline ban đầu** | `day4.txt` L698, L669; `rag_old/day5-rag-study-guide.html` L1331 | **0.7298** | **3.99** | - | Chunk 1000, overlap 200, all-MiniLM-L6-v2, K=5 |
| **Thử nghiệm Chunk 500** | `day4.txt` L699 | > 0.73 | - | - | Giảm chunk 500, tăng K=10, giữ MiniLM |
| **Thử nghiệm Chunk 1667** | `day4.txt` L700 | 0.7475 | - | - | Tăng chunk 1667, giảm K=3 |
| **Thử nghiệm Markdown Splitter** | `day4.txt` L701 | 0.7380 | - | - | Chia theo tiêu đề Markdown (#, ##) |
| **OpenAI Small Embeddings** | `day4.txt` L755 | 0.7849 | - | - | Đổi sang `text-embedding-3-small` (1536D), K=10 |
| **OpenAI Large Embeddings** | `day4.txt` L756–758; `rag_old/day5-rag-study-guide.html` L1332 | **0.7903** | **4.21** | **4.05** | Đổi sang `text-embedding-3-large` (3072D), K=10 |
| **Advanced RAG Pro** | `day5.txt` L648; `rag_old/day5-rag-study-guide.html` L1333 | **0.9116** | **4.62** | - | Đổi đồng thời: Semantic Chunking + OpenAI Large + Query Rewrite + Dual Retrieval (k=40) + LLM Reranker (`gpt-5-nano`) |

- **Nhận xét của Implementer cho Huế:**
  - Việc theo dõi hành trình chỉ số qua từng giai đoạn là phương pháp luận khoa học tốt.
  - Tuy nhiên, bước nhảy của PRO RAG là kết quả cộng gộp của 5 biến số thay đổi đồng thời, không thể quy kết quả cho riêng kỹ thuật semantic chunking.
  - Trong Phase 8 của Huế, việc đánh giá mô hình đã tách bạch từng thí nghiệm ablation (08a riêng Embedding dense, 08b riêng Fusion/Sparse, 08c riêng Reranker). Huế cần tiếp tục phương pháp ablation có kiểm soát này khi mở rộng cho full corpus.

---

## 5. Dẫn chứng mẫu dữ liệu thực tế (Real Records Analysis)

Dưới đây là 4 mẫu dữ liệu thực tế được trích xuất trực tiếp từ `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/tests.jsonl`:

### Mẫu 1: `direct_fact` (Row 0, Line 1)
```json
{
  "question": "Who won the prestigious IIOTY award in 2023?",
  "keywords": ["Maxine", "Thompson", "IIOTY"],
  "reference_answer": "Maxine Thompson won the prestigious Insurellm Innovator of the Year (IIOTY) award in 2023.",
  "category": "direct_fact"
}
```
- *Đặc điểm:* Câu hỏi tra cứu một sự thật đơn lẻ. Cả 3 từ khóa đều nằm tập trung trong 1 file nhân sự (`knowledge-base/employees/Maxine Thompson.md`). Basic RAG giải quyết tốt.

### Mẫu 2: `temporal` (Row 65, Line 66)
```json
{
  "question": "When did Maxine Thompson join Insurellm?",
  "keywords": ["January 2017", "Maxine"],
  "reference_answer": "Maxine Thompson joined Insurellm in January 2017 as a Junior Data Engineer.",
  "category": "temporal"
}
```
- *Đặc điểm:* Câu hỏi liên quan đến mốc thời gian. Từ khóa gồm tên thực thể và tháng năm cụ thể.

### Mẫu 3: `spanning` (Row 100, Line 101)
```json
{
  "question": "What product does the IIOTY award winner work on?",
  "keywords": ["Maxine", "Thompson", "Senior Data Engineer", "IIOTY"],
  "reference_answer": "Maxine Thompson, who won the IIOTY award in 2023, works as a Senior Data Engineer.",
  "category": "spanning"
}
```
- *Đặc điểm cấu trúc:* Câu hỏi bắc cầu nhiều tài liệu / nhiều phần (nối thông tin người đoạt giải IIOTY với sản phẩm làm việc).
- *Lỗi chất lượng Ground Truth thực tế:* Câu hỏi hỏi rõ về sản phẩm ("What product does the IIOTY award winner work on?"), nhưng câu trả lời chuẩn lại chỉ nêu chức danh công việc ("works as a Senior Data Engineer") mà không hề trả lời sản phẩm nào. Từ khóa vàng cũng đưa cụm "Senior Data Engineer" thay vì tên sản phẩm. Đây là bằng chứng thực tế cho thấy tập `tests.jsonl` có lỗi không khớp giữa câu hỏi và đáp án tham chiếu, không thể xem là 100% hoàn chỉnh.

### Mẫu 4: `holistic` (Row 140, Line 141)
```json
{
  "question": "How many employees at Insurellm have a current salary under $80,000?",
  "keywords": ["salary", "employees"],
  "reference_answer": "Based on the employee records, there are several employees with salaries under $80,000, including Tyler Brooks ($75,000) and Alex Harper ($75,000).",
  "category": "holistic"
}
```
- *Lỗi chất lượng Ground Truth thực tế:* Câu hỏi hỏi về số lượng nhân viên ("How many employees..."), đòi hỏi con số thống kê tổng thể hoặc danh sách đầy đủ, nhưng đáp án chuẩn chỉ trả lời định tính chung chung "there are several employees..." và nêu hai ví dụ. Đáp án này không trả lời trọn vẹn yêu cầu câu hỏi.
- *Đặc điểm truy xuất:* Câu hỏi mang tính tổng hợp toàn kho dữ liệu (holistic/aggregate). Các câu hỏi dạng này rất khó để Top-K vector thông thường gom đủ mọi thông tin liên quan, đòi hỏi các giải pháp mở rộng ngữ cảnh hoặc cấu trúc hóa dữ liệu phù hợp; tuy nhiên các kiến trúc Agentic RAG phức tạp nằm ngoài phạm vi MVP của Huế.

---

## 6. Bảng đánh giá kế thừa cho Full-Corpus Huế

| Khía cạnh kỹ thuật | Trạng thái trong Reference (`llm_rag`) | Đánh giá đối với Full-Corpus Huế | Đề xuất hướng xử lý cho Huế |
|---|---|---|---|
| **Tách biệt 2 khâu Retrieval & Answer** | Có. Đo riêng tầng truy xuất và tầng trả lời. | **Kế thừa 100%**. Đây là nguyên tắc cốt lõi đã áp dụng từ Phase 7 Foods. | Giữ nguyên việc đánh giá độc lập tầng Retrieval và tầng Generation. |
| **Phân loại câu hỏi theo Categories** | Có 7 categories (`direct_fact`, `temporal`, `spanning`, `comparative`, `numerical`, `relationship`, `holistic`). | **Kế thừa & Điều chỉnh**. Huế cần phân loại đa chiều: theo 5 domain (`foods`, `heritages`, `festivals`, `performing_arts`, `travel`) và theo loại truy vấn (sự thật, so sánh, liên miền, lịch trình, vé). | Xây dựng bộ Golden có phân loại theo cả Domain và Query Type. |
| **Cơ chế Cutoff và Đơn vị Retrieval** | Không đồng nhất: $k$ không truyền vào retriever; MRR và Coverage duyệt toàn bộ retrieved docs; chỉ nDCG cắt Top-$k$; IDCG chỉ tính nội bộ trên list đã kéo về. | **Không kế thừa cách đo này**. IDCG nội bộ làm sai lệch bản chất nDCG chuẩn; thiếu đồng nhất cutoff giữa các metric. | Chuẩn hóa cutoff $k$ rõ ràng và thống nhất (Recall@k, MRR@k, nDCG@k) trên đơn vị chunk/source, tính IDCG dựa trên toàn bộ true evidence trong corpus. |
| **Gán Evidence bằng `keywords`** | Chỉ dùng list từ khóa con, so khớp `keyword.lower() in doc.page_content.lower()`. | **KHÔNG kế thừa**. Dễ dương tính giả, không kiểm soát được citation; có rủi ro tiềm ẩn làm méo mó kết quả khi chunk có summary. | Áp dụng Phương án C đã được User xác nhận: Golden lưu dạng JSONL đơn giản (theo tinh thần Foods V3), từng expected claim gắn với `evidence_groups` chứa exact source spans (`source`, `heading_path`, `start`, `end`, `text` trên file nguồn chuẩn hóa LF). Tuyệt đối không lưu cứng `chunk_id` làm canonical ground truth mà phân giải động theo candidate chunking khi eval. |
| **Input gửi cho LLM Judge** | Chỉ gửi `question`, `generated_answer`, `reference_answer`. Hoàn toàn không gửi context. | **KHÔNG kế thừa**. Bỏ qua context khiến Judge không thể đo Groundedness và không thể phát hiện ảo giác. | Đề xuất Judge prompt nhận thêm `retrieved_context` để đánh giá groundedness, citation validity và việc tuân thủ từ chối khi thiếu dữ liệu; rubric và prompt cụ thể là đề xuất mở chờ Reviewer/User quyết định. |
| **Chất lượng Golden & Ca kiểm thử âm tính** | 100% câu hỏi có text đáp án (không có ca negative được gán nhãn có chủ đích), nhưng có lỗi không khớp nội dung (dòng 101, 141). | **CẦN BỔ SUNG LỚN & KIỂM TOÁN**. Chính sách trả lời của Huế bắt buộc từ chối khi corpus không có hoặc thiếu thông tin. | Thiết kế có chủ đích nhóm câu hỏi Out-of-Corpus / Partial-Evidence; đồng thời kiểm toán chặt chẽ câu hỏi - đáp án - bằng chứng trước khi chốt Golden. |
| **Ca mâu thuẫn nguồn & Khác điều kiện** | Có nhóm `temporal`, nhưng không có trường/nhãn riêng và chưa xác minh ca mâu thuẫn nguồn trong cùng phạm vi được thiết kế có chủ đích. | **CẦN BỔ SUNG LỚN**. Huế đã chốt chính sách xử lý minh bạch cho cả hai tình huống. | Phân định rõ: (1) Nguồn mâu thuẫn trong cùng phạm vi: trình các thông tin kèm nguồn; (2) Khác biệt do khác điều kiện, thời điểm, nhà cung cấp: nêu rõ điều kiện tương ứng. |
| **Ngưỡng màu trực quan (Dashboard Thresholds)** | Có (Gradio Dashboard với Xanh $\ge 0.9$, Vàng $\ge 0.75$, Đỏ $< 0.75$). | **Tham khảo giao diện, KHÔNG lấy làm gate nghiệm thu**. Ngưỡng InsureLLM không phản ánh bài toán của Huế. | Huế sẽ tự định nghĩa các ngưỡng đánh giá và tiêu chuẩn nghiệm thu độc lập trong written spec và benchmark plan. |
| **Kiểm soát tính tái lập (Reproducibility)** | Cố định `seed=42`, `temperature=0` trong `evaluator2.py`. | **Kế thừa có nhận thức giới hạn**. Cấu hình kiểm soát tốt nhưng không đảm bảo 100% tất định từ phía API. | Áp dụng `temperature=0` và cố định seed cho các pipeline benchmark/evaluator, ghi nhận độ biến thiên tự nhiên của LLM Judge. |
| **Phân chia tập dữ liệu (Data Split)** | Không có. Dùng chung 150 câu cho cả baseline và tuning. | **Cần xem xét cho đồ án**. Tránh rủi ro overfitting khi tinh chỉnh chunking/retrieval. | Cân nhắc chia Golden thành tập Dev (để tinh chỉnh) và tập Test (held-out để đánh giá nghiệm thu khách quan). |

---

## 7. Những quyết định thiết kế cần Reviewer và User giải quyết tiếp theo

Dựa trên kết quả rà soát reference, Implementer tổng hợp các câu hỏi và đề xuất kiến trúc còn mở cần Reviewer phân tích thiết kế độc lập và User định hướng (đây là các đề xuất tham khảo, không tự xem là requirement đã chốt):

1. **Schema và biểu diễn bằng chứng của Golden Dataset cho toàn corpus Huế:**
   - Reference dùng `{question, keywords, reference_answer, category}`.
   - Chuẩn Phase 8 Foods (`golden_v3.jsonl` theo spec thiết kế `docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md:131–143`) gồm đúng 6 trường: `{case_id, question, keywords, reference_answer, category, evidence}`, trong đó trường `evidence` ánh xạ đường dẫn file nguồn tương đối tới danh sách các heading H2 chính xác (`{"<relative_source_path>": ["<H2 heading 1>", ...]}`).
   - **Định hướng đơn vị bằng chứng đã chốt:** User đã chính thức chọn **Phương án C** (2026-09-10): Golden dataset toàn corpus vẫn là file JSONL đơn giản theo tinh thần Foods V3, nhưng từng expected claim sẽ được gắn với các `evidence_groups` chứa exact source spans (`source`, `heading_path`, `start`, `end`, `text` trên file nguồn chuẩn hóa LF); tuyệt đối không dùng `chunk_id` làm canonical ground truth (chunk ID được ánh xạ động khi đánh giá theo từng cấu hình candidate chunking). Do đó, câu hỏi lựa chọn giữa source+section hay exact spans đã được giải quyết xong, không còn đặt lại.
   - **Các vấn đề mở còn lại về schema cần Reviewer và User giải quyết tiếp:**
     - Bộ trường đầy đủ chính xác của từng record JSONL (các trường domain/metadata bổ sung nếu cần).
     - Cấu trúc biểu diễn cụ thể của các nhóm bằng chứng thay thế (alternative evidence groups) khi một luận điểm có thể chứng minh từ nhiều nguồn/vị trí độc lập.
     - Cơ chế biểu diễn cho các ca đặc thù (câu hỏi ngoài corpus / negative, thiếu bằng chứng một phần / partial, nguồn mâu thuẫn / conflict).
     - Quy chuẩn kiểm thực schema (schema validation) trước khi tạo và nghiệm thu bộ dữ liệu.
2. **Quy mô và phân bổ hạn ngạch (Quotas) câu hỏi:**
   - Reference dùng 150 câu cho kho dữ liệu nhỏ (~40 file). Huế có 204 file Markdown answer-facing trên 5 domain.
   - **Vấn đề mở:** Tổng số lượng câu hỏi là bao nhiêu (ví dụ tham khảo: 100, 150 hay 200 câu)? Phân bổ hạn ngạch cho 5 domain (`foods`, `heritages`, `festivals`, `performing_arts`, `travel/places, services, tickets`) như thế nào để đảm bảo tính đại diện?
3. **Tỷ lệ các câu hỏi đặc thù (Negative / Partial / Conflict Cases):**
   - Trong reference chưa có trường/nhãn riêng và chưa xác minh các ca kiểm thử được thiết kế có chủ đích cho các nhóm này.
   - **Vấn đề mở:** Có dành một tỷ lệ tham khảo (ví dụ gợi ý 10–15% số câu) cho: (a) Câu hỏi ngoài corpus / không có thông tin, (b) Câu hỏi thiếu bằng chứng một phần, (c) Câu hỏi có thông tin mâu thuẫn trong cùng phạm vi, và (d) Câu hỏi có thông tin phụ thuộc điều kiện/thời hạn?
4. **Cơ chế chấm điểm của LLM Judge (Groundedness vs. Correctness):**
   - **Vấn đề mở:** Thiết kế rubric và prompt cho LLM Judge nhận `retrieved_context` và đánh giá đa tiêu chí: (1) Groundedness (1-5 điểm), (2) Completeness (1-5 điểm), (3) Citation Validity (trích dẫn đúng nguồn), và (4) Tuân thủ từ chối khi thiếu dữ liệu.
5. **Chiến lược phân chia tập dữ liệu (Split Strategy):**
   - **Vấn đề mở:** Có nên chia tập Golden thành `dev` (để tinh chỉnh tham số chunking/retrieval) và `test` (held-out để đánh giá nghiệm thu cuối cùng) nhằm chống overfitting hay không?

---

## 8. Tự review và trạng thái Git

- **Bảo toàn phạm vi:**
  - Không chạy code, model, notebook, tests, API hoặc benchmark.
  - Không đọc `.env` hoặc thông tin bảo mật.
  - Không sửa đổi bất kỳ file nào trong `/home/minhhieu/llm_rag`.
  - Không sửa đổi runtime, tests, corpus, index, settings của `hue_rag`.
  - Chỉ chỉnh sửa đúng 2 file được giao: `reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md` và `session_prompt/CURRENT_HANDOFF.md`.
- **Trạng thái findings R1–R3:** Reviewer đã xác nhận đóng trong đợt review lượt 2 (`reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md` mục 9–10). Giữ nguyên toàn bộ các nội dung đã sửa cho R1–R3, không mở lại hay thay đổi.
- **Thực hiện correction lượt 3 cho finding R4 (schema Foods V3 & Phương án C):**
  - Sửa lại mô tả schema canonical của Foods V3 trong §7 về đúng 6 trường `{case_id, question, keywords, reference_answer, category, evidence}` và cấu trúc `evidence` ánh xạ source path tới danh sách heading H2 chính xác theo đúng spec thiết kế `docs/superpowers/specs/2026-08-27-phase-8-golden-dataset-v3-design.md:131–143` và `knowledge-base-hue/foods/evaluation/golden_v3.jsonl` (thay cho mô tả sai trước đó).
  - Loại bỏ câu hỏi lỗi thời về việc chọn source+section hay exact spans: khẳng định rõ User đã chọn Phương án C (file JSONL đơn giản theo tinh thần Foods V3, từng expected claim gắn với `evidence_groups` dùng exact source spans `{source, heading_path, start, end, text}` trên file nguồn chuẩn hóa LF; chunk ID không lưu làm canonical ground truth mà phân giải động khi eval).
  - Đồng bộ toàn bộ các đề xuất tại §4.2, Bảng mục 6 và §7 theo đúng Phương án C.
  - Phân định rành mạch các vấn đề mở còn lại chưa chốt: exact full field set, cấu trúc alternative evidence groups, biểu diễn các ca đặc thù (negative/partial/conflict), schema validation, hạn ngạch quotas, train/dev/test split, ngưỡng đánh giá (thresholds) và exact judge rubric vẫn là đề xuất mở chờ Reviewer thiết kế spec/plan và User phê duyệt.
  - Báo cáo được chuyển về Reviewer để đánh giá độc lập; tuyệt đối không tự đánh dấu R4 approved hay technical PASS.
- **Kiểm tra định dạng:** Lệnh `git diff --check` sạch hoàn toàn, không có lỗi khoảng trắng hay định dạng.
