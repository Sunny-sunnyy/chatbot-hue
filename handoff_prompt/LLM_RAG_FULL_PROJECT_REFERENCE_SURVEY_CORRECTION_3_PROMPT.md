# Implementer — correction lượt 3 khảo sát toàn bộ project `llm_rag`

Bạn là **Implementer** tại `/home/minhhieu/hue_rag`.

Sửa đúng các finding RR5–RR8 trong §7 của:

```text
reports/llm_rag_full_project_reference_survey_codex_review_2026_09_11.md
```

Report đích:

```text
reports/llm_rag_full_project_reference_survey_2026_09_11.md
```

Đây là correction Markdown/read-only hẹp. Không khảo sát lại toàn project,
không mở lại phần đã đóng và không tự thay quyết định canonical Hue.

## 1. Bootstrap và mức đọc bắt buộc

Đọc theo đúng thứ tự và mức sau. Với **mọi file `full-read`**, nếu công cụ hiển
thị bị cắt thì phải tiếp tục từ dòng dừng cho tới EOF; không được coi output bị
truncate là đã đọc xong:

1. `full-read` — `session_prompt/Session_Prompt.md`.
2. `targeted-read` — `session_prompt/Project_Status.md`: `Project overview`,
   `Current runtime and data`, `Thiết kế full-corpus hiện hành`, `Decisions
   currently in force`, `Safety and authorization boundaries`, và đoạn survey
   `llm_rag` trong `Workstream và roadmap`.
3. `full-read` — `session_prompt/IMPLEMENTER_WORKFLOW.md`.
4. `full-read` — `skills/risk-gated-agent-review/SKILL.md`.
5. `full-read` — `skills/practical-project-coding/SKILL.md`.
6. `full-read` — `session_prompt/CURRENT_HANDOFF.md`.
7. `full-read` — prompt correction lượt 3 này.
8. `full-read` — Codex review nêu trên; §7 là active findings, §§2, 6.3 và
   7.3 là các phần phải giữ đóng.
9. `full-read` — report đích hiện hành, toàn bộ 866 dòng hiện tại.
10. `targeted-read` — `guides/full_corpus_rag.md`: `Quyết định đã chốt`, `Nội
    dung chưa chốt`, `Chuỗi tài liệu và điểm duyệt`.
11. `targeted-read` —
    `docs/superpowers/specs/2026-09-09-full-corpus-context-decisions.md`: `Trả
    đáp án và nguồn`, `Qdrant collection strategy`, `Thứ tự quyết định sau khi
    survey đóng`.

Correction lượt 2 là `reference-only`; chỉ mở khi cần truy nguyên một yêu cầu
RR1–RR4. Original survey prompt cũng là `reference-only`; chỉ mở §§4–8 nếu cần
đối chiếu exact deliverable. Source `/home/minhhieu/llm_rag` là
`reference-only`: chỉ đọc exact files/anchors nêu ở §3 dưới đây và những anchor
khác trong report cần sửa sau khi audit. Không mở `.env`, logs, generated/binary
state, raw `rag_old_0`, notebooks hoặc đọc lại toàn source tree.

## 2. Phần phải giữ đóng

- Đúng 22 top-level deliverables theo original contract; 53 Python tổng = 40
  non-init + 13 init; 20 backend READMEs và 9 root first-party files.
- Một configured collection mặc định `nmk_chatbot_collection`, override bằng
  `QDRANT_COLLECTION_NAME`; static source không chứng minh live inventory.
- Dense+sparse cùng point; request path chỉ query dense; BM25 rescore dense
  pool; reranker/fusion/scoring in-memory. C3/C4 không được mở lại.
- Hue giữ 3 isolated baseline/6 A-B collections, Foods targets read-only, và
  trả answer + sources một lần (one-shot, non-streaming) cho MVP.
