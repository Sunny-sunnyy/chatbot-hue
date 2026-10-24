# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 2026-10-24 13:15 (A). Cách dùng: `WORKFLOW.md` §3, §9. Chỉ giữ việc
đang mở; việc xong chuyển tóm tắt sang `PROJECT_HISTORY.md`.

## Session

| Vai | Terminal (ListAgents) | Agent | Việc hiện tại | Trạng thái |
|---|---|---|---|---|
| A — điều phối | `hue-rag-c3` | Claude Opus 5.5 | Áp dụng Governance v2; review Gate 3 | đang làm |
| B — thực thi | `hue-rag-c0` | Claude Opus 5.5 | Phase 7A2 Gate 3 | chờ User xóa 9 file |
| C — thực thi | (chưa mở) | Claude Opus 5.5 | — | User mở sau khi Governance v2 xong |

## Quyền đang hiệu lực (User duyệt qua A)

- Git: A commit/push `origin main`; B/C không commit.
- Paid: không có việc paid đang mở.
- Qdrant: B xóa đúng 13 collection spec 7A2 §6.1 (đã xong); không tạo/sửa khác.
- Duyệt cho A = duyệt cho B/C (User 2026-10-24).

## Việc của A

- Áp dụng Governance v2 (`docs/superpowers/specs/2026-10-24-governance-v2-design.md`
  §7 bước 3–6, 9). Khai báo sửa: `session_prompt/*`, `skills/*`, `.claude/skills/*`.
- Review Gate 3 khi B bàn giao; trình User đóng Gate 3, rồi đóng Phase 7A2.

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
   `full_corpus_sparse_state.json`. — **bị permission của B chặn; chờ User chạy
   bằng `!` trong terminal B**
4. Kiểm sau: còn đúng 3 collection, point count không đổi; thư mục build còn đúng 2
   file; health (`uvicorn api.app:app` từ `backend/` với `../.env`) HTTP 200, mọi
   component ready; dừng server (port 8018 đang chạy, chờ User `kill`).
5. Report `reports/phase_7a2_gate_3_cleanup_implementation_2026_10_24.md`
   (trước/sau, lệnh, kết quả; không chép nội dung private).

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

- Chạy trong terminal B:
  `! cd /home/minhhieu/hue_rag && rm data/full_corpus_builds/hue_full_corpus_a_*.json data/full_corpus_builds/phase_3_sparse_state.json && ls data/full_corpus_builds/`
  và `! kill 321255 321261` (server health port 8018).
- Đóng Gate 3 sau review của A.
