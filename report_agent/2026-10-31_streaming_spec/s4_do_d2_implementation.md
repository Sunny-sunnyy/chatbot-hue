# Implementation Report: Streaming S4 — đo D2 trên trình duyệt (spec §6 C1–C3, C5, C6)

Người làm: B (Claude Opus 5.5)
Date: 12:24 01/11/2026 (`date`) · Lượt đo chạy 12:20:39–12:23:10 01/11/2026
Spec: `docs/superpowers/specs/2026-10-31-streaming-design.md` (`00fb57ee01b2`) §6, §5 hàng S4. Tiêu chí ghi trước: `data/s4_2026-11-01/tieu_chi_ghi_truoc.md` (**`5d217f6a5b79`**,
viết 12:13 01/11/2026 theo `date` trong file, trước khi chạy). A quyết 01/11: bộ câu **pa1**; User duyệt **trần S4 riêng 0,03 USD**.
Đo trên nhánh **`streaming-final`** commit **`6a0c842`** (S1–S3 + B108), worktree `/tmp/b_final`. Nhãn độ tin: **[một lần chạy]**.

## 1. Phạm vi

Đo thời gian người dùng chờ trên **trình duyệt thật** khi hỏi qua giao diện streaming: tới chữ trả lời đầu tiên (C1), câu từ chối (C2), tới đủ câu (C3), tiền / câu (C6), và chữ hiện = chữ đã
kiểm (C5). Không đổi code chatbot.

## 2. Thay đổi chính

Không đổi code dự án. File private `data/s4_2026-11-01/`: `questions_s4.jsonl` (`ef141415cc25`), `ngoai_kho_tu_viet.jsonl` (`22c775e747e7`), `ghi_truoc_khi_chay.txt`, `run_pilot.jsonl`
(`d01f88a599f5`), `run_main.jsonl` (**`77c7a1b0ef16`**), `summary_main.json` (`9322f5fbb337`); script `tools/s4_build_questions.py` (`75f3d04e2f93`), `tools/s4_measure.py` (`dd955d863521`),
`tools/s4_summarize.py` (`8c475a72503f` — sửa đường import sau lượt thử, logic không đổi).

## 3. Cách đã chạy thật

1. **Ghi trước** (12:19, máy kiểm): commit `6a0c842`; build record `51fb1ec63cbc`; sparse `c8134c49a648`; Qdrant 1 collection 8.424 point; T1 `4d5bbe9e0edc` (chạy trên nhánh này 01/11);
   Golden md5 `6331e88fb171`; không server API nào khác đang chạy; tải máy 0,09.
2. Server: `cd /tmp/b_final/backend && HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env uvicorn api.app:app --port 8796` (settings production) ⇒ `/health` 5 / 5.
3. Trình duyệt: Chromium headless 145 (Playwright 1.58.0), `127.0.0.1`. **Chạy một mình (W31):** A báo C / agent con không chạy việc nặng / có phí / server; tải máy suốt lượt 0,5–0,6.
4. **Thử 3 câu** (+ 1 khởi động) — kiểm script, **không** gộp số. Rồi **lượt chính 59 câu** (+ 1 khởi động không tính), tuần tự, mỗi câu một trang mới:
   `t_first_text` = `performance.now()` từ lúc bấm gửi tới khung hình đầu sau khi `#answer` có chữ; `t_done` = lúc ô hỏi mở lại. Mỗi câu ghép **đúng 1** dòng `chat_metrics` mới (khác ⇒ dừng).
5. Tóm: `uv run python ../data/s4_2026-11-01/tools/s4_summarize.py ../data/s4_2026-11-01/run_main.jsonl` (từ `backend/` của nhánh; p50 / p95 nội suy tuyến tính; CI bootstrap 10.000, seed `20261101`).

