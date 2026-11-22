# Điện thoại, trang Trợ lý: nút "Cuộc trò chuyện mới" hết bị thanh điều hướng đáy che — report của phiên C (viết 10:21 22/11/2026)

Lỗi có sẵn từ trước, phiên đo tái hiện trên server thật sáng 22/11 (khổ 390 × 844). Nhánh `p9-c-nut-cuoc-moi-390`: một dòng CSS ở `frontend/src/tl.css`. Người nhìn lại: phiên đo.

## Người dùng thấy gì khác
| Khổ màn hình | Trước | Sau |
|---|---|---|
| Điện thoại (≤ 760 px, có thanh điều hướng đáy) | Sau khi đã hỏi ít nhất một câu, nút "Cuộc trò chuyện mới" nằm DƯỚI thanh đáy và không cuộn lên được; chạm vào là trúng một mục của thanh đáy ⇒ sang trang khác. Không mở được cuộc trò chuyện mới từ trang Trợ lý | Ô nhập, dòng nhắc "Trợ lý AI trả lời từ kho tư liệu…" và nút nằm trọn phía trên thanh đáy; bấm nút ⇒ cuộc trò chuyện về rỗng, vẫn ở trang Trợ lý |
| Máy tính (1440) | — | không đổi (cùng toạ độ từng px) |

## Vì sao
Khung nhập của trang Trợ lý dính ở đáy màn hình. `index.css` có luật riêng cho điện thoại "dính cách đáy 64 px" (chừa chỗ thanh đáy) — `.tro-ly-trang .chat-form { bottom: 64px }`,
hai lớp. `tl.css` (tải sau, cho bố cục mới của trang) có `.tro-ly-trang .tl-chat .chat-form { bottom: 0 }`, BA lớp ⇒ thắng luật kia ở mọi khổ ⇒ khung nhập dính sát đáy,
nửa dưới của nó (dòng nhắc + nút) chui xuống dưới thanh đáy cao 64 px. Sửa: thêm vào `tl.css` đúng luật đó cho khổ ≤ 760 px với cùng độ ưu tiên.

## Số đo [máy kiểm; 0 đồng — lời gọi tới model bị chặn ngay trong trình duyệt, lượt hiện "Không kết nối được máy chủ" nhưng nút vẫn hiện]
Server tạm cổng 8011 từ cây nhánh; cùng phép đo với phiên đo (cuộn hết xuống đáy; vị trí nút ↔ mép trên thanh đáy; phần tử nằm ở tâm nút) + bấm thật vào nút.
Script + ảnh + số (riêng tư): `data/test_cuoi/chay_2026-11-22_c_nut_cuoc_moi/` (`do_nut.py`, `truoc/`, `sau/`).

| Khổ | Mép trên thanh đáy | Nút, TRƯỚC (px từ đỉnh) | Bấm, TRƯỚC | Nút, SAU | Bấm, SAU |
|---|---|---|---|---|---|
| 390 × 844 | 780 | 782–818 (dưới thanh đáy; ở tâm nút là một mục của thanh đáy) | không bấm được (hết 4 giây) | 718–754 | được; cuộc trò chuyện về 0 lượt; còn ở trang Trợ lý |
| 360 × 740 | 676 | 678–714 | không bấm được | 614–650 | được |
| 760 × 900 (mép khổ có thanh đáy) | 836 | 838–874 | không bấm được | 774–810 | được |
| 1440 × 1000 | không có thanh đáy | 861–897 | được | 861–897 | được |

Dòng nhắc và ô nhập ở ba khổ hẹp: thấy trọn cả trước lẫn sau ở phép đo của tôi (phiên đo thấy dòng nhắc bị cắt nửa dưới ở lượt có câu trả lời thật — vị trí cuộn khác); sau khi
sửa cả hai nằm cách mép thanh đáy ít nhất 26 px. Tràn ngang 0, lỗi trang 0 ở cả bốn khổ, trước và sau.

## Chưa làm · giới hạn
- CHƯA: phiên đo nhìn lại trên lượt có câu trả lời thật; dựng lại `frontend/dist` ở cây chính sau khi gộp (`cd frontend && npm run build`).
- Chỉ đo Chromium không màn hình; chưa thử điện thoại thật (thanh công cụ của trình duyệt điện thoại có thể che thêm vài px — khung nhập đã cách thanh đáy đúng 0 px như thiết kế cũ ở `index.css`).
- Khổ 761–980 px không có thanh đáy nên giữ `bottom: 0` (không đo riêng).
- Frontend không có bộ test tự động; bằng chứng là phép đo trình duyệt trên.

Phép này KHÔNG cho biết các trang khác có phần tử nào chui dưới thanh đáy không · hướng rộng hơn: một phép quét mọi trang ở khổ 390 tìm nút / link có tâm bị thanh đáy che · đếm rẻ nhất: chính phép quét đó, 0 đồng.
