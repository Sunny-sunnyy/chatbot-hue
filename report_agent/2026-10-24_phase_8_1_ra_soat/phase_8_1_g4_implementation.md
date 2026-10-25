# Implementation Report: Phase 8.1 G4 — xếp hạng lại (rerank)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 (giờ ghi theo `date`) · Việc: B17 bước 2 ·
Kế hoạch duyệt: `phase_8_1_g2_g4_plan.md` sha `a4adfc8eedd9` (A 11:40, commit `b9789f4`) · Spec 8.1 §5 G4 (gồm sửa đổi
User 25/10) · skill `run-experiment`.

## 1. Phạm vi

Đã làm: mốc byte; tập câu cố định; G4.0 đo latency (CPU + GPU); G4-A (xếp lại top-10: M1, M2 × đoạn trơn / đoạn kèm mục,
luna listwise); G4-B (M1 đoạn trơn trên pool 100) + mốc native pool 100 không rerank. Không đổi chatbot / settings runtime,
không ghi Qdrant, không mở câu kín. Xác nhận trên test: xem §4.4.

## 2. Thay đổi

- `backend/reranking/cross_encoder.py`: `CrossEncoderReranker(..., max_length=None)` truyền thẳng cho `CrossEncoder` (để
  cắt cặp ≤ 1024 token như nhau cho M1/M2) và property `loaded_device` (thiết bị thật sau khi nạp, cho bước kiểm GPU).
  Mặc định `None` = hành vi cũ; runtime đang chạy `reranker: none` nên không gọi tới lớp này.
- `backend/experiments/phase_8_1/g4_rerank.py` (mới): harness; logic biến thể chỉ ở đây — đầu vào pool 100 (hợp hai nhánh
  native), "đoạn kèm mục", rerank listwise bằng `gpt-6-luna`, kiểm GPU 4 điều, trần thời gian. Dùng lại `compare`,
  `gold_coverage`, `load_gold`, `load_payloads`, `keep_realism` của harness G1.
- `pyproject.toml` + `uv.lock`: `uv add sentencepiece` → **0.2.2** (A duyệt; User 25/10). Lý do: M2 không có
  `tokenizer.json`, chỉ có `sentencepiece.bpe.model`, nên transformers cần gói này mới dựng được tokenizer. `uv.lock` chỉ
  thêm đúng gói đó.
- Model tải về HF cache (không phải "đã có sẵn" như plan §0 ghi — cache chỉ có thư mục `refs` rỗng): M1
  `BAAI/bge-reranker-v2-m3` rev `953dc6f6f85a…`, M2 `AITeamVN/Vietnamese_Reranker` rev `f53697624840…`, 2,2 GB mỗi model,
  11:45–11:47; từ đó chạy `HF_HUB_OFFLINE=1`. File `sentencepiece.bpe.model` của M1 và M2 giống hệt (sha `cfc8146a…`).

## 3. Cách đã chạy thật

Từ `backend/`, `uv` trong `.venv`. Kết quả từng câu + meta (kiểm GPU, latency, usage): `data/phase_8_1/g4/*.jsonl`,
`*.meta.json` (private). Log: `/tmp/b17/` (có thể mất).

1. Mốc byte (11:39): `full_corpus_eval retrieval --treatment dense_bm25_rrf|native_hybrid_rrf --golden full` → sha
   `cefb2d1a…` và `1fbb5c17…` — **PASS** (giống từng byte). Sau khi sửa `cross_encoder.py` chạy lại `dense_bm25_rrf`
   (12:32): vẫn `cefb2d1a…` — **PASS**. `pytest tests/test_full_corpus_retrieval.py` 26 passed (có
   `test_cross_encoder_primitives_contract`); MiniLM mặc định vẫn `max_length` 512, `cpu`.
2. `g4_rerank subset` → `data/phase_8_1/g4/subset.json` sha `b9b6e6123ba4` (dev 30, pilot 10, pilot CPU 5, test 15; seed
   20261024, đúng plan §1.1).
3. `g4_rerank run --name <cấu hình> --cases … --input top10|pool100 --reranker none|m1|m2|luna --text plain|section
   --device cuda|cpu`, mỗi lượt một cấu hình, tuần tự. Luna: pilot 10 câu (`--cases pilot`) → đo USD → 20 câu còn lại
   (`--cases dev30_rest`), gộp hai file. Lệnh luna chạy thử trước không có khóa API: dừng ở bước tạo client, 0 lời gọi.
