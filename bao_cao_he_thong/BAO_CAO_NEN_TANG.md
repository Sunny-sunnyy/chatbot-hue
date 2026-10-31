# Báo cáo cho bạn: Nền tảng — luật chơi và khung backend (Phase 0–1)

**Cập nhật lần cuối: 16:59 31/10/2026 — bản 4: chỉ sửa số file kho (204 từ 28/10); nền tảng không đổi.** Bản 3 (26/10/2026): sau đợt 3 rà code (26/10) — gỡ bộ chạy kiểm khói Phase 5, logger `api`; bản 2 (19:58 24/10):
đưa về mẫu mới, gỡ code bản món ăn.**
Người viết: B · Review: A. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** đặt luật chơi cho cả dự án ("đơn giản là mặc định"; không dùng dữ liệu giả làm
  bằng chứng) và dựng khung `backend/`: 10 gói Python, một file cấu hình, một hàm đọc cấu hình có kiểm
  lỗi, một cấu hình ghi log chung, một khuôn chung cho kết quả tìm kiếm. Đã đóng tháng 8/2026.
- **Đang chạy cách nào:** khung này vẫn là nền của chatbot toàn kho (204 file từ 28/10). File cấu hình
  `settings.yaml` nay chỉ còn 4 nhóm: kho tri thức, địa chỉ Qdrant, runtime (model tìm kiếm, cách tìm),
  sinh câu trả lời. Hàm đọc cấu hình kiểm đúng các nhóm này. Phần cấu hình và code của bản món ăn cũ đã
  gỡ ngày 24/10.
- **Đo được:** khâu nền, không có số chất lượng. Kiểm kỹ thuật sau khi gỡ code cũ (24/10): 191 test của
  bản toàn kho đạt, kết quả tìm kiếm giống từng byte với trước khi gỡ, API báo sức khỏe 200.
- **Giới hạn chính:** 2 lệnh chạy riêng (build chỉ mục, thử nhanh tìm kiếm) chưa dùng cấu hình log
  chung; một file test còn dùng giả lập để thử nhánh lỗi.
- **Chi phí / tốc độ:** không tốn tiền.
- **Bạn cần quyết gì:** không. Hai giới hạn trên đã xếp vào đợt rà Phase 8.1.

## 2. Hoạt động thế nào (bản đang chạy)

```text
settings.yaml (4 nhóm) -> load_settings() -> kiểm nhóm kho tri thức + runtime + sinh câu trả lời -> settings
API khởi động -> setup_logging() -> ghi log ra màn hình + backend/logs/application.log
tìm kiếm -> RetrievedDocument(id, điểm, text, metadata) -> dựng ngữ cảnh -> sinh câu trả lời
lỗi -> một lớp lỗi dùng chung (core/schema.py) -> API trả mã lỗi tiếng Việt rõ ràng
```

- Code: hàm đọc cấu hình `backend/core/settings_loader.py:11-21` (kiểm runtime/sinh `:24-78`, kiểm kho
  tri thức `:81` trở đi); log `backend/core/logging_setup.py:13`; khuôn kết quả và lớp lỗi
  `backend/core/schema.py:7-42`.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Khung 10 gói backend | **Đã xử lý, đóng gói** | `ls backend/*/__init__.py` ra 10 file |
| Cấu hình tập trung, đọc một chỗ, sai thì báo lỗi ngay | **Đã xử lý, đóng gói** | `settings_loader.py:11-21`, `:24-78`; 191 test đạt 24/10 |
| Khuôn kết quả tìm kiếm chung | **Đã xử lý, đóng gói** | `schema.py:36`; dùng ở `retrieval/full_corpus.py:327`, `:647` |
| Lớp lỗi dùng chung, API trả lỗi rõ | **Đã xử lý, đóng gói** | `schema.py:7-32`; `api/app.py:21-24`, `:70`, `:77` |
| API báo sức khỏe từng thành phần | **Đã xử lý, đóng gói** | `api/health.py:17-23`; 200, mọi thành phần `ready` (24/10) |
| Ghi log chung cho mọi lệnh chạy | **Xử lý một phần** | API dùng `setup_logging()` (`api/app.py:38`), từ 26/10 có logger `api` trong `logging.yaml`; lệnh dựng kho `ingestion/full_corpus_pipeline.py` còn tự cấu hình log riêng (`retrieval/full_corpus_smoke.py` đã gỡ 26/10) |
| Test chỉ chạy trên hệ thống thật | **Xử lý một phần** | Gần hết test dùng Qdrant/model thật; `tests/test_phase6_live_smoke.py:223-228`, `:314` còn giả lập nhánh lỗi |
| Chạy bằng `uv` trong môi trường dự án | **Đã xử lý, đóng gói** | `pyproject.toml`; `session_prompt/Session_Prompt.md` §10 |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

