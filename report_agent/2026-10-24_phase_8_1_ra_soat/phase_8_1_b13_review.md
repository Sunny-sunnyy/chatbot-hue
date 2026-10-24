# Review: Phase 8.1 — B13 phá hòa nhánh sparse `native_hybrid_rrf`

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 1 minor)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a3`)
Date: 24/10/2026, 21:19–21:24 (giờ lấy bằng `date`)
Implementation report: `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_b12_native_baseline.md` §4 (cơ
chế), §7 (B13). A duyệt sửa lúc 21:18 (report §7). Việc: A giao C19.

## 1. Phạm vi đã review

Đã đọc exact diff (working tree trên `b8dbe95`; chưa commit) của 3 file, tổng +29/−2:

- `backend/retrieval/full_corpus.py`: hàm thuần `order_by_score_then_point_id` + **đúng 1 chỗ gọi** ở nhánh
  sparse của `native_hybrid_rrf`, ngay sau `query_points`;
- `backend/tests/test_full_corpus_retrieval.py`: +1 test logic thuần;
- `backend/llm/generator_openai_full_corpus.py`: chỉ đổi comment (m2 của B11: `None` hoặc `""` = không
  gửi reasoning).

Đối chiếu bằng chứng cơ chế ở report §4 với lần chạy lại độc lập.

## 2. Findings

**Không có blocker hoặc major.**

- **Đúng chỗ, đúng luật.**
  - Hàm sắp `(-score, str(point.id))`. Đây là cùng luật phá hòa với `rank_positive_bm25` (`:179-183`) và
    RRF (`:176`), nên cả ba bước của retrieval giờ phá hòa giống nhau.
  - Chỉ nhánh `native_hybrid_rrf` bị ảnh hưởng; runtime chạy `dense_bm25_rrf` nên không đổi (đã kiểm
    byte, §4).
  - Không thêm tham số, cấu hình hay đường đi thứ hai. Docstring ghi rõ *vì sao* (Qdrant không cam kết
    thứ tự giữa các điểm bằng điểm).
- **Test** bảo vệ đúng hành vi cần thiết: cùng tập điểm, hai thứ tự đến khác nhau thì ra một thứ tự. Test
  dùng `models.ScoredPoint` thật, không mock.
- **Độ đơn giản:** sửa một dòng gọi + một hàm 1 dòng. Tương xứng với vấn đề đã chứng minh: 24/158 câu đổi
  thứ tự top-30 sparse theo `limit`, 6/6 câu lệch mốc 7B giải thích được bằng hoán vị hòa điểm.

**Minor:**

- **m1. Tập ứng viên vẫn phụ thuộc pool khi nhóm hòa điểm vắt qua biên.** Ví dụ một câu có điểm hòa ở
  hạng 30/31: Qdrant tự chọn đoạn nào lọt vào top-`limit` trước khi code sắp lại. Sắp lại không sửa được
  phần này. B đã ghi đúng giới hạn (1/158 câu ở pool 30 vs 40). Tiêu chí đóng: report G1.1/G1.3 báo số câu
  có hòa ở biên pool khi so các pool. Không cần sửa code; lấy dư rồi cắt là phức tạp không tương xứng.

## 3. Cách người kiểm chạy lại thật

Từ `backend/`, `uv` trong `.venv`, `HF_HUB_OFFLINE=1`, Qdrant chỉ đọc, 0 USD.

```bash
uv run python -m evaluation.full_corpus_eval retrieval --treatment native_hybrid_rrf --out /tmp/c19_native_1.jsonl
uv run python -m evaluation.full_corpus_eval retrieval --treatment native_hybrid_rrf --out /tmp/c19_native_2.jsonl
sha256sum /tmp/c19_native_{1,2}.jsonl ../data/phase_8_1/baseline/retrieval_native_hybrid_rrf_b13.jsonl
uv run python -m evaluation.full_corpus_eval retrieval --out /tmp/c19_dense.jsonl   # + cmp mốc 7B
PYTHONPATH=.:.. uv run python /tmp/b11/pool_check.py                                # dùng service production, pool 30 vs 40
uv run python -m pytest -p no:cacheprovider tests/test_full_corpus_retrieval.py -q
```

## 4. Kết quả quan sát

| Kiểm | Kết quả |
|---|---|
| `native_hybrid_rrf` 2 lượt của C | **PASS**: cả hai SHA-256 `1fbb5c17b82003b1…`, **giống** mốc mới B lưu ở `data/phase_8_1/baseline/retrieval_native_hybrid_rrf_b13.jsonl` |
| `dense_bm25_rrf` | **PASS**: giống từng byte mốc 7B `cefb2d1a…` (runtime không đổi) |
| Top-30 sparse pool 30 vs 30 đầu của pool 40 | **157/158 trùng**; 1 câu khác do hòa điểm vắt qua hạng 30; 0 câu khác vì lý do khác (trước B13: 24/158 khác, theo B §4) |
| `test_full_corpus_retrieval.py` | **PASS**: 26 passed (gồm test mới) |
| `git diff --check` | sạch |

Không chạy lại pytest 15 file. B đã chạy (196 passed), và thay đổi chỉ chạm một nhánh retrieval cùng file
test của nó, mà C đã chạy lại. Dùng lại bằng chứng của B cho các file test còn lại vì đầu vào khác không đổi.

## 5. Giới hạn

- Nguyên nhân làm thứ tự hòa điểm đổi giữa 14:39 và hôm nay vẫn **chưa chứng minh** (B §4). Sau B13 điều
  này không còn ảnh hưởng tới kết quả native, trừ trường hợp hòa ở biên pool (m1).
- Dense HNSW không phá hòa (vẫn lấy thứ tự Qdrant). Dense hòa điểm hiếm, và `dense_bm25_rrf` giống byte qua
  nhiều lần chạy, nên chưa thấy vấn đề quan sát được; không đề xuất sửa.

## 6. Decision và bước tiếp theo

**`ready_for_user_confirmation`.** A commit 3 file B13 + report B12. Mốc native cho G1.3 = SHA `1fbb5c17…`
(`data/phase_8_1/baseline/`, private). Báo m1 trong report G1.
