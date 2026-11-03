# Review: Phase 9 B3 (nhánh `p9-b3`, B136)

## B3b `a3dabba..7a76ba2` (nhánh `p9-b3b`, B138 + B141 — C154 · 19:18 03/11/2026 `date`)

Người kiểm: C (Claude Opus 5.5) — viết bộ đo B3 + B3b, chạy phần kín B3 (C146) và bộ mới B3b (C152); không code. Đối chiếu plan B3 bản 2 `cd099ec0a00e` §4 (Q1–Q8, "Kết quả âm") + luật A cho B3b (README bộ B3b `58dd7910eeb9` §3) + report
`b138_b3b_implementation.md` `eb5ad5e14906` §1, §3, §5, §5c. `risk-gated-agent-review`. 0 USD. Worktree riêng `/tmp/c_p9b3b` (detach `7a76ba2`, gỡ khi xong). Ca dò private `data/phase_9/c154_review/`.

### 1. Cổng tối thiểu

| Cổng | Kết quả |
|---|---|
| Git | `origin/p9-b3b` = `7a76ba2`; 3 commit trên `a3dabba` (`1ed7b34` câu dặn · `57f0e0b` chỉ nhớ câu hỏi · `7a76ba2` bật nhớ) |
| Đường dẫn đổi | `backend/llm/full_corpus_prompt.py` (+1 câu trong `ASSISTANT_HISTORY_NOTE`), `backend/config/settings.yaml` (2 cờ), `backend/tests/test_b3_memory.py` (test không-cookie tắt cờ tường minh) — khớp report §1 |
| `git diff --check` | sạch |
| sha | `ASSISTANT_HISTORY_NOTE` `64e347d5df58`, `ANSWER_SYSTEM_INSTRUCTIONS` `81d3040cf53f`, `ROUTER_HISTORY_NOTE` `62f8197730ad` (C tính từ code ở `57f0e0b`); `settings.yaml` `7a76ba2` `31a7c369485e` — khớp |
| Ngoài phạm vi | không |

### 2. Kiểm theo rủi ro

| Điểm | Cách kiểm (C) | Kết quả |
|---|---|---|
| **Đi đúng đường ghi trước, không "chạy lại tìm lần đạt"** | thư mục dữ liệu: `data/phase_9/b3b/sau/` (câu dặn, 1 lượt) và `sau_a/` (chỉ nhớ câu hỏi, 1 lượt); plan B3 §4 "Kết quả âm: Q3 / Q4 không đạt ⇒ `nho_cau_tra_loi: false` ⇒ đo lại Q3–Q6 trên đã thấy (1 lượt)" | lượt 1 Q4 không đạt ⇒ (a) đúng đường ghi trước, mỗi cấu hình **một** lượt. **Đạt** |
| **Q4 (a) — số quyết** | **tính lại từ điểm thô** `sau_a/judge/scores_*.jsonl` bằng script C (khác script B; chạy trên bộ đã thấy B3 cho ra đúng số B3 trước đó) | +0,80, CI 95 % [+0,25; +1,50], 6 / 14 / 0 — **khớp** report §5 |
| Bộ mới (S1 / S2) | C chạy (C152), B không mở | S1 0 / 6, S2 nho 0 / 19 ↔ doc_lap 5 / 19 — khớp §5c |
| **Chỉ nhớ câu hỏi — đường code** | đọc `conversations.py:77` (lưu câu trả lời rỗng khi `keep_answers` tắt), `with_history` (bỏ tin assistant rỗng), `app.py:124` (API dựng kho với `keep_answers=flags.nho_cau_tra_loi`); **ca dò khác cách** `do_mac_dinh.py`: app **mặc định** (đọc `settings.yaml` nhánh), generator giả, 2 lượt qua cookie | kho có, `keep_answers` False; lượt 1 lịch sử `()` và chuỗi gửi như B2 (bất biến Q1); lượt 2 nhận đúng câu hỏi lượt 1, câu trả lời rỗng; chuỗi tin = `[user, user]` (không tin trợ lý rỗng). **Đạt** |
| Bật cờ (`7a76ba2`) | đọc diff; tìm test khác dùng app mặc định (`create_app()` không tham số): chỉ `test_b3_memory.py` | test "không cookie" giờ tắt cờ tường minh — đúng; không test khác lệ thuộc mặc định cũ |
| Test | `test_b3_memory` `test_b2_tool_loop` `test_api_chat` `test_static_ui` `test_phase6_settings` ở `7a76ba2` (có `--env-file`, bản build mới) | **41 / 41** |
| **Cổng B141** | đọc file thô `cong_b141/*.h`, `exit.txt`, `ui.json` + log server `/tmp/b_p9b3b` sau `log_mark.txt` | cookie `HttpOnly; Max-Age=1800; Path=/api; SameSite=strict`; chuỗi c1–c3 cùng một mã, "cuộc mới" ⇒ mã mới dùng lại ở c4; curl exit 0 cả 5; **8 dòng log = 8 lượt**, `n_history_turns` 0-1-2 · 0 · 0 · 0-1-0; mã cuộc trong log **0**. Khớp §5c |

