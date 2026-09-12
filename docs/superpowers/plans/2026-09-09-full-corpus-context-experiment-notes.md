# Full-corpus RAG — ghi chú cho kế hoạch evaluation và thử nghiệm context

Trạng thái: ghi nhận hướng thử nghiệm user yêu cầu để đưa vào plan sau này;
không phải implementation plan/Review Contract, chưa cấp quyền code hoặc chạy.

Quyết định liên quan: [bản ghi dành cho spec](../specs/2026-09-09-full-corpus-context-decisions.md).

Guide umbrella: [Full-corpus RAG](../../../guides/full_corpus_rag.md). Written
spec đích chỉ được soạn sau khi khảo sát schema qua review và các quyết định
kiến trúc còn mở được chốt. File này vẫn là working notes dù nằm trong thư mục
`plans/`.

## Đồng bộ guides, spec và implementation plan

User yêu cầu Reviewer sở hữu việc đồng bộ guides và viết spec/plan đủ chi tiết
cho Implementer, tránh over-engineering. Chỉ dùng simplicity reports của phase
liên quan khi đối chiếu evidence lịch sử; đọc theo thứ tự thay đổi và kiểm code.
Việc này không thay điểm duyệt written spec rồi plan/Review Contract riêng.

- Guide: hành vi của phase, input/output, phạm vi, cách dùng và acceptance;
  phân biệt Foods đã thực hiện với full-corpus đang thiết kế.
- Spec: quyết định, data flow, contracts, ví dụ corpus và lý do thay đổi;
  giải quyết các điểm mở trước khi trình duyệt written spec hoàn chỉnh.
- Implementation plan: thứ tự thay đổi, affected files/consumers, checks,
  evidence và Review Contract. Chỉ viết bản triển khai sau khi spec được duyệt.
  Không khóa tên hàm/class nội bộ nếu không cần cho consumer contract.
- Reports: bằng chứng thực hiện/kiểm chứng, giữ nguyên lịch sử, không chép
  toàn bộ lệnh hoặc test counts vào guides/spec.

Thứ tự phụ thuộc cần đưa vào plan đầy đủ:

1. Chốt chunk output qua mẫu thật, source locator và token budget; cập nhật
   chunker/splitter và discovery theo contract mới.
2. Cập nhật embedding input, Qdrant payload/ingestion và startup để nhận contract;
   thay count gate 572 bằng kiểm tra theo input ingest thực tế.
3. Cập nhật retrieval/scoring/reranking/context và generation/citation consumers;
   không để metadata bị bỏ tại payload allowlist hoặc bước build context.
4. Evaluation/benchmark theo corpus mới và frontend theo phạm vi MVP đã chốt.

Đây là ghi chú phụ thuộc, không là các bước thực thi đã authorize. Không tạo
provider framework, graph, version store, retry/resume hoặc test audit machinery
chỉ để chuẩn bị cho tương lai. Checks phải bảo vệ contract hoặc lỗi thực tế;
notebook có giá trị học tập và gọi public backend API.

## Hướng đã xác nhận

Xây pipeline MVP cơ bản trước; evaluation baseline rồi thử nghiệm các cách theo
[Phase 7](../../../guides/phase_7_retrieval_answer_evaluation.md) và
[Phase 8](../../../guides/phase_8_benchmark_model_selection.md), như cách đã làm
với Foods, trên toàn bộ corpus mới. Không chỉ đo riêng nhánh context mở rộng.

Các nhóm cần đưa vào thiết kế matrix: embedding local; dense-only, BM25-only,
dense → BM25 rescoring, true hybrid dense + BM25, TF-IDF-only và dense + TF-IDF;
fusion; no-rerank/rerank; end-to-end generation/answer evaluation. Đối chiếu
các amendments trong guides, không khôi phục máy móc model đã bị loại hoặc
mọi tổ hợp lịch sử. Exact candidates, settings và thứ tự thực thi sẽ được duyệt
trong plan đầy đủ; roadmap GPU/Qwen vẫn giữ theo context mới.

