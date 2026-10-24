# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 2026-10-24 (A, mở lại phiên). Cách dùng: `WORKFLOW.md` §3, §7, §9. Chỉ giữ
việc đang mở; việc xong chuyển tóm tắt sang `PROJECT_HISTORY.md`.

## Session

| Vai | Terminal | Agent | Liên lạc | Việc hiện tại | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-77` | Claude Opus 5.5 | trực tiếp | Điều phối Phase 7B | đang làm |
| B — thực thi | `hue-rag-64` | Claude Opus 5.5 | trực tiếp | B2 Phase 7B Gate 1 | chờ review A |
| C — thực thi | `hue-rag-d9` | Claude Opus 5.5 | trực tiếp | C3 Claude judge 7B Gate 3 | đang làm |

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

### B4 — Phase 7B Gate 4 chuẩn bị + chẩn đoán từ chối nhầm (free)

- **(a) Tổng hợp nhiễu và mức khớp** (spec 7B §4.4): thêm vào `full_corpus_eval.py` phần so hai
  file điểm theo `case_index` (chênh trung bình có dấu, tỉ lệ trùng, tỉ lệ lệch ≤1, tỉ lệ đổi ≥2,
  theo metric) + đọc điểm User từ `data/evaluation/phase_7b/user_scoring.md` qua
  `user_scoring_map.json` (`Điểm: a / c / r`). Test logic thuần. Chạy được ngay cho luna (Run 1 vs
  chấm lại 30); phần Claude/User chạy khi có file.
- **(b) Chẩn đoán 22 từ chối nhầm** (Run 1): mỗi case, keyword mang đáp án có nằm trong 5 chunk
  context không (`context_sources`, lấy lại context bằng retrieval local như `answer_case`, không gọi
  sinh)? Phân loại: *retrieval miss* (không có trong context) / *có bằng chứng nhưng model từ chối*
  (ứng viên H8 prompt tất-cả-hoặc-không) / *không rõ*. Bảng đếm theo category; không chép nội dung.
- **Không làm:** gọi paid; sửa runtime/prompt; đọc file điểm Claude trước khi C báo xong.
- **Đầu ra:** code + test; `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`; `STATUS_B.md`; nhắn A.

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

### C3 — chờ 7B Gate 3 (Claude judge, spec 7B §4.3)

## Đang chờ User

- Gửi ChatGPT hai file trong `gửi chatgpt/tìm thông tin/`:
  `phase_7b_rag_evaluation_2026_10_24.md`, `phase_8_retrieval_improvements_2026_10_24.md`.
- Quyết định Phase 8 (khi brainstorm): trả lời phần có căn cứ hay từ chối cả câu (C1 §5.1, H8).
- Duyệt danh sách dọn C2 (xóa code/test/notebook Foods, 2 collection Foods).
- Chấm tay 20 case 7B: **file sẵn sàng** `data/evaluation/phase_7b/user_scoring.md` (private; ghi `Điểm: Đúng / Đủ / Trúng ý` mỗi câu).
