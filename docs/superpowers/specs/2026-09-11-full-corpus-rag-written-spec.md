# Full-corpus RAG Written Spec

```text
Status: approved by User
Date: 2026-09-11
Runtime authorization: none
Implementation Plan: approved by User 2026-09-11; Phase 3 active
Sequential phase workflow amendment: approved by User 2026-09-11; terminology updated 2026-09-12
```

## 1. Mục tiêu và ranh giới

Spec này mở rộng Hue Foods RAG MVP thành RAG một lượt cho toàn bộ curated corpus
Huế, với ingestion có locator, dense/sparse retrieval có benchmark kiểm soát,
citation nguồn nguyên văn, frontend tối giản và evaluation full-corpus.

Năm domain sản phẩm là `foods`, `heritages`, `festivals`, `performing_arts` và
`travel`; `travel` gồm `places`, `services`, `tickets`. Hệ thống trả lời tiếng
Việt trong closed-world corpus. Thiếu bằng chứng thì trả phần có căn cứ hoặc nói
không đủ thông tin; không dùng kiến thức ngoài corpus để lấp chỗ trống.

Ngoài scope:

- multi-turn/session/personalization, streaming và conversational memory;
- Agentic RAG, tool use/search, planner, workflow state hoặc agentic UI;
- incremental indexing, alias/migration/version registry và cleanup tự động;
- groundedness/citation judge claim-level hoặc Golden source-span annotations;
- metric threshold, composite score và runtime winner trước baseline thật.

Agentic RAG về sau phải có profile và contract riêng cho tool schemas/results,
plan/state, số bước/tool calls, timeout/failure, tổng token/thời gian/chi phí và
provenance. Không dùng ngân sách one-shot trong spec này làm ngân sách agentic.

Spec là contract cần User duyệt; nó không cấp quyền sửa runtime, gọi API/model,
ghi Qdrant, tạo Golden hoặc chạy benchmark.

## 2. Luồng end-to-end

```text
curated Markdown
→ deterministic discovery + LF normalization
→ Markdown blocks có source positions
→ condition attachment + semantic grouping/splitting
→ representation A (và B có kiểm soát cho finalists)
→ dense + sparse vectors trong isolated Qdrant collection
→ baseline hoặc native-hybrid retrieval
→ optional finalist reranking
→ whole-chunk token packing, tối đa 5 primary chunks
→ Qwen one-shot answer + citation validation
→ {answer, sources}
→ inline citation/source-card UI
```

Mọi benchmark chính thức dùng dữ liệu/index/model/API thật. Mock hoặc synthetic
chỉ được dùng cho technical tests, không phải official quality evidence.

## 3. Corpus discovery và tính nhất quán nguồn

Discovery chỉ lấy curated Markdown thuộc năm domain, theo thứ tự path ổn định.
Loại các nhánh `evaluation`, `_source-dumps`, `meta`, file quản lý và section
source-tracking đã chốt; không loại answer content chỉ vì heading có tính quản
lý. Exact include/exclude paths phải được liệt kê trong Implementation Plan.

Mỗi file được đọc UTF-8 strict. CRLF và CR được đổi thành LF trước parsing,
locator và hashing. Không Unicode-normalize, bỏ dấu, gộp whitespace, xóa dòng
trống hoặc sửa Markdown trong evidence.

Ingestion tạo một build record tối thiểu, chỉ gồm dữ liệu có consumer startup:

- tập source paths tương đối đã ingest và SHA-256 của text LF UTF-8;
- collection target, dense model/vector size và representation A/B;
- trạng thái build hoàn tất.

Build record không phải version registry hoặc migration framework. Khi startup,
discovery và hash được tính lại. Thêm/xóa/đổi tên file hoặc đổi text LF làm
corpus stale; backend chưa phục vụ chat và trả lỗi yêu cầu ingest lại. Chỉ đổi
kiểu newline nhưng text LF giống nhau không làm stale. Citation luôn dùng
evidence đã lưu cùng build, không đọc nội dung file mới sửa để thay thế.

## 4. Parsing, chunking và locator

Parser dùng `markdown-it-py` với table support. H1 là `title`; intro trước H2
được giữ; `heading_path` gồm các heading tổ tiên và hiện tại, không lặp H1.
Heading là tín hiệu cấu trúc, không phải lệnh tạo một chunk cho mọi section.

Grouping ưu tiên giữ đơn vị cùng chủ đề và đủ nghĩa:

