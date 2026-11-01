# Implementation Report: lượt đo cuối Phase 1–8 — phần không phải bộ kín (C111, gộp phần B)

Người làm: C (Claude Opus 5.5, terminal `hue-rag-6a`) — §0–§5, §9; B — §6–§7 (`do_cuoi_b_an_toan_ngay.md`) · Date: 13:13 01/11/2026 (`date`)
Plan duyệt `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` **`ae8d42d520d4`**; runbook private `data/do_cuoi_2026-11-01/runbook.md` **`bdd883bb367c`** (B review vòng 2 ready). Bộ kín mới (§8)
do B chạy (chỉ in số đếm) — §4 gộp tóm tắt từ `do_cuoi_b_bo_kin.md`. Câu tả ở mức loại câu; không chép câu hỏi / câu trả lời / ngữ cảnh. Kết quả chi tiết: private `data/do_cuoi_2026-11-01/`.

## 1. Phạm vi

Chụp lại chatbot cuối Phase 8 (đã có streaming + tính tiền giá đủ) trên **một bản code**, không chọn biến thể: Golden 176 "không làm hỏng" so với mốc 30/10 + A/A cùng ngày; bộ an toàn 32; 15 câu theo ngày;
22 câu B65 qua `/api/chat`; tốc độ trên trình duyệt (S4, dùng lại); tiền / câu.

## 2. Thay đổi chính

Không đổi code / dữ liệu dùng chung. Một sửa trong harness private **trước mọi lần gọi có phí** (12:53 01/11/2026, A đồng ý): `do_cuoi.py run` chốt "cùng một commit" theo **HEAD** nên dừng ngay khi A commit tài liệu
(`d50e679`, chỉ docs) ⇒ đổi chốt thành **code** (`backend/`, `frontend/`, `pyproject.toml`, `uv.lock`) phải giống commit đo `89c988e`, khác thì dừng; meta ghi cả HEAD lúc chạy lẫn `commit_do`. Đây là thay đổi
harness **sau** review vòng 2 của B — người kiểm xem (`tools/do_cuoi.py` `run`).

## 3. Cách đã chạy thật

- **Commit đo** `89c988e` (HEAD `main` lúc preflight; các commit sau đó chỉ tài liệu — `git diff 89c988e HEAD -- backend frontend pyproject.toml uv.lock` rỗng ở mọi lượt). Code giống `6a0c842` (S4 + cổng ổn định
  của B chạy trên đó) — `git diff 6a0c842 89c988e -- backend/ frontend/` rỗng ⇒ **dùng lại** S4 và cổng ổn định (`Session_Prompt.md` §6), không chạy lại.
- **Ghi trước (preflight, 0 USD):** build record `51fb1ec63cbc`, sparse `c8134c49a648`, nhãn v5 `33d16fd6b8f4`, 8.424 point, 1 collection, 10 đoạn ngữ cảnh, `gpt-6-luna`, Golden md5 `6331e88fb171`, 176 câu
  (`golden/preflight.json` `e6fc91051f37`). **T1** 158 câu chạy lại ⇒ **giống byte `4d5bbe9e0edc`**. Bộ "trước" = bản sao giống byte bộ "sau" đợt 2 (`45487ea1d88a`, commit `751b352`).
- **§4** 22 câu B65 (`bac5c91db005`) qua `POST /api/chat` server thật cổng 8796, tuần tự, chạy một mình (W31); server tắt sau đó.
- **§5** Golden: pilot 10 câu (0,00016 USD / câu < ngưỡng dừng 0,0004) ⇒ 166 câu còn lại ⇒ A/A 176 câu cùng ngày; `export-judge` ⇒ 18 lô, 413 mục (528 câu trả lời của ba bên, chữ trùng chấm một lần) ⇒
  **6 sub-agent judge mới** (Opus 5.5), mỗi agent đọc chỉ `backend/evaluation/full_corpus_judge_prompt.md` + 3 lô ⇒ `check-judge` 413 / 413, 0 lỗi ⇒ `f2-candidates` = [] (không rejudge) ⇒ `analyze` một lần.
  B chạy §6 / §7 song song (thư mục riêng) ⇒ `wall_ms` của Golden (chỉ theo dõi) có thể lệch nhẹ.
- **§6 / §7:** B — xem `do_cuoi_b_an_toan_ngay.md` §3 (2 judge mỗi phần, cổng đối chứng, phân loại A2 vế 2, sinh lại 3 lần hai bên — bên mốc trong worktree `751b352`, T1 giống byte trước khi sinh).

