# Review: Phase 8.1 G1 — chẩn đoán retrieval chỉ đọc (B15)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 3 minor; 1 phát hiện cần A ghi nhận)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a3`)
Date: 24/10/2026, 21:48–21:59 (giờ lấy bằng `date`)
Tiêu chí ghi trước: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_plan.md` §0–1, §4 (A duyệt, ghi trước khi đo)
Implementation report: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g1_implementation.md`

## 1. Phạm vi đã review

- **Đọc hết:** plan §0–4; report §1–6; harness `backend/experiments/phase_8_1/g1_retrieval.py` (370 dòng,
  untracked).
- **Đối chiếu kết luận với luật ghi trước:**
  - "tốt hơn" = CI > 0 sau Holm **và** đủ guardrail;
  - điều kiện dừng sớm;
  - luật G1.2, G1.4.
- **Hợp đồng kiểm** (plan §0): C tự chạy lại ít nhất G1.1 và một biến thể G1.3. C chạy G1.1 (runtime,
  native p100, p200) + G1.3 (native p30 k=2), rồi phân tích lại toàn bộ bảng G1.3 và G1.6 từ JSONL.

## 2. Findings

**Không có blocker hoặc major.**

**Đúng đường production, đúng phạm vi:**

- Harness gọi `build_full_corpus_retrieval_service` với tham số B11/B13 (`candidate_pool`, `rrf_k`,
  `search_params`), `build_context_builder` / `FullCorpusContextBuilder`, `score_retrieval`, bootstrap /
  `verdict` / `holm_adjust` của evaluator.
- Logic chỉ nằm trong harness: DBSF, biến đổi câu hỏi, chấm đoạn đúng theo offset.
- Không ghi Qdrant (chỉ `scroll`/`query_points`), không đổi code production, 0 USD.
- Cấu hình runtime và native trong harness trùng từng câu với mốc (B kiểm; C kiểm lại gián tiếp, §4).

**Kết luận khớp luật ghi trước** (C tính lại cả 10 biến thể G1.3, Holm trên 10):

- **native p30 k=2:** `top10_gold_all` +0,100 [0,025; 0,200], 4/36/0. Qua CI trước Holm, **không qua
  Holm** ⇒ "chưa rõ". Đúng luật.
- **runtime k=10:** MRR qua Holm (+0,004 [0,001; 0,008]) nhưng mất 1 câu đoạn đúng (vi phạm guardrail) ⇒
  không "tốt hơn". Đúng luật.
- **Điều kiện dừng sớm** không chạm: 17/18 câu lỗi có đủ đoạn đúng ở hợp hai nhánh @200. Đúng.
- **G1.2:** giữ HNSW (top-10 giống 108/108). Đúng luật.
- **G1.4:** NFD tụt, NFC phục hồi ⇒ đề xuất NFC query cho 8.2; bỏ dấu tụt mạnh ⇒ ghi giới hạn. Đúng luật.

**Minor:**

- **m1. `context_ids = top_ids[: len(packed.sources)]` giả định context builder đóng gói một tiền tố của
  danh sách** (`g1_retrieval.py`, `run_config`). Builder thật bỏ qua đoạn không có `evidence_parts`
  (`continue`) và dừng khi hết ngân sách (`break`). Với index hiện tại, giả định đúng: C quét 8.459 point,
  0 point thiếu `evidence_parts`; ngân sách chưa bao giờ chạm trần. Biến thể chunk ở G3 có thể khác.
  Tiêu chí đóng: G3 lấy id từ chính `packed.sources` (hoặc kiểm lại giả định cho mỗi index).
- **m2. Độ lớn hiệu ứng ghi chưa nổi.** MRR của mọi biến thể G1.3 chênh ≤ 0,01. "Qua Holm" của k=10 là
  +0,004 MRR, không có ý nghĩa thực tế. Report §5 đã ghi "rất nhỏ". Đề xuất: bảng G5 ghi kèm mức chênh,
  để "tốt hơn" không bị đọc như "tốt hơn đáng kể".
- **m3. Lệnh `run` ghi đè file cùng `--name`** (B đã cảnh báo). Không cần sửa. Ghi vào hướng dẫn chạy lại
  cho mọi gate sau.

**Phát hiện cần A ghi nhận** (ảnh hưởng tới các kết luận cũ):

