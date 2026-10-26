# Plan: Phase 8.2 §10 — K1, pool dense 30 → 100 (nhánh khâu tìm)

Người viết: B (Claude Opus 5.5, `hue-rag-23`) · 2026-10-26 21:4x +0700 · Việc: B46 vòng 2. Bản này thay `phase_8_2_k1_k2_plan.md`: K2 đã
**NOT RUN** theo spec mới. Trạng thái: **vòng 2 sau review C41** (`phase_8_2_k1_plan_review.md`, changes_requested 0 / 1 / 4 — sửa ở mục
"Sửa sau review C41" cuối file); C kiểm phần sửa, rồi A ghi "duyệt bản sha" (`WORKFLOW.md` §9.1). **Chưa chạy gì; 0 USD lúc viết.**

## Căn cứ để review

1. `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md` **§10.2–§10.4**: mốc, luật (i), mức tụt, sàn, Holm, cỡ mẫu, tiền,
   dừng. Bản **A đã duyệt** sha `09e8f3932ede` (commit `a5cace6`). Spec đổi thì plan này phải đối chiếu lại.
2. `report_agent/2026-10-26_cai_tien_tung_khau/phan_loai_loi_B.md` **§2, §3.2, §3.4**: định nghĩa trúng / mất, nhóm câu, hạng dense.
3. `backend/experiments/phase_8_1/g1_retrieval.py` **dòng 161–222, 243–268**: `run_config`, `compare` — harness dùng lại.
4. `report_agent/2026-10-25_phase_8_2_ap_dung/phase_8_2_b1_implementation.md` **§4** (trên nhánh `p82-b1`): A/A context 10, tiền một lượt
   sinh. A/A test chính tính thêm từ `data/phase_8_2/b1/judge/` (§4, bảng A/A).

Người review được chạy lệnh chỉ đọc và tính lại từ `data/phase_8_1/g1/runtime.jsonl` và `data/cai_tien_tung_khau_2026-10-26/b42_per_case.jsonl`.

## 1. Câu hỏi và giả định

- **Lớp bài toán:** ở mốc context 10, 8 câu dev có fact mà đoạn đúng nằm ngoài pool 30 của dense (11 fact, B42 §3.2). Runtime chỉ cho
  BM25 xếp lại đúng pool đó.
- **K1 đổi đúng một thứ:** `candidate_pool` 30 → 100. Giữ treatment `dense_bm25_rrf` (BM25 chỉ xếp lại trong pool) và RRF k 60.
  - `candidate_pool` vừa là số ứng viên dense, vừa là số giữ lại sau RRF (`retrieval/full_corpus.py:406` ở `811d25d`).
  - Context vẫn lấy `fused[:10]` (`:602`).
- **Giả định đã kiểm bằng máy** (`b42_per_case.jsonl` sha `79e4ba43b38e`):
  - 9 / 11 fact ngoài pool có hạng dense ≤ 100.
  - **Trần dev 6 câu** (19, 22, 92, 97, 113, 168). Trong đó 19 và 168 còn một fact bị xếp sau ⇒ thực tế khoảng 4 câu.
  - Trần test 2 / 8.
- **Rủi ro chính:** BM25 chấm thêm 70 đoạn có thể đẩy đoạn đúng của câu đang đủ ra ngoài top-10. Đã thấy ở G1.3: native p100 mất 1 câu.
  Sàn ở §4 chặn trường hợp này.

## 2. Mốc (§10.2)

- Code mốc: nhánh `p82-b1` **`811d25d`** (context 10 + NFC). Chạy trong worktree `/tmp/b_k1` trên nhánh mới **`p82-k1`** tạo từ `811d25d`.
  Bẫy worktree: `Project_Status.md` §8 (`uv run --project /home/minhhieu/hue_rag`; symlink `data/` + `knowledge-base-hue/` gỡ khi xong).
