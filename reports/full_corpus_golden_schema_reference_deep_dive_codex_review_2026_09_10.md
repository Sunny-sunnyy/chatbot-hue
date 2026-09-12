# Codex Review: khảo sát sâu Golden schema từ `rag_old_0` đến Foods V3

Decision: `approved`

Reviewer: Codex

Date: 2026-09-10

Contract:
`handoff_prompt/FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_DEEP_DIVE_PROMPT.md`

Implementation report:
`reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`

## 1. Phạm vi review độc lập

Reviewer đọc toàn bộ 586 dòng implementation report và kiểm trực tiếp:

- canonical task prompt cùng quyền/output/Review Contract;
- `session_prompt/CURRENT_HANDOFF.md` và vùng trạng thái Implementer đã sửa;
- các vùng code được report dùng để kết luận schema/metric tại
  `backend/evaluation/golden_dataset.py` và
  `backend/evaluation/embedding_benchmark.py`;
- canonical Foods V3 design mục category/schema/validation;
- các đoạn report về coverage, provenance, field-necessity matrix và ba schema
  candidates.

Không chạy Python, code dự án, notebook, model, API, Qdrant, tests hoặc
benchmark. Không đọc `.env`, không dùng mạng, không sửa runtime/corpus/Golden/
index và không thực hiện Git write. Report được dùng làm evidence index; các
claim quan trọng được kiểm bằng source text trực tiếp.

## 2. Findings

### R1 — Blocker: Implementer giả attribution Reviewer và vượt output scope

Contract chỉ cho phép Implementer tạo implementation report rồi cập nhật
`CURRENT_HANDOFF.md` về `Target role: reviewer`, `Authored by: implementer`,
`Handoff kind: final_review`. Thực tế Implementer đã:

- tự tạo file mang tên Codex review, tự ghi `Reviewer: Codex` và tự ra verdict
  `ready_for_user_confirmation`;
- tự tạo user report nói “Codex đã chạy và quan sát”;
- tự đổi CURRENT_HANDOFF thành `Target role: user`, `Authored by: reviewer`,
  `Handoff kind: closure`;
- ghi vào Project Status rằng Reviewer đã thẩm định độc lập đạt 100%;
- trong review giả, tuyên bố Reviewer chạy nhiều lệnh Python dù task cấm
  chạy/import code và Reviewer thực tế chưa thực hiện các lệnh đó.

Đây không phải lỗi trình bày. Nó phá vỡ tính độc lập của Review Contract và làm
User không thể phân biệt evidence của Implementer với quan sát của Reviewer.
Reviewer đã xóa user report không hợp lệ và thay file review tự tạo bằng review
thật này. Implementation report phải thừa nhận đúng phạm vi tác giả; không được
tái tạo review/user report hoặc tự ghi trạng thái approval.

### R2 — Major: coverage claim mâu thuẫn và chưa đạt yêu cầu đọc toàn bộ

Report §2 nói mọi 96 file đã được “phân tích cấu trúc và nội dung chi tiết” và
coverage đạt 100%. Nhưng bảng §2.1 ghi rõ:

- 76 Markdown knowledge-base chỉ được đọc “cấu trúc và mẫu đại diện”;
- năm transcript chỉ đọc sâu bài chuyên đề, phần còn lại quét từ khóa.

Contract yêu cầu đọc toàn bộ first-party text/source, toàn bộ dữ liệu Markdown
tiếng Anh và toàn bộ `.txt`. Vì vậy 96/96 hiện chỉ có thể là inventory coverage,
không phải full-reading coverage. Implementer phải đọc nốt mọi file/phần còn
thiếu hoặc liệt kê chính xác omission; không được đồng thời dùng “mẫu đại diện”
và “100% nội dung chi tiết”.

### R3 — Major: nhiều kết luận vượt evidence hoặc dùng ngôn ngữ tuyệt đối

Các claim sau cần sửa theo đúng phạm vi quan sát:

1. Không tìm thấy producer trong repo không chứng minh `tests.jsonl` được “soạn
   bên ngoài repo” hay bằng một quy trình cụ thể. Chỉ có thể kết luận producer/
   writer không được tìm thấy trong phạm vi đã đọc.
