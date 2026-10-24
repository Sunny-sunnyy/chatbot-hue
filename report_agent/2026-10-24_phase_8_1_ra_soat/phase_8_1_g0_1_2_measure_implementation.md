# Implementation Report: Phase 8.1 G0.1–G0.2 — chia nhóm thử/kiểm + so sánh theo cặp (C16)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-a3`)
Date: 24/10/2026, 20:50–21:01 (giờ lấy bằng `date`)
Spec: `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` (User duyệt 20:49) §3.4, §5
G0.1–G0.2, §6.1. Việc: `session_prompt/CURRENT_HANDOFF.md` "### C16". Review: B.

## 1. Phạm vi

- **G0.1:** chia 176 câu Golden thành 120 câu thử / 56 câu kiểm, phân tầng theo `category`, seed cố
  định. Ghi file private. Không sửa Golden chính thức.
- **G0.2:** sửa thước đo trong `backend/evaluation/full_corpus_eval.py`:
  - so sánh theo cặp: paired bootstrap 10.000 lần, CI 95%, thắng/hòa/thua, theo loại câu; lọc theo
    nhóm thử/kiểm; Holm khi có >1 biến thể;
  - macro theo loại câu;
  - bảng từ chối 2×2;
  - metric bằng chứng @5 đưa vào phép so;
  - tự kiểm đối chứng âm và đối chứng dương.
- **Không làm:** sửa retrieval/generator/pipeline (việc B11 của B); paid; ghi Qdrant.

## 2. Thay đổi chính

Chỉ 2 file code của C: `backend/evaluation/full_corpus_eval.py` (+224/−10),
`backend/tests/test_full_corpus_eval.py` (+69).

| Thay đổi | Mục đích |
|---|---|
| `question_key`, `make_split`, `split_group_indexes`; lệnh CLI `split` | Chia phân tầng. Mỗi loại lấy số câu kiểm tỉ lệ với cỡ loại; làm tròn theo phần dư lớn nhất để tổng đúng 56; chọn câu trong loại bằng xáo theo seed. Mỗi câu có khóa = 12 ký tự SHA-256 câu hỏi NFC. Khi dùng nhóm, khóa lệch thì raise (không dùng nhầm Golden đã đổi). File chia ghi thêm 10 câu smoke nằm ở nhóm nào |
| `row_metrics` | Đọc giá trị từng case từ mọi loại file kết quả: điểm judge (Đúng/Đủ/Trúng ý), retrieval (MRR/nDCG/Coverage), câu trả lời (`false_refusal` câu trong kho, `correct_refusal` câu ngoài kho, `citation_error`), context-coverage (`evidence_rate_<N>` = tỉ lệ keyword đáp án trong N đoạn đưa model). Bỏ case lỗi kỹ thuật |
| `bootstrap_mean_diff`, `verdict`, `paired_compare` | Chênh B − A trên đúng các case cả hai cùng có; CI 95% percentile (10.000 lần, seed 20261024, numpy); p hai phía; thắng/hòa/thua; kết luận `better` / `worse` / `no_difference` (CI chứa 0 ⇒ không khác). `LOWER_IS_BETTER` cho từ chối nhầm và lỗi citation. Có tổng + từng loại câu |
| `holm_adjust`, `compare_variants`; lệnh `compare` mới | `--b` nhận nhiều biến thể; >1 biến thể thì thêm `p_holm` + `verdict_holm` trên dòng tổng. `--split … --group dev\|test` lọc nhóm. Với file điểm judge, vẫn in thêm phần "mức khớp" cũ (`compare_scores`, giữ nguyên) dưới khóa `judge_agreement` |
| `mean_by_category` thêm khóa `macro` | Trung bình các trung bình loại câu (mỗi loại nặng như nhau). Sửa docstring cũ ghi nhầm "macro-average theo case" (C11 7B.4): `overall` là trung bình theo case |
| `refusal_rates` thêm `matrix` | Bảng 2×2: ngoài kho / trong kho × từ chối / trả lời |
| `run_retrieval_eval(..., shuffle_seed)`; lệnh `retrieval --shuffle-seed` | Chỉ cho đối chứng dương: xáo thứ tự top-10 mỗi case (`seed + case_index`), cùng tập đoạn. Mặc định `None` thì hành vi như cũ (đã kiểm byte, §4) |
| 4 test logic thuần mới + mở rộng 2 test cũ | Chia đúng quota/tất định/khóa lệch; so theo cặp: giống hệt ⇒ không khác, chiều tốt/xấu, `LOWER_IS_BETTER`, bỏ case lỗi; Holm; macro; bảng 2×2 |

**Thay đổi output của lệnh `compare`:** trước in thẳng kết quả "mức khớp"; nay in
`{"paired": {...}, "judge_agreement": {...}}`. Không có script nào trong repo đọc output này
(chỉ in ra stdout).

## 3. Cách đã chạy thật

Từ `backend/`, `uv` trong `.venv` dự án, `HF_HUB_OFFLINE=1`. Qdrant chỉ đọc, 0 USD.

