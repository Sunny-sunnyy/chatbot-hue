# Codex Review: Verified Architecture Extraction từ `llm_rag`

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-11
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/llm_rag_verified_architecture_extraction_implementation_report_2026_09_11.md`

## 1. Phạm vi đã review

Reviewer đã đọc đầy đủ active contract, extraction, implementation report và
các bootstrap bắt buộc; đọc đúng các section targeted của guide/decision notes;
kiểm trạng thái Git, exact task paths, cấu trúc/kích thước, nhãn, nội dung lặp,
mọi file URL/range và các source anchors trọng yếu theo Review Contract §6.

Source checks tập trung gồm `data.processed_dir`, ingestion/upsert, dense-only
candidate retrieval, sparse mapping, UUID/index lifecycle, fusion/reranker
score, test boundary và các quyết định Hue về collection/one-shot. Report survey
885 dòng và hai tài liệu lịch sử của reference không được mở.

## 2. Findings

### VAE-R1 — Major: lexical recommendation và các lựa chọn còn mở bị trình bày như thiết kế Hue đã chốt

Vị trí: extraction §4 và §5.1, đặc biệt các dòng 46–52 và 63–66 của bản được
review.

Requirement: artifact không được tạo quyết định Hue mới; phải tách rõ
`[Canonical Hue decision]` khỏi `[Design inference]` và open decisions.

Evidence:

- `guides/full_corpus_rag.md:247-265` và decision notes
  `2026-09-09-full-corpus-context-decisions.md:1051-1075` đặt lexical baseline,
  lifecycle, payload, fusion/reranker, representation B và API/context budgets
  trong Decision Queue; dense + BM25 local chỉ là khuyến nghị hiện hành;
- extraction gọi “Kiến trúc Lexical Canonical” và nói Hue sử dụng Python BM25
  in-memory. Anchor `guides/llm_rag_reference_for_hue_rag.md:304-320` chỉ mô tả
  Foods runtime hiện hành, không chốt lexical baseline cho full corpus;
- bảng §4 còn dùng lời chỉ dẫn về deterministic ID, schema cleanup, RRF/min-max,
  token budget và error/session handling nhưng không gắn nhãn inference/open.

Tác động: artifact có thể bỏ qua chính Decision Queue phải hỏi User sau closure
và làm Written Spec nhận recommendation như requirement.

Tiêu chí đóng: chuyển lexical baseline về open decision; chỉ giữ canonical các
quyết định thực sự đã chốt. Mọi mapping chưa chốt phải ghi rõ là design
inference/constraint, hoặc bỏ nếu trùng Decision Queue; không chọn mechanism.

### VAE-R2 — Major: artifact tái tạo duplication/self-review mà complexity reset yêu cầu loại bỏ

Vị trí: extraction dòng 13 và §§2–4 của bản được review.

Requirement: mỗi technical claim xuất hiện một lần; không có traceability table
lặp, self-review/completion claim hoặc lời cấm tuyệt đối.

Evidence: dense retrieval/BM25/fusion, UUID/lifecycle, E5 input, reranker score,
context separator và API/session behavior đều được lặp giữa flow §2, findings §3
và bảng mapping §4. Cột “Primary Source Anchor” của bảng lặp lại anchors/claims.
Dòng 13 tự tuyên bố mọi claim chỉ xuất hiện một lần và đã loại bỏ hoàn toàn các
nhóm nội dung; dòng 80 dùng “Tuyệt đối không”.

Tác động: lặp lại đúng maintenance surface/root cause khiến survey 885 dòng bị
complexity reset và làm các bản sao dễ lệch nhau.

Tiêu chí đóng: mỗi source fact có đúng một authoritative occurrence/anchor trên
toàn artifact; §4 chỉ nêu mapping ngắn không lặp source fact/anchor và không là
traceability matrix. Xóa self-review/completion prose và lời cấm tuyệt đối.

### VAE-R3 — Major: nhiều observed claim và anchor không được source hiện hành hỗ trợ đúng nghĩa

Vị trí: extraction dòng 27, 32, 36, 41, 54 và 63 của bản được review.

Requirement: mỗi kết luận kỹ thuật quan trọng có primary-source anchor đúng
nghĩa; observed claim không vượt quá static source đã đọc.

Evidence độc lập:

- `architectureTypes.py:68` chỉ chứng minh điều kiện cần `name` và
  `description`; source tĩnh không chứng minh processed records thiếu
  `description` hay kết quả bằng 0. Artifact không được đọc raw/processed data;
- `sparse_embedder.py:52` lặp trên `set(tokens)`, không phải “thứ tự gặp từ”;
- ba file test có 20 test functions, nhưng 9 functions không nhận
  `monkeypatch`; vì vậy “20 hàm ... hoàn toàn sử dụng monkeypatch” là sai. Ba
  file được giao chỉ hỗ trợ kết luận hẹp rằng các integration/provider paths
  được fake/monkeypatch và review này chưa thấy live integration evidence;
- `frontend/lib/api.ts:56-144` không chứng minh version “Next.js 15”; version
  này cũng không decision-relevant;
- anchor `guides/llm_rag_reference_for_hue_rag.md:424-426` không ghi quyết định
  one-shot/non-streaming. Decision trực tiếp nằm tại decision notes dòng 68–72
  hoặc guide umbrella dòng 272–276;
- nhãn range `sparse_embedder.py:21, 52-56` chỉ link tới `#L21`, và nhãn
  `chat_openai.py:26-46, 139-165` chỉ link tới `#L26-L46`. Validator đã kiểm URL
  fragment nhưng không phát hiện phần range thứ hai trong link label.