Giữ cách so sánh có kiểm soát, cùng dữ liệu/câu hỏi, tách kết quả từng domain và
nhóm câu hỏi, ghi lỗi và độ trễ thật. Foods metrics/thresholds/Golden và giới hạn
context là reference lịch sử, không tự thành acceptance toàn corpus. Khảo sát
Golden/evaluation reference đầu tiên đã qua correction R1–R4 và được User xác
nhận ngày 2026-09-10.

Khảo sát sâu schema và simplicity survey `rag_old_0` sau đó đều đã qua correction,
independent Reviewer review và User xác nhận `approved/completed`. Quyết định
mới nhất là schema metric-only gồm bốn required fields `question`, `keywords`,
`reference_answer`, `category`; không lưu `case_id`, `expected_claims`,
`evidence_groups`, source spans, chunk IDs, `case_type`, `domain` hoặc `claim_id`.
`partition` chỉ dùng trong authoring rồi bị strip khi merge.

User cũng chọn một full-corpus Golden canonical nhưng biên soạn/review theo
từng lĩnh vực trước. Plan sau phải tách authoring partitions khỏi official
evaluation input, merge deterministic chỉ sau quality approval, tạo smoke
deep-equal từ full file và retire partitions khỏi đường chạy chính. Foods V3
giữ nguyên; case phù hợp được copy và reclassify, không enrich evidence C. User
đã chọn P7: `foods`, `heritages`, `festivals`, `performing_arts`,
`travel_places`, `travel_services`, `travel_tickets`.

Không đặt hard quota trước curation; planning target toàn corpus khoảng 150–200
case. Không chia dev/test. Retrieval dùng MRR@10, nDCG@10 và Keyword Coverage@10;
Answer Evaluation dùng Accuracy, Completeness và Relevance. Overall và category
breakdown dùng macro-average theo case; không thêm micro/composite score. Ba
Answer metrics được chấm riêng bằng số nguyên 1–5 như `rag_old_0`; rubric từng
mức đã được chốt đầy đủ cho từng metric. Mỗi case dùng một judge prompt chỉ có
question/generated answer/reference answer, trả ba số nguyên và một feedback
ngắn; không thêm multi-pass/voting hoặc citation/groundedness scoring. Error
handling và thresholds vẫn chờ quyết định riêng.

Official aggregate cần đủ toàn bộ canonical cases. Retrieval thành công nhưng
rỗng nhận ba điểm retrieval bằng 0; generation thành công nhưng answer rỗng
nhận ba điểm Answer bằng 1. Technical error/timeout/judge failure hoặc output
judge không hợp lệ làm run `incomplete`; ghi case/stage/error và chạy lại case
lỗi trước khi aggregate. Không loại failure khỏi denominator, không chế điểm
hạ tầng và không thêm resume/retry framework nếu consumer hiện tại không cần.

Không đặt trước hard threshold hoặc diagnostic color bands cho sáu metric ở
full-corpus phase. Báo exact values, counts và category breakdown để so sánh
trên cùng Golden; không kế thừa các ngưỡng UI của `rag_old_0`. Review Contract
sau vẫn kiểm run completeness, schema/data validity và controlled comparison,
nhưng không biến các gate đó thành metric score thresholds.

Authoring `keywords` dùng một danh sách không rỗng các term/phrase quan trọng,
chính xác, có dạng chữ nguyên văn trong corpus liên quan và được reference answer
hỗ trợ. Giữ thực thể trung tâm cùng fact cụ thể được hỏi, như `Bánh ép` và tên
đường/địa chỉ khi case yêu cầu; không thêm generic words, synonym phòng xa, cả
câu hoặc duplicate. Vì metric mean theo keyword, không tách/lặp một phrase để
tăng trọng số. Không đặt quota keyword; quality review đối chiếu từng phần tử.

Implementer author working JSONL P7 từ curated corpus/tài liệu được giao, có thể
web-search về phương pháp viết câu hỏi tự nhiên, rõ ràng, dễ hiểu. Web không là
nguồn fact cho Golden. Category sơ bộ được chọn từ thao tác chính thể hiện trong
câu hỏi theo bảy định nghĩa chung, không multi-label/routing. User và Reviewer
đọc từng case, quyết định giữ, sửa/cập nhật, reclassify hoặc xóa; Implementer
thực hiện correction. Chỉ partition qua content review mới được merge.

