# C34 — rà code luồng trả lời + đánh giá (chỉ đọc) — **DỞ**

Người làm: C (Claude Opus 5.5, terminal `hue-rag-d6`) · 2026-10-25 17:06 (`date`) · Việc: C34 (A giao 16:58), dừng vì User kết phiên 17:0x ·
Rà trên `main` `bc568f1` · 0 USD.

**DỞ.**
- **Đã rà:** `retrieval/full_corpus.py` (đủ), `retrieval/full_corpus_context.py`, `llm/generator_openai_full_corpus.py`,
  `llm/openai_tokenizer.py`, `llm/citations.py`, `llm/full_corpus_prompt.py`, `api/app.py`, `api/routes/chat.py` (phần xử lý lỗi);
  `evaluation/full_corpus_eval.py` (sơ đồ hàm, ai gọi, các hàm so cặp); `evaluation/golden_full_corpus.py` (vai trò).
- **Chưa rà:** `frontend/`, `reranking/cross_encoder.py`, `llm/evidence_recorder.py`, `llm/phase6_live_smoke.py`,
  `retrieval/full_corpus_smoke.py` (chỉ grep ai gọi), phần còn lại của `evaluation/full_corpus_eval.py`, mọi test trong phạm vi,
  notebook 06, guide `phase_5`–`phase_9` + `llm_rag_reference_for_hue_rag.md` + phần trả lời của `full_corpus_rag.md`,
  `backend/experiments/phase_8_1/` (trừ C-02).
- 3 sub-agent (guide, test, harness 8.1) bị dừng lúc kết phiên, **chưa ghi kết quả**. Brief chung vẫn còn ở `data/ra_soat_code_2026-10-25/tools/brief_common.md`
  để dùng lại.

## Top (theo mức; mới 8 finding, chưa đủ 10)

| id | mức | khâu | một dòng |
|---|---|---|---|
| C-01 | **vừa** | API ↔ retrieval | runtime nạp `core.schema` hai lần (2 tên) ⇒ API bắt hụt lỗi của retrieval: Qdrant lỗi ⇒ 500 thay vì 503; index cũ ⇒ 503 thay vì 409 |
| C-02 | **vừa** | harness 8.1 | `g2_generate.paired` không đổi dấu cho chỉ số "càng thấp càng tốt": với `refusal`, "wins" là câu bị từ chối **thêm**, `verdict` ngược |
| C-03 | thấp | prompt / context | định dạng tin nhắn gửi model nằm 2 nơi; đếm token context luôn dùng prompt mặc định kể cả khi harness đổi prompt |
| C-04 | thấp | context | nhánh `apply_chat_template` (thời Qwen) không bao giờ chạy với tokenizer tiktoken hiện tại |
| C-05 | thấp | generator | đường Representation B (agent thứ hai, prompt, `representation_b.py`) runtime không dùng |
| C-06 | thấp | retrieval | nhánh `native_hybrid_rrf` và reranker `minilm` trong service: loader runtime cấm, chỉ harness còn tới được |
| C-07 | thấp | evaluator | lệnh `parse-user-scores` thừa sau quyết định User 15:44 "không chấm điểm" |
| C-08 | — | hiệu năng | đã đo: không có vấn đề ở tầng tìm kiếm (khởi động 3,8 s; mỗi câu p50 28 ms) |

## Finding

### C-01 — Lớp lỗi bị nạp hai lần, API bắt hụt lỗi của retrieval
- **Khâu / file:dòng:** `backend/api/app.py:7-11` (thêm cả gốc repo lẫn `backend/` vào `sys.path`);
  `backend/retrieval/full_corpus.py:18-112` (`try: from backend.… except ModuleNotFoundError: from …`);
  `backend/ingestion/full_corpus_pipeline.py:13-47` (chỉ import kiểu `backend.*`, không có nhánh dự phòng — **phạm vi B25**);
  `backend/api/routes/chat.py:9-15, 64-80`; `backend/api/app.py:21-25, 61-84`.
- **Loại:** 2 / 3 · **Mức:** vừa (người dùng nhận sai mã / thông báo lỗi; log ghi "Unexpected…" làm khó chẩn đoán).
- **Quan sát:**
  - Chạy `data/ra_soat_code_2026-10-25/tools/dual_module_check.py` (cwd `backend/`, `import api.app` như `uvicorn api.app:app`) in ra:
    `twice (X and backend.X): ['core', 'core.schema', 'core.settings_loader']`, `core.schema is backend.core.schema: False`.
  - Chạy `data/ra_soat_code_2026-10-25/tools/exc_identity.py` in ra: retrieval ném `backend.core.schema.ComponentNotReadyError` /
    `RetrievalDependencyError` / `RetrievalConfigurationError`, còn API `except` các lớp `core.schema`: `same=False; subclass=False`
    (cả 3 lớp).
  - Có 9 file dùng mẫu import hai kiểu (`grep -rln "except ModuleNotFoundError"`, trừ experiments) và 5 chỗ chèn `sys.path`.
