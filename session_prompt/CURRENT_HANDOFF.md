# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 20:49 24/10/2026 (A). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc đang mở; việc xong
ở `PROJECT_HISTORY.md` và `report_agent/<đợt>/`.

## ĐANG LÀM — Phase 8.1 G0 (đọc trước nhất)

**Hệ thống:** `main`; chatbot full-corpus chạy được; Qdrant `:6335` (v1.18.3) còn **1** collection
`hue_full_corpus_7a2_e5_small_384` (8.459). B9 đã đóng (`1832201`). GPU GTX 1650 4 GB; `.venv` có torch
2.13+cu130 (`cuda.is_available()` True).

**Spec đang làm:** `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` — **approved**
20:49 24/10 (bản 4, gồm M1 `BAAI/bge-reranker-v2-m3`, M2 `AITeamVN/Vietnamese_Reranker`). full-read cho mọi
người làm 8.1. Đợt: `report_agent/2026-10-24_phase_8_1_ra_soat/`. Input: bảng rà C11
`phase_8_1_decision_inventory.md`, kiểm URL C14, nghiên cứu `gửi chatgpt/2026-10-24/kết quả nghiên cứu/`
(private), ghi chú private `data/phase_8_1/external_lessons_private.md`.

**Nguyên tắc thường trực (User 20:49):** được thực nghiệm, so sánh, thử — cả khi quay lại Phase trước; luôn
thử + đánh giá + so baseline trước khi chọn.

**Repo `chatbot-hue` PUBLIC:** không commit nội dung/số đo/đường dẫn của dự án khác của User; trước khi
nhắn A "xong", chạy `git diff | grep -i mekong` trên file mình sửa.

**Skill mới (User 21:00):** `practical-project-coding` có mục "Ranh giới theo khâu pipeline — dùng lại
được": B11 và harness 8.1 áp đúng luật này; khâu còn dính ngoài phạm vi ⇒ ghi vào report (G5 gom lại cho 8.2).
A sửa skill ⇒ B review khi xong B11.

**Thứ tự G0** (spec §5): B11 (G0.5) ‖ C16 (G0.1 + G0.2) chạy song song (file không chồng) → G0.3 đoạn đúng
(giao sau khi có file chia) ‖ G0.4 câu kín (A, sub-agent mới) → G0.6 khóa baseline → đóng G0 → G1.

## Câu hỏi còn mở cho User

- H8 (trả lời phần có căn cứ hay từ chối cả câu): 8.1 chỉ **thử** (G2); quyết ở 8.2 trên số đo.
- Trước quyết định 8.2 dựa vào điểm câu trả lời: nhắc lại đề xuất User chấm tay 20 câu (D6).
- 15 file đã commit từ trước còn nhắc tên MekongAI (tài liệu cách làm việc User cho học) — A đề xuất để
  nguyên; User chưa trả lời.

## Session

| Vai | Terminal (tối 24/10) | Agent | Liên lạc | Việc | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-47` | Claude Opus 5.5 | trực tiếp | điều phối 8.1; G0.4 câu kín; review | đang làm |
| B — thực thi | `hue-rag-b0` | Claude Opus 5.5 | trực tiếp | B11 (G0.5) | giao 20:49 |
| C — thực thi | `hue-rag-a3` | Claude Opus 5.5 | trực tiếp | C16 (G0.1 + G0.2) | giao 20:49 |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit; duyệt cho A = duyệt cho B/C;
  Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report; code luôn `uv run`
  trong `.venv` dự án; thư viện thừa giữ nguyên (chỉ gỡ khi xung đột).
- **Phiên tối 24/10 (User 19:00, hết hạn khi kết phiên — §9.8):** A tự điều phối rộng; ngân sách API ≤1 USD
  cho phiên (đã dùng ~0,0013 USD).
- **Spec 8.1 §8:** Qdrant tạo/ghi/xóa chỉ `hue_81_*`; paid chỉ `gpt-6-luna`, trần 0,5 USD cả 8.1; file private
  mới ở `knowledge-base-hue/evaluation/phase_8_1/` và `data/phase_8_1/`; M1/M2 tải về HF cache, chạy GPU fp32.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra.

## Việc của B

### B11 — G0.5: tham số mặc định-như-cũ cho code production (free)

- Đọc: spec 8.1 full-read (đặc biệt §3.1, §5 G0.5, §6); skill `practical-project-coding`.
- Làm: thêm **tham số keyword, mặc định = giá trị hiện tại** đúng ở các chỗ spec §3.1 liệt kê:
  - `backend/llm/generator_openai_full_corpus.py`: instructions của answer agent, reasoning effort (mặc định
    không truyền = như hiện nay);
  - `backend/retrieval/full_corpus.py`: pool (hằng 30), RRF k (60), `exact`/search params cho `query_points`
    (`:461-476`); `build_full_corpus_retrieval_service` nhận tên collection + đường build record + sparse
    state (`:723-750`), mặc định như cũ;
  - `backend/ingestion/full_corpus_pipeline.py`: tên collection, đường sparse state, danh sách tokenizer kiểm
    giới hạn (mặc định như cũ).
  Không đổi giá trị mặc định; không thêm key vào `settings.yaml`; không sửa loader; không thêm abstraction.
- Kiểm (gate G0.5): pytest 15 file full-corpus (liệt kê file, không `--deselect`) đạt; retrieval
  `dense_bm25_rrf` 176 câu giống từng byte mốc `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`
  (sha `cefb2d1a…`); `/health` 200 in-process; `git diff --check`. Không paid, không ghi Qdrant.
- Không: logic chia đoạn mới (nằm trong harness, việc sau); sửa evaluator (C16).
- Đầu ra: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g0_5_params_implementation.md`
  (`TEMPLATE_IMPLEMENTATION_REPORT.md`); `STATUS_B.md`; nhắn A + C (C review).

