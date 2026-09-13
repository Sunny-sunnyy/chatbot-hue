# Codex Review: Phase 4 Task 7 Candidate 1 Incident

Decision: changes_requested
Reviewer: Codex
Date: 2026-09-13 +07
Canonical guide: `guides/phase_4_qdrant_ingestion.md`
Implementation report: incident report supplied by User on 2026-09-13 +07

## 1. Phạm vi đã review

Reviewer kiểm exact failure path trong `verify_full_corpus_collection()`,
current worktree/record state và read-only `exists/get_collection/count` trên
duy nhất `hue_full_corpus_a_e5_small_384`. Không scroll/retrieve, không access
Foods, không sửa runtime, không chạy model/candidate và không mutation.

## 2. Findings

### I1 — Blocker — Live-write approval chưa có trong evidence hiện hành

Vị trí: `session_prompt/CURRENT_HANDOFF.md` tại thời điểm Task 7 được chạy và
incident report hiện tại.

Requirement: Task 7 chỉ được chạy sau verbatim User approval nêu đủ bốn target
collections. Review Contract yêu cầu Implementer lưu exact approval text.

Evidence: handoff vẫn ghi `Live-write approval: pending User confirmation` và
turn hiện tại không cung cấp approval text trước lệnh build. Việc User được mời
phê duyệt ở review trước không tự cấu thành approval.

Tác động: collection mutation đã xảy ra nhưng authority trail chưa kiểm chứng
được. Không hành động live nào tiếp theo được suy ra hoặc cấp hồi tố.

Tiêu chí đóng: User cung cấp exact prior approval nếu nó tồn tại; bất kể kết
quả, mọi recovery/delete/rerun tiếp theo vẫn cần authority mới ghi đúng target,
count và boundary.

### I2 — Major — Sample verification dùng set thay vì mapping

Vị trí: `backend/vectorstore/upsert.py:194-197`.

Requirement: sau exact count và full ID/payload verification, pipeline phải
retrieve/validate exact deterministic 12-point sample trước final build record.

Evidence: `chunk_by_id = {chunk.chunk_id for chunk in chunks}` tạo `set`, nhưng
dòng sau dùng `chunk_by_id[chunk_id]`, gây observed
`TypeError: 'set' object is not subscriptable`. Reviewer xác nhận source hiện
hành đúng như report.

Tác động: Candidate 1 đã ghi đủ 8.460 points nhưng completion verification
không kết thúc và không có final record; target phải được coi là failed partial
state. Candidates 2–4 dừng đúng contract.

Tiêu chí đóng: sửa đúng một dòng thành mapping `chunk_id -> chunk`, không thêm
helper/framework hoặc fake client test. Chạy focused pure suite và sau recovery
sẽ dùng exact real 12-vector readback làm regression evidence.

Finding này mới vì live Task 7 là lần đầu exact integration path đi qua phần
sample mapping; review trước chỉ được phép chạy pure value validators và không
được tạo/retrieve collection.

## 3. Cách Reviewer chạy lại thật

```bash
nl -ba backend/vectorstore/upsert.py | sed -n '150,220p'
test -e data/full_corpus_builds/hue_full_corpus_a_e5_small_384.json
```

Reviewer dùng Qdrant client thật read-only trên exact failed target để gọi
`collection_exists`, `get_collection`, validate schema và exact `count`.

## 4. Kết quả quan sát

- Root cause source: xác nhận set comprehension tại dòng 194 và subscript tại
  dòng 197.
- Target `hue_full_corpus_a_e5_small_384`: exists, exact Phase 4 schema PASS,
  count `8460`.
- Final record: absent; không có adjacent `.tmp.*` record file.
- Không có independent evidence cho trạng thái Foods hoặc candidates 2–4; các
  claim đó không cần cho quyết định recovery hiện tại.

## 5. Giới hạn hoặc phần chưa chạy

Reviewer chưa rerun full payload scroll hoặc 12-vector retrieve vì code chưa
được sửa và target đang ở failed state. Không chạy delete/reset/recovery.
Không có verbatim prior live-write approval trong evidence đã nhận.

## 6. Decision và bước tiếp theo

Technical verdict: `FAIL` — `changes_requested`; recovery đồng thời `blocked`
cho tới exact User delete approval.

Chọn **Clean Rebuild** theo approved recovery contract. Reject “verify and
complete in-place” vì nó bypass fresh-target guard/final-record pipeline và tạo
một recovery architecture chưa được duyệt.

Implementer trước hết xử lý code-only Correction 2 theo `CURRENT_HANDOFF.md` và
dừng. Sau independent correction review, Reviewer sẽ trình User một exact
guarded-delete approval cho duy nhất
`hue_full_corpus_a_e5_small_384` với observed count `8460`, verify absent rồi
rerun sequence từ Candidate 1. Không xóa hoặc rerun trước gate đó.
