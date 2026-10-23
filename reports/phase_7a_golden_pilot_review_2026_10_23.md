# Review: Phase 7A GATE P — module kiểm tra + pilot `heritages`

Decision: changes_requested (correction nhỏ trước Task 3, chờ User xác nhận văn phong và hướng dẫn viết)
Reviewer: Claude Opus 5.5 (`hue-rag-66`)
Date: 2026-10-23 (+07)
Plan: `docs/superpowers/plans/2026-10-23-phase-7a-golden-full-corpus-implementation-plan.md`
Implementation report: `reports/phase_7a_golden_pilot_implementation_2026_10_23.md`

## 1. Phạm vi đã review

Handoff `final_review` Task 1–2. Hai file Task 1, report pilot, 20 case private
và hướng dẫn viết private, cùng các file `heritages/` nằm trong `sources`.
Chi tiết từng case nằm ở file private
`knowledge-base-hue/evaluation/phase_7a_review_notes.md`.

## 2. Findings

Không có blocker.

- **P1 — major (hướng dẫn viết):** 8/20 reference answer thêm dữ kiện ngoài điều
  câu hỏi hỏi. Mẫu `reference_answer` trong hướng dẫn đang yêu cầu "câu sau thêm
  chi tiết". Tác động: ở Phase 7B, Completeness chấm theo reference nên câu trả
  lời đúng mà ngắn bị trừ điểm oan, còn Relevance phạt thông tin thừa. Nếu không
  sửa trước Task 3 thì lỗi nhân lên khoảng 175 case. Tiêu chí đóng: hướng dẫn đổi
  thành "chỉ trả lời đúng điều được hỏi, cộng điều kiện bắt buộc; không thêm dữ
  kiện phụ", và 8 case được cắt gọn.
- **P2 — minor:** 1 case `comparative` hỏi hai dữ kiện chứ không so sánh. Viết lại
  thành câu so sánh thật.
- **P3 — minor:** 2 case dùng keyword số quá chung (dạng `N km`/`N m`), dễ khớp
  nhầm đoạn khác. Hướng dẫn bổ sung: keyword số phải kèm ngữ cảnh nguyên văn
  hoặc đi cùng tên thực thể.
- **P4 — minor:** out-of-scope ledger trong report tracked nêu tên hai thực thể,
  gần như lộ câu hỏi. Thay bằng mô tả chung.
- **Corpus:** Implementer báo K1–K9; Reviewer thêm K10 (hai nhà hát cùng được gọi
  là "cổ nhất"). Ngoài scope Phase 7A; Golden tránh các dữ kiện này. Việc có mở
  lifecycle sửa corpus hay không do User quyết.

Không thấy over-engineering. Module giống hệt plan.

## 3. Cách Reviewer chạy lại

```bash
git status --short; git diff --check                                  # sạch, exit 0
# so khối code trong plan với 2 file: giống hệt
cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_golden_full_corpus.py -q   # 8 passed
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check \
  ../knowledge-base-hue/heritages/evaluation/golden_full_corpus_authoring.jsonl --authoring  # exit 0
# đối chiếu 20/20 case bằng tìm text trong file sources (script tạm ngoài repo)
# tìm text độc lập cho 2 out_of_scope trên toàn corpus curated
```

## 4. Kết quả quan sát

- Module và test: đúng plan, 8 passed. Check pilot exit 0; phân bố
  8/3/4/3/2 (direct_fact/multi_source/comparative/conditional/out_of_scope).
- Độ đúng nội dung: 20/20 case có mọi dữ kiện trong corpus; 2 `out_of_scope`
  thật sự vắng thông tin được hỏi.
- Văn phong: câu ngắn, rõ, tự nhiên, không đánh đố, không câu xin lời khuyên.
- File private được gitignore; report tracked không chứa câu hỏi hay đáp án,
  trừ P4.

## 5. Giới hạn

Độ tự nhiên là đánh giá chủ quan; User là người xác nhận cuối ở GATE P.

## 6. Decision và bước tiếp theo

1. User đọc 20 case cùng hướng dẫn viết và xác nhận văn phong cùng quy tắc
   P1–P3.
2. Implementer làm một correction batch nhỏ: sửa hướng dẫn (P1, P3), cắt 8
   answer, viết lại 1 case (P2), redact ledger (P4), rồi chạy lại `check`.
3. Reviewer kiểm lại delta, rồi mở Task 3 (viết song song, có sub-agent).

## 7. Correction GATE P — re-review (2026-10-23)

User đã đọc 20 case: văn phong ổn, đồng ý P1–P4. Reviewer kiểm lại delta:
đúng 10 dòng thay đổi (#1, #3, #6, #8, #9, #13, #16, #17, #18, #19); 8 answer chỉ
còn đúng điều được hỏi; #18 đã thành câu so sánh thật; keyword #8/#9 đặc thù
và có trong answer; hướng dẫn có quy tắc mới và trỏ tới danh sách mâu thuẫn
corpus K1–K10 (private); report tracked không còn tên thực thể `out_of_scope`.
`check --authoring` exit 0, phân bố giữ 8/3/4/3/2; `git diff --check` exit 0;
module không đổi nên dùng lại `8 passed`.

**P1–P4 CLOSED. GATE P technically passed.** Task 3 mở sau khi User chọn cách
xử lý mâu thuẫn corpus (A: việc sửa riêng sau 7A; B: sửa trước Task 3).
