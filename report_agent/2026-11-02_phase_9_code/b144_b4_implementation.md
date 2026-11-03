# Implementation Report: Phase 9 B4 — hỏi lại (`hoi_lai`) — **dở: code + test 0 USD xong; chưa lượt đo có phí (chờ B143 merge)**

Người làm: B (Claude Opus 5.5, `hue-rag-32`) · việc **B144** (A giao) · bản này 21:10 03/11/2026 (`date`). Plan: `docs/superpowers/plans/2026-11-03-phase-9-b4-plan.md` bản 2 **`42fa62d2425f`** (A duyệt; Lệch Q6 chấp nhận; Q-a giữ + đo hỏi thừa; Q-b không trả lời tạm).
Nhánh **`p9-b4`** từ `main` `849005c`, worktree `/tmp/b_b4`. Commit (sau rebase lên `main` `ac46c96` — có B143 `e3cdb96`, 21:13 03/11/2026): **`c4f2b76`** (backend + test), **`86c311b`** (giao diện); trước rebase `18da59b`, `10d57c1`. Đã push (`--force-with-lease`, nhánh riêng chưa review). **Chưa merge, cờ `hoi_lai` tắt.** B4 không chạm `ROUTER_INSTRUCTIONS`.
Report tracked, repo public: không chép câu bộ đo; câu ví dụ tự viết. Dữ liệu: `data/phase_9/b4/` (private). B không mở `cau_sealed.jsonl`.

## 1. Đã làm (theo D1–D10)

| File | Thay đổi |
|---|---|
| `backend/llm/hoi_lai.py` (mới) | D2 bảng trường / giá trị / bắt buộc (khớp C143 + plan B5); D3 `loc_truong` (bỏ trường sai loại, rỗng ⇒ bắt buộc "dien", > 3 ⇒ cắt "cat"); D8 `the_hoi_lai` (dữ liệu nút + `bat_buoc`); D4 `TruongInput` (`Literal`, `extra="forbid"`) + `ghep_cau` (nhãn code, tất định; `{}` ⇒ câu gốc) |
| `backend/llm/generator_openai_full_corpus.py` | `_assistant_for(…, hoi_lai_fn)`: công cụ thứ hai `hoi_lai` + `StopAtTools(["hoi_lai"])` + lời dặn có `HOI_LAI_NOTE`; `_tools_result`: `final_output` là dict công cụ trả ⇒ `GeneratedText.clarify` (đọc **trước** khi ép `AnswerOutput`, spec §3) — thường + stream; `assistant_instructions_for(history, hoi_lai)` (ngân sách đếm đúng chuỗi) |
| `backend/llm/assistant.py` | cờ `hoi_lai`; trace `da_co_truong`, `search_query` (m-3: lần tìm đầu = câu gốc), `clarify`, `hoi_lai_raw` (tham số thô — Q2, M-1), `hoi_lai_d3`; `hoi_lai_for_turn`; chỉ đưa công cụ khi cờ bật **và** lượt chưa có trường (D4: không hỏi lại lần hai); `_finish_generated` ⇒ `outcome="hoi_lai"`, không chữ, không kiểm citation; stream không phát "đang tìm" cho `hoi_lai` |
| `backend/llm/full_corpus_prompt.py` | `HOI_LAI_NOTE` (khi nào gọi + Cách A cho câu chi phí — D7), chỉ ghép khi cờ bật |
| `backend/api/routes/chat.py` | `ChatRequest.truong`; `_model_query` (câu ghép, `co_truong`); `/api/chat` trả `clarify` (answer rỗng, không `turn_id`); stream: sự kiện `clarify` + `done` (không `turn_id`); lượt hỏi được nhớ "chỉ câu hỏi" (D5); log `hoi_lai` {loai, n, d3}, `co_truong` (số, không giá trị) |
| `backend/config/settings.yaml` | `assistant.hoi_lai: false` |
| `frontend/src/App.jsx`, `stream.js`, `index.css` | D10 thẻ hỏi lại: nhóm nút / trường (chọn một, bỏ chọn được), "(không bắt buộc)", "Gửi" chỉ bật khi đủ bắt buộc, "Trả lời luôn" (`truong: {}`); lượt ghép hiện câu gốc + "· 2 ngày · 2 người"; Thử lại giữ lựa chọn; khung nguồn ghi "Chọn thêm thông tin…" |
| `backend/tests/test_b4_hoi_lai.py` (mới, 8 test) | D3, D4; **SDK thật + client giả có kịch bản** (không mạng): dừng ngay ở `hoi_lai` (1 lần gọi), công cụ + lời dặn gửi đi, `clarify` sau D3, tham số thô; stream không "đang tìm", không `delta`; cờ tắt / lượt đã có trường ⇒ chỉ `tim_kho`, lời dặn = B3 (Q1 mức test); route `clarify` ⇒ `truong` ⇒ câu ghép tới model, không `hoi_lai`; 422 giá trị / trường lạ; log số đếm; sự kiện `clarify` |

