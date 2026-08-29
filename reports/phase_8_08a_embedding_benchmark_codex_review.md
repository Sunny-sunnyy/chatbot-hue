# Codex Review: Phase 8 — Notebook 08a Dense Embedding Benchmark

Decision: changes_requested
Reviewer: Codex
Date: 2026-08-28 +07
Canonical guide: `guides/phase_8_benchmark_model_selection.md`
Implementation report: `reports/phase_8_08a_embedding_benchmark_implementation_report.md`

## 1. Phạm vi đã review

Reviewer đã đọc toàn bộ workflow, status/session prompt, template, các guide Phase 0/8, benchmark summary, LLM/RAG reference, exact 08a design/implementation plan, Golden V3 design/review, 45-case full dataset, 10-case smoke dataset và implementation report.

Reviewer đã đọc toàn bộ exact diff và mọi untracked file trong 08a allowlist: dependency changes, hai backend modules, test module, notebook, long-format CSV và implementation report. Không quan sát changed file ngoài allowlist. Golden V3, production settings và production embedder không có diff.

Static model-contract review bao gồm installed `FlagEmbedding==1.4.0` source tại `.venv/lib/python3.13/site-packages/FlagEmbedding/inference/embedder/encoder_only/m3.py`, cùng official BGE-M3 và Qwen3 Embedding sources mà implementation dựa vào:

- https://github.com/FlagOpen/FlagEmbedding/blob/master/research/BGE_M3/README.md
- https://github.com/FlagOpen/FlagEmbedding/blob/master/FlagEmbedding/inference/embedder/encoder_only/m3.py
- https://github.com/QwenLM/Qwen3-Embedding/blob/main/evaluation/qwen3_embedding_model.py

Theo chỉ đạo mới nhất của user, live verification chỉ chạy lại E5-small 384D, Multilingual MiniLM-L12 384D và E5-base 768D. Reviewer không dùng kết quả E5-large/BGE-M3/Qwen3 làm PASS evidence.

## 2. Findings

### major — BGE exact-batch adapter không đưa model vào inference mode

`BGEM3DenseRunner._encode_exact_batch()` gọi underlying model dưới `torch.no_grad()` nhưng không gọi `model.eval()`; `load()` cũng không thực hiện bước này (`backend/embedding/dense_benchmark.py:349`, `backend/embedding/dense_benchmark.py:364`). `no_grad()` không tắt dropout/training behavior. Official installed BGE-M3 public encode path thực hiện `self.model.float()`, `self.model.to(device)` và `self.model.eval()` trước inference (`.venv/lib/python3.13/site-packages/FlagEmbedding/inference/embedder/encoder_only/m3.py:342`). Vì adapter cố ý bỏ qua public auto-shrink loop, nó cũng vô tình bỏ qua inference preparation bắt buộc. BGE dense vectors có thể không deterministic hoặc không tương đương official behavior.

Correction: chuẩn bị underlying model một lần với exact CPU FP32 inference state trước mọi exact-batch forward, và thêm deterministic focused test đối chiếu một exact batch với official `dense_vecs` path theo approved plan.

### major — CSV category rows thiếu candidate-minus-control metric deltas

Mọi category row luôn ghi rỗng `delta_recall_at_5`, `delta_mrr_at_5` và `delta_ndcg_at_5` (`backend/evaluation/embedding_benchmark.py:805`). Fresh CSV xác nhận ví dụ `e5-base-768 + relationship` có cả ba delta rỗng dù gate là `False`. Exact approved plan yêu cầu category rows giữ metric, candidate-minus-control deltas và category guardrail result. Artifact bền vững hiện không đủ bằng chứng để audit nguyên nhân pass/fail theo category.

Correction: tính ba simple category deltas từ cùng control/candidate category aggregates, persist vào chín category rows của mỗi candidate, và thêm test exact overall + 9 rows kiểm tra giá trị delta.

### major — CSV upsert không validate exact header trước khi rewrite

