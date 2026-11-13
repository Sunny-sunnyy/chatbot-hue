# Review: bật cờ "hết lượt tìm thì dừng" (`assistant.het_luot_bo_cong_cu: true`) — commit `9d6a0f7`

Decision: **ready_for_user_confirmation** (0 blocker · 0 major · 2 minor)
Người kiểm: C (`hue-rag-eb`, Claude Code) — người làm: A
Date: 20:11 13/11/2026 (`date`)
Canonical guide: plan `docs/superpowers/plans/2026-11-12-het-luot-tim-plan.md` · `report_agent/2026-11-12_ra_khoang_cach/b_het_luot_tim_implementation.md` + `_review.md`
Implementation report: tin của A + thân commit `9d6a0f7`

## 1. Phạm vi đã review

`main` cục bộ: `9d6a0f7` trên `d5ea552`, chưa push. Diff đúng 4 file / 5 dòng (`git show --stat`): `settings.yaml` cờ `false ⇒ true` + chú thích; `test_het_luot_tim.py` bỏ khẳng định "settings thật = false" (giữ khẳng định mặc định dataclass = False); 2 bộ sinh giả trong `test_api_chat.py`, `test_b3_memory.py` nhận `**_cong_cu`. Không có thay đổi ngoài phạm vi; `git diff --check` sạch.

## 2. Findings

Không có blocker / major.

- **m-1** — `session_prompt/Project_Status.md` dòng 129 (và báo cáo khâu `bao_cao_he_thong/07_…`) còn ghi "cờ `het_luot_bo_cong_cu: false`". Đóng: A sửa lúc đóng đợt / kết phiên (luật mức nhẹ cho phép), ghi giờ bật + "User: bật kèm theo dõi".
- **m-2** — `evaluation generate` không `--flags` đọc `settings.yaml` (`AssistantFlags.from_settings`) ⇒ từ commit này mọi lượt đo trợ lý mặc định **có** cờ (kể cả lượt B7 cuối). Đúng ý "đo cái đang chạy", nhưng so với B7 giữa kỳ (cờ tắt) là đổi một thứ ⇒ plan B7 cuối nên ghi một dòng. Đóng: một dòng trong plan / handoff B7.

## 3. Cách người kiểm chạy lại thật

- `git show --stat 9d6a0f7`, `git show 9d6a0f7`, `git diff --check 9d6a0f7~1 9d6a0f7`.
- Ca dò khác cách người làm: (1) `git diff --stat cd1f6ef 9d6a0f7 -- backend/llm backend/api backend/core backend/retrieval` ⇒ **rỗng**: code lõi của cờ không đổi từ lúc merge nhánh đã đo 12/11 ⇒ số đo 12/11 (8 / 8 câu kho thiếu bớt ≥ 1 lượt gọi; trung vị 22,85 ⇒ 16,15 s; 0 / 6 bịa ở 3 câu chạm chỗ bớt từ chối) **dùng lại được** cho phần A chưa chạy lại (câu chạm đúng ngưỡng 2 lần tìm trên server thật) — dùng lại, không gọi là lần chạy mới. (2) `git grep` mọi nơi gọi `generate_with_tools(` / `start_tools_stream(` ngoài test ⇒ chỉ 2 chỗ trong `assistant.py` (đường thường + stream), đều truyền `**extra` có `con_luot_fn`; mọi bộ sinh giả trong test đã nhận `**kwargs` ⇒ không còn bộ giả nào gãy khi cờ bật. (3) Probe 0 USD: `AssistantFlags.from_settings(load_settings())` ⇒ `het_luot_bo_cong_cu = True`, `tim_them = True` (cờ cần `tim_them`).
- `cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_het_luot_tim.py tests/test_b3_memory.py -q` (không key) ⇒ **20 passed, 30,7 s**. Không chạy lại cả suite / `test_api_chat.py` có key (A: 873 passed có key, 288 s; 3 file chạm cờ 99 / 99 có + không key — không kiểm lại).

## 4. Kết quả quan sát

- Bất biến kiểm: cờ tắt (mặc định dataclass) ⇒ `assistant.py:762` không truyền `con_luot_fn` ⇒ chuỗi gửi model như trước — code không đổi từ `cd1f6ef` (228 / 228 giống byte đo lúc merge), test khoá mặc định False còn. Cờ bật đi cả đường thường lẫn stream; model xin công cụ đã ẩn ⇒ `xin_cong_cu_da_an` ⇒ câu từ chối cố định, không lỗi 500.
- Theo dõi User yêu cầu: khi cờ cắt công cụ, `trace.tools` ghi mục `"het_luot": true` ⇒ đếm được trên trường `tools` của dòng `chat_metrics` (log không chứa chữ câu hỏi — A đã kiểm).
- Lượt biểu mẫu "Lên kế hoạch" không bị cờ chạm (test `test_form_turn_is_unchanged_by_the_flag` bật / tắt giống byte — nằm trong 20 passed).

## 5. Giới hạn hoặc phần chưa chạy

Không chạy server thật / lượt có phí (A đã chạy 2 câu, 0,0016 USD); câu chạm đúng ngưỡng 2 lần tìm trên `main` dựa vào số đo 12/11 dùng lại (lý do ở mục 3).

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation`: A push `9d6a0f7` khi đã báo User; sửa m-1 lúc đóng đợt; ghi m-2 vào plan B7 cuối. Theo dõi: đếm `het_luot` trong `chat_metrics` sau mỗi phiên dùng thật.
