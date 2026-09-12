# Báo Cáo Khảo Sát Tính Tối Giản Của Hệ Thống Đánh Giá RAG Trong `rag_old_0` (Correction Lượt 2)

- **Ngày lập:** 2026-09-10 (Cập nhật Correction lượt 2)
- **Dự án:** `/home/minhhieu/hue_rag`
- **Nguồn khảo sát:** `/home/minhhieu/llm_rag/tai_lieu/rag_old_0`
- **Vai trò:** Implementer
- **Mã văn bản / Handoff Contract:** `handoff_prompt/FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_CORRECTION_2_PROMPT.md`
- **Trạng thái:** Hoàn tất correction lượt 2 — Chuyển giao Reviewer (`final_review`)

---

## 1. Executive Summary (Tóm Lược Điều Hành Cho User)

Báo cáo này được cập nhật theo kết quả thẩm định độc lập tại mục 6–7 của [`reports/full_corpus_rag_old_0_evaluation_simplicity_survey_codex_review_2026_09_10.md`](file:///home/minhhieu/hue_rag/reports/full_corpus_rag_old_0_evaluation_simplicity_survey_codex_review_2026_09_10.md). Các nội dung đã PASS tại lượt 1 (C1 về kiểm kê/số dòng và C4 về giọng điệu trung tính/bỏ phần trăm không căn cứ) được giữ nguyên vẹn; bản cập nhật này tập trung xử lý dứt điểm các sai sót tham chiếu dòng mã nguồn (C2), đồng bộ triệt để với các quyết định canonical về schema (C3), chuẩn hóa định nghĩa phạm vi đo lường của evidence groups, và tinh chỉnh kết luận về tính tái lập (C5).

### Những kết luận kỹ thuật trọng tâm:

1. **Bản chất của các metric trong `rag_old_0`:**
   - Cụm từ "Retrieval Evaluation" là tên nhánh đánh giá truy xuất, không phải tên metric. Nhánh này gồm **3 metric thực tế**: **MRR (Mean Reciprocal Rank)**, **nDCG@10 (Normalized Discounted Cumulative Gain tại $k=10$)**, và **Keyword Coverage**. Cả 3 metric này đều vận hành dựa trên cơ chế **so khớp chuỗi con từ khóa đại diện (keyword substring matching proxy)** (`keyword.lower() in doc.page_content.lower()`).
   - Nhánh "Answer Evaluation" gồm **3 metric thực tế**: **Accuracy (Độ chính xác)**, **Completeness (Độ đầy đủ)**, và **Relevance (Độ liên quan)**, được chấm theo thang điểm 1 đến 5 bởi mô hình giám khảo LLM-as-a-judge (`evaluate_answer`) thông qua việc đối chiếu câu trả lời sinh ra với câu trả lời mẫu mà không nhận ngữ cảnh văn bản gốc.
2. **Yêu cầu dữ liệu tối thiểu để tính đúng 6 metrics của `rag_old_0`:**
   - Để tính toán đầy đủ và chính xác toàn bộ 6 metric trên, **chỉ cần 3 trường dữ liệu bắt buộc**:
     - `question`: Truy vấn đầu vào cho cả truy xuất và sinh câu trả lời.
     - `keywords`: Danh sách từ khóa đại diện để kiểm tra sự xuất hiện trong tài liệu truy xuất (phục vụ MRR, nDCG@10, Coverage).
     - `reference_answer`: Căn cứ đối chiếu duy nhất để LLM Judge chấm điểm Accuracy, Completeness và Relevance.
   - Trường `category` **chỉ phục vụ thống kê phân nhóm**: Trong mã nguồn, trường này không tham gia vào việc tính điểm của từng test case mà chỉ dùng để tính trung bình và vẽ biểu đồ thanh cho MRR và Accuracy trong dashboard (`evaluator.py`, `evaluator2.py`). Trường này là **tùy chọn (optional)** trong schema đích nếu loader và hệ thống báo cáo cho phép thiếu.
   - Trường `case_id` **hoàn toàn không có consumer** trong `rag_old_0` (mã nguồn dùng chỉ số mảng $0 \dots 149$). Nếu đưa vào Hue RAG, `case_id` chỉ đóng vai trò là một **định danh vận hành đề xuất (proposed operational identifier)** nhằm hỗ trợ ghi log và so sánh diff giữa các lần chạy kiểm thử.
3. **Phân định ranh giới giữa 6 metrics của `rag_old_0` và các yêu cầu khác của Hue RAG:**
   - Đối với 6 metric của `rag_old_0`, các trường như `evidence_groups` và `expected_claims` **hoàn toàn không có hàm nào tiêu thụ**.
   - Tuy nhiên, điều này **không đồng nghĩa** với việc các trường bằng chứng là vô ích. Các trường này phục vụ các **yêu cầu kỹ thuật riêng biệt đã chốt trước đây của Hue RAG**: (a) kiểm chứng trích dẫn nguồn thật (citation verification), (b) đánh giá độ đầy đủ và độ phủ truy xuất (retrieval coverage / completeness) đối với các luận điểm đã khai báo trong ground truth, và (c) kiểm tra tính bám sát nguồn tránh ảo giác (claim-source support / groundedness).
   - Khảo sát không quyết định thay User mà phân định rành mạch hai phạm vi để User đưa ra quyết định kiến trúc: giữ nguyên yêu cầu kiểm chứng trích dẫn/groundedness hay chuyển hoàn toàn sang bộ metric tối giản kiểu `rag_old_0`.
4. **Hiệu chỉnh kỹ thuật về Source Span và Chunk ID:**
   - Khi thay đổi chiến lược chunking (ví dụ chuyển từ fixed-size chunking sang semantic chunking), các `chunk_id` sẽ thay đổi.
   - Ngược lại, **source-level exact LF spans** (chuỗi văn bản nguồn, đường dẫn file Markdown, heading path và vị trí offset trên văn bản gốc chuẩn hóa LF) **không bị thay đổi khi rechunking**. Chúng chỉ thay đổi khi nội dung văn bản nguồn gốc bị chỉnh sửa.

---

## 2. Bản Đồ Khảo Sát & Kiểm Kê File (Coverage Map & Inventory — Đã PASS)

Thư mục khảo sát `/home/minhhieu/llm_rag/tai_lieu/rag_old_0` chứa đúng **96 file** (không có file ẩn `.*`). Toàn bộ số dòng được thống kê nhất quán theo quy chuẩn dòng lệnh chuẩn (`wc -l`):

### 2.1. Danh Sách 20 File First-Party Non-Data Được Đọc Toàn Văn 100% (Tổng cộng 10,344 dòng)

| STT | Tên file | Số dòng (`wc -l`) | Kích thước | Phân loại & Vai trò chức năng trong repo |
|:---:|---|:---:|:---:|---|
| 1 | `evaluation/test.py` | 24 | 694 B | Model dữ liệu `TestQuestion` (Pydantic) và hàm nạp `load_tests()`. |
| 2 | `evaluation/eval.py` | 249 | 9,475 B | Logic toán học cho 6 metric: MRR, nDCG@10, Coverage, LLM Judge (Accuracy, Completeness, Relevance). |
| 3 | `evaluation/tests.jsonl` | 150 | 38,985 B | 150 test cases chuẩn, mỗi dòng gồm 4 trường (`question`, `keywords`, `reference_answer`, `category`). |
| 4 | `implementation/answer.py` | 59 | 2,133 B | Pipeline trả lời câu hỏi cơ bản (Basic RAG) dùng LangChain & MiniLM. |
| 5 | `implementation/ingest.py` | 65 | 2,423 B | Pipeline nạp dữ liệu cơ bản: cắt chunk thô 1000/200, nạp vào Chroma `vector_db`. |
| 6 | `pro_implementation/answer.py` | 145 | 5,502 B | Pipeline nâng cao: Native Chroma, Query Rewriting, Dual Retrieval, LLM Reranking. |
| 7 | `pro_implementation/ingest.py` | 146 | 5,856 B | Pipeline nạp nâng cao: LLM Semantic Chunking (headline + summary), Multiprocessing. |
| 8 | `app.py` | 61 | 2,130 B | Ứng dụng giao diện Gradio Chat tương tác trực tiếp với người dùng. |
| 9 | `evaluator.py` | 236 | 10,131 B | Dashboard Gradio đơn luồng; thực hiện tổng hợp điểm và vẽ biểu đồ category cho MRR và Accuracy. |
| 10 | `evaluator2.py` | 372 | 16,913 B | Dashboard Gradio đa luồng (`ThreadPoolExecutor`), cấu hình best-effort seed=42 và thanh trượt concurrency. |
| 11 | `phien_am_bai_hoc/day1.txt` | 365 | 22,668 B | Phiên âm Day 1: Ý niệm RAG, Dictionary keyword matching vs Vector Store. |
| 12 | `phien_am_bai_hoc/day2.txt` | 250 | 16,042 B | Phiên âm Day 2: LangChain loader, TextSplitter, Embedding MiniLM, trực quan hóa t-SNE. |
| 13 | `phien_am_bai_hoc/day3.txt` | 272 | 16,930 B | Phiên âm Day 3: Kết nối Retriever và LLM, hạn chế của ngữ cảnh bị cắt khúc. |
| 14 | `phien_am_bai_hoc/day4.txt` | 811 | 48,154 B | Phiên âm Day 4: Triết lý Evaluation là North Star, công thức MRR, nDCG, LLM Judge, số liệu baseline. |
| 15 | `phien_am_bai_hoc/day5.txt` | 745 | 45,556 B | Phiên âm Day 5: Kiến trúc PRO, Semantic chunking, Reranking, Query Rewriting, số liệu cải tiến. |
| 16 | `day1.ipynb` | 490 | 37,831 B | Sổ tay Day 1: Xây dựng RAG sơ khởi bằng tra cứu từ khóa trong từ điển Python. |
| 17 | `day2.ipynb` | 428 | 20,482 B | Sổ tay Day 2: Thực hành LangChain chunking và trực quan hóa vector space 2D/3D. |
| 18 | `day3.ipynb` | 270 | 13,208 B | Sổ tay Day 3: Kết nối Retriever và ChatOpenAI qua ChatInterface của Gradio. |
| 19 | `day4.ipynb` | 301 | 12,030 B | Sổ tay Day 4: Minh họa chạy thử nghiệm đánh giá trên 1 test case đơn lẻ (`tests[0]`). |
| 20 | `day5.ipynb` | 4,905 | 304,925 B | Sổ tay Day 5: Triển khai PRO RAG và lưu vết các lệnh gọi truy vấn thử nghiệm đơn lẻ. |
| **Tổng** | **20 files** | **10,344** | **604,089 B** | Toàn bộ first-party non-data source đã đọc đầy đủ theo hợp đồng. |

### 2.2. Phân Bố 150 Test Cases Trong `evaluation/tests.jsonl`

Tất cả 150 câu hỏi đều có đầy đủ 4 trường (`question`, `keywords`, `reference_answer`, `category`), phân bổ theo 7 thể loại:
- `direct_fact`: 70 câu
- `temporal`: 20 câu
- `spanning`: 20 câu
- `comparative`: 10 câu
- `numerical`: 10 câu
- `relationship`: 10 câu
- `holistic`: 10 câu

### 2.3. Kiểm Kê (Inventory-Only) 76 File Dữ Liệu Knowledge Base (Không Đọc Nội Dung)

Các file dữ liệu nghiệp vụ tiếng Anh trong `knowledge-base/` chỉ được kiểm kê danh mục, không đọc nội dung chi tiết:
- **`knowledge-base/company/` (4 files):** `about.md`, `careers.md`, `culture.md`, `overview.md`.
- **`knowledge-base/products/` (8 files):** `Bizllm.md`, `Carllm.md`, `Claimllm.md`, `Healthllm.md`, `Homellm.md`, `Lifellm.md`, `Markellm.md`, `Rellm.md`.
- **`knowledge-base/contracts/` (32 files):** Danh sách 32 văn bản hợp đồng B2B có thật trong thư mục, ví dụ:
  - `knowledge-base/contracts/Contract with Advantage Medical Coverage for Healthllm.md`
  - `knowledge-base/contracts/Contract with Apex Reinsurance for Rellm - AI-Powered Enterprise Reinsurance Solution.md`
  - `knowledge-base/contracts/Contract with Atlantic Risk Solutions for Bizllm.md`
  - `knowledge-base/contracts/Contract with GlobalRe Partners for Rellm.md`
  - `knowledge-base/contracts/Contract with SafeHaven Property Insurance for Homellm.md`
  - `knowledge-base/contracts/Contract with United Healthcare Alliance for Healthllm.md` (và 26 hợp đồng khác).
- **`knowledge-base/employees/` (32 files):** Danh sách 32 hồ sơ nhân sự có thật trong thư mục, ví dụ:
  - `knowledge-base/employees/Alex Chen.md`
  - `knowledge-base/employees/Amanda Foster.md`
  - `knowledge-base/employees/Avery Lancaster.md`
  - `knowledge-base/employees/Maxine Thompson.md`
  - `knowledge-base/employees/Priya Sharma.md`
  - `knowledge-base/employees/Tyler Brooks.md` (và 26 nhân sự khác; nhân sự mang họ Brooks là `Tyler Brooks`, không có `Zachary Brooks`).

### 2.4. Các Thành Phần Nằm Ngoài Phạm Vi Hoặc Bỏ Qua (Skipped Artifacts)

- Tệp `.env` (bảo mật khóa API, không đọc).
- Môi trường ảo `.venv/`, thư mục cache `__pycache__/`, `.ipynb_checkpoints/`.
- Không thực hiện lệnh ghi Git, không truy cập internet, không chạy sub-agent.

---

## 3. Kiến Trúc Luồng Dữ Liệu Đánh Giá (Architectural Data Flow & Exact Signatures)

Hệ thống đánh giá của `rag_old_0` phân tách thành hai nhánh độc lập tại `evaluation/eval.py`. Trong mã nguồn hiện hành, `evaluation/eval.py` import trực tiếp implementation PRO:
```python
# evaluation/eval.py:8-9
#from implementation.answer import answer_question, fetch_context
from pro_implementation.answer import answer_question, fetch_context
```

### 3.1. Luồng Dữ Liệu Nhánh 1: Đánh Giá Truy Xuất (Retrieval Evaluation)

- **Hàm thực thi và chữ ký (Signature):**
  ```python
  def evaluate_retrieval(test: TestQuestion, k: int = 10) -> RetrievalEval:
  ```
  *(Tham chiếu: [`evaluation/eval.py:81`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L81))*
  - Hàm **không** có tham số dependency injection cho `fetch_context`. Hàm trực tiếp gọi hàm `fetch_context(test.question)` được import ở đầu tệp từ `pro_implementation.answer` ([`eval.py:9`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L9)).
  - Tham số `k` (mặc định = 10) **chỉ được truyền vào hàm tính nDCG** (`calculate_ndcg(keyword, retrieved_docs, k)` tại dòng 100); nó **không điều khiển** số lượng tài liệu mà `fetch_context` truy xuất.
- **Quy trình truy xuất trong `pro_implementation/answer.py`:**
  - `fetch_context(question)` gọi `fetch_context_unranked` với `RETRIEVAL_K = 20` ([`pro_implementation/answer.py:21`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation/answer.py#L21)) cho câu hỏi gốc và câu hỏi đã viết lại (`rewrite_query`), gộp kết quả qua `merge_chunks`, đưa vào `rerank` và **cắt lấy đúng 10 tài liệu cuối cùng (`FINAL_K = 10`)** ([`pro_implementation/answer.py:22, 126-133`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation/answer.py#L126-L133)).
  - Do đó, danh sách `retrieved_docs` mà `evaluate_retrieval` nhận được luôn có độ dài tối đa là 10 tài liệu.
- **Tính toán 3 metric per-keyword:**
  1. *MRR:* Gọi `calculate_mrr(keyword, retrieved_docs)` ([`eval.py:45-51`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L45-L51)). Duyệt qua toàn bộ danh sách tài liệu trả về. Nếu tìm thấy `keyword.lower() in doc.page_content.lower()`, gán điểm $1.0 / rank$. Nếu không có, điểm là $0.0$. Điểm MRR của câu hỏi được tổng hợp bằng trung bình cộng các từ khóa tại [`eval.py:96-97`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L96-L97).
  2. *nDCG@10:* Gọi `calculate_ndcg(keyword, retrieved_docs, k)` ([`eval.py:62-78`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L62-L78)) sử dụng hàm phụ trợ `calculate_dcg` ([`eval.py:54-59`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L54-L59)). Lấy `retrieved_docs[:k]`, tạo vector nhị phân 0/1, tính DCG và IDCG theo công thức discounted gain. Điểm nDCG của câu hỏi được tổng hợp tại [`eval.py:100-101`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L100-L101).
  3. *Coverage:* Đếm số lượng từ khóa có $MRR > 0$, chia cho tổng số từ khóa của test case $\times 100\%$ ([`eval.py:104-106`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L104-L106)).
- **Đầu ra:** Trả về `RetrievalEval(mrr=avg_mrr, ndcg=avg_ndcg, keywords_found=..., total_keywords=..., keyword_coverage=...)` ([`eval.py:108-113`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L108-L113)).
- **Trường dữ liệu tiêu thụ:** Duy nhất **`test.question`** và **`test.keywords`**.

### 3.2. Luồng Dữ Liệu Nhánh 2: Đánh Giá Câu Trả Lời (Answer Evaluation)

- **Hàm thực thi và chữ ký (Signature):**
  ```python
  def evaluate_answer(test: TestQuestion) -> tuple[AnswerEval, str, list]:
  ```
  *(Tham chiếu: [`evaluation/eval.py:117`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L117))*
  - Hàm **không** có tham số dependency injection cho `answer_question`. Hàm trực tiếp gọi hàm `answer_question(test.question)` được import từ `pro_implementation.answer` ([`eval.py:9, 128`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L128)).
  - Kết quả trả về gồm `generated_answer` (chuỗi câu trả lời) và `retrieved_docs` (danh sách tài liệu đã dùng để trả lời).
- **Quy trình giám khảo LLM (LLM-as-a-judge):**
  - Prompt gửi tới mô hình (`MODEL = "gpt-5-nano"` qua LiteLLM `completion` với `response_format=AnswerEval` tại [`eval.py:157`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L157)) gồm:
    - `system_prompt` ([`eval.py:133-135`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L133-L135)): Định nghĩa vai trò giám khảo đánh giá chất lượng câu trả lời bằng cách so sánh câu trả lời sinh ra với câu trả lời mẫu.
    - `user_prompt` ([`eval.py:137-154`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L137-L154)):
      ```text
      Question: {test.question}
      Generated Answer: {generated_answer}
      Reference Answer: {test.reference_answer}
      ```
  - **Lưu ý quan trọng:** `retrieved_docs` (context tài liệu) **không được đưa vào prompt của LLM Judge**. LLM Judge chỉ so sánh trực tiếp văn bản của `generated_answer` với `test.reference_answer`.
- **Đầu ra:** Trả về bộ 3 giá trị: `(answer_eval, generated_answer, retrieved_docs)` ([`eval.py:161`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L161)), trong đó `answer_eval` là đối tượng `AnswerEval(feedback: str, accuracy: float, completeness: float, relevance: float)`.
- **Trường dữ liệu tiêu thụ:** Duy nhất **`test.question`** và **`test.reference_answer`**.

### 3.3. Thực Tế Xử Lý Tổng Hợp Và Tiêu Thụ Trường `category`

- **Trong `evaluation/eval.py`:**
  - Hai hàm chạy lô `evaluate_all_retrieval()` ([`eval.py:164-171`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L164-L171)) và `evaluate_all_answers()` ([`eval.py:174-181`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L174-L181)) là các **generator** đơn thuần: Chúng duyệt qua từng test và `yield test, result, progress`. Các hàm này **hoàn toàn không thực hiện tính toán trung bình hay gom nhóm theo category**.
- **Trong `evaluator.py` và `evaluator2.py`:**
  - Toàn bộ logic tổng hợp (aggregation) được thực hiện tại tầng giao diện dashboard:
    - Khởi tạo `category_mrr = defaultdict(list)` tại [`evaluator.py:84`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py#L84) và [`evaluator2.py:132`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L132).
    - Khởi tạo `category_accuracy = defaultdict(list)` tại [`evaluator.py:131`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py#L131) và [`evaluator2.py:216`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L216).
  - **Phạm vi phân rã theo category trên Dashboard:**
    - Giao diện người dùng **chỉ vẽ biểu đồ thanh (bar chart) cho 2 chỉ số**: `Average MRR by Category` ([`evaluator.py:196`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py#L196), [`evaluator2.py:314`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L314)) và `Average Accuracy by Category` ([`evaluator.py:216`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py#L216), [`evaluator2.py:352`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L352)).
    - Bốn chỉ số còn lại (**nDCG@10**, **Keyword Coverage**, **Completeness**, **Relevance**) **không được phân rã theo category** trên giao diện mà chỉ hiển thị dưới dạng điểm trung bình tổng thể toàn bộ tập test trên các thẻ HTML card.

---

## 4. Bảng Phân Tích 6 Chỉ Số Đánh Giá (Metric Breakdown Table)

Dưới đây là chi tiết kỹ thuật của 6 metrics quan sát được trong mã nguồn:

| Tên Metric | Nhánh Đánh Giá | Công Thức / Thuật Toán Trong Mã Nguồn | Trường Dữ Liệu Tiêu Thụ | Miền Giá Trị | Phương Thức Tổng Hợp Quan Sát Được | Giới Hạn Kỹ Thuật Quan Sát Được (Caveats / Limitations) |
|---|---|---|---|:---:|---|---|
| **MRR**<br>*(Mean Reciprocal Rank)* | Retrieval | Với mỗi `kw` $\in$ `keywords`, duyệt `retrieved_docs` (tối đa 10 tài liệu trả về từ PRO), tìm rank $r$ đầu tiên có `kw.lower() in doc.lower()`. Gán $score = \frac{1}{r}$ (hoặc 0 nếu không thấy).<br>$MRR = \text{mean}_{kw}(score)$.<br>Tham chiếu: [`eval.py:45-51`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L45-L51), tổng hợp case: [`eval.py:96-97`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L96-L97) | `question`,<br>`keywords` | $[0.0, 1.0]$ | - Mean trên toàn bộ tập test.<br>- Mean phân rã theo `category` trên dashboard ([`evaluator.py:196`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py#L196), [`evaluator2.py:314`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L314)). | **1. Keyword Proxy:** Chỉ đo lường sự xuất hiện chuỗi con từ khóa, không đo lường tính liên quan ngữ nghĩa thực sự.<br>**2. Bị chặn bởi số tài liệu trả về:** Quét toàn bộ danh sách tài liệu do `fetch_context` cung cấp (ở PRO là 10 docs). |
| **nDCG@10**<br>*(Normalized Discounted Cumulative Gain)* | Retrieval | Với mỗi `kw`, tạo vector nhị phân $rel_i \in \{0, 1\}$ trên `retrieved_docs[:k]` với $k=10$.<br>$DCG = \sum_{i=1}^{10} \frac{rel_i}{\log_2(i+1)}$.<br>$ideal = \text{sorted}(rel, \text{reverse=True})$.<br>$IDCG = \sum_{i=1}^{10} \frac{ideal_i}{\log_2(i+1)}$.<br>$nDCG = \frac{DCG}{IDCG}$ (0 nếu $IDCG=0$).<br>Tham chiếu: [`eval.py:54-59, 62-78`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L62-L78), tổng hợp case: [`eval.py:100-101`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L100-L101) | `question`,<br>`keywords` | $[0.0, 1.0]$ | - Mean trên toàn bộ tập test.<br>- *Không phân rã theo category trên dashboard*. | **Giới hạn $IDCG$ nghiêm trọng:** $IDCG$ được tính bằng cách sắp xếp lại chính các kết quả đã truy xuất được trong top 10, **không dựa trên toàn bộ corpus**. Nếu chỉ có 1 chunk chứa từ khóa và nó nằm ở rank 1, $nDCG = 1.0$ ngay cả khi có 5 chunk liên quan khác trong kho bị bỏ sót hoàn toàn. |
| **Keyword Coverage** | Retrieval | Đếm số lượng từ khóa trong `keywords` có $MRR > 0$, chia cho tổng số từ khóa $\times 100\%$.<br>Tham chiếu: [`eval.py:104-106`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L104-L106) | `keywords` | $[0.0, 100.0]\%$ | - Mean trên toàn bộ tập test.<br>- *Không phân rã theo category trên dashboard*. | Chỉ đo độ phủ bề mặt của danh sách từ khóa đại diện. |
| **Accuracy**<br>*(Độ chính xác)* | Answer | LLM Judge so sánh `generated_answer` với `reference_answer`.<br>Chỉ thị: Nếu câu trả lời sai sự thật so với reference, bắt buộc chấm điểm **1**.<br>Tham chiếu: [`eval.py:148, 152`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L148) | `question`,<br>`reference_answer` | $[1.0, 5.0]$ | - Mean trên toàn bộ tập test.<br>- Mean phân rã theo `category` trên dashboard ([`evaluator.py:216`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py#L216), [`evaluator2.py:352`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L352)). | **Reference-bounded:** Giám khảo không xem context tài liệu gốc. Nếu câu trả lời sinh ra có thêm chi tiết đúng từ tài liệu nhưng không có trong reference, có thể bị trừ điểm vì thông tin chưa kiểm chứng. |
| **Completeness**<br>*(Độ đầy đủ)* | Answer | LLM Judge đánh giá mức độ bao quát: Điểm 5 chỉ khi bao hàm toàn bộ thông tin từ `reference_answer`.<br>Tham chiếu: [`eval.py:149`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L149) | `question`,<br>`reference_answer` | $[1.0, 5.0]$ | - Mean trên toàn bộ tập test.<br>- *Không phân rã theo category trên dashboard*. | Phụ thuộc hoàn toàn vào độ đầy đủ của câu trả lời mẫu biên soạn ban đầu. |
| **Relevance**<br>*(Độ liên quan)* | Answer | LLM Judge đánh giá tính trực tiếp: Trả lời thẳng vào câu hỏi, không lan man, không chứa thông tin thừa.<br>Tham chiếu: [`eval.py:150`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L150) | `question`,<br>`reference_answer` | $[1.0, 5.0]$ | - Mean trên toàn bộ tập test.<br>- *Không phân rã theo category trên dashboard*. | Đo lường độ cô đọng và văn phong phản hồi của mô hình sinh. |

---

## 5. Ma Trận Tiêu Thụ Trường Dữ Liệu & Đối Chiếu Các Trường Canonical Của Hue

### 5.1. Ma Trận Tiêu Thụ Dữ Liệu Thực Tế Trong `rag_old_0`

| Tên Trường Dữ Liệu | Có Trong `tests.jsonl` Của `rag_old_0`? | Observed Consumer Trong Retrieval Eval | Observed Consumer Trong Answer Eval | Observed Consumer Trong Dashboard / Báo Cáo | Mức Độ Cần Thiết Đối Với 6 Metrics Của `rag_old_0` |
|---|:---:|---|---|---|:---:|
| **`question`** | **CÓ** | `fetch_context(test.question)` | - Sinh câu trả lời `answer_question(test.question)`.<br>- Đầu vào cho LLM Judge | Hiển thị chi tiết test case trên giao diện Gradio | **BẮT BUỘC (Required)** |
| **`keywords`** | **CÓ** | So khớp chuỗi `in doc.page_content.lower()` cho MRR, nDCG, Coverage | Không dùng | Không dùng | **BẮT BUỘC (Required)** (cho retrieval proxy) |
| **`reference_answer`** | **CÓ** | Không dùng | Căn cứ đối chiếu duy nhất cho LLM Judge chấm 3 tiêu chí | Hiển thị trên UI để con người đối chiếu | **BẮT BUỘC (Required)** (cho answer eval) |
| **`category`** | **CÓ** | Không dùng trong tính điểm | Không dùng trong tính điểm | Gom nhóm điểm số tính trung bình và vẽ biểu đồ thanh cho MRR và Accuracy | **TÙY CHỌN (Optional)** (cho phân rã thống kê) |
| **`case_id`** | **KHÔNG** | Không có code consumer | Không có code consumer | Hiển thị chỉ số mảng $0 \dots 149$ | **KHÔNG CÓ CONSUMER** trong `rag_old_0` |
| **`evidence_groups` / `expected_claims`** | **KHÔNG** | Không có code consumer | Không có code consumer | Không dùng | **KHÔNG CÓ CONSUMER** đối với 6 metrics này |

### 5.2. Đối Chiếu Toàn Diện Các Trường Dữ Liệu Canonical Của Hue RAG

Bảng dưới đây đối chiếu chi tiết từng trường dữ liệu với các quyết định canonical đã chốt tại [`guides/full_corpus_rag.md:38-64`](file:///home/minhhieu/hue_rag/guides/full_corpus_rag.md#L38-L64):

| Trường Canonical | Observed Consumer Trong `rag_old_0` | Quyết Định Canonical Tại `guides/full_corpus_rag.md` | Requirement Phục Vụ Trong Dự Án Hue | Khả Năng Suy Luận Tất Định (Derivation) Hoặc Lưu Trữ |
|---|---|---|---|---|
| **`question`** | `fetch_context`, `answer_question`, `eval.py` | Bắt buộc lưu trên từng record | Đầu vào trực tiếp cho Retriever, Generator và Judge. | **Bắt buộc lưu**. Không thể suy luận. |
| **`keywords`** | So khớp chuỗi cho MRR, nDCG@10, Coverage | Bắt buộc lưu trên từng record (nhưng không thay thế evidence) | Đo lường truy xuất theo cơ chế keyword substring proxy kiểu `rag_old_0`. | **Bắt buộc lưu**. Không thể suy luận. |
| **`reference_answer`** | Căn cứ đối chiếu cho LLM Judge | Bắt buộc lưu trên từng record | Căn cứ chấm Accuracy, Completeness, Relevance và thẩm định của con người. | **Bắt buộc lưu**. Không thể suy luận. |
| **`expected_claims`** | **Không có** | Bắt buộc lưu trên từng record (mỗi claim có trường `text` và `evidence_groups`) | Đánh giá độ phủ truy xuất (retrieval coverage) và kiểm tra tính bám sát nguồn (groundedness) ở mức từng luận điểm. | **Bắt buộc lưu theo canonical**. Không thể suy luận từ các trường khác. |
| **`category`** | Gom nhóm tính trung bình MRR và Accuracy trên dashboard | Field tùy chọn (optional), chỉ phục vụ diagnostic statistics | Phân rã báo cáo chẩn đoán theo dạng câu hỏi (factual, temporal, comparative...). | **Tùy chọn**. Không thể suy luận; có thể bỏ nếu không cần phân rã chẩn đoán. |
| **`case_id`** | **Không có** (dùng array index) | Bắt buộc lưu trên từng record | Khóa định danh duy nhất cho từng ca kiểm thử, phục vụ logging, benchmark mapping và error tracking. | **Bắt buộc lưu theo canonical**. Không có consumer trong 6 metric gốc của `rag_old_0`; là định danh vận hành của Hue RAG. |
| **`claim_id`** | **Không có** | **Không lưu trong JSONL canonical** | Định danh luận điểm khi sinh báo cáo chi tiết. | **Không lưu**. Được derive tại thời điểm đánh giá từ `case_id` kết hợp số thứ tự (ordinal) của claim. |
| **`evidence_groups`** | **Không có** | Bắt buộc lưu bên trong từng claim theo Phương án C | Biểu diễn quan hệ logic OR/AND giữa các nhóm bằng chứng để kiểm tra trích dẫn và đo lường độ phủ truy xuất tài liệu nguồn. | **Bắt buộc lưu theo canonical**. Không thể suy luận. |
| **`case_type`** | **Không có** | **Không lưu trong canonical** | Đề xuất phân loại ca kiểm thử trước đây. | **Loại bỏ theo canonical**: Retrieval metrics không consume trường này; chất lượng câu trả lời được đo qua `reference_answer` và `expected_claims`. |
| **`domain`** | **Không có** | **Không lưu trong canonical** | Phân nhóm theo 5 domain sản phẩm của Huế. | **Loại bỏ theo canonical**: Không có consumer trong code; nếu cần thống kê có thể suy luận từ authoring partition hoặc đường dẫn nguồn tài liệu trong evidence. |
| **`partition`** | **Không có** | **Chỉ tồn tại trong authoring/review P7, bị loại bỏ (strip) khi merge** | Quản lý quy trình biên soạn độc lập giữa 7 phân vùng P7. | **Không tồn tại trong canonical JSONL**: Bị loại bỏ hoàn toàn khi merge vào tệp canonical chính. |

---

## 6. So Sánh Kiến Trúc, Benchmark Attribution Và Giới Hạn Tái Lập

### 6.1. So Sánh Kiến Trúc Basic vs PRO

| Thành phần kỹ thuật | Basic RAG (Days 2 & 3) | PRO RAG (Day 5) |
|---|---|---|
| **Framework** | LangChain (`DirectoryLoader`, `RecursiveCharacterTextSplitter`, `Chroma`). | **Native Python** kết hợp Pydantic và Chroma PersistentClient trực tiếp. |
| **Chiến lược Chunking** | Cắt thô theo ký tự: `chunk_size=1000`, `chunk_overlap=200` $\rightarrow$ 413 chunks. | **LLM Semantic Chunking**: Dùng LLM tạo Pydantic `Chunk(headline, summary, original_text)` $\rightarrow$ 543 chunks. Ghép cả 3 trường khi vector hóa giúp bao quát ngữ nghĩa. |
| **Embedding Model** | HuggingFace `all-MiniLM-L6-v2` (384 dimensions). | OpenAI `text-embedding-3-large` (3072 dimensions). |
| **Truy vấn (Querying)** | Truy vấn đơn nguyên văn câu hỏi người dùng. | **Query Rewriting & Dual Retrieval**: Viết lại câu hỏi, truy vấn đồng thời câu hỏi gốc và câu hỏi viết lại với `RETRIEVAL_K=20`, sau đó hợp nhất (`merge_chunks`). |
| **Xếp hạng lại (Reranking)** | Không có reranking. | **LLM Reranking**: Dùng `gpt-5-nano` với cấu trúc `RankOrder(order: list[int])` sắp xếp lại và cắt lấy `FINAL_K=10`. |

### 6.2. Đối Chiếu Benchmark Nguồn (Benchmark Attribution)

Các số liệu cải tiến được ghi nhận trong tài liệu tham chiếu cần được dẫn chứng chính xác theo nguồn gốc văn bản thay vì suy diễn:

- **Các số liệu tìm thấy trong bản phiên âm bài giảng (Transcripts):**
  - **Baseline (Day 4):** MRR ban đầu đạt **0.7298** với chunk size 1000 và $k=5$ ([`phien_am_bai_hoc/day4.txt:698`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day4.txt#L698)). Điểm Accuracy ban đầu được nhắc đến ở mức **3.99** ([`day4.txt:669`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day4.txt#L669)).
  - **Thử nghiệm tối ưu (Day 4):** Khi thử nghiệm chunk size 1667 và $k=3$, MRR đạt **0.7475** ([`day4.txt:700`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day4.txt#L700)). Khi nâng cấp lên `text-embedding-3-large`, MRR đạt đỉnh **0.7903** ([`day4.txt:756`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day4.txt#L756)), Accuracy tăng lên 4.21 và Completeness tăng lên 4.05 ([`day4.txt:757`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day4.txt#L757)).
  - **PRO RAG (Day 5):** Khi kết hợp Semantic Chunking, Query Rewriting và LLM Reranking, MRR được giảng viên công bố đạt **0.9116** ([`phien_am_bai_hoc/day5.txt:648`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day5.txt#L648)) và Accuracy tăng lên **4.62/5.0** ([`day5.txt:602`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day5.txt#L602)).
- **Thực tế lưu trữ trong các Sổ tay Jupyter (Saved Notebooks):**
  - Khảo sát xác nhận rằng các con số benchmark tổng hợp trên **không được lưu trữ dưới dạng bảng kết quả toàn cục trong các notebook**.
  - `day4.ipynb` chỉ lưu vết kết quả chạy của duy nhất 1 ca kiểm thử mẫu (`tests[0]`, câu hỏi về Maxine Thompson và giải thưởng IIOTY tại các dòng 130-170).
  - `day5.ipynb` chỉ lưu vết thực thi của các truy vấn thăm dò đơn lẻ ("Who won the IIOTY award?", "Who went to Manchester University?" tại các ô code cuối dòng 4470-4870), không chứa bảng chạy toàn bộ 150 câu hỏi.
  - Các chỉ số như *Keyword Coverage 97.8%*, *Completeness 4.55*, hay *Relevance 4.71* **hoàn toàn không tìm thấy trong văn bản của 20 file non-data** và do đó đã bị loại bỏ khỏi báo cáo.
- **Về việc tái sử dụng Test Harness:**
  - Diễn tiến khóa học (course narrative) cho thấy module đánh giá (`evaluation/eval.py`) được thiết kế để tái sử dụng giữa Basic và PRO thông qua việc thay đổi lệnh import từ `implementation.answer` sang `pro_implementation.answer`.
  - Đây là một quyết định thiết kế phần mềm quan sát thấy trong giáo trình nhằm so sánh trên cùng một thước đo, không phải là bằng chứng cho thấy tính tối giản của bộ test là nguyên nhân tạo ra sự cải thiện điểm số của pipeline RAG.

### 6.3. Giới Hạn Tái Lập (Reproducibility), Seed, Temperature Và Ngưỡng Màu Dashboard

- **Cấu hình tái lập (Reproducibility):**
  - Trong module đánh giá cốt lõi (`evaluation/eval.py`), lệnh gọi giám khảo LLM Judge (`completion(model=MODEL, messages=judge_messages, response_format=AnswerEval)` tại dòng 157) **không thiết lập tham số `temperature`**, **không thiết lập `seed`**, và **chỉ thực hiện đúng 1 lần gọi (single repetition)** mà không có cơ chế lặp lại hay bỏ phiếu đa số.
  - Tệp `evaluator2.py` có cài đặt cơ chế tái lập dạng *best-effort* ([`evaluator2.py:41-60`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L41-L60)) bằng cách gán `SEED = 42` cho `random`, `numpy.random`, monkey-patching `completion` để chèn `kwargs.setdefault("seed", seed)`, và thiết lập `ChatOpenAI(temperature=0, seed=seed)`.
  - Do cấu hình `seed=42` tại `evaluator2.py` chỉ mang tính chất best-effort và bản thân core evaluator không cung cấp cơ chế kiểm soát nhiệt độ hay chạy lặp lại, việc chạy đánh giá một lần duy nhất với LLM Judge không cung cấp sự bảo đảm tất định (no deterministic guarantee).
- **Ngưỡng màu trực quan hóa trên Dashboard (Color Coding Thresholds):**
  - Tại [`evaluator.py:10-20`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator.py#L10-L20) và [`evaluator2.py:28-38`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L28-L38), mã nguồn định nghĩa các ngưỡng màu phục vụ hiển thị giao diện:
    - *Nhánh Retrieval:*
      - MRR: Xanh ($\ge 0.90$), Hổ phách/Vàng ($0.75 \le x < 0.90$), Đỏ ($< 0.75$).
      - nDCG: Xanh ($\ge 0.90$), Hổ phách/Vàng ($0.75 \le x < 0.90$), Đỏ ($< 0.75$).
      - Coverage: Xanh ($\ge 90.0\%$), Hổ phách/Vàng ($75.0\% \le x < 90.0\%$), Đỏ ($< 75.0\%$).
    - *Nhánh Answer (Thang điểm 1-5):*
      - Accuracy, Completeness, Relevance: Xanh ($\ge 4.5$), Hổ phách/Vàng ($4.0 \le x < 4.5$), Đỏ ($< 4.0$).
  - **Lưu ý kỹ thuật:** Các ngưỡng trên **chỉ là quy ước màu sắc trực quan (UI color coding thresholds)** trong dashboard, không phải là các cổng chấp nhận (acceptance gates) mang tính ràng buộc tự động ngắt dừng hệ thống trong mã nguồn.

---

## 7. Đề Xuất Các Phương Án Schema Cho Hue RAG & Phân Tích Trade-Off

Để User có đầy đủ cơ sở đưa ra quyết định, báo cáo xây dựng 3 phương án schema minh họa:

### Ứng Viên A: Baseline Tối Thiểu Theo Metric (3 Trường Bắt Buộc, Category Tùy Chọn)

Phương án này phản ánh đúng và đủ dữ liệu cần thiết để chạy 6 metric của `rag_old_0`:
```json
{
  "question": "Lăng Tự Đức được xây dựng trong khoảng thời gian nào?",
  "keywords": ["Lăng Tự Đức", "xây dựng", "1864", "1867", "Khiêm Lăng"],
  "reference_answer": "Lăng Tự Đức (Khiêm Lăng) được xây dựng từ năm 1864 đến năm 1867 dưới thời vua Tự Đức.",
  "category": "temporal"
}
```
- **Các trường bắt buộc (Mandatory):** `question`, `keywords`, `reference_answer`.
- **Trường tùy chọn (Optional):** `category` (chỉ cần thiết nếu hệ thống muốn duy trì phân rã thống kê trung bình MRR và Accuracy theo nhóm câu hỏi; có thể bỏ nếu loader cho phép).
- **Observed Consumers:** 100% các trường bắt buộc đều có code tiêu thụ trực tiếp trong `eval.py`.
- **Đánh giá:** Đây là mức tinh giản tối đa về mặt dữ liệu đánh giá, sao chép trọn vẹn triết lý đo lường của `rag_old_0`.

---

### Ứng Viên B: Schema Có Bổ Sung Định Danh Vận Hành Đề Xuất (`case_id`)

Phương án này bổ sung mã định danh vận hành cho quy trình kiểm thử phần mềm của Hue RAG:
```json
{
  "case_id": "HUE_TEMP_001",
  "question": "Lăng Tự Đức được xây dựng trong khoảng thời gian nào?",
  "keywords": ["Lăng Tự Đức", "xây dựng", "1864", "1867", "Khiêm Lăng"],
  "reference_answer": "Lăng Tự Đức (Khiêm Lăng) được xây dựng từ năm 1864 đến năm 1867 dưới thời vua Tự Đức.",
  "category": "temporal"
}
```
- **Phân loại vai trò của `case_id`:**
  - *Observed Consumer trong `rag_old_0`:* **Không có**.
  - *Proposed Consumer trong Hue RAG:* Đóng vai trò là khóa định danh phục vụ kỹ nghệ vận hành (logging, error reporting, đối chiếu regression diff giữa các phiên bản khi số lượng test case tăng lên).
- **Lưu ý trung thực về trade-off:**
  - Việc đưa thêm `case_id` đòi hỏi kỷ luật biên tập và quy tắc đặt tên nhất quán của nhóm phát triển (có chi phí quản lý vận hành nhất định).
  - Định danh `case_id` không mang tính bất biến vĩnh viễn nếu cấu trúc phân loại của dự án thay đổi sau này.

---

### Ứng Viên C: Schema Minh Họa Tích Hợp Yêu Cầu Kiểm Chứng Nguồn & Groundedness

Phương án này tích hợp các yêu cầu đã chốt tại `guides/full_corpus_rag.md` về kiểm chứng trích dẫn và bám sát nguồn:
```json
{
  "case_id": "HUE_TEMP_001",
  "question": "Lăng Tự Đức được xây dựng trong khoảng thời gian nào?",
  "keywords": ["Lăng Tự Đức", "xây dựng", "1864", "1867"],
  "reference_answer": "Lăng Tự Đức (Khiêm Lăng) được xây dựng từ năm 1864 đến năm 1867 dưới thời vua Tự Đức.",
  "category": "temporal",
  "expected_claims": [
    {
      "text": "Lăng Tự Đức được xây dựng từ năm 1864 đến năm 1867.",
      "evidence_groups": [
        [
          {
            "source": "heritages/monuments/lang_tu_duc.md",
            "heading_path": "Lịch sử xây dựng",
            "start": 120,
            "end": 285,
            "text": "Công trình được khởi công xây dựng vào năm 1864 và hoàn thành vào năm 1867..."
          }
        ]
      ]
    }
  ]
}
```
- **Đặc điểm schema:**
  - Không lưu `claim_id` trong JSONL: Được suy luận tất định (derived) tại thời điểm đánh giá từ `case_id` và số thứ tự của claim.
  - Thuộc tính mô tả luận điểm dùng khóa `text` (không dùng `claim_text`).
  - Không lưu `case_type` và không lưu `domain` theo đúng quyết định canonical.
  - *Lưu ý quan trọng:* Cú pháp `evidence_groups` ở trên chỉ mang tính chất minh họa (`illustrative only`), cú pháp và ngữ nghĩa chi tiết vẫn là điểm thiết kế chưa chốt (unresolved design point) chờ Reviewer và User quy định trong written spec.
- **Mục đích phục vụ:** Không phục vụ cho 6 metric của `rag_old_0`, mà phục vụ các bài toán: (a) Citation Verification (đối chiếu câu trả lời có trích dẫn đúng nguồn không), (b) Claim-level Groundedness (phát hiện ảo giác ở từng ý nhỏ), và (c) đo lường độ phủ truy xuất (retrieval coverage / completeness) đối với các expected claims và evidence groups đã được khai báo trong ground truth (lưu ý: không đồng nghĩa với nhãn exhaustive cho toàn bộ kho tài liệu).
- **Trade-off:**
  - *Ưu điểm:* Đảm bảo độ tin cậy học thuật cao, hỗ trợ kiểm toán tự động sự thật văn hóa lịch sử Huế.
  - *Nhược điểm:* Đòi hỏi công sức biên soạn và rà soát thủ công rất lớn khi tạo lập tập dữ liệu Golden.

---

## 8. Phân Tích Thiết Lập Lại Tính Tối Giản (Complexity Reset Analysis)

Dựa trên kết quả đối chiếu giữa `rag_old_0` và nhu cầu của Hue RAG, các lựa chọn kỹ thuật được phân loại rõ ràng:

### 8.1. Nếu Mục Tiêu Là Tối Giản Hóa Tuyệt Đối Theo Phong Cách `rag_old_0`
- **Áp dụng Ứng viên A hoặc B:** Chỉ lưu 3 trường dữ liệu bắt buộc (`question`, `keywords`, `reference_answer`), giữ `category` ở mức tùy chọn nếu muốn phân rã thống kê, và cân nhắc bổ sung `case_id` chỉ khi nhóm phát triển có nhu cầu tracking vận hành cụ thể.
- **Lược bỏ:** Toàn bộ cấu trúc `expected_claims`, `evidence_groups`, tọa độ ký tự và chunk ID. Hệ thống đo lường retrieval thuần túy qua sự xuất hiện của từ khóa đại diện và đo lường câu trả lời qua LLM Judge đối chiếu với câu trả lời mẫu.

### 8.2. Nếu User Muốn Giữ Lại Yêu Cầu Kiểm Chứng Trích Dẫn Và Groundedness
- **Áp dụng Ứng viên C:** Cần giữ lại `expected_claims` và `evidence_groups` theo quy định tại `guides/full_corpus_rag.md`.
- **Làm rõ kỹ thuật về Source Span và Ground Truth:** Cần hiểu đúng rằng các đoạn trích dẫn văn bản nguồn chuẩn hóa LF (`source`, `heading_path`, `start`, `end`, `text`) **hoàn toàn độc lập với thuật toán chunking** và không bị mất giá trị khi thay đổi kích thước chunk hay phương pháp chia đoạn. Việc khai báo expected claims và evidence groups cung cấp thước đo độ đầy đủ truy xuất (coverage/completeness) trong phạm vi các bằng chứng đã được gán nhãn, chứ không tự tạo ra nhãn exhaustive cho toàn bộ mọi chunk trong kho dữ liệu.

---

## 9. Khoảng Trống Bằng Chứng, Giới Hạn Khảo Sát & Bàn Giao Reviewer

### 9.1. Giới Hạn Khảo Sát (Intentionally Skipped / Not Verified)
- Khảo sát tuân thủ 100% nguyên tắc read-only: Không chạy mã nguồn Python, script, notebook, mô hình, API, Qdrant, tests hay benchmark.
- Không đọc tệp cấu hình bảo mật `.env`, không sử dụng mạng ngoài, không ghi Git, không kích hoạt sub-agent.
- Không đọc nội dung chi tiết của 76 tệp dữ liệu tiếng Anh trong `knowledge-base/` (đã kiểm kê đúng số lượng và đường dẫn thực tế).
- Implementer không tự đưa ra quyết định thay thế các quyết định kiến trúc đã chốt của User, không tự claim `PASS`, approval hay closure.

### 9.2. Bảng Đối Chiếu Các Điểm Đã Sửa Theo Correction Lượt 2

| Nhóm Sửa Đổi | Yêu Cầu Của Reviewer (Lượt 2) | Kết Quả Triển Khai Trong Báo Cáo |
|:---:|---|---|
| **Exact Source Lines** | Sửa các vị trí dòng còn sai: `calculate_mrr` dòng 45–51, aggregation case dòng 96–97; `calculate_ndcg` dòng 62–78, aggregation case dòng 100–101; `evaluator2.py` category aggregation dòng 132 và 216. | Đã cập nhật chính xác 100% toàn bộ các số dòng tham chiếu trong văn bản và bảng tổng hợp: `calculate_mrr` ([`eval.py:45-51`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L45-L51)), case aggregation ([`eval.py:96-97`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L96-L97)), `calculate_ndcg` ([`eval.py:62-78`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L62-L78)), case aggregation ([`eval.py:100-101`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py#L100-L101)), `category_mrr` ([`evaluator2.py:132`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L132)), `category_accuracy` ([`evaluator2.py:216`](file:///home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluator2.py#L216)). |
| **Canonical Decisions** | Đồng bộ ma trận và Candidate C với canonical: không lưu `claim_id`, đổi `claim_text` thành `text`, không đề xuất `case_type`, không lưu `domain`, mô tả `partition` authoring-only bị loại khi merge; ghi rõ `evidence_groups` syntax minh họa, semantics chưa chốt. | Đã loại bỏ `claim_id` khỏi Candidate C JSON, đổi thuộc tính thành `text`, không mở lại routing cho `case_type`, không đề xuất `domain`, mô tả đúng `partition` là P7 authoring metadata bị loại khi merge. Bổ sung ghi chú rõ ràng cú pháp `evidence_groups` là illustrative only. |
| **Metric Boundary** | Thay cụm từ "True Corpus Retrieval Recall" bằng mô tả đúng: coverage/completeness đối với expected claims/evidence groups đã khai báo. Không nói tự tạo exhaustive labels cho toàn corpus. | Đã thay thế triệt để tại §7.3 và §8.2 bằng khái niệm "độ phủ/độ đầy đủ truy xuất (retrieval coverage / completeness) đối với các expected claims và evidence groups đã được khai báo trong ground truth", nhấn mạnh không phải nhãn exhaustive cho toàn kho. |
| **Reproducibility Claim** | Bỏ việc quy nguyên nhân cụ thể gây nondeterminism cho server drift hay floating-point; chỉ giữ kết luận seed best-effort và single-run judge không cung cấp bảo đảm deterministic. | Đã điều chỉnh tại §6.3: bỏ suy đoán nguyên nhân kỹ thuật không được khảo sát, chỉ giữ kết luận trung thực rằng core eval không có seed/temperature/repetition và seed ở evaluator2 chỉ là best-effort nên không có deterministic guarantee. |
