# Implementation Report: B92 — harness thí nghiệm Qwen3-Embedding-8B (chỉ code, chưa chạy lượt có phí)

Người làm: B (Claude Opus 5.5, `hue-rag-24`) · Date: 11:25 30/10/2026 (`date`) · Việc: `CURRENT_HANDOFF.md` "PHIÊN 30/10" B92 (A giao 11:05; đổi người so với plan §10.2:
B viết, **C review code**). Plan: `qwen3_8b_plan.md` (A duyệt `52555da95828`) §4, §6. Nhánh `b92-qwen3-harness` (từ `main` `e70007b`), worktree `/tmp/b92_qwen3`.
**0 USD**: không gọi OpenRouter, không tạo collection, không build. B92 tạm dừng 11:16–11:23 để làm B93 bước 1 (đợt 2), rồi làm tiếp.

## Tóm tắt cho User (lời thường)

- **Làm gì:** viết sẵn công cụ để thử model tìm kiếm lớn Qwen3-8B (chạy qua mạng) thay model nhỏ e5 đang chạy trên máy, theo kế hoạch đã duyệt. Chưa gửi gì ra ngoài,
  chưa tốn tiền.
- **Chatbot không đổi:** chỉ thêm "cửa phụ" tùy chọn cho công cụ thử nghiệm; khi chatbot chạy bình thường (không truyền gì) thì đi đúng đường cũ. Kiểm bằng hệ thống thật: kết
  quả tìm 158 câu giống **từng byte** trước và sau khi sửa; công cụ chẩn đoán g1 cho 108 câu dev cũng giống hệt.
- **Công cụ thêm gì:** gọi lại có giới hạn khi mạng / nhà cung cấp lỗi tạm (429 / 5xx / quá giờ — 7A2 từng hỏng đúng chỗ này); lưu từng lô vector đã trả tiền để chạy
  lại không trả tiền hai lần; ghi log từng lần gọi (mã lỗi, thời gian, nhà cung cấp, số token); giữ vector câu hỏi để đo độ dao động giữa hai lượt.

## 1. Thay đổi (`git diff e70007b..b92-qwen3-harness`, 5 file, +405 / −6)

| File | Đổi | Plan |
|---|---|---|
| `backend/ingestion/full_corpus_pipeline.py` | `build_candidate(..., dense_runner=None)`; `None` = `create_dense_runner(spec)` như cũ; runner truyền vào sai spec ⇒ `ValueError` | §4.1 |
| `backend/retrieval/full_corpus.py` | `build_full_corpus_retrieval_service(..., dense_runner=None)`; `None` = như cũ; sai spec ⇒ `RetrievalConfigurationError` | **lệch §4.2** (dưới) |
| `backend/experiments/phase_8_1/g1_retrieval.py` | `run --candidate / --collection / --record / --sparse-state` (mặc định = runtime e5); `run_config(args, dense_runner=None)`; tách `build_parser()` để harness dựng `run` đúng mặc định g1 | §4.2 |
| `backend/experiments/phase_8_2/qwen3_8b.py` (mới, `761b02e5e5ae`) | `LoggedOpenRouterRunner` (lớp con `OpenRouterDenseRunner`); lệnh `preflight`, `pilot`, `build`, `retrieve`, `aa` | §4.1, §6 bước 1, 3, 4, 5; §3 A/A |
| `backend/tests/test_qwen3_8b_harness.py` (mới, `a2949986f970`) | 3 test logic thuần: lịch thử lại, cache batch (đọc / ghi, dừng khi chữ đổi) | — |

Runner bọc (chỉ trong `experiments/`): giữ nguyên input (`prepare_document` / `prepare_query`), batch 64, pin Nebius + `data_collection: deny`
(`OPENROUTER_PROVIDER_ROUTING`), timeout 180 s, kiểm response (`parse_embeddings_response`). Thêm:
- **Thử lại** chỉ với 429 / 5xx / timeout; batch đoạn tối đa 3 lần, chờ 10 / 30 / 90 s; 429 có `Retry-After` (số giây) ⇒ max(lịch, Retry-After). Hết lượt ⇒ raise (build dừng,
  cache giữ). Câu hỏi: 1 lần thử lại trong runner — **lệch plan §4.2**, xem §2 mục 5; lần lỗi vẫn nằm trong log.
- **Cache batch** `data/qwen3_8b_2026-10-28/emb/batch_NNN.npy` + `.json` (sha của chính các chuỗi gửi đi, số dòng, provider). Meta ghi sau `.npy` (thiếu meta = batch chưa xong).
  Chữ đổi (vd kho đổi sau pilot) ⇒ dừng, không dùng vector cũ. Batch đọc từ cache vẫn thêm provider vào `providers_seen` ⇒ build record ghi đúng.
- **Log từng request** `emb/attempts.jsonl` / `queries_<name>.jsonl`: nhãn (batch / query / pilot_repeat), lần thử, HTTP, ms, provider, `id`, `prompt_tokens`, lỗi rút gọn, giờ.
- Là **lớp con** của `OpenRouterDenseRunner` để dòng `isinstance(runner, OpenRouterDenseRunner)` của `build_candidate` vẫn ghi `providers_seen` (không sửa dòng đó).

## 2. Lệch plan / cần A biết

1. **`dense_runner` ở factory dựng service tìm (lệch §4.2):** plan §4.2 chỉ truyền 4 tham số. Nhưng §3 cần (a) cos giữa hai lượt vector câu hỏi (A/A) và (b) id / ms /
   provider từng request — runner production tạo **bên trong** factory nên harness không lấy được. Cách trực tiếp nhất là cùng mẫu với §4.1: tham số `dense_runner=None`. Mặc định
   giữ nguyên, kiểm bằng T1 + test (§3). Không sửa `OpenRouterDenseRunner`, API, `settings.yaml` (§4.3 giữ). **A duyệt 11:3x 30/10/2026** (chi tiết trong phạm vi, cùng mẫu §4.1).