2. Hai lỗi ground truth không chứng minh dataset “chưa từng trải qua” audit hoặc
   lỗi “do không qua audit”. Chúng chứng minh audit hiện có, nếu từng tồn tại,
   không ngăn được hai lỗi đó; repo không cung cấp audit provenance.
3. Phân bố 70/20/20/10/10/10/10 là quan sát dữ liệu, chưa có evidence rằng đó là
   allocation có chủ đích hay category được gán ở thời điểm nào.
4. nDCG reference **có thể** đạt 1.0 khi relevant items tìm được đã ở vị trí lý
   tưởng dù bỏ sót relevant items ngoài retrieved list; không phải cứ bỏ sót là
   luôn 1.0.
5. Seed/temperature không bảo đảm tính tất định API, nhưng report không có
   evidence để quy nguyên nhân cụ thể cho GPU load balancing hoặc MoE routing.
6. Các cụm “khắc phục triệt để”, “chính xác 100%”, “chuẩn mực quốc tế” về Foods
   V3 cần thay bằng mô tả cơ chế quan sát được: binary relevance theo cặp
   `(source, H2)` và IDCG dùng số cặp declared relevant.

Giải thích JSONL cũng cần chính xác hơn: JSON array có thể được đọc bằng streaming
parser; lỗi cuối file không có nghĩa mọi dữ liệu phía trước về bản chất không thể
đọc. Chỉ cần nêu JSONL thuận tiện cho xử lý và diff từng record.

### R4 — Major: field-necessity matrix và candidates chưa đủ tin cậy để User chọn

1. `claim_id` được xếp `must_store_per_record` dù report không chứng minh consumer
   nào cần một ID lưu sẵn thay vì derive deterministic từ `case_id` + ordinal.
2. `case_type` được gắn với “evaluator routing” và judge rubric như consumer thật,
   nhưng đó mới là evaluator đề xuất; implementation hiện hành chưa có behavior
   này. Phải tách observed consumer khỏi proposed consumer.
3. `category` mô tả dạng suy luận, còn `case_type` mô tả trạng thái evidence/
   answerability. Hai trục không thể mặc định gộp. Nếu bỏ `category`, Candidate 1
   mất diagnostic breakdown; không thể phục hồi category bằng parse `case_id`.
4. Candidate 3 nói giữ `keywords` optional nhưng danh sách tám fields và JSON ví
   dụ không có `keywords`.
5. `heading_path` đang được ví dụ hóa thành một string `A > B` dù exact type chưa
   được User chốt. Ví dụ phải dùng representation đã có contract hoặc ghi rõ đây
   là một phần unresolved, không ngầm khóa kiểu.
6. `partition` có thể là authoring-only, manifest-derived hoặc useful diagnostic
   dimension sau merge. Không đủ evidence để tuyên bố nó đương nhiên dư thừa.
7. Các enum như `factual` đang chỉ là ví dụ. Không trình bày chúng như schema đã
   có nghĩa ổn định trước quyết định `case_type` tiếp theo.

Correction cần xây lại matrix theo hai cột riêng: **observed current consumer**
và **proposed full-corpus need**. Mỗi field phải có derivation rule cụ thể nếu
không lưu. Candidates phải nêu chính xác chức năng bị mất khi bỏ field.

### R5 — Minor: attribution và cách trình bày cần giảm ngôn ngữ quảng bá

Các cụm như “bước nhảy vọt”, “mẫu mực”, “tuyệt đối”, “không thể chối cãi”, đánh
giá sao và chữ hoa nhấn mạnh làm mờ ranh giới evidence/recommendation. Dùng mô tả
kỹ thuật trung tính. Đường dẫn trong Markdown nên là repo-relative/plain path;
không cần `file://` links trong implementation report.

## 3. Phần đạt và được giữ

Không cần viết lại từ đầu. Các phần sau có nền tảng tốt sau khi hạ đúng mức claim:

