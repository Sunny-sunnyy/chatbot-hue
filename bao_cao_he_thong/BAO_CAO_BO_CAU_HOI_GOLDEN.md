# Báo cáo cho bạn: Bộ câu hỏi chuẩn Golden và chấm điểm thử món ăn (Phase 7, 7A, 8.1)

**Cập nhật lần cuối: 14:04 25/10/2026 — bản 5: thêm Phase 8.1 (chia nhóm thử / kiểm, đoạn đúng, nhãn độ tự nhiên, sửa
10 đáp án, bộ câu kín); sửa các dòng ở §1 và §3 đã cũ.**
Người viết: C · Review: A (bản 1–4), B (bản 5). Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** tạo "đề thi" để chấm chatbot. **Bộ Golden toàn kho** có 176 câu phủ cả 5 mảng,
  cộng bộ thử nhanh 10 câu. Mỗi câu có: câu hỏi viết như người thật hỏi, đáp án tham chiếu ngắn,
  keyword lấy nguyên văn từ kho (để chấm bước tìm đoạn) và loại câu. Phase 7B và Phase 8 dùng đề này.
- **Đang chạy cách nào:** file `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` (private);
  lệnh `golden_full_corpus check` kiểm định dạng và keyword có nguyên văn trong kho. Trạng thái: Phase 7
  (món ăn) đóng 24/08/2026; Phase 7A (Golden toàn kho) đóng 23/10/2026.
- **Đo được:** 176 câu = một dữ kiện 75, nhiều nguồn 29, điều kiện 29, so sánh 25, ngoài kho 18; 100%
  câu đối chiếu với file nguồn. Kiểm lại 24/10: Golden 176 và smoke 10 đều đạt. Dùng thật ở 7B: chấm
  hai lần chênh ≤0,011 điểm.
- **8.1 (24–25/10) đã thêm:**
  - chia 120 câu thử / 56 câu kiểm;
  - **đoạn đúng** (vị trí trong file nguồn) cho 55 câu khó;
  - **nhãn độ tự nhiên** cho 176 câu: 82 tự nhiên / 65 chỉ đo năng lực / 29 không tự nhiên. Số chính bỏ 29 câu không tự
    nhiên.
  - **sửa đáp án tham chiếu 10 câu**, theo nguyên tắc bạn duyệt 25/10: đáp án chỉ trả lời điều được hỏi;
  - **bộ 36 câu kín** viết kiểu người dùng thật, cho chấm cuối 8.2: soạn xong, chưa khóa.
- **Giới hạn chính:** câu do AI viết rồi người duyệt, không phải câu người dùng thật hỏi; keyword chỉ là
  "proxy"; giá vé, giờ mở cửa lấy mốc 09/2026; 121/176 câu đã đạt điểm tối đa ở mốc 7B. Đoạn đúng mới có cho 55/176 câu.
- **Chi phí:** kiểm định dạng không tốn phí; mọi việc 8.1 với đề là 0 USD (quota Claude).
- **Bạn cần quyết gì:** xem mẫu câu kín bản 5 lần cuối, để A khóa bộ kín (xem §6).

## 2. Hoạt động thế nào (bản đang chạy)

```text
Phase 7A (làm đề):
đọc file .md → viết thử 20 câu → bạn chỉnh văn phong → 6 sub-agent viết 6 nhóm còn lại
 → máy kiểm định dạng + keyword có nguyên văn trong kho → người kiểm đối chiếu từng câu với kho
 → bạn đọc mẫu → sửa → gộp thành 1 file (nối các nhóm theo thứ tự cố định, không xáo) + chọn tay 10 câu smoke

Phase 7B (chấm, dùng đề này):
176 câu → chatbot thật trả lời → chấm tìm đoạn (keyword) + Claude chấm câu trả lời
```

Năm loại câu: một dữ kiện (`direct_fact`), nhiều nguồn (`multi_source`), có điều kiện
(`conditional`), so sánh (`comparative`), ngoài kho (`out_of_scope`, đáp án đúng là từ chối).

Code: `backend/evaluation/golden_full_corpus.py` (lệnh `check`, `merge`). Tự kiểm định dạng (không bắt
buộc, không tốn phí), từ `backend/`:

```bash
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
```

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Câu một dữ kiện | **Đã xử lý, đóng gói** | 75 câu |
| Câu nhiều nguồn | **Đã xử lý, đóng gói** | 29 câu |
| Câu có điều kiện | **Đã xử lý, đóng gói** | 29 câu |
| Câu so sánh | **Đã xử lý, đóng gói** | 25 câu |
| Câu ngoài kho (đáp án đúng là từ chối) | **Đã xử lý, đóng gói** | 18 câu |
| Kiểm định dạng + keyword nguyên văn trong kho | **Đã xử lý, đóng gói** | `check` đạt 24/10 sau khi kho được sửa ở 7A2; `golden_full_corpus.py:26–28` |
| Đối chiếu dữ kiện từng câu với kho | **Đã xử lý, đóng gói** | 100% câu; 4 câu xóa, 10 câu sửa |
| Bộ thử nhanh 10 câu | **Đã xử lý, đóng gói** | 10/10 câu trùng khớp file chuẩn |
| Giá vé, giờ mở cửa còn đúng | **Xử lý một phần** | Lấy mốc 09/2026, có thể cũ |
| Tách nhóm thử / nhóm kiểm | **Đã xử lý, đóng gói** | 8.1: 120 / 56 theo loại câu, seed cố định, khóa theo câu hỏi |
| Bằng chứng chuẩn (đoạn đúng) cho câu khó | **Xử lý một phần** | 8.1: 55 câu (40 thử / 15 kiểm), agent gắn, agent khác kiểm, bạn xem mẫu |
| Nhãn độ tự nhiên | **Đã xử lý** | 8.1: 82 / 65 / 29; số chính bỏ 29 câu không tự nhiên |
| Đáp án tham chiếu chỉ trả lời điều được hỏi | **Đã xử lý** | 8.1: sửa 10 câu (25/10); 5 câu "chưa chắc" giữ nguyên |
| Bộ câu kín cho chấm cuối | **Xử lý một phần** | 8.1: 36 câu soạn xong, đủ dấu, 36/36 tự nhiên; chưa khóa |
| Câu người dùng thật hỏi | **Chưa thực hiện** | Đề do AI viết, người duyệt; câu kín viết theo kiểu người dùng thật nhưng vẫn do AI soạn |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 25/10/2026 — Phase 8.1: sửa đáp án và hoàn thiện bộ câu kín

- **Nguyên tắc bạn duyệt (12:20):** đáp án chỉ trả lời điều câu hỏi hỏi; chỉ thêm điều kiện khi thiếu nó thì sai hoặc gây
  hiểu lầm; chi tiết phụ đúng nguồn thì giữ.
- **Golden — sửa đáp án 10 câu** (A làm, C kiểm):
  - chỉ đổi đáp án; câu hỏi, keyword và loại câu giữ nguyên;
  - mọi dữ kiện mới đều có ở dòng nguồn;
  - máy kiểm đạt trên cả 9 file đề;
  - C phát hiện 1 câu còn thêm lời dặn ngoài câu hỏi và 1 câu thiếu nguồn, A đã sửa cả hai;
  - 5 câu "chưa chắc" giữ nguyên.
  - **PASS** · tiền 0.
  - Hệ quả: điểm 7B của 10 câu này không còn so trực tiếp được.
- **Câu kín** (36 câu; C không đọc nội dung, A chỉ thấy 3 câu do bạn trích khi hỏi; mọi việc qua sub-agent mới, mỗi lượt một người sửa và một người kiểm):
  - bạn yêu cầu đủ dấu ⇒ 16 câu được thêm dấu, chỉ đổi dấu;
  - bạn chỉ ra 1 đáp án lặp chủ ngữ ⇒ sửa câu đó, rà cả 36 đáp án, sửa thêm 3 đáp án bị lặp;
  - bạn duyệt sửa 3 câu "chỉ đo năng lực" thành câu người dùng thật hay hỏi, và bỏ một quy định thừa ở 1 đáp án;
  - mỗi lượt: máy kiểm đạt, người kiểm độc lập báo đạt.
  - Hiện **36/36 câu tự nhiên**; phân bố một dữ kiện 15, nhiều nguồn 6, điều kiện 7, so sánh 5, ngoài kho 3.
  - Mẫu bản 5 (17 dòng, 8 dòng đánh dấu đổi) **chờ bạn xem lần cuối**.
  - **PARTIAL** (chưa khóa) · tiền 0.

