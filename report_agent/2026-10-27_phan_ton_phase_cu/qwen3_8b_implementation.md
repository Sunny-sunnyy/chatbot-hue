# Implementation Report: thí nghiệm Qwen3-Embedding-8B (dense thay e5-small) — tầng tìm

Người chạy: B (Claude Opus 5.5, `hue-rag-24`) · Date: 15:54 30/10/2026 (`date`) · Việc: A giao sau khi duyệt plan (14:53 30/10/2026). Quyền: User duyệt 29/10 gửi kho + câu
hỏi đánh giá ra OpenRouter (pin Nebius, `data_collection: deny`), tạo collection thử, xóa khi xong; trần 0,10 USD.
Plan: `qwen3_8b_plan.md` **`d6d6c7d51584`** (A duyệt; C review harness `qwen3_8b_harness_review.md` §8 ready). Harness: nhánh `b92-qwen3-harness` `01bf0c2`
(`backend/experiments/phase_8_2/qwen3_8b.py`). File này không chép câu hỏi / chữ kho — chỉ mã câu (`case_index`), số đếm, sha.

## Tóm tắt cho User (lời thường)

- **Thử gì:** đổi model tìm theo nghĩa từ e5-small (nhỏ, chạy trên máy) sang Qwen3-Embedding-8B (lớn, gọi qua mạng), xem có tìm được đoạn đúng nhiều hơn không.
- **Kết quả: kém hơn — không đưa vào chatbot.** Trên 40 câu dev có nhãn: 2 câu tốt hơn, **3 câu mất đoạn đúng** (sàn là 0 câu mất); hai lượt đo cho đúng cùng 3 câu ⇒ không phải
  do dao động. Nhóm kiểm (15 câu) cũng 2 tốt / 3 mất. Các chỉ số còn lại "không khác".
- **Còn chậm hơn nhiều:** riêng bước biến câu hỏi thành vector mất trung vị **2,2 s** (e5: 0,02 s), câu chậm 6,5–7,2 s ⇒ cả câu ước ~11 s so với trần 5 s bạn chốt.
- **Tiền:** **0,0089 USD** (trần 0,10). Collection thử **đã xóa**; bộ đệm vector (133 MB, private) còn giữ — xóa khi bạn duyệt.

## 1. Đã chạy (plan §6)

| Bước | Kết quả |
|---|---|
| Chuẩn bị (plan "Sửa đổi 30/10" mục 1–2, 7) | nhánh rebase lên `main` `bfb0b41` (gold **v5** `33d16fd6b8f4`); T1 trên nhánh giống byte `main` `4d5bbe9e0edc`; mốc e5 kho đợt 2 chạy 2 lần — tất định; dev 40: context đủ 24, pool dense 33, thiếu ở context 16, thiếu ngay ở pool dense 7; ngưỡng CI 95 % > 0: 4 / 0, 7 / 1, 9 / 2, 11 / 3 (C review ready) |
| 1 Preflight (free) | 1 collection runtime, chưa có `hue_c78_*`; có key OpenRouter (không in); gold v5; 8.424 đoạn = build record runtime; sparse runtime `c8134c49a648` |
| 3 Pilot (14:55) | 2 batch đầu (128 đoạn) + nhúng lại 20 đoạn: **chỉ Nebius**; cos lần 2 ↔ lần 1 min **0,99990** (≥ 0,999), mean 0,99992; 0 lỗi; 29,9 / 25,4 s mỗi batch ⇒ ước ~60 phút; 10.427 token / 128 đoạn ⇒ ước kho 686 nghìn token ≈ 0,0069 USD (≤ ước plan) ⇒ chạy tiếp |
| 4 Build (14:57–15:28, nền, timeout 110 phút) | `hue_c78_qwen3_8b_4096` **8.424** point (`verification` 8.424 / 8.424 / 5), ma trận 8.424 × 4.096; **providers chỉ Nebius**; sparse state **giống byte** runtime; build record riêng `58a0673e6ec2`; 133 lần gọi, **0** lỗi, 0 thử lại; 870.531 token ≈ 0,0087 USD; log `data/qwen3_8b_2026-10-28/build.log`, `emb/attempts.jsonl` |
| 5 Tầng tìm 8B | dev (`c78_8b_dev`), dev lần 2 (`c78_8b_dev_aa`), test (`c78_8b_test`) qua `g1_retrieval.run_config` mặc định + runner ghi log; providers Nebius; câu thử lại: 0 / 108, 0 / 108, **1 / 50** (2 %, dưới mức dừng 5 %) |
| 6 Khâu trả lời | **NOT RUN** — chỉ chạy khi tầng tìm "tốt hơn" (§7); tầng tìm "kém hơn" ⇒ dừng |
| 7 Dọn | trước khi xóa: 8.424 point, status green, 6 segment; **`DELETE` collection 15:5x** ⇒ Qdrant còn 1 collection runtime. Bộ đệm `emb/` 133 MB **giữ** (plan: xóa khi User duyệt) |

## 2. Kết quả theo tiêu chí ghi trước (plan §3, §7)

