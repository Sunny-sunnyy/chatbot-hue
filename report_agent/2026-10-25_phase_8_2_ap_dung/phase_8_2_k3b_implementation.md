# Implementation Report: Phase 8.2 §10 K3b — `gpt-6-luna` chọn 10 từ 30 đoạn RRF — nhánh n kém hơn (lỗi kỹ thuật), nhánh m tầng tìm tốt hơn (tạm)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-31`) · 2026-10-27 09:58 +0700 (`date`) · Việc: B56 (plan) → B59 (chạy). A giao 27/10; User duyệt quyền
phiên 08:47 27/10.
Plan A duyệt: `phase_8_2_k3b_plan.md` bản 2 sha **`57dad7150322`** (commit `765f45a`; B tính lại từ file trước khi chạy: khớp). Spec §10 bản `cd910c4c4169`.
Code: nhánh `p82-k3b` = `80e7329` (`p82-k3`, A chấp nhận gốc này thay `811d25d`) + `7c0467d` (harness + test) + `f4d3225` (sửa bắt lỗi + ghi từng dòng).
**Tiền:**
- log: **0,0592176 USD** (nhánh m 0,055714 + pilot n 0,0035036);
- ước: **+ ≈ 0,0074 USD** (lượt n bị mất usage, cận trên 0,0105).

⇒ **≈ 0,067 USD (≤ 0,070)** / trần 0,10.

Trạng thái: **chờ review** (C).

## Cho bạn — lời thường

1. Mình thử lại cách "nhờ model AI chọn 10 đoạn tốt nhất trong 30 đoạn tìm được". Lần này model chỉ cần trả 10 số thay vì 30, và có luật ghi sẵn
   cho trường hợp trả sai.
2. Bản **không cho model suy nghĩ trước** (nhanh: chờ thêm khoảng 1,8 giây) bị dừng. Có một lần model viết thêm chữ sau kết quả, nên máy không đọc được.
   Theo luật, đó là lỗi kỹ thuật, nên bản này **kém hơn**.
3. Bản **cho model suy nghĩ như bình thường** đạt ở bước tìm:
   - nhóm thử: cứu được **cả 9 / 9 câu** có thể cứu, **lặp lại y hệt ở lần chạy thứ hai**, và không làm mất câu nào;
   - nhóm kiểm: cứu **3 / 3**, không mất câu nào;
   - 95 lần gọi, không lần nào trả sai.

   Số câu mà chatbot nhận đủ đoạn đúng tăng từ **22 lên 31 trên 40** câu thử.
4. Cái giá của bản này:
   - mỗi câu **chờ thêm khoảng 5 giây** (có lúc 7 giây);
   - tiền một câu **gấp khoảng 3,9 lần** (≈ 0,0008 USD, khoảng 20 đồng, so với ≈ 0,0002 USD);
   - **chưa đo câu trả lời cuối cùng** (lượt sinh + chấm điểm), vì việc đó cần trần tiền riêng.

   Bạn sẽ được hỏi có chấp nhận mức chờ / tiền này không, sau khi đo câu trả lời.
5. Có một sự cố do code thí nghiệm của mình: khi bản nhanh lỗi, mình mất số token của một lượt. Tiền lượt đó là **ước** (khoảng 0,0074 USD). Mình
   đã sửa code để không mất số liệu nữa.

## 1. Phạm vi

Làm theo plan §5, các bước sau.

**Bước 0 (0 USD):**
- M1;
- M2' (dev), so với K3: 40 / 40 khớp;
- `--arm none` test: 15 / 15 khớp.

**Nhánh n (`reasoning={"effort": "none"}`):**
- pilot 10 câu: đạt mọi điều kiện;
- L1 phần còn lại: **lỗi kỹ thuật** ⇒ nhánh n dừng (plan §6.3);
- NOT RUN: L2, test.

**Nhánh m (không gửi reasoning):** chạy vì nhánh n kém hơn (plan §1, A chốt).
- pilot 10;
- L1 phần còn lại 30;
- L2 40;
- test 15.

**NOT RUN cả plan:** lượt sinh + judge. Theo plan §4, phần này để ngoài plan, cần phụ lục và trần riêng.

Không đổi production, không ghi Qdrant, không mở câu kín, không đọc câu test theo từng câu.

## 2. Thay đổi

