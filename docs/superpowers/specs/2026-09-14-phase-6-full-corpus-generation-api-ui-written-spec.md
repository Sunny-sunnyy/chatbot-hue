# Phase 6 Full-corpus Generation, API, Citations và Static UI — Written Spec

> **Lifecycle update 2026-09-29:** User đã dừng Phase 6 trước implementation để
> đánh giá lại metadata xuyên Phase 2/4/5/6. Spec này được giữ làm artifact đã
> duyệt ngày 2026-09-14 và reference cho dependency analysis; nó không còn cấp
> implementation/runtime authority cho tới khi metadata redesign được duyệt.

**Ngày:** 2026-09-14
**Trạng thái:** User-approved
**Approved by:** User
**Approval date:** 2026-09-14
**Vai trò thiết kế/review:** Codex Reviewer
**Phạm vi:** Full-corpus Phase 6

## 1. Mục tiêu

Phase 6 nối retrieval full-corpus đã hoàn tất ở Phase 5 với hai consumer cụ thể:

1. sinh phần bổ sung cho Representation B phục vụ retrieval experiment;
2. sinh câu trả lời tiếng Việt có citation, expose qua `POST /api/chat` và một
   static UI tối giản.

Phase này phải chạy được bằng dependency và dữ liệu thật, giữ đường đi tuyến
tính `retrieval -> context -> generation -> citation validation -> response`,
và không đưa agent loop hoặc frontend framework vào khi chưa có consumer.

## 2. Quyết định kế thừa và điều chỉnh

Spec này kế thừa Full-corpus Written Spec, Phase 5 Written Spec và các quyết
định umbrella #6a–#6e, trừ hai điều chỉnh được User phê duyệt trong brainstorming
ngày 2026-09-14:

- Không pin một OpenRouter upstream. OpenRouter được tự routing/fallback giữa
  các upstream phục vụ cùng model `qwen/qwen3.5-9b`.
- Không dùng mock, fake hoặc stub trong implementation validation và review
  evidence của Phase 6. Mọi claim runtime phải dựa trên dependency, corpus và
  response thật; nhánh chưa quan sát được phải ghi rõ là chưa live-verified.

Hai điều chỉnh trên thay thế phần “explicit upstream/no automatic provider
fallback” trong Decision #6c/#6d và phần “tests dùng mocked provider” trong kế
hoạch umbrella cũ. Chúng không cho phép model fallback: request luôn dùng đúng
`qwen/qwen3.5-9b`.

## 3. In scope

- một runtime retrieval cell được chọn bằng cấu hình và khởi tạo ở startup;
- validation cell của Phase 6 là:
  `e5-small-384 + dense_bm25_rrf + none`;
- tokenizer-aware Top-5 whole-chunk context packing;
- generator Representation B, output tối đa 256 tokens;
- answer generator tiếng Việt qua OpenRouter;
- response-local citation `[n]` và backend-owned source mapping;
- strict success/error schemas cho `POST /api/chat`;
- static HTML/CSS/JavaScript UI được FastAPI serve;
- kiểm thử và bounded live validation bằng hệ thống thật;
- báo cáo cấu hình, latency, token usage, upstream/cost nếu response cung cấp,
  output và kết luận thật.

## 4. Out of scope

- chọn retrieval/embedding/reranker winner;
- bật MiniLM trong validation cell mặc định;
- chạy full Representation B build hoặc tạo B indexes cho mọi candidate;
- production cutover hoặc xóa collection;
- OpenAI Agents SDK `Agent`/`Runner` trong Phase 6;
- tools, agent loop, planning, memory, session hoặc conversation history;
- streaming, application retry, model fallback hoặc automatic answer repair;
- Next.js/React migration;
- web search, routing ngoài Hue hoặc Phase 9 behavior;
- public retrieval trace, score, search text, filesystem path hoặc debug panel.

## 5. Kiến trúc và lifecycle

Luồng chat:

```text
Static UI
  -> POST /api/chat
  -> Full-corpus retrieval
  -> ContextBuilder
  -> Qwen answer generator
  -> CitationValidator
  -> SourceBuilder
  -> {answer, sources}
```

