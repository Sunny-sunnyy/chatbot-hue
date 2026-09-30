# Phase 6 Full-corpus Generation, API, Citations và Static UI — Metadata v2 Amendment

**Ngày:** 2026-09-30

**Trạng thái:** User-approved

**Approved by:** User

**Approval date:** 2026-09-30

**Vai trò thiết kế/review:** Codex Reviewer

**Phạm vi:** Delta để mở lại Full-corpus Phase 6 sau Metadata v2

## 1. Mục tiêu

Amendment này mở lại cổng thiết kế của Full-corpus Phase 6 sau khi Metadata v2
Tasks 1–7 đã được independent review và User xác nhận closure. Nó giữ nguyên
hành vi sản phẩm đã duyệt ngày 2026-09-14, đồng thời khóa ba thay đổi cần thiết:

1. Phase 6 phải consume strict Metadata v2 retrieval path đã hoàn tất;
2. curated corpus và runtime data là dependency private được provision ngoài
   Git;
3. execution dùng một Implementer handoff, với non-paid gate bắt buộc trước
   đúng năm Qwen call attempts.

Amendment không cấp implementation, runtime, paid-call hoặc Git authority.
Implementation chỉ được mở sau khi User duyệt riêng Written Spec này và
Implementation Plan kèm Review Contract mới.

## 2. Source hierarchy và supersession

Các nguồn áp dụng theo thứ tự:

1. amendment này cho lifecycle, Metadata v2 dependency, private provisioning và
   execution gating;
2. Metadata v2 Written Spec cho payload, build record, freshness, retrieval
   identity, private trace và public boundary;
3. Phase 6 Written Spec ngày 2026-09-14 cho mọi behavior sản phẩm còn lại;
4. Implementation Plan mới sẽ được viết sau khi amendment này được User duyệt.

Các artifact liên quan:

```text
docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md
docs/superpowers/specs/2026-09-14-phase-6-full-corpus-generation-api-ui-written-spec.md
docs/superpowers/plans/2026-09-14-phase-6-full-corpus-generation-api-ui-implementation-plan.md
```

Spec và plan ngày 2026-09-14 được giữ nguyên làm audit history. Amendment này
không chép lại toàn bộ requirement đã duyệt và không làm mất hiệu lực các quyết
định về Qwen/OpenRouter, Representation B, token budget, API, citation hoặc
static UI.

Plan ngày 2026-09-14 không còn execution authority và không được dùng trực tiếp
để khởi chạy implementation. Plan mới phải tham chiếu requirement còn hiệu lực,
loại bỏ checkpoint ceremony không cần thiết và dùng code/runtime state hiện tại.

## 3. Behavior được giữ nguyên

Các behavior sau tiếp tục có hiệu lực:

- validation cell là
  `e5-small-384 + dense_bm25_rrf + none`, không phải benchmark winner;
- ContextBuilder pack tối đa Top 5 whole chunks theo rank bằng pinned Qwen
  tokenizer và exact token budget đã duyệt;
- answer context và public excerpts chỉ lấy từ `title`, `heading_path` và
  `evidence_parts`;
- direct reusable `AsyncOpenAI` gọi `qwen/qwen3.5-9b` qua OpenRouter với
  `temperature=0`, `max_retries=0`, `provider.require_parameters=true`, không
  provider pin, model fallback hoặc application retry;
- Representation B chỉ bổ sung private `search_text`, không thay
  `evidence_parts`, citations hoặc Golden truth;
- public success là strict `{answer,sources}` với response-local citation `[n]`;
- backend sở hữu citation validation và source mapping;
- static HTML/CSS/JavaScript UI render sanitized Markdown bằng pinned local
  assets và hỗ trợ citation bằng click lẫn keyboard;
- Phase 6 là single-turn tiếng Việt, không streaming, history, memory, tools,
  agent loop, domain routing hoặc debug API.

## 4. Private provisioning contract

`knowledge-base-hue/` là curated corpus local/private và không còn là tracked
Git content. Một môi trường mới phải được provision ngoài repository trước khi
Phase 6 startup. Private runtime prerequisites gồm:

- toàn bộ curated `knowledge-base-hue/` từ bản sao lưu private đã được User quản
  lý;
- Metadata v2 build records tương ứng;
- bốn Metadata v2 Qdrant collections;
- pinned tokenizer/model cache cần thiết;
- credentials được nạp qua process environment.

Tracked documentation chỉ được ghi destination, contract validation và failure
behavior. Không ghi private backup location, secret, corpus inventory, source
content, fixed private questions, payload dump hoặc vectors.