Bất biến đã kiểm: lượt không lịch sử gửi model đúng chuỗi như trước (Q1); nhớ tắt ⇒ không cookie (test B + vòng sớm 2).

### 3. Findings

**0 blocker · 0 major · 1 minor.**

- **m-4 — câu "ngoài kho" của cổng thực ra là câu ngoài phạm vi.** Log dòng thứ 5 của cổng: tuyến `ngoai_pham_vi`, `outcome` `out_of_scope` (câu cố định của code), trong khi report §5c ghi "câu ngoài kho … ⇒ câu từ chối chuẩn". Đường **từ chối của kho khi nhớ bật** không được cổng chạm (đã có bằng chứng qua harness cùng lõi: C152 6 / 6 lượt thiếu từ chối chuẩn; Q5 đã thấy 0 / 0). Tác động: thấp. Đóng khi report ghi đúng "ngoài phạm vi"; không cần chạy lại.

Ghi nhận (không phải finding — giới hạn đã ghi ở report §5c): ca dò tự viết không tái hiện K-N2; bộ mới chưa có ca "bác tiền đề bằng đúng nguồn"; không nhớ câu trả lời ⇒ câu "ý thứ hai bạn vừa nói…" chưa hỗ trợ.

### 4. Kết luận

**ready_for_user_confirmation** — dải `a3dabba..7a76ba2` (nhớ **bật**, chỉ nhớ câu hỏi) đủ để A merge; m-4 sửa chữ report (không chặn).

**Kiểm m-4 (19:19 03/11/2026 `date`):** report B138 `05714acd9fc9` §5c ghi đúng "câu ngoài phạm vi … tuyến `ngoai_pham_vi`, câu cố định (outcome `out_of_scope`)"; chữ cũ "câu ngoài kho đơn lẻ" không còn. **m-4 đóng.**

## Vòng sớm 2 `10ec9a2..b156f92` (C147 · 18:24 03/11/2026 `date`)

Người kiểm: C (Claude Opus 5.5) — viết bộ đo B3, chạy + chấm phần kín (C146), không code B3. Đối chiếu plan B3 **bản 2 `cd099ec0a00e`** (D1, D2, D8, D9 (b) (c), §4 Q10) + report
`b136_b3_implementation.md` §2b, §4b, §4c. `risk-gated-agent-review`. 0 USD. Worktree riêng `/tmp/c_p9b3` (detach, chỉ chạy test / build; gỡ khi xong). Ca dò (private): `data/phase_9/c147_review/`.
Phần mới so vòng sớm 1: `cb73e19` (m-1 / m-2), `46008ed` (D6 bản hẹp), `291b459` (bước 8 giao diện), `b156f92` (câu gợi ý lễ hội).

### 1. Cổng tối thiểu

