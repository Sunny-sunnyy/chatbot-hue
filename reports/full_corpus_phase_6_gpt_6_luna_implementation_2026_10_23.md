# Implementation Report: Phase 6 gpt-6-luna + Qdrant port amendment

Implementer: Claude Opus 5.5 (session `hue-rag-08`)
Date: 2026-10-23 (+07)
Base commit: `151bc53865faec5618be0b4a9ef6c5f3d5f1b66c`
Head commit: worktree (chưa commit; Git authorization của Implementer: none)
Risk level: high
Canonical inputs:

```text
docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md
handoff_prompt/PHASE_6_OPENAI_BASELINE_REVIEW_CONTRACT.md
guides/phase_6_generation_api.md
```

Paid-call authorization: **consumed**. Đã chạy đúng một runner invocation,
`call_attempt_count = 5`, không retry, không có call thứ sáu và không rerun.

## 1. Phạm vi

Scope được duyệt (amendment §4, User ngày 2026-10-23) gồm hai thay đổi: đổi mọi
model OpenAI sang `gpt-6-luna`, và đổi host port Qdrant của hue_rag sang
`127.0.0.1:6335/6336` để chạy song song với `mekongai-template` đang giữ
6333/6334. Thứ tự đã thực hiện:

1. Gửi nhận xét khả thi cho Reviewer. Reviewer chấp nhận và chốt Q2 là (a):
   cập nhật 5 chuỗi Markdown trong notebook.
2. Sửa đúng các path trong §4.
3. Chạy `docker compose up -d` cho hue Qdrant trên 6335, không đụng container
   Mekong.
4. Chạy non-paid gate §7 bước 1–8: đều PASS.
5. Reviewer gửi `GO` và ghi fingerprint vào `CURRENT_HANDOFF.md` §4. User xác
   nhận trong session Implementer. Tôi tính lại `sha256sum -c` (15/15 OK) ngay
   trước khi chạy, rồi chạy đúng một paid invocation.
6. Làm các bước post-run trong handoff §5, gồm phân tích `conditional_evidence`
   theo amendment §6. Không sửa code.

Không sửa prompt, cases, retrieval, context packer, citations, API/UI, runner
logic, dependencies hoặc Qdrant data. Không xóa container hay volume nào.

## 2. Thay đổi chính

12 file, 26 dòng thêm / 26 dòng xóa, tất cả thuộc amendment §4:

| Path | Thay đổi |
|---|---|
| `backend/config/settings.yaml` | `vector_database.url` → `http://localhost:6335`. `llm.answer_model`, `evaluation.answer_model`, `evaluation.judge_model` (trước là `gpt-5.4-mini`) và `full_corpus_generation.model` → `gpt-6-luna`. Comment "verified 2026-08-13" thay bằng nguồn quan sát mới và ghi chú R4 |
| `backend/core/settings_loader.py` | guard model của Phase 6 → `gpt-6-luna` |
| `backend/llm/openai_tokenizer.py` | `OPENAI_GENERATION_MODEL` → `gpt-6-luna`; encoding vẫn là `o200k_base` |
| `backend/llm/generator_openai_full_corpus.py` | comment và default `config.get("model", ...)` → `gpt-6-luna` |
| `backend/ingestion/full_corpus_pipeline.py` | guard URL Phase 4 → `http://localhost:6335` |
| `docker-compose.yml` | ports `"127.0.0.1:6335:6333"`, `"127.0.0.1:6336:6334"`; image digest và volume giữ nguyên |
| `backend/tests/test_phase6_settings.py`, `test_openai_full_corpus_generator.py`, `test_phase6_live_smoke.py`, `test_llm_generator_openai.py` | chỉ đổi chuỗi model mà test kỳ vọng |
| `notebooks/06_generation_and_api.ipynb` (3), `notebooks/07_evaluation.ipynb` (2) | chỉ đổi chuỗi model trong Markdown đang mô tả cấu hình hiện hành. Code cells giống HEAD từng byte, outputs rỗng, mọi `execution_count` là `null` |

Không có thay đổi logic. Data flow giữ nguyên. Thay đổi duy nhất là giá trị
model và URL, cùng các guard đang khóa cứng giá trị cũ.

Ghi chú SDK (R3): Agents SDK 0.19.4 có bảng default reasoning theo tên model,
trong đó có `gpt-5.6-luna` nhưng không có `gpt-6-luna`. Bảng này không áp dụng
ở đây vì agent nhận một instance `OpenAIResponsesModel`, nên SDK resolve
implicit settings thành `ModelSettings()` rỗng. Reviewer xác nhận id
`gpt-6-luna` xuất hiện nguyên văn trong `GET /v1/models` và là id khác với
`gpt-5.6-luna`.

