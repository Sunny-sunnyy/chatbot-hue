# C78 — Plan thí nghiệm Qwen3-Embedding-8B (dense thay e5-small) — chưa chạy

Người viết: C (Claude Opus 5.5, `hue-rag-32`) · Date: 11:57 28/10/2026 (`date`) · Việc: C78 (`session_prompt/CURRENT_HANDOFF.md` "### C78", A giao 11:46 28/10/2026). Người review: B.
Plan **chỉ viết**: 0 USD; C không gọi OpenRouter, không tạo collection.
**Chạy cần User duyệt** hai việc: (1) gửi toàn bộ 8.426 đoạn kho (private) ra OpenRouter → Nebius; (2) tạo một collection Qdrant mới. A trình khi User về.
Nhãn: **[N]** nguồn / code nói (`file:dòng`) · **[Đo]** số đo của dự án · **[S]** C suy ra, chưa đo.

**Bản 2** (12:12 28/10/2026) sửa theo review B (`qwen3_8b_plan_review.md`, bản 1 `e04d67e0f034`, changes_requested 0 / 1 / 4):
- **M-1:** bỏ `latency_gate` tự đặt; theo luật (i) spec 8.2 §10.2, 8B luôn thêm 1 lần gọi API ⇒ mọi kết quả "tốt hơn" đều **A trình User kèm số**; báo `dense_ms` so +50 ms và p95 cả
  câu ước so 5 s (§3, §7).
- **m-1:** tập quyết = **dev 40**; số chính 32 là phụ (§3, §7).
- **m-2:** ghi id / ms từng request nhúng câu hỏi; giới hạn cache và nhiễu phía index (§3, §9).
- **m-3:** 429 chờ max(lịch, `Retry-After`); timeout 180 s (§4).
- **m-4:** điều kiện chạy lại sau lỗi (§4).
- Cỡ mẫu: dùng số B tính bằng bootstrap (§3).

## Căn cứ để review

| File | Mục cần đọc | Để kiểm gì |
|---|---|---|
| `backend/embedding/full_corpus.py` | `:41-73` (2 spec dense, `QWEN_QUERY_TASK`), `:76-100` (`prepare_document` / `prepare_query`), `:278-379` (`OpenRouterDenseRunner`: pin Nebius, `data_collection: deny`, batch 64, không retry) | đổi đúng **một** thứ (dense); hợp đồng input của Qwen đúng như code |
| `backend/ingestion/full_corpus_pipeline.py` | `:149-260` (`build_candidate`: `collection_name` / `sparse_state_path` / `record_path`; runner tạo bên trong `:191`; không retry, không resume) | cách dựng collection riêng; chỗ phải thêm tham số (§4) |
| `backend/retrieval/full_corpus.py` + `backend/experiments/phase_8_1/g1_retrieval.py` | service `:637-650` (nhận `collection_name` / `record_path` / `sparse_state_path`); g1 `:181-243` (`run_config` gắn cứng `"e5-small-384"`; tầng `pool_dense` / `top10` / `context5` = context thật, nay 10 đoạn) | chỉ số tầng tìm theo gold v4 tính đúng chỗ |
| `docs/superpowers/specs/2026-10-27-sua-kho-build-lai-index-design.md` §4 Q4 + §5 bước 12; spec 8.2 `…-phase-8-2-apply-winners-design.md` §10.2 (sàn khâu tìm, luật (i)) | — | plan khớp quyết định User; sàn / luật lấy từ spec, không tự đặt mới |

Thêm khi cần: `session_prompt/Project_Status.md` §8 (bẫy OpenRouter); `reports/phase_7a2_gate_2_review_2026_10_24.md` §6 (504, provider trộn).

## 1. Câu hỏi thí nghiệm

**Lớp bài toán:** sau đợt sửa kho, có 16 / 40 câu dev có nhãn mà context chưa phủ đủ fact. 7 câu trong đó thiếu ngay từ 30 ứng viên dense [Đo, §5]. Đây là tầng mà model
dense quyết định. Câu hỏi: model dense lớn (Qwen3-Embedding-8B, 4.096 chiều, gọi qua OpenRouter) có đưa đoạn đúng vào context nhiều hơn e5-small (384 chiều, CPU) không, với
giá nào về tiền và độ trễ?

