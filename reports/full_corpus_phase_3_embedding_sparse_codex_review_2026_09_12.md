# Codex Review: Phase 3 Full-corpus Dense Embedding và Biểu diễn Thưa

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-12 +07
Canonical guide: `guides/phase_3_embedding_sparse_representation.md`
Implementation report: `reports/full_corpus_phase_3_embedding_sparse_implementation_2026_09_12.md`

## 1. Phạm vi đã review

Reviewer đã:

- xác nhận handoff `reviewer/final_review`, base commit
  `071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f`, head `worktree`, risk `high`
  và Git authorization `none`;
- đọc toàn bộ implementation report, Review Contract, ba module Phase 3 mới,
  ba test file mới, Notebook 03, preflight evidence JSON và sparse state;
- kiểm complete worktree/path inventory và exact tracked diff; tách các thay đổi
  Reviewer-owned/pre-existing được bàn giao khỏi implementation Phase 3;
- đối chiếu Qwen device/dtype/eager/no-fallback path, sparse formula,
  deterministic serialization, evidence schema, sample 12 chunks, notebook
  cleanliness và immutable paths;
- chạy exact offline Reviewer suite, `git diff --check`, focused suite có BM25,
  sparse artifact round-trip và checksum checks.

Reviewer không lặp model download/inference, full tokenizer scan hoặc Notebook
Run All theo Review Contract.

## 2. Findings

### R1 — Major — Fresh Phase 2 identity gate chưa thực hiện đủ contract

Vị trí: `backend/evaluation/full_corpus_embedding_preflight.py:327-371` và
`:409-455`.

Requirement: plan yêu cầu đối chiếu status, exact source list,
file/chunk/condition counts và ba tokenizer maxima của fresh Phase 2 với
preserved artifact; bất kỳ mismatch nào phải trả `BLOCKED_PHASE_2` trước dense
inference.

Evidence: code đọc `expected_sources` nhưng không sử dụng. Nó chỉ so sánh số
file và số chunk; `condition_rules_count` được chép từ artifact thay vì tính và
đối chiếu; ba fresh tokenizer maxima được ghi sau đó nhưng không so với
`tokenizer_limits` của artifact. Không có kiểm tra ordered/non-empty source
identity tương ứng.

Tác động: một corpus có cùng file/chunk count nhưng đổi source membership,
condition count hoặc tokenizer input có thể vẫn được đánh `PASS` và tạo sparse/
dense evidence trên dependency khác Phase 2 đã đóng.

Tiêu chí đóng: thực hiện exact comparison từ artifact, fail closed trước dense
inference, và thêm deterministic tests cho source/count/condition/maxima
mismatch bằng pure values hoặc helper trực tiếp, không thay dependency thật bằng
mock/fake/stub.

### R2 — Major — Failure attribution của snapshot/model không trung thực

Vị trí: `backend/evaluation/full_corpus_embedding_preflight.py:288-315` kết hợp
với `derive_status()` tại `:218-236`.

Requirement: snapshot/Qwen/model failure phải được ghi đúng observed component
và JSON phải phản ánh đúng mọi outcome.

Evidence: mọi snapshot/tokenizer resolution failure đều đặt
`cpu_models="FAILED"`; sau đó `derive_status()` chạy khi chưa có `phase_2`, nên
trả `BLOCKED_PHASE_2`, kể cả snapshot Qwen bị thiếu hoặc CPU model resolve lỗi.

Tác động: blocked artifact gán sai nguyên nhân, làm người vận hành sửa nhầm
Phase 2 và khiến evidence failure path không đáng tin.

Tiêu chí đóng: phân loại chính xác Qwen so với CPU model/snapshot resolution,
không để missing status che nguyên nhân thật, luôn ghi sanitized evidence với
exit non-zero; kiểm pure status/control flow không dùng fake dependency.

### R3 — Major — Test dùng fake dependency trái hard boundary

Vị trí: `backend/tests/test_full_corpus_embedding.py:121-135`.

Requirement: Session Prompt và post-approval consistency correction của plan
cấm mock/fake/stub dependency trong implementation/test. Exact Reviewer suite
được dự kiến có 29 tests.

Evidence: `test_count_tokens_calls_tokenizer_with_exact_flags` tạo class
`FakeTokenizer`. Fresh exact Reviewer rerun vì vậy thu 30 tests thay vì 29.

Tác động: test bảo vệ implementation detail bằng một dependency giả và vi phạm
boundary đã duyệt, dù production tokenizer scan hiện có evidence thật.

Tiêu chí đóng: xóa test fake này; giữ verification flags bằng source inspection
và full real tokenizer/preflight evidence đã yêu cầu. Không thay bằng mock/fake/
stub khác.

### R4 — Major — Evidence package chưa đủ các trường bắt buộc để tự audit

Vị trí:

- `reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json`;
- `reports/full_corpus_phase_3_embedding_sparse_implementation_2026_09_12.md`;
- `backend/evaluation/full_corpus_embedding_preflight.py:286-304`, `:388-403`
  và `:500-547`.

Requirement: Review Contract yêu cầu observed Qwen parameter device/dtype,
batch/eager/native dimension và role preprocessing proof; sparse two-generation
byte comparison plus round-trip equality; exact before/after worktree và hashes
cho mọi immutable path group.

