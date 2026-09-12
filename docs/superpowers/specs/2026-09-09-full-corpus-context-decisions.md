# Full-corpus RAG — quyết định về context và phạm vi MVP

Trạng thái: bản ghi quyết định brainstorming theo yêu cầu trực tiếp của user;
chưa phải written spec hoàn chỉnh được duyệt. Không cấp quyền implementation.

> Khảo sát parser đã user-approved sau correction lượt 3; xem
> [review mục 9–10](../../../reports/full_corpus_parser_locator_codex_review_2026_09_09.md).
> Chọn markdown-it-py cho thiết kế tiếp theo. Hai composites VN/QT đúng spans
> [10901,11141) / [11142,11317) đã đo bổ sung: VN 290/290/224, QT 268/268/208
> cho E5-small/base/HuyDang; MiniLM orig/long 411/453 và 385/427. Reviewer đã
> kiểm code/artifacts, không rerun; user đã approved/completed khảo sát mới.
> Counts input sai vẫn không dùng. Written spec toàn corpus chưa được soạn để
> duyệt; bản ghi này chỉ là đầu vào cho spec đó.

Guide umbrella hiện hành là `guides/full_corpus_rag.md`. Các khảo sát Golden/
evaluation reference, schema deep-dive và simplicity evaluation `rag_old_0` đều
đã qua correction, independent Reviewer review và User xác nhận
`approved/completed`. User đã chọn schema metric-only; written spec và
implementation plan toàn corpus vẫn chưa được soạn/duyệt.

## Quyết định hiện hành

### Xác nhận mới: nhánh B bổ sung context có chọn lọc

User chọn **lựa chọn 1** sau khảo sát mẫu và đối chiếu reference: giữ nguyên
bộ chunk A; chỉ bổ sung context tìm kiếm do API sinh khi toàn bộ input mới
vừa giới hạn của cả E5-small, E5-base và HuyDang, với preprocessing đúng từng
model. Chunk không vừa giữ representation A; không cắt body/điều kiện, đổi
boundaries hoặc đổi model để nhường chỗ. Không đặt số token sinh cố định từ
ví dụ tiếng Anh hoặc coi mọi chunk đều phải được bổ sung.

Context sinh lưu riêng, không phải evidence/citation/Golden. Đây là thử nghiệm
sau baseline, khác lấy thêm điều kiện gốc sau Top-5. Chưa chọn provider/model,
prompt, ngân sách API hoặc representation cho reranker/generator; các bước đó
phải kiểm input riêng. Chưa thêm vector riêng, metadata câu hỏi giả định hoặc
consumer tìm kiếm mới trong lượt thử B đầu tiên.

Kết quả cần ghi tỷ lệ chunk thực sự được bổ sung và đánh giá toàn bộ tập câu
hỏi; không chỉ chọn các ca có lợi. Đây là phép đo tác dụng của bổ sung có chọn
lọc, không phải bằng chứng mọi chunk đều hưởng lợi từ context sinh.

Xác nhận này không thay approval của written spec/implementation plan và
không cấp quyền gọi API hoặc triển khai runtime.

### Phạm vi baseline đã xác nhận

- Ingest toàn bộ curated answer-facing corpus của năm domain vào Qdrant;
  loại source dumps, meta/research, inventory và Golden evaluation khỏi corpus
  trả lời. Chi tiết lọc nội dung quản lý lẫn trong answer documents còn cần thiết kế.
- MVP ban đầu gồm embedding, ingestion, retrieval, scoring, reranking và
  generator; giữ no-rerank baseline để so sánh. Frontend, citation và evaluation
  vẫn thuộc nghiệm thu MVP như đã xác nhận trước.
- Context baseline lấy các chunk chính được chọn sau scoring/optional reranking,
  tối đa 5 chunk theo xác nhận trong phiên này, chịu ngân sách input tổng.
  Chưa chốt số token; không kế thừa mặc định giới hạn 3.000 ký tự của Foods.
- Baseline chưa tự lấy thêm các đoạn điều kiện liên kết sau khi chọn Top-5.
  Khi chia chunk, vẫn giữ điều kiện cần thiết cùng nội dung khi phù hợp, bảo toàn
  nguyên văn và ngữ nghĩa. Thiếu bằng chứng thì trả lời phần có căn cứ hoặc nêu
  thiếu thông tin; việc hoãn mở rộng context không hủy yêu cầu trả lời có bằng chứng.
- Citation hiển thị đúng đoạn nguyên văn của bản đã ingest. User tắt server khi
  ingest. Khi khởi động backend, nếu có file thuộc corpus thêm/sửa/xóa so với bản
  đã ingest thì báo yêu cầu ingest lại và chưa phục vụ chatbot. Cơ chế kiểm tra
  và locator/schema chưa chốt.
- Qwen3.5 9B qua OpenRouter là generator user đang lấy làm cơ sở thảo luận.
  Không chạy local 9B; provider ID/settings cần đối chiếu khi thiết kế experiment.
  Các API candidates đã ghi nhận trước không tự bị loại bởi bản ghi này.

## Trả đáp án và nguồn — user chọn trả một lần

MVP trả câu trả lời hoàn chỉnh cùng nguồn sau khi xử lý xong, không streaming.
Frontend hiển thị trạng thái đang xử lý trong lúc chờ; không đưa đoạn sinh
dở hoặc debug/token/score ra UI. Quyết định này không thêm retry API tự động.
Đề xuất response tối thiểu gồm answer và sources dùng cho chính câu trả lời;
mỗi nguồn có nhãn tài liệu/mục và evidence gốc dễ đọc. Backend kiểm tham chiếu
citation trỏ tới evidence thực đã cấp cho generator trước khi trả response.
Việc kiểm ID hợp lệ không chứng minh claim được evidence hỗ trợ; generation vẫn
phải bám evidence. Public response/error đã được chốt ở Decision #6a bên dưới;
không khôi phục nguyên JSON context/phần quản lý nguồn cũ của Foods.

### Citation/response/error tối thiểu — Decision #6a

User chọn strict minimal. Response success gồm `answer` và `sources`. Trong
answer, dùng nhãn `[1]`, `[2]` cạnh câu/nhóm câu dựa trên cùng bằng chứng; đánh
số trong một response, không dùng chunk_id hoặc đường dẫn máy làm nhãn. Mỗi
source gồm
`id`, `title`, `heading_path`, `excerpts` (các đoạn nguyên văn bản ingest).
Backend ánh xạ số citation với chunk/evidence thật trong context request;
không nhận nội dung source do generator tự viết lại. Chỉ trả sources được
answer tham chiếu. Không cần public source ID bền qua reindex cho MVP một lượt.

Frontend bấm nhãn để xem tên tài liệu/mục và từng excerpt. Các excerpts rời
nhau hiện thành các đoạn riêng, không giả là một đoạn liên tục. Có thể render
Markdown để dễ đọc nhưng không thực thi HTML/script từ nguồn; giữ bản text
evidence nguyên vẹn ở backend. Chi tiết component/render thuộc plan sau;
không tạo version store hoặc endpoint đọc file tùy ý từ machine path.

Kiểm citation ID tồn tại không chứng minh mọi claim đúng. Generation cần bám
evidence và evaluation phải kiểm claim–source support. Retrieval/provider/
generation hoặc citation validation failure trả typed non-2xx
`{error:{code,message}}`; không partial success, silent fallback hay automatic
repair/retry. Thiếu evidence không phải technical failure: trả phần có căn cứ
hoặc nêu thiếu thông tin. Exact HTTP statuses/codes được khóa trong Written Spec.

### Context budget — Decision #6b

User chọn token-budget động. Budget linh hoạt theo approved generator profile,
nhưng `context_limit`, `reserved_output_tokens` và `safety_margin` được cố định
trong từng benchmark run để kết quả reproducible. Mỗi request trừ actual tokens
của system prompt, query và format/citation overhead, rồi pack nguyên primary
chunks theo final rank, tối đa 5. Khi chunk kế tiếp không vừa thì dừng; không
skip chunk hạng cao, truncate hoặc summarize evidence để nhét thêm chunk.

Đổi model/profile mới được đổi budget và report phải ghi exact values. Nếu chunk
hạng đầu không vừa sau các khoản reserve, trả typed configuration/input error.
Không dùng một character/token limit chung cho mọi model và không tự mở rộng tới
provider maximum theo từng request.

### Generator/provider và evaluation judge — Decision #6c

User chọn một concrete generation profile: `qwen/qwen3.5-9b` qua OpenRouter cho
cả hai consumer sinh nội dung của experiment — tạo phần bổ sung của
representation B ở preprocessing và tạo câu trả lời online. Mỗi benchmark run
pin đúng một upstream provider, ghi provider/settings vào report và không dùng
automatic routing hoặc silent failover. Exact upstream được kiểm availability
trước execution rồi khóa trong approved plan/run; quyết định này không cấp quyền
gọi API trước khi Written Spec và Plan được duyệt.

Evaluation giữ vai trò độc lập: LLM judge chấm Accuracy, Completeness và
Relevance bằng `gpt-5.4-mini` qua OpenAI API. Judge không tạo representation B,
không tạo câu trả lời được chấm và không thay thế citation validation. Như vậy
candidate generator và judge không bị nhập thành một vai trò.

Representation B không phải nguồn mới hoặc vector type mới. Nó giữ nguyên chunk
A và `evidence_parts`, rồi bổ sung có chọn lọc một đoạn context tìm kiếm do Qwen
sinh từ chính input chunk ở preprocessing. Chuỗi bổ sung tham gia
`search_text` cho embedding/retrieval nhưng không là evidence, citation hoặc
Golden truth; chunk không vừa giới hạn của cả ba embedding tokenizers giữ nguyên
representation A, không truncate hay đổi boundaries.

### Exact generator settings và numeric budgets — Decision #6d

User chọn profile balanced/reproducible A. Với `qwen/qwen3.5-9b`, không set thêm
sampling knobs ngoài `temperature=0`. Representation B có
`max_output_tokens=256`. Answer generation dùng `context_limit=16384`,
`reserved_output_tokens=2048`, `safety_margin=512` và timeout 90 giây. Không có
automatic retry/failover. Exact upstream provider được preflight, pin và ghi lại
trước mỗi approved benchmark run. Đây là application profile cố định trong run,
không phải claim về provider maximum.