Phase 6 không tạo corpus downloader, sync service, registry, recovery workflow,
web reconstruction hoặc checksum layer mới. Provisioning là operator
precondition; runtime readiness là lớp xác minh. Metadata v2 build identity và
source hashes hiện có là nguồn kiểm chứng duy nhất.

Clean clone thiếu private prerequisites là trạng thái hợp lệ nhưng chưa ready;
không được tự động lấy dữ liệu từ web hoặc phục vụ bằng stale collection.

## 5. Runtime architecture và data flow

Luồng chuẩn:

```text
private corpus provisioned locally
  -> Metadata v2 source/build/collection readiness
  -> full-corpus retrieval v2
  -> evidence-only ContextBuilder
  -> one-shot Qwen generation
  -> citation validation and source mapping
  -> {answer, sources}
  -> static UI
```

FastAPI composition root phải gọi trực tiếp canonical
`build_full_corpus_retrieval_service(...)`. Phase 6 không duplicate payload,
build-record, source-hash, point-ID, `chunk_id` hoặc `domain` validation.

`backend/retrieval/full_corpus.py` tiếp tục sở hữu Metadata v2 readiness và trả:

```text
RetrievedDocument
  id: payload.chunk_id
  text: private search_text
  metadata:
    source
    title
    heading_path
    evidence_parts
    domain
```

Phase 6 chỉ consume `title`, `heading_path` và `evidence_parts` để dựng context
và source cards. `RetrievedDocument.id`, `domain`, Qdrant point ID,
`search_text`, source path, score, rank, build identity và trace không đi vào
prompt evidence hoặc public response.

Không dùng `domain` để filter, boost, fuse, rerank hoặc route câu hỏi.

## 6. Components và responsibility

- Canonical full-corpus retrieval giữ toàn bộ Metadata v2 readiness, query và
  result validation.
- Phase 6 composition root tạo retrieval service, pinned tokenizer,
  evidence-only context builder và reusable OpenRouter client đúng một lần
  trong lifespan.
- ContextBuilder chỉ làm whole-chunk packing và token accounting.
- Generator chỉ thực hiện hai structured operations: answer và
  Representation B search context.
- Citation component chỉ validate response-local markers và chọn packed sources
  được trích dẫn.
- API route chỉ điều phối tuyến tính và map typed failures.
- Static UI chỉ consume public API contract.

Không thêm provider abstraction, metadata compatibility layer, domain router,
generic registry, background recovery, fallback stack hoặc state machine.

## 7. Startup và failure behavior

Import application không được kết nối dependency. Lifespan khởi tạo dependency
thật và chỉ publish readiness khi các prerequisite bắt buộc đạt.

Failure mapping:

| Điều kiện | Public behavior |
|---|---|
| Corpus thiếu, file/path/hash lệch, build/collection schema hoặc identity stale | health `degraded`; chat `409 corpus_reingest_required` |
| Qdrant, embedding hoặc retrieval dependency unavailable | `503 retrieval_unavailable` |
| OpenRouter/Qwen timeout, provider hoặc structured-output failure | `502 generation_unavailable` |
| Highest-ranked evidence chunk không vừa exact token budget | `500 context_budget_error` |
| Missing/unknown/invalid citation | `500 citation_integrity_error` |
| Lỗi ngoài dự kiến | `500 internal_error` |

Không trả partial answer cho failure. Không retry, đổi model, đổi retrieval cell,
fallback sang legacy collection, bỏ freshness check hoặc tự provision dữ liệu.

No-usable-evidence path tiếp tục skip model và trả exact insufficient-evidence
answer với `sources: []`.

## 8. Implementation gating

Sau khi User duyệt Plan mới, Phase 6 dùng một Implementer handoff duy nhất.
Implementer tự thực hiện tuần tự:

1. triển khai và hoàn tất toàn bộ non-paid scope;
2. chạy focused affected checks cùng real read-only startup/retrieval;
3. xác nhận tokenizer/assets/config, corpus freshness, collection immutability
   và public privacy boundary;
4. chỉ khi mọi non-paid gate đạt mới chạy bounded paid runner;
5. lập một implementation report và chuyển một final-review handoff cho
   Reviewer.

Không có Reviewer checkpoint sau từng internal task. Bất kỳ non-paid failure
nào cũng dừng trước paid runner.

## 9. Verification và paid evidence

Non-paid verification phải dùng dependency và dữ liệu thật phù hợp:

- exact settings và pinned tokenizer/assets;
- Metadata v2 source/build/collection readiness;
- read-only retrieval trên validation cell;
- evidence-only whole-chunk packing và token accounting;
- citation rules và public source selection;
- API request/error envelopes, cached health và import safety;
- static serving, sanitization và keyboard interaction;
- affected Metadata v2/retrieval cùng Phase 6 API/LLM/UI checks.

Không mặc định chạy toàn bộ backend suite nếu exact affected scope không chứng
minh blast radius tương ứng. Không dùng mock, fake, stub, replay output hoặc
fabricated provider response làm implementation/acceptance evidence. Pure
deterministic values nhỏ chỉ được dùng cho pure decision logic, không thay
integration evidence.

Paid runner thực hiện đúng năm Qwen call attempts, không application retry:

1. một Representation B generation;
2. một direct-fact answer;
3. một multi-source synthesis answer;
4. một conditional/conflicting-evidence answer;
5. một out-of-scope answer phải trả exact insufficient-evidence fallback.

Một failed call vẫn được tính và không được thay bằng call thứ sáu. Nhánh lỗi
provider không xuất hiện tự nhiên được ghi `not live-verified`; không dựng dead
URL, monkeypatch hoặc fake response để ép failure.

Reviewer độc lập đọc complete diff/report/artifact, chạy focused non-paid checks,
kiểm real read-only API/UI path và audit citation-to-evidence. Reviewer không tự
chi thêm paid call. Paid artifact chỉ được reuse khi configuration, timestamp,
call ledger và safe metadata đủ chứng minh đúng execution đã duyệt.

## 10. Privacy và data safety

- Bốn legacy và bốn Metadata v2 collections/build records giữ immutable và
  read-only.
- Không create, upsert, replace, reconcile, alias, payload-index, delete hoặc
  cleanup collection trong Phase 6.
- Không log hoặc serialize API key, Authorization header, full prompt, full
  context, private path, vectors hoặc raw provider body.
- Public API/UI không trả `chunk_id`, `domain`, source path, point ID, build
  identity, score, rank, search text hoặc retrieval trace.
- Tracked artifact không chứa corpus dump, private query set hoặc full payload.
- Representation B generated text không trở thành evidence hoặc citation.

## 11. Documentation lifecycle

Sau khi User duyệt amendment này, Reviewer mới viết một Implementation Plan và
Review Contract mới. Plan mới phải:

- tham chiếu amendment, Metadata v2 Spec và behavior còn hiệu lực từ Phase 6
  Spec ngày 2026-09-14;
- dùng source/runtime interfaces hiện tại thay vì giả định pre-Metadata-v2;
- định nghĩa exact changed paths, commands, evidence và stop conditions;
- giữ một Implementer handoff cùng internal non-paid gate;
- không chép lại toàn bộ plan lịch sử hoặc tạo requirement thứ hai.

Chỉ sau khi User duyệt Plan mới, Reviewer mới cập nhật canonical guide/status và
`CURRENT_HANDOFF.md` để mở implementation. Git commit/push là quyền riêng, không
được suy ra từ design/spec/plan approval.

## 12. Acceptance criteria

Written Spec amendment đạt khi:

1. behavior Phase 6 ngày 2026-09-14 được giữ nguyên ngoài exact delta đã nêu;
2. Metadata v2 là retrieval/readiness dependency duy nhất của Phase 6;
3. private corpus provisioning và clean-clone-not-ready behavior được định nghĩa
   rõ mà không thêm recovery automation;
4. context/citation tiếp tục chỉ dùng exact evidence provenance;
5. Metadata v2 private identity không lộ qua prompt evidence, API hoặc UI;
6. startup và typed public failures fail closed, không fallback;
7. một Implementer handoff có non-paid gate bắt buộc trước đúng năm paid calls;
8. verification dùng hệ thống thật và ghi đúng failed/skipped/not-verified;
9. collection/data immutability và secret/privacy boundaries được giữ;
10. old spec/plan được giữ nguyên làm history và chưa có implementation/Git
    authority trước approval riêng của Plan mới.

## 13. Explicit exclusions

Amendment không mở:

- thay model/provider/profile, retrieval algorithm hoặc validation cell;
- benchmark winner selection, full Representation B build hoặc new indexes;
- domain filtering/routing hoặc public metadata expansion;
- corpus curation, reconstruction, download, sync hoặc backup implementation;
- Golden/evaluator change, Phase 7, Phase 8 hoặc Agentic RAG;
- production deployment/cutover, collection cleanup hoặc destructive action;
- streaming, conversation state, authentication hoặc frontend framework
  migration.

Mọi thay đổi các ranh giới trên cần design và authority riêng.
