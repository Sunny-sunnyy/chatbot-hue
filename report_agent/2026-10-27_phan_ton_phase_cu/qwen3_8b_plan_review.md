# Review: plan C78 — thí nghiệm Qwen3-Embedding-8B (dense thay e5-small)

Decision: **changes_requested** (0 blocker / 1 major / 4 minor)
Người kiểm: B (Claude Opus 5.5, `hue-rag-ac`) · Date: 12:06 28/10/2026 (`date`) · Việc: B84 (A giao 28/10). Bản `qwen3_8b_plan.md` sha `e04d67e0f034` (B tính từ file). 0 USD, chỉ đọc.
Chỉ dựa gói "Căn cứ để review" (WORKFLOW §9.1); không đọc STATUS_C / tin của C.

## 1. Phạm vi đã review

Plan 188 dòng. Đối chiếu trên `main`:
- `backend/embedding/full_corpus.py`: `:41-73` (spec dense), `:76-100` (`prepare_document` / `prepare_query`); `:281` `OPENROUTER_PROVIDER_ROUTING = {"order": ["nebius"], "allow_fallbacks": False,
  "data_collection": "deny"}`; `OpenRouterDenseRunner` (`:309-379`): "lỗi thì raise, không retry/fallback", `httpx.Client(timeout=180)`, batch `spec.batch_size`, `providers_seen`.
- `backend/ingestion/full_corpus_pipeline.py:149-260`: thứ tự **kiểm đích ⇒ ghi / kiểm sparse state ⇒ `create_dense_runner` + nhúng toàn kho ⇒ tạo collection + upsert ⇒ record**.
- `backend/retrieval/full_corpus.py:637-650`: service nhận `collection_name`, `record_path`, `sparse_state_path`. `backend/experiments/phase_8_1/g1_retrieval.py:184`:
  `run_config` gắn cứng `"e5-small-384"` — đúng như plan nói (cần thêm `--candidate` …).
- Spec sửa kho §4 Q4 + §5 bước 12; spec 8.2 §10.2 (sàn khâu tìm, luật (i)).

**Đạt:** đổi đúng một thứ (dense); collection / record / sparse state riêng, runtime không đụng; hợp đồng input Qwen theo code, không chỉnh instruction; sàn "0 câu mất
đoạn đúng khỏi context" lấy đúng spec 8.2 §10.2; chọn dev / xác nhận test; "chưa rõ" ghi trước là kết quả hợp lệ; dừng khi pilot cos < 0,999 / provider ≠ Nebius / sparse
state khác byte; dọn chỉ khi User duyệt; nêu đúng hai việc cần User duyệt (dữ liệu ra ngoài + collection mới).

## 2. Trả lời 5 điểm A hỏi

1. **Chịu 504 / 429 — đủ, kèm 1 minor (m-3).** Cache từng batch + thử lại có giới hạn (429 / 5xx / timeout, 3 lần, 10 / 30 / 90 s, log từng lần) giải quyết đúng chỗ 7A2 hỏng.
   B kiểm thứ tự ghi của `build_candidate`: lỗi giữa lúc nhúng thì **chưa có collection** (tạo sau khi nhúng xong); sparse state đã ghi giống byte nên lần chạy lại qua
   `_write_or_check_sparse_state` ⇒ chạy lại sau lỗi + đọc cache **đứng được** (plan nên ghi rõ điều này). Câu hỏi lúc tìm không thử lại — đúng để đo tỉ lệ lỗi runtime.
2. **A/A 8B bằng nhúng câu hỏi 2 lần — đúng một nửa (m-2).** Đo được nhiễu **phía câu hỏi** trên cùng index; đó chính là nhiễu khi so e5 ↔ 8B trên một index cố định. Không đo
   nhiễu **phía index** (build lại cho vector đoạn khác) — pilot "nhúng lại 20 đoạn, cos ≥ 0,999" chỉ phủ một phần. Thêm: hai request giống hệt có thể được trả từ cache phía
   OpenRouter / provider ⇒ A/A = 0 giả.
