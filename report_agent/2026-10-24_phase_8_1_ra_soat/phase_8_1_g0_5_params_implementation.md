# Implementation Report: Phase 8.1 G0.5 — tham số mặc định-như-cũ cho code production (B11)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-b0`)
Date: 2026-10-24 20:55–21:05 +0700 (lấy bằng `date`)
Việc: `session_prompt/CURRENT_HANDOFF.md` → B11; spec `docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` §3.1, §5 G0.5, §6.1
Canonical guide: `guides/full_corpus_rag.md` (không sửa — thuộc A)

## 1. Phạm vi

Thêm **tham số keyword, mặc định = giá trị đang chạy** đúng ở các chỗ spec §3.1 liệt kê, để harness 8.1 gọi
code production thay vì dựng đường đi thứ hai. Không đổi giá trị mặc định, không thêm key vào `settings.yaml`,
không sửa loader, không thêm abstraction. Không đụng `backend/evaluation/` (C16 đang làm song song), không
đụng chunker, không thêm logic chia đoạn mới.

## 2. Thay đổi chính (3 file, `git diff --stat`: +97 / −26 dòng)

| File | Tham số mới (mặc định) | Ghi chú |
|---|---|---|
| `backend/llm/generator_openai_full_corpus.py` | `answer_instructions` (= `ANSWER_SYSTEM_INSTRUCTIONS`), `reasoning_effort` (= `None`) ở `__init__` và `from_environment` | `None` ⇒ `ModelSettings(reasoning=None)`, đúng bằng mặc định của SDK như trước; có giá trị ⇒ `Reasoning(effort=…)`. Agent Representation B không đổi |
| `backend/retrieval/full_corpus.py` | `FullCorpusRetrievalService`: `candidate_pool` (30), `rrf_k` (60), `search_params` (`None`). `build_full_corpus_retrieval_service`: thêm `collection_name` (`None` = collection runtime của candidate), `record_path` (`None` = record cạnh collection), `sparse_state_path` (= `SPARSE_STATE_PATH`) + chuyển tiếp 3 tham số trên | `candidate_pool` dùng cho `limit` của cả hai `query_points` (dense, sparse) **và** `limit` của RRF — runtime đang 30/30/30. `search_params` truyền vào cả hai `query_points` (`None` = mặc định client; `models.SearchParams(exact=True)` cho G1.2). Đổi tên collection bằng `dataclasses.replace` trên candidate, nên kiểm record (`collection_name`), query và trace cùng dùng tên mới. Thông báo lỗi dùng `_repo_relative()` — với đường mặc định ra đúng chuỗi cũ `data/full_corpus_builds/<tên>` |
| `backend/ingestion/full_corpus_pipeline.py` | `prepare_full_corpus_input(embedding_models=None)`; `build_candidate(…, collection_name=None, sparse_state_path=SPARSE_STATE_PATH, record_path=None, embedding_models=None)` | `embedding_models` thay `full_corpus.embedding_models` trên **bản sao** settings rồi đưa vào `chunk_full_corpus` (chunker đã nhận settings, không cần sửa chunker). `record_path` không có trong danh sách §3.1 nhưng cần cho §3.2 (build record biến thể ở `data/phase_8_1/builds/`), nên thêm cùng lượt |

## 3. Cách đã chạy thật

Mọi lệnh bằng `uv` trong `.venv` dự án, `HF_HUB_OFFLINE=1`, Qdrant `:6335` chỉ đọc, 0 call trả phí.
Log/kết quả ở `/tmp/b11/` (có thể mất).

1. **So byte retrieval (gate).** Vì C đang sửa `backend/evaluation/full_corpus_eval.py` (C16) trong cùng
   working tree, B chạy **bản HEAD** của evaluator: `git show HEAD:backend/evaluation/full_corpus_eval.py`
   → `/tmp/b11/full_corpus_eval_head.py`, chỉ đổi 2 dòng `REPO_ROOT`/`BACKEND_DIR` thành đường tuyệt đối
   (`diff` chỉ 2 dòng đó), rồi
   `cd backend && HF_HUB_OFFLINE=1 uv run python /tmp/b11/full_corpus_eval_head.py retrieval --treatment dense_bm25_rrf --out /tmp/b11/retrieval_after.jsonl`
   + `cmp` với `data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl`. Như vậy: evaluator HEAD + code
   production của B11.