- `backend/experiments/phase_8_2/k3b.py` (`7c0467d`, sửa ở `f4d3225`; sha hiện tại `658e381c8c37`):
  - `luna_top10`: prompt plan §1, sha 12 `4717583a1489` (ghi trong `.meta.json`). Đầu ra `{"order": list[int]}`, `store=False`, 2048 token ra.
    Nhánh n gửi `reasoning={"effort": "none"}`; nhánh m không gửi.
  - `apply_contract` (plan §2 bản 2): đúng 10 số khác nhau trong 1..30 ⇒ dùng thứ tự luna; sai ⇒ câu đó dùng nguyên top-10 RRF. Đếm từng dạng.
    Trần 4 lần / nhánh, số đếm tuyệt đối cộng dồn qua các lượt.
  - Vòng lặp tầng tìm giống `k3.retrieval`; import `gold_cases`, `new_file`, `POOL`, `TOP_K` từ `k3.py`.
  - `compare`: luật hai lượt trên `context_gold_all`, Holm họ cố định {K1 0,798, K3 1, nhánh này, nhánh kia}, mức tụt hợp đồng + CI
    Clopper–Pearson.
  - `check-base`, `merge`. Bản gộp `*.merged.jsonl` bỏ trường `arm` để không đếm hai lần.
- `backend/tests/test_k3b_contract.py` (mới): 4 test cho hợp đồng (đúng / thiếu / thừa / lặp / ngoài khoảng) và CI 1 / 40 (khớp số scipy của
  report K3). **4 passed.**
- **Sửa `f4d3225` sau sự cố** (A duyệt 09:3x, không đổi tiêu chí):
  - (a) bắt `pydantic.ValidationError` của `responses.parse` ⇒ lỗi kỹ thuật kèm raw, đúng phân loại plan §2 loại 1, ghi `usage_unknown`;
  - (b) ghi từng dòng ngay sau mỗi câu, luôn ghi `.meta.json`, kể cả khi lượt dừng vì exception (`crashed`).

## 3. Cách đã chạy thật

Worktree `/tmp/b_k3b`, symlink `data/` + `knowledge-base-hue/` tạm. Từ `backend/`, Qdrant `:6335` chỉ đọc, e5-small CPU. Lệnh có phí dùng
`--env-file /home/minhhieu/hue_rag/.env`:

```bash
… -m evaluation.full_corpus_eval retrieval --out …/k3b/m1_t1.jsonl                       # M1
… -m experiments.phase_8_2.k3b retrieval --name base_dev  --cases dev  --arm none       # M2' (+ check-base)
… -m experiments.phase_8_2.k3b retrieval --name base_test --cases test --arm none       # (+ check-base --group test)
… -m experiments.phase_8_2.k3b retrieval --name n_l1_pilot --cases pilot --arm n        # 09:29:25–09:29:41
… -m experiments.phase_8_2.k3b retrieval --name n_l1_rest  --cases rest  --arm n        # 09:30:04–09:30:53, exception (harness 7c0467d)
… -m experiments.phase_8_2.k3b retrieval --name m_l1_pilot --cases pilot --arm m        # 09:35:46–09:36:38 (harness f4d3225 từ đây)
… -m experiments.phase_8_2.k3b retrieval --name m_l1_rest  --cases rest  --arm m        # 09:37:11–09:39:33
… -m experiments.phase_8_2.k3b merge --parts m_l1_pilot m_l1_rest --name m_l1
… -m experiments.phase_8_2.k3b retrieval --name m_l2   --cases dev  --arm m             # 09:51:21–09:54:34
… -m experiments.phase_8_2.k3b retrieval --name m_test --cases test --arm m             # …–09:56:50
… -m experiments.phase_8_2.k3b compare --arm m --runs m_l1.merged m_l2 --other-arm-p 1.0   > …/k3b/compare_m_dev.json
… -m experiments.phase_8_2.k3b compare --arm m --runs m_test --group test                  > …/k3b/compare_m_test.json
PYTHONPATH=. uv run --project /home/minhhieu/hue_rag python ../data/phase_8_2/k3b/tools/k3b_watch.py                    # §4.4
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_k3b_contract.py -q
```

`--other-arm-p 1.0`: nhánh n dừng, không có p. Plan §4 ghi nhánh không có p thì lấy p = 1.

## 4. Kết quả quan sát