## 4. Kết quả quan sát

**Golden 176 — "không làm hỏng" so với mốc 30/10** (`golden/analyze.json` `13fccf9bab68`; số chính = 129 câu trong kho, bỏ câu người thật ít hỏi)

| Tiêu chí ghi trước (plan §3.1) | Ngưỡng | Kết quả | |
|---|---|---|---|
| F1 câu ngoài kho bị trả lời | 0 / 18 | **0 / 18** | đạt |
| F3 lỗi kỹ thuật (sau, A/A) | 0 | **0 / 0** | đạt |
| F4 lỗi trích dẫn (500) mới | 0 | **0** | đạt |
| F2 "nói chắc sai" mới | 0 | **0 ứng viên** (không cần chấm lại) | đạt |
| T1 Đủ ý: số câu tụt / TB theo cặp | ≤ 5 và ≥ −0,1 | **2** · **+0,016** [−0,023; +0,054] (thắng / hoà / thua 4 / 123 / 2) | đạt |
| T2 Đúng: số câu tụt / TB | ≤ 5 và ≥ −0,1 | **2** · **+0,008** [−0,023; +0,039] (3 / 124 / 2) | đạt |
| T3 từ chối nhầm trong phạm vi | ≤ mốc + 1 (12) | **12** / 158 | đạt |
| A/A (luật Q2: chỉ dùng khi 4–6 câu tụt) | — | không sát ngưỡng ⇒ không áp; "sau" ↔ A/A: Đủ 0 / 128 / 1, Đúng 1 / 128 / 0 | |
| **Kết luận** | | **không làm hỏng** | |

Theo dõi: điểm trung bình số chính bên "sau" Đúng **4,713** · Đủ **4,581** · Trúng ý **4,721** (mốc 30/10: 4,705 / 4,566 / 4,721; A/A 4,721 / 4,574 / 4,698). Đủ ý theo loại câu (bên "sau"): một dữ kiện 4,91 ·
có điều kiện 4,68 · so sánh 4,35 · **nhiều nguồn 3,50** (yếu nhất — User đã để Phase 9). Tiền / câu (giá đủ): sau TB **0,000247** · p95 0,000339 · lớn nhất 0,000436 USD (A/A 0,000248) ⇒ **đạt** trần 0,0005.
Thời gian sinh trong harness (theo dõi, không HTTP): sau p50 1,76 / p95 3,42 s · A/A 1,89 / 4,06 s · mốc 30/10 2,19 / 4,90 s.

**22 câu B65 qua `/api/chat` (cả câu, không stream — theo dõi)** (`b65/seq.meta.json` `267e2cd3fd43`)

| Mục | Kết quả | Mốc B65 27/10 (10 đoạn, tuần tự) |
|---|---|---|
| Thời gian phía trình khách p50 / p95 / lớn nhất | **2.340** [1.703; 3.086] / **3.800** [3.466; 4.141] / 4.141 ms | 3.068 / 6.039 ms |
| `total_ms` phía server p50 / p95 | 2.390 / 4.106 ms | — |
| Lỗi · dòng `chat_metrics` mới | 0 / 22 · 23 = 22 + 1 khởi động | |
| Câu ngoài kho từ chối đúng · câu trong kho bị từ chối | 2 / 2 · 2 / 20 | |

**Tốc độ trên trình duyệt (S4, dùng lại — `s4_do_d2_implementation.md`)**: tới chữ trả lời đầu tiên p50 **1.228** / p95 **2.612** ms (n = 38) ⇒ đạt sàn 3 / 5 s **và** mục tiêu báo cáo 1,5 / 3 s.

**Bộ an toàn 32 + câu theo ngày (B — `do_cuoi_b_an_toan_ngay.md` §4):** A1 0 / 4 câu ngoài kho bị trả lời · A2 vế 1 **2** câu sai điều kiện mới (đúng ngưỡng ≤ 2; cả hai là 2 câu từng dao động ở A/A 29/10, sinh lại
3 lần: bản mới và bản mốc `751b352` đều sai 1 / 3 ⇒ dao động ngang mốc) · A2 vế 2 **0** đảo cảnh báo (cả hai loại "nói sai về nguồn") · câu theo ngày: **0** câu đoán ngày rồi nói sai / 12, từ chối nhầm 5 câu
trong kho (mốc 6 / 14). Cổng judge đạt (10 / 10, 0 / 5, tách lô 0; phiếu kiểm 6 / 6).

