# Kế hoạch G2 + G4 — sinh câu trả lời và xếp hạng lại (tiêu chí ghi trước)

Người viết: B (Claude Opus 5.5) · bản nháp 2026-10-24 22:44 (B16, terminal `hue-rag-b0`, sha `c29b547b7417`) · **bản sửa
2026-10-25 11:26 +0700**, vòng sửa 1 lúc 11:36 (B17 bước 1, terminal `hue-rag-3f`; giờ lấy bằng `date`) · Trạng thái: **chờ C review + A
duyệt; chưa chạy GPU / paid** · Spec 8.1 §5 G2, G4 (gồm sửa đổi User 25/10), §7, §8; skill `run-experiment`. Đầu vào:
kết quả G1 (`phase_8_1_g1_implementation.md` §4, §6, §7); `report_agent/2026-10-25_cai_tien_cach_lam/de_xuat_cho_du_an.md`
mục 1–5, 8.

## Thay đổi so với bản nháp `c29b547b7417` (theo mục B17 trong `CURRENT_HANDOFF.md`, A ghi 11:22)

- G4-B được User duyệt (spec §5 G4 sửa đổi 25/10): bỏ điều kiện "chỉ khi sửa spec"; G4-B không chờ G4-A thắng (§1.4).
- Giới hạn GPU của User: mỗi lượt GPU 20–30 câu ⇒ G4 chạy trên **tập cố định 30 câu dev** (§1.1), xác nhận trên 15 câu
  test có đoạn đúng; ghi trước "cỡ mẫu nhỏ ⇒ có thể chưa rõ" và tính sẵn trần số câu cứu được (đề xuất mục 1).
- Kiểm GPU trước mỗi lượt, dừng nếu không phải `cuda` (§0); đo latency đúng cách (đề xuất mục 4).
- Luật đầu ra lỗi của rerank luna ghi trước, không fallback (đề xuất mục 3).
- G2: guardrail "lỗi citation không tăng" đổi thành mức tụt cho phép đã trừ nhiễu 7B (đề xuất mục 2); kiểm `is_refusal`
  xong và thêm cách đếm từ chối một phần (đề xuất mục 8); G2.3 dùng đúng một chính sách thay thế do A chọn; G2.4 thêm
  `none`, baseline gọi "mặc định (không gửi)" (đề xuất mục 5).

**Vòng sửa 1 theo review C23** (`phase_8_1_b16_review.md` §2 phần 2; A quyết M2 lúc chiều 25/10):
- M1: thêm khối tiêu chí chung cho mọi biến thể G2 (§2.1) — chỉ số chính, luật quyết, nhóm Holm, guardrail, xác nhận test.
- M2: luật quyết G4 theo **đúng spec** §5 G4 (`…design.md:141`): MRR@10 **và** đoạn đúng trong 5 đoạn đưa model cùng tăng
  có CI (A quyết, không ghi lệch).
- M3: thêm mốc "native pool 100 không rerank" cho G4-B để tách đóng góp của reranker khỏi đóng góp của pool.
- m3 giới hạn test 15 đã nhìn ở G1.6; m4 cách xử lý khi `packed.sources` lệch số G1; m5 một lượt GPU = một cấu hình + trần
  thời gian; m6 báo cả số câu lỗi citation mới.
- User 25/10: giữ cả 9 câu độ tự nhiên bất đồng ⇒ tập số chính không đổi; số phụ "chỉ natural" thêm 9 câu.

## 0. Chung

- **Số chính** (User 21:58): bỏ câu `unnatural` theo `data/phase_8_1/golden_realism_final.jsonl`. User 25/10 giữ cả 9
  câu `disputed_unnatural` ⇒ tập số chính không đổi; số phụ "chỉ `natural`" tính theo file nhãn sau khi cập nhật 9 câu
  này (thêm 9 câu). Mọi bảng báo cả hai. Dev số chính: 100 câu = 88 câu trong kho + 12 câu `out_of_scope`; 32 câu có
  đoạn đúng.
