# Review: dọn sau Phase 7 (B9)

Decision: **ready_for_user_confirmation**
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a3`)
Date: 24/10/2026, 19:40–19:53 (giờ lấy bằng `date`)
Canonical guide: đích dọn `reports/phase_7_cleanup_inventory_2026_10_24.md` (C2) §2–§5;
mục việc B9 trong `session_prompt/CURRENT_HANDOFF.md`
Implementation report: `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md`

Review theo skill `risk-gated-agent-review`. C chỉ đọc và chạy kiểm, không sửa code B9, không gọi API
trả phí, không commit.

## 1. Phạm vi đã review

- **Git:** `main` @ `3077b9b`. Working tree có:
  - 42 file tracked bị xóa (` D`);
  - 13 file code/test/notebook sửa (` M`);
  - các file governance/report: report của B, `STATUS_B/C`, `CURRENT_HANDOFF`;
  - một file untracked của User ở gốc (`báo cáo nghiên cứu github.txt`, ngoài phạm vi).

  Khớp report §2–§3.
- **Exact diff đã đọc:**
  - `backend/config/settings.yaml`, `backend/core/settings_loader.py`, `backend/scoring/bm25.py`;
  - `backend/vectorstore/{qdrant,points,upsert}.py`;
  - `backend/tests/{conftest,test_bm25,test_full_corpus_chunker,test_full_corpus_qdrant_ingestion}.py`;
  - `notebooks/{03,04,06}` (phần source).

  Danh sách xóa đã đối chiếu từng mục với C2.
- **Dữ liệu và Qdrant:**
  - liệt kê collection Qdrant;
  - quét payload toàn bộ collection còn lại;
  - kiểm build record, sparse state;
  - kiểm 5 file `data/full_corpus_metadata_v2_*` đã mất;
  - kiểm file authoring 7A còn.
- **Điểm B nhờ xem:** case 81 của smoke 10 lỗi citation.

## 2. Findings

**Không có blocker hoặc major.**

Đối chiếu tiêu chí B9 / C2:

| Tiêu chí | Kết quả |
|---|---|
| Xóa code Foods C2 §2.2, gồm `vectorstore/reset.py` và 2 CSV | Đúng danh sách (42 file + thư mục `ingestion/helpers/`). Không xóa thừa file nào |
| Xóa 10 test Foods C2 §2.3 + bỏ fixture Foods trong `conftest.py` | Đúng. `conftest.py` còn đúng 4 fixture full-corpus (`live_settings`, `require_openai_key`, `full_corpus_service`, `full_corpus_documents`). Grep tên fixture đã bỏ trong `backend/`: 0 kết quả |
| Sửa hàm Foods trong module dùng chung | `qdrant.py`, `points.py`, `upsert.py`, `bm25.py` chỉ bỏ đúng các hàm C2 liệt kê. Import còn lại vẫn được dùng (`math` ở `points.py:32`, `bm25.py:66`). Giữ class `BM25` như C2 cho phép |
| Ràng buộc C2 §3.1 (`full_corpus_eval.py` không import `evaluation.eval`) | Đạt (grep 0) |
| Ràng buộc C2 §3.2 (`settings.yaml` + `settings_loader.py` cùng lượt, giữ `vector_database.url/timeout`) | Đạt. `load_settings()` còn 4 nhóm `full_corpus`, `full_corpus_generation`, `full_corpus_runtime`, `vector_database` |
| Ràng buộc C2 §3.4 (giữ `foods/evaluation/golden_full_corpus_authoring.jsonl`) | Đạt (file còn; `knowledge-base-hue/` không bị đụng) |
| Ràng buộc C2 §3.5 (Qdrant xóa đúng 2 tên, liệt kê trước/sau) | Đạt. Report ghi trước/sau. C liệt kê lại: chỉ còn `hue_full_corpus_7a2_e5_small_384` |
| Notebook: xóa 02/05/07/08a/08b/08c; sửa 03/04/06; outputs rỗng | Đạt. 03/04/06 có 0 output, `execution_count` null hết. Notebook 04 lấy sample id đúng như `full_corpus_pipeline.build_candidate`, bỏ qua candidate không có build record |
| Sửa test chunker 8.460 mà không đổi chunker | Đạt. Test so với `corpus.chunk_count/file_count` của build record đang chạy. Chunker không đổi (không có trong diff) |
| Xóa `requirements.txt`, 5 file `data/full_corpus_metadata_v2_*` | Đạt |
| Không đụng `phase6_live_smoke.py`, `full_corpus_smoke.py`, `session_prompt/` (ngoài STATUS/mục việc của B) | Đạt |
| `git diff --check` | Sạch |

Độ đơn giản: thay đổi chỉ là gỡ code và bớt cấu hình. Không thêm abstraction hay guard mới. Comment
mới bằng tiếng Việt ghi đúng *vì sao* (`test_full_corpus_chunker.py`, `conftest.py`). Không có finding.

**Minor** (không chặn, không mở vòng sửa):

- **m1. Report §4b, câu tả case 81, hơi lệch.** Report ghi "gần trùng chữ… khác vài ký tự cuối". Số
  đo của C:
  - lần chạy mới có 0 ký hiệu `[n]`, các lần 7B có 1–3 ký hiệu;
  - tỉ lệ giống chữ 0,82–0,94.

  Kết luận của B (đầu vào không đổi; thiếu `[n]` là dao động của model) vẫn đúng, xem §4. Tiêu chí
  đóng: B sửa câu tả khi tiện, hoặc giữ nguyên. Không cần vòng sửa.
  **Đã đóng:** B sửa report §4b dòng 106–107 ("không có ký hiệu nguồn `[n]` nào (7B có 1–3 ký hiệu)"); C
  đã đọc lại.

**Ngoài phạm vi B9** (ghi cho A, không đưa vào correction):

- **o1. Tài liệu governance còn nhắc tới thứ đã gỡ.** A sửa khi cập nhật 4 chỗ sau B9.
  - `session_prompt/Project_Status.md:81-82` (2 collection Foods) và `:167-168` (`dense_benchmark.py`,
    `test_reranker_benchmark.py`, `test_markdown_chunker.py`);
  - `guides/full_corpus_rag.md:126`;
  - `session_prompt/chạy_môi_trường.md:13` (`python -m ingestion.pipeline`). C2 §2.7 đề xuất xóa file
    này, nhưng B9 chỉ được giao `requirements.txt`.
- **o2. Dependency không còn ai dùng.** Không phải đích C2. Gỡ dependency cần User duyệt qua A.
  - Sau dọn: `gradio` (chỉ `evaluator.py` dùng), `polars` (2 file Foods), dependency-group `evaluation`
    (`underthesea`, chỉ `sparse_benchmark.py` dùng).
  - Từ trước dọn đã không có import trong `backend/`/`notebooks/`: `beautifulsoup4`, `scikit-learn`,
    `nltk`, `pyarrow`, `requests`.
- **o3.** `backend/test.ipynb`, `backend/scripts/`: B đã hỏi A (report §7), C không xét.

## 3. Cách người kiểm chạy lại thật

Mọi lệnh dùng `uv` trong `.venv` của dự án, `HF_HUB_OFFLINE=1`. Qdrant `127.0.0.1:6335` chỉ đọc
(GET/scroll). Không gọi model sinh. Script và output của C ở `/tmp/c9/`.

```bash
# Pytest 15 file như B (không test nào gọi model: các test /api/chat dừng ở lỗi ngân sách context hoặc generator_ready=False)
cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest -p no:cacheprovider \
  tests/test_full_corpus_{chunker,sparse,embedding,qdrant_ingestion,retrieval,context,eval}.py \
  tests/test_{citations,bm25,golden_full_corpus,phase6_settings,static_ui,api_chat,openai_full_corpus_generator,phase6_live_smoke}.py -q