Khi file đã tồn tại, `upsert_embedding_results_csv()` đọc bất kỳ header nào rồi silently project dữ liệu về `CSV_COLUMNS` (`backend/evaluation/embedding_benchmark.py:404`, `backend/evaluation/embedding_benchmark.py:426`). Một file thiếu, thừa hoặc đổi tên cột sẽ bị rewrite và có thể mất evidence thay vì fail rõ ràng, trái contract “validate exact known columns”.

Correction: từ chối file hiện hữu nếu `DictReader.fieldnames` không bằng exact ordered `CSV_COLUMNS`; thêm test cho missing/extra/reordered header và test idempotent upsert key `setting_key + category`.

### major — Public benchmark entry point không khóa exact supported setting/target và active snapshot

`run_embedding_benchmark()` nhận một `DenseBenchmarkSetting` tùy ý rồi copy trực tiếp `model_id`, dimension và `collection_name` sang settings dùng để tạo/upsert Qdrant (`backend/evaluation/embedding_benchmark.py:501`). Không có validation rằng object bằng một trong bảy approved settings, collection thuộc exact isolated target allowlist, hoặc active snapshot vẫn bằng baseline trước mutation. Notebook hiện truyền constants đúng, nhưng reusable production backend không bảo vệ boundary mà approved plan yêu cầu; caller khác có thể ghi vào collection ngoài 08a.

Correction: fail closed trước model load/Qdrant mutation nếu setting không khớp exact approved constant hoặc target là active/non-allowlisted; truyền expected active snapshot vào orchestration và kiểm tra tại các safety boundaries. Thêm focused test chứng minh arbitrary setting và active target bị từ chối trước mọi write.

### major — Error sanitizer vẫn có thể persist signed URL query và raw authorization header

`sanitize_benchmark_error()` chỉ redact một số `name=value` và Bearer token (`backend/evaluation/embedding_benchmark.py:378`). Fresh deterministic probe với `X-Amz-Credential`, `X-Amz-Signature` và `Authorization: Basic ...` trả lại nguyên chuỗi. Vì status/error được persist vào CSV, download/provider failure có thể làm lộ credential/query/header, trái approved failure-evidence contract.

Correction: loại bỏ toàn bộ URL query string và raw authorization/header-like fields trước truncate/persist; bổ sung tests cho signed URLs, Basic authorization, cookies và nested causes.

### major — Notebook chưa hiển thị category evidence theo exact approved design

Notebook parse được, sạch output, dùng Markdown tiếng Việt/identifier tiếng Anh, control có cell riêng và sáu candidate nằm trong một sequential cell. Tuy nhiên phần kết quả chỉ hiển thị aggregate quality, comparison, latency, resource và failures; không có bảng chín category với case/hit counts, metric deltas và per-category guardrails (`notebooks/08a_embedding_benchmark.ipynb:246`). Vì category gates là một tiêu chí quyết định chính, user không thể audit trực tiếp bằng notebook như exact design yêu cầu.

Correction: thêm một display helper/backend view đơn giản và cell ngắn để trình bày category rows; giữ notebook chỉ orchestration/display, không duplicate scoring logic. Kết luận phải nêu rõ observed lighter/heavier trade-off từ các bảng, không tự cutover.

### minor — Category identity chưa được validate trước guardrail grouping

`evaluate_category_guardrails()` kiểm tra length và ordered case IDs nhưng không kiểm tra category của từng case (`backend/evaluation/embedding_benchmark.py:242`). Candidate có cùng IDs nhưng category sai có thể bị regroup/zip im lặng thay vì fail input validation.

Correction: yêu cầu ordered `(case_id, category)` identity khớp exact và thêm mismatch test. Nên áp dụng cùng invariant cho paired inputs trước bootstrap để evidence pairing rõ ràng.

