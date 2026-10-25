# Review: plan G3 §10 "G3.B10" (sha `6d71a4589ea8`) — chỉ §10

Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 (A giao qua C) · Phạm vi: chỉ §10 plan
`phase_8_1_g3_plan.md`; đối chiếu §1, §2, §4, §9 và dữ liệu `data/phase_8_1/g3/base.jsonl` (chỉ xem tên trường).

**Kết luận: `changes_requested` (nhẹ) — 1 major, 2 minor; đều sửa bằng chữ trong plan, trước khi tính biến thể.**

## Findings

- **M1 (major) — phép so quyết đổi hai thứ cùng lúc (câu hỏi (1) của C).**
  - Vị trí: §10 "Baseline quyết = runtime context 10 đếm theo số đoạn"; quyết `ctxB10` biến thể vs `ctx10` baseline.
  - Yêu cầu: skill `run-experiment` §1.2 (một thay đổi mỗi biến thể); chính §9.2 của plan này (quyết bằng phép so với base
    mà bước đó dựng lên, phép so tổng vẫn báo).
  - Tác động: biến thể khác baseline ở **cả** cách chia đoạn **lẫn** cách dựng context (ngân sách token vs đếm 10 đoạn).
    Vì B10 là trung vị, khoảng nửa số câu baseline có context 10 đoạn **dài hơn** B10 ⇒ biến thể bị thiệt về token ở nửa đó
    và được lợi ở nửa kia; kết quả "thắng / thua" trộn hiệu ứng ngân sách với hiệu ứng đoạn to. Không tách được "đoạn to giúp"
    khỏi "đổi luật dựng context".
  - **Đóng khi:** plan ghi hai phép so, ghi trước:
    (a) **quyết** = `ctxB10` biến thể vs `ctxB10` của **base cùng chunker nền** (H1 — vì biến thể dựng trên H1; runtime
    ctxB10 báo kèm), cùng luật dựng context ⇒ đổi đúng một thứ; Holm 2.
    (b) **thực dụng / đề xuất 8.2** = `ctxB10` biến thể vs `ctx10` runtime (cấu hình G2.1a): chỉ để vào danh sách đề xuất
    thay G2.1a, cần **thêm** 0 câu mất so với `ctx10` runtime và cận trên CI ≥ 0 (không kém) — như cách §9.2 dùng phép so
    baseline làm điều kiện phụ.
- **m1 (minor) — §4 chưa nói context nào dùng cho câu trả lời nếu B10 thắng.**
  - §4 sinh câu trả lời cho {chunker thắng × context 5 / 10} **đếm theo số đoạn**; còn §10 quyết dưới context-B10. Nếu B10
    thắng mà §4 chạy context 10 đoạn đếm số, thì cấu hình đo câu trả lời khác cấu hình đã thắng.
  - **Đóng khi:** §10 "Nếu tốt hơn" ghi: lượt câu trả lời dùng context-B10 (harness dựng `packed` từ đúng danh sách
    context-B10, như cách G2 dùng `answer_case` với builder tham số), baseline = G2.1a (ctx10) chấm lại cùng lượt mù (§9.3).
- **m2 (minor) — cách tính offline: tương đương được, nhưng nên có một cổng tự kiểm (câu hỏi (2) của C).**
  - Lập luận tương đương: retrieval của biến thể chỉ phụ thuộc chỉ mục lúc build (đã xóa collection) và câu hỏi; top-10 đã
    lưu (`top_chunk_ids`) là kết quả thật. Khâu tính mới (đóng gói context theo ngân sách) chỉ cần nội dung đoạn
    (`evidence_parts`, `search_text`) — dựng lại bằng `make_chunks` + kiểm sha danh sách đoạn = nội dung lúc build ⇒ tất định,
    tương đương chạy lại. Hai chỗ có thể lệch: (i) id trong `top_chunk_ids` phải là id của danh sách dựng lại (đoạn gộp
    đổi id) — sha khớp thì id khớp; (ii) đếm token phải dùng đúng hàm của context-B (`o200k_base` trên khối bằng chứng, bỏ
    đoạn không bằng chứng như `FullCorpusContextBuilder._source`).
  - **Đóng khi:** plan thêm cổng trước khi tính B10: dùng chính lệnh `rebudget` với **B cũ (750)** trên `base`, `h1`,
    `h1-h2_384`, `h1-h2_512` ⇒ `ctxB_chunk_ids` phải **giống hệt** bản đã lưu từ lượt chạy thật (mọi câu). Lệch ⇒ dừng, tìm
    nguyên nhân. Rẻ, và chứng minh offline = live cho đúng khâu bị tính lại.

Ghi nhận, không phải finding: context-B10 lấy đoạn "trong top-10" nên với runtime chunks (đoạn nhỏ) có thể không dùng hết
B10 khi 10 đoạn ngắn hơn B10 — chấp nhận được (cùng giới hạn top-10 cho mọi bên), nên báo số câu "chưa dùng hết ngân sách"
cho từng bên.