3. **`latency_gate` (p95 nhúng câu hỏi > 1 s ⇒ trình User) — xem M-1:** lệch luật (i) spec 8.2 và lỏng so với yêu cầu p95 ≤ 5 s cả câu.
4. **Cỡ mẫu — đủ cho hiệu ứng lớn, "chưa rõ" dễ xảy ra.** B tính bằng `bootstrap_mean_diff` (10.000, seed 20261024) trên 40 cặp: CI 95 % > 0 khi **4 thắng / 0 thua** (CI
   [0,025; 0,2]), **7 / 1**, hoặc ≥ 9 / 2; 3 / 0 và 5 / 1 thì CI chạm 0. Plan ghi "≥ 5–6 thắng ròng, 0 thua" — chặt hơn thực tế một chút, không sai hướng. Trần: 7 câu dev thiếu ngay
   ở pool dense (8B sửa trực tiếp được) + 9 câu đủ ở pool mà thiếu ở context (8B chỉ tác động gián tiếp qua RRF) ⇒ cần gần như toàn thắng. Bộ quyết là dev 40 hay số chính 32 chưa
   rõ (m-1).
5. **Câu §10:** (1) đồng ý thêm `dense_runner=None` vào `build_candidate` (mặc định = hôm nay; kèm T1 giống byte + test) — rẻ, đúng chỗ đã hỏng; (2) thay bằng M-1;
   (3) đồng ý C viết harness, B review code + kết quả.

## 3. Findings

### M-1 (major) — `latency_gate` là ngưỡng tự đặt, lệch luật (i) spec 8.2 và lỏng so với yêu cầu phi chức năng User

- **Vị trí:** §7 `interpretation.latency_gate` (`p95 > 1.000 ms` hoặc lỗi > 1 % ⇒ "tốt hơn nhưng vướng vận hành"); §10 câu 2.
- **Yêu cầu:** plan tự ghi (Căn cứ dòng 4) "sàn / luật lấy từ spec, không tự đặt mới". Spec 8.2 §10.2 luật (i): biến thể nâng chất lượng phải **"khâu tìm ≤ +50 ms / câu" và
  "không thêm lần gọi API / dịch vụ nào"**; vượt ⇒ **"A trình User kèm số, không tự nhận"**. Yêu cầu User 28/10: p95 ≤ 5 s **cả câu**.
- **Bằng chứng:** 8B **luôn** thêm một lần gọi mạng mỗi câu hỏi ⇒ theo luật (i) mọi kết quả "tốt hơn" đều thành "trình User", bất kể p95 nhúng là 0,3 s hay 1 s. Mốc cả câu hôm
  nay đã sát trần: bộ "trước" / "sau" sửa kho (176 câu, tuần tự, harness) p95 **4,9 s** (`check_truoc.json`); 9,8 s ở lượt "sau" là lúc provider chậm. Cộng +1 s nhúng câu
  hỏi ⇒ ~5,9 s > 5 s, nhưng gate 1 s vẫn cho qua.
- **Tác động:** kết luận "tốt hơn" không ghi rõ cái giá so với yêu cầu User; ngưỡng mới không có nguồn.
- **Đóng:** thay `latency_gate` bằng: (a) "8B thêm 1 lần gọi API / câu ⇒ theo luật (i) mọi kết quả 'tốt hơn' đều **A trình User kèm số**"; (b) báo
  `dense_ms` 8B − e5 (p50 / p95, theo câu) so với **+50 ms** của luật (i); (c) báo **p95 cả câu ước** = p95 mốc hôm nay + chênh p95 nhúng (hoặc đo cả câu ở bước 6) so với
  **5 s**. Tỉ lệ lỗi gọi: giữ làm watch, nêu số.

### m-1 — bộ quyết chưa định đúng một tập

- `metrics` / `data`: "decide: dev (40 có nhãn; số chính 32)". `run-experiment` §1 mục 3 cần một tập n cụ thể. **Đóng:** ghi một tập quyết (đề xuất: dev 40 — vì nhãn
  đoạn đúng không phụ thuộc độ tự nhiên, n lớn hơn), tập kia là phụ.

### m-2 — A/A 8B: thiếu kiểm cache và nhiễu phía index

- **Đóng:** (a) ghi `id` / `ms` từng request nhúng câu hỏi ở hai lượt; nếu lượt 2 nhanh bất thường (≪ lượt 1) và vector giống byte ⇒ ghi "có thể cache", A/A này là cận dưới; (b) ghi
  giới hạn "không đo nhiễu phía index (chỉ một lần build)", và nêu pilot cos 20 đoạn là bằng chứng một phần.

