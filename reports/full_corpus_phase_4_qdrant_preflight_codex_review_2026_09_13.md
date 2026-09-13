# Codex Review: Phase 4 Full-corpus Qdrant Preflight

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-13 +07
Canonical guide: `guides/phase_4_qdrant_ingestion.md`
Implementation report: checkpoint report supplied by User on 2026-09-13 +07

## 1. Phạm vi đã review

Reviewer đã đọc full Written Spec, Implementation Plan/Review Contract, guide
Phase 4, toàn bộ 8 tracked worktree diffs, 3 untracked Phase 4 deliverables và
untracked `PROJECT_DOCUMENT_REGISTRY.md`; đối chiếu current HEAD
`511e8a3eac783b324470f2da3ce5d5fddd786ab8` với declared base
`071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f` và xác nhận base là ancestor.

Reviewer đã kiểm NumPy/list API, sparse lookup, point/payload construction,
Qdrant schema/fresh-target guards, completion verification, final-record write,
registry/build orchestration, focused tests, immutable paths và preflight JSON.
Không load dense model, encode full corpus hoặc mutate/query/scroll/retrieve bất
kỳ collection nào.

## 2. Findings

### R1 — Blocker — Focused suite không phải pure/offline và có mutation path ngoài quyền

Vị trí: `backend/tests/conftest.py:93-98`, `:171-174`; ba focused test files.

Requirement: Review Contract yêu cầu exact focused suite chạy không model,
network/Qdrant connection hoặc mutation; current handoff chỉ cho preflight gọi
`info`, `collection_exists`, `get_collection`, `count` trên bốn exact targets.

Evidence: session-scoped autouse fixture `_live_cleanup_sweep(real_client)` luôn
khởi tạo real Qdrant client cho cả ba pure test files. Teardown gọi
`get_collections()` và có thể gọi `delete_collection()` cho names mang test
prefix. Fresh Reviewer run đạt `41 passed` nhưng phát cảnh báo
`Failed to obtain server version`, chứng minh client/network path đã được kích
hoạt. Vì vậy kết quả assertion PASS không chứng minh hard boundary được giữ.

Tác động: lệnh được mô tả là deterministic/pure có thể truy cập rộng hơn bốn
targets và thực hiện deletion không được cấp quyền. Task 7 không thể mở từ
evidence này.

Tiêu chí đóng: refactor fixture nhỏ nhất để real cleanup chỉ được request khi
test thật sự dùng `real_client`/live fixture, không autouse trong focused suite;
giữ cleanup cho live tests. Chạy exact focused command và chứng minh fixture
plan không chứa `real_client`/`_live_cleanup_sweep`; không mock/fake/stub Qdrant.

### R2 — Major — Existing-empty schema guard chấp nhận tuning bị cấm

Vị trí: `backend/vectorstore/qdrant.py:88-103`.

Requirement: existing-empty target chỉ hợp lệ khi exact schema khớp; Phase 4
cấm explicit on-disk placement, custom dense/sparse index configuration,
quantization và các tuning ngoài Qdrant defaults.

Evidence: validator chỉ kiểm vector names, dimension, distance và sparse
modifier. Hai fresh pure probes tạo schema dense `on_disk=True` và sparse index
`on_disk=True`; cả hai đều được validator chấp nhận (`ACCEPTED`).

Tác động: preflight/build có thể coi foreign empty collection là hợp lệ rồi ghi
8.460 points vào schema không đúng contract.

Tiêu chí đóng: đối chiếu các dense/sparse params có liên quan với exact objects
từ `expected_full_corpus_schema()` và reject mọi non-default tuning bị Spec cấm;
thêm focused pure cases ít nhất cho dense on-disk/quantization hoặc HNSW và
sparse index config.

### R3 — Major — Final build-record write không thực sự exclusive

Vị trí: `backend/ingestion/source_state.py:192-208`, đặc biệt `Path.replace()` ở
dòng 204; test tại `backend/tests/test_full_corpus_qdrant_ingestion.py:68-76`.

