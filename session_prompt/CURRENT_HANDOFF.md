# CURRENT_HANDOFF — việc đang mở của A/B/C

Cập nhật: 17:10 24/10/2026 (A, kết phiên). Cách dùng: `WORKFLOW.md` §3, §6, §7, §9. Chỉ giữ việc
đang mở; việc xong ở `PROJECT_HISTORY.md` và `report_agent/<đợt>/TONG_HOP.md`.

## PHIÊN SAU — ĐỌC TRƯỚC NHẤT

**Hệ thống lúc kết phiên 24/10:** `main` (A commit cuối ghi trong `sessions/STATUS_A.md`); chatbot
full-corpus chạy được (`/health` 200 ở B1); Qdrant trước khi B9 xóa: 3 collection (kiểm lại bằng
`curl -s http://127.0.0.1:6335/collections` — B9 có thể đã xóa 2 collection Foods, xem `STATUS_B.md`).
**Working tree có thay đổi CHƯA COMMIT của B9** (xóa code/test/notebook Foods, sửa `settings.yaml`,
`settings_loader.py`, `conftest.py`, `vectorstore/*`, `scoring/bm25.py`, test chunker): chưa review —
**không commit, không revert** trước khi C review.

**Thứ tự việc phiên sau:**

1. Mở A/B/C bằng `START_SESSION.md`; A `ListAgents` cập nhật bảng Session; A **hỏi lại User quyền
   phiên** (quyền đặc biệt 24/10 đã hết hạn — `WORKFLOW.md` §9.8): tự điều phối rộng, trần tiền
   `gpt-6-luna`, commit/push.
2. **C review B9** (dọn) theo `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2) + report B
   `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md` + skill
   `risk-gated-agent-review`; chạy lại phần kiểm then chốt (so byte retrieval, test full-corpus,
   `/health`). Đạt → A commit theo từng đường dẫn (`git diff --cached --stat`), cập nhật
   `Project_Status.md` §4 (Qdrant còn 1 collection, code Foods đã gỡ), `bao_cao_he_thong/` (4 chỗ,
   `WORKFLOW.md` §6). B9 dở → B làm nốt trước.
3. **Brainstorm Phase 8 với User** (A, skill `propose-options`, mỗi lần một câu). Input:
   - giả thuyết + thứ tự ưu tiên: `reports/phase_8_candidate_hypotheses_2026_10_24.md` §8.4;
   - baseline 7B: `bao_cao_he_thong/BAO_CAO_DANH_GIA.md`, `guides/full_corpus_rag.md` "Cập nhật Phase 7B";
   - từ chối nhầm: `reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`;
   - thăm dò context 10: `reports/phase_8_probe_context_top10_2026_10_24.md`;
   - nghiên cứu: `gửi chatgpt/2026-10-24/kết quả nghiên cứu/` (2 file, private).
   Kết quả: **một** spec Phase 8 trong `docs/superpowers/specs/`, User duyệt một lần; mở đợt
   `report_agent/<ngày>_phase_8_<chủ_đề>/`.
4. Việc nhỏ có thể giao song song khi rảnh (free): đưa 9 file `bao_cao_he_thong/BAO_CAO_*.md` về mẫu
   mới (`TEMPLATE_USER_REPORT.md`: dòng "Cập nhật lần cuối … bản N", Tóm tắt đầu file, checklist thang
   5 mức, mã nội bộ xuống Phụ lục) — B các file B viết, C các file C viết, A 2 file của A.

## Câu hỏi cho User (phiên sau)

1. **Quyền phiên:** tiếp tục cho A tự điều phối rộng + commit/push? Trần tiền `gpt-6-luna` cho phiên?
   (24/10: ≤1 USD, đã dùng ~0,09 USD.)
2. **Phase 8 — H8:** khi chỉ có bằng chứng cho một phần câu hỏi, bot **trả lời phần có căn cứ (nói rõ
   phần thiếu)** hay **từ chối cả câu** như hiện nay? (Spec umbrella §1/Decision #6a cho phép trả phần
   có căn cứ; spec Phase 6 §10 + prompt hiện tại bắt từ chối cả câu.)
3. **Phase 8 — Golden:** có tách 176 câu thành nhóm phát triển / nhóm giữ kín để chấm cuối không? (C7:
   tối ưu và báo trên cùng bộ là đo lạc quan; spec 7A §8 từng chốt không chia; MekongAI dùng bộ kiểm
   cuối "chưa ai thấy", chấm mù.)
4. **Phase 8 — luật so sánh:** dùng paired bootstrap / permutation trên cùng 176 câu (nghiên cứu 7B
   khuyên), không đặt ngưỡng cố định — User đồng ý?
5. **Phase 8 — thứ tự làm:** đồng ý thứ tự C7 §8.4 (0 đo candidate recall + bằng chứng chuẩn → 1 context 10
   + H8 → 2 bảng/BM25 bigram/tách câu hỏi → 3 gộp chunk → 4 reranker → 5 phần có phí)?
6. Chunker có 3 cặp đoạn lặp nội dung (blockquote trong list item) — sửa cùng đợt chunker Phase 8?
7. **Phase 8 — bằng chứng chuẩn:** gắn tay đoạn/dòng đúng cho 30–40 câu khó (để đo "đoạn đúng có
   vào nhóm ứng viên không", C7 §8.4 bước 0)? Tốn công người (agent soạn, User duyệt mẫu).
8. Model/dependency mới cần duyệt khi đề xuất: reranker `bge-reranker-v2-m3`, `Qwen3-Embedding-0.6B`,
   tách từ `pyvi` (C7).

## Session

| Vai | Terminal (24/10) | Agent | Liên lạc | Việc phiên sau | Trạng thái kết phiên |
|---|---|---|---|---|---|
| A — điều phối | `hue-rag-77` | Claude Opus 5.5 | trực tiếp | hỏi quyền; commit B9 sau review; brainstorm Phase 8 | kết phiên |
| B — thực thi | `hue-rag-64` | Claude Opus 5.5 | trực tiếp | làm nốt B9 nếu dở; sửa minor review; báo cáo khâu theo mẫu mới | xem `STATUS_B.md` |
| C — thực thi | `hue-rag-d9` | Claude Opus 5.5 | trực tiếp | review B9; báo cáo khâu theo mẫu mới | xem `STATUS_C.md` |

Tên terminal đổi mỗi lần mở: dùng `ListAgents`. Cả ba Claude Code ⇒ liên lạc `trực tiếp`.

## Quyền

- **Thường trực:** A commit/push `origin main`; B/C không commit; duyệt cho A = duyệt cho B/C;
  Qdrant chỉ đọc trừ đích ghi trong việc; paid ghi usage token + tiền trong report.
- **Phiên 24/10 (đã hết hạn khi kết phiên, hỏi lại — §9.8):** A tự điều phối/thử nghiệm/tối ưu rộng;
  ngân sách `gpt-6-luna` ≤1 USD (tối đa 1,5) — dùng ~0,09 USD; User duyệt dọn B9 (đích C2). **B9 đã
  được duyệt trong phiên 24/10** — làm nốt phần dở ở phiên sau không cần xin lại, trong đúng đích C2.
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

- Phiên sau: review B9 (mục "Phiên sau" bước 2). Báo cáo khâu theo mẫu mới (bước 4).

## Việc của A

- Phiên sau: bước 1–3 mục "Phiên sau". Viết spec Phase 8 sau brainstorm.