Tác động: evidence companion không đủ tin cậy để làm đầu vào cho Written Spec.

Tiêu chí đóng: bỏ hoặc thu hẹp các claim trên theo đúng source; sửa anchor
one-shot; tách mọi disjoint range thành link độc lập và kiểm cả label lẫn URL
fragment. Không thay source thiếu bằng prose của frozen survey.

### VAE-R4 — Major: implementation evidence index mâu thuẫn với artifact và trạng thái worktree

Vị trí: implementation report §§1–2 và §4; `CURRENT_HANDOFF.md` summary.

Requirement: implementation report là evidence index chính xác, không tự chứng
minh kết quả hoặc che trạng thái pre-existing của worktree.

Evidence: report nói không có traceability/source table lặp, nhãn nhất quán,
không biến open decision thành canonical và validator đã kiểm mọi range; VAE-R1
đến VAE-R3 chứng minh ngược lại. `wc -l -c` lúc review là 81 dòng/24.833 bytes,
không phải 24.836 bytes. `git status --short` hiện có nhiều thay đổi/untracked
full-corpus đã tồn tại trước task; chỉ ba task paths là phạm vi Implementer khai
báo, không thể mô tả output Git tổng thể là chỉ có ba paths.

Tác động: User/Reviewer không thể dùng self-verification hiện tại làm chỉ mục
evidence đáng tin cho closure.

Tiêu chí đóng: không sửa implementation report gốc. Tạo correction report ngắn
ghi fresh observed values, phân biệt task paths với pre-existing worktree và
không claim các tiêu chí chưa được kiểm đúng.

## 3. Cách Reviewer chạy lại thật

Reviewer đã dùng các lệnh read-only sau:

```text
git rev-parse HEAD
git cat-file -e ea87d3ed52851f6b6ab5c47b138540ebc8ff8340^{commit}
git status --short --untracked-files=all
git diff --check
wc -l -c reports/llm_rag_verified_architecture_extraction_2026_09_11.md
rg -n '^## ' reports/llm_rag_verified_architecture_extraction_2026_09_11.md
awk 'END { print NR }' <từng source path được anchor>
rg/nl/sed trên exact source ranges nêu trong Review Contract
```

Reviewer cũng quét đủ 69 file URLs, so path/range với EOF thực và đối chiếu
semantic source cho các anchors trọng yếu. Không chạy project code.

