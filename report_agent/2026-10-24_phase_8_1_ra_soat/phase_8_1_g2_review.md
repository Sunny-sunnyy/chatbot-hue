# Review: Phase 8.1 G2 — sinh câu trả lời (B17 bước 2, phần G2)

Decision: **ready_for_user_confirmation** cho toàn bộ G2 (0 blocker, 0 major; m1 đã đóng — §7, report bản `96db6e05d547`).
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a1`)
Date: 2026-10-25 13:13 (`date`)
Canonical guide: kế hoạch `phase_8_1_g2_g4_plan.md` bản duyệt `a4adfc8eedd9` §2, §2.1; spec 8.1 §5 G2
Implementation report: `phase_8_1_g2_implementation.md` sha **`56b6afa4c7ce`** (khớp tin B)

## 1. Phạm vi đã review

- **Diff:** chỉ `backend/experiments/phase_8_1/g2_generate.py` (mới, untracked, 383 dòng). C đọc hết. Không đổi production.
- **Đối chiếu code:**
  - harness gọi `answer_case`, `build_context_builder(settings, max_docs)`,
    `OpenAIFullCorpusGenerator.from_environment(answer_instructions, reasoning_effort)` của production;
  - chữ P1 / P2 thay đúng câu luật từ chối (có `assert` câu đó tồn tại), **khớp nguyên văn** plan §2 G2.2;
  - `DocOrderService` lấy đúng 5 đoạn mà builder sẽ lấy (`packed_chunk_ids`), xếp ổn định theo tài liệu;
  - `pooled_items` gộp câu trả lời giống hệt chữ theo (câu, câu trả lời), xáo theo seed, id mờ;
  - lô chấm chỉ có 4 trường `question`, `reference_answer`, `answer`, `case_index` (số mờ). C kiểm 456 item: **không lộ
    biến thể**;
  - `analyze`: chỉ số câu trả lời tính trên câu trong kho; guardrail out_of_scope, citation và USD tính trên cả 120 dev,
    đúng chữ §2.1 "trên 120 dev"; Holm trong nhóm cho Completeness và Accuracy.
- **Dữ liệu:** `data/phase_8_1/g2/*.jsonl` + `*.meta.json`, `judge/` (map sha `33b4c9603f20`), `judge_test/`.

## 2. Findings

Không có blocker hay major.

- **m1 (minor) — report chưa có kết quả G2.4 chạy đủ, đã chạy sau khi viết report.**
  - Bằng chứng: meta có thêm `g24_none_rest`, `g24_low_rest`, `g24_high_rest` (110 câu mỗi lượt, 13:06:19–13:09:39) và các
    file gộp `g24_{none,low,high}.jsonl` (13:07–13:10). Report sha `56b6afa4c7ce` ghi lúc 13:02 vẫn nói "chỉ pilot, chờ A".
  - A đã duyệt chạy đủ (`CURRENT_HANDOFF.md` dòng 255, ước 0,041 USD). Tiền thật 3 lượt: 0,0134288 + 0,0133858 +
    0,0162278 = **0,0430424 USD**, +5% so với ước. Mỗi lượt ≤ 0,05, nên đúng luật tiền.
  - Tổng G2 theo meta là **0,1565240 USD**, chứ không phải 0,1134816 như report §5. Cộng B17 (kể cả G4) = **0,1653212
    USD** ≤ 0,25.
  - **Đóng khi:** B thêm vào report §4.5 / §4.6 / §5 kết quả G2.4 đủ, chấm cùng quy trình mù, và tổng tiền mới. Sau đó C
    review phần thêm.

Ghi nhận, không phải finding:
- **Quy trình chấm khác 7B:** mỗi sub-agent chấm khoảng 40 câu (7B: 10). B đã ghi ở §6. Rủi ro thấp: mọi biến thể trộn chung
  trong cùng lô mù, nên không lệch giữa các biến thể. Model judge cùng 7B (Claude Opus 5.5), cùng prompt chấm, nên không
  phải "judge mới" theo skill §2.
- **Nhiễu tham chiếu "G2.0 vs 7B Run 1"** gộp cả sinh lại lẫn chấm lại bởi sub-agent khác. Đây không phải A/A thuần, B đã ghi
  đúng như vậy. Kết luận "tốt hơn" dựa trên CI theo cặp **trong cùng một lượt chấm mù**, nên hợp lệ.
- `t_context10_pilot`: `finished` (12:58:42) sớm hơn `started` (12:58:45). Hai mốc lấy bằng `time.strftime` ở cùng tiến trình,
  nên nghi đồng hồ WSL nhảy. Không ảnh hưởng số đo.
- **G2.1b** có lỗi citation tổng +2 (đúng ngưỡng), nhưng 6 câu lỗi mới / 4 câu hết lỗi. B báo đủ theo C23 m6.
- **G2.3** chính sách một nguồn không bao giờ áp dụng, vì mọi lượt đều có 5 (hoặc 10) nguồn. Lập luận đúng, phát lại khớp số
  đã lưu ở mọi file.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `HF_HUB_OFFLINE=1`. Không gọi API, không judge mới.

```bash
uv run python -m experiments.phase_8_1.g2_generate analyze --base g20_baseline --b g2_context10 g2_doc_order --realism main
uv run python -m experiments.phase_8_1.g2_generate analyze --base g20_baseline --b g2_p1_partial g2_p2_spec_rules --realism main
uv run python -m experiments.phase_8_1.g2_generate analyze --base t_baseline --b t_context10 --realism main --judge judge_test
uv run python -m experiments.phase_8_1.g2_generate analyze --base g20_baseline --b g2_context10 --realism natural
uv run python -m experiments.phase_8_1.g2_generate check-judge;  … check-judge --judge judge_test
uv run python -m experiments.phase_8_1.g2_generate replay-citation --files <7B run1, run2, g20_baseline, g2_context10, g2_doc_order, g2_p1_partial, g2_p2_spec_rules>
# + script python -I: cộng usage mọi *.meta.json, kiểm golden_md5 từng lượt, kiểm trường của lô chấm
```

## 4. Kết quả quan sát — khớp report

| Biến thể (dev số chính, 88 câu trong kho) | Completeness [CI], t/h/t, p Holm | Accuracy [CI] | từ chối nhầm | OOS bị trả lời | citation (mới / hết) | USD × | Kết luận |
|---|---|---|---|---|---|---|---|
| G2.1a context 10 | +0,261 [0,080; 0,477], 9/77/2, 0,007 | +0,273 [0,091; 0,500] | 13 → 7 | 0 → 0 | 4 → 4 (+2/−2) | 1,53 | tốt hơn ✓ |
| G2.1b xếp theo tài liệu | −0,023 [−0,068; 0,023], 1/84/3, 0,432 | −0,011 | 13 → 13 | 0 | 4 → 6 (+6/−4) | 1,00 | không khác ✓ |
| P1 trả lời một phần | +0,114 [−0,023; 0,250], 12/71/5, 0,227 | +0,170 [0,000; 0,352] | 13 → 1 | **0 → 2** | 4 → 3 (+2/−3) | 1,11 | kém hơn (sàn) ✓ |
| P2 2 luật spec | 0,000 [−0,068; 0,068], 2/84/2, 1,0 | +0,023 | 13 → 12 | 0 | 4 → 1 (+1/−4) | 1,00 | không khác ✓ |
| test: G2.1a (41 câu) | +0,268 [0,024; 0,585], 6/34/1 | +0,220 [−0,024; 0,537] | 3 → 1 | 0 | 4 → 4 (+3/−3) | 1,49 | xác nhận ✓ |

Chi tiết thêm:
- Nhóm (a) / (b) của G2.1a: (a) 13 câu, chênh 0; (b) 75 câu, +0,307 [0,093; 0,573].
- "Chỉ natural" G2.1a: 45 câu, +0,200 [0,044; 0,422], 5/40/0.
- `answer_type`: G2.1a 81 / 0 / 7; P1 70 / 17 / 1.
- **Áp luật ghi trước** (§2.1): G2.1a đủ 4 guardrail.
  - out_of_scope 0;
  - Accuracy cận trên ≥ 0 (thực tế tăng có CI);
  - citation +0 ≤ +2;
  - USD 1,53 ≤ 2×.

  Completeness có CI > 0 sau Holm, nên **tốt hơn**. Test cùng dấu, đủ guardrail, nên **đã xác nhận**. P1 vi phạm sàn
  out_of_scope, nên **kém hơn**. G2.1b và P2 **không khác**.
- **Judge:** `check-judge` cho 456/456 (dev) và 102/102 (test) điểm + nhãn, `score_errors` rỗng. `map.json` gồm 8 lượt, 630
  câu trả lời → 456 item.
- **G2.3:** `replay-citation` trên 7 file. `replay_matches_stored` = true ở cả 7; số lỗi 4 / 6 / 4 / 4 / 6 / 3 / 1; chính
  sách một nguồn đổi **0 câu**.
- **Golden:** mọi meta G2 ghi `golden_md5` bắt đầu `0f7dbf41b422` (Golden đã sửa).

## 5. Giới hạn hoặc phần chưa chạy

- Không chấm lại câu trả lời (judge quota). Điểm được dùng lại nguyên từ `judge/` và `judge_test/` của B: C chỉ kiểm đủ, mù
  và khớp phân tích.
- Không đọc nội dung câu trả lời / điểm từng câu (không cần cho các kết luận ở đây).
- G2.4 chạy đủ: chưa review (m1).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** cho G2.0–G2.3 + xác nhận test. Kết quả chính cho User: đưa 10 đoạn thay vì 5 làm câu trả
lời đầy đủ hơn (điểm Completeness +0,26 / 5 trên dev, +0,27 trên test) và gần nửa số từ chối nhầm biến mất; đổi lại tốn
thêm ~50% tiền mỗi câu. Đưa vào runtime là việc riêng, User duyệt.

Bước tiếp: B bổ sung G2.4 (m1), rồi C review phần thêm; A đóng G2.

Tiền (C): **0 USD**.

## 7. Review phần thêm G2.4 + đóng m1 (13:18)

B bổ sung report, bản **`96db6e05d547`**: §1, §4.5 viết lại, §4.6 thêm 3 dòng G2.4, lời thường, §5 (3 lượt rest + tổng mới,
ghi chú bản 13:02).

C kiểm lại (0 USD):
- `check-judge --judge judge_g24`: 360/360 điểm + nhãn, không lỗi. Map sha `38d237bc03df` gồm 4 lượt (`g20_baseline`,
  `g24_none`, `g24_low`, `g24_high`), 480 câu trả lời → 360 item.
- G2.0 được **chấm lại cùng lượt mù** với 3 mức, nên baseline và biến thể cùng người chấm. Đây đúng là cách A chốt cho G3 §9.3.
- `analyze --base g20_baseline --b g24_none g24_low g24_high --realism main --judge judge_g24`, khớp §4.5:

| Mức | Completeness [CI], t/h/t, p Holm | Accuracy [CI] | citation (mới / hết) | USD × | token ra TB | Kết luận |
|---|---|---|---|---|---|---|
| none | +0,136 [0,034; 0,261], 8/78/2, 0,031 | +0,227 [0,080; 0,398] | 4 → 8 (+7/−3) | 0,91 | 54,3 | kém hơn (citation +4 > +2) ✓ |
| low | +0,023 [−0,114; 0,148], 5/80/3, 1,0 | +0,102 | 4 → 9 (+8/−3) | 0,91 | 53,6 | kém hơn (citation +5 > +2) ✓ |
| high | +0,023 [0,000; 0,068], 1/87/0, 1,0 | +0,011 | 4 → 4 (+2/−2) | 1,11 | 107,0 | không khác ✓ |

- Cả ba mức: 0 câu out_of_scope bị trả lời.
- Áp luật §2.1 thì kết luận đúng: `none` có Completeness tốt lên vượt Holm, nhưng vi phạm guardrail citation, nên **kém
  hơn** chứ không phải "tốt hơn". B ghi đúng điều này là tín hiệu cho 8.2.
- **Tiền:** §5 mới ghi G2 0,1565240 / B17 0,1653212 USD, khớp tổng meta C cộng ở §2.

**m1: đóng.**
