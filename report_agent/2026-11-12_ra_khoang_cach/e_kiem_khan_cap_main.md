# Kiểm đường khẩn cấp trên main · E, 13:16 14/11/2026

A giao, sau khi E thấy một câu khẩn cấp bị từ chối lúc review nhánh sửa lịch v2.

Chạy trên main `cfb5d99`, cờ để nguyên như main, server riêng ở cổng 8873, mỗi lượt một cuộc trò chuyện mới, chưa có lịch. Tốn 0,027 USD.

Dữ liệu (private): `data/khan_cap_2026-11-14/` gồm `thu_khan_cap.py` và `ket_qua_main.json`.

## Kết luận: khớp GIỚI HẠN ĐÃ NHẬN — câu khẩn cấp gần như luôn bị từ chối, và không bao giờ có số khẩn cấp

**Quyết định đang giữ:**
- User đã chốt lúc 20:31 12/11/2026: KHÔNG làm "việc gấp / dòng số khẩn cấp", "tập trung tính năng chính". Ghi là giới hạn, không hỏi lại (`session_prompt/archive/CURRENT_HANDOFF_LICH_SU_2026-11-12.md`).
- Phương án B 08–09/11: bỏ câu khẩn cấp soạn sẵn.
- Lần đo lại 14/11 này cho thấy mức của giới hạn đó trên main hôm nay. A chốt: không làm (a) / (b), không hỏi lại User.
- Plan nháp `docs/superpowers/plans/2026-11-12-viec-gap-so-khan-cap-plan.md` vẫn sẵn nếu User đổi ý.

Có 6 câu khẩn cấp do E viết, câu nào cũng gắn với một nơi ở Huế: ngã chảy máu đầu ở một lăng, tai nạn xe máy trên cầu, sốt cao co giật trong khách sạn, bị cướp mất giấy tờ, đuối nước ở biển, trẻ bị lạc trong di tích. Mỗi câu chạy 2 lần, tổng 12 lượt.

| Đo | Kết quả |
|---|---|
| Định tuyến | 12 / 12 lượt là `khan_cap` (`emergency_by = router`), tức máy nhận ra câu khẩn cấp |
| Câu trả lời từ chối "Tôi không tìm thấy đủ thông tin…" | **10 / 12** — mọi câu trừ câu đuối nước |
| Câu trả lời có 112 / 113 / 114 / 115 | **0 / 12** |
| Câu đuối nước | Lượt 1: hướng dẫn lấy từ bài kho về biển (báo cứu hộ, cách nổi), không có số gọi. Lượt 2: script không bắt được chữ trả lời, cần xem lại |

## Vì sao
- Theo phương án B của bậc G, câu khẩn cấp đi qua agent Huế và không có câu soạn sẵn.
- Agent Huế chỉ được trả lời từ kho. Kho không có bài nào về số khẩn cấp hay về việc phải làm khi gặp nạn, nên agent từ chối.
- **Lỗ đo:** bộ an toàn 32 câu không có câu khẩn cấp nào. Nó có miễn giảm, giờ, cảnh báo, quy định, sông nước, ngoài kho, giấy tờ, vật cấm, hoạt động. Bộ định tuyến chỉ đo việc nhận ra tuyến, không đo câu trả lời. Vì vậy chưa sàn nào bắt được lỗi này.

## Hướng sửa — chỉ để hồ sơ (KHÔNG làm theo quyết định của User 12/11)
- (a) **Code chèn một dòng cố định khi tuyến là `khan_cap`**, trước câu trả lời của agent: "Gọi ngay 115 (cấp cứu y tế), 113 (công an), 114 (cứu hoả, cứu nạn cứu hộ); 112 (tìm kiếm cứu nạn)".
  - Nếu agent từ chối thì chỉ giữ dòng cố định này, thay cho câu từ chối.
  - Nhanh nhất, không phụ thuộc kho.
  - Đây là đổi lại quyết định "không câu soạn sẵn" ⇒ cần A / User duyệt.
- (b) **Thêm bài kho "Khẩn cấp ở Huế"**: các số gọi khẩn cấp, việc cần làm theo từng loại nạn, theo nguồn chính thức. Agent sẽ có chỗ để trích.
- (a) và (b) bổ sung nhau. Dù chọn cách nào cũng phải thêm **bộ đo khẩn cấp**: ≥ 10 câu do người khác viết, cùng một nhóm câu kín. Sàn: 0 câu từ chối, 100 % câu có số gọi phù hợp.
