# Implementation Report: Phase 8.1 G4 phần từ khóa — BM25: tách từ, khử dấu, k RRF, b

Người làm: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 13:41 (`date`) · Việc: B18 · Kế hoạch duyệt:
`phase_8_1_g4_keyword_plan.md` sha `d7e53186b364` (C review ready, A duyệt) · Spec 8.1 §5 G4 dòng "Từ khóa" · 0 USD.

## 1. Phạm vi

Đã làm đủ plan: bước 0 (mốc byte + cổng tương đương), A (3 cách tách từ × 2 cách trộn), E (khử dấu × 2 cách trộn × 2 dạng câu
hỏi), P (k RRF / b). NFC: NOT RUN có lý do (plan §3, G1.4 đã đo). Xác nhận test: NOT RUN — không biến thể nào "tốt hơn"
(plan). Không đổi production, không tạo / ghi collection, không GPU, không API trả phí.

## 2. Thay đổi

- `backend/experiments/phase_8_1/g4_keyword.py` (mới): harness. BM25 trong bộ nhớ (`MemoryBM25`, chỉ mục ngược) với công
  thức chép đúng `fit_sparse_state` / `encode_sparse_document` / `encode_sparse_query`, có tham số tách từ / k1 / b; cộng
  điểm theo thứ tự term tăng dần (= thứ tự chỉ số từ vựng production). Nhánh dense: Qdrant chỉ đọc, chạy một lần mỗi dạng câu
  hỏi, lưu cả `limit=30` (runtime) và `limit=100` (native). Trộn: `reciprocal_rank_fusion`, `rank_positive_bm25` production;
  context: `FullCorpusContextBuilder` + `g4_rerank.packed_chunk_ids`. Lệnh: `dense`, `gate`, `run`, `same-as-g1`, `compare`,
  `analyze` (bảng quyết theo plan §2: Holm chung trên các cặp, sàn, keyword −2,0 điểm %). Từ chối ghi đè file kết quả.
- Tách từ (plan §3): `syllable` (= `scoring.bm25.tokenize`), `bigram`, `codes`, `pyvi` (`pyvi.ViTokenizer`), `deaccent`.

## 3. Cách đã chạy thật

Từ `backend/`, `HF_HUB_OFFLINE=1 uv run python -m experiments.phase_8_1.g4_keyword …`. Kết quả: `data/phase_8_1/g4k/*.jsonl`
(private). Tập: 108 câu dev trong kho (G1 `select_cases("dev")`), phân tích theo số chính (nhãn sha `0b65d1c138d2`): 32 câu
có đoạn đúng (`gold_draft.jsonl` `bab707b9…`), 88 câu keyword.

1. Mốc byte runtime (evaluator) 13:30: `cefb2d1a…` — **PASS**.
2. `dense --form orig` / `--form noaccent` (13:24–13:33; 108 câu × 2 lần hỏi Qdrant mỗi dạng).
3. `gate` (13:25, chạy lại sau sửa dense): xem §4.0.
4. `run --name <tên> --fusion runtime|native --tokenizer <t> [--form noaccent] [--b …] [--rrf-k …]` — 20 lượt, mỗi lượt
   fit 0,5–6,9 s (pyvi chậm nhất), chấm 1–18 ms/câu.
5. `analyze --realism main --pairs <base>:<biến thể> …` cho từng nhóm Holm.
6. Tất định: chạy lại `e_native_na` với tên `check_e_native_na` ⇒ JSONL giống hệt (trừ `bm25_ms`, `config`).

## 4. Kết quả quan sát

### 4.0 Cổng tương đương (plan §1) — PASS

| Kiểm | Kết quả |
|---|---|
| Sparse state trong bộ nhớ vs production (`full_corpus_sparse_state.json`) | 8.459 đoạn, avgdl, từ vựng 5.660, idf **giống hệt** |
| 200 cặp (câu hỏi, đoạn) seed 20261024: điểm trong bộ nhớ vs `compute_sparse_dot_product(encode_…)` | 195/200 giống từng bit; lệch lớn nhất 8,9e-16 |
| R0 (runtime, âm tiết) vs G1 `runtime.jsonl` | 108/108 câu giống top-10, context, MRR |
| N0 (native pool 100, âm tiết) vs G1 `native_p100.jsonl` | 107/108 giống; **câu 162** đổi chỗ hạng 5↔6 |
| Dense `limit=30` lưu vs hỏi lại 10 câu | 10/10 giống; 30 đầu của `limit=100` = `limit=30` ở 107/108 câu |

