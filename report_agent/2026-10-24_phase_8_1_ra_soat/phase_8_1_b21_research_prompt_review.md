# Review: B21 — prompt nghiên cứu ChatGPT "câu hỏi gõ không dấu" (chuẩn bị 8.2)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 2 minor tùy chọn)
Người kiểm: C (Claude Opus 5.5, terminal `hue-rag-a1`)
Date: 2026-10-25 14:23 (`date`)
File (private): `gửi chatgpt/2026-10-25/tìm thông tin/phase_8_2_khong_dau_2026_10_25.md`, sha 12 **`68ee4b03ba7f`** (khớp tin B),
109 dòng · Căn cứ: `session_prompt/Session_Prompt.md` §9 (khuôn deep research), §5 (dữ liệu private / repo public).

## 1. Phạm vi đã review

- Đọc hết prompt.
- Đối chiếu từng số ở §2 với các report / review C đã kiểm: G1 §4 / §7, G4K report §4.1 / §4.3, review G4K.
- Đối chiếu §1 "đã nghiên cứu rồi" với `gửi chatgpt/2026-10-24/kết quả nghiên cứu/phase_8_rag_retrieval_2026_10_24.md`
  mục 5: NFC; NFC không giải quyết vị trí dấu / câu không dấu; trường ASCII-folded là đề xuất; [Chưa rõ] về e5-small. Khớp.

## 2. Kiểm theo tiêu chí

| Tiêu chí | Kết quả |
|---|---|
| Không chép câu Golden / câu kín / nội dung corpus | **đạt**. Ví dụ duy nhất là một câu chung ("bun bo hue o dau ngon"); chỉ có số đo, số file / đoạn, tên model, cấu hình |
| Không có secret, không có chi tiết dự án khác của User | **đạt** |
| Khuôn deep research §9: bối cảnh | **đạt** (§2: kho, vector, BM25, cách trộn, phần cứng, ngân sách) |
| Câu hỏi chính xác | **đạt** (§3: 7 câu, mỗi câu tách ý con đo được) |
| Chuẩn bằng chứng | **đạt** (§0: URL + ngày, 5 nhãn, cảnh báo số ngoại miền, không bịa URL) |
| Khuôn trả về có URL | **đạt** (§4: tóm tắt, theo từng câu, bảng phương án có cột "rủi ro cho câu có dấu", thứ tự P0–P3 có điều kiện dừng, danh mục nguồn, giới hạn) |
| Phần nghiên cứu cũ đã có | **đạt** (§1, dặn không lặp lại) |
| Số đo §2 khớp report | **đạt** — xem bảng dưới |

| Số trong prompt | Nguồn đã kiểm |
|---|---|
| MRR 0,73 → 0,19 (108) / 0,72 → 0,16 (88) | G1.4 / G1 §7 |
| Đủ trong 5 đoạn 13/32 → 1/32 | G1 `q_noaccent` (C tính lại ở review B18 plan) |
| Vector @100: 0,91 → 0,22 | G4K `n0` / `n0_na` cột dense pool (0,906 / 0,219) |
| Vector-30: 24/32 → 3/32 | G1 `runtime` / `q_noaccent` |
| Bỏ dấu BM25: từ vựng 5.660 → 3.182; sparse@100 25% → 81%; top-10 13% → 34%; 5 đoạn 2 → 5/32; MRR 0,21 → 0,41; câu có dấu mất 2 / 4 câu | G4K §4.1, §4.3 |

**Đủ để thiết kế thí nghiệm 8.2 không:** đủ. Q1 (phục hồi dấu), Q2 (phát hiện), Q3 (hai trường / định tuyến), Q4 (vector) phủ đúng
ba hướng thí nghiệm khả dĩ. Q5 (tỉ lệ thật, câu thật vs bỏ dấu máy, cỡ mẫu) và Q6 (mơ hồ, đ / d) phủ cách đo. Không câu nào
thừa đến mức nên bỏ.

## 3. Findings (minor, tùy chọn — không chặn)

- **m1 — thiếu một câu về cách làm trong Qdrant.** Dự án dùng Qdrant (sparse vector có tên, Query API / prefetch + RRF). Q3 hỏi
  "multi-field / dual index" theo kiểu Elasticsearch / Lucene, nhưng chưa hỏi cách làm tương đương trong Qdrant: hai sparse
  vector có tên trên cùng point, prefetch hai nhánh, chi phí lưu trữ / build lại. Nghiên cứu 24/10 đã có phần Qdrant hybrid
  query. Đề xuất thêm một gạch ở Q3: "trong Qdrant (named sparse vectors, prefetch) làm thế nào, có hạn chế gì".
- **m2 — Q7 (hệ thống thực tế) nên đánh dấu ưu tiên thấp.** Câu này khó có nguồn công khai và ít ảnh hưởng thiết kế thí nghiệm.
  Ghi "(ưu tiên thấp, nếu còn thời gian)" để Deep Research không tốn phần lớn công cho nó.

## 4. Decision

**ready_for_user_confirmation.** B có thể thêm m1 / m2 (một dòng mỗi chỗ) hoặc để nguyên, rồi A / User gửi ChatGPT. Prompt
không chứa dữ liệu private của corpus / Golden / câu kín.

Tiền (C): **0 USD**.