Budget 256 chỉ áp dụng cho phần mở rộng tìm kiếm của representation B, không áp
dụng cho câu trả lời người dùng. Phần B phải cô đọng và toàn input sau bổ sung
vẫn phải qua kiểm giới hạn của cả ba embedding tokenizers; không vừa thì giữ A.
Answer reserve 2048 dành chỗ cho câu trả lời dài hơn như lịch trình nhiều ngày,
nhưng vẫn chỉ dựa trên evidence được cấp và tuân thủ tối đa 5 primary chunks.

Agentic RAG tương lai phải có profile và contract riêng cho tool schemas/results,
plan/state, số bước/tool calls, timeout/failure, tổng token/thời gian/chi phí và
provenance. Không dùng hoặc suy rộng ngân sách one-shot RAG hiện tại thành ngân
sách agentic; thêm profile agentic cần một scope và approval riêng.

### UI interaction cho one-shot response/citations — Decision #6e

User chọn inline tối giản. UI có một ô câu hỏi và nút gửi; trong lúc request đang
xử lý, hiển thị loading và ngăn submit trùng. Thành công render answer Markdown
an toàn. Mỗi citation `[n]` là control truy cập được bằng bàn phím; khi kích hoạt,
UI cuộn và chuyển focus tới source card cùng `id` ngay dưới answer.

Source card chỉ render `title`, `heading_path` và từng `excerpt` tách biệt theo
public response đã chốt; không giả các excerpts rời nhau thành một đoạn liên tục.
Typed error hiển thị message và cho phép người dùng thử lại thủ công, không tạo
automatic retry. MVP không có streaming, chat history/session, raw payload,
debug/score/token UI hoặc agentic tool/plan UI. Exact visual styling và component
structure thuộc Written Spec/Plan, không mở rộng API/state.

### Nguồn mâu thuẫn — user đã chọn A

Nếu evidence được cung cấp trong context mâu thuẫn về cùng đối tượng, thời
điểm và điều kiện áp dụng, câu trả lời nêu rõ các thông tin khác nhau cùng
citation tương ứng, nói chưa thể xác định thông tin nào đúng, và tiếp tục
trả lời phần còn lại có căn cứ. Không tự ưu tiên theo thứ hạng retrieval,
tên file/domain hoặc kiến thức sẵn có của generator. Không suy rằng một
nguồn duy nhất trong context chứng minh toàn corpus không có mâu thuẫn.

Khác giá theo nhà cung cấp, thời điểm, đối tượng hoặc quyền lợi không tự là
mâu thuẫn; trình bày rõ các phạm vi đó. Đây là policy generation trên evidence
hiện có, không yêu cầu xây bộ phát hiện mâu thuẫn toàn corpus, gọi web hoặc
thêm model phán xử cho mỗi request. Evaluation cần có ca mâu thuẫn cùng phạm
vi và ca chỉ khác điều kiện để kiểm hành vi này; chưa chốt số ca/threshold.

## Reranker và input quá dài — user đã chọn A

Reranking thuộc phạm vi MVP, cùng đường no-rerank để so sánh có kiểm soát.
Có module reranker không đồng nghĩa mọi cấu hình hoặc lượt hỏi đều phải dùng
nó. Chưa chọn winner/default trên full corpus. MiniLM được nhắc ở đây là
candidate local `cross-encoder/ms-marco-MiniLM-L-6-v2`, chấm mức liên quan
của cặp query/chunk để sắp lại candidates; không phải generator viết đáp án.
Giới hạn pair 512 là config khảo sát đã ghi, không là số từ hoặc body budget.

User chọn A: với query hợp lệ, nếu input pair của bất kỳ candidate dự kiến
rerank vượt giới hạn model thì bỏ rerank cho toàn bộ request, giữ thứ tự và
điểm trước rerank. Không cắt query/evidence, không rerank riêng phần vừa rồi
trộn điểm hai loại. Kiểm input thật trước inference. Ghi lý do và số lượt
bỏ rerank trong logs/evaluation; báo kết quả pipeline thực tế và phân biệt
các lượt có/không rerank, không ghi mọi lượt đều đã rerank. UI không hiện
token counts hoặc debug. Đây là chính sách độ dài, không fallback chung cho
lỗi model/provider. API query limit và embedding query budget vẫn cần thiết
kế riêng; lựa chọn này không cho phép query dài tùy ý.

## Nguồn thay đổi và quy ước xuống dòng — user đã chọn A

User xác nhận tập trung vào nội dung văn bản, giao Reviewer quyết định chi
tiết xuống dòng. Đọc UTF-8 strict và đổi CRLF/CR thành LF trước cả tính locator
lẫn đối chiếu nguồn lúc startup. Đổi kiểu xuống dòng đơn thuần không yêu cầu
ingest lại. Không mở rộng xác nhận này thành bỏ dấu, Unicode-normalize, xóa
Markdown, gộp khoảng trắng hoặc xóa dòng trống: các phép đó có thể đổi cấu trúc
và vị trí bằng chứng. Không cần hỏi user từng chi tiết xử lý text nội bộ.

Thiết kế đề xuất cho startup: lưu danh sách source paths đã ingest cùng
SHA-256 của text LF mã hóa UTF-8; startup discovery lại đúng corpus rồi so tập
paths và dấu vết nội dung. Thêm/xóa/đổi tên file hoặc text LF thay đổi thì báo
cần ingest lại, chưa phục vụ chatbot. Không dùng mtime/size làm bằng chứng
nội dung giống nhau. Đây là kiểm nguồn cho citation đã chốt, không phải cơ
chế quản lý lịch sử/evaluation package. Nơi lưu, dấu hiệu ingest hoàn tất và
đối chiếu cấu hình/payload còn hoàn thiện cùng ingestion lifecycle; chưa có
execution evidence. Citation luôn dùng evidence bản ingest, không lấy file
vừa sửa thay cho evidence đó.

## Nhánh thử nghiệm: lấy thêm điều kiện gốc sau Top-5

User đồng ý thiết kế sau nhưng yêu cầu đưa vào thử nghiệm sau baseline, chưa
triển khai/bật mặc định cho MVP ban đầu:

1. Retrieval và scoring/reranking chọn tối đa 5 chunk chính.
2. Lấy các đoạn điều kiện gốc đã liên kết với chunk chính.
3. Điều kiện bắt buộc không cạnh tranh điểm với chunk chính và không bị loại
   chỉ vì điểm retrieval/reranking thấp.
4. Gộp trùng đoạn dùng chung. Context có thể có hơn 5 đoạn bằng chứng, nhưng
   vẫn phải nằm trong ngân sách token tổng, tính cả nhãn và phần input khác.
5. Khi thiếu ngân sách, ưu tiên nhóm chunk chính có thứ hạng cao hơn cùng điều
   kiện bắt buộc; không giữ phần chính rồi cắt riêng điều kiện cần để hiểu đúng.
6. Citation truy tới từng đoạn nguồn thực sự dùng, kể cả các đoạn không liên tục.

Lo ngại user nêu: lấy thêm nguồn có thể đưa nội dung không liên quan vào context,
làm câu trả lời mơ hồ, đặc biệt với generator dự kiến Qwen3.5 9B. Đây là giả thuyết
cần đo trên corpus thật, chưa phải kết luận chất lượng của model.

Nhánh này khác B của chunking: B sinh ngữ cảnh tìm kiếm bằng API ở preprocessing;
mở rộng context ở đây lấy nguyên văn nguồn sau retrieval. Không trộn hai biến
trong cùng phép so sánh ban đầu.

## Chunking baseline đã được user xác nhận sau đối chiếu corpus

Mục tiêu là điều chỉnh MVP Foods đã thực hiện trong guides/backend cho toàn bộ
corpus hiện tại. Không xây một MVP độc lập hoặc chỉ mở rộng glob.

### Input và luồng xử lý

`curated Markdown → discovery → cấu trúc heading/paragraph/list/table/blockquote
→ nhóm nội dung → tách theo token → text tìm kiếm và evidence → embedding/Qdrant`.

Giữ sorted discovery, H1 title, đọc intro trước H2, source-relative paths và
output deterministic khi input/cấu hình không đổi. Loại image-only lines,
source-tracking section và file quản lý theo phạm vi được chốt. Không bỏ
paragraph ở giữa heading levels; không tạo chunk chỉ có heading hoặc separator.

Parser hiện tại đã đọc intro trước H2. Phần cần thay là H2-only grouping,
400-character splitting, xử lý list không giữ cấp lồng nhau, nhãn Foods và
metadata không có source positions. Không viết lại những behavior đã đủ.

### Ranh giới và các mẫu đối chiếu

| Cấu trúc thật | Hành vi cần bảo vệ |
|---|---|
| Mệ Kéo / Thông tin | Giữ mục ngắn nếu vừa ngân sách, gồm giờ và “thường hết sớm hơn” |
| Hội xuân Gia Lạc / Thông tin chung | Giữ nhãn thời gian/địa điểm với list con; phân biệt lịch sử và phục dựng |
| Đại Nội / Các công trình kiến trúc | Tách chủ đề Ngọ Môn, Điện Thái Hòa…; mục dài chia tiếp theo đoạn/nhóm list, giữ heading path |
| Lịch trình 3 ngày 2 đêm / Module biển và đầm phá | Ưu tiên giữ phạm vi thay thế, cách chọn và điều kiện cùng nhau, không tự tách mọi H3 |
| Vé biểu diễn / bảng Ca Huế | Giữ header, đơn vị, đối tượng và nhà cung cấp khi chia; không trộn chính sách trẻ em |
| Chi phí du lịch Huế / dự toán | Giữ quan hệ hạng mục/tổng và bản chất hạn mức kế hoạch, không biến thành giá nhà cung cấp |

Heading là dấu hiệu tổ chức, không phải lệnh tạo chunk. Văn bản dài ưu tiên
ngắt theo đoạn/câu; list giữ cha/con; bảng dài chia theo nhóm ý nghĩa và giữ
headers/đơn vị/điều kiện. Baseline không overlap cố định. Chỉ dẫn tối thiểu
ngoài corpus có thể cần cho trường hợp quan sát được, không mặc định parser
hiểu mọi quan hệ ngữ nghĩa hoặc xây sẵn hệ thống liên kết toàn corpus.

### Dữ liệu đầu ra và giới hạn input

Phân biệt text tìm kiếm (title, heading path, nội dung), evidence nguyên văn
và thông tin nguồn. Hướng đã được user xác nhận là giữ khoảng ký tự trong bản
nguồn đã ingest cùng đoạn gốc; chunk ID phục vụ indexing, locator phục vụ
truy ngược. Chi tiết quy ước offsets/newlines/schema vẫn phải xác định trước
implementation, không đưa ID/path kỹ thuật ra UI chatbot.

