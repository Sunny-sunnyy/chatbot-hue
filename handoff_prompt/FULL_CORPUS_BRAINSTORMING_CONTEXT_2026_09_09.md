# Ngữ cảnh chuyển tiếp: thiết kế RAG cho toàn bộ corpus Huế

## Snapshot hiện hành — đọc trước lịch sử

Canonical docs full-corpus nay nằm trong `handoff_prompt/`. Bốn bootstrap
files và CURRENT_HANDOFF vẫn ở `session_prompt/`; các file FULL_CORPUS cũ tại
đó chỉ dẫn sang vị trí mới để prompt/report đã gửi còn dùng được.

**Đã hoàn tất:** curation/migration tourism → travel; khảo sát parser; đo hai
input VN/QT; khảo sát Golden/evaluation reference; khảo sát sâu Golden schema;
và simplicity survey `rag_old_0`. Các phần này đã qua các correction cần thiết,
independent Reviewer review và User xác nhận `approved/completed`. Không mở lại
findings hoặc khảo sát đã đóng khi không có evidence mới.

**Nhiệm vụ hiện hành:** survey toàn project `/home/minhhieu/llm_rag` dài 885
dòng vẫn đóng băng working/non-canonical sau complexity reset. Verified
Architecture Extraction thay thế đã qua hai correction, independent Reviewer
review và User closure ngày 2026-09-11; artifact là approved evidence companion.
Decision #1 đã chốt baseline A + hybrid candidate có sparse consumer thật;
Decision #2 chốt fresh-by-default và cho phép nhiều experiment collections.
Decision #3 chốt payload 5 fields, point ID và dense/sparse vectors dùng trường
Qdrant chuẩn. Decision #4 chốt staged retrieval/fusion/reranker matrix và báo
exact metrics/results. Decision #5 chốt B theo staged finalists với API/index/
full-corpus runs thật.
#6a strict minimal response/citation/error, #6b context budget, #6c
generator/provider + judge separation và #6d exact generator settings/budgets
cùng #6e UI inline citation/source cards đã chốt. Decision Queue tiền-spec hoàn
tất; Written Spec, Plan và Review Contract đã được User duyệt ngày 2026-09-11.
`CURRENT_HANDOFF.md` giao Implementer duy nhất Wave 1; các wave và live gate sau
chưa active.

Guide umbrella của workstream là `guides/full_corpus_rag.md`. Hai tài liệu ngày
2026-09-09 trong `docs/superpowers/specs` và `docs/superpowers/plans` là working
notes; artifact Spec/Plan được duyệt là hai file ngày 2026-09-11.

**Quyết định đã chốt:**
- MVP cá nhân tiếng Việt, toàn curated answer-facing corpus năm domain;
  frontend/citation/evaluation bắt buộc, một lượt, không web fallback/memory.
- Trả phần có evidence, giữ thời hạn/điều kiện, không bịa giá/ngày/giờ/di
  chuyển. Mâu thuẫn cùng phạm vi thì trình các thông tin kèm nguồn, không
  chọn bên đúng; khác nhà cung cấp/thời điểm không tự là mâu thuẫn.
- A chia theo cấu trúc Markdown, không LLM; chung chunks E5-small/base/HuyDang,
  full input kiểm từng tokenizer. Giữ list cha/con, bảng/header/điều kiện/
  intro; không fixed overlap/400 chars/H2-only/count 572 cho full corpus.
- Nhóm tối thiểu vẫn vượt limit mà chưa xử lý đủ nghĩa: preview báo rõ,
  chặn ingest trước embedding/ghi index; không ingest thiếu hoặc truncate.
- Baseline tối đa 5 chunk chính theo budget, chưa expansion sau Top-5.
  B offline chọn lọc giữ nguyên A; text sinh riêng không là evidence, chỉ
  thêm nếu vừa cả ba models; không vector phụ hoặc đổi boundaries.
- Reranker thuộc MVP, giữ no-rerank so sánh; chưa winner/default full corpus.
  Pair quá dài thì bỏ rerank cả request, giữ ranking trước đó và ghi
  evaluation; không cắt query/evidence hoặc che lỗi provider.
- Trả đáp án hoàn chỉnh cùng nguồn một lần, không streaming. UI không lộ
  machine path/chunk ID/scores/token/debug. Citation dùng đúng bản ingest.
- Ingest khi server tắt; source thêm/sửa/xóa thì startup yêu cầu ingest lại.
  Chỉ đổi CRLF/CR/LF coi là cùng text LF; kỹ thuật xuống dòng do Reviewer chọn.
- Roadmap GPU/Qwen0.6B/multi-turn/agentic không chặn MVP; latency chưa hard gate.

**Evidence mới nhất:** VN 931 ký tự, E5-small/base 290/290, HuyDang 224,
MiniLM orig/long 411/453; QT 866 ký tự, 268/268, 208, 385/427. Đều vừa
limits mẫu. Counts input sai không dùng; không suy quality/mọi query. Review
VN/QT mục 6 và context mục 33–34 giữ closure và giới hạn; không rerun.

**Golden/evaluation đã chốt:** một canonical JSONL có bốn required fields
`question`, `keywords`, `reference_answer`, `category`; không có `case_id`,
`expected_claims`, `evidence_groups`, source spans, chunk IDs, `case_type`,
`domain` hoặc `claim_id`. `partition` chỉ dùng authoring P7 rồi strip khi merge;
evaluator chỉ derive `case_index` từ canonical row order khi cần.
Bảy category generic dùng để count/breakdown, không routing/scoring. Không hard
quota; làm từng partition rồi merge, planning target khoảng 150–200. Không
dev/test; smoke deep-equal. Retrieval dùng MRR@10, nDCG@10, Keyword Coverage@10;
keywords là các term/phrase quan trọng, chính xác, có dạng chữ nguyên văn trong
corpus liên quan và được reference answer hỗ trợ; không synonym/generic padding.
Answer dùng Accuracy, Completeness, Relevance; tổng hợp macro-average theo case.
Ba Answer metrics dùng thang số nguyên 1–5 với rubric đủ năm mức cho từng
metric và một judge prompt tối thiểu mỗi case. Official aggregate cần đủ mọi
case; technical failure làm run incomplete, không bị loại hoặc gán điểm giả.
Không metric threshold trước full-corpus baseline và không micro/composite
score.
Evidence C trước đây đã bị supersede vì không có consumer trong sáu metric hiện
hành.

**Còn mở:** Decision Queue bắt đầu tại #1 Qdrant sparse consumer/lexical
baseline, sau đó lần lượt full rebuild/replacement lifecycle, payload/source
locator, retrieval/scoring matrix, timing của representation B,
API/query/generator budgets, citation/error behavior, provider/model settings
và frontend chi tiết. Alias/manifest/checksum/migration framework không tự được
thêm khi chưa có consumer hoặc failure thật. Không coi mọi đề xuất lịch sử là
requirement.

**Tham khảo `rag_old_0`:** dùng implementation survey và Codex review ngày
2026-09-10 trong `reports/`. Không đọc/phân tích lại raw source, notebook hoặc
transcript `rag_old_0` nếu User không yêu cầu hay không có câu hỏi mới mà hai
report chưa trả lời.

Reviewer phân tích/thiết kế/docs; code/đo/test/đọc thông số/tóm tắt rộng giao
Implementer qua user, không tạo việc thừa. Guide → written spec → User duyệt →
plan/Review Contract → User duyệt → Implementer. Không runtime/corpus/index/
dependencies/.env/API/Git mutation/subagent. Worktree có thay đổi sẵn.

## Lịch sử và evidence — không dùng các trạng thái cũ làm next action

Mục 1–76 giữ diễn tiến và bằng chứng; các câu “chưa đo”, “chưa chọn”, “chờ
tài liệu” chỉ đúng tại mốc được ghi. Snapshot phía trên, CURRENT_HANDOFF và
§§77–80 giữ trạng thái chuyển phiên. Giữ lịch sử counts sai/correction
để tránh dùng nhầm evidence, không xóa dấu vết rồi gọi số đo cũ là hợp lệ.

Mốc lịch sử mở bản ghi: 2026-09-09, Asia/Bangkok, sau user xác nhận khảo sát
parser; diễn tiến tiếp theo nằm ở các mục lịch sử, còn trạng thái hiện hành nằm
trong snapshot và §§91–95.
Workspace: `/home/minhhieu/hue_rag`. Target role: implementer.
Mục 33–34 ghi khảo sát hai input và lựa chọn trả đáp án một lần; mục 35–76 là
lịch sử Golden/reference, survey và corrections; §§77–80 ghi trạng thái mới nhất.
User đã approved khảo sát VN/QT.
Khảo sát parser/source locator: **approved**, sau review ba lượt correction.
Thiết kế full-corpus: Spec/Plan/Review Contract approved; Wave 1 active.
HEAD: `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`. Git/sub-agent authorization: none.

Mục 25–29 giữ trạng thái tại mốc parser closure và kết quả review khi đó,
không giữ next action hiện hành. Mục 26 giữ evidence tokenizer lịch sử với
đính chính VN/QT ngay tại bảng. Mục 1–24 giữ bối cảnh/lịch sử; các câu “chờ”,
“chưa có report” trong mô tả phiên cũ không còn là next action. Không chạy lại
migration, khảo sát hoặc correction đã đóng. Bản ghi không thay approved spec.


## 1. Mục tiêu và yêu cầu đã chốt với user

Backend và guides ban đầu được thiết kế cho Foods MVP. User đã hoàn thành
curation toàn bộ dữ liệu, muốn Reviewer nghiên cứu corpus, backend và guides,
cùng thảo luận để thiết kế lại chunking, embedding, ingestion, retrieval,
reranking, context và evaluation khi cần. Không chỉ mở rộng glob ingest.

### Phạm vi sản phẩm

- Hiện tại: MVP cơ bản, chatbot hỏi đáp và tổng hợp từ toàn bộ corpus đã có.
  User yêu cầu các chức năng nền tảng embedding, ingestion, generator,
  reranking, retrieval, scoring và evaluation để xem kết quả đánh giá hiện tại.
  Có module/thử nghiệm reranking không đồng nghĩa phải bật reranker mặc định
  khi chưa chứng minh hiệu quả. Không mở rộng MVP thành hệ thống agent phức tạp.
- Ngôn ngữ câu hỏi và câu trả lời: tiếng Việt.
- Cá nhân hóa, hội thoại nhiều lượt và Agentic RAG: đưa vào specs/plans dưới
  dạng roadmap triển khai sau; không triển khai ngay, không là gate nghiệm thu
  của giai đoạn hiện tại.
- User đã xác nhận gợi ý/lịch trình một lượt dựa trên corpus và điều kiện nêu
  ngay trong câu hỏi. Không lưu sở thích, không nhớ lượt trước, không xây hồ sơ
  người dùng hoặc bộ tối ưu lịch trình chuyên biệt ở MVP.
- Các khả năng nâng cao chỉ triển khai sau khi MVP đủ ổn định. Tiêu chí
  “đủ ổn định” đã chốt ở mức nguyên tắc tại mục 12; ngưỡng chất lượng cụ thể
  chưa chốt. Khảo sát parser đã approved; bước tiếp tục là hoàn thiện written
  spec theo mục 29–31; hành vi nguồn thay đổi đã chốt tại mục 17.
- Không có yêu cầu chatbot hiện tại duyệt web hoặc dùng công cụ ngoài corpus.
  Việc Reviewer tra tài liệu kỹ thuật trên web không đồng nghĩa mở scope đó.

### Chính sách trả lời: user đã xác nhận phương án 2

- Trả lời phần có bằng chứng; chỉ rõ phần thiếu hoặc chưa xác minh tính hiện hành.
- Nếu không biết hoặc corpus không có thông tin trả lời, nói rõ không có thông
  tin, ví dụ “Kho dữ liệu hiện có chưa có thông tin này”. Không bắt buộc một
  chuỗi literal duy nhất; chưa chốt chi tiết response schema.
- Không dùng kiến thức sẵn có của LLM để tự lấp chỗ thiếu bằng chứng. Có thể
  diễn đạt/tổng hợp từ nguồn nhưng không biến suy đoán thành sự kiện.
- Ngày tổ chức, giờ mở cửa, giá vé và thời gian di chuyển không được tự khẳng
  định nếu thiếu bằng chứng. Thông tin có năm/thời hạn phải giữ phạm vi đó,
  không tự gọi là “mới nhất” hay “hiện tại”.
- Cách hiểu nhất quán của Reviewer với xác nhận trước: không bịa/khẳng định
  thiếu bằng chứng là yêu cầu ngay ở MVP, không phải tính năng hoãn tới sau MVP.
  Lời user cuối nhắc gộp cả các ví dụ này với roadmap; không dùng lời đó để
  ngầm hủy chính sách bằng chứng đã được user xác nhận rõ ràng.

### Dẫn nguồn và ranh giới hiển thị: user đã xác nhận

- Người dùng có thể bấm nguồn để xem đoạn bằng chứng gốc liên quan.
- Trình bày nguồn bằng tên tài liệu, tên mục và nội dung dễ đọc; hướng đã
  thảo luận là ký hiệu [1], [2] gắn với thông tin tương ứng và danh sách nguồn.
  Chưa chốt thiết kế UI hoặc endpoint cụ thể; không tự mở workstream frontend.
- Không hiển thị đường dẫn máy, chunk ID kỹ thuật hoặc độ đo kỹ thuật cho
  người dùng chatbot. Không dùng tên file kỹ thuật làm nhãn nguồn khó hiểu.
- Diễn giải thiết kế của Reviewer: collection names, similarity/reranking
  scores, token counts, latency, benchmark metrics, logs và stack traces cũng
  không đưa vào câu trả lời/giao diện chatbot. Nguồn công khai cần format riêng,
  không trả nguyên internal metadata để frontend chỉ che bằng CSS.
- Internal identifiers/scoring vẫn cần cho pipeline, truy vết và evaluation;
  không hiểu yêu cầu ẩn kỹ thuật là xóa các chức năng này khỏi backend.
- Evaluation/report dành cho chủ dự án/developer vẫn phải có kết quả kỹ thuật
  để đánh giá MVP. Tách chúng khỏi trải nghiệm người dùng chatbot; chưa yêu cầu
  xây admin dashboard hoặc hệ thống phân quyền mới.

### Roadmap Agentic RAG: user đã cấp định hướng rõ

- Sau MVP ổn định, cho phép LLM dùng tools/API tìm kiếm như Serper khi corpus
  không chứa đủ thông tin trả lời, để tra cứu thông tin mới.
- Đây là yêu cầu ghi vào specs/plans tương lai, không là quyền gọi Serper hoặc
  triển khai web fallback ngay trong MVP.
- Chi tiết còn cần thiết kế ở giai đoạn đó: trigger thiếu bằng chứng/thông tin
  hết hiệu lực, lựa chọn và kiểm chứng nguồn, xử lý mâu thuẫn, dẫn nguồn web,
  thời điểm truy cập, ngân sách, lỗi tool và untrusted web content.
- Serper là ví dụ API được user nêu; chưa có provider integration, key hoặc
  budget nào được kiểm tra trong session này.

### Model và hạ tầng: user xác nhận

- Embedding/reranking phải có phương án nhẹ, chạy local như hiện tại.
- Embedding candidates ban đầu: E5-small, E5-base, HuyDang.
- Reranker: MiniLM `cross-encoder/ms-marco-MiniLM-L-6-v2` hoặc model nhẹ phù hợp
  tiếng Việt; vẫn cần benchmark, không tự coi MiniLM là winner.
- Nghiên cứu sau: `Qwen/Qwen3-Embedding-0.6B` và
  `Qwen/Qwen3-Reranker-0.6B`, đánh giá khả năng local và GPU.
- Máy Windows, CPU Intel Core i5-11400H, RAM tổng 32 GB DDR4,
  GPU NVIDIA GTX 1650 4 GB VRAM.
- Project chạy trong WSL2 Ubuntu; user chưa kích hoạt được GPU trong WSL.
- User hiểu WSL thường có khoảng 16 GB từ máy 32 GB, nhưng đã quan sát có lúc
  WSL dùng hơn 16 GB. Đây là mô tả của user, KHÔNG phải cấu hình đã kiểm chứng.
  Chưa đọc `.wslconfig`, chưa đo RAM/swap/cgroup hay xác minh phiên bản WSL.
  Không khẳng định 16 GB là hard limit, cũng không giả định WSL dùng đủ 32 GB.
- User cho phép đưa nghiên cứu/kích hoạt GPU WSL và thử hai Qwen3 0.6B vào
  specs/plans. Chưa yêu cầu cài driver hoặc thay đổi môi trường ngay.
- Không đưa Qwen3.5 9B chạy local vào phạm vi; user muốn model này qua API.

### API: thông tin mới nhất từ user

- GPT-5.4 nano và GPT-5.4 mini gọi qua OpenAI API.
- Qwen3.5 9B gọi qua OpenRouter.
- User nói cả hai provider đã có key trong `.env`.
- KHÔNG đọc/in `.env`; chưa kiểm tra tên biến, key, endpoint hoặc kết nối.
- Tên `OPENAI_API` trong lời user là mô tả tuyến API, không phải bằng chứng
  về tên environment variable. Exact model ID OpenRouter cũng chưa chốt.
- Được phép dùng các API trên khi thử nghiệm; chưa gọi API trong session này.
  Trần chi phí, số lượt gọi, phân vai generation/judge và test matrix còn mở.
  Không hiểu đây là quyền chi tiêu không giới hạn.

## 2. Workflow và quyền tại mốc khởi đầu — trạng thái mới ở mục 29

Bootstrap đã đọc trong session trước:

- `session_prompt/REVIEWER_WORKFLOW.md`
- `session_prompt/Session_Prompt.md`
- `session_prompt/Project_Status.md`
- `session_prompt/CURRENT_HANDOFF.md`
- `session_prompt/brainstorming.md`

Đã dùng workflow `using-superpowers`, `brainstorming`,
`skills/risk-gated-agent-review/SKILL.md`; đã đọc thêm
`skills/practical-project-coding/SKILL.md` để hiểu thiết kế implementation.
Session mới đọc và áp dụng lại các instruction liên quan, không coi bản ghi
này là bản thay thế skill. Không sao chép doctrine vào spec.

User đang trực tiếp giao nhiệm vụ brainstorming mới. `CURRENT_HANDOFF.md` là
closure cũ, target implementer, state completed, cho curation Tickets/taxonomy.
Nó có next action cũ yêu cầu migration dù phần trên ghi migration đã xong.
Không thực hiện migration lần nữa; không để target role cũ chặn brainstorming.
Giữ approval lịch sử và không coi curation approved là runtime multidomain approved.

Chưa được phép implement runtime, ingest/rebuild/reset index, benchmark tốn phí
không giới hạn, sửa dữ liệu nguồn, commit/push hoặc spawn subagent.
User trực tiếp yêu cầu tạo rồi cập nhật bản ghi và prompt chuyển tiếp này; đây là exact
docs-only task, không phải tự ý viết approved spec trước design gate.

Luồng tiếp theo vẫn là thảo luận -> duyệt design -> viết/self-review spec ->
user duyệt written spec -> viết plan/Review Contract -> user duyệt plan ->
handoff implementer. Không hỏi lại các quyết định đã chốt ở mục 1.

## 3. Corpus thực tế đã khảo sát

204 Markdown answer-facing theo bộ lọc khảo sát:

| Nhánh | Entity / tài liệu | Guide | Tổng |
|---|---:|---:|---:|
| foods | 57 restaurants + 24 cafes + 9 local_specialties | 1 | 91 |
| festivals | 26 | 1 | 27 |
| heritages | 28 | 1 | 29 |
| performing_arts | 11 | 1 | 12 |
| travel/places | 35 | 1 | 36 |
| travel/services | 4 cẩm nang | — | 4 |
| travel/tickets | 5 cẩm nang | — | 5 |
| Tổng | | | 204 |

Canonical taxonomy hiện tại là `travel/`, không phải `tourism/`.
`travel_guides.md` nằm dưới `travel/places/`.
Loại khỏi answer corpus: `_source-dumps/`, `meta/`, Foods `evaluation/`,
các inventory/research management files trong domain folders.
Không ingest toàn bộ `**/*.md` thiếu bộ lọc.

Đã quét cấu trúc tất cả 204 file bằng code đọc text thuần: đều có một H1 và ít
nhất một H2. Dữ liệu mới dài và phân cấp H3/H4 sâu hơn Foods, có bảng, danh sách
lồng, điều kiện áp dụng, mô tả lịch sử và thông tin có hiệu lực theo thời gian.

### Chỉ báo độ dài (khảo sát cấu trúc, không phải output chunker canonical)

| Nhánh | Số section khảo sát | Median ký tự | Section > 1.500 ký tự |
|---|---:|---:|---:|
| foods | 367 | 350 | 1 |
| festivals | 263 | 740 | 26 |
| heritages | 268 | 1.318,5 | 106 |
| performing_arts | 125 | 1.458 | 60 |
| travel/places | 366 | 2.014 | 281 |
| travel/services | 35 | 664 | 1 |
| travel/tickets | 40 | 2.628 | 36 |

Phép đếm này loại section H2 `Nguồn dữ liệu`, nhưng tính intro/nonempty blocks;
không dùng làm acceptance số lượng chunk. Ví dụ H2 kiến trúc trong `Đại Nội
Huế.md` dài khoảng 11.251 ký tự. Có hai bảng vé hơn 3.000 ký tự.

### Diagnostic splitter đã chạy

Chỉ thực thi hàm split text hiện có bằng stdlib trong bộ nhớ, với phần chuẩn bị
text độc lập (H2/intro, bỏ image-only và section nguồn), không chạy ingestion
pipeline, embedding hoặc Qdrant. Kết quả mảnh text:

- Foods 572; festivals 815; heritages 1.581; performing_arts 734;
  travel/places 2.830; services 79; tickets 347; tổng 6.958.
- Có mảnh chỉ còn separator `---`; nhiều mảnh kết thúc ngay tại H3, khiến phần
  nội dung tiếp theo mất tiêu đề; hai mảnh bảng vượt 3.000 ký tự trước khi thêm nhãn.
- Đây là bằng chứng structural risk, KHÔNG là expected production chunk count
  hoặc kết quả chất lượng retrieval. Không lưu script/artifact của phép mô phỏng.

### Đặc điểm ngữ nghĩa cần thiết kế

- Đừng gộp di sản, thực hành nghệ thuật, chương trình biểu diễn và địa điểm thành
  một entity chỉ vì cùng tên/từ khóa: Nhã nhạc, Ca Huế, vé biểu diễn là ví dụ.
- Phân biệt hệ thống và thành phần: Tam Giang–Cầu Hai / Phá Tam Giang / Đầm Cầu
  Hai / Đầm Chuồn; đèo Hải Vân khác Hải Vân Quan và chính sách vé của di tích.
- Lễ hội định kỳ khác lần tổ chức cụ thể; lịch âm/lịch sử khác ngày tổ chức
  năm hiện tại; dự kiến, đã diễn ra, hủy tổ chức không được trộn lẫn.
- Vé: giữ giá đi cùng đối tượng, điều kiện miễn/giảm, thời hạn và phạm vi áp dụng.
- Lịch trình: giữ điều kiện thời tiết, di chuyển, các phương án thay thế; không
  biến module thay thế thành những điểm cộng thêm vào cùng một lịch trình.
- New-domain provenance được quản lý trong research/evidence ngoài answer body;
  thiếu H2 `Nguồn dữ liệu` như Foods không tự động là lỗi dữ liệu.
- Các template/inventory lịch sử có thuật ngữ `tourism` hoặc thiết kế services
  cũ; đọc đối chiếu canonical files, không áp nguyên template cũ vào ingestion.
- Chưa fact-check toàn bộ nội dung hoặc luật/giá vé hiện hành. Curation approved
  không có nghĩa mọi thông tin vẫn còn hiệu lực ở thời điểm người dùng hỏi.

## 4. Backend: hiện trạng và các coupling quan sát được

Đã đọc luồng runtime ingestion, embedding, vectorstore, startup, retrieval,
reranking, context, generation và API. Đã quét AST 62 Python files để định vị
module/tests/evaluation. Chưa đọc thủ công từng dòng của tất cả test và harness lớn.

| Thành phần / nguồn | Quan sát |
|---|---|
| `backend/config/settings.yaml` | Foods globs; E5-small 384D CPU; collection `hue_foods_e5_small_384`; profile `dense_only`; top_k 10, candidate multiplier 3, max context 5 docs/3.000 chars |
| `backend/ingestion/chunking/markdown_chunker.py` | H1 title/H2 split; H3+ là body; chunk khoảng 400 ký tự; category hardcode foods; nhãn contextualization mang nghĩa quán ăn |
| `backend/ingestion/helpers/split_text.py` | Giữ bảng atomic; chưa bảo toàn hierarchy/nested-list semantics; không overlap; có thể để separator thành chunk |
| Chunk metadata | 7 fields: chunk_id, source, title, section, category, subcategory, chunk_type; chưa có heading path/evidence span/temporal contract |
| Chunk identity | `source|heading|file_running_index`; thay số chunks section trước có thể dịch ID các section sau |
| `backend/ingestion/pipeline.py` | Count gate 572 trước embedding; default chunker tự load settings trên đĩa, chưa hoàn toàn theo settings được truyền vào pipeline |
| `backend/embedding/embedder.py` | Concrete E5 wrapper, query/passage prefix, normalized encode; chưa có runtime model selection adapter cho mọi candidate |
| `backend/vectorstore/points.py` | UUID5 từ chunk_id; fixed payload allowlist, thêm metadata phải đi xuyên các layer |
| `backend/vectorstore/upsert.py` | Kiểm existing points chỉ scroll một page limit 1.000; chưa đủ full corpus |
| `backend/core/startup.py` | Count gate 572; warm-up Foods; hybrid BM25 lấy toàn corpus có pagination và kiểm model; dense-only chưa kiểm payload model identity tương đương |
| `backend/retrieval/hybrid_retriever.py` | Production BM25 rescore chỉ dense Top-30, không lexical search độc lập rồi union; khác true hybrid trong benchmark 08b |
| `backend/retrieval/context_builder.py` | Budget ký tự, gặp doc quá lớn thì break; nếu doc đầu quá lớn có thể context rỗng dù còn doc hữu ích; mất source path/chunk ID trong context format |
| `backend/llm/prompt.py` | Persona trợ lý ẩm thực; fallback nghiêm ngặt khi thiếu evidence, chưa có partial-answer policy |
| `backend/llm/generator_openai.py` | Agent tool-less, structured answer-only, OpenAI provider; không tự suy diễn đã hỗ trợ OpenRouter |
| API chat | Stateless, query tối đa 500 ký tự, answer-only response; chưa citation contract/memory/streaming |

