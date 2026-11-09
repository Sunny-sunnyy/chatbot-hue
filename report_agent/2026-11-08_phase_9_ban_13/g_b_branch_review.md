# Review: Phase 9 bậc G — phương án B (giữ 4 tuyến, `khan_cap` đi agent Huế) — nhánh `p9-g-b`

Decision: **`ready_for_user_confirmation`** cho `4df9427` (phần backend). Commit giao diện sắp có (gỡ `.emergency`) ⇒ E xem delta khi B báo sha cuối.
Người kiểm: E (Claude Code, `hue-rag-ea`) · 21:14 09/11/2026 (`date`) · B nhờ (A giao), mức nhẹ: một review cả nhánh.
Căn cứ: spec Phase 9 bản 13 §12.2 dòng G cột "Phương án B"; report B `b_g_cong_implementation.md` §0 + §4; bằng chứng `data/phase_9/g_cong/ket_qua/pab_r1.jsonl`.

## 1. Phạm vi đã review
- `git diff main...p9-g-b` (`main` `85cf473` → `4df9427`): 7 file — `assistant.py`, `settings.yaml`, xoá `llm/emergency.py` + `tests/test_emergency.py`, 3 test sửa. Đọc hết.
- `full_corpus_prompt.py` / `generator_openai_full_corpus.py` **không** trong diff ⇒ lời dặn định tuyến + lời dặn trả lời giống byte `main` (đúng spec: phương án B không đổi lời dặn).

## 2. Findings — không có blocker / major
- **m-1 (minor):** `api/routes/chat.py:118` `REMEMBERED_OUTCOMES` còn `"emergency"` — outcome này không còn sinh ra (mã chết, vô hại). Đóng: gỡ cùng commit giao diện.
- **m-2 (minor, B đã nói sẽ làm):** `frontend/src/chat.jsx:294-297` khối `turn.outcome === "emergency"` + CSS `.emergency` chết. Đóng: commit sắp có + build lại `frontend/dist`.
- **Ghi nhận rủi ro đã chấp nhận (không phải finding):** câu khẩn cấp nay là `tro_ly_hue` ⇒ agent từ chối ⇒ **cổng web B6 mở** (ca dò E: `web_gate_open` = True cho trace `route=tro_ly_hue, emergency_by="router"`, câu từ chối) ⇒ có mục "Từ web (chưa kiểm)"; câu thiên tai vẫn ra câu cố định NCHMF / 112 (B6). Khớp quyết định bạn 08/11 + 1 câu S2b B ghi (y tế ngoài phạm vi bị xếp `khan_cap`). **Với T2:** câu khẩn cấp có thể tự yêu cầu web như câu Huế ⇒ đếm riêng `emergency_by` khi đọc số T2.

## 3. Cách người kiểm chạy lại thật
- Worktree `/tmp/e_gb` (`4df9427`): `pytest tests/test_assistant.py tests/test_toc_do_song_song.py tests/test_b6_tra_web.py tests/test_api_chat.py tests/test_chat_stream.py` (không khoá).
- `git grep "EMERGENCY|is_emergency|emergency_rule|llm.emergency" -- backend frontend/src`.
- Ca dò (đường **khác** test của B — B kiểm `answer_turn` + #6; E kiểm stream **thường** `song_song_tra_loi=False`): `/tmp/e_g_probe/probe_b.py`, SDK thật + client giả, Qdrant thật chỉ đọc.

## 4. Kết quả quan sát
- pytest: **131 passed**, 1 error = test cần `OPENAI_API_KEY` (bẫy đã biết).
- grep: chỉ còn m-1, m-2 + chú thích lịch sử.
- Ca dò stream thường, định tuyến trả `khan_cap`: `route = tro_ly_hue`, `emergency_by = router`, `fixed_outcome = None`, sự kiện `status` ×3 rồi `delta` (đi agent Huế, không câu soạn sẵn).
- **Bất biến đã kiểm:** `ngoai_pham_vi` vẫn ra câu cố định, không gọi model trả lời (test B `test_router_out_of_scope_skips_answer_model` + #6 `test_other_route_discards_everything_of_the_early_answer` đạt); `_merge_spec.keep_own` giữ `emergency_by` của trace chính (đọc code `assistant.py:1136`).
- Đơn giản: một nhánh `if` đổi nhãn tuyến, gỡ cờ + module chết; không thêm cờ / lớp mới.

## 5. Giới hạn
- Không chạy lượt có phí; số sàn (S2 0 · S3 0 · S3b 0 · lỗi citation 0 / 92 câu) là của B (`pab_r1.jsonl`), E không chạy lại.
- Chưa xem commit giao diện (chưa có).

## 6. Decision
`ready_for_user_confirmation` (backend). Khi B báo sha cuối: E xem delta giao diện + m-1 ⇒ đóng.

## 7. Delta `4df9427` → `2deec02` (sha cuối, B báo) — 21:19 09/11/2026

- `git diff 4df9427 2deec02`: 3 file, +2 / −8 — đúng m-1 (`REMEMBERED_OUTCOMES` bỏ "emergency") và m-2 (`chat.jsx` bỏ khối + điều kiện `.emergency`, `index.css` bỏ 2 rule). `git diff --check` sạch; `git grep emergency` trong `frontend/src` = 0.
- Dùng lại bằng chứng của B cho phần chạy (build giao diện, test rộng 842, server thật 3 câu) — delta chỉ gỡ mã chết, không đổi đường dữ liệu.
- **m-1, m-2 đóng.** Decision cuối: **`ready_for_user_confirmation`** cho `2deec02`.
