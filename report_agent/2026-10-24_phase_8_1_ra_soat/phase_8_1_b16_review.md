# Review: Phase 8.1 — B16 (G1 §7 số chính mới + `--realism main`) và kế hoạch B17 (G2/G4)

Decision: **ready_for_user_confirmation** (vòng 2, 11:37). Nghĩa: plan sha `a4adfc8eedd9` sẵn sàng để A duyệt. Vòng 1
(11:31) là changes_requested với M1–M3 + m3–m6; tất cả đã đóng (§7).
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a1`)
Date: 2026-10-25 11:26 (bắt đầu) – 11:31 (vòng 1) – 11:37 (vòng 2) (`date`)
Canonical guide: spec `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §5 G2/G4 (gồm sửa đổi 25/10)
Implementation report: `phase_8_1_g1_implementation.md` §7; kế hoạch `phase_8_1_g2_g4_plan.md`
Việc: C23 (`CURRENT_HANDOFF.md` mục "Việc của C", A giao 11:22)

## 1. Phạm vi đã review

**Phần 1 — B16 code + report G1 §7.**

- Git: `main` @ `c3528be`. Working tree: 2 file sửa của B16 (`backend/experiments/phase_8_1/g1_retrieval.py` +10/−4,
  `phase_8_1_g1_implementation.md` +27). Untracked: `phase_8_1_g2_g4_plan.md` (B) và `báo cáo nghiên cứu github.txt`
  (User). `git diff --check` exit 0.
- Đọc exact diff cả hai file, cùng `load_realism` / `keep_realism` / `compare` / `failure_layers` / `main()` của harness.
- File nhãn `data/phase_8_1/golden_realism_final.jsonl`: sha 12 `6916a29a1dee` (khớp `CURRENT_HANDOFF.md`). Có 176 dòng,
  `case_index` 0–175 không trùng. Phân bố: natural 73, capability_only 65, unnatural 29, disputed_unnatural 9. Các câu
  disputed là #1, 28, 100, 112, 113, 125, 133, 137, 148, khớp `realism_disputed_user.md`.

**Phần 2 — kế hoạch B17**, bản sửa sha 12 `43086f053db8`. C tính sha lại và khớp với tin nhắn của B. Bản nháp
`c29b547b7417` sao ở `/tmp/c23/plan_c29b547b.md`. C đọc hết bản sửa và đối chiếu với:
- mục B17 bước 1 trong `CURRENT_HANDOFF.md` (A, 11:22);
- spec §5 G4, gồm sửa đổi 25/10 (`docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md:134-155`);
- `de_xuat_cho_du_an.md` mục 1–5 và 8;
- code thật: `verdict` (`backend/evaluation/full_corpus_eval.py:604`), `is_refusal` (`:167`) cùng test
  `backend/tests/test_full_corpus_eval.py:52-54`, `FullCorpusContextBuilder.build`
  (`backend/retrieval/full_corpus_context.py:88-110`), `CrossEncoderReranker` (`backend/reranking/cross_encoder.py`);
- số 7B ở `reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md` §4.2.

Sửa m1/m2 ở G1 §7: đọc diff, đúng nội dung C yêu cầu.

## 2. Findings

### Phần 1

Không có blocker hay major.

