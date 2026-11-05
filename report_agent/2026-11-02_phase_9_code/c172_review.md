# Review: Phase 9 — thí nghiệm tốc độ #6 (chạy lần trả lời song song với định tuyến)

Decision: **ready_for_user_confirmation** cho kết quả thí nghiệm (đạt) — kèm **điều kiện merge M-1** (đóng khi rebase lên `main` có B4b / B5)
Người kiểm: B (Claude Opus 5.5, `hue-rag-48`) · việc B161 (A giao)
Date: 11:51 05/11/2026 (`date`)
Canonical guide: `docs/superpowers/plans/2026-11-04-phase-9-toc-do-song-song-plan.md` bản 2 `093d548445a3` (sha khớp)
Implementation report: `report_agent/2026-11-02_phase_9_code/c172_toc_do_song_song.md` `43f501cb37da` (sha khớp)

## 1. Phạm vi đã review

- Git: nhánh `p9-toc-do-6` = `ea081b0` (local = origin), 1 commit trên `main` `ebd8965` ⇒ khớp report. Đổi 4 file (`backend/llm/assistant.py` +83, `backend/api/routes/chat.py` +9 / −3, `backend/config/settings.yaml` +1, `backend/tests/test_toc_do_song_song.py` mới); không file ngoài phạm vi; `git diff --check` sạch.
- Đọc exact diff: `answer_turn_stream_parallel`, `_merge_spec`, 3 trường trace, route stream, log; đọc thêm `_pick_route` + `answer_turn_stream` (phần tuyến có sẵn, phần đọc nốt khi huỷ) trên nhánh.
- Dữ liệu private `data/phase_9/toc_do/thi_nghiem_6/` (chấm lại 0 USD), log `log_bien.log`.

## 2. Findings

**0 blocker · 1 major (điều kiện merge, không chặn kết quả thí nghiệm) · 0 minor.**

**M-1 (major — đóng khi rebase).** `assistant.py` `answer_turn_stream_parallel`: trace phụ dựng mới `AnswerTrace(history=trace.history)` — chỉ mang `history`. Trên `main` hiện tại (B4b `b019aab`) route đặt sẵn trên trace **trước** khi gọi lõi: `search_query`, `da_co_truong` (`chat.py` `_model_query`); B5 (`p9-b5`, chưa merge) thêm `truong`. Sau rebase, cờ #6 bật:
  (a) lượt bấm nút (có trường) ⇒ lần tìm đầu đi bằng **câu ghép** thay vì câu gốc ⇒ yêu cầu gửi model khác cờ tắt (phạm Q1 "cờ bật giống byte cờ tắt");
  (b) B5 "Trả lời luôn" (`truong: {}`) ⇒ trace phụ có `truong = None` ⇒ code coi như thiếu số ngày ⇒ **hỏi lại lần hai** (phạm sàn TL của B5);
  (c) `_merge_spec` chép mọi trường trừ `keep_own` ⇒ ghi đè `truong` / `search_query` của trace chính bằng `None` (log `co_truong`, thẻ "Sửa" sai).
  Bằng chứng: đọc code [Code, chưa chạy — nhánh chưa có các trường này nên không chạy được ca dò]. Q1 của report (228 yêu cầu trên `ebd8965`) không có lượt có trường ⇒ "rebase + chạy lại Q1 + test" như report §Giới hạn **không bắt được** lỗi này.
  **Tiêu chí đóng:** trace phụ nhận đủ mọi trường đầu vào route đặt trước khi gọi lõi (cách đơn giản: chép trace chính lúc bắt đầu, vd `dataclasses.replace(trace)`, rồi `keep_own` giữ cả các trường đó) + test trên nhánh đã rebase, cờ #6 bật: (1) `truong={"so_ngay": "2"}` ⇒ yêu cầu gửi model giống byte cờ #6 tắt; (2) B5 `truong={}` ⇒ 0 thẻ hỏi lại, lịch 1 ngày tạm; (3) trace chính sau gộp còn đúng `truong` / `search_query`; + Q1 chạy lại có thêm vài lượt stream có trường.