- ***Suy ra*** (đọc code, chưa tái tạo bằng sự cố thật — không được dựng lỗi giả):
  - lúc chạy, Qdrant lỗi ⇒ `RetrievalDependencyError` lọt qua `chat.py:73` ⇒ handler chung `app.py:166` trả **500 internal_error**,
    thay vì **503 retrieval_unavailable**;
  - lúc khởi động, index không khớp corpus (sửa kho chưa build lại) ⇒ `ComponentNotReadyError` lọt qua `app.py:70` xuống
    `except Exception` ⇒ **503** "tạm thời không khả dụng", thay vì **409 corpus_reingest_required** "cần lập chỉ mục lại".
    `Project_Status.md` §4 / §8 mô tả hành vi 409 này;
  - test API có thể vẫn đạt vì test ném lớp `core.schema` (chưa kiểm — phần test chưa rà).
- **Đề xuất sửa (nhỏ nhất đủ):** một kiểu import duy nhất. Chạy từ `backend/` thì dùng import trần (`core.…`): bỏ các khối
  `try/except ModuleNotFoundError`, sửa `full_corpus_pipeline.py` sang import trần, bỏ chèn gốc repo vào `sys.path`. Cần phối hợp
  B25 (ingestion thuộc phạm vi B).
- **Cách kiểm khi sửa:** chạy lại `exc_identity.py` ⇒ `same=True`; `dual_module_check.py` ⇒ không module nào bị nạp hai lần;
  pytest các file liên quan; khởi động API thật, gọi `/api/chat` một câu (paid nhỏ); harness / notebook vẫn import được
  (`experiments/phase_8_1/*` thêm `..` vào `sys.path`).
- **Rủi ro khi sửa:** test hiện import cả hai kiểu (`from backend.reranking…`, `from llm…`) ⇒ phải sửa cùng lúc; script chạy từ gốc
  repo (`python -m backend.…`) sẽ hỏng nếu có — cần grep trước.

### C-02 — `paired` của harness 8.1 ngược dấu với chỉ số "càng thấp càng tốt"
- **Khâu / file:dòng:** `backend/experiments/phase_8_1/g2_generate.py:243-254` (`paired`: `wins = diffs > 0`,
  `verdict(metric, …)` với `metric="refusal"`); so với `backend/evaluation/full_corpus_eval.py:613-648` (`paired_compare` có
  `sign = -1` cho `LOWER_IS_BETTER = {false_refusal, citation_error}`).
- **Loại:** 3 (khâu đo) · **Mức:** vừa (đọc nhầm kết luận thí nghiệm có chỉ số quyết là số câu từ chối — E1 của 8.2).
- **Quan sát:** input nhỏ hợp lệ (mốc từ chối 4 / 24 câu, biến thể hết cả 4):
  `g2 paired: wins 0, losses 4, verdict 'worse'` trong khi `paired_compare … false_refusal: wins 4, losses 0, verdict 'better'`.
- ***Suy ra:*** report 8.1 G2 ghi số câu từ chối (13 → 7, 13 → 1) chứ không dùng `verdict` của `refusal_in_scope`, nên kết luận 8.1
  **có vẻ** không bị ảnh hưởng (chưa kiểm hết các report). **Plan E1 của C (`phase_8_2_e1_plan.md` sha `f86240418ca1` §4 / §5)
  dùng chữ "thắng / thua" theo nghĩa câu được cứu, trong khi ghi `fn: g2_generate.paired(…, 'refusal', …)`** ⇒ khi 8.2 chạy lại
  phải sửa plan: dùng `paired_compare` (`false_refusal`) hoặc ghi rõ đảo dấu.
- **Đề xuất sửa:** harness 8.2 dùng `paired_compare` của evaluator thay vì chép `paired`; hoặc thêm `sign` như evaluator.
- **Cách kiểm:** chạy lại đúng input nhỏ trên ⇒ hai hàm cho cùng `wins / losses / verdict`.
- **Rủi ro:** thấp (harness, không phải runtime).

### C-03 — Định dạng tin nhắn gửi model nằm hai nơi
- **File:dòng:** `backend/llm/generator_openai_full_corpus.py:252` tự dựng chuỗi `"Câu hỏi:\n…\n\nNgữ cảnh truy xuất:\n…"`;
  `backend/llm/full_corpus_prompt.py:24-35` `build_answer_messages` dựng cùng chuỗi đó + system prompt mặc định, nhưng chỉ
  `retrieval/full_corpus_context.py:43, 48` gọi (để đếm token).
- **Loại:** 2 / 3 · **Mức:** thấp.
- **Quan sát:** `grep build_answer_messages` ⇒ chỉ context builder dùng. Bộ đếm token luôn tính `ANSWER_SYSTEM_INSTRUCTIONS` mặc định,
  kể cả khi harness truyền `answer_instructions` khác (P1, E1).
- ***Suy ra:*** sửa một nơi mà quên nơi kia thì đếm ngân sách context lệch thật. Hiện lệch nhỏ (P1 thêm ~45 token) và ngân sách
  còn rộng (16.384 − 2.048 − 512).
