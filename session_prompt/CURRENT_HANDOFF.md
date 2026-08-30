# Bàn giao hiện hành

Target role: reviewer
Authored by: reviewer
Handoff kind: next_design
State: ready
Base commit: worktree
Head commit: worktree
Risk level: high
Git authorization: none
Sub-agent authorization: none

---

## 1. Closed lifecycle

User đã xác nhận Phase 8 Notebook 08c ngày `2026-08-30 +07`.

- 08c status: `approved`.
- 60 summary rows/135 cases reconcile complete.
- Cả ba MiniLM pairings `eligible=False`; không reranker finalist/cutover.
- Production, active Qdrant, Golden/corpus và runtime giữ nguyên.
- Phase 8 tổng thể vẫn `not_ready`.

Canonical closure evidence:

```text
reports/phase_8_08c_reranker_benchmark_codex_review.md
reports/user_reports/phase_8_08c_reranker_benchmark_user_report.md
```

User đã authorize một lần commit/push work package 08c và closure; Reviewer thực
hiện quyền đó trước khi bàn giao này có hiệu lực. Quyền Git cho workstream kế
tiếp trở về `none`.

## 2. Next-design objective

Research và thiết kế exact workstream để hoàn thiện curated answer-facing data
cho mọi domain phù hợp dưới:

```text
/home/minhhieu/hue_rag/knowledge-base-hue
```

Observed structure hiện có:

- `foods/` là domain duy nhất có coverage chi tiết theo entity cùng Golden data;
- `festivals/`, `heritage/`, `performing_arts/`, `tourism/`, `tickets/` và
  `statistics/` mới có một số guide tổng hợp hoặc nhiều subdirectory rỗng;
- `services/` hiện có các category directories nhưng chưa có answer-facing files;
- `_source-dumps/` là raw/reference material, không tự động thành retrievable
  content;
- `meta/` là governance/source tracking, không phải answer corpus.

## 3. Reviewer design tasks

Trước mọi corpus edit, Reviewer phải:

1. inventory coverage/content quality theo domain, entity type và user intent;
2. phân loại file nào là curated answer-facing, raw source, governance hoặc
   duplicate/stale content;
3. xác định domain taxonomy và minimum content contract dùng chung nhưng không
   ép mọi domain vào Foods template;
4. research authoritative sources chỉ khi cần lấp evidence gaps, lưu provenance
   và không copy raw web content thẳng vào corpus;
5. đề xuất staged curation/review scope cho Festivals, Heritage, Tourism,
   Performing Arts, Services, Tickets, Statistics và domain hợp lệ khác;
6. thiết kế riêng các bước sau corpus: domain-aware chunking/metadata, fresh
   embeddings, isolated full-corpus index và Combined Golden Dataset có quota
   overall/per-domain;
7. xác định phần Phase 7/8 phải rerun sau khi corpus contract thay đổi.

Reviewer trình design/spec và implementation plan để user duyệt trước khi giao
Implementer.

## 4. Current boundaries

Chưa authorize:

- sửa/tạo/xóa corpus hoặc source dumps;
- thay chunker/runtime/dependencies;
- tạo embeddings/index/Golden Dataset;
- start/mutate Qdrant;
- chạy paid API hoặc multi-domain benchmark;
- production cutover;
- commit/push hoặc spawn sub-agent.

Foods 07/08 results chỉ được dùng làm historical Foods evidence, không đại diện
cho full Hue corpus.

## 5. Next action

Reviewer bắt đầu bằng read-only inventory và research/brainstorming, sau đó trình
cho user một design đề xuất rõ domain coverage, quality gates, provenance,
staging và verification. Không bắt đầu implementation trong handoff này.