### 24/10/2026 — Phase 8.1: chia nhóm, đoạn đúng, nhãn độ tự nhiên

- **Chia 176 câu:** 120 câu thử / 56 câu kiểm, theo loại câu, seed cố định. Đối chứng âm / dương của phép so theo cặp đều
  **PASS** (chi tiết `BAO_CAO_DANH_GIA.md`).
- **Đoạn đúng cho 55 câu khó:** agent gắn, agent khác kiểm (55/55 đúng nguồn, 0 thiếu nguồn), bạn xem mẫu · **PASS**.
- **Nhãn độ tự nhiên:**
  - 2 agent gắn độc lập, đồng ý cao (kappa 0,765);
  - 9 câu bất đồng bạn giữ là tự nhiên ⇒ **82 / 65 / 29**;
  - số chính của mọi thí nghiệm 8.1 bỏ 29 câu không tự nhiên; "chỉ tự nhiên" là số phụ.
  - **PASS** · tiền 0.

### 24/10/2026 — Dọn code món ăn sau Phase 7 (bản 4)
Gỡ bộ chấm món ăn (`eval.py`, `evaluator.py`, `test.py`, `golden_dataset.py`) và notebook 07. Kiểm lại
sau dọn: Golden 176 câu và smoke 10 câu vẫn đạt `check` · **PASS** · tiền: 0. File Golden món ăn cũ
(private) giữ nguyên.

### 24/10/2026 — Đính chính cách gộp đề (bản 3)
Đối chiếu lại code và spec 7A khi rà quyết định Phase 8.1: đề được nối theo thứ tự nhóm cố định, không
xáo. Bản 2 ghi "xáo cố định" là nhầm. Không đổi số đo nào.

### 24/10/2026 — Kiểm lại đề (C chạy `golden_full_corpus check`)
Kết quả: **PASS** — Golden 176 câu đạt; smoke 10 câu đạt, 10/10 câu trùng khớp file chuẩn · đề vẫn
đúng định dạng sau khi kho được sửa ở 7A2 · tiền: 0.

### 24/10/2026 — Dùng thật ở Phase 7B
Đủ 176 câu chạy; chấm hai lần chênh ≤0,011 điểm · đề dùng được làm thước đo ổn định (chi tiết:
`BAO_CAO_DANH_GIA.md`).

### 23/10/2026 — Đóng Phase 7A (Golden toàn kho)
176 câu đủ 5 loại, nhóm nào cũng ≥10 câu · 100% câu kiểm với file nguồn; 4 câu xóa, 10 câu sửa — chỉ
giữ dữ kiện chắc chắn · phát hiện 53 mục mâu thuẫn trong kho gốc, 21 mục đủ căn cứ để sửa → dẫn tới
Phase 7A2 (sửa kho).

