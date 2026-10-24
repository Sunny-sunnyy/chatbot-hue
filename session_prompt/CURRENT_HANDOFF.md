# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 19:25 24/10/2026 (A; User vắng, ủy quyền A tự điều phối). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc
đang mở; việc xong ở `PROJECT_HISTORY.md` và `report_agent/<đợt>/TONG_HOP.md`.

## PHIÊN TỐI 24/10 — ĐANG LÀM (đọc trước nhất)

**Hệ thống lúc mở phiên (18:51):** `main` @`54670a0`; Qdrant `:6335` chạy lại, đúng 3 collection
(Foods 572/572, full-corpus 8.459); working tree = phần B9 dở (55 thay đổi, chưa commit, chưa review);
mốc so byte `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl` sha `cefb2d1a…` còn;
`/tmp/phase7_cleanup/` đã mất. File untracked `báo cáo nghiên cứu github.txt` ở gốc là của User — giữ nguyên.

**User chốt 19:00 24/10:**
- Phase 8 tách **8.1 rồi 8.2** (tên 8.1/8.2 để khỏi nhầm với model "8B"). **8.1** = Claude rà lại các
  quyết định Phase 0–7 (trước đây do AGY/Codex làm): cái gì chưa thử, chưa so sánh, chưa tối ưu, chưa
  làm; đề xuất phương pháp/hướng cải tiến + thực nghiệm so sánh, **giữ phương án cũ làm baseline**; 8.1
  không đổi hành vi chatbot. User đóng 8.1 → A mới brainstorm + thiết kế **8.2** (cải tiến) trên số đo 8.1.
- B9 làm nốt + C review **song song** với brainstorm 8.1.

**Thứ tự việc:**

1. **B làm nốt B9** (mục "Việc của B", report §6 bước 1–4) → nhắn A → **C review B9** + chạy lại kiểm
   sức khỏe toàn hệ thống (như B1 `reports/phase_7b_gate_0_health_audit_2026_10_24.md`, free) trên hệ
   thống đã dọn. Đạt → A commit từng đường dẫn, cập nhật `Project_Status.md` §4 + `bao_cao_he_thong/`
   (4 chỗ, `WORKFLOW.md` §6) → Phase 7 sạch.
2. **A brainstorm 8.1 với User** (skill `propose-options`, mỗi lần một câu) → **một** spec 8.1 trong
   `docs/superpowers/specs/`, User duyệt; mở đợt `report_agent/<ngày>_phase_8_1_<chủ_đề>/`. Input:
   `reports/phase_8_candidate_hypotheses_2026_10_24.md` (H1–H14, §8.4), `bao_cao_he_thong/BAO_CAO_*.md`,
   `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`, `reports/phase_8_probe_context_top10_2026_10_24.md`,
   `gửi chatgpt/2026-10-24/kết quả nghiên cứu/`.
3. Rảnh (free, không chồng file B9): C đưa 4 báo cáo khâu của C về `TEMPLATE_USER_REPORT.md`.

## Câu hỏi cho User (đưa vào brainstorm 8.1/8.2, mỗi lần một câu)

1. ~~Quyền phiên~~ — đã trả lời 19:00 (mục Quyền).
2. **H8:** khi chỉ có bằng chứng cho một phần câu hỏi, bot **trả lời phần có căn cứ (nói rõ phần
   thiếu)** hay **từ chối cả câu** như hiện nay? (Spec umbrella §1/Decision #6a cho phép trả phần có căn
   cứ; spec Phase 6 §10 + prompt hiện tại bắt từ chối cả câu.)
3. **Golden:** tách 176 câu thành nhóm phát triển / nhóm giữ kín để chấm cuối? (C7: tối ưu và báo trên
   cùng bộ là đo lạc quan; spec 7A §8 từng chốt không chia.)
