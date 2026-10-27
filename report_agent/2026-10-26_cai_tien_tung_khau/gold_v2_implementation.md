# Implementation Report: nhãn đoạn đúng bản 2 (gold v2) + đếm cả tiêu đề mục

Người làm: B (Claude Opus 5.5, terminal `hue-rag-31`) · 2026-10-27 13:10 +0700 (`date`) · Việc: **B69** (A giao 27/10). 0 USD.
User duyệt sửa nhãn C56 + đếm tiêu đề mục: A báo, B nhận tin lúc 13:06:30 27/10/2026 (`date`).
Code: nhánh `gold-v2` = `main` `e452e27` + `3f2099f`. A ghi "từ `2ddd65d`"; `main` đã sang `e452e27` (governance của A, đã gồm `2ddd65d`), nên B lấy
`main` mới nhất. Không đụng `api/`, `llm/` (việc C59 / C60).
Trạng thái: **chờ review** (C).

Report public tả câu ở mức loại câu (W26), không nêu chủ đề hay tên file.

## Cho bạn — lời thường

1. Thước "đoạn đúng" đếm thiếu ở 3 câu thử: kho nói lại cùng thông tin ở chỗ khác, hoặc thông tin nằm ở tiêu đề mục. Bạn đã duyệt sửa.
2. Mình làm hai việc:
   - **bản nhãn mới** (thêm 3 chỗ cho 2 câu); bản nhãn cũ giữ nguyên, vì các kết quả trước đã khóa theo nó;
   - **đếm cả tiêu đề mục**, khi model thấy tiêu đề đó trong đoạn được đưa vào.
3. Tính lại bằng thước mới:
   - chatbot hiện tại: 22 → **24 / 40** câu thử có đủ đoạn đúng;
   - cách "luna chọn 10 đoạn": 31 → **33 / 40**;
   - kết luận cũ không đổi: luna vẫn cứu 9 câu, không làm mất câu nào. Nhóm kiểm không đổi.
4. Không tốn tiền.

## 1. Phạm vi

1. **Nhãn:** tạo `data/phase_8_1/gold/gold_v2.jsonl` = bản cũ + 3 khoảng C56. Ghi `gold_v2_CHANGES.md`. Kiểm nhãn mới.
   **Không ghi đè** `gold_draft.jsonl` (sha `bab707b9ab22`, manifest G0.6 khóa).
2. **Code:** `backend/experiments/phase_8_1/g1_retrieval.py`:
   - `GOLD_PATH` trỏ v2;
   - `chunk_hits_quote` trúng thêm khi trích dẫn là dòng tiêu đề nằm trong `heading_path` của chunk cùng file;
   - 2 test nhỏ.
3. **Kiểm:** tính lại `context_gold_all` / `top10_gold_all` của mốc B1 và K3b-m bằng hàm mới. A ghi kỳ vọng: B1 24, K3b-m 32 hoặc 33.

## 2. Thay đổi

**Dữ liệu (private, không vào git):**
- `gold_v2.jsonl` sha `2f5a347a71ff`: 55 câu.
  - **2 câu đổi:** 1 câu `direct_fact` (+2 khoảng) và 1 câu `comparative` (+1 khoảng).
  - Chỉ **thêm** khoảng và `quote_ids`. B kiểm: evidence cũ là tiền tố của evidence mới, chữ fact giữ nguyên, `quote_ids` cũ ⊂ mới, các trường khác giữ nguyên.
  - Nguồn: `data/phase_8_2/gold_fix_proposal_2710/proposal.jsonl` (C56), bỏ trường `proposal`.
- `gold_v2_CHANGES.md`: sha cũ / mới, câu đổi, giờ duyệt.
- `data/phase_8_1/tools/build_gold_v2.py` (sha `113716eb5cb4`): dựng v2, từ chối ghi đè.

**Code (`3f2099f`):**
- `g1_retrieval.py`:
  - `KB_ROOT`.
  - `GOLD_PATH = …/gold_v2.jsonl`, comment ghi bản 1 giữ vì G0.6.
  - `source_text(source)` (`lru_cache`) đọc file kho theo đúng cách nhãn tính offset (`validate_gold.py`: CRLF → LF).
  - `quote_is_chunk_heading(payload, quote_text)`: trích dẫn bắt đầu bằng `#` và phần chữ sau `#` nằm trong `heading_path`.
  - `chunk_hits_quote`: giữ luật cũ (cùng file + `evidence_parts` giao khoảng). Chỉ khi luật cũ không trúng mới đọc đoạn văn bản `[start, end)` và thử luật
    tiêu đề.
  - Hình dạng `(source, start, end)` không đổi, nên 6 harness đang gọi `load_gold` / `gold_coverage` không phải sửa.
- `backend/tests/test_gold_coverage.py` (mới, 2 test, chuỗi tự viết): dòng tiêu đề trúng; cùng chữ nhưng không phải dòng tiêu đề, hoặc tiêu đề khác, thì không trúng.

**Cách nhỏ nhất đã chọn:**
- **Không đổi bộ ba thành bộ bốn** (thêm chữ trích dẫn). Đổi thì chạm `load_gold` + 6 harness.
- **Đọc văn bản file kho chỉ khi cần**, có cache: luật tiêu đề chỉ chạy khi cùng file mà thân đoạn không trúng.