- [N] User 27/10 (spec sửa kho §4 Q4): "thí nghiệm sau đợt sửa kho — chưa từng đo; collection riêng, đo tầng tìm trước, plan riêng có review; chatbot không đổi tới khi có số".
- [N] Phase 8 dense chỉ e5-small + Qwen3-8B (`Project_Status.md` §5, 24/10); 8B pin Nebius (`full_corpus.py:281`).

## 2. Đổi một thứ

| | Mốc (e5) | Biến thể (8B) |
|---|---|---|
| Dense | `e5-small-384` (local CPU) | `qwen3-embedding-8b-4096` (OpenRouter, `order: [nebius]`, `allow_fallbacks: false`, `data_collection: deny` — `full_corpus.py:281`) |
| Input | `passage:` / `query:` | document nguyên văn; query `Instruct: <QWEN_QUERY_TASK>\nQuery: …` (`:76-100`) — đúng hợp đồng code, **không** chỉnh instruction |
| Kho / chunker | 204 file, 8.426 đoạn (sau sửa kho) | giống |
| BM25 / pool / RRF / context / prompt / model sinh | sparse state runtime `1bae9e0f3c49`; pool 30; RRF k 60; context 10 | giống (sparse state build riêng phải **giống byte** runtime — kiểm tra bất biến) |
| Collection | `hue_full_corpus_7a2_e5_small_384` (runtime, **không đụng**) | mới: `hue_c78_qwen3_8b_4096`; build record + sparse state ở `data/qwen3_8b_2026-10-28/` |

## 3. Bộ câu, nhãn, chỉ số

- Nhãn: **gold v4** (`data/phase_8_1/gold/gold_v4.jsonl` `927bae1bf201`; `GOLD_PATH` trỏ v4 sau B83). 55 câu có nhãn: dev 40 / test 15 (`split.json`).
- **Chọn trên dev, xác nhận trên test** (`run-experiment` §2). Số chính = bỏ nhãn `unnatural` (dev 32 / test 10).
- **Chỉ số quyết** (tầng tìm, tất định với e5): số câu **dev 40** (cả 40 câu có nhãn — nhãn đoạn đúng không phụ thuộc độ tự nhiên, n lớn hơn) có **mọi fact** được context
  phủ (`context5_gold_all` của g1 — tên cũ; giá trị là context thật, 10 đoạn). So theo cặp 8B − e5 trên cùng câu: thắng / hòa / thua + CI 95 % bootstrap (`bootstrap_mean_diff`,
  10.000 vòng, seed `20261024`). Số chính dev 32 (bỏ `unnatural`) báo **phụ**, không quyết.
- **Sàn** (spec 8.2 §10.2 "khâu tìm: 0 câu mất đoạn đúng khỏi context so với mốc"): 0 câu dev có `context_gold_all` = 1 ở e5 mà = 0 ở 8B.
- **Theo dõi:**
  - `pool_dense_gold_all` (30 ứng viên dense) và `top10_gold_all`;
  - `*_gold_frac`; MRR / keyword (`score_retrieval`);
  - số câu đổi top-10;
  - độ trễ nhúng câu hỏi `dense_ms` p50 / p95 (8B gọi mạng mỗi câu) và **chênh theo câu 8B − e5** so với **+50 ms** (luật (i) spec 8.2 §10.2);
  - **p95 cả câu ước** = p95 mốc cả câu hôm nay (4,9 s — bộ "trước" B78, 176 câu tuần tự) + chênh p95 `dense_ms`, so với yêu cầu User **5 s** (đo thật cả câu ở bước 6 nếu chạy);
  - tỉ lệ lỗi gọi câu hỏi (HTTP ≠ 200 / timeout);
  - `providers_seen` (phải chỉ có Nebius).
