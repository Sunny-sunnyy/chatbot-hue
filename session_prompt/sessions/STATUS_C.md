# STATUS C — cập nhật 2026-10-24 19:08

Terminal: `hue-rag-a3` (tên đổi mỗi lần mở) · Agent: Claude Opus 5.5 · Vai: thực thi

## Đang làm
- C10 (A giao 19:00, User duyệt): 4 báo cáo khâu của C về `TEMPLATE_USER_REPORT.md` — xong 19:08, **chờ A review**. Bản 2 mỗi file: Tóm tắt đầu file, checklist 5 mức, §4 lịch sử theo ngày, mã nội bộ/spec/report xuống Phụ lục; số đo giữ nguyên (kiểm: mọi số trong diff đã có ở bản 1, trừ giờ/tỉ giá/commit và "~600 đồng" = 0,024 USD × 25.000). `git diff --check` sạch.
- C9 review B9 + kiểm sức khỏe: chờ B nhắn "B9 xong".

## Đang khai báo sửa
- `bao_cao_he_thong/BAO_CAO_{TIM_KIEM,SINH_CAU_TRA_LOI_API,BO_CAU_HOI_GOLDEN,KHO_DU_LIEU}.md` (C10)

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