- **Baseline:** runtime commit hiện hành (`dense_bm25_rrf`, pool 30, k 60, top-10, context 5, reranker `none`, prompt
  `ANSWER_SYSTEM_INSTRUCTIONS`, `gpt-6-luna`, reasoning **mặc định (không gửi)**). Trước khi đo: chạy lại retrieval
  runtime, phải giống byte `cefb2d1a…`; không khớp ⇒ dừng, báo A.
- **Chọn trên dev, xác nhận trên test** chỉ cho phương án "tốt hơn". Câu kín không đụng. G4 được chạy trước khi khóa
  G0.6 (chỉ retrieval, không dùng câu kín; A 11:22).
- **Đoạn đúng:** `gold_draft.jsonl` (`bab707b9…`), chấm theo offset như G1. "5 đoạn đưa model" lấy từ `packed.sources`
  của context builder (C21 m1), không lấy tiền tố top-10. `FullCorpusContextBuilder.build` bỏ qua nguồn không có bằng
  chứng (`backend/retrieval/full_corpus_context.py:97-99`), nên số mới có thể lệch số G1 (G1 lấy tiền tố top-10 dài bằng
  `packed.sources`). Nếu lệch: ghi số câu lệch và từng câu, dùng số từ `packed` làm baseline mới cho mọi so sánh G4; không
  dừng (chỉ dừng khi mốc byte retrieval lệch).
- **Theo cặp:** bootstrap 10.000 (seed 20261024), CI 95%, thắng/hòa/thua; Holm trong từng nhóm biến thể ghi dưới.
- **Judge câu trả lời:** Claude (sub-agent Claude Code; ghi model id), cùng một model judge cho baseline và mọi biến
  thể; prompt chấm `backend/evaluation/full_corpus_judge_prompt.md` (như 7B). Hai câu trả lời **giống hệt từng ký tự**
  thì dùng chung điểm — ghi số câu dùng chung. Judge dùng quota Claude, không USD.
- **Tiền:** chỉ `gpt-6-luna` (0,1 / 0,5 USD mỗi 1M token vào/ra), **trần B17 0,25 USD** (A). Ước từ số thật 7B Run 1:
  947 token vào + 82 ra = **0,000136 USD/câu** ở context 5. Mỗi lượt có phí: **chạy thử 10 câu trước**, đo USD thật, rồi
  mới chạy đủ; lượt nào vượt ước 50% ⇒ dừng, báo A. Ghi token + USD từ log.
- **GPU** (GTX 1650 4 GB, fp32, một model một lúc — D11; M1 `BAAI/bge-reranker-v2-m3`, M2 `AITeamVN/Vietnamese_Reranker`
  đã có trong HF cache ⇒ giữ `HF_HUB_OFFLINE=1`; thiếu file mới bỏ biến đó cho lần tải đầu và ghi lại).
  **Một lượt GPU = một cấu hình (model × cách chấm × đầu vào) trên một tập ≤ 30 câu** (User); chạy tuần tự, không gộp
  nhiều cấu hình vào một lượt. **Trần thời gian:** câu đo đầu tiên của lượt (sau câu khởi động) > 60 s ⇒ dừng lượt đó, bỏ
  cấu hình đó, ghi số thật; cả lượt > 20 phút ⇒ dừng, báo A. **Trước mỗi lượt GPU** kiểm và ghi vào log:
  1. `torch.cuda.is_available()` = True;
  2. model thật ở `cuda`: device của tham số model (`next(model.parameters()).device.type == "cuda"`) sau khi nạp;
  3. `nvidia-smi` thấy tiến trình của lượt + VRAM đang dùng, và **không** có tiến trình GPU của session khác;
  4. một câu thử có thời gian cỡ GPU (so với số CPU đo ở G4.0).

  Một điều không đạt ⇒ **dừng**, không chạy tiếp trên CPU, báo A. Lượt CPU duy nhất là đo latency CPU 5 câu (G4.0), ghi
  rõ là CPU. Trong lúc chạy: dòng "đang giữ GPU" trong `STATUS_B.md`, xóa khi xong.
