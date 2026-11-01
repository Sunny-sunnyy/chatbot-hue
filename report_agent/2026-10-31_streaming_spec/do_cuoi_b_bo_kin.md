# Implementation Report: lượt đo cuối Phase 1–8 — §8 bộ kín mới (phần của B)

Người làm (người chạy): B (Claude Opus 5.5) · Date: 13:19 01/11/2026 (`date`) · Để C gộp vào `do_cuoi_implementation.md`.
Plan duyệt `docs/superpowers/plans/2026-11-01-do-cuoi-phase-1-8-plan.md` **`ae8d42d520d4`** §3.7; runbook `data/do_cuoi_2026-11-01/runbook.md` **`bdd883bb367c`** §8. A cho chạy sau khi §5 Golden qua mọi sàn.
**Giữ mù:** B không đọc / in câu hỏi, đáp án, câu trả lời, ngữ cảnh, lời nhận xét judge — chỉ số đếm, trung bình, mã câu `K01…K40`. Report này: **chỉ số đếm theo loại câu** (`Session_Prompt.md` §5).
Bộ kín đã mở **một lần** cho lượt này ⇒ từ nay không còn kín (plan §3.7).

## 1. Phạm vi

40 câu bộ kín mới (sub-agent viết + sub-agent khác kiểm + User đọc mẫu, khoá sha trước): 12 một dữ kiện · 6 nhiều nguồn · 6 so sánh · 10 có điều kiện (gồm 4 câu điều kiện / cảnh báo) ·
6 ngoài kho. Một lượt sinh trên chatbot cuối Phase 8, chấm mù bằng thước Golden + thước lỗi nặng; so khoảng cách với Golden số chính của §5.

## 2. Thay đổi chính

Không đổi code / dữ liệu dùng chung. Script tạm `/tmp/b_kin/kin.py` (Session_Prompt §5: script việc câu kín để `/tmp`, **đã xoá** khi xong) — `prep` (đổi bộ kín sang khuôn câu hỏi của `an_toan_run.py`),
`export` (lô chấm), `check`, `summarize` (chỉ số đếm; bỏ trường `feedback` của judge). Kết quả private `data/do_cuoi_2026-11-01/kin/` (tên chứa `sealed`).

## 3. Cách đã chạy thật

- **Kiểm trước khi sinh:** `sha256sum final_sealed.jsonl` = **`7f97d4c10b2b`** (= khoá); 40 dòng; file câu hỏi đã đổi khuôn `sealed_questions.jsonl` `83097456c812` (qid K01–K40, `in_kho` = loại ≠ ngoài kho).
- **Commit:** HEAD `1a0445c`, code = commit §2 `89c988e` (`git diff 89c988e HEAD -- backend frontend pyproject.toml uv.lock` rỗng). Cùng build record / Qdrant với §5 (preflight của C).
- **Sinh** (từ `backend/`, `uv run`, đường production `answer_case` 10 đoạn, lưu ngữ cảnh model đọc): `an_toan_run.py --questions …/kin/sealed_questions.jsonl --out …/kin/sealed_gen --cap 0.0125`
  (trần phẳng 0,0125 ≈ trần 0,015 giá đủ của runbook) ⇒ `sealed_gen/answers_r1.jsonl` `f009d8e649be`.
- **Chấm** — mỗi lô một **sub-agent mới** (Claude Opus 5.5, cùng model phiên), đọc **chỉ** hướng dẫn + một lô, ghi file, trả về "xong + số mục":
  - thước Golden (`backend/evaluation/full_corpus_judge_prompt.md`): 1 agent, 40 mục (mọi câu không lỗi kỹ thuật, kể cả từ chối), xáo seed;
  - thước lỗi nặng (`data/loi_nang_2026-10-28/rubric.md`): **2 judge độc lập × 3 lô**, mỗi judge 45 mục = 30 câu trong kho được trả lời + 15 câu đối chứng B89 (cổng: bắt câu chèn sai ≥ 9 / 10, báo
    nhầm câu chép đúng ≤ 1 / 5); "một trong hai judge" như mọi lượt trước.
- `check` ⇒ đủ mục, 0 lỗi khuôn; `summarize` ⇒ `sealed_summary_counts.json` `7e6652acad82`. Khoảng tin cậy 95 % bootstrap 10.000 (seed `20261101`) tính trên điểm, không đọc nội dung.

## 4. Kết quả quan sát

**Sàn (plan §3.7):**

| Sàn | Kết quả | |
|---|---|---|
| Câu ngoài kho bị trả lời | **0 / 6** | **đạt** |
| Lỗi kỹ thuật | **0 / 40** | **đạt** |
| Đảo cảnh báo ở câu có điều kiện (gồm 4 câu điều kiện / cảnh báo) | **0** — không câu nào có ý sai điều kiện (P0_sai = 0 / 30) | **đạt** |
| Cổng judge lỗi nặng | judge 1: 10 / 10 · 0 / 5; judge 2: 10 / 10 · 0 / 5 | qua |

**Báo số (không quyết):**

