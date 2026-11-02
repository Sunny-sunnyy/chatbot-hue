# Implementation Report: Phase 9 B0 — nền (lõi chung `assistant.py`, `tim_kho`, sổ nguồn, log USD + ms)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-e7`) · việc **B127** · 19:34 02/11/2026 (`date`).
Plan: `docs/superpowers/plans/2026-11-02-phase-9-b0-plan.md` bản 2 sha `c126e7432c82` (A duyệt; review C124 vòng 2 ready).
Nhánh **`p9-b0`** commit **`215a77f`** (từ `main` `18e8f42`), đã push `origin`; worktree `/tmp/b_p9b0`. **Chưa merge.**
Spec: `docs/superpowers/specs/2026-11-02-phase-9-design.md` bản 9 `169c2dd5f86a` §3, §5 B0. Tiền paid: **≈ 0,0020 USD** (trần 0,01).
Report tracked, repo public: không chép câu Golden / kho; số đếm + sha; dữ liệu chạy ở `data/phase_9/b0/` (private).

## 1. Phạm vi

Làm đúng §1 "Làm" của plan; không làm phần "Không làm" (định tuyến, vòng công cụ do model, nhớ, web, đổi lời dặn / `ModelSettings` / ngữ cảnh, dời vòng stream,
sửa báo cáo / guide / `Project_Status.md`). Hành vi chatbot người dùng thấy **không đổi** (T-2: chuỗi gửi model giống byte); thêm trường log.

## 2. Thay đổi chính

| File | Thay đổi |
|---|---|
| `backend/llm/grounded_answer.py` ⇒ `backend/llm/assistant.py` | một lõi (D1). `tim_kho(cau_tim, *, retrieval_service, context_builder, trace)` = tìm + dựng ngữ cảnh (phần trước model cũ), ghi `trace.tools` `{name, ms}` + sổ nguồn; `TOOLS = {"tim_kho": tim_kho}` (D2). `AnswerTrace` thêm `route` (`"tro_ly_hue"`, D7), `so_nguon`, `tools`, `llm_calls`. `check_citations` đọc `so_nguon` (D4). `record_llm_calls` gắn tuyến vào từng lần gọi; `turn_usd` = cộng USD (0 khi không gọi model, `None` khi đã gọi mà không có usage). Không import SDK / client mạng (D3) |
| `backend/llm/pricing.py` (mới) | `cost_usd` + 4 hằng giá dời nguyên văn từ bộ đánh giá |
| `backend/llm/generator_openai_full_corpus.py` | `CallLog(RunHooks)` mỗi lượt một đối tượng, `hooks=` ở `Runner.run` + `Runner.run_streamed`; `call_entry` (loại đầu ra, ms, USD giá đủ, 5 loại token); `GeneratedText.llm_calls`; `start_answer_stream` trả `(result, CallLog)`, `finish_answer_stream(result, call_log, started)` |
| `backend/api/routes/chat.py` | import `llm.assistant`; `METRIC_FIELDS` thêm `route`, `usd`, `n_llm_calls`, `llm_calls`, `tools`; route stream ghi `CallLog.calls` ở `finally` (cả khi ngắt / lỗi) |
| `backend/evaluation/full_corpus_eval.py` | import `llm.assistant`, `llm.pricing`; dòng `answer_case` thêm `route`, `usd`, `llm_calls`, `tools`. `run_retrieval_eval` **không đổi** |
| tests | `test_assistant.py` (đổi tên), `test_chat_stream.py` (dựng trace có `so_nguon`), `test_api_chat.py` (3 chỗ tên module), mới `test_assistant_boundary.py` (T-3, T-4), thêm 1 test `CallLog` ở `test_openai_full_corpus_generator.py` |

Diff: 11 file, +368 / −132 (gồm 99 dòng file cũ xoá ↔ 143 dòng file mới).

## 3. Cách đã chạy thật

Mọi lệnh từ `/tmp/b_p9b0/backend`, `uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`. Thứ tự: **mốc HEAD trước khi sửa** (cùng worktree, `18e8f42`) ⇒ code ⇒ 0 USD trên nhánh ⇒ có phí.

