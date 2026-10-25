# Review: Phase 8.1 G4 phần từ khóa (B18) — BM25: tách từ, khử dấu, k RRF, b

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 0 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a1`)
Date: 2026-10-25 14:00 (`date`)
Kế hoạch duyệt: `phase_8_1_g4_keyword_plan.md` sha `d7e53186b364` · Implementation report: `phase_8_1_g4_keyword_implementation.md`
sha **`5e8c847df34e`** (khớp tin B)

## 1. Phạm vi đã review

- **Diff:** chỉ `backend/experiments/phase_8_1/g4_keyword.py` (mới, untracked, 344 dòng). C đọc hết. Không đổi production;
  không tạo collection (C kiểm `GET /collections`: chỉ runtime).
- **`MemoryBM25`:**
  - df, idf `log((N − n + 0,5)/(n + 0,5) + 1)`, trọng số `idf · tf(k1 + 1) / (tf + k1(1 − b + b·dl/avgdl))`, bỏ đoạn rỗng;
  - câu hỏi: tập term khác nhau, trọng số 1;
  - cộng theo term tăng dần;
  - khớp mô tả `embedding/sparse.py` và đã kiểm bằng cổng.
- **Hai đường trộn:**
  - runtime: chấm lại đúng `dense_ids30` (Qdrant `limit=30`) bằng `rank_positive_bm25` production;
  - native: sparse top-100 trên cả kho, phá hòa theo point_id, rồi `reciprocal_rank_fusion` production;
  - context: `FullCorpusContextBuilder` + `packed_chunk_ids`.
- **`analyze`** (lệnh thêm sau plan): chỉ in bảng theo luật plan §2.
  - sàn: câu baseline đủ mà biến thể không;
  - keyword: cận dưới CI ≥ −2,0 điểm %;
  - tốt hơn: p Holm < 0,05 và cận dưới CI > 0.

  Không đổi luật.
- **Tách từ** đúng plan §3:
  - `bigram`: âm tiết + cặp trong đoạn không ngắt dấu câu;
  - `codes`: âm tiết + chuỗi có chữ số;
  - `pyvi` thay âm tiết;
  - `deaccent` dùng `transform_query("noaccent")` của G1.

## 2. Findings

Không có finding.

Ghi nhận:
- **Holm của P:** plan ghi "4 (hoặc 2 nếu bỏ k)" cho một base. Thực tế có hai base (runtime, native) vì không tách từ nào thắng,
  nên B dùng Holm chung 6. B đã ghi rõ. Cách này chặt hơn; với Holm riêng thì kết luận không đổi, vì không dòng nào có cận dưới
  CI > 0.
- **N0 lệch G1 ở 1/108 câu** (câu 162, hạng 5 ↔ 6). Lý do: Qdrant phá hòa bằng float32 khi hai đoạn bằng điểm ở float64. Tập 100
  ứng viên giống hệt. Đúng nhánh "chỉ do hòa ⇒ dùng mốc trong bộ nhớ" của plan §1.
- **Đề xuất 8.2 của B** "chỉ dùng chỉ mục khử dấu khi câu hỏi không có dấu" là giả thuyết, chưa đo; B đã ghi đúng là "chưa đo".
  Ghi chú thêm: câu không dấu ở đây là bản biến đổi bằng máy. Trước khi quyết ở 8.2 cần câu không dấu thật của người dùng (B đã
  ghi ở §5).
- **Đầu vào chưa kiểm lại:** C dùng `dense_<dạng>.jsonl` đã lưu (cổng xác nhận 10/10 câu `limit=30` hỏi lại giống), không chạy
  lại nhánh dense cho mọi câu.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `HF_HUB_OFFLINE=1`, 0 USD, Qdrant chỉ đọc.

```bash
uv run python -m experiments.phase_8_1.g4_keyword gate
uv run python -m experiments.phase_8_1.g4_keyword same-as-g1 --name r0 --g1 runtime
uv run python -m experiments.phase_8_1.g4_keyword same-as-g1 --name n0 --g1 native_p100
uv run python -m experiments.phase_8_1.g4_keyword analyze --realism main --pairs <A: 6 cặp> | <E1: 2 cặp> | <E2: 2 cặp> | <P: 6 cặp>   # như report §6
uv run python -m experiments.phase_8_1.g4_keyword run --name c_check_bigram_native --fusion native --tokenizer bigram
```

## 4. Kết quả quan sát — khớp report

- **Cổng:**
  - sparse state trong bộ nhớ = production: 8.459 đoạn, avgdl, từ vựng, idf giống hệt;
  - 200 cặp điểm: 195 giống từng bit, lệch lớn nhất 8,9e-16;
  - dense-30 lưu = hỏi lại 10/10; 30 đầu của `limit=100` = `limit=30` ở 107/108 câu.
- **`same-as-g1`:**
  - r0 vs G1 runtime: 108/108, 0 lệch top-10 / context / MRR;
  - n0 vs G1 native_p100: lệch đúng câu 162 ở top-10 / context, MRR 0 lệch.
- **A** (Holm 6):

| Biến thể | `context5_gold_all` | câu mất | keyword |
|---|---|---|---|
| bigram · runtime | 1/30/1 | 169 | đạt |
| codes · runtime | 0/32/0 | — | đạt |
| pyvi · runtime | 0/31/1 | 169 | đạt |
| bigram · native | 2/27/3 | 19, 134, 169 | −2,65 |
| codes · native | 0/32/0 | — | đạt |
| pyvi · native | 1/27/4 | 19, 89, 134, 169 | −2,27 |

  ⇒ kém hơn ×4, không khác ×2 (codes). ✓
- **E (1) câu có dấu:** runtime mất 45, 169; native mất 89, 134, 139, 169, keyword −3,60 ⇒ kém hơn cả hai. ✓
- **E (2) câu không dấu** (Holm 2): runtime 1/31/0, p Holm 0,73; native 3/29/0, p Holm 0,18 ⇒ chưa rõ. ✓
- **P** (Holm 6):

| Biến thể | `context5_gold_all` | câu mất | keyword |
|---|---|---|---|
| runtime b 0,5 | 1/31/0 | — | đạt |
| runtime b 1,0 | 1/30/1 | 29 | đạt |
| native k 10 | 1/31/0 | — | −2,27 |
| native k 30 | 0/32/0 | — | đạt |
| native b 0,5 | 0/31/1 | 89 | −2,84 |
| native b 1,0 | 1/29/2 | 19, 29 | đạt |

  ⇒ không biến thể nào tốt hơn; b 1,0 (cả hai) và native b 0,5 kém hơn. ✓
- **Tất định:** chạy lại `bigram · native` với tên mới cho 108/108 câu giống hệt `a_bigram_native.jsonl` (bỏ `bm25_ms`,
  `config`). Từ vựng 105.999 khớp §4.1.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại nhánh dense cho cả 216 câu (dùng file đã lưu; cổng kiểm 10 câu).
- Không xác nhận test (đúng plan: không có "tốt hơn").

## 6. Decision

**ready_for_user_confirmation.** B18 thực hiện đúng plan `d7e53186b364`. Mọi số C tính lại đều khớp. Kết luận theo luật ghi
trước:
- không cách tách từ / khử dấu / tham số nào tốt hơn BM25 âm tiết hiện tại;
- tín hiệu đáng ghi cho 8.2: khử dấu giúp mạnh ở câu không dấu với native (chỉ số phụ), nhưng hại câu có dấu.

A đóng B18.

Tiền (C): **0 USD**.
