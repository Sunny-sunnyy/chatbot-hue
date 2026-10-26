# Implementation Report: Phase 8.2 §10 K1 — pool dense 30 → 100 (B48)

Người làm: B (Claude Opus 5.5, `hue-rag-23`) · 2026-10-26 21:56 +0700 (`date`) · Plan A duyệt: `phase_8_2_k1_plan.md` sha `b8f1597f6a0f`
(commit `2c0520c` trên `main`) · Spec §10 bản `09e8f3932ede` · Code: nhánh `p82-k1` (`d50c41f` = `811d25d` + harness `k1.py`) · **0 USD**
· Trạng thái: **chờ review** (C).

## Cho bạn — 5 dòng lời thường

1. Mình thử cho bước tìm lấy **100 ứng viên thay vì 30**, để các đoạn chứa đáp án hiện đang nằm ngoài 30 có cơ hội được chọn.
2. Đúng là cả 6 câu nhắm tới đều có thêm đoạn đúng trong nhóm ứng viên. Nhưng chỉ **1 câu** lên được 10 đoạn đưa model, và **1 câu khác bị
   đẩy mất** đoạn đúng đang có.
3. Theo luật ghi trước ("không được làm mất câu nào"), kết quả là **kém hơn**, nên **không đưa vào chatbot** và **không chạy lượt sinh có phí**.
4. Tốc độ vẫn ổn: chậm thêm trung bình khoảng 9 ms mỗi câu (ngưỡng 50 ms), không tốn thêm tiền.
5. Điều học được: chỗ nghẽn là **xếp hạng** trong nhóm ứng viên, không phải số ứng viên. Đây là đầu vào để quyết có thử K3 (cho model xếp lại)
   hay không.

## 1. Phạm vi

Làm đúng plan §5 tới điều kiện dừng §6 bước 2:
- M1, M2 (kiểm mốc);
- K1 trên dev, rồi so theo cặp;
- latency, chạy để ghi đủ số của phương án bị bỏ (`run-experiment` §5), 0 USD.

**Không chạy** (theo plan §6.2, vì K1 phạm sàn ở dev): tầng tìm trên test, pilot sinh, lượt sinh, judge. Không ghi Qdrant, không sửa production.

## 2. Thay đổi

- `backend/experiments/phase_8_2/k1.py` (mới, `d50c41f`, sha `eb9ebcd863c4`), đúng plan §3:
  - các lệnh `retrieval`, `compare`, `check-base`, `latency`, `run`, `merge`, `export-judge`, `check-judge`, `analyze`;
  - mọi lệnh ghi đều **từ chối ghi đè**;
  - gọi lại `g1_retrieval.run_config` / `compare`.
- Không sửa production, `g1_retrieval.py`, `b1.py`.

## 3. Cách đã chạy thật

Worktree `/tmp/b_k1/backend`, `HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m …`, Qdrant `:6335` chỉ đọc, e5-small CPU:

```bash
evaluation.full_corpus_eval retrieval --out …/data/phase_8_2/k1/m1_t1.jsonl            # M1
experiments.phase_8_2.k1 retrieval --name base_dev --group dev --pool 30                  # M2
experiments.phase_8_2.k1 check-base --name base_dev
experiments.phase_8_2.k1 retrieval --name k1_dev --group dev --pool 100                   # K1
experiments.phase_8_2.k1 compare --a base_dev --b k1_dev --metrics top10_gold_all top10_gold_frac keyword_coverage mrr ndcg
experiments.phase_8_2.k1 latency --name lat_dev --runs 2                                  # base → k1 → base → k1, cùng phiên
```

## 4. Kết quả quan sát (lần chạy mới, 21:5x)

**Mốc:**
- **M1** sha `cefb2d1ad6094913…` ✓.
- **M2** `check-base`: 108 / 108 câu, **0 trường lệch** so với G1 `runtime.jsonl`. Các trường so: `top_chunk_ids`, `dense_chunk_ids`,
  `pool_*`, `top10_gold_*` ✓.

**Tầng tìm, dev** (`data/phase_8_2/k1/compare_dev.json`):

| Chỉ số | Vai | n | Chênh K1 − mốc | CI 95 % | T / H / T | Kết |
|---|---|---|---|---|---|---|
| `top10_gold_all` | **quyết** | 40 | +0,025 | [−0,050; +0,100] | 2 / 37 / **1** | không khác (cần ≥ 5 / 0) |
| câu mất đoạn đúng khỏi context 10 | **sàn** | 40 | — | — | **1** (câu 154) | **phạm sàn** |
| latency, trung bình chênh theo câu | mức tụt | 108 | **+8,9 ms** | — | — | đạt (≤ +50) |
| `top10_gold_frac` | theo dõi | 40 | +0,011 | [−0,039; +0,063] | 3 / 35 / 2 | không khác |
| `keyword_coverage` | theo dõi | 108 | +1,08 điểm % | [0,00; +2,47] | 3 / 105 / 0 | không khác |
| MRR@10 | theo dõi | 108 | +0,005 | [+0,000; +0,011] | 11 / 92 / 5 | tốt hơn (rất nhỏ) |
| nDCG@10 | theo dõi | 108 | +0,006 | [+0,000; +0,012] | 26 / 66 / 16 | tốt hơn (rất nhỏ) |
| số câu đổi tập top-10 | theo dõi | 108 | **54** | — | — | — |