| Cổng | Kết quả |
|---|---|
| Git | `origin/p9-b3` = `b156f92`; 5 commit trên `10ec9a2`; backend chỉ đổi tới `46008ed`, sau đó chỉ `frontend/src/` (4 file) |
| Đường dẫn đổi `10ec9a2..b156f92` | 11 file backend (như report §2) + `frontend/src/{App.jsx, index.css, markdown.js, stream.js}`; `package.json` / `package-lock.json` / `index.html` **không đổi** ⇒ 0 gói npm mới |
| `git diff --check` | sạch (cả dải) |
| Đọc exact diff | `cb73e19`, `46008ed`, `291b459`, `b156f92` — đọc hết |
| Ngoài phạm vi | không thấy; `settings.yaml` vẫn `nho_hoi_thoai: false` (`c18aa9872a6f`) |

### 2. Kiểm theo rủi ro

| Điểm | Cách kiểm (C) | Kết quả |
|---|---|---|
| **m-1 (vòng 1) — test kiểm tên rỗng** | đọc diff test | câu hỏi lượt 1 giờ có tên ⇒ phép kiểm "tên không vào log" có nghĩa. **Đóng** |
| **m-2 (vòng 1) — lượt lỗi không gửi cookie** | đọc `chat.py`; **ca dò khác cách** `do_cookie_loi.py`: generator chưa sẵn (502) hai lượt liên tiếp có cookie jar, câu rỗng (422), nhớ tắt trên `/api/chat/stream` | lượt lỗi có cookie; lượt 2 dùng **cùng** mã (kho 1 cuộc — không cuộc mồ côi); 422 không cookie, không tạo cuộc; nhớ tắt ⇒ không cookie. **Đóng** |
| **D6 bản hẹp** (`46008ed`) | so chữ với report §4 / A quyết | đúng một câu trong `ANSWER_SYSTEM_INSTRUCTIONS`, khớp chữ A quyết; số Q2 vòng 2 ở report (không chạy lại — ngoài phạm vi vòng này) |
| **D9 (c) số hiển thị 1..k** | **ca dò khác cách** `do_so_hien_thi.mjs` (node, gọi thẳng `displayNumbers`; B kiểm bằng Playwright trên câu thật): dạng `[Nguồn n]`, hoa thường + khoảng trắng, mã trong chữ không có trong `sources`, nguồn trích không thấy trong chữ, id chuỗi, 0 nguồn | **6 / 6**. Đọc code: `data-cite` giữ **số gốc** (bất biến: code kiểm trích dẫn / log / judge dùng số gốc), chỉ chữ hiện là số hiển thị; trước sự kiện `sources` số gốc mờ, không bấm được (yêu cầu 9 giữ) |
| D9 (b) thứ tự nhãn | đọc `newTurn` + `ket_qua_ui.json` `status_sequences` | lượt mới mở bằng "Đang hiểu câu hỏi…" rồi tìm ⇒ viết; khớp |
| D1 / D2 — server giữ lịch sử, lượt lỗi không nhớ | đọc `App.jsx`: trang không gửi lịch sử; "Thử lại" thay lượt lỗi; "Cuộc trò chuyện mới" gọi server **trước** rồi mới xoá màn hình | khớp plan |
| Câu khẩn cấp | đọc: `stream.js` chuyển `done` (có `outcome`); backend `StreamEvents.done` gửi `outcome` = `emergency` cho câu cố định | thẻ riêng, chữ thường (React tự thoát ký tự), không qua `innerHTML` |
| An toàn chữ / CSP | đọc: chữ trả lời vẫn qua `DOMPurify` + đổi trích dẫn trên nút chữ sau bộ lọc (không ghép chuỗi HTML); build lại ở `b156f92` | `dist/index.html` 1 `<script>` module ngoài file, 0 `style=` inline; CSS / JS 0 URL `http(s)://`; `test_static_ui.py` **3 / 3**; Playwright của B: CSP vi phạm 0, request ra ngoài 0 (`ket_qua_ui.json`, `q10_ui.json` — C đọc file thô) |
| **Q10** | đọc file thô B: `q10/curl_out/*.h`, `exit.txt`, log server `/tmp/b_p9b3/backend/logs/application.log` sau mốc `log_mark.txt` | cookie `HttpOnly; Max-Age=1800; Path=/api; SameSite=strict` ở mọi phản hồi; chuỗi A cùng một mã, sau "cuộc mới" mã khác và được dùng lại; ca ngắt `curl` exit 28; log **11 dòng = 11 lượt**, `n_history_turns` 0-1-2 / 0 / 0-1(ngắt, `client_disconnected`)-1-2 / 0-1-0 ⇒ **lượt bị ngắt không được nhớ**; mã cuộc trong log **0**. Khớp report §4c |
| Test | `pytest test_b3_memory.py test_b2_tool_loop.py test_static_ui.py test_api_chat.py` không khoá; test cần khoá chạy riêng có `--env-file` (chỉ dựng app) | **36 / 36** (35 + 1) |