Requirement: final-only build record phải được ghi atomically và exclusively;
record xuất hiện đồng thời từ tiến trình khác phải không bị overwrite.

Evidence: hai lần `path.exists()` đều xảy ra trước `temporary.replace(path)`.
`Path.replace()` cho phép thay thế target đã xuất hiện trong khoảng race giữa
lần kiểm cuối và replace. Test hiện tại chỉ kiểm lần gọi tuần tự sau khi target
đã tồn tại, không chứng minh no-overwrite atomicity.

Tác động: một record vừa được tiến trình khác publish có thể bị ghi đè, làm mất
fail-closed ownership evidence ngay trước live build records.

Tiêu chí đóng: dùng primitive cùng filesystem vừa atomic publish vừa fail nếu
target đã tồn tại; giữ cleanup temp và bytes deterministic. Test bằng filesystem
thật rằng target có sẵn không đổi và primitive không có overwrite window; không
thêm lock/resume framework.

### R4 — Minor — Báo cáo inventory không chính xác

Vị trí: checkpoint report mục 3.

Evidence: report nói mọi changed/untracked file đều thuộc Allowed paths nhưng
`PROJECT_DOCUMENT_REGISTRY.md` không nằm trong allowlist và là document-audit
track riêng. Report cũng không ghi exact HEAD hoặc before-worktree inventory.

Tác động: không chứng minh Implementer sửa registry, nhưng làm scope/evidence
index không chính xác.

Tiêu chí đóng: correction report tách registry thành unrelated pre-existing
change được bảo toàn, ghi exact base/current HEAD và before/after inventory có
thể chứng minh; không sửa hoặc xóa registry.

Không phát hiện Task 7/8 execution, dense full-corpus inference, Qdrant write,
Foods access, dependency/settings/corpus mutation, retry/fallback hoặc Git write
trong Phase 4 implementation delta.

## 3. Cách Reviewer chạy lại thật

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py \
  -q --tb=short

git diff --check

docker compose ps
docker compose config --images
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-review-preflight-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline preflight
```

Reviewer còn chạy pure schema probes với qdrant-client value models cho dense
on-disk và sparse-index on-disk; không tạo Qdrant client/collection trong probe.

## 4. Kết quả quan sát

- Focused suite: `41 passed, 1 warning`, exit `0`; warning Qdrant compatibility
  chứng minh R1, nên không được coi là pure/offline evidence.
- `git diff --check` trên current worktree: exit `0`, không output.
- Immutable tracked paths được chọn theo Review Contract: không có worktree diff.
- Sparse state SHA-256 khớp exact closed value
  `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`.
- Docker Compose chạy Qdrant đúng pinned digest
  `sha256:0bd98fa7977f1e75694779359ca4e212822e5a71334e28421182f72f209d5286`.
- Fresh read-only preflight: `READY`; Qdrant server `1.18.3`, client `1.19.0`,
  205 files, 8.460 chunks, exact corpus/sparse identities; cả bốn targets
  `absent`, record absent, blockers rỗng.
- Preflight phát tokenizer length warnings nhưng fresh identity và Phase 3
  closed tokenizer evidence vẫn khớp; warnings không đổi finding/gate hiện tại.
- Pure forbidden-schema probes: `dense on_disk=True` và
  `sparse index on_disk=True` đều bị implementation hiện tại chấp nhận.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không chạy dense model, full-corpus encode, create/upsert hoặc Task 8.
Không list/query/scroll/retrieve Foods hay candidate collections. Không thể tái
dựng before-worktree inventory từ checkpoint report; current diff vẫn được cô
lập đầy đủ khỏi HEAD hiện hành.

## 6. Decision và bước tiếp theo

Technical verdict: `FAIL` — `changes_requested` do R1 blocker và R2–R3 major.

Preflight `READY` được xác minh, nhưng **Task 7 chưa được phép mở**. Implementer
xử lý một correction batch theo `session_prompt/CURRENT_HANDOFF.md`, chỉ chạy
pure checks và exact four-target read-only preflight. Sau independent re-review
đạt, Reviewer mới trình User exact live-write approval cho đủ bốn targets.
