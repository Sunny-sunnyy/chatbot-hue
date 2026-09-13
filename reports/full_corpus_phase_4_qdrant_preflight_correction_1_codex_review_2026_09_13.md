# Codex Review: Phase 4 Full-corpus Preflight Correction 1

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-09-13 +07
Canonical guide: `guides/phase_4_qdrant_ingestion.md`
Implementation report: correction evidence supplied by User on 2026-09-13 +07

## 1. Phạm vi đã review

Reviewer đã đọc exact correction tại `backend/tests/conftest.py`,
`backend/vectorstore/qdrant.py`, `backend/ingestion/source_state.py`, focused
test delta và regenerated preflight artifact. Base
`071b1137bd5d1af60053bd3bb2c3fe47ba29ac0f` là ancestor của current HEAD
`511e8a3eac783b324470f2da3ce5d5fddd786ab8`; unrelated
`PROJECT_DOCUMENT_REGISTRY.md` được giữ ngoài Phase 4 scope.

## 2. Findings

R1–R4 của review trước đã đóng:

- R1: focused suite không còn resolve real Qdrant fixtures; cleanup chỉ đi qua
  `real_client` khi live tests yêu cầu.
- R2: dense/sparse non-default vector params bị reject fail-closed.
- R3: final record publish dùng adjacent temp + atomic no-overwrite `os.link`.
- R4: evidence đã tách registry audit khỏi Phase 4 deliverables và ghi đúng
  base/current HEAD.

Minor không chặn: `backend/tests/conftest.py:173-176` còn fixture
`_live_cleanup_sweep` không có consumer và lặp cleanup đã chuyển vào
`real_client`. Không tạo correction riêng; có thể xóa trong một edit được cấp
quyền sau này nếu file này tiếp tục được sửa.

Không còn blocker hoặc major trong checkpoint Tasks 1–6.

## 3. Cách Reviewer chạy lại thật

```bash
QDRANT_URL=http://127.0.0.1:9999 HF_HUB_OFFLINE=1 \
UV_CACHE_DIR=/tmp/hue-rag-phase4-correction1-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-correction1-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py --fixtures-per-test -q

git diff --check

docker compose ps
docker compose config --images
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase4-review-preflight-uv-cache \
uv run --env-file .env python -m backend.ingestion.full_corpus_pipeline preflight
```

Reviewer còn chạy pure qdrant model probes cho dense/sparse on-disk rejection
và real-filesystem concurrent publish với 16 writers.

## 4. Kết quả quan sát

- Focused suite với unreachable Qdrant URL: `41 passed`, zero warnings, exit 0.
- Fixture inventory: chỉ các tests dùng filesystem nhận `tmp_path`/
  `tmp_path_factory`; không có `real_client` hoặc cleanup fixture.
- Dense `on_disk=True` và sparse index `on_disk=True`: đều bị reject đúng.
- Concurrent record publish: đúng một writer thành công, 15 writers nhận
  `FileExistsError`, không còn temp file.
- `git diff --check`: sạch.
- Qdrant chạy đúng server 1.18.3 và pinned image digest; client 1.19.0.
- Fresh preflight: `READY`, 205 files, 8.460 chunks, exact corpus/sparse
  identities; bốn targets đều absent, record absent, blockers rỗng.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không load dense model, encode full corpus, create/upsert hoặc chạy
Task 8. Không inspect/query Foods collections; tuyên bố của Implementer rằng hai
Foods collections nguyên vẹn không được dùng làm fresh Reviewer evidence.
Preflight tiếp tục in tokenizer length warnings đã biết trong bước fresh
chunking; closed Phase 3 tokenizer evidence và exact corpus identity vẫn khớp.

## 6. Decision và bước tiếp theo

Technical verdict cho Tasks 1–6: `PASS WITH LIMITATIONS` —
`ready_for_user_confirmation` tại live-write gate.

Task 7 vẫn đóng cho tới khi User phê duyệt bằng văn bản đủ bốn exact targets.
Approval chỉ mở sequential create/upsert và completion/build-record work của
Task 7, sau đó Task 8 read-only inspection/report. Nó không mở deletion,
recovery, Foods access, replacement, cleanup, cutover, Phase 5, dependency/
settings changes, paid API hoặc Git operations.
