# Review: rà code — gói 3a / 3b (C-02 + C-20 so cặp; C-03 một nơi dựng tin nhắn) — C38

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 2 minor không chặn) — việc rủi ro trung bình ⇒ A đóng, báo User
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-c3`)
Date: 2026-10-25 20:46 +0700 (`date`) · nền `main` `83e1aa9` + diff chưa commit của C · chỉ đọc · **0 USD**
Canonical: mục "Đợt 2" trong `session_prompt/CURRENT_HANDOFF.md`; `bao_cao_he_thong/DE_XUAT_SUA_CODE.md` gói 3a / 3b; C-02, C-03, C-20
Implementation report: `report_agent/2026-10-25_ra_soat_code/sua_3_implementation.md`

Không đọc `STATUS_C.md`; không chạy script của C. Mốc "trước" lấy bằng `git show 1b9c126:backend/evaluation/full_corpus_eval.py` và
`git show 1b9c126:backend/llm/full_corpus_prompt.py` (nền C khai; `git diff 1b9c126 83e1aa9 -- <5 file>` rỗng — chỉ thêm commit docs).

## 1. Phạm vi đã review

- **Cổng tối thiểu:** `git status --short` — phần của C đúng 5 file khai báo + report; working tree còn file test 1b của B (`tests/test_api_chat.py`
  thêm 2 test, `tests/test_startup_model_missing.py` mới — chưa sửa code 1b), không chồng 5 file của C. Exact diff 5 file (+68 / −25) đã đọc hết.
  Ngoài phạm vi: không có (không đổi prompt, generator khác ngoài một dòng, harness 8.1, route, context builder).
- Đọc thêm: `retrieval/full_corpus_context.py:36-110` (bộ đếm token gọi `build_answer_messages`), `llm/generator_openai_full_corpus.py:115-185`
  (`Agent(instructions=…)`), mọi nơi dựng chuỗi "Câu hỏi:" (`grep -rn` ngoài test).

## 2. Findings

Không có blocker hoặc major.

### m-01 (minor) — `build_answer_messages` thêm `.strip()` ⇒ thay đổi hành vi nhỏ, đúng hướng, cần ghi một câu
- Vị trí: `llm/full_corpus_prompt.py:24-33`.
- Quan sát: trước, chuỗi **đếm token** (`build_answer_messages`) giữ nguyên `query` / `context`, còn chuỗi **gửi** (generator) có `.strip()` ⇒ câu hỏi
  có khoảng trắng hai đầu bị đếm khác chuỗi gửi (probe: bản cũ `counted == sent` False, bản mới True). Nay cả hai cùng strip.
- Tác động thực tế: 0 — route API strip câu hỏi trước (`api/routes/chat.py:50`), 176 / 176 câu Golden không có khoảng trắng hai đầu (đếm, không in
  nội dung), context đóng gói luôn bắt đầu `[Nguồn` và kết thúc bằng excerpt đã strip (`full_corpus_context.py:61`); 25 / 25 câu thật khớp byte (§4).
- Tiêu chí đóng: report §2 ghi một câu "đếm token giờ strip như chuỗi gửi (trước lệch ở câu có khoảng trắng hai đầu; 0 trường hợp ở API / Golden)".

### m-02 (minor) — test hợp đồng thay `_execute_agent` bằng hàm ghi lại — hợp lệ như kiểm logic, không phải bằng chứng provider
- Vị trí: `tests/test_openai_full_corpus_generator.py:60-76`.
- Đánh giá: key giả qua `monkeypatch.setenv` chỉ để dựng client, bước gọi model thay bằng hàm ghi `(agent.instructions, input)` — kiểm chuỗi gửi đi,
  không gọi mạng. Hợp `Session_Prompt.md` §6 vì không phải bằng chứng duy nhất (cổng ổn định của C có 2 lượt thật). Không cần sửa.

### Ghi chú (không phải finding)
- (c) A hỏi: generator không gọi `build_answer_messages` vì OpenAI Agents SDK nhận system qua `Agent(instructions=…)` (`generator_openai_full_corpus.py:124-127`)
  và chỉ nhận user ở `Runner.run(input=…)` — hợp lý; một hàm dựng nội dung user dùng chung (`build_answer_input`) là cách nhỏ nhất. Chuỗi "Câu hỏi:" còn
  lại: `evaluation/full_corpus_eval.py:400-406` (`build_judge_message` — đầu vào **judge**, khác mục đích) và `experiments/phase_8_1/g4_rerank.py:81` (prompt
  rerank listwise của harness 8.1 đã đóng) ⇒ không còn chỗ dựng trùng chuỗi trả lời. Phần C-03 còn lại (bộ đếm luôn dùng `ANSWER_SYSTEM_INSTRUCTIONS`
  mặc định dù harness truyền `answer_instructions` khác) C đã ghi ở §5 — đồng ý để tới khi harness 8.2 thật sự đổi prompt.
- Plan E1 phải đổi `fn` sang `paired_stats` (`false_refusal`) — C đã ghi; khớp R-04 của B (`kiem_cheo_B.md`).

## 3. Cách người kiểm chạy lại thật

Mọi lệnh `uv run` trong `.venv`, `HF_HUB_OFFLINE=1`, **không** `--env-file` (không key ⇒ không thể gọi paid); Qdrant `:6335` chỉ đọc.
- `cd backend && uv run python -I /tmp/b29/check_3a.py` — nạp `paired_compare` / `compare_variants` cũ (file từ `1b9c126`) và mới, so JSON (sort keys) trên
  5 cặp file thật: judge Claude 7B Run 1 ↔ 2; retrieval 7B `dense_bm25_rrf` ↔ `native_hybrid_rrf`; câu trả lời 7B Run 1 ↔ 2; 8.1 G2.0 ↔ G2.1a; G2.0 ↔ G2.4
  none; thêm `compare_variants` G2.0 ↔ G2.4 none / low / high (Holm). Category từ `run1_answers.jsonl`. Kèm chiều trên dữ liệu thật và input nhỏ tự viết.
- `cd backend && uv run python -I /tmp/b29/check_3b.py` — 25 câu **tự viết** (không Golden) qua retrieval + context thật; với mỗi câu dựng gói context bằng
  `FullCorpusContextBuilder` hai lần (hàm đếm cũ / mới), so `(text, input_tokens, sources)`; so tin nhắn đếm cũ / mới; so chuỗi gửi (f-string generator tại
  `1b9c126`) với `build_answer_input`. Không dựng / gọi generator.
- Đếm câu Golden có khoảng trắng hai đầu (chỉ in số).
- `pytest` liệt kê file: `test_openai_full_corpus_generator.py test_full_corpus_context.py test_full_corpus_eval.py test_citations.py test_phase6_live_smoke.py
  test_api_chat.py test_golden_full_corpus.py`; riêng 2 test mới của C.
- Import 6 harness 8.1 (g1, g2, g3, g4_keyword, g4_rerank, g5).
- Cổng ổn định: **dùng lại** lượt của C (report §4; 2 câu thật, `/` 200, `/health` 5 / 5, marker khớp `sources`, câu ngoài kho từ chối, log sạch) — không chạy
  lại; hợp lệ vì B review đúng diff C đã chạy cổng, 3b đã chứng minh chuỗi gửi giống byte nên đường sinh không đổi.

## 4. Kết quả quan sát

- **(a) 3a — fresh:** 5 / 5 cặp `paired_compare` **SAME** (sha JSON mới: judge `1dee18cd1828`, retrieval `b2389237865a`, câu trả lời 7B `97d865ee29dc`, G2.0↔G2.1a
  `a0ab8e7f9084`, G2.0↔none `4ed139e78bc8`); `compare_variants` (3 biến thể, Holm) **SAME**. Chiều trên dữ liệu thật: `false_refusal` G2.0 → context 10 —
  `mean_a 0,1481 → mean_b 0,0833`, **thắng 7 / thua 0, `better`** (khớp 8.1 "13 → 7"). Input nhỏ tự viết: `citation_error` 3 lỗi → 2 lỗi (một câu mới lỗi)
  ⇒ thắng 2 / thua 1; `completeness` +1 ⇒ thắng 1 / thua 0. `LOWER_IS_BETTER = {citation_error, false_refusal}`; `correct_refusal` (cao tốt) không nằm trong
  đó — đúng.
- **(b) 3b — fresh:** 25 câu, 25 có nguồn · gói context (text, `input_tokens`, nguồn) khác cũ / mới **0** · tin nhắn đếm khác **0** · chuỗi gửi khác **0**.
  Câu có khoảng trắng hai đầu: bản cũ đếm ≠ gửi, bản mới đếm = gửi (m-01). Golden: 0 / 176 câu có khoảng trắng hai đầu.
- **Pytest (fresh):** `72 passed, 2 failed, 7 errors` — **72 passed khớp report C** (43 + 29). 2 failed là `test_api_catches_the_same_error_classes_that_retrieval_raises`,
  `test_stale_corpus_at_startup_returns_409` — **test 1b của B, cố ý đỏ trước khi sửa code 1b**, không liên quan gói 3. 7 error = `require_openai_key` khi không key
  (C-17), đều là test có từ trước. 2 test mới của C: `2 passed`.
- Harness 8.1: 6 / 6 import được, 0 lỗi.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy lại cổng ổn định (dùng lại của C, lý do §3); tiền cổng của C là **ước** (route không log usage) — giới hạn C đã ghi.
- (b) so trên 25 câu tự viết + suy luận về dạng chuỗi (strip) cho phần còn lại; không chạy 176 câu Golden qua retrieval (không cần: chỉ khác khi có khoảng
  trắng hai đầu, Golden 0 câu).

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation.** 3a: hàm so cặp chung đổi dấu đúng chiều, đầu ra cũ giữ nguyên byte trên dữ liệu thật; 3b: một hàm dựng nội dung user, chuỗi gửi
model không đổi. A tự đóng (rủi ro trung bình), commit 5 file + report + review (C thêm một câu m-01 vào report nếu muốn — không chặn). Sau commit, B tiếp gói 1b
(`full_corpus_eval.py:29-31` bỏ chèn `sys.path` thuộc 1b, rebase không xung đột vì 3a chỉ đổi `:613-`).