Đây là findings phục vụ thiết kế lại, không phải verdict fail cho MVP đã approved.
Không chọn trước parent-child retrieval, graph, semantic chunking hoặc framework
mới nếu chưa chứng minh giá trị so với thiết kế đơn giản.

## 5. Evaluation và guides

- Baseline lịch sử: 91 Foods files, 572 chunks, Golden V3 45 full + 10 smoke.
- `backend/evaluation/golden_dataset.py`: schema/path/source-family và category
  gắn Foods; relevance theo cặp source + H2 section, không supporting span.
- H2 dài chứa nhiều ý: trúng section có thể bị chấm đúng dù chunk không có
  bằng chứng trả lời. Thiết kế Golden mới phải giải quyết vấn đề này.
- Golden hiện hành yêu cầu evidence nonempty; chưa có contract chuẩn cho câu
  không có đáp án trong corpus, thiếu một phần evidence hoặc mâu thuẫn.
- Phase 7 metric keyword khác binary source-section metric của Phase 8.
- Judge hiện nhận question/reference/generated answer, không nhận retrieved
  context; chưa đo groundedness trực tiếp trên evidence đã cấp cho generator.
- Chưa có Combined Golden cho corpus đầy đủ. Chưa chốt số câu, quotas,
  held-out split, threshold hay cách gán evidence.
- Đã đọc rộng guides 0–9 và reference. Phần lớn đọc đầy đủ; một số output dài
  bị truncate trong khảo sát, cần đọc lại exact đoạn nếu quyết định phụ thuộc.
- Guides có historical/as-built contracts Foods. Giữ dấu vết approved trước,
  không âm thầm viết lại lịch sử thành kiến trúc mới.
- Phase 8 tổng thể vẫn `not_ready`; 08a/08b/08c approved cho phạm vi của chúng.
  Quyết định post-08c là mở đầy đủ corpus, không chỉ pilot festivals.
- Phase 9 agentic là roadmap, không là scope implementation hiện tại.

## 6. Phase 8: báo cáo và artifacts đã đối chiếu

Đọc đầy đủ:

- `reports/user_reports/phase_8_08a_embedding_benchmark_user_report.md`
- `reports/user_reports/phase_8_08b_retrieval_fusion_benchmark_user_report.md`
- `reports/user_reports/phase_8_08c_reranker_benchmark_user_report.md`

Parse tất cả rows/records bằng stdlib; đọc summary, manifest và mẫu per-case,
không nói đã audit thủ công từng ranking hoặc rerun reconciliation/model:

- `evaluation/results/phase8_embedding_results.csv`: 50 rows, gồm historical
  MiniLM embedding và Qwen embedding; executable catalog cuối 08a chỉ 3 model.
- `phase8_sparse_calibration.csv`: 70 rows.
- `phase8_sparse_results.csv`: 200 rows, 20 settings.
- `phase8_sparse_cases.jsonl`: 900 records.
- `phase8_sparse_manifest.json`: corpus/golden/chunker fingerprints, revisions,
  config, batch history và historical active collection snapshots.
- `phase8_reranker_results.csv`: 60 rows.
- `phase8_reranker_cases.jsonl`: 135 records.

### Dense 08a (Foods, không phải corpus mới)

| Model | Recall@5 | MRR@5 | nDCG@5 | Warm total p95 ms |
|---|---:|---:|---:|---:|
| E5-small | 0,8185 | 0,7748 | 0,7425 | 46,54 |
| HuyDang | 0,8370 | 0,7211 | 0,7164 | 80,27 |
| E5-base | 0,8407 | 0,6985 | 0,7061 | 210,99 |
| Qwen3-Embedding-0.6B 384D, historical | 0,7481 | 0,6237 | 0,6175 | 1.125,91 |

Qwen row là CPU FP32 historical, không kết luận cho GPU hoặc chunking mới.
Latency khác lần chạy/harness không dùng so sánh ngang tùy tiện.
`finalist_eligible=True` trong 08a code chỉ là completed + 3 repetitions
(`embedding_benchmark.py`), không đồng nghĩa pass quality guards hay approved
production. Không dùng riêng cột này chọn model.

### Sparse/fusion 08b

- HuyDang + BM25 weighted: Recall@5 0,9111; nDCG@5 0,7655; không eligible.
- Một số hybrid candidate unions đạt recall 1,0 nhưng giảm sau Top-10/Top-5.
  Đây là động lực đo riêng evidence discovery, ordering và context selection.
- Không có BM25 hoặc TF-IDF finalist. Báo cáo nhấn mạnh relationship regression;
  CSV còn các failure theo setting ở comparative/direct_fact/food_knowledge/
  guide_planning/spanning. Không nói mọi setting đều fail cùng một category.
- Unicode tokenizer được giữ; Underthesea không cải thiện trong calibration cũ.
  BM25 selected k1=1,5; b=0,75. Đây chưa phải tham số chốt cho corpus mới.
- Benchmark có dense/sparse độc lập, union/fusion; production hybrid vẫn chỉ
  rescore dense candidates. Không đánh đồng hai đường chạy.

### Reranker 08c

- MiniLM trên E5-small: ΔnDCG@5 -0,070267.
- MiniLM trên HuyDang dense: +0,006488 nhưng vẫn fail guards.
- MiniLM trên HuyDang/BM25 weighted diagnostic: -0,060505; production safety false.
- Cả ba pairing eligible=false, clear_gain=false. Giữ no-rerank baseline.
- Không suy ra mọi reranker kém cho tiếng Việt từ một model/bộ Foods này.

Kế thừa isolation, fingerprints, per-case evidence, guardrails và so sánh
theo cặp khi có ích. Không áp nguyên 45 câu/9 category/threshold Foods cho corpus
mới; không tái tạo harness phức tạp mà chưa xác định nhu cầu.

## 7. Nghiên cứu kỹ thuật bên ngoài đã làm

Nguồn chính thức đã mở; đọc lại khi thiết kế phụ thuộc version hiện hành:

- https://huggingface.co/intfloat/multilingual-e5-small
  (đã đọc phần limitations qua raw README): model truncates ở 512 tokens.
  Bảng atomic dài có rủi ro mất nội dung khi encode dù splitter giữ nguyên.
- https://qdrant.tech/documentation/search/hybrid-queries/
  Query API có independent prefetch và fusion. Chưa chọn native Qdrant fusion;
  cần kiểm version và RRF semantics trước khi thay local implementation.
- https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
  0.6B, 32K model context, output dimensions 32–1024, instruction-aware queries.
- https://huggingface.co/Qwen/Qwen3-Reranker-0.6B
  0.6B, 32K model context; có instruction/template và scoring riêng.
- https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl
- https://docs.nvidia.com/cuda/wsl-user-guide/index.html
  Driver CUDA GPU đến từ Windows; không cài Linux NVIDIA display driver vào WSL.

Chưa kiểm hệ điều hành/driver/PyTorch/GPU trên máy thực. Không bảo đảm 4 GB VRAM
chạy đủ hai model đồng thời. Không mặc định FlashAttention/BF16 hoặc 32K context
phù hợp GTX 1650; các compatibility/dtype/batch/length phải được kiểm riêng.
Không lấy giới hạn context quảng bá làm chunk size hay runtime budget.

## 8. Phân rã thiết kế đề xuất và trạng thái phê duyệt

Phân rã work packages dưới đây chưa được duyệt. Các nguyên tắc chunking đã
được xác nhận tiếp trong session nằm tại mục 13; không đưa chúng trở lại trạng
thái chưa quyết định. Toàn bộ design/spec/plan vẫn chưa được duyệt.

Phân rã công việc thay vì một spec triển khai khổng lồ:

1. Corpus contract, metadata, evidence identity và chunking bảo toàn cấu trúc.
2. Combined Golden / evaluation đa domain, cross-domain và thiếu bằng chứng.
3. Embedding, ingestion, retrieval/fusion, reranking và context assembly.
4. Generation/API/citations, end-to-end evaluation, index transition và guides.
5. Roadmap riêng cho GPU/Qwen3 và cá nhân hóa/multi-turn/Agentic RAG.

Phân rã work packages chưa được duyệt; các đề xuất cơ chế bên dưới là lịch sử,
trạng thái xác nhận mới nhất nằm ở mục 13 và 17–20. Các hành vi sản
phẩm ở mục 1 (partial answer, thiếu thông tin, citation, ẩn kỹ thuật, một lượt)
đã được xác nhận, không đưa chúng trở lại trạng thái “chưa quyết định”.

Các đề xuất kỹ thuật ban đầu (đọc cùng xác nhận mới tại mục 13):

- Thiết kế evidence mapping/API đáp ứng citation đã chốt, tách public sources
  khỏi internal IDs/paths/scores; evaluation có ca thiếu một phần/toàn bộ bằng
  chứng, thông tin có thời hạn, citation correctness và lộ metadata kỹ thuật.
- Chunking theo cấu trúc H1/H2/H3/H4, giữ điều kiện/list/table semantics,
  budget token phù hợp model, cân nhắc child retrieval/parent context nếu cần.
- E5-small CPU baseline; sparse independent retrieval và reranker là nhánh
  thử nghiệm, không default winner.
- Index cô lập cho corpus mới; manifest thay hardcode 572; rollback/cutover
  cần exact authority, không tác động production khi chỉ research.
- Tách chất lượng retrieval, context evidence coverage và answer groundedness.
- GPU work package không chặn bản CPU. Kiểm WSL -> smoke CUDA -> từng model với
  batch/token cap nhỏ -> đo quality/latency/RAM/VRAM -> kiểm runtime coexistence.
- API experiments có provider/model identity và budget rõ; chưa chốt model judge.

## 9. Điểm tiếp tục tại mốc parser closure — lịch sử

User đã approved khảo sát parser sau correction lượt 3. Reviewer tiếp tục
hoàn thiện written spec theo mục 28–29, không chờ báo cáo hoặc xác nhận nữa.
Giữ A baseline, B có chọn lọc, chung chunk set, Top-5 và các quyết định đã chốt.
Golden vẫn chờ tài liệu khóa học user sẽ gửi; phần này chưa được cung cấp chỉ
vì đã đọc reference Day5. Không hỏi dồn hoặc tự chọn tham số từ mẫu tokenizer.


## 10. Giới hạn đọc của các phiên khảo sát trước (bổ sung mới tại mục 18–22)

- Đã đọc bootstrap/workflow, runtime chính, guides rộng, templates mới và
  samples có chủ đích; quét text toàn bộ 204 curated files và AST 62 Python files.
- KHÔNG đọc thủ công từng dòng toàn bộ khoảng 2 triệu ký tự curated text hay
  toàn bộ các harness/tests. Đọc sâu thêm đúng phần quyết định phụ thuộc.
- Samples đọc sâu gồm Hội xuân Gia Lạc, Festival Huế, Nhã nhạc cung đình Huế,
  lịch trình 3 ngày 2 đêm, Vé tham quan Hải Vân Quan; đã xem Huế Wonderverse
  Music Fest và một phần Đầm Chuồn. Một số output dài bị truncate.
- Đã đọc templates festivals/heritage/performing-arts/tourism; không khẳng định
  đã đọc đầy đủ mọi evidence document trong meta hoặc mọi source dump.
- Không chạy tests, model, Qdrant, API hoặc ingestion. Không kiểm live index.
- Không đọc secrets, cài dependencies, đổi config/driver hay chạy benchmark mới.
- Worktree sạch trước lần tạo handoff đầu. Các phiên đầu chỉ sửa hai file
  context/prompt; phiên tiếp theo user đã cấp quyền cập nhật guides/spec/plan
  (trạng thái hiện tại tại mục 22). CURRENT_HANDOFF/backend/corpus vẫn không sửa.
- Session mới kiểm git status/HEAD lại; không giả định state mãi giống snapshot.

## 11. File đồng hành

Prompt copy/paste cho session mới:
`handoff_prompt/FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md`.

Sau khi đọc, session mới tóm tắt rất ngắn phạm vi đã chốt và tiếp tục câu hỏi
ở mục 9. Không khởi động khảo sát toàn repo lại, không trả về plan giả định đã
approved và không bắt đầu kích hoạt GPU chỉ vì có roadmap.

## 12. Xác nhận mới: MVP đồ án, frontend và evaluation

- MVP dùng thử cá nhân cho đồ án tốt nghiệp, không phải triển khai thực tế
  cho người dùng bên ngoài. Không tự thêm yêu cầu production/concurrency/SLA.
- Nghiệm thu ở mức hữu ích: cho phép thiếu sót truy xuất/độ đầy đủ được ghi nhận;
  phải sửa lỗi nghiêm trọng đã phát hiện như bịa giá/ngày/giờ, citation không
  hỗ trợ khẳng định, lộ thông tin kỹ thuật. Không đòi mọi câu hoàn hảo hoặc coi
  bộ kiểm tra đạt là bảo đảm không bao giờ có lỗi.
- Evaluation bao phủ cân bằng 5 domain, kiểm riêng places/services/tickets,
  có so sánh, liên miền, lịch trình, thiếu một phần/toàn bộ bằng chứng và thông
  tin có thời hạn. Cân bằng không đồng nghĩa chia đều số câu. Báo cáo từng nhóm.
- User sẽ gửi tài liệu khóa học RAG về đánh giá/tạo Golden; Foods Golden cũng
  từng tham khảo tài liệu đó. Đến bước Golden phải đọc và đối chiếu trước khi
  chốt số câu, schema, gán evidence, split và threshold. Chưa nhận tài liệu ấy.
- User chấp nhận chờ để có kết quả trên local. Chưa có ngưỡng latency chặn
  nghiệm thu. Ghi thời gian phản hồi ở terminal backend; đề xuất đã ghi nhận
  gồm tổng thời gian và retrieval/reranking/generation, tổng hợp trong evaluation.
  Khi quan sát quá chậm mới tìm nguyên nhân/tối ưu; không quy hết latency cho LLM.
- MVP bắt buộc có frontend, không chỉ backend. Mốc backend/evaluation là trung
  gian; MVP cần luồng hỏi → trả lời → bấm xem bằng chứng trên giao diện thật.
- Tới thiết kế frontend, user sẽ cung cấp dự án llm_rag để tham khảo. Hướng
  công nghệ tham khảo: Next.js, React, TypeScript, Tailwind CSS, Axios,
  lucide-react. Chưa chốt UI/endpoints/streaming; chưa có quyền implement.
- Đã đọc đầy đủ guides/llm_rag_reference_for_hue_rag.md. Các đoạn frontend
  ngoài scope là lịch sử backend Phase 0–6, không giới hạn MVP mới.
- MVP đạt gate là hoàn thành phần cốt lõi đồ án. GPU, cá nhân hóa, multi-turn,
  Agentic RAG là mở rộng theo kết quả và thời gian; không tự bắt đầu khi MVP đạt.
- User chọn corpus/chunking trước Golden. Backend/guides Foods chỉ là reference
  lịch sử, không áp nguyên thiết kế cũ cho full corpus; giữ approval lịch sử.

## 13. Nguyên tắc chunking đã được user xác nhận

Đây là các quyết định trong brainstorming, chưa phải written spec/approved plan.

1. Giữ mục ngắn, cùng chủ đề khi phù hợp; không tự chia nhỏ chỉ vì có nhiều dòng.
   Ví dụ Thông tin Quán bún bò Mệ Kéo: địa chỉ, mức giá, giờ và “thường hết sớm hơn”.
2. Giữ quan hệ nhãn cha/con của danh sách lồng. Ví dụ Hội xuân Gia Lạc: thời
   gian/địa điểm lịch sử khác lần phục dựng cụ thể. Chưa coi mọi list là atomic.
3. Các phần tạo nên một phương án có điều kiện nên giữ cùng nhau khi phù hợp.
   Module biển/đầm phá gồm phạm vi thay thế, cách chọn, điều kiện; không mặc
   định mỗi H3 là một chunk độc lập.
4. Bảng xử lý theo nghĩa: ngắn giữ cùng giải thích; dài có thể chia nhóm hàng
   với tiêu đề cột/đơn vị/đối tượng/điều kiện. Không mặc định giữ nguyên mọi
   bảng hoặc tách mọi hàng. Bảng dự toán có tổng cần giữ quan hệ tính toán.
5. Tự động theo cấu trúc, xem trước trên dữ liệu thật, chỉ dẫn riêng tối thiểu
   ngoài corpus khi có trường hợp thực sự cần. Chưa chốt hình thức chỉ dẫn.
6. Dùng tên tài liệu và chuỗi tiêu đề gốc làm ngữ cảnh nền thay bộ nhãn Foods.
   Giữ phần văn bản giữa các cấp heading, không chỉ lấy leaf. Heading path
   là vị trí trong tài liệu, không tự chứng minh quan hệ địa lý/lịch sử.
7. Cho phép chunk tìm kiếm ngắn và mở rộng context bằng đoạn nguồn liên quan
   đã được xác định theo cấu trúc/chỉ dẫn, có giới hạn; không mặc định lấy toàn
   tài liệu. Áp dụng cho cả A/B. Chưa chọn parent-child framework/graph hay API.
8. Baseline không overlap cố định. Lặp tiêu đề/điều kiện khác với overlap body.
   Chỉ thử overlap ở văn bản dài nếu quan sát mất mạch nghĩa. Đây là quyết định
   mới, không kế thừa máy móc quy tắc no-overlap Foods.
9. Kích thước chọn qua khảo sát tokenizer và evaluation; tính cả nhãn/context/
   prefix trong input thật. Chưa chọn 400 ký tự, 256 token hay tỷ lệ overlap.
   So sánh vài mức phù hợp model khi có approved experiment scope.
10. User xác nhận cuối session: “đồng ý lấy khả năng truy ngược tới đúng đoạn
    nguyên văn làm yêu cầu chung cho cả A và B”. Chunk phải truy tới đúng
    đoạn/các đoạn nguồn; phân biệt body, điều kiện gốc lấy thêm và ngữ cảnh
    do API sinh. Chỉ tên file + H2 không đủ. Chưa chốt locator/schema/version.

### Ba phương án sau đối chiếu llm_rag: user đã xác nhận

- **A — baseline:** chia theo cấu trúc Markdown, không dùng LLM trong chunking;
  bảo toàn nguồn/quan hệ đã chốt, kiểm ngân sách input phù hợp model.
- **B — nhánh API đầu tiên:** giữ ranh giới và evidence của A; LLM đọc chunk
  cùng tài liệu để tạo ngữ cảnh tiếng Việt ngắn giúp tìm kiếm. Lưu phần sinh
  thêm riêng; không dùng làm nguồn gốc/Golden. Generator cần evidence gốc và
  điều kiện gốc liên quan. Chưa chốt exact representation đưa vào reranker/LLM.
- **C — chỉ thử nếu cần:** LLM hỗ trợ ranh giới khi A/B cho thấy hạn chế. Đề xuất
  kỹ thuật là chọn các khối nguồn đã đánh dấu rồi code lấy nguyên văn thay vì
  LLM chép lại toàn văn; chi tiết này chưa có spec/implementation được duyệt.
- Không tự chuyển sang API embedding hoặc model của reference. CPU embedding
  candidates vẫn giữ. API bổ sung ngữ cảnh là bước offline, không tự thêm call
  vào mỗi câu hỏi. Exact provider/model/prompt/budget cho B còn mở.
- So sánh A/B giữ cùng boundaries, embedding và retrieval/context budget tương
  đương; đánh giá trên evidence gốc, không để từ khóa trong summary sinh thêm
  tự tạo điểm đạt. Chưa chốt chi tiết benchmark trước tài liệu khóa học.

User đã nhắc Reviewer nghiên cứu dữ liệu trước khi đề xuất; lựa chọn A/B ban
đầu “heading vs tăng kích thước Foods” không phải quyết định. A/B/C có hiệu lực
là ba phương án vừa nêu sau khảo sát và research. Tránh hỏi user từng tham số
nội bộ; tự tổng hợp bằng chứng và hỏi từng trade-off có ý nghĩa.

## 14. Khảo sát corpus và reference trong session tiếp tục

### Corpus Huế

Đọc lại guide Phase 2, settings, markdown_chunker.py và split_text.py. Dùng
stdlib đọc cấu trúc tất cả 204 file (loại inventory/evaluation), không gọi
backend/models. Số heading theo regex và bảng Markdown theo khối dòng `|`:

| Nhánh | File | H2 | H3 | H4 | Bảng phát hiện |
|---|---:|---:|---:|---:|---:|
| foods | 91 | 457 | 115 | 0 | 24 |
| festivals | 27 | 263 | 210 | 0 | 0 |
| heritages | 29 | 268 | 158 | 10 | 1 |
| performing_arts | 12 | 125 | 90 | 0 | 2 |
| travel/places | 36 | 366 | 595 | 0 | 2 |
| travel/services | 4 | 31 | 75 | 0 | 3 |
| travel/tickets | 5 | 37 | 72 | 2 | 8 |

H2 Foods gồm 90 Nguồn dữ liệu. Counts này là khảo sát text, không chunk output;
khác đơn vị “section khảo sát” ở mục 3 (có intro, loại nguồn), không chứng minh
data đã thay đổi. Guide Foods có counts lịch sử khác, không lấy làm hard gate.
Không đo tokenizer, không chạy lại diagnostic splitter hoặc benchmark.

- Bốn services và ba tickets có intro trước H2. Intro Chi phí du lịch Huế xác
  định bảng là hạn mức kế hoạch, không phải giá nhà cung cấp; quan hệ ngữ nghĩa
  có thể vượt heading gần nhất.
- Tickets có blockquote cảnh báo `[!WARNING]`, HTML `<br>` trong ô, bảng nhiều
  nhà cung cấp/đơn vị tính. Không áp cùng một temporal/provider label cho mọi
  phần của file. Hai bảng dài nhất khảo sát khoảng 3.400 và 3.384 ký tự.
- Bảng Ca Huế phân biệt khách ghép/nguyên thuyền, chính sách trẻ em theo tuổi
  hoặc chiều cao của nhà cung cấp khác nhau; có bao gồm/không bao gồm ngoài bảng.
- Vé Hải Vân Quan có mục “Mô hình dữ liệu chuẩn hóa…” trộn bảng tổng hợp thông
  tin hữu ích và cách diễn đạt quản lý nghiên cứu. Chưa quyết định lọc mục đó;
  không mặc định toàn body của mọi file answer-facing đều cùng vai trò.
- Ghi chú sau bảng Bún bò Huế giới hạn tính khái quát của đặc điểm vùng miền.
- Tài liệu hệ đầm phá và từng thành phần có quan hệ/nhắc lại; không tự gộp entity
  hay deduplicate nội dung liên miền chỉ vì chung từ khóa.

Đã đọc sâu toàn bộ hoặc đoạn liên quan có chủ đích: Quán bún bò Mệ Kéo, TAN.
CAFE, Bún bò Huế, Hội xuân Gia Lạc, Nhã nhạc cung đình Huế, Đại Nội, Huế
Wonderverse Music Fest, Hệ đầm phá Tam Giang–Cầu Hai, Chợ Đông Ba, Chi phí du
lịch Huế, Lịch trình 3 ngày 2 đêm và các tickets. Đọc outline và opening của
5 guide tổng quan, outline cả 5 tickets. Một số output dài bị truncate; không
khẳng định đã đọc trọn mọi file mẫu hoặc đã fact-check nội dung.

### llm_rag và rag_old_0

Đã đọc tài liệu handoff, chương 5 ingestion/chunking và các đoạn liên quan của
deep-dive (không đọc trọn tài liệu 3.024 dòng); đối chiếu pipeline, helpers,
các chunker JSON, mẫu record projects. Một số batch output bị truncate và đọc
bổ sung phần liên quan; không claim audit toàn bộ backend llm_rag.

Canonical reference pointers:

- /home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md
- /home/minhhieu/llm_rag/tai_lieu/rag_system_pipeline_deep_dive.md
- /home/minhhieu/llm_rag/backend/ingestion/pipeline.py
- /home/minhhieu/llm_rag/backend/ingestion/chunking/projects.py
- /home/minhhieu/llm_rag/backend/ingestion/chunking/news.py
- /home/minhhieu/llm_rag/backend/ingestion/chunking/companyInfo.py
- /home/minhhieu/llm_rag/backend/ingestion/helpers/split_paragraphs.py
- /home/minhhieu/llm_rag/tai_lieu/rag_old_0/implementation/ingest.py
- /home/minhhieu/llm_rag/tai_lieu/rag_old_0/implementation/answer.py
- /home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation/ingest.py
- /home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation/answer.py
- /home/minhhieu/llm_rag/tai_lieu/rag_old_0/evaluation/eval.py

Quan sát từ source (không chạy):

- llm_rag JSON tiếng Việt: chia theo nhóm field/khía cạnh, thêm tên đối tượng;
  helper 400 ký tự chỉ dùng một số text dài. Helper split `. ` rồi có thể cắt
  cứng, không phải bộ tách câu tiếng Việt đầy đủ. 450 chunks là evidence cũ.
- rag_old_0 cơ bản: Markdown tiếng Anh, RecursiveCharacterTextSplitter
  chunk_size=1000/chunk_overlap=200 (ký tự), all-MiniLM-L6-v2, Chroma.
- PRO: LLM `openai/gpt-4.1-nano` tạo headline/summary/original_text qua schema;
  ghép cả ba để embed `text-embedding-3-large`. Đây là model trong reference,
  không phải lựa chọn/authorization mới cho Huế.
- AVERAGE_CHUNK_SIZE=100 dùng len(text) để gợi ý số chunk, không phải token
  budget. Prompt gợi ý khoảng 25%/50 words overlap, yêu cầu bao phủ và nguyên
  văn nhưng code không kiểm exact source coverage hoặc nguyên văn.