## 4. Kết quả quan sát

- Base commit hợp lệ và bằng current Hue `HEAD`:
  `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`.
- Reference `llm_rag` có `HEAD`
  `920c5798e855b67fc073b3c8b117db65c61df6b6`; tracked backend source được kiểm
  không xuất hiện trong status thay đổi của reference.
- Extraction có đúng 6 H2 theo thứ tự, 81 dòng và 24.833 bytes; nằm trong giới
  hạn. `git diff --check` sạch.
- 69/69 file URLs trỏ tới path tồn tại; URL fragments không vượt EOF. Hai link
  labels chứa disjoint ranges không khớp fragment như VAE-R3.
- Các core source claims về `processed_dir`, one-shot ingestion/upsert,
  dense-only candidate query, raw fusion, UUID/lifecycle và reranker score đã
  khớp source focused-check.
- VAE-R1–R4 còn mở; technical readiness chưa đạt.

## 5. Giới hạn hoặc phần chưa chạy

Review là docs-only. Reviewer không chạy/import Python/Node project code, tests,
model, API, Qdrant, frontend, notebook hoặc benchmark; không đọc `.env`, logs,
raw/processed data, report survey 885 dòng hoặc hai tài liệu lịch sử
reference-only. Các quality/latency/integration claims tiếp tục là not verified.

## 6. Decision và bước tiếp theo

Decision: `changes_requested`.

Correction delta nằm tại
`handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_CORRECTION_1_PROMPT.md`.
Implementer chỉ sửa extraction, tạo correction report mới và trả handoff về
Reviewer/final_review. Không sửa frozen survey hay implementation report gốc,
không resume Decision Queue/Written Spec/Plan và không có Approval Closure
Contract cho tới khi VAE-R1–R4 đóng.

## 7. Re-review Correction 1 — 2026-09-11

### 7.1. Phạm vi và kết quả cơ học

Reviewer full-read extraction đã sửa, correction implementation report và
handoff; chạy lại minimum Git gate, cấu trúc/kích thước, forbidden-term scan,
toàn bộ link/path/range validator và semantic checks bị ảnh hưởng.

Các kiểm tra cơ học đạt:

- extraction có đúng 6 H2, 80 dòng/24.932 bytes;
- 70/70 file URLs tồn tại, URL ranges không vượt EOF, label khớp fragment và
  không còn disjoint-range label;
- không có duplicate URL target; `git diff --check` sạch;
- VAE-R1 đã đóng: lexical baseline và các lựa chọn phụ thuộc đã trở lại Decision
  Queue; one-shot/collection decisions dùng đúng canonical anchors;
- phần `architectureTypes`, `set(tokens)`, version frontend và disjoint links
  của VAE-R3 đã được sửa đúng.

### 7.2. Findings còn mở

#### VAE-R2 — Major, còn mở: duplicate URL validator không kiểm duplicate claim

Extraction §4 dòng 44–51 vẫn lặp lại gần như toàn bộ conclusions của §2–3:

- offline/online separation: §2 và dòng 44;
- JSON-vs-Markdown chunking: dòng 30 và 45;
- UUID/idempotency: dòng 32 và 46;
- E5 prefixes: dòng 33 và 47;
- sparse/no consumer: dòng 34 và 48;
- fusion/reranker score: dòng 36 và 49;
- separator budget: dòng 37 và 50;
- streaming error/session state: dòng 38–39 và 51;
- one-shot decision: dòng 51 và 58.

Việc bỏ anchors khỏi §4 chỉ làm URL targets thành duy nhất; không làm technical
claims thành duy nhất. Đây là đúng VAE-R2, không phải finding mới.

Tác động: complexity-reset root cause vẫn tồn tại và các bản diễn giải có thể
lệch nhau ở correction sau.