## 3. Cách đã chạy thật

Mọi lệnh chạy từ `/home/minhhieu/hue_rag`, trừ các lệnh có ghi `backend/`.
Secrets được nạp qua `--env-file`; không giá trị secret nào bị in ra.

| # | Lệnh | Exit / kết quả |
|---|---|---|
| G1 | `git diff --check` (chạy trước gate và sau bước 8) | exit 0 cả hai lần |
| G2 | `docker compose up -d` | tạo `hue_rag-qdrant-1`, digest `0bd98fa7…` (Qdrant 1.18.3), `127.0.0.1:6335->6333`, `127.0.0.1:6336->6334` |
| G2 | `curl http://localhost:6335/collections` | `ok`, 15 hue collections |
| G2 | `curl http://localhost:6333/` | HTTP 200 (Mekong vẫn chạy, không bị đụng) |
| G3 | `UV_CACHE_DIR=/tmp/hue-rag-phase6-review-verify-uv-cache uv run --env-file .env python -m backend.ingestion.full_corpus_metadata_v2 verify` | `Verification status: VERIFIED`, exit 0 |
| G3 | exact count `POST /collections/<name>/points/count` × 4 metadata-v2 targets trên 6335 | 8460 × 4 = 33.840 |
| G4 | Check 1 focused suite từ `backend/` (cùng 9 file test như report 2026-10-01 §4) | `141 passed, 1 warning in 58.28s` |
| G5 | `tiktoken.encoding_for_model("gpt-6-luna")` | `KeyError`, ghi R1 = **not verified** |
| G5 | construction-only `OpenAIFullCorpusGenerator.from_environment(load_settings())`, không gọi mạng | xem §4 |
| G6 | `uvicorn api.app:app --host 127.0.0.1 --port 8016` từ `backend/` + `curl /health` | HTTP 200, 5 components ready; server đã dừng, port đã đóng |
| G7 | parse artifact cũ (chỉ đọc metadata) | ledger cũ còn nguyên |
| G8 | `sha256sum` 15 fingerprint files | gửi Reviewer; Reviewer tự tính và thấy khớp |
| P0 | `sha256sum -c` theo fingerprint `CURRENT_HANDOFF.md` §4, chạy ngay trước invocation | 15/15 OK; không có runner process nào khác |
| P1 | paid invocation đúng như handoff §3 (từ `backend/`, `--confirm-paid`) | exit 1 (overall FAIL); xem §4 |
| P2 | Metadata v2 verify + 4 exact counts sau run | `VERIFIED`; 8460 × 4 |

Không chạy `test_llm_generator_openai.py`, vì file này chứa live paid test
ngoài scope. Không chạy Foods evaluation.

Fingerprint đã được Reviewer duyệt (`GO`) và đã khớp 15/15 ngay trước
invocation:

```text
8eae4b39b1b52b45e6fc101c563a39325e3e115323d134a24549a970df6a6542  data/full_corpus_phase_6_live_cases.json
b503daf929cce3101eadf8152d4319030c2d0a333f213701a843ab5656047b64  backend/llm/phase6_live_smoke.py
4111af729e0b12da9a68747f2d4fceadcbb02a292dcecf53787e4b70ace862e2  backend/llm/evidence_recorder.py
d3b88a16ef622ddd8569d7219490ca8581636a0621a1d5a1250bf018dc8aefe8  backend/llm/generator_openai_full_corpus.py
3ca145b82fa308663ff52bc78fbf033b9fb267172178588f3bed00046b4cfd39  backend/llm/full_corpus_prompt.py
8877af4a6ea066eae3c19ce164b6ce598ee0c70f3f2997b203cdf3b32af0bbf2  backend/llm/openai_tokenizer.py
e323a504acd43982d33cd2558825079c783b323fee7f0693c4a8b2275c8feaec  backend/llm/representation_b.py
de78c742dd04d00d7fec9c1c1214a638ebcb74e1957adb95333598fca10fbe19  backend/api/app.py
13670088d25a46ee1806d6925e16de439d2712395bd37bf107814c5d1ea8f30d  backend/api/routes/chat.py
c71b2191d530dd5bc450923a6c065cf4eb02008e83050274d56bca50225f616b  backend/retrieval/full_corpus_context.py
abaee46b3b51780fb2067e0c686190de279ecfa12f4652843b1cd360a6f861a5  backend/llm/citations.py
e4d3fe6bee4b268483c1f43b711653b772364ff296af71a919870e1ca29ee341  backend/config/settings.yaml
5393203d47c524b3828d3e1e12927c1e778c00a1a67556dae57bec29c029a095  backend/core/settings_loader.py
c87a66fd34c36c67c3a90328828d94dd0489cb0204cef2acdfc9524d5fb9ace9  pyproject.toml
61e77b5a50c30e55728eaa1ede1dc7bb89789e11cf99d20c3b4ab1fea75ba984  uv.lock
```

