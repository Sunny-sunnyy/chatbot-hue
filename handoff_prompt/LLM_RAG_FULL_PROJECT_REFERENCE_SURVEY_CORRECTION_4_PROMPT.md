# Implementer — correction lượt 4 khảo sát toàn bộ project `llm_rag`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Sửa đúng RR9–RR10 tại §8 của:

```text
reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md
```

Report đích:

```text
reports/llm_rag_full_project_reference_survey_2026_09_11.md
```

Đây là correction Markdown/read-only cuối cùng trước complexity-reset ceiling.
Không khảo sát lại project, không mở phần đã đóng và không thay quyết định Hue.

## 1. Bootstrap và mức đọc bắt buộc

Đọc theo thứ tự. Với mọi file `full-read`, output bị cắt/truncate phải đọc tiếp
từ dòng dừng tới EOF:

1. `full-read` — `session_prompt/Session_Prompt.md`.
2. `targeted-read` — `session_prompt/Project_Status.md`: `Project overview`,
   `Current runtime and data`, `Thiết kế full-corpus hiện hành`, `Decisions
   currently in force`, `Safety and authorization boundaries`, đoạn survey
   `llm_rag` trong `Workstream và roadmap`.
3. `full-read` — `session_prompt/IMPLEMENTER_WORKFLOW.md`.
4. `full-read` — `skills/risk-gated-agent-review/SKILL.md`.
5. `full-read` — `skills/practical-project-coding/SKILL.md`.
6. `full-read` — `session_prompt/CURRENT_HANDOFF.md`.
7. `full-read` — correction contract lượt 4 này.
8. `full-read` — Codex review; §8 là active findings, §§2, 6.3, 7.3 và 8.3 là
   phần phải giữ đóng.
9. `full-read` — toàn bộ report đích hiện hành (881 dòng trước correction).
10. `targeted-read` — `guides/full_corpus_rag.md`: `Quyết định đã chốt`, `Nội
    dung chưa chốt`, `Chuỗi tài liệu và điểm duyệt`.

Correction cũ/original survey là `reference-only`; chỉ mở exact section khi cần
truy nguyên. Trong `/home/minhhieu/llm_rag`, chỉ đọc exact sources ở §3 và file
được một report anchor cần kiểm; không đọc lại tree, `.env`, logs, generated/
binary state, raw `rag_old_0` hay notebooks.

## 2. Phần phải giữ đóng

- Toàn bộ conclusions tại review §§2, 6.3, 7.3 và 8.3.
- Đúng 22 deliverables; totals inventory; checksum; dataclass; §8 ingestion/
  upsert; historical 450; dependency separation; legacy API detail.
- Collection and retrieval conclusions; Hue 3/6 isolated collections; Foods
  read-only; one-shot non-streaming.
- Frontend rendering/HTML limitation/loading behavior và exact 20 test names/
  monkeypatch boundaries đã đóng.
- Retention wording và lifecycle option/open-decision boundary đã sửa.

## 3. Correction bắt buộc

### F1 — RR9: sửa duplicate entrypoint và config consumer matrix

1. Tại §4.2, thay anchor không tồn tại `pipeline.py:126-170` bằng call flow:
   - `pipeline.py:17-33`: gọi bảy chunkers, gom `all_chunks`, rồi
     `upsert_chunks(all_chunks)`;
   - `upsert.py:15-38`: client/collection/sparse fit/build points/one upsert;
   - `hybrid_index.py:17-53`: dense+sparse point construction.
   Không nói các bước transitive nằm trực tiếp trong `pipeline.py`.
2. Tại §8.1, sửa “37 dòng” thành 36 dòng hoặc bỏ file-length claim.
3. Tại executive §1.3, anchor exact `using="dense"` là
   `hybrid_retriever.py:41`; có thể dùng range 38–45.
4. Audit từng row §6.2 theo actual consumer:
   - `app.name`: không tìm thấy runtime consumer; `settings_loader.py:16` chỉ là
     function declaration;
   - `app.env`: có override ở `settings_loader.py:22-23`, nhưng không tìm thấy
     runtime consumer khác;
   - `data.raw_dir`: `load_data.py:16`;
   - `data.processed_dir`: `load_data.py:35` và exact chunker reads;
   - `embedding.batch_size`: đọc ở `batch_embed.py:9`, dùng ở 18–19; module
     không có caller;
   - `vector_database.api_key`: dùng ở `qdrant.py:30` và 39;
   - retrieval `top_k`, `score_threshold`, `dense_weight`, `bm25_weight`:
     `hybrid_retriever.py:19-22`, với actual effects tại 42/44/58/74 khi liên
     quan.
