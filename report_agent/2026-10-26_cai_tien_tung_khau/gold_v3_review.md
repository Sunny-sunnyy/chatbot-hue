# Review: nhãn đoạn đúng bản 3 (gold v3) — B75

Decision: **ready_for_user_confirmation** (0 blocker / 0 major / 2 minor)
Người kiểm: C (Claude Opus 5.5, `hue-rag-86`) · 15:09 27/10/2026 (`date`)
Implementation report: `report_agent/2026-10-26_cai_tien_tung_khau/gold_v3_implementation.md` (B, 15:06). 0 USD. File này không chép câu hỏi, đáp án hay nội dung kho.
**Lưu ý độc lập:** C là người viết đề xuất gốc (C64 mục 3); việc kiểm ở đây là B áp đúng đề xuất + quyết định B74 m-1 hay không, không phải chấm lại đề xuất của chính C.

## 1. Phạm vi đã review

- Diff tracked (working tree chung, `main`, chưa commit): `backend/experiments/phase_8_1/g1_retrieval.py` (`GOLD_PATH` → v3 + comment), `backend/tests/test_gold_coverage.py`
  (docstring + 1 test). Đọc đủ. `git diff --check -- backend/` sạch.
- Private: `data/phase_8_1/gold/gold_v3.jsonl` (sha tính lại `3b1117cf59e9` = report), `data/phase_8_1/tools/build_gold_v3.py` (`7983388a9e08` = report; đọc đầu file: dựng
  từ v2 + `proposal_test_c64.jsonl`, câu 138 đặt fact 2 = `[3]` có assert nội dung, kiểm offset như `validate_gold.py`, từ chối ghi đè), `v3_check/recount_v3.py`.

## 2. Findings

Không có blocker hoặc major.

### m-1 — report ghi đếm B1 "từ `b1/b1_test.jsonl`", nhưng file đó không lưu context

- **Vị trí:** report §4 bảng (dòng B1); `recount_v3.py:11-14`.
- **Bằng chứng:** `b1_test.jsonl` / `b1_dev.jsonl` không có `context_chunk_ids` (chỉ `top_chunk_ids`, `context_sources`); script dựng lại context bằng `top_chunk_ids[:context_sources]`
  (giả định context = N đoạn đầu theo hạng). C đếm bằng `context_chunk_ids` **đã lưu** của cùng mốc B1 (`data/phase_8_2/k3/base_test.jsonl`, `base_dev.jsonl`) ⇒ ra **cùng số**
  (test 7 → 9, dev 24 → 24) ⇒ giả định đúng ở đây.
- **Tiêu chí đóng:** một câu trong report (hoặc docstring script) nói context B1 được dựng lại từ `top_chunk_ids`; lần sau dùng file có `context_chunk_ids`.

### m-2 — danh sách "ảnh hưởng ngoài file sửa" thiếu hai chỗ đọc `GOLD_PATH`

- **Vị trí:** report §2 "Ảnh hưởng ngoài file sửa" (nêu `g2_generate.py:47`, `g4_keyword.py:26`).
- **Bằng chứng:** `grep GOLD_PATH backend`: còn `experiments/phase_8_1/g4_rerank.py:41`, `g3_chunking.py:50`; trên nhánh hồ sơ (không merge) `p82-k3` / `p82-k3b`
  `experiments/phase_8_2/k3.py:57, :76`, `k3b.py:126` — chạy lại các nhánh đó sau khi commit cũng đếm theo v3.
- **Tiêu chí đóng:** bổ sung vào câu ảnh hưởng (hoặc ghi "mọi harness import `g1_retrieval.GOLD_PATH`"). Không cần sửa code.

Quan sát (không phải finding): câu 138 v3 gắn fact so sánh chỉ `[3]` (trích dẫn nói thẳng ý so sánh), khác đề xuất C64 `[0, 1, 2, 3]` — đúng quyết định B74 m-1, User đồng ý
(qua A). Ý C: `[3]` chặt và đúng nghĩa hơn; đánh đổi: context có đủ hai số liệu (trích dẫn 0 + 1) mà thiếu trích dẫn 3 sẽ bị tính thiếu ý so sánh — chấp nhận được vì
fact 0 / 1 đã đo riêng hai số.

## 3. Cách người kiểm chạy lại thật

0 USD, chỉ đọc (Qdrant :6335 scroll payload). Script tạm của C chạy từ `backend/` (`PYTHONPATH=. HF_HUB_OFFLINE=1 uv run python -`): so v2 ↔ v3 từng dòng; kiểm offset mọi
trích dẫn v3; đếm `context_gold_all` v2 / v3 bằng `g1.gold_coverage` + `context_chunk_ids` đã lưu. `sha256sum` 4 file. `pytest tests/test_gold_coverage.py`.

## 4. Kết quả quan sát (lần chạy mới, 15:09 27/10/2026)

| Kiểm | Kết quả | Khớp report |
|---|---|---|
| sha v3 / v2 / v1 / build script | `3b1117cf59e9` / `2f5a347a71ff` / `bab707b9ab22` / `7983388a9e08` — v2, v1 không đổi | ✓ |
| v2 ↔ v3 | 55 / 55 câu, cùng tập câu; khác đúng **2** câu (130, 138) | ✓ |
| câu 130 | thêm 1 trích dẫn ở cuối (trích dẫn cũ giữ nguyên thứ tự), fact 0 `[0]` → `[0, 2]`, chữ fact không đổi; khoảng mới = đúng khoảng C64 đề xuất | ✓ |
| câu 138 | trích dẫn không đổi; fact 2 `[0, 1]` → `[3]`; fact 0 / 1 giữ | ✓ |
| offset mọi trích dẫn v3 | 0 lỗi (đúng 1 lần, start / end đúng) | ✓ |
| `context_gold_all` B1 test (15) | v2 7 → v3 **9** (130, 138) | ✓ |
| K3b-m test (15) | 10 → **11** (138) | ✓ |
| B1 dev / K3b-m dev (40) | 24 → 24 / 33 → 33 | ✓ |
| `test_gold_coverage.py` | 3 passed | ✓ |

Không chạy lại thử ngược test mới (dùng lại bằng chứng của B, report §5 — thay hàm bằng hai bản sai trong bộ nhớ ⇒ fail cả hai). Đọc test: trích dẫn "khác file" trả
`False` ngay ở `chunk_hits_quote` (không đọc file) ⇒ test không cần kho.

## 5. Giới hạn hoặc phần chưa chạy

- Không chạy full suite, không chạy lại thí nghiệm nào (đúng phạm vi: nhãn chỉ dùng trong harness, chatbot không đổi).

## 6. Decision và bước tiếp theo

`ready_for_user_confirmation`: A commit 2 file tracked + báo User; số `*_gold_*` từ commit này là v3 (trước: v1 tới `a819789`, v2 tới commit này). Hai minor sửa chữ
trong report khi tiện, không cần vòng review riêng.