4. `g4_rerank compare --a base_runtime --b … --metrics context5_gold_all mrr …` (bootstrap 10.000, seed 20261024, Holm
   trên số biến thể truyền vào); `g4_rerank summary --names … [--realism natural]`.

**Kiểm GPU (plan §0) — mọi lượt GPU đạt:** `torch.cuda.is_available()` True; `loaded_device` = `cuda:0`; `nvidia-smi`
chỉ thấy đúng pid của lượt (WSL không báo VRAM theo tiến trình, nên ghi tổng `memory.used` = 2.253 MiB sau khi nạp model);
thời gian câu cỡ GPU (top-10 đoạn trơn ~0,85 s so với CPU ~4,9 s).

## 4. Kết quả quan sát

### 4.0 Mốc trên dev 30 (không rerank)

Chạy lại bằng harness G4 (context lấy từ `packed.sources`): **0 câu lệch** G1 ở top-10, context, MRR (C23 m4 không xảy ra).

| Mốc | đoạn đúng đủ trong 5 đoạn | top-10 | đầu vào | MRR@10 | nDCG@10 |
|---|---:|---:|---:|---:|---:|
| runtime (pool 30) | 12/30 | 15/30 | 15/30 | 0,424 | 0,499 |
| native pool 100 | 15/30 | 18/30 | 29/30 | 0,452 | 0,540 |

### 4.1 G4.0 — latency (ms, p50 / p95; bỏ lần nạp model + 1 câu khởi động)

| Cấu hình | thiết bị | n | cả luồng | rerank |
|---|---|---:|---:|---:|
| M1 top-10 đoạn trơn | CPU | 5 | 4.886 / 6.640 | 4.855 / 6.609 |
| M2 top-10 đoạn trơn | CPU | 5 | 4.902 / 6.386 | 4.864 / 6.360 |
| M1 top-10 đoạn trơn | GPU | 10 | 848 / 1.186 | 807 / 1.138 |
| M1 top-10 đoạn kèm mục | GPU | 10 | 2.731 / 4.758 | 2.699 / 4.725 |
| M1 pool 100 đoạn trơn | GPU | 10 | 8.835 / 12.875 | 8.791 / 12.830 |
| M1 pool 100 đoạn kèm mục | GPU | 1 | **165.272 — dừng** (câu đo đầu > 60 s, plan §0) | |
| M2 top-10 đoạn trơn | GPU | 10 | 836 / 1.173 | 810 / 1.145 |
| M2 top-10 đoạn kèm mục | GPU | 10 | 2.741 / 4.788 | 2.715 / 4.762 |
| M2 pool 100 đoạn trơn | GPU | 10 | 8.880 / 12.958 | 8.836 / 12.917 |
| M2 pool 100 đoạn kèm mục | GPU | 1 | **167.041 — dừng** (như trên) | |

"Đoạn kèm mục" ở top-10 vượt mức ước 3 s/câu (p95 ~4,8 s) — ghi số thật cho User cân nhắc. Ở pool 100 thì không dùng được
trên GTX 1650 (≈ 2,8 phút một câu).

### 4.2 G4-A — xếp lại top-10 (dev 30, so runtime; Holm trên 5 cho mỗi chỉ số)