2. Như trên với `--treatment native_hybrid_rrf` (ngoài gate; B sửa cả nhánh sparse), so với
   `retrieval_native_hybrid_rrf_1.jsonl`; vì khác, chạy lại bằng **code HEAD hoàn toàn**: `git archive HEAD backend`
   → `/tmp/b11/head/`, symlink `data/` và `knowledge-base-hue/` (chỉ đọc), xác nhận module import từ
   `/tmp/b11/head/backend/...`, rồi `uv run --project <repo> python -m evaluation.full_corpus_eval retrieval --treatment native_hybrid_rrf`.
3. **Pytest 15 file** (liệt kê file, không `--deselect`):
   `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest tests/test_full_corpus_chunker.py tests/test_full_corpus_sparse.py tests/test_full_corpus_embedding.py tests/test_full_corpus_qdrant_ingestion.py tests/test_full_corpus_retrieval.py tests/test_full_corpus_context.py tests/test_citations.py tests/test_bm25.py tests/test_golden_full_corpus.py tests/test_phase6_settings.py tests/test_static_ui.py tests/test_full_corpus_eval.py tests/test_api_chat.py tests/test_openai_full_corpus_generator.py tests/test_phase6_live_smoke.py -q -p no:cacheprovider`.
4. **`/health` in-process + dùng thật tham số mới** (`/tmp/b11/param_check.py`): `create_app(load_settings())`
   + lifespan + `httpx.ASGITransport`; dựng service mặc định vs service truyền tường minh đúng tên collection,
   record, sparse state runtime; dựng service `candidate_pool=100, rrf_k=10, search_params=SearchParams(exact=True)`;
   dựng generator mặc định và generator có `answer_instructions`/`reasoning_effort` (client `None`, không gọi mạng).
5. **Tham số tokenizer của build:** `prepare_full_corpus_input()` vs
   `prepare_full_corpus_input(embedding_models=[e5-small])` (chạy chunker trên máy, không ghi file/Qdrant).
   `build_candidate` **không chạy** (sẽ ghi Qdrant + build record — ngoài quyền B11).
6. `git diff --check` trên 3 file.

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| Retrieval `dense_bm25_rrf` (gate) | **PASS**: giống từng byte mốc, SHA-256 `cefb2d1a…826e4`, 158 dòng (176 case; 18 `out_of_scope` không có dòng retrieval — như mốc) |
| Pytest 15 file (gate) | **PASS**: 195 passed, 0 failed, 0 error (163 s). 191 là bộ cũ + 4 test C16 mới trong `test_full_corpus_eval.py` (file đó đang chứa thay đổi dở của C) |
| `/health` in-process (gate) | **PASS**: 200, `status: ok`, mọi thành phần `ready` |
| Service truyền tường minh tên collection/record/sparse runtime | cùng top-10 với service mặc định |
| Service `pool=100, k=10, exact=True` | chạy được; `counts`: dense 100, bm25 100, rrf 100, final 10 |
| Generator mặc định | `reasoning=None`, instructions = `ANSWER_SYSTEM_INSTRUCTIONS` |
| Generator tùy chỉnh | `Reasoning(effort='low')`, instructions = chuỗi truyền vào |
| `prepare_full_corpus_input` mặc định / chỉ e5-small | 8.459 / **8.398** đoạn (identity khác); settings gốc vẫn 3 tokenizer. Số 8.398 là quan sát phụ, có ích cho H1 ở G3 — chưa phải kết quả thí nghiệm |
| Retrieval `native_hybrid_rrf` (ngoài gate) | B11 **khác** mốc 7B ở 6/158 câu (chỉ `top_chunk_ids`/MRR/nDCG); **code HEAD cho kết quả giống hệt B11** ⇒ khác biệt có trước B11, không do B11. Nguyên nhân **chưa tìm** (giả thuyết: mốc native 7B sinh ở code/thời điểm khác, hoặc hòa điểm ở biên top-30 sparse) |
| `git diff --check` | sạch |

Tiền: **0 USD**.

## 5. Lỗi và giới hạn

- **Mốc `native_hybrid_rrf` của 7B không tái lập** bằng code hiện tại (6/158 câu). G1.3 so hybrid độc lập với
  runtime: theo skill `run-experiment` §3.1 ("baseline khác byte mốc đã lưu thì dừng, tìm nguyên nhân") cần chốt
  trước G1: dùng lượt chạy mới làm mốc native, hay tìm nguyên nhân trước. B đề xuất: chạy native 2 lần bằng HEAD
  để biết có dao động giữa lượt không (free), rồi A quyết.
