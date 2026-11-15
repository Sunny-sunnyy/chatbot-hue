# Plan — trần tìm thêm 2 ⇒ 1 (tốc độ, bậc 2) · B · bản 1 · 11:51 15/11/2026

A giao 15/11 (bàn nhóm: B, C, E cùng chọn; User đã đồng ý làm tốc độ, mỗi bước plan nhẹ). Bậc trước (tìm song song) âm: model gọi song song 1 / 176 câu,
nhưng −2,3 s ở 7 câu đến từ **bớt tìm** (`report_agent/2026-11-12_ra_khoang_cach/b_tim_song_song_implementation.md`). Bậc này đo thẳng việc bớt tìm.

## 1. Đổi MỘT thứ

- `MODEL_SEARCH_LIMIT` (`backend/llm/assistant.py:56`, đang 2) đọc từ `settings.yaml` `assistant.tim_them_toi_da` (mặc định 2 ⇒ hành vi + chuỗi gửi model giống byte).
  Biến thể = 1. Lời dặn, công cụ, `het_luot_bo_cong_cu` (ẩn `tim_kho` khi hết lượt), `max_turns` **không đổi**.
- **Rủi ro chính — phải đo:** Phase 9 B2 đo tìm thêm cho câu nhiều nguồn **Completeness +1,17** (`bao_cao_he_thong/06_BAO_CAO_TIM_KIEM.md:65`). Bớt một lần tìm có thể làm câu
  nhiều nguồn / so sánh **thiếu ý**.

## 2. Câu chạm (đếm bằng code, 0 USD — mốc Golden 176 sáng 15/11, `data/tim_song_song_2026-11-15/moc/golden.jsonl`)

- Trần 1 chỉ đổi yêu cầu gửi model ở câu mà model **đã tìm thêm ≥ 1 lần** (sau lần tìm thứ nhất công cụ bị ẩn sớm hơn) ⇒ **37 / 176 câu**:
  nhiều nguồn 13 · so sánh 11 · ngoài kho 7 · điều kiện 5 · một dữ kiện 1. Trong đó **7 câu** tìm 2 lần (câu được lợi tốc độ).
- Câu không tìm thêm (139): yêu cầu giống byte ⇒ không chạy. An toàn 32: chạy ×1 (luật).

## 3. Tiêu chí (ghi trước khi thấy số)

- **Sàn:** 0 lỗi kỹ thuật · 0 lỗi trích dẫn mới · an toàn 32: 0 đổi lớp so với lượt sáng 15/11 · từ chối nhầm trên 30 câu trong kho ≤ mốc + 1.
- **Ngoài kho (7 câu chạm):** bị trả lời ≤ mốc; riêng câu hỏi giá vé đi lại đã đo A/A ×5 trên main: **3 / 5 bị "trả lời"** (`data/tim_song_song_2026-11-15/aa_160/`)
  ⇒ câu đó so với **mốc nhiễu 3 / 5** (chạy ×5 trên biến thể, trượt khi rõ hơn mốc, vd 5 / 5); 17 câu còn lại giữ sàn 0. Đây **không** phải hạ sàn: main trượt ở câu này
  là lỗi chất lượng thật, A đã đưa vào "Câu hỏi cho User" (A chốt 15/11). ×5 thêm ≈ 0,003 USD.
- **Thiếu ý (chỉ số quyết chất lượng):** 30 câu trong kho chạm, chữ khác mốc ⇒ agent con chấm mù từng cặp so đáp án mẫu: cùng ý / khác ý + bên nào thiếu ý.
  **Đạt khi bản trần 1 thiếu ý ≤ 1 câu nhiều hơn mốc** (mốc A/A: 56 / 57 cùng ý ở đo bù 15/11 ⇒ ~1 câu nhiễu / 57).
- **Tốc độ (theo dõi):** cả câu theo cặp trên 7 câu tìm 2 lần (trung vị hiệu số) và trên 37 câu chạm; số lần gọi trợ lý.
  Theo cấu trúc, 7 câu đó tối đa 2 lần gọi (từ 3) ⇒ lợi tốc độ chắc có; câu hỏi của bậc là **có mất ý không**.
- **Giữ khi:** đủ sàn + thiếu ý ≤ mốc + 1 ⇒ đề xuất bật (A merge, User đã đồng ý bật khi đạt). Không đạt ⇒ **gác tốc độ**, ghi kết quả âm.

## 4. Đo + tiền

- Mốc: dùng lại Golden 176 sáng nay (cùng kho, cùng code trừ cờ — dùng lại hợp lệ vì đầu vào / dependency / kho không đổi; ghi rõ). An toàn: lượt sáng nay.
- Biến thể ×1: 37 câu chạm + an toàn 32, cờ đặt trong settings worktree (trả lại ngay).
- Tiền ≈ 37 × 0,0005 + 32 × 0,0007 ≈ **0,04 USD**; chấm mù: quota Claude. Trần 0,1.

## 5. Khi nào sai

- Câu nhiều nguồn cần ≥ 3 nguồn ⇒ một lần tìm thêm không đủ ⇒ thiếu ý: chính là chỗ chấm mù bắt.
- Mẫu 30 câu nhỏ ⇒ "thiếu ý ≤ mốc + 1" có thể bỏ lọt tụt nhỏ (~3 %) — giới hạn ghi trong report.
- Lợi chỉ ở câu tìm 2 lần (~4 % Golden, ~13 % lượt thật) ⇒ sàn tốc độ chung vẫn chưa đạt sau bậc này.