4. **Luật so sánh:** paired bootstrap / permutation trên cùng 176 câu, không ngưỡng cố định?
5. **Thứ tự 8.2:** quyết sau khi có số đo 8.1 (C7 §8.4 là đề xuất ban đầu).
6. Chunker 3 cặp đoạn lặp nội dung (blockquote trong list item) — 8.1 đo, 8.2 sửa?
7. **Bằng chứng chuẩn:** gắn tay đoạn/dòng đúng cho 30–40 câu khó (agent soạn, User duyệt mẫu)?
8. Model/dependency mới cần duyệt khi đề xuất: reranker `bge-reranker-v2-m3`, `Qwen3-Embedding-0.6B`,
   tách từ `pyvi` (C7).
9. (A tự quyết, báo User) `backend/test.ipynb`, `backend/scripts/` (ngoài C2); phát hiện B8 (test còn
   mock, `logging.basicConfig`, nhánh CUDA Qwen-0.6B) — A xếp vào 8.1 phần dọn code.

## Session

| Vai | Terminal (tối 24/10) | Agent | Liên lạc | Việc | Trạng thái |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-47` | Claude Opus 5.5 | trực tiếp | điều phối; brainstorm 8.1; commit B9 sau review | đang làm |
| B — thực thi | `hue-rag-b0` | Claude Opus 5.5 | trực tiếp | làm nốt B9 | đang làm |
| C — thực thi | `hue-rag-a3` | Claude Opus 5.5 | trực tiếp | C9 review B9 (khi B nhắn) | C10 (`c57ec43`), C11, C12 đạt (A 19:55); C11/C12 chờ commit; C9 chờ B |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit; duyệt cho A = duyệt cho B/C;
  Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report.
- **Phiên tối 24/10 (User 19:00, hết hạn khi kết phiên — §9.8):** A tự điều phối rộng; A commit/push;
  ngân sách API trả phí ≤1 USD cho phiên. **B9 đã được duyệt 24/10** — làm nốt trong đúng đích C2.
- Giá `gpt-6-luna`: 0,1 USD / 1M token vào, 0,5 USD / 1M token ra.

## Việc của B

### B9 — Dọn sau Phase 7 (User duyệt 2026-10-24: "không còn cần thiết, xoá mà hệ thống vẫn chạy bình thường thì xoá")

Mức rủi ro: cao (xóa code + 2 collection). Đích = `reports/phase_7_cleanup_inventory_2026_10_24.md`
(C2) §2.1–2.5, §2.6 dòng `data/full_corpus_metadata_v2_*`, §2.7 `requirements.txt`; theo ràng buộc §3.

- **Trước khi xóa — tiêu chí ghi trước + mốc so sánh (free):** lưu output hiện tại của
  `full_corpus_eval retrieval --treatment dense_bm25_rrf` (đã có `retrieval_dense_bm25_rrf_1.jsonl`)
  làm mốc; sau dọn chạy lại phải **giống từng byte**. Liệt kê lại Qdrant collections; khác
  {2 Foods + 1 full-corpus} thì dừng.
- **Làm (một lượt code, rồi Qdrant):**
  1. Gỡ code/test/notebook/settings Foods theo C2 §2.2–2.5 (sửa `settings.yaml` + `settings_loader.py`
     cùng lúc; xóa module Foods cùng fixture Foods trong `conftest.py`; giữ `vector_database.url/timeout`;
     xóa `evaluation/{eval,evaluator,test,template,golden_dataset,retrieval_comparison,*_benchmark}.py`
     + 2 CSV; `embedding/dense_benchmark.py`). Notebook: xóa 02, 05, 07, 08a, 08b, 08c; sửa markdown 03,
     06; sửa notebook 04 (chỉ candidate có build record, sample id như `full_corpus_pipeline.py`) và Run
     All trên bản tạm (Qdrant chỉ đọc), outputs rỗng trong repo. Xóa `requirements.txt`.
  2. Sửa test chunker so với artifact 8.460 cũ (`test_full_corpus_chunker.py:984-996`) để so với số
     hiện hành hoặc bỏ phần so artifact — không đổi chunker.
  3. Kiểm (C2 §5) + so byte retrieval + API in-process `/health` 200 + 1 retrieval; smoke 10
     `generate --golden smoke` (paid ≤0,005 USD) để chắc đường sinh còn chạy.
  4. Đạt hết mới xóa 2 collection Foods (`hue_foods_e5_small_384`, `hue_foods_e5_small_384_dense`),
     liệt kê trước/sau. Xóa `data/full_corpus_metadata_v2_*.json` (5 file, liệt kê trước).
- **Không làm:** đụng `knowledge-base-hue/` (giữ Golden Foods V2/V3 và
  `foods/evaluation/golden_full_corpus_authoring.jsonl`); sửa chunker (overlap để Phase 8); sửa
  governance `session_prompt/` (A làm); `phase6_live_smoke.py`, `full_corpus_smoke.py` (C2 §4, giữ).
- **Quyền:** Qdrant xóa đúng 2 tên trên; paid ≤0,005 USD; không commit. Bị permission chặn `rm`/xóa
  Qdrant thì dừng, nhờ User chạy bằng `!` trong terminal B.
- **Dừng:** byte so retrieval khác; test full-corpus fail; API không lên.
- **Đầu ra:** `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` (danh sách
  xóa/sửa, lệnh kiểm + kết quả); `STATUS_B.md`; nhắn A → C review.

## Việc của C

### C9 — Review B9 + kiểm sức khỏe sau dọn (khi B nhắn "B9 xong")

- Đọc: `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2) §2–§5 full-read; report B
  `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` full-read; skill
  `risk-gated-agent-review`.
