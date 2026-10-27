# Plan: Phase 8.2 §10 — K3b, `gpt-6-luna` chọn 10 đoạn từ pool 30 (chỉ trả 10 số), hai nhánh mức suy luận

Người viết: B (Claude Opus 5.5, `hue-rag-31`) · 2026-10-27 09:13 +0700 (`date`) · Việc: B56 (A giao 27/10). Trạng thái: **bản 2** (sửa theo review C50 + quyết định A,
09:22 27/10/2026; bản 1 `4f92e478cb65`) — chờ C kiểm phần sửa, rồi A ghi "duyệt bản sha" (`WORKFLOW.md` §9.1). **Chưa gọi API; 0 USD.**

Plan không chép câu hỏi, đáp án hay đoạn kho. Repo public: chỉ có `case_index` và số đếm.

## Căn cứ để review

1. `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` **§10.2–§10.4** (bản A duyệt `cd910c4c4169`): mốc, luật (i), "chất
   lượng trước", sàn chung, Holm theo nhánh, dòng K3 bảng §10.3, tiền, "tốn hơn ⇒ trình User".
2. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_plan.md` **§1, §4, §6** (sha `0a6370204c7d`): khung K3 mà K3b giữ nguyên (pool 30, trần
   9 câu, luật thắng / thua hai lượt, sàn).
3. Report K3 trên nhánh: `git show origin/p82-k3:report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k3_implementation.md` **§4.1, §4.3–§4.5, §5**:
   lỗi đầu ra (câu 173), số theo dõi 39 câu, token, tiền, latency. Kèm review C49 `phase_8_2_k3_review.md` **§5–§6** (giới hạn của số 9 / 0;
   yêu cầu đo tỉ lệ lỗi luna như một chỉ số; "bù theo RRF" là fallback) và review plan C50 `phase_8_2_k3b_plan_review.md` §2.
4. Code: `backend/experiments/phase_8_1/g4_rerank.py` **dòng 63–93** (`LUNA_INSTRUCTIONS`, `luna_rank`) và
   `backend/llm/generator_openai_full_corpus.py` **dòng 94–118** (cách runtime / 8.1 gửi `reasoning`), cả hai ở `811d25d`.
   Harness K3 `git show origin/p82-k3:backend/experiments/phase_8_2/k3.py`.

Người review được chạy lệnh chỉ đọc và tính lại từ `data/phase_8_2/k3/` (`base_dev`, `base_test`, `l1_pilot`, `l1_rest`) và
`data/phase_8_2/k1/base_dev.jsonl`.

## 1. Câu hỏi và giả định

**Lớp bài toán** (giữ từ K3): ở mốc context 10, 9 câu dev có đủ đoạn đúng trong pool 30 nhưng RRF không xếp vào top-10. K3 (luna xếp đủ 30)
có tín hiệu lớn: trên 39 câu hợp lệ của một lượt, thắng 9 / thua 0. Nhưng K3 dừng vì hai vấn đề:
- **lỗi đầu ra:** luna trả 29 / 30 số ở câu 173, tức 1 / 40 lần gọi;
- **giá:** `rerank_ms` p50 5,6 s, p95 8,6 s; USD / câu đầu–cuối ≈ 4×.

K3b hỏi: giữ được lợi ở tầng tìm với **hợp đồng đầu ra ghi trước** và **giá thấp hơn** không?

**K3b đổi gì so với mốc B1** (luật "đổi một thứ" tính so mốc — spec §10.2: mọi biến thể so cùng mốc, không so nối tiếp): thêm **một bước**
"luna chọn 10 từ 30 đoạn RRF". Bước này có hai tham số đặt khác K3: **đầu ra 10 số** (thay vì đủ 30) và **mức suy luận**. Hai nhánh:

| Nhánh | Đầu ra luna | `reasoning` của lần gọi rerank | Vai |
|---|---|---|---|
| **K3b-n** | 10 số đầu | `{"effort": "none"}` | cấu hình rẻ / nhanh nhất; nếu giữ được lợi thì đây là bản đáng trình User |
| **K3b-m** | 10 số đầu | không gửi (= mặc định `medium`, như K3 và runtime) | gần K3 nhất; cho biết bỏ suy luận có làm mất lợi không |

**Vì sao không gộp thành một biến thể** (A gợi ý ghép `none`): so với mốc thì gộp vẫn là "một bước thêm", nhưng hai tham số ảnh hưởng hai thứ
khác nhau. Bỏ suy luận có thể làm **xếp hạng kém đi**, tức đúng chỉ số quyết. Đầu ra 10 số thì đổi **hợp đồng lỗi**. Nếu chỉ chạy bản gộp
mà trượt, sẽ không biết vì đâu: do bỏ suy luận, hay do hướng rerank không giữ được ở lượt thứ hai. Nhánh m tốn thêm tối đa ≈ 0,058 USD (§5),
chỉ chạy khi nhánh n không đạt (luật thứ tự dưới đây).

**Thứ tự (A chốt sau C50 m-4):** K3b-n trước. Lý do: (1) giá là chỗ K3 không trình User được (p95 8,6 s so với mức theo dõi 5 s); (2) K3b-n
rẻ hơn. **K3b-m chỉ chạy khi K3b-n kém hơn hoặc chưa rõ** về chất lượng tầng tìm (§4). K3b-n "tốt hơn (tạm)" ⇒ **không chạy** K3b-m, kể cả khi
K3b-n dưới trần 9 / 0.
- Lý do (C50 m-4, *suy ra* từ 40 lần gọi K3): `rerank_ms` gần như tuyến tính theo token ra (tương quan 0,94; ≈ 9,2 ms / token + 1,8 s).
- K3b-m (token ra ≈ 410, G3) ước ≈ **5,6 s**, tức như K3, nên không sửa được vấn đề giá. K3b-n (≈ 25–40 token) ước ≈ **2,1 s**.
- K3b-m chỉ còn giá trị khi K3b-n không giữ được chất lượng: lúc đó nó cho biết lợi có còn khi có suy luận + hợp đồng mới không.

*Không trái* "chất lượng trước": cả hai nhánh đều là biến thể nâng chất lượng (luật (i)). K3b-n thắng thì đã có chất lượng cần thiết ở giá thấp hơn.

**Chữ prompt rerank (ghi trước, không sửa sau khi thấy số).** Câu đầu giữ nguyên `LUNA_INSTRUCTIONS` 8.1, chỉ câu sau đổi:

```text
Bạn xếp hạng các đoạn văn theo mức hữu ích để trả lời câu hỏi của người dùng về du lịch và văn hóa Huế. Trả về đúng 10 số thứ tự của 10 đoạn hữu ích nhất, mỗi số đúng một lần, đoạn hữu ích nhất đứng đầu.
```

Đầu vào luna giữ y K3 (`luna_rank`): `Câu hỏi: …` + 30 đoạn `[n] <search_text>` theo thứ tự RRF. Đầu ra có cấu trúc `{"order": list[int]}`
(Pydantic `extra="forbid"`, như `LunaRanking`). Không ép độ dài bằng schema: không dựa vào `minItems` / `maxItems` của structured output. Độ
dài do hợp đồng §2 xử lý. `store=False`, `max_output_tokens` = `answer_max_output_tokens` (2048 ở `811d25d`), model `gpt-6-luna`, `timeout` 45 s,
`max_retries=0`.

**Giả định — kiểm bằng máy trước khi code / ở lần gọi đầu:**

| Giả định | Kiểm | Kết quả / khi nào kiểm |
|---|---|---|
| G1. Trần dev 9, test 3 trên đúng mốc (W23) | `data/phase_8_2/k3/base_{dev,test}.jsonl` (K3 bước 0, M2 khớp K1) | dev: `pool_gold_all` 1 ∧ `top10_gold_all` 0 = **9** (17, 38, 48, 67, 70, 85, 156, 159, 167); test **3** (20, 95, 130). Mốc context = top-10 ở 40 / 40 (B đã tính 09:0x) |
| G2. API nhận `reasoning={"effort": "none"}` qua `responses.parse` | 8.1 G2.4 gửi `none` qua `Reasoning(effort=…)` (`generator_openai_full_corpus.py:118`): "API nhận cả `none`" | **lần gọi đầu của pilot**; API từ chối ⇒ lỗi kỹ thuật ⇒ dừng nhánh n, báo A |
| G3. Đầu ra 10 số giảm token ra | K3: TB 453, max 818 / lần (gồm suy luận); JSON 30 số ≈ 65 token (*ước*) ⇒ suy luận ≈ 390 | *ước* K3b-m ≈ 410, K3b-n ≈ 25–40; **đo ở pilot** |
| G4. Lỗi đầu ra K3 thuộc dạng hợp đồng §2 xử lý được | câu 173: `status completed`, 29 số, thiếu 5, không lặp, không số lạ; C50 đếm: 40 / 40 lần gọi K3 trả ≥ 29 số hợp lệ | dạng "danh sách sai" (không phải lỗi API) ⇒ hợp đồng §2 loại 3 |
| G5. Giảm suy luận giảm latency | 8.1 G2.4 (khâu sinh): `none` p50 1,53 s / p95 2,07 s so với 1,66 / 2,79 s (`de_xuat_khau_tra_loi_C.md` §3) — khâu khác, đầu ra khác | *giả thuyết* cho rerank; **đo ở pilot** |

## 2. Hợp đồng đầu ra (ghi trước; tất định; có đếm, có trần)

Mỗi lần gọi phân thành **một** trong ba loại:

1. **Lỗi kỹ thuật** (sàn = 0; dừng như K3 plan §6.3): `OpenAIError` (gồm timeout), `status != "completed"` (gồm bị cắt ở `max_output_tokens`), hoặc
   `output_parsed is None`. Ba loại này không có danh sách để dùng. Ở chatbot, xử lý chúng là quyết định sản phẩm (User), không thuộc plan
   này. **Không gọi lại, không thay bằng thứ tự RRF.**
2. **Đầu ra đúng hợp đồng:** `order` gồm **đúng 10 số, mỗi số trong 1..30, không lặp** ⇒ top-10 = các đoạn đó theo thứ tự luna.
3. **Đầu ra sai hợp đồng** (mọi trường hợp còn lại: thiếu / thừa số, lặp, số ngoài 1..30) ⇒ câu đó dùng **nguyên top-10 RRF** (= mốc). Không ghép
   một phần danh sách luna. Mỗi lần gọi ghi `contract_violation` và dạng: `n_returned`, `n_out_of_range`, `n_duplicate`.

**Đổi so với K3 — nói thẳng (C50 m-1, A duyệt cùng sha):** ở K3, "đầu ra không phải hoán vị" là **sàn** (K3 dừng vì nó). Ở K3b, dạng này thành
**mức tụt có trần** (dưới đây).
- Lý do: K3b là biến thể mới, tiêu chí ghi trước khi chạy (vòng 2 / 3, §6.6).
- Người dùng không nhận lỗi: câu đó vẫn có top-10 = mốc, nên sàn chung spec §10.2 "0 lỗi kỹ thuật / 500" vẫn đạt.
- **Kết luận K3 không đổi: kém hơn.** Lỗi kỹ thuật (loại 1) vẫn là sàn 0.

**Loại 3 là fallback** — lý do theo `Session_Prompt.md` §7:
- **Vấn đề quan sát được:** K3 câu 173 (1 / 40 lần gọi).
- **Cách trực tiếp không đủ:** gọi lại thì thêm tiền và độ trễ, không chắc hết lỗi. Dừng cả câu thì chatbot không có top-10.
- **Lợi giải thích được:** người dùng vẫn nhận top-10, và tác hại bị chặn đúng bằng mốc.
- **Bằng chứng:** đếm mọi lần dùng và báo theo `case_index`.
- **Độ phức tạp tương xứng:** một điều kiện, một hàm thuần có test.

**Vì sao chọn "nguyên RRF" thay vì "lọc rồi bù theo RRF" của bản 1** (C50 m-2; A nghiêng về cách đơn giản khi tác động tương đương):
- "Lọc + bù" giữ được các số hợp lệ của luna khi danh sách sai, nhưng trộn hai thứ tự và cần 4 bước.
- Với trần ≤ 4 lần sai / nhánh, hai cách chỉ khác nhau ở tối đa 4 câu. Ở K3, mọi lần gọi đều trả ≥ 29 số hợp lệ (C50), nên dự đoán hai cách cho
  cùng kết quả.
- ⇒ Chọn cách đơn giản hơn. Cái giá: một câu sai hợp đồng mất lợi của luna ở câu đó. Cái giá này **hiện ra ở chỉ số quyết**, không bị che.

**Trần sai hợp đồng — số đếm tuyệt đối** (C50 m-3): cộng dồn mọi lần gọi của một nhánh (dev L1 + L2 + test), **≤ 4 lần, bất kể n**. Báo kèm
k / n và CI 95 % Clopper–Pearson, theo dạng. Vượt trần ⇒ nhánh **kém hơn**, dù chỉ số quyết qua: hợp đồng đã thành cơ chế chính thay vì ngoại lệ.
Câu sai hợp đồng vẫn tính vào chỉ số quyết và sàn với top-10 = mốc.

## 3. Mốc, harness

- **Mốc:** `811d25d` (context 10 + NFC). Tầng tìm mốc = `data/phase_8_2/k3/base_{dev,test}.jsonl` (lượt `--rerank none` của K3, M2 khớp K1
  40 / 40). **Kiểm mốc trước khi gọi luna:**
  - M1: T1 sha `cefb2d1ad609`;
  - M2': chạy lại `--rerank none` dev bằng harness K3b, `top_chunk_ids` + `top10_gold_*` + `context_gold_*` khớp từng câu với `k3/base_dev.jsonl`.
- **Nhánh `p82-k3b`** tạo từ `origin/p82-k3` `80e7329`, worktree `/tmp/b_k3b` (bẫy worktree `Project_Status.md` §8).
- **Harness mới `backend/experiments/phase_8_2/k3b.py`.** Không sửa `k3.py`, `g4_rerank.py`, production.
  - Import từ `k3`: `gold_cases`, `new_file`, `POOL`, `TOP_K`.
  - Vòng lặp tầng tìm giống `k3.retrieval` (`service.search` production, 30 đoạn từ `stages["rrf"]`, context builder production, `gold_coverage`).
    Chỉ thay lần gọi rerank bằng `luna_top10(…, effort)` + `apply_contract(order, n=30)` (§2: đúng 10 số hợp lệ ⇒ dùng, không thì
    top-10 RRF).
  - `compare` dùng luật hai lượt của K3 và Holm họ cố định (§4).
  - Dừng ở lỗi kỹ thuật đầu tiên. Từ chối ghi đè. Ghi `data/phase_8_2/k3b/`.
  - Lặp ~40 dòng vòng lặp của `k3.retrieval` là chấp nhận được: tham số hóa `k3.py` sẽ sửa harness đã làm hồ sơ cho K3.
- Có một test nhỏ cho `apply_contract` (logic thuần, input nhỏ): đúng / thiếu / thừa / lặp / ngoài khoảng. Đây là logic quyết định
  top-10 nên đáng có test.

## 4. Tiêu chí ghi trước

```yaml
experiment_id: p82_k3b_luna_choose10_pool30
baseline: p82-b1 811d25d — dense_bm25_rrf pool 30, RRF k 60, không rerank, context 10, NFC (tầng tìm: data/phase_8_2/k3/base_{dev,test}.jsonl)
changed_variable: "thêm bước luna chọn 10 từ 30 đoạn RRF, đầu ra 10 số + hợp đồng §2; nhánh n: reasoning none, nhánh m: không gửi reasoning"
unchanged: [corpus, chunker, e5-small, index, pool 30, rrf_k 60, context 10, context builder, đầu vào luna (câu hỏi + 30 đoạn thứ tự RRF), model gpt-6-luna, max_output_tokens 2048]
data:
  dev: {gold: 40 câu, trần 9}        # split e2b1788dfbbc, gold bab707b9ab22
  test: {gold: 15 câu, trần 3}       # test đã nhìn ở G1.6 / K3 bước 0 (chỉ mốc)