**Lệch plan:** harness đo đặt ở `data/phase_9/b4/tools/chay_b4.py` (private, như harness định tuyến C156) thay vì lệnh mới trong `backend/evaluation/full_corpus_eval.py` (plan §3) — ít code tracked hơn, đủ cho Q2 / Q3 / Q6; ghi tham số thô + sau D3 (M-1). Lệnh `kiem` / `dem` chạy thử 0 USD (W36 4b): đọc đúng `chon_da_thay.json` C158 (`060d62a56e97`, khoá `chon`), `dem` trên kết quả giả ở `/tmp` (kiểm logic, đã xoá).

## 2. Đã chạy (0 USD)

- Test: `test_b4_hoi_lai` + `test_b3_memory` + `test_b2_tool_loop` + `test_api_chat` + `test_chat_stream` + `test_feedback` + `test_assistant_boundary` ⇒ **66 passed** (+ `test_b4` thêm 1 sau đó), 1 error = test cần khoá API (bẫy đã biết); `test_static_ui` 3 / 3; `npm ci && npm run build`.
- **Q1 (byte, `capture_all.py` B134 — thay `AsyncResponses.create`, không gọi mạng; 176 Golden + 32 an toàn + smoke = 228 ca × 2 lần gọi):** lần 1 (nhánh trước rebase ↔ cây `main`) khác ở **lần định tuyến 228 / 228**, lần trả lời giống 228 / 228 ⇒ nguyên nhân: A merge B143 vào `main` trong lúc chạy (`ROUTER_INSTRUCTIONS` main `164bd4a254e9` ↔ nhánh `fb4e1aa7f8fe`), không phải B4. Sau rebase: **giống byte 228 / 228** (`data/phase_9/b4/q1/main.jsonl` ↔ `b4_rebase_co_tat.jsonl`, `cmp`) ⇒ **Q1 PASS** — cờ tắt, chuỗi gửi model như `main`.

## 2b. Pilot + Q2 / Q3 đã thấy (B145, A giao tối 03/11; 21:39 03/11/2026) — **chưa khoá, chưa kín**

Harness `data/phase_9/b4/tools/chay_b4.py` (cờ `hoi_lai` bật ở rìa trên bản sao cờ, nhớ tắt, định tuyến theo settings), commit nhánh lúc chạy: pilot + v0 trên `86c311b`, v1 trên cây có ghi chú vòng 1 (commit sau đó `c76934c`; phần sửa m-1 chỉ chạm đường stream, harness đi đường thường). Không đo latency.

| Lượt | Ghi chú `HOI_LAI_NOTE` | Q2 thiếu hỏi đúng (tham số thô) | Q3 câu đủ bị hỏi | gần giống bị hỏi | hỏi thừa · D3 điền / cắt | USD |
|---|---|---|---|---|---|---|
| pilot 4 câu (2 thiếu · 1 đủ · 1 gần giống) | bản code `c4f2b76` | 2 / 2 | **1 / 1** (LD1 — hỏi thêm 2 trường không bắt buộc) | 0 / 1 | — · 0 / 0 | 0,0016 |
| **v0** 20 câu | như trên | **9 / 10** (trượt LT4) | **0 / 7** | 0 / 3 | 0 · 0 / 0 | 0,0124 |
| **v1** 20 câu (vòng chỉnh 1: "câu đã đủ bắt buộc thì không gọi hoi_lai chỉ để hỏi trường không bắt buộc", sha `2b62c390f2fa`) | `c76934c` | **9 / 10** (trượt LT4) | **1 / 7** (CD4) | 0 / 3 | 0 · 0 / 0 | 0,0115 |

