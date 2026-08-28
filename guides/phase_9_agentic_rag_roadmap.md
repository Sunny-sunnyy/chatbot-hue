# Phase 9: Roadmap thiết kế Agentic RAG sau MVP

## Mục tiêu và giá trị cho người dùng

Phase 9 mô tả các câu hỏi thiết kế cần giải quyết trước khi thêm Agentic RAG cho văn hóa và du lịch Huế. File giúp người dùng hiểu agent có thể cải thiện loại câu hỏi nào, đồng thời ngăn orchestration phức tạp khi MVP chưa ổn định.

## Trạng thái

```text
Status: not_ready
Owner: Codex Reviewer
Implementation authorization: none
```

Không được implement Phase 9 từ guide này. Trước runtime code phải có separate
design, cách đánh giá rõ ràng và user approval.

## Dependency hard gate

- Phase 8 đã chọn và bảo vệ một MVP pipeline.
- Retrieval/answer baseline metrics, latency và cost đã biết.
- Người dùng xác định Agentic RAG giải quyết failure categories cụ thể.
- Có cost/latency/loop limits và agentic evaluation set.
- Parent-child data model, memory policy và tool boundary được phê duyệt.

Nếu chưa đủ năm điều kiện, Phase 9 giữ `not_ready`.

## Capability có thể nghiên cứu

### Query classification và routing

Phân biệt:

- direct fact: một retrieval call thường đủ;
- recommendation/comparison: cần nhiều evidence và constraints;
- multi-hop: cần chia nhỏ câu hỏi;
- holistic/planning: tổng hợp nhiều entity/source;
- unsafe/out-of-scope: safe response hoặc làm rõ.

Direct questions phải giữ fast path nếu baseline đủ tốt; không bắt mọi query qua agent loop.

### Query rewrite

Chuẩn hóa diễn đạt, typo hoặc implicit entity. Design phải giữ user constraints và lưu original/rewrite cho evaluation. Rewrite không thêm facts không có trong query.

### Query decomposition

Tách multi-part/multi-hop question thành bounded subqueries, retrieve độc lập rồi merge/deduplicate evidence. Giới hạn số subqueries, parallelism, candidates và total token/cost.

### Evidence sufficiency và retrieval retry

Judge có thể đánh giá evidence đủ chưa và cho phép tối đa một retry với strategy khác. Retry phải có stop reason; không tự đổi provider/model/index hoặc loop vô hạn.

### Parent-child retrieval

Có thể tham khảo `rag_old`: retrieve child chunks nhưng trả parent context. Trước code phải thiết kế parent/child IDs, source integrity, reindex migration, duplicate control và comparison với section chunks.

### Tool use

Future tools có thể gồm local retrieval, structured place/food lookup hoặc itinerary constraints. Web search/enrichment không tự động được phép chỉ vì có agent; vẫn cần user scope và source policy.

### Memory và session

Phân biệt request-local state, conversation history, user preference memory và
persistent profile. Bước đầu nên dùng bounded conversation history. Persistent
memory cần privacy, retention, deletion, conflict resolution và poisoning design
riêng.

Tên định danh future chat là `conversation_id`, không phải `session_id`.
`session_id` trong web thường chỉ authentication session; không được dùng một
conversation identifier như authentication credential. Phase 6 không còn
identifier placeholder. `conversation_id` chỉ được thêm cùng feature lưu history
hoàn chỉnh trong separate conversational design.

### Research baseline cho conversation và memory

Research được người dùng yêu cầu và xác nhận ngày 2026-08-25 khóa terminology:

| Khái niệm | Phạm vi | Storage/lifetime dự kiến |
|---|---|---|
| Request-local state | Một request | Không persist |
| Conversation history | User/assistant messages trong một thread | Persist theo `conversation_id`, bounded khi đưa vào model |
| Long-term user memory | Preference/fact qua nhiều thread | Separate opt-in policy; chưa được phép implement |
| RAG knowledge | Curated Huế corpus | Qdrant/index hiện hành, không trộn với user memory |
| Authentication session | Identity/access control của web app | Separate security boundary |

