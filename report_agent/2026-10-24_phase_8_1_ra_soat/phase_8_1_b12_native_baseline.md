# Implementation Report: Phase 8.1 — mốc `native_hybrid_rrf` không tái lập (B12, điều tra, không sửa)

Người làm: B (Claude Opus 5.5, terminal `hue-rag-b0`)
Date: 2026-10-24 21:05–21:15 +0700 (lấy bằng `date`)
Việc: A giao 21:04 (tin nhắn; quyết theo đề xuất ở report B11 §5). Skill `systematic-debugging` — tìm nguyên nhân, không vá.
Liên quan: `phase_8_1_g0_5_params_implementation.md` §4–§5 (phát hiện), spec 8.1 §5 G1.3.

## 1. Phạm vi

(1) Chạy `native_hybrid_rrf` 176 câu 2 lần bằng code HEAD: hai lượt có giống nhau không. (2) 6/158 câu lệch
so với file 7B lệch ở đâu. (3) Đề xuất mốc native mới. Chỉ đọc Qdrant, không sửa code, 0 USD.

## 2. Thay đổi

Không đổi code hay dữ liệu. Script điều tra (chỉ đọc) ở `/tmp/b11/`: `b12_trace.py`, `b12_perm.py`, `b12_ties.py`.

## 3. Cách đã chạy thật

- Code HEAD thuần: `git archive HEAD backend` → `/tmp/b11/head/` (symlink `data/`, `knowledge-base-hue/` chỉ đọc;
  đã kiểm module import từ chính bản đó), `uv run --project <repo> python -m evaluation.full_corpus_eval retrieval
  --treatment native_hybrid_rrf` **2 lần** (`/tmp/b11/retrieval_native_head.jsonl`, `…_head2.jsonl`).
- Lịch sử: mtime file mốc, `git log`/`git diff ea5a1d5 HEAD` cho `retrieval/full_corpus.py`, `embedding/sparse.py`,
  `scoring/bm25.py`, `embedding/full_corpus.py`, `vectorstore/qdrant.py`, `evaluation/full_corpus_eval.py`.
- Lần theo 6 câu (`b12_trace.py`): trace từng nhánh (dense / sparse / RRF) của service hiện tại; hỏi lại nhánh
  sparse với `limit=40` để thấy hòa điểm quanh biên 30.
- Thử giả thuyết (`b12_perm.py`): giữ nhánh dense hiện tại; hoán vị trong từng nhóm điểm sparse **bằng nhau**
  (lấy 40 hạng, cắt 30), tính RRF bằng chính `reciprocal_rank_fusion` production; có hoán vị nào ra **đúng**
  top-10 của file 7B không.
- Đo phạm vi (`b12_ties.py`): trên 158 câu trong kho, đếm câu có hòa điểm trong top-30 sparse; so thứ tự top-30
  giữa `limit=30` và `limit=40`; so 2 lần gọi cùng `limit=30`.

## 4. Kết quả quan sát

**(1) Hai lượt HEAD giống nhau từng byte** (SHA-256 `3cf954e5…`), và giống lượt có code B11. Hôm nay không có
dao động giữa các lượt.

**(2) Lệch ở đâu.**

| Câu | Loại | Hạng lệch (1–10) | Cùng tập 10 đoạn? | Hòa điểm sparse trong top-30 (hạng bắt đầu, cỡ nhóm) |
|---|---|---|---|---|
| 0 | direct_fact | 10 | không (đổi 1 đoạn ở hạng 10/11) | (13,2) (17,3) (21,3) |
| 10 | direct_fact | 6–8 | có (đảo thứ tự) | (8,3) (12,2) |
| 14 | direct_fact | 5, 7–10 | không | (3,3) (6,2) (8,3) (11,2) (13,4) (17,2) |
| 16 | multi_source | 1–4 | có | (2,2) |
| 25 | conditional | 3–5, 8–9 | có | (5,3) (12,2) (30,2) ← vắt qua biên 30 |
| 162 | direct_fact | 9–10 | không | (3,2) (6,2) (9,2) (11,3) (14,5) (30,2) ← vắt qua biên 30 |

- Nhánh lệch: **sparse** (Qdrant). Nhánh dense không lệch: `dense_bm25_rrf` (cùng truy vấn dense) vẫn giống từng
  byte mốc 7B.
- **Thử giả thuyết: 6/6 câu PASS** — với mỗi câu có một cách xếp lại các đoạn hòa điểm sparse cho ra đúng top-10
  của file 7B (dense giữ nguyên, RRF production). Câu 0 và 16: chính thứ tự trả về khi gọi `limit=40` đã khớp 7B.
- **Phạm vi:** 40/158 câu có hòa điểm trong top-30 sparse; ở **24/158** câu, thứ tự top-30 **khác nhau giữa
  `limit=30` và `limit=40`**; gọi lại cùng `limit=30` thì 0/158 khác. Tức là Qdrant xếp các đoạn hòa điểm theo
  chi tiết nội bộ (phụ thuộc cả `limit`): lặp lại được trong cùng trạng thái, nhưng không cam kết.
- Code truy xuất/từ khóa/evaluator không đổi về logic từ lúc ghi mốc (14:39) tới HEAD: diff chỉ là xóa hàm
  không dùng (`bm25.py`, `qdrant.py`, B9) và tham số mặc định (B11, chưa commit). Golden có mtime 16:41 nhưng
  `dense_bm25_rrf` (có tính keyword) vẫn giống byte, nên câu hỏi/keyword dùng cho truy xuất không đổi.

**Nguyên nhân — tách bậc chứng minh:**