- **Harness:** `backend/experiments/phase_8_1/` gọi production qua tham số (retrieval, `FullCorpusContextBuilder`,
  `OpenAIFullCorpusGenerator(answer_instructions=…, reasoning_effort=…)`, `CrossEncoderReranker(model_id, device)`).
  Logic biến thể chỉ ở harness: thứ tự context theo tài liệu, "đoạn kèm mục", rerank listwise bằng `gpt-6-luna`.
  Không đổi chatbot / settings runtime; Qdrant chỉ đọc (G2/G4 không cần collection mới).

## 1. G4 — xếp hạng lại (làm TRƯỚC G2: phần GPU không tốn tiền; G1 cho thấy nghẽn ở xếp hạng)

### 1.1 Tập câu (cố định cho mọi nhánh G4, kể cả luna)

- **Dev 30:** 32 câu dev số chính có đoạn đúng, xếp theo `case_index`, lấy `sorted(random.Random(20261024).sample(…, 30))`.
  **Pilot latency 10 câu:** `random.Random(20261024).sample(dev30, 10)`. Danh sách `case_index` ghi vào
  `data/phase_8_1/g4/subset.json` ở bước 2 (private), sha256 ghi trong report.
- **Test 15:** cả 15 câu test có đoạn đúng (một lượt GPU); số chính trên test = 10 câu (bỏ 5 `unnatural`), 15 là số phụ.
  **Giới hạn:** 15 câu test này đã được nhìn ở G1.6 (phân tầng lỗi dev + test, G1 report §5) ⇒ xác nhận trên test không
  hoàn toàn "chưa nhìn"; ghi giới hạn này cạnh mọi kết quả xác nhận G4.
- Số tính lại từ JSONL G1 trên dev 30 (chưa chạy gì mới; C kiểm lại khớp):

  | Mốc (không rerank) | đoạn đúng đủ trong 5 đoạn | trong top-10 | trong hợp hai nhánh |
  |---|---:|---:|---:|
  | runtime (pool 30) | 12/30 | 15/30 | 22/30 |
  | native pool 100 | 15/30 (mất 1 câu so với runtime) | 18/30 | 29/30 |

### 1.2 Cỡ mẫu — ghi trước

- **G4-A (xếp lại top-10) cứu được tối đa 3 câu** trên dev 30 (đoạn đúng có trong top-10 nhưng ngoài 5 đoạn). Với 3
  thắng / 0 thua / 27 hòa, bootstrap theo cặp có ~4% mẫu lại toàn hòa ⇒ cận dưới CI 95% = 0 ⇒ **`context5_gold_all` của
  G4-A về mặt số học không thể tăng có CI**, mà luật spec đòi cả hai chỉ số (§1.4) ⇒ **G4-A không thể ra "tốt hơn"** trên dev
  30; kết quả sẽ là "chưa rõ" hoặc "kém hơn" (nếu mất câu). MRR@10 (keyword) là chỉ số G4-A đổi được: báo riêng CI của nó
  như tín hiệu, không gọi là "tốt hơn". G4-A vẫn chạy vì: guardrail (có làm mất đoạn đúng không), MRR@10, latency, và chọn
  model + cách chấm cho G4-B.
- **G4-B (pool 100) cứu được tối đa 17 câu so với runtime, 14 câu so với mốc native pool 100 không rerank** ⇒ đây là câu
  hỏi chính của G4 (đề xuất mục 1). Cần ≥ 4–5 thắng, 0 thua để CI > 0 (thêm Holm khi 2 biến thể).
- Test 10 câu số chính quá nhỏ cho CI ⇒ "xác nhận" chỉ đòi cùng dấu và guardrail (§1.4).

### 1.3 Đo latency (đề xuất mục 4)

Từng câu một (không gộp nhiều câu vào một batch), không session nào khác dùng GPU (`nvidia-smi` trước lượt), bỏ lần nạp
model và 1 câu khởi động đầu (không tính vào số đo), báo p50 / p95 cho **cả luồng** (retrieval + rerank + context) và **từng
khâu** (retrieval, rerank). CPU: 5 câu đầu của pilot, cùng cách. `model_max_length` thật của tokenizer M1/M2 ghi ở G4.0.

### 1.4 Thí nghiệm

