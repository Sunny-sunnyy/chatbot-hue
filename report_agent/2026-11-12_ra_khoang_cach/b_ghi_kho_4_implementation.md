# Ghi kho lần 4 14/11 — 8 bài quán ăn cho vùng thiếu quán trong lịch + dòng nguồn giờ Đại Nội · B · 17:56 14/11/2026

A giao (User cấp quyền "như 14/11": ghi kho / ingest được). Tiêu chí ghi trước: `data/sua_kho_2026-11-14_ghi_kho_4/TIEU_CHI.md`. Review 8 bài nháp: C (ready sau 5 minor, B sửa hết). Dữ liệu, script, log: `data/sua_kho_2026-11-14_ghi_kho_4/`.

## Đổi gì
- 8 bài mới `foods/restaurants/` (Thủy Xuân 3, Kim Long 2, Đầm Chuồn 3): 41 đoạn. Không giá; giờ chỉ ở mức "mở từ trưa tới chiều" khi nguồn nói vậy; bài nhà chòi có câu "nên hỏi trước khi đến".
- Bài Đại Nội: dòng nguồn giờ mở cửa bỏ cụm "dẫn quy định của Trung tâm…" (trang nguồn không nói vậy — C review lần 3). Mục "Nguồn dữ liệu" không được chia thành đoạn (kiểm: 0 / 108 đoạn bài Đại Nội) ⇒ sửa này không đổi tìm kiếm / câu trả lời.
- Chỉ mục: 216 ⇒ 224 file, 8.603 ⇒ **8.644 đoạn**; record `944858b9972a`, sparse `f899fe3ddee0`, T1 `f6bc8d6e4676`. Sao lưu: `knowledge-base-hue/meta/backup_ghi_kho_2026-11-14_lan_4/`. Dựng 17:47 – 17:51, cả nhóm dừng việc nặng trong lúc dựng.

## Đo (luật đo câu chạm) — ĐẠT, trừ 1 ý con
| Bộ | Kết quả |
|---|---|
| T1 (0 USD) | 9 / 158 câu đổi top 10; **3 câu chạm** (top 10 có đoạn bài mới; 0 câu chạm đoạn Đại Nội) |
| Golden: 3 câu chạm + 18 câu ngoài kho ×1 | 0 lỗi kỹ thuật, 0 lỗi trích dẫn; **ngoài kho bị trả lời 0 / 18**; từ chối nhầm 0 / 3. Đọc tay 3 cặp trước / sau (mốc: lượt đủ 176 câu sau ghi kho 2 — ghi kho 3 không chạm 3 câu này): 2 câu giống hệt; 1 câu nhiều nguồn bỏ một ý phụ câu hỏi không hỏi, còn lại sát đáp án mẫu hơn ⇒ không tụt |
| An toàn 32 ×1 | 0 lỗi, 0 lỗi định tuyến, 0 câu ngoài kho bị trả lời, 0 lỗi trích dẫn; 0 câu đổi lớp so với lần 3; **0 câu có đoạn bài mới trong ngữ cảnh** |
| 4 câu hỏi thử (B viết, không phải Golden) | Trước: 3 / 4 từ chối, 0 / 4 trích bài mới. Sau: **4 / 4 trả lời, mỗi câu có quán từ bài mới, trích đúng bài**; 0 giá; giờ chỉ "trưa tới chiều" — đúng câu trong bài (tiêu chí ghi "bài không có giờ" là viết thiếu). **Chưa đạt:** câu Đầm Chuồn không nhắc "nên hỏi trước" dù 3 bài đều có câu đó |

## Tiền (từ log)
≈ **0,030 USD**: Golden 21 câu 0,0055 · an toàn 32 0,0226 · 4 câu thử sau 0,0020 (trước 0,0033, phiên trước). Dựng chỉ mục + T1: 0 USD (CPU).

## Còn lại
- Ý con "nên hỏi trước": báo A — chọn nhận (lời dặn mềm, câu trả lời không nói gì sai) hoặc đưa câu đó lên đầu bài nhà chòi ở lần ghi kho kế. B không đo thêm sau khi đã thấy số.
- Bảng quán lịch sau ghi kho: C đã làm (`p9-quan-kho4-bang`, merge).
- Sổ ghi việc + `bai_hoc/`: theo A giao.