- `build_candidate` với tham số mới chưa chạy end-to-end (ghi Qdrant). Lần chạy thật đầu tiên sẽ ở harness G3
  (`hue_81_*`); khi đó kiểm record/sparse state đúng chỗ.
- Ranh giới khâu còn dính, **ngoài phạm vi B11** (không sửa, ghi theo luật skill "Ranh giới theo khâu pipeline"):
  1. `build_candidate` chỉ build từ `chunk_full_corpus` — **không nhận danh sách chunk** do harness xử lý tiếp
     (spec §3.1: logic chia đoạn mới nằm trong harness). G3 cần một lối vào nhận `chunks` (hoặc tách bước
     prepare/build); nếu không harness sẽ phải chép phần build — đúng thứ luật cấm.
  2. `prepare_full_corpus_input`/`build_candidate` tự đọc settings bên trong (`_phase4_settings()` gọi
     `load_settings()` và ép URL/timeout Qdrant); Qdrant client tạo bên trong, không truyền vào được.
  3. Retrieval: top-k cuối `fused[:10]` vẫn là hằng (`retrieval/full_corpus.py`, nhánh `reranker == "none"`
     và `minilm`); dense runner tạo trong factory; câu warm-up cứng. BM25 `K1`/`B` là hằng ở `scoring/bm25.py`
     (spec §4 để NOT RUN nên chưa cần).
  4. `candidate_pool` gộp "pool mỗi nhánh" và "số giữ sau RRF" (đúng runtime 30/30). Nếu G1/G4 cần tách
     (ví dụ pool 100 nhưng chỉ rerank 30) thì thêm tham số riêng lúc đó.

## 6. Bàn giao cho người kiểm (C)

- Đọc trước: §2 bảng thay đổi; `git diff -- backend/llm/generator_openai_full_corpus.py backend/retrieval/full_corpus.py backend/ingestion/full_corpus_pipeline.py`.
- Chạy lại then chốt: so byte `dense_bm25_rrf` (lưu ý tách evaluator HEAD khỏi thay đổi C16 như §3.1, hoặc
  chạy sau khi C16 xong); pytest 15 file; `/health` (`/tmp/b11/param_check.py`, chạy từ `backend/` với `PYTHONPATH=.`).
- Không commit (A commit theo gate). File của B: đúng 3 file trên + report này + `STATUS_B.md` + dòng B trong `CURRENT_HANDOFF.md`.

## 7. Review governance A nhờ (A tự viết → B kiểm)

**Skill `practical-project-coding` mục "Ranh giới theo khâu pipeline":** rõ, khớp luật đơn giản (abstraction
vẫn phải có bằng chứng) và đúng cách B11 làm. Hai góp ý nhỏ: (a) nói rõ "tham số" là keyword có mặc định trong
code, **không** phải key mới trong `settings.yaml` — tránh người sau hiểu "không giấu hằng số" = đẩy hết vào
cấu hình; (b) "kiểm runtime không đổi … retrieval giống từng byte mốc" chỉ có nghĩa khi mốc tái lập được —
thêm "mốc được chạy lại bằng code HEAD trước khi sửa" (bài học native hybrid ở §4).

**Skill `run-experiment`:** đủ bước (ghi trước, một biến, theo cặp/tầng, dev/check, giữ phương án bỏ, trần).
Góp ý: (a) §3.1 "baseline khác byte mốc đã lưu thì dừng" — đúng, nhưng nên ghi bước xử lý: chạy lại baseline 2
lần bằng HEAD, nếu tự nó không ổn định thì ghi dao động và dùng lượt mới làm mốc sau khi A duyệt (nếu không
G1.3 sẽ kẹt ngay vì mốc native 7B không tái lập); (b) khuôn YAML ghi `split: phase_8_1/split.json` — nên ghi
đường đầy đủ `knowledge-base-hue/evaluation/phase_8_1/split.json` như §2 cho khỏi lệch; (c) §3.2 "build record
+ sparse state riêng" hiện làm được nhờ B11, nhưng còn thiếu lối vào nhận chunk của harness (§5 mục 1) — G3
chưa chạy được đúng luật cho tới khi có. Không thấy chỗ nào trái `Session_Prompt.md`/`WORKFLOW.md`.
