# Review: Streaming S1 — gom lõi chung (chưa stream)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor không chặn)
Người kiểm: A (Claude Opus 5.5) — thay C (C đang việc 1b; A kiểm B/C theo `WORKFLOW.md` §1)
Date: 11:00 01/11/2026 (`date`)
Spec: `docs/superpowers/specs/2026-10-31-streaming-design.md` duyệt `00fb57ee01b2` (§4.8, §5 hàng S1, §6 C4–C5)
Implementation report: `report_agent/2026-10-31_streaming_spec/s1_loi_chung_implementation.md` (`71121b481abd`)

## 1. Phạm vi đã review

- Nhánh `origin/s1-loi-chung` một commit `9c83003`, gốc `74a6082` (= `main`); worktree `/tmp/b_s1` sạch (chỉ symlink untracked `data/`, `knowledge-base-hue/`).
- Exact diff 6 file: `backend/llm/grounded_answer.py` (mới), `backend/core/schema.py`, `backend/api/routes/chat.py`, `backend/evaluation/full_corpus_eval.py`,
  `backend/tests/test_api_chat.py`, `backend/tests/test_grounded_answer.py` (mới). Không có file ngoài phạm vi (không đụng retrieval, prompt, settings, frontend, `cost_usd`).
- Đọc thêm `backend/llm/citations.py` (regex chung) và phần route `chat()` / `error_response` trên nhánh để kiểm đường log + mã lỗi.

## 2. Findings

Không có blocker / major.

- **m-1 (minor, không mở vòng):** `chat.py` — route nay bắt 4 lớp lỗi trong **một** `try` quanh cả lõi (trước: mỗi lớp quanh đúng bước). Hiện đúng hành vi (B `grep raise`: mỗi lớp chỉ
  ném ở bước của nó); rủi ro chỉ khi sau này một bước khác ném cùng lớp ⇒ ra mã lỗi đó thay vì 500. Đã khai báo ở report §5 (b). Tiêu chí đóng: S2 thêm route stream ⇒ người làm
  `git grep` lại các `raise` của 4 lớp; ghi vào mục giới hạn streaming khi đóng spec (a6).
- **m-2 (minor, không mở vòng):** `citation_ms` trong `chat_metrics` nay không gồm `normalize_citations` (đổi nghĩa trường log, chênh micro giây; đã khai báo §5 (a)). Tiêu chí đóng:
  ghi một dòng vào `BAO_CAO_SINH_CAU_TRA_LOI_API.md` (mục log số đo) khi merge nhánh streaming.

Độ đơn giản: `AnswerTrace` điền dần phục vụ hành vi thật (dòng log / dòng chấm của lần lỗi vẫn có số đo bước đã chạy — trước S1 hai nơi có hành vi này riêng lẻ); `GeneratorNotReadyError`
cần vì `ComponentNotReadyError` bị bước tìm / reranker ném (route sẽ bắt nhầm). Không có lớp phòng xa cho S2. Đạt.

## 3. Cách người kiểm chạy lại thật

1. Cổng tối thiểu: `git log main..origin/s1-loi-chung`, `git merge-base`, `git -C /tmp/b_s1 status --short`, `git diff --check main...origin/s1-loi-chung`, đọc exact diff.
2. **Ca dò khác cách (W32)** cho khác biệt 1 §4.8 — chỗ report tự ghi "chỉ lập luận, chưa có ca dò": script `/tmp/a_s1_probe/fuzz_cite.py` (ngoài repo) chạy trên nhánh
   (`cd /tmp/b_s1/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python /tmp/a_s1_probe/fuzz_cite.py`): 200.000 chuỗi ngẫu nhiên (seed `20261101`) ghép từ `[`, `]`,
   "Nguồn" (hoa / thường / tổ hợp dấu rời), khoảng trắng, số 1–10, `[[`, `]]`, câu từ chối chuẩn, xuống dòng ⇒ so `select_cited_sources(raw)` với `select_cited_sources(normalize_citations(raw))`
   (cả tập nguồn trả về lẫn thông báo lỗi).
3. **Câu bất biến:** "chuẩn hóa citation hai lần = một lần" (route chỉ chuẩn hóa một lần, sau khi kiểm) — kiểm trong cùng script.
4. Test file chạm trên nhánh, **không key**: `cd /tmp/b_s1/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_grounded_answer.py tests/test_full_corpus_eval.py tests/test_api_chat.py tests/test_citations.py -q`.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Ca dò citation chữ gốc ↔ sau chuẩn hóa | **PASS** — 200.000 ca, **0 khác** (116.358 ca lỗi + 83.642 ca hợp lệ, cả hai loại đều trùng) ⇒ khác biệt 1 §4.8 (route trả chữ đã chuẩn hóa, `answer_case` giữ chữ gốc) còn nguyên và kết quả kiểm citation không đổi |
| Câu bất biến chuẩn hóa hai lần | **PASS** — 0 lệch |
| Test file chạm (không key) | **39 passed, 1 error** — error là `test_api_chat.py::test_health_is_cached_and_ready_after_real_lifespan`, test đã biết cần `OPENAI_API_KEY` (`Project_Status.md` §8) |
| Đọc diff: 5 khác biệt §4.8 | khớp bảng report §2: (1) route `normalize_citations(trace.answer)`, `answer_case` ghi `trace.answer`; (2) `trace.citation_error` ⇒ route 500 / `answer_case` giữ chữ; (3) `answer_case` `except Exception` ⇒ `row["error"]`, các trường bước đã chạy ghi sau `try`; (4) recorder chỉ route truyền, thứ tự gọi recorder giữ (ngữ cảnh ⇒ từ chối / lỗi ⇒ kết quả sinh ⇒ lỗi citation / `mark_success`); (5) token / `response_id` chỉ vào dòng `answer_case`, `METRIC_FIELDS` không đổi |
| Đường log khi lỗi | `finally: _copy_trace_metrics` chạy ở mọi nhánh trong `_answer`; `chat()` vẫn ghi đúng một dòng (`finally` ngoài) — lỗi không có kiểu vẫn ra 500 chung kèm số đo các bước đã chạy |

**Dùng lại bằng chứng của B (không chạy lại, lý do):** T1 giống byte `4d5bbe9e0edc`, cổng ổn định C4 (2 câu, ≈ 0,0007 USD), `answer_case` 3 câu nhánh ↔ `main`, 2 test cần key — cùng commit
`9c83003`, cùng môi trường; diff không chạm file tìm / chia đoạn (T1 không thể đổi do mã tìm không đổi; lõi gọi đúng `retrieval_service.search` như trước). A không gọi API trả phí (0 USD).

## 5. Giới hạn hoặc phần chưa chạy

- A không chạy lại T1 / cổng ổn định (dùng lại của B, lý do ở trên).
- Nhánh citation hỏng và `generation_failed` chỉ kiểm bằng đọc diff + ca dò logic (không có đường thật ép model / provider lỗi — giống giới hạn spec §10).

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation` cho S1 `9c83003`. Việc trung bình (sửa code trong phạm vi spec đã duyệt) ⇒ A đóng bước S1, báo User. **Không merge `main` bây giờ:** theo mục việc (a1)
nhánh S1–S4 merge một lần sau review cả nhánh bằng agent con ngữ cảnh mới. Bước tiếp: S2 (generator stream + route `/api/chat/stream` + log) trên cùng nhánh, sau khi B xong B107.