CoALA phân biệt episodic, semantic và procedural memory. Đối với follow-up như
`Bún bò Huế là gì?` -> `Các quán nổi tiếng?`, requirement thực tế chỉ là
conversation history trong cùng thread và contextualized retrieval query; chưa
cần semantic user profile, cross-session memory hoặc MemGPT-style hierarchical
memory.

OpenAI Agents SDK hỗ trợ application-owned history, SDK `Session`, OpenAI
Conversations và `previous_response_id`. Design phải chọn đúng một persistence
strategy trên mỗi conversation để tránh duplicate context. Hue RAG retrieval
chạy trước answer `Runner`, nên SDK Session chỉ đặt ở generator không đủ: history
phải được đọc ở application layer trước retrieval để tạo standalone query.

Phase 6 giữ một tool-less `Agent/Runner` với one-field `AnswerOutput`, nhưng đây
chỉ là final-generation boundary, không phải authorization cho agent loop.
Phase 9 được phép reuse Agents SDK; mỗi capability phải có schema nhỏ riêng như
`RewriteOutput`, `RouteDecision` hoặc `SufficiencyOutput`, không mở rộng một
answer schema thành object chứa mọi state.

Query rewriting research (QReCC/CONQRR) chỉ ra cách chuyển context-dependent
follow-up thành self-contained query dùng được với off-the-shelf retriever. Không
nối thẳng toàn bộ prior user questions như `rag_old_0`, vì topic switch có thể
làm retrieval bị nhiễu. Rewrite phải giữ original query để evaluation, không
thêm facts và không bỏ constraints.

Không gửi toàn bộ lịch sử vô hạn vào model. `Lost in the Middle` cho thấy long
context không bảo đảm model dùng tốt evidence ở mọi vị trí. Candidate design
phải budget riêng recent messages, older-history summary và retrieved evidence.
LongMemEval cho thấy cần đánh giá riêng information extraction, multi-session
reasoning, temporal reasoning, knowledge updates và abstention; lưu được message
không đồng nghĩa memory system đã đúng.

Persistent user memory là attack surface riêng. MINJA cho thấy memory bank của
agent có thể bị injection; PoisonedRAG cho thấy knowledge base cũng có thể bị
poisoning. Nội dung retrieved, web content và assistant-generated summaries đều
phải được xem là untrusted. Không cho model tự động biến retrieved content thành
durable user memory.

Nguồn research canonical:

- OpenAI Agents SDK state/conversation management:
  <https://openai.github.io/openai-agents-python/running_agents/>
- OpenAI Agents SDK Session protocol:
  <https://openai.github.io/openai-agents-python/ref/memory/session/>
- OpenAI Agents SDK encrypted session với TTL:
  <https://openai.github.io/openai-agents-python/sessions/encrypted_session/>
- OWASP Session Management Cheat Sheet:
  <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
- CoALA:
  <https://arxiv.org/abs/2309.02427>
- MemGPT:
  <https://arxiv.org/abs/2310.08560>
- QReCC:
  <https://arxiv.org/abs/2010.04898>
- CONQRR:
  <https://aclanthology.org/2022.emnlp-main.679/>
- Lost in the Middle:
  <https://arxiv.org/abs/2307.03172>
- LongMemEval:
  <https://arxiv.org/abs/2410.10813>
- LoCoMo — very long-term conversational memory evaluation:
  <https://aclanthology.org/2024.acl-long.747/>
- MINJA:
  <https://papers.nips.cc/paper_files/paper/2025/file/42a97bbd9844d2bf68596730af80bcdf-Paper-Conference.pdf>
- PoisonedRAG:
  <https://www.usenix.org/system/files/usenixsecurity25-zou-poisonedrag.pdf>

### Định hướng multi-turn và routing đã chốt từ Phase 6

