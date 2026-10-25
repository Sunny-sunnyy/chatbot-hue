# Báo cáo cho bạn: Đánh giá — thước đo chất lượng và điểm mốc (Phase 7B, Phase 8.1)

**Cập nhật lần cuối: 14:04 25/10/2026 — bản 2: xếp lại theo mẫu mới + thêm thước đo Phase 8.1 (so theo cặp, nhóm thử /
nhóm kiểm, đoạn đúng, độ tự nhiên, nhiễu của người chấm, câu kín). Số liệu 7B giữ nguyên, nay nằm ở §4.**
Người viết: A (bản 1, 24/10), C (bản 2) · Review: B. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** chấm chatbot một cách tự động và lặp lại được, để mọi thay đổi đều so với một **điểm mốc** trên
  cùng bộ câu hỏi, rồi mới quyết giữ hay bỏ.
- **Đang chạy cách nào:** chatbot vẫn chạy đúng cấu hình đo mốc 7B (Phase 8.1 không đổi chatbot).
  - Bộ chấm chạy đúng đường API thật: tìm đoạn → 5 đoạn → `gpt-6-luna` trả lời.
  - Chấm tìm đoạn bằng keyword (miễn phí).
  - Chấm câu trả lời: Claude chấm 3 điểm 1–5 (Đúng / Đủ / Trúng ý); không tốn API.
- **Mốc 7B** (176 câu): Đúng / Đủ / Trúng ý **4,43 / 4,28 / 4,45**; từ chối nhầm 22/158 câu; lỗi trích dẫn 4/176. Chạy lại
  lần 2 chênh trung bình ≤ 0,011.
- **8.1 làm thước đo chặt hơn** (25/10):
  - **So theo cặp từng câu** (bootstrap, CI 95%, thắng/hòa/thua, Holm khi nhiều biến thể). Tự kiểm đạt: hai lượt giống
    nhau ⇒ "không khác"; cố tình làm hỏng ⇒ "kém hơn".
  - Chia 176 câu: **120 câu thử** (để chọn) / **56 câu kiểm** (chỉ để xác nhận).
  - **Đoạn đúng** (vị trí trong file nguồn) cho 55 câu khó, đo chính xác hơn keyword.
  - **Số chính bỏ 29 câu không tự nhiên.**
  - Đo được **nhiễu riêng của người chấm**: cùng câu trả lời, chấm lại thì điểm "Đủ" đổi ở 2/88 câu.
- **8.1 đã dùng thước này** cho tìm kiếm, xếp hạng lại, chia đoạn, từ khóa và sinh câu trả lời. Kết luận đáng kể nhất:
  **đưa 10 đoạn thay vì 5** cho model trả lời đầy đủ hơn (+0,26 điểm "Đủ" trên bộ thử, +0,27 trên bộ kiểm). Chưa đưa vào
  chatbot: cần bạn duyệt ở 8.2.
- **Giới hạn chính:**
  - chưa có người chấm tay;
  - chỉ 32 câu thử có nhãn đoạn đúng (sau khi bỏ câu không tự nhiên), nên nhiều kết quả chỉ là "chưa rõ";
  - bộ câu kín chưa khóa;
  - người chấm không trừ điểm khi câu trả lời lỗi trích dẫn.
- **Chi phí:** 7B + thử nhanh ~0,087 USD (~2.200 đồng). Thước đo 8.1 (chia nhóm, so theo cặp, đoạn đúng, nhãn) 0 USD; chấm
  dùng quota Claude Code.
- **Bạn cần quyết gì:**
  1. Xem mẫu câu kín bản 5 lần cuối rồi khóa (§6).
  2. Trước khi 8.2 quyết dựa trên điểm câu trả lời: chấm tay khoảng 20 câu để có mốc người.

## 2. Hoạt động thế nào (bản đang chạy)

```text
Mốc (7B):  176 câu Golden → API thật (tìm đoạn → 5 đoạn → gpt-6-luna trả lời)
           → chấm tìm đoạn (keyword trong top-10)          — miễn phí
           → Claude chấm câu trả lời so đáp án mẫu, 1–5    — quota Claude, không tốn API
           → đếm từ chối đúng / nhầm, lỗi trích dẫn         — miễn phí

So một thay đổi (8.1):  chạy mốc + biến thể trên CÙNG câu nhóm thử
           → chênh từng câu → bootstrap 10.000 lần → CI 95% (chứa 0 ⇒ "không khác")
           → nhiều biến thể ⇒ hiệu chỉnh Holm → "tốt hơn" thì xác nhận trên nhóm kiểm
           → đoạn đúng đo theo tầng: có trong pool ứng viên → top-10 → 5 đoạn đưa model
           → câu trả lời của mọi biến thể gộp MÙ cho người chấm (không biết của biến thể nào)
```

