# Implementation Report: Streaming S1 — gom lõi chung (chưa stream)

Người làm: B (Claude Opus 5.5)
Date: 10:55 01/11/2026 (`date`)
Spec: `docs/superpowers/specs/2026-10-31-streaming-design.md` — User duyệt `00fb57ee01b2` (commit `74a6082`); mục việc `CURRENT_HANDOFF.md` "B — S1 streaming: gom lõi chung".
Nhánh: `s1-loi-chung` từ `main` `74a6082`, commit **`9c83003`**, đã push `origin` (không commit `main`). Worktree `/tmp/b_s1`.

## 1. Phạm vi

Đã làm đúng hàng S1 (spec §5): một lõi chung "tìm → ngữ cảnh → sinh → kiểm citation". `POST /api/chat` và `answer_case` cùng gọi lõi đó. **Chưa** có stream; hành vi không đổi.
Không làm (đúng mục việc): route stream, giao diện, `cost_usd`, prompt / model / settings, ghi Qdrant. Không thêm gì "để sẵn cho S2" — lõi chỉ có những thứ hai nơi gọi hôm nay cần.

## 2. Thay đổi chính

Trước khi sửa: `git grep` mọi nơi gọi (`answer_case`: `full_corpus_eval.py` `run_generation`, `experiments/phase_8_1/g2_generate.py`; route: `api/app.py`, `test_api_chat.py`,
`test_phase6_live_smoke.py`, notebook 06 chỉ nhập `ChatResponse` / `SourceResponse`). Chữ ký `answer_case(case, service, context_builder, generator)` giữ nguyên.

| File | Đổi gì |
|---|---|
| `backend/llm/grounded_answer.py` (mới, 86 dòng) | `answer_query(query, retrieval_service, context_builder, generator, trace, recorder=None)` chạy 4 bước và **điền dần** `AnswerTrace` (kết quả tìm, ngữ cảnh, kết quả sinh, chữ gốc, nguồn được trích, lỗi citation, thời gian từng bước). Lỗi đi ra nguyên kiểu; citation hỏng **không ném** mà ghi `trace.citation_error` — vì mỗi nơi xử lý khác nhau. `generator=None` = chưa sẵn sàng ⇒ `GeneratorNotReadyError`, chỉ khi thật sự cần gọi model (ngữ cảnh rỗng vẫn từ chối được — đúng thứ tự route hôm nay). `elapsed_ms` dời vào đây (route dùng chung) |
| `backend/core/schema.py` | thêm `GeneratorNotReadyError` (cạnh các lỗi có kiểu khác). Không dùng lại `ComponentNotReadyError` vì bước tìm / reranker ném lớp đó (`reranking/cross_encoder.py:38-90`) ⇒ route sẽ bắt nhầm |
| `backend/api/routes/chat.py` | `_answer` gọi lõi trong **một** `try`, giữ nguyên 4 nhánh lỗi (503 / 500 context / 502 chưa sẵn sàng / 502 `generation_failed`), recorder, log; `finally` chép số đo từ `trace` vào `chat_metrics` (`_copy_trace_metrics`) ⇒ dòng lỗi vẫn có số đo của các bước đã chạy. Sau lõi: không nguồn ⇒ từ chối; citation hỏng ⇒ 500; ok ⇒ `normalize_citations` rồi trả |
| `backend/evaluation/full_corpus_eval.py` | `answer_case` gọi lõi (không truyền recorder); giữ chữ gốc, giữ chữ khi citation hỏng, mọi lỗi ⇒ `row["error"]`; sau `try` ghi các trường của bước đã chạy (như trước: dòng lỗi vẫn có `top_chunk_ids`, `context_sources`, token nếu bước đó đã chạy) |
| `backend/tests/test_api_chat.py` | test "bắt đúng đối tượng lớp lỗi": thêm `GeneratorNotReadyError` (route ↔ lõi); cặp `CitationIntegrityError` chuyển từ route sang lõi (route không bắt lớp này nữa) |
| `backend/tests/test_grounded_answer.py` (mới) | đường thật (Qdrant chỉ đọc, e5 + tokenizer local, không gọi model): `answer_case` gặp `ContextBudgetError` ⇒ `row["error"]`, không ném; `top_chunk_ids` đủ 10 (bước tìm đã chạy), các trường sau lỗi `None` — bảo vệ §4.8 khác biệt 3 (trước đó chưa test nào chạm `answer_case`) |

**5 khác biệt §4.8 — còn nguyên:**

