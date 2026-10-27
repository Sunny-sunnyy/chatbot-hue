# Implementation Report: Phase 8.2 §10 K3b-m — lượt sinh + judge (phụ lục) — dừng sau dev: vượt mức tụt Completeness (5 > 4)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-31`) · 2026-10-27 10:44 +0700 (`date`) · Việc: B60–B65 (A giao 27/10).
Plan A duyệt: `phase_8_2_k3b_m_answer_plan.md` **bản 3** sha **`2a3b22b38ab6`** (commit `c46019f`; B tính lại từ file trước khi chạy: khớp).
- Bản 1 `84d4aaf0ad04`.
- Bản 2 `92a8a7eb4177`: chạy pilot, dừng ở sàn 120.
- Bản 3: User chọn đưa 120 về theo dõi.

Code: nhánh `p82-k3b` = … `806e8ad` (report K3b) + `9ff6ebb` (harness `k3b_answer.py` + test) + `6b4114e` (bản 3: bỏ dừng ở 120).

**Tiền thật (log): 0,0749297 USD** / trần 0,13. Gồm:
- pilot bản 2: 0,0047854;
- pilot v3: 0,0052245;
- dev còn lại v3: 0,0649198.

Trạng thái: **chờ review** (C).

## Cho bạn — lời thường

1. Bước tìm của "luna chọn 10 đoạn" đã tốt hơn. Lần này mình đo **câu trả lời cuối cùng** trên 120 câu thử, chấm mù cùng lượt với câu trả lời
   hiện tại.
2. Nhìn chung câu trả lời **tốt lên**:
   - điểm đủ ý (Completeness) tăng trung bình +0,22 / 5, điểm đúng (Accuracy) +0,25 / 5;
   - bốn câu trước bị từ chối nay trả lời đúng và đủ: 48, 67, 167 (5 / 5) và 120;
   - không câu nào trả lời "vòng vo" kiểu "nguồn không nêu…".
3. Nhưng có **5 câu bị chấm thấp hơn 1–2 điểm** về đủ ý, mà luật ghi trước chỉ cho phép tối đa 4 câu. Vì vậy kết luận theo luật là
   **"kém hơn"**, và mình **dừng, không chạy nhóm kiểm**. Ba trong 5 câu này có context gần như giống hiện tại (7–9 / 10 đoạn trùng), nên một phần có
   thể là dao động khi model viết lại. Đây là suy ra, chưa đo.
4. Giá đo thật: mỗi câu chờ khoảng **6,5 giây** (có lúc 9 giây), tiền mỗi câu gấp **3,8 lần**. Tiền lượt này: 0,075 USD (≈ 1.900 đồng).

## 1. Phạm vi

Plan bản 3 §3:
- bước 1: pilot dev 10 (`v3_dev_pilot`);
- bước 2: dev còn lại 110 (`v3_dev_rest`) ⇒ gộp `answer_dev` 120 câu ⇒ `check`;
- bước 3: judge mù dev (K3b-m + B1 chấm lại cùng lượt) ⇒ `analyze` dev;
- thêm 2 kiểm theo dõi A giao: C51 trên dev K3b-m, và dạng câu trả lời của 168.

Bước 3 phạm mức tụt T3 ⇒ **dừng** (plan §3 bước 3). **NOT RUN:** test 56, judge test, W3 (R4).

Lượt bản 2 (`dev_pilot`, 9 câu, 10:16) **giữ làm hồ sơ**, kết luận lượt đó = phạm sàn T8 bản 2. Lượt v3 chạy lại từ đầu, **không** dùng 9 câu đó
(plan bản 3 "Đổi sau khi thấy số").

Không đổi production, không ghi Qdrant, không mở câu kín, không đọc câu test.

## 2. Thay đổi

