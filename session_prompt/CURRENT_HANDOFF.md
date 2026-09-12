# Bàn giao hiện hành — Phase 3 / Full-corpus Wave 2.1 Design Gate

Target role: reviewer
Authored by: reviewer
Handoff kind: next_design
State: active
Base commit: d631d3cc47a66d7a43c71f36c585d73ae9d21f9e
Head commit: closure commit on origin/main; verify at session start
Risk level: medium
Git authorization: none
Sub-agent authorization: none

## Closed dependency

Full-corpus RAG Wave 1 được User xác nhận closure ngày 2026-09-12. Final review:
`reports/full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`.
Observed offline result: `PASS`, 205 sorted/unique files, 8460 chunks, ba
condition rules, zero errors/oversized; max token `366/512`, `366/512`,
`255/256`. Implementer báo 39 tests pass và repeated preview byte-identical;
Reviewer không rerun dynamic checks. Wave 1 chưa embedding hoặc Qdrant mutation.

## Objective

Bắt đầu design gate Phase 3/Full-corpus Wave 2.1 từ evidence thật của Wave 1.
Reviewer phải xác định các quyết định embedding/sparse representation còn mở,
brainstorm với User **mỗi lượt một quyết định**, rồi cập nhật detailed Phase 3
guide và soạn exact Wave 2.1 spec/addendum, implementation plan cùng Review
Contract. Trình User duyệt trọn design package trước khi tạo Implementer handoff.

Không bắt đầu implementation, không giao Implementer Wave 2.1 trong session
bootstrap và không author ahead nội dung phụ thuộc như đã có live result.

## Active design inputs

### Full-read

- Full-corpus umbrella/status/observed Wave 1:
  `guides/full_corpus_rag.md`
- Detailed Phase 3 guide, gồm Foods as-built history và extension gate:
  `guides/phase_3_embedding_sparse_representation.md`
- Final Wave 1 technical review và limitations:
  `reports/full_corpus_rag_wave_1_correction_3_codex_review_2026_09_12.md`

Nếu output của bất kỳ file `full-read` nào bị truncate, tiếp tục từ dòng dừng tới
EOF.

### Targeted-read

- `docs/superpowers/specs/2026-09-11-full-corpus-rag-written-spec.md`: exact
  embedding, Representation A/B, payload và Wave 2.1 dependency requirements;
- `docs/superpowers/plans/2026-09-11-full-corpus-rag-implementation-plan.md`:
  design-gate workflow và exact Wave 2.1/Phase 3 roadmap sections;
- `handoff_prompt/FULL_CORPUS_RAG_IMPLEMENTATION_REVIEW_CONTRACT.md`: Wave 2
  static/code review requirements và authority boundaries;
- canonical preview artifact chỉ các totals/tokenizer limits cần làm Wave 2.1
  dependency evidence.

### Reference-only

Correction prompts/reports cũ, production Foods code/data history, full corpus
source text, `.env`, logs, caches, Qdrant state, notebooks và mọi Wave 2.2+ nội
dung chưa cần cho quyết định đang hỏi.

## Design boundaries

- Foods runtime/collections giữ read-only; Wave 1 không cutover chúng.
- Không chạy tests, model/API, embedding inference, Qdrant, frontend, notebook
  hoặc benchmark trong design gate.
- Không tạo collection/point/build record, không paid call và không Git write.
- E5-small, E5-base và HuyDang là approved dense candidates; exact local model
  readiness/dimensions/preprocessing phải được Wave 2.1 plan kiểm bằng evidence,
  không suy từ tên model.
- Representation B chỉ thuộc staged finalists sau này, không triển khai trong
  Wave 2.1 nếu exact new approval chưa cho phép.
- Giữ chuỗi Wave 2.1 → Wave 2.2 → Wave 2.3; không gộp embedding, live indexing và
  retrieval chỉ để giảm số gate.

## Required design outputs trước Implementer handoff

1. danh sách quyết định còn mở, hỏi User từng quyết định một;
2. detailed Phase 3 guide cập nhật với target behavior, exclusions, evidence và
   trạng thái `proposed`/`ready` đúng lifecycle;
3. exact Wave 2.1 spec/addendum;
4. exact Wave 2.1 implementation plan;
5. exact Wave 2.1 Review Contract;
6. một lần trình User duyệt toàn bộ package; chỉ sau approval mới tạo Implementer
   handoff Wave 2.1.

## Next action duy nhất

Reviewer nạp context theo bốn file bootstrap chuẩn, kiểm cấu trúc thư mục, rồi
đọc ba full-read inputs trên. Sau đó tóm tắt dependency Wave 1 và hỏi User **một
quyết định thiết kế Phase 3 đầu tiên**; chưa sửa guide/spec/plan trước khi
brainstorm đủ các quyết định cần thiết và chưa giao Implementer.