Không phát hiện blocker. Các runner E5/MiniLM/Qwen static contract, exact Vietnamese Qwen instruction, official `truncate_dim=384`, batch sizes, normalization, dense-only Qdrant schema, duplicate evidence credit, top-30/top-5, 1 warm-up + 3 repetitions, bootstrap 10,000/seed 42 và finalist 3/3 logic đều phù hợp trong phần source đã review.

## 3. Cách Reviewer chạy lại thật

Focused deterministic tests:

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-review-uv-cache \
  uv run --env-file ../.env python -m pytest tests/test_embedding_benchmark.py -q --tb=short
```

Kết quả: `12 passed, 1 warning in 6.34s`.

Three-model live verification theo giới hạn mới nhất của user:

```bash
cd /home/minhhieu/hue_rag/backend
PYTHONPATH=. UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-review-uv-cache \
  uv run --env-file ../.env python /tmp/phase8_08a_three_model_review.py
```

Temporary reviewer script gọi trực tiếp production `load_embedding_benchmark_inputs()`, `run_embedding_benchmark()` và `run_embedding_benchmarks()` với tuple hard-code chỉ gồm `MINILM_L12_SETTING` và `E5_BASE_SETTING` sau control `E5_SMALL_SETTING`. Nó dùng real pinned local models, canonical 45 cases, 572 chunks và actual isolated Qdrant collections; không dùng mock, fake vectors, replay hay output cũ.

Reviewer còn chạy `git diff --check`, kiểm tra JSON/notebook outputs bằng `jq`, đọc full current status/diff, truy vấn Qdrant collection info qua local API và chạy deterministic sanitizer probe. `git diff --check` không có output.

## 4. Kết quả quan sát

Fresh three-model results:

| Setting | Status | Hits | Recall@5 | MRR@5 | nDCG@5 | Repetitions | Stable | Truncated |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E5-small 384D | completed | 41/45 | 0.818519 | 0.774815 | 0.742538 | 3 | true | 0 |
| MiniLM-L12 384D | completed | 34/45 | 0.581481 | 0.514444 | 0.470909 | 3 | true | 83 |
| E5-base 768D | completed | 42/45 | 0.840741 | 0.698519 | 0.706088 | 3 | true | 0 |

Reviewer tự tính lại `foods-v3-0002`: hai exact relevant `source + section` pairs xuất hiện ở hai rank đầu, nên Recall@5 = 1, MRR@5 = 1 và nDCG@5 = 1; kết quả khớp stored `CaseMetrics`. Reviewer cũng tính lại `relationship` gate của E5-base: control 14 hits, candidate 13 hits, manual result `False`, khớp persisted gate.

Ba collection được phép đều green, dense-only, đúng 572 points và dimensions 384/384/768. Active `hue_foods_e5_small_384` trước/sau đều 572 points, dense 384D cosine và sparse vector name `sparse`; production config không đổi.

Notebook repository hợp lệ nbformat 4, mọi code cell có `outputs: []` và `execution_count: null`; không quan sát secrets/output payload trong notebook.

## 5. Giới hạn hoặc phần chưa chạy

Theo chỉ đạo mới nhất của user, Reviewer không chạy lại BGE-M3 hoặc hai Qwen3 configurations, và không dùng chúng làm PASS evidence. BGE finding dựa trên full static comparison với exact installed FlagEmbedding 1.4.0 source.

Trước khi nhận giới hạn mới, Reviewer đã bắt đầu temporary full Notebook Run All theo reviewer workflow. Khi user đổi giới hạn, process được interrupt và xác nhận không còn nbconvert/ipykernel process. Tuy nhiên E5-large đã hoàn tất trước thời điểm chỉ đạo mới và đã tạo `hue_foods_08a_e5_large_1024` 572-point dense-only collection cùng 10 CSV rows. Reviewer không chạy lại hoặc dùng kết quả đó để đánh giá PASS, không tự ý xóa artifact. Vì vậy current CSV có 40 data rows thay vì 30 rows mô tả trong implementation report.

Không có BGE/Qwen collection nào được tạo bởi lượt verification ba-model sau chỉ đạo mới.

## 6. Decision và bước tiếp theo

Decision là `changes_requested` vì còn sáu `major` findings ảnh hưởng model correctness, durable evidence, safety boundary, secret sanitation và notebook auditability.

Implementer cần sửa đúng các findings trên, bổ sung focused deterministic tests tương ứng, làm sạch/rerun repository notebook theo phạm vi user cho phép và viết implementation report vòng sửa mới. Reviewer không sửa runtime code, không commit/push, không tạo user report và không đánh dấu Notebook 08a hoặc Phase 8 approved. Phase 8 tổng thể tiếp tục `not_ready`; Notebook 08b vẫn đóng.

## 7. Reviewer Addendum — vòng sửa và scope amendment ngày 2026-08-28 +07

Decision tiếp tục là `changes_requested`.

### 7.1. Kết quả kiểm tra phản hồi vòng sửa

Reviewer đã đọc lại source/test/notebook/report và chạy độc lập:

```bash
cd /home/minhhieu/hue_rag/backend
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase8-08a-review-fix-uv-cache \
  uv run --env-file ../.env python -m pytest tests/test_embedding_benchmark.py -q --tb=short