- **Nhiễu A/A:**
  - e5: tất định (T1 giống byte qua nhiều lần chạy) ⇒ nhiễu 0;
  - 8B: nhúng 176 câu hỏi **hai lần** (cùng index) ⇒ đếm câu đổi top-10 và đổi `context_gold_all` giữa hai lượt, cos trung bình / nhỏ nhất giữa hai vector cùng câu. Ghi **trước**
    khi so với e5. Mỗi request ghi `id` (nếu có trong response) + ms + provider: nếu lượt 2 nhanh bất thường so với lượt 1 **và** vector giống byte ⇒ ghi "có thể trả từ cache",
    A/A này là **cận dưới** của nhiễu.
  - Chỉ đo nhiễu **phía câu hỏi** trên một index; nhiễu **phía index** (build lại cho vector đoạn khác) không đo — chỉ có pilot cos 20 đoạn (§6 bước 3) làm bằng chứng một phần.
- **Cỡ mẫu** [Đo + S]:
  - dev: 16 câu có thể đổi theo hướng tốt (context thiếu), 24 câu có thể tụt (sàn);
  - "CI 95 % > 0" trên 40 cặp nhị phân (B tính bằng `bootstrap_mean_diff`, review C78 §2): **4 thắng / 0 thua**, **7 / 1**, hoặc **≥ 9 / 2**; 3 / 0 và 5 / 1 thì CI chạm 0;
  - trần thắng: 7 câu thiếu ngay ở pool dense (8B sửa trực tiếp được) + 9 câu đủ ở pool nhưng thiếu ở context (8B chỉ tác động gián tiếp qua RRF);
  - 7 câu thiếu từ pool dense là phần 8B có thể sửa trực tiếp ⇒ **"chưa rõ" là kết quả hợp lệ** (ghi trước);
  - test 15 câu chỉ để "không làm hỏng" (sàn + không tụt quá A/A).

## 4. Code cần thêm (chưa viết; viết sau khi plan duyệt; B review code trước lượt thật)

Theo `practical-project-coding` "ranh giới theo khâu": tham số mặc định = hành vi đang chạy; thêm tham số kèm kiểm "runtime không đổi" (T1 `23c58c47635d` giống byte + test).

1. **`build_candidate(..., dense_runner=None)`** (`full_corpus_pipeline.py:149`) — `None` thì giữ `create_dense_runner(spec)` như hôm nay. Lý do: runner OpenRouter hiện **không
   thử lại** (`full_corpus.py:310`) và build không resume. 7A2 gặp 504 khi pin Nebius ([N] `Project_Status.md` §8), mà quyết định 24/10 yêu cầu "thiết kế cách gọi chịu
   504 / 429 (batch, thử lại)". Harness truyền vào một runner bọc (chỉ trong `backend/experiments/`):
   - **cache từng batch** ra `data/qwen3_8b_2026-10-28/emb/batch_NNN.npy` (đã có thì đọc lại, không gọi lại — chạy lại sau lỗi không trả tiền hai lần);
   - **thử lại có giới hạn:** chỉ với HTTP 429 / 5xx / timeout, tối đa 3 lần, chờ 10 / 30 / 90 s — với 429 có header `Retry-After` thì chờ **max(lịch, `Retry-After`)**; mỗi lần thử
     ghi một dòng log (batch, mã HTTP, ms, provider) vào `emb/attempts.jsonl`; hết 3 lần ⇒ raise (build dừng, cache giữ);
   - không đổi input / batch 64 / pin provider / timeout 180 s của runner (`full_corpus.py:323-326`).
   - **Vì sao chạy lại sau lỗi được** (đọc `full_corpus_pipeline.py:149-260`): kiểm đích (chưa có collection / record) ⇒ ghi sparse state ⇒ nhúng toàn kho ⇒ **chỉ sau đó** mới tạo
     collection + upsert ⇒ record. Lỗi lúc nhúng ⇒ chưa có collection; sparse state đã ghi giống byte nên lần chạy lại qua `_write_or_check_sparse_state`; vector đã có trong
     cache không gọi lại. Lỗi **sau** khi đã tạo collection (upsert / kiểm sau upsert) ⇒ phải xóa collection thử (**User duyệt**) rồi mới chạy lại.