### 24/10/2026 — Gỡ code bản món ăn khỏi nền (bản 2)
Bỏ khỏi `settings.yaml` các khối "profile" và cấu hình bản món ăn; bỏ phần kiểm `active_profile` trong
hàm đọc cấu hình (sửa cùng lúc); gỡ `core/startup.py` và fixture bản món ăn trong test. Tiêu chí ghi
trước: kết quả tìm kiếm giống từng byte, test bản toàn kho đạt, API lên · kết quả **PASS**: 191 test đạt,
giống từng byte, sức khỏe 200; người kiểm độc lập chạy lại cũng đạt · tiền: 0,0013 USD (khoảng 33 đồng,
cho lượt thử 10 câu ở khâu sinh câu trả lời).

### 24/10/2026 — Kiểm lại hiện trạng (bản 1, chỉ đọc)
Hàm đọc cấu hình chạy được (lúc đó vẫn kiểm profile `dense_only`, 3 profile); Qdrant có 3 kho; 10 gói.
Không khởi động API, không chạy pytest.

### 24/08/2026 — Rà soát đơn giản hóa Phase 0 + 1
Phase 0 chỉ sửa tài liệu; bộ test lúc đó `222 passed, 4 warnings`. Chạy thật: `/health` `status=ok`,
giao diện HTTP 200, 74 + 222 test đạt, 572 point trước/sau, file kết quả CSV không đổi · **PASS** ·
bỏ Notebook 01 và `README_config.md`.

### 09/08/2026 — Dựng khung backend (Phase 1)
10 gói, profile `dense_only` trong 3 profile, tên profile sai báo `ValueError`, log thử, khuôn kết quả
tìm kiếm, 6 ô notebook · **PASS**; không gọi mạng, Qdrant hay API trả phí.

## 5. Hôm nay còn đúng không