Câu hỏi độ đơn giản: hàng đợi + task huỷ là cách trực tiếp nhất để "chạy trước, giữ sự kiện tới khi có tuyến"; dùng lại nguyên `answer_turn_stream` cho phần chạy trước (không viết đường thứ hai) — hợp lý, không thêm trừu tượng.

## 3. Cách người kiểm chạy lại thật (0 USD)

- Worktree riêng `/tmp/b_rv6` (detached `ea081b0`, symlink `data/`, `knowledge-base-hue/`), từ `backend/`: `HF_HUB_OFFLINE=1 PYTHONPATH=$PWD uv run --project /home/minhhieu/hue_rag pytest -q tests/test_toc_do_song_song.py <ca dò B>` (Qdrant thật chỉ đọc, e5 local; model là client kịch bản của test C — chỉ kiểm logic thứ tự / giữ / bỏ).
- **Ca dò của B (khác cách C, không commit — `/tmp/b_rv6_probe/test_probe_b161.py`):** (1) ngắt kết nối (`aclose`) giữa lúc xả hàng đợi ở tuyến giữ; (2) tuyến giữ + phần chạy trước lỗi ⇒ so kiểu lỗi với đường cũ; (3) lượt **có lịch sử** ⇒ so byte yêu cầu gửi model với đường cũ (C chỉ thử lượt không lịch sử).
- **Bất biến kiểm:** "cờ #6 bật, tuyến `tro_ly_hue` ⇒ yêu cầu gửi model + chuỗi sự kiện giống đường cũ" — kiểm thêm ở lượt có lịch sử (ca 3).
- Chấm lại từ dữ liệu đã lưu: `tools/cham_an_toan.py an_toan_r1.jsonl`, `tools/chu_dau_abba.py tinh chu_dau_r1.jsonl`; so `q1/{main,nhanh_tat,nhanh_bat}.jsonl` (đa tập dòng).
- Đọc log `chat_stream_drain` của bên biến (rủi ro: phần bị huỷ đọc nốt trong vùng che trước khi `done` ra ở câu khẩn cấp).

## 4. Kết quả quan sát

- pytest: **11 passed** (7 test C + 3 ca dò B, 1 test tham số hoá 2 ca). Ngắt kết nối ⇒ không task treo, tuyến đúng, `llm_calls` mở đầu bằng định tuyến; lỗi phần chạy trước ở tuyến giữ ⇒ cùng kiểu lỗi đường cũ; lượt có lịch sử ⇒ yêu cầu + sự kiện giống byte.
- Chấm lại khớp report từng số: AN 0 vi phạm / 90 · K 0 / 30 · S1 0 · R 123: 0 (ngưỡng 2), lịch sử: 0 (ngưỡng 1) · lượt bỏ 62 (61 huỷ giữa chừng), `usd_bo` 0,0143 · **Q 1,368 s [0,337; 2,137], 15 / 20** · KC biến 1.802 ↔ mốc 1.832 ms · p50 / p95 chữ đầu mốc 5.357 / 8.687 ↔ biến 3.533 / 7.720 ms.
- Q1: `main` = cờ tắt = cờ bật, 228 / 228 dòng (so đa tập).
- Đọc nốt khi huỷ: 12 lần ở bên biến, 0,3–1,3 ms (trần 0,5 s) ⇒ không làm chậm `done` của câu cố định.
- Tiền report 0,0593 ≤ trần 0,10: khớp tổng `usd` hai công cụ chấm (0,0214 + 0,0116 + 0,0119).

## 5. Giới hạn hoặc phần chưa chạy

- M-1 chỉ đọc code (nhánh chưa có trường B4b / B5) — kiểm thật khi rebase.
- Không chạy lại lượt có phí; số tốc độ / an toàn là chấm lại trên dữ liệu C đã lưu (dùng lại hợp lệ: cùng commit, cùng dữ liệu, không đổi đầu vào).
- Câu trò chuyện chậm hơn khi bật (C ghi theo dõi, mẫu 2 câu) — không kiểm thêm.

