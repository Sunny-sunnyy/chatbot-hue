# C34 — rà code luồng trả lời + đánh giá (chỉ đọc) — **XONG, chờ kiểm chéo**

Người làm: C (Claude Opus 5.5) · phần 1: terminal `hue-rag-d6`, 17:06 25/10 (dừng vì kết phiên) · phần 2: terminal `hue-rag-7f`,
18:26–18:41 25/10 (`date`), A "làm đi" 18:2x · Rà trên `main` (`bc568f1` phần 1; `1e8cf8f` phần 2 — chỉ thêm commit docs, `git diff
bc568f1..HEAD` không đổi code) · **0 USD**. Chỉ thị User 18:3x (qua A): chỉ rà và đề xuất, chưa sửa gì.

- **Đã rà:** `retrieval/`, `reranking/`, `llm/`, `api/`, `evaluation/`, `frontend/`; test trong phạm vi (11 file, chạy thật không key:
  104 test → 96 passed, 1 failed + 7 error đều do thiếu `OPENAI_API_KEY`); notebook 06; guide `phase_5`–`phase_9`, `llm_rag_reference`,
  phần trả lời `full_corpus_rag.md`; `experiments/phase_8_1/` (import + `--help`, không chạy thí nghiệm).
- **Sub-agent (3, brief chung `data/ra_soat_code_2026-10-25/tools/brief_common.md`, commit nền `1e8cf8f`):** S1 guide + notebook 06,
  S2 test, S3 harness 8.1 + 2 file smoke. Kết quả gốc giữ ở `/tmp/c34/s{1,2,3}_*.md` (tạm). C đã gộp vào C-01, C-09, C-10, C-12 → C-20 và
  **tự kiểm lại bằng file thật**: guide 7 ghi "canonical", 0 lần nhắc `full_corpus_eval`; notebook 06 tìm gốc theo tên `hue_rag`, không ô code
  nào gọi `/api/chat`; `build_representation_b_messages` / `record_generation_success` 0 lời gọi; `require_openai_key` dùng `pytest.fail`;
  `full_corpus_smoke` từ `backend/` ⇒ `ModuleNotFoundError: No module named 'backend'`; probe index cũ (S2) chạy lại ⇒ `503
  retrieval_unavailable` (xem C-01).

## Top 10 (theo mức)

| # | id | mức | khâu | một dòng |
|---:|---|---|---|---|
| 1 | C-09 | **cao** | context ↔ validator ↔ UI | validator chỉ bắt `[n]`, context gắn nhãn `[Nguồn n]` ⇒ 8 / 176 câu chatbot hiện tại ra lỗi 500 dù có trích nguồn; nguyên nhân ghi ở 8.1 chưa đúng; quyết định 8.1 reasoning có thể mở lại (A đã tự kiểm) |
| 2 | C-01 | **vừa** | API ↔ retrieval | lớp lỗi nạp hai lần ⇒ API bắt hụt: index cũ ⇒ 503 thay 409 (**đã tái tạo**), Qdrant lỗi khi hỏi ⇒ 500 thay 503 (suy ra); sửa phải kèm tách lỗi "model không nạp" khỏi 409; không test nào đi qua ranh giới này |
| 3 | C-02 | **vừa** | harness 8.1 | `g2_generate.paired` không đổi dấu cho `refusal` ⇒ thắng / thua ngược (ảnh hưởng plan E1) |
| 4 | C-12 | **vừa** | guide | guide Phase 7 (tự nhận "canonical") chỉ tả evaluator Foods đã gỡ; guide Phase 8 còn `not_ready`, baseline MiniLM / gpt-5.4 — không có 7B / 8.1 / 8.2 |
| 5 | C-19 | thấp | smoke | `full_corpus_smoke.py` (Phase 5) lệch hệ thống, hỏng khi chạy từ `backend/`; `phase6_live_smoke.py` là kiểm live duy nhất qua route nhưng gánh Representation B + hook recorder — giữ / gỡ cần quyết |
| 6 | C-17 | thấp | test | `require_openai_key` = `pytest.fail` chặn cả 3 test miễn phí ⇒ suite không key không bao giờ xanh; marker `live` khai mà không dùng |
| 7 | C-20 | thấp | harness 8.1 | harness thành thư viện ngầm (import chéo, `OUT_DIR` ghim) ⇒ hàm so cặp đã chép 4 + 1 lần; 8.2 sẽ chép tiếp |
| 8 | C-10 | thấp | API | bộ ghi bằng chứng smoke Phase 6 cài 11 nhánh `if recorder:` vào route production, runtime không bao giờ bật |
| 9 | C-18 | thấp | test | ~31 test khóa code runtime không dùng; 2 test smoke gọi `confirm_paid=True` chỉ được monkeypatch chặn; vài assert rỗng |
| 10 | C-03 | thấp | prompt / context | định dạng tin nhắn gửi model nằm 2 nơi; đếm token context luôn dùng prompt mặc định |

Còn lại (thấp): C-04 nhánh `apply_chat_template` chết · C-05 Representation B không dùng · C-06 nhánh `native` / `minilm` runtime cấm ·
C-07 `parse-user-scores` thừa · C-11 nhánh 409 lúc hỏi + `rerank()` không tới được · C-13 guide 5 / 6 / 9 / `llm_rag_reference` /
`full_corpus_rag` lệch nhỏ · C-14 notebook 06 · C-08 hiệu năng tìm kiếm: đã đo, ổn.