- **Kiểm mốc trước khi đo** (khác thì dừng):
  - **(M1)** `evaluation.full_corpus_eval retrieval` ⇒ sha **`cefb2d1ad609`**.
  - **(M2)** lượt mốc của harness mới (pool 30) trên dev: `top_chunk_ids`, `pool_*_gold_*`, `top10_gold_*` khớp từng câu với
    `data/phase_8_1/g1/runtime.jsonl` (108 / 108).
- **Bẫy tên cột:** trên `811d25d` context builder lấy 10 đoạn, nên cột `context5_gold_*` của harness G1 thật ra là **context 10**. Không so
  cột này với file G1 cũ. Chỉ số quyết dùng `top10_gold_all`; ở context 10 hai cột bằng nhau, vì mọi câu đóng đủ 10 đoạn (B42).
- Câu trả lời mốc: `data/phase_8_2/b1/b1_{dev,test}.jsonl` (lượt B1, code trước rebase). Đầu vào model giống từng byte với code `811d25d`
  ở 176 / 176 câu (B41 T2) ⇒ dùng lại làm mốc tầng trả lời. Mốc vẫn được **chấm lại cùng lượt mù** với K1.

## 3. Thay đổi code (chỉ harness)

- **Mới:** `backend/experiments/phase_8_2/k1.py` trên nhánh `p82-k1`. Lý do không chạy thẳng `g1_retrieval run`: lệnh đó ghi
  `data/phase_8_1/g1/<name>.jsonl` **không chặn ghi đè**, và không ghi tổng thời gian tìm. Các lệnh:
  - `retrieval --name --group --pool`: gọi `g1_retrieval.run_config(argparse.Namespace(...))` (treatment `dense_bm25_rrf`, RRF k 60); ghi
    `data/phase_8_2/k1/<name>.jsonl`; **từ chối ghi đè**.
  - `compare --a --b --metrics`: đọc `data/phase_8_2/k1/`, gọi `g1_retrieval.compare`; thêm đếm "câu mất" (mốc 1 → K1 0) và danh sách
    `case_index` thắng / thua; số câu đổi tập top-10; theo dõi 120 / 168.
  - `check-base --name`: M2 — so từng câu lượt mốc với G1 `runtime.jsonl` ở `top_chunk_ids`, `dense_chunk_ids`, `pool_*`, `top10_gold_*`.
  - `latency --name --runs 2`: hai service (pool 30 và 100) dựng một lần, mỗi cái bỏ 1 câu khởi động; đo xen kẽ base → k1 → base → k1;
    ghi `trace.timings_ms["total_ms"]` từng câu (`retrieval/full_corpus.py:606` ở `811d25d`) cho 108 câu dev; in trung bình chênh theo câu,
    p50 / p95 mỗi cấu hình và nhiễu base lượt 2 − lượt 1.
  - `run` / `merge` / `export-judge` / `check-judge` / `analyze` như `phase_8_2/b1.py`. Khác ở chỗ retrieval dựng bằng
    `build_full_corpus_retrieval_service(..., candidate_pool=100)`; context, prompt, generator dùng code production
    (`full_corpus_eval.answer_case`, `build_context_builder(settings)`). Câu trả lời gộp ra `k1_{dev,test}.answers.jsonl` (khác tên file
    retrieval). Lô chấm mù gộp câu trả lời mốc B1 với câu trả lời K1. `analyze` tính lỗi citation v2 lại cho **cả hai** lượt bằng cùng hàm
    (lượt B1 sinh trước validator v2 — cách của gói 3c).
  - Dùng lại: `b1.read_jsonl / write_jsonl / paired`, `g2_generate.select / usage / write_batches / read_scores`, `bootstrap_mean_diff`.
- **Không sửa:** production, `settings.yaml`, `g1_retrieval.py`, `b1.py`. Không thêm test cho harness (`Session_Prompt.md` §8); đường đúng
  kiểm bằng M1–M2.

## 4. Tiêu chí ghi trước

