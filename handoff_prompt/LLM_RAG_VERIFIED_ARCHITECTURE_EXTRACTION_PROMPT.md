# Implementer — Verified Architecture Extraction từ reference `llm_rag`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

User đã chấp thuận complexity reset ngày 2026-09-11 sau bốn verdict
`changes_requested` của survey toàn project `llm_rag`. Đây là một nhiệm vụ
`implementation` mới, không phải Correction 5.

Mục tiêu là tạo một evidence companion ngắn, chính xác và chỉ giữ các kết luận
có tác động tới thiết kế Hue RAG. Báo cáo survey 885 dòng được đóng băng ở trạng
thái working/non-canonical và không được chỉnh sửa tiếp.

## 1. Bootstrap và mức đọc bắt buộc

Đọc đúng thứ tự dưới đây. Với mọi file `full-read`, nếu công cụ hiển thị bị
cắt/truncate thì phải đọc tiếp từ dòng dừng đến EOF trước khi làm việc.

1. `full-read` — `session_prompt/Session_Prompt.md`.
2. `targeted-read` — `session_prompt/Project_Status.md`:
   - `Project overview`;
   - `Current runtime and data`;
   - `Thiết kế full-corpus hiện hành`;
   - `Decisions currently in force`;
   - `Safety and authorization boundaries`;
   - đoạn survey `llm_rag` trong `Workstream và roadmap`.
3. `full-read` — `session_prompt/IMPLEMENTER_WORKFLOW.md`.
4. `full-read` — `skills/risk-gated-agent-review/SKILL.md`.
5. `full-read` — `session_prompt/CURRENT_HANDOFF.md`.
6. `full-read` — contract này.
7. `full-read` — `guides/llm_rag_reference_for_hue_rag.md`.
8. `targeted-read` — `guides/full_corpus_rag.md`:
   - `Quyết định đã chốt`;
   - `Nội dung chưa chốt`;
   - `Chuỗi tài liệu và điểm duyệt`;
   - đoạn trạng thái complexity reset `llm_rag`.
9. `targeted-read` —
   `reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md`:
   - §2 `Các kết luận đã được xác nhận`;
   - §9 `Re-review correction lượt 4 và complexity reset`.
10. `targeted-read` —
    `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`:
    `Evidence constraints từ initial survey llm_rag` và các đoạn collection/
    retrieval liên quan.

Các correction prompts cũ và report survey 885 dòng là `reference-only`. Không
full-read chúng; chỉ mở một exact đoạn nếu cần tìm lại source pointer, rồi xác
minh claim bằng source thật. Không sao chép prose, bảng hay self-review từ report
cũ sang artifact mới.

Hai file dưới đây cũng là `reference-only`, không thuộc bootstrap/full-read:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md
/home/minhhieu/llm_rag/tai_lieu/rag_system_pipeline_deep_dive.md
```

File thứ nhất là snapshot 2026-08-08; file thứ hai dài 3.024 dòng và mô tả
snapshot khoảng 2026-08-02. Chỉ targeted-read một đoạn khi cần source pointer,
sau đó xác minh bằng source code; không dùng chúng làm primary evidence hay
nguồn trạng thái hiện hành.

Task docs-only nên không dùng `practical-project-coding`. Không load thêm skill,
không dùng subagent.

## 2. Exact source phải full-read

Đọc đầy đủ các file source/config sau trong repository read-only
`/home/minhhieu/llm_rag`. Nếu output bị cắt phải đọc tiếp tới EOF:

```text
backend/config/settings.yaml
backend/core/settings_loader.py
backend/core/schema.py
backend/core/startup.py
backend/ingestion/load_data.py
backend/ingestion/pipeline.py
backend/ingestion/helpers/make_metadata.py
backend/ingestion/chunking/architectureTypes.py
backend/ingestion/chunking/news.py
backend/ingestion/chunking/projects.py
backend/embedding/embedder.py
backend/embedding/batch_embed.py
backend/embedding/sparse_embedder.py
backend/vectorstore/qdrant.py
backend/vectorstore/hybrid_index.py
backend/vectorstore/upsert.py
backend/retrieval/hybrid_retriever.py
backend/scoring/bm25.py
backend/reranking/reranker.py
backend/retrieval/context_builder.py
backend/llm/prompt.py
backend/llm/generator_openai.py
backend/api/app.py
backend/api/health.py
backend/api/routes/chat.py
backend/api/routes/chat_openai.py
frontend/lib/api.ts
frontend/components/ChatInterface.tsx
backend/tests/test_context_builder.py
backend/tests/test_llm_generator_openai.py
backend/tests/test_api_chat_openai.py
```

Để xác nhận `data.processed_dir`, còn phải targeted-read exact đầu file của bốn
chunker còn lại tới hết câu lệnh tạo `file_path`:

```text
backend/ingestion/chunking/companyInfo.py
backend/ingestion/chunking/interiorStyles.py
backend/ingestion/chunking/newCategories.py
backend/ingestion/chunking/projectCategories.py
```

Chỉ đọc source/config; không import hay chạy project. Không đọc `.env`, logs,
raw/processed JSON, model cache, Qdrant storage, generated/binary state,
notebooks, `node_modules` hoặc toàn bộ tree.

## 3. Artifact phải tạo

Tạo:

```text
reports/llm_rag_verified_architecture_extraction_2026_09_11.md
```

Artifact phải ngắn hơn hoặc bằng **320 dòng và 55.000 bytes**. Sau một title
`#`, phải có đúng sáu section `##` theo thứ tự:

1. `Mục đích, trạng thái và ranh giới bằng chứng`
2. `Kiến trúc và luồng dữ liệu đang hoạt động`
3. `Các phát hiện decision-relevant từ llm_rag`
4. `Ánh xạ sang Hue RAG: giữ, thích ứng, không sao chép`
5. `Quyết định Hue đã chốt và quyết định còn mở`
6. `Khoảng trống bằng chứng và điều kiện sử dụng`

Không cần đạt một số dòng tối thiểu. Ưu tiên câu ngắn, bullet và bảng nhỏ tối đa
năm cột. Không dùng Mermaid nếu một dòng flow text đã đủ rõ.

### 3.1. Nội dung bắt buộc

Chỉ giữ các kết luận sau khi source/guide hỗ trợ:

- hai flow chính: offline ingestion và startup/request-time;
- JSON field chunking của reference khác Markdown heading/breadcrumb chunking
  của Hue;
- `data.processed_dir` được `load_data.py` và cả bảy chunker tiêu thụ qua
  settings, không phải path cứng;
- active ingestion gom toàn bộ chunks, direct dense+sparse embedding và một
  lần upsert; batch wrapper 64 không nằm trên active path;
- random UUID, thiếu stale-point cleanup và thiếu existing-schema validation;
- một configured Qdrant collection chứa dense+sparse; runtime query chỉ lấy 30
  dense candidates rồi BM25 rescore trong candidate set;
- sparse vocabulary/index mapping không persist và sparse vector không có query
  consumer trong runtime quan sát được;
- raw dense/BM25 score fusion chưa normalize; reranker lưu
  `metadata["rerank_score"]` nhưng không thay `doc.score`;
- context giới hạn document/character và bỏ qua separator length;
- E5 reference dùng chung raw embed path không tự thêm `query:`/`passage:`;
- SSE/API/citation/logging/session behaviors chỉ giữ khi chúng tạo contrast hữu
  ích với Hue one-shot MVP hoặc chỉ ra risk không nên sao chép;
- test evidence chỉ mô tả ranh giới mocked/unit và thiếu live integration
  evidence; không liệt kê 20 test functions;
- Hue decisions đã chốt: ba isolated candidate collections, tối đa sáu cho A/B
  representation, Foods historical collections read-only và one-shot
  non-streaming MVP;
- exact collection names/schema/lifecycle, sparse-vs-local lexical approach,
  fusion/reranker matrix và remaining API/context budgets vẫn là open decisions.

Mỗi kết luận kỹ thuật quan trọng phải có inline primary-source anchor ngay tại
lần xuất hiện duy nhất. Canonical Hue decisions dẫn guide/decision notes, không
gắn nhãn như observed source của `llm_rag`.

### 3.2. Nội dung phải loại

Không đưa vào artifact mới:

- comprehensive/exhaustive file inventory hoặc file counts;
- checksum, JSON record counts/sampling catalogue và historical 450/1.486/48,84;
- ma trận 34 config parameters;
- dependency-version catalogue trừ khi một version trực tiếp thay đổi kết luận;
- bảng 20 test functions hoặc mô tả từng mock;
- frontend component catalogue;
- JSON-to-Markdown matrix 16 giai đoạn;
- glossary, traceability table lặp hoặc self-review/completion claims;
- lời khen, lời cấm tuyệt đối, benchmark/latency/quality claim chưa đo;
- bất kỳ quyết định Hue mới nào ngoài các quyết định đã chốt trong guide/notes.

