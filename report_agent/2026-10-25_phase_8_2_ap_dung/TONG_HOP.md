# TỔNG HỢP Phase 8.2 — áp dụng phương án thắng 8.1 (chờ User đóng)

Người viết: A (`hue-rag-bf`) · 10:21 28/10/2026 (`date`) · Đợt mở 16:05 25/10. Spec `docs/superpowers/specs/2026-10-25-phase-8-2-apply-winners-design.md`: bản gốc
`dabae90b2b60` (User duyệt 16:21 25/10) + §10 sửa đổi 26/10 (`cd910c4c4169`) + §11 sửa đổi 28/10 (`5255f3274707`, User chọn PA3). Bước 2 (đợt cải tiến từng khâu) có
tổng hợp riêng: `report_agent/2026-10-26_cai_tien_tung_khau/TONG_HOP.md`.

## 1. Mục tiêu

Đưa vào chatbot phương án thắng của 8.1 (**context 10** + chuẩn hóa **NFC** câu hỏi), thử tín hiệu trên chatbot mới, rồi kiểm cuối trên 36 câu kín chưa ai dùng để chọn.

## 2. Quyết định chính theo thời gian

| Khi | Ai | Quyết định |
|---|---|---|
| 25/10 16:21 | User | Duyệt spec 8.2: B0 mốc người ⇒ B1 ⇒ Bước 2 ⇒ B3; trần 0,5 USD |
| 25/10 16:5x | User | Dừng 8.2, rà code Phase 0–7 trước (xong 26/10, `report_agent/2026-10-25_ra_soat_code/TONG_HOP.md`) |
| 26/10 21:1x–21:3x | User | Bước 2 = đợt cải tiến từng khâu (spec §10, luật (a) / (i)) |
| 27/10 11:0x | User | Chốt đợt cải tiến: không biến thể nào vào chatbot |
| 28/10 09:2x | User | **PA3**: B0 không chặn B1 / đóng 8.2; B0 thành mốc người làm sau (trước bảo vệ) — spec §11 |
| 28/10 09:34 | A | Merge B1 `510e1a8` (C71 ready 0 / 0 / 0); 5 chỗ báo cáo `92b9a43` + `3ad2265` (B79 ready) |
| 28/10 09:5x | User | Chạy B3 ngay (mở câu kín cho người chạy B) |

## 3. Kết quả

| Bước | Kết quả | Bằng chứng |
|---|---|---|
| B0 mốc người | **Dời** (spec §11) — file đọc cặp mù sẵn `data/phase_8_2/b0/`, luật dừng §3 mục 4 giữ nguyên | `phase_8_2_b0_prep_implementation.md` / `_review.md` |
| B1 context 10 + NFC | **Vào chatbot 28/10** (`510e1a8`): T1 158 câu giống byte mốc; 176 câu ở 10 đoạn ≈ 0,00021 USD / câu, từ chối nhầm 12 / 158 (5 đoạn: 22 / 158) | `phase_8_2_b1_implementation.md`, `_rebase2_*`, `_merge_*`, `_bao_cao_review.md` |
| Bước 2 đợt cải tiến | K1, K3, K3b-n, R1, R2 kém hơn; K3b-m tầng tìm tốt hơn (tạm) nhưng trả lời kém hơn theo luật (gác); R3, K2, E2 NOT RUN; R4 xong (thước số) | `2026-10-26_cai_tien_tung_khau/TONG_HOP.md` |
| **B3 câu kín (S36)** | "Không làm hỏng" **và** tốt hơn: 33 câu trong kho — Completeness **+0,818** [+0,394; +1,333] (12 tốt / 21 như nhau / **0 tụt**), Accuracy **+0,697** [+0,273; +1,212] (8 / 25 / 0); ngoài kho bị trả lời **0 / 3**; lỗi kỹ thuật 0; từ chối nhầm 4 ⇒ 2; câu 500 citation 4 ⇒ 0; bỏ 4 câu 500 vẫn Completeness +0,448 [+0,138; +0,828], 0 tụt | `phase_8_2_b3_implementation.md`, C74 `phase_8_2_b3_review.md` (ready 0 / 0 / 1, tái lập byte) |

Chatbot cuối 8.2 (đang chạy): `dense_bm25_rrf` (pool 30) ⇒ top-10 nguyên đoạn vào context ⇒ `gpt-6-luna` (suy luận mặc định) ⇒ validator v2 (nhận `[n]` và `[Nguồn n]`);
câu hỏi NFC trước khi tìm; `/api/chat` ghi `chat_metrics` mỗi câu.

## 4. Tiêu chí nghiệm thu (spec §6, có §10 / §11 thay)

1. B0 — **thay bởi §11**: không là điều kiện đóng; làm sau. ✓ (theo §11)
2. B1 đạt B1.2, chatbot thật chạy context 10 + NFC, báo cáo cập nhật. ✓
3. Bước 2 theo §10: mỗi biến thể có plan duyệt sha, kết luận ghi cả âm. ✓
4. B3 chạy khi User quyết; kết quả ghi cả âm. ✓
5. Tiền 8.2 ≈ **0,227 / 0,5 USD** (≈ 0,213 tới 27/10 + cổng merge 0,000423 + B3 0,0138); Qdrant vẫn 1 collection runtime. ✓

## 5. Giới hạn

- **Chưa có mốc người**: mọi điểm chất lượng do judge Claude chấm; B0 làm sau — luật dừng kích hoạt ⇒ A trình User giữ 10 / về 5 và xét lại kết luận dựa judge.
- B3 chỉ báo S36 (khớp được 1 / 3 câu A đã thấy, không dựng S33); 0 câu kín ở dạng NFD ⇒ NFC chưa được câu kín thử (8.1 đã đo trên câu dựng).
- B3 gộp ba thay đổi (context 10, NFC, validator v2) — không tách phần từng cái. Judge về nguyên tắc có thể đoán bên qua citation [6]–[10] (giống 8.1) ⇒ lần sau đánh
  số lại citation trước khi xuất lô chấm (C74).
- **Tốc độ chưa đạt yêu cầu User chốt 28/10** (p50 ≤ 3 s, p95 ≤ 5 s): context 5 đo p50 3,3 / p95 5,7 s; context 10 chưa đo p50 / p95 (đang đo ở bộ "trước" B78).
- Câu kín đã mở ⇒ không còn là bộ kiểm "chưa ai thấy" cho các lần đo sau.

## 6. Bước tiếp

1. User đóng 8.2 ⇒ A: Project_Status §3, HISTORY, guide 8, nhật ký, README.
2. **Đợt sửa kho + build lại index** (spec `937cf8969810`): bộ "trước" đang chạy (B, plan `41485782b39e`); bước 1–6 sau khi kiểm "còn hiệu lực".
3. Đo thời gian tới chữ đầu tiên (C73, plan `9683641b6c38`) sau bộ "trước" ⇒ A brainstorm spec streaming với User.
4. Thí nghiệm Qwen3-8B sau đợt sửa kho; B0 khi User rảnh.