Các phần có thể nằm cùng Qdrant payload; chưa cần kho lưu toàn bộ lịch sử.
Không giữ contract đúng bảy fields hoặc ID chạy toàn file chỉ vì code cũ dùng.
Khi render/ghép lại bảng hay lặp header, vẫn phải phân biệt phần trình bày với
các đoạn nguyên văn; không dùng text đã ghép làm bằng chứng exact substring.

Ngân sách dựa trên input thật của embedding/reranker/generator, gồm ngữ cảnh,
prefix và overhead tương ứng. Đã đo tokenizer trên mẫu đến lượt 3, chưa chốt
target body hoặc policy mọi oversized group trên toàn corpus. Bảng
không được miễn kiểm input limit; trường hợp không chia được mà vẫn đủ nghĩa
phải được ghi rõ khi xem trước, không âm thầm truncate hoặc bỏ nội dung.

### Các điểm cần giải quyết để hoàn thiện written spec

- Parser đã chọn sau khảo sát approved; đưa cấu hình/quy ước locator vào spec,
  không mở lại khảo sát mặc định.
- Dùng khảo sát tokenizer đã có để hoàn thiện packing và hành vi cho nhóm
  nội dung quá dài; không chạy lại mẫu cũ mặc định.
- Chốt schema/locator tối thiểu, cách giữ liên hệ khi render bảng hoặc bỏ ảnh.
- Kiểm nội dung quản lý lẫn answer content, như bảng chuẩn hóa Hải Vân Quan;
  không loại cả mục chỉ vì heading mang tính quản lý.
- Chốt các mẫu output và verification toàn corpus: nội dung được bao phủ đúng
  scope, không bị mất/biến đổi nguyên văn, list/table giữ nghĩa, output ổn định.

### Schema/locator sau khảo sát parser approved và Decision #3

User chốt A tại Decision #3. Mỗi Qdrant point có ba vùng dữ liệu, không lặp giữa
chúng:

| Vùng | Nội dung |
|---|---|
| Point ID | ID nội bộ deterministic; không phải locator hoặc nhãn UI |
| Vector | Hai named vectors `dense` và `sparse` theo Decision #1 |
| Payload | Chỉ `search_text`, `source`, `title`, `heading_path`, `evidence_parts` |

`source` là POSIX path tương đối `knowledge-base-hue/`. `title` là H1 gốc;
`heading_path` là danh sách heading tổ tiên và heading hiện tại theo thứ tự,
không lặp H1; intro trước H2 dùng danh sách rỗng. `evidence_parts` là danh sách
`{role,start,end,text}` với role `body`, `header` hoặc `condition`.
`search_text` là representation phục vụ embedding/retrieval/reranker/context.

Không lặp point ID hoặc vectors trong payload. Không lưu `domain`, `subdomain`,
source hash, model/representation IDs, token counts, timestamps, versions hay
scores per-point: domain suy từ `source`; source fingerprint thuộc file/index;
model/representation identity thuộc collection/build. Chỉ thêm field mới khi
có consumer được User duyệt.

Quy ước đề xuất: đọc UTF-8 nghiêm ngặt, chuẩn hóa CRLF/CR thành LF một lần,
tính zero-based Unicode code points `[start,end)` trên chính chuỗi đó. Không
Unicode-normalize, sửa dấu hoặc xóa whitespace bên trong evidence. Mỗi part
phải đúng `source_text[start:end] == text`; không tìm bằng lần xuất hiện đầu
tiên của substring trên toàn file khi có nội dung lặp.

Parser chỉ xác định cấu trúc/vị trí. Evidence phải được cắt từ source đã
chuẩn hóa, không lấy HTML render hoặc token.content đã bỏ Markdown làm gốc.
Nếu chia trong một paragraph, offset con phải được suy ra trong vùng nguồn
cha. Nếu bỏ dòng chỉ có ảnh, phần trước/sau có thể thành hai spans; không nối
chúng rồi tuyên bố là một substring liên tục. Giữ nguyên inline HTML/Markdown
trong evidence; trình bày an toàn cho UI thuộc thiết kế citation/frontend.

Thứ tự `evidence_parts` là thứ tự trình bày trong chunk; không bắt buộc tăng
dần theo vị trí nguồn. Header/điều kiện có thể được dùng lại ở nhiều chunk.
Mỗi part vẫn định vị riêng; không tạo graph/dependency expansion sau Top-5.
Heading/title là nhãn có nguồn gốc từ tài liệu, không thay body evidence.
Khi chính nội dung heading là cần thiết cho bằng chứng, phải giữ nguyên dòng
heading trong part nguồn thích hợp, không chỉ dựa vào nhãn render.

`chunk_id` không hứa ổn định qua edit/rechunk; đề xuất cụ thể cho ID/lưu trữ ở
mục dưới. Startup đối chiếu bản ingest vẫn phải có contract riêng; không thêm
version store hoặc coi source locator tự giải quyết việc nguồn thay đổi.
Backend trả evidence text đã resolve cho frontend; frontend không tự áp
offset Python vào chuỗi UTF-16. Public citation contract chưa chốt tại đây.

### ID và lưu trữ tối thiểu — Decision #3

ID nội bộ dùng cặp `(source, chunk_ordinal)` với ordinal bắt đầu từ 0 trong
mỗi file, theo thứ tự chunker deterministic xuất ra; serialize cặp bằng JSON
compact để không nhập nhằng ký tự phân cách trong path. Qdrant point ID dùng
UUID5 từ chunk_id với một namespace cố định. Không nhét offsets/conditions
vào ID hoặc hứa ID giữ nguyên sau khi thêm/chia lại chunk trước đó. Locator
và evidence_parts mới là căn cứ xác định bằng chứng trong bản ingest.

Payload lưu `search_text` một lần cùng `source`, `title`, `heading_path` và
`evidence_parts`. Không lưu thêm body/citation text ghép trùng với các parts.
Retrieval trả các fields cần qua context builder để citation còn nguồn gốc;
public response chỉ lấy whitelist theo citation contract, không trả nguyên
payload.

Đề xuất ingest toàn bộ lại khi corpus thay đổi trong MVP, lúc server tắt;
không thêm incremental update cho ID vốn không ổn định qua rechunk. Ingest
phải xử lý hết preview errors trước embedding/ghi index, không để points của
bản cũ còn lẫn trong kết quả mới. Cách tạo/đổi collection, ghi manifest hoàn
tất và kiểm payload/model identity sẽ cụ thể hóa tiếp trong ingestion
lifecycle; mọi mutation active collection vẫn cần exact authority trong
approved plan. Đây là đề xuất thiết kế, không quyền reindex hiện tại.

### Gắn điều kiện: cấu trúc hỗ trợ, quyết định ngữ nghĩa phải rõ

- Bảng lặp header cột khi chia; paragraph/list giữ nhãn cha và các điều kiện
  cần để hiểu đúng. Câu dẫn trước H3/H4 không bị mất chỉ vì không thuộc leaf.
- Không mặc định mọi paragraph trước bảng hoặc mọi intro là điều kiện bắt
  buộc của mọi chunk con. Không suy luận từ vị trí rằng một điều kiện áp dụng
  cho nhà cung cấp khác hoặc tiểu mục ngang hàng.
- Mẫu Ca Huế: câu dẫn khảo sát 09/2026 thuộc H3 2.3, áp dụng cho các mức giá
  bên dưới; Không bao gồm ở A không tự lan sang B thuê nguyên thuyền. Chính
  sách trẻ em của từng nhà cung cấp nằm cùng hàng nguồn tương ứng.
- Mẫu Chi phí du lịch Huế: intro mô tả bản chất hạn mức kế hoạch cần được xét
  cùng bảng dự toán, kể cả khi cách xa heading hiện tại.
- Hướng trực tiếp cho ngoại lệ đã quan sát: chỉ dẫn nhỏ ngoài corpus liên kết
  vùng điều kiện với vùng nội dung đích trong cùng file, resolve ngay ingest.
  Probe đã kiểm full heading path/type/exact signature và match duy nhất trên
  mẫu. Chốt format nhỏ và mismatch policy cho ingest; không xây rule engine.
- Chưa tự loại mục quản lý có lẫn answer content; mẫu Hải Vân Quan cần đọc
  và liệt kê phần hữu ích/phần quản lý trước khi chốt phạm vi lọc.

Parser đã chọn: `markdown-it-py` 4.2.0, `MarkdownIt().enable('table')`.
Khảo sát sáu file có line maps cho list/table rows/heading/paragraph/blockquote;
map không phải character offsets và một số inline/cell tokens không có map.
Evidence lấy từ slice source LF. Two-pass và condition probes có kết quả mẫu
được review; không production-harden hoặc copy script khảo sát vào runtime.
40/40 parts không chứng minh coverage toàn corpus; coverage report là tĩnh.

User approved khảo sát, không approved written spec. Contract khảo sát gốc đã
completed; canonical review mục 9–10 dẫn report/script/JSON. Cần hoàn thiện
schema/format điều kiện/oversized groups và consumers trước implementation.

### Đề xuất cụ thể cho packing và condition mapping — chờ duyệt written spec

Phần này cụ thể hóa thiết kế của Reviewer từ khảo sát đã approved; không nâng
agenda mục 30 thành quyết định user. Hành vi chặn ingest khi nhóm tối thiểu vẫn
vượt input limit đã được user chọn A; chi tiết ở cuối mục này.

Luồng đề xuất: `source LF → blocks có vị trí → gắn điều kiện → nhóm/chia
→ tạo search_text → kiểm từng tokenizer → xuất chunks`.

**Nhóm và chia:** giữ mục ngắn cùng chủ đề khi vừa input. Với mục dài, xét
ranh giới chủ đề từ headings, rồi paragraph, nhóm list cùng nhãn cha, nhóm hàng
bảng. Không gộp các phương án loại trừ nhau hoặc các nhà cung cấp chỉ để lấp
đầy budget. Không ghép các mục độc lập chỉ vì còn chỗ; không tự tách mọi H3/H4.
Paragraph dài có thể chia tại ranh giới câu trong source span khi mỗi phần
vẫn hiểu được cùng nhãn/điều kiện. Không cắt cứng giữa câu, list item hoặc ô
bảng để ép vừa tokenizer. Nếu một đơn vị đó chứa nhiều ý có thể tách nhưng
cấu trúc chưa chỉ rõ, báo vị trí cần chỉ dẫn cụ thể thay vì đoán ngữ nghĩa.