Dữ liệu private `data/phase_8_2/k3b/`, sha 12:

| File | sha |
|---|---|
| `m1_t1.jsonl` | `cefb2d1ad609` |
| `base_dev.jsonl` | `480cd80c8bd1` |
| `base_test.jsonl` | `20b90d6da6f0` |
| `n_l1_pilot.jsonl` | `cf0fb6903cdc` |
| `m_l1_pilot.jsonl` | `3f1a866ad88a` |
| `m_l1_rest.jsonl` | `0add44bf9552` |
| `m_l1.merged.jsonl` | `60db477951c9` |
| `m_l2.jsonl` | `03ec90bd33ea` |
| `m_test.jsonl` | `7e0287f9f576` |
| `tools/k3b_watch.py` | `426df5b68360` |

Mỗi lượt có kèm `.meta.json`, cùng `compare_m_{dev,test}.json`. **Không có file `n_l1_rest`** (§4.2).

### 4.1 Mốc

- M1: T1 `cefb2d1ad609` ✓.
- M2' dev: 40 / 40, 0 trường lệch (`top_chunk_ids`, `top10_gold_*`, `context_chunk_ids`, `context_gold_all`, `pool_gold_all`) so `k3/base_dev.jsonl` ✓.
- Test: 15 / 15, 0 lệch so `k3/base_test.jsonl` ✓.
- Mốc: `context_gold_all` dev 22 / 40, test 7 / 15. Trần dev 9, test 3. Context = top-10 ở mọi câu.

### 4.2 Nhánh n — kém hơn (phạm sàn lỗi kỹ thuật)

**Pilot `n_l1_pilot`** (10 câu dev): đạt mọi điều kiện dừng của plan §6.2.

| | Ước | Thật |
|---|---|---|
| USD / lần | 0,00042 | **0,000350** |
| `rerank_ms` p50 / p95 | — | **1.760 / 2.092 ms** |
| Token ra | — | 33 / lần |
| Lỗi kỹ thuật | — | 0 |
| Sai hợp đồng | — | 0 / 10 |

API nhận `reasoning none` qua `responses.parse` (giả định G2 ✓).

**L1 phần còn lại `n_l1_rest`: lỗi kỹ thuật.**
- Luna trả JSON đúng rồi **viết thêm chữ sau JSON**. Raw bị SDK cắt: `{"order":[8,2,11,23,1,3,... LunaTop10 format only.`
- SDK (openai 2.53.0) `responses.parse` ném `pydantic.ValidationError` ("Invalid JSON: trailing characters") thay vì trả `output_parsed` None.
- **Ghi chú (A hỏi):** `responses.parse(text_format=…)` gửi `text.format` = `json_schema` với **`strict: True`** (`openai/lib/_parsing/_responses.py`,
  `type_to_text_format_param`). Vậy chữ thừa xuất hiện **dù schema là strict**, ở `reasoning none`.
- Theo plan §2 loại 1 (parse hỏng), đây là lỗi kỹ thuật, sàn 0 ⇒ **nhánh n kém hơn**, dừng, không gọi lại (§6.3; A xác nhận 09:3x).

**Sự cố harness của B (`7c0467d`):**
- `luna_top10` chỉ bắt `OpenAIError`, nên exception làm cả lượt dừng.
- Harness chỉ ghi file ở cuối lượt, nên **mất mọi dòng của lượt này**: không có câu nào được ghi, không có usage, không biết lỗi ở câu nào.
- **Tiền lượt này là ƯỚC, không phải số log.**
  - Cách ước: process chạy 09:30:04 → crash 09:30:53, tức 49 s. Trừ ~10 s khởi động (như pilot), chia ~1,85 s / lần (pilot: TB `total_ms` 1.788 ms)
    ⇒ **≈ 21 lần × 0,000350 ≈ 0,0074 USD**.
  - Cận trên: đủ 30 lần ⇒ **0,0105 USD**.
- Sửa ở `f4d3225` (§2). A ghi sự cố vào sổ cải tiến.

### 4.3 Nhánh m — tầng tìm tốt hơn (tạm)

**Pilot `m_l1_pilot`:** đạt mọi điều kiện dừng của plan §6.2.

