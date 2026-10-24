# STATUS C — cập nhật 2026-10-24 21:25

Terminal: `hue-rag-a3` (tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm
- C19 (21:22, A giao): review B13 — xong 21:25: ready_for_user_confirmation, 1 minor (hòa ở biên pool). `phase_8_1_b13_review.md`.
- C20 (A giao 21:25): review mù lần 2 câu kín (11 dòng đổi) bằng sub-agent mới khác — đang làm. A đang hỏi User về 9 câu kín trùng Golden; người sửa là sub-agent mới (A và C vẫn mù câu kín).
- A commit `b8dbe95` (21:14): B11 + C16 + report/review. A quyết: mốc native G1.3 = lượt hôm nay; tham số `chunks` giao khi mở G3.
- C18 (A giao 21:05): review B11 — xong 21:12: ready_for_user_confirmation, 2 minor; A quyết mốc native (khác 7B 6/158, không do code) và lối vào `chunks` trước G3. `phase_8_1_g0_5_review.md`.
- C17 (A giao 21:05): review G0.4 36 câu kín qua **sub-agent mới** — C giữ mù — xong 21:17: changes_requested (9/36 trùng ý Golden, 1 mơ hồ); mẫu 17 dòng cho User ở `phase_8_1/sealed_user_sample.md` (private). Report `phase_8_1_g0_4_sealed_review.md`.
- C16 (A giao 20:52): G0.1 split 120/56 + G0.2 thống kê evaluator — xong 21:03, **B review đạt** (3 minor đã sửa 21:12). Đối chứng âm PASS (Run1 vs Run2 mọi metric no_difference), dương PASS (xáo top-10 → MRR/nDCG worse), retrieval mặc định giống byte, 27 test pass, 0 USD. Report `phase_8_1_g0_1_2_measure_implementation.md`.
- C15d (A giao 20:47): gỡ tên/số đo/đường dẫn dự án khác khỏi `phase_8_1_spec_review.md` (repo public) — xong 20:48; grep -i mekong trong đợt 8.1 = 0. Kết luận review giữ nguyên.
- C15c (A giao 20:38): kiểm nhanh spec 8.1 v4 — xong 20:40: ready_for_user_confirmation; 5 ghi chú minor n1–n5 (sửa chữ). Review §8.
- C15b (A giao 20:27): kiểm lại spec 8.1 v2 — xong 20:28: M1, M2, m1–m10 đóng; còn r1–r3 minor (sửa chữ) → ready_for_user_confirmation sau khi A bổ sung.
- C15 (A giao 20:22): review spec 8.1 nháp của A — xong 20:25: **changes_requested** (2 major: M1 thí nghiệm cần thêm tham số vào code production/sparse state riêng; M2 xác nhận 56 câu kiểm cho metric đoạn đúng; 10 minor). `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_spec_review.md`.
- C13 (A giao 19:55): cập nhật TIM_KIEM + KHO_DU_LIEU theo hiện trạng sau B9 (commit `1832201`) — xong 19:58, **A review đạt** (TIM_KIEM bản 4, KHO_DU_LIEU bản 3).
- C13b (A giao): SINH §5 số dòng settings.yaml sau B9; GOLDEN Phụ lục lệch → đã xử lý — xong 20:00, **A review đạt** (cả hai lên bản 4).
- C14 (A giao 20:01): WebFetch kiểm nguồn nghiên cứu ChatGPT 8.1 — xong 20:07, **A review đạt** (chưa commit): 22/29 nguồn kiểm, 16 khớp, 5 khớp một phần/lệch, 1 không kiểm trọn; Qdrant 1.18.3. Free.
- C10 (A giao 19:00, User duyệt): 4 báo cáo khâu của C về `TEMPLATE_USER_REPORT.md` — xong 19:08, **A review đạt, commit `c57ec43`**. Bản 2 mỗi file: Tóm tắt đầu file, checklist 5 mức, §4 lịch sử theo ngày, mã nội bộ/spec/report xuống Phụ lục; số đo giữ nguyên (kiểm: mọi số trong diff đã có ở bản 1, trừ giờ/tỉ giá/commit và "~600 đồng" = 0,024 USD × 25.000). `git diff --check` sạch.
- C12 (A giao): sửa 4 lỗi báo cáo cũ (C11 §6 mục 13) + "brainstorm Phase 8" → "Phase 8.1" — xong 19:33, **A review đạt** (chưa commit — commit A chờ User). 3 báo cáo khâu lên bản 3 (Golden §2 không xáo; Tìm kiếm MiniLM chỉ Foods + câu brainstorm → 8.1; Sinh §5 Representation B đã gọi 1 lần); H-report thêm §9 đính chính H6/O9. Số đo không đổi; `git diff --check` sạch.
- C9 review B9 + kiểm sức khỏe: xong 19:54 — **ready_for_user_confirmation**, 0 blocker/major, 1 minor (m1 câu tả case 81), 3 ngoài phạm vi cho A (o1 tài liệu còn nhắc Foods, o2 dependency không dùng, o3 test.ipynb/scripts). Review `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_review.md`. Chạy lại: pytest 191 passed; retrieval giống byte (cefb2d1a); /health 200; payload 8.459×7 field; Qdrant 1 collection; Golden check; notebook 03/04. Không paid.
- C11 (A giao 19:25): bảng rà quyết định Phase 0–7B — xong 19:30, **A review đạt** (chưa commit — commit A chờ User): `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md` (56 quyết định; 3 sub-agent gom dữ kiện, C kiểm điểm then chốt §1.1). Free, không paid. Phát hiện lỗi trong báo cáo cũ của C (§6 mục 13) — chờ A giao sửa.

## Đang khai báo sửa
- `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g0_4_sealed_review.md` (C20, thêm §2 lần 2); sub-agent ghi lại private `phase_8_1/sealed_user_sample.md` + notes

## Phiên sau
1. **Review B9 (dọn sau Phase 7)** khi A nhắn — skill `risk-gated-agent-review`; đối chiếu đích với
   `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2) §2 và ràng buộc §3: chỉ xóa `eval.py` sau khi
   `full_corpus_eval.py` không còn import `evaluation.eval`; sửa `settings.yaml` + `settings_loader.py`
   cùng lúc (giữ `vector_database.url/timeout`); **giữ**
   `knowledge-base-hue/foods/evaluation/golden_full_corpus_authoring.jsonl`; xóa module Foods cùng
   fixture Foods trong `conftest.py`; Qdrant còn đúng 1 collection full-corpus sau khi xóa 2 collection
   Foods (liệt kê trước/sau). Kiểm theo C2 §5 (pytest full-corpus không paid, import 3 lối vào +
   `load_settings`, `/health` 200, `golden_full_corpus check`, grep tên đã xóa). Review ghi vào
   `report_agent/<đợt>/…_review.md` (WORKFLOW §6 mới), không vào `reports/`.
2. **Input brainstorm Phase 8:** `reports/phase_8_candidate_hypotheses_2026_10_24.md` §8.4 (thứ tự mới:
   đo pool/gold → context 10 + trả lời một phần → bảng/bigram/tách câu → gộp chunk → reranker → paid).

## Vừa xong hôm nay (2026-10-24)
| Việc | Kết quả | Commit A |
|---|---|---|
| C1 giả thuyết Phase 8 | `reports/phase_8_candidate_hypotheses_2026_10_24.md` (H1–H14, O1–O11) | `1027ec3` |
| C2 danh sách dọn sau Phase 7 | `reports/phase_7_cleanup_inventory_2026_10_24.md` (đồ thị import AST, ràng buộc thứ tự) | `dba4881` |
| C3 Claude judge 7B Gate 3 | 39 sub-agent, 382 lượt chấm, 0 lỗi, không paid; `reports/phase_7b_gate_3_claude_judge_implementation_2026_10_24.md` | `1994ea5` |
| C5 review Gate 4 (B) | `reports/phase_7b_review_2026_10_24.md` — ready_for_user_confirmation có điều kiện; m1–m3 → B7 | `c1f4f20` |
| C7 nguồn cho giả thuyết Phase 8 | cột nguồn [R1]–[R11] + §8 (WebFetch 5 URL; thứ tự mới §8.4) | `a595e02` |
| C8 báo cáo khâu Phase 5, 6, 7/7A, 7A2 | `bao_cao_he_thong/BAO_CAO_{TIM_KIEM,SINH_CAU_TRA_LOI_API,BO_CAU_HOI_GOLDEN,KHO_DU_LIEU}.md`; minor m1 (bỏ số liệu corpus) đã sửa | `4426ed0` |

Paid đã dùng: **0 USD** (C chỉ chạy local/free; chấm Claude dùng quota Claude Code ~1,1M token).

## Script tạm ở /tmp (mất khi khởi động lại; không commit — viết lại được theo mô tả)
- `/tmp/c_probe/`: `chunk_stats.py` (phân bố token chunk), `retrieval_probe.py` (hạng chunk F2, đa dạng
  nguồn top-5), `chunk9.py`, `table_split.py` (bảng bị tách vì tokenizer nào), `imports.py` (đồ thị
  import AST từ 3 lối vào; dùng lại được cho review B9).
- `/tmp/c_judge/`: `batches.py` (`split` lô ≤10 giữ thứ tự; `merge` kiểm đủ case, số nguyên 1–5),
  `subagent_prompt.md`. Lô/điểm từng lô giữ ở `data/evaluation/phase_7b/claude_batches/` (private).
- `/tmp/c_review/`: output chạy lại `summarize`/`compare` cho C5.

## Đã học / bẫy gặp
- **Repo `chatbot-hue` là PUBLIC** (A 24/10): file tracked không chép tên, số đo, đường dẫn của dự án khác của User; chi tiết để ở ghi chú private `data/…` (không commit).
- Chạy script import `backend.*` từ **repo root** (`sys.path` = repo root); `full_corpus_pipeline.py`
  import tuyệt đối `backend.core`. Lệnh `evaluation.*` CLI chạy từ `backend/`.
- `knowledge-base-hue/foods/evaluation/` có cả Golden Foods cũ lẫn file authoring 7A đang dùng.
- `load_settings` bắt buộc `active_profile` ∈ `profiles` (Foods); `vector_database.url/timeout` vẫn được
  full-corpus dùng.
- Grep có brace-expansion `--exclude-dir={…}` kèm tên tiếng Việt bị safety check chặn → dùng nhiều
  `--exclude-dir=` riêng.
- Kiểm tuân thủ sub-agent: đọc transcript `tasks/*.output` chỉ lấy tên tool + `file_path`.
- Sub-agent judge chấm rất nhanh (8–34 s/10 case); độ tin đo bằng nhiễu/khớp (7B: lệch ≤1 ở 100%).
- File tracked (`bao_cao_he_thong/`, report): nhắc tên địa danh/chủ đề được, **không** chép số liệu,
  địa chỉ, giá từ corpus (minor m1 C8).
- Quy tắc mới (commit `0a709db`, WORKFLOW §6/§8): report mới vào `report_agent/<YYYY-MM-DD>_<chủ_đề>/`;
  báo cáo cho User ở `bao_cao_he_thong/`; giờ lấy bằng `date`; STATUS cập nhật ngay sau mỗi việc.
- ChatGPT: `gửi chatgpt/<YYYY-MM-DD>/{tìm thông tin,kết quả nghiên cứu}/`; đọc kết quả rồi WebFetch đối chiếu.
- B/C không dùng git để chuyển/xóa file (dùng `mv` thường); A commit. User: A giao = User giao.

## Câu hỏi / thắc mắc cho A/User
- **User quyết (Phase 8):** trả lời phần có căn cứ hay từ chối cả câu (spec umbrella §1/#6a vs spec
  Phase 6 §10 + prompt) — H8; B4/B5 cho thấy đây là nguồn chính của 22 từ chối nhầm.
- **User quyết (Phase 8):** có tách 176 câu thành phần thử / phần giữ kín không (spec 7A chốt không chia;
  thử và báo trên cùng bộ là đo lạc quan). A đã ghi vào "Đang chờ User".
- Phase 8 có gắn "bằng chứng chuẩn" (đoạn/dòng đúng) cho 30–40 câu khó không — công người, đề xuất ở
  §8.4 bước 0.
- Model/dependency mới (reranker bge-v2-m3, Qwen3-Embedding-0.6B, pyvi) cần User duyệt trước khi thử.
