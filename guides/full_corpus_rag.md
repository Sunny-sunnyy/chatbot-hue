# Full-corpus RAG workstream

```text
Status: Wave 1 user-approved closure; Phase 3/Wave 2.1 design gate next
Runtime authorization: no Wave 2.1 implementation or live systems
Written spec: docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md
Implementation plan: approved — docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md
Review contract: approved — handoff_prompt/FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md
```

## Vai trò của guide này

Đây là entrypoint cho việc mở rộng MVP Foods sang toàn bộ curated corpus. Guide
này nối các thay đổi xuyên Phase 2–8 và phân biệt chúng với behavior Foods đã
được triển khai. Các guide phase hiện có vẫn là nguồn sự thật cho runtime Foods;
approval của full-corpus Written Spec không thay đổi approval lịch sử của chúng
hoặc tự approve implementation.

## Workflow tuần tự theo wave và guide

Spec/Plan hiện hành là umbrella. Mỗi wave sau Wave 1 chỉ được giao Implementer
sau chuỗi sau:

```text
evidence + closure wave trước
-> Reviewer cập nhật guide phase phụ thuộc
-> brainstorming từng quyết định còn mở
-> exact wave spec/addendum + implementation plan + Review Contract
-> User duyệt design package
-> Implementer thực hiện đúng một wave và báo cáo
-> Reviewer independent review/correction
-> User closure
-> đồng bộ guide/status rồi quay lại design gate kế tiếp
```

Guide phải tách `Foods as-built history`, `full-corpus approved target` và
`observed implementation result`. Không ghi kế hoạch thành kết quả đã chạy.
Không chờ Wave 6 mới cập nhật guide phase đã hoàn tất; Wave 6 chỉ rà soát tích
hợp cuối.

Thứ tự dependency:

| Design package | Guide canonical cần cập nhật trước implementation | Dependency |
|---|---|---|
| Wave 1 | Phase 2 | User closure 2026-09-12; observed offline preview recorded |
| Wave 2.1 | Phase 3 | Wave 1 technical review + User closure |
| Wave 2.2 | Phase 4 | Wave 2.1 closure; live index là approval riêng |
| Wave 2.3 | Phase 5 | Wave 2.2 code/index evidence theo gate |
| Wave 3 | Phase 6 | Wave 2.3 closure; live API là approval riêng |
| Wave 4 | Phase 7 Golden | Wave 3 closure; từng P7 closure tuần tự |
| Wave 5A | Phase 7 evaluator | Golden canonical closure |
| Wave 5B | Phase 8 | Evaluator/index readiness; từng paid stage riêng |
| Wave 6 | Các guide bị ảnh hưởng | Mọi wave cần thiết đã closure |

Nếu evidence làm thay đổi architecture, data/public contract hoặc quyền, dừng
để sửa và duyệt lại package; không hợp thức hóa sau khi Implementer đã làm.

Workstream bao phủ năm domain sản phẩm:

- `foods`;
- `heritages`;
- `festivals`;
- `performing_arts`;
- `travel`, gồm `places`, `services` và `tickets`.

## Trạng thái hiện hành

Curation và taxonomy toàn corpus đã hoàn tất. Khảo sát parser/source locator,
khảo sát hai input Ca Huế VN/QT và khảo sát Golden/evaluation reference đầu tiên
đã được Reviewer kiểm và User xác nhận. Các khảo sát này là evidence thiết kế;
chúng không cấp quyền sửa runtime, tạo Golden, ghi index hoặc chạy benchmark.

Khảo sát sâu về schema Golden đã qua correction lượt 3, independent Reviewer
review và được User xác nhận `approved/completed` ngày 2026-09-10. Kết quả là
evidence đầu vào cho thiết kế. User đã chọn hướng schema canonical tinh giản;
Spec/Plan umbrella đã approved, còn detailed Phase 7 package chỉ được soạn sau
closure các dependency trước đó.

