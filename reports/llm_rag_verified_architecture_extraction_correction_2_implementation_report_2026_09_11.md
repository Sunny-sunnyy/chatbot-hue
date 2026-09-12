# Implementation Report: Correction 2 Verified Architecture Extraction từ `llm_rag`

- **Implementer**: implementer
- **Date**: 2026-09-11
- **Active Contract**: [`handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_2_PROMPT.md`](file:///home/minhhieu/hue_rag/handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_2_PROMPT.md)
- **Canonical Guide**: [`guides/full_corpus_rag.md`](file:///home/minhhieu/hue_rag/guides/full_corpus_rag.md)
- **Artifact chính**: [`reports/llm_rag_verified_architecture_extraction_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_2026_09_11.md)
- **Review tham chiếu**: [`reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md) (§7)

---

## 1. Phạm vi

Thực hiện correction delta cho các nội dung còn mở sau re-review Correction 1:

- **VAE-R2**: Chuyển §4 thành mapping tối thiểu (3 điểm), xác định rõ quan hệ vai trò giữa bằng chứng đối chiếu (§§2–3), quyết định canonical (§5.1) và Decision Queue (§5.2); loại bỏ hoàn toàn việc lặp lại technical details hoặc cơ chế đã nêu ở các mục khác.
- **VAE-R3**:
  - Giới hạn ranh giới kiểm thử đúng trong phạm vi 3 tệp đã đọc (`test_api_chat_openai.py`, `test_llm_generator_openai.py`, `test_context_builder.py`): gồm pure deterministic tests và monkeypatch provider/API, không cung cấp live Qdrant/model integration evidence; không kết luận toàn bộ repository.
  - Xóa bỏ câu "Toàn bộ dữ liệu kiểm thử của `llm_rag` là mock" tại §6.1; nêu rõ khoảng trống đo lường tải/độ trễ do task không chạy runtime.
  - Bổ sung anchor sơ cấp đầy đủ cho claim 30 ứng viên với cả cấu hình `top_k: 10` ([`backend/config/settings.yaml:48-52`](file:///home/minhhieu/llm_rag/backend/config/settings.yaml#L48-L52)) và câu lệnh truy vấn `limit=TOP_K * 3` ([`backend/retrieval/hybrid_retriever.py:38-44`](file:///home/minhhieu/llm_rag/backend/retrieval/hybrid_retriever.py#L38-L44)).
- **VAE-R4**: Lập báo cáo triển khai Correction 2 mới, súc tích, chỉ phản ánh evidence quan sát được; không sửa báo cáo Correction 1 cũ; không tự tuyên bố đóng finding mà để Reviewer kết luận.

Nhiệm vụ thuần tài liệu (docs-only), không chạy runtime hay kiểm thử.

---

## 2. Thay đổi chính

1. [`reports/llm_rag_verified_architecture_extraction_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_2026_09_11.md):
   - *§3*: Cập nhật anchor cho claim 30 ứng viên (dẫn đồng thời `settings.yaml:48-52` và `hybrid_retriever.py:38-44`); thu hẹp ranh giới kiểm thử về đúng 3 tệp khảo sát.
   - *§4*: Rút gọn thành 3 bullet points mapping vai trò bằng chứng và quyết định; không nhắc lại UUID, E5, sparse, fusion, reranker, separator, streaming/session hay one-shot.
   - *§6.1*: Bỏ nhận định mock toàn bộ dữ liệu kiểm thử; diễn đạt chính xác lý do chưa đo tải/độ trễ.
2. [`reports/llm_rag_verified_architecture_extraction_correction_2_implementation_report_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_correction_2_implementation_report_2026_09_11.md):
   - Báo cáo triển khai ngắn cho Correction 2.
3. [`session_prompt/CURRENT_HANDOFF.md`](file:///home/minhhieu/hue_rag/session_prompt/CURRENT_HANDOFF.md):
   - Chuyển handoff sang Reviewer cho lượt re-review Correction 2.

---

## 3. Cách đã chạy thật

Đã chạy các lệnh kiểm tra read-only độc lập:

- Đo kích thước extraction: `wc -l -c reports/llm_rag_verified_architecture_extraction_2026_09_11.md`.
- Kiểm tra danh mục và thứ tự 6 tiêu đề H2 qua regex.
- Chạy script kiểm tra toàn bộ 71 liên kết tệp tin: xác thực đường dẫn tồn tại, EOF qua `awk 'END { print NR }'`, khoảng dòng bắt đầu/kết thúc và đối chiếu khớp chính xác giữa nhãn và fragment URL.
- Quét từ khóa cấm và các câu tự đánh giá hoàn tất.
- Rà soát tính độc nhất ngữ nghĩa (semantic claim uniqueness) giữa §§2–6 bằng đọc trực tiếp văn bản.
- Kiểm tra định dạng Git và trạng thái cây làm việc: `git diff --check`, `git status --short --untracked-files=all`.

---

## 4. Kết quả quan sát

- **Cấu trúc và kích thước**: Extraction đạt **75 dòng** ($\le 320$), **23.570 bytes** ($\le 55.000$); đúng 6 tiêu đề H2 theo thứ tự quy định.
- **Liên kết và khoảng dòng**: 71/71 file URLs trỏ tới tệp tồn tại trên đĩa, khoảng dòng nằm trong $[1, \text{EOF}]$; nhãn liên kết khớp hoàn toàn fragment `#Lstart-Lend`. Anchor `settings.yaml:48-52` (EOF 59) và `hybrid_retriever.py:38-44` (EOF 81) thể hiện chính xác `top_k: 10` và `limit=TOP_K * 3`.
- **Phân định trạng thái Git**:
  - `git diff --check` thực thi sạch (mã thoát 0).
  - 3 task paths thuộc phạm vi:
    1. `reports/llm_rag_verified_architecture_extraction_2026_09_11.md`
    2. `reports/llm_rag_verified_architecture_extraction_correction_2_implementation_report_2026_09_11.md`
    3. `session_prompt/CURRENT_HANDOFF.md`
  - Các thay đổi sửa đổi và tệp untracked khác trong worktree (tại `guides/`, `handoff_prompt/`, `reports/`, `session_prompt/`, `docs/`) đều là trạng thái tồn tại sẵn từ các phiên trước, không bị tác động.
- **Evidence reuse**: Tái sử dụng kết quả kiểm tra mã nguồn cho các phần không đổi của VAE-R1 và VAE-R3 (như `processed_dir`, pipeline/upsert, dense-only query, raw fusion, `SparseEmbedder` fit `set(tokens)`, UUID, và canonical decisions).

---

## 5. Lỗi và giới hạn

- Không có lỗi kỹ thuật tồn đọng trong phạm vi sửa đổi Correction 2.
- Ranh giới thuần tài liệu (docs-only): không chạy runtime mã nguồn, container Qdrant hay mô hình/API. Các chỉ số tải đồng thời, độ trễ và chất lượng reranker trên tiếng Việt được giữ nguyên ở mục §6.1 `[Not verified]`.

---

## 6. Handoff cho Reviewer

- **Tài liệu Reviewer cần đọc**:
  1. [`reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_codex_review_2026_09_11.md) (§7).
  2. [`reports/llm_rag_verified_architecture_extraction_2026_09_11.md`](file:///home/minhhieu/hue_rag/reports/llm_rag_verified_architecture_extraction_2026_09_11.md) (75 dòng, 23.570 bytes).
  3. Báo cáo triển khai này.
- **Các kiểm tra Reviewer nên chạy lại**:
  - `git diff --check` và `git status --short --untracked-files=all`.
  - `wc -l -c reports/llm_rag_verified_architecture_extraction_2026_09_11.md` và kiểm tra 6 H2.
  - Chạy validator cho 71 links/ranges.
  - Đọc semantic kiểm tra tính tối thiểu của §4 và ranh giới kiểm thử tại §3 và §6.1.