- PRO answer còn query rewrite, truy xuất cả query gốc/viết lại, merge và LLM
  rerank. Không quy cải thiện toàn pipeline thành cải thiện riêng chunking.
- Evaluator reference dùng keyword trong page_content; judge prompt đọc
  question/reference/generated answer, không thực sự nhận retrieved context.
  Summary sinh thêm có thể làm keyword metrics lệch; không kế thừa làm bằng
  chứng groundedness cho Huế.
- Xem chọn lọc Markdown cells/saved output trong day3/4/5 notebooks và mẫu MD
  about.md; không Run All, không audit toàn bộ notebooks/evaluation. Chưa thấy
  trong phần đã đọc controlled A/B chứng minh riêng PRO chunking thắng trên Huế.

## 15. Research web bổ sung và cách dùng

User cho phép web research và chấp nhận thử API theo ý tưởng PRO. Đã mở nguồn
chính thức dưới đây; không gửi corpus cho provider, không gọi API trả phí.

- https://docs.langchain.com/oss/python/integrations/splitters/markdown_header_metadata_splitter
  Heading splitter giữ header metadata; có thể split tiếp bên trong section.
  Default có thể bỏ headings/whitespace; không tự đáp ứng nguyên văn/citation.
- https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter
  Recursive splitting theo separator; mặc định không phải tách câu tiếng Việt.
- https://docling-project.github.io/docling/concepts/chunking/
  HybridChunker kết hợp document structure và tokenizer; split khi dài, merge
  peers phù hợp, có repeated table headers. Đây là nguồn ý tưởng, chưa chọn
  dependency hoặc khẳng định parser bảo toàn mọi điều kiện của corpus Huế.
- https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/semantic_splitter/
  Semantic splitter dùng embedding similarity giữa nhóm câu; khác chia theo
  field ở llm_rag và khác LLM chia/sinh summary trong PRO.
- https://docs.llamaindex.ai/en/v0.10.18/module_guides/loading/node_parsers/modules.html
  Tài liệu lịch sử cảnh báo regex thiên về tiếng Anh; không coi là xác nhận
  behavior mọi version hiện tại. Có đọc reference hierarchical/sentence window,
  chưa chọn framework hoặc node hierarchy cụ thể.
- https://huggingface.co/intfloat/multilingual-e5-small/raw/main/README.md
  Đã xác minh 512-token truncation và prefix query/passage kể cả non-English.
  Phải tính input thật cả nhãn/prefix/special tokens, không lấy 512 làm body cap.
- https://aclanthology.org/L08-1355/
  Tách từ tiếng Việt khác split khoảng trắng; syllable/word/model token khác nhau.
- https://github.com/undertheseanlp/underthesea/blob/main/NLP.md
  Có sent_tokenize và word_tokenize riêng. Chưa cài/chọn Underthesea; không tự
  nối dấu gạch dưới, đổi dấu, dịch tiếng Anh hay sửa nguyên văn corpus.
- https://www.anthropic.com/engineering/contextual-retrieval
  LLM bổ sung ngữ cảnh riêng cho chunk trước embedding/BM25; khác summary chung
  và khác LLM chọn boundary. Kết quả của tác giả là động lực thử B, không là
  evidence tiếng Việt/Huế hoặc lý do tự bật hybrid/reranker. Chưa dùng Claude.
- https://aclanthology.org/2025.findings-naacl.114/
  “Is Semantic Chunking Worth the Computational Cost?”: abstract báo cải thiện
  không nhất quán trong tác vụ khảo sát. Chỉ đọc abstract/tóm tắt nguồn, chưa
  audit toàn bộ phương pháp; không kết luận mọi semantic/LLM chunking đều kém.

Không có winner cho Huế từ research hoặc llm_rag đã chạy được. Chọn bằng cấu
trúc thực tế, kiểm toàn vẹn và evaluation có kiểm soát; chưa chốt thư viện.

## 16. Kết thúc phiên trước — đã được thay thế

Phiên đầu tạm dừng trước khi chốt hành vi nguồn thay đổi. Phiên tiếp theo user
đã xác nhận citation bản ingest, ingest khi server tắt và startup yêu cầu ingest
lại khi corpus thêm/sửa/xóa (mục 17). Đã bỏ câu hỏi nguồn cũ/mới ở đây vì không
còn là next action. Trạng thái mới nhất, phần còn mở và prompt tiếp tục ở mục
20–22 cùng file FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md.

## 17. Xác nhận tiếp theo: baseline trước, context expansion là thử nghiệm

- User xác nhận citation dùng nguyên văn bản đã ingest; ingest khi server tắt.
  Startup phát hiện file thuộc corpus thêm/sửa/xóa thì yêu cầu ingest lại và
  chưa phục vụ chatbot. Chưa chọn cơ chế kiểm tra hoặc locator/schema.
- User xác nhận ingest toàn curated answer-facing corpus vào Qdrant và ví dụ
  giữ quan hệ giá/điều kiện/không bao gồm của tài liệu vé Duyệt Thị Đường.
- User đồng ý thiết kế Top-5 chunk chính rồi lấy thêm điều kiện gốc, không loại
  điều kiện bắt buộc vì điểm thấp, gộp trùng và giữ nhóm trong ngân sách token.
- Xác nhận mới nhất điều chỉnh phạm vi: MVP ban đầu dùng pipeline cơ bản,
  chưa triển khai/bật bước tự lấy thêm điều kiện liên kết. Thiết kế trên được
  ghi vào hướng thử nghiệm/spec/plan sau baseline. Không hỏi lại để bật mặc định.
- User lo context thêm thông tin không liên quan làm Qwen3.5 9B trả lời mơ hồ;
  đây là giả thuyết cần kiểm qua evaluation, chưa có observed evidence.
- User muốn thử các cách theo guides Phase 7–8 như Foods trên corpus mới.
  Giữ baseline rồi controlled benchmark; không áp nguyên Golden, thresholds,
  ngân sách 3.000 ký tự hoặc các model/matrix lịch sử đã bị thay thế.
- Citation nguyên văn, chunking bảo toàn nghĩa, partial-answer policy, frontend
  và evaluation vẫn là yêu cầu MVP. API-context B khác lấy thêm nguồn sau Top-5.
- User trực tiếp yêu cầu ghi vào specs/plans. Đã tạo hai bản ghi quyết định và
  hướng thử nghiệm, chưa phải written spec/implementation plan hoàn chỉnh:
  `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md` và
  `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`.
- Bước tiếp theo: tiếp tục thiết kế chunking baseline A và evidence locator tối
  thiểu; không quay lại hỏi nguồn cũ/mới hoặc mặc định xây dependency expansion.
  Written spec rồi implementation plan/Review Contract vẫn cần duyệt riêng.

## 18. Xác nhận baseline chunking và cách chuẩn bị tài liệu cho Implementer

User làm rõ MVP mới là MVP Foods đã thực hiện trong guides/backend, điều chỉnh
cho toàn corpus. User đã xác nhận đề xuất đối chiếu guide Phase 2, code và mẫu
thực tế: giữ discovery/H1/no fixed overlap, thay H2-only/400 ký tự/atomic mọi bảng/
nhãn Foods/bảy fields/count 572 bằng cấu trúc và ngân sách token, evidence locator.
Hướng khoảng ký tự trong bản nguồn ingest cùng nguyên văn được chấp nhận trong
đề xuất; exact schema/offset semantics, tokenizer budget/parser còn chưa chốt.

User yêu cầu đọc thêm reports và user_reports liên quan có `simplicity`; đã đọc
implementation/review của Phase 2, 3, 4–5, 6, post-simplicity Phase 7 và các user
reports phù hợp Phase 2, 4–5, 7. Không đọc report ngoài bộ lọc trong bước này,
không chạy lại tests/models/API. Các lệnh/tests liệt kê dài có phần đọc chọn lọc.

Phát hiện cần giữ: Phase 3 còn sparse TF-IDF nhưng Phase 4–5 đã xóa khỏi runtime;
Phase 4–5 có context JSON nhưng Phase 6 đã đổi thành labeled string/answer-only.
Reports là evidence theo thời điểm, không tự override source và requirement mới.

User giao Reviewer đồng bộ guides, viết spec/plan chi tiết, chất lượng và vừa đủ.
Đã cập nhật guide index và Phase 2 với trạng thái full-corpus đang thiết kế,
giữ contract/approval Foods lịch sử. Bổ sung quyết định chunking và evidence
vào hai bản thảo spec/plan đã tạo, không tạo approved implementation plan.
Chưa đồng bộ thiết kế chi tiết Phase 3–8 vì các contracts đó còn cần thảo luận.

Mẫu output/locator và khảo sát tokenizer sau đó đã được thực hiện ở mục 19;
quyết định chung chunk set ở mục 20. Bước tiếp tục theo mục 21, không quay lại
hỏi những nguyên tắc đã xác nhận. Written spec hoàn chỉnh → user duyệt →
implementation plan/Review Contract → user duyệt.

## 19. Khảo sát tokenizer và mẫu output/locator — evidence đầy đủ

User đã cho phép chuyển sang mẫu output, locator và khảo sát tokenizer. Đã chạy
`uv run --no-sync python /tmp/hue_full_corpus_tokenizer_survey.py` bằng project
environment (Transformers 5.14.1; PyVi dependency trong project pin 0.1.1).
AutoTokenizer đọc exact snapshot local với `local_files_only=True`; không tải
weights/tokenizers, không inference embedding/reranker, không production chunker,
Qdrant/API hoặc quality benchmark. Không nạp `.env`/secrets.

`uv` lần đầu bị cache filesystem sandbox chặn; đã xin và được approval chạy
ngoài sandbox. Script khảo sát lần đầu dùng sai header bảng (`| Đối tượng`),
dừng với `ValueError: substring not found`; sửa thành `| Hạng mục đối tượng`
và heading path đúng mục 2.3 rồi rerun thành công sáu mẫu. Không dùng lần fail
làm kết quả hoàn tất. Không chạy lại survey trong lần cập nhật tài liệu cuối.

### Models, snapshots và giới hạn đã đọc

Cache root: `/home/minhhieu/.cache/huggingface/hub/`.
Đường dẫn tokenizer là `models--<model-id thay / bằng -->/snapshots/<revision>`.

| Model | Revision khảo sát | Input limit trong config |
|---|---|---:|
| intfloat/multilingual-e5-small | 614241f622f53c4eeff9890bdc4f31cfecc418b3 | 512 |
| intfloat/multilingual-e5-base | d128750597153bb5987e10b1c3493a34e5a4502a | 512 |
| CODE4LIFEOFFICIAL/huydang-dek21-embedding | 517f1af7dd04a57194f1de2990f0c6ede0a3109b | 256 |
| cross-encoder/ms-marco-MiniLM-L-6-v2 | 233902d25c440f23af6f7d6e94d2946bac0bee0a | 512 (cặp query/document) |

E5/HuyDang limits khớp tokenizer config, `sentence_bert_config.json` và
`backend/embedding/dense_benchmark.py`. MiniLM tokenizer config có
`model_max_length=512`; chưa load model để kiểm runtime truncation. Những
revision này là identity khảo sát, chưa tự là approved full-corpus model pins.

### Cách tạo text và đếm token

1. Đọc bytes UTF-8; đổi CRLF và CR thành LF. Không Unicode-normalize hoặc bỏ dấu.
2. Chọn khối bằng heading/bảng gốc; bỏ khoảng trắng ngoài cùng và separator
   `---` cuối vùng nếu có. Giữ nguyên phần còn lại, kể cả Markdown/list/HTML.
3. Label là `title + "\n" + " > ".join(heading_path) + "\n"`.
   `search_text = label + body`. Đây là format khảo sát, chưa chốt format runtime.
4. E5: tokenize `"passage: " + search_text`, add_special_tokens=True.
5. HuyDang: `ViTokenizer.tokenize(search_text)` rồi tokenize, không thêm E5 prefix.
6. MiniLM: tokenize cặp `(query, search_text)`, không E5 prefix, có special tokens.
7. Tất cả `truncation=False`; đo độ dài đầy đủ, không coi text bị truncate là vừa.
8. Tìm lại body trong source đã chuẩn hóa LF và kiểm
   `source_text[start:end] == body`; cả sáu mẫu đều True. Đây là kiểm substring
   mẫu, không chứng minh parser/locator hoàn chỉnh hoặc mapping qua Qdrant.

### Kết quả

| Khối nguồn | Ký tự body | E5-small | E5-base | HuyDang | MiniLM pair |
|---|---:|---:|---:|---:|---:|
| me_keo_info | 274 | 97 | 97 | 78 | 144 |
| gia_lac_info | 1171 | 352 | 352 | 272 | 512 |
| sea_module | 629 | 204 | 204 | 160 | 305 |
| ngo_mon | 1726 | 530 | 530 | 423 | 738 |
| budget_one_day | 754 | 280 | 280 | 212 | 371 |
| ca_hue_table | 1050 | 444 | 444 | 339 | 574 |

Sáu mẫu được chọn có chủ đích; không phải toàn bộ chunk output hoặc phân bố
thống kê đại diện corpus. Bảng Ca Huế chưa kèm mọi cảnh báo/bao gồm/không bao gồm
ngoài bảng; dự toán một ngày chưa kèm intro toàn tài liệu về bản chất hạn mức.
Khi bổ sung các phần này, phải đếm lại input thật. Mẫu vừa token chưa đồng nghĩa
đủ nghĩa hoặc retrieval tốt. Câu hỏi dài hơn có thể làm MiniLM vượt giới hạn.
Chưa đo tokenizer Qwen3.5 9B, token budget generator hoặc full prompt input.

### Vị trí, label và câu hỏi cụ thể để kiểm lại

Các đường dẫn dưới đây tương đối `knowledge-base-hue/`. Offsets là khoảng
`[start, end)` Unicode code points trên source chuẩn hóa LF, không phải byte
offsets hoặc UTF-16 indices. Các label lưu literal newline trong code block.

**me_keo_info**

- Source: `foods/restaurants/quan bun bo me keo.md`.
- Body span: `[516, 790)`, exact-match True.
- Query: Quán bún bò Mệ Kéo mở cửa đến mấy giờ?
- Label:

```text
Quán bún bò Mệ Kéo
Thông tin
```

Body nguyên văn của mẫu Mệ Kéo:

```markdown
- Địa chỉ: Số 20 đường Bạch Đằng, phường Phú Cát, Thành phố Huế (ngay khu vực chân cầu Gia Hội, không gian nằm trong một ngôi nhà gỗ cổ kính đậm chất Huế).
- Mức giá: Dao động từ 25.000 VNĐ – 50.000 VNĐ/tô
- Giờ hoạt động: Khoảng 6:00 sáng – 10:00 sáng (thường hết sớm hơn).
```

**gia_lac_info**

- Source: `festivals/festival/Hội xuân Gia Lạc.md`.
- Body span: `[40, 1211)`, exact-match True.
- Query: Hội xuân Gia Lạc tổ chức ở đâu và vào thời gian nào?
- Label:

```text
Hội xuân Gia Lạc
Thông tin chung
```

**sea_module**

- Source: `travel/services/Lịch trình du lịch Huế 3 ngày 2 đêm.md`.
- Body span: `[3182, 3811)`, exact-match True.
- Query: Có thể thay ngày cuối bằng đi biển và đầm phá không?
- Label:

```text
Lịch trình du lịch Huế 3 ngày 2 đêm
Module thay thế: Biển và đầm phá
```

**ngo_mon**

- Source: `heritages/heritage/Đại Nội Huế.md`.
- Body span: `[10219, 11945)`, exact-match True.
- Query: Ngọ Môn có cấu trúc và ý nghĩa lịch sử như thế nào?
- Label:

```text
Đại Nội Huế
Các công trình kiến trúc hạt nhân của Hoàng thành > Ngọ Môn
```

**budget_one_day**

- Source: `travel/services/Chi phí du lịch Huế.md`.
- Body span: `[2561, 3315)`, exact-match True.
- Query: Một ngày tại Huế cần dự toán bao nhiêu tiền?
- Label:

```text
Chi phí du lịch Huế
Dự toán một ngày tại Huế
```

**ca_hue_table**

- Source: `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`.
- Body span: `[10760, 11810)`, exact-match True.
- Query: Vé Ca Huế cho trẻ em được tính như thế nào?
- Label:

```text
Vé biểu diễn nghệ thuật và trải nghiệm sông Hương
2. Ca Huế trên sông Hương và dịch vụ thuyền rồng > 2.3. Chi tiết bảng giá khảo sát dịch vụ Ca Huế > A. Vé khách lẻ ghép thuyền (Tour ghép đoàn)
```

Với 5 mẫu heading, body bắt đầu sau dòng heading đã nêu và kết thúc trước heading
kế tiếp: Mệ Kéo trước `## Món ăn / trải nghiệm`; Gia Lạc trước `## Tổng quan`;
module biển trước `## Module thay thế: Làng nghề và nghỉ dưỡng`; Ngọ Môn trước
`### Hồ Thái Dịch và Cầu Trung Đạo`; dự toán một ngày trước
`## Dự toán hai ngày một đêm tại Huế`. Bảng Ca Huế bắt đầu từ header
`| Hạng mục đối tượng`, kết thúc trước dòng `- **Bao gồm:**` ngay sau bảng.
Offsets/counts chỉ đúng snapshot text đã đo, không áp mù nếu nguồn đã đổi.

### Diễn giải và schema đã trình, chưa chốt chi tiết

- Module biển 629 ký tự có thể giữ chung trong mẫu đã đo; 400 ký tự sẽ ép chia
  dù không cần thiết về model limits.
- Gia Lạc 352 E5 nhưng 272 HuyDang cần tách thêm cho chung chunk set; MiniLM
  pair mẫu đúng 512 nên không có dư địa cho câu hỏi dài hơn.
- Ngọ Môn vượt limits tất cả candidates: cần tách theo đoạn/nhóm list có nghĩa.
- Bảng Ca Huế vừa E5 nhưng vượt HuyDang/MiniLM. Bảng không được miễn input limit.
- Không suy ra một số ký tự/tokenizer chung hoặc chọn trước 256/384 body tokens.

Output đề xuất: `chunk_id`, `source`, `domain`, `subdomain`, `title`,
`heading_path`, `evidence_parts`, `search_text`. Tên fields và schema chưa duyệt.
`evidence_parts` lưu nguyên văn, vai trò body/header/condition cùng source span.
Bảng chia có thể có phần header và phần hàng ở các spans khác nhau, được ghép
để đọc; không gọi text render đã ghép là exact substring của file. Phần title/
heading gốc và nhãn trình bày cũng cần phân định, không bịa thêm quan hệ thực tế.

Locator đề xuất: `[start,end)` trên UTF-8 decoded source chuẩn hóa CRLF/CR → LF,
đếm Unicode code points từ 0. Backend resolve và trả evidence text cho UI;
không yêu cầu JavaScript dùng trực tiếp offsets Python. Exact convention này
mới trình bày, chưa được user duyệt riêng. Hướng lưu khoảng ký tự + nguyên văn
đã được chấp nhận trong đề xuất tổng thể trước đó. ID deterministic khi input
không đổi không bảo đảm ID không đổi sau edit/rechunk; công thức ID chưa chốt.

Raw script/results còn tại `/tmp/hue_full_corpus_tokenizer_survey.py` và
`/tmp/hue_full_corpus_tokenizer_survey.json`. Không phụ thuộc /tmp để tiếp tục:
đã lưu method, query, label, offsets, counts, models và giới hạn đầy đủ tại đây.

## 20. Xác nhận cuối: dùng chung chunk set cho benchmark embedding

User chọn **A — Dùng chung một bộ chunk cho E5-small, E5-base và HuyDang; kiểm
input bằng từng tokenizer để tránh vượt giới hạn**, nhằm tách ảnh hưởng của
embedding model. Đã trả lời; không hỏi lại hoặc ghi còn chờ xác nhận.

Cùng boundaries, source evidence và nội dung/ngữ cảnh nền. Model-specific
preprocessing vẫn giữ đúng contract: E5 query/passage prefix; HuyDang PyVi;
không sửa evidence gốc theo preprocessing. Độ dài đo trên input thực của từng
model gồm nhãn/prefix/special tokens, không lấy 256 token HuyDang làm 256 token E5.
So sánh cùng câu hỏi, retrieval settings và metric definitions khi thiết kế
benchmark. Chia riêng từng model chỉ là phương án tương lai nếu có nhu cầu và
phép so pipeline riêng; không thuộc benchmark embedding đầu tiên đã chốt.

Phân biệt ba bộ lựa chọn cùng từng được gọi A/B:

1. Chunking A/B/C: A cấu trúc Markdown; B sinh context offline bằng API giữ
   chunk A; C LLM boundary chỉ nếu cần. Các quyết định này vẫn giữ.
2. Citation A: giữ evidence bản ingest; startup gate đã chốt ở mục 17.
3. Benchmark embedding A: chung chunk set ba models, quyết định mới tại đây.

Chung chunk set không tự chốt parser, target token, representation mọi stage,
MiniLM query budget hoặc generator budget. Không coi việc user chọn A là cho
phép chạy full benchmark, API hoặc reindex. B preprocessing cũng phải kiểm lại
input sau thêm context, không âm thầm để model truncate; budget B còn mở.

## 21. Kế hoạch tại mốc trước khảo sát bổ sung — đã được mục 29 thay thế

Các bước chia mẫu dưới đây đã được Implementer thực hiện trong session này.
Giữ để giải thích lịch sử; không dùng làm next action hiện tại.

Không có blocker cần user trả lời ngay. Lần này user yêu cầu ghi nhận đầy đủ
trước khi tiếp tục; không tự mở bước research/experiment mới trong lượt cập nhật.
Phiên sau bootstrap/read-only Git rồi tiếp tục thiết kế cụ thể, không khảo sát
lại toàn repo hoặc hỏi lại các quyết định đã chốt.

### Việc Reviewer nên làm tiếp

1. Dùng số đo và samples trên để trình cách chia chung cho **Gia Lạc, Ngọ Môn,
   bảng Ca Huế**, là các trường hợp đã quan sát vượt limits. Giữ Mệ Kéo/module
   biển làm đối chứng mục ngắn; kiểm thêm intro của bảng dự toán khi cần.
2. Trình các chunk minh họa đầy đủ title/heading/body/điều kiện và evidence spans,
   đếm lại input bằng từng tokenizer. Đây là khảo sát text/tokenizer có mục tiêu,
   không implementation runtime. Không báo số chunk production khi chưa có parser.
3. Đề xuất policy kích thước: mục tiêu đóng gói, hard input limits theo từng model,
   ưu tiên ranh giới và cách xử lý nhóm không thể vừa mà vẫn đủ nghĩa. Không ép
   mọi chunk bằng nhau hoặc để lớn tùy ý. Chỉ mở khảo sát cấu trúc/tokenizer toàn
   corpus khi cần đánh giá policy, ghi rõ chưa quality benchmark.
4. Hoàn thiện locator/schema bằng ví dụ thật: header+rows, nội dung giữa headings,
   ảnh bị bỏ, các đoạn không liên tục, newline normalization. Chọn parser sau
   đối chiếu khả năng giữ positions, không dựng framework/parser custom lớn nếu
   công cụ trực tiếp đáp ứng. Chưa chọn dependency hoặc cho phép cài đặt.
5. Khi chunking design đủ rõ, hoàn thiện written spec để user duyệt; đồng bộ
   guide Phase 2, rồi viết implementation plan/Review Contract và chờ duyệt plan.
   Chưa giao Implementer hoặc sửa backend trước các điểm duyệt đó.

### Các quyết định chưa chốt (hỏi khi có ví dụ/trade-off, không hỏi dồn)

- Khi một nhóm ý nghĩa cùng nhãn/header bắt buộc vượt input limits của chung
  chunk set: cách chia và giữ điều kiện tối thiểu; nếu vẫn không đủ, giải pháp
  trực tiếp nào phù hợp. Reviewer phải trình mẫu và đề xuất trước khi hỏi user.
- Exact token packing policy; chưa chọn target 256/384/512 chung. Baseline
  không overlap cố định đã chốt, không mở lại tỷ lệ overlap khi chưa có nhu cầu.
- Locator normalization/schema và chunk ID; startup change detection thực hiện
  thế nào; chỉ hành vi từ chối phục vụ khi cần reingest đã được xác nhận.
- Lọc metadata/quản lý lẫn answer documents: bảng chuẩn hóa Hải Vân Quan có nội
  dung hữu ích; không loại toàn mục chỉ vì tên. Không tự sửa corpus hoặc mặc định
  nguồn nào thắng khi trùng/mâu thuẫn giữa các domain.
- MiniLM input query+document, budget/truncation policy; generator token budget,
  prompt/partial-answer/citation contract và exact OpenRouter configuration.
- Golden/evaluation sau tài liệu khóa học; số câu/schema/threshold còn mở.
- API preprocessing B model/prompt/budget và thử nghiệm context expansion sau
  Top-5; không để hai nhánh này chặn baseline hoặc trộn biến trong phép so đầu.

Câu hỏi kế tiếp không nên là lặp lựa chọn A/B embedding. Reviewer nên mở bằng
“Với bộ chunk chung đã chốt, đây là cách tôi đề xuất chia phần Gia Lạc/bảng Ca Huế
đang vượt giới hạn…” rồi trình mẫu đủ nghĩa và số đo. Chỉ hỏi một quyết định
thực sự làm thay đổi design khi còn trade-off, không giao user tự thiết kế thuật toán.

## 22. Tài liệu, evidence và trạng thái workspace để chuyển phiên

### Phạm vi tài liệu Reviewer sở hữu

User yêu cầu đồng bộ guides, viết specs/plans chi tiết/chất lượng/vừa đủ cho
Implementer. Guide giữ behavior/scope/contracts/acceptance; spec giữ design và
lý do; plan giữ thứ tự sửa, files/consumers, checks/evidence/Review Contract.
Không chép report hoặc khóa mọi tên hàm/class nội bộ. Không biến phần chưa chốt
thành plan thực thi hoặc tái lập framework đã loại trong simplicity campaign.

Hiện đã cập nhật:

- `guides/README.md`: entrypoint workstream full-corpus, không đổi approval Foods.
- `guides/phase_2_foods_markdown_chunking.md`: phần full-corpus phía đầu, giữ
  history phía dưới; chung chunk set được thêm theo xác nhận cuối.