- **Luật quyết ghi trước khi chạy**, có ba lớp:
  - sàn không được vi phạm, ví dụ 0 câu mất đoạn đúng, 0 câu ngoài kho bị trả lời;
  - mức tụt cho phép của chỉ số khác;
  - 1–2 chỉ số quyết phải tốt lên vượt nhiễu.
- Code:
  - `backend/evaluation/full_corpus_eval.py`: `compare`, `split`, `summarize`, chấm;
  - prompt chấm `backend/evaluation/full_corpus_judge_prompt.md`;
  - harness thí nghiệm 8.1 ở `backend/experiments/phase_8_1/`.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Chấm tìm đoạn bằng keyword (MRR, nDCG, Keyword Coverage @10) | **Đã xử lý, đóng gói** | mốc 7B; `full_corpus_eval.py` |
| Chấm câu trả lời bằng Claude (Đúng / Đủ / Trúng ý) | **Đã xử lý, đóng gói** | chạy lại lần 2 chênh ≤ 0,011 |
| Từ chối đúng / từ chối nhầm, lỗi trích dẫn | **Đã xử lý, đóng gói** | bảng 2×2 từ 8.1 |
| So theo cặp + CI + Holm, tự kiểm đối chứng âm / dương | **Đã xử lý, đóng gói** | đạt cả hai đối chứng (§4, 25/10) |
| Nhóm thử 120 / nhóm kiểm 56 | **Đã xử lý, đóng gói** | chia theo loại câu, seed cố định, khóa theo câu hỏi |
| Đoạn đúng (vị trí trong file) cho câu khó | **Xử lý một phần** | 55/176 câu (40 thử / 15 kiểm); câu còn lại chỉ có keyword |
| Nhãn độ tự nhiên (bỏ câu người thật ít hỏi) | **Đã xử lý** | 82 tự nhiên / 65 chỉ đo năng lực / 29 không tự nhiên; số chính bỏ 29 câu |
| Đo nhiễu riêng của người chấm | **Đã xử lý** | chấm lại cùng câu trả lời: "Đủ" đổi 2/88, chênh TB 0 |
| Bộ câu kín cho chấm cuối 8.2 | **Xử lý một phần** | 36 câu soạn xong, đủ dấu, 36/36 tự nhiên; chưa khóa |
| Người chấm tay (mốc người) | **Chưa thực hiện** | bạn bỏ ở 7B; nhắc lại trước quyết định 8.2 |
| Kiểm bám nguồn bằng code (số trong câu có trích dẫn phải có trong nguồn) | **Chưa thực hiện** | đề xuất 8.2; người chấm hiện không chấm trích dẫn |
| Điểm trên câu người dùng thật sự nhận (câu lỗi trích dẫn người dùng thấy lỗi, nhưng vẫn có thể được 5 điểm) | **Chưa thực hiện** | đề xuất 8.2 |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 25/10/2026 — Phase 8.1: làm thước đo chặt hơn (G0)

Tiêu chí ghi trước (spec 8.1): so theo cặp phải ra "không khác" khi so hai lượt như nhau, và "kém hơn" khi cố tình làm hỏng.

| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Chia 120 thử / 56 kiểm theo loại câu | một dữ kiện 24, nhiều nguồn 9, điều kiện 9, so sánh 8, ngoài kho 6 ở nhóm kiểm | chọn phương án trên nhóm thử, chỉ xác nhận trên nhóm kiểm ⇒ tránh "tự chấm bài mình chọn" |
| Đối chứng âm (hai lượt 7B như nhau) | mọi chỉ số "không khác", ở cả tổng, từng loại câu và cả hai nhóm · **PASS** | thước không báo khác giả |
| Đối chứng dương (cố tình xáo top-10) | MRR, nDCG "kém hơn" rõ ở cả ba nhóm · **PASS** | thước bắt được thay đổi thật |
| Đoạn đúng cho 55 câu khó | agent gắn, agent khác kiểm (55/55 đúng nguồn), bạn xem mẫu · **PASS** | đo "đoạn có đáp án có lọt vào phần đưa model không", không chỉ đếm keyword |
| Nhãn độ tự nhiên 176 câu | 2 agent gắn độc lập, đồng ý cao (kappa 0,765); 9 câu bất đồng bạn giữ ⇒ 82 / 65 / 29 | số chính chỉ tính câu người dùng thật có thể hỏi |
| Nhiễu riêng của người chấm (G2) | cùng câu trả lời chấm 2 lần: "Đủ" đổi 2/88 câu, chênh TB 0,000; "Đúng" 1/88; "Trúng ý" 3/88 | nhiễu nhỏ; vẫn chấm mốc và biến thể trong **cùng một lượt mù** |
| Nhiễu "sinh lại + chấm lại" (G2.0 so 7B Run 1) | 10/83 câu đổi điểm "Đủ", chênh TB +0,048 | đây là lý do mỗi biến thể có mốc chạy lại cùng lúc |
| Câu kín | 36 câu: soạn mới, đủ dấu (25/10), 36/36 tự nhiên, sửa đáp án theo nguyên tắc bạn duyệt 12:20; chưa khóa | dùng cho chấm cuối 8.2; C không đọc nội dung, A chỉ thấy 3 câu do bạn trích khi hỏi (không đề xuất biến thể nhắm vào chúng) |