- Làm: cổng tối thiểu (exact diff mọi đường dẫn, đối chiếu đích C2 + ràng buộc §3, tìm ngoài phạm vi,
  `git diff --check`); chạy lại độc lập: so byte retrieval với mốc, pytest full-corpus free (liệt kê
  file, không `--deselect`), `/health` 200 + 1 retrieval, `golden_full_corpus check`, Qdrant liệt kê
  (còn đúng 1 collection full-corpus 8.459 sau khi B xóa). Kiểm sức khỏe như B1 (corpus 205/8.459,
  build record fresh, sparse state, payload 7 field) trên hệ thống đã dọn.
- Không: sửa code B9 (finding → B sửa); paid (smoke 10 của B là đủ); commit.
- Đầu ra: `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_review.md` (`TEMPLATE_REVIEW.md`),
  kết luận `ready_for_user_confirmation` / `changes_requested` / `blocked`; `STATUS_C.md`; nhắn A.

### C10 — 4 báo cáo khâu của C về mẫu mới (free, làm trong lúc chờ B)

- File: `bao_cao_he_thong/BAO_CAO_{TIM_KIEM,SINH_CAU_TRA_LOI_API,BO_CAU_HOI_GOLDEN,KHO_DU_LIEU}.md`
  theo `session_prompt/TEMPLATE_USER_REPORT.md` (dòng "Cập nhật lần cuối … bản N", Tóm tắt đầu file,
  checklist thang 5 mức, mã nội bộ xuống Phụ lục). Không đổi nội dung kỹ thuật/số đo; không chép số
  liệu corpus. Khai báo file trong `STATUS_C.md`. Xong → nhắn A (A review).

### C11 — Bảng rà quyết định Phase 0–7 (đầu vào spec 8.1; chỉ đọc, free)

A giao 19:25 24/10 (User ủy quyền A tự điều phối). **Ưu tiên C9 khi B nhắn**: dừng C11 ở điểm gọn,
làm C9, rồi quay lại.

- Mục tiêu: liệt kê **mọi quyết định kỹ thuật đang hiệu lực** của Phase 0–7 (do AGY/Codex làm trước
  đây) và bằng chứng đứng sau nó, để User biết cái gì chưa thử / chưa so sánh / chỉ đo trên Foods /
  mặc định không lý do. Phương án cũ = baseline.