- paragraph dài chỉ chia tại ranh giới câu trong source;
- list giữ quan hệ cha/con và lặp nhãn cha cần thiết;
- table giữ header, đơn vị, đối tượng/nhà cung cấp và điều kiện áp dụng;
- không trộn phương án loại trừ nhau hoặc sibling độc lập để lấp token budget;
- không cắt giữa câu, list item hoặc table cell; không dùng overlap cố định;
- dòng chỉ có ảnh và separator không tạo chunk riêng.

Các quan hệ điều kiện không suy đoán chỉ từ khoảng cách. Một JSON chỉ dẫn nhỏ
ngoài corpus có record `{source, condition, targets}`; mỗi selector dùng
`{heading_path, block_type, exact_text}`. Selector phải match đúng một block
trong đúng file; missing/duplicate/mismatch là preview error chặn ingestion.
Không tạo DSL, regex engine, graph hoặc fallback “match đầu tiên”.

Các rule đã biết phải được bảo vệ: lead Ca Huế áp dụng đúng các bảng thuộc phạm
vi; “Không bao gồm” của một phương án không lan sang phương án khác; intro hạn
mức của bảng dự toán được giữ cùng nội dung cần nó.

Mỗi evidence part có schema:

```json
{"role":"body|header|condition","start":0,"end":1,"text":"..."}
```

Offsets là zero-based Unicode code points `[start,end)` trên source LF. Mỗi part
phải thỏa `source_text[start:end] == text`. Evidence được slice từ source, không
lấy từ HTML render hoặc parser text đã biến đổi. Các spans không liên tục phải
là các parts riêng; UI không giả chúng thành một substring liên tục.

Chunk ID nội bộ serialize deterministic cặp `(source, chunk_ordinal)`, ordinal
bắt đầu từ 0 trong mỗi file. Qdrant point ID là UUID5 từ chunk ID với namespace
cố định. ID có thể đổi khi edit/rechunk; locator mới là căn cứ truy nguồn.

Trước embedding, preview phải liệt kê mọi nhóm tối thiểu vượt input limit theo
file/mục và count/limit từng model. Còn bất kỳ lỗi nào thì chặn toàn ingestion;
không ingest một phần, truncate, bỏ evidence hoặc tự sửa corpus/model.

## 5. Representation và Qdrant point contract

Một Qdrant point có:

- point ID chuẩn của Qdrant;
- hai named vectors `dense` và `sparse`;
- payload đúng năm field `search_text`, `source`, `title`, `heading_path`,
  `evidence_parts`.

`source` là POSIX path tương đối `knowledge-base-hue/`. Không lặp point ID,
vectors, domain/subdomain, source hash, model/representation ID, token count,
timestamp, version hoặc score trong payload. Domain suy từ path; source hash
thuộc build/file; model và representation thuộc collection/build.

Representation A dựng `search_text` từ title, heading path và evidence parts.
Nhãn và separator chỉ phục vụ trình bày/tìm kiếm, không tự là evidence. Citation
đọc `evidence_parts`, không đọc text ghép như bằng chứng.

Full representation phải được tokenize bằng preprocessing thực của cả ba dense
candidates, gồm prefix/special tokens, với `truncation=False`. Chỉ xuất chunk
khi vừa cả E5-small, E5-base và HuyDang; không đặt một character limit thay cho
kiểm tokenizer.

Representation B giữ nguyên chunk A và `evidence_parts`, rồi dùng
`qwen/qwen3.5-9b` sinh một đoạn context tìm kiếm cô đọng từ chính nội dung A.
Output cap là 256 tokens. Phần sinh thêm chỉ bổ sung vào `search_text` để tạo
vectors/retrieval; không là evidence, citation hoặc Golden truth và không tạo
vector type mới. Chỉ dùng B nếu input hoàn chỉnh sau bổ sung vẫn vừa cả ba dense
tokenizers; nếu không, point tương ứng giữ representation A nguyên vẹn.

## 6. Collection và ingestion lifecycle

Mỗi dense embedding candidate dùng một isolated full-corpus collection. Tập A
ban đầu gồm E5-small, E5-base và HuyDang. Collection của một candidate chứa cả
dense/sparse vectors vì native hybrid là sparse consumer thật. Không tạo
collection riêng cho BM25, fusion, reranker hoặc generator.

Mỗi experiment build mặc định ghi vào target mới hoặc rỗng. Target không rỗng
bị từ chối nếu chưa có exact replacement approval. Không reconcile/upsert lẫn
với điểm cũ và không tự xóa stale points. Full rebuild diễn ra khi backend dừng.

