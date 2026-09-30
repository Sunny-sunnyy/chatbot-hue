# Codex Review: Full-corpus Metadata v2 Workstream (Tasks 1–7)

Decision: approved — User-confirmed closure 2026-09-30 +07
Reviewer: Codex
Date: 2026-09-30 +07
Canonical guide: `guides/full_corpus_rag.md`
Implementation report: `reports/full_corpus_metadata_v2_implementation_2026_09_29.md`

## 1. Phạm vi đã review

Reviewer đã full-read Metadata v2 Written Spec, Implementation Plan/Review
Contract, implementation report và current handoff; đọc exact implementation
diff từ base `92f2e2cce0e85c9b4f733aaab038bc99cad314c0` tới worktree hiện hành.

Các path implementation được kiểm trực tiếp:

- `backend/core/schema.py`;
- `backend/ingestion/full_corpus_metadata_v2.py`;
- `backend/ingestion/full_corpus_pipeline.py`;
- `backend/ingestion/source_state.py`;
- `backend/retrieval/full_corpus.py`;
- `backend/vectorstore/points.py`;
- năm focused test files được khóa trong Task 7;
- bốn ignored v2 build records, tracked Gate 1 preflight artifact và ignored
  Gate 2/Gate 3 evidence artifacts.

Reviewer đối chiếu staged/unstaged/untracked inventory. Khối staged corpus
untracking/deletion, `.gitignore`, guide/status và các report lịch sử ngoài
exact Metadata v2 implementation được coi là pre-existing/unrelated state và
không bị sửa. Canonical corpus vẫn hiện diện trên filesystem dưới ignore rule;
fresh verification đã rediscover đủ source state và đạt.

Gate 2 independent target/vector review và Gate 3 Correction 1 runtime/smoke
review được targeted-read để xác định evidence có thể reuse. Task 7 không đổi
collections, vectors, build records hay runtime behavior nên evidence này vẫn
hợp lệ; Reviewer không gọi đó là fresh Task 7 execution.

## 2. Findings

Không có `blocker` hoặc `major`.

### F1 — Minor — Inventory trong evidence index chưa khớp exact Git state

Vị trí:

- `reports/full_corpus_metadata_v2_implementation_2026_09_29.md`, mục
  `Changed paths and responsibilities`;
- `session_prompt/CURRENT_HANDOFF.md`, mục danh mục tập tin triển khai trước
  khi handoff này được thay bằng closure packet.

Requirement: comprehensive report/handoff phải là evidence index chính xác cho
mọi changed/untracked implementation path và phân biệt current Git state.

Evidence:

- inventory bỏ sót `backend/vectorstore/points.py` và
  `backend/tests/test_full_corpus_sparse.py`;
- inventory gán `FullCorpusChunk.domain` và seven-field payload cho
  `backend/ingestion/chunker.py`, trong khi exact diff đặt thay đổi này tại
  `backend/core/schema.py`;
- `backend/ingestion/full_corpus_metadata_v2.py` và test tương ứng được mô tả
  là untracked dù hiện nằm trong commit `adb060c`; bốn build records v2 là
  ignored runtime state dưới `data/`, không xuất hiện trong Git inventory.

Tác động: người đọc report có thể chọn thiếu source anchor hoặc hiểu sai trạng
thái Git. Không ảnh hưởng runtime, collection, vector, payload hoặc acceptance
và không biện minh một correction riêng.

Tiêu chí đóng: final Codex review và closure handoff dùng exact inventory như
phần 1. Implementer report được giữ nguyên làm lịch sử; không sửa retroactively.
F1 được ghi nhận là minor evidence-only, không chặn readiness.

## 3. Cách Reviewer chạy lại thật

```bash
git rev-parse HEAD
git cat-file -t 92f2e2cce0e85c9b4f733aaab038bc99cad314c0
git status --short
git diff --check

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache \
  uv run --env-file .env python -m pytest \
  backend/tests/test_full_corpus_chunker.py \
  backend/tests/test_full_corpus_sparse.py \
  backend/tests/test_full_corpus_qdrant_ingestion.py \
  backend/tests/test_full_corpus_metadata_v2.py \
  backend/tests/test_full_corpus_retrieval.py -q --tb=short

UV_CACHE_DIR=/tmp/hue-rag-metadata-v2-review-uv-cache \
  uv run --env-file .env python -m \
  backend.ingestion.full_corpus_metadata_v2 verify

sha256sum data/full_corpus_builds/hue_full_corpus_a_e5_small_384.json \
  data/full_corpus_builds/hue_full_corpus_a_e5_base_768.json \
  data/full_corpus_builds/hue_full_corpus_a_huydang_dek21_768.json \
  data/full_corpus_builds/hue_full_corpus_a_qwen3_06b_1024.json
```