2. **`g1_retrieval run`** thêm `--candidate`, `--collection`, `--record`, `--sparse-state` (mặc định = runtime e5). Truyền thẳng vào `build_full_corpus_retrieval_service`
   (đã nhận sẵn `:644-646`). Câu hỏi 8B **không** thử lại: lỗi ⇒ dòng lỗi, chạy lại đúng câu đó một lần (đo đúng tỉ lệ lỗi mà runtime sẽ gặp). Một câu hỏi treo có thể tới
   180 s (timeout runner) ⇒ đếm là "timeout" trong tỉ lệ lỗi gọi.
3. Không sửa runtime API, `settings.yaml`, `OpenRouterDenseRunner`.

## 5. Mốc đã đo (để biết còn chỗ cải thiện) — [Đo] C, 11:5x 28/10, in-memory, không ghi file

Index sau sửa kho (T1 `23c58c47635d`), e5, gold v4, gọi `g1_retrieval.run_config` với tham số mặc định:

| Nhóm | n có nhãn | context đủ fact | top-10 đủ | pool dense 30 đủ | context thiếu | thiếu cả ở pool dense |
|---|---:|---:|---:|---:|---:|---:|
| dev | 40 | 24 | 24 | 33 | 16 | 7 |
| dev số chính | 32 | 19 | 19 | 26 | 13 | 6 |
| test | 15 | 9 | 9 | 11 | 6 | 4 |
| test số chính | 10 | 7 | 7 | 8 | 3 | 2 |

Mốc chính thức sẽ chạy lại bằng harness (§6 bước 2) và lưu file. Bảng này chỉ để ước cỡ mẫu.

## 6. Cách chạy (sau khi User duyệt + A duyệt sha plan + B review code)

1. **Preflight (free):**
   - `git` HEAD;
   - T1 runtime = `23c58c47635d`;
   - Qdrant đúng 1 collection runtime, chưa có `hue_c78_*`;
   - `OPENROUTER_API_KEY` có (`uv run --env-file ../.env`, không in);
   - gold v4 sha; số đoạn 8.426.
2. **Mốc e5 (free):** `g1_retrieval run --name c78_e5_dev --group dev` và `--group test` ⇒ phải trùng bảng §5. Lệch ⇒ dừng, tìm nguyên nhân.
3. **Pilot nhúng (có phí, rất nhỏ):**
   - 2 batch đầu (128 đoạn) qua runner bọc ⇒ đo ms / batch, provider, số token usage;
   - ước lại tiền + thời gian cả kho;
   - **kiểm lại hiện tượng 7A2:** nhúng lại 20 đoạn đầu lần hai ⇒ cos ≥ 0,999 với lần một (`Project_Status.md` §8: không pin thì cos ~0,996).
4. **Build** `build_candidate("qwen3-embedding-8b-4096", collection_name="hue_c78_qwen3_8b_4096", sparse_state_path=…/sparse_state.json, record_path=…/record.json, dense_runner=<bọc>)`:
   - 132 batch;
   - kiểm sau build: `verification` (8.426 / 8.426), `providers_seen == ["nebius"]`, sparse state **giống byte** `1bae9e0f3c49`.
5. **Tầng tìm 8B:**
   - `g1_retrieval run --candidate qwen3-embedding-8b-4096 --collection hue_c78_qwen3_8b_4096 … --name c78_8b_dev` (và `_dev_aa` lần hai cho A/A), rồi test;
   - `compare --a c78_e5_dev --b c78_8b_dev --metrics context5_gold_all top10_gold_all pool_dense_gold_all mrr` (+ `--realism main`).