```yaml
- experiment_id: G4.0_pilot_latency
  measure: "10 câu pilot (§1.1), GPU — M1, M2 × (đoạn trơn, đoạn kèm mục) × (top-10, pool 100) = 8 lượt, mỗi lượt một cấu hình (trần thời gian §0); CPU 5 câu — M1, M2 top-10 đoạn trơn"
  purpose: p50/p95 thật trước khi chạy đủ; "đoạn kèm mục" > 3 s/câu ở top-10 thì ghi số thật cho User cân nhắc
  cost_usd: 0
- experiment_id: G4-A_rerank_top10        # spec §5 G4
  baseline: runtime top-10, reranker none
  changed_variable: thứ tự top-10 do reranker quyết (tập 10 đoạn giữ nguyên)
  variants: [M1 đoạn trơn, M1 đoạn kèm mục, M2 đoạn trơn, M2 đoạn kèm mục, luna listwise đoạn trơn]   # Holm trên 5
  section_text: "các chunk cùng (source, heading_path) nối theo thứ tự; cặp (câu hỏi, đoạn) cắt ≤ 1024 token tokenizer của từng model, như nhau cho M1/M2"
  data: {group: dev, subset: dev30 (§1.1)}
  primary_metrics: [context5_gold_all (đoạn đúng đủ trong 5 đoạn đưa model), MRR@10 (keyword, 30 câu)]   # spec §5 G4, cả hai
  secondary: context5_gold_frac, nDCG@10, thắng/hòa/thua, natural
  guardrails:
    - "0 câu mất đoạn đúng khỏi 5 đoạn đưa model so với baseline"
    - "latency p95 GPU ≤ 3 s/câu (ước; ghi số thật nếu vượt)"
  luna_output_rule: >   # đề xuất mục 3 — ghi trước, không fallback
    structured output là danh sách id; hợp lệ = đúng 10 id đã đưa, mỗi id một lần. Thiếu / lặp / thêm id lạ / bị cắt /
    lỗi API = lỗi kỹ thuật: lưu nguyên output, KHÔNG thay bằng thứ tự gốc, không gọi lại. Bảng báo "n câu hợp lệ / 30";
    chỉ số tính trên câu hợp lệ, baseline cùng tập câu đó. Biến thể có ≥ 1 câu lỗi không được kết luận "tốt hơn" (run
    incomplete, quy ước 7A). Pilot 10 câu có ≥ 2 câu lỗi ⇒ dừng, báo A (không tự sửa prompt rồi chạy lại).
  decision_rule: >
    tốt hơn = context5_gold_all VÀ MRR@10 đều CI > 0 sau Holm (mỗi chỉ số Holm trên 5) + đủ guardrail → xác nhận trên test
    15. kém hơn = một trong hai cận trên CI < 0 hoặc vi phạm guardrail. Còn lại = chưa rõ. Theo §1.2, G4-A không thể ra
    "tốt hơn" trên dev 30; MRR@10 CI > 0 một mình chỉ ghi là tín hiệu.
  cost_usd: "M1/M2 = 0; luna: pilot 10 câu + 20 câu còn lại ≈ 30 × (1.400 vào + 100 ra) ≈ 0,006; test 15 nếu thắng ≈ 0,003"
- experiment_id: G4-B_rerank_pool100      # sửa đổi spec §5 G4, User duyệt 25/10
  baseline: runtime top-10
  reference_no_rerank: >   # C23 M3 — tách đóng góp của reranker khỏi đóng góp của pool
    mốc thứ hai "native pool 100 không rerank" (top-10 theo RRF native) trên cùng dev 30; chạy lại retrieval bằng harness
    G4 (free, không GPU) để context lấy từ packed.sources như các nhánh khác
  changed_variable: reranker chấm hợp hai nhánh native pool 100 rồi lấy top-10 (sau đó context 5 như runtime)
  variants: "1 hoặc 2 (M1 / M2), cách chấm chọn theo luật dưới; Holm trên số biến thể"
  choose_rule: >   # ghi trước; G4-B không chờ G4-A thắng
    sau G4-A, chọn model theo context5_gold_frac trên dev 30 (số phụ), hòa thì theo MRR@10; hai model chênh ≤ 1 câu ở
    context5_gold_all thì chạy cả hai (Holm 2). Cách chấm: theo cùng chỉ số; nếu "đoạn kèm mục" ở pool 100 có p95 > 30
    s/câu ở G4.0 (≈ 15 phút một lượt 30 câu) thì dùng đoạn trơn và ghi số thật. Lý do chọn ghi vào report TRƯỚC khi chạy.
  data: {group: dev, subset: dev30}
  primary_metrics: [context5_gold_all, MRR@10 (keyword, 30 câu)]   # spec §5 G4, cả hai
  secondary: top10_gold_all, context5_gold_frac, nDCG@10
  guardrails: ["0 câu mất đoạn đúng khỏi 5 đoạn đưa model so với runtime", "latency p95 ghi số thật (100 cặp/câu)"]
  decision_rule: >
    (1) so runtime: tốt hơn = context5_gold_all VÀ MRR@10 đều CI > 0 sau Holm (trên số biến thể) + đủ guardrail; kém hơn /
    chưa rõ như G4-A. (2) so mốc native pool 100 không rerank, cùng luật và cùng Holm: chỉ khi (2) "tốt hơn" mới kết luận
    "reranker có đóng góp". (1) tốt hơn mà (2) không ⇒ báo riêng "lợi đến từ pool rộng, chưa thấy đóng góp của reranker"
    (kết quả cho 8.2: có thể không cần GPU). Xác nhận trên test (cho (1), và cho (2) nếu (2) tốt hơn): số chính 10 câu
    thắng > thua ở context5_gold_all, 0 câu mất, MRR@10 cùng dấu, 15 câu cùng dấu; kèm giới hạn test đã nhìn (§1.1)
  cost_usd: 0 (GPU); luna pool 100 không làm (≈ 10.000 token/câu, đắt và chậm)
```