P7 được author/review tuần tự theo thứ tự `foods`, `heritages`, `festivals`,
`performing_arts`, `travel_places`, `travel_services`, `travel_tickets`. Mỗi
partition phải qua Implementer self-review, User + Reviewer full-case review,
Implementer correction, Reviewer recheck và User confirmation trước partition
kế tiếp. Không author trước toàn bộ batch, không hard quota/padding và không
merge sớm; không thêm state machine hay approval database.

Mỗi P7 dùng `golden_full_corpus_authoring.jsonl` trong `evaluation/` của nhánh
corpus tương ứng: Foods, heritages, festivals, performing_arts và ba nhánh
travel. Foods artifacts lịch sử không bị sửa. Sau approval của cả P7, merge vào
`knowledge-base-hue/evaluation/golden_full_corpus.jsonl`; smoke nằm cạnh đó tại
`golden_full_corpus_smoke.jsonl`. Working files bị loại khỏi official evaluator
path sau merge. Việc tạo folder/file chờ approved implementation plan.

Smoke gồm đúng 10 rows chọn thủ công sau merge, mỗi P7 có ít nhất một case và
ba vị trí còn lại ưu tiên phủ thêm category. Implementer đề xuất; User và
Reviewer duyệt. Rows deep-equal và giữ thứ tự canonical; smoke không có field
riêng, không sửa độc lập và phải regenerate nếu canonical rows tương ứng đổi.
Không dùng random sampling/seed; smoke chỉ cho bounded check, không thay full
official evaluation.

Merge đọc approved P7 files theo thứ tự đã chốt, giữ internal row order, validate
`partition`, strip authoring field, rồi xáo toàn bộ concatenated rows bằng fixed
seed `42`. Output có đúng bốn fields theo canonical order và byte-identical khi
inputs/config không đổi. Chặn duplicate question sau trim/case-insensitive
comparison; không thêm semantic dedup model, global sort, ID, manifest/checksum
hay package state. Working files retire khỏi official evaluator path.

Sau khi canonical merge/shuffle hoàn tất, chạy full mọi canonical case cho cả ba
Retrieval metrics và ba Answer metrics. Planning target 150–200 không là quota;
smoke không thay full run. Complete-run/no-threshold contracts giữ nguyên. Exact
provider/model, pipeline matrix và execution authority phải có trong approved
plan trước khi chạy.

Qdrant baseline dùng ba isolated full-corpus collections cho E5-small, E5-base
và HuyDang; active/dense-candidate Foods giữ read-only. Controlled A/B cho
representation B có thể thêm ba B collections nếu cần giữ đồng thời, nên base
matrix dự kiến là 3–6 collections; đây không phải hard cap cho các experiment
variants được duyệt. Theo Decision #1 đã được User xác nhận,
mỗi candidate collection lưu cả dense và sparse named vectors trên cùng points:
baseline A query dense rồi BM25 local rescoring; hybrid candidate query dense và
sparse độc lập rồi fusion. BM25/TF-IDF ở ngoài Qdrant; reranker/fusion/scoring
không có collection riêng. Isolation là controlled benchmark choice của Hue,
không phải giới hạn named-vector tuyệt đối của Qdrant.
Decision #2 cho phép nhiều fresh experiment collections, không đặt hard cap khi
mỗi collection gắn với candidate/variant được duyệt. Target phải mới/rỗng; không
in-place reconcile. Exact replacement/cleanup cần target và approval riêng; sau
benchmark đề xuất giữ khoảng 1–3 collections tốt nhất. Exact schema/names và
cutover winner vẫn cần Decision Queue/spec/approval riêng.

## Evidence constraints từ initial survey `llm_rag` — 2026-09-11

Initial report đã chạm correction ceiling và bị đóng băng working/non-canonical.
Verified Architecture Extraction thay thế đã qua hai correction, independent
Reviewer review và User closure ngày 2026-09-11; artifact là approved evidence
companion. Những source checks Reviewer đã xác nhận đủ để ràng buộc plan sau này:

- không gọi dense-candidate + BM25 rescoring là true hybrid candidate retrieval;
  lexical scorer không thể lấy lại tài liệu nằm ngoài dense pool;
- không copy weighted sum dense cosine/raw BM25 mà thiếu normalization hoặc
  calibration; 0.6/0.4 chỉ là config, không là bằng chứng tỷ lệ đóng góp;
- không lưu Qdrant sparse vector khi không có sparse query consumer;
- nếu thử native sparse, vocabulary/token-index mapping phải reproducible và
  persist/coupled đúng với indexed points; không rebuild mapping độc lập theo
  process như reference;
- candidate collection phải bắt đầu sạch hoặc có replacement contract rõ;
  existing schema cần được verify, không upsert random UUID vào stale state;
- E5 query/document input phải giữ query/passage prefix đã chốt của Hue;
  reference dùng chung unprefixed embed function không được copy;
- số 450/1.486/48,84 chỉ là documented historical evidence, không là fresh
  benchmark hay live-state evidence.

Decision #1 đã chốt baseline A làm comparison control và hybrid làm candidate có
sparse consumer thật. Decision #2 chốt fresh-by-default, cho phép nhiều
experiment collections nhưng không tự cấp quyền tạo/cleanup collection hoặc
thêm manifest/alias/migration framework. Decision #3 chốt point ID và vectors ở
trường Qdrant chuẩn; payload chỉ giữ `search_text`, `source`, `title`,
`heading_path`, `evidence_parts`. Identity/fingerprint không lặp per-point.
Decision #4 chốt staged matrix: mỗi dense model so baseline A với native hybrid
bằng RRF; chỉ retrieval finalists so một reranker với no-rerank control.
Retrieval stage báo MRR@10, nDCG@10, Keyword Coverage@10; end-to-end finalists
báo đủ sáu metrics. Không full Cartesian matrix, composite hoặc winner/default
trước evidence; component failure làm run incomplete, không silent fallback.
Decision #5 chốt representation B theo staged finalists: A chạy thật trên toàn
matrix để chọn finalists, sau đó B dùng API thật, fresh indexes thật và
full-corpus A/B runs thật trên finalists với các biến nền tương đương. User chấp
nhận API/index cost; mock không là official evidence và execution authority vẫn
chờ approved Spec/Plan. Decision #6a chốt strict minimal success
`{answer,sources}` và typed non-2xx error; không partial success, silent
fallback hoặc automatic repair/retry. Decision #6b chốt budget linh hoạt theo
generator profile nhưng cố định trong từng run: trừ actual prompt/query/format
  overhead và fixed output reserve/safety margin, rồi pack whole chunks theo rank,
  tối đa 5; không skip/truncate/summarize. Decision #6c chốt
  `qwen/qwen3.5-9b` qua OpenRouter cho representation B và answer generation,
  pin một upstream provider cho mỗi run và không silent failover. LLM judge giữ
  `gpt-5.4-mini` qua OpenAI API. Decision #6d chốt Qwen `temperature=0`, B
  output 256, answer `context_limit=16384`, output reserve 2048, safety margin
  512, timeout 90 giây, không automatic retry/failover. Exact upstream phải
  preflight/pin/report trong approved run. Agentic RAG phải có profile và
  contract riêng cho tools, plan/state, steps và total budget; không dùng budget
  one-shot hiện tại. Decision #6e chốt UI inline: citation `[n]` cuộn/focus
  source card dưới answer, Markdown an toàn, loading/chặn duplicate submit và
  manual retry cho typed error; không streaming/history/agentic UI. Decision
  Queue tiền-spec đã hoàn tất. Reviewer đưa exact matrix vào
written spec/approved plan.

## Simplicity constraints cho spec/plan sau extraction — 2026-09-11

Complexity reset của survey `llm_rag` cho thấy tài liệu lặp cùng claim ở nhiều
summary/matrix/index làm tăng lỗi và chi phí review. Written spec/plan sau này
phải giữ một nguồn cho mỗi contract và chỉ thêm mechanism có consumer, failure
hoặc acceptance thật:

- không copy exhaustive inventory/config/test catalogue vào spec;
- không lặp requirement ở guide, spec, plan và traceability table; guide giữ
  rationale/trạng thái, spec giữ behavior/data contract, plan giữ steps/checks;
- chỉ lưu sparse khi có sparse query consumer; Decision #1 đã thỏa điều kiện này
  bằng hybrid candidate trong benchmark;
- không thêm alias/manifest/checksum/migration/automatic cleanup chỉ để phòng
  xa; fresh isolated candidate collection là lifecycle đã chốt;
- không tạo provider/plugin/registry/interface framework khi chỉ có một
  implementation thật;
- không triển khai representation B, context expansion hoặc nhiều thay đổi
  retrieval trong cùng baseline nếu chưa có câu hỏi thử nghiệm riêng;
- không đặt metric threshold/composite trước full-corpus baseline;
- line anchors chỉ dùng cho evidence companion/review, không biến mọi dòng code
  thành acceptance thủ công phải duy trì.

Khi User chọn một phương án phức tạp hơn, spec phải ghi consumer/risk cụ thể,
lợi ích cần chứng minh và phép so sánh kiểm soát tương ứng. Nếu không có, giữ
data flow trực tiếp và hoãn mechanism.

## Controls và các phép so sánh cần thiết kế

### Control cho benchmark embedding đã được user xác nhận

Dùng chung một bộ chunk cho E5-small, E5-base và HuyDang; kiểm input thực bằng
từng tokenizer trước embedding, gồm title/heading/prefix/special tokens theo
contract model. HuyDang dùng PyVi, E5 dùng query/passage prefixes; preprocessing
không thay bản evidence gốc. Giữ cùng boundaries, nội dung nền, questions và
retrieval/metric settings để so ảnh hưởng embedding model.

Không chia riêng từng model trong benchmark đầu tiên; không truncate âm thầm.
Đã có khảo sát chia Gia Lạc/Ngọ Môn/Ca Huế tới lượt 3; context mục 26 giữ số
đo/queries/spans và giới hạn evidence. Không thực hiện lại khảo sát này mặc định.
Exact packing và oversized groups cần hoàn thiện cùng parser; không coi lựa
chọn chung chunk set là approval chạy benchmark/runtime. MiniLM pair và
generator input budget được thiết kế riêng, không suy ra từ vài query mẫu.

### Control và candidate cho context expansion

Phần này độc lập với nhánh B có chọn lọc đã chốt bên dưới.

- Control: chỉ các chunk chính Top-5 trong ngân sách context.
- Candidate: cùng ranking và danh sách chunk chính trước bước đóng gói context,
  bổ sung điều kiện gốc liên kết, gộp trùng và giữ nhóm theo bản ghi spec.
- Giữ corpus/chunking, questions, embedding, retrieval/reranker, generator và
  ngân sách input tổng tương đương. Nếu lấy thêm điều kiện khiến ít chunk chính
  thực sự vào LLM hơn, ghi rõ ảnh hưởng đó trong kết quả.
- Official evaluation đo ba retrieval metrics và Accuracy/Completeness/Relevance
  theo schema metric-only. Citation support/evidence coverage không thuộc metric
  phase này; nếu cần cho một experiment runtime riêng thì phải có scope mới.
- Đọc các ca mất điều kiện lẫn ca thêm nội dung không liên quan để đánh giá
  lo ngại của user về câu trả lời mơ hồ với Qwen3.5 9B.
- Không dùng keyword xuất hiện trong ngữ cảnh API sinh để tự nâng relevance
  ground truth. Judge phase này không được mô tả như phép đo groundedness hoặc
  citation correctness.
- Chỉ đề xuất bật mở rộng context khi kết quả cho thấy lợi ích tương xứng độ
  phức tạp. Chưa chốt threshold hoặc tuyên bố candidate tốt hơn baseline.

Nhánh API preprocessing B và LLM boundary C vẫn giữ trạng thái trong context;
không gộp với thử nghiệm context này hoặc mặc định phải triển khai trước baseline.

## Control cho nhánh B có chọn lọc — user đã chọn lựa chọn 1