Khảo sát complexity reset trên toàn bộ evaluation `rag_old_0` cũng đã qua hai
correction, independent Reviewer review và được User xác nhận
`approved/completed` ngày 2026-09-10. Khảo sát xác nhận sáu metric reference chỉ
cần `question`, `keywords`, `reference_answer`; `category` chỉ phục vụ
diagnostic breakdown. `case_id` từng được đề xuất làm metadata vận hành của Hue
nhưng đã bị User loại khỏi canonical vì chưa có consumer cần khóa ổn định.
`expected_claims`/`evidence_groups` không phục vụ sáu metric đó mà chỉ phục vụ
scope citation/groundedness riêng. User đã chọn loại scope này khỏi official
Golden/evaluation để tránh annotation và evaluator complexity không cần cho
các metric hiện tại.

Survey toàn project `llm_rag` đã chạm correction ceiling sau bốn verdict
`changes_requested`; report 885 dòng được đóng băng working/non-canonical.
Verified Architecture Extraction thay thế đã qua hai correction, independent
Reviewer review và được User xác nhận closure ngày 2026-09-11. Artifact này là
approved evidence companion cho design, không phải approval runtime/Spec/Plan.

Wave 1 initial review ngày 2026-09-12 yêu cầu Correction 1 cho năm Major; hai
review sau tạo các delta hẹp cho report/schema/cache/test evidence. Correction 3
đã đóng finding cuối và User xác nhận closure ngày 2026-09-12. Observed canonical
artifact là `PASS`: 205 sorted/unique files, 8460 chunks, ba condition rules,
zero errors/oversized; max token E5-small `366/512`, E5-base `366/512`, HuyDang
`255/256`. Implementer báo fresh offline suite `39 passed, 1 warning` và repeated
preview byte-identical; Reviewer chỉ static-review, không rerun dynamic checks.
Con số 8460 là observed result, không phải product invariant. Full backend/live
ingestion suites không thuộc Wave 1 acceptance vì dùng real embedder/Qdrant.

Wave 1 đã triển khai discovery, strict UTF-8/LF/hash, Markdown structure/spans,
condition exact-one matching, semantic split, exact `EvidencePart`, deterministic
chunk IDs/UUID5 và Representation A tokenizer preview. Wave này chưa embedding,
chưa tạo Qdrant point/build record, chưa retrieval/generation/API/UI/Golden/
benchmark. Foods runtime 572 points/chunks là as-built history riêng và không bị
Wave 1 cutover hoặc mutation.

## Quyết định đã chốt

- Golden đích là một file JSONL canonical cho official evaluation.
- Biên soạn và review dùng bảy working partitions P7: `foods`, `heritages`,
  `festivals`, `performing_arts`, `travel_places`, `travel_services` và
  `travel_tickets`.
- Chỉ merge sau khi từng partition đạt quality gate. Smoke rows phải deep-equal
  với các record tương ứng trong file canonical; partitions được rút khỏi đường
  chạy evaluator chính sau merge.
- Foods Golden V3 là artifact lịch sử được giữ nguyên. Các case Foods dùng cho
  Golden mới phải được copy, reclassify và review theo schema mới; không sửa
  file V3.
- Official Golden/evaluation không lưu `expected_claims`, `evidence_groups`,
  source spans hoặc chunk IDs. Quyết định Evidence C trước đây đã được User
  thay thế sau complexity reset; không còn alternative-evidence/locator design
  trong scope Golden hiện hành.
- Schema canonical giữ đúng bốn field bắt buộc `question`, `keywords`,
  `reference_answer`, `category`. `category` chỉ phục vụ thống kê/breakdown và
  không route evaluator hoặc đổi điểm case. `partition` chỉ tồn tại trong
  authoring/review P7 và bị loại khi merge; không lưu `case_id`, `domain` hoặc
  `claim_id`. Evaluator có thể sinh `case_index` từ thứ tự dòng để báo tiến độ/
  lỗi; giá trị này không được ghi vào Golden và không hứa ổn định qua phiên bản.
  `keywords` là relevance proxy theo substring cho ba retrieval metrics đã
  chọn, không được mô tả như exhaustive corpus relevance ground truth.