Bất biến đã kiểm: nhớ **tắt** ⇒ không cookie, không lịch sử (cả `/api/chat/stream`); số trích dẫn gốc không đổi ở tầng máy.

### 3. Findings

**0 blocker · 0 major · 1 minor.**

- **m-3 — report cần cập nhật sau quyết định phần kín.** `b136_b3_implementation.md` §1 ghi "bật sau giao diện" và §2b ghi dải `46008ed..291b459`. Sau C146 + A quyết (sàn Q5 kín phạm ⇒ cờ nhớ **không bật**), §1 / §6 cần ghi: cờ giữ `false` khi merge, lý do (số đếm, không chép chữ kín), dải code cuối `..b156f92`. Đóng khi report sửa.

Ghi nhận (không phải finding): logic D9 (c) không có test được theo dõi (dự án không có bộ test JS; thêm bộ test = thêm gói npm) — Playwright của B + ca dò của C là bằng chứng một lần. Giới hạn A đã giữ: cookie hết hạn 30 phút khi màn hình còn lượt cũ thì server âm thầm bắt đầu cuộc mới (report §6).

### 4. Giới hạn

- Không chạy lại lượt có phí của B (Q2, chuỗi đã thấy, Q10); Q10 kiểm bằng file thô + log server thật của B. Không tự chạy Playwright (ảnh / đo giao diện là của B; C đọc kết quả JSON, không xem ảnh).
- Không đo latency.

### 5. Kết luận vòng sớm 2

**Code `10ec9a2..b156f92` không có finding chặn** để merge với `nho_hoi_thoai: false` (plan §5 bước 7). Quyết định chất lượng B3: phần kín (C146) — nhớ tên, hỏi tiếp, đổi chủ đề, giữ cảnh báo đạt; **sàn ngoài kho kín phạm 1 / 2 lượt** (câu trả lời trích nguồn của đối tượng khác, dòng kho đúng không có trong ngữ cảnh) ⇒ A quyết cờ nhớ **không bật**; hướng tiếp A trình User. Còn trước merge: m-3; nếu B thêm commit thì C review phần thêm.

**Kiểm m-3 (18:26 03/11/2026 `date`):** report B136 `1c4459e8d80d` — dòng 5 ghi dải `10ec9a2..b156f92`; §1 cờ `false` giữ khi merge + lý do theo luật §4; §2b dải `46008ed..b156f92` (2 commit); §5b số đếm K-N2 + kết luận, không chép chữ kín (quét trùng 0); §6 "Merge với `nho_hoi_thoai: false`" — 1 / 2 kín, 1 / 6 cộng đã thấy (khớp số C: đã thấy 4 lượt ngoài kho, 0 bị trả lời). sha `KET_QUA_C146.md` trong §5b (`0be2f074fba3`) là bản lúc C gửi; bản hiện `7901ff994abb` chỉ thêm dòng ghi quyết định của A — không đổi số. **m-3 đóng.** Dải `10ec9a2..b156f92`: **ready_for_user_confirmation** để merge với cờ nhớ tắt (quyết định hướng B3 tiếp: User qua A).

## Vòng sớm `e69c293` (C145 · 12:20 03/11/2026 `date`)

Người kiểm: C (Claude Opus 5.5) — viết bộ đo B3 (C136), không code B3. Đối chiếu plan B3 **bản 2 `cd099ec0a00e`** (C142 vòng 2 ready). `risk-gated-agent-review`. 0 USD (B đang chạy Q2 có phí, không đo latency ⇒ C chỉ việc 0 USD, nhẹ).
Ca dò (private): `data/phase_9/c145_review/`.

