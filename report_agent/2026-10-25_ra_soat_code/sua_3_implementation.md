# Implementation Report: rà code — gói 3a / 3b (C-02 + C-20 so cặp; C-03 một nơi dựng tin nhắn)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-7f`)
Date: 2026-10-25 20:37 (`date`) · nền `main` `1b9c126` · chưa commit (A commit sau review) · paid ~0,0004 USD (ước, xem §4)
Canonical: `bao_cao_he_thong/DE_XUAT_SUA_CODE.md` gói 3a / 3b (User duyệt 19:4x); mục "Đợt 2" trong `session_prompt/CURRENT_HANDOFF.md`; A giao
20:1x; finding C-02, C-03, C-20 (`ra_soat_code_C.md`). Review: B.

## 1. Phạm vi

- **3a (C-02, C-20):** tách hàm so cặp thuần trong `evaluation/full_corpus_eval.py`, đổi dấu theo `LOWER_IS_BETTER`, kết luận đúng chiều; harness
  8.2 sau này gọi hàm đó. **Không sửa harness 8.1** (đã đóng, giữ để tái lập) — C-02 (`g2_generate.paired` ngược dấu với `refusal`) chỉ ghi chú ở đây.
- **3b (C-03):** generator và bộ đếm token context dùng chung một hàm dựng nội dung tin nhắn. Tiêu chí: chuỗi gửi model giống byte trước / sau
  trên ≥ 20 context dựng từ câu tự viết, 0 USD.
- **File (5, khai báo trong `STATUS_C.md` trước khi sửa):** `backend/evaluation/full_corpus_eval.py`, `backend/tests/test_full_corpus_eval.py`,
  `backend/llm/full_corpus_prompt.py`, `backend/llm/generator_openai_full_corpus.py`, `backend/tests/test_openai_full_corpus_generator.py`. Không
  chạm thư mục của 1b (`retrieval/`, `ingestion/`, `embedding/`, `vectorstore/`, `reranking/`, `api/app.py`). **Chồng nhẹ với 1b (b):** plan 1b bỏ
  dòng chèn `sys.path` đầu `full_corpus_eval.py` (`:29-31`); 3a chỉ đổi `paired_compare` (`:613-`) ⇒ khác dòng, rebase không xung đột nội dung.

## 2. Thay đổi chính

- **`paired_stats(a_values, b_values, metric, rounds, seed)`** (mới, `full_corpus_eval.py` ngay sau `paired_compare`): nhận hai dãy giá trị cùng thứ tự
  case, trả đúng các khóa `paired_compare` vẫn trả (`n, mean_a, mean_b, mean_diff, ci95, p_value, wins, ties, losses, verdict`); thắng / thua và
  kết luận theo chiều chỉ số (`sign = -1` khi tên trong `LOWER_IS_BETTER`); `zip(strict=True)` ⇒ hai dãy khác độ dài là `ValueError`. Docstring nói rõ
  chỉ số càng thấp càng tốt phải mang tên trong `LOWER_IS_BETTER` (ví dụ `false_refusal`, không phải `refusal`) — đúng bẫy C-02.
  `paired_compare` giữ nguyên chữ ký và đầu ra, chỉ còn gom case theo nhóm rồi gọi `paired_stats` (công thức giữ nguyên từng phép tính:
  `mean_a = sum / len`, `diffs` float numpy, cùng `bootstrap_mean_diff`). Không thêm tham số chiều / cấu hình.
- **`build_answer_input(query, context)`** (mới, `llm/full_corpus_prompt.py`): một nơi dựng nội dung user `"Câu hỏi:\n{query.strip()}\n\nNgữ cảnh truy
  xuất:\n{context.strip()}"` — đúng chuỗi generator đang gửi. `build_answer_messages` (bộ đếm token context dùng) lấy nội dung user từ hàm này;
  `generate_answer` gọi hàm này thay cho f-string riêng. **Lệch nhỏ so với câu giao "generator dùng `build_answer_messages`":** OpenAI Agents SDK
  nhận system prompt qua `Agent.instructions` lúc dựng agent và chỉ nhận nội dung user ở `Runner.run(input=…)`, nên generator không truyền được cả
  danh sách message; dùng chung hàm dựng nội dung user là cách nhỏ nhất để hai bên không lệch (đúng phương án "một hàm dựng chuỗi chung" của C-03).