- Author `keywords` bám sát cách dùng của `rag_old_0`: một danh sách không rỗng
  gồm các từ/cụm từ quan trọng, chính xác và mang thông tin đáp án. Mỗi keyword
  phải có dạng chữ nguyên văn trong phần corpus liên quan và được
  `reference_answer` hỗ trợ; evaluator chỉ so khớp substring không phân biệt
  hoa/thường, không mở rộng synonym hay bỏ dấu. Với case về một quán như Bánh
  ép 1992, keywords cần giữ thực thể trung tâm như `Bánh ép` và thông tin cụ thể
  được hỏi như tên đường/địa chỉ khi đó là ý đáp án. Không dùng từ quá chung,
  cả câu, biến thể phòng xa hoặc keyword trùng nhau. Không tách một cụm có nghĩa
  thành nhiều token đồng nghĩa chỉ để tăng trọng số, vì mỗi keyword được tính
  ngang nhau trong metric case. Không đặt quota số keyword; content review giữ
  bộ nhỏ nhất vẫn đại diện đủ các ý chính cần truy xuất.
- Không lưu `case_type`: retrieval metrics không consume field này; answer
  thiếu/sai được phản ánh qua `reference_answer` và ba điểm Answer Evaluation.
  Chỉ xem lại nếu một scope tương lai thật sự cần nhiều rubric riêng.
- Official metrics gồm keyword-proxy MRR@10, nDCG@10, Keyword Coverage@10 và
  LLM-judge Accuracy, Completeness, Relevance.
- Ba Answer metrics được chấm riêng trên thang số nguyên 1–5 như reference
  `rag_old_0`. Không chuẩn hóa thành 0–1, không đổi thành pass/fail và không
  gộp ba điểm thành composite score.
- Judge dùng một prompt cho mỗi case, chỉ nhận `question`, generated answer và
  `reference_answer`, rồi trả ba số nguyên cùng một feedback ngắn. Mỗi metric có
  rubric đủ năm mức:

| Điểm | Accuracy | Completeness | Relevance |
|---:|---|---|---|
| 5 | Hoàn toàn nhất quán với reference, không có sai lệch thực chất | Bao phủ toàn bộ thông tin cần thiết trong reference để trả lời câu hỏi | Trả lời trực tiếp, tập trung, không có nội dung thừa đáng kể |
| 4 | Đúng về ý chính, chỉ có sai lệch nhỏ không đổi kết luận | Bao phủ hầu hết nội dung cần thiết, chỉ thiếu chi tiết nhỏ | Chủ yếu trực tiếp, chỉ có ít nội dung thừa hoặc lặp |
| 3 | Đúng một phần nhưng có ít nhất một sai lệch thực chất; vẫn còn giá trị sử dụng | Bao phủ khoảng một nửa hoặc chỉ một phần các ý chính | Có trả lời câu hỏi nhưng lan man, lặp hoặc lệch trọng tâm đáng kể |
| 2 | Phần lớn sai hoặc gây hiểu sai, chỉ còn ít nội dung đúng | Chỉ nêu một phần nhỏ, thiếu phần lớn ý chính | Chỉ chạm một phần câu hỏi; phần lớn nội dung không liên quan |
| 1 | Sai hoàn toàn, mâu thuẫn ý chính hoặc không có câu trả lời đánh giá được | Không nêu được thông tin cần thiết hoặc không có câu trả lời | Không trả lời câu hỏi hoặc nội dung không liên quan |

  Judge chấm ba tiêu chí độc lập và không dùng kiến thức ngoài prompt. Chi tiết
  được sinh thêm nhưng reference không xác nhận cũng không phủ nhận không tự bị
  coi là sai Accuracy; nếu làm câu trả lời lan man thì ảnh hưởng Relevance. Đây
  là answer-reference evaluation, không được diễn giải thành groundedness hay
  citation verification.
- Vocabulary `category` dùng chung cho toàn corpus gồm đúng bảy nhãn:
  `direct_fact`, `temporal`, `comparative`, `numerical`, `relationship`,
  `spanning`, `holistic`. Mỗi case có đúng một nhãn; category chỉ dùng để đếm
  và breakdown, không routing evaluator hoặc đổi scoring.
- Category được chọn theo thao tác chính mà câu hỏi yêu cầu, dựa trên chính câu
  hỏi chứ không dựa vào từ khóa bề mặt, domain hay vị trí nguồn:

| Category | Ý định chính của câu hỏi |
|---|---|
| `direct_fact` | Lấy một fact hoặc một nhóm fact nhỏ, trực tiếp về một đối tượng; dùng khi không có thao tác chuyên biệt hơn |
| `temporal` | Hỏi thời điểm, khoảng thời gian, trình tự hoặc thay đổi theo thời gian |
| `comparative` | So sánh rõ hai hay nhiều đối tượng, lựa chọn hoặc thời điểm |
| `numerical` | Câu trả lời chính là số lượng, giá, khoảng/range, khoảng cách hoặc phép tính; ngày/mốc lịch sử vẫn là `temporal` khi thời gian là ý định chính |
| `relationship` | Làm rõ quan hệ, vai trò, phụ thuộc hoặc liên hệ giữa các thực thể/khái niệm |
| `spanning` | Kết hợp nhiều ý/fact hữu hạn mà câu hỏi nêu rõ thành một câu trả lời |
| `holistic` | Tổng hợp rộng, giải thích tổng quan, lập kế hoạch hoặc đưa khuyến nghị trên một chủ đề |

  Nếu có nhiều dấu hiệu, chọn nhãn mô tả thao tác chính cần để trả lời. Phân
  biệt `spanning` với `holistic` bằng phạm vi: nhiều fact hữu hạn so với tổng
  hợp rộng. Không gắn nhiều nhãn; ca còn mơ hồ được giữ provisional để User và
  Reviewer quyết định trong content review.
- Implementer author các working JSONL P7 từ curated corpus và tài liệu được
  giao. Được web-search để học phương pháp viết câu hỏi/dữ liệu tự nhiên, rõ
  ràng, dễ hiểu và có giọng người; web không được đưa fact mới vào `question`,
  `keywords` hoặc `reference_answer` và không trở thành closed-world ground
  truth. Tránh template lặp máy móc. Implementer tự phân loại sơ bộ chỉ từ yêu
  cầu thể hiện trong câu hỏi. Sau khi author, User và Reviewer đọc từng case để
  quyết định giữ, sửa/cập nhật, reclassify hoặc xóa; correction nội dung được
  trả cho Implementer. Chỉ partition đã qua content review này mới được merge.
- P7 được thực hiện tuần tự theo thứ tự đã chốt: `foods`, `heritages`,
  `festivals`, `performing_arts`, `travel_places`, `travel_services`,
  `travel_tickets`. Với mỗi partition, Implementer author và self-review trước;
  sau đó User và Reviewer đọc mọi case, gom quyết định giữ/sửa/reclassify/xóa;
  Implementer xử lý correction và trả lại phần bị ảnh hưởng. Chỉ khi partition
  không còn required correction và được User xác nhận mới bắt đầu partition kế
  tiếp. Không hard quota/padding, không author trước sáu partition còn lại và
  không merge sớm.
- Working Golden nằm trong `evaluation/` của chính nhánh corpus, theo cùng cách
  tổ chức đã có ở Foods. Dùng một tên rõ là artifact authoring, không nhầm với
  canonical sau merge:

```text
knowledge-base-hue/foods/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/festivals/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/performing_arts/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/places/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/services/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/tickets/evaluation/golden_full_corpus_authoring.jsonl
```

  Sáu thư mục `evaluation/` chưa có sẽ chỉ được tạo ở implementation đã duyệt;
  thư mục Foods và Golden V2/V3 lịch sử giữ nguyên. Sau khi cả P7 được duyệt,
  merge thành `knowledge-base-hue/evaluation/golden_full_corpus.jsonl`.
  `knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl` là smoke đích;
  smoke gồm đúng 10 canonical rows được chọn thủ công sau merge, mỗi P7 có ít
  nhất một case và phủ được nhiều category nhất có thể. Rows phải deep-equal và
  giữ thứ tự tương đối trong canonical; User và Reviewer duyệt danh sách chọn.
  Smoke không được sửa độc lập, không là split hoặc benchmark thay full set; nếu
  canonical row tương ứng đổi/xóa thì phải tạo lại smoke từ canonical. Các file
  theo nhánh là authoring artifacts và bị rút khỏi official evaluator path sau
  merge, không trở thành bảy benchmark.