**Gợi ý gộp khi sửa** (để A / User chọn): nhóm *đường lỗi API* = C-01 + C-11 + test (C-01); nhóm *citation* = C-09 (+ test, + đo lại
M1–M3); nhóm *dọn code chết* = C-04 + C-05 + C-06 (`minilm`) + C-07 + C-10 + C-18 + C-19 (phụ thuộc quyết định giữ / gỡ 2 smoke);
nhóm *tài liệu* = C-12 + C-13 + C-14; nhóm *harness 8.2* = C-02 + C-20 (trước khi viết E1).

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
  - **Đã tái tạo trường hợp index cũ (phiên tối, S2, C chạy lại 18:3x):** `data/ra_soat_code_2026-10-25/tools/c01_probe_stale.py` —
    `create_app` thật, settings đọc thật rồi **chỉ trong bộ nhớ** thêm `exclude_parts += ["foods"]` (giống "sửa kho mà chưa build lại"),
    không ghi file / Qdrant, không paid ⇒ retrieval ném `backend.core.schema.ComponentNotReadyError` (thông điệp "stale"), `isinstance(…,
    core.schema.ComponentNotReadyError)` = `False`, `POST /api/chat` ⇒ **503 `retrieval_unavailable`** thay vì 409. *Ghi để A xét:* tình
    huống "cũ" được dựng bằng cấu hình trong bộ nhớ, không phải sửa kho thật (`Session_Prompt.md` §8 cấm đổi môi trường để tạo lỗi giả —
    C coi đây là đọc đường thật với đầu vào khác, không mock; bằng chứng chính của C-01 vẫn là danh tính lớp ở trên).
    Trường hợp Qdrant lỗi khi hỏi (500 thay 503): vẫn chỉ suy ra từ code.
  - **Test không che bằng mock, nhưng không test nào đi qua ranh giới API ↔ retrieval** (S2): `test_api_chat.py` không ném lỗi retrieval,
    chỉ kiểm 422 / 200 / 500 `context_budget_error` (`:15-60`; nhánh này đúng thật — `ContextBudgetError` cùng một lớp); `grep -n
    "corpus_reingest_required\|retrieval_unavailable\|409" backend/tests/*.py` ⇒ 0; `test_full_corpus_retrieval.py:8, :18` import `backend.*`
    (cùng bản lớp với bên ném) ⇒ đạt dù API có bắt được hay không; `conftest.py:13-16` chèn cả hai đường vào `sys.path`.
  - **Thêm (S1-04, C tự đọc lại `app.py:70-76`, `full_corpus.py:815-823, 834`):** `ComponentNotReadyError` dùng chung cho hai nghĩa —
    "index không khớp corpus / build record / sparse state / collection" (đúng là 409) **và** "model dense / MiniLM không nạp được"
    (thiếu HF cache, mất mạng — spec Phase 6 amendment 2026-09-30 §: phải 503 `retrieval_unavailable`). Hiện nay *nhờ* C-01 nên cả hai rơi
    xuống `except Exception` ⇒ 503 (index cũ sai, model lỗi tình cờ đúng). **Chỉ sửa C-01 thôi thì model lỗi sẽ thành 409 "cần lập chỉ mục
    lại"** ⇒ người vận hành build lại index không cần thiết. Sửa C-01 phải kèm: bọc lỗi nạp / warm-up model bằng `RetrievalDependencyError`.
- **Đề xuất sửa (nhỏ nhất đủ):** một kiểu import duy nhất. Chạy từ `backend/` thì dùng import trần (`core.…`): bỏ các khối
  `try/except ModuleNotFoundError`, sửa `full_corpus_pipeline.py` sang import trần, bỏ chèn gốc repo vào `sys.path`. Cần phối hợp
  B25 (ingestion thuộc phạm vi B).
- **Cách kiểm khi sửa:** viết **trước** 2 test miễn phí (S2-01, hiện sẽ đỏ): (a) trong subprocess import sạch, `retrieval.full_corpus.X is
  core.schema.X` cho 3 lớp lỗi; (b) `create_app` với kho thiếu một file (bản kho trong `tmp_path`, ổn định hơn bỏ domain) ⇒ `POST /api/chat`
  409. Sau đó chạy lại `exc_identity.py` ⇒ `same=True`; `dual_module_check.py` ⇒ không module nào bị nạp hai lần;
  pytest các file liên quan; khởi động API thật, gọi `/api/chat` một câu (paid nhỏ); harness / notebook vẫn import được
  (`experiments/phase_8_1/*` thêm `..` vào `sys.path`).