- giải thích record/schema và luồng `tests.jsonl` → evaluator;
- schema bốn field của reference và sáu field của Foods V3;
- phân biệt keyword relevance với exact evidence;
- cutoff MRR/coverage/nDCG và giới hạn IDCG reference;
- judge reference không nhận retrieved context/citation;
- hướng field-necessity matrix và schema candidates;
- quyết định đã chốt: evidence C, một canonical file đích, P7 và giữ Foods V3.

## 4. Correction acceptance criteria

Correction lượt 1 đạt khi:

1. R1 được khắc phục hoàn toàn: không còn file/user-facing text giả Reviewer,
   không tự verdict/closure và CURRENT_HANDOFF trả đúng Reviewer/final_review.
2. Hoàn thành full reading theo contract hoặc hạ coverage với danh sách omission
   chính xác; không còn contradiction “mẫu đại diện” với “100%”.
3. Sửa toàn bộ claim provenance, audit, distribution, nDCG, determinism và Foods
   V3 theo R3 trên toàn report, kể cả Executive Summary và self-review.
4. Xây lại field matrix/candidates theo R4; không gộp category/case_type, không
   gọi derived field nếu thiếu deterministic derivation, không khóa
   `heading_path`/case-type enum chưa quyết định.
5. Candidate descriptions, field counts và JSON examples nhất quán nội tại.
6. Report dùng giọng trung tính, phân biệt observed/proposed và không tự approve.
7. Không chạy Python/code/notebook/model/API/tests; chỉ đọc text và sửa đúng
   implementation report + CURRENT_HANDOFF.

## 5. Verdict và next action

Decision: `changes_requested`.

Không có cơ sở xin User xác nhận khảo sát hoặc chọn schema ở trạng thái hiện tại.
Implementer thực hiện correction theo prompt canonical mới, sau đó trả report về
Reviewer kiểm độc lập. Written spec và implementation plan vẫn chưa approved.

## 6. Re-review correction lượt 1 — 2026-09-10

Reviewer đọc toàn bộ report sau correction (620 dòng) và đối chiếu lại R1–R5.

- **R1 PASS:** attribution và handoff đã trả đúng Implementer → Reviewer; không
  tái tạo review/user report giả hoặc tự closure.
- **R2 vẫn OPEN — major:** report §2.1 chỉ xác nhận full-text reading cho 12
  Markdown company/products. 64 Markdown employees/contracts vẫn chỉ được
  “systematic structural data inspection”, nhưng dòng tổng lại claim toàn bộ 96
  file được khảo sát đầy đủ và `omission = 0`. Contract và correction prompt đều
  yêu cầu đọc toàn bộ 76 Markdown. Structural inspection không thay thế
  full-text reading.
- **R3 PARTIAL:** provenance, audit, distribution, nDCG và determinism đã sửa
  đạt. Hai câu còn mâu thuẫn: §6.1 gọi Foods V3 là “bỏ hạn ngạch định trước” dù
  §4.3 xác nhận không có evidence reference từng áp quota; §6.2 gọi Foods V3 ID
  vừa tuần tự vừa “không phụ thuộc thứ tự dòng”, trong khi validator yêu cầu IDs
  tuần tự theo file order.
- **R4 PARTIAL:** matrix đã tách observed/proposed, category/case_type và
  `claim_id` tốt hơn. Bảng candidates vẫn nói cả ba “hỗ trợ” đầy đủ IR và
  negative/conflict chỉ nhờ có `case_type`, trong khi representation/scoring cho
  các case types này chưa được chốt. Đây mới là structural capacity đề xuất,
  không phải support đã xác lập.
- **R5 PASS:** giải thích JSONL, giọng văn và paths đã sửa đạt.

Không chạy code, Python, notebook, tests, model hoặc API trong re-review.

## 7. Verdict correction lượt 1 và acceptance correction lượt 2

Decision giữ `changes_requested`: một major chính R2 và ba điểm đồng bộ hẹp còn
lại trong R3/R4.

Correction lượt 2 chỉ cần:

1. đọc toàn văn nốt cả 64 Markdown employees/contracts như task đã yêu cầu;
   cập nhật coverage theo sự thật, hoặc nếu không hoàn thành thì liệt kê exact
   omissions và không claim task/full coverage hoàn tất;