**Bộ câu (pa1):** 40 câu dev (nhóm `dev`, không nhóm test, không câu kín): 8 câu tự nhiên loại dài (nhiều nguồn / so sánh) + 4 câu loại dài nhãn "chỉ đo năng lực" ⇒ 12 câu dài; 28 câu tự nhiên khác
⇒ 40 câu dev = 36 tự nhiên + 4 năng lực; + 7 câu dev ngoài kho tự nhiên + 12 câu ngoài kho tự viết. Thứ tự xáo seed.

## 4. Kết quả quan sát

59 / 59 câu chạy xong, **0 lỗi kỹ thuật**, 59 dòng `chat_metrics` (+ 1 khởi động). 38 câu dev được trả lời, 2 câu dev bị model từ chối (sang C2), 19 / 19 câu ngoài kho từ chối đúng (0 bị trả lời).

| Tiêu chí | Ngưỡng ghi trước | Kết quả | |
|---|---|---|---|
| **C1** tới chữ trả lời đầu tiên trên trình duyệt (n = 38) | sàn p50 ≤ 3.000 / p95 ≤ 5.000 ms | **p50 1.228 · p95 2.612 · max 4.741 ms** | **ĐẠT sàn** |
| C1 — mục tiêu báo cáo (Q1) | p50 ≤ 1.500 / p95 ≤ 3.000 ms | 1.228 / 2.612 | **đạt** mục tiêu |
| C1 — chỉ câu tự nhiên (n = 34) | (báo kèm, pa1) | p50 1.173 · p95 2.857 · max 4.741 | đạt sàn + mục tiêu |
| C1 — chỉ câu dài (n = 11) | (báo kèm) | p50 1.896 · p95 2.364 · max 2.429 | |
| C1 — phía server `first_text_ms` (n = 38) | (theo dõi) | p50 1.205 · p95 2.589 | trình duyệt chậm hơn server trung vị **22,5 ms** |
| **C2** câu từ chối: tới lúc biết chắc (n = 21: 19 ngoài kho + 2 dev) | cùng sàn 3.000 / 5.000 ms | **p50 1.476 · p95 2.930 · max 6.287 ms** | **ĐẠT sàn** (1 câu > 5 s) |
| **C3** tới đủ câu (n = 38) | theo dõi | p50 1.725 · p95 3.807 · max 5.504 ms | 2 câu chữ đầu > 3 s, 0 câu > 5 s |
| C3 — lợi "đủ câu − chữ đầu" (theo cặp) | **< 500 ms ⇒ A xem lại PA3 (D5)** | **trung vị 441 ms, CI 95 % [371; 535]** | **chạm luật — A xem lại** |
| C3 — lợi riêng câu dài (n = 11) / ngắn (n = 27) | (báo thêm) | 510 [430; 711] / 375 [328; 558] ms | |
| **C5** chữ ghép từ `delta` = chữ cuối đã kiểm | kỳ vọng 0 lệch | **0 / 59** `delta_matches_final = false` | ĐẠT |
| **C6** USD / lần gọi (giá đủ, token + token đệm từ log) | ≤ 0,0005 | **TB 0,000247 · max 0,000339** | **ĐẠT** |

**Đọc số:**
- Sàn tốc độ của User (3 / 5 s tới chữ đầu) **đạt rộng**; cả mục tiêu báo cáo 1,5 / 3 s cũng đạt. Theo luật Q1 ("đạt mục tiêu dễ ⇒ A đề xuất nâng sàn"): p50 dư 0,27 s, p95 dư 0,39 s so với mục
  tiêu ⇒ đạt nhưng không dư nhiều; A quyết có đề xuất nâng sàn không.
- **Lợi của hiện chữ dần nhỏ trên bộ này** (trung vị 0,44 s): câu trả lời trong bộ dev phần lớn ngắn (đủ câu trung vị 1,7 s), và hôm nay model gần như không suy luận trước khi viết (token suy
  luận trung vị **0** ở 38 câu, so với 81 ở C73 28/10) ⇒ chữ đầu tới sát lúc xong. Câu dài lợi ~0,5 s. Số harness 28/10 "sớm hơn 1,92 s" đo trên 10 câu tự viết dài hơn, kho / cấu hình khác — không
  so trực tiếp. Theo luật ghi trước (spec §2 D5, §6 C3): **A xem lại PA3** (chỉ tiến độ, câu trả lời hiện một lần). Lưu ý: CI 95 % [371; 535] chứa 500.