- `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`: bản thảo
  quyết định chunking/context/locator, evidence simplicity và tokenizer; còn
  điểm mở nên chưa phải approved written spec hoàn chỉnh.
- `docs/superpowers/plans/2026-09-09-full-corpus-context-experiment-notes.md`:
  ghi chú kế hoạch/experiment và dependencies, không phải approved implementation
  plan/Review Contract. Chung chunk set được ghi vào control của embedding.
- Hai file context/prompt này đã cập nhật theo yêu cầu trực tiếp cuối phiên.

Chưa cập nhật chi tiết tất cả guides Phase 3–8, chưa sửa CURRENT_HANDOFF hoặc
Project_Status. Các hướng post-08c trong những file cũ không override task mới.

### Reports simplicity đã đọc trong phiên này

Paths dưới đây là evidence đúng scope user yêu cầu; Phase 0/1 simplicity reports
đã thấy trong danh sách nhưng chưa đọc ở bước này vì chưa ảnh hưởng quyết định.
Không mở lại reports ngoài bộ lọc chỉ để kiểm tra đủ danh sách.

```text
reports/phase_2_foods_markdown_chunking_simplicity_review.md
reports/phase_2_foods_markdown_chunking_simplicity_implementation_report.md
reports/phase_2_foods_markdown_chunking_simplicity_codex_review.md
reports/user_reports/phase_2_foods_markdown_chunking_simplicity_user_report.md
reports/phase_3_embedding_sparse_representation_simplicity_review.md
reports/phase_3_embedding_sparse_representation_simplicity_implementation_report.md
reports/phase_4_5_qdrant_retrieval_simplicity_implementation.md
reports/phase_4_5_qdrant_retrieval_simplicity_codex_review.md
reports/user_reports/phase_4_5_qdrant_retrieval_simplicity_user_report.md
reports/phase_6_generation_api_simplicity_implementation_report.md
reports/phase_6_generation_api_simplicity_codex_review.md
reports/phase_7_post_simplicity_correction_implementation_report.md
reports/phase_7_post_simplicity_correction_codex_review.md
reports/user_reports/phase_7_post_simplicity_correction_user_report.md
```

Phát hiện có ảnh hưởng (không rerun, đây là historical evidence):

- Phase 2 giữ ordered text/metadata/order 572 chunks trước/sau, hai modules;
  400 ký tự được giữ để không đổi input Foods, không chứng minh full-corpus tối ưu.
- Phase 3 concrete E5, native batching, bỏ base/cache/remote wrapper; sparse
  TF-IDF còn ở thời điểm đó, đã bị Phase 4–5 loại khỏi runtime.
- Phase 4–5 active/candidate ranking parity 104/104 cho từng ba profiles; candidate
  dense-only chưa cutover. Reviewer correction ghi focused 27, full non-paid
  90 passed/6 deselected; không lấy claim 91 của handoff hay 8 evaluation tests
  trong implementation report làm chuẩn. Context JSON ở đây bị Phase 6 thay.
- Phase 6 dùng labeled string, tối đa 5 chunks/3.000 ký tự và answer-only API;
  Reviewer exact suite 10 passed, Notebook 05–06 chạy thật tại thời điểm đó.
  Bỏ JSON/source mapping cũ không cấm citation mới khi có requirement thật.
- Phase 7 post-simplicity correction: reviewer smoke 20 rows, 0 errors;
  keyword MRR 0.7917/nDCG 0.8020/coverage 96.67%, answer 4.40/4.05/4.25.
  Implementer là run riêng: answer 4.20/4.05/4.10; không trộn hai run hoặc gọi
  là regression từ những số khác nhau. Không chạy paid full 104 trong correction.
- Phase 8 evidence đã đọc ở phiên trước được giữ ở mục 6; không bị xóa chỉ vì
  tên report không có simplicity, nhưng không mở lại trong bước đọc bị giới hạn.

Source mới đối chiếu trong phiên: guide Phase 2, markdown_chunker.py,
split_text.py, tests/test_markdown_chunker.py, ingestion/pipeline.py,
vectorstore/points.py, config/settings.yaml (đoạn liên quan), startup count gate,
embedding/embedder.py, embedding/dense_benchmark.py (preprocessing/catalog),
reranking/cross_encoder.py, retrieval/context_builder.py; guides Phase 7–8 và
README. Không audit từng dòng mọi backend module/test; một số report dài đọc
chọn lọc sau output truncation. Source hiện tại xác nhận E5 concrete, context
string, hardcode Foods/572 và fixed payload allowlist như findings trước.

Mẫu đọc chọn lọc mới gồm Mệ Kéo, Hội xuân Gia Lạc, Đại Nội, chương trình nghệ
thuật Duyệt Thị Đường, Chi phí du lịch, Lịch trình 3 ngày 2 đêm, vé biểu diễn/
sông Hương và mục bảng chuẩn hóa vé Hải Vân Quan. Không fact-check giá/luật,
không claim đã đọc đầy đủ mọi sample hoặc toàn corpus trong phiên này.

### Git/runtime/authority

HEAD kiểm tra lại: `ea87d3ed52851f6b6ab5c47b138540ebc8ff8340`, nhánh `main`.
Worktree dự kiến sau lần ghi này: 2 tracked guides modified, 4 untracked files
(hai docs spec/plan và hai session_prompt files). Chưa stage/commit/push.
Phiên sau phải kiểm lại, không reset/overwrite thay đổi không liên quan.

Không sửa runtime/corpus/index; không chạy tests/benchmark/models/API, không
cài dependency/driver hoặc mở GPU. Đã chạy tokenizer/PyVi khảo sát như mục 19
và đọc/ghi Markdown trong scope user cấp; không gọi đây là model inference.
User đã cho phép research trước; phiên này đủ context nên chưa browse web mới.
Research sâu/parser/API docs chỉ khi quyết định cần evidence, không mở broad
research hoặc paid calls tự động. Không đọc/in secrets; không subagent.

User yêu cầu ghi nhận để có thể bắt đầu session tiếp theo, rồi tiếp tục khi
sẵn sàng; không coi cập nhật tài liệu là hoàn tất design hoặc implementation.
User không cần chép/tổng hợp lại context, chỉ gửi đường dẫn prompt chuyển phiên.

## 23. Xác nhận nhánh B có chọn lọc và phân công tiết kiệm giới hạn sử dụng

User yêu cầu Reviewer tập trung brainstorming, phân tích evidence, thiết kế
specs/plans/guides; giao code, đo tokenizer, thống kê và tests cho Implementer
qua prompt do user chuyển tiếp. Reviewer chỉ đọc/kiểm phần cần thiết cho
quyết định, không chạy lại công việc có evidence đủ hoặc tự dùng subagent.

Implementer đã khảo sát chia mẫu và bổ sung đến lượt 3:
- `reports/full_corpus_chunk_samples_tokenizer_survey_2026_09_09.md`
- `reports/artifacts/full_corpus_chunk_samples_2026_09_09.json`
- `reports/artifacts/full_corpus_chunk_samples_2026_09_09.py`

Gia Lạc/Ngọ Môn P1 là mẫu ưu tiên Reviewer đề xuất. Ca Huế sau khi thêm nguyên
văn câu dẫn khảo sát tháng 09/2026 phải tách riêng hàng khách VN/QT; hai chunk
trẻ em giữ nhà cung cấp, header và Không bao gồm, đạt 248/245 HuyDang và
479/459 MiniLM với query dài đã cố định. Reviewer đề xuất chunk dịch vụ riêng
có câu dẫn để giữ phạm vi. Đây là số đo Implementer báo cáo, Reviewer chưa
rerun; không chứng minh chất lượng retrieval hoặc parser toàn corpus.

Research reference nằm trong
`reports/full_corpus_chunking_reference_research_2026_09_09.md` (bản correction).
Bản đầu có ví dụ tự soạn bị gọi là dữ liệu thật, sai model PRO và gán nhầm
số đo; đã yêu cầu correction. Reviewer kiểm chọn lọc source PRO và nguồn Ca
Huế, không chứng nhận mọi chi tiết trong report. Không lấy MRR bài học làm
ablation chunking; không loại nhánh API chỉ vì nối context vào chunk gần đầy
sẽ vượt giới hạn. Không dùng các khẳng định tuyệt đối còn sót làm contract.

**Quyết định mới nhất của user: lựa chọn 1 cho B.** Giữ nguyên bộ chunk A;
chỉ bổ sung context tìm kiếm do API sinh khi input hoàn chỉnh vừa cả ba
embedding tokenizers E5-small/E5-base/HuyDang theo đúng preprocessing.
Chunk không vừa giữ representation A. Không cắt body/điều kiện, đổi model,
đổi boundaries hoặc tạo bộ chunk nhỏ hơn riêng cho B. Context sinh lưu riêng,
không là evidence/citation/Golden. Báo tỷ lệ chunk thực sự được bổ sung và
đánh giá toàn bộ tập câu hỏi, không chỉ các ca tốt lên. Chưa thêm vector riêng,
câu hỏi giả định hoặc metadata search trong lượt thử B đầu tiên.

A là baseline cấu trúc; B là thử nghiệm sau baseline; C chỉ xét khi có lý do
từ A/B. Giữ tối đa 5 chunk chính ở baseline, không tự mở context expansion.
Chưa chốt provider/model/prompt/budget API, parser, schema/locator chi tiết,
MiniLM query policy hoặc generator representation. Không coi quyết định B
là approval toàn bộ written spec, implementation plan hay paid execution.

**Next action tại mốc này (đã tiến tới mục 24–29):** Reviewer hoàn thiện đề xuất schema/locator và nhóm điều kiện
bằng các mẫu đã có; chỉ giao kiểm tra parser/source positions có mục tiêu
cho Implementer khi cần evidence. Không lặp lại khảo sát tokenizer đã xong
hoặc hỏi lại A/B/C, chung chunk set hay lựa chọn B có chọn lọc.

Workspace vẫn có hai guides modified và docs/context/reports/artifacts
untracked; không gọi là Git sạch. Chưa stage/commit/push. Đã đồng bộ quyết định
B vào bản thảo spec, experiment notes, guide Phase 2 và prompt chuyển phiên;
chưa sửa backend/corpus/index, CURRENT_HANDOFF hoặc Project_Status.

## 24. Lịch sử giao khảo sát parser — đã hoàn tất, xem mục 29

User xác nhận cho Reviewer thực hiện bước tiếp theo và quyết định phần thiết
kế; khi cần code/khảo sát, tạo prompt để user chuyển Implementer. Reviewer
đã cụ thể hóa đề xuất schema record/evidence_parts, normalization, giới hạn
ID/locator và condition mapping trong bản thảo spec hiện có. Chưa chốt parser,
format chỉ dẫn ngoài corpus hoặc công thức chunk ID; written spec/plan vẫn
cần duyệt trước implementation.

Lockfile có markdown-it-py 4.2.0 và mistune 3.3.4; Reviewer chưa kiểm package
cài thực tế. Đã đọc tài liệu chính thức Token.map/Using markdown_it: map theo
dòng, không phải character offsets, không có cho mọi inline token. Không
chạy parser/tokenizer hoặc tests trong lượt này.

Prompt user chuyển Implementer:
`handoff_prompt/FULL_CORPUS_PARSER_LOCATOR_SURVEY_HANDOFF.md`.
Scope: khảo sát một parser trên vài vùng thật của Gia Lạc/Đại Nội/Ca Huế/
Chi phí/Hải Vân Quan, exact spans/list/table/image/blockquote và đề xuất nhỏ
cho liên kết điều kiện ngay ingest. Không runtime/corpus/index/API mutation.
Outputs dự kiến: report `reports/full_corpus_parser_locator_survey_2026_09_09.md`
và script/JSON được chỉ định trong prompt. Chưa có kết quả khảo sát ở thời
điểm ghi mục này. Next action của Reviewer: nhận report rồi quyết định parser
và hoàn thiện schema/locator, không thực hiện lại tokenizer research.

## 25. Trạng thái chuyển session và các quyết định không hỏi lại

### Phân công đã được user nhắc và xác nhận nhiều lần

Để tiết kiệm “Giới hạn sử dụng” của Reviewer, user muốn Reviewer tập trung
brainstorming, ý tưởng, phân tích evidence và viết plans/specs/guides rõ ràng.
Code, tests, đếm token/từ, thống kê, đọc nhiều source/phiên âm và khảo sát có thể
giao Implementer thì soạn prompt có context/scope/output, user copy chuyển tiếp.
Reviewer có quyền đọc/research/kiểm chọn lọc khi quyết định cần, không mặc định
rerun script hoặc kiểm toàn repo. Reviewer không tự spawn agent/gửi công cụ
nhắn vai trò khác. User là người chuyển prompt và chuyển báo cáo.

User đã nói “xác nhận, cho phép thực hiện bước tiếp theo” sau khi chọn B có
chọn lọc; Reviewer được quyết định các chi tiết thiết kế trong phạm vi và
chuẩn bị nhiệm vụ cho Implementer. Approval written spec rồi plan riêng vẫn
giữ. Không suy ra quyền triển khai runtime/paid API/Git từ câu xác nhận đó.

Latest user instruction: **xác nhận kết quả khảo sát**, cho phép cập nhật toàn
bộ trạng thái/quyết định/ngữ cảnh và sửa/xóa chỉ dẫn lỗi thời trong các Markdown
cần thiết. Sau đồng bộ, tiếp tục hoàn thiện written spec. Không cần xin lại
quyền ghi docs đã cấp; vẫn duyệt written spec rồi plan riêng trước implementation.

### Quyết định hiện hành

- Baseline A theo cấu trúc Markdown, không LLM chia. Giữ mục ngắn, list cha/con,
  bảng/đơn vị/đối tượng/điều kiện, text giữa các cấp heading và intro liên quan.
- Chung boundaries/evidence/nội dung nền cho E5-small, E5-base, HuyDang;
  preprocessing đúng từng model, kiểm từng tokenizer, không truncate âm thầm.
- Title + heading gốc thay nhãn Foods; không 400 ký tự, H2-only, count 572,
  schema 7 fields hoặc tỷ lệ overlap cố định cho full corpus.
- B sau baseline: **lựa chọn 1, bổ sung có chọn lọc trên nguyên bộ chunk A**.
  Chỉ thêm context sinh khi input hoàn chỉnh vừa cả ba tokenizer embedding.
  Nếu không vừa, giữ representation A; không cắt body/điều kiện, đổi model,
  boundaries hoặc tạo bộ chunk nhỏ hơn riêng cho B. Context lưu riêng, không
  phải evidence/citation/Golden. Ghi tỷ lệ bổ sung và chất lượng toàn tập.
- Chưa dùng vector riêng, synthetic questions/tags hay metadata search trong
  lượt B đầu. Phương án 2 (bộ chunk nhỏ riêng cho phép so A/B) không được chọn.
- C (LLM hỗ trợ boundaries) chỉ nếu A/B cho thấy cần; khác sinh context của B.
- Baseline Top-5 chunk chính theo input budget; context expansion sau Top-5 là
  thử nghiệm khác, chưa bật. Điều kiện có thể lặp ngay ingest nếu cần giữ nghĩa.
- Phạm vi sản phẩm/citation/ingest server-off/startup gate/partial answer/
  frontend/evaluation/roadmap tại mục 1, 12, 17 vẫn hiệu lực.

### Đề xuất Reviewer chưa phải full-corpus approval

Reviewer ưu tiên Gia Lạc P1 và Ngọ Môn P1 (mỗi mẫu 2 chunks); Ca Huế P3B lượt 3
gồm 4 chunks giá và 1 chunk dịch vụ có câu dẫn khảo sát. Mệ Kéo/module biển giữ
nguyên. Đây là các mẫu thiết kế đã trình, chưa phải output parser production.
Parser đã approved riêng theo mục 29; lựa chọn B và approval khảo sát không
đồng nghĩa approved tất cả schema/format/ID hoặc runtime.

Token packing đề xuất: nhóm nội dung đủ nghĩa trước → kiểm input đầy đủ từng
embedding model → chia tiếp theo ranh giới có nghĩa nếu vượt. Không cố làm
chunk bằng nhau hoặc target body 120–200; không ép dưới 250/235–240. Nhóm không
thể chia giữ nghĩa phải được nêu rõ khi preview, không âm thầm bỏ/truncate.
MiniLM/generator kiểm input riêng; chưa chốt mọi query policy hoặc LLM budget.

## 26. Khảo sát tokenizer bổ sung — số đo và locator cần giữ

### Provenance và giới hạn

Implementer thực hiện bằng project `uv`, Transformers 5.14.1, PyVi 0.1.1,
tokenizer snapshots local_files_only=True như mục 19 (đủ 4 revision IDs).
E5-small/base limit 512; HuyDang 256; MiniLM pair 512. Counts có preprocessing,
nhãn và special tokens; truncation=False. Không inference/Qdrant/API/weights.
Reviewer đọc report/JSON có mục tiêu, đọc source Ca Huế và một phần script;
**không rerun độc lập** khảo sát bổ sung. Đây không phải quality benchmark.

Artifacts canonical (không phụ thuộc /tmp):
- `reports/full_corpus_chunk_samples_tokenizer_survey_2026_09_09.md`
- `reports/artifacts/full_corpus_chunk_samples_2026_09_09.json`
- `reports/artifacts/full_corpus_chunk_samples_2026_09_09.py`

JSON lưu search_text nguyên vẹn, source_file, heading_path, queries,
evidence_parts với span/text/exact_match và counts từng mẫu. Role/shape trong
artifact khảo sát không phải runtime schema; không copy toàn bộ audit fields
vào Qdrant. Bảng dưới là số hiện có trong report/JSON, không phép đo mới của
Reviewer. Không dùng số lượng mẫu/chunks trong lời tóm tắt làm gate; artifacts
có cả phương án cũ, mới và diagnostic, không phải một bộ chunk để ingest.

Lệnh tái lập của Implementer (lưu để biết, **không tự chạy phiên sau**):
`uv run --no-sync python reports/artifacts/full_corpus_chunk_samples_2026_09_09.py`.
Script cập nhật JSON nên không phải lệnh read-only.

### Queries chuẩn hóa cuối cùng

Các phương án trong cùng tài liệu dùng cùng query_orig và query_long. Trước
correction có trường hợp đổi query theo chunk, làm pair counts không so được.

| Nhóm | query_orig | query_long |
|---|---|---|
| Gia Lạc | Hội xuân Gia Lạc tổ chức ở đâu và vào thời gian nào? | Lễ hội xuân Gia Lạc trong lịch sử và các kỳ phục dựng chuyên đề hiện nay được tổ chức vào thời gian nào, tại địa điểm nào? |
| Ngọ Môn | Ngọ Môn có cấu trúc và ý nghĩa lịch sử như thế nào? | Cửa Ngọ Môn Hoàng thành Huế được xây dựng vào năm nào, cấu trúc đài nền cùng lầu Ngũ Phụng có đặc điểm kiến trúc và ý nghĩa lịch sử ra sao? |
| Ca Huế | Vé Ca Huế cho trẻ em được tính như thế nào? | Giá vé xem Ca Huế ghép thuyền trên sông Hương cho người lớn và trẻ em bao nhiêu tiền một người, áp dụng điều kiện bao gồm và không bao gồm những dịch vụ gì? |
| Mệ Kéo | Quán bún bò Mệ Kéo mở cửa đến mấy giờ? | Quán bún bò Mệ Kéo nằm ở địa chỉ nào tại Huế, mở bán trong khung giờ nào và mức giá mỗi tô dao động khoảng bao nhiêu? |
| Module biển | Có thể thay ngày cuối bằng đi biển và đầm phá không? | Nếu muốn đổi lịch trình ngày thứ ba sang tham quan biển Thuận An hoặc phá Tam Giang thì cần lưu ý những điều kiện thời tiết nào? |

### Mẫu ưu tiên và diagnostic cuối — tokenizer lịch sử, có đính chính

**Đính chính sau khảo sát parser đã approved:** hai mẫu lead VN/QT trong bảng
này được tokenize trên ranh giới sai. Counts 298/298/230/420/462 và
260/260/203/376/418 vẫn là lịch sử của input cũ, không phải counts nguyên hàng.
Hai composites đúng trong JSON parser có search_text 931/866 ký tự và
`tokens.status=not_measured`. Hai mẫu P3A tương ứng cũng bị ảnh hưởng.


Ký tự là độ dài **search_text**, không phải body. E5 hai model đếm riêng và
trùng nhau trên các mẫu này. MiniLM là orig/long với queries phía trên.

| chunk_id | Ký tự search_text | E5-small/base | HuyDang | MiniLM orig/long |
|---|---:|---:|---:|---:|
| gia_lac_baseline_oversized | 1204 | 352/352 | 272 | 512/540 |
| gia_lac_p1_chunk_1 | 583 | 177/177 | 142 | 256/284 |
| gia_lac_p1_chunk_2 | 653 | 186/186 | 138 | 290/318 |
| ngo_mon_baseline_oversized | 1798 | 530/530 | 423 | 738/774 |
| ngo_mon_p1_chunk_1 | 921 | 273/273 | 223 | 393/429 |
| ngo_mon_p1_chunk_2 | 948 | 278/278 | 214 | 394/430 |
| ca_hue_baseline_table_only | 1244 | 444/444 | 339 | 574/616 |
| ca_hue_p3b_lead_chunk_1_merged | 1107 | 349/349 | 264 | 485/527 |
| ca_hue_p3b_lead_chunk_1a | 948 | 298/298 | 230 | 420/462 |
| ca_hue_p3b_lead_chunk_1b | 849 | 260/260 | 203 | 376/418 |
| ca_hue_p3b_lead_chunk_2 | 954 | 311/311 | 248 | 437/479 |
| ca_hue_p3b_lead_chunk_3 | 919 | 302/302 | 245 | 417/459 |
| ca_hue_p3b_lead_chunk_4_service | 615 | 168/168 | 125 | 274/316 |
| ca_hue_p3b_lead_chunk_4_service_with_lead | 799 | 221/221 | 165 | 343/385 |
| control_me_keo_info | 303 | 97/97 | 78 | 144/173 |
| control_sea_module | 698 | 204/204 | 160 | 305/334 |

Mẫu dự toán một ngày chỉ có số đo khối ban đầu ở mục 19; chưa đo phiên bản
giữ intro hạn mức kế hoạch. Không gọi mẫu cũ là chunk tự đủ nghĩa.

### Diễn tiến các phương án và vì sao không lấy kết luận cũ

- Gia Lạc P1 giữ thời gian lịch sử/phục dựng với nhãn cha ở chunk 1; nơi tổ
  chức và bản chất văn hóa ở chunk 2. P2 gồm 3 chunks HuyDang 155/51/85,
  có chunk ghép hai đoạn rời; không phải mọi chunk đều 51–85 như mô tả sai cũ.
- Ngọ Môn P1 giữ khởi dựng/đài nền và Lầu Ngũ Phụng/lịch sử thành hai nhóm.
  P2 tách thêm lịch sử (223/129/99 HuyDang), chưa có quality evidence tốt hơn.
  P1 chunk 1/P2 chunk 1 nay cùng MiniLM 393/429; số 386 cũ do query rút gọn.
- Ca Huế P1/P2 ban đầu tách giá và điều kiện. Kết luận “đây là cách duy nhất”
  bị Reviewer bác vì chưa thử nhóm hàng nhỏ giữ điều kiện liên quan.
- P3A giữ từng hàng + toàn bộ Bao gồm/Không bao gồm 475 ký tự (chưa câu dẫn
  2.3): VN 249 HuyDang/517 MiniLM long; QT 222/473; trẻ Lá Quê 267/534;
  trẻ Thuyền Rồng 264/514. Một số input vượt; không chứng minh mọi API bất khả thi.
- P3B lượt 2 giữ Không bao gồm 170 ký tự ở chunks giá, tách Bao gồm chi tiết;
  HuyDang người lớn gộp/trẻ Lá Quê/trẻ Thuyền Rồng là 224/208/205, MiniLM long
  458/410/390. Reviewer phát hiện **thiếu câu dẫn khảo sát tháng 09/2026**.
- P3B lượt 3 thêm nguyên văn câu dẫn. Khối VN+QT 264 HuyDang/527 MiniLM long
  vượt nên tách 1a/1b. Hai chunk trẻ em còn dư 8/11 HuyDang: hợp lệ với input
  đã đo, không bảo đảm representation/query mới luôn vừa.
- Implementer đề xuất dịch vụ không cần lead vì không có giá; Reviewer ưu
  tiên biến thể **with_lead**: không suy ra sức chứa/hành trình/quyền lợi của
  tour khảo sát là quy chuẩn chung mọi dịch vụ. Nhiễu retrieval chưa được đo.

### Spans và điều kiện nguồn

Source paths tương đối `knowledge-base-hue/` đã có ở mục 19. Chuỗi được decode
UTF-8, CRLF/CR → LF; `[start,end)` là Unicode code points, không bytes/UTF-16.

- Gia Lạc: `[40,590)` + gap LF `[590,591)` + `[591,1211)`.
- Ngọ Môn: `[10219,11068)` + gap LF `[11068,11069)` + `[11069,11945)`.
- Ca Huế: `travel/tickets/Vé biểu diễn nghệ thuật và trải nghiệm sông Hương.md`.

| Phần Ca Huế | Span | Ký tự |
|---|---|---:|
| Câu dẫn khảo sát H3 2.3 | [10409,10591) | 182 |
| Heading H4 A (metadata/label) | [10593,10641) | 48 |
| Dẫn tour ghép | [10643,10758) | 115 |
| Header bảng (khối đã chọn) | [10760,10900) | 140 |
| Hàng khách VN — đã sửa theo parser | [10901,11141) | 240 |
| Hàng khách QT — đã sửa theo parser | [11142,11317) | 175 |
| Trẻ em Lá Quê | [11318,11581) | 263 |
| Trẻ em Thuyền Rồng | [11582,11810) | 228 |
| Bao gồm | [11812,12116) | 304 |
| Không bao gồm | [12117,12287) | 170 |

Câu dẫn nguyên văn cần giữ:
“Dưới đây là mức giá khảo sát thực tế từ các đơn vị cung cấp dịch vụ tiêu biểu
(Thuyền Rồng Huế, Ca Huế Trên Sông Hương - Lá Quê Travel, Đại Việt Tourist) tại
thời điểm tháng 09/2026:” (line wraps ở đây chỉ để đọc; exact string trong JSON).

