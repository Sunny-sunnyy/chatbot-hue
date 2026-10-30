# Hướng dẫn Hue RAG — mục lục guide

Cập nhật 2026-10-25 (B26, rà code). Bản trước (dừng ở 2026-10-01, còn vai "Codex Reviewer" và quy trình `reports/`) xem lịch sử Git
của file này.

## Đọc gì trước

| Cần biết | Đọc |
|---|---|
| Hệ thống **đang chạy** (runtime, dữ liệu, Qdrant, bẫy) | [`session_prompt/Project_Status.md`](../session_prompt/Project_Status.md) §4, §8 |
| Việc đang mở, ai làm gì | [`session_prompt/CURRENT_HANDOFF.md`](../session_prompt/CURRENT_HANDOFF.md) |
| Luật chung, cách làm A / B / C | [`session_prompt/Session_Prompt.md`](../session_prompt/Session_Prompt.md), [`session_prompt/WORKFLOW.md`](../session_prompt/WORKFLOW.md) |
| Guide hiện hành của luồng full-corpus (cập nhật 7A2 / 7B, build lại index) | [`full_corpus_rag.md`](full_corpus_rag.md) |
| Báo cáo cho User theo từng khâu | [`bao_cao_he_thong/README.md`](../bao_cao_he_thong/README.md) |
| Report của agent theo đợt | [`report_agent/README.md`](../report_agent/README.md); `reports/` là lịch sử tới 2026-10-24 |

Thứ tự ưu tiên khi tài liệu khác nhau: `Session_Prompt.md` §2. Code, dữ liệu canonical và lần chạy mới cho biết hệ thống đang làm gì;
guide lệch với chúng ⇒ báo A (sửa guide, hoặc sửa code nếu guide ghi đúng yêu cầu đã duyệt).

## Các guide

Guide có dòng **"Guide lịch sử"** ở đầu tả hệ thống Foods / thiết kế cũ lúc viết: file, collection, profile, model và lệnh trong đó có
thể đã gỡ — không làm theo như hướng dẫn hiện hành. Guide có mục **"Hiện hành"** ở đầu: chỉ mục đó là hiện trạng, phần còn lại là lịch sử.

| Phase | Guide | Trạng thái Phase | Loại guide |
|---:|---|---|---|
| 0 | [`phase_0_mvp_foundation.md`](phase_0_mvp_foundation.md) | `approved` | lịch sử |
| 1 | [`phase_1_backend_skeleton.md`](phase_1_backend_skeleton.md) | `approved` | lịch sử |
| 2 | [`phase_2_foods_markdown_chunking.md`](phase_2_foods_markdown_chunking.md) | `approved` | lịch sử |
| 3 | [`phase_3_embedding_sparse_representation.md`](phase_3_embedding_sparse_representation.md) | `approved` | lịch sử |
| 4 | [`phase_4_qdrant_ingestion.md`](phase_4_qdrant_ingestion.md) | `approved` | lịch sử |
| 5 | [`phase_5_retrieval_profiles_reranking.md`](phase_5_retrieval_profiles_reranking.md) | `approved` | mục "Hiện hành" + lịch sử |
| 6 | [`phase_6_generation_api.md`](phase_6_generation_api.md) | `approved` (`gpt-6-luna`) | mục "Hiện hành" + lịch sử |
| 7, 7A, 7A2, 7B | [`phase_7_retrieval_answer_evaluation.md`](phase_7_retrieval_answer_evaluation.md) | `approved` | mục "Hiện hành" + lịch sử Foods |
| 8.1, 8.2 | [`phase_8_benchmark_model_selection.md`](phase_8_benchmark_model_selection.md) | 8.1 `approved`, 8.2 `approved` (User đóng 28/10) | mục "Hiện hành" + lịch sử Foods |
| 9 | [`phase_9_agentic_rag_roadmap.md`](phase_9_agentic_rag_roadmap.md) | `not_ready` | roadmap |
| — | [`full_corpus_rag.md`](full_corpus_rag.md) | — | hiện hành (phần đầu) + lịch sử quyết định |
| — | [`llm_rag_reference_for_hue_rag.md`](llm_rag_reference_for_hue_rag.md) | — | tham khảo từ một repo khác của User |

Trạng thái chính thức từng Phase: bảng `Project_Status.md` §3 (bảng này chỉ là lối tắt).

## Notebook

Còn 3 notebook: `notebooks/03_embedding_models.ipynb`, `04_qdrant_ingestion.ipynb`, `06_generation_and_api.ipynb`. Luật: `Session_Prompt.md`
§11 — mỗi cell một việc, Markdown ngắn trước code, code ngắn gọi backend, không phải validator / test suite, outputs rỗng và
`execution_count: null` trong repo, Run All thật trên bản tạm. Phong cách mẫu là các notebook ngắn trong repo tham khảo của User (đường dẫn
máy không ghi trong repo public).

## Khi sửa guide

Guide do A giữ (hoặc session được giao); thay đổi provider, model, schema, collection đang chạy, thao tác xóa, ranh giới Phase hay tiêu chí
nghiệm thu cần User duyệt (`Session_Prompt.md` §4). Guide không phải nhật ký: lịch sử chi tiết ở Git, `PROJECT_HISTORY.md` và report.