# So byte retrieval với mốc 7B
HF_HUB_OFFLINE=1 uv run python -m evaluation.full_corpus_eval retrieval --treatment dense_bm25_rrf --out /tmp/c9/retrieval_after.jsonl
cmp /tmp/c9/retrieval_after.jsonl ../data/evaluation/phase_7b/retrieval_dense_bm25_rrf_1.jsonl
# Sức khỏe kiểu B1 (script riêng của C, không dùng script của B): settings, discovery + freshness, chunker,
# sparse state, Qdrant list/info, quét payload 8.459 point, 1 retrieval, /health in-process
HF_HUB_OFFLINE=1 uv run --env-file ../.env python -I /tmp/c9/health_c.py
HF_HUB_OFFLINE=1 uv run python -I /tmp/c9/chunks_c.py
# Golden
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus.jsonl
HF_HUB_OFFLINE=1 uv run python -m evaluation.golden_full_corpus check ../knowledge-base-hue/evaluation/golden_full_corpus_smoke.jsonl
# Notebook 03, 04 Run All trên bản tạm (nbclient, output ghi ra /tmp/c9/*_run.ipynb)
HF_HUB_OFFLINE=1 uv run python /tmp/c9/run_nb.py 03_embedding_models 04_qdrant_ingestion
```

Case 81: so `/tmp/phase7_cleanup/smoke_generate.jsonl` (B) với `data/evaluation/phase_7b/{smoke_answers_1,
run1_answers,run2_answers}.jsonl`. Chỉ đếm ký hiệu `[n]`, độ dài, nguồn context; không in nội dung.

## 4. Kết quả quan sát

| Kiểm | Kết quả (mới, C chạy) |
|---|---|
| Pytest 15 file | **PASS**: 191 passed, 0 failed, 142,8 s (khớp B: 193 trước dọn − 2 test của 2 hàm BM25 đã xóa) |
| So byte retrieval | **PASS**: giống từng byte, 158 dòng, SHA-256 `cefb2d1a…826e4` cả hai file |
| Settings | **PASS**: `load_settings()` ổn, còn 4 nhóm |
| Corpus / build record | **PASS**: discovery 205 file = record 205; freshness đúng, 0 lệch; chunker cho 8.459 chunk, 0 lỗi chặn = `corpus.chunk_count`; record `full_corpus_build:v3`, `complete` |
| Sparse state | **PASS**: SHA khớp record; vocabulary 5.660 |
| Qdrant | **PASS**: chỉ còn `hue_full_corpus_7a2_e5_small_384`; `green`, 8.459 point; dense 384, có `sparse` |
| Payload | **PASS**: quét đủ 8.459 point, 0 point khác đúng 7 field (`chunk_id, domain, evidence_parts, heading_path, search_text, source, title`) |
| Retrieval + API | **PASS**: `build_full_corpus_retrieval_service("e5-small-384","dense_bm25_rrf","none").search(...)` trả 10 document. `/health` in-process **200**, `status: ok`, qdrant/retrieval/tokenizer/generator `ready` |
| Golden | **PASS**: official 176 câu (75/29/29/25/18), smoke 10 câu; exit 0 |
| Notebook 03, 04 | **PASS**: Run All 0 lỗi (7 và 5 cell); notebook trong repo không đổi |
| Dữ liệu private | **PASS**: 5 file `data/full_corpus_metadata_v2_*` không còn; file authoring 7A còn |

**Case 81 (smoke, lỗi "Grounded answer has no citation"):**

- **Đã chứng minh:** đầu vào của model không đổi do dọn.
  - Cùng `context_sources` với cả 3 lần chạy 7B.
  - `top_chunk_ids` giống, theo B. Retrieval giống byte theo kiểm của C.
  - Code sinh/prompt/citation không có trong diff.
- **Quan sát thêm** (ủng hộ giả thuyết của B, chưa phải chứng minh nguyên nhân): ngay trong 7B, giữa
  Run 1 và Run 2 với cùng code và cùng input, **6/176 case đổi trạng thái lỗi citation** (Run 1 có 4
  lỗi, Run 2 có 6, chỉ 2 case lỗi ở cả hai). Vậy lỗi citation dao động giữa các lượt sinh của
  `gpt-6-luna` là hiện tượng đã có trước B9.
- **Kết luận:** không phải lỗi do B9. Bất ổn citation đã có trong bảng rà 8.1 (dòng 6.5, 6.6 của
  `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md`).

**Dùng lại bằng chứng của B (không gọi là mới):**

- **Smoke 10 có phí** (0,0013334 USD; 10 call, 0 lỗi kỹ thuật). C không chạy lại vì việc C9 không có
  quyền paid. Bằng chứng còn hợp lệ: sau lượt smoke, diff code không đổi; thay đổi duy nhất sau đó là
  xóa 2 collection Foods, không nằm trên đường sinh. `/health` và retrieval do C chạy lại sau khi xóa
  đều đạt.
- **Notebook 06** không chạy (có gọi OpenAI trả phí); chỉ sửa markdown, đã đọc diff.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy smoke 10 có phí (dùng lại của B, lý do ở §4).
- Không chạy notebook 06 (có phí; chỉ đổi markdown).
- Các test Foods đã xóa không được chạy trước khi xóa (ghi Qdrant hoặc có phí). Đây là chủ ý theo C2
  §2.3, không ảnh hưởng runtime full-corpus.
- Không kiểm `pyproject.toml`/`uv.lock` vì không thuộc đích B9 (xem o2).

## 6. Decision và bước tiếp theo

**`ready_for_user_confirmation`.** Hệ thống full-corpus chạy bình thường sau dọn:

- kết quả tìm kiếm giống từng byte với mốc 7B;
- 191 test đạt;
- `/health` 200;
- corpus, chỉ mục và payload nguyên vẹn;
- Qdrant còn đúng 1 collection đang dùng.

B9 là việc rủi ro cao (xóa code + 2 collection), nên A trình User để đóng. User cần xác nhận:

- đồng ý kết quả dọn: code/test/notebook Foods đã gỡ; 2 collection Foods và 5 file metadata v2 đã
  xóa — không hoàn tác được, không có snapshot (theo C2 §2.1);
- tùy chọn: có gỡ dependency không dùng (o2) không.

Sau khi User đóng:

- A commit theo từng đường dẫn (`git diff --cached --stat`);
- cập nhật `Project_Status.md` §4/§8, `guides/full_corpus_rag.md` và `bao_cao_he_thong/` (4 chỗ, o1);
- xử lý `session_prompt/chạy_môi_trường.md` (o1).

Minor m1 không cần vòng sửa.