- Merge đọc bảy working files đã approved theo thứ tự P7, giữ row order trong
  từng file, kiểm `partition` khớp nhánh và strip field authoring này. Mỗi output
  row có đúng bốn fields theo thứ tự `question`, `keywords`, `reference_answer`,
  `category`; question không được trùng sau trim + so sánh không phân biệt
  hoa/thường. Sau khi nối, xáo toàn bộ rows bằng một deterministic shuffle với
  fixed seed `42`, rồi mới ghi canonical UTF-8 JSONL. Cùng exact inputs/order và
  seed phải cho byte-identical output. Không global sort, interleave, ID,
  manifest, checksum hoặc package state.
- Khi canonical đã đủ các case được duyệt (planning target 150–200, không là
  quota) và merge/shuffle được Reviewer kiểm là không đổi nội dung, phải chạy
  full file cho toàn bộ Retrieval Evaluation (MRR@10, nDCG@10, Keyword
  Coverage@10) và Answer Evaluation (Accuracy, Completeness, Relevance). Smoke
  chỉ phục vụ bounded check và không thay full evaluation này. Exact provider,
  model và matrix vẫn phải nằm trong approved implementation plan trước khi chạy.
- Qdrant benchmark dùng collection isolated theo từng dense embedding candidate;
  active Foods collections giữ read-only. Baseline E5-small, E5-base và HuyDang
  dùng ba full-corpus candidate collections theo lựa chọn cách ly benchmark đã
  được User chốt. Việc tách giúp phân định schema, lifecycle và cutover evidence;
  exact lifecycle vẫn là Decision #2. Đây là design choice của Hue, không phải
  khẳng định Qdrant về kỹ thuật không thể đặt nhiều named vectors trong một
  collection.
  Nếu chạy controlled A/B cho representation B trên cả ba model và cần giữ đồng
  thời kết quả, base matrix có thể cần thêm ba B collections, tức sáu
  full-corpus benchmark collections; Decision #2 xác nhận đây không phải hard
  cap cho các experiment variants được duyệt. User đã chốt Decision #1: mỗi
  candidate collection lưu
  cả dense và sparse vectors trên cùng point/schema vì hybrid candidate có sparse
  query consumer thật. Baseline A chỉ query dense rồi BM25 local rescoring; đây
  không phải true hybrid candidate retrieval. Hybrid candidate query dense và
  sparse độc lập rồi fusion; exact fusion/reranker chờ Decision #4. Không tạo
  collection riêng cho BM25, reranker, fusion hoặc scoring. Chỉ cutover một
  winner sau benchmark, Reviewer review và User approval.
  Decision #2 chốt fresh-by-default: mỗi experiment build vào target mới/rỗng,
  không in-place reconcile; cho phép nhiều collections khi mỗi collection gắn
  với candidate/variant được duyệt. Exact replacement là lối phụ cần verify
  target và approval riêng. Sau benchmark đề xuất giữ khoảng 1–3 collections
  tốt nhất; cleanup không tự động và luôn cần exact targets/authority. Exact
  names còn chờ spec/plan.
  Decision #3 chốt mỗi Qdrant point có point ID và hai named vectors
  `dense`/`sparse` ở trường chuẩn của Qdrant; không lặp chúng trong payload.
  Payload chỉ giữ `search_text`, `source`, `title`, `heading_path` và
  `evidence_parts[{role,start,end,text}]`. Model/representation identity thuộc
  collection/build; source fingerprint thuộc file/index; domain/subdomain suy
  từ `source`. Không thêm metadata per-point khi chưa có consumer.
  Decision #4 chốt matrix theo giai đoạn. Với mỗi dense model, so baseline A
  (dense pool + BM25 local, fusion bằng RRF trong pool) với native hybrid
  (dense/sparse retrieval độc lập, fusion bằng RRF). Chỉ retrieval finalists mới
  so một reranker với no-rerank control. Retrieval stage dùng MRR@10, nDCG@10,
  Keyword Coverage@10; end-to-end finalists báo đủ sáu metrics. Không composite,
  threshold hay winner/default trước kết quả thực nghiệm. Lỗi component làm run
  incomplete, không silent fallback; pair quá dài giữ pre-rerank order theo
  contract đã chốt.
  Decision #5 chốt representation B theo staged finalists: hoàn tất
  representation A trên mọi dense model/retrieval method, chọn finalists bằng
  metrics đã chốt, rồi tạo B và fresh indexes thật chỉ cho finalists. A/B giữ
  model, retrieval, fusion và reranker tương đương. Official evidence phải từ
  API/index/full-corpus run thật; mock chỉ phục vụ technical tests. User chấp
  nhận chi phí, nhưng exact provider/model/prompt/budget và execution authority
  vẫn chờ Decision #6, Written Spec và approved Plan.
  Decision #6a chốt strict minimal public contract: success chỉ có `answer` và
  `sources`; answer dùng response-local `[n]`, mỗi source chỉ có
  `{id,title,heading_path,excerpts}` và phải được answer tham chiếu. Technical/
  citation-integrity failure trả typed non-2xx `{error:{code,message}}`, không
  partial success, silent fallback hoặc automatic repair/retry. Thiếu evidence
  vẫn trả phần có căn cứ hoặc nêu thiếu thông tin.
  Decision #6b chốt token-budget động nhưng reproducible: mỗi approved generator
  profile khóa `context_limit`, `reserved_output_tokens` và `safety_margin` cho
  toàn benchmark run. Mỗi request trừ actual system/query/format/citation
  overhead rồi pack nguyên chunk theo final rank, tối đa 5; dừng khi chunk kế
  tiếp không vừa, không skip/truncate/summarize. Đổi model/profile mới được đổi
  budget; report phải ghi exact values. Chunk hạng đầu không vừa là typed
  configuration/input error.
  Decision #6c chốt `qwen/qwen3.5-9b` qua OpenRouter cho cả representation B và
  answer generation. Mỗi benchmark run pin một upstream provider và không
  automatic routing/silent failover; exact upstream được preflight rồi khóa
  trong approved plan/run. Evaluation judge vẫn là `gpt-5.4-mini` qua OpenAI
  API, độc lập với candidate generator. Representation B chỉ bổ sung context tìm
  kiếm do Qwen sinh vào `search_text` của chunk A đủ chỗ; phần bổ sung không là
  evidence/citation/Golden và không tạo vector type mới.
  Decision #6d chốt profile Qwen balanced/reproducible: `temperature=0`, không
  set sampling knobs khác; representation B `max_output_tokens=256`; answer
  generation có `context_limit=16384`, `reserved_output_tokens=2048`,
  `safety_margin=512`, timeout 90 giây và không automatic retry/failover. Exact
  upstream được preflight, pin và ghi trước approved run. Agentic RAG tương lai
  phải có profile/contract riêng cho tools, plan/state, steps và tổng budget;
  không dùng ngân sách one-shot này cho agentic workflow.
  Decision #6e chốt UI inline tối giản: một ô câu hỏi/nút gửi, loading và chặn
  submit trùng; answer Markdown an toàn; click/keyboard citation `[n]` cuộn và
  focus source card tương ứng ngay dưới answer. Card chỉ hiển thị title,
  heading path và các excerpts tách riêng. Typed error có manual retry; không
  streaming, history/session, debug/score/token hoặc agentic tool/plan UI.