Phase 6 là single-turn stateless API và không tạo identifier. Khi Phase 9 vượt
đủ hard gate, design riêng phải nghiên cứu luồng ưu tiên sau:

```text
new conversation -> server tạo conversation_id -> persist ownership/lifecycle
  -> user message được lưu đúng thứ tự
  -> load bounded recent history
  -> standalone-query contextualizer trước retrieval
  -> structured input router
       casual conversation -> Conversation Agent, không retrieval/web
       Hue culture/travel -> RAG path
       out of domain -> safe out-of-scope response
  -> Hue RAG thiếu evidence
       -> explicit evidence-sufficiency gate
       -> Web Agent chỉ tra cứu văn hóa/du lịch Huế
       -> answer có web provenance riêng
  -> persist final assistant answer
```

Standalone-query contextualizer phải giải quyết follow-up có đại từ hoặc entity
ẩn, ví dụ biến "Các quán ăn nổi tiếng về nó?" thành câu độc lập vẫn giữ đúng
"cơm hến" từ lịch sử trước khi retrieval. Rewrite không được thêm facts hoặc bỏ
constraints của người dùng.

Router nên trả structured route enum như `casual`, `hue_rag`,
`out_of_scope`, kèm confidence và safe reason code; không lưu hoặc trả hidden
chain-of-thought. Không để một agent tự đoán rằng KB thiếu dữ liệu rồi bỏ qua
RAG: với query thuộc Huế, RAG chạy trước và web escalation chỉ mở sau evidence
gate rõ ràng.

Web Agent không phải trợ lý web tổng quát. Nó chỉ được xử lý câu hỏi thuộc văn
hóa/du lịch Huế mà curated RAG thiếu evidence, không silent fallback, phải lưu
URL/thời điểm truy cập và phân biệt nguồn web với nguồn curated. Nội dung web
không tự động ghi vào `knowledge-base-hue/`.

### Conversation lifecycle tối thiểu phải thiết kế

Separate conversational design phải chốt:

- API tạo conversation mới và cách frontend nhận/lưu `conversation_id` mà
  không hiển thị trong chat content;
- persistent conversation/message repository; SQLite là baseline local đơn
  giản, còn production storage phải được chọn theo durability, multi-worker và
  transaction requirements thực tế;
- association giữa conversation và authenticated `user_id` khi authentication
  tồn tại; biết ID không đồng nghĩa có quyền đọc conversation;
- message ordering, concurrent requests, idempotency và behavior khi regenerate;
- bounded recent-history window, summary policy và token budget;
- retention, user deletion/export, encryption và safe logging;
- provider portability: application-owned source of truth, không đồng thời lưu
  cùng history ở app và provider mà không có reconciliation rõ ràng;
- conversation delete/expiry không để orphaned summaries hoặc memory vectors.

Long-term memory qua nhiều conversation là phase con độc lập sau conversation
history. Không tự động trích xuất preference/profile trong realtime; trước tiên
phải có opt-in, provenance, update/supersede rules, TTL/deletion và memory
retrieval evaluation.

## Ba architecture options bắt buộc so sánh

1. Modern/SOTA: graph/state-machine orchestration với router, parallel subqueries và evidence judge.
2. Safe/stable: deterministic controller, rule-first direct path và tối đa một LLM-planned retry.
3. Simple/MVP: một query classifier, optional rewrite và một retrieval retry.

Khuyến nghị ban đầu là safe/stable hoặc simple MVP. Chỉ chọn graph orchestration khi evaluation chứng minh nhiều categories cần branching/state.

## Interface boundaries cần thiết kế

Design riêng phải định nghĩa tối thiểu:

```python
class QueryPlan: ...
class Subquery: ...
class EvidenceBundle: ...
class SufficiencyDecision: ...
class AgentTraceSummary: ...
```

Mỗi interface phải có input/output fields, maximum budgets, allowed transitions, failure/stop reasons, source lineage và safe trace fields.

