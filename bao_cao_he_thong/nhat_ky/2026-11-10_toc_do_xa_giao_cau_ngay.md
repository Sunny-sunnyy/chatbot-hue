# Nhật ký 10/11/2026 — tăng tốc câu xã giao và câu hỏi ngày; sửa báo cáo cho đúng hiện trạng

**Cập nhật lần cuối: 19:48 10/11/2026.** Tiền paid trong ngày tới giờ: ≈ 0,11 USD (~2.800 đồng) — B ≈ 0,079 (xã giao) · E ≈ 0,031 (câu ngày) · C, A 0 (review / sửa báo cáo dùng quota Claude). Phase 9 ≈ 3,7 / trần 4,2 USD.

## Tóm tắt
- Phiên tối 10/11 (mở 19:02) chỉ sửa **hai lỗi tốc độ đã đo thật** ở lượt đo chung 09/11, không thêm tính năng:
  - **Câu hỏi ngày** (hôm nay là ngày âm nào, lễ hội còn mấy ngày) — **ĐẠT mọi tiêu chí ghi trước**: code tính sẵn ngày đưa vào ngữ cảnh, model không phải gọi công cụ nhiều vòng. Chữ đầu trung vị 5,60 ⇒ **2,35 s**, chậm nhất (p95) 10,14 ⇒ **4,56 s**; tiền 0,00049 ⇒ **0,00036 USD / câu**; số lần gọi model 52 ⇒ 31 (19 câu); đúng ngày bằng bản cũ; an toàn 12 / 12. Lượt đo đầu có 1 câu nói sai năm ("năm nay") ⇒ sửa bằng code, đo lại đúng. Review (C) bắt thêm 1 lỗi tiềm ẩn ("mùng 2 tháng 9" không có chữ "âm" bị hiểu là ngày âm) ⇒ đã sửa. **Chờ bạn đồng ý để thay bản đang chạy** (không có cờ riêng — merge là đổi ngay).
  - **Câu xã giao** (chào, cảm ơn) — **CHƯA ĐẠT tiêu chí ghi trước**: cho model trò chuyện chạy cùng lúc với bước phân loại câu hỏi. Trung vị 3,46 ⇒ **1,85 s** (nhanh rõ), nhưng chậm nhất (p95) 7,73 ⇒ **5,74 s** (sàn 5 s); câu ngoài phạm vi p95 5,21 s (sàn 5) và 0,00056 USD / câu (trần 0,0005). Phần đuôi chậm nghi do bước phân loại xếp nhầm / chậm ở vài câu (giả thuyết, chưa chứng minh). Mình **không sửa tiêu chí sau khi thấy số**, không đưa vào chatbot; code đã review xong, để sẵn — **bạn chọn bật hay đóng thành hồ sơ**.
