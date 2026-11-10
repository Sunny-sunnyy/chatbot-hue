# Review: Phase 9 T2 — công cụ `yeu_cau_tra_web`, phần 0 USD (nhánh `p9-t2-web` `2ac126a`, E)

Decision: **ready** cho phần 0 USD (0 blocker · 0 major · 2 minor) — lượt có phí chạy sau khi rebase lên `main` có G (phương án B); review lại phần chạm khi rebase
Người kiểm: C (Claude Code, `hue-rag-6a`)
Date: 21:08 09/11/2026 (`date`)
Canonical guide: plan `docs/superpowers/plans/2026-11-08-phase-9-t2-web-plan.md` bản 2 (A duyệt `88b1f0586e99`; md5 bộ hỏi kèm ghi thêm ⇒ `69836a615353`)
Implementation report: `report_agent/2026-11-08_phase_9_ban_13/e_t2_web_implementation.md`

## 1. Phạm vi đã review

Exact diff `main...origin/p9-t2-web` (5 file: `settings.yaml`, `assistant.py`, `full_corpus_prompt.py`, `generator_openai_full_corpus.py`, test mới); đường #6
(`assistant.py:1112` `without_router`, `_merge_spec`). Không đọc STATUS_E.

## 2. Findings

Đối chiếu plan §1: (1) công cụ không tham số, câu trả về cố định trung tính, trần 1 lần (lần 2 ghi `het_luot`, không đổi gì) — **khớp**; mô tả công cụ **đúng nguyên văn** plan
§1.1. (2) `max_turns_for(ngay_lich_fn, web_fn)` +1 cộng dồn với T1 — **khớp** (M-1 review plan). (3) `web_gate_open` sửa một chỗ: nhánh mới = cờ ∧ đã yêu cầu ∧
`fixed_outcome is None` ∧ chữ ∉ `REFUSAL_ANSWERS`, điều kiện chung giữ (tuyến, chưa tra, lỗi citation / công cụ, hỏi lại, lịch, lượt ghép) — **khớp**. (4) `cong_web`, `TU_WEB_LUAT`
không đổi — **khớp**. (5) test đủ các ca plan ghi.

Hai chỗ E tự quyết:
- **#6 tắt `tra_web` ở phần chạy song song** (`dataclasses.replace` gọi lại `__post_init__`) ⇒ ràng buộc "`tra_web_cong_cu` cần `tra_web`" chuyển sang `from_settings`: **đúng** — phần
  song song vẫn đưa công cụ (chuỗi gửi model giống đường thường, test `song_song_6` khẳng định), cờ `web_yeu_cau` là trường `AnswerTrace` nên `_merge_spec` chép sang, cổng chạy
  trên trace chính với `flags` gốc. Hệ quả nhỏ: ai dựng `AssistantFlags(tra_web_cong_cu=True)` tay mà thiếu `tra_web` ⇒ công cụ có, cổng không bao giờ mở (vô hại).
- **"Lượt có lịch không đưa" hiểu là lượt ghép từ nút; lượt có `lich_trinh` vẫn có công cụ, cổng đóng:** **chấp nhận** — trước lần sinh code chưa biết model có gọi
  `lich_trinh` không, nên không thể bỏ công cụ theo "lượt có lịch"; cổng đã đóng bằng `trace.lich is None`.

- **m-1 (T4):** khi bật `lich_trinh` (T4) lượt có thể gồm `tim_kho` + `lich_trinh` + `yeu_cau_tra_web` — chuỗi xấu nhất chưa test với `lich_trinh`; T4 kiểm `max_turns` = 0 trên bộ của nó.
- **m-2 (bẫy chung, A ghi):** harness đọc `application.log` theo vị trí dòng — từ `p12-chot-deploy` (`ccc9f4f`) log xoay vòng ở 10 MB ⇒ lượt đo trùng lúc xoay sẽ đếm hụt; lượt đo
  T2 kiểm cỡ log trước (hoặc đọc cả `application.log.1`).

## 3. Cách người kiểm chạy lại thật

- `cd /tmp/c_t2rv/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_t2_web_cong_cu.py tests/test_b6_tra_web.py tests/test_b2_tool_loop.py tests/test_ngay_lich.py -q`
  (worktree tách ở `2ac126a`, Qdrant thật chỉ đọc).
- Q1 cờ tắt: `capture_all.py` trên nhánh ⇒ `data/phase_9/t2_web/q1_c_review_tat.jsonl`, so `cmp` với mốc `data/phase_9/t3_bang_ve_gio/q1_a/main_5c982a0.jsonl` (dùng lại được:
  `git diff 5c982a0 fb621e0 -- backend` rỗng, `fb621e0` = điểm tách nhánh).

## 4. Kết quả quan sát

183 passed (32 giây). **Q1 cờ tắt 228 / 228 giống byte** (27 giây) — khớp số E báo. 0 USD.

## 5. Giới hạn hoặc phần chưa chạy

Không chạy test rộng (E đã chạy file chạm; test rộng một lần trước merge, sau rebase lên G). Không chạy Q1 cờ bật (khác chuỗi là đúng thiết kế — test `test_request_per_turn_type`
khẳng định chỉ thêm công cụ, lời dặn + tin nhắn giống). Lượt có phí: NOT RUN (chờ G).

## 6. Decision và bước tiếp theo

Phần 0 USD sẵn sàng. Bước tiếp (E): rebase lên `main` có G (phương án B) ⇒ chạy lại file test chạm + Q1 cờ tắt ⇒ lượt có phí theo plan §2 ⇒ test rộng ⇒ review cả nhánh (C xem phần
delta sau rebase + kết quả đo).