- Test: `test_full_corpus_eval.py` +1 test `paired_stats` (input C-02: mốc từ chối nhầm 4 / 24, biến thể 0 ⇒ thắng 4 / hòa 20 / thua 0, `better`;
  cùng chênh với `completeness` ⇒ thua 4, `worse`; độ dài lệch ⇒ `ValueError`). `test_openai_full_corpus_generator.py` +1 test hợp đồng: generator
  gửi đúng `build_answer_messages(...)` (system = `agent.instructions`, user = input), có `.strip()` — key giả qua `monkeypatch.setenv` chỉ để dựng
  client, bước gọi agent thay bằng hàm ghi lại, không gọi mạng, không dùng `require_openai_key` (C-17).

## 3. Cách đã chạy thật

Từ `backend/`, script của C ở `/tmp/c38/`, bản dùng lại `data/ra_soat_code_2026-10-25/tools/sua_3/` (private):

1. **Mốc trước (trước khi sửa, `main` `1b9c126`):**
   - `HF_HUB_OFFLINE=1 uv run python -I /tmp/c38/snap_3a.py /tmp/c38/3a_before.json` — `paired_compare` / `compare_variants` trên file kết quả thật:
     7B judge Claude Run 1 ↔ Run 2; retrieval 7B `dense_bm25_rrf` ↔ `native_hybrid_rrf`; 8.1 G2.0 ↔ G2.1a (từ chối / lỗi citation); `compare_variants`
     G2.0 ↔ G2.4 none / low / high (có Holm). Category lấy từ file câu trả lời 7B (không đọc Golden).
   - `env -u OPENAI_API_KEY HF_HUB_OFFLINE=1 uv run python -I /tmp/c38/snap_3b.py /tmp/c38/3b_before.json` — **25 câu tự viết** (không Golden):
     retrieval + context thật (Qdrant đọc, e5 CPU) ⇒ `packed.text`, `packed.input_tokens`; generator dựng thật bằng `from_environment` với key giả,
     `_execute_agent` thay bằng hàm ghi `(agent.instructions, user_prompt)` ⇒ 0 lời gọi mạng; ghi kèm `build_answer_messages(q, packed.text)`.
2. Sửa code ⇒ chạy lại đúng hai lệnh trên ra `*_after.json`, so bằng `cmp`.
3. Test (không `--env-file`): `test_openai_full_corpus_generator.py`, `test_full_corpus_context.py`, `test_full_corpus_eval.py`, `test_citations.py`;
   thêm `test_phase6_live_smoke.py`, `test_api_chat.py`, `test_golden_full_corpus.py` (đường có generator / evaluator). Import 6 harness 8.1;
   `python -m evaluation.full_corpus_eval --help`.
4. **Cổng ổn định** (`CURRENT_HANDOFF.md`): `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -I /tmp/c38/gate.py` — script khởi
   động `uvicorn api.app:app --port 8011` thật (tiến trình con, cổng trống trước khi chạy), gọi `/`, `/health`, 1 câu trong kho + 1 câu ngoài kho (tự
   viết), đọc log, tắt server.

## 4. Kết quả quan sát