List chia theo nhóm con phải lặp nhãn cha nguyên văn cần thiết. Bảng chia theo
nhóm hàng phải lặp header gồm delimiter, giữ đơn vị, đối tượng/nhà cung cấp
và các điều kiện áp dụng. Không đặt một hàng làm kích thước mặc định. Với bảng
dự toán, ưu tiên giữ cả bảng cùng intro hạn mức; nếu phải chia, không tách hàng
tổng khỏi các hạng mục mà nó tổng hợp rồi trình bày như một dự toán đầy đủ.
Trường hợp chưa có cách chia giữ quan hệ này đi vào danh sách cần xử lý.

**Format chỉ dẫn:** đề xuất một JSON ngoài corpus, là danh sách record
`{source, condition, targets}`. `source` là path tương đối knowledge-base-hue;
`condition` và mỗi phần tử `targets` dùng selector
`{heading_path, block_type, exact_text}`. Block types chỉ cần các loại thực có
trong chỉ dẫn: paragraph, list_item, table. `exact_text` là toàn văn block
nguồn LF được chọn, giữ Markdown và LF nội bộ; không phải prefix, hash hoặc
text render. Chỉ dẫn nhỏ này chấp nhận lặp nguyên văn vài block để người đọc
kiểm được đích; không tạo DSL, regex rules hoặc bảng liên kết giữa chunk IDs.

Resolve mỗi selector trong đúng file, full heading path không H1 (`[]` cho
intro), đúng loại block và toàn văn. Mỗi selector phải có đúng một kết quả;
không tự chọn kết quả đầu hoặc fallback theo tên heading cuối. Thiếu/trùng/
sai signature hoặc span ngoài vùng cấu trúc đã chọn là lỗi chỉ dẫn, cần sửa
trước xuất bộ chunks hợp lệ. Mọi kiểm tra này phải có tác dụng quyết định
kết quả, không chỉ xuất boolean rồi vẫn báo đạt. Chúng không chứng minh đủ
ngữ nghĩa: người review vẫn đối chiếu phạm vi điều kiện trên các vùng liên quan.

Các liên kết đã có evidence để cụ thể hóa: lead Ca Huế H3 2.3 → bảng A và B;
Không bao gồm H4 A → chỉ bảng A; intro Chi phí giữ hai LF → ba bảng dự toán.
Khi target được chia, condition đi vào mỗi chunk chứa phần target cần điều
kiện đó. Đây là sao chép evidence ngay ingest, không là lấy thêm sau Top-5.
Không tự lan điều kiện sang siblings hoặc tài liệu khác. Chỉ dẫn mới chỉ thêm
cho quan hệ thực được phát hiện; không hứa ba rules này bao phủ toàn corpus.

**Representation A:** dùng schema ở mục trên. Label là title + LF, tiếp theo
là heading_path nối bằng ` > ` + LF nếu path không rỗng. Ghép evidence theo
nhóm cấu trúc: hai LF giữa paragraph/list/table độc lập; một LF giữa header
và các hàng thuộc cùng bảng. Giữ nguyên LF bên trong mỗi part. Với hai mẫu
Ca Huế đã đo: label + lead + hai LF + header + LF + row + hai LF + exclusions.
Các LF nối là phần trình bày; không sửa text/spans của evidence để ghép.
Điều kiện sau bảng giữ sau hàng khi cách đọc đó phù hợp nguồn.
Một span dùng nhiều lần trong cùng chunk chỉ giữ một lần; header/condition
được lặp giữa các chunks khi cần. Nhãn và LF thêm khi ghép là phần trình bày,
không tự là source evidence. Citation đọc từng part, không đọc search_text.

Kiểm toàn bộ representation sau preprocessing riêng từng embedding model,
tính prefix/special tokens, không truncation. Chỉ chấp nhận chunk khi vừa cả
ba model; không đặt target body chung, không giữ chỗ tùy ý cho B. Nếu quá dài,
chia lại nhóm theo nguyên tắc trên rồi đo lại input đầy đủ. MiniLM query pair
và generator prompt có ngân sách riêng, không dùng để hứa mọi query đều vừa.
Nếu thay format mẫu thì số đo mẫu cũ chỉ là tham khảo, không PASS cho text mới.

**User đã chọn A — nhóm tối thiểu vẫn vượt embedding limit:**
Preview liệt kê file/mục, nhóm nguồn và counts/limit từng model;
chặn ingest trước embedding/ghi index nếu còn nhóm chưa xử lý. Người triển
khai cùng Reviewer xử lý đúng ngoại lệ bằng ranh giới/chỉ dẫn giữ nghĩa;
không mặc định sửa corpus hoặc đổi model. Nếu không có cách đáp ứng contract,
trình user trade-off thay đổi thiết kế. Preview gom các vấn đề trong một lượt,
không thêm workflow retry/resume hoặc trạng thái quản lý ngoại lệ riêng.

Không bỏ các nhóm chưa xử lý để ingest phần còn lại. Silent truncation/bỏ
điều kiện không là lựa chọn hợp lệ. Quyết định này không duyệt toàn bộ written
spec/plan hoặc cấp quyền triển khai runtime.
Chưa có evidence về nhóm bất khả chia trong toàn corpus. Hai input VN/QT đúng
đã đo bổ sung và vừa limits theo mẫu; không phải ví dụ nhóm bất khả chia.

**Giải thích schema/locator cho phạm vi MVP:** metadata cho biết tên tài liệu,
mục và file nguồn; evidence_parts giữ từng đoạn gốc cùng vị trí; search_text
là chuỗi ghép nhãn và các đoạn đó cho tìm kiếm. Ca Huế có lead, header, hàng
giá và Không bao gồm ở các vị trí khác nhau, nên một khoảng liên tục có thể
kéo thêm hàng giá không liên quan. Mỗi part giữ locator riêng giải quyết đúng
nhu cầu bấm xem bằng chứng đã chốt. `role` chỉ phân biệt body/header/condition,
không tạo graph hoặc cơ chế truy xuất mới. `search_text` có thể dựng từ metadata
và parts; việc cần lưu thêm bản dựng đó trong payload phải theo consumer thực,
không mặc định lưu trùng ở mọi layer. Exact storage vẫn cần hoàn thiện cùng
payload/citation contract; user đang yêu cầu giải thích tính cần thiết, chưa
coi câu hỏi này là approval tất cả fields.

### Evidence bổ sung và trạng thái mẫu thiết kế

Khảo sát Implementer đã tới lượt 3:
`reports/full_corpus_chunk_samples_tokenizer_survey_2026_09_09.md`, JSON/script
cùng tên gốc dưới `reports/artifacts/`. Reviewer chưa rerun độc lập. Số đo,
queries chuẩn hóa, spans và các correction được lưu đầy đủ ở context mục 26.
Research reference correction và giới hạn Reviewer kiểm ở context mục 27;
không dùng bản report đầu với ví dụ tự soạn bị gọi data thật hoặc số đo sai.

Mẫu Reviewer ưu tiên: Gia Lạc P1 2 chunks, Ngọ Môn P1 2 chunks; Ca Huế lượt 3
4 chunks giá tách VN/QT/hai nhà cung cấp trẻ em, mỗi chunk giữ nguyên câu dẫn
khảo sát 09/2026 + header + Không bao gồm. Chunk dịch vụ ưu tiên with_lead để
giữ phạm vi tour khảo sát. Không có giá không đủ để coi quyền lợi/hành trình
đó là quy chuẩn chung. Mệ Kéo/module biển giữ nguyên nếu vừa input đầy đủ.

Hai mẫu lead VN/QT cũ sai boundaries: counts HuyDang 230/203 và MiniLM long
462/418 không được dùng cho input nguyên hàng đã sửa. Hai composites mới
search_text 931/866 ký tự đã đo: E5-small/base 290/290 và 268/268, HuyDang
224/208, MiniLM orig/long 411/453 và 385/427. Xem
[review khảo sát mới](../../../reports/full_corpus_vn_qt_token_check_codex_review_2026_09_09.md):
user đã approved; Reviewer kiểm artifact, không rerun tokenizer.
Hai mẫu trẻ em giữ evidence
lịch sử 248/245 HuyDang, 479/459 MiniLM long; dịch vụ with_lead 165/385. Khối VN+QT gộp 264/527 vượt giới hạn tương ứng.
Đây là ví dụ dùng hoàn thiện thiết kế, chưa phải production output toàn corpus.
Không chốt 1–2 hàng/bảng hoặc target 250 token; kiểm input đầy đủ từng model.

## Evidence simplicity đã đối chiếu trong phiên

Chỉ đọc reports có `simplicity` theo yêu cầu user; không chạy lại các lệnh trong
reports. Đã đọc report implementation/review tương ứng và user report khi có
file phù hợp ở Phase 2, 3, 4–5, 6 và post-simplicity Phase 7. Một số phần liệt kê
lệnh/tests được đọc chọn lọc; không gọi đây là audit live toàn backend.

| Nguồn evidence | Kết luận phục vụ thiết kế |
|---|---|
| [Phase 2 Reviewer](../../../reports/phase_2_foods_markdown_chunking_simplicity_codex_review.md) | Refactor trước giữ nguyên 572 ordered chunks, chỉ còn chunker/splitter; không chứng minh 400 ký tự tối ưu cho corpus mới |
| [Phase 3 review](../../../reports/phase_3_embedding_sparse_representation_simplicity_review.md) | Concrete E5 instance, native batching, bỏ provider wrappers; TF-IDF còn ở thời điểm này nhưng bị bỏ ở Phase 4–5 |
| [Phase 4–5 Reviewer](../../../reports/phase_4_5_qdrant_retrieval_simplicity_codex_review.md) | Candidate dense-only giữ parity ranking với active Foods; chưa cutover. Report có correction nhỏ về test counts, không lấy claim Implementer thay Reviewer evidence |
| [Phase 6 Reviewer](../../../reports/phase_6_generation_api_simplicity_codex_review.md) | Context string và answer-only API đã thay JSON context/source mapping cũ; citation full-corpus là requirement mới cần thiết kế tối thiểu |
| [Phase 7 Reviewer](../../../reports/phase_7_post_simplicity_correction_codex_review.md) | Correction và smoke 20 câu chạy thật ở thời điểm đó; không phải full-corpus quality evidence hoặc threshold mới |

Đối chiếu source hiện tại xác nhận concrete E5 và labeled context string. Không
khôi phục TF-IDF runtime hoặc JSON context cũ chỉ vì report phase trước mô tả.
Các metrics giữa Implementer/Reviewer là những lần chạy riêng; không ghép
thành một fresh result. Reports cũ giữ nguyên.

## Tham chiếu và việc còn mở

### Lịch sử đã bị thay thế — Golden evidence claim-level exact source spans

