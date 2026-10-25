# STATUS B — kết phiên 2026-10-25 17:07 +0700 (User kết phiên 17:0x; B25 dừng giữa chừng)

Terminal phiên này: `hue-rag-de` (A = `hue-rag-00`; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi
User (25/10, terminal B): B báo cáo trực tiếp cho A; việc A giao = User nói "làm đi".

## Trạng thái kết phiên
- **File đang khai báo sửa: không.** Đang giữ GPU: không. Server uvicorn kiểm (port 8000) đã dừng.
- **B25 rà code luồng dựng index + nền — DỞ** (dừng 17:05). File `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md` (đầu file ghi
  đã rà / chưa rà). 10 finding tạm; nổi bật **B-01 (cao)**: `core.schema` và `backend.core.schema` cùng nạp trong API ⇒ `chat.py` / `app.py`
  bắt sai lớp lỗi (Qdrant lỗi khi hỏi ⇒ 500 thay 503; corpus đổi lúc khởi động ⇒ 503 thay 409) — *suy ra* từ code + kiểm `is`, chưa tái tạo
  bằng lỗi thật. **Phiên sau:** rà nốt chunker / markdown_blocks / upsert, test, notebook 03 / 04, guide phase_0–4 + phần index
  `full_corpus_rag.md` + `guides/README.md` (2 sub-agent bị dừng, chưa ra file — giao lại); chốt top 10; rồi kiểm chéo top 5 của C.
- **8.2 tạm dừng (User 16:5x).** B1 (B23) xong, T1–T5 đạt, report `phase_8_2_b1_implementation.md` (sha `bb5fea83aeb6`) — **chờ A
  review**; code ở nhánh `p82-b1` (A cất, chưa merge). Dữ liệu `data/phase_8_2/b1/`.
- Review xong trong phiên: B22 spec 8.2 (3 vòng ⇒ ready; User duyệt `dabae90b2b60`); B24 B0 prep (2 vòng ⇒ ready, `doc_cap_mu.md`
  `37b66efb3499`). B đã thấy khóa X / Y ⇒ **B không làm người tóm nhãn** B0.
- Việc còn chờ B (theo handoff): review plan E1 của C (sha `f86240418ca1`) khi 8.2 chạy lại.

## Việc phiên chiều 25/10 (sau 15:51)
| Việc | Kết quả | File |
|---|---|---|
| B22 review spec 8.2 | 3 vòng: 4 major + 5 minor ⇒ 1 major + 2 minor ⇒ ready | `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_spec_review.md` |
| B23 B1 context 10 + NFC | plan duyệt `1a5ac660bd5d`; T1–T5 đạt; A/A context 10; nhiễu citation 12 vs 8 | `phase_8_2_b1_plan.md`, `phase_8_2_b1_implementation.md` |
| B24 review B0 prep | F1 major (lộ mù câu 17 `[Nguồn 8]`) ⇒ sửa ⇒ ready | `phase_8_2_b0_prep_review.md` |
| B25 rà code (dở) | 10 finding tạm | `report_agent/2026-10-25_ra_soat_code/ra_soat_code_B.md` |

## Tiền paid phiên chiều 25/10
- **B1: 0,0369194 USD** (log; 291.269 token vào / 15.585 ra, 176 câu) + live `/chat` 2 câu ≈ **0,0004 USD (ước — API không ghi usage)**.
  Judge: 8 sub-agent Claude (quota, 0 USD). Review / rà code: 0 USD. (Phiên sáng 25/10, 8.1: 0,1653212 USD — đã ghi ở các report 8.1.)

## File tạm / private
- `/tmp/b24/`, `/tmp/b24_out*`, `/tmp/b25/`, log uvicorn: **đã xóa** (17:06).
- Private B tạo phiên này: `data/phase_8_2/b1/` (lượt B1, judge, check / analyze, câu NFD tự viết); `data/ra_soat_code/` (rỗng).

## Đã học / bẫy gặp
- 25/10 B22: đọc JSON private bằng `python3 -I` thay vì `uv run python -I` (A nhắc) ⇒ mọi lệnh Python, kể cả chỉ đọc, dùng `uv run`.
- Qdrant có thể tắt giữa phiên; pytest vẫn chạy và lỗi môi trường trông như lỗi code: đọc dòng `E` trước.
- pytest: rootdir là gốc repo; chỉ liệt kê file test, không dựa vào `--deselect`.
- Lệnh paid mới: chạy thử không `--env-file` trước để thấy nó định gọi gì.
- Auto-mode chặn `curl -X DELETE` Qdrant / `rm` lớn: dừng, nhờ User chạy `!` trong terminal B.
- Hai session cùng sửa working tree: khi gate cần so byte mà file session khác đang dở, chạy bản HEAD (`git show HEAD:…`
  hoặc `git archive HEAD backend` vào `/tmp` + symlink `data/`, `knowledge-base-hue/` chỉ đọc).
- Script ngoài `backend/` cần `PYTHONPATH=.:..`.
- Qdrant không cam kết thứ tự hòa điểm; runtime và native đã phá hòa theo point_id.
- Validator citation: câu từ chối chuẩn + `[n]` = lỗi.
- `g1_retrieval run` với `--name` đã có sẽ ghi đè JSONL.
- `g1/c_runtime.jsonl` cùng tập câu với `runtime.jsonl` (dev, 108 câu) — không phải tập test; số test lấy theo `split.json`.
- Mở phiên: chưa biết terminal nào là A ⇒ gửi cùng tin cho cả hai peer, hỏi ai là A (25/10, ổn).
- Danh sách "chưa commit" trong STATUS / tin nhắn bị cũ khi A commit giữa chừng (25/10: báo g2_generate.py chưa commit
  trong khi đã ở `266c105`) ⇒ trước khi liệt kê, chạy `git status --short` + `git log --oneline -3`.
- Model "đã có trong HF cache" có thể chỉ là thư mục `refs` rỗng ⇒ kiểm `du -sh` / file `.safetensors` trước khi lập kế
  hoạch offline (25/10: M1 / M2 phải tải 2,2 GB mỗi cái; M2 cần `sentencepiece`).
- Lượt có phí với model tự suy luận: token ra có thể gấp ~3 lần ước (luna listwise ~270 token / câu) ⇒ luôn pilot 10 câu và
  ước lại từ pilot.
- Khi so điểm judge giữa biến thể, chấm baseline **cùng lượt mù** với biến thể (nhiễu judge-only đo được 2/88 câu).
- HNSW: kết quả dense phụ thuộc `limit` (30 đầu của `limit=100` ≠ `limit=30` ở 1/108 câu) ⇒ tái lập runtime phải hỏi
  đúng `limit` như production. Qdrant sparse tính float32 ⇒ phá hòa có thể khác float64 trong bộ nhớ.
- 25/10 B24: kiểm mù bằng regex chỉ dạng `[n]` bỏ sót `[Nguồn n]` do model tự viết ⇒ quét mọi cụm ngoặc vuông có số + "nguồn <số>".
- 25/10 B23: giờ ghi trong file phải lấy bằng `date` ngay trước khi ghi (B ghi nhầm 16:37 khi `date` là 16:32 — đã sửa).
- 25/10 B25: `python -m` từ `backend/` + `sys.path` có cả gốc repo ⇒ module nạp hai lần (`core.*` / `backend.core.*`), lớp lỗi khác nhau;
  khi so `isinstance` / `except` giữa module, kiểm `sys.modules`.

## Câu hỏi cho A / User
- B-01 (import kép): sửa cách import cho cả `backend/` là thay đổi nhiều file — chọn một kiểu import (`core.*` hay `backend.*`) và có tái
  tạo lỗi 503 / 409 bằng app thử (collection không tồn tại, port khác) không — A / User quyết.
- B-03: tham số sinh câu trả lời — hằng trong code hay yaml là nguồn (loader chỉ kiểm kiểu)?
- Mâu thuẫn corpus Hải Vân Quan vẫn chờ User (sửa khi build lại index).