6. **Khâu trả lời — chỉ khi tầng tìm "tốt hơn" theo §7** (lần có phí thứ hai, A duyệt riêng sau khi thấy số tầng tìm):
   - 176 câu qua `answer_case` với service 8B;
   - so với bộ "sau" của B83 (e5, cùng kho, context 10) — chấm **cùng lượt mù** (chấm lại câu trả lời e5 trong cùng lô; `run-experiment` §3.6);
   - luật (i) spec 8.2 §10.2.
7. **Dọn:** xóa `hue_c78_qwen3_8b_4096` + `data/qwen3_8b_2026-10-28/emb/` chỉ khi User duyệt (`Project_Status.md` §6); report ghi số point / dung lượng trước khi xóa.

## 7. Tiêu chí ghi trước

```yaml
experiment_id: c78_qwen3_8b_dense
baseline: "main HEAD lúc chạy; index runtime e5 sau sửa kho (T1 23c58c47635d); gold v4 927bae1bf201"
changed_variable: "dense model e5-small-384 → qwen3-embedding-8b-4096 (OpenRouter, pin Nebius)"
unchanged: [kho 204 file / 8.426 đoạn, chunker, BM25 + sparse state, pool 30, RRF k 60, context 10, prompt, gpt-6-luna, validator, judge]
data: {split: knowledge-base-hue/evaluation/phase_8_1/split.json, decide: "dev 40 (mọi câu có nhãn)", secondary: "dev số chính 32", confirm: "test 15 (số chính 10)"}
metrics:
  - {name: context_gold_all (dev 40), fn: "g1 context5_gold_all, cặp 8B − e5", better: up, role: decide, rule: "thắng ròng, CI 95 % > 0, vượt A/A 8B"}
  - {name: mất đoạn đúng khỏi context (dev + test), fn: "e5 = 1, 8B = 0", role: floor, floor: 0, src: "spec 8.2 §10.2 sàn khâu tìm"}
  - {name: pool_dense_gold_all, top10_gold_all, gold_frac, MRR, keyword, role: watch}
  - {name: dense_ms p50 / p95 (176 câu hỏi) + chênh theo câu 8B − e5, role: watch, note: "so +50 ms (luật (i) spec 8.2 §10.2)"}
  - {name: p95 cả câu ước, fn: "4,9 s (mốc bộ trước B78) + chênh p95 dense_ms", role: watch, note: "so 5 s (User 28/10); đo thật ở bước 6 nếu chạy"}
  - {name: lỗi gọi câu hỏi, fn: "HTTP ≠ 200 / timeout trên 176 × 2 lượt", role: watch, report_if: "> 0"}
  - {name: A/A 8B, fn: "câu đổi top-10 / đổi context_gold_all giữa 2 lượt nhúng câu hỏi; cos min", role: noise}
  - {name: USD (nhúng kho + câu hỏi), role: watch}
interpretation:
  better: "CI > 0, 0 câu mất, test không tụt quá A/A + 0 câu ⇒ 'tầng tìm tốt hơn' ⇒ đề xuất bước 6 (khâu trả lời) — A duyệt riêng"
  same: "CI chứa 0 ⇒ 'không khác' — dừng ở tầng tìm, ghi hồ sơ, không chạy khâu trả lời"
  worse: "vi phạm sàn hoặc thua ròng ⇒ 'kém hơn' — dừng"
  rule_i: "8B luôn thêm 1 lần gọi API / câu (vi phạm điều kiện 'không thêm lần gọi API' của luật (i) spec 8.2 §10.2) ⇒ mọi kết quả 'tốt hơn' đều A TRÌNH USER KÈM SỐ, không tự nhận: chênh dense_ms so +50 ms, p95 cả câu ước so 5 s, tỉ lệ lỗi gọi, USD / câu, và chính sách dữ liệu (mọi câu hỏi gửi ra ngoài)"
result: null
conclusion: null
```

## 8. Tiền, thời gian, dừng

