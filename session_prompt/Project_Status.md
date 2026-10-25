# Project Status

Last updated: `2026-10-25 11:05` (A, kết phiên sáng — cải tiến cách làm; chatbot và Phase 8.1 không đổi)

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

**Phase 7B — Evaluator full-corpus + baseline 176 case: User-closed 2026-10-24** (spec
`docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md`; report
`reports/phase_7b_*`, review `reports/phase_7b_review_2026_10_24.md`; guide mục "Cập nhật Phase 7B").

- Baseline (Claude judge, Run 1): Accuracy 4,43 / Completeness 4,28 / Relevance 4,45; keyword proxy
  @10 MRR 0,721 / nDCG 0,755 / Coverage 92,35; từ chối nhầm 22/158; lỗi citation 4/176.
- Thước đo ổn định (Run 1 vs Run 2 chênh TB ≤0,011); **giới hạn:** chưa có mốc người (User bỏ chấm tay).
- Tiền paid cả 7B + thăm dò: ~0,087 USD.

Mốc kế tiếp: **Phase 8.1** (rà quyết định + thí nghiệm, không đổi chatbot) — spec approved 20:49 24/10; G0 gần xong, G1 xong (22:00), tiếp G4/G2 chờ A duyệt plan B16;
input: bảng rà 56 quyết định `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_decision_inventory.md`
(C11), giả thuyết `reports/phase_8_candidate_hypotheses_2026_10_24.md`, chẩn đoán từ chối nhầm
(`reports/phase_7b_false_refusal_diagnosis_2026_10_24.md`), thăm dò context 10
(`reports/phase_8_probe_context_top10_2026_10_24.md`), nghiên cứu ChatGPT
`gửi chatgpt/2026-10-24/kết quả nghiên cứu/phase_8_1_decision_audit_2026_10_24.md` (private).
Dọn Foods sau Phase 7 (B9) **đóng** 24/10.

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
| 7B | `approved` | User-closed 2026-10-24: evaluator + baseline 176 (Claude judge); giới hạn: chưa có mốc người |
| 8.1 | `in_progress` | Spec approved 20:49 24/10; G0 gần xong (chờ User: câu kín, 9 nhãn tự nhiên; G0.6 chưa khóa); **G1 xong**: nghẽn ở xếp hạng; không đổi chatbot (đợt `report_agent/2026-10-24_phase_8_1_ra_soat/`) |
| 8.2 | `not_ready` | Cải tiến dựa trên số đo 8.1; thiết kế sau khi User đóng 8.1 |
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
`mekongai-template`). Còn đúng **1 collection** `hue_full_corpus_7a2_e5_small_384` (8.459
point). Hai collection Foods đã xóa ở B9 (24/10, User chạy); code/test/notebook Foods cũ đã gỡ
(`1832201`).

**Corpus:** 205 file → 8.459 chunk (chunker giữ nguyên từ Phase 2: chia theo cấu
trúc Markdown, không overlap có chủ đích (thực tế 3 cặp chunk lặp body: blockquote lồng trong list
item, `markdown_blocks.py:233-250`, B8 2026-10-24), mỗi chunk vừa cả 3 tokenizer e5-small 512 / e5-base
512 / huydang 256; trung vị 85 token e5). `knowledge-base-hue/` không có Git
(`.gitignore`); backup Gate 1 đã xóa khi đóng Phase 7A2.

**Golden:** `knowledge-base-hue/evaluation/golden_full_corpus.jsonl` (176 case),
`golden_full_corpus_smoke.jsonl` (10, deep-equal); schema 4 field `question`,
`keywords`, `reference_answer`, `category`; private. Foods Golden V3 (45 + 10)
là lịch sử.

## 5. Quyết định đang hiệu lực