Không có hard cap số collection trong giai đoạn thử nghiệm nếu mỗi collection
gắn với candidate/variant đã duyệt. Sau benchmark, Reviewer đề xuất khoảng 1–3
collection cần giữ dựa trên evidence. Replacement hoặc cleanup luôn cần exact
targets và quyền riêng; không tự động. Mọi Foods collection hiện hành read-only.

## 7. Retrieval, fusion và reranking

Hai retrieval treatments bắt buộc cho mỗi dense model trên representation A:

1. Baseline A: dense retrieval tạo candidate pool; BM25 local chỉ chấm lại các
   dense candidates; dense rank và BM25-local rank hợp nhất bằng RRF trong pool.
   Đây không phải native hybrid candidate retrieval.
2. Native hybrid: dense và sparse query độc lập trên collection, sau đó hợp nhất
   bằng RRF.

Candidate depth, RRF constant và tie-break phải cố định trong một run và ghi
trong report; Plan khóa exact values công bằng giữa treatments. Kết quả báo Top
10 cho retrieval metrics. Không silent fallback giữa baseline và hybrid; lỗi
một component làm run incomplete.

Reranker là capability MVP nhưng chỉ được so sau khi có retrieval finalists.
Candidate local hiện hành là `cross-encoder/ms-marco-MiniLM-L-6-v2`; compare một
reranker treatment với no-rerank control, giữ các biến khác tương đương. Nếu
query/chunk pair vượt input limit, bỏ reranking cho toàn request và giữ nguyên
pre-rerank order; không truncate hoặc rerank một phần.

## 8. Context packing và generation

Sau final rank, context builder xét tối đa 5 primary chunks. Profile Qwen khóa:

```yaml
model: qwen/qwen3.5-9b
provider: OpenRouter
temperature: 0
context_limit: 16384
reserved_output_tokens: 2048
safety_margin: 512
timeout_seconds: 90
automatic_retry: false
automatic_failover: false
```

Không set thêm sampling knobs. Một upstream provider được preflight, pin và ghi
trong Plan/report trước mỗi approved benchmark run. Availability được kiểm lại
tại thời điểm thực thi; không tự đổi provider giữa calls/runs.

Mỗi request trừ token thực của system prompt, query, format/citation overhead,
output reserve và safety margin. Pack nguyên primary chunks theo final rank.
Khi chunk tiếp theo không vừa thì dừng; không skip chunk hạng cao để lấy chunk
thấp hơn, không truncate hoặc summarize evidence. Nếu chunk đầu tiên không vừa,
trả typed configuration/input error.

Generator trả một lần, không streaming. Prompt chỉ cho phép dùng evidence đã
pack. Evidence mâu thuẫn về cùng đối tượng/thời điểm/điều kiện phải được nêu cùng
citation tương ứng, không tự chọn theo rank, filename hoặc kiến thức sẵn có.

Nhánh lấy thêm điều kiện gốc sau Top-5 là experiment hậu-baseline, không mặc định
trong treatment đầu. Khi được duyệt, điều kiện gốc đi cùng primary chunk cần nó,
được gộp trùng và vẫn nằm trong token budget; không trộn biến này với
representation B trong phép so sánh đầu tiên.

## 9. Public API và citation integrity

Giữ endpoint one-shot `POST /api/chat` với request:

```json
{"query":"Câu hỏi tiếng Việt"}
```

Sau trim, `query` phải có từ 1 đến 500 ký tự. Whitespace-only hoặc vượt giới
hạn là `invalid_request`; backend không tự cắt query.

Success HTTP 200 có đúng contract:

```json
{
  "answer": "... [1] ...",
  "sources": [
    {
      "id": 1,
      "title": "Tên tài liệu",
      "heading_path": ["Mục", "Tiểu mục"],
      "excerpts": ["Đoạn nguyên văn thứ nhất", "Đoạn nguyên văn thứ hai"]
    }
  ]
}
```

Citation IDs là số response-local. Chỉ sources được answer tham chiếu mới được
trả. Backend ánh xạ `[n]` tới evidence thật đã cấp cho generator và dựng excerpts
từ `evidence_parts`; không tin source text do model tự viết. Validation bảo đảm
ID tồn tại, mỗi source được dùng và không có citation mồ côi. Nó không thay thế
claim-level groundedness evaluation.

Không evidence là success 200 với câu trả lời nói không đủ thông tin và
`sources: []`; đây không phải technical failure. Technical/integrity failures
dùng đúng envelope `{"error":{"code":"...","message":"..."}}`:

| HTTP | `code` | Điều kiện |
|---:|---|---|
| 422 | `invalid_request` | query thiếu/rỗng/vượt request contract |
| 409 | `corpus_reingest_required` | build thiếu, chưa hoàn tất hoặc corpus stale |
| 503 | `retrieval_unavailable` | dense/sparse/BM25/reranker dependency lỗi |
| 502 | `generation_unavailable` | OpenRouter/upstream/generation lỗi |
| 500 | `context_budget_error` | primary chunk đầu không thể vừa fixed profile |
| 500 | `citation_integrity_error` | answer/source mapping không hợp lệ |
| 500 | `internal_error` | lỗi không phân loại khác |

Không partial success, warning schema, silent fallback, automatic repair/retry
hoặc debug trong public message. Không trả machine path, chunk ID, hash,
model/provider ID, offsets, vectors, scores, token usage hoặc raw payload.

## 10. Frontend contract

UI inline tối giản gồm một ô câu hỏi và nút gửi. Trong khi chờ, hiển thị loading
và ngăn submit trùng. Success render answer Markdown an toàn, không thực thi
HTML/script từ model hoặc corpus.

Mỗi `[n]` là control keyboard-accessible. Click/activate cuộn và chuyển focus
tới source card cùng ID ngay dưới answer. Card hiển thị title, heading path và
từng excerpt riêng; không ghép excerpts rời nhau thành một đoạn liên tục.

Typed error hiển thị message và nút thử lại thủ công, giữ câu hỏi để người dùng
không phải nhập lại. Không streaming, source drawer/modal, chat history/session,
debug/score/token panel hoặc agentic tool/plan UI.

## 11. Golden và evaluation contract

Authoring tuần tự theo P7: `foods`, `heritages`, `festivals`,
`performing_arts`, `travel_places`, `travel_services`, `travel_tickets`. Mỗi
partition được Implementer author/self-review, rồi User và Reviewer review từng
case; chỉ khi partition được xác nhận mới sang partition tiếp theo.

Working files nằm trong `evaluation/golden_full_corpus_authoring.jsonl` của từng
nhánh tương ứng. Planning target toàn bộ là 150–200 cases nhưng không là quota:
không padding case yếu để đạt số và không loại case tốt chỉ để ép tổng.

Working rows có `partition`; canonical row sau merge có đúng bốn field theo thứ
tự `question`, `keywords`, `reference_answer`, `category`. Không có `case_id`,
`expected_claims`, evidence/source spans hoặc chunk IDs. Category thuộc đúng một
trong `direct_fact`, `temporal`, `comparative`, `numerical`, `relationship`,
`spanning`, `holistic` và chỉ phục vụ count/breakdown.

| Category | Thao tác chính |
|---|---|
| `direct_fact` | lấy một fact hoặc nhóm fact nhỏ về một đối tượng |
| `temporal` | thời điểm, khoảng thời gian, trình tự hoặc thay đổi theo thời gian |
| `comparative` | so sánh rõ hai hay nhiều đối tượng/lựa chọn/thời điểm |
| `numerical` | số lượng, giá, range, khoảng cách hoặc phép tính là đáp án chính |
| `relationship` | quan hệ, vai trò, phụ thuộc hoặc liên hệ |
| `spanning` | kết hợp một tập hữu hạn nhiều fact được hỏi rõ |
| `holistic` | tổng hợp rộng, lập kế hoạch hoặc khuyến nghị |

Keywords là danh sách không rỗng các từ/cụm từ nguyên văn, cụ thể, được
reference answer hỗ trợ. Matching là substring không phân biệt hoa/thường;
không synonym expansion, bỏ dấu, keyword chung chung, duplicate hoặc padding.

Sau khi cả P7 approved, merge theo thứ tự P7, giữ row order nội partition, strip
`partition`, kiểm câu hỏi không trùng sau trim/casefold rồi deterministic shuffle
seed 42. Cùng inputs/order/seed phải sinh canonical byte-identical. Canonical:
`knowledge-base-hue/evaluation/golden_full_corpus.jsonl`.

Smoke có đúng 10 canonical rows, mỗi P7 ít nhất một case và phủ nhiều category
nhất có thể; rows deep-equal và giữ thứ tự tương đối trong canonical. User và
Reviewer duyệt selection. Smoke không phải split/benchmark và không thay full
evaluation. Foods Golden V2/V3 lịch sử không bị sửa.

Official retrieval metrics là keyword-proxy MRR@10, nDCG@10 và Keyword
Coverage@10. Answer metrics là Accuracy, Completeness, Relevance, mỗi metric là
số nguyên 1–5, chấm độc lập bằng `gpt-5.4-mini` qua OpenAI API. Judge mỗi case chỉ
nhận question, generated answer và reference answer; không dùng kiến thức ngoài
prompt. Đây là answer-reference evaluation, không phải citation groundedness.