## 6. Decision và bước tiếp theo

**ready_for_user_confirmation** cho kết luận thí nghiệm: mọi sàn + chỉ số quyết đạt, số tái lập được. Hai đổi User cần biết khi quyết bật (report đã nêu đúng): câu không về Huế tốn thêm ≈ 0,00023 USD / câu; câu khẩn cấp / ngoài phạm vi / trò chuyện nay cũng gửi kèm đoạn kho tới OpenAI.
**Trước merge:** rebase lên `main` (B4b, và B5 nếu đã merge) ⇒ đóng **M-1** theo tiêu chí trên ⇒ Q1 + test chạy lại ⇒ cổng ổn định ⇒ B kiểm lại phần M-1 (một vòng).

**Giải thích ngắn:** Bật cờ này thì câu về Huế ra chữ sớm hơn khoảng 1,4 giây, vì code bắt đầu tìm kho và gọi model trả lời trong lúc model định tuyến còn đang chạy; tuyến khác thì code bỏ phần chạy trước, không lọt chữ. Số đo của C tái lập được. Có một chỗ phải sửa lúc rebase: phần chạy trước phải mang theo các giá trị người dùng bấm nút (B4b / B5), không thì lịch trình sẽ hỏi lại lần hai.

## Vòng 2 — rebase + sửa M-1: `p9-toc-do-6b` `14db83b` (C kiểm · 13:18 05/11/2026 `date`, A giao)

Người sửa là B (rebase lên `main` `d66f6a3` + sửa M-1) ⇒ C kiểm (người viết code #6 ban đầu là C, phần sửa của vòng này là của B). Chỉ kiểm phần sửa M-1 + 2 test + Q1. 0 USD.

- **Cổng:** `d66f6a3..14db83b` = 1 commit, 4 file (`chat.py`, `settings.yaml` thêm `song_song_tra_loi: false`, `assistant.py`, test mới). `git diff --check` sạch. `git range-diff` so `ea081b0`: ngoài phần nối với B5 (`lich_cho_giao_dien`), chỉ đổi đúng chỗ M-1.
- **M-1 — đóng.** `ROUTE_INPUTS = ("history", "truong", "search_query")`. Trace phụ chép từng trường (không `dataclasses.replace` — đúng lý do B ghi: tránh dùng chung list sổ nguồn / công cụ). `_merge_spec` giữ cả 3 trường trong `keep_own`. **C kiểm đủ:** `chat.py` chỉ đặt sẵn đúng 3 trường này trước khi gọi lõi (`_start_conversation` ⇒ `history`; `_model_query` ⇒ `truong`, `search_query`).
- **2 test mới có giá trị thật** (C kiểm ngược, cách khác B): tạm đặt `ROUTE_INPUTS = ("history",)` trong worktree review ⇒ **cả 2 test hỏng**; trả lại ⇒ đạt. pytest `test_toc_do_song_song` + `test_b5_lich_trinh` + `test_chat_stream` + `test_api_chat` trên `14db83b`: **118 passed** (1 error = test cần khoá API thật, đã biết).
- **Q1 — C tự chạy lại độc lập** (`capture_all.py` trên worktree `/tmp/c_toc_do6b_r` detach `14db83b`; so với bản bắt `main` của C ở C191 — phần backend giống `d66f6a3` theo chuỗi bằng chứng C191 vòng 1–2): cờ `song_song_tra_loi` **tắt 228 / 228 giống byte**; **bật** (sửa `settings.yaml` tạm trong worktree review, đã trả lại) **228 / 228 giống byte**, cả thứ tự dòng. 10 lượt `api_chat_stream` đi đường song song.
- **Ghi chú (không phải finding):** khi bậc "sửa lịch nhiều lượt" thêm đầu vào route đặt trước (vd khung lịch đã lưu của cuộc) ⇒ phải thêm vào `ROUTE_INPUTS` — C ghi điều này vào plan C193.

**Decision vòng 2: ready_for_user_confirmation** — A merge với cờ bật (theo quyết của User).