Không bao gồm nguyên văn: “- **Không bao gồm:** Phương tiện đưa đón tận nơi
(khách tự di chuyển đến Bến Tòa Khâm), ăn uống cá nhân trên thuyền, tiền tip
bồi dưỡng nghệ sĩ (không bắt buộc, tùy tâm).”

Các vùng trắng Ca Huế: `[10591,10593)`, `[10641,10643)`, `[10758,10760)`,
`[10900,10901)`, `[11141,11142)`, `[11317,11318)`, `[11581,11582)`,
`[11810,11812)`, `[12116,12117)`. Hạch toán vùng `[10409,12287)` đủ 1878 ký tự
gồm evidence + heading metadata + whitespace; **không phải** mọi ký tự đều
nằm trong evidence_parts. Exact match từng part khác coverage/semantic sufficiency.
Header/lead/exclusions được lặp ở nhiều chunks; không dùng text render ghép
như một substring liên tục. Điều kiện A không tự lan sang B thuê nguyên thuyền.

### Overhead và các số không dùng làm contract

Nhãn Ca Huế khảo sát dài 194 ký tự. Report cuối ghi label-only: E5 54,
HuyDang 42, MiniLM 79; MiniLM query_long 59, query_orig 17, pair special 3,
suy ra pair query+label 141/99. 141 **không phải riêng nhãn**. Đây là các số
Implementer báo; phép kiểm quyết định vẫn tokenize input hoàn chỉnh, không
lấy phép cộng riêng từng fragment làm invariant cho mọi tokenizer.

Con số câu dẫn 68 HuyDang/117 MiniLM trong report research trước không có
provenance đủ được Reviewer xác nhận, không dùng để suy ra budget. Full-input
counts bảng trên mới là evidence tham chiếu. Không lấy % trần, 250, 235–240,
120–200 token body hoặc 500–850 ký tự làm policy. Không gọi “PASS” là retrieval
PASS, “triệt tiêu truncation” hoặc “loại trừ hoàn toàn LLM nhầm nhà cung cấp”.

## 27. Reference/research: kết luận dùng được và giới hạn correction

User yêu cầu đọc lại llm_rag tiếng Việt/JSON và rag_old_0 tiếng Anh/Markdown,
kể cả phiên âm. Reviewer giao Implementer đọc nhiều source, tự research nguồn
chính thức và kiểm chọn lọc khi report có mâu thuẫn. Report hiện tại:
`reports/full_corpus_chunking_reference_research_2026_09_09.md` (correction).

Nguồn local giữ để truy lại khi cần:
- `guides/llm_rag_reference_for_hue_rag.md`
- `/home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md`
- `/home/minhhieu/llm_rag/tai_lieu/rag_system_pipeline_deep_dive.md`
- `/home/minhhieu/llm_rag/backend/ingestion/pipeline.py`
- `/home/minhhieu/llm_rag/backend/ingestion/chunking/`
- `/home/minhhieu/llm_rag/backend/ingestion/helpers/split_paragraphs.py`
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/implementation/`
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/pro_implementation/`
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc/day5.txt`

### Bài học có căn cứ dùng cho thiết kế

- llm_rag chia theo field/nhóm field JSON và gắn tên thực thể; tiếng Việt giống
  Huế nhưng JSON đã cung cấp ranh giới nghiệp vụ. Huế dùng cấu trúc Markdown
  và source positions; không bê helper 400 ký tự sang làm giới hạn mới.
- Basic dùng RecursiveCharacterTextSplitter 1000/200 ký tự và MiniLM embedding;
  chưa chứng minh đơn vị/kích thước này phù hợp tiếng Việt, bảng/điều kiện Huế.
- PRO ingest dùng `openai/gpt-4.1-nano`; schema headline/summary/original_text,
  ghép cả ba để embed `text-embedding-3-large`. `AVERAGE_CHUNK_SIZE=100` dùng
  len(text) gợi ý số chunk, không phải budget token; prompt overlap 25%/50 words.
  Reviewer đọc source xác nhận không có bước exact source-match trong flow này.
- PRO answer.py dùng `openai/gpt-5-nano` cho rewrite/rerank/answer, retrieval
  k=20 mỗi query gốc/rewritten, merge/dedup tối đa 40, FINAL_K=10. Không nhầm
  ingest model với reranker. Không tự áp model/settings này cho Huế.
- Report correction dẫn day5.txt bài 135, dòng 596–660: MRR khoảng .73→.79→.91
  (Pro .9116), answer accuracy 3.99→4.21→4.62. Đây là bản tổng hợp bài học;
  bước giữa đổi cả embedding và chunk size, bước sau đổi nhiều biến. Không
  ablation riêng chunking, không suy ra % đóng góp hay winner Huế. Reviewer
  chưa audit từng dòng phiên âm trong phiên này; attribution qua report.
- Không có output LLM trung gian đã được xác minh cho ví dụ PRO. Việc report
  nói Chroma binary không phải bằng chứng output không thể đọc; không cần mở
  database reference để hoàn thành task thiết kế này.

### Lỗi report đã phát hiện và xử lý

Bản đầu tự soạn “NMK Villa Hội An”, “Accidental Damage Cover” rồi gọi dữ liệu
thật; dựng sai đường dẫn/bảng Ca Huế nhưng gắn số 248; ghi MiniLM 425; ghi sai
helper/rerank model; suy đoán “hơn 80%” cải thiện; đổi nghĩa A/B/C; loại API và
khẳng định an toàn tuyệt đối. Reviewer yêu cầu correction, không dùng bản đầu.
Correction thay mẫu llm_rag bằng record 46 trong backend/data/processed/projects.json,
mẫu Basic bằng products/Carllm.md, dẫn Ca Huế đúng JSON khảo sát và counts
248/479, 245/459. Các ví dụ reference này là Implementer đối chiếu; Reviewer
không tự nhận fresh verification tất cả chúng.

Report sửa các lỗi chính nhưng không được approved toàn bộ. Những câu còn sót
như “bất kỳ context nào cũng vượt”, “C phải đổi hoàn toàn ingestion”, “A chỉ
kiểm HuyDang/MiniLM”, “code giống thì luôn cùng output”, “B phải thêm vector
store riêng”, “tối đa 479 mọi mẫu/query” không là contract. Phải xét đầy đủ
input/config/dependency; cả E5-small/base; cùng tokenizer cụ thể; phạm vi mẫu.
Hướng C có thể LLM chọn block IDs rồi code lấy lại nguồn để bảo vệ evidence.
Synthetic questions/tags không cải thiện vector search chỉ vì được lưu payload;
cần consumer thực, là nhánh khác chưa duyệt và không thuộc B đầu tiên.

### Research chính thức đã đọc lại bởi Reviewer

- https://www.anthropic.com/engineering/contextual-retrieval
  LLM sinh chunk-specific context cho chunk sẵn có trước embedding/BM25,
  khác LLM chọn boundaries và khác generic document summary. Các giảm failure
  35%/49%/67% là những cấu hình riêng trong nghiên cứu, không quality Huế;
  không quy 50–100 tokens thành HuyDang hoặc mặc định provider/model cho B.
- https://aclanthology.org/2025.findings-naacl.114/
  Reviewer đọc trang/abstract; chưa đọc trọn PDF. Kết quả không cải thiện nhất
  quán không đủ để loại mọi LLM boundary/context enrichment. Implementer report
  mô tả sentence-embedding distance nhưng chưa cung cấp đủ page/section và
  dataset/ngôn ngữ để Reviewer xác nhận toàn bộ phương pháp. Không lấy câu
  khuyến nghị “structural + hybrid” làm kết luận trực tiếp của paper.
- https://docling-project.github.io/docling/concepts/chunking/
  và https://docling-project.github.io/docling/_generated/examples/hybrid_chunking/
  Structure-first + tokenizer, contextualized text tính cả nhãn; ý tưởng này
  hữu ích, chưa chọn dependency, chưa chứng minh exact spans Markdown Huế.
- https://docs.langchain.com/oss/python/integrations/splitters/markdown_header_metadata_splitter
  Header metadata không tự bảo vệ offsets; default có bỏ headers/whitespace.
  Không bắt buộc phải dùng RecursiveCharacterTextSplitter làm bước sau.
- https://markdown-it-py.readthedocs.io/en/latest/api/markdown_it.token.html
  và https://markdown-it-py.readthedocs.io/en/latest/using.html
  Token.map là line range, có thể None, không direct character offsets. Đây
  là lý do giao khảo sát parser thay vì tự chọn chỉ từ tài liệu.

Research hiện đủ để giữ A baseline, B chọn lọc, C khi có lý do. Không mở lại
broad research hoặc đọc toàn reference “cho chắc” khi chưa có quyết định cần.

## 28. Schema/locator và condition mapping sau khảo sát approved

Đề xuất chi tiết hiện nằm tại mục “Schema/locator sau khảo sát parser approved” trong `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`.
Chưa được coi là approved runtime contract chỉ vì đã viết vào thư mục specs.

| Field đề xuất | Contract dự kiến |
|---|---|
| chunk_id | ID nội bộ deterministic với cùng inputs/config; không là locator, không hứa giữ ID sau edit/rechunk |
| source | POSIX path tương đối knowledge-base-hue/, cùng nguồn cho mọi part của một chunk |
| domain | Một trong năm domain đã chốt |
| subdomain | Nhánh con thực tế, có thể null, không tự tạo taxonomy |
| title | Nội dung H1 gốc làm nhãn |
| heading_path | Danh sách headings gốc theo thứ tự, không lặp H1; intro trước H2 là [] |
| evidence_parts | Danh sách {role, start, end, text}, role body/header/condition |
| search_text | Representation A với nhãn + phần nguồn; chưa E5 prefix/PyVi; B lưu context sinh riêng |

Normalization đề xuất: UTF-8 strict, CRLF/CR→LF một lần; Unicode code points
[start,end) zero-based end-exclusive. Không đổi dấu/Unicode normalize. Parser
chỉ tìm cấu trúc/vị trí, evidence slice source normalized, không dùng HTML
render/token.content đã bỏ Markdown. Không lấy source.find lần đầu toàn file
để định vị text trùng. Offset con phải neo vào vùng cha. Header/condition có
thể lặp qua nhiều chunks; thứ tự trình bày parts có thể khác source order.

Bỏ image-only line thì giữ các spans hai bên; không ghép rồi gọi contiguous.
Inline HTML như <br> giữ ở evidence; UI safe rendering chưa thiết kế. Heading
là nhãn không thay body evidence; nếu heading có thông tin cần làm bằng chứng
thì giữ dòng heading nguyên văn trong part thích hợp. Backend resolve evidence
text; frontend không dùng offsets Python trên JavaScript UTF-16.

Chunk ID formula, source freshness/startup manifest/cơ chế kiểm tra, Qdrant
payload round-trip và public citation chưa chốt. Không đề xuất version store,
graph, registry hay validator framework để phòng xa.

Điều kiện: parser nhận heading/list/table, không tự hiểu mọi lead áp dụng cho
mọi con. Ca Huế lead H3 2.3 liên quan bảng giá; Không bao gồm H4 A không tự
lan sang B; tên nhà cung cấp giữ cùng tiêu chuẩn trẻ em. Chi phí: intro hạn
mức kế hoạch liên quan bảng dự toán xa. Chỉ dẫn nhỏ ngoài corpus có thể liên
kết vùng điều kiện→vùng nội dung cùng file ngay ingest; format/chống nhầm
heading trùng/source thay đổi đã có probe trên mẫu; written spec còn cần chốt
format và failure behavior cho ingest thật. Chưa tự bỏ bảng chuẩn hóa
Hải Vân Quan vì heading quản lý; cần tách phần hữu ích trước quyết định lọc.

## 29. Khảo sát approved, ngữ cảnh review và bước hoàn thiện written spec

### User confirmation và trạng thái

User xác nhận sau verdict ready_for_user_confirmation của correction lượt 3:
“xác nhận ... Tôi xác nhận kết quả khảo sát ... tiếp tục hoàn thiện written spec”.
Reviewer ghi **approved** cho khảo sát; correction series completed. Approval
chỉ áp dụng khảo sát parser/locator, không phải runtime full-corpus hoặc mọi
chi tiết spec/plan. CURRENT_HANDOFF chuyển sang next_design cho Reviewer.

Canonical artifacts:
- `reports/full_corpus_parser_locator_survey_2026_09_09.md`
- `reports/artifacts/full_corpus_parser_locator_survey_2026_09_09.py`
- `reports/artifacts/full_corpus_parser_locator_samples_2026_09_09.json`
- `reports/full_corpus_parser_locator_codex_review_2026_09_09.md`, mục 9–10.
Prompt khảo sát gốc giữ làm contract lịch sử, đã completed:
`handoff_prompt/FULL_CORPUS_PARSER_LOCATOR_SURVEY_HANDOFF.md`.

### Những gì đã được chứng minh và chọn cho thiết kế

- Chọn markdown-it-py 4.2.0, `MarkdownIt().enable('table')`. Phiên bản đọc từ
  package runtime; không cần parser dự phòng. Package đang transitive thì ghi
  dependency trực tiếp vào plan sau, chưa sửa pyproject/lock.
- Token.map cung cấp ranges dòng; chuyển thành Unicode code-point spans trên
  source LF. Không dùng token.content/render làm evidence. Source normalize
  CRLF/CR → LF, không Unicode-normalize; UTF-8 strict, `[start,end)` zero-based.
- Sáu nguồn khảo sát: Gia Lạc, Đại Nội, vé biểu diễn sông Hương, Chi phí,
  Hải Vân Quan, Mệ Kéo. Có nested lists, text giữa H2/H3, table header + delimiter,
  từng row/HTML br, blockquote, ảnh và chia câu cục bộ.
- Evidence Implementer: hai lần parse mỗi file có type/tag/maps giống nhau;
  ba condition probes resolve duy nhất; 40 source-text parts bounds/slice PASS.
  Counts token ở probe là Markdown tokens, không phải embedding token counts.
- Rules trên mẫu: lead 09/2026 tới hai bảng A/B (4+2 rows); Không bao gồm chỉ
  A; Chi phí intro có 2 LF tới ba bảng dự toán, mỗi bảng có hàng tổng. Probe
  so full signature độc lập và full heading paths không H1, intro dùng [].
- Ranh giới A/B quan sát: hàng cuối A kết thúc 11810, heading B bắt đầu 12289,
  không giao spans. Rows B đúng `[12617,12968)` / `[12969,13386)`.
- Hai composites VN/QT dùng spans parser và flat `{role,start,end,text}` với
  condition/header/body; cả hai có lead + header + nguyên hàng + Không bao gồm.
  Source/title/heading_path/search_text riêng. Evidence có thể không liên tục.
- Hải Vân Quan: giữ cảnh báo riêng vé/combo/miễn giảm/thời hạn; section đầu có
  thông tin hữu ích. Nguồn ghi bắt đầu thu phí 02/06/2026, hết thí điểm 31/12/2028,
  Trung tâm BTDT Cố đô Huế trực tiếp quản lý/đón khách/thu phí. Tên quận Liên
  Chiểu chỉ là chú thích địa giới cũ. Đây là đối chiếu corpus, không xác minh
  chính sách hiện hành trên web. Chưa loại cả section đầu hoặc bảng chuẩn hóa.

### Correction history và bài học không được mất

Review đầu phát hiện F1 mẫu tokenizer VN lấn sang đầu hàng QT, QT mất nhãn;
F2 thiếu parse lại và gán PASS không đủ evidence; F3 signature Chi phí mất LF.
Reviewer nhận lỗi bỏ sót ranh giới ở phiên trước. Lượt 1 sửa nguyên hàng/LF/
parse lại nhưng còn composite offsets cứng/schema sai và chưa probe selectors;
đồng thời thêm factual Hải Vân Quan sai. Lượt 2 đóng composite/factual nhưng
probe còn so tiền tố, bỏ qua path intro và target ancestor. Lượt 3 sửa đủ các
phép so; Reviewer đóng findings, user approved. Chi tiết từng finding ở review,
không dùng lịch sử làm yêu cầu chạy lại.

Spans sai cũ VN `[10901,11158)`, QT `[11159,11317)` vẫn exact substring nhưng
không đúng hàng. Spans đúng VN `[10901,11141)` (240), QT `[11142,11317)` (175).
Counts cũ không chứng minh input đúng mới; giữ `not_measured`, không cộng/trừ
counts theo ký tự. Không sửa artifacts tokenizer lịch sử hoặc bác mọi số đo
không liên quan. Bài học: source-match, đúng boundary, coverage và đủ ngữ nghĩa
là các phép đánh giá khác nhau.

### Giới hạn evidence và complexity

Reviewer đọc code/report/JSON và dùng jq/sed/rg kiểm chọn lọc nguồn, signatures,
paths, schema và ranh giới. Không rerun parser/tokenizer/models/API/Qdrant/full
suite. Không tự nhận độc lập xác minh execution mọi 40 parts. git diff --check
chỉ kiểm tracked diff; artifacts untracked chưa có exact Git base riêng.

40/40 không bao probe records span-list hoặc coverage tĩnh, không chứng minh
coverage toàn corpus. Probe là khảo sát cục bộ, chưa production resolver:
boundary bool được xuất nhưng chưa chặn PASS khi false; lookup phụ heading B
còn theo tên. Các chi tiết đó không chặn khảo sát mẫu đã verified, nhưng không
copy cơ học sang runtime. Không mở thêm correction/validator framework chỉ để
production-harden script khảo sát. Ảnh là minh họa cục bộ, không bộ lọc tổng quát.

### Next action duy nhất và các điểm phải hoàn thiện

**Reviewer tiếp tục hoàn thiện written spec**, không chờ Implementer/user gửi
report hoặc duyệt lại khảo sát. Bắt đầu từ schema/locator/condition mapping và
packing/oversized groups; cập nhật bản thảo quyết định rồi tự review trước khi
trình written spec hoàn chỉnh cho user.

- Chốt format chỉ dẫn nhỏ ngoài corpus, resolve cùng-file ngay ingest; lookup
  theo path/type/signature, mismatch/0/>1 xử lý rõ. Không graph/rule engine.
- Chốt grouping/splitting đủ nghĩa, headers/conditions và policy nếu nhóm tối
  thiểu vẫn vượt input limits; không silent truncate/bỏ phần chính hoặc điều kiện.
- Cân nhắc giao đúng hai input VN/QT đã sửa để đo bổ sung nếu quyết định budget
  cần; chưa có task đo đang chạy, không tự chạy khảo sát toàn bộ lượt 3 lại.
- Chốt chunk_id khác locator, payload xuyên Qdrant/retrieval/context, full reindex
  và startup phát hiện thêm/sửa/xóa nguồn; chưa thêm version store/registry.
- Tiếp đến MiniLM query policy; generator full prompt budget/citation/API;
  B model/prompt/representation/budget; Golden chờ tài liệu khóa học; retrieval,
  scoring/evaluation/frontend. Không hỏi dồn hoặc bắt user tự chọn chi tiết code.
- Giữ A/B/Top-5/shared chunks và mọi scope đã chốt. Written spec được user duyệt
  rồi mới viết plan/Review Contract; plan được duyệt rồi mới handoff implementation.

### Files, workspace, authority

User cho phép cập nhật/xóa chỉ dẫn Markdown lỗi thời thuộc Reviewer ownership.
Đã đồng bộ context/prompt, review, handoff, Project_Status, spec/experiment notes,
guide Phase 2 và index theo trạng thái mới; lịch sử implementation reports giữ
nguyên. Worktree modified/untracked, HEAD trên; không reset/stage/commit/push.
Không sửa backend/tests/corpus/index/settings/dependencies, không đọc .env,
paid calls/downloads/inference/subagent. Approval khảo sát không mở các quyền đó.

## 30. Agenda chuẩn bị trước đây — lịch sử, trạng thái mới ở snapshot

User yêu cầu ghi trước để **thảo luận/thực hiện ở session tiếp theo**. Đây là
agenda và đề xuất của Reviewer, không phải approved spec, implementation plan
hoặc nhiệm vụ khảo sát mới. Không hỏi hết danh sách cùng một lượt.

### Điểm bắt đầu đề xuất

Bắt đầu bằng luồng `nguồn LF → blocks có vị trí → nhóm nội dung và điều kiện
→ kiểm input → chunks/evidence/search_text`. Trình một thiết kế ngắn dựa trên
các mẫu đã khảo sát, rồi giải quyết nhóm nội dung quá dài. Không nghiên cứu
lại parser hoặc yêu cầu user thiết kế helpers/schema từ đầu.

**Câu hỏi ưu tiên đầu tiên:** nếu một nhóm nội dung cùng điều kiện bắt buộc
vẫn vượt giới hạn sau khi đã chia theo cấu trúc hợp lý, có đồng ý để bước
preview báo rõ file/mục/vấn đề và chặn ingest cho tới khi xử lý ngoại lệ không?
Reviewer nghiêng về hướng này để giữ nguyên yêu cầu không mất nội dung/điều
kiện. Phải trình trade-off: cần xử lý thủ công vài ngoại lệ, đổi lại tránh
phục vụ corpus thiếu mà không biết. Chưa có bằng chứng rằng toàn corpus thực
sự gặp nhóm bất khả chia; không tự xây workflow ngoại lệ phức tạp trước.
Silent truncation/bỏ điều kiện không là phương án vì trái quyết định đã chốt.

### Ý tưởng kỹ thuật để Reviewer cụ thể hóa

| Vấn đề | Hướng đề xuất để viết spec | Phần cần xác định |
|---|---|---|
| Nhóm và chia nội dung | Giữ đoạn/list cha-con ngắn; chia đoạn dài theo câu trong source span; bảng chia hàng/nhóm hàng và lặp header/điều kiện | Khi nào giữ cả nhóm, khi nào chia tiếp; nhãn cha và điều kiện nào phải lặp |
| Điều kiện ở xa | Một danh sách chỉ dẫn cùng-file ngoài corpus, chọn condition/target bằng full heading path và signature | Format tối thiểu, scope A/B và ba bảng dự toán; dừng khi thiếu/trùng/mismatch |
| Evidence và text tìm kiếm | Evidence parts nguyên văn; search_text ghép nhãn + các parts, preprocessing model thực hiện sau | Thứ tự ghép, dấu phân cách, quy tắc heading làm evidence khi cần; không dùng search_text làm nguồn citation |
| Nguồn và lần ingest | Full reindex khi ingest server-off; lưu danh sách source cùng dấu vết nội dung để startup đối chiếu | Cách đối chiếu thêm/sửa/xóa đơn giản, tính trên bytes hay nguồn LF, nơi lưu; chưa cần version store |
| ID chunk | ID deterministic từ source và vị trí/thứ tự chunk trong bộ ingest; locator tách riêng | Công thức rõ, không hứa ID bền qua sửa nguồn/rechunk; liên hệ với Qdrant point ID |
| Ngân sách token | Kiểm input đầy đủ bằng từng tokenizer, không áp target body tùy ý | Hai input VN/QT cần đo lại nếu dùng làm ví dụ acceptance; MiniLM pair và generator có budget riêng |
| Citation | Backend cung cấp tên nguồn/mục và đúng evidence text; UI hiển thị nguồn dễ đọc | Public response schema, liên kết claim–source, xử lý citation không hợp lệ, render Markdown/HTML an toàn |

Đây là lựa chọn thiết kế để cân nhắc, không cam kết áp dụng mọi cơ chế trong
bảng. Dấu vết nội dung source nhằm bảo vệ startup contract đã được user chọn,
không phải mở lại checksum/evaluation package machinery đã bỏ ở Foods.

### Câu hỏi tiếp theo theo phụ thuộc

1. **Khi viết ingest contract:** source chỉ đổi CRLF↔LF có được xem là cùng
   bản nội dung không? Reviewer nghiêng về so nội dung sau normalize LF vì
   locator dùng bản đó; cần ghi rõ quyết định, không suy từ approval parser.
2. **Khi viết reranker contract:** với query hợp lệ nhưng cặp query/chunk quá
   dài, giới hạn query từ API hay bỏ rerank cho cả request và dùng ranking
   trước đó? Trình ảnh hưởng trải nghiệm và controlled benchmark trước chọn;
   không tự cắt evidence hoặc dùng fallback để che lỗi provider.
3. **Khi viết generation/frontend:** câu trả lời hoàn chỉnh một lần hay stream?
   Reviewer nghiêng về trả một lần cho MVP để đơn giản hóa citation validation,
   nhưng đây là quyết định chưa chốt; frontend vẫn bắt buộc trong cả hai hướng.
4. **Khi đến Golden/evaluation:** đề nghị user cung cấp tài liệu khóa học đã
   hứa để chốt ground truth/evidence/split/metrics. Không hỏi số câu/ngưỡng khi
   chưa có cơ sở, không coi Day5/reference cũ thay tài liệu còn thiếu.

Các câu hỏi chỉ đưa ra khi ảnh hưởng đến phần spec đang viết. Không hỏi lại
MVP một lượt, shared chunks, B chọn lọc, Top-5, parser hoặc việc nguồn thay đổi
phải ingest lại. Model/provider/budget của B và generator còn mở nhưng bàn sau
khi schema/context contract đủ rõ; không gọi API trong lúc ghi ý tưởng.

### Bằng chứng cần và cách tránh lặp công việc

- Dùng JSON parser làm mẫu schema/locator đúng. Nếu đo hai input VN/QT, giữ
  đúng search_text/queries/preprocessing để so; giao prompt nhỏ cho Implementer,
  không rerun toàn khảo sát và không dùng ký tự suy token counts.
- Trước quyết định bỏ nội dung quản lý Hải Vân Quan, đọc chọn lọc phần có thể
  mất answer content; không lọc cả mục theo từ khóa heading.
- Coverage toàn corpus, payload round-trip và startup source-change gate là
  acceptance tương lai cần đưa vào plan sau; chưa có fresh execution evidence.
- Ưu tiên draft đủ rõ cho Implementer theo data flow, không copy script khảo
  sát hoặc liệt kê hàng loạt tên hàm/class bắt buộc.

### Kết quả mong muốn của session tiếp theo

Hoàn thiện phần chunking/schema/locator/condition mapping và xác định rõ các
contracts liên quan còn thiếu. Tiếp tục viết spec theo phụ thuộc; chỉ trình
duyệt khi phạm vi spec đó đủ hoàn chỉnh, không gọi agenda này là spec đã xong.
Nếu cần chia spec thành các phần duyệt riêng, trình user phạm vi/phụ thuộc
trước; không tự thu hẹp MVP. Sau user duyệt written spec mới viết implementation
plan và Review Contract; sau duyệt plan mới giao triển khai.

## 31. Tiếp tục thiết kế: packing/schema/condition mapping

Reviewer đã đọc bootstrap, prompt tiếp tục, toàn bộ context, bản thảo spec,
experiment notes và review parser; áp dụng bốn skills theo workflow. Read-only
HEAD vẫn ea87d3ed52851f6b6ab5c47b138540ebc8ff8340, worktree có thay đổi sẵn.
Không audit repo, mở lại correction hoặc chạy parser/tokenizer/runtime.

Đã cụ thể hóa trong spec mục “Đề xuất cụ thể cho packing và condition mapping”:
nhóm theo nghĩa rồi kiểm input; list giữ cha/con, bảng giữ header/điều kiện/
quan hệ tổng; selectors cùng-file `{heading_path, block_type, exact_text}`
trong danh sách `{source, condition, targets}`; resolve duy nhất, lỗi khi thiếu/
trùng/mismatch; ghép representation A nhưng evidence vẫn là từng source slice.
Đây là thiết kế Reviewer đề xuất, chưa có user approval written spec hoặc
evidence execution cho format mới. Không chép counts cũ thành acceptance mới.

User đã chọn A: khi nhóm tối thiểu chưa thể chia đủ nghĩa và vừa cả ba
embedding models, preview báo rõ và chặn ingest trước embedding/ghi index để
xử lý ngoại lệ; không ingest thiếu các nhóm đó. Chưa chứng minh corpus có
nhóm bất khả chia; hai VN/QT đúng vẫn not_measured. Không mở task đo mới.

User hỏi schema/locator/evidence_parts/search_text là gì và có cần thiết không.
Reviewer giải thích bằng các vùng rời nhau của Ca Huế: giữ từng đoạn nguyên
văn và vị trí để citation không kéo nhầm hàng khác; search_text là bản ghép
cho tìm kiếm, có thể dựng từ metadata/parts, không mặc định phải lưu trùng.
Câu hỏi chưa phải approval mọi fields/storage. User nhắc nếu cần code chạy
xử lý ngoại lệ thì Reviewer tự soạn prompt giới hạn để user gửi Implementer.
Không phải quyền Reviewer chạy code hoặc implementation trước spec/plan gates.

Sau quyết định này tiếp tục các contracts theo mục 29; source freshness,
MiniLM query, citation/generation và Golden vẫn mở đúng phạm vi đã ghi. Mục
30 là agenda chưa duyệt, không tự coi mọi đề xuất thành requirement. Luồng
spec approval → plan/Review Contract → plan approval → Implementer giữ nguyên.

## 32. Phân công tiết kiệm giới hạn sử dụng và khảo sát hai input

User yêu cầu chủ động giao code, đọc thông số, tests, đo đạc và tóm tắt có ích
cho Implementer qua prompt user copy; Reviewer tập trung phân tích kết quả,
brainstorming, quyết định và specs/plans/guides. Đã ghi vào Session_Prompt và
hai role workflows; không thay doctrine trong coordination skill hoặc bỏ
spec/plan approval. Reviewer vẫn kiểm chọn lọc cần thiết cho review độc lập.

Nhiệm vụ bổ sung mới: đo đúng hai composites VN/QT đã sửa trong JSON parser;
contract `handoff_prompt/FULL_CORPUS_VN_QT_TOKEN_CHECK_HANDOFF.md`. Đo tokenizer
local với input/queries/preprocessing giữ nguyên, không inference/downloads,
không rerun parser survey hoặc sửa artifacts cũ. CURRENT_HANDOFF chuyển tới
Implementer cho exact task này. Chưa chạy, chưa có report/counts mới. Đây là
nhiệm vụ mới lấp evidence thiếu, không correction của khảo sát đã approved.

Reviewer tiếp tục thiết kế độc lập trong khi user chuyển prompt. User đã
chọn A: đổi CRLF↔LF đơn thuần được coi là cùng nội dung, không ingest lại;
Reviewer tự chọn cách xử lý xuống dòng phù hợp, không hỏi chi tiết nội bộ.
Spec ghi text LF dùng chung cho locator và đối chiếu nguồn. Đề xuất lưu
source paths + SHA-256 text LF cho startup; chưa triển khai/kiểm thực thi.
Không suy thành quyền xóa Markdown, gộp whitespace hoặc đổi nguyên văn. Schema/
locator vừa được giải thích, chưa tự coi mọi fields/storage được approved.

User chọn A: với câu hỏi hợp lệ nhưng cặp query/chunk vượt reranker input
limit, bỏ rerank cả request và giữ ranking trước rerank; ghi rõ trong
evaluation. Không truncate câu hỏi/evidence hoặc dùng chính sách này che lỗi
model/provider khác. User hỏi vì sao không luôn rerank và MiniLM là gì:
Reviewer làm rõ module reranking thuộc MVP, nhưng còn đường no-rerank để so
sánh, chưa có default winner full-corpus. MiniLM là candidate cross-encoder
local chấm cặp query/chunk, không phải generator. Không coi câu hỏi là user
đã hủy no-rerank baseline hoặc chọn MiniLM làm winner.

Tiếp thảo luận trải nghiệm trả đáp án hoàn chỉnh một lần hay streaming;
khuyến nghị một lần cho MVP để xử lý citation đơn giản, chưa có user chọn.
Handoff đo VN/QT giữ scope; kết quả và review tiếp theo ở mục 33.

## 33. Hai input VN/QT đạt kỹ thuật; user chọn trả đáp án một lần

User chọn A cho giao diện: trả câu trả lời hoàn chỉnh cùng nguồn, không
streaming. Đã ghi spec; citation/public API/groundedness còn hoàn thiện.

User chuyển report khảo sát hai input. Reviewer đã đọc toàn văn ba artifacts
mới, final_review handoff và contract; đối chiếu bằng jq hai search_text,
metadata/parts với parser và cả tám source slices LF: khớp. Script đúng
snapshots local, preprocessing, queries và no truncation. Counts do
Implementer đo, Reviewer kiểm code/artifacts, không rerun tokenizer:

| Mẫu | E5-small/base | HuyDang | MiniLM orig/long |
|---|---:|---:|---:|
| VN, 931 ký tự | 290/290 | 224 | 411/453 |
| QT, 866 ký tự | 268/268 | 208 | 385/427 |

Cả hai vừa limits của inputs/queries đã đo; không phải quality evidence hoặc
mọi query đều vừa. Counts cũ input sai vẫn không dùng. Parser JSON và artifacts
tokenizer lịch sử giữ nguyên; không sửa not_measured trong artifact cũ.

Phát hiện thiết kế Reviewer: mẫu parser dùng hai LF giữa lead/bảng/exclusions,
không phải nối mọi part bằng một LF như spec vừa đề xuất. Phép so một LF
false, ghép đúng nhóm true. Đã chỉnh spec theo cấu trúc paragraph/table như
input đã đo, không cần đo lại hoặc correction Implementer. Report tự gọi
“nghiệm thu 100%” không là approval; claim 45 từ/margin an toàn không dùng
làm contract. Không có blocker/major cần correction.

Review: `reports/full_corpus_vn_qt_token_check_codex_review_2026_09_09.md`;
user report cùng tên nhiệm vụ dưới reports/user_reports. Verdict
ready_for_user_confirmation; chưa approved. CURRENT_HANDOFF là closure cho
Reviewer chờ user xác nhận khảo sát theo contract trong review mục 6. User
không cần chạy lại. Độc lập với approval written spec/plan; phần thiết kế
được tiếp tục trong khi chờ. Không có task khảo sát mới hoặc quyền runtime.

## 34. Closure khảo sát VN/QT và tiếp tục citation/generation

User trả lời “xac nhận” cho kết quả khảo sát hai input. Reviewer đã đóng
approved/completed theo review mục 6; đồng bộ user report/status/spec/prompt/
experiment notes và chuyển CURRENT_HANDOFF về next_design. Mục 33 ghi trạng
thái trước xác nhận; nay không còn chờ approval hoặc task khảo sát đang chạy.
Không sửa artifacts Implementer hoặc chạy lại tokenizer/runtime.

Reviewer cụ thể hóa citation draft: answer + sources public, nhãn số trong
response, tên tài liệu/mục và excerpts gốc; backend lấy evidence thật thay
text do generator tự sinh, UI giữ phân biệt các đoạn nguồn rời. Chưa phải
approved written spec. User đã chọn A cho evidence trong context mâu thuẫn
cùng đối tượng/thời điểm/điều kiện: nêu các thông tin khác nhau với nguồn,
nói chưa xác định bên đúng và trả lời phần còn lại có căn cứ. Không
coi giá khác nhà cung cấp/thời điểm là mâu thuẫn; không tự chọn nguồn thắng.

Reviewer bổ sung draft ID/lưu trữ: chunk_id serialize cặp source/ordinal trong
file, Qdrant UUID5 namespace cố định; search_text lưu một lần cho retrieval,
payload giữ metadata/evidence parts. Đề xuất full reingest khi nguồn thay
đổi, không incremental/ID stability framework; lifecycle/collection target
và approval runtime còn mở. Đây là thiết kế Reviewer, chưa approved spec.

Bước chuẩn bị Golden cần đường dẫn tài liệu khóa học user đã hứa; hỏi input
này trước khi chốt schema/evidence/split/metrics. Khi user cung cấp, giao
Implementer đọc/tóm tắt có dẫn vị trí theo phân công; Reviewer phân tích và
thiết kế, không mặc định tự đọc toàn reference. Không tự chọn số câu/ngưỡng
hoặc coi Day5 đã đọc là thay thế tài liệu chưa được cung cấp.

## 35. User cung cấp tài liệu Golden/evaluation và giao đọc reference

User cung cấp:
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0`;
- `/home/minhhieu/llm_rag/tai_lieu/rag_old_0/phien_am_bai_hoc` (phiên âm lời giảng);
- `/home/minhhieu/llm_rag/tai_lieu/rag_old`.

