# Báo cáo cho bạn: Nền tảng — luật chơi và khung backend (Phase 0–1)

**Cập nhật lần cuối: 17:12 31/10/2026 — bản 5: rà lại cho đúng hiện trạng, xoá phần không còn đúng (User 31/10).**
Các bản trước: xem `git log` file này.
Người viết: agent con của A (bản 31/10; bản trước: B) · Review: agent con ngữ cảnh mới. Tỉ giá ước: 1 USD ≈ 25.000 đồng.

## 1. Tóm tắt (sửa lại mỗi bản — luôn đúng hiện trạng)

- **Khâu này làm gì:** đặt luật chơi cho cả dự án ("đơn giản là mặc định"; không dùng dữ liệu giả làm bằng chứng) và dựng khung
  `backend/`: các gói Python, một file cấu hình, một hàm đọc cấu hình có kiểm lỗi, một cấu hình ghi log chung, một khuôn chung cho kết quả
  tìm kiếm, một bộ lớp lỗi dùng chung. Đã đóng tháng 8/2026.
- **Đang chạy cách nào:** khung này vẫn là nền của chatbot toàn kho (204 file / 8.424 đoạn). `backend/` có **11 gói** (10 gói gốc +
  `experiments/` thêm 24/10 cho công cụ đo Phase 8.1). File cấu hình `settings.yaml` có 4 nhóm: kho tri thức, địa chỉ Qdrant, runtime
  (model tìm kiếm, cách tìm), sinh câu trả lời; hàm đọc cấu hình kiểm đúng các nhóm này. Cấu hình và code bản món ăn cũ đã gỡ (24/10).
- **Đo được:** khâu nền, không có số chất lượng. Mốc bộ test ghi lại gần nhất (26/10, không nạp khoá OpenAI): **197 đạt**; 1 hỏng + 4 lỗi
  đều là test cần khoá OpenAI (đúng thiết kế).
- **Giới hạn chính:** lệnh dựng chỉ mục chưa dùng cấu hình log chung (tự cấu hình log riêng); một file test còn dùng bản giả để thử nhánh
  lỗi. Cả hai chưa xử lý, chưa có lịch.
- **Chi phí / tốc độ:** không tốn tiền.
- **Bạn cần quyết gì:** không.

## 2. Hoạt động thế nào (bản đang chạy)

```text
settings.yaml (4 nhóm) -> load_settings() -> kiểm nhóm runtime + sinh câu trả lời + kho tri thức -> settings
API khởi động -> setup_logging() -> ghi log ra màn hình + backend/logs/application.log (có logger "chat" ghi số đo mỗi câu)
tìm kiếm -> RetrievedDocument(id, điểm, text, metadata) -> dựng ngữ cảnh -> sinh câu trả lời
lỗi -> một bộ lớp lỗi dùng chung (core/schema.py) -> API trả mã lỗi + lời báo tiếng Việt
```

- Code: hàm đọc cấu hình `backend/core/settings_loader.py:11` (kiểm runtime / sinh `:24`, kiểm kho tri thức `:79`); log
  `backend/core/logging_setup.py:13`, `backend/config/logging.yaml`; lớp lỗi `backend/core/schema.py:7-32`, khuôn kết quả `:35-42`.

## 3. Checklist tình huống

| Tình huống / loại nội dung | Trạng thái | Ghi chú (số đo, file:dòng) |
|---|---|---|
| Khung gói backend | **Đã xử lý, đóng gói** | `ls backend/*/__init__.py` ra 11 file (thêm `experiments/` 24/10) |
| Cấu hình tập trung, đọc một chỗ, sai thì báo lỗi ngay | **Đã xử lý, đóng gói** | `settings_loader.py:11`, `:24`, `:79` |
| Khuôn kết quả tìm kiếm chung | **Đã xử lý, đóng gói** | `schema.py:35-42`; dựng ở `retrieval/full_corpus.py:291-318` |
| Lớp lỗi dùng chung, API trả lỗi rõ | **Đã xử lý, đóng gói** | `schema.py:7-32`; `api/app.py:65-85` (409 / 503 lúc khởi động), `:161-165` (500 chung) |
| API báo sức khỏe từng thành phần | **Đã xử lý, đóng gói** | `api/health.py:15-24` (qdrant / retrieval / tokenizer / generator: `ready` / `not_ready`) |
| Ghi log chung cho mọi lệnh chạy | **Xử lý một phần** | API dùng `setup_logging()` (`api/app.py:38`); lệnh dựng kho còn `logging.basicConfig` riêng (`ingestion/full_corpus_pipeline.py:273`) |
| Test chỉ chạy trên hệ thống thật | **Xử lý một phần** | Gần hết test dùng Qdrant / model thật, chỉ đọc Qdrant; `tests/test_phase6_live_smoke.py:219-231`, `:313-319` còn thay app bằng bản giả để thử nhánh lỗi |
| Chạy bằng `uv` trong môi trường dự án | **Đã xử lý, đóng gói** | `pyproject.toml`, `uv.lock`; `session_prompt/Session_Prompt.md` §10 |

Thang 5 mức: **Đã xử lý, đóng gói** (đang chạy, đã kiểm) · **Đã xử lý** (có code, chưa đóng gói hết) ·
**Xử lý một phần** · **Đã thử, chưa áp dụng** (kèm vì sao) · **Chưa thực hiện**.

## 4. Thử nghiệm và lịch sử (thêm mục mới ở trên)