- **m1 (minor) — G1.6 số chính không chạy lại được bằng lệnh đã ghi.** §7 ghi "Lệnh: `g1_retrieval compare/… --realism
  main`", nhưng lệnh `layers` không có `--realism`. Bảng G1.6 (42 câu) vì vậy phải tính bằng cách lọc ngoài CLI. C tự lọc
  kết quả `layers --name runtime_all_minilm` theo nhãn cuối và ra đúng số của B (xem §4). Ảnh hưởng: người sau không biết
  G1.6 được tính thế nào. **Đóng khi:** §7 ghi một dòng cách tính G1.6, ví dụ "lọc `per_case` của `layers` theo nhãn
  ≠ unnatural". Không bắt buộc thêm cờ vào code.
- **m2 (minor) — số "natural" ở §4 không còn chạy lại được.** Code đã chuyển `REALISM_PATH` sang file nhãn cuối, nên
  `--realism natural` giờ cho dev natural 40 câu, trong đó 11 câu có đoạn đúng. §4 (dòng 40, 54, 81, 110, 119) vẫn ghi
  "47 / 14", là số tính bằng file nhãn rater 1 cũ (`golden_realism.jsonl`; C kiểm: 47 / 14). Ảnh hưởng: đọc §4 sẽ tưởng
  số natural lấy từ nhãn cuối. **Đóng khi:** có một câu ở §4 hoặc §7 nói "số natural ở §4 theo nhãn rater 1; theo nhãn
  cuối dev natural = 40 (11 có đoạn đúng)". Không cần tính lại §4.

Ghi nhận khác, không phải finding:
- `keep_realism("main")` dùng `labels.get(i) != "unnatural"`, nên câu thiếu nhãn sẽ lặng lẽ được giữ lại. Hiện file phủ
  đủ 176/176 câu nên không ảnh hưởng. Khi User quyết 9 câu disputed, file nhãn chỉ đổi giá trị, code không cần sửa.
- `--realism natural` loại 9 câu disputed. Như vậy đúng định nghĩa số phụ "chỉ tự nhiên".
- Code thay đổi đúng phạm vi: chỉ đổi đường dẫn file nhãn và thêm lựa chọn `main`, không đụng code production. Mức đơn
  giản phù hợp.

m1, m2: **đã đóng** (B sửa ở §7, một đoạn ngay dưới câu "Lệnh: …"; C đọc diff).

### Phần 2 — plan sha `43086f053db8`

**Những gì đúng (C tự kiểm, xem §4):**
- Tập dev 30 và pilot 10 chọn bằng seed, ghi trước.
- Trần cứu được: G4-A 3 câu, G4-B 17 câu.
- Phép tính 0,9^30 ≈ 4,2%, đi cùng luật `verdict` (cận dưới CI = 0 ⇒ "không khác"). Như vậy chỉ số chính của G4-A về số
  học không thể ra "tốt hơn". Đúng.
- Kiểm GPU 4 bước, dừng thật khi không phải `cuda`, không chạy tiếp trên CPU.
- Luật đầu ra lỗi của luna: không fallback, câu lỗi đếm riêng, biến thể có câu lỗi không được kết luận "tốt hơn".
- Đo latency theo đề xuất mục 4.
- `is_refusal` mô tả đúng code và test.
- Nhiễu citation 7B (4 → 6) trích đúng.
- G2.4 có thêm `none`, baseline gọi là "mặc định (không gửi)".
- G4 chạy trước khi khóa G0.6.
- G2.3 chỉ có một chính sách thay thế, đúng câu chữ A chọn.

Các mục bắt buộc trong B17 bước 1 và đề xuất 1–5, 8 đều có trong plan.

- **M1 (major) — G2.1a, G2.1b, G2.4 chưa có tiêu chí ghi trước.**
  - Vị trí: plan §2. Ba thí nghiệm này chỉ có `changed_variable` và `cost_usd`. G2.2 có chỉ số chính và guardrail nhưng
    cũng chưa có `decision_rule` (thế nào là "tốt hơn"), cũng chưa ghi Holm trong nhóm nào cho G2.1.
  - Yêu cầu: skill `run-experiment` (tiêu chí ghi trước: sàn, mức tụt, chỉ số quyết); `Session_Prompt.md` §6. Đây là các
    lượt có trả tiền.
  - Tác động: chạy xong mới chọn chỉ số. G2.1a (context 10) đã có probe B5 nên dễ chọn chỉ số theo kết quả.
  - **Đóng khi:** plan có một khối chung cho mọi biến thể G2 (hoặc ghi riêng từng cái) gồm: chỉ số chính, luật "tốt hơn"
    (ví dụ CI > 0 sau Holm), nhóm Holm (G2.1: 2 · G2.2: 2 · G2.4: 3), guardrail (dùng lại 3 guardrail của G2.2). G2.4
    ghi thêm guardrail token / USD mỗi câu.
- **M2 (major) — luật quyết của G4 bỏ một tiêu chí spec mà không khai.**
  - Vị trí: plan §1.4, `decision_rule` của G4-A và G4-B chỉ dùng `context5_gold_all`.
  - Spec §5 G4 (`…design.md:141`) ghi tiêu chí "MRR@10 **+** đoạn đúng trong 5 đoạn đưa model tăng có CI". Mục "Thay đổi
    so với bản nháp" không nhắc chuyện này.
  - Yêu cầu: không sửa tiêu chí đã duyệt mà không khai; đổi tiêu chí là việc A/User quyết (`Session_Prompt.md` §4).
  - Tác động: với G4-A, MRR@10 là chỉ số mà việc xếp lại top-10 thật sự làm đổi được (§1.2 đã chỉ ra `context5` không
    thể thắng). Bỏ MRR@10 khỏi luật quyết làm G4-A mất câu hỏi chính của nó.
  - **Đóng khi:** chọn một trong hai. (a) Luật quyết theo đúng spec (cả hai chỉ số, hoặc ghi rõ cách kết hợp). (b) Ghi lệch
    spec vào mục "Thay đổi …" kèm lý do (ví dụ MRR keyword chỉ có 30 câu), để A duyệt hoặc trình User.
- **M3 (major) — G4-B gộp hai thay đổi, nên không biết phần lợi là của reranker.**
  - Vị trí: plan §1.4 G4-B. Baseline là runtime top-10; biến thể đổi cùng lúc pool (native hybrid 100 thay pool 30
    runtime) và reranker.
  - Bằng chứng (C tính từ JSONL G1, dev 30): native p100 **không rerank** đã cho `context5_gold_all` 15/30, runtime chỉ
    12/30, tức +3 câu, và mất 1 câu. `top10_gold_all` 18/30, runtime 15/30.
  - Yêu cầu: skill `run-experiment` (đổi một thứ); `de_xuat` mục 11 (reranker tốn GPU / latency, cần biết nó có đáng
    không).
  - Tác động: G4-B có thể "tốt hơn runtime" chủ yếu nhờ pool rộng. Khi đó 8.2 sẽ chọn nhầm việc thêm reranker GPU.
  - **Đóng khi:** plan thêm mốc thứ hai "native pool 100 không rerank" trên cùng dev 30. Mốc này có sẵn từ G1, hoặc chạy
    lại retrieval miễn phí. Luật ghi trước: chỉ kết luận "reranker có đóng góp" khi G4-B hơn mốc đó (CI hoặc thắng/thua
    ghi trước); nếu không, báo "lợi đến từ pool" là kết quả riêng. Guardrail "0 câu mất" vẫn tính so với runtime.

- **m3 (minor) — 15 câu test đã bị nhìn ở G1.6.** G1 report §5 ghi "khi xác nhận ở gate sau, ghi giới hạn"; plan §1.1 /
  §1.4 chưa mang sang. **Đóng khi:** có một dòng giới hạn ở bước xác nhận test.
- **m4 (minor) — chưa ghi cách xử lý khi baseline không ra đúng số G1.** Plan §0 viết "lượt baseline phải ra đúng số G1",
  nhưng `FullCorpusContextBuilder.build` bỏ qua nguồn không có bằng chứng (`full_corpus_context.py:97-99`), nên
  `packed.sources` có thể khác tiền tố top-5 mà G1 dùng (C21 m1). **Đóng khi:** ghi trước sẽ làm gì nếu lệch (đề xuất:
  ghi số câu lệch; dùng số từ `packed` làm baseline mới; không dừng trừ khi mốc byte retrieval lệch).
- **m5 (minor) — lượt GPU chưa có trần thời gian.** G4.0 chạy 8 cấu hình × 10 câu, có cấu hình pool 100 × "đoạn kèm mục"
  cắt 1024 token. Luật p95 > 30 s/câu chỉ dùng để chọn cho G4-B, không dừng chính lượt pilot. **Đóng khi:** ghi "một lượt =
  một cấu hình × tập câu (≤ 30)" và một trần, ví dụ câu thử đầu > 60 s ⇒ bỏ cấu hình đó, ghi số thật. Đây là ý User về GPU
  yếu.
- **m6 (minor) — nhiễu citation theo câu lớn hơn chênh tổng.** C đọc `run1/run2_answers.jsonl`: lỗi citation Run 1 = 4,
  Run 2 = 6, chỉ **2 câu chung**, tức 6 câu đổi trạng thái trên 176. Ngưỡng "+2 câu tổng" vẫn hợp lý. **Đóng khi:** report G2
  báo cả chênh tổng lẫn số câu lỗi mới (tránh trường hợp biến thể sửa 3 lỗi cũ nhưng sinh 3 lỗi mới). Không bắt buộc đổi
  ngưỡng.

Không có blocker. Không thấy chỗ nào phức tạp quá mức. Nhãn `answer_type` do sub-agent riêng gắn là cần: câu báo thiếu của
P1 cố ý không dùng nguyên câu từ chối, nên đếm bằng máy không bắt được. Kèm thêm đếm máy để đối chiếu là đủ.

## 3. Cách người kiểm chạy lại thật

Các lệnh dưới chỉ phân tích JSONL đã có trong `data/phase_8_1/g1/`. Không chạy retrieval, không gọi API, không dùng GPU.

```bash
cd backend
uv run python -m experiments.phase_8_1.g1_retrieval table --names runtime native_p30 native_p100 native_p200 --realism main
uv run python -m experiments.phase_8_1.g1_retrieval compare --a runtime --b native_p30 native_p100 runtime_k2 runtime_k10 \
  runtime_k30 native_p30_k2 native_p30_k10 native_p30_k30 dbsf_w02 dbsf_w03 --metrics top10_gold_all mrr ndcg --realism main
