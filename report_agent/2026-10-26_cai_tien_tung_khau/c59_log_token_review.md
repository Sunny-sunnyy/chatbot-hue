# Review: C60 — `/api/chat` ghi một dòng log số đo (plan C59)

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor, không mở vòng sửa riêng)
Người kiểm: B (Claude Opus 5.5, `hue-rag-31`) · Việc: B70 (A giao 27/10)
Date: 2026-10-27 13:19 +0700 (`date`)
Plan: `c59_log_token_plan.md` bản 2 sha `7f1456a1ae55` (+ review B68 vòng 1–2: m-4, m-5)
Implementation: `origin/c59-log` `cc70124` (code `2270723`, report `c59_log_token_implementation.md`)
Theo: `risk-gated-agent-review`, `practical-project-coding`. **0 USD**: B không chạy lại cổng có phí; dùng lại dữ liệu cổng của C, lý do ở §3.

## 1. Phạm vi đã review

- `git diff 2ddd65d..origin/c59-log`: đúng 3 file code (`backend/api/routes/chat.py` +54, `backend/llm/generator_openai_full_corpus.py` +5,
  `backend/tests/test_api_chat.py` +46 / −3) + report. Không file nào khác.
- Đọc hết diff code + report.
- Dữ liệu cổng private `data/phase_8_2/c60_gate/{server.log, client.json}`.
- Chạy lại test trên nhánh và trên mốc trong worktree tạm `/tmp/b_c59rev` (đã gỡ).

## 2. Findings

Không có blocker / major.

**m-1 (minor, ghi nhận — không sửa) — test khóa danh sách trắng chỉ phủ các trường gán trước điểm lỗi ngân sách context.**
- Bằng chứng: B thử ngược hai lần.
  - Thêm `metrics["query"] = query` **ngay sau** `context_builder.build` ⇒ test vẫn **xanh**: ở nhánh 500 `context_budget_error`, `build` ném lỗi trước dòng
    đó.
  - Thêm ở **đầu** `_answer` ⇒ test **đỏ** đúng chỗ (`Extra items in the left set`), như C báo.
- Tác động: trường lạ thêm ở phần sinh / citation (đường thành công) không có test không key nào bắt. Chỉ cổng ổn định bắt, vì cổng kiểm "đủ 15 trường"
  và grep câu hỏi = 0.
- Không cần đổi code. Đường thành công cần model thật, mà không được mock (`Session_Prompt.md` §6). Ghi giới hạn này ở report hoặc `Project_Status`
  §8 khi merge.

**m-2 (minor) — `dense_ms` không làm tròn như các trường thời gian khác** (gate: `39.852`, `25.352`; các trường khác 1 chữ số thập phân).
- Lấy nguyên từ `trace.timings_ms`. Vô hại (vẫn là float). Muốn nhất quán thì `round(…, 1)`. Không chặn.

## 3. Bảy điểm A hỏi

1. **Diff đúng plan, 9 `return` không sửa — đạt.**
   - `git diff … chat.py` có **0 dòng xóa** (chỉ thêm). Dòng `async def chat(...)` cũ giữ làm wrapper; thân cũ nằm dưới `async def _answer(body, request,
     metrics)`. Cả 9 `return` (7 `error_response`, 2 `ChatResponse`) giữ nguyên.
   - Thêm đúng các chỗ plan §2.2 + m-5: `refusal_no_sources` gán ngay trước `return` từ chối không nguồn; `generation_failed` gán trong
     `except GenerationError`; wrapper chỉ điền `outcome` khi còn None.
   - Generator: `reasoning_tokens` là trường cuối, có mặc định; đọc `getattr` lồng.
2. **Wrapper giữ hành vi, 500 qua handler chung — đạt** (đọc code).
   - `try` gọi `_answer` → điền `status_code` / `refusal` / `outcome` (chỉ đọc giá trị kiểu thường, `json.loads` body JSON do `error_response` tự tạo)
     → `return response`.
   - `except Exception` gán `internal_error` / 500 rồi `raise` nguyên exception ⇒ `exception_handler(Exception)` ở `app.py` vẫn trả 500 như cũ.
   - `finally` ghi đúng một dòng.
   - `@router.post(..., response_model=ChatResponse)` và chữ ký `chat(body, request)` giữ ⇒ FastAPI kiểm phản hồi như cũ.
   - Đường `internal_error` không chạy thật được nếu không dựng lỗi giả (`Session_Prompt.md` §8) ⇒ đọc code, như C ghi.
3. **Danh sách trắng không lọt nội dung — đạt.** B đọc **dòng log thật** của cổng (`c60_gate/server.log`):
   - **2** dòng `chat_metrics`. Mỗi dòng đúng **15** khóa = `METRIC_FIELDS`. Giá trị chỉ là số / bool / `gpt-6-luna` / mã cố định (`success`).
   - Các dòng còn lại của log là dòng khởi động / dừng cố định.
   - `client.json` không lưu câu hỏi, đúng là không nên lưu. Vì vậy B **không grep lại được** câu hỏi trong log; dựa vào grep C báo = 0, cộng việc đọc
     log thấy không có chuỗi tiếng Việt nào ngoài dòng khởi động.
   - Code: không ghi `query`, `answer`, nguồn, `chunk_id`, `response_id`, `str(exc)`.