```

Fresh result: `17 passed, 1 warning in 5.44s`. Notebook vẫn parse được, mọi repository output rỗng và `execution_count: null`. `git diff --check` pass.

Các corrections về BGE inference state, category deltas, exact CSV header, sanitizer, category table/trade-off display và ordered `(case_id, category)` identity hiện phù hợp ở static/focused-test level. BGE không được chạy live theo giới hạn hardware mới nhất của user.

### 7.2. Finding còn mở — exact setting boundary chưa fail closed hoàn toàn

Severity: `major`.

`run_embedding_benchmark()` hiện chỉ kiểm tra `setting.setting_key in APPROVED_SETTING_KEYS` và `setting.collection_name in APPROVED_COLLECTIONS` như hai điều kiện độc lập (`backend/evaluation/embedding_benchmark.py:524`). Một frozen dataclass giả có approved key nhưng thay `model_id`, revision, dimension hoặc ghép sang approved collection của model khác vẫn qua boundary. Ngoài ra `expected_active_snapshot` vẫn optional, nên caller có thể bỏ qua invariant bằng `None`. Điều này chưa đáp ứng correction “object bằng exact approved constant” và “active baseline bắt buộc” trong review trước.

Correction bắt buộc:

- map exact key sang canonical frozen setting rồi yêu cầu equality toàn object;
- tách full model catalog khỏi exact user-authorized run tuple;
- reject every non-local setting trước model load/download/Qdrant write;
- biến expected active snapshot thành input bắt buộc cho mutation path;
- thêm tests cho forged approved key, cross-wired approved collection, changed revision/dimension và omitted/mismatched snapshot.

### 7.3. User-authorized model/run scope mới

Historical research catalog có tám configurations, nhưng exact executable local Run All hiện chỉ được phép chạy 5 configurations:

1. `e5-small-384` — control;
2. `multilingual-minilm-l12-384`;
3. `huydang-dek21-embedding-768` — mới;
4. `e5-base-768`;
5. `qwen3-embedding-0.6b-384`.

Ba configurations sau không còn được phép chạy local trên máy này và phải bị runtime boundary từ chối:

- `e5-large-1024`;
- `bge-m3-dense-1024`;
- `qwen3-embedding-0.6b-1024`.

Không dùng dimension đơn thuần làm thứ tự “lighter”. Proposed sequential/resource order ở trên đặt model PhoBERT khoảng 135M parameters trước E5-base và Qwen 0.6B; Implementer phải ghi rõ order này trong design amendment. Không thêm registry/framework/CLI selector/resume engine; chỉ cần một explicit immutable full catalog và một explicit immutable authorized-run tuple.

Notebook control cell giữ riêng. Candidate cell phải loop đúng authorized tuple gồm MiniLM, Huydang 768D, E5-base và Qwen3 384D; không được loop historical catalog. Settings table cần phân biệt rõ `authorized_local`, `remote_proposal_only` và `excluded`.

### 7.4. Research contract — `CODE4LIFEOFFICIAL/huydang-dek21-embedding`

Primary source: [Hugging Face model card](https://huggingface.co/CODE4LIFEOFFICIAL/huydang-dek21-embedding), pinned repository revision `517f1af7dd04a57194f1de2990f0c6ede0a3109b`.

Observed official artifacts at that revision:

- Sentence Transformers / RoBERTa-PhoBERT architecture, native 768D, FP32;
- 12 layers, hidden size 768, approximately 135M parameters;
- `max_seq_length=256` and tokenizer `model_max_length=256`;
- mean-token pooling, cosine similarity, no configured prompt/default prompt;
- Apache-2.0 model license;
- human-written model card recommends Vietnamese word segmentation with `ViTokenizer.tokenize()` because the PhoBERT input was pretrained on segmented Vietnamese;
- model was fine-tuned on approximately 100,000 in-house Vietnamese legal query/context examples using Matryoshka and Multiple Negatives Ranking losses;
- repository is about 2.16 GB because it also contains ONNX/training artifacts, while the FP32 safetensors weights are about 540 MB.

Implementation contract:

- exact setting key: `huydang-dek21-embedding-768`;
- exact collection: `hue_foods_08a_huydang_dek21_768`;
- exact requested repository and pinned SHA above; do not substitute the older `huyydangg/DEk21_hcmute_embedding` identifier shown inside copied usage text;
- native 768D only; no slicing, PCA or Matryoshka truncation in this configuration;
- `SentenceTransformer` on CPU FP32, document batch 8, query batch 1, `max_seq_length=256`, `normalize_embeddings=True`;
- apply the same deterministic `ViTokenizer.tokenize()` preprocessing to every query and document before truncation counting/encoding;
- no query/passage prefix because the pinned Sentence Transformers config defines no prompt;
- count `truncated_document_count` after native word segmentation with the pinned tokenizer/max length;
- prefer native `SentenceTransformer(..., revision=PINNED_SHA, device="cpu")` loading so unused `optimizer.pt`, RNG, training args and ONNX artifacts are not deliberately downloaded;
- evaluate only against canonical Hue-foods evidence. The self-reported model-card results are legal-domain and unverified, so they are motivation for a local benchmark, not PASS evidence.

The model card's PyVi preprocessing recommendation introduces a new dependency. [PyVi 0.1.1](https://pypi.org/project/pyvi/) is an older MIT-licensed release. Implementer must first prove it installs and tokenizes deterministically in the exact Python 3.13 environment, then pin it in `pyproject.toml`/`uv.lock`. If it is incompatible, stop and report the exact failure; do not silently fall back to raw text or switch tokenizers.

Focused tests required for the new runner:

- exact setting/revision/dimension/max length/collection;
- exact PyVi output for representative Vietnamese food text;
- identical preprocessing contract for documents and queries;
- native mean-pooling path and L2-normalized 768D outputs;
- truncation count performed on preprocessed text;
- approved runner accepts the exact canonical setting and rejects a forged variant;
- isolated Qdrant schema is dense-only cosine 768D with 572 points after a successful run.

### 7.5. Qwen3 384D authorization

`qwen3-embedding-0.6b-384` is now authorized for local execution. Existing exact Vietnamese instruction, official Sentence Transformers `truncate_dim=384`, last-token pooling/native normalization, CPU FP32, document batch 8 and query batch 1 remain unchanged. No slicing/PCA, quantization, retry, auto-shrink, fallback or device/dtype/revision change is allowed. OOM/failure must persist the exact sanitized status/error and stop that setting normally.

This authorization does not extend to Qwen3 native 1024D.

### 7.6. Required live verification and artifact reconciliation

After implementation, run one discarded warm-up plus three full 45-case repetitions sequentially for exactly the five authorized settings. Verify five dense-only collections with 572 points and dimensions 384/384/768/768/384, reconcile 50 long-format data rows (`overall + 9 categories` per authorized setting), recompute one metric sample and category gate, and prove the active production snapshot/config unchanged.

User subsequently authorized cleanup. Reviewer verified the exact target as a green dense-only 1024D collection with 572 points, deleted `hue_foods_08a_e5_large_1024`, and removed the 10 CSV rows keyed `e5-large-1024`. The Qdrant deletion is not recoverable except by a new embedding/index run; the removed CSV evidence was untracked and must not be reconstructed as PASS evidence.

After the five local settings complete, a separate proposal may evaluate OpenRouter `intfloat/multilingual-e5-large` and `baai/bge-m3` dense embeddings. This is not current API-call or paid-run authorization. Qwen3 native 1024D remains excluded, and OpenRouter dense BGE output does not reopen learned sparse/ColBERT scope.

Implementer must update the exact 08a design/plan, implementation report, source/tests/notebook and allowlist description for this eight-model catalog/five-model authorized run. Reviewer will perform a new independent review after the new implementation report exists. No production cutover, Notebook 08a approval, Notebook 08b work, commit or push is authorized.

## 8. Reviewer Addendum — Qwen removal và four-model handoff ngày 2026-08-29 +07

Decision tiếp tục là `changes_requested`.

User đã loại `qwen3-embedding-0.6b-384` khỏi local Phase 8 sau khi evidence hiện
có cho thấy candidate này thấp hơn E5-small về quality, không đạt category
guardrails và quá chậm trên CPU. Quyết định mới supersede catalog tám model/five
authorized settings trong Section 7. Exact executable 08a scope chỉ còn:

1. `e5-small-384`;
2. `multilingual-minilm-l12-384`;
3. `huydang-dek21-embedding-768`;
4. `e5-base-768`.

Reviewer đã chạy focused tests mới: `23 passed, 1 warning in 6.05s`. Hai lượt
temporary Notebook Run All bị Reviewer/user interrupt trong Qwen stage; trước
đó cả bốn model được giữ lại đã ghi fresh 3/3 evidence trên 45 cases và 572
chunks vào CSV lúc `2026-08-29 08:21:50 +07`. Theo quyết định trực tiếp của user,
Reviewer vòng sau không cần chạy lại bốn model nếu correction chỉ xóa
Qwen/deferred paths và không đổi encoding, retrieval, scoring hoặc metric logic.

Fresh retained-model latency summary từ CSV:

| Setting | Status | Repetitions | Document embedding | Warm total p50/p95 |
|---|---:|---:|---:|---:|
| E5-small 384D | completed | 3/3 | 19.81 s | 27.40 / 39.75 ms |
| MiniLM-L12 384D | completed | 3/3 | 15.77 s | 29.34 / 48.31 ms |
| Huydang DEk21 768D | completed | 3/3 | 44.38 s | 71.24 / 114.62 ms |
| E5-base 768D | completed | 3/3 | 47.15 s | 57.09 / 88.44 ms |

Qwen historical CSV rows được giữ để giải thích rejection. Theo exact cleanup
authorization, Reviewer đã xóa cache Hugging Face Qwen khoảng 1.2 GiB và
isolated collection `hue_foods_08a_qwen3_06b_384`; active collection không thuộc
cleanup target. Các artifact này chỉ phục hồi được bằng download/reindex mới và
không được tái tạo trong current scope.

Current implementation vẫn giữ Qwen settings/runner, ba deferred 1024D settings,
local BGE runner, `FlagEmbedding` dependency, catalog/table tám model và notebook
loop bốn candidates. Đây là `major` scope/over-engineering finding so với exact
four-model amendment. Implementer phải xóa các path/dependency/test/display đó,
giữ CSV Qwen như historical evidence, cập nhật implementation report và bàn giao
lại. Reviewer không sửa runtime code thay Implementer và chưa tạo user report.