- Control là representation A trên nguyên bộ chunk A.
- Candidate giữ cùng boundaries, evidence và nội dung nền; bổ sung context
  do API sinh chỉ khi input hoàn chỉnh vừa cả ba tokenizer embedding đã chọn.
  Chunk không vừa giữ representation A; không truncate hoặc chia lại chunk.
- Giữ các biến còn lại tương đương khi so A/B cho từng model; không ghép
  thêm thay đổi fusion/reranker/context expansion vào cùng phép so ban đầu.
- Lưu context sinh riêng. Evidence dùng chấm điểm/citation vẫn là nguyên văn;
  từ khóa trong context sinh không tự chứng minh câu trả lời có căn cứ.
- Ghi số/tỷ lệ chunk được bổ sung và không được bổ sung, phân bố theo domain,
  cùng kết quả trên toàn bộ tập câu hỏi. Phân tích nhóm chịu ảnh hưởng là bổ
  sung, không thay kết quả toàn tập hoặc chỉ báo cáo những ca tốt lên.
- Không tạo bộ chunk nhỏ hơn riêng cho B, vector phụ hoặc metadata search
  trong lượt thử đầu. Provider/model/prompt, budget API, cách xử lý lỗi API
  và input của reranker/generator còn cần thiết kế trước execution approval.

Không coi lựa chọn này là quyền chạy thử nghiệm. Đây vẫn là ghi chú plan,
chưa phải approved implementation plan/Review Contract.

## Trạng thái chuẩn bị kế hoạch sau khảo sát parser approved

User đã approved khảo sát parser sau correction lượt 3; xem review mục 9–10
và context mục 29. Parser không còn chờ report/correction; extraction `llm_rag`
đã được User xác nhận closure. Written spec toàn corpus chưa được soạn: trước
hết Decision Queue phải được User chốt. Chỉ viết implementation plan/Review
Contract sau spec approval.

Parser đã chọn markdown-it-py với table enabled, source LF/Unicode spans.
Hai mẫu lead Ca Huế VN/QT cũ sai ranh giới, counts cũ không đại diện cho input
nguyên hàng. Hai composites đúng đã đo bổ sung và vừa limits theo exact input:
xem `reports/full_corpus_vn_qt_token_check_codex_review_2026_09_09.md` từ repo
root. Reviewer kiểm code/artifacts, không rerun; user đã approved khảo sát.
Không tự giao đo lại hoặc coi đây là approval runtime/models/Qdrant.

Reviewer sở hữu thiết kế/guides; code/tests/đo đạc giao prompt cho Implementer
qua user. Không spawn agent hoặc rerun mọi lệnh báo cáo. Những phần chưa chốt
(lexical baseline, ID/reindex/startup, payload/citation, candidate matrix,
representation B timing và budgets/API/frontend) theo current decision queue;
không biến roadmap thành acceptance core MVP.

## Golden organization và trạng thái khảo sát reference — 2026-09-10

- User chọn P7: bảy authoring partitions `foods`, `heritages`, `festivals`,
  `performing_arts`, `travel_places`, `travel_services`, `travel_tickets`.
- Official evaluator vẫn chỉ dùng một canonical full-corpus JSONL sau merge;
  smoke subset phải deep-equal với rows tương ứng trong full file.
- Canonical record có đúng bốn required fields `question`, `keywords`,
  `reference_answer`, `category`; không lưu `case_id`; evidence/claims/spans không thuộc official
  Golden/evaluation hiện hành.
- Không hard quota; planning target 150–200. Không dev/test. Retrieval cutoff
  `K=10`; tổng hợp macro-average theo case và breakdown theo category.
- Correction R4 đã qua independent Reviewer re-review. R1–R4 đều đóng; User đã
  xác nhận và khảo sát reference là `approved/completed`.
- Simplicity survey `rag_old_0` cũng đã approved/completed. Các phiên sau dùng
  implementation report và Codex review đã tạo; không phân tích lại source
  `rag_old_0` nếu không có câu hỏi mới ngoài phạm vi hai report.
- Written spec và implementation plan vẫn chưa approved; ghi chú này không cấp
  quyền tạo Golden, chạy evaluator hoặc sửa runtime/corpus/index.