uv run python -m experiments.phase_8_1.g1_retrieval compare --a runtime --b q_nfd q_nfd_nfc q_noaccent q_noaccent_nfc \
  q_tone_swap q_tone_swap_nfc --metrics top10_gold_all mrr --realism main
uv run python -m experiments.phase_8_1.g1_retrieval layers --name runtime_all_minilm   # rồi C lọc per_case theo nhãn cuối
```

Đầu ra: `/tmp/c23_g13.json`, `/tmp/c23_g14.json`, `/tmp/c23_g16.json`. Điều kiện dừng sớm và số natural cũ/mới tính bằng
script nhỏ `python -I` đọc cùng các JSONL đó.

## 4. Kết quả quan sát

So với §7 của B, mọi số **khớp**:

- **Bảng G1.1:** 88 câu, 32 câu có đoạn đúng. Cả 4 cấu hình × 6 cột trùng đến 3 chữ số thập phân. Ví dụ runtime: hợp hai
  nhánh 0,750, top-10 0,531, 5 đoạn 0,406, MRR 0,716; native p100: hợp hai nhánh 0,969, top-10 0,625, 5 đoạn 0,500.
- **Điều kiện dừng sớm:** 15 câu lỗi top-10. 14 câu đủ đoạn đúng trong hợp hai nhánh @200, trong đó 7 câu đủ ngay trong
  pool 30 runtime. Khớp.
- **G1.3 (Holm trên 10):** `verdict_holm` = `no_difference` ở mọi biến thể với `top10_gold_all` và MRR. Trước Holm, MRR
  "tốt hơn" ở 4 biến thể: native p100 +0,008, runtime k=2 +0,009, runtime k=10 +0,005, native p30 k=2 +0,012. Hai biến
  thể có `top10_gold_all` cao nhất là native p100 và native p30 k=2: +0,094, 3/29/0. nDCG không biến thể nào có CI < 0.
  Khớp.
  - Bổ sung (không phải lỗi): trên tập số chính, native p30, p30 k=10 và p30 k=30 vẫn **mất 1 câu** đoạn đúng khỏi
    top-10 (3/28/1). Runtime k=10 không còn mất câu nào (bảng §4 trên toàn dev ghi mất 1). §7 không có cột guardrail;
    các biến thể này không qua luật nên kết luận không đổi.
- **G1.4 (Holm trên 6):** NFD MRR −0,200 [−0,269; −0,132] kém hơn; NFD+NFC = gốc; bỏ dấu MRR −0,555 [−0,634; −0,475],
  `top10_gold_all` −0,500 (0,531 → 0,031) kém hơn; NFC không cứu; đổi kiểu dấu MRR +0,001, không khác. Khớp.
- **G1.6 (42 câu):** thiếu ở pool 11, rơi khỏi top-10 8, rơi khỏi 5 đoạn 6, đủ tới bước trả lời 17. Từ chối nhầm 16 câu,
  chia pool 7 / top-10 4 / 5 đoạn 5, không câu nào đủ fact trong context. Khớp.

Kết luận "không đổi kết luận mục 4" của B đúng với số đã kiểm.

**Plan (script `python -I` đọc JSONL G1 + nhãn cuối + split; không chạy retrieval):**
- Dev số chính có đoạn đúng: 32 câu. `sorted(Random(20261024).sample(dev32, 30))` cho baseline runtime: context 5 = 12/30,
  top-10 = 15/30, hợp hai nhánh native p100 = 29/30. Trần G4-A = 3, trần G4-B = 17. **Khớp plan §1.1–1.2.**
- Native p100 không rerank trên dev 30: top-10 18/30, context 5 15/30, mất 1 câu so với runtime (dùng cho M3).
- Câu test có đoạn đúng: 15, trong đó 10 thuộc số chính. Khớp §1.1.
- 0,9^30 = 0,0424 (khớp "~4%"). `verdict`: `low <= 0` ⇒ `no_difference` (khớp lập luận §1.2).
- `is_refusal` = trùng hệt sau `strip()`; test `:52-54` khẳng định câu từ chối có thêm chữ thì không tính. Khớp.
- 7B: lỗi citation 4/176 (Run 1), 6/176 (Run 2), 22 = 22 từ chối nhầm (report 7B §4.2 dòng 79, 81). Khớp. Theo câu: 2 câu
  chung, 6 câu đổi (m6).

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại retrieval. Phần 1 chỉ đổi cách lọc lúc phân tích, không đổi đường chạy hay JSONL, nên dùng lại JSONL G1
  mà C21 đã kiểm trùng từng câu là hợp lệ.
- Plan chưa chạy gì, nên C chỉ kiểm được lập luận và số tính lại từ G1. Các điểm sau chỉ kiểm được khi chạy ở bước 2:
  latency thật, `model_max_length` của M1/M2, CrossEncoder có thật sự nằm trên `cuda` không, và luna có nhận
  `reasoning: none` không.

## 6. Decision và bước tiếp theo

**changes_requested (vòng 1).** Phần 1 đạt (m1, m2 đã đóng). Phần 2: B sửa M1–M3 trong plan. Nên sửa luôn m3–m5 cùng lượt
vì chỉ là thêm vài dòng; m6 làm khi viết report G2. Sau đó B ghi sha mới và nhắn C. C chỉ kiểm lại các đoạn đổi (diff với
bản `43086f053db8`, C giữ một bản ở `/tmp/c23/plan_43086f05.md`). Không cần chạy gì.

Chỗ lệch tài liệu (báo A): skill `risk-gated-agent-review` mục Correction nói người kiểm ghi phần cần sửa vào mục việc của
người làm trong `CURRENT_HANDOFF.md`. Nhưng `WORKFLOW.md` §3.2 chỉ cho B/C sửa mục của chính mình. C làm theo WORKFLOW: không
sửa mục B17; correction nằm ở file này và trong tin nhắn gửi A + B.

## 7. Vòng 2 — plan sha `a4adfc8eedd9` (B sửa 11:36; C kiểm 11:37)

Cách kiểm: C tính lại sha (khớp tin của B). Plan là file untracked, nên C so bằng `diff /tmp/c23/plan_43086f05.md` với
bản mới. Diff chỉ chạm các đoạn B liệt kê ở mục "Vòng sửa 1 theo review C23"; không có đoạn nào khác đổi. Bản mới sao ở
`/tmp/c23/plan_a4adfc8e.md`.

| Finding | Sửa | C kiểm | Trạng thái |
|---|---|---|---|
| M1 | §2.1 mới: khối tiêu chí chung cho 7 biến thể G2 (chỉ số chính Completeness 88 câu; Holm G2.1: 2 / G2.2: 2 / G2.4: 3; 4 guardrail, gồm USD/câu ≤ 2 × G2.0; luật tốt hơn / kém hơn / chưa rõ; xác nhận test 56 = cùng dấu + guardrail). G2.1a/b, G2.2, G2.4 trỏ về §2.1 | đủ thành phần tiêu chí đóng | đóng |
| M2 | Theo spec (A quyết): G4-A và G4-B đều cần `context5_gold_all` **và** MRR@10 có CI > 0 sau Holm. §1.2 ghi rõ hệ quả: G4-A không thể "tốt hơn"; MRR@10 đứng riêng chỉ là tín hiệu | khớp spec `…design.md:141` | đóng |
| M3 | `reference_no_rerank` = native p100 không rerank, chạy lại miễn phí bằng harness G4 (context lấy từ `packed`). Chỉ kết luận "reranker có đóng góp" khi G4-B hơn mốc này theo cùng luật; nếu không thì báo "lợi đến từ pool". Bảng mốc §1.1 | C tính lại: runtime 12/15/22, native p100 15/18/29, mất 1 câu; trần G4-B so với native 29 − 15 = 14. Khớp | đóng |
| m3 | Giới hạn "test 15 đã nhìn ở G1.6" ở §1.1 và trong luật xác nhận G4-B | có | đóng |
| m4 | §0: nếu lệch thì ghi từng câu lệch, dùng `packed` làm baseline mới, chỉ dừng khi mốc byte lệch | có | đóng |
| m5 | Một lượt GPU = một cấu hình ≤ 30 câu; câu đo đầu > 60 s ⇒ bỏ cấu hình đó; cả lượt > 20 phút ⇒ dừng, báo A; G4.0 = 8 lượt | có | đóng |
| m6 | Guardrail citation §2.1 báo cả số câu lỗi mới và số câu hết lỗi | có | đóng |

Thay đổi thêm (ngoài finding): §0 ghi User giữ cả 9 câu bất đồng. Khớp `CURRENT_HANDOFF.md` 11:33 ("giữ cả 9 (tính
natural)"), nên tập số chính không đổi, còn số phụ "chỉ natural" có thêm 9 câu. Bước "mốc" thêm vào §4, đúng thứ tự.

Không có finding mới. **Kết luận: plan `a4adfc8eedd9` sẵn sàng để A duyệt** (A ghi "duyệt bản sha a4adfc8eedd9" ở mục
B17, rồi commit B16). Bước 2 vẫn theo plan: mỗi gate G4/G2 có report riêng và C review.
