# Review: Phase 9 B0 — nền (nhánh `p9-b0`, B127)

Người kiểm: C (Claude Opus 5.5, `hue-rag-cc`) · việc **C128** · 19:42 02/11/2026 (`date`). Skill `risk-gated-agent-review`.
Căn cứ: plan B0 bản 2 `c126e7432c82`; report `b127_b0_implementation.md`; diff `18e8f42..215a77f`. Không đọc `STATUS_B` / tin nhắn B.
C chạy trong worktree riêng: `/tmp/c128` (detached `215a77f`) và `/tmp/c128_head` (detached `18e8f42`). **Không sửa** `/tmp/b_p9b0`.

## 1. Phạm vi đã review

- **Git:** nhánh `p9-b0` có đúng 1 commit `215a77f`, cha `18e8f42`, đã có trên `origin/p9-b0`. Khớp report.
- **Đường dẫn đổi** (11 file, +368 / −132):
  - `llm/assistant.py` (mới, thay `grounded_answer.py` bị xoá), `llm/pricing.py` (mới);
  - `llm/generator_openai_full_corpus.py`, `api/routes/chat.py`, `evaluation/full_corpus_eval.py`;
  - 5 file test (1 đổi tên, 1 mới).
  - Không đụng `full_corpus_prompt.py`, `retrieval/`, `settings.yaml`, `frontend/`, đúng như plan §3 "Không chạm".
- **Đọc toàn bộ diff code** (`llm/`, `api/`, `evaluation/`) và đối chiếu với D1–D7 của plan:
  - D1: một lõi, `git mv`.
  - D2: `tim_kho` là hàm thường; tham số vị trí chỉ có `cau_tim`; `TOOLS` đặt một chỗ.
  - D3: `assistant.py` không import SDK.
  - D4: `so_nguon`, và `check_citations` đọc từ đó.
  - D5: mỗi lượt một `CallLog` mới; `pricing.py` dời nguyên văn; `full_corpus_eval` import lại `cost_usd`.
  - D6: vòng stream vẫn ở `chat.py`.
  - D7: `route = "tro_ly_hue"`.
  - **Khớp.** Không thấy thay đổi ngoài phạm vi, cũng không thấy phần phòng xa.
- `git diff --check 18e8f42..215a77f`: sạch.

## 2. Findings

**0 blocker · 0 major · 1 minor.**

### m-1 (minor, không mở vòng mới) — `/api/chat` và `answer_case` bỏ mất `llm_calls` khi model đã trả lời nhưng lượt vẫn lỗi; route stream thì giữ

- **Vị trí:** `generator_openai_full_corpus.py` `_execute_agent`. `call_log` là biến cục bộ; chỉ khi chạy thành công nó mới được gắn vào `GeneratedText` (`_generated_text(…, call_log)`). `assistant.py` `answer_query` gọi `record_llm_calls` sau khi `generate_answer` thành công.
- **Ca bị ảnh hưởng:** model trả lời xong, rồi `parse_structured_output` ném `GenerationError`; hoặc hết giờ sau khi đã có phản hồi. Khi đó `CallLog.calls` đã có một mục (token thật, tiền thật), nhưng `usd` ghi `None`.
  - Route stream thì khác: `chat.py` ghi `call_log.calls` ở `finally`, nên cùng loại lỗi vẫn có số.
  - [Code — chưa tạo được ca thật: không có cách 0 USD để model trả JSON hỏng.]
- **Tác động:** nhỏ. Ca này hiếm, và `None` vẫn đúng tinh thần "không đoán". Nhưng hai đường ghi khác nhau cho cùng một ca lỗi, và tổng USD Phase 9 sẽ đếm thiếu những câu này.
- **Tiêu chí đóng (B chọn):**
  - (a) `GenerationError` mang theo `calls` của lượt, `answer_query` ghi vào `trace` ở `finally`; hoặc
  - (b) ghi rõ giới hạn này vào report / docstring `turn_usd`.
  - Không cần review lại.

### Ghi chú (không phải finding)

- **Ngắt giữa stream có tốn tiền thật nhưng log ghi `usd: None`.** Ca dò ở §4 cho thấy model đã sinh 23 mảnh chữ trước khi client cắt. Plan chấp nhận điều này ("không có usage, không đoán"). Khi B7 cộng tiền cả Phase thì nên nhớ: câu bị ngắt không được tính.
- **Tài liệu còn nhắc `grounded_answer`:** đã liệt kê ở plan §6 / report §5 (A sửa lúc merge, gồm cả `Project_Status.md` §4 "không ghi USD").
- Script cũ trong `data/` không gọi `start_answer_stream` / `finish_answer_stream`, nên đổi chữ ký không làm hỏng chúng. `grep` cũng chỉ thấy probe của chính C.

## 3. Cách người kiểm chạy lại thật

Mọi lệnh chạy với `uv run --project /home/minhhieu/hue_rag`, `HF_HUB_OFFLINE=1`, trong `/tmp/c128/backend` (nhánh) hoặc `/tmp/c128_head/backend` (`18e8f42`).
Bằng chứng ở `data/phase_9/c128_review/` (private).

1. **T-7 một lõi:** `git -C /tmp/c128 grep -n grounded_answer -- backend` ⇒ **0 dòng** (trên `18e8f42` là 9 dòng).
2. **T-1 chạy lại** (cả hai cách của plan):
   - `python -m evaluation.full_corpus_eval retrieval --out …/t1_branch_c.jsonl`;
   - `python ../data/phase_9/b0/tools/t1_qua_tim_kho.py …/t1_tim_kho_c.jsonl`.