- **Rủi ro khi sửa:** test hiện import cả hai kiểu (`from backend.reranking…`, `from llm…`) ⇒ phải sửa cùng lúc. **Đã grep (phiên tối
  25/10):** lệnh build index chính thức chạy **từ gốc repo** — `python -m backend.ingestion.full_corpus_pipeline build --candidate <id>`
  (`guides/full_corpus_rag.md:114`, `bao_cao_he_thong/BAO_CAO_KHO_DU_LIEU.md:89`; `ingestion/preview.py:4` cũng vậy), còn API chạy **từ
  `backend/`** — `uvicorn api.app:app` (22 lần trong tài liệu). Hai đầu vào ⇒ hai kiểu import là gốc của C-01. Chọn import trần thì lệnh build
  phải đổi thành `cd backend && python -m ingestion.full_corpus_pipeline …` (và sửa guide / báo cáo); chọn `backend.*` thì API chạy
  `uvicorn backend.api.app:app` từ gốc. Phải chọn **một** quy ước cho cả build, API, test, harness — việc của A / User.

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

### C-09 — Validator citation không nhận dạng `[Nguồn n]` mà chính context dạy model ⇒ API trả 500 cho câu trả lời có trích nguồn
- **Khâu / file:dòng:** `backend/retrieval/full_corpus_context.py:82` (mỗi nguồn gắn nhãn `[Nguồn {id}]`);
  `backend/llm/full_corpus_prompt.py:12` (prompt dặn "Đặt citation [n]"); `backend/llm/citations.py:9` (`CITATION_PATTERN = \[(\d+)\]`,
  chỉ bắt `[n]`) ⇒ `:21-22` raise "Grounded answer has no citation" ⇒ `backend/api/routes/chat.py` trả **500
  `citation_integrity_error`** "Câu trả lời không đáp ứng yêu cầu trích dẫn"; `frontend/app.js:44` cũng chỉ nối link cho `[n]`.
  Evaluator và harness 8.1 dùng cùng `select_cited_sources` (`evaluation/full_corpus_eval.py:361`, `experiments/phase_8_1/g2_generate.py:206`).
- **Loại:** 3 (khâu dính: nhãn context ↔ validator ↔ UI) · **Mức:** **cao** (người dùng thật nhận lỗi thay vì câu trả lời đúng có
  trích nguồn; chỉ số "lỗi citation" của 7B / 8.1 / 8.2 đo phần lớn là định dạng, không phải model quên trích).
- **Quan sát** (script `data/ra_soat_code_2026-10-25/tools/recheck_both.py`, `nguon_count.py`; đọc file kết quả có sẵn, chỉ in số đếm, 0 USD):

  | Lượt (đã sinh sẵn) | lỗi citation hiện tại | trong đó chỉ có `[Nguồn n]` | nếu validator nhận cả `[n]` lẫn `[Nguồn n]` |
  |---|---:|---:|---:|
  | 7B Run 1 (176, cấu hình đang chạy) | 4 | — | **0** |
  | 7B Run 2 (176) | 6 | — | 2 |
  | 8.1 G2.0 baseline dev 120 / test 56 (= chatbot hiện tại) | 4 / 4 | 4 / 4 | **0 / 0** |
  | 8.1 G2.1a context 10 dev / test | 4 / 4 | 4 / 4 | 0 / 0 |
  | 8.2 B1 context 10 + NFC dev / test | 6 / 6 | 6 / 6 | **0 / 0** |
  | 8.1 G2.4 reasoning `none` / `low` / `high` | 8 / 9 / 4 | 6 / 5 / 3 | 2 / 4 / 1 |
  | 8.1 G2.1b thứ tự / P1 / P2 | 6 / 3 / 1 | 4 / 1 / 0 | 2 / 2 / 1 |

  Không câu nào trộn hai dạng; mọi lỗi còn lại sau khi nhận cả hai dạng là "không có ngoặc số nào" (đếm hình dạng: `cite_shapes.py`).
  Ở cấu hình đang chạy, **8 / 176 câu (4,5 %) trên chatbot thật sẽ ra lỗi 500**, cả 8 đều do định dạng.
- **Đã biết một phần:** `Project_Status.md` §8 + B24 (`phase_8_2_b0_prep_review.md` F1) biết model viết `[Nguồn n]`, nhưng chỉ sửa công cụ
  đọc cặp mù. **Mới:** tác động lên runtime / UI / chỉ số. Report 8.1 G2 §4.3 kết luận "lỗi citation hiện tại là model quên đặt `[n]` khi có
  nhiều nguồn" và bảng G5 dòng 7 đề xuất "giảm lỗi citation ở bước sinh" ⇒ **nguyên nhân ghi trong 8.1 chưa đúng**.
- ***Suy ra*** (chưa kiểm, cần A / User xem — không kết luận): (a) quyết định 8.1 **3c reasoning** loại `none` vì "lỗi citation 4 → 8 (> +2)";
  tính lại với validator nhận cả hai dạng là 0 → 2 (= +2, không vượt ngưỡng) trong khi Completeness +0,136 [+0,034; +0,261] p Holm 0,031 ⇒
  `none` **có thể** qua guardrail dev (vẫn phải xác nhận trên test theo luật 8.1); (b) "nhiễu citation lớn" ghi ở B1 (12 vs 8) toàn là định
  dạng ⇒ tiêu chí lỗi citation của E2 / E3 nên đo sau khi sửa C-09.
- **Đề xuất sửa (nhỏ nhất đủ, chọn một — A / User quyết):** (1) `CITATION_PATTERN` nhận cả `[Nguồn n]` (không phân biệt hoa thường) và
  đổi về `[n]` trước khi trả text cho UI (UI giữ nguyên); hoặc (2) đổi nhãn context thành `[n]` để khớp prompt — đổi đầu vào model ⇒ là
  thí nghiệm (`run-experiment`), phải sinh lại. (1) không đổi câu trả lời của model, kiểm offline được ngay.