### 24/08/2026 — Phase 7: chấm thử bản món ăn, 104 câu
Lần đầu chatbot được chấm: tìm đoạn MRR 0,83; câu trả lời Đúng/Đủ/Trúng ý 4,37 / 4,02 / 4,19; 103/104
câu chấm được · mốc lịch sử cho kho món ăn, không so trực tiếp với số toàn kho · có notebook và giao
diện Gradio để xem từng câu · ý tưởng chấm được giữ, nhưng code **đã thay** ở Phase 7B.

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`, sau dọn) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026; các dòng 8.1 kiểm ngày 25/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Golden 176 câu + smoke 10, schema 4 trường (`question`, `keywords`, `reference_answer`, `category`) | **còn dùng** (Phase 7B, Phase 8) | `backend/evaluation/golden_full_corpus.py:26–28`; `backend/evaluation/full_corpus_eval.py:43–44` |
| 5 loại câu (gồm `out_of_scope`) | **còn dùng** | kiểm `check` 24/10; spec [R3] |
| File soạn theo nhóm (`*/evaluation/golden_full_corpus_authoring.jsonl`) | **còn dùng** cho lệnh `check`/`merge` | `golden_full_corpus.py:113,159` |
| 6 thước đo (MRR@10, nDCG@10, Keyword Coverage@10; Đúng/Đủ/Trúng ý 1–5), trung bình theo câu | **còn dùng** (Phase 7B) | `full_corpus_eval.py` |
| Người chấm là `gpt-6-luna` | **đã thay** bởi Claude chính, `gpt-6-luna` phụ (Phase 7B, bạn chọn) | `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` |
| Không chia đề thành phần luyện / phần giữ kín | **đã thay** (8.1): 120 thử / 56 kiểm + 36 câu kín riêng | `knowledge-base-hue/evaluation/phase_8_1/split.json` (private) |
| Đáp án tham chiếu của 10 câu (bản 7A) | **đã thay** bởi bản sửa 25/10; bản cũ sao lưu | `knowledge-base-hue/meta/golden_backup_2026-10-25/` (private) |
| Mọi câu đều tính vào số chính | **đã thay** (8.1): số chính bỏ 29 câu không tự nhiên | `data/phase_8_1/golden_realism_final.jsonl` (private) |
| Bộ chấm món ăn Phase 7 (`eval.py`, `evaluator.py` Gradio, `test.py`) | **đã thay** bởi `full_corpus_eval.py` (Phase 7B); code **đã gỡ** khi dọn sau Phase 7 (trước đó đường sinh món ăn hỏng: gửi `temperature` → lỗi 400) | commit `1832201` |
| Golden món ăn V2/V3, `tests.jsonl` | **lịch sử**; file private còn, không còn code nào đọc (code món ăn đã gỡ) | commit `1832201` |
| Notebook `07_evaluation.ipynb` | **đã xóa** khi dọn sau Phase 7 | [R2] §2.4; commit `1832201` |

## 6. Việc còn lại / cần quyết

- **Bạn quyết:** xem mẫu câu kín bản 5 lần cuối; sau đó A tạo file chính thức và khóa.
- **Đề xuất 8.2:** gắn thêm đoạn đúng cho câu thử (hiện 32 câu thử thuộc số chính có đoạn đúng, nên nhiều kết quả chỉ "chưa
  rõ"); viết thêm câu kiểu người dùng thật (gõ không dấu, gõ tắt) khi đo khâu từ khóa.
- Keyword là "proxy": đoạn chứa keyword chưa chắc đủ ý; đoạn đúng diễn đạt khác thì bị tính trượt.
- 121/176 câu đã đạt điểm tối đa ở mốc 7B → cải tiến chủ yếu thấy ở 55 câu còn lại.

## Phụ lục — hồ sơ kỹ thuật

- [R1] giả thuyết Phase 8 (bằng chứng chuẩn: §8.4 bước 0): `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7).
- [R2] danh sách dọn sau Phase 7: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- [R3] spec 7A: `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md` (`:32`, `:138`: nối theo partition, không shuffle; code `golden_full_corpus.py:110-121`).
- Đính chính bản 3: C12, theo `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md` §6 mục 13.
- Bản 1 (C8, 24/10/2026, commit `4426ed0`). Bản 4 (C13b): sau dọn B9 (commit `1832201`). Bản 5 (C30, 25/10).
- **8.1** (`report_agent/2026-10-24_phase_8_1_ra_soat/`):
  - chia nhóm `phase_8_1_g0_1_2_measure_implementation.md` (C16);
  - đoạn đúng `phase_8_1_g0_3_gold_review.md` (B14);
  - câu kín `phase_8_1_g0_4_sealed_review.md` §1–§10 (C17–C26);
  - sửa 10 đáp án `phase_8_1_golden_fix_review.md` (C27).
- **Hash (private):**
  - Golden chính thức md5 `0f7dbf41b422` (trước sửa `c30b56f22bd3`); smoke `d80b58c50f38`;
  - `split.json` `e2b1788dfbbc`; nhãn `golden_realism_final.jsonl` `0b65d1c138d2`;
  - câu kín v6 `631334704fdd`; mẫu bản 5 `4f7fe6df5cca`.
- **Lệch phát hiện (24/10):**
  - **Đã xử lý (gỡ ở B9, commit `1832201`):** bộ chấm món ăn từng có hai đường dẫn đề khác nhau —
    `settings.yaml` `evaluation.test_file` trỏ `foods/evaluation/tests.jsonl`, còn mặc định trong
    `backend/evaluation/test.py` là `test2.jsonl`. Cả khóa `evaluation` lẫn `test.py` đã gỡ.
  - Guide `guides/full_corpus_rag.md` mục "Quyết định đã chốt" còn mô tả 7 loại câu cũ; đã có ghi chú
    "7A supersede" ở đầu mục, nên không sai, nhưng người đọc nhanh dễ nhầm.