Tiền: 0 USD; chấm dùng quota Claude.

**Phát hiện làm đổi chẩn đoán cũ:** chẩn đoán 7B (dựa trên keyword) ghi "4/22 câu có đủ bằng chứng mà vẫn từ chối". Đo bằng
đoạn đúng ở 8.1 cho thấy **22/22 câu từ chối nhầm đều thiếu dữ kiện trong 5 đoạn đưa model**. Nguyên nhân chính là khâu tìm
và xếp đoạn, không phải model "từ chối vô cớ".

### 24/10/2026 — Phase 7B: bộ chấm và điểm mốc 176 câu (bản 1, A)

Bộ chấm tự động + điểm mốc của hệ thống hiện tại trên 176 câu Golden; mỗi cải tiến Phase 8 so với mốc này. Người chấm chính
là Claude (bạn chọn, để tiết kiệm), `gpt-6-luna` chấm phụ để so. Câu trả lời vẫn do `gpt-6-luna` sinh.

| Nội dung | Kết quả | Ý nghĩa |
|---|---|---|
| Điểm mốc (Đúng / Đủ / Trúng ý) | **4,43 / 4,28 / 4,45** | Khá tốt tổng thể |
| Câu một dữ kiện (75 câu) | 4,87 / 4,84 / 4,89 | Gần hoàn hảo |
| Câu có điều kiện (29) | 4,72 / 4,41 / 4,76 | Tốt |
| Câu so sánh (25) | 3,68 / 3,44 / 3,60 | Yếu |
| Câu ghép nhiều nguồn (29) | **3,28 / 3,00 / 3,41** | Yếu nhất |
| Câu ngoài kho (18) | 5 / 5 / 5 — từ chối đúng 18/18 | Không bịa |
| Tìm đoạn (158 câu, keyword proxy @10) | MRR 0,72 · nDCG 0,755 · Keyword Coverage 92,4% | Đoạn chứa keyword đáp án thường lọt top-10; yếu ở câu so sánh (MRR 0,53) và nhiều nguồn (0,54) |
| **Từ chối nhầm** | **22 / 158 câu** | Đây là toàn bộ 22 câu bị 1/1/1; bỏ chúng ra điểm còn 4,92 / 4,75 / 4,95 |
| Lỗi trích dẫn (người dùng thấy lỗi) | 4 / 176 | Hiếm |
| Chạy lại toàn bộ lần 2 | chênh trung bình ≤ 0,011 điểm | Thước đo rất ổn định |
| Claude chấm lại 30 câu | không câu nào lệch quá 1 điểm | Người chấm ổn định |
| Claude so với gpt-6-luna | trùng 89–96% số câu | Hai người chấm khác hãng đồng ý cao |

Vì sao từ chối nhầm (chẩn đoán 22 câu, không tốn tiền; dấu hiệu, chưa chứng minh nguyên nhân). **Đã được 8.1 thay**, xem
mục 25/10 và §5:

| Phân loại (theo keyword đáp án trong 5 đoạn ngữ cảnh) | Số câu |
|---|---:|
| Đoạn chứa đáp án không nằm trong 5 đoạn ngữ cảnh | 8 |
| Có một vế, thiếu vế kia → bot từ chối cả câu | 10 |
| Có đủ bằng chứng mà vẫn từ chối | 4 |

12/22 câu có thêm keyword liên quan ở hạng 6–10, bị cắt vì chỉ giữ 5 đoạn. Thử nhanh với 10 đoạn (0,005 USD): 10/22 câu hết
từ chối (chưa chấm điểm, chỉ là dấu hiệu). 8.1 đã đo đầy đủ: 10 đoạn **tốt hơn**, đã xác nhận trên bộ kiểm.

Giới hạn ghi ở bản 1, nay vẫn đúng:
- chưa có người chấm tay (bạn quyết bỏ);
- 121/176 câu đã đạt tối đa, nên cải tiến chủ yếu lộ ở 55 câu còn lại;
- Golden do LLM viết, người duyệt;
- chỉ số truy xuất dựa trên keyword nên chỉ là "proxy".

