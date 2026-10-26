# Plan: Phase 8.2 §10 — K3, `gpt-6-luna` xếp lại pool 30 → top-10 (nhánh khâu tìm)

Người viết: B (Claude Opus 5.5, `hue-rag-23`) · 2026-10-26 22:08 +0700 (`date`) · Việc: B50 (A giao 22:2x) · Trạng thái: **bản nháp chờ C review**,
rồi A ghi "duyệt bản sha" (`WORKFLOW.md` §9.1). **Chưa code, chưa gọi API; 0 USD lúc viết.**

## Căn cứ để review

1. `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` **§10.2–§10.4** (bản A duyệt `cd910c4c4169`, commit `ce8b310`): luật (i),
   "chất lượng trước", "đo tốc độ theo khâu", sàn, Holm {K1, K3}, dòng K3 bảng §10.3, tiền.
2. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_k1_implementation.md` **§4–§5** (trên nhánh `p82-k1`, `870a5d5`): mốc M1 / M2, K1 kém hơn,
   pool 30 đủ đoạn đúng 31 / 40, câu 154 ở hạng 10.
3. `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g4_implementation.md` **§4.2, §5** và `backend/experiments/phase_8_1/g4_rerank.py`
   **dòng 63–96** (`LUNA_INSTRUCTIONS`, `luna_rank`): luna listwise top-10 8.1 — số đo, token, lỗi đầu ra.
4. `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_B.md` **§3.4** (nhóm "trong pool 30 nhưng ngoài top-10").

Người review được chạy lệnh chỉ đọc và tính lại từ `data/phase_8_1/g4/a_luna_plain*.jsonl`, `data/phase_8_2/k1/base_dev.jsonl`,
`data/cai_tien_tung_khau_2026-10-26/b42_per_case.jsonl`.

## 1. Câu hỏi và giả định

- **Lớp bài toán:** ở mốc context 10, 9 câu dev có đủ đoạn đúng trong pool 30 nhưng RRF không xếp được vào top-10. K1 cho thấy mở rộng pool
  không giải được: pool 100 có đủ đoạn đúng ở 37 / 40 câu nhưng top-10 chỉ 23 / 40. **Chỗ nghẽn là xếp hạng.**
- **K3 đổi đúng một thứ:** sau RRF (pool 30, giữ nguyên `dense_bm25_rrf`, RRF k 60), cho `gpt-6-luna` xếp lại **cả 30 đoạn**. Lấy 10 đoạn
  đầu làm top-10 đưa context builder.
  - Dùng lại nguyên `g4_rerank.luna_rank` + `LUNA_INSTRUCTIONS`: cùng model, cùng đầu ra có cấu trúc, `store=False`, không gửi reasoning, `max_output_tokens` = **2048**
    (`answer_max_output_tokens` ở `811d25d`, như 8.1; C review m-1)
    (giống runtime).
  - Các đoạn đưa vào theo **thứ tự RRF** (như 8.1).
- **Vì sao không dùng số 8.1:** 8.1 cho luna xếp lại **top-10**, tức chỉ đổi thứ tự trong cùng 10 đoạn. Ở mốc context 10 việc đó không đổi
  tập đoạn đưa model (B43 §1). K3 chọn 10 từ 30 nên tập đoạn mới đổi.
- **Giả định đã kiểm bằng máy:**
  - Trần dev **9 câu** (17, 38, 48, 67, 70, 85, 156, 159, 167). Đây là câu mà mọi fact đang thiếu ở context 10 đều nằm trong pool 30
    (`b42_per_case.jsonl`). Trần test **3 / 8**.
  - Không thể cứu 8 câu có fact ngoài pool 30 (19, 22, 68, 92, 97, 113, 120, 168), cũng không cứu câu 143 (thước đo).
  - **Rủi ro sàn:** luna có thể bỏ ra ngoài top-10 một đoạn đúng mà RRF đang giữ. Câu 154 là ví dụ (đoạn đúng ở hạng 10, K1 đã làm rơi).
    Vì vậy sàn được đo trên **cả 22 câu đang đủ**.
- **Về "14 câu của K1"** (tin A 22:2x): 14 là khoảng cách ở **pool 100** (37 − 23). K3 theo spec §10.3 là pool 30, nên trần là 9.
  - Xếp lại pool 100 sẽ **đổi hai thứ** so với mốc (pool + rerank).
  - Pool 100 cũng tốn khoảng 3 lần token vào và chậm hơn.
  - **B đề xuất:** chạy K3 pool 30 trước. Nếu K3 thắng, "pool 100 + luna" là biến thể sau, cần plan riêng. **A chốt.**

## 2. Mốc

- Code mốc `811d25d` (context 10 + NFC). Harness chạy trên nhánh **`p82-k3`** tạo từ `811d25d`, worktree `/tmp/b_k3` (bẫy worktree:
  `Project_Status.md` §8).
- Kiểm mốc trước khi đo:
  - **M1:** T1 sha `cefb2d1ad609`.
  - **M2:** lượt "không rerank" của harness K3 trên dev 40 có đoạn đúng phải cho `top_chunk_ids` và `top10_gold_*` khớp từng câu với
    `data/phase_8_2/k1/base_dev.jsonl` (lượt mốc K1, tất định).
- Câu trả lời mốc: `data/phase_8_2/b1/b1_{dev,test}.jsonl`. Đầu vào model trùng `811d25d` (B41 T2). Mốc được chấm lại **cùng lượt mù** với K3.

## 3. Thay đổi code (chỉ harness)

- **Mới:** `backend/experiments/phase_8_2/k3.py` trên nhánh `p82-k3`.
  - Dùng lại `k1.py` (`retrieval_service`, `new_file`, `pooled_items` / `analyze` cùng khuôn) và `g4_rerank.luna_rank`.
  - **Đoạn đưa luna:** `trace.stages["rrf"]` của `service.search` (30 point id theo thứ tự RRF). Payload lấy qua
    `g1_retrieval.load_payloads`, dựng bằng `build_retrieved_document`.
  - **Lớp bọc retrieval cho lượt sinh:** `search()` trả `RetrievalResult` với `documents` = 10 đoạn luna chọn. Khuôn giống
    `g2_generate.DocOrderService`, nên `full_corpus_eval.answer_case` chạy nguyên.
  - Mỗi lần gọi luna ghi: `input_tokens`, `output_tokens`, `usd`, `rerank_ms`, `order`, `error`.
  - **Phát lại thứ tự đã ghi:** ở lượt sinh, câu đã có thứ tự luna từ lượt 1 tầng tìm thì **dùng lại thứ tự đó**, không gọi lại.
    `run-experiment` §3.5 cho phát lại đầu ra model đã ghi thật để đo khâu sau. Lượt sinh ghi rõ câu nào phát lại.
  - Mọi lệnh ghi đều từ chối ghi đè. Thư mục ghi: `data/phase_8_2/k3/`.
- **Không sửa:** production, `settings.yaml`, `g4_rerank.py`, `k1.py`. Kiểm đúng đường bằng M2 và lượt `--rerank none`.

## 4. Tiêu chí ghi trước

```yaml
experiment_id: p82_k3_luna_rerank_pool30
baseline: p82-b1 811d25d — dense_bm25_rrf pool 30, RRF k 60, không rerank, context 10, NFC
changed_variable: "xếp lại 30 đoạn sau RRF bằng gpt-6-luna listwise (g4_rerank.luna_rank), lấy 10 đầu"
unchanged: [corpus, chunker, e5-small, index, pool 30, rrf_k, context 10, prompt sinh, gpt-6-luna sinh, judge Claude]
data:
  dev: {gold: 40 câu / 101 fact, answer_main: 88}            # split e2b1788dfbbc, gold bab707b9ab22, realism 0b65d1c138d2
  test: {gold: 15, answer_main: 41}                         # test đã nhìn ở G1.6
