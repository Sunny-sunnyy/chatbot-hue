# Codex Review: Full-corpus Phase 4 Qdrant Ingestion Final

Decision: ready_for_user_confirmation (`PASS WITH LIMITATIONS`)
Reviewer: Codex
Date: 2026-09-13 +07
Canonical guide: `guides/phase_4_qdrant_ingestion.md`
Implementation report: `reports/full_corpus_phase_4_qdrant_ingestion_implementation_2026_09_12.md`

## 1. Phạm vi đã review

Reviewer đã đọc full Written Spec, Implementation Plan/Review Contract, hai
implementation reports và exact current handoff; targeted-read guide Phase 4,
bốn prior reviewer records, Phase 3 identities/sample artifact và initial Phase
4 preflight artifact.

Reviewer đã xác nhận base
`071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f` là ancestor của current HEAD
`511e8a3eac783b324470f2da3ce5d5fddd786ab8`; inspect complete tracked/untracked
inventory, exact implementation diff, source/tests, four ignored final records,
Notebook 04 và reviewer-owned status/handoff changes. Untracked
`PROJECT_DOCUMENT_REGISTRY.md` là Reviewer-owned audit track có trước, không
phải Phase 4 implementation deliverable. Remote-GPU context là Reviewer-owned
deferred workstream, không được dùng làm Phase 4 evidence.

Independent dynamic review gồm focused offline suite, immutable-path audit,
record/schema/hash cross-check, temporary Notebook 04 Run All và post-build
preflight trên đúng bốn full-corpus targets. Không access Foods collections,
không load dense model, không encode lại corpus và không mutate Qdrant.

## 2. Findings

Không còn blocker hoặc major.

### F1 — Minor — Fixture cleanup dư sau Correction 1

Vị trí: `backend/tests/conftest.py`, fixture `_live_cleanup_sweep`.

Requirement: code/test phải trực tiếp và không giữ mechanism không còn consumer.
Correction 1 đã chuyển cleanup thật vào lifecycle của `real_client`; fixture
không-autouse này không có consumer và lặp cùng sweep.

Tác động: không được resolve bởi focused suite, không truy cập Qdrant và không
ảnh hưởng Phase 4 acceptance; chỉ là code test dư. Không tạo correction riêng.
Có thể xóa khi file tiếp tục được sửa trong một scope được cấp quyền.

### F2 — Minor — Qwen execution report ghi sai payload fields và trộn estimate deferred

Vị trí:
`reports/qwen3_gtx1650_embedding_execution_report_2026_09_13.md`, mục 4.2 và
mục 5–6.

Requirement: payload Phase 4 có đúng
`search_text`, `source`, `title`, `heading_path`, `evidence_parts`; estimate
remote-GPU không được trình bày như observed Phase 4 result.

Evidence: report phụ ghi `source_path`, `section_title`, `chunk_index` thay cho
`source`, `title`, `heading_path`, đồng thời nêu Colab `35–45 giây`/batch
`32–64` chưa có benchmark. Exact source, implementation report chính và fresh
live verification đều cho thấy dữ liệu thật dùng đúng năm fields canonical.
Deferred context cũng ghi rõ chưa có evidence để khóa remote batch/throughput.

Tác động: không ảnh hưởng collection hoặc acceptance đã xác minh, nhưng report
phụ không đáng dùng làm nguồn chuẩn cho payload hay remote throughput. Không tạo
correction riêng; downstream phải dùng final review, implementation report
chính và exact live evidence. Có thể sửa hoặc retire report phụ trong document
audit được User duyệt sau này.

## 3. Cách Reviewer chạy lại thật

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-final-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py \
  -q --tb=short

git diff --check

docker compose ps
curl --fail --silent --show-error http://localhost:6333/

