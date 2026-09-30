# Báo cáo Triển khai Phase 5 — Full-corpus Retrieval, RRF và Reranking (Bao gồm Correction 1, 2 & 3)

```text
Date: 2026-09-14 +07
Role: Implementer
Status: completed (Correction 3 incorporated)
Risk level: high
Git authorization: none
Sub-agent authorization: standing authorization (executed directly by lead implementer)
```

## 1. Phạm vi và thẩm quyền (Authority & Scope)

- **Phê duyệt triển khai:** User đã phê duyệt Full-corpus Phase 5 Written Spec, Implementation Plan và Review Contract ngày 2026-09-13.
- **Review findings:**
  - Initial review: P5-R1..P5-R4 (Correction 1 đã xử lý).
  - Correction 1 review: P5-C1-R1, P5-C1-R2, P5-C1-R3 (Correction 2 đã xử lý).
  - Correction 2 review: P5-C2-R1 (Major - non-string role gây TypeError), P5-C2-R2 (Minor - wording inventory & evidence reuse) tại [Codex Review](file:///home/minhhieu/hue_rag/reports/full_corpus_phase_5_retrieval_reranking_codex_review_2026_09_13.md).
- **Base commit:** `41b638642caf432fc7484d08444ba609a0368708`
- **Head commit:** `HEAD` (worktree)
- **Quyền Git:** `none`. Không commit, push, stage, unstage, reset hay dọn dẹp worktree.
- **Bảo toàn ranh giới và ownership:**
  - Tuyệt đối không sửa các tệp Reviewer/User-owned: [`session_prompt/Project_Status.md`](file:///home/minhhieu/hue_rag/session_prompt/Project_Status.md), Written Spec, Implementation Plan, canonical guide hay review reports.
  - Không sửa `full_corpus_smoke.py` và `cross_encoder.py` trong Correction 3 theo đúng ranh giới được giao.
  - Giữ nguyên dirty worktree từ trước: `.gitignore` staged, 264 tệp cached removals dưới `knowledge-base-hue/` staged, `PROJECT_DOCUMENT_REGISTRY.md` untracked.

---

## 2. Các thay đổi chính (Changed Paths & Responsibilities)

| Đường dẫn | Thao tác | Trách nhiệm |
|---|---|---|
| [`backend/retrieval/full_corpus.py`](file:///home/minhhieu/hue_rag/backend/retrieval/full_corpus.py) | Cập nhật C3 | **P5-C2-R1:** Thêm type guard `isinstance(role, str)` trước khi kiểm tra `role not in ALLOWED_EVIDENCE_ROLES`. Đảm bảo các giá trị `role` không phải chuỗi (kể cả mảng JSON `[]`, đối tượng `{}` không hash được) đều fail closed với `RetrievalDependencyError`, không gây raw `TypeError: unhashable type`. Dùng chung trực tiếp cho dense và sparse. |
| [`backend/tests/test_full_corpus_retrieval.py`](file:///home/minhhieu/hue_rag/backend/tests/test_full_corpus_retrieval.py) | Cập nhật C3 | Bổ sung pure probes trong `test_validate_point_payload_nested_evidence_parts_fail_closed` kiểm tra các giá trị non-string role (`[]`, `{}`, `123`, `True`, `False`, `None`) đều ném `RetrievalDependencyError` thay vì `TypeError`. |
| [`reports/full_corpus_phase_5_retrieval_reranking_implementation_2026_09_13.md`](file:///home/minhhieu/hue_rag/reports/full_corpus_phase_5_retrieval_reranking_implementation_2026_09_13.md) | Cập nhật C3 | **P5-C2-R2:** Cập nhật báo cáo triển khai: đính chính số lượng 5 paths tại C2 inventory, đính chính số liệu evidence reuse sang `1007.95–1331.49 ms`, và ghi nhận kết quả Correction 3. |
| [`session_prompt/CURRENT_HANDOFF.md`](file:///home/minhhieu/hue_rag/session_prompt/CURRENT_HANDOFF.md) | Cập nhật C3 | Đóng gói handoff `final_review` chuyển tiếp về Reviewer. |

---

## 3. Cách thức đã chạy và xác minh (Verification Executed)

### 3.1. Kiểm tra định dạng mã nguồn
```bash
git diff --check
```
- **Kết quả:** Thoát mã 0, sạch 100%, không có lỗi định dạng hay khoảng trắng thừa.

### 3.2. Regression & Focused Unit Tests
```bash
UV_CACHE_DIR=/tmp/hue-rag-phase5-review-uv-cache uv run --env-file .env python -m pytest backend/tests/test_full_corpus_retrieval.py backend/tests/test_retrieval_service.py -q --tb=short
```
- **Kết quả:** **23 passed, 1 warning in 62.69s**
  - [`backend/tests/test_full_corpus_retrieval.py`](file:///home/minhhieu/hue_rag/backend/tests/test_full_corpus_retrieval.py): **15 passed** (toàn bộ các nhánh kiểm tra type guard, privacy allowlist, RRF và BM25/sparse đều đạt).
  - [`backend/tests/test_retrieval_service.py`](file:///home/minhhieu/hue_rag/backend/tests/test_retrieval_service.py): **8 passed** (Foods baseline regression đạt 100%).

---

## 4. Kết quả quan sát đối chiếu tiêu chí nghiệm thu Correction 3

### P5-C2-R1 — Non-string role typed fail-closed
- Code kiểm tra trực tiếp:
  ```python
  role = part["role"]
  if not isinstance(role, str) or role not in ALLOWED_EVIDENCE_ROLES:
      raise RetrievalDependencyError(
          f"Point {point_id} evidence_parts[{idx}] invalid role: {role!r}. Allowed: {sorted(ALLOWED_EVIDENCE_ROLES)}"
      )
  ```
- Nhờ cơ chế short-circuit của Python (`or`), khi `role` không phải `str` (như `role=[]` hoặc `role={}`), điều kiện `not isinstance(role, str)` trả về `True` ngay lập tức, ngăn chặn việc thực thi membership test trên `frozenset` vốn đòi hỏi object phải hashable.
- Do đó, mọi non-string role đều ném đúng typed `RetrievalDependencyError`, loại bỏ hoàn toàn raw `TypeError`.
- Unit tests đã bao phủ: `[]`, `{}`, `123`, `True`, `False`, `None` và invalid string `"INVALID"`.

### P5-C2-R2 — Inventory & Evidence Wording Correction
- Đính chính mục P5-C1-R3: Lượt Correction 2 đã sửa đổi chính xác 5 tệp (`backend/retrieval/full_corpus.py`, `backend/retrieval/full_corpus_smoke.py`, `backend/tests/test_full_corpus_retrieval.py`, báo cáo triển khai và `CURRENT_HANDOFF.md`).
- Trong lượt Correction 3 này, chỉ có đúng 4 tệp được sửa đổi (`full_corpus.py`, `test_full_corpus_retrieval.py`, báo cáo này và `CURRENT_HANDOFF.md`).
- Đính chính mục Evidence Reused: Bằng chứng độc lập từ Correction 1 ghi nhận MiniLM warm end-to-end p95 đạt `1007.95–1331.49 ms` (thay vì ghi nhầm `1.007–1.893 ms`).

---

## 5. Bằng chứng được tái sử dụng (Evidence Reused)

Theo hợp đồng bàn giao:
- Thử nghiệm âm tính selector (`--treatment typo`) và unsafe destination (`backend/trace.json`) từ Correction 1: Đều chặn trước thực thi và trả mã lỗi 1.
- MiniLM warm end-to-end p95 độc lập từ Correction 1: `1007.95–1331.49 ms` (đều <= ngưỡng 3.000 ms).
- Lượt chạy live ma trận đọc ngoài sandbox từ Correction 2: 4 candidates × 2 treatments × `reranker=none` × `P5-Q01` đạt `8/8 PASS`, tính xác định `8/8 = True`, anomaly `0`.
- Privacy behavior của failure trace P5-C1-R1 đã đóng hoàn toàn và được tái sử dụng. Không cần chạy lại ma trận live khi chỉ áp dụng type-guard cục bộ cho `role`.

---

## 6. Lỗi, giới hạn và bàn giao Reviewer

1. **Lỗi quan sát:** `0` (Không có lỗi trong toàn bộ test suite).
2. **Hạn chế kỹ thuật:**
   - Chất lượng truy xuất và so sánh benchmark mô hình tiếp tục được bảo lưu sang Phase 8.
   - Bốn collection canonical trên Qdrant và Foods collection tiếp tục giữ trạng thái read-only.
3. **Chuyển giao cho Reviewer:**
   - Trạng thái mã nguồn đã sẵn sàng cho independent final review.
   - Đã cập nhật [`session_prompt/CURRENT_HANDOFF.md`](file:///home/minhhieu/hue_rag/session_prompt/CURRENT_HANDOFF.md) sang `handoff_kind: final_review`, `target_role: reviewer`.
