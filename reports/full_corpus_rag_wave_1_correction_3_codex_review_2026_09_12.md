# Codex Review: Full-corpus RAG Wave 1 Correction 3

Decision: approved
Reviewer: Codex
Date: 2026-09-12
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_rag_wave_1_correction_1_implementation_report_2026_09_12.md`

## 1. Phạm vi đã review

Reviewer đã kiểm static/read-only:

- base/HEAD `d631d3cc47a66d7a43c71f36c585d73ae9d21f9e`, toàn bộ
  `git status --short --untracked-files=all`, task paths và `git diff --check`;
- full Correction 3 Contract, Review Correction 2, implementation report cập
  nhật và toàn bộ `backend/tests/test_full_corpus_chunker.py` đến EOF;
- targeted canonical preview artifact và exact source sections Mệ Kéo/Gia Lạc;
- exact W1-C2-R1 acceptance và các Wave 1 requirements đã được review trước đó.

Reviewer không chạy tests, preview CLI, tokenizer/model/API, embedding, Qdrant,
frontend, notebook hoặc benchmark; không đọc `.env`, logs hoặc model cache; không
thực hiện Git write.

## 2. Findings

Không còn Blocker hoặc Major.

W1-C2-R1 đã closed:

- `backend/tests/test_full_corpus_chunker.py:987-1019` gọi full chunker hai lần,
  so sánh ordered chunk fields/evidence, kiểm unique chunk/point IDs, đối chiếu
  `point_id_for_chunk_id()` và UUID version 5;
- `:1030-1035` giữ hai preview outputs byte-identical;
- `:575-604` chọn hai exact Mệ Kéo chunks, kiểm content/evidence/source slices và
  distinct IDs, không còn multi-chunk join;
- `:616-658` chọn exact historical, contemporary và non-commercial Gia Lạc
  chunks, kiểm các cặp quan hệ, source slices và distinct historical/contemporary
  IDs;
- implementation report phản ánh đúng delta, 24 test names, exact commands/
  results và hai suite `NOT RUN`; không tự tuyên bố approved/closed.

Không phát hiện complexity hoặc duplication mới cần correction. Delta chỉ thêm
direct assertions và một import thư viện chuẩn `uuid`; production code/config,
corpus và canonical artifact không bị Correction 3 sửa.

## 3. Cách Reviewer chạy lại thật

Reviewer chỉ chạy các lệnh static/read-only sau:

```bash
git rev-parse HEAD
git merge-base HEAD d631d3cc47a66d7a43c71f36c585d73ae9d21f9e
git status --short --untracked-files=all
git diff --check
wc -l <full-read inputs>
sed -n <complete ranges> <full-read inputs>
rg -n <required assertions> backend/tests/test_full_corpus_chunker.py
jq <artifact consistency projection> reports/artifacts/full_corpus_rag_wave_1_preview_2026_09_11.json
```

Các lệnh đều hoàn tất như dự kiến; `git diff --check` exit 0. Reviewer không chạy
các command động do Implementer báo.

## 4. Kết quả quan sát

- Base và HEAD khớp commit tài liệu `d631d3c`; Wave 1 implementation vẫn là
  worktree chưa commit đúng lifecycle hiện hành.
- Test source hiện có 24 Wave 1 test functions; Correction 3 không tăng count mà
  siết direct assertions trong hai sample tests và determinism test.
- Canonical artifact vẫn tự nhất quán: `PASS`, 205 unique/sorted sources, 8460
  chunks, 3 condition rules, zero blocking errors và zero oversized groups.
- Domain/P7 totals đều cộng về 205/8460. Max observed token là `366/512`,
  `366/512`, `255/256`.
- Exact strings mà tests dùng tồn tại trong source Mệ Kéo/Gia Lạc và assertions
  không còn nối nhiều chunks.
- Implementer evidence ghi fresh suite `39 passed, 1 warning`, preview exit 0 và
  `cmp` exit 0. Đây là execution evidence được đối chiếu với source/artifact,
  không phải fresh Reviewer run.

## 5. Giới hạn hoặc phần chưa chạy

- Reviewer không rerun tests/tokenizers/preview theo authority xuyên suốt Wave 1;
  execution status là Implementer evidence.
- Full backend suite và `test_ingestion_pipeline.py` không chạy vì dùng real
  Qdrant/embedder ngoài offline Wave 1 acceptance.
- Wave 1 chỉ chứng minh discovery/parser/chunker/locator/Representation A preview
  offline. Chưa embedding inference, Qdrant ingestion, retrieval, generation,
  frontend, Golden hoặc benchmark; không được suy diễn readiness cho Wave 2+.

## 6. Decision, Approval Closure Contract và bước tiếp theo

Technical verdict trước User closure là `ready_for_user_confirmation`.

### Approval Closure Contract

Xác nhận cần từ User:

```text
Tôi xác nhận closure Full-corpus RAG Wave 1.
```

Xác nhận chỉ công nhận Wave 1 technical readiness với observed artifact/giới hạn
nêu trên. Nó không phê duyệt Wave 2.1, live Qdrant/API/paid calls, representation
B, Golden, finalist, winner/cutover/replacement/cleanup hoặc Agentic RAG.

Sau exact User confirmation, Reviewer được phép:

1. đổi review/Project Status từ `ready_for_user_confirmation` sang User-approved
   Wave 1 closure;
2. cập nhật `guides/README.md`, `guides/full_corpus_rag.md` và
   `guides/phase_2_foods_markdown_chunking.md` bằng observed Wave 1 results và
   limitations, phân biệt Foods as-built history, approved full-corpus target và
   observed Wave 1 result;
3. cập nhật `reports/README.md`, `handoff_prompt/README.md` và các session indexes
   cần thiết;
4. chuyển `session_prompt/CURRENT_HANDOFF.md` sang Reviewer/`next_design` cho
   Phase 3/Wave 2.1, chưa giao Implementer;
5. commit và push lên `origin/main` toàn bộ Wave 1 implementation/config/tests,
   canonical preview, implementation/review reports, contracts và closure docs
   thuộc task paths. Không đưa các historical untracked survey files có whitespace
   debt hoặc nội dung ngoài Wave 1 vào commit này.

Sau closure, Reviewer mới bắt đầu design gate Wave 2.1 từ observed Wave 1 evidence,
brainstorm từng quyết định còn mở và trình User duyệt trọn design package trước
khi tạo bất kỳ Implementer handoff nào.

### User closure — 2026-09-12

User đã xác nhận exact câu `Tôi xác nhận closure Full-corpus RAG Wave 1.`. Wave 1
được chuyển thành `approved` trong đúng phạm vi offline và limitations của review
này. Approval không mở Wave 2.1 implementation hoặc bất kỳ live/paid gate nào.
Reviewer được thực hiện năm action cơ học trong Approval Closure Contract; handoff
tiếp theo là Reviewer/`next_design`.