### 1. Cổng tối thiểu

- `origin/p9-b3` = `e69c293` (1 commit trên `10ec9a2`), worktree `/tmp/b_p9b3`. 11 file, +569 / −54: `api/conversations.py` (mới), `api/routes/chat.py`, `api/app.py`, `llm/assistant.py`, `llm/generator_openai_full_corpus.py`,
  `llm/full_corpus_prompt.py`, `retrieval/full_corpus_context.py`, `evaluation/full_corpus_eval.py`, `config/settings.yaml`, `tests/test_b3_memory.py` (mới), `tests/test_b2_tool_loop.py` (sửa). Khớp plan §3; `frontend/` không sửa (bước 8 chờ User).
- `git diff --check` sạch. `settings.yaml`: `nho_hoi_thoai: false`, `nho_cau_tra_loi: true` (D7, D8).

### 2. Kiểm theo rủi ro (điểm A dặn)

| Điểm | Cách C kiểm (khác cách B) | Kết quả |
|---|---|---|
| **Q1** — nhớ tắt; khác B2 đúng câu D6 | `probe_q1.py` (`a0f56b6960c3`): bắt thân **HTTP** (httpx) mọi lần gọi OpenAI, cờ **mặc định** (nhớ tắt, `tim_them` bật), 32 an toàn + 10 smoke qua `answer_case`, trên nhánh và trên `main` (B2); chuẩn hoá = đọc JSON, bỏ `prompt_cache_key`, (tuỳ chọn) xoá đúng câu D6 trong mọi chuỗi | nhánh **bỏ câu D6 ⇒ 42 / 42 giống byte `main`**; giữ D6 ⇒ 0 / 42 ⇒ chỗ khác **duy nhất** là câu D6 (2 lần gọi / câu cả hai bên). **Đạt** |
| **Cookie + mã cuộc không vào log, không chứa tên** | `probe_mem.py` (`34d800e2e6eb`): `create_app()` thật (Qdrant chỉ đọc), generator giả, kho bật; **tên nằm trong câu hỏi** ("Mình tên là …"); grep **toàn bộ đầu ra màn hình + dòng mới của `application.log`** | 9 dòng log mới (3 `chat_metrics` = 3 lượt): tên **0**, mã cuộc **0**, chữ câu hỏi **0**. Mã cuộc = `secrets.token_urlsafe(16)` (không dẫn từ tên). Cookie HttpOnly / SameSite=Strict / Path=/api (test B). **Đạt** |
| **TTL / trần số cuộc dọn bộ nhớ thật** | đồng hồ giả: tạo 600 cuộc; vượt 30 phút | trần ⇒ còn **500**, cuộc cũ nhất bị bỏ, cuộc mới nhất còn; sau TTL cookie cũ ⇒ **mã mới**, kho chỉ còn **1** cuộc (mọi cuộc hết hạn bị dọn ở lần `ensure` kế). Hạn tính từ lượt cuối (`append`). **Đạt** |
| **Lịch sử không chứa kết quả công cụ / chữ kho; lượt lỗi không lưu** | `probe_mem.py`: lượt 1 thường, lượt 2 model ném `GenerationError` (502), lượt 3 hỏi tiếp | lượt 3 nhận **1** lượt lịch sử (lượt lỗi **không** có); lịch sử chỉ (câu hỏi, câu trả lời cuối), **không** chứa đoạn ngữ cảnh kho; mã `[1]` đã bỏ. Đọc code: `_remember` chỉ ghi `success / out_of_scope / emergency / refusal_no_sources / max_turns`; stream ghi ở `finally` sau dòng log, `client_disconnected` không ghi. **Đạt** |
| **D5 đếm token có lịch sử** | đọc `_token_count` (lịch sử + lời dặn trợ lý + `TOOL_PATH_OVERHEAD + ITEM_OVERHEAD × số mục`); **ước lại** hằng số từ `data/phase_9/b2_chay/pilot/b2b10.jsonl` (`viet_input_tokens − builder_tokens` theo số mục 1 / 3 / 5) | hồi quy C: **≈ 159 + 35,9 × mục**, sai lệch lớn nhất so công thức B (158 + 36 × mục) **15 token** ⇒ hằng số có nguồn, khớp. Lượt không lịch sử, đường sinh một lần: phép đếm như B1 (`instructions` None ⇒ không cộng đệm). Ghi nhận: tin lịch sử đếm không theo thứ tự xen kẽ (mọi câu hỏi rồi mọi câu trả lời) — **không** ảnh hưởng tổng token. **Đạt** (pilot B3 có lịch sử vẫn phải đo m-1 C142) |
| **Test B2 sửa đúng chủ đích** | đọc diff `test_b2_tool_loop.py` | (1) thứ tự: `generating` chỉ phát ngay trước chữ đầu ở đường công cụ (D9 (b), có chủ ý); chạm trần ⇒ không có `generating` (không có chữ model) — đúng; (2) ngân sách: so **chặt hơn** — bỏ phần đệm rồi so < 128 (trước < 512). **Không che lỗi** |
| D6 / D3 | đọc `full_corpus_prompt.py` | D6 = đúng một câu trong `ANSWER_SYSTEM_INSTRUCTIONS`; 2 câu dặn lịch sử (định tuyến, công cụ) chỉ ở bản agent dùng khi có lịch sử ⇒ lượt đầu như B2 |
| test chạm (không key) | `pytest test_b3_memory test_b2_tool_loop test_assistant test_assistant_boundary test_chat_stream` | **53 / 53** |