Không lưu hidden chain-of-thought. Observability dùng structured summaries: route, tool name, latency, candidate/source count, stop reason và token/cost usage.
Agents SDK tracing tiếp tục tắt mặc định. Chỉ được mở lại sau một observability
design riêng có field allowlist, retention/privacy policy và user opt-in; không
dùng Trace Dashboard như điều kiện để runtime hoạt động.

## Evaluation requirements trước implementation

Agentic evaluation set phải thêm:

- ambiguous entity;
- multiple constraints;
- comparison;
- multi-hop across documents;
- holistic itinerary/food planning;
- query rewrite needed;
- evidence insufficient;
- direct query để kiểm tra agent không làm chậm vô ích.

Conversation evaluation set phải tách riêng và tối thiểu có:

- follow-up ẩn entity: `bún bò` -> `các quán nổi tiếng?`;
- đại từ/coreference: `cơm hến` -> `món đó cay không?`;
- constraint carry-over và constraint update;
- topic switch để bảo đảm history cũ không làm nhiễu retrieval;
- câu độc lập không cần rewrite;
- rewrite không thêm fact hoặc bỏ constraint;
- isolation giữa hai `conversation_id`;
- unauthorized cross-user access bị từ chối;
- concurrent/out-of-order messages;
- history quá dài, summary và token budget;
- delete/expiry và provider/storage failure;
- không đủ evidence sau rewrite vẫn trả safe fallback.

Metrics thêm:

- route accuracy;
- plan/subquery validity;
- tool-call count;
- retry rate và success delta;
- evidence-source coverage;
- end-to-end latency p50/p95;
- token/cost per category;
- loop/timeout/error rate;
- direct-path regression.

Agentic system chỉ có giá trị khi cải thiện failure categories mà không làm direct queries suy giảm quá mức.

## Security và safety questions

- Retrieved prompt injection được neutralize thế nào?
- Tool input/output schema validation ở đâu?
- Agent được gọi tools nào và tối đa bao nhiêu lần?
- Web/external data có được phép không, provenance lưu thế nào?
- Conversation/user data giữ và xóa thế nào?
- Conversation ID được bind với user/tenant và authorize ra sao?
- Concurrent messages, replay và idempotency được xử lý thế nào?
- Retrieved/web content có được phép ghi durable memory không? Mặc định là không.
- Trace nào an toàn, không lộ query/context nhạy cảm?
- Provider outage có fast-path fallback hay fail rõ?

Những câu hỏi này phải có answer trong design trước code.

## Reliability và performance budgets

Design phải chốt numeric ceilings cho:

```text
maximum planning calls
maximum subqueries
maximum retrieval calls
maximum retries
maximum total context
maximum end-to-end latency
maximum token/cost per request
```

Default conceptual ceiling là một retry; các số khác phải được user phê duyệt dựa trên Phase 8 baseline.

## Bài học được phép tham khảo

Từ `rag_old`:

- router/rewrite/decompose concepts;
- parent-child retrieval concept;
- one-retry judge idea;
- retrieval/answer evaluation discipline.

Không copy Chroma/SQLite/OpenAI embedding choices, paid LLM ingestion, provider-specific code, evaluator inconsistencies, English-only assumptions hoặc directory tools chưa threat-model.

Từ `llm_rag` có thể học module boundaries, bounded context và startup caching;
không mặc định reuse SSE/frontend, mocked tests hoặc English-centric reranker.

## Separate design bắt buộc

Design session riêng phải:

1. Phân tích Phase 8 failure cases và problem statement.
2. So sánh ba architecture options.
3. Chọn state transitions, tool permissions và budgets.
4. Thiết kế data/interface/source-lineage contracts.
5. Thiết kế agentic evaluation và regression gates.
6. Phân tích security/privacy/observability.
7. Chia implementation thành phases nhỏ có independent acceptance.
8. Được user phê duyệt trước runtime files.

