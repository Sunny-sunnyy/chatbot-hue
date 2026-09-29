# Bàn giao hiện hành — Đánh giá lại metadata Full-corpus

Target role: reviewer
Authored by: reviewer
Handoff kind: next_design
State: active
Base commit: 41b638642caf432fc7484d08444ba609a0368708
Head commit: HEAD
Risk level: high — thay đổi metadata có thể ảnh hưởng chunk contract, Qdrant payload, retrieval, citation/API và rebuild collections
Git authorization: none
Sub-agent authorization: none

## Quyết định mới nhất của User

Ngày 2026-09-29, User yêu cầu dừng Full-corpus Phase 6 trước implementation để
đánh giá lại metadata. Phase 6 Written Spec/Plan/Review Contract vẫn được giữ
làm artifact đã duyệt tại thời điểm 2026-09-14, nhưng không còn cấp authority
thực thi cho tới khi metadata design và các dependency bị ảnh hưởng được User
duyệt lại.

Không chạy Task 1 của Phase 6, không gọi Qwen/OpenRouter và không dùng quyền năm
call trước đây. Không sửa runtime, rebuild index hoặc mutate bốn canonical
full-corpus collections trong handoff này.

## Mục tiêu

Cùng User đánh giá metadata hiện hành theo consumer thật, xác định phần nào cần
giữ, bổ sung, suy diễn hoặc tách sang document/build metadata, rồi mới thiết kế
amendment phù hợp. Không chọn field mới chỉ vì có thể hữu ích trong tương lai.

## Trạng thái metadata hiện hành

- Phase 2 tạo `FullCorpusChunk` với identity nội bộ, source/title/heading path,
  exact `evidence_parts` và Representation A `search_text`.
- Phase 4 Qdrant payload đang có đúng năm field: `search_text`, `source`,
  `title`, `heading_path`, `evidence_parts`.
- Domain/subdomain hiện suy từ `source`; source hashes, corpus/model/sparse
  identity nằm ở file/build record; dense/sparse vectors và point ID dùng trường
  Qdrant chuẩn.
- Phase 5 chỉ chuyển `source`, `title`, `heading_path`, `evidence_parts` vào
  retrieval document metadata. Bốn canonical collections hiện read-only.
- Exact provenance bằng offsets/text trong `evidence_parts` là behavior đã được
  kiểm chứng và phải được xem là dependency an toàn quan trọng khi redesign.

## Active inputs và mức đọc

Full-read:

```text
session_prompt/Session_Prompt.md
session_prompt/REVIEWER_WORKFLOW.md
session_prompt/Project_Status.md
session_prompt/CURRENT_HANDOFF.md
skills/risk-gated-agent-review/SKILL.md
```

Targeted-read phần metadata/payload/source locator/consumer:

```text
guides/full_corpus_rag.md
guides/phase_2_foods_markdown_chunking.md
guides/phase_4_qdrant_ingestion.md
guides/phase_5_retrieval_profiles_reranking.md
guides/phase_6_generation_api.md
backend/core/schema.py
backend/ingestion/source_state.py
backend/ingestion/chunking/full_corpus_chunker.py
backend/vectorstore/points.py
backend/retrieval/full_corpus.py
```

Reference-only, chỉ mở để giải quyết claim hoặc trade-off cụ thể:

```text
docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md
docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md
docs/superpowers/specs/2026-09-14-phase-6-full-corpus-generation-api-ui-written-spec.md
docs/superpowers/plans/2026-09-14-phase-6-full-corpus-generation-api-ui-implementation-plan.md
reports/full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md
reports/full_corpus_phase_4_final_codex_review_2026_09_13.md
reports/full_corpus_phase_5_retrieval_reranking_codex_review_2026_09_13.md
```

## Design questions cần chốt tuần tự

1. Consumer thật cần metadata: retrieval filter/fusion, benchmark breakdown,
   context packing, citation/source cards, freshness/provenance hay vận hành.
2. Field nào thuộc document, chunk, build/collection hoặc chỉ nên derive.
3. Field nào phải nằm trong Qdrant payload và cần payload index; field nào nên
   nằm trong manifest để tránh lặp trên 8.460 points.
4. Identity nào cần ổn định qua edit/rechunk/taxonomy move.
5. Metadata nào có nguồn canonical đáng tin trong curated corpus; không suy
   diễn hoặc enrich bằng web khi chưa có data scope được duyệt.
6. Blast radius tối thiểu: chỉ derive ở retrieval, rebuild fresh collections,
   hay cần sửa parser/chunker và downstream contracts.

## Hard boundaries

- Đây là design/assessment, chưa cấp quyền implementation.
- Không thay đổi curated corpus, Qdrant, build records, runtime code hoặc tests.
- Không gọi paid API/model, không chạy benchmark và không production cutover.
- Không tự coi mọi metadata field đề xuất là requirement.
- Không sửa/xóa bốn canonical collections; mọi rebuild hoặc fresh collection
  cần exact approved plan và target riêng.
- Phase 2–5 closure vẫn là lịch sử hợp lệ cho implementation đã quan sát; design
  mới phải nêu rõ contract nào bị supersede và verification nào phải chạy lại.

## Next action duy nhất

Reviewer dùng brainstorming với User để lập inventory consumer và pain point
metadata thực tế. Sau khi User chốt hướng thiết kế, Reviewer mới soạn Written
Spec/amendment; chỉ viết Implementation Plan và Review Contract sau khi Written
Spec được User duyệt. Không tiếp tục Phase 6 trước các gate này.