## 2. G2 — sinh câu trả lời, retrieval giữ cố định = runtime (spec §5 G2)

Đo tách hai nhóm như C21 gợi ý: **(a) context có đủ đoạn đúng** (`context5_gold_all = 1`) và **(b) context thiếu** — với câu
không có đoạn đúng dùng proxy keyword đáp án trong context (`evidence_rate`). (a) cho biết prompt có làm hỏng câu đáng lẽ
đúng không; (b) cho biết prompt xử lý thiếu bằng chứng ra sao. G2 không dùng GPU ⇒ chạy cả 120 câu dev, phân tích theo số
chính.

**Nhiễu sẵn có (7B Run 1 ↔ Run 2, 176 câu, 0 USD — đề xuất mục 2):** 16/176 câu đổi ít nhất một điểm; lỗi citation 4 → 6;
từ chối nhầm 22 = 22, 0 câu đổi quyết định từ chối (`reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md` §4.2,
§5). Quy về 120 câu dev: lỗi citation dao động ≈ 2 × 120/176 ≈ 1,4 ⇒ **cho phép tối đa +2 câu**.

**Từ chối (đề xuất mục 8, đã kiểm):** `is_refusal` (`backend/evaluation/full_corpus_eval.py:167-169`) chỉ đúng khi toàn
bộ câu trả lời trùng hệt `INSUFFICIENT_ANSWER`; test `backend/tests/test_full_corpus_eval.py:54` khẳng định câu từ chối + câu
thêm **không** tính là từ chối. ⇒ Câu "trả lời một phần" (P1) bị tính là đã trả lời. Cách đếm ở G2: giữ `is_refusal` làm
"từ chối nhầm" (so được với 7B), thêm nhãn `answer_type ∈ {full, partial, refusal}` do **một sub-agent Claude riêng** gắn
(không phải judge; cùng chỉ dẫn cố định cho baseline và mọi biến thể; không biết câu thuộc biến thể nào), kèm đếm máy "chứa
`INSUFFICIENT_ANSWER` như chuỗi con" để đối chiếu.

### 2.1 Tiêu chí chung cho mọi biến thể G2 (ghi trước — C23 M1)

