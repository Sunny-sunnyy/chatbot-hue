# Implementation Report: nhãn đoạn đúng bản 3 (gold v3 = v2 + 2 câu nhóm kiểm) — B75

Người làm: B (Claude Opus 5.5, terminal `hue-rag-2d`) · 15:06 27/10/2026 (`date`) · Việc: `session_prompt/CURRENT_HANDOFF.md` → B75 (User đồng ý 15:01, A giao).
Trạng thái: **chờ review** (C). Không commit (A commit). **0 USD.** File này không chép câu hỏi, đáp án hay nội dung kho — chỉ `case_index`, loại câu, số đếm.

## 1. Phạm vi

Dựng `gold_v3.jsonl` từ `gold_v2.jsonl` + đề xuất C64 mục 3 (đã review B74), riêng câu 138 theo B74 m-1; đổi `GOLD_PATH` mặc định sang v3; sửa test; đếm lại.
**Không đổi** `gold_v2.jsonl`, `gold_draft.jsonl`; không đổi chatbot (`GOLD_PATH` chỉ dùng trong harness thí nghiệm).

## 2. Thay đổi chính

| File | Thay đổi | Tracked? |
|---|---|---|
| `backend/experiments/phase_8_1/g1_retrieval.py:44-47` | `GOLD_PATH` → `gold_v3.jsonl`; comment ghi v1 / v2 giữ nguyên + sha | có |
| `backend/tests/test_gold_coverage.py` | docstring (v2 trở đi + luật "một trích dẫn bất kỳ"); **+1 test** `gold_coverage`: fact phủ khi một trích dẫn bất kỳ trúng, `all` cần mọi fact (chuỗi tự viết) — nhãn 138 v3 dựa vào luật này | có |
| `data/phase_8_1/tools/build_gold_v3.py` (sha `7983388a9e08`) | dựng + kiểm (cùng cách `build_gold_v2.py`), từ chối ghi đè, in sha v2 / v1 trước–sau | private |
| `data/phase_8_1/gold/gold_v3.jsonl` (sha `3b1117cf59e9`) + `gold_v3_CHANGES.md` | nhãn bản 3 + ghi thay đổi | private |
| `data/phase_8_1/gold/v3_check/recount_v3.py` + `.json` | đếm lại v2 / v3 trên B1, K3b-m (dev + test) | private |

Câu đổi (cả hai ở nhóm test): **130** (nhiều nguồn) +1 khoảng cho một fact; **138** (so sánh) fact so sánh chỉ gắn trích dẫn nói thẳng ý so sánh (khác đề xuất C64 —
C64 gắn cả 4); **95** (so sánh) giữ. Chi tiết private: `gold_v3_CHANGES.md`.

**Ảnh hưởng ngoài file sửa** (sửa chữ theo review C m-2, 15:10 27/10/2026): trên `main`, `GOLD_PATH` được import bởi `experiments/phase_8_1/g2_generate.py:47`,
`g3_chunking.py:50`, `g4_keyword.py:26`, `g4_rerank.py:41` (`r4_numbers.py` chỉ dùng bộ câu Golden, không dùng nhãn). Trên hai nhánh hồ sơ `p82-k3`, `p82-k3b`, ngoài
các file trên còn `experiments/phase_8_2/b1.py`, `k3.py`, `k3b.py`, `k3b_answer.py` (`git grep`). Chạy lại bất kỳ harness nào sau khi commit (hoặc sau khi
rebase nhánh hồ sơ lên `main`) sẽ đếm theo v3 (như lần đổi v2, C61 m-1). Số `*_gold_*` cũ: trước 27/10 là v1, 27/10 (sau `a819789`) là v2.

## 3. Cách đã chạy thật

```bash
uv run python -I data/phase_8_1/tools/build_gold_v3.py                       # gốc repo
cd backend && HF_HUB_OFFLINE=1 uv run python -m pytest tests/test_gold_coverage.py -q
HF_HUB_OFFLINE=1 uv run python -I ../data/phase_8_1/gold/v3_check/recount_v3.py   # Qdrant :6335 chỉ đọc (scroll payload)
```

## 4. Kết quả quan sát (lần chạy mới, 15:0x 27/10)

| Kiểm | Kết quả |
|---|---|
| build: số câu / câu đổi / lỗi kiểm | 55 / **[130, 138]** / **0**; không câu nào đổi tập trường |
| so v2 ↔ v3 từng trường | 130: evidence +1, fact 0 `[0]` → `[0, 2]`; 138: evidence không đổi, fact 2 `[0, 1]` → `[3]`; trường khác giống |
| sha `gold_v2.jsonl` / `gold_draft.jsonl` trước → sau | `2f5a347a71ff` → `2f5a347a71ff`; `bab707b9ab22` → `bab707b9ab22` |
| `test_gold_coverage.py` | **3 passed** (lượt đầu test mới fail vì trích dẫn "không trúng" cùng file nên rơi vào nhánh đọc file tiêu đề — đổi sang file khác; lỗi ở test, không ở code) |
| `git diff --check -- backend/` | sạch |

`context_gold_all` theo `GOLD_PATH` mặc định (v3) so với v2 (`recount_v3.json`):

| Lượt | Nhóm | n | v2 | v3 | đổi |
|---|---|---:|---:|---:|---|
| B1 (context 10) `b1/b1_test.jsonl` | test | 15 | 7 | **9** | 130, 138 |
| K3b-m `k3b/m_test.jsonl` | test | 15 | 10 | **11** | 138 |
| B1 `b1/b1_dev.jsonl` | dev | 40 | 24 | 24 | — |
| K3b-m `k3b/m_l1.merged.jsonl` | dev | 40 | 33 | 33 | — |

Context B1 **dựng lại** từ `top_chunk_ids[:context_sources]` (file `b1_*.jsonl` không lưu `context_chunk_ids`); K3b-m đọc `context_chunk_ids`
có sẵn. C đếm B1 bằng `k3/base_test.jsonl` (có `context_chunk_ids`) ra cùng số; B74 đã thấy hai nguồn giống nhau 15 / 15 câu test (sửa chữ theo review C m-1).
Khớp kỳ vọng mục việc (9 / 11 trên 15) và số v2 đã ghi (B1 dev 24, K3b-m 33).

## 5. Lỗi và giới hạn

- Không chạy full suite; `test_gold_coverage.py` không đọc file nhãn thật (cố ý: clone public không có `data/`).
- Không chạy lại thí nghiệm nào; kết luận đã đóng (K3b-m gác) không đổi — test chỉ là "không làm hỏng".
- Thử ngược test mới **trong bộ nhớ** (không sửa file): thay `gold_coverage` bằng hai bản sai (`all` chỉ cần một fact; fact cần mọi trích dẫn) ⇒ test **fail**
  cả hai ⇒ test bắt đúng.

## 6. Bàn giao cho người kiểm

- Diff tracked: 2 file `backend/`. Chạy lại rẻ nhất: `build_gold_v3.py` trên bản sao (từ chối ghi đè ⇒ đổi tên `out` tạm), `recount_v3.py`, pytest 1 file.
- Kiểm: câu 138 v3 khác đề xuất C64 đúng ở fact 2 (theo B74 m-1); sha v2 / v1 không đổi.