User chọn phương án C ngày 2026-09-10. Full-corpus Golden vẫn là một dataset
JSONL đơn giản theo tinh thần `knowledge-base-hue/foods/evaluation/golden_v3.jsonl`;
không tạo annotation service, database hoặc framework riêng. Khác biệt cần
thiết là mỗi test case liên kết từng expected claim với evidence nguyên văn,
thay vì chỉ ánh xạ toàn case tới source + H2.

Mỗi claim dùng một hoặc nhiều `evidence_groups`; mỗi group là một tập
`evidence_ref` tối thiểu cùng hỗ trợ claim. Một `evidence_ref` dùng locator
`{source, heading_path, start, end, text}` trên source text LF đã ingest và phải
thỏa `source_text[start:end] == text`. Claim-to-evidence là ground truth
canonical; chunk IDs của một lần chunking không được lưu làm ground truth vì
có thể đổi khi rechunk. Evaluator ánh xạ spans sang chunks của candidate hiện
hành để đo retrieval, còn citation/answer evaluation dùng quan hệ claim–source
để kiểm support và completeness.

Giữ `question`, `reference_answer` và metadata phân loại ở cấp case để con
người đọc/review tương tự Foods V3. Cách biểu diễn alternative evidence groups,
case không có/thiếu/mâu thuẫn evidence, validation và metrics sẽ hoàn thiện ở
các quyết định tiếp theo. Lựa chọn C chưa duyệt toàn bộ written spec, chưa cấp
quyền tạo dataset hoặc implementation.

### Lịch sử đã bị thay thế — Golden record có expected claims

User xác nhận ngày 2026-09-10:

- năm top-level fields bắt buộc là `case_id`, `question`, `keywords`,
  `reference_answer`, `expected_claims`;
- `category` là optional diagnostic field, chỉ dùng breakdown/thống kê dạng câu
  hỏi và không đổi điểm của từng case;
- `partition` là authoring/review metadata của P7, được kiểm trong merge nhưng
  không đi vào canonical full-corpus JSONL;
- không lưu `domain` ở từng record; khi thật sự cần có thể suy ra từ authoring
  partition/manifest hoặc evidence sources;
- không lưu `claim_id`; evaluator/report derive từ `case_id` và claim ordinal;
- `keywords` được giữ làm lexical checklist/diagnostic, không làm retrieval
  ground truth và không thay thế exact evidence;
- `expected_claims` giữ mỗi claim `text` cùng `evidence_groups`; exact group
  semantics và locator validation còn chờ các quyết định tiếp theo.
- không lưu `case_type`. Với scope hiện tại, retrieval metrics resolve evidence
  spans còn answer evaluation so `reference_answer` và claim coverage; không có
  consumer cần routing field này. Chỉ mở lại nếu một scope tương lai được duyệt
  cần rubric riêng cho nhiều trạng thái answerability.

Schema này giữ ba nội dung User xem là trọng tâm (`question`, `keywords`,
`reference_answer`) nhưng chỉ thêm ID vận hành và claim-to-source ground truth
cần cho retrieval completeness, groundedness cùng citation support. Đây là
quyết định thiết kế, chưa phải written spec approval hoặc quyền tạo Golden.

### Complexity reset — User thay thế schema evidence bằng schema metric-only

Sau khảo sát toàn bộ evaluation `rag_old_0`, hai correction và independent
Reviewer review, User chọn phương án A ngày 2026-09-10. Quyết định này
**supersede** các đoạn “Golden evidence” và “Golden record field set” ngay phía
trên đối với official full-corpus Golden/evaluation:

- tại quyết định trung gian này từng chọn năm field gồm `case_id`, `question`,
  `keywords`, `reference_answer`, `category`; mục “bỏ `case_id`” phía sau đã
  supersede lựa chọn này và canonical hiện chỉ còn bốn field;
- `category` được giữ để thống kê số lượng/breakdown các loại câu hỏi, không
  tham gia routing hoặc tính điểm từng case;
- bỏ `expected_claims`, `evidence_groups`, source spans và chunk IDs khỏi
  official Golden;
- tiếp tục không lưu `case_type`, `domain`, `claim_id`; `partition` vẫn chỉ là
  metadata authoring/review P7 và bị strip khi merge;
- retrieval dùng keyword-substring relevance proxy cho MRR, nDCG@10 và Keyword
  Coverage; answer dùng `reference_answer` cho Accuracy, Completeness,
  Relevance;
- không claim các metric keyword này là exhaustive corpus relevance/recall;
- runtime citation UI/source mapping vẫn là scope riêng, nhưng official
  evaluation phase hiện tại không chấm citation verification hoặc claim-source
  groundedness.

Đây là thay đổi có chủ đích để loại annotation/metric complexity không phục vụ
sáu metric User cần. Vocabulary category, cách xác định số case, split, cutoff
K và aggregation đã được chốt ở các mục sau; thresholds và judge rubric vẫn mở.
Written spec và implementation plan chưa được duyệt; không có quyền sửa
Golden/runtime/index từ quyết định này.

### Tổ chức Golden — một file đích, biên soạn theo từng lĩnh vực

User chọn phương án A với quy trình theo giai đoạn ngày 2026-09-10: không viết
trộn toàn corpus ngay từ đầu. Trước hết biên soạn và review Golden riêng theo
từng lĩnh vực để `question`, `keywords`, `reference_answer` và `category` dễ
đối chiếu. Chỉ sau khi mọi phần đạt quality gate mới hợp nhất thành một JSONL
full-corpus canonical và tạo smoke subset từ chính file đó.

Các file theo lĩnh vực là working authoring/review partitions, không phải nhiều
benchmark độc lập lâu dài. Chúng không được evaluator dùng để ghép tùy ý trong
production benchmark. Sau merge, file full-corpus là dataset duy nhất dùng cho
official evaluation; smoke rows phải deep-equal với các rows tương ứng trong
full file. Thứ tự merge và IDs cần deterministic để cùng inputs tạo cùng output.

`knowledge-base-hue/foods/evaluation/golden_v3.jsonl` giữ nguyên như artifact
lịch sử đã approved. Phần Foods của Golden mới có thể copy các case phù hợp,
gán `case_id`/category generic theo schema mới và review lại nội dung; không sửa
hoặc định nghĩa lại Foods V3. Không bổ sung expected claims, evidence groups,
source spans hoặc chunk IDs vào official Golden mới.

Sau khi full-corpus được approved, các working partitions phải được retire khỏi
đường chạy chính để không có hai nguồn sự thật. Exact paths, cách lưu/retire
partitions, merge order, ID convention và validation sẽ chốt trong written spec
và plan; quyết định này chưa cấp quyền tạo hoặc merge Golden.

User chọn **P7** cho giai đoạn authoring/review ngày 2026-09-10: bảy working
partitions gồm `foods`, `heritages`, `festivals`, `performing_arts`,
`travel_places`, `travel_services` và `travel_tickets`. Cách chia này giữ riêng
ba nhánh travel trong lúc soạn và kiểm toán; nó không thay đổi taxonomy sản phẩm
gồm năm domain. Sau khi cả bảy partition đạt quality review, chúng được merge
vào một canonical full-corpus JSONL và rút khỏi official evaluator path.

User đã cung cấp reference Golden/evaluation tại
`/home/minhhieu/llm_rag/tai_lieu/rag_old_0`, thư mục phiên âm con
`phien_am_bai_hoc`, và `/home/minhhieu/llm_rag/tai_lieu/rag_old`.
Implementer được giao đọc/tóm tắt theo
`handoff_prompt/FULL_CORPUS_GOLDEN_EVALUATION_REFERENCE_HANDOFF.md` từ repo root.
Đã nhận report; review chọn lọc yêu cầu correction R1–R3 tại
`reports/full_corpus_golden_evaluation_reference_codex_review_2026_09_09.md`.
Đã kiểm được schema keyword và judge thiếu context; không nhận claim mọi
reference_answer đúng/đủ hoặc mọi metric cùng cutoff k. Tại mốc khảo sát này,
schema/số câu/quotas/split/metrics/threshold chưa được chốt; các quyết định mới
hơn ở phần Complexity reset và các mục cuối file đã thay trạng thái đó.
Reviewer đã kiểm correction lượt 2 ngày 2026-09-10 và đóng R1–R3. Đối chiếu
canonical Foods V3 sau câu hỏi của user phát hiện R4; Implementer đã sửa ở
correction lượt 3 và Reviewer re-review PASS. R1–R4 đều đóng. User xác nhận ngày
2026-09-10; khảo sát reference đã `approved/completed`. Written spec chưa
approved; các phần schema/evaluation còn lại vẫn mở.

Khảo sát sâu schema từ `rag_old_0` đến Foods V3 đã qua correction lượt 3,
independent Reviewer review và User confirmation; trạng thái
`approved/completed`. Các candidate trong report là evidence lịch sử, không
override lựa chọn metric-only mới nhất của User.

### Khảo sát tokenizer ngày 2026-09-09 và đề xuất output tiếp theo

Đã chạy khảo sát chọn lọc sáu khối nguồn bằng project `uv run --no-sync python`,
Transformers 5.14.1, tokenizer cache local và PyVi hiện có. Không tải weights,
chạy embedding/reranker inference, production chunker, Qdrant hoặc paid API.
Đây là đo độ dài input trên mẫu, không phải production chunks/quality benchmark
hoặc bằng chứng đã bao phủ toàn corpus. Lần đầu script sai tên header bảng và
dừng; đã sửa theo header thật rồi chạy lại thành công cả sáu mẫu.

| Khối nguồn | Ký tự body | E5-small/base | HuyDang | MiniLM query + document |
|---|---:|---:|---:|---:|
| Mệ Kéo / Thông tin | 274 | 97 / 97 | 78 | 144 |
| Gia Lạc / Thông tin chung | 1.171 | 352 / 352 | 272 | 512 |
| Lịch trình / Module biển và đầm phá | 629 | 204 / 204 | 160 | 305 |
| Đại Nội / Ngọ Môn | 1.726 | 530 / 530 | 423 | 738 |
| Chi phí / Dự toán một ngày | 754 | 280 / 280 | 212 | 371 |
| Ca Huế / bảng khách lẻ ghép thuyền | 1.050 | 444 / 444 | 339 | 574 |