### m-3 — 429: tôn trọng `Retry-After`; timeout 180 s

- Runner dùng `httpx.Client(timeout=180)` cho cả nhúng kho lẫn câu hỏi. Thử lại 10 / 30 / 90 s cố định có thể ngắn hơn `Retry-After` mà OpenRouter trả cho 429. **Đóng:** khi
  có `Retry-After` thì chờ max(lịch, `Retry-After`); ghi rằng một câu hỏi treo có thể tới 180 s (đếm là timeout trong "lỗi gọi").

### m-4 — ghi rõ điều kiện chạy lại sau lỗi

- Plan nói "cache giữ" nhưng không nói vì sao chạy lại không vướng "không ghi đè". **Đóng:** thêm một dòng §4: collection chỉ tạo sau khi nhúng xong (`full_corpus_pipeline.py`
  thứ tự ở §1 review này), sparse state ghi trước nhưng giống byte ⇒ chạy lại qua `_write_or_check_sparse_state`; nếu lỗi **sau** khi tạo collection thì phải xóa collection
  thử (User duyệt) trước khi chạy lại.

## 4. Giới hạn

- Không WebFetch lại giá OpenRouter (C ghi 0,01 USD / 1M token, WebFetch 11:4x) — tiền ước rất nhỏ so với trần.
- Không kiểm bảng mốc §5 bằng chạy lại (C ghi là số in-memory; plan bước 2 chạy lại chính thức).

## 5. Decision

`changes_requested`: C sửa M-1 (bắt buộc), minor nên gộp; báo sha mới ⇒ B kiểm phần sửa ⇒ A duyệt sha ⇒ A trình User (dữ liệu ra ngoài + collection mới).

## Vòng 2 — kiểm phần sửa (bản 2, sha `52555da95828`)

Decision vòng 2: **ready_for_user_confirmation** (0 / 0 / 0). Date: 12:13 28/10/2026 (`date`). B tính lại sha từ file: `52555da95828` (208 dòng). Đọc `git diff` bản 1 (`e04d67e0f034`, đã commit) ↔ bản 2.

| Finding | Bản 2 | Kết quả |
|---|---|---|
| M-1 `latency_gate` tự đặt | bỏ; `rule_i` §7: 8B luôn thêm 1 lần gọi API ⇒ mọi "tốt hơn" **A trình User kèm số**; §3 + §7 báo chênh `dense_ms` theo câu 8B − e5 so **+50 ms** và **p95 cả câu ước** (4,9 s mốc bộ "trước" + chênh p95) so **5 s**; lỗi gọi giữ watch; §10 câu 2 bỏ có ghi lý do | **đóng** |
| m-1 tập quyết | `decide: dev 40`, `secondary: dev số chính 32`, `confirm: test 15` — nêu lý do (nhãn đoạn đúng không phụ thuộc độ tự nhiên) | **đóng** |
| m-2 A/A + cache | ghi `id` / ms / provider từng request; lượt 2 nhanh bất thường **và** vector giống byte ⇒ "có thể cache", A/A là cận dưới; giới hạn nhiễu phía index + pilot cos 20 đoạn là bằng chứng một phần | **đóng** |
| m-3 429 / timeout | chờ max(lịch, `Retry-After`); timeout 180 s (`full_corpus.py:323-326` — B kiểm: `httpx.Client(timeout=180)` ở `:325`) đếm là timeout trong tỉ lệ lỗi | **đóng** |
| m-4 chạy lại sau lỗi | §4 ghi đúng thứ tự `build_candidate` (khớp review §1) và trường hợp lỗi sau khi đã tạo collection ⇒ xóa (User duyệt) rồi mới chạy lại | **đóng** |
| (cỡ mẫu) | thay bằng số bootstrap 4 / 0, 7 / 1, ≥ 9 / 2 + trần thắng 7 + 9 | đúng số review §2 |

**Kết luận vòng 2:** bản `52555da95828` sẵn để A duyệt sha; chạy vẫn cần User duyệt (gửi toàn bộ kho + câu hỏi đánh giá ra OpenRouter → Nebius; tạo collection
`hue_c78_qwen3_8b_4096`). B review code harness trước lượt thật (§4).