Không dùng các cụm `toàn diện`, `100%`, `mọi anchor đã đúng`, `hoàn chỉnh tuyệt
đối`, `PASS`, `approved`, `completed` để tự đánh giá artifact.

### 3.3. Nhãn bằng chứng

Dùng tối thiểu và nhất quán:

- `[Observed in llm_rag]` cho source fact;
- `[Design inference]` cho suy luận có giải thích;
- `[Canonical Hue decision]` cho quyết định đã chốt trong guide/notes;
- `[Not verified]` cho runtime/model/integration chưa chạy.

Không dùng hai nhãn khác loại cho cùng một câu. Không gọi intent là observed
behavior nếu source chỉ cho thấy cấu hình.

## 4. File được phép thay đổi

Chỉ được tạo/sửa:

1. `reports/llm_rag_verified_architecture_extraction_2026_09_11.md`;
2. `reports/llm_rag_verified_architecture_extraction_implementation_report_2026_09_11.md`;
3. `session_prompt/CURRENT_HANDOFF.md`.

Không sửa report survey 885 dòng, Codex review, contract này, guide, status,
decision/plan notes, source/runtime/tests/corpus/Golden/index/dependencies hoặc
repository `/home/minhhieu/llm_rag`.

Không chạy/import Python/Node/project code, tests, model, API, Qdrant, frontend
build, notebook hay benchmark. Không network, Git write hoặc subagent.

## 5. Verification bắt buộc

Trước bàn giao:

1. full-read artifact mới tới EOF;
2. xác nhận đúng 6 top-level sections, `wc -l -c` nằm trong limits;
3. dùng `rg` xác nhận không có các nhóm nội dung bị loại hoặc completion claim;
4. kiểm mọi local source path tồn tại;
5. kiểm cả đầu và cuối của mọi line/range anchor không vượt số dòng thật bằng
   `awk 'END { print NR }'`, không dùng riêng `wc -l`;
6. semantic-check từng anchor quan trọng với câu nó hỗ trợ, đặc biệt:
   `data.processed_dir`, pipeline/upsert, dense-only candidate retrieval,
   sparse mapping, UUID/lifecycle, score/reranker và one-shot Hue decision;
7. chạy `git diff --check`, `git status --short` và xác nhận đúng allowed files.

Implementation report phải ngắn, chỉ mapping acceptance -> evidence, lệnh
read-only đã chạy, kết quả quan sát, phần skipped/not verified và exact changed
files. Không lặp nội dung extraction hoặc governance checklist.

## 6. Review Contract

Risk: `medium` vì artifact là candidate evidence companion cho Written Spec,
nhưng thay đổi chỉ là Markdown và không cấp quyền runtime.

Reviewer sẽ:

- kiểm exact changed/untracked files và `git diff --check`;
- full-read extraction và implementation report;
- kiểm structure/size, duplicated claims, evidence labels và lifecycle wording;
- chạy validator path/range cho toàn bộ anchors;
- kiểm độc lập các anchor trọng yếu về `data.processed_dir`, ingestion/upsert,
  retrieval/sparse/fusion, UUID/lifecycle, reranker score và Hue decisions;
- không chạy lại model/API/Qdrant/tests vì task docs-only.

Technical readiness chỉ đạt khi không còn blocker/major, artifact không phụ
thuộc prose của report frozen và không biến open decision thành canonical.
Minor không ảnh hưởng kết luận sẽ không tạo correction loop mới. Sau technical
readiness, Reviewer trình User Approval Closure Contract; artifact chỉ thành
approved evidence companion sau exact User confirmation.

## 7. Bàn giao

Cập nhật `CURRENT_HANDOFF.md` thành:

```text
Target role: reviewer
Authored by: implementer
Handoff kind: final_review
State: active
Base commit: ea87d3ed52851f6b6ab5c47b138540ebc8ff8340
Head commit: worktree
Risk level: medium
Git authorization: none
Sub-agent authorization: none
```

Next action duy nhất: Reviewer final-review Verified Architecture Extraction
theo Review Contract §6. Không tự claim PASS/approved/completed và không resume
Written Spec/Plan.