E5 đếm title + heading path + body + `passage: ` + special tokens; HuyDang dùng
PyVi cho title/heading/body như benchmark runner hiện tại, không thêm E5 prefix.
MiniLM đếm cặp một câu hỏi tiếng Việt riêng cho mỗi mẫu với title/heading/body,
có special tokens. Không truncation. Counts chỉ áp dụng đúng text đã đo:
chưa thêm mọi điều kiện nằm ngoài các khối chọn, nên không coi bảng Ca Huế hay
bảng dự toán ở đây đã là chunk tự đủ nghĩa. Câu hỏi khác sẽ đổi pair length.

Cache snapshots đọc trực tiếp:

- E5-small: `614241f622f53c4eeff9890bdc4f31cfecc418b3`.
- E5-base: `d128750597153bb5987e10b1c3493a34e5a4502a`.
- HuyDang: `517f1af7dd04a57194f1de2990f0c6ede0a3109b`.
- MiniLM: `233902d25c440f23af6f7d6e94d2946bac0bee0a`.

Tokenizer configs hiện có: E5 512, HuyDang 256, MiniLM 512. E5/HuyDang max length
còn khớp `sentence_bert_config.json` và `dense_benchmark.py`. Chưa load model
để kiểm runtime truncation. Không dùng số token của những tokenizer này để
suy ra số token Qwen3.5 9B; generator tokenizer/context budget chưa đo.

Raw results và script khảo sát tạm:
`/tmp/hue_full_corpus_tokenizer_survey.json`,
`/tmp/hue_full_corpus_tokenizer_survey.py`. Đường dẫn /tmp không phải artifact
canonical tồn tại vĩnh viễn; counts và phạm vi đã ghi tại đây để chuyển phiên.

Schema/locator, ID/lưu trữ và các policy hiện hành đã được cụ thể hóa ở các
mục thiết kế phía trên; không giữ bản đề xuất sơ khởi thứ hai tại đây.
Sáu mẫu lịch sử không chứng minh Qdrant round-trip, toàn corpus hoặc chất
lượng RAG. Counts mới VN/QT nằm ở mục evidence bổ sung và review riêng.

- [Bản ghi context](../../../handoff_prompt/FULL_CORPUS_BRAINSTORMING_CONTEXT_2026_09_09.md): snapshot đầu file giữ quyết định hiện hành; mục 19/26/33 giữ các phép đo theo từng mốc, mục 35–38 giữ task reference Golden, review và trạng thái chuyển phiên.
- [Ghi chú kế hoạch thử nghiệm](../plans/2026-09-09-full-corpus-context-experiment-notes.md).
- Lifecycle/payload, API query/generator budgets, citation lỗi, model/provider
  settings, B budget/prompt, retrieval/evaluation matrix và Golden/frontend
  chi tiết còn cần hoàn thiện. Written spec rồi plan/Review Contract vẫn cần
  user duyệt riêng; bản ghi này không cấp quyền implementation.

### Category vocabulary — User chọn bảy nhãn generic

User chọn phương án A ngày 2026-09-10. Mỗi record canonical bắt buộc có đúng
một trong bảy giá trị:

`direct_fact`, `temporal`, `comparative`, `numerical`, `relationship`,
`spanning`, `holistic`.

`category` chỉ dùng để thống kê số lượng và breakdown kết quả. Nó không điều
hướng evaluator, không chọn rubric và không thay đổi điểm của từng case. Hai
nhãn riêng của Foods V3 (`food_knowledge`, `guide_planning`) không đi vào
vocabulary full-corpus. Artifact Foods V3 vẫn giữ nguyên; các case được đưa vào
Golden mới sẽ được phân loại lại vào một trong bảy nhãn generic mà không sửa
V3. Quota/phân bố theo category chưa được chốt.

### Case count — author theo chủ đề rồi suy ra tổng

User chưa chốt một tổng số cứng. Golden được biên soạn và review theo từng
partition P7 trước, sau đó merge để suy ra tổng thực tế. Khoảng planning target
là 150–200 câu cho toàn corpus, không phải acceptance quota.

Không đặt quota cứng theo category hoặc partition ở thời điểm này. Không tạo
case yếu chỉ để đạt một con số và không loại case đạt chất lượng chỉ để ép tổng
vào biên. Phân bố P7/category sẽ được báo cáo như kết quả quan sát sau curation;
coverage chất lượng của từng chủ đề vẫn phải được review trước merge.

### Evaluation split — một canonical set, không chia dev/test

User chọn phương án A ngày 2026-09-10. Scope hiện tại dùng toàn bộ file Golden
canonical làm một evaluation set; không tạo `dev`/`test` split. Lý do phạm vi:
Golden không được dùng để train hoặc fine-tune model trong phase này, nên chưa
cần thêm cơ chế holdout và quản lý hai tập.

Smoke vẫn là subset chạy nhanh có record deep-equal với canonical. Smoke không
phải một split độc lập và không thay đổi kết quả canonical. Nếu scope tương lai
dùng Golden để huấn luyện hoặc cần một holdout thật sự, đó là quyết định mới,
không được suy ngược vào thiết kế hiện hành.

### Retrieval cutoff — K=10 thống nhất

User chọn phương án A ngày 2026-09-10: official report dùng MRR@10, nDCG@10 và
Keyword Coverage@10. Một cutoff duy nhất giữ output đơn giản và khớp danh sách
10 tài liệu cuối mà evaluator PRO của `rag_old_0` thực sự trả về.

`K=10` ở đây là cutoff tính/báo cáo metric. Nó không tự quy định retrieval
depth nội bộ của pipeline; pipeline có thể lấy nhiều candidate hơn trước khi
rerank, nhưng evaluator chỉ chấm top 10 cuối.

### Metric aggregation — macro-average theo case

User chọn phương án A ngày 2026-09-10. Mỗi metric được tính cho từng case rồi
lấy trung bình cộng trên các case; mỗi câu hỏi có trọng số bằng nhau.
Official report hiển thị overall macro-average, tổng số case và cùng loại
macro-average/count theo `category`.

Không tính micro-average theo tổng số keywords và không tạo weighted/composite
score gộp sáu metric. Quy tắc xử lý case lỗi/không có kết quả vẫn cần chốt để
tránh âm thầm loại case khỏi mẫu số.

### Answer Evaluation — thang điểm 1–5

User chọn phương án A ngày 2026-09-11: Accuracy, Completeness và Relevance được
chấm thành ba điểm riêng, mỗi điểm là số nguyên từ 1 đến 5 như `rag_old_0`.
Thang này giữ kết quả dễ đọc và đối chiếu được với reference đã khảo sát.

Không chuẩn hóa điểm thành 0–1, không rút thành pass/fail và không gộp ba điểm
thành một composite score. Tại mốc lựa chọn này chỉ chốt miền điểm; rubric cụ
thể và prompt được chốt ở quyết định ngay sau. Error handling và metric
thresholds vẫn chưa chốt, không được suy ra từ lựa chọn thang điểm.

### Answer Evaluation — rubric đủ năm mức và prompt tối thiểu

User chọn phương án A ngày 2026-09-11. Mỗi metric có tiêu chí riêng cho đủ năm
mức; không để judge tự nội suy từ 1/3/5 hoặc chỉ hai đầu thang điểm.

| Điểm | Accuracy | Completeness | Relevance |
|---:|---|---|---|
| 5 | Hoàn toàn nhất quán với reference, không có sai lệch thực chất | Bao phủ toàn bộ thông tin cần thiết trong reference để trả lời câu hỏi | Trả lời trực tiếp, tập trung, không có nội dung thừa đáng kể |
| 4 | Đúng về ý chính, chỉ có sai lệch nhỏ không đổi kết luận | Bao phủ hầu hết nội dung cần thiết, chỉ thiếu chi tiết nhỏ | Chủ yếu trực tiếp, chỉ có ít nội dung thừa hoặc lặp |
| 3 | Đúng một phần nhưng có ít nhất một sai lệch thực chất; vẫn còn giá trị sử dụng | Bao phủ khoảng một nửa hoặc chỉ một phần các ý chính | Có trả lời câu hỏi nhưng lan man, lặp hoặc lệch trọng tâm đáng kể |
| 2 | Phần lớn sai hoặc gây hiểu sai, chỉ còn ít nội dung đúng | Chỉ nêu một phần nhỏ, thiếu phần lớn ý chính | Chỉ chạm một phần câu hỏi; phần lớn nội dung không liên quan |
| 1 | Sai hoàn toàn, mâu thuẫn ý chính hoặc không có câu trả lời đánh giá được | Không nêu được thông tin cần thiết hoặc không có câu trả lời | Không trả lời câu hỏi hoặc nội dung không liên quan |

Judge chạy một lần cho mỗi case với đúng ba nội dung `question`, generated
answer và `reference_answer`; output tối thiểu là ba số nguyên 1–5 cùng một
feedback ngắn. Ba tiêu chí được chấm độc lập. Prompt cấm dùng kiến thức ngoài
ba nội dung được cấp và không chứa retrieved context/evidence/citation.

Vì reference có thể không exhaustive, chi tiết thêm mà reference không xác
nhận cũng không phủ nhận không tự bị coi là lỗi Accuracy; nội dung thừa hoặc
lệch trọng tâm vẫn được phản ánh ở Relevance. Contract này chỉ đo chất lượng
answer so với reference, không claim groundedness hay citation correctness.
Không thêm nhiều judge passes, voting hoặc rubric theo category khi chưa có
consumer. Cách xử lý lỗi/timeout và thresholds vẫn là các quyết định riêng.

### Evaluation failures — không công bố partial aggregate

User chọn phương án A ngày 2026-09-11. Official overall và category
macro-average chỉ được tính/công bố khi đủ kết quả hợp lệ cho toàn bộ canonical
cases của run. Không loại case lỗi khỏi mẫu số và không gán điểm giả cho lỗi kỹ
thuật chỉ để hoàn tất aggregate.

Phân biệt hai loại outcome:

- retrieval đã thực thi thành công nhưng danh sách kết quả rỗng là một kết quả
  chất lượng hợp lệ: MRR@10, nDCG@10 và Keyword Coverage@10 đều bằng 0;
- generation đã thực thi thành công nhưng answer rỗng hoặc không có nội dung
  đánh giá được là một kết quả chất lượng hợp lệ: Accuracy, Completeness và
  Relevance đều bằng 1 theo rubric;
- lỗi kỹ thuật, timeout, generation call failure, judge failure hoặc judge
  output thiếu/sai kiểu/ngoài 1–5 không có metric hợp lệ. Run được đánh dấu
  `incomplete`, ghi derived `case_index`, question, stage và lỗi quan sát được,
  rồi case đó phải được chạy lại thành công trước khi có official aggregate.

