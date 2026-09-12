# Implementer — correction lượt 1 báo cáo simplicity evaluation `rag_old_0`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Sửa đúng các findings trong:

`reports/full_corpus_rag_old_0_evaluation_simplicity_survey_codex_review_2026_09_10.md`

Report cần sửa:

`reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md`

Đây là correction docs-only hẹp. Không khảo sát lại từ đầu và không tự đổi bất
kỳ quyết định canonical nào.

## 1. Bootstrap bắt buộc

Đọc đầy đủ theo thứ tự:

1. `session_prompt/Session_Prompt.md`
2. `session_prompt/Project_Status.md`
3. `session_prompt/IMPLEMENTER_WORKFLOW.md`
4. `session_prompt/CURRENT_HANDOFF.md`
5. `skills/risk-gated-agent-review/SKILL.md`
6. `skills/practical-project-coding/SKILL.md`
7. prompt khảo sát gốc
8. Codex review nêu trên
9. report cần sửa

Chỉ đọc lại đúng source/canonical sections cần để sửa R1–R5. Không đọc nội dung
`knowledge-base/**/*.md`.

## 2. Correction bắt buộc

### C1 — inventory

- Thay các filename ví dụ không tồn tại bằng path có thật từ inventory; sửa
  `Zachary Brooks` thành tên đúng hoặc bỏ examples.
- Dùng một quy ước line count nhất quán cho năm notebook và tổng, hoặc bỏ cột
  line count. Không cần đọc lại notebook chỉ để đếm.

### C2 — data flow

- Viết đúng signatures hiện hành: `evaluate_retrieval(test, k=10)` và
  `evaluate_answer(test)`; không mô tả dependency injection không tồn tại.
- Nêu rõ `evaluation/eval.py` trực tiếp dùng PRO implementation hiện hành.
- Đặt tổng aggregation/category breakdown đúng tại `evaluator.py` và
  `evaluator2.py`; chỉ MRR và Accuracy được chart theo category.
- Nêu rõ `k` chỉ cắt nDCG; nó không điều khiển `fetch_context`. PRO trả final
  top 10; `RETRIEVAL_K=20` là mỗi query trước merge/rerank.
- Sửa toàn bộ path:line theo source hiện hành.

### C3 — schema và scope

- Kết luận trực tiếp: với đúng sáu metric hiện hành của `rag_old_0`, required
  data fields là `question`, `keywords`, `reference_answer`; `category` optional
  cho thống kê/breakdown nếu target loader cho phép.
- Tách riêng `case_id`: không có consumer trong `rag_old_0`; nếu vẫn đề xuất cho
  Hue thì chỉ gọi là operational identifier đề xuất, không gọi bất biến, không
  nói cần cho concurrency và không nói chi phí bằng zero.
- Tách rõ evidence/expected claims không cần cho sáu metric trên nhưng đang phục
  vụ requirement khác đã chốt của Hue: citation tới nguồn thật, retrieval
  completeness và claim–source support/groundedness. Không quyết định thay User.
- Sửa kỹ thuật: chunk ID có thể đổi khi rechunk; source-level exact LF span
  không đổi chỉ vì rechunk, nhưng có thể đổi khi source text đổi.
- Đối chiếu đủ `evidence_groups`, `case_type`, `partition`, `domain`, `claim_id`:
  consumer hiện tại, requirement nào phục vụ, và phần nào có thể omit/derive.
- Candidate baseline phải là ba field metric với `category` optional. Mỗi
  candidate khác phải phân biệt observed consumer và proposed consumer.

### C4 — evidence-bounded claims

- Xóa các ước lượng 70%, 200%–300% và mọi claim cost/effort tuyệt đối không có
  measurement.
- Hạ claim test harness “không đổi một dòng” thành điều transcript/course
  narrative mô tả, trừ khi có version diff thật trong scope.
- Không dùng reuse evaluator để suy rằng simplicity gây ra score improvement.
- Bỏ ngôn ngữ quảng bá và các kết luận “vô nghĩa”, “loại bỏ ngay”, “do X chứng
  minh” vượt evidence.

### C5 — benchmark và reproducibility

- Gắn 0.7298/0.7903/0.9116/3.99/4.62 đúng với transcript, không gắn với saved
  notebook output.
- Bỏ 97.8%, Completeness 4.55 và Relevance 4.71 nếu không chỉ ra được exact
  first-party non-data source trong scope.
- Nêu saved notebooks thực sự chứng minh gì: Day 4 có single-case output;
  Day 5 có implementation/probes, không lưu full aggregate benchmark được nêu.
- Thêm mục ngắn: `evaluator2.py` best-effort seed 42; core judge không đặt
  temperature/repetitions; một lần LLM judge không bảo đảm deterministic.
- Ghi đúng ngưỡng dashboard: MRR/nDCG 0.90/0.75, coverage 90/75, answer
  4.5/4.0; đây là color thresholds quan sát được, không tự gọi acceptance gate.

## 3. Phần phải giữ

Không viết lại khảo sát từ đầu. Giữ các kết luận Reviewer đã xác nhận:

- coverage counts 20 non-data + 76 data inventory-only;
- 150 record và phân bố category;
- bốn field reference, sáu metric và main field consumers;
- keyword substring proxy, per-keyword aggregation, MRR/nDCG cutoff khác nhau;
- IDCG limitation;
- LLM Judge không nhận retrieved context/evidence;
- không có current `rag_old_0` consumer cho evidence/expected claims.

## 4. Quyền và output

Chỉ được sửa:

1. `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md`
2. `session_prompt/CURRENT_HANDOFF.md`

Không tạo review/user report khác. Không sửa guide, decision notes, context,
Project Status, prompt, runtime, tests, notebooks, corpus, Golden hoặc index.
Không chạy/import code, Python, test, notebook, model, API, Qdrant hay benchmark;
không đọc `.env`, không mạng, không Git write và không spawn subagent.

## 5. Bàn giao

Khi hoàn tất, cập nhật `CURRENT_HANDOFF.md`:

- `Target role: reviewer`
- `Authored by: implementer`
- `Handoff kind: final_review`
- `State: active`

Liệt kê correction mapping C1–C5, exact files changed và giới hạn. Không tự
claim PASS, approval hoặc closure.
