# Active — Phase 7A2 Gate 3: xóa 13 collection cũ + build record cũ

Target role: implementer (B)
Authored by: reviewer/điều phối (A)
Handoff kind: implementation
State: active
Base commit: b781af8
Head commit: worktree
Risk level: high (xóa không hoàn tác)
Git authorization: none (A commit sau review)
Sub-agent authorization: theo standing authorization trong `IMPLEMENTER_WORKFLOW.md`
Paid-call authorization: không cần (0 call)
Qdrant authorization: xóa đúng 13 collection trong spec §6.1; không tạo/sửa collection nào

User đã duyệt Gate 3 trong spec (2026-10-23) và đóng Gate 2 ngày 2026-10-24.
User làm việc với A; quyền ghi trong handoff này là quyền User đã duyệt.

## Đọc

- `full-read`: handoff này; plan Task 9 (`docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md`)
- `targeted-read`: spec §6 (bản đã sửa 2026-10-24: còn 3 collection, không có 8B)

## Việc (plan Task 9, có điều chỉnh vì 8B hoãn)

1. Ghi trạng thái trước: danh sách mọi collection + point count; danh sách file
   trong `data/full_corpus_builds/`. Hiện có 16 collection = 13 trong spec §6.1
   + `hue_foods_e5_small_384` + `hue_foods_e5_small_384_dense` +
   `hue_full_corpus_7a2_e5_small_384`. Nếu thực tế khác danh sách này: dừng, báo A.
2. Xóa đúng 13 collection trong spec §6.1, từng tên một (lệnh mẫu ở plan Task 9
   Step 2); ghi kết quả từng lệnh.
3. Xóa 8 build record `data/full_corpus_builds/hue_full_corpus_a_*.json` và
   `data/full_corpus_builds/phase_3_sparse_state.json`. Giữ
   `hue_full_corpus_7a2_e5_small_384.json` và `full_corpus_sparse_state.json`.
4. Kiểm sau:
   - Qdrant còn đúng 3 collection: hai Foods + `hue_full_corpus_7a2_e5_small_384`;
     point count không đổi so với bước 1.
   - `data/full_corpus_builds/` còn đúng 2 file nêu ở bước 3.
   - Health runtime: `uvicorn api.app:app` từ `backend/` với `../.env`, `GET /health` HTTP 200, mọi component ready; dừng server.
5. Report `reports/phase_7a2_gate_3_cleanup_implementation_2026_10_24.md`
   (trạng thái trước/sau, lệnh, kết quả; không chép nội dung private).

## Ranh giới

Không đổi code, không xóa collection/file ngoài danh sách, không động vào
`knowledge-base-hue/` (backup Gate 1 xóa khi đóng Phase, không phải bây giờ).

## Dừng và nhắn A khi

Danh sách thực tế khác bước 1, một lệnh xóa lỗi, point count collection được giữ
đổi, hoặc health FAIL.

## Đầu ra

Thay handoff này bằng `final_review` cho A; SendMessage `hue-rag-c3`.

## Lịch sử

Gate 2 đóng 2026-10-24 với giới hạn (8B hoãn sang Phase 8):
`reports/phase_7a2_gate_2_review_2026_10_24.md`.