- Ngưỡng plan: Q2 ≥ 8 / 10 — **đạt cả hai lượt**; Q3 ≤ 1 / 10 (7 đã thấy + 3 kín) — v0 0 / 7, v1 1 / 7 (còn 0 suất cho phần kín nếu giữ v1).
- **Câu đủ bị hỏi chập chờn:** LD1 bị hỏi ở pilot, không bị hỏi ở v0 / v1; CD4 không bị ở v0, bị ở v1 ⇒ vòng chỉnh 1 **không cho thấy cải thiện rõ** (quan sát trên 1 lượt mỗi bản; chưa đo A/A). Đề xuất phiên sau: đo lại v0 ↔ v1 trên 7 câu đủ × 2–3 lượt trước khi chọn bản khoá.
- LT4 (lịch trình theo sở thích ẩm thực, thiếu số ngày): model **trả lời luôn** bằng mẹo ăn uống có nguồn (3 nguồn), không hỏi — trượt Q2 nhưng không nói sai.
- Tiền B145: **0,0256 USD** (ước pilot 0,002 — đúng; mỗi lượt 20 câu ≈ 0,012, cao hơn ước 0,008 / lượt của plan — câu đủ / gần giống có lượt viết). B4 tới giờ ≈ 0,026 / 0,12.

**Review sớm C163** (`b144_review.md` "Vòng sớm" `1ccb676f475d`, 0B / 0M / 3m) — A quyết:
- **m-1** stream phát "đã tìm" cho lần gọi `hoi_lai` ⇒ **sửa xong `c76934c`** (bỏ cả `searching` lẫn `searched` khi công cụ là `hoi_lai`; test mới hỏng khi bỏ phần sửa, đạt khi có).
- **m-2** model chỉ hỏi trường không bắt buộc ⇒ câu lịch trình thiếu `so_ngay` vẫn đi tiếp ⇒ **sửa ở phiên sau**: D3 thêm "code luôn thêm trường bắt buộc còn thiếu (theo `loai`) vào thẻ" ⇒ **plan bản 3** (chỉ D3 + chỗ đổi), C kiểm, A duyệt sha lại. Q2 vẫn đếm trên tham số thô (M-1).
- **m-3** đệm token chưa đếm lược đồ công cụ `hoi_lai` ⇒ báo `usage − builder` max ⇒ **chưa có số**: harness `chay_b4.py` chưa ghi `usage_tru_builder` ⇒ phiên sau thêm trường này (như harness `chuoi` B3) rồi báo max ở lượt đã thấy.

## 3. Còn lại (PHIÊN SAU — thứ tự)

1. ~~Chờ B143 merge ⇒ rebase ⇒ Q1~~ **xong** (§2).
2. ~~Pilot~~ xong (§2b). **Plan bản 3** (D3: code thêm trường bắt buộc còn thiếu — C163 m-2) ⇒ C kiểm ⇒ A duyệt sha; harness ghi `usage − builder` (m-3); đo lại câu đủ v0 ↔ v1 × 2–3 lượt ⇒ chọn bản ghi chú.
3. **Q2 + Q3** 20 câu đã thấy ⇒ ≤ 3 vòng chỉnh `HOI_LAI_NOTE` ⇒ **khoá** (sha ghi chú + `settings.yaml` + commit) ⇒ Q4 (bộ tuyến, nhãn `can_hoi_lai.json` C158 `ef9179c8f266`), Q5 (mẫu 30 + an toàn 32, ngoài nhãn), Q6 (`--chon`, judge an toàn 2 sub-agent + regex tổng), Q7 (4 chuỗi tự viết, nhớ bật).
4. C chạy kín 10 câu ⇒ Q2 / Q3 kín.
5. **Q8 cổng** + Playwright thẻ hỏi lại (laptop + điện thoại, CSP) ⇒ report ⇒ C review ⇒ A merge (cờ theo kết quả).
