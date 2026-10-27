# Implementation Report: Phase 8.2 §10 R1 — mức suy luận `none` cho lượt sinh — dừng ở pilot, phạm sàn (câu 168)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-5b`) · 2026-10-27 09:23 +0700 (`date`) · Việc: C46 → chạy R1 (A giao 27/10; User duyệt quyền phiên 08:47 27/10).
Plan A duyệt: `phase_8_2_r1_plan.md` sha **`8e76e77e0448`** (bản 2, commit `78a5f05` trên `main`; C tính lại từ file ngay trước khi chạy: khớp). Spec §10 bản `cd910c4c4169`.
Code: nhánh `p82-r1` = `811d25d` + `d2646e6` (harness `r1.py`). **Tiền thật: 0,0049030 USD** (24 lần gọi `gpt-6-luna`).
Trạng thái: **chờ review** (B: report + harness).

Report không chép câu hỏi, đáp án, câu trả lời hay nội dung kho — chỉ `case_index`, số đếm, sha.

## Cho bạn — lời thường

1. Mình thử cho model **trả lời ngay, không suy nghĩ trước** (bỏ phần "suy luận ẩn"), để xem câu trả lời có rẻ / nhanh hơn mà vẫn đúng không.
2. Ở lượt thử đầu (24 câu), có **1 câu lẽ ra phải từ chối** (kho không có thông tin được hỏi) thì model lại trả lời vòng: nêu một thông tin có thật
   nhưng không phải điều được hỏi, rồi thêm câu "nguồn không nêu…". Theo luật ghi trước, đây là phạm sàn ⇒ **dừng, kết luận kém hơn**.
3. Câu trả lời đó **không bịa** (con số nêu ra đúng với nguồn), nhưng không trả lời câu hỏi và không dùng câu từ chối chuẩn — cùng dạng lỗi đã làm
   thí nghiệm "trả lời một phần" (R2) dừng hôm qua.
4. Trên 24 câu đó, token ra giảm khoảng 28 % và tiền mỗi câu giảm khoảng 3–6 % — đúng như dự đoán (tiền chủ yếu nằm ở phần đầu vào). Đây chỉ là số
   lượt thử, không dùng để kết luận. Tiền đã dùng: 0,0049 USD (≈ 120 đồng).

## 1. Phạm vi

Làm đúng plan §3 bước 1–2:
- bước 1: 12 câu OOS dev (sàn OOS);
- bước 2: pilot trong phạm vi 12 câu — 120, 168 (sàn "vẫn từ chối"), 172 (8.1 `none` trả lời không citation), 9 câu under-answer (gồm 173).

Bước 2 phạm sàn ở câu 168 ⇒ dừng theo plan §3 bước 2. **NOT RUN:** bước 3 (96 câu dev còn lại), judge (bước 4), test (bước 5), R4 (bước 6).
Không đổi production, không ghi Qdrant, không mở câu kín, không đọc câu test theo từng câu.

## 2. Thay đổi

`backend/experiments/phase_8_2/r1.py` (mới, `d2646e6`). Khung theo `r2.py` (`origin/p82-r2`); khác duy nhất ở `generate`:
`OpenAIFullCorpusGenerator.from_environment(settings, reasoning_effort="none")`. Mọi khâu khác qua `full_corpus_eval.answer_case` production
(retrieval, context 10 theo `settings.yaml` ở `811d25d`, prompt, validator). Lệnh: `run`, `merge`, `check`, `export-judge`, `check-judge`, `analyze`; mọi lệnh
ghi file từ chối ghi đè. Khác plan: không — `check` / `analyze` chưa chạy vì dừng ở bước 2.

## 3. Cách đã chạy thật

Worktree `/tmp/c_r1` (nhánh `p82-r1`), symlink `data/` + `knowledge-base-hue/` tạm. Từ `/tmp/c_r1/backend`, Qdrant `:6335` chỉ đọc, e5-small CPU:

```bash
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python -m experiments.phase_8_2.r1 run --cases oos_dev --name r1_oos_dev   # 09:20:58–09:21:09
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python -m experiments.phase_8_2.r1 run --cases early --name r1_early       # 09:21:41–09:21:59
```

Chạy sau khi K3 đã dừng (K3 L1 xong 09:03:42) — không chồng thời gian với lượt có phí khác (plan §6 Q3). Số ở §4 tính bằng `uv run python -c` đọc hai file kết
quả + `data/phase_8_2/b1/b1_dev.jsonl`.

## 4. Kết quả quan sát

Dữ liệu private `data/phase_8_2/r1/`: `r1_oos_dev.jsonl` (`5aebbf048711`), `r1_early.jsonl` (`a65765027572`), mỗi file kèm `.meta.json`
(`reasoning_effort` `none`, golden md5 `0f7dbf41b422`).

### 4.1 Bước 1 — 12 câu OOS dev: đạt sàn

12 / 12 trả câu từ chối chuẩn; 0 lỗi kỹ thuật; 0 lỗi citation. **0,0024497 USD.**