4. **`getattr(generated, f, None)` — chấp nhận được, không che lỗi hành vi.**
   - Chỉ dùng cho 4 trường **số đo log** (`model`, token).
   - Đường phản hồi vẫn đọc thẳng `generated.text`: lỗi thật ở đó vẫn nổ như cũ.
   - Trong production, `GeneratedText` luôn có đủ 4 trường, nên `getattr` không bao giờ đổi giá trị thật.
   - Nó chỉ làm route **không đổi phản hồi** khi generator là đối tượng khác (test có sẵn `test_chat_returns_bracket_citations_when_model_writes_nguon_label`
     dùng đối tượng chỉ có `text`). Đây đúng yêu cầu m-4 "log không được đổi phản hồi", và cùng cách `EvidenceRecorder`.
   - Nếu sau này trường usage bị đổi tên trong production, log sẽ im lặng ra None. Cổng ổn định (token là số > 0) bắt được trường hợp này. Cân với
     `practical-project-coding` ("không fallback che lỗi"): đây không phải fallback cho hành vi người dùng, chỉ là chịu thiếu ở dữ liệu log ⇒ hợp lý.
   - Ghi chú ngoài phạm vi: test có sẵn kia dùng đối tượng thay generator, tức gần với "fake" mà luật dự án hạn chế. Có từ trước C60, không thuộc việc này.
5. **Test — đạt, khớp mốc.** B chạy lại (không key, liệt kê 3 file):

   | Lượt | Kết quả |
   |---|---|
   | nhánh `c59-log` | **32 passed / 4 errors** |
   | mốc `2ddd65d` | **31 passed / 4 errors** |

   4 errors giống hệt nhau, đều do thiếu key (C-17). +1 là test mới `test_chat_metrics_logged_when_retrieval_not_ready`. Thử ngược: xem m-1.
6. **Cổng ổn định — đạt** (dùng lại bằng chứng của C).
   - Dữ liệu cổng khớp report:
     - 2 dòng mới;
     - `outcome success`, `refusal` false / true;
     - token vào 869 / 1.332, ra 149 / 58, **suy luận 65 / 25** — provider có trả;
     - `n_cited_sources` 2 / 0;
     - `total_ms` 3.657,2 / 1.677,6 so client 3.662 / 1.679 ms.
   - Tiền (869 + 1.332) × 0,1 + (149 + 58) × 0,5 / 1M = **0,0003236 USD** ✓.
   - **Lý do không chạy lại cổng có phí:** code giữa lúc C chạy cổng và `cc70124` không đổi (`2270723` là commit code duy nhất, report là commit sau). Rủi ro
     chính (lọt nội dung, đổi phản hồi) đã kiểm bằng đọc dòng log thật + test + đọc code.
   - Khi merge vào `main`: cổng ổn định chạy lại một lần trên `main` sau merge, như luật cổng sau mỗi gói.
7. **Không đụng file của `gold-v2` — đạt.**
   - `c59-log` chạm `api/routes/chat.py`, `llm/generator_openai_full_corpus.py`, `tests/test_api_chat.py` + report riêng.
   - `gold-v2` chạm `experiments/phase_8_1/g1_retrieval.py`, `tests/test_gold_coverage.py` + report riêng.
   - Không giao nhau ⇒ merge theo thứ tự nào cũng không xung đột file.
   - `c59-log` gốc `2ddd65d`, `main` nay `a872c59`. Các commit `main` sau `2ddd65d` chỉ chạm tài liệu / governance, không chạm 3 file code này (B kiểm:
     `git diff --name-only 2ddd65d main -- backend` rỗng).

## 4. Cách người kiểm chạy lại thật (0 USD)

```bash
git worktree add --detach /tmp/b_c59rev origin/c59-log      # + symlink data/, knowledge-base-hue/
cd /tmp/b_c59rev/backend
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_api_chat.py tests/test_openai_full_corpus_generator.py tests/test_phase6_live_smoke.py -q -p no:cacheprovider
git checkout --detach 2ddd65d   # mốc, cùng lệnh pytest
# thử ngược (đã trả code về): metrics["query"] = query sau build (xanh — m-1) / ở đầu _answer (đỏ)
```

## 5. Giới hạn

- Không chạy lại cổng có phí (lý do §3.6). Không chạy được đường 500 / 409 / `generation_failed` / `citation_integrity_error` thật (đọc code).
- Không grep được câu hỏi của cổng (không lưu), nên dựa vào grep C báo + đọc log.

## 6. Decision

**ready_for_user_confirmation.** A merge `c59-log` (rồi `gold-v2`) vào `main` + cổng ổn định trên `main`. m-1 ghi ở hồ sơ; m-2 tùy C.
