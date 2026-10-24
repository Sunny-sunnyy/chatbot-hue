# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 2026-10-24 (A, mở lại phiên). Cách dùng: `WORKFLOW.md` §3, §7, §9. Chỉ giữ
việc đang mở; việc xong chuyển tóm tắt sang `PROJECT_HISTORY.md`.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc hiện tại | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-77` | Claude Opus 5.5 | trực tiếp | Điều phối Phase 7B | đang làm |
| B — thực thi | `hue-rag-64` | Claude Opus 5.5 | trực tiếp | B7 sửa minor Gate 4; chờ điểm User | đang làm |
| C — thực thi | `hue-rag-d9` | Claude Opus 5.5 | trực tiếp | C6 chờ kiểm phần User của Gate 4 | rảnh |

User 2026-10-24: cả ba là Claude Code nên liên lạc `trực tiếp`. Nếu User đổi một
session sang Codex/AGY thì cột "Liên lạc" của nó là `qua User` (`WORKFLOW.md` §7).

## Quyền đang hiệu lực (User duyệt qua A)

- **User 2026-10-24 (trước khi nghỉ):** A được commit, push, tự điều phối, tự kiểm
  tra, tự tối ưu và phát triển hệ thống; tự dùng chi phí `gpt-6-luna` trong ngân sách.
- **Ngân sách `gpt-6-luna`:** giá 0,1 USD/1M input, 0,5 USD/1M output. Tổng session
  ≤1 USD (không bao giờ vượt 1,5 USD), "không cần dùng hết". Phase 7B ≤0,6 USD (spec 7B §6).
  Mỗi session gọi paid phải ghi usage token và báo tổng tiền trong report.
- Git: A commit/push `origin main`; B/C không commit.
- Qdrant: chỉ đọc.
- Duyệt cho A = duyệt cho B/C (User 2026-10-24). User đồng ý xóa những gì không còn
  cần/lỗi thời — A vẫn liệt kê đích và trình trước khi xóa thứ gì chưa có trong
  một việc đã duyệt.

## Việc của A

1. Trình User danh sách dọn C2 (sau khi 7B đóng).
2. Review B4, C3. Tập chấm lại 30 + mẫu User 20 **đã chọn** (rời nhau, phân tầng category, đủ 7
   partition, seed 20261025): `data/evaluation/phase_7b/subsets.json` (private, `case_index` 0-based).
3. Điều phối các Gate còn lại của 7B; chuẩn bị file chấm cho User.

## Việc của B

### B1 — Kiểm sức khỏe các Phase trước — A đóng 2026-10-24

`reports/phase_7b_gate_0_health_audit_2026_10_24.md`: nền full-corpus khớp `Project_Status.md` §4
(A chạy lại `audit.py`: PASS; 2 test fail do hằng số/dữ liệu cũ — đích dọn). Sự cố deselect §5.1
đã xử lý (CSV khôi phục; bẫy ghi §8). Nền đủ để lấy baseline 7B.

### B2 — Phase 7B Gate 1 — A đóng 2026-10-24

`reports/phase_7b_gate_1_evaluator_implementation_2026_10_24.md`. A kiểm: thứ tự `answer_case`
khớp `api/routes/chat.py`; 10 test pass; hai file retrieval `dense_bm25_rrf` giống byte; smoke
summarize khớp report (0,0028 USD). Finding minor m1 (sửa ở B3): `judge-luna --cases` không
kèm giá trị → `[] or …` thành mọi case (paid); `export-judge-input` cùng mẫu (free).

### B3 — Phase 7B Gate 2 — A đóng 2026-10-24

`reports/phase_7b_gate_2_runs_implementation_2026_10_24.md`. A kiểm: m1 đúng (`answered_cases`), 11
test pass; summarize Run 1 + luna khớp report; 352 response id khác nhau; 64/176 câu trả lời giống
hệt chữ giữa hai run; **0 case đổi quyết định từ chối** → 22 từ chối nhầm là hệ thống, không phải
nhiễu. Tiền 7B tới đây ~0,082 USD.

### B4 — tổng hợp nhiễu + chẩn đoán từ chối nhầm — A đóng 2026-10-24

`reports/phase_7b_false_refusal_diagnosis_2026_10_24.md` (commit `9514f75`): luna chấm lại gần tất
định (lệch ≤1 ở 100%); 22 từ chối nhầm = 8 retrieval miss, 10 một phần bằng chứng, 4 đủ bằng chứng;
12/22 có keyword ở hạng 6–10 bị cắt khỏi context top-5.

### B5 — Thăm dò context 10 chunk (exploratory) — A đóng 2026-10-24

`reports/phase_8_probe_context_top10_2026_10_24.md`: keyword đáp án trong context 0,853 → 0,918 (case
đủ keyword 78,5% → 87,3%; comparative 44% → 72%); token prompt ×1,77. 22 từ chối nhầm với context 10:
còn 12/22 từ chối, 0 lỗi citation. Chưa chấm điểm; n=22 chọn theo lỗi. Tiền 0,005 USD. Input cho
brainstorm Phase 8 (H4), không phải quyết định. `settings.yaml` không đổi.

### B6 — Phase 7B Gate 4 report baseline — C review: `ready_for_user_confirmation` (chờ phần User)

`reports/phase_7b_gate_4_baseline_implementation_2026_10_24.md`; review
`reports/phase_7b_review_2026_10_24.md` (C chạy lại mọi số: khớp; 3 minor).

### B7 — Sửa 3 minor của C5 ngay; phần User khi User chấm xong (free)

**Trạng thái (B):** m1–m3 đã sửa trong report Gate 4 (§3, §5, §5.1, §6); phần User chờ User chấm.

- Ngay: m1 (§5.1: retrieval tất định — cái chưa biết là chênh native vs runtime có vượt biến thiên
  do mẫu 158 case không), m2 (§3 thay placeholder `<rerun_30>` bằng cách lấy từ `subsets.json`), m3
  (§6 ghi quota Claude Code ~1,1M token cho judge Claude).
- Khi A nhắn User đã chấm: `parse-user-scores` → `user_scores.jsonl`; `compare` User–Claude, User–luna
  trên 20 case; điền §5 report; nếu Claude lệch User có hệ thống (chênh TB ≥1 ở một metric) thì báo A
  trước (spec §4.4). Nhắn A; C kiểm lại phần User.

## Việc của C

### C1 — Rà soát lựa chọn Phase 2–6 cho Phase 8 — A đóng 2026-10-24

Report `reports/phase_8_candidate_hypotheses_2026_10_24.md` (A kiểm O3, O5, O8 với code: đúng;
không lộ Golden). Dùng làm input brainstorm Phase 8 sau baseline 7B. Câu hỏi §5.1 (trả lời
một phần vs từ chối cả câu) là quyết định của User → đưa vào brainstorm Phase 8. Cột "Cách làm
phổ biến" cập nhật nguồn khi có kết quả ChatGPT.

### C2 — Danh sách dọn sau Phase 7 — A đóng 2026-10-24

`reports/phase_7_cleanup_inventory_2026_10_24.md`: đích, người tham chiếu, ràng buộc thứ tự (đợi
B2 chép metric; sửa `settings.yaml` + `settings_loader` cùng lúc; giữ
`knowledge-base-hue/foods/evaluation/golden_full_corpus_authoring.jsonl`). A trình User trước khi
xóa (sau khi 7B đóng).

### C3 — Claude judge 7B Gate 3 — A đóng 2026-10-24

`reports/phase_7b_gate_3_claude_judge_implementation_2026_10_24.md`: 39 sub-agent, 0 lỗi, không paid.
A kiểm: `score_errors` rỗng cả 3 file; đọc ngẫu nhiên 6 feedback — bám đáp án tham chiếu, không thấy
kiến thức ngoài. Số tổng hợp (A chạy `compare`): Claude chấm lại 30 lệch ≤1 ở 100%; Run 1 vs Run 2
chênh TB ≤0,011 mọi metric; Claude vs luna trùng 89–96%, lệch ≤1 ở ≥99,4%.

### C5 — review chéo Gate 4 — xong: `ready_for_user_confirmation` (điều kiện: phần User)

### C6 — kiểm lại phần User của report Gate 4 khi B báo

## Đang chờ User

- Gửi ChatGPT hai file trong `gửi chatgpt/tìm thông tin/`:
  `phase_7b_rag_evaluation_2026_10_24.md`, `phase_8_retrieval_improvements_2026_10_24.md`.
- Quyết định Phase 8 (khi brainstorm): trả lời phần có căn cứ hay từ chối cả câu (C1 §5.1, H8).
- Duyệt danh sách dọn C2 (xóa code/test/notebook Foods, 2 collection Foods).
- Chấm tay 20 case 7B: **file sẵn sàng** `data/evaluation/phase_7b/user_scoring.md` (private; ghi `Điểm: Đúng / Đủ / Trúng ý` mỗi câu).