FastAPI lifespan khởi tạo fail-fast theo thứ tự:

1. load và validate settings;
2. đọc `OPENROUTER_API_KEY` từ process environment bằng `os.getenv`;
3. load tokenizer `Qwen/Qwen3.5-9B` từ một immutable pinned revision;
4. khởi tạo đúng một full-corpus retrieval service;
5. khởi tạo một `AsyncOpenAI` client cho OpenRouter;
6. mount static UI và chỉ chuyển readiness sang ready khi mọi dependency bắt
   buộc đã sẵn sàng.

Ứng dụng không tự mở hoặc parse `.env`. Lệnh chạy dùng `uv run --env-file .env`
để nạp environment. Key thiếu hoặc chỉ có whitespace làm startup fail closed.
`OPENROUTER_API_KEY` chỉ dùng cho OpenRouter; `OPENAI_API_KEY` vẫn tách riêng
cho OpenAI judge/evaluation ở phase khác.

Tokenizer, retrieval service và OpenRouter client được tạo một lần, dùng lại
cho mọi request và đóng trong lifespan shutdown. Không tạo client/model trong
từng request và không thêm generic LLM/provider abstraction.

## 6. OpenRouter/Qwen profile

Phase 6 gọi OpenRouter bằng `AsyncOpenAI` trực tiếp:

- base URL: `https://openrouter.ai/api/v1`;
- model: `qwen/qwen3.5-9b`;
- `temperature=0`;
- answer maximum output: 2048 tokens;
- Representation B maximum output: 256 tokens;
- request timeout: 90 giây;
- OpenAI client `max_retries=0`;
- không set sampling knobs khác;
- không gửi model fallback list;
- không gửi provider `order` hoặc `only`;
- gửi provider requirement `require_parameters: true` để chỉ dùng upstream hỗ
  trợ các request parameters, gồm structured output;
- giữ OpenRouter automatic upstream routing/fallback mặc định trong cùng model.

Phase 6 không dùng OpenRouter-specific SDK và không dùng raw HTTP. Generator là
`async` và gọi `await client.chat.completions.create(...)`.

Answer JSON schema đặt `additionalProperties=false`, require đúng một field
string `answer`, không có
`used_source_ids`, source objects, trace hoặc model-selected metadata. JSON sai
schema, field rỗng hoặc response không parse được là generation failure; không
retry và không tự sửa.

## 7. Representation B

Representation B giữ nguyên chunk A và toàn bộ `evidence_parts`. Qwen nhận nội
dung Representation A và sinh một đoạn `search_context` tiếng Việt cô đọng,
chỉ chứa thông tin suy ra từ input. Internal structured output có đúng field
string `search_context`.

Sau generation:

1. trim output và từ chối output rỗng/invalid;
2. nối `search_context` vào `search_text` bằng format cố định
   `<Representation A>\n\n[Ngữ cảnh tìm kiếm bổ sung]\n<search_context>`;
3. tokenize full combined representation bằng preprocessing thật của cả ba
   dense candidates E5-small, E5-base và HuyDang với `truncation=False`;
4. nếu combined representation vừa mọi tokenizer, dùng nó làm B `search_text`;
5. nếu valid generation làm representation vượt bất kỳ embedding limit nào,
   giữ nguyên A và ghi deterministic fallback reason;
6. nếu provider/generation lỗi, dừng B operation; không coi lỗi đó là một B
   thành công và không ghi artifact dở dang.

Generated `search_context` chỉ là retrieval augmentation. Nó không được thêm
vào `evidence_parts`, answer context, citations, source cards hoặc Golden truth.
Phase 6 xây và live-check path này bằng một call. Full B generation và fresh
indexes chỉ chạy cho retrieval finalists sau approval riêng.

## 8. Chat request và retrieval

Endpoint là `POST /api/chat`. Request body có đúng contract:

```json
{"query": "Câu hỏi tiếng Việt"}
```

