# Project Status

Last updated: `2026-10-24` (A, mở Phase 7B)

Chỉ ghi hiện trạng (quy tắc: Governance v2 §6). Lịch sử và lý do các quyết
định cũ: `PROJECT_HISTORY.md`. Việc đang làm của từng session: `CURRENT_HANDOFF.md`.

## 1. Tổng quan

`hue_rag` là chatbot RAG về văn hóa và du lịch Huế, trả lời từ kho tri thức
curated `knowledge-base-hue/` (5 domain: `foods`, `heritages`, `festivals`,
`performing_arts`, `travel`). Ưu tiên code/data flow dễ hiểu, độ phức tạp tương
xứng nhu cầu và bằng chứng từ dữ liệu, Qdrant, model, API thật.

```text
curated Markdown (205 file) -> chunker (8.459 chunk) -> e5-small dense + BM25 sparse
-> Qdrant -> retrieval dense_bm25_rrf (top-5 whole chunk) -> gpt-6-luna -> API/UI có citation
```

Làm việc theo mô hình A/B/C (Governance v2, User duyệt 2026-10-24): A điều phối
và làm việc với User; B, C thực thi; review chéo; cả ba Claude Opus 5.5.

## 2. Phase hiện tại

**Phase 7A2 — Sửa corpus + tạo lại index: User-closed 2026-10-24** (spec
`docs/superpowers/specs/2026-10-23-phase-7a2-corpus-correction-reindex-design.md`,
plan `docs/superpowers/plans/2026-10-23-phase-7a2-corpus-correction-reindex-implementation-plan.md`):

- Gate 1 (sửa 25 mục corpus): User-closed 2026-10-24.
- Gate 2 (build index + cutover): User-closed 2026-10-24 **với giới hạn** — chỉ
  index e5; index 8B hoãn sang Phase 8.
- Gate 3 (xóa 13 collection + build record cũ): User-closed 2026-10-24
  (`reports/phase_7a2_gate_3_review_2026_10_24.md`).
- Đóng Phase: backup Gate 1 đã xóa; guide `guides/full_corpus_rag.md` có mục cập
  nhật 7A2 + ghi chú Phase 8; user report
  `reports/user_reports/phase_7a2_corpus_correction_reindex_user_report_2026_10_24.md`.

Mốc kế tiếp: **Phase 7B** (evaluator, baseline 176 case trên chunker hiện hành) —
brainstorm với User, một tài liệu thiết kế. Song song: C rà soát lựa chọn Phase
2–6 cho Phase 8.

## 3. Bảng Phase

| Phase | Status | Kết quả / ranh giới |
|---:|---|---|
| 0–1 | `approved` | MVP foundation, simplicity governance, backend foundation |
| 2 | `approved` | Foods chunking; full-corpus chunker/locator (205 file) |
| 3 | `approved` | Embedding/sparse preflight (lịch sử; module preflight đã xóa ở 7A2) |
| 4 | `approved` | Qdrant ingestion 4 collection legacy (xóa ở 7A2 Gate 3) |
| 5 | `approved` | Retrieval profiles/reranking |
| 6 | `approved` | Generation/API/UI trên `gpt-6-luna`, live 4/5; giới hạn F1 (đa nguồn), F2 (bảng giá ngoài top-30) |
| 7 | `approved` | Evaluation baseline Foods (lịch sử) |
| 7A | `approved` | Golden full-corpus 176 case + smoke 10 (private) |
| 7A2 | `approved` | User-closed 2026-10-24; giới hạn: index 8B hoãn sang Phase 8 |
| 7B | `in_progress` | Evaluator full-corpus + baseline 176 case; spec 2026-10-24 approved |
| 8 | `not_ready` | Đợt ổn định trước Phase 9 (mục 5); spec/plan phải thiết kế lại |
| 9 | `not_ready` | Agentic RAG / Hybrid Recommender — roadmap, chưa có scope |

## 4. Runtime và dữ liệu đang chạy

**Full-corpus runtime (API `backend/api/app.py`):**

- candidate `e5-small-384` (`intfloat/multilingual-e5-small`, local CPU, 384 chiều);
- collection `hue_full_corpus_7a2_e5_small_384`, 8.459 point, payload 7 field
  (`search_text`, `source`, `title`, `heading_path`, `evidence_parts`,
  `chunk_id`, `domain`), dense + sparse;
- build record `data/full_corpus_builds/hue_full_corpus_7a2_e5_small_384.json`
  (schema `full_corpus_build:v3`) là nguồn sự thật duy nhất "index khớp corpus";
  runtime từ chối khởi động nếu hash file corpus khác record;
- sparse state chung `data/full_corpus_builds/full_corpus_sparse_state.json`
  (vocabulary 5.660);
- retrieval `dense_bm25_rrf`, reranker `none`, context tối đa 5 whole chunk;
- generation `gpt-6-luna` (OpenAI); config `backend/config/settings.yaml`
  (`full_corpus_runtime`, `full_corpus_generation`).