| Ngày | Quyết định | Nguồn |
|---|---|---|
| 2026-10-25 (chiều) | 8.1 G4: duyệt G4-A (xếp lại top-10) **và G4-B** (rerank pool 100 → top-10; sửa spec §5 G4). GPU yếu ⇒ mỗi lượt GPU chỉ 20–30 câu, kiểm model thật trên GPU trước khi chạy (không chạy nhầm CPU) | User; spec 8.1 §5 G4 "Sửa đổi 25/10" |
| 2026-10-25 | Cải tiến cách làm (không đổi chatbot): vòng tự cải tiến có người duyệt (`improve-workflow` + `SO_CAI_TIEN_CACH_LAM.md`); `run-experiment` có sàn / mức tụt / chỉ số quyết, cỡ mẫu trước, nhiễu A/A, kiểm người chấm; Session D học cùng User; `AGENTS.md` bản chính cho mọi agent; hook git chặn commit dữ liệu private. **Cách làm phải dùng được gần như nhau cho Codex/AGY**: luật ở Markdown trong repo + rào ở tầng git, không chỉ ở memory / settings của Claude | User; `report_agent/2026-10-25_cai_tien_cach_lam/` |
| 2026-10-24 | User ủy quyền A: tự điều phối B/C, tự kiểm tra, đề xuất, thử nghiệm, tối ưu và phát triển các Phase trước; commit/push theo mốc; ghi report; hệ thống phải chạy ổn định; dùng skill khi code | User (trước khi nghỉ) |
| 2026-10-24 | Giá `gpt-6-luna`: 0,1 USD/1M input, 0,5 USD/1M output. Ngân sách session ≤1 USD (tối đa 1,5 USD), không cần dùng hết | User |
| 2026-10-24 | Phase 7B: judge chính là Claude (session Claude Code), `gpt-6-luna` chỉ sinh + judge phụ; User chấm ~20 case; đo nhiễu (thay judge `gpt-6-luna` cũ) | `docs/superpowers/specs/2026-10-24-phase-7b-evaluator-baseline-design.md` |
| 2026-10-24 | Mô hình A/B/C, review chéo, quy trình theo rủi ro, một tài liệu thiết kế/Phase, STATUS riêng mỗi session; duyệt cho A = duyệt cho B/C | `docs/superpowers/specs/2026-10-24-governance-v2-design.md` |
| 2026-10-24 | Index 8B hoãn sang Phase 8; khi build lại thiết kế cách gọi chịu 504/429 (batch, thử lại) | `reports/phase_7a2_gate_2_review_2026_10_24.md` §6 |
| 2026-10-24 | OpenRouter 8B pin Nebius (`order:[nebius]`, `allow_fallbacks:false`) | spec 7A2 §5.2 |
| 2026-10-24 | Giữ 2 collection Foods qua Phase 7; sau Phase 7 A đề xuất xóa mọi collection không dùng (kèm gỡ code/test/notebook Foods cũ) | User |
| 2026-10-24 | Cách làm việc học từ MekongAI: báo cáo cho User chỉ ở `bao_cao_he_thong/` (README mục lục, `LUONG_HOAT_DONG_HE_THONG`, `BAO_CAO_<khâu>` sống + thang 5 mức, `nhat_ky/`); report agent theo đợt `report_agent/<YYYY-MM-DD>_<chủ_đề>/` + `TONG_HOP.md`; giờ bằng `date`; stage từng file + `git diff --cached --stat`; A thử trong worktree; quyền đặc biệt hết hạn cuối phiên | `WORKFLOW.md` §6, §8, §9; `report_agent/2026-10-24_to_chuc_bao_cao/MO_TA_CACH_LAM_VIEC_MEKONGAI.md` |
| 2026-10-24 | Chunker giữ nguyên tới khi có baseline 7B | User |
| 2026-10-24 | Code/test/script luôn chạy bằng `uv` trong `.venv` của dự án | `Session_Prompt.md` §10 |
| 2026-10-24 | Kênh liên lạc: Claude Code ↔ Claude Code `trực tiếp` (SendMessage); có Codex/AGY thì `qua User` (khối "Tin cho <X>") | `WORKFLOW.md` §7 |
| 2026-09 (giữ) | Phase tuần tự `7A2 → 7B → 8 → 9`; trước Phase mới: Phase trước review + User đóng, cập nhật guide bằng bằng chứng, rồi một tài liệu thiết kế User duyệt | `WORKFLOW.md` §9.4 |
| 2026-10-24 (tối) | Phase 8 tách **8.1** (Claude rà mọi quyết định Phase 0–7 do AGY/Codex làm; thí nghiệm, phương án cũ làm baseline; không đổi chatbot) → **8.2** (cải tiến). 8.1 rà toàn bộ gồm Golden/evaluator; model/thư viện mới liệt kê trong spec để User duyệt từng cái; paid nhỏ trong trần 1 USD/phiên; index 8B để 8.2. Bộ chấm: chia 176 thành 120 thử / 56 kiểm, thêm 30–40 câu mới kiểu người dùng thật giữ kín tới cuối 8.2 | User |
| 2026-10-24 (tối) | Đoạn đúng cho câu khó: agent gắn, agent khác kiểm chéo, User duyệt ~10 câu; điểm câu trả lời chưa có mốc người | User |
| 2026-10-24 (tối) | **Giữ `gpt-6-luna`**, không so model sinh ở Phase 8; tối ưu sang model nhỏ để sau khi hệ thống ổn. **Thay** amendment `2026-10-01-phase-6-openai-baseline-amendment.md` §5 và amendment 10-23 R6 ("Qwen là benchmark bắt buộc ở Phase 8") | User |
| 2026-10-24 (tối) | Dense ở Phase 8 chỉ e5-small + Qwen3-Embedding-8B (giữ spec 7A2 §2; 8B ở 8.2). Rerank thử trên GPU GTX 1650 4 GB fp32 trong `.venv` (torch cu130 sẵn có); chatbot hiện chạy máy User, có thể deploy AWS sau (chưa chắc) ⇒ đo cả latency CPU | User |
| 2026-10-24 21:58 | Số chính 8.1 = **bỏ câu không tự nhiên** (tự nhiên + đo năng lực; 2 agent gắn độc lập, kappa 0,765, 29 câu loại, 9 câu bất đồng chờ User); "chỉ tự nhiên" là số phụ. Nhãn: `data/phase_8_1/golden_realism_final.jsonl` (private) | User |
| 2026-10-24 21:40 | Câu hỏi đánh giá phải **tự nhiên** (người dùng thật hỏi). Golden giữ nguyên nhưng gắn nhãn natural / capability_only / unnatural; số chính = phần natural; câu kín không tự nhiên thì thay. Skill tự cải thiện + ý từ khóa AI FDE tạm gác tới khi User gửi báo cáo | User |
| 2026-10-24 20:49 | **Nguyên tắc thường trực:** được thực nghiệm, so sánh, thử — không chỉ Phase 8.1, cả khi quay lại các Phase trước; luôn thử + đánh giá + so với baseline trước khi chọn, không chọn một giải pháp rồi làm luôn. Vẫn theo quyền/tiền/ranh giới dữ liệu hiện hành | User |
| 2026-10-24 20:49 | **Spec 8.1 approved** (`docs/superpowers/specs/2026-10-24-phase-8-1-decision-audit-design.md` bản 4) + M1 `bge-reranker-v2-m3`, M2 `AITeamVN/Vietnamese_Reranker` | User |
| 2026-10-24 (tối) | 8.1 G4 thêm rerank listwise bằng `gpt-6-luna` (kiểu `rag_old_0`) so cùng rerank GPU; chi tiết dự án khác của User giữ private (`data/phase_8_1/external_lessons_private.md`), không đưa lên repo công khai | User |
| 2026-10-24 (tối) | B9 đóng; thư viện không dùng giữ nguyên, chỉ gỡ khi xung đột; nghiên cứu ngoài qua ChatGPT trước với prompt deep research đầy đủ | User |
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
AGENTS.md                              lối vào cho mọi agent (CLAUDE.md chỉ nhập file này)
session_prompt/START_SESSION.md        mở mọi session
session_prompt/Session_Prompt.md       luật chung
session_prompt/WORKFLOW.md             cách làm, việc thêm của A
session_prompt/CURRENT_HANDOFF.md      việc đang mở của A/B/C
session_prompt/sessions/STATUS_*.md    ngữ cảnh riêng từng session
session_prompt/PROJECT_HISTORY.md      lịch sử (reference-only)
session_prompt/TEMPLATE_*.md           mẫu report
session_prompt/SO_CAI_TIEN_CACH_LAM.md sổ cải tiến cách làm (skill improve-workflow)
skills/{practical-project-coding,risk-gated-agent-review,propose-options,run-experiment,improve-workflow}/SKILL.md
.githooks/pre-commit, .claude/settings.json   rào bằng máy (hook git mọi agent; Claude Code cấm đọc .env)
guides/full_corpus_rag.md              guide umbrella full-corpus
docs/superpowers/specs/, docs/superpowers/plans/   thiết kế từng Phase
report_agent/<YYYY-MM-DD>_<chủ_đề>/   report + review từ 2026-10-24 (README trong report_agent/)
bao_cao_he_thong/                      báo cáo cho User: luồng hệ thống, BAO_CAO_<khâu>, nhat_ky/
reports/                               report cũ tới 2026-10-24 — lịch sử, chỉ đọc
gửi chatgpt/<YYYY-MM-DD>/              yêu cầu + kết quả nghiên cứu ChatGPT (private)
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
- `test_phase6_live_smoke.py` còn mock/monkeypatch — rà ở Phase 8.1 (B8). Code/test Foods cũ đã gỡ ở B9
  (`1832201`): pytest 15 file full-corpus 191 passed.
- OpenRouter 8B: không pin thì trộn provider (vector lệch, cos ~0,996); pin Nebius
  thì 10–30 s/batch và đã gặp 504; DeepInfra từng trả 429.
- Notebook còn lại: 03, 04, 06 (02, 05, 07, 08a–c đã xóa ở B9); 03/04 Run All đạt trên bản tạm.
- Permission tự động của từng session có thể chặn `rm`/`pkill`: session đó dừng và
  nhờ User chạy bằng `!` trong terminal của nó; session khác không chạy hộ.
- Memory Claude dùng chung cho cả ba session (cùng thư mục dự án).
- Hook `.githooks/pre-commit` chỉ chạy khi `git config core.hooksPath` = `.githooks` (cấu hình cục bộ, không đi theo
  clone): bản clone mới phải bật một lần. Hook chặn dòng thêm mới có tên dự án khác, kể cả khi trích tên file tài liệu
  cũ — viết "tài liệu cách làm của dự án khác" thay vì tên file. Bỏ qua (`--no-verify`) chỉ khi User duyệt đúng commit đó.