Tiêu chí đóng: §4 không lặp từng source finding. Giữ section bắt buộc bằng một
mapping tối thiểu: nói source observations ở §§2–3 chỉ là evidence, canonical
Hue decisions nằm ở §5.1 và mọi adaptation chưa chốt nằm ở §5.2. Không nhắc lại
UUID, sparse, fusion, reranker, separator, error/session hoặc one-shot details.

#### VAE-R3 — Major, còn mở: test boundary vẫn có claim sai/rộng và anchor “30” chưa đủ nghĩa

Vị trí: extraction dòng 34, 40 và 74.

Evidence:

- focused text count xác nhận ba file có 20 test functions, trong đó 11 nhận
  `monkeypatch`; 9 còn lại không nhận. Dòng 40 đã thừa nhận có pure deterministic
  tests nhưng vẫn kết luận cho toàn repository rằng không có live integration
  test; phạm vi ba file không chứng minh inventory toàn repository;
- dòng 74 vẫn nói “Toàn bộ dữ liệu kiểm thử của `llm_rag` là mock”, mâu thuẫn
  trực tiếp với dòng 40 và source;
- dòng 34 nói lấy 30 candidates nhưng anchor duy nhất tại claim đó là
  `hybrid_retriever.py:41`, chỉ chứng minh `using="dense"`. Số 30 cần cả
  `TOP_K=10`/configured `top_k: 10` và `limit=TOP_K * 3` tại source liên quan.

Tác động: artifact tiếp tục vượt evidence boundary và một mandatory retrieval
claim thiếu inline primary anchor đủ nghĩa.

Tiêu chí đóng: giới hạn test claim vào đúng ba file—các file này không cung cấp
live Qdrant/model integration evidence—và bỏ câu “toàn bộ ... là mock” ở §6.
Không kết luận về toàn repository. Với 30 candidates, dùng anchor/range thể hiện
cả configured/default `TOP_K=10` và `limit=TOP_K * 3`, hoặc diễn đạt chính xác
theo cấu hình mà anchor thực sự hỗ trợ.

#### VAE-R4 — Major, còn mở: correction evidence index tiếp tục claim sai trạng thái

Correction implementation report nói VAE-R2/VAE-R3 đã đóng, “0 duplicate
targets” đồng nghĩa mỗi technical claim chỉ xuất hiện một lần, và không có lỗi/
giới hạn kỹ thuật đã biết. §7.2 chứng minh các kết luận đó chưa đúng. Report dài
159 dòng và lặp lại findings/thay đổi/scripts thay vì làm evidence index ngắn.

Tiêu chí đóng: giữ report Correction 1 nguyên trạng lịch sử; Correction 2 tạo
một report mới ngắn, chỉ map exact acceptance tới evidence, observed outputs,
task paths và skipped/not-verified. Không dùng URL-target uniqueness làm proxy
cho semantic claim uniqueness và không tự tuyên bố finding đã đóng.

### 7.3. Decision và bước tiếp theo

Decision: `changes_requested`.

Correction 2 chỉ xử lý VAE-R2, phần còn mở của VAE-R3 và VAE-R4. VAE-R1 cùng
các phần VAE-R3 đã đạt được reuse. Không có Approval Closure Contract và chưa
được tiếp tục Decision Queue/Written Spec/Plan.

## 8. Re-review Correction 2 và Approval Closure Contract — 2026-09-11

### 8.1. Phạm vi và kết quả độc lập

Reviewer full-read extraction, Correction 2 implementation report và handoff;
chạy lại minimum Git gate, structure/size, semantic uniqueness, test boundary,
anchor 30 candidates và toàn bộ path/range validator theo Correction 2 Review
Contract.

Kết quả quan sát:

- extraction có đúng 6 H2, 75 dòng/23.570 bytes;
- 71/71 file URLs tồn tại; start/end không vượt EOF theo
  `awk 'END { print NR }'`; link labels khớp URL fragments;
- §4 chỉ còn mapping vai trò giữa evidence, canonical decisions và Decision
  Queue; không lặp technical findings hoặc one-shot decision;
