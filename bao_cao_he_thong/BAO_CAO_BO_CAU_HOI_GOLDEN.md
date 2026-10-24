# Báo cáo cho bạn: Phase 7 và 7A — Chấm điểm thử (Foods) và bộ câu hỏi chuẩn toàn corpus

```text
Trạng thái: Phase 7 (Foods) đóng 24/08/2026 · Phase 7A (Golden toàn corpus) đóng 23/10/2026
Cập nhật lúc: 24-10-2026 +07
Người viết: C · Review: A
```

## 1. Bạn nhận được gì

**Phase 7 (Foods, 08/2026)** là lần đầu chatbot được **chấm điểm**: chạy một bộ câu hỏi món ăn, đo
bước tìm đoạn (MRR, nDCG, độ phủ keyword) và nhờ một model khác chấm câu trả lời theo 3 tiêu chí
Đúng / Đủ / Trúng ý (1–5). Có notebook và giao diện Gradio để xem từng câu. Cách chấm này về sau được
giữ nguyên ý tưởng, nhưng code đã được thay ở Phase 7B.

**Phase 7A (10/2026)** tạo **bộ câu hỏi chuẩn (Golden) cho toàn bộ kho**: 176 câu phủ cả 5 mảng, cộng
bộ thử nhanh 10 câu. Mỗi câu có: câu hỏi viết như người thật hỏi, đáp án tham chiếu ngắn, keyword lấy
nguyên văn từ kho (để chấm bước tìm đoạn), và loại câu. Đây là "đề thi" mà Phase 7B và Phase 8 dùng.

## 2. Hệ thống hoạt động như thế nào

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

## 3. Đã chạy và quan sát gì

| Nội dung | Kết quả | Ý nghĩa |
|---|---|---|
| Phase 7 Foods, 104 câu (08/2026) | Tìm đoạn MRR 0,83; câu trả lời 4,37 / 4,02 / 4,19; 103/104 câu chấm được | Mốc lịch sử cho kho món ăn; không so trực tiếp với số toàn corpus |
| Golden 7A: số câu | 176 = một dữ kiện 75, nhiều nguồn 29, điều kiện 29, so sánh 25, ngoài kho 18 | Đủ các loại câu, nhóm nào cũng ≥10 câu |
| Đối chiếu dữ kiện lúc làm | 100% câu kiểm với file nguồn; 4 câu xóa, 10 câu sửa | Chỉ giữ dữ kiện chắc chắn |
| Mâu thuẫn trong kho gốc (phát hiện khi làm đề) | 53 mục; 21 mục đủ căn cứ để sửa | Dẫn tới Phase 7A2 (sửa kho) |
| **Kiểm lại hôm nay** (24/10, C chạy `golden_full_corpus check`) | Golden 176 câu đạt; smoke 10 câu đạt, 10/10 câu trùng khớp file chuẩn | Đề vẫn đúng định dạng sau khi kho được sửa ở 7A2 |
| Dùng thật ở Phase 7B | Đủ 176 câu chạy, chấm hai lần chênh ≤0,011 điểm | Đề dùng được làm thước đo ổn định |

## 4. Cách bạn kiểm tra thêm nếu cần

Mở `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` (private, mỗi dòng một câu). Kiểm định
dạng, từ `backend/`, không tốn phí:

```bash
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
```

## 5. Hôm nay còn đúng không

Kiểm với code và `session_prompt/Project_Status.md` §4 ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ |
|---|---|---|
| Golden 176 câu + smoke 10, schema 4 trường (`question`, `keywords`, `reference_answer`, `category`) | **còn dùng** (Phase 7B, Phase 8) | `backend/evaluation/golden_full_corpus.py:26–28`; `backend/evaluation/full_corpus_eval.py:43–44` |
| 5 loại câu (gồm `out_of_scope`) | **còn dùng** | kiểm `check` hôm nay; spec `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md` |
| File soạn theo nhóm (`*/evaluation/golden_full_corpus_authoring.jsonl`) | **còn dùng** cho lệnh `check`/`merge` | `golden_full_corpus.py:113,159` |
| 6 thước đo (MRR@10, nDCG@10, Keyword Coverage@10; Đúng/Đủ/Trúng ý 1–5), trung bình theo câu | **còn dùng** (Phase 7B) | `full_corpus_eval.py` |
| Người chấm là `gpt-6-luna` | **đã thay** bởi Claude chính, `gpt-6-luna` phụ (Phase 7B, bạn chọn) | `report_agent/user_reports/phase_07b_danh_gia_baseline.md` |
| Không chia đề thành phần luyện / phần giữ kín | **còn đúng theo spec 7A**; Phase 8 đang chờ bạn quyết có tách hay không | `CURRENT_HANDOFF.md` "Đang chờ User" |
| Bộ chấm Foods Phase 7 (`eval.py`, `evaluator.py` Gradio, `test.py`) | **đã thay** bởi `full_corpus_eval.py` (Phase 7B); đường sinh câu trả lời Foods **hỏng** (gửi `temperature`, `gpt-6-luna` trả 400); nằm trong danh sách dọn | `backend/evaluation/eval.py:148`; `backend/llm/generator_openai.py:44` |
| Golden Foods V2/V3, `tests.jsonl` | **lịch sử**, chỉ code Foods đọc | `backend/evaluation/golden_dataset.py:11–16` |
| Notebook `07_evaluation.ipynb` | **đã bỏ dùng** (gọi bộ chấm Foods); đề xuất xóa | `reports/phase_7_cleanup_inventory_2026_10_24.md` §2.4 |

## 6. Giới hạn và bước tiếp theo

- Câu hỏi do AI viết rồi người duyệt, không phải câu người dùng thật hỏi.
- Keyword là "proxy": đoạn chứa keyword chưa chắc đủ ý; đoạn đúng diễn đạt khác thì bị tính trượt.
- Giá vé, giờ mở cửa lấy mốc 09/2026, có thể cũ.
- 121/176 câu đã đạt điểm tối đa ở baseline 7B → cải tiến chủ yếu thấy ở 55 câu còn lại.
- Phase 8 có thể thêm "bằng chứng chuẩn" (đoạn/dòng đúng) cho 30–40 câu khó để đo chính xác hơn
  keyword — đề xuất, chưa duyệt.

## Lệch phát hiện

- Bộ chấm Foods có hai đường dẫn đề khác nhau: `settings.yaml` `evaluation.test_file` trỏ
  `foods/evaluation/tests.jsonl` (`backend/config/settings.yaml:106`), còn mặc định trong code là
  `test2.jsonl` (`backend/evaluation/test.py:8–10`). Không ảnh hưởng hiện tại (bộ chấm Foods không còn
  dùng, sẽ dọn), chỉ ghi lại.
- Guide `guides/full_corpus_rag.md` mục "Quyết định đã chốt" còn mô tả 7 loại câu cũ; đã có ghi chú
  "7A supersede" ở đầu mục, nên không sai, nhưng người đọc nhanh dễ nhầm.
