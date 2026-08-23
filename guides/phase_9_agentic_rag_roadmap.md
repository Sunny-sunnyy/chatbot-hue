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

Phân biệt request-local state, conversation history, user preference memory và persistent profile. Bước đầu nên dùng bounded request/conversation state. Persistent memory cần privacy, retention và deletion design riêng.

### Định hướng multi-turn và routing đã chốt từ Phase 6

Phase 6 chỉ tạo/echo `session_id` và không lưu lịch sử. Khi Phase 9 vượt đủ hard
gate, design riêng phải nghiên cứu luồng ưu tiên sau:

```text
bounded persistent conversation history
  -> standalone-query contextualizer trước retrieval
  -> structured input router
       casual conversation -> Conversation Agent, không retrieval/web
       Hue culture/travel -> RAG path
       out of domain -> safe out-of-scope response
  -> Hue RAG thiếu evidence
       -> explicit evidence-sufficiency gate
       -> Web Agent chỉ tra cứu văn hóa/du lịch Huế
       -> answer có web provenance riêng
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
```

```text
Decision: Future router nghiên cứu tách casual conversation, Hue RAG và out-of-scope; web escalation chỉ dành cho Hue query thiếu RAG evidence.
Reason: Giữ direct RAG fast path và chỉ thêm agent/tool khi có failure thật.
Date +07: 2026-08-13.
```

Hai decision records trên chỉ khóa hướng nghiên cứu. Chúng không thay đổi
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

Không có action Phase 9 trong MVP hiện tại. Bước hợp lệ là hoàn thành Phase 7,
review Phase 0 đến Phase 6, rồi mới cân nhắc Phase 8.