```yaml
experiment_id: p82_k1_dense_pool100
baseline: p82-b1 811d25d — dense_bm25_rrf, candidate_pool 30, rrf_k 60, context 10, NFC (T1 cefb2d1ad609)
changed_variable: candidate_pool 30 → 100
unchanged: [corpus, chunker, e5-small, index, sparse state, treatment, rrf_k, context 10, prompt, gpt-6-luna, judge Claude]
data:
  dev: {gold: 40 câu / 101 fact, keyword: 108, answer_main: 88}   # split.json e2b1788dfbbc, gold bab707b9ab22, realism 0b65d1c138d2
  test: {gold: 15, keyword: 50, answer_main: 41}                 # test chính = test, bỏ unnatural, trong phạm vi; đã nhìn ở G1.6 — giới hạn ghi sẵn
metrics:
  # tầng tìm (0 USD)
  - {name: top10_gold_all, fn: g1_retrieval.gold_coverage, set: dev 40, better: up, role: decide,
     rule: "paired bootstrap (bootstrap_mean_diff, 10.000, seed 20261024), CI 95% > 0, Holm họ nhánh tìm {K1, K3 nếu chạy}", noise: 0 (tất định)}
  - {name: câu mất đoạn đúng khỏi context 10, def: "top10_gold_all mốc 1 → K1 0", set: dev 40 + test 15, role: floor, floor: 0}
  - {name: latency tìm, def: "TRUNG BÌNH chênh theo câu (K1 − mốc) của total_ms trung bình 2 lượt, 108 câu dev, CPU; mốc và K1 đo cùng phiên, xen kẽ base → k1 → base → k1", role: tolerance, max_worse: "+50 ms",
     noise: "chênh base lượt 2 − base lượt 1 (cùng phiên) — ghi trong report"}
  - {name: số câu đổi tập top-10 so với mốc, set: dev 108 / test 50, role: watch}
  - {name: top10_gold_frac, keyword_coverage, MRR@10, nDCG@10, latency p95 (K1 và chênh), role: watch}
  # tầng trả lời — chỉ khi qua tầng tìm trên dev + test
  - {name: out_of_scope bị trả lời, set: 18 (dev 12 + test 6), role: floor, floor: 0}
  - {name: lỗi kỹ thuật / 500, set: 176, role: floor, floor: 0}
  - {name: số câu Completeness tụt, set: dev chính 88, role: tolerance, max_worse: "≤ A/A + 3 = 4"}
  - {name: số câu Accuracy tụt, set: dev chính 88, role: tolerance, max_worse: "≤ A/A + 3 = 4"}
  - {name: từ chối nhầm trong phạm vi, set: dev chính 88, role: tolerance, max_worse: "tăng ≤ A/A + 1 = 1 câu"}
  - {name: số câu Completeness tụt, set: test chính 41, role: tolerance, max_worse: "≤ A/A + 3 = 6"}
  - {name: số câu Accuracy tụt, set: test chính 41, role: tolerance, max_worse: "≤ A/A + 3 = 5"}
  - {name: từ chối nhầm trong phạm vi, set: test chính 41, role: tolerance, max_worse: "tăng ≤ A/A + 1 = 1 câu"}
  - {name: lỗi citation (validator v2), set: 176, role: tolerance, max_worse: "tăng ≤ 2 câu"}
  - {name: USD / câu (usage log), role: tolerance, max_worse: "+20 %; 0 lần gọi API thêm"}
  - {name: Completeness / Accuracy / Relevance chênh TB (dev chính, test chính), role: watch}
  - {name: 120 / 168 trả lời hay từ chối + context có fact không (top10_gold_frac), role: watch}   # A 21:4x: sàn 120 / 168 chỉ của khâu trả lời
result: null
conclusion: null   # tốt hơn / không đổi / kém hơn / chưa rõ / NOT RUN — dựa judge ⇒ TẠM tới khi B0 xong (§10.2)
```