- Câu thắng: **22** (ngoài pool → đủ); **67** (đã ở pool, xếp lại lên top-10 — không nằm trong trần).
- Câu thua: **154**. Ở mốc, đoạn đúng thứ hai ở **hạng 10** (B42: bị cắt ở context 5, vừa đủ ở context 10). K1 đẩy nó xuống ngoài top-10.
- **Theo dõi 120 / 168:** `top10_gold_frac` 0 → 0 cả hai. K1 không đưa fact nào của hai câu này vào context.

**Tầng pool, giải thích vì sao trượt** (chỉ đọc file):
- Pool dense đủ đoạn đúng: **31 → 37 / 40**. Cả 6 câu trong trần B42 (19, 22, 92, 97, 113, 168) đều có đủ đoạn đúng trong pool 100.
- Nhưng chỉ 22 lên đủ top-10. Hai câu tăng một phần: 19 (`top10_gold_frac` 0,33 → 0,67). Bốn câu không đổi: 92, 97, 113, 168.
- *Suy ra* (từ cơ chế, chưa đo riêng): BM25 chỉ chấm lại trong pool và RRF k 60 không đủ kéo các đoạn hạng dense 36–99 lên top-10. **Vùng ứng
  viên đã đủ; chỗ nghẽn là xếp hạng.**

**Latency** (`data/phase_8_2/k1/lat_dev.json`, CPU, 108 câu × 2 lượt mỗi cấu hình, xen kẽ cùng phiên):

| | p50 | p95 |
|---|---|---|
| mốc (pool 30) | 33,0 ms | 76,1 ms |
| K1 (pool 100) | 43,1 ms | 82,3 ms |
| chênh theo câu | trung bình **+8,9 ms**; p95 của chênh +48,4 ms | |
| nhiễu base lượt 2 − lượt 1 | trung bình −1,8 ms; p95 \|chênh\| 62,8 ms | |

Máy có session khác chạy cùng lúc nên p95 nhiễu lớn. Trung bình thì ổn định.

**Tiền / câu:** K1 không thêm lần gọi API. Retrieval chạy local nên tầng tìm 0 USD. Lượt sinh **NOT RUN**, nên chưa có USD / câu đo từ usage log.
*Ước*: không đổi so với mốc (≈ 0,000204 USD / câu, vẫn 10 đoạn). **Tổng tiền B48: 0 USD.**

## 5. Kết luận theo tiêu chí ghi trước

- **K1 — kém hơn** (phạm sàn "0 câu mất": câu 154). Chỉ số quyết cũng không vượt nhiễu (2 / 37 / 1, CI chứa 0).
- **Không chạy:** test, lượt sinh, judge (plan §6.2).
- **Không đưa vào chatbot.**
- Hồ sơ phương án bị bỏ: đủ số ở §4. A ghi vào `BAO_CAO_TIM_KIEM.md`, mục "Đã thử, chưa áp dụng".
- **Đầu vào cho K3** (§10.3, "chỉ khi K1 không đủ"): pool 100 đã chứa đủ đoạn đúng ở 37 / 40 câu dev, trong khi top-10 đủ ở 23 / 40. Khoảng
  cách 14 câu này là phần một bước xếp lại có thể nhắm tới. Có thể là K3 trên pool 30, hoặc một biến thể "xếp lại pool 100".
  - Trần của K3 pool 30 theo B42 là 9 câu. Trên pool 100 chưa tính.
  - K3 tốn thêm 3–5 s và có phí ⇒ A trình User theo §10.2.

## 6. Lỗi và giới hạn

- 40 câu có đoạn đúng (nhãn agent); một câu thua đủ để phạm sàn, vì sàn được đặt chặt có chủ đích.
- Câu 154 là ca "biên": đoạn đúng ở hạng 10. Mọi biến thể đổi thứ tự đều dễ đẩy nó ra ngoài. Đây không phải lỗi riêng của K1.
- HNSW phụ thuộc `limit` (`Project_Status.md` §8): `limit=100` đổi nhẹ thứ tự dense, và điều này là một phần của biến thể.
- Latency đo trên máy User có tải khác chạy song song.

## 7. Bàn giao cho người kiểm (C)

- Chạy lại rẻ nhất, tất định, khoảng 1 phút mỗi lệnh: `k1 retrieval` (đặt tên mới) cho pool 30 và pool 100, rồi `k1 compare`.
  - Phải ra 2 / 37 / 1, mất câu 154.
  - So với `data/phase_8_2/k1/{base_dev,k1_dev,compare_dev}.json*`.
- Đọc: plan §4 / §6; `k1.py` (`d50c41f`).
- Dữ liệu private: `data/phase_8_2/k1/` gồm `m1_t1.jsonl`, `base_dev.jsonl`, `k1_dev.jsonl`, `compare_dev.json`, `lat_dev.json`.