| | Ước | Thật |
|---|---|---|
| USD / lần | 0,00061 | 0,000512 |
| `rerank_ms` p50 / p95 | — | 5.280 / 8.705 ms |
| Lỗi kỹ thuật | — | 0 |
| Sai hợp đồng | — | 0 / 10 |

**Chỉ số quyết, dev 40** (`compare_m_dev.json`, L1 = `m_l1.merged`, L2 = `m_l2`):

| | Kết quả | Luật | |
|---|---|---|---|
| Thắng ổn định (mốc 0 → 1 ở cả L1, L2) | **9**: 17, 38, 48, 67, 70, 85, 156, 159, 167 (= cả 9 câu trần) | ≥ 5 | ✓ |
| Thua (mốc 1 → 0 ở bất kỳ lượt), context / top-10 | **0 / 0** | sàn 0 | ✓ |
| Bootstrap vector (+1 / −1 / 0) | TB +0,225, CI 95 % **[+0,10; +0,35]**, p bootstrap = 0 (không lần lấy mẫu nào ≤ 0) | CI > 0 | ✓ |
| p Holm họ {K1 0,798, K3 1, K3b-n 1, K3b-m} | **0** (4 × 0) | < 0,05 | ✓ |
| A/A L1 ↔ L2: câu đổi `context_gold_all` | **0** | theo dõi | — |
| `context_gold_all` | mốc 22 → L1 **31**, L2 **31** / 40 | | |

**Test 15** (`compare_m_test.json`, một lượt):

| | Kết quả | |
|---|---|---|
| Thắng | **3** (20, 95, 130 = cả 3 câu trần) | theo dõi |
| Mất (context / top-10) | **0 / 0** | sàn ✓ |
| Lỗi kỹ thuật | 0 | sàn ✓ |
| `context_gold_all` | 7 → 10 / 15 | |

**Mức tụt hợp đồng** (cộng dồn cả nhánh m, 95 lần gọi): **0 / 95** sai hợp đồng, CI 95 % Clopper–Pearson [0; 3,8 %]. Trần ≤ 4 ✓. Theo dạng:
sai độ dài 0, ngoài khoảng 0, lặp 0.

⇒ Theo luật giữ plan §4 bước 1–2: **nhánh m, tầng tìm "tốt hơn (tạm)"**. Kết luận dựa trên đoạn đúng do agent gắn, không phải judge.
Test chỉ là "không làm hỏng".

### 4.4 Giá và số theo dõi (đo thật; `k3b_watch.py`)

| | Mốc | K3b-m (95 lần) | K3b-n (pilot 10 lần) | K3 (40 lần, 26/10) |
|---|---:|---:|---:|---:|
| `rerank_ms` p50 [CI 95 %] | 0 | **5.021** [4.890; 5.445] | 1.760 [1.559; 1.913] | 5.613 |
| `rerank_ms` p95 [CI] | 0 | **7.007** [6.641; 7.873] | 2.092 [1.794; 2.140] | 8.565 |
| Tìm đầu–cuối p50 / p95 (ms) | 27 / 33 | 5.058 / 7.037 | 1.793 / 2.124 | 5.681 / 8.618 |
| Token luna vào TB / ra TB / ra max | — | 3.958 / 381 / 702 | 3.339 / 33 / 33 | 4.013 / 453 / 818 |
| USD / lần rerank | 0 | **0,000586** | 0,000350 | 0,000628 |
| USD / câu đầu–cuối (sinh = mốc B1 0,000204, **ước**) | 0,000204 | **≈ 0,00079 (3,9×)** | ≈ 0,00055 (2,7×) | ≈ 0,00083 (4,1×) |

- p95 nhánh m ≈ **7,0 s** vượt mức theo dõi 5 s (spec §10.2: theo dõi, không phải sàn).
- Pilot nhánh n đã có p95 ≈ 2,1 s, nhưng nhánh n đã dừng.
- CI là bootstrap trên các lần gọi, seed 20261024. Gọi tuần tự, trên máy User.

**So K3 trên cùng câu** (theo dõi):
- 39 câu K3 hợp lệ: `context_gold_all` K3 30, K3b-m L1 30, L2 30; câu khác nhau: **0**.
- 10 câu pilot: mốc 6, K3b-n 9, K3b-m 9, K3 9.

  ⇒ Trên các câu đo được, ba cách rerank cho **cùng** số đoạn đúng. *Suy ra*, chưa chứng minh: bản nhanh (n) có thể giữ cùng chất lượng nếu sửa được
  lỗi chữ thừa. Mới có 10 câu cho n.