5. Kiểm các row còn lại để cột “consumer” thực sự là nơi đọc/dùng setting;
   không dùng loader override như bằng chứng duy nhất cho runtime consumption.
   Nếu setting chỉ loaded/overridden nhưng unused, ghi rõ `no runtime consumer
   found`.
6. Quét toàn report cho link có anchor bắt đầu vượt EOF và sửa mọi match. Sau
   đó semantic-check các anchor Config/Entrypoint, vì in-range không đồng nghĩa
   đúng claim.

Exact source full-read cho F1:

```text
/home/minhhieu/llm_rag/backend/ingestion/pipeline.py
/home/minhhieu/llm_rag/backend/vectorstore/upsert.py
/home/minhhieu/llm_rag/backend/vectorstore/hybrid_index.py
/home/minhhieu/llm_rag/backend/core/settings_loader.py
/home/minhhieu/llm_rag/backend/ingestion/load_data.py
/home/minhhieu/llm_rag/backend/embedding/batch_embed.py
/home/minhhieu/llm_rag/backend/retrieval/hybrid_retriever.py
/home/minhhieu/llm_rag/backend/vectorstore/qdrant.py
/home/minhhieu/llm_rag/backend/config/settings.yaml
```

### F2 — RR10: đồng bộ coverage và evidence wording

1. §3.1 processed overview phải khớp §3.2.3: năm full-read files
   (`companyInfo`, `architectureTypes`, `interiorStyles`, `newsCategories`,
   `projectCategories`) và ba sampled files (`heroSlides`, `projects`, `news`).
2. §5.2 chỉ kết luận source không có application-level authentication/
   authorization. Không suy từ đó rằng deployment/network chắc chắn public.
3. §16.2 bỏ “biến môi trường được tải an toàn”; chỉ nêu `python-dotenv` load
   env và không thấy API-key logging trong exact paths đã kiểm.
4. §15.3 chỉ mô tả observed `reasoning.effort="none"`; nếu nêu mục đích/quota,
   gắn `[Documented intent]` hoặc `[Inference]`, không gọi là behavior verified.
5. §22.3 bỏ “sửa toàn bộ”/completion absolutes; mô tả các nhóm anchor đã kiểm và
   static-review limitation. Không tự claim PASS/approval/closure.
6. Trong recommendations/matrix, phân biệt rõ `[Canonical Hue decision]`,
   model preprocessing requirement có source và `[Candidate lesson for Hue]`.
   Không dùng “bắt buộc” để biến candidate lesson thành quyết định Hue.

## 4. Quyền và phạm vi file

Chỉ được sửa:

1. `reports/llm_rag_full_project_reference_survey_2026_09_11.md`;
2. `session_prompt/CURRENT_HANDOFF.md`.

Không sửa Codex review/correction prompt/guide/spec/status/runtime/tests/corpus/
Golden/index/dependencies hay `/home/minhhieu/llm_rag`. Không chạy/import code,
tests, model, API, Qdrant, frontend build/notebook/benchmark; không network,
đọc `.env`/logs, Git write hoặc subagent.

## 5. Verification và bàn giao

Trước bàn giao:

- đọc lại toàn report đã sửa tới EOF;
- xác nhận 22 sections và phần đã đóng không đổi;
- kiểm §1.3, §3.1, §4.2, toàn bảng §6.2, §8.1, §15.3, §16.2, §22.3;
- chạy scan anchor-vượt-EOF và semantic-check consumer anchors F1;
- dùng `rg` tìm các stale strings: `pipeline.py:126`, `37 dòng`,
  `hybrid_retriever.py:40`, `settings_loader.py:16`, `load_data.py:10`,
  `load_data.py:11`, `batch_embed.py:16`, retrieval anchors 18–21, “được tải
  an toàn”, “mở hoàn toàn cho truy cập công khai”, “sửa toàn bộ”;
- chạy `git diff --check` và `wc -l -c`.

Cập nhật `CURRENT_HANDOFF.md` về reviewer/final_review, giữ base commit,
`Head commit: worktree`, risk low, Git/subagent none. Next action duy nhất:
Reviewer re-review correction lượt 4 RR9–RR10. Không tự claim PASS/approved/
completed.