- **Đề xuất:** generator dùng `build_answer_messages` (hoặc ngược lại một hàm dựng chuỗi chung). Không thêm abstraction mới.
- **Cách kiểm:** `input_tokens` của B1 lượt mới khớp G2.1a 176 / 176 (như tiêu chí B1.2 T2).

### C-04 — Nhánh `apply_chat_template` không bao giờ chạy
- **File:dòng:** `backend/retrieval/full_corpus_context.py:41-46`.
- **Loại:** 1 · **Mức:** thấp.
- **Quan sát:** tokenizer runtime là `tiktoken.get_encoding("o200k_base")` (`llm/openai_tokenizer.py:12`), không có
  `apply_chat_template`; `grep apply_chat_template` chỉ ra đúng chỗ này. *Suy ra:* còn sót từ thời Qwen (Phase 6 cũ).
- **Đề xuất:** xóa nhánh. **Kiểm:** test context + `input_tokens` không đổi.

### C-05 — Đường Representation B runtime không dùng
- **File:dòng:** `backend/llm/generator_openai_full_corpus.py:136-148, 255-261` (agent thứ hai luôn được tạo);
  `backend/llm/full_corpus_prompt.py:16-19`; `backend/llm/representation_b.py`.
- **Loại:** 1 · **Mức:** thấp.
- **Quan sát:** `grep generate_search_context` ⇒ chỉ `llm/phase6_live_smoke.py:351` và test gọi. Spec 8.2 §4 ghi Representation B
  **ngoài phạm vi**.
- **Đề xuất:** User / A quyết giữ (hướng thử sau) hay gỡ cùng `phase6_live_smoke.py`. Không tự gỡ.

### C-06 — Nhánh retrieval / rerank mà runtime cấm
- **File:dòng:** `backend/retrieval/full_corpus.py:564-623` (`native_hybrid_rrf`), `:648-692` (`minilm`), `:755-758`;
  loader `backend/core/settings_loader.py:36` chỉ cho `reranker: none`.
- **Loại:** 1 / 2 · **Mức:** thấp.
- **Quan sát:** chỉ harness 8.1 dựng service với treatment / reranker khác (G1 dùng native). *Chưa chắc:* harness nào còn dùng
  nhánh `minilm` (tên gọi còn từ Foods).
- **Đề xuất:** giữ `native_hybrid_rrf` nếu E3a 8.2 dùng (spec 8.2: "cách trộn native như G4-B"); đổi tên / gỡ `minilm` sau khi kiểm
  harness.

### C-07 — `parse-user-scores` thừa
- **File:dòng:** `backend/evaluation/full_corpus_eval.py:679-707`, CLI `:871`.
- **Loại:** 1 · **Mức:** thấp.
- **Quan sát:** chỉ CLI + test gọi; User 15:44 25/10 quyết định không chấm điểm tay (mốc người 8.2 là đọc cặp mù).
- **Đề xuất:** gỡ khi dọn evaluator (kèm test). Hỏi A trước, vì 7B còn tham chiếu.

### C-08 — Hiệu năng tầng tìm kiếm: đã đo, không có vấn đề
- **Quan sát:** `data/ra_soat_code_2026-10-25/tools/latency.py`: đường runtime thật (đọc Qdrant, e5 CPU), 20 câu tự viết (không lấy Golden):
  khởi động service **3,76 s**; `total_ms` p50 **28**, max 78; dense p50 25; BM25 cục bộ trên 30 ứng viên p50 3 ms.
  *Suy ra:* độ trễ người dùng nằm ở bước sinh (B1: p50 ~1,9 s), không ở tìm kiếm.

## Đã kiểm, không thấy vấn đề
- `llm/citations.py` (27 dòng): khớp hợp đồng Phase 6 §10 (câu từ chối đúng nguyên văn, không kèm `[n]`).
- `evaluation/golden_full_corpus.py`: CLI kiểm / gộp file Golden (Phase 7A), không gọi mạng; runtime không dùng, nhưng còn giá trị
  khi sửa Golden.

## Không rà được / chưa chắc
- Toàn bộ phần "chưa rà" ở đầu file.
- C-01: chưa kiểm test API có che lỗi không; chưa grep lệnh chạy kiểu `python -m backend.…`.
- `retrieval/full_corpus_smoke.py` (548 dòng) và `llm/phase6_live_smoke.py` (502 dòng): chỉ test import — chưa kiểm còn ai chạy CLI.
- Generator dùng OpenAI Agents SDK cho một lần gọi không tool. *Giả thuyết* (loại 2 / 7): gọi thẳng Responses API đơn giản hơn;
  chưa đánh giá chi phí đổi.

## Lệch
- Không có lệch đề bài.

Script đo (chỉ đọc, private, chạy từ `backend/` bằng `HF_HUB_OFFLINE=1 uv run python -I <file>`): `data/ra_soat_code_2026-10-25/tools/` (`dual_module_check.py`, `exc_identity.py`, `latency.py`, `brief_common.md`).