Câu 162: hai đoạn bằng điểm thật ở float64 (20,1391783752); Qdrant tính sparse bằng float32 (20,13918 / 20,139177) nên phá
hòa khác; tập 100 ứng viên giống hệt ⇒ không phải lỗi công thức. Theo plan: N0 trong bộ nhớ làm baseline native. Lần chạy
gate đầu (13:25) lộ chỗ 30 đầu của `limit=100` ≠ `limit=30` ở 1 câu ⇒ sửa harness lưu cả hai trước khi chạy biến thể nào; ghi
vào plan bản duyệt.

### 4.1 Bảng tổng (32 câu đoạn đúng; 88 câu keyword; in từ JSONL)

| Lượt | đủ trong 5 đoạn | top-10 | dense pool | sparse pool | hợp hai nhánh | MRR@10 | keyword top-10 (%) | chỉ natural: 5 đoạn (n) | BM25 ms/câu |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `r0` | 0.406 | 0.531 | 0.750 | 0.750 | 0.750 | 0.716 | 91.29 | 0.500 (12) | 0.9 |
| `n0` | 0.500 | 0.625 | 0.906 | 0.875 | 0.969 | 0.725 | 93.56 | 0.417 (12) | 9.0 |
| `a_bigram_runtime` | 0.406 | 0.562 | 0.750 | 0.750 | 0.750 | 0.719 | 91.86 | 0.417 (12) | 1.0 |
| `a_codes_runtime` | 0.406 | 0.531 | 0.750 | 0.750 | 0.750 | 0.717 | 91.29 | 0.500 (12) | 1.0 |
| `a_pyvi_runtime` | 0.375 | 0.531 | 0.750 | 0.750 | 0.750 | 0.724 | 91.86 | 0.417 (12) | 1.8 |
| `a_bigram_native` | 0.469 | 0.562 | 0.906 | 0.875 | 0.969 | 0.722 | 92.80 | 0.417 (12) | 11.0 |
| `a_codes_native` | 0.500 | 0.625 | 0.906 | 0.844 | 0.969 | 0.722 | 93.56 | 0.417 (12) | 9.8 |
| `a_pyvi_native` | 0.406 | 0.594 | 0.906 | 0.875 | 0.969 | 0.721 | 93.18 | 0.333 (12) | 8.4 |
| `e_runtime_orig` | 0.344 | 0.562 | 0.750 | 0.750 | 0.750 | 0.713 | 92.23 | 0.333 (12) | 1.0 |
| `e_native_orig` | 0.406 | 0.562 | 0.906 | 0.812 | 0.969 | 0.720 | 92.23 | 0.417 (12) | 13.3 |
| `r0_na` (không dấu) | 0.031 | 0.031 | 0.094 | 0.062 | 0.094 | 0.162 | 29.92 | 0.083 (12) | 1.9 |
| `n0_na` (không dấu) | 0.062 | 0.125 | 0.219 | 0.250 | 0.375 | 0.209 | 39.02 | 0.167 (12) | 5.7 |
| `e_runtime_na` (không dấu) | 0.062 | 0.062 | 0.094 | 0.094 | 0.094 | 0.207 | 32.95 | 0.167 (12) | 1.3 |
| `e_native_na` (không dấu) | 0.156 | 0.344 | 0.219 | 0.812 | 0.812 | 0.414 | 76.33 | 0.333 (12) | 13.6 |
| `p_runtime_b05` | 0.438 | 0.531 | 0.750 | 0.750 | 0.750 | 0.724 | 91.29 | 0.500 (12) | 1.9 |
| `p_runtime_b10` | 0.406 | 0.594 | 0.750 | 0.750 | 0.750 | 0.716 | 91.29 | 0.500 (12) | 1.9 |
| `p_native_k10` | 0.531 | 0.625 | 0.906 | 0.875 | 0.969 | 0.725 | 92.99 | 0.500 (12) | 16.5 |
| `p_native_k30` | 0.500 | 0.625 | 0.906 | 0.875 | 0.969 | 0.725 | 92.99 | 0.417 (12) | 16.3 |
| `p_native_b05` | 0.469 | 0.594 | 0.906 | 0.875 | 0.969 | 0.734 | 92.42 | 0.417 (12) | 18.0 |
| `p_native_b10` | 0.469 | 0.625 | 0.906 | 0.906 | 0.969 | 0.722 | 92.99 | 0.500 (12) | 8.9 |