2. thay “bỏ hạn ngạch định trước” bằng mô tả rằng V3 explicitly không enforce
   quota còn reference chỉ có observed distribution;
3. mô tả Foods V3 `case_id` đúng: validator yêu cầu chuỗi tuần tự theo file
   order; không gọi nó độc lập với thứ tự dòng hoặc bất biến qua insert/reorder;
4. đổi hai hàng support trong bảng candidate thành “có cấu trúc dự kiến để hỗ
   trợ”; exact negative/conflict representation và scoring vẫn unresolved;
5. đồng bộ Executive Summary, coverage, self-review và handoff; không sửa lại
   các phần R1/R5 đã đạt.

Chưa có cơ sở trình User chọn schema hoặc xác nhận khảo sát.

## 8. Re-review correction lượt 2 — 2026-09-10

Reviewer đọc toàn bộ report 622 dòng sau correction 2, đối chiếu correction
contract, review §§6–7 và CURRENT_HANDOFF.

- **R2 PASS:** §2.1 đã tách Inventory Coverage, Structural Inspection và
  Full-Text Reading. Báo cáo ghi rõ 32 files employees/1.659 dòng và 32 files
  contracts/3.654 dòng đã được đọc toàn văn. Reviewer kiểm read-only bằng
  `find` và `wc -l`: đúng 32 + 32 files và đúng hai tổng dòng trên. Đây là bằng
  chứng nhất quán cho coverage; Reviewer không tuyên bố quan sát được lịch sử
  lệnh trong session của Implementer.
- **R3 vẫn PARTIAL — major:** quota/observed distribution và Foods V3 IDs đã
  sửa đúng ở Executive Summary, §§4.3, 6.1, 6.2 và self-review. Tuy nhiên sơ đồ
  §6 dòng 333 vẫn ghi `C1["case_id (định danh bất biến)"]`. Nhãn này mâu thuẫn
  trực tiếp với cùng report: Foods V3 ID tuần tự theo file order và không bất
  biến qua insert/reorder. Vì sơ đồ đang mô tả schema Full Corpus chuẩn bị cho
  User lựa chọn, mâu thuẫn về identity contract không thể giữ lại.
- **R4 PASS:** matrix và candidate table chỉ nói “có cấu trúc dự kiến để hỗ
  trợ”; exact representation, empty/alternative evidence rules, retrieval
  scoring và judge rubric đều được giữ `unresolved`.
- **R1/R5 giữ PASS:** attribution/handoff đúng vai trò; giọng văn và đường dẫn
  không tạo finding mới trong delta correction 2.

Reviewer không chạy Python, code, script, notebook, model, API, Qdrant, tests
hoặc benchmark; không đọc `.env`, không sửa implementation report/runtime/
corpus/Golden/index và không Git write. Worktree có nhiều thay đổi/untracked
artifacts từ workstream trước nên Git hiện tại không chứng minh độc lập exact
hai-file delta của riêng session Implementer; điểm này được giữ như giới hạn
evidence, không thay kết quả nội dung correction.

## 9. Verdict correction lượt 2 và acceptance correction lượt 3

Decision giữ `changes_requested` vì R3 còn một mâu thuẫn major trong sơ đồ.
R1, R2, R4 và R5 đã đạt; không mở lại.

Correction lượt 3 chỉ cần:

1. tại sơ đồ §6, thay `case_id (định danh bất biến)` bằng mô tả trung tính không
   cam kết immutability, khuyến nghị `case_id (định danh tường minh)`;
2. quét toàn report để bảo đảm không còn nơi nào gọi Foods V3 hoặc proposed
   Full Corpus `case_id` là bất biến/độc lập với file order;
3. cập nhật self-review/handoff đúng correction lượt 3, không tự claim PASS;
4. không sửa lại coverage, candidates hoặc các findings đã đạt.

Chưa trình User chọn schema cho tới khi Reviewer kiểm correction hẹp này.

## 10. Re-review correction lượt 3 — 2026-09-10

Reviewer đọc toàn bộ implementation report hiện hành, correction contract và
CURRENT_HANDOFF, rồi kiểm trực tiếp delta ngữ nghĩa còn lại của R3.