**A/A ghi trước** (lượt B1 ↔ G2.1a, cùng đầu vào từng token, chấm cùng lượt mù `data/phase_8_2/b1/judge/`; B tính 21:4x bằng `b1.scored_rows` +
`b1.paired`, 0 USD). A/A không có chiều, nên "A/A tụt" = số câu đổi điểm theo chiều nhiều hơn (thắng / hòa / thua của B1 − G2.1a):

| Tập | n | Completeness | Accuracy | Relevance | câu đổi từ chối ↔ trả lời | A/A tụt (C / A) |
|---|---|---|---|---|---|---|
| dev chính | 88 | 1 / 86 / 1 | 1 / 86 / 1 | 1 / 84 / 3 | 0 | 1 / 1 |
| test chính | 41 | 3 / 38 / 0 | 2 / 38 / 1 | 2 / 37 / 2 | 0 | 3 / 2 |

**Luật giữ** (§10.2 luật (i), `run-experiment` §4):
1. Dev tầng tìm: sàn + latency + chỉ số quyết qua Holm ⇒ chạy test tầng tìm.
2. Test: 0 câu mất / 15 ("không làm hỏng"; lệch `run-experiment` §4, chờ User — §10.6 Q2) ⇒ chạy lượt sinh.
3. Lượt sinh: đạt sàn + mọi mức tụt trên **dev chính và test chính** ⇒ **"tốt hơn" (tạm)**, đề xuất A.

Phần "không tốn thêm tiền": K1 không thêm lần gọi API, vẫn 10 đoạn ⇒ USD / câu gần như không đổi. Ghi số thật để chắc.

**Cỡ mẫu (theo §10.3, C38 M-1):**
- Trên 40 câu: 4 thắng / 0 thua cho p 0,026, nên trượt ngưỡng đầu của Holm họ 2 (0,025); 5 / 0 cho p 0,008 thì qua.
  ⇒ **K1 cần ≥ 5 / 0**. Trần 6 câu, thực tế khoảng 4 ⇒ **ghi trước: "chưa rõ" rất có thể**. Đó vẫn là kết quả hợp lệ.
- Ngưỡng 5 / 0 áp **dù K3 có chạy hay không**. Lý do: lúc quyết K1 chưa biết K3 có chạy không, mà chọn họ sau khi thấy số thì sai luật.
  A xác nhận cách đọc này.

## 5. Lệnh (từ `/tmp/b_k1/backend`; tiền tố `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m`)

| Bước | Lệnh | Tiền |
|---|---|---|
| M1 | `evaluation.full_corpus_eval retrieval --out /home/minhhieu/hue_rag/data/phase_8_2/k1/m1_t1.jsonl` + `sha256sum` | 0 |
| M2 | `experiments.phase_8_2.k1 retrieval --name base_dev --group dev --pool 30` ⇒ `… k1 check-base --name base_dev` (phải 0 trường lệch) | 0 |
| K1 dev | `… k1 retrieval --name k1_dev --group dev --pool 100` | 0 |
| So | `… k1 compare --a base_dev --b k1_dev --metrics top10_gold_all top10_gold_frac keyword_coverage mrr ndcg` | 0 |
| Latency | `… k1 latency --name lat_dev --runs 2` (xen kẽ base → k1 → base → k1, cùng phiên, dev 108) | 0 |
| Test | `… k1 retrieval --group test` cho `base_test`, `k1_test` + `compare` (chỉ đếm câu mất) | 0 |
| Pilot sinh | `--env-file ../.env … k1 run --cases pilot --name k1_pilot` (10 câu) | ≈ 0,002 |
| Sinh | `run` rest / test_pilot / test_rest ⇒ `merge` ⇒ `export-judge` ⇒ sub-agent judge Claude (ghi model id) ⇒ `check-judge` ⇒ `analyze` | ≈ 0,034 |

**Ước tiền:** tầng tìm 0. Lượt sinh 176 × ~0,000204 ≈ **0,036 USD** (B1 thật 0,0369). Judge: quota Claude. **Trần 0,04 USD** (A).

