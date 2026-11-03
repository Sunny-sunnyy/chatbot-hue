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

## 3. Còn lại (PHIÊN SAU — thứ tự)

1. ~~Chờ B143 merge ⇒ rebase ⇒ Q1~~ **xong** (§2).
2. **Pilot 4 câu đã thấy** (2 thiếu / 1 đủ / 1 gần giống) ⇒ ước lại tiền (trần B4 0,12, dừng > 0,11).
3. **Q2 + Q3** 20 câu đã thấy ⇒ ≤ 3 vòng chỉnh `HOI_LAI_NOTE` ⇒ **khoá** (sha ghi chú + `settings.yaml` + commit) ⇒ Q4 (bộ tuyến, nhãn `can_hoi_lai.json` C158 `ef9179c8f266`), Q5 (mẫu 30 + an toàn 32, ngoài nhãn), Q6 (`--chon`, judge an toàn 2 sub-agent + regex tổng), Q7 (4 chuỗi tự viết, nhớ bật).
4. C chạy kín 10 câu ⇒ Q2 / Q3 kín.
5. **Q8 cổng** + Playwright thẻ hỏi lại (laptop + điện thoại, CSP) ⇒ report ⇒ C review ⇒ A merge (cờ theo kết quả).
