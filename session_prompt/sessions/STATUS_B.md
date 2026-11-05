# STATUS B — 11:46 05/11/2026 (sổ tay ≤ 30 dòng; kết quả nằm ở report — luật A 05/11 commit `1d1fa77`)

Vai: thực thi. Phiên mở theo `session_prompt/START_SESSION.md`; việc lấy ở `CURRENT_HANDOFF.md`. Tên terminal đổi mỗi lần mở ⇒ `ListAgents`.
Phiên tối 05/11 (mở 19:16): B `hue-rag-4b` · A `hue-rag-4f` · C `hue-rag-3c` · E `hue-rag-bc`. Quyền (User 19:18 05/11/2026): việc A giao = "làm đi"; hết hạn cuối phiên.
Lúc mở: B163 đã có `p9-sua-lich` `1c53627` (16:49, đã push, cờ tắt, chưa đo, chưa report); worktree `/tmp/b_sualich` mất ⇒ prune + add lại khi làm tiếp.

## Đang làm
- **B164 (A giao 19:19 05/11/2026) = B163 phần 0 USD** — worktree `/tmp/b_sualich` (`p9-sua-lich` `1c53627`). File B sửa: `report_agent/2026-11-02_phase_9_code/b163_sua_lich_implementation.md` (mới), file này. Xong: 72 test thuần; `xep` nhánh ↔ main giống 12.528 / 12.528. **Sau C192 (19:50): Q1 228/228 giống byte, Q1m 228/228, 165 test passed, build xong** ⇒ phần 0 USD B164 XONG; chờ `lich_trinh` bật cho lượt có phí. Report `b163_sua_lich_implementation.md`.
- **B166 XONG (20:26 05/11/2026, report b163 §7):** `p9-sua-lich` rebase lên `main` `80faf1a` + sửa hết điểm thay `6543f82`; 202 test, build, mô phỏng đã thấy 10/10, Q1 / Q1m 228/228.
- **B165 (A giao tối 05/11) = code B6 tra web phần 0 USD** — plan bản 3 `6e5c3b21065d`; nhánh `p9-b6` từ `main` `2693422`, worktree `/tmp/b_b6`. File B sửa (nhánh): `backend/llm/tra_web.py` (mới), `backend/llm/assistant.py`, `backend/llm/generator_openai_full_corpus.py`, `backend/llm/full_corpus_prompt.py`, `backend/api/conversations.py`, `backend/api/routes/chat.py`, `backend/config/settings.yaml`, `frontend/src/markdown.js`, `frontend/src/App.jsx`, `backend/api/app.py`, `backend/tests/test_assistant_boundary.py`, `backend/tests/test_b6_tra_web.py` (mới); report `report_agent/2026-11-02_phase_9_code/b165_b6_implementation.md`. **Phần 0 USD XONG (19:54):** `7873e0f` + sửa `d7ec216` (cờ #6), 51 test B6 + 216 cùng file chạm, build, Q1 / Q1m 228/228. Probe Serper ĐẠT (≤ 0,001 USD). Harness `data/phase_9/b6/tools/` (`app_web.py`, `chay_b6.py`, `cham_b6.py`) chạy thử 0 USD xong (server khoá giả + OpenAI trỏ cổng đóng). Đã thấy ×2: Q3 8/10 đạt, Q2 code 0, Q2 judge phạm (X04, X05) ⇒ vòng 1 code `cedac73` (A quyết) ⇒ chạy lại judge 0/7 đạt; Q1/Q1m 228/228. KHOÁ `cedac73`. Q4 ĐẠT (từ chối nhầm 0, S-OOS 0/11), Q8 ĐẠT (API + Playwright, CSP 0). Tiền B6 ≈ 0,144 / 0,22. Rebase lên `main` `b75fefc` ⇒ `9140152` (push), 251 test, build, Q1 228/228. Còn: kín (C203) ⇒ review (E).
- **Review plan B6 bản 2** (19:29 05/11/2026): changes_requested 0 / 1 / 5 — `docs/superpowers/plans/2026-11-05-phase-9-b6-plan_review.md` `96f198855a9d`. Vòng 2 (19:33): **ready** trên bản 3 `6e5c3b21065d` (review `7bb1c21aff9c`) ⇒ A duyệt.
- **B160 = B5 `lich_trinh`** — nhánh `p9-b5` **`5bc45cf`** (khoá `908e93b` + B5.1 + sửa C191 vòng 1, push), worktree `/tmp/b_b5` (symlink `data/`, `knowledge-base-hue/`). Report **`report_agent/2026-11-02_phase_9_code/b160_b5_implementation.md`**.
  Mọi sàn B đo được đạt (Q1, Q1m, đã thấy v2, chuỗi v2, Q4 + S-AT, Q8 cổng 2 lượt + Playwright). Kín (C, khoá 908e93b): Q2a 5/5, đạt theo nội dung (A); rút nhầm 1/5 ⇒ B5.1 sửa, đã thấy 13 chạy lại sạch. **Chờ:** User chấm Q3 ⇒ C review ⇒ A merge.
  Tiền B5 (B) ≈ 0,0997 (+ kín C 0,0046) / 0,15. Dữ liệu `data/phase_9/b5/`; harness `data/phase_9/b5/tools/` (`chay_b5.py`, `chuoi_b5.py`, `q8_b5.py`, `app_lich.py`).
- **B161** review c172 tốc độ #6 ⇒ ready + điều kiện merge M-1 (`c172_review.md`); Rebase + M-1 xong: nhánh **`p9-toc-do-6b`** `e3e235b` (từ `p9-b5` `5bc45cf`, worktree `/tmp/b_toc6`; `p9-toc-do-6` của C giữ nguyên) — test #6 10 passed, Q1 cờ tắt / bật 228/228 (`data/phase_9/toc_do/b161_rebase/`). Chờ C kiểm; cờ bật lúc merge (User duyệt).
- **B162 = B5c `tinh_tien`** — nhánh `p9-b5c` **`42bdd93`** (từ `p9-b5` `5bc45cf`, worktree `/tmp/b_b5c`). Phần 0 USD xong: test 160, Q1 228/228, Q1m 228/228, đáp án C 8/8. Report `report_agent/2026-11-02_phase_9_code/b162_b5c_implementation.md`. Rebase lên main `ae5a6d6` ⇒ `ae1bb63`, Q1/Q1m 228/228 lại. **B5c ÂM ở Q4 (luật ghi trước):** Golden F2 1 câu (giá vé biểu diễn ngoài bảng — luật trình bày làm model bỏ giá kho) + S-AT câu miễn giảm vé 1/3 ↔ 0/3. Đã thấy 14×2 + chuỗi 7×2 đạt. **B5c-2 cũng ÂM** (khoá `7821d34`): Q1/Q1m′ đạt, đã thấy đạt, Golden sạch, nhưng S-AT câu miễn vé trẻ nhỏ 3/3 ↔ 1/3. Tiền tổng ≈ 0,128 / 0,14. Chờ A.
- Đã xong phiên này (chi tiết ở report / file review): B156 B4 âm, B157 B4b âm (`b144_b4_implementation.md` §2f §2g); B158 review spec Phase 10; B159 review plan B5c; rà over-engineering `data/ra_soat_over_engineering_2026-11-05/B.md`.

- **Trước merge (A báo tối 05/11):** `main` có `p10-anh` `2ca9937` (chạm `app.py`, `settings.yaml`, `test_assistant_boundary.py`, `App.jsx`) ⇒ `p9-sua-lich` + `p9-b6` rebase lên `main` mới + chạy lại Q1 (+ test + build) lúc tới bước merge.

## Lệnh hay dùng (từ `/tmp/b_b5/backend`, luôn `PYTHONPATH=$PWD HF_HUB_OFFLINE=1`)
- Có phí: `uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env python <tool> …`; 0 USD bỏ `--env-file`.
- An toàn 32: `sinh_an_toan.py <out> <side> <round> [--qids …] [--lich-trinh|--moc]` ⇒ `DO_CUOI_DIR=<thư mục> an_toan_b2.py export|check|accept|compare --judge k [--round regen]`.
  `compare --round regen` chỉ đếm sai điều kiện; thiếu cảnh báo đếm riêng bằng `by_src` (xem `data/phase_9/b5/q4/an_toan/sat_thieu_regen.json`).
- Server thật cờ bật: `uvicorn --factory --app-dir data/phase_9/b5/tools app_lich:make_app --port 8765` (run_in_background, TaskStop khi xong); log `backend/logs/application.log`.

## Bẫy — đọc trước khi làm
- Push từ worktree bị auto mode chặn ⇒ push từ working tree chính. Máy khởi động lại ⇒ worktree `/tmp` mất: `git worktree prune` + `add` + symlink lại.
- Script `data/…/tools/*.py` chạy từ `backend/` cần `PYTHONPATH=$PWD`. `--out` của harness là FILE; harness không ghi đè lượt thật.
- Brief judge phải ghi rõ khoá đầu ra (item id). Judge sub-agent: một lô một file `labels_*`, chạy tiếp được.
- Playwright: `wait_for_function` bị CSP chặn ⇒ chờ bằng vòng `page.evaluate`. Kiểm hành vi trên uvicorn thật, không TestClient.
- `pgrep -f "<mẫu>"` khớp chính lệnh chờ ⇒ dùng `pgrep -f "[u]vicorn …"`; chờ dài ⇒ `run_in_background`, không `sleep`.
- Kiểm giống byte khi nhiều lần gọi model / lượt: lấy lần bắt cuối (trả lời).
- Heredoc `<<'EOF'`; `rm`/`cp` đường dẫn tuyệt đối; worktree có symlink ⇒ `unlink` rồi `git worktree remove` (không `--force`).
- Giờ ghi file luôn lấy từ `date`. Không bao giờ gọi `agy`. Câu kín B không mở.
- Lịch sử sổ tay cũ: `git show HEAD:session_prompt/sessions/STATUS_B.md` (trước bản này).
