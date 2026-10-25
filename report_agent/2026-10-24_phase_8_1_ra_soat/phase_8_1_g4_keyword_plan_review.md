# Review: Phase 8.1 G4 phần từ khóa — kế hoạch B18

Decision: **ready_for_user_confirmation** (A duyệt plan được; 0 blocker, 0 major, 2 minor — nên sửa trước khi duyệt vì cả
hai là chữ "ghi trước")
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a1`)
Date: 2026-10-25 13:22 (`date`)
File: `phase_8_1_g4_keyword_plan.md` sha **`f5678965a448`** (khớp tin B) · Căn cứ: spec 8.1 §5 G4 dòng "Từ khóa", §8; skill
`run-experiment`.

## 1. Phạm vi đã review

- Đọc hết plan.
- Đối chiếu cơ chế §0 với code: runtime `dense_bm25_rrf` chấm BM25 lại đúng các đoạn dense bằng `encode_sparse_document`
  (`retrieval/full_corpus.py:526-555`), giữ điểm > 0, phá hòa theo point_id (`rank_positive_bm25`, `:179-181`). Khớp mô tả:
  BM25 chỉ xếp lại, không đưa đoạn mới vào.
- Tính lại trần §2 từ JSONL G1 (dev số chính, 32 câu có đoạn đúng, nhãn `0b65d1c138d2`).

## 2. Findings

Không có blocker hay major. Plan làm tốt các điểm sau:
- Cổng tương đương BM25 trong bộ nhớ ↔ production (top-10 / context đúng G1 + 200 cặp điểm ≤ 1e-9);
- dense chạy một lần mỗi dạng câu hỏi;
- không tạo collection;
- luật E hai phần (có dấu không kém + không dấu tốt hơn);
- ngưỡng keyword đúng thang %;
- lý do bỏ phần k khi base là âm tiết + runtime (G1.3 đã đo);
- NFC ghi NOT RUN có lý do.

- **m1 (minor) — trần của nhánh khử dấu trên runtime đã biết trước, nên ghi luôn.**
  - Bằng chứng (G1 `q_noaccent.jsonl`): câu không dấu, runtime có `context5` đủ 1/32 và dense-30 đủ chỉ **3/32**. Runtime
    BM25 chỉ xếp lại dense-30, nên E trên runtime cứu tối đa **2 câu**: về số học không thể có CI > 0, còn sau Holm thì càng
    không.
  - Plan §2 ghi "tính ở bước 0". Con số này có sẵn từ G1, không phụ thuộc biến thể, nên ghi trước được ngay.
  - **Đóng khi:** §2 / §3 E ghi "runtime không dấu: trần 2 câu ⇒ chỉ có thể chưa rõ". Có thể đổi Holm của E thành 1 (chỉ
    native là phép quyết, runtime báo theo dõi), hoặc giữ Holm 2 và ghi rõ là chấp nhận mất lực. A chọn.
- **m2 (minor) — spec ghi "đo với cách trộn thắng ở G1", plan đo cả hai cách trộn.**
  - G1 không có cách trộn nào "tốt hơn" (G1.3 chưa rõ). G4-B cho thấy lợi đến từ pool rộng. Vì vậy đo cả runtime lẫn native là
    cách đọc hợp lý.
  - Nhưng plan không nói đây là cách diễn giải chữ spec, mà việc này nhân đôi Holm (A: 6 thay vì 3).
  - **Đóng khi:** §1 thêm một câu "G1 không có cách trộn thắng ⇒ đo cả hai; A xác nhận".

Ghi nhận, không phải finding:
- **T1 cặp âm tiết** cộng chung túi từ với âm tiết, câu hỏi trọng số 1 cho mọi từ khác nhau. Như vậy một cụm 2 âm tiết khớp sẽ
  được cộng 3 lần. Đây là lựa chọn thiết kế (đã ghi rõ), không phải lỗi.
- pyvi chưa đo thời gian trên 8.459 đoạn. Plan đã có trần 20 phút / bước.
- Không chồng với G3: G3 đổi chunk ở `hue_81_g3_*`; B18 chỉ đọc collection runtime và tính BM25 trong bộ nhớ. Nếu G3 có chunker
  thắng, phần từ khóa vẫn đo trên chunk runtime. 8.2 cần đo lại khi gộp.

## 3. Kết quả tự kiểm của C (từ JSONL G1, không chạy gì mới)

| Số trong plan | C tính | Khớp |
|---|---|---|
| runtime `context5` đủ 13/32; dense-30 đủ 24/32 ⇒ trần 11 | 13; 24 | ✓ |
| native p100 `context5` 16/32; hợp hai nhánh 31/32; sparse 28/32; dense 29/32 ⇒ trần 16 | 16; 31; 28; 29 | ✓ |
| không dấu runtime `context5` 1/32 | 1 (dense-30 đủ: 3) | ✓ (+ m1) |

## 4. Decision

**ready_for_user_confirmation.** A duyệt plan sau khi B thêm hai câu m1, m2 (không đổi thiết kế); ghi sha bản duyệt. Không
cần C review lại cả plan, chỉ kiểm diff hai câu.

Tiền (C): **0 USD**.
