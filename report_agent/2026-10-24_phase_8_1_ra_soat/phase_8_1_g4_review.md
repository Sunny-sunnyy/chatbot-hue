# Review: Phase 8.1 G4 — xếp hạng lại (B17 bước 2, phần G4)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 2 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a1`)
Date: 2026-10-25 12:39 (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §5 G4 (gồm sửa đổi 25/10);
kế hoạch `phase_8_1_g2_g4_plan.md` bản duyệt sha `a4adfc8eedd9` (commit `b9789f4`)
Implementation report: `phase_8_1_g4_implementation.md`. B nhắn sha `6c70e903c0fa`; B sửa tiếp phần "chỉ natural" theo
nhãn mới, nên C review bản **`d99341dc66c6`**.

## 1. Phạm vi đã review

- **Git:** `main` @ `b9789f4` + working tree. Thay đổi của B17:
  - `backend/reranking/cross_encoder.py` (production);
  - `backend/experiments/phase_8_1/g4_rerank.py` (mới, untracked, 334 dòng);
  - `pyproject.toml` + `uv.lock` (`uv add sentencepiece`);
  - report G4 (untracked).

  Các file khác trong working tree là của A/C. `git diff --check` exit 0.
- **Đọc exact diff:** `cross_encoder.py`, `pyproject.toml`, `uv.lock` (+38 dòng, 0 dòng xóa, chỉ gói `sentencepiece`
  0.2.2); đọc hết `g4_rerank.py`.
- **Đối chiếu code thật:** `FullCorpusContextBuilder.build` (`full_corpus_context.py:88-110`), `PackedSource` (`:10-14`),
  `CrossEncoderReranker.rerank` (luật phá hòa, `cross_encoder.py:106`), `build_retrieved_document`
  (`full_corpus.py:335-337`, `id = chunk_id`), chỗ runtime tạo reranker (`full_corpus.py:829`).
- **Dữ liệu:** 19 file `data/phase_8_1/g4/*.meta.json` + JSONL; `subset.json` (sha `b9b6e6123ba4`, khớp report).

## 2. Findings

Không có blocker hay major.

- **m1 (minor) — "100 cặp/câu" không đúng với đầu vào thật của pool 100.**
  - Vị trí: report §4.4 ("rerank 100 cặp trên GTX 1650") và tên "pool 100" ở §4.1 / §7.
  - Bằng chứng: harness lấy **hợp** hai nhánh native (dense 100 ∪ sparse 100; `g4_rerank.py` `candidates`). Đúng như plan
    và G1 định nghĩa. C đếm lại trên dev 30 (chỉ đọc Qdrant): **112–192 đoạn/câu, trung vị 147, trung bình 149**.
  - Tác động: người đọc tưởng latency 10–14 s là cho 100 cặp. Thật ra là ~150 cặp, nên ước "nếu chỉ 100 cặp" sẽ lệch.
    Kết luận không đổi.
  - **Đóng khi:** §4.4 và §7 ghi "hợp hai nhánh, 112–192 đoạn/câu (trung vị 147)".
- **m2 (minor) — meta của lượt luna ghi `device: cuda`.**
  - Bằng chứng: `a_luna_plain_pilot.meta.json`, `a_luna_plain_rest.meta.json` ghi `"device": "cuda"` (giá trị mặc định
    của `--device`), trong khi luna gọi API. Report §7 đã ghi đúng là "API".
  - Tác động: ai đọc meta riêng lẻ sẽ hiểu sai.
  - **Đóng khi:** report ghi một dòng "meta luna: trường `device` không dùng", hoặc harness bỏ / ghi `api` cho luna ở lượt
    sau. Không cần chạy lại.

Ghi nhận, không phải finding:
- `packed_chunk_ids` gọi `FullCorpusContextBuilder._source` (hàm private) để biết đoạn nào vào context, vì `PackedSource`
  không có `chunk_id`. C đọc `build`: builder bỏ nguồn không có bằng chứng rồi `break` ở nguồn đầu tiên vượt ngân sách. Vì
  vậy `kept[:len(packed.sources)]` đúng là các đoạn đã đóng gói. Cách này đơn giản hơn thêm field vào production. Chấp
  nhận cho harness; G3 có thể dùng lại.
- Luật phá hòa của harness (`-score`, rồi `d.id`) giống `CrossEncoderReranker.rerank` (`-score`, rồi
  `metadata["chunk_id"]`), vì `id = chunk_id`.
- Tiền luna: lượt 20 câu vượt 54% so với ước tỉ lệ của plan. B đã dừng và báo A, đúng luật "vượt 50% thì dừng, báo A".
- Report đủ thông số từng lượt theo yêu cầu A (12:27):
  - model + revision (§2, §7); thiết bị thật (`gpu_check.model_device`); `max_length` 1024 (tokenizer cũng 1024);
  - pool, top-k 10, sha tập câu, seed, latency p50/p95 cả luồng và từng khâu;
  - token / USD (§5), mẫu lệnh, đường dẫn kết quả.

  Revision và lệnh chỉ có trong report, không có trong meta. Chấp nhận.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `uv` trong `.venv`, `HF_HUB_OFFLINE=1`. Mọi lệnh không gọi API trả phí. Lệnh có GPU được A duyệt 12:35.

```bash
# (a) mặc định production
uv run python -I -c "inspect CrossEncoder.__init__ max_length default"            # sentence-transformers 5.6.1
uv run python -I -c "CrossEncoderReranker() → max_length, loaded_device"            # MiniLM, CPU
uv run python -m pytest tests/test_full_corpus_retrieval.py -q
uv lock --check --offline
# (b) tính lại từ JSONL của B
uv run python -m experiments.phase_8_1.g4_rerank compare --a base_runtime --b a_m1_plain a_m1_section a_m2_plain \
  a_m2_section a_luna_plain --metrics context5_gold_all mrr context5_gold_frac ndcg
uv run python -m experiments.phase_8_1.g4_rerank compare --a base_runtime   --b b_m1_plain_p100 --metrics context5_gold_all mrr top10_gold_all
uv run python -m experiments.phase_8_1.g4_rerank compare --a base_native100 --b b_m1_plain_p100 --metrics context5_gold_all mrr top10_gold_all ndcg
uv run python -m experiments.phase_8_1.g4_rerank compare --a base_runtime   --b base_native100 --metrics context5_gold_all mrr
uv run python -m experiments.phase_8_1.g4_rerank summary --names base_runtime base_native100 a_m1_plain a_m1_section \
  a_m2_plain a_m2_section a_luna_plain b_m1_plain_p100 --realism natural
# (c) lượt GPU kiểm lại (nvidia-smi trước: 0 tiến trình, 0 MiB; dòng "đang giữ GPU" trong STATUS_C, đã xóa sau)
uv run python -m experiments.phase_8_1.g4_rerank run --name c_rerun_m1 --cases pilot --input top10 --reranker m1 --text plain --device cuda
# (d) đếm đầu vào pool 100 trên dev 30 (Qdrant chỉ đọc) — m1
```

## 4. Kết quả quan sát

**(a) Code production giữ hành vi mặc định:**
- `CrossEncoder.__init__` mặc định `max_length=None` (sentence-transformers 5.6.1), nên `CrossEncoderReranker(...,
  max_length=None)` truyền đúng giá trị mặc định.
- `CrossEncoderReranker()` sau khi nạp: `max_length` 512, `loaded_device` `cpu`, `CrossEncoder.max_length` 512. Không
  đổi.
- `loaded_device` chỉ được harness dùng. Runtime gọi `CrossEncoderReranker()` không tham số (`full_corpus.py:829`), và
  settings hiện là `reranker: none`.
- pytest `test_full_corpus_retrieval.py`: **26 passed**, gồm `test_cross_encoder_primitives_contract`.
- `uv lock --check --offline`: **exit 0** (211 gói); `sentencepiece` 0.2.2 cài trong `.venv`.
- Mốc byte retrieval `cefb2d1a…` sau sửa: **dùng lại bằng chứng của B**, không chạy lại. Lý do: thay đổi chỉ chạm lớp
  reranker, mà đường `dense_bm25_rrf` với `reranker: none` không gọi tới lớp này.

**(b) Số trong report — khớp hết** (C tính lại; mọi biến thể n = 30):

| So sánh | `context5_gold_all` | MRR@10 | Kết luận |
|---|---|---|---|
| G4-A M1 trơn vs runtime | +0,067 [−0,067; 0,200] 3/26/1 | +0,105 [0,024; 0,201], Holm 0,024 | kém hơn (mất câu 16) ✓ |
| G4-A M1 kèm mục | −0,033, 2/25/3 | +0,027 | kém hơn ✓ |
| G4-A M2 trơn / kèm mục | −0,033, 2/25/3 | +0,018 / +0,035 | kém hơn ✓ |
| G4-A luna | +0,100 [0,000; 0,233] 3/27/0 | +0,172 [0,092; 0,261], Holm < 0,001 | chưa rõ ✓ |
| G4-B vs runtime | +0,133 [0,000; 0,300] 5/24/1 | +0,140 [0,054; 0,239] | kém hơn (mất câu 16) ✓ |
| G4-B vs native p100 không rerank | +0,033 [−0,067; 0,133] 2/27/1 | +0,112 [0,021; 0,214] | không khác ⇒ chưa thấy đóng góp reranker ✓ |
| native p100 vs runtime | +0,100 [−0,033; 0,233] 4/25/1 | +0,028 [0,004; 0,056] | khớp §4.4 ✓ |

- Chỉ số phụ khớp: luna `context5_gold_frac` +0,133 [0,066; 0,206] 10/20/0, nDCG +0,130; M1 trơn nDCG +0,075 (Holm 0,01);
  G4-B vs native nDCG +0,084.
- Áp luật ghi trước, kết luận đúng:
  - M1 / M2 vi phạm sàn "0 câu mất", nên **kém hơn**;
  - luna có cận dưới CI `context5` = 0 (đúng trần §1.2), nên **chưa rõ**; MRR@10 là tín hiệu;
  - G4-B so mốc native: `context5` không khác.
- Không có nhánh nào "tốt hơn", nên không chạy test. Đúng plan.
- **Luật chọn G4-B (§4.3):** C tính lại từ JSONL.
  - `context5_gold_frac`: M1 trơn 0,651 / M1 kèm mục 0,619 / M2 trơn 0,598 / M2 kèm mục 0,590.
  - `context5_gold_all`: M1 trơn 14 / các biến thể còn lại 11.
  - Chênh 3 > 1 nên chỉ chạy M1. Đoạn kèm mục ở pool 100 dừng ở câu đầu, nên dùng đoạn trơn. Đúng `choose_rule`.
- **Câu mất:** G4-A M1 trơn và G4-B đều làm mất đúng câu 16. Ở G4-B, câu 16 vẫn đủ đoạn đúng trong top-10 nhưng rơi khỏi 5
  đoạn đưa model. Khớp report.
- **Luna:** `a_luna_plain.jsonl` = `_pilot` + `_rest` nối từng byte (30 dòng). 0/30 lỗi, mọi `order` là hoán vị đúng. Tổng
  USD theo từng câu là 0,0087972, khớp §5 và meta.
- **"Chỉ natural"** (11 câu, nhãn sha `0b65d1c138d2`, đúng file A cập nhật): `context5` / MRR@10 = runtime 0,455 / 0,345 ·
  native100 0,364 / 0,374 · M1 trơn 0,364 / 0,538 · M1 kèm mục 0,364 / 0,413 · M2 trơn 0,273 / 0,402 · M2 kèm mục 0,364 /
  0,455 · luna 0,455 / 0,591 · G4-B 0,364 / 0,586. Khớp bản `d99341dc66c6`.

**(c) Kiểm GPU và giới hạn lượt:**
- Cả 13 lượt GPU của B (8 pilot + 4 G4-A + 1 G4-B) đều có `gpu_check`: `cuda_available` True, `model_device` `cuda:0`, `gpu_pids` đúng một pid =
  `own_pid`, `memory_used_mib` 2253.
- Điều 4 (thời gian cỡ GPU): top-10 đoạn trơn trên GPU p50 ~0,85 s, trên CPU ~4,9 s.
- Mọi lượt ≤ 30 câu; harness có chặn `MAX_GPU_CASES`.
- Hai lượt "đoạn kèm mục" pool 100 dừng vì câu đo đầu > 60 s (165 s, 167 s), đúng luật. Lượt dài nhất ~5,7 phút, dưới
  trần 20 phút.
- **Lượt GPU kiểm lại của C** (12:36:51–12:37:04):
  - `gpu_check` đạt (pid riêng, `cuda:0`); p50 / p95 cả luồng 822 / 1155 ms;
  - **10/10 câu giống hệt** lượt `p0_gpu_m1_top10_plain` của B, và giống 10 câu tương ứng trong `a_m1_plain`, ở top-10,
    context, MRR / nDCG và độ phủ đoạn đúng (bỏ các trường thời gian);
  - kết quả M1 trên GPU tất định;
  - sau lượt, `nvidia-smi` không còn tiến trình nào.
  - File: `data/phase_8_1/g4/c_rerun_m1.jsonl` + `.meta.json` (tên mới, không ghi đè file của B).

**(d) Đầu vào pool 100:** 112–192 đoạn/câu (m1).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại lượt luna (có trả tiền) hay lượt pool 100 trên GPU. Kết quả của chúng chỉ kiểm từ JSONL và meta.
- Không chạy lại mốc byte retrieval (dùng lại bằng chứng của B, lý do ở §4a).
- Cỡ mẫu 30 câu và trần 3 câu của G4-A là giới hạn của thiết kế (ghi trước ở plan §1.2), không phải lỗi thực hiện.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** Thực hiện đúng plan `a4adfc8eedd9`. Đổi production nhỏ và giữ hành vi mặc định. Mọi số
khớp khi tính lại, và lượt GPU chạy lại cho ra đúng kết quả. B sửa m1, m2 bằng lời trong report (không cần chạy lại), rồi A
đóng G4.

Ý nghĩa cho User (giữ nguyên lời của B ở report §4.5):
- M1 / M2 làm mất đoạn đúng của 1–3 câu, nên chưa dùng được.
- Luna không làm mất câu nào và thứ tự tốt lên rõ, nhưng 30 câu chưa đủ để gọi là tốt hơn.
- Mở rộng vùng tìm (hợp hai nhánh, ~150 đoạn) tự nó đã giúp phần lớn; reranker M1 thêm chủ yếu ở thứ tự.

Tiền (C): **0 USD**. GPU: 1 lượt 10 câu, ~13 s.