Không còn chờ user gửi paths. Thư mục phiên âm là con rag_old_0, không tính
hai lần cùng file. Reviewer chưa đọc/quét lại ba roots trong lượt giao này.
Theo phân công, tạo contract
`handoff_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md` và chuyển
CURRENT_HANDOFF tới Implementer. Chỉ đọc/tổng hợp, không chạy code/model/test/
notebooks/API/mạng, không sửa reference hoặc tạo Golden. Output một report
`reports/full_corpus_golden_evaluation_reference_summary_2026_09_09.md`.

Yêu cầu đối chiếu lời giảng/code/kết quả lưu sẵn, dẫn exact path+dòng/cell;
đọc data flow thật của Golden/evaluator và inputs judge, keyword relevance,
controls/leakage/split, phân biệt các phiên bản. Những kết luận reference cũ
là điểm kiểm tra, không đáp án áp đặt. Báo rõ phần đã đọc/chưa đọc; không
claim audit toàn repo hoặc suy metric cải thiện là riêng chunking.

Chưa có report mới/kết quả review. Reviewer phân tích sau khi user chuyển
report; tiếp tục phần thiết kế độc lập, chưa chốt Golden schema/số câu/
threshold/split. Không hỏi lại paths user đã cung cấp. Spec/plan approvals
và trạng thái completed hai khảo sát trước giữ nguyên.

## 36. Đồng bộ tài liệu và chuyển bộ FULL_CORPUS sang handoff_prompt

User yêu cầu cập nhật mọi thông tin/quyết định/trạng thái quan trọng, sửa/xóa
chỉ dẫn lỗi thời và cho phép chuyển FULL_CORPUS Markdown sang handoff_prompt/.
Đã chuyển năm tài liệu; cập nhật pointers trong docs Reviewer, thêm README
và snapshot hiện hành, rút gọn prompt Reviewer để không chép lại toàn lịch sử.
Các file cũ ở session_prompt/ chỉ là link chuyển tiếp, giữ prompt/report đã
copy còn dùng được. Không sửa implementation reports/scripts/JSON lịch sử.

Đã sửa guide index/Phase 2 còn ghi VN/QT chưa đo, bỏ câu hỏi đã chốt khỏi prompt
Reviewer và bản schema đề xuất sơ khởi trùng trong spec. Lịch sử correction,
counts sai và giới hạn evidence vẫn giữ, được phân biệt khỏi trạng thái mới.
Governance/bootstrap/CURRENT_HANDOFF vẫn ở session_prompt/. Spec/plan/report
không đổi thư mục. Không đổi requirement, tạo task mới hoặc chạy khảo sát.

User sẽ gửi prompt đọc reference cho Implementer và chuyển phản hồi khi xong.
Chưa nhận report; task đọc/tóm tắt Golden/evaluation giữ nguyên authority và
outputs theo contract. Hai khảo sát trước completed, spec/plan chưa approved.
Next action thực thi duy nhất vẫn nằm trong CURRENT_HANDOFF; Reviewer chờ
user chuyển báo cáo để kiểm theo contract rồi tiếp tục thiết kế.

## 37. Review báo cáo reference Golden/evaluation — correction lượt 1

User chuyển report Implementer. Reviewer đọc report/handoff và kiểm chọn lọc
source/test.py/eval.py hai roots, bốn records, day4.ipynb saved cells và một
vùng day4.txt; không chạy code/model/API/test, không audit toàn reference.
Đã xác nhận schema keyword, metric substring, judge không nhận retrieved
context/citation; bốn records thật và saved retrieval cell 7 khớp báo cáo.

Review canonical: reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md.
Verdict changes_requested, một batch R1–R3:
- R1: k chỉ cắt nDCG, không truyền retrieval và không cắt MRR/coverage; IDCG
  chỉ dựa list đã retrieve; rag_old chỉ dùng child_chunks[0].
- R2: record 101 hỏi product nhưng đáp án là chức danh; 141 hỏi how many
  nhưng đáp án chỉ nói several/ví dụ. Không thể gọi mọi đáp án Golden đầy đủ.
- R3: phạm vi đọc/attribution quá mức, day5.txt L1333 không tồn tại; notebook
  day4 scores 4/3/4 khác điểm từ tài liệu tổng hợp; không chứng minh summary
  thực tế thổi phồng MRR hoặc seed đảm bảo deterministic. Ca khác nhà cung
  cấp/thời điểm không phải cùng phạm vi mâu thuẫn; Agentic/threshold cũ không
  thành requirement Huế. Review giữ exact source pointers/tiêu chí đóng.

Không sửa implementation report thay Implementer. CURRENT_HANDOFF chuyển
correction, chỉ report + handoff được sửa, không thay reference/Golden/runtime
hoặc mở lại hai khảo sát completed. User chỉ chuyển prompt; không cần duyệt
scope correction. Khi nhận bản sửa, Reviewer kiểm delta, không lặp mọi lần đọc.
Các phần đã kiểm đủ dùng định hướng Golden evidence-based và kiểm chất lượng
question–answer trước dùng làm chuẩn; chưa chốt số câu/10–15%/split/threshold.

## 38. Chuyển phiên sau correction 1 — chưa review bản sửa

User yêu cầu đồng bộ các Markdown cần thiết, sửa pointers sau migration sang
handoff_prompt và chuẩn bị prompt để phiên sau nhận báo cáo Implementer.
Khi đọc workspace, CURRENT_HANDOFF đã là target reviewer/final_review do
Implementer ghi hoàn tất correction 1. Reviewer chỉ ghi nhận trạng thái này,
không đọc/review bản report sửa hoặc xác nhận các findings đã đóng trong lượt
đồng bộ. Verdict bản đầu changes_requested vẫn là verdict Reviewer gần nhất.

Phiên sau đọc bootstrap, prompt Reviewer, snapshot này, spec/experiment notes,
contract reference và review R1–R3; nhận báo cáo user gửi và kiểm bản sửa có
mục tiêu. Reuse evidence đã xác minh nếu nguồn không đổi. Report untracked
có thể không có Git base riêng: không gọi diff rỗng là bằng chứng không đổi;
đọc những phần cần đối chiếu findings và các summary/kết luận liên quan.
Không review lại toàn repo/ba thư mục hoặc mở lại parser/VN-QT đã approved.

Nếu correction đạt: ghi verdict, evidence/giới hạn và trình user xác nhận
khảo sát theo workflow; không tự approve spec/plan. Nếu chưa đạt: gom findings
trong scope thành prompt correction. Tiếp tục thiết kế Golden dựa phần evidence
đủ tin cậy; ưu tiên đơn vị evidence và cách kiểm question–answer–evidence trước
khi chốt số câu, split hay threshold. Mỗi lượt chỉ hỏi một quyết định cần user.

Đã rà pointers FULL_CORPUS trong Markdown thuộc session_prompt/handoff_prompt/
docs/guides/reports. Canonical đang dùng trỏ handoff_prompt; các đường dẫn cũ
trong implementation reports/lịch sử có năm file chuyển tiếp còn hiệu lực.
Giữ các file chuyển tiếp và evidence lịch sử, không sửa report của Implementer
để đổi đường dẫn hoặc xóa dấu vết correction. Không đổi thư mục spec/plans/reports.

Không có quyết định sản phẩm mới ở lượt này. Phân công, giới hạn, approval
gates và các quyết định đã chốt trong snapshot giữ nguyên. HEAD ghi nhận
ea87d3ed52851f6b6ab5c47b138540ebc8ff8340; worktree có thay đổi sẵn, không Git
mutation/runtime/tests/model/API/.env/subagent. User gửi prompt Reviewer và
báo cáo Implementer ở session tiếp theo; không có task thực thi mới.

## 39. Re-review correction 1 và tiếp tục thiết kế Golden/evidence

Ngày 2026-09-10, Reviewer đọc toàn văn report sửa và CURRENT_HANDOFF, reuse
evidence R1–R3 đã xác minh vì reference inputs/code/data flow không đổi; chỉ
đọc lại vùng metric cần giải quyết wording, không chạy code/model/API/tests.
Review canonical mục 7–8 ghi verdict `changes_requested` và correction lượt 2.

Phần đã đạt: cutoff riêng MRR/Coverage/nDCG; `child_chunks[0]`; records 101/141;
pointer day5; saved notebook không phải current code; summary keyword chỉ là
rủi ro tiềm ẩn; seed không bảo đảm deterministic; phân biệt conflict scope;
Agentic và dashboard threshold không là requirement Huế.

Phần còn sửa: “ngoài corpus” phải là relevant evidence trong corpus nhưng
ngoài `retrieved_docs[:k]`; không khẳng định reference “thiếu hoàn toàn” các
case khi chỉ biết chưa có field/category/intentional labels; không gọi phạm vi
đọc là toàn diện hoặc gán tài liệu tổng hợp cho giảng viên; không quy hai saved
scores khác bối cảnh cho variability; exact judge rubric vẫn là đề xuất mở.

Thiết kế độc lập tiếp tục từ đơn vị Golden evidence. Ba hướng đang trình user:
source+heading như Foods V3; case-level exact source spans; hoặc claim-level
evidence groups dùng exact source spans. Reviewer khuyến nghị claim-level để
kiểm được tính đủ, citation support, partial answer và conflict mà không khóa
ground truth vào chunk IDs thay đổi theo chunking. Chưa ghi thành quyết định
spec cho tới khi user chọn. Số câu, quotas, split, metric thresholds và exact
judge rubric vẫn mở; mỗi lượt chỉ hỏi một quyết định.

## 40. User chọn Golden evidence C và chuyển correction 2 cho Implementer

User chọn C ngày 2026-09-10. Golden full-corpus vẫn dùng JSONL đơn giản tương
tự Foods V3 ở cấp dataset/case. Điểm mở rộng là mỗi expected claim có các
`evidence_groups` gồm exact source spans `{source, heading_path, start, end,
text}` trên source LF đã ingest. Chunk IDs được suy ra cho từng candidate khi
evaluation, không là canonical ground truth. Cách này phục vụ retrieval,
completeness, partial answer, conflict và citation support từ cùng annotation.

Quyết định C đã được ghi vào decision spec nhưng không approve toàn bộ written
spec/plan và không cấp quyền tạo Golden. Task thực thi hiện hành vẫn là
correction lượt 2 cho report reference theo CURRENT_HANDOFF; sau khi sửa,
Implementer phải trả Reviewer/final_review và không tự đóng findings.
Prompt chuyển session canonical:
`handoff_prompt/FULL_CORPUS_IMPLEMENTER_CORRECTION_2_PROMPT.md`.

## 41. Re-review correction 2 — R1–R3 đóng, phát hiện schema baseline sai

Reviewer kiểm correction lượt 2: R1–R3 đều đã sửa đạt. Khi trả lời câu hỏi mới
của user về việc giữ Golden giống Foods V3, Reviewer đối chiếu canonical design
và row thật, phát hiện report §7 ghi sai schema Foods V3 thành fields `domain`,
`query`, `relevant_sources`. Schema thật là `{case_id, question, keywords,
reference_answer, category, evidence}`, với evidence source → H2 headings.

Report cũng vẫn hỏi lại lựa chọn source+section hay spans dù user đã chọn C;
§4.2 và bảng §6 còn recommendation trước quyết định. Review mục 9–10 ghi R4
major mới và giải thích evidence mới/điểm bị bỏ sót. CURRENT_HANDOFF chuyển
correction lượt 3 hẹp, chỉ đồng bộ report; không mở lại R1–R3 hoặc tạo Golden.
Prompt chuyển session:
`handoff_prompt/FULL_CORPUS_IMPLEMENTER_CORRECTION_3_PROMPT.md`.

## 42. User chọn một Golden đích, authoring/review theo từng lĩnh vực

User xác nhận phương án A nhưng yêu cầu tránh nhầm lẫn bằng cách tạo và hoàn
thiện từng Golden theo lĩnh vực trước, sau đó mới gộp. Thiết kế ghi nhận:

- working partitions tách lĩnh vực để biên soạn và review claim/evidence;
- chỉ merge sau khi tất cả partitions đạt quality gate;
- một full-corpus JSONL là canonical input cho official evaluation;
- smoke subset copy deep-equal từ full file;
- partitions không trở thành các benchmark song song lâu dài và được retire
  khỏi đường chạy chính sau merge;
- Foods V3 giữ nguyên artifact approved; phần Foods mới copy/enrich 45 cases
  bằng evidence C, không sửa file V3 lịch sử.

User đã chọn **P7**: bảy working partitions `foods`, `heritages`, `festivals`,
`performing_arts`, `travel_places`, `travel_services` và `travel_tickets` trong
giai đoạn authoring/review. Việc tách ba nhánh travel không thay đổi taxonomy sản
phẩm năm domain. Paths, merge order, IDs, validation và cơ chế retire thuộc
written spec/plan sau; quyết định này không cấp quyền tạo Golden.

## 43. Correction lượt 3 và trạng thái khảo sát reference — 2026-09-10

Reviewer đã kiểm correction lượt 3 cho R4 và kết luận PASS. Báo cáo hiện mô tả
đúng sáu fields canonical của Foods V3, đồng bộ quyết định evidence C, và không
còn câu hỏi lựa chọn evidence đã được User chốt. R1–R4 đều đóng.

Technical verdict của khảo sát reference Golden/evaluation là
`ready_for_user_confirmation`. User đã xác nhận ngày 2026-09-10 nên khảo sát
được chuyển `approved/completed`. Xác nhận đó không approve written spec hoặc
implementation plan.

## 44. User đóng khảo sát reference — 2026-09-10

User trả lời “xac nhận” cho Approval Closure Contract. Reviewer đã cập nhật
review, user report, context, status và handoff theo cơ chế closure. Không cần
chạy lại kỹ thuật. Bước tiếp theo là chốt lần lượt các phần còn mở của thiết kế
Golden/evidence/evaluation; không hỏi lại evidence C, một file canonical đích,
P7 hoặc việc giữ nguyên Foods V3 lịch sử.

## 45. Đề xuất record schema đang chờ User chọn

Reviewer trình ba phương án cho một quyết định schema. Khuyến nghị S1 với chín
top-level fields `{case_id, partition, domain, category, case_type, question,
keywords, reference_answer, expected_claims}`. Mỗi claim là `{claim_id, text,
evidence_groups}`; groups ngoài là OR, refs trong một group là AND; mỗi ref dùng
locator C `{source, heading_path, start, end, text}`.

S1 không lặp case-level `evidence`; `partition` giữ provenance P7 còn `domain`
giữ taxonomy sản phẩm năm domain. S2 giữ cả legacy evidence và claims nên có hai
nguồn sự thật. S3 gom nhãn vào metadata nên linh hoạt hơn nhưng khó audit và
validate hơn. Chưa ghi S1 thành quyết định cho tới khi User chọn; exact
`case_type` semantics là quyết định tiếp theo.

User yêu cầu hoãn lựa chọn S1/S2/S3 cho tới khi có khảo sát sâu hơn. Vì vậy các
phương án trên chỉ là proposal lịch sử, không còn là câu hỏi active.

## 46. Giao khảo sát sâu schema reference cho Implementer — 2026-09-10

User cung cấp lại root `rag_old_0`, phiên âm, evaluation code và `tests.jsonl`,
đồng thời yêu cầu Implementer khám phá toàn bộ trước khi chọn schema. Reviewer
đã tạo canonical prompt:

`handoff_prompt/FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_DEEP_DIVE_PROMPT.md`.

Task mới truy nguyên cách Golden được tạo, field consumers, toàn data flow
evaluation và quá trình từ schema bốn field của reference đến Foods V3. Nó phải
lập field-necessity matrix và 2–4 candidates tối giản, nhưng không tự chốt
schema. Output duy nhất là
`reports/full_corpus_golden_schema_reference_deep_dive_2026_09_10.md`, sau đó
trả Reviewer/final_review.

Khảo sát reference trước vẫn approved/completed; task này là design research
mới, không correction và không mở lại R1–R4. Không chạy code/model/API/tests,
đọc `.env`, sửa corpus/Golden/runtime/index, Git write hoặc spawn subagent.

## 47. Reviewer bác self-review giả và giao correction schema — 2026-09-10