- Không đặt tổng case count hoặc quota theo category/P7 trước khi biên soạn.
  Golden được làm và review riêng theo từng partition, rồi merge để xác định số
  thực tế; khoảng planning target là 150–200 cases. Không padding case yếu để
  đạt số và không loại case đạt chất lượng chỉ để ép một tổng cứng.
- Không chia canonical Golden thành `dev`/`test` trong scope hiện tại. Toàn bộ
  canonical file là một evaluation set; smoke chỉ là subset chạy nhanh được
  copy deep-equal từ canonical, không phải một split độc lập.
- Retrieval Evaluation dùng một cutoff thống nhất `K=10`: MRR@10, nDCG@10 và
  Keyword Coverage@10. Đây là cutoff báo cáo metric, không tự thay đổi retrieval
  depth của pipeline.
- Điểm toàn Golden dùng macro-average theo case: tính từng metric cho từng câu
  rồi lấy trung bình, mỗi câu có trọng số bằng nhau. Báo cáo thêm case count và
  cùng loại macro-average theo `category`; không tạo micro-average hoặc một
  weighted/composite score mới.
- Official aggregate chỉ được công bố khi mọi canonical case có kết quả hợp lệ.
  Retrieval thực thi thành công nhưng không trả kết quả nhận 0 cho MRR@10,
  nDCG@10 và Keyword Coverage@10. Generation thực thi thành công nhưng trả
  answer rỗng/không đánh giá được nhận 1 cho cả ba Answer metrics. Lỗi kỹ thuật,
  timeout, judge failure hoặc judge output không hợp lệ làm run `incomplete`;
  ghi đúng case/stage/error và chạy lại case lỗi trước khi tính official overall
  hay category aggregate. Không chế điểm cho lỗi hạ tầng và không loại case khỏi
  mẫu số. Kết quả dở dang nếu hiển thị phải ghi rõ là progress, không phải
  official metric.