- **Theo đoạn đúng, 22/22 câu từ chối nhầm của 7B đều thiếu ít nhất một fact trong 5 đoạn đưa model.**
  Phân rã: 10 thiếu ngay ở pool 30, 5 rơi khỏi top-10, 7 rơi khỏi 5 đoạn; 0 câu đủ đoạn đúng mà vẫn bị
  từ chối. C tính lại từ `runtime_all_minilm.jsonl` và ra đúng số này.
  - Kết luận này **ngược** với chẩn đoán B4 theo keyword (`reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`):
    "4/22 có đủ keyword mà vẫn từ chối". Hai cách đo khác nhau. Keyword proxy lạc quan: keyword có trong
    context chưa chắc đủ fact. Đoạn đúng thì khắt khe: `gold_all` thiếu 1 fact là 0, và nhãn do agent
    gắn.
  - **Hệ quả:** lập luận "H8 (trả lời một phần) cần vì có câu đủ bằng chứng vẫn bị từ chối" (C11 dòng 6.4,
    B5) **yếu đi**. H8 vẫn có thể giúp nhóm "có một vế". Tuy nhiên G2.2 nên đo cả hai nhóm: câu đủ đoạn
    đúng trong context, và câu thiếu một phần.
  - Đề xuất: A ghi vào bảng rà C11 / report G5 rằng kết luận B4 "4 câu đủ mà vẫn từ chối" không đứng
    vững khi đo theo đoạn đúng.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `uv` trong `.venv`, `HF_HUB_OFFLINE=1`, Qdrant chỉ đọc, 0 USD. Đầu vào khóa đúng như report:

- đoạn đúng: `gold_draft.jsonl` SHA-256 `bab707b9…`;
- nhãn độ tự nhiên: `golden_realism.jsonl` SHA-256 `060f2df9…`.

```bash
uv run python -m evaluation.full_corpus_eval retrieval --out /tmp/c21_dense.jsonl                       # cmp mốc 7B
uv run python -m evaluation.full_corpus_eval retrieval --treatment native_hybrid_rrf --out /tmp/c21_native.jsonl   # cmp mốc B13
G="uv run python -m experiments.phase_8_1.g1_retrieval"
$G run --name c_runtime --group dev
$G run --name c_native_p30_k2 --group dev --treatment native_hybrid_rrf --rrf-k 2
$G run --name c_native_p100 --group dev --treatment native_hybrid_rrf --pool 100
$G run --name c_native_p200 --group dev --treatment native_hybrid_rrf --pool 200
$G compare --a c_runtime --b native_p30 native_p100 runtime_k2 runtime_k10 runtime_k30 c_native_p30_k2 \
   native_p30_k10 native_p30_k30 dbsf_w02 dbsf_w03 --metrics top10_gold_all mrr
$G table --names c_runtime native_p30 c_native_p100 c_native_p200
$G layers --name runtime_all_minilm
uv run python -I /tmp/c21_ev.py      # đếm point thiếu evidence_parts (m1)
```

Tên file của C có tiền tố `c_` để không ghi đè file của B.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Mốc `dense_bm25_rrf` / native | **PASS**: giống byte `cefb2d1a…` / `1fbb5c17…` |
| 4 cấu hình C chạy lại vs file của B | **Giống hệt từng câu** (bỏ trường `dense_ms` thời gian và `config` tên): runtime, native p30 k=2, native p100, native p200 — 108/108 câu mỗi cấu hình |
| G1.1 (40 câu có đoạn đúng): hợp hai nhánh / top-10 / 5 đoạn | runtime 0,775 / 0,550 / 0,425; native p30 0,875 / 0,575 / 0,475; p100 0,975 / 0,600 / 0,500; p200 0,975 / 0,600 / 0,500 — **khớp report** |
| G1.3 (10 biến thể, Holm) | Mọi số Δ, CI, thắng/hòa/thua, kết luận **khớp report**: native p30 k=2 tốt hơn trước Holm, không qua Holm; runtime k=10 MRR qua Holm, mất 1 câu đoạn đúng; DBSF không khác |
| G1.5 MiniLM vượt 512 | 0/158 (từ `runtime_all_minilm.jsonl`) — khớp |
| G1.6 tầng lỗi (55 câu) | pool 14 / top-10 12 / 5 đoạn 8 / tới bước trả lời 21; 22 câu từ chối nhầm: 10 / 5 / 7 / 0 — khớp |
| Giả định m1 | 0/8.459 point thiếu `evidence_parts` |

Không chạy lại G1.2, G1.4 và các biến thể G1.3 khác. C chỉ phân tích lại JSONL của B; dùng lại bằng chứng vì
4 cấu hình chạy lại đều trùng từng câu, cùng code và cùng index.

## 5. Giới hạn

- C không kiểm lại nhãn đoạn đúng. Nhãn do agent gắn, B14 kiểm chéo, User duyệt mẫu. Mọi kết luận theo
  đoạn đúng phụ thuộc nhãn này.
- Cỡ mẫu theo đoạn đúng nhỏ (40 dev, 14 natural), như B ghi.
- Test (15 câu có đoạn đúng) đã bị nhìn ở G1.6. Khi xác nhận ở gate sau phải ghi giới hạn này.

## 6. Decision và bước tiếp theo

**`ready_for_user_confirmation`.** A commit harness `backend/experiments/phase_8_1/` + plan + report. C đồng
ý thứ tự đề xuất của B:

1. G4 rerank trên pool 100 (hợp hai nhánh 0,975);
2. G2.1 context 10;
3. NFC query vào hàng đợi 8.2;
4. câu không dấu ghi giới hạn.

Thêm: ghi nhận phát hiện "22/22 câu từ chối nhầm thiếu đoạn đúng" vào bảng rà, và sửa m1 trước khi G3 dùng
harness với index khác.
