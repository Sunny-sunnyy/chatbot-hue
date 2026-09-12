# Codex Review: khảo sát simplicity evaluation `rag_old_0`

Decision: `approved`

Reviewer: Codex

Date: 2026-09-10

Contract:
`handoff_prompt/FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_SURVEY_PROMPT.md`

Implementation report:
`reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md`

## 1. Phạm vi review độc lập

Reviewer đã đọc toàn bộ 380 dòng implementation report và kiểm trực tiếp:

- inventory của root reference và danh sách 20 file non-data/76 file
  `knowledge-base`;
- đủ 150 record `evaluation/tests.jsonl` cùng bốn field và phân bố category;
- `evaluation/test.py`, `evaluation/eval.py`, `evaluator.py`, `evaluator2.py`,
  `app.py`, hai implementation Basic/PRO;
- saved text/output liên quan trong `day4.ipynb`, `day5.ipynb` và hai
  transcript Day 4/Day 5;
- các quyết định Golden/evidence/citation hiện hành trong guide và working
  decision notes;
- base/worktree, changed/untracked files, tracked diff check và trailing
  whitespace của report.

Không chạy/import Python, code, test, notebook, model, API, Qdrant hay benchmark;
không đọc `.env`, không đọc nội dung `knowledge-base/**/*.md`, không dùng mạng,
không sửa runtime/corpus/Golden/index và không thực hiện Git write. Report chỉ
được dùng làm evidence index; các claim chính được đối chiếu bằng source text.

## 2. Phần đạt

Các kết luận sau có source support và được giữ nguyên sau correction:

- root có 20 file first-party non-data trong scope và 76 Markdown data chỉ cần
  inventory; tổng 150 test cases cùng phân bố 70/20/20/10/10/10/10 là đúng;
- `tests.jsonl` có bốn field `question`, `keywords`, `reference_answer`,
  `category` ở cả 150 record;
- nhánh retrieval dùng `question` và `keywords`; MRR, nDCG và coverage đều là
  keyword-substring proxy, được tính per keyword rồi mean thành điểm case;
- MRR quét toàn danh sách được trả về, còn nDCG cắt `[:10]`; IDCG chỉ sắp xếp
  relevance trong chính top kết quả đã lấy nên không biết relevant items bị bỏ
  ngoài retrieved list;
- nhánh answer đưa `question`, generated answer và `reference_answer` vào LLM
  Judge; retrieved chunks, keywords, category và citation/evidence không được
  đưa vào prompt judge;
- với đúng sáu điểm hiện tại của `rag_old_0`, không có code consumer cho
  `evidence`, `expected_claims` hoặc negative chunks.

## 3. Findings

### R1 — Major: coverage map chứa path ví dụ không tồn tại

Số lượng 96/20/76 đúng, nhưng report §2.2 nêu các contract như `Acme
Corporation`, `Zenith Insurance` và employee `Zachary Brooks` làm ví dụ path.
Không tên nào tồn tại trong inventory hiện hành; employee thực là `Tyler
Brooks`. Đây là lỗi evidence map, dù không làm thay đổi count.

Năm row notebook dùng logical-line count lớn hơn `wc -l` một dòng mỗi file,
trong khi tổng 10.344 lại là tổng `wc -l`. Correction chỉ cần dùng một quy ước
nhất quán hoặc bỏ cột line count; không cần đọc lại các file.

### R2 — Major: một số data flow và call-site không khớp source hiện hành

Report §3.1/§3.2 mô tả `evaluate_retrieval(..., fetch_context=...)` và
`evaluate_answer(..., answer_question=...)`; source hiện hành không có hai
dependency-injection parameter này. `evaluation/eval.py` import trực tiếp PRO
implementation rồi gọi trực tiếp hai hàm.

Report §3.3 gán `category_mrr`, `category_ndcg` và `category_accuracy` cho
`evaluate_all_*()` trong `evaluation/eval.py`. Thực tế các hàm đó chỉ yield kết
quả; aggregation tổng và theo category nằm trong `evaluator.py`/
`evaluator2.py`. Dashboard chỉ breakdown MRR và Accuracy theo category, không
breakdown nDCG, Coverage, Completeness hoặc Relevance.

Tham số `k` của `evaluate_retrieval` chỉ được truyền vào `calculate_ndcg`; nó
không điều khiển số tài liệu mà `fetch_context` retrieve. Với import hiện hành,
PRO `fetch_context` trả final top 10; `RETRIEVAL_K=20` là số lấy cho mỗi query
trước merge/rerank, không phải danh sách 10–20 docs mà MRR nhận. Các path:line
trong report cũng lệch đáng kể so với source hiện hành và phải được cập nhật.

