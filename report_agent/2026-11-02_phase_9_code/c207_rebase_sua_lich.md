# C207 — rebase `p9-sua-lich` lên `main` mới + Q1 + test (0 USD)

Người làm: C (Claude Code, Opus 5.5) · 11:00 06/11/2026 (`date`) · A giao sáng 06/11 (`CURRENT_HANDOFF.md` mục "PHIÊN 06/11", dòng C).
Plan gốc của nhánh: `docs/superpowers/plans/2026-11-05-phase-9-sua-lich-plan.md` bản 3 `5b68f3cb666a`. Code: B (B163 + B166), report `b163_sua_lich_implementation.md`.

## 1. Việc

`p9-sua-lich` `6543f82` đứng sau `main` 25 commit (trong đó merge B6 tra web: `assistant.py`, `chat.py`, `settings.yaml`… đổi) ⇒ rebase lên `main` `0a9e0f3`, kiểm lại cờ tắt / cờ bật bằng Q1 / Q1m, chạy test + build, rồi chạy thử 0 USD các công cụ đo đã có. Không đổi hành vi nào của nhánh.

## 2. Rebase

- Worktree `/tmp/c_sualich`, nhánh tạm `c207-rebase` (từ `6543f82`) — không đụng ref `p9-sua-lich` tới khi A cho push.
- **Xung đột 3 file, đều "hai bên cùng thêm":** `chat.py` (danh sách trường log: B6 thêm trường web, nhánh thêm trường sửa lịch; lời gọi `answer_turn_stream_parallel` ở đường stream: ghép thành `_model_query(..., _flags(state).bang_lich)` **và** đối số `_tim_web(state)`), `settings.yaml` (cờ `tra_web` + `tra_web_timeout_seconds` của `main` + cờ `sua_lich: false` của nhánh), `assistant.py` (import `tra_web` + `sua_lich`; cờ `tra_web` + `sua_lich`; kiểm cờ trong `__post_init__`). Giữ cả hai phía, không sửa dòng nào khác.
- Các file git tự ghép (`generator_openai_full_corpus.py`, `full_corpus_prompt.py`, `App.jsx`, `conversations.py`): đọc lại diff với `main` — chỉ phần của nhánh (công cụ `sua_lich_fn`, `SUA_LICH_MO_TA`, thẻ chọn).
- **`git range-diff`:** commit B166 giống hệt (`6543f82` = `09ddaf9`); commit B163 chỉ khác dòng ngữ cảnh do `main` thêm (B6) — mọi dòng `+` của nhánh không đổi.
- **Kết quả:** `5c2d486` (B163) · **`09ddaf9`** (B166) trên `main` `0a9e0f3`.

## 3. Kiểm [Chạy]

| Kiểm | Lệnh (từ `backend/` của cây cần đo) | Kết quả |
|---|---|---|
| **Q1** cờ tắt ⇒ chuỗi gửi model giống byte `main` | `env -u OPENAI_API_KEY OPENAI_API_KEY=capture-only HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag python ../data/phase_9/b2_chay/tools/capture_all.py <out>` ở `main` `0a9e0f3` và ở nhánh | **228 / 228 giống byte**, sha `dba1f578eef1` cả hai (`data/phase_9/sua_lich/q1_c207/main_0a9e0f3.jsonl`, `nhanh_09ddaf9.jsonl`) |
| **Q1m** `lich_trinh` bật: `sua_lich` bật ↔ tắt | `…/capture_flags.py <out> lich_trinh=1 sua_lich=<0|1>` (bản sao settings, chạy `capture_all.py` nguyên; script tạm `/tmp/c207_tools/`, thay `/tmp/b164/capture_flags.py` đã mất khi máy khởi động lại) | **228 / 228 giống byte**, sha `ac53ea9046f3` cả hai (`q1m_lich1_sua{0,1}.jsonl`) — khác `main` đúng như mong đợi (có mục công cụ `lich_trinh`); sha trùng lần đo B166 hôm qua |
| Test (không khoá) | `HF_HUB_OFFLINE=1 uv run --project … python -m pytest -q tests/test_sua_lich.py test_b5_lich_trinh.py test_b2_tool_loop.py test_b3_memory.py test_toc_do_song_song.py test_assistant.py test_chat_stream.py test_assistant_boundary.py test_feedback.py test_b6_tra_web.py` | **239 passed** |
| Build giao diện + test tĩnh | `cd frontend && npm ci && npm run build`; `pytest tests/test_static_ui.py` | build xong (JS 319,29 kB); **3 passed** |
| Mô phỏng 0 USD (hành động nhãn ⇒ `ap_hanh_dong` thật) | `PYTHONPATH=$PWD HF_HUB_OFFLINE=1 uv run --project … python ../data/phase_9/sua_lich/tools/mo_phong.py` | **10 / 10 ok** (bộ đã thấy) |
| Kiểm bộ | `… python ../data/phase_9/bo_do_sua_lich/tools/kiem_bo.py --pha` | **OK**, ca phá **6 / 6** |

Ghi chú Q1: không nạp `.env` (khoá giả) ⇒ cổng tra web B6 (đang bật trong `settings.yaml`) không có khoá Serper, không mở kết nối nào; giống nhau ở hai bên nên so byte vẫn đúng. 0 USD.

Không chạy: `test_api_chat.py`, `test_openai_full_corpus_generator.py` (cần khoá — `Project_Status.md` §8); bộ kín (không cần ở bước này; chạy kín qua User `!` trên khoá ở plan bước 5).

## 4. Push

`git push --force-with-lease=p9-sua-lich:6543f82 origin c207-rebase:p9-sua-lich` (A cho phép 06/11): **`6543f82` → `09ddaf9`** — đã push (`+ 6543f82...09ddaf9 (forced update)`); ref cục bộ `p9-sua-lich` = `origin/p9-sua-lich` = `09ddaf9`; worktree `/tmp/c_sualich` nay giữ nhánh `p9-sua-lich` (gỡ trước khi session khác cần chuyển sang nhánh này); nhánh tạm `c207-rebase` đã xoá.

## 5. Chạy thử lượt có phí (WORKFLOW §4 (4b)) — phát hiện thiếu công cụ

- Công cụ đã có cho lượt đo sửa lịch đều 0 USD và đã chạy đạt ở §3 (`mo_phong.py`, `kiem_bo.py`); `mo_phong_kin.py` (bộ kín) chỉ chạy qua User `!` ở bước 5.
- **Chưa có harness lượt có phí** cho plan bước 3–5: không có script nào gửi chuỗi nhiều lượt (cookie cuộc, lượt bấm nút `sua_chon`) tới server thật với `lich_trinh` + `sua_lich` bật, ghi khung trước / sau mỗi lượt và chấm Q2 (a)–(i) / Q3 pass^2 theo nhãn. Script tạm của B (`/tmp/b164/`) đã mất và chỉ gồm bắt chuỗi gửi (Q1 / Q1m). ⇒ Báo A; đề xuất C viết harness + bộ chấm (0 USD, chạy thử bằng khoá giả + OpenAI trỏ cổng đóng như B5b `app_thoi_tiet.py`) trong lúc chờ B5 bật.

## 6. Trạng thái

- Nhánh `p9-sua-lich` = `09ddaf9` trên `main` `0a9e0f3` (sau push). Cờ `sua_lich: false`.
- Tiền C207: **0 USD**.
- Còn (không đổi): lượt có phí chờ `lich_trinh` bật (B5 — bộ kín mới đang làm); trước lượt đó rebase lại nếu `main` đổi code + Q1.
