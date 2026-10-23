# Review: Phase 7A Golden full-corpus — GATE R, Task 5 và closure

Decision: PASS — User xác nhận closure ngày 2026-10-23
Reviewer: Claude Opus 5.5 (`hue-rag-66`)
Date: 2026-10-23 (+07)
Spec: `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md`
Plan: `docs/superpowers/plans/2026-10-23-phase-7a-golden-full-corpus-implementation-plan.md`
Implementation report: `reports/phase_7a_golden_implementation_2026_10_23.md`
Review GATE P: `reports/phase_7a_golden_pilot_review_2026_10_23.md`

## 1. Phạm vi đã review

- Task 3: 180 case authoring do 6 sub-agent của Implementer viết, cộng 16 case
  Implementer tự viết cho `heritages`.
- Correction GATE R: 14 case.
- Task 5: merge 176 case và smoke 10.
- Chi tiết từng case nằm ở file private
  `knowledge-base-hue/evaluation/phase_7a_review_notes.md`. Report này không chép
  câu hỏi hay đáp án.

## 2. Findings

**GATE R (180 case).** Reviewer tự đọc 160 case mới về văn phong, nhãn và tính
khách quan. Dữ kiện được đối chiếu độc lập bởi 3 sub-agent read-only của
Reviewer: foods; heritages-mới + festivals + performing_arts; 3 partition
travel. Kết quả: 166/180 OK; 14 case cần xử lý (4 DROP, 10 FIX):

- **Mâu thuẫn corpus chưa biết trước:** K51 (chu kỳ Cầu ngư), K52 (độ cao đèo
  Hải Vân), và nguồn ghi khác nhau về chi phí ăn uống mỗi ngày. Cả 3 case dính
  vào đây đều bị DROP.
- **Câu kiểu tin tức hoặc hành chính, không giống du khách hỏi:** 1 DROP, 1 viết
  lại.
- **Đáp án lấp lửng hoặc mơ hồ:** 4 FIX.
- **Sai nhãn:** 2 FIX.
- **Câu hỏi mơ hồ hoặc rối:** 2 FIX.
- **Keyword quá chung:** 1 FIX.

Đều là major về chất lượng Golden. Tất cả đã đóng ở Correction GATE R: Reviewer
kiểm lại đúng 15 dòng thay đổi so với bản sao lưu.

**Task 5.** Không có finding.

**Quy trình.** Prompt đầu cho sub-agent foods chỉ tóm tắt spec, phần nguyên văn
được gửi bổ sung sau. Đây là minor: Reviewer đã đối chiếu độc lập toàn bộ case
foods (37/38 OK; case còn lại bị DROP vì lý do dữ liệu, không liên quan prompt).

Không có over-engineering: module vẫn giống hệt plan, không thêm cơ chế nào.

## 3. Cách Reviewer chạy lại

```bash
git status --short; git diff --check                                    # exit 0
cd backend
HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_golden_full_corpus.py -q   # 8 passed (GATE P; module không đổi)
for d in foods heritages festivals performing_arts travel/places travel/services travel/tickets; do
  HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/$d/evaluation/golden_full_corpus_authoring.jsonl --authoring
done                                                                    # 7 × exit 0
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl        # exit 0, 176
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl  # exit 0, 10
# smoke deep-equal: 10/10 dòng có nguyên văn trong file chính thức, tại dòng 3 24 42 44 55 82 114 141 155 163
```

## 4. Kết quả quan sát

| Kiểm tra | Kết quả |
|---|---|
| File chính thức | 176 case, 4 field, check exit 0, private (gitignored) |
| Phân bố | direct_fact 75 / multi_source 29 / conditional 29 / comparative 25 / out_of_scope 18. Cả 5 nằm trong ±20% so với target |
| Theo partition | foods 37, heritages 36, festivals 27, performing_arts 17, travel_places 32, travel_services 13, travel_tickets 14. Mọi partition ≥10 |
| Smoke | 10 case, phủ đủ 5 category và 7 partition; deep-equal; User đã duyệt |
| Độ đúng nội dung | 100% case được đối chiếu với nguồn (pilot: Reviewer 20/20; Task 3: 3 sub-agent Reviewer 160/160) |
| User đọc | Pilot 20/20; mẫu 55 case (seed 20261023); duyệt toàn bộ 14 xử lý GATE R |
| Mâu thuẫn corpus | K1–K53, private; Golden không dùng dữ kiện nào trong số này |
| Tracked report | Không chứa câu hỏi, đáp án hay tên thực thể out_of_scope |

## 5. Giới hạn

- Golden do LLM viết rồi người review, không phải câu hỏi người dùng thật.
- Judge sẽ là `gpt-6-luna`, cùng model với generator; xem lại ở Phase 7B/8.
- Keyword proxy vẫn còn nhiễu với các đáp án dạng số hoặc ngày.
- Một số dữ kiện giá và giờ có mốc 09/2026, có thể lỗi thời.
- `multi_source` = 29, sát biên dưới; User đã chấp nhận.
- Nếu sửa corpus, phải chạy lại `check` cho file chính thức và file smoke.

## 6. Decision và closure

User xác nhận đóng Phase 7A ngày 2026-10-23.

User cấp `commit_and_push` cho Reviewer. Phạm vi commit:

- module và test;
- các report Phase 7A;
- tài liệu trạng thái.

Không commit dữ liệu private: `knowledge-base-hue/`, `gửi chatgpt/`.

**Phase kế tiếp (User chọn ngày 2026-10-23):** "Sửa corpus + tạo lại index". Sửa
21 mục đủ căn cứ theo
`gửi chatgpt/kết quả nghiên cứu/TONG_HOP_REVIEWER_2026_10_23.md` (private), rồi
tạo lại index. Phase này cần thiết kế riêng, vì:

- sửa bất kỳ file `.md` nào cũng làm runtime báo `Full-corpus source state is
  stale` và dừng chạy;
- các collection metadata v2 đang immutable.

Phase 7B vẫn đóng cho tới khi có spec và plan riêng.
