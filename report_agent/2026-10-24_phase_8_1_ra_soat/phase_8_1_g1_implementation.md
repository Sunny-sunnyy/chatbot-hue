# Implementation Report: Phase 8.1 G1 — chẩn đoán retrieval chỉ đọc (B15)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-b0`)
Date: 2026-10-24 21:43–21:55 +0700 (lấy bằng `date`)
Kế hoạch + tiêu chí ghi trước (A duyệt): `phase_8_1_g1_plan.md` (mục 0–1, bổ sung mục 4 ghi lúc 21:42 trước khi đo)
Spec: `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §5 G1

## Cho bạn — 5 dòng lời thường

1. Đoạn chứa đáp án **phần lớn đã nằm trong nhóm ứng viên** (lấy 100 đoạn thì 97,5% câu có đủ), nhưng **chỉ 55–60%
   lọt vào 10 đoạn đầu** và 42–50% vào 5 đoạn đưa model: chỗ nghẽn là **xếp hạng**, không phải tìm ứng viên.
2. **Cả 22 câu bot từ chối nhầm** ở 7B đều thiếu ít nhất một đoạn đúng trong 5 đoạn đưa model — tức là lỗi tìm/xếp
   đoạn, chưa phải lỗi prompt.
3. Đổi cách trộn kết quả (10 biến thể: hybrid độc lập, hệ số RRF, DBSF) **chưa biến thể nào thắng chắc** theo luật đã
   ghi trước; tốt nhất là hybrid độc lập + RRF k=2 (+4 câu đủ đoạn đúng, 0 câu mất) nhưng chưa đủ chắc với 40 câu.
4. Câu hỏi **không dấu** làm tìm kiếm sập (MRR 0,73 → 0,19); câu hỏi dạng Unicode NFD tụt 0,73 → 0,53 nhưng chỉ cần
   chuẩn hóa NFC là hết. Tìm gần đúng (HNSW) và tìm chính xác cho kết quả giống hệt.
5. Đã chạy: 0 USD, chỉ đọc Qdrant, chatbot không đổi. Bước nên làm tiếp: xếp hạng lại (reranker, G4) và thử 10 đoạn
   context (G2) — đó là nơi có nhiều đoạn đúng bị rơi nhất.

## 1. Phạm vi

G1.1–G1.5 và G1.6 (4 tầng tự động) theo kế hoạch, trên nhóm thử **dev** (108 câu trong kho; 40 câu có đoạn đúng).
G1.6 chạy trên 55 câu có đoạn đúng (dev + test — **test đã bị nhìn ở bước chẩn đoán này**, ghi rõ theo kế hoạch).
Không mở test cho G1.3 vì không biến thể nào đạt "tốt hơn". Không gọi API trả phí, không ghi Qdrant, không đổi
runtime. Hai tầng judge của G1.6 (model dùng fact, trích đúng): **NOT RUN** (để sau, theo A).

## 2. Thay đổi

- `backend/experiments/phase_8_1/g1_retrieval.py` (harness, untracked; mô tả ở plan §3), thêm sau khi A duyệt: ghi
  `dense_chunk_ids` cho G1.2; lệnh `table`, `overlap`, `layers`; lọc `--realism` lúc phân tích. Không đổi code production.
- Script chạy: `/tmp/b15/run_g1.sh` (21 cấu hình). Kết quả từng câu: `data/phase_8_1/g1/*.jsonl` (private).

## 3. Cách đã chạy thật

`/tmp/b15/run_g1.sh` (từ `backend/`, `HF_HUB_OFFLINE=1`, `uv` trong `.venv`): (1) chạy lại 2 mốc, `cmp` từng byte —
dừng nếu khác; (2) `g1_retrieval run --group dev` cho 20 cấu hình; (3) `run --group all --minilm` (G1.5/G1.6). Phân
tích bằng `compare` (bootstrap 10.000, seed 20261024, Holm trên 10 biến thể G1.3 / 6 biến thể G1.4), `overlap`, `layers`.
Đầu vào khóa: đoạn đúng `gold_draft.jsonl` SHA-256 `bab707b9…`; nhãn độ tự nhiên `golden_realism.jsonl` `060f2df9…`
(dev: natural 47 / capability_only 39 / unnatural 22; 14/40 câu có đoạn đúng là natural).

## 4. Kết quả quan sát

**Mốc:** `dense_bm25_rrf` giống byte `cefb2d1a…`; native giống byte `1fbb5c17…` (B13). **PASS**. 21/21 cấu hình chạy hết.

### G1.1 — đoạn đúng trong tập ứng viên (40 câu dev; `gold_all` = đủ mọi fact)

| Cấu hình | dense | sparse | hợp hai nhánh | top-10 | 5 đoạn đưa model |
|---|---:|---:|---:|---:|---:|
| runtime (pool 30; BM25 chỉ xếp lại tập dense) | 0,775 | 0,775* | 0,775 | 0,550 | 0,425 |
| native pool 30 | 0,775 | 0,675 | 0,875 | 0,575 | 0,475 |
| native pool 100 | 0,925 | 0,875 | **0,975** | 0,600 | 0,500 |
| native pool 200 | 0,950 | 0,975 | 0,975 | 0,600 | 0,500 |
| *natural (14 câu)*: runtime / p100 hợp hai nhánh | | | 0,714 / 0,929 | 0,500 / 0,643 | 0,500 / 0,500 |

\* với runtime, "sparse" là các đoạn BM25 > 0 trong chính tập dense. Hòa điểm ở biên nhánh sparse: 3 / 6 / 5 câu (trên
108) ở pool 30 / 100 / 200.

**Điều kiện dừng sớm (spec §5): KHÔNG chạm.** 18 câu lỗi (runtime top-10 thiếu fact): 17 câu có đủ đoạn đúng trong hợp
hai nhánh @200 (16 câu chỉ với dense @200); 9 câu đã đủ ngay trong pool 30 của runtime nhưng bị xếp ra khỏi top-10.

### G1.2 — HNSW vs exact (108 câu)

Top-10 giống hệt 108/108; tập 30 dense giống hệt 108/108; `top10_gold_all`, MRR không đổi; dense p50/p95 20,5/24,5 ms
vs 20,5/24,1 ms. Theo luật: **giữ HNSW**.

### G1.3 — cách trộn (so với runtime; Holm trên 10 biến thể)

| Biến thể | `top10_gold_all` (40) Δ, CI 95%, T/H/T | MRR (108) Δ, CI | Holm | guardrail mất đoạn đúng |
|---|---|---|---|---|
| native p30 | +0,025 [−0,075; 0,125] 3/35/2 | +0,006 [−0,001; 0,014] | không khác | **mất 2** |
| native p100 | +0,050 [−0,050; 0,150] 3/36/1 | +0,007 [0,000; 0,015] | không khác | **mất 1** |
| runtime k=2 | +0,050 [0,000; 0,125] 2/38/0 | +0,007 [−0,000; 0,015] | không khác | 0 |
| runtime k=10 | 0 [−0,075; 0,075] 1/38/1 | **+0,004 [0,001; 0,008]** | MRR **tốt hơn** | **mất 1** |
| runtime k=30 | 0 1/40 hòa | +0,001 | không khác | 0 |
| **native p30 k=2** | **+0,100 [0,025; 0,200] 4/36/0** | +0,009 [0,001; 0,019] | không khác (trước Holm: tốt hơn cả hai) | 0 |
| native p30 k=10 / k=30 | +0,025 3/35/2 | +0,005 / +0,006 | không khác | **mất 2** |
| DBSF w=0,2 | +0,050 [0,000; 0,125] 2/38/0 | −0,007 [−0,038; 0,026] | không khác | 0 |
| DBSF w=0,3 | +0,025 [0,000; 0,075] 1/39/0 | −0,001 | không khác | 0 |

nDCG: không biến thể nào tụt (mọi CI chứa 0). Phần natural (14 / 47 câu): cùng hướng, không biến thể nào qua Holm.
**Kết luận theo luật ghi trước: không biến thể nào "tốt hơn"** (k=10 qua Holm ở MRR nhưng vi phạm guardrail; native p30
k=2 có tín hiệu rõ nhất nhưng không qua Holm) ⇒ **chưa rõ**; không mở test. Hiệu ứng MRR mọi biến thể rất nhỏ (≤ 0,01).

### G1.4 — dạng câu hỏi (108 câu; Holm trên 6)

| Dạng | MRR Δ (CI) | `top10_gold_all` Δ |
|---|---|---|
| NFD | **−0,204 [−0,265; −0,144] kém hơn** | −0,050 (không khác) |
| NFD + NFC | 0 (giống hệt gốc) | 0 |
| bỏ dấu | **−0,543 [−0,616; −0,470] kém hơn** | **−0,525 kém hơn** (0,55 → 0,025) |
| bỏ dấu + NFC | như trên (NFC không cứu) | như trên |
| đổi kiểu dấu oa/oe/uy | +0,003 (không khác; chỉ 20/108 câu bị đổi) | +0,025 (không khác) |

Natural: cùng kết quả. Theo luật: **NFD tụt mà NFC phục hồi ⇒ đề xuất chuẩn hóa NFC câu hỏi ở 8.2**; **bỏ dấu tụt
mạnh ⇒ ghi giới hạn** (cần khử dấu/tách từ, ngoài G1). Kho dùng lẫn hai kiểu dấu (≈3.316 dòng kiểu mới, 2.336 kiểu cũ),
nên đổi kiểu dấu ít ảnh hưởng.

### G1.5 — MiniLM vượt 512 token

0/158 câu (dev 0/108) có cặp nào trong 30 đoạn sau RRF vượt `max_length`: luật "bỏ rerank cả request" sẽ không kích
hoạt với chunk hiện tại.

### G1.6 — tầng lỗi đầu tiên (55 câu có đoạn đúng; runtime; 4 tầng tự động + từ chối 7B Run 1)

| Nhóm | thiếu ở pool 30 | rơi khỏi top-10 | rơi khỏi 5 đoạn đưa model | đủ tới bước trả lời |
|---|---:|---:|---:|---:|
| tất cả 55 | 14 | 12 | 8 | 21 |
| dev 40 / test 15 | 9 / 5 | 9 / 3 | 5 / 3 | 17 / 4 |
| natural 18 | 5 | 3 | 1 | 9 |
| **22 câu từ chối nhầm 7B** | **10** | **5** | **7** | **0** |

Không câu nào đủ đoạn đúng trong context mà vẫn bị từ chối. Hai tầng sau (model dùng fact, trích đúng) cần judge: NOT RUN.

Tiền: **0 USD**.

## 5. Lỗi và giới hạn

- **Cỡ mẫu nhỏ cho metric theo đoạn đúng:** 40 câu dev (14 natural); CI rộng, Holm trên 10 biến thể khắt khe. "Không
  khác" ở G1.3 nghĩa là chưa chứng minh được, không phải đã chứng minh bằng nhau.
- Đoạn đúng là **nhãn agent** (A + sub-agent, B kiểm chéo B14), User mới duyệt mẫu; `gold_all` khắt khe (thiếu 1 fact
  là 0) — `gold_frac` có trong JSONL nếu cần đọc mềm hơn.
- Test (15 câu có đoạn đúng) đã bị nhìn trong G1.6 — không dùng các câu này để chọn; khi xác nhận ở gate sau, ghi giới
  hạn này (spec §9).
- `candidate_pool` vừa là pool mỗi nhánh vừa là số giữ sau RRF; native p100/p200 vì thế giữ nhiều ứng viên hơn cho RRF.
- G1.6 tầng "từ chối" dùng câu trả lời 7B Run 1 đã lưu (sinh với context 5 runtime — cùng runtime đang đo).

## 6. Bàn giao cho người kiểm (C) và đề xuất cho A

- Đọc: plan §0–1, §4; mục 4 report này. Chạy lại tối thiểu: 2 mốc byte; `run --name runtime --group dev` +
  `run --name native_p30_k2 --treatment native_hybrid_rrf --rrf-k 2` rồi `compare … --metrics top10_gold_all mrr`; `layers
  --name runtime_all_minilm`. Mọi lệnh ở plan §3 / `/tmp/b15/run_g1.sh`.
- **Đề xuất (A quyết):**
  1. Ưu tiên **G4 rerank** và **G2.1 context 10**: 12 + 8 câu rơi ở top-10 / 5 đoạn, 9/18 câu lỗi đã có đoạn đúng trong
     pool 30 nhưng xếp sai. MiniLM không bị chặn bởi độ dài (G1.5).
  2. Ở G4 dùng **pool ứng viên 100 (hợp hai nhánh 0,975)** thay vì 30 (0,775) làm đầu vào reranker — tiêu chí ghi trước
     của G4 nên giữ "0 câu mất đoạn đúng khỏi 5 đoạn".
  3. **Chuẩn hóa NFC câu hỏi** → hàng đợi 8.2 (đơn giản, bằng chứng rõ). **Câu không dấu** → ghi giới hạn; nếu cần,
     một thí nghiệm riêng (khử dấu cả index + query) sau G3/G4.
  4. Cách trộn: giữ runtime; native p30 k=2 để làm ứng viên phụ khi có thêm câu có đoạn đúng (hoặc gộp vào G4 như cấu hình pool).
