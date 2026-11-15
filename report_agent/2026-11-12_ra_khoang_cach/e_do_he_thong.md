# Dò hệ thống như người dùng thật sau loạt merge 15/11 (E · 12:20 15/11/2026, `date`)

A giao (0 USD, lượt dò — không sửa). Server tạm `127.0.0.1:8893` trên main `0f739ed` (giao diện dựng lại cùng lúc), Playwright khổ 1440, 5 luồng tới kết quả cuối.
Kịch bản `data/do_he_thong_2026-11-15/tools/pw_5_luong.py`; ảnh toàn trang + số đếm `data/do_he_thong_2026-11-15/anh/`, `ket_qua.json`. Server đã tắt (TaskStop).
**Tiền: 6 lần gọi model ≈ 0,0026 USD.**

## Kết quả

| Luồng | Kết quả | Ảnh |
|---|---|---|
| 1a. Hỏi một món | trả lời bằng kho, 3 nguồn; **2 ảnh** dưới câu (món + một quán), có tên dưới ảnh | `1_chat_mon.png` |
| 1b. Hỏi một di tích | trả lời bằng kho, 2 nguồn (bài di tích + bài cẩm nang); **0 ảnh** ⇒ xem "Phát hiện" | `1_chat_di_tich.png` |
| 1c. So sánh hai quán | trả lời bằng kho, đúng 2 nguồn; **0 ảnh** ⇒ xem "Phát hiện" | `1_chat_so_sanh.png` |
| 2. Lên kế hoạch 3 ngày, chọn "4–5 sao" | 3 ngày, 22 ảnh điểm; Nơi ở **5 cơ sở 4–5 sao, 5 / 5 có ảnh** (gồm La Vela, TTC Imperial, Meliá vừa thay ảnh); 6 bữa | `2_lich_3_ngay_4_5_sao.png` |
| 3. Sửa lịch bằng lời ("chỉ đi 2 ngày") | "Đã đổi số ngày: 3 ngày → 2 ngày"; **mức 4–5 sao giữ nguyên** qua lượt sửa | `3_sua_lich.png` |
| 4. Trang Chỗ ở từ ô Nơi ở | mở `#/cho-o/<khu trung tâm>`, đúng 1 nhóm khu, 122 cơ sở, 55 có ảnh | `4_cho_o.png` |
| 5. Khám phá + mở một bài | 12 thẻ, 0 ảnh hỏng; bài mở được | `5_kham_pha.png`, `5_kham_pha_bai.png` |

- **0 lỗi console, 0 lỗi trang, 0 yêu cầu ra ngoài origin** ở cả 5 luồng. Không thấy chữ lạ (mã `[n]`, `undefined`, thẻ HTML) trong chữ trả lời.
- Thời gian tới khi có nút 👍 (cả câu, qua giao diện): chat 4,4–4,5 s; lịch 4,4 s; sửa lịch 2,4 s. Mỗi loại 1 lượt ⇒ chỉ để xem, không phải số đo.

## Phát hiện (lỗi thật, chưa sửa — báo A)
**Ảnh trong chat hụt ở hai kiểu câu rất thường gặp.** Luật khi câu trích ≥ 2 bài: tên bài (≥ 2 chữ) phải có nguyên văn trong chữ trả lời.
- **So sánh hai quán:** câu trả lời gọi tắt tên quán (bỏ phần tên món đứng trước), không lặp đủ tên bài ⇒ 0 / 2 ảnh, dù cả 2 bài đều là quán có ảnh chắc.
- **Hỏi đích danh một nơi:** người dùng đã nêu tên trong câu hỏi, câu trả lời chỉ nói "lăng", không lặp tên. Nguồn thứ hai là bài cẩm nang (không thuộc loại "một nơi") ⇒ chỉ 1 bài đủ loại, nhưng vẫn rơi vào nhánh "≥ 2 bài" ⇒ 0 ảnh.
- Hướng sửa có thể (cần plan; E chưa đo):
  - (a) đếm "bài một nơi / món có ảnh chắc" TRƯỚC: chỉ có 1 ⇒ dùng luật một bài (không cần tên trong chữ);
  - (b) khớp tên trên cả **câu hỏi của người dùng** lẫn chữ trả lời. Câu hỏi là chữ người dùng, nhưng chỉ dùng để khớp với tên bài trong kho, không hiện ra, không gửi đi.
- Ghi chú phụ: ở ảnh toàn trang, thanh đầu trang (cố định) đè lên dòng tiêu đề khung trợ lý. Nhiều khả năng do cách chụp `full_page` với phần tử cố định, không phải lỗi giao diện. Chưa kiểm bằng ảnh cửa sổ thường.