### R3 — Major: kết luận schema đánh đồng sáu metric với toàn bộ requirement Hue

Kết luận tối giản đúng phải có hai tầng:

1. Nếu mục tiêu chỉ là tái tạo đúng sáu điểm keyword/reference-judge của
   `rag_old_0`, ba field `question`, `keywords`, `reference_answer` là đủ về dữ
   liệu metric; `category` chỉ cần cho breakdown và là optional trong schema
   đích nếu loader/aggregator cho phép thiếu.
2. Điều đó không chứng minh evidence/claims “vô nghĩa” cho Hue RAG. Citation
   tới nguồn thật và kiểm claim–source support/groundedness là requirement đã
   chốt riêng, nằm ngoài sáu điểm trên. Report phải trình bày đúng trade-off để
   User có thể quyết định có bỏ scope đó hay không.

Report còn gộp source-level offsets với chunk IDs rồi nói cả hai đổi khi
rechunk. Chunk IDs có thể đổi; exact offsets trên normalized source không đổi
chỉ vì thay chunking. Vì vậy §8.2 sai kỹ thuật.

Report không thực hiện đối chiếu bắt buộc với `evidence_groups`, `case_type`,
`partition`, `domain`, `claim_id`. Candidate B lại nói “100% trường đều có
consumer thực tế”, trong khi chính matrix xác nhận `case_id` không có consumer
trong `rag_old_0`. `case_id` cũng bị gọi là bất biến và cần cho concurrency mà
không có contract/source support. Candidate baseline bắt buộc phải có đúng ba
field metric với `category` optional, nhưng Candidate A hiện trình bày
`category` như field cố định.

### R4 — Major: claim định lượng và nhân quả không có evidence

Không có đo đạc nào trong scope hỗ trợ các con số “giảm hơn 70% công sức” hoặc
“tăng 200%–300% thời gian”. Tương tự, `case_id` không thể được gọi là “hoàn toàn
không làm tăng chi phí”, và việc reuse test harness không “chứng minh” schema
tối giản là nguyên nhân then chốt làm pipeline tốt hơn.

Snapshot hiện tại và transcript chỉ cho thấy bài học mô tả đổi import/interface
để tái sử dụng evaluator. Chúng không chứng minh lịch sử ba file eval/test
“không đổi một dòng” nếu không có version history/diff tương ứng. Hạ claim
thành observed course narrative; không suy quan hệ nhân quả hoặc mức tiết kiệm.

### R5 — Major: benchmark attribution và reproducibility chưa đạt contract

Các aggregate 0.7298, 0.7903, 0.9116, 3.99 và 4.62 tìm thấy trong transcript
Day 4/Day 5, không có trong saved output của hai notebook. `day4.ipynb` chỉ lưu
ví dụ một case tại vùng được dẫn; vùng cuối `day5.ipynb` là thử nghiệm câu hỏi
Manchester, không phải full benchmark. Các số 97.8%, Completeness 4.55 và
Relevance 4.71 không tìm thấy trong 20 file non-data bằng text search. Không
được gắn chúng với notebook hoặc trình bày như Reviewer-verifiable result; phải
gỡ hoặc ghi rõ nguồn/giới hạn nếu có evidence thật trong scope.

Report chỉ nhắc `evaluator2.py` có seed nhưng bỏ phần contract yêu cầu phân tích
temperature, repetitions và giới hạn tái lập. Source chỉ áp `seed=42` theo kiểu
best-effort trong `evaluator2.py`; core evaluator không đặt temperature, không
chạy repetitions và một lần chấm LLM không bảo đảm deterministic. Các ngưỡng
màu dashboard cũng chưa được tổng hợp dù prompt yêu cầu.

## 4. Correction acceptance criteria

Correction lượt 1 đạt khi:

1. giữ nguyên các kết luận đã đạt ở §2, sửa inventory examples và line-count
   convention mà không đọc lại data;
2. sửa signatures, imports, aggregation, cutoff/data flow và exact source
   locations theo R2;
3. tách rõ “đủ cho sáu metric `rag_old_0`” khỏi citation/groundedness đã chốt
   của Hue; sửa semantics source span/chunk ID và đối chiếu đủ các field mà
   contract yêu cầu;
