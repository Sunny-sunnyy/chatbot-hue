# Implementation Report: Phase 8.2 §10 R2 — trả lời phần có căn cứ (chữ E1b) — dừng ở bước 1, phạm sàn

Người làm: C (Claude Opus 5.5, terminal `hue-rag-b5`) · 2026-10-26 22:13 +0700 (`date`) · Việc: C43 (A giao 22:1x, "làm đi").
Plan A duyệt: `phase_8_2_r2_plan.md` sha `b70ea775efb2` (commit `08419c0` trên `main`). Spec §10 bản `cd910c4c4169`.
Code: nhánh `p82-r2` = `811d25d` + `0cbad2d` (harness `r2.py`, sha `a8967cfe591a`).
**Tiền thật: 0,0026861 USD.** Trạng thái: **chờ review** (B).

## Cho bạn — lời thường

1. Mình thử cho chatbot trả lời **phần có căn cứ** khi chỉ tìm được một phần thông tin, thay vì từ chối cả câu.
2. Theo kế hoạch, bước đầu là phép thử rẻ nhất: 12 câu hỏi **ngoài phạm vi kho**. Câu nào chatbot cũng phải từ chối.
3. Có **1 / 12 câu bị trả lời**: câu hỏi giá vé tàu từ một thành phố khác tới Huế. Chatbot nói một ý chung về giá vé, có trích nguồn, rồi thêm
   "nguồn không có giá cụ thể". Phiên bản cũ ở Phase 8.1 mắc **đúng lỗi này, ở đúng câu này**. Câu chữ mới viết thêm để chặn lỗi đó nhưng
   không chặn được.
4. Theo luật ghi trước, kết quả là **kém hơn (phạm sàn)**. Mình **dừng ngay**, không chạy các câu khác, không chấm điểm, và **không đưa vào
   chatbot**. Tiền đã dùng: khoảng 0,0027 USD (≈ 70 đồng).

## 1. Phạm vi

Làm đúng plan §3 bước 1: 12 câu OOS nhóm dev. Plan §3 bước 1 và §4 ghi: "Có ≥ 1 câu không đúng chuỗi từ chối ⇒ kém hơn (phạm sàn),
dừng". Vì vậy **NOT RUN**: bước 2 (7 câu), bước 3 (phần dev còn lại), judge, test, phân tích theo tầng. Không đổi production, không ghi Qdrant,
không mở câu kín.

## 2. Thay đổi

- `backend/experiments/phase_8_2/r2.py` (mới, `0cbad2d`). Chữ E1b nguyên văn plan §1, thay đúng `_REFUSAL_RULE` (có `assert`); sha 12 ký tự
  của prompt R2 = `4acd169d706d` (ghi trong `.meta.json`). Mọi khâu khác là code production qua `full_corpus_eval.answer_case`: retrieval,
  context 10 theo `settings.yaml` ở `811d25d`, generator, validator.
- Các lệnh `run`, `merge`, `check`, `export-judge` / `check-judge` / `analyze` (theo nhóm dev / test). Mọi lệnh ghi đều **từ chối ghi đè**.
  Chỉ lệnh `run` đã chạy.
- Khác plan §3: bản harness đầu (trước khi duyệt) có lệnh `latency` 30 câu. C đã gỡ lệnh này theo B49 M-1 trước commit, nên khớp plan đã duyệt.

## 3. Cách đã chạy thật

Worktree `/tmp/c_r2` (nhánh `p82-r2`), symlink `data/` + `knowledge-base-hue/` tạm (gỡ khi xong):

```bash
cd /tmp/c_r2/backend
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag --env-file /home/minhhieu/hue_rag/.env \
    python -m experiments.phase_8_2.r2 run --cases oos_dev --name r2_oos_dev      # 22:12:04–22:12:21
```

## 4. Kết quả quan sát

`data/phase_8_2/r2/r2_oos_dev.jsonl` (sha `16158d284b5b`, private) + `.meta.json`:

| Kiểm | Kết quả | Sàn | |
|---|---|---|---|
| 12 câu OOS dev: đúng chuỗi từ chối | **11 / 12** | 12 / 12 | ✗ **phạm sàn** |
| Câu bị trả lời | `case_index` **160** | — | — |
| Lỗi kỹ thuật | 0 | 0 | ✓ |
| Lỗi citation (validator production) | 0. Câu 160 **có** `[n]`, nên validator không chặn; API sẽ trả lời người dùng | — | — |
| Mốc B1, cùng 12 câu | 12 / 12 từ chối | — | — |
| Tiền (usage log) | 23.561 token vào / 660 ra = **0,0026861 USD** (0,000224 / câu) | trần 0,06 | ✓ |