- **Cách kiểm khi sửa:** chạy lại `recheck_both.py` dạng test trên file có sẵn ⇒ lỗi cũ chỉ còn loại "không có ngoặc số"; test citations
  thêm ca `[Nguồn 2]` và ca trộn `[1]` + `[Nguồn 2]` (S2-05: `test_citations.py:16-39` chỉ có `[1]` / `[99]`); một câu `/api/chat` thật (paid nhỏ) có `sources` khớp marker; UI nối link cho câu đã đổi dạng.
- **Rủi ro khi sửa:** (1) đổi định nghĩa chỉ số "lỗi citation" ⇒ mốc 7B / 8.1 / G0.6 phải tính lại theo định nghĩa mới (free, từ file có
  sẵn) và ghi rõ trong report; không trộn số cũ với số mới.
- **Cách đo trước–sau (theo `run-experiment`; A 18:3x yêu cầu; chỉ là đề xuất, chưa chạy, không kết luận):**
  - **M1 — sửa validator (cách (1)).** Đổi đúng một thứ: `CITATION_PATTERN` nhận thêm `[Nguồn n]`. Khâu sau bước sinh, tất định ⇒ được
    phát lại câu trả lời đã sinh thật (`run-experiment` §3.5), không cần A/A, 0 USD.
    ```yaml
    experiment_id: c09_m1_validator_nguon
    baseline: llm/citations.py trên main 1e8cf8f
    changed_variable: CITATION_PATTERN nhận cả [n] và [Nguồn n] (không phân biệt hoa thường, sau NFC)
    data: mọi file câu trả lời có sẵn — 7B run1/run2 (176), 8.1 G2.0/G2.1a/G2.1b/P1/P2/G2.4 (dev 120, test 56), 8.2 B1 (176)
    metrics:
      - {name: câu bị 500 vì chỉ có [Nguồn n], fn: select_cited_sources mới, better: down, role: decide, noise: 0 (tất định)}
      - {name: câu đang hợp lệ thành lỗi, better: down, role: floor, floor: 0}
      - {name: câu đang hợp lệ bị đổi tập nguồn trả UI, better: down, role: floor, floor: 0}
      - {name: lỗi id lạ / câu từ chối kèm citation mới, better: down, role: floor, floor: 0}
      - {name: lỗi "không có ngoặc số" còn lại, role: watch}
    ```
    Mốc (đã tính, bảng trên): cấu hình đang chạy 8 / 176 → 0. Còn phải chạy khi sửa: 3 sàn (so tập nguồn từng câu trước / sau). Kiểm
    runtime: một câu `/api/chat` thật có `[Nguồn n]` (paid nhỏ) + UI hiện link.
  - **M2 — mở lại quyết định 8.1 3c (reasoning `none`).** Thay đổi ở chính bước sinh ⇒ phát lại chỉ dùng để **tính lại một chỉ số** trên câu
    đã sinh thật; Completeness / Accuracy (judge) giữ nguyên số 8.1. **Cảnh báo:** định nghĩa chỉ số đổi *sau khi* đã thấy số 8.1 (lý do: lỗi
    đo C-09, độc lập với `none`) ⇒ số dev tính lại chỉ là **tín hiệu**, không đủ để quyết.
    - Số tính lại (dev 120, định nghĩa mới): baseline 0, `none` 2, `low` 4, `high` 1 (cũ 4 / 8 / 9 / 4). Ngưỡng 8.1 "lỗi citation ≤ +2
      câu" ⇒ `none` +2 đúng ngưỡng; nhưng **nhiễu A/A** theo định nghĩa mới (7B Run 1 → Run 2) cũng là 0 → 2 ⇒ +2 nằm trong nhiễu.
    - Nếu A / User muốn mở lại: ghi tiêu chí **trước** (sàn: 0 câu `out_of_scope` bị trả lời; tụt cho phép: lỗi citation định nghĩa mới
      ≤ +2 câu; chỉ số quyết: Completeness CI 95 % > 0 sau Holm), rồi **xác nhận trên test 56** bằng một lượt `none` mới, baseline test có
      sẵn (`t_baseline`), judge Claude chấm cùng lượt mù. Ước tiền: 56 × ~0,000121 USD ≈ **0,007 USD** (đơn giá `none` ở G2.4) — NOT RUN.
    - Tương tác 8.2: spec 8.2 chưa có reasoning; mở lại 3c là thay đổi phạm vi ⇒ User quyết.
  - **M3 — tiêu chí citation của 8.2 (B1 / E1 / E2 / E3).** Nếu sửa C-09 trước khi 8.2 chạy lại: tính lại "lỗi citation" của B1 và A/A
    theo định nghĩa mới (B1 12 → 0; G2.1a 8 → 0) trước khi ghi ngưỡng cho E2 / E3; plan E1 (C33) đổi sha.