## 6. Dừng

1. M1 / M2 lệch mốc ⇒ dừng, báo A.
2. K1 mất ≥ 1 câu ở dev ⇒ **kém hơn**; không chạy test, không lượt sinh.
3. Chỉ số quyết trượt (CI chứa 0, hoặc < 5 / 0) ⇒ **chưa rõ**; ghi đủ số; không lượt sinh (§10.2: qua tầng tìm mới sinh).
4. Latency > +50 ms ⇒ không nhận theo luật (i); A trình User kèm số nếu chất lượng tăng.
5. Pilot vượt ước > 50 % hoặc tổng sắp vượt 0,04 USD ⇒ dừng, báo A. Lỗi kỹ thuật > 0 ⇒ dừng, tìm nguyên nhân (không fallback).
6. Không ghi Qdrant (chỉ `query_points`); không sửa corpus / Golden / split / đoạn đúng; không mở câu kín.

## 7. A đã trả lời (21:4x, `CURRENT_HANDOFF.md` dòng C41)

1. Sàn 120 / 168 chỉ áp cho khâu trả lời; với K1 chỉ **theo dõi** (dòng watch trong YAML).
2. Ngưỡng 5 / 0 **cố định**.
3. Quyền (nhánh `p82-k1`, paid ≤ 0,04 USD, sub-agent judge) A ghi khi duyệt sha.

Nội dung câu hỏi gốc (giữ để đọc lý do):

- **Sàn "120, 168 vẫn từ chối"** (§10.2) ghi cho khâu trả lời. Với K1 thì sàn này không hợp: câu 168 nằm trong trần K1 (K1 có thể đưa fact
  vào context, khi đó trả lời là **đúng**). B đề xuất: với K1, **không** áp sàn này. Thay vào đó, ghi 120 / 168 trả lời hay từ chối và
  context có fact hay không, làm chỉ số theo dõi.
- Ngưỡng 5 / 0 áp cố định (§4).
- Quyền: tạo + commit + push nhánh `p82-k1` (không merge); paid `gpt-6-luna` trần 0,04 USD cho lượt sinh K1; sub-agent judge Claude.

## 8. Đầu ra

`phase_8_2_k1_implementation.md`, gồm:
- M1–M2;
- tầng tìm dev / test: bảng theo §4, câu thắng / thua theo `case_index`;
- latency;
- lượt sinh, nếu có;
- tiền thật;
- kết luận;
- 3–5 dòng lời thường cho User.

Dữ liệu ở `data/phase_8_2/k1/`. Nếu K1 không được nhận, report vẫn ghi đủ số (`run-experiment` §5).

## Sửa sau review C41 (B, 2026-10-26 21:42 +0700, `date`)

| Finding | Sửa |
|---|---|
| M-1 mức tụt test | YAML thêm 3 dòng `test chính 41` (Completeness ≤ 6, Accuracy ≤ 5, từ chối nhầm ≤ +1); bảng A/A dev + test ghi trước (§4); luật giữ bước 3 "dev chính **và** test chính" |
| m-1 sha spec | Căn cứ 1 trỏ bản duyệt `09e8f3932ede` (`a5cace6`) |
| m-2 trả lời §7 | §7 ghi 3 ý A đã trả lời; YAML thêm dòng theo dõi 120 / 168 |
| m-3 latency | tolerance = **trung bình** chênh theo câu ≤ +50 ms; p95 theo dõi; nhiễu = base lượt 2 − lượt 1 cùng phiên |
| m-4 tập top-10 | YAML thêm dòng theo dõi "số câu đổi tập top-10" (dev 108 / test 50); `compare` in số này |
| (B tự thêm) | §3 / §5 khớp `k1.py` đã viết trên nhánh `p82-k1` (chưa commit, chưa chạy): lệnh `check-base` cho M2; `latency --name --runs`; file câu trả lời `.answers.jsonl` |

