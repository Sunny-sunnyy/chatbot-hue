# Nhật ký 10/11/2026 — tăng tốc câu xã giao và câu hỏi ngày

**Cập nhật lần cuối: 19:16 10/11/2026.** Tiền paid trong ngày: chưa có lượt có phí nào xong (sẽ ghi từ log khi B / E đo xong).

## Tóm tắt
- Phiên tối 10/11 (mở 19:02) chỉ làm **hai lỗi tốc độ đã đo thật** ở lượt đo chung S5 hôm 09/11, không thêm tính năng mới:
  - **Câu xã giao** (chào hỏi, cảm ơn): chữ đầu chậm nhất (p95) 7,7 s, sàn 5 s. Nguyên nhân: phải chờ bước định tuyến (~1,7 s) xong mới gọi model trò chuyện.
  - **Câu hỏi ngày** (hôm nay là ngày âm nào, lễ hội còn mấy ngày): chữ đầu trung vị (p50) 5,2 s, sàn 3 s; 0,00063 USD / câu, sàn 0,0005. Nguyên nhân: model gọi công cụ ngày 2–4 lần rồi mới viết.
- Cách sửa đang làm: B cho model trò chuyện **chạy cùng lúc** với định tuyến (như câu về Huế đã làm từ 05/11); E cho **code tính sẵn ngày** đưa vào ngữ cảnh trước lần gọi model đầu, công cụ cũ giữ làm dự phòng. C review cả hai khi xong.
- Bạn chốt: quyền phiên như 09/11, trần tiền Phase 9 nâng 4,0 ⇒ 4,2 USD; **không chốt mốc đóng tính năng** (xong sớm đóng sớm, vẫn giữ chất lượng); 2 luật cách làm mới (W59, W61 — dưới).
- Vòng tự soi 1 (cả nhóm bàn): cắt bớt bộ đo không bảo vệ sàn nào — B bỏ 22 câu kiểm thêm và 5 câu ngày khỏi lượt đo tốc độ; E thu gọn phần code dò ngày chỉ còn các dạng câu có thật trong bộ đo, bỏ đo lại mốc cho 9 câu Golden.

## Bạn cần làm gì
- Không gấp, khi rảnh: phiếu toạ độ bản đồ (~15 phút) · bảng điểm v7 (~10 phút) · thu 40 câu giọng nói (~30–45 phút / người) — đường dẫn ở `session_prompt/CURRENT_HANDOFF.md` "Làm tiếp" mục 2.
- Khi bạn về: bật hay không hai cờ tốc độ (A trình kèm số đo + tiền mỗi câu). Lưu ý trước: chạy song song xã giao làm **mỗi câu về Huế đắt thêm ≈ 0,00004 USD** (có thể chạm trần 0,0005 USD / câu) — B đo số thật.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Xã giao chạy song song định tuyến (B) | đang đo — code + test đạt | nếu đạt: chào hỏi hiện chữ nhanh hơn ~1,7 s |
| Câu ngày tính sẵn (E) | đang code | nếu đạt: câu ngày bớt 1–3 lần gọi model, rẻ hơn |
| Nháp plan so sánh cuối B7 (C, 0 USD) | đang viết | chuẩn bị bước so cả hệ với RAG 1–8 trước bảo vệ |
| Luật W61 "đếm lỗi trước khi xây" | vào luật | trước tính năng mới chạy một lượt đếm rẻ; không thấy lỗi thật ⇒ không xây (09/11 bốn việc âm tốn ≈ 0,6 USD) |
| Luật W59 "đổi cờ ⇒ test có và không khoá" | vào luật | lỗi này đã lặp 3 lần |

## Giải thích ngắn (để bạn tự nói lại được)
Hai lần gọi model không phụ thuộc nhau thì cho chạy cùng lúc, bớt thời gian chờ; phép tính (ngày âm, đếm ngày) để code làm trước rồi đưa kết quả cho model, thay vì để model gọi công cụ nhiều vòng. Cả hai giữ nguyên sàn an toàn và sàn "không nói sai ngày"; đo một lượt, review một lần, cờ tắt khi merge, bạn quyết bật.

## Đọc thêm
- `session_prompt/CURRENT_HANDOFF.md` "VIỆC PHIÊN 10/11" (việc, tiêu chí, chốt tự soi)
- Plan: `docs/superpowers/plans/2026-11-10-phase-9-xa-giao-song-song-plan.md` (B), `…-t1-nhanh-plan.md` (E, trên nhánh `p9-t1-nhanh`)