| Biến thể | đoạn đúng trong 5 đoạn: chênh [CI 95%], thắng/hòa/thua | MRR@10: chênh [CI], p Holm | p95 cả luồng | Kết luận |
|---|---|---|---:|---|
| M1 đoạn trơn | +0,067 [−0,067; +0,200], 3/26/**1** | **+0,105** [+0,024; +0,201], 0,024 | 1,5 s | **kém hơn** (mất 1 câu — phạm sàn) |
| M1 đoạn kèm mục | −0,033 [−0,167; +0,100], 2/25/**3** | +0,027 [−0,061; +0,120], 1,0 | 4,8 s | **kém hơn** (mất 3 câu) |
| M2 đoạn trơn | −0,033 [−0,167; +0,100], 2/25/**3** | +0,018 [−0,052; +0,095], 1,0 | 1,5 s | **kém hơn** (mất 3 câu) |
| M2 đoạn kèm mục | −0,033 [−0,167; +0,100], 2/25/**3** | +0,035 [−0,051; +0,125], 1,0 | 4,9 s | **kém hơn** (mất 3 câu) |
| luna listwise đoạn trơn | +0,100 [+0,000; +0,233], 3/27/0 | **+0,172** [+0,092; +0,261], <0,001 | 5,2 s (API) | **chưa rõ** |

- Luna cứu đủ 3/3 câu cứu được (trần §1.2), không làm mất câu nào, 0/30 câu lỗi đầu ra. Cận dưới CI của "đoạn đúng trong 5
  đoạn" = 0 đúng như đã tính trước ⇒ theo luật spec (cả hai chỉ số) **không** "tốt hơn"; MRR@10 tăng có CI là **tín hiệu**.
  Chỉ số phụ cùng hướng: `context5_gold_frac` +0,133 [+0,066; +0,206] (10/20/0), nDCG@10 +0,130 [+0,076; +0,193].
- M1 đoạn trơn: MRR@10 và nDCG@10 tăng có CI sau Holm, nhưng đẩy đoạn đúng của 1 câu ra khỏi 5 đoạn ⇒ phạm sàn.
- "Đoạn kèm mục" không giúp với M1 hay M2 (giả thuyết "đơn vị chấm rộng quan trọng hơn chọn model" **không** được ủng hộ ở
  đây; n nhỏ).
- Phần "chỉ natural" (11 câu, tính lại theo file nhãn A cập nhật 25/10 — 9 câu bất đồng User giữ → natural, sha
  `0b65d1c138d2`): đoạn đúng trong 5 đoạn runtime 0,455 / M1 trơn 0,364 / M1 kèm mục 0,364 / M2 trơn 0,273 / M2 kèm mục
  0,364 / luna 0,455; MRR@10 0,345 / 0,538 / 0,413 / 0,402 / 0,455 / 0,591 — cùng hướng với số chính.
- Không biến thể nào "tốt hơn" ⇒ **không chạy xác nhận test cho G4-A** (plan: chỉ phương án tốt hơn).

### 4.3 G4-B — chọn biến thể (ghi TRƯỚC khi chạy, theo `choose_rule` plan §1.4)

- Model: `context5_gold_frac` trên dev 30 — M1 tốt nhất 0,651 (đoạn trơn) > M2 tốt nhất 0,598 (đoạn trơn) ⇒ **M1**. Chênh
  `context5_gold_all` giữa hai model tốt nhất: M1 14/30, M2 11/30 = 3 câu > 1 ⇒ chỉ chạy M1 (không Holm).
- Cách chấm: "đoạn kèm mục" ở pool 100 dừng ở câu đầu (165 s > 60 s; p95 chắc chắn > 30 s) ⇒ **đoạn trơn**.
- Biến thể G4-B duy nhất: **M1 đoạn trơn, pool 100**. Hai so sánh: (1) với runtime; (2) với mốc native pool 100 không
  rerank. Luna pool 100: không làm (plan).

### 4.4 G4-B — M1 đoạn trơn chấm pool 100 rồi lấy top-10 (dev 30; 1 biến thể, không Holm)

| So với | đoạn đúng trong 5 đoạn: chênh [CI], thắng/hòa/thua | MRR@10: chênh [CI], thắng/hòa/thua | top-10 có đủ đoạn đúng | Kết luận |
|---|---|---|---|---|
| (1) runtime | +0,133 [+0,000; +0,300], 5/24/**1** | **+0,140** [+0,054; +0,239], 19/6/5 | +0,200 [+0,067; +0,367], 6/24/0 | **kém hơn** (mất 1 câu — phạm sàn); chỉ số chính chưa vượt 0 |
| (2) native pool 100 không rerank | +0,033 [−0,067; +0,133], 2/27/1 | **+0,112** [+0,021; +0,214], 18/5/7 | +0,100 [−0,033; +0,267], 4/25/1 | **không khác** ở chỉ số chính ⇒ **chưa thấy đóng góp của reranker** ở đoạn đúng đưa model |

- Đối chứng "lợi đến từ pool": native pool 100 không rerank so với runtime: đoạn đúng trong 5 đoạn +0,100 [−0,033;
  +0,233] (4/25/1 — cũng mất 1 câu, câu khác), MRR@10 +0,028 [+0,004; +0,056]. Pool rộng tự nó đã mang lại phần lớn mức
  tăng ở "đoạn đúng trong 5 đoạn"; reranker M1 thêm chủ yếu ở thứ tự (MRR@10, nDCG@10 +0,084 [+0,009; +0,165]).
- Câu mất của G4-B là cùng câu M1 đẩy ra ở G4-A (đoạn đúng vẫn trong top-10, rơi khỏi 5 đoạn đưa model): lỗi lặp lại của M1
  trên câu đó, không phải nhiễu (tất định).
- Latency G4-B p50 / p95 cả luồng 10,6 / 13,8 s (rerank hợp dense 100 ∪ sparse 100 = 112–192 đoạn/câu, trung vị 147 — C23 đếm trên dev 30 — trên GTX 1650) — xa mức 3 s/câu.
- "Chỉ natural" (11 câu, nhãn sha `0b65d1c138d2`): đoạn đúng trong 5 đoạn 0,364 (runtime 0,455, mốc pool 100 0,364), MRR@10
  0,586 (runtime 0,345, mốc pool 100 0,374).
- Không biến thể G4-B nào "tốt hơn" ⇒ **không chạy xác nhận test** (plan).

### 4.5 Kết luận G4 (theo tiêu chí ghi trước)

| Nhánh | Kết luận | Ghi chú |
|---|---|---|
| G4-A M1 / M2 (4 biến thể) | kém hơn | đều làm mất 1–3 câu đoạn đúng khỏi 5 đoạn đưa model |
| G4-A luna listwise | chưa rõ | 3/27/0, MRR@10 +0,17 có CI; trần số học §1.2 chặn chỉ số chính |
| G4-B M1 pool 100 | kém hơn so runtime (mất 1 câu); không khác so mốc pool 100 | lợi chủ yếu do pool rộng; 10–14 s/câu trên GPU |
| "Đoạn kèm mục" | không giúp ở top-10; không chạy được ở pool 100 trên GPU này | ≈ 2,8 phút/câu ở pool 100 |

**Tín hiệu cho 8.2 (A 25/10):** luna listwise tăng MRR@10 +0,17 có CI và không mất câu nào — ghi là tín hiệu, **không** xác
nhận trên test vì chỉ số chính chưa rõ. Muốn trả lời câu này cần bộ có nhiều câu "đoạn đúng trong top-10 nhưng ngoài 5 đoạn"
hơn (dev chỉ có 3/30).

**Lời thường cho User:** Mình thử cho một model "chấm điểm lại" sắp xếp lại các đoạn tìm được, để đoạn có đáp án lên đầu.
Các model chạy trên card đồ họa (M1, M2) sắp thứ tự tốt hơn chút ít, nhưng lại đẩy mất đoạn đúng của 1–3 câu ra khỏi 5
đoạn đưa cho model trả lời, nên theo luật đã đặt trước là **chưa dùng được**. Cho `gpt-6-luna` tự sắp xếp thì không mất câu
nào và thứ tự tốt lên rõ, nhưng với 30 câu thử thì nó chỉ có thể cứu tối đa 3 câu, nên chưa đủ bằng chứng để gọi là tốt hơn
(tốn 0,0088 USD ≈ 220 đồng cho 30 câu, chậm thêm ~3,5 s/câu). Mở rộng vùng tìm (100 ứng viên) tự nó đã giúp nhiều hơn việc
sắp xếp lại. Giới hạn: bộ thử nhỏ (30 câu), mới đo ở bước tìm kiếm, chưa đo câu trả lời.

## 5. Tiền

| Lượt | token vào | token ra | USD |
|---|---:|---:|---:|
| luna pilot 10 câu | 12.770 | 2.719 | 0,0026365 |
| luna 20 câu còn lại | 30.082 | 6.305 | 0,0061607 |
| **Cộng G4 (B17)** | 42.852 | 9.024 | **0,0087972** |

Ước plan: ≈ 0,006 cho 30 câu. Pilot 0,00026 USD/câu (ước 0,0002) — token ra ~270/câu (model tự suy luận), nhiều hơn mức
ước 100. Lượt 20 câu: +54% so với ước plan theo tỉ lệ (0,004), +17% so với ước lại từ pilot (0,0053) ⇒ chạm luật "vượt
50% thì dừng, báo A" theo cách đọc thứ nhất; đã dừng, báo A. **A chấp nhận** (25/10, chiều) và chốt cách đọc từ nay: so với
mức ước lại từ pilot 10 câu của chính lượt đó; thêm trần mỗi lượt đủ ≤ 0,05 USD, tổng B17 ≤ 0,25 USD. Nguyên nhân vượt:
`gpt-6-luna` tự suy luận khi không gửi tham số reasoning, ~270 token ra/câu (dao động 202–541 ở pilot). GPU / CPU: 0 USD.

## 6. Lỗi và giới hạn

- Cỡ mẫu nhỏ (30 dev; G4-A tối đa 3 câu cứu được) — ghi trước ở plan §1.2; kết quả "chưa rõ" của luna là do trần số học.
- Đoạn đúng chỉ phủ câu có nhãn `gold_draft.jsonl`; MRR@10 / nDCG@10 là proxy keyword.
- Latency GPU đo trên GTX 1650 khi không session nào khác dùng GPU; luna đo gồm mạng tới OpenAI.
- Plan §0 ghi "M1/M2 đã có trong HF cache" — sai (đã tải, ghi ở §2).

## 7. Thông số từng lượt (in từ `data/phase_8_1/g4/*.meta.json`)

Chung: retrieval `e5-small-384`, collection `hue_full_corpus_7a2_e5_small_384`; đầu vào `top10` = runtime
`dense_bm25_rrf` pool 30, k 60; `pool100` = `native_hybrid_rrf` pool 100, k 60, hợp hai nhánh dense + sparse; top-k 10;
context `max_context_documents` 5 (settings); subset `data/phase_8_1/g4/subset.json` sha `b9b6e6123ba4`, seed 20261024;
bootstrap 10.000 seed 20261024. M1 `BAAI/bge-reranker-v2-m3` rev `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`, M2
`AITeamVN/Vietnamese_Reranker` rev `f536976248403314225d7fdfdbc87f0e9516a54e`; fp32; `max_length` 1024 (tokenizer
`model_max_length` sau khi nạp = 1024 cả hai); luna `gpt-6-luna`, `max_output_tokens` 2048, `store=False`, structured output
`{order: list[int]}`. Lệnh: `HF_HUB_OFFLINE=1 uv run [--env-file ../.env] python -m experiments.phase_8_1.g4_rerank run
--name <tên> --cases <tập> --input <đầu vào> --reranker <r> --text <cách chấm> --device <thiết bị>` (đúng các cột dưới).
Kết quả: `data/phase_8_1/g4/<tên>.jsonl` + `<tên>.meta.json`; `a_luna_plain.jsonl` = gộp `_pilot` + `_rest`.

| Tên | tập | đầu vào | reranker | thiết bị | max_length | n | cả luồng p50 / p95 ms | retrieval | rerank | giờ chạy | dừng |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| `base_runtime` | dev30 | top10 (pool 30) | none | cpu | — | 30 | 31 / 44 | 29 / 42 | 0 / 0 | 11:43:33–11:43:35 | |
| `base_native100` | dev30 | pool100 (pool 100) | none | cpu | — | 30 | 41 / 45 | 40 / 44 | 0 / 0 | 11:43:49–11:43:52 | |
| `p0_cpu_m1_top10_plain` | pilot_cpu | top10 (pool 30) | m1 plain | cpu | 1024 | 5 | 4886 / 6640 | 26 / 30 | 4855 / 6609 | 11:48:08–11:48:44 | |
| `p0_cpu_m2_top10_plain` | pilot_cpu | top10 (pool 30) | m2 plain | cpu | 1024 | 5 | 4902 / 6386 | 24 / 34 | 4864 / 6360 | 12:00:37–12:01:08 | |
| `p0_gpu_m1_top10_plain` | pilot | top10 (pool 30) | m1 plain | cuda:0 | 1024 | 10 | 848 / 1186 | 36 / 65 | 807 / 1138 | 11:50:25–11:50:41 | |
| `p0_gpu_m1_top10_section` | pilot | top10 (pool 30) | m1 section | cuda:0 | 1024 | 10 | 2731 / 4758 | 27 / 46 | 2699 / 4725 | 11:50:57–11:51:37 | |
| `p0_gpu_m1_pool100_plain` | pilot | pool100 (pool 100) | m1 plain | cuda:0 | 1024 | 10 | 8835 / 12875 | 39 / 49 | 8791 / 12830 | 11:51:51–11:53:45 | |
| `p0_gpu_m1_pool100_section` | pilot | pool100 (pool 100) | m1 section | cuda:0 | 1024 | 1 | 165272 | 46 | 165225 | 11:54:11–11:59:36 | câu đo đầu > 60 s |
| `p0_gpu_m2_top10_plain` | pilot | top10 (pool 30) | m2 plain | cuda:0 | 1024 | 10 | 836 / 1173 | 24 / 29 | 810 / 1145 | 12:01:33–12:01:46 | |
| `p0_gpu_m2_top10_section` | pilot | top10 (pool 30) | m2 section | cuda:0 | 1024 | 10 | 2741 / 4788 | 24 / 27 | 2715 / 4762 | 12:01:59–12:02:38 | |
| `p0_gpu_m2_pool100_plain` | pilot | pool100 (pool 100) | m2 plain | cuda:0 | 1024 | 10 | 8880 / 12958 | 37 / 44 | 8836 / 12917 | 12:02:51–12:04:43 | |
| `p0_gpu_m2_pool100_section` | pilot | pool100 (pool 100) | m2 section | cuda:0 | 1024 | 1 | 167041 | 42 | 166998 | 12:04:56–12:10:33 | câu đo đầu > 60 s |
| `a_m1_plain` | dev30 | top10 (pool 30) | m1 plain | cuda:0 | 1024 | 30 | 949 / 1517 | 26 / 59 | 922 / 1470 | 12:11:07–12:11:42 | |
| `a_m1_section` | dev30 | top10 (pool 30) | m1 section | cuda:0 | 1024 | 30 | 3109 / 4814 | 25 / 30 | 3080 / 4789 | 12:11:56–12:13:44 | |
| `a_m2_plain` | dev30 | top10 (pool 30) | m2 plain | cuda:0 | 1024 | 30 | 962 / 1521 | 26 / 33 | 935 / 1490 | 12:13:58–12:14:32 | |
| `a_m2_section` | dev30 | top10 (pool 30) | m2 section | cuda:0 | 1024 | 30 | 3148 / 4881 | 25 / 32 | 3117 / 4856 | 12:14:45–12:16:34 | |
| `a_luna_plain_pilot` | pilot | top10 (pool 30) | luna | API | — | 10 | 3336 / 5138 | 29 / 41 | 3309 / 5107 | 12:18:43–12:19:20 | |
| `a_luna_plain_rest` | dev30_rest | top10 (pool 30) | luna | API | — | 20 | 3732 / 5175 | 32 / 49 | 3625 / 5144 | 12:19:48–12:21:20 | |
| `b_m1_plain_p100` | dev30 | pool100 (pool 100) | m1 plain | cuda:0 | 1024 | 30 | 10637 / 13824 | 38 / 58 | 10596 / 13778 | 12:23:50–12:29:35 | |

Khâu context: p50 1 ms / p95 ≤ 3 ms ở mọi lượt. Trường `device` trong meta của hai lượt luna ghi `cuda` (giá trị mặc định
của `--device`) nhưng **không dùng** cho luna (gọi API; bảng trên ghi "API") — G4 review m2. Đầu vào `pool100` là hợp
dense 100 ∪ sparse 100 (112–192 đoạn/câu, trung vị 147), không phải 100 đoạn — G4 review m1. Giờ chạy là `started`–`finished` của tiến trình (gồm nạp model + câu khởi
động). Hai lượt "đoạn kèm mục" pool 100 tốn ~5,5 phút mỗi lượt (câu khởi động + câu đo đầu).

## 8. Bàn giao cho người kiểm (C)

Đọc §4.2–4.4 + `data/phase_8_1/g4/*.meta.json` (kiểm GPU, usage). Chạy lại được không tốn tiền: `compare`/`summary` trên
JSONL có sẵn; một lượt GPU bất kỳ (ví dụ `--name rerun_check --cases pilot --input top10 --reranker m1`). Diff code:
`cross_encoder.py`, `g4_rerank.py`; diff `pyproject.toml` / `uv.lock`.