Có thể hiển thị tiến độ và per-case outcomes đã hoàn tất để chẩn đoán, nhưng
không gọi trung bình trên phần thành công là official/partial metric. Không thêm
resume state, retry framework hoặc artifact audit phức tạp chỉ từ policy này;
cách thực thi trực tiếp sẽ được chốt trong plan. Thresholds vẫn là quyết định
riêng và không được suy ra từ failure policy.

### Metric thresholds — chưa đặt trước full-corpus baseline

User chọn phương án A ngày 2026-09-11. Full-corpus phase hiện tại không dùng
hard acceptance threshold và cũng không thêm diagnostic color bands cho sáu
metric. Report phải giữ exact MRR@10, nDCG@10, Keyword Coverage@10, Accuracy,
Completeness, Relevance, tổng số case và breakdown/count theo category để so
sánh các cấu hình trên cùng Golden.

Các ngưỡng xanh/vàng/đỏ quan sát được trong dashboard `rag_old_0` chỉ là
reference lịch sử và không được mang sang Hue như requirement. Chưa có baseline
toàn corpus để biện minh các mốc đó. Việc một run hoàn tất đầy đủ, Golden/schema
hợp lệ và phép so sánh giữ control vẫn là quality/acceptance contract riêng;
không gọi chúng là metric thresholds. Nếu sau benchmark có nhu cầu đặt gate,
đó là quyết định mới dựa trên evidence quan sát được.

### Authoring `keywords` — từ/cụm từ quan trọng và chính xác

User chọn phương án A ngày 2026-09-11 và yêu cầu bám sát bài học
`rag_old_0`: `keywords` là các từ/cụm từ quan trọng, chính xác dùng làm
keyword-substring proxy. Mỗi case có một danh sách không rỗng; mỗi phần tử phải:

- là một term hoặc phrase mang thực thể hay ý đáp án cần truy xuất;
- xuất hiện nguyên văn trong phần canonical corpus liên quan và được
  `reference_answer` hỗ trợ;
- dùng cách viết tiếng Việt canonical, gồm dấu và chi tiết chính xác; evaluator
  chỉ bỏ khác biệt hoa/thường, không tự thêm synonym hoặc accent normalization;
- không trùng keyword khác sau so sánh không phân biệt hoa/thường.

Ví dụ User đưa: với case nói đến Bánh ép 1992, keywords nên chứa thực thể quan
trọng như `Bánh ép`, và chứa tên đường/địa chỉ chính xác nếu địa chỉ là thông tin
được hỏi hoặc là ý cần có trong đáp án. Không dùng các từ chung như “quán”,
“địa điểm”, không chép cả câu và không thêm biến thể/synonym phòng xa.

Ba retrieval metrics tính điểm từng keyword rồi lấy mean trong case, nên không
tách một phrase có nghĩa thành nhiều token đồng nghĩa hoặc lặp nhiều cách viết
để vô tình tăng trọng số một fact. Không có hard keyword count: author chọn bộ
nhỏ nhất vẫn đại diện đủ các ý chính cần truy xuất, rồi content reviewer đối
chiếu từng keyword với corpus và reference answer. Đây vẫn là relevance proxy,
không phải nhãn exhaustive cho mọi relevant chunk.

### Complexity reset tiếp theo — bỏ `case_id` khỏi canonical

User chọn phương án A ngày 2026-09-11 sau khi đối chiếu lại consumer. Quyết định
này supersede mọi đoạn trước mô tả `case_id` là required field. Canonical Golden
có đúng bốn required fields: `question`, `keywords`, `reference_answer`,
`category`. Không lưu `case_id` trong authoring record hay canonical record.

Sáu metric không consume ID; một canonical ordered file là đủ cho scope hiện
tại. Khi chạy, evaluator derive `case_index` từ zero-based row position và có
thể báo kèm question cho progress/error. Khi author/review, partition path và
row position xác định record đang xét. `case_index` không được ghi vào Golden,
không phải stable identifier và không được hứa giữ nguyên nếu dataset đổi thứ
tự hoặc nội dung.

Không tạo mapping/ID tạm chỉ để bù cho field đã bỏ. Nếu tương lai xuất hiện
consumer thật sự cần join per-case qua nhiều phiên bản Golden, việc thêm stable
ID là một quyết định schema mới. Trong scope hiện tại, smoke deep-equal và
deterministic merge không phụ thuộc `case_id`.

### Category — chọn theo thao tác chính và review từng case

User chọn phương án A ngày 2026-09-11. Implementer gán đúng một category sơ bộ
dựa trên chính câu hỏi và thao tác chính cần để trả lời, không phân loại theo
keyword bề mặt, domain hoặc source location. Định nghĩa dùng chung cho P7:

| Category | Ý định chính của câu hỏi |
|---|---|
| `direct_fact` | Lấy một fact hoặc nhóm fact nhỏ, trực tiếp về một đối tượng; là nhãn mặc định khi không có thao tác chuyên biệt hơn |
| `temporal` | Hỏi thời điểm, khoảng thời gian, trình tự hoặc thay đổi theo thời gian |
| `comparative` | So sánh rõ hai hay nhiều đối tượng, lựa chọn hoặc thời điểm |
| `numerical` | Kết quả chính là số lượng, giá, range, khoảng cách hoặc phép tính; mốc/ngày lịch sử thuộc `temporal` nếu thời gian là ý định chính |
| `relationship` | Làm rõ quan hệ, vai trò, phụ thuộc hoặc liên hệ giữa các thực thể/khái niệm |
| `spanning` | Kết hợp nhiều ý/fact hữu hạn được câu hỏi yêu cầu rõ |
| `holistic` | Tổng hợp rộng, giải thích tổng quan, lập kế hoạch hoặc đưa khuyến nghị trên một chủ đề |

Khi một câu hỏi có nhiều đặc điểm, chọn nhãn mô tả thao tác chính. Dùng
`spanning` cho tập fact hữu hạn và `holistic` cho tổng hợp rộng; không tạo
precedence máy móc hoặc multi-label. Label ban đầu là provisional: User và
Reviewer đọc từng question rồi có thể giữ, reclassify, sửa/cập nhật hoặc xóa.
Category vẫn chỉ phục vụ count/breakdown, không đổi scoring.

### Authoring và content review Golden

User giao Implementer tạo các working JSONL từ curated corpus và tài liệu được
cung cấp. Implementer được web-search để học cách tạo câu hỏi và dữ liệu tự
nhiên, có giọng người, rõ ràng, dễ hiểu, không máy móc. Web research chỉ phục vụ
phương pháp authoring: không được đưa fact ngoài corpus vào question/keywords/
reference answer và không trở thành closed-world ground truth.

Implementer phải tự review để câu hỏi tự nhiên, có nghĩa rõ, answerable từ
corpus; reference answer đúng/đủ theo câu hỏi; keywords theo contract đã chốt;
category sơ bộ suy từ chính câu hỏi. Sau khi JSONL được tạo, User và Reviewer
đọc từng case. Mỗi case nhận một quyết định quan sát được: giữ, yêu cầu sửa/cập
nhật, đổi category hoặc xóa. Implementer thực hiện correction và trả lại phần
bị ảnh hưởng; Reviewer không sửa Golden thay Implementer. Chỉ partition đã qua
content review mới đủ điều kiện merge.

### P7 quality gate — đóng tuần tự từng partition

User chọn phương án A ngày 2026-09-11. Author/review đi theo thứ tự `foods`,
`heritages`, `festivals`, `performing_arts`, `travel_places`,
`travel_services`, `travel_tickets`; không author sẵn toàn bộ batch trước khi
nhận feedback của partition hiện tại.

Mỗi partition đi qua một vòng trực tiếp:

1. Implementer author từ corpus/tài liệu được giao và self-review toàn bộ case;
2. User và Reviewer đọc từng case, gom quyết định giữ, sửa/cập nhật, reclassify
   hoặc xóa;
3. Implementer thực hiện correction và trả lại exact cases bị ảnh hưởng;
4. Reviewer kiểm correction; User xác nhận partition khi không còn required
   change;
5. chỉ sau confirmation mới bắt đầu partition kế tiếp.

Không đặt hard case quota, không padding và không merge partition chưa đạt.
Không tạo approval database, per-case state machine hoặc workflow bổ sung;
review findings và confirmation trong handoff/report hiện hành là đủ. Sau khi
cả P7 đạt, mới chạy deterministic merge theo contract sẽ chốt riêng.

### Canonical paths — `evaluation/` theo từng nhánh rồi merge tập trung

User chọn cấu trúc theo convention Foods ngày 2026-09-11. Mỗi P7 có một working
Golden trong thư mục `evaluation/` của chính nhánh:

```text
knowledge-base-hue/foods/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/festivals/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/performing_arts/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/places/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/services/evaluation/golden_full_corpus_authoring.jsonl
knowledge-base-hue/travel/tickets/evaluation/golden_full_corpus_authoring.jsonl
```

Việc tạo sáu thư mục `evaluation/` mới và các JSONL chỉ xảy ra sau spec/plan
approval; docs-only session này không tạo chúng. Foods V2/V3/smoke lịch sử giữ
nguyên và case dùng lại phải copy/review vào working file mới.

Sau khi bảy partition được User xác nhận tuần tự, deterministic merge tạo đúng
một official file:

```text
knowledge-base-hue/evaluation/golden_full_corpus.jsonl
```

Smoke đích nằm cạnh canonical tại
`knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl`. Working files được retire khỏi evaluator path sau merge nhưng vẫn là
artifact authoring/review, không phải benchmark độc lập. Không tạo central
`authoring/` folder hoặc phân tán final file vào root `evaluation/data/`.

### Smoke selection — 10 canonical rows chọn thủ công

User chọn phương án A ngày 2026-09-11. Sau khi canonical merge hoàn tất, chọn
thủ công đúng 10 records cho smoke. Mỗi P7 phải có ít nhất một case; ba vị trí
còn lại ưu tiên giúp phủ được nhiều category nhất có thể. Đây là coverage cho
bounded check, không tạo quota ngược cho Golden chính.

Implementer đề xuất 10 rows; User và Reviewer đọc/duyệt danh sách. Smoke copy
nguyên record, deep-equal với canonical và giữ thứ tự tương đối của canonical.
Không chỉnh question/keywords/reference/category riêng trong smoke. Nếu một row
được chọn bị sửa, xóa hoặc thay thứ tự trong canonical, smoke phải được tạo lại
từ canonical và kiểm deep equality.

Smoke là đường chạy nhanh, không phải dev/test split, không thay full-corpus
official evaluation và không được dùng để quyết định chất lượng benchmark thay
full set. Chọn thủ công một lần sau merge; không thêm random seed, sampling
framework hoặc metadata đánh dấu smoke vào canonical records.