Reviewer còn đọc read-only Qdrant collection-info endpoint cho bốn legacy và
bốn metadata-v2 collections, kiểm tracked artifact privacy bằng allowlist/pattern
scan, và đọc cấu trúc bốn v2 build records cùng exact vector-copy lineage.

## 4. Kết quả quan sát

- Base commit hợp lệ; current `HEAD` là
  `cd369100855aa61dd9c859b9524f9867b17eec32`.
- Fresh focused suite: `158 passed in 120.21s`, exit `0`.
- Fresh complete read-only verify: `Verification status: VERIFIED`, exit `0`;
  đủ bốn source/target pairs và 33.840 target points được kiểm qua production
  verification path.
- Verify in ba tokenizer length warnings trong bước corpus preparation
  (`265 > 256`, hai lần `598 > 512`) nhưng không có verification failure;
  final status vẫn `VERIFIED`.
- `git diff --check`: exit `0`.
- Cả tám Qdrant collections đều `green`, mỗi collection có `8.460` points,
  exact dense dimension `384/768/768/1024`, sparse vector name `sparse` và
  `payload_schema == {}`.
- Bốn legacy v1 record SHA-256 fresh-check khớp lineage trong bốn v2 records:
  `ea19021a…c76`, `0cd69406…d7b`, `10b3f847…c4a`, `2faa9d4f…dd5`.
- Tracked preflight artifact là `READY`, 4/4 pairs, `total_mutations: 0`; scan
  không tìm absolute path, secret, query/search/evidence dump hoặc vector dump
  trong tracked final evidence được kiểm.
- Static call-path check xác nhận migration module không import/call dense
  runner hoặc external model; Qdrant mutation chỉ nằm trong guarded `migrate`
  path. `preflight` và `verify` là read-only.
- Reused Gate 3 evidence: no-rerank smoke `8/8 PASS`, MiniLM smoke `2/2 PASS`,
  determinism true và không anomaly. Reuse hợp lệ vì Task 7 chỉ thêm report/
  handoff và chạy verification, không đổi runtime path đã được review.
- Lần curl collection-info đầu trong sandbox không kết nối được localhost;
  exact read-only check được chạy lại ngoài sandbox và PASS. Không dùng lần
  sandbox failure làm evidence về Qdrant state.

## 5. Giới hạn hoặc phần chưa chạy

- Không rerun `migrate`, đúng hard boundary để tránh lặp live write.
- Không chạy full backend suite; Review Contract khóa final regression vào năm
  focused suites và không có failure/blast-radius evidence yêu cầu mở rộng.
- Không rerun Gate 3 retrieval smoke trong Task 7. Gate 3 runtime không có delta
  sau independent Correction 1 review; smoke evidence được reuse có ghi nguồn.
- Reviewer không audit nội dung của 264 pre-existing corpus deletions/untracking
  ngoài scope; chỉ xác nhận chúng được bảo toàn và fresh corpus/runtime
  verification vẫn đọc được canonical state hiện hành.

Các giới hạn này không chặn decision vì exact high-risk data path, lineage,
collection schema/count, complete vector/payload verification và focused
runtime contracts đều có independent evidence phù hợp.

## 6. Decision và bước tiếp theo

Technical decision: `ready_for_user_confirmation`.

Metadata v2 Tasks 1–7 đạt approved acceptance: exact seven-field payload và
five-value domain; deterministic logical/storage identity; fixed four-pair
vector-copy migration; v2 build/payload schema cùng lineage; strict source
freshness; four fully verified immutable targets; logical result ID/private
trace; unchanged ranking, public API và Golden boundaries; không payload index,
filter/router, re-embedding hoặc paid API/model call.

F1 là minor evidence-only và không mở correction. Phase 6, cleanup/delete,
Qdrant mutation, evaluation và Git operations vẫn đóng.

### Approval Closure Contract

User confirmation được đề nghị:

```text
Tôi xác nhận closure Full-corpus Metadata v2 Workstream Tasks 1–7 theo final
Codex review; giữ Phase 6 paused và không cấp quyền cleanup/delete, Qdrant
mutation, evaluation, paid model/API hay Git commit/push.
```

Sau exact confirmation, Reviewer được phép thực hiện các chỉnh sửa cơ học:

1. đổi decision của review này thành User-confirmed closure;
2. cập nhật `Project_Status.md`, `guides/full_corpus_rag.md` và
   `CURRENT_HANDOFF.md` thành Metadata v2 completed;
3. ghi trạng thái closure trong user report;
4. giữ `git_authorization: none`, không tạo Implementer handoff mới và chờ User
   quyết định có mở lại Phase 6 hay workstream khác hay không.

### User confirmation recorded

Ngày 2026-09-30 +07, User đã xác nhận exact Approval Closure Contract. Metadata
v2 Workstream Tasks 1–7 chuyển thành User-confirmed closure. Phase 6 tiếp tục
`paused_before_implementation`; cleanup/delete, Qdrant mutation, evaluation,
paid model/API và Git commit/push vẫn không có authority.