| Tiêu chí | Kết quả |
|---|---|
| 3a: đầu ra so cặp trên file thật | `3a_before.json` **= byte** `3a_after.json` (sha `7722ba991269`; 4 phép so, gồm Holm) |
| 3a: chiều đúng cho chỉ số càng thấp càng tốt | test input C-02: `false_refusal` thắng 4 / hòa 20 / thua 0, `better`; `completeness` cùng chênh ⇒ thua 4, `worse` |
| 3b: chuỗi gửi model (instructions + input) | `3b_before.json` **= byte** `3b_after.json` — 25 / 25 câu (25 có nguồn), gồm cả chuỗi đếm token và `input_tokens` (ví dụ 692, 826, 628 …) |
| 3b: chuỗi đếm = chuỗi gửi | trước sửa: 0 / 25 khác (đầu vào thật không có khoảng trắng đầu / cuối); sau sửa: cùng một hàm dựng — khóa bằng test hợp đồng |
| Test | 4 file chính: **43 passed, 2 error**; 3 file thêm: **29 passed, 5 error** — cả 7 error là test cũ dùng `require_openai_key` khi không có key (C-17), không liên quan; 2 test mới đạt không cần key |
| Harness 8.1 | 6 / 6 import được (g1, g2, g3, g4_keyword, g4_rerank, g5); `evaluation.full_corpus_eval --help` liệt kê 11 lệnh |
| **Cổng ổn định** | `/` 200 (1.346 byte) · `/health` 200 `ok`, 5 / 5 `ready` · câu trong kho 200, 4,0 s, marker [1, 3] = `sources` [1, 3] · câu ngoài kho 200, 3,6 s, từ chối đúng (0 nguồn) · log: 0 dòng `ERROR` / `Traceback` · server tắt (SIGTERM) |
| `git diff --check` | sạch; `git diff --stat -- backend`: 5 file, +68 / −25 |

**Tiền:** 2 lượt `gpt-6-luna` ở cổng ổn định. Route API không ghi usage vào log ⇒ **không đo được** token của 2 lượt này; **ước ~0,0004 USD**
theo lượt đo được ở gói 1a (2 câu, 1.637 + 526 token = 0,000427 USD). Cộng dồn trần chung gói 1–5 (0,05 USD): ~0,0008 USD (1a 0,000427 đo +
3 ~0,0004 ước) — A cộng thêm lượt cổng 1a của A.

## 5. Lỗi và giới hạn

- **C-02 không sửa trong harness 8.1** (theo giao): `experiments/phase_8_1/g2_generate.py:243-254` `paired` vẫn không đổi dấu cho `refusal` — kết
  luận 8.1 không bị ảnh hưởng (8.1 G2 báo số câu từ chối, không dùng `verdict` của `refusal`; kiểm ở C34). Harness 8.2 (E1…) gọi `paired_stats` với
  tên `false_refusal`; plan E1 (C33, sha `f86240418ca1`) phải đổi `fn` sang `paired_stats` ⇒ sha mới khi 8.2 chạy lại.
- **C-03 phần 2 chưa làm:** bộ đếm token context luôn đếm với `ANSWER_SYSTEM_INSTRUCTIONS` mặc định, kể cả khi harness truyền `answer_instructions`
  khác cho generator (P1 của E1 thêm ~45 token). Runtime không đổi prompt nên không ảnh hưởng chatbot; ngân sách còn rộng (16.384 − 2.048 − 512).
  Sửa (cho `FullCorpusContextBuilder` nhận instructions) khi harness 8.2 thật sự đổi prompt — có người dùng thật thì mới thêm tham số.
- C-20 phần "harness import chéo / `OUT_DIR` ghim" không đổi (harness 8.1 đã đóng); `paired_stats` là chỗ chung cho 8.2 để không chép thêm.
- Tiền cổng ổn định là ước (route không log usage). Ý cải tiến ghi `STATUS_C.md`.

## 6. Bàn giao cho người kiểm (B)

- Đọc trước: `git diff -- backend/evaluation/full_corpus_eval.py backend/llm backend/tests/test_full_corpus_eval.py
  backend/tests/test_openai_full_corpus_generator.py`.
- Chạy lại (free): người kiểm tự chụp mốc từ `1b9c126` (`git show 1b9c126:backend/evaluation/full_corpus_eval.py`, …) bằng script riêng, hoặc đọc
  `data/ra_soat_code_2026-10-25/tools/sua_3/snap_3a.py` / `snap_3b.py`; pytest các file ở §3 bước 3 (liệt kê file, không `--env-file`).
- Cổng ổn định: chạy lại chỉ khi người kiểm thấy cần (2 câu ~0,0004 USD, trong trần chung).
- Lệch đã ghi: hàm chung là `build_answer_input` (không phải generator gọi thẳng `build_answer_messages`) — lý do §2.