### Deterministic merge — nối P7 rồi xáo bằng fixed seed

User chọn phương án A và bổ sung yêu cầu xáo sau merge ngày 2026-09-11. Merge
đọc đúng bảy working files đã approved theo thứ tự P7, giữ thứ tự row trong mỗi
file và kiểm `partition` authoring khớp nhánh. Merge strip `partition`; mỗi row
đích có đúng bốn fields theo thứ tự `question`, `keywords`, `reference_answer`,
`category`.

Trước khi ghi, validate schema/content rules đã chốt và chặn exact duplicate
question sau trim + so sánh không phân biệt hoa/thường. Semantic near-duplicate
được xử lý ở manual content review, không thêm similarity/dedup model vào merge.
Sau khi concat, dùng deterministic shuffle với fixed seed công khai `42`; cùng
exact inputs, input order và seed phải tạo byte-identical UTF-8 JSONL. Không
global sort, round-robin, ID, manifest, checksum, version store hoặc package
state. Working files vẫn được retire khỏi official evaluator path sau merge.

Smoke được chọn từ canonical đã xáo và giữ thứ tự tương đối của canonical.
Reviewer kiểm canonical là đúng hợp của bảy approved partitions sau khi strip
authoring metadata, không tự review lại content đã đóng nếu không có sai lệch.

### Full evaluation sau khi Golden hoàn tất

User yêu cầu: khi toàn bộ Golden đã được author/review, merge và xáo hoàn tất,
chạy full canonical file cho cả Retrieval Evaluation và Answer Evaluation. Tập
thực tế được kỳ vọng trong planning range 150–200 nhưng không padding hoặc loại
case tốt để ép range.

Full run bao gồm MRR@10, nDCG@10, Keyword Coverage@10, Accuracy, Completeness và
Relevance trên mọi canonical row; smoke không thay full run. Complete-run policy
và no-threshold decision tiếp tục áp dụng. Đây là acceptance requirement cho
implementation/benchmark plan sau, không cấp quyền chạy model/API/evaluation
trong docs-only session. Exact pipeline candidates, provider/model và run order
vẫn phải được chốt trước plan approval.

### Qdrant collection strategy — isolated theo embedding candidate

User chọn phương án A ngày 2026-09-11 và chấp nhận nhiều collection khi có
consumer benchmark thật. Active Foods collection và dense-only Foods candidate
giữ read-only; full-corpus không overwrite chúng.

Baseline dùng một isolated collection cho mỗi dense embedding candidate:
E5-small, E5-base và HuyDang, nên tập candidate ban đầu có ba full-corpus
collections. Nếu thực hiện controlled representation A/B cho cả ba model và giữ
hai index đồng thời, nhánh B có thể thêm ba collections. Decision #2 không đặt
hard cap cho giai đoạn thử nghiệm: có thể tạo thêm fresh collection khi mỗi
collection trả lời một candidate/variant đã được duyệt.
Isolation là lựa chọn benchmark/lifecycle của User, không phải giới hạn tuyệt
đối của Qdrant: named-vector schema có thể biểu diễn nhiều vector names. Không
gộp candidates trong scope hiện tại vì việc tách giúp tránh lẫn model space,
representation, rebuild evidence và cutover state.
Không nhân collection theo mọi pipeline component:

- mỗi candidate collection lưu dense và sparse named vectors trên cùng points;
  hybrid candidate là sparse query consumer thật, nên sparse không phải dữ liệu
  dự phòng;
- BM25/TF-IDF dùng lexical index/state ngoài Qdrant;
- reranker, fusion/scoring và generator không có corpus collection riêng.

User xác nhận Decision Queue #1 ngày 2026-09-11: baseline A query dense
candidates rồi BM25 local rescoring và được giữ làm comparison control; đây
không phải true hybrid candidate retrieval. Hybrid candidate query dense và
sparse độc lập trên cùng indexed points rồi fusion. Exact fusion/reranker,
failure behavior và runtime default vẫn chờ Decision #4 và benchmark; sparse
vocabulary/token-index mapping phải reproducible và coupled với indexed points.

Không nhân collection theo component hoặc dự phòng. Sau benchmark, Reviewer đề
xuất giữ khoảng 1–3 collections tốt nhất; đây không phải quota/winner count chốt
trước kết quả. Fresh-by-default vào target mới/rỗng và không in-place reconcile.
Exact replacement hoặc cleanup là thao tác riêng: phải verify exact target, có
authority và không đụng Foods. Collection names, payload và cutover vẫn chờ
Decision Queue, written spec và approved plan.
Không có quyền tạo/mutate collection trong session này.

### Trạng thái survey toàn project `llm_rag` — complexity reset

Implementer nộp initial report ngày 2026-09-11. Reviewer đọc đủ report và kiểm
tập trung source/config/backend/frontend, kết luận `changes_requested` tại:

```text
reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md
```

Các kết luận đã xác nhận và không mở lại trong correction:

- active code/config của `llm_rag` tham chiếu một configured collection, default
  `nmk_chatbot_collection`, chứa named dense+sparse trên cùng points;
- request-time chỉ query `using="dense"`; sparse stored vector không có query
  consumer; BM25 chỉ rescoring dense candidates trong memory;
- CrossEncoder, fusion và scoring không cần collection;
- source/config không chứng minh live Qdrant chỉ có đúng một collection;
- các số 450 chunks, vocabulary 1.486 và avg length 48,84 là historical saved
  evidence, không phải fresh run của survey;
- không copy random UUID/non-idempotent upsert, unverified existing schema,
  unnormalized dense+BM25 fusion, non-persisted sparse vocabulary hay E5 input
  thiếu query/passage prefix sang Hue.

Initial report không được approved. Sau bốn verdict `changes_requested`, report
885 dòng vẫn còn RR11 Major về config consumer/anchor và đã chạm correction
ceiling. Reviewer kích hoạt complexity reset; User xác nhận ngày 2026-09-11.
Report dài được đóng băng working/non-canonical và không có Correction 5.
Verified Architecture Extraction ngắn đã được tạo theo
`handoff_prompt/LLM_RAG_VERIFIED_ARCHITECTURE_EXTRACTION_PROMPT.md`, qua hai
correction và independent Reviewer review. User xác nhận closure ngày
2026-09-11; artifact là approved evidence companion. Report 885 dòng vẫn đóng
băng working/non-canonical.

### Decision queue sau Verified Architecture Extraction

Closure extraction đã được User xác nhận ngày 2026-09-11. Queue hiện hoạt động ở
mục #6. Mỗi lượt hỏi User một quyết định có consumer hiện hành; ghi câu trả lời
vào file này và guide trước khi hỏi câu tiếp theo.

1. **Đã chốt 2026-09-11 — Lexical baseline/sparse consumer:** baseline A dùng
   dense candidate retrieval + BM25 local rescoring. Hybrid là controlled
   candidate có sparse query consumer thật; candidate collections lưu cả dense
   và sparse vectors. Benchmark so hai modes trước khi đề xuất runtime default.
2. **Đã chốt 2026-09-11 — Index lifecycle:** fresh-by-default vào target
   mới/rỗng, cho phép nhiều collections phục vụ các experiment candidates; không
   in-place reconcile. Exact replacement/cleanup cần target và approval riêng.
   Sau benchmark đề xuất giữ khoảng 1–3 collections tốt nhất.
3. **Đã chốt 2026-09-11 — Payload/source locator:** Qdrant point giữ point ID và
   named dense/sparse vectors ở trường chuẩn; payload chỉ có `search_text`,
   `source`, `title`, `heading_path`, `evidence_parts`. Không lặp metadata cấp
   collection/file hoặc field chưa có consumer.
4. **Đã chốt 2026-09-11 — Retrieval/fusion/reranker matrix:** staged matrix. Với
   mỗi dense model, so baseline A và native hybrid bằng RRF; chỉ retrieval
   finalists so một reranker với no-rerank control. Dùng retrieval metrics cho
   stage đầu và đủ sáu metrics cho end-to-end finalists; báo exact results,
   không composite hoặc winner/default trước evidence. Component failure làm run
   incomplete; không silent fallback.
5. **Đã chốt 2026-09-11 — Representation B timing:** staged finalists. Hoàn tất
   representation A và chọn retrieval/model finalists trước; sau đó tạo B bằng
   API thật, build fresh index thật và chạy full-corpus A/B thật trên finalists,
   giữ các biến nền tương đương. User chấp nhận API/index cost; execution vẫn
   chờ Spec/Plan approval.
6. **Đang chốt — Context/generator/API/citation/frontend:** #6a đã chốt strict
   minimal `{answer,sources}` và typed non-2xx error; #6b chốt token-budget động
   theo profile nhưng cố định trong run; #6c chốt `qwen/qwen3.5-9b` qua
   OpenRouter với một upstream pinned cho representation B và answer generation,
   còn evaluation judge dùng `gpt-5.4-mini` qua OpenAI API. #6d chốt profile
   Qwen `temperature=0`, B output 256, answer context/reserve/margin
   16384/2048/512 và timeout 90 giây; agentic dùng profile/contract riêng. #6e
   chốt UI inline với citation focus tới source cards dưới answer. Decision #6
   đã đủ đầu vào cho Written Spec.
7. **Metric thresholds/cutover:** chỉ quyết định sau full-corpus baseline thật;
   không suy threshold/composite từ Foods hoặc historical reference.

Không thêm alias, manifest, checksum, migration framework, cleanup automation,
generic provider abstraction hoặc metadata chỉ để dự phòng trước khi có
consumer/failure/risk cụ thể. Không hỏi lại A/B boundaries, Top-5, one-shot,
isolated/fresh-by-default collections không hard cap experiment, Foods read-only
hoặc Golden contracts đã chốt.

### Chính sách tham khảo `rag_old_0`

Khảo sát source/notebook/transcript `rag_old_0` đã hoàn tất, qua hai correction,
independent Reviewer review và User approval. Từ phiên sau, dùng hai report sau
làm nguồn tham khảo đã tổng hợp:

- `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_2026_09_10.md`;
- `reports/full_corpus_rag_old_0_evaluation_simplicity_survey_codex_review_2026_09_10.md`.

Không đọc hoặc phân tích lại thư mục `/home/minhhieu/llm_rag/tai_lieu/rag_old_0`
mặc định. Chỉ mở lại source khi User yêu cầu hoặc xuất hiện câu hỏi kỹ thuật mới
mà hai report không đủ trả lời; không mở lại findings đã đóng.