- ba test files được giao có 20 test functions, gồm 11 functions nhận
  `monkeypatch` và 9 pure/non-monkeypatch cases. Extraction chỉ kết luận ba file
  này không cung cấp live Qdrant/model integration evidence;
- claim 30 candidates dẫn cả `settings.yaml:48-52` (`top_k: 10`) và
  `hybrid_retriever.py:38-44` (`limit=TOP_K * 3`);
- Correction 2 report là evidence index 85 dòng/7.294 bytes, không chép script
  hoặc tự tuyên bố Reviewer đã đóng findings. Con số 86 dòng trong handoff/
  user summary lệch 1 dòng so với `wc -l`, là minor không ảnh hưởng artifact hay
  acceptance và được thay bằng số quan sát thật trong closure state;
- `git diff --check` sạch; ba task paths được phân biệt với worktree có sẵn.

VAE-R1–VAE-R4 đã đóng về kỹ thuật. Không còn blocker/major. Technical verdict:
`ready_for_user_confirmation`.

### 8.2. Giới hạn

Review docs-only: không chạy/import project code, tests, model, API, Qdrant,
frontend, notebook hoặc benchmark; không đọc `.env`, logs, raw/processed data,
survey 885 dòng hoặc hai tài liệu lịch sử reference-only. Runtime quality,
latency và integration vẫn là `[Not verified]`; đây là giới hạn đã khai báo,
không phải acceptance của extraction.

### 8.3. Approval Closure Contract

Xác nhận cần từ User:

```text
Tôi xác nhận closure Verified Architecture Extraction.
```

Xác nhận này chỉ công nhận extraction là **approved evidence companion** cho
full-corpus design. Nó không phê duyệt runtime, Written Spec, Implementation
Plan, benchmark, collection mutation, Git write hoặc bất kỳ lựa chọn nào trong
Decision Queue.

Sau exact User confirmation, Reviewer được cập nhật docs-only:

1. append User confirmation và closure decision vào Codex review này;
2. đồng bộ trạng thái survey frozen/extraction approved và next Decision Queue
   trong `session_prompt/Project_Status.md`;
3. đồng bộ trạng thái/chuỗi duyệt trong `guides/full_corpus_rag.md`;
4. cập nhật index pointers/status trong `guides/README.md`, `reports/README.md`
   và `handoff_prompt/README.md`;
5. ghi closure và mở Decision Queue trong
   `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md` cùng
   `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`;
6. cập nhật snapshot và append mốc closure trong
   `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`;
7. chuyển `session_prompt/CURRENT_HANDOFF.md` sang Reviewer/next_design với next
   action duy nhất là hỏi Decision Queue #1 — lexical baseline/sparse consumer.

Không sửa extraction, implementation reports, frozen survey, runtime/tests/
corpus/Golden/index/dependencies hoặc reference repository. Sau các cập nhật,
Reviewer chạy `git diff --check`, targeted status/link consistency checks và
giữ `Git authorization: none`.

Next handoff sau closure: Reviewer hỏi User đúng một quyết định về lexical
baseline/sparse consumer, ghi câu trả lời vào guide/decision notes trước khi
hỏi quyết định kế tiếp. Written Spec và Plan vẫn đóng.

### 8.4. User confirmation và closure — 2026-09-11

User đã gửi đúng xác nhận:

```text
Tôi xác nhận closure Verified Architecture Extraction.
```

Closure decision: extraction được công nhận là **approved evidence companion**
cho full-corpus design. Survey 885 dòng vẫn frozen/working/non-canonical. Xác
nhận không phê duyệt runtime, Written Spec, Implementation Plan, benchmark,
collection mutation, Git write hoặc quyết định nào còn mở.

Reviewer đã đồng bộ các tài liệu docs-only thuộc §8.3 và chuyển handoff sang
`Reviewer/next_design`. Next action duy nhất là hỏi Decision Queue #1 — lexical
baseline/sparse consumer; chỉ sau câu trả lời mới cập nhật guide/decision notes
và chuyển sang quyết định tiếp theo.