Ghi chú: ở runtime, cột "dense pool / sparse pool / hợp" đều là dense-30 (BM25 chỉ chấm lại tập đó). Từ vựng: âm tiết 5.660;
bigram 105.999; codes 6.719; pyvi 14.211; khử dấu 3.182.

### 4.2 A — cách tách từ (Holm 6; so với baseline cùng cách trộn)

| Biến thể | đủ trong 5 đoạn: chênh [CI], t/h/t | câu mất | keyword (cận dưới CI ≥ −2,0) | Kết luận |
|---|---|---|---|---|
| bigram · runtime | +0,000 [−0,094; +0,094], 1/30/1 | 1 (169) | đạt | **kém hơn** (sàn) |
| codes · runtime | +0,000 [0; 0], 0/32/0 | 0 | đạt | không khác |
| pyvi · runtime | −0,031 [−0,094; +0,000], 0/31/1 | 1 (169) | đạt | **kém hơn** (sàn) |
| bigram · native | −0,031 [−0,156; +0,094], 2/27/3 | 3 | **tụt** (−2,65) | **kém hơn** |
| codes · native | +0,000 [0; 0], 0/32/0 | 0 | đạt | không khác |
| pyvi · native | −0,094 [−0,219; +0,031], 1/27/4 | 4 | **tụt** (−2,27) | **kém hơn** |

p Holm = 1,0 mọi dòng. Không tách từ nào thắng ⇒ base của P là âm tiết (plan).

### 4.3 E — khử dấu cả kho + câu hỏi

| Phần luật | runtime | native pool 100 |
|---|---|---|
| (1) câu **có dấu**: không kém | **mất 2 câu** (45, 169); −0,062 [−0,156; 0], 0/30/2 | **mất 4 câu**; −0,094 [−0,219; +0,031]; keyword tụt (−3,60) |
| (2) câu **không dấu**: quyết (Holm 2) | +0,031 [0; +0,094], 1/31/0, p Holm 0,73 | +0,094 [0; +0,188], 3/29/0, p Holm 0,18 |
| Kết luận | **kém hơn** (phạm (1)) | **kém hơn** (phạm (1)); (2) chưa rõ |

- Trần ghi trước đúng: runtime không dấu chỉ cứu được tối đa 2 câu (dense-30 không dấu đủ đoạn đúng 3/32) ⇒ chưa rõ.
- **Tín hiệu mạnh ở native với câu không dấu** (chỉ số phụ): sparse pool đủ đoạn đúng 0,250 → **0,812** (18/14/0), top-10
  0,125 → 0,344 (7/25/0), MRR 0,209 → **0,414**, keyword 39,0 → 76,3 %. Chỉ số chính chưa vượt 0 vì nhánh dense (e5) với câu
  không dấu vẫn kém và 5 đoạn đưa model còn ít đoạn đúng.
- ⇒ Đề xuất 8.2 (chưa đo): chỉ dùng chỉ mục khử dấu khi **câu hỏi không có dấu** (phát hiện đơn giản: không ký tự có dấu),
  câu có dấu giữ nguyên BM25 hiện tại — tránh được phần (1). Cần đo riêng, kèm câu không dấu thật của người dùng.

### 4.4 P — tham số (base âm tiết; runtime chỉ b vì G1.3 đã đo k; Holm chung 6)

