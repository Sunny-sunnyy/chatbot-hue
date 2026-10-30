# Review: B93 bước 1 — chuẩn bị áp đợt 2 sửa kho (chưa áp)

Người kiểm: C (Claude Opus 5.5, `hue-rag-0e`) · Date: 11:24 30/10/2026 (`date`) · Việc: A giao 30/10 (kiểm từng bước B93). Người làm: B (`hue-rag-24`).
Plan: `sua_kho_dot2_do_plan.md` bản 3 `5f30ac7eac16` §2, §6 bước 1. Chỉ đọc; 0 USD. File tracked chỉ ghi sha / số đếm.

## Kết luận

`ready_for_user_confirmation` — 0 / 0 / 0. Bước 1 đúng plan; kho và Qdrant chưa đổi (40 file kho giống byte backup; collection 8.426 point) ⇒ B áp bước 2 được.

## Đã kiểm (máy)

| Mục | Kiểm | Kết quả |
|---|---|---|
| (a) `dot2/eval_truoc/` | `cmp` + sha 3 bản sao ↔ `eval_sau/` đợt 1 | giống byte: `truoc.jsonl` `07e1d6571fb4`, `preflight_truoc.json` `31c7afcf30c5`, `chunks_truoc.json` `7392734a512c` ✓; `check_truoc.json` ↔ `check_sau.json` khác **chỉ** trường `arm` ✓ |
| 4 kiểm "còn hiệu lực" (B) | C chạy lại (1), (2): `git diff 748c1e3 HEAD -- backend/` trừ tests / experiments rỗng (HEAD `e70007b`); record / sparse dưới | ✓ ((3) T1, (4) meta: dựa số B ghi trong README — không chạy lại) |
| (b) backup kho `knowledge-base-hue/meta/backup_sua_kho_dot2_2026-10-30/` | tập file ↔ tập file trong `dot2.jsonl` `c0b5876ea510`; so byte với kho hiện tại | 40 / 40 file, 0 thiếu, 0 khác byte ✓; thêm 1 file mẫu chunker (giống byte kho) — có ích để khôi phục test mẫu, không phải lệch |
| (c) `dot2/backup/` | sha record, sparse ↔ `data/full_corpus_builds/`; sha256 snapshot ↔ checksum Qdrant (`GET …/snapshots`) | record `574b5d02088b` ✓, sparse `1bae9e0f3c49` ✓; snapshot 50.919.424 byte, sha256 **trùng** checksum Qdrant ✓ |
| (d) `an_toan_run.py` `7f84db74bec6` ↔ `an_toan_aa.py` `ea02a89ff594` `gen` | đọc hai bản | thân vòng sinh giống từng dòng (search ⇒ build ngữ cảnh ⇒ `answer_case` ⇒ cùng trường + `repeat`); thêm `--out` (thư mục mới, `mkdir` từ chối ghi đè), `--qids` (qid lạ ⇒ dừng), `--repeat` (mỗi lần một file `answers_r<k>.jsonl`, mở `"x"`), `--cap` (bắt buộc, kiểm trước mỗi câu như C84). Không sửa `an_toan_gen.py` / `an_toan_aa.py` ✓ |
| (e) `an_toan/moc_regen_2026-10-30/` | 3 file × 2 câu (S11, S12); so với B89 + lượt A/A | 6 / 6 dòng, 0 lỗi / từ chối / lỗi citation; ngữ cảnh giống từng chữ B89 **và** A/A, top đoạn giống B89 ở cả 6 ✓; câu trả lời khác B89 ở cả 6 (đúng là sinh lại); meta: `gpt-6-luna`, context 10, commit `e70007b`, 0,0017045 USD = tổng `usd` các dòng ✓, không chạm trần 0,005 |

## Ghi chú (không phải finding)

- 6 câu trả lời mốc **chưa chấm** — plan §5 A2 vế 1: chấm cùng rubric ở bước 9 (cùng lượt mù với "sau") để có số lần P0_sai mỗi bên.
- `--out` nhận cả đường dẫn tuyệt đối (`B / "/…"`) — chỉ người chạy dùng, không cần chặn.