```bash
uv run python -m pytest -p no:cacheprovider tests/test_full_corpus_eval.py tests/test_golden_full_corpus.py -q
uv run python -m evaluation.full_corpus_eval split --seed 20261024 --out ../knowledge-base-hue/evaluation/phase_8_1/split.json
# đối chứng âm (dữ liệu 7B có sẵn), cho nhóm all / --split … --group dev / --group test
uv run python -m evaluation.full_corpus_eval compare --a claude_run1.jsonl --b claude_run2.jsonl [--split S --group G]
uv run python -m evaluation.full_corpus_eval compare --a run1_answers.jsonl --b run2_answers.jsonl [...]
uv run python -m evaluation.full_corpus_eval compare --a retrieval_dense_bm25_rrf_1.jsonl --b retrieval_dense_bm25_rrf_2.jsonl [...]
# retrieval sau khi sửa code: phải giống byte mốc 7B; rồi đối chứng dương
uv run python -m evaluation.full_corpus_eval retrieval --out /tmp/c16/retrieval_baseline.jsonl
cmp /tmp/c16/retrieval_baseline.jsonl ../data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl
uv run python -m evaluation.full_corpus_eval retrieval --shuffle-seed 81 --out /tmp/c16/retrieval_shuffled_81.jsonl
uv run python -m evaluation.full_corpus_eval compare --a /tmp/c16/retrieval_baseline.jsonl --b /tmp/c16/retrieval_shuffled_81.jsonl [...]
# metric bằng chứng @5 và nhánh Holm (2 biến thể)
uv run python -m evaluation.full_corpus_eval context-coverage --sizes 5 10 --out /tmp/c16/coverage.jsonl
uv run python -m evaluation.full_corpus_eval compare --a /tmp/c16/coverage.jsonl --b /tmp/c16/coverage.jsonl
uv run python -m evaluation.full_corpus_eval compare --a /tmp/c16/retrieval_baseline.jsonl --b /tmp/c16/retrieval_shuffled_81.jsonl retrieval_dense_bm25_rrf_2.jsonl
uv run python -m evaluation.full_corpus_eval summarize --retrieval retrieval_dense_bm25_rrf_1.jsonl --answers run1_answers.jsonl --scores claude_run1.jsonl
```

Output tạm ở `/tmp/c16/` (có thể mất). File chia ở
`knowledge-base-hue/evaluation/phase_8_1/split.json` (private, `.gitignore` bỏ qua; SHA-256
`e2b1788d…0279`; Golden lúc chia SHA-256 `b90bf8da…bc70`).

## 4. Kết quả quan sát

**Test:** 27 passed (19 trong `test_full_corpus_eval.py`: 15 cũ + 4 mới; 8 của `test_golden_full_corpus.py`).
`git diff --check` sạch.

**G0.1 chia nhóm** (seed 20261024): nhóm thử 120 / nhóm kiểm 56.

| Loại câu | Tổng | Nhóm kiểm |
|---|---:|---:|
| `direct_fact` | 75 | 24 |
| `multi_source` | 29 | 9 |
| `conditional` | 29 | 9 |
| `comparative` | 25 | 8 |
| `out_of_scope` | 18 | 6 |

- Smoke 10: 7 câu ở nhóm thử, 3 câu ở nhóm kiểm.
- 22 câu từ chối nhầm của 7B: 15 ở nhóm thử, 7 ở nhóm kiểm.
- Vì 6 câu `out_of_scope` của nhóm kiểm không tính vào truy xuất, retrieval nhóm kiểm là 50 câu, nhóm thử
  108 câu.

**Đối chứng âm** (cùng code, cùng input, hai lần chạy 7B): mọi metric đều `no_difference` ở cả tổng lẫn
từng loại câu, trên cả ba nhóm (all / thử / kiểm). **PASS**.

| So | Metric (all) | n | Chênh | CI 95% |
|---|---|---:|---:|---|
| Claude Run 1 vs Run 2 | Đúng / Đủ / Trúng ý | 176 | +0,006 / +0,011 / −0,006 | [−0,011; 0,028] / [−0,017; 0,046] / [−0,034; 0,023] |
| Câu trả lời Run 1 vs Run 2 | từ chối nhầm / từ chối đúng / lỗi citation | 158 / 18 / 176 | 0 / 0 / +0,011 | [0; 0] / [0; 0] / [−0,017; 0,040] |
| Retrieval lần 1 vs lần 2 | MRR / nDCG / Coverage | 158 | 0 / 0 / 0 | [0; 0] |

Ghi chú: ở nhóm kiểm, Đủ có CI [0,000; 0,054]. Cận dưới đúng bằng 0 nên tính là "không khác"; quy ước
"CI chứa 0" tính cả biên.

**Đối chứng dương** (xáo thứ tự top-10, seed 81): MRR và nDCG "kém hơn" rõ ở cả ba nhóm. Keyword
Coverage@10 không đổi (n=158, CI [0; 0]), đúng kỳ vọng vì cùng tập 10 đoạn. **PASS**.