- Config table đã đủ env override names; health là dynamic/not-verified;
  reranker chỉ ghi `metadata["rerank_score"]`, không đổi `doc.score`.
- Frontend `onDone` chỉ cập nhật session ID; loading tắt trong `finally`; success
  sequence là `meta -> delta* -> sources -> done`, `error` là alternative.
- Danh sách đủ 20 test names và historical labels cốt lõi đã có; chỉ sửa exact
  mock boundary/wording còn sai.

## 3. Correction bắt buộc

### E1 — RR5: coverage, core model và ingestion lifecycle

- Sửa breakdown inventory: `backend/api/` có 4 non-init Python files;
  `backend/tests/` có 4 Python files. Giữ tổng 40 non-init + 13 init.
- Sửa SHA-256 của cả hai raw exports thành
  `b38e8cf04a2e392733037e89fafffaeab0f6ecfc49253965105278a4a007c598`.
  Không đổi size/count nếu source không thay đổi.
- Mô tả đúng `backend/core/schema.py:1-11`: `RetrievedDocument` là
  `@dataclass`; bốn fields `id`, `score`, `text`, `metadata`; metadata bắt buộc,
  không có Pydantic `BaseModel`/`Field(default_factory=dict)`.
- Mô tả đúng call flow:
  `ingestion/pipeline.py:17-33` gom kết quả bảy chunkers rồi gọi
  `upsert_chunks(all_chunks)`;
  `vectorstore/upsert.py:15-38` nhận chunks, lấy client, ensure collection, fit
  sparse, init shared sparse embedder, build points rồi gọi **một lần**
  `client.upsert(..., points=points)`. Không có batch-upsert 64 trong active
  path; 64 chỉ là batch size của dead `batch_embed.py`.
- Không nói mọi invocation có 450 texts. Static fact là active point builder
  gửi toàn bộ `texts` của invocation vào `embed_texts(texts)`; 450 chỉ là
  `[Documented historical result]`.

### E2 — RR6: facts, config, dependencies và anchor audit

- Sửa `app.env` default thành `production` từ `settings.yaml:5`.
- Audit toàn bộ anchor trên report theo source HEAD; sửa claim cùng số dòng,
  không chỉ sửa URL. Tối thiểu đối chiếu:
  - `embedding/embedder.py:9-10, 14-18, 21-27`;
  - `llm/generator_openai.py:22-29, 44-68, 71-109, 112-153`;
  - `core/startup.py:16-19, 45-107`;
  - `retrieval/context_builder.py:8-12, 40-62`;
  - `embedding/sparse_embedder.py:8-17, 52-55, 74-83, 112-135`;
  - `retrieval/hybrid_retriever.py:24-74`;
  - `llm/prompt.py:30-42`;
  - `api/routes/chat.py:81-151`;
  - `api/routes/chat_openai.py` cho source construction/event generator;
  - `vectorstore/hybrid_index.py`, `qdrant.py`, `upsert.py` cho vector flow.
- Legacy `/api/chat` broad catch biến intended 503 thành 500, nhưng detail 500
  là chuỗi tiếng Việt cố định ở `chat.py:148-150`, không phải `str(e)`.
- Với dependency, phân biệt constraint trong `pyproject.toml`, resolved version
  trong `uv.lock`, frontend manifest/lock và Qdrant server image trong compose.
  Bỏ câu Python `qdrant-client` “tương thích container v1.18.3” nếu không có
  source compatibility evidence. Không chạy package manager.
- Bỏ self-review claim “100% anchors chính xác”. Thay bằng mô tả hữu hạn và
  limitation kiểm chứng được.

### E3 — RR7: frontend và test boundaries

- Sửa source UI: không có accordion hay helper `getSourceImage()`.
  `ChatInterface.tsx:182-233` filter inline bảy image URL fields, lấy tối đa ba
  nguồn và render image cards.
