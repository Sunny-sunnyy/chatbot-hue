# Báo cáo dành cho người dùng: Giai đoạn 0–1 - Nền tảng MVP và backend

```text
Trạng thái: Đã đóng (lịch sử) — viết lại 2026-10-24
Nguồn lịch sử: reports/phase_0_mvp_foundation_simplicity_review.md,
  reports/user_reports/phase_1_backend_skeleton_user_report.md,
  reports/user_reports/phase_1_backend_skeleton_simplicity_user_report.md
Notebook: không có (Notebook 01 đã xóa 2026-08-24)
```

## 1. Bạn nhận được gì

Phase 0 đặt luật chơi cho cả dự án. Luật chính: "đơn giản là mặc định". Code phải dễ đọc.
Chỉ thêm lớp trừu tượng khi có nhiều cách làm thật. Không dùng mock/fake làm bằng chứng.

Phase 1 dựng phần khung `backend/`: 10 gói Python, một file cấu hình `settings.yaml`,
một hàm đọc cấu hình `load_settings()`, một cấu hình logging chung và một khuôn kết quả
tìm kiếm `RetrievedDocument`.

Lúc đó hệ thống chỉ có Foods: 572 chunk trong collection `hue_foods_e5_small_384`.
Sau này dự án chuyển sang full-corpus 205 file (8.459 chunk). Khung Phase 1 vẫn là nền,
nhưng đường chạy chính đã đổi (xem mục 4).

## 2. Hệ thống hoạt động như thế nào (lúc Phase 0–1)

```text
settings.yaml -> load_settings() -> kiểm active_profile (1 trong 3 profile) -> trả settings
entrypoint (API / ingestion / evaluation) -> setup_logging() -> console + backend/logs/application.log
kết quả tìm kiếm -> RetrievedDocument(id, score, text, metadata) -> rerank / context
```

Ba profile tìm kiếm: `dense_only`, `hybrid_no_rerank`, `hybrid_rerank`. Profile đang dùng: `dense_only`.

## 3. Agent đã chạy và quan sát gì

**Bằng chứng lịch sử** (theo report cũ, không chạy lại hôm nay):

| Ngày | Nội dung | Kết quả theo report | Nguồn |
|---|---|---|---|
| 2026-08-09 | 10 gói, `dense_only`, 3 profile, tên sai -> `ValueError`, log thử, `RetrievedDocument`, 6 ô notebook | Đạt; không gọi mạng/Qdrant/paid | `phase_1_backend_skeleton_user_report.md:45-56` |
| 2026-08-24 | Phase 0 chỉ sửa tài liệu; baseline backend trước review | `222 passed, 4 warnings` | `phase_0_mvp_foundation_simplicity_review.md:24-31` |
| 2026-08-24 | API thật `/health`, Gradio, test, Qdrant, CSV Phase 7 | `status=ok`; UI HTTP 200; 74 + 222 test passed; 572 point trước/sau; CSV không đổi | `phase_1_backend_skeleton_simplicity_user_report.md:32-39` |

**Đã kiểm hôm nay 2026-10-24** (chỉ đọc):

| Kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| `uv run python -c "load_settings()"` từ `backend/` | Đạt: `dense_only`, 3 profile, Foods collection, runtime `e5-small-384` / `dense_bm25_rrf` / `none` | Loader Phase 1 vẫn chạy, có thêm nhóm full-corpus |
| `GET 127.0.0.1:6335/collections` | 3 collection; 2 Foods 572 point (green); full-corpus 8.459 (green) | Foods còn trong Qdrant |
| `ls backend/*/__init__.py` | 10 gói | Cấu trúc gói giữ nguyên |
| `GET /health` (port 8000/8011/8080) | Chưa kiểm: API không chạy | Không khởi động API trong việc này |
| pytest | Chưa chạy | Không cần cho report docs-only |

## 4. Hôm nay còn đúng không