noise_AA: "luna không tất định ⇒ mỗi nhánh 2 lượt dev (L1, L2); nhiễu = số câu đổi context_gold_all giữa L1 ↔ L2"
metrics:
  # sàn (mỗi nhánh; lượt nào cũng tính)
  - {name: câu mất đoạn đúng (mốc context_gold_all 1 → 0, hoặc top10_gold_all 1 → 0), set: "dev 40 (L1, L2) + test 15", role: floor, floor: 0}
  - {name: lỗi kỹ thuật (§2 loại 1), set: mọi lần gọi, role: floor, floor: 0}
  # quyết (mỗi nhánh)
  - {name: context_gold_all, set: dev 40, role: decide,
     rule: "thắng = mốc 0 → 1 ở CẢ L1 và L2; thua = mốc 1 → 0 ở ÍT NHẤT một lượt; bootstrap_mean_diff trên vector +1 / −1 / 0 (seed 20261024),
            CI 95 % > 0 VÀ Holm họ nhánh tìm CỐ ĐỊNH {K1 p 0,798, K3 p 1 (dừng, không có p), K3b-n, K3b-m (p 1 nếu không chạy)} < 0,05"}
  # (context = đoạn thật sự đưa model; ở mốc context = top-10 ở 40 / 40, nên hai chỉ số trùng ở mốc — top10_gold_all là theo dõi.
  #  Chỉ số quyết đo bằng ĐOẠN ĐÚNG (gold_coverage); MRR / nDCG theo keyword chỉ theo dõi)
  # mức tụt (mỗi nhánh)
  - {name: số lần đầu ra sai hợp đồng (§2 loại 3 ⇒ top-10 RRF), set: "cộng dồn mọi lần gọi của nhánh (dev L1 + L2 + test)", role: tolerance,
     max: "≤ 4 lần (số đếm tuyệt đối, bất kể n)", report: "k / n, CI 95 % Clopper–Pearson, case_index, theo dạng (thiếu / thừa / lặp / ngoài khoảng)"}
  # theo dõi
  - {name: rerank_ms p50 / p95, role: watch, report: "kèm CI bootstrap; mức theo dõi 5 s p95 (spec §10.2)"}
  - {name: tìm đầu–cuối p50 / p95 (retrieval + rerank), role: watch}
  - {name: token luna vào TB / ra TB / ra max, role: watch}
  - {name: USD / lần rerank và USD / câu đầu–cuối, def: "rerank đo thật + sinh mốc B1 0,000204 (lượt sinh NOT RUN trong plan này)", role: watch}
  - {name: top10_gold_all, top10_gold_frac, MRR@10, nDCG, số câu đổi tập top-10, 120 / 168, role: watch}
  - {name: so K3 (một lượt, 39 câu) trên cùng câu, role: watch}
result: null
conclusion: null   # tầng tìm mỗi nhánh: tốt hơn / không đổi / kém hơn / chưa rõ; giá: số thật ⇒ A trình User
```

**Cỡ mẫu** (dev 40, `bootstrap_mean_diff` seed 20261024, B tính 09:1x): 4 / 0 ⇒ p 0,026; **5 / 0 ⇒ p 0,0076**; 6 / 0 ⇒ 0,0024. Holm họ 4 (K1 0,798, K3 1,
K3b-n, K3b-m): nếu chỉ một nhánh có p nhỏ, p Holm = 4 × p ⇒ **5 / 0 ⇒ 0,030 < 0,05 qua; 4 / 0 ⇒ 0,106 trượt**. Mọi câu thua đã phạm sàn, nên
thực tế cần **≥ 5 thắng ổn định / 0 thua**. Trần 9 ⇒ đủ chỗ. Số theo dõi K3 cho 9 / 0 trên một lượt, nhưng hai nhánh K3b đổi prompt và mức suy
luận. **Ghi trước: "chưa rõ" (< 5 / 0 ổn định) có thể xảy ra, nhất là ở nhánh n.**

**Dev và test.** 9 câu trần được chọn **trên chính dev** (B42), nên số dev có thể lạc quan. Test là phép **xác nhận "không làm hỏng"**
(spec §10.2; User đồng ý Q2 §10.6 sáng 27/10): trần test chỉ 3, nên không thể thấy "tốt hơn". Test chạy **một lượt** (ghi rõ trong report), còn
dev có A/A (L1, L2). Số thắng trên test (≤ 3) chỉ theo dõi.

**Luật giữ (mỗi nhánh):**
1. Dev L1 + L2: đủ sàn, không vượt mức tụt, chỉ số quyết qua ⇒ chạy test 15 (một lượt).
2. Test: 0 câu mất, 0 lỗi kỹ thuật, mức tụt sai hợp đồng vẫn đạt (đếm cả lần gọi test) ⇒ **tầng tìm "tốt hơn (tạm)"**.
3. Kết luận tầng tìm + giá (rerank_ms, USD / câu đầu–cuối, tỉ lệ sai hợp đồng) ⇒ **A trình User**, vì mọi nhánh đều thêm lần gọi API (spec
   §10.2: "tốn hơn" ⇒ User). Plan này không tự nhận biến thể nào.

**Tầng trả lời (lượt sinh + judge) — ngoài plan này, ngoài trần dưới đây.** Chỉ làm khi một nhánh đạt luật giữ bước 2. Khi đó:
- B viết phụ lục ngắn: ước tiền từ USD đo thật, A duyệt trần riêng;
- tiêu chí giữ **nguyên** K3 plan §4 phần "tầng trả lời" (sàn OOS 0 / 18, lỗi kỹ thuật / 500 0, mức tụt Completeness 4 / 6, Accuracy 4 / 5, từ chối
  nhầm +1 / +1, citation v2 +2, `output_tokens` sinh +20 %);
- phát lại thứ tự luna đã ghi cho 55 câu có đoạn đúng (`run-experiment` §3.5), gọi mới cho phần còn lại.

Lý do để ngoài: A cần **giá thật** của lợi tầng tìm trước. Lượt sinh 176 câu + 121 lần rerank sẽ vượt trần 0,10.

## 5. Bước chạy, tiền

*Ước* (K3 thật: token vào TB 4.013 / lần; G3):
- K3b-n ≈ 0,00040 + 0,00002 ≈ **0,00042 USD / lần**;
- K3b-m ≈ 0,00040 + 0,00021 ≈ **0,00061 USD / lần**.

| Bước | Gì | Lần gọi | Ước USD |
|---|---|---:|---:|
| 0 | M1, M2' (lượt none dev) | 0 | 0 |
| 1n | **Pilot K3b-n** 10 câu dev (seed 20261024 — cùng 10 câu pilot K3: 17, 22, 27, 29, 45, 48, 51, 89, 156, 169) | 10 | 0,004 |
| 2n | K3b-n L1 dev còn lại (30) | 30 | 0,013 |
| 3n | K3b-n L2 dev 40 | 40 | 0,017 |
| 4n | K3b-n test 15 (chỉ khi 1n–3n đạt) | 15 | 0,006 |
| 1m–4m | K3b-m như trên (chỉ khi K3b-n **kém hơn / chưa rõ**; pilot 10 trước) | 95 | 0,058 |
| | **Cộng nếu chạy hết hai nhánh** | 190 | **≈ 0,098** |
| | K3b-n tốt hơn (tạm) ⇒ bỏ K3b-m | 95 | ≈ 0,040 |

**Trần đề xuất (A chốt khi duyệt): 0,10 USD cho cả K3b** (trần con K3b-n 0,045, K3b-m 0,055). Trần 8.2: 0,5. Đã dùng trước plan này:
- 0,0396 (B1 + R2);
- 0,0251 (K3);
- R1 chưa chạy.

## 6. Dừng

1. M1 / M2' lệch ⇒ dừng.
2. Pilot mỗi nhánh:
   - USD / lần × số lần còn lại vượt trần con ⇒ dừng, báo A;
   - USD / lần > 1,5 × ước ⇒ dừng, báo A;
   - `rerank_ms` p95 > 15 s ⇒ dừng;
   - sai hợp đồng ≥ 3 / 10 ⇒ dừng nhánh, báo A (chữ prompt không hợp với model; hợp đồng thành cơ chế chính, không còn là ngoại lệ).
   - Trong lượt, khi đếm cộng dồn của nhánh đã vượt trần §2 / §4 (sai hợp đồng > 4) ⇒ nhánh **kém hơn**, dừng nhánh.
3. Lỗi kỹ thuật ≥ 1 ⇒ dừng nhánh, ghi nguyên văn; không gọi lại. Nhánh còn lại vẫn chạy theo luật thứ tự §1.
4. Mất ≥ 1 câu (L1 / L2 / test) ⇒ nhánh đó **kém hơn**, dừng nhánh.
5. Chỉ số quyết trượt sau L2 ⇒ nhánh đó **chưa rõ**, không chạy test nhánh đó.
6. Đổi chữ prompt, hợp đồng §2 hay mức suy luận sau khi thấy số = biến thể mới, cần plan mới (`run-experiment` §4). Tính từ K3, đây là
   vòng 2 / 3.
7. Không ghi Qdrant, không sửa corpus / Golden / split / đoạn đúng, không mở câu kín, không đọc câu test theo từng câu.

## 7. Đầu ra

`phase_8_2_k3b_implementation.md` trên nhánh `p82-k3b` (B commit + push, lệnh push riêng — W22) ⇒ C review. Report gồm:
- M1 / M2';
- pilot từng nhánh;
- L1 / L2 / test: thắng / thua theo `case_index`, nhiễu L1 ↔ L2;
- tỉ lệ sai hợp đồng (CI, theo dạng);
- giá: `rerank_ms` p50 / p95 kèm CI, tìm đầu–cuối, USD / câu đầu–cuối;
- bảng so K3 trên cùng câu;
- kết luận từng nhánh;
- 3–5 dòng lời thường cho User.

Dữ liệu `data/phase_8_2/k3b/`.

## 8. Câu hỏi cho A (trả lời khi duyệt)

1. **Tách hai nhánh n / m** — A trả lời sau C50: đồng ý tách, n trước, m chỉ khi n kém hơn / chưa rõ (§1).
2. **Trần 0,10 USD** (con 0,045 / 0,055).
3. **Quyền:** nhánh `p82-k3b` (tạo + commit + push, không merge), worktree `/tmp/b_k3b`, paid `gpt-6-luna` trong trần mục 2.
4. **Chỉ số quyết `context_gold_all`** thay `top10_gold_all` của K3 (A nêu cả hai). Ở mốc hai chỉ số trùng 40 / 40. `context` là đoạn thật sự đưa
   model, sát mục tiêu cuối hơn. `top10` để theo dõi.

## Sửa sau review C50 (09:22 27/10/2026 +0700, `date`)

| Finding / quyết định A | Sửa |
|---|---|
| m-1 tiêu đề §2 mâu thuẫn; nới sàn K3 không nói thẳng | Tiêu đề §2 "có đếm, có trần"; thêm đoạn "Đổi so với K3 — nói thẳng" (sàn "không phải hoán vị" ⇒ mức tụt có trần; lý do; kết luận K3 không đổi; lỗi kỹ thuật vẫn sàn 0) |
| m-2 phương án "nguyên RRF" | **Chọn "nguyên top-10 RRF" khi sai hợp đồng** (đơn giản hơn, tác hại chặn bằng mốc, tác động tương đương ở trần ≤ 4); bỏ bước (a)–(d) và trần riêng của bước bù |
| m-3 trần đếm tuyệt đối hay tỉ lệ | "≤ 4 lần, số đếm tuyệt đối cộng dồn trong nhánh, bất kể n" (§2, §4, §6.2) |
| m-4 + A (2) luật chạy nhánh m | K3b-m chỉ chạy khi K3b-n kém hơn / chưa rõ; ghi ước latency K3b-m ≈ K3 (5,6 s), K3b-n ≈ 2,1 s (*suy ra*, C50); §1 "Vì sao không gộp" bỏ lý do "dưới trần" cho khớp |

Không đổi: chỉ số quyết `context_gold_all`, luật thắng / thua hai lượt, Holm họ 4, sàn mất đoạn đúng, sàn lỗi kỹ thuật, prompt rerank, trần 0,10 USD,
điều kiện dừng khác.