| Nhóm | MRR A → B | CI 95% chênh | nDCG A → B | CI 95% chênh | thắng/hòa/thua (MRR) |
|---|---|---|---|---|---|
| all (158) | 0,721 → 0,418 | [−0,354; −0,252] | 0,755 → 0,538 | [−0,253; −0,181] | 17 / 25 / 116 |
| thử (108) | 0,731 → 0,431 | [−0,364; −0,238] | 0,757 → 0,546 | [−0,257; −0,167] | 13 / 21 / 74 |
| kiểm (50) | 0,699 → 0,391 | [−0,393; −0,230] | 0,750 → 0,521 | [−0,290; −0,172] | 4 / 4 / 42 |

**Retrieval sau khi sửa code:** `retrieval` mặc định giống **từng byte** mốc 7B
(`retrieval_dense_bm25_rrf_1.jsonl`, sha `cefb2d1a…`). Lần chạy này dùng working tree có cả thay đổi
B11 chưa commit của B ở `retrieval/full_corpus.py`, nên cũng là một quan sát phụ: với giá trị mặc định,
B11 không đổi retrieval runtime.

**Metric bằng chứng @5:** `context-coverage` → `compare` đọc được `evidence_rate_5` 0,853 và
`evidence_rate_10` 0,918 (n=158; tự so với chính nó ⇒ `no_difference`). Khớp số B5 (0,785 → 0,873 là
tỉ lệ case *đủ* keyword; ở đây là tỉ lệ keyword, nên không cùng đại lượng).

**Holm** (2 biến thể so cùng baseline): xáo top-10 p=0, p Holm=0 → `worse`; retrieval lần 2 p=1, p
Holm=1 → `no_difference`.

**Macro và 2×2** (dữ liệu 7B Run 1):

- macro retrieval (4 loại): MRR 0,676 / nDCG 0,712 / Coverage 89,76. Thấp hơn trung bình theo case
  0,721 / 0,755 / 92,35, vì so sánh và nhiều nguồn yếu.
- macro câu trả lời (5 loại): 4,31 / 4,14 / 4,33.
- bảng từ chối: ngoài kho 18 từ chối / 0 trả lời; trong kho 22 từ chối / 136 trả lời.

Tiền: **0 USD**.

## 5. Lỗi và giới hạn

- **p của bootstrap là xấp xỉ** (tỉ lệ lần bootstrap nằm phía bên kia 0, nhân 2). Với 10.000 lần, p
  nhỏ nhất phân biệt được là ~0,0002. Đủ cho Holm với vài biến thể.
- **Bootstrap theo câu, chưa theo cụm tài liệu.** Nghiên cứu §2/§12 gợi ý thêm "cluster bootstrap theo
  file" khi nhiều câu chung một nguồn. Spec 8.1 §3.4 chỉ yêu cầu theo cặp trên câu, nên chưa làm; ghi
  lại để cân nhắc nếu kết luận sát biên.
- Đối chứng dương mới kiểm phía retrieval. Phía điểm câu trả lời chưa có đối chứng dương (cần sinh câu
  trả lời cố ý kém, có phí); spec chỉ yêu cầu xáo top-10.
- `verdict_holm` chỉ tính trên dòng tổng, không tính cho từng loại câu.

## 6. Bàn giao cho người kiểm (B)

- **Đọc:** `git diff -- backend/evaluation/full_corpus_eval.py backend/tests/test_full_corpus_eval.py`.
  Không lẫn với diff B11 ở retrieval/generator/pipeline.
- **Chạy lại tối thiểu:**
  - pytest 2 file ở §3;
  - một lần `compare` đối chứng âm (`claude_run1` vs `claude_run2`, `--split … --group test`);
  - một lần đối chứng dương (`retrieval --shuffle-seed 81` rồi `compare`).
- **Kiểm file chia:** `split.json` có `dev` 120, `test` 56, `test_quota`, `keys` 176, `smoke`. Không chép
  câu hỏi ra report.
- Không commit (A commit).

## 7. Sửa theo review của B (`phase_8_1_g0_1_2_measure_review.md`, 21:12)

| Minor | Sửa |
|---|---|
| m1 `row_metrics` chia cho 0 khi `answer_keywords=0` | Case không có keyword mang đáp án thì không sinh `evidence_rate_*` (bỏ khỏi phép so, không coi là 0) |
| m2 `compare` loại case không có metric mà không báo | `paired_compare` trả thêm `excluded_cases: {a: [...], b: [...]}` (lỗi kỹ thuật hoặc không có keyword đáp án) |
| m3 `a_rows[0]` lỗi khi file A rỗng | Kiểm `a_rows` trước khi đọc dòng đầu |

Kiểm lại:

- `test_full_corpus_eval.py` 19 passed (một test mở rộng thêm 2 assert cho m1, m2).
- `compare` run1 vs run2 nhóm kiểm vẫn `no_difference`, `excluded_cases` rỗng.
- Pytest 15 file (lúc review B11) 195 passed.
- `git diff --check` sạch.

Logic thống kê không đổi, nên đối chứng âm/dương ở §4 vẫn đúng.
