# Codex Review: Phase 3 Embedding/Sparse Correction 2

Decision: ready_for_user_confirmation
Reviewer: Codex
Date: 2026-09-12 +07
Canonical guide: `guides/phase_3_embedding_sparse_representation.md`
Implementation report: `reports/full_corpus_phase_3_embedding_sparse_implementation_2026_09_12.md`

## 1. Phạm vi đã review

Reviewer đọc full Correction 2 report/handoff, đối chiếu exact worktree với danh
sách 40 paths, kiểm 205 discovered Phase 2 sources so với broader whole-tree
proof, kiểm current JSON/sparse/notebook và chạy lại GPU/CUDA cùng exact offline
bounded preflight. R1–R3/R5 đã đóng ở Correction 1 và không bị mở lại.

## 2. Findings

Không còn blocker hoặc major.

- R4 đã đóng: current inventory có đúng 19 tracked modified và 21 untracked
  paths, phân tách Phase 3, Reviewer-owned/pre-existing và review artifacts.
- 205 được mô tả đúng là discovered Phase 2 source list; `knowledge-base-hue`
  whole-tree/no-diff proof là ranh giới bất biến rộng hơn.
- Current artifact phân biệt configured/observed runtime state, ghi Qwen
  CUDA/FP16/eager/native 1024D, sparse repeated-byte và round-trip.
- Không phát hiện thay đổi immutable runtime/corpus/Golden/evaluation,
  dependency, Qdrant, dense full-corpus hoặc Phase 4 scope.

## 3. Cách Reviewer chạy lại thật

```bash
/usr/lib/wsl/lib/nvidia-smi

UV_CACHE_DIR=/tmp/hue-rag-phase3-review-correction2-uv-cache uv run python -c \
'import json, torch; print(json.dumps({"torch":torch.__version__,"torch_cuda":torch.version.cuda,"available":torch.cuda.is_available(),"count":torch.cuda.device_count(),"name":torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}))'

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-review-correction2-uv-cache \
uv run python -m backend.evaluation.full_corpus_embedding_preflight \
  --sparse-output data/full_corpus_builds/phase_3_sparse_state.json \
  --evidence-output reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json

git diff --check
```

GPU commands và preflight được chạy ngoài sandbox vì sandbox không cấp GPU
device access. Reviewer còn kiểm `git status --short`, base diff, SHA-256,
artifact bằng `jq`, prohibited-pattern search và notebook cleanliness.

## 4. Kết quả quan sát

- NVIDIA-SMI: GTX 1650, 4096 MiB, exit 0.
- Torch: `2.13.0+cu130`, CUDA `13.0`, available true, count 1.
- Fresh offline preflight: exit 0, status `PASS`, 205 files, 8.460 chunks,
  condition rules 3, sample 12, errors empty.
- Qwen: exact revision, observed `cuda:0`, `torch.float16`, eager, native 1024D,
  batch 1; peak allocation `1323201536` bytes.
- Tokenizer scan: zero over-limit; maxima `366`, `366`, `255`, `560`.
- Sparse SHA-256:
  `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`;
  repeated-byte và round-trip đều true.
- Artifact redaction sạch; notebook canonical có output rỗng/execution count
  null; `git diff --check` sạch.
- Worktree inventory fresh: 40 paths = 19 tracked modified + 21 untracked,
  khớp report/handoff.
- Core `31 passed` và extended `35 passed` được reuse từ Correction 1 vì
  Correction 2 không sửa code/tests; Reviewer đã quan sát trực tiếp các kết quả
  đó trong cùng review series.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer không chạy lại full backend suite: Review Contract không yêu cầu và
Implementer đã ghi các Foods/Qdrant failures ngoài Phase 3 khi Qdrant không bật.
Notebook Run All được reuse từ Correction 1 vì Notebook không đổi. Không có
giới hạn nào còn làm giảm độ tin cậy của acceptance Phase 3.

## 6. Decision và bước tiếp theo

Technical verdict: `PASS` — `ready_for_user_confirmation`.

### Approval Closure Contract

User confirmation chính xác: `Tôi xác nhận Phase 3.`

Sau xác nhận, Reviewer được cập nhật cơ học:

- `guides/phase_3_embedding_sparse_representation.md`: Full-corpus Phase 3
  thành `approved/completed`, dẫn final review và user report;
- `session_prompt/Project_Status.md`: snapshot/phase table ghi Phase 3 đã User
  closure, Phase 4 design là next gate;
- `session_prompt/CURRENT_HANDOFF.md`: đóng closure và chuyển thành một
  `reviewer/next_design` cho Phase 4, không cấp implementation authority.

Checks sau cập nhật: consistency/links, complete worktree và `git diff --check`.
Git authorization vẫn `none`; không commit/push. Phase 4 implementation, Qdrant,
dense full-corpus và mọi mutation vẫn cần design package cùng User approval
riêng.
