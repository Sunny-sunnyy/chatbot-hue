# Review: C30 — 3 báo cáo cho User (Phase 8.1)

Decision: **ready_for_user_confirmation** (0 blocker, 0 major, 4 minor — sửa chữ)
Người kiểm: B (Claude Opus 5.5, terminal `hue-rag-3f`) · 2026-10-25 (`date` khi viết: sau 14:10)
File được kiểm: `bao_cao_he_thong/BAO_CAO_DANH_GIA.md` (bản 2, sha `e923249c13af`), `BAO_CAO_BO_CAU_HOI_GOLDEN.md` (bản 5,
`98c92d8e9d40`), `BAO_CAO_EMBEDDING_TU_KHOA.md` (bản 3, `e056d8561662`). Đối chiếu: `session_prompt/TEMPLATE_USER_REPORT.md`,
`WORKFLOW.md` §6, report gốc G0–G4K. Chỉ docs ⇒ kiểm nhất quán, số, link, trạng thái; không chạy lại.

## 1. Cổng tối thiểu

- Chỉ 3 file trên đổi (ngoài 3 file B20 của B); không đổi code. `git diff --check` sạch.
- Đúng mẫu: §1 Tóm tắt có dòng 8.1 + "bạn cần quyết gì"; §3 checklist dùng thang 5 mức; §4 mục mới ở trên; §5 bảng còn
  đúng / đã thay; §6; mã nội bộ dồn xuống Phụ lục. Lời thường, số kèm ý nghĩa, tiền ghi rõ (0 USD cho 8.1 ở cả ba).
- Repo public: không chép câu Golden / câu kín / corpus; câu kín chỉ có số đếm và trạng thái; hash chỉ 12 ký tự. **Đạt.**

## 2. Đối chiếu số với report gốc (khớp)

| File | Số kiểm | Nguồn | Kết quả |
|---|---|---|---|
| EMBEDDING §4 | cặp âm tiết mất 1 / 3; pyvi 1 / 4; khử dấu có dấu mất 2 / 4; không dấu native sparse@100 25 % → 81 %, top-10 13 % → 34 %, 5 đoạn 2/32 → 5/32; b 1,0 cả hai + b 0,5 native mất 1–2 | G4K §4.1–4.4 | khớp |
| EMBEDDING §1 | không dấu 1/32 vs 13/32 | G4K §4.1 | khớp |
| DANH_GIA §4 | nhiễu judge-only Đủ 2/88 (TB 0,000), Đúng 1/88, Trúng ý 3/88; cả đường 10/83, +0,048 | G2 §4 đối chứng, §4.5 | khớp |
| DANH_GIA §1, §4 | context 10 +0,26 / +0,27; 22/22 từ chối nhầm thiếu dữ kiện | G2 §4.1, §4.4; G1 G1.6 | khớp |
| DANH_GIA §4 | nhóm kiểm 24 / 9 / 9 / 8 / 6 = 56; câu ngoài kho ở test = 6 | G2 test (6 OOS) | khớp |
| GOLDEN §1, §3 | nhãn 82 / 65 / 29; đoạn đúng 55 (40 / 15); câu kín 36, phân bố 15 / 6 / 7 / 5 / 3 | handoff + realism sha `0b65d1c138d2` | khớp |

## 3. Findings

- **m1 — "A và C không đọc nội dung câu kín" (DANH_GIA §4 hàng Câu kín; GOLDEN §4 mục 25/10) lệch report G5 §6** ("A đã thấy
  nội dung 3 câu kín — User trích khi hỏi"). **Đóng khi:** viết "A và C không mở file câu kín; A đã thấy 3 câu do bạn trích khi
  hỏi" (hoặc tương đương) ở cả hai chỗ.
- **m2 — EMBEDDING §4 "công thức kiểm khớp từng bit với code đang chạy"** nói mạnh hơn số đo: cổng G4K cho 195/200 cặp giống
  từng bit, 5 cặp lệch ≤ 8,9e-16; mốc runtime 108/108 câu giống; native lệch 1/108 do Qdrant tính float32. **Đóng khi:** "khớp
  code đang chạy (thống kê giống hệt; điểm giống tới bit cuối ở 195/200 cặp; kết quả runtime giống 108/108 câu)".
- **m3 — EMBEDDING Phụ lục lệch 3 ghi nhánh GPU còn sót "Phase 8.1"**, trong khi §6 cùng file ghi "dời sang 8.2". **Đóng khi:**
  sửa Phụ lục thành 8.2.
- **m4 — DANH_GIA chưa nói "theo loại câu" của 8.1.** Spec §6 tiêu chí 2 đòi kết quả theo loại câu; bảng mới
  `report_agent/2026-10-24_phase_8_1_ra_soat/phase_8_1_g5_by_category.md` (B, sau review G5 M1) có số. **Đóng khi:** §4 mục
  25/10 hoặc §6 thêm một dòng trỏ tới bảng đó (ví dụ "lợi của 10 đoạn nằm ở câu nhiều nguồn / so sánh; câu trực tiếp không
  đổi"). Tùy A nếu muốn để A ghi ở `TONG_HOP`.

Ghi nhận, không phải finding:
- DANH_GIA §4 (bản 1 của A) ghi nDCG 7B **0,75**, `BAO_CAO_TIM_KIEM.md` ghi **0,76** (số gốc 0,755) — chênh do làm tròn, có từ
  bản trước; nếu sửa thì chọn một cách làm tròn cho cả hai.
- EMBEDDING ghi đúng chỗ "câu không dấu do máy bỏ dấu, chưa phải câu thật" — giới hạn quan trọng nhất của G4K E.

## 4. Kiểm lại phần sửa (DANH_GIA `144743777731`, GOLDEN `5f88735f8bc4`, EMBEDDING `49ad454d61ce`)

- m1: DANH_GIA §4 (hàng Câu kín) và GOLDEN §4 (mục 25/10) ghi "C không đọc nội dung, A chỉ thấy 3 câu do bạn trích khi hỏi" —
  khớp G5 §6 — **đóng**.
- m2: EMBEDDING §4 ghi "195/200 cặp giống từng bit, 5 cặp lệch ≤ 8,9e-16" — **đóng**.
- m3: EMBEDDING Phụ lục lệch 3 ghi "dời sang 8.2", khớp §6 — **đóng**.
- m4: DANH_GIA Phụ lục trỏ `phase_8_1_g5_by_category.md` — **đóng**.
- Ghi nhận nDCG: DANH_GIA dùng số gốc 0,755 — hết lệch làm tròn với TIM_KIEM (0,76 là làm tròn của cùng số).

Kết luận giữ nguyên: **ready_for_user_confirmation**, không còn finding mở.