## 4. Kết quả quan sát

### Non-paid gate (bước 1–8): PASS

- Versions: openai 2.53.0, openai-agents 0.19.4, tiktoken 0.14.0, httpx 0.28.1.
  Không đổi `uv.lock` hay `pyproject.toml` (hash khớp fingerprint).
- Construction: `generator.model` và `responses_model.model` là `gpt-6-luna`;
  client `max_retries=0`, `timeout=45`; Runner `max_turns=1`; `RunConfig`
  `tracing_disabled=True`. Agent answer có `max_tokens=2048`, agent
  Representation B có `max_tokens=256`; cả hai có `include_usage=True`,
  `store=False`, 0 tools. Không có `temperature`, `top_p`, `reasoning`,
  `verbosity` hay `extra_*` nào khác `None`. Sau khi merge với implicit
  settings, reasoning, temperature và verbosity vẫn là `None`.
- Tokenizer ứng dụng load `o200k_base`.
- `/health`: `{"status":"ok"}`. Components: app alive; qdrant, retrieval,
  tokenizer và generator ready.
- Artifact cũ trước run: status FAIL, 5 attempts, PASS/FAIL/PASS/FAIL/PASS,
  model `gpt-5.4-nano`, mtime 2026-10-01 20:43:51 +07.

### Paid invocation: artifact `data/full_corpus_phase_6_live_smoke.json` (ignored/private)

- `schema_version` `phase_6_full_corpus_live_smoke:v2`; `timestamp_utc`
  2026-10-23T03:22:10Z; git commit `151bc53…`, `dirty: true`.
- `call_attempt_count = 5`. Checks: `exact_five_attempts = true`,
  `point_count_intact = true`, `all_calls_pass = false`. Overall **FAIL**,
  runner exit 1.
- Configuration ghi trong artifact: provider `openai`, model `gpt-6-luna`,
  `o200k_base`, caps 2048/256, timeout 45, context 16384/2048/512,
  `max_retries 0`, `max_turns 1`; temperature, reasoning và top_p override
  đều `null`.
- Qdrant before/after (runner đếm `hue_full_corpus_a_e5_small_384_metadata_v2`):
  8460 / 8460. Sau run, verify độc lập cho cả 4 targets: `VERIFIED`, 33.840
  points.
- Artifact parse được; grep không thấy `sk-`, `Traceback` hay `api_key`. Không
  có raw provider exception.

| Attempt | Case | Status | Latency (ms) | Tokens in/out/total | Ghi chú an toàn |
|:---:|---|:---:|---:|---|---|
| 1 | `representation_b` | PASS | 4218 | 296 / 104 / 400 | search context không rỗng |
| 2 | `direct_fact` | PASS | 3268 | 1239 / 241 / 1480 | citations [1,5,2,3], sources [1,2,3,5] |
| 3 | `multi_source_synthesis` | PASS | 2504 | 1018 / 147 / 1165 | citation [3], 1 source |
| 4 | `conditional_evidence` | **FAIL** | 1902 | 807 / 89 / 896 | trả `INSUFFICIENT_ANSWER`, 0 sources |
| 5 | `out_of_scope` | PASS | 2610 | 1184 / 31 / 1215 | đúng exact fallback, 0 sources |

Mọi attempt đều có `response_id`. `finish_reason` là `null` ở cả 5 attempt vì
Responses API không trả field `choices`; giá trị được ghi đúng là `null`. So với
artifact cũ (`gpt-5.4-nano`): `direct_fact` lần trước FAIL vì lỗi runner (502),
lần này **quan sát PASS**; `conditional_evidence` vẫn FAIL.

### Manual claim/citation-to-excerpt audit (đọc artifact private)

- `direct_fact`: có 3 câu nhận định, cite lần lượt [1], [5] và [2][3]. Mỗi câu
  đều được excerpt của source mà nó cite hỗ trợ. Không thấy claim nào thiếu
  nguồn và không có citation tới id không tồn tại.
- `multi_source_synthesis`: danh sách công trình là tập con nguyên văn của
  excerpt [3]. Lưu ý: câu trả lời chỉ dùng **một** source dù có 5 source được
  đóng gói. Runner chấm PASS vì tiêu chí chỉ yêu cầu citation hợp lệ, không yêu
  cầu tổng hợp nhiều nguồn. Ghi lại để Reviewer đánh giá; không coi đây là
  bằng chứng cho khả năng tổng hợp đa nguồn.