1. **T-2 bắt chuỗi gửi model** (0 USD, không mạng, không nạp `.env`, `OPENAI_API_KEY=capture-only`): `data/phase_9/b0/tools/capture_model_request.py` thay `AsyncResponses.create`
   bằng hàm ghi kwargs rồi ném lỗi; chuẩn hoá đúng bảng plan §4 (`Omit`/`NotGiven` ⇒ `"<omit>"`; `prompt_cache_key` kiểm `^agents-sdk:run:[0-9a-f]{32}$` rồi ⇒ `"<run-key>"`; so chéo bỏ `stream` + `X-Stainless-Raw-Response`).
   Chạy thử 2 câu × 2 lần trước (W36 4b) ⇒ đủ: HEAD lần 1, HEAD lần 2, nhánh ⇒ `req_head_1_*`, `req_head_2_*`, `req_branch_*`.
2. **T-1:** HEAD + nhánh `python -m evaluation.full_corpus_eval retrieval --out …` ⇒ `t1_head.jsonl`, `t1_branch.jsonl`; nhánh `data/phase_9/b0/tools/t1_qua_tim_kho.py` ⇒ `t1_branch_tim_kho.jsonl`; `sha256sum`, `cmp`.
3. **T-8:** `python -m pytest tests/test_assistant.py tests/test_assistant_boundary.py tests/test_chat_stream.py tests/test_api_chat.py tests/test_openai_full_corpus_generator.py -q`
   không key trên HEAD (tên cũ `test_grounded_answer.py`) và nhánh; rồi 3 test cần key với `--env-file /home/minhhieu/hue_rag/.env`.
4. **T-7:** `git grep -n grounded_answer -- backend`.
5. **T-9 cổng ổn định** (có phí): `cd frontend && npm ci && npm run build`; `uvicorn api.app:app --port 8841` (`--env-file` tuyệt đối); `/`, `/health`;
   `/api/chat` 1 câu trong kho + 1 câu ngoài kho, `/api/chat/stream` 1 + 1 (câu tự viết, `data/phase_9/b0/gate/questions.txt`); tắt bằng TaskStop.
6. **T-5 (b):** `python -m evaluation.full_corpus_eval generate --golden smoke --cases 2 23 41 --out ../data/phase_9/b0/gen_smoke3.jsonl`.
7. **T-6:** `grep -cF` từng câu cổng trong dòng log mới (`data/phase_9/b0/gate/log_new.txt`).

## 4. Kết quả quan sát

| Mã | Kết quả | Bằng chứng (private `data/phase_9/b0/`) |
|---|---|---|
| T-1 | **PASS** — `t1_head` = `t1_branch` = `t1_branch_tim_kho` = sha **`4d5bbe9e0edc`**; `cmp t1_head t1_branch_tim_kho` = 0 khác | `t1_*.jsonl` |
| T-2 | **PASS** — HEAD 2 lần: 176 / 176 + 20 / 20 cùng sha, 0 lỗi dạng khoá; nhánh = HEAD **176 / 176** (`answer_case`) + **20 / 20** (2 route × 10 smoke); so chéo `/api/chat` ↔ stream 10 / 10 bằng nhau (cả HEAD và nhánh); mỗi lượt đúng 1 lần bắt | `req_head_1_*`, `req_head_2_*`, `req_branch_*` |
| T-3 | **PASS** — cây AST từ `api.app` có `api.routes.chat`, `llm.assistant`, `llm.generator_openai_full_corpus`, `embedding.full_corpus`, `ingestion.preview` (nạp lười); 0 vi phạm; `llm.assistant` 0 import mạng / SDK | `tests/test_assistant_boundary.py` (3 test) |
| T-4 | **PASS** — `TOOLS` = {`tim_kho`}, tham số vị trí = (`cau_tim`), không tham số URL | `test_tools_take_only_declared_parameters_and_no_url` |
| T-5 | **PASS** — (a) test khoá tập trường `chat_metrics` qua (lỗi ngân sách) — (b) 5 dòng `chat_metrics` cổng + 3 dòng `answer_case`: đủ `route`=`tro_ly_hue`, `usd`, `n_llm_calls`=1, `llm_calls` (mỗi mục đủ 9 trường), `tools` (`tim_kho`, 23–118 ms); `ms` lần gọi 1.872–5.027; Σ USD từng lần = `usd` câu = `cost_usd(token câu)` sai lệch < 1e-9 ở 8 / 8; `kind` thấy `['message']` và `['reasoning','message']` | `gate/log_new.txt`, `gen_smoke3.jsonl` |
| T-6 | **PASS** — 0 dòng log chứa câu hỏi (5 câu cổng); mã phiên: không áp dụng (B0 chưa có phiên — B3) | `gate/log_new.txt` |
| T-7 | **PASS** — 0 dòng | `git grep` |
| T-8 | **PASS** — không key: HEAD 30 pass / 3 error; nhánh **35 pass / 3 error** (+4 test ranh giới + 1 test `CallLog`); 3 error đúng 3 test cần key (`require_openai_key`, như `Project_Status.md` §8); có key: **3 / 3 pass** | lệnh §3 bước 3 |
| T-9 | **PASS** — `/` 200; `/health` 5 / 5 ready; `/api/chat` câu trong kho 200 có 5 nguồn, trích `[1] [2] [5] [7] [8]`; câu ngoài kho = câu từ chối chuẩn, 0 nguồn; stream câu trong kho: `status ×2 … delta … sources` (có nguồn) `… done{success}`; stream câu ngoài kho: chữ ghép = đúng câu từ chối chuẩn, `sources` = `[]` (model gọi, `outcome` route ghi `success` như hôm nay); `chat_metrics` mới = số câu gửi (5); cổng 8841 đóng sau TaskStop | `gate/` |