**Candidate dense trong code** (`backend/embedding/full_corpus.py`):
`e5-small-384` (local) và `qwen3-embedding-8b-4096` (OpenRouter
`qwen/qwen3-embedding-8b`, pin Nebius, `data_collection: deny`, batch 64) —
8B chưa có index.

**Qdrant** `127.0.0.1:6335` (gRPC 6336; port đổi để chạy song song
`mekongai-template`). Còn đúng 3 collection (sau Gate 3):
`hue_full_corpus_7a2_e5_small_384`, `hue_foods_e5_small_384` (572),
`hue_foods_e5_small_384_dense` (572). Hai collection Foods không đứng sau API nào;
chỉ settings/tests/benchmark Foods cũ tham chiếu; collection Foods còn địa chỉ cũ
"An Đông" ở 5 quán AEON.

**Corpus:** 205 file → 8.459 chunk (chunker giữ nguyên từ Phase 2: chia theo cấu
trúc Markdown, không overlap, mỗi chunk vừa cả 3 tokenizer e5-small 512 / e5-base
512 / huydang 256; trung vị 85 token e5). `knowledge-base-hue/` không có Git
(`.gitignore`); backup Gate 1 đã xóa khi đóng Phase 7A2.

**Golden:** `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` (176 case),
`golden_full_corpus_smoke.jsonl` (10, deep-equal); schema 4 field `question`,
`keywords`, `reference_answer`, `category`; private. Foods Golden V3 (45 + 10)
là lịch sử.

## 5. Quyết định đang hiệu lực

| Ngày | Quyết định | Nguồn |
|---|---|---|
| 2026-10-24 | User ủy quyền A: tự điều phối B/C, tự kiểm tra, đề xuất, thử nghiệm, tối ưu và phát triển các Phase trước; commit/push theo mốc; ghi report; hệ thống phải chạy ổn định; dùng skill khi code | User (trước khi nghỉ) |
| 2026-10-24 | Giá `gpt-6-luna`: 0,1 USD/1M input, 0,5 USD/1M output. Ngân sách session ≤1 USD (tối đa 1,5 USD), không cần dùng hết | User |
| 2026-10-24 | Phase 7B: judge chính là Claude (session Claude Code), `gpt-6-luna` chỉ sinh + judge phụ; User chấm ~20 case; đo nhiễu (thay judge `gpt-6-luna` cũ) | `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` |
| 2026-10-24 | Mô hình A/B/C, review chéo, quy trình theo rủi ro, một tài liệu thiết kế/Phase, STATUS riêng mỗi session; duyệt cho A = duyệt cho B/C | `docs/superpowers/specs/2026-10-24-governance-v2-design.md` |
| 2026-10-24 | Index 8B hoãn sang Phase 8; khi build lại thiết kế cách gọi chịu 504/429 (batch, thử lại) | `reports/phase_7a2_gate_2_review_2026_10_24.md` §6 |
| 2026-10-24 | OpenRouter 8B pin Nebius (`order:[nebius]`, `allow_fallbacks:false`) | spec 7A2 §5.2 |
| 2026-10-24 | Giữ 2 collection Foods qua Phase 7; sau Phase 7 A đề xuất xóa mọi collection không dùng (kèm gỡ code/test/notebook Foods cũ) | User |
| 2026-10-24 | Chunker giữ nguyên tới khi có baseline 7B | User |
| 2026-10-24 | Code/test/script luôn chạy bằng `uv` trong `.venv` của dự án | `Session_Prompt.md` §10 |
| 2026-10-24 | Kênh liên lạc: Claude Code ↔ Claude Code `trực tiếp` (SendMessage); có Codex/AGY thì `qua User` (khối "Tin cho <X>") | `WORKFLOW.md` §7 |
| 2026-09 (giữ) | Phase tuần tự `7A2 → 7B → 8 → 9`; trước Phase mới: Phase trước review + User đóng, cập nhật guide bằng bằng chứng, rồi một tài liệu thiết kế User duyệt | `WORKFLOW.md` §9.4 |
| 2026-10-24 | Phase 8 = đợt ổn định: chunk size/gộp chunk vụn, reranker đa ngôn ngữ, truy xuất bảng giá (F2), tổng hợp đa nguồn (F1), BM25 tiếng Việt (tách từ/bigram), rà lại lựa chọn các Phase trước | User |
| 2026-10-23 | Dense full-corpus chỉ e5-small + qwen3-embedding-8b; build thẳng metadata v2; build record là nguồn sự thật; runtime mặc định e5-small, cutover 8B chờ bằng chứng 7B/8 | spec 7A2 §2 |
| 2026-10-23 | Mọi model OpenAI (generation, evaluation answer/judge) là `gpt-6-luna` | `docs/superpowers/specs/2026-10-23-phase-6-gpt-6-luna-amendment.md` |
| 2026-10-23 | Golden 176 + smoke 10; retrieval K=10; 3 metric answer thang 1–5; macro-average theo case; lỗi kỹ thuật làm run incomplete; chưa đặt ngưỡng trước baseline | `docs/superpowers/specs/2026-10-23-phase-7a-golden-full-corpus-design.md` |
| 2026-09-29 | Payload metadata v2 đúng 7 field; `domain` = thành phần đầu của path; không payload index/filter | `docs/superpowers/specs/2026-09-29-full-corpus-metadata-v2-written-spec.md` |
| 2026-09-11 | Full-corpus umbrella: chia theo cấu trúc, evidence slice từ source, citation đọc `evidence_parts`, context whole-chunk top-5 | `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md` |
| 2026-09-08 | Taxonomy `knowledge-base-hue/travel/{places,services,tickets}`; inventory bị loại khỏi discovery | `PROJECT_HISTORY.md` |
| — | User ưu tiên mặc định đơn giản, nhưng mặc định phải được kiểm bằng bằng chứng thật | User |