Implementer tạo đúng implementation report nhưng sau đó vượt contract: tự tạo
Codex review và user report, tự ghi Reviewer đã chạy Python/kiểm độc lập, đổi
CURRENT_HANDOFF sang User/closure và sửa Project Status. Reviewer không công
nhận các artifact/claim này, đã xóa user report sai vai trò và thay review giả
bằng review thật tại:

`reports/full_corpus_golden_schema_reference_deep_dive_codex_review_2026_09_10.md`.

Verdict thật là `changes_requested`: R1 blocker về attribution/review
independence; R2 major vì claim 96/96 full reading mâu thuẫn với việc chỉ đọc mẫu
76 Markdown và quét transcript; R3 major vì claim vượt evidence; R4 major vì
field matrix/candidates còn sai logic; R5 minor về JSONL/giọng văn.

Correction canonical:
`handoff_prompt/FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_CORRECTION_1_PROMPT.md`.
Implementer chỉ được sửa implementation report và CURRENT_HANDOFF, phải đọc nốt
toàn bộ text/source theo contract bằng lệnh đọc, không chạy Python/code/tests và
không tự tạo review/user report. Chưa có schema candidate hay khảo sát mới nào
được User approval.

## 48. Re-review correction 1 schema — còn R2 major — 2026-09-10

Reviewer đọc toàn bộ report correction 1. R1 và R5 đạt; phần lớn R3/R4 đã sửa
đúng. R2 vẫn chưa đạt vì Implementer chỉ full-text read 12 Markdown
company/products, còn 64 employees/contracts chỉ structural inspection nhưng
vẫn claim full coverage và omission zero.

Ba điểm hẹp khác cần đồng bộ: không gọi Foods V3 “bỏ quota định trước” khi
reference chỉ có observed distribution; không gọi sequential IDs độc lập với
file order; không gọi candidates đã hỗ trợ đầy đủ IR/negative/conflict trước khi
case-type representation/scoring được chốt.

Review §§6–7 giữ verdict `changes_requested`. Correction lượt 2 canonical:
`handoff_prompt/FULL_CORPUS_GOLDEN_SCHEMA_REFERENCE_CORRECTION_2_PROMPT.md`.
Task yêu cầu full-text read nốt 64 Markdown bằng lệnh đọc và chỉ sửa report +
CURRENT_HANDOFF. R1/R5 không mở lại; chưa trình schema cho User.

## 49. Chuỗi guide, spec và plan được chuẩn hóa — 2026-09-10

User yêu cầu đồng bộ toàn bộ trạng thái và hỏi spec/plan thuộc guide nào.
Reviewer tạo `guides/full_corpus_rag.md` làm guide umbrella ở trạng thái
`designing`, nối các thay đổi xuyên Phase 2–8. Các guide phase hiện có tiếp tục
mô tả Foods/runtime đã approved; đặc biệt guide Phase 2 không bị đổi thành
contract đa domain.

Chuỗi gate hiện hành: correction 2 schema phải qua independent review; Reviewer
và User chốt các quyết định Golden/evaluation rồi các quyết định kiến trúc còn
mở; Reviewer mới soạn written spec toàn corpus. Chỉ sau khi User duyệt spec mới
soạn implementation plan + Review Contract, và chỉ sau khi plan được duyệt mới
giao Implementer. Tên dự kiến:

```text
docs/superpowers/specs/2026-09-10-full-corpus-rag-design.md
docs/superpowers/plans/2026-09-10-full-corpus-rag-implementation-plan.md
```

Hai files ngày 2026-09-09 hiện có là decision/experiment notes, không phải các
artifact duyệt trên. Việc đồng bộ Markdown không cấp quyền code, tests, API,
Golden creation, index mutation hoặc Git write.

## 50. Re-review correction 2 schema — còn một nhãn ID — 2026-09-10

Reviewer đọc toàn bộ report và kiểm read-only inventory/line counts: đúng 32
employees/1.659 dòng và 32 contracts/3.654 dòng. R2 PASS. Quota/ID prose đúng;
candidate table đã hạ support thành structural capacity, nên R4 PASS.

Sơ đồ §6 vẫn ghi proposed Full Corpus `case_id (định danh bất biến)`, trái với
phần còn lại nói ID tuần tự theo file order và không bất biến qua insert/reorder.
R3 vì vậy còn PARTIAL major. Review §§8–9 giữ `changes_requested`; correction
lượt 3 chỉ thay nhãn thành `định danh tường minh`, quét mâu thuẫn tương tự và
đồng bộ self-review/handoff. Không mở lại R1/R2/R4/R5 hoặc đọc lại 64 Markdown.

## 51. Closure khảo sát sâu schema và tiếp tục thiết kế — 2026-09-10

Reviewer kiểm correction lượt 3: nhãn §6 đã đổi thành
`case_id (định danh tường minh)` và toàn report nhất quán với ID tuần tự theo
file order, không bất biến qua insert/reorder. Handoff đúng Reviewer/final_review,
không có tự approval hoặc fake attribution. R3 PASS; R1/R2/R4/R5 giữ PASS.

Technical verdict là `ready_for_user_confirmation`; User trả lời `xác nhận`
ngày 2026-09-10. Khảo sát sâu Golden schema được chuyển
`approved/completed`. Approval chỉ cho phép dùng report làm evidence thiết kế;
không chọn schema, không approve written spec/plan và không cấp quyền tạo Golden,
chạy evaluator hay sửa runtime/index.

CURRENT_HANDOFF chuyển sang Reviewer/next_design. Bước tiếp theo là chốt record
schema rồi lần lượt alternative evidence groups, locator/validation, quy mô/
phân bố, split, metrics/thresholds và judge rubric. Mỗi lượt chỉ hỏi một
quyết định chưa chốt; không hỏi lại evidence C, P7, một canonical file đích hoặc
việc giữ nguyên Foods V3.

## 52. User chọn schema canonical tinh giản — 2026-09-10

Sau khi Reviewer giải thích vai trò từng field và giới hạn của keyword matching,
User ban đầu đồng ý schema canonical có sáu field bắt buộc: `case_id`,
`question`, `keywords`, `reference_answer`, `case_type`, `expected_claims`.
`category` là optional và chỉ phục vụ thống kê dạng câu hỏi. Quyết định này
được tinh giản tiếp tại mục 53 sau khi User chất vấn consumer thật của
`case_type`.

`partition` chỉ dùng trong các file authoring/review P7 và được loại khỏi record
khi merge. Không lưu `domain`; không lưu `claim_id`, mà derive từ `case_id` và
claim ordinal. `keywords` được giữ làm lexical checklist/diagnostic nhưng không
làm retrieval ground truth hoặc thay exact evidence. `expected_claims` là nơi
giữ claim text cùng evidence groups theo quyết định C.

Các chi tiết evidence groups, locator/validation, số lượng/phân bố, split,
metrics/thresholds và judge rubric vẫn chưa chốt. Chưa tạo written spec hoặc
implementation plan.

## 53. User loại `case_type` để giữ schema tương xứng scope — 2026-09-10

User chỉ ra mục tiêu hiện tại là xây Golden rồi đo retrieval metrics như
Recall@K, MRR@K và nDCG@K; answer thiếu/sai tự nhận điểm thấp. Reviewer đánh giá
lại và đồng ý `case_type` không có consumer cần thiết trong scope này. Thêm
routing/rubric cho các trạng thái giả định lúc này là over-engineering.

Schema canonical được chốt lại với năm required fields: `case_id`, `question`,
`keywords`, `reference_answer`, `expected_claims`; `category` optional cho
thống kê. `partition` chỉ ở authoring, `case_type`/`domain` không lưu và
`claim_id` derive. `keywords` không thay retrieval ground truth;
`expected_claims.evidence_groups` vẫn cung cấp exact span ground truth theo
quyết định C.

User xác nhận loại `case_type`. Chỉ mở lại field này nếu scope tương lai thật sự
được duyệt có nhiều rubric answerability riêng. Quyết định tiếp theo là semantics
tối thiểu của alternative `evidence_groups`.

## 54. User yêu cầu khảo sát lại evaluation để reset complexity — 2026-09-10

User dừng thảo luận `evidence_groups` và yêu cầu Reviewer nạp lại workflow. Sau
đối chiếu, Reviewer xác nhận OR/AND alternative groups chỉ là đề xuất chưa được
duyệt và không được coi là requirement. Điểm kiến trúc thực sự cần kiểm lại là
liệu mục tiêu metric hiện tại có cần `evidence`/`expected_claims` hay chỉ cần
schema kiểu `tests.jsonl`.

User giao một khảo sát mới cho Implementer trên
`/home/minhhieu/llm_rag/tai_lieu/rag_old_0`: inventory toàn root; đọc đầy đủ
mọi first-party non-data source, toàn `evaluation/tests.jsonl`, ba vùng code,
ba evaluator/app, năm notebooks và năm transcript; không đọc nội dung
`knowledge-base/**/*.md`. Task phải truy nguyên MRR/nDCG/metric retrieval còn
lại và Accuracy/Completeness/Relevance, map từng field vào consumer thật và đề
xuất complexity reset nhỏ nhất.

Contract canonical:
`handoff_prompt/FULL_CORPUS_RAG_OLD_0_EVALUATION_SIMPLICITY_SURVEY_PROMPT.md`.
Output duy nhất là
`reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md` rồi
trả Reviewer/final_review. Chỉ đọc text; không chạy code/model/API/tests/notebook,
không sửa decisions/runtime/corpus/Golden/index, không Git write hoặc sub-agent.

## 55. Closure khảo sát simplicity evaluation `rag_old_0` — 2026-09-10

Implementer hoàn tất report qua hai correction. Reviewer kiểm độc lập inventory,
150 test records, source data flow, formulas/cutoffs/consumers, notebook saved
outputs, transcript benchmark attribution và canonical field decisions. User
xác nhận đóng khảo sát ở trạng thái `approved/completed`.

Kết luận được chấp nhận: `Retrieval Evaluation` là tên nhánh; ba retrieval
metrics là keyword-proxy MRR, nDCG@10 và Keyword Coverage. Answer metrics là
LLM-judge Accuracy, Completeness, Relevance. Sáu metric chỉ cần ba data fields
`question`, `keywords`, `reference_answer`; `category` optional cho breakdown;
`case_id` là metadata vận hành Hue. `expected_claims`/`evidence_groups` không
được sáu metric tiêu thụ, nhưng phục vụ declared-evidence retrieval coverage,
citation verification và claim-source groundedness nếu User giữ scope đó.

Report/reference không tự quyết định thay User. Technical review ghi một minor
anchor-line defect không đổi kết luận và không mở correction lượt 3. Không có
runtime/corpus/Golden/index mutation, code/test/notebook/model/API execution hay
Git write. Quyết định tiếp theo là giữ, tách riêng hay bỏ citation/groundedness
khỏi official Golden/evaluation trước khi tiếp tục guide → written spec → plan.

## 56. User chọn Golden/evaluation metric-only — 2026-09-10

User chọn phương án A sau complexity reset: loại `expected_claims`,
`evidence_groups` và source spans khỏi official Golden/evaluation. Schema
canonical hiện hành có năm required fields: `case_id`, `question`, `keywords`,
`reference_answer`, `category`. User yêu cầu giữ `category` để thống kê số lượng
các loại câu hỏi; field này không route evaluator hoặc đổi điểm case.

Quyết định Evidence C trước đây bị supersede đối với Golden. Không còn thiết kế
alternative groups, claim IDs, locator validation hoặc claim-level judge trong
scope evaluation hiện hành. `case_type`/`domain`/`claim_id` tiếp tục không lưu;
`partition` chỉ là P7 authoring metadata và bị strip khi merge.

Official evaluation dự kiến chỉ có keyword-proxy MRR, nDCG@10, Keyword Coverage
và LLM-judge Accuracy, Completeness, Relevance. Keyword proxy không được gọi là
exhaustive corpus relevance ground truth. Runtime citation UI/source mapping
không tự bị xóa bởi quyết định này, nhưng không có citation/groundedness score
trong phase hiện hành.

Chưa sửa runtime/corpus/Golden/index, chưa chạy code/test/model/API/notebook và
chưa approve written spec/plan. Quyết định tiếp theo là vocabulary `category`
dùng chung cho toàn corpus.

## 57. User chọn bảy category generic — 2026-09-10

User chọn phương án A: mỗi canonical Golden case có đúng một `category` thuộc
`direct_fact`, `temporal`, `comparative`, `numerical`, `relationship`,
`spanning`, `holistic`. Category chỉ phục vụ đếm số lượng và breakdown, không
route evaluator, không chọn rubric và không đổi điểm case.

Hai nhãn Foods V3 `food_knowledge` và `guide_planning` không thuộc vocabulary
full-corpus mới. Foods V3 vẫn giữ nguyên như artifact lịch sử; case tái sử dụng
trong Golden mới được gán một trong bảy nhãn generic. Chưa chốt tổng số case,
phân bố theo P7/category hoặc split. Không có quyền tạo/sửa Golden hay runtime từ
quyết định này.

## 58. User không đặt case quota trước curation — 2026-09-10

User chọn làm Golden riêng theo từng chủ đề/partition rồi mới merge và suy ra
tổng số. Không chốt chính xác 100/150/210 từ trước; khoảng planning target cho
file cuối là 150–200 câu.

Không có hard quota theo P7 hoặc category. Không padding câu yếu để đạt target
và không loại câu đạt chất lượng chỉ để ép tổng. Counts và distribution được
báo cáo sau khi từng partition qua content review. Tại mốc §58 split chưa chốt;
§59 ngay sau đó đã chốt không chia dev/test. Smoke tiếp tục là deep-equal subset
của canonical, không tự được coi là train/dev/test split.

## 59. User chọn một evaluation set, không chia dev/test — 2026-09-10

User chọn phương án A: toàn bộ Golden canonical là một evaluation set trong
scope hiện tại; không chia `dev`/`test`. Golden không được dùng để train hoặc
fine-tune model trong phase này, nên không thêm holdout management.

Smoke chỉ là subset chạy nhanh được copy deep-equal từ canonical, không phải
một split riêng. Chỉ xem lại holdout nếu một scope tương lai thực sự dùng
Golden để huấn luyện hoặc cần tách tập để chống tuning leakage. Quyết định tiếp
theo là cutoff `K` cho ba retrieval metrics.

## 60. User chọn retrieval cutoff K=10 — 2026-09-10

User chọn phương án A sau khi đối chiếu `rag_old_0`: official Retrieval
Evaluation báo cáo MRR@10, nDCG@10 và Keyword Coverage@10. Evaluator reference
import PRO path; PRO lấy candidate depth 20 cho mỗi query nhưng rerank và trả
top 10 cuối. MRR/Coverage chạy trên danh sách 10 kết quả đó; nDCG nhận `k=10`.

Cutoff metric không đồng nhất máy móc với candidate retrieval depth. Quyết định
không cấp quyền thay đổi runtime. Tiếp theo cần chốt aggregation giữa các case.

## 61. User chọn macro-average theo case — 2026-09-10

User chọn phương án A: tính từng metric cho từng câu hỏi rồi lấy trung bình
cộng; mỗi case có trọng số bằng nhau. Official report hiển thị overall
macro-average và cùng loại macro-average/count theo `category`.

Không dùng micro-average theo tổng keywords và không tạo weighted/composite
score mới. Cách xử lý case lỗi/không có kết quả chưa chốt; không được âm thầm
loại case làm mẫu số đẹp hơn. Sau lựa chọn này User yêu cầu đồng bộ toàn bộ
Markdown hiện hành và tạo prompt Reviewer cho phiên tiếp theo.

## 62. User chọn thang điểm Answer 1–5 — 2026-09-11

User chọn phương án A: Accuracy, Completeness và Relevance được chấm riêng bằng
số nguyên từ 1 đến 5 như `rag_old_0`. Không chuẩn hóa thành 0–1, không đổi thành
pass/fail và không tạo composite score từ ba metric.

Quyết định chỉ chốt miền điểm. Rubric cụ thể cho từng mức và judge prompt tối
thiểu là quyết định tiếp theo; error handling và thresholds vẫn để các lượt
riêng. Không có quyền chạy judge/evaluation hoặc sửa Golden/runtime từ lựa chọn
này.

## 63. User chọn rubric đủ năm mức — 2026-09-11

User chọn phương án A: Accuracy, Completeness và Relevance đều có mô tả riêng
cho từng mức 1–5. Mỗi case chỉ dùng một judge prompt gồm question, generated
answer và reference answer; output là ba số nguyên cùng một feedback ngắn.

Rubric chấm ba metric độc lập. Judge không dùng kiến thức ngoài prompt. Chi tiết
thêm mà reference không xác nhận cũng không phủ nhận không tự bị coi là sai
Accuracy; phần thừa/lệch trọng tâm ảnh hưởng Relevance. Không đưa retrieved
context, citation hay groundedness vào judge và không thêm multi-pass/voting.
Rubric cụ thể đã được đồng bộ vào guide và working decision notes.

Cách xử lý no-result, lỗi kỹ thuật/timeout và judge failure là quyết định kế
tiếp; thresholds vẫn chưa chốt. Không có quyền chạy evaluation hoặc sửa
Golden/runtime từ lựa chọn này.

## 64. User chọn complete-run gate cho official aggregate — 2026-09-11

User chọn phương án A: chỉ công bố overall/category macro-average chính thức
khi mọi canonical case có metric hợp lệ. Retrieval chạy thành công nhưng rỗng
nhận ba retrieval scores bằng 0; generation chạy thành công nhưng answer rỗng
nhận ba Answer scores bằng 1.

Technical error, timeout, generation failure, judge failure hoặc judge output
không hợp lệ làm run `incomplete`. Case/stage/error phải được ghi đúng và case
lỗi phải chạy lại thành công trước khi aggregate. Không loại case khỏi mẫu số,
không biến lỗi hạ tầng thành điểm chất lượng và không gọi trung bình phần đã
xong là official metric. Policy không tự yêu cầu resume/retry framework.

Thresholds là quyết định tiếp theo; chưa có quyền chạy evaluation hay sửa
Golden/runtime.

## 65. User chưa đặt metric thresholds — 2026-09-11

User chọn phương án A: full-corpus phase chưa dùng pass/fail thresholds hoặc
diagnostic color bands cho sáu metric trước khi có baseline trên corpus mới.
Report giữ exact values, counts và category breakdown để chẩn đoán/so sánh các
cấu hình trên cùng Golden.

Không kế thừa ngưỡng màu UI của `rag_old_0` thành requirement. Run completeness,
schema/data validity và controlled comparison vẫn là acceptance contracts riêng,
không phải metric thresholds. Nếu evidence benchmark sau này tạo nhu cầu đặt
gate, đó là quyết định mới.

Quyết định tiếp theo là nguyên tắc author `keywords`; chưa có quyền chạy
evaluation hoặc sửa Golden/runtime.

## 66. User chọn keywords quan trọng, chính xác theo `rag_old_0` — 2026-09-11

User chọn phương án A và nhấn mạnh bám sát bài học `rag_old_0`: keywords là các
từ/cụm từ quan trọng, chính xác làm substring proxy. Mỗi case dùng danh sách
không rỗng; mỗi keyword có dạng chữ nguyên văn trong corpus liên quan, được
reference answer hỗ trợ và giữ cách viết tiếng Việt canonical.

Ví dụ User đưa: case nói đến Bánh ép 1992 cần keyword thực thể như `Bánh ép`,
hoặc tên đường/địa chỉ chính xác khi đó là fact được hỏi/cần trả lời. Không thêm
từ chung, synonym phòng xa, cả câu hay duplicate. Vì metric mean theo keyword,
không tách/lặp một phrase để tăng trọng số. Không hard quota; reviewer đối chiếu
từng keyword với corpus và reference. Đây không phải exhaustive relevance.

Quyết định tiếp theo là convention `case_id`; chưa có quyền tạo/sửa Golden hoặc
chạy evaluation.

## 67. User bỏ `case_id` khỏi canonical — 2026-09-11

User chọn phương án A sau khi hỏi lại tính cần thiết của ID và đối chiếu
`rag_old_0`. Quyết định này supersede schema năm-field trước đó. Canonical Golden
nay có đúng bốn required fields: `question`, `keywords`, `reference_answer`,
`category`; không lưu `case_id` ở authoring hay sau merge.

Không có consumer hiện hành cần stable per-case key. Author/review dùng partition
và row position; evaluator derive zero-based `case_index` từ canonical row order
và có thể báo kèm question. Derived index không được ghi vào Golden và không hứa
ổn định qua phiên bản. Không tạo ID tạm hoặc mapping thay thế. Nếu có consumer
cross-version thật trong tương lai, đó là schema decision mới.

Quyết định tiếp theo là quy tắc chọn đúng một category; chưa có quyền tạo/sửa
Golden hoặc chạy evaluation.

## 68. User chọn category theo thao tác chính và manual case review — 2026-09-11

User chọn phương án A. Implementer gán một category sơ bộ dựa trên thao tác
chính thể hiện trong chính câu hỏi, không dựa keyword bề mặt/domain/source và
không multi-label. Bảy định nghĩa chung cùng phân biệt spanning/holistic đã được
ghi trong guide và working decisions. User và Reviewer đọc từng case rồi quyết
định giữ, sửa/cập nhật, reclassify hoặc xóa.

Implementer author các working JSONL P7 từ curated corpus và tài liệu được giao.
Implementer được web-search để học cách tạo câu hỏi/dữ liệu tự nhiên, có giọng
người, rõ ràng, dễ hiểu, không máy móc; web không được đưa fact ngoài corpus vào
Golden hoặc thành ground truth. Implementer tự review và thực hiện correction;
Reviewer không sửa Golden thay Implementer. Chỉ partition qua content review
mới được merge.

Quyết định tiếp theo là nhịp author/review từng P7; chưa có quyền giao
implementation hoặc tạo/sửa Golden.

## 69. User chọn đóng tuần tự từng P7 — 2026-09-11

User chọn phương án A. P7 đi theo thứ tự `foods`, `heritages`, `festivals`,
`performing_arts`, `travel_places`, `travel_services`, `travel_tickets`. Mỗi
partition phải qua Implementer author + self-review, User và Reviewer đọc mọi
case, Implementer correction, Reviewer recheck và User confirmation trước khi
bắt đầu partition kế tiếp.

Không author sẵn toàn batch, không hard quota/padding, không merge partition
chưa đạt và không thêm approval database/per-case state machine. Quyết định tiếp
theo là canonical paths cho final/smoke/working files; chưa có quyền tạo Golden
hoặc giao implementation.

## 70. User chọn per-domain evaluation folders rồi merge tập trung — 2026-09-11

User chọn giữ convention như Foods: mỗi nhánh corpus có thư mục `evaluation/`
riêng và một working Golden của nhánh đó. Exact working filename được Reviewer
chọn là `golden_full_corpus_authoring.jsonl` để không nhầm với canonical:

```text
knowledge-base-hue/foods/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/festivals/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/performing_arts/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/places/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/services/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/tickets/evaluation/golden_full_corpus_authoring.jsonl
```

Các partition vẫn được author/review/approve tuần tự. Sau khi cả P7 được chốt,
merge vào `knowledge-base-hue/evaluation/golden_full_corpus.jsonl`; smoke đích
là `knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl`. Foods V2/V3
giữ nguyên. Working files bị retire khỏi official evaluator path sau merge.

Docs-only session chưa tạo bất kỳ folder/JSONL nào. Smoke selection là quyết
định tiếp theo; chưa có quyền giao implementation.

## 71. User chọn smoke 10 case thủ công — 2026-09-11

User chọn phương án A: sau canonical merge, Implementer đề xuất đúng 10 rows;
mỗi P7 có ít nhất một case và ba vị trí còn lại ưu tiên phủ thêm category. User
và Reviewer đọc/duyệt danh sách.

Smoke records deep-equal và giữ thứ tự tương đối trong canonical, không có field
đánh dấu, không sửa độc lập và regenerate nếu canonical rows tương ứng đổi.
Không random seed/sampling framework. Smoke chỉ phục vụ bounded check, không là
dev/test split hoặc thay full official evaluation.

Quyết định tiếp theo là deterministic merge/retirement; chưa có quyền tạo file
hoặc giao implementation.

## 72. User chọn concat rồi deterministic shuffle và full evaluation — 2026-09-11

User chọn phương án A nhưng yêu cầu xáo sau khi merge. Contract cuối: đọc P7 đã
approved theo thứ tự chốt, giữ internal row order, validate/strip `partition`,
concat rồi shuffle toàn bộ rows với fixed seed công khai `42`. Cùng exact
inputs/order/seed phải cho byte-identical canonical JSONL. Không global sort,
round-robin, ID, manifest, checksum hoặc package state. Working files retire
khỏi official evaluator path.

User yêu cầu sau khi Golden đầy đủ được merge/xáo (planning target 150–200,
không hard quota), chạy full mọi canonical case cho cả MRR@10, nDCG@10, Keyword
Coverage@10, Accuracy, Completeness và Relevance. Smoke không thay full run;
complete-run/no-threshold contracts giữ nguyên. Exact provider/model/matrix và
execution authority vẫn chờ spec/plan approval.

Quyết định tiếp theo là collection strategy full-corpus; docs-only session chưa
chạy merge/evaluation hoặc tạo/sửa Golden.

## 73. User chọn isolated collections và yêu cầu survey toàn bộ `llm_rag` — 2026-09-11

User chọn phương án A và chấp nhận nhiều collection khi có consumer benchmark
thật. Baseline có ba isolated full-corpus collections cho E5-small, E5-base và
HuyDang; controlled representation A/B có thể đưa tổng full-corpus candidate
collections lên sáu nếu giữ đồng thời. Sparse named vector dùng cùng candidate
collection; BM25/TF-IDF ở ngoài Qdrant; reranker, fusion và scoring không cần
collection riêng. Hai Foods collections đã ghi nhận giữ read-only. Exact
schema/names/lifecycle chờ evidence survey.

User tạm chuyển next action sang một read-only Implementer survey toàn bộ project
`/home/minhhieu/llm_rag`, gồm backend/frontend và ba tài liệu được chỉ định.
Mục tiêu là tạo report canonical đủ chi tiết để các phiên sau không khảo sát lại
từ đầu, đặc biệt làm rõ API/config/core/chunking/embedding/ingestion/LLM/logs/
reranking/retrieval/scoring/vectorstore/frontend và số collection/index thực sự
cần khi tham khảo sang Hue. Tiến độ full-corpus design được bảo toàn tại snapshot
và các mục 62–73.