noise_AA: "luna không tất định ⇒ tầng tìm chạy 2 lượt (L1, L2) trên dev 40; nhiễu = số câu đổi top10_gold_all giữa L1 và L2"
metrics:
  # tầng tìm
  - {name: top10_gold_all, set: dev 40, role: decide,
     rule: "thắng = câu mốc 0 → K3 1 ở CẢ L1 và L2; thua = mốc 1 → K3 0 ở ÍT NHẤT một lượt; paired bootstrap trên vector (thắng +1 / thua −1 / còn lại 0),
            CI 95% > 0, Holm họ {K1 (p 0,798), K3} ⇒ K3 cần p < 0,025 ⇔ ≥ 5 thắng / 0 thua"}
  - {name: câu mất đoạn đúng khỏi context 10, set: "dev 40 (L1 và L2) + test 15", role: floor, floor: 0}
  - {name: lỗi đầu ra luna (không phải hoán vị 1..30 / API lỗi / bị cắt), set: mọi lần gọi, role: floor, floor: 0}   # sàn "0 lỗi kỹ thuật"
  - {name: số câu đổi top10_gold_all giữa L1 và L2, role: watch}    # nhiễu A/A của luna
  - {name: top10_gold_frac, MRR@10 (keyword), số câu đổi tập top-10, 120 / 168, role: watch}
  # tầng trả lời — chỉ khi qua tầng tìm trên dev + test
  - {name: out_of_scope bị trả lời, set: 18, role: floor, floor: 0}
  - {name: lỗi kỹ thuật / 500, set: 176, role: floor, floor: 0}
  - {name: số câu Completeness tụt, set: "dev chính 88 / test chính 41", role: tolerance, max_worse: "4 / 6 (A/A + 3)"}
  - {name: số câu Accuracy tụt, set: "dev chính 88 / test chính 41", role: tolerance, max_worse: "4 / 5"}
  - {name: từ chối nhầm trong phạm vi, set: "dev chính / test chính", role: tolerance, max_worse: "+1 / +1"}
  - {name: lỗi citation v2 (tính lại cả hai lượt như k1.analyze), set: 176, role: tolerance, max_worse: "+2"}
  # tốc độ / tiền — luật (i): K3 THÊM một lần gọi API ⇒ biết trước là không đạt "không tốn thêm" ⇒ trình User kèm số (spec §10.2)
  - {name: rerank_ms mỗi câu (đo thật), role: watch, report: "p50 / p95 kèm CI; trần theo dõi 5 s p95 (spec §10.2)"}
  - {name: token ra luna (TB + max) mỗi lần gọi, role: watch, note: "8.1 top-10 max 541; chạm 2048 ⇒ status incomplete ⇒ lỗi luna ⇒ sàn"}
  - {name: độ trễ tìm đầu–cuối (retrieval + rerank), role: watch}
  - {name: USD / câu đầu–cuối (rerank + sinh, usage log), role: watch, report: "so mốc ≈ 0,000204"}
  - {name: output_tokens sinh / câu, role: tolerance, max_worse: "+20 % (khâu sinh, spec 'đo tốc độ theo khâu')"}
result: null
conclusion: null   # chất lượng: tốt hơn / không đổi / kém hơn / chưa rõ (tạm tới B0); tốc độ / tiền: số thật ⇒ A trình User
```

**Luật giữ:**
1. Dev L1 + L2: đạt sàn, và chỉ số quyết qua (≥ 5 thắng ổn định / 0 thua) ⇒ chạy test.
2. Test (một lượt): 0 câu mất / 15, 0 lỗi luna ⇒ chạy lượt sinh.
3. Lượt sinh: đạt sàn + mọi mức tụt trên dev chính **và** test chính ⇒ **"chất lượng tốt hơn (tạm)"**.

Vì K3 thêm một lần gọi API, kết luận cuối luôn là **"trình User kèm số tốc độ / tiền"**. Theo "chất lượng trước" (spec §10.2), nếu K3 thắng,
bước tiếp là tìm cách làm nhanh / rẻ hơn **trước khi** trình User đưa vào chatbot. Đó là việc riêng, không thuộc plan này.

**Cỡ mẫu:** trần 9 câu. Cần 5 / 0 ổn định qua hai lượt. 8.1 (luna top-10, 30 câu) cứu 3 / 3 câu cứu được và mất 0, nhưng ở đó tập đoạn không
đổi. **Ghi trước: "chưa rõ" có thể xảy ra**; đó vẫn là kết quả hợp lệ.

## 5. Bước chạy, tiền

Ước từ 8.1 (luna top-10, 30 lần gọi thật): 1.428 token vào, 301 token ra (gồm suy luận), 0,00029 USD / lần, `rerank_ms` p50 3,5 s / p95 ≈ 5,2 s,
0 / 30 lỗi đầu ra. Pool 30 gấp khoảng 3 lần số đoạn ⇒ *ước* khoảng 4.000 token vào và 350–600 token ra ⇒ **≈ 0,0006 USD / lần**, có thể
chậm 4–8 s. Hai số này **phải đo lại ở pilot**.

| Bước | Gì | Lần gọi luna | Lần gọi sinh | Ước USD |
|---|---|---:|---:|---:|
| 0 | M1, M2, lượt `--rerank none` | 0 | 0 | 0 |
| 1 | **Pilot** L1, 10 câu dev có đoạn đúng (seed 20261024) ⇒ đo USD / lần + `rerank_ms` thật ⇒ ước lại mọi bước sau | 10 | 0 | 0,006 |
| 2 | L1 phần dev còn lại (30) | 30 | 0 | 0,018 |
| 3 | L2 dev 40 (A/A) | 40 | 0 | 0,024 |
| 4 | Test 15, một lượt (chỉ khi bước 1–3 đạt) | 15 | 0 | 0,009 |
| 5 | Lượt sinh 176 câu: rerank mới cho 121 câu chưa có thứ tự + phát lại 55; sinh 176 (chỉ khi bước 4 đạt) | 121 | 176 | 0,073 + 0,040 |
| | **Cộng nếu chạy hết** | 216 | 176 | **≈ 0,17** |
| | Dừng sau bước 3 (chỉ số quyết trượt) | 80 | 0 | ≈ 0,05 |

**Trần (A chốt 22:1x):** **0,20 USD** cho cả K3, gồm hai trần con: tầng tìm (bước 1–4) ≤ 0,06; lượt sinh (bước 5) ≤ 0,14. Mức A gợi ý (0,15)
**không đủ** nếu K3 qua hết các bước; nếu A giữ 0,15 thì bước 5 phải bỏ phần test (56 câu) hoặc chờ A. **A chốt.** Trong trần 8.2 (0,5 USD).

Judge: sub-agent Claude, ghi model id, 0 USD.

## 6. Dừng

1. M1 / M2 lệch ⇒ dừng.
2. Pilot: USD / lần ước lại × số lần còn lại vượt trần con ⇒ dừng, báo A. Pilot `rerank_ms` p95 > 15 s ⇒ dừng, báo A (quá xa trần theo dõi 5 s).
3. Lỗi đầu ra luna ≥ 1 ⇒ dừng, ghi nguyên văn lỗi. Không gọi lại, không thay bằng thứ tự RRF (`luna_output_rule` 8.1).
4. Mất ≥ 1 câu ở L1 hoặc L2 ⇒ **kém hơn**, dừng.
5. Chỉ số quyết trượt sau L2 ⇒ **chưa rõ**, dừng (không chạy test, không lượt sinh).
6. Không ghi Qdrant, không sửa corpus / Golden / split / đoạn đúng, không mở câu kín.

## 7. A đã trả lời (22:1x, tin A)

1. **K3 = pool 30** (trần 9). "Pool 100 + luna" để plan riêng, chỉ khi K3 thắng. Con số "14 câu" trong tin giao việc là nhầm mức pool.
2. **Trần K3 0,20 USD**, gồm trần con tầng tìm (bước 1–4) 0,06 và lượt sinh (bước 5) 0,14. A chọn vì nguyên tắc chất lượng trước. Tổng 8.2
   dự kiến ≈ 0,41 < 0,5 USD.
3. **Đồng ý luật 2 lượt:** thắng phải ổn định cả 2 lượt; thua tính ở bất kỳ lượt nào.
4. Quyền (nhánh `p82-k3` tạo + commit + push, paid theo trần mục 2, sub-agent judge): A ghi khi duyệt sha, sau khi C review.

Câu hỏi gốc (giữ để đọc lý do):


1. K3 = **pool 30** theo spec (trần 9). Hay A muốn thêm "pool 100 + luna" (trần 14, đổi hai thứ, cần plan riêng)?
2. Trần tiền 0,20 USD (hai trần con), hay 0,15 kèm bỏ test ở bước 5?
3. Định nghĩa thắng / thua qua hai lượt (§4): thắng phải ổn định, thua tính ở bất kỳ lượt nào.
4. Quyền: nhánh `p82-k3` (tạo + commit + push, không merge), paid theo trần ở mục 2, sub-agent judge.

## 8. Đầu ra

`phase_8_2_k3_implementation.md`, gồm:
- M1 / M2;
- pilot (USD / lần, `rerank_ms` thật);
- L1 / L2 / test: câu thắng / thua theo `case_index`, nhiễu L1 ↔ L2;
- lượt sinh, nếu có;
- tốc độ: `rerank_ms` p50 / p95 kèm CI, độ trễ tìm đầu–cuối;
- tiền thật: USD / câu đầu–cuối;
- kết luận;
- 3–5 dòng lời thường cho User.

Dữ liệu ở `data/phase_8_2/k3/`. Nếu K3 không được nhận, report vẫn ghi đủ số.