| # | Khác biệt | Ở đâu sau S1 | Bằng chứng |
|---|---|---|---|
| 1 | route chuẩn hóa `[Nguồn n]`, `answer_case` giữ chữ gốc | route `normalize_citations(trace.answer)` trước khi trả; `answer_case` ghi `trace.answer` | đọc diff; `test_chat_returns_bracket_citations_when_model_writes_nguon_label` đạt. Lõi kiểm citation trên **chữ gốc** cho cả hai: `CITATION_PATTERN` (`citations.py:11`) nhận cả `[n]` lẫn `[Nguồn n]`, thay thế chỉ đổi chữ trong một match ⇒ cùng tập số, cùng câu từ chối ⇒ kết quả kiểm giống kiểm sau chuẩn hóa như route cũ [Code — lập luận, không chạy ca dò riêng] |
| 2 | `answer_case` giữ chữ khi citation hỏng; route 500 | lõi ghi `trace.citation_error`; route ⇒ 500 `citation_integrity_error`; `answer_case` ⇒ `row["citation_error"] = str(…)` + giữ `answer` | đọc diff (ca này 0 / 489 lần thật — chưa chạy được bằng model thật) |
| 3 | `answer_case` mọi lỗi ⇒ `row["error"]`; route mã riêng | `answer_case` `except Exception`; route 4 nhánh như cũ | test mới (đường thật); test route 503 / 409 / 500 context / 502 chưa sẵn sàng đều đạt |
| 4 | recorder chỉ route | route truyền `get_current_recorder()`; `answer_case` không truyền | `test_asgi_route_evidence_recorder_integration_with_real_retrieval` đạt (recorder có ngữ cảnh đã đóng gói **trước** nhánh 502 chưa sẵn sàng) |
| 5 | `answer_case` ghi `response_id`, `latency_ms`, token; route không log id | `answer_case` đọc từ `trace.generated`; `METRIC_FIELDS` không đổi | test khóa tập trường `chat_metrics` đạt; 3 dòng `answer_case` có `response_id` |

## 3. Cách đã chạy thật

Mọi lệnh chạy từ `backend/` (worktree `/tmp/b_s1` cho nhánh, working tree chung cho `main`), `uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`. Dữ liệu chạy: `data/streaming_s1_2026-11-01/` (private).

1. **Mốc T1 trên `main` `74a6082` trước khi sửa:** `python -m evaluation.full_corpus_eval retrieval --out ../data/streaming_s1_2026-11-01/t1_head_74a6082.jsonl` (không nạp key).
2. **T1 trên nhánh** cùng lệnh ⇒ `t1_branch_s1.jsonl`; `cmp` hai file.
3. **Test file chạm** (không key): `python -m pytest tests/test_grounded_answer.py tests/test_api_chat.py tests/test_full_corpus_eval.py tests/test_citations.py tests/test_phase6_live_smoke.py -q`;
   2 test cần key chạy lại với `--env-file /home/minhhieu/hue_rag/.env`: `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan` + cả `test_phase6_live_smoke.py`
   (lifespan chỉ dựng client, không gọi model — `api/app.py` bước 3).
4. **Cổng ổn định §6 C4 trên `/api/chat`:** `uvicorn api.app:app --port 8765` (nhánh, `--env-file` tuyệt đối); `/` + `/health`; 2 câu tự viết (1 câu món ăn trong kho, 1 câu ngoài kho về
   vé máy bay nước ngoài); đếm `chat_metrics` mới trong `backend/logs/application.log` của worktree (mốc lấy ngay trước câu đầu); `grep -cF` câu hỏi trong log; tắt server (TaskStop).
5. **`answer_case` 3 câu dev** (`split.json` nhóm `dev`; 1 câu hỏi thẳng, 1 câu nhiều nguồn, 1 câu ngoài kho; không câu kín, không nhóm test):
   `python -m evaluation.full_corpus_eval generate --cases <3 case_index> --out …` trên **nhánh** và trên **`main`**, rồi so từng dòng (khóa, `top_chunk_ids`, luật citation / từ chối, token vào).