UV_CACHE_DIR=/tmp/hue-rag-phase4-final-review-uv-cache \
uv run --env-file .env jupyter nbconvert --execute --to notebook \
  notebooks/04_qdrant_ingestion.ipynb \
  --output /tmp/04_qdrant_ingestion-phase4-final-review.ipynb \
  --ExecutePreprocessor.timeout=1800

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-final-review-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline preflight
```

Reviewer còn dùng `sha256sum` và `jq` trên đúng bốn final records; static-check
canonical notebook outputs/execution counts/forbidden symbols; kiểm selected
immutable paths không có worktree diff. Existing Compose container được start
lại sau khi User bật Docker engine; không tạo instance hoặc storage mới.

## 4. Kết quả quan sát

- Focused suite: `41 passed in 9.53s`, exit `0`; không resolve live fixture,
  model hoặc Qdrant path.
- `git diff --check`: exit `0`, không output.
- Selected immutable tracked paths, corpus, Phase 3 artifact và sparse state:
  không có worktree diff. Sparse SHA-256 khớp
  `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`.
- Qdrant Compose: exact pinned digest, server `1.18.3`, client `1.19.0`.
- Bốn final records: schema/status/representation đúng; cùng exact corpus
  identity, 205-entry source mapping, `8.460` chunks, sparse identity/vocabulary
  và point count; model/revision/dimension đúng registry. Record SHA-256 lần
  lượt là `ea19021a...`, `0cd69406...`, `10b3f847...`, `2faa9d4f...`, khớp
  implementation report.
- Temporary Notebook 04 Run All: exit `0`. Trên từng target, exact schema PASS,
  point count `8460`, full expected ID/payload comparison `8460`, deterministic
  sampled dense+sparse vector readback `12`; payload projection có đúng
  `evidence_parts`, `heading_path`, `search_text`, `source`, `title`.
- Post-build preflight: expected exit `2`, status `BLOCKED`; cả bốn targets đều
  `non_empty: 8460`, final record present và cùng fresh corpus/source/sparse
  identities. Đây là positive guard evidence, không phải Phase failure.
- Canonical Notebook 04 vẫn clean: code-cell outputs rỗng, execution counts
  `null`, không có forbidden mutation/model symbols.
- Authority trail có exact initial four-target live-write approval và exact
  guarded recovery approval cho Candidate 1; incident giữ target/record đúng
  fail-closed, Correction 2 sửa focused root cause rồi clean rebuild đủ bốn.

Evidence được reuse: full dense inference/runtime summaries của bốn candidates,
Qwen full-matrix norm range, elapsed và peak VRAM đến từ cùng implementation
series. Reviewer không gọi đó là fresh execution vì exact source/corpus/sparse/
model contracts không đổi và Review Contract không yêu cầu lặp bốn expensive
encodes. Fresh Qdrant readback xác minh stored sample norms/structure, không tái
tạo full pre-upsert matrix statistics.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không rerun bốn dense encodes; do đó Qwen elapsed khoảng 65 phút,
  peak VRAM `1.323.238.400` bytes và full-matrix min/max norm không được đo lại.
- Tokenizer length warnings xuất hiện khi fresh preparation nhưng exact corpus
  identity và closed Phase 3 tokenizer evidence vẫn khớp; không có model
  inference trong review này.
- Foods collections không được access theo hard boundary; Implementer claim về
  Foods không được coi là fresh Reviewer evidence. Tracked Foods config/runtime
  paths không có diff.
- Remote Colab/Lightning/Vast/RTX throughput, compatibility và batch size chưa
  được kiểm chứng và hoàn toàn ngoài verdict này.

## 6. Decision và bước tiếp theo

Technical verdict: `PASS WITH LIMITATIONS` — `ready_for_user_confirmation`.
Tasks 1–8 đáp ứng Phase 4 contract; hai minor trên không ảnh hưởng index/data
safety hoặc required behavior và không tạo correction riêng. Phase 4 chưa closed
cho tới khi User xác nhận.

### Approval Closure Contract

User xác nhận bằng câu:

```text
Tôi xác nhận closure Full-corpus Phase 4 với verdict PASS WITH LIMITATIONS.
```

Sau xác nhận, Reviewer được phép cập nhật cơ học duy nhất:

- đánh dấu Phase 4 User-closed trong `session_prompt/Project_Status.md`;
- chuyển `session_prompt/CURRENT_HANDOFF.md` sang state `completed`, Git
  authorization `none` và chờ nhiệm vụ mới;
- giữ final review này làm canonical Phase 4 closure evidence.

Không có Git authorization, không commit/push. Phase 5, remote-GPU research và
mọi implementation/live/cloud action vẫn đóng; chúng cần design/handoff và
authority riêng theo yêu cầu tiếp theo của User.

## 7. Post-closure addendum — 2026-09-13 +07

User đã xác nhận closure bằng exact câu trong Approval Closure Contract. Sau đó
User yêu cầu audit sâu riêng collection Qwen vì lần encode local mất khoảng
65–70 phút. Fresh read-only full scan và 12-sample exact-model re-encode đều
PASS; không phát hiện lỗi collection, payload, dense/sparse vectors hoặc Qdrant
runtime. Evidence đầy đủ:

```text
reports/full_corpus_phase_4_qwen_post_closure_audit_2026_09_13.md
```

F2 đã được sửa ở documentation layer: auxiliary Qwen report hiện dùng đúng năm
payload fields canonical và không còn trình bày batch/throughput remote chưa đo
như observed fact. F1 vẫn là minor không chặn và không được sửa bởi Reviewer.
Addendum không thay verdict/closure Phase 4 và không kích hoạt Phase 5 hay
remote-GPU workstream.
