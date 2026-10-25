# STATUS B — cập nhật 2026-10-25 14:23 +0700 (nghỉ, chờ A sau khi User đóng 8.1)

Terminal phiên này: `hue-rag-3f` (A = `hue-rag-c6`, C = `hue-rag-a1`; tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi
User (25/10, terminal B): việc A giao = User nói "làm đi"; xong báo cáo, nhắn A, chờ việc tiếp.

## Trạng thái
- **Phần 8.1 của B đã hết** (A 14:2x). Không mở việc mới; chờ User đóng 8.1 → A brainstorm 8.2 rồi giao.
- Đang giữ GPU: **không** (G4 dùng 11:50–12:29, đã nhả).
- Chờ người khác: C review prompt B21 (`gửi chatgpt/2026-10-25/tìm thông tin/phase_8_2_khong_dau_2026_10_25.md`, private,
  C review ready, 2 minor tùy chọn đã áp — sha mới `6eb09b4066ca`); User gửi ChatGPT khi tiện, lưu kết quả vào `gửi chatgpt/2026-10-25/kết quả nghiên cứu/`.

## Việc phiên 25/10 (đã xong; số và kết luận ở report)
| Việc | Kết quả | Report / commit |
|---|---|---|
| B17 bước 1 — sửa plan G2/G4 | duyệt `a4adfc8eedd9` (2 vòng C23) | `phase_8_1_g2_g4_plan.md` · `b9789f4` |
| B17 G4 rerank (GPU + luna) | không nhánh nào tốt hơn; luna tín hiệu MRR +0,17 | `phase_8_1_g4_implementation.md` · `ee557f9` |
| B17 G2 sinh câu trả lời | **context 10 tốt hơn, xác nhận test**; P1 / G2.4 none / low kém hơn; còn lại không khác | `phase_8_1_g2_implementation.md` · `266c105` |
| B18 G4 từ khóa BM25 | không biến thể nào tốt hơn; khử dấu = tín hiệu cho câu không dấu | `phase_8_1_g4_keyword_*` · `50006da` |
| B19 bảng G5 | bảng chính thức G5 | `phase_8_1_g5_decision_table_draft.md` |
| B20 3 báo cáo User | TIM_KIEM / SINH_CAU_TRA_LOI_API / CHIA_DOAN, C review ready | `23e0cbf` |
| G5 M1 theo loại câu | context 10 lợi ở nhiều nguồn / so sánh | `phase_8_1_g5_by_category.md`, `g5_by_category.py` |
| Review (B kiểm) | G3 ready · G3 §10 · G5 (2 vòng, ready) · C30 ready · G0.6 ready | `phase_8_1_{g3,g3_b10,g5,c30_user_reports,g0_6}_review.md` |
| B21 prompt nghiên cứu không dấu | chờ C review | private |

## Thay đổi CHƯA COMMIT của B (git status 14:23, sau `471e717`)
- `session_prompt/sessions/STATUS_B.md` (file này).
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g0_6_review.md` — thêm §6 (đóng m1/m2 của C31).
- Không phải của B: `báo cáo nghiên cứu github.txt` (User).

## Tiền paid (B, 25/10)
- **0,1653212 USD** = G4 luna 0,0087972 + G2 0,1565240 (G2: 1.147.055 token vào / 83.637 ra). G3 / G4K / review: 0 USD.
  Judge + `answer_type`: 29 sub-agent dùng quota Claude Code (0 USD). Không lượt nào vượt luật tiền A chốt (≤ 1,5 × ước pilot,
  ≤ 0,05 USD / lượt, B17 ≤ 0,25 USD).

## File private B tạo (không commit)
- `data/phase_8_1/g4/` (rerank, `subset.json` `b9b6e6123ba4`), `data/phase_8_1/g2/` (câu trả lời, meta, `judge/`, `judge_test/`,
  `judge_g24/`), `data/phase_8_1/g4k/` (dense + BM25 trong bộ nhớ). HF cache: M1 / M2 reranker (2,2 GB mỗi cái).
- Log tạm `/tmp/b17/` (có thể mất).

## Đã học / bẫy gặp
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

## Câu hỏi cho A
- Không còn câu hỏi mở cho 8.1. Mâu thuẫn corpus Hải Vân Quan — vẫn chờ User (đề xuất sửa khi build lại index ở 8.2).