Request từ chối extra fields. `query` phải là string, được trim, không rỗng và
không quá 500 ký tự. Phase 6 chỉ thiết kế, prompt và kiểm thử cho tiếng Việt;
generator luôn trả lời tiếng Việt. API không thêm language detector hoặc một
nhánh xử lý ngôn ngữ khác. Không có `session_id`, history, debug option hoặc
retrieval selector trong request.

Runtime chọn một retrieval cell tại startup bằng ba giá trị đã có contract ở
Phase 5:

```text
candidate_id
retrieval_treatment = dense_bm25_rrf | native_hybrid_rrf
reranker = none | minilm
```

Một process không đổi cell giữa các request. Phase 6 validation dùng
`e5-small-384 + dense_bm25_rrf + none`; đây chỉ là smoke configuration, không
phải winner/default cuối cùng. Retrieval trả Top 10 `documents` và private
`trace`. Phase 6 chỉ consume `documents`; trace không đi vào prompt hoặc public
response.

## 9. ContextBuilder và token budget

ContextBuilder tuyệt đối không dùng `RetrievedDocument.text/search_text` làm
bằng chứng. Mỗi answer block chỉ được dựng từ:

- `metadata.title`;
- `metadata.heading_path`;
- `metadata.evidence_parts`, giữ nguyên thứ tự và nguyên văn text.

Mỗi packed document là một whole chunk, một citation ID và một source card.
Không group/deduplicate theo title hoặc source. Tối đa năm chunks được xem xét
theo final retrieval rank.

Generator profile khóa:

```text
context_limit = 16384
reserved_output_tokens = 2048
safety_margin = 512
```

Với mỗi candidate chunk, ContextBuilder dựng lại exact system/user messages và
dùng official pinned Qwen tokenizer/chat template để đếm:

- system instructions;
- query;
- generation/citation/format instructions;
- labels, title và heading path;
- toàn bộ evidence text;
- chat template/special-token overhead.

Packing bắt đầu từ rank 1 và chỉ thêm nguyên chunk khi:

```text
input_tokens + reserved_output_tokens + safety_margin <= context_limit
```

Nếu chunk kế tiếp không vừa, packing dừng ngay; không skip xuống rank thấp hơn,
truncate, summarize hoặc dùng character fallback. Nếu chunk đầu tiên không
vừa, request thất bại bằng `context_budget_error`. Tokenizer được load một lần
ở startup; không có provider pre-call để đếm token.

Internal context dùng response-local labels `[1]` đến `[5]`. ID được gán theo
packed rank và chỉ tồn tại trong response hiện tại.

## 10. Grounded answer behavior

System instructions yêu cầu Qwen:

- trả lời tự nhiên, trực tiếp và chỉ bằng tiếng Việt;
- chỉ dùng evidence blocks được cung cấp;
- gắn `[n]` ngay sau claim được hỗ trợ;
- giữ điều kiện, ngoại lệ và bằng chứng mâu thuẫn;
- không dùng title/heading label như bằng chứng nếu evidence text không hỗ trợ;
- không bịa nguồn, URL, dữ kiện hoặc citation ID;
- dùng paragraph ngắn cho câu đơn giản và list khi câu trả lời thực sự có nhiều
  items/steps;
- không bắt buộc greeting, praise, emoji hoặc closing invitation.

Exact insufficient-evidence answer là:

```text
Tôi không tìm thấy đủ thông tin trong nguồn dữ liệu để trả lời câu hỏi này.
```

Nếu retrieval không có usable evidence, route trả ngay exact answer trên cùng
`sources: []` và không gọi Qwen. Nếu context tồn tại nhưng không đủ để trả lời,
Qwen phải trả đúng chuỗi này.

## 11. Citation validation và source mapping

Backend, không phải model, sở hữu source mapping. Sau khi parse structured
answer, CitationValidator áp dụng:

1. exact fallback chỉ hợp lệ khi không có citation marker; response có
   `sources: []`;
2. mọi answer khác phải có ít nhất một `[n]`;
3. mọi `n` phải là ID của packed block hiện tại;
4. marker lặp lại hợp lệ và chỉ tạo một source object;
5. unknown marker, missing marker hoặc fallback kèm marker là
   `citation_integrity_error`;
