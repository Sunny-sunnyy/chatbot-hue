# Codex Review: Phase 4 Task 7 Correction 2

Decision: ready_for_user_recovery_confirmation
Reviewer: Codex
Date: 2026-09-13 +07
Canonical guide: `guides/phase_4_qdrant_ingestion.md`
Implementation report: Correction 2 report supplied by User on 2026-09-13 +07

## 1. Phạm vi đã review

Reviewer kiểm exact one-line correction trong
`verify_full_corpus_collection()`, chạy lại focused pure suite, kiểm
`git diff --check`, kiểm final-record path và dùng Qdrant client thật read-only
trên duy nhất failed target `hue_full_corpus_a_e5_small_384` để xác nhận
state/schema/count. Không access Foods hoặc other collections, không
scroll/retrieve, không chạy model/candidate và không mutation.

## 2. Kết quả findings

### I1 — Blocker — Closed

User-provided evidence hiện đã chứa nguyên văn prior live-write approval, nêu
đủ đúng bốn target collections và các exclusion. Evidence này đóng gap
authority trail cho lần chạy Task 7 trước.

Approval cũ không cấp quyền delete/reset/recovery. Vì vậy nó không cho phép
xử lý failed target hoặc tiếp tục sequence ở trạng thái hiện tại.

### I2 — Major — Closed

Tại `backend/vectorstore/upsert.py:194`, mapping hiện là:

```python
chunk_by_id = {chunk.chunk_id: chunk for chunk in chunks}
```

`chunk_by_id[chunk_id].point_id` vì thế không còn subscript một `set`. Exact
delta đúng phạm vi Correction 2; không có thay đổi runtime khác được yêu cầu.

## 3. Verification độc lập

```bash
HF_HUB_OFFLINE=1 \
UV_CACHE_DIR=/tmp/hue-rag-phase4-correction2-review-uv-cache \
uv run python -m pytest \
  backend/tests/test_full_corpus_embedding.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py -q --tb=short
```

Kết quả: `41 passed in 4.69s`, exit code 0.

`git diff --check` trả exit code 0. Final build record
`data/full_corpus_builds/hue_full_corpus_a_e5_small_384.json` absent và không
có adjacent `.tmp.*` record.

Read-only live observation:

```text
target: hue_full_corpus_a_e5_small_384
state: non_empty
schema: PASS
point_count: 8460
final build record: absent
blocker: target is non-empty: 8460 points
```

## 4. Giới hạn

Focused suite chứng minh regression thuần không phát sinh, nhưng chưa thể tự
nó chứng minh exact 12-vector live retrieve path. Evidence đó phải đến từ
Clean Rebuild sau guarded recovery. Reviewer không xác minh claim về Foods vì
boundary không cho phép và claim đó không cần cho decision này.

## 5. Decision và gate kế tiếp

Correction 2 technical verdict: `PASS`.

Task 7 vẫn `BLOCKED` ở recovery gate. Reviewer tiếp tục chọn **Clean Rebuild**;
không chấp nhận complete in-place. Trước bất kỳ mutation nào, User phải phê
duyệt riêng guarded deletion cho duy nhất
`hue_full_corpus_a_e5_small_384`, observed count `8460`, với exact confirmation
string:

```text
DELETE hue_full_corpus_a_e5_small_384
```

Sau approval: guarded reset exact target, verify absent, rồi resume Task 7 từ
Candidate 1 theo sequence và boundaries đã được phê duyệt; dừng ngay nếu bất
kỳ candidate nào thất bại. Không có quyền xóa target khác, access Foods, hoặc
thực hiện Git operation.