## 3. Cách đã chạy thật (0 USD)

```bash
uv run python data/phase_8_1/tools/build_gold_v2.py     # dựng + kiểm v2 (chỉ đọc kho), từ chối ghi đè
cd /tmp/b_gold/backend                                    # worktree tạm nhánh gold-v2 (đã gỡ; nay nhánh đã vào main ⇒ chạy từ backend/)
HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python -m pytest tests/test_gold_coverage.py -q
PYTHONPATH=. HF_HUB_OFFLINE=1 uv run --project /home/minhhieu/hue_rag python /home/minhhieu/hue_rag/data/phase_8_1/tools/recount_gold_v2.py    # tính lại (Qdrant :6335 chỉ đọc)
```

*(Sửa 27/10, C62 — review C61 m-2 / m-3: lần chạy thật dùng `python3` hệ thống cho `build_gold_v2.py` và bản tạm `/tmp/b75_recount.py`; hai lệnh
trên là lệnh đúng cho lần sau — `uv run` và script đã lưu `data/phase_8_1/tools/recount_gold_v2.py` (sha `aad629632518`). Không chạy lại; `gold_v2.jsonl`
đã có nên `build_gold_v2.py` sẽ từ chối chạy.)*

**`validate_gold.py` không chạy:** script này không nhận đầu vào, đọc `gold_batch_*.jsonl` rồi **ghi đè `gold_draft.jsonl`**, tức file đang khóa.
`build_gold_v2.py` kiểm v2 bằng đúng luật của nó, ở chế độ chỉ đọc:
- quote nguyên văn đúng 1 lần trong file nguồn sau CRLF → LF;
- start / end = vị trí đó;
- thêm: `quote_ids` trong khoảng.

## 4. Kết quả quan sát

- **Kiểm nhãn v2:** 55 câu, **0 lỗi**. `gold_draft.jsonl` vẫn `bab707b9ab22` sau khi chạy.
- **Test:** `test_gold_coverage.py` **2 passed**.
- **Tính lại `*_gold_all`** (payload Qdrant thật; `context_chunk_ids` / `top_chunk_ids` đã ghi của từng lượt):

| Lượt | Số cũ (nhãn v1, chỉ thân đoạn) | Mới (v2 + tiêu đề) | Câu đổi (loại câu) |
|---|---:|---:|---|
| Mốc B1, dev 40 (context và top-10) | 22 | **24** | 1 `conditional` (luật tiêu đề), 1 `comparative` (nhãn mới) |
| K3b-m L1, dev 40 | 31 | **33** | 1 `direct_fact` (nhãn mới), 1 `conditional` (luật tiêu đề) |
| K3b-m L2, dev 40 | 31 | **33** | như L1 |
| Mốc B1, test 15 | 7 | 7 | — |
| K3b-m, test 15 | 10 | 10 | — |

- **K3b-m dev (context):** thắng ổn định **9**, thua **0**.
  - Câu `comparative` ra: mốc nay đã đủ.
  - Câu `direct_fact` vào.
  - ⇒ kết luận tầng tìm (kém hơn ở khâu trả lời, tầng tìm tốt hơn tạm) **không đổi**.
- Khớp kỳ vọng A / C56: B1 **24** ✓; K3b-m **33**, nằm trong "32 hoặc 33" ✓. C56 tính 32 khi chưa có luật tiêu đề; luật tiêu đề thêm 1.
- **Tách hai thay đổi:** nhãn **v1** + luật tiêu đề ⇒ B1 22 → 23, chỉ đổi đúng câu `conditional`. Luật tiêu đề không làm trúng thêm câu nào khác.

## 5. Lỗi và giới hạn

- Số trong các report đã đóng (8.1, 8.2 trước 27/10) tính trên nhãn v1 và **không tính lại**. Từ nay harness nào import `GOLD_PATH` trên nhánh này sẽ đọc
  v2. Đó là đổi thước: không so trực tiếp số mới với số cũ.
- Luật tiêu đề chỉ bắt trích dẫn là **đúng một dòng tiêu đề** khớp nguyên văn một mục trong `heading_path`. Trích dẫn gồm tiêu đề + thân thì vẫn do luật
  thân đoạn xử lý.
- 3 câu test C56 "chưa quyết" vẫn chưa ai đọc; v2 không đổi chúng.
- `validate_gold.py` vẫn có thói quen ghi đè `gold_draft.jsonl` khi chạy. Ai chạy nó thì bản khóa sẽ bị viết lại từ `gold_batch_*`. Đề xuất (A quyết, ngoài
  phạm vi): thêm tham số đầu vào / đầu ra, hoặc ghi rõ cảnh báo ở đầu file.

## 6. Bàn giao cho người kiểm (C)

- `git diff main..origin/gold-v2` (2 file code / test + report).
- Kiểm lại 0 USD:
  - chạy `build_gold_v2.py` trên bản copy; hoặc so `gold_v2.jsonl` với `proposal.jsonl` theo câu;
  - `pytest tests/test_gold_coverage.py`;
  - tính lại bảng §4 bằng `gold_coverage` trên `k3/base_{dev,test}.jsonl`, `k3b/m_l1.merged.jsonl`, `m_l2.jsonl`, `m_test.jsonl`.
- `gold_draft.jsonl` phải vẫn là `bab707b9ab22`.