| Kết quả/quyết định Phase 0–1 | Hôm nay | Bằng chứng (file:dòng) |
|---|---|---|
| 10 gói `api, core, embedding, evaluation, ingestion, llm, reranking, retrieval, scoring, vectorstore` | *còn dùng* | `ls backend/*/__init__.py` (10 file); `backend/api/app.py:18-30` |
| `settings.yaml` tập trung + `load_settings()` kiểm `active_profile` | *còn dùng*, mở rộng: kiểm thêm `full_corpus`, `full_corpus_runtime/generation` (full-corpus, Phase 6) | `backend/core/settings_loader.py:11-28`, `:31-85` |
| 3 profile, active `dense_only` | *đã thay bởi* `full_corpus_runtime` (`dense_bm25_rrf`, Phase 6 full-corpus); profile cũ vẫn bị kiểm nhưng API không dùng | `backend/config/settings.yaml:2-17`, `:110-113`; `backend/api/app.py:61-67` |
| `setup_logging()` + `logging.yaml`, gọi ở 3 entrypoint | *còn dùng* (entrypoint full-corpus mới không theo, xem Lệch) | `backend/core/logging_setup.py:13-19`; `backend/api/app.py:43`; `backend/ingestion/pipeline.py:95`; `backend/evaluation/evaluator.py:73` |
| `/health` (Phase 1 simplicity kiểm `qdrant/retrieval/generator`) | *đã thay bởi* health full-corpus (Phase 6): thêm `tokenizer`, giá trị `ready`/`not_ready` | `backend/api/health.py:15-24` |
| `RetrievedDocument(id, score, text, metadata)` | *còn dùng*, cả đường full-corpus | `backend/core/schema.py:35-42`; `backend/retrieval/full_corpus.py:327` |
| Error class dùng chung trong `core/schema.py` | *còn dùng* | `backend/core/schema.py:7-32`; `backend/api/app.py:70-77` |
| Xóa Notebook 01 và `README_config.md` | *đã bỏ* (2026-08-24); hôm nay `ls` không thấy cả hai | `docs/superpowers/specs/2026-08-24-phase-1-backend-foundation-simplicity-design.md:97-100` |
| Đơn giản là mặc định, không fallback/abstraction phòng xa | *còn dùng*, nay nằm ở Session_Prompt §7 | `session_prompt/Session_Prompt.md:98-105`; spec governance `2026-08-23-…-design.md:52-56` |
| Không mock/fake làm bằng chứng | *còn dùng* (luật); test còn vài chỗ vi phạm, xem Lệch | `session_prompt/Session_Prompt.md:89`; spec governance `:87` |
| Loại checksum/tamper detection | *đã thay bởi* build record + hash corpus (Phase 7A2); luật nay "chỉ quay lại khi có nhu cầu" | `session_prompt/Session_Prompt.md:106-109`; `backend/retrieval/full_corpus.py:415`, `:745-746`; `session_prompt/Project_Status.md:65-67` |
| Test live-only (Qdrant/E5 thật, collection test riêng) | *còn dùng*; full suite không còn mặc định | `backend/tests/conftest.py:1-10`, `:28`; `session_prompt/Session_Prompt.md:118-120` |
| Chạy bằng `uv` | *còn dùng* (hôm nay `uv 0.12.5`) | `session_prompt/Session_Prompt.md:140-145`; `pyproject.toml:1-5` |
| Collection Foods `hue_foods_e5_small_384` (572) | *đã thay bởi* `hue_full_corpus_7a2_e5_small_384` (Phase 7A2); Foods còn trong Qdrant, không đứng sau API | `backend/config/settings.yaml:70`; `backend/core/startup.py:24`; `session_prompt/Project_Status.md:62`, `:80-83` |
| Generation `gpt-5.4-nano` qua OpenAI Agents SDK (hợp đồng MVP Phase 0) | *đã thay bởi* `gpt-6-luna` (Phase 6, 2026-10-23); Agents SDK còn dùng | `reports/phase_0_mvp_foundation_simplicity_review.md:18`; `backend/config/settings.yaml:117`; `backend/llm/generator_openai_full_corpus.py:9` |
| Skill `karpathy-guidelines` | *đã thay bởi* `practical-project-coding` | spec governance `:71`; `session_prompt/Session_Prompt.md:112` |

## 5. Giới hạn và bước tiếp theo

- Hôm nay chưa khởi động API, chưa chạy pytest. `/health` chỉ kiểm bằng đọc code.
- Code Foods cũ (`core/startup.py`, profile, Foods collection) còn nằm trong repo. Theo quyết định User, A sẽ đề xuất gỡ sau Phase 7 (`Project_Status.md:106`).
- Phase 0–1 đã đóng. Không cần User xác nhận lại. Bước kế tiếp của dự án: Phase 8.

## Lệch phát hiện

1. Health: report nói `generator: configured` (`reports/user_reports/phase_1_backend_skeleton_simplicity_user_report.md:59`). Code trả `ready`/`not_ready` và thêm `tokenizer` (`backend/api/health.py:19-20`).
2. Logging: spec yêu cầu entrypoint gọi `setup_logging()`, bỏ `logging.basicConfig()` (`docs/superpowers/specs/2026-08-24-phase-1-backend-foundation-simplicity-design.md:86`, `:136-137`; `guides/phase_1_backend_skeleton.md:130-135`). Entrypoint full-corpus dùng `basicConfig` (`backend/ingestion/full_corpus_pipeline.py:242`; `backend/retrieval/full_corpus_smoke.py:67`, chạy lúc import).
3. Mock/fake: luật cấm (`session_prompt/Session_Prompt.md:89`; spec governance `:87`), conftest gọi suite là "live-only" (`backend/tests/conftest.py:1`). Test vẫn có fake/monkeypatch: `backend/tests/test_phase6_live_smoke.py:219-228`, `backend/tests/test_reranker_benchmark.py:437-440`, `backend/tests/test_markdown_chunker.py:118`.
4. Tên "active": `backend/tests/conftest.py:30` đặt `ACTIVE_COLLECTION = "hue_foods_e5_small_384"`. Thực tế collection đang chạy là full-corpus; Foods không đứng sau API (`session_prompt/Project_Status.md:62`, `:81-82`).
5. "Profile đang dùng": guide nói loader kiểm profile đang dùng (`guides/phase_1_backend_skeleton.md:9`). API không đọc `active_profile`; nó đọc `full_corpus_runtime` (`backend/api/app.py:61-67`), loader kiểm cứng giá trị runtime (`backend/core/settings_loader.py:39-44`).
6. Skill: spec governance trỏ `skills/karpathy-guidelines/SKILL.md` (`docs/superpowers/specs/2026-08-23-project-simplicity-governance-design.md:71`). File không còn; `skills/` chỉ có `practical-project-coding`, `propose-options`, `risk-gated-agent-review`.
7. Guide cũ: `guides/phase_1_backend_skeleton.md:27` ghi "bước tiếp theo của campaign là Phase 6". Đã lỗi thời (`session_prompt/Project_Status.md:34`: mốc kế tiếp là Phase 8).