`backend/experiments/phase_8_2/k3b_answer.py` (`9ff6ebb`, sửa ở `6b4114e`):
- **`K3bService`** bọc retrieval production. 30 đoạn `stages["rrf"]` ⇒ thứ tự luna (phát lại từ `m_l1.merged` / `m_test` cho 55 câu có đoạn
  đúng; gọi mới `k3b.luna_top10` cho phần còn lại) ⇒ `k3b.apply_contract` ⇒ 10 đoạn. `full_corpus_eval.answer_case` chạy nguyên.
- Sàn được kiểm bằng máy:
  - T1: OOS bị trả lời;
  - T2: `error` hoặc `citation_error` ≠ null, tức API 500;
  - sai hợp đồng > 4.
- Ghi từng dòng ngay sau mỗi câu, luôn ghi `.meta.json`, từ chối ghi đè.
- Judge mù gộp K3b-m + B1, đúng khuôn `r2.pooled_items`.
- `analyze`: T3–T5, T7, W1, W2, W4.
- W2 dùng bộ tách câu giữ `[n]` sau dấu kết câu, kể cả `. [1]`, không phân biệt hoa thường như `CITATION_PATTERN` (C53 vòng 2 m-4).
  `backend/tests/test_k3b_answer_text.py`: 3 test, cùng 4 test hợp đồng ⇒ **7 passed**.

Khác plan: không có.

## 3. Cách đã chạy thật

Worktree `/tmp/b_k3b`, từ `backend/`, Qdrant `:6335` chỉ đọc. Lệnh có phí dùng `--env-file /home/minhhieu/hue_rag/.env`:

```bash
… -m experiments.phase_8_2.k3b_answer run --cases pilot --name v3_dev_pilot      # 10:35:19–10:35:35
… -m experiments.phase_8_2.k3b_answer run --cases rest  --name v3_dev_rest       # 10:36:33–10:38:53
… -m experiments.phase_8_2.k3b_answer merge --parts v3_dev_pilot v3_dev_rest --name answer_dev
… -m experiments.phase_8_2.k3b_answer check                  > …/answer/check_dev.json
… -m experiments.phase_8_2.k3b_answer export-judge --group dev --batch-size 25   # 215 câu trả lời khác nhau / 240, 9 lô
#   5 sub-agent judge Claude mới (global.anthropic.claude-opus-5-5 — cùng model judge B1), chỉ Read full_corpus_judge_prompt.md + lô, Write scores_NN.jsonl
… -m experiments.phase_8_2.k3b_answer check-judge --group dev                    # 215 / 215, 0 lỗi schema
… -m experiments.phase_8_2.k3b_answer analyze --group dev    > …/answer/analyze_dev.json
PYTHONPATH=. uv run --project /home/minhhieu/hue_rag python ../data/phase_8_2/k3b/answer/tools/c51_on_k3b.py   # C51 L1 / L2
```

## 4. Kết quả quan sát

Dữ liệu private `data/phase_8_2/k3b/answer/`, sha 12:

| File | sha |
|---|---|
| `v3_dev_pilot.jsonl` | `de55e3213a91` |
| `v3_dev_rest.jsonl` | `d24527f93de4` |
| `answer_dev.jsonl` | `d5da57bb201c` |
| `check_dev.json` | `5419bdceed6a` |
| `analyze_dev.json` | `31da6a65cb5e` |
| `c51_dev.json` | `3521180bce58` |
| `judge_dev/map.json` | `47fe32a30dba` |
| `tools/c51_on_k3b.py` | `1c7f107f8307` |
| (hồ sơ bản 2) `dev_pilot.jsonl` | `9dc4a659eb45` |

### 4.1 Sàn và kiểm tất định (dev 120)

| | Kết quả | |
|---|---|---|
| T1 OOS bị trả lời (12) | 0 | ✓ |
| T2 lỗi kỹ thuật / `citation_error` (= API 500) | 0 | ✓ |
| Phát lại = `top_chunk_ids` file gốc | 40 / 40 | ✓ |
| Sai hợp đồng ở 80 lần rerank mới | 0 (CI 95 % [0; 4,5 %]) | ✓ |
| T6 citation v2 theo dạng (theo dõi) | K3b-m 0, B1 0 | — |
| T8 (theo dõi) | 120: B1 từ chối → K3b-m trả lời; 168: như vậy | — |