Tiền: toàn bộ 7B + thử nhanh **~0,087 USD (~2.200 đồng)**. Claude chấm dùng quota Claude Code (~1,1M token).

## 5. Hôm nay còn đúng không

Kiểm ngày 25/10/2026 với code `main` và các report 8.1.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Bộ chấm `full_corpus_eval.py` (`generate`, `summarize`, `compare`) | **còn dùng**; `compare` nay so theo cặp (8.1) | `backend/evaluation/full_corpus_eval.py` |
| Prompt chấm cố định `full_corpus_judge_prompt.md` | **còn dùng** (không chấm trích dẫn, không trừ chi tiết thêm) | `backend/evaluation/full_corpus_judge_prompt.md:13-16` |
| Người chấm chính Claude, luna phụ | **còn dùng**; 8.1 chỉ dùng Claude, chấm mù gộp biến thể | report G2 8.1 |
| Điểm mốc đo trên runtime (`e5-small-384`, `dense_bm25_rrf`, `reranker: none`, 5 đoạn) | **còn đúng**: chatbot chưa đổi; retrieval vẫn giống từng byte mốc `cefb2d1a…` (kiểm 25/10) | `backend/config/settings.yaml`; report G3 8.1 |
| Điểm 7B Run 1 làm mốc cho mọi câu | **còn dùng, trừ 10 câu** Golden đã sửa đáp án 25/10: không so trực tiếp | `phase_8_1_golden_fix_review.md` |
| Chẩn đoán từ chối nhầm theo keyword (8 / 10 / 4) | **đã thay** bởi chẩn đoán theo đoạn đúng: 22/22 thiếu dữ kiện trong context | report G1 8.1 §4 |
| Macro-average "theo case" (docstring cũ) | **đã sửa** (8.1): `overall` = trung bình theo câu; `macro` = trung bình các loại câu | `full_corpus_eval.py` `mean_by_category` |
| So hai lượt bằng "mức khớp" | **đã thay** bởi so theo cặp + CI; mức khớp vẫn in kèm | `full_corpus_eval.py` `compare_variants` |

## 6. Việc còn lại / cần quyết

- **Bạn quyết:** xem mẫu câu kín bản 5 (17 dòng, 8 dòng đánh dấu đổi) lần cuối. Sau đó A tạo file chính thức và khóa mốc
  8.1 (G0.6: ghi hash kho, chỉ mục, nhóm chia, đoạn đúng, nhãn, câu kín).
- **Bạn quyết (trước 8.2):** chấm tay khoảng 20 câu để có mốc người cho người chấm Claude.
- **Đề xuất 8.2:**
  - kiểm bám nguồn bằng code (số trong câu có `[n]` phải có trong đoạn `[n]`);
  - báo riêng "điểm trên câu người dùng thật sự nhận" (câu lỗi trích dẫn tính là hỏng);
  - gắn thêm đoạn đúng cho câu thử để tăng cỡ mẫu (32 câu hiện nay làm nhiều kết quả chỉ "chưa rõ").

## Phụ lục — hồ sơ kỹ thuật

- **7B:**
  - spec `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md`;
  - report `reports/phase_7b_*` (baseline `reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md`; chẩn đoán từ chối
    nhầm `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`);
  - guide `guides/full_corpus_rag.md` mục "Cập nhật Phase 7B".
- **8.1 G0** (đợt `report_agent/2026-10-24_phase_8_1_ra_soat/`):
  - G0.1–G0.2: `phase_8_1_g0_1_2_measure_implementation.md` (C16) + review;
  - G0.3 đoạn đúng: `phase_8_1_g0_3_gold_review.md` (B14);
  - G0.4 câu kín: `phase_8_1_g0_4_sealed_review.md` §1–§10;
  - G0.5 tham số mặc định-như-cũ: `phase_8_1_g0_5_review.md`;
  - nhiễu người chấm: `phase_8_1_g2_implementation.md` §4.5;
  - kết quả 8.1 tách theo loại câu: `phase_8_1_g5_by_category.md`;
  - G1 chẩn đoán theo tầng: `phase_8_1_g1_implementation.md`.
- **File private:**
  - `split.json` sha `e2b1788dfbbc`;
  - đoạn đúng `data/phase_8_1/gold/gold_draft.jsonl` sha `bab707b9…`;
  - nhãn độ tự nhiên `golden_realism_final.jsonl` sha `0b65d1c138d2`;
  - câu kín v6 md5 `631334704fdd`;
  - Golden chính thức md5 `0f7dbf41b422`.
- Bản 1: A, 24/10/2026. Bản 2: C30, 25/10/2026.