2. **Mốc e5 plan §5 là số của kho đợt 1.** B tính lại hôm nay trên kho hiện tại: dev 40 câu có nhãn, context đủ 24, top-10 24, pool dense 33, thiếu ở pool dense 7 — **khớp §5**.
   Nhưng 8B chạy **sau đợt 2** ⇒ kho đổi, có thể gold v5 ⇒ điều kiện dừng "mốc e5 lệch bảng §5" (§6 bước 2, §8) không còn áp; mốc e5 phải chạy lại trên kho sau đợt 2 và lấy làm
   mốc mới (cỡ mẫu §3 tính lại nếu số câu thiếu đổi). **A quyết 11:3x 30/10/2026:** viết "Sửa đổi 30/10" cuối plan (B viết, C review, A duyệt sha) **trước** khi chạy 8B.
3. `providers_seen` thật là `"Nebius"` (hằng `OPENROUTER_EXPECTED_PROVIDER`), plan §6 bước 4 viết `"nebius"` ⇒ harness so với **chính hằng đó** (commit `400ccdc`, A yêu cầu:
   so đúng giá trị thật, không gõ chuỗi tay). Runner production cũng so bằng hằng này (`parse_embeddings_response`).
4. `preflight` so số đoạn với build record runtime + sha sparse runtime (không gắn cứng 8.426 / `1bae9e0f3c49`) vì đợt 2 đổi cả hai. T1 runtime chạy riêng bằng evaluator.
5. **Đường lỗi câu hỏi lệch §4.2** (review C88 M-1 — B tả sai là "khớp plan" ở §1; **A chọn giữ code** 11:3x 30/10/2026): runner thử lại 1 lần sau 10 s (hoặc `Retry-After`)
   ⇒ `dense_ms` câu đó gồm cả lúc chờ; lỗi hai lần ⇒ cả lượt dừng (chưa ghi `<name>.jsonl`) ⇒ chạy lại cả lượt. Bù: `query_latency` (lệnh `latency`, in cả trong `retrieve`)
   báo p50 / p95 `dense_ms` mọi câu **và** chỉ câu gọi một lần, số câu thử lại, dòng log ≠ 200; luật dừng mới "câu thử lại > 5 %". Ghi ở plan "Sửa đổi 30/10" mục 6
   (commit `fb0b82c`; cùng commit: m-1 — ghi log trước khi parse JSON, 200 hỏng vẫn có dòng log rồi mới dừng).
6. `pilot`: nếu response không có `usage.prompt_tokens` thì ước tiền ra rỗng ⇒ đọc thẳng `attempts.jsonl` và dừng theo plan §8 (ước > 1,5 × thì báo A).

## 3. Đã chạy (0 USD)

| Kiểm | Kết quả |
|---|---|
| T1 158 câu (`evaluation.full_corpus_eval retrieval`) **trước** sửa (worktree ở `e70007b`) | `23c58c47635d` = mốc |
| T1 **sau** sửa (worktree) | `23c58c47635d`, `cmp` giống byte |
| g1 `run_config` mặc định, 108 câu dev: code cũ (working tree chính, Namespace tay) ↔ code mới (`build_parser()`), bỏ `dense_ms` | giống hệt |
| pytest (không key): `test_qwen3_8b_harness.py`, `test_full_corpus_retrieval.py`, `test_full_corpus_qdrant_ingestion.py`, `test_full_corpus_embedding.py`, `test_gold_coverage.py` | **70 passed** |
| `qwen3_8b preflight` (env có key, chỉ in có / không) | `ok: true`; 1 collection; chưa có `hue_c78_*`; 8.426 = record; gold v4 `927bae1bf201`; sparse `1bae9e0f3c49` |
| `git diff --check`; hook pre-commit (commit WIP `8545650`) | sạch; 0 trùng kho / Golden |

## 4. NOT RUN / giới hạn

- **Mọi đường mạng** (thử lại, log, cache từ response thật, `pilot`, `build`, `retrieve`, `aa`): NOT RUN — cần User + A duyệt lượt có phí (plan §6). `pilot` (2 batch + 20 đoạn,
  ≈ 0,002 USD) là lần chạy thật đầu tiên của các đường này; lỗi ở đó dừng trước build.
- Test không giả lập HTTP (luật dự án: không mock) ⇒ chỉ logic thuần có test; phần còn lại kiểm bằng `pilot`.
- `aa` ghép vector hai lượt theo sha câu hỏi (gồm câu warm-up của factory, giống nhau hai lượt).

## 5. Bàn giao cho người kiểm (C)

- Đọc `git diff e70007b..b92-qwen3-harness` (nhánh đã push; đỉnh `fb0b82c` — WIP `8545650` + so provider `400ccdc` + sửa review C88 `fb0b82c`; test harness 4). Chỗ nên soi: `_embed` (vòng thử lại, câu lỗi cuối cùng raise), `embed_documents_matrix` (cache + `providers_seen`),
  `retrieve` (dựng `run` qua `g1.build_parser()`; từ chối ghi đè), `aa`.
- Chạy lại free: T1 trong worktree (symlink `data/`, `knowledge-base-hue/`), pytest 5 file trên, `preflight`.
- Sau khi đợt 2 áp: chạy lại T1 trên nhánh sau rebase (kho mới) — phải giống T1 mới của `main`.