- Mô tả Markdown/HTML đúng mức source chứng minh: current component dùng
  `ReactMarkdown` + `remarkGfm` và không cấu hình plugin xử lý raw HTML. Không
  gọi đây là “sanitizer tự động” hoặc security guarantee nếu report không có
  exact supporting evidence.
- Bỏ claim có `sm:`/`md:` breakpoint và Shift+Enter; current form dùng text
  `<input>` và submit form. Chỉ giữ accessibility/responsive behavior có exact
  source anchor.
- Thay “0% test coverage” bằng fact: không tìm thấy first-party automated
  frontend test files/test framework config trong inventory đã khảo sát; không
  có coverage run nên phần trăm coverage là `[Not verified]`.
- Giữ đủ 20 test names nhưng sửa exact boundaries của sáu API tests theo
  `backend/tests/test_api_chat_openai.py`: tests 15, 16, 18 không monkeypatch
  `check_rate_limit`; test 17 dùng class `FakeReranker`, không phải
  `MockReranker`. Liệt kê đúng mọi object được monkeypatch trong từng test.

### E4 — RR8: tone, self-review và open decisions

- Quét toàn report và handoff; bỏ các praise/causal/completion assertions như
  “xử lý triệt để”, dùng “chuẩn mực” để ca ngợi quyết định/khung đánh giá, hoặc
  tự nhận đã loại hết khi chưa đúng. Thuật ngữ nằm trong trích dẫn source code
  không cần đổi; prose của report phải trung tính.
- Không nói IP/session keys lưu “vĩnh viễn”. Nêu đúng: source không có TTL/key
  deletion/cleanup; các entries có thể còn suốt vòng đời process và tạo rủi ro
  tăng memory theo cardinality/history.
- Matrix không chốt `script recreate/reset` hoặc cleanup mechanism. Đưa về
  option/open question cho Written Spec, giữ approval chain guide -> written
  spec -> User duyệt spec -> implementation plan + Review Contract -> User
  duyệt plan -> Implementer.
- Đổi prescription “tuyệt đối không” thành observed risk/candidate lesson khi
  đó không phải canonical Hue decision hay safety boundary.
- Self-review phải nêu các kiểm tra thực hiện và limitation; không claim mọi
  assertion/anchor/tone đã hoàn hảo hoặc tự claim PASS/approval/closure.

## 4. Phạm vi file và quyền

Chỉ được sửa:

1. `reports/llm_rag_full_project_reference_survey_2026_09_11.md`;
2. `session_prompt/CURRENT_HANDOFF.md`.

Không sửa Codex review, correction prompt, guide/spec/notes/status, runtime,
tests, corpus, Golden, index, dependencies hoặc `/home/minhhieu/llm_rag`.
Không chạy/import Python/Node/project code, tests, model, API, Qdrant, notebook,
browser, build hay benchmark; không network, đọc `.env`/logs, Git write hoặc
spawn subagent. Chỉ dùng read-only text/file/Git utilities.

## 5. Verification và bàn giao

Trước bàn giao:

1. đọc lại toàn bộ report đã sửa đến EOF;
2. kiểm 22 top-level sections vẫn đúng thứ tự;
3. kiểm inventory subgroup/checksum/dataclass/ingestion-upsert và 450 label;
4. kiểm config defaults/dependency wording và audit anchor toàn report;
5. kiểm frontend/test boundaries;
6. dùng `rg` quét banned/completion wording, `0%`, `vĩnh viễn`,
   `getSourceImage`, `accordion`, `upsert_chunks(client`, stale anchors và tự
   xem từng match trong ngữ cảnh;
7. chạy `git diff --check` và `wc -l -c` (read-only verification).

Không tự claim PASS/approval/completed. Cập nhật `CURRENT_HANDOFF.md` về
`reviewer`/`final_review`, giữ base commit, `Head commit: worktree`, risk low,
Git/subagent none. Next action duy nhất: Reviewer re-review correction lượt 3
RR5–RR8.