## Việc của C

### C16 — G0.1 file chia 120/56 + G0.2 sửa thước đo evaluator (free)

- Đọc: spec 8.1 full-read (§3.4, §5 G0.1–G0.2, §6); skill `practical-project-coding`.
- G0.1: chia `golden_full_corpus.jsonl` 176 câu thành 120 thử / 56 kiểm, phân tầng theo `category`, seed cố
  định, khóa nhận diện câu ổn định (ví dụ chỉ số dòng + hash câu hỏi); ghi
  `knowledge-base-hue/evaluation/phase_8_1/split.json` (private). Không sửa Golden chính thức. Smoke 10 nằm
  ở nhóm nào thì ghi ra.
- G0.2 trong `backend/evaluation/full_corpus_eval.py` (+ test logic thuần cần thiết):
  - `compare`: paired bootstrap 10.000 lần (CI 95% chênh trung bình) + thắng/hòa/thua, theo loại câu, lọc
    theo nhóm thử/kiểm; Holm khi >1 biến thể (tham số);
  - macro theo loại câu; bảng từ chối 2×2;
  - metric "bằng chứng trong 5 đoạn đưa model" (từ `context-coverage` sẵn có);
  - tự kiểm: **đối chứng âm** Run 1 vs Run 2 7B ⇒ CI chứa 0 ở mọi metric; **đối chứng dương** retrieval
    baseline vs xáo top-10 (seed cố định) ⇒ "kém hơn" ở MRR/nDCG.
- Không: sửa retrieval/generator/pipeline (B11); paid; ghi Qdrant.
- Đầu ra: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g0_1_2_measure_implementation.md`;
  `STATUS_C.md`; nhắn A + B (B review).

## Việc của A

- G0.4 **nháp xong 21:00**: sub-agent mới (không mở `evaluation/`, `meta/`, `data/`, report, inventory) viết
  `knowledge-base-hue/evaluation/phase_8_1/sealed_authoring.jsonl` (private, gitignored): 36 câu — direct_fact 14,
  multi_source 7, conditional 7, comparative 5, out_of_scope 3; 7 partition; không dấu 14 / văn nói 14 / lỗi gõ
  8. `check --authoring` exit 0 (A chạy lại). Sub-agent tự đánh dấu dòng 6 (nhãn conditional?), 22 (cần suy
  luận nhỏ về chu kỳ năm), 36 (multi_source nhưng 2 đoạn cùng file). A **không đọc nội dung** (giữ kín).
  **Chờ review chéo** — người xong việc G0 trước (B hoặc C): đối chiếu từng câu với `sources`, ba dòng đánh dấu,
  trùng ý với Golden 176; ghi `phase_8_1_g0_4_sealed_review.md` (không chép câu hỏi); rồi chọn ~10 câu cho
  User duyệt mẫu. Sau đó A tạo file chính thức 4 field (bỏ `partition`/`sources`) và khóa.
- Giao G0.3 (đoạn đúng ~40 thử + ~15 kiểm) khi C16 có file chia. Review B11/C16 sau review chéo; commit.
