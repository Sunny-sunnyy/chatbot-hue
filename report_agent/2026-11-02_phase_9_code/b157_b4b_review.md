# Review: Phase 9 B4b — nhánh `p9-b4` `990825e` để merge với cờ `hoi_lai: false` (C183)

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 2 minor)
Người kiểm: C (Claude Opus 5.5, `hue-rag-52`)
Date: 10:17 05/11/2026 (`date`)
Canonical guide: plan B4 bản 8 `69afbb2732cf`; User chọn 10:07 05/11/2026 "Merge cờ tắt + code tự hỏi" (`CURRENT_HANDOFF.md`)
Implementation report: `report_agent/2026-11-02_phase_9_code/b144_b4_implementation.md` (§2e–§2g)

Phạm vi A giao: **chỉ phần cờ tắt** — Q1 giống byte, code chết / phạm vi, test, giao diện khi cờ tắt không hiện thẻ. Không review lại kết quả đo cờ bật (B4b âm ở Q5 S-AT — report §2g). Skill `risk-gated-agent-review`. 0 USD.

## 1. Phạm vi đã review

- **Git:** `p9-b4` = `origin/p9-b4` = `990825e`; 7 commit trên `main` (`e6caa83` … `990825e`). `main` hiện `114bbe6` — từ `cafb1b6` chỉ đổi tài liệu (`git diff --stat cafb1b6 main -- backend frontend` rỗng). `git merge-tree --write-tree main 990825e`: **không xung đột**.
- **Đường đổi** (`git diff --stat main...990825e`, 11 file, +425 / −42): `backend/api/routes/chat.py`, `backend/config/settings.yaml`, `backend/llm/{assistant,full_corpus_prompt,generator_openai_full_corpus,hoi_lai}.py`, `backend/retrieval/full_corpus_context.py`, `backend/tests/test_b4_hoi_lai.py`, `frontend/src/{App.jsx,index.css,stream.js}`. Không file untracked trên nhánh. `git diff --check main...990825e`: sạch.
- **Đọc exact diff** cả 11 file, theo câu hỏi "cờ tắt thì khác `main` ở đâu".

## 2. Findings

Không có blocker hoặc major.

| Mã | Mức | Vị trí | Bằng chứng | Tác động | Tiêu chí đóng |
|---|---|---|---|---|---|
| m-1 | minor | `chat.py` `ChatRequest.truong` + `_model_query` (không gắn cờ) | Ca dò C (0 USD, Pydantic + hàm route trong tiến trình): trên `990825e` cờ tắt, `ChatRequest(query, truong={})` **được nhận**; `truong={"so_ngay": "2"}` ⇒ `_model_query` trả **câu ghép** (`co_truong` 1). Trên `main` `114bbe6` cùng yêu cầu ⇒ **422** (`extra="forbid"`). `truong={"so_nguoi": …}` ⇒ 422 trên B4b (D2′ đúng) | **Hợp đồng API khác `main` khi cờ tắt**, chỉ với yêu cầu tự soạn có `truong`: giao diện chỉ gửi `truong` từ thẻ, mà thẻ chỉ có khi có sự kiện `clarify` ⇒ từ giao diện không tới được khi cờ tắt. Chữ ghép chỉ là nhãn cố định của code ⇒ không mở đường chữ tự do. **Có lợi cho B5** (plan B5 bản 7 D15 dùng lại đường này khi `hoi_lai` tắt) | report B4b ghi một dòng "đường `truong` / câu ghép không gắn cờ `hoi_lai` — cố ý, B5 dùng lại" + một test route "cờ tắt + `truong` ⇒ 200, câu ghép" (khoá hành vi để B5 không vỡ). Không cần sửa code |
| m-2 | minor | `assistant.py` `hoi_lai_for_turn`, `_offer_hoi_lai`; `generator_openai_full_corpus.py` nhánh `StopAtTools`; `full_corpus_prompt.HOI_LAI_NOTE`; `full_corpus_context.HOI_LAI_TOOL_OVERHEAD`; `hoi_lai.loc_truong`; trường trace `hoi_lai_raw` / `hoi_lai_d3` / `hoi_lai_offered` | 13 chỗ tham chiếu ngoài test chỉ chạy khi cờ bật. User chọn **không** dùng công cụ `hoi_lai` nữa (B5 code tự hỏi — plan B5 bản 7 D15) ⇒ phần **công cụ** `hoi_lai` thành code chết lâu dài. Phần **dùng lại**: `the_hoi_lai`, `TruongInput`, `ghep_cau`, `clarify` (route + stream + giao diện), `_tools_result` (rẽ khi `final_output` là dict có `loai`) | `Session_Prompt.md` §7 (không giữ code không phục vụ hành vi thật). Gỡ ngay trước merge sẽ đổi chính diff đã đo; giữ sau cờ là hướng User chọn ("merge cờ tắt") | report B4b ghi danh sách phần "chỉ cờ bật, không dùng nữa"; **B5 gỡ** phần công cụ `hoi_lai` / `HOI_LAI_NOTE` / `HOI_LAI_TOOL_OVERHEAD` / `loc_truong` khi D15 thay (lịch sử giữ bằng tag `hoso/p9-b4`), hoặc A ghi lý do giữ |