### C-10 — Bộ ghi bằng chứng của smoke Phase 6 cài vào route production nhưng runtime không bao giờ bật
- **Khâu / file:dòng:** `backend/api/routes/chat.py:17, 55` + 10 nhánh `if recorder:` (`:58-147`); `backend/llm/evidence_recorder.py`
  (135 dòng; `record_evidence` chỉ được gọi ở `llm/phase6_live_smoke.py:395` và test).
- **Loại:** 2 / 1 · **Mức:** thấp.
- **Quan sát:** `grep -rn "record_evidence\|get_current_recorder" backend --include=*.py` (trừ test) ⇒ chỉ `chat.py` (đọc) và
  `phase6_live_smoke.py` (bật). API không có middleware nào gọi `record_evidence` ⇒ `get_current_recorder()` luôn `None` khi chạy
  thật. `record_generation_success`, `packed_text`, `request_id` không ai đọc ngoài test.
- ***Suy ra:*** route chính dài gấp đôi vì công cụ kiểm tra một lần của Phase 6; đọc luồng lỗi khó hơn.
- **Đề xuất:** đi cùng quyết định giữ / gỡ `phase6_live_smoke.py` (xem phần harness): gỡ smoke thì gỡ recorder + các nhánh. Không tự gỡ.
- **Cách kiểm:** `test_api_chat.py` đạt; một câu `/api/chat` thật. **Rủi ro:** thấp.

### C-11 — Nhánh 409 lúc hỏi và `CrossEncoderReranker.rerank()` không tới được
- **Khâu / file:dòng:** `backend/api/routes/chat.py:72-80` (`except ComponentNotReadyError` ⇒ 409 `corpus_reingest_required` khi đang hỏi);
  `backend/retrieval/full_corpus.py:651` là chỗ duy nhất `search()` ném `ComponentNotReadyError` (nhánh `minilm`, runtime cấm — C-06);
  freshness chỉ kiểm lúc dựng service (`:424-426`, `:761-772`) ⇒ 409 thật đi qua `app.py:61-84` lúc khởi động. `reranking/cross_encoder.py:95-114`
  `rerank()` (kiểm `chunk_id` trùng / rỗng): `grep -rn "\.rerank(" backend` ⇒ 0 lời gọi; service và harness G4 dùng `score_documents`.
- **Loại:** 1 · **Mức:** thấp.
- ***Suy ra:*** kể cả khi sửa C-01, nhánh 409 lúc hỏi vẫn không chạy; "cần lập chỉ mục lại" chỉ đúng nghĩa ở lúc khởi động.
- **Đề xuất:** khi sửa C-01 / C-06, bỏ nhánh 409 trong route (hoặc để `minilm` ném lỗi cấu hình) và bỏ `rerank()`. **Kiểm:** test API + retrieval.

