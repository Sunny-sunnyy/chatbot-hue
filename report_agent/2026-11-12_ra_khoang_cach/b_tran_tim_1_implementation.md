# Trần tìm thêm 2 ⇒ 1 (tốc độ, bậc 2) — KHÔNG ĐẠT, không bật · B · 12:02 15/11/2026

Plan `docs/superpowers/plans/2026-11-15-toc-do-tran-tim-1-plan.md` (`611e5ee3c1df`, A duyệt). Nhánh `p9-tran-tim-1` `655d292`: setting `assistant.tim_them_toi_da`
(1 hoặc 2, **mặc định 2 = như cũ**, test khẳng định yêu cầu gửi model giống byte; 1 ⇒ ẩn `tim_kho` sau 1 lần tìm thật). Số: `data/tran_tim_1_2026-11-15/` (`tom_tat.json`, `tools/so.py`).

Đo ×1 (11:54–12:01): biến thể trần 1 trên **37 câu chạm** (câu mốc có tìm thêm) + câu hỏi giá vé đi lại ×5 + an toàn 32; mốc = Golden 176 sáng 15/11
(`data/tim_song_song_2026-11-15/moc/`, dùng lại hợp lệ: không commit nào chạm `backend/` hay kho từ lúc đó). Settings worktree trả về 2 sau lượt.

| Tiêu chí (ghi trước) | Mốc | Trần 1 | |
|---|---|---|---|
| Lỗi kỹ thuật | 0 | 0 | đạt |
| **Từ chối trên 30 câu trong kho chạm** (sàn ≤ mốc + 1) | 5 | **7** (2 mới, 0 hết) | **TRƯỢT** |
| Ngoài kho bị trả lời (6 câu, trừ câu giá vé) | 0 | 0 | đạt |
| Câu giá vé ×5 (mốc nhiễu 3 / 5 bị "trả lời") | 3 / 5 | 1 / 5 | đạt (không tệ hơn) |
| Lỗi trích dẫn mới | — | 0 | đạt |
| An toàn 32: đổi lớp so với kho 6 | — | 0 (29 / 3), 0 lỗi | đạt |
| Theo dõi: lần gọi trợ lý trên 37 câu | 81 | 66 | −15 |
| Theo dõi: cả câu, trung vị hiệu số theo cặp | — | câu tìm 2 lần (7): **−2,42 s** · 37 câu chạm: −0,73 s | |

- **Hai câu từ chối mới:** một câu (loại so sánh nhiều nguồn) mốc tìm 2 lần ⇒ trần 1 không đủ bằng chứng ⇒ từ chối — đúng rủi ro "thiếu ý" plan ghi (B2 tìm thêm +1,17 Completeness).
  Câu kia mốc tìm 1 lần. Cả hai từng dao động ở lượt cũ (câu thứ nhất từ chối 1 / 6 lượt cũ; câu thứ hai 0 / 4) ⇒ một phần có thể là nhiễu, nhưng sàn ghi trước không có mức nhiễu
  và không đo thêm sau khi thấy số.
- Chấm mù ý thiếu (24 cặp chữ khác): **NOT RUN** — sàn đã trượt, chấm không đổi quyết định (luật tự soi 15/11).
- Tiền: 37 câu 0,0247 + giá vé ×5 ≈ 0,0025 + an toàn 0,0246 ≈ **0,052 USD** (trần 0,1).

## Kết luận

**Không đạt — không bật.** Lợi tốc độ có thật (−2,4 s ở câu tìm 2 lần) nhưng đổi lại thêm từ chối ở câu cần nhiều nguồn — đúng thứ "chất lượng cần thiết trước" cấm đổi.
Theo chốt A: **gác tốc độ**, ghi kết quả âm. Hai bậc tốc độ hôm nay đều âm (song song: model không dùng; trần 1: mất câu trả lời).
Còn mở (cần User): mục web gọi Serper sớm (đường dữ liệu ra ngoài mới); lời dặn gộp câu tìm (đổi lời dặn).