## 6. Ranh giới an toàn

- Qdrant: chỉ đọc, trừ đích chính xác được ghi trong việc của session.
- `knowledge-base-hue/`, `data/`, Qdrant storage, Golden, trace chi tiết và
  `gửi chatgpt/` là private: không commit, không chép nội dung vào report tracked.
- Sửa corpus: backup vào `knowledge-base-hue/meta/` trước, review bằng diff.
- Data egress: chỉ gửi chunk/query tới OpenRouter cho `qwen/qwen3-embedding-8b`
  trong việc đã duyệt; mọi request `data_collection: deny`.
- Không đọc/in/log `.env` hay secret; dùng `uv run --env-file .env`.
- Provider/model/dataset mới, paid run ngoài giới hạn đã ghi, deploy, xóa dữ
  liệu: cần User duyệt qua A.
- Git: A được commit/push (User 2026-10-24); B/C không commit trừ khi việc ghi rõ.

## 7. Bản đồ tài liệu đang dùng

```text
session_prompt/START_SESSION.md        mở mọi session
session_prompt/Session_Prompt.md       luật chung
session_prompt/WORKFLOW.md             cách làm, việc thêm của A
session_prompt/CURRENT_HANDOFF.md      việc đang mở của A/B/C
session_prompt/sessions/STATUS_*.md    ngữ cảnh riêng từng session
session_prompt/PROJECT_HISTORY.md      lịch sử (reference-only)
session_prompt/TEMPLATE_*.md           mẫu report
skills/{practical-project-coding,risk-gated-agent-review,propose-options}/SKILL.md
guides/full_corpus_rag.md              guide umbrella full-corpus
docs/superpowers/specs/, docs/superpowers/plans/   thiết kế từng Phase
reports/phase_7a2_*                    report + review Phase 7A2
reports/user_reports/                  report cho User
handoff_prompt/README.md               contract lịch sử (reference-only)
```

## 8. Bẫy kỹ thuật đã biết

- Chunker và e5 cần tokenizer trong HF cache; chạy với `HF_HUB_OFFLINE=1`. Cảnh
  báo "Token indices sequence length…" là bình thường.
- Sửa corpus làm runtime từ chối khởi động (freshness) cho tới khi build lại index.
- `full_corpus_sparse_state.json` chỉ ghi một lần: corpus đổi thì phải xóa file cũ
  trước khi build lại, nếu không build raise.
- Pytest chạy từ `backend/`: `cd backend && HF_HUB_OFFLINE=1 uv run --env-file ../.env python -m pytest tests/<file> -q`;
  không chạy test có paid call ngoài giới hạn (ví dụ `test_llm_generator_openai.py`).
- Pytest lấy **gốc repo** làm rootdir: node id là `backend/tests/<file>::<test>`; `--deselect tests/…` không khớp và không bỏ được test (B1 2026-10-24: lỡ chạy 1 paid call trả 400 + một collection tạm tự xóa). Bỏ test ghi/paid bằng cách liệt kê file cần chạy, không dựa vào `--deselect`. Test ghi Qdrant/paid: `test_evaluation.py` (một phần), `test_ingestion_pipeline.py`, `test_retrieval_service.py`, `test_llm_generator_openai.py`, benchmark.
- Generator/evaluator Foods cũ (`llm/generator_openai.py`) gửi `temperature` → `gpt-6-luna` trả 400; đường full-corpus không dùng tham số này.
- OpenRouter 8B: không pin thì trộn provider (vector lệch, cos ~0,996); pin Nebius
  thì 10–30 s/batch và đã gặp 504; DeepInfra từng trả 429.
- Notebook 06, 08a, 08b còn tên collection/model cũ đã xóa (gãy); notebook 04
  chưa kiểm hành vi với 2 candidate mới; notebook 03 còn
  markdown mô tả 4 model — dọn sau Phase 7.
- Permission tự động của từng session có thể chặn `rm`/`pkill`: session đó dừng và
  nhờ User chạy bằng `!` trong terminal của nó; session khác không chạy hộ.
- Memory Claude dùng chung cho cả ba session (cùng thư mục dự án).