- **Đã chứng minh (cơ chế):** lệch do **thứ tự giữa các đoạn hòa điểm ở nhánh sparse của `native_hybrid_rrf`**.
  Nhánh này lấy nguyên thứ tự Qdrant trả về (`backend/retrieval/full_corpus.py:595-605`), không phá hòa. Ngược
  lại, runtime `dense_bm25_rrf` tự chấm BM25 và phá hòa theo ID điểm (`rank_positive_bm25`, `:179-183`), RRF cũng
  phá hòa theo ID (`:176`) — nên runtime tất định, native thì không.
- **Chưa chứng minh (cái gì làm thứ tự hòa đổi giữa 14:39 và hôm nay):** giả thuyết là trạng thái nội bộ Qdrant
  đổi sau khi tắt/bật lúc ~17:10 (và/hoặc khi xóa 2 collection Foods). Không tái tạo được trạng thái cũ để kiểm.

## 5. Lỗi và giới hạn

- Không có bản trace sparse của lượt 7B, nên bước (2) chứng minh "có một hoán vị hòa điểm khớp", không chứng minh
  hoán vị đó là đúng thứ tự Qdrant đã trả lúc 14:39 (với câu 14 và 162 có nhiều hoán vị; B dừng ở hoán vị đầu
  tiên khớp).
- Không sửa code (đúng yêu cầu). Không thử bật/tắt Qdrant để tái tạo (đổi môi trường, ngoài quyền).

## 6. Đề xuất (A quyết)

**A quyết 21:15:** mốc native cho G1.3 = lượt hôm nay, ghi giới hạn (cái làm thứ tự hòa điểm đổi giữa 14:39 và
hôm nay chưa chứng minh). Mục 2 dưới (phá hòa sparse trước G1) vẫn chờ A.

1. **Mốc native mới = lượt HEAD hôm nay** (`/tmp/b11/retrieval_native_head.jsonl`, SHA-256 `3cf954e5…`; 2 lượt
   giống nhau). Nên chép vào `data/phase_8_1/` (private) khi A khóa baseline G0.6 — `/tmp` có thể mất. MRR/nDCG
   của 6 câu đổi chỉ vì đảo các đoạn hòa điểm, nên số trung bình mốc mới khác mốc 7B rất ít.
2. **Cảnh báo cho G1:** 24/158 câu có thứ tự hòa điểm sparse đổi theo `limit`. Thí nghiệm G1.1/G1.3 đổi pool
   30/100/200 ở nhánh sparse sẽ **trộn hai hiệu ứng**: đổi pool thật + xáo lại hòa điểm. Trước G1 nên chọn một
   trong hai: (a) phá hòa tất định cho nhánh sparse (sắp `(-score, point_id)` như `rank_positive_bm25`) — đổi
   code production nhánh `native_hybrid_rrf` (runtime không chạy nhánh này nên byte runtime không đổi), cần A
   duyệt như một tham số/sửa riêng; hoặc (b) giữ nguyên, ghi giới hạn, và khi so cùng pool thì chạy lại mốc ngay
   trước khi đo (skill `run-experiment` §3.1). B nghiêng (a): một dòng sắp xếp, loại hẳn nhiễu thay vì phải
   giải thích nó trong mọi kết luận về hybrid.
3. Không cần đổi mốc `dense_bm25_rrf`.

Tiền: **0 USD**.

## 7. B13 — phá hòa nhánh sparse native (A duyệt 21:18; 21:16–21:22 +0700, 0 USD)

**Sửa (đúng một chỗ dùng):** `backend/retrieval/full_corpus.py` thêm hàm thuần `order_by_score_then_point_id`
(sắp `(-score, point_id)`, cùng luật với `rank_positive_bm25`) và gọi nó ở nhánh sparse của `native_hybrid_rrf`
ngay sau `query_points`. `backend/tests/test_full_corpus_retrieval.py` +1 test logic thuần: cùng tập điểm, hai
thứ tự đến khác nhau ⇒ một thứ tự. m2 (B11): giữ nguyên, ghi rõ trong comment generator `None hoặc "" = không
gửi`. Diff: +29 / −2 trên 3 file.

| Kiểm (chạy thật, Qdrant chỉ đọc) | Kết quả |
|---|---|
| `retrieval --treatment dense_bm25_rrf` | **PASS** giống từng byte mốc `cefb2d1a…` (runtime không đổi) |
| `retrieval --treatment native_hybrid_rrf` × 2 | **PASS** hai lượt giống nhau; **mốc native mới SHA-256 `1fbb5c17b82003b19aea11b38d85796cbf9f15b99c2230783c42b9b27164136f`**, lưu ở `data/phase_8_1/baseline/retrieval_native_hybrid_rrf_b13.jsonl` (private, git bỏ qua) |
| So mốc mới với file 7B / với lượt HEAD trước B13 | khác 6 / 7 câu (chỉ thứ tự hòa); trung bình MRR 0,7263 / nDCG 0,7613 / Coverage 93,41 — trùng mốc 7B tới 4 chữ số (lượt trước B13: 0,7255 / 0,7609 / 93,41) |
| Top-30 nhánh sparse: pool 30 vs 30 đầu của pool 40 (`/tmp/b11/pool_check.py`) | **157/158 trùng** (trước sửa: 24/158 khác). 1 câu khác vì nhóm hòa điểm vắt qua hạng 30 — pool 30 chỉ nhận một phần nhóm, tức là hiệu ứng pool thật, không còn xáo hòa |
| Pytest 15 file | **PASS** 196 passed (195 + 1 test mới) |
| `git diff --check` | sạch |

Giới hạn còn lại: hòa điểm vắt qua biên pool vẫn làm *tập* ứng viên phụ thuộc pool (đúng bản chất "lấy N đầu" khi
điểm bằng nhau); G1 nên báo số câu có hòa ở biên khi so pool.