- Đuôi chậm: chữ đầu max 4,7 s (1 câu dài); một câu ngoài kho 6,3 s tới lúc biết từ chối (một lần — server cùng 6,1 s ⇒ phía model / mạng, không phải giao diện).

**Tiền:** lượt chính 0,014548 USD; cả S4 (64 lần gọi: thử 3 + 2 khởi động + 59) **0,015802 USD** theo giá đủ (97 % phần vào là ghi đệm) — ước 0,019, **trần S4 0,03** ⇒ trong trần.

## 5. Lỗi và giới hạn

- **Một lần chạy** buổi trưa 01/11 trên máy cá nhân, `127.0.0.1` (không có mạng tới người dùng), Chromium headless; không đo điện thoại / mạng yếu / proxy (spec §10). Thời gian phía provider đổi theo giờ
  và theo lượng suy luận (hôm nay suy luận gần 0 ⇒ chữ đầu sớm hơn thường).
- n = 38 ⇒ p95 gần như là câu chậm thứ hai (spec C1 đã ghi) — báo kèm max.
- "Chữ đầu được vẽ" lấy ở khung hình đầu (`requestAnimationFrame`) sau khi DOM có chữ — sai khác so với lúc pixel thật hiện ≤ ~1 khung hình (~16 ms).
- Bộ câu pa1 có 4 câu "chỉ đo năng lực" (A quyết); số chỉ câu tự nhiên báo riêng (vẫn đạt).
- `s4_summarize.py` sửa đường import sau lượt thử (lỗi `ModuleNotFoundError`), không đổi phép tính; lượt chính tóm bằng bản đã sửa.
- Lượt này dùng được lại cho plan đo cuối §3.4 **chỉ khi** `git diff 6a0c842 <commit đo cuối> -- backend/ frontend/` rỗng + build record / sparse / Qdrant giống (plan §3.4).

## 6. Bàn giao cho người kiểm

- Tính lại (0 USD, tất định): lệnh §3 bước 5 trên `run_main.jsonl` (`77c7a1b0ef16`) ⇒ so `summary_main.json` (`9322f5fbb337`); kiểm 59 dòng ↔ 59 câu, `t_first_text` ≤ `t_done` mọi câu, 0 câu ngoài kho
  bị trả lời.
- Ca dò khác cách gợi ý: tính p50 / p95 bằng thứ hạng gần nhất (thay nội suy) xem kết luận sàn có đổi không; đối chiếu `t_first_text` trình duyệt ↔ `first_text_ms` server từng câu (chênh trung vị 22,5 ms).
- Server đã tắt (`curl :8796/health` không trả lời). Worktree `/tmp/b_final` giữ tới khi A merge.

**Giải thích ngắn:** mình đo bằng trình duyệt thật xem người hỏi phải chờ bao lâu mới thấy chữ trả lời đầu tiên. Trên 38 câu, một nửa thấy chữ trong khoảng 1,2 giây, 95 % trong 2,6 giây — đạt
cả sàn 3 / 5 giây lẫn mục tiêu 1,5 / 3 giây; câu ngoài kho cũng được từ chối nhanh và đúng hết, tiền mỗi câu khoảng nửa mức trần. Nhưng vì câu trả lời phần lớn ngắn, hiện chữ dần chỉ giúp thấy
sớm hơn khoảng 0,4 giây so với chờ cả câu — dưới mốc 0,5 giây đã ghi trước, nên A cần xem lại có giữ kiểu "chữ chạy dần" hay chuyển sang kiểu đơn giản hơn.