### 4.2 Mức tụt và chất lượng (dev chính 88, judge cùng lượt mù)

Cột "Chênh TB [CI]" là **chỉ báo, không quyết**. Luật nhận chỉ dùng số câu thua (T3, T4) và các dòng T5, T7.


| | Chênh TB K3b-m − B1 [CI 95 %] | Thắng / thua | Ngưỡng | |
|---|---|---|---|---|
| Completeness | **+0,216** [+0,023; +0,443] | 8 / **5** | T3: thua ≤ 4 | **✗ vượt** |
| Accuracy | **+0,250** [+0,068; +0,466] | 8 / 1 | T4: thua ≤ 4 | ✓ |
| Relevance | +0,227 [+0,045; +0,443] | — / 2 | theo dõi | — |
| T5 từ chối mới (B1 trả lời → K3b-m từ chối) | 0 | | ≤ +1 | ✓ |
| T7 `output_tokens` sinh / câu | 0,968× | | ≤ 1,2× | ✓ |
| Từ chối nhầm (theo dõi) | 7 / 88 → 2 / 88 | | | — |

**5 câu Completeness tụt** (`case_index`, không chép nội dung):

| Câu | Loại | Completeness | Accuracy | Đoạn đúng (B1 → K3b-m) | Top-10 trùng mốc | Phát lại |
|---|---|---|---|---|---|---|
| 26 | conditional | 5 → 4 | 5 → 5 | không nhãn | 9 / 10 | không |
| 66 | direct_fact | 5 → 4 | 5 → 5 | không nhãn | 8 / 10 | không |
| 93 | conditional | 5 → 4 | 5 → 5 | không nhãn | 5 / 10 | không |
| 112 | conditional | 5 → **3** | 5 → 4 | không nhãn | 7 / 10 | không |
| 134 | multi_source | 5 → 4 | 5 → 5 | 1,0 → 1,0 | 7 / 10 | có |

*Suy ra*, chưa đo:
- Ở 26 / 66, context gần như giống mốc, nên tụt điểm có thể do model viết khác hoặc do judge.
- Nhưng A/A của mốc (B1 ↔ G2.1a, cùng judge cùng lượt) chỉ có 1 câu tụt. Đây đúng là lý do luật đặt ngưỡng A/A + 3, và luật được giữ nguyên.

### 4.3 Theo dõi

- **W1 — câu thắng ở tầng tìm** (dev chính, Completeness / Accuracy B1 → K3b-m):

  | Câu | Completeness | Accuracy |
  |---|---|---|
  | 48 | 1 → 5 | 1 → 5 |
  | 67 | 1 → 5 | 1 → 5 |
  | 167 | 1 → 5 | 1 → 5 |
  | 70 | 3 → 5 | 4 → 5 |
  | 159 | 3 → 4 | 5 → 5 |
  | 38 | 4 → 4 | 5 → 5 |
  | 156 | 5 → 5 | 5 → 5 |

  ⇒ **5 / 6** câu có lý do biết trước đã tăng (plan W1).
- **W2:**
  - Câu từ chối → trả lời: **48, 67, 85, 120, 167, 168**. Mỗi câu có **0** câu thiếu trích. Ngược lại (trả lời → từ chối): 0.
  - **C51** (hàm `check` của `c51_scan.py`, không sửa): K3b-m dev **L1 0 / L2 0** trên 105 câu trả lời. Mốc B1 dev: L1 1 (câu 70), L2 0.
- **168** (A giao kiểm, B đọc trong terminal):
  - câu trả lời nêu đúng số tiền của đáp án tham chiếu, trích `[1]` từ đúng file nhãn cho fact đó, 0 câu thiếu trích;
  - ⇒ **không** phải dạng "trả lời vòng" (R1 / R2).
  - Fact còn lại ("giá thuyền chưa gồm vé") không có trong context theo nhãn; câu trả lời diễn đạt là "khoản riêng".