- Ổn định giữa hai lượt m: tập top-10 giống nhau ở 15 / 40 câu, thứ tự giống ở 3 / 40. Nhưng `context_gold_all` không đổi ở 40 / 40 câu: luna đổi
  thứ tự / đoạn phụ, không đổi đoạn đúng.
- 120 / 168 (`top10_gold_frac`): 120 vẫn 0. 168 từ 0 lên 0,5 ở cả L1, L2, tức thêm 1 / 2 fact.

## 5. Kết luận theo tiêu chí ghi trước

- **K3b-n — kém hơn** (phạm sàn: lỗi kỹ thuật, chữ thừa sau JSON strict ở `reasoning none`). NOT RUN: L2, test.
- **K3b-m — tầng tìm tốt hơn (tạm):**
  - dev 9 thắng / 0 thua, ổn định qua hai lượt, p Holm ≈ 0 (bootstrap);
  - test 3 / 0 ("không làm hỏng");
  - sai hợp đồng 0 / 95.
- **Giá:** +5,0 s p50 / +7,0 s p95 mỗi câu; USD / câu ≈ 3,9×. Vì thêm một lần gọi API, kết luận cuối là **trình User kèm số** (spec §10.2, plan §4
  bước 3). Plan này không tự nhận.
- **NOT RUN:** lượt sinh + judge (plan §4). Chưa biết Completeness / Accuracy / từ chối nhầm có tăng tương ứng không. Ghi chú từ dữ liệu cũ:
  B42 đã thấy câu tự nhiên không lợi từ context 10. Vì vậy cần đo trước khi trình User.
- **Hướng mở** (B ghi, A quyết; *chưa đo*):
  - (1) phụ lục lượt sinh cho K3b-m. Tiêu chí giữ nguyên K3 plan §4; phát lại thứ tự m đã ghi cho 55 câu có đoạn đúng. Ước theo USD thật: rerank
    121 câu ≈ 0,071 + sinh 176 câu ≈ 0,036 ⇒ **≈ 0,11 USD**, cần trần riêng.
  - (2) "K3c": giữ tốc độ của n, xử lý chữ thừa sau JSON. Đây là biến thể mới, plan mới, vòng 3 / 3.

## 6. Lỗi và giới hạn

- Sự cố harness §4.2: tiền `n_l1_rest` là **ước**. Câu lỗi của nhánh n không xác định được (không có dòng).
- Trần con: nhánh m chạy tới 0,055714 USD, **vượt trần con ban đầu 0,055** khoảng 0,0007 USD. A dời phần dư trần con của n sang m (trần con m
  mới **0,065**, tổng K3b giữ ≤ 0,10). B nhận tin A lúc **09:51:39 27/10/2026** (`date`), trước khi chạy test (L2 bắt đầu 09:51:21). Lý do: n dừng
  sớm, chỉ dùng ≤ 0,014 / 0,045.
- 9 câu trần được chọn trên chính dev (B42), nên test là phép xác nhận "không làm hỏng", và chỉ có một lượt.
- Đoạn đúng do agent gắn, agent khác kiểm, User duyệt ~10 câu (spec §10.5).
- Latency đo tuần tự trên máy User. Production gọi đồng thời có thể khác. Retrieval ms các lượt luna (p50 28, p95 57) chạy khác lúc mốc, không xen kẽ.
- Nhánh n mới có 10 câu đo được. Số so K3 ở §4.4 chỉ là theo dõi.

## 7. Bàn giao cho người kiểm (C)

- Đọc `git diff 80e7329..origin/p82-k3b` (`k3b.py`, test, report):
  - prompt = plan §1;
  - `apply_contract` = plan §2 bản 2;
  - luật hai lượt + Holm họ 4;
  - sửa `f4d3225` không đổi tiêu chí.
- Kiểm lại 0 USD từ dữ liệu:
  - `compare --arm m --runs m_l1.merged m_l2 --other-arm-p 1.0`;
  - `compare --arm m --runs m_test --group test`;
  - `check-base` dev / test;
  - `k3b_watch.py`;
  - tiền = tổng `luna.usd` + `.meta.json`;
  - test `test_k3b_contract.py`.
- Không cần chạy lại lượt có phí.