3. **T-2 — ca dò khác cách B** (W32): `http_body.py` sha `2fb997a106b5`.
   - B bắt **kwargs** của `AsyncResponses.create`. C bắt **byte thân HTTP** ở `httpx.AsyncClient.send`, tức là sau khi thư viện `openai` đã tuần tự hoá, đúng chuỗi sẽ đi ra mạng. Lời gọi ném `ConnectError` trước khi gửi: 0 USD, 0 request ra ngoài; host khác `api.openai.com` cũng ném lỗi.
   - Dựng generator bằng `from_environment` thật, với `OPENAI_API_KEY=capture-only`, `max_retries=0`.
   - Chuẩn hoá **duy nhất**: thay `prompt_cache_key` dạng `agents-sdk:run:<32 hex>` bằng hằng. Mỗi thân phải khớp đúng 1 lần, nếu không thì ném lỗi.
   - Hai đường trên 10 câu smoke: `answer_case`, và `prepare_answer` → `start_answer_stream` (đọc hết).
   - Chạy `18e8f42` hai lần, rồi `215a77f` một lần.
4. **Ngắt giữa stream, chạy thật** (A dặn: B mới đọc code).
   - uvicorn của nhánh, cổng 8842 (`--env-file` tuyệt đối); `/health` ra 5 / 5 ready.
   - Cùng một câu tự viết (trong kho), gửi `/api/chat/stream` 3 lần: (a) đọc hết; (b) `curl -m 1.5` cắt giữa chừng; (c) `curl -m 3`.
   - Đọc `chat_metrics` + `chat_stream_drain` (`stream_ngat_log.txt` `ac14893a8159`). `grep -F` câu hỏi trong log. Tắt server bằng TaskStop; `/health` không còn trả lời.
5. **Test không key:** cùng lệnh T-8 của plan, chạy trên nhánh.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| T-7 | **PASS**: 0 dòng `grounded_answer` trong `backend/` của nhánh |
| T-1 | **PASS**: `t1_branch_c` và `t1_tim_kho_c` đều sha **`4d5bbe9e0edc`**, 158 dòng mỗi file |
| T-2 (ca dò C, byte HTTP) | **PASS**: 3 file kết quả (HEAD lần 1, HEAD lần 2, nhánh) **giống hệt nhau** (sha `316172f7648e`). Mỗi câu đúng 1 thân `POST /v1/responses`: 10 / 10 `answer_case` + 10 / 10 stream. Cùng một câu, thân thường khác thân stream (đúng thiết kế: `stream: true`) |
| Ngắt giữa stream (chạy thật) | (a) `success`, `n_llm_calls` 1, `llm_calls` đủ 9 trường + `route`, `usd` = `cost_usd(token)`. (b) **cắt sau 23 `delta`** ⇒ `outcome: client_disconnected`, `usd: None`, `n_llm_calls: 0`, `llm_calls: []`, `tools` có `tim_kho`; `chat_stream_drain {finished: true}`. Đúng như plan và report mô tả. (c) xong trước 3 s ⇒ `success` (không cắt được; ghi đúng như vậy) |
| T-6 (trên lượt của C) | **PASS**: `grep -cF` câu hỏi trong log = 0; 3 dòng `chat_metrics` = 3 request |
| T-8 (không key) | 35 passed / 3 error; 3 error đúng 3 test cần key. Khớp report |
| Độ đơn giản | Mỗi phần mới gọi tên được việc của nó (`tim_kho`, `TOOLS`, `CallLog`, `call_entry`, `record_llm_calls`, `turn_usd`, `pricing`); không có lớp bọc hay cấu hình phòng xa |

**Câu bất biến đã kiểm:** "Thân yêu cầu gửi OpenAI của đường RAG 1–8 không đổi qua B0." Kiểm ở mức byte HTTP, độc lập với bảng chuẩn hoá kwargs của B. **Đúng.**

**Tiền của C:** 3 request stream thật. Từ log: 0,000239 + 0,000240 = 0,000479 USD, cộng lần bị ngắt (không có usage, ước ≈ 0,00024) ⇒ **≈ 0,0007 USD** (trần 0,005).

## 5. Giới hạn hoặc phần chưa chạy

- Ca dò T-2 của C dùng 10 câu smoke, không phải 176 câu. B đã chạy 176 câu bằng cách của B.
- Không tạo được ca "model trả JSON hỏng" (m-1), chỉ đọc code.
- Chỉ cắt được 1 lần giữa `delta`. Chưa cắt **trước** `delta` đầu tiên (lúc đang chờ model), vì phải canh giờ chính xác hơn. Hai đường đi qua cùng một nhánh `except (CancelledError, GeneratorExit)`, nhưng điều này chưa chạy thật.
- Không chạy lại T-9 cổng ổn định đầy đủ (`/` cần bản build trong worktree của C) và các test cần key. Dùng lại bằng chứng của B, vì đầu vào giống nhau (cùng commit `215a77f`).

## 6. Decision và bước tiếp theo

**`ready_for_user_confirmation`** cho nhánh `p9-b0` `215a77f`.

- m-1 sửa hoặc ghi giới hạn khi tiện, không mở vòng review mới.
- Trước merge, A làm "5 chỗ" (plan §6): báo cáo khâu, `01_LUONG_HOAT_DONG_HE_THONG.md`, `Project_Status.md` §4 (có `usd` trong `chat_metrics`), guide 6, nhật ký.
- Worktree của C (`/tmp/c128`, `/tmp/c128_head`) đã gỡ, script tạm `/tmp/c128_probe` đã xoá. Worktree `/tmp/b_p9b0` của B để B gỡ sau merge.