**Dạng lỗi của câu 160** (C đọc; câu dev; report không chép nguyên văn): câu hỏi về giá vé một phương tiện đi tới Huế, ngoài phạm vi kho.
Câu trả lời R2 gồm **một câu chung chung có trích `[1]`** (giá thay đổi theo điểm đi và thời điểm) cộng một câu "nguồn dữ liệu không có mức
giá cụ thể". P1 ở 8.1 (context 5) cho **gần như cùng câu trả lời ở cùng câu 160**. Đây là dạng "trích ý chung" mà plan E1 §2 đã chỉ ra.

⇒ **Giả định G4 của plan sai** với dạng "ý chung". Chữ E1b có câu "Thông tin chỉ cùng chủ đề mà không trả lời điều được hỏi thì không tính
là trả lời được", nhưng model vẫn coi một nhận xét chung là "trả lời được một phần". Dạng thứ hai (câu báo thiếu tự viết, không `[n]`) không
xuất hiện ở 12 câu này.

## 5. Kết luận theo tiêu chí ghi trước

- **R2 (E1b) — kém hơn (phạm sàn: 1 / 12 câu OOS dev bị trả lời).** Dừng ở bước 1 đúng plan §3 / §4.
- **Không chạy:** bước 2–6, test, judge. Không có số Completeness hay từ chối nhầm, nên **không** kết luận gì về lợi ích của R2.
- **Không đưa vào chatbot; không trình User đọc mẫu** (plan §5 chỉ áp khi R2 đạt).
- Theo plan §4 và `run-experiment` §4: đổi chữ E1b sau khi thấy số là **biến thể mới (E1c)**, cần plan mới và review lại. Tính cả P1 (8.1) và
  E1b, bài toán này đã qua **2 vòng**; vòng thứ 3 là vòng cuối trước khi dừng hẳn. A / User quyết có thử E1c không. C chỉ ghi các hướng (chưa
  đo):
  - siết chữ thêm (yêu cầu phần trả lời nhắc đúng đối tượng được hỏi);
  - kiểm bằng code sau sinh (câu trả lời có câu "nguồn không có…" ⇒ đổi thành từ chối). Hướng này là thêm cơ chế, cần cân nhắc
    `Session_Prompt.md` §7;
  - bỏ hướng trả lời một phần, quay sang khâu tìm (K3).
- **A quyết (22:1x): gác hướng R2**, không chạy vòng 3 (E1c) lúc này. Lý do: 2 vòng ra cùng một dạng lỗi; 80 % điểm mất nằm ở khâu tìm (C36);
  K3 có thể giảm chính nhóm câu P. Đây là **hướng mở**: chỉ quay lại khi có cách mới, và cách đó phải được kiểm trước là chặn đúng dạng
  "trích ý chung + nguồn không có" (ví dụ chạy lại trên câu 160 của P1 / E1b trước).

## 6. Lỗi và giới hạn

- Chỉ chạy 12 câu, một lượt LLM. Câu 160 trượt ở cả P1 8.1 lẫn E1b nên khó coi là nhiễu, nhưng chưa đo A/A cho riêng câu này. Theo luật sàn,
  một lần trượt là đủ để dừng.
- Không biết R2 có cứu được 5 câu nhóm P hay không (NOT RUN).
- 12 câu OOS dev là toàn bộ câu OOS dev; 6 câu OOS test chưa chạy.

## 7. Bàn giao cho người kiểm (B)

- Đọc `r2.py` (`0cbad2d`): chữ E1b khớp plan §1; `cases_for("oos_dev")` = 12 câu OOS của `split.json` dev; lệnh `run` chạy đúng
  `answer_case` production.
- Kiểm `data/phase_8_2/r2/r2_oos_dev.jsonl`: 12 dòng, 11 `refusal: true`, câu 160 `refusal: false`, có `[1]`, `citation_error: null`. Không cần
  chạy lại (có phí; kết luận đã chốt bằng một câu).
- Tiền thật lấy từ `.meta.json`.