- Full-corpus phase hiện tại không đặt pass/fail threshold hoặc diagnostic color
  bands cho sáu metric trước khi có baseline trên corpus mới. Official report
  ghi exact values, case counts và category breakdown để so sánh cấu hình; các
  ngưỡng màu của `rag_old_0` không được kế thừa thành acceptance. Run-completeness
  và data/schema quality gates vẫn bắt buộc, nhưng không phải metric thresholds.
- Runtime citation UI/source mapping là scope riêng. Loại Golden evidence không
  tự xóa runtime citation, nhưng citation/groundedness chưa được chấm tự động
  trong phase evaluation hiện hành.
- Taxonomy sản phẩm vẫn có năm domain; P7 chỉ là cách chia việc authoring/review.

## Nội dung chưa chốt

Golden schema, authoring P7, review, merge/shuffle, smoke và full-evaluation
contracts đã chốt ở mức design notes. Verified Architecture Extraction từ
`llm_rag` đã được approved làm evidence companion sau closure ngày 2026-09-11.

Decision Queue hiện hoạt động tại mục #6. Mỗi lượt chỉ hỏi một quyết định có ảnh
hưởng contract, cập nhật câu trả lời vào guide/decision notes trước mục kế tiếp:

1. **Đã chốt 2026-09-11 — lexical baseline/sparse consumer:** baseline A dùng
   dense candidates + BM25 local; hybrid là controlled candidate có sparse query
   consumer thật. Cùng candidate collection lưu cả dense và sparse vectors.
2. **Đã chốt 2026-09-11 — index lifecycle:** fresh-by-default vào target
   mới/rỗng; cho phép nhiều experiment collections, không reconcile in place.
   Exact replacement và cleanup cần target/approval riêng; sau benchmark đề xuất
   giữ khoảng 1–3 collections tốt nhất.
3. **Đã chốt 2026-09-11 — payload/source locator:** point ID và dense/sparse
   vectors dùng trường Qdrant chuẩn; payload chỉ có `search_text`, `source`,
   `title`, `heading_path`, `evidence_parts`. Không lặp model/hash/domain metadata
   ở từng point.
4. **Đã chốt 2026-09-11 — retrieval/fusion/reranker matrix:** staged comparison
   baseline A với native hybrid bằng RRF; chỉ retrieval finalists so một
   reranker với no-rerank. Báo exact metrics/results, không full Cartesian matrix
   hoặc chọn winner trước evidence.
5. **Đã chốt 2026-09-11 — representation B timing:** staged finalists sau
   representation A; dùng API/index/full-corpus run thật, không dùng mock làm
   official evidence. User chấp nhận chi phí thực nghiệm.
6. **Đang chốt — context/generator/API/citation/frontend:** #6a strict minimal
   response/citation/error, #6b dynamic-per-profile/fixed-per-run context budget
   và #6c Qwen/OpenRouter pinned-provider + OpenAI judge separation đã chốt;
   #6d chốt exact profile 16384/2048/512, B output 256, temperature 0, timeout
   90 giây và agentic profile riêng; #6e chốt UI inline citation/source cards.
   Decision #6 đã đủ đầu vào cho Written Spec.
