# Review: Phase 8.1 G0.1–G0.2 — chia nhóm thử/kiểm + so sánh theo cặp (C16)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 3 minor + 1 ghi chú)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-b0`)
Date: 2026-10-24 21:08–21:15 +0700 (lấy bằng `date`)
Canonical guide: `guides/full_corpus_rag.md` (không đổi)
Implementation report: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g0_1_2_measure_implementation.md`
Việc: `session_prompt/CURRENT_HANDOFF.md` "### C16"; spec 8.1 §3.4, §5 G0.1–G0.2, §6.1

## 1. Phạm vi đã review

- Cổng tối thiểu: `git status` (2 file của C: `backend/evaluation/full_corpus_eval.py`,
  `backend/tests/test_full_corpus_eval.py`, khớp report; các file `M` khác là B11 của B và governance);
  đọc **exact diff** cả hai file; `git diff --check` sạch; đối chiếu với mục việc C16 và spec.
- File private `knowledge-base-hue/evaluation/phase_8_1/split.json` (chỉ đọc số, không chép câu hỏi).
- Đọc thêm phần không nằm trong diff mà diff dựa vào: `RETRIEVAL_K`, `answer_keywords`, `context-coverage`.

## 2. Findings

Không có blocker hoặc major. Code trực tiếp, theo được data flow (đọc file → `row_metrics` → chênh theo
cặp → bootstrap → kết luận); không có abstraction thừa. Thay đổi output của `compare` đã khai báo, repo không
có chỗ nào đọc output đó.

- **m1 (minor) — chia cho 0 ở `row_metrics`** (`full_corpus_eval.py`, nhánh `found_`): `found / row["answer_keywords"]`
  sẽ `ZeroDivisionError` nếu một câu trong kho có 0 keyword mang đáp án. Golden hiện tại: B kiểm bằng máy, **0
  câu** như vậy, nên không ảnh hưởng kết quả hôm nay. Rủi ro khi chạy `context-coverage` trên bộ câu mới (30–40
  câu kín, G0.4). Tiêu chí đóng: câu 0 keyword đáp án bị bỏ khỏi `evidence_rate` (hoặc báo lỗi rõ có số case),
  không crash.
- **m2 (minor) — case lỗi kỹ thuật bị loại lặng lẽ khỏi `compare`:** `row_metrics` trả `{}` khi có `error`,
  nên case đó biến mất khỏi phép so; chỉ thấy qua `n`. Luật 7A/7B: lỗi kỹ thuật làm run *incomplete*. Tiêu chí
  đóng: `compare` in số case bị loại vì lỗi ở mỗi bên (một con số là đủ).
- **m3 (minor) — `compare` với file A rỗng:** `a_rows[0]` → `IndexError`. Không gặp thực tế; sửa chung với m2
  nếu tiện, không cần vòng riêng.
- **Ghi chú (không cần sửa):** metric nhị phân thưa (từ chối nhầm, lỗi citation) với percentile bootstrap dễ cho
  CI chạm 0 (ví dụ Đủ nhóm kiểm [0,000; 0,054]), nên "không khác" ở đó nên đọc cùng thắng/hòa/thua. Đúng quy
  ước spec ("CI chứa 0"), report C đã nêu. Cluster bootstrap theo file chưa làm — C đã ghi giới hạn, đồng ý.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `uv` trong `.venv` dự án, `HF_HUB_OFFLINE=1`, Qdrant chỉ đọc, 0 USD. Output ở `/tmp/b11/`.

1. `uv run python -m pytest -p no:cacheprovider tests/test_full_corpus_eval.py tests/test_golden_full_corpus.py -q`
2. Kiểm độc lập `split.json` bằng script nhỏ (đọc Golden qua `load_golden_cases`): số câu, giao/hợp, khóa từng
   case so `question_key`, quota theo loại, smoke; dựng lại bằng `make_split(cases, 56, 20261024)` rồi so; đếm câu
   trong kho có 0 keyword đáp án.
3. Đối chứng âm nhóm kiểm: `compare --a claude_run1.jsonl --b claude_run2.jsonl --split <split.json> --group test`.
4. Đối chứng dương: `retrieval --shuffle-seed 81 --out /tmp/b11/c16_shuffled_81.jsonl`, rồi `compare` với
   `/tmp/b11/retrieval_after.jsonl` (lượt baseline B chạy ở B11, giống từng byte mốc 7B); tính tay chênh MRR.
5. `holm_adjust([0.01, 0.04, 0.03])` và `verdict` cho metric "thấp hơn là tốt".
6. `retrieval` mặc định bằng **code working tree** (C16 + B11) → `cmp` với `retrieval_dense_bm25_rrf_1.jsonl`.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Pytest 2 file | **PASS** 27 passed |
| `split.json` | **PASS**: thử 120 / kiểm 56, giao 0, hợp = 176 case; 176 khóa khớp, không trùng; nhóm kiểm theo loại 24/9/9/8/6 = quota; smoke 7 thử / 3 kiểm, đủ 10; dựng lại từ seed **giống hệt** |
| Đối chứng âm (nhóm kiểm, Claude Run 1 vs 2) | **PASS**: Đúng 0 [0; 0], Đủ +0,018 [0,000; 0,054], Trúng ý 0 [−0,071; 0,071]; mọi loại câu `no_difference` (n=56) |
| Đối chứng dương (xáo top-10 seed 81) | **PASS**: MRR 0,721 → 0,418, CI [−0,354; −0,252], 17/25/116 `worse`; nDCG 0,755 → 0,538 [−0,253; −0,181] `worse`; Coverage không đổi [0; 0]; cùng tập 10 đoạn mỗi case; chênh MRR tính tay −0,303 khớp — **trùng số report C** |
| Holm / chiều metric | đúng: `[0.03, 0.06, 0.06]`; `false_refusal` CI âm ⇒ `better`, MRR CI âm ⇒ `worse` |
| Retrieval mặc định với code C16 + B11 | **PASS** giống từng byte mốc 7B (`cefb2d1a…`) |
| `git diff --check` | sạch |

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại đối chứng âm cho file câu trả lời (`run1_answers` vs `run2_answers`) và retrieval lần 1 vs 2 —
  report C có; phép so dùng cùng hàm đã kiểm ở mục 4. Không chạy lại `context-coverage`.
- Không kiểm nhánh `--b` nhiều biến thể qua CLI (chỉ kiểm hàm `holm_adjust`).

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation`. G0.1–G0.2 đạt tiêu chí spec §6.1 phần "tự kiểm thống kê (đối chứng âm +
dương) đạt": đối chứng âm ra "không khác" ở mọi metric, đối chứng dương ra "kém hơn" ở MRR/nDCG, file chia
đúng và tái lập được. 3 minor không chặn; m1 nên sửa trước G0.4 (bộ câu mới). Việc trung bình ⇒ A đóng gate
và báo User. B không sửa code của C.