- **26/10/2026 — Rà code đợt 3:** gỡ bộ chạy kiểm khói Phase 5 (một trong hai lệnh chưa dùng log chung); thêm logger `api`; kết quả tìm /
  câu trả lời giống từng byte trước ↔ sau · giữ (`report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`).
- **24/10/2026 — Gỡ code bản món ăn khỏi nền:** bỏ cấu hình "profile" và bản món ăn khỏi `settings.yaml` + hàm đọc cấu hình, gỡ
  `core/startup.py` và fixture bản món ăn · **PASS**: 191 test đạt, kết quả tìm giống từng byte, sức khỏe 200; người kiểm độc lập chạy lại
  đạt · 0,0013 USD (lượt thử 10 câu sinh câu trả lời) · giữ.
- **24/08/2026 — Rà soát đơn giản hóa Phase 0 + 1:** chỉ sửa tài liệu; 222 test đạt, `/health` ok · **PASS** · bỏ Notebook 01 và
  `README_config.md`.
- **09/08/2026 — Dựng khung backend (Phase 1):** 10 gói, 3 "profile" tìm kiếm (dùng `dense_only`), log thử, khuôn kết quả · **PASS**; sau này
  profile bị thay bởi nhóm runtime `dense_bm25_rrf` (Phase 6) và gỡ hẳn 24/10.

## 5. Hôm nay còn đúng không

Kiểm lại với code hiện tại (`main` `1985a81`) lúc 17:12 31/10/2026.

| Kết quả / quyết định | Trạng thái | Căn cứ (file:dòng) |
|---|---|---|
| Khung gói `api, core, embedding, evaluation, ingestion, llm, reranking, retrieval, scoring, vectorstore` | **còn dùng**; thêm `experiments` | `ls backend/*/__init__.py` |
| `settings.yaml` tập trung + `load_settings()` | **còn dùng** | `backend/core/settings_loader.py:11` |
| 3 profile tìm kiếm, `dense_only` | **đã thay** bởi nhóm runtime `dense_bm25_rrf`, reranker `none` | `backend/config/settings.yaml:41-44` |
| `setup_logging()` + `logging.yaml` | **còn dùng** ở API; lệnh dựng kho chưa theo | `backend/core/logging_setup.py:13`; `backend/api/app.py:38` |
| `/health` | **còn dùng**, bản Phase 6: có thêm `tokenizer`, giá trị `ready` / `not_ready` | `backend/api/health.py:15-24` |
| `RetrievedDocument(id, score, text, metadata)` | **còn dùng** | `backend/core/schema.py:35-42`; `backend/retrieval/full_corpus.py:295` |
| Đơn giản là mặc định; không fallback / abstraction phòng xa | **còn dùng** | `session_prompt/Session_Prompt.md` §7 |
| Không mock / fake làm bằng chứng | **còn dùng** (luật); còn một file test dùng bản giả ở nhánh lỗi | `session_prompt/Session_Prompt.md` §6; `backend/tests/test_phase6_live_smoke.py:219-231` |
| Kiểm checksum / chống sửa trộm kiểu cũ | **đã thay** bởi phiếu build + hash corpus (Phase 7A2) | `backend/retrieval/full_corpus.py:383-385`, `:685` |
| Test chạy hệ thống thật | **còn dùng**; không test nào tạo / ghi collection | `backend/tests/conftest.py:1-5` |
| Sinh câu trả lời `gpt-5.4-nano` | **đã thay** bởi `gpt-6-luna` (23/10); vẫn qua OpenAI Agents SDK | `backend/config/settings.yaml:48`; `backend/llm/generator_openai_full_corpus.py:9` |
| Skill `karpathy-guidelines` | **đã thay** bởi `practical-project-coding` | `skills/` |

## 6. Việc còn lại / cần quyết

- Cho lệnh dựng chỉ mục dùng cấu hình log chung (`ingestion/full_corpus_pipeline.py:273`) — nhỏ, chưa có lịch.
- Bỏ bản giả trong `test_phase6_live_smoke.py` hoặc ghi rõ đây là test logic thuần — nhỏ, chưa có lịch.
- Không cần bạn quyết gì ở khâu này.

## Phụ lục — hồ sơ kỹ thuật

- Report lịch sử: `reports/phase_0_mvp_foundation_simplicity_review.md`,
  `reports/user_reports/phase_1_backend_skeleton_user_report.md`,
  `reports/user_reports/phase_1_backend_skeleton_simplicity_user_report.md`.
- Bản 1: B8, 24/10/2026. Bản 2: B10, sau dọn B9 (commit `1832201`; report
  `report_agent/2026-10-24_to_chuc_bao_cao/phase_7_cleanup_implementation.md`, review `phase_7_cleanup_review.md` cùng thư mục). Bản 3:
  sau rà code đợt 3 (merge `421c302`, 26/10).
- **Tài liệu cũ lệch code (còn, chỉ là lịch sử, không gây lỗi):** report Phase 1 ghi `generator: configured` (code trả `ready` / `not_ready`);
  spec Phase 1 đòi mọi lệnh dùng `setup_logging()`
  (`docs/superpowers/specs/2026-08-24-phase-1-backend-foundation-simplicity-design.md:86`, `:136-137`); spec governance cũ
  (`docs/superpowers/specs/2026-08-23-project-simplicity-governance-design.md`) trỏ `skills/karpathy-guidelines/SKILL.md` đã không còn;
  `guides/phase_1_backend_skeleton.md:34` ghi bước tiếp là Phase 6. Các lệch khác ghi
  ở bản 1 (mock ở 2 file test, `conftest.py` trỏ collection món ăn, kiểm `active_profile`) đã gỡ ở B9 (24/10).