- **120:** như đã kiểm trước khi viết bản 3. Câu trả lời khớp đáp án tham chiếu, hai fact có trong context (B61).

### 4.4 Giá đo thật (W4)

| | Mốc B1 | K3b-m |
|---|---:|---:|
| `e2e_ms` p50 [CI] — 80 câu gọi rerank mới, gọi đồng thời 4 | (retrieval 27 ms + sinh 1.772 ms) | **6.502** [6.242; 7.011] |
| `e2e_ms` p95 [CI] | (sinh p95 3.293 ms) | **9.126** [8.687; 10.533] |
| USD / câu (sinh + rerank; câu phát lại tính tiền rerank đã trả ở K3b) | 0,000204 | **0,00078 (3,8×)** |
| `output_tokens` sinh TB | 77,0 | 74,5 (0,968×) |

Latency B1 đo ngày 26/10, khác phiên, nên chỉ để theo dõi. Gọi đồng thời 4 làm `e2e_ms` cao hơn khi một người dùng (K3b tuần tự: rerank p50 5,0 s).

## 5. Kết luận theo tiêu chí ghi trước

- **K3b-m (khâu trả lời) — kém hơn: vượt mức tụt T3** (Completeness thua 5 > 4 ở dev chính). Dừng sau dev, đúng plan §3 bước 3.
- Các tiêu chí khác ở dev đều đạt: T1, T2, T4, T5, T7.
- Chỉ báo, không quyết: chất lượng chung **tăng có CI > 0** (Completeness +0,22, Accuracy +0,25, Relevance +0,23); từ chối nhầm 7 → 2.
- Luật nhận của đợt là "không hỏng ở bất kỳ mức tụt nào". Luật không đổi sau khi thấy số; kết luận theo luật là **kém hơn**.
- **NOT RUN:** test, R4.
- **Không đưa vào chatbot.** Nhánh `p82-k3b` giữ làm hồ sơ.
- Hướng mở (B ghi, A / User quyết; *chưa đo*):
  - (1) **A/A của chính biến thể**, cần **plan mới với tiêu chí ghi trước**, không phải "chạy lại cho qua". Sinh lại 120 câu dev trên **cùng context
    K3b-m**: phát lại thứ tự luna đã ghi ở lượt này, 0 lần rerank mới. Judge mù cùng lượt với `answer_dev` + B1. Mục đích: đo số câu Completeness đổi
    giữa hai lượt sinh K3b-m. Lượt này **không thay** kết luận "kém hơn" ở trên; nó chỉ cho biết ngưỡng A/A + 3 lấy từ mốc có hợp với biến thể đổi context
    không. Ước ≈ 0,025 USD;
  - (2) xem User có muốn đặt luật nhận khác cho biến thể "chất lượng tăng nhưng vài câu tụt" không. Đó là đổi luật đợt, User quyết.

## 6. Lỗi và giới hạn

- Judge Claude ⇒ kết luận **tạm tới B0**. Một lượt sinh. Chưa có A/A sinh trên context K3b-m.
- Nhãn đoạn đúng thiếu chỗ lặp (B61): không đổi kết quả tầng tìm. Ở khâu trả lời, 120 / 168 chỉ theo dõi (bản 3).
- 5 câu tụt đều là câu chính. 4 / 5 không có nhãn đoạn đúng, nên không đo được tầng tìm của chúng.
- Latency đo khi gọi đồng thời 4 trên máy User.

## 7. Bàn giao cho người kiểm (C)

- Đọc `git diff 806e8ad..origin/p82-k3b` (`k3b_answer.py`, test, report).
- Kiểm lại 0 USD:
  - `check`;
  - `check-judge --group dev`;
  - `analyze --group dev` (đếm thua Completeness bằng map + scores);
  - `tools/c51_on_k3b.py`;
  - tiền = tổng `usd_answer` + `usd_rerank` + `.meta.json`.
- Không cần chạy lại lượt có phí.