**Câu hỏi độ đơn giản:** phần dùng lại (`clarify`, nút, câu ghép) phục vụ hành vi thật của B5 ⇒ hợp lý; phần công cụ `hoi_lai` không còn hành vi nào dùng ⇒ m-2.

## 3. Cách người kiểm chạy lại thật

1. **Q1 — chạy lại độc lập** (không dùng file của B): worktree `/tmp/c_b4k` detach `990825e` (`settings.yaml` `37b9ab1beb37`, `hoi_lai: false`); từ `backend/`: `env -u OPENAI_API_KEY OPENAI_API_KEY=capture-only HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag python ../data/phase_9/b2_chay/tools/capture_all.py /tmp/c183_q1_990825e.jsonl` (không gọi mạng) ⇒ `cmp` với `data/phase_9/b4/q1/main_cafb1b6.jsonl`.
2. **Test:** `HF_HUB_OFFLINE=1 uv run --project … python -m pytest tests/test_b4_hoi_lai.py tests/test_assistant.py tests/test_assistant_boundary.py tests/test_b2_tool_loop.py tests/test_b3_memory.py tests/test_chat_stream.py tests/test_emergency.py tests/test_feedback.py -q` trên `990825e`.
3. **Ca dò khác cách** (script tạm `/tmp`, đã xoá): trong tiến trình, trên `990825e` và trên `main`: `ChatRequest` với `truong`, `_model_query`, `AssistantFlags.from_settings` + `_offer_hoi_lai` khi cờ tắt.
4. **Đọc diff giao diện** (`App.jsx`, `stream.js`): điều kiện hiện thẻ, thân yêu cầu gửi đi.

## 4. Kết quả quan sát

- **Q1 (fresh):** **228 / 228 giống byte `main`** (`cmp` 0 khác; 228 dòng, mỗi dòng 2 lần bắt) — cũng giống file của B `b4b_990825e_co_tat.jsonl`. `main_cafb1b6` vẫn đại diện `main` `114bbe6` vì backend / frontend không đổi từ `cafb1b6`.
- **Test (fresh):** **83 passed** (8 file chạm).
- **Câu bất biến — "cờ tắt ⇒ lượt trợ lý như `main`":** `AssistantFlags.hoi_lai` = `False` từ settings; `_offer_hoi_lai` = `False` ⇒ `_assistant_instructions(…, False)` gọi y như B3 (không `HOI_LAI_NOTE`); `_assistant_for(…, hoi_lai_fn=None)` ⇒ chỉ công cụ `tim_kho`, không `StopAtTools`; `extra_tool_tokens` = 0 ⇒ phép đếm ngân sách như cũ; `trace.search_query` chỉ đặt khi có `truong` ⇒ lần tìm đầu bằng câu gốc như cũ; stream: `asking` chỉ đúng khi tên công cụ là `hoi_lai` ⇒ `searching` / `searched` như cũ; `_tools_result` chỉ rẽ khi `final_output` là dict có `loai` (không xảy ra khi không có `hoi_lai`); `if trace.answer:` trước `delta` của câu cố định — `max_turns` có chữ ⇒ như cũ; `REMEMBERED_OUTCOMES` thêm `hoi_lai` — không xảy ra khi cờ tắt. ⇒ **giữ** (khớp Q1).
- **Giao diện khi cờ tắt:** `ClarifyCard` chỉ vẽ khi `turn.phase === "done" && turn.clarify`; `clarify` chỉ đặt từ sự kiện SSE `clarify`, server chỉ phát khi `trace.clarify` có (chỉ từ công cụ `hoi_lai`) ⇒ **không hiện thẻ**. `streamAnswer` gửi `{ query }` khi `truong === null` (mọi câu gõ) ⇒ thân yêu cầu **giống `main`**; `summary` rỗng ⇒ tiêu đề lượt không thêm chữ; bảng nguồn chỉ đổi chữ khi `turn.clarify`.
- **Ca dò:** xác nhận m-1 (bảng trên).
- **Dùng lại bằng chứng (không phải chạy mới):** build giao diện + CSP 0 + Playwright thẻ (B, Q8 §2f) — đường cờ tắt không vẽ thẻ nên không chạy lại Playwright; kín B4b (C180) và Q5 (B) ngoài phạm vi cờ tắt.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy server thật / cổng ổn định (`/`, `/health`, 1 câu trong + 1 ngoài kho, đếm `chat_metrics`) trên `990825e` cờ tắt — cổng là bước A làm lúc merge (`CURRENT_HANDOFF.md` "Cổng ổn định"); Q1 giống byte + 83 test là bằng chứng chính cho "không đổi".
- Không chạy `npm ci && npm run build` trên nhánh (dùng lại Q8 của B); test cần khoá OpenAI (`test_api_chat.py` …) không chạy.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** — merge `p9-b4` `990825e` với `hoi_lai: false` được (User đã chọn hướng). Hai minor không chặn: m-1 ghi + khoá bằng test (B5 dùng đường `truong`); m-2 ghi danh sách code chỉ cờ bật + gỡ ở B5. Trước merge: A chạy cổng ổn định (server thật, cờ tắt) + 5 chỗ báo cáo.