Judge profile giữ `temperature=0` và output cap 600 tokens như evaluator hiện
hành; exact request timeout được khóa trong Plan. Một prompt/case trả đúng ba số
nguyên và feedback ngắn. Mức 5 là hoàn toàn đúng/đủ/trực tiếp; 4 chỉ có thiếu
hoặc lệch nhỏ; 3 đúng/đủ một phần hoặc lệch trọng tâm đáng kể; 2 phần lớn
sai/thiếu/lạc đề; 1 sai hoàn toàn, không đủ nội dung hoặc không trả lời. Ba tiêu
chí được chấm độc lập, không gộp thành một điểm.

Mỗi metric aggregate bằng macro-average theo case; báo count và category
breakdown. Không micro/weighted/composite score. Retrieval thành công nhưng
không trả kết quả nhận 0; generation thành công nhưng answer rỗng nhận 1 cho ba
answer metrics. Technical/timeout/judge/schema failure làm run `incomplete`;
không chế điểm, bỏ case hoặc công bố partial aggregate là official.

## 12. Experiment sequencing và cutover gate

1. Build representation A thật cho ba dense candidates.
2. Với mỗi dense model, chạy baseline A và native hybrid; báo ba retrieval
   metrics chính xác, không composite/threshold.
3. Reviewer dựa trên kết quả để đề xuất retrieval/model finalists; User xác nhận
   trước stage kế tiếp.
4. Trên finalists, so một reranker với no-rerank, giữ biến nền tương đương.
5. Tạo representation B bằng API thật và fresh indexes thật chỉ cho finalists;
   chạy controlled A/B giữ model/retrieval/fusion/reranker không đổi.
6. Chạy end-to-end finalists trên full canonical Golden và báo đủ sáu metrics,
   case counts, category breakdown, run completeness, model/provider/settings.
7. Reviewer đề xuất winner, khoảng 1–3 collections cần giữ và cutover dựa trên
   exact results; User duyệt trước mọi runtime switch hoặc cleanup.

Không đặt pass/fail threshold, diagnostic bands hoặc winner trước baseline thật.
Metric thresholds/cutover rule cụ thể là post-baseline decision, không phải phần
User đang duyệt trước execution.

## 13. Acceptance contract cho implementation sau này

Implementation chỉ có thể được chấp nhận khi approved Plan chứng minh tối thiểu:

- discovery/chunk output deterministic và full-corpus preview không có lỗi;
- mọi evidence part exact-match source LF và mọi point đúng schema tối thiểu;
- không silent truncation, partial ingestion hoặc mutation Foods collections;
- fresh-target/replacement protections có tác dụng quyết định;
- baseline và native hybrid thực sự dùng consumers khác nhau như contract;
- component failure tạo incomplete run hoặc typed API error, không fallback;
- context packing đúng token profile, whole-chunk order và Top-5;
- citation IDs/sources/excerpts được validate và public response không lộ field;
- UI thực hiện inline focus/source cards và safe Markdown;
- Golden merge/smoke/evaluator đúng schema, seed, metrics và failure semantics;
- official results đến từ full-corpus model/API/index runs thật.

Exact commands, file paths, task ordering, test cases, Review Contract và quyền
chạy paid/live systems chỉ thuộc Implementation Plan sau khi User duyệt spec này.

## 14. Nguồn quyết định và trạng thái

Spec này hợp nhất các quyết định canonical trong
[full-corpus guide](../../../guides/full_corpus_rag.md) và
[decision notes](2026-09-09-full-corpus-context-decisions.md). Verified
Architecture Extraction là evidence companion; report survey `llm_rag` 885 dòng
vẫn frozen/non-canonical và không phải nguồn contract.

User đã duyệt spec, Implementation Plan và Review Contract ngày 2026-09-11.
Phase 2 đã User-closed; Reviewer đã kích hoạt duy nhất Phase 3 hiện hành qua
active handoff. Các phase sau và mọi
runtime/API/Qdrant/paid benchmark vẫn giữ gate riêng trong Plan/Review Contract.

Spec này là umbrella behavior contract. Trước từng phase sau Phase 2, Reviewer
phải cập nhật guide phase và soạn exact phase spec, plan cùng Review
Contract dựa trên evidence dependency trước đó; User duyệt package rồi mới giao
Implementer. Addendum không được âm thầm đổi quyết định umbrella hoặc mô tả
behavior chưa triển khai như observed result.