Kiểm với code (commit `1832201`) ngày 24/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| 10 gói `api, core, embedding, evaluation, ingestion, llm, reranking, retrieval, scoring, vectorstore` | **còn dùng** | `ls backend/*/__init__.py` |
| `settings.yaml` tập trung + `load_settings()` | **còn dùng**; nay kiểm nhóm kho tri thức + runtime + sinh câu trả lời | `backend/core/settings_loader.py:11-21` |
| 3 profile tìm kiếm, đang dùng `dense_only` | **đã bỏ** (gỡ ở B9, 24/10); thay bởi nhóm runtime `dense_bm25_rrf` từ Phase 6 | `backend/config/settings.yaml:40-43` |
| `setup_logging()` + `logging.yaml` | **còn dùng** ở API; 2 lệnh toàn kho chưa theo (mục 3) | `backend/core/logging_setup.py:13`; `backend/api/app.py:38` |
| `/health` kiểm `qdrant/retrieval/generator` | **đã thay** bởi bản Phase 6: thêm `tokenizer`, giá trị `ready`/`not_ready` | `backend/api/health.py:17-23` |
| `RetrievedDocument(id, score, text, metadata)` | **còn dùng** cả ở đường toàn kho | `backend/core/schema.py:36`; `backend/retrieval/full_corpus.py:327` |
| Lớp lỗi dùng chung trong `core/schema.py` | **còn dùng** | `backend/core/schema.py:7-32` |
| Xóa Notebook 01 và `README_config.md` | **đã bỏ** (24/08/2026) | `docs/superpowers/specs/2026-08-24-phase-1-backend-foundation-simplicity-design.md:97-100` |
| Đơn giản là mặc định; không fallback/abstraction phòng xa | **còn dùng**, nay ở luật chung §7 | `session_prompt/Session_Prompt.md` §7 |
| Không mock/fake làm bằng chứng | **còn dùng** (luật); còn một file test giả lập nhánh lỗi | `session_prompt/Session_Prompt.md` §6; `backend/tests/test_phase6_live_smoke.py:223-228` |
| Loại checksum/tamper detection | **đã thay** bởi build record + hash corpus (Phase 7A2) | `backend/retrieval/full_corpus.py:415`; `session_prompt/Session_Prompt.md` §7 |
| Test chạy hệ thống thật, collection test riêng | **còn dùng** phần "hệ thống thật"; fixture tạo collection test **đã bỏ** (B9), test nay chỉ đọc Qdrant | `backend/tests/conftest.py:1-5` |
| Chạy bằng `uv` | **còn dùng** | `session_prompt/Session_Prompt.md` §10; `pyproject.toml` |
| Collection món ăn `hue_foods_e5_small_384` (572) | **đã bỏ**: không đứng sau API từ Phase 7A2, xóa khỏi Qdrant 24/10 (B9) | `GET /collections` chỉ còn `hue_full_corpus_7a2_e5_small_384` |
| Sinh câu trả lời `gpt-5.4-nano` qua OpenAI Agents SDK | **đã thay** bởi `gpt-6-luna` (Phase 6, 23/10); Agents SDK còn dùng | `backend/config/settings.yaml:47`; `backend/llm/generator_openai_full_corpus.py:9` |
| Skill `karpathy-guidelines` | **đã thay** bởi `practical-project-coding` | `skills/` |

## 6. Việc còn lại / cần quyết

- Cho 2 lệnh build chỉ mục và thử nhanh tìm kiếm dùng cấu hình log chung (Phase 8.1).
- Bỏ giả lập trong `test_phase6_live_smoke.py` hoặc ghi rõ đây là test logic thuần (Phase 8.1).
- Không cần bạn quyết gì ở khâu này.

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/phase_0_mvp_foundation_simplicity_review.md`,
  `reports/user_reports/phase_1_backend_skeleton_user_report.md`,
  `reports/user_reports/phase_1_backend_skeleton_simplicity_user_report.md`.
- Bản 1: B8, 24/10/2026. Bản 2: B10, sau dọn B9 (commit `1832201`; report
  `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md`, review
  `phase_7_cleanup_review.md` cùng thư mục).
- **Lệch đã ghi ở bản 1 và trạng thái hôm nay:**
  1. Health: report Phase 1 ghi `generator: configured`; code trả `ready`/`not_ready` và có thêm
     `tokenizer` (`backend/api/health.py:19-20`). Chỉ là report cũ — còn.
  2. Logging: spec Phase 1 yêu cầu mọi lệnh chạy dùng `setup_logging()`
     (`docs/superpowers/specs/2026-08-24-phase-1-backend-foundation-simplicity-design.md:86`, `:136-137`);
     `ingestion/full_corpus_pipeline.py` dùng `basicConfig` — **còn**; `retrieval/full_corpus_smoke.py` đã gỡ (26/10, đợt 3 rà code).
  3. Mock/fake: `test_reranker_benchmark.py`, `test_markdown_chunker.py` **đã gỡ ở B9**;
     `test_phase6_live_smoke.py:223-228`, `:314` **còn**, Phase 8.1.
  4. `conftest.py` đặt `ACTIVE_COLLECTION` = collection món ăn — **đã gỡ ở B9**.
  5. Hàm đọc cấu hình kiểm `active_profile` dù API không dùng — **đã gỡ ở B9**.
  6. Spec governance trỏ `skills/karpathy-guidelines/SKILL.md` đã không còn — còn (spec lịch sử).
  7. `guides/phase_1_backend_skeleton.md:27` ghi bước tiếp là Phase 6 — còn (guide lịch sử).