| Chỉ số | Vai trò | dev (40 có nhãn) | test (15) |
|---|---|---|---|
| `context_gold_all` (context đủ mọi fact), cặp 8B − e5 | **quyết** | 0,600 ⇒ 0,575; −0,025 [−0,125; +0,075]; **2 / 35 / 3** | 0,600 ⇒ 0,533; [−0,333; +0,200]; 2 / 10 / 3 |
| Câu **mất** đoạn đúng (e5 = 1, 8B = 0) | **sàn = 0** | **3** (132, 134, 135) — lần 2: đúng 3 câu đó | **3** (33, 130, 138) |
| Câu được thêm (e5 < 1, 8B = 1) | — | 2 (48, 70) | 2 (20, 21) |
| `pool_dense_gold_all` | theo dõi | 0,825 ⇒ 0,775; 4 / 30 / 6 | 0,733 ⇒ 0,867; 3 / 11 / 1 |
| MRR (keyword) | theo dõi | 0,731 ⇒ 0,736 (n 108); 24 / 59 / 25 | 0,700 ⇒ 0,674 (n 50) |
| Số chính dev 32 (bỏ câu không tự nhiên) | phụ | context 0,594 ⇒ 0,594 (2 / 28 / 2) | — |
| A/A 8B (hai lượt nhúng câu hỏi, cùng index) | nhiễu | cos min 0,99985, mean 0,99990; 6 / 109 vector giống byte; top-10 đổi 27 / 108; **`context_gold_all` đổi 0 / 40** | — |
| `dense_ms` p50 / p95 | theo dõi | e5 21 / 28 ms ⇒ 8B **2.228 / 6.487 ms** (lần 2: 2.305 / 7.240) | e5 21 / 28 ⇒ 8B 2.821 / 25.008 ms (đuôi chậm phía nhà cung cấp: 1 lần 504 sau ~62 s rồi thử lại được; 17 request thành công > 5 s, chậm nhất 75 s) |
| `dense_ms` 8B − e5 so +50 ms (luật (i)) | theo dõi | **+2,2 s** trung vị | — |
| p95 cả câu ước (4,9 s + chênh p95 `dense_ms`) | theo dõi | ≈ **11,4 s** (trần User 5 s) | — |
| Lỗi gọi câu hỏi | theo dõi | 0 / 109 · 0 / 109 | 1 / 52 dòng log ≠ 200 (thử lại thành công) |

**Kết luận (plan §7 `interpretation`): "kém hơn"** — vi phạm sàn "0 câu mất đoạn đúng" ở cả dev (3, ổn định qua hai lượt) lẫn test (3); chỉ số quyết CI chứa 0 và nghiêng âm.
Thêm: trượt rất xa điều kiện tốc độ (luật (i) +50 ms; p95 cả câu 5 s). ⇒ **không chạy khâu trả lời; chatbot giữ e5-small.**

## 3. Ghi chú / lệch

- Top-10 của 8B đổi giữa hai lượt ở 27 / 108 câu dù cùng index (vector câu hỏi qua API không tất định, cos ~0,9999) — chỉ số quyết không đổi, nhưng nếu dùng 8B thật thì kết quả
  tìm sẽ dao động theo lần hỏi.
- Lượt test: 1 câu gặp **504 sau ~62 s** rồi thử lại thành công; ngoài ra **17 request thành công > 5 s** (có 49 s, 75 s) ⇒ p95 riêng các request thành công đã ~25 s
  (C95 đếm 24,8 s) — đuôi chậm do phía nhà cung cấp, không chỉ do lần thử lại. Dev cũng có 18 (lần 2: 13) request thành công > 5 s, chậm nhất 12 s (lần 2: 16 s).
  Đếm từ `queries_c78_8b_{dev,dev_aa,test}.jsonl`; "chỉ câu gọi một lần" xem `qwen3_8b latency`. Làm mạnh thêm kết luận tốc độ, không đổi kết luận. (Sửa theo C95 m-1.)
- Bộ đệm `emb/` giữ để chạy lại không mất tiền (nếu sau này thử 8B ở khâu khác, vd rerank) — chỉ hợp lệ khi kho không đổi (cache khóa theo sha chữ gửi đi).
- Không đo (plan §9, NOT RUN): 8B làm rerank; instruction khác; nhà cung cấp khác; khâu trả lời.

## 4. Giới hạn

- Nhãn đoạn đúng chỉ 40 câu dev / 15 test ⇒ chỉ thấy hiệu ứng lớn; "kém hơn" ở đây dựa trên sàn (3 câu mất, ổn định), không phải CI.
- Một lần build (nhiễu phía index không đo; pilot cos 20 đoạn ≥ 0,9999).
- Độ trễ đo từ máy User tới OpenRouter / Nebius trong một khung giờ (chiều 30/10).

## 5. Bàn giao

- C kiểm: `data/phase_8_1/g1/c78_{e5,8b}_*.jsonl`, `data/qwen3_8b_2026-10-28/{build_summary.json, build.log, emb/attempts.jsonl, queries_*.jsonl, queries_*.npy}`; chạy lại free:
  `g1_retrieval compare --a c78_e5_dev --b c78_8b_dev --metrics context5_gold_all …`, `qwen3_8b aa --a c78_8b_dev --b c78_8b_dev_aa`, `qwen3_8b latency --name …` (worktree `/tmp/b92_qwen3`).
- A / User: đóng thí nghiệm "kém hơn"; quyết xóa `emb/` (133 MB) hay giữ; nhánh `b92-qwen3-harness` giữ làm hồ sơ (hoặc merge phần `dense_runner=None` nếu muốn dùng lại) — A quyết.