**Tiền thật (từ log mới):** cổng 5 câu 0,001364 + `generate` 3 câu 0,000617 + 3 test có key ≈ 0 (không gọi model) ⇒ **≈ 0,0020 USD**.

**Quan sát phụ (không thuộc tiêu chí):**
- Câu "trong kho" đầu tiên B tự viết cho `/api/chat` ra câu từ chối, 0 nguồn ⇒ B gửi thêm 1 câu trong kho khác (5 câu thay vì 4). T-2 đã chứng minh chuỗi gửi model giống HEAD, nên đây là hành vi sẵn có của RAG 1–8 (từ chối nhầm / kho thiếu), không do B0 — B không đào nguyên nhân (ngoài phạm vi).
- Mọi lần gọi: `cached_tokens` = 0, `cache_write_tokens` 1.309–2.397 — khớp ghi chú A về thí nghiệm cache key sau B0.

## 5. Lỗi và giới hạn

- `llm_calls` khi ngắt / lỗi giữa chừng ở stream: chỉ có mục của lần gọi đã xong (thường rỗng ⇒ `usd` = `None`) — **[Code, chưa chạy]** đường ngắt thật; test hook chỉ là logic thuần.
- T-2 qua `TestClient` chỉ so thân yêu cầu; hành vi luồng thật kiểm ở T-9 trên uvicorn.
- T-3: import động (`importlib`, `__import__`) không theo được (ghi trong test).
- Mẫu Golden ~30 câu "khoá ở B0" là C123 — ngoài việc này.
- Tài liệu còn nhắc `grounded_answer` (plan §6, A sửa lúc merge): `bao_cao_he_thong/LUONG_HOAT_DONG_HE_THONG.md`, `BAO_CAO_SINH_CAU_TRA_LOI_API.md`, `BAO_CAO_SO_SANH_PHUONG_AN.md`,
  `guides/phase_6_generation_api.md`, `session_prompt/Project_Status.md` (kể cả §4 "không ghi USD" ⇒ nay có `usd`).

## 6. Bàn giao cho người kiểm

- Đọc trước: plan bản 2 §2 (D1–D7) + §4 (T-1…T-9, bảng chuẩn hoá T-2); `git diff 18e8f42..p9-b0` (11 file).
- Chạy lại (0 USD): T-1 (3 lệnh §3 bước 2), T-2 (`capture_model_request.py` với tiền tố mới trên nhánh, so `req_head_1_*`), T-3 / T-4 / T-8 (pytest §3 bước 3), T-7.
- Ca dò khác cách gợi ý (W32): đọc `chat_metrics` của một câu bị ngắt giữa stream (uvicorn thật, `curl --max-time` ngắn) ⇒ `llm_calls`, `usd`.
- Worktree `/tmp/b_p9b0` còn (symlink `data/`, `knowledge-base-hue/`, `frontend/dist/` đã build) để người kiểm dùng; gỡ sau merge (`unlink` rồi `git worktree remove`).