7. metric thresholds/cutover chỉ sau khi có full-corpus baseline thật.

Decision #6 được chốt theo từng subdecision có một consumer rõ. #6a public
response/citation/error, #6b context budget, #6c generator/provider + judge
separation, #6d exact generator settings/numeric budgets và #6e UI interaction
đã chốt. Không gom thêm agentic workflow vào MVP; bước kế tiếp là Written Spec.

Các quyết định chunking, embedding, ingestion/indexing, retrieval/reranking,
context/generation, API/frontend và evaluation sẽ được gom thành một written
spec toàn corpus. Những ghi chú hiện có trong `docs/superpowers/` là đầu vào cho
spec đó, chưa phải spec hoặc plan được duyệt.

Các quyết định đã chốt không hỏi lại: A theo cấu trúc Markdown; B giữ nguyên A
và chỉ bổ sung chọn lọc; Top-5 primary chunks; reranker là capability MVP nhưng
winner/default cần benchmark; one-shot non-streaming; isolated collections với
fresh-by-default và không hard cap experiment; Foods read-only; Golden
metric-only/P7/smoke 10/seed 42/K=10/macro-average và không đặt threshold trước
baseline.

## Chuỗi tài liệu và điểm duyệt

1. Các khảo sát trước survey toàn project `llm_rag` đã hoàn tất independent
   Reviewer review và User confirmation; không mở lại nếu không có evidence
   mới. Survey dài `llm_rag` đã bị đóng băng non-canonical; Verified
   Architecture Extraction thay thế đã qua review và User closure, trở thành
   approved evidence companion.
2. Decision Queue tiền-spec đã hoàn tất qua #6e.
3. Written Spec toàn corpus tại
   `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` đã được
   User duyệt ngày 2026-09-11.
4. Implementation Plan và Review Contract đã được User duyệt ngày 2026-09-11.
5. Wave 1 đã User-closed ngày 2026-09-12; final review là
   `reports/full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`.
6. **Hiện hành:** `CURRENT_HANDOFF.md` giao Reviewer bắt đầu design gate Phase
   3/Wave 2.1. Reviewer brainstorming từng quyết định còn mở, cập nhật detailed
   Phase 3 guide và soạn exact addendum/plan/Review Contract để User duyệt; chưa
   giao Implementer và mọi live gate vẫn đóng.

Không pre-create hoặc cố định tên ngày cho spec/plan trước gate. Reviewer chọn
exact path khi bắt đầu artifact sau khi decision queue đủ; path không tự tạo
approval.

## Tài liệu hiện hành

- Trạng thái task: `session_prompt/CURRENT_HANDOFF.md`.
- Wave 1 final review/closure:
  `reports/full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md` và
  `reports/user_reports/full_corpus_rag_wave_1_user_report_2026_09_12.md`.
- Correction 1–3 prompts/reviews là lifecycle history, không còn active contract.
- Context và lịch sử quyết định:
  `handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md`.
- Bản ghi quyết định đang tích lũy:
  `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`.
- Ghi chú phụ thuộc/thử nghiệm cho plan sau này:
  `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`.
- Review schema đã completed:
  `reports/full_corpus_golden_schema_reference_deep_dive_codex_review_2026_09_10.md`.
- Tham chiếu `rag_old_0` đã được khảo sát và review đầy đủ trong hai report
  `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md` và
  `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_codex_review_2026_09_10.md`.
  Các phiên sau dùng hai report này; không đọc/phân tích lại source, notebook
  hoặc transcript `rag_old_0` nếu không có finding mới hay yêu cầu mới của User.
- Survey toàn project `llm_rag` đã chạm correction ceiling; review/complexity
  reset source of truth là
  `reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md`
  (§9–10). User đã xác nhận contract thay thế tại
  `handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md`. Không dùng
  report 885 dòng làm canonical basis.

Hai file ngày 2026-09-09 ở `docs/superpowers/` là working notes. Tên thư mục
không biến chúng thành approved written spec hoặc implementation plan.
