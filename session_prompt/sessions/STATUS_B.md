# STATUS B — 11:46 05/11/2026 (sổ tay ≤ 30 dòng; kết quả nằm ở report — luật A 05/11 commit `1d1fa77`)

Vai: thực thi. Phiên mở theo `session_prompt/START_SESSION.md`; việc lấy ở `CURRENT_HANDOFF.md`. Tên terminal đổi mỗi lần mở ⇒ `ListAgents`.
Phiên 05/11: B `hue-rag-48` · A `hue-rag-b0` · C `hue-rag-52`. Quyền (User 08:51 05/11): việc A giao = "làm đi"; hết hạn cuối phiên.

## Đang làm
- **B160 = B5 `lich_trinh`** — nhánh `p9-b5` **`5bc45cf`** (khoá `908e93b` + B5.1 + sửa C191 vòng 1, push), worktree `/tmp/b_b5` (symlink `data/`, `knowledge-base-hue/`). Report **`report_agent/2026-11-02_phase_9_code/b160_b5_implementation.md`**.
  Mọi sàn B đo được đạt (Q1, Q1m, đã thấy v2, chuỗi v2, Q4 + S-AT, Q8 cổng 2 lượt + Playwright). Kín (C, khoá 908e93b): Q2a 5/5, đạt theo nội dung (A); rút nhầm 1/5 ⇒ B5.1 sửa, đã thấy 13 chạy lại sạch. **Chờ:** User chấm Q3 ⇒ C review ⇒ A merge.
  Tiền B5 (B) ≈ 0,0997 (+ kín C 0,0046) / 0,15. Dữ liệu `data/phase_9/b5/`; harness `data/phase_9/b5/tools/` (`chay_b5.py`, `chuoi_b5.py`, `q8_b5.py`, `app_lich.py`).
- **B161** review c172 tốc độ #6 ⇒ ready + điều kiện merge M-1 (`c172_review.md`); Rebase + M-1 xong: nhánh **`p9-toc-do-6b`** `e3e235b` (từ `p9-b5` `5bc45cf`, worktree `/tmp/b_toc6`; `p9-toc-do-6` của C giữ nguyên) — test #6 10 passed, Q1 cờ tắt / bật 228/228 (`data/phase_9/toc_do/b161_rebase/`). Chờ C kiểm; cờ bật lúc merge (User duyệt).
- **B162 = B5c `tinh_tien`** — nhánh `p9-b5c` **`42bdd93`** (từ `p9-b5` `5bc45cf`, worktree `/tmp/b_b5c`). Phần 0 USD xong: test 160, Q1 228/228, Q1m 228/228, đáp án C 8/8. Report `report_agent/2026-11-02_phase_9_code/b162_b5c_implementation.md`. **Lượt có phí chỉ sau B5 merge** (rebase lên main + Q1/Q1m lại). Harness `data/phase_9/b5c/tools/`.
- Đã xong phiên này (chi tiết ở report / file review): B156 B4 âm, B157 B4b âm (`b144_b4_implementation.md` §2f §2g); B158 review spec Phase 10; B159 review plan B5c; rà over-engineering `data/ra_soat_over_engineering_2026-11-05/B.md`.

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
