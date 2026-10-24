# Review: Phase 7B Gate 4 — baseline full-corpus 176 case

Decision: ready_for_user_confirmation (có điều kiện: tiêu chí 5 — User chấm mẫu 20 case — còn NOT RUN)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-d9`)
Date: 2026-10-24
Spec: `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` §4.2, §4.4, §7
Implementation report: `reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md` (B)

Review không chép câu hỏi, đáp án, câu trả lời hay feedback; chỉ số tổng hợp.

Lưu ý độc lập: C là người chấm Claude (Gate 3). Review này kiểm việc **tổng hợp** của B
(Gate 4), không tự kiểm lại chất lượng điểm Claude; độ tin của điểm Claude được đo bằng số
nhiễu/khớp ở §4 và mốc User (còn chờ).

## 1. Phạm vi đã review

- Cổng tối thiểu: `git log` HEAD `f80737a`; `git status` — report Gate 4 untracked (mới), tracked
  chỉ đổi `session_prompt/CURRENT_HANDOFF.md`, `sessions/STATUS_B.md`, `sessions/STATUS_C.md`
  (trạng thái). **Không có thay đổi code** — khớp report §1 ("không đổi code"). `git diff --check`
  sạch (tracked + report mới).
- Đọc toàn bộ report Gate 4; script phân tích `/tmp/phase7b_b6/extra.py` (chỉ đọc file private,
  in số tổng hợp — không ghi gì); `subsets.json`, `user_scoring_map.json` (chỉ chỉ số case).
- Đối chiếu từng số ở report §4–6 với lần chạy lại của C (§3 dưới).
- Kiểm đường runtime của evaluator (tiêu chí 1) bằng đọc `backend/evaluation/full_corpus_eval.py`.

## 2. Findings

Không có blocker hoặc major.

- **m1 (minor) — report §5.1, cách diễn đạt về nhiễu retrieval.** Report ghi "chưa có ngưỡng
  nhiễu cho retrieval". Nhưng retrieval tất định: hai lần `dense_bm25_rrf` giống từng byte (C
  kiểm lại: `cmp` bằng nhau), nên nhiễu chạy-lại = 0. Điều chưa biết là chênh 0,005–0,011 giữa
  `native_hybrid_rrf` và runtime có vượt **biến thiên do mẫu 158 case** không (cần so cặp theo
  case). Tác động: người đọc Phase 8 có thể hiểu nhầm là retrieval có nhiễu chạy-lại. Tiêu chí
  đóng: sửa câu thành "retrieval tất định; chênh nhỏ, chưa kiểm ý nghĩa thống kê theo cặp trên
  158 case". Không chặn.
- **m2 (minor) — report §3, lệnh `compare --cases <rerun_30>` là placeholder.** Người chạy lại phải
  tự lấy danh sách từ `subsets.json`. Tiêu chí đóng: ghi cách lấy (ví dụ "`--cases` = 30 số trong
  `subsets.json` → `rerun_30`") hoặc lệnh đầy đủ. Không chặn.
- **m3 (minor, thông tin) — report §6, chi phí judge Claude "0 API".** Đúng là không tốn tiền API,
  nhưng đã dùng quota Claude Code (39 sub-agent × ~29k token ≈ 1,1M token, theo report Gate 3).
  Có thể thêm một chú thích để Phase 8 ước lượng quota khi chấm lại nhiều cấu hình. Không chặn.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, đều free, chỉ đọc file private trong `data/evaluation/phase_7b/`:

```bash
E="uv run python -m evaluation.full_corpus_eval"
R30="6 9 17 18 24 39 40 42 50 51 56 58 61 84 87 92 96 98 102 104 108 110 113 117 119 121 131 136 160 164"  # subsets.json rerun_30
$E summarize --retrieval retrieval_dense_bm25_rrf_1.jsonl --answers run1_answers.jsonl --scores claude_run1.jsonl
$E summarize --answers run2_answers.jsonl --scores claude_run2.jsonl
$E summarize --answers run1_answers.jsonl --scores run1_judge_luna.jsonl
$E summarize --retrieval retrieval_native_hybrid_rrf_1.jsonl
$E summarize --answers smoke_answers_1.jsonl --scores smoke_judge_luna_1.jsonl
$E summarize --answers run1_answers.jsonl --scores run1_judge_luna_rerun30.jsonl
$E compare --a claude_run1.jsonl     --b claude_run1_rerun30.jsonl     --cases $R30
$E compare --a run1_judge_luna.jsonl --b run1_judge_luna_rerun30.jsonl --cases $R30
$E compare --a claude_run1.jsonl     --b claude_run2.jsonl
$E compare --a claude_run1.jsonl     --b run1_judge_luna.jsonl
uv run python /tmp/phase7b_b6/extra.py
cmp data/evaluation/phase_7b/retrieval_dense_bm25_rrf_{1,2}.jsonl   # từ repo root
```

Thêm một script chỉ đọc nhỏ (không lưu) đếm từ chối nhầm/lỗi citation theo category từ
`run{1,2}_answers.jsonl` và so `user_scoring_map.json` với `subsets.json`.

## 4. Kết quả quan sát

### 4.1 Số trong report so với chạy lại

| Report | Mục | Chạy lại | Khớp |
|---|---|---|---|
| §4.1 | 6 metric tổng + 5 category (Claude Run 1; retrieval 158) | `summarize` s1: A/C/R 4,426/4,284/4,455; MRR 0,721, nDCG 0,755, KC 92,35; từng category đúng tới 3 chữ số | ✓ |
| §4.2 | Từ chối đúng 18/18; từ chối nhầm 22/158 = 0,139 (multi 11, comp 8, direct 2, cond 1); Run 2 cùng 22 case | `summarize` + đếm: đúng; tập case từ chối nhầm Run 1 = Run 2 | ✓ |
| §4.2 | Lỗi citation 4/176 (direct 2, cond 1, multi 1); Run 2 6/176 | rate 0,0227 / 0,0341; đếm theo category đúng | ✓ |
| §4.3 | 121 × 5/5/5, 22 × 1/1/1, 33 khác; histogram 3 metric; 22 case 1/1/1 = đúng 22 từ chối nhầm (Claude R1, R2, luna) | `extra.py`: đúng | ✓ |
| §4.4 | Bỏ từ chối nhầm: 4,916/4,753/4,948 (n=154) + 4 category; trong phạm vi được trả lời 4,904/4,721/4,941 (n=136), 103 case 5/5/5; citation lỗi 5,0/4,75/5,0 | `extra.py`: đúng; "≈85%" = (4,916−4,426)/(5−4,426) = 0,854 | ✓ |
| §5 | Nhiễu judge Claude (30), luna (30), cả đường (176), Claude→luna (176): mọi chênh TB / trùng / ≤1 / ≥2 | 4 lệnh `compare`: đúng tới 3 chữ số; không thiếu case ở A/B | ✓ |
| §5 | 16/176 case đổi ≥1 metric; 64 câu trả lời trùng chữ, 1 trong đó đổi điểm | `extra.py`: đúng | ✓ |
| §5.1 | native 0,726/0,761/93,41 | `summarize` sn: 0,7263/0,7613/93,41 | ✓ |
| §6 | Tiền: smoke 0,00282 (20 call), Run 1 0,02387, Run 2 0,02410, luna R1 0,02651, luna 30 0,00474; tổng 0,08203 | usage trong `summarize`: smoke 0,0013174+0,0015013 = 0,0028187 (19.107 in / 1.816 out); các dòng còn lại đúng; tổng 0,08204 (làm tròn) | ✓ |
| §2 | `user_scoring.md` gồm đúng 20 case `user_20`, rời `rerun_30` | `user_scoring_map.json`: 20 case = `user_20`; giao với `rerun_30` rỗng. (Không kiểm "là Run 1" — map không ghi run.) | ✓ (một phần) |

### 4.2 Tiêu chí nghiệm thu spec §7

| # | Tiêu chí | Bằng chứng | Kết quả |
|---|---|---|---|
| 1 | Evaluator chạy đúng đường runtime | `full_corpus_eval.py:37–40,204–221,306`: dùng `build_full_corpus_retrieval_service` với `settings["full_corpus_runtime"]`, `FullCorpusContextBuilder` với `max_context_documents` từ settings, `OpenAIFullCorpusGenerator` — cùng component/config với API | PASS |
| 2 | Retrieval 158 case (bỏ `out_of_scope`) hai lần giống hệt | `cmp` hai file retrieval: giống từng byte | PASS |
| 3 | Run 1, Run 2 đủ case không lỗi kỹ thuật | `summarize`: 176 case, `technical_errors` 0, `complete` true (cả hai run) | PASS |
| 4 | Claude chấm đủ; luna đủ; điểm số nguyên 1–5 | `score_errors` rỗng: Claude R1/R2 (176), Claude 30, luna R1 (176), luna 30 | PASS |
| 5 | User chấm xong mẫu; khớp giữa các nguồn, nhiễu judge, nhiễu cả đường | Nhiễu judge + cả đường + Claude–luna: có, khớp. **Khớp với User: NOT RUN** (User chưa chấm) | PARTIAL |
| 6 | 6 metric + 2 tỉ lệ từ chối, tổng + theo category; tiền ≤0,6 USD; ghi giới hạn | §4.1–4.2 đủ; 0,082 USD; §7 ghi Golden do LLM viết, keyword proxy, judge LLM, mẫu User nhỏ, hiệu ứng trần | PASS |
| 7 | Không lộ nội dung private; `git diff --check` sạch | Report chỉ số tổng hợp, case_index và tên file; grep không thấy câu hỏi/trích dẫn; `git ls-files data knowledge-base-hue` rỗng; diff-check sạch | PASS |
| 8 | Review chéo `ready_for_user_confirmation`; User đóng | Review này; User đóng — chờ | chờ User |

### 4.3 Giới hạn trong report có trung thực không

Có. Report nêu đúng các điểm A yêu cầu: hiệu ứng trần (121/176 đạt 5/5/5, điểm tổng bị chi phối
bởi 22 từ chối nhầm 1/1/1 — C xác nhận bằng `extra.py`), Golden do LLM viết, keyword là proxy,
judge là LLM, mẫu User nhỏ và chỉ Run 1, nhiễu đo trên một cặp run, lỗi citation đứng riêng
không trừ điểm, tiền là cận trên (không trừ cache, chưa đối chiếu dashboard). Report ghi rõ phân
tích §4.4 là quan sát, nguyên nhân từ chối nhầm dẫn sang B4.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại sinh/judge luna (paid) — chỉ đối chiếu tổng hợp trên file đã có; đúng phạm vi
  Gate 4 (B không gọi paid).
- Không kiểm "20 câu trả lời trong `user_scoring.md` là của Run 1" (map chỉ ghi case_index; không
  mở nội dung file chấm).
- Không đánh giá lại chất lượng từng điểm judge (C là người chấm Claude ở Gate 3).
- Tiêu chí 5 phần User: NOT RUN, chờ User chấm `user_scoring.md`.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation**, có điều kiện:

- Số baseline (Claude Run 1): A/C/R 4,426 / 4,284 / 4,455; MRR@10 0,721, nDCG@10 0,755, Keyword
  Coverage@10 92,35 (158 case); từ chối đúng 1,000, từ chối nhầm 0,139; lỗi citation 0,023;
  tiền 0,082 USD. Thước đo ổn định: nhiễu cả đường ≤0,011 mọi metric, 0 case lệch ≥2; Claude–luna
  lệch ≤1 ở ≥99,4%.
- **Điều kiện đóng:** User chấm 20 case `user_20` → B chạy `parse-user-scores` + 3 `compare`
  (report §5) và cập nhật report; nếu Claude lệch User có hệ thống (chênh TB ≥1 ở một metric)
  thì A báo User trước khi coi điểm Claude là chính thức (spec §4.4). Phần cập nhật đó cần kiểm
  lại (chỉ phần User).
- Minor m1–m3 sửa cùng lượt cập nhật phần User; không mở vòng sửa riêng.
- Việc rủi ro cao (quyết định chất lượng): A trình User; User đóng Phase 7B. Phase 8 vẫn đóng
  cho tới khi User đóng 7B.