**Câu bất biến:** "Cờ nhớ tắt thì chuỗi gửi model = B2 + đúng câu D6; cờ nhớ bật thì log không bao giờ có tên / câu hỏi / mã cuộc." **Đúng** (42 / 42; 0 / 0 / 0).

### 3. Findings (vòng sớm)

**0 blocker · 0 major · 2 minor.**

- **m-1 — kiểm tên trong test B là rỗng.** `test_api_cookie_carries_history_and_new_conversation_clears_it` khẳng định `"Lan" not in m` nhưng **không câu hỏi nào trong test có chữ "Lan"** ⇒ phép kiểm luôn đúng dù code có lỗi.
  Hành vi thật đúng (ca dò C: tên trong câu hỏi ⇒ 0 trong log), nhưng test không bảo vệ được. **Đóng:** đưa tên vào câu hỏi lượt 1 (ví dụ "Mình tên là …") rồi giữ phép kiểm; nên kiểm cả dòng `chat_metrics` lẫn mọi bản ghi.
- **m-2 — lượt `/api/chat` lỗi không gửi cookie.** `chat()` chỉ `_set_cookie` khi kết quả không phải `JSONResponse` lỗi (`chat.py` ~dòng 130). Người dùng chưa có cookie mà lượt đầu lỗi (502 / 503) ⇒ server đã tạo cuộc (`ensure`) nhưng trình duyệt không nhận mã ⇒ một cuộc mồ côi mỗi lượt lỗi (bị chặn bởi trần 500 + TTL — không rò bộ nhớ vô hạn). Đường stream thì luôn đặt cookie. Không sai dữ liệu.
  **Đóng (chọn một):** đặt cookie cả ở phản hồi lỗi; hoặc tạo cuộc lúc `append` lần đầu thay vì ở `ensure`; hoặc ghi giới hạn này trong report.

### 4. Giới hạn

- Chưa có lượt có phí nào của B3 (Q2 đang chạy, Q3–Q8 chưa). Lịch sử có thật sự giúp model hiểu câu hỏi tiếp, nhớ tên, và token thật − builder có lịch sử: **review cuối**.
- Ca dò đường stream có lịch sử: chỉ đọc code + test B (`test_stream_tool_path_sends_generating_right_before_first_text`); chưa chạy uvicorn thật với cookie (Q10 của B).
- Q1: C kiểm 42 câu (B 228).

### 5. Kết luận vòng sớm

**Không có finding chặn** ở `e69c293`. m-1, m-2 sửa hoặc ghi lại trước review cuối. Review cuối: `e69c293..<cuối>` + bằng chứng có phí (Q2, pilot nhớ / Q8 token có lịch sử, Q3–Q7, phần kín C chạy, Q10 cổng).
