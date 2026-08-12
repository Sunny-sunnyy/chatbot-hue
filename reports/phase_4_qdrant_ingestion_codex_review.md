# Codex Review: Phase 4 Qdrant Ingestion

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-08-12
Review path:

```text
reports/phase_4_qdrant_ingestion_codex_review.md
```

Implementer report:

```text
reports/phase_4_qdrant_ingestion_implementation_report.md
```

Phase guide context:

```text
guides/phase_0_mvp_foundation.md
guides/phase_4_qdrant_ingestion.md
session_prompt/Project_Status.md
reports/hue_foods_rag_benchmark.md
```

## Tóm Tắt

Phase 4 đạt technical review sau hai correction rounds và hai live approval
gates. Implementation tạo Qdrant local pinned, deterministic dense+sparse
points, bounded/idempotent upsert, schema/count postconditions và reset command
fail-closed. Live ingestion tạo collection green với 572/572 points hợp lệ.

Không có retrieval, native sparse query, answer generation hoặc benchmark
winner claim. Phase 5 vẫn đóng cho đến khi người dùng kiểm tra notebook và xác
nhận Phase 4.

## Findings

Không có blocker hoặc major findings.

Accepted limitations:

- Live rerun không chạy; idempotency được chứng minh bằng UUID5 deterministic
  và mocked partial-failure/rerun test.
- Live reset không chạy; destructive guards chỉ mock-tested và mọi lần xóa thật
  vẫn cần user approval riêng.

## Verification

Reviewer đã chạy độc lập:

```bash
cd backend
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile vectorstore/qdrant.py vectorstore/hybrid_index.py vectorstore/upsert.py vectorstore/reset.py ingestion/pipeline.py
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/test_qdrant_schema.py tests/test_hybrid_index.py tests/test_ingestion_pipeline.py -q --tb=short
# 44 passed
UV_CACHE_DIR=/tmp/uv-cache uv run python -m pytest tests/ -q --tb=short
# 118 passed

cd ..
docker compose config
HUE_RAG_QDRANT_REAL=1 UV_CACHE_DIR=/tmp/uv-cache uv run jupyter nbconvert --to notebook --execute --output /tmp/hue_phase4_real_review.ipynb notebooks/04_qdrant_ingestion.ipynb
git diff --check
codegraph status .
```

Live evidence do Reviewer thu thập sau approval riêng:

```text
Qdrant: 1.18.3, exact pinned digest, REST 200
collection: hue_foods_e5_small_384
status: green
dense: 384 Cosine
sparse index: enabled
exact points: 572
expected/actual UUID5 sets: equal (572/572)
payload identity: valid trên toàn bộ 572 points
```

Gate 2 ép `HF_HUB_OFFLINE=1` và `TRANSFORMERS_OFFLINE=1`; E5 load từ cache,
không download hoặc gọi paid API.

## Scope Check

Implementation nằm trong allowlist Phase 4, gồm scope expansion được user phê
duyệt cho `pyproject.toml` và `uv.lock` để gỡ package PyPI `vectorstore==0.0.0`
đã shadow local package. Các deletion dưới `knowledge-base/`, notebook Phase
1–2 và `skills/` là thay đổi có sẵn, không thuộc Phase 4 và không bị chạm.

Reviewer chỉ sửa guide lifecycle, benchmark ledger, Codex review và user report
theo reviewer scope. `Project_Status.md` chưa được cập nhật.

## Safety And Quality Check

- Security: không đọc/log secret, key hoặc header; không gọi OpenAI/OpenRouter/web.
- Data safety: chỉ 572 curated foods chunks được index; payload không có absolute private path.
- Reliability: validation hoàn tất trước mutation; schema, existing IDs/payload và final count fail closed; reset tách riêng.
- Performance: E5 cache một lần/process, batch 64, một transient retry, không concurrency framework thừa.
- Tests: 44 Phase 4 và 118 full-suite tests đạt; mocked suite không chạm Qdrant.
- Notebooks: JSON hợp lệ, 15 cells, outputs rỗng, execution counts null; default non-live và real mode read-only đạt.
- Evaluation: chưa có retrieval/answer metrics; ledger chỉ ghi ingestion evidence.

## Required Changes

Not applicable.

## User Confirmation Readiness

- Technically accepted: Docker/config, Phase 4 vectorstore/ingestion modules,
  tests, dependency cleanup, notebook và implementation report.
- Accepted limitations: không live rerun và không live reset; không có retrieval
  quality/native sparse evidence.
- Canonical notebook: `notebooks/04_qdrant_ingestion.ipynb`; committed file sạch,
  default mode safe, real mode chỉ đọc collection.
- User checks: chạy notebook từ trên xuống; xác nhận 572 chunks, UUID5 ổn định,
  sample point dense+sparse đúng. Tùy chọn real mode để thấy collection, dense
  384 cosine, sparse index và 572 points.
- User report: `reports/user_reports/phase_4_qdrant_ingestion_user_report.md`.
- Phase 5 vẫn đóng; `Project_Status.md` chưa được đánh dấu Phase 4 approved.