4. có baseline ba field `question`/`keywords`/`reference_answer`, `category`
   optional; mọi field thêm phải ghi đúng observed hoặc proposed consumer;
5. bỏ toàn bộ phần trăm effort/cost và các từ “chứng minh”, “vô nghĩa”, “loại bỏ
   ngay” không được evidence hỗ trợ;
6. sửa benchmark attribution, bỏ ba số không truy được nguồn, và thêm mục ngắn
   về seed/temperature/repetitions/thresholds/reproducibility;
7. giữ giọng trung tính, không tự đổi quyết định canonical, không tự approval;
   chỉ sửa implementation report và `CURRENT_HANDOFF.md`.

## 5. Verdict và next action

Decision: `changes_requested`.

Chưa dùng Candidate B hoặc recommendation của report làm cơ sở đổi schema.
Implementer thực hiện correction hẹp theo prompt mới rồi trả lại Reviewer kiểm
độc lập. Không cần chạy code/test/notebook/model/API và không cần đọc lại
`knowledge-base`.

## 6. Re-review correction lượt 1 — 2026-09-10

Reviewer đọc toàn bộ report sau correction (375 dòng), đối chiếu C1–C5 với
source hiện hành, canonical field decisions và `CURRENT_HANDOFF.md`.

- **C1 PASS:** inventory examples nay đều là path có thật; năm notebook và tổng
  10.344 dòng đã dùng cùng quy ước `wc -l`.
- **C2 PARTIAL — major:** signatures, direct PRO import, vị trí aggregation và
  semantics của `k` đã sửa đúng. Tuy nhiên report vẫn dẫn `calculate_mrr` tại
  `eval.py:16-24` thay vì dòng 45–51, `calculate_ndcg` tại `eval.py:27-57`/
  `59-78` thay vì dòng 62–78, và `evaluator2.py` category aggregation tại dòng
  126/187 thay vì 132/216. Claim “đã cập nhật đúng toàn bộ file:line” chưa đạt.
- **C3 PARTIAL — major:** report đã tách đúng ba field metric, `category`
  optional, `case_id` operational, và sáu metric khỏi citation/groundedness.
  Nhưng matrix/candidate lại mở lại các cơ chế đã chốt bỏ: `claim_id` có một
  format tự sáng tạo rồi còn được lưu trong Candidate C; `case_type` được gắn
  proposed routing; `domain` bị gọi là derive từ directory/case-ID prefix dù
  không có consumer hoặc quy tắc prefix đã duyệt. Canonical hiện hành quy định
  không lưu `claim_id`, không lưu `case_type`, không lưu `domain`, và
  `partition` chỉ là authoring-only rồi strip khi merge. Candidate C còn dùng
  `claim_text` thay vì field `text` đã chốt.
- **C3 còn một overclaim metric:** exact claim/evidence groups có thể làm ground
  truth cho claim retrieval coverage/completeness và citation support, nhưng
  không tự chứng minh “True Corpus Retrieval Recall” hay một danh sách exhaustive
  mọi relevant chunk trong corpus.
- **C4 PASS:** các phần trăm effort/cost và suy diễn nhân quả đã được bỏ; reuse
  test harness nay được ghi đúng là course narrative.
- **C5 PARTIAL — minor:** benchmark attribution, các số bị loại, notebook scope,
  seed/temperature/repetition và UI thresholds đã sửa đạt. Câu quy nguyên nhân
  nondeterminism cho server drift và floating-point không có evidence trong
  khảo sát; chỉ cần kết luận seed best-effort + single run không tạo bảo đảm
  deterministic.

Kiểm tra định dạng read-only:

- `git diff --check <base> --` trả mã thoát 0 cho tracked diff;
- không có trailing whitespace trong report/handoff;
- worktree vẫn chứa nhiều thay đổi và artifact untracked của workstream trước,
  nên Git không chứng minh độc lập exact two-file delta của Implementer.

Reviewer không chạy Python, code, test, notebook, model, API, Qdrant hoặc
benchmark; không đọc `.env`/nội dung knowledge-base và không thực hiện Git write.

## 7. Verdict correction lượt 1 và acceptance correction lượt 2

Decision giữ `changes_requested` vì C2/C3 còn hai major hẹp. C1/C4 giữ PASS;
phần benchmark chính của C5 không mở lại.

Correction lượt 2 chỉ cần:

1. sửa tất cả source line references nêu trên bằng line hiện hành;
2. đồng bộ matrix và Candidate C với canonical: không lưu `claim_id`, dùng claim
   field `text`, không đề xuất `case_type`/`domain`, mô tả `partition` đúng là
   authoring-only và bị strip khi merge;
3. thay “True Corpus Retrieval Recall” bằng claim/evidence retrieval coverage
   hoặc completeness trong phạm vi ground truth đã khai báo;
4. bỏ nguyên nhân nondeterminism không được khảo sát, giữ kết luận giới hạn;
5. cập nhật self-review/handoff, không viết lại các phần đã đạt và không tự
   claim PASS/approval.

## 8. Re-review correction lượt 2 — 2026-09-10

Reviewer đọc toàn bộ report hiện hành (378 dòng), correction contract và
`CURRENT_HANDOFF.md`, rồi đối chiếu trực tiếp bốn nhóm còn mở.

- **C2 PASS về nội dung:** MRR/nDCG/case aggregation và category aggregation
  nay trỏ đúng source; signatures, direct PRO import và semantics `k` nhất
  quán. Hai anchor phụ cho hằng số `RETRIEVAL_K`/`FINAL_K` vẫn ghi dòng 21–22
  thay vì 27–28, và range `fetch_context` ghi 126–133 thay vì 128–134. Nội dung
  20 trước merge/rerank và tối đa 10 sau rerank là đúng. Đây là minor citation
  defect không làm đổi kết luận, không đáng mở correction lượt 3.
- **C3 PASS:** matrix phản ánh đúng canonical hiện hành: không lưu `claim_id`,
  `case_type`, `domain`; `partition` chỉ authoring/review và bị strip khi merge;
  Candidate C dùng claim field `text`, không chứa `claim_id`, và ghi rõ cú pháp
  `evidence_groups` chỉ minh họa khi semantics chi tiết còn unresolved.
- **Metric boundary PASS:** report chỉ claim retrieval coverage/completeness đối
  với expected claims/evidence groups đã khai báo, không gọi đó là exhaustive
  corpus recall.
- **C5 PASS:** kết luận reproducibility chỉ dựa trên seed best-effort, core
  settings và single repetition; các nguyên nhân không được khảo sát đã bị bỏ.
- **C1/C4 và benchmark attribution giữ PASS:** correction lượt 2 không mở lại
  các phần đã đóng.

Kiểm tra định dạng read-only:

- `git diff --check <base> --` trả mã thoát 0 cho tracked diff;
- không có trailing whitespace trong report/handoff;
- worktree vẫn có nhiều tracked/untracked artifacts từ workstream trước nên
  Git không chứng minh độc lập exact two-file delta của Implementer.

Reviewer không chạy Python, code, test, notebook, model, API, Qdrant hoặc
benchmark; không đọc `.env`/nội dung knowledge-base, không dùng mạng và không
thực hiện Git write.

## 9. Verdict correction lượt 2

Decision: `ready_for_user_confirmation`.

Khảo sát đủ tin cậy làm evidence đầu vào cho bước thiết kế. Kết luận giới hạn
được chấp nhận là:

- đúng sáu metric kiểu `rag_old_0` chỉ cần `question`, `keywords`,
  `reference_answer`; `category` optional cho breakdown;
- `case_id` là metadata vận hành của Hue, không phải input của sáu metric;
- `expected_claims`/`evidence_groups` không cần cho sáu metric đó, nhưng phục vụ
  scope khác: declared-evidence retrieval coverage, citation verification và
  claim-source groundedness;
- việc giữ hay bỏ scope khác này là quyết định sản phẩm/đánh giá của User, không
  thể suy ra chỉ từ việc `rag_old_0` không triển khai nó.

Không sửa canonical decisions trong bước review này. Sau khi User xác nhận đóng
khảo sát, Reviewer tiếp tục guide → written spec → implementation plan và hỏi
từng quyết định kiến trúc một.

## 10. User confirmation và closure — 2026-09-10

User trả lời `xác nhận`. Khảo sát simplicity evaluation `rag_old_0` được đóng ở
trạng thái `approved/completed` và được dùng làm evidence đầu vào cho thiết kế.

Approval này xác nhận các kết luận giới hạn tại §9; nó không tự giữ hoặc loại
`expected_claims`/`evidence_groups`, không approve written spec/implementation
plan và không cấp quyền sửa runtime/corpus/Golden/index hay chạy evaluation.
Quyết định tiếp theo thuộc User là scope citation/groundedness trong official
Golden/evaluation.