```yaml
applies_to: [G2.1a, G2.1b, G2.2 P1, G2.2 P2, G2.4 none, G2.4 low, G2.4 high]
baseline: G2.0 (sinh lại cùng phiên); so theo cặp trên dev số chính
primary_metric: Completeness (judge Claude), 88 câu trong kho của dev số chính
secondary: Accuracy, Relevance, từ chối nhầm (`is_refusal`, thắng/thua theo câu), answer_type, lỗi citation, tách nhóm (a)/(b), natural
holm_groups: {G2.1: 2 (a, b), G2.2: 2 (P1, P2), G2.4: 3 (none, low, high)}
guardrails:
  - "từ chối đúng out_of_scope dev giữ nguyên: 0 câu out_of_scope bị trả lời (nhiễu 7B = 0 câu đổi)"
  - "Accuracy không tụt: cận trên CI 95% của chênh Accuracy ≥ 0"
  - "lỗi citation: tổng của biến thể − G2.0 ≤ +2 câu trên 120 dev (nhiễu 7B); > +2 = vi phạm. Báo cả số câu lỗi MỚI
     (lỗi ở biến thể, không lỗi ở G2.0) và số câu hết lỗi — 7B Run 1/2 chỉ 2 câu lỗi chung (C23 m6)"
  - "USD/câu ≤ 2 × G2.0 (đo từ log); G2.4 thêm: token ra trung bình/câu báo riêng, high vượt 2 × thì ghi là vi phạm"
decision_rule: >
  tốt hơn = Completeness CI > 0 sau Holm trong nhóm + đủ mọi guardrail → xác nhận trên test 56 (số chính). kém hơn =
  Completeness cận trên CI < 0 hoặc vi phạm guardrail. Còn lại = chưa rõ / không khác (cận dưới CI ≤ 0 ≤ cận trên).
test_confirmation: >
  chỉ cho biến thể "tốt hơn": chạy G2.0 + biến thể trên 56 câu test; xác nhận = chênh Completeness cùng dấu + đủ guardrail
  (không đòi CI vì cỡ mẫu nhỏ). Câu kín không đụng.
```