- Vùng: (0–1) format curated Markdown, data flow; (2) chunker, tokenizer, overlap, bảng; (3) dense
  model, tiền tố, BM25/tokenize, sparse state; (4) Qdrant schema, HNSW/exact, sparse modifier/IDF,
  payload; (5) retrieval treatment, pool 30, RRF k=60, top-10, reranker; (6) context 5 chunk, thứ tự,
  prompt, từ chối, citation, model/tham số sinh, API/UI; (7/7A) Golden: cách soạn, cỡ, phân loại,
  keyword, smoke; (7B) evaluator: metric, judge, thang, so sánh. Thêm vùng nếu gặp.
- Mỗi dòng: quyết định · giá trị hiện tại (`file:dòng`) · ai/khi nào chốt (spec/report) · phương án
  từng xem xét · **bằng chứng**: đo trên gì (full-corpus 176 / Foods 45 / probe 1 case / không đo) +
  metric + kết quả · trạng thái (`so sánh trên full-corpus` / `chỉ đo trên Foods` / `chưa so sánh` /
  `mặc định không lý do` / `bị ép bởi ràng buộc đã hết`) · tác động ước (cao/vừa/thấp, vì sao) ·
  thí nghiệm đề xuất (đổi một thứ, baseline, metric, free/paid ước USD, cần model/dependency mới?).
- Dùng lại, không làm lại: `reports/phase_8_candidate_hypotheses_2026_10_24.md` (H1–H14, O1–O11) —
  trỏ mã H; nghiên cứu `gửi chatgpt/2026-10-24/kết quả nghiên cứu/` (2 file). Nguồn: `Project_Status.md`
  §5, `docs/superpowers/specs/` (targeted), `PROJECT_HISTORY.md` (targeted), code, `bao_cao_he_thong/`.
- Không: sửa code/config/corpus/Golden; paid; ghi Qdrant; chép corpus/câu Golden vào report; đề xuất
  kiến trúc Phase 9.
- Đầu ra: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md` — bảng theo
  vùng + mục cuối "10 chỗ đáng lo nhất" (xếp theo tác động × độ thiếu bằng chứng) + "cần nghiên cứu
  ngoài" (câu hỏi cho ChatGPT, A gộp vào yêu cầu nghiên cứu). `STATUS_C.md`; nhắn A.

**C11 xong 19:26, A review 19:50: đạt** (kiểm lại độc lập 5 điểm then chốt: loader ép tổ hợp
`settings_loader.py:39-44`; prompt thiếu 2 luật spec Phase 6 §10; chunker bản đầu gộp 3.318 chunk;
amendment 10-01 §5 "Qwen là benchmark bắt buộc ở Phase 8"; `exclude_files` chỉ 2 inventory travel).
Câu hỏi §7 đã gộp vào yêu cầu ChatGPT (mục F).

### C12 — Sửa 4 lỗi trong báo cáo cũ của C (C11 §6 mục 13; free, nhỏ)

- `bao_cao_he_thong/BAO_CAO_BO_CAU_HOI_GOLDEN.md` §2 (gộp **không xáo**), `BAO_CAO_TIM_KIEM.md` §3
  (MiniLM chỉ thử trên Foods), `BAO_CAO_SINH_CAU_TRA_LOI_API.md` §5 (Representation B đã gọi live 1 lần,
  chưa có index) — tăng "bản N", ghi một dòng ở §4 lịch sử. `reports/phase_8_candidate_hypotheses_2026_10_24.md`
  H6/O9: thêm ghi chú đính chính (Foods 08b "dense+BM25" là weighted 0,6/0,4, không phải RRF), không viết lại.
- Câu "bàn khi brainstorm Phase 8" trong 4 báo cáo khâu → "Phase 8.1". Không đổi số đo khác.
- Khai báo trong `STATUS_C.md`; xong nhắn A. C9 vẫn ưu tiên khi B nhắn.

## Việc của A

- Brainstorm 8.1 với User → spec 8.1; commit B9 sau C9 đạt; C10 đã review + commit `c57ec43`.
- Yêu cầu nghiên cứu ChatGPT cho 8.1: `gửi chatgpt/2026-10-24/tìm thông tin/phase_8_1_decision_audit_2026_10_24.md` (User relay).