6. `git diff --check`; hook `pre-commit` tự chạy lúc commit trên nhánh.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| T1 158 câu | **PASS** — `main` trước sửa `4d5bbe9e0edc` = mốc; nhánh `4d5bbe9e0edc`; `cmp` giống byte |
| Test file chạm | **PASS** — 57 passed (không key) + 20 passed (chạy lại 2 file có test cần key; gồm 2 test trước đó báo lỗi thiếu key). 0 lần gọi model |
| Cổng ổn định C4 (`/api/chat`) | **PASS** — `/` 200; `/health` 5 / 5 `ready`; câu trong kho 200, trích `[1]`, `[8]` ⇔ `sources` id 1, 8, không còn chữ "Nguồn"; câu ngoài kho 200, `refusal: true`, 0 nguồn; `chat_metrics` mới **2 = 2 câu**, đủ trường, `outcome` `success`; câu hỏi trong log **0** (cả hai câu + mẩu đầu câu); server đã tắt (`curl` không trả lời). Dòng log: `data/streaming_s1_2026-11-01/c4_chat_metrics_branch.log` |
| `answer_case` 3 câu dev, nhánh ↔ `main` | **PASS** — cả 3: cùng tập khóa, cùng `top_chunk_ids`, cùng `context_sources` 10, cùng `input_tokens`; citation hợp lệ ở 2 câu có trả lời (cùng tập số trích ở hai bên), câu ngoài kho từ chối ở cả hai; `citation_error` / `error` = `None`; có `response_id`. Chữ trả lời khác nhau theo lần gọi model (không tất định) — không so chữ |
| `test_phase6_live_smoke.py` | **PASS** (chạy được với key, không gọi model) — không phải NOT RUN |
| `git diff --check`; hook | sạch; hook quét 6 file ⇒ 0 trùng kho / Golden |

**Tiền (paid `gpt-6-luna`):** cổng ổn định 2 câu: vào 4.369 / ra 230 token; `answer_case` nhánh: vào 3.715 / ra 166; `main`: vào 3.715 / ra 155. Tổng vào 11.799 / ra 551 ⇒ **≈ 0,0018 USD**
nếu tính phần vào theo giá ghi đệm 0,125 (B95: mỗi câu ghi đệm ≈ toàn bộ phần vào) — ≈ 0,0015 USD theo giá phẳng 0,10. Trần việc 0,005 USD.
Câu trong kho của cổng ổn định mất 6,7 s phần sinh (một lần, không phải lượt đo tốc độ).

## 5. Lỗi và giới hạn

- **Đổi nhỏ, không đổi phản hồi:** (a) `citation_ms` nay chỉ đo bước kiểm, không gồm `normalize_citations` (route chuẩn hóa sau lõi) — chênh micro giây, log đều làm tròn 0,1 ms;
  (b) route bắt 4 lớp lỗi trong **một** `try` quanh cả lõi, trước đây mỗi lớp chỉ bắt ở bước của nó. Trong code hiện tại mỗi lớp chỉ được ném ở đúng bước của nó (`grep raise`:
  `ContextBudgetError` chỉ ở `full_corpus_context.py:98`; generator chỉ ném `GenerationError` / `ValueError`) ⇒ cùng hành vi; nếu sau này một bước khác ném các lớp này thì sẽ ra mã lỗi
  đó thay vì 500 chung.
- Khác biệt 2 (citation hỏng) và nhánh `generation_failed` chỉ kiểm bằng đọc diff — không có tham số thật ép model bỏ `[n]` hay lỗi provider (giống giới hạn spec §10).
- Khác biệt 1 kết luận bằng lập luận trên regex, chưa có ca dò riêng (ví dụ chữ có `[Nguồn 01]`).
- Không chạy lại 176 câu có judge (spec C5: lõi chung giữ T1 + hành vi §4.8).
- Ngoài phạm vi, thấy khi đọc: `test_chat_returns_bracket_citations_when_model_writes_nguon_label` dùng generator chữ cố định (`SimpleNamespace`) — lệch luật "không stub" của dự án, có từ trước S1; không sửa.

## 6. Bàn giao cho người kiểm (C)

- Đọc trước: diff `git diff 74a6082 9c83003` (6 file); spec §4.8 + hàng S1 §5; bảng 5 khác biệt ở §2 trên.
- Chạy lại phần rủi ro: T1 trên nhánh (lệnh §3 bước 1, so `4d5bbe9e0edc`); `pytest tests/test_grounded_answer.py tests/test_api_chat.py -q`; nếu muốn đường thật: cổng ổn định
  §3 bước 4 (≈ 0,0007 USD). Gợi ý ca dò khác cách (W32): chữ model có `[Nguồn n]` + citation sai số ⇒ route 500, `answer_case` giữ chữ (dùng `select_cited_sources` trực tiếp, không cần model).
- Worktree `/tmp/b_s1` còn (symlink `data/`, `knowledge-base-hue/`) — B gỡ khi review xong hoặc A bảo.

**Giải thích ngắn:** trước đây route API và bộ đánh giá mỗi bên tự viết lại cùng chuỗi "tìm → dựng ngữ cảnh → gọi model → kiểm trích dẫn"; nay cả hai gọi chung một hàm, nên sửa
chuỗi này một chỗ là cả chatbot lẫn phép đo cùng đổi, và bước streaming sau (S2) dùng lại được đúng đường đó. Người dùng không thấy gì khác: kết quả tìm giống từng byte, API trả lời
và báo lỗi như cũ.