- **Giá** (WebFetch 11:4x 28/10/2026, `https://openrouter.ai/api/v1/embeddings/models` + `…/models/qwen/qwen3-embedding-8b/endpoints`):
  - `qwen/qwen3-embedding-8b` **0,01 USD / 1M token vào** (prompt `0.00000001` / token), 0 cho đầu ra;
  - Nebius cùng giá, context 40.960, uptime 1 ngày 99,44 %;
  - DeepInfra cùng giá; SiliconFlow (fp8) 0,04 USD / 1M;
  - trang endpoint **không** ghi chính sách dữ liệu — `data_collection: deny` là yêu cầu routing của code (`full_corpus.py:281`), không phải cam kết thấy được trên trang ⇒ ghi
    là giới hạn khi trình User.
- **Cỡ kho:** 8.426 đoạn, 2.648.045 ký tự, **752.077 token theo tokenizer e5** [Đo, 11:5x]. Tokenizer Qwen không có trong cache ⇒ [S] ước 0,75–1,5 M token.
- **Ước tiền:**
  - nhúng kho ≈ 0,0075–0,015 USD;
  - câu hỏi 176 × 2 lượt × ~70 token ≈ 0,0003;
  - pilot + nhúng lại 20 đoạn ≈ 0,002;
  - thử lại (cận trên +50 %);
  - ⇒ **tầng tìm ≈ 0,01–0,03 USD**;
  - khâu trả lời (bước 6, nếu có): 176 × ~0,0002 ≈ 0,037 USD.
- **Trần:** tầng tìm **0,05 USD**; cả thí nghiệm **0,10 USD** (trong 1 USD phiên). Vượt ⇒ dừng.
- **Thời gian:**
  - nhúng 7A2 pin Nebius 10–30 s / batch ⇒ 132 batch ≈ 22–66 phút [N `Project_Status.md` §8];
  - tầng tìm 2 × 176 câu ≈ vài phút (mạng);
  - không chạy cùng lượt trả phí khác (đo độ trễ).
- **Dừng + báo A:**
  - pilot cos < 0,999 hoặc `providers_seen` ≠ Nebius;
  - 1 batch hết 3 lần thử;
  - ước sau pilot > 1,5 × ước;
  - sparse state khác byte runtime;
  - mốc e5 lệch bảng §5;
  - lỗi gọi câu hỏi > 5 % một lượt.

## 9. Rủi ro và giới hạn

- **Dữ liệu ra ngoài:** toàn bộ kho + mọi câu hỏi đánh giá gửi qua OpenRouter → Nebius ⇒ User duyệt (spec sửa kho §7: "Không OpenRouter" trong đợt sửa kho; thí nghiệm này
  là việc riêng). Nếu sau này đưa vào chatbot, **mọi câu hỏi người dùng** cũng phải gửi ra ngoài — đổi chính sách dữ liệu, User quyết riêng.
- **Hai lớp không tất định:** provider (đã pin) và chính API embedding ⇒ đo A/A, không giả định 0.
- **Nhãn chỉ 55 câu** (dev 40) ⇒ chỉ thấy hiệu ứng lớn. Câu không nhãn chỉ có keyword (theo dõi).
- **Dung lượng:** 8.426 × 4.096 × 4 byte ≈ 138 MB vector + HNSW, trên máy User; xóa khi xong (User duyệt).
- **Không đo:**
  - 8B ở khâu rerank;
  - nhúng câu hỏi ở chế độ khác instruction;
  - DeepInfra / SiliconFlow (pin Nebius theo quyết định 24/10);
  - e5-base / model local lớn hơn.
  Đều ghi `NOT RUN` trong report.

## 10. Câu hỏi cho A khi duyệt

1. Đồng ý thêm `dense_runner` vào `build_candidate` (mặc định giữ nguyên) để chịu 504 / 429 + cache batch, hay giữ code và chấp nhận build có thể hỏng giữa chừng (chạy lại từ
   đầu, trả tiền lại)? C khuyên thêm: tiền nhỏ, nhưng 7A2 đã hỏng đúng chỗ này.
2. Người viết harness: C; B review code + kết quả.

(Bản 1 câu 2 "ngưỡng `latency_gate`" bỏ — thay bằng luật (i) spec 8.2, M-1 review B.)

