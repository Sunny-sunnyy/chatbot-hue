# Báo cáo cho bạn: Bộ câu hỏi chuẩn Golden và chấm điểm thử món ăn (Phase 7, 7A)

**Cập nhật lần cuối: 19:04 24/10/2026 — bản 2: đưa về mẫu mới (Tóm tắt đầu file, checklist 5 mức, mã
nội bộ xuống Phụ lục); nội dung kỹ thuật và số đo giữ nguyên bản 1.**
Người viết: C · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

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
- **Giới hạn chính:** câu do AI viết rồi người duyệt, không phải câu người dùng thật hỏi; keyword chỉ là
  "proxy"; giá vé, giờ mở cửa lấy mốc 09/2026; 121/176 câu đã đạt điểm tối đa ở mốc 7B.
- **Chi phí:** kiểm định dạng không tốn phí.
- **Bạn cần quyết gì (Phase 8):** có tách 176 câu thành phần luyện / phần giữ kín không; có gắn "bằng
  chứng chuẩn" cho 30–40 câu khó không (xem §6).

## 2. Hoạt động thế nào (bản đang chạy)

```text
Phase 7A (làm đề):
đọc file .md → viết thử 20 câu → bạn chỉnh văn phong → 6 sub-agent viết 6 nhóm còn lại
 → máy kiểm định dạng + keyword có nguyên văn trong kho → người kiểm đối chiếu từng câu với kho
 → bạn đọc mẫu → sửa → gộp thành 1 file (xáo cố định) + chọn tay 10 câu smoke

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
| Tách phần luyện / phần giữ kín | **Chưa thực hiện** | Spec 7A chốt không chia; chờ bạn quyết ở Phase 8 |
| Bằng chứng chuẩn (đoạn/dòng đúng) cho câu khó | **Chưa thực hiện** | Đề xuất 30–40 câu, chưa duyệt |
| Câu người dùng thật hỏi | **Chưa thực hiện** | Đề hiện do AI viết, người duyệt |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

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

Kiểm với code (commit `54670a0`) và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Golden 176 câu + smoke 10, schema 4 trường (`question`, `keywords`, `reference_answer`, `category`) | **còn dùng** (Phase 7B, Phase 8) | `backend/evaluation/golden_full_corpus.py:26–28`; `backend/evaluation/full_corpus_eval.py:43–44` |
| 5 loại câu (gồm `out_of_scope`) | **còn dùng** | kiểm `check` 24/10; spec [R3] |
| File soạn theo nhóm (`*/evaluation/golden_full_corpus_authoring.jsonl`) | **còn dùng** cho lệnh `check`/`merge` | `golden_full_corpus.py:113,159` |
| 6 thước đo (MRR@10, nDCG@10, Keyword Coverage@10; Đúng/Đủ/Trúng ý 1–5), trung bình theo câu | **còn dùng** (Phase 7B) | `full_corpus_eval.py` |
| Người chấm là `gpt-6-luna` | **đã thay** bởi Claude chính, `gpt-6-luna` phụ (Phase 7B, bạn chọn) | `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` |
| Không chia đề thành phần luyện / phần giữ kín | **còn đúng theo spec 7A**; Phase 8 chờ bạn quyết | `session_prompt/CURRENT_HANDOFF.md` "Câu hỏi cho User" |
| Bộ chấm món ăn Phase 7 (`eval.py`, `evaluator.py` Gradio, `test.py`) | **đã thay** bởi `full_corpus_eval.py` (Phase 7B); đường sinh câu trả lời món ăn **hỏng** (gửi `temperature` → lỗi 400); nằm trong danh sách dọn | `backend/evaluation/eval.py:148`; `backend/llm/generator_openai.py:44` |
| Golden món ăn V2/V3, `tests.jsonl` | **lịch sử**, chỉ code món ăn đọc | `backend/evaluation/golden_dataset.py:11–16` |
| Notebook `07_evaluation.ipynb` | **đã bỏ dùng** (gọi bộ chấm món ăn); đề xuất xóa | [R2] §2.4 |

## 6. Việc còn lại / cần quyết

- **Bạn quyết (Phase 8):** có tách 176 câu thành phần luyện / phần giữ kín để chấm cuối không (thử và
  báo trên cùng bộ là đo lạc quan; spec 7A từng chốt không chia).
- **Bạn quyết (Phase 8):** có gắn "bằng chứng chuẩn" (đoạn/dòng đúng) cho 30–40 câu khó để đo chính
  xác hơn keyword không — tốn công người (agent soạn, bạn duyệt mẫu); đề xuất, chưa duyệt.
- Keyword là "proxy": đoạn chứa keyword chưa chắc đủ ý; đoạn đúng diễn đạt khác thì bị tính trượt.
- 121/176 câu đã đạt điểm tối đa ở mốc 7B → cải tiến chủ yếu thấy ở 55 câu còn lại.

## Phụ lục — hồ sơ kỹ thuật

- [R1] giả thuyết Phase 8 (bằng chứng chuẩn: §8.4 bước 0): `reports/phase_8_candidate_hypotheses_2026_10_24.md` (C1, C7).
- [R2] danh sách dọn sau Phase 7: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2).
- [R3] spec 7A: `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md`.
- Bản 1 (C8, 24/10/2026, commit `4426ed0`).
- **Lệch phát hiện (24/10):**
  - Bộ chấm món ăn có hai đường dẫn đề khác nhau: `settings.yaml` `evaluation.test_file` trỏ
    `foods/evaluation/tests.jsonl` (`backend/config/settings.yaml:106`), còn mặc định trong code là
    `test2.jsonl` (`backend/evaluation/test.py:8–10`). Không ảnh hưởng hiện tại (bộ chấm món ăn không
    còn dùng, đang được dọn ở B9), chỉ ghi lại.
  - Guide `guides/full_corpus_rag.md` mục "Quyết định đã chốt" còn mô tả 7 loại câu cũ; đã có ghi chú
    "7A supersede" ở đầu mục, nên không sai, nhưng người đọc nhanh dễ nhầm.