| Biến thể | đủ trong 5 đoạn: chênh [CI], t/h/t | câu mất | keyword | Kết luận |
|---|---|---|---|---|
| runtime b 0,5 | +0,031 [0; +0,094], 1/31/0 | 0 | đạt | chưa rõ |
| runtime b 1,0 | +0,000 [−0,094; +0,094], 1/30/1 | 1 (29) | đạt | **kém hơn** |
| native k 10 | +0,031 [0; +0,094], 1/31/0 | 0 | **tụt** (−2,27) | chưa rõ |
| native k 30 | +0,000 [0; 0], 0/32/0 | 0 | đạt | không khác |
| native b 0,5 | −0,031 [−0,094; 0], 0/31/1 | 1 (89) | **tụt** (−2,84) | **kém hơn** |
| native b 1,0 | −0,031 [−0,156; +0,062], 1/29/2 | 2 | đạt | **kém hơn** |

Cách đọc Holm của P: plan ghi "Holm 4 (hoặc 2 nếu bỏ k)" cho một base; không có tách từ thắng nên có hai base (runtime,
native) ⇒ B dùng Holm chung 6 (chặt hơn). Với Holm riêng (2 / 4) kết luận không đổi — không dòng nào có cận dưới CI > 0.

### 4.5 Kết luận

| Nhánh | Kết luận |
|---|---|
| A cặp âm tiết / pyvi | kém hơn (mất 1–4 câu; native còn tụt keyword) |
| A nguyên cụm mã | không khác (0 câu đổi ở chỉ số chính) |
| E khử dấu | kém hơn (mất đoạn đúng ở câu có dấu); tín hiệu mạnh cho câu không dấu ở native |
| P k / b | không biến thể nào tốt hơn; b 0,5 runtime và k 10 native chỉ +1 câu |
| NFC câu hỏi | NOT RUN (G1.4 đã đo: NFD→NFC = gốc); đề xuất 8.2: thêm NFC cho câu hỏi |

**Lời thường cho User:** Mình thử nhiều cách cho phần "tìm theo từ khóa": ghép hai âm tiết thành cụm, giữ nguyên các mã số,
tách từ tiếng Việt bằng thư viện `pyvi`, bỏ dấu, và chỉnh hai tham số. Không cách nào tốt hơn cách đang dùng; vài cách còn
làm rơi đoạn đúng của 1–4 câu. Phát hiện đáng giá: khi người dùng gõ **không dấu**, hệ thống hiện tại gần như hỏng (chỉ 1/32
câu còn đủ đoạn đúng), và bản bỏ dấu tìm lại được nhiều hơn hẳn — nhưng lại làm hại câu có dấu, nên nên dùng nó **chỉ khi
câu hỏi không dấu** (việc của 8.2). Không tốn tiền.

## 5. Lỗi và giới hạn

- 32 câu có đoạn đúng: trần cứu được runtime 11 / native 16 (ghi trước) — nhiều kết quả "chưa rõ" là do cỡ mẫu.
- Câu không dấu là bản biến đổi máy từ câu dev (như G1.4), chưa phải câu người dùng thật gõ không dấu.
- MRR / keyword là proxy keyword; đoạn đúng chỉ có cho 40 câu dev.
- Native trong bộ nhớ khác Qdrant ở 1/108 câu (float32 phá hòa) — mọi so sánh native dùng N0 trong bộ nhớ.
- Test: NOT RUN (không có "tốt hơn").

## 6. Bàn giao cho người kiểm (C)

Đọc §4.0–4.5. Chạy lại free: `gate`; `same-as-g1 --name r0 --g1 runtime` và `--name n0 --g1 native_p100`; `analyze` cho ba
nhóm (A: `r0:a_bigram_runtime r0:a_codes_runtime r0:a_pyvi_runtime n0:a_bigram_native n0:a_codes_native n0:a_pyvi_native`;
E: `r0:e_runtime_orig n0:e_native_orig` và `r0_na:e_runtime_na n0_na:e_native_na`; P: `r0:p_runtime_b05 r0:p_runtime_b10
n0:p_native_k10 n0:p_native_k30 n0:p_native_b05 n0:p_native_b10`); một `run` bất kỳ với `--name` mới phải ra cùng JSONL.
Diff: `backend/experiments/phase_8_1/g4_keyword.py` (mới).