## Sửa đổi 30/10

Người viết: B (`hue-rag-24`), 11:28 30/10/2026 (`date`); bản A duyệt trước đó `52555da95828`. Quyết định A 11:3x 30/10/2026 (B92). **Không sửa các mục trên; không đổi tiêu
chí §7.** C review phần này ⇒ A duyệt sha mới; phải xong **trước** mọi lượt có phí của 8B.

1. **Mốc e5 chính thức = mốc trên kho sau đợt 2.** Bảng §5 là số trên kho đợt 1 (B tính lại 30/10 trên kho đợt 1 bằng `g1_retrieval.run_config` mặc định: dev 40 câu có nhãn,
   context đủ 24, top-10 24, pool dense 33, thiếu ở pool dense 7 — khớp §5). 8B chạy sau đợt 2 (kho đổi; có thể có nhãn v5) ⇒ §6 bước 2 thay bằng: trên kho đợt 2, với nhãn
   `GOLD_PATH` lúc chạy, chạy mốc e5 `--group dev` và `--group test` **hai lần** (tên thứ hai thêm `_rerun`); hai lần phải giống từng dòng trừ `dense_ms` (e5 tất định). Điều kiện
   này **thay** "mốc e5 lệch bảng §5" ở §6 bước 2 và §8. Ghi bảng như §5 cho mốc mới vào report trước pilot.
2. **Cỡ mẫu tính lại trước pilot** (ghi vào report, trước lượt có phí đầu tiên): n dev có nhãn; số câu context thiếu (trần thắng); trong đó số câu thiếu ngay ở pool dense; số
   câu có thể tụt (context đủ). Nếu n ≠ 40 ⇒ tính lại các cặp thắng / thua nhỏ nhất cho "CI 95 % > 0" bằng `bootstrap_mean_diff` (10.000 vòng, seed `20261024`) như cách ở §3.
   Nếu số câu context thiếu < số thắng nhỏ nhất cần (khi 0 thua) ⇒ thí nghiệm không thể ra "tốt hơn" ở cỡ mẫu này ⇒ dừng, báo A (A trình User có chạy hay không).
3. **Cùng một file nhãn** cho mốc e5 và 8B (sha ghi trong report). Nhãn đổi giữa chừng ⇒ chạy lại mốc e5.
4. **Code:** harness `backend/experiments/phase_8_2/qwen3_8b.py`, nhánh `b92-qwen3-harness` — B viết, C review (đổi người so với §10.2, A 30/10). Lệch §4.2 A duyệt:
   `build_full_corpus_retrieval_service(..., dense_runner=None)` để lấy vector câu hỏi (A/A §3) + log từng request. Provider kiểm bằng hằng `OPENROUTER_EXPECTED_PROVIDER`
   (giá trị thật `"Nebius"`; §6 bước 4 viết `"nebius"`). Report `qwen3_8b_harness_implementation.md`.
5. Không đổi: chỉ số quyết, sàn, theo dõi (§3), YAML (§7), tiền / trần / các điều kiện dừng khác (§8).
6. **Đường lỗi câu hỏi** (review C88 M-1, A quyết 11:3x 30/10/2026; thêm 11:33 30/10/2026): thay §4.2 "không thử lại; lỗi ⇒ dòng lỗi" — runner tự thử lại **1 lần** (chờ 10 s,
   hoặc `Retry-After`); câu lỗi cả hai lần ⇒ lượt dừng ⇒ **chạy lại cả lượt** (tên mới). `dense_ms` p50 / p95 báo **hai cách**: mọi câu (gồm câu thử lại — sát trải nghiệm thật) và
   chỉ câu gọi đúng một lần, kèm số câu thử lại và số dòng log ≠ 200 (`qwen3_8b latency --name …`, cũng in trong `retrieve`). Luật dừng §8 "lỗi gọi câu hỏi > 5 % một lượt"
   thay bằng **"câu phải thử lại > 5 % một lượt ⇒ dừng, báo A"**.