Evidence: JSON lưu configured spec fields và VRAM/smoke result nhưng không phân
biệt chúng với observed parameter device/dtype/attention state; sparse section
chỉ lưu hash/count, không lưu kết quả repeated-byte và round-trip checks. Report
không có exact base/head/worktree before/after inventory và chỉ đưa một current
hash cho sáu path, không có before/after manifest cho 205 curated inputs,
Foods Golden và existing evaluation artifacts. Reviewer đã tự xác nhận các
tracked immutable paths không có diff, nhưng điều đó không thay required
Implementer evidence package.

Tác động: Reviewer bị buộc suy diễn live claims từ config/source hoặc tự bù
traceability mà contract giao cho Implementer; high-risk model/artifact evidence
chưa tự phân biệt configured với observed.

Tiêu chí đóng: evidence ghi sanitized observed runtime fields cho Qwen và các
boolean/result của sparse repeated generation + round-trip; report bổ sung exact
before/after base/head/worktree separation và immutable group manifests. Không
thêm framework/validator mới; dùng trực tiếp runner/state và Git/hash evidence
đã có.

### R5 — Minor — Handoff/test count và Notebook lifecycle wording chưa chính xác

Vị trí: `session_prompt/CURRENT_HANDOFF.md`, implementation report mục 2/3.5,
và `notebooks/03_embedding_models.ipynb` cell cuối.

Evidence: handoff nói exact Reviewer suite có 29 tests trong khi fresh run có
30 do R3; report ghi sparse 7 tests và BM25 5 tests trong khi source hiện có 8
và 4, dù tổng suite 34 là đúng. Notebook nói Phase 3 đã hoàn tất và Phase 4 sẽ
được thực hiện trước khi Reviewer/User closure.

Tác động: không làm sai runtime nhưng làm evidence/lifecycle khó kiểm.

Tiêu chí đóng: đồng bộ exact counts sau khi bỏ fake test; Notebook chỉ nói
preflight đã quan sát PASS, closure đang chờ Reviewer/User và Phase 4 vẫn đóng.

Không phát hiện fallback, quantization, FlashAttention, `device_map=auto`, dense
full-corpus encoding, Qdrant access/mutation hoặc thay đổi immutable Foods paths
trong implementation Phase 3.

## 3. Cách Reviewer chạy lại thật

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py \
  -q --tb=short

git diff --check

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py \
  backend/tests/test_bm25.py -q --tb=short

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-review-uv-cache \
uv run python -c 'from pathlib import Path; from backend.embedding.sparse import load_sparse_state, serialize_sparse_state; p=Path("data/full_corpus_builds/phase_3_sparse_state.json"); s=load_sparse_state(p); assert serialize_sparse_state(s)==p.read_bytes(); print(s.document_count, len(s.vocabulary), s.corpus_identity)'
```

Reviewer còn kiểm JSON bằng `jq`, SHA-256 của sparse/immutable paths, notebook
cells và prohibited-pattern search trong code/evidence.

## 4. Kết quả quan sát

- Exact Reviewer suite: `30 passed, 2 warnings`, exit `0`.
- Focused suite cộng BM25: `34 passed, 2 warnings`, exit `0`.
- `git diff --check`: exit `0`, không có output.
- Sparse round-trip độc lập: PASS; `document_count=8460`, vocabulary `5662`,
  corpus identity `0e5c059516cd942b151286cf597f785c65e642cacd1b0421124fe50fe574f223`.
- Sparse SHA-256 độc lập khớp artifact:
  `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`.
- Evidence JSON: status `PASS`, 205 files, 8.460 chunks, sample 12, đủ model
  summaries, GTX 1650/CUDA available và Qwen peak allocation `1323201536`
  bytes; prohibited content search sạch.
- Notebook canonical: code cell outputs rỗng và execution counts null; gọi
  backend Phase 3 thay vì duplicate dense pipeline.
- `git diff --name-only` trên settings, Foods embedder/dense benchmark, BM25,
  Phase 2 chunker/preview, curated corpus, Golden/evaluation, `pyproject.toml`
  và `uv.lock`: không có output.

Hai warning fresh là Qdrant compatibility warning từ test bootstrap và NVML
initialization warning; không làm thay đổi verdict. Full backend suite, model
inference, tokenizer scan và Notebook Run All của Implementer không được
Reviewer lặp lại theo contract.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không lặp heavy model download/inference, full tokenizer scan hoặc
Notebook Run All theo chỉ đạo User trong Review Contract. Các kết quả đó được
đọc từ artifact/report và audit bằng source; vì R1/R4, package hiện chưa đủ để
chấp nhận toàn bộ live claims làm closure evidence.

Reviewer không thể tái dựng chắc chắn worktree-before từ report hiện tại vì
Implementer chưa ghi exact before inventory/manifest. Current worktree và
tracked diff đã được kiểm đầy đủ theo khả năng hiện có.

## 6. Decision và bước tiếp theo

Technical verdict: `FAIL` — `changes_requested` do còn bốn Major R1–R4.

Implementer xử lý một correction batch theo
`session_prompt/CURRENT_HANDOFF.md`. Giữ nguyên model/revision/device/dtype,
corpus, Qdrant/Git/safety boundaries. Sau correction, chạy lại focused tests,
offline bounded preflight để sinh evidence đã sửa, notebook temporary Run All
nếu notebook thay đổi, artifact/hash checks và cập nhật report/handoff. Phase 4
vẫn đóng; chưa có Approval Closure Contract.
