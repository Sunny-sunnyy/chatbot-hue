# Codex Review: Phase 3 Embedding/Sparse Correction 1

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-12 +07
Canonical guide: `guides/phase_3_embedding_sparse_representation.md`
Implementation report: `reports/full_corpus_phase_3_embedding_sparse_implementation_2026_09_12.md`
Prior review: `reports/full_corpus_phase_3_embedding_sparse_codex_review_2026_09_12.md`

## 1. Phạm vi đã review

Reviewer đọc full correction report/handoff và kiểm exact delta R1–R5 trong
dense runner, preflight, tests, JSON evidence và Notebook 03. Reviewer đối chiếu
worktree/base, immutable Git paths, sparse artifact, prohibited patterns và chạy
core/extended suites cùng offline bounded preflight được correction yêu cầu.

## 2. Findings

### R1 — Closed

`validate_phase_2_identity()` nay đối chiếu status, exact ordered source list,
file/chunk/condition counts; `validate_phase_2_tokenizer_maxima()` đối chiếu ba
fresh maxima với preserved artifact. Các mismatch trả `BLOCKED_PHASE_2` trước
dense inference. Pure-value tests phủ các nhánh mismatch.

### R2 — Closed

Snapshot resolution phân biệt Qwen `BLOCKED_QWEN` và CPU `FAILED_MODEL`;
`derive_status()` không còn biến missing `phase_2` thành Phase 2 failure.

### R3 — Closed

`FakeTokenizer` và test liên quan đã bị xóa. Không còn mock/fake/stub trong ba
test file Phase 3.

### R4 — Open Major — Exact worktree before/after inventory vẫn thiếu

Vị trí: implementation report mục 5 và `CURRENT_HANDOFF.md` mục 3.

Requirement: correction R4 yêu cầu exact base/head/worktree before/after
inventory, tách toàn bộ pre-existing paths; complete worktree là minimum review
gate.

Evidence: hai tài liệu chỉ liệt kê Notebook 03 và CURRENT_HANDOFF là modified,
trong khi fresh `git status --short` còn có 17 tracked modified paths khác như
Reviewer-owned guides, umbrella spec/plan, READMEs và workflows/status. Handoff
có danh sách pre-existing untracked nhưng không liệt kê/tách nhóm tracked
modified này. Do đó tiêu đề “Worktree Inventory Before / After” không khớp nội
dung và correction R4 chưa đạt.

Tác động: Reviewer không thể audit từ handoff/report rằng mọi changed path đã
được nhận diện và tách khỏi correction scope; đây chính là traceability gap R4
đã yêu cầu đóng.

Tiêu chí đóng: cập nhật report và handoff bằng complete fresh
`git status --short`, phân nhóm rõ Phase 3/correction, Reviewer-owned hoặc
pre-existing tracked modifications, pre-existing untracked files và review
reports. Không sửa các path pre-existing; không tạo manifest/runtime mechanism.

Phần còn lại của R4 đã đóng: JSON có configured/observed model state; Qwen
observed CUDA/FP16/eager/1024D trong run Implementer; sparse evidence ghi
repeated-byte và round-trip; immutable Git/hash evidence khớp base. Ghi chú nhỏ:
report gọi nhóm Phase 2 là “205 Markdown curated”, trong khi tree hash bao phủ
toàn `knowledge-base-hue`; nên mô tả đây là 205 discovered Phase 2 sources và
whole-tree/no-diff proof để tránh nhập nhằng.

### R5 — Closed

Counts đã khớp source (`13 + 8 + 10 = 31`, cộng 4 BM25 = 35). Notebook canonical
sạch và nói rõ observed preflight, pending closure, Phase 4 đóng.

### External condition — Current GPU passthrough bị chặn trở lại

Fresh Reviewer preflight trả `BLOCKED_GPU`; `/usr/lib/wsl/lib/nvidia-smi` trả
`GPU access blocked by the operating system`, Torch 2.13.0+cu130 báo CUDA false,
device count 0. Đây không phải correction code regression, nhưng current JSON
artifact đã được exact rerun cập nhật trung thực thành `BLOCKED_GPU` và không
còn là closure PASS artifact.

## 3. Cách Reviewer chạy lại thật

```bash
HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-review-correction1-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py -q --tb=short

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-review-correction1-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_embedding_preflight.py \
  backend/tests/test_bm25.py -q --tb=short

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-phase3-review-correction1-uv-cache \
uv run python -m backend.evaluation.full_corpus_embedding_preflight \
  --sparse-output data/full_corpus_builds/phase_3_sparse_state.json \
  --evidence-output reports/artifacts/full_corpus_phase_3_embedding_sparse_preflight_2026_09_12.json

/usr/lib/wsl/lib/nvidia-smi
git diff --check
```

Reviewer còn đối chiếu `git status --short`, base diff, SHA-256, JSON bằng `jq`,
Notebook cleanliness và prohibited patterns.

## 4. Kết quả quan sát

- Core suite: `31 passed, 2 warnings`, exit 0.
- Extended suite: `35 passed, 2 warnings`, exit 0.
- Offline preflight: exit 1, JSON `BLOCKED_GPU`; Phase 2 identity/tokenizer gate
  và sparse state đã chạy đạt trước CUDA gate.
- Current GPU: NVIDIA WSL NVML bị OS block; Torch CUDA false/count 0.
- Sparse hash vẫn
  `5dcdda79cef8824eb0e4cc2b78cf1eb275b29dd892162b34d27ba804b5ccb3be`,
  repeated-byte true và round-trip true.
- `git diff --check`: sạch; immutable runtime/corpus/Golden/evaluation paths
  không có diff với base.
- Notebook canonical: năm code cells đều output rỗng/execution count null.

Hai warnings là Qdrant compatibility check từ test bootstrap và NVML init.
Implementer báo một warning ở run trước; khác biệt này phù hợp trạng thái GPU
hiện tại và không phải test failure.

## 5. Giới hạn hoặc phần chưa chạy

Notebook Run All không được lặp vì current GPU gate đã fail trước model path.
Prior corrected PASS artifact đã bị exact Reviewer rerun thay bằng current
honest `BLOCKED_GPU`, đúng failure contract. Reviewer không mutate host/Windows.

## 6. Decision và bước tiếp theo

Technical verdict: `FAIL` / `changes_requested` vì R4 còn một Major. Đồng thời
closure còn phụ thuộc khôi phục GPU passthrough và một fresh offline preflight
PASS.

Implementer thực hiện correction 2 rất hẹp: chỉ sửa report/handoff để hoàn tất
inventory; sau khi User khôi phục GPU, rerun exact current CUDA checks và
offline preflight để phục hồi fresh PASS evidence. Không đổi runtime/test/model,
không chạy lại full backend suite và không mở Phase 4.