- `out_of_scope`: trả đúng chuỗi `INSUFFICIENT_ANSWER` với `sources: []`, dù
  context được đóng gói gồm các bảng giá vé không liên quan. Không bịa giá.

### `conditional_evidence`: phân tích theo amendment §6 (không sửa code)

- Packed evidence: 5 sources, 777 tokens (giống con số Reviewer probe trước
  đây). Cả 5 excerpt đều nói về **chính sách miễn/giảm phí** theo đối tượng và
  căn cứ quy định.
- Packed evidence **không** chứa giá vé niêm yết của Đại Nội. Trong khi đó,
  tài liệu vé của quần thể di tích trong private corpus có dòng bảng giá vé điểm
  đơn lẻ cho Đại Nội; dòng này không nằm trong top-5 được đóng gói. Câu hỏi hỏi
  cả giá vé lẫn chính sách miễn giảm, nên evidence chỉ đủ cho một nửa câu hỏi.
- Câu prompt có khả năng dẫn tới từ chối (`backend/llm/full_corpus_prompt.py`,
  `ANSWER_SYSTEM_INSTRUCTIONS`): "Nếu bằng chứng không đủ, trả đúng duy nhất
  câu sau, không thêm citation". Đây là quy tắc all-or-nothing, không cho phép
  trả lời phần có bằng chứng (miễn giảm) và nói rõ phần thiếu (giá vé). Model
  đã làm đúng quy tắc này.
- Nhận định: FAIL là kết hợp của (a) retrieval/packing không đưa chunk bảng giá
  vào top-5 và (b) chính sách fallback all-or-nothing của prompt. Đây là quan
  sát từ một case, **chưa phải root cause đã chứng minh**. Chưa chạy probe
  retrieval nào để xác định thứ hạng của chunk bảng giá. Theo §6, Reviewer
  quyết định correction và mọi lần chạy thêm.

## 5. Lỗi và giới hạn

- **Phase 6 live smoke overall FAIL** (4/5 PASS) vì `conditional_evidence`. Đây
  là kết quả thật, không retry và không rerun. Contingent authority của User
  (tối đa thêm một invocation sau correction được Reviewer duyệt và một `GO`
  mới) **chưa được dùng**.
- R1: `gpt-6-luna` dùng encoding nào là **not verified** (tiktoken không biết
  model này); ngân sách token của ứng dụng vẫn dùng `o200k_base`. Usage thật
  của provider (ví dụ input 807–1239 tokens) không bị vượt cap nào.
- R2: không thấy output bị cắt hay rỗng; output lớn nhất là 241/2048 tokens và
  104/256 tokens cho Representation B. Nhưng `finish_reason` là `null`, nên
  không xác nhận được từ field đó; usage không cho thấy reasoning tokens làm
  hết cap.
- R4: compatibility của `temperature` (Foods `llm.temperature: 0.2`, gửi qua
  `backend/evaluation/eval.py`) với `gpt-6-luna` là **not live-verified**. Phase
  này không chạy Foods generator hay evaluation.
- R5/R6: judge cùng model với generator, và benchmark Foods/Phase 7 cũ đo bằng
  `gpt-5.4-nano`. Hai giới hạn này ghi lại cho Phase 7B/8, không được đo ở đây.
- `multi_source_synthesis` PASS chỉ với một source (xem audit ở §4).
- Static UI, vendor hashes và keyboard citation behavior không được kiểm lại
  thủ công trong amendment này vì frontend không đổi. `tests/test_static_ui.py`
  nằm trong focused suite đã PASS.
- Không có cost accounting (SDK không cung cấp). Giới hạn chi phí là 5 attempts
  cộng các caps.
- Hue Qdrant container `hue_rag-qdrant-1` vẫn đang chạy trên 6335/6336 sau
  phiên này.

## 6. Handoff cho Reviewer

- Đọc trước: report này, sau đó là artifact private
  `data/full_corpus_phase_6_live_smoke.json` (calls 1–5, `packed_evidence` của
  call 4) và exact diff 12 file trong §2.
- Phần cần chạy lại theo Review Contract 2026-10-01 (đổi `gpt-5.4-nano` thành
  `gpt-6-luna`): `git diff --check`; focused suite; construction-only check;
  `/health` trên 6335; đếm attempt trong artifact và audit citation/excerpt.
  Reviewer không chạy paid call bổ sung.
- Quyết định cần Reviewer/User: correction cho `conditional_evidence`
  (retrieval/packing hay chính sách fallback của prompt), và có dùng contingent
  invocation hay không.
- Deviation: không có deviation ngoài scope. Q2 notebook (a) đã được Reviewer
  chốt trước khi sửa.
- Sub-agent: không dùng. Git: không commit/push.