6. không automatic repair hoặc model retry.

SourceBuilder chỉ xuất distinct cited blocks, theo citation ID tăng dần. Public
source schema là:

```json
{
  "id": 1,
  "title": "Tên tài liệu",
  "heading_path": ["Mục", "Tiểu mục"],
  "excerpts": ["Đoạn bằng chứng nguyên văn"]
}
```

`excerpts` lấy trực tiếp từ `evidence_parts[].text`, giữ thứ tự. Public source
không có role, source path, point/chunk ID, score, token count, search text,
generated augmentation hoặc retrieval trace. Sources không được answer tham
chiếu không xuất hiện trong response.

## 12. Public API contract

Success, gồm cả insufficient-evidence case, trả HTTP 200:

```json
{
  "answer": "Câu trả lời có citation [1].",
  "sources": [
    {
      "id": 1,
      "title": "Tên tài liệu",
      "heading_path": ["Mục"],
      "excerpts": ["Đoạn bằng chứng nguyên văn"]
    }
  ]
}
```

Error response luôn có dạng:

```json
{
  "error": {
    "code": "generation_unavailable",
    "message": "Không thể tạo câu trả lời vào lúc này."
  }
}
```

Mapping bắt buộc:

| HTTP | `error.code` | Trường hợp |
|---:|---|---|
| 422 | `invalid_request` | JSON/schema/query không hợp lệ |
| 409 | `corpus_reingest_required` | build/corpus/index không còn tương thích |
| 503 | `retrieval_unavailable` | embedding, Qdrant hoặc retrieval failure |
| 502 | `generation_unavailable` | timeout, OpenRouter/Qwen hoặc structured output failure |
| 500 | `context_budget_error` | packed rank 1 không vừa budget |
| 500 | `citation_integrity_error` | answer/citation vi phạm contract |
| 500 | `internal_error` | lỗi ngoài dự kiến |

Không trả partial answer cho non-2xx response. Public message là tiếng Việt,
ngắn gọn và không chứa stack trace, provider body, prompt hoặc secret.

## 13. Static UI

FastAPI serve một static UI bằng HTML/CSS/JavaScript. Phase 6 không thêm
Next.js, React, bundler hoặc Node runtime. UI gồm đúng:

- textarea/ô nhập câu hỏi;
- nút gửi;
- loading state và chặn submit trùng;
- answer Markdown;
- inline citation `[n]` có thể click và dùng keyboard;
- source cards ngay dưới answer;
- trạng thái lỗi tiếng Việt và nút retry thủ công.

Markdown được parse và sanitize bằng các browser assets `marked` và `DOMPurify`
được pin, lưu local và serve cùng ứng dụng; không dùng runtime CDN. UI render
text/source metadata an toàn, không dùng raw unsanitized HTML. Citation click
hoặc Enter/Space cuộn tới và focus card có cùng `id`.

Không có history, streaming, source drawer/modal, score/debug view, agent step
hoặc tool UI. Public API contract được giữ độc lập với static implementation để
frontend tương lai có thể thay view bằng Next.js mà không đổi backend contract.

## 14. Error handling và logging

- Không biến dependency/generation failure thành answer HTTP 200.
- Không application retry; OpenAI client có `max_retries=0`.
- OpenRouter có thể thử upstream khác trong cùng một request và cùng model.
- Không tự chuyển retrieval cell, reranker mode, model hoặc Representation B
  failure sang một success path khác.
- Valid B output vượt embedding limit được giữ A theo Representation B contract;
  đây là deterministic length fallback, không phải provider failure fallback.
- Generation timeout là 90 giây.

Internal log ghi tối thiểu request ID, stage, elapsed time, candidate/treatment/
reranker, retrieved/packed counts, input/output token usage, model, finish reason
và upstream/cost khi OpenRouter response cung cấp. Không log API key,
Authorization header hoặc full prompt. Client không nhận internal stack trace.

## 15. Live-only validation

Phase 6 không tạo hoặc dùng mock/fake/stub cho provider, Qdrant, embedding,
retrieval documents hay API response. Validation dùng:

- curated corpus thật đang được build record chấp nhận;
- Qdrant collections thật;
- embedding/tokenizer thật;
- FastAPI endpoint thật;
- OpenRouter/Qwen response thật;
- static UI render response thật.

Malformed HTTP requests dùng để kiểm public validation contract là request biên
thật, không phải dependency simulation. Provider outage, malformed provider
response hoặc model-produced invalid citation không được ép bằng dead URL,
monkeypatch hoặc fabricated response; nếu không xảy ra tự nhiên, report ghi
`chưa được live-verified` và reviewer kiểm code path tĩnh.

Bounded generation validation gồm đúng năm Qwen calls, không application retry:

1. một Representation B generation;
2. một direct-fact answer với một citation;
3. một synthesis answer cần nhiều citations;
4. một conditional/conflicting-evidence answer;
5. một out-of-scope answer trong đó retrieval vẫn cung cấp context và Qwen phải
   trả exact insufficient-evidence fallback.

No-usable-context skip-model path chỉ được live-claim khi trạng thái này xuất
hiện tự nhiên. Không tạo collection rỗng hoặc dữ liệu giả để ép nó. Call thất
bại vẫn là một observed call và không được tự thay bằng call thứ sáu; mọi call
bổ sung cần User approval riêng.

## 16. Báo cáo bắt buộc

Implementation/review report phải ghi:

- timestamp, Git commit và dirty worktree state;
- exact retrieval cell, collection/build identity và corpus readiness;
- Qwen model/profile, tokenizer repository và immutable revision;
- OpenRouter routing requirement và upstream thực tế khi response cung cấp;
- cho từng call: mục đích, exact test question/input không chứa secret, latency, token usage,
  finish reason, reported cost, output, citations và source mapping;
- manual evidence check cho từng claim/citation;
- HTTP/UI checks và observed error contracts;
- PASS/FAIL theo acceptance criterion;
- mọi giới hạn hoặc nhánh chưa live-verified.

Report không được biến năm-call smoke thành official quality benchmark hoặc chọn
winner Phase 8.

## 17. Acceptance criteria

Phase 6 chỉ đủ điều kiện Reviewer review khi:

1. startup fail closed với missing key/tokenizer/retrieval/build dependency;
2. validation cell đúng `e5-small-384 + dense_bm25_rrf + none` và không load
   MiniLM;
3. Phase 5 retrieval Top 10 đi vào token-aware whole-chunk Top-5 packing;
4. answer context chỉ dùng exact `evidence_parts`;
5. official pinned Qwen tokenizer đếm full request overhead và không truncate;
6. generator dùng direct reusable `AsyncOpenAI`, không Agent/Runner;
7. OpenRouter dùng đúng model/profile, `require_parameters: true`, không model
   fallback, không application retry và không provider pin;
8. answer luôn tiếng Việt và mọi non-fallback answer có citation hợp lệ;
9. backend tạo strict `{answer,sources}` từ packed evidence, không tin
   model-generated source metadata;
10. exact fallback là trường hợp duy nhất được phép có zero citations/sources;
11. typed HTTP errors đúng mapping và không có partial success;
12. Representation B output không đi vào evidence/citation và length fallback
    giữ A nguyên vẹn;
13. static UI sanitize Markdown, chặn duplicate submit và map citation/source
    bằng click lẫn keyboard;
14. không có mock/fake/stub evidence;
15. năm bounded Qwen calls được chạy và báo cáo bằng kết quả thật, hoặc report
    FAIL/incomplete nếu dependency thực ngăn hoàn tất;
16. không có unauthorized collection mutation, production cutover, cleanup,
    Git commit hoặc push.

## 18. Handoff boundary

Sau khi User duyệt Written Spec này, Reviewer mới lập implementation plan chi
tiết. Việc chạy paid calls diễn ra ở implementation/review execution theo đúng
năm-call contract đã duyệt. Mọi mở rộng số call, full Representation B build,
collection mutation, Git action hoặc thay đổi ngoài scope cần quyền riêng.