| Thước | Bộ kín (34 câu trong kho) | Golden §5 "sau", số chính (129 câu) | Khoảng cách |
|---|---:|---:|---:|
| Đủ ý (Completeness) TB | **4,18** [CI 95 % 3,74; 4,59] | 4,58 | **−0,40** |
| Đúng (Accuracy) TB | **4,38** [3,91; 4,77] | 4,71 | −0,33 |
| Trúng ý (Relevance) TB | 4,38 | 4,72 | −0,34 |
| Đủ ý — chỉ câu **được trả lời** (30 câu) | **4,60** | — | ≈ Golden |
| Từ chối nhầm câu trong kho | **4 / 34 (12 %)** | 12 / 158 (8 %) | +4 điểm % |
| Lỗi trích dẫn (500) | 0 | 0 | |
| Bịa thêm (H) / sai điều kiện (P0_sai) | 0 / 30 · 0 / 30 | — | |
| Thiếu điều kiện (P0_thiếu, theo dõi) | 7 / 30 | — | |

**Theo loại câu (câu trong kho):**

| Loại | n | Đủ ý TB (bộ kín) | Đủ ý TB (Golden số chính) | Đúng TB (bộ kín) | Từ chối nhầm |
|---|---:|---:|---:|---:|---:|
| Một dữ kiện | 12 | 4,42 | 4,91 | 5,00 | 0 |
| Nhiều nguồn | 6 | 3,67 | 3,50 | 3,50 | **2** |
| Có điều kiện | 10 | 4,70 | 4,68 | 4,70 | 0 |
| So sánh | 6 | **3,33** | 4,35 | 3,50 | **2** |

**Đọc số:**
- Mọi sàn an toàn của bộ kín **đạt**: không câu ngoài kho nào bị trả lời, không bịa thêm, không sai điều kiện trên câu chưa ai thiết kế hệ thống nhìn thấy.
- Điểm trung bình thấp hơn Golden khoảng 0,3–0,4; khoảng tin cậy rộng (n = 34) và **chạm** số Golden ở cận trên (Đủ ý 4,59 ≈ 4,58) ⇒ "chưa rõ" theo nghĩa thống kê, nhưng hướng nhất quán: **số dev hơi
  lạc quan**. Khoảng cách gần như toàn bộ do **từ chối nhầm** (4 câu, đều ở loại nhiều nguồn và so sánh): chỉ tính câu được trả lời thì Đủ ý 4,60 ≈ Golden. Khớp Q3a (câu nhiều nguồn thiếu bằng chứng
  ở tầng tìm, User để Phase 9).
- Câu so sánh trên bộ kín yếu hơn Golden rõ (3,33 so với 4,35, n = 6 — mẫu rất nhỏ).

**Tiền:** giá đủ **0,011182 USD** (phẳng 0,009475) — trần 0,015. Judge: quota Claude (0 USD).

## 5. Lỗi và giới hạn

- Cỡ mẫu nhỏ: 34 câu trong kho (6 câu mỗi loại nhiều nguồn / so sánh) ⇒ CI rộng; 0 / 6 câu ngoài kho chỉ nói tỉ lệ trả lời câu ngoài kho < ~39 % (một phía 95 %) — cộng 18 Golden + 4 an toàn ⇒ 0 / 28 ⇒ < ~10 %.
- Bộ kín do agent viết (User chọn Q1 = PA1) ⇒ có thể vẫn "dễ" hơn câu người dùng thật (plan §9).
- Một lượt sinh, judge Claude (thước Golden 1 judge như các lượt Golden; thước lỗi nặng 2 judge), chưa có người đọc.
- Golden số chính bỏ 29 câu người thật ít hỏi; bộ kín không gắn nhãn độ tự nhiên (viết theo văn nói du khách) — so sánh hai bộ khác cách chọn câu, chỉ để biết hướng.
- Bộ kín đã mở ⇒ không dùng lại làm phép kiểm "chưa ai thấy"; muốn kiểm tổng quát hoá lần sau cần bộ mới.

## 6. Bàn giao cho người kiểm

- Tính lại (0 USD): đọc `sealed_summary_counts.json` + điểm / nhãn trong `kin/sealed_judge_*` bằng script chỉ in số — **người kiểm không phải A / B / C đọc nội dung** (plan §3.7: người kiểm là
  session khác; chỉ chạy phần tất định, không đọc câu).
- Bất biến kiểm: 40 dòng sinh = 40 câu; 34 trong kho + 6 ngoài kho; 30 câu được trả lời = 34 − 4 từ chối nhầm = số câu thật trong lô lỗi nặng.

**Giải thích ngắn:** mình chạy chatbot cuối Phase 8 trên 40 câu mới mà chưa ai làm hệ thống từng thấy, rồi cho người chấm mù chấm. Hệ thống vẫn an toàn như trên bộ cũ: không trả lời câu ngoài kho,
không bịa, không nói sai điều kiện. Điểm trung bình thấp hơn bộ cũ một chút, gần như chỉ vì 4 câu bị từ chối nhầm ở loại câu cần gom nhiều nguồn / so sánh — đúng chỗ yếu đã biết và đã để sang Phase 9;
những câu được trả lời thì chất lượng ngang bộ cũ.