**Bộ kín mới §8 (B — `do_cuoi_b_bo_kin.md` §4; gộp 13:21 01/11/2026, C chỉ đọc số đếm, không mở `kin/`):** 40 câu chưa ai thiết kế hệ thống thấy (34 trong kho + 6 ngoài kho), một lượt: sàn **đạt** —
0 / 6 câu ngoài kho bị trả lời, 0 / 40 lỗi kỹ thuật, 0 / 30 sai điều kiện, 0 bịa thêm (cổng judge 10 / 10 · 0 / 5). Điểm TB thấp hơn Golden số chính: Đủ **4,18** [3,74; 4,59] ↔ 4,58, Đúng 4,38 ↔ 4,71;
từ chối nhầm **4 / 34** ↔ 12 / 158 — cả 4 ở loại nhiều nguồn / so sánh; chỉ câu được trả lời Đủ 4,60 ≈ Golden ⇒ số dev **hơi lạc quan**, CI chạm số Golden (chưa rõ về thống kê).

**Tiền lượt đo cuối (giá đủ, `tools/tien_cuoi.py`)**: Golden sau 0,0434 + A/A 0,0436 · B65 0,0070 · an toàn 0,0095 + sinh lại 0,0021 + mốc 0,0022 · ngày 0,0043 ⇒ **0,1122 USD**; + S4 đã tiêu 0,0158 ⇒
**0,1280**; + bộ kín §8 0,0112 (B) ⇒ **0,1392 / trần 0,20** USD. Judge / sub-agent: quota Claude.

## 5. Lỗi và giới hạn

- Không lỗi kỹ thuật nào ở mọi lượt. A2 vế 1 của bộ an toàn chạm **đúng** ngưỡng (B §5).
- Golden và bộ an toàn đo đường **không stream** (`answer_case`); route stream dựa trên lõi chung + spec C5 (giới hạn plan §10).
- Mốc "trước" sinh ngày 30/10 (khác ngày) — không sát ngưỡng nên không cần tách trôi; A/A cùng ngày cho nhiễu rất nhỏ (1 câu đổi mỗi chỉ số).
- Judge Claude, chưa có mốc người (B0); bộ câu tự viết / LLM viết; "không làm hỏng" chỉ phát hiện được tụt lan rộng, không tụt nhỏ ở một loại câu.
- `wall_ms` Golden đo lúc B chạy §6 / §7 song song (chỉ theo dõi). 22 câu B65 chạy một mình.
- Harness sửa sau review (chốt theo code thay vì HEAD — §2).

## 6. Bàn giao cho người kiểm

- Tính lại 0 USD (từ `backend/`, trên bản sao bằng `DO_CUOI_DIR` vì lệnh ghi file từ chối ghi đè): `do_cuoi.py check --arm truoc|sau|aa`, `check-judge`, `analyze` ⇒ so `golden/analyze.json` `13fccf9bab68`;
  sha file đáp: `golden/sau/sau.jsonl` `6084e3aec7e1`, `golden/aa/aa.jsonl` `96278512f7c0`, T1 `4d5bbe9e0edc`.
- Đọc `tools/do_cuoi.py` `run` (chốt theo code, §2) và `analyze` (luật A/A, bỏ câu chưa có điểm).
- Ca dò gợi ý: đếm tụt Đủ / Đúng chỉ trên câu có cùng tập 10 đoạn hai bên (tách nhiễu sinh khỏi đổi tìm — tìm giống byte nên kỳ vọng mọi câu); so điểm judge của các câu trả lời trùng chữ ở hai bên (phải bằng nhau vì chấm một lần).

**Giải thích ngắn:** mình chạy lại toàn bộ bộ câu chuẩn trên chatbot cuối Phase 8 (đã có hiện chữ dần và tính tiền đúng giá) rồi cho người chấm mù chấm cùng lúc với kết quả ngày 30/10 và một lượt chạy lặp cùng
ngày. Không có câu ngoài kho nào bị trả lời, không lỗi, không câu nào "nói chắc sai" mới; chỉ 2 / 129 câu bị chấm kém đi, trong mức cho phép ⇒ không làm hỏng. Hỏi qua web: chữ đầu hiện sau ~1,2 s (95 % câu dưới
2,6 s); cả câu qua API trung vị 2,3 s; mỗi câu ~0,00025 USD (~6 đồng). Câu cần ghép nhiều nguồn vẫn yếu nhất — để Phase 9.