```yaml
- experiment_id: G2.0_baseline_fresh
  run: baseline sinh lại dev (120 câu gồm out_of_scope) trong cùng phiên với các biến thể
  why: so biến thể với lượt baseline mới; so thêm 7B Run 1 làm đối chứng nhiễu
  cost_usd: "≈ 120 × 0,000136 ≈ 0,016"
- experiment_id: G2.1a_context10
  changed_variable: max_context_documents 5 → 10 (qua build_context_builder, như probe B5)
  criteria: §2.1 (Holm trên 2 cùng G2.1b)
  cost_usd: "≈ 120 × 0,00021 ≈ 0,026 (≈1.700 token vào/câu)"
- experiment_id: G2.1b_context_doc_order
  changed_variable: 5 đoạn giữ nguyên tập, xếp gom theo tài liệu (thứ tự xuất hiện đầu tiên) thay vì theo hạng
  criteria: §2.1 (Holm trên 2 cùng G2.1a)
  cost_usd: "≈ 0,016"
- experiment_id: G2.2_prompt
  variants:   # Holm trên 2
    P1_partial: >
      baseline, thay luật từ chối bằng: "Nếu bằng chứng chỉ đủ cho một phần câu hỏi, trả lời phần có căn cứ kèm
      citation, rồi nói rõ phần nào nguồn dữ liệu không có thông tin bằng một câu riêng không citation. Chỉ khi không có
      bằng chứng liên quan nào, trả đúng duy nhất câu sau, không thêm citation: <INSUFFICIENT_ANSWER>"
      — câu báo thiếu KHÔNG được dùng nguyên câu từ chối, vì validator (`llm/citations.py`) coi câu trả lời chứa câu từ
      chối + citation là lỗi.
    P2_spec_rules: >
      baseline + 2 luật spec Phase 6 §10 đang thiếu: "Không dùng tiêu đề hoặc tên mục làm bằng chứng nếu phần Bằng
      chứng không hỗ trợ." và "Dùng đoạn văn ngắn cho câu hỏi đơn giản; chỉ dùng danh sách khi câu trả lời thật sự có
      nhiều mục hoặc bước."
  criteria: §2.1 (chỉ số chính Completeness, Holm trên 2, guardrail chung)
  extra_secondary: claim không nguồn trên 32 câu có đoạn đúng; số câu answer_type = partial
  note: H8 chỉ THỬ ở 8.1, quyết ở 8.2 (CURRENT_HANDOFF); P1 đổi hành vi so với spec Phase 6 §10 nên kết luận chỉ là đề xuất
  cost_usd: "≈ 2 × 0,016 ≈ 0,033"
- experiment_id: G2.3_citation_replay
  run: >
    phát lại trên câu trả lời đã lưu (7B Run 1/2 + G2.0) hai chính sách: (1) validator hiện tại; (2) chính sách thay thế
    A chọn 11:22 — câu trả lời mà context chỉ có **một nguồn** (hoặc mọi câu thiếu `[n]` đều thuộc đúng một nguồn duy
    nhất được trích) thì gán nguồn đó thay vì báo lỗi
  measure: số câu lỗi citation (User thấy lỗi 500) mỗi chính sách; liệt kê từng câu đổi kết luận để đọc tay xem gán có đúng nguồn không
  note: chỉ đo, không đổi chatbot
  cost_usd: 0 (phát lại, đo khâu sau bước sinh — skill §3.5)
- experiment_id: G2.4_reasoning_effort     # tùy chọn, spec; đề xuất mục 5
  baseline: mặc định (không gửi tham số reasoning) — không gọi là "medium"
  variants: [none, low, high]   # Holm trên 3
  criteria: §2.1 (gồm guardrail USD/câu và token ra)
  pilot: >
    10 câu mỗi mức, đo token/USD thật; chỉ chạy 120 câu nếu tổng vẫn trong trần. Nếu API trả lỗi cho một mức (ví dụ
    `none` không được model nhận) thì ghi lỗi quan sát được, bỏ mức đó, không đổi model / tham số khác để lách
  cost_usd: "pilot ≈ 0,005–0,015; đủ 120 câu: none/low ≈ 0,016 mỗi mức, high ước 0,03–0,08 (chưa đo)"
```

## 3. Tổng tiền ước (trần B17: 0,25 USD; trần 8.1: 0,5 USD)

| Thí nghiệm | USD ước |
|---|---:|
| G4-A luna listwise (dev 30; test 15 nếu thắng) | ≈ 0,006 – 0,009 |
| G2.0 + G2.1a + G2.1b | ≈ 0,058 |
| G2.2 (2 prompt) | ≈ 0,033 |
| G2.4 (pilot 3 mức; đủ nếu đáng) | ≈ 0,005 – 0,11 |
| Xác nhận trên test cho phương án G2 thắng (ước 1–2 lượt × 56 câu) | ≈ 0,02 |
| **Cộng** | **≈ 0,12 – 0,23** |

Không tính phần đã tiêu trong 8.1 trước đó (A theo dõi). Vượt ước 50% ở bất kỳ lượt nào ⇒ dừng, báo A. Tổng sắp chạm
0,25 USD ⇒ bỏ phần G2.4 chạy đủ trước.

## 4. Thứ tự (bước 2, chỉ sau khi A ghi "duyệt bản sha …" trong mục B17)

1. Retrieval mốc byte `cefb2d1a…`. 2. Ghi `data/phase_8_1/g4/subset.json` (dev 30, pilot 10, test 15) + sha. 3. G4.0
pilot latency (GPU + CPU 5 câu). 4. Mốc runtime + mốc native pool 100 không rerank trên dev 30 (free, không GPU; ghi số
câu lệch G1 nếu có). 5. G4-A M1/M2 (free) → luna pilot 10 câu → luna 20 câu còn lại. 6. Ghi lý do chọn rồi G4-B (free).
7. Xác nhận test 15 cho nhánh G4 nào "tốt hơn". 8. G2.0 + G2.1 (pilot 10 câu mỗi lượt) → judge + `answer_type`.
9. G2.2 → judge. 10. G2.3 (free). 11. G2.4 pilot → A quyết chạy đủ. Mỗi gate: report + review chéo (C).