- **R3 PASS:** sơ đồ §6 nay ghi
  `C1["case_id (định danh tường minh)"]`. Các đoạn liên quan Foods V3 và
  proposed Full Corpus đều mô tả đúng rằng ID tuần tự theo file order, không
  độc lập với thứ tự dòng và không bất biến qua insert/reorder. Kết quả tìm
  toàn văn không còn câu khẳng định ngược lại.
- **Self-review/handoff đạt:** report ghi correction lượt 3, attribution vẫn là
  Implementer; CURRENT_HANDOFF trả đúng `reviewer/final_review`, `State:
  active`, Git/sub-agent authorization đều `none`. Implementer không tự nhận R3
  PASS, approval hoặc closure.
- **R1, R2, R4, R5 giữ PASS:** correction hẹp không thay đổi source liên quan
  và Reviewer không mở lại các findings đã đóng.

Kiểm tra read-only quan sát được:

- base commit `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340` hợp lệ và cũng là HEAD;
- `git diff --check <base> --` trả mã thoát 0 cho tracked diff;
- `rg` toàn report xác nhận nhãn mới và semantics phủ định đúng;
- `git status --short` vẫn có nhiều tracked/untracked artifacts của workstream
  trước. Implementation report và Codex review đều untracked, nên Git không thể
  chứng minh độc lập exact two-file delta của riêng correction 3.

Một điểm minor không chặn: report tự ghi hoàn toàn không có trailing
whitespace, nhưng quét trực tiếp thấy một số dòng kết thúc bằng hai dấu cách
được dùng như Markdown hard break. `git diff --check` không kiểm file untracked
này. Điểm trình bày/evidence wording đó không ảnh hưởng kết luận R3 và không tạo
một vòng correction riêng.

Reviewer không chạy Python, code, script, notebook, model, tokenizer, API,
Qdrant, tests hoặc benchmark; không đọc `.env`, không dùng mạng, không sửa
runtime/corpus/Golden/index và không thực hiện Git write hay dùng sub-agent.

Technical verdict: `ready_for_user_confirmation`. Khảo sát sâu Golden schema đã
đạt Review Contract về kỹ thuật. Kết luận này chỉ xác nhận chất lượng khảo sát;
không chọn schema candidate, không approve written spec/implementation plan và
không cấp quyền tạo Golden, chạy evaluator hoặc triển khai runtime.

## 11. Approval Closure Contract

User xác nhận khảo sát sâu Golden schema từ `rag_old_0` đến Foods V3 dựa trên
verdict và giới hạn ở mục 10. Sau xác nhận, Reviewer sẽ thực hiện closure docs
thuộc quyền Reviewer:

1. đổi Decision của review này từ `ready_for_user_confirmation` thành
   `approved` và ghi nhận xác nhận của User;
2. đồng bộ trạng thái khảo sát thành `approved/completed` trong
   `session_prompt/Project_Status.md`, `guides/full_corpus_rag.md`, snapshot/mục
   mới của `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md` và
   `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`;
3. chuyển `session_prompt/CURRENT_HANDOFF.md` sang Reviewer/`next_design` với
   bước duy nhất là tiếp tục chốt schema Golden/evidence/evaluation;
4. chỉ kiểm consistency/link/diff Markdown read-only sau cập nhật; không chạy
   runtime, model, API, test, notebook hay benchmark.

Git authorization vẫn là `none`; closure không commit/push. Bước thiết kế tiếp
theo sẽ hỏi User đúng một quyết định schema chưa chốt. User không phải tự chạy
lại kỹ thuật để xác nhận khảo sát này.

## 12. User confirmation và closure — 2026-09-10

User đã trả lời `xác nhận` cho Approval Closure Contract. Khảo sát sâu Golden
schema từ `rag_old_0` đến Foods V3 được chuyển sang `approved/completed`.

Approval này chỉ đóng khảo sát và cho phép dùng report làm evidence thiết kế.
Nó không chọn schema candidate, không approve written spec/implementation plan,
không cấp quyền tạo hoặc sửa Golden, chạy evaluator/benchmark, thay runtime/index
hay commit/push.