## Nhiệm vụ của DeepSeek Implementer

Không có implementation task hiện tại. DeepSeek chỉ được đọc roadmap để chuẩn bị câu hỏi hoặc inspect MVP evidence. Không tạo `backend/agentic/` và không thêm dependency.

## Nhiệm vụ của Codex Reviewer

- Giữ Phase 9 ở `not_ready` đến khi user duyệt separate design.
- Yêu cầu evidence rằng complexity giải quyết failure thật.
- Điều phối design riêng và kiểm tra scope creep.
- Không approve plan thiếu budgets, tools, evaluation hoặc security model.

## Định hướng đã được người dùng xác nhận

```text
Decision: Future multi-turn flow nghiên cứu bounded persistent history và standalone-query contextualization; Phase 6 giữ stateless session_id.
Reason: Follow-up như "nó" cần ngữ cảnh hội thoại nhưng không thuộc MVP hiện tại.
Date +07: 2026-08-13.
Status: superseded ngày 2026-08-25 bởi decision bên dưới.
```

```text
Decision: Phase 6 không có session/conversation identifier. Future conversational phase thêm server-generated conversation_id chỉ cùng lúc với persistent message storage, lifecycle/ownership policy và standalone-query contextualization trước retrieval. Long-term cross-conversation memory là scope độc lập, chưa được phép implement.
Reason: Identifier echo-only không tạo memory; SDK generator session không contextualize retrieval; application-owned conversation state rõ ràng và provider-portable hơn cho Hue RAG.
Evidence: OpenAI Agents SDK, OWASP, CoALA, MemGPT, QReCC/CONQRR, Lost in the Middle, LongMemEval, MINJA và PoisonedRAG research.
Approved by: User
Date +07: 2026-08-25.
```

```text
Decision: Future router nghiên cứu tách casual conversation, Hue RAG và out-of-scope; web escalation chỉ dành cho Hue query thiếu RAG evidence.
Reason: Giữ direct RAG fast path và chỉ thêm agent/tool khi có failure thật.
Date +07: 2026-08-13.
```

Các decision records trên chỉ khóa hướng nghiên cứu. Chúng không thay đổi
`Status: not_ready` và không tạo implementation authorization.

## Notebook

Không tạo notebook Phase 9 ở trạng thái `not_ready`. Nếu Phase 9 được tách thành
implementation phases sau design riêng, mỗi implementation phase phải có
notebook mang prefix `09_`, import runtime modules và phục vụ user confirmation;
exact filename được khóa trong design mới.

## Tiêu chí để chuyển từ roadmap sang design-ready

- Phase 8 baseline ổn định.
- Failure categories và expected benefit đo được.
- User chọn architecture direction.
- Interface, tool, state, budget và safety contracts được viết.
- Agentic evaluation/regression plan hoàn chỉnh.
- Design được Codex review và user approve.

Các tiêu chí chỉ cho phép lập implementation plan; không tự động cho phép code.

## Reports và cập nhật trạng thái

Không tạo implementation, Codex review hoặc user report cho Phase 9 trước
implementation thực tế. Nếu implementation được phê duyệt riêng, áp dụng
workflow và user confirmation hiện hành. `Project_Status.md` tiếp tục mô tả
Phase 9 là post-MVP và `not_ready` cho đến khi user thay đổi.

## Bước tiếp theo

Không có action Phase 9 trong MVP hiện tại. Phase 0–7 và simplicity reviews đã
approved; Golden Dataset V3 Gate 0 và Phase 8 Gate 1 common contracts cũng đã
approved. Exact Notebook 08a design/plan và isolated implementation/Run All đã
được authorize; bước hợp lệ là hoàn tất implementation, independent review và
user confirmation của 08a, rồi tiếp tục từng Notebook 08 group theo authorization
riêng. Chỉ sau khi Phase 8 hoàn tất mới cân nhắc Phase 9 từ failure evidence thật.
