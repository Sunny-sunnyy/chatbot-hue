# Codex Review: Phase 8 Golden Dataset V3 — Correction Round 2

Decision: `ready_for_user_confirmation`
Reviewer: Codex
Date: `2026-08-28 +07`
Proposed final size: `45`
User confirmation: `approved`
User confirmation date: `2026-08-28 +07`
Gate 0 lifecycle: `approved`
Implementation report: `reports/phase_8_golden_dataset_v3_implementation_report.md`

## 1. Findings

Không còn blocker hoặc major finding.

Các finding của vòng trước đã được đóng:

- food tour nửa ngày được khôi phục với keywords cấp intent đã được User xác
  nhận; case địa chỉ Bánh canh O Hoa được loại để giữ đúng 45;
- các mismatch tại Cơm Âm Phủ, Hải Triều, Thanh Liễu, DeChill, The TIME và hai
  spanning questions đã được sửa theo declared Markdown;
- evidence mappings đã được thu hẹp từ `97` references xuống `80`, không làm
  mất claim cần bảo vệ;
- implementation report đã ghi web research boundary, URL/query, exact test
  outcomes và per-smoke retrieval observations.

Không tạo finding cho việc các spanning cases `0039`–`0041` dùng hai sections
trên mỗi source: `Tóm tắt` bảo vệ nhận diện/đặc tính của quán hoặc thương hiệu,
còn `Thông tin` bảo vệ địa chỉ; đây là synthesis tự nhiên, không phải quota.

Ghi chú không chặn: reference answer `foods-v3-0044` lặp từ “buổi sáng” trong
cụm mở đầu, nhưng answer vẫn rõ, trực tiếp và không gây nhập nhằng ground truth.
Không cần mở thêm correction chỉ cho chỉnh sửa văn phong này.

## 2. Manual review coverage

- Đọc đủ `45/45` rows: question, category, keywords, reference answer và
  evidence mapping.
- Mở và đọc đủ `80/80` declared case/source/section references, tương ứng `70`
  unique H2 sections trong `39` Markdown files.
- Kiểm tra toàn tập về tourist likelihood, tiếng Việt tự nhiên, standalone
  intent, semantic duplicate, repeated template, price/time-only prohibition,
  keyword quality và category.
- Kiểm tra mọi answer claim với declared H2; web không được dùng làm Golden
  evidence.
- Xác nhận 45 là mức cao nhất defensible trong `50 -> 45 -> 40`: năm case yếu
  hoặc trùng của draft 50 đã được loại/thay, trong khi 45 case còn lại đều có
  intent thực dụng và evidence trực tiếp. Không có lý do chất lượng để hạ xuống
  40.
- Xác nhận full có 45 IDs tuần tự; smoke có đúng 10 unique rows deep-equal.
- Xác nhận V2/Phase 7 evaluation datasets không có worktree diff.
- Đọc validator/tests và relevant diff; không thấy quota, semantic judge,
  abstraction hoặc fake/mock completion evidence mới.

## 3. Fresh verification độc lập

Chạy từ `backend/`:

```bash
UV_CACHE_DIR=/tmp/hue-rag-golden-v3-review-r3-uv-cache \
  uv run --env-file ../.env python -m pytest tests/test_evaluation.py \
  -q --tb=short -k 'golden_v3 and not binary_relevance'

UV_CACHE_DIR=/tmp/hue-rag-golden-v3-review-r3-uv-cache \
  uv run --env-file ../.env python -m pytest tests/test_evaluation.py \
  -q --tb=short -k 'golden_v2_contract or golden_v2_smoke'

HF_HUB_OFFLINE=1 UV_CACHE_DIR=/tmp/hue-rag-golden-v3-review-r3-uv-cache \
  uv run --env-file ../.env python -m pytest \
  tests/test_evaluation.py::test_golden_v3_binary_relevance_uses_real_retrieval_metadata \
  -q --tb=short -s
```

Reviewer còn chạy một audit độc lập qua real ingestion/retrieval path trên
exact isolated target `hue_rag_live_test_golden_v3_review_r3`, in exact
relevant ranks và returned `source :: section` cho từng smoke case, rồi xóa
target trong `finally`.

## 4. Kết quả quan sát

| Kiểm tra | Fresh outcome |
|---|---|
| V3 deterministic | `5 passed, 13 deselected, 1 warning in 3.97s` |
| V2 regression | `2 passed, 16 deselected, 1 warning in 3.99s` |
| Canonical live metadata test | `1 passed, 2 warnings in 36.02s`; cleanup `ok` |
| Validator summaries | full `45`; smoke `10`; counts khớp implementation report |
| Smoke exact hits | `10/10`; first ranks `1,1,1,2,2,1,1,1,2,1` |
| Isolated audit | ingest đủ `572` points; target tồn tại `False` sau cleanup |
| Active collection | green; `points_count 572 -> 572` |
| Collections sau audit | chỉ còn `hue_foods_e5_small_384` và `_dense` |
| `git diff --check` | PASS |
| Manual content/evidence audit | PASS, không còn blocker/major |

Không chạy paid generation/judge, Phase 8 benchmark hoặc active mutation.

## 5. Decision và lifecycle

Technical decision: `ready_for_user_confirmation`.

User đã xác nhận nội dung và kích thước `45` câu ngày `2026-08-28 +07`.
Golden Dataset V3 cùng smoke subset 10 câu vì vậy hoàn tất và được phê duyệt ở
Gate 0. Bước tiếp theo là brainstorming Gate 1 dựa trên distribution cuối này.

Approval Gate 0 không authorize code benchmark, model download, paid
generation/judging, Qdrant mutation hoặc production cutover. Phase 8 tổng thể
vẫn `not_ready` cho tới khi các experiment contract còn mở được brainstorm,
thiết kế/plan tương ứng được user duyệt và exact experiment group được authorize.

Không commit hoặc push.