### C-12 — Guide Phase 7 và Phase 8 không có phần hiện hành (S1-01, S1-02)
- **File:dòng:** `guides/phase_7_retrieval_answer_evaluation.md:3-8` (banner "Full-corpus extension gate — chưa active"), `:19` ("Guide này
  là nguồn canonical…"), `:68-116` (`test.py` / `eval.py` / Gradio), `:186-207` (judge `gpt-5.4-mini`, `temperature=0`);
  `guides/phase_8_benchmark_model_selection.md:12` (`not_ready`), `:48-57` (baseline MiniLM / `gpt-5.4-nano` / judge `gpt-5.4-mini`),
  `:96-112` (3 profile `dense_only` / `hybrid_*`).
- **Loại:** 5 · **Mức:** vừa (agent mở guide theo bảng `guides/README.md` gặp kiến trúc đã gỡ; guide 7 dặn `temperature=0` mà
  `full_corpus_rag.md:93` ghi luna trả 400 khi có `temperature`).
- **Quan sát:** `grep -c full_corpus_eval guides/phase_7_…` = 0 (C kiểm); `backend/evaluation/` chỉ còn `full_corpus_eval.py`,
  `golden_full_corpus.py`, `full_corpus_judge_prompt.md`; guide 8 0 lần nhắc 8.1 / 8.2 / `gpt-6-luna`; `HybridRetriever` / `DenseRetriever`
  0 trong code. Hiện trạng 7A / 7B chỉ có ở `full_corpus_rag.md:83-103, 208-214`. `guides/README.md:159-161` cùng gốc (ngoài phạm vi C).
- **Đề xuất:** mỗi guide thêm khối đầu "Hiện hành" 5–8 dòng trỏ evaluator / Golden / judge Claude (7) và 8.1 closed / 8.2 paused (8);
  gắn nhãn "lịch sử Foods" cho phần còn lại; bỏ "canonical" / `not_ready`. Không chép số Golden private.
- **Cách kiểm:** `grep -n "gpt-5.4\|MiniLM\|not_ready\|canonical"` chỉ còn trong phần đã gắn nhãn lịch sử. **Rủi ro:** thấp.

### C-13 — Lệch nhỏ ở guide 5 / 6 / 9 / `llm_rag_reference` / `full_corpus_rag` (S1-03, S1-06, S1-07, S1-08)
- **File:dòng:** `guides/phase_6_generation_api.md:42` (`gpt-5.4-nano` trong khối "Contract full-corpus hiện hành" — C kiểm), `:10-13`
  ("handoff active"), không có bảng mã lỗi hiện hành (`grep -rln "corpus_reingest_required\|generation_unavailable" guides/` = 0);
  `phase_5_…:55` ("Reranker hiện hành vẫn là MiniLM"), `:21-22` (4 collection); `phase_9_…:29-42`; `llm_rag_reference_for_hue_rag.md:27,
  346-347, 380-399, 436`; `full_corpus_rag.md:88-90` (thiếu lệnh `split`), `:398-402` (#6a "trả phần có căn cứ" — đã biết, G5 §1 dòng 2b),
  `:588, 598-602` ("Tài liệu hiện hành" trỏ gói 2026-10-01 "Active").
- **Loại:** 5 · **Mức:** thấp. **Đề xuất:** sửa từng dòng như S1 ghi (gắn "lịch sử" / thay giá trị hiện hành; guide 6 thêm bảng 7 mã lỗi
  từ `chat.py` / `app.py`). **Kiểm:** grep từ khóa cũ chỉ còn trong đoạn lịch sử; `full_corpus_eval --help` khớp danh sách lệnh.

### C-14 — Notebook 06: nói có ô gọi `/api/chat` tốn phí nhưng không có; tìm gốc repo theo tên thư mục (S1-05)
- **File:dòng:** `notebooks/06_generation_and_api.ipynb` cell 7 (markdown "ô gọi `/api/chat` tốn phí"), cell 2
  (`while REPO_ROOT.name != "hue_rag"`), cell 0 (Representation B như một phần luồng).
- **Loại:** 5 · **Mức:** thấp.
- **Quan sát (C kiểm):** `/api/chat` chỉ xuất hiện ở 3 ô markdown (0, 5, 7); 3 ô code: settings, `/health` qua `TestClient`, dựng
  `ChatResponse` mẫu. Remote là `chatbot-hue.git` ⇒ clone mặc định tên `chatbot-hue`, vòng tìm gốc chạy tới `/`. Outputs rỗng,
  `execution_count: null` (đạt luật §11).
- **Đề xuất:** bỏ câu "tốn phí" (hoặc thêm đúng một ô POST); tìm gốc theo `backend/config/settings.yaml` tồn tại. **Kiểm:** Run All trên bản
  tạm trong thư mục tên khác.

### C-15 — (gộp vào C-04 / C-05) Phần thừa nhỏ thêm (S1-09)
- `llm/full_corpus_prompt.py:37` `build_representation_b_messages` và `llm/evidence_recorder.py:99` `record_generation_success`: 0 lời gọi
  kể cả test (C kiểm). `settings.yaml` `token_encoding` bị `settings_loader.py:63-64` ép bằng `o200k_base` nhưng `llm/openai_tokenizer.py:12`
  dùng hằng, không đọc settings (khâu dính loại 3 — giữ một nơi). Gỡ cùng C-04 / C-05.

### C-16 — (gộp vào C-01) không test nào đi qua ranh giới API ↔ retrieval (S2-01) — xem C-01.

### C-17 — Suite không key không bao giờ xanh; marker `live` khai mà không dùng (S2-02, S2-08)
- **File:dòng:** `backend/tests/conftest.py:37-46` (`require_openai_key` = `pytest.fail` — C kiểm), dùng ở `test_api_chat.py:30, 45, 86`,
  `test_openai_full_corpus_generator.py:24, 46`, `test_phase6_live_smoke.py:126, 403`; `test_phase6_settings.py:66` kiểm env, không kiểm code;
  `conftest.py:23-28` đăng ký marker `live`, `grep -rn "mark.live\|-m live" backend` = 0.
- **Loại:** 4 · **Mức:** thấp.
- **Quan sát:** 11 file không `--env-file` ⇒ 1 failed + 7 error, tất cả do thiếu key; 3 test (`test_api_chat.py:45, 86`,
  `test_phase6_live_smoke.py:403`) không tới generator mà vẫn bị chặn. `Project_Status.md` §8 dặn chạy pytest có `--env-file`.
- ***Suy ra:*** quen bỏ qua màu đỏ; luôn nạp key vào pytest làm tăng rủi ro với file paid (bẫy `--deselect` §8).
- **Đề xuất:** bỏ fixture khỏi 3 test miễn phí; đánh `@pytest.mark.live` cho test cần key và ghi `-m "not live"` vào §8 (hoặc xóa marker).
  **Kiểm:** 11 file không key ⇒ chỉ còn test thật sự cần generator báo lỗi. **Rủi ro:** thấp.

### C-18 — Test khóa code không dùng; test paid tiềm ẩn chỉ được mock chặn; assert rỗng (S2-03, S2-06, S2-07)
- **File:dòng:** ~31 test cho Representation B (`test_openai_full_corpus_generator.py:15-21, 53-106`; `test_phase6_settings.py:20`), runner
  Phase 6 (cả `test_phase6_live_smoke.py`, 19 test), runner Phase 5 (`test_full_corpus_retrieval.py:354, 381, 413`), MiniLM (`:186-206`,
  `:817-829`), `parse-user-scores` (`test_full_corpus_eval.py:170-190`). `test_phase6_live_smoke.py:202-236, 295-321` gọi
  `run_smoke_async(confirm_paid=True)` — chỉ monkeypatch `create_app` (`:228, :314`, đã biết) chặn lượt paid. Assert rỗng / hiển nhiên:
  `test_full_corpus_context.py:82-85` (`if domain: pass`), `:88-93`, `test_phase6_live_smoke.py:388-391`.
- **Loại:** 1 / 4 · **Mức:** thấp.
- **Đề xuất:** gỡ code nào (C-05 / C-06 / C-07 / C-19) thì gỡ test tương ứng cùng commit; nếu giữ runner Phase 6 thì đổi 2 test sang
  `confirm_paid=False`; xóa assert rỗng cùng C-04. **Kiểm:** grep tên hàm ⇒ 0; pytest 11 file đạt.

### C-19 — Hai runner smoke: một đã lệch hệ thống, một là kiểm live duy nhất qua route (S3-04, S3-05, S3-06)
- **File:dòng:** `backend/retrieval/full_corpus_smoke.py:3` ("16 configuration cells"), `:84-86` (mặc định mọi candidate × 2 treatment × 2
  reranker, gồm 8B không có index), `:22-65` (import kép); `backend/llm/phase6_live_smoke.py:226-229` (`--confirm-paid`), `:336-375` (lượt
  Representation B), `:396` (`POST /api/chat` qua ASGI), `:263-268` (`--output` ghi câu hỏi / trả lời / excerpt kho, không kiểm gitignore).
- **Loại:** 1 / 2 / 5 · **Mức:** thấp.
- **Quan sát:** `cd backend && uv run python -m retrieval.full_corpus_smoke --help` ⇒ `ModuleNotFoundError: No module named 'backend'` (C
  chạy lại); từ gốc repo chạy được. Trace cuối `data/full_corpus_phase_5_smoke_trace.json` 13/09 trên 4 candidate không còn; 7A2 Gate 2 dùng
  script tạm thay runner này. `full_corpus_smoke.py:86, 264-271` là **chỗ duy nhất** dựng service `reranker="minilm"`. `phase6_live_smoke.py`
  chạy lần cuối 24/10 (7A2 Gate 2), 5 lượt paid; là nơi duy nhất ngoài test bật `record_evidence` (C-10). Evaluator không đi qua route HTTP
  nên không thấy lỗi kiểu C-01 — runner này thấy được.
- **Đề xuất (A / User chọn):** `full_corpus_smoke` — (A) gỡ + 3 test + nhánh `minilm` của service, hoặc (B) giữ, mặc định chỉ candidate
  runtime, bỏ import dự phòng. `phase6_live_smoke` — (A) giữ, rút gọn (bỏ lượt Representation B, kiểm đường dẫn `--output`; dùng làm bước
  "API live qua `/chat`" của 8.2), hoặc (B) gỡ cùng `evidence_recorder` + 11 nhánh hook (đụng route ⇒ review).
- **Cách kiểm:** `--help` từ đúng thư mục; `preflight` e5 từ gốc (free); pytest file test tương ứng. **Rủi ro:** thấp (B của live smoke: vừa).

### C-20 — Harness 8.1 thành thư viện ngầm; hàm so cặp bị chép (S3-01, S3-02, S3-03, S3-07)
- **File:dòng:** so cặp: `experiments/phase_8_1/g1_retrieval.py:243-268` (`compare`, được g3 / g4_keyword / g4_rerank import),
  `g2_generate.py:243-254` (`paired`, C-02), `g5_by_category.py:25-41`, `p82-b1:backend/experiments/phase_8_2/b1.py:119-125` — gốc
  `evaluation/full_corpus_eval.py:613-648` chỉ nhận metric tên cố định qua `row_metrics` `:578-592`. Import chéo: g2 ← g1, g4_rerank
  (`g2_generate.py:47-48`, kéo theo `torch` + `openai`); `OUT_DIR` ghim cấp module (g1 `:44`, g2 `:54`, g3 `:63`, g4k `:46`, g4r `:54`);
  `g2_generate.run_variant` (`:128-151`) chép `run_generation` (`full_corpus_eval.py:372-389`); `g4_keyword.py:144-145` dựng service
  `native_hybrid_rrf` mà không dùng.
- **Loại:** 2 / 3 · **Mức:** thấp (số 8.1 không bị ảnh hưởng: metric g1 / g3 / g4 / g5 / b1 dùng đều "cao là tốt"; rủi ro thật duy nhất
  là C-02).
- **Quan sát:** cả 6 harness import được, 5 có argparse `--help` rc 0; G1 `runtime` khớp retrieval 7B 108 / 108; `g3 stats` tái lập
  `chunk_list_sha` của h1-h2_512; mọi file `data/` cần đều còn. Plan B1 (`phase_8_2_b1_plan.md:63-64`) và E1 (`:141`) ghi sẽ chép tiếp.
- **Đề xuất:** trước khi viết E1 — tách hàm thuần `paired_stats(a_values, b_values, metric)` trong evaluator (đổi dấu theo
  `LOWER_IS_BETTER`), `paired_compare` gọi nó, harness 8.2 gọi nó; `run_generation` nhận `generator` / `service` tùy chọn. Không sửa harness
  8.1 đã đóng. **Kiểm:** `g1 compare` / `g4_keyword analyze` trên JSONL đã lưu ⇒ JSON giống byte; test với `false_refusal` (đầu vào C-02).

## Đã kiểm, không thấy vấn đề
- `llm/citations.py` (27 dòng): luật từ chối khớp hợp đồng Phase 6 §10 (câu từ chối đúng nguyên văn, không kèm `[n]`); dạng marker:
  xem C-09.
- `frontend/` (`app.js` 107 dòng, `index.html`, `styles.css`, vendor marked 18.0.12 / DOMPurify 3.4.15): render Markdown qua `DOMPurify.sanitize`,
  nguồn dựng bằng `textContent` (không chèn HTML thô), nút thử lại, chặn gửi đôi (`pending`), lỗi hiện `error.message`; chỉ thiếu nối link
  `[Nguồn n]` (C-09).
- `reranking/cross_encoder.py`: chỉ harness G4 và nhánh `minilm` dùng; điểm không hữu hạn / sai số lượng ⇒ `RetrievalDependencyError`
  (đúng hợp đồng). Thừa: `rerank()` (C-11).
- `evaluation/full_corpus_eval.py`: `answer_case` theo đúng thứ tự `chat.py` (retrieval → context → sinh → citation) và ghi rõ chỗ API trả
  500; freshness được kiểm trong `build_full_corpus_retrieval_service` nên evaluator cũng không chạy trên index cũ; `paired_compare` đổi dấu
  đúng cho `LOWER_IS_BETTER`; lệnh `judge-luna` (judge phụ, paid) còn đúng quyết định 7B, 8.1 / 8.2 không dùng — giữ.
- Test (S2): `test_full_corpus_eval.py` (19), `test_golden_full_corpus.py` (8) logic thuần đúng chuẩn; `test_full_corpus_retrieval.py`
  `MockPoint` chỉ là object 2 field cho hàm thuần; `test_citations.py`, `test_full_corpus_context.py` dùng tài liệu Qdrant thật (đọc) +
  tokenizer thật; `test_phase6_settings.py:7-38` khóa cấu hình runtime đã duyệt (cố ý); không test nào trong phạm vi ghi Qdrant hay gọi paid
  khi monkeypatch C-18 còn trúng.
- Harness 8.1 (S3): `g3_chunking.drop` chỉ xóa đúng tên `hue_81_g3_<variant>`, `build` chặn > 3 collection; mọi `g2/*.meta.json` cùng
  `golden_md5`; `assert` P1 / P2 vẫn đúng trên prompt hiện tại.
- `evaluation/golden_full_corpus.py`: CLI kiểm / gộp file Golden (Phase 7A), không gọi mạng; runtime không dùng, nhưng còn giá trị
  khi sửa Golden.

## Không rà được / chưa chắc
- C-01: Qdrant lỗi giữa lúc hỏi (500 thay 503) chưa tái tạo — phải can thiệp vào trong service. Trường hợp model dense không nạp lúc khởi
  động (C-01 thêm / S1-04) chỉ đọc code: probe với HF cache rỗng bị permission chặn.
- 8 test cần `OPENAI_API_KEY` không chạy (không `--env-file` — đúng ranh giới) ⇒ "không gọi mạng khi có key" dựa trên đọc code.
- Harness 8.1: không chạy `run` / `compare` / `analyze`, không chạy `g5_by_category`; model rerank m1 / m2 trong cache HF và GPU chưa kiểm.
- C-19: "`full_corpus_smoke` mặc định FAIL ở ô 8B" suy ra từ code + danh sách collection, chưa chạy `preflight`.
- Generator dùng OpenAI Agents SDK cho một lần gọi không tool. *Giả thuyết* (loại 2 / 7): gọi thẳng Responses API đơn giản hơn;
  chưa đánh giá chi phí đổi.
- Lịch sử sâu trong `phase_6` (`:586-885`) / `phase_8` (`:547-945`) chỉ dò đường dẫn + từ khóa runtime (có nhãn lịch sử Foods).

## Lệch
- `Project_Status.md` §8: lệnh pytest chuẩn có `--env-file ../.env` (brief rà code cấm) và danh sách test ghi Qdrant / paid ghi 4 file không
  còn tồn tại (`test_evaluation.py`, `test_ingestion_pipeline.py`, `test_retrieval_service.py`, `test_llm_generator_openai.py`); §8 còn ghi
  "`test_phase6_live_smoke.py` còn mock — rà ở 8.1 (B8)" nhưng mock vẫn ở `:228, :314`. Governance ⇒ A sửa.
- Spec 8.2 không nêu tên harness 8.1 nào ⇒ "8.2 dùng helper nào" lấy từ plan B1 / E1 và `b1.py` trên nhánh `p82-b1` (đọc bằng `git show`).
  Trên `main`, `backend/experiments/phase_8_2/` chỉ có `__pycache__` sót từ nhánh.
- `guides/README.md:159-161` (ngoài phạm vi C) cùng gốc với C-12.

Script đo (chỉ đọc, private, chạy từ `backend/` bằng `HF_HUB_OFFLINE=1 uv run python -I <file>`): `data/ra_soat_code_2026-10-25/tools/` (`dual_module_check.py`, `exc_identity.py`, `latency.py`, `nguon_count.py`, `cite_shapes.py`, `recheck_both.py` — chạy từ gốc repo, `c01_probe_stale.py`, `c01_probe_bogus_reranker.py`, `brief_common.md`).