### 4.2 Bước 2 — pilot 12 câu trong phạm vi: phạm sàn ở câu 168

| Sàn (plan §2) | Kết quả |
|---|---|
| 120 vẫn từ chối | ✓ |
| **168 vẫn từ chối** | **✗ — trả lời** (không từ chối) |
| 172 / 173 (và mọi câu) không có câu có nội dung mà không citation (API 500) | ✓ — 0 / 12 câu `Grounded answer has no citation`; 172, 173 trả lời có `[n]` |
| lỗi kỹ thuật | ✓ 0 |

**Dạng lỗi câu 168** (C đọc câu trả lời + nguồn được trích, chỉ trong terminal): một câu nêu thông tin **đúng với nguồn được trích**, có `[n]`, nhưng là
thông tin **cùng chủ đề**, không phải điều câu hỏi hỏi; tiếp theo một câu **không citation** dạng "nguồn không nêu … nên chưa xác định được". Validator
production nhận câu trả lời này (có `[n]`, không chứa câu từ chối chuẩn) ⇒ người dùng nhận một câu trả lời không trả lời câu hỏi thay vì câu từ chối.
Cùng dạng với lỗi R2 câu 160 (`phase_8_2_r2_implementation.md`) và P1 8.1. Không phải "nói chắc sai": con số nêu ra đúng nguồn.

**0,0024533 USD.** Ước phần còn lại (plan §3 bước 2) không còn cần vì đã dừng.

### 4.3 Số theo dõi trên 24 câu đã chạy — **không dùng để kết luận** (pilot, không phải dev 120)

| | R1 | B1 cùng câu | Tỉ lệ |
|---|---:|---:|---:|
| `output_tokens` TB — OOS 12 | 31,0 | 42,3 | 0,73× |
| `output_tokens` TB — trong phạm vi 12 | 64,7 | 90,2 | 0,72× |
| USD / câu — OOS 12 | 0,000204 | 0,000210 | 0,97× |
| USD / câu — trong phạm vi 12 | 0,000204 | 0,000217 | 0,94× |
| latency sinh p50 — trong phạm vi 12 (B1 đo 26/10, khác phiên) | 2.355 ms | 2.250 ms | — |
| `top_chunk_ids`, `context_sources`, `input_tokens` = B1 | 24 / 24 | | đúng giả định G1 |

Khớp ước trong plan (G3, G4): token ra ~0,7×; USD sát 0,95× vì token vào chiếm ~81 % tiền.

## 5. Kết luận theo tiêu chí ghi trước

- **R1 (`reasoning_effort="none"`) — kém hơn (phạm sàn: câu 168, từ chối đúng ở mốc, bị trả lời).** Dừng ở pilot bước 2, đúng plan §3.
- **NOT RUN:** dev còn lại (96), judge, test, R4. Không có số Completeness / Accuracy.
- **Không đưa vào chatbot.**
- Hướng mở (C ghi, A / User quyết; *chưa đo*): lợi của R1 nhỏ (USD ~ −3–6 %, token ra ~ −28 %, độ trễ chưa thấy giảm trên 12 câu). Rủi ro đã thấy rơi đúng vào
  lỗi "trả lời vòng thay vì từ chối" — dạng đã chặn R2. Mở lại chỉ khi có cách bắt dạng này **được kiểm trước** (ví dụ kiểm bằng code sau sinh: câu trả lời có
  câu không citation dạng "nguồn không …"), như ghi chú hướng R2 trong `CURRENT_HANDOFF.md`. Đổi mức suy luận khác (`low`) = biến thể mới (spec §10.3 không chạy).

## 6. Lỗi và giới hạn

- Pilot chọn có chủ đích (câu sàn + câu U), không ngẫu nhiên ⇒ số §4.3 không đại diện dev 120.
- Model không tất định: một lượt; không biết câu 168 có lặp lại ở lượt khác không. Luật ghi trước dừng ở lần phạm đầu tiên — đúng như R2 / K3.
- Nhãn "168 từ chối đúng (context không có fact)" từ C36 (một người gắn); ở K3 số theo dõi, luna đưa thêm một phần fact của 168 vào top-10 — ở mốc B1 (context
  này) vẫn 0 fact.
- Tiền thật từ usage provider: 22.637 + 20.653 token vào, 372 + 776 token ra ⇒ 0,0049030 USD (= tổng hai `.meta.json`).

## 7. Bàn giao cho người kiểm (B)

- Đọc `r1.py` (`d2646e6`): đổi duy nhất `reasoning_effort="none"`; tập `early` = 120, 168, 172 + 9 U; từ chối ghi đè.
- Kiểm lại không tốn tiền: `refusal` của 168 trong `r1_early.jsonl` (false) so `b1_dev.jsonl` (true); 0 câu `Grounded answer has no citation`; tiền = tổng
  `usd`; tất định 24 / 24.
- Không cần chạy lại lượt có phí: kết luận chốt bằng một lần phạm sàn quan sát được.