- **Sửa báo cáo cho đúng hiện trạng** (bạn yêu cầu): 2 agent con đọc thử thư mục này như người không đọc code, tìm ~60 chỗ cũ / sai và chỗ khó hiểu ⇒ sửa mục lục + 10 báo cáo khâu (vd Qdrant có 2 collection, hỏi bằng ảnh đã bật 08/11, câu khẩn cấp soạn sẵn đã gỡ 09/11, số tốc độ 09/11, chatbot Phase 9 **chưa đo lại cả bộ 176 câu**); mỗi file chỉ còn một dòng "Cập nhật lần cuối". C review: đạt. **Chưa đổi cấu trúc / thứ tự đọc** — chờ bạn chọn.
- B chuẩn bị bản deploy chạy trên máy (không đụng AWS): bắt được 1 lỗi thật — cấu hình cũ sẽ đưa ảnh riêng #5 vào bản công khai ⇒ đã chặn.
- **Vào chatbot (`1633c18`, bạn đồng ý 20:47):** câu hỏi ngày nhanh — kiểm trên server thật sau merge: sức khoẻ 5 / 5, câu trong kho + ngoài kho đúng, câu "rằm tháng Giêng năm nay" có nhắc Huế đúng ngày (3/3/2026, đã qua), log không chứa câu hỏi; ≈ 0,001 USD.
- **Vào `main` (5081e89):** phần code nhỏ của bản deploy — đọc địa chỉ Qdrant và bật / tắt tra web từ biến môi trường của Docker; không đặt biến ⇒ chatbot trên máy bạn chạy y như cũ (test đạt). Bản deploy chạy thử trên máy đạt mọi điểm kiểm (ảnh 3,6 GB, 0 file riêng tư, quá lượt ⇒ báo 429, hỏi bằng ảnh chạy) — C review 2 vòng đạt.
- C viết nháp kế hoạch so sánh cuối B7 (0 USD); mốc so sánh "RAG 1–8" đã gắn tag `p9-moc` (trước đó spec ghi mà chưa có).
- Bạn chốt: quyền như 09/11, trần 4,2; không chốt mốc đóng tính năng; luật W59 + W61; "cắt test không cần, đẩy nhanh" ⇒ vòng tự soi cắt bớt bộ đo (B bỏ 22 câu kiểm thêm + 5 câu ngày; E thu gọn phần dò ngày, bỏ đo lại mốc cho 9 câu Golden).

## Bạn cần làm gì (khi về — A hỏi mỗi lần một câu)
1. Thay bản câu hỏi ngày nhanh vào chatbot? (A khuyên: có — đạt mọi tiêu chí, nhanh hơn + rẻ hơn.)
2. Câu xã giao chạy song song: bật dù p95 chưa đạt, hay đóng hồ sơ?
3. Câu ngày không nhắc Huế (vd "rằm tháng Giêng năm nay là ngày nào"): 9 / 19 câu đo bị từ chối vì bước phân loại xếp "ngoài phạm vi" — trợ lý Huế có nên trả lời loại câu này?
4. Sắp xếp lại thư mục báo cáo để đọc theo thứ tự (A chuẩn bị 2–3 cách).
- Không gấp: phiếu toạ độ bản đồ · bảng điểm v7 · thu 40 câu giọng nói.

## Trạng thái
| Việc | Kết quả | Ý nghĩa |
|---|---|---|
| Câu ngày tính sẵn (E) | đạt, review đạt, chờ bạn | câu ngày đạt sàn tốc độ + tiền |
| Xã giao song song (B) | chưa đạt p95, review code đạt, chờ bạn | trung vị nhanh hơn ~1,6 s; đuôi chưa đạt |
| Sửa báo cáo (A + agent con, C review) | xong | báo cáo khớp hệ thống đang chạy |
| Deploy chạy trên máy (B) | đang làm | sẵn sàng khi bạn quyết deploy AWS |
| Nháp kế hoạch B7 (C) | nháp xong; tag mốc gắn | chuẩn bị bước so cả hệ với RAG 1–8 |

## Giải thích ngắn (để bạn tự nói lại được)
Câu ngày chậm vì model phải hỏi công cụ rồi mới viết; đổi sang để code tính ngày trước rồi đưa cho model ⇒ bớt vòng gọi, nhanh hơn và rẻ hơn, vẫn đúng ngày. Câu xã giao chậm vì phải chờ phân loại xong mới gọi model; chạy song song bớt được phần chờ ở đa số câu, nhưng vài câu bị phân loại chậm / sai vẫn kéo phần chậm nhất vượt sàn — nên chưa đưa vào.

## Đọc thêm
- Report: `report_agent/2026-11-02_phase_9_code/e_t1_nhanh_implementation.md` (+ `_review.md`), `report_agent/2026-11-08_phase_9_ban_13/b_xa_giao_song_song_implementation.md` (+ `_review.md`), `…/c_sua_bao_cao_1011_review.md`
- Kế hoạch B7 (nháp): `docs/superpowers/plans/2026-11-10-phase-9-b7-plan.md`