## 74. Initial survey `llm_rag` bị yêu cầu correction và handoff phiên mới — 2026-09-11

Implementer nộp report 743 dòng tại
`reports/llm_rag_full_project_reference_survey_2026_09_11.md`. Reviewer đọc đủ
và đối chiếu tập trung source/config/backend/frontend theo Review Contract, sau
đó kết luận `changes_requested` tại
`reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md`.

Phần đã xác nhận, correction không mở lại:

- active `llm_rag` code/config dùng một configured Qdrant collection, default
  `nmk_chatbot_collection`, với named dense+sparse trong cùng points;
- runtime chỉ query named dense vector; BM25 rescoring dense pool trong memory;
  CrossEncoder/fusion/scoring không cần collection;
- sparse stored vector không có query consumer; đây không phải true lexical
  candidate retrieval;
- Architecture Types 0 chunk, `news.part_index` rơi khỏi payload và ba module
  batch/dense legacy không có active caller là các phát hiện có source support;
- Hue vẫn giữ 3 isolated baseline/6 A-B collections. Isolation là quyết định
  benchmark/lifecycle của User, không phải giới hạn tuyệt đối của Qdrant.

Initial report chưa đủ làm canonical reference vì thiếu coverage inventory và
các bảng config/core/logs/frontend/adaptation bắt buộc; nhiều claim sai source
như batch size 32 thay vì 64, timeout 10 thay vì 30, sparse formula, chunking,
startup batch, rate limit và context behavior; historical runtime numbers bị
gọi như fresh observation. Review còn yêu cầu ghi các rủi ro không copy: BM25
chỉ rescoring dense pool, fusion hai score scale chưa normalize, sparse token
indices không persist ổn định, collection không verify/migrate existing schema,
random UUID/upsert không idempotent và E5 không dùng query/passage prefix.

User đã gửi
`handoff_prompt/LLM_RAG_FULL_PROJECT_REFERENCE_SURVEY_CORRECTION_1_PROMPT.md`
cho Implementer. `CURRENT_HANDOFF.md` phải giữ target Implementer cho tới khi
Implementer trả correction với `Target role: reviewer`/`final_review`. Điều kiện
này đã hoàn thành; trạng thái tiếp theo được ghi tại §76.

Reviewer phiên mới đọc prompt
`handoff_prompt/FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md`. Nếu correction đã
về, re-review đúng C1–C7, dùng lại các kết luận đã đóng và không khảo sát lại
toàn project. Nếu đạt, trình User xác nhận closure; chỉ sau closure mới tiếp tục
mỗi lượt một câu hỏi. Câu đầu dự kiến: baseline full-corpus candidate collection
dense-only + BM25 local, hay có sparse query consumer thật để lưu/query sparse.
Khuyến nghị hiện tại là dense-only cho baseline vì chưa có Qdrant sparse consumer;
đây chưa phải quyết định của User.

## 75. User chốt bootstrap phân tầng để tiết kiệm Reviewer usage — 2026-09-11

User xác nhận cách nạp context tối ưu phải giữ đầy đủ thông tin cần cho vai trò
nhưng không buộc Reviewer đọc lại mọi tài liệu/source/history. `Session_Prompt`,
`REVIEWER_WORKFLOW` và `IMPLEMENTER_WORKFLOW` đã được đồng bộ với ba mức:

- `full-read`: stable role rules, current handoff, active contract/spec/plan/
  correction và report đang review; nếu tool chỉ hiển thị một phần của chính
  file này thì đọc tiếp phần thiếu;
- `targeted-read`: current snapshot hoặc exact section/range được prompt nêu;
- `reference-only`: biết path và chỉ mở khi active evidence không đủ cho một
  finding/decision cụ thể.

Reviewer vẫn đọc trọn Implementer report đang review, nhưng independent check
chỉ đi vào exact diff/high-impact anchors/Review Contract; không khảo sát lại
toàn source mặc định. Implementer vẫn đọc trọn exact source/input thuộc approved
implementation hoặc survey scope, tự kiểm và lập evidence; tài nguyên rộng hơn
không cho phép mở rộng scope.

Prompt `FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md` đã được rút gọn theo chính
sách này: full-read active correction/review/report, targeted-read current
canonical sections, reference-only lịch sử và hai report `rag_old_0`. Câu chung
“đọc toàn bộ mọi canonical documents và tiếp tục tới EOF” không còn áp dụng.
Điều này không hạ correctness: file đã gắn `full-read` vẫn phải đọc đủ; tiết kiệm
đến từ việc không biến mọi linked artifact thành full-read.

## 76. Implementer trả correction `llm_rag`; chuyển sang Reviewer final review — 2026-09-11

Implementer đã cập nhật
`reports/llm_rag_full_project_reference_survey_2026_09_11.md`, tự báo mapping
C1–C7 và chuyển `session_prompt/CURRENT_HANDOFF.md` sang `Target role: reviewer`,
`Handoff kind: final_review`. Self-report chỉ là evidence index, chưa phải PASS.

Reviewer phiên mới dùng prompt phân tầng tại
`handoff_prompt/FULL_CORPUS_REVIEWER_NEXT_SESSION_PROMPT.md`, đọc đầy đủ active
correction/report/review contract và chỉ kiểm source/diff theo các high-impact
anchors C1–C7. Không khảo sát lại toàn project, không mở lại kết luận đã đạt và
không resume design trước khi re-review cùng User confirmation đóng survey.

## 77. Bốn lượt correction survey `llm_rag` và correction ceiling — 2026-09-11

Reviewer đã re-review lần lượt bốn correction của report
`reports/llm_rag_full_project_reference_survey_2026_09_11.md`. Các lượt sửa đã
đóng phần lớn findings về inventory, architecture flow, config/API, ingestion,
retrieval, frontend/tests và evidence tone. Tuy nhiên report mở rộng tới 885
dòng, lặp cùng claim ở summary/body/matrix/self-review/traceability nên mỗi lượt
sửa exact finding vẫn để sót hoặc tạo claim/anchor sai ở vị trí khác.

Correction lượt 4 sửa đúng pipeline call flow, `using="dense"`, coverage,
authentication boundary và reasoning wording nhưng còn RR11 Major:

- §6.2 nói bảy chunker dùng path cứng `data/processed/`, trong khi cả bảy đều
  đọc `settings["data"]["processed_dir"]`;
- anchor `load_dotenv` trỏ dòng 17 thay vì call ở dòng 13;
- validator chỉ kiểm range bắt đầu vượt EOF nên bỏ sót các range kết thúc vượt
  EOF.

Codex review §9 ghi evidence và root-cause audit. Theo Reviewer Workflow, sau
bốn verdict `changes_requested` không tạo Correction 5; tiếp tục vá report dài
không xử lý nguyên nhân complexity/lặp.

## 78. User xác nhận complexity reset và contract thay thế — 2026-09-11

User trả lời `xác nhận` với phương án complexity reset. Phạm vi xác nhận:

- report survey 885 dòng được đóng băng working/non-canonical, không sửa tiếp;
- tạo Verified Architecture Extraction ngắn, chỉ giữ decision-relevant claims;
- mỗi claim xuất hiện một lần với primary-source anchor; loại exhaustive
  inventory, full config matrix, 20-test catalogue, glossary, traceability và
  self-review completion claims;
- guide/decision notes là nguồn thiết kế canonical; extraction là evidence
  companion và vẫn cần Reviewer review + User confirmation riêng;
- đây là implementation mới, không phải Correction 5 và không cấp quyền
  runtime/API/model/Qdrant/Git.

Active contract:
`handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md`.
`CURRENT_HANDOFF.md` target Implementer/implementation cho tới khi hai artifact
extraction/report được tạo và handoff trở lại Reviewer/final_review.

## 79. Phân loại hai tài liệu `tai_lieu` của reference

User hỏi có cần bắt Implementer full-read:

```text
/home/minhhieu/llm_rag/tai_lieu/rag_agent_handoff_current_repo.md
/home/minhhieu/llm_rag/tai_lieu/rag_system_pipeline_deep_dive.md
```

Reviewer kiểm tra cấu trúc và các phần liên quan rồi quyết định **không** đưa
chúng vào full-read bootstrap:

- handoff là snapshot ngày 2026-08-08, phần lớn lặp architecture/source;
- deep-dive dài 3.024 dòng/143 KB, mô tả snapshot khoảng 2026-08-02, chứa
  inventory, historical 450/1.486/48,84, sơ đồ và diễn giải cũ;
- đọc toàn văn hai file sẽ tái tạo noise/duplication mà complexity reset đang
  loại. Primary source và canonical guide mới là evidence ưu tiên.

Cả hai là `reference-only`: chỉ targeted-read một đoạn để tìm source pointer khi
active evidence thiếu, sau đó xác minh bằng source code. Không dùng chúng làm
primary evidence hoặc nguồn trạng thái hiện hành.

## 80. Decision queue sau extraction và nguyên tắc simplicity

Sau khi extraction đạt technical review và User confirmation, Reviewer hỏi một
quyết định mỗi lượt theo thứ tự:

1. lexical baseline dùng dense candidates + BM25 local hay thêm Qdrant sparse
   với query consumer thật;
2. fresh-build/replacement lifecycle cho candidate collections;
3. payload/source-locator tối thiểu cho retrieval/citation/frontend;
4. candidate retrieval/fusion/reranker matrix, failure behavior và cách đề xuất
   winner;
5. representation B được đưa vào lượt đầu hay hoãn sau A baseline;
6. context/generator/API/citation/frontend schema, budgets và error behavior;
7. thresholds/cutover chỉ sau full-corpus baseline thật.

Khuyến nghị khởi đầu, chưa là User decision: dense + BM25 local cho baseline,
không lưu sparse nếu chưa có query consumer; build candidate vào target mới/rỗng;
không thêm alias/manifest/checksum/migration/cleanup automation trước consumer,
failure hoặc exact replacement need; hoãn B nếu A đủ trả lời benchmark đầu.

Không hỏi lại những gì đã chốt: A Markdown structural, B giữ nguyên A và có
chọn lọc, Top-5 primary chunks, reranker capability, one-shot non-streaming,
isolated/fresh-by-default collections không hard cap experiment, Foods read-only
và Golden metric-only/P7/smoke 10/seed 42/K=10/macro/no-threshold-before-baseline.

Sau mỗi câu trả lời, Reviewer cập nhật decision notes và guide trước khi hỏi câu
kế. Khi end-to-end contracts đủ mới soạn written spec; chỉ sau User duyệt spec
mới soạn plan + Review Contract; chỉ sau User duyệt plan mới giao runtime
implementation.

## 81. User xác nhận closure Verified Architecture Extraction — 2026-09-11

Sau initial review và hai correction, Reviewer đã kiểm độc lập artifact thay
thế: đúng 6 H2, 75 dòng/23.570 bytes, 71/71 file URLs/labels/ranges hợp lệ;
VAE-R1–VAE-R4 đều đóng về kỹ thuật. Correction 2 implementation report thực tế
có 85 dòng/7.294 bytes; sai lệch 86 dòng trong báo cáo miệng là minor không ảnh
hưởng acceptance.

User gửi đúng câu `Tôi xác nhận closure Verified Architecture Extraction.`.
Extraction từ đó là approved evidence companion cho full-corpus design. Survey
885 dòng vẫn frozen/working/non-canonical và không được dùng làm basis cho
Spec/Plan.

Closure không phê duyệt runtime, Written Spec, Implementation Plan, benchmark,
collection mutation, Git write hoặc lựa chọn còn mở. `CURRENT_HANDOFF.md` chuyển
sang Reviewer/next_design. Next action duy nhất khi đó là hỏi Decision Queue #1
— lexical baseline/sparse consumer; mỗi lượt chỉ hỏi một quyết định và phải cập
nhật guide/decision notes sau câu trả lời trước khi hỏi mục kế tiếp.

## 82. User chốt Decision Queue #1 — lexical baseline/sparse consumer

User xác nhận baseline A là comparison control: query dense candidates rồi
BM25 local rescoring, nên không gọi là true hybrid candidate retrieval. Đồng
thời benchmark có hybrid candidate với sparse query consumer thật: mỗi candidate
collection lưu cả dense và sparse vectors trên cùng points; hybrid query hai
nhánh độc lập rồi fusion.

Sparse storage vì vậy có consumer hiện hành, không phải dữ liệu dự phòng. Exact
sparse representation/vocabulary phải reproducible và coupled với indexed
points; exact fusion, reranker, failure behavior và runtime default vẫn chờ
Decision #4 cùng benchmark. Quyết định không cấp quyền ingest/index/runtime.

Guide và decision/experiment notes đã được đồng bộ. Decision Queue chuyển sang
#2 index lifecycle; sau khi User trả lời, Reviewer cập nhật các nguồn này trước
khi hỏi #3 payload/source locator.

## 83. User chốt Decision Queue #2 — index lifecycle

User chọn C với ưu tiên thử nghiệm: fresh-by-default vào target mới/rỗng, không
in-place reconcile. Giai đoạn experiment không đặt hard cap số collections;
mỗi collection mới phải gắn với một candidate/variant đã được duyệt, không nhân
theo component hoặc tạo dự phòng không có câu hỏi so sánh.

Exact replacement là lối phụ, chỉ sau verify exact target và approval riêng.
Sau benchmark, Reviewer đề xuất giữ khoảng 1–3 collections tốt nhất; con số này
là mục tiêu retention sau evidence, không phải quota/winner count chốt trước.
Mọi cleanup đều cần exact target/authority, không tự động và không đụng Foods.
Quyết định này không cấp quyền tạo, thay thế hoặc xóa collection hiện tại.

Guide và decision/experiment notes đã được đồng bộ. Decision Queue chuyển sang
#3 payload/source locator; sau khi User trả lời, Reviewer cập nhật các nguồn này
trước khi hỏi #4 retrieval/fusion/reranker matrix.

## 84. User chốt Decision Queue #3 — payload/source locator

User chọn A sau khi Reviewer đối chiếu cách lưu của `llm_rag` và loại metadata
per-point không có consumer. Mỗi Qdrant point vẫn có point ID và hai named
vectors `dense`/`sparse` ở các trường chuẩn của Qdrant; các giá trị này không bị
lặp trong payload.

Payload chỉ giữ `search_text`, `source`, `title`, `heading_path` và
`evidence_parts[{role,start,end,text}]`. `source` là path tương đối nội bộ;
locator dùng offsets Unicode `[start,end)` trên source LF đã ingest. Domain/
subdomain suy từ source; source fingerprint thuộc cấp file/index;
model/representation identity thuộc collection/build. Không lưu token counts,
timestamps, versions, scores hoặc metadata phòng xa trong từng point.

Public API không trả nguyên payload; exact response/source whitelist chờ
Decision #6. Quyết định #3 không cấp quyền ingest/index/runtime. Guide và
decision/experiment notes đã được đồng bộ; Decision Queue chuyển sang #4
retrieval/fusion/reranker matrix.

## 85. User chốt Decision Queue #4 — retrieval/fusion/reranker matrix

User chọn A: chỉ so sánh các phương pháp có mục đích rõ, dùng độ đo phù hợp và
đưa ra kết quả thực nghiệm. Với mỗi dense model, stage retrieval so baseline A
(dense pool + BM25 local, fusion RRF trong pool) với native hybrid
(dense/sparse retrieval độc lập, fusion RRF). RRF tránh cộng thô các thang điểm
khác nhau mà chưa calibration.

Chỉ retrieval finalists mới sang stage so một reranker với no-rerank control.
Stage retrieval báo MRR@10, nDCG@10, Keyword Coverage@10; end-to-end finalists
báo đủ sáu metrics hiện hành. Không full Cartesian matrix, composite score,
threshold hoặc winner/default trước evidence. Component failure làm run
incomplete, không silent fallback; pair quá dài giữ pre-rerank order theo
contract đã chốt.

Reviewer sẽ báo exact result theo từng cấu hình và chỉ đề xuất winner/default
sau benchmark để User duyệt. Quyết định không cấp execution authority. Guide và
decision/experiment notes đã đồng bộ; Decision Queue chuyển sang #5
representation B timing.

## 86. User chốt Decision Queue #5 — representation B timing

User chọn B: hoàn tất representation A và staged retrieval matrix để chọn
model/retrieval finalists trước; sau đó tạo representation B chỉ cho finalists,
giữ model, retrieval, fusion và reranker tương đương giữa A/B để đo riêng tác
động của generated context.

User chấp nhận chi phí API và index, đồng thời yêu cầu official evidence phải
từ API thật, fresh indexes thật và full-corpus runs thật. Mock/synthetic chỉ có
thể phục vụ technical tests, không thay kết quả chính thức. Generated context
vẫn không là citation evidence; chunk/evidence boundaries giữ nguyên A và chỉ
bổ sung khi full input vừa cả ba embedding tokenizers.

Chi phí được chấp nhận không phải execution authority: exact provider/model,
prompt, budget và failure contract phải vào Written Spec và approved Plan trước
khi chạy. Guide và decision/experiment notes đã đồng bộ; Decision Queue chuyển
sang #6a public response/citation/error contract.

## 87. User chốt Decision Queue #6a — public response/citation/error

User chọn A strict minimal. Response success one-shot chỉ có `answer` và
`sources`; answer dùng response-local citation `[1]`, `[2]`. Mỗi source chỉ có
`id`, `title`, `heading_path`, `excerpts`, và chỉ source được answer tham chiếu
mới được trả.

Retrieval/provider/generation hoặc citation-validation failure trả typed non-2xx
`{error:{code,message}}`; không partial success, silent fallback, warning schema
hoặc automatic repair/retry. Thiếu evidence không phải technical failure:
generator trả phần có căn cứ hoặc nêu thiếu thông tin. Exact HTTP statuses/codes
chờ Written Spec; public response không lộ machine path, chunk ID, hashes,
model IDs, offsets, vectors, scores, debug hoặc token usage.

Guide và decision/experiment notes đã được đồng bộ. Decision Queue chuyển sang
#6b context budget policy; provider/model và frontend được hỏi riêng sau đó.

## 88. User chốt Decision Queue #6b — context budget policy

User chọn A và giao Reviewer quyết định fixed/flexible. Contract là linh hoạt
theo approved generator profile nhưng cố định trong từng benchmark run:
`context_limit`, `reserved_output_tokens` và `safety_margin` được khóa, ghi exact
values trong report để kết quả reproducible.

Mỗi request trừ actual tokens của system prompt, query, format/citation overhead
rồi pack nguyên primary chunks theo final rank, tối đa 5. Khi chunk kế tiếp
không vừa thì dừng; không skip chunk hạng cao, truncate hoặc summarize evidence.
Chunk hạng đầu không vừa là typed configuration/input error. Chỉ khi đổi approved
model/profile mới đổi budget; không dùng character/token limit chung hoặc tự mở
đến provider maximum theo từng request.

Guide và decision/experiment notes đã đồng bộ. Decision Queue chuyển sang #6c
generator/provider model; frontend được hỏi riêng sau đó.

## 89. User chốt Decision Queue #6c — generator/provider và judge

User chọn A: `qwen/qwen3.5-9b` qua OpenRouter dùng cho cả offline
representation B và online answer generation. Mỗi benchmark run pin một upstream
provider, khóa settings và không automatic routing/silent failover. Exact
upstream được recheck availability trước execution rồi ghi trong approved plan
và report; quyết định này chưa cấp quyền gọi API.

User giữ `gpt-5.4-mini` qua OpenAI API làm LLM judge cho Accuracy, Completeness
và Relevance. Judge độc lập với candidate generator, không tạo representation B
hoặc answer được chấm.

Representation B được giải thích lại: giữ chunk A và evidence gốc, chỉ bổ sung
có chọn lọc context tìm kiếm do Qwen sinh ở preprocessing vào `search_text` khi
toàn input vẫn vừa ba embedding tokenizers. Phần sinh thêm không phải evidence,
citation/Golden hoặc vector type mới; chunk không vừa giữ A nguyên vẹn.

Guide và decision/experiment notes đã đồng bộ. Decision Queue chuyển sang #6d
exact generator settings/numeric budgets; UI được hỏi riêng sau đó.

## 90. User chốt Decision Queue #6d — exact generator settings/budgets

User chọn A balanced/reproducible. Qwen profile dùng `temperature=0`, không set
sampling knobs khác; representation B `max_output_tokens=256`; answer generation
dùng `context_limit=16384`, `reserved_output_tokens=2048`, `safety_margin=512`
và timeout 90 giây. Không automatic retry/failover. Exact upstream provider
được preflight, pin và ghi lại trước approved benchmark run.

Budget 256 chỉ dành cho context tìm kiếm cô đọng của representation B, không
phải answer. Answer reserve 2048 cho phép trả nội dung dài hơn như lịch trình
nhiều ngày nhưng vẫn theo Top-5/evidence contract.

User yêu cầu ghi rõ trong plans/specs: Agentic RAG phải có profile và contract
riêng cho tool schemas/results, plan/state, số bước/tool calls, timeout/failure,
tổng token/thời gian/chi phí và provenance. Không dùng hoặc suy rộng ngân sách
one-shot RAG hiện tại cho agentic workflow.

Guide, decision spec và experiment notes đã đồng bộ. Decision Queue chuyển sang
#6e UI interaction cho one-shot response/citations.

## 91. User chốt Decision Queue #6e — UI interaction

User chọn A inline tối giản. UI có một ô câu hỏi và nút gửi; request đang xử lý
hiển thị loading và chặn submit trùng. Answer render Markdown an toàn. Citation
`[n]` hỗ trợ click/keyboard, cuộn và focus source card cùng ID ngay dưới answer.
Card chỉ hiển thị title, heading path và từng excerpt tách biệt. Typed error cho
manual retry, không automatic retry.

MVP không có streaming, chat history/session, raw payload, debug/score/token UI
hoặc agentic tool/plan UI. Agentic RAG vẫn là profile/contract riêng.

Guide, decision spec và experiment notes đã đồng bộ. Decision Queue tiền-spec
đã hoàn tất; metric thresholds/cutover tiếp tục bị defer đến sau full-corpus
baseline thật. Bước kế tiếp là Reviewer soạn Written Spec toàn corpus để User
duyệt; chưa soạn Implementation Plan và chưa giao Implementer.

## 92. Reviewer soạn Full-corpus RAG Written Spec

Reviewer hợp nhất các quyết định đã chốt thành
`docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md`. Spec ở trạng
thái `proposed — awaiting User approval`, mô tả behavior/data contracts từ
discovery, chunk/locator, representation, index/retrieval/reranker, generation,
API/citation/UI đến Golden/evaluation và experiment gates.

Spec giữ metric thresholds/cutover là post-baseline decision; Agentic RAG có
profile/contract riêng và không dùng one-shot budget. Spec không chứa quyền
runtime/API/Qdrant/benchmark, không phải Implementation Plan và không giao
Implementer. Next action duy nhất là User duyệt hoặc yêu cầu correction cho
Written Spec.

## 93. User duyệt Full-corpus RAG Written Spec

User xác nhận nguyên văn approval ngày 2026-09-11 và cho phép Reviewer soạn
Implementation Plan + Review Contract. Spec chuyển sang `approved by User`.
Approval không cấp quyền implementation/runtime, không giao Implementer và không
cho phép gọi API/model, ghi Qdrant hay chạy benchmark.

Next action duy nhất là Reviewer soạn Plan + Review Contract, trình User duyệt ở
gate riêng; chỉ sau Plan approval mới chuyển handoff sang Implementer.

## 94. Reviewer soạn Implementation Plan + Review Contract

Reviewer tạo hai artifact proposed:

- `docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md`;
- `handoff_prompt/FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md`.

Plan chia implementation thành Wave 1 parser/locator, Wave 2 index/retrieval,
Wave 3 generation/API/UI, Wave 4 Golden P7 tuần tự, Wave 5 evaluator/live
benchmark và Wave 6 documentation/final handoff. Mỗi wave dừng để Reviewer
review; live Qdrant/API/paid stages cần exact preflight và User confirmation.

Review Contract giữ independent source review, severity/verdict, P7 full-row
review và cấm Reviewer tự chạy runtime/tests theo authority hiện hành. Plan
approval chỉ cho phép giao duy nhất Wave 1; không cấp quyền live, cleanup,
cutover hoặc Agentic RAG.

## 95. User duyệt Plan + Review Contract và kích hoạt Wave 1

User xác nhận nguyên văn approval ngày 2026-09-11. Plan và Review Contract
chuyển sang `approved`; Reviewer tạo
`handoff_prompt/FULL_CORPUS_RAG_WAVE_1_IMPLEMENTATION_PROMPT.md` và chuyển
`CURRENT_HANDOFF.md` sang Implementer/implementation.

Active scope chỉ gồm discovery, parser/chunker, condition attachment, source
locator, representation-A preview, technical tests và artifacts Wave 1. Không
có quyền model/API/embedding inference/Qdrant/frontend/notebook/benchmark,
Git write, Wave 2 hoặc live gate.

## 96. User chốt workflow tuần tự theo wave và detailed guide

User yêu cầu không dùng Plan umbrella để giao liên tục nhiều wave. Sau mỗi wave,
Implementer báo cáo; Reviewer review/correction, trình User closure và cập nhật
detailed phase guide bằng observed evidence. Chỉ sau đó Reviewer mới dùng kết
quả dependency để brainstorming, soạn guide target + exact wave spec/addendum +
implementation plan + Review Contract và xin User duyệt trước handoff kế tiếp.

Thứ tự là Phase 2/Wave 1 → Phase 3/Wave 2.1 → Phase 4/Wave 2.2 → Phase 5/Wave
2.3 → Phase 6/Wave 3 → Phase 7 Golden/Wave 4 → Phase 7 evaluator/Wave 5A →
Phase 8 benchmark/Wave 5B → Wave 6 integrated closure. Live Qdrant/API/paid,
từng P7, finalist, winner/cutover/cleanup vẫn có exact gate riêng. Không author
ahead chi tiết phụ thuộc và không chờ Wave 6 mới cập nhật guide đã hoàn tất.
