# STATUS B — cập nhật 2026-10-24 22:47 +0700 (kết phiên)

Terminal phiên này: `hue-rag-b0` (A = `hue-rag-47`, C = `hue-rag-a3`; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang chờ (phiên sau) — KHÔNG chạy gì, kể cả GPU/paid, tới khi A duyệt
- **Kế hoạch G2 + G4:** `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_g4_plan.md` (B16, tiêu chí ghi trước,
  ước ≈ 0,14–0,23 USD trong trần 8.1 0,5 USD). Chờ A duyệt.
- **Lệch spec cần A/User quyết:** spec 8.1 §5 G4 "chỉ xếp lại thứ tự top-10, không chọn đoạn ngoài tập" vs đầu vào
  pool 100 (G4-B). Kế hoạch tách G4-A (theo spec) / G4-B (chỉ chạy nếu sửa spec).
- Thứ tự đề xuất khi được duyệt: chạy lại mốc byte → G4.0 pilot latency GPU → G4-A (M1/M2 free, luna pilot 10 câu) →
  G2.0/G2.1 → G2.2 → G2.3 → G2.4 pilot.

## Thay đổi CHƯA COMMIT của B (lúc 22:47)
- `backend/experiments/phase_8_1/g1_retrieval.py` — B16: đọc `golden_realism_final.jsonl`, thêm `--realism main`
  (bỏ câu `unnatural`, câu `disputed_unnatural` tạm tính vào).
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md` — thêm §7 bảng phụ số chính.
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g2_g4_plan.md` — mới (untracked).
- `session_prompt/sessions/STATUS_B.md` (file này), dòng B + mục "Việc của B" trong `CURRENT_HANDOFF.md`.
- Không có code production nào chưa commit. `git diff --check` sạch.

## Vừa xong phiên 24/10 tối (đã commit bởi A trừ phần trên)
- **B9** dọn sau Phase 7 — `1832201`, User đóng 20:01 (smoke 10: 0,0013334 USD).
- **B10** 4 báo cáo khâu bản 2 — `74270ab`.
- **B11** G0.5 tham số mặc định-như-cũ (generator/retrieval/build) — `b8dbe95`; review C16 (ready, 3 minor).
- **B12** điều tra mốc `native_hybrid_rrf` không tái lập: chứng minh do thứ tự hòa điểm nhánh sparse Qdrant.
- **B13** phá hòa sparse native `(-score, point_id)` — `0131afb`; mốc native mới `1fbb5c17…`.
- **B14** review đoạn đúng G0.3 (55 câu, ready, 8 minor — A đã áp).
- **B15** kế hoạch + harness + đo G1 — `8156395`: nghẽn ở xếp hạng (union@100 đủ fact 0,975 / top-10 0,55–0,60);
  22 câu từ chối nhầm đều thiếu fact trong context; không biến thể fusion nào qua Holm; NFD tụt (NFC cứu), không dấu sập;
  HNSW = exact; MiniLM vượt 512 = 0.
- **B16** bảng phụ số chính + kế hoạch G2/G4 (chưa commit, xem trên).

## File private đang dùng (không commit)
- `data/phase_8_1/g1/*.jsonl` — kết quả G1 từng câu (21 cấu hình + `pilot_*`).
- `data/phase_8_1/gold/gold_draft.jsonl` (đoạn đúng, bản khóa G1, SHA-256 `bab707b9…`) + `batch_*`, `selection.json`.
- `data/phase_8_1/baseline/retrieval_native_hybrid_rrf_b13.jsonl` (mốc native `1fbb5c17…`).
- `data/phase_8_1/golden_realism_final.jsonl` (nhãn độ tự nhiên, số chính = bỏ `unnatural`).
- Mốc runtime: `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl` (`cefb2d1a…`).
- Script/log tạm (có thể mất): `/tmp/b15/run_g1.sh`, `/tmp/b11/`, `/tmp/b13/`.

## Tiền paid phiên (B)
- 0,0013334 USD (B9 smoke 10). B11–B16: 0 USD (sub-agent dùng quota Claude Code).

## Đã học / bẫy gặp
- Qdrant có thể tắt giữa phiên; pytest vẫn chạy và lỗi môi trường trông như lỗi code: đọc dòng `E` trước.
- pytest: rootdir là gốc repo; chỉ liệt kê file test, không dựa vào `--deselect`.
- Lệnh paid mới: chạy thử không `--env-file` trước để thấy nó định gọi gì.
- Auto-mode chặn `curl -X DELETE` Qdrant / `rm` lớn: dừng, nhờ User chạy `!` trong terminal B.
- **Hai session cùng sửa working tree:** khi gate cần so byte mà file của session khác đang dở (ví dụ evaluator), chạy
  bản HEAD của file đó (`git show HEAD:… > /tmp/…`, chỉ đổi đường gốc) hoặc `git archive HEAD backend` vào `/tmp`
  + symlink `data/`, `knowledge-base-hue/` (chỉ đọc). Gói `backend` không cài vào `.venv`, import theo vị trí file.
- Script ngoài `backend/` cần `PYTHONPATH=.:..` (import `backend.*` lẫn `core.*`).
- **Qdrant không cam kết thứ tự hòa điểm** (đổi theo `limit`, trạng thái); runtime `dense_bm25_rrf` tất định nhờ phá hòa
  theo point_id; sau B13 native cũng vậy. Còn lại: hòa điểm vắt qua biên pool làm *tập* ứng viên phụ thuộc pool.
- Validator citation: câu trả lời chứa câu từ chối chuẩn + `[n]` = lỗi — prompt "trả lời một phần" phải báo thiếu bằng câu khác.
- Chạy `g1_retrieval run` với `--name` đã có sẽ ghi đè file JSONL.

## Câu hỏi cho A (phiên sau)
- Duyệt `phase_8_1_g2_g4_plan.md`; quyết G4-B (sửa spec §5 G4 hay giữ top-10-only).
- G2.3: chọn 1–2 chính sách validator citation thay thế để phát lại.
- Mâu thuẫn corpus Hải Vân Quan (`travel/places/Đèo Hải Vân.md:84` vs file vé) — A đã báo User; chờ quyết sửa corpus.
