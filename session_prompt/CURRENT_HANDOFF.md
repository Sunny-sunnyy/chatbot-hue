# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 2026-10-24 14:00 (A). Cách dùng: `WORKFLOW.md` §3, §9. Chỉ giữ việc
đang mở; việc xong chuyển tóm tắt sang `PROJECT_HISTORY.md`.

## Session

| Vai | Terminal (ListAgents) | Agent | Việc hiện tại | Trạng thái |
|---|---|---|---|---|
| A — điều phối | `hue-rag-c3` | Claude Opus 5.5 | Trình User đóng Gate 3 + Phase 7A2 | chờ User |
| B — thực thi | `hue-rag-c0` | Claude Opus 5.5 | Phase 7A2 Gate 3 xong, A review đạt | rảnh, chờ việc |
| C — thực thi | (chưa mở) | Claude Opus 5.5 | — | User mở bằng `START_SESSION.md` |

## Quyền đang hiệu lực (User duyệt qua A)

- Git: A commit/push `origin main`; B/C không commit.
- Paid: không có việc paid đang mở.
- Qdrant: B xóa đúng 13 collection spec 7A2 §6.1 (đã xong); không tạo/sửa khác.
- Duyệt cho A = duyệt cho B/C (User 2026-10-24).

## Việc của A

- Governance v2 xong (commit `86e9431`).
- Gate 3: review đạt (`reports/phase_7a2_gate_3_review_2026_10_24.md`); trình
  User đóng Gate 3, rồi đóng Phase 7A2: xóa backup Gate 1
  `knowledge-base-hue/meta/backup_7a2_2026_10_23/` (cần User đồng ý), cập nhật
  `guides/full_corpus_rag.md`, ghi chú Phase 8 (spec 7A2 §7), user report.

## Việc của B — Phase 7A2 Gate 3: xóa 13 collection cũ + build record cũ

Mức rủi ro: cao (xóa không hoàn tác). Base commit `b781af8`. Paid: 0 call.

**Đọc:** `full-read` mục này + plan Task 9
(`docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md`);
`targeted-read` spec 7A2 §6 (bản sửa 2026-10-24: còn 3 collection, không có 8B).

**Làm:**

1. Ghi trạng thái trước: mọi collection + point count; file trong
   `data/full_corpus_builds/`. Kỳ vọng 16 collection = 13 (spec §6.1) + 2 Foods +
   `hue_full_corpus_7a2_e5_small_384`. Khác thì dừng, nhắn A.
2. Xóa đúng 13 collection spec §6.1, từng tên một, ghi kết quả. — **xong** (13 × `true`)
3. Xóa 8 `data/full_corpus_builds/hue_full_corpus_a_*.json` và
   `phase_3_sparse_state.json`; giữ `hue_full_corpus_7a2_e5_small_384.json` và
   `full_corpus_sparse_state.json`. — **xong** (User chạy `rm` bằng `!` trong
   terminal B vì permission của B chặn; 9 × `removed`)
4. Kiểm sau: còn đúng 3 collection, point count không đổi; thư mục build còn đúng 2
   file; health (`uvicorn api.app:app` từ `backend/` với `../.env`) HTTP 200, mọi
   component ready; dừng server. — **xong**: 3 collection (572 / 572 / 8.459),
   2 file, health 200 (uvicorn, và in-process sau khi xóa file); port 8018 đã tắt
   (User `kill`).
5. Report `reports/phase_7a2_gate_3_cleanup_implementation_2026_10_24.md`
   (trước/sau, lệnh, kết quả; không chép nội dung private). — **xong**

**Không làm:** đổi code; xóa ngoài danh sách; động vào `knowledge-base-hue/`.

**Dừng, nhắn A khi:** danh sách thực tế khác bước 1, lệnh xóa lỗi, point count
collection giữ lại đổi, health FAIL.

**Xong:** đổi trạng thái hàng B trong bảng Session thành "chờ review", cập nhật
`sessions/STATUS_B.md`, nhắn A.

## Việc của C

Chưa có. Sau khi Governance v2 xong, User mở C bằng `START_SESSION.md`; việc đầu
dự kiến: rà soát lựa chọn của Phase 2–6 (chỉ đọc) để lập danh sách giả thuyết cho
Phase 8.

## Đang chờ User

- Xác nhận đóng Gate 3 và đồng ý xóa backup Gate 1 khi đóng Phase 7A2.
- Mở lại A, B, C bằng `START_SESSION.md` (User đã báo).
